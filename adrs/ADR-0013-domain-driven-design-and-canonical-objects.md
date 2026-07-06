# ADR-0013: Domain-Driven Design with Frozen Canonical Domain Object Names

**Status:** Accepted

## Context

Aegis's value depends on a shared, precise language across founder, product, engineering, documentation, and AI. Ambiguous or drifting terminology corrodes institutional memory and produces systems that no longer mean what they say. Domain-Driven Design offers the discipline: model the domain explicitly, bound its contexts, and use a ubiquitous language everywhere.

The founder has fixed a set of canonical domain object names and requires that they never be renamed. These names are the ubiquitous language of the company.

## Decision

Aegis is designed with **Domain-Driven Design** and strict domain boundaries (see ADR-0008).

The following canonical domain object names are **frozen** and are never renamed. They are used exactly, in code, documentation, conversation, and AI:

Portfolio, Holding, Company, Investment Thesis, Investment Case, Evidence, Observation, Knowledge, Decision, Capital Mission, Risk, Catalyst, Learning Event, Behavior Profile, Policy.

Their canonical definitions are maintained in `bible/appendices/glossary.md`.

## Consequences

- The canonical names are the ubiquitous language; synonyms and renamings are not permitted.
- Code identifiers, database schemas, API contracts, and documentation reflect these names faithfully.
- The glossary is the authoritative definition of each object; changes to a definition follow the standard lifecycle and require Bible updates.
- New domain concepts may be introduced through the lifecycle, but the existing canonical names are immutable and may not be repurposed.
- This shared language is a precondition for the explainability and auditability required by ADR-0003.
