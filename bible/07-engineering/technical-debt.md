# Technical Debt

*Volume VII — Engineering · Chapter 9*

Technical debt is not a moral failing; it is a financial instrument. Like
financial debt, it can be a sound, deliberate choice that buys speed now against
a repayment later — and like financial debt, it destroys you when it is taken on
silently, forgotten, and left to compound. Aegis, a platform that advises
investors on exactly this trade-off, holds itself to the discipline it teaches:
debt is taken on consciously, recorded, priced, and paid down on a plan. This
chapter defines how.

## The Governing Principle

**Speed is never traded for long-term quality without an explicit, documented
decision.** This is the non-negotiable rule of this volume. There is nothing
wrong with shipping a deliberately simpler solution to meet a real need faster —
that is often the right call. There is everything wrong with doing so silently,
so that the shortcut is invisible to the next engineer, absent from any plan, and
discovered only as a mysterious source of pain. The difference between a
sound shortcut and rot is a single artifact: a written record that this debt
exists, why it was taken, and how it will be repaid.

## What Counts As Technical Debt

We name debt broadly and honestly. It includes: a deliberately simplified
implementation that will need to grow; a missing abstraction we chose to defer
until a second use case appeared; incomplete test coverage outside the critical
paths (coverage of Thesis validation, Decision recording, and Capital allocation
is never debt — it is a hard requirement, Chapter 4); a known performance
limitation we have measured and accepted for now; a workaround around a vendor or
library constraint; friction in tooling or setup that taxes every engineer
(Chapter 6); and documentation that has fallen behind code. If it is a gap
between what exists and what our principles (Chapter 1) call for, it is debt, and
it is named as debt — not excused as "just how it is".

## How Debt Is Tracked

Debt is never carried only in someone's head. It is recorded where it is
incurred and where it can be found:

- **At the point of decision.** When a shortcut is chosen during Implementation
  Planning or Implementation (Chapter 3), it is written into the plan and, in the
  PR, into the "known limitations" and "future improvements" sections that every
  PR requires (Chapter 7). The reviewer sees the trade-off and consents to it, or
  does not.
- **As a tracked item.** Each material piece of debt becomes a tracked issue with
  a consistent label, describing the shortcut, the reason, the cost of leaving it,
  and the intended repayment. This is the debt register — the single place the
  team can see what it owes.
- **As an ADR, when the debt is architectural.** A deliberate deviation from a
  stated principle or architectural constraint is not merely an issue; it is an
  ADR (Chapter 3), because it is a consequential decision the whole system must
  understand. The ADR makes the override visible and permanent in the record.

Debt that is written down loses its power to surprise. That is the entire point
of tracking it.

## How Debt Is Prioritised

Not all debt is worth repaying, and pretending otherwise is its own waste. We
price each item by two questions: **what does it cost us to carry** (how often it
slows work, how much risk it adds, whether it blocks a coming feature) and **what
does it cost to repay**. High-carry, low-repay debt is paid down first. Debt that
touches critical investment logic, security, or correctness is prioritised above
convenience debt regardless of repayment cost, because the carrying risk is
borne by users' capital. Debt that costs little to carry and much to repay may be
deliberately *kept* — and that too is a documented decision, so that "we are
choosing to live with this" is a recorded position, not an accident of neglect.

## How Debt Is Paid Down

Repayment is planned work, not heroics between features. We repay debt through
the same lifecycle as any change (Chapter 3): a prioritised item becomes a
Business Need in its own right, sized and scheduled, not squeezed guiltily into
the margins of unrelated PRs. Two rules keep the register from growing without
bound. First, the **Boy Scout rule**: leave touched code cleaner than you found
it, repaying small, local debt opportunistically as you pass through — but never
smuggling large, risky refactors into an unrelated change, which defeats review.
Second, **deliberate paydown capacity**: repaying debt is treated as
first-class engineering work that competes for time openly against features,
because a team that never schedules repayment has simply decided, silently, to
let quality decay — the exact failure this chapter forbids.

## The Standard We Hold

The measure of our discipline is not that Aegis has no technical debt — every
living system does. It is that a new engineer can open the debt register and the
ADR log and see, completely and honestly, every place we have knowingly fallen
short of our principles, why, and what we intend to do about it. Debt we can see
is debt we can manage. Debt we hide is the debt that eventually owns us — and on
a platform entrusted with people's capital, that is a price we do not pay.
