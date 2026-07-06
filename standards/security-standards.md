# Security Standards

Aegis holds investors' financial reasoning and connects to real brokerage accounts. A security defect here is not an inconvenience — it can move real money or leak an investor's entire strategy. These standards are mandatory and enforced in review.

## 1. Secrets never live in code

- No secret — API key, database password, brokerage credential, AI provider token, signing key — is ever committed to the repository, in any branch, in any form, including tests and fixtures.
- Secrets are read from environment variables (injected via the platform secret manager in deployed environments, `.env` locally). `.env` is git-ignored; a committed `.env` is a security incident.
- A `.env.example` documents required variable *names* with placeholder values only.
- Secret scanning (gitleaks/trufflehog) runs in CI and pre-commit. A detected secret blocks merge and triggers rotation of the exposed credential — removing the commit is not sufficient; the secret is considered compromised.
- Never log secrets, tokens, or full brokerage credentials. Redact them in structured logs and error messages.

## 2. Dependency vulnerability scanning

- Every dependency change is scanned: `pip-audit` for Python, `npm audit`/`osv-scanner` for TypeScript, and container image scanning for Docker builds. These run in CI.
- Critical and high-severity advisories block the build. They are remediated by upgrade, or, if no fix exists, by a documented, time-boxed exception approved by a security reviewer and tracked to closure.
- Dependencies are pinned (lockfiles committed). Automated update PRs are reviewed like any other change, not merged blind.
- New third-party dependencies require justification in the PR: what it does, why a first-party solution is inadequate, and its maintenance health.

## 3. Least-privilege database access per module

- Each module accesses only the tables it owns. Cross-module data access goes through the owning module's published interface or domain events — never by querying another module's tables directly.
- Database roles are scoped per module boundary with the minimum grants required (a read-only reporting path uses a read-only role). No module uses a superuser or shared omnipotent connection in application code.
- All queries are parameterized. String-built SQL is prohibited; ORM query builders or parameter binding only. Raw SQL, where unavoidable, is reviewed line by line for injection.
- Migrations grant privileges explicitly and are reviewed for privilege creep.

## 4. Mandatory review for sensitive surfaces

Any change that touches the following requires review and explicit sign-off from a designated security reviewer, in addition to the normal reviewer:

- **Authentication and authorization** — login, session, token issuance/validation, permission checks, tenancy isolation. Authorization is enforced server-side on every request; never trust a client-supplied identity or role. Deny by default.
- **Brokerage credential handling** — storage, retrieval, encryption, and use of IBKR (or any broker) credentials and access tokens. Credentials are encrypted at rest with a managed key, decrypted only in the boundary adapter that needs them, and never pass through the domain layer.
- **PII and financial data export** — any new path that emits portfolio holdings, decisions, or personal data out of the system.

The PR description for these changes must state the threat considered and how it is mitigated. "Refactor only" is not an exemption if the code path is sensitive.

## 5. Boundaries and input handling

- All external input — API requests, webhook payloads, AI provider responses, broker data — is validated and typed at the boundary before entering the application layer. Treat AI output as untrusted input: never execute it, and constrain it to expected schemas.
- Outbound calls (brokerage, AI providers) use TLS with certificate verification enabled. Never disable verification to make a call succeed.
- Apply least privilege to service-to-service and third-party tokens: request the narrowest scope that works.

## 6. Handling incidents

If you discover a leaked secret, an authz gap, or exposed credentials: rotate the affected credential immediately, notify the security channel, and open a tracked incident. Do not quietly fix and move on — a leaked secret is compromised regardless of how briefly it was exposed.

Reviewers enforce every section above. A change touching a sensitive surface without security sign-off is not merged.
