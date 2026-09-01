from __future__ import annotations

import argparse
import json
from pathlib import Path

from . import __version__
from .contracts import ContractError, SCHEMA_FILES, contract_snapshot, validate_document
from .evaluator import AssessmentError, assess, build_evidence_manifest, digest_file, load_json


def _json_bytes(document: dict[str, object]) -> bytes:
    return (json.dumps(document, indent=2, sort_keys=True) + "\n").encode("utf-8")


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog="saassecops")
    parser.add_argument("--version", action="version", version=f"%(prog)s {__version__}")
    sub = parser.add_subparsers(dest="command", required=True)

    assess_cmd = sub.add_parser("assess", help="Assess a declared AWS SaaS security posture.")
    assess_cmd.add_argument("posture")
    assess_cmd.add_argument("--policy", required=True)
    assess_cmd.add_argument("--output")
    assess_cmd.add_argument("--manifest-output")

    validate_cmd = sub.add_parser("validate", help="Validate a JSON document against a public contract.")
    validate_cmd.add_argument("document")
    validate_cmd.add_argument("--kind", required=True, choices=sorted(SCHEMA_FILES))

    digest_cmd = sub.add_parser("digest", help="Print the SHA-256 digest of exact file bytes.")
    digest_cmd.add_argument("document")

    sub.add_parser("contract-snapshot", help="Print the current CLI/schema contract snapshot.")

    args = parser.parse_args(argv)

    try:
        if args.command == "validate":
            validate_document(load_json(args.document), args.kind)
            print(f"valid {args.kind}: {args.document}")
            return 0

        if args.command == "digest":
            print(digest_file(args.document))
            return 0

        if args.command == "contract-snapshot":
            print(json.dumps(contract_snapshot(__version__), indent=2, sort_keys=True))
            return 0

        posture_path = Path(args.posture)
        policy_path = Path(args.policy)
        report = assess(load_json(posture_path), load_json(policy_path))
        report_bytes = _json_bytes(report)

        if args.output:
            output = Path(args.output)
            output.parent.mkdir(parents=True, exist_ok=True)
            output.write_bytes(report_bytes)
        else:
            print(report_bytes.decode("utf-8"), end="")

        if args.manifest_output:
            if not args.output:
                raise AssessmentError("--manifest-output requires --output so exact report bytes can be bound")
            manifest = build_evidence_manifest(
                report,
                posture_name=str(posture_path),
                policy_name=str(policy_path),
                report_name=str(Path(args.output)),
                report_bytes=report_bytes,
            )
            manifest_path = Path(args.manifest_output)
            manifest_path.parent.mkdir(parents=True, exist_ok=True)
            manifest_path.write_bytes(_json_bytes(manifest))

        return 0 if report["overall"] == "pass" else 2
    except (AssessmentError, ContractError, OSError, json.JSONDecodeError) as exc:
        parser.error(str(exc))

    return 2
