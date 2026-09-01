# Compatibility Policy

SaaSSecOps follows Semantic Versioning for the packaged CLI and machine-readable contracts.

## Before v1.0

Minor releases may refine or replace public contracts while the v1 boundary is being established. Breaking changes must be documented in `CHANGELOG.md` and should include a migration note when persisted artifacts are affected.

## v1 stable boundary

At v1.0, the stable boundary will include the documented CLI commands, their required arguments and the versioned public JSON Schemas. Removing a stable command, changing a required field incompatibly, narrowing an accepted enum or changing assessment identity semantics requires a future major release unless a versioned parallel contract is introduced.

Reference Terraform, architecture diagrams, documentation prose and internal Python modules are not stable APIs unless explicitly promoted.

## Evidence compatibility

An artifact is interpreted against its own `schema_version`. Consumers must fail closed on unsupported future schema versions rather than silently accepting fields they do not understand.
