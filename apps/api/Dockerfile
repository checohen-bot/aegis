# Aegis API service image.
# Single-stage, slim base — this is a local/sandbox skeleton, not a hardened
# production image (production build is out of scope per RFC-0001 / ADR-0015).
FROM python:3.11-slim

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=1

WORKDIR /app

# Optional extra CA certificates. Empty by default (a no-op); used only in
# environments behind a TLS-intercepting egress proxy, where the proxy CA is
# dropped into ./certs. Pointing pip/requests at the system bundle is standard
# and correct in normal environments too.
COPY certs/ /usr/local/share/ca-certificates/
RUN update-ca-certificates || true
ENV PIP_CERT=/etc/ssl/certs/ca-certificates.crt \
    SSL_CERT_FILE=/etc/ssl/certs/ca-certificates.crt \
    REQUESTS_CA_BUNDLE=/etc/ssl/certs/ca-certificates.crt

# Install dependencies first for better layer caching.
COPY pyproject.toml ./
COPY src ./src
RUN pip install --upgrade pip && pip install .

EXPOSE 8000

# Uvicorn serves the ASGI app from the installed package.
CMD ["uvicorn", "aegis_api.main:app", "--host", "0.0.0.0", "--port", "8000"]
