from __future__ import annotations

from .models import RuleFinding, ScoreResult

SEVERITY_RANK = {"high": 0, "medium": 1, "low": 2}


def calculate_score(findings: list[RuleFinding]) -> ScoreResult:
    total_weight = sum(item.weight for item in findings)
    earned = sum(item.weight for item in findings if item.status == "pass")
    points = round((earned / total_weight) * 100) if total_weight else 0
    failed = [item for item in findings if item.status == "fail"]
    recommendations = sorted(
        failed,
        key=lambda item: (SEVERITY_RANK[item.severity], -item.weight, item.rule_id),
    )[:5]
    return ScoreResult(
        points=points,
        grade=_grade(points),
        passed=sum(1 for item in findings if item.status == "pass"),
        failed=len(failed),
        total_rules=len(findings),
        top_recommendations=recommendations,
    )


def _grade(points: int) -> str:
    if points >= 90:
        return "excellent"
    if points >= 75:
        return "healthy"
    if points >= 50:
        return "needs-work"
    return "starter"
