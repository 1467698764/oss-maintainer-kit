from pathlib import Path

from oss_maintainer_kit.scanner import scan_repository


def write(path: Path, text: str = "content") -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def test_scan_repository_detects_oss_maintenance_evidence(tmp_path: Path) -> None:
    write(tmp_path / "README.md", "# Demo\n\n" + "useful docs " * 30)
    write(tmp_path / "LICENSE", "MIT License")
    write(tmp_path / "pyproject.toml", "[project]\nname='demo'")
    write(tmp_path / "tests" / "test_demo.py", "def test_demo(): assert True")
    write(tmp_path / ".github" / "workflows" / "ci.yml", "name: CI")
    write(tmp_path / "CONTRIBUTING.md", "How to contribute")
    write(tmp_path / ".github" / "ISSUE_TEMPLATE" / "bug_report.md", "Bug")
    write(tmp_path / ".github" / "pull_request_template.md", "Checklist")
    write(tmp_path / "CHANGELOG.md", "# Changelog")
    write(tmp_path / "SECURITY.md", "# Security")

    result = scan_repository(tmp_path)

    assert result.root == tmp_path.resolve()
    assert result.profile.project_types == ["python"]
    assert result.evidence.has_readme is True
    assert result.evidence.readme_words >= 30
    assert result.evidence.has_license is True
    assert result.evidence.has_tests is True
    assert result.evidence.has_ci is True
    assert result.evidence.has_contributing is True
    assert result.evidence.has_issue_template is True
    assert result.evidence.has_pr_template is True
    assert result.evidence.has_changelog is True
    assert result.evidence.has_security_policy is True
    assert "pyproject.toml" in result.evidence.manifests


def test_scan_repository_raises_for_missing_path(tmp_path: Path) -> None:
    missing = tmp_path / "missing"

    try:
        scan_repository(missing)
    except FileNotFoundError as exc:
        assert str(missing) in str(exc)
    else:
        raise AssertionError("scan_repository should reject a missing path")
