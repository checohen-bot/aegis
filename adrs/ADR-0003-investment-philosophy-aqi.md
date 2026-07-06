# ADR-0003: Investment Philosophy is Adaptive Quality Investing (AQI)

**Status:** Accepted

## Context

An investment intelligence platform must declare what it believes good investing is, because that belief determines what the system optimizes, measures, and rewards. Much of the industry optimizes for prediction — forecasting prices, timing markets, and chasing returns. Prediction is noisy, hard to attribute, and encourages overconfidence.

The founder rejects prediction as the objective. The alternative is to optimize the **quality of the decision** itself: was it well-reasoned, evidence-backed, explainable, and consistent with a stated thesis? A high-quality decision can have a poor outcome and a low-quality decision a good one; over time, decision quality is the controllable variable that compounds.

## Decision

The investment philosophy of Aegis is **Adaptive Quality Investing (AQI)**. Decision quality, not prediction accuracy, is the north star.

The following principles are binding:

- Aegis does not predict markets or prices.
- Every recommendation must be explainable.
- Every investment has a thesis.
- Every thesis has evidence.
- Every decision is auditable.
- Knowledge and trust compound over time.

"Adaptive" means the system learns from outcomes and from the investor, continuously improving the quality of reasoning rather than the accuracy of forecasts.

## Consequences

- Success is measured by decision quality and process integrity, not by return prediction accuracy.
- The domain model is built around theses, evidence, decisions, and learning — not around price forecasts or signals.
- Any feature that implies market or price prediction is out of scope and contradicts the philosophy.
- Explainability and auditability are non-negotiable requirements of every recommendation, not optional features.
- The system must capture outcomes and learning so that quality improves over time.
