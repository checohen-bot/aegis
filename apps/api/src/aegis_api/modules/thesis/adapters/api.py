"""FastAPI router and boundary DTOs for the Investment Thesis resource.

DTOs here are boundary objects (camelCase JSON per the API standards); they are
mapped explicitly to and from domain objects and never leak into the domain.
Endpoints follow the API standards: canonical resource name (``theses``), state
transitions modeled as sub-resources (``/activation``, ``/invalidation``),
cursor pagination, and required explainability fields.
"""

from __future__ import annotations

import base64
import json
from collections.abc import Iterator
from typing import Annotated

from fastapi import APIRouter, Depends, Query, Request, Response, status
from pydantic import BaseModel, ConfigDict, Field
from pydantic.alias_generators import to_camel
from sqlalchemy.orm import Session

from ..application import FormThesisCommand, LoggingEventPublisher, ThesisService
from ..domain import InvestmentThesis
from .repository import SqlAlchemyThesisRepository

_DEFAULT_LIMIT = 25
_MAX_LIMIT = 100

router = APIRouter(prefix="/v1/theses", tags=["theses"])


# --------------------------------------------------------------------------- #
# DTOs
# --------------------------------------------------------------------------- #


class _CamelModel(BaseModel):
    """Base DTO: serialize camelCase, accept either camelCase or snake_case."""

    model_config = ConfigDict(alias_generator=to_camel, populate_by_name=True)


class FormThesisRequest(_CamelModel):
    """Request body to form a new Investment Thesis."""

    company_ref: str = Field(min_length=1)
    author_ref: str = Field(min_length=1)
    thesis_statement: str = Field(min_length=1)
    rationale: str = Field(default="")
    key_assumptions: list[str] = Field(default_factory=list)
    falsification_conditions: list[str] = Field(min_length=1)
    time_horizon: str = Field(min_length=1)
    conviction_level: int = Field(ge=1, le=5)


class InvalidateThesisRequest(_CamelModel):
    """Request body to invalidate a Thesis: which falsification condition was met."""

    condition_met: str = Field(min_length=1)


class ThesisExplainability(_CamelModel):
    """Reasoning links carried by a Thesis.

    The Thesis's own reasoning (rationale, assumptions, falsification conditions)
    lives on the resource itself. Evidence, Catalysts, and Risks are separate
    aggregates that do not yet exist in the walking skeleton (RFC-0001 scope);
    the required explainability arrays are present and empty until those modules
    land, rather than omitted.
    """

    evidence: list[dict[str, str]] = Field(default_factory=list)
    catalysts: list[dict[str, str]] = Field(default_factory=list)
    risks: list[dict[str, str]] = Field(default_factory=list)


class ThesisResponse(_CamelModel):
    """Representation of an Investment Thesis returned to clients."""

    id: str
    company_ref: str
    author_ref: str
    thesis_statement: str
    rationale: str
    key_assumptions: list[str]
    falsification_conditions: list[str]
    time_horizon: str
    conviction_level: int
    status: str
    created_at: str
    last_reviewed_at: str | None
    invalidation_condition_met: str | None
    based_on: ThesisExplainability


class PageInfo(_CamelModel):
    """Cursor-pagination metadata."""

    next_cursor: str | None
    has_more: bool
    limit: int


class ThesisListResponse(_CamelModel):
    """A paginated list of Theses."""

    data: list[ThesisResponse]
    page: PageInfo


# --------------------------------------------------------------------------- #
# Mapping
# --------------------------------------------------------------------------- #


def _to_response(thesis: InvestmentThesis) -> ThesisResponse:
    return ThesisResponse(
        id=thesis.thesis_id.value,
        company_ref=thesis.company_ref,
        author_ref=thesis.author_ref,
        thesis_statement=thesis.thesis_statement,
        rationale=thesis.rationale,
        key_assumptions=thesis.key_assumptions,
        falsification_conditions=[c.text for c in thesis.falsification_conditions],
        time_horizon=thesis.time_horizon,
        conviction_level=thesis.conviction_level.value,
        status=thesis.status.value,
        created_at=thesis.created_at.isoformat(),
        last_reviewed_at=(
            thesis.last_reviewed_at.isoformat()
            if thesis.last_reviewed_at is not None
            else None
        ),
        invalidation_condition_met=thesis.invalidation_condition_met,
        based_on=ThesisExplainability(),
    )


