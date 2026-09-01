# Architecture

SaaSSecOps treats tenant isolation as an explicit authorization boundary, not as a side effect of authentication or shared infrastructure. Tenant context should be established from a trusted identity path, propagated across service calls and enforced where protected resources are accessed.

## Logical layers

1. **Identity plane** — workforce/customer federation and tenant-aware identity claims.
2. **Edge plane** — intentionally managed ingress.
3. **Application plane** — private workloads receiving validated tenant context.
4. **Isolation plane** — policy or scoped AWS credentials constraining resource access.
5. **Data plane** — tenant-aware partitioning and authorization.
6. **Security telemetry plane** — CloudTrail, network telemetry, GuardDuty and Security Hub.
7. **Trust plane** — evidence for security reviews, questionnaires and architecture conversations.

The repository does not prescribe pooled, siloed or hybrid tenancy. The security objective remains the same: one tenant must not gain access to another tenant's protected resources.

## Production direction

The included Terraform is deliberately account scoped. A production design would normally consider separate workload and security/logging accounts, AWS Organizations controls, delegated security administration, environment separation, tested response workflows and workload-specific tenant-isolation controls.
