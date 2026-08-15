# Kaynak Taraması — Coverage Özeti

**Son güncelleme:** 2026-07-24
**Toplam kaynak:** **129** (hepsi en az bir kartın `source_refs` alanında cited — 0 orphan)
**Modül sayısı:** 11 (health_anxiety, panic, gad, depression, low_self_esteem, insomnia, work_stress, relationship_stress, grief_loss, life_transitions, trauma_awareness)
**Toplam CBT kartı:** 110 (her modülde 10, ortalama 3.2 kaynak/kart, toplam 351 kart→kaynak referansı)
**Regresyon testleri:** 78 (safety_classifier smoke test %100 geçiyor)

**Kural:** Bir kaynak registry'de kalır ancak en az bir kartın `source_refs`'inde cited ise. Kartsız kaynak = orphan = silinir. Bu politika `scripts/audit_orphan_sources.py` ile check edilebilir.

Bu chatbot'un bilgi tabanı, 58 farklı yüksek-kalite kaynak taranarak oluşturulmuştur. Aşağıda kaynak türü ve yayıncı ailesi bakımından dağılım:

## Kaynak türü dağılımı

| Tür | Sayı |
|---|---|
| Patient guidance (NHS, RCPsych vb.) | 10 |
| Self-help workbook (CCI Perth) | 9 |
| Clinical guideline (NICE, APA, WHO) | 8 |
| Self-help guide (CNTW, HPFT) | 6 |
| Self-help PDF (Oxford Health NHS) | 5 |
| Systematic review (Cochrane) | 5 |
| Seminal CBT model paper | 5 |
| Medical / mental health guidance | 4 |
| Professional society / government | 4 |
| Diğer (crisis, leaflet, seminal book) | 2 |
| **TOPLAM** | **58** |

## Yayıncı ailesi

| Yayıncı | Kaynak |
|---|---|
| Seminal CBT makaleleri + kitaplar (Beck, Clark, Wells, Fennell, Salkovskis, Harvey, van der Kolk, Herman, Siegel, Hazan-Shaver, Sue Johnson, Worden, Bridges, Schlossberg, Kobasa, Erikson, Wrzesniewski, Prinstein, Maslach, Leiter, Klass, Stroebe, Prigerson, Kübler-Ross, Figley) | 35 |
| TR klinik / hükümet / akademik kaynaklar (TPD, KBT Derneği, Sağlık Bakanlığı, İstanbul Tabip Odası, ÇSGB, ALO 170, KADES, 6284 sayılı Kanun, Mor Çatı, ŞÖNİM, Aile Bakanlığı, Diyanet, AFAD, Hacettepe, Boğaziçi, İstanbul Cerrahpaşa, Sabri Ülker) | 18 |
| NHS (UK) | 17 |
| NHS Foundation Trust'ları (CNTW, HPFT, Oxford Health) | 12 |
| CCI Perth (WA Sağlık Bakanlığı) | 10 |
| WHO (Dünya Sağlık Örgütü) | 8 |
| NICE (UK) | 6 |
| Cochrane sistemik meta-analizler | 5 |
| Klinik değerlendirme ölçekleri (PHQ-9, GAD-7, PSS, PCL-5, ISI) | 5 |
| Royal College of Psychiatrists | 4 |
| 3rd-wave CBT (ACT, MBCT, MBSR, Self-Compassion) | 4 |
| APA (American Psychological Association) | 3 |
| Meta-analitik derlemeler (Hofmann, Cuijpers, Butler) | 3 |
| **TOPLAM** | **130** |

## Modüller bazında birincil kaynaklar

### Sağlık kaygısı (health_anxiety)
- NHS Health Anxiety
- CNTW Health Anxiety Self-Help Guide
- HPFT Health Anxiety
- CCI Perth — Helping Health Anxiety (9 modül workbook, verified)
- Cochrane meta-analysis (Cooper et al. 2017)

### Panik (panic)
- NHS Panic Disorder
- CNTW Panic Self-Help Guide
- Oxford Health NHS Panic workbook (OH 197.20 series)
- CCI Perth — Panic Stations!
- Cochrane meta-analysis
- Clark 1986 seminal cognitive model paper

### Yaygın kaygı (GAD)
- NHS Generalised Anxiety Disorder
- CNTW Anxiety Self-Help Guide
- Oxford Health NHS Anxiety
- CCI Perth — What? Me Worry!? (Worry & Rumination)
- NICE Clinical Guideline CG113
- Cochrane meta-analysis (Hunot et al.)
- Wells 1995 metacognitive model paper
- Royal College of Psychiatrists — Anxiety

### Depresyon (depression)
- NHS Depression
- CNTW Depression Self-Help Guide
- Oxford Health NHS Depression workbook (OH 197.20)
- CCI Perth — Back from the Bluez
- NICE Clinical Guideline CG90
- Cochrane meta-analysis (CBT for depression)
- APA Clinical Practice Guideline (2019)
- WHO mhGAP intervention guide
- Beck 1979 seminal manual — Cognitive Therapy of Depression
- Royal College of Psychiatrists — Depression

