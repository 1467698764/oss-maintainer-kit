from __future__ import annotations

import argparse
import sys
from pathlib import Path

from .badge import render_markdown_badge
from .report import render_json_report, render_markdown_report
from .rules import evaluate_rules
from .scanner import scan_repository
from .scoring import calculate_score
from .templates import init_templates


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="omk",
        description="Audit open-source repository maintenance health.",
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    scan = subparsers.add_parser("scan", help="Show repository evidence summary.")
    scan.add_argument("path", nargs="?", default=".")

    score = subparsers.add_parser("score", help="Show repository health score.")
    score.add_argument("path", nargs="?", default=".")

    audit = subparsers.add_parser("audit", help="Enforce a minimum repository health score.")
    audit.add_argument("path", nargs="?", default=".")
    audit.add_argument("--min-score", type=int, default=75)

    badge = subparsers.add_parser("badge", help="Render a Markdown OSS health badge.")
    badge.add_argument("path", nargs="?", default=".")

    report = subparsers.add_parser("report", help="Render a JSON or Markdown report.")
    report.add_argument("path", nargs="?", default=".")
    report.add_argument("--format", choices=("markdown", "json"), default="markdown")
    report.add_argument("--output", type=Path, help="Write report to a file instead of stdout.")

    templates = subparsers.add_parser(
        "init-templates",
        help="Create starter OSS maintenance templates.",
    )
    templates.add_argument("path", nargs="?", default=".")
    templates.add_argument(
        "--force",
        action="store_true",
        help="Overwrite existing generated files.",
    )
    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)

    try:
        if args.command == "scan":
            scan = scan_repository(args.path)
            project_types = ", ".join(scan.profile.project_types) or "unknown"
            manifests = ", ".join(scan.evidence.manifests) or "none"
            print(f"Repository: {scan.root}")
            print(f"Project types: {project_types}")
            print(
                f"README: {'yes' if scan.evidence.has_readme else 'no'} "
                f"({scan.evidence.readme_words} words)"
            )
            print(f"License: {'yes' if scan.evidence.has_license else 'no'}")
            print(f"Tests: {'yes' if scan.evidence.has_tests else 'no'}")
            print(f"CI: {'yes' if scan.evidence.has_ci else 'no'}")
            print(f"Manifests: {manifests}")
            return 0

        if args.command == "score":
            scan = scan_repository(args.path)
            findings = evaluate_rules(scan)
            score = calculate_score(findings)
            print(f"Health score: {score.points}/100 ({score.grade})")
            print(f"Passing checks: {score.passed}/{score.total_rules}")
            if score.top_recommendations:
                print("Top recommendations:")
                for finding in score.top_recommendations:
                    print(f"- {finding.rule_id}: {finding.recommendation}")
            return 0

        if args.command == "audit":
            scan = scan_repository(args.path)
            findings = evaluate_rules(scan)
            score = calculate_score(findings)
            if score.points < args.min_score:
                print(
                    f"Health score {score.points}/100 is below required minimum "
                    f"{args.min_score}/100."
                )
                for finding in score.top_recommendations:
                    print(f"- {finding.rule_id}: {finding.recommendation}")
                return 1
            print(f"Health score {score.points}/100 meets required minimum {args.min_score}/100.")
            return 0

        if args.command == "badge":
            scan = scan_repository(args.path)
            findings = evaluate_rules(scan)
            score = calculate_score(findings)
            print(render_markdown_badge(score.points, score.grade))
            return 0

        if args.command == "report":
            scan = scan_repository(args.path)
            findings = evaluate_rules(scan)
            score = calculate_score(findings)
            output = (
                render_json_report(scan, findings, score)
                if args.format == "json"
                else render_markdown_report(scan, findings, score)
            )
            if args.output:
                args.output.parent.mkdir(parents=True, exist_ok=True)
                args.output.write_text(output, encoding="utf-8")
            else:
                print(output, end="")
            return 0

        if args.command == "init-templates":
            result = init_templates(args.path, force=args.force)
            print(f"Created: {', '.join(result.created) if result.created else 'none'}")
            print(f"Skipped: {', '.join(result.skipped) if result.skipped else 'none'}")
            return 0
    except (FileNotFoundError, NotADirectoryError) as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 2

    parser.error(f"unknown command: {args.command}")
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
