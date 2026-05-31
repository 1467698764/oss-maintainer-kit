from pathlib import Path

from oss_maintainer_kit.cli import main


def test_cli_scan_outputs_repository_summary(tmp_path: Path, capsys) -> None:
    (tmp_path / "README.md").write_text("short", encoding="utf-8")

    exit_code = main(["scan", str(tmp_path)])

    captured = capsys.readouterr()
    assert exit_code == 0
    assert "Repository" in captured.out
    assert "README" in captured.out


def test_cli_report_can_emit_markdown(tmp_path: Path, capsys) -> None:
    (tmp_path / "README.md").write_text("short", encoding="utf-8")

    exit_code = main(["report", str(tmp_path), "--format", "markdown"])

    captured = capsys.readouterr()
    assert exit_code == 0
    assert "# OSS Maintainer Kit Report" in captured.out


def test_cli_init_templates_reports_created_files(tmp_path: Path, capsys) -> None:
    exit_code = main(["init-templates", str(tmp_path)])

    captured = capsys.readouterr()
    assert exit_code == 0
    assert "Created" in captured.out
    assert (tmp_path / "CONTRIBUTING.md").exists()
