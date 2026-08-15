# Health Anxiety — Synthesized Product Notes

**Status:** draft, needs psychologist review
**Sources synthesized from:** nhs_health_anxiety_001, cntw_health_anxiety_001, hpft_health_anxiety_001
**Bucket:** B (synthesize only — never copy verbatim phrases into the chatbot)
**Language target:** TR (Turkish) for end-user content; EN for internal taxonomy

---

## 1. relevant_concepts

Sağlık kaygısı, kişinin bedenindeki olağan duyumları veya hafif belirtileri ciddi bir hastalığın işareti olarak yorumlama eğilimidir. Bu yorumlama yoğun kaygıya, kontrol davranışlarına ve günlük yaşamda işlev kaybına yol açabilir.

Çekirdek bilişsel mekanizma: beden duyumlarının tehlikeli olarak yanlış yorumlanması (catastrophic misinterpretation of bodily sensations).

CBT modelinde sağlık kaygısının kısır döngüsü:
- tetikleyici (haber, ağrı, yorgunluk, normal beden değişimi, stres)
- beden duyumu
- felaket yorum ("bu kanser olabilir")
- tehdit algısı → fizyolojik uyarılma (kalp hızlanması, terleme, tremor) → daha fazla beden duyumu
- başa çıkma davranışları: kontrol, güvence arayışı, internet arama, kaçınma
- bu davranışlar kısa vadede rahatlatır ama uzun vadede kaygıyı besler

Sürdürücü davranışlar (maintaining behaviors):
- beden kontrolü (lump/lump-checking, nabız sayma, sürekli yutkunma, ciltte iz arama)
- güvence arayışı (yakınlara, hekime tekrar tekrar sorma; tekrar tekrar test isteme)
- aşırı bilgi arama (Dr Google, semptom siteleri, forumlar)
- hastalık içeriğinden kaçınma (TV programları, makaleler, doktor randevuları)
- fiziksel aktiviteden kaçınma → kondisyon kaybı → daha fazla yorgunluk → kaygıya destek
- "hasta gibi" davranma (oturma, yatma, planları iptal etme)

Önemli ayrım: sağlık kaygısı, gerçek bir hastalığa sahip olma anlamına gelmez; aynı zamanda gerçekten hasta olan biri de sağlık kaygısı yaşayabilir. Hedef belirtileri yok etmek değil, belirtilere yönelik kaygıyı azaltmaktır.

---

## 2. product_insights_tr (chatbot için kullanım fırsatları)

a) **Psikoeğitim modülü:** Kullanıcıya sağlık kaygısının ne olduğunu, kısır döngüsünü ve neden kaygı azaltmanın hedef olduğunu (semptom yok etme değil) anlatan kısa metinler.

b) **Kendi kendine değerlendirme (self-screen):** Kullanıcıya "Bu davranışlardan hangileri sende var?" tarzı yumuşak bir liste sunulabilir (kontrol, güvence arama, internet arama, kaçınma). Tanı koyma değil, farkındalık.

c) **Davranış izleme (behavior tracking):**
- Günlük "kaç kez kontrol ettim", "kaç kez güvence aradım", "kaç dakika internet araştırması yaptım" gibi sayım.
- Kullanıcı bu sayıların zamanla nasıl değiştiğini grafikte görebilir.

d) **Düşünce kaydı (thought record) — sağlık kaygısı için uyarlanmış:**
- Tetikleyici beden duyumu
- Otomatik felaket düşünce
- Olasılık ve şiddet abartısı kontrolü
- Alternatif, daha gerçekçi açıklama (stres, normal değişim, geçmiş benzer durumlar)
- Yeni kaygı puanı

e) **5 dakikalık dikkat deneyi:** Kullanıcıya "beden duyumuna 5 dk odaklan, sonra başka bir şeye odaklan, ikisini karşılaştır" şeklinde içgörü egzersizi. Kanıtla gösterir ki dikkat semptomu büyütüyor.

f) **Güvence arayışını azaltma planı:** "Bu hafta hekime ekstra randevu almadan önce 48 saat bekle", "yakın çevreden hastalık sorusu sorma sayısını azalt", "yakınlarına 'bana güvence vermemelerini' söyle" gibi adımlar.

g) **Kontrol davranışını azaltma planı:** "Ne sıklıkta kontrol makul?" sorusunu hekim tavsiyesine bağlayarak (örn. aylık olağan öz-muayene) çerçevele. Aşırı dürtüsel kontrol yerine dikkat dağıtma araçları sun.

h) **Bilgi arama sınırı:** "Bugün semptom araması yapmama" denemesi. Google yerine alternatif aktivite önerileri.

i) **Kaçınma için kademeli maruz bırakma (graded exposure):** Kullanıcı kaçındığı içerikleri 0–10 skalasında sıralar; en kolay olandan başlayarak küçük adımlarla yaklaşır.

j) **Fiziksel aktiviteye dönüş:** Çok hafif başlayarak yürüyüş/aktivite programı; kondisyon kaybının nasıl semptom üretebileceği psikoeğitimi.

