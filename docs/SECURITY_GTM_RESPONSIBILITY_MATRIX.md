# Security GTM Responsibility Matrix

## Operating model

| Function | Primary accountability |
| --- | --- |
| Security Engineering | Technical architecture facts, control implementation and remediation state |
| Product | Product behavior, feature scope and roadmap accuracy |
| Legal | Contractual, privacy and regulatory commitments |
| GRC | Control mappings, approved policy statements, audit evidence and exception governance |
| Security GTM | Customer translation, evidence retrieval and routing of unsupported questions |

## Decision rules

Security GTM may translate approved facts but must not create stronger claims than the evidence supports. Planned features are not current controls. Configuration is not the same as tested operating effectiveness. A repository mapping is not a certification.

Questions that cannot be answered from current evidence remain `needs_review` and are routed to the accountable function. This is intentional fail-closed behavior rather than an incomplete workflow.

## Escalation examples

- Tenant-isolation implementation detail → Security Engineering.
- Product feature availability or roadmap → Product.
- DPA, MSA, BAA or regulatory commitment → Legal.
- SOC 2 / ISO certificate scope or audit evidence → GRC.
- Customer wording and questionnaire coordination → Security GTM.
