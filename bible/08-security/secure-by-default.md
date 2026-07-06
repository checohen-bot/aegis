# Secure by Default

## Principle

Every module, endpoint, configuration, and data path in Aegis ships in its most restrictive safe state. Security is not a feature added late; it is the default posture that a developer must consciously and explicitly loosen — never the reverse. If a new capability is deployed with no security configuration written, it must fail closed, not open.

This is a frozen founder directive. Aegis handles real brokerage account data, real holdings, and the private investment reasoning of individual investors. A single insecure default is not a bug — it is a breach of trust with someone's financial life.

## Default-Deny Access

All access decisions default to deny.

- **Network.** Containers expose no ports beyond those explicitly declared. The database, Redis, and internal module boundaries are never reachable from the public internet. Only the API gateway is exposed, and only over TLS. Inbound firewall/security-group rules are allow-lists; the base rule denies all.
- **Authorization.** Every API route requires an authenticated principal unless it is explicitly and deliberately marked public (health checks, static assets). A route with no authorization decorator/policy must be rejected by CI, not served. Absence of a rule means no access.
- **Data queries.** Every query that touches user-scoped data (holdings, Theses, Decisions, Evidence) is scoped to the authenticated user's identity at the repository layer. There is no code path that returns another user's financial data, and cross-user access is not a runtime check bolted on top — it is enforced in the data-access layer so that forgetting it is impossible.
- **Capability Gateway.** AI capability calls are denied unless the specific capability, its data scope, and its provider are explicitly registered. A new capability cannot silently gain access to sensitive data by default.

## Encryption in Transit

All traffic is encrypted end to end.

- External clients connect only over TLS 1.2+ (prefer 1.3). HTTP is redirected to HTTPS or refused; there is no plaintext listener.
- IBKR connections and all outbound AI provider calls use TLS with certificate validation enabled. Disabling certificate verification is prohibited and blocked in review.
- Internal service-to-service and database connections use TLS where the transport crosses a trust boundary (e.g. managed Postgres, managed Redis). Within a single host's Docker network, isolation is enforced, but production database connections require TLS.

## Encryption at Rest

- The PostgreSQL volume and all backups are encrypted at rest via the storage layer (disk/volume encryption). Backups are never stored unencrypted.
- Application-layer field encryption is applied to the highest-sensitivity fields — brokerage credentials, OAuth tokens, and any secret material — using a key managed outside the database (see `secrets-management.md`). Even a full database compromise must not yield usable brokerage access.
- Redis, when used to cache anything user-scoped, is treated as sensitive storage: encrypted at rest, access-controlled, and never used to persist secrets.

## Minimal Data Collection

We collect and retain the least data required to deliver a capability.

- We do not pull, store, or log brokerage data fields we have no product use for. IBKR sync retrieves only the account data the platform actually reasons over.
- We never persist raw AI provider request/response payloads containing sensitive account data beyond what auditability strictly requires (see `data-protection.md` and `auditability.md`).
- Personally identifying information is separated from investment-reasoning data where feasible, so that analytics and debugging can operate on de-identified data.

## Secure Defaults in Every New Module

When a developer scaffolds a new module or configuration, the defaults must already be safe:

- **Authentication required** on every new endpoint.
- **User-scoped data access** wired through the shared repository layer.
- **Structured logging with secret redaction** enabled — new loggers inherit redaction filters; they do not opt in.
- **Least-privilege credentials.** A new module receives its own scoped credentials, not a shared superuser (see `authn-authz.md`).
- **Feature flags default off.** New capabilities, especially those touching real money or external providers, ship disabled and are enabled deliberately.
- **Config validation at startup.** Missing or malformed security-relevant configuration (TLS settings, secret references, allowed origins) causes a hard startup failure. The system refuses to run in an ambiguous security state rather than degrade silently.

## Enforcement

Secure-by-default is enforced mechanically, not by memory:

- CI rejects endpoints without an explicit authorization policy.
- CI rejects committed secrets, disabled TLS verification, and permissive CORS wildcards.
- A security checklist is part of the definition of done for any module touching financial data, external providers, or authentication.
- Configuration templates and module scaffolds encode these defaults, so the path of least resistance is also the secure path.

## Rationale

Individual investors trust Aegis with data that reveals their net worth, their strategy, and their thinking. The cost of a permissive default here is not measured in downtime — it is measured in irreversible loss of financial privacy. Making the secure state the default state is the only design that survives human error at scale.
