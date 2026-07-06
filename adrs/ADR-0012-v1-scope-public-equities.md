# ADR-0012: V1 Scope Limited to Long-Term Public Equities, with Extensible Architecture

**Status:** Accepted

## Context

Aegis's long-term ambition spans multiple capital allocation domains: public equities, private equity, venture capital, real estate, corporate capital allocation, and strategic procurement. Attempting all of them at once would produce a shallow, unfocused product. At the same time, an architecture built narrowly for one domain would require painful rewrites to expand.

The founder resolves this by scoping V1 tightly while requiring the architecture to preserve extensibility. Long-term public equity investing is the beachhead: it is well-defined, data-rich, and squarely aligned with the individual investor customer.

## Decision

V1 scope is **long-term public equity investing only**.

The architecture and canonical domain model must be designed so that the following domains can be added later without a rewrite: Private Equity, Venture Capital, Real Estate, Corporate Capital Allocation, and Strategic Procurement. These domains are **not** implemented in V1.

## Consequences

- V1 features, data, and integrations target long-term public equities exclusively.
- Domain modeling avoids assumptions that would prevent generalization to other capital allocation domains; the canonical objects are named and shaped to be domain-general where reasonable.
- No effort is spent implementing the other domains in V1, and their absence is intentional, not an oversight.
- Adding any additional capital allocation domain requires its own trip through the development lifecycle, including RFC and, where consequential, a new ADR.
