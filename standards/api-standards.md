# API Design Standards

These standards apply to all HTTP APIs at Aegis — FastAPI services on the backend and Next.js route handlers on the web tier. They exist so that clients, and our own future selves, can consume the platform predictably. They are enforced in review.

## 1. Resources are named for canonical domain objects

REST resources map directly to the canonical domain vocabulary. Collections are plural nouns; nested paths express ownership.

```
GET  /v1/portfolios
GET  /v1/portfolios/{portfolioId}/holdings
GET  /v1/companies/{companyId}
GET  /v1/theses/{thesisId}
POST /v1/decisions
GET  /v1/capital-missions/{missionId}
```

- Use the canonical names verbatim: `theses`, `decisions`, `capital-missions`, `evidence`, `observations`, `catalysts`, `risks`, `policies`. No synonyms, no invented resources.
- Paths are lower-kebab-case; identifiers are opaque strings (UUID/ULID), never sequential integers exposed as-is.
- Verbs do not appear in paths. State transitions that are not plain CRUD are modeled as sub-resources representing the domain event: `POST /v1/theses/{thesisId}/invalidation` rather than `POST /v1/theses/{thesisId}/invalidate`. HTTP methods carry the action.

## 2. Versioning

- The API is versioned in the path: `/v1/...`. The version increments only on a breaking change.
- Additive changes (new optional fields, new endpoints) are backward-compatible and do not bump the version. Clients must tolerate unknown fields.
- Breaking changes require an ADR and a deprecation window: the old version runs alongside the new one, with a `Deprecation` and `Sunset` response header on the old, until the documented removal date.

## 3. Error response format

Every error response uses one consistent envelope with an appropriate HTTP status (`400/401/403/404/409/422/429/500`):

```json
{
  "error": {
    "code": "THESIS_NOT_FOUND",
    "message": "No thesis exists with id 01H...",
    "details": [
      { "field": "thesisId", "issue": "unknown identifier" }
    ],
    "traceId": "b7ad6b7169203331"
  }
}
```

- `code` is a stable, screaming-snake-case machine identifier; clients branch on it, not on `message`.
- `message` is human-readable and safe to surface; it never leaks secrets, stack traces, or internal identifiers.
- `traceId` is the OpenTelemetry trace id, so any error can be tied to its trace.
- Validation failures return `422` with per-field `details`.

## 4. Pagination

List endpoints are always paginated — never return an unbounded collection. Aegis uses cursor-based pagination:

```
GET /v1/decisions?limit=50&cursor=eyJvZmZzZXQiOjUwfQ

{
  "data": [ ... ],
  "page": { "nextCursor": "eyJ...", "hasMore": true, "limit": 50 }
}
```

- Default `limit` is 25, maximum 100; requests exceeding the max are clamped, not rejected.
- Cursors are opaque and stable under insertion. Do not use raw offset pagination for domain collections that change frequently.
- List responses put items under `data` and pagination under `page`, consistently across all endpoints.

## 5. Explainability is a first-class field, not an afterthought

Aegis is an intelligence platform: an investor must be able to see *why*. Any response representing a reasoned domain object must expose the reasoning links it carries in the model.

- A **Decision** response includes the Evidence and the Thesis it was based on:

```json
{
  "id": "01H...",
  "action": "REDUCE",
  "holdingId": "01H...",
  "rationale": "Thesis catalyst failed to materialize by target date.",
  "basedOn": {
    "thesisId": "01H...",
    "evidence": [
      { "id": "01H...", "type": "OBSERVATION", "summary": "Q3 revenue missed guidance by 8%" }
    ]
  }
}
```

- A **Thesis** response links its supporting Evidence, Catalysts, and Risks. A **Capital Mission** response links its governing Policy and originating Thesis.
- These explainability fields are required, not optional. A Decision returned without its `basedOn` linkage is a defect. Where the underlying links are absent, that itself is a domain invariant violation, not a reason to omit the field.
- When explainability content originates from the AI layer, it is returned as structured domain Evidence/Observation objects — never as raw provider output.

## 6. Conventions

Request and response bodies are `application/json` with `camelCase` fields. Timestamps are RFC 3339 UTC (`2026-07-06T14:30:00Z`). `GET` is side-effect-free and cacheable; mutations use `POST/PATCH/DELETE`. Reviewers verify resource naming, the error envelope, pagination, and the presence of explainability fields on every reasoned resource.
