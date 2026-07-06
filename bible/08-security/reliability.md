# Reliability

## Principle

Aegis must never corrupt or lose an investor's Thesis or Decision data — full stop. Every reliability decision is subordinate to that invariant. When an external dependency fails, the system degrades gracefully and honestly: it preserves the integrity of the investor's reasoning data, it clearly surfaces any partial-data state, and it never silently guesses a value it does not actually have. A wrong-but-confident number is worse than an obvious gap, because investors make real financial decisions on what Aegis shows them.

## The Non-Negotiable Invariant: No Corruption, No Silent Loss

- **Investor reasoning data is sacred.** Theses, Decisions, and Evidence are written durably and atomically. A failure mid-operation must leave the data in a consistent prior state, never a partially-written or ambiguous one.
- **Writes are transactional.** Multi-step operations that record Decisions or Thesis changes use database transactions so they either complete fully or not at all. Append-only audit history (see `auditability.md`) means a retry never overwrites or duplicates history ambiguously — operations are idempotent where they can be retried.
- **External failures never cascade into data loss.** An IBKR outage or an AI provider error may block *new* enrichment, but it must never damage or delete data the investor already owns.

## Graceful Degradation of External Dependencies

Aegis depends on two classes of external system that can and will fail: IBKR and AI providers. The system is designed to keep functioning safely without them.

### IBKR Unavailable

- When IBKR is unreachable or a token is expired/revoked, the platform serves the last successfully synced data **clearly labeled with its freshness/as-of time** and marks the connection state as degraded.
- The system never fabricates or interpolates current holdings or prices to fill a gap. It shows what it last knew and when it knew it, and it surfaces "reconnect required" or "sync delayed" states plainly.
- Sync retries with backoff; failure and staleness are observable and alertable (see `observability.md`). The investor is never left believing stale data is live.

### AI Provider Unavailable

- The Capability Gateway abstracts providers, so a single provider outage does not take down reasoning features that can fall back or wait.
- When an AI-assisted capability cannot run, the affected feature is disabled or shows an explicit "AI assistance unavailable" state — it does not return a fabricated or empty-but-unlabeled result. Core, non-AI functions (viewing holdings, recording a Decision, reviewing history) remain fully available.
- Timeouts, retries with backoff, and circuit breakers protect the platform from a slow or failing provider degrading the whole system. A hung provider call must never block Decision recording.

## Partial-Data State Is Always Surfaced

This is a first-class product and safety requirement:

- Any time the data shown is incomplete, stale, or missing an AI-derived component, that state is explicitly visible to the investor — with what is missing and, where possible, why.
- Aegis never silently guesses, interpolates, or presents partial data as if it were complete and current. Ambiguity is shown, not smoothed.
- Freshness (as-of timestamps) accompanies externally-sourced data so the investor can weight it appropriately in their own reasoning.

## Health Checks Per Container

Every container exposes health endpoints so orchestration and operators can reason about state:

- **Liveness** — is the process alive and not deadlocked? A failed liveness check triggers a restart.
- **Readiness** — can this instance safely serve traffic right now (dependencies reachable, migrations applied, config valid)? An unready instance is pulled from rotation rather than serving errors or degraded results.
- **Dependency-aware health** distinguishes "the app is down" from "IBKR/AI is degraded but we are safely serving cached, labeled data." Degraded-dependency states are reported, not hidden, and feed the alerting model.
- Health checks are cheap, do not leak sensitive data, and do not themselves cause load amplification.

## Resilience Patterns

- **Timeouts everywhere** on external and inter-module calls — no unbounded waits.
- **Retries with exponential backoff and jitter** for transient failures, with idempotency to make retries safe.
- **Circuit breakers** around IBKR and AI providers to fail fast and recover cleanly rather than pile up.
- **Backpressure and queue bounds** so a surge or a slow dependency cannot exhaust resources and threaten data integrity.
- **Bulkheads** so failure in one capability (e.g. AI enrichment) cannot starve a critical one (e.g. Decision recording).

## Backups and Recovery

- Investor reasoning data is backed up regularly, backups are encrypted at rest (see `secure-by-default.md`), and restores are tested — an untested backup is not a backup.
- Recovery objectives (RPO/RTO) are defined for the data classes that matter most; Thesis/Decision/audit data carries the strictest objectives.

## Enforcement

- New external integrations must ship with timeouts, retries, a degradation path, and a surfaced partial-data state before they are enabled.
- Code review rejects any path that could present stale or partial data as current-and-complete, or that fabricates a missing value.
- Chaos/failure testing exercises IBKR-down and provider-down scenarios to prove data integrity and honest degradation hold.

## Rationale

Investors act on what Aegis tells them. The platform earns trust by being honest about what it knows, refusing to guess about money, and guaranteeing that no external hiccup can ever damage the reasoning history an investor has built. Reliability here means integrity and honesty first, uptime second.
