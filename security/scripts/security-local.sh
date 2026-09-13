#!/usr/bin/env bash
set -euo pipefail

ROOT="${1:-.}"
missing=0

EXPECTED_GITLEAKS='8.30.1'
EXPECTED_SEMGREP='1.177.0'
EXPECTED_TRIVY='0.70.0'
EXPECTED_CHECKOV='3.3.17'
EXPECTED_OSV='2.5.1'

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

check_version() {
  local tool="$1"
  local expected="$2"
  shift 2
  local actual
  if ! actual="$("$@" 2>&1)"; then
    echo "Unable to read $tool version." >&2
    exit 2
  fi
  if [[ "$actual" != *"$expected"* ]]; then
    echo "$tool version mismatch: expected $expected; got: ${actual%%$'\n'*}" >&2
    exit 2
  fi
}

check_version Gitleaks "$EXPECTED_GITLEAKS" gitleaks version
check_version Semgrep "$EXPECTED_SEMGREP" semgrep --version
check_version Trivy "$EXPECTED_TRIVY" trivy --version
check_version Checkov "$EXPECTED_CHECKOV" checkov --version
check_version OSV-Scanner "$EXPECTED_OSV" osv-scanner --version

REPO_ROOT="$(git -C "$ROOT" rev-parse --show-toplevel)"

echo '==> Gitleaks (full Git history)'
gitleaks git --redact=100 --exit-code 1 "$REPO_ROOT"

echo '==> Semgrep'
semgrep scan --config auto --error --severity ERROR --severity WARNING "$ROOT"

echo '==> Trivy'
trivy fs --scanners vuln,secret,misconfig --severity HIGH,CRITICAL --ignore-unfixed --exit-code 1 "$ROOT"

echo '==> Checkov'
checkov -d "$ROOT" --quiet --compact

echo '==> OSV-Scanner'
osv-scanner scan source -r "$ROOT"

echo 'Local security gate passed.'
