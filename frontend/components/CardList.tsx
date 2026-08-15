"use client";

import { useEffect, useState } from "react";
import { ArrowLeft, Search, X } from "lucide-react";
import { getTopics, listCards, getCard } from "@/lib/api";
import type { CBTCardSummary, CBTCardOut, TopicInfo } from "@/lib/types";
import ThemeToggle from "./ThemeToggle";

const TYPE_LABELS: Record<string, string> = {
  psychoeducation: "Bilgi",
  self_assessment: "Kontrol",
  exercise: "Egzersiz",
  technique: "Teknik",
  in_attack: "Anlık",
  safety: "Güvenlik",
};

export default function CardList() {
  const [topics, setTopics] = useState<TopicInfo[]>([]);
  const [selectedTopic, setSelectedTopic] = useState<string>("");
  const [q, setQ] = useState("");
  const [cards, setCards] = useState<CBTCardSummary[]>([]);
  const [total, setTotal] = useState(0);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [openCard, setOpenCard] = useState<CBTCardOut | null>(null);
  const [openLoading, setOpenLoading] = useState(false);

  useEffect(() => {
    getTopics()
      .then((r) => setTopics(r.topics))
      .catch((e) => setError(e.message));
  }, []);

  useEffect(() => {
    setLoading(true);
    setError(null);
    const t = setTimeout(() => {
      listCards({
        topic: selectedTopic || undefined,
        q: q || undefined,
        limit: 50,
      })
        .then((r) => {
          setCards(r.cards);
          setTotal(r.total);
        })
        .catch((e) => setError(e.message))
        .finally(() => setLoading(false));
    }, q ? 200 : 0);
    return () => clearTimeout(t);
  }, [selectedTopic, q]);

  async function openDetail(id: string) {
    setOpenLoading(true);
    try {
      const c = await getCard(id);
      setOpenCard(c);
    } catch (e: any) {
      setError(e.message);
    } finally {
      setOpenLoading(false);
    }
  }

  return (
    <div className="min-h-screen bg-cbt-bg dark:bg-cbt-dark-bg">
      <header className="sticky top-0 z-30 border-b border-cbt-border/60 dark:border-cbt-dark-border/60 bg-cbt-bg/80 dark:bg-cbt-dark-bg/80 backdrop-blur-xl backdrop-saturate-150">
        <div className="max-w-4xl mx-auto flex items-center justify-between px-4 py-3">
          <div>
            <h1 className="text-[15px] font-semibold tracking-tight text-cbt-text dark:text-cbt-dark-text">
              Kart Kütüphanesi
            </h1>
            <p className="text-xs text-cbt-textMuted dark:text-cbt-dark-textMuted mt-0.5">
              CBT temelli bilgi ve egzersiz kartları
            </p>
          </div>
          <div className="flex items-center gap-2">
            <ThemeToggle />
            <a
              href="/"
              className="flex items-center gap-1 text-xs text-cbt-textMuted dark:text-cbt-dark-textMuted hover:text-cbt-text dark:hover:text-cbt-dark-text transition-colors"
            >
              <ArrowLeft size={14} strokeWidth={2.2} />
              Ana sayfa
            </a>
          </div>
        </div>
      </header>

      <div className="max-w-4xl mx-auto px-4 py-6 space-y-5">
        <div className="flex flex-wrap gap-1.5">
          <TopicPill
            active={selectedTopic === ""}
            onClick={() => setSelectedTopic("")}
          >
            Tümü
          </TopicPill>
          {topics.map((t) => (
            <TopicPill
              key={t.topic}
              active={selectedTopic === t.topic}
              onClick={() => setSelectedTopic(t.topic)}
              count={t.count}
            >
              {t.display_name_tr}
            </TopicPill>
          ))}
        </div>

        <div className="relative">
          <Search
            size={15}
            strokeWidth={2.2}
            className="absolute left-3 top-1/2 -translate-y-1/2 text-cbt-textMuted dark:text-cbt-dark-textMuted"
          />
          <input
            className="w-full pl-9 pr-9 py-2.5 bg-cbt-surface dark:bg-cbt-dark-surface border border-cbt-border dark:border-cbt-dark-border rounded-xl text-[14px] text-cbt-text dark:text-cbt-dark-text placeholder:text-cbt-textMuted dark:placeholder:text-cbt-dark-textMuted focus:outline-none focus:border-cbt-borderStrong dark:focus:border-cbt-dark-borderStrong transition-colors"
            placeholder="Başlıkta ara…"
            value={q}
            onChange={(e) => setQ(e.target.value)}
          />
          {q && (
            <button
              onClick={() => setQ("")}
              className="absolute right-3 top-1/2 -translate-y-1/2 text-cbt-textMuted dark:text-cbt-dark-textMuted hover:text-cbt-text dark:hover:text-cbt-dark-text"
              aria-label="Temizle"
            >
              <X size={14} strokeWidth={2.4} />
            </button>
          )}
        </div>

        <div className="text-xs text-cbt-textMuted dark:text-cbt-dark-textMuted">
          {loading ? "Yükleniyor…" : `${total} kart`}
        </div>

        {error && (
          <div className="text-xs text-cbt-danger dark:text-cbt-dark-danger bg-cbt-dangerSoft dark:bg-cbt-dark-dangerSoft border border-cbt-danger/20 dark:border-cbt-dark-danger/30 rounded-lg px-4 py-3">
            {error}
          </div>
        )}

        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-3">
          {loading && cards.length === 0
            ? Array.from({ length: 6 }).map((_, i) => (
                <div
                  key={i}
                  className="h-24 rounded-xl bg-cbt-surface dark:bg-cbt-dark-surface border border-cbt-border/40 dark:border-cbt-dark-border/40 shimmer"
                />
              ))
            : cards.map((c, i) => (
                <button
                  key={c.id}
                  onClick={() => openDetail(c.id)}
                  className="text-left p-4 rounded-xl bg-cbt-surface dark:bg-cbt-dark-surface border border-cbt-border/60 dark:border-cbt-dark-border/60 hover:border-cbt-borderStrong dark:hover:border-cbt-dark-borderStrong hover:shadow-soft transition-all active:scale-[0.99] group animate-slide-up"
                  style={{
                    animationDelay: `${Math.min(i * 40, 400)}ms`,
                    animationFillMode: "backwards",
                  }}
                >
                  <div className="text-[14px] font-medium leading-snug text-cbt-text dark:text-cbt-dark-text group-hover:text-cbt-accent dark:group-hover:text-cbt-dark-accent transition-colors">
                    {c.title_tr}
                  </div>
                  <div className="mt-2 flex items-center gap-1.5 text-[11px] text-cbt-textMuted dark:text-cbt-dark-textMuted">
                    <span className="uppercase tracking-wide">
                      {c.topic.replace("_", " ")}
                    </span>
                    <span className="w-0.5 h-0.5 rounded-full bg-cbt-textMuted dark:bg-cbt-dark-textMuted" />
                    <span>{TYPE_LABELS[c.type] || c.type}</span>
                  </div>
                </button>
              ))}
        </div>

        {cards.length === 0 && !loading && (
          <div className="text-sm text-cbt-textMuted dark:text-cbt-dark-textMuted text-center py-12">
            Kart bulunamadı.
          </div>
        )}
      </div>

      {openCard && (
        <div
          className="fixed inset-0 z-40 bg-black/40 dark:bg-black/60 backdrop-blur-sm p-4 flex items-center justify-center animate-fade-in"
          onClick={() => setOpenCard(null)}
        >
          <div
            className="max-w-2xl w-full bg-cbt-surface dark:bg-cbt-dark-surface rounded-2xl shadow-modal max-h-[85vh] overflow-hidden flex flex-col animate-modal-in border border-cbt-border/40 dark:border-cbt-dark-border/40"
            onClick={(e) => e.stopPropagation()}
          >
            <div className="border-b border-cbt-border/60 dark:border-cbt-dark-border/60 px-6 py-4 flex items-start justify-between gap-3">
              <div>
                <h2 className="text-base font-semibold tracking-tight text-cbt-text dark:text-cbt-dark-text">
                  {openCard.title_tr}
                </h2>
                <div className="mt-1 flex items-center gap-1.5 text-[11px] text-cbt-textMuted dark:text-cbt-dark-textMuted">
                  <span className="uppercase tracking-wide">
                    {openCard.topic.replace("_", " ")}
                  </span>
                  <span className="w-0.5 h-0.5 rounded-full bg-cbt-textMuted dark:bg-cbt-dark-textMuted" />
                  <span>{TYPE_LABELS[openCard.type] || openCard.type}</span>
                  <span className="w-0.5 h-0.5 rounded-full bg-cbt-textMuted dark:bg-cbt-dark-textMuted" />
                  <code className="font-mono">{openCard.id}</code>
                </div>
              </div>
              <button
                className="flex items-center justify-center w-8 h-8 rounded-lg text-cbt-textMuted dark:text-cbt-dark-textMuted hover:text-cbt-text dark:hover:text-cbt-dark-text hover:bg-cbt-surfaceMuted dark:hover:bg-cbt-dark-surfaceMuted transition-colors"
                onClick={() => setOpenCard(null)}
                aria-label="Kapat"
              >
                <X size={16} strokeWidth={2.2} />
              </button>
            </div>
            <div className="p-6 overflow-y-auto chat-scroll text-[14px] leading-relaxed text-cbt-text dark:text-cbt-dark-text whitespace-pre-wrap">
              {openCard.content_tr}
              {openCard.safety_notes && (
                <div className="mt-5 text-xs text-cbt-warning dark:text-cbt-dark-warning bg-cbt-warningSoft dark:bg-cbt-dark-warningSoft border border-cbt-warning/20 dark:border-cbt-dark-warning/30 rounded-lg px-3 py-2.5">
                  <div className="font-medium mb-1">Güvenlik notu</div>
                  {openCard.safety_notes}
                </div>
              )}
              {openCard.source_refs.length > 0 && (
                <div className="mt-5 text-xs text-cbt-textMuted dark:text-cbt-dark-textMuted border-t border-cbt-border/60 dark:border-cbt-dark-border/60 pt-4">
                  Kaynaklar:{" "}
                  <code className="font-mono">
                    {openCard.source_refs.join(", ")}
                  </code>
                </div>
              )}
            </div>
          </div>
        </div>
      )}

      {openLoading && (
        <div className="fixed bottom-4 right-4 text-xs text-cbt-textMuted dark:text-cbt-dark-textMuted italic bg-cbt-surface dark:bg-cbt-dark-surface shadow-soft border border-cbt-border dark:border-cbt-dark-border rounded-lg px-3 py-2">
          Yükleniyor…
        </div>
      )}
    </div>
  );
}

function TopicPill({
  children,
  active,
  onClick,
  count,
}: {
  children: React.ReactNode;
  active: boolean;
  onClick: () => void;
  count?: number;
}) {
  return (
    <button
      onClick={onClick}
      className={
        active
          ? "flex items-center gap-1.5 px-3 py-1.5 rounded-full text-[13px] font-medium bg-cbt-text dark:bg-cbt-dark-text text-cbt-surface dark:text-cbt-dark-bg transition-all"
          : "flex items-center gap-1.5 px-3 py-1.5 rounded-full text-[13px] font-medium bg-cbt-surface dark:bg-cbt-dark-surface border border-cbt-border dark:border-cbt-dark-border text-cbt-textSecondary dark:text-cbt-dark-textSecondary hover:border-cbt-borderStrong dark:hover:border-cbt-dark-borderStrong hover:text-cbt-text dark:hover:text-cbt-dark-text transition-all"
      }
    >
      <span>{children}</span>
      {count != null && (
        <span
          className={
            active
              ? "text-[11px] opacity-60"
              : "text-[11px] text-cbt-textMuted dark:text-cbt-dark-textMuted"
          }
        >
          {count}
        </span>
      )}
    </button>
  );
}
