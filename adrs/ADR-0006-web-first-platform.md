# ADR-0006: Web-First Platform Strategy

**Status:** Accepted

## Context

Aegis must choose an initial delivery platform. The product is analytical and evidence-rich, favoring larger surfaces and deep-linking of provenance and reasoning. The company must reach individual investors broadly and iterate quickly, without the distribution and release friction of native app stores in the early stages.

The founder has chosen a web-first strategy. This does not preclude native clients later; it fixes the first, primary surface.

## Decision

Aegis is **web-first**. The primary product surface is a web application built with TypeScript, Next.js, and React.

Native mobile or desktop clients are out of V1 scope. The web application is designed to be responsive and usable across devices, but the web is the canonical surface.

## Consequences

- Product and engineering prioritize the web experience; there is no native app in V1.
- Rapid iteration and universal reach are favored over platform-specific native capabilities.
- The frontend stack is fixed by ADR-0011; this ADR fixes the platform strategy that motivates it.
- Future native clients, if pursued, will require their own ADR and will consume the same backend and domain services rather than replacing them.