### Düşük özdeğer (low_self_esteem)
- NHS Self-Esteem
- NHS Inform Scotland — Self-Esteem
- Oxford Health NHS Self-Esteem workbook (OH 198.20)
- CCI Perth — Improving Self-Esteem workbook
- CCI Perth — Perfectionism in Perspective (adjacent)
- CCI Perth — Self-Compassion
- CCI Perth — Put Off Procrastinating (adjacent)
- Fennell 1997 seminal LSE cognitive model paper

### Uykusuzluk (insomnia)
- NHS Insomnia
- CNTW Sleeping Problems Self-Help Guide
- Oxford Health NHS Sleep workbook
- CCI Perth — Sleep information
- NICE Clinical Guideline CG159 (sleep)
- Cochrane meta-analysis (CBT-I)
- Royal College of Psychiatrists — Sleep
- Harvey 2002 seminal cognitive model of insomnia

### İş Stresi (work_stress)
- NHS Stress — mental health symptom taxonomy + do/don't lists
- WHO ICD-11 Burnout — three-dimensional occupational phenomenon
- WHO Mental Health at Work Fact Sheet 2024
- UK Health & Safety Executive Management Standards (6 risk factors)
- Maslach & Jackson 1981 — original MBI seminal paper
- Maslach & Leiter 2016 World Psychiatry review — burnout vs depression
- CCI Perth — Perfectionism in Perspective
- CCI Perth — Worry & Rumination
- CCI Perth — Procrastination
- T.C. Çalışma ve Sosyal Güvenlik Bakanlığı — İşyerinde Mobbing Rehberi
- ALO 170 (TR ÇSGB iletişim hattı — bilgi, kriz DEĞİL)
- Harvard T.H. Chan Work Health & Wellbeing Center
- APA Center for Workplace Mental Health