---

## 3. safety_boundaries_tr (chatbot ne söylememeli / nasıl davranmalı)

- Chatbot tanı koymaz. "Sende sağlık kaygısı var" demek yerine "Bu yaşadığın örüntü sağlık kaygısı dediğimiz şeyle uyumlu olabilir; bir uzmana danışman bunu daha net görmeni sağlar" gibi yumuşak bir dil kullanır.
- Chatbot tıbbi tavsiye vermez. "Şu semptom büyük ihtimalle bir şey değil" gibi tıbbi güvence cümleleri kurmaz — çünkü bu hem yanlış güvence olabilir hem de tam olarak kullanıcıyı sağlıksız döngüye sokan davranışı (reassurance) besler.
- Chatbot güvence arayışına güvence vererek yanıt vermez. Kullanıcı 10. kez "ama bu kanser olabilir mi?" sorduğunda, chatbot her seferinde rahatlatmak yerine örüntüyü adlandırır: "Bunu bugün üçüncü kez soruyorsun — bu sağlık kaygısının tipik bir döngüsü olabilir. Birlikte buna farklı yaklaşmayı dener misin?"
- Yeni veya değişen bedensel semptom varsa kullanıcı önce bir hekime yönlendirilir. CBT teknikleri hekim değerlendirmesi yerine geçmez.
- Acil durum kırmızı bayrakları açıkça belirtilir: yoğun göğüs ağrısı + nefes darlığı, bilinç değişikliği, ani şiddetli baş ağrısı, kanama, intihar düşüncesi → derhal acil servis / 112.
- İntihar düşüncesi, kendine zarar verme, çaresizlik dile getirilirse kriz hattına yönlendir. Türkiye için ALO 182, intihar önleme için 112 ve yetişkin ruh sağlığı acilleri belirtilebilir; üst-kaynak güncel olmalı.
- Chatbot kullanıcının yaşadığı bedensel belirtilerin "gerçek olmadığını", "kafanda" olduğunu söylemez. Belirtiler gerçektir; yorumlama yolu üzerinde çalışılır.
- Çocuk, gebe, kronik hastalığı olan, yeni teşhis almış kullanıcılarda chatbot daha temkinli olmalı ve uzman desteğine yönlendirmeli.
- Chatbot, OKB benzeri yoğun ritüellerde (saatlerce kontrol, işlev kaybı) klinik destek önermeli; sadece kendi kendine yardım modülüyle yetinmemeli.

---

## 4. possible_cards (10 önerilen kart — psikolog onayı bekliyor)

| # | id | topic | type | one-liner |
|---|----|-------|------|-----------|
| 1 | ha_psychoed_001 | health_anxiety | psychoeducation | Sağlık kaygısı nedir, hedef nedir |
| 2 | ha_cycle_002 | health_anxiety | psychoeducation | Sağlık kaygısının kısır döngüsü |
| 3 | ha_selfcheck_003 | health_anxiety | self_assessment | Davranış farkındalığı listesi |
| 4 | ha_reassurance_004 | health_anxiety | technique | Güvence arayışını azaltma adımları |
| 5 | ha_bodychecking_005 | health_anxiety | technique | Kontrol davranışını azaltma |
| 6 | ha_googlestop_006 | health_anxiety | technique | İnternet semptom aramasını azaltma |
| 7 | ha_attentionexp_007 | health_anxiety | exercise | 5 dakikalık dikkat deneyi |
| 8 | ha_thoughtrec_008 | health_anxiety | exercise | Sağlık kaygısı için düşünce kaydı |
| 9 | ha_avoidance_009 | health_anxiety | technique | Kademeli maruz bırakma |
| 10 | ha_safetynet_010 | health_anxiety | safety | Ne zaman uzmana/acile başvur |

---

## 5. do_not_copy_warning

Bu notlar üç NHS kaynağından (NHS, CNTW, HPFT/Brendan Hogan) sentezlenmiştir. Hiçbir cümle birebir kopyalanmamalıdır. Vaka örnekleri (örn. HPFT'deki "Mary" hikayesi) ürüne taşınmamalıdır. Klinik model (kısır döngü, sürdürücü davranışlar) ortak CBT literatürünün parçasıdır ve kendi sözcüklerimizle yeniden ifade edilebilir.

Lisans durumu: NHS Crown copyright (NHS sayfası); CNTW kılavuzu ücretli/sipariş bazlı; HPFT IAPT broşürü ücretsiz ama yazarı (Dr Brendan Hogan) belirtilmiş — yine ticari yeniden kullanım için açık değil. Bu nedenle hepsi Bucket B → yalnızca sentez.

İnceleme gerekenler:
- Türkçe terminoloji bir klinisyen tarafından kontrol edilmeli
- Kriz/acil yönlendirmeleri Türkiye bağlamında güncel mi?
- Tanı koyma sınırı her kartta uygulanmış mı?
- Güvence verme tuzağına düşmemiş miyiz?
