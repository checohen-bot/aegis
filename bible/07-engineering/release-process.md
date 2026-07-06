# Release Process

*Volume VII — Engineering · Chapter 8*

A release is the moment a proven change becomes a change users depend on. Our
release discipline exists to make that moment boring: small, frequent,
reversible, and fully traceable. Everything before this point — the lifecycle
(Chapter 3), the tests (Chapter 4), the pipeline (Chapter 5) — is what earns the
right to a boring release. This chapter defines how we version, record, ship,
and, when necessary, undo.

## Versioning Strategy

Aegis versions releases with semantic versioning — `MAJOR.MINOR.PATCH`:

- **MAJOR** for a breaking change to a published contract — a module interface or
  an event schema other modules or the frontend depend on. Breaking changes are
  consequential and are expected to be rare and ADR-backed.
- **MINOR** for backward-compatible new capability — a new feature, a new event,
  an additive interface method.
- **PATCH** for backward-compatible fixes — bug fixes and internal improvements
  that change no contract.

Because Aegis is a Modular Monolith deployed as a single lineage, the release
version identifies the deployable as a whole. Individual module interfaces and
event schemas carry their own contract versions (a mandatory module concern,
Volume IV) so that consumers can reason about compatibility independently of the
release number. Every release maps to exactly one content-addressed Docker image
and one Git tag; the version, the tag, and the image are three names for the same
artifact.

## Changelog Discipline

Every release has a changelog entry, and every user-visible or contract-visible
change contributes to it. The changelog is written for the reader who needs to
know *what changed and whether it affects them* — grouped into added, changed,
fixed, and, prominently, breaking. Breaking changes state the migration path.
Each entry references its governing RFC/ADR so a reader can trace any line back
to the decision behind it. The changelog is not generated blindly from commit
messages; it is curated as part of the release, because it is a document our own
future engineers and, eventually, integrators will rely on. A release with no
changelog entry is not a release.

## The Release Checklist

A release is executed against an explicit checklist, not from memory:

1. All changes merged are lifecycle-complete — RFC/ADR-backed, tested,
   documented, reviewed.
2. The version number is chosen per the semantic-versioning rules above and the
   change's contract impact.
3. The changelog entry is written, reviewed, and includes migration notes for any
   breaking change.
4. The release pipeline is green — full test matrix including E2E for critical
   journeys, production-parity image built once, migrations validated (Chapter 5).
5. The candidate has been exercised in **staging** with production-shaped data
   and configuration, including migration rehearsal.
6. Database migrations are backward-compatible with the currently-running version
   (expand-then-contract), so the new code and old code can coexist during
   rollout and rollback is possible.
7. Observability is ready — the dashboards, metrics, logs, and traces that will
   tell us whether the release is healthy are known before deploy.
8. A rollback path is confirmed for this specific release.
9. The Git tag is cut and the exact image promoted through dev → staging → prod
   (Chapter 5).

Promotion to prod is deliberate and observed live through the OpenTelemetry
signals every module emits. Releases are kept small precisely so that this
checklist stays cheap and the blast radius of any single release stays small.

## Rollback Philosophy

We design for rollback before we deploy, because the fastest safe response to a
bad release is to stop exposing it. Our stance:

- **Rolling back is a normal, blameless operation**, not a failure of nerve.
  Recover first; understand later.
- **Roll back by promoting the previous known-good image**, which still exists
  because every release is an immutable, content-addressed artifact. We do not
  hot-patch production.
- **Migrations are expand-then-contract** so that schema changes never strand a
  rollback. The destructive contract step happens only after the new version is
  confirmed healthy, in a later release.
- **Health checks gate the deploy** (a mandatory module concern): a release that
  fails its health checks is stopped by orchestration before it takes
  user-facing traffic, which is rollback made automatic.

A release we cannot roll back is a release we are not ready to ship; if a change
genuinely cannot be reversed, that irreversibility is an ADR-level decision made
consciously, not discovered in an incident.

## Release And The Learning Stage

Shipping is not the end of the lifecycle; it is the setup for its final stage.
Every release is observed against the business need that motivated it (Chapter
3, Learning). We ask: did it produce the outcome the RFC predicted? What did the
metrics, the user behaviour, and any incident teach us? The answer is written
down as a Learning Event — the durable artifact that closes the loop and feeds
the next Research stage. Incidents and rollbacks are especially rich learning and
always yield a regression test (Chapter 4) and, where a systemic cause is found,
a bible or standards update. In this way each release makes the next one safer,
and the release process is not merely how we ship but part of how Aegis learns.
