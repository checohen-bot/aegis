"""Database engine, session factory, and declarative base.

Infrastructure concern only: nothing in the domain layer imports from here. The
declarative ``Base`` collects the metadata that ``create_all`` uses at startup
to create tables (Alembic migrations are deferred per ADR-0015).
"""

from __future__ import annotations

from sqlalchemy import Engine, create_engine
from sqlalchemy.orm import DeclarativeBase, Session, sessionmaker


class Base(DeclarativeBase):
    """Declarative base carrying the shared metadata for all ORM models."""


def create_db_engine(database_url: str) -> Engine:
    """Create a SQLAlchemy engine.

    ``pool_pre_ping`` guards against stale connections after the database
    restarts (common with a Compose ``db`` container). SQLite URLs (used by the
    integration test) get the flags they need to be shared across threads.
    """
    connect_args: dict[str, object] = {}
    if database_url.startswith("sqlite"):
        connect_args["check_same_thread"] = False
    return create_engine(
        database_url,
        pool_pre_ping=True,
        future=True,
        connect_args=connect_args,
    )


def create_session_factory(engine: Engine) -> sessionmaker[Session]:
    """Create a session factory bound to the given engine."""
    return sessionmaker(bind=engine, autoflush=False, expire_on_commit=False)


def create_all(engine: Engine) -> None:
    """Create all tables registered on ``Base.metadata`` if absent.

    Import side effect: models must be imported before this runs so their tables
    are registered. ``main`` imports the thesis ORM module before calling this.
    """
    Base.metadata.create_all(engine)
