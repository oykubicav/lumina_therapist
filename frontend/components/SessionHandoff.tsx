"use client";

import { useState } from "react";
import { getSessionRecap } from "@/lib/api";
import { Loader2 } from "lucide-react";

export default function SessionHandoff({
  sessionId,
  onStartNew,
  onDismiss,
}: {
  sessionId: string;
  onStartNew: () => Promise<void> | void;
  onDismiss: () => void;
}) {
  const [recap, setRecap] = useState<string | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  async function wrapUp() {
    setLoading(true);
    setError("");
    try {
      const res = await getSessionRecap(sessionId);
      setRecap(res.recap);
    } catch {
      setError("Özet şu an oluşturulamadı, ama istediğin zaman devam edebilirsin.");
    } finally {
      setLoading(false);
    }
  }

  if (recap) {
    return (
      <div className="rounded-2xl bg-cbt-surface dark:bg-cbt-dark-surface border border-cbt-border/60 dark:border-cbt-dark-border/60 p-6">
        <div className="text-[13px] font-medium text-cbt-textMuted dark:text-cbt-dark-textMuted mb-3">
          Bugünkü konuşmadan
        </div>
        <p className="text-[15px] text-cbt-text dark:text-cbt-dark-text leading-[1.7] whitespace-pre-wrap mb-6">
          {recap}
        </p>
        <div className="flex flex-wrap gap-3">
          <button
            onClick={onStartNew}
            className="h-11 px-5 rounded-xl bg-cbt-text dark:bg-cbt-dark-text text-cbt-bg dark:text-cbt-dark-bg text-[14px] font-medium hover:opacity-85 transition-opacity"
          >
            Yeni bir konuşma başlat
          </button>
          <button
            onClick={onDismiss}
            className="h-11 px-5 rounded-xl text-[14px] text-cbt-textSecondary dark:text-cbt-dark-textSecondary hover:text-cbt-text dark:hover:text-cbt-dark-text transition-colors"
          >
            Buradan devam et
          </button>
        </div>
      </div>
    );
  }

  return (
    <div className="rounded-2xl bg-cbt-surface dark:bg-cbt-dark-surface border border-cbt-border/60 dark:border-cbt-dark-border/60 p-6">
      <div className="text-[15px] font-semibold text-cbt-text dark:text-cbt-dark-text mb-2">
        Bugünlük burada bırakalım mı?
      </div>
      <p className="text-[14px] text-cbt-textSecondary dark:text-cbt-dark-textSecondary leading-relaxed mb-5">
        Uzun bir konuşma oldu. İstersen bugün konuştuklarımızı toparlayayım —
        ya da devam edelim, sende kalsın karar.
      </p>

      {error && (
        <p className="text-[13px] text-cbt-danger dark:text-cbt-dark-danger mb-4">
          {error}
        </p>
      )}

      <div className="flex flex-wrap gap-3">
        <button
          onClick={wrapUp}
          disabled={loading}
          className="h-11 px-5 rounded-xl bg-cbt-text dark:bg-cbt-dark-text text-cbt-bg dark:text-cbt-dark-bg text-[14px] font-medium hover:opacity-85 transition-opacity disabled:opacity-40 inline-flex items-center gap-2"
        >
          {loading && <Loader2 size={15} className="animate-spin" />}
          {loading ? "Toparlanıyor…" : "Bugünlük yeter, toparla"}
        </button>
        <button
          onClick={onDismiss}
          className="h-11 px-5 rounded-xl text-[14px] text-cbt-textSecondary dark:text-cbt-dark-textSecondary hover:text-cbt-text dark:hover:text-cbt-dark-text transition-colors"
        >
          Devam etmek istiyorum
        </button>
      </div>
    </div>
  );
}
