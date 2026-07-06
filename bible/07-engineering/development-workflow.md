# Development Workflow

*Volume VII — Engineering · Chapter 3*

Every feature in Aegis passes through the same lifecycle, in the same order. No
stage is skipped. The workflow is not bureaucracy; it is how a small team keeps
a capital-bearing system correct, explainable, and maintainable. Each stage has
an owner, an input, and a durable artifact. If a stage produced no artifact, it
did not happen.

The lifecycle is:

> Business Need → Research → RFC → Architecture Review → ADR (if required) →
> Domain Model → Implementation Plan → Implementation → Tests → Documentation →
> Review → Release → Learning

## The Stages

**1. Business Need.** Every change starts with a stated need traceable to the
mission — improving the quality of investment decisions for individual
investors. *Owner:* the requester (product or an engineer). *Artifact:* a
problem statement naming the user, the pain, and the intended outcome. No
solutions yet. A need that cannot be articulated in domain terms is not ready.

**2. Research.** Understand the problem before proposing an answer: prior art in
the bible, existing modules and ADRs, domain constraints, technical options,
and cost. *Owner:* the engineer picking up the need. *Artifact:* research notes,
often attached to the draft RFC. This stage is where most bad ideas die cheaply.

**3. RFC.** The Request for Comment is where the change becomes a formal
proposal. Copy the template from `/templates`, write the business need, the
research, the options considered, the recommendation, the domain impact, and the
observability and failure-handling plan. *Owner:* the proposing engineer.
*Reviewers:* the team. *Artifact:* an RFC in `/rfcs`. RFCs are discussed openly;
the goal is to surface disagreement early, on cheap prose, not on expensive code.

**4. Architecture Review.** A designated architecture reviewer (or the review
group) checks the RFC against Volume IV: module boundaries, replaceability,
explainability, event contracts, and the Modular-Monolith constraint. *Owner:*
architecture reviewer. *Outcome:* approved, revised, or rejected — and a ruling
on whether an ADR is required. Implementation RFCs that introduce `/apps` or
`/packages` are gated here.

**5. ADR (if required).** When the change makes a consequential, hard-to-reverse
decision — a new module boundary, a vendor choice, a schema-level commitment, a
deviation from a principle — an Architecture Decision Record is written.
*Owner:* the decision's author. *Artifact:* a numbered, immutable ADR in
`/adrs` capturing context, options, decision, and consequences. Not every change
needs one; every override of a stated principle does.

**6. Domain Model.** Before implementation, model the domain: the entities,
value objects, aggregates, invariants, and events involved, in the language of
Volume III. *Owner:* the implementing engineer, reviewed by a domain owner.
*Artifact:* a domain-model document (template in `/templates`) and, where
useful, a diagram in `/diagrams`. This stage ensures the code will speak the
business, not the framework.

**7. Implementation Plan.** Translate the domain model into a concrete build
sequence: modules touched, interfaces to define, tests to write, migrations,
rollout, and the observability and health-check surface. *Owner:* the
implementing engineer. *Artifact:* an implementation plan. It makes the work
reviewable *before* it is built and prevents scope drift during it.

**8. Implementation.** Now, and only now, code is written — against the approved
plan, following `/standards`, on a feature branch. *Owner:* the implementing
engineer. Every module delivers its mandatory concerns: typed interfaces,
logging, metrics, tracing, configuration, health checks, and failure handling.
Deviation from the plan that matters goes back to the plan, not silently into
the diff.

**9. Tests.** Not a separate afterthought — tests are written alongside
implementation and are a first-class deliverable (Chapter 4). Unit, integration,
and, for critical investment logic, business-rule and regression tests. *Owner:*
the implementing engineer. *Gate:* CI enforces coverage of the critical paths.

**10. Documentation.** Update the bible, `/docs`, and any changed contracts,
prompts, or standards in the same PR as the code. *Owner:* the implementing
engineer. Documentation is a Definition-of-Done item; a PR that changes
behaviour without changing docs is incomplete.

**11. Review.** Peer review against the RFC/ADR, focused on architectural
conformance, domain correctness, and maintainability — not style, which CI
handles (Chapter 7). *Owner:* one or more reviewers, at least one a code owner
for the touched module. *Gate:* approval is required to merge.

**12. Release.** The change is versioned, changelogged, and promoted through
dev → staging → prod (Chapters 5 and 8). *Owner:* the releaser, following the
release checklist. Releases are small, frequent, and reversible.

**13. Learning.** After release, the outcome is observed against the original
business need and recorded as a Learning Event: what was expected, what happened,
what we now know. *Owner:* the feature's engineer and product. *Artifact:* a
learning note that feeds future Research and, sometimes, a new Business Need.
The lifecycle is a loop, not a line.

## Why It Is Strict

The workflow trades a little upfront speed for durable correctness and
explainability. Each artifact — RFC, ADR, domain model, plan, changelog,
learning note — is a link in the chain of provenance that lets any engineer, at
any later date, reconstruct not just *what* Aegis does but *why*. That chain is
the product.
