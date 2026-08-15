"use client";

import {
  MessageCircle,
  ArrowRight,
  Pencil,
  Lightbulb,
  Wind,
  Lock,
  Heart,
  Compass,
  BookOpen,
} from "lucide-react";
import ThemeToggle from "./ThemeToggle";

export default function Landing({ onStart }: { onStart: () => void }) {
  return (
    <div className="relative min-h-screen flex flex-col">
      {/* Header */}
      <header className="sticky top-0 z-20 border-b border-cbt-border/50 dark:border-cbt-dark-border/50 bg-cbt-bg/80 dark:bg-cbt-dark-bg/80 backdrop-blur-xl">
        <div className="max-w-5xl mx-auto flex items-center justify-between px-6 py-4">
          <span className="text-[17px] font-semibold tracking-tight text-cbt-text dark:text-cbt-dark-text">
            Neva
          </span>
          <div className="flex items-center gap-2">
            <a
              href="/cards"
              className="px-3 h-9 flex items-center rounded-full text-[13px] font-medium text-cbt-textSecondary dark:text-cbt-dark-textSecondary hover:text-cbt-text dark:hover:text-cbt-dark-text transition-colors"
            >
              Konular
            </a>
            <ThemeToggle />
            <button
              onClick={onStart}
              className="px-4 h-9 flex items-center rounded-full bg-cbt-text dark:bg-cbt-dark-text text-cbt-bg dark:text-cbt-dark-bg text-[13px] font-medium hover:opacity-85 transition-opacity"
            >
              Başla
            </button>
          </div>
        </div>
      </header>

      {/* Hero */}
      <main className="flex-1 flex flex-col items-center px-6">
        <div className="max-w-3xl w-full text-center pt-24 sm:pt-36 pb-20">
          <h1 className="text-[44px] sm:text-[64px] font-semibold tracking-[-0.02em] text-cbt-text dark:text-cbt-dark-text leading-[1.05] mb-6">
            Zihnin için
            <br />
            sakin bir alan.
          </h1>

          <p className="text-[17px] sm:text-[19px] text-cbt-textSecondary dark:text-cbt-dark-textSecondary leading-relaxed max-w-xl mx-auto mb-10">
            Kaygı, düşük ruh hali, uykusuzluk ya da zor bir dönem —
            ne yaşıyorsan, bilişsel davranışçı terapi temelli yöntemlerle
            birlikte üzerinden geçelim.
          </p>

          <div className="flex flex-col sm:flex-row items-center justify-center gap-4 mb-6">
            <button
              onClick={onStart}
              className="inline-flex items-center gap-2 px-7 h-12 rounded-full bg-cbt-text dark:bg-cbt-dark-text text-cbt-bg dark:text-cbt-dark-bg text-[15px] font-medium hover:opacity-85 transition-opacity active:scale-[0.98]"
            >
              Konuşmaya başla
            </button>
            <a
              href="/cards"
              className="inline-flex items-center gap-1.5 px-5 h-12 rounded-full text-[15px] text-cbt-textSecondary dark:text-cbt-dark-textSecondary hover:text-cbt-text dark:hover:text-cbt-dark-text transition-colors"
            >
              Konuları incele
              <ArrowRight size={15} strokeWidth={2} />
            </a>
          </div>

          <p className="text-[12px] text-cbt-textMuted dark:text-cbt-dark-textMuted">
            Üyelik gerektirmez · Verilerini istediğin an silebilirsin
          </p>
        </div>

        {/* How it works */}
        <section className="w-full max-w-4xl pb-24">
          <h2 className="text-[28px] sm:text-[32px] font-semibold tracking-tight text-cbt-text dark:text-cbt-dark-text text-center mb-12">
            Nasıl çalışır
          </h2>

          <div className="grid grid-cols-1 md:grid-cols-3 gap-5">
            <Step
              icon={<Pencil size={20} strokeWidth={1.8} />}
              title="Anlat"
              body="Bugün seni zorlayan ne varsa yaz. Düzgün cümleler kurman gerekmiyor — aklından geçen neyse o."
            />
            <Step
              icon={<Lightbulb size={20} strokeWidth={1.8} />}
              title="Fark et"
              body="Düşünce ve davranış örüntülerini birlikte inceleyelim. Neyin seni sıkıştırdığını görmek, çoğu zaman ilk adımdır."
            />
            <Step
              icon={<Wind size={20} strokeWidth={1.8} />}
              title="Küçük bir adım at"
              body="Kısa bir nefes egzersizi, bir düşünce kaydı ya da küçük bir plan. Bugün için bir adım yeterli."
            />
          </div>
        </section>

        {/* Values */}
        <section className="w-full max-w-4xl pb-24">
          <h2 className="text-[28px] sm:text-[32px] font-semibold tracking-tight text-cbt-text dark:text-cbt-dark-text text-center mb-12">
            Neye güvenebilirsin
          </h2>

          <div className="grid grid-cols-1 sm:grid-cols-3 gap-5">
            <Value
              icon={<Lock size={18} strokeWidth={1.8} />}
              title="Gizlilik"
              body="Üyeliksiz kullanabilirsin. Mesajların kalıcı olarak saklanmaz; hesabını ve verilerini istediğin an silebilirsin."
            />
            <Value
              icon={<BookOpen size={18} strokeWidth={1.8} />}
              title="Bilimsel temel"
              body="İçerik; NICE, APA gibi klinik rehberlere ve hakemli araştırmalara dayanan bilişsel davranışçı terapi yöntemlerinden derlenmiştir."
            />
            <Value
              icon={<Compass size={18} strokeWidth={1.8} />}
              title="Sınırlarını bilir"
              body="Neva bir terapist değildir ve terapinin yerini tutmaz. İhtiyaç hâlinde seni bir uzmana ya da acil yardım hattına yönlendirir."
            />
          </div>
        </section>

        {/* Final CTA */}
        <section className="w-full max-w-2xl text-center pb-24">
          <h2 className="text-[24px] font-semibold tracking-tight text-cbt-text dark:text-cbt-dark-text mb-3">
            Hazır olduğunda başla.
          </h2>
          <p className="text-[15px] text-cbt-textSecondary dark:text-cbt-dark-textSecondary mb-8">
            Acele etmene gerek yok.
          </p>
          <button
            onClick={onStart}
            className="inline-flex items-center gap-2 px-7 h-12 rounded-full bg-cbt-text dark:bg-cbt-dark-text text-cbt-bg dark:text-cbt-dark-bg text-[15px] font-medium hover:opacity-85 transition-opacity active:scale-[0.98]"
          >
            Konuşmaya başla
          </button>
        </section>
      </main>

      <footer className="border-t border-cbt-border/50 dark:border-cbt-dark-border/50 px-6 py-6">
        <div className="max-w-5xl mx-auto text-center text-[12px] text-cbt-textMuted dark:text-cbt-dark-textMuted leading-relaxed">
          Neva bir terapist, hekim ya da acil servis değildir.
          <br />
          Kendine zarar verme düşüncen varsa ya da acil durumdaysan{" "}
          <span className="font-semibold text-cbt-text dark:text-cbt-dark-text">112</span>
          'yi ara.
        </div>
      </footer>
    </div>
  );
}

