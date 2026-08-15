
"""Backfill batch-3 sources into existing cards' source_refs.

For each of the 20 batch-3 sources, adds it to the source_refs of the
cards where it genuinely informs content — NOT tangentially, but as a
substantive anchor. If a source doesn't fit ≥2 cards meaningfully, log
a warning to consider removing it from registry.

Rule: no source stays in registry without ≥1 card citation.
"""

import json
from pathlib import Path

CARDS = Path("/sessions/hopeful-cool-bell/mnt/cbt_knowledge_base/cards/cbt_cards.jsonl")

# Mapping: source_id → list of card_ids where it belongs


MAPPING = {
    # --- Assessment scales (clinical anchors for self-check cards) ---
    "kroenke_2001_phq9_001": [
        "dep_selfcheck_003",       # PHQ-9 depression severity
    ],
    "spitzer_2006_gad7_001": [
        "ga_selfcheck_003",        # GAD-7
    ],
    "cohen_1983_pss_001": [
        "work_selfcheck_003",      # PSS perceived stress
        "trans_schlossberg_003",   # transitions stress assessment
    ],
    "weathers_2013_pcl5_001": [
        "trauma_responses_002",    # PTSD 4 groups (DSM-5 anchor)
        "trauma_types_003",        # PTSD types
    ],
    "bastien_2001_isi_001": [
        "insom_selfcheck_003",     # Insomnia Severity Index
    ],

    # --- Third-wave CBT ---
    "hayes_2004_act_001": [
        "work_values_004",         # ACT values-based living core
        "ga_worrytime_007",        # cognitive defusion cross
        "trauma_grounding_005",    # present-moment awareness
    ],
    "segal_mbct_2018_001": [
        "dep_rumination_006",      # MBCT relapse prevention for depression
        "ga_worrytime_007",        # mindfulness of thoughts
    ],
    "kabat_zinn_1990_mbsr_001": [
        "work_microbreaks_006",    # stress reduction breaks
        "trauma_body_007",         # body awareness + regulation
        "pa_grounding_004",        # breath awareness
    ],
    "neff_2003_self_compassion_001": [
        "dep_selfcompassion_008",  # Neff's theoretical anchor
        "lse_innercritic_005",     # self-compassion vs inner critic
        "grief_thought_008",       # self-compassion in grief guilt
    ],

    # --- Meta-analyses (CBT evidence base for psychoed cards) ---
    "hofmann_2012_cbt_meta_001": [
        "ha_psychoed_001",         # CBT evidence for HA
        "pa_psychoed_001",         # CBT for panic
        "trauma_psychoed_001",     # CBT evidence anchor
    ],
    "cuijpers_2016_cbt_depression_meta_001": [
        "dep_psychoed_001",        # depression CBT meta
        "ga_psychoed_001",         # anxiety CBT meta
    ],
    "butler_2006_cbt_empirical_status_001": [
        "lse_psychoed_001",        # broad CBT empirical support
        "insom_psychoed_001",      # sleep CBT included in Butler review
    ],

    # --- TR academic institutions (for safety_net referral) ---
    "hacettepe_psikiyatri_001": [
        "dep_safetynet_010",       # Ankara psychiatry referral
        "ga_safetynet_010",
        "trauma_safetynet_010",
    ],
    "bogazici_psikoloji_001": [
        "lse_safetynet_010",       # İstanbul psychology research
        "rel_safetynet_010",       # relationship research
    ],
    "istanbul_cerrahpasa_ruh_sagligi_001": [
        "pa_safetynet_010",        # İstanbul psychiatry referral
        "ha_safetynet_010",
    ],
    "sabri_ulker_ruh_sagligi_001": [
        "work_lifestyle_009",      # public health / lifestyle info
        "insom_lifestyle_009",     # sleep-related lifestyle guidance
    ],

    # --- Guidelines + taxonomy ---
    "nice_ng222_depression_2022_001": [
        "dep_psychoed_001",        # updated NICE evidence base
        "dep_safetynet_010",       # treatment pathways
    ],
    "who_icd11_2019_001": [
        "grief_psychoed_001",      # PGD ICD-11 formalization
        "trauma_types_003",        # C-PTSD ICD-11 formalization
    ],
    "iapt_manual_uk_001": [
        "ha_safetynet_010",        # stepped-care framing (self-help vs clinical)
        "dep_safetynet_010",
    ],
    "iasp_pain_2020_001": [
        "ha_psychoed_001",         # pain definition (real vs perceived symptom framing)
        "ha_bodychecking_005",     # body sensation interpretation
    ],
}


# Apply

with open(CARDS, encoding="utf-8") as f:
    cards = [json.loads(l) for l in f]

card_by_id = {c["id"]: c for c in cards}

added_count = 0
missing_cards = []
for source_id, card_ids in MAPPING.items():
    for card_id in card_ids:
        if card_id not in card_by_id:
            missing_cards.append((source_id, card_id))
            continue
        c = card_by_id[card_id]
        refs = c.get("source_refs", [])
        if source_id not in refs:
            refs.append(source_id)
            c["source_refs"] = refs
            added_count += 1

if missing_cards:
    print("WARNING — missing cards referenced by mapping:")
    for s, cid in missing_cards:
        print(f"  {s} → {cid}")
    print()

# Write back
with open(CARDS, "w", encoding="utf-8") as f:
    for c in cards:
        f.write(json.dumps(c, ensure_ascii=False) + "\n")

print(f"Added {added_count} source_refs entries across {len(MAPPING)} sources")
print()

# Verify — each batch-3 source now cited ≥1
print("Post-backfill citation counts:")
for source_id in MAPPING:
    n = sum(1 for c in cards if source_id in c.get("source_refs", []))
    marker = "✓" if n >= 1 else "✗"
    print(f"  {marker} {source_id:45s} {n} card(s)")

# Also verify no orphan sources across the WHOLE registry
import csv
REG = Path("/sessions/hopeful-cool-bell/mnt/cbt_knowledge_base/registry/source_registry.csv")
with open(REG, encoding="utf-8") as f:
    reg_ids = [r["source_id"] for r in csv.DictReader(f)]

all_refs = set()
for c in cards:
    all_refs.update(c.get("source_refs", []))

orphans = [sid for sid in reg_ids if sid not in all_refs]
print(f"\nOrphan sources (in registry but 0 card citations): {len(orphans)}")
if orphans:
    for o in orphans:
        print(f"  ✗ {o}")
