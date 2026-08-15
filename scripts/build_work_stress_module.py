
"""Build the work_stress module end-to-end:
  1. Append work_stress sources to registry
  2. Append 10 work_stress CBT cards to cbt_cards.jsonl
"""

import csv
import json
from pathlib import Path

BASE = Path("/sessions/hopeful-cool-bell/mnt/cbt_knowledge_base")
REG = BASE / "registry" / "source_registry.csv"
CARDS = BASE / "cards" / "cbt_cards.jsonl"

# 1. Registry additions

NEW_SOURCES = [
    {
        "source_id": "nhs_stress_001",
        "title": "NHS — Get Help with Stress",
        "url": "https://www.nhs.uk/mental-health/feelings-symptoms-behaviours/feelings-and-symptoms/stress/",
        "source_type": "patient_guidance",
        "license": "nhs_crown",
        "bucket": "B",
        "commercial_use_allowed": "false",
        "notes": "NHS anchor for stress symptomatology (physical/mental/behavioural). Includes cause categorization + do/don't lists. Reviewed 2026-03; next review 2029-03.",
        "review_status": "needs_review",
    },
    {
        "source_id": "who_burnout_icd11_001",
        "title": "WHO — Burn-out an occupational phenomenon (ICD-11)",
        "url": "https://www.who.int/news/item/28-05-2019-burn-out-an-occupational-phenomenon-international-classification-of-diseases",
        "source_type": "clinical_taxonomy",
        "license": "who_reference",
        "bucket": "B",
        "commercial_use_allowed": "false",
        "notes": "WHO ICD-11 burn-out definition: three-dimensional model (exhaustion + cynicism + reduced professional efficacy). Explicitly NOT a medical condition. Anchors work_stress module framing.",
        "review_status": "needs_review",
    },
    {
        "source_id": "who_mental_health_workplace_2024_001",
        "title": "WHO — Mental Health at Work Fact Sheet (September 2024)",
        "url": "https://www.who.int/news-room/fact-sheets/detail/mental-health-at-work",
        "source_type": "policy_document",
        "license": "who_reference",
        "bucket": "B",
        "commercial_use_allowed": "false",
        "notes": "WHO 2024 policy anchor for workplace mental health interventions: manager training, organizational risk assessment, decent work.",
        "review_status": "needs_review",
    },
    {
        "source_id": "hse_stress_uk_001",
        "title": "UK Health & Safety Executive — Work-related Stress Guidance",
        "url": "https://www.hse.gov.uk/stress/what-to-do.htm",
        "source_type": "regulatory_guidance",
        "license": "hse_uk_reference",
        "bucket": "B",
        "commercial_use_allowed": "false",
        "notes": "HSE Management Standards approach: 6 workplace risk factors — demands, control, support, relationships, role, change. Structural reference; TR IS Kanunu ile eşleştirilir.",
        "review_status": "needs_review",
    },
    {
        "source_id": "maslach_burnout_inventory_001",
        "title": "Maslach C, Jackson SE. The measurement of experienced burnout. Journal of Occupational Behavior 1981;2:99-113",
        "url": "https://doi.org/10.1002/job.4030020205",
        "source_type": "seminal_paper",
        "license": "citation_reference",
        "bucket": "B",
        "commercial_use_allowed": "false",
        "notes": "Original Maslach Burnout Inventory (MBI) paper — theoretical foundation for WHO ICD-11 three-dimensional model. Citation-only reference.",
        "review_status": "needs_review",
    },
    {
        "source_id": "leiter_maslach_2016_burnout_review_001",
        "title": "Maslach C, Leiter MP. Understanding the burnout experience: recent research and its implications for psychiatry. World Psychiatry 2016;15(2):103-11",
        "url": "https://doi.org/10.1002/wps.20311",
        "source_type": "seminal_paper",
        "license": "citation_reference",
        "bucket": "B",
        "commercial_use_allowed": "false",
        "notes": "Maslach & Leiter 2016 World Psychiatry review — differentiates burnout from depression, discusses areas of worklife model (workload, control, reward, community, fairness, values). Anchor for work_stress cognitive framework.",
        "review_status": "needs_review",
    },
    {
        "source_id": "csgb_iskanun_mobbing_001",
        "title": "T.C. Çalışma ve Sosyal Güvenlik Bakanlığı — İşyerinde Psikolojik Taciz (Mobbing) Rehberi",
        "url": "https://www.csgb.gov.tr/",
        "source_type": "government_resource",
        "license": "public_domain_gov",
        "bucket": "B",
        "commercial_use_allowed": "false",
        "notes": "TR ÇSGB mobbing rehberi + İş Kanunu Madde 5 (ayrımcılık) ve 24/II-d (haklı fesih). TR yerelinde mobbing/psikolojik taciz için hukuki + kurumsal başvuru zemini.",
        "review_status": "needs_review",
    },
    {
        "source_id": "alo_170_calisma_001",
        "title": "ALO 170 — T.C. Çalışma ve Sosyal Güvenlik İletişim Merkezi",
        "url": "https://alo170.csgb.gov.tr/",
        "source_type": "government_resource",
        "license": "public_domain_gov",
        "bucket": "B",
        "commercial_use_allowed": "false",
        "notes": "TR resmi işçi hakları / mobbing / iş güvenliği bilgi hattı. 7 gün 24 saat. Kriz hattı DEĞİL — bilgilendirme hattı. Kartlarda safety hattı olarak kullanma; sadece iş hukuku danışma referansı.",
        "review_status": "needs_review",
    },
    {
        "source_id": "harvard_worklife_balance_001",
        "title": "Harvard T.H. Chan School of Public Health — Work, Health & Well-being",
        "url": "https://www.hsph.harvard.edu/centers-for-work-health-and-wellbeing/",
        "source_type": "academic_center",
        "license": "citation_reference",
        "bucket": "B",
        "commercial_use_allowed": "false",
        "notes": "Harvard T.H. Chan Work Health Wellbeing merkezi araştırma anchor — total worker health çerçevesi.",
        "review_status": "needs_review",
    },
    {
        "source_id": "apa_workplace_mental_health_001",
        "title": "APA Center for Workplace Mental Health",
        "url": "https://www.workplacementalhealth.org/",
        "source_type": "professional_association",
        "license": "apa_reference",
        "bucket": "B",
        "commercial_use_allowed": "false",
        "notes": "American Psychiatric Association Workplace Mental Health center — evidence-informed employer resources. Reference anchor.",
        "review_status": "needs_review",
    },
]

