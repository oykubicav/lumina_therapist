# CBT chatbot API — production Docker image.
#
# Multi-stage: builder installs deps, runtime image copies only what's needed.
# Retrieval prod'da TF-IDF (sklearn) ile çalışır — torch/HF modeli imajda yok.

FROM python:3.11-slim AS builder

WORKDIR /build

# System build deps (sklearn/scipy wheels bazı mimarilerde derleme ister)
RUN apt-get update && apt-get install -y --no-install-recommends \
        build-essential curl \
    && rm -rf /var/lib/apt/lists/*

COPY requirements-api.txt .
RUN pip install --no-cache-dir --prefix=/install -r requirements-api.txt


# ============================================================
# Runtime image
# ============================================================

FROM python:3.11-slim

WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends \
        curl \
    && rm -rf /var/lib/apt/lists/*

# Copy installed deps from builder
COPY --from=builder /install /usr/local

# App source
COPY pipeline/ ./pipeline/
COPY api/ ./api/
COPY cards/ ./cards/
COPY rules/ ./rules/
COPY policies/ ./policies/
COPY registry/ ./registry/
# NOT: evals/ dosyaları prod runtime'da gerekli değil — lokal test için.
# `.dockerignore` `evals/*.jsonl`'i hariç bırakıyor, uyumlu.

# Alembic — migration container startup'ında çalıştırılır (CMD içinde)
COPY alembic.ini ./
COPY alembic/ ./alembic/

# Graph — Neo4j GraphRAG (opsiyonel, env yoksa hybrid retriever fallback yapar)
COPY graph/ ./graph/

# Runtime configuration
ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1
ENV LOG_LEVEL=INFO
ENV CBT_LLM_PROVIDER=anthropic
ENV CBT_PREFER_ST=0

# Non-root user
RUN useradd --create-home --shell /bin/bash apiuser \
    && chown -R apiuser:apiuser /app
USER apiuser

EXPOSE 8000

HEALTHCHECK --interval=30s --timeout=5s --retries=3 --start-period=15s \
    CMD curl -fsS http://localhost:8000/health || exit 1

# Startup: önce migration (idempotent), sonra API. Free tier'da
# preDeployCommand yok, o yüzden migration'ı container start'ında yapıyoruz.
# Port: Render $PORT=10000 set eder; lokal Docker'da default 8000.
# Workers: free tier 512 MB RAM — tek worker.
CMD ["sh", "-c", "alembic upgrade head && uvicorn api.main:app --host 0.0.0.0 --port ${PORT:-8000} --workers 1"]
