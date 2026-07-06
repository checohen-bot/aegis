"""Domain events for the Investment Thesis aggregate.

Events are immutable, past-tense facts describing something that happened to a
Thesis. They are real typed objects, never stringly-typed payloads. Other
modules would react to these once they exist; for the walking skeleton they are
emitted (collected on the aggregate and logged) to prove the event convention.
Pure Python: no framework imports.
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime


@dataclass(frozen=True, slots=True)
class DomainEvent:
    """Base class for domain events. ``occurred_at`` is UTC."""

    thesis_id: str
    occurred_at: datetime

    @property
    def event_name(self) -> str:
        return type(self).__name__


@dataclass(frozen=True, slots=True)
class ThesisFormed(DomainEvent):
    """A new Investment Thesis was formed in DRAFT state."""

    company_ref: str
    author_ref: str
    thesis_statement: str
    falsification_condition_count: int


@dataclass(frozen=True, slots=True)
class ThesisActivated(DomainEvent):
    """A Thesis was activated (DRAFT -> ACTIVE) and is now under continuous test."""


@dataclass(frozen=True, slots=True)
class ThesisInvalidated(DomainEvent):
    """A Thesis was invalidated because a falsification condition was met."""

    condition_met: str
