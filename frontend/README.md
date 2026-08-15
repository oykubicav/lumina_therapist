# CBT Frontend

Next.js 14 (App Router) + TypeScript + Tailwind. Backend olarak `../api/` (FastAPI) çalışır durumda olmalı.

## Hızlı başlangıç

```bash
cd frontend
npm install

# Backend çalışıyor mu kontrol et:
curl http://localhost:8000/health

# .env.local oluştur
cp .env.local.example .env.local
# NEXT_PUBLIC_API_BASE=http://localhost:8000

npm run dev
# → http://localhost:3000
```

## Ne var

- `/` — Chat UI. İlk açılışta KVKK consent modal'ı çıkar. Kabul edilmeden mesaj gönderilemez.
- `/cards` — Kart kütüphanesi. Modüle göre filtre, başlıkta arama, detay modal'ı.
- Debug switch — header'da `Debug` kutusunu işaretlersen her assistant cevabının altında sistem detayları (safety route, intent, retrieved kart id'leri, critic durumu, timing) açılır.
- Feedback butonları — 👍 👎 🚩 her assistant cevabının altında. Thumbs down / flag için opsiyonel not kutusu.
- Session persist — `session_id` localStorage'a kaydedilir; refresh'te aynı oturuma döner. Header'daki "Oturumu sil" düğmesi backend'e `DELETE /chat/session/{id}` atar ve localStorage'ı temizler (KVKK silme hakkı).

## Yapısı

```
frontend/
├── app/
│   ├── layout.tsx           kök layout
│   ├── page.tsx             chat
│   ├── globals.css
│   └── cards/page.tsx       kart kütüphanesi
├── components/
│   ├── ChatWindow.tsx       header + mesajlar + input
│   ├── Message.tsx          user + assistant balonu
│   ├── DebugPanel.tsx       safety/intent/critic detayları
│   ├── FeedbackButtons.tsx  👍 👎 🚩 + not
│   ├── ConsentModal.tsx     KVKK aydınlatma + kabul
│   └── CardList.tsx         /cards sayfası
├── lib/
│   ├── api.ts               fetch wrapper
│   ├── types.ts             backend schema'sının TS karşılığı
│   ├── session.ts           localStorage session_id
│   └── consent.ts           localStorage consent ts
├── package.json
├── tsconfig.json
├── tailwind.config.ts
├── postcss.config.mjs
├── next.config.mjs
└── .env.local.example
```

## Test scripts

```bash
npm run dev        # dev sunucu, hot reload
npm run build      # prod build
npm run start      # prod sunucu
npm run lint       # eslint
npm run typecheck  # tsc --noEmit
```

## KVKK notları

- İlk açılışta `ConsentModal` blokluyor. Kullanıcı kabul edene kadar mesaj göndereMYECek — ancak MVP'de UI seviyesinde blok var; asıl backend endpoint'i (`/consent`) henüz yok.
- Session TTL backend'de default 1 saat. Frontend `session_id`'yi localStorage'da tutar; kullanıcı "Oturumu sil"'e basarsa hem backend'e DELETE gider hem localStorage temizlenir.
- Debug panel'da hiçbir user mesajı ham hâlde loglanmaz — sadece server'ın döndürdüğü meta bilgiler görünür.

## Bilinen boşluklar (MVP)

- Kullanıcı hesabı yok — soft account (magic link) Aşama 6+
- Streaming yanıt yok — backend orchestrator bulk döndürüyor. Sonnet ~3-5s bekleme
- Server-side rendering minimal — çoğu şey `"use client"`. İlk paint hızlı, ama SEO odaklı değil
- Test yok — MVP; Playwright/vitest ekleneceklerin sırasında

## Backend paralel çalıştırma

```bash
# Terminal 1 (backend)
cd cbt_knowledge_base
export ANTHROPIC_API_KEY=sk-ant-...
uvicorn api.main:app --reload

# Terminal 2 (frontend)
cd cbt_knowledge_base/frontend
npm run dev
```

Backend `http://localhost:8000`, frontend `http://localhost:3000`. CORS zaten backend'de localhost:3000'e izin veriyor.
