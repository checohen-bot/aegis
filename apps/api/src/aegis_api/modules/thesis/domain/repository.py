"""Repository port for the Investment Thesis aggregate.

The domain declares the persistence interface it needs; infrastructure (the
adapters layer) implements it. The domain never depends on SQLAlchemy, HTTP, or
any vendor type. This is the dependency-inversion boundary: application code
orchestrates use cases against this Protocol, not against a concrete database.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Protocol

from .entities import InvestmentThesis
from .value_objects import ThesisId


@dataclass(frozen=True, slots=True)
class ThesisPage:
    """A single page of Theses plus the cursor to fetch the next one.

    ``next_offset`` is ``None`` when there are no further items. The adapter is
    responsible for encoding this into an opaque API cursor.
    """

    items: list[InvestmentThesis]
    next_offset: int | None


class ThesisRepository(Protocol):
    """Persistence port for Investment Theses."""

    def add(self, thesis: InvestmentThesis) -> None:
        """Persist a newly formed Thesis."""
        ...

    def get(self, thesis_id: ThesisId) -> InvestmentThesis | None:
        """Return the Thesis with this identity, or ``None`` if absent."""
        ...

    def save(self, thesis: InvestmentThesis) -> None:
        """Persist changes to an existing Thesis (e.g. after a transition)."""
        ...

    def list(self, *, limit: int, offset: int) -> ThesisPage:
        """Return a page of Theses ordered by creation time (newest first)."""
        ...
