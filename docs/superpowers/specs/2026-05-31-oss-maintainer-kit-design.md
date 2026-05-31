# oss-maintainer-kit Design

## Purpose

`oss-maintainer-kit` is an offline-first CLI for solo and small-team open-source maintainers. It scans a repository, identifies common maintenance gaps, scores repository health, and generates practical contributor-facing templates.

## Target Users

- Solo maintainers preparing a project for public collaboration.
- Developers who want a quick OSS readiness audit before publishing.
- Maintainers who need repeatable Markdown or JSON reports for project hygiene.

## Core User Flows

1. Run `omk scan .` to inspect repository evidence such as README, LICENSE, tests, CI, templates, changelog, security policy, and package manifests.
2. Run `omk score .` to get a 0-100 maintenance health score with prioritized findings.
3. Run `omk report . --format markdown` to produce a shareable report.
4. Run `omk init-templates .` to create starter `CONTRIBUTING.md`, `SECURITY.md`, issue templates, and pull request template without overwriting existing files unless `--force` is supplied.

## Architecture

The package is split into small modules:

- `models.py`: immutable dataclasses for repository profiles, rule findings, scan results, and scores.
- `scanner.py`: filesystem inspection and project type detection.
- `rules.py`: rule catalog that converts scan evidence into findings.
- `scoring.py`: weighted scoring and priority ordering.
- `report.py`: JSON and Markdown rendering.
- `templates.py`: safe template creation.
- `cli.py`: argparse-based command line interface.

The default implementation uses only the Python standard library so the tool works offline and in fresh environments.

## Rule Set

The first release checks for:

- README with meaningful length.
- OSI-style license file presence.
- Test directory or language-specific test files.
- CI workflow under `.github/workflows`.
- Package manifest such as `pyproject.toml`, `package.json`, `Cargo.toml`, `go.mod`, or similar.
- Contribution guide.
- Issue and pull request templates.
- Changelog.
- Security policy.

## Error Handling

- Missing target path returns a clear CLI error and non-zero exit.
- Existing generated files are skipped by default.
- `--force` overwrites generated template files intentionally.
- Reports are deterministic for stable tests and reliable diffs.

## Testing Strategy

Tests use temporary directories to model repositories. Coverage focuses on scanner evidence, rule findings, scoring math, report rendering, template safety, and CLI behavior.

## Non-goals for v1

- No network calls.
- No required OpenAI API key.
- No hosted service or database.
- No automatic repository mutation except explicit template initialization.
