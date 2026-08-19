"""Cards + ontology + registry → Neo4j graph.
Kullanım: python -m graph.migrate
"""
import csv
import json
import re

from . import config
from .driver import get_driver, close_driver
from .schema import create_schema

# Modül komşulukları — klinik gerçekten yakın olanlar
MODULE_NEIGHBORS = [
    ("panic", "health_anxiety"),
    ("depression", "insomnia"),
    ("depression", "low_self_esteem"),
    ("depression", "grief_loss"),
    ("gad", "insomnia"),
    ("relationship_stress", "trauma_awareness"),
    ("grief_loss", "life_transitions"),
    ("work_stress", "depression"),
    ("life_transitions","depression"),
    ("social_anxiety", "low_self_esteem"),
    ("social_anxiety", "gad"),
    ("social_anxiety", "panic"),
]


# Technique regex — kart içeriklerinden çıkarılan gerçek Türkçe terimler
# Prensip: her teknik için birden fazla yazım varyantı  Aynı tekniği
# farklı kartlar farklı kelimelerle anlatıyor olabilir.
TECHNIQUE_PATTERNS = {
    # ---- Kognitif teknikler ----
    "thought_record": [
        r"düşünce kayd",                    # düşünce kaydı / kaydını
        r"lehinde.*aleyhinde",               # 6-adım kaydın parçası
        r"lehinde kanıt", r"aleyhinde kanıt",
        r"otomatik düşünce", r"otomatik felaket",
        r"daha dengeli düşünce",
        r"altı soru", r"yedi soru", r"beş soru",  # kartlar N-soru diyor
        r"0-100.*inan",                      # inanma puanı
    ],
    "cognitive_reframing": [
        r"yeniden değerlendir", r"yeniden çerçevele",
        r"bilişsel yeniden yapı", r"düşünceyi sorgu",
    ],

    # ---- Davranışsal ----
    "behavioural_activation": [
        r"davranışsal aktivasyon", r"davranış planlama",
        r"küçük adım", r"küçük başla", r"aktivite planla",
    ],
    "exposure_gradual": [
        r"maruz kalma", r"kademeli maruz",
        r"korku hiyerarşisi", r"kaçındığın.*kademeli",
    ],
    "interoceptive_exposure": [
        r"iç algı maruz", r"interoseptif",
        r"bedensel duyum.*tekrar",
    ],

    # ---- Grounding / duyu ----
    "grounding": [
        r"grounding", r"topraklan", r"topraklama",
        r"5-4-3-2-1",
        r"görebildiğin \d+", r"dokunabildiğin \d+", r"duyabildiğin \d+",
    ],
    "diaphragm_breathing": [
        r"diyafragmatik", r"diyafram nefes",
        r"karın nefesi", r"uzun ekshalasyon",
        r"yavaş nefes", r"hiperventilasyon",
    ],
    "progressive_muscle_relaxation": [
        r"aşamalı kas gevşetme", r"PMR",
        r"kasları.*gev",
    ],

    # ---- GAD ----
    "worry_time": [
        r"endişe zamanı", r"kaygı zamanı",
        r"endişeyi ertele", r"endişe erteleme", r"kaygı erteleme",
    ],
    "problem_solving": [
        r"problem çöz", r"6 adımlı problem",
        r"olası çözümler", r"adım.*çözüm",
    ],

    # ---- LSE / self-compassion ----
    "self_compassion": [
        r"öz-şefkat", r"öz şefkat", r"kendine şefkat",
        r"yakın arkadaş.*söyler", r"self-compassion",
    ],
    "assertiveness": [
        r"assertif", r"'?hayır'? demek",
        r"hayır demenin", r"birden.*hayır",
    ],

    # ---- İlişki / Gottman ----
    "four_horsemen_antidotes": [
        r"dört atlı", r"dört yıpratıcı",
        r"four horsemen",
        r"eleştiri.*aşağılama",
        r"savunmacılık.*duvar",
        r"gottman",
    ],
    "repair_attempt": [
        r"onarım girişimi", r"repair attempt",
        r"tartışmayı.*düzelt",
    ],

    # ---- Yas ----
    "continuing_bonds": [
        r"continuing bonds", r"bağı sürdür", r"bağı sürdürm",
        r"anmak.*konuşmak", r"anmak.*yazmak",
    ],

    # ---- Uyku / CBT-I ----
    "stimulus_control": [
        r"uyaran kontrolü", r"stimulus control",
        r"20 dakika kural",
        r"yataktan kalk", r"yatak.*sadece uyku",
    ],
    "sleep_restriction": [
        r"uyku kısıtlaması", r"sleep restriction",
        r"uyku verimliliği", r"yatakta daha az",
    ],
    "sleep_hygiene": [
        r"uyku hijyeni",
        r"sabit uyanma", r"yatağa.*uykulu",
        r"yatak odası karanlık",
    ],

    # ---- ACT ----
    "values_clarification": [
        r"değer haritası", r"değer harita",
        r"ne için çalışıyorum",
        r"değerlerin.*ne",
    ],

    # ---- İş / kariyer ----
    "job_crafting": [
        r"job crafting", r"işi yeniden şekillendir",
    ],
    "boundary_setting": [
        r"sınır koy", r"sınır cümlesi",
        r"4 tip.*sınır", r"'?hayır'? formul",
    ],
    "microbreak": [
        r"mikro[- ]mola", r"90.*dakika.*10",
        r"ultradyen", r"pomodoro",
    ],
}

