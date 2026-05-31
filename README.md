# OSS Maintainer Kit

[![CI](https://github.com/alphahui/oss-maintainer-kit/actions/workflows/ci.yml/badge.svg)](https://github.com/alphahui/oss-maintainer-kit/actions/workflows/ci.yml)
[![Python](https://img.shields.io/badge/python-3.10%2B-blue.svg)](https://www.python.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

`oss-maintainer-kit` (`omk`) is an offline-first command line assistant for open-source maintainers. It scans a repository for practical maintenance signals, scores OSS readiness, renders shareable reports, and initializes contributor-facing templates.

The project is designed for solo maintainers who want a repeatable checklist before inviting contributors or submitting an open-source project for review.

## Why this exists

Small open-source projects often fail to communicate the basics: what the project does, how to run tests, how to report bugs, what license applies, and how contributors should open pull requests. `omk` turns those expectations into a deterministic local audit that can run in CI or before a release.

## Features

- Offline repository health scanning; no account or network required.
- Weighted 0-100 maintenance score with grade labels.
- Rule findings for README depth, license, tests, CI, package manifests, contribution guide, templates, changelog, and security policy.
- Markdown and JSON reports for humans and automation.
- Safe template initialization that skips existing files unless `--force` is used.
- Pure Python runtime with a small, testable module structure.

## Installation

From a checkout:

```bash
python -m pip install -e .
```

After installation, the `omk` command is available:

```bash
omk --help
```

## Quick start

Audit the current repository:

```bash
omk scan .
omk score .
omk report . --format markdown
```

Create starter contributor templates:

```bash
omk init-templates .
```

Write a JSON report for automation:

```bash
omk report . --format json --output omk-report.json
```

## Example output

```text
Health score: 100/100 (excellent)
Passing checks: 10/10
```

A Markdown report starts with:

```markdown
# OSS Maintainer Kit Report

## Health score

**100/100** — `excellent`
```

## Commands

| Command | Purpose |
| --- | --- |
| `omk scan <path>` | Print repository evidence summary. |
| `omk score <path>` | Print score and prioritized recommendations. |
| `omk report <path>` | Render Markdown or JSON report. |
| `omk init-templates <path>` | Create CONTRIBUTING, SECURITY, issue, and PR templates. |

See [`docs/usage.md`](docs/usage.md) and [`docs/rule-reference.md`](docs/rule-reference.md) for details.

## Development

```bash
python -m pip install -e .
python -m pip install pytest ruff build
python -m pytest
python -m ruff check .
python -m build
```

## Project status

This is an early but usable release focused on deterministic local audits. Planned next steps are tracked in [`docs/roadmap.md`](docs/roadmap.md).

## License

MIT. See [`LICENSE`](LICENSE).
