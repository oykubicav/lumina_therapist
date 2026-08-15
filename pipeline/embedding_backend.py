"""Embedding backend — dual-mode (sentence-transformers preferred, TF-IDF fallback).

Both backends produce L2-normalised vectors so the same cosine-similarity
code works downstream. Default policy:
  - If sentence-transformers + torch are importable, use it (best semantic
    quality, multilingual MiniLM).
  - Else, fall back to a character-n-gram TF-IDF vectorizer (Turkish-
    morphology-friendly). Fully local, KVKK-safe, no network.

The pipeline never sends user text to any external service from this
module.
"""

from __future__ import annotations

import hashlib
from functools import lru_cache
from pathlib import Path
from typing import List, Tuple

from . import config



# Detect available backend
def _has_sentence_transformers() -> bool:
    try:
        import sentence_transformers  # noqa: F401
        import torch  # noqa: F401
        return True
    except ImportError:
        return False


# Sentence-transformers backend
class _STBackend:
    def __init__(self, model_name: str):
        from sentence_transformers import SentenceTransformer
        self.name = "sentence-transformers"
        self.model_name = model_name
        self._model = SentenceTransformer(model_name)
        self._fitted = True

    def fit(self, corpus: List[str]):
        # No fit needed
        pass

    def encode(self, texts: List[str]):
        import numpy as np
        return np.asarray(self._model.encode(texts, normalize_embeddings=True, show_progress_bar=False))


# TF-IDF fallback backend (char n-grams + word)
class _TfidfBackend:
    def __init__(self, char_range=(3, 5), word_max=20000):
        from sklearn.feature_extraction.text import TfidfVectorizer
        self.name = "tfidf-char-ngram"
        self.model_name = f"tfidf_char{char_range[0]}-{char_range[1]}+word"
        self._char_vec = TfidfVectorizer(
            analyzer="char_wb", ngram_range=char_range, min_df=1, max_df=1.0, sublinear_tf=True
        )
        self._word_vec = TfidfVectorizer(
            analyzer="word", ngram_range=(1, 2), min_df=1, max_df=1.0, max_features=word_max,
            sublinear_tf=True,
        )
        self._fitted = False

    def fit(self, corpus: List[str]):
        # Fit both vectorizers on the corpus so unseen tokens still map
        self._char_vec.fit(corpus)
        self._word_vec.fit(corpus)
        self._fitted = True

    def encode(self, texts: List[str]):
        import numpy as np
        from scipy.sparse import hstack
        from sklearn.preprocessing import normalize as l2norm
        if not self._fitted:
            raise RuntimeError("TF-IDF backend not fitted. Call fit(corpus) first.")
        ch = self._char_vec.transform(texts)
        wd = self._word_vec.transform(texts)
        m = hstack([ch, wd])
        m = l2norm(m, norm="l2", axis=1)
        return m  # sparse matrix; downstream code uses .dot for cosine



# Factory
def get_backend(prefer_st: bool = None):
    """Return a NEW backend instance each call.

    sentence-transformers backend is stateless after construction, so
    caching is fine in principle — but the TF-IDF backend stores fitted
    vocab and a single shared instance would let one consumer overwrite
    another's fit. Returning a fresh instance keeps consumers isolated.
    """
    # Default: honor config flag; can be overridden per-call if needed.
    if prefer_st is None:
        prefer_st = config.PREFER_SENTENCE_TRANSFORMERS
    if prefer_st and _has_sentence_transformers():
        return _STBackend(config.EMBED_MODEL)
    return _TfidfBackend()


def cosine_similarity(a, b):
    """Cosine similarity for dense numpy or sparse scipy.

    `a` is (n, d), `b` is (m, d) (or single vector).
    Returns (n, m) similarity matrix.
    """
    import numpy as np
    if hasattr(a, "toarray"):  # sparse
        return (a @ b.T).toarray()
    return a @ b.T


def to_dense(x):
    if hasattr(x, "toarray"):
        return x.toarray()
    return x


def hash_corpus(texts: List[str]) -> str:
    h = hashlib.sha1()
    for t in texts:
        h.update(t.encode("utf-8"))
        h.update(b"\x00")
    return h.hexdigest()[:12]
