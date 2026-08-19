"""API-side card helpers.

Raw JSON loading lives in pipeline.cards (single source of truth).
This module is just thin API-facing sugar:
  - Turkish display names for topics
  - filter helper for /cards route
"""

from __future__ import annotations

from collections import Counter
from typing import Optional, List

from pipeline import cards as _cards


TOPIC_DISPLAY_TR = {
    "health_anxiety": "Sağlık Kaygısı",
    "panic": "Panik",
    "gad": "Yaygın Kaygı",
    "depression": "Depresyon",
    "low_self_esteem": "Düşük Öz-Değer",
    "insomnia": "Uykusuzluk",
    "work_stress": "İş Stresi",
    "relationship_stress": "İlişki Stresi",
    "grief_loss": "Yas ve Kayıp",
    "life_transitions": "Yaşam Geçişleri",
    "trauma_awareness": "Travma Farkındalığı",
    "social_anxiety": "Sosyal Kaygı",
}

TOPICS_ORDER = ["health_anxiety", "panic", "gad", "depression", "low_self_esteem", "insomnia", "work_stress", "relationship_stress", "grief_loss", "life_transitions", "trauma_awareness", "social_anxiety"]


def filter_cbt_cards(
    topic: Optional[str] = None,
    type_: Optional[str] = None,
    q: Optional[str] = None,
) -> List[dict]:
    result = _cards.all_cbt_cards()
    if topic:
        result = [c for c in result if c["topic"] == topic]
    if type_:
        result = [c for c in result if c["type"] == type_]
    if q:
        q_low = q.lower()
        result = [c for c in result if q_low in c["title_tr"].lower()]
    return result


def topic_counts() -> dict:
    return dict(Counter(c["topic"] for c in _cards.all_cbt_cards()))
