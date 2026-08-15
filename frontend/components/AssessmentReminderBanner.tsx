"use client";

import { useState } from "react";
import { X, TrendingUp } from "lucide-react";
import Link from "next/link";

interface Props {
  onDismiss: () => void;
}

export default function AssessmentReminderBanner({ onDismiss }: Props) {
  return (
    <div className="mx-4 mt-3 p-3 rounded-xl bg-cbt-accent/10 border border-cbt-accent/30 flex items-center gap-3">
      <TrendingUp className="text-cbt-accent shrink-0" size={16} />
      <p className="text-sm text-cbt-text dark:text-cbt-dark-text flex-1">
        Bu haftaki ölçümünü yaptın mı?
      </p>
      <Link
        href="/progress"
        className="text-sm text-cbt-accent font-medium hover:underline"
      >
        Şimdi yap
      </Link>
      <button
        onClick={onDismiss}
        className="text-cbt-textMuted hover:text-cbt-text"
        aria-label="Kapat"
      >
        <X size={16} />
      </button>
    </div>
  );
}