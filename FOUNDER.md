# Founder Decisions

This document is the authoritative record of the frozen founder decisions that define Aegis. These decisions are **immutable** through ordinary engineering work. They may only be changed by an explicit, accepted Architecture Decision Record (ADR) that names the decision it supersedes. Until such an ADR exists, these decisions are binding on all contributors, documents, and code.

The founder owns vision, product, investment philosophy, canonical terminology, and architecture direction. This document is the founder's instrument for exercising that ownership in a durable, auditable form.

## Frozen Decisions

### Company and product
- **What Aegis is:** the world's most trusted Investment Intelligence Platform for individual investors.
- **What Aegis is not:** a market or price prediction service. Aegis improves the quality of capital allocation decisions through structured reasoning, evidence, institutional memory, explainability, and continuous learning.
- **Customer:** individual investors.

### Investment philosophy
- **Adaptive Quality Investing (AQI).** Decision quality, not prediction accuracy, is the north star.
- Every recommendation must be explainable.
- Every investment has a thesis.
- Every thesis has evidence.
- Every decision is auditable.
- Knowledge and trust compound over time.

### Brand
- **Apple-level simplicity, Palantir-level depth.** The surface is calm and minimal; the substance beneath is rigorous and deep.

### Business and platform
- **Business model:** hybrid.
- **Platform:** web-first.
- **Broker integration:** Interactive Brokers (IBKR) is the initial broker integration.

### Scope
- **V1 scope:** long-term public equity investing only.
- The architecture must preserve extensibility to Private Equity, Venture Capital, Real Estate, Corporate Capital Allocation, and Strategic Procurement. These domains are **not** implemented in V1.

### Canonical domain objects
The following names are frozen and are never renamed. They are the shared vocabulary of the company across product, engineering, documentation, and code:

Portfolio, Holding, Company, Investment Thesis, Investment Case, Evidence, Observation, Knowledge, Decision, Capital Mission, Risk, Catalyst, Learning Event, Behavior Profile, Policy.

Their canonical definitions are maintained in `bible/appendices/glossary.md`.

### Architecture
- **Modular Monolith** with strict domain boundaries.
- **Domain-Driven Design.**
- **Event-driven** internal architecture. Event sourcing and CQRS are deferred until explicitly justified by a future ADR.
- **AI must be model-agnostic.** It is never coupled to a specific LLM provider. It is built around durable capabilities, not swappable models.
- **OpenTelemetry** for observability.

### Technology stack
- **Python** for backend, domain, and AI services.
- **TypeScript, Next.js, React** for the web frontend.
- **PostgreSQL** as the system of record.
- **Redis** for cache and queues.
- **Docker** for all environments.

### Repository and license
- **Repository:** `aegis` (GitHub: `checohen-bot/aegis`), public visibility.
- **License:** proprietary, All Rights Reserved. The repository is public for visibility and portfolio purposes; the code and methodology are not open source.

### Development lifecycle
No step is ever skipped:

Business Need → Research → RFC → Architecture Review → ADR (if required) → Domain Model → Implementation Plan → Implementation → Tests → Documentation → Review → Release → Learning.

### Authority order
When resolving conflicts, this order governs:

Engineering Bible > Architecture Decision Records (ADRs) > RFC Specifications > Canonical Domain Model > Capability Map > Product Specifications > existing source code.

## Decision Authority

Authority is divided cleanly so that ownership is never ambiguous.

### The founder owns
- **Vision** — what Aegis is and why it exists.
- **Product** — what Aegis does for its customer and what it deliberately does not do.
- **Investment philosophy** — Adaptive Quality Investing and its principles.
- **Canonical terminology** — the frozen domain object names and their meaning.
- **Architecture direction** — the intent and constraints the architecture must satisfy.

### Engineering owns
- **Implementation** — how the product is built.
- **Testing** — how correctness and quality are verified.
- **Repository** — its structure, hygiene, and history.
- **Infrastructure** — environments, deployment, and operations.
- **CI/CD** — the pipeline that moves code to production.
- **Documentation** — the accuracy and completeness of engineering records.

### How the two interact
The founder sets direction and constraints. Engineering decides how to satisfy them and is accountable for the result. When engineering believes a founder decision should change, the mechanism is not persuasion in code review or silent deviation in the codebase — it is an RFC followed by an accepted ADR. Until that ADR is accepted, the decision stands and is implemented faithfully.

## Changing a frozen decision

1. Open an RFC describing the proposed change, the reasoning, and the consequences.
2. Conduct an Architecture Review.
3. If accepted, author an ADR whose Status is Accepted and whose Context explicitly names the founder decision it supersedes.
4. Update this document and the affected Bible sections to reference the superseding ADR.

Absent that chain, a frozen decision cannot be changed by any commit, comment, or convention.
