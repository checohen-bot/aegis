"""The Investment Thesis aggregate root.

An Investment Thesis is a single, explicit, falsifiable claim about a Company.
This is a pure-Python aggregate: it enforces its own invariants, owns its
lifecycle transitions, and records domain events. It is NOT a SQLAlchemy model;
persistence is handled by a repository in the adapters layer that maps to and
from this object.

Invariants enforced here (see bible/03-domain/investment-thesis.md):
  - A Thesis must state at least one falsification condition, or it cannot exist.
  - The thesis_statement must be non-empty and long enough to read as a claim.
  - Lifecycle transitions follow draft -> active -> {invalidated, ...}; illegal
    transitions raise InvalidThesisTransitionError.
"""

from __future__ import annotations

from collections.abc import Sequence
from datetime import datetime

from .events import DomainEvent, ThesisActivated, ThesisFormed, ThesisInvalidated
from .exceptions import (
    InvalidThesisStatementError,
    InvalidThesisTransitionError,
    ThesisRequiresFalsificationConditionError,
)
from .value_objects import (
    ConvictionLevel,
    FalsificationCondition,
    ThesisId,
    ThesisStatus,
)

# A statement shorter than this is treated as too terse to be a real claim. This
# is a deliberately simple check; NLP claim-detection is explicitly out of scope
# for the skeleton (see the task brief and domain model Invariants).
_MIN_STATEMENT_LENGTH = 10


