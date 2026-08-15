# Backend setup — Postgres + Alembic

## Yerel development (Docker Compose)

En kolay yol — Postgres, migration, API hepsi bir arada:

```bash
export ANTHROPIC_API_KEY=sk-ant-...
export CBT_ADMIN_TOKEN=$(openssl rand -hex 32)

# Postgres + API başlat
docker compose up -d db
docker compose logs -f db      # "database system is ready" bekle

# Migration uygula (bir kere)
docker compose run --rm api alembic upgrade head

# API'yi başlat
docker compose up api
# → http://localhost:8000/docs
```

## Yerel development (Docker'sız)

Sadece Postgres'i Docker'da çalıştırıp API'yi lokalde:

```bash
docker compose up -d db

# Deps
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements-api.txt

# Env
export ANTHROPIC_API_KEY=sk-ant-...
export CBT_DB_URL=postgresql+psycopg://cbt:cbt@localhost:5432/cbt

# Migration
alembic upgrade head

# API
uvicorn api.main:app --reload
# → http://localhost:8000/docs
```

## Migration workflow

```bash
# Yeni migration oluştur (auto-generate)
alembic revision --autogenerate -m "add users email index"

# Uygula
alembic upgrade head

# Bir revision geri al
alembic downgrade -1

# Mevcut durum
alembic current
alembic history
```

## Env değişkenleri

| Değişken | Default | Anlam |
|---|---|---|
| `ANTHROPIC_API_KEY` | — | LLM API key (mock ise gerekmez) |
| `CBT_LLM_PROVIDER` | `anthropic` | anthropic / openai / local / mock |
| `CBT_DB_URL` | postgres localhost | Full DB URL — set edildi ise diğer CBT_DB_* ignore |
| `CBT_DB_HOST` | localhost | Postgres host |
| `CBT_DB_PORT` | 5432 | Postgres port |
| `CBT_DB_USER` | cbt | |
| `CBT_DB_PASSWORD` | cbt | |
| `CBT_DB_NAME` | cbt | |
| `CBT_HASH_SALT` | dev default | user_message hash salt (PROD'DA DEĞİŞTİR) |
| `CBT_SESSION_TTL_SECONDS` | 3600 | Session expiry (1 saat default) |
| `CBT_ADMIN_TOKEN` | boş | Set edildi ise /eval, /cards/safety admin gated |
| `CBT_POLICY_VERSION` | 0.2 | /consent endpoint accepted version |
| `CBT_CORS_ORIGINS` | localhost:3000 | Comma-separated allowed origins |
| `LOG_LEVEL` | INFO | JSON structured logs seviyesi |

## Test

```bash
# SQLite in-memory kullanır — Postgres gerekmez
pytest tests/ -v
```

conftest.py:
- `CBT_LLM_PROVIDER=mock`, `CBT_PREFER_ST=0`, `CBT_DB_URL=sqlite:///:memory:`
- create_all_for_tests() ile schema, her testte reset

## Schema

```
users              → future magic link auth
consent_records    → KVKK audit trail
sessions           → chat sessions (anon user_id NULL)
turns              → user↔assistant exchanges + safety/intent/critic JSON
feedback           → 👍👎🚩 verdictler
```

Cascade: session silinince → turns + feedback silinir. User silinince → sessions silinir.

## KVKK notları

- `turns.user_message` **ephemeral** (session TTL boyunca), `retention_ends_at` ile purge işareti
- `turns.user_hash` kalıcı (audit)
- `feedback.comment` prod'da PII redact önerilir (şu an ham)
- Session silme: `DELETE /chat/session/{id}` → cascade turns + feedback

## Deploy'a hazırlık

Prod'a çıkmadan mutlaka set:

```bash
CBT_HASH_SALT=$(openssl rand -hex 32)
CBT_ADMIN_TOKEN=$(openssl rand -hex 32)
CBT_DB_PASSWORD=$(openssl rand -base64 24)
CBT_CORS_ORIGINS=https://app.tr,https://www.app.tr
LOG_LEVEL=INFO
```

Postgres backup:
```bash
docker exec cbt-db pg_dump -U cbt cbt > backup_$(date +%Y%m%d).sql
```
