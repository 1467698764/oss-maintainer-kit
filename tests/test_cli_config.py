from pathlib import Path

from oss_maintainer_kit.cli import main


def test_cli_audit_uses_min_score_from_omk_config(tmp_path: Path, capsys) -> None:
    (tmp_path / "README.md").write_text("short", encoding="utf-8")
    (tmp_path / "omk.toml").write_text("min_score = 0\n", encoding="utf-8")

    exit_code = main(["audit", str(tmp_path)])

    captured = capsys.readouterr()
    assert exit_code == 0
    assert "meets required minimum 0/100" in captured.out


def test_cli_score_uses_rule_weights_from_omk_config(tmp_path: Path, capsys) -> None:
    (tmp_path / "README.md").write_text("# Demo\n\n" + "docs " * 40, encoding="utf-8")
    (tmp_path / "omk.toml").write_text(
        """
[rule_weights]
readme-depth = 1
license = 99
""".strip(),
        encoding="utf-8",
    )

    exit_code = main(["score", str(tmp_path)])

    captured = capsys.readouterr()
    assert exit_code == 0
    assert "Health score: 1/100" in captured.out
