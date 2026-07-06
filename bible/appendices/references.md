# References

This is a living document. It records the categories of external reference material the team should track and consult, not a fixed bibliography. It is maintained through the standard development lifecycle: when a body of reference material becomes relevant to a decision or implementation, add or refine its category here, and cite specific sources within the RFC, ADR, or standard that relies on them.

No fabricated links appear in this document. Specific URLs, document versions, and citations belong in the artifact that depends on them, where they can be pinned and reviewed. Below are the categories the team is expected to track.

## Reference Categories

### Regulatory filings and disclosure data
Primary-source corporate disclosures for public equities, including the U.S. Securities and Exchange Commission's filings and the EDGAR system. These are the authoritative source of Evidence about a Company's financials, risks, and governance. Team members working on Company research and Evidence ingestion should track the relevant filing types, their schedules, and the access mechanisms for the disclosure systems.

### Broker integration documentation
The official Interactive Brokers (IBKR) developer and API documentation, covering authentication, account and position data, and the programmatic interfaces Aegis integrates with (see ADR-0007). This documentation governs how the broker capability is implemented and must be tracked for version changes, deprecations, and constraints. Broker-specific details are isolated within the integration and cited there.

### Accounting and reporting standards
The accounting standards that give financial statements their meaning, including U.S. Generally Accepted Accounting Principles (US GAAP) and International Financial Reporting Standards (IFRS), along with the bodies that maintain them. Correct interpretation of Evidence drawn from financial statements depends on understanding the standards under which they were prepared. The team tracks the applicable standards and material changes to them.

### Evidence-based and decision-quality investing literature
The body of work on evidence-based investing, decision quality, and the separation of process from outcome that underpins Adaptive Quality Investing (see ADR-0003). This includes literature on decision analysis, behavioral finance and investor biases (relevant to the Behavior Profile), and the discipline of judging decisions by their quality rather than their results. This literature informs methodology rather than implementation and is cited within the Bible sections and RFCs it supports.

### Engineering and observability references
Authoritative documentation for the core technology stack and practices fixed by ADR-0011, including OpenTelemetry specifications and the official documentation for Python, TypeScript, Next.js, React, PostgreSQL, Redis, and Docker. Standards in `/standards` that depend on these references cite the specific versions they target.

## Maintaining this page
When a decision, RFC, or standard introduces a meaningful dependency on external material, ensure its category is represented here and place the precise, versioned citation in that artifact. Keep this page a durable map of what to consult, and let the citing documents carry the specifics.
