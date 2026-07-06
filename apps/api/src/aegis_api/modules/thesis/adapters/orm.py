"""SQLAlchemy ORM model for persisting Investment Theses.

This is an infrastructure detail — a persistence row, NOT the domain aggregate.
The repository maps between this row and the pure-Python ``InvestmentThesis``.
The domain layer never imports this module.
"""

from __future__ import annotations

from datetime import datetime

from sqlalchemy import JSON, DateTime, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from ....db import Base


class ThesisRow(Base):
    """Persistence row for one Investment Thesis, owned by the thesis schema."""

    __tablename__ = "theses"

    thesis_id: Mapped[str] = mapped_column(String(36), primary_key=True)
    company_ref: Mapped[str] = mapped_column(String(255), nullable=False)
    author_ref: Mapped[str] = mapped_column(String(255), nullable=False)
    thesis_statement: Mapped[str] = mapped_column(Text, nullable=False)
    rationale: Mapped[str] = mapped_column(Text, nullable=False)
    key_assumptions: Mapped[list[str]] = mapped_column(JSON, nullable=False)
    falsification_conditions: Mapped[list[str]] = mapped_column(JSON, nullable=False)
    time_horizon: Mapped[str] = mapped_column(String(255), nullable=False)
    conviction_level: Mapped[int] = mapped_column(Integer, nullable=False)
    status: Mapped[str] = mapped_column(String(32), nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    last_reviewed_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True), nullable=True
    )
    invalidation_condition_met: Mapped[str | None] = mapped_column(
        Text, nullable=True
    )