def extract_techniques(content_tr: str) -> list[str]:
    txt = content_tr.lower()
    return [t for t, pats in TECHNIQUE_PATTERNS.items()
            if any(re.search(p, txt, re.IGNORECASE) for p in pats)]

# Loaders — her fonksiyon tek bir sorumluluk
def load_sources(session, sources):
    """Source registry CSV → Source node.

    CSV columns: source_id, title, url, source_type, license, bucket,
                 commercial_use_allowed, notes, review_status
    """
    for s in sources:
        session.run("""
            MERGE (src:Source {id: $id})
              ON CREATE SET src.title = $title,
                            src.url = $url,
                            src.source_type = $source_type,
                            src.license = $license,
                            src.review_status = $review_status
        """, id=s["source_id"],
             title=s["title"],
             url=s.get("url", ""),
             source_type=s.get("source_type", "unknown"),
             license=s.get("license", "unknown"),
             review_status=s.get("review_status", "needs_review"))


def load_cards(session, cards):
    """CBT kartları → Card + Module + PART_OF."""
    for c in cards:
        session.run("""
            MERGE (card:Card {id: $id})
              ON CREATE SET card.type = $type,
                            card.title_tr = $title_tr,
                            card.topic = $topic,
                            card.review_status = $review_status
            MERGE (m:Module {id: $topic})
              ON CREATE SET m.display_name_tr = $topic
            MERGE (card)-[:PART_OF]->(m)
        """, id=c["id"], type=c["type"], title_tr=c["title_tr"],
             topic=c["topic"], review_status=c.get("review_status", "needs_review"))

def load_concepts_and_groups(session, ontology):
    """Concept + ConceptGroup + REQUIRES_ALL / REQUIRES_ANY.

    AND/OR semantiği graf-native korunur:
      - requires_all: [["a"], ["b", "c"]] = "a VE (b veya c)"
      - Aynı group_index içindeki edge'ler OR alternatifi (biri yeter)
      - Farklı group_index → AND (hepsi gerek)
    """
    # Groups
    for gid, gdef in ontology["concept_groups"].items():
        session.run("""
            MERGE (g:ConceptGroup {id: $gid})
              ON CREATE SET g.feature_only = $feature_only
        """, gid=gid, feature_only=gdef.get("feature_only", False))

    # Concepts
    for cid, cdef in ontology["concepts"].items():
        # Concept node — sadece description + risk_level
        # requires_all/any ve target_card_ids grafta edge olarak var, property olarak DUPLICATE etme
        session.run("""
            MERGE (c:Concept {id: $cid})
              ON CREATE SET c.description = $description,
                            c.risk_level = $risk_level
        """, cid=cid,
             description=cdef.get("description", ""),
             risk_level=cdef.get("risk_level", "medium"))

        # REQUIRES_ALL edges — outer list = AND grupları
        # Inner list = OR alternatifleri (aynı group_index)
        for idx, req_list in enumerate(cdef.get("requires_all", [])):
            for group_id in req_list:
                session.run("""
                    MATCH (c:Concept {id: $cid})
                    MATCH (g:ConceptGroup {id: $gid})
                    MERGE (c)-[r:REQUIRES_ALL {group_index: $idx}]->(g)
                """, cid=cid, gid=group_id, idx=idx)

        # REQUIRES_ANY edges — herhangi biri fire ederse concept fire eder
        for idx, req_list in enumerate(cdef.get("requires_any", [])):
            for group_id in req_list:
                session.run("""
                    MATCH (c:Concept {id: $cid})
                    MATCH (g:ConceptGroup {id: $gid})
                    MERGE (c)-[r:REQUIRES_ANY {group_index: $idx}]->(g)
                """, cid=cid, gid=group_id, idx=idx)

