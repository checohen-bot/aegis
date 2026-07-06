# ADR-[number]: [short present-tense title of the decision]

> Copy this file to `adrs/ADR-[number]-[short-slug].md`.
> An ADR records one architecturally significant decision and the reasoning behind it. It is immutable once Accepted — to change the decision, write a new ADR that supersedes this one.

| Field | Value |
|-------|-------|
| **ADR** | ADR-[number] |
| **Status** | [Proposed / Accepted / Rejected / Deprecated / Superseded by ADR-[n]] |
| **Deciders** | [names of those who made the call] |
| **Date** | [YYYY-MM-DD] |
| **Related RFC** | [RFC-[number], or "n/a"] |
| **Supersedes** | [ADR-[n], or "none"] |

## Context

[What is the forces-and-constraints situation that requires a decision? Describe the problem, the relevant part of the architecture (which modules and canonical domain objects are affected), and the constraints in play — technical, domain, regulatory, operational. State the facts neutrally; do not argue for the decision yet. A reader six months from now should understand *why a decision was needed* without external context.]

## Decision

[State the decision in active voice: "We will ...". Be specific and unambiguous. Name the modules, domain objects, boundaries, technologies, and patterns chosen. This is the durable heart of the ADR — write it so it can be quoted in code review to settle a dispute.]

We will [decision].

Key points:

- [specific commitment, e.g., "Evidence is owned by the Knowledge module; other modules reference it by EvidenceId only"]
- [specific commitment]
- [specific commitment]

## Consequences

[The honest results of this decision — good and bad. Every architectural choice has costs; name them.]

**Positive**

- [benefit gained]
- [benefit gained]

**Negative / trade-offs accepted**

- [cost, limitation, or new constraint we now live with]
- [what becomes harder]

**Neutral / follow-on**

- [new work this creates: migrations, follow-up ADRs, instrumentation, deprecations]

## Alternatives considered

[The other options that were genuinely on the table, and why each lost. This is what makes an ADR trustworthy — it shows the decision was chosen, not defaulted into.]

1. **[Alternative A]** — [description]. Not chosen because [reason].
2. **[Alternative B]** — [description]. Not chosen because [reason].
3. **[Alternative C / do nothing]** — [description]. Not chosen because [reason].

## Compliance and enforcement

[How is adherence to this decision enforced in practice? e.g., "Reviewers reject cross-module imports into `knowledge/domain`", "CI check X", "boundary test Y". A decision that cannot be enforced will erode.]

## Notes

[Links to the RFC, discussion threads, benchmarks, or references that informed the decision. Any assumptions that, if invalidated, would warrant revisiting this ADR.]
