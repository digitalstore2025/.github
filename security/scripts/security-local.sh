#!/usr/bin/env bash
set -euo pipefail

ROOT="${1:-.}"
missing=0

require() {
  if ! command -v "$1" >/dev/null 2>&1; then
    echo "Missing required local tool: $1" >&2
    missing=1
  fi
}

require gitleaks
require semgrep
require trivy
require checkov
require osv-scanner

if [ "$missing" -ne 0 ]; then
  echo "Install the missing tools before running the local security gate." >&2
  exit 2
fi

echo '==> Gitleaks'
gitleaks git --redact=100 --exit-code 1 "$ROOT"

echo '==> Semgrep'
semgrep scan --config auto --error --severity ERROR --severity WARNING "$ROOT"

echo '==> Trivy'
trivy fs --scanners vuln,secret,misconfig --severity HIGH,CRITICAL --ignore-unfixed --exit-code 1 "$ROOT"

echo '==> Checkov'
checkov -d "$ROOT" --quiet --compact

echo '==> OSV-Scanner'
osv-scanner scan source -r "$ROOT"

echo 'Local security gate passed.'
