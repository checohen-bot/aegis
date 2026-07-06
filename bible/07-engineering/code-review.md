# Code Review

*Volume VII — Engineering · Chapter 7*

Code review is where the human judgement of the team meets a change. CI has
already settled everything mechanical — formatting, types, tests, security scans
(Chapter 5) — so review spends its full attention on what machines cannot judge:
whether the change is architecturally sound, domain-correct, and maintainable.
Review is a required merge gate (Chapter 5) and a stage of the lifecycle
(Chapter 3). It is collegial and direct: we review the code, not the coder, and
we do it thoroughly because the alternative is defects in a capital-bearing
system.

## What Every PR Must Contain

A pull request is not just a diff; it is an argument for a change, and it must
make that argument. Using the PR template in `/templates`, every PR states:

- **The governing RFC and/or ADR.** A PR references the RFC it implements and any
  ADR it honours or enacts. A change with no traceable proposal behind it — a
  feature that skipped the lifecycle — is sent back to Research, not reviewed on
  its merits. The reference is how a reviewer checks the code against the
  decision it is meant to implement.
- **The business objective.** In domain language, what user problem this change
  serves and why now. A reviewer who cannot connect the diff to a business need
  cannot judge whether it is the right change.
- **Testing performed.** Which tests were written and run — unit, integration,
  contract, business-rule, regression — and, for critical investment logic, an
  explicit statement of the coverage (Chapter 4). "Tested manually" is not an
  acceptable answer for domain logic.
- **Known limitations.** What this change does *not* do, what edge cases are
  unhandled, what assumptions it rests on. Honesty here is valued, not
  penalised; hidden limitations are the ones that hurt.
- **Future improvements.** Follow-ups deliberately deferred, each linked to
  tracked technical debt where it represents a real trade-off (Chapter 9). This
  keeps deferral explicit rather than silent.

A PR missing these is incomplete and the reviewer's first response is to ask for
them, not to start reading code.

## What Reviewers Focus On

Reviewers assess the change against, in order of priority:

**1. Architectural conformance.** Does the change respect Volume IV — module
boundaries, replaceability, communication only through interfaces and events, no
reaching into another module's internals, no vendor leakage past an adapter, no
unjustified move toward microservices? Does it honour the ADRs it touches? Does
it deliver the mandatory module concerns — typed interfaces, logging, metrics,
tracing, docs, versioning, health checks, config, failure handling? A change
that violates architecture is blocked regardless of how clean the code reads.

**2. Domain correctness.** Does the code do the *right thing* in the language of
Volume III? Are invariants enforced, are business rules faithful to their
specification, is provenance recorded where a Decision or AI artifact is
produced? For Thesis validation, Decision recording, and Capital allocation, at
least one reviewer must be a domain owner, and correctness is scrutinised
against the business rule, not just the test that happens to pass.

**3. Maintainability.** Will the engineer who inherits this in eighteen months
understand it? Is it clear over clever, local over entangled, obvious over
magic? Is there premature optimisation, unnecessary abstraction, or
over-engineering to remove (Chapter 1)? Does it read as the domain, or as the
framework?

Style is explicitly *not* a review topic — CI owns it. A reviewer who finds
themselves commenting on formatting is doing CI's job; a reviewer who approves a
boundary violation because "the code is clean" has missed theirs.

## How We Review

Reviews are timely — a stalled review blocks a teammate and ages a branch, so we
prioritise reviewing over starting new work. Comments distinguish **blocking**
concerns (must change to merge) from **suggestions** (the author decides), so
authors know what is required versus advised. Blocking feedback names the
principle, standard, or ADR it rests on, so it is a shared rule being applied,
not an opinion being imposed — "this reaches into another module's tables,
violating Explicit Boundaries" rather than "I wouldn't do it this way". Authors
respond to every thread and resolve it by change or by discussion; unresolved
threads block merge (Chapter 5).

At least one approving reviewer must be a code owner of every touched module. For
critical investment logic, the review bar is highest and a domain owner's
approval is mandatory; a reviewer cannot waive critical-path coverage — that
requires an ADR.

## The Spirit

Review is not a hurdle; it is how the team's collective knowledge is applied to
every change, and how a new engineer learns what "good" means here faster than
any document teaches. Approve when the change is correct, conformant, and
maintainable — not when it is perfect. Block when it is wrong, and say why with a
reference. Both are acts of care for the same thing: a system people trust with
their capital.
