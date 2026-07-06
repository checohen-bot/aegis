# CLAUDE.md — The Aegis Engineering Bible

## 1. Identity, Context & Authority

**What Aegis is.** Aegis is building the world's most trusted Investment Intelligence Platform for individual investors. We do **not** predict markets, prices, or returns. We improve the *quality* of capital allocation decisions through structured reasoning, evidence, institutional memory, explainability, and continuous learning. Our investment philosophy is **Adaptive Quality Investing (AQI)**: decision quality — not prediction accuracy — is the north star. Every feature, model, and line of code is judged by whether it helps an investor make a better-reasoned, better-evidenced, more self-aware decision.

**What this file is.** This is the Engineering Bible — the permanent operating ruleset for anyone (Claude Code, GPT, other AI agents, or human contributors) who reads, writes, reviews, or ships code in this repository. It encodes our engineering culture so that it survives staff turnover, model upgrades, and a decade of development. It is normative: when it says ALWAYS or NEVER, treat that as a hard constraint, not a suggestion.

**Ownership boundary.** The Founder owns vision, product direction, investment philosophy, canonical terminology, and architecture direction. Engineering owns implementation, testing, the repository, infrastructure, CI/CD, and documentation. Neither silently overrides the other.

**Authority order (for resolving any conflict).** When two sources disagree, the higher one wins:
1. Engineering Bible (this file)
2. ADRs (Architecture Decision Records)
3. RFCs (Requests for Comment)
4. Canonical Domain Model
5. Capability Map
6. Product Specs
7. Existing source code

If reality (the code) conflicts with a higher authority, the code is wrong until an ADR or RFC says otherwise — fix the code or raise the conflict; never treat "it's already like this" as justification.

**Canonical domain objects (never renamed, never aliased):** Portfolio, Holding, Company, Investment Thesis, Investment Case, Evidence, Observation, Knowledge, Decision, Capital Mission, Risk, Catalyst, Learning Event, Behavior Profile, Policy.

**Development lifecycle (never skip a step):** Business Need → Research → RFC → Architecture Review → ADR (if required) → Domain Model → Implementation Plan → Implementation → Tests → Documentation → Review → Release → Learning.

**Stack:** Python (backend, domain, AI), TypeScript + Next.js + React (web), PostgreSQL, Redis, Docker, OpenTelemetry. Architecture is a **Modular Monolith** with strict domain boundaries, Domain-Driven Design, and event-driven communication (no premature event sourcing or CQRS), and **model-agnostic AI** (capabilities over providers).

**Prime directive when specs are incomplete:** Never implement business logic from assumptions. Stop, name the gap explicitly, and draft an RFC. Inventing investment logic is the single most damaging thing you can do in this codebase.

---

## 2. Engineering Rules

### 2.1 Architecture & Domain Modeling