function Step({
  icon,
  title,
  body,
}: {
  icon: React.ReactNode;
  title: string;
  body: string;
}) {
  return (
    <div className="p-7 rounded-2xl bg-cbt-surface dark:bg-cbt-dark-surface border border-cbt-border/60 dark:border-cbt-dark-border/60">
      <div className="text-cbt-text dark:text-cbt-dark-text mb-4">{icon}</div>
      <div className="text-[16px] font-semibold text-cbt-text dark:text-cbt-dark-text mb-2">
        {title}
      </div>
      <div className="text-[14px] text-cbt-textSecondary dark:text-cbt-dark-textSecondary leading-relaxed">
        {body}
      </div>
    </div>
  );
}

function Value({
  icon,
  title,
  body,
}: {
  icon: React.ReactNode;
  title: string;
  body: string;
}) {
  return (
    <div className="p-7 rounded-2xl bg-cbt-surface dark:bg-cbt-dark-surface border border-cbt-border/60 dark:border-cbt-dark-border/60">
      <div className="text-cbt-text dark:text-cbt-dark-text mb-4">{icon}</div>
      <div className="text-[16px] font-semibold text-cbt-text dark:text-cbt-dark-text mb-2">
        {title}
      </div>
      <div className="text-[14px] text-cbt-textSecondary dark:text-cbt-dark-textSecondary leading-relaxed">
        {body}
      </div>
    </div>
  );
}
