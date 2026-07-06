# Policy

## Definition

A Policy is an explicit, machine-evaluable rule or guardrail that constrains or guides how capital is allocated and how Decisions are made, derived from a Capital Mission and optionally sharpened by the investor's Behavior Profile. Policies encode the pre-commitments an investor makes to their future self — position-size ceilings, concentration limits, mandatory cooling-off periods before selling, required thesis review before adding, exclusion lists, rebalancing bands. A Policy is normative and enforceable: at Decision time the system evaluates the relevant Policies and either permits, warns, or blocks, and every evaluation is recorded.

## Why It Exists

Adaptive Quality Investing holds that decision quality is protected less by in-the-moment willpower than by rules set in advance, when the investor is calm and rational, and honored when they are not. Policy exists to (1) translate the abstract intent of a Capital Mission into concrete, checkable constraints, (2) counter the specific failure modes identified in the Behavior Profile with targeted guardrails, (3) make discipline measurable by recording adherence and breaches, and (4) provide a consistent, auditable governance layer over all Decisions across present and future capital-allocation domains.

## Key Attributes

- `id` (identifier): Globally unique, immutable identifier.
- `mission_ref` (reference): The Capital Mission this Policy serves.
- `name` (string): Human-readable label.
- `rule_type` (enum): `ConcentrationLimit`, `PositionSizeLimit`, `Exclusion`, `CoolingOff`, `ReviewGate`, `RebalancingBand`, `LiquidityFloor`.
- `predicate` (structured expression): The evaluable condition, expressed against Portfolio/Holding/Decision state.
- `enforcement_level` (enum): `Advisory`, `SoftBlock`, `HardBlock` — whether a violation warns, requires override with justification, or is prohibited.
- `scope` (structured): What the Policy applies to — the whole Portfolio, a sector, a single Holding, or a Decision type.
- `origin` (enum): `MissionDerived`, `BehaviorDerived`, `UserAuthored` — provenance for explainability.
- `status` (enum): `Draft`, `Active`, `Suspended`, `Retired`.
- `created_at`, `activated_at`, `updated_at` (timestamp).

## Invariants

- A Policy MUST reference exactly one Capital Mission and MUST NOT contradict that Mission's constraints.
- A Policy's `predicate` MUST be deterministically evaluable against Portfolio, Holding, and Decision state — no ambiguous or purely subjective rules.
- A `HardBlock` Policy, when violated, MUST prevent the Decision from being committed; a `SoftBlock` MUST require and record an explicit override justification.
- Every Policy evaluation against a Decision MUST be recorded (permit, warn, override, or block), producing an auditable adherence trail.
- Policies MUST NOT be retroactively applied to already-committed Decisions; they govern Decisions made while `Active`.

## Relationships

- Derived from and governed by **Capital Mission** (`mission_ref`), many Policies to one Mission.
- Evaluated against **Decision**, **Portfolio**, and **Holding** state at decision time.
- May be authored or strengthened in response to **Behavior Profile** traits (`origin = BehaviorDerived`).
- Breaches and adherence feed back into the **Behavior Profile**'s discipline metrics.
- A recurring breach pattern surfaced by a **Learning Event** is a common trigger for creating or tightening a Policy.

## Lifecycle / State

`Draft` while authored and validated against its Mission. `Draft → Active` once validated and non-contradictory. `Active → Suspended` temporarily disables enforcement (recorded, e.g., during an intentional strategy shift). `Suspended → Active` re-enables it. `Active`/`Suspended → Retired` permanently ends the Policy; retirement is recorded and the Policy remains queryable for the audit history of past Decisions it governed. Historical evaluations are immutable regardless of later status changes.

## Aggregate Boundary

Policy is an **aggregate root**. It owns its `predicate`, `enforcement_level`, `scope`, and `status`, which must be mutated atomically to keep enforcement coherent. It references but does not own the Capital Mission it derives from, nor the Portfolio/Holding/Decision state it evaluates — evaluation is a read against those aggregates, and the resulting adherence record is emitted as a domain event (`PolicyEvaluated` / `PolicyBreached`) rather than written into them. This isolation lets the governance layer evolve independently of the assets it governs.
