from __future__ import annotations

from urllib.parse import quote

GRADE_COLORS = {
    "excellent": "brightgreen",
    "healthy": "brightgreen",
    "needs-work": "yellow",
    "starter": "orange",
}


def render_markdown_badge(points: int, grade: str) -> str:
    """Render a Shields.io Markdown badge for the current OSS health score."""
    color = GRADE_COLORS.get(grade, "lightgrey")
    message = quote(f"{points}/100_{grade}", safe="")
    return f"![OSS health](https://img.shields.io/badge/OSS_health-{message}-{color})"
