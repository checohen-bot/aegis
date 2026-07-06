# ADR-0014: Event-Driven Architecture Now; Event Sourcing and CQRS Deferred

**Status:** Accepted

## Context

Aegis's domains must communicate without tight coupling, and the system must capture meaningful things that happen — decisions made, evidence added, learning captured — so that behavior can be explained and audited over time. An event-driven internal architecture achieves this decoupling and supports the auditability the philosophy demands.

Event sourcing (storing state as an append-only log of events) and CQRS (separating read and write models) are powerful but costly patterns. They add significant complexity, and adopting them prematurely, before the domain and its query and consistency needs are well understood, would slow the team and entrench decisions that may not fit.

## Decision

Aegis uses an **event-driven** internal architecture now. Domains communicate through well-defined events, and consequential occurrences are captured as events.

**Event sourcing and CQRS are deferred.** They are not adopted in V1. Adopting either requires a future ADR that explicitly justifies it with demonstrated need.

The system of record remains PostgreSQL storing current state (ADR-0011); events drive communication and capture, not the primary persistence model.

## Consequences

- Domains publish and consume events across boundaries, preserving loose coupling within the modular monolith (ADR-0008).
- Auditability is supported by capturing meaningful events, consistent with ADR-0003, without requiring full event sourcing.
- State is persisted conventionally in PostgreSQL; the system is not built as an event-sourced log in V1.
- Introducing event sourcing or CQRS to any domain is a consequential decision that must pass through the lifecycle and be recorded in a new ADR before implementation.
