# Klinisyen Review Kit

30 senaryolu klinik uygunluk denetimi. Bir psikiyatri hekimi ya da klinik psikolog bir
oturumda (yaklaşık 45-60 dakika) sistemin çıktılarını gözden geçirsin, doldurulmuş
Google Docs / basılı formu bize geri versin.

## Ne var

- `scenarios.json` — 30 senaryo (10 safety + 10 CBT + 10 boundary/nüans). Her senaryonun
  `user_message` (klinisyenin göreceği input) + `expected_behavior` (bizim klinik referansımız).
- `run_review.py` — orchestrator'ı her senaryo için çalıştırıp klinisyene sunulacak markdown
  rapor üretir.
- `output/review_YYYYMMDD_HHMMSS.md` — üretilen çıktı.

## Kullanım

Adım 1 — sistemi çalıştırıp senaryoları toplu koştur:

```bash
export ANTHROPIC_API_KEY=sk-ant-...
export CBT_DB_URL=postgresql+psycopg://cbt:cbt@localhost:5433/cbt
export CBT_LLM_PROVIDER=anthropic  # ya da mock (dev)
alembic upgrade head              # DB hazır olmalı

python -m evals.clinician_review.run_review
```

Adım 2 — çıktıyı incele:

```bash
open evals/clinician_review/output/review_*.md
# ya da:
cat evals/clinician_review/output/review_*.md | pbcopy   # panoya kopyala
```

Adım 3 — Google Docs'a taşı ve paylaş:

1. Yeni Google Docs oluştur.
2. Markdown içeriği paste et (Google Docs modern kopyalama ile başlık/liste yapısını korur).
3. Görüntüle > "Aşama 2" başlığı falan varsa TOC ekle (opsiyonel).
4. Docs'un "Yorum yapabilir" izniyle klinisyene paylaş.

Adım 4 — sonuç geldiğinde:

- ⛔ (ciddi sorun) işaretlenmiş senaryolar → **eval regression testine ekle** (`evals/response_test_set.jsonl`).
- ⚠ (küçük iyileştirme) → composer system prompt tune ya da concept ontology güncelle.
- ☑ (uygun) → sistem şu haliyle prod'a hazır olan bölüm.

## Faydalı komutlar

```bash
# Yalnız kriz senaryoları (S01-S10):
python -m evals.clinician_review.run_review --ids S01,S02,S03,S04,S05,S06,S07,S08,S09,S10

# Debug meta dahil (klinisyen değil, iç geliştirme için):
python -m evals.clinician_review.run_review --debug

# Mock (LLM yok, sadece iskelet kontrol):
CBT_LLM_PROVIDER=mock python -m evals.clinician_review.run_review
```

## Maliyet ve süre tahmini

- Sonnet composer + Haiku critic + Haiku intent × 30 senaryo = **~1-2 USD**
- ~10-15 sn / senaryo × 30 = **~5-8 dakika** (rewrite'lı senaryolarda daha uzun)
- Klinisyen incelemesi = **45-60 dakika**

## Sonraki iterasyon

Klinisyen review'dan çıkan bulgular:
1. `response_test_set.jsonl`'e regression case olarak eklenir
2. Composer / critic prompt'ları tune edilir
3. Yeni safety concept'leri ontology'e eklenir
4. Sonraki review (v0.3) — 45-60 senaryo, daha ince case'ler

Bu her 4-6 haftada bir tekrarlanır. **Her prod release'inden önce en az bir klinisyen
review geçmiş olmalı** — organizasyonel bir kural olarak yerleştir.
