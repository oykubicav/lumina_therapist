"""Profile extractor — Haiku ile turn'den yapılandırılmış sinyal çıkarma.

Her turn (user_message + response) sonrası çağrılır. Kullanıcının:
  - somut tetikleyicileri (triggers)
  - tekrarlayan temaları (themes)
  - denenen egzersizleri + sonuçlarını (coping_tried)
  - konuşulan modülleri (modules_engaged)
çıkarır ve mevcut profile'a MERGE eder.

Design principles:
  - MUHAFAZAKAR: kullanıcı açıkça söylediyse ekle, yorum yapma
  - KVKK: llm_adapter.redact=True → TCKN/telefon/email PII gitmez
  - Fail-safe: LLM hatası → mevcut profile bozulmadan kalır, patch skip

Öykü karar 2 (muhafazakar) + 3 (her turn) + 1 (async) + 4 (opaque) — Faz 2 planı.
"""

from __future__ import annotations

import json
import re
from typing import Optional
from dataclasses import dataclass, field

from . import config
from . import llm_adapter


@dataclass
class ProfilePatch:
    """Haiku'nun ürettiği delta — mevcut profile'a merge edilecek."""
    add_triggers: list[str] = field(default_factory=list)
    add_themes: list[str] = field(default_factory=list)
    coping_updates: dict[str, str] = field(default_factory=dict)   # {tech_id: "yararlı"|"yararsız"|"denenmedi"}
    add_modules: list[str] = field(default_factory=list)
    progress_note: Optional[str] = None                            # bir cümlelik ilerleme özeti

    def is_empty(self) -> bool:
        return not (
            self.add_triggers or self.add_themes or self.coping_updates
            or self.add_modules or self.progress_note
        )


_EXTRACTOR_SYSTEM_TR = """Sen bir CBT chatbot'unun arka plan sinyal çıkarım modelisin. Görevin: bir turn'deki (user_message + response) KONKRE bilgileri yapılandırılmış JSON'a çevirmek.

TEMEL KURAL — MUHAFAZAKAR ÇIKARIM:
- Kullanıcı AÇIKÇA söylediyse ekle. Yorumlama yapma.
- Bir tema çıkarımı için kullanıcının o temayı en az 1 kez ima etmesi gerek.
- Uydurma. Hallucinate etme. Boşsa boş dön.
- KVKK: kişisel isim, telefon, adres asla çıkarma. Sadece jenerik rol ("partneri", "annesi") ve durum bilgisi.

ÇIKARILACAK ALANLAR:

1. add_triggers (list[str]):
   Kullanıcının belirttiği SOMUT tetikleyici olaylar. Örnekler:
   - "iş toplantısı", "sabahları uyanış", "annemle görüşme", "trafikte"
   - Genel duygu değil ("kaygı" değil), somut olay ("Cuma günü sunum")

2. add_themes (list[str]):
   Tekrarlayan psikolojik temalar (kullanıcının 2+ kez ima ettiği).
   Örnekler: "yalnızlık", "kontrolsüzlük", "yetersizlik", "reddedilme korkusu"
   Sadece 1 kez geçtiyse EKLEME.

3. coping_updates (dict):
   Kullanıcının denediğini söylediği ya da chatbot'un önerdiği tekniği kabul/red etmesi.
   Formatı: {"technique_id": "yararlı" | "yararsız" | "denenmedi" | "deneyecek"}
   Technique_id örnekleri: thought_record, grounding, diaphragm_breathing, worry_time
   Kullanıcı "denedim yaradı" derse "yararlı"; "olmuyor" derse "yararsız"
   Chatbot önerdi ama kullanıcı henüz denemediyse "deneyecek"

4. add_modules (list[str]):
   Konuşmada değinilen modüller. Sadece bunlar:
   health_anxiety, panic, gad, depression, low_self_esteem, insomnia,
   work_stress, relationship_stress, grief_loss, life_transitions, trauma_awareness

5. progress_note (str, opsiyonel):
   Bir cümlelik klinik-tarzı ilerleme notu. SADECE somut bir ilerleme/gerileme fark ettiysen.
   Örnek: "3 haftadır nabız kontrolü sıklığı azaldığını bildirdi"
   Belirsizse null bırak.

FORMAT — sadece geçerli JSON döndür, başka hiçbir şey:
{"add_triggers":[],"add_themes":[],"coping_updates":{},"add_modules":[],"progress_note":null}

ÖRNEKLER:

Turn:
User: "Bugün annemle çok kötü bir tartışma yaşadım, sonra da nabzımı sürekli kontrol etmeye başladım."
Assistant: "Sen bu durumda kontrol davranışını fark etmişsin, güzel. Bir sonraki dürtüde 90 saniye bekle egzersizini deneyebilir misin?"

Çıkarım:
{"add_triggers":["annesiyle tartışma"],"add_themes":[],"coping_updates":{"urge_surfing":"deneyecek"},"add_modules":["health_anxiety"],"progress_note":"kontrol davranışı örüntüsünü kendisi fark etti"}

Turn:
User: "İyiyim bugün."
Assistant: "Bu güzel. Nasıl hissettiğini paylaşmak istediğin bir şey var mı?"

Çıkarım:
{"add_triggers":[],"add_themes":[],"coping_updates":{},"add_modules":[],"progress_note":null}

Turn:
User: "Geçen konuşmada söylediğin nefes egzersizini denedim, hiç işe yaramadı."
Assistant: "Bunu duyduğuma üzüldüm. Diyafram nefesinin bazı kişilerde işe yaramaması normal — birlikte başka bir teknik bulalım."

Çıkarım:
{"add_triggers":[],"add_themes":[],"coping_updates":{"diaphragm_breathing":"yararsız"},"add_modules":[],"progress_note":null}"""


