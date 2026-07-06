"""Investment Thesis domain layer — pure Python, no framework imports.

Public surface of the domain layer. Application and adapter code imports from
here; nothing in this package imports from application or adapters.
"""

from __future__ import annotations

from .entities import InvestmentThesis
from .events import (
    DomainEvent,
    ThesisActivated,
    ThesisFormed,
    ThesisInvalidated,
)
from .exceptions import (
    InvalidConvictionLevelError,
    InvalidFalsificationConditionError,
    InvalidThesisIdError,
    InvalidThesisStatementError,
    InvalidThesisTransitionError,
    ThesisError,
    ThesisNotFoundError,
    ThesisRequiresFalsificationConditionError,
)
from .repository import ThesisPage, ThesisRepository
from .value_objects import (
    ConvictionLevel,
    FalsificationCondition,
    ThesisId,
    ThesisStatus,
)

__all__ = [
    "InvestmentThesis",
    "DomainEvent",
    "ThesisFormed",
    "ThesisActivated",
    "ThesisInvalidated",
    "ThesisError",
    "ThesisNotFoundError",
    "ThesisRequiresFalsificationConditionError",
    "InvalidThesisStatementError",
    "InvalidThesisTransitionError",
    "InvalidThesisIdError",
    "InvalidFalsificationConditionError",
    "InvalidConvictionLevelError",
    "ThesisRepository",
    "ThesisPage",
    "ThesisId",
    "FalsificationCondition",
    "ConvictionLevel",
    "ThesisStatus",
]
