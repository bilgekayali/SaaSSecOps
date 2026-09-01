# Security Assurance Pack

## Scope

This pack is a reference structure for customer security reviews. It translates repository evidence into bounded, reviewable statements. It is not an attestation for a deployed SaaS service.

## Assurance sections

| Section | Reference evidence | Customer-safe boundary |
| --- | --- | --- |
| Architecture | multi-account and workload architecture | Describes the reference design only |
| Tenant isolation | tenant context, STS/ABAC and negative vectors | Does not prove deployed isolation |
| Application/API security | OWASP mappings, CodeQL, dependency audit and SBOM | Does not prove vulnerability absence |
| Logging/detection | CloudTrail, GuardDuty, Security Hub reference controls | Does not prove production monitoring effectiveness |
| Vulnerability lifecycle | finding ownership and exception evidence | Does not prove all findings are current or complete |

## Answer-strength model

- `documented` — the repository describes the control or design;
- `configured` — environment-specific configuration evidence exists;
- `tested` — dated test evidence supports the statement;
- `independently_assessed` — external assurance supports the statement;
- `certified` — current certification evidence supports the statement.

The repository itself can demonstrate `documented` reference behavior. Stronger claims require environment-specific or external evidence.

## Release gate

A response set is not customer-ready when an affirmative answer lacks available evidence, customer-safe wording is missing, a question is still `needs_review`, an approved answer lacks a reviewer, or an independent-assessment/certification claim lacks external assurance.

`python scripts/build_customer_trust_summary.py` demonstrates this fail-closed behavior.