# Append to registry
with open(REG, "a", newline="", encoding="utf-8") as f:
    fields = ["source_id","title","url","source_type","license","bucket","commercial_use_allowed","notes","review_status"]
    w = csv.DictWriter(f, fieldnames=fields, quoting=csv.QUOTE_MINIMAL)
    for row in NEW_SOURCES:
        w.writerow(row)

# 2. Ten work_stress CBT cards

CARDS_DATA = [
    # 1. Psychoeducation — stress vs burnout
    {
        "id": "work_stressvsburnout_001",
        "topic": "work_stress",
        "type": "psychoeducation",
        "title_tr": "İş stresi ve tükenmişlik — aynı şey mi?",
        "content_tr": (
            "Bu ikisi çoğu zaman birbirine karıştırılır ama aynı şey değil.\n\n"
            "İş stresi (work stress): belirli bir talep, süre kısıtlı yoğun bir sezon, bir sunum, bir deadline, bir zorlu proje karşısında bedensel ve zihinsel gerilme. Ortadan kalkabilir, dinlenmeyle azalır. Fizyolojik olarak adrenalin ve kortizol seviyeleri geçici olarak yükselir.\n\n"
            "Tükenmişlik (burnout): Dünya Sağlık Örgütü'nün (WHO) ICD-11 sınıflandırmasında 'iş yerinde başarıyla yönetilememiş kronik strese bağlı bir sendrom'. Üç boyutu var:\n"
            "1. Enerji tükenmesi ya da bitkinlik hissi\n"
            "2. İşe karşı zihinsel mesafe artışı; işe dair olumsuzluk ya da alaycılık\n"
            "3. Mesleki verimlilikte azalma — 'işimi eskisi gibi iyi yapamıyorum' hissi\n\n"
            "Dinlenmeyle geçmez. Hafta sonu tatili sonrasında pazartesi hala tükenmiş hissediyorsan, klasik yorgunluktan öte bir şey vardır.\n\n"
            "Bir önemli not: WHO tükenmişliği bir 'hastalık' olarak sınıflandırmıyor — 'mesleki bir olgu' olarak sınıflandırıyor. Bu ayrım önemli, çünkü:\n"
            "• Tükenmişlik kişisel bir zayıflık değil; çalışma koşullarının yansımasıdır\n"
            "• Tanısı chatbot koyamaz; sadece hissedilebilir bir örüntü olarak fark edilir\n"
            "• Tükenmişlik + depresyon örtüşebilir ama aynı şey değildir\n\n"
            "Ne zaman depresyon ihtimalini düşünmek gerekir?\n"
            "• Yorgunluk sadece iş bağlamında değil, her yerde (hobiler, sosyal, cinsellik)\n"
            "• Hafta sonu bile mood düşük, hiçbir şey keyif vermiyor\n"
            "• Uyku ve iştah sürekli bozuk\n"
            "• Kendine dair olumsuz düşünceler ('değersizim, umut yok')\n"
            "• Yaşamdan kaçınma düşünceleri\n\n"
            "Böyle bir durumda depresyon modülüne bakmak ve mutlaka bir uzmana danışmak daha uygun."
        ),
        "safety_notes": "WHO ICD-11 tanımı verbatim değil, paraphrase. Burnout ≠ depression ayrımı net verildi. Kişisel zayıflık değil çerçevesi — damgalanmayı azaltıyor.",
        "source_refs": ["who_burnout_icd11_001", "maslach_burnout_inventory_001", "leiter_maslach_2016_burnout_review_001"],
        "review_status": "needs_review",
    },
    # 2. Cycle
    {
        "id": "work_cycle_002",
        "topic": "work_stress",
        "type": "psychoeducation",
        "title_tr": "İş stresinin sürdürücü döngüsü",
        "content_tr": (
            "İş stresi genelde bir tetikleyici ile başlar (yeni yönetici, artan iş yükü, bir zam yapılmadı, iş güvencesizliği). Ama kalıcı hale gelmesinin nedeni tetikleyici değil, tetikleyicinin peşinden gelen döngüdür. CBT'de bu döngü şöyle işler:\n\n"
            "1. Tetikleyici: Bir e-posta, bir toplantı, bir hafta sonu vardiyası, bir zam beklerken alamamak.\n\n"
            "2. Düşünce: 'Yetiştiremeyeceğim / işten atılacağım / patronum benden nefret ediyor / bu iş bana göre değil.' — otomatik düşünceler devreye girer.\n\n"
            "3. Duygu: Kaygı, öfke, üzüntü, çaresizlik.\n\n"
            "4. Bedensel tepki: Kaslar gerilir, kalp hızlanır, mide sıkışır, uyku bozulur.\n\n"
            "5. Davranışlar: Sürekli mesajlara bakmak, gece geç saatte çalışmak, hafta sonu 'sadece bir mail atayım', molasız çalışmak, sürekli evet demek, alkol/kafein/sigara artışı, insanlardan uzaklaşmak, sağlığı ihmal etmek.\n\n"
            "6. Sonuç: Beden ve zihin daha da yorulur. Uyku bozulur. Konsantrasyon düşer. Küçük hatalar artar.\n\n"
            "7. Yeni düşünce: 'Gördün mü — hata yaptım. Yetersizim.' → 2. adıma dön.\n\n"
            "Döngü kendini besleyerek büyür. Bir noktada tetikleyici geçmiş olsa bile (mesela zor proje bitti) döngü döner: beden hala tetikte, uyku hala bozuk, davranışlar aynı.\n\n"
            "İyi haber: döngünün her noktasına müdahale edilebilir. Sonraki kartlarda bu üç noktaya sırayla vuracağız:\n"
            "• Davranışsal: sınır koyma, mikro-molalar, mesaj-dışı zaman (kartlar 5, 6, 7)\n"
            "• Bilişsel: felaketleştirici düşüncelere karşı çalışma (kart 8)\n"
            "• Değer/anlam: mükemmelcilik + kimlik = iş denklemini gevşetme (kart 9)"
        ),
        "safety_notes": "Nedeni 'kişisel zayıflık' değil 'döngü' olarak çerçeveledi. İşyeri koşulları (yönetici, iş yükü, zam) meşru tetikleyici olarak kabul edildi — yani 'başın çare bul' değil.",
        "source_refs": ["nhs_stress_001", "leiter_maslach_2016_burnout_review_001", "hse_stress_uk_001"],
        "review_status": "needs_review",
    },
    # 3. Self-check
    {
        "id": "work_selfcheck_003",
        "topic": "work_stress",
        "type": "self_assessment",
        "title_tr": "İş stresi ve tükenmişlik için kendini kontrolü",
        "content_tr": (
            "Bu liste tanı koymaz — sadece son birkaç haftaya ayna tutar. Sana uyan maddeleri say.\n\n"
            "**Bölüm A — İş stresi belirtileri (NHS temelli)**\n"
            "• İşle ilgili olduğunda başım ağrıyor, sırtım/omzum geriliyor\n"
            "• Konsantre olmakta zorlanıyorum, karar veremiyorum\n"
            "• Sürekli bir 'yetişemiyorum' hissi\n"
            "• Sinirli, kırılgan, alıngan hissediyorum\n"
            "• Uyku bozuldu — ya uyuyamıyorum ya çok uyuyorum\n"
            "• Yemekten keyif almıyorum ya da aşırı yiyorum\n"
            "• Sigara/alkol/kafein tüketimi arttı\n"
            "• İş dışı hobilerimi bıraktım\n"
            "• Meslektaş/arkadaş görüşmesi azaldı\n\n"
            "3+ madde birkaç haftadır süregeliyorsa: bu modüldeki egzersizler işine yarayabilir. 6+ madde varsa daha ciddi.\n\n"
            "**Bölüm B — Tükenmişlik üç boyutu (WHO temelli)**\n\n"
            "Boyut 1 — Enerji tükenmesi:\n"
            "• Sabah kalktığımda zaten yorgunum\n"
            "• Hafta sonu sonrası pazartesi hala bitkin uyanıyorum\n"
            "• Tatil sonrası bir hafta geçmesine rağmen enerjim geri gelmedi\n\n"
            "Boyut 2 — İşten zihinsel mesafe / alaycılık:\n"
            "• İşimden nefret ediyorum ya da nötr / kayıtsız hissediyorum\n"
            "• Meslektaşlar, müşteriler, öğrenciler, hastalar — kimse benim için değerli gelmiyor\n"
            "• 'Umurumda değil' hissi işin çoğunda\n\n"
            "Boyut 3 — Mesleki verim düşüşü:\n"
            "• Eskiden yaptığım işi eskisi kadar iyi yapamıyorum\n"
            "• Küçük hatalar arttı\n"
            "• Basit görevler bile zorlaştı\n\n"
            "Her üç boyutta da en az bir madde varsa: tükenmişlik örüntüsü olabilir. Bu bir tanı DEĞİL, ama bir uzmana danışman iyi olur — özellikle 3+ ay sürüyorsa.\n\n"
            "**Bölüm C — Sınır aşan durumlar (bu modül YETMEZ, hemen ele al)**\n"
            "• Hafta sonu bile mood sürekli düşük, hiçbir şey keyif vermiyor → depresyon modülüne bak + hekime danış\n"
            "• Kendine zarar / yaşamdan kaçınma düşünceleri → hemen 112\n"
            "• İş yerinde fiziksel şiddet, cinsel taciz, ısrarlı psikolojik taciz (mobbing) → istismar/mobbing kart 10\n"
            "• Beklenmedik kilo kaybı, panik ataklar, sürekli fiziksel semptom → hekim değerlendirmesi\n"
            "• İntihar planı ya da yöntemi düşüncesi → hemen 112 / acil servis"
        ),
        "safety_notes": "Üç bölüm: NHS symptomlar / WHO burnout / kırmızı çizgiler. Mobbing için ayrı kart yönlendirmesi. Depresyon çakışması net. Tanı koymaz.",
        "source_refs": ["nhs_stress_001", "who_burnout_icd11_001", "maslach_burnout_inventory_001"],
        "review_status": "needs_review",
    },
    # 4. Values + priorities
    {
        "id": "work_values_004",
        "topic": "work_stress",
        "type": "exercise",
        "title_tr": "Bu iş neden burada — kendi değer haritanı çıkar",
        "content_tr": (
            "İş stresine çözüm ararken çoğumuz doğrudan 'ne yapabilirim' e atlıyoruz. Ama 'ne yapıyorum'un altında bir de 'ne için yapıyorum' var. Bu sorunun cevabı belirsizken teknikler yüzeysel kalır.\n\n"
            "Bu egzersizi 20-30 dakika ayırıp yaz — kafanda çevirme, elle yaz. Yazmak farklı bir şey açar.\n\n"
            "**Adım 1 — Ne için çalışıyorum?**\n"
            "Bu işten hayatına ne katıyor? Birden fazla olabilir. Her birine 0-10 puan ver (bu iş bu ihtiyacı ne kadar karşılıyor):\n"
            "• Maddi güvenlik\n"
            "• Anlam duygusu ('yaptığım şey önemli')\n"
            "• Kimlik ('ben bir X'im, X sağlar')\n"
            "• Sosyallik (meslektaşlar, ortak amaç)\n"
            "• Öğrenme / gelişim\n"
            "• Bir sonraki adım için basamak (bu iş kendisi değil, geleceğe yatırım)\n"
            "• Aileme yardım / sorumluluk\n\n"
            "**Adım 2 — Ne pahasına çalışıyorum?**\n"
            "Bu işin sana kaybettirdikleri neler? 0-10 puan (bu kayıp ne kadar acıtıyor):\n"
            "• Sağlık (uyku, spor, doktor)\n"
            "• Yakın ilişkiler (partner, çocuk, arkadaşlar)\n"
            "• Hobi / kendi zamanı\n"
            "• Öz-değer / benlik saygısı\n"
            "• Gelişim (yeni beceri öğrenmek için vakit)\n"
            "• Ruh sağlığı\n\n"
            "**Adım 3 — Denge:**\n"
            "İki listenin toplamını karşılaştır. Kayıplar kazançlardan çok yüksekse, döngü değişmediği sürece devam edemez.\n\n"
            "**Adım 4 — Kararın:**\n"
            "Ne yapabilirsin? Genellikle üç yol var:\n"
            "1. İşi değiştir (kısa vadede zor olabilir; 'daha kötü olmasın' korkusu yaygın)\n"
            "2. İşi yeniden şekillendir (job crafting): görev, zaman, sınırlar, ilişkiler üzerinden\n"
            "3. Bu işi kabul et ama telafi et: iş dışı alanları güçlendir (aile, hobi, arkadaş, sağlık)\n\n"
            "Çoğu zaman 2 ve 3'ün karışımı en gerçekçidir. 1'i düşünüyorsan bu chatbot karar veremez — ama bir klinik psikolog / kariyer danışmanı ile konuşmak yardımcı olabilir.\n\n"
            "Bu egzersiz 'iş bırak' baskısı yapmaz. Aksine — kendi verilerinden hareketle daha bilinçli tercih yapmanı sağlar."
        ),
        "safety_notes": "Karar dayatmıyor. Job crafting'i (Wrzesniewski) tanıtıyor. İş güvencesizliği kültürel gerçeği kabul ediliyor. Kariyer kararı için uzman yönlendirmesi.",
        "source_refs": ["leiter_maslach_2016_burnout_review_001", "harvard_worklife_balance_001"],
        "review_status": "needs_review",
    },
    # 5. Boundary setting
    {
        "id": "work_boundary_005",
        "topic": "work_stress",
        "type": "technique",
        "title_tr": "Sınır koymak — 'hayır' demenin CBT hali",
        "content_tr": (
            "Sınır koymak sanıldığı kadar kaba değil, ama sanıldığı kadar kolay da değil. Özellikle iş yerinde 'hayır' demenin kendine dair anlamı var: 'işten atılmalıyım / yeteneksiz görüneceğim / patrona hayır denmez / iş arkadaşlarımı hayal kırıklığına uğratırım'.\n\n"
            "**Neden zor:**\n"
            "Sınır koyamamamızın altında genelde bir inanç yatar: 'değerim, ne kadar çok yaptığıma bağlı' ya da 'reddedersem, sevilmem'. Bu inançlar (CBT dilinde 'temel inanç') sınırı aşmayı otomatikleştirir.\n\n"
            "**Neden gerekli:**\n"
            "Sınır koymayan biri sürekli fazla yükleniyor demektir. Sonuç: yorgunluk, hata, öfke — ve paradoksal olarak iş kalitesinin düşmesi. Sınır kısa vadede sıkıntı yaratabilir; uzun vadede seni ve işini korur.\n\n"
            "**4 tip iş yeri sınırı:**\n\n"
            "1. **Zaman sınırı**: 'Bu iş bugün için tamam, yarın devam edeceğim.' 'Toplantıdan sonra 10 dakika bloklanmış, sonra müsaitim.'\n\n"
            "2. **Görev sınırı**: 'Bu benim öncelik listemde yok; şu an X ve Y üzerinde çalışıyorum. Hangi öncelik değişmeli sizce?' Yönetici ile beraber öncelik listesi.\n\n"
            "3. **İletişim sınırı**: Mesai dışı e-posta/mesajlara cevap yok, ya da acil olanlara ayırt edilmiş bir kanal (örn. sadece telefon acil kabul edilir).\n\n"
            "4. **Enerji sınırı**: Öğle molası kutsaldır. Toplantı arası 5 dakika oturmak. Öğleden sonra kısa yürüyüş.\n\n"
            "**CBT 4-adım — bir sınır cümlesi kurmak:**\n\n"
            "Adım 1 — Durum: Ne olmasını istiyorsun ve neyi engelliyorsun?\n"
            "Adım 2 — Duygu ve düşünce: Sınır koyarken içinden ne geçiyor? ('Reddederse ne olur?')\n"
            "Adım 3 — Cümle: KISA + NÖTR + ALTERNATIF ver.\n"
            "  Örnek: 'Bu hafta yoğunum ama önümüzdeki hafta çalışabilirim' > 'Belki, bakayım' > 'Hayır yapamam'\n"
            "Adım 4 — Uygula ve sonucu gözlemle. Genelde sonuç, kafandaki senaryodan (patron çığlık atacak) daha nötr olur.\n\n"
            "**Yaygın engel: 'Kariyer görev-övgü sistemine bağlı, hayır dersem geride kalırım.'**\n"
            "Bu bazı iş yerlerinde gerçek. Ama uzun vadede tükenip performansı düşmüş biriyle vs. sınır koyup sürdürülebilir çalışan biri arasında ikincisi kazanır. Sınır koyma = tembellik değil, sürdürülebilirlik yatırımı.\n\n"
            "**Uyarı:** Toksik bir yönetici sınırı iyi karşılamayabilir. Böyle bir durumda bu teknik yetmez — HR, İK, hukuk danışmanı ya da iş değiştirme değerlendirmesi gündeme gelir."
        ),
        "safety_notes": "Toksik yönetici / iş güvencesizliği gerçekliğini kabul ediyor. 'Hayır' dogmatik değil — kalıp cümle örneği veriyor. Kariyer sonuçları için sorumluluk almıyor.",
        "source_refs": ["cci_worry_001", "hse_stress_uk_001"],
        "review_status": "needs_review",
    },
    # 6. Micro-breaks
    {
        "id": "work_microbreaks_006",
        "topic": "work_stress",
        "type": "technique",
        "title_tr": "Mikro-molalar — 90 dakika yoğunluk, 10 dakika sıfır",
        "content_tr": (
            "Bir bilim vardır: insan zihni saatlerce sürekli konsantre olamaz. Ultradyen ritim (Kleitman) çalışma kapasitesinin 90-120 dakikalık dalgalarda geldiğini gösteriyor. Bu dalganın tepesinde çalış, sonra 10-15 dakika duraksa.\n\n"
            "Mikro-molalar tembellik değil — bilimsel bir dinlenme protokolüdür. Hem konsantrasyonu hem enerjiyi korur. Molasız 8 saat vs. molalı 6 saat — genellikle molalı 6 saat daha çok iş bitirir.\n\n"
            "**Nasıl uygulanır:**\n\n"
            "1. Bir görev seç ve 90 dakikalık bir 'yoğunluk penceresi' aç. Telefon sessiz, kapı kapalı, e-posta bildirimi off, tarayıcıda gereksiz sekmeler kapalı.\n\n"
            "2. 90 dakika sonra hangi zil çalarsa (Pomodoro app, saat, sessiz alarm) — DUR. Görev bitmese bile.\n\n"
            "3. Mola başlar. 10-15 dakika. Ama bu mola SAATE bakmak, e-postaya bakmak, sosyal medya kaydırmak DEĞİL. Bunlar zihni dinlendirmez.\n\n"
            "Mikro-mola aktivite önerileri:\n"
            "• Pencere kenarına git, dışarı bak, gözü uzağa odakla (bilgisayardan kaynaklı yakın odaklanmayı gevşetir)\n"
            "• 2-3 dakika yürü (bina içinde, koridorda, merdivende)\n"
            "• Bir bardak su iç, sakince\n"
            "• 4-6 nefes egzersizi (yavaş, uzun ekshalasyon)\n"
            "• Kısa gerdirme (boyun, omuz, sırt)\n"
            "• Pencereyi aç, taze hava\n"
            "• Bir iş arkadaşı ile iş-dışı 3 dakikalık sohbet\n\n"
            "4. Mola sonrası tekrar 90 dakika. Günde 3-4 böyle blok idealdir.\n\n"
            "**Öğle molası kutsaldır** — masada yeme yerine, mümkünse dışarıda / farklı bir alanda yeme. Beyin bağlam değiştirdiğinde daha çok dinlenir.\n\n"
            "**Toplantı yoğun günlerde:** Bir toplantı ile diğerinin arasına 5-10 dakika bloklu boşluk koy. Ard arda toplantı beyin için travmadır.\n\n"
            "**Uyarı — bu her iş yerinde uygulanamaz:**\n"
            "• Vardiya işleri, bakım işleri, çağrı merkezi — burada mikro-molalar iş yerinin politikasına bağlı olabilir. Sendika/İK ile konuşulabilecek bir konu.\n"
            "• 'Herkes molasız çalışıyor, ben nasıl mola alırım' — bu döngü kırılmaz ise tükenmişlik kaçınılmaz olur. Meslektaşlarla ortak fikir birliği bazen mümkün olabilir.\n"
            "• Gösterişçi çalışma kültürü olan yerlerde mikro-molalar 'göze çarpmayacak' şekilde alınabilir (masada nefes, gözü kısa süre kapatmak)."
        ),
        "safety_notes": "Kültürel/kurumsal engelleri kabul ediyor. Mikro-mola tembellik değil bilimsel çerçevesi. Vardiya/çağrı merkezi gerçekliğini konuşuyor.",
        "source_refs": ["nhs_stress_001", "cci_procrastination_001"],
        "review_status": "needs_review",
    },
    # 7. Cognitive restructuring for work
    {
        "id": "work_thoughtrec_007",
        "topic": "work_stress",
        "type": "exercise",
        "title_tr": "İş düşünceleri — 'batacağım / atılacağım / yetersizim'",
        "content_tr": (
            "İş stresinin altında çoğu zaman düşünce örüntüleri vardır. En yaygınları:\n\n"
            "1. **Felaketleştirme**: 'Bu projeyi mahvedersem, işten atılacağım, sonra kimse işe almaz, evsiz kalırım.'\n\n"
            "2. **Zihin okuma**: 'Yönetici son toplantıda bana bakmadı, benden nefret ediyor demek ki.'\n\n"
            "3. **Ya hep ya hiç**: 'Bu sunumu mükemmel yapmalıyım. Yoksa tamamen başarısızım.'\n\n"
            "4. **Etiketleme**: 'Bu hatayı yaptım, ben bir salağım.'\n\n"
            "5. **'Malı olmalıyım'**: 'Bu yaşta manager olmalıydım, arkadaşlarımdan geride kaldım.'\n\n"
            "6. **Aşırı sorumluluk**: 'Ekipte moral düşük, bu benim yetersiz liderliğim yüzünden.'\n\n"
            "Bu düşünceler sana doğru gibi hissettirir ama iki sorunu var: (1) çoğu abartılı, (2) kaygıyı besleyip performansı düşürürler.\n\n"
            "**6-adımlı düşünce kaydı** (CBT klasiği):\n\n"
            "1. **Durum**: Ne oldu? (örn. 'Cuma öğleden sonra yönetici bir Slack mesajı attı: pazartesi konuşalım')\n\n"
            "2. **Otomatik düşünce**: Aklından ne geçti? Kelime kelime yaz. (örn. 'Beni işten çıkaracak / önemli bir hata bulmuşlar / kariyerim bitti')\n\n"
            "3. **Bu düşünceye ne kadar inanıyorum? (0-100)** (örn. 85)\n\n"
            "4. **Lehinde ve aleyhinde kanıt:**\n"
            "   Lehinde: 'Geçen ay bir raporda hata olmuştu; yönetici Cuma toplantısı istediğinde genelde ciddi bir konu olur.'\n"
            "   Aleyhinde: 'Son 6 ayda performansıma dair olumlu geri bildirim aldım; bu ay ekip taraması dönemi, yöneticinin herkesle konuşması normal; 'pazartesi konuşalım' cümlesi kötü bir haber şablonu değil; Cuma öğleden sonra bir mesaj bazen sadece bir mesajdır.'\n\n"
            "5. **Daha dengeli düşünce**: (örn. 'Yönetici benimle konuşmak istiyor. Konusu belli değil. Belki performans, belki yeni proje, belki başka bir şey. Şu an bilmiyorum ve kafamda senaryo kurmak boşuna. Pazartesi öğreneceğim.')\n\n"
            "6. **Yeni inanç puanı (0-100)**: (örn. 40, düşüş belirgin)\n\n"
            "Bir ekstra: eğer haftada 3+ kez bu tip düşüncelere yakalanıyorsan ve düşünceler işini kalitesiz yapmaya başladıysa, 4 hafta düzenli düşünce kaydı yaparak örüntülerini görebilirsin. Örüntü net olduğunda o düşüncenin otomatik gelmesi zayıflar."
        ),
        "safety_notes": "6 tipik iş düşünce hatası tanıtıldı — Burns'un klasik listesinden. 'Aşırı sorumluluk' özellikle yönetici pozisyondakiler için nüansla verildi. Egzersiz somut örnekli.",
        "source_refs": ["cci_worry_001", "cci_self_esteem_001", "beck_1979_cbt_depression_001"],
        "review_status": "needs_review",
    },
    # 8. Perfectionism at work
    {
        "id": "work_perfectionism_008",
        "topic": "work_stress",
        "type": "exercise",
        "title_tr": "İş yerinde mükemmelcilik — kalite mi, hapishane mi?",
        "content_tr": (
            "Mükemmelcilik ilk bakışta bir 'yüksek standart' gibi görünür. Ama mükemmelcilik ile 'kaliteli iş çıkarmak' aynı şey değildir.\n\n"
            "Kalite: doğru kararla, gerçekçi bir standart hedefiyle, işin gerektirdiği detay seviyesinde çalışmak.\n\n"
            "Mükemmelcilik: hedefi imkansız yüksek koyup, ulaşılmadığında kendine sert olmak, ulaşılınca da 'zaten gerekiyordu' demek.\n\n"
            "Kısa vadede: mükemmelciler çok iş çıkarabilir. Ama uzun vadede: aşırı çalışma → yorgunluk → hata → daha sert öz eleştiri → daha aşırı çalışma → tükenmişlik. Ve genellikle 'iyi' bile onlar için 'yeter' değil.\n\n"
            "**Mükemmelcilik testi — kendine sor:**\n"
            "• 'İyi' bir işi 'yetersiz' gibi hissediyor musun?\n"
            "• Bir işi bitiremediğinde, o iş kafanda döner mi (mesaj göndermeden önce 5 kez okurum vs.)?\n"
            "• Küçük bir hata seni saatlerce üzer mi?\n"
            "• Övgü aldığında 'hak etmiyorum' diyor musun?\n"
            "• Başkalarının seni takdir etmesi seni kısa süre iyi hissettirir ama sonra yok olur mu?\n\n"
            "3+ 'evet' → mükemmelcilik örüntüsü olabilir.\n\n"
            "**Bir egzersiz — 'yeter iyi' hedefi (good enough):**\n\n"
            "Bir hafta boyunca bir görev seç. Bu görevi 'mükemmel' değil, 'yeter iyi' yapmayı hedefle. 'Yeter iyi' senin standartlarına göre 70/100 gibi. Bu görev için harcadığın süre ile eskiden harcadığın süre arasındaki farkı fark et.\n\n"
            "Sonuçları gözlemle:\n"
            "• İş ne kadar farklı çıktı?\n"
            "• Başkaları farklı algıladı mı?\n"
            "• Sen ne hissettin?\n\n"
            "Çoğu insan bu deneyi yaptığında şunu bulur: 70/100 yaptığında bile iş 95/100 çıkıyor gibi görünüyor. Çünkü mükemmelcilik gereğinden çok emek harcatıyor.\n\n"
            "**Ayrı bir katman: benlik-değer mükemmelciliği**\n"
            "Bazı insanlar için mükemmelcilik sadece iş değil, kim olduklarına dair bir soru: 'ben ne kadar iyi işim, o kadar iyi insanım.' Bu inanç değişmediği sürece teknikler yüzeysel kalır. Böyle bir durum var ise: düşük öz-değer modülüne bakmak ve/veya bir klinik psikolog ile çalışmak yararlı olur.\n\n"
            "Kaynak: CCI Perth'in 'Perfectionism in Perspective' workbook'u — bu konuda kapsamlı 8-modül bir CBT rehberidir (İngilizce)."
        ),
        "safety_notes": "Mükemmelcilik vs kalite ayrımı net. 'Yeter iyi' bir egzersiz — dogmatik değil. LSE cross-referansı verildi.",
        "source_refs": ["cci_perfectionism_001", "cci_self_esteem_001"],
        "review_status": "needs_review",
    },
    # 9. Sleep, exercise, substance
    {
        "id": "work_lifestyle_009",
        "topic": "work_stress",
        "type": "technique",
        "title_tr": "İş stresini destekleyen zemin — uyku, hareket, kafein, alkol",
        "content_tr": (
            "İş stresi ile bedensel zemin birbiriyle konuşur. Zemin kötüyse stres daha çok etkiler; iyiyse aynı stres daha az yıpratır. Bu bir 'sihirli çözüm' değil — sadece sistemin gerçekliği.\n\n"
            "**Uyku**\n"
            "İş stresinin altında en yaygın 'gizli' faktör kötü uykudur. Uyku yoksunluğu ile ilgili şey:\n"
            "• Duygusal regülasyon zayıflar (küçük bir e-posta katlanılmaz gelir)\n"
            "• Konsantrasyon %30-50 düşebilir\n"
            "• Karar verme kalitesi bozulur — özellikle sosyal/etik kararlar\n"
            "• Kortizol seviyesi yükselir → stres tepkisi hipertrof olur\n\n"
            "Yani 6 saat uyuyup 10 saat çalışmak, 8 saat uyuyup 8 saat çalışmaktan daha az verimli. Uykusuzluk modülüne bak (biz de yaptık).\n\n"
            "**Hareket**\n"
            "Günde 20-30 dakika hafif-orta yoğunlukta hareket → stres hormonlarını dengeler, endorfin salgılatır, uykuyu iyileştirir. Spor salonu şart değil: hızlı yürüyüş, merdiven, evde vücut ağırlığı.\n"
            "İpucu: iş çıkışı yürüyerek eve dönmek (mümkünse) 'iş bitirdim' geçiş ritüelidir. Fizyolojik bir 'off switch'.\n\n"
            "**Kafein**\n"
            "Bir kahve iyidir, 6 kahve intihardır. Kafein yarı ömrü 5-6 saat. 3'de içilen espresso gece 9'da hala yarı miktarda kanında. Uyku bozulur → ertesi gün daha yorgun → daha çok kahve → döngü. Öğleden sonra 3'ten sonra kafein YOK — buradan başla.\n\n"
            "**Alkol / sigara**\n"
            "İş stresinden alkole dönmek çok yaygın bir örüntü — ama alkol kısa vadede gevşetir, uzun vadede uyku kalitesini bozar, kaygıyı besler (asıl kötü his ertesi gün gelir), enerjiyi düşürür. Sigara da kafein gibi bir stimulanttır — gevşetici değildir.\n"
            "Bu iki maddenin iş stresinden kaynaklı artışını fark edersen: bu kendisiyle bir problem, ayrı bir konu. Küçümseme.\n\n"
            "**Ekran**\n"
            "İş bittikten sonra hemen sosyal medya / haber siteleri açmak beyin için 'iş bitmedi' sinyalidir. En az 30 dakikalık 'ekran-siz geçiş' iş ile ev arasında bir tampon.\n\n"
            "**Beslenme**\n"
            "Öğün atlamak → kan şekeri dalgalanması → sinirlilik + konsantrasyon düşüşü. Öğle yemeğinde ağır un/şeker → 3'de enerji çöker. Basit gerçekler ama iş yerinde ihmal ediliyor.\n\n"
            "**Sosyal bağ**\n"
            "İş stresinin tampon faktörü: iş dışı ilişkiler. Bir yakınla haftada bir görüşmek, iş dışı bir grup (spor, dernek, ders), aile toplantısı. Stresi paylaşmak stresi yarıya indirir — bilim böyle diyor.\n\n"
            "Bu maddelerin hepsini bir anda değiştirmeye çalışma. Bir hafta bir maddeyi seç ve dene."
        ),
        "safety_notes": "Alkol/sigara ile ilgili nötr — küçümsemeden ama gerçekleri söyleyerek. Uykusuzluk modülüne cross-referans. Beslenme genel çerçevede kaldı, tanı yok.",
        "source_refs": ["nhs_stress_001", "cci_procrastination_001"],
        "review_status": "needs_review",
    },
    # 10. Safety net + mobbing
    {
        "id": "work_safetynet_010",
        "topic": "work_stress",
        "type": "safety",
        "title_tr": "Ne zaman uzmana, ne zaman İK'ya, ne zaman avukata — iş modülü için",
        "content_tr": (
            "İş stresi çoğu zaman self-help ile ele alınabilir. Ama bazı durumlar bu chatbot'un kapsamının çok dışında. Bu kartı atlama.\n\n"
            "**Derhal 112 / acil servis:**\n"
            "• Kendine zarar / yaşamına son verme düşüncesi ya da dürtüsü\n"
            "• İş yerinde fiziksel bir saldırıya uğradın\n"
            "• Şiddetli göğüs ağrısı, nefes darlığı, felç belirtileri (iş stresi zannetme, önce tıbbi acili ekarte et)\n\n"
            "**Bir ruh sağlığı uzmanı (psikiyatri hekimi ya da klinik psikolog):**\n"
            "• İş stresine ve/veya tükenmişliğe eşlik eden kalıcı düşük mood (hafta sonu, tatilde bile geçmiyor)\n"
            "• Uykusuzluk 3+ ay + bu modülü denediğin halde iyileşmiyor\n"
            "• Panik atak başlıyor\n"
            "• Kalıcı umutsuzluk, geleceğe dair 'çıkış yok' hissi\n"
            "• Alkol / madde tüketimin belirgin arttı (haftada 4+ gün alkol, ya da her akşam)\n"
            "• Aile / partnerle ilişki iş yüzünden ciddi zarar görüyor\n"
            "• Sürekli bir 'yanlış bir şey oluyor bende' hissi\n\n"
            "TR'de nasıl:\n"
            "• Aile hekimine başvur → sevk zinciri\n"
            "• Devlet hastanesi / üniversite hastanesi / özel klinik psikiyatri veya klinik psikoloji polikliniği\n"
            "• MHRS üzerinden randevu (182)\n\n"
            "**İnsan Kaynakları (İK) / işyeri hekimi ile konuşman gereken durumlar:**\n"
            "• İş yükü sürdürülebilir değil (nesnel olarak) — resmi ricayla değişmesi mümkün olabilir\n"
            "• Yöneticiyle sürekli çatışma\n"
            "• Ekip içi ciddi bir sorun\n"
            "• Sağlık sorunu iş performansını etkiliyor — makul konaklama (reasonable accommodation) hakkın olabilir\n\n"
            "Not: İK 'senin dostun' değildir; işverenin çıkarını korur. Yine de resmi bir kanal olarak dokümanlı bir başvuru koruyucu olabilir.\n\n"
            "**İş hukuku / avukat / sendika ile konuşman gereken durumlar — CİDDİ:**\n\n"
            "**İşyerinde psikolojik taciz (mobbing):**\n"
            "TR'de Yargıtay ve İş Kanunu mobbing'i şöyle tanımlar: 'İşyerinde bir çalışana yönelik sistematik olarak yapılan, bir süredir devam eden, kişilik haklarını ihlal eden davranışlar.' Örnekler:\n"
            "• Sistematik dışlama (toplantılara çağrılmama, bilgi verilmeme)\n"
            "• Sürekli aşağılama, alay etme, azarlanma\n"
            "• İş yükü kasıtlı olarak imkansız ayarlanması\n"
            "• Yeteneğinin altında iş verme (küçük düşürme)\n"
            "• Sözlü ya da yazılı tehdit\n"
            "• Cinsel taciz\n\n"
            "Bunlardan biri sende varsa:\n"
            "1. Yaşadıklarını YAZ — tarih, saat, ne oldu, kim vardı. Kanıt zinciri kur.\n"
            "2. Mesaj / e-posta gibi yazılı kanıtı sakla.\n"
            "3. ALO 170'i ara — TR Çalışma ve Sosyal Güvenlik Bakanlığı iletişim hattı. 7/24. Bilgi al.\n"
            "4. İK'ya yazılı başvur (e-posta) — konuşma dahil değil, yazılı.\n"
            "5. Bir iş hukuku avukatı ile görüş — bir seanslık danışma bile yön verir.\n"
            "6. Ruh sağlığı desteği al — mobbing psikolojik olarak yıpratır, tek başına atlatılacak bir şey değil.\n\n"
            "**Ayrımcılık, taciz, şiddet:**\n"
            "İş Kanunu Madde 5 (ayrımcılık yasağı) ve Madde 24/II-d (haklı fesih hakkı) senin lehine hükümler içerir. Bir avukatla konuş.\n\n"
            "**Cinsel taciz:**\n"
            "Cinsel taciz hem TCK hem İş Kanunu kapsamında suçtur. Delili sakla. Bir avukat + polis + kadın örgütü (Mor Çatı gibi) yardım kanalları vardır.\n\n"
            "**Bu chatbot ne yapamaz:**\n"
            "• Hukuki tavsiye veremez\n"
            "• İK'ya ne yazacağını yazamaz (avukatın yapmalı)\n"
            "• Terapi yapmaz — self-help çerçevesi sunar sadece\n"
            "• Bir tanı koyamaz\n\n"
            "Bu chatbot bir uzman değildir. Kendini iyi hissetmiyorsan lütfen bir insana ulaş — aile hekimi, klinik psikolog, arkadaş, aile, avukat, meslektaş."
        ),
        "safety_notes": "TR-özel mobbing tanımı Yargıtay çerçevesinden alındı. ALO 170 bilgi hattı olarak, kriz hattı OLMAYARAK ayrıştırıldı. Cinsel taciz için polis + Mor Çatı yönlendirmesi. İK'nın 'işverenin çıkarını koruduğu' gerçekliği net söylendi.",
        "source_refs": ["nhs_stress_001", "who_burnout_icd11_001", "csgb_iskanun_mobbing_001", "alo_170_calisma_001"],
        "review_status": "needs_review",
    },
]

with open(CARDS, "a", encoding="utf-8") as f:
    for c in CARDS_DATA:
        f.write(json.dumps(c, ensure_ascii=False) + "\n")

# Verify

with open(REG, encoding="utf-8") as f:
    reg_rows = list(csv.DictReader(f))
with open(CARDS, encoding="utf-8") as f:
    all_cards = [json.loads(ln) for ln in f]

print(f"Registry sources: {len(reg_rows)}")
print(f"CBT cards total:  {len(all_cards)}")
from collections import Counter
tc = Counter(c["topic"] for c in all_cards)
print()
print("By topic:")
for t, n in sorted(tc.items()):
    print(f"  {t:20s} {n}")
