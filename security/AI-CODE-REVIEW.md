# AI-generated code security review

Automated scanners find known patterns. They do not prove business authorization, tenant isolation or correct security intent. Treat AI-generated code as untrusted implementation until validated.

## Mandatory human-review zones

- Authentication and session lifecycle
- Authorization, RBAC/ABAC and object ownership
- Payments, billing and refunds
- File upload, parsing, archive extraction and media processing
- Database policies, RLS and privileged queries
- Admin and support impersonation features
- OAuth, OIDC, JWT and webhook verification
- Secrets, encryption and key-management code
- SSRF-sensitive outbound HTTP and URL-fetching code
- AI agents, tool calling, MCP integrations and prompt-injection boundaries

## Review questions

### Authorization

- Is authorization enforced server-side on every sensitive operation?
- Can a user change an object ID and access another tenant's data?
- Are admin-only operations protected independently from UI visibility?

### Input and output boundaries

- Is untrusted input schema-validated before use?
- Are database queries parameterized?
- Are HTML/Markdown rendering paths protected against injection?
- Are uploaded files constrained by size, content and storage policy?

### Secrets and identity

- Are secrets absent from source, logs, client bundles and exception messages?
- Are JWT algorithms, issuer, audience, expiration and key rotation validated?
- Are webhook signatures validated before payload processing?

### AI/agent-specific boundaries

- Can retrieved documents or web content redefine system/tool policy?
- Does every destructive/external tool call have authorization independent of model text?
- Are tool arguments schema-validated and least-privilege scoped?
- Can an agent exfiltrate secrets through URLs, logs or tool outputs?
- Are memory writes isolated by user/tenant and constrained to appropriate data classes?

## Merge rule

A green CI run is necessary but not sufficient for the zones above. Require a reviewer who understands the affected trust boundary and record accepted residual risk in the PR when relevant.
