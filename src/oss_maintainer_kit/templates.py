from __future__ import annotations

from pathlib import Path

from .models import TemplateInitResult

TEMPLATES: dict[str, str] = {
    "CONTRIBUTING.md": """# Contributing\n\nThanks for considering a contribution.\n\n## Local setup\n\n1. Fork and clone the repository.\n2. Create a virtual environment or language-specific development environment.\n3. Install dependencies.\n4. Run the test suite before opening a pull request.\n\n## Pull requests\n\nPlease include a clear description, tests for behavior changes, and documentation updates when needed.\n""",
    "SECURITY.md": """# Security Policy\n\n## Reporting a vulnerability\n\nPlease do not open public issues for security vulnerabilities. Contact the maintainer privately with reproduction steps, affected versions, and impact.\n\n## Supported versions\n\nThe latest release receives security fixes.\n""",
    ".github/ISSUE_TEMPLATE/bug_report.md": """---\nname: Bug report\nabout: Report reproducible behavior that should be fixed\n---\n\n## What happened?\n\n## Expected behavior\n\n## Reproduction steps\n\n## Environment\n""",
    ".github/ISSUE_TEMPLATE/feature_request.md": """---\nname: Feature request\nabout: Suggest a focused improvement\n---\n\n## Problem\n\n## Proposed solution\n\n## Alternatives considered\n""",
    ".github/pull_request_template.md": """## Summary\n\n## Verification\n\n- [ ] Tests pass locally\n- [ ] Documentation updated if needed\n- [ ] Change is small enough to review\n""",
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
