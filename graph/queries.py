"""Read-only Cypher query'ler.

Retriever bu fonksiyonları çağıracak
Her fonksiyon bir session alır, deterministik döner.
"""
from typing import Any
from .driver import get_driver


# Query 1: Belirli concept'i hedefleyen tüm kartlar
def cards_targeting_concept(concept_id: str) -> list[dict]:
    """Bir concept'e route eden tüm kartları döndür.

    Örnek: cards_targeting_concept("active_suicidal_ideation")
    → [{"id": "safety_self_harm_suicide_001", "title_tr": "...", "risk_level": "critical"}]
    """
    driver = get_driver()
    with driver.session() as session:
        result = session.run("""
            MATCH (co:Concept {id: $cid})-[:TARGETS]->(c:Card)
            RETURN c.id AS id, c.title_tr AS title_tr, c.type AS type
        """, cid=concept_id)
        return [dict(r) for r in result]



# Query 2: Aynı tekniği paylaşan kartlar (cross-modül)
def cards_sharing_technique(card_id: str) -> list[dict]:
    """Bu kartın öğrettiği teknikleri paylaşan diğer kartları döndür.

    Örnek: cards_sharing_technique("pa_thoughtrec_009")
    → [{"id": "ha_thoughtrec_008", "topic": "health_anxiety", "technique": "thought_record"},
       {"id": "dep_thoughtrec_007", "topic": "depression", "technique": "thought_record"}]

    Vector'ın kaçırdığı: iki kart aynı tekniği öğretiyor ama farklı MODÜLDE.
    """
    driver = get_driver()
    with driver.session() as session:
        result = session.run("""
            MATCH (c:Card {id: $card_id})-[:TEACHES_TECHNIQUE]->(t:Technique)<-[:TEACHES_TECHNIQUE]-(other:Card)
            WHERE other.id <> c.id
            RETURN other.id AS id, other.title_tr AS title_tr, other.topic AS topic, t.id AS technique""", card_id=card_id)
        return [dict(r) for r in result]



# Query 3: Modül komşuluk — bir modüldeki kart için ilgili komşu modülden kartlar
def neighbor_module_cards(card_id: str, limit: int = 5) -> list[dict]:
    """Bu kartın modülüne komşu modüllerden kartlar.

    Örnek: card panic modülünde, komşu = health_anxiety
    → health_anxiety modülünün ilk `limit` kartını dön

    Kullanım: bir kullanıcı panic konusunda konuşurken health_anxiety'ye
    doğal geçiş yapıyor — GraphRAG bu geçişi önceden bilir.
    """
    driver = get_driver()
    with driver.session() as session:
      

        result = session.run("""
            MATCH (c:Card {id: $card_id})-[:PART_OF]->(m:Module)-[:NEIGHBOR_OF]-(neighbor:Module)<-[:PART_OF]-(other:Card)
            WHERE other.id <> c.id
            RETURN other.id AS id, other.title_tr AS title_tr , neighbor.id AS neighbor_module
            LIMIT $limit""", card_id=card_id, limit=limit)
        return [dict(r) for r in result]


# Query 4: Bir kartın tüm bağlamı (retriever için "kart paketi")
def card_context(card_id: str) -> dict:
    """Bir kartın tüm graf-bağlamını tek dict'te.

    Döndürür:
      - card: kart metadata
      - module: hangi modülde
      - sources: kullandığı kaynaklar
      - techniques: öğrettiği teknikler
      - concepts: hedeflediği concept'ler (safety için)
      - neighbor_cards: komşu modülden ilk 3 kart

    Retriever bunu composer'a "zengin bağlam" olarak verecek.
    """
    driver = get_driver()
    with driver.session() as session:
        result = session.run("""
            MATCH (c:Card {id: $card_id})
            OPTIONAL MATCH (c)-[:PART_OF]->(m:Module)
            OPTIONAL MATCH (c)-[:USES_SOURCE]->(s:Source)
            WITH c, m, collect(DISTINCT {id: s.id, title: s.title}) AS sources
            OPTIONAL MATCH (c)-[:TEACHES_TECHNIQUE]->(t:Technique)
            WITH c, m, sources, collect(DISTINCT t.id) AS techniques
            OPTIONAL MATCH (co:Concept)-[:TARGETS]->(c)
            WITH c, m, sources, techniques, collect(DISTINCT co.id) AS concepts
            OPTIONAL MATCH (m)-[:NEIGHBOR_OF]-(neighbor:Module)<-[:PART_OF]-(other:Card)
            WHERE other.id <> c.id
            WITH c, m, sources, techniques, concepts, collect(DISTINCT other.id)[..5] AS neighbor_cards
            RETURN c.id AS id,
                   c.title_tr AS title_tr,
                   c.type AS type,
                   m.id AS module,
                   sources, techniques, concepts, neighbor_cards
        """, card_id=card_id)
        record = result.single()
        return dict(record) if record else {}


if __name__ == "__main__":
    # Basit smoke test
    print("Query 1 —", cards_targeting_concept("active_suicidal_ideation"))
    print("Query 2 —", cards_sharing_technique("pa_thoughtrec_009"))
    print("Query 3 —", neighbor_module_cards("pa_psychoed_001"))
    print("Query 4 —", card_context("pa_psychoed_001"))