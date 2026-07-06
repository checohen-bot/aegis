# Pull Request Template (content reference)

> This is the canonical content reference for Aegis pull request descriptions.
> The active GitHub template lives at `.github/PULL_REQUEST_TEMPLATE.md`; keep the two in sync.
> Fill every section. Delete a section only if you can honestly write "n/a" and say why.

## Business objective

[What investor or business outcome does this PR serve, in one or two sentences? Not "what the code does" — *why it matters*. If this closes an issue, link it: Closes #[issue].]

## Relevant RFC

[Link the RFC that proposed this work: RFC-[number]. If none applies, write "n/a — [reason, e.g., internal fix within existing design]". Architecturally significant changes without an RFC will be blocked in review.]

## Relevant ADR

[Link the ADR(s) this implements or complies with: ADR-[number]. If this PR *makes* a new architectural decision, that decision must be recorded in an ADR first — link it here. Write "n/a" only if no architectural decision is involved.]

## What changed

[A concise, accurate summary of the change so a reviewer knows what to expect before reading the diff. Bullet the notable points. Name the modules and canonical domain objects touched (Thesis, Decision, Capital Mission, ...).]

- [change]
- [change]

## Architecture impact

[Address each that applies; write "none" for the rest.]

- **Domain boundaries:** [new/changed cross-module contracts, module ownership]
- **Data / migrations:** [schema changes; link the migration; reversible?]
- **API surface:** [new/changed endpoints; versioning; explainability fields present on reasoned resources?]
- **External boundaries:** [IBKR, AI providers — adapter changes; no raw vendor types crossed into the domain]
- **Security:** [touches authn/authz or brokerage credentials? If yes, security reviewer required — @-mention them.]
- **Observability:** [new traces/metrics/domain-event instrumentation added]

## Testing performed

[What proves this works? List the test types added or updated (unit, integration, contract, e2e) and any manual verification. For changes to Thesis / Decision / Capital Mission / Risk logic, confirm the 95% branch-coverage floor is met and failure paths are tested. State what you did, not "tested locally".]

- [ ] Unit tests added/updated
- [ ] Integration tests added/updated
- [ ] Contract tests for affected external boundaries
- [ ] E2E for affected user journey (if applicable)
- [ ] Domain model is not mocked in any new test
- [ ] Full suite green locally

## Known limitations

[What does this PR deliberately *not* handle? Edge cases out of scope, temporary constraints, tech debt knowingly incurred. Be candid — hidden limitations become production incidents.]

## Future improvements

[Follow-on work this enables or requires. Link tracking issues for anything deferred. Do not leave TODOs in the code — record them here or as issues.]

## Reviewer checklist reminder

[Confirm before requesting review:]

- [ ] PR is single-purpose and reasonably sized
- [ ] Commits follow Conventional Commits and reference RFC/ADR
- [ ] The review checklist (`templates/review-checklist.md`) can be satisfied
