# Code Review Checklist

> The reviewer works through this checklist on every pull request. Approving a PR means every applicable item is satisfied — not "looks fine". Items marked **(blocker)** prevent merge until resolved. Check "n/a" only where you can defend it.

## 1. Architectural conformance

- [ ] The change respects module boundaries — no reaching into another module's `domain/` internals; cross-module access goes through published interfaces or domain events. **(blocker)**
- [ ] Import direction flows inward (adapters → application → domain); the domain imports nothing outward. **(blocker)**
- [ ] No raw external/vendor types (IBKR, AI provider SDK, ORM rows, HTTP DTOs) appear inside domain or application code — they are translated at the boundary. **(blocker)**
- [ ] Architecturally significant changes link the authorizing RFC/ADR; new architectural decisions are recorded in an ADR. **(blocker)**
- [ ] The PR is single-purpose and reasonably sized; refactors are not mixed with behavior changes.

## 2. Domain correctness

- [ ] Naming uses the canonical domain vocabulary verbatim (Portfolio, Holding, Thesis, Decision, Capital Mission, Evidence, ...); no invented synonyms.
- [ ] Domain invariants are enforced in the model, not merely in the caller (e.g., a Decision requires linked Evidence). **(blocker for investment-critical modules)**
- [ ] Domain events are named as past-tense facts (ThesisFormed, DecisionMade) and raised where the business event occurs.
- [ ] Money, quantities, and prices use precise types (no float for currency); rounding and units are correct.
- [ ] Behavior matches the acceptance criteria in the linked task/RFC.

## 3. Test coverage

- [ ] Correct test types are present for the layer (unit / integration / contract / e2e). **(blocker)**
- [ ] The domain model is never mocked; only external boundaries are faked/mocked. **(blocker)**
- [ ] Failure and rejection paths are tested, not just the happy path.
- [ ] Investment-critical modules (Thesis, Decision, Capital Mission, Risk) meet the 95% branch-coverage floor. **(blocker)**
- [ ] Tests assert on outcomes/behavior and would fail if the change were reverted. Test names read as specifications.
- [ ] Tests are deterministic — no real network, no wall-clock, seeded randomness.

## 4. API and contracts

- [ ] Resources are named for canonical domain objects; versioning and the standard error envelope are used.
- [ ] List endpoints are paginated with bounded limits.
- [ ] Reasoned resources (Decision, Thesis, Capital Mission) include their explainability fields (linked Evidence/Thesis/Policy). **(blocker)**
- [ ] Changes to shared cross-module or external contracts are backward-compatible or version-bumped with an ADR.

## 5. Documentation

- [ ] Public domain classes and use-case handlers have docstrings stating intent and invariants.
- [ ] Comments explain *why*, not *what*; no commented-out code; no TODOs left in merged code.
- [ ] User- or developer-facing docs, API docs, and the changelog are updated where behavior changed.
- [ ] The PR description is complete: business objective, RFC/ADR, architecture impact, testing, known limitations.

## 6. Security

- [ ] No secrets, credentials, or tokens in code, tests, fixtures, or logs. **(blocker)**
- [ ] All external input is validated at the boundary; queries are parameterized; AI output is treated as untrusted.
- [ ] Least-privilege database access is respected; no cross-module direct table queries.
- [ ] Changes touching authn/authz or brokerage credentials carry security-reviewer sign-off. **(blocker)**
- [ ] New/updated dependencies pass vulnerability scanning and are justified.

## 7. Observability

- [ ] Cross-module and external calls are traced with domain-id attributes (no secrets/PII in attributes).
- [ ] New domain events emit their metric (e.g., decision_made_total).
- [ ] Logs are structured, correlated by traceId, and free of secrets.
- [ ] New containers expose `/health/live` and `/health/ready`.

## Reviewer sign-off

- [ ] I have read the diff in full, not just the summary.
- [ ] All applicable items above are satisfied; blockers are resolved.
- [ ] Security reviewer approval obtained where required.
