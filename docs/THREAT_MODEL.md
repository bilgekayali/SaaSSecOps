# Threat Model

| Threat | Example failure | Reference mitigation |
| --- | --- | --- |
| Cross-tenant access | Tenant A reads Tenant B data | Tenant context + scoped authorization + data-layer enforcement |
| Privilege escalation | Workload assumes broad role | Least privilege + STS + Access Analyzer |
| Credential leakage | Static secret is committed | Federation/short-lived credentials + managed secrets |
| Public data exposure | Data store or log bucket is public | Private data tier + public-access blocking |
| Audit tampering | Security evidence is overwritten | Versioned archive + CloudTrail validation + KMS |
| Detection gap | Suspicious activity is not surfaced | GuardDuty + Security Hub + owned response route |
| Trust overstatement | Questionnaire says yes without evidence | Evidence-bound answers + explicit exceptions |
| Response ambiguity | Finding has no owner | Defined IR roles and exercised playbooks |

This is a reference threat model, not a penetration test or production security assessment.
