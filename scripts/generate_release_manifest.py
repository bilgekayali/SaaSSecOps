from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path

from saassecops.contracts import validate_document


def _sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def _media_type(path: Path) -> str:
    if path.name.endswith(".whl"):
        return "application/zip"
    if path.name.endswith(".tar.gz"):
        return "application/gzip"
    if path.suffix == ".json":
        return "application/json"
    return "application/octet-stream"


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--version", required=True)
    parser.add_argument("--source-sha", required=True)
    parser.add_argument("--artifact-dir", required=True)
    parser.add_argument("--sbom")
    parser.add_argument("--output", required=True)
    args = parser.parse_args()

    source_sha = args.source_sha.lower()
    if len(source_sha) != 40 or any(ch not in "0123456789abcdef" for ch in source_sha):
        raise SystemExit("--source-sha must be a 40-character hexadecimal commit SHA")

    artifact_dir = Path(args.artifact_dir)
    files = sorted(path for path in artifact_dir.iterdir() if path.is_file())
    if not files:
        raise SystemExit("artifact directory is empty")

    artifacts = [
        {
            "path": str(path.as_posix()),
            "sha256": _sha256(path),
            "size_bytes": path.stat().st_size,
            "media_type": _media_type(path),
        }
        for path in files
    ]

    sbom = None
    if args.sbom:
        sbom_path = Path(args.sbom)
        sbom = {
            "path": str(sbom_path.as_posix()),
            "sha256": _sha256(sbom_path),
            "format": "CycloneDX",
            "spec_version": "1.7",
        }

    manifest = {
        "schema_version": "1.0",
        "version": args.version,
        "source_sha": source_sha,
        "generated_by": "SaaSSecOps",
        "artifacts": artifacts,
        "sbom": sbom,
    }
    validate_document(manifest, "release-manifest")

    output = Path(args.output)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(manifest, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps({"artifacts": len(artifacts), "source_sha": source_sha}, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
