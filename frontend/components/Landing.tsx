"use client";

import {
  MessageCircle,
  LayoutGrid,
  ArrowRight,
  Sparkles,
  Pencil,
  Lightbulb,
  Wind,
  Lock,
  Heart,
  Compass,
} from "lucide-react";
import ThemeToggle from "./ThemeToggle";

export default function Landing({ onStart }: { onStart: () => void }) {
  return (
    <div className="relative min-h-screen flex flex-col overflow-hidden">
      <div className="hero-orb hero-orb-1" />
      <div className="hero-orb hero-orb-2" />

      {/* Header */}
      <header className="relative z-10 border-b border-cbt-border/40 dark:border-cbt-dark-border/40 bg-cbt-bg/60 dark:bg-cbt-dark-bg/60 backdrop-blur-xl backdrop-saturate-150">
        <div className="max-w-5xl mx-auto flex items-center justify-between px-6 py-3.5">
          <div className="flex items-center gap-2">
            <div className="flex items-center justify-center w-7 h-7 rounded-lg bg-cbt-accent text-white dark:bg-cbt-dark-accent dark:text-cbt-dark-bg">
              <Sparkles size={14} strokeWidth={2.4} />
            </div>
            <span className="text-[14px] font-semibold tracking-tight text-cbt-text dark:text-cbt-dark-text">
              CBT Destek
            </span>
          </div>
          <div className="flex items-center gap-1">
            <a
              href="/cards"
              className="flex items-center gap-1.5 px-3 h-8 rounded-lg text-[13px] text-cbt-textSecondary dark:text-cbt-dark-textSecondary hover:text-cbt-text dark:hover:text-cbt-dark-text hover:bg-cbt-surfaceMuted dark:hover:bg-cbt-dark-surfaceMuted transition-colors"
            >
              <LayoutGrid size={14} strokeWidth={2.2} />
              Kartlar
            </a>
            <ThemeToggle />
          </div>
        </div>
      </header>

      {/* Hero */}
      <main className="relative z-10 flex-1 flex flex-col items-center px-6 pt-16 sm:pt-24 pb-10">
        <div className="max-w-2xl w-full text-center animate-hero-in">
          <div className="inline-flex items-center gap-1.5 px-3 py-1 rounded-full bg-cbt-accentSoft dark:bg-cbt-dark-accentSoft text-cbt-accent dark:text-cbt-dark-accent text-[12px] font-medium mb-8">
            <Heart size={12} strokeWidth={2.4} fill="currentColor" />
            Yanında birileri olduğunu hatırlatmak için burada
          </div>

          <h1 className="text-4xl sm:text-5xl font-semibold tracking-tight text-cbt-text dark:text-cbt-dark-text mb-5 leading-tight">
            Bazı günler{" "}
            <span className="text-cbt-accent dark:text-cbt-dark-accent">ağır</span>
            .
            <br />
            Bugün onlardan biriyse,
            <br />
            <span className="text-cbt-accent dark:text-cbt-dark-accent">
              konuşabiliriz.
            </span>
          </h1>

          <p className="text-lg text-cbt-textSecondary dark:text-cbt-dark-textSecondary leading-relaxed max-w-xl mx-auto mb-10">
            Kaygı, düşük mood, panik, iç eleştirmenle savaşmak — hepsi tanıdık.
            Bir arkadaş kadar sıcak, bir çerçeve kadar net konuşan bir sohbet
            arkadaşı. Terapist değilim, ama iyi bir dinleyici olabilirim.
          </p>

          <div className="flex flex-col sm:flex-row items-center justify-center gap-3 mb-4">
            <button
              onClick={onStart}
              className="group inline-flex items-center gap-2 px-6 py-3 rounded-full bg-cbt-accent dark:bg-cbt-dark-accent text-white dark:text-cbt-dark-bg text-[15px] font-medium shadow-glow hover:shadow-elevated transition-all active:scale-[0.97]"
            >
              <MessageCircle size={16} strokeWidth={2.4} />
              Sohbete başla
              <ArrowRight
                size={15}
                strokeWidth={2.4}
                className="transition-transform group-hover:translate-x-0.5"
              />
            </button>
            <a
              href="/cards"
              className="inline-flex items-center gap-2 px-5 py-3 rounded-full text-[14px] text-cbt-textSecondary dark:text-cbt-dark-textSecondary hover:text-cbt-text dark:hover:text-cbt-dark-text transition-colors"
            >
              Önce kartları incele
              <ArrowRight size={13} strokeWidth={2.2} />
            </a>
          </div>

          <p className="text-[11px] text-cbt-textMuted dark:text-cbt-dark-textMuted">
            Kayıt gerekmiyor · İstediğin an silebilirsin · 2 dakikada başla
          </p>
        </div>

        {/* How it works */}
        <section className="mt-24 w-full max-w-4xl">
          <div className="text-center mb-10">
            <div className="inline-flex items-center gap-1.5 px-3 py-1 rounded-full bg-cbt-surfaceMuted dark:bg-cbt-dark-surfaceMuted text-cbt-textSecondary dark:text-cbt-dark-textSecondary text-[11px] font-medium mb-3 tracking-wide uppercase">
              Nasıl çalışır
            </div>
            <h2 className="text-2xl sm:text-3xl font-semibold tracking-tight text-cbt-text dark:text-cbt-dark-text">
              Üç küçük adım, hepsi bu.
            </h2>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
            <Step
              num="01"
              icon={<Pencil size={18} strokeWidth={2.2} />}
              title="Anlat"
              body="Bugün ne var, ne oldu, ne düşünüyorsun — cümle kurmasan bile olur. Kafanda ne varsa yaz."
            />
            <Step
              num="02"
              icon={<Lightbulb size={18} strokeWidth={2.2} />}
              title="Örüntüyü gör"
              body="CBT çerçevelerinden hangisi durumuna uygun onu birlikte bulalım. Kaygı döngüsü mü, iç eleştirmen mi, kaçınma mı?"
            />
            <Step
              num="03"
              icon={<Wind size={18} strokeWidth={2.2} />}
              title="Küçük bir adım dene"
              body="3 dakikalık bir nefes egzersizi, tek cümlelik bir yeniden çerçeveleme, minik bir aktivite planı — bugün için yeterli."
            />
          </div>
        </section>

        {/* Values */}
        <section className="mt-24 w-full max-w-4xl">
          <div className="text-center mb-10">
            <div className="inline-flex items-center gap-1.5 px-3 py-1 rounded-full bg-cbt-surfaceMuted dark:bg-cbt-dark-surfaceMuted text-cbt-textSecondary dark:text-cbt-dark-textSecondary text-[11px] font-medium mb-3 tracking-wide uppercase">
              Bilmen gerekenler
            </div>
            <h2 className="text-2xl sm:text-3xl font-semibold tracking-tight text-cbt-text dark:text-cbt-dark-text">
              Sınırların farkında bir arkadaş.
            </h2>
          </div>

          <div className="grid grid-cols-1 sm:grid-cols-3 gap-3">
            <Value
              icon={<Lock size={16} strokeWidth={2.2} />}
              title="Anonim"
              body="Kayıt yok. Mesajlarının ham hâli kalıcı saklanmaz, oturum bitince silinir."
            />
            <Value
              icon={<Heart size={16} strokeWidth={2.2} />}
              title="Yargısız"
              body="Sıcak, sakin, patologize etmeyen bir ton. 'Yanlış hissediyorsun' asla."
            />
            <Value
              icon={<Compass size={16} strokeWidth={2.2} />}
              title="Yönlendirir, ikame etmez"
              body="Krizde 112'ye, klinik değerlendirmede uzmana yönlendirir. Terapinin yerine geçmez."
            />
          </div>
        </section>

        {/* Final CTA */}
        <section className="mt-24 mb-8 w-full max-w-2xl text-center">
          <p className="text-[15px] text-cbt-textSecondary dark:text-cbt-dark-textSecondary mb-5">
            Hazırsan başlayalım. Aceleye gerek yok.
          </p>
          <button
            onClick={onStart}
            className="group inline-flex items-center gap-2 px-6 py-3 rounded-full bg-cbt-accent dark:bg-cbt-dark-accent text-white dark:text-cbt-dark-bg text-[15px] font-medium shadow-glow hover:shadow-elevated transition-all active:scale-[0.97]"
          >
            <MessageCircle size={16} strokeWidth={2.4} />
            Sohbete başla
            <ArrowRight
              size={15}
              strokeWidth={2.4}
              className="transition-transform group-hover:translate-x-0.5"
            />
          </button>
        </section>
      </main>

      <footer className="relative z-10 border-t border-cbt-border/40 dark:border-cbt-dark-border/40 px-6 py-4">
        <div className="max-w-5xl mx-auto text-center text-[11px] text-cbt-textMuted dark:text-cbt-dark-textMuted">
          Kriz durumunda{" "}
          <span className="font-medium text-cbt-text dark:text-cbt-dark-text">
            112
          </span>
          'yi ara. Bu araç terapist, hekim ya da acil servis yerine geçmez.
        </div>
      </footer>
    </div>
  );
}

