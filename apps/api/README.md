# Aegis API — Investment Thesis (walking skeleton)

The Phase 1 walking skeleton for Aegis: a real, running, tested end-to-end slice
of the **Investment Thesis** canonical domain object, proving the modular-monolith
architecture (domain / application / adapters), PostgreSQL persistence, a typed
REST API, domain events, and a Docker-based local environment.

Authoritative context: `rfcs/RFC-0001-walking-skeleton-investment-thesis.md`,
`adrs/ADR-0015-walking-skeleton-implementation-choices.md`, and
`bible/03-domain/investment-thesis.md`.

## Module structure

```
src/aegis_api/
  main.py            composition root (app factory, middleware, startup)
  config.py          typed settings from environment
  db.py              SQLAlchemy engine / session / declarative base
  errors.py          standard error-envelope exception handlers
  logging_config.py  structured JSON logging
  modules/thesis/
    domain/          InvestmentThesis aggregate, value objects, events,
                     exceptions, repository port — pure Python, no framework imports
    application/     ThesisService use cases + EventPublisher port
    adapters/        SQLAlchemy repository, ORM row, FastAPI router + DTOs
tests/               domain unit tests + API integration tests
```

Dependencies flow inward: `adapters -> application -> domain`. The domain layer
imports nothing from the outer layers and holds no vendor types.

## Endpoints (`/v1/theses`)

| Method | Path                              | Purpose                          |
|--------|-----------------------------------|----------------------------------|
| POST   | `/v1/theses`                      | Form a Thesis (draft)            |
| GET    | `/v1/theses/{id}`                 | Retrieve one Thesis              |
| GET    | `/v1/theses?limit=&cursor=`       | List Theses (cursor-paginated)   |
| POST   | `/v1/theses/{id}/activation`      | draft → active                   |
| POST   | `/v1/theses/{id}/invalidation`    | active → invalidated (records met condition) |
| GET    | `/health`                         | Liveness signal                  |

State transitions are modeled as sub-resources (not verbs in the path) per
`standards/api-standards.md`. Errors use the standard envelope
`{"error": {code, message, details, traceId}}`.

## Run it

### Via Docker Compose (full stack: db + api + web)

From the repository root:

```bash
docker compose up --build -d       # start postgres, api, web
curl http://localhost:8000/health  # {"status":"ok"}
# API docs:  http://localhost:8000/docs
# Web UI:    http://localhost:3000
docker compose down                # stop (add -v to drop the db volume)
```

Environment variables and their defaults are documented in `.env.example` at the
repo root.

### Directly with uvicorn (fast iteration)

Requires a reachable PostgreSQL (or point `DATABASE_URL` at any SQLAlchemy URL;
SQLite works for a quick spin). From `apps/api`:

```bash
python -m venv .venv && . .venv/bin/activate
pip install -e ".[dev]"
export DATABASE_URL="postgresql+psycopg2://aegis:aegis@localhost:5432/aegis"
uvicorn aegis_api.main:app --reload --port 8000
```

Schema tables are created at startup via SQLAlchemy `metadata.create_all()`.

## Tests

```bash
. .venv/bin/activate
pytest        # unit (domain) + integration (API over HTTP)
mypy          # strict type check, zero errors
```

- **Unit tests** (`tests/test_domain_thesis.py`) construct **real** domain
  objects (never mocked, per `standards/testing-standards.md`) and assert on
  invariants, lifecycle transitions, and emitted domain events.
- **Integration tests** (`tests/test_api_thesis.py`) drive the real FastAPI app
  over HTTP via `TestClient` through the real SQLAlchemy repository.

### Why SQLite in the integration tests

The integration tests run against an ephemeral file-based **SQLite** database
rather than spinning up PostgreSQL. This is a deliberate, pragmatic choice for
the skeleton: it exercises the *real* repository, session handling, and HTTP
layer deterministically and without a container in the test path, keeping the
suite fast and reliable. The identical repository code runs against **PostgreSQL**
under Docker Compose, which is verified separately (see
`IMPLEMENTATION_NOTES.md` for the curl transcript against Postgres). Testcontainers-
backed Postgres integration tests are a natural Phase 2 upgrade.

## What's deferred (per ADR-0015)

Explicitly deferred for this proof-of-architecture skeleton — not silently
skipped, and to be revisited before Phase 2 adds a second module or real data:

- **Alembic migrations** — schema is created via SQLAlchemy metadata for now.
- **Authentication / authorization** — the skeleton is local-only, single-tenant.
- **Full OpenTelemetry** tracing/metrics — structured logging plus a per-request
  placeholder `traceId` only.
- **Real event bus (Redis/broker)** — domain events are typed objects that are
  emitted to structured logs; no cross-module consumer exists yet.
- **AI Capability Gateway** and any broker (IBKR) integration.
