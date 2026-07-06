# Phase 0 & Phase 1 Milestones

*Volume IX — Execution Playbook · Chapter 4*

This chapter is a **checklist**, not prose. It lists concrete, checkable milestones for the two phases that are current or next: Phase 0 (Engineering Foundation) and Phase 1 (Walking Skeleton). Each item is written so that it is unambiguously either done or not done — a founder can literally read down the list and tick boxes. A milestone is checked only when its stated condition is verifiably true, not when it is "mostly there." Order is roughly dependency order, but items may be worked in parallel where they do not block each other.

## Phase 0 — Engineering Foundation

**Bible & Philosophy**
- [x] Founder manifesto (`bible/00-founder-manifesto`) written and accepted.
- [x] FOUNDER.md authority split documented (founder owns vision/product/philosophy/terminology/architecture direction; engineering owns implementation/testing/repo/infra/CI-CD/docs).
- [x] All canonical domain objects defined in `bible/03-domain` (Portfolio, Holding, Company, Investment Thesis, Investment Case, Evidence, Observation, Knowledge, Decision, Capital Mission, Risk, Catalyst, Learning Event, Behavior Profile, Policy).
- [x] Architectural principles (`bible/04-architecture/principles.md`) written and accepted.
- [x] AI "capabilities not models" volume written.
- [x] Volume IX (this Execution Playbook) complete and reviewed.
- [ ] Full Bible reviewed end-to-end for internal consistency (terminology, cross-references).

**Decisions & Standards**
- [x] ADR process defined and an ADR template committed.
- [x] Baseline ADRs accepted: Modular Monolith, technology stack (Python + TypeScript/Next.js, PostgreSQL, Redis, Docker), module-boundary enforcement, event/provenance conventions.
- [x] Coding standards (Python and TypeScript) written and committed.
- [x] Repository structure and naming conventions documented.
- [x] Definition of Done published (`bible/09-execution/definition-of-done.md`) and agreed as the merge gate.

**Repository & CI/CD**
- [x] Repository initialized with the agreed structure.
- [x] README.md and CLAUDE.md present and accurate.
- [ ] Docker-based local environment defined and starts cleanly from a documented single command.
- [x] CI/CD pipeline configured (build, lint, type-check, test, boundary checks).
- [ ] CI runs green on the empty-but-real repository.
- [ ] Branch protection / merge gates wired to the Definition of Done.

**Operating Readiness**
- [x] Operating model, feature lifecycle, roadmap, milestones, and onboarding documents committed.
- [ ] Onboarding read-order path verified by walking it once.

*Phase 0 exit criterion:* every box above is checked — the rules of construction exist and are enforced before any application code.

## Phase 1 — Walking Skeleton

**First Lifecycle Run**
- [ ] First RFC submitted (proposes the one canonical object for the skeleton).
- [ ] First RFC approved by both founder (mission/meaning) and engineering (buildability).
- [ ] Skeleton ADR accepted (if the slice sets any architectural precedent).
- [ ] Chosen domain object modeled per the Volume III template (attributes, invariants, relationships, lifecycle, aggregate boundary).

**End-to-End Slice**
- [ ] One canonical domain object persisted in PostgreSQL behind its module boundary.
- [ ] One API endpoint exposes the object through a published interface (no cross-module table access).
- [ ] One domain event emitted and observable.
- [ ] At least one test proves the slice end-to-end (create → persist → retrieve → assert invariant).
- [ ] Documentation for the slice committed (domain object + any ADR + interface).
- [ ] Slice reviewed against the Definition of Done and approved.
- [ ] **Walking skeleton passes CI end-to-end** (build, lint, type-check, tests, boundary checks all green on the real slice).
- [ ] Slice released through the pipeline (not merged by hand).

**IBKR Read-Only Proof of Concept**
- [ ] Interactive Brokers sandbox account provisioned.
- [ ] **First real IBKR sandbox connection established** and authenticated.
- [ ] Read-only pull of a single account's positions returns real data.
- [ ] Broker data flows through an adapter that contains no domain logic (replaceability proven).
- [ ] Provenance recorded on ingested data (source, timestamp, inputs current at the time).
- [ ] PoC documented, including the adapter boundary and what would be required to swap the broker.

**Phase 1 Retrospective**
- [ ] Learning captured: what the skeleton proved, what it exposed, what changes the next phase's plan.
- [ ] Roadmap amended if sequence assumptions changed.

*Phase 1 exit criterion:* one domain object lives end-to-end and passes CI, and a real IBKR sandbox connection has returned real position data through a replaceable adapter. The architecture is demonstrated, not asserted — and the company is cleared to begin Phase 2.
