// Hesap profilinin cihaz-yerel önbelleği.
//
// Kaynak doğruluk sunucuda: users.display_name / focus_topics / onboarded_at.
// Burası yalnızca senkron okuma için kopya tutuyor — ChatWindow karşılama
// metnini render sırasında kuruyor ve orada await edemiyoruz.
//
// Önbellek kaybolursa kimse zarar görmez; useAuth bir sonraki /auth/me
// yanıtında yeniden yazıyor.

import type { AuthUser } from "./types";

const NAME_KEY = "neva_name";
const FOCUS_KEY = "neva_focus";
const FOCUS_USED_KEY = "neva_focus_used";

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

// Seçilen konular yalnızca ilk karşılamada anılır. Bu bayrak cihaza özel
// ve kasten sunucuya taşınmadı — kaybolursa en fazla selamlama bir kez
// daha konulardan bahseder.
export function getFocusLabels(): string[] {
  if (typeof window === "undefined") return [];
  if (window.localStorage.getItem(FOCUS_USED_KEY) === "true") return [];
  const ids = getFocus();
  return FOCUS_OPTIONS.filter((o) => ids.includes(o.id) && o.id !== "unsure").map(
    (o) => o.label
  );
}

export function markFocusUsed(): void {
  if (typeof window === "undefined") return;
  window.localStorage.setItem(FOCUS_USED_KEY, "true");
}

/** Sunucudan gelen kullanıcıyı önbelleğe yaz. Kullanıcı yoksa temizle. */
export function cacheProfileFromUser(user: AuthUser | null): void {
  if (typeof window === "undefined") return;
  if (!user) {
    clearProfile();
    return;
  }
  if (user.display_name) {
    window.localStorage.setItem(NAME_KEY, user.display_name);
  } else {
    window.localStorage.removeItem(NAME_KEY);
  }
  window.localStorage.setItem(FOCUS_KEY, JSON.stringify(user.focus_topics || []));
}

export function clearProfile(): void {
  if (typeof window === "undefined") return;
  window.localStorage.removeItem(NAME_KEY);
  window.localStorage.removeItem(FOCUS_KEY);
  window.localStorage.removeItem(FOCUS_USED_KEY);
}

/** Sunucuya geçişten önce cihazda kalmış ad/konu — bir kez yukarı taşınır. */
export function readLegacyLocalProfile(): { name: string; focus: string[] } | null {
  if (typeof window === "undefined") return null;
  if (window.localStorage.getItem("neva_onboarded") !== "true") return null;
  const name = window.localStorage.getItem(NAME_KEY) || "";
  const focus = getFocus();
  return { name, focus };
}

export function clearLegacyMarkers(): void {
  if (typeof window === "undefined") return;
  window.localStorage.removeItem("neva_onboarded");
  window.localStorage.removeItem("neva_profile_owner");
}
