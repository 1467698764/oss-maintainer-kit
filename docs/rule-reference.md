# Rule Reference

OSS Maintainer Kit uses a weighted checklist. Passing all rules yields a 100/100 score.

| Rule ID | Weight | Severity | Passing evidence |
| --- | ---: | --- | --- |
| `readme-depth` | 14 | high | README exists and has at least 30 words. |
| `license` | 12 | high | License or copying file exists. |
| `tests` | 12 | high | Common test directory or test file exists. |
| `ci` | 10 | high | GitHub Actions, GitLab CI, or CircleCI config exists. |
| `package-manifest` | 10 | high | Supported manifest such as `pyproject.toml`, `package.json`, `Cargo.toml`, or `go.mod` exists. |
| `contributing-guide` | 9 | medium | `CONTRIBUTING.md` exists in root or `.github/`. |
| `issue-template` | 8 | medium | GitHub issue template exists. |
| `pr-template` | 8 | medium | Pull request template exists. |
| `changelog` | 8 | low | Changelog/history/release notes file exists. |
| `security-policy` | 9 | medium | `SECURITY.md` exists in root or `.github/`. |

The rule set is intentionally practical rather than exhaustive. A high score means the project communicates the basics well; it does not guarantee code quality or security.
