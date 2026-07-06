"""Test factories that build real, valid domain objects.

Per the testing standards, domain objects are constructed through explicit
factories with sensible defaults — never mocked. These build genuine
``InvestmentThesis`` aggregates so tests exercise real invariants.
"""

from __future__ import annotations

from collections.abc import Sequence
from datetime import datetime, timezone

from aegis_api.modules.thesis.domain import (
    ConvictionLevel,
    FalsificationCondition,
    InvestmentThesis,
    ThesisId,
)

FIXED_NOW = datetime(2026, 7, 6, 12, 0, 0, tzinfo=timezone.utc)


def make_thesis(
    *,
    thesis_statement: str = (
        "Acme Corp will sustain returns on capital above its cost of capital "
        "because of a durable distribution advantage."
    ),
    falsification_conditions: Sequence[str] | None = (
        "Return on invested capital falls below the cost of capital for four "
        "consecutive quarters.",
    ),
    conviction_level: int = 4,
    now: datetime = FIXED_NOW,
) -> InvestmentThesis:
    """Build a valid draft Thesis with overridable fields.

    Pass ``falsification_conditions=[]`` (or an empty tuple) to exercise the
    missing-condition invariant.
    """
    conditions = [
        FalsificationCondition(text)
        for text in (falsification_conditions or [])
    ]
    return InvestmentThesis.form(
        thesis_id=ThesisId.generate(),
        company_ref="company:acme",
        author_ref="author:analyst-1",
        thesis_statement=thesis_statement,
        rationale="Distribution network is hard to replicate within the horizon.",
        key_assumptions=["Incumbent distribution remains a moat."],
        falsification_conditions=conditions,
        time_horizon="3y",
        conviction_level=ConvictionLevel.from_int(conviction_level),
        now=now,
    )
