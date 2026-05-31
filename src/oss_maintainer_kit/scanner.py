from __future__ import annotations

import re
from pathlib import Path

from .models import RepositoryEvidence, RepositoryProfile, ScanResult

MANIFEST_TYPES = {
    "pyproject.toml": "python",
    "setup.py": "python",
    "requirements.txt": "python",
    "package.json": "javascript",
    "Cargo.toml": "rust",
    "go.mod": "go",
    "pom.xml": "java",
    "build.gradle": "java",
}

README_NAMES = ("README.md", "README.rst", "README.txt", "README")
LICENSE_NAMES = ("LICENSE", "LICENSE.md", "COPYING", "COPYING.md")
CHANGELOG_NAMES = ("CHANGELOG.md", "CHANGELOG", "HISTORY.md", "RELEASES.md")
SECURITY_NAMES = ("SECURITY.md", ".github/SECURITY.md")
CONTRIBUTING_NAMES = ("CONTRIBUTING.md", ".github/CONTRIBUTING.md")


def scan_repository(path: str | Path) -> ScanResult:
    root = Path(path).expanduser().resolve()
    if not root.exists():
        raise FileNotFoundError(f"Repository path does not exist: {path}")
    if not root.is_dir():
        raise NotADirectoryError(f"Repository path is not a directory: {path}")

    manifests = sorted(name for name in MANIFEST_TYPES if (root / name).exists())
    project_types = sorted({MANIFEST_TYPES[name] for name in manifests})
    readme = _first_existing(root, README_NAMES)

    evidence = RepositoryEvidence(
        has_readme=readme is not None,
        readme_words=_word_count(readme) if readme else 0,
        has_license=_any_exists(root, LICENSE_NAMES),
        has_tests=_has_tests(root),
        has_ci=_has_ci(root),
        has_contributing=_any_exists(root, CONTRIBUTING_NAMES),
        has_issue_template=_has_issue_template(root),
        has_pr_template=_has_pr_template(root),
        has_changelog=_any_exists(root, CHANGELOG_NAMES),
        has_security_policy=_any_exists(root, SECURITY_NAMES),
        manifests=manifests,
    )
    return ScanResult(
        root=root,
        profile=RepositoryProfile(project_types=project_types),
        evidence=evidence,
    )


def _first_existing(root: Path, names: tuple[str, ...]) -> Path | None:
    return next((root / name for name in names if (root / name).exists()), None)


def _any_exists(root: Path, names: tuple[str, ...]) -> bool:
    return any((root / name).exists() for name in names)


def _word_count(path: Path) -> int:
    text = path.read_text(encoding="utf-8", errors="ignore")
    return len(re.findall(r"\b[\w'-]+\b", text))


def _has_tests(root: Path) -> bool:
    common_dirs = ("tests", "test", "spec", "__tests__")
    if any((root / name).is_dir() for name in common_dirs):
        return True
    patterns = ("test_*.py", "*_test.py", "*.test.js", "*.spec.js", "*.test.ts", "*.spec.ts")
    return any(next(root.rglob(pattern), None) is not None for pattern in patterns)


def _has_ci(root: Path) -> bool:
    if (root / ".github" / "workflows").is_dir():
        return any((root / ".github" / "workflows").glob("*.yml")) or any(
            (root / ".github" / "workflows").glob("*.yaml")
        )
    return any((root / name).exists() for name in (".gitlab-ci.yml", ".circleci/config.yml"))


def _has_issue_template(root: Path) -> bool:
    return (root / ".github" / "ISSUE_TEMPLATE").is_dir() or (
        root / ".github" / "ISSUE_TEMPLATE.md"
    ).exists()


def _has_pr_template(root: Path) -> bool:
    names = (
        ".github/pull_request_template.md",
        ".github/PULL_REQUEST_TEMPLATE.md",
        "pull_request_template.md",
        "PULL_REQUEST_TEMPLATE.md",
    )
    return _any_exists(root, names)
