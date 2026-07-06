"""Event publication port for the application layer.

Use cases publish the domain events an aggregate accumulates. The port keeps the
application layer decoupled from *how* events are delivered. For the walking
skeleton the only implementation is a structured-logging publisher (a real
message bus / Redis is deferred per ADR-0015); tests use a collecting fake.
"""

from __future__ import annotations

import logging
from collections.abc import Sequence
from typing import Protocol

from ..domain import DomainEvent

_logger = logging.getLogger("aegis.thesis.events")


class EventPublisher(Protocol):
    """Publishes domain events raised by the Investment Thesis aggregate."""

    def publish(self, events: Sequence[DomainEvent]) -> None:
        """Publish a batch of domain events."""
        ...


class LoggingEventPublisher:
    """Emits each domain event as a structured log line.

    This is the skeleton's stand-in for a real event bus: it proves the
    event-driven convention (typed events, past-tense names) is observable
    without introducing broker infrastructure that no second module consumes yet.
    """

    def publish(self, events: Sequence[DomainEvent]) -> None:
        for event in events:
            _logger.info(
                "domain_event",
                extra={
                    "event": event.event_name,
                    "thesis_id": event.thesis_id,
                    "occurred_at": event.occurred_at.isoformat(),
                },
            )
