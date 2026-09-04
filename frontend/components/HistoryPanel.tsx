"use client";

import { useCallback, useEffect, useState } from "react";
import { X, MessageSquare, Trash2, Loader2 } from "lucide-react";
import { listMySessions, deleteMySession } from "@/lib/api";
import { formatRelativeTime } from "@/lib/time";
import type { SessionSummary } from "@/lib/types";

interface Props {
  open: boolean;
  onClose: () => void;
  activeSessionId: string;
  onSelect: (sessionId: string) => void;
}

export default function HistoryPanel({
  open,
  onClose,
  activeSessionId,
  onSelect,
}: Props) {
  const [sessions, setSessions] = useState<SessionSummary[]>([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [busyId, setBusyId] = useState<string | null>(null);

  const load = useCallback(async () => {
    setLoading(true);
    setError(null);
    try {
      const r = await listMySessions({ limit: 50 });
      setSessions(r.sessions);
    } catch {
      setError("Geçmiş yüklenemedi.");
    } finally {
      setLoading(false);
    }
  }, []);

  useEffect(() => {
    if (open) void load();
  }, [open, load]);

  useEffect(() => {
    if (!open) return;
    const onKey = (e: KeyboardEvent) => {
      if (e.key === "Escape") onClose();
    };
    window.addEventListener("keydown", onKey);
    return () => window.removeEventListener("keydown", onKey);
  }, [open, onClose]);

  const remove = async (id: string) => {
    setBusyId(id);
    try {
      await deleteMySession(id);
      setSessions((prev) => prev.filter((s) => s.session_id !== id));
    } catch {
      setError("Silinemedi.");
    } finally {
      setBusyId(null);
    }
  };

  if (!open) return null;

  return (
    <div className="fixed inset-0 z-40">
      <div
        className="absolute inset-0 bg-black/30 backdrop-blur-sm"
        onClick={onClose}
      />
      <aside className="absolute left-0 top-0 h-full w-[min(340px,85vw)] bg-cbt-bg dark:bg-cbt-dark-bg border-r border-cbt-border dark:border-cbt-dark-border flex flex-col shadow-xl animate-slide-in-left">
        <div className="flex items-center justify-between px-4 py-3 border-b border-cbt-border/60 dark:border-cbt-dark-border/60">
          <h2 className="text-[14px] font-semibold text-cbt-text dark:text-cbt-dark-text">
            Sohbetlerim
          </h2>
          <button
            onClick={onClose}
            aria-label="Kapat"
            className="text-cbt-textMuted hover:text-cbt-text dark:hover:text-cbt-dark-text transition-colors"
          >
            <X size={16} strokeWidth={2.2} />
          </button>
        </div>

        <div className="flex-1 overflow-y-auto px-2 py-2">
          {loading && (
            <div className="flex justify-center py-8">
              <Loader2 className="animate-spin text-cbt-textMuted" size={18} />
            </div>
          )}

          {error && (
            <p className="px-3 py-2 text-[13px] text-cbt-danger dark:text-cbt-dark-danger">
              {error}
            </p>
          )}

          {!loading && !error && sessions.length === 0 && (
            <p className="px-3 py-8 text-[13px] text-cbt-textMuted dark:text-cbt-dark-textMuted leading-relaxed">
              Henüz kayıtlı bir sohbetin yok. Konuşmaya başladığında burada
              görünecek.
            </p>
          )}

          {sessions.map((s) => {
            const active = s.session_id === activeSessionId;
            return (
              <div
                key={s.session_id}
                className={[
                  "group flex items-start gap-2 rounded-xl px-3 py-2.5 mb-1 cursor-pointer transition-colors",
                  active
                    ? "bg-cbt-surface dark:bg-cbt-dark-surface"
                    : "hover:bg-cbt-surface/60 dark:hover:bg-cbt-dark-surface/60",
                ].join(" ")}
                onClick={() => onSelect(s.session_id)}
              >
                <MessageSquare
                  size={14}
                  strokeWidth={2}
                  className="mt-0.5 shrink-0 text-cbt-textMuted dark:text-cbt-dark-textMuted"
                />
                <div className="min-w-0 flex-1">
                  <p className="text-[13px] text-cbt-text dark:text-cbt-dark-text leading-snug line-clamp-2">
                    {s.title}
                  </p>
                  <p className="text-[11px] text-cbt-textMuted dark:text-cbt-dark-textMuted mt-0.5">
                    {formatRelativeTime(new Date(s.last_active).getTime())} ·{" "}
                    {s.turn_count} mesaj
                  </p>
                </div>
                <button
                  onClick={(e) => {
                    e.stopPropagation();
                    void remove(s.session_id);
                  }}
                  disabled={busyId === s.session_id}
                  aria-label="Bu sohbeti sil"
                  className="opacity-0 group-hover:opacity-100 focus:opacity-100 text-cbt-textMuted hover:text-cbt-danger dark:hover:text-cbt-dark-danger transition-all shrink-0"
                >
                  <Trash2 size={13} strokeWidth={2.2} />
                </button>
              </div>
            );
          })}
        </div>

        <p className="px-4 py-3 border-t border-cbt-border/60 dark:border-cbt-dark-border/60 text-[11px] text-cbt-textMuted dark:text-cbt-dark-textMuted leading-relaxed">
          Sohbetlerin sen silene kadar hesabında saklanır.
        </p>
      </aside>
    </div>
  );
}