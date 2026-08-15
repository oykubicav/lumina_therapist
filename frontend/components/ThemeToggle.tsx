"use client";

import { useEffect, useState } from "react";
import { Sun, Moon } from "lucide-react";
import { resolveTheme, toggleTheme, applyTheme, type Theme } from "@/lib/theme";

export default function ThemeToggle() {
  const [theme, setThemeState] = useState<Theme>("light");
  const [mounted, setMounted] = useState(false);

  useEffect(() => {
    const t = resolveTheme();
    setThemeState(t);
    applyTheme(t);
    setMounted(true);
  }, []);

  function handleToggle() {
    const next = toggleTheme();
    setThemeState(next);
  }

  // Avoid hydration mismatch — render neutral until mounted
  if (!mounted) {
    return (
      <div className="w-8 h-8" aria-hidden />
    );
  }

  const isDark = theme === "dark";

  return (
    <button
      onClick={handleToggle}
      className="flex items-center justify-center w-8 h-8 rounded-lg text-cbt-textMuted hover:text-cbt-text hover:bg-cbt-surfaceMuted dark:text-cbt-dark-textMuted dark:hover:text-cbt-dark-text dark:hover:bg-cbt-dark-surfaceMuted transition-colors"
      title={isDark ? "Açık moda geç" : "Koyu moda geç"}
      aria-label={isDark ? "Açık moda geç" : "Koyu moda geç"}
    >
      {isDark ? (
        <Sun size={16} strokeWidth={2.2} />
      ) : (
        <Moon size={16} strokeWidth={2.2} />
      )}
    </button>
  );
}
