# Engineer Onboarding

*Volume IX — Execution Playbook · Chapter 6*

This chapter is the path a new engineer walks in their first week at Aegis. It is deliberately reading-heavy and code-light, because the company's founding philosophy is that the engineering foundation precedes business code. A new engineer's job in week one is not to ship a feature; it is to absorb how Aegis thinks, prove their environment works, and make one small, real contribution to the foundation itself. Everything here is consistent with that philosophy: understand before you build, and build the foundation before the product.

## Day 1–2: Read, In Order

Read the following in exactly this order. The order matters — each document assumes the ones before it. Do not skim; these are the source of the company's coherence.

1. **README.md** — what Aegis is at a glance, how the repository is organized, and how to get the environment running. Orientation only.
2. **CLAUDE.md** — how work is done in this repository, including conventions that both human and AI contributors follow. This tells you the *operating rules* of the repo.
3. **FOUNDER.md** — the authority split you will operate under: the founder owns vision, product, philosophy, terminology, and architecture direction; engineering owns implementation, testing, repository, infrastructure, CI/CD, and documentation. Internalize this boundary before you touch anything — it governs what is yours to decide and what is not.
4. **`bible/00-founder-manifesto`** — the *why* of Aegis and Adaptive Quality Investing. This is the philosophical bedrock. If you understand nothing else deeply in week one, understand this.
5. **`bible/03-domain`** — the canonical domain objects (Portfolio, Holding, Company, Investment Thesis, Investment Case, Evidence, Observation, Knowledge, Decision, Capital Mission, Risk, Catalyst, Learning Event, Behavior Profile, Policy). Learn the *meanings* and the *names*. Terminology is owned by the founder and is non-negotiable; using the wrong word for a concept is a real error here, not a style preference.
6. **The volume relevant to your work** — for architecture work, Volume IV (System Architecture); for AI work, Volume V (Capabilities Not Models); for execution and process, this Volume IX. Read the whole volume you will be working in before you change anything in its area.

By the end of day two you should be able to explain, in domain language, what Aegis is for and what any canonical object means — without looking it up.

## Day 2–3: Stand Up the Environment

Aegis develops on a **Docker-based** environment so that "works on my machine" is never an excuse and onboarding is reproducible. Expectations:

- The entire local stack (application, PostgreSQL, Redis) starts from the single documented command in the README. If it does not start cleanly for you, that is a foundation defect — file it, because the next engineer will hit it too.
- You do not install language-specific dependencies globally or hand-configure services; the container definitions are the source of truth.
- You run the test suite and the CI checks locally and see them pass before you consider your environment ready. Green locally is the baseline; the pipeline is the authority.

A working environment means: the stack is up, the tests pass, and you have run the same checks CI runs. Confirm all three before moving on.

## Day 3–5: Your First Contribution

Your first meaningful contribution will almost certainly **not be application code.** At this stage there is little or no business code to change — and that is intentional. The foundation comes first. Your first contribution is most likely one of:

- **A small RFC** — proposing a refinement to a process, a standard, or the shape of an upcoming slice. Writing an RFC teaches you the lifecycle (Chapter 2) from the inside and produces something the company actually uses.
- **A documentation improvement** — clarifying a Bible passage you found ambiguous while reading, tightening a standard, or fixing a gap in the onboarding path you just walked. You have fresh eyes exactly once; spend them on the docs while the confusion is still visible to you.

This is not busywork and it is not hazing. It is the genuine work of Phase 0 (see the roadmap): the foundation is the product right now. A well-argued RFC or a clarifying documentation change raises the floor for everyone who builds on it later, and it is judged by the same Definition of Done (Chapter 5) as any code — architectural consistency, decision quality, repository quality, maintainability, explainability, trust.

## How You Will Be Judged in Week One

Not by lines of code, commits, or speed — those are explicitly rejected as measures (Chapter 5). You will be judged by whether you understood the philosophy, respected the terminology and the authority split, got a reproducible environment running, and made one small contribution that left the repository clearer than you found it. Do that, and you have started exactly the way Aegis is meant to be built: foundation first, meaning before mechanism, quality over volume.
