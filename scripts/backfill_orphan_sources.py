
"""Backfill the 35 orphan sources (from batch 1+2) into cards.

Every source should have a natural home in ≥1 card. If a source has no
natural home, it should be removed from the registry (not left orphan).

For each orphan, mapping was chosen based on:
  - Semantic fit (source is truly about the topic of the card)
  - Was the source actually used at card writing time (even if not cited)
  - Non-tangential — avoid "sprinkle everywhere" citations
"""

import csv
import json
from pathlib import Path

CARDS = Path(__file__).resolve().parent.parent / "cards" / "cbt_cards.jsonl"
REG = Path(__file__).resolve().parent.parent / "registry" / "source_registry.csv"

# Mapping: orphan source → cards where it naturally belongs

MAPPING = {
    # --- Seminal papers (should have been in psychoed / cycle / thoughtrec) ---
    "clark_1986_panic_001": [
        "pa_psychoed_001",           # Clark cognitive model of panic — foundational
        "pa_cycle_002",              # catastrophic misinterpretation of body sensations
        "pa_hyperv_005",             # hyperventilation-catastrophizing cycle
    ],
    "wells_1995_gad_001": [
        "ga_psychoed_001",           # Wells metacognitive model of GAD
        "ga_cycle_002",              # worry-about-worry Type 2
        "ga_worrytime_007",          # worry postponement, metacognitive
    ],
    "fennell_1997_lse_001": [
        "lse_psychoed_001",          # Fennell LSE cognitive model
        "lse_cycle_002",             # negative core beliefs cycle
        "lse_innercritic_005",       # inner critic
    ],
    "harvey_2002_insomnia_cog_model_001": [
        "insom_psychoed_001",        # Harvey cognitive model of insomnia
        "insom_cycle_002",           # worry about sleep cycle
        "insom_thoughtrec_007",      # cognitive component of CBT-I
    ],

    # --- CCI Perth workbooks (raw extract confirmed content in cards) ---
    "cci_health_anxiety_001": [
        "ha_reassurance_004",        # CCI Module 6 — reducing reassurance seeking
        "ha_bodychecking_005",       # CCI Module 4 — attention training / body checking
        "ha_thoughtrec_008",         # CCI Module 5 — re-evaluating unhelpful thinking
        "ha_avoidance_009",          # CCI Module 7 — safety behaviours & avoidance
    ],
    "cci_panic_001": [
        "pa_cycle_002",              # panic cycle
        "pa_hyperv_005",             # interoceptive exposure basis
        "pa_safetybeh_007",          # safety behaviours
    ],
    "cci_self_compassion_001": [
        "dep_selfcompassion_008",    # self-compassion structure
        "lse_innercritic_005",       # inner critic vs compassionate voice
    ],
    "cci_depression_001": [
        "dep_psychoed_001",          # 8-module CBT depression structure
        "dep_actsched_004",          # behavioural activation
        "dep_thoughtrec_007",        # cognitive restructuring
    ],
    "cci_sleep_001": [
        "insom_hygiene_004",         # sleep hygiene from CCI
        "insom_stimuluscontrol_005", # stimulus control CBT-I
    ],

    # --- NICE guidelines (clinical anchor + safety_net referral) ---
    "nice_cg113_001": [               # GAD/anxiety
        "ga_psychoed_001",
        "ga_safetynet_010",
    ],
    "nice_cg90_001": [                # Depression
        "dep_psychoed_001",
        "dep_safetynet_010",
    ],
    "nice_cg159_001": [               # Sleep
        "insom_psychoed_001",
        "insom_safetynet_010",
    ],
    "nice_cg31_ocd_001": [            # OCD — scope-boundary reference
        "ga_safetynet_010",          # if user shows OCD signs → scope boundary
    ],
    "nice_ng116_ptsd_001": [          # PTSD
        "trauma_types_003",          # NICE PTSD types
        "trauma_safetynet_010",      # treatment pathway reference
    ],

    # --- Cochrane meta-analyses ---
    "cochrane_cbt_depression_001": [
        "dep_psychoed_001",          # CBT evidence base for depression
    ],
    "cochrane_cbt_gad_001": [
        "ga_psychoed_001",           # CBT evidence base for GAD
    ],
    "cochrane_cbt_panic_001": [
        "pa_psychoed_001",           # CBT for panic evidence
    ],
    "cochrane_cbt_health_anxiety_001": [
        "ha_psychoed_001",           # CBT for HA evidence
    ],

    # --- RCPsych patient guidance ---
    "rcpsych_anxiety_001": [
        "ga_psychoed_001",           # patient-facing anxiety anchor
    ],
    "rcpsych_depression_001": [
        "dep_psychoed_001",          # patient-facing depression anchor
    ],
    "rcpsych_cbt_intro_001": [
        "ha_psychoed_001",           # 'what is CBT' explainer
        "dep_psychoed_001",
    ],

    # --- APA guidelines ---
    "apa_depression_guideline_2019_001": [
        "dep_psychoed_001",          # APA guideline
        "dep_safetynet_010",
    ],
    "apa_ptsd_guideline_001": [
        "trauma_psychoed_001",       # APA PTSD guideline
        "trauma_safetynet_010",
    ],
    "apa_workplace_mental_health_001": [
        "work_stressvsburnout_001",  # workplace mental health anchor
        "work_safetynet_010",
    ],

    # --- TR clinical/gov (referral safety_net) ---
    "tpd_ruh_sagligi_001": [
        "dep_safetynet_010",         # Turkish Psychological Association referral
        "ga_safetynet_010",
        "trauma_safetynet_010",
    ],
    "saglik_bakanligi_ruh_sagligi_001": [
        "dep_safetynet_010",         # TR gov mental health services
        "ga_safetynet_010",
        "trauma_safetynet_010",
    ],
    "istanbul_tabip_odasi_ruh_sagligi_001": [
        "pa_safetynet_010",          # İstanbul yerel referral
        "ha_safetynet_010",
    ],
    "aile_bakanligi_evlilik_001": [
        "rel_family_009",            # marriage preparation program TR
        "trans_types_004",           # marriage as life transition
    ],
    "who_bereavement_covid_001": [
        "grief_psychoed_001",        # bereavement care policy
        "grief_safetynet_010",
    ],
    "nhs_moving_house_wellbeing_001": [
        "trans_types_004",           # moving-house stress
        "trans_tr_gurbet_008",
    ],
    "prinstein_2017_developmental_transitions_001": [
        "trans_types_004",           # adolescent developmental transitions
    ],
    "who_mental_health_workplace_2024_001": [
        "work_stressvsburnout_001",  # WHO 2024 workplace policy
        "work_safetynet_010",
    ],
    "cci_perth_grief_reference_001": [
        "grief_avoidance_007",       # coping-with-loss adjacency
        "grief_psychoed_001",
    ],
    "samhsa_trauma_informed_care_001": [
        "trauma_psychoed_001",       # trauma-informed 6 principles
    ],

    # --- No natural home — REMOVE ---
    # salkovskis_1985_ocd_001 — OCD boundary; we don't have OCD module.
    # We could cite in a general boundary card but it would be forced.
    # REMOVE from registry.
}

