# OSS Maintainer Kit Report

Repository: examples/minimal-python-project
Project types: python

## Health score

**36/100** - `starter` (3/10 checks passing)

## Findings

| Rule | Status | Severity | Message |
| --- | --- | --- | --- |
| `changelog` | FAIL fail | low | No changelog was found. |
| `ci` | FAIL fail | high | No CI workflow was found. |
| `contributing-guide` | FAIL fail | medium | No contribution guide was found. |
| `issue-template` | FAIL fail | medium | No issue template was found. |
| `license` | FAIL fail | high | No license file was found. |
| `package-manifest` | PASS pass | high | At least one package manifest was found. |
| `pr-template` | FAIL fail | medium | No pull request template was found. |
| `readme-depth` | PASS pass | high | README is present and has enough detail for new visitors. |
| `security-policy` | FAIL fail | medium | No security policy was found. |
| `tests` | PASS pass | high | Tests or a test directory are present. |

## Top recommendations

1. **License is declared** - Add an OSI-approved license such as MIT, Apache-2.0, or BSD-3-Clause.
2. **Continuous integration is configured** - Add a GitHub Actions workflow or equivalent CI to run tests on pull requests.
3. **Contribution guide is available** - Add CONTRIBUTING.md with setup, test, issue, and pull request guidance.
4. **Security policy explains vulnerability reporting** - Add SECURITY.md describing supported versions and private vulnerability reporting.
5. **Issue template guides reports** - Add .github/ISSUE_TEMPLATE templates for bug reports and feature requests.
