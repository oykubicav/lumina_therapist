"use client";

import { useState } from "react";

export default function CrisisConfirm({
  onConfirm,
  onDeny,
}: {
  onConfirm: () => Promise<void> | void;
  onDeny: () => Promise<void> | void;
}) {
  const [busy, setBusy] = useState(false);

  async function handle(action: () => Promise<void> | void) {
    setBusy(true);
    try {
      await action();
    } finally {
      setBusy(false);
    }
  }

  return (
    <div className="flex flex-wrap gap-2.5 pl-1">
      <button
        onClick={() => handle(onConfirm)}
        disabled={busy}
        className="h-10 px-5 rounded-full bg-cbt-text dark:bg-cbt-dark-text text-cbt-bg dark:text-cbt-dark-bg text-[14px] font-medium hover:opacity-85 transition-opacity disabled:opacity-40"
      >
        Evet, öyle
      </button>
      <button
        onClick={() => handle(onDeny)}
        disabled={busy}
        className="h-10 px-5 rounded-full bg-cbt-surface dark:bg-cbt-dark-surface border border-cbt-border dark:border-cbt-dark-border text-[14px] text-cbt-textSecondary dark:text-cbt-dark-textSecondary hover:text-cbt-text dark:hover:text-cbt-dark-text hover:border-cbt-borderStrong dark:hover:border-cbt-dark-borderStrong transition-colors disabled:opacity-40"
      >
        Hayır, öyle değil
      </button>
    </div>
  );
}
