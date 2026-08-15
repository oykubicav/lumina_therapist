"use client";

import { useState } from "react";
import { ThumbsUp, ThumbsDown, Flag, Check, X } from "lucide-react";
import { postFeedback } from "@/lib/api";

type Verdict = "thumbs_up" | "thumbs_down" | "flag";

export default function FeedbackButtons({
  turnId,
  sessionId,
  onSent,
  sent,
}: {
  turnId: string;
  sessionId: string;
  onSent?: (v: Verdict) => void;
  sent?: Verdict;
}) {
  const [busy, setBusy] = useState<Verdict | null>(null);
  const [commentOpen, setCommentOpen] = useState(false);
  const [pendingVerdict, setPendingVerdict] = useState<Verdict | null>(null);
  const [comment, setComment] = useState("");

  async function send(verdict: Verdict, cmt?: string) {
    if (sent) return;
    setBusy(verdict);
    try {
      await postFeedback({
        turn_id: turnId,
        session_id: sessionId,
        verdict,
        comment: cmt,
      });
      onSent?.(verdict);
      setCommentOpen(false);
      setPendingVerdict(null);
      setComment("");
    } catch (err) {
      console.error("feedback error", err);
    } finally {
      setBusy(null);
    }
  }

  function openComment(v: Verdict) {
    setPendingVerdict(v);
    setCommentOpen(true);
  }

  if (sent) {
    return (
      <div className="mt-3 flex items-center gap-1.5 text-[11px] text-cbt-textMuted dark:text-cbt-dark-textMuted">
        <Check size={12} strokeWidth={2.4} />
        <span>Geri bildirim alındı</span>
      </div>
    );
  }

  return (
    <div className="mt-3 flex items-center gap-1">
      <IconChip
        label="Beğendim"
        onClick={() => send("thumbs_up")}
        disabled={!!busy}
        active={busy === "thumbs_up"}
      >
        <ThumbsUp size={13} strokeWidth={2.2} />
      </IconChip>
      <IconChip
        label="Beğenmedim"
        onClick={() => openComment("thumbs_down")}
        disabled={!!busy}
      >
        <ThumbsDown size={13} strokeWidth={2.2} />
      </IconChip>
      <IconChip
        label="Bayrakla (ciddi sorun)"
        onClick={() => openComment("flag")}
        disabled={!!busy}
      >
        <Flag size={13} strokeWidth={2.2} />
      </IconChip>

      {commentOpen && pendingVerdict && (
        <div className="ml-2 flex items-center gap-1.5 animate-fade-in">
          <input
            className="text-[12px] border border-cbt-border dark:border-cbt-dark-border rounded-md px-2.5 py-1.5 bg-cbt-surface dark:bg-cbt-dark-surface text-cbt-text dark:text-cbt-dark-text min-w-[220px] focus:outline-none focus:border-cbt-borderStrong dark:focus:border-cbt-dark-borderStrong placeholder:text-cbt-textMuted dark:placeholder:text-cbt-dark-textMuted"
            placeholder={
              pendingVerdict === "flag"
                ? "Ne yanlış gitti? (opsiyonel)"
                : "Neden? (opsiyonel)"
            }
            value={comment}
            onChange={(e) => setComment(e.target.value.slice(0, 500))}
            autoFocus
            onKeyDown={(e) => {
              if (e.key === "Enter") send(pendingVerdict, comment || undefined);
              if (e.key === "Escape") {
                setCommentOpen(false);
                setPendingVerdict(null);
                setComment("");
              }
            }}
          />
          <button
            className="flex items-center justify-center w-7 h-7 rounded-md bg-cbt-accent dark:bg-cbt-dark-accent text-white dark:text-cbt-dark-bg hover:bg-cbt-accentHover dark:hover:bg-cbt-dark-accentHover disabled:opacity-40 transition-all active:scale-95"
            onClick={() => send(pendingVerdict, comment || undefined)}
            disabled={!!busy}
            aria-label="Gönder"
          >
            <Check size={13} strokeWidth={2.4} />
          </button>
          <button
            className="flex items-center justify-center w-7 h-7 rounded-md text-cbt-textMuted dark:text-cbt-dark-textMuted hover:text-cbt-text dark:hover:text-cbt-dark-text hover:bg-cbt-surfaceMuted dark:hover:bg-cbt-dark-surfaceMuted transition-colors"
            onClick={() => {
              setCommentOpen(false);
              setPendingVerdict(null);
              setComment("");
            }}
            aria-label="İptal"
          >
            <X size={13} strokeWidth={2.4} />
          </button>
        </div>
      )}
    </div>
  );
}

function IconChip({
  children,
  label,
  onClick,
  disabled,
  active,
}: {
  children: React.ReactNode;
  label: string;
  onClick: () => void;
  disabled?: boolean;
  active?: boolean;
}) {
  const cls = [
    "flex items-center justify-center w-7 h-7 rounded-lg transition-all",
    active
      ? "bg-cbt-accentSoft dark:bg-cbt-dark-accentSoft text-cbt-accent dark:text-cbt-dark-accent"
      : "text-cbt-textMuted dark:text-cbt-dark-textMuted hover:text-cbt-text dark:hover:text-cbt-dark-text hover:bg-cbt-surfaceMuted dark:hover:bg-cbt-dark-surfaceMuted",
    disabled ? "opacity-40 cursor-not-allowed" : "active:scale-95",
  ].join(" ");
  return (
    <button
      className={cls}
      onClick={onClick}
      disabled={disabled}
      title={label}
      aria-label={label}
    >
      {children}
    </button>
  );
}