def _encode_cursor(offset: int) -> str:
    raw = json.dumps({"offset": offset}).encode("utf-8")
    return base64.urlsafe_b64encode(raw).decode("ascii")


def _decode_cursor(cursor: str | None) -> int:
    if cursor is None:
        return 0
    try:
        raw = base64.urlsafe_b64decode(cursor.encode("ascii"))
        offset = json.loads(raw)["offset"]
        return int(offset) if int(offset) >= 0 else 0
    except (ValueError, KeyError, TypeError):
        # An unreadable cursor is treated as "start from the beginning" rather
        # than a hard error, per the standard's tolerance for opaque cursors.
        return 0


# --------------------------------------------------------------------------- #
# Dependencies
# --------------------------------------------------------------------------- #


def get_session(request: Request) -> Iterator[Session]:
    """Yield a request-scoped session; commit on success, roll back on error."""
    factory = request.app.state.session_factory
    session: Session = factory()
    try:
        yield session
        session.commit()
    except Exception:
        session.rollback()
        raise
    finally:
        session.close()


def get_service(
    session: Annotated[Session, Depends(get_session)],
) -> ThesisService:
    """Assemble the application service with request-scoped adapters."""
    repository = SqlAlchemyThesisRepository(session)
    publisher = LoggingEventPublisher()
    return ThesisService(repository, publisher)


ServiceDep = Annotated[ThesisService, Depends(get_service)]


# --------------------------------------------------------------------------- #
# Endpoints
# --------------------------------------------------------------------------- #


@router.post("", status_code=status.HTTP_201_CREATED, response_model=ThesisResponse)
def form_thesis(body: FormThesisRequest, service: ServiceDep) -> ThesisResponse:
    """Form a new Investment Thesis in DRAFT state."""
    thesis = service.form_thesis(
        FormThesisCommand(
            company_ref=body.company_ref,
            author_ref=body.author_ref,
            thesis_statement=body.thesis_statement,
            rationale=body.rationale,
            key_assumptions=body.key_assumptions,
            falsification_conditions=body.falsification_conditions,
            time_horizon=body.time_horizon,
            conviction_level=body.conviction_level,
        )
    )
    return _to_response(thesis)


@router.get("", response_model=ThesisListResponse)
def list_theses(
    service: ServiceDep,
    limit: Annotated[int, Query(ge=1)] = _DEFAULT_LIMIT,
    cursor: Annotated[str | None, Query()] = None,
) -> ThesisListResponse:
    """List Theses, newest first, with cursor-based pagination."""
    effective_limit = min(limit, _MAX_LIMIT)  # clamp, do not reject
    offset = _decode_cursor(cursor)
    page = service.list_theses(limit=effective_limit, offset=offset)
    return ThesisListResponse(
        data=[_to_response(t) for t in page.items],
        page=PageInfo(
            next_cursor=(
                _encode_cursor(page.next_offset)
                if page.next_offset is not None
                else None
            ),
            has_more=page.next_offset is not None,
            limit=effective_limit,
        ),
    )


@router.get("/{thesis_id}", response_model=ThesisResponse)
def get_thesis(thesis_id: str, service: ServiceDep) -> ThesisResponse:
    """Retrieve a single Thesis by id."""
    return _to_response(service.get_thesis(thesis_id))


@router.post(
    "/{thesis_id}/activation",
    status_code=status.HTTP_200_OK,
    response_model=ThesisResponse,
)
def activate_thesis(thesis_id: str, service: ServiceDep) -> ThesisResponse:
    """Activate a Thesis (DRAFT -> ACTIVE), modeled as an activation sub-resource."""
    return _to_response(service.activate_thesis(thesis_id))


@router.post(
    "/{thesis_id}/invalidation",
    status_code=status.HTTP_200_OK,
    response_model=ThesisResponse,
)
def invalidate_thesis(
    thesis_id: str, body: InvalidateThesisRequest, service: ServiceDep
) -> ThesisResponse:
    """Invalidate a Thesis (ACTIVE -> INVALIDATED), recording the met condition."""
    return _to_response(
        service.invalidate_thesis(thesis_id, body.condition_met)
    )
