# Migration to v1

## Summary

v0.8.0 establishes the first checked stable-contract candidate for SaaSSecOps v1. The candidate freezes the documented CLI command shapes, public JSON Schema identities and core evidence semantics under one SHA-256 fingerprint.

No existing v0.7 JSON payload requires a data migration solely because of v0.8.0. The existing public schema identities and their `schema_version` values remain unchanged.

## Consumer guidance

Consumers preparing for v1 should:

1. validate persisted JSON against the schema identified by its contract kind and `schema_version`;
2. treat unknown future schema versions as unsupported rather than silently accepting them;
3. invoke only the documented CLI arguments in `contracts/v1-candidate.json`;
4. use exact-byte SHA-256 verification where a manifest or release evidence contract requires it;
5. pin automation to a released package version rather than internal Python modules;
6. treat Terraform examples, architecture diagrams and internal Python modules as non-API surfaces.

## Candidate fingerprint

The v1 candidate descriptor is checked in at `contracts/v1-candidate.json`. Its canonical JSON SHA-256 is stored in `contracts/v1-candidate.sha256` and verified in CI against the actual argparse surface and packaged schema `$id` values.

Changing the candidate requires an explicit compatibility decision. A change that removes a command, removes or makes an argument mandatory, changes a schema `$id`, narrows an accepted contract incompatibly, or changes a listed semantic invariant must not be merged as an undocumented refactor.

## Additive changes

Before v1.0, an additive change may still be considered when it does not invalidate existing consumers. If it changes the checked candidate descriptor, the pull request must state whether the candidate is intentionally being revised and document any migration impact.

After v1.0, incompatible changes to the stable public boundary require a new major version unless a versioned parallel contract is introduced.

## Non-API surfaces

Reference Terraform, documentation prose, diagrams, scripts used only for repository release engineering and internal Python modules remain implementation/reference surfaces unless explicitly promoted into the stable contract.
