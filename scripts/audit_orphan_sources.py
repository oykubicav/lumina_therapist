
"""Audit — every source in the registry must be cited in at least one card.

Exit code:
  0 — all sources cited (healthy)
  1 — orphan sources found

Called before each release / batch merge. Prevents "ghost source" drift.
"""

import csv
import json
import sys
from pathlib import Path

BASE = Path("/sessions/hopeful-cool-bell/mnt/cbt_knowledge_base")

# Collect all refs from CBT + safety cards
all_refs = set()
with open(BASE / "cards" / "cbt_cards.jsonl", encoding="utf-8") as f:
    for l in f:
        c = json.loads(l)
        all_refs.update(c.get("source_refs", []))
with open(BASE / "cards" / "safety_cards.jsonl", encoding="utf-8") as f:
    for l in f:
        c = json.loads(l)
        all_refs.update(c.get("source_ids", []))
        all_refs.update(c.get("source_refs", []))

# Registry
with open(BASE / "registry" / "source_registry.csv", encoding="utf-8") as f:
    reg_ids = [r["source_id"] for r in csv.DictReader(f)]

orphans = [s for s in reg_ids if s not in all_refs]
missing = [s for s in all_refs if s not in reg_ids]

print(f"Registry: {len(reg_ids)}")
print(f"Cited:    {len(reg_ids) - len(orphans)}")
print(f"Orphan:   {len(orphans)}")
print(f"Referenced-but-missing-from-registry: {len(missing)}")

if orphans:
    print("\nORPHANS (in registry, cited in 0 cards):")
    for o in orphans:
        print(f"  ✗ {o}")

if missing:
    print("\nMISSING (cited in cards, not in registry):")
    for m in missing:
        print(f"  ✗ {m}")

if orphans or missing:
    sys.exit(1)
print("\n✓ Clean — every source has a home, every citation resolves.")
sys.exit(0)
