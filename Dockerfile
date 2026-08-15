# CBT chatbot API — production Docker image.
#
# Multi-stage: builder installs deps + downloads embedding model at build
# time (image is heavier but first request is instant). Runtime image
# copies only what's needed.

FROM python:3.11-slim AS builder

WORKDIR /build

# System build deps (needed by torch/sklearn wheels on some archs)
RUN apt-get update && apt-get install -y --no-install-recommends \
        build-essential curl \
    && rm -rf /var/lib/apt/lists/*

COPY requirements-api.txt .
RUN pip install --no-cache-dir --prefix=/install -r requirements-api.txt

# Pre-download the multilingual sentence-transformers model into the image
# so the container never needs to reach HF at runtime.
ENV PYTHONPATH=/install/lib/python3.11/site-packages
RUN python -c "from sentence_transformers import SentenceTransformer; \
    SentenceTransformer('sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2')"


# ============================================================
# Runtime image
# ============================================================

FROM python:3.11-slim

WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends \
        curl \
    && rm -rf /var/lib/apt/lists/*

# Copy installed deps + model cache from builder
COPY --from=builder /install /usr/local
COPY --from=builder /root/.cache/huggingface /root/.cache/huggingface

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
