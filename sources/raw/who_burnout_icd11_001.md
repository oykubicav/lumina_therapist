# WHO Burnout ICD-11 — Raw Source Extract

**Source ID:** who_burnout_icd11_001
**URL:** https://www.who.int/news/item/28-05-2019-burn-out-an-occupational-phenomenon-international-classification-of-diseases
**Publisher:** World Health Organization
**Fetched:** 2026-07-23
**Published:** 28 May 2019
**License:** WHO. Bucket B, synthesize only
**Source type:** clinical_taxonomy

## Central definition (verbatim WHO)

"Burn-out is a syndrome conceptualized as resulting from chronic workplace stress that has not been successfully managed. It is characterized by three dimensions:

- feelings of energy depletion or exhaustion;
- increased mental distance from one's job, or feelings of negativism or cynicism related to one's job; and
- reduced professional efficacy.

Burn-out refers specifically to phenomena in the occupational context and should not be applied to describe experiences in other areas of life."

## Critical clinical distinction

"Burn-out is included in the 11th Revision of the International Classification of Diseases (ICD-11) as an occupational phenomenon. **It is not classified as a medical condition.**"

ICD-11 chapter: 'Factors influencing health status or contact with health services' — reasons for contact with health services that are NOT illnesses.

## Why this matters for our product

This shapes work_stress module framing at the root level:

1. **Burnout ≠ depression** — although they share features (exhaustion, low motivation), burnout is domain-specific (work) and does not require depressive core (persistent low mood, anhedonia across contexts, sleep/appetite disturbance not specific to work).

2. **Burnout is NOT a diagnosis** to which our chatbot can refer someone. It's a description of a state.

3. **The three-dimensional model** (exhaustion + cynicism + reduced efficacy) is the WHO-official structure. Any burnout self-check card MUST use these three dimensions, not folk-taxonomy.

4. **Scope boundary in the safety framing**: if someone with "burnout" also shows depression features (anhedonia in ALL contexts, not just work; sleep problems that persist on weekends/leave; passive suicidal ideation), this crosses from burnout to depression — which routes to the depression module and a professional evaluation.

## Cross-reference

The WHO Mental Health at Work fact sheet (September 2024) is the companion policy document — see https://www.who.int/news-room/fact-sheets/detail/mental-health-at-work

## Use in our product

- **work_burnout_002** card (Tükenmişlik nedir?) — MUST cite WHO three-dimensional model verbatim as anchor
- **work_selfcheck_003** — self-assessment uses exhaustion / cynicism / reduced efficacy triad
- **work_when_seek_help_010** — depression cross-over as escalation trigger

## TR adaptation

- ICD-11 tanımı çeviri: "iş yerinde başarıyla yönetilememiş kronik strese bağlı bir sendrom"
- "Occupational phenomenon" = "mesleki bir olgu" — TR'de "hastalık" olarak çerçevelenmemesi çok önemli (kültürel damgalanma azaltıcı)
- "Reduced professional efficacy" TR'de "işini iyi yapamıyorum" hissi olarak tercüme edilebilir

**Do not copy** — the definition is public; the framing must be paraphrased in card copy.
