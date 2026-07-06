"""Value objects for the Investment Thesis aggregate.

Value objects are immutable and defined entirely by their attributes. They are
pure Python: no framework, ORM, or provider imports are permitted here.
"""

from __future__ import annotations

import uuid
from dataclasses import dataclass
from enum import Enum

from .exceptions import (
    InvalidConvictionLevelError,
    InvalidFalsificationConditionError,
    InvalidThesisIdError,
)


@dataclass(frozen=True, slots=True)
class ThesisId:
    """Stable, opaque identity for an Investment Thesis.

    Wraps a UUID string rather than passing a bare ``str`` around, so the type
    system distinguishes a Thesis identity from any other identifier.
    """

    value: str

    def __post_init__(self) -> None:
        try:
            uuid.UUID(self.value)
        except (ValueError, AttributeError, TypeError) as exc:
            raise InvalidThesisIdError(
                f"ThesisId must be a valid UUID string, got {self.value!r}"
            ) from exc

    @classmethod
    def generate(cls) -> ThesisId:
        """Mint a fresh, random Thesis identity."""
        return cls(str(uuid.uuid4()))

    def __str__(self) -> str:
        return self.value


@dataclass(frozen=True, slots=True)
class FalsificationCondition:
    """An observable condition under which the Thesis would be considered wrong.

    A Thesis is only a Thesis if it can be falsified; each condition must carry
    real, non-empty text describing what would refute the claim.
    """

    text: str

    def __post_init__(self) -> None:
        if not self.text or not self.text.strip():
            raise InvalidFalsificationConditionError(
                "A falsification condition must be non-empty text."
            )


class ConvictionLevel(Enum):
    """The author's current strength of belief, as a bounded ordinal (1-5).

    Modeled as an ordinal enum so conviction cannot take an arbitrary numeric
    value; it is one of five defined strengths.
    """

    VERY_LOW = 1
    LOW = 2
    MODERATE = 3
    HIGH = 4
    VERY_HIGH = 5

    @classmethod
    def from_int(cls, value: int) -> ConvictionLevel:
        """Build a ConvictionLevel from a 1-5 integer, rejecting out-of-range input."""
        try:
            return cls(value)
        except ValueError as exc:
            raise InvalidConvictionLevelError(
                f"conviction_level must be an integer 1-5, got {value!r}"
            ) from exc


class ThesisStatus(Enum):
    """Lifecycle state of an Investment Thesis.

    See ``bible/03-domain/investment-thesis.md`` for the full lifecycle. The
    walking skeleton exercises DRAFT -> ACTIVE -> INVALIDATED; the remaining
    states are defined here so the enum is complete and future transitions do
    not require renaming.
    """

    DRAFT = "draft"
    ACTIVE = "active"
    UNDER_REVIEW = "under_review"
    CONFIRMED = "confirmed"
    INVALIDATED = "invalidated"
    RETIRED = "retired"
