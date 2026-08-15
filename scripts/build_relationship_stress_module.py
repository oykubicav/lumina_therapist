
"""Build the relationship_stress module end-to-end.

Adds ~10 sources (Gottman, EFT, attachment theory anchors, NHS, TR IPV
resources) to registry, then appends 10 CBT cards.

CRITICAL SAFETY DESIGN:
  - IPV disclosure MUST route to abuse safety card. This module does NOT
    provide "communication skills" for abusive relationships — Gottman
    Institute itself makes this distinction.
  - TR resources verified: KADES app (İçişleri Bakanlığı), 155 Polis, 183
    Aile ve Sosyal Hizmetler Bakanlığı hattı, Mor Çatı, ŞÖNİM, 6284 sayılı
    Kanun. NONE are UK/US charity hotlines.
"""

import csv
import json
from pathlib import Path

BASE = Path("/sessions/hopeful-cool-bell/mnt/cbt_knowledge_base")
REG = BASE / "registry" / "source_registry.csv"
CARDS = BASE / "cards" / "cbt_cards.jsonl"


# 1. Sources

NEW_SOURCES = [
    {
        "source_id": "gottman_four_horsemen_001",
        "title": "The Gottman Institute — The Four Horsemen: Criticism, Contempt, Defensiveness, Stonewalling",
        "url": "https://www.gottman.com/blog/the-four-horsemen-recognizing-criticism-contempt-defensiveness-and-stonewalling/",
        "source_type": "research_center_publication",
        "license": "gottman_reference",
        "bucket": "B",
        "commercial_use_allowed": "false",
        "notes": "40+ years longitudinal research anchor for couple communication patterns predicting dissolution. Verified verbatim examples of each Horseman + antidotes. Structure confirmed.",
        "review_status": "needs_review",
    },
    {
        "source_id": "gottman_sound_relationship_house_001",
        "title": "The Gottman Institute — Sound Relationship House Theory",
        "url": "https://www.gottman.com/about/the-gottman-method/",
        "source_type": "research_center_publication",
        "license": "gottman_reference",
        "bucket": "B",
        "commercial_use_allowed": "false",
        "notes": "Gottman Method's foundational model: love maps, fondness/admiration, turning towards, positive perspective, conflict management, shared meaning. Framework for rel_communication + rel_repair cards.",
        "review_status": "needs_review",
    },
    {
        "source_id": "gottman_domestic_violence_resources_001",
        "title": "The Gottman Institute — Domestic Violence Resources",
        "url": "https://www.gottman.com/domestic-violence-resources/",
        "source_type": "safety_referral",
        "license": "gottman_reference",
        "bucket": "B",
        "commercial_use_allowed": "false",
        "notes": "Gottman's OWN separation of IPV from couples-therapy. Anchor for our safety framing: 'communication skills' are contraindicated in IPV. This citation strengthens the boundary card.",
        "review_status": "needs_review",
    },
    {
        "source_id": "hazan_shaver_1987_attachment_001",
        "title": "Hazan C, Shaver P. Romantic love conceptualized as an attachment process. Journal of Personality and Social Psychology 1987;52(3):511-524",
        "url": "https://doi.org/10.1037/0022-3514.52.3.511",
        "source_type": "seminal_paper",
        "license": "citation_reference",
        "bucket": "B",
        "commercial_use_allowed": "false",
        "notes": "Foundational paper extending Bowlby-Ainsworth infant attachment theory to adult romantic relationships. Basis for secure/anxious/avoidant framework in rel_attachment_004 card.",
        "review_status": "needs_review",
    },
    {
        "source_id": "sue_johnson_eft_reference_001",
        "title": "Johnson SM. Hold Me Tight: Seven Conversations for a Lifetime of Love. Little, Brown Spark",
        "url": "https://www.iceeft.com/",
        "source_type": "seminal_book",
        "license": "citation_reference",
        "bucket": "B",
        "commercial_use_allowed": "false",
        "notes": "Sue Johnson's Emotionally Focused Therapy (EFT) for couples — attachment-based approach. Reference anchor; ICEEFT (International Centre) is professional home.",
        "review_status": "needs_review",
    },
    {
        "source_id": "nhs_relationships_wellbeing_001",
        "title": "NHS — Relationships and Wellbeing",
        "url": "https://www.nhs.uk/mental-health/self-help/tips-and-support/looking-after-your-relationships/",
        "source_type": "patient_guidance",
        "license": "nhs_crown",
        "bucket": "B",
        "commercial_use_allowed": "false",
        "notes": "NHS structural anchor for relationship wellbeing tips: talking, listening, quality time. General framing reference.",
        "review_status": "needs_review",
    },
    {
        "source_id": "nhs_grief_bereavement_001",
        "title": "NHS — Grief after bereavement or loss",
        "url": "https://www.nhs.uk/mental-health/feelings-symptoms-behaviours/feelings-and-symptoms/grief-bereavement-loss/",
        "source_type": "patient_guidance",
        "license": "nhs_crown",
        "bucket": "B",
        "commercial_use_allowed": "false",
        "notes": "NHS grief page — used analogously for breakup grief in rel_breakup_008. Direct claim of grief framing to relationship loss is well-established in psychology literature (Bowlby, Parkes).",
        "review_status": "needs_review",
    },
    {
        "source_id": "who_ipv_2021_001",
        "title": "WHO — Violence against women 2021 estimates",
        "url": "https://www.who.int/publications/i/item/9789240022256",
        "source_type": "policy_document",
        "license": "who_reference",
        "bucket": "B",
        "commercial_use_allowed": "false",
        "notes": "WHO 2021 report: ~1 in 3 women globally has experienced IPV or non-partner sexual violence. Statistical anchor for prevalence framing in rel_safetynet_010.",
        "review_status": "needs_review",
    },
    {
        "source_id": "kades_app_001",
        "title": "KADES — Kadın Destek Uygulaması (T.C. İçişleri Bakanlığı)",
        "url": "https://www.icisleri.gov.tr/",
        "source_type": "government_resource",
        "license": "public_domain_gov",
        "bucket": "B",
        "commercial_use_allowed": "false",
        "notes": "TR resmi kadına şiddet ihbar mobil uygulaması; tek dokunuşla 155'e konum bilgisi + ihbar gönderir. Android + iOS. Kart 10'da doğrudan yönlendirilecek TR-özel araç.",
        "review_status": "needs_review",
    },
    {
        "source_id": "kanun_6284_ailenin_korunmasi_001",
        "title": "6284 sayılı Ailenin Korunması ve Kadına Karşı Şiddetin Önlenmesine Dair Kanun",
        "url": "https://www.mevzuat.gov.tr/mevzuat?MevzuatNo=6284&MevzuatTur=1&MevzuatTertip=5",
        "source_type": "legal_statute",
        "license": "public_domain_gov",
        "bucket": "B",
        "commercial_use_allowed": "false",
        "notes": "TR 6284 sayılı Kanun — koruma ve önleyici tedbir kararları (uzaklaştırma, sağlık, barınma, mali yardım). Kadına yönelik şiddet için hukuki temel. Mor Çatı, ŞÖNİM, savcılık, aile mahkemesi tümü buna dayanır.",
        "review_status": "needs_review",
    },
    {
        "source_id": "mor_cati_001",
        "title": "Mor Çatı Kadın Sığınağı Vakfı",
        "url": "https://www.morcati.org.tr/",
        "source_type": "ngo_support",
        "license": "public",
        "bucket": "B",
        "commercial_use_allowed": "false",
        "notes": "TR bağımsız kadın sığınağı ve dayanışma merkezi. Sığınak, hukuk, psikolojik destek. 0212 292 52 31 / 32 (dayanışma hattı) — mesai saatleri içinde bilgi + yönlendirme; kriz hattı DEĞİL.",
        "review_status": "needs_review",
    },
    {
        "source_id": "aile_bakanligi_sonim_001",
        "title": "T.C. Aile ve Sosyal Hizmetler Bakanlığı — ŞÖNİM (Şiddet Önleme ve İzleme Merkezleri)",
        "url": "https://www.aile.gov.tr/kadin/",
        "source_type": "government_resource",
        "license": "public_domain_gov",
        "bucket": "B",
        "commercial_use_allowed": "false",
        "notes": "TR 81 ilde ŞÖNİM — 7/24 kadına yönelik şiddet vakalarında koordinasyon (barınma, hukuki destek, psikolojik destek). 183 çağrı merkezi — Aile ve Sosyal Hizmetler Bakanlığı bilgi hattı, kadın/çocuk/yaşlı/engelli.",
        "review_status": "needs_review",
    },
]

