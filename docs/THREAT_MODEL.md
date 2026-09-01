# Threat Model

## Scope

This review covers the SaaSSecOps reference boundaries that are candidates for v1: AWS account and logging architecture, tenant isolation, application/API security, software supply-chain evidence, customer trust, evidence integrity and incident-response ownership. It is a repository threat model, not a penetration test or production security assessment.

## Reviewed threats

| Domain | Threat | Example failure | Reference controls / evidence | Residual boundary |
| --- | --- | --- | --- | --- |
| Cloud and organization | Management-plane overreach | Production workload is placed in the AWS Organizations management account | Separate management, Security Tooling, Log Archive and workload account roles; SCP reference | Requires real organization/deployment evidence |
| Cloud and organization | Privilege escalation | Workload assumes a role broader than intended | Federation, short-lived credentials, least privilege, IAM Access Analyzer | Reference policies do not prove effective deployed IAM |
| Cloud and organization | Public data exposure | Data store or audit archive becomes public | Private data tier, S3 public-access blocking, encrypted/versioned log archive | Requires deployed configuration evidence |
| Cloud and organization | Audit blind spot | Organization activity is not centrally recorded | Multi-Region CloudTrail, log validation, Log Archive account | Requires real trail delivery/retention evidence |
| Tenant isolation | Cross-tenant data access | Tenant A reads Tenant B data | Authoritative tenant context, scoped authorization, data-layer enforcement, negative vectors | Local vectors are not an AWS IAM proof |
| Tenant isolation | Tenant-context injection | Caller overrides tenant identity in request data | Trusted tenant context and fail-closed context validation | Depends on real identity/application integration |
| Tenant isolation | Confused-deputy authorization | Shared service acts with another tenant's scope | Tenant-scoped session/tag reference and explicit resource scoping | Requires service-specific authorization design |
| Application and API security | Broken object authorization | API returns another tenant's object by identifier | Tenant guard plus object authorization requirement | No live endpoint penetration test |
| Application and API security | Broken function authorization | Low-privilege caller reaches administrative operation | Function authorization, RBAC and negative authorization expectations | No production identity-provider evidence |
| Application and API security | Injection / malformed input | Untrusted request reaches unsafe interpreter or data path | Request validation, OWASP mappings, CodeQL reference gate | Static/reference checks do not prove absence of runtime flaws |
| Application and API security | Secret exposure | Static credential is committed or embedded | Managed-secret requirement and short-lived credentials | No production secret-store custody claim |
| Software supply chain | Vulnerable dependency | Known vulnerable package enters release candidate | `pip-audit` strict gate and explicit dependency set | Audit coverage depends on advisory data available at run time |
| Software supply chain | Build artifact substitution | Distributed wheel differs from reviewed source | Exact-source release manifest, SHA-256 checksums, SBOM, provenance workflow | Tag/release process must run on exact source |
| Software supply chain | CI action drift | Mutable action tag changes underlying code unexpectedly | v0.9 pins critical GitHub Actions to reviewed commit SHAs | Pins require deliberate maintenance |
| Customer trust | Unsupported affirmative answer | Questionnaire states a control is deployed without evidence | Evidence-bound answer contract and `needs_review` fail-closed state | Repository evidence cannot prove customer-specific deployment |
| Customer trust | Certification overstatement | Reference design is described as certified | External-assurance requirement for certification/independent-assessment claims | External assurance remains outside repository scope |
| Evidence integrity | Evidence tampering | Signed envelope or payload is modified after review | Ed25519 envelope, payload SHA-256 binding and signature verification | Signature proves integrity, not truth of claim |
| Evidence integrity | Revoked signing key accepted | Historical or compromised key remains trusted | Active/retired/revoked registry and fail-closed revocation check | Production key custody remains external |
| Evidence integrity | Stale evidence treated as current | Old evidence is reused after architecture/control changes | `current`, `revalidation_due`, `expired` freshness states | Revalidation quality depends on real evidence owner |
| Incident response and operations | Unowned finding | Security issue has no accountable response path | Owned finding route, IR roles and exception ownership | No claim of operational response performance |
| Incident response and operations | Unbounded risk acceptance | Exception remains open indefinitely | Approver, rationale and expiry requirements | Business acceptance still requires authorized human decision |

## Release-candidate review outcome

The v0.9 candidate requires every reviewed domain above to have a documented control/evidence path and at least one fail-closed or validation mechanism where the repository can test the invariant locally. Repository-owned critical/high release defects are tracked in `release/defect-register.json`; the v0.9 gate fails if an entry is open at either severity.

An empty blocker register is a review record only. It does not establish vulnerability absence, deployed AWS effectiveness, penetration-test success, compliance or independent assurance.
