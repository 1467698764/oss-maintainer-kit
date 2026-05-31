import json
from pathlib import Path

from oss_maintainer_kit.report import render_json_report, render_markdown_report
from oss_maintainer_kit.rules import evaluate_rules
from oss_maintainer_kit.scanner import scan_repository
from oss_maintainer_kit.scoring import calculate_score


def test_markdown_report_contains_score_findings_and_recommendations(tmp_path: Path) -> None:
    (tmp_path / "README.md").write_text("short", encoding="utf-8")
    findings = evaluate_rules(scan_repository(tmp_path))
    score = calculate_score(findings)

    markdown = render_markdown_report(scan_repository(tmp_path), findings, score)

    assert markdown.startswith("# OSS Maintainer Kit Report")
    assert "Health score" in markdown
    assert "readme-depth" in markdown
    assert "Top recommendations" in markdown


def test_json_report_is_machine_readable_and_deterministic(tmp_path: Path) -> None:
    (tmp_path / "README.md").write_text("short", encoding="utf-8")
    scan = scan_repository(tmp_path)
    findings = evaluate_rules(scan)
    score = calculate_score(findings)

    payload = json.loads(render_json_report(scan, findings, score))

    assert payload["score"]["points"] == score.points
    assert payload["repository"]["root"] == str(tmp_path.resolve())
    assert payload["findings"][0]["rule_id"] <= payload["findings"][-1]["rule_id"]


def test_markdown_report_uses_ascii_status_for_console_portability(tmp_path: Path) -> None:
    (tmp_path / "README.md").write_text("short", encoding="utf-8")
    scan = scan_repository(tmp_path)
    findings = evaluate_rules(scan)
    score = calculate_score(findings)

    markdown = render_markdown_report(scan, findings, score)

    assert "✅" not in markdown
    assert "❌" not in markdown
    assert "—" not in markdown
    assert "FAIL fail" in markdown
