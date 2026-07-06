# Domain Events Catalog

Aegis is an event-driven modular monolith. Modules communicate across strict domain boundaries by publishing and subscribing to **domain events** rather than by direct cross-aggregate writes. This catalog defines the key events, what triggers each, the primary data it carries, and which modules consume it. Events are named in the past tense, are immutable, carry the identifiers of the aggregates they concern, and are the sole sanctioned mechanism for cross-aggregate reaction.

## Event Conventions

- **Naming:** `PastTenseFact` (e.g., `ThesisInvalidated`). An event states that something has already happened; consumers may not veto it.
- **Payload:** Minimal — aggregate ID(s), a timestamp, actor, and the few fields consumers need. Consumers re-read source aggregates for detail.
- **Ordering & idempotency:** Consumers must tolerate at-least-once delivery and out-of-order arrival within reason; handlers are idempotent keyed on event ID.
- **Boundaries:** An event is owned by the module of the aggregate that emits it (Thesis events by the Thesis module, and so on).

## Thesis & Case Lifecycle

**ThesisFormed** — Emitted when an Investment Thesis is first created for a Company. Payload: thesis ID, company ID, investor ID. Consumers: the Portfolio/Holding module (to link justification to a Holding), the Learning module (to register a pre-registration baseline), and analytics.

**ThesisUpdated** — Emitted when a Thesis's belief statement or its owned Risks/Catalysts change materially. Consumers: Decision module (rationale may be stale), Behavior Profile (frequency of revision is a discipline signal).

**ThesisInvalidated** — Emitted when a Thesis is judged false — its falsification condition is met, a ThesisBreaking Risk materialized, or supporting Evidence collapsed. Payload: thesis ID, reason, triggering object reference. Consumers: Decision module (prompts an exit/resize review), Learning module (a canonical Learning Event trigger), Holding module (position may no longer be justified), Behavior Profile (was invalidation timely?).

**CaseConstructed / CaseUpdated** — Emitted when an Investment Case supporting or challenging a Thesis is assembled or revised from Evidence. Consumers: Decision module (updated argument strength), analytics.

## Evidence & Observation Flow

**ObservationRecorded** — Emitted when an unevaluated change is noted (manually or by ingestion). Payload: observation ID, subject reference, source. Consumers: the evaluation service (queues it for assessment), Risk monitoring (may match a Risk's watched signals), Catalyst module (may correspond to an anticipated event).

**EvidenceRecorded** — Emitted when an Observation is evaluated and promoted to sourced Evidence, or when Evidence is directly captured. Payload: evidence ID, thesis/company reference, stance (confirming/challenging), source credibility. Consumers: Investment Case module (may strengthen or weaken a Case), Risk module (may substantiate or refute a Risk), Knowledge module (candidate for distillation), Thesis module (may trigger invalidation review if strongly disconfirming).

**KnowledgeCaptured / KnowledgeSuperseded** — Emitted when a Knowledge unit is created from Evidence/Observations, or when a revised unit replaces a prior one. Consumers: Thesis and Case modules (available understanding changed), search/retrieval indexing, analytics.

## Risk & Catalyst

**RiskIdentified** — Emitted when a new failure mode is articulated against a Thesis. Payload: risk ID, thesis ID, category, likelihood, impact. Consumers: monitoring service (subscribes its watched signals), Policy engine (may affect sizing constraints), Behavior Profile (thoroughness of risk enumeration).

**RiskReassessed** — Emitted when a Risk's likelihood or impact changes. Consumers: Decision module (sizing), analytics.

**RiskMaterialized** — Emitted when confirming signals show a Risk has occurred. Payload: risk ID, thesis ID, impact severity. Consumers: Thesis module (if ThesisBreaking, flags invalidation review), Decision module (exit/resize prompt), Learning module (Learning Event trigger).

**CatalystAnticipated** — Emitted when a Catalyst is registered with its pre-registered expected direction and window. Consumers: scheduling/attention service, calibration tracking in Behavior Profile.

**CatalystTriggered** — Emitted when an anticipated event occurs. Payload: catalyst ID, thesis ID, outcome, resulting observation ID. Consumers: Observation module (an Observation is created), Decision module (may warrant action), Learning module (enables expectation-vs-outcome comparison), Behavior Profile (calibration data point).

**CatalystLapsed** — Emitted when a Catalyst's window closes without occurrence. Consumers: calibration tracking, cleanup.

## Decision & Governance

**DecisionMade** — Emitted when a buy/sell/hold/resize Decision is committed with its reasoning. Payload: decision ID, holding/portfolio ID, action, cited theses/cases. Consumers: Holding/Portfolio module (position state changes), Policy engine (records final adherence outcome), Behavior Profile (a core behavioral data point), Learning module (registers the decision's expectation for later comparison).

**HoldingResized / HoldingOpened / HoldingClosed** — Emitted by the Portfolio module when a Decision changes a position. Consumers: analytics, Policy engine (concentration/rebalancing re-check), Behavior Profile.

**PolicyEvaluated** — Emitted for every Policy check against a Decision, recording permit/warn/override/block. Consumers: audit log, Behavior Profile (discipline metrics).

**PolicyBreached** — Emitted when a Decision violates an Active Policy (soft override or attempted hard block). Payload: policy ID, decision ID, enforcement level, override justification if any. Consumers: Behavior Profile (a discipline signal that may recompute traits), Learning module (recurring breaches may prompt a Learning Event), notification service.

**PolicyActivated / PolicyRetired** — Emitted on Policy lifecycle transitions. Consumers: Decision module (guardrail set changed), audit.

## Mission & Learning

**MissionActivated / MissionSuspended / MissionRetired** — Emitted on Capital Mission lifecycle transitions. Consumers: Policy engine (revalidate governed Policies), Portfolio module (allocation permission), analytics.

**LearningCaptured** — Emitted when a Learning Event records an expectation-vs-outcome comparison and attribution. Payload: learning event ID, trigger reference, attribution. Consumers: Knowledge module (may create/supersede Knowledge), Behavior Profile (recompute traits/calibration), Policy engine (a ProcessGap or BehavioralError may propose a new guardrail).

**BehaviorProfileRecomputed** — Emitted when the derived Behavior Profile is regenerated. Payload: investor ID, version, changed traits. Consumers: Policy engine (personalization), UI (surfacing tendencies), notification service.

## Why This Matters

These events keep modules decoupled: the Thesis module need not know the Learning module exists — it emits `ThesisInvalidated`, and any module that cares subscribes. This preserves strict domain boundaries, makes the system's behavior auditable as an event log, and lets future capital-allocation domains plug in as new publishers/subscribers without reworking existing modules.
