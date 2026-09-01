from __future__ import annotations

import argparse
import json
from pathlib import Path

from .evaluator import AssessmentError, assess, load_json


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog="saassecops")
    sub = parser.add_subparsers(dest="command", required=True)
    cmd = sub.add_parser("assess", help="Assess a declared AWS SaaS security posture.")
    cmd.add_argument("posture")
    cmd.add_argument("--policy", required=True)
    cmd.add_argument("--output")
    args = parser.parse_args(argv)

    try:
        report = assess(load_json(args.posture), load_json(args.policy))
    except (AssessmentError, OSError, json.JSONDecodeError) as exc:
        parser.error(str(exc))

    rendered = json.dumps(report, indent=2, sort_keys=True) + "\n"
    if args.output:
        output = Path(args.output)
        output.parent.mkdir(parents=True, exist_ok=True)
        output.write_text(rendered, encoding="utf-8")
    else:
        print(rendered, end="")

    return 0 if report["overall"] == "pass" else 2