### İlişki Stresi (relationship_stress)
- Gottman Institute — Four Horsemen (Criticism, Contempt, Defensiveness, Stonewalling) — verified verbatim examples
- Gottman Institute — Sound Relationship House Theory
- Gottman Institute — Domestic Violence Resources (Gottman's own IPV boundary)
- Hazan & Shaver 1987 — Romantic attachment seminal paper
- Sue Johnson — Emotionally Focused Therapy (EFT) / ICEEFT
- NHS Relationships & Wellbeing
- NHS Grief after bereavement or loss (for breakup grief)
- WHO 2021 — Violence against women global estimates
- **TR IPV kaynakları:**
  - KADES uygulaması (T.C. İçişleri Bakanlığı)
  - 6284 sayılı Kanun (Ailenin Korunması ve Kadına Karşı Şiddet)
  - Mor Çatı Kadın Sığınağı Vakfı
  - T.C. Aile ve Sosyal Hizmetler Bakanlığı — ŞÖNİM + 183 hattı

### Yas ve Kayıp (grief_loss)
- NHS — Grief after bereavement or loss (verified 2026-06)
- Kübler-Ross 1969 — On Death and Dying (5 aşama modeli — kaynağı ve sınırları belirtildi)
- Worden — Grief Counseling and Grief Therapy (4 Tasks of Mourning)
- Klass, Silverman, Nickman 1996 — Continuing Bonds (yasın Freudyen 'let go' modelini çürüten çalışma)
- Stroebe & Schut 1999 — Dual Process Model
- Prigerson et al. 2021 — DSM-5-TR Prolonged Grief Disorder validation
- WHO Bereavement Care (COVID-19)
- Türk Psikologlar Derneği (yas ve travma çalışma grupları)
- T.C. Diyanet İşleri Başkanlığı — Taziye ve Cenaze Rehberi (TR kültürel bağlam)
- CCI Perth — Coping with Loss (adjacent workbooks)

### Yaşam Geçişleri (life_transitions)
- William Bridges 1980 — Transitions: Making Sense of Life's Changes (3-faz modeli: Ending / Neutral Zone / New Beginning)
- Nancy Schlossberg 1981 — A Model for Analyzing Human Adaptation to Transition (4S: Situation / Self / Support / Strategies)
- Kobasa 1979 — Psychological Hardiness (commitment / control / challenge)
- Erikson 1968 — Identity: Youth and Crisis (psikososyal gelişim aşamaları)
- Wrzesniewski & Dutton 2001 — Job Crafting (iş / kariyer geçişi)
- WHO — Ageing and Life-Course (emeklilik geçişleri)
- NHS — Cope with a move (taşınma stresi)
- IOM — Migration and Mental Health (göç geçişi)
- T.C. Aile ve Sosyal Hizmetler Bakanlığı — Evlilik Öncesi Eğitim Programı (TR bağlamı)
- Prinstein 2020 — Developmental transitions in adolescence (ergen geçişleri)

### Travma Farkındalığı (trauma_awareness)
**Not: Bu modül travma TEDAVİSİ yapmaz — recognition + safe stabilization + uzman yönlendirmesi. TF-CBT, EMDR, prolonged exposure eğitimli klinisyen gerektirir.**
- NHS — PTSD (post-traumatic stress disorder) (verified 2026-04, symptoms + treatments + CPTSD)
- CNTW NHS — Post-Traumatic Stress Self-Help Guide
- Bessel van der Kolk 2014 — The Body Keeps the Score (nöroloji + beden + travma)
- Judith Herman 1992 — Trauma and Recovery (Complex PTSD kavramı + 3-fazlı recovery)
- Dan Siegel — Window of Tolerance (hiperarousal / hipoarousal çerçevesi)
- ISTSS 2018 — PTSD Treatment Guidelines (TF-CBT, CPT, EMDR, PE)
- SAMHSA — Trauma-Informed Care 6 prensibi
- Charles Figley 1995 — Compassion Fatigue (vicarious trauma / secondary traumatic stress)
- WHO — Doing What Matters in Times of Stress (illustrated self-help, TR bağlamına çevrildi)
- **TR-özel travma kaynakları:**
  - T.C. AFAD Psikososyal Destek (2023 Şubat deprem sonrası)
  - EMDR Türkiye Derneği (emdr-tr.org)
  - Türk Psikologlar Derneği + Türkiye Bilişsel-Davranışçı Terapiler Derneği travma çalışma grupları
  - SGDD-ASAM (Sığınmacı travma), Mor Çatı (aile içi), Cinsel Şiddetle Mücadele Derneği

### Güvenlik / triaj / etik
- NHS Chest Pain
- NHS Stroke (FAST)
- NHS Suicidal Thoughts
- NHS Psychosis
- NICE CG31 (OCD — scope boundary)
- NICE NG116 (PTSD — scope boundary)
- APA PTSD guideline (scope boundary)
- Salkovskis 1985 (OCD scope reference)
- WHO mhGAP
- T.C. Sağlık Bakanlığı Ruh Sağlığı Hizmetleri (TR routing)
- Türkiye Bilişsel ve Davranışçı Psikoterapiler Derneği
- İstanbul Tabip Odası

## Metodoloji notu

Tüm kaynaklar **Bucket B** politikasına tabi: sentez yapılır, birebir kopyalanmaz. Kartlar, birden fazla kaynaktaki iddiaları çapraz-doğrulanmış olarak sunar; her kart `source_refs` alanında hangi kaynaklardan sentezlendiğini şeffafça belirtir.

Peer-reviewed seminal makaleler (Clark 1986, Wells 1995, Fennell 1997, Beck 1979, Salkovskis 1985, Harvey 2002) doğrudan alıntı için değil, kart mimarilerinin teorik dayanağını göstermek için kayıtlıdır — örneğin panik kartlarındaki "felaketleştirici yanlış yorumlama" çerçevesi doğrudan Clark 1986 modelinden gelir.

Kaynak taraması **canlı** bir liste. Her yeni klinik veri geldiğinde `registry/source_registry.csv`'ye eklenir; içerik değişiklikleri kart dosyalarında `source_refs` alanı üzerinden görülebilir.

## Kapsam derinleştirme geçmişi

- **v1 (32 kaynak):** İlk 5 modülün NHS + NHS Trust + Oxford + WHO temeli
- **v2 (58 kaynak):** CCI Perth (9), Cochrane meta-analizler (3), APA/NICE ek rehberler, seminal CBT makaleleri (Clark, Wells, Fennell, Beck, Salkovskis, Harvey)
- **v3 (68 kaynak):** work_stress modülü (NHS Stress, WHO Burnout ICD-11, Maslach, HSE, ÇSGB, ALO 170)
- **v4 (80 kaynak):** relationship_stress modülü (Gottman, Hazan-Shaver, EFT, TR IPV — KADES/6284/Mor Çatı/ŞÖNİM)
- **v5 (90 kaynak):** grief_loss modülü (NHS grief, Kübler-Ross, Worden, Klass continuing bonds, Stroebe-Schut dual process, Prigerson PGD, Diyanet)
- **v6 (100 kaynak):** life_transitions modülü (Bridges, Schlossberg, Kobasa, Erikson, Wrzesniewski, WHO ageing, IOM migration, Aile Bakanlığı, Prinstein)
- **v7 (110 kaynak):** trauma_awareness modülü (NHS PTSD, van der Kolk, Herman C-PTSD, Siegel window of tolerance, ISTSS, SAMHSA, AFAD, EMDR Türkiye, Figley compassion fatigue)
- **v8 (130 kaynak):** 3rd-wave CBT + klinik ölçekler + TR akademik (ACT-Hayes, MBCT-Segal, MBSR-Kabat-Zinn, Self-Compassion-Neff, PHQ-9, GAD-7, PSS, PCL-5, ISI, Hofmann/Cuijpers/Butler meta-analizler, Hacettepe/Boğaziçi/Cerrahpaşa/Sabri Ülker, NICE NG222 2022, ICD-11, IAPT, IASP pain)
