"use client";

const PROMPTS = [
  "Kaygım yükseldi, sakinleşmek istiyorum",
  "Bugün moralim çok bozuk",
  "İş yükümden bunaldım, tükenmiş hissediyorum",
  "Kendimi sürekli eleştiriyorum",
  "Panik atak geçirdim, ne yapabilirim?",
  "Uykuya dalamıyorum, zihnim susmuyor",
  "Kendimi yalnız hissediyorum",
  "Partnerimle sürekli tartışıyoruz",
  "Sevdiğim birini kaybettim",
  "Hayatımda büyük bir değişim var, zorlanıyorum",
  "Zor bir olay yaşadım, etkisinden çıkamıyorum",
];

export default function SuggestedPrompts({
  onPick,
}: {
  onPick: (prompt: string) => void;
}) {
  return (
    <div className="animate-fade-in">
      <p className="text-[13px] text-cbt-textMuted dark:text-cbt-dark-textMuted mb-3 pl-1">
        İstersen şunlardan biriyle başlayabilirsin
      </p>
      <div className="flex flex-wrap gap-2">
        {PROMPTS.map((label, i) => (
          <button
            key={i}
            onClick={() => onPick(label)}
            className="inline-flex items-center px-3.5 py-2 rounded-full bg-cbt-surface dark:bg-cbt-dark-surface border border-cbt-border/60 dark:border-cbt-dark-border/60 text-[13px] text-cbt-textSecondary dark:text-cbt-dark-textSecondary hover:text-cbt-text dark:hover:text-cbt-dark-text hover:border-cbt-borderStrong dark:hover:border-cbt-dark-borderStrong transition-all active:scale-[0.98] animate-slide-up"
            style={{ animationDelay: `${i * 50}ms`, animationFillMode: "backwards" }}
          >
            {label}
          </button>
        ))}
      </div>
    </div>
  );
}
