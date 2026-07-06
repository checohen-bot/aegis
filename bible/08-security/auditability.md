# Auditability

## Principle

Every Decision, every Thesis change, and every AI-assisted recommendation in Aegis must be traceable: *who or what* produced it, *what Evidence* it relied on, *when* it happened, and *why*. This is a frozen founder directive. Auditability is not a compliance afterthought — it is the mechanism by which an investor can trust, review, and learn from their own decision history. If a piece of financial reasoning cannot be reconstructed after the fact, it does not meet the bar for this platform.

## What Must Be Auditable

The audit trail covers the full lifecycle of investment reasoning:

- **Decisions.** Every recorded Decision (buy, sell, hold, size change, or an explicit decision not to act) captures the actor, timestamp, the Thesis state it was made under, the Evidence considered, and the reasoning recorded.
- **Thesis changes.** Theses are versioned. Every change records what changed, who or what changed it, when, and the prior state. The full evolution of a Thesis is reconstructable — investors can see how and why their conviction changed over time.
- **AI-assisted recommendations.** Every AI capability output that informs reasoning records: which capability was invoked, which model/provider served it (via the Capability Gateway), the exact input scope provided, the output returned, and the timestamp. An AI recommendation is never anonymous — it is always attributable to a specific capability call.
- **Evidence linkage.** Decisions and Theses link to the specific Evidence artifacts they relied on, captured as they existed at that moment, so a later change to source data does not silently rewrite the historical basis of a past Decision.

## Attribution: Who or What

Every audit record names its actor unambiguously:

- **Human actors** are identified by authenticated user identity.
- **AI actors** are identified by capability, model, provider, and version — not merely "the AI." When a recommendation is machine-generated, the record makes that explicit and distinguishes AI-suggested from human-decided. An investor must always be able to tell what a machine proposed versus what they themselves chose.
- **System actors** (scheduled syncs, background jobs) are identified by the process and version that acted.

This distinction is essential: the value of Aegis rests on an investor being able to separate their own judgment from machine assistance when they review history.

## Evidence Provenance

Auditability requires that the *inputs* to reasoning are preserved, not just the outputs.

- Evidence referenced by a Decision or Thesis is captured or content-addressed so the exact version relied upon is recoverable.
- For AI-assisted steps, the specific, minimized input scope sent to the provider is recorded (consistent with `data-protection.md` — only what was strictly needed for that call), so the basis of the recommendation is reviewable without depending on the external provider retaining anything.
- Where source data later changes, the historical record retains the value as-of the decision time. History is append-only; it is never retroactively "corrected" in place.

## Immutable Audit Log Philosophy

Financial-reasoning audit data is append-only and tamper-evident.

- **Append-only.** Audit records are written once and never updated or deleted through application paths. Corrections are new records that reference and supersede prior ones; the original remains visible. There is no application code path that mutates a historical Decision or Thesis version in place.
- **Tamper-evidence.** Audit records carry integrity protection — sequential ordering and cryptographic chaining/hashing where appropriate — so that any attempt to alter or remove history is detectable. The goal is not merely to record history but to make silent revision impossible.
- **Separation of duties.** The ability to access user financial data and the ability to alter audit storage are held by different roles (see `authn-authz.md`). No single actor can both act on an account and erase the evidence of having done so.
- **Retention.** Audit records for financial reasoning are retained per the retention policy in `data-protection.md`, and outlive transient operational data. Deletion of audit history, where legally required (e.g. a user's right to erasure), is itself a logged, authorized, and audited event.

## User-Facing Auditability

Auditability is not only for engineers and regulators — it is a product surface for the investor.

- Investors can review their own decision history: what they decided, when, under which Thesis, on what Evidence, and where AI assisted.
- The trail is presented honestly: AI contributions are labeled as such, and gaps or partial data are surfaced, never smoothed over (see `reliability.md`).
- This directly mirrors Aegis's investment methodology: a reviewable history is what enables genuine learning from past Decisions.

## Feeding the Learning Loop

The audit trail is the substrate for the platform's own Learning Events. Because every Decision and its outcome are traceable, the system — and the investor — can compare intended reasoning against realized results and extract lessons. Auditability and learning are the same infrastructure viewed from two angles.

## Enforcement

- Writes to Decisions, Theses, and AI recommendation records go through audited, append-only paths; direct mutation is not exposed.
- CI and code review reject changes that would allow in-place edits or deletion of historical reasoning records.
- Audit completeness (actor, timestamp, evidence, provenance present) is validated at write time; an incomplete audit record is a hard failure, not a warning.

## Rationale

An investor's trust in Aegis is only as strong as their ability to look back and understand exactly how each Decision came to be. Immutable, attributable, evidence-linked history is what turns a black box into an accountable partner.
