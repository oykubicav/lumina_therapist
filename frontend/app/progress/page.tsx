"use client";

import { useState, useEffect } from "react";
import Link from "next/link";
import { ArrowLeft, Plus } from "lucide-react";
import { getSessionId } from "@/lib/session";
import AssessmentTrend from "@/components/AssessmentTrend";
import AssessmentModal from "@/components/AssessmentModal";
import type { AssessmentKind } from "@/lib/types";


export default function ProgressPage() {
  const [sessionId, setSessionId] = useState<string | null>(null);
  const [activeKind, setActiveKind] = useState<AssessmentKind>("phq9");
  const [showModal, setShowModal] = useState(false);
  const [refreshKey, setRefreshKey] = useState(0);   // submit sonrası chart'ı yenile

  useEffect(() => {
    const sessionid = getSessionId();
        setSessionId(sessionid);
  }, []);

  // Session yoksa — chat başlatmadan progress'e gelinemiyor
  if (sessionId === null) {
    return (
      <div className="min-h-screen flex items-center justify-center p-6 bg-cbt-bg dark:bg-cbt-dark-bg">
        <div className="max-w-md text-center">
          <p className="text-cbt-textSecondary dark:text-cbt-dark-textSecondary mb-4">
            İlerlemeni görmek için önce sohbet başlatman gerek.
          </p>
          <Link
            href="/"
            className="inline-block px-6 py-3 rounded-xl bg-cbt-accent text-white font-medium"
          >
            Ana sayfaya dön
          </Link>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-cbt-bg dark:bg-cbt-dark-bg">
      {/* Header */}
      <header className="border-b border-cbt-border dark:border-cbt-dark-border">
        <div className="max-w-3xl mx-auto px-4 py-4 flex items-center justify-between">
          <Link
            href="/"
            className="flex items-center gap-2 text-cbt-textSecondary dark:text-cbt-dark-textSecondary hover:text-cbt-text"
          >
            <ArrowLeft size={18} />
            <span className="text-sm">Sohbete dön</span>
          </Link>
          <h1 className="text-lg font-medium text-cbt-text dark:text-cbt-dark-text">
            İlerlemem
          </h1>
          <button
            onClick={() => setShowModal(true)}
            className="flex items-center gap-1 text-sm text-cbt-accent hover:text-cbt-accent/80"
          >
            <Plus size={16} />
            Yeni ölçüm
          </button>
        </div>
      </header>

      {/* Kind selector tabs */}
      <div className="max-w-3xl mx-auto px-4 pt-6">
        <div className="flex gap-2 border-b border-cbt-border dark:border-cbt-dark-border">
          <TabButton
            active={activeKind === "phq9"}
            onClick={() => setActiveKind("phq9")}
            label="Depresyon (PHQ-9)"
          />
          <TabButton
            active={activeKind === "gad7"}
            onClick={() => setActiveKind("gad7")}
            label="Kaygı (GAD-7)"
          />
        </div>
      </div>

      {/* Chart body */}
      <main className="max-w-3xl mx-auto px-4 py-8">
        <div className="bg-white dark:bg-cbt-dark-surface rounded-2xl p-6 shadow-subtle">
          <AssessmentTrend
            key={`${activeKind}-${refreshKey}`}     /* refreshKey değişince chart yeniden yükler */
            sessionId={sessionId}
            kind={activeKind}
          />
        </div>

        {/* KVKK / açıklayıcı not */}
        <p className="mt-6 text-xs text-cbt-textMuted leading-relaxed text-center max-w-md mx-auto">
          Bu skorlar bir klinik tanı değildir — sadece zaman içindeki değişimi görmen için
          işaretlenmiş tarama ölçekleridir. Kendini kötü hissediyorsan, bir uzmanla
          görüşmek en iyi adım.
        </p>
      </main>

      {/* Assessment modal */}
      {showModal && (
        <AssessmentModal
          sessionId={sessionId}
          kind={activeKind}
          onClose={() => setShowModal(false)}
          onSubmit={(_r) => {
            setRefreshKey((k) => k + 1);
            // Modal'ı ManuAL kapatma — kullanıcı sonuç ekranını görsün
            // Kullanıcı "Tamam"a basınca onClose tetiklenir
          }}
        />
      )}
    </div>
  );
}


function TabButton({
  active,
  onClick,
  label,
}: {
  active: boolean;
  onClick: () => void;
  label: string;
}) {
  return (
    <button
      onClick={onClick}
      className={`px-4 py-2 text-sm border-b-2 transition-colors ${
        active
          ? "border-cbt-accent text-cbt-accent"
          : "border-transparent text-cbt-textMuted hover:text-cbt-text"
      }`}
    >
      {label}
    </button>
  );
}

