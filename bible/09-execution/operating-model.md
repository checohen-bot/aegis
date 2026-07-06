# Operating Model

*Volume IX — Execution Playbook · Chapter 1*

This chapter describes how Aegis actually operates day to day at its current stage: a founder-led company establishing an engineering foundation before writing business code. It is deliberately concrete. It says who decides what, how work is chosen, and how the mission arbitrates when priorities compete. It is not an org chart aspiration; it is the working contract that keeps a small team fast without becoming incoherent.

## Two Roles, One Authority Split

At this stage the company has two operating roles. The split of authority between them is fixed and is restated here so it can be enforced, not merely remembered.

**The founder owns direction.** The founder is the sole authority over vision, product, philosophy, terminology, and architecture *direction*. Concretely, the founder decides what Aegis is for, what Adaptive Quality Investing means in practice, what the canonical domain objects are and what they are named (Portfolio, Holding, Company, Investment Thesis, Investment Case, Evidence, Observation, Knowledge, Decision, Capital Mission, Risk, Catalyst, Learning Event, Behavior Profile, Policy), what the product must feel like, and which direction the architecture must move to serve that intent. When a question is "what should this mean, and is it right for the mission," it is the founder's to answer.

**Engineering owns realization.** Engineering is the sole authority over implementation, testing, repository structure, infrastructure, CI/CD, and documentation of *how* the system is built. Concretely, engineering decides how a domain object is persisted, how modules are wired, which libraries are used, how tests are structured, how the pipeline gates merges, and how the code is documented. When a question is "how do we build this well, safely, and maintainably," it is engineering's to answer.

The boundary is meaning versus mechanism. The founder defines the *what* and the *why*; engineering defines the *how*. Neither silently crosses the line. If engineering believes a directional choice is wrong, it raises it explicitly — it does not re-decide it in code. If the founder wants an implementation changed, the request is framed as intent ("Decisions must be explainable to a non-expert") not as instruction to use a specific mechanism.

## How Decisions Get Made

Decisions are made in one of three registers, matched to their weight:

1. **Directional decisions** (what a domain object is, what the product does, what a principle requires) are made by the founder and recorded where they belong: in the Bible for durable philosophy and domain definition, and in an ADR when they constrain architecture. A directional decision that changes an existing Bible statement is made by amending the Bible.

2. **Structural decisions** (module boundaries, technology choices, data models, cross-cutting mechanisms) are made by engineering through an **ADR**. An ADR names the decision, its context, the options weighed, and the consequences. Once an ADR is accepted it is binding until superseded by another ADR. A structural decision that must override an architectural principle (Volume IV) is *only* valid as a written, visible ADR — silent override is a defect.

3. **Local decisions** (naming a variable, choosing a test layout inside an agreed structure) are made inline by whoever is doing the work, governed by the standards already written down. These need no ceremony; the standards are the decision.

The escalation rule is simple: if a choice changes what something *means* or what the product *is*, it is the founder's; if it changes how something is *built*, it is engineering's; if it is already covered by an accepted ADR or a written standard, it is nobody's to relitigate without superseding that record.

## How Work Gets Prioritized Against the Mission

Work is not prioritized by feature demand, backlog age, or effort. It is prioritized by proximity to the mission's current objective. At this stage that objective is explicit: **prove the architecture is buildable via a walking skeleton before broadening scope.** Therefore Phase 0 foundation work (this Bible, the ADR baseline, standards, CI/CD) outranks all speculative feature work, and Phase 1 skeleton work outranks all Phase 2 breadth.

The prioritization test applied to any candidate piece of work is a short sequence of questions:

- **Does it serve the current phase's goal?** If the current goal is the walking skeleton, work that does not advance one canonical object end-to-end waits.
- **Does it raise the floor or the ceiling?** Foundation work that raises the floor (makes everything after it safer and cheaper) is preferred over work that raises the ceiling (adds a capability) while the floor is still being poured.
- **Is it reversible cheaply?** Reversible work can proceed on engineering judgment; irreversible or precedent-setting work (a schema convention, a boundary rule) is elevated to an ADR first.
- **Does it compound?** Aegis is a decision-quality and knowledge-compounding product; internally we apply the same lens. Work that makes future understanding cheaper — clearer boundaries, better provenance, reusable patterns — is favored over one-off throughput.

## The Cadence

The operating rhythm is deliberately lightweight while the team is small. Direction is set and revisited by the founder as the mission clarifies. Engineering pulls the highest-mission-value item that is *ready* (unblocked, specified enough to build well) and moves it through the feature lifecycle (Chapter 2). Nothing merges without passing the Definition of Done (Chapter 5). Progress is measured against the checkable milestones (Chapter 4), never against velocity or commit count.

The point of this model is that a two-role company can move at the speed of one mind while retaining the discipline of an institution: the founder holds coherence of meaning, engineering holds coherence of construction, and the mission — not preference, urgency, or volume — decides what happens next.
