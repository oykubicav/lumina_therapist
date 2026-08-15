"use client";

import { useState } from "react";
import {
  ChevronDown,
  ChevronRight,
  AlertOctagon,
  AlertTriangle,
  CheckCircle2,
} from "lucide-react";
import type { ChatResponse } from "@/lib/types";

const ROUTE_STYLE: Record<string, { bg: string; text: string; label: string }> = {
  cbt_support: {
    bg: "bg-cbt-accentSoft dark:bg-cbt-dark-accentSoft",
    text: "text-cbt-accent dark:text-cbt-dark-accent",
    label: "CBT",
  },
  scope_boundary: {
    bg: "bg-cbt-warningSoft dark:bg-cbt-dark-warningSoft",
    text: "text-cbt-warning dark:text-cbt-dark-warning",
    label: "Boundary",
  },
  conditional_cbt_after_safety_check: {
    bg: "bg-cbt-warningSoft dark:bg-cbt-dark-warningSoft",
    text: "text-cbt-warning dark:text-cbt-dark-warning",
    label: "Conditional",
  },
  crisis_referral: {
    bg: "bg-cbt-dangerSoft dark:bg-cbt-dark-dangerSoft",
    text: "text-cbt-danger dark:text-cbt-dark-danger",
    label: "Crisis",
  },
  medical_emergency_referral: {
    bg: "bg-cbt-dangerSoft dark:bg-cbt-dark-dangerSoft",
    text: "text-cbt-danger dark:text-cbt-dark-danger",
    label: "Medical",
  },
  professional_or_emergency_referral: {
    bg: "bg-cbt-warningSoft dark:bg-cbt-dark-warningSoft",
    text: "text-cbt-warning dark:text-cbt-dark-warning",
    label: "Professional",
  },
  medical_professional_referral: {
    bg: "bg-cbt-warningSoft dark:bg-cbt-dark-warningSoft",
    text: "text-cbt-warning dark:text-cbt-dark-warning",
    label: "Medication",
  },
  minor_referral: {
    bg: "bg-cbt-warningSoft dark:bg-cbt-dark-warningSoft",
    text: "text-cbt-warning dark:text-cbt-dark-warning",
    label: "Minor",
  },
  abuse_safety_referral: {
    bg: "bg-cbt-dangerSoft dark:bg-cbt-dark-dangerSoft",
    text: "text-cbt-danger dark:text-cbt-dark-danger",
    label: "Abuse",
  },
};

export default function DebugPanel({ turn }: { turn: ChatResponse }) {
  const [open, setOpen] = useState(false);
  const style = ROUTE_STYLE[turn.safety.route] || {
    bg: "bg-cbt-surfaceMuted dark:bg-cbt-dark-surfaceMuted",
    text: "text-cbt-textMuted dark:text-cbt-dark-textMuted",
    label: turn.safety.route,
  };

  return (
    <div className="mt-3 pt-3 border-t border-cbt-border/60 dark:border-cbt-dark-border/60">
      <button
        onClick={() => setOpen((v) => !v)}
        className="flex items-center gap-1 text-[11px] text-cbt-textMuted dark:text-cbt-dark-textMuted hover:text-cbt-text dark:hover:text-cbt-dark-text transition-colors"
      >
        {open ? (
          <ChevronDown size={12} strokeWidth={2.4} />
        ) : (
          <ChevronRight size={12} strokeWidth={2.4} />
        )}
        Sistem detayları
      </button>

      {open && (
        <div className="mt-2 space-y-2.5 text-[11px] animate-fade-in">
          <Row label="Route">
            <span
              className={`px-1.5 py-0.5 rounded ${style.bg} ${style.text} font-medium`}
            >
              {style.label}
            </span>
            <span className="text-cbt-textMuted dark:text-cbt-dark-textMuted ml-2">
              allow_cbt: {String(turn.safety.allow_cbt)} · risk:{" "}
              {turn.safety.highest_risk}
            </span>
          </Row>

          {turn.safety.matched_card_ids.length > 0 && (
            <Row label="Safety kartları">
              <code className="text-[10.5px] text-cbt-textSecondary dark:text-cbt-dark-textSecondary">
                {turn.safety.matched_card_ids.join(", ")}
              </code>
            </Row>
          )}

          <Row label="Intent">
            <code className="text-[10.5px] text-cbt-textSecondary dark:text-cbt-dark-textSecondary">
              {turn.intent.module} → {turn.intent.subintent}
            </code>
            <span className="text-cbt-textMuted dark:text-cbt-dark-textMuted ml-2">
              {(turn.intent.confidence * 100).toFixed(0)}%
            </span>
          </Row>

          <Row label="Kartlar">
            <code className="text-[10.5px] text-cbt-textSecondary dark:text-cbt-dark-textSecondary break-all">
              {turn.retrieved_card_ids.slice(0, 8).join(", ")}
              {turn.retrieved_card_ids.length > 8 ? " …" : ""}
            </code>
          </Row>

          <Row label="Critic">
            {turn.critic.passed ? (
              <span className="inline-flex items-center gap-1 text-cbt-accent dark:text-cbt-dark-accent">
                <CheckCircle2 size={11} strokeWidth={2.4} /> Geçti
              </span>
            ) : (
              <span className="inline-flex items-center gap-1 text-cbt-danger dark:text-cbt-dark-danger">
                <AlertOctagon size={11} strokeWidth={2.4} /> Kaldı
              </span>
            )}
            {turn.critic.rewrites > 0 && (
              <span className="text-cbt-textMuted dark:text-cbt-dark-textMuted ml-2">
                rewrite: {turn.critic.rewrites}
              </span>
            )}
            {turn.critic.used_fallback && (
              <span className="inline-flex items-center gap-1 text-cbt-warning dark:text-cbt-dark-warning ml-2">
                <AlertTriangle size={11} strokeWidth={2.4} /> fallback
              </span>
            )}
          </Row>

          {turn.critic.findings_summary &&
            turn.critic.findings_summary.length > 0 && (
              <details>
                <summary className="cursor-pointer text-cbt-textMuted dark:text-cbt-dark-textMuted hover:text-cbt-text dark:hover:text-cbt-dark-text">
                  Critic bulguları ({turn.critic.findings_summary.length})
                </summary>
                <ul className="mt-1.5 space-y-0.5 pl-4 list-disc text-cbt-textSecondary dark:text-cbt-dark-textSecondary">
                  {turn.critic.findings_summary.map((f, i) => (
                    <li key={i} className="text-[10.5px] font-mono">
                      {f}
                    </li>
                  ))}
                </ul>
              </details>
            )}

          <Row label="Süreler">
            <span className="text-cbt-textMuted dark:text-cbt-dark-textMuted font-mono text-[10.5px]">
              {Object.entries(turn.timing_ms)
                .map(([k, v]) => `${k}=${Math.round(v)}ms`)
                .join(" · ")}
            </span>
          </Row>
        </div>
      )}
    </div>
  );
}

function Row({
  label,
  children,
}: {
  label: string;
  children: React.ReactNode;
}) {
  return (
    <div className="flex items-baseline gap-2 flex-wrap">
      <span className="text-cbt-textMuted dark:text-cbt-dark-textMuted min-w-[85px]">
        {label}
      </span>
      <div className="flex-1">{children}</div>
    </div>
  );
}
