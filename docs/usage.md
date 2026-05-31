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

## Audit gate

```bash
omk audit .
omk audit . --min-score 80
```

The audit command exits with status code `1` when the score is below the configured threshold. This makes it useful in CI jobs that should block releases until the repository has basic maintainer-facing files.

When `--min-score` is omitted, `omk audit` uses `min_score` from `omk.toml`, or `75` if no configuration file exists.

## Badge

```bash
omk badge .
```

The badge command prints a Markdown Shields.io badge such as:

```markdown
![OSS health](https://img.shields.io/badge/OSS_health-100%2F100_excellent-brightgreen)
```

## Initialize templates

```bash
omk init-templates .
omk init-templates . --force
```

Without `--force`, existing files are skipped. With `--force`, generated files are overwritten intentionally.
