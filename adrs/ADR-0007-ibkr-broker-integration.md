# ADR-0007: Interactive Brokers (IBKR) as the Initial Broker Integration

**Status:** Accepted

## Context

To move from analysis to action and to reflect real holdings, Aegis must integrate with at least one brokerage. Supporting many brokers at once dilutes focus and multiplies integration and compliance surface. The company should integrate deeply with one credible broker first, chosen for breadth of instruments, programmatic access, and suitability for serious individual investors.

The founder has chosen Interactive Brokers (IBKR) as the first integration. IBKR offers broad market access and a mature programmatic interface appropriate for long-term public equity investing.

## Decision

**Interactive Brokers (IBKR)** is the initial broker integration for Aegis.

The integration is built behind a clear domain boundary so that IBKR is the first implementation of a broker capability, not a hard-coded assumption throughout the system.

## Consequences

- V1 integrates with IBKR only. Support for additional brokers is deferred and would follow the standard lifecycle.
- Broker interaction is abstracted at the domain boundary so that additional brokers can be added later without rewriting core domains.
- Aegis depends on IBKR's programmatic interface and its constraints; those constraints are documented and isolated within the broker integration.
- Nothing about the IBKR integration may leak broker-specific assumptions into the Portfolio, Holding, or Decision domains.
