# Usage Guide

`omk` accepts a repository path. If no path is supplied, it scans the current working directory.

## Scan

```bash
omk scan .
```

The scan command prints direct evidence: detected project types, README word count, license presence, tests, CI, and package manifests.

## Score

```bash
omk score .
```

The score command evaluates all rules and prints a grade:

- `excellent`: 90-100
- `healthy`: 75-89
- `needs-work`: 50-74
- `starter`: 0-49

## Report

```bash
omk report . --format markdown
omk report . --format json --output omk-report.json
```

Markdown is intended for maintainers and project discussions. JSON is intended for automation and CI checks.

## Initialize templates

```bash
omk init-templates .
omk init-templates . --force
```

Without `--force`, existing files are skipped. With `--force`, generated files are overwritten intentionally.
