# Provider Abstraction: The Capability Gateway

## Purpose

This chapter specifies the concrete seam that makes the frozen principle enforceable: the **Capability Gateway**. The Gateway is the sole boundary through which any part of Aegis reaches a large language model. No domain module, no application service, and no API handler imports a provider SDK, holds a provider API key, or constructs a provider-shaped request. They call capabilities; the Gateway resolves capabilities to providers. Everything vendor-specific lives on the far side of this boundary in swappable **provider adapters**.

## Layered Structure

```
Domain / Application code
        │  depends only on ↓
   Capability interfaces          (stable, typed, provider-free)
        │  resolved by ↓
   Capability Gateway             (registry, routing, policy, telemetry)
        │  dispatches to ↓
   Provider Adapter               (translates contract ⇄ one vendor API)
        │  calls ↓
   Vendor SDK                     (Anthropic / OpenAI / Gemini / local)
```

The rule is directional: dependencies point inward toward the stable interface. A provider SDK is a leaf; nothing above the adapter layer may know it exists. This is a Modular Monolith enforcing an internal boundary the way it would enforce a network boundary — by contract and by dependency direction, not by process separation.

## Defining a Capability

A capability is declared as an abstract interface plus its contract types. In Python this is a `Protocol` (structural, so adapters need no inheritance coupling) over Pydantic contract models:

```python
class AssessThesisContradiction(Protocol):
    name: ClassVar[str] = "assess.thesis_contradiction"
    version: ClassVar[str] = "1.2.0"

    def invoke(self, request: ContradictionRequest) -> ContradictionAssessment: ...
```

`ContradictionRequest` and `ContradictionAssessment` are composed from canonical domain projections — an `InvestmentThesis` snapshot, an `Observation`, referenced `Evidence` ids. They contain no `model`, `temperature`, `messages`, or `tokens` field. The contract is the whole of what a caller sees.

## Registering a Provider Adapter

A provider adapter implements the capability's behavior for exactly one vendor. It is the *only* place that imports a vendor SDK and the *only* place that reads model configuration:

```python
class AnthropicContradictionAdapter:
    name = "assess.thesis_contradiction"
    version = "1.2.0"
    provider = "anthropic"

    def invoke(self, request: ContradictionRequest) -> ContradictionAssessment:
        rendered = self._prompts.render("assess.thesis_contradiction", "1.2.0", request)
        raw = self._client.complete(rendered, schema=ContradictionAssessment.schema())
        return ContradictionAssessment.model_validate(raw)   # contract-validated
```

Adapters are registered into the Gateway at composition root, never discovered implicitly:

```python
gateway.register(
    capability="assess.thesis_contradiction",
    version="1.2.0",
    adapter=AnthropicContradictionAdapter(client, prompt_library),
    routing=RoutingPolicy(primary="anthropic", fallback="openai"),
)
```

The prompt text an adapter renders is pulled from the versioned Prompt Library (see `prompt-strategy.md`), not embedded as a string literal — so even the vendor-specific phrasing is externalized and testable.

## Invocation

Callers resolve and invoke through the Gateway by capability name and contract, never by provider:

```python
assessment = gateway.invoke(
    "assess.thesis_contradiction",
    ContradictionRequest(thesis=thesis, observation=obs, evidence=ev_refs),
)
```

The Gateway performs, in order: contract validation of the request; resolution of the active adapter per the routing policy and per-tenant configuration; emission of an OpenTelemetry span (`ai.capability.invoke`) tagged with capability name, contract version, resolved provider, model id, token counts, latency, and cost; the adapter call; contract validation of the response; and guardrail post-checks (grounding, source presence — see `evaluation-and-guardrails.md`). A response that fails validation or grounding never reaches the caller; it raises or triggers fallback.

## Cross-Cutting Concerns Live in the Gateway

Because every AI call funnels through one seam, all operational policy is implemented once, provider-agnostically: routing and fallback between adapters, retries and timeouts, circuit breaking on provider outage, rate limiting and budget enforcement, response caching keyed by capability + contract-hash, redaction of PII before egress, and full telemetry. None of this is duplicated per provider or per feature. Adding a provider adds an adapter; it does not touch cross-cutting logic.

## The Swap Test, Demonstrated

Suppose Aegis replaces Anthropic with a different vendor for `assess.thesis_contradiction`. The complete change set:

1. Author `NewVendorContradictionAdapter` implementing the same contract.
2. Register it and update `RoutingPolicy(primary="newvendor")` at the composition root.
3. Add the vendor's rendering of the capability prompt as a new file under `/prompts` (same capability, same contract version).

What is **not** touched: the `AssessThesisContradiction` interface, the request/response contracts, the cognitive pipeline that calls it, every domain object, every application service, every test that asserts the contract, the UI, the API. The evaluation harness re-runs against the new adapter and gates the switch on quality parity. This is the frozen principle expressed as a diff: bounded entirely to adapter registration and prompt artifacts.

## Prohibited Couplings

The following are architectural violations, caught in code review and by an import-linter boundary rule:

- Any import of a vendor SDK outside `ai/adapters/<provider>/`.
- Any provider-specific field (`model`, `temperature`, `system`, `messages`) in a capability contract.
- Any `if provider == "..."` branch in domain or application code.
- Any consumer reading a provider's raw text response instead of the validated output contract.
- Any capability whose output type is or contains a `Decision`.

The Gateway is not a convenience layer; it is the mechanism that keeps the platform permanently model-agnostic. Everything above it reasons in capabilities. Only the adapters below it know a model's name — and they are designed to be thrown away and rewritten without the rest of the system noticing.
