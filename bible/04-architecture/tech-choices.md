# Architecture: Technology Choices and Rationale

## Purpose

This document records *why* each core technology in the Aegis stack was chosen, in terms of the architectural principles the platform commits to: maintainability, ecosystem fit for AI and data work, developer experience, and avoidance of vendor lock-in. These are frozen decisions; the rationale exists so that future contributors understand the reasoning and can judge whether a proposed change actually respects it. No technology here was chosen for novelty — each earns its place against the modular-monolith, event-driven, model-agnostic architecture.

## Python — Backend, Domain, and AI

Python is the language of the backend monolith, the domain model, and the AI capability layer.

- **Ecosystem fit for AI and data work.** The decisive factor. The mature AI/ML and data ecosystem — provider SDKs, model-agnostic orchestration libraries, vector and retrieval tooling, numerical and data-processing libraries — is native to Python. Because the AI capability layer must be model-agnostic (a capability abstraction over swappable providers), building it where every provider ships a first-class SDK minimizes integration friction and keeps the abstraction thin.
- **Domain expressiveness and maintainability.** Python expresses the canonical domain objects and their invariants clearly, with modern type hints enabling static checking on the domain core. A modular monolith lives or dies by the readability of its boundaries; Python keeps those boundaries legible.
- **One language across concerns.** Domain logic, application services, and AI reasoning share a language and toolchain, so the same engineers move fluidly between the Decisioning module and the Knowledge-retrieval logic feeding the AI layer — a real maintainability gain for a small team.

The cost — raw CPU performance — is not on the critical path for a decision-support platform whose heavy lifting is I/O and model calls, so it does not outweigh the ecosystem advantage.

## TypeScript + Next.js + React — Web

The web client is TypeScript with Next.js and React.

- **TypeScript for maintainability.** Static typing across the frontend catches whole classes of errors at build time and lets the client model the canonical domain objects (Portfolio, Holding, Decision, Knowledge) as explicit types that mirror the API contract. Type safety at the API boundary is a maintainability principle, not a preference.
- **React for a complex, explanation-heavy UI.** Adaptive Quality Investing surfaces reasoning — a Decision with its supporting Thesis, Evidence, and Knowledge. Rendering that richly interlinked, drill-down interface is exactly React's strength: composable components reflecting composable domain objects.
- **Next.js for developer experience and delivery.** Next.js provides routing, server-side rendering, and a coherent build/deploy story out of the box, so the team ships a production-grade web application without assembling a bespoke framework. It containerizes cleanly as the `web` unit in the deployment model.

React and Next.js are the industry-standard, deeply supported choices; they carry the lowest lock-in and hiring risk of the credible options.

## PostgreSQL — System of Record

PostgreSQL is the single durable system of record.

- **Relational integrity for a relational domain.** The canonical objects are richly related (a Holding to a Portfolio to a Company; a Decision to a Thesis to Evidence). A relational store with strong transactional guarantees is the honest fit; aggregate invariants are enforced in local ACID transactions.
- **One engine, many capabilities.** PostgreSQL supports schema-per-module isolation, JSON where semi-structured data is warranted, and vector indexing for the semantic side of Knowledge retrieval — so the platform gets relational truth *and* AI-adjacent retrieval without adding a second database in V1. Fewer moving parts is a maintainability principle.
- **No lock-in.** PostgreSQL is open source and portable across every hosting environment, keeping the system of record free of any proprietary cloud database dependency.

## Redis — Cache, Queues, Event Bus

Redis is the volatile tier: caching, background-job queues, and the pub/sub transport for domain events.

- **Right tool for reconstructible state.** Everything Redis holds is disposable and rebuildable from PostgreSQL, matching Redis's in-memory nature to state that must be fast but need not be the source of truth.
- **Three needs, one dependency.** Caching, queueing, and pub/sub are all served by a single well-understood component, avoiding a separate message broker in V1 while still giving the event-driven architecture a real transport. It is deliberately kept substitutable — the event contract, not Redis, is what modules depend on, so a heavier broker can replace it later without touching domain code.

## Docker — Packaging and Parity

Docker containerizes every runnable unit.

- **Environment parity.** The same image runs local, dev, staging, and production, collapsing the "works on my machine" gap — a direct maintainability and reliability win.
- **Clean mapping to architecture.** Containers align to the C4 container units, and the modular monolith deploys as one backend image (serving both API and worker), keeping operations simple now while leaving room to extract a service later.
- **Ubiquity, no lock-in.** Docker is the portable standard; images run on any orchestrator or host, so no deployment target is baked into the architecture.

## OpenTelemetry — Observability

OpenTelemetry provides tracing, metrics, and logs across every service.

- **Vendor-neutral by design.** OpenTelemetry is an open standard; instrumentation is written once against the standard, and the backend can export to whatever observability backend an environment chooses. This is the single strongest anti-lock-in choice in the stack — observability data is notoriously sticky, and OTel keeps it portable.
- **Explainability's operational twin.** The platform promises explainable *decisions*; OpenTelemetry delivers explainable *behavior* — the correlation IDs that let any API response or IBKR sync failure be traced end to end, satisfying the API and integration error-handling principles.

## Coherence

Read together, the choices share a spine: open standards over proprietary platforms, one strong component per concern rather than many weak ones, a language chosen where its ecosystem is deepest for the work, and portability that keeps every future option — new AI provider, new broker, extracted service, new capital-allocation domain — a configuration or additive change rather than a rewrite.
