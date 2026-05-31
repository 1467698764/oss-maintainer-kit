from pathlib import Path

from oss_maintainer_kit.config import load_config
from oss_maintainer_kit.rules import evaluate_rules
from oss_maintainer_kit.scanner import scan_repository
from oss_maintainer_kit.scoring import calculate_score


def test_load_config_reads_min_score_and_rule_weights(tmp_path: Path) -> None:
    (tmp_path / "omk.toml").write_text(
        """
min_score = 85

[rule_weights]
license = 30
tests = 20
""".strip(),
        encoding="utf-8",
    )

    config = load_config(tmp_path)

    assert config.min_score == 85
    assert config.rule_weights == {"license": 30, "tests": 20}


def test_load_config_returns_defaults_when_file_is_missing(tmp_path: Path) -> None:
    config = load_config(tmp_path)

    assert config.min_score == 75
    assert config.rule_weights == {}


def test_configured_rule_weights_affect_score(tmp_path: Path) -> None:
    (tmp_path / "README.md").write_text("# Demo\n\n" + "docs " * 40, encoding="utf-8")
    (tmp_path / "omk.toml").write_text(
        """
[rule_weights]
readme-depth = 1
license = 99
""".strip(),
        encoding="utf-8",
    )

    scan = scan_repository(tmp_path)
    config = load_config(tmp_path)
    findings = evaluate_rules(scan, config=config)
    score = calculate_score(findings)

    assert next(item for item in findings if item.rule_id == "license").weight == 99
    assert score.points < 10
    assert score.top_recommendations[0].rule_id == "license"


def test_load_config_accepts_utf8_bom_files(tmp_path: Path) -> None:
    (tmp_path / "omk.toml").write_text("min_score = 92\n", encoding="utf-8-sig")

    config = load_config(tmp_path)

    assert config.min_score == 92
