"use client";

import {
  Wind,
  CloudRain,
  Frown,
  Zap,
  Heart,
  Sparkles,
  Briefcase,
  Users,
  Feather,
  Compass,
  Shield,
} from "lucide-react";

// Warm, common CBT starter prompts.
const PROMPTS = [
  {
    label: "Kaygım yükseldi, sakinleşmek istiyorum",
    icon: <Wind size={13} strokeWidth={2.2} />,
  },
  {
    label: "Bugün moralim çok düşük",
    icon: <CloudRain size={13} strokeWidth={2.2} />,
  },
  {
    label: "İş stresim çok arttı, tükenmiş hissediyorum",
    icon: <Briefcase size={13} strokeWidth={2.2} />,
  },
  {
    label: "Kendime karşı çok sertim",
    icon: <Frown size={13} strokeWidth={2.2} />,
  },
  {
    label: "Panik atak yaşadım, ne yapabilirim?",
    icon: <Zap size={13} strokeWidth={2.2} />,
  },
  {
    label: "Uyuyamıyorum, zihnim durmuyor",
    icon: <Sparkles size={13} strokeWidth={2.2} />,
  },
  {
    label: "Yalnız hissediyorum",
    icon: <Heart size={13} strokeWidth={2.2} />,
  },
  {
    label: "Partnerimle iletişim çöktü, çıkış yolu göremiyorum",
    icon: <Users size={13} strokeWidth={2.2} />,
  },
  {
    label: "Yakınımı kaybettim, yasın içindeyim",
    icon: <Feather size={13} strokeWidth={2.2} />,
  },
  {
    label: "Büyük bir yaşam geçişindeyim, yönümü bulamıyorum",
    icon: <Compass size={13} strokeWidth={2.2} />,
  },
  {
    label: "Travmatik bir olay yaşadım, tepkilerimi anlamak istiyorum",
    icon: <Shield size={13} strokeWidth={2.2} />,
  },
];

export default function SuggestedPrompts({
  onPick,
}: {
  onPick: (prompt: string) => void;
}) {
  return (
    <div className="animate-fade-in">
      <p className="text-[12px] text-cbt-textMuted dark:text-cbt-dark-textMuted mb-3 pl-1">
        Bugün seninle konuşabileceğimiz şeyler
      </p>
      <div className="flex flex-wrap gap-2">
        {PROMPTS.map((p, i) => (
          <button
            key={i}
            onClick={() => onPick(p.label)}
            className="group inline-flex items-center gap-1.5 px-3 py-2 rounded-full bg-cbt-surface dark:bg-cbt-dark-surface border border-cbt-border/60 dark:border-cbt-dark-border/60 text-[13px] text-cbt-textSecondary dark:text-cbt-dark-textSecondary hover:text-cbt-text dark:hover:text-cbt-dark-text hover:border-cbt-borderStrong dark:hover:border-cbt-dark-borderStrong hover:shadow-subtle transition-all active:scale-[0.98] animate-slide-up"
            style={{ animationDelay: `${i * 60}ms`, animationFillMode: "backwards" }}
          >
            <span className="text-cbt-accent dark:text-cbt-dark-accent group-hover:scale-110 transition-transform">
              {p.icon}
            </span>
            {p.label}
          </button>
        ))}
      </div>
    </div>
  );
}
