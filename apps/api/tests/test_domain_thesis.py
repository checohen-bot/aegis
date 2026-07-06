"""Unit tests for the Investment Thesis domain aggregate.

These construct real domain objects (never mocks) and assert on real invariants,
lifecycle transitions, and emitted domain events, per the testing standards.
"""

from __future__ import annotations

from datetime import datetime, timezone

import pytest

from aegis_api.modules.thesis.domain import (
    InvalidConvictionLevelError,
    InvalidThesisStatementError,
    InvalidThesisTransitionError,
    ThesisActivated,
    ThesisFormed,
    ThesisInvalidated,
    ThesisRequiresFalsificationConditionError,
    ThesisStatus,
)

from .factories import FIXED_NOW, make_thesis

LATER = datetime(2026, 8, 1, 9, 0, 0, tzinfo=timezone.utc)


def test_forming_a_thesis_without_a_falsification_condition_is_rejected() -> None:
    with pytest.raises(ThesisRequiresFalsificationConditionError):
        make_thesis(falsification_conditions=[])


def test_forming_a_thesis_with_a_condition_succeeds_and_starts_in_draft() -> None:
    thesis = make_thesis()

    assert thesis.status is ThesisStatus.DRAFT
    assert len(thesis.falsification_conditions) == 1


def test_forming_a_thesis_emits_a_thesis_formed_event() -> None:
    thesis = make_thesis()

    events = thesis.pull_events()

    assert len(events) == 1
    event = events[0]
    assert isinstance(event, ThesisFormed)
    assert event.thesis_id == thesis.thesis_id.value
    assert event.falsification_condition_count == 1
    assert event.occurred_at == FIXED_NOW


def test_pulling_events_clears_them() -> None:
    thesis = make_thesis()

    thesis.pull_events()

    assert thesis.pull_events() == []


def test_a_statement_that_is_too_short_is_rejected() -> None:
    with pytest.raises(InvalidThesisStatementError):
        make_thesis(thesis_statement="too short")


def test_an_empty_statement_is_rejected() -> None:
    with pytest.raises(InvalidThesisStatementError):
        make_thesis(thesis_statement="   ")


def test_conviction_level_outside_one_to_five_is_rejected() -> None:
    with pytest.raises(InvalidConvictionLevelError):
        make_thesis(conviction_level=6)


def test_activating_a_draft_thesis_moves_it_to_active() -> None:
    thesis = make_thesis()
    thesis.pull_events()

    thesis.activate(LATER)

    assert thesis.status is ThesisStatus.ACTIVE
    assert thesis.last_reviewed_at == LATER


def test_activating_emits_a_thesis_activated_event() -> None:
    thesis = make_thesis()
    thesis.pull_events()

    thesis.activate(LATER)
    events = thesis.pull_events()

    assert len(events) == 1
    assert isinstance(events[0], ThesisActivated)
    assert events[0].occurred_at == LATER


def test_activating_an_already_active_thesis_is_an_invalid_transition() -> None:
    thesis = make_thesis()
    thesis.activate(LATER)

    with pytest.raises(InvalidThesisTransitionError):
        thesis.activate(LATER)


def test_invalidating_a_draft_thesis_without_activating_is_rejected() -> None:
    thesis = make_thesis()

    with pytest.raises(InvalidThesisTransitionError):
        thesis.invalidate("condition met", LATER)


def test_invalidating_an_active_thesis_records_the_condition_met() -> None:
    thesis = make_thesis()
    thesis.activate(LATER)
    thesis.pull_events()

    thesis.invalidate("ROIC fell below cost of capital for four quarters.", LATER)

    assert thesis.status is ThesisStatus.INVALIDATED
    assert thesis.invalidation_condition_met == (
        "ROIC fell below cost of capital for four quarters."
    )


def test_invalidating_emits_a_thesis_invalidated_event_with_the_condition() -> None:
    thesis = make_thesis()
    thesis.activate(LATER)
    thesis.pull_events()

    thesis.invalidate("Catalyst failed to materialize.", LATER)
    events = thesis.pull_events()

    assert len(events) == 1
    assert isinstance(events[0], ThesisInvalidated)
    assert events[0].condition_met == "Catalyst failed to materialize."


def test_invalidation_requires_a_non_empty_condition() -> None:
    thesis = make_thesis()
    thesis.activate(LATER)

    with pytest.raises(InvalidThesisStatementError):
        thesis.invalidate("   ", LATER)


def test_invalidating_an_invalidated_thesis_is_an_invalid_transition() -> None:
    thesis = make_thesis()
    thesis.activate(LATER)
    thesis.invalidate("condition", LATER)

    with pytest.raises(InvalidThesisTransitionError):
        thesis.invalidate("again", LATER)
