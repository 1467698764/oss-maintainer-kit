# Contributing

Thank you for helping improve OSS Maintainer Kit.

## Local setup

```bash
git clone https://github.com/alphahui/oss-maintainer-kit.git
cd oss-maintainer-kit
python -m pip install -e .
python -m pip install pytest ruff build
```

## Checks

Run these before opening a pull request:

```bash
python -m pytest
python -m ruff check .
python -m build
```

## Pull request guidance

- Keep changes focused and reviewable.
- Add or update tests for behavior changes.
- Update documentation when commands, rules, or output change.
- Prefer deterministic output so reports are easy to diff.
