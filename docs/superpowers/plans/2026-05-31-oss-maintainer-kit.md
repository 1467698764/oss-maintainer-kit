# oss-maintainer-kit Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build a polished offline-first OSS maintenance audit CLI suitable as a public open-source project.

**Architecture:** A pure-Python package with focused modules for scanning repository evidence, evaluating maintenance rules, computing scores, rendering reports, creating templates, and exposing an argparse CLI. Tests use pytest fixtures and temporary repositories.

**Tech Stack:** Python 3.10+, pytest, ruff, standard-library argparse/dataclasses/pathlib/json.

---

## File Structure

- `pyproject.toml`: package metadata, console script, pytest and ruff config.
- `src/oss_maintainer_kit/models.py`: dataclasses and typed result objects.
- `src/oss_maintainer_kit/scanner.py`: repository evidence scanning.
- `src/oss_maintainer_kit/rules.py`: rule definitions and evaluation.
- `src/oss_maintainer_kit/scoring.py`: health score calculation.
- `src/oss_maintainer_kit/report.py`: JSON and Markdown report rendering.
- `src/oss_maintainer_kit/templates.py`: safe generation of OSS templates.
- `src/oss_maintainer_kit/cli.py`: CLI commands.
- `tests/`: behavior tests for every module and CLI.
- `.github/workflows/ci.yml`: lint and tests.
- `docs/`: user docs and rule reference.
- `examples/`: sample scanned project.

## Tasks

### Task 1: Scanner and models
- [ ] Write failing tests for repository evidence scanning.
- [ ] Implement dataclasses and scanner until tests pass.
- [ ] Refactor names and deterministic ordering.

### Task 2: Rules and scoring
- [ ] Write failing tests for rule findings and weighted scoring.
- [ ] Implement rule catalog and score calculation until tests pass.
- [ ] Add priority ordering and score grade labels.

### Task 3: Reports
- [ ] Write failing tests for JSON and Markdown rendering.
- [ ] Implement deterministic renderers until tests pass.

### Task 4: Template initialization
- [ ] Write failing tests for safe file creation and force overwrite.
- [ ] Implement template generation until tests pass.

### Task 5: CLI
- [ ] Write failing CLI tests for `scan`, `score`, `report`, and `init-templates`.
- [ ] Implement argparse CLI until tests pass.

### Task 6: Project polish
- [ ] Add README, LICENSE, docs, example project, and CI.
- [ ] Run `python -m pytest`, `python -m ruff check .`, and `python -m build` or equivalent package validation.
- [ ] Fix issues and commit coherent milestones.
