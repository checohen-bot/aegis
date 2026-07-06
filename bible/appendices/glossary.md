# Glossary

This glossary is the authoritative definition of Aegis's canonical domain objects and key methodology terms. The canonical domain object names are frozen (see ADR-0013) and are used exactly as written here, in code, documentation, conversation, and AI. Where a definition changes, it changes only through the standard development lifecycle, with the Engineering Bible updated accordingly.

## Canonical Domain Objects

### Portfolio
A Portfolio is an individual investor's collection of investments managed as a coherent whole. It aggregates Holdings and provides the context — objectives, constraints, and composition — against which allocation Decisions are evaluated. A Portfolio is the top-level unit through which an investor sees and directs their capital in Aegis.

### Holding
A Holding is a specific position in a Company held within a Portfolio. It records what is owned and connects the position to its Investment Thesis and the Decisions that established and changed it. A Holding is the link between an investor's actual position and the reasoning that justifies it.

### Company
A Company is a public business that can be analyzed and invested in. It is the subject of research, Evidence, and Observations, and the entity a Holding is a position in. In V1, Companies are public equity issuers; the concept is modeled to remain meaningful as Aegis extends to other capital allocation domains.

### Investment Thesis
An Investment Thesis is the reasoned argument for why a particular investment is expected to be a good allocation of capital. It states the belief, the reasoning behind it, and the conditions under which it holds or fails. Every investment has a thesis, and every thesis is grounded in Evidence.

### Investment Case
An Investment Case is the structured, comprehensive assembly of an investment's reasoning: the Investment Thesis together with its supporting Evidence, Observations, Risks, Catalysts, and the reasoning that connects them. It is the complete, explainable record that justifies a Decision and can be audited later. Where the Thesis is the argument, the Investment Case is the full dossier around it.

### Evidence
Evidence is a verifiable fact or source that supports or challenges an Investment Thesis. It carries provenance — where it came from and when — so that any conclusion can be traced back to its basis. Every thesis has Evidence, and no recommendation is made without it.

### Observation
An Observation is a discrete, recorded noticing about a Company, market, or situation, derived from Evidence or analysis. Observations are the intermediate units of understanding that feed into an Investment Case and may accumulate into Knowledge. An Observation is smaller and more atomic than a Thesis; it is something noticed and recorded, not yet a full argument.

### Knowledge
Knowledge is durable, structured understanding accumulated by Aegis over time from Evidence, Observations, Decisions, and Learning Events. It is the institutional memory that lets the system reason better with each cycle rather than starting fresh. Knowledge is what compounds, and its compounding is central to Adaptive Quality Investing.

### Decision
A Decision is a recorded act of capital allocation reasoning — for example, to establish, increase, reduce, or exit a Holding, or to refrain from acting. Each Decision references the Investment Case that justifies it and is auditable after the fact. In Aegis, the quality of Decisions, not the accuracy of predictions, is the measure of success.

### Capital Mission
A Capital Mission is the investor's overarching purpose and mandate for their capital: what the capital is for, over what horizon, and under what constraints and objectives. It provides the frame within which Portfolios are constructed and Decisions are judged for fit. A Capital Mission connects an individual's goals to the allocation choices Aegis helps them reason about.

### Risk
A Risk is an identified way in which an Investment Thesis could fail or an investment could impair capital. Risks are explicit, recorded elements of an Investment Case, weighed in Decisions rather than left implicit. Naming Risks openly is part of the rigor that earns trust.

### Catalyst
A Catalyst is an identified event or condition that could materially advance or invalidate an Investment Thesis. Catalysts are recorded so that the conditions expected to move a thesis are explicit and can be monitored. A Catalyst is the counterpart to a Risk: what could make the thesis work, or confirm that it is playing out.

### Learning Event
A Learning Event is a recorded instance in which an outcome, a review, or new Evidence produces an improvement in reasoning. It is the mechanism by which Decisions and their results are converted into Knowledge. Learning Events make the "Adaptive" in Adaptive Quality Investing concrete and are the final, non-skippable step of the development and investment lifecycles.

### Behavior Profile
A Behavior Profile is the recorded understanding of an individual investor's tendencies, preferences, and behavioral patterns, including biases that affect decision quality. It lets Aegis adapt its guidance to the person and help them make better Decisions than they would unaided. A Behavior Profile is used to improve decision quality, never to encourage activity for its own sake.

### Policy
A Policy is an explicit rule or constraint that governs allocation behavior within a Portfolio or across the system — for example, limits, guardrails, or standing conditions an investor sets. Policies make constraints machine-checkable and auditable so that Decisions can be evaluated against them. A Policy encodes intent as an enforceable rule rather than an informal preference.

## Methodology Terms

### Adaptive Quality Investing (AQI)
Adaptive Quality Investing is Aegis's investment philosophy. Its north star is decision quality, not prediction accuracy: Aegis does not predict markets or prices, but improves how capital allocation decisions are reasoned, evidenced, explained, and audited. "Adaptive" reflects continuous learning from outcomes and from the investor, so that reasoning improves over time. Its principles are that every recommendation is explainable, every investment has a thesis, every thesis has evidence, every decision is auditable, and knowledge and trust compound.

### Decision Quality
Decision Quality is the standard by which Aegis judges investment reasoning: whether a Decision was well-reasoned, evidence-backed, explainable, consistent with its Investment Thesis, and appropriate to the investor's Capital Mission. It is assessed independently of outcome, because good Decisions can have poor results and vice versa. Decision Quality is the controllable variable that compounds, which is why it, not prediction, is the measure of success.

### Institutional Memory
Institutional Memory is the durable, structured record of everything Aegis has reasoned, decided, and learned — Evidence, Observations, Decisions, Knowledge, and Learning Events — preserved so that nothing consequential is forgotten. It is what lets an individual investor benefit from the accumulated reasoning that professional institutions normally reserve for themselves. In this repository, the Engineering Bible and the ADRs are the institutional memory of the engineering organization itself.

### Explainability
Explainability is the requirement that every recommendation Aegis makes can be understood and traced to its reasoning and Evidence. It is layered in keeping with the brand: a plain answer on the surface, with full reasoning and provenance one step away. Explainability is non-negotiable; a recommendation that cannot be explained is not made.
