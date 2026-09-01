# Application and API Security

## Summary

v0.5 adds a reference application-security boundary around SaaSSecOps. It maps current OWASP web and API risk catalogs to explicit delivery controls, introduces code/dependency scanning gates, generates a CycloneDX SBOM and defines evidence requirements for vulnerability findings and time-bounded exceptions.

## Reference standards

The repository uses:

- **OWASP Top 10:2025** for web-application security awareness;
- **OWASP API Security Top 10:2023** for API-specific risks;
- **CycloneDX 1.7** for the stable SBOM format used by this milestone.

The mappings in `architecture/appsec-reference.json` are engineering references. They do not represent OWASP certification or a claim that every risk is fully mitigated in a deployed application.

## Secure SDLC gate

The reference delivery path requires:

1. threat modeling before material architecture changes;
2. peer review for source changes;
3. unit, negative and security regression tests;
4. CodeQL static analysis;
5. dependency audit against published vulnerability data;
6. CycloneDX SBOM generation;
7. accountable disposition of critical/high findings before release.

A finding may be remediated, demonstrated false positive or covered by an explicitly approved and time-bounded exception. An exception is not equivalent to remediation.

## API edge controls

A deployable implementation should provide environment-specific evidence for:

- managed ingress and WAF policy;
- TLS 1.2 or stronger according to the actual service/client boundary;
- authentication and tenant/object/function authorization;
- request-body/schema validation;
- rate, concurrency and request-size limits;
- API inventory and ownership;
- outbound API trust and SSRF controls;
- managed secrets and least-privilege secret access;
- security logging that can support detection and investigation.

The repository does not deploy a production WAF or API Gateway policy in v0.5 because such policies depend on the selected application architecture and traffic model.

## Supply-chain evidence

`scripts/generate_sbom.py` produces a deterministic-shape CycloneDX 1.7 SBOM using the package version and the resolved runtime dependency versions in the build environment. `scripts/verify_sbom.py` checks the repository's required SBOM invariants.

The SBOM is inventory evidence only. It does not show that a dependency is secure, supported or correctly configured.

## Vulnerability evidence

`schemas/vulnerability-evidence.schema.json` defines a small reference contract for findings. Each finding has an accountable owner, severity, lifecycle state and evidence references. `risk_accepted` findings additionally require an approver, rationale and expiration timestamp.

The example data is synthetic and must not be presented as a real scan result.

## Deployment evidence checklist

A production assurance review should obtain evidence for at least:

- current architecture and API inventory;
- authentication/authorization tests including cross-tenant and object-level cases;
- WAF/API-edge configuration and exception rules;
- TLS and certificate configuration;
- secret-store configuration and access policy;
- current SAST/dependency scan results;
- generated SBOM bound to the release artifact;
- vulnerability remediation/exception register;
- independent penetration-test results when required by the assurance scope.

## References

- OWASP Top 10:2025: https://owasp.org/Top10/2025/
- OWASP API Security Top 10:2023: https://owasp.org/API-Security/editions/2023/en/0x11-t10/
- CycloneDX specification: https://cyclonedx.org/specification/overview/
