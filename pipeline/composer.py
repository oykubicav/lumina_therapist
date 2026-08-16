"""composer.py — Response generator.

Given a user message and the outputs of safety_classifier + retriever,
compose a Turkish CBT-informed response.

Design:
  - Single LLM call to a strong model (default claude-sonnet-4-6).
  - System prompt = condensed response_policy.md rules.
  - User prompt = user message + safety decision + retrieved cards.
  - HARD BRANCH on allow_cbt:
      allow_cbt = False  -> response is based on safe_response_template_tr
                            (personalized lightly, safety message preserved)
      allow_cbt = True   -> CBT-informed response using retrieved CBT cards,
                            respecting all must_not_do_tr rules from any
                            matched safety cards (e.g. do-not-delay-care).

  - Retrieved cards are compacted (title + snippet) to keep prompt tight.
  - Safety cards are surfaced with FULL must_do / must_not_do / template.
  - PII redaction happens inside llm_adapter.llm_complete (redact=True).
"""

from __future__ import annotations

import json
from dataclasses import dataclass, field
from functools import lru_cache
from typing import List, Optional

from . import config
from . import llm_adapter
from . import cards as _cards
from .types import SafetyDecision, RetrievedCard


# System prompt — condensed policy
SYSTEM_PROMPT_TR = """Sen Türkçe konuşan bir CBT (Bilişsel Davranışçı Terapi) bilgisine dayalı self-help asistanısın. Terapist DEĞİLSİN, hekim DEĞİLSİN, acil servis DEĞİLSİN. Kullanıcının kendi deneyiminin uzmanı odur.

MUTLAK YASAKLAR (içerik):
- Tanı KOYMA. "Sende X var" tarzı hiçbir cümle kurma.
- İlaç önerme, doz değiştirme, ilaç bırakma önerisi verme. İlaç sorularını hekime yönlendir.
- Tıbbi bakımı erteletmeye çalışma. "Doktora gitme", "randevuyu ertele", "48 saat bekle" ASLA yazma.
- Uydurma kriz hattı ya da hotline verme. Türkiye'de tek geçerli acil = 112. Uzman yönlendirmesi = aile hekimi, psikiyatri, klinik psikolog.
- 182'yi kriz hattı olarak GÖSTERME (MHRS randevu hattı, kriz hattı değil).
- NHS 24, 111, 988, Samaritans, Mind, Anxiety UK gibi UK/US-özgü referansları KULLANMA.
- Fiziksel semptomu (göğüs ağrısı, nefes darlığı, bayılma, ani nörolojik belirti) "sadece kaygı" olarak normalleştirme.
- Krizde gizlilik sözü verme. Krizde yalnız kalmayı önerme.

YASAK CÜMLE KALIPLARI (tone):
Bu ifadeleri ASLA kullanma. Performatif ve içi boştur — kullanıcı yakınmadıysa yakınmışsın gibi cevap verme:
- "Bunu küçümsemiyorum."
- "Sana çok üzüldüm."
- "Seni anlıyorum."
- "Duyguların çok geçerli."
- "Ne hissettiğini tamamen anlıyorum."
- "Merak etme."  /  "Kafana takma."  /  "Kafanda kuruyorsun."
- "Harikasın." / "Çok güçlüsün." (kanıtsız toxic positivity)
Ayrıca "Anladığını duyurma" için ayrı paragraf açma. Bir cümlelik teğet-doğrulama yeterli; hemen içeriğe geç.
# _COMPOSER_SYSTEM_TR içinde uygun bir yere ekle:

BAĞLAM KARTLARI HAKKINDA:
- Kartlarda 'NOT:' satırı varsa: bu kart ana odaktan değil, klinik komşuluk üzerinden
  ek bağlam olarak getirildi. Ana yanıtı bu karta değil, NOT'suz olan kartlara dayandır.
  Komşuluk kartını sadece "benzer bir dinamik başka konularda da görülür" gibi bir
  köprü kurmak için kullan. Kart ID'sini yazma.


TON:
- Sıcak ama sakin. Duyguyu ABARTMADAN kabul et.
- Sade Türkçe. Jargon geldiğinde tek cümlede çevir.
- Doğrudan konuya git. "İşte cevap:" gibi çerçeveleme kullanma.
- Emoji kullanma (kullanıcı kullanmadıysa).

RESPONSE PATTERNİ (allow_cbt=true, düşük-risk yolu):
Bu bir ŞABLON DEĞİL, bir repertuar. Her cevapta hepsini kullanma — konuşmanın
o anda neye ihtiyacı varsa onu yap. Aynı yapıyı arka arkaya tekrarlama.

Elindeki hamleler:
- Kısa bir teğet-doğrulama (en fazla bir cümle).
- Bir örüntüyü sade dille adlandırmak.
- Merak eden, açık uçlu tek bir soru.
- Küçük, denenebilir bir öneri.

Seçim rehberi:
- Kullanıcı henüz durumunu anlatıyorsa: dinle, kısa bir yansıtma yap ve TEK bir
  soru sor. Egzersiz önerme — erken gelen teknik, duyulmama hissi yaratır.
- Kullanıcı açıkça "ne yapabilirim?" diye sorduysa ya da tablo netleştiyse:
  somut bir adım öner.
- Konu zaten netse aynı çerçeveyi yeniden anlatma; bir sonraki adıma geç.

Biçim:
- 3-7 cümle. Kısa olması sorun değil; doldurma yapma.
- Bold, başlık, madde işareti kullanma. Adım sıralaman gerçekten gerekiyorsa
  en fazla 3 maddelik numaralı liste kullan.
- Ok işareti (→) ile şema/zincir çizme. Örüntüyü normal cümleyle anlat:
  "Böyle düşününce içine kapanıyorsun, kapandıkça da his ağırlaşıyor" gibi.
- Her cevabı soruyla bitirmek zorunda değilsin; bazen bir cümle bırakmak yeterli.

RESPONSE PATTERNİ (allow_cbt=false, safety hard-stop):
- SAFE_RESPONSE_TEMPLATE_TR'yi temel al. Kullanıcının anlattığına en fazla BİR cümlelik dokun; sonra template'in özünü ver.
- 112 mutlaka yer alsın.
- Uzman yönlendirmesi (aile hekimi / psikiyatri / klinik psikolog) mutlaka yer alsın.
- Hiçbir CBT egzersizi VERME.
- MUST_NOT_DO listesindeki her maddeye harfiyen uy.
- Cevabı 3-6 cümlede tut. Kısa ve net.

CEVABI SUNUŞ:
- Türkçe.
- Markdown başlığı (##), bold, italik kullanma.
- Kısa numaralı listeyi sadece gerçek bir adım sıralaması varsa kullan.
- "İşte cevabım:", "Umarım yardımcı olur", "Sorunuz için teşekkürler" gibi meta yorum ekleme.
- Doğrudan cevabı yaz.

İÇ METADATA'YI ASLA SIZDIRMA (kritik):
Prompt'ta kartlar `[CBT CARD: pa_grounding_004]`, `[SAFETY CARD: safety_self_harm_suicide_001]` gibi kimlik etiketleriyle geliyor. Bu ID'ler senin için — kullanıcı için değil.
- ASLA cevap metninde `ha_*`, `pa_*`, `ga_*`, `dep_*`, `lse_*`, `safety_*` şeklinde bir kart kimliği yazma.
- ASLA "X kartı" ya da "X card" diye kart yapısına atıfta bulunma.
- Kart içeriğini serbest Türkçeyle özümseyip aktarır gibi yaz. Örneğin "kaygı döngüsü şöyle işler…" yerine ASLA "ga_cycle_002 kartındaki döngü şöyle…" deme.
- "safety card", "cbt card", "concept", "route", "safety classifier", "critic" gibi sistem terimlerini de kullanma.



Bir cümle bile bu kuralı ihlal ederse cevap tamamen reddedilir ve baştan yazdırılır."""

