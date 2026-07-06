"""Integration tests for the Investment Thesis API.

These drive the real FastAPI app over HTTP (via TestClient) against a real
SQLAlchemy repository and database. They prove the full end-to-end slice:
form -> retrieve -> activate -> invalidate -> list, plus the error envelope on
failure paths.
"""

from __future__ import annotations

from typing import Any

from fastapi.testclient import TestClient

_VALID_BODY: dict[str, Any] = {
    "companyRef": "company:acme",
    "authorRef": "author:analyst-1",
    "thesisStatement": (
        "Acme Corp will sustain returns on capital above its cost of capital "
        "due to a durable distribution advantage."
    ),
    "rationale": "The distribution network cannot be replicated within the horizon.",
    "keyAssumptions": ["Incumbent distribution remains a moat."],
    "falsificationConditions": [
        "ROIC falls below cost of capital for four consecutive quarters."
    ],
    "timeHorizon": "3y",
    "convictionLevel": 4,
}


def _form(client: TestClient, **overrides: Any) -> dict[str, Any]:
    body = {**_VALID_BODY, **overrides}
    response = client.post("/v1/theses", json=body)
    assert response.status_code == 201, response.text
    data: dict[str, Any] = response.json()
    return data


def test_forming_a_thesis_returns_201_in_draft_with_explainability(
    client: TestClient,
) -> None:
    data = _form(client)

    assert data["status"] == "draft"
    assert data["id"]
    assert data["falsificationConditions"] == _VALID_BODY["falsificationConditions"]
    # Explainability block is present even though its aggregates are deferred.
    assert data["basedOn"] == {"evidence": [], "catalysts": [], "risks": []}


def test_forming_a_thesis_without_a_falsification_condition_returns_422(
    client: TestClient,
) -> None:
    response = client.post(
        "/v1/theses", json={**_VALID_BODY, "falsificationConditions": []}
    )

    assert response.status_code == 422
    envelope = response.json()["error"]
    assert envelope["code"] == "VALIDATION_FAILED"
    assert "traceId" in envelope


def test_retrieving_a_formed_thesis_returns_it(client: TestClient) -> None:
    created = _form(client)

    response = client.get(f"/v1/theses/{created['id']}")

    assert response.status_code == 200
    assert response.json()["id"] == created["id"]


def test_retrieving_an_unknown_thesis_returns_404_envelope(
    client: TestClient,
) -> None:
    response = client.get("/v1/theses/00000000-0000-0000-0000-000000000000")

    assert response.status_code == 404
    envelope = response.json()["error"]
    assert envelope["code"] == "THESIS_NOT_FOUND"
    assert envelope["traceId"]


def test_full_lifecycle_form_activate_invalidate(client: TestClient) -> None:
    created = _form(client)
    thesis_id = created["id"]

    activation = client.post(f"/v1/theses/{thesis_id}/activation")
    assert activation.status_code == 200
    assert activation.json()["status"] == "active"

    invalidation = client.post(
        f"/v1/theses/{thesis_id}/invalidation",
        json={"conditionMet": "ROIC fell below cost of capital for four quarters."},
    )
    assert invalidation.status_code == 200
    body = invalidation.json()
    assert body["status"] == "invalidated"
    assert body["invalidationConditionMet"].startswith("ROIC fell below")


def test_invalidating_a_draft_thesis_returns_409_conflict(
    client: TestClient,
) -> None:
    created = _form(client)

    response = client.post(
        f"/v1/theses/{created['id']}/invalidation",
        json={"conditionMet": "some condition"},
    )

    assert response.status_code == 409
    assert response.json()["error"]["code"] == "INVALID_THESIS_TRANSITION"


def test_activating_an_already_active_thesis_returns_409(client: TestClient) -> None:
    created = _form(client)
    client.post(f"/v1/theses/{created['id']}/activation")

    response = client.post(f"/v1/theses/{created['id']}/activation")

    assert response.status_code == 409


def test_listing_theses_returns_data_and_page_envelope(client: TestClient) -> None:
    _form(client)
    _form(client)

    response = client.get("/v1/theses?limit=1")

    assert response.status_code == 200
    body = response.json()
    assert len(body["data"]) == 1
    assert body["page"]["hasMore"] is True
    assert body["page"]["nextCursor"]
    assert body["page"]["limit"] == 1

    # Follow the cursor to the next page.
    second = client.get(f"/v1/theses?limit=1&cursor={body['page']['nextCursor']}")
    assert second.status_code == 200
    assert len(second.json()["data"]) == 1


def test_list_limit_is_clamped_to_the_maximum(client: TestClient) -> None:
    _form(client)

    response = client.get("/v1/theses?limit=5000")

    assert response.status_code == 200
    assert response.json()["page"]["limit"] == 100
