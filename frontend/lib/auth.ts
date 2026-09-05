// Frontend auth state — localStorage helpers.
// JWT + user info persist edilir. React hook (useAuth) bunun üzerine oturur.

const TOKEN_KEY = "cbt_jwt";
const USER_KEY = "cbt_user";

import type { AuthUser } from "./types";

export function getToken(): string | null {
  if (typeof window === "undefined") return null;
  return window.localStorage.getItem(TOKEN_KEY);
}

export function setToken(token: string): void {
  window.localStorage.setItem(TOKEN_KEY, token);
}

export function clearToken(): void {
  if (typeof window === "undefined") return;
  window.localStorage.removeItem(TOKEN_KEY);
  window.localStorage.removeItem(USER_KEY);
}

export function getStoredUser(): AuthUser | null {
  if (typeof window === "undefined") return null;
  const raw = window.localStorage.getItem(USER_KEY);
  if (!raw) return null;
  try {
    return JSON.parse(raw) as AuthUser;
  } catch {
    return null;
  }
}

export function setStoredUser(user: AuthUser): void {
  window.localStorage.setItem(USER_KEY, JSON.stringify(user));
}

export function isAuthenticated(): boolean {
  return getToken() !== null;
}

/** JWT payload'undaki exp (saniye). Okunamazsa null.
 *
 * İmza DOĞRULANMIYOR ve doğrulanamaz — gizli anahtar sunucuda. Bu yalnızca
 * bir arayüz ipucu: süresi geçmiş token'la sunucuya gidip 401 beklemek
 * yerine kullanıcıyı hemen çıkışa alabilmek için. Yetki kararını her zaman
 * sunucu veriyor.
 */
export function getTokenExpiry(): number | null {
  const token = getToken();
  if (!token) return null;

  const parts = token.split(".");
  if (parts.length !== 3) return null;

  try {
    const b64 = parts[1].replace(/-/g, "+").replace(/_/g, "/");
    const padded = b64 + "=".repeat((4 - (b64.length % 4)) % 4);
    const payload = JSON.parse(atob(padded));
    return typeof payload.exp === "number" ? payload.exp : null;
  } catch {
    return null;
  }
}

/** Token'ın süresi dolmuş mu? Okunamayan token'a "dolmuş" demiyoruz —
 * kararı sunucuya bırakıyoruz. */
export function isTokenExpired(): boolean {
  const exp = getTokenExpiry();
  if (exp === null) return false;
  return exp * 1000 <= Date.now();
}