# ADR-0009: Model-Agnostic AI Architecture — Capabilities over Providers

**Status:** Accepted

## Context

AI is central to Aegis, but the AI model landscape changes rapidly. Coupling the system to a specific LLM provider creates fragility: provider outages, pricing changes, capability shifts, and lock-in all become existential risks. More importantly, the durable asset is not any single model but the **capabilities** Aegis composes — reasoning over evidence, generating explanations, extracting observations, supporting decisions.

The founder's direction is explicit: AI must be model-agnostic and never coupled to a specific LLM provider. It must be built around durable capabilities, not swappable models.

## Decision

Aegis's AI architecture is **model-agnostic**. It is organized around durable **capabilities**, not around any specific provider or model.

Providers and models sit behind capability interfaces. No domain depends on a particular provider's API, prompt format, or model identity. A model or provider can be replaced without changing any domain that consumes a capability.

## Consequences

- Domains depend on capabilities (for example, "explain a thesis" or "extract observations from a filing"), never on a named model or provider SDK.
- Provider selection, routing, and evaluation are concerns of the AI capability layer, isolated from the rest of the system.
- The system can adopt better models as they emerge without domain changes, and can withstand provider disruption.
- AI outputs must remain explainable and auditable regardless of which model produced them, consistent with ADR-0003.
