# Module Boundaries

*Volume IV — System Architecture · Chapter 5*

The value of a Modular Monolith is entirely in the discipline of its internal
boundaries. Without that discipline it degrades into a "big ball of mud" — a
single deployable with none of the separability that made the pattern worth
choosing. This chapter states the rules that make Aegis's boundaries real and
enforceable, and the criteria under which a module may eventually leave the
monolith. These rules are binding; an exception requires an ADR.

## The Rules

### Rule 1 — Each module owns its domain objects and its data

Every canonical domain object has exactly one owning module (see Chapter 4).
Ownership is total: the owning module defines the object's schema, invariants,
and lifecycle, and is the *only* code permitted to read or write its persistence.
Ownership is physically expressed as a **private PostgreSQL schema per module**.
No shared "domain" schema exists. A module's tables are its private
implementation, as encapsulated as a class's private fields.

### Rule 2 — No direct cross-module database access

No module may issue a query — read or write — against another module's schema.
There are no cross-schema joins, no foreign keys spanning module boundaries, and
no "just this once" shared table. If Module A needs data owned by Module B, it
asks B through B's interface or learns it from B's events. This is the single
most important rule: it is what prevents the database from becoming the hidden
coupling that quietly welds modules together. It is enforced in code review and
by static checks (schema-access linting) and integration tests that fail on
cross-schema access.

### Rule 3 — Collaboration only through interfaces and domain events

Modules communicate in exactly two sanctioned ways, and no others:

- **Published interfaces (synchronous).** A module exposes a narrow, explicit
  interface — a set of typed operations and the data-transfer objects they
  exchange. Callers depend on the interface, never on the implementation. Use
  synchronous interface calls when the caller needs an immediate answer within a
  single request (e.g. the Decision module asking Policy to `evaluate` a proposed
  decision).

- **Domain events (asynchronous).** A module announces facts about things that
  have happened — `HoldingReconciled`, `EvidenceCaptured`,
  `PolicyBreachDetected` — onto the Event Bus (carried over Redis). Subscribers
  react in their own time. Use events when modules must stay decoupled and the
  reaction need not be immediate (e.g. Notification reacting to a breach, or the
  Portfolio projection updating after reconciliation).

Direct imports of another module's internal classes, reaching into its objects,
or sharing mutable in-memory state are all prohibited. The interface and the
event schema are the *entire* contract.

### Rule 4 — Reference by identity, never by embedded state

When one module's object relates to another's — a Thesis to a Company, a Decision
to the Evidence it weighed — it holds the other object's **identity** (a stable
ID), not a copy of its state. State is resolved on demand through the owning
module's interface. This keeps each object's source of truth singular and
prevents stale duplicated data from drifting across boundaries.

### Rule 5 — Events are contracts and carry provenance

Event schemas are versioned, explicit, and treated with the same care as public
APIs; a breaking change to an event is a breaking change to a contract.
Consistent with the explainability principle, events that convey decisions,
observations, or AI output carry provenance (source, model and version where
applicable, and the inputs current at the time). The event stream is a primary
audit surface, not incidental logging.

### Rule 6 — Dependencies point inward and stay acyclic

The domain core (Portfolio, Thesis, Company, Evidence & Knowledge, Risk &
Catalyst, Decision, Policy & Behavior) must not depend on
infrastructure/integration modules (IBKR Integration, AI Capability Gateway) in
the wrong direction: integration modules adapt the outside world *to* the domain,
so the domain defines the interfaces and the adapters implement them
(dependency inversion). The module dependency graph is kept **acyclic**; a
proposed cycle is a design smell to be resolved by introducing an event or an
interface, not by mutual import.

### Rule 7 — AI access only through the AI Capability Gateway

No module may call an LLM provider directly. All AI capability is requested
through the AI Capability Gateway's intent-shaped interface, and every such call
is recorded. This is both a model-agnosticism rule and a boundary rule: it keeps
non-determinism quarantined behind a single, auditable edge.

## Enforcement

Boundaries that rely on goodwill decay. Aegis enforces them mechanically: module
code lives in separate packages with declared, lint-checked dependencies;
schema-access checks fail any query crossing into a foreign schema; interfaces
and event payloads are typed and versioned; and OpenTelemetry traces make
cross-module calls visible so that an illegitimate coupling shows up in the
telemetry. Architectural tests run in CI and fail the build on violation. A
boundary that cannot be violated by accident is the goal.

## Criteria for Extracting a Module into a Service

Aegis stays a monolith until a *specific, evidenced* pressure justifies
extracting a particular module — never as a default, and always recorded in an
ADR. A module is a candidate for extraction only when it already satisfies the
rules above (owns its schema, communicates solely via interface and events) —
which is precisely what makes extraction a transport change rather than a
rewrite. Beyond that precondition, at least one of the following must hold:

1. **Independent scaling.** The module's resource profile diverges sharply from
   the rest of the system — for example, the AI Capability Gateway needing to
   scale on AI throughput independently of investor request load.
2. **Fault isolation.** The module's failure or resource exhaustion must not be
   allowed to degrade the core (e.g. isolating a volatile external-integration
   module).
3. **Independent deployment cadence or team topology.** A dedicated team needs to
   release the module on its own schedule without coordinating the whole
   monolith's deploy.
4. **Divergent operational or compliance requirements.** The module needs a
   separate security boundary, data-residency regime, or runtime that the shared
   process cannot satisfy.

Absent one of these, extraction adds distributed-systems cost for no return and
is rejected. The default answer is "keep it in the monolith"; extraction is an
exception that must be argued and documented. Event sourcing and CQRS are held to
the same standard — deferred until a module's specific needs justify them in an
ADR.
