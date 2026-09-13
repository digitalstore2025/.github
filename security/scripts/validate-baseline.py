#!/usr/bin/env python3
from __future__ import annotations

import hashlib
import json
import re
import sys
from pathlib import Path

ROOT = Path(sys.argv[1] if len(sys.argv) > 1 else '.').resolve()
SECURITY = ROOT / 'security'
VERSIONS = json.loads((SECURITY / 'versions.json').read_text(encoding='utf-8'))


def fail(message: str) -> None:
    raise SystemExit(f'baseline validation failed: {message}')


def require_contains(path: Path, *needles: str) -> None:
    text = path.read_text(encoding='utf-8')
    for needle in needles:
        if needle not in text:
            fail(f'{path.relative_to(ROOT)} is missing expected pin/invariant: {needle}')


# Immutable reusable-workflow references in consumer templates.
baseline_sha = VERSIONS['reusable_workflow_baseline_commit']
if not re.fullmatch(r'[0-9a-f]{40}', baseline_sha):
    fail('reusable_workflow_baseline_commit must be a full commit SHA')
for path in sorted((SECURITY / 'templates').glob('consumer-*.yml')):
    text = path.read_text(encoding='utf-8')
    if '@main' in text:
        fail(f'{path.relative_to(ROOT)} contains mutable @main')
    refs = re.findall(r'uses:\s+digitalstore2025/\.github/[^@\s]+@([^\s]+)', text)
    if refs and any(ref != baseline_sha for ref in refs):
        fail(f'{path.relative_to(ROOT)} does not pin the audited baseline SHA')

# All GitHub Actions used by central workflows must be exact commit SHA pins.
for path in sorted((ROOT / '.github' / 'workflows').glob('*.yml')):
    for line in path.read_text(encoding='utf-8').splitlines():
        stripped = line.strip()
        if not stripped.startswith('uses:') or stripped.startswith('uses: ./'):
            continue
        if '@' not in stripped:
            fail(f'{path.relative_to(ROOT)} has action without a ref: {stripped}')
        ref = stripped.split('@', 1)[1].split()[0]
        if not re.fullmatch(r'[0-9a-f]{40}', ref):
            fail(f'{path.relative_to(ROOT)} has non-SHA GitHub Action ref: {stripped}')

security_gate = ROOT / '.github/workflows/security-gate.yml'
local_gate = SECURITY / 'scripts/security-local.sh'
zap_workflow = ROOT / '.github/workflows/zap-baseline-reusable.yml'
precommit = SECURITY / 'templates/pre-commit-config.yaml'

# Tool/version parity between documented inventory, CI, and local gate.
require_contains(security_gate, VERSIONS['semgrep']['version'])
require_contains(local_gate, VERSIONS['semgrep']['version'])
require_contains(security_gate, VERSIONS['checkov']['version'])
require_contains(local_gate, VERSIONS['checkov']['version'])
require_contains(security_gate, VERSIONS['osv_scanner']['version'])
require_contains(local_gate, VERSIONS['osv_scanner']['version'].lstrip('v'))
require_contains(security_gate, VERSIONS['trivy']['version'])
require_contains(local_gate, VERSIONS['trivy']['version'].lstrip('v'))
require_contains(security_gate, VERSIONS['gitleaks']['container_manifest_digest'])
require_contains(precommit, VERSIONS['gitleaks']['source_commit'])
require_contains(zap_workflow, VERSIONS['zap']['manifest_digest'])

# Regression invariants from security review.
if 'cache: pip' in security_gate.read_text(encoding='utf-8'):
    fail('setup-python pip caching must not require consumer Python manifests')
require_contains(zap_workflow, '--add-host "$TARGET_HOST:$TARGET_IP"')
if 'zaproxy/action-baseline' in zap_workflow.read_text(encoding='utf-8'):
    fail('ZAP wrapper action reintroduces a DNS validation/use TOCTOU gap')

# Integrity manifest.
manifest = json.loads((SECURITY / 'MANIFEST.json').read_text(encoding='utf-8'))
for entry in manifest['files']:
    path = ROOT / entry['path']
    if not path.is_file():
        fail(f"manifest path does not exist: {entry['path']}")
    actual = hashlib.sha256(path.read_bytes()).hexdigest()
    if actual != entry['sha256']:
        fail(f"manifest hash mismatch: {entry['path']}")

print('DevSecOps baseline validation passed.')
