// Backend response types — must mirror api/schemas.py

export type SafetyRoute =
  | "cbt_support"
  | "crisis_referral"
  | "medical_emergency_referral"
  | "professional_or_emergency_referral"
  | "medical_professional_referral"
  | "scope_boundary"
  | "conditional_cbt_after_safety_check"
  | "minor_referral"
  | "abuse_safety_referral";

export type RiskLevel = "low" | "medium" | "high" | "critical";
export type AssessmentKind = "phq9" | "gad7";

export interface SafetyView {
  route: SafetyRoute;
  allow_cbt: boolean;
  highest_risk: RiskLevel;
  matched_card_ids: string[];
}

export interface IntentView {
  module: string;
  subintent: string;
  confidence: number;
}

export interface CriticView {
  passed: boolean;
  rewrites: number;
  used_fallback: boolean;
  findings_summary?: string[];
}

export interface ChatResponse {
  turn_id: string;
  session_id: string;
  response: string;
  safety: SafetyView;
  intent: IntentView;
  retrieved_card_ids: string[];
  critic: CriticView;
  timing_ms: Record<string, number>;
  boundary_state?: string;
  turn_count?: number;
}

export interface ChatOptions {
  enable_llm_critic?: boolean;
  enable_intent?: boolean;
  max_rewrites?: number;
  top_k?: number;
  temperature?: number;
}

export interface ChatRequest {
  user_message: string;
  session_id?: string;
  options?: ChatOptions;
}

// UI-local view of a turn — includes both the user prompt and assistant response
export interface Turn {
  user_message: string;
  chat: ChatResponse;
  feedback_sent?: "thumbs_up" | "thumbs_down" | "flag";
  ts?: number;  // client-side timestamp (ms) when the turn was completed
}

// Cards
export interface CBTCardSummary {
  id: string;
  topic: string;
  type: string;
  title_tr: string;
  review_status: string;
}

export interface CBTCardOut {
  id: string;
  topic: string;
  type: string;
  title_tr: string;
  content_tr: string;
  safety_notes?: string;
  source_refs: string[];
  review_status: string;
}

export interface CBTCardListResponse {
  cards: CBTCardSummary[];
  total: number;
  limit: number;
  offset: number;
}

export interface TopicInfo {
  topic: string;
  count: number;
  display_name_tr: string;
}

export interface TopicsResponse {
  topics: TopicInfo[];
}

// Feedback
export interface FeedbackRequest {
  turn_id: string;
  session_id?: string;
  verdict: "thumbs_up" | "thumbs_down" | "flag";
  comment?: string;
}

export interface Assessment {
  id: string;
  kind: AssessmentKind;
  total_score: number;
  severity: "minimal" | "mild" | "moderate" | "moderately_severe" | "severe";
  suicide_flag: boolean;
  taken_at: string;   // ISO
}

export interface AssessmentSubmit {
  session_id: string;
  kind: AssessmentKind;
  answers: number[];   // PHQ-9: 9 madde, GAD-7: 7 madde. Her biri 0-3.
  notes?: string;
}

export interface AssessmentSubmitResponse {
  assessment: Assessment;
  crisis_alert: boolean;
  crisis_message?: string;
}

export interface TransparencyView {
  turn_id: string;
  session_id: string;
  timestamp: string;
  response: string;
  model_version: string | null;
  boundary_state: string | null;
  retrieved_card_ids: string[] | null;
  safety: {
    route: string;
    allow_cbt: boolean;
    highest_risk: string;
    matched_card_ids: string[];
  } | null;
  intent: {
    module: string;
    subintent: string;
    confidence: number;
  } | null;
  critic: {
    passed: boolean;
    rewrites: number;
    used_fallback: boolean;
    findings_summary: string[];
  } | null;
  timing_ms: Record<string, number> | null;
}

export interface AuthUser {
  id: string;
  email: string;
  email_verified: boolean;
  created_at: string;
}

export interface LoginResponse {
  access_token: string;
  token_type: string;
  user: AuthUser;
}

