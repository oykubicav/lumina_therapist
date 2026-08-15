// Theme (light / dark) — localStorage-persisted + respects prefers-color-scheme.
// Manipulates `document.documentElement` classList directly for Tailwind
// darkMode: "class" strategy.

export type Theme = "light" | "dark";

const KEY = "cbt_theme";

export function getStoredTheme(): Theme | null {
  if (typeof window === "undefined") return null;
  const v = window.localStorage.getItem(KEY);
  return v === "dark" || v === "light" ? v : null;
}

export function getSystemTheme(): Theme {
  if (typeof window === "undefined") return "light";
  return window.matchMedia("(prefers-color-scheme: dark)").matches
    ? "dark"
    : "light";
}

export function resolveTheme(): Theme {
  return getStoredTheme() ?? getSystemTheme();
}

export function applyTheme(theme: Theme): void {
  if (typeof document === "undefined") return;
  document.documentElement.classList.toggle("dark", theme === "dark");
}

export function setTheme(theme: Theme): void {
  if (typeof window === "undefined") return;
  window.localStorage.setItem(KEY, theme);
  applyTheme(theme);
}

export function toggleTheme(): Theme {
  const current = resolveTheme();
  const next: Theme = current === "dark" ? "light" : "dark";
  setTheme(next);
  return next;
}