REMOVE_FROM_REGISTRY = [
    "salkovskis_1985_ocd_001",  # No OCD module; forced citation would be dishonest
]

# Apply
with open(CARDS, encoding="utf-8") as f:
    cards = [json.loads(l) for l in f]
card_by_id = {c["id"]: c for c in cards}

added = 0
missing = []
for source_id, card_ids in MAPPING.items():
    for card_id in card_ids:
        if card_id not in card_by_id:
            missing.append((source_id, card_id))
            continue
        c = card_by_id[card_id]
        refs = c.get("source_refs", [])
        if source_id not in refs:
            refs.append(source_id)
            c["source_refs"] = refs
            added += 1

if missing:
    print("WARNING — missing cards:")
    for s, cid in missing:
        print(f"  {s} → {cid}")
    print()

with open(CARDS, "w", encoding="utf-8") as f:
    for c in cards:
        f.write(json.dumps(c, ensure_ascii=False) + "\n")

# Remove from registry
if REMOVE_FROM_REGISTRY:
    with open(REG, encoding="utf-8") as f:
        rows = list(csv.DictReader(f))
    fields = list(rows[0].keys())
    kept = [r for r in rows if r["source_id"] not in REMOVE_FROM_REGISTRY]
    with open(REG, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=fields, quoting=csv.QUOTE_MINIMAL)
        w.writeheader()
        for r in kept:
            w.writerow(r)
    print(f"Removed {len(REMOVE_FROM_REGISTRY)} orphan sources from registry:")
    for s in REMOVE_FROM_REGISTRY:
        print(f"  - {s}")
    print()

# Re-audit
all_refs = set()
for c in cards:
    all_refs.update(c.get("source_refs", []))
with open("cards/safety_cards.jsonl", encoding="utf-8") as f:
    for l in f:
        sc = json.loads(l)
        all_refs.update(sc.get("source_ids", []))
        all_refs.update(sc.get("source_refs", []))

with open(REG, encoding="utf-8") as f:
    reg_ids = [r["source_id"] for r in csv.DictReader(f)]
orphans_after = [s for s in reg_ids if s not in all_refs]

print(f"Added {added} source_refs entries across {len(MAPPING)} sources")
print()
print(f"Post-backfill audit:")
print(f"  Registry size:      {len(reg_ids)}")
print(f"  Cited:              {len(reg_ids) - len(orphans_after)}")
print(f"  Orphan:             {len(orphans_after)}")
if orphans_after:
    print(f"\nStill orphan (should be 0):")
    for o in orphans_after:
        print(f"  ✗ {o}")
