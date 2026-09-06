// User-Agent'tan okunabilir bir etiket. Kesin değil — UA dizesi kolayca
// taklit edilebiliyor ve tarayıcılar birbirinin adını taşıyor (Chrome'un
// UA'sında "Safari" de geçiyor). Amaç kullanıcının kendi cihazını tanıması,
// adli bir kayıt değil.

export function deviceLabel(ua: string | null): string {
    if (!ua) return "Bilinmeyen cihaz";
  
    const tarayici =
      /Edg\//.test(ua) ? "Edge"
      : /OPR\/|Opera/.test(ua) ? "Opera"
      : /Chrome\//.test(ua) ? "Chrome"
      : /Firefox\//.test(ua) ? "Firefox"
      : /Safari\//.test(ua) ? "Safari"
      : null;
  
    const sistem =
      /iPhone/.test(ua) ? "iPhone"
      : /iPad/.test(ua) ? "iPad"
      : /Android/.test(ua) ? "Android"
      : /Mac OS X|Macintosh/.test(ua) ? "Mac"
      : /Windows/.test(ua) ? "Windows"
      : /Linux/.test(ua) ? "Linux"
      : null;
  
    if (tarayici && sistem) return `${tarayici} · ${sistem}`;
    return tarayici || sistem || "Bilinmeyen cihaz";
  }