# ADR-0002: Customer Segment is Individual Investors

**Status:** Accepted

## Context

Every product decision — surface, depth, tone, workflow, integrations, pricing — depends on who the customer is. The company must fix its primary customer before designing for them, so that scope, language, and trust standards are anchored to a real person rather than an abstract market.

The founder has chosen individual investors as the customer. This is distinct from institutional asset managers, financial advisors, or funds. The individual investor typically lacks the institutional infrastructure — research staff, decision processes, institutional memory — that professional allocators rely on. Aegis exists to give the individual investor that infrastructure.

## Decision

The customer of Aegis is the **individual investor**.

All product, domain, and interface decisions are made for the individual investor first. Other segments are out of scope unless and until introduced by a future ADR.

## Consequences

- Product design optimizes for a single, self-directed decision-maker rather than teams, approval chains, or fiduciary reporting obligations.
- Language, explanations, and onboarding assume an intelligent non-professional, not a finance specialist.
- Trust, explainability, and auditability are designed to serve the individual's own confidence and record-keeping, not third-party compliance.
- Features that serve only institutional workflows are deferred, and their absence in V1 is intentional.
