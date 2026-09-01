from __future__ import annotations

import argparse
import importlib.metadata
import json
import re
import tomllib
import uuid
from pathlib import Path
from urllib.parse import quote

ROOT = Path(__file__).resolve().parents[1]


def dependency_name(requirement: str) -> string:
    match = re.match(r"^([A-Za-z0-9_.-]+)", requirement.strip())
    if not match:
        raise ValueError(f"unsupported dependency requirement: {requirement}")
    return match.group(1)


def build_sbom() -> dict[str, object]:
    project = tomllib.loads((ROOT / "pyproject.toml").read_text(encoding="utf-8"))["project"]
    components = []
    for requirement in sorted(project.get("dependencies", [])):
        name = dependency_name(requirement)
        version = importlib.metadata.version(name)
        normalized = name.lower().replace("_", "-")
        components.append(
            {
                "type": "library",
                "bom-ref": f"pkg:pypi/{quote(normalized)}@{quote(version)}",
                "name": name,
                "version": version,
                "purl": f"pkg:pypi/{quote(normalized)}@{quote(version)}",
                "properties": [
                    {"name": "saassecops:declared-requirement", "value": requirement}
                ],
            }
        )

    project_name = project["name"]
    project_version = project["version"]
    fingerprint = "|".join([project_name, project_version] + [c["purl"] for c in components])
    serial = uuid.uuid5(uuid.NAMESPACE_URL, f"https://github.com/bilgekayali/SaaSSecOps/{fingerprint}")

    return {
        "bomFormat": "CycloneDX",
        "specVersion": "1.7",
        "serialNumber": f"urn:uuid:{serial}",
        "version": 1,
        "metadata": {
            "component": {
                "type": "application",
                "bom-ref": f"pkg:pypi/{project_name}@{project_version}",
                "name": project_name,
                "version": project_version,
                "purl": f"pkg:pypi/{project_name}@{project_version}"
            }
        },
        "components": components,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Generate a deterministic CycloneDX 1.7 SBOM for SaaSSecOps.")
    parser.add_argument("--output", required=True)
    args = parser.parse_args()
    output = Path(args.output)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(build_sbom(), indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
