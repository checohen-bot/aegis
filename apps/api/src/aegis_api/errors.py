"""API error envelope and exception handlers.

Every error response uses the one envelope defined in standards/api-standards.md:
``{"error": {"code", "message", "details", "traceId"}}``. Domain exceptions are
translated to stable machine codes and appropriate HTTP statuses here, at the
boundary — internal details and stack traces are never surfaced to clients.
"""

from __future__ import annotations

from typing import Any

from fastapi import FastAPI, Request, status
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse

from .modules.thesis.domain import (
    InvalidConvictionLevelError,
    InvalidFalsificationConditionError,
    InvalidThesisIdError,
    InvalidThesisStatementError,
    InvalidThesisTransitionError,
    ThesisNotFoundError,
    ThesisRequiresFalsificationConditionError,
)


def _trace_id(request: Request) -> str:
    return getattr(request.state, "trace_id", "unknown")


def _envelope(
    *,
    code: str,
    message: str,
    trace_id: str,
    details: list[dict[str, Any]] | None = None,
    http_status: int,
) -> JSONResponse:
    return JSONResponse(
        status_code=http_status,
        content={
            "error": {
                "code": code,
                "message": message,
                "details": details or [],
                "traceId": trace_id,
            }
        },
    )


def register_exception_handlers(app: FastAPI) -> None:
    """Wire domain and validation exceptions to the standard error envelope."""

    @app.exception_handler(ThesisNotFoundError)
    async def _not_found(
        request: Request, exc: ThesisNotFoundError
    ) -> JSONResponse:
        return _envelope(
            code="THESIS_NOT_FOUND",
            message=str(exc),
            trace_id=_trace_id(request),
            details=[{"field": "thesisId", "issue": "unknown identifier"}],
            http_status=status.HTTP_404_NOT_FOUND,
        )

    @app.exception_handler(InvalidThesisTransitionError)
    async def _bad_transition(
        request: Request, exc: InvalidThesisTransitionError
    ) -> JSONResponse:
        # A transition that is illegal for the aggregate's current state is a
        # conflict with the persisted state, not a malformed request.
        return _envelope(
            code="INVALID_THESIS_TRANSITION",
            message=str(exc),
            trace_id=_trace_id(request),
            details=[
                {"field": "status", "issue": f"current state is '{exc.current}'"}
            ],
            http_status=status.HTTP_409_CONFLICT,
        )

    @app.exception_handler(ThesisRequiresFalsificationConditionError)
    @app.exception_handler(InvalidThesisStatementError)
    @app.exception_handler(InvalidFalsificationConditionError)
    @app.exception_handler(InvalidConvictionLevelError)
    @app.exception_handler(InvalidThesisIdError)
    async def _domain_validation(
        request: Request, exc: Exception
    ) -> JSONResponse:
        return _envelope(
            code="THESIS_VALIDATION_FAILED",
            message=str(exc),
            trace_id=_trace_id(request),
            http_status=status.HTTP_422_UNPROCESSABLE_ENTITY,
        )

    @app.exception_handler(RequestValidationError)
    async def _request_validation(
        request: Request, exc: RequestValidationError
    ) -> JSONResponse:
        details = [
            {
                "field": ".".join(str(p) for p in err.get("loc", []) if p != "body"),
                "issue": err.get("msg", "invalid value"),
            }
            for err in exc.errors()
        ]
        return _envelope(
            code="VALIDATION_FAILED",
            message="Request validation failed.",
            trace_id=_trace_id(request),
            details=details,
            http_status=status.HTTP_422_UNPROCESSABLE_ENTITY,
        )
