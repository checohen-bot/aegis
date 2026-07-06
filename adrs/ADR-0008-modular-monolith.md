# ADR-0008: Modular Monolith over Microservices

**Status:** Accepted

## Context

The system must be organized to enforce strict domain boundaries while remaining tractable for a small team at an early stage. Microservices impose distributed-systems overhead — network boundaries, deployment complexity, eventual consistency, operational burden — that is rarely justified before domain boundaries and load characteristics are well understood. A monolith without discipline, however, degrades into tangled coupling.

The founder's architecture direction calls for strict domain boundaries and Domain-Driven Design, delivered with the operational simplicity appropriate to the company's stage.

## Decision

Aegis is built as a **modular monolith** with strict, explicitly enforced domain boundaries.

Domains communicate through well-defined interfaces and internal events, not by reaching into each other's internals or databases. The system is a single deployable unit, but its internal structure is modular enough that a domain could be extracted into a separate service in the future if and when an ADR justifies it.

## Consequences

- One deployable unit keeps operations, testing, and local development simple.
- Domain boundaries are enforced in code structure and review; cross-boundary access is a defect, not a shortcut.
- The modular structure preserves the option to extract services later without a rewrite.
- Premature distribution is explicitly avoided; a move to microservices requires a future ADR grounded in real, demonstrated need.
