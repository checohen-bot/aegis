# Aegis

Aegis is building the world's most trusted Investment Intelligence Platform for individual investors.

Aegis does not predict markets or prices. It improves the quality of capital allocation decisions through structured reasoning, evidence, institutional memory, explainability, and continuous learning. The investment philosophy is **Adaptive Quality Investing (AQI)**: decision quality, not prediction accuracy, is the north star. Every recommendation is explainable, every investment has a thesis, every thesis has evidence, every decision is auditable, and knowledge and trust compound over time.

## What this repository is

This repository is not merely the codebase. It is the company's **engineering operating system** — the durable, version-controlled record of how Aegis reasons about its product, its domain, its architecture, and its own way of working. Code is one artifact produced by this system. The decisions, standards, domain model, and institutional memory that govern the code are first-class citizens and live here alongside it.

If the source code were deleted, this repository would still contain enough to rebuild Aegis faithfully: why it exists, who it serves, what it believes about investing, how it is structured, and every consequential decision made along the way.

## How the repository is organized

- **`/bible`** — The Engineering Bible. The highest authority in the repository. It defines the founder manifesto, the investment philosophy, the canonical domain model, engineering principles, and the appendices (glossary, ADR index, references). When any two documents conflict, the Bible wins.
- **`/adrs`** — Architecture Decision Records. Numbered, immutable records of consequential decisions. An ADR is the only mechanism by which a frozen decision can be overridden.
- **`/rfcs`** — Request for Comments specifications. Proposals for substantial changes, reviewed before implementation begins.
- **`/standards`** — Engineering standards: coding conventions, testing expectations, observability, security, and operational practices.
- **`/templates`** — Canonical templates for RFCs, ADRs, domain models, implementation plans, and pull requests.

Root-level governance documents:

- **`FOUNDER.md`** — The frozen founder decisions and the decision-authority model.
- **`CONTRIBUTING.md`** — The mandatory development lifecycle and contribution rules.
- **`CLAUDE.md`** — Operating instructions for automated and AI-assisted engineering within this repository.
- **`LICENSE`** — Proprietary, All Rights Reserved. Public for visibility; not open source.
- **`CHANGELOG.md`** — Human-readable record of notable changes.

## Authority order

When documents or code conflict, resolve in this order:

1. Engineering Bible (`/bible`)
2. Architecture Decision Records (`/adrs`)
3. RFC Specifications (`/rfcs`)
4. Canonical Domain Model (`/bible/03-domain`)
5. Capability Map
6. Product Specifications
7. Existing source code

Source code is the lowest authority. If the code disagrees with a decision recorded above it, the code is wrong.

## Orientation for a new engineer

Aegis is a **modular monolith** with strict domain boundaries, built with Domain-Driven Design and an event-driven internal architecture. The backend, domain logic, and AI services are written in Python. The web frontend is TypeScript with Next.js and React. PostgreSQL is the system of record; Redis provides caching and queues. Everything runs in Docker in every environment. Observability is standardized on OpenTelemetry. AI capabilities are model-agnostic and are never coupled to a specific LLM provider.

V1 is scoped to **long-term public equity investing only**. The architecture deliberately preserves extensibility to other capital allocation domains (Private Equity, Venture Capital, Real Estate, Corporate Capital Allocation, Strategic Procurement), but none of those are implemented in V1.

## Start here (reading order)

Read these in order before writing any code or opening any pull request:

1. **`bible/00-founder-manifesto`** — Why Aegis exists and what it believes.
2. **`CLAUDE.md`** — How work is conducted in this repository.
3. **`bible/03-domain`** — The canonical domain model and the frozen vocabulary you must use.

After that, read `FOUNDER.md`, `CONTRIBUTING.md`, and the `/adrs` directory in numerical order. The ADR index at `bible/appendices/adr-index.md` is the fastest way to survey the decisions that shaped the system.

## A note on vocabulary

The canonical domain object names are frozen and are never renamed: Portfolio, Holding, Company, Investment Thesis, Investment Case, Evidence, Observation, Knowledge, Decision, Capital Mission, Risk, Catalyst, Learning Event, Behavior Profile, Policy. Use these names exactly, in documentation, code, and conversation. Their definitions are in `bible/appendices/glossary.md`.
