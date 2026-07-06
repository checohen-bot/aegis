# ADR Index

This index lists every Architecture Decision Record in numerical order. It is maintained manually: when a new ADR is accepted, add a row here in the same pull request that adds the ADR. ADRs are immutable once accepted; a decision is changed only by a new, superseding ADR, which is added as a new row rather than an edit to an existing one.

| ADR | Title | Status | Summary |
|-----|-------|--------|---------|
| [ADR-0001](../../adrs/ADR-0001-repository-and-visibility.md) | Repository Name "aegis" and Public Visibility | Accepted | The repository is named `aegis` at `checohen-bot/aegis` and is public for visibility, while remaining proprietary and closed source. |
| [ADR-0002](../../adrs/ADR-0002-customer-segment.md) | Customer Segment is Individual Investors | Accepted | The primary customer is the individual investor; product and domain decisions are made for them first. |
| [ADR-0003](../../adrs/ADR-0003-investment-philosophy-aqi.md) | Investment Philosophy is Adaptive Quality Investing (AQI) | Accepted | Decision quality, not prediction accuracy, is the north star; Aegis does not predict markets or prices. |
| [ADR-0004](../../adrs/ADR-0004-brand-positioning.md) | Brand Positioning — Apple Simplicity × Palantir Depth | Accepted | A minimal, calm surface over rigorous, always-reachable depth. |
| [ADR-0005](../../adrs/ADR-0005-business-model.md) | Hybrid Business Model | Accepted | Value capture is a hybrid; core domains assume no single monetization mechanism. |
| [ADR-0006](../../adrs/ADR-0006-web-first-platform.md) | Web-First Platform Strategy | Accepted | The web application is the primary and canonical product surface in V1. |
| [ADR-0007](../../adrs/ADR-0007-ibkr-broker-integration.md) | Interactive Brokers (IBKR) as the Initial Broker Integration | Accepted | IBKR is the first broker integration, built behind a broker capability boundary. |
| [ADR-0008](../../adrs/ADR-0008-modular-monolith.md) | Modular Monolith over Microservices | Accepted | A single deployable modular monolith with strict, enforced domain boundaries. |
| [ADR-0009](../../adrs/ADR-0009-model-agnostic-ai.md) | Model-Agnostic AI Architecture — Capabilities over Providers | Accepted | AI is organized around durable capabilities and never coupled to a specific LLM provider. |
| [ADR-0010](../../adrs/ADR-0010-bible-source-of-truth.md) | Engineering Bible in Git is the Source of Truth; Notion is a Read-Only Mirror | Accepted | Git is the single source of truth for engineering knowledge; any Notion presence is a one-way mirror. |
| [ADR-0011](../../adrs/ADR-0011-technology-stack.md) | Core Technology Stack | Accepted | Python, TypeScript/Next.js/React, PostgreSQL, Redis, Docker, and OpenTelemetry are the fixed baseline. |
| [ADR-0012](../../adrs/ADR-0012-v1-scope-public-equities.md) | V1 Scope Limited to Long-Term Public Equities, with Extensible Architecture | Accepted | V1 is long-term public equities only; the architecture preserves extensibility to other capital allocation domains. |
| [ADR-0013](../../adrs/ADR-0013-domain-driven-design-and-canonical-objects.md) | Domain-Driven Design with Frozen Canonical Domain Object Names | Accepted | DDD with a frozen, never-renamed set of canonical domain object names as the ubiquitous language. |
| [ADR-0014](../../adrs/ADR-0014-event-driven-defer-sourcing-cqrs.md) | Event-Driven Architecture Now; Event Sourcing and CQRS Deferred | Accepted | Domains communicate through events now; event sourcing and CQRS are deferred until a future ADR justifies them. |
| [ADR-0015](../../adrs/ADR-0015-walking-skeleton-implementation-choices.md) | Walking Skeleton Implementation Choices — Framework, Layout, and Deferred Concerns | Accepted | FastAPI + SQLAlchemy under `apps/api`/`apps/web`, Docker Compose locally; migrations, auth, and full observability explicitly deferred until Phase 2. |