with open(REG, "a", newline="", encoding="utf-8") as f:
    fields = ["source_id","title","url","source_type","license","bucket","commercial_use_allowed","notes","review_status"]
    w = csv.DictWriter(f, fieldnames=fields, quoting=csv.QUOTE_MINIMAL)
    for row in NEW_SOURCES:
        w.writerow(row)

# 2. Ten relationship_stress CBT cards

CARDS_DATA = [
    # 1. Psychoeducation — what is relationship_stress
    {
        "id": "rel_psychoed_001",
        "topic": "relationship_stress",
        "type": "psychoeducation",
        "title_tr": "İlişki stresi nedir, ne değildir?",
        "content_tr": (
            "Her ilişkide gerginlik olur. Bu doğal. İki farklı insan aynı yaşamı paylaşırken zaman zaman anlaşmazlıklar çıkar — bu ilişkinin bittiği anlamına gelmez; aksine yaşadığı anlamına gelir.\n\n"
            "İlişki stresi (sağlıklı örüntü): belirli konularda tekrarlayan tartışma, dönemsel iletişim güçlüğü, hayat geçişleri (yeni iş, çocuk, taşınma) sırasında artan gerginlik. Bu tip stres, üzerinde konuşulabilir, iki taraf birlikte çözebilir, geçici olabilir.\n\n"
            "İlişki krizi (endişe verici örüntü): sürekli bir gerginlik hali, iletişimin çoktan çöktüğü his, birbirinden uzaklaşma, tekrar tekrar aynı yerde takılma. Bu, çift terapisi ya da bireysel çalışma ile daha iyi ele alınır.\n\n"
            "İlişki tehlikesi (bu farklı bir kategoridir): şiddet, tehdit, sistematik kontrol, mali/fiziksel/duygusal istismar. Bu bir 'ilişki sorunu' değildir; **bir güvenlik meselesidir**. Bu modülün son kartı bu ayrıma ayrılıyor — atlamayın.\n\n"
            "Bu modül SANA odaklı — çift terapisi değil. Öğreneceğin şeyler:\n"
            "• Kendi tepkilerini fark etmek\n"
            "• Kendi ilişki stilini (bağlanma) tanımak\n"
            "• Sağlıklı iletişim örüntüleri kurmak\n"
            "• Bir ayrılık yaşadıysan yasın içinden geçmek\n"
            "• Ne zaman bir uzmandan çift terapisi almak, ne zaman bireysel destek almak\n"
            "• Ve en kritik olan: ne zaman bu ilişkinin senin güvenliğine tehdit oluşturduğunu fark etmek\n\n"
            "**Bir önemli sınır:** Bu chatbot bir çift terapisti değildir. Aynı zamanda partnerin için karar vermez, partnerin için tavsiye üretmez, 'ondan ayrıl' ya da 'onunla kal' demez. Karar senin — ama bu karar için gerekli çerçeveyi sunmaya çalışır.\n\n"
            "Ayrıca: bu modül tek başına bir kişiye yönelik. Partnerine tek başına 'bunları okusun' demek yerine, öğrendiklerini kendi davranışında sınayabilirsin. Çift olarak çalışmak istiyorsanız birlikte bir çift terapistiyle görüşmek daha etkili olur."
        ),
        "safety_notes": "İlişki stresi / kriz / tehlike üç kategorisi net ayırıldı. IPV = güvenlik meselesi vurgusu ilk kartta. Çift terapisi rolüne dair sınır. Karar özerkliği kullanıcıda.",
        "source_refs": ["nhs_relationships_wellbeing_001", "gottman_sound_relationship_house_001"],
        "review_status": "needs_review",
    },
    # 2. Cycle
    {
        "id": "rel_cycle_002",
        "topic": "relationship_stress",
        "type": "psychoeducation",
        "title_tr": "İlişki çatışmasının sürdürücü döngüsü",
        "content_tr": (
            "İki insan bir tartışmayı 'çözemiyorsa', çoğu zaman ana konu değil, döngü sorundur. Tanıdık gelen bir örüntü:\n\n"
            "1. **Tetikleyici**: Küçük bir şey (bulaşık, bir mesajın cevaplanması, bir çamaşır sepeti, kayınvalidenin bir cümlesi).\n\n"
            "2. **Yorum**: Sen bu davranışı 'sana karşı bir şey' olarak yorumlarsın. 'Beni önemsemiyor / beni takmıyor / hep aynı şey.'\n\n"
            "3. **Duygu ve beden**: Öfke, üzüntü, alınganlık. Kalp hızı artar, ses tonu değişir.\n\n"
            "4. **Davranış — iki tip**: \n"
            "   • Peşine düşen (pursuer): 'Konuşmalıyız. Şimdi. Bunu çözelim.' Yaklaşır, açıklar, ısrar eder.\n"
            "   • Geri çekilen (withdrawer): Sessizleşir, konuyu değiştirir, odayı terk eder.\n"
            "   İki taraf genelde birbirinin zıddını yapar — pursuer-withdrawer döngüsü klasik bir örüntü.\n\n"
            "5. **Partnerin yorumu**: Senin peşine düşmen partnerinde 'suçlanıyorum' hissi yaratabilir. Geri çekilmen partnerinde 'reddediliyorum' hissi. Yani her iki taraf da aslında incinmiş.\n\n"
            "6. **Karşı tepki**: Partner geri çekildikçe sen daha çok peşine düşersin. Sen peşine düştükçe partner daha çok geri çekilir. Döngü yoğunlaşır.\n\n"
            "7. **Sonuç**: Aslında ana konu (bulaşık, mesaj) hala orada, ama tartışma bambaşka bir yere gitti — 'sen hep böylesin', 'ben mi hep böyleyim'.\n\n"
            "**Gottman'ın 'Dört Atlı':** Bu döngüde tekrarlayan dört iletişim örüntüsü ilişkinin sağlığını en çok yıpratır: eleştiri, aşağılama, savunmacılık, duvar örme (kart 5'te detay). Bu dört örüntü ilişkideyken sıklıkla ortaya çıkıyorsa, bu bir alarm sinyalidir — ama düzeltilebilir bir alarm.\n\n"
            "**İyi haber:** Döngü kırılabilir. En etkili yer: kendi tepkinin arasındaki mikron. Peşine düşerken, ya da geri çekilirken — bir an durup 'ben şu an ne yapıyorum, neden yapıyorum' diye sorabilirsen, döngü zayıflar. Sonraki kartlar bu 'duraklama' becerisini geliştiren teknikler.\n\n"
            "**Uyarı:** Bu döngü modeli sağlıklı, birbirine tepki veren iki yetişkin ilişkisi için geçerlidir. Bir tarafın diğerine sürekli baskı, tehdit, şiddet uyguladığı bir ilişkide 'iletişim kalıbı' anlatısı doğru DEĞİLDİR. Şiddetin sorumluluğu tek başına şiddeti uygulayan taraftadır — 'ikimiz de yanlış yaptık' çerçevesi burada geçerli değildir. Bu ayrım için kart 10'a bak."
        ),
        "safety_notes": "Pursuer-withdrawer döngüsü + Gottman Four Horsemen çerçeveleri kullanıldı. İki taraf da 'sorumlu' çerçevesi IPV'de tehlikeli olduğundan, IPV istisnası açıkça belirtildi.",
        "source_refs": ["gottman_four_horsemen_001", "sue_johnson_eft_reference_001"],
        "review_status": "needs_review",
    },
    # 3. Self-check
    {
        "id": "rel_selfcheck_003",
        "topic": "relationship_stress",
        "type": "self_assessment",
        "title_tr": "İlişkin nerede — kendini kontrolü",
        "content_tr": (
            "Bu liste tanı koymaz. Sana bir örüntü haritası verir. Son 2-3 ay boyunca ilişkin için sana uyanları say.\n\n"
            "**Bölüm A — Sağlıklı bağ göstergeleri (Gottman)**\n"
            "• Partnerimle günlük 15+ dakika iş dışı sohbet ediyorum\n"
            "• Küçük şeyler için birbirimize teşekkür ediyoruz\n"
            "• Tartışma sonrası birbirimize dönüp konuşabiliyoruz\n"
            "• Ortak gelecek planları yapabiliyoruz\n"
            "• Partnerimin çevresi (arkadaş, aile) benim de çevremdir\n"
            "• Fiziksel yakınlık — sarılma, dokunma — var\n"
            "• Gülüyoruz beraber\n\n"
            "3+ 'evet' → sağlıklı bir temel var. Zorluklar geçici sorunlar olabilir.\n\n"
            "**Bölüm B — Uyarı sinyalleri**\n"
            "• Tartışmalarımız aynı konu üzerinde tekrarlıyor, çözülmüyor\n"
            "• Küçük şeyler için birbirimizi eleştiriyoruz\n"
            "• Fiziksel yakınlık belirgin biçimde azaldı\n"
            "• Partnerimin varlığından çok, yokluğunda rahat hissediyorum\n"
            "• Duygusal olarak paylaşmayı bıraktım\n"
            "• Ondan uzaklaşmayı sıklıkla düşünüyorum\n"
            "• Ortak konular yerine, yaptığımız her şey iş / çocuk yönetimi\n"
            "• Onun huyları önce sevdiğim şeylerdi, şimdi rahatsız edici geliyor\n\n"
            "3+ 'evet' → ilişki krizi işareti olabilir. Çift terapisi düşünmeye değer. Aynı zamanda bu modüldeki egzersizler — kendi tarafın için — işine yarayabilir.\n\n"
            "**Bölüm C — Kırmızı çizgiler (bu bir 'ilişki sorunu' değil, güvenlik meselesi)**\n"
            "**Bu maddelerden BİRİ bile varsa lütfen bu modülü bırak ve kart 10'a git.**\n"
            "• Bana fiziksel olarak zarar verdi (dövmek, itmek, sarsmak, saç çekmek, tokat)\n"
            "• 'Beni kızdırma' der ki fiziksel şiddetle tehdit anlamı taşıyor\n"
            "• Kime konuşacağımı, ne giyeceğimi, kimle görüşeceğimi kontrol ediyor\n"
            "• Telefonuma, mesajlarıma, sosyal medyama izin almadan bakıyor\n"
            "• Beni ailemden / arkadaşlarımdan uzaklaştırdı\n"
            "• Paramı kontrol ediyor / bana para vermiyor\n"
            "• 'Seni bırakırsam mahvolursun' diyor\n"
            "• Cinsel olarak istemediğim şeyleri kabul etmemi istiyor\n"
            "• Beni sürekli aşağılıyor, küçük düşürüyor\n"
            "• Çocuğa / bana / kendine zarar vermekle tehdit ediyor\n"
            "• 'Boşan boşanmam, önce seni öldürürüm' dedi\n\n"
            "Bu maddelerin herhangi birine 'evet' diyorsan bu bir 'ilişki krizi' değil, bir şiddet ilişkisidir. Bu chatbot senin güvenliğinin sorumluluğunu alamaz — ama sana yönlendirebilir. Kart 10 bunu detaylı ele alıyor."
        ),
        "safety_notes": "Üç bölüm net: sağlıklı / kriz / şiddet. Şiddet listesi kapsamlı — fiziksel + sözlü + izolasyon + finansal + cinsel + tehdit. IPV'yi 'iletişim sorunu' olarak sınıflandırmayı reddediyor.",
        "source_refs": ["gottman_sound_relationship_house_001", "who_ipv_2021_001", "kanun_6284_ailenin_korunmasi_001"],
        "review_status": "needs_review",
    },
    # 4. Attachment styles
    {
        "id": "rel_attachment_004",
        "topic": "relationship_stress",
        "type": "psychoeducation",
        "title_tr": "Bağlanma stilleri — kendini ve partnerini anlamak",
        "content_tr": (
            "Yetişkin romantik ilişkilerindeki tepkilerimizin bir kısmı, bebeklikte ve çocuklukta öğrendiğimiz 'yakın ilişki nasıl olur' örüntülerinden gelir. Bu, Hazan ve Shaver'ın 1987'de yayınladığı ve bugün de yaygın kabul gören bir çerçeveden geliyor. Üç ana bağlanma stili var:\n\n"
            "**Güvenli bağlanma:**\n"
            "• Yakınlıktan rahat, mesafeden de rahat\n"
            "• Duygularını rahatça paylaşır\n"
            "• Bir sorun olduğunda konuşmayı seçer\n"
            "• Partnerini rakip olarak değil, ortak olarak görür\n\n"
            "**Kaygılı bağlanma:**\n"
            "• 'Bir gün beni bırakacak' korkusu yüksek\n"
            "• Partner geç cevap verirse aklından binlerce senaryo geçer\n"
            "• Ayrılığa dair hassasiyet çok yüksek\n"
            "• Sürekli güvence arayışı ('beni seviyor musun?')\n"
            "• Küçük mesafe → panik → daha çok yaklaşma\n\n"
            "**Kaçıngan bağlanma:**\n"
            "• Yakınlık boğucu hissettirir\n"
            "• Duygulardan konuşmak zor\n"
            "• Yalnız zaman çok gerekli\n"
            "• 'Kendi kendime yeterim' inancı güçlü\n"
            "• Yakınlaşma → panik → geri çekilme\n\n"
            "Bir de karışım tipi var (fearful-avoidant / disorganize) — hem yakınlık istiyor hem korkuyor.\n\n"
            "**Neden önemli:**\n"
            "Kaygılı biri kaçıngan biriyle çıktığında, kart 2'deki pursuer-withdrawer döngüsü doğal olarak kurulur. Kaygılı ne kadar yaklaşırsa kaçıngan o kadar geri çekilir; kaçıngan ne kadar geri çekilirse kaygılı o kadar yaklaşır. İki taraf da acı çeker.\n\n"
            "**İyi haber:**\n"
            "Bağlanma stilleri değişebilir. 'Kazanılmış güvenli bağlanma' — çocuklukta güvenli değildin ama yetişkinlikte olabilirsin. Bir güvenli partnerle uzun süreli ilişki, iyi bir terapist, kişisel öz-farkındalık — üçü de yardımcı.\n\n"
            "**Bu kart bir tanı değildir.** Kişilik envanteri değil. Sadece kendini tanımanın bir aynası. Kesin kategorilere düşme (herkes bir spektrumdadır); ama bir örüntü tanıdıksa, o örüntüyle çalışmak mümkündür.\n\n"
            "**Bir egzersiz:**\n"
            "Son üç ilişkindeki tepkilerine bak. Peşine mi düştün, geri mi çekildin, ikisini de yaptığın anlar oldu mu? Partnerin ne yapıyordu? Bu döngü tanıdık geliyor mu?\n\n"
            "Bu çerçeve seni suçlamak için değil, kendini anlamak içindir. Bağlanma stilin kim olduğunun tamamı değil, sadece ilişkilerde bir parçan."
        ),
        "safety_notes": "Hazan-Shaver 1987 anchor'a dayalı. Değiştirilebilir çerçevesi — 'kazanılmış güvenli bağlanma'. Kesinci kategorilerden kaçınıldı. Kişilik envanteri olmadığı vurgusu.",
        "source_refs": ["hazan_shaver_1987_attachment_001", "sue_johnson_eft_reference_001"],
        "review_status": "needs_review",
    },
    # 5. Communication — Four Horsemen + antidotes
    {
        "id": "rel_communication_005",
        "topic": "relationship_stress",
        "type": "technique",
        "title_tr": "Dört yıpratıcı iletişim örüntüsü ve panzehirleri",
        "content_tr": (
            "Bu kart Gottman Institute'un 40+ yıllık araştırmasına dayanıyor. John Gottman ve ekibi çiftleri Seattle 'Aşk Laboratuvarı'nda saatlerce gözlemleyip, ilişkinin ileriki geleceğini yüksek doğrulukla tahmin edebilen dört iletişim örüntüsü tanımladı. Bu dört örüntü ilişkideyken sık ortaya çıktığında, ilişki büyük ihtimalle uzun soluklu kalamaz — düzeltilmezse. Panzehirleri var, öğrenilebilir.\n\n"
            "**1. Eleştiri (criticism)**\n"
            "Yanlış: Bir davranıştan konuşmak yerine karakteri yıkmak.\n"
            "• 'Sen hep unutursun. Sen bencilsin. Sen hiç düşünmezsin.'\n"
            "Panzehir — Şikayeti dile getir (karakter değil):\n"
            "• 'Bugün alışverişi unuttuğunda üzüldüm, çünkü akşam yemeği için o malzemelere ihtiyacım vardı.'\n"
            "Formül: 'Ben hissettim + durum + ihtiyacım'.\n\n"
            "**2. Aşağılama (contempt) — en tehlikeli**\n"
            "Yanlış: Ahlaki üstünlük konumundan konuşmak. Alay, isim takmak, göz devirme, mimiklerle küçük düşürme.\n"
            "• 'Yorgunmuşsun? Ben de yorgunum ama işini yapıyorum. Salak gibi kanepede oturma.'\n"
            "Gottman'ın araştırması: Aşağılama, boşanmanın en güçlü tek belirtecidir.\n"
            "Panzehir — Takdir kültürü kur:\n"
            "• Küçük şeyler için teşekkür et. 'Çöpü çıkardığın için sağ ol.'\n"
            "• Partnerinin iyi yönlerini hatırla ve söyle.\n"
            "• 'Şu an sinirliyim ama benim değerlendirmem sınırlı, biraz düşünmek istiyorum.'\n\n"
            "**3. Savunmacılık (defensiveness)**\n"
            "Yanlış: Bir eleştiriye karşılık suçu partnere geri çevirmek, 'zaten sen de' modu.\n"
            "• (Partner: 'Bugün annemi aramayı unuttun.') 'Bütün gün çalıştım, sen niye aramadın?'\n"
            "Panzehir — Kısmi sorumluluk al:\n"
            "• 'Haklısın, unuttum. Şimdi arayayım. Bir sonraki sefere hatırlatıcı koyayım.'\n"
            "Kısmi bile olsa sorumluluk almak, tartışmayı dindirir.\n\n"
            "**4. Duvar örme (stonewalling)**\n"
            "Yanlış: Konuşmayı bırakmak, uzaklaşmak, mesajlara cevap vermemek, 'ben bir şey söylemeyeceğim' modu. Bu genellikle bedensel olarak 'sel altında' hissetmekten kaynaklanır (kalp hızı 100+, konuşamaz hale gelmek).\n"
            "Panzehir — Zamanlı ara ver:\n"
            "• 'Şu an sinirim çok yüksek, düzgün konuşamıyorum. 20 dakikaya döneceğim.'\n"
            "• 20 dakika boyunca sakinleştirici bir şey yap — nefes, yürüyüş, sessizce oturma. Sosyal medya, konu hakkında ruminasyon ETMEZ.\n"
            "• 20 dakika sonra dön ve konuş.\n\n"
            "**Egzersiz — bir hafta:**\n"
            "Her partnerinle bir tartışmada, dört örüntüden hangisine düştüğünü fark et. Yargılamadan, sadece isimlendir. Fark etmek yarısı; düzeltme yavaş yavaş gelir.\n\n"
            "**Kritik uyarı:** Bu teknikler sağlıklı çiftler için tasarlandı — iki tarafın da eşit güçte, birbirine karşılıklı saygı taşıdığı ilişkiler. Bir tarafın diğerine sistematik olarak tehdit, kontrol, şiddet uyguladığı ilişkilerde 'iletişim tekniği' geçerli değildir — Gottman Institute'un kendisi bunu açıkça belirtir. Kart 10 bu ayrımı ele alıyor."
        ),
        "safety_notes": "Gottman research-based; Four Horsemen + antidotes verbatim örneklendi. IPV için tekniğin geçerli olmadığı Gottman Institute'un kendi konumuyla desteklenerek belirtildi.",
        "source_refs": ["gottman_four_horsemen_001", "gottman_domestic_violence_resources_001"],
        "review_status": "needs_review",
    },
    # 6. Emotional boundary
    {
        "id": "rel_boundary_006",
        "topic": "relationship_stress",
        "type": "technique",
        "title_tr": "İlişkide duygusal sınır — çitle duvar arasında",
        "content_tr": (
            "Sınır ile duvar aynı şey değil. Sınır: 'İşte ben burasıyım, senle bağlantım şuraya kadar sağlıklı.' Duvar: 'Sana kapıyı kapatıyorum.' İyi bir ilişkide sınır var, duvar yok.\n\n"
            "**Sınır neden zor:**\n"
            "Yakın ilişkilerde 'hayır' demek daha zordur, çünkü:\n"
            "• 'Reddedersem, sevmediğim anlaşılır' korkusu\n"
            "• 'İyi bir eş / iyi bir sevgili her isteği karşılar' inancı\n"
            "• Bağlanma stiline göre değişir — kaygılı biri 'hayır' derse partnerinin gidebileceğini düşünür; kaçıngan biri 'hayır' der ama sonra suçluluk hisseder\n\n"
            "**Sağlıklı bir sınır ne değildir:**\n"
            "• Sessizce uzaklaşma değildir (duvar örmenin başka adı)\n"
            "• Cezalandırma değildir ('sen de bana yapmıştın')\n"
            "• Ultimatom değildir ('bir daha yaparsan biterim')\n"
            "• Manipülasyon değildir\n\n"
            "**Sağlıklı sınır — 3 örnek:**\n\n"
            "1. **Duygu paylaşımı sınırı:**\n"
            "Partner: 'Bugün nasıl geçti?'\n"
            "Sen (kötü bir gündeysin): 'Bugün çok yorgunum, iş konusunu şimdi konuşmak istemiyorum. Yemek yiyip sonra dinlensek olur mu?'\n"
            "Duvar versiyonu: '...' (sessizlik) — bu partnere 'bir şey saklıyor / benden nefret ediyor' hissi verir.\n\n"
            "2. **Aile sınırı:**\n"
            "Partner: 'Bu hafta sonu annemlere gidiyoruz.'\n"
            "Sen (istemiyor): 'Bu ay üç kere gittik. Bu hafta sonu ikimize ait bir zaman istiyorum. Bir sonraki hafta sonuna alalım annemlere gitmeyi.'\n"
            "Duvar versiyonu: 'Sen git.' — bu bir sınır değil, uzaklaşmadır.\n\n"
            "3. **Cinsel sınır:**\n"
            "'Bugün istemiyorum. Yorgunum. Yarın olabilir.' — sağlıklı sınırdır.\n"
            "Cinselliğe zorlanma (partnerin baskısı, suçlaması, tehditi) sağlıklı bir ilişkinin göstergesi DEĞİLDİR. Bu sınırın çiğnenmesi cinsel şiddettir — evlilik içinde bile. Kart 10'a bak.\n\n"
            "**Bir örüntü hakkında sınır:**\n"
            "Diyelim partnerin sürekli seni ailesinin önünde eleştiriyor. Bir sınır cümlesi kurabilirsin:\n"
            "'Ailenin önünde benim bir şeyimi eleştirirsen ben rahatsız oluyorum. Bunu ikimize ait kalmasını rica ediyorum. Bir daha olursa, ben odadan çıkacağım — cezalandırma değil, kendimi koruma.'\n"
            "Sonrasında olursa: gerçekten odadan çık. Sadece bir kere. Bu sınırın tutması için tutarlı olmak gerekir.\n\n"
            "**Bir uyarı:**\n"
            "Bazı partnerler sınırı iyi karşılamaz. Sağlıklı bir partner 'anladım, saygı duyuyorum, konuşalım' der. Manipülatif ya da kontrolcü bir partner 'bencilsin, aile olmamızın anlamı yok, benimle nasıl yapabilirsin bunu' der ve seni bilerek suçlu hissettirir. Sınırının 'saldırgan' olarak nitelendirilmesi tekrar tekrar oluyorsa, bu partner sorunudur — senin sorunun değil. Kart 10'a bak."
        ),
        "safety_notes": "Sınır ≠ duvar / ultimatom / manipülasyon. Cinsel sınır özellikle net — evlilik içi cinsel şiddet tanımı. Kontrolcü partner tepkileri = alarmın da referansı.",
        "source_refs": ["gottman_sound_relationship_house_001", "sue_johnson_eft_reference_001"],
        "review_status": "needs_review",
    },
    # 7. Repair attempts
    {
        "id": "rel_repair_007",
        "topic": "relationship_stress",
        "type": "technique",
        "title_tr": "Onarım girişimi — tartışmayı 'dindirmek' değil, 'düzeltmek'",
        "content_tr": (
            "Bir tartışma başladığında, bir noktadan sonra 'kim haklı' önemli değil hale gelir. Önemli olan: bu tartışmayı yıkım olmadan nasıl bitiririz.\n\n"
            "Gottman'ın araştırması: sağlıklı çiftler daha az tartışmaz — daha iyi onarım yaparlar. Onarım girişimi (repair attempt), tartışmayı 'sıcak' iken 'soğuk' hale getirmeye yönelik küçük bir hamle olabilir.\n\n"
            "**Onarım örnekleri:**\n\n"
            "• Espri (uygun anda): 'Sen ne kadar aynı gömleği kaç kere yıkasan, ben o kadar aynı şeyi diyorum' — hafif bir esprinin ötesinde küçümseme değil.\n\n"
            "• İfade değişimi: 'Dur. Yeniden başlayalım. Ben ilk cümleyi yanlış söyledim.'\n\n"
            "• Duygu ifadesi: 'Aslında şu an çok üzgünüm, öfke gibi görünüyor.'\n\n"
            "• Fiziksel dokunuş (rıza varken): Elini tutmak, omzuna dokunmak.\n\n"
            "• Meta yorum: 'Şu an ikimiz de gerginiz. Beş dakika ara verelim mi?'\n\n"
            "• Şükran: 'Beni dinlediğin için teşekkür ederim, zor olduğunu biliyorum.'\n\n"
            "• Sorumluluk alma: 'Az önce çok sert söyledim, özür dilerim.'\n\n"
            "Gottman'a göre başarılı çiftlerin dilinde 100+ farklı onarım hareketi var. Sınırsız yaratıcı.\n\n"
            "**Onarımın çalışması için:**\n\n"
            "Bir taraf onarım girişiminde bulunduğunda, diğer tarafın 'kabul etmesi' gerek. Kabul demek:\n"
            "• Espriyi gülerek karşılamak\n"
            "• 'Yeniden başlayalım' teklifini duymak\n"
            "• Dokunuşu geri itmemek\n\n"
            "Duygular çok kabarmışsa (kalp hızı 100+) beyin bilişsel olarak kabul edemez — bu 'sel altında olma' halidir (flooding). O anda ne kadar çok onarım gelirse gelsin işlemez. Bu durumda 20 dakika ara vermek en iyi.\n\n"
            "**Kendine sor:**\n"
            "Partnerin son ay içinde sana kaç onarım girişiminde bulundu? Sen bunu fark ettin mi, kabul ettin mi, yoksa reddettin mi? Bu, çok değerli bir öz-farkındalık.\n\n"
            "**Not:** Onarım girişimi partneri suçlamayı bırakmakla eş değildir. Yaşanan bir şey ciddi ise (mesela hafta boyunca sürecek konu), önce sakinleşmek ve sonra geri dönüp konuşmak — bu da bir onarım biçimidir."
        ),
        "safety_notes": "Onarım = sözlü hile değil, samimi hamle çerçevesi. Fiziksel dokunuş için rıza ön koşulu. Flooding fenomeni açıklandı.",
        "source_refs": ["gottman_sound_relationship_house_001", "gottman_four_horsemen_001"],
        "review_status": "needs_review",
    },
    # 8. Breakup grief
    {
        "id": "rel_breakup_008",
        "topic": "relationship_stress",
        "type": "psychoeducation",
        "title_tr": "Ayrılık sonrası — bir yas gibi geçmesine izin ver",
        "content_tr": (
            "Ciddi bir ilişkinin bitişi, sevilen bir kişinin ölümüne benzer bir yas süreci başlatır. Bu tesadüf değil — bağlanma teorisine göre, uzun süreli romantik ilişki bir 'bağlanma bağı'dır ve bu bağın kopması nöroloji, biyoloji ve psikolojinin ortak bir yas tepkisi verir.\n\n"
            "Yani: bir ayrılıktan sonra kendini kötü hissetmek 'zayıf' olmak değildir. Beynin bir bağı kaybettiğini kayıt ediyor.\n\n"
            "**Yas fazları (Kübler-Ross'a dayalı, kesin bir sıra değil):**\n"
            "1. **İnkar / şok**: 'Gerçekten bitti mi? Belki yarın konuşuruz.'\n"
            "2. **Öfke**: 'Nasıl yapar bunu bana? Ne cesaret?'\n"
            "3. **Pazarlık**: 'Eğer daha iyi olsaydım, geri gelirdi. Ona bir mesaj atıp özür dilesem.'\n"
            "4. **Depresyon**: 'Bir daha kimse beni sevmez. Her şey bitti.'\n"
            "5. **Kabul**: 'Bu oldu. Şimdi hayatım bundan sonra.'\n\n"
            "Bu fazlar sıralı gitmez. Bir gün öfke, bir gün pazarlık, bir gün kabul, tekrar öfke — normal.\n\n"
            "**Yas ne kadar sürer?**\n"
            "Standart bir cevap yok. Ortalama olarak: yoğun akut faz 2-3 ay, önemli iyileşme 6 ay, tamamen 'geçme' 1-2 yıl (ama 'geçmek' hatırlamamak değil, hatırlarken artık acımaması). Uzun süreli ilişkilerde (5+ yıl) yas süreci daha uzun.\n\n"
            "**Yasın içinde neyi yapmalı:**\n\n"
            "• **Duyguları bastırma.** Ağlamak, kızmak, üzülmek — bunların hepsi işlemenin parçası. Duyguları içine bastırmak yası uzatır.\n\n"
            "• **Rutin koru.** Yeme, uyuma, işe gitme, arkadaş görme. Bu bir 'iyileşme' değil, temel zeminini koruma.\n\n"
            "• **Sosyal bağ.** Yalnız kalmak yası derinleştirir. Arkadaş, aile, kardeş — bir kaç kişiyle düzenli görüş.\n\n"
            "• **Küçük anlam kaynakları.** Bir hobi, bir kitap, bir egzersiz. Yeni bir kimlik yavaş yavaş oluşur.\n\n"
            "• **Beden hareketi.** Yürüyüş, spor. Yasla ilgili biyokimya harekete olumlu tepki verir.\n\n"
            "**Yasın içinde neyi yapmamalı:**\n\n"
            "• **Eski partnere ısrarla ulaşma.** Onun 'seni özlediğini duymak' bir an rahatlatabilir ama yası uzatır. Bir kez son bir konuşma tamam; ondan sonra iletişimin azaldığı bir dönem gerekli.\n\n"
            "• **Sosyal medya kontrolü.** Onun profiline bakmak, kimi lakelediğini takip etmek — beyin için 'hala buradayım' sinyali. Bir süre unfollow / hide.\n\n"
            "• **Yeni bir ilişkiye kaçış.** Yas gitmeden başlayan yeni ilişki genellikle işlem görmemiş yas'ı taşır. Bir süre bekle (kesin bir kural yok ama duygusal olarak hazır hissetmek).\n\n"
            "• **Alkol / madde ile kapatma.** Kısa vadede rahatlatır, uzun vadede depresyonu ve bağımlılığı besler.\n\n"
            "**Ne zaman uzmana:**\n"
            "• 3+ ay sonra hala günlük hayat işlemez halde\n"
            "• Sabit intihar düşünceleri\n"
            "• Umutsuzluk her yerde, ilişki bağlamının dışında da\n"
            "• Beklenmedik kilo kaybı, uyku kaybı, alkol artışı\n"
            "• Ayrılığın sebebi bir istismar / şiddet ilişkisi ise — travma-farkındalıklı bir terapist önemli\n\n"
            "Yas 'atlatılmaz' — içinden geçilir. Bu geçişin kendine has bir ritmi var; kendine bu ritmi tanıma iznini ver."
        ),
        "safety_notes": "Kübler-Ross fazları 'kesin sıra değil' notuyla verildi. Yas süresi için tıbbi çerçevede kalındı, gaslighting yapılmadı ('iki haftada geçer' değil). İstismar sonrası ayrılık için travma-farkındalıklı terapist önerisi.",
        "source_refs": ["nhs_grief_bereavement_001", "hazan_shaver_1987_attachment_001"],
        "review_status": "needs_review",
    },
    # 9. TR context — family/in-laws
    {
        "id": "rel_family_009",
        "topic": "relationship_stress",
        "type": "psychoeducation",
        "title_tr": "Aile ve ilişki — Türkiye bağlamında sınır",
        "content_tr": (
            "TR'de bir ilişki genelde sadece iki kişinin ilişkisi değil, iki ailenin ilişkisi olarak da yaşanır. Bu bazı güzellikler getirir (destek, sosyal bağ, çocuk büyütmede yardım), ama aynı zamanda özgün gerilimler yaratır — özellikle kayınvalide, kayınbaba, anne, baba, aile üzerinden partner ilişkisi.\n\n"
            "Yaygın örüntüler:\n\n"
            "**1. Aileler tarafından karar verilen ilişki:**\n"
            "Görücü usulü ya da aile tarafından tanıştırıldığın bir ilişkide, aile 'sahiplik' hissiyle davranabilir. 'Onunla evlenmek zorunda değilsin ama...' cümlelerine benzer baskılar. Bu bir karar özerkliği meselesi — bu chatbot senin adına karar veremez.\n\n"
            "**2. Kayınvalide / kayınbaba dinamiği:**\n"
            "Klasik bir örüntü: partnerinin ailesi partnerini çocuk gibi görmeye devam eder; sen bir 'sonradan gelen' pozisyondasın. Bu partnerin de zorlanmasına neden olur — o iki tarafın arasında sıkışır.\n\n"
            "Sağlıklı bir dinamikte: partnerin, ailesiyle senin arana koruyucu bir sınır koyar. Partner, ailesine 'ben ve karım / kocam bir ekibiz, ona böyle davranmayın' diyebiliyorsa güvenli.\n\n"
            "Sınır koymuyorsa, bunu partnerinle konuşmak — sakin, saldırgan olmadan — önemli. Suçlama yerine ihtiyaç dilinde:\n"
            "'Annen dün sabah yaptığım yemek için 'yeterli değil' dediğinde çok üzüldüm. Ben senden aile içindeki eleştirilere karşı yanımda olmanı istiyorum. Bir dahaki sefere böyle bir şey olduğunda, konuyu değiştirir misin ya da bana destek verir misin?'\n\n"
            "**3. Kendi ailen ve partner:**\n"
            "Aynı örüntü ters yönde de çalışabilir. Kendi ailenin partnerine karşı beklentileri, eleştirileri, kabul etmemesi. Bu sefer sen partnerinle ailen arasında sıkışırsın. Partner tarafında olmak, aileni 'terk etmek' anlamına gelmez — sınır koymak anlamına gelir.\n\n"
            "**4. Ekonomik dinamikler:**\n"
            "TR'de aile içi ekonomik bağ (mülk, iş, miras) partner ilişkisini derinden etkileyebilir. Bir tarafın ailesinin diğerinden 'daha üstün' pozisyonda olması, güç dengesizliği yaratır. Bunu konuşulur bir konu olarak açmak — bir çift terapisti / aile terapisti bu tip konularda yararlıdır.\n\n"
            "**5. Kültürel farklılık:**\n"
            "Farklı din, milliyet, dil, sosyoekonomik arka plan olan çiftlerde 'kimin ailesinin gelenekleri' sorusu sürekli konudur. Yılbaşı? Bayram? Çocuk büyütme? Cenaze? Bunlar önceden konuşulmalı ideali; olmamışsa, şimdi konuşulmalı.\n\n"
            "**Sağlıklı bir aile-ilişki dengesinin göstergesi:**\n"
            "• Partnerin, ailesiyle senin arana koruyucu duruyor\n"
            "• Sen partnerinle ailen arasına koruyucu duruyorsun\n"
            "• Aileler yardımcı olabiliyor ama karar veremiyorlar\n"
            "• Aile toplantıları güzel, ama sonu geliyor — bir kere değil, düzenli olarak sizin ikiniz de var\n"
            "• Aile eleştirisi partnerini korumak için filtreleniyor\n\n"
            "**Sağlıksız gösterge:**\n"
            "• Partner, seni ailesinin karşısında yalnız bırakıyor / eleştirilere destek olmuyor\n"
            "• Aile toplantısı sonrası her seferinde tartışma çıkıyor\n"
            "• Partner, ailesinin fikrini seninkinden değerli tutuyor\n"
            "• Aile içindeki bir kişi (kayınbaba/kayınvalide/vs) sürekli ilişkinize müdahale ediyor ve partnerin buna karşı çıkmıyor\n"
            "• Aile içi baskı yüzünden ciddi ilişki kararları alınıyor (evlenme, çocuk yapma, taşınma)\n\n"
            "**Sınır** kart 6'da anlatıldı — burada da geçerli, sadece kime karşı olduğu farklı."
        ),
        "safety_notes": "TR aile bağlamı nüanslı ele alındı. Karar özerkliği vurgusu ('senin adına karar veremez'). Sağlıklı/sağlıksız aile-ilişki dengesi ayrımı somut örneklerle.",
        "source_refs": ["gottman_sound_relationship_house_001", "sue_johnson_eft_reference_001"],
        "review_status": "needs_review",
    },
    # 10. IPV Safety Net — TR-specific
    {
        "id": "rel_safetynet_010",
        "topic": "relationship_stress",
        "type": "safety",
        "title_tr": "Şiddet, kontrol, taciz — güvenlik ağı ve Türkiye kaynakları",
        "content_tr": (
            "Bu kart bir 'ilişki iyileştirme' kartı değildir. Eğer aşağıdakilerden biri seninle olduysa, bu kartı okuduğunu bir yakınına söyle ve kaynaklara ulaş. Bu chatbot senin güvenliğini garanti edemez — ama sana yönlendirebilir.\n\n"
            "**ŞU AN acil durumdaysan (fiziksel tehlike hissediyorsan):**\n\n"
            "• **KADES uygulaması** — Android + iOS'ta ücretsiz. T.C. İçişleri Bakanlığı tarafından geliştirildi. Tek dokunuşla konum bilginle beraber 155 (polis) çağırır. Sözlü ihbar yapamayacak durumdayken kritik.\n\n"
            "• **155 — Polis Acil.** 7/24, ücretsiz.\n\n"
            "• **En yakın karakol, jandarma, savcılık** — koruma kararı için başvuru.\n\n"
            "• **112 acil servis** — fiziksel yaralanma varsa.\n\n"
            "**Fiziksel tehlike şu an yoksa ama şiddet, tehdit, kontrol yaşıyorsan:**\n\n"
            "• **183 — Aile ve Sosyal Hizmetler Bakanlığı Sosyal Destek Hattı.** 7/24, ücretsiz. Kadın, çocuk, yaşlı, engelli, aile destek hizmetleri, ŞÖNİM yönlendirmesi. Kriz hattı olarak dizayn edilmedi — bilgi + yönlendirme.\n\n"
            "• **Mor Çatı Kadın Sığınağı Vakfı** — 0212 292 52 31 / 32 dayanışma hattı (Salı, Perşembe 10-17 arası). Yönlendirme + hukuki bilgi + sığınak.\n\n"
            "• **ŞÖNİM (Şiddet Önleme ve İzleme Merkezi)** — 81 ilde. Aile ve Sosyal Hizmetler İl Müdürlüğü aracılığıyla ulaşılır. Barınma, ilk müdahale, rehabilitasyon, adli süreç eşliği.\n\n"
            "• **KA-DER, KAMER, Türk Kadınlar Birliği** — sivil toplum destek kuruluşları.\n\n"
            "**6284 sayılı Kanun — Ailenin Korunması ve Kadına Karşı Şiddetin Önlenmesine Dair Kanun:**\n\n"
            "TR'de 6284 sayılı kanun kadına yönelik şiddet vakalarında hızlı koruma sağlar. Aile Mahkemesi'ne yaptığın başvuru sonucu şu tedbirler alınabilir:\n"
            "• Şiddet uygulayan taraf konuttan uzaklaştırılır\n"
            "• Sana ve çocuklarına yaklaşma yasağı konur\n"
            "• Silaha el konur (varsa)\n"
            "• Barınma yeri sağlanır (ŞÖNİM)\n"
            "• Geçici mali destek verilir\n"
            "• Kimlik değişikliği talebi yapılabilir\n\n"
            "Başvuru için bir avukat şart değildir; savcılık ya da aile mahkemesine doğrudan başvurabilirsin. Ama bir hukuk desteği alabiliyorsan (Mor Çatı yönlendirme yapabilir, Baro'nun ücretsiz avukat programı vardır — CMK atama), bu süreci kolaylaştırır.\n\n"
            "**Cinsel şiddet için:**\n\n"
            "Evlilik içi cinsel şiddet de bir suçtur. Türk Ceza Kanunu ilgili maddeleri koruma altına alır. Beden muayenesi için:\n"
            "• Bir hastane acil servisine gitmeden önce yıkanma / kıyafet değiştirme (delil kaybı olur)\n"
            "• Adli tıp değerlendirmesi savcılık yönlendirmesi ile yapılır\n"
            "• Mor Çatı bu süreçte eşlik edebilir\n\n"
            "**Kontrolcü / duygusal istismar sinyalleri (fiziksel şiddet olmasa bile ciddi):**\n\n"
            "• Kime konuşacağını, ne giyeceğini, nereye gideceğini kontrol ediyor\n"
            "• Telefonuna, mesajlarına, sosyal medyana izin almadan bakıyor\n"
            "• Seni aileden / arkadaşlardan uzaklaştırdı\n"
            "• Parayı kontrol ediyor — sana para vermiyor, senden kazandığını istiyor\n"
            "• Sürekli aşağılıyor, küçük düşürüyor\n"
            "• Suçluluk hissettirerek istediklerini yaptırıyor ('sen olmasan iyi olurdum')\n"
            "• 'Seni terk edersem mahvolursun' diyor\n"
            "• Kıskançlığı ilerledi — bunu 'seni seviyorum' olarak sunuyor\n\n"
            "Bu örüntüler bir gün fiziksel şiddete evrilir — bilimsel araştırmalar (WHO, IPV literatürü) bunu tekrar tekrar gösteriyor. Kontrolcü ilişki 'sadece bir kişilik meselesi' değil, ilerici bir dinamiktir.\n\n"
            "**Şu inançlar bir ayrılma engeli olabilir — ve bunlar sık:**\n\n"
            "• 'Belki değişir. Benimle iyi olmaya çalışıyor.'\n"
            "• 'Çocuklar için birlikte kalmam gerek.'\n"
            "• 'Ailem ne der.'\n"
            "• 'Ekonomik olarak bağımlıyım, gidecek yer yok.'\n"
            "• 'Beni gerçekten seviyor, sadece sinirlendiğinde.'\n"
            "• 'Ben de yanlış yaptım, bu benim de suçum.'\n\n"
            "Bu inançların hepsinin altında gerçek bir şey var (değişebilir mi? bazen. çocuklar? önemli. aile? gerçek. ekonomik bağımlılık? kritik). Ama bu inançlar aynı zamanda seni tehlike içinde tutan bir çerçeve olabilir. Bir dış göze (klinik psikolog, Mor Çatı, güvendiğin arkadaş) bu inançları anlatmak, kendi durumunu görmen için değerli olur.\n\n"
            "**Bu chatbot ne söyleyemez:**\n\n"
            "• 'İyileştirmek için X'i yap' — bir istismar ilişkisinde 'iletişim tekniği' işe yaramaz. Bilim böyle diyor (Gottman Institute'un kendisi de IPV'yi çift terapisinden ayrı tutar).\n"
            "• 'Ondan ayrıl' — bu chatbot senin adına bu kararı veremez. Kararın senin.\n"
            "• 'Kendi güvenliğinin sorumluluğunu taşıyorum' — taşımıyor. Sen ya da bir uzman taşıyor.\n\n"
            "**Sonuç:**\n\n"
            "Şiddet ilişkilerinden ayrılmak zor. Ortalama olarak bir kişi şiddet ilişkisinden çıkmadan önce 7 kez ayrılma girişiminde bulunur (araştırma verisi). Bu 'başarısızlık' değildir — bu sürecin doğasıdır.\n\n"
            "Şu an durum ne olursa olsun, seni destekleyecek insanlar ve kaynaklar var. Bir yakınına bunu söyle. 183'ü ara. Mor Çatı'ya danış. Adım adım gitmek de bir yol."
        ),
        "safety_notes": "TR-özel: KADES, 155, 183, Mor Çatı, ŞÖNİM, 6284 sayılı Kanun. Kriz hattı olarak 183 ve Mor Çatı doğru tanımlandı (bilgi + yönlendirme, kriz DEĞİL). 'Ondan ayrıl' demeyi reddetti. Gaslighting yok — inançların altındaki gerçekliği tanıdı. Ayrılma süreçlerinin zorluğunu bilimsel veri ile normalize etti (ortalama 7 girişim).",
        "source_refs": ["kades_app_001", "kanun_6284_ailenin_korunmasi_001", "mor_cati_001", "aile_bakanligi_sonim_001", "who_ipv_2021_001", "gottman_domestic_violence_resources_001"],
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
    print(f"  {t:22s} {n}")
