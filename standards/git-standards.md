# Git Workflow Standards

A clean, legible history is part of the engineering record — it is how we reconstruct *why* a change was made, tie code to the RFC/ADR that authorized it, and learn from what shipped. These standards are enforced through branch protection and code review.

## 1. Branch naming

Branches are short-lived and named `type/short-description` in lower-kebab-case, optionally prefixed with an issue key:

```
feat/thesis-invalidation-flow
fix/decision-missing-evidence-guard
refactor/portfolio-repository-boundary
chore/bump-pip-audit
docs/api-error-envelope
AEG-142/capital-mission-policy-check
```

`type` is one of: `feat`, `fix`, `refactor`, `chore`, `docs`, `test`, `perf`. One branch, one focused piece of work. Long-lived personal branches accumulate conflicts and hide work — delete branches after merge.

## 2. Commit messages

Commits follow Conventional Commits:

```
<type>(<scope>): <imperative summary>

<body: what changed and why, wrapped at 72 cols>

Refs: RFC-014, ADR-009
```

- `type` matches the branch types above; `scope` is the module (`decision`, `thesis`, `api`, `web`).
- The summary is imperative and under 72 characters: "add evidence guard to Decision", not "added" or "fixes".
- The body explains *why*, referencing the RFC/ADR where applicable. The diff already shows *what*.
- Each commit builds and passes tests on its own; do not commit known-broken intermediate states on a shared branch.

## 3. PR size and scope

- Keep pull requests small and single-purpose. Target under ~400 lines of diff excluding generated files, lockfiles, and tests. Large PRs get shallow reviews; split them.
- A PR does one thing: one feature, one fix, one refactor. Do not mix a refactor with a behavior change — reviewers cannot tell which lines changed behavior. If a refactor is needed to enable a feature, land the refactor first as its own PR.
- Every PR fills out the pull request template (business objective, RFC/ADR links, architecture impact, testing performed, known limitations).

## 4. PRs reference the RFC/ADR that authorized them

Aegis's lifecycle runs Business Need → Research → RFC → Architecture Review → ADR → ... → Implementation. Code does not appear from nowhere.

- Any PR that introduces new architecture, a new domain concept, a new external dependency, a new cross-module contract, or a breaking API change **must** link the RFC and/or ADR that authorized it. A PR making an architectural decision that has no ADR is blocked until the decision is recorded.
- Small, self-evident fixes and internal refactors within a module's existing design do not require an RFC/ADR, but still link the tracking issue.
- Reviewers reject architecturally significant changes that arrive without their governing decision documented.

## 5. Rebase vs merge

- Update a feature branch by **rebasing** onto `main` (`git pull --rebase`). Do not create "Merge branch main into feature" commits on feature branches — they clutter history and obscure the real change.
- Keep the branch's own history tidy: squash noise commits ("wip", "fix typo", "address review") locally before requesting final review, so each commit is meaningful.
- Merge to `main` via the platform's **squash merge**, producing one clean, well-described commit per PR that references the RFC/ADR. This keeps `main` linear and each entry traceable to a reviewed PR.
- Never force-push a shared branch that others are working on. Force-pushing your own in-review branch after a rebase is fine; coordinate if anyone else has it checked out.

## 6. Protected `main`

`main` is always releasable. Protection rules enforce:

- No direct pushes. All changes land through reviewed, squash-merged PRs.
- At least one approving review; sensitive surfaces (authn/authz, brokerage credentials) require the additional security reviewer per the security standards.
- All required status checks green: `mypy --strict`, TypeScript strict build, lint, the full test suite with coverage floors, secret scanning, and dependency audit.
- Branch must be up to date with `main` (rebased) before merge.
- Force-pushes and deletions of `main` are forbidden for everyone.

History is a shared asset. Keep it legible, keep it traceable, keep `main` green.
