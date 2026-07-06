# Secrets Management

## Principle

Secrets are never in code and never in version control — this is a frozen founder directive with no exceptions. A secret that appears in a commit is considered compromised the moment it is written, regardless of whether the commit is later removed. Aegis manages three primary classes of secret: IBKR API credentials and access tokens, database and Redis credentials, and AI provider API keys. Each is treated as capable of causing serious harm if leaked.

## What Counts as a Secret

- Brokerage credentials and IBKR access/refresh tokens (highest sensitivity — grants access to real accounts).
- Database, Redis, and message-broker credentials.
- AI provider API keys (per provider, via the Capability Gateway).
- Application-layer field-encryption keys and signing keys.
- Webhook signing secrets and any third-party service credentials.

If a value grants access, proves identity, or decrypts data, it is a secret and is governed by this document.

## Never in Code or Version Control

- No secret literals in source, config files, Dockerfiles, docker-compose files, CI definitions, or infrastructure code.
- `.env` files are for local development only, are listed in `.gitignore`, and never contain production secrets.
- Committed configuration references secrets by *name*, never by *value* (e.g. `IBKR_CLIENT_SECRET` is resolved at runtime, not stored).
- Automated secret scanning runs in CI and as a pre-commit hook. A detected secret fails the build and triggers rotation of the exposed credential — removal from history is necessary but not sufficient.

## Environment-Based Injection

Secrets enter the running system only through the environment at deploy time, sourced from a dedicated secrets manager:

- In production, a secrets manager (cloud KMS-backed secret store or equivalent) is the single source of truth. Containers receive secrets as injected environment variables or mounted in-memory files at startup; they are never baked into images.
- The application reads secrets once at startup into a typed configuration object and validates that every required secret is present. A missing required secret is a hard startup failure — the service refuses to run rather than operate degraded or fall back to a default credential.
- Secrets are never written to logs, traces, error reports, or metrics. Structured logging applies redaction filters by default (see `observability.md`), and the config object marks secret fields so they render as `***` in any dump.
- Field-encryption keys used to protect brokerage tokens at rest live in the secrets manager, not in the database that holds the encrypted data. Compromise of the database alone must not yield the decryption key.

## Scoping Secrets per Environment

Every environment — local, CI, staging, production — has its own distinct set of secrets. No secret is shared across environments.

- A staging IBKR credential set is entirely separate from production and, wherever IBKR supports it, points at paper/test facilities rather than real accounts.
- AI provider keys are separated per environment so that non-production usage, quotas, and abuse are isolated and independently revocable.
- Database credentials differ per environment; a leaked staging credential grants nothing in production.
- This scoping means the blast radius of any single leaked secret is bounded to one environment, and rotation in one environment never disrupts another.

## Least-Privilege Scoping

Beyond per-environment separation, each secret grants the minimum access required:

- Database credentials are per-service and role-scoped. The application connects with a role that can read/write only its own schemas — not a superuser. Migration credentials are separate from runtime credentials.
- IBKR access is scoped to the permissions the platform actually uses; unnecessary trading or withdrawal scopes are not requested.
- AI provider keys are project- or workspace-scoped with spending and rate limits set at the provider, so a leaked key cannot generate unbounded cost or exfiltrate quota.

## Rotation Philosophy

Secrets are rotatable by design, and the ability to rotate is tested, not assumed.

- **Assume eventual exposure.** Every secret has a defined owner and a maximum lifetime. Rotation is routine, not an emergency-only procedure.
- **Rotate on a schedule and on trigger.** Scheduled rotation bounds the value of an undetected leak. Event-triggered rotation is immediate upon any suspected exposure, employee offboarding, or scanning hit.
- **Zero-downtime rotation.** The system supports overlapping validity (accept old and new credential during a transition window) so rotation never forces an outage. This is a design requirement for any new secret-consuming module.
- **Rotation is a runbook, not tribal knowledge.** Each secret class has a documented, rehearsed rotation procedure with an expected time-to-complete, so that under incident pressure rotation is mechanical.
- **User-facing brokerage tokens** follow IBKR's token lifecycle: refresh tokens are rotated per provider policy, revocation is honored immediately, and a user disconnecting their brokerage connection revokes and deletes stored tokens.

## Enforcement and Auditability

- Access to the production secrets manager is least-privilege, logged, and reviewed. Every read of a production secret by a human is an auditable event.
- CI blocks merges that introduce secret literals or disable secret scanning.
- Secret access from the application is part of the audit trail where it touches user financial data.

## Rationale

An IBKR credential is a key to someone's real brokerage account. An AI provider key is a channel through which sensitive reasoning could leak or costs could run away. Treating every secret as short-lived, scoped, and externally managed is what keeps a single mistake from becoming a catastrophe.
