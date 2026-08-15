# Deploy Rehberi — Render + Vercel + Cloudflare

Bu doküman sıfırdan prod'a kadar adım adım gider. **Sıra**: backend (Render) →
frontend (Vercel) → domain (Cloudflare). Beklenen toplam süre: **1-2 saat**
(dashboard'da bekleme + tıklama).

## Ön koşullar

- GitHub'da bu repo (private / public fark etmez)
- Anthropic API key
- Ödemeye hazır kart (Render Starter $7/ay, Postgres $7/ay — toplam ~$14/ay)
- Alan adı (opsiyonel — Cloudflare'de ücretsiz `*.pages.dev` / `*.onrender.com` da kullanılabilir)

---

## 1. Backend + Postgres — Render

### 1.1. Repo'yu push et

```bash
git add render.yaml Dockerfile alembic/ alembic.ini .env.production.example
git commit -m "chore: add render blueprint + prod env template"
git push origin main
```

### 1.2. Render hesabı ve Blueprint

1. [render.com](https://render.com) → GitHub ile sign in.
2. Dashboard'da **New +** → **Blueprint**.
3. Repo'yu seç → Render `render.yaml`'ı otomatik okur.
4. Servis + database'i onayla. **Region: Frankfurt** (KVKK — EU).
5. **Deploy** butonu → Render Docker build'i başlatır (~5-8 dk).

### 1.3. Environment variables — dashboard'dan set et

Blueprint şu 3 secret'ı sync etmez (dashboard'dan girmelisin):

| Variable | Nereden alırsın |
|---|---|
| `ANTHROPIC_API_KEY` | [console.anthropic.com](https://console.anthropic.com) → API Keys |
| `CBT_CORS_ORIGINS` | Vercel deploy sonrası set edeceksin. Şimdilik `https://placeholder.tr` yaz. |

Diğer secret'ları (`CBT_HASH_SALT`, `CBT_ADMIN_TOKEN`) Render otomatik generate eder.

### 1.4. İlk deploy sonrası doğrulama

Render dashboard "Live" olduğunda:

```bash
export API_URL=https://cbt-api.onrender.com   # kendi URL'in

curl $API_URL/health
# → {"ok":true,"version":"0.1.0"}

curl $API_URL/readyz | jq
# → checks hepsi true olmalı:
#   cbt_cards, safety_cards, safety_rules, llm_api_key, embedding_backend
```

**Eğer `llm_api_key: false`** dönerse → `ANTHROPIC_API_KEY` doğru set edilmemiş, dashboard'dan kontrol et, redeploy tetikle.

### 1.5. Migration doğrulaması

`preDeployCommand: alembic upgrade head` her deploy'da otomatik koşar. İlk deploy'da tablolar oluşturulur. Kontrol:

```bash
# Render dashboard → cbt-postgres → "Connect" → connection string kopyala
# Sonra:
psql "$CONNECTION_STRING" -c "\dt"
# → users, sessions, consent_records, turns, feedback, alembic_version görmelisin
```

### 1.6. Custom domain (opsiyonel)

Render dashboard → cbt-api → Settings → Custom Domains → `api.cbt-destek.tr` ekle. Sonra 3. bölümde Cloudflare'de DNS ayarla.

---

## 2. Frontend — Vercel

### 2.1. Vercel hesabı

1. [vercel.com](https://vercel.com) → GitHub ile sign in.
2. **Add New...** → **Project** → repo'yu seç.
3. **Root Directory** = `frontend` (önemli — proje kökü değil).
4. Framework auto-detect → **Next.js**. Değiştirmene gerek yok.

### 2.2. Environment variables

Sadece 1 tane:

| Variable | Value |
|---|---|
| `NEXT_PUBLIC_API_BASE` | `https://cbt-api.onrender.com` (Render URL'in) |

Not: `NEXT_PUBLIC_*` prefix'i frontend'e expose olacağı anlamına gelir (public). API base URL public olması normal.

### 2.3. Deploy

**Deploy** butonu → Vercel `next build` çalıştırır, ~1-2 dakikada canlı.

URL'in: `cbt-destek.vercel.app` gibi bir şey olacak.

### 2.4. Backend CORS'u güncelle

Vercel URL'ini artık biliyorsun. Render dashboard'a dön:
- `CBT_CORS_ORIGINS=https://cbt-destek.vercel.app`
- Save → Render otomatik redeploy eder (~2 dk)

Kontrol:
```bash
curl -X POST https://cbt-api.onrender.com/consent \
  -H "Content-Type: application/json" \
  -H "Origin: https://cbt-destek.vercel.app" \
  -d '{"policy_version":"0.2"}'
# → 200 + session_id + consent_id dönmeli
```

### 2.5. Test — tam akış

`https://cbt-destek.vercel.app` aç:
1. Landing hero görün
2. "Sohbete başla" → Consent modal
3. Kabul et → chat açılır
4. Test mesajı yolla → cevap geldi mi?
5. `/cards` sayfası açılıyor mu?

---

## 3. Cloudflare — DNS + domain + bot koruma

Bu adım opsiyonel ama **canlıya çıkmadan önce kesinlikle yap**. Ücretsiz.

### 3.1. Domain ekleme

1. [cloudflare.com](https://cloudflare.com) → hesap aç → domain'i Cloudflare'e taşı (nameserver değişikliği ~24 saat).
2. Ya da mevcut Cloudflare-yönetimli bir domain'in altında subdomain kullan.

### 3.2. DNS kayıtları

Cloudflare DNS panel'de:

| Tip | Ad | Hedef | Proxy |
|---|---|---|---|
| CNAME | `@` (ana) | `cbt-destek.vercel.app` | 🟠 (Proxied) |
| CNAME | `www` | `cbt-destek.vercel.app` | 🟠 |
| CNAME | `api` | `cbt-api.onrender.com` | 🟠 |

Vercel ve Render'a da bu domain'leri "Custom Domain" olarak ekle — otomatik SSL sertifikası alırlar.

### 3.3. Turnstile CAPTCHA (bot koruma)

1. Cloudflare dashboard → **Turnstile** → **Add site**.
2. Domain'i seç, "Invisible" widget seç.
3. Site key + Secret key üretilir.
4. Site key → Vercel env var: `NEXT_PUBLIC_TURNSTILE_SITE_KEY`
5. Secret key → Render env var: `CBT_TURNSTILE_SECRET`

**Frontend integrasyonu** (`ChatWindow` içine ilk `/chat` çağrısı öncesi):

```tsx
// components/ChatWindow.tsx içinde, henüz eklenmedi — sonraki iterasyonda
```

Şimdilik Turnstile'ı **kur ama entegre etme** — 5 dakikalık iş, canlıya çıkmadan önce eklersin.

### 3.4. Rate limit + WAF

Cloudflare dashboard → Security:
- **Rate Limiting Rules**: `/chat` endpoint'i için IP başına dakikada 20 istek.
- **WAF Managed Rules**: default açık.
- **Bot Fight Mode**: on.

### 3.5. Under Attack Mode (gerektiğinde)

Eğer viral olursan ya da DDoS gelirse: dashboard'dan tek tıkla "Under Attack" mode → tüm istekler önce JS challenge geçer.

---

## 4. Prod öncesi kontrol listesi

- [ ] `curl https://api.cbt-destek.tr/readyz` → tüm checks true
- [ ] `CBT_ADMIN_TOKEN` set (Render'da otomatik generate edildi) → `/eval/run` korunuyor
- [ ] `CBT_HASH_SALT` set (otomatik) → session hash'leri güvenli
- [ ] `CBT_CORS_ORIGINS` doğru domain — sadece frontend origin'i
- [ ] Rate limit Cloudflare'de aktif
- [ ] `/health` endpoint public erişilebiliyor (Cloudflare bloklu değil)
- [ ] Migration çekildi (`\dt` ile tablolar görülüyor)
- [ ] Frontend'de consent modal → backend'e POST atıyor (Network sekmesinde 200)
- [ ] Chat mesajı end-to-end çalışıyor (safety + intent + response)
- [ ] Feedback butonu POST atıyor
- [ ] `Debug` toggle bilgi gösteriyor
- [ ] Dark mode toggle çalışıyor
- [ ] Mobile responsive (DevTools iPhone view)

---

## 5. KVKK ön kontrol (canlıya açmadan)

- [ ] Consent modal metni hukukçu tarafından gözden geçirildi
- [ ] Aydınlatma metni ayrı bir sayfada erişilebilir (henüz yok — Aşama 5+)
- [ ] VERBİS kaydı yapıldı (veri sorumlusu >5 çalışan / hassas veri işleme)
- [ ] Veri işleme envanteri güncellendi
- [ ] Silme talebi endpoint'i test edildi (`DELETE /chat/session/{id}`)
- [ ] Log seviyesi INFO — DEBUG loglarında kullanıcı verisi yok
- [ ] Backup stratejisi tanımlı (bkz. bölüm 7)

---

## 6. Rollback — bir şey ters giderse

**Backend hatalı deploy**:
1. Render dashboard → cbt-api → Deploys → önceki başarılı deploy → **Rollback**.
2. ~2 dakikada eski versiyona döner.

**Frontend hatalı deploy**:
1. Vercel dashboard → Deployments → önceki deploy → **Promote to Production**.
2. Anında eski versiyona döner.

**Migration ters**:
1. `alembic downgrade -1` — dashboard'dan Shell → çalıştır.
2. Ya da Render dashboard → **Manual Deploy** → önceki commit'i seç.

---

## 7. Backup

Render Postgres otomatik günlük backup alır (7 gün retention Free tier'da; Pro tier'da uzun).

**Manuel backup** (ekstra güvenlik):

```bash
# Render dashboard → Postgres → Connection string kopyala
export DB_URL="postgresql://cbt:...@dpg-....com/cbt"

# Dump
pg_dump "$DB_URL" > backup_$(date +%Y%m%d).sql

# Restore
psql "$DB_URL" < backup_20260801.sql
```

Cron ile hafta bir alıp Backblaze/S3'e yollamak iyi pratik. MVP için Render'ın otomatik backup'ı yeter.

---

## 8. Monitoring

Prod'a çıktığında set etmen gerekenler:

- **Sentry** (frontend + backend error tracking) — Free tier yeter, `sentry-sdk` ekle
- **Better Uptime** ya da **UptimeRobot** — `/health` her 5 dakikada ping, aksama olursa email/SMS
- **Anthropic dashboard** — token kullanımı takibi, daily budget alert
- **Render dashboard** — CPU/RAM/latency metrikleri built-in
- **Cloudflare Analytics** — trafik, bot vs. gerçek kullanıcı ayrımı

---

## 9. Maliyet takip

Aylık beklenen (ilk 100 kullanıcı):

| Servis | Maliyet |
|---|---|
| Render backend (Starter) | $7 |
| Render Postgres (Basic 256MB) | $7 |
| Vercel Hobby | $0 |
| Cloudflare | $0 |
| Anthropic API (100 user × 15 msg × Sonnet+Haiku+Haiku) | ~$15-30 |
| **TOPLAM** | **~$30-45/ay** |

1000 kullanıcıya çıkarken:
- Render Postgres'i Basic-1GB ($20/ay) yap
- Render backend'i Standard ($25/ay) yap → daha yüksek RAM
- Anthropic prompt caching aç (%90 indirim)
- Toplam ~$100/ay + LLM

---

## 10. Sonraki iterasyonlar (post-launch)

Öncelik sırasıyla:

1. **Turnstile CAPTCHA** entegrasyonu (frontend)
2. **Sentry** kurulumu
3. **Magic link auth** — kullanıcı geçmişini görebilsin (Aşama 6)
4. **Anthropic prompt caching** — cost %90 düşer
5. **Streaming responses** — UX iyileşir
6. **Admin dashboard** — flagged turn review workflow
7. **Analytics** — kullanıcı retention, feedback pattern
8. **Türkiye data residency** — Turkcell Cloud'a taşıma (gerekirse)

---

**Sorun olursa**: `render.yaml` env var isimleri backend kodundaki `os.environ.get(...)` isimleriyle **kesinlikle eşleşmeli**. Tek bir typo tüm sistemi kırar. Yenilikle karşılaşırsan önce `readyz` çıktısına bak, hangi check false onu debug et.

**İyi launch'lar.**
