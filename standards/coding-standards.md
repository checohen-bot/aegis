# Coding Standards

These standards are enforced in code review. A pull request that violates them is not merged until it conforms. They apply to all first-party code in the Aegis modular monolith: Python (domain, application, AI, API) and TypeScript (web).

## 1. Strong typing is mandatory

**Python.** Every function, method, and module-level constant carries type hints. `mypy --strict` runs in CI and must pass with zero errors. `Any` is prohibited except at genuine dynamic boundaries (deserialization, third-party stubs) and must be justified in a comment. Prefer domain types over primitives: a function that accepts a portfolio identifier takes `PortfolioId`, not `str`. Use `@dataclass(frozen=True)` or Pydantic models for value objects; never pass around bare dicts to represent domain concepts.

**TypeScript.** `strict: true`, `noUncheckedIndexedAccess: true`, and `noImplicitAny: true` are set in `tsconfig.json` and may not be relaxed per-file. `any` is banned; use `unknown` and narrow. All exported functions and React component props have explicit types. Do not use non-null assertions (`!`) to silence the compiler — narrow the type instead.

## 2. Naming aligns to canonical domain objects

The canonical domain vocabulary is fixed: Portfolio, Holding, Company, Investment Thesis, Investment Case, Evidence, Observation, Knowledge, Decision, Capital Mission, Risk, Catalyst, Learning Event, Behavior Profile, Policy.

- Class, type, and file names use these terms verbatim. A class is `InvestmentThesis`, not `Idea`, `Hypothesis`, or `TradeReason`.
- Do not invent synonyms. If a concept is not in the canonical list, it is either a new domain object requiring an ADR, or it belongs to an existing one.
- Identifiers are typed and named `<Object>Id` (`DecisionId`, `HoldingId`).
- Events are past-tense facts named `<Object><Verb>ed`: `ThesisFormed`, `DecisionMade`, `EvidenceRecorded`, `CapitalMissionOpened`.

## 3. No raw vendor objects inside the domain

Domain and application code must never import, reference, or hold a type owned by an external system — IBKR client objects, AI provider SDK response types, HTTP request models, ORM rows exposed as domain entities. These are translated to domain types at the boundary (an adapter, gateway, or repository) and translated back on the way out.

- A broker adapter returns `list[Holding]`, never an `ib_insync.Position`.
- An AI gateway returns domain `Observation` or `Evidence` objects, never a raw provider completion object. The AI layer is model-agnostic; provider types stop at the gateway.
- API request/response schemas (FastAPI/Pydantic, Next.js route types) are boundary DTOs and live in the API layer, not the domain. Map them explicitly.

A `grep` for a vendor package name inside a `domain/` package is a review blocker.

## 4. Module structure

Each domain module is a self-contained package with a stable public surface:

```
modules/<domain>/
  domain/        # entities, value objects, domain events, domain services
  application/   # use cases / command + query handlers
  adapters/      # inbound/outbound: repositories, gateways, API controllers
  __init__.py    # explicit public exports only
```

Cross-module access goes through published application interfaces or domain events — never by reaching into another module's `domain/` internals. Import direction flows inward: `adapters → application → domain`. The domain layer imports nothing from `application` or `adapters`. Circular imports between modules are a design defect, not a lint warning to suppress.

TypeScript mirrors this: feature modules under `web/src/features/<domain>/` with `components/`, `hooks/`, `api/`, and `types/`. Shared UI primitives live in `web/src/ui/`; domain logic never lives in a component.

## 5. Docstrings and comments: explain the why

Comments justify decisions; they do not narrate code.

- **Bad:** `# increment the counter`
- **Good:** `# IBKR reports partial fills out of order; we re-sort by exec time before aggregating.`

Public domain classes and every use-case handler carry a docstring stating the business intent and any invariants they enforce (e.g., "A Decision must reference at least one Evidence; enforced in `__post_init__`"). Do not restate parameter types already visible in the signature. Delete commented-out code before merge — history lives in git. TODO comments are not permitted in merged code; open an issue and link it, or do the work.

## 6. Errors and nulls

Raise typed domain exceptions (`ThesisNotFoundError`), not bare `Exception`. Do not swallow exceptions silently. In TypeScript, model absence with explicit unions or `Result`-style returns for expected failures; reserve thrown errors for the unexpected. Never return `null` where an empty collection is meaningful.

Adherence to these rules is what keeps the monolith modular. Enforce them.
