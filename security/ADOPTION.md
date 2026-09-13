# Adoption guide

## 1. Copy caller workflows

Copy the templates from this repository into the target repository:

```text
security/templates/consumer-security.yml -> .github/workflows/security.yml
security/templates/consumer-codeql.yml   -> .github/workflows/codeql.yml
security/templates/consumer-zap.yml      -> .github/workflows/zap-staging.yml
security/templates/pre-commit-config.yaml -> .pre-commit-config.yaml
security/zap/rules.tsv                    -> .zap/rules.tsv
security/templates/renovate.json          -> renovate.json
```

The reusable workflows live in `digitalstore2025/.github`. The supplied caller templates intentionally pin them to an audited commit SHA rather than mutable `main`. Treat a baseline-SHA update as a normal reviewed dependency change.

`content_scan_path` scopes Semgrep, Trivy, Checkov, and OSV-Scanner. Gitleaks intentionally scans the complete Git history because a secret elsewhere in history remains an exposure even when application code lives in a subdirectory.

## 2. Start in observation mode

Do not make every scanner a required check on the first run. First execute the workflows, classify existing findings, remove false positives, and document accepted risks. Then require the stable jobs in branch protection/rulesets.

Recommended progression:

1. Gitleaks: required immediately. A real secret is a release blocker.
2. Trivy: require HIGH/CRITICAL after baseline cleanup.
3. Semgrep: require ERROR/WARNING after rules are tuned to the codebase.
4. Checkov: require when IaC exists; no blanket suppressions.
5. OSV-Scanner: require after lockfiles/manifests are deterministic.
6. CodeQL: require for supported languages where GitHub code scanning is enabled. Set `build_mode` per language; use `autobuild` where compilation is required and supported.
7. ZAP: run against an explicitly authorized staging target after deployment.

## 3. AI-generated code gate

Any change touching authentication, authorization, payments, file upload, RLS/database policy, admin functions, OAuth/JWT, webhooks, secrets, model tool-calling or external URL fetching receives a human security review even when all automated checks pass.

See `AI-CODE-REVIEW.md`.

## 4. Configure ZAP safely

The consumer workflow is manual by default. Provide the staging URL as the dispatch input. Do not point the baseline at production unless there is an explicit testing authorization and an approved test window.

The reusable workflow rejects localhost, private, link-local, multicast, reserved and unspecified target addresses, URL credentials, fragments, and rules-file traversal. It resolves the target before scanning and pins one vetted public IPv4 address into the ZAP container with Docker `--add-host` so a second DNS resolution cannot rebind the authorized hostname to a private address.

The ZAP image itself is pinned by manifest digest. The workflow currently requires the target to expose at least one public IPv4 address so DNS pinning stays deterministic.

## 5. Enable Renovate deliberately

Install/authorize Renovate for the repository, then use `security/templates/renovate.json`. The template extends `config:best-practices`, groups low-risk updates, pins GitHub Action digests and keeps automerge off by default for security-sensitive updates.

## 6. Make checks required

After baseline stabilization, use repository rulesets/branch protection to require the security jobs before merge. Never bypass required checks for AI-generated changes.