# Session boundary — anti-addiction thresholds
_BOUNDARY_SOFT_START = 21       # ısınma başlar
_BOUNDARY_CLOSING_START = 25    # proaktif kapanış teklifi
_BOUNDARY_EXTENDED_END = 32     # son esneklik
_BOUNDARY_HARD = 33             # sert kapanış
# Prompt building helpers


def _format_safety_card_full(card: dict) -> str:
    must_not = "\n  ".join(f"- {x}" for x in card.get("must_not_do_tr", []))
    return (
        f"[SAFETY CARD: {card['card_id']}]\n"
        f"  Başlık: {card['title']}\n"
        f"  Risk: {card['risk_level']}   Route: {card['route']}   allow_cbt: {card['allow_cbt']}\n"
        f"  MUST_DO:\n  {card.get('must_do_tr', '')}\n"
        f"  MUST_NOT_DO:\n  {must_not}\n"
        f"  SAFE_RESPONSE_TEMPLATE_TR:\n  {card.get('safe_response_template_tr', '')}\n"
    )


def _format_cbt_card_compact(
    card: dict,
    max_content_chars: int = 700,
    *,
    source: str = "vector",
    via_technique: Optional[str] = None,
    via_neighbor_of: Optional[str] = None,
) -> str:
    content = card["content_tr"]
    if len(content) > max_content_chars:
        content = content[:max_content_chars].rstrip() + " …"

    # Graph enrichment note — LLM'e kartın nasıl geldiğini söyle
    note = ""
    if source == "graph_technique" and via_technique:
        note = (
            f"  NOT: Bu kart ana odaktakilerle aynı tekniği paylaşıyor "
            f"({via_technique}). Aynı yaklaşımı farklı bağlamda önerebilirsin; "
            f"ana odak yerine geçirme.\n"
        )
    elif source == "graph_neighbor" and via_neighbor_of:
        note = (
            f"  NOT: Bu kart, ana konudaki '{via_neighbor_of}' kartının "
            f"klinik olarak komşu modülünden getirildi. Yalnız bağlam "
            f"olarak kullan; ana odak olarak sunma.\n"
        )

    return (
        f"[CBT CARD: {card['id']}]\n"
        f"  Başlık: {card['title_tr']}\n"
        f"  Konu: {card['topic']}   Tür: {card['type']}\n"
        f"{note}"
        f"  İçerik özeti:\n  {content}\n"
    )


