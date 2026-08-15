
"""Batch 3 source expansion — 20 sources across 5 categories:

A. Clinical assessment scales (reference, NOT user-facing) — PHQ-9, GAD-7, PSS-10, PCL-5, ISI
B. Third-wave CBT (currently missing) — ACT, MBCT, MBSR, Self-Compassion
C. Meta-analyses — Hofmann 2012, Cuijpers 2016, Butler 2006
D. TR academic institutions — Boğaziçi, Hacettepe, İstanbul Üni Cerrahpaşa, Sabri Ülker
E. Guideline updates + ICD-11 — NICE NG222, WHO ICD-11, IAPT UK Manual
"""

import csv
from pathlib import Path

REG = Path("/sessions/hopeful-cool-bell/mnt/cbt_knowledge_base/registry/source_registry.csv")

NEW = [
    # A. Clinical assessment scales (reference for card content)
    {
        "source_id": "kroenke_2001_phq9_001",
        "title": "Kroenke K, Spitzer RL, Williams JBW. The PHQ-9: Validity of a brief depression severity measure. JGIM 2001;16(9):606-13",
        "url": "https://doi.org/10.1046/j.1525-1497.2001.016009606.x",
        "source_type": "seminal_paper",
        "license": "citation_reference",
        "bucket": "B",
        "commercial_use_allowed": "false",
        "notes": "PHQ-9 depression severity scale — 9 madde, klinik depresyon taraması. 5/10/15/20 eşikleri (hafif/orta/ortaağır/ağır). Reference-only; chatbot self-scoring TOOL sunmaz.",
        "review_status": "needs_review",
    },
    {
        "source_id": "spitzer_2006_gad7_001",
        "title": "Spitzer RL, Kroenke K, Williams JBW, Löwe B. A brief measure for assessing generalized anxiety disorder: the GAD-7. Arch Intern Med 2006;166(10):1092-7",
        "url": "https://doi.org/10.1001/archinte.166.10.1092",
        "source_type": "seminal_paper",
        "license": "citation_reference",
        "bucket": "B",
        "commercial_use_allowed": "false",
        "notes": "GAD-7 generalized anxiety scale — 7 madde. 5/10/15 eşikleri. Klinik yaygın kaygı taraması. Reference-only, self-scoring TOOL değil.",
        "review_status": "needs_review",
    },
    {
        "source_id": "cohen_1983_pss_001",
        "title": "Cohen S, Kamarck T, Mermelstein R. A global measure of perceived stress. J Health Soc Behav 1983;24(4):385-96",
        "url": "https://doi.org/10.2307/2136404",
        "source_type": "seminal_paper",
        "license": "citation_reference",
        "bucket": "B",
        "commercial_use_allowed": "false",
        "notes": "Perceived Stress Scale (PSS-10 / PSS-14) — 'algılanan stres' klasik ölçüm. work_stress + life_transitions modüllerinde stres seviyesi framework anchor.",
        "review_status": "needs_review",
    },
    {
        "source_id": "weathers_2013_pcl5_001",
        "title": "Weathers FW, Litz BT, Keane TM, Palmieri PA, Marx BP, Schnurr PP. The PTSD Checklist for DSM-5 (PCL-5). National Center for PTSD (2013)",
        "url": "https://www.ptsd.va.gov/professional/assessment/adult-sr/ptsd-checklist.asp",
        "source_type": "clinical_assessment",
        "license": "us_gov_public",
        "bucket": "B",
        "commercial_use_allowed": "false",
        "notes": "PCL-5 — DSM-5 PTSD self-report ölçek, 20 madde. VA (US) resmi klinik değerlendirme aracı. trauma_awareness modülünün klinik anchor'ı.",
        "review_status": "needs_review",
    },
    {
        "source_id": "bastien_2001_isi_001",
        "title": "Bastien CH, Vallières A, Morin CM. Validation of the Insomnia Severity Index as an outcome measure for insomnia research. Sleep Med 2001;2(4):297-307",
        "url": "https://doi.org/10.1016/S1389-9457(00)00065-4",
        "source_type": "seminal_paper",
        "license": "citation_reference",
        "bucket": "B",
        "commercial_use_allowed": "false",
        "notes": "Insomnia Severity Index (ISI) — 7 madde, uykusuzluk şiddet ölçümü. insomnia modülü kart içeriği için klinik anchor.",
        "review_status": "needs_review",
    },

    # B. Third-wave CBT (currently missing — critical gap)
    {
        "source_id": "hayes_2004_act_001",
        "title": "Hayes SC, Strosahl KD, Wilson KG. Acceptance and Commitment Therapy: The Process and Practice of Mindful Change (2nd ed). Guilford Press (2012)",
        "url": "https://contextualscience.org/act",
        "source_type": "seminal_book",
        "license": "citation_reference",
        "bucket": "B",
        "commercial_use_allowed": "false",
        "notes": "Steven Hayes ACT (Acceptance and Commitment Therapy) — 3rd wave CBT. 6 çekirdek süreç: cognitive defusion, acceptance, present-moment awareness, self-as-context, values, committed action. ACBS resmi anchor.",
        "review_status": "needs_review",
    },
    {
        "source_id": "segal_mbct_2018_001",
        "title": "Segal ZV, Williams JMG, Teasdale JD. Mindfulness-Based Cognitive Therapy for Depression (2nd ed). Guilford Press (2018)",
        "url": "https://www.guilford.com/books/Mindfulness-Based-Cognitive-Therapy-for-Depression/Segal-Williams-Teasdale/9781462537037",
        "source_type": "seminal_book",
        "license": "citation_reference",
        "bucket": "B",
        "commercial_use_allowed": "false",
        "notes": "Segal-Williams-Teasdale MBCT — depresyon nüksü önlemi için mindfulness + CBT hibriti. NICE'ın önerdiği kanıta dayalı yaklaşımlardan biri. depression modülünde anchor.",
        "review_status": "needs_review",
    },
    {
        "source_id": "kabat_zinn_1990_mbsr_001",
        "title": "Kabat-Zinn J. Full Catastrophe Living: Using the Wisdom of Your Body and Mind to Face Stress, Pain, and Illness. Delacorte (1990/2013)",
        "url": "https://www.penguinrandomhouse.com/books/98285/full-catastrophe-living-revised-edition-by-jon-kabat-zinn/",
        "source_type": "seminal_book",
        "license": "citation_reference",
        "bucket": "B",
        "commercial_use_allowed": "false",
        "notes": "Jon Kabat-Zinn MBSR (Mindfulness-Based Stress Reduction) — Massachusetts Üni tıp merkezinde geliştirdiği 8-haftalık program. Genel stres + kronik ağrı için kanıta dayalı. work_stress + trauma_awareness cross.",
        "review_status": "needs_review",
    },
    {
        "source_id": "neff_2003_self_compassion_001",
        "title": "Neff K. Self-compassion: An alternative conceptualization of a healthy attitude toward oneself. Self and Identity 2003;2(2):85-101",
        "url": "https://doi.org/10.1080/15298860309032",
        "source_type": "seminal_paper",
        "license": "citation_reference",
        "bucket": "B",
        "commercial_use_allowed": "false",
        "notes": "Kristin Neff — Self-Compassion Scale + 3 boyutu (self-kindness, common humanity, mindfulness). low_self_esteem + grief_loss modüllerinde anchor. CCI self-compassion workbook zaten kayıtlıydı; bu asıl teorik kaynak.",
        "review_status": "needs_review",
    },
    # C. Meta-analyses (kanıta dayalı temel)
    {
        "source_id": "hofmann_2012_cbt_meta_001",
        "title": "Hofmann SG, Asnaani A, Vonk IJJ, Sawyer AT, Fang A. The Efficacy of Cognitive Behavioral Therapy: A Review of Meta-analyses. Cognit Ther Res 2012;36(5):427-40",
        "url": "https://doi.org/10.1007/s10608-012-9476-1",
        "source_type": "systematic_review",
        "license": "citation_reference",
        "bucket": "B",
        "commercial_use_allowed": "false",
        "notes": "Hofmann et al. 2012 — CBT'nin farklı bozukluklarda etkililiğinin sistematik review of meta-analyses. Tüm modüller için 'kanıta dayalı çerçeve' temel referans.",
        "review_status": "needs_review",
    },
    {
        "source_id": "cuijpers_2016_cbt_depression_meta_001",
        "title": "Cuijpers P, Cristea IA, Karyotaki E, Reijnders M, Huibers MJH. How effective are cognitive behavior therapies for major depression and anxiety disorders? A meta-analytic update. World Psychiatry 2016;15(3):245-58",
        "url": "https://doi.org/10.1002/wps.20346",
        "source_type": "systematic_review",
        "license": "citation_reference",
        "bucket": "B",
        "commercial_use_allowed": "false",
        "notes": "Cuijpers et al. 2016 — depresyon ve kaygı bozukluklarında CBT'nin güncel meta-analitik değerlendirmesi. Kronikleşme + koruyucu etki bulguları.",
        "review_status": "needs_review",
    },
    {
        "source_id": "butler_2006_cbt_empirical_status_001",
        "title": "Butler AC, Chapman JE, Forman EM, Beck AT. The empirical status of cognitive-behavioral therapy: A review of meta-analyses. Clin Psychol Rev 2006;26(1):17-31",
        "url": "https://doi.org/10.1016/j.cpr.2005.07.003",
        "source_type": "systematic_review",
        "license": "citation_reference",
        "bucket": "B",
        "commercial_use_allowed": "false",
        "notes": "Butler-Beck 2006 — CBT'nin ampirik statüsü. Anxietisi bozuklukları, depresyon, yeme, PTSD, çocukluk kaygısı — hepsi için etki büyüklükleri.",
        "review_status": "needs_review",
    },

    # D. TR academic institutions
    {
        "source_id": "hacettepe_psikiyatri_001",
        "title": "Hacettepe Üniversitesi Tıp Fakültesi Psikiyatri Anabilim Dalı",
        "url": "https://www.hacettepe.edu.tr/",
        "source_type": "academic_institution",
        "license": "public_reference",
        "bucket": "B",
        "commercial_use_allowed": "false",
        "notes": "Ankara Hacettepe Üni Psikiyatri A.D. — TR'nin en güçlü psikiyatri araştırma-tedavi merkezlerinden. Uzman yönlendirmesi + akademik referans.",
        "review_status": "needs_review",
    },
    {
        "source_id": "bogazici_psikoloji_001",
        "title": "Boğaziçi Üniversitesi Psikoloji Bölümü",
        "url": "http://www.psy.boun.edu.tr/",
        "source_type": "academic_institution",
        "license": "public_reference",
        "bucket": "B",
        "commercial_use_allowed": "false",
        "notes": "İstanbul Boğaziçi Üni Psikoloji Bölümü — TR'nin lider psikoloji araştırma merkezlerinden. Klinik uygulama + TR-özel araştırma anchor.",
        "review_status": "needs_review",
    },
    {
        "source_id": "istanbul_cerrahpasa_ruh_sagligi_001",
        "title": "İstanbul Üniversitesi Cerrahpaşa Tıp Fakültesi Ruh Sağlığı ve Hastalıkları A.D.",
        "url": "https://cerrahpasa.istanbul.edu.tr/",
        "source_type": "academic_institution",
        "license": "public_reference",
        "bucket": "B",
        "commercial_use_allowed": "false",
        "notes": "İstanbul Cerrahpaşa Ruh Sağlığı A.D. — TR'nin klasik psikiyatri klinik referanslarından. Erişkin + çocuk-ergen poliklinik.",
        "review_status": "needs_review",
    },
    {
        "source_id": "sabri_ulker_ruh_sagligi_001",
        "title": "Sabri Ülker Vakfı — Ruh ve Beden Sağlığı Kaynakları",
        "url": "https://www.sabriulkerfoundation.org/",
        "source_type": "ngo_public_health",
        "license": "public_reference",
        "bucket": "B",
        "commercial_use_allowed": "false",
        "notes": "TR bağlamında halka açık ruh + beden sağlığı bilgi kaynağı üreten vakıf. Beslenme + stres + uyku için TR-dostu kaynak.",
        "review_status": "needs_review",
    },

    # E. Guideline updates + ICD-11
    {
        "source_id": "nice_ng222_depression_2022_001",
        "title": "NICE NG222 — Depression in adults: treatment and management (2022 update)",
        "url": "https://www.nice.org.uk/guidance/ng222",
        "source_type": "clinical_guideline",
        "license": "nice_reference",
        "bucket": "B",
        "commercial_use_allowed": "false",
        "notes": "NICE NG222 (2022) — depresyon tedavi rehberi büyük güncelleme. CG90'ı büyük ölçüde değiştirir. Stepped care + kanıta dayalı psikoterapi (CBT, IPT, MBCT, kişilerarası terapi) + ilaç.",
        "review_status": "needs_review",
    },
    {
        "source_id": "who_icd11_2019_001",
        "title": "WHO — International Classification of Diseases, 11th Revision (ICD-11)",
        "url": "https://icd.who.int/browse11/",
        "source_type": "clinical_taxonomy",
        "license": "who_reference",
        "bucket": "B",
        "commercial_use_allowed": "false",
        "notes": "WHO ICD-11 (2019, yürürlükte 2022) — uluslararası hastalık sınıflandırması. Complex PTSD, burnout, prolonged grief disorder ilk kez resmi tanı. Her modülün tanı çerçeve anchor'ı.",
        "review_status": "needs_review",
    },
    {
        "source_id": "iapt_manual_uk_001",
        "title": "NHS England — IAPT (NHS Talking Therapies) Manual",
        "url": "https://www.england.nhs.uk/publication/the-improving-access-to-psychological-therapies-manual/",
        "source_type": "clinical_guideline",
        "license": "nhs_crown",
        "bucket": "B",
        "commercial_use_allowed": "false",
        "notes": "IAPT (Improving Access to Psychological Therapies) — UK'nin stepped-care CBT hizmeti modeli. Self-help → guided self-help → high-intensity CBT basamakları. Bir chatbot self-help'in yerini konumlandırmak için referans.",
        "review_status": "needs_review",
    },
    {
        "source_id": "iasp_pain_2020_001",
        "title": "IASP — Revised Definition of Pain (2020)",
        "url": "https://www.iasp-pain.org/publications/iasp-news/iasp-announces-revised-definition-of-pain/",
        "source_type": "clinical_taxonomy",
        "license": "citation_reference",
        "bucket": "B",
        "commercial_use_allowed": "false",
        "notes": "International Association for the Study of Pain — ağrı tanımı (2020 güncelleme): 'gerçek ya da potansiyel doku hasarına bağlı, ya da öyle görünen hoş olmayan duyusal ve duygusal deneyim'. health_anxiety + kronik ağrı için anchor.",
        "review_status": "needs_review",
    },
]

# Append to registry
with open(REG, "a", newline="", encoding="utf-8") as f:
    fields = ["source_id","title","url","source_type","license","bucket","commercial_use_allowed","notes","review_status"]
    w = csv.DictWriter(f, fieldnames=fields, quoting=csv.QUOTE_MINIMAL)
    for row in NEW:
        w.writerow(row)

# Verify
with open(REG, encoding="utf-8") as f:
    all_rows = list(csv.DictReader(f))
print(f"Registry rows now: {len(all_rows)}")

from collections import Counter
type_counts = Counter(row["source_type"] for row in all_rows)
print("\nBy source_type:")
for t, n in sorted(type_counts.items(), key=lambda x: -x[1]):
    print(f"  {t:32s} {n}")

print(f"\nNew sources added this batch: {len(NEW)}")
for n in NEW:
    print(f"  {n['source_id']:45s} {n['source_type']}")