def link_cards_to_sources(session, cards):
    """Card -[:USES_SOURCE]-> Source.

    CBT kartlarında alan 'source_refs' (safety_cards.jsonl'de 'source_ids').
    """
    for c in cards:
        for source_id in c.get("source_refs", []):
            session.run("""
                MATCH (card:Card {id: $card_id})
                MATCH (s:Source {id: $source_id})
                MERGE (card)-[:USES_SOURCE]->(s)
            """, card_id=c["id"], source_id=source_id)
def load_safety_cards(session, safety_cards):
    """SafetyCard → Card multi-label + Source ilişkileri."""
    for sc in safety_cards:
        session.run("""
            MERGE (c:Card {id: $id})
              ON CREATE SET c.type = "safety",
                            c.title_tr = $title,
                            c.risk_level = $risk_level,
                            c.route = $route,
                            c.allow_cbt = $allow_cbt,
                            c.module = $module
            SET c:SafetyCard
        """, id=sc["card_id"], title=sc["title"], risk_level=sc["risk_level"],
             route=sc["route"], allow_cbt=sc["allow_cbt"], module=sc["module"])
        for source_id in sc.get("source_ids", []):
            session.run("""
                MATCH (c:Card {id: $card_id})
                MATCH (s:Source {id: $source_id})
                MERGE (c)-[:USES_SOURCE]->(s)
            """, card_id=sc["card_id"], source_id=source_id)

def link_concepts_to_safety_cards(session, ontology):
    """Concept -[:TARGETS]-> Card (ontology target_card_ids üzerinden).

    SafetyCard yerine Card kullanıyoruz — defensive: bazı concept'ler CBT kartı
    da hedefleyebilir (multi-label sayesinde SafetyCard olanlar da match olur).
    """
    for cid, cdef in ontology["concepts"].items():
        for target_card_id in cdef.get("target_card_ids", []):
            session.run("""
                MATCH (c:Concept {id: $cid})
                MATCH (target:Card {id: $target_card_id})
                MERGE (c)-[:TARGETS]->(target)
            """, cid=cid, target_card_id=target_card_id)


def create_techniques(session, cards):
    """Regex ile teknik çıkar → Technique node + TEACHES_TECHNIQUE.

    Card için MATCH (zaten var olmalı), Technique için MERGE (yoksa yarat).
    """
    for c in cards:
        for tech_id in extract_techniques(c["content_tr"]):
            session.run("""
                MERGE (t:Technique {id: $tech_id})
                WITH t
                MATCH (card:Card {id: $card_id})
                MERGE (card)-[:TEACHES_TECHNIQUE]->(t)
            """, tech_id=tech_id, card_id=c["id"])

def create_module_neighbors(session):
    """Module -[:NEIGHBOR_OF]- Module (yönsüz)."""
    for a, b in MODULE_NEIGHBORS:
        session.run("""
            MATCH (ma:Module {id: $a})
            MATCH (mb:Module {id: $b})
            MERGE (ma)-[:NEIGHBOR_OF]-(mb)
        """, a=a, b=b)


# Verification
def print_counts(session):
    print("\nNode counts:")
    for r in session.run("""
        MATCH (n) RETURN labels(n)[0] AS label, count(*) AS n ORDER BY n DESC
    """).data():
        print(f"  {r['label']:20s} {r['n']}")

    print("\nRelationship counts:")
    for r in session.run("""
        MATCH ()-[r]->() RETURN type(r) AS rel, count(*) AS n ORDER BY n DESC
    """).data():
        print(f"  {r['rel']:25s} {r['n']}")

# Main
def main():
    cards = [json.loads(l) for l in open(config.CARDS_PATH, encoding="utf-8")]
    safety_cards = [json.loads(l) for l in open(config.SAFETY_CARDS_PATH, encoding="utf-8")]
    ontology = json.load(open(config.ONTOLOGY_PATH, encoding="utf-8"))
    sources = list(csv.DictReader(open(config.REGISTRY_PATH, encoding="utf-8")))

    print(f"Loaded: {len(cards)} cards, {len(safety_cards)} safety, "
          f"{len(ontology['concepts'])} concepts, {len(sources)} sources")

    driver = get_driver()
    try:
        with driver.session() as session:
            create_schema(session)
            load_sources(session, sources)
            load_cards(session, cards)
            load_concepts_and_groups(session, ontology)
            link_cards_to_sources(session, cards)
            load_safety_cards(session, safety_cards)
            link_concepts_to_safety_cards(session, ontology)
            create_techniques(session, cards)
            create_module_neighbors(session)
            print_counts(session)
    finally:
        close_driver()
    print("\n✓ Migration done.")

if __name__ == "__main__":
    main()