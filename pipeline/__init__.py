"""CBT Support pipeline.

Stage 2 — offline pipeline components.

Order of execution for a user message:
    safety_classifier  ->  intent_classifier  ->  retriever  ->  composer  ->  output_critic

The orchestrator wires these together. The eval_runner runs the retrieval
test set through this pipeline and emits pass/fail metrics.

Design notes:
- All LLM calls go through llm_adapter, which can be swapped between
  Anthropic / OpenAI / local without touching component code.
- redact_pii() must run before any user text leaves the process boundary,
  for KVKK compliance.
- safety_classifier is rule-based first and offline-runnable. LLM fallback
  is opt-in.
- The retriever loads embeddings once and stays in-memory.
"""

__version__ = "0.1.0"
