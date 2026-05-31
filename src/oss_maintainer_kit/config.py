from __future__ import annotations

import sys
from dataclasses import dataclass, field
from pathlib import Path

if sys.version_info >= (3, 11):
    import tomllib
else:  # pragma: no cover - exercised only on Python 3.10
    import tomli as tomllib


@dataclass(frozen=True)
class OmkConfig:
    min_score: int = 75
    rule_weights: dict[str, int] = field(default_factory=dict)


def load_config(path: str | Path) -> OmkConfig:
    root = Path(path).expanduser().resolve()
    config_path = root / "omk.toml"
    if not config_path.exists():
        return OmkConfig()

    payload = tomllib.loads(config_path.read_text(encoding="utf-8-sig"))

    min_score = int(payload.get("min_score", 75))
    weights = payload.get("rule_weights", {})
    if not isinstance(weights, dict):
        raise ValueError("omk.toml [rule_weights] must be a table")

    return OmkConfig(
        min_score=min_score,
        rule_weights={str(rule_id): int(weight) for rule_id, weight in weights.items()},
    )
