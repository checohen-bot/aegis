# Observability

## Principle

No critical workflow in Aegis may become a black box. Thesis evaluation, Decision recording, and IBKR sync — the paths that touch real money and irreplaceable investor reasoning — must be observable in production at all times. Every critical capability (module) exposes three signals: metrics, structured logs, and distributed traces, unified through OpenTelemetry. Observability is a design requirement of a module's definition of done, not instrumentation added after an incident.

## Three Pillars via OpenTelemetry

Aegis standardizes on OpenTelemetry (OTel) so that metrics, logs, and traces share context and correlate cleanly.

### Metrics

Every critical module emits metrics covering the four golden signals — latency, traffic, errors, and saturation — plus domain-specific counters:

- Request/operation rate, error rate, and latency distributions (percentiles, not just averages) per capability.
- Financial-critical domain metrics: IBKR sync success/failure and freshness, count of Decisions recorded, Thesis evaluations run, AI capability calls per provider with success/error/latency and cost signals.
- Resource saturation: connection pool usage, queue depth, Redis and Postgres health.

Metrics are dimensioned enough to diagnose but never carry sensitive values as labels (no account numbers, holdings, or user secrets in metric dimensions).

### Structured Logs

Logs are structured (machine-parseable, key/value), correlated to traces via IDs, and safe by construction:

- Every log line carries a trace/span ID and, where applicable, a user-scoped correlation ID so a single workflow can be reconstructed end to end.
- **Redaction is default.** Loggers inherit secret- and PII-redaction filters (see `secrets-management.md`); developers do not opt in to safety. Brokerage tokens, credentials, and raw sensitive account data never appear in logs.
- Log levels are disciplined: errors and security-relevant events are always logged; sensitive-path successes are logged at a level sufficient to prove the workflow ran without leaking its contents.

### Distributed Tracing

Every critical workflow is traced across module boundaries:

- Thesis evaluation, Decision recording, and IBKR sync produce spans from entry to completion, including calls into the Capability Gateway and out to IBKR and AI providers.
- Spans record outcome, duration, and error status. External calls (IBKR, AI providers) are their own spans so latency and failure attribution is unambiguous — when something is slow or broken, the trace shows exactly which dependency caused it.
- Trace context propagates through async jobs and background sync so nothing critical runs untraced.

## No Critical Workflow Is a Black Box

The following workflows must never lack a full observability picture:

- **Thesis evaluation** — traced, timed, and counted; AI-assisted steps attributed to provider and model.
- **Decision recording** — every write observable; failures surfaced immediately because a lost Decision is unacceptable (see `reliability.md`).
- **IBKR sync** — success, failure, partial state, and data freshness all measured; staleness is a first-class, alertable metric.

If any of these cannot be reconstructed from telemetry after the fact, that is treated as a production defect.

## Alerting Philosophy

Alerting is oriented around investor impact on financial-data-critical paths, not vanity thresholds.

- **Alert on symptoms that matter.** Failed or stale IBKR syncs, elevated Decision-recording error rates, Thesis-evaluation failures, AI provider outages affecting capabilities, and data-integrity anomalies are page-worthy because they degrade the investor's ability to reason or corrupt their trust in the data.
- **Severity-tiered.** Alerts map to the severity model in `incident-response.md`. Anything risking corruption or loss of Thesis/Decision data, or exposure of financial data, is highest severity and pages immediately. Degraded-but-safe conditions (an AI provider down, gracefully degraded) notify but do not necessarily page.
- **Actionable, low-noise.** Every alert links to a runbook and a dashboard. Alert fatigue is itself a reliability risk; thresholds are tuned to be meaningful, and chronically noisy alerts are fixed or removed.
- **Security alerts** — anomalous auth patterns, secret-scanning hits, unexpected access to sensitive data, audit-integrity anomalies — route to the security on-call path and are never silently suppressed.
- **Freshness and silence detection.** Absence of expected signal (a scheduled sync that did not run, a metric that went silent) is alertable. Silence is treated as a potential failure, not as health.

## Instrumentation Standards

- New modules inherit shared OTel instrumentation (auto-instrumentation for HTTP, DB, Redis, and outbound calls) plus explicit spans for domain-critical steps.
- Telemetry carries no secrets or sensitive account data — this is enforced by shared redaction and reviewed in code.
- Dashboards and alerts are defined as code, versioned alongside the module, so observability evolves with the system rather than rotting.

## Rationale

When an investor's IBKR data is stale or a Decision fails to record, the difference between a five-minute fix and a silent, trust-destroying data problem is whether the system can see itself. Comprehensive, correlated, secret-safe telemetry across every critical path is how Aegis stays honest under load and diagnosable under pressure.
