// PHQ-9 & GAD-7 Türkçe soru metinleri
// Klinik Türkçe kullanımı — orijinal İngilizce validasyon skalasının
// resmi TR adaptasyonuna yakın (kaynak: TPD çalışmaları).

export const PHQ9_QUESTIONS_TR = [
    "İşlerinizi yapmakta çok az ilgi ya da zevk almak",
    "Kendinizi kötü, karamsar ya da umutsuz hissetmek",
    "Uykuya dalmakta ya da uykuyu sürdürmekte zorluk, ya da çok fazla uyumak",
    "Kendinizi yorgun hissetmek ya da az enerjiniz olması",
    "Az iştahınız olması ya da aşırı yeme",
    "Kendinizden kötü hissetmek — ya da başarısız olduğunuzu ya da kendinize/ailenize başarısız düşürdüğünüzü düşünmek",
    "Gazete okumak ya da televizyon izlemek gibi şeylere odaklanmakta zorluk",
    "Diğer insanların fark edebileceği kadar yavaş hareket etmek ya da konuşmak — ya da tam tersi, çok fazla huzursuz hissedip normalden daha çok hareket etmek",
    "Ölmüş olsanız daha iyi olacağı ya da kendinize bir şekilde zarar vermek gibi düşüncelerinizin olması",
  ];
  
  export const GAD7_QUESTIONS_TR = [
    "Sinirli, kaygılı ya da endişeli hissetmek",
    "Endişelenmenizi durduramamak ya da kontrol edememek",
    "Farklı şeyler için çok fazla endişelenmek",
    "Rahatlamakta zorluk",
    "Yerinizde duramayacak kadar huzursuz hissetmek",
    "Kolayca sinirlenmek ya da öfkelenmek",
    "Kötü bir şey olacakmış gibi hissetmek",
  ];
  
  export const LIKERT_OPTIONS_TR = [
    { value: 0, label: "Hiç" },
    { value: 1, label: "Bazı günler" },
    { value: 2, label: "Çoğu gün" },
    { value: 3, label: "Neredeyse her gün" },
  ];
  
  export const SEVERITY_LABELS_TR: Record<string, string> = {
    minimal: "Belirti yok / minimal",
    mild: "Hafif",
    moderate: "Orta",
    moderately_severe: "Orta-şiddetli",
    severe: "Şiddetli",
  };
  
  export const SEVERITY_COLORS: Record<string, string> = {
    minimal: "bg-emerald-500",
    mild: "bg-yellow-500",
    moderate: "bg-orange-500",
    moderately_severe: "bg-red-500",
    severe: "bg-red-700",
  };

  const OPTIN_KEY = "cbt_assess_optin";
  const FREQ_KEY = "cbt_assess_freq";
  const LAST_KEY = "cbt_assess_last";

  export type AssessFrequency = "weekly" | "biweekly" | "off";

  export function hasAssessmentOptedIn(): boolean {
    if (typeof window === "undefined") return false;
    return window.localStorage.getItem(OPTIN_KEY) === "true";
  }

  export function getFrequency(): AssessFrequency {
    if (typeof window === "undefined") return "biweekly";
    return (window.localStorage.getItem(FREQ_KEY) as AssessFrequency) || "biweekly";
  }

  export function setOptIn(freq: AssessFrequency) {
    window.localStorage.setItem(OPTIN_KEY, freq === "off" ? "false" : "true");
    window.localStorage.setItem(FREQ_KEY, freq);
  }

  export function markAssessmentTaken() {
    window.localStorage.setItem(LAST_KEY, new Date().toISOString());
  }

  export function shouldPromptNow(): boolean {
    if (!hasAssessmentOptedIn()) return false;
    const freq = getFrequency();
    if (freq === "off") return false;
  
    const last = window.localStorage.getItem(LAST_KEY);
    if (!last) return true;   // henüz hiç ölçüm yok → hemen prompt
  
    const daysSince = (Date.now() - new Date(last).getTime()) / (1000 * 60 * 60 * 24);
    const threshold = freq === "weekly" ? 7 : 14;
    return daysSince >= threshold;
  }
  const DECISION_KEY = "cbt_assess_decided";

  export function hasDecided(): boolean {
    if (typeof window === "undefined") return true;   // SSR — modal gösterme
    return window.localStorage.getItem(DECISION_KEY) === "true";
  }

  export function markDecided() {
    window.localStorage.setItem(DECISION_KEY, "true");
  }