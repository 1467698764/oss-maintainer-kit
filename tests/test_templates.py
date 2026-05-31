from pathlib import Path

from oss_maintainer_kit.templates import init_templates


def test_init_templates_creates_contributor_files_without_overwriting(tmp_path: Path) -> None:
    existing = tmp_path / "CONTRIBUTING.md"
    existing.write_text("custom", encoding="utf-8")

    result = init_templates(tmp_path)

    assert existing.read_text(encoding="utf-8") == "custom"
    assert "CONTRIBUTING.md" in result.skipped
    assert (tmp_path / "SECURITY.md").exists()
    assert (tmp_path / ".github" / "ISSUE_TEMPLATE" / "bug_report.md").exists()
    assert (tmp_path / ".github" / "pull_request_template.md").exists()
    assert "SECURITY.md" in result.created


def test_init_templates_force_overwrites_existing_files(tmp_path: Path) -> None:
    existing = tmp_path / "CONTRIBUTING.md"
    existing.write_text("custom", encoding="utf-8")

    result = init_templates(tmp_path, force=True)

    assert "CONTRIBUTING.md" in result.created
    assert "custom" not in existing.read_text(encoding="utf-8")
