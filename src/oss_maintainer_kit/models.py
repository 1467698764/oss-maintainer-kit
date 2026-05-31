from __future__ import annotations

from dataclasses import asdict, dataclass, field
from pathlib import Path
from typing import Literal

FindingStatus = Literal["pass", "fail"]
FindingSeverity = Literal["low", "medium", "high"]


@dataclass(frozen=True)
class RepositoryProfile:
    project_types: list[str]


@dataclass(frozen=True)
class RepositoryEvidence:
    has_readme: bool = False
    readme_words: int = 0
    has_license: bool = False
    has_tests: bool = False
    has_ci: bool = False
    has_contributing: bool = False
    has_issue_template: bool = False
    has_pr_template: bool = False
    has_changelog: bool = False
    has_security_policy: bool = False
    manifests: list[str] = field(default_factory=list)


@dataclass(frozen=True)
class ScanResult:
    root: Path
    profile: RepositoryProfile
    evidence: RepositoryEvidence


@dataclass(frozen=True)
class RuleFinding:
    rule_id: str
    title: str
    status: FindingStatus
    severity: FindingSeverity
    weight: int
    message: str
    recommendation: str

    def to_dict(self) -> dict[str, object]:
        return asdict(self)


@dataclass(frozen=True)
class ScoreResult:
    points: int
    grade: str
    passed: int
    failed: int
    total_rules: int
    top_recommendations: list[RuleFinding]

    def to_dict(self) -> dict[str, object]:
        data = asdict(self)
        data["top_recommendations"] = [item.to_dict() for item in self.top_recommendations]
        return data


@dataclass(frozen=True)
class TemplateInitResult:
    created: list[str]
    skipped: list[str]
