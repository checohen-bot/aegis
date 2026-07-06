# CI/CD

*Volume VII — Engineering · Chapter 5*

Continuous integration and delivery mechanise the checkable parts of our
principles. CI's job is to make the correct path automatic and the incorrect path
impossible to merge; humans then spend their review attention on what machines
cannot judge — architecture, domain correctness, maintainability (Chapter 7).
All pipelines live in `/.github` as source-controlled workflows, so what runs on
your PR is itself reviewable code.

## Philosophy

Three rules shape our pipeline. **Fast feedback:** the common path — lint,
typecheck, unit tests — returns in minutes, because a slow pipeline is a pipeline
engineers learn to route around. **Deterministic and reproducible:** every job
runs in a pinned, Docker-based environment with locked dependencies, so a green
run on CI means a green run anywhere and a failure is never "works on my
machine". **The pipeline is the gate:** merge protection is defined in the
repository, not in a person's discipline. If a check matters, it is enforced by
CI, not requested in a comment.

## On Every Pull Request

Every PR, on every push, runs the full pre-merge suite:

- **Lint.** Python (formatting and static lint) and TypeScript (ESLint,
  formatting). Style is a machine's job; reviewers never spend attention on it.
- **Typecheck.** Full static type checking on both the Python backend/domain and
  the TypeScript/Next.js frontend. Typed interfaces are a mandatory module
  concern (Volume IV); CI proves they hold.
- **Unit tests.** The complete unit suite, isolated from infrastructure, fast.
- **Integration tests.** Against ephemeral PostgreSQL and Redis provisioned by
  Docker inside the CI job — the same images used locally and in production.
- **Contract tests.** Module interface and event-schema contracts, including the
  AI Capability Gateway boundary.
- **Security checks.** Dependency vulnerability audit and secret scanning. A new
  high-severity vulnerability or a leaked secret fails the build.
- **Critical-path coverage.** A dedicated gate asserts full coverage of Thesis
  validation, Decision recording, and Capital allocation (Chapter 4). It cannot
  be waived without an ADR.

A red pipeline cannot be merged, and a stale branch must be updated against the
base before merging so the checks reflect reality.

## What Gates A Merge

Merging to the default branch requires, all together: a green pipeline; at least
one approving review from a code owner of every touched module (Chapter 7); a PR
description that references the governing RFC/ADR and states the business
objective, testing performed, known limitations, and future improvements; an
up-to-date branch; and resolution of every review thread. These gates are
encoded in branch protection, not left to memory. There is no "merge anyway"
for anyone; an exception requires an explicit, documented decision.

## On Release

When a change is promoted for release (Chapter 8), the release pipeline runs a
superset of the PR suite: the full test matrix including end-to-end tests for
critical user journeys; a production-parity build of the Docker images that will
actually ship; database-migration validation against a production-shaped
schema; and generation of the versioned artifact and changelog entry. The
release pipeline builds the image once; that exact, content-addressed image is
what promotes through every environment. We never rebuild per environment —
rebuilding would break the guarantee that what we tested is what we ship.

## Environment Promotion

Aegis uses three environments, and a build moves forward through all of them in
order — never sideways, never skipping:

- **dev** — continuously updated from the default branch. Where integration is
  observed first. Disposable data, fast iteration.
- **staging** — a production-parity environment: same Docker images, same
  configuration shape, production-like data volumes and schema. The release
  candidate is exercised here, including E2E tests and migration rehearsal.
  Nothing reaches production that has not proven itself in staging.
- **prod** — user-facing, capital-bearing. Deployments are deliberate, small,
  and reversible. Promotion to prod is a gated action following the release
  checklist, observed live through the OpenTelemetry metrics, logs, and traces
  every module is required to emit (Volume IV).

Configuration differs between environments only through injected configuration
and secrets, never through different code or different images. The same
content-addressed image that ran in staging is the one promoted to prod.

## Integration With Docker

Docker is the substrate that makes CI, local development, and production the same
world. Developers run the stack locally with the same Compose-defined
PostgreSQL and Redis that CI provisions and that production runs (Chapter 6). CI
jobs execute inside these images; the release pipeline builds the shippable
images; promotion moves those images across environments. This single lineage —
one image, built once, tested in CI and staging, promoted to prod — is what lets
a green check honestly mean "safe to ship". Health checks (a mandatory module
concern) are wired into the container orchestration so that a failing deploy is
detected and stopped before it takes user-facing traffic, which is the technical
foundation of the rollback philosophy in Chapter 8.
