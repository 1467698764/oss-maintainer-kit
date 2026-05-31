from __future__ import annotations

from pathlib import Path

from .models import TemplateInitResult

TEMPLATES: dict[str, str] = {
    "CONTRIBUTING.md": """# Contributing

Thanks for considering a contribution.

## Local setup

1. Fork and clone the repository.
2. Create a development environment.
3. Install dependencies.
4. Run the test suite before opening a pull request.

## Pull requests

Please include a clear description, tests for behavior changes, and documentation updates.
""",
    "SECURITY.md": """# Security Policy

## Reporting a vulnerability

Please do not open public issues for security vulnerabilities. Contact the maintainer privately
with reproduction steps, affected versions, and impact.

## Supported versions

The latest release receives security fixes.
""",
    ".github/ISSUE_TEMPLATE/bug_report.md": """---
name: Bug report
about: Report reproducible behavior that should be fixed
---

## What happened?

## Expected behavior

## Reproduction steps

## Environment
""",
    ".github/ISSUE_TEMPLATE/feature_request.md": """---
name: Feature request
about: Suggest a focused improvement
---

## Problem

## Proposed solution

## Alternatives considered
""",
    ".github/pull_request_template.md": """## Summary

## Verification

- [ ] Tests pass locally
- [ ] Documentation updated if needed
- [ ] Change is small enough to review
""",
}


def init_templates(path: str | Path, *, force: bool = False) -> TemplateInitResult:
    root = Path(path).expanduser().resolve()
    if not root.exists():
        raise FileNotFoundError(f"Repository path does not exist: {path}")
    created: list[str] = []
    skipped: list[str] = []

    for relative, content in TEMPLATES.items():
        destination = root / relative
        if destination.exists() and not force:
            skipped.append(relative)
            continue
        destination.parent.mkdir(parents=True, exist_ok=True)
        destination.write_text(content, encoding="utf-8")
        created.append(relative)

    return TemplateInitResult(created=created, skipped=skipped)
