from pathlib import Path

from oss_maintainer_kit.badge import render_markdown_badge


def test_render_markdown_badge_uses_grade_color_and_score() -> None:
    badge = render_markdown_badge(87, "healthy")

    assert badge == (
        "![OSS health](https://img.shields.io/badge/OSS_health-87%2F100_healthy-brightgreen)"
    )


def test_cli_badge_outputs_markdown_badge(tmp_path: Path, capsys) -> None:
    (tmp_path / "README.md").write_text("# Demo\n\n" + "docs " * 40, encoding="utf-8")
    (tmp_path / "LICENSE").write_text("MIT", encoding="utf-8")
    (tmp_path / "pyproject.toml").write_text("[project]\nname='demo'", encoding="utf-8")
    (tmp_path / "tests").mkdir()

    from oss_maintainer_kit.cli import main

    exit_code = main(["badge", str(tmp_path)])

    captured = capsys.readouterr()
    assert exit_code == 0
    assert captured.out.startswith("![OSS health](https://img.shields.io/badge/OSS_health-")


def test_cli_audit_fails_when_score_is_below_threshold(tmp_path: Path, capsys) -> None:
    (tmp_path / "README.md").write_text("short", encoding="utf-8")

    from oss_maintainer_kit.cli import main

    exit_code = main(["audit", str(tmp_path), "--min-score", "80"])

    captured = capsys.readouterr()
    assert exit_code == 1
    assert "below required minimum" in captured.out


def test_cli_audit_passes_when_score_meets_threshold(tmp_path: Path, capsys) -> None:
    (tmp_path / "README.md").write_text("# Demo\n\n" + "docs " * 40, encoding="utf-8")
    (tmp_path / "LICENSE").write_text("MIT", encoding="utf-8")
    (tmp_path / "pyproject.toml").write_text("[project]\nname='demo'", encoding="utf-8")
    (tmp_path / "tests").mkdir()
    (tmp_path / ".github" / "workflows").mkdir(parents=True)
    (tmp_path / ".github" / "workflows" / "ci.yml").write_text("name: CI", encoding="utf-8")
    (tmp_path / "CONTRIBUTING.md").write_text("guide", encoding="utf-8")
    (tmp_path / ".github" / "ISSUE_TEMPLATE").mkdir()
    (tmp_path / ".github" / "ISSUE_TEMPLATE" / "bug.md").write_text("bug", encoding="utf-8")
    (tmp_path / ".github" / "pull_request_template.md").write_text("pr", encoding="utf-8")
    (tmp_path / "CHANGELOG.md").write_text("changes", encoding="utf-8")
    (tmp_path / "SECURITY.md").write_text("security", encoding="utf-8")

    from oss_maintainer_kit.cli import main

    exit_code = main(["audit", str(tmp_path), "--min-score", "90"])

    captured = capsys.readouterr()
    assert exit_code == 0
    assert "meets required minimum" in captured.out
