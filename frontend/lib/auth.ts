// Access token BELLEKTE tutuluyor, localStorage'da değil.
//
// Gerekçe: localStorage'daki her şeyi XSS ile çalınabilir sayman gerekiyor.
// Access token bellekte durursa sayfa yenilenince kayboluyor ve refresh
// çerezinden yeniden alınıyor — o çerez de httpOnly, JavaScript göremiyor.
// Yani diskte okunabilir kimlik bilgisi kalmıyor.

let accessToken: string | null = null;

export function getAccessToken(): string | null {
  return accessToken;
}

export function setAccessToken(token: string | null): void {
  accessToken = token;
}

export function clearAccessToken(): void {
  accessToken = null;
}