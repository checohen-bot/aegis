# ADR-0010: Engineering Bible in Git is the Source of Truth; Notion is a Read-Only Mirror

**Status:** Accepted

## Context

Institutional knowledge must have exactly one authoritative home. When the same information lives editably in two systems, they diverge, and no one can say which is correct. Aegis's decisions, domain model, and standards must be versioned, reviewable, diff-able, and bound to the code they govern. Wikis and documents are convenient for reading and sharing but are poor systems of record because they lack rigorous version control and review.

The team also benefits from a friendly, browsable surface for non-engineering stakeholders. That surface must never become an alternate source of truth.

## Decision

The **Engineering Bible in Git** (`/bible`, alongside `/adrs`, `/rfcs`, and `/standards`) is the single source of truth for all engineering knowledge and decisions.

Any Notion presence is a **read-only mirror** of the Git content. It is a convenience for reading and sharing, never a place where authoritative content is authored or edited. When Notion and Git disagree, Git is correct by definition.

## Consequences

- All authoritative knowledge is authored, reviewed, and versioned in Git through pull requests.
- Notion, if used, is generated or copied from Git and carries no authority; edits made there are not real.
- The authority order in `FOUNDER.md` and the README applies to the Git content; mirrors are outside that order.
- Any tooling that syncs to Notion is one-directional, from Git to Notion only.
