// Onboarding konu listesi ve id → etiket çevirisi.
//
// Ad, seçilen konular ve "konular anıldı mı" bilgisi sunucuda tutuluyor
// (users.display_name / focus_topics / focus_greeted_at). Burada yerel
// kopya yok; tek kaynak useAuth'un döndürdüğü user nesnesi.

const LEGACY_NAME_KEY = "neva_name";
const LEGACY_FOCUS_KEY = "neva_focus";
const LEGACY_DONE_KEY = "neva_onboarded";
const LEGACY_USED_KEY = "neva_focus_used";
const LEGACY_OWNER_KEY = "neva_profile_owner";

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

/** Seçilen konu id'lerini görünür etiketlere çevirir. "unsure" anılmaz. */
export function focusLabelsFor(ids: string[] | null | undefined): string[] {
  if (!ids || ids.length === 0) return [];
  return FOCUS_OPTIONS.filter((o) => ids.includes(o.id) && o.id !== "unsure").map(
    (o) => o.label
  );
}

/** Sunucuya geçişten önce cihazda kalmış ad/konu — bir kez yukarı taşınır. */
export function readLegacyLocalProfile(): { name: string; focus: string[] } | null {
  if (typeof window === "undefined") return null;
  if (window.localStorage.getItem(LEGACY_DONE_KEY) !== "true") return null;

  const name = window.localStorage.getItem(LEGACY_NAME_KEY) || "";
  let focus: string[] = [];
  try {
    const raw = window.localStorage.getItem(LEGACY_FOCUS_KEY);
    const parsed = raw ? JSON.parse(raw) : null;
    if (Array.isArray(parsed)) focus = parsed;
  } catch {
    // bozuk kayıt — konu seçimi olmadan devam
  }
  return { name, focus };
}

/** Taşıma sonrası eski anahtarları temizle. */
export function clearProfile(): void {
  if (typeof window === "undefined") return;
  for (const key of [
    LEGACY_NAME_KEY,
    LEGACY_FOCUS_KEY,
    LEGACY_DONE_KEY,
    LEGACY_USED_KEY,
    LEGACY_OWNER_KEY,
  ]) {
    window.localStorage.removeItem(key);
  }
}
