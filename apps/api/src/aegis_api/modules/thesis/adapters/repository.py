"""SQLAlchemy implementation of the ThesisRepository port.

Maps between the pure-domain ``InvestmentThesis`` aggregate and the ``ThesisRow``
persistence model. This is the only place that knows both the domain shape and
the database shape; the mapping is explicit in both directions.
"""

from __future__ import annotations

from datetime import datetime, timezone

from sqlalchemy import select
from sqlalchemy.orm import Session

from ..domain import (
    ConvictionLevel,
    FalsificationCondition,
    InvestmentThesis,
    ThesisId,
    ThesisPage,
    ThesisStatus,
)
from .orm import ThesisRow


def _as_utc(value: datetime | None) -> datetime | None:
    """Normalize a possibly-naive stored datetime to UTC-aware.

    SQLite (used in integration tests) drops tzinfo; PostgreSQL preserves it.
    We treat any naive value as UTC, which is our internal storage convention.
    """
    if value is None:
        return None
    if value.tzinfo is None:
        return value.replace(tzinfo=timezone.utc)
    return value.astimezone(timezone.utc)


class SqlAlchemyThesisRepository:
    """Persists Investment Theses to a relational database via SQLAlchemy."""

    def __init__(self, session: Session) -> None:
        self._session = session

    def add(self, thesis: InvestmentThesis) -> None:
        self._session.add(_to_row(thesis))

    def get(self, thesis_id: ThesisId) -> InvestmentThesis | None:
        row = self._session.get(ThesisRow, thesis_id.value)
        if row is None:
            return None
        return _to_domain(row)

    def save(self, thesis: InvestmentThesis) -> None:
        row = self._session.get(ThesisRow, thesis.thesis_id.value)
        if row is None:
            # Saving an aggregate we never added is a programming error.
            self._session.add(_to_row(thesis))
            return
        _apply_to_row(thesis, row)

    def list(self, *, limit: int, offset: int) -> ThesisPage:
        # Fetch one extra row to determine whether a further page exists.
        stmt = (
            select(ThesisRow)
            .order_by(ThesisRow.created_at.desc(), ThesisRow.thesis_id.desc())
            .offset(offset)
            .limit(limit + 1)
        )
        rows = list(self._session.execute(stmt).scalars().all())
        has_more = len(rows) > limit
        page_rows = rows[:limit]
        next_offset = offset + limit if has_more else None
        return ThesisPage(
            items=[_to_domain(row) for row in page_rows],
            next_offset=next_offset,
        )


def _to_row(thesis: InvestmentThesis) -> ThesisRow:
    return ThesisRow(
        thesis_id=thesis.thesis_id.value,
        company_ref=thesis.company_ref,
        author_ref=thesis.author_ref,
        thesis_statement=thesis.thesis_statement,
        rationale=thesis.rationale,
        key_assumptions=thesis.key_assumptions,
        falsification_conditions=[c.text for c in thesis.falsification_conditions],
        time_horizon=thesis.time_horizon,
        conviction_level=thesis.conviction_level.value,
        status=thesis.status.value,
        created_at=thesis.created_at,
        last_reviewed_at=thesis.last_reviewed_at,
        invalidation_condition_met=thesis.invalidation_condition_met,
    )


def _apply_to_row(thesis: InvestmentThesis, row: ThesisRow) -> None:
    row.company_ref = thesis.company_ref
    row.author_ref = thesis.author_ref
    row.thesis_statement = thesis.thesis_statement
    row.rationale = thesis.rationale
    row.key_assumptions = thesis.key_assumptions
    row.falsification_conditions = [c.text for c in thesis.falsification_conditions]
    row.time_horizon = thesis.time_horizon
    row.conviction_level = thesis.conviction_level.value
    row.status = thesis.status.value
    row.last_reviewed_at = thesis.last_reviewed_at
    row.invalidation_condition_met = thesis.invalidation_condition_met


def _to_domain(row: ThesisRow) -> InvestmentThesis:
    created_at = _as_utc(row.created_at)
    assert created_at is not None  # created_at is non-nullable in the schema
    return InvestmentThesis.reconstitute(
        thesis_id=ThesisId(row.thesis_id),
        company_ref=row.company_ref,
        author_ref=row.author_ref,
        thesis_statement=row.thesis_statement,
        rationale=row.rationale,
        key_assumptions=list(row.key_assumptions),
        falsification_conditions=[
            FalsificationCondition(text) for text in row.falsification_conditions
        ],
        time_horizon=row.time_horizon,
        conviction_level=ConvictionLevel.from_int(row.conviction_level),
        status=ThesisStatus(row.status),
        created_at=created_at,
        last_reviewed_at=_as_utc(row.last_reviewed_at),
        invalidation_condition_met=row.invalidation_condition_met,
    )
