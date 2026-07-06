# ADR-0015: Walking Skeleton Implementation Choices — Framework, Layout, and Deferred Concerns

**Status:** Accepted

## Context

RFC-0001 authorizes building the Phase 1 walking skeleton around the Investment Thesis domain object. ADR-0011 fixes the core technology stack at the company level (Python, TypeScript/Next.js/React, PostgreSQL, Redis, Docker, OpenTelemetry) but does not name specific frameworks within Python, nor does it establish the concrete repository layout for `/apps` and `/packages`, which `bible/07-engineering/repository-guide.md` states will appear "when the first implementation RFC is approved." That RFC is RFC-0001. This ADR makes the concrete choices RFC-0001 depends on and records what is deliberately deferred for a proof-of-architecture skeleton versus what is required for Phase 2 onward.

## Decision

We will implement the walking skeleton as follows:

- **Backend framework:** FastAPI, chosen for its native typed request/response models (aligning with `standards/coding-standards.md`'s strong-typing mandate), automatic OpenAPI schema generation, and async support suited to future I/O-bound work (IBKR, AI providers).
- **Persistence:** SQLAlchemy (2.x, typed ORM style) against PostgreSQL, with the `thesis` module owning its own schema exclusively, per ADR-0008's module-boundary rules.
- **Repository layout:** `apps/api` (Python backend, containing `modules/thesis/{domain,application,adapters}` per `standards/coding-standards.md`) and `apps/web` (minimal Next.js/TypeScript frontend, per ADR-0006). `/packages` remains unused until a second module or a genuinely shared library emerges — introducing it now for one module would be the "unnecessary abstraction" `bible/07-engineering/principles.md` warns against.
- **Local environment:** a single `docker-compose.yml` at the repository root wiring PostgreSQL, the API service, and the web service, run only in local/sandbox contexts.
- **Deferred for this skeleton** (explicitly, not silently): Alembic-managed migrations (schema is created via SQLAlchemy metadata for now); full OpenTelemetry tracing/metrics (structured logging only); authentication and authorization; the AI Capability Gateway; any broker integration. Each deferral is recorded as technical debt in `bible/07-engineering/technical-debt.md`'s spirit and must be revisited before Phase 2 introduces a second module or any real user data.

## Consequences

**Positive**
- Proves the modular-monolith module structure, PostgreSQL persistence boundary, typed API layer, and Docker-based local environment with a real, running, tested slice rather than a description.
- Establishes the concrete `apps/`+module layout that Phase 2 modules (Portfolio, Holding, Company, Decision, etc.) will follow without further architectural debate.

**Negative / trade-offs accepted**
- No migration tooling, auth, or full observability in this slice — acceptable only because it never runs against real data, real users, or a public network.
- FastAPI/SQLAlchemy are now the de facto backend framework choices; changing them later, once a second module depends on the pattern, would require a superseding ADR and nontrivial rework.

**Neutral / follow-on**
- Phase 2 kickoff must introduce Alembic migrations, real authentication, and full OpenTelemetry instrumentation before any module handles real user or brokerage data, consistent with `bible/08-security/secure-by-default.md` and `standards/observability-standards.md`.

## Alternatives considered

1. **Django / Django REST Framework** — more batteries-included, but heavier and less naturally typed than FastAPI's Pydantic-based models; rejected in favor of the lighter, strongly-typed option that better fits `standards/coding-standards.md`.
2. **Introducing `/packages` now for shared domain kernel code** — rejected as premature; `bible/07-engineering/principles.md` explicitly warns against abstractions with only one consumer.
3. **Full production-shaped deployment (Kubernetes manifests, etc.) instead of Docker Compose** — rejected; Phase 1's explicit goal is proof of architecture in an isolated sandbox, not production readiness (see `bible/04-architecture/deployment.md` for the eventual production deployment model).

## Compliance and enforcement

- Code review for any PR touching `apps/api/modules/thesis` checks conformance to `standards/coding-standards.md` (module structure, typing) and `standards/testing-standards.md` (no mocking the domain model).
- Before Phase 2 begins, a follow-up ADR must address migrations, auth, and observability upgrades; the roadmap and milestones documents are updated accordingly at that time.

## Notes

See RFC-0001 for the full business justification and scope boundary. See `bible/03-domain/investment-thesis.md` for the domain model this skeleton implements.
