"""Typed domain exceptions for the Investment Thesis aggregate.

Domain code raises these specific exceptions, never bare ``Exception``. The
application and adapter layers translate them into API error envelopes at the
boundary. Pure Python: no framework imports.
"""

from __future__ import annotations


class ThesisError(Exception):
    """Base class for all Investment Thesis domain errors."""


class InvalidThesisIdError(ThesisError):
    """Raised when a ThesisId is constructed from a non-UUID value."""


class InvalidFalsificationConditionError(ThesisError):
    """Raised when a falsification condition carries empty text."""


class InvalidConvictionLevelError(ThesisError):
    """Raised when conviction_level is outside the defined 1-5 ordinal range."""


class ThesisRequiresFalsificationConditionError(ThesisError):
    """Raised when forming a Thesis with no falsification condition.

    Invariant: a claim with no condition under which it could be wrong is not a
    Thesis and cannot be persisted (see the domain model's Invariants section).
    """


class InvalidThesisStatementError(ThesisError):
    """Raised when the thesis_statement is empty or too short to be a claim."""


class ThesisNotFoundError(ThesisError):
    """Raised when a Thesis cannot be found for a given identity."""

    def __init__(self, thesis_id: str) -> None:
        self.thesis_id = thesis_id
        super().__init__(f"No thesis exists with id {thesis_id}")


class InvalidThesisTransitionError(ThesisError):
    """Raised when a lifecycle transition is not permitted from the current state."""

    def __init__(self, current: str, attempted: str) -> None:
        self.current = current
        self.attempted = attempted
        super().__init__(
            f"Cannot {attempted} a thesis in state '{current}'."
        )
