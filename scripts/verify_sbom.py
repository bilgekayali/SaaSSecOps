from __future__ import annotations

import argparse
import json
from pathlib import Path


def verify(document: dict[str, object]) -> None:
    if document.get("bomFormat") != "CycloneDX":
        raise ValueError("SBOM must use CycloneDX")
    if document.get("specVersion") != "1.7":
        raise ValueError("SBOM must use CycloneDX 1.7")
    if not str(document.get("serialNumber", "")).startswith("urn:uuid:"):
        raise ValueError("SBOM must have a UUID serialNumber")
    metadata = document.get("metadata")
    if not isinstance(metadata, dict) or not isinstance(metadata.get("component"), dict):
        raise ValueError("SBOM metadata.component is required")
    components = document.get("components")
    if not isinstance(components, list) or not components:
        raise ValueError("SBOM must contain resolved runtime components")
    refs = []
    for component in components:
        if not isinstance(component, dict):
            raise ValueError("SBOM component must be an object")
        for field in ("name", "version", "purl", "bom-ref"):
            if not component.get(field):
                raise ValueError(f"SBOM component missing {field}")
        refs.append(component["bom-ref"])
    if len(refs) != len(set(refs)):
        raise ValueError("SBOM bom-ref values must be unique")


def main() -> int:
    parser = argparse.ArgumentParser(description="Verify SaaSSecOps CycloneDX SBOM invariants.")
    parser.add_argument("document")
    args = parser.parse_args()
    document = json.loads(Path(args.document).read_text(encoding="utf-8"))
    verify(document)
    print(f"valid CycloneDX 1.7 SBOM: {args.document}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
