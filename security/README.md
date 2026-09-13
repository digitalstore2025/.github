# DevSecOps Vibe Coding Kit

A reusable security baseline for repositories where developers and AI coding agents both contribute code. It turns security from an end-of-project audit into deterministic gates from pre-commit through staging.

## Coverage

| Layer | Primary control | Purpose |
|---|---|---|
| Pre-commit | Gitleaks | Stop secrets before they enter Git history |
| Pull request | Semgrep | SAST and insecure-code patterns |
| Pull request | Trivy | Vulnerabilities, secrets, misconfiguration and SBOM |
| Pull request | Checkov | IaC and cloud configuration policy |
| Pull request | OSV-Scanner | Dependency vulnerability matching |
| Pull request / schedule | CodeQL | Deeper semantic and data-flow analysis |
| Staging only | OWASP ZAP | Passive runtime baseline DAST |
| Continuous | Renovate | Controlled dependency and GitHub Action updates |

## Architecture

```text
Developer / AI Agent
        |
        v
Pre-commit -------- Gitleaks
        |
        v
Pull Request ------- Semgrep
        |----------- Trivy + SBOM
        |----------- Checkov
        |----------- OSV-Scanner
        |----------- CodeQL
        |----------- Unit / Integration / E2E tests
        |
        v
Build / Preview
        |
        v
Authorized Staging - OWASP ZAP baseline
        |
        v
Production

Renovate ----------> continuously proposes reviewed dependency/action updates
```

## Reusable workflows

- `.github/workflows/security-gate.yml`
- `.github/workflows/codeql-reusable.yml`
- `.github/workflows/zap-baseline-reusable.yml`

Use the caller templates under `security/templates/` in each application repository. Read `ADOPTION.md` before enabling required checks.

## Security design choices

- Third-party GitHub Actions are pinned to exact commit SHAs.
- Consumer templates pin the central reusable workflow to an audited commit SHA instead of mutable `main`.
- Semgrep, Checkov, Trivy, OSV-Scanner, and Gitleaks are pinned to explicit versions/digests.
- Gitleaks scans the full Git history intentionally, even when the other scanners are scoped to a subdirectory.
- Gitleaks runs as the open-source CLI container, avoiding the organization-license requirement of `gitleaks-action`.
- CodeQL accepts a per-language `none`/`autobuild` matrix instead of forcing `build-mode: none` on every language. Repositories requiring a manual build should own a custom CodeQL workflow.
- ZAP uses a digest-pinned stable container and pins the target hostname to a previously vetted public IPv4 address inside the container, closing the validate-then-resolve DNS-rebinding gap.
- ZAP is intentionally staging-only in this baseline and rejects localhost/private/reserved targets, embedded credentials, and unsafe rules-file paths.
- The ZAP baseline is passive; active scanning is not part of this baseline.
- SARIF upload is optional because GitHub code scanning availability depends on repository/account configuration.
- SBOM generation uses CycloneDX and is retained as a workflow artifact.

## Current tool pins

See `versions.json`. Renovate should update GitHub Action SHAs. Tool-version changes should be reviewed like code changes.
