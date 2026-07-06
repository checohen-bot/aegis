# Aegis web image — multi-stage build producing Next.js standalone output.
# Local/sandbox skeleton, not a production-hardened image (per RFC-0001).
FROM node:20-slim AS builder

WORKDIR /app

# Optional extra CA certificate for TLS-intercepting egress proxies. Empty by
# default (Node just ignores a missing file); the proxy CA is dropped into
# ./certs in sandboxed environments so npm can verify the registry.
COPY certs/ /certs/
ENV NODE_EXTRA_CA_CERTS=/certs/proxy-ca.crt

COPY package.json ./
RUN npm install

COPY . .
# NEXT_PUBLIC_* vars are inlined at build time; the browser calls the API
# directly, so this must be the URL reachable from the user's browser.
ARG NEXT_PUBLIC_API_BASE_URL=http://localhost:8000
ENV NEXT_PUBLIC_API_BASE_URL=$NEXT_PUBLIC_API_BASE_URL
RUN npm run build

FROM node:20-slim AS runner

WORKDIR /app
ENV NODE_ENV=production

# Standalone output bundles only what the server needs at runtime.
COPY --from=builder /app/.next/standalone ./
COPY --from=builder /app/.next/static ./.next/static
COPY --from=builder /app/public ./public

EXPOSE 3000
CMD ["node", "server.js"]
