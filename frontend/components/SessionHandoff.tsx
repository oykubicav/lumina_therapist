"use client";

import { useState } from "react";

export default function SessionHandoff({
  onStartNew,
}: {
  onStartNew: () => Promise<void> | void;
}) {
  const [busy, setBusy] = useState(false);

  async function handle() {
    setBusy(true);
    try {
      await onStartNew();
    } finally {
      setBusy(false);
    }
  }

  return (
    <div className="rounded-2xl bg-cbt-surface dark:bg-cbt-dark-surface border border-cbt-border/60 dark:border-cbt-dark-border/60 p-6">
      <div className="text-[15px] font-semibold text-cbt-text dark:text-cbt-dark-text mb-2">
        Bugünlük iyi bir yere geldik
      </div>
      <p className="text-[14px] text-cbt-textSecondary dark:text-cbt-dark-textSecondary leading-relaxed mb-5">
        Uzun bir konuşma oldu. İstersen burada bırakıp taze bir sayfada devam
        edebilirsin — konuştuklarımız hatırlanmaya devam eder. Dilersen bu
        sohbetten de devam edebilirsin, kapı kapalı değil.
      </p>
      <button
        onClick={handle}
        disabled={busy}
        className="h-11 px-6 rounded-xl bg-cbt-text dark:bg-cbt-dark-text text-cbt-bg dark:text-cbt-dark-bg text-[14px] font-medium hover:opacity-85 transition-opacity disabled:opacity-40"
      >
        {busy ? "Hazırlanıyor…" : "Yeni bir sayfa aç"}
      </button>
    </div>
  );
}
