# Compatibility Policy

SaaSSecOps follows Semantic Versioning for the packaged CLI and machine-readable contracts.

## v1.0 stable boundary

v1.0.0 promotes the checked v1 candidate established in v0.8.0 and release-hardened in v0.9.0 without changing its public fingerprint.

Stable-contract fingerprint:

`sha256:d12b26f57701507934e88ed561546255694d72485b6c30dc29bab2944847cf94`

The checked descriptor remains in `contracts/v1-candidate.json` and its canonical SHA-256 remains in `contracts/v1-candidate.sha256`. The filename is intentionally retained so the exact bytes/fingerprint verified during RC promotion do not change merely for naming purposes.

The stable boundary includes:

- the `saassecops` executable;
- the documented `assess`, `validate`, `digest` and `contract-snapshot` command shapes;
- the public JSON Schema identities listed in the checked contract;
- deterministic assessment identity semantics;
- exact-byte SHA-256 digest semantics;
- evidence-manifest binding semantics;
- fail-closed handling of unsupported contract kinds and future schema versions.

Removing a stable command, removing an accepted argument, making an optional argument mandatory, changing a public schema `$id`, narrowing accepted data incompatibly or changing a listed semantic invariant requires a future major release unless a versioned parallel contract is introduced.

Backward-compatible commands, fields, schemas and controls may be added in a v1.x release when they do not invalidate existing stable consumers.

Reference Terraform, architecture diagrams, documentation prose, repository release scripts and internal Python modules are not stable APIs unless explicitly promoted.

## Security-sensitive compatibility

A security fix may tighten validation when continued acceptance would be unsafe. Such a change must be documented with the security rationale and migration impact rather than being hidden as an unrelated refactor.

## Evidence compatibility

An artifact is interpreted against its own `schema_version`. Consumers must fail closed on unsupported future schema versions rather than silently accepting fields they do not understand.

Cryptographic validity and evidence freshness are separate decisions. A valid signature does not make expired or revalidation-due evidence current.

## Release continuity

The v1 stable release verifier requires the v0.9 release-candidate fingerprint, checked fingerprint and live parser/schema projection to remain identical. This prevents the stable promotion itself from silently changing the public boundary.

Migration guidance from pre-stable releases is maintained in [docs/MIGRATION_TO_V1.md](docs/MIGRATION_TO_V1.md). Stable-release rules are documented in [docs/STABLE_RELEASE.md](docs/STABLE_RELEASE.md).
