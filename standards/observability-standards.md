# Observability Standards

If we cannot see it, we cannot operate it or learn from it. Observability at Aegis serves two purposes: keeping the platform healthy, and making the investment *intelligence* auditable — every Thesis, Decision, and Capital Mission leaves a trace. These standards are enforced in review and are built on OpenTelemetry.

## 1. Tracing: every cross-module and external call is a span

- All cross-module application calls and all outbound boundary calls (PostgreSQL, Redis, IBKR/brokerage, AI providers) are wrapped in OpenTelemetry spans. Trace context propagates across module boundaries and out to the web tier, so a single user action produces one connected trace end to end.
- Inbound API handlers start (or continue) a trace; the trace id is returned to clients in error responses (`traceId`) and set as a response header.
- Spans are named for the operation, not the framework: `decision.record`, `ibkr.fetch_positions`, `ai.generate_observation`. Attach domain identifiers as span attributes (`thesis.id`, `portfolio.id`, `capital_mission.id`) — never secrets, credentials, or full PII.
- AI provider calls record the model-agnostic attributes needed to reason about them: provider, model, token counts, latency, and a stable request id — set at the gateway, never inside the domain.

## 2. Metrics: instrument key domain events, not just infrastructure

Beyond standard RED metrics (request rate, errors, duration) on every API endpoint, each module emits metrics for the domain events that matter to the business. At minimum:

- `thesis_formed_total`, `thesis_invalidated_total`
- `decision_made_total` (labeled by action: open/reduce/close/hold)
- `capital_mission_opened_total`, `capital_mission_closed_total`
- `evidence_recorded_total`, `observation_generated_total`
- `learning_event_recorded_total`

Metrics are counters/histograms with bounded, low-cardinality labels (action, module, outcome). Never label a metric with a raw identifier, user id, or ticker set that explodes cardinality. Latency-sensitive paths (AI generation, brokerage sync) also emit duration histograms. Emitting the domain-event metric is part of "done" for the handler that raises the event — a `DecisionMade` handler that does not increment `decision_made_total` is incomplete.

## 3. Structured logging

- Logs are structured JSON, one event per line, never free-form `print`/`console.log`. Every log line carries: `timestamp` (RFC 3339 UTC), `level`, `service`, `module`, `message`, `traceId`, and `spanId`, plus relevant domain ids as typed fields.
- Log levels are used with discipline: `ERROR` for failures requiring attention, `WARN` for recovered/degraded conditions, `INFO` for significant domain events, `DEBUG` for development detail (off in production). Do not log at `ERROR` for expected, handled conditions.
- Logs never contain secrets, brokerage credentials, or full AI provider payloads. Redact at the logging boundary.
- Log the *why* and the outcome, correlated by trace id — logs, metrics, and traces must be joinable. A log line describing a Decision includes `decisionId`, `thesisId`, and `traceId` so it ties back to the reasoning and the trace.

## 4. Health checks per container

Every deployable container exposes two endpoints:

- `GET /health/live` — liveness. Returns `200` if the process is up and able to serve. It does not check dependencies; a slow database must not cause a liveness failure and a needless restart.
- `GET /health/ready` — readiness. Returns `200` only when the container can serve real traffic: required dependencies (its database, Redis, essential gateways) are reachable. Returns `503` with a per-dependency breakdown when not ready, so the orchestrator withholds traffic.

Health endpoints are unauthenticated, cheap, side-effect-free, and never expose secrets or detailed internal topology beyond dependency up/down status.

## 5. What review checks

Reviewers verify that: cross-module and external calls are traced with domain-id attributes; new domain events emit their metric; logs are structured, correlated by trace id, and free of secrets; and any new container ships both health endpoints. A feature that runs but cannot be observed is not complete. Instrumentation is written with the code, not bolted on after an incident.
