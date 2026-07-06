# RFC-[number]: [concise, descriptive title]

> Copy this file to `rfcs/RFC-[number]-[short-slug].md` and fill every section.
> An RFC proposes a change and invites review *before* implementation. It precedes Architecture Review and any resulting ADR.

| Field | Value |
|-------|-------|
| **RFC** | RFC-[number] |
| **Title** | [title] |
| **Status** | [Draft / In Review / Accepted / Rejected / Superseded by RFC-[n]] |
| **Author(s)** | [name, @handle] |
| **Reviewers** | [names of required reviewers] |
| **Created** | [YYYY-MM-DD] |
| **Last updated** | [YYYY-MM-DD] |
| **Related** | [links: business need, prior RFCs, issues] |

## 1. Business need

[State the investor or business problem this solves, in plain terms. What need are we serving? What is the cost of not solving it? Reference the originating Business Need or research. Avoid jumping to a solution here.]

## 2. Context and background

[What does a reviewer need to know to evaluate this? Current behavior, relevant domain objects (Portfolio, Thesis, Decision, Capital Mission, ...), constraints, and any prior decisions (link ADRs) that bound this space.]

## 3. Proposed solution

[Describe the proposed change concretely. What is built or changed? Which modules and canonical domain objects are involved? Include the key flow, data, and any new domain events (e.g., ThesisFormed, DecisionMade). Diagrams welcome. Be specific enough that a reviewer could anticipate the ADR that follows.]

### Scope

- **In scope:** [what this RFC covers]
- **Out of scope:** [explicitly excluded, deferred, or handled elsewhere]

## 4. Alternatives considered

[List the real alternatives, including "do nothing". For each, state the trade-off and why it was not chosen. An RFC with no alternatives has not been thought through.]

1. **[Alternative A]** — [description]. Rejected because [reason].
2. **[Alternative B]** — [description]. Rejected because [reason].
3. **Do nothing** — [consequence of inaction].

## 5. Architecture impact

[How does this affect the modular monolith and its domain boundaries? Address each that applies:]

- **Domain boundaries:** [new module? new cross-module contract? boundary changes?]
- **Data / persistence:** [schema changes, migrations, ownership]
- **External boundaries:** [IBKR, AI providers — new or changed adapters]
- **API surface:** [new/changed endpoints, versioning implications]
- **Observability:** [new traces/metrics/domain-event instrumentation required]
- **Security:** [touches authn/authz or brokerage credentials? if so, flag for security review]

## 6. Risks and mitigations

[What could go wrong — technical, operational, or investment-correctness risk — and how is each mitigated?]

| Risk | Likelihood | Impact | Mitigation |
|------|-----------|--------|------------|
| [risk] | [L/M/H] | [L/M/H] | [mitigation] |

## 7. Rollout and migration

[How does this ship? Phased? Feature-flagged? Backfill or data migration needed? How do we roll back if it goes wrong?]

## 8. Open questions

[List unresolved questions that need reviewer input before acceptance. Keep this honest — unknowns belong here, not hidden.]

- [ ] [open question]
- [ ] [open question]

## 9. Decision record

[On acceptance, note the outcome and link the resulting ADR(s). If rejected or superseded, state why and link the successor.]

- **Outcome:** [Accepted / Rejected — date, decider]
- **Resulting ADR(s):** [ADR-[n]]
