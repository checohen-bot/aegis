# Definition of Done

*Volume IX — Execution Playbook · Chapter 5*

This is the company-wide Definition of Done. It is the single standard against which every pull request, feature, and milestone is judged. It exists to prevent the most common failure of engineering organizations: mistaking motion for progress. Read this chapter as a gate, not an aspiration — work that does not satisfy it is not done, regardless of how much of it exists or how quickly it arrived.

## What Success Is Not

The founder's definition is explicit and is restated here without softening. Success at Aegis is **not** measured by:

- **Lines of code.** More code is a cost, not an achievement. The best solution is often the one that deletes code.
- **Velocity.** Story points and burn-down charts measure the appearance of speed, not the creation of durable value.
- **Feature count.** A long feature list on a weak foundation is a liability, not an asset.
- **Commit count.** Activity is not accomplishment. A thousand commits that muddy the architecture are worse than one that clarifies it.

Any metric that rewards volume over quality is explicitly rejected as a measure of done. We do not celebrate throughput.

## What Success Is

Success **is** measured by the following qualities. These are the axes of the Definition of Done, and every unit of work is checked against them.

1. **Architectural consistency** — the work respects module boundaries, the Modular Monolith discipline, and the architectural principles. Cross-module communication is through published interfaces or domain events only; no shared-table access, no reaching into another module's internals. Any override of a principle is a written, accepted ADR — never silent.

2. **Decision quality** — the choices embedded in the work are sound and, where structural, are recorded. A reviewer can reconstruct *why* the work is shaped as it is from the repository alone (RFC, ADR, domain model).

3. **Repository quality** — the change leaves the repository cleaner or no worse: consistent structure, correct naming, no dead code, no orphaned config, no undocumented magic.

4. **Maintainability** — a competent engineer who has never seen this code can understand, safely change, and extend it. Complexity is justified, isolated, and documented — never incidental.

5. **Reliability** — the work behaves correctly under expected and adverse conditions, has tests that encode its invariants (not its implementation), and fails safely and visibly rather than silently.

6. **Developer productivity** — the work makes future work cheaper: reusable patterns over one-offs, clear interfaces over clever coupling, good local ergonomics (it builds and runs from the documented single command).

7. **Explainability** — consistent with the product's own first principle, any Decision, AI-produced Observation or Knowledge artifact, or material recommendation carries its provenance: the Evidence it rests on, the Thesis or Policy it serves, the model and prompt version that produced it, and the inputs current at the time. If a feature cannot explain itself, it is not shippable.

8. **Trust** — the work is honest. It does what it claims, its documentation matches its behavior, and it does not hide failure modes, data loss risks, or shortcuts. Trust is the product's core value proposition to investors and must be true internally first.

9. **Long-term evolution** — the work can be extended and replaced without breakage. Dependencies are behind adapters; objects can gain attributes without rewrites; the boundary is designed so the component could be removed. If you cannot describe how it would be replaced, it is not done.

## The Checklist

A pull request or milestone is done when **all** of the following hold. Any unchecked item blocks merge.

- [ ] It traces to a Business Need and, where required, an approved RFC and ADR — no invented business logic.
- [ ] Boundaries respected — interfaces/events only, no cross-module table access; any principle override is a written ADR.
- [ ] The reasoning is recoverable from the repo — RFC/ADR/domain model present as the change warrants.
- [ ] Repository left cleaner or equal — no dead code, no orphaned config, consistent naming and structure.
- [ ] Understandable by a fresh engineer — complexity justified, isolated, and documented.
- [ ] Invariants tested — tests encode promises, not implementation; the slice is proven end-to-end where applicable.
- [ ] Fails safely and visibly — adverse conditions handled; no silent failure or silent data loss.
- [ ] Provenance present — Decisions/AI artifacts/recommendations carry Evidence, served intent, model/prompt version, and inputs-at-time.
- [ ] Docs match behavior — documentation is accurate and lives where it will be found.
- [ ] Replaceability describable — you can state how this component would be removed or swapped.
- [ ] CI green — build, lint, type-check, tests, and boundary checks all pass through the pipeline.

## How It Is Applied

The Definition of Done is enforced at two points. **CI/CD** enforces the mechanically checkable items (build, lint, types, tests, boundary checks) — a merge that fails them cannot land. **Review** enforces the judgment items (consistency, decision quality, maintainability, explainability, trust, evolution) — a reviewer who cannot check every box does not approve. Milestones (Chapter 4) inherit this standard: a milestone is done only when the work under it is done by this definition. We measure what we are — architecturally consistent, reliable, explainable, trustworthy, and built to evolve — not how much we produced.
