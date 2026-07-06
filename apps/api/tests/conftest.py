"""Shared test fixtures.

The API/integration tests run against a real SQLAlchemy stack backed by an
ephemeral file-based SQLite database. SQLite is chosen as a pragmatic stand-in
for PostgreSQL in the skeleton's integration tests: it exercises the real
repository, real session handling, and real HTTP layer deterministically and
without a container, while the same repository code runs against PostgreSQL in
Docker Compose (verified separately via curl). The reasoning is recorded in
apps/api/README.md.
"""

from __future__ import annotations

from collections.abc import Iterator

import pytest
from fastapi.testclient import TestClient

from aegis_api.config import Settings
from aegis_api.main import create_app


@pytest.fixture()
def client(tmp_path: object) -> Iterator[TestClient]:
    db_path = f"{tmp_path}/aegis_test.db"
    settings = Settings(
        database_url=f"sqlite:///{db_path}",
        log_level="WARNING",
        cors_origins=("http://localhost:3000",),
    )
    app = create_app(settings)
    # Entering the context manager runs the lifespan (create_all) so the schema
    # exists before any request.
    with TestClient(app) as test_client:
        yield test_client
