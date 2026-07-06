# Task / Implementation Plan: [task title]

> Copy this into the tracking issue or `docs/plans/`. An implementation plan turns an accepted RFC/ADR into a concrete, reviewable unit of work *before* code is written. It is the "Implementation Plan" step of the Aegis lifecycle.

| Field | Value |
|-------|-------|
| **Task** | [ID / issue key] |
| **Owner** | [name] |
| **Status** | [Not started / In progress / In review / Done] |
| **Target module(s)** | [e.g., decision, thesis, capital-mission] |
| **Estimate** | [rough size] |

## Linked RFC / ADR

[The work must trace to an authorized decision. Link them.]

- **RFC:** [RFC-[number], or "n/a — internal change within existing design"]
- **ADR:** [ADR-[number], or "n/a"]
- **Related issues:** [#...]

## Scope

[Precisely what will be built. Name the canonical domain objects and modules involved and the behavior being added or changed.]

**In scope**

- [deliverable]
- [deliverable]

**Out of scope**

- [explicitly excluded; deferred to [where]]

## Approach

[The intended technical approach at a glance: key components, new domain events (e.g., DecisionMade), boundary adapters, and where translation happens so no raw vendor types enter the domain. Keep it short — enough for a reviewer to sanity-check the plan before implementation.]

## Acceptance criteria

[Observable, testable conditions that define "done". Write them so anyone can verify them without asking you. Each should map to at least one test.]

- [ ] [Given ... when ... then ... — a concrete, checkable outcome]
- [ ] [e.g., "A Decision cannot be persisted without at least one linked Evidence; attempting it returns a 422 with code DECISION_MISSING_EVIDENCE"]
- [ ] [e.g., "DecisionMade event is emitted and decision_made_total is incremented"]
- [ ] [API responses for the affected reasoned resource include explainability fields]

## Test plan

[How each acceptance criterion is proven. Specify the test types per the testing standards.]

- **Unit:** [domain logic / handlers to cover, including failure paths]
- **Integration:** [repository / event / DB behavior]
- **Contract:** [external boundaries — IBKR, AI provider — pinned]
- **E2E:** [user journey, if applicable]
- **Coverage:** [confirm floor; for Thesis/Decision/Capital Mission/Risk, 95% branch]

## Migrations and data

[Any schema or data migration? Is it reversible? Is it backward-compatible with the currently deployed code (deploy-then-migrate or migrate-then-deploy)?]

- [migration description, or "none"]

## Rollout plan

[How this reaches production safely: feature flag? phased? default off then on? Any coordination with other teams or services.]

## Rollback plan

[If this goes wrong in production, how do we revert — cleanly and quickly? Address code rollback *and* data: is the migration reversible, or is a forward-fix required? A plan with no viable rollback must say so explicitly and justify it.]

- **Code:** [revert the squash-merged PR; any caveats]
- **Data:** [reverse migration, or forward-fix strategy]
- **Flag:** [disable feature flag [name] to neutralize without deploy]

## Observability and monitoring

[What signals confirm this is healthy post-release? New metrics/traces/logs to watch; alerts to add or adjust.]

## Open questions

- [ ] [anything unresolved that blocks starting or completing this task]