- ALWAYS keep business logic in the domain layer; the domain layer must be pure Python with zero imports from web, infrastructure, or AI-provider packages.
- NEVER let a domain module import from another domain's internals; cross-domain interaction happens only through published application-service interfaces or domain events.
- ALWAYS translate external data (market feeds, filings, provider responses) into canonical domain objects at the boundary before it reaches any domain logic.
- NEVER leak an infrastructure concept (ORM row, HTTP request, Redis key, Kafka-style envelope) into a domain object or domain method signature.
- ALWAYS use the exact canonical names — Portfolio, Holding, Company, Investment Thesis, Investment Case, Evidence, Observation, Knowledge, Decision, Capital Mission, Risk, Catalyst, Learning Event, Behavior Profile, Policy — in code, tables, events, and docs.
- NEVER introduce a synonym, abbreviation, or "temporary" alias for a canonical domain object (no `Pos` for Holding, no `Co` for Company, no `Thesis2`).
- ALWAYS model a new business concept as an explicit domain object or value object before writing behavior for it; no logic may hang off dictionaries or loose primitives.
- PREFER value objects for anything defined by its attributes (money amounts, confidence scores, time ranges) and entities only for things with a lifecycle identity.
- NEVER give a domain object a public setter that can put it into an invalid state; enforce invariants inside the object's own methods.
- ALWAYS express state changes that other domains care about as domain events named in past tense (e.g., `DecisionRecorded`, `EvidenceAttached`, `LearningEventCaptured`).
- NEVER build event sourcing, CQRS read models, or a message broker until an ADR explicitly approves it; in-process event dispatch is the default.
- AVOID adding a new bounded context or top-level domain without an approved RFC that defines its boundary, ubiquitous language, and owned canonical objects.
- ALWAYS depend inward: web → application → domain; infrastructure implements interfaces the domain declares, never the reverse.
- NEVER call the database, cache, or an external API directly from a domain object; the domain declares a repository or port interface and infrastructure supplies it.
- PREFER explicit application-service methods that orchestrate a use case over "smart" controllers or fat repositories that accumulate business rules.
- ALWAYS keep the Capital Mission as the anchoring context for a Portfolio; no Decision or Holding logic may ignore the Portfolio's Capital Mission.
- NEVER couple a Decision to a specific market outcome; a Decision records reasoning, evidence, and expected quality, not a predicted price.
- ALWAYS represent uncertainty, confidence, and evidence strength as first-class fields on the relevant domain objects rather than burying them in prose.
- AVOID circular dependencies between modules; if two modules need each other, a missing shared abstraction or a boundary error is the real problem — raise it.
- ALWAYS write a short domain-model note (in the module's docs) when you add or change a canonical object's behavior, so institutional memory is preserved.

### 2.2 AI & Model Usage

- NEVER call an LLM provider SDK (OpenAI, Anthropic, Google, etc.) directly from domain or application code; always go through the capability abstraction layer in `ai/capabilities/`.
- ALWAYS express AI needs as capabilities (e.g., `summarize_evidence`, `extract_thesis_claims`, `critique_reasoning`) — never as "call GPT-4" or "call Claude."
- NEVER hardcode a provider name, model ID, or provider-specific parameter into core architecture, domain logic, or business rules.
- ALWAYS keep provider selection, model IDs, and pricing/limits in configuration or the Capability Map, so a model can be swapped without touching business code.
- NEVER let a raw provider response object cross out of the AI infrastructure layer; map it into a canonical domain object or a typed capability result first.
- ALWAYS treat LLM output as an untrusted Observation until it has been validated, structured, and evidenced — never as authoritative Knowledge.
- NEVER let an AI capability silently fabricate Evidence; every AI-derived claim must carry provenance (source, capability, model, timestamp) so it is auditable.
- ALWAYS make AI reasoning explainable: capabilities must return the reasoning trace or citations that justify their output, not just a verdict.
- PREFER deterministic, testable prompt templates stored as versioned artifacts over inline f-strings scattered through the code.
- ALWAYS pin and record the capability version and model behind any AI output that influences a Decision, so we can reproduce and audit it later.
- NEVER use an LLM to compute anything that has a correct deterministic algorithm (arithmetic, portfolio weights, date math); use code for math and LLMs for reasoning over language.
- ALWAYS enforce a strict output schema (typed parsing/validation) on capability results and fail loudly when the model returns something off-contract.
- AVOID prompt logic that assumes a specific model's quirks; if a capability only works on one model, that is a bug in the capability contract.
- ALWAYS set explicit timeouts, retry policy, and cost/token budgets on every AI capability call, and degrade gracefully when they are exceeded.
- NEVER send more user or portfolio data to a provider than the capability strictly requires; minimize and redact at the capability boundary.
- ALWAYS record AI usage (capability, model, tokens, latency, cost) as telemetry so we can reason about spend and quality over time.
- PREFER capturing model disagreement or low confidence as an explicit signal surfaced to the user over hiding it behind a confident-sounding sentence.
- NEVER let AI generate a final investment recommendation presented as certainty; frame outputs as reasoning aids that the investor evaluates.
- ALWAYS route any new AI capability through the Capability Map so its contract, inputs, outputs, and fallbacks are documented before use.

### 2.3 Coding Standards

- ALWAYS write fully type-annotated Python and pass the configured type checker with no ignores except a commented, justified exception.
- ALWAYS run the repository formatter and linter before committing; unformatted or lint-failing code never lands.
- NEVER commit commented-out code, dead code, or "just in case" scaffolding; delete it — git remembers.
- PREFER small, single-responsibility functions and modules over large ones; if a function does not fit on a screen, question it.
- NEVER use bare `except:` or swallow exceptions silently; catch specific exceptions and either handle or re-raise with context.
- ALWAYS name things in the ubiquitous language of the domain, not in technical shorthand; a Holding is a `Holding`, never a `record` or `item`.
- AVOID primitive obsession: wrap money, percentages, identifiers, and scores in value objects rather than passing raw `float`/`str` around.
- ALWAYS make illegal states unrepresentable through types and constructors rather than validating them repeatedly at call sites.
- NEVER introduce global mutable state or module-level singletons for anything that carries request or portfolio context.
- PREFER pure functions and explicit dependency injection over hidden side effects and implicit global lookups.
- ALWAYS keep TypeScript `strict` mode on in web code and never use `any` without an inline justification and a follow-up plan.
- NEVER duplicate a domain rule in the TypeScript front end; the front end renders and collects, the Python domain decides.
- PREFER composition over inheritance; deep class hierarchies are a smell in this codebase.
- ALWAYS handle the empty, loading, and error states explicitly in React components — never assume data is present.
- NEVER hardcode configuration, secrets, URLs, or feature flags in source; read them from typed configuration.
- AVOID clever one-liners that obscure intent; optimize for the reader ten years from now, not for keystrokes today.
- ALWAYS keep functions free of hidden I/O; if a function reads a file, hits the network, or touches the clock, make that visible in its design.
- PREFER explicit units and time zones (UTC everywhere internally) over ambiguous timestamps and naive datetimes.
- NEVER leave `print` debugging or stray console logs in committed code; use the structured logger.

### 2.4 Testing

- ALWAYS write tests in the same change that introduces behavior; untested business logic does not merge.
- NEVER mock the domain layer in domain tests; test real domain objects against real invariants.
- ALWAYS cover the business rules of every canonical domain object with unit tests that assert its invariants and forbidden states.
- PREFER fast, deterministic unit tests for domain logic and reserve integration tests for boundaries (DB, cache, AI capabilities).
- NEVER let a test depend on a live LLM provider; test AI capabilities against recorded fixtures or a fake capability implementation.
- ALWAYS test the capability abstraction with a fake provider to prove business code is genuinely model-agnostic.
- NEVER write a test that asserts exact LLM wording; assert on structure, schema, provenance, and invariants instead.
- ALWAYS make tests deterministic — no reliance on wall-clock time, random seeds, network, or ordering of unordered collections.
- PREFER testing observable behavior and public interfaces over implementation details that will change.
- ALWAYS include at least one test that reproduces a bug before you fix it, and keep it as a regression guard.
- NEVER reduce coverage of the domain layer to make a deadline; if you must cut scope, cut features, not tests of what ships.
- ALWAYS test error paths and degraded modes (timeouts, provider failures, missing evidence), not just the happy path.
- AVOID over-mocking; a test that mocks everything proves only that the mocks were called.
- ALWAYS run the full test suite locally (or in CI) and see it green before requesting review.
- PREFER property-based or table-driven tests for logic with many input combinations (scoring, evidence weighting, policy evaluation).
- NEVER commit a skipped or `xfail` test without a linked issue explaining why and when it will be re-enabled.

### 2.5 Observability & Operations

- ALWAYS instrument code with OpenTelemetry traces, metrics, and structured logs; observability is a feature, not an afterthought.
- ALWAYS propagate a trace/correlation ID from the web request through the application and AI capabilities to the database.
- NEVER log secrets, credentials, tokens, or full portfolio holdings; log identifiers and redact sensitive fields.
- ALWAYS emit structured logs (key-value/JSON), never free-text strings that cannot be queried.
- PREFER meaningful, low-cardinality metric names tied to business outcomes (decisions recorded, evidence attached, capability latency) over incidental technical counters.
- ALWAYS record latency, cost, and outcome for every AI capability call as spans/metrics so quality and spend are observable.
- NEVER ship a feature without at least one health signal that tells operators whether it is working in production.
- ALWAYS define and document the failure mode of every external dependency (DB, Redis, provider) and how the system degrades when it is down.
- PREFER idempotent operations and safe retries; assume any external call can fail or be delivered twice.
- ALWAYS set explicit timeouts on every network and database call; no unbounded waits.
- NEVER let a background job fail silently; failures must surface as alerts or dead-letter records with enough context to diagnose.
- ALWAYS make configuration changes observable — log what config a service started with (secrets redacted).
- PREFER graceful degradation (serve cached or reduced results) over hard failure when a non-critical dependency is unavailable.
- ALWAYS keep runbooks for operational tasks (migrations, provider outage, cache flush) current in the docs.

### 2.6 Security

- NEVER commit secrets, API keys, or credentials to the repository; use the secrets manager and reference them via configuration.
- ALWAYS validate and sanitize all external input at the boundary before it reaches domain logic.
- NEVER build SQL by string concatenation; use parameterized queries or the ORM's safe interfaces.
- ALWAYS enforce authorization at the application-service boundary, checking that the caller may act on the given Portfolio or Decision.
- NEVER trust client-supplied identifiers to grant access; resolve ownership server-side on every request.
- ALWAYS treat LLM-generated content as untrusted input and guard against prompt injection when it is fed back into tools or capabilities.
- PREFER least privilege for every credential, service account, and database role; grant only what the component needs.
- ALWAYS encrypt sensitive data in transit and at rest, and document what is classified as sensitive.
- NEVER expose internal stack traces, provider errors, or infrastructure details in API responses to users.
- ALWAYS pin and audit third-party dependencies, and remove any dependency that is unmaintained or unnecessary.
- NEVER disable TLS verification or weaken crypto to "make it work"; fix the root cause.
- ALWAYS rotate credentials on a schedule and immediately if exposure is suspected.
- PREFER allow-lists over deny-lists when validating inputs, file types, or outbound destinations.
- ALWAYS scope personal and financial data access with an audit trail; who read or changed a Portfolio must be reconstructable.

### 2.7 Documentation

- ALWAYS update the relevant documentation in the same pull request that changes behavior; stale docs are treated as bugs.
- ALWAYS document the "why" — the decision and its trade-offs — not just the "what," which the code already shows.
- PREFER a short ADR for any architecturally significant decision over an undocumented change that future engineers must reverse-engineer.
- NEVER let a canonical domain object exist without a docstring explaining its meaning, invariants, and relationships to other objects.
- ALWAYS keep the Capability Map current whenever an AI capability is added, changed, or retired.
- ALWAYS write module-level READMEs that state the module's responsibility and its public interface, and keep them accurate.
- PREFER runnable examples and clear interface docs over long prose; show how to use a capability or service.
- NEVER document aspirational behavior as if it exists; document what the code actually does today and mark future work explicitly.
- ALWAYS record institutional learning from incidents and Learning Events so mistakes are not repeated.
- AVOID duplicating the same explanation in many places; link to a single source of truth and keep it authoritative.

### 2.8 Git & Pull Requests

- ALWAYS work on a branch; never commit directly to the default branch.
- ALWAYS write imperative, descriptive commit messages that explain intent, and keep each commit a coherent logical unit.
- PREFER small, focused pull requests that do one thing over large PRs that mix refactors, features, and fixes.
- NEVER mix an unrelated refactor into a feature PR; separate them so review and revert stay clean.
- ALWAYS link the PR to its RFC, ADR, or issue so the lifecycle trail is intact.
- ALWAYS ensure CI is green (tests, lint, type check, security scan) before requesting review; never ask a human to review red CI.
- NEVER force-push over a shared branch others are working on or over review history without agreement.
- ALWAYS keep the PR description explaining what changed, why, how it was tested, and what risks remain.
- PREFER rebasing your branch on the latest default branch over merge commits that clutter history, unless the team convention says otherwise.
- NEVER merge your own PR without the required approvals, and never bypass branch protection.
- ALWAYS delete merged branches to keep the repository tidy.
- AVOID committing generated artifacts, build output, or large binaries; add them to ignore files and store them appropriately.

### 2.9 RFC / ADR Process

- ALWAYS follow the lifecycle in order: Business Need → Research → RFC → Architecture Review → ADR → Domain Model → Implementation Plan → Implementation → Tests → Documentation → Review → Release → Learning, and never skip a step.
- ALWAYS write an RFC before implementing anything that introduces a new domain concept, crosses a domain boundary, or changes architecture.
- NEVER change architecture silently because you disagree with it; document the issue, explain trade-offs, draft a proposed RFC, and wait for approval.
- ALWAYS stop and draft an RFC — rather than inventing business logic — when a spec is incomplete or ambiguous about investment behavior.
- ALWAYS capture an ADR for every architecturally significant decision, including the context, the options considered, the decision, and its consequences.
- NEVER mark an ADR as superseded without a new ADR that references and explains why it replaces the old one.
- PREFER writing the RFC as a genuine question seeking review, listing alternatives and trade-offs, over writing it as a rubber-stamp of a decision already made.
- ALWAYS get the Founder's sign-off when a change touches vision, product direction, investment philosophy, canonical terminology, or architecture direction.
- NEVER treat an RFC as approved until it is explicitly approved; a draft RFC does not authorize implementation.
- ALWAYS record the outcome of the Learning step so each shipped change feeds institutional memory.
- AVOID letting RFCs become novels; keep them focused on the decision, the constraints, and the trade-offs.

### 2.10 Repository Structure

- ALWAYS place domain logic under the domain layer, application orchestration under the application layer, adapters under infrastructure, and AI capability implementations under `ai/capabilities/`.
- NEVER put web, infrastructure, or provider code inside a domain package; the folder structure must mirror the dependency rule.
- ALWAYS keep one bounded context per top-level domain package with clear ownership of its canonical objects.
- PREFER explicit public interfaces (an `__init__` or interface module) per module and keep everything else internal.
- NEVER reach into another module's private internals; import only its published interface.
- ALWAYS colocate tests with the code they test following the repository's established convention.
- ALWAYS keep prompt templates, capability contracts, and the Capability Map in their designated versioned locations, not inline in business code.
- PREFER a consistent, predictable layout so a new engineer can guess where something lives; deviations need a reason.
- NEVER create a `utils`/`misc`/`common` dumping ground; give shared code a real home named for its responsibility.
- ALWAYS keep configuration, migrations, and infrastructure definitions in their designated directories, versioned with the code.

### 2.11 Code Review

- ALWAYS review for correctness, domain-boundary integrity, canonical-naming compliance, and provider-agnosticism, not just style.
- NEVER approve a change that leaks infrastructure into the domain, calls a provider SDK from business code, or renames a canonical object.
- ALWAYS check that new business logic is tested, documented, and traceable to an RFC/ADR/issue before approving.
- PREFER blocking a PR that invents business logic from assumptions and asking for an RFC over letting it merge to "iterate later."
- ALWAYS leave specific, actionable review comments and distinguish blocking issues from optional suggestions.
- NEVER approve code you do not understand; ask until you do, because you are co-owning it.
- ALWAYS verify observability, error handling, and security are present, not just the happy path.
- PREFER at least one reviewer with context on the touched domain; architecture-significant changes need architecture review.
- NEVER rubber-stamp; an approval means you would be comfortable maintaining this code.
- ALWAYS confirm the PR's scope matches its description and that unrelated changes were not smuggled in.
- AVOID nitpicking style the formatter already enforces; spend review attention on design and correctness.

### 2.12 Release Management

- ALWAYS release from a green pipeline with all tests, checks, and scans passing; no manual overrides to ship faster.
- ALWAYS use versioned, reversible database migrations, and never make a breaking schema change without a backward-compatible transition.
- PREFER small, frequent, incremental releases over large risky batches.
- ALWAYS be able to roll back or forward-fix quickly; every release must have a known recovery path.
- NEVER change a public interface or event contract without versioning it and providing a migration path for consumers.
- ALWAYS gate risky or unfinished features behind flags rather than shipping half-built behavior to all users.
- ALWAYS write a concise changelog entry describing what changed and any operational impact for each release.
- NEVER deploy on assumptions about production state; verify config, migrations, and health after release.
- ALWAYS complete the Learning step after a release, capturing what went well, what broke, and what we will change.
- PREFER automated, repeatable deployments over manual steps; if a release step is manual, document it and plan to automate it.
- AVOID coupling a release to a specific AI provider being available; provider changes must not require a redeploy of business code.

---

## 3. Definition of Done

A change is Done only when **all** of the following are true:

- [ ] It traces to a Business Need and, where required, an approved RFC and ADR — no invented business logic.
- [ ] Domain logic lives in the domain layer, uses only canonical names, and leaks no infrastructure or provider details.
- [ ] All AI usage goes through the capability abstraction with recorded provenance, versioning, and provider-agnostic contracts.
- [ ] Tests (unit + integration where relevant) are written, deterministic, and green; error and degraded paths are covered.
- [ ] Type checking, linting, formatting, and security scanning all pass in CI.
- [ ] Observability (traces, metrics, structured logs) is in place with correlation IDs and no sensitive data logged.
- [ ] Documentation, module READMEs, the Capability Map, and any ADR are updated in the same PR.
- [ ] The PR is small, focused, reviewed, approved, and linked to its issue/RFC/ADR.
- [ ] Migrations are reversible, interfaces are versioned, and a rollback path exists.
- [ ] The Learning step is captured so institutional memory grows.

---

## 4. Closing Principle

Build as if this system will be actively developed ten years from now — by engineers and AI agents who have never met you and cannot ask you what you meant. That means canonical names stay canonical, boundaries stay strict, decisions are written down, evidence is preserved, and no shortcut is worth eroding the trust an individual investor places in Aegis to help them reason well about their own capital. We are not optimizing for speed of typing or cleverness of code; we are compounding decision quality, explainability, and institutional memory. Every commit either strengthens that foundation or quietly weakens it — always choose to strengthen it.
