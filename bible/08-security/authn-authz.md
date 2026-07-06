# Authentication & Authorization

## Principle

Authentication proves *who* a principal is; authorization decides *what* that principal may do. Both default to deny (see `secure-by-default.md`). Aegis holds real brokerage access and private financial reasoning, so identity and access control are load-bearing security infrastructure, not conveniences.

## Investor Authentication

Individual investors authenticate to Aegis with credentials the platform controls — never their brokerage password.

- **Credential storage.** Passwords, where used, are stored only as salted hashes using a memory-hard algorithm (Argon2id preferred; bcrypt acceptable). Plaintext or reversibly-encrypted passwords are prohibited. Federated sign-in (OIDC with a reputable identity provider) is preferred where available, so Aegis holds fewer password secrets.
- **Multi-factor authentication.** MFA is available and strongly encouraged for all accounts, and required before a user can link a brokerage connection or perform sensitive account actions. Financial data access warrants a second factor.
- **Sessions.** Sessions use short-lived, signed tokens with server-side revocation. Tokens are transmitted only over TLS, stored in secure, `HttpOnly`, `SameSite` cookies where browser-based, and are invalidated on logout, password change, and suspected compromise. Session lifetime is bounded; sensitive actions may require re-authentication (step-up).
- **Anti-abuse.** Login endpoints are rate-limited and monitored for credential stuffing. Account enumeration is avoided (uniform responses). Lockout and anomaly alerts protect against brute force.

## Brokerage Credential Handling (IBKR)

Aegis never asks for, stores, or transmits a user's raw IBKR username and password. Brokerage linkage uses a delegated, OAuth-style authorization flow.

- The user authorizes Aegis at IBKR; Aegis receives scoped access and refresh tokens, never the underlying login.
- **Least scope.** Aegis requests only the scopes it uses (read of positions/account data required for the product). Trading or withdrawal scopes are not requested unless a specific capability requires them and the user has explicitly consented.
- **Token storage.** Access and refresh tokens are treated as top-tier secrets: application-layer encrypted at rest with a key held in the secrets manager (not the database), never logged, never returned to the client, and never sent to any AI provider.
- **Revocation and disconnect.** A user can disconnect their brokerage link at any time. Disconnection revokes the token at IBKR where supported and deletes the stored token material. Revoked or expired tokens fail closed — the system surfaces a clear "reconnect required" state rather than guessing or serving stale data (see `reliability.md`).
- **Token refresh** follows IBKR's lifecycle with overlapping-validity handling so a refresh never corrupts the linked state.

## Least-Privilege Access to Financial Data (Internal)

Inside the platform, access to sensitive financial data is minimized at every layer.

- **User scoping in the data layer.** Every read/write of holdings, Theses, Decisions, and Evidence is scoped to the owning user at the repository layer, so no application code path can return another user's data. This is enforced structurally, not by per-endpoint discipline.
- **Module least privilege.** Each module holds only the database privileges it needs (per-role credentials, not a shared superuser — see `secrets-management.md`). The AI capability layer accesses only the specific, minimized data a capability call requires (see `data-protection.md`).
- **No standing human access to raw user financial data.** Engineers do not have routine, unaudited access to production holdings or reasoning data. Debugging uses de-identified data where possible. Any human access to production sensitive data is exceptional, requires justification, is time-bounded, and is logged as an auditable event.

## Role Separation for Internal / Admin Tooling

Administrative capability is separated from ordinary user capability and from each other by role.

- **Distinct roles.** Support, operations, engineering, and security are distinct roles with distinct permissions. No single role can both access user financial data *and* silently alter audit logs — separation of duties protects the integrity of the audit trail (see `auditability.md`).
- **Admin actions are never implicit.** Admin tooling requires its own authentication, MFA, and explicit authorization checks. There is no "god mode" that bypasses user scoping without producing an audit record.
- **Every privileged action is audited.** Who did what, to which user's data, when, and why is recorded immutably. Admin access to a user's account is visible in the audit trail and, where appropriate, to the user.
- **Break-glass is controlled.** Emergency elevated access exists for incidents but is time-boxed, requires a second approver where feasible, is loudly logged, and is reviewed after every use.

## Enforcement

- CI rejects endpoints lacking an explicit authorization policy; absence of a rule is treated as a defect, not a default-allow.
- Authorization is centralized in a policy layer so rules are auditable and testable, not scattered across handlers.
- Access-control changes to sensitive-data paths require security review.

## Rationale

The strongest encryption is worthless if the wrong principal is authorized. By proving identity rigorously, delegating brokerage access rather than holding raw credentials, scoping every data access to its owner, and separating administrative duties, Aegis ensures that access to an investor's financial life is always deliberate, minimal, and accountable.
