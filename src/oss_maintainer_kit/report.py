from __future__ import annotations

import json
from dataclasses import asdict

from .models import RuleFinding, ScanResult, ScoreResult


def render_json_report(scan: ScanResult, findings: list[RuleFinding], score: ScoreResult) -> str:
    payload = {
        "repository": {
            "root": str(scan.root),
            "project_types": scan.profile.project_types,
            "evidence": asdict(scan.evidence),
        },
        "score": score.to_dict(),
        "findings": [finding.to_dict() for finding in sorted(findings, key=lambda item: item.rule_id)],
    }
    return json.dumps(payload, indent=2, sort_keys=True) + "\n"


def render_markdown_report(scan: ScanResult, findings: list[RuleFinding], score: ScoreResult) -> str:
    lines = [
        "# OSS Maintainer Kit Report",
        "",
        f"Repository: `{scan.root}`",
        f"Project types: {', '.join(scan.profile.project_types) if scan.profile.project_types else 'unknown'}",
        "",
        "## Health score",
        "",
        f"**{score.points}/100** — `{score.grade}` ({score.passed}/{score.total_rules} checks passing)",
        "",
        "## Findings",
        "",
        "| Rule | Status | Severity | Message |",
        "| --- | --- | --- | --- |",
    ]
    for finding in sorted(findings, key=lambda item: item.rule_id):
        icon = "✅" if finding.status == "pass" else "❌"
        lines.append(f"| `{finding.rule_id}` | {icon} {finding.status} | {finding.severity} | {finding.message} |")

    lines.extend(["", "## Top recommendations", ""])
    if score.top_recommendations:
        for index, finding in enumerate(score.top_recommendations, start=1):
            lines.append(f"{index}. **{finding.title}** — {finding.recommendation}")
    else:
        lines.append("No immediate recommendations. Keep maintaining the project.")
    lines.append("")
    return "\n".join(lines)