function Step({
  num,
  icon,
  title,
  body,
}: {
  num: string;
  icon: React.ReactNode;
  title: string;
  body: string;
}) {
  return (
    <div className="p-6 rounded-2xl bg-cbt-surface/60 dark:bg-cbt-dark-surface/60 border border-cbt-border/60 dark:border-cbt-dark-border/60 backdrop-blur-sm hover:border-cbt-borderStrong dark:hover:border-cbt-dark-borderStrong transition-colors">
      <div className="flex items-center gap-3 mb-3">
        <div className="flex items-center justify-center w-9 h-9 rounded-xl bg-cbt-accentSoft dark:bg-cbt-dark-accentSoft text-cbt-accent dark:text-cbt-dark-accent">
          {icon}
        </div>
        <div className="text-[11px] font-mono text-cbt-textMuted dark:text-cbt-dark-textMuted tracking-widest">
          {num}
        </div>
      </div>
      <div className="text-[15px] font-semibold text-cbt-text dark:text-cbt-dark-text mb-1.5">
        {title}
      </div>
      <div className="text-[13px] text-cbt-textSecondary dark:text-cbt-dark-textSecondary leading-relaxed">
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
    <div className="p-4 rounded-xl bg-cbt-surface/60 dark:bg-cbt-dark-surface/60 border border-cbt-border/60 dark:border-cbt-dark-border/60 backdrop-blur-sm">
      <div className="flex items-center gap-2 mb-2 text-cbt-accent dark:text-cbt-dark-accent">
        {icon}
        <div className="text-[13px] font-medium text-cbt-text dark:text-cbt-dark-text">
          {title}
        </div>
      </div>
      <div className="text-[12px] text-cbt-textMuted dark:text-cbt-dark-textMuted leading-relaxed">
        {body}
      </div>
    </div>
  );
}
