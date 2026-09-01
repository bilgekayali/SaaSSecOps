# Compatibility Policy

SaaSSecOps follows Semantic Versioning for the packaged CLI and machine-readable contracts.

## v0.8 stable-contract candidate

v0.8.0 establishes the first checked candidate for the v1 stable public boundary. The candidate is stored in `contracts/v1-candidate.json`; its canonical JSON SHA-256 is stored in `contracts/v1-candidate.sha256` and verified in CI against the actual CLI parser and public schema `$id` values.

From v0.8 onward, changes to that descriptor require an explicit compatibility decision and migration assessment. Candidate changes must not be hidden inside unrelated refactors.

## v1 stable boundary

At v1.0, the stable boundary includes:

- the `saassecops` executable;
- the documented `assess`, `validate`, `digest` and `contract-snapshot` command shapes;
- the public JSON Schema identities listed in the stable contract;
- deterministic assessment identity semantics;
- exact-byte SHA-256 digest semantics;
- evidence-manifest binding semantics;
- fail-closed handling of unsupported contract kinds and future schema versions.

Removing a stable command, removing an accepted argument, making an optional argument mandatory, changing a public schema `$id`, narrowing accepted data incompatibly or changing a listed semantic invariant requires a future major release unless a versioned parallel contract is introduced.

Reference Terraform, architecture diagrams, documentation prose, repository release scripts and internal Python modules are not stable APIs unless explicitly promoted.

## Evidence compatibility

An artifact is interpreted against its own `schema_version`. Consumers must fail closed on unsupported future schema versions rather than silently accepting fields they do not understand.

Cryptographic validity and evidence freshness are separate decisions. A valid signature does not make expired or revalidation-due evidence current.

## Migration

Migration guidance from the pre-stable releases into the candidate boundary is maintained in [docs/MIGRATION_TO_V1.md](docs/MIGRATION_TO_V1.md).