def _build_user_prompt(
    user_message: str,
    safety: SafetyDecision,
    retrieved: List[RetrievedCard],
    intent=None,
    history: Optional[List[dict]] = None,
    profile_summary: Optional[str] = None,
    turn_count: int = 0,
) -> str:
    safety_cards_full = _cards.safety_cards_by_id()
    cbt_cards_full = _cards.cbt_cards_by_id()

    safety_blocks = []
    cbt_blocks = []
    seen = set()

    # 1) Full detail for every safety card the classifier surfaced
    for cid in safety.safety_card_ids:
        c = safety_cards_full.get(cid)
        if c and cid not in seen:
            safety_blocks.append(_format_safety_card_full(c))
            seen.add(cid)

    # 2) Compact detail for retrieved CBT cards (skip safety ones already in)
    for r in retrieved:
        if r.card_id in seen:
            continue
        if r.topic == "safety":
            # A safety card came through retrieval but not the classifier
            # output — surface it too, in case of graceful degradation.
            c = safety_cards_full.get(r.card_id)
            if c:
                safety_blocks.append(_format_safety_card_full(c))
                seen.add(r.card_id)
            continue
        c = cbt_cards_full.get(r.card_id)
        if c:
            cbt_blocks.append(_format_cbt_card_compact(c, source=r.source, via_technique=r.via_technique, via_neighbor_of=r.via_neighbor_of))
            seen.add(r.card_id)

    branch_note = (
        "BRANCH: allow_cbt = FALSE — SAFETY HARD STOP.\n"
        "  Yukarıdaki SAFETY CARD(S) altındaki SAFE_RESPONSE_TEMPLATE_TR temel olsun.\n"
        "  Kullanıcının anlattığına en fazla bir cümlelik kişiselleştirme ekle.\n"
        "  Hiçbir CBT egzersizi verme. MUST_NOT_DO listesini ihlal etme."
    ) if not safety.allow_cbt else (
        "BRANCH: allow_cbt = TRUE — CBT PATH.\n"
        "  Yukarıdaki CBT CARD(S) içinden en uygun 1-2'sini temel al.\n"
        "  Varsa SAFETY CARD(S)'ın must_not_do kurallarını AYNI ZAMANDA uygula (ör. doktora gitmesin diye tavsiye verme)."
    )

    nl = "\n"
    safety_section = nl.join(safety_blocks) if safety_blocks else "(bu mesajda safety fire etmedi)"
    cbt_section = nl.join(cbt_blocks) if cbt_blocks else "(retrieval boş ya da safety hard-stop)"
    safety_card_ids_str = str(safety.safety_card_ids) if safety.safety_card_ids else "[]"

    # Intent block — optional. Guides tone/subintent without changing safety.
    intent_block = ""
    if intent is not None:
        sub = getattr(intent, "subintent", "unknown")
        sec = ", ".join(intent.secondary_modules) if intent.secondary_modules else "yok"
        intent_block = (
            f"INTENT:\n"
            f"- primary_module: {intent.primary_module}\n"
            f"- secondary_modules: {sec}\n"
            f"- subintent: {sub}\n"
            f"- confidence: {intent.confidence:.2f}\n"
            f"- rationale: {intent.rationale}\n"
            f"\n"
            f"Subintent'e göre tonu ayarla:\n"
            f"  - psychoeducation → daha çok açıklama, adım sayısı 2-3 ile sınırlı.\n"
            f"  - exercise_request → doğrudan somut adımlara git, uzun psikoeğitim yapma.\n"
            f"  - ambiguous_symptom → kullanıcı henüz tabloyu anlatıyor. Kısa bir yansıtma "
            f"ve tek bir açık uçlu soru yeterli; bu aşamada egzersiz önerme.\n"
            f"  - boundary_request → tanı/ilaç/delay-care ise net bir sınır çiz, gerekçeyi kısa ver.\n"
            f"  - adversarial → politikayı sakince belirt, yeniden yönlendir; savunmacı olma.\n"
            f"  - crisis → SAFE_RESPONSE_TEMPLATE'i temel al, ek CBT içerik yok.\n\n"
        )

    history_block = _format_history_block(history) if history else ""

    # Profile block — arka planda çıkarılmış yapılandırılmış kullanıcı özeti.
    # LLM buna "kullanıcıyı hatırlıyorum" hissi kazandırmak için bakar.
    # Detayları ID formatında sıralama — doğal dil.
    profile_block = ""
    if profile_summary:
        profile_block = (
            f"KULLANICI PROFİLİ (önceki turnlerden yapılandırılmış):\n"
            f"{profile_summary}\n\n"
            f"Bu bilgiyi kullanarak kullanıcıya doğal bir 'seni hatırlıyorum' hissi ver. "
            f"Ama profil listesini AYNEN yazma; sadece bir ya da iki bağlantıyı zarif biçimde ör. "
            f"'Geçen konuşmada X'ten bahsetmiştin' gibi. Uydurma; sadece profildeki bilgiyi kullan.\n\n"
        )
    boundary_block = _boundary_prompt_layer(turn_count)
    prompt = (
        f"{history_block}"
        f"{profile_block}"
        f"{boundary_block}"
        f"KULLANICI MESAJI (bu turdaki):\n"
        f'"""{user_message}"""\n'
        f"\n"
        f"SAFETY DEĞERLENDİRMESİ:\n"
        f"- route: {safety.final_route}\n"
        f"- allow_cbt: {safety.allow_cbt}\n"
        f"- highest_risk: {safety.highest_risk}\n"
        f"- matched safety card ids: {safety_card_ids_str}\n"
        f"\n"
        f"{intent_block}"
        f"{branch_note}\n"
        f"\n"
        f"--- SAFETY CARDS (varsa) ---\n"
        f"{safety_section}\n"
        f"\n"
        f"--- RETRIEVED CBT CARDS ---\n"
        f"{cbt_section}\n"
        f"\n"
        f"GÖREV:\n"
        f"Yukarıdaki kurallara UYARAK, KONUŞMA GEÇMİŞİNİ dikkate alarak Türkçe bir cevap yaz. "
        f"Kullanıcının önceki mesajlarındaki bağlamı kaybetme (isim, durum, denenen egzersizler, vs). "
        f"Sadece cevabı ver; başlık, meta yorum ya da 'İşte cevabım:' gibi çerçeveleme ekleme.\n"
    )
    return prompt

