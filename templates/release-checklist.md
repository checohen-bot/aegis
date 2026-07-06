# Release Checklist

> Completed by the release owner for every release to production. A release proceeds only when every applicable item is checked. Items marked **(blocker)** stop the release. This is the "Release" step of the Aegis lifecycle and feeds directly into "Learning".

| Field | Value |
|-------|-------|
| **Release** | [version / tag] |
| **Release owner** | [name] |
| **Date** | [YYYY-MM-DD] |
| **Scope** | [PRs / features included — link the RFCs/ADRs shipped] |

## 1. Code and changelog

- [ ] All included PRs are squash-merged to `main` and reference their RFC/ADR.
- [ ] `CHANGELOG.md` is updated with user-facing changes, grouped (Added / Changed / Fixed / Security), under the new version. **(blocker)**
- [ ] Version tag follows the agreed scheme and is applied to the release commit.
- [ ] Breaking API changes are versioned and documented with deprecation/sunset headers where applicable.

## 2. Tests and quality gates

- [ ] Full test suite is green on the release commit (unit, integration, contract, e2e). **(blocker)**
- [ ] Coverage floors met, including the 95% floor on Thesis / Decision / Capital Mission / Risk. **(blocker)**
- [ ] `mypy --strict` and TypeScript strict build pass; lint clean.
- [ ] Secret scanning and dependency vulnerability scans pass with no unresolved critical/high advisories. **(blocker)**

## 3. Migrations and data

- [ ] All database migrations in this release are reviewed and tested against a production-like dataset. **(blocker)**
- [ ] Migration ordering vs. deploy is confirmed (backward-compatible: deploy-then-migrate or migrate-then-deploy chosen deliberately).
- [ ] Each migration is reversible, or a forward-fix path is documented where it is not.
- [ ] Estimated migration duration and locking impact reviewed for large tables.

## 4. Rollback plan

- [ ] Rollback procedure is documented and understood by the on-call engineer. **(blocker)**
- [ ] Code rollback path confirmed (revert/redeploy previous tag).
- [ ] Data rollback or forward-fix confirmed for every migration in this release.
- [ ] Feature flags for new behavior are identified so features can be neutralized without a redeploy.

## 5. Monitoring and alerts

- [ ] Dashboards for affected modules and domain-event metrics (thesis_formed_total, decision_made_total, capital_mission_opened_total, ...) are in place and confirmed reporting.
- [ ] New alerts added / thresholds adjusted for changed behavior; on-call knows what "healthy" looks like post-release. **(blocker)**
- [ ] `/health/ready` for affected containers verified in staging.
- [ ] Error-rate, latency, and key domain-event baselines noted so post-release anomalies are detectable.

## 6. Security and compliance

- [ ] Any authn/authz or brokerage-credential changes in this release carried security-reviewer sign-off. **(blocker)**
- [ ] No secrets introduced; credential handling changes verified.

## 7. Communication

- [ ] Stakeholders informed of release window and user-visible changes.
- [ ] Support/relevant channels briefed on new behavior and known limitations.
- [ ] Release notes published.

## 8. Post-release verification

- [ ] Smoke-test the critical journeys in production (form a Thesis, record a Decision, open a Capital Mission).
- [ ] Confirm metrics, traces, and logs flow for the new/changed paths.
- [ ] Watch dashboards for the agreed soak window before declaring the release stable.

## 9. Learning / retrospective

- [ ] A Learning Event is recorded for what shipped and how the release went. **(blocker)**
- [ ] Retro scheduled if the release was large, incident-prone, or introduced significant new architecture.
- [ ] Any follow-on issues (deferred work, discovered debt, alert gaps) are filed and linked.

## Sign-off

- [ ] Release owner: all applicable items satisfied; blockers resolved. [name / date]
- [ ] Second approver (for production): [name / date]
