from __future__ import annotations

import argparse
import hashlib
import json
from typing import Any

from .contracts import SCHEMA_FILES, schema_document


SEMANTIC_INVARIANTS: dict[str, Any] = {
    "assessment_exit_codes": {"0": "pass", "2": "gaps_or_error"},
    "assessment_identity": "deterministic_from_canonical_posture_and_policy",
    "digest_algorithm": "SHA-256",
    "digest_scope": "exact_file_bytes",
    "evidence_manifest": "binds_input_policy_and_exact_report_bytes",
    "future_schema_versions": "fail_closed",
    "json_schema_draft": "2020-12",
    "unsupported_contract_kind": "fail_closed",
}


def canonical_json_bytes(document: Any) -> bytes:
    return json.dumps(
        document,
        sort_keys=True,
        separators=(",", ":"),
        ensure_ascii=False,
    ).encode("utf-8")


def contract_fingerprint(document: dict[str, Any]) -> str:
    return hashlib.sha256(canonical_json_bytes(document)).hexdigest()


def _long_option(action: argparse.Action) -> str | None:
    options = sorted(option for option in action.option_strings if option.startswith("--"))
    return options[0] if options else None


def _subparsers_action(parser: argparse.ArgumentParser) -> argparse._SubParsersAction:
    for action in parser._actions:
        if isinstance(action, argparse._SubParsersAction):
            return action
    raise RuntimeError("CLI parser does not expose subcommands")


def _command_descriptor(parser: argparse.ArgumentParser) -> dict[str, Any]:
    positionals: list[str] = []
    required_options: list[str] = []
    optional_options: list[str] = []
    result: dict[str, Any] = {}

    for action in parser._actions:
        if isinstance(action, argparse._HelpAction):
            continue
        if not action.option_strings:
            if action.dest != "help":
                positionals.append(action.dest)
            continue
        option = _long_option(action)
        if not option:
            continue
        if action.required:
            required_options.append(option)
        else:
            optional_options.append(option)
        if action.dest == "kind" and action.choices is not None:
            result["kind_values"] = sorted(str(choice) for choice in action.choices)

    result.update(
        {
            "optional_options": sorted(optional_options),
            "positionals": positionals,
            "required_options": sorted(required_options),
        }
    )
    return result


def stable_contract_descriptor(parser: argparse.ArgumentParser) -> dict[str, Any]:
    subparsers = _subparsers_action(parser)
    commands = {
        name: _command_descriptor(command_parser)
        for name, command_parser in sorted(subparsers.choices.items())
    }

    global_options = []
    for action in parser._actions:
        if isinstance(action, (argparse._HelpAction, argparse._SubParsersAction)):
            continue
        option = _long_option(action)
        if option:
            global_options.append(option)

    return {
        "contract_candidate": "1.0",
        "executable": parser.prog,
        "global_options": sorted(global_options),
        "cli": commands,
        "schemas": {
            kind: schema_document(kind)["$id"]
            for kind in sorted(SCHEMA_FILES)
        },
        "semantic_invariants": SEMANTIC_INVARIANTS,
    }
