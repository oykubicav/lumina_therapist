"use client";

import { setOptIn, markDecided, type AssessFrequency } from "@/lib/assessments";
import { X, TrendingUp } from "lucide-react";

interface Props {
  onDismiss: () => void;
}

export default function AssessmentOptInModal({ onDismiss }: Props) {
  const handleChoose = (freq: AssessFrequency) => {
    setOptIn(freq);
    markDecided();
    onDismiss();
  };

  return (
    <div className="fixed inset-0 z-40 flex items-center justify-center bg-black/50 p-4">
      <div className="w-full max-w-md rounded-2xl bg-white dark:bg-cbt-dark-surface p-6 shadow-xl">
        <div className="flex items-center gap-3 mb-4">
          <div className="w-10 h-10 rounded-full bg-cbt-accent/10 flex items-center justify-center">
            <TrendingUp className="text-cbt-accent" size={20} />
          </div>
          <div>
            <h2 className="text-base font-medium text-cbt-text dark:text-cbt-dark-text">
              İlerlemeni takip edelim mi?
            </h2>
            <p className="text-xs text-cbt-textMuted">Opsiyonel — istediğin zaman değiştirebilirsin.</p>
          </div>
        </div>

        <p className="text-sm text-cbt-textSecondary dark:text-cbt-dark-textSecondary mb-4 leading-relaxed">
          Her 2 haftada bir kısa (2-3 dk) bir anketle depresyon ve kaygı seviyeni
          ölçebiliriz. Zaman içindeki değişimini görmek, ilerlediğini fark
          etmenin en somut yolu.
        </p>

        <p className="text-xs text-cbt-textMuted mb-6 leading-relaxed">
          Kanıta dayalı ölçekler (PHQ-9, GAD-7) — klinik pratikte kullanılan aynı sorular.
          Verilerini sadece sen görürsün, istediğinde silinir.
        </p>

        <div className="space-y-2">
          <button
            onClick={() => handleChoose("biweekly")}
            className="w-full py-3 rounded-xl bg-cbt-accent text-white font-medium"
          >
            Evet — 2 haftada bir hatırlat
          </button>
          <button
            onClick={() => handleChoose("weekly")}
            className="w-full py-3 rounded-xl border border-cbt-border text-cbt-text dark:text-cbt-dark-text"
          >
            Haftalık istiyorum
          </button>
          <button
            onClick={() => handleChoose("off")}
            className="w-full py-2 text-sm text-cbt-textMuted hover:text-cbt-text"
          >
            Şimdilik hayır
          </button>
        </div>

        <button
          onClick={onDismiss}
          className="absolute top-4 right-4 text-cbt-textMuted"
          aria-label="Kapat"
        >
          <X size={18} />
        </button>
      </div>
    </div>
  );
}