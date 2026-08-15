// Persist session_id in localStorage so refresh keeps the conversation.

const KEY = "cbt_session_id";

export function getSessionId(): string | null {
  if (typeof window === "undefined") return null;
  return window.localStorage.getItem(KEY);
}

export function setSessionId(id: string): void {
  if (typeof window === "undefined") return;
  window.localStorage.setItem(KEY, id);
}

export function clearSessionId(): void {
  if (typeof window === "undefined") return;
  window.localStorage.removeItem(KEY);
}
