"""Application composition root for the Aegis API service.

Wires configuration, logging, the database engine, middleware, exception
handlers, and the thesis module's router into a FastAPI application. Schema is
created via SQLAlchemy metadata at startup (Alembic migrations are deferred per
ADR-0015).
"""

from __future__ import annotations

import logging
import uuid
from collections.abc import Awaitable, Callable
from contextlib import asynccontextmanager
from typing import AsyncIterator

from fastapi import FastAPI, Request, Response
from fastapi.middleware.cors import CORSMiddleware

from .config import Settings, load_settings
from .db import create_all, create_db_engine, create_session_factory
from .errors import register_exception_handlers
from .logging_config import configure_logging

# Importing the ORM module registers ThesisRow on Base.metadata so create_all
# can build the table. Kept explicit rather than relying on import side effects
# happening elsewhere.
from .modules.thesis.adapters import orm as _thesis_orm  # noqa: F401
from .modules.thesis.adapters.api import router as thesis_router

_logger = logging.getLogger("aegis.api")

_TRACE_HEADER = "X-Trace-Id"


def create_app(settings: Settings | None = None) -> FastAPI:
    """Create and configure the FastAPI application."""
    settings = settings or load_settings()
    configure_logging(settings.log_level)

    engine = create_db_engine(settings.database_url)
    session_factory = create_session_factory(engine)

    @asynccontextmanager
    async def lifespan(app: FastAPI) -> AsyncIterator[None]:
        create_all(engine)
        _logger.info("api_started", extra={"config": settings.redacted})
        yield

    app = FastAPI(
        title="Aegis API",
        version="0.1.0",
        summary="Investment Thesis walking skeleton (RFC-0001 / ADR-0015).",
        lifespan=lifespan,
    )
    app.state.settings = settings
    app.state.engine = engine
    app.state.session_factory = session_factory

    # The web tier (apps/web) runs on a different origin (port 3000) and calls
    # this API directly from the browser, so CORS must be explicit. Origins are
    # configured, never hardcoded beyond the local-dev default (see config.py).
    app.add_middleware(
        CORSMiddleware,
        allow_origins=list(settings.cors_origins),
        allow_credentials=False,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    @app.middleware("http")
    async def trace_id_middleware(
        request: Request, call_next: Callable[[Request], Awaitable[Response]]
    ) -> Response:
        # Placeholder correlation id per request; full OpenTelemetry trace
        # propagation is deferred per ADR-0015.
        trace_id = request.headers.get(_TRACE_HEADER) or uuid.uuid4().hex
        request.state.trace_id = trace_id
        response = await call_next(request)
        response.headers[_TRACE_HEADER] = trace_id
        return response

    register_exception_handlers(app)

    @app.get("/health", tags=["ops"])
    def health() -> dict[str, str]:
        """Liveness signal for operators and Compose healthchecks."""
        return {"status": "ok"}

    app.include_router(thesis_router)
    return app


app = create_app()
