# Data Protection

## Principle

Aegis holds some of the most sensitive data a person owns: access to their real brokerage accounts, the composition of their wealth, and the private reasoning behind their financial decisions. Data protection governs how each class of data is classified, minimized, retained, exported, deleted, and — critically — how little of it ever reaches a third party, especially an external AI provider. The governing rule is minimal exposure: collect the least, retain it the shortest defensible time, and share the narrowest slice strictly required.

## Data Classification

Not all data is equally sensitive; protection scales with classification.

- **Class 1 — Secret / Credential (highest).** Brokerage credentials, IBKR access/refresh tokens, encryption and signing keys. Compromise grants access to real accounts. Application-layer encrypted at rest with keys in the secrets manager (not the database), never logged, never returned to clients, and **never sent to any AI provider under any circumstance** (see `secrets-management.md`).
- **Class 2 — Financial / Portfolio Data.** Holdings, positions, balances, transaction history synced from IBKR. Encrypted at rest, strictly user-scoped in the data layer, access-audited. Shared with an AI provider only as a minimized, purpose-specific subset when a capability genuinely requires it (see below).
- **Class 3 — Investment Reasoning.** Theses, Decisions, Evidence, and the investor's own written rationale. Deeply personal and central to platform trust; append-only and auditable (see `auditability.md`). Treated as sensitive as portfolio data; minimized before any external processing.
- **Class 4 — Personal Identifying Information.** Name, email, contact and authentication data. Protected, minimized, and separated from Class 2/3 data where feasible so analytics and debugging can run de-identified.
- **Class 5 — Operational / De-identified.** Aggregated metrics and telemetry carrying no secrets or sensitive account values (see `observability.md`). Lowest sensitivity, still handled with care.

Classification is explicit: new data fields are assigned a class when introduced, and protection controls follow from the class automatically rather than being decided case by case.

## Minimal Collection and Retention

- **Collect the least.** We pull only the brokerage fields the product reasons over; we do not hoard data "in case." Minimal collection (see `secure-by-default.md`) is the first line of data protection — data never collected cannot leak.
- **Retention philosophy.** Each data class has a defined purpose and a retention bound tied to that purpose. Data is kept only as long as it serves the investor or a legal obligation, then deleted or de-identified.
  - Class 1 tokens live only as long as the brokerage link is active; disconnection revokes and deletes them.
  - Class 2 portfolio snapshots are retained to support historical reasoning and audit, but raw operational caches are expired aggressively.
  - Class 3 reasoning and its audit trail have the longest retention because reviewable decision history is core to the product and to auditability — but it remains the investor's data, subject to their deletion rights below.
- **Backups** inherit the classification and are encrypted (see `reliability.md`); deletion policies account for backup lifecycles.

## User Data Rights: Export and Deletion

The investor owns their data, and the platform is built to honor that.

- **Export.** Investors can export their data — holdings, Theses, Decisions, Evidence, and decision history — in a portable, machine-readable format. Access to one's own financial reasoning is a right, not a favor.
- **Deletion / erasure.** Investors can request deletion of their account and personal data. Deletion revokes and removes brokerage tokens, removes personal and portfolio data per policy, and honors applicable legal erasure rights.
- **Deletion vs. audit integrity.** Where audit or legal-retention obligations require preserving certain records, we retain the minimum required, de-identify where possible, and record the deletion itself as an authorized, audited event (see `auditability.md`). We are transparent with the investor about what is deleted immediately, what is retained, why, and for how long.
- Requests are verified against the authenticated account owner and fulfilled within committed and legally required timeframes.

## Third-Party Data Sharing Restrictions

We do not sell, rent, or share investor financial or reasoning data. Third-party sharing is restricted to the minimum required to deliver the service, and each recipient is governed by contract and least-privilege access.

## AI Provider Restrictions (Critical)

AI processing is where sensitive data is most likely to leak, so it is governed most strictly.

- **Never raw, never whole.** Raw sensitive account data is never sent to an external AI provider. Class 1 secrets/credentials are *never* sent under any circumstance. For Class 2/3 data, only the minimized, purpose-specific slice strictly required for a given capability call is sent.
- **The Capability Gateway is the choke point.** All AI provider calls route through the Capability Gateway, which enforces what data a specific capability may include, minimizes and where possible de-identifies inputs (stripping account numbers and direct identifiers), and records the exact scope sent for auditability. There is no side channel to a provider that bypasses this control.
- **Purpose limitation and data-use terms.** Providers are used under terms that prohibit training on or retaining our users' data beyond serving the request. Provider selection weighs these data-handling guarantees, not just capability.
- **No provider dependency for integrity.** Because inputs are minimized and audit records are held by Aegis (not the provider), the trustworthiness of an investor's history never depends on an external provider retaining anything.

## Enforcement

- New data fields are classified at introduction; controls follow the class automatically.
- CI and code review block any path that could send Class 1 data — or un-minimized Class 2/3 data — to an external provider or to logs.
- Access to Class 1–3 data is least-privilege and audited (see `authn-authz.md`).
- Export and deletion flows are tested to actually remove/return the data they claim to.

## Rationale

An investor lets Aegis see their whole financial life on the promise that we protect it, minimize its exposure, keep it theirs, and never leak it to an AI provider or anyone else beyond the narrow slice a specific feature truly needs. Rigorous classification, minimization, honored user rights, and a hard boundary at the Capability Gateway are how that promise is kept.
