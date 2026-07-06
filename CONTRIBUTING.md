# Contributing to Aegis

Aegis is built through a disciplined, documented process. This is not bureaucracy for its own sake — it is how institutional memory and decision quality compound over time, which is the same standard Aegis holds itself to for its customers. Contributions that respect the process are welcome. Contributions that bypass it are not accepted.

## The mandatory development lifecycle

Every substantive change passes through this lifecycle. No step is ever skipped, though small changes may pass through several steps in a single lightweight document.

1. **Business Need** — State the problem or opportunity in terms of the customer and the company objective. If there is no articulated need, there is no work.
2. **Research** — Gather evidence, prior art, constraints, and options. Record what was learned, including what was rejected.
3. **RFC** — Write a Request for Comments specification proposing the change. See "Proposing an RFC" below.
4. **Architecture Review** — Review the RFC against the Engineering Bible, existing ADRs, and the domain model. Confirm the change respects domain boundaries and the frozen decisions.
5. **ADR (if required)** — If the change makes or alters a consequential, hard-to-reverse decision, record it as an Architecture Decision Record. See "Creating an ADR" below.
6. **Domain Model** — Update or extend the canonical domain model as needed, using only the frozen canonical object names.
7. **Implementation Plan** — Break the work into a concrete, reviewable sequence.
8. **Implementation** — Build it.
9. **Tests** — Prove it works and guard against regression.
10. **Documentation** — Update the Bible, standards, changelog, and any affected records.
11. **Review** — Peer review against the RFC, ADR, and standards.
12. **Release** — Ship it through the standard pipeline.
13. **Learning** — Capture what was learned as a Learning Event so the next decision is better than this one.

## Proposing an RFC

1. Copy the RFC template from `/templates`.
2. Place the RFC in `/rfcs` with the next sequential number and a descriptive slug.
3. State the Business Need, the research and options considered, the proposed specification, the domain impact, the alternatives rejected, and the open questions.
4. Request an Architecture Review. The RFC is not "in progress" until it has been reviewed and its status reflects that.

An RFC is a proposal, not a decision. It becomes binding only through review and, where required, an accepted ADR.

## Creating an ADR

An ADR is required whenever a decision is consequential and costly to reverse — for example, a change to architecture direction, a technology choice, a domain boundary, or any deviation from a frozen founder decision.

1. Copy the ADR template from `/templates`.
2. Place the ADR in `/adrs` with the next sequential number (`ADR-NNNN-short-title.md`).
3. Use the standard sections: Title, Status, Context, Decision, Consequences.
4. Set Status to `Accepted` only after Architecture Review approves it. A superseding ADR must name the ADR or founder decision it replaces in its Context.
5. Add the new ADR to the index at `bible/appendices/adr-index.md`.

ADRs are immutable once accepted. They are not edited to reflect new thinking; they are superseded by a new ADR.

## Pull request expectations

Every pull request must include, in its description:

- **Referenced RFC and/or ADR** — the identifiers of the specification and decision that authorize this change. A PR that changes behavior without a referenced RFC or ADR is incomplete.
- **Business objective** — the Business Need this PR serves, stated plainly.
- **Testing performed** — what was tested and how, including automated tests added or changed and any manual verification.
- **Known limitations** — what this PR deliberately does not do, and any follow-up required.

Additional expectations:

- Use only the frozen canonical domain object names in code, comments, and description.
- Respect domain boundaries. A PR that reaches across a boundary must be justified by the referenced RFC/ADR.
- Keep the PR scoped to its stated objective. Unrelated changes belong in their own PR.
- Update documentation and the changelog in the same PR that changes behavior.

## Undocumented pull requests are not accepted

A pull request that lacks a referenced RFC or ADR, a stated business objective, a description of testing performed, and its known limitations will be closed or sent back regardless of code quality. Working code is necessary but not sufficient. In this repository, undocumented work does not exist, because the record — not the diff — is the asset that compounds.
