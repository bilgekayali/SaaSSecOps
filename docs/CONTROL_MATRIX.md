# Control Matrix

| Control | Family | Reference evidence |
| --- | --- | --- |
| `TENANT-01` Tenant context is propagated | TENANT | tenant model, authorization design, isolation-test evidence |
| `TENANT-02` Cross-tenant access is denied | TENANT | tenant model, authorization design, isolation-test evidence |
| `TENANT-03` Workload credentials are tenant scoped | TENANT | tenant model, authorization design, isolation-test evidence |
| `TENANT-04` Data access enforces tenant identity | TENANT | tenant model, authorization design, isolation-test evidence |
| `IAM-01` Human access uses federation | IAM | role/policy review, federation configuration, Access Analyzer findings |
| `IAM-02` Workloads use short-lived credentials | IAM | role/policy review, federation configuration, Access Analyzer findings |
| `IAM-03` Least-privilege review is performed | IAM | role/policy review, federation configuration, Access Analyzer findings |
| `IAM-04` IAM Access Analyzer is enabled | IAM | role/policy review, federation configuration, Access Analyzer findings |
| `NET-01` Application workloads are private | NET | VPC/subnet/security-group design, Flow Logs |
| `NET-02` Datastores are private | NET | VPC/subnet/security-group design, Flow Logs |
| `NET-03` VPC Flow Logs are enabled | NET | VPC/subnet/security-group design, Flow Logs |
| `DATA-01` TLS is enforced | DATA | TLS policy, KMS/key design, secret-management configuration |
| `DATA-02` Encryption at rest is enabled | DATA | storage-encryption configuration and evidence |
| `DATA-03` Audit evidence uses customer-managed KMS | DATA | KMS key policy, rotation and audit-archive binding |
| `DATA-04` Secrets are managed outside source | DATA | Secrets Manager or equivalent secret-store evidence |
| `LOG-01` CloudTrail is multi-Region | LOG | CloudTrail configuration |
| `LOG-02` CloudTrail validation is enabled | LOG | CloudTrail log-file validation configuration |
| `LOG-03` Audit archive is private and versioned | LOG | S3 public-access block, versioning and encryption evidence |
| `DET-01` GuardDuty is enabled | DET | GuardDuty detector configuration |
| `DET-02` Security Hub is enabled | DET | Security Hub configuration and standards posture |
| `DET-03` Findings have an owned response route | DET | Event routing, ownership and escalation evidence |
| `IR-01` Incident-response roles are defined | IR | response roles and escalation matrix |
| `IR-02` Response playbooks are exercised | IR | tabletop or simulation evidence |
| `TRUST-01` Architecture evidence is maintained | TRUST | architecture pack and review history |
| `TRUST-02` Questionnaire answers require evidence | TRUST | questionnaire workflow and source evidence |
| `TRUST-03` Security exceptions have accountable owners | TRUST | exception register, owner and review date |

A control being represented in this matrix does not establish effective production implementation or compliance.
