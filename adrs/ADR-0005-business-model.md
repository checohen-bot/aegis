# ADR-0005: Hybrid Business Model

**Status:** Accepted

## Context

The company must choose how it captures value in a way that aligns with its philosophy. Pure transaction-based models can incentivize activity over quality. Pure subscription models must continuously justify recurring value. The founder wants a model that aligns the company's incentives with the customer's decision quality and long-term trust, rather than with trading volume.

## Decision

Aegis adopts a **hybrid business model**.

The specific composition of the hybrid is a product and commercial matter owned by the founder and refined over time. The architecture and domain model must not assume a single monetization mechanism, and must accommodate a combination of models without rework to core domains.

## Consequences

- Systems that touch monetization (entitlements, access, usage) are designed to support multiple, coexisting models rather than one.
- No core domain encodes an assumption that revenue comes from a single source such as trading activity.
- Incentive alignment is a design constraint: the business model must never reward behavior that degrades decision quality.
- The precise commercial structure may evolve without requiring changes to the canonical domain model.