class InvestmentThesis:
    """Aggregate root for one falsifiable claim about a Company.

    Construct new Theses via :meth:`form` (which validates and emits
    ``ThesisFormed``); rebuild persisted ones via :meth:`reconstitute` (which
    validates invariants but emits no events).
    """

    def __init__(
        self,
        *,
        thesis_id: ThesisId,
        company_ref: str,
        author_ref: str,
        thesis_statement: str,
        rationale: str,
        key_assumptions: Sequence[str],
        falsification_conditions: Sequence[FalsificationCondition],
        time_horizon: str,
        conviction_level: ConvictionLevel,
        status: ThesisStatus,
        created_at: datetime,
        last_reviewed_at: datetime | None,
        invalidation_condition_met: str | None = None,
    ) -> None:
        self._validate_statement(thesis_statement)
        self._validate_falsification(falsification_conditions)

        self._thesis_id = thesis_id
        self._company_ref = company_ref
        self._author_ref = author_ref
        self._thesis_statement = thesis_statement
        self._rationale = rationale
        self._key_assumptions = list(key_assumptions)
        self._falsification_conditions = list(falsification_conditions)
        self._time_horizon = time_horizon
        self._conviction_level = conviction_level
        self._status = status
        self._created_at = created_at
        self._last_reviewed_at = last_reviewed_at
        self._invalidation_condition_met = invalidation_condition_met
        self._pending_events: list[DomainEvent] = []

    # -- Construction ----------------------------------------------------------

    @classmethod
    def form(
        cls,
        *,
        thesis_id: ThesisId,
        company_ref: str,
        author_ref: str,
        thesis_statement: str,
        rationale: str,
        key_assumptions: Sequence[str],
        falsification_conditions: Sequence[FalsificationCondition],
        time_horizon: str,
        conviction_level: ConvictionLevel,
        now: datetime,
    ) -> InvestmentThesis:
        """Form a new Thesis in DRAFT state, emitting ``ThesisFormed``.

        The falsification-condition invariant is enforced in ``__init__``, so a
        Thesis can never be formed without at least one condition.
        """
        thesis = cls(
            thesis_id=thesis_id,
            company_ref=company_ref,
            author_ref=author_ref,
            thesis_statement=thesis_statement,
            rationale=rationale,
            key_assumptions=key_assumptions,
            falsification_conditions=falsification_conditions,
            time_horizon=time_horizon,
            conviction_level=conviction_level,
            status=ThesisStatus.DRAFT,
            created_at=now,
            last_reviewed_at=None,
        )
        thesis._record(
            ThesisFormed(
                thesis_id=str(thesis_id),
                occurred_at=now,
                company_ref=company_ref,
                author_ref=author_ref,
                thesis_statement=thesis_statement,
                falsification_condition_count=len(thesis._falsification_conditions),
            )
        )
        return thesis

    @classmethod
    def reconstitute(
        cls,
        *,
        thesis_id: ThesisId,
        company_ref: str,
        author_ref: str,
        thesis_statement: str,
        rationale: str,
        key_assumptions: Sequence[str],
        falsification_conditions: Sequence[FalsificationCondition],
        time_horizon: str,
        conviction_level: ConvictionLevel,
        status: ThesisStatus,
        created_at: datetime,
        last_reviewed_at: datetime | None,
        invalidation_condition_met: str | None,
    ) -> InvestmentThesis:
        """Rebuild a Thesis from persisted state without emitting events."""
        return cls(
            thesis_id=thesis_id,
            company_ref=company_ref,
            author_ref=author_ref,
            thesis_statement=thesis_statement,
            rationale=rationale,
            key_assumptions=key_assumptions,
            falsification_conditions=falsification_conditions,
            time_horizon=time_horizon,
            conviction_level=conviction_level,
            status=status,
            created_at=created_at,
            last_reviewed_at=last_reviewed_at,
            invalidation_condition_met=invalidation_condition_met,
        )

    # -- Invariants ------------------------------------------------------------

    @staticmethod
    def _validate_statement(statement: str) -> None:
        if not statement or not statement.strip():
            raise InvalidThesisStatementError(
                "thesis_statement must be a non-empty claim."
            )
        if len(statement.strip()) < _MIN_STATEMENT_LENGTH:
            raise InvalidThesisStatementError(
                "thesis_statement is too short to read as a claim "
                f"(minimum {_MIN_STATEMENT_LENGTH} characters)."
            )

    @staticmethod
    def _validate_falsification(
        conditions: Sequence[FalsificationCondition],
    ) -> None:
        if len(conditions) == 0:
            raise ThesisRequiresFalsificationConditionError(
                "A Thesis must state at least one falsification condition."
            )

    # -- Lifecycle transitions -------------------------------------------------

    def activate(self, now: datetime) -> None:
        """Transition DRAFT -> ACTIVE, emitting ``ThesisActivated``."""
        if self._status is not ThesisStatus.DRAFT:
            raise InvalidThesisTransitionError(self._status.value, "activate")
        self._status = ThesisStatus.ACTIVE
        self._last_reviewed_at = now
        self._record(ThesisActivated(thesis_id=str(self._thesis_id), occurred_at=now))

    def invalidate(self, condition_met: str, now: datetime) -> None:
        """Transition ACTIVE (or UNDER_REVIEW) -> INVALIDATED.

        Records which falsification condition was met and emits
        ``ThesisInvalidated``. The recorded reason must be non-empty free text.
        """
        if self._status not in (ThesisStatus.ACTIVE, ThesisStatus.UNDER_REVIEW):
            raise InvalidThesisTransitionError(self._status.value, "invalidate")
        if not condition_met or not condition_met.strip():
            raise InvalidThesisStatementError(
                "Invalidation must record which falsification condition was met."
            )
        self._status = ThesisStatus.INVALIDATED
        self._invalidation_condition_met = condition_met
        self._last_reviewed_at = now
        self._record(
            ThesisInvalidated(
                thesis_id=str(self._thesis_id),
                occurred_at=now,
                condition_met=condition_met,
            )
        )

    # -- Events ----------------------------------------------------------------

    def _record(self, event: DomainEvent) -> None:
        self._pending_events.append(event)

    def pull_events(self) -> list[DomainEvent]:
        """Return and clear the events accumulated since the last pull."""
        events = list(self._pending_events)
        self._pending_events.clear()
        return events

    # -- Read-only accessors ---------------------------------------------------

    @property
    def thesis_id(self) -> ThesisId:
        return self._thesis_id

    @property
    def company_ref(self) -> str:
        return self._company_ref

    @property
    def author_ref(self) -> str:
        return self._author_ref

    @property
    def thesis_statement(self) -> str:
        return self._thesis_statement

    @property
    def rationale(self) -> str:
        return self._rationale

    @property
    def key_assumptions(self) -> list[str]:
        return list(self._key_assumptions)

    @property
    def falsification_conditions(self) -> list[FalsificationCondition]:
        return list(self._falsification_conditions)

    @property
    def time_horizon(self) -> str:
        return self._time_horizon

    @property
    def conviction_level(self) -> ConvictionLevel:
        return self._conviction_level

    @property
    def status(self) -> ThesisStatus:
        return self._status

    @property
    def created_at(self) -> datetime:
        return self._created_at

    @property
    def last_reviewed_at(self) -> datetime | None:
        return self._last_reviewed_at

    @property
    def invalidation_condition_met(self) -> str | None:
        return self._invalidation_condition_met
