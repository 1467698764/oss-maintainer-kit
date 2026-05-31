from pathlib import Path

from oss_maintainer_kit.rules import evaluate_rules
from oss_maintainer_kit.scanner import scan_repository
from oss_maintainer_kit.scoring import calculate_score


def write(path: Path, text: str = "content") -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def test_rules_identify_missing_maintenance_basics(tmp_path: Path) -> None:
    write(tmp_path / "README.md", "short")
    write(tmp_path / "pyproject.toml", "[project]\nname='demo'")

    findings = evaluate_rules(scan_repository(tmp_path))
    by_id = {finding.rule_id: finding for finding in findings}

    assert by_id["readme-depth"].status == "fail"
    assert by_id["license"].status == "fail"
    assert by_id["tests"].status == "fail"
    assert by_id["ci"].status == "fail"
    assert by_id["package-manifest"].status == "pass"
    assert by_id["security-policy"].severity == "medium"


def test_score_rewards_complete_repository_and_grades_result(tmp_path: Path) -> None:
    write(tmp_path / "README.md", "# Demo\n\n" + "docs " * 80)
    write(tmp_path / "LICENSE", "MIT")
    write(tmp_path / "pyproject.toml", "[project]\nname='demo'")
    write(tmp_path / "tests" / "test_demo.py", "def test_demo(): assert True")
    write(tmp_path / ".github" / "workflows" / "ci.yml", "name: CI")
    write(tmp_path / "CONTRIBUTING.md", "How")
    write(tmp_path / ".github" / "ISSUE_TEMPLATE" / "bug.md", "Bug")
    write(tmp_path / ".github" / "pull_request_template.md", "PR")
    write(tmp_path / "CHANGELOG.md", "# Changelog")
    write(tmp_path / "SECURITY.md", "# Security")

    score = calculate_score(evaluate_rules(scan_repository(tmp_path)))

    assert score.points == 100
    assert score.grade == "excellent"
    assert score.passed == score.total_rules
    assert score.failed == 0


def test_score_prioritizes_high_impact_failures(tmp_path: Path) -> None:
    write(tmp_path / "README.md", "short")

    score = calculate_score(evaluate_rules(scan_repository(tmp_path)))

    assert score.points < 50
    assert score.top_recommendations[0].rule_id in {
        "license",
        "package-manifest",
        "readme-depth",
        "tests",
        "ci",
    }
