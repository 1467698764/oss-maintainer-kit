from __future__ import annotations

from collections.abc import Callable
from dataclasses import dataclass

from .models import RuleFinding, ScanResult


@dataclass(frozen=True)
class Rule:
    rule_id: str
    title: str
    severity: str
    weight: int
    check: Callable[[ScanResult], bool]
    pass_message: str
    fail_message: str
    recommendation: str


RULES: tuple[Rule, ...] = (
    Rule(
        "readme-depth",
        "README explains the project",
        "high",
        14,
        lambda scan: scan.evidence.has_readme and scan.evidence.readme_words >= 30,
        "README is present and has enough detail for new visitors.",
        "README is missing or too short for new contributors.",
        "Expand README with purpose, installation, usage examples, and contribution notes.",
    ),
    Rule(
        "license",
        "License is declared",
        "high",
        12,
        lambda scan: scan.evidence.has_license,
        "A license file is present.",
        "No license file was found.",
        "Add an OSI-approved license such as MIT, Apache-2.0, or BSD-3-Clause.",
    ),
    Rule(
        "tests",
        "Tests are discoverable",
        "high",
        12,
        lambda scan: scan.evidence.has_tests,
        "Tests or a test directory are present.",
        "No tests or common test directory were found.",
        "Add automated tests that demonstrate core behavior and prevent regressions.",
    ),
    Rule(
        "ci",
        "Continuous integration is configured",
        "high",
        10,
        lambda scan: scan.evidence.has_ci,
        "CI configuration is present.",
        "No CI workflow was found.",
        "Add a GitHub Actions workflow or equivalent CI to run tests on pull requests.",
    ),
    Rule(
        "package-manifest",
        "Package manifest identifies the project",
        "high",
        10,
        lambda scan: bool(scan.evidence.manifests),
        "At least one package manifest was found.",
        "No supported package manifest was found.",
        (
            "Add a language package manifest such as pyproject.toml, package.json, "
            "Cargo.toml, or go.mod."
        ),
    ),
    Rule(
        "contributing-guide",
        "Contribution guide is available",
        "medium",
        9,
        lambda scan: scan.evidence.has_contributing,
        "Contribution guide is present.",
        "No contribution guide was found.",
        "Add CONTRIBUTING.md with setup, test, issue, and pull request guidance.",
    ),
    Rule(
        "issue-template",
        "Issue template guides reports",
        "medium",
        8,
        lambda scan: scan.evidence.has_issue_template,
        "Issue template is present.",
        "No issue template was found.",
        "Add .github/ISSUE_TEMPLATE templates for bug reports and feature requests.",
    ),
    Rule(
        "pr-template",
        "Pull request template guides contributors",
        "medium",
        8,
        lambda scan: scan.evidence.has_pr_template,
        "Pull request template is present.",
        "No pull request template was found.",
        "Add .github/pull_request_template.md with a concise review checklist.",
    ),
    Rule(
        "changelog",
        "Changelog records releases",
        "low",
        8,
        lambda scan: scan.evidence.has_changelog,
        "Changelog is present.",
        "No changelog was found.",
        "Add CHANGELOG.md to record user-visible changes and release notes.",
    ),
    Rule(
        "security-policy",
        "Security policy explains vulnerability reporting",
        "medium",
        9,
        lambda scan: scan.evidence.has_security_policy,
        "Security policy is present.",
        "No security policy was found.",
        "Add SECURITY.md describing supported versions and private vulnerability reporting.",
    ),
)


def evaluate_rules(scan: ScanResult) -> list[RuleFinding]:
    findings = []
    for rule in RULES:
        passed = rule.check(scan)
        findings.append(
            RuleFinding(
                rule_id=rule.rule_id,
                title=rule.title,
                status="pass" if passed else "fail",
                severity=rule.severity,  # type: ignore[arg-type]
                weight=rule.weight,
                message=rule.pass_message if passed else rule.fail_message,
                recommendation=rule.recommendation,
            )
        )
    return sorted(findings, key=lambda item: item.rule_id)