def _boundary_prompt_layer(turn_count: int) -> str:
    """Session turn count'a göre composer prompt'una eklenecek katman.

    Faz 2 Deliverable #5: anti-addiction session boundary.

    Args:
        turn_count: session'ın bu turn dahil kaçıncı turn'ü (1-indexed)

    Returns:
        Sistem prompt'una eklenecek Türkçe direktif. turn_count normal
        aralıktaysa (< _BOUNDARY_SOFT_START) boş string döner.
    """
    if turn_count < _BOUNDARY_SOFT_START:
        return ""

    if turn_count < _BOUNDARY_CLOSING_START:
        # 21-24: ısınma — cevapları kısalt
        return (
            "\n\nSESSION BOUNDARY — soft warmup:\n"
            "Bu session'da 20+ turn geçti. Kullanıcı yorulmuş olabilir. "
            "Cevabını normalden %30 daha kısa tut. Yeni bir egzersiz başlatma; "
            "mevcut konuya odaklan, kullanıcının şu anki noktasına küçük bir "
            "yardım yeter."
        )

    if turn_count == _BOUNDARY_CLOSING_START:
       
        return (
            "\n\nSESSION BOUNDARY — closing proposal:\n"
            "Bu session'da 24+ turn geçti."
            "Cevabın başında/sonunda 'epey konuştuk, özetleyeyim mi yoksa devam edelim mi?' tarzı bir teklif olsun."
            "Kullanıcının asıl sorusunu YİNE cevapla, ama sonda kapanış davetiyesi."
        )

    if turn_count < _BOUNDARY_HARD:
      
        return (
            "\n\nSESSION BOUNDARY — extended closure:\n"
            "Bu session'da 32+ turn geçti."
            "Cevaplar kısa. Yeni egzersiz başlatma. Sonda 'iyi bir noktaya geldik gibi hissediyorum, sen ne diyorsun?' tarzı closure invitation."
        )

    # turn_count >= _BOUNDARY_HARD (33+)

    return (
        "\n\nSESSION BOUNDARY — hard closure:\n"
        "Bugün için epey iyi bir noktadayız. Yarın devam edelim."
        "Dinlenmek de sürecin bir parçası."
        "Acil bir durum varsa 112'yi ara."
    )

