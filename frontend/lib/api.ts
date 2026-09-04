// Thin fetch wrapper around the CBT backend.

import type {
  ChatRequest,
  ChatResponse,
  CBTCardListResponse,
  CBTCardOut,
  TopicsResponse,
  FeedbackRequest,
  Assessment,
  AssessmentSubmit,
  AssessmentSubmitResponse,
  TransparencyView,
  AuthUser,
  LoginResponse,
  SessionListResponse,
  SessionDetail,
  ProfileUpdate,


} from "./types";
import { getToken } from "./auth";

const API_BASE =
  process.env.NEXT_PUBLIC_API_BASE || "http://localhost:8000";

async function fetchJson<T>(path: string, init?: RequestInit): Promise<T> {
  const token = getToken();
  const authHeader: HeadersInit = token
    ? { Authorization: `Bearer ${token}` }
    : {};
  const res = await fetch(`${API_BASE}${path}`, {
    
    ...init,
    headers: {
      "Content-Type": "application/json",
      ...authHeader,
      ...(init?.headers || {}),
    },
  });
  if (!res.ok) {
    const text = await res.text().catch(() => "");
    throw new ApiError(res.status, text || res.statusText);
  }
  return res.json();
}

export class ApiError extends Error {
  constructor(public status: number, public body: string) {
    super(`API ${status}: ${body.slice(0, 200)}`);
  }
}
export interface ConsentResponse {
  session_id: string;
  consent_id: string;
  policy_version: string;
}

// Chat

export async function postChat(req: ChatRequest): Promise<ChatResponse> {
  return fetchJson<ChatResponse>("/chat", {
    method: "POST",
    body: JSON.stringify(req),
  });
}

export async function deleteSession(sessionId: string): Promise<{ deleted: boolean }> {
  return fetchJson(`/chat/session/${sessionId}`, { method: "DELETE" });
}

export async function getSessionRecap(
  sessionId: string
): Promise<{ session_id: string; recap: string }> {
  return fetchJson(`/chat/session/${sessionId}/recap`);
}


// Cards
export async function listCards(params: {
  topic?: string;
  type?: string;
  q?: string;
  limit?: number;
  offset?: number;
}): Promise<CBTCardListResponse> {
  const search = new URLSearchParams();
  if (params.topic) search.set("topic", params.topic);
  if (params.type) search.set("type", params.type);
  if (params.q) search.set("q", params.q);
  if (params.limit != null) search.set("limit", String(params.limit));
  if (params.offset != null) search.set("offset", String(params.offset));
  const qs = search.toString();
  return fetchJson<CBTCardListResponse>(`/cards${qs ? "?" + qs : ""}`);
}

export async function getCard(cardId: string): Promise<CBTCardOut> {
  return fetchJson<CBTCardOut>(`/cards/${encodeURIComponent(cardId)}`);
}

export async function getTopics(): Promise<TopicsResponse> {
  return fetchJson<TopicsResponse>("/cards/topics");
}


// Feedback

export async function postFeedback(
  req: FeedbackRequest
): Promise<{ received: boolean; feedback_id: string }> {
  return fetchJson("/feedback", {
    method: "POST",
    body: JSON.stringify(req),
  });
}
export async function postConsent(
  policyVersion: string,
  sessionId?: string,
): Promise<ConsentResponse> {
  return fetchJson<ConsentResponse>("/consent", {
    method: "POST",
    body: JSON.stringify({
      policy_version: policyVersion,
      session_id: sessionId,
    }),
  });
}

export async function submitAssessment(
  req: AssessmentSubmit
): Promise<AssessmentSubmitResponse> {
  return fetchJson<AssessmentSubmitResponse>("/assessments", {
    method: "POST",
    body: JSON.stringify(req),
  });
}
export async function getLatestAssessment(
  sessionId: string,
  kind?: "phq9" | "gad7"
): Promise<Assessment | null> {
  const params = new URLSearchParams({ session_id: sessionId });
  if (kind) params.set("kind", kind);
  return fetchJson<Assessment | null>(`/assessments/latest?${params}`);
}


export async function listAssessments(
  sessionId: string,
  kind?: "phq9" | "gad7",
  limit = 20
): Promise<Assessment[]> {
  const params = new URLSearchParams({
    session_id: sessionId,
    limit: String(limit),
  });
  if (kind) params.set("kind", kind);
  return fetchJson<Assessment[]>(`/assessments?${params}`);
}

export async function getTransparency(turnId: string): Promise<TransparencyView> {
  return fetchJson<TransparencyView>(`/transparency/${turnId}`);
}

//Auth Endpoints
export async function postRegister(email: string, password: string): Promise<AuthUser> {
  return fetchJson<AuthUser>("/auth/register", {
    method: "POST",
    body: JSON.stringify({ email, password }),
  });
}
export async function postLogin(email: string, password: string): Promise<LoginResponse> {
  return fetchJson<LoginResponse>("/auth/login", {
    method: "POST",
    body: JSON.stringify({ email, password }),
  });
}
export async function postVerify(token: string): Promise<{ status: string }> {
  return fetchJson("/auth/verify", {
    method: "POST",
    body: JSON.stringify({ token }),
  });
}
export async function postForgotPassword(email: string): Promise<{ status: string }> {
  return fetchJson("/auth/forgot-password", {
    method: "POST",
    body: JSON.stringify({ email }),
  });
}
export async function postResetPassword(token: string, newPassword: string): Promise<{ status: string }> {
  return fetchJson("/auth/reset-password", {
    method: "POST",
    body: JSON.stringify({ token, new_password: newPassword }),
  });
}
export async function getMe(): Promise<AuthUser> {
  return fetchJson<AuthUser>("/auth/me");
}

export async function patchMyProfile(req: ProfileUpdate): Promise<AuthUser> {
  return fetchJson<AuthUser>("/auth/me/profile", {
    method: "PATCH",
    body: JSON.stringify(req),
  });
}
export async function deleteMe(): Promise<{ status: string }> {
  return fetchJson("/auth/me", { method: "DELETE" });
}
export async function postResendVerify(email: string): Promise<{ status: string }> {
  return fetchJson("/auth/resend-verify", {
    method: "POST",
    body: JSON.stringify({ email }),
  });

}
// Sohbet geçmişi — sadece kayıtlı kullanıcı

export async function listMySessions(
  params: { limit?: number; offset?: number } = {}
): Promise<SessionListResponse> {
  const qs = new URLSearchParams();
  if (params.limit != null) qs.set("limit", String(params.limit));
  if (params.offset != null) qs.set("offset", String(params.offset));
  const suffix = qs.toString() ? `?${qs}` : "";
  return fetchJson<SessionListResponse>(`/auth/sessions${suffix}`);
}

export async function getMySession(sessionId: string): Promise<SessionDetail> {
  return fetchJson<SessionDetail>(`/auth/sessions/${sessionId}`);
}

export async function deleteMySession(
  sessionId: string
): Promise<{ status: string }> {
  return fetchJson<{ status: string }>(`/auth/sessions/${sessionId}`, {
    method: "DELETE",
  });
}


