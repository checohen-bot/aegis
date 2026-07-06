# Testing Standards

Tests are how we protect capital. Investment logic that is wrong is worse than logic that is missing, because it acts with false confidence. These standards define what "tested" means at Aegis and are enforced in review.

## 1. Required test types per module

Every module ships with tests appropriate to its layer. A pull request that adds behavior without the corresponding test type is not merged.

- **Unit tests** — required for all domain logic: entities, value objects, domain services, and use-case handlers. Fast, in-process, no I/O.
- **Integration tests** — required wherever a module touches a real external boundary it owns: repositories against a real PostgreSQL (via Testcontainers or an ephemeral schema), Redis-backed logic, event publication/consumption.
- **Contract tests** — required for every external gateway (IBKR/brokerage, AI providers) and for every cross-module event contract. A contract test pins the shape and semantics we depend on so provider drift breaks CI, not production.
- **End-to-end tests** — required for critical user journeys that span the API and web: forming a Thesis, recording a Decision, opening a Capital Mission. E2E is deliberately sparse; it covers journeys, not permutations.

## 2. Coverage expectations

Line coverage is a floor, not a goal. Global floor is 80%. The following modules carry a hard 95% line-and-branch floor because a defect there mis-allocates capital or corrupts investment reasoning:

- Investment Thesis and Investment Case
- Decision
- Capital Mission
- Risk and Catalyst evaluation

For these modules, every branch of every domain invariant must be exercised, including the failure paths (a Decision rejected for missing Evidence, a Capital Mission that violates a Policy). Coverage on these modules is checked in CI and a regression fails the build. Reviewers additionally confirm that the tests assert on *behavior and outcomes*, not merely that code executed.

## 3. Never mock the domain model

This is the load-bearing rule. You mock the boundaries you do not own; you never mock the model you are testing.

- **Never mock:** domain entities, value objects, domain services, domain events, or use-case handlers. If a Thesis is hard to construct for a test, that is a design signal, not a reason to mock it — build a real one via a test factory.
- **Mock or fake only external boundaries:** the IBKR gateway, AI provider clients, the clock, and outbound HTTP. Prefer in-memory *fakes* (a real in-memory repository, a deterministic fake AI gateway returning canned `Observation`/`Evidence`) over ad-hoc mocks; fakes exercise real behavior and rot less.

A test that patches an `InvestmentThesis` method or asserts a mock's call count on a domain object will be rejected in review.

## 4. Fixtures and test data

- Domain objects are constructed through explicit test factories/builders (`make_thesis(...)`, `make_holding(...)`) that produce valid canonical objects with sensible defaults and overridable fields. Do not scatter raw constructors across the suite.
- Fixtures are the smallest thing that makes the test true. Prefer building the exact state under test over loading a large shared fixture whose relevance is unclear.
- Test data uses realistic domain values (real tickers, plausible weights) so tests double as executable documentation.

## 5. Naming and organization

Tests live beside the code they cover: `modules/<domain>/tests/` for Python, colocated `*.test.ts(x)` for TypeScript. Test names read as specifications of behavior:

```python
def test_decision_is_rejected_when_it_references_no_evidence(): ...
def test_capital_mission_closes_when_thesis_is_invalidated(): ...
```

Structure each test as Arrange / Act / Assert with the intent obvious. One behavior per test; if the name needs "and", split it. TypeScript uses `describe("Decision", () => it("rejects when no evidence linked", ...))`.

## 6. Determinism and speed

Tests must be deterministic and order-independent. No real network, no wall-clock sleeps, no reliance on today's date — inject the clock. Randomness is seeded. Flaky tests are treated as failing tests: quarantine and fix within the sprint, never retry-until-green in CI.

## 7. What review checks

Reviewers verify: the correct test types are present for the layer; the domain is not mocked; critical-module branches (including rejection paths) are covered; assertions check outcomes, not implementation details; and new tests fail if reverted against the old code. A green suite that would still pass with the feature deleted is not a passing suite.
