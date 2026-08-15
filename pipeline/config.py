"""Pipeline configuration.

All paths and runtime flags live here. Secrets (API keys) come from env vars,
NOT from this file.
"""

import os
from pathlib import Path

# --- paths ---
ROOT = Path(__file__).resolve().parent.parent  # cbt_knowledge_base/
CARDS_PATH = ROOT / "cards" / "cbt_cards.jsonl"
SAFETY_CARDS_PATH = ROOT / "cards" / "safety_cards.jsonl"
POLICY_PATH = ROOT / "policies" / "response_policy.md"
TEST_SET_PATH = ROOT / "evals" / "retrieval_test_set.jsonl"
REGISTRY_PATH = ROOT / "registry" / "source_registry.csv"

# --- LLM provider ---
# Switchable at runtime. KVKK note: for production deployment to TR users,
# this should default to a private/local model, with cloud APIs gated.
LLM_PROVIDER = os.environ.get("CBT_LLM_PROVIDER", "anthropic")  # anthropic | openai | local | mock
LLM_MODEL_COMPOSER = os.environ.get("CBT_MODEL_COMPOSER", "claude-sonnet-4-6")
LLM_MODEL_INTENT = os.environ.get("CBT_MODEL_INTENT", "claude-haiku-4-5-20251001")
LLM_MODEL_CRITIC = os.environ.get("CBT_MODEL_CRITIC", "claude-haiku-4-5-20251001")

# --- safety classifier ---
SAFETY_KEYWORD_MATCH_MIN_RATIO = 0.6  # token overlap threshold for fuzzy match
SAFETY_LLM_FALLBACK = False           # off by default for offline / KVKK-safe runs

# Embedding backend preference for Layer 3.
# Empirically TF-IDF outperforms sentence-transformers on the current
# test set (90% vs 78% overall_pass) because ST's semantic breadth
# over-triggers CBT-appropriate messages onto safety routes. Anchor
# cümleleri şu an TF-IDF karakter n-gram örüntüsüne uygun; ST için
# ayrı ve daha ayırt edici anchor seti gerekir. LLM composer/critic
# tarafı gelince Layer 3 üzerindeki basınç zaten düşecek — o zaman
# ST tekrar değerlendirilebilir.
PREFER_SENTENCE_TRANSFORMERS = os.environ.get("CBT_PREFER_ST", "0") == "1"

# --- retriever ---
EMBED_MODEL = os.environ.get(
    "CBT_EMBED_MODEL",
    "sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2"
)
RETRIEVAL_TOP_K = 5
EMBED_CACHE_PATH = ROOT / "pipeline" / "_embed_cache.npz"  # gitignore this

# --- privacy / KVKK ---
ENABLE_PII_REDACTION = True
ENABLE_LLM_PROMPT_LOGGING = False  # never log raw user input by default
ENABLE_TEST_PROMPT_LOGGING = os.environ.get("CBT_TEST_LOG_PROMPTS", "0") == "1"

# --- eval ---
EVAL_RESULTS_DIR = ROOT / "evals" / "results"
EVAL_RESULTS_DIR.mkdir(parents=True, exist_ok=True)
