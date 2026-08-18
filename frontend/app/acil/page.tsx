import PageShell, { Block } from "@/components/PageShell";

export const metadata = {
  title: "Acil durumlar",
  description: "Kriz anında başvurabileceğin destek hatları ve kaynaklar.",
};

const LINES = [
  {
    name: "112 Acil Çağrı Merkezi",
    detail: "Tıbbi aciliyet, güvenlik riski ve hayati tehlike durumları için.",
    availability: "7/24",
  },
  {
    name: "183 Sosyal Destek Hattı",
    detail:
      "Aile, Çalışma ve Sosyal Hizmetler Bakanlığı — şiddet, istismar ve psikososyal destek için.",
    availability: "7/24, ücretsiz",
  },
  {
    name: "155 Polis İmdat",
    detail: "Güvenliğin tehlikedeyse, şiddet ya da tehdit durumunda.",
    availability: "7/24",
  },
];

export default function AcilPage() {
  return (
    <PageShell
      title="Acil durumlar"
      intro="Neva kriz anları için tasarlanmadı. Şu an güvende değilsen ya da kendine zarar verme düşüncen varsa, aşağıdaki hatlara ulaş."
    >
      <div className="space-y-3 not-prose">
        {LINES.map((l) => (
          <div
            key={l.name}
            className="p-6 rounded-2xl bg-cbt-surface dark:bg-cbt-dark-surface border border-cbt-border/60 dark:border-cbt-dark-border/60"
          >
            <div className="text-[17px] font-semibold text-cbt-text dark:text-cbt-dark-text mb-1">
              {l.name}
            </div>
            <p className="text-[14px] text-cbt-textSecondary dark:text-cbt-dark-textSecondary leading-relaxed mb-2">
              {l.detail}
            </p>
            <div className="text-[12px] text-cbt-textMuted dark:text-cbt-dark-textMuted">
              {l.availability}
            </div>
          </div>
        ))}
      </div>

      <Block heading="Şu an zorlanıyorsan">
        <p>
          Yalnız kalmamaya çalış. Güvendiğin birine haber ver — yanında
          olmasını istemek zayıflık değil.
        </p>
        <p>
          Kendine zarar vermek için kullanabileceğin şeyleri uzaklaştır ya da
          başkasına teslim et. Karar vermeyi ertele; bu his kalıcı değil, ama
          şimdi verilen kararlar kalıcı olabiliyor.
        </p>
        <p>
          Bir acil servise başvurmak psikiyatrik destek için de geçerli bir
          yoldur. Hastanelerin acil servisleri ruh sağlığı krizlerinde de
          değerlendirme yapar.
        </p>
      </Block>

      <Block heading="Uzun vadeli destek">
        <p>
          Aile hekimin ilk adım için iyi bir başlangıç — seni uygun uzmana
          yönlendirebilir. Devlet hastanelerinin psikiyatri poliklinikleri ve
          toplum ruh sağlığı merkezleri ücretsiz hizmet verir.
        </p>
        <p>
          Üniversite öğrencisiysen, çoğu üniversitenin ücretsiz psikolojik
          danışmanlık birimi bulunuyor.
        </p>
        <p>
          Türk Psikologlar Derneği ve Türkiye Psikiyatri Derneği&apos;nin
          web siteleri üzerinden bölgendeki uzmanlara ulaşabilirsin.
        </p>
      </Block>
    </PageShell>
  );
}
