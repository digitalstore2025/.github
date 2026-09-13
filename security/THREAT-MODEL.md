# Threat model

## Assets

- Source code and Git history
- Cloud and third-party credentials
- Build/deploy identities
- User and tenant data
- Dependency graph and build artifacts
- Infrastructure definitions
- AI-agent tools, memory and external connectors

## Primary threats

| Threat | Control |
|---|---|
| Secret committed by developer/agent | Gitleaks pre-commit + CI |
| Vulnerable dependency | OSV-Scanner + Trivy + Renovate |
| Insecure code pattern | Semgrep + CodeQL + human review |
| Cloud/IaC misconfiguration | Checkov + Trivy misconfig |
| Runtime web weakness | ZAP on authorized staging |
| Compromised action tag | Full commit-SHA pinning + Renovate |
| Missing software inventory | CycloneDX SBOM |
| Prompt injection leads to privileged tool action | Independent server authorization + schema validation + least privilege |
| AI-generated authorization bug | Mandatory human review + authorization tests |

## Residual risks

This baseline does not prove business-logic correctness, tenant isolation, cryptographic design, production configuration, incident readiness or regulatory compliance. Add product-specific tests and threat modeling for high-impact systems.
