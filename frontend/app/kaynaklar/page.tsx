import PageShell, { Block } from "@/components/PageShell";

export const metadata = {
  title: "Bilimsel kaynaklar",
  description:
    "Neva'nın içerikleri klinik rehberler, sistematik derlemeler ve alanın temel çalışmalarından derlenmiştir.",
};

const SOURCES = [
  {
    name: "NICE",
    full: "National Institute for Health and Care Excellence",
    note: "Birleşik Krallık'ın ulusal klinik rehberleri — kaygı bozuklukları, depresyon, uyku ve travma sonrası stres için tedavi standartları.",
  },
  {
    name: "APA",
    full: "American Psychological Association",
    note: "Depresyon ve travma sonrası stres bozukluğu için kanıta dayalı uygulama rehberleri.",
  },
  {
    name: "Cochrane",
    full: "Cochrane Library",
    note: "Bilişsel davranışçı terapinin etkililiğine dair sistematik derlemeler ve meta-analizler.",
  },
  {
    name: "CCI",
    full: "Centre for Clinical Interventions, Perth",
    note: "Kamuya açık, klinisyenler tarafından hazırlanmış kendine yardım modülleri.",
  },
  {
    name: "NHS",
    full: "National Health Service",
    note: "Hasta bilgilendirme materyalleri ve kendine yardım rehberleri.",
  },
  {
    name: "WHO",
    full: "Dünya Sağlık Örgütü",
    note: "Ruh sağlığı politika belgeleri, işyeri ruh sağlığı ve yas süreçlerine dair kılavuzlar.",
  },
];

export default function KaynaklarPage() {
  return (
    <PageShell
      title="Bilimsel kaynaklar"
      intro="Neva'nın verdiği cevaplar serbest üretim değil; belirli bir içerik havuzuna dayanıyor. O havuz da rastgele derlenmedi."
    >
      <Block heading="İçerik nasıl hazırlandı">
        <p>
          Neva&apos;nın bilgi tabanı, on bir konu başlığı altında toplanmış yüzlerce
          içerik parçasından oluşuyor. Her parça, aşağıdaki kurumların yayımladığı
          klinik rehberler, sistematik derlemeler, hakemli araştırmalar ve alanın
          temel kitaplarından sentezlendi.
        </p>
        <p>
          Her içerik parçası hangi kaynaklardan
          türetildiğini kayıt altında tutuyor; kaynağı olmayan içerik bilgi
          tabanına girmiyor.
        </p>
      </Block>

      <Block heading="Başlıca kurumlar">
        <div className="grid grid-cols-1 sm:grid-cols-2 gap-4 not-prose">
          {SOURCES.map((s) => (
            <div
              key={s.name}
              className="p-5 rounded-2xl bg-cbt-surface dark:bg-cbt-dark-surface border border-cbt-border/60 dark:border-cbt-dark-border/60"
            >
              <div className="text-[15px] font-semibold text-cbt-text dark:text-cbt-dark-text">
                {s.name}
              </div>
              <div className="text-[12px] text-cbt-textMuted dark:text-cbt-dark-textMuted mb-2">
                {s.full}
              </div>
              <p className="text-[13px] leading-relaxed">{s.note}</p>
            </div>
          ))}
        </div>
      </Block>

      <Block heading="Kuramsal temel">
        <p>
          İçerikler ağırlıklı olarak bilişsel davranışçı terapi geleneğine
          dayanıyor: panik için Clark&apos;ın bilişsel modeli, yaygın kaygı için
          Wells&apos;in üstbilişsel modeli, düşük özdeğer için Fennell&apos;in
          çerçevesi, uykusuzluk için Harvey&apos;in bilişsel modeli ve
          depresyonda davranışsal aktivasyon gibi alanda yerleşmiş yaklaşımlar.
        </p>
        <p>
          Kabul ve kararlılık terapisi ile farkındalık temelli yaklaşımlardan da
          yararlanıldı; yaşam değişimleri için Bridges ve Schlossberg
          çerçeveleri kullanıldı.
        </p>
      </Block>

      <Block heading="Sınırlar">
        <p>
          Kaynakların çoğu İngilizce literatürden geliyor ve Türkiye&apos;ye özgü
          kültürel bağlam için uyarlandı. Bu uyarlama bir çeviri işlemi değil,
          yeniden yazım süreciydi — ancak yine de her yöntemin her kültürel
          bağlamda aynı ölçüde işlediği varsayılmamalı.
        </p>
        <p>
          İçerikler eğitim ve kendine yardım amaçlıdır; klinik uygulama
          protokolü değildir.
        </p>
      </Block>
    </PageShell>
  );
}
