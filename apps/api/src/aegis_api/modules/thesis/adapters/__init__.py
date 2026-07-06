"""Investment Thesis adapters layer — inbound/outbound infrastructure.

Contains the SQLAlchemy repository, the ORM row, and the FastAPI router. This is
the only layer permitted to touch vendor types (SQLAlchemy, FastAPI, Pydantic).
"""

from __future__ import annotations

from .api import router
from .orm import ThesisRow
from .repository import SqlAlchemyThesisRepository

__all__ = ["router", "ThesisRow", "SqlAlchemyThesisRepository"]
