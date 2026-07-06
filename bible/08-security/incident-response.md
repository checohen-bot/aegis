# Incident Response

## Principle

Incidents are inevitable; being unprepared is a choice. Aegis maintains a lightweight but real incident-response framework appropriate to the company's current stage — enough structure to respond quickly and consistently to events affecting availability, data integrity, or the security of investor financial data, without bureaucracy that slows the response. Our culture is blameless and root-cause focused: every incident is a Learning Event, directly analogous to the learning loop in our own investment methodology.

## What Is an Incident

An incident is any unplanned event that degrades or threatens: the confidentiality of financial or personal data, the integrity of Thesis/Decision/audit data, the availability of critical workflows (Thesis evaluation, Decision recording, IBKR sync), or the trustworthiness of what the platform shows investors. Security incidents (potential exposure of financial data, credential compromise, audit-integrity anomalies) are always incidents regardless of user-visible impact.

## Severity Classification

Severity is driven by impact to investor financial data and trust, not by internal inconvenience.

- **SEV-1 — Critical.** Actual or suspected exposure, corruption, or loss of investor financial or reasoning data; brokerage credential/token compromise; audit-log tampering; or a full outage of a critical workflow. Immediate response, day or night. Highest priority in the company.
- **SEV-2 — Major.** Significant degradation of a critical path (e.g. IBKR sync broadly failing, Decision recording erroring for many users), AI provider outage materially degrading capabilities, or a security weakness with plausible near-term exploitation. Rapid response during and outside business hours as warranted.
- **SEV-3 — Minor.** Localized or degraded-but-safe conditions with clear, honest fallback (e.g. a single provider down while gracefully degraded per `reliability.md`), non-sensitive bugs, or low-risk security findings. Handled in normal working hours.

When severity is ambiguous, we round up. Under-classifying a data-exposure event is a far worse error than over-classifying a minor bug.

## On-Call and Response Expectations (Current Stage)

At the company's current size, on-call is a shared, explicit responsibility rather than a large rotation:

- A designated responder is reachable for SEV-1/SEV-2 at all times, with a documented escalation path to the founder and to whoever owns security.
- Alerts (see `observability.md`) route to the on-call responder with severity, a runbook link, and a dashboard. Security-class alerts additionally route to the security owner.
- **First actions are standardized:** acknowledge, assess severity, and for SEV-1 open a coordination channel and assign a single incident lead. The lead coordinates; they do not have to personally fix everything.
- **Contain first, then fix.** For security incidents, containment (revoke/rotate the affected credential, isolate the affected component, cut off an abused provider key) precedes root-cause work. Rotation runbooks (see `secrets-management.md`) exist precisely so containment is mechanical under pressure.
- **Protect the evidence.** Preserve logs, traces, and audit records needed to understand the incident before making changes that could destroy them. The immutable audit trail is a primary investigative asset.
- **Investor data integrity is the top priority** during any response: no remediation step may risk corrupting or losing Thesis/Decision data to restore availability faster.

## Postmortem Culture

Every SEV-1 and SEV-2 gets a written postmortem; SEV-3s get one when there is something to learn.

- **Blameless.** Postmortems examine systems, defaults, and processes — never individuals. People act reasonably given the information and tools they had; if a person could cause the incident, the system allowed it, and the system is what we fix. Fear of blame hides the truth we need.
- **Root-cause focused.** We drive past the proximate trigger to the underlying cause and the reasons it went undetected. We ask why the safeguards (secure-by-default, tests, alerts) did not prevent or catch it.
- **Concrete follow-through.** Each postmortem produces owned, tracked action items — often hardening a default so the same class of failure becomes structurally impossible (see `secure-by-default.md`).
- **A Learning Event.** Postmortems feed our institutional learning loop exactly as realized-vs-intended analysis feeds investment learning. An incident that produces no durable improvement was a cost with no return; we do not waste it.

## Disclosure Principles

For incidents affecting user financial or personal data, we disclose honestly and promptly.

- **Truthful and timely.** Affected investors are informed about incidents materially affecting their financial or personal data, with what happened, what data was involved, what we did, and what they should do. We do not minimize, delay for convenience, or obscure.
- **Trust over optics.** Aegis's entire value rests on investor trust. We would rather deliver uncomfortable news accurately than protect our image. Silence about a data incident is a violation of the trust the platform exists to earn.
- **Regulatory and contractual obligations** for breach notification are met within required timeframes; where uncertain, we err toward disclosure.
- **Coordinated security disclosure.** External security researchers have a clear, good-faith reporting channel; we acknowledge reports, remediate responsibly, and do not retaliate against good-faith disclosure.

## Enforcement and Readiness

- Runbooks for the most likely incidents (credential compromise, IBKR-down, provider-down, database issues) are written, rotation is rehearsed, and backups/restores are tested (see `reliability.md`).
- Severity definitions, escalation contacts, and the incident lead role are documented where responders can find them under stress.
- Postmortem action items are tracked to completion and reviewed; unfinished hardening is itself a reliability risk.

## Rationale

The measure of Aegis is not that incidents never happen — it is that when they do, we respond fast, protect investor data first, tell the truth, and become structurally harder to break the next time.
