"""Investment Thesis module — the walking-skeleton's first bounded context.

Public surface of the module. Other modules (once they exist) integrate through
the application service and domain events published here, never by reaching into
``domain`` internals.
"""

from __future__ import annotations

from .adapters import router
from .application import FormThesisCommand, ThesisService

__all__ = ["router", "ThesisService", "FormThesisCommand"]