def extract_profile_patch(
    user_message: str,
    response_text: str,
    current_profile_summary: Optional[str] = None,
) -> ProfilePatch:
    """Turn'den ProfilePatch üret. LLM hatası → boş patch (idempotent no-op)."""

    user_prompt = (
        f"KULLANICI MESAJI:\n\"\"\"{user_message}\"\"\"\n\n"
        f"ASİSTAN CEVABI:\n\"\"\"{response_text}\"\"\"\n\n"
    )
    if current_profile_summary:
        user_prompt += f"MEVCUT PROFİL ÖZETİ (referans):\n\"\"\"{current_profile_summary}\"\"\"\n\n"
    user_prompt += "Şimdi çıkarım JSON'unu üret:"

    try:
        resp = llm_adapter.llm_complete(
            system=_EXTRACTOR_SYSTEM_TR,
            user=user_prompt,
            model=config.LLM_MODEL_INTENT,   # Haiku — ucuz
            max_tokens=300,
            temperature=0.0,
            redact=True,                      # KVKK: PII scrub
        )
    except Exception:
        return ProfilePatch()   # boş — sessiz fail

    # Parse
    m = re.search(r"\{.*\}", resp.text, flags=re.DOTALL)
    if not m:
        return ProfilePatch()
    try:
        data = json.loads(m.group(0))
    except Exception:
        return ProfilePatch()

    # Validate + coerce
    def _clean_list(v, max_len=10):
        if not isinstance(v, list):
            return []
        return [str(x).strip()[:80] for x in v if x and isinstance(x, (str, int))][:max_len]

    def _clean_dict(v, max_len=15):
        if not isinstance(v, dict):
            return {}
        allowed_values = {"yararlı", "yararsız", "denenmedi", "deneyecek"}
        out = {}
        for k, val in list(v.items())[:max_len]:
            k = str(k).strip()[:40]
            val = str(val).strip().lower()
            if val in allowed_values and k:
                out[k] = val
        return out

    allowed_modules = {
        "health_anxiety", "panic", "gad", "depression", "low_self_esteem",
        "insomnia", "work_stress", "relationship_stress", "grief_loss",
        "life_transitions", "trauma_awareness",
    }
    modules = [m for m in _clean_list(data.get("add_modules", []), max_len=5)
               if m in allowed_modules]

    progress_note = data.get("progress_note")
    if progress_note is not None:
        progress_note = str(progress_note).strip()[:200]
        if not progress_note or progress_note.lower() in ("null", "none"):
            progress_note = None

    return ProfilePatch(
        add_triggers=_clean_list(data.get("add_triggers", []), max_len=5),
        add_themes=_clean_list(data.get("add_themes", []), max_len=3),
        coping_updates=_clean_dict(data.get("coping_updates", {})),
        add_modules=modules,
        progress_note=progress_note,
    )


def format_profile_for_composer(profile: dict) -> str:
    """UserProfile row'undan composer system prompt'una girecek özet üret.

    ~200-400 char, insan-okunabilir Türkçe. Boş profile → boş string.
    """
    if not profile:
        return ""

    parts = []
    triggers = profile.get("triggers") or []
    themes = profile.get("themes") or []
    coping = profile.get("coping_tried") or {}
    modules = profile.get("modules_engaged") or []
    progress = profile.get("progress_notes") or []

    if triggers:
        parts.append(f"Sık tetikleyiciler: {', '.join(triggers[:5])}.")
    if themes:
        parts.append(f"Tekrarlayan temalar: {', '.join(themes[:3])}.")
    if coping:
        useful = [k for k, v in coping.items() if v == "yararlı"]
        useless = [k for k, v in coping.items() if v == "yararsız"]
        will_try = [k for k, v in coping.items() if v == "deneyecek"]
        subparts = []
        if useful:
            subparts.append(f"yararlı bulduğu: {', '.join(useful[:3])}")
        if useless:
            subparts.append(f"işe yaramadığını söylediği: {', '.join(useless[:3])}")
        if will_try:
            subparts.append(f"deneyeceğini söylediği: {', '.join(will_try[:3])}")
        if subparts:
            parts.append("Egzersizler: " + "; ".join(subparts) + ".")
    if modules:
        parts.append(f"Konuştuğu konular: {', '.join(modules[:5])}.")
    if progress:
        # En son 2 notu al
        parts.append("İlerleme: " + " ".join(progress[-2:]))

    return " ".join(parts)


if __name__ == "__main__":
    # Smoke test
    patch = extract_profile_patch(
        user_message="Bugün annemle çok kötü bir tartışma yaşadım, sonra nabzımı sürekli kontrol etmeye başladım.",
        response_text="Kontrol davranışını fark etmişsin, güzel. 90 saniye bekle egzersizini deneyebilir misin?",
    )
    print("Extracted patch:")
    print(f"  triggers: {patch.add_triggers}")
    print(f"  themes:   {patch.add_themes}")
    print(f"  coping:   {patch.coping_updates}")
    print(f"  modules:  {patch.add_modules}")
    print(f"  progress: {patch.progress_note}")
