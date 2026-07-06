# ADR-0011: Core Technology Stack

**Status:** Accepted

## Context

A single, deliberate technology stack reduces cognitive load, hiring friction, and integration risk, and lets the team invest deeply rather than broadly. The stack must fit the workloads: Python for backend, domain, and AI work where the ecosystem is strongest; a modern, productive web stack for the web-first surface; a reliable relational system of record; a fast cache and queue; consistent containerized environments; and standardized observability.

The founder has fixed the stack. This ADR records it as the accepted baseline.

## Decision

The core technology stack is:

- **Python** — backend, domain, and AI services.
- **TypeScript, Next.js, React** — web frontend.
- **PostgreSQL** — the system of record.
- **Redis** — cache and queues.
- **Docker** — all environments, from local development to production.
- **OpenTelemetry** — observability (tracing, metrics, logs).

## Consequences

- These technologies are the default for all new work; introducing a different core technology requires a future ADR.
- PostgreSQL is the authoritative store; Redis is never treated as a system of record.
- Every environment runs in Docker so that local, CI, and production behavior are consistent.
- Observability is standardized on OpenTelemetry, so instrumentation is portable across backends and not tied to a single vendor.
- The stack fixes tooling but not architecture; it is subordinate to the architecture ADRs (ADR-0008, ADR-0009, ADR-0013, ADR-0014).
