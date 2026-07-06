"""Application use cases for the Investment Thesis module.

Each use case orchestrates one interaction: it loads or builds the aggregate,
invokes domain behavior (which enforces invariants and records events), persists
through the repository port, and publishes the resulting events. Use cases
depend only on domain types and the repository / publisher ports — never on
SQLAlchemy, FastAPI, or any provider SDK.

The clock is injected (``now``) so behavior is deterministic and testable.
"""

from __future__ import annotations

from collections.abc import Callable, Sequence
from dataclasses import dataclass
from datetime import datetime, timezone

from ..domain import (
    ConvictionLevel,
    FalsificationCondition,
    InvestmentThesis,
    ThesisId,
    ThesisNotFoundError,
    ThesisPage,
    ThesisRepository,
)
from .events import EventPublisher

Clock = Callable[[], datetime]


def _utc_now() -> datetime:
    return datetime.now(timezone.utc)


@dataclass(frozen=True, slots=True)
class FormThesisCommand:
    """Inputs required to form a new Investment Thesis."""

    company_ref: str
    author_ref: str
    thesis_statement: str
    rationale: str
    key_assumptions: Sequence[str]
    falsification_conditions: Sequence[str]
    time_horizon: str
    conviction_level: int


class ThesisService:
    """Application service exposing the Investment Thesis use cases.

    Holds the repository and event-publisher ports plus an injectable clock.
    Instantiated per request in the adapter layer with a request-scoped
    repository.
    """

    def __init__(
        self,
        repository: ThesisRepository,
        publisher: EventPublisher,
        clock: Clock = _utc_now,
    ) -> None:
        self._repository = repository
        self._publisher = publisher
        self._clock = clock

    def form_thesis(self, command: FormThesisCommand) -> InvestmentThesis:
        """Form a Thesis in DRAFT state and persist it.

        Domain invariants (>=1 falsification condition, valid statement, 1-5
        conviction) are enforced by the value objects and aggregate, so an
        invalid command never reaches the database.
        """
        now = self._clock()
        conditions = [
            FalsificationCondition(text) for text in command.falsification_conditions
        ]
        thesis = InvestmentThesis.form(
            thesis_id=ThesisId.generate(),
            company_ref=command.company_ref,
            author_ref=command.author_ref,
            thesis_statement=command.thesis_statement,
            rationale=command.rationale,
            key_assumptions=command.key_assumptions,
            falsification_conditions=conditions,
            time_horizon=command.time_horizon,
            conviction_level=ConvictionLevel.from_int(command.conviction_level),
            now=now,
        )
        self._repository.add(thesis)
        self._publisher.publish(thesis.pull_events())
        return thesis

    def activate_thesis(self, thesis_id: str) -> InvestmentThesis:
        """Transition a Thesis DRAFT -> ACTIVE."""
        thesis = self._load(thesis_id)
        thesis.activate(self._clock())
        self._repository.save(thesis)
        self._publisher.publish(thesis.pull_events())
        return thesis

    def invalidate_thesis(
        self, thesis_id: str, condition_met: str
    ) -> InvestmentThesis:
        """Transition a Thesis ACTIVE -> INVALIDATED, recording the met condition."""
        thesis = self._load(thesis_id)
        thesis.invalidate(condition_met, self._clock())
        self._repository.save(thesis)
        self._publisher.publish(thesis.pull_events())
        return thesis

    def get_thesis(self, thesis_id: str) -> InvestmentThesis:
        """Retrieve one Thesis or raise ThesisNotFoundError."""
        return self._load(thesis_id)

    def list_theses(self, *, limit: int, offset: int) -> ThesisPage:
        """Return a page of Theses, newest first."""
        return self._repository.list(limit=limit, offset=offset)

    def _load(self, thesis_id: str) -> InvestmentThesis:
        thesis = self._repository.get(ThesisId(thesis_id))
        if thesis is None:
            raise ThesisNotFoundError(thesis_id)
        return thesis
