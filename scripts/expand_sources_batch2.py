
"""Append batch-2 sources to source_registry.csv.

Adds ~20 high-legitimacy sources across all modules:
  - Cochrane systematic reviews (peer-reviewed meta-analyses)
  - APA / NICE / RCPsych clinical guidelines
  - Centre for Clinical Interventions (CCI Perth) workbooks — CBT self-help
    published by a WA government health service
  - Turkish clinical resources (KBT Derneği, TR Sağlık Bakanlığı)
  - Seminal CBT model papers (Beck, Clark, Wells, Fennell, Salkovskis) as
    concept anchors — content used only as citation reference, not verbatim
"""

import csv
from pathlib import Path

REG = Path("/sessions/hopeful-cool-bell/mnt/cbt_knowledge_base/registry/source_registry.csv")

NEW = [
    # CCI Perth workbooks (Centre for Clinical Interventions)
    # WA state government mental-health service — CBT self-help.
    # Structure verified for Health Anxiety module (9 modules).
    {
        "source_id": "cci_health_anxiety_001",
        "title": "CCI Perth — Helping Health Anxiety Workbook",
        "url": "https://www.cci.health.wa.gov.au/Resources/Looking-After-Yourself/Health-Anxiety",
        "source_type": "self_help_workbook",
        "license": "wa_gov_health_public",
        "bucket": "B",
        "commercial_use_allowed": "false",
        "notes": "9-module CBT-based health anxiety workbook by clinical psychologists; structure verified: Understanding / Development / Maintenance / Attention training / Cognitive restructuring / Reducing checking + reassurance / Avoidance-safety behaviours / Rules & assumptions / Healthy living. Synthesize only.",
        "review_status": "needs_review",
    },
    {
        "source_id": "cci_panic_001",
        "title": "CCI Perth — Panic Stations! Coping with Panic Workbook",
        "url": "https://www.cci.health.wa.gov.au/Resources/Looking-After-Yourself/Panic",
        "source_type": "self_help_workbook",
        "license": "wa_gov_health_public",
        "bucket": "B",
        "commercial_use_allowed": "false",
        "notes": "CBT panic workbook — panic cycle, catastrophic misinterpretation, interoceptive exposure, breathing retraining. Confirms Clark 1986 cognitive model of panic.",
        "review_status": "needs_review",
    },
    {
        "source_id": "cci_worry_001",
        "title": "CCI Perth — What? Me Worry!? Worry & Rumination Workbook",
        "url": "https://www.cci.health.wa.gov.au/Resources/Looking-After-Yourself/Worry-and-Rumination",
        "source_type": "self_help_workbook",
        "license": "wa_gov_health_public",
        "bucket": "B",
        "commercial_use_allowed": "false",
        "notes": "Excellent GAD-focused workbook: worry beliefs (metacognitive), problem-solving vs hypothetical worry, worry postponement, intolerance of uncertainty. Directly maps to GAD module.",
        "review_status": "needs_review",
    },
    {
        "source_id": "cci_self_esteem_001",
        "title": "CCI Perth — Improving Self-Esteem Workbook",
        "url": "https://www.cci.health.wa.gov.au/Resources/Looking-After-Yourself/Self-Esteem",
        "source_type": "self_help_workbook",
        "license": "wa_gov_health_public",
        "bucket": "B",
        "commercial_use_allowed": "false",
        "notes": "Fennell-based LSE workbook: negative core beliefs, biased thinking, negative predictions, adjustment of rules and assumptions.",
        "review_status": "needs_review",
    },
    {
        "source_id": "cci_perfectionism_001",
        "title": "CCI Perth — Perfectionism in Perspective Workbook",
        "url": "https://www.cci.health.wa.gov.au/Resources/Looking-After-Yourself/Perfectionism",
        "source_type": "self_help_workbook",
        "license": "wa_gov_health_public",
        "bucket": "B",
        "commercial_use_allowed": "false",
        "notes": "Perfectionism cycle — self-worth contingent on achievement. LSE + GAD adjacency; cross-references self-critical thinking patterns.",
        "review_status": "needs_review",
    },
    {
        "source_id": "cci_procrastination_001",
        "title": "CCI Perth — Put Off Procrastinating Workbook",
        "url": "https://www.cci.health.wa.gov.au/Resources/Looking-After-Yourself/Procrastination",
        "source_type": "self_help_workbook",
        "license": "wa_gov_health_public",
        "bucket": "B",
        "commercial_use_allowed": "false",
        "notes": "Procrastination as avoidance behaviour; depression + LSE adjacency (behavioural activation angle).",
        "review_status": "needs_review",
    },
    {
        "source_id": "cci_self_compassion_001",
        "title": "CCI Perth — Building Self-Compassion Workbook",
        "url": "https://www.cci.health.wa.gov.au/Resources/Looking-After-Yourself/Self-Compassion",
        "source_type": "self_help_workbook",
        "license": "wa_gov_health_public",
        "bucket": "B",
        "commercial_use_allowed": "false",
        "notes": "Kristin Neff self-compassion framework applied via CBT lens. LSE + depression module utility.",
        "review_status": "needs_review",
    },
    {
        "source_id": "cci_depression_001",
        "title": "CCI Perth — Back from the Bluez: Coping with Depression",
        "url": "https://www.cci.health.wa.gov.au/Resources/Looking-After-Yourself/Depression",
        "source_type": "self_help_workbook",
        "license": "wa_gov_health_public",
        "bucket": "B",
        "commercial_use_allowed": "false",
        "notes": "8-module CBT depression workbook — behavioural activation, cognitive restructuring, core belief work, relapse prevention. Complements NHS depression + Oxford OH197.20.",
        "review_status": "needs_review",
    },
    {
        "source_id": "cci_sleep_001",
        "title": "CCI Perth — Sleep Information Sheets and Workbook",
        "url": "https://www.cci.health.wa.gov.au/Resources/Looking-After-Yourself/Sleep",
        "source_type": "self_help_workbook",
        "license": "wa_gov_health_public",
        "bucket": "B",
        "commercial_use_allowed": "false",
        "notes": "CBT-I materials: sleep hygiene, stimulus control, sleep restriction, cognitive component. Confirms insomnia module framing.",
        "review_status": "needs_review",
    },

    # Cochrane systematic reviews (peer-reviewed meta-analyses)
    # Reference-only — abstracts/conclusions cited, not full text
    {
        "source_id": "cochrane_cbt_gad_001",
        "title": "Cochrane — Psychological therapies for generalised anxiety disorder (Hunot et al., updated)",
        "url": "https://www.cochranelibrary.com/cdsr/doi/10.1002/14651858.CD001848.pub4/full",
        "source_type": "systematic_review",
        "license": "cochrane_reference",
        "bucket": "B",
        "commercial_use_allowed": "false",
        "notes": "Meta-analytic anchor for GAD module claiming CBT is first-line psychological treatment; effect sizes moderate-to-large. Citation reference only.",
        "review_status": "needs_review",
    },
    {
        "source_id": "cochrane_cbt_panic_001",
        "title": "Cochrane — Psychological therapies for panic disorder with or without agoraphobia",
        "url": "https://www.cochranelibrary.com/cdsr/doi/10.1002/14651858.CD011003.pub2/full",
        "source_type": "systematic_review",
        "license": "cochrane_reference",
        "bucket": "B",
        "commercial_use_allowed": "false",
        "notes": "Meta-analytic anchor for panic module: CBT (especially with exposure) is first-line. Citation reference only.",
        "review_status": "needs_review",
    },
    {
        "source_id": "cochrane_cbt_health_anxiety_001",
        "title": "Cochrane — Cognitive and behavioural therapies for hypochondriasis (health anxiety)",
        "url": "https://www.cochranelibrary.com/cdsr/doi/10.1002/14651858.CD011675.pub2/full",
        "source_type": "systematic_review",
        "license": "cochrane_reference",
        "bucket": "B",
        "commercial_use_allowed": "false",
        "notes": "Cooper et al. 2017 meta-analysis — CBT-based interventions reduce health anxiety symptoms. Reference anchor for health-anxiety module.",
        "review_status": "needs_review",
    },

    # Clinical guidelines (national bodies)
    {
        "source_id": "apa_depression_guideline_2019_001",
        "title": "APA Clinical Practice Guideline for the Treatment of Depression",
        "url": "https://www.apa.org/depression-guideline",
        "source_type": "clinical_guideline",
        "license": "apa_reference",
        "bucket": "B",
        "commercial_use_allowed": "false",
        "notes": "APA 2019 depression treatment guideline — CBT, IPT, behavioural activation all supported for adults. Bot-protected page; reference by known content.",
        "review_status": "needs_review",
    },
    {
        "source_id": "apa_ptsd_guideline_001",
        "title": "APA Clinical Practice Guideline for the Treatment of PTSD",
        "url": "https://www.apa.org/ptsd-guideline",
        "source_type": "clinical_guideline",
        "license": "apa_reference",
        "bucket": "B",
        "commercial_use_allowed": "false",
        "notes": "Scope-boundary reference: PTSD is out of scope for our chatbot; guideline used to justify explicit deferral to professional care in safety cards.",
        "review_status": "needs_review",
    },
    {
        "source_id": "nice_cg31_ocd_001",
        "title": "NICE Clinical Guideline CG31 — Obsessive-compulsive disorder and body dysmorphic disorder",
        "url": "https://www.nice.org.uk/guidance/cg31",
        "source_type": "clinical_guideline",
        "license": "nice_reference",
        "bucket": "B",
        "commercial_use_allowed": "false",
        "notes": "OCD is out of scope for chatbot self-help without ERP supervision; guideline cited for boundary safety card.",
        "review_status": "needs_review",
    },
    {
        "source_id": "nice_ng116_ptsd_001",
        "title": "NICE Guideline NG116 — Post-traumatic stress disorder",
        "url": "https://www.nice.org.uk/guidance/ng116",
        "source_type": "clinical_guideline",
        "license": "nice_reference",
        "bucket": "B",
        "commercial_use_allowed": "false",
        "notes": "PTSD scope boundary. Trauma-focused CBT / EMDR require trained clinician; chatbot cannot substitute.",
        "review_status": "needs_review",
    },
    {
        "source_id": "rcpsych_cbt_intro_001",
        "title": "Royal College of Psychiatrists — What is CBT?",
        "url": "https://www.rcpsych.ac.uk/mental-health/treatments-and-wellbeing/cognitive-behavioural-therapy-(cbt)",
        "source_type": "patient_guidance",
        "license": "unknown",
        "bucket": "B",
        "commercial_use_allowed": "false",
        "notes": "Consumer-facing 'what is CBT' explainer — used as anchor for our own psychoeducation card framing across all modules.",
        "review_status": "needs_review",
    },


    # Turkish clinical / regulatory / association resources

    {
        "source_id": "kbtdernegi_001",
        "title": "Türkiye Bilişsel ve Davranışçı Psikoterapiler Derneği (KBTDerneği)",
        "url": "https://www.kbtdernegi.org.tr/",
        "source_type": "professional_society",
        "license": "unknown",
        "bucket": "B",
        "commercial_use_allowed": "false",
        "notes": "TR bilişsel-davranışçı psikoterapi mesleki derneği; klinisyen bulma / eğitim listesi için TR-özel referans.",
        "review_status": "needs_review",
    },
    {
        "source_id": "saglik_bakanligi_ruh_sagligi_001",
        "title": "T.C. Sağlık Bakanlığı — Ruh Sağlığı Hizmetleri",
        "url": "https://halksagligi.saglik.gov.tr/",
        "source_type": "government_resource",
        "license": "public_domain_gov",
        "bucket": "B",
        "commercial_use_allowed": "false",
        "notes": "TR devlet ruh sağlığı hizmet yapısı — aile hekimliği, TSM ruh sağlığı birimleri, CSM, MHRS randevu 182. Kullanıcıya yönlendirme referansı.",
        "review_status": "needs_review",
    },
    {
        "source_id": "istanbul_tabip_odasi_ruh_sagligi_001",
        "title": "İstanbul Tabip Odası — Ruh Sağlığı Ağı Broşürleri",
        "url": "https://www.istabip.org.tr/",
        "source_type": "professional_society",
        "license": "unknown",
        "bucket": "B",
        "commercial_use_allowed": "false",
        "notes": "TR yerelinde hekim odası broşürleri — kaygı, depresyon, uyku, damgalama. Klinik yönlendirme dilinde TR aksanı için yararlı.",
        "review_status": "needs_review",
    },

    # Seminal CBT model papers (citation anchors — content not extracted verbatim)
    # These give theoretical legitimacy to card structures ("Clark model of panic",
    # "Wells metacognitive model", "Fennell LSE model", "Salkovskis OCD model")
    {
        "source_id": "clark_1986_panic_001",
        "title": "Clark DM. A cognitive approach to panic. Behaviour Research and Therapy, 24(4), 461-470",
        "url": "https://doi.org/10.1016/0005-7967(86)90011-2",
        "source_type": "seminal_paper",
        "license": "citation_reference",
        "bucket": "B",
        "commercial_use_allowed": "false",
        "notes": "David Clark's foundational cognitive model of panic disorder — catastrophic misinterpretation of bodily sensations. Model referenced in panic cards.",
        "review_status": "needs_review",
    },
    {
        "source_id": "wells_1995_gad_001",
        "title": "Wells A. Meta-cognition and worry: A cognitive model of generalized anxiety disorder. Behavioural and Cognitive Psychotherapy, 23(3), 301-320",
        "url": "https://doi.org/10.1017/S1352465800015897",
        "source_type": "seminal_paper",
        "license": "citation_reference",
        "bucket": "B",
        "commercial_use_allowed": "false",
        "notes": "Adrian Wells metacognitive model of GAD — Type 1 worry (about world) + Type 2 worry (about worry). Reference for GAD psychoeducation card.",
        "review_status": "needs_review",
    },
    {
        "source_id": "fennell_1997_lse_001",
        "title": "Fennell MJV. Low self-esteem: A cognitive perspective. Behavioural and Cognitive Psychotherapy, 25(1), 1-25",
        "url": "https://doi.org/10.1017/S1352465800018129",
        "source_type": "seminal_paper",
        "license": "citation_reference",
        "bucket": "B",
        "commercial_use_allowed": "false",
        "notes": "Melanie Fennell's cognitive model of low self-esteem — bottom rules, negative predictions, self-critical thinking. Foundation of Oxford OH198.20 self-esteem workbook and CCI self-esteem workbook.",
        "review_status": "needs_review",
    },
    {
        "source_id": "beck_1979_cbt_depression_001",
        "title": "Beck AT, Rush AJ, Shaw BF, Emery G. Cognitive Therapy of Depression. Guilford Press",
        "url": "https://www.guilford.com/books/Cognitive-Therapy-of-Depression/Beck-Rush-Shaw-Emery/9780898629194",
        "source_type": "seminal_book",
        "license": "citation_reference",
        "bucket": "B",
        "commercial_use_allowed": "false",
        "notes": "Aaron Beck's foundational CBT for depression manual (1979) — cognitive triad, thought record, behavioural activation. Historical anchor.",
        "review_status": "needs_review",
    },
    {
        "source_id": "salkovskis_1985_ocd_001",
        "title": "Salkovskis PM. Obsessional-compulsive problems: A cognitive-behavioural analysis. Behaviour Research and Therapy, 23(5), 571-583",
        "url": "https://doi.org/10.1016/0005-7967(85)90105-6",
        "source_type": "seminal_paper",
        "license": "citation_reference",
        "bucket": "B",
        "commercial_use_allowed": "false",
        "notes": "Salkovskis inflated-responsibility model — reference for OCD scope-boundary safety card (OCD out of chatbot scope).",
        "review_status": "needs_review",
    },
    {
        "source_id": "harvey_2002_insomnia_cog_model_001",
        "title": "Harvey AG. A cognitive model of insomnia. Behaviour Research and Therapy, 40(8), 869-893",
        "url": "https://doi.org/10.1016/S0005-7967(01)00061-4",
        "source_type": "seminal_paper",
        "license": "citation_reference",
        "bucket": "B",
        "commercial_use_allowed": "false",
        "notes": "Allison Harvey's cognitive model of insomnia — worry about sleep, selective attention, safety behaviours, misperception of sleep. Foundation of CBT-I cognitive component.",
        "review_status": "needs_review",
    },
]

# Append rows
with open(REG, "a", newline="", encoding="utf-8") as f:
    fieldnames = [
        "source_id","title","url","source_type","license","bucket",
        "commercial_use_allowed","notes","review_status",
    ]
    w = csv.DictWriter(f, fieldnames=fieldnames, quoting=csv.QUOTE_MINIMAL)
    for row in NEW:
        w.writerow(row)

# Verify
with open(REG, encoding="utf-8") as f:
    r = csv.DictReader(f)
    all_rows = list(r)
print(f"Registry rows now: {len(all_rows)}")
from collections import Counter
type_counts = Counter(row["source_type"] for row in all_rows)
print("By source_type:")
for t, n in sorted(type_counts.items(), key=lambda x: -x[1]):
    print(f"  {t:30s} {n}")
print()
print(f"New sources added this batch: {len(NEW)}")
for n in NEW:
    print(f"  {n['source_id']:40s} {n['source_type']}")
