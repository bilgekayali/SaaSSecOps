# Customer Trust Playbook

## Objective

Translate verified security facts into concise customer-facing answers without overstating architecture, implementation, testing, independent assurance or certification.

## Evidence hierarchy

1. documented design;
2. deployed/configured evidence;
3. tested operating evidence;
4. independent assessment;
5. certification.

A stronger answer requires stronger evidence. The existence of an AWS service, control mapping, SBOM or local test does not automatically justify a stronger customer claim.

## Questionnaire workflow

1. Parse the exact question, scope and implied claim strength.
2. Assign the accountable owner.
3. Retrieve current evidence.
4. Set the answer to `needs_review` when evidence is missing, stale or ambiguous.
5. Draft customer-safe wording only to the strength of the evidence.
6. Link material exceptions and known limitations.
7. Obtain review from the appropriate function.
8. Revalidate after architecture, evidence or contractual scope changes.

## Tenant isolation

A customer answer should identify the tenancy pattern, source of tenant context, enforcement points, scoped authorization and relevant test evidence. “We use AWS IAM” or “data is encrypted” does not establish tenant isolation.

## Vulnerabilities and penetration testing

Distinguish repository scanning from production vulnerability management and independent penetration testing. Findings and exceptions require accountable owners and explicit status. A penetration-test statement requires current environment-specific evidence.

## Certification and compliance

Do not convert a control mapping into a compliance or certification statement. `certified` and `independently_assessed` claims require current external assurance evidence.

## Boundary

This playbook is a reference operating model. It is not an approved communications policy for a real company and does not authorize customer, contractual or regulatory commitments.
