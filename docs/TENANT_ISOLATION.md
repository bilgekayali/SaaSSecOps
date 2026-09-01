# Tenant Isolation

## Summary

Tenant isolation is treated as a first-class authorization boundary. Authentication identifies the caller; isolation determines which tenant resources that caller may access. A valid login must never be treated as sufficient proof of tenant authorization.

AWS documents pool, silo and bridge models as distinct SaaS isolation strategies. SaaSSecOps represents all three because real products frequently mix them by service, data domain, risk tier or customer requirement.

## Reference models

| Model | Shared footprint | Dedicated footprint | Primary trade-off |
| --- | --- | --- | --- |
| Pool | Compute and/or storage can be shared | None required | Highest operational efficiency; strongest need for logical tenant enforcement |
| Silo | Identity, onboarding and operations remain unified | Some or all tenant workload resources | Strong resource separation with higher cost and operational footprint |
| Bridge | Selected services remain shared | Selected services/data are dedicated | Isolation can follow risk and service characteristics |

Dedicated resources do not remove the need for a unified SaaS operating model. Shared resources do not reduce the tenant-isolation requirement.

## Tenant context

The v0.4 reference uses `tenant-id` as the canonical synthetic tenant attribute.

Reference rules:

1. Tenant identity originates from an authenticated identity or trusted authorization service.
2. A request body, query parameter or arbitrary client header cannot override the authoritative tenant.
3. Tenant context is propagated across service boundaries that access protected tenant resources.
4. When AWS STS session tags are used, the role trust boundary must deliberately permit and constrain `sts:TagSession`.
5. If role chaining is part of the design, the tenant tag must be handled deliberately as a transitive session tag where required.
6. The data layer enforces the tenant boundary independently; application routing alone is insufficient.

AWS STS exposes session tags through `aws:PrincipalTag/<key>` in request context. The included pooled S3 policy demonstrates how `aws:PrincipalTag/tenant-id` can bind a temporary principal to one tenant prefix. The bucket name is intentionally a placeholder.

## Fail-closed decision model

`saassecops.isolation.evaluate_tenant_access` models only the repository's tenant-boundary invariants:

```text
missing principal tenant -> deny
missing resource tenant  -> deny
action outside allowlist -> deny
principal != resource    -> deny
otherwise                -> allow
```

This is not an IAM simulator. It exists so that the control contract, examples and negative tests share one deterministic reference rule.

Run the synthetic vectors:

```bash
python scripts/run_isolation_vectors.py
```

The vector set includes same-tenant allow cases plus cross-tenant, missing-context and unauthorized-action denial cases.

## Pooled data example

`policies/iam/pool-s3-tenant-prefix-policy.json` uses the policy variable:

```text
${aws:PrincipalTag/tenant-id}
```

to scope S3 listing and object access to one tenant prefix.

A production design still needs, at minimum:

- authoritative generation of the tenant session tag;
- trust-policy constraints on who may call `sts:TagSession`;
- least-privilege role permissions;
- protection against confused-deputy paths;
- tenant-aware application authorization;
- storage-specific enforcement;
- logging and alerting;
- independent negative testing.

## Threats and controls

| Threat | Example | Reference control |
| --- | --- | --- |
| Caller-selected tenant | Client changes `tenant-id` in a request | Tenant comes from authenticated identity, caller override denied |
| Cross-tenant resource access | Tenant A requests Tenant B object | Principal/resource tenant mismatch fails closed |
| Context loss | Internal service drops tenant context | Propagation contract and negative tests |
| Over-broad workload credentials | Shared role can access all tenant data | Temporary tenant-scoped session/ABAC pattern |
| Application-only enforcement | Data store accepts unscoped queries | Independent data-layer tenant enforcement |
| Role-chain context loss | Tenant tag disappears on second role | Explicit transitive-session-tag design where needed |
| Unsupported assurance claim | Synthetic test is presented as deployed proof | Explicit evidence requirements and non-claims |

## Evidence checklist

A production claim of effective isolation should be supported by environment-specific evidence such as:

- identity-provider or authorization-service configuration for the tenant claim;
- STS/role trust and permission policies;
- application authorization tests;
- storage/database tenant-enforcement tests;
- negative cross-tenant integration tests;
- CloudTrail/application telemetry showing scoped identities and denied attempts;
- change/review evidence for isolation policies;
- independent security testing appropriate to the risk profile.

Repository examples are design evidence only until bound to a deployed environment.

## References

- AWS SaaS Lens — Tenant Isolation: https://docs.aws.amazon.com/wellarchitected/latest/saas-lens/tenant-isolation.html
- AWS SaaS Lens — Silo, Pool, and Bridge Models: https://docs.aws.amazon.com/wellarchitected/latest/saas-lens/silo-pool-and-bridge-models.html
- AWS IAM — Pass session tags in AWS STS: https://docs.aws.amazon.com/IAM/latest/UserGuide/id_session-tags.html
- AWS IAM — Attribute-based access control: https://docs.aws.amazon.com/IAM/latest/UserGuide/introduction_attribute-based-access-control.html
