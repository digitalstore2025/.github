# Security gate policy

## Blocking severity

| Finding | Default action |
|---|---|
| Exposed credential or secret | Block immediately; revoke/rotate if real |
| Critical exploitable dependency | Block |
| High dependency vulnerability | Block unless documented non-exploitability or no fix exists |
| Semgrep ERROR | Block |
| Semgrep WARNING | Block initially; tune narrowly if proven false positive |
| Checkov failed policy | Block for deployed IaC; document explicit exceptions |
| CodeQL high-confidence security alert | Block |
| ZAP baseline FAIL | Block staging promotion until triaged |

## Suppression rules

A suppression is acceptable only when all of the following are recorded:

1. Scanner/rule identifier.
2. Exact affected path/resource.
3. Evidence showing false positive or accepted risk.
4. Owner.
5. Expiration/review date for accepted risk.
6. Compensating control when applicable.

Do not use directory-wide or rule-family-wide suppressions merely to make CI green.

## Secret incident response

If a real credential is detected in Git history:

1. Revoke or rotate it first.
2. Determine exposure and usage from provider logs.
3. Remove the credential from current code/configuration.
4. Decide separately whether history rewrite is justified; do not delay rotation for Git cleanup.
5. Add prevention at pre-commit and CI.