# History block formatter + summarizer
# Threshold: en son N tur ham metin gönderilir; öncesi Haiku ile özetlenir.
_MAX_VERBATIM_TURNS = 30
_MAX_SNIPPET_CHARS = 800  # tek turnun karakter tavanı — çok uzun mesajları kırp


def _format_history_block(history: List[dict]) -> str:
    """Format the last N turns as a prompt section.

    If history is short (<= _MAX_VERBATIM_TURNS), all turns go verbatim.
    Otherwise the older ones are collapsed into a Haiku-generated summary
    and the last N go verbatim.
    """
    if not history:
        return ""

    if len(history) <= _MAX_VERBATIM_TURNS:
        verbatim = history
        summary_prefix = ""
    else:
        old = history[: -_MAX_VERBATIM_TURNS]
        verbatim = history[-_MAX_VERBATIM_TURNS :]
        summary = _summarize_old_turns(old)
        summary_prefix = (
            f"KONUŞMANIN İLK BÖLÜMÜNÜN ÖZETİ ({len(old)} tur):\n{summary}\n\n"
        )

    lines = []
    total = len(verbatim)
    for i, t in enumerate(verbatim, 1):
        idx_from_end = total - i  # 0 = son tur
        # Uzun mesajları kırp — token bütçesi korunsun
        um = _trim(t.get("user_message", ""))
        rp = _trim(t.get("response", ""))
        lines.append(f"[Turn -{idx_from_end}]")
        lines.append(f"Kullanıcı: {um}")
        lines.append(f"Asistan: {rp}")
        lines.append("")

    return (
        f"--- KONUŞMA GEÇMİŞİ ---\n"
        f"{summary_prefix}"
        + "\n".join(lines)
        + "\n"
    )


