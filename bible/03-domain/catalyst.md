# Catalyst

## Definition

A Catalyst is a specific, anticipated future event or condition expected to change the value, understanding, or standing of an Investment Thesis when it occurs — an earnings release, a product launch, a regulatory ruling, a debt maturity, a management transition, or the crossing of a defined operating threshold. A Catalyst is defined *before* it happens: it is a watch item with an expected window and an expected directional consequence. When the anticipated event occurs, the Catalyst *triggers*, converting expectation into an Observation and, upon evaluation, into Evidence.

## Why It Exists

Quality decisions require knowing not only what is believed but what would move the belief and when. Investors otherwise react to events unsystematically and with hindsight bias. A first-class Catalyst object lets the investor pre-register expectations, distinguish thesis-confirming from thesis-challenging outcomes in advance, schedule attention, and measure calibration (did the anticipated event happen, and did it move things the predicted way). Catalysts also power the monitoring of Risks and the timing dimension of Decisions, and they generate the honest before-versus-after comparisons that Learning Events depend on.

## Key Attributes

- `id` (identifier): Globally unique, immutable identifier.
- `thesis_ref` (reference): The Investment Thesis whose outlook the Catalyst bears on.
- `description` (text): The anticipated event or condition.
- `catalyst_type` (enum): `Scheduled`, `Conditional`, `OpenEnded` — whether it has a known date, a triggering condition, or an indefinite window.
- `expected_window` (date range, nullable): When the event is expected; null for purely conditional catalysts.
- `expected_direction` (enum): `Confirming`, `Challenging`, `Ambiguous` — the pre-registered expected effect on the Thesis.
- `linked_risk_ref` (reference, nullable): A Risk this Catalyst helps monitor.
- `outcome` (text, nullable): The realized result, populated on trigger.
- `resulting_observation_ref` (reference, nullable): The Observation created when the Catalyst triggered.
- `status` (enum): `Anticipated`, `Triggered`, `Evaluated`, `Lapsed`, `Cancelled`.
- `created_at`, `triggered_at`, `evaluated_at` (timestamp).

## Invariants

- A Catalyst MUST reference exactly one Investment Thesis.
- A `Scheduled` Catalyst MUST have an `expected_window`.
- `expected_direction` MUST be recorded at creation and MUST NOT be edited after trigger — calibration integrity depends on the pre-registration being immutable.
- On transition to `Triggered`, a Catalyst MUST produce a `resulting_observation_ref`; the raw event enters the system as an Observation, not directly as evaluated Evidence.
- A Catalyst whose `expected_window` passes without occurrence transitions to `Lapsed`, not `Cancelled`.

## Relationships

- Anticipated against an **Investment Thesis** (`thesis_ref`).
- May monitor a **Risk** (`linked_risk_ref`).
- On trigger, produces an **Observation**, which upon evaluation yields **Evidence** feeding the **Investment Case**.
- Triggered Catalysts frequently prompt a **Decision** and, through prediction-versus-outcome comparison, a **Learning Event**.

## Lifecycle / State

`Anticipated` on creation. `Anticipated → Triggered` when the event occurs (emits `CatalystTriggered`, creates an Observation). `Triggered → Evaluated` once the Observation is assessed and its effect on the Thesis recorded, enabling calibration scoring. `Anticipated → Lapsed` if the expected window closes with no event. `Anticipated → Cancelled` if the catalyst becomes irrelevant (e.g., Thesis closed) before triggering. `Triggered`, `Evaluated`, `Lapsed`, and `Cancelled` are terminal for that Catalyst instance.

## Aggregate Boundary

Catalyst is **not an aggregate root**; it is an entity within the **Investment Thesis** aggregate. Its pre-registered `expected_direction` and its status must remain consistent with the Thesis and are mutated within that boundary. It creates and references Observation aggregates (separately rooted) via domain events rather than owning them, preserving the separation between raw signal capture and thesis-bound expectation.
