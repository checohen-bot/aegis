# ADR-0001: Repository Name "aegis" and Public Visibility

**Status:** Accepted

## Context

The company needs a single, durable home for its engineering operating system: code, decisions, domain model, standards, and institutional memory. The name of that home and its visibility posture are foundational decisions that shape branding, discoverability, and the boundary between what is shared and what is protected.

The founder has chosen the name and a public-but-closed posture. An "aegis" is a shield and a source of protection, which reflects the product's purpose: protecting individual investors from poor capital allocation decisions. A public repository serves visibility and portfolio purposes, while the intellectual property remains protected by license.

## Decision

The repository is named `aegis` and is hosted on GitHub at `checohen-bot/aegis` with **public** visibility.

The repository is public for visibility and portfolio purposes only. It is licensed as proprietary, All Rights Reserved (see `LICENSE`). The code and methodology are not open source.

## Consequences

- The name `aegis` is the canonical identity of the repository and product surface.
- Anyone can read the repository. Contributors must assume all committed content is world-readable, and must never commit secrets, credentials, customer data, or confidential material.
- The proprietary license governs use; public visibility grants no rights to the code or methodology.
- Documentation and history are written to a public-facing standard of clarity and professionalism at all times.
