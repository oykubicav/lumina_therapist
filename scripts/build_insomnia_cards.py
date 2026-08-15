
"""Append 10 insomnia CBT cards to cbt_cards.jsonl."""

import json
from pathlib import Path

OUT = Path("/Users/oykubicav/cbt_knowledge_base/cards/cbt_cards.jsonl")

cards = [

    # 1. Psychoeducation — what insomnia is
    {
        "id": "insom_psychoed_001",
        "topic": "insomnia",
        "type": "psychoeducation",
        "title_tr": "Uykusuzluk nedir, neden geçmiyor?",
        "content_tr": (
            "Uykusuzluk (insomnia) sadece 'bir gece uyuyamadım' değildir. Düzenli olarak şunlardan biri ya da birkaçı yaşanıyorsa uykusuzluktan söz ediyoruz:\n\n"
            "• Uykuya dalmakta zorlanmak\n"
            "• Gece defalarca uyanmak\n"
            "• Erken uyanıp bir daha uyuyamamak\n"
            "• Uyandığında hala yorgun hissetmek\n"
            "• Gündüz sürekli yorgunluk, sinirlilik, konsantrasyon güçlüğü\n\n"
            "İki tür var (NHS ayrımı):\n"
            "• Kısa süreli (akut) uykusuzluk: 3 aydan az. Genellikle stres, yeni bir olay, jet lag ya da geçici bir hastalıkla ilgilidir.\n"
            "• Uzun süreli (kronik) uykusuzluk: 3 ay ya da daha uzun. Sistem 'oturmuş' demektir — burada CBT tabanlı yaklaşımlar en etkili tedavi.\n\n"
            "Yetişkinler ortalama 7-9 saat uykuya ihtiyaç duyar ama bireysel değişir. Ne kadar uyuduğundan çok, gündüz nasıl hissettiğin daha iyi bir göstergedir.\n\n"
            "Önemli bir gerçek: uykusuzluk çoğu zaman *başlatan* şey (stres, hastalık, jet lag) çoktan geçmiş olsa bile kendi kendini besleyerek devam eder. Bu döngüyü kırmak için ne yapılabilir, sonraki kartlarda anlatacağız.\n\n"
            "Bu kart bir tanı koymaz. Belirtilerin haftalardır günlük yaşamını ciddi biçimde etkiliyorsa, ya da aşağıdakilerden biri varsa bir hekime başvurmak önemlidir:\n"
            "• Yüksek sesli horlama + nefes durmaları (uyku apnesi ihtimali)\n"
            "• Gündüz beklenmedik anda uykuya dalma (narkolepsi ihtimali)\n"
            "• Sabit intihar ya da kendine zarar düşünceleri\n"
            "• Yeni bir ilaç başladıktan sonra ortaya çıkan uykusuzluk"
        ),
        "safety_notes": "Tanı koymaz. Uyku apnesi, narkolepsi, mania, intihar düşüncesi için hekim/psikiyatri/112 köprüsü açık. NHS'in 3-ay süre ayrımı korundu.",
        "source_refs": ["nhs_insomnia_001", "cntw_sleep_001"],
        "review_status": "needs_review",
    },
    # 2. Cycle
    {
        "id": "insom_cycle_002",
        "topic": "insomnia",
        "type": "psychoeducation",
        "title_tr": "Uykusuzluğun kısır döngüsü",
        "content_tr": (
            "Uykusuzluğun ilginç yanı: onu başlatan şey (bir sınav stresi, bir hastalık, bir yolculuk) geçmiş olsa bile devam edebilir. Neden? Çünkü uykusuzluk kendi kendini besleyen bir döngü kurar. CBT'de bu döngü şöyle işler:\n\n"
            "1. Tetikleyici bir olay uykuyu bozar (birkaç gece).\n"
            "2. Kaygılanmaya başlarsın: 'Yine uyuyamayacak mıyım? Yarın iş yapamayacağım.'\n"
            "3. Yatağa girmek başlı başına stres kaynağı olur. Beden yatak = kaygı yeri bağlantısı kurar.\n"
            "4. Uyumaya *çalışırsın* — bu ters teper, çünkü uyku zorlamayla gelmez.\n"
            "5. Telafi davranışları başlar: erken yatağa girmek, geç kalkmak, gündüz kestirme, alkol, uyku hapı, saatlere sürekli bakmak.\n"
            "6. Bu davranışlar uyku basıncını (adenozin birikimi) bozar — yani vücudun 'gerçek uyku' ihtiyacı düşer.\n"
            "7. Bir sonraki gece daha zor uyunur → 2. adıma dön.\n\n"
            "Sonuç: başlatıcı stres gitmiş olsa bile döngü döner. Bu yüzden 'stres bitince uykusuzluk da geçer' cümlesi kronik uykusuzlukta çoğu zaman gerçek değildir.\n\n"
            "İyi haber şu: döngü kendi kendini besliyorsa, bir kez kırıldığında da hızla toparlanabilir. Sonraki kartlar bu döngünün üç noktasına vuracak:\n"
            "• Davranışsal: uyaran kontrolü + uyku kısıtlaması (kartlar 5 ve 6)\n"
            "• Kognitif: uyku katastrofizasyonu ile çalışma (kart 7)\n"
            "• Fizyolojik: rahatlama + yaşam tarzı (kartlar 8 ve 9)"
        ),
        "safety_notes": "Uykusuzluğu 'karakter zayıflığı' olarak çerçevelemedi. Alkol/uyku hapı 'telafi davranışı' olarak nötr tanıtıldı — cesaretlendirilmedi.",
        "source_refs": ["nhs_insomnia_001", "cochrane_cbt_i_001"],
        "review_status": "needs_review",
    },
    # 3. Self-check
    {
        "id": "insom_selfcheck_003",
        "topic": "insomnia",
        "type": "self_assessment",
        "title_tr": "Uyku sorunu için kendini kontrolü",
        "content_tr": (
            "Bu liste bir tanı koymaz; sadece son birkaç haftadaki uyku örüntüne ayna tutar. Sana uyan maddeleri sayıver:\n\n"
            "• Yatağa girdikten sonra uykuya dalmam 30 dakikadan uzun sürüyor\n"
            "• Gece 2 ya da daha fazla kez uyanıyorum\n"
            "• Erken uyanıp bir daha uyuyamıyorum\n"
            "• Sabah kalktığımda hala yorgun hissediyorum\n"
            "• Gündüz yorgunluk, sinirlilik, konsantrasyon güçlüğüm var\n"
            "• Yatağa girmek başlı başına kaygı yaratıyor\n"
            "• Saatlere sürekli bakıyorum, kaç saatim kaldı diye hesaplıyorum\n"
            "• Uyumak için alkol, uyku hapı ya da bitkisel çözüm kullanıyorum\n"
            "• Uyuyamayınca gündüz kestirme telafi ediyorum\n"
            "• Bu 3 aydan uzun sürüyor\n\n"
            "3-5 madde ve birkaç haftadır süregeliyorsa: bu modüldeki egzersizler işine yarayabilir.\n"
            "6+ madde, ya da 3+ ay ve günlük yaşamın belirgin biçimde aksıyorsa: bir hekime danışmak önemli — CBT-I'ı klinik gözetimde yapmak daha etkili olur.\n\n"
            "Şu üç madde varsa bu modül **yetmez**, mutlaka uzmana:\n"
            "• Partnerin senin için 'yüksek sesle horluyorsun, nefesin duruyor' diyor (uyku apnesi olabilir — kardiyovasküler risk taşır)\n"
            "• Gündüz beklenmedik anda uykuya dalıyorsun, direksiyonda tehlike (narkolepsi olabilir)\n"
            "• Sabit intihar/kendine zarar düşüncelerin var (bu bir uyku sorunu değil, kriz — hemen 112'yi ara)\n"
            "• Son zamanlarda alışılmadık biçimde enerjik, uykusuz ama yorgun değilsin, art arda büyük kararlar veriyorsun (mania belirtileri; psikiyatriye acilen)\n\n"
            "Reçeteli uyku ilacı (özellikle benzodiazepin) kullanıyorsan: ilacını kendi başına bırakma, dozunu değiştirme. Bunlar hekim gözetimi ister."
        ),
        "safety_notes": "Uyku apnesi, narkolepsi, mania, intihar için triaj net. TR bağlamında yaygın reçetesiz benzodiazepin kullanımı için uyarı. Tanı koymaz.",
        "source_refs": ["nhs_insomnia_001", "rcpsych_sleep_001"],
        "review_status": "needs_review",
    },
    # 4. Sleep hygiene
    {
        "id": "insom_hygiene_004",
        "topic": "insomnia",
        "type": "technique",
        "title_tr": "Uyku hijyeni — temel kurallar",
        "content_tr": (
            "Uyku hijyeni, uykuyu destekleyen çevre ve alışkanlıkların toplamıdır. Tek başına kronik uykusuzluğu çözmez ama zemin oluşturur — diğer teknikler bu zemin üzerinde çalışır. NHS'in do/don't listesi ile başlayalım:\n\n"
            "Yapılacaklar:\n"
            "• Yatağa sadece uykulu olduğunda gir. 'Vakti geldi' diye erken yatma.\n"
            "• Her gün aynı saatte uyan — hafta sonu bile. Vücudun sirkadiyen ritmi düzenlilik ile güçlenir.\n"
            "• Yatmadan en az 1 saat önce rahatlatıcı bir şeyler: sıcak duş, kitap, sakin müzik.\n"
            "• Yatak odası karanlık ve sessiz olsun. Perde, göz maskesi, kulak tıkacı — ihtiyaca göre.\n"
            "• Yatak odası sıcaklığı 18-20°C civarı ideal.\n"
            "• Gündüz düzenli egzersiz. 20-30 dakika yürüyüş yeter.\n"
            "• Rahat yatak, yastık ve örtü. Ucuz olmayabilir ama iyi bir yatırım.\n\n"
            "Yapılmayacaklar:\n"
            "• Yatmadan 6 saat önce sigara, alkol, çay, kahve. Kafeinin yarı ömrü 5-6 saat — 20:00'de kahve içersen gece 2'de yarı miktar hala kanda.\n"
            "• Geç gece büyük öğün. Sindirim uykuyu böler.\n"
            "• Yatmadan 4 saat önce yoğun egzersiz. Adrenalin yüksek kalır.\n"
            "• Yatmadan hemen önce ekran (telefon, TV, laptop). Mavi ışık uyanıklığı artırır. iPhone'da Night Shift, Android'de gece modu bir başlangıç ama en iyisi 30 dk önce ekranı kapatmak.\n"
            "• Gündüz kestirme. Uyku basıncını (adenozin) bozar.\n"
            "• Uykulu iken araç kullanma — hayati güvenlik.\n"
            "• Kötü bir geceden sonra 'telafi uykusu'. Düzenlilik daha önemli.\n\n"
            "Bir öneri: bir hafta boyunca sadece bir maddeyi seç ve deneyelim (mesela sabit uyanma saati). Her şeyi bir anda değiştirmek zor. Hangi maddenin sana en cazip geldiğini fark et."
        ),
        "safety_notes": "Her şeyi bir anda değiştirme baskısı yaratmaz. Kafein/alkol tarihi bilgiye dayalı. Kestirme yasağını nüanssız değil, uyku basıncı açıklamasıyla verdi.",
        "source_refs": ["nhs_insomnia_001", "oxford_sleep_001"],
        "review_status": "needs_review",
    },
    # 5. Stimulus control
    {
        "id": "insom_stimuluscontrol_005",
        "topic": "insomnia",
        "type": "technique",
        "title_tr": "Uyaran kontrolü — yatak = sadece uyku",
        "content_tr": (
            "Uyaran kontrolü (stimulus control), CBT-I'nın en kanıtlı tekniklerinden biri. Amacı basit: yatağın anlamını 'kaygı, düşünme, saat kontrolü' yerinden çıkarıp yeniden 'uyku' ile eşitlemek.\n\n"
            "Beynin öğrenme yoluyla iş yapar. Sen yıllardır yatakta uyanık kalıp saatlere bakıyor, düşünüyor, film izliyorsan, beynin 'yatak = uyanıklık' bağlantısını kurmuştur. Bu bağlantıyı sökmek zaman ister ama mümkün.\n\n"
            "Kurallar:\n\n"
            "1. Yatak SADECE uyku ve cinsellik için kullanılır. TV izlemek, telefonda scroll etmek, yemek yemek, çalışmak — yatak dışında.\n\n"
            "2. Yatağa sadece uykulu olduğunda gir. Uykulu değilsen okuma odasına git, sakin bir şey yap.\n\n"
            "3. **20 dakika kuralı**: yatağa girdin, 15-20 dakika içinde uyuyamadın. Yataktan KALK. Loş ışıklı başka bir odaya git. Sakin bir şey yap (kitap, dergi, sesli meditasyon). Uykulu olunca dön. Bu kez de uyuyamazsan tekrar kalk. Gece bunu 3 kez yapman gerekebilir — normal.\n\n"
            "4. Sabah SABIT saatte kalk. Dünkü uyku ne kadar kötü olursa olsun. Bu kural en zoru ama uyku basıncını korumak için kritik.\n\n"
            "5. Gündüz kestirmesiz (mümkünse). Uzun bir kestirme geceki uykuyu böler.\n\n"
            "Bu teknik başlangıçta yorgunluk artırır — genellikle 1-2 hafta zor. Sonraki 2-3 hafta içinde uyku belirgin biçimde toparlanır. Kanıt sağlamı: Cochrane meta-analizi ve onlarca RCT.\n\n"
            "Zorluk notu: 20 dakikada kalkma kuralı basit görünse de pratikte disiplin ister. 3'te uyandın, kalktın, kitap okudun, döndün, uyuyamadın — tekrar kalkmak zor gelebilir. Buna hazır ol.\n\n"
            "Ayrıca: ortak yatak odası (partner, çocuk, öğrenci evi) durumunda 'kalkıp başka odaya gitmek' pratikte zor olabilir. Bir sandalyeye oturup göz maskesiyle sakin nefes egzersizi de alternatiftir.\n\n"
            "Bu tekniği 4 hafta düzenli denemene rağmen belirgin bir değişim yoksa, klinik gözetim iyi olur — muhtemelen ek bir faktör var (uyku apnesi, ruh hali, ilaç)."
        ),
        "safety_notes": "20 dk kuralının zorluğu dürüstçe belirtildi. Ortak yatak odası bağlamı için pratik alternatif önerildi. 4 hafta sonra uzman köprüsü.",
        "source_refs": ["oxford_sleep_001", "cochrane_cbt_i_001"],
        "review_status": "needs_review",
    },
    # 6. Sleep restriction
    {
        "id": "insom_restriction_006",
        "topic": "insomnia",
        "type": "exercise",
        "title_tr": "Uyku kısıtlaması — CBT-I'nın en güçlü ve en zor tekniği",
        "content_tr": (
            "Uyku kısıtlaması (sleep restriction), CBT-I'nın en etkili tekniği ama başlangıçta en zor olanı. Mantığı ilk bakışta ters gelir: yatakta *daha az* zaman geçirerek uykuyu iyileştirmek.\n\n"
            "Neden işe yarar? Çünkü:\n"
            "• Uykuyu 'zorlamak' onu geciktirir. Yatakta 9 saat kalıp 5 saat uyumak, yatağı 'kaygı yeri' yapar.\n"
            "• Yatakta geçen sürenin gerçek uyku süresine yakın olması, uyku basıncını korur. Yorgun yatağa girersin, çabuk dalarsın.\n"
            "• Uyku 'yoğunlaşır': aynı 5 saatte daha derin ve yenileyici uyku olur.\n\n"
            "Adımlar:\n\n"
            "1. **Uyku günlüğü** tut, 1-2 hafta. Her gün: yatağa giriş saati, uykuya dalış tahminin, kaç kez uyandın, sabah kalkış saati, öznel yorgunluk (0-10).\n\n"
            "2. **Ortalama uyunan süreyi hesapla** (yatakta geçen değil, gerçekten uyunan). Diyelim 5.5 saat.\n\n"
            "3. Yatakta geçirilecek toplam süreyi bu miktara indir — ama **minimum 5 saat**. Yani örneğimizde 5.5 saat.\n\n"
            "4. Sabit bir sabah kalkma saati belirle — hangisi hayatına en uygunsa. Diyelim 06.30.\n\n"
            "5. Yatma saatini geriye ayarla: 06.30 - 5.30 saat = 01.00. Bu senin yeni yatma zamanın.\n\n"
            "6. Birkaç gün böyle git. Uyku verimliliği hesapla: (uyunan saat) / (yatakta geçen saat) × 100.\n"
            "   • Verimlilik ≥85% ise: yatma saatini 15 dakika ÖNE al (00.45'de yat). Bir hafta böyle.\n"
            "   • Verimlilik <85% ise: aynı programa devam et.\n"
            "   • Verimlilik >95% + hala yorgunsan: yatakta zamanı 15 dakika UZAT.\n\n"
            "7. Kademeli olarak yatakta geçen zaman doğal seviyeye yaklaşır.\n\n"
            "Uyarılar:\n"
            "• İlk 1-2 hafta yorgunluk artar. Gündüz araç kullanma dikkatli ol, ağır iş güvenliği önemli.\n"
            "• Gündüz kestirme YASAK — tekniğin özü bozulur.\n"
            "• Yatakta uyanık uzandığın anlarda uyaran kontrolü (kart 5) devrede: 20 dakika içinde uyumazsan kalk.\n"
            "• Bu teknik disiplin ister. En iyisi klinik gözetimde — bir uyku terapisti ya da klinik psikolog. Kendi başına da denenebilir ama düşük tempo tutmayı unutma.\n\n"
            "**Kimin denemesi UYGUN DEĞİL:**\n"
            "• Bipolar bozukluk (uyku kısıtlaması mania tetikleyebilir)\n"
            "• Epilepsi\n"
            "• Gebe kadınlar\n"
            "• Ağır operatör güvenliği gerektiren mesleklerde (kamyon şoförü, cerrah)\n"
            "• Aktif ciddi depresyon\n\n"
            "Bu durumlardan biri sende varsa lütfen önce hekimine danış."
        ),
        "safety_notes": "Bipolar/epilepsi/gebelik/güvenlik-kritik meslek için açık kontrendikasyon. Gündüz araç kullanımı uyarısı ilk hafta için. Klinik gözetim önerisi net.",
        "source_refs": ["oxford_sleep_001", "cochrane_cbt_i_001"],
        "review_status": "needs_review",
    },
    # 7. Cognitive restructuring
    {
        "id": "insom_thoughtrec_007",
        "topic": "insomnia",
        "type": "exercise",
        "title_tr": "Uyku katastrofizasyonu — yatakta dönen düşünceleri yeniden çerçevele",
        "content_tr": (
            "Uykusuzluğu sürdüren sadece davranışlar değil, düşüncelerdir. Yatakta uyanık uzandığında zihninden geçen tipik cümleler:\n\n"
            "• 'Yine uyuyamayacağım.'\n"
            "• 'Yarın işe yaramam.'\n"
            "• 'Bu böyle giderse hastalanacağım.'\n"
            "• 'Uyumam LAZIM.'\n"
            "• 'Herkes uyuyor, ben niye uyuyamıyorum.'\n"
            "• (Saate bakıp) 'Sadece 4 saatim kaldı, mahvoldum.'\n\n"
            "Bu düşünceler doğru gibi hissettirir ama iki sorunu var: (1) çoğu abartılı ya da kesin değil, (2) kaygı yaratıp uyanıklığı besliyorlar. Uyku 'başarma'yla gelmez, gevşemeyle gelir. Bu düşünceler tam tersini yapıyor.\n\n"
            "Egzersiz: bir gün içinde yatakta uyanık uzandığında akla gelen bir cümleyi yakala. Yarın gün ortasında yazılı olarak şu altı adımı geç:\n\n"
            "1. **Durum:** ne oldu? (örn. 'Gece 3'te uyandım, uyuyamadım.')\n\n"
            "2. **Otomatik düşünce:** aklımdan tam olarak ne geçti? (örn. 'Yine sabah bitkin olacağım, sunumu batıracağım.')\n\n"
            "3. **Bu düşünceye ne kadar inanıyorum?** (0-100)\n\n"
            "4. **Lehinde ve aleyhinde kanıt:**\n"
            "   • Lehinde: 'Az uyuduğum bazı günler zorlandım.'\n"
            "   • Aleyhinde: 'Az uyuduğum günlerin çoğunda idare edebildim; birkaç yıl önce en zor sunumumu 3 saat uykuyla verdim; kısa vadeli tek gün uykusuzluk yıkım değildir.'\n\n"
            "5. **Daha dengeli düşünce:** (örn. 'Yorgun olacağım, evet. Ama sunumu iptal etmem gerekmiyor; bugüne kadar bunu birkaç kez atlattım. Yorgunluk hayatın sonu değil.')\n\n"
            "6. **Yeni puan:** 0-100. Genelde 20-40 puan düşer.\n\n"
            "İnce bir püf noktası: saate bakma. Saat 3, saat 4, saat 5 — bunları bilmek uykuya yardım etmez, kaygıyı artırır. Yatak odasından saati çıkarabilir ya da yönünü değiştirebilirsin.\n\n"
            "Bir de: 'ideal uyku miktarı' takıntısını gevşet. 6-7 saat kaliteli uyku birçok insan için yeter. '8 saat uyumazsam olmaz' aksiyomu genellikle yanlıştır.\n\n"
            "Bu egzersizi 2-3 hafta düzenli yaptığında yatağa girdiğinde otomatik olarak devreye giren düşünceleri değil, hatırlatmak istediğin dengeli cümleleri fark etmeye başlarsın. Zihin buna esnek. Sadece pratik ister."
        ),
        "safety_notes": "Sahte pozitif düşünme reddedildi ('mahvoldum' yerine 'mükemmelim' değil, 'yorgun olacağım ama atlatırım'). Saate bakmama pratik önerisi.",
        "source_refs": ["oxford_sleep_001", "cochrane_cbt_i_001"],
        "review_status": "needs_review",
    },
    # 8. Relaxation
    {
        "id": "insom_relaxation_008",
        "topic": "insomnia",
        "type": "technique",
        "title_tr": "Rahatlama — beden uyarılmışsa uyku gelmez",
        "content_tr": (
            "Uykusuzluğun bir katmanı zihinsel (düşünceler), bir katmanı fizyolojik (bedenin uyarılmış olması — yüksek nabız, gergin kaslar, hızlı nefes). Fizyolojik katmanı gevşetmenin iki basit yöntemi var. İkisi de yatmadan ~1 saat önce yapılırsa daha etkili (hemen yatarken çok geç kalabilir).\n\n"
            "**1. Aşamalı kas gevşetme (progressive muscle relaxation)**\n\n"
            "Rahat pozisyonda otur ya da uzan. Gözlerini kapat. Kas gruplarını sırayla gererek gevşeteceksin:\n\n"
            "• Sağ el ve kol: 5 saniye ger (yumruk sık) → 10 saniye bırak. Bırakırken 'bırakıyorum' cümlesini içinden söyle.\n"
            "• Sol el ve kol: aynı.\n"
            "• Yüz: gözlerini sık, alnını kırıştır → bırak.\n"
            "• Boyun ve omuzlar: omuzlarını yukarı kaldır → bırak.\n"
            "• Karın: kasla → bırak.\n"
            "• Sağ bacak ve ayak: parmakları büz → bırak.\n"
            "• Sol bacak ve ayak: aynı.\n\n"
            "Toplam 10-15 dakika. Her kas grubunda gerginlik ve bırakma arasındaki farkı hisset — asıl amaç bu farkı öğretmektir.\n\n"
            "Bu tekniği fizyoterapi ya da sağlık uygulamalarında ücretsiz rehber ses kayıtları var (aramalar: 'progressive muscle relaxation Türkçe', 'PMR guided').\n\n"
            "**2. Diyafram nefesi (yavaş nefes)**\n\n"
            "Sırt üstü uzan. Bir el göğsüne, bir el karnına koy.\n"
            "• Burnundan 4 saniyede içeri nefes al. Karnındaki elin YÜKSELDİĞİNİ hissetmelisin (göğüs değil).\n"
            "• 2 saniye tut.\n"
            "• Ağzından 6-8 saniyede yavaşça dışarı ver — 'huuh' sesi çıkarabilirsin.\n"
            "• 5-10 dakika tekrarla.\n\n"
            "Uzun nefes verme parasempatik sinir sistemini aktive eder — vücut 'güvendeyim, dinlenebilirim' moduna geçer.\n\n"
            "**Uyarı ve öneriler:**\n\n"
            "• Aşırı hızlı nefes alma (hiperventilasyon) baş dönmesi yapabilir — yavaş git.\n"
            "• KOAH, ağır astım, gebelik gibi durumlarda diyafram nefesi için hekimine sor.\n"
            "• Bu teknikleri yatakta değil, yatmadan 1 saat önce oturur ya da yarı yatar pozisyonda yaparsan daha etkili. Yatağa girmeden önce gevşemiş olarak yatarsın.\n"
            "• İlk denemede işe yaramazsa şaşırma. Beden uyarılmışlığı bir seansta gitmez; birkaç haftalık düzenli pratikle etkisi artar.\n\n"
            "Rahatlama uykuyu 'garanti' etmez — ama uyarılmışlığı düşürür, zemin oluşturur. Diğer CBT-I teknikleriyle (uyaran kontrolü, uyku kısıtlaması) kombinasyonda etkilidir."
        ),
        "safety_notes": "Hiperventilasyon uyarısı verildi. KOAH/astım/gebelik için hekim onayı. Tek başına yeterli sunulmadı — kombinasyon vurgusu.",
        "source_refs": ["oxford_sleep_001", "cntw_sleep_001"],
        "review_status": "needs_review",
    },
    # 9. Lifestyle
    {
        "id": "insom_lifestyle_009",
        "topic": "insomnia",
        "type": "technique",
        "title_tr": "Yaşam tarzı zemini — kafein, alkol, ekran, ışık",
        "content_tr": (
            "CBT-I teknikleri sıkı takip edilse bile bazı yaşam tarzı faktörleri uykuyu sabote edebilir. Bunlar 'sihirli' değil ama zemin oluşturur.\n\n"
            "**Kafein**\n"
            "Kafeinin yarı ömrü 5-6 saat. 20:00'de içilen bir kahve, gece 2'de yarı miktarda hala kanında dolaşıyor demektir. Öneri: **15:00'ten sonra kafein YOK**. Kola, siyah çay, yeşil çay, kahve, enerji içeceği — hepsi sayılır. Bitki çayları (papatya, ıhlamur) kafeinsizdir, akşamları güvenli.\n\n"
            "**Alkol**\n"
            "Alkol kısa vadede seni uykuya götürür — evet. Ama uyku kalitesini bozar. REM (rüya) fazını baskılar, gece uyandırır, sabah tazelenmiş uyanmayı engeller. 'Uykuya dalmak için bir kadeh' pratik olarak seni daha yorgun bırakır. Öneri: **yatmadan 4-6 saat önce alkol yok**. Genel olarak alkolü uyku aracı olarak kullanmayı bırakmak, kronik uykusuzluk için önemli bir adım.\n\n"
            "**Nikotin**\n"
            "Sigara stimulanttır. Yatmadan 2 saat önce içmeyi kesmek yardımcı olur. Sigarayı bırakmak süreç açısından daha büyük bir kazanım.\n\n"
            "**Ekran ve mavi ışık**\n"
            "Telefon, tablet, TV — mavi ışık salınımı melatonin (uyku hormonu) salınımını geciktirir. Yatmadan 30 dakika – 1 saat önce ekran kapatmak ideal. Eğer bu mümkün değilse: iPhone'da 'Gece Vardiyası' (Night Shift), Android'de 'Gece Modu', laptop'ta f.lux gibi mavi ışık filtresi. Mükemmel değil ama fark eder.\n\n"
            "**Egzersiz**\n"
            "Günlük 20-30 dakika hafif-orta yoğunlukta hareket → uyku kalitesini iyileştirir. Ama yatmadan **4 saat önce** yoğun egzersizi bitir — sonrasında vücut ısısı ve adrenalin yüksek kalır, uyanıklık verir. Sabah ya da öğleden sonra egzersiz en iyisi.\n\n"
            "**Gün ışığı — sirkadiyen ritim için**\n"
            "Bu genellikle atlanır ama önemli. Sabah 15-20 dakika **doğal gün ışığı** al (pencere önü değil, dışarıda ideal — camdan geçen ışık yeterince güçlü değil). Bu, iç saatinin 'gündüz' sinyalini alır, akşamları melatonin salınımı zamanında olur.\n\n"
            "**Sıcaklık**\n"
            "Yatak odası sıcaklığı 18-20°C civarı ideal. Sıcak yatak odası uykuyu böler. Yatmadan önce sıcak duş çelişkili görünebilir ama işe yarar: duş sonrası vücut soğur → uyku sinyali.\n\n"
            "**Öğle uykusu / kestirme**\n"
            "Şu genel kural: kronik uykusuzlukla mücadelede ideal 'kestirme yok'. Ama Türkiye kültüründe siesta yaygın; ilk hafta bunu sıfırlamak zor olabilir. Kısa bir orta yol: gerekirse öğleden önce 15-20 dk 'power nap' (asla 30 dakikadan uzun değil, öğleden sonra değil).\n\n"
            "Bu maddelerin hepsini bir anda değiştirmek imkansız. Bir hafta bir maddeyi hedef seç — mesela kafein zamanını 15:00'e çek — ve dene."
        ),
        "safety_notes": "Alkol uykuya araç olarak kullanımını 'bırak' değil 'sorgula' tonu. Sigara bırakma daha büyük iş olarak nötr çerçevelendi. Kültürel (siesta) uyum önerildi. Aşamalı değişim vurgusu.",
        "source_refs": ["nhs_insomnia_001", "oxford_sleep_001"],
        "review_status": "needs_review",
    },
    # 10. Safety net
    {
        "id": "insom_safetynet_010",
        "topic": "insomnia",
        "type": "safety",
        "title_tr": "Ne zaman acile, ne zaman uzmana — uyku modülü için",
        "content_tr": (
            "Bu kart önemli — özellikle uykusuzluk 3 aydır sürüyorsa ya da aşağıdaki durumların biri sana uyuyorsa lütfen okumayı atlama.\n\n"
            "Derhal 112 veya en yakın acil servis:\n"
            "• Şu anda kendine zarar verme ya da yaşamına son verme düşünceleri ya da dürtüsü\n"
            "• Uyumadığın halde aşırı enerjik ve tükenmemişsin, art arda büyük kararlar veriyorsun (mania belirtileri; psikiyatrik acildir)\n"
            "• Gerçeklikten kopma, halüsinasyonlar, hızla kötüleşen ruhsal durum\n\n"
            "Ruh sağlığı uzmanı (psikiyatri hekimi / klinik psikolog) ya da aile hekimine başvurman önemli olan durumlar:\n"
            "• Uykusuzluk 3 ay ya da daha uzun süredir devam ediyor\n"
            "• Bu modüldeki egzersizleri (uyku hijyeni + uyaran kontrolü + rahatlama) 4-6 hafta düzenli denedin, anlamlı bir değişim yok\n"
            "• Uykusuzluğa depresyon, kaygı ya da başka bir ruh sağlığı problemi eşlik ediyor\n"
            "• Yatağa girmek başlı başına belirgin bir kaygı yaratıyor\n"
            "• Postpartum dönemdeysen (doğum sonrası uyku bozukluğu depresyon riskini artırır)\n"
            "• Reçeteli uyku ilacı (özellikle benzodiazepin) uzun süredir kullanıyorsun — bırakma kendi başına tehlikelidir, kademeli plan gerek\n\n"
            "Uyku bozuklukları merkezi (üniversite hastanesi uyku laboratuvarı) gerektiren durumlar:\n"
            "• Partnerin senin için 'yüksek sesle horluyorsun, nefes tıkanmaları var' diyor → uyku apnesi olabilir. Bu ciddi bir durumdur: uzun vadede kardiyovasküler risk (kalp krizi, inme) getirir. Uyku çalışması (polisomnografi) tanı koyar; CPAP cihazı standart tedavidir.\n"
            "• Gündüz beklenmedik anda uykuya dalıyorsun (özellikle direksiyonda tehlikeli) → narkolepsi olabilir\n"
            "• Uykuda anormal davranış (uyurgezerlik, gece terörleri, uykuda konuşma) → parasomnia\n"
            "• Bacaklarda yatmadan önce huzursuzluk hissi → huzursuz bacak sendromu (restless legs) — nöroloji ya da uyku bozuklukları uzmanı\n\n"
            "Endokrin değerlendirme gerektiren durumlar:\n"
            "• Kilo değişimi, aşırı terleme, çarpıntı → hipertiroidi kontrol\n"
            "• Menopoz döneminde uyku bozukluğu → jinekoloji + kadın hastalıkları\n\n"
            "İlaç uyarısı (kritik):\n"
            "• Reçeteli uyku ilacı ya da benzodiazepin (Xanax, Rivotril, Diazem gibi) kullanıyorsan: **kendi başına bırakma, dozunu değiştirme, başka ilaçla birleştirme**. Bu ilaçların ani bırakılması ciddi (bazen hayatı tehdit eden) yoksunluk sendromu yaratabilir. Reçeteyi yazan hekiminle konuş; kademeli azaltma planı gerek.\n"
            "• Türkiye'de reçetesiz benzodiazepin kullanımı yaygın — bu chatbot bunu asla desteklemez. Uyku hapı satın alıp kullanma çözüm değil; bağımlılık ve tolerans hızlı gelişir.\n"
            "• Bitkisel ürünler (valerian, melatonin) 1-2 hafta güvenlik açısından görece iyi ama iyileştirici değil, hekim gözetimi olmadan uzun süreli kullanılmamalı.\n\n"
            "Türkiye'de profesyonel destek için: aile hekimine başvurarak uygun yönlendirmeyi alabilirsin (psikiyatri, klinik psikolog, uyku laboratuvarı, endokrin, nöroloji — soruna göre). Doğrudan da randevu alabilirsin (devlet hastanesi, üniversite hastanesi, özel klinik). Kriz ya da tıbbi acilde 112'yi ara ya da en yakın acil servise git.\n\n"
            "Bu chatbot tıbbi/ruh sağlığı tanı koymaz ve uzman değerlendirmesinin ya da tedavinin yerine geçmez."
        ),
        "safety_notes": "İntihar + mania + psikoz üçlüsü en üstte, 112 net. Uyku apnesi kardiyovasküler risk vurgulandı — ihmal edilmemesi kritik. TR bağlamında reçetesiz benzodiazepin uyarısı özellikle güçlü. Postpartum, endokrin, parasomnia için ayrı uzmanlık alanı yönlendirmesi. Bitkisel ürünler için nötr çerçeve.",
        "source_refs": ["nhs_insomnia_001", "rcpsych_sleep_001", "who_mhgap_001"],
        "review_status": "needs_review",
    },
]

# Append to jsonl
with open(OUT, "a", encoding="utf-8") as f:
    for c in cards:
        f.write(json.dumps(c, ensure_ascii=False) + "\n")

# Verify
with open(OUT, encoding="utf-8") as f:
    all_cards = [json.loads(ln) for ln in f]

print(f"Total cards now: {len(all_cards)}")
print(f"By topic:")
from collections import Counter
for topic, n in sorted(Counter(c["topic"] for c in all_cards).items()):
    print(f"  {topic:20s} {n}")

print(f"\nNew insomnia cards added:")
for c in cards:
    print(f"  {c['id']:32s} {c['type']:16s} {c['title_tr']}")
