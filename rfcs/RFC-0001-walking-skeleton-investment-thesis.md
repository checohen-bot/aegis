# RFC-0001: Walking Skeleton — Investment Thesis End-to-End Slice

| Field | Value |
|-------|-------|
| **RFC** | RFC-0001 |
| **Title** | Walking Skeleton — Investment Thesis End-to-End Slice |
| **Status** | Accepted |
| **Author(s)** | Engineering |
| **Reviewers** | Founder, Engineering |
| **Created** | 2026-07-06 |
| **Last updated** | 2026-07-06 |
| **Related** | bible/09-execution/roadmap.md (Phase 1), bible/09-execution/milestones.md, bible/03-domain/investment-thesis.md |

## 1. Business need

The Engineering Bible (Phase 0) is complete: philosophy, domain model, architecture, and standards are written and accepted. Per the roadmap (`bible/09-execution/roadmap.md`), Phase 1 requires proving the architecture is buildable with a real, thin, end-to-end slice before any broader implementation begins. Until one canonical object exists as running, tested, persisted, observable code, the architecture described in Volume IV is a hypothesis, not a proven foundation.

## 2. Context and background

The canonical domain object **Investment Thesis** is already fully specified in `bible/03-domain/investment-thesis.md`: definition, key attributes, invariants (must have at least one falsification condition; must be specific enough to be wrong), relationships, lifecycle states (draft → active → under_review → confirmed/invalidated/retired), and aggregate boundary (an aggregate root, owning its claim, rationale, assumptions, falsification conditions, and lifecycle state).

Investment Thesis is chosen as the walking-skeleton slice because it is the most representative object in the AQI methodology, requires no external integrations (unlike Holding/Portfolio, which need IBKR), and is self-contained enough to exercise the full architecture (persistence, API, module boundary, events, tests) without scope creep.

This build runs in an isolated local/sandbox environment only. It does not connect to Interactive Brokers, does not call any real AI provider, and does not touch any production system. It exists to prove the architecture, per Phase 1's explicit boundary in the roadmap.

## 3. Proposed solution

Implement the `thesis` module as a self-contained package inside a new `apps/api` Python service, following the module structure in `standards/coding-standards.md` (`domain/`, `application/`, `adapters/`), and a minimal `apps/web` Next.js page consistent with ADR-0006 (web-first).

Scope of the slice, matching the lifecycle states already defined in the domain model:
- **Form** a Thesis (`draft` state): core claim, key assumptions, at least one falsification condition, time horizon.
- **Activate** a Thesis (`draft → active`).
- **Invalidate** a Thesis (`active → invalidated`), recording which falsification condition was met.
- **Retrieve** a Thesis and **list** Theses.

Persistence in PostgreSQL, owned exclusively by the `thesis` module's schema (no other module exists yet to conflict with, but the boundary is built correctly from the start per ADR-0008). Domain events (`ThesisFormed`, `ThesisActivated`, `ThesisInvalidated`) are emitted and at minimum logged/observable, proving the event-driven convention in ADR-0014 without requiring a second module to consume them yet.

### Scope

- **In scope:** Investment Thesis domain logic, PostgreSQL persistence, a REST API (`/v1/theses`), a minimal web page to exercise it, unit + integration tests, Docker Compose to run the whole stack locally.
- **Out of scope:** any other canonical domain object; IBKR integration; AI Capability Gateway; authentication (the skeleton is single-tenant/local-only); production deployment; CI wiring beyond what already exists in `.github/workflows`.

## 4. Alternatives considered

1. **Portfolio + Holding via a mock IBKR adapter** — proves the broker-boundary pattern earlier, but requires more scaffolding (two objects, a fake adapter) before anything runs end-to-end. Rejected for the *first* slice; a natural second slice once Investment Thesis proves the pattern.
2. **A non-persistent, in-memory-only skeleton** — faster to stand up, but does not prove the PostgreSQL persistence boundary or Docker Compose story that Phase 1's exit criteria explicitly require. Rejected.
3. **Do nothing / proceed directly to Phase 2** — rejected per the roadmap's explicit floor-before-ceiling sequencing; Phase 2 depends on the architecture being demonstrated, not merely described.

## 5. Architecture impact

- **Domain boundaries:** introduces the repository's first module (`thesis`), and therefore the first use of `/apps` and `/packages`-style layout described in `bible/07-engineering/repository-guide.md`. This RFC is the trigger the repository guide names for their creation.
- **Data / persistence:** new PostgreSQL schema owned solely by the `thesis` module. Schema creation is handled via SQLAlchemy metadata for the skeleton; a real migration tool (Alembic) is deferred and tracked as technical debt per `bible/07-engineering/technical-debt.md`, to be introduced before Phase 2 adds a second module with real migration needs.
- **External boundaries:** none in this slice (no IBKR, no AI provider).
- **API surface:** new `/v1/theses` resource family, per `standards/api-standards.md`.
- **Observability:** structured logs and basic request logging for the skeleton; full OpenTelemetry instrumentation per `standards/observability-standards.md` is deferred to Phase 2 and tracked as debt, since a single-module skeleton has no cross-module traces to prove yet.
- **Security:** no authentication in the skeleton (local-only, no real user data, no secrets). This is acceptable only because the skeleton never runs against real data or a public network; it is explicitly out of scope for anything beyond Phase 1 proof.

## 6. Risks and mitigations

| Risk | Likelihood | Impact | Mitigation |
|------|-----------|--------|------------|
| Skeleton patterns get copied into Phase 2 without adding deferred concerns (migrations, auth, full observability) | M | M | This RFC and the technical-debt entries explicitly flag what is deferred; Phase 2 kickoff must review this RFC first. |
| Docker Compose setup doesn't match production-shape deployment (Volume IV, Chapter on Deployment) | L | L | Compose is explicitly scoped as local/dev-only, not a production deployment artifact. |

## 7. Rollout and migration

Not applicable — this is the first code in the repository, run only in an isolated local/sandbox environment. No production rollout occurs from this RFC.

## 8. Open questions

- [x] Which object to build first — resolved: Investment Thesis.
- [x] Which environment — resolved: local Docker Compose in the current sandbox, isolated from any real broker or production system.

## 9. Decision record

- **Outcome:** Accepted — 2026-07-06, Engineering (walking-skeleton proof, no founder sign-off required per FOUNDER.md since no vision/product/philosophy/terminology/architecture *direction* is being changed — only architecture *direction already set* is being demonstrated).
- **Resulting ADR(s):** ADR-0015
