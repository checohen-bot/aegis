# Repository Guide

*Volume VII — Engineering · Chapter 2*

This chapter is a guided tour of `checohen-bot/aegis`. Read it before you clone,
and keep it open during your first week. The repository is public under a
proprietary licence; treat everything in it as visible to the world and owned by
Aegis. The layout is deliberate: it encodes the development lifecycle
(Chapter 3) as directories, so that following the process is the same as
navigating the tree.

## Where To Look First

A new engineer starts in exactly one place: **`/bible`**. It is the source of
truth for how Aegis thinks — domain, architecture, and engineering. Read
Volume III (Domain) and Volume IV (Architecture) before writing code, then this
volume. Nothing else in the repository will make sense until the bible does.

## The Directories

**`/bible` — the handbook.** The canonical, curated knowledge of Aegis,
organised into numbered volumes. It is prose, not code, and it changes slowly
and deliberately through review. When code and bible disagree, one of them is a
bug; the bible usually wins, and if it does not, the bible is updated in the
same PR. This is the only directory a non-engineer is expected to read cover to
cover.

**`/adrs` — Architecture Decision Records.** Immutable, numbered records of
consequential decisions and their context, options, and consequences. An ADR is
never edited after acceptance; it is superseded by a newer ADR that references
it. Read the ADR index to understand *why* Aegis is shaped the way it is — every
"why is it done this way?" answer lives here.

**`/rfcs` — Requests for Comment.** Proposals under discussion or recently
decided. An RFC is where a change begins its formal life (Chapter 3): it states
the business need, the research, the options, and a recommendation. RFCs are the
working memory of the team; ADRs are the long-term memory distilled from them.

**`/standards` — normative engineering rules.** Language style guides (Python and
TypeScript), naming conventions, error-handling rules, logging and metrics
conventions, API and event-schema standards, security baselines. Where the bible
explains principles, `/standards` gives the enforceable specifics that CI and
reviewers check against.

**`/templates` — the starting points.** Templates for RFCs, ADRs, domain models,
implementation plans, pull requests, and new modules. Never start these
documents from a blank page; copy the template. The templates encode the
required sections so that the process cannot be accidentally skipped.

**`/diagrams` — architecture and domain diagrams.** Source-controlled diagrams
(module maps, event flows, sequence diagrams, context maps) kept as text-based
sources where possible so they diff and review like code. Diagrams are
referenced from the bible and RFCs, never left to drift on someone's laptop.

**`/prompts` — versioned AI prompts.** The prompt library for the model-agnostic
AI subsystem. Prompts are versioned artifacts with owners, because the
Capability Gateway records which prompt version produced each Observation or
Knowledge item (Volume IV). A prompt change is a code change and follows the same
review.

**`/docs` — generated and operational documentation.** Runbooks, onboarding
notes, API references, and operational guides. Distinguished from `/bible`:
`/docs` is practical and fast-moving ("how do I run the migration?"); `/bible`
is durable and principled ("why do migrations work this way?").

**`/examples` — worked examples.** Reference implementations and usage examples —
a canonical module, a sample adapter, an example event handler. New engineers
copy patterns from here rather than inventing them, which keeps the codebase
consistent.

**`/scripts` — automation.** Setup, local-environment bootstrapping, code
generation, migration helpers, and maintenance tasks. The rule of thumb: any
command a human runs more than twice becomes a script here, so the "right way"
is the "easy way" (Chapter 6).

**`/.github` — the repository's control plane.** CI/CD workflows, PR and issue
templates, CODEOWNERS, and branch-protection-supporting configuration. This is
where the gates described in Chapter 5 are defined. Read the workflows to know
exactly what runs on your PR before it does.

## The Future Directories

Two directories do not yet exist and must not be created speculatively:

**`/apps` — deployable applications.** The web frontend (Next.js/React) and any
runnable backend entrypoints. It appears when the first implementation RFC is
approved — not before.

**`/packages` — shared libraries and domain modules.** The Python domain
modules, the AI Capability Gateway, shared TypeScript packages, and internal
tooling. This is where the Modular Monolith's modules physically live, each with
the mandatory concerns of Volume IV: ownership, typed interfaces, tests,
logging, metrics, tracing, docs, versioning, health checks, configuration, and
failure handling.

Their absence is intentional and enforces the lifecycle: **Aegis writes its
thinking down before it writes its code.** Until an implementation RFC clears
Architecture Review, the repository is documentation and decisions. When you see
`/apps` and `/packages` appear, the first implementation has been sanctioned —
and everything under them will have arrived through the workflow in Chapter 3.
