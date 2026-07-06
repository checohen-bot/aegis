# Implementation Notes — Walking Skeleton (RFC-0001 / ADR-0015)

Technical record of what was built and verified for the Phase 1 walking skeleton.

## What was built

**`apps/api/` — FastAPI service** implementing the Investment Thesis module with
strict domain/application/adapters separation:

- **Domain** (`modules/thesis/domain/`, pure Python, zero framework imports):
  - `InvestmentThesis` aggregate root — not a SQLAlchemy model; enforces its own
    invariants and owns lifecycle transitions and event recording.
  - Value objects: `ThesisId` (UUID), `FalsificationCondition`, `ConvictionLevel`
    (1–5 ordinal enum), `ThesisStatus` (full lifecycle enum).
  - Typed domain events: `ThesisFormed`, `ThesisActivated`, `ThesisInvalidated`
    (past-tense, real dataclasses).
  - Typed exceptions: `ThesisRequiresFalsificationConditionError`,
    `ThesisNotFoundError`, `InvalidThesisTransitionError`,
    `InvalidThesisStatementError`, and value-object validation errors.
  - `ThesisRepository` port (Protocol) — dependency inversion boundary.
- **Application** (`modules/thesis/application/`): `ThesisService` with use cases
  `form_thesis`, `activate_thesis`, `invalidate_thesis`, `get_thesis`,
  `list_theses`. Clock is injected for determinism. `EventPublisher` port with a
  `LoggingEventPublisher` implementation.
- **Adapters** (`modules/thesis/adapters/`): `SqlAlchemyThesisRepository`,
  `ThesisRow` ORM model, and the FastAPI router with camelCase Pydantic DTOs,
  cursor pagination (`data`/`page` envelope), and the required `basedOn`
  explainability block.
- **Shared infra**: typed config from env, structured JSON logging, per-request
  `traceId` middleware, standard error-envelope handlers (404/409/422), startup
  `metadata.create_all()`, `/health` endpoint.
- Packaging: `pyproject.toml` (fastapi, uvicorn, sqlalchemy, psycopg2-binary,
  pydantic; dev: pytest, httpx, mypy), `Dockerfile`.

**`apps/web/` — Next.js (TypeScript, App Router)**: list page, create form
(multiple falsification conditions, conviction 1–5), and a detail page with
Activate / Invalidate actions. Typed fetch client returning a `Result` union;
`strict` + `noUncheckedIndexedAccess`. Multi-stage `Dockerfile` (standalone output).

**Root**: `docker-compose.yml` (db / api / web with healthchecks and a named
volume), `.env.example`.

**Tests** (`apps/api/tests/`): 24 tests — domain unit tests (real objects, not
mocked) covering the falsification invariant, statement/conviction validation,
lifecycle transitions, and event emission; API integration tests driving real
HTTP through a real SQLAlchemy repository (form → get → activate → invalidate →
list, plus 404/409/422 envelopes and pagination).

### Sandbox build note (not part of the product)

Images build behind a TLS-intercepting egress proxy. The Dockerfiles include an
empty, no-op `certs/` CA-injection point (a standard corporate-proxy pattern);
the sandbox proxy CA is dropped there at build time and is git-ignored
(`apps/*/certs/*.crt`). In a normal environment `certs/` is empty and the step
is inert. Docker Hub blobs are pulled via the `mirror.gcr.io` registry mirror
configured in the daemon; this is environment setup, not repository code.

## Deferred (matching ADR-0015)

- Alembic-managed migrations (schema via SQLAlchemy metadata for now)
- Authentication / authorization (local-only, single-tenant)
- Full OpenTelemetry tracing/metrics (structured logs + placeholder `traceId`)
- Real event bus / Redis (events are typed objects emitted to logs)
- AI Capability Gateway; IBKR / broker integration

## Verified proof

Environment: `docker compose build` + `docker compose up -d`; db and api reached
`healthy`, web served HTTP 200. All commands run against the running stack.

### Test suite (local venv)

```
24 passed in 0.42s
mypy: Success: no issues found in 21 source files
```

### API lifecycle over HTTP (against PostgreSQL in Docker Compose)

```
POST /v1/theses                     -> HTTP 201  (status "draft", id 176b6e95-…)
GET  /v1/theses/{id}                -> HTTP 200  (status "draft")
POST /v1/theses/{id}/activation     -> HTTP 200  (status "active", lastReviewedAt set)
POST /v1/theses/{id}/invalidation   -> HTTP 200  (status "invalidated",
                                        invalidationConditionMet recorded)
GET  /v1/theses?limit=25            -> HTTP 200  ({"data":[…],"page":{"nextCursor":null,
                                        "hasMore":false,"limit":25}})
```

Error envelopes:

```
GET  /v1/theses/{unknown}           -> HTTP 404  code THESIS_NOT_FOUND
POST .../invalidation (bad state)   -> HTTP 409  code INVALID_THESIS_TRANSITION
POST /v1/theses (no falsification)  -> HTTP 422  code VALIDATION_FAILED
```

### Domain events observed in `docker compose logs api` (structured JSON)

```
{"level":"INFO","logger":"aegis.thesis.events","message":"domain_event","event":"ThesisFormed","thesis_id":"176b6e95-…","occurred_at":"2026-07-06T03:29:16.810983+00:00"}
{"level":"INFO","logger":"aegis.thesis.events","message":"domain_event","event":"ThesisActivated","thesis_id":"176b6e95-…","occurred_at":"2026-07-06T03:29:16.859428+00:00"}
{"level":"INFO","logger":"aegis.thesis.events","message":"domain_event","event":"ThesisInvalidated","thesis_id":"176b6e95-…","occurred_at":"2026-07-06T03:29:16.878429+00:00"}
```

### Web

`GET http://localhost:3000/` -> HTTP 200, rendering the Aegis thesis list shell.
