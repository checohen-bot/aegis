# Testing Strategy

*Volume VII — Engineering · Chapter 4*

Tests are how Aegis proves correctness on a system that moves capital. They are
a first-class deliverable of the Implementation and Tests stages (Chapter 3),
written alongside the code, reviewed with the same rigour, and gated in CI
(Chapter 5). A feature is not done when it works once; it is done when it is
proven to keep working.

## The Test Types

**Unit tests.** The foundation. They exercise a single unit of domain logic —
an aggregate method, a value object's invariant, a policy calculation — in
isolation, with no database, network, clock, or AI provider. Domain code is
designed to make this possible (Chapter 1, Testability): dependencies are
injected, side effects live at edges. Unit tests are fast (milliseconds), run on
every PR and every save, and are the majority of the suite. If a unit needs
infrastructure to test, its design is wrong.

**Integration tests.** These verify that a module works correctly against real
infrastructure — PostgreSQL, Redis, the event bus — and that adapters honour
their interfaces. They run against ephemeral, Docker-provisioned dependencies so
they are reproducible and disposable. Integration tests cover persistence
mapping, migrations, transaction behaviour, event publication and consumption,
and idempotency of handlers. They are slower than unit tests and run in CI on
every PR.

**Contract tests.** Aegis is a Modular Monolith of independently-owned modules
(Volume IV). Contract tests pin the promises between them: a module's published
interface and the schema of the domain events it emits and consumes. A provider
proves it satisfies its contract; a consumer proves it depends only on the
contract, not on internals. These tests are what make replaceability real — an
adapter (LLM, market data, broker) is swappable precisely because its contract
is tested independently of its implementation. AI prompts are contract-tested at
the Capability Gateway boundary so a model swap cannot silently break callers.

**End-to-end tests, where appropriate.** For a small number of critical user
journeys — recording a Decision, validating a Thesis, allocating Capital — we
test the whole path through the running system, frontend to database. E2E tests
are expensive and brittle, so they are used sparingly and deliberately: enough
to catch integration gaps between the web app and the backend, never as a
substitute for unit and integration coverage. Reserve them for flows where a
silent break would directly harm a user's capital decision.

**Business-rule validation tests.** Aegis encodes investment rules — thesis
invariants, allocation constraints, risk limits, policy conditions. These are
tested explicitly against the domain specification, not merely against the
implementation. A business-rule test reads like a statement of the rule ("a
Thesis with unresolved falsification evidence cannot be marked validated") and
fails if the rule is ever violated. They are written with a domain owner's
review so the test asserts the *intended* rule, not the coded one.

**Regression tests.** Every bug that reaches any environment beyond dev earns a
regression test that reproduces it before the fix and passes after. This is
non-negotiable: a bug fixed without a regression test is a bug invited back. The
regression suite is the accumulated memory of everything Aegis has gotten wrong
and refuses to get wrong twice, and it feeds the Learning stage (Chapter 3).

## The Critical-Logic Rule

Three domains carry a bar above all others because they act on user capital and
must be explainable:

- **Thesis validation** — the logic that decides whether an investment thesis
  holds against its evidence.
- **Decision recording** — the capture and provenance of every capital-bearing
  Decision.
- **Capital allocation** — the logic that sizes and distributes capital across
  holdings and missions.

For these, testing is mandatory, exhaustive, and specially reviewed. Every
branch, every boundary, every invariant, and every failure mode is covered by
unit *and* business-rule tests; the paths are covered by integration and, where
a user journey exists, E2E tests; and every historical defect has a regression
test. Coverage of these paths is enforced in CI and cannot be waived by a
reviewer — an override requires an ADR (Chapter 3). Determinism matters here:
these tests inject the clock and seed any randomness so results are reproducible.
Non-deterministic AI outputs never flow unbounded into these paths; they are
mediated by the gateway and validated before they influence a Decision.

## How We Write Tests

Tests are named for the behaviour they assert, not the method they call
("rejects allocation exceeding the mission's cap", not `test_allocate_3`). They
follow arrange–act–assert, test one behaviour each, and avoid asserting on
incidental detail so they survive refactoring. They use realistic domain
fixtures drawn from `/examples`. They never depend on test-execution order,
shared mutable state, or wall-clock time. A test that is flaky is treated as a
failing test and fixed or deleted, never retried into green — flakiness erodes
the trust the suite exists to provide.

## What Coverage Means

We do not chase a single global percentage; a high number over trivial code
proves nothing. We require full coverage of critical investment logic, strong
coverage of domain rules and module contracts, and pragmatic coverage of glue
and edges. The question a reviewer asks is not "what is the percentage?" but
"if this rule broke, which test would tell us?" If the answer is "none", the PR
is incomplete.
