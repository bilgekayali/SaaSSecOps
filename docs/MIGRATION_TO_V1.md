# Migration to v1

## Summary

SaaSSecOps v1.0.0 promotes the checked contract established in v0.8.0 and release-hardened in v0.9.0 to the stable public boundary. The CLI command shapes, public JSON Schema identities and core evidence semantics are unchanged during the RC-to-v1 promotion.

No existing v0.7+ JSON payload requires a data migration solely because of the v1.0.0 promotion. Existing public schema identities and their `schema_version` values remain unchanged.

## Consumer guidance

Consumers moving to v1 should:

1. validate persisted JSON against the schema identified by its contract kind and `schema_version`;
2. treat unknown future schema versions as unsupported rather than silently accepting them;
3. invoke only the documented CLI arguments in `contracts/v1-candidate.json`;
4. use exact-byte SHA-256 verification where a manifest or release evidence contract requires it;
5. pin automation to a released package version rather than internal Python modules;
6. treat Terraform examples, architecture diagrams, release scripts and internal Python modules as non-API surfaces.

## Stable fingerprint

The v1 descriptor remains checked in at `contracts/v1-candidate.json`. Its canonical JSON SHA-256 remains in `contracts/v1-candidate.sha256`:

`d12b26f57701507934e88ed561546255694d72485b6c30dc29bab2944847cf94`

The filename is intentionally preserved so the exact descriptor bytes verified during the release-candidate phase are not changed merely for naming purposes.

## Compatibility after v1.0

Backward-compatible additions may be introduced in v1.x when they do not invalidate existing stable consumers. Removing a stable command, removing an accepted argument, making an optional argument mandatory, changing a public schema `$id`, narrowing accepted data incompatibly or changing a listed semantic invariant requires a future major version unless a versioned parallel contract is introduced.

Security fixes may tighten validation when continued acceptance would be unsafe. Those changes must document the security rationale and migration impact.

## Non-API surfaces

Reference Terraform, documentation prose, diagrams, repository release engineering scripts and internal Python modules remain implementation/reference surfaces unless explicitly promoted into the stable contract.
