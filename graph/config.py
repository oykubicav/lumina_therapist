"""Neo4j connection config + dosya yolları."""
import os
from pathlib import Path

BASE = Path(__file__).resolve().parent.parent

# Connection — env'den, default sadece local dev için
NEO4J_URI = os.environ.get("CBT_NEO4J_URI", "bolt://localhost:7688")  
NEO4J_USER = os.environ.get("CBT_NEO4J_USER", "neo4j")
NEO4J_PASSWORD = os.getenv("CBT_NEO4J_PASSWORD")
  

# Data dosyaları
CARDS_PATH = BASE / "cards" / "cbt_cards.jsonl"
SAFETY_CARDS_PATH = BASE / "cards" / "safety_cards.jsonl"
ONTOLOGY_PATH = BASE / "rules" / "safety_trigger_rules.json"
REGISTRY_PATH = BASE / "registry" / "source_registry.csv"