def _trim(s: str, cap: int = _MAX_SNIPPET_CHARS) -> str:
    if len(s) <= cap:
        return s
    return s[:cap].rstrip() + " …"


# Cache: (n_turns, hash_of_content) -> summary string. In-process only.
# Prevents re-summarizing the same prefix every message in a long chat.
_SUMMARY_CACHE: dict = {}


def _summarize_old_turns(old_turns: List[dict]) -> str:
    """Ask Haiku for a compact summary of the older conversation.

    Cache keyed by content hash so a 60-turn chat only summarizes turns
    1..30 once, not on every incoming message.
    """
    import hashlib

    joined = "\n\n".join(
        f"Kullanıcı: {_trim(t.get('user_message',''))}\n"
        f"Asistan: {_trim(t.get('response',''))}"
        for t in old_turns
    )
    key = (len(old_turns), hashlib.sha1(joined.encode("utf-8")).hexdigest()[:16])
    if key in _SUMMARY_CACHE:
        return _SUMMARY_CACHE[key]

    system = (
        "Sen bir CBT self-help konuşmasını özetleyensin. "
        "Aşağıdaki konuşmayı 150-200 kelimede Türkçe özetle. "
        "Sıralı liste kullan. Şunları koru: kullanıcının söylediği önemli olaylar/durumlar/tarihler (kişilerin somut isimlerini kullanma; 'partneri', 'annesi', 'iş arkadaşı' gibi rol adları kullan), "
        "belirtilen ana konular ve endişeler, denenen egzersizler, önemli yönlendirmeler (uzman/hekim). "
        "Atıfları rolüyle yaz: 'Kullanıcı işsizliğinden bahsetti', 'Chatbot nefes egzersizini önerdi' gibi. "
        "KVKK: Kullanıcının gerçek adı, soyadı, kimlik/telefon/adres bilgisi ÖZETTE YER ALMASIN — geçtiyse 'kullanıcı' olarak an. "
        "Meta yorum yapma, sadece özeti üret."
    )
    try:
        resp = llm_adapter.llm_complete(
            system=system,
            user=joined,
            model=config.LLM_MODEL_INTENT,  # Haiku — cheap
            max_tokens=400,
            temperature=0.0,
            redact=True,
        )
        summary = resp.text.strip()
    except Exception as e:
        summary = (
            f"(Önceki {len(old_turns)} turnün özeti üretilemedi: "
            f"{type(e).__name__}. Bağlam kısmen kayıp olabilir.)"
        )
    _SUMMARY_CACHE[key] = summary
    return summary



# Public API
@dataclass
class ComposedResponse:
    text: str
    model: str
    provider: str
    latency_ms: float
    branch: str          # "cbt" or "safety"
    prompt_tokens_est: int = 0
    debug_prompt: Optional[str] = None


