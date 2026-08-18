const NAME_KEY = "neva_name";
const FOCUS_KEY = "neva_focus";
const DONE_KEY = "neva_onboarded";

export interface FocusOption {
  id: string;
  label: string;
}

export const FOCUS_OPTIONS: FocusOption[] = [
  { id: "anxiety", label: "Kaygı ve endişe" },
  { id: "mood", label: "Düşük ruh hali" },
  { id: "sleep", label: "Uyku sorunları" },
  { id: "self", label: "Kendime karşı sertlik" },
  { id: "work", label: "İş ve tükenmişlik" },
  { id: "relationships", label: "İlişkiler" },
  { id: "loss", label: "Kayıp ve yas" },
  { id: "change", label: "Yaşam değişimleri" },
  { id: "panic", label: "Panik" },
  { id: "unsure", label: "Henüz emin değilim" },
];

export function getName(): string {
  if (typeof window === "undefined") return "";
  return window.localStorage.getItem(NAME_KEY) || "";
}

export function getFocus(): string[] {
  if (typeof window === "undefined") return [];
  const raw = window.localStorage.getItem(FOCUS_KEY);
  if (!raw) return [];
  try {
    const parsed = JSON.parse(raw);
    return Array.isArray(parsed) ? parsed : [];
  } catch {
    return [];
  }
}

export function getFocusLabels(): string[] {
  const ids = getFocus();
  return FOCUS_OPTIONS.filter((o) => ids.includes(o.id) && o.id !== "unsure").map(
    (o) => o.label
  );
}

export function saveProfile(name: string, focus: string[]): void {
  if (typeof window === "undefined") return;
  const trimmed = name.trim();
  if (trimmed) {
    window.localStorage.setItem(NAME_KEY, trimmed);
  } else {
    window.localStorage.removeItem(NAME_KEY);
  }
  window.localStorage.setItem(FOCUS_KEY, JSON.stringify(focus));
  window.localStorage.setItem(DONE_KEY, "true");
}

export function skipOnboarding(): void {
  if (typeof window === "undefined") return;
  window.localStorage.setItem(DONE_KEY, "true");
}

export function hasOnboarded(): boolean {
  if (typeof window === "undefined") return true;
  return window.localStorage.getItem(DONE_KEY) === "true";
}

export function clearProfile(): void {
  if (typeof window === "undefined") return;
  window.localStorage.removeItem(NAME_KEY);
  window.localStorage.removeItem(FOCUS_KEY);
  window.localStorage.removeItem(DONE_KEY);
}
