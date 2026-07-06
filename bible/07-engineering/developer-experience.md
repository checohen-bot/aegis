# Developer Experience

*Volume VII — Engineering · Chapter 6*

Developer experience is not a comfort; it is a correctness strategy. When the
right way is also the easy way, engineers do the right thing by default and the
process defends itself. When the right way is painful, people route around it,
and every workaround is a future defect. This chapter is the standard for
keeping friction low so that quality is cheap.

## Fast Local Setup Via Docker

A new engineer must reach a running, testable system on their first day, with a
single command. We achieve this with Docker: a Compose-defined stack brings up
PostgreSQL, Redis, and the application services using the *same images* CI and
production use (Chapter 5). There is no bespoke local install of a database, no
"works on my machine" divergence, and no undocumented setup lore. The bootstrap
lives in `/scripts` and is itself tested — if setup breaks, that is a
priority-one bug, because it multiplies across every engineer and every new hire.

Concretely, the target is: clone, run the setup script, and have the stack up,
migrations applied, seed data loaded from `/examples`, and the test suite green —
in minutes, not a day. The onboarding runbook in `/docs` walks a first-day
engineer through it. If any step requires tribal knowledge not written down, the
runbook is incomplete and gets fixed.

## Clear Error Messages

An error message is a conversation with a future engineer, often at their most
frustrated. We treat error quality as a feature. A good error, by our standard,
says what failed, why, and what to do next — in domain language where the error
is a domain condition. "Allocation of 12,000 exceeds mission cap of 10,000 for
mission `growth-2026`" is correct; "ValueError: invalid amount" is a defect.
This applies from domain exceptions through API responses to the setup script:
when the stack fails to start, it must say which dependency and how to recover.
Failure handling is a mandatory module concern (Volume IV); legible failures are
part of honouring it.

## Documentation As A DX Feature

Documentation is not overhead paid after the work; it is part of the work
(Chapter 3, Documentation stage) and one of the highest-leverage DX investments
we make. The division of labour is deliberate: `/bible` explains durable
principles and *why*; `/docs` gives fast, practical *how*; `/standards` gives
enforceable specifics; `/examples` shows working patterns to copy. An engineer
with a question should find the answer in one of these before needing another
human — and if they could not, the resolution includes writing it down so the
next person can. Documentation that lies is worse than none, so it changes in the
same PR as the code it describes; CI and review enforce this.

## Minimising Friction In RFC/ADR

The lifecycle in Chapter 3 is strict, but strictness must not mean drudgery, or
engineers will treat process as an obstacle rather than a tool. We reduce the
cost of doing it right: every process document has a template in `/templates`, so
no one starts from a blank page or guesses the required sections. RFCs and ADRs
are lightweight Markdown in the repository, reviewed like code, not a separate
ticketing ceremony. The templates are sized to the decision — a small change
gets a short RFC; the process scales down, not just up. The goal is that writing
the RFC feels like thinking on paper, which it is, rather than filing paperwork.
When the process feels heavier than the decision warrants, that is a bug in the
template, and we fix the template.

## Tooling: The Right Way Is The Easy Way

This is the organising principle of Aegis DX. We invest in tooling so that the
correct action is the path of least resistance:

- **Anything done more than twice becomes a script** in `/scripts` — setup,
  migrations, code generation, scaffolding a new module with its mandatory
  concerns already stubbed (interfaces, tests, logging, metrics, tracing, health
  checks, config).
- **Formatting and linting are automated**, run locally and in CI, so style is
  never a manual burden or a review topic (Chapter 7).
- **New modules are scaffolded, not hand-assembled**, so the mandatory concerns
  of Volume IV are present from the first commit rather than remembered later.
- **CI mirrors local**, so a check that passes locally passes in CI, and
  feedback is trusted (Chapter 5).

The test of good tooling is simple: an engineer who does the fastest available
thing should end up having done the correct thing. Where that is not yet true,
closing the gap is real engineering work, prioritised like any other, not a
nice-to-have. Friction is technical debt against every future engineer (Chapter
9), and we pay it down deliberately.
