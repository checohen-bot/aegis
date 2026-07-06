"""Typed application configuration, read from the environment.

Configuration is never hardcoded in source (per the coding standards); it is
read here from environment variables with sensible local-dev defaults. Secrets
are not logged.
"""

from __future__ import annotations

import os
from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class Settings:
    """Runtime settings for the API service."""

    database_url: str
    log_level: str

    @property
    def redacted(self) -> dict[str, str]:
        """A log-safe view of settings, with credentials in the URL masked."""
        return {
            "database_url": _redact_url(self.database_url),
            "log_level": self.log_level,
        }


def _redact_url(url: str) -> str:
    """Mask any ``user:password@`` credentials in a database URL."""
    if "@" not in url or "://" not in url:
        return url
    scheme, rest = url.split("://", 1)
    if "@" not in rest:
        return url
    _creds, host = rest.split("@", 1)
    return f"{scheme}://***@{host}"


def load_settings() -> Settings:
    """Load settings from the environment, applying local-dev defaults."""
    return Settings(
        database_url=os.environ.get(
            "DATABASE_URL",
            "postgresql+psycopg2://aegis:aegis@localhost:5432/aegis",
        ),
        log_level=os.environ.get("LOG_LEVEL", "INFO"),
    )