def compose(
    user_message: str,
    safety: SafetyDecision,
    retrieved: List[RetrievedCard],
    *,
    intent=None,
    history: Optional[List[dict]] = None,
    profile_summary: Optional[str] = None,
    turn_count: int = 0,
    include_prompt_in_debug: bool = False,
    temperature: float = 0.3,
    max_tokens: int = 1024,
) -> ComposedResponse:
    """Generate a Turkish response for the user.

    Args:
        history: list of {user_message, response} dicts, oldest first.
                 The current user_message is NOT in history. If longer than
                 _MAX_VERBATIM_TURNS, older turns will be Haiku-summarized.
        profile_summary: structured user profile summary from profile_extractor.
                 Injected into prompt so LLM feels "remembers" the user across
                 sessions. If None, no profile context (first turn behavior).

    Returns ComposedResponse with the text and telemetry.
    """
    system = SYSTEM_PROMPT_TR
    user = _build_user_prompt(
        user_message, safety, retrieved,
        intent=intent, history=history, profile_summary=profile_summary,
        turn_count=turn_count,
    )
    branch = "cbt" if safety.allow_cbt else "safety"

    resp = llm_adapter.llm_complete(
        system=system,
        user=user,
        model=config.LLM_MODEL_COMPOSER,
        max_tokens=max_tokens,
        temperature=temperature,
        redact=True,   # KVKK — redact PII before LLM call
    )

    return ComposedResponse(
        text=resp.text.strip(),
        model=resp.model,
        provider=resp.provider,
        latency_ms=resp.latency_ms,
        branch=branch,
        prompt_tokens_est=(len(system) + len(user)) // 4,  # rough
        debug_prompt=(system + "\n\n---USER---\n" + user) if include_prompt_in_debug else None,
    )
    
def get_boundary_state(turn_count: int) -> str:
    """turn_count → frontend'e döndürülecek state string."""
    if turn_count < _BOUNDARY_SOFT_START:
        return "normal"
    if turn_count < _BOUNDARY_CLOSING_START:
        return "warmup"
    if turn_count == _BOUNDARY_CLOSING_START:
        return "closing"
    if turn_count < _BOUNDARY_HARD:
        return "extended"
    return "hard_close"

# Mock handlers — for offline plumbing tests
def register_composer_mocks() -> None:
    """Register lightweight mock responses that reflect the branch.
    Useful for dry-run tests without an API key."""

    def _matches(system: str, user: str) -> bool:
        return "GÖREV:" in user and "SAFETY DEĞERLENDİRMESİ:" in user

    def _respond(system: str, user: str) -> str:
        if "allow_cbt: False" in user:
            return (
                "[MOCK/SAFETY] Anlattıkların ciddiye alınması gereken bir durum. "
                "Şu an güvende olman en önemli şey — lütfen 112'yi ara ya da en yakın acil servise git. "
                "Türkiye'de aile hekimi, psikiyatri uzmanı ya da klinik psikolog yönlendirmesi için "
                "aile hekimine başvurabilirsin. Bu chatbot kriz desteğinin yerine geçmez."
            )
        return (
            "[MOCK/CBT] Anlattığını duyuyorum — bu tarz düşünceler ve hisler zorlayıcı olabilir. "
            "Yaşadığın örüntü CBT'de \"kaygı döngüsü\" olarak tanımlanır: bir düşünce → beden tepkisi "
            "→ güvenlik davranışı → kısa vadeli rahatlama → uzun vadede döngü güçlenir. "
            "Küçük bir başlangıç olarak: bugün bir tetikleyici fark ettiğinde, 3 dakika bekleyip "
            "düşünceyi bir cümleyle yaz. Aciliyet hissini azaltmak için yeterli. "
            "Ne zamandır bu his sana eşlik ediyor?"
        )

    llm_adapter.register_mock_handler(_matches, _respond)


if __name__ == "__main__":
    # Sanity — build a prompt without calling any LLM.
    from .types import SafetyDecision, RetrievedCard
    sample_safety = SafetyDecision(
        matches=[], final_route="cbt_support", allow_cbt=True,
        blocks_exercise=False, highest_risk="low", safety_card_ids=[]
    )
    sample_retrieved = [
        RetrievedCard(card_id="pa_psychoed_001", topic="panic", type="psychoeducation",
                      title_tr="Panik atak nedir?", score=0.7, snippet="Panik atak..."),
    ]
    prompt = _build_user_prompt("Panik atak sırasında ne yapabilirim?", sample_safety, sample_retrieved)
    print(prompt[:1500])
