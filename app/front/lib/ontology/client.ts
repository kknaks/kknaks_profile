/**
 * 온톨로지 데모 — **API 호출의 단일 경유지**.
 *
 * 화면은 `fetch` 를 직접 부르지 않는다. 실 API(WORK-002·003)가 붙으면
 * `NEXT_PUBLIC_ONTOLOGY_API_BASE` 한 줄로 전환되고 화면 코드는 그대로다.
 *
 * - env 가 비면 **mock 모드** — `lib/ontology/mock/*` 픽스처를 돌려준다.
 * - env 가 있으면 **실 API 모드** — SPEC-003 §4 경로를 그대로 부르고 쿠키로 인증한다.
 *
 * 응답 shape 는 두 모드가 같다(SPEC-003 계약). 화면에서 변환하지 않는다.
 */

import type {
  ApiLayer,
  ConversationResponse,
  ForecastResponse,
  GraphResponse,
  KpiCardsResponse,
  Layer,
  LayerTablesResponse,
  LayerRowsResponse,
  LineageResponse,
  RowValue,
  SessionResponse,
} from "./types";
import { OntologyApiError } from "./types";
import { mockKpiCards } from "./mock/kpi";
import { mockGraph } from "./mock/graph";
import { mockForecast } from "./mock/forecast";
import { mockLayerRows, mockLayerTables, mockTableExists } from "./mock/tables";
import { mockLineage } from "./mock/lineage";
import {
  mockCreateConversation,
  mockGetConversation,
  mockPostMessage,
  mockRetry,
} from "./mock/chat";

export const ONTOLOGY_API_BASE = (process.env.NEXT_PUBLIC_ONTOLOGY_API_BASE ?? "").replace(
  /\/+$/,
  "",
);

/** 실 API 가 아직 없다 — mock 으로 선행하고 스위치 하나로 넘긴다(WORK-004 §3). */
export const isMockMode = ONTOLOGY_API_BASE.length === 0;

/**
 * 프론트 게이트 마커 쿠키.
 *
 * 백엔드 세션 쿠키(`ontology_demo_sid`)는 httpOnly 라 미들웨어가 **같은 오리진일 때만**
 * 본다. 데모는 프론트(Vercel)와 API(홈서버)가 다른 오리진이므로, 화면 가드는 이
 * 마커 쿠키로 하고 **API 가드는 백엔드가 자기 쿠키로** 한다 — 가드가 양쪽에 있다는
 * SPEC-003 §5 의 요구는 그대로 지킨다.
 */
export const GATE_COOKIE = "ontology_demo_gate";
export const BACKEND_SESSION_COOKIE = "ontology_demo_sid";

const MOCK_LATENCY_MS = 120;

function delay<T>(value: T): Promise<T> {
  return new Promise((resolve) => setTimeout(() => resolve(value), MOCK_LATENCY_MS));
}

async function request<T>(path: string, init?: RequestInit): Promise<T> {
  const response = await fetch(`${ONTOLOGY_API_BASE}${path}`, {
    ...init,
    credentials: "include",
    headers: { "Content-Type": "application/json", ...(init?.headers ?? {}) },
  });

  if (!response.ok) {
    let detail = `HTTP_${response.status}`;
    try {
      const body = (await response.json()) as { detail?: string };
      if (body?.detail) detail = body.detail;
    } catch {
      // 본문이 JSON 이 아니면 상태 코드만으로 판정한다.
    }
    throw new OntologyApiError(detail, response.status);
  }

  return (await response.json()) as T;
}

/* ─────────────────────────── 세션(접속 게이트) ─────────────────────────── */

function readCookie(name: string): string | null {
  if (typeof document === "undefined") return null;
  const hit = document.cookie
    .split(";")
    .map((part) => part.trim())
    .find((part) => part.startsWith(`${name}=`));
  return hit ? decodeURIComponent(hit.slice(name.length + 1)) : null;
}

function writeGateCookie(): void {
  if (typeof document === "undefined") return;
  const maxAge = 60 * 60 * 24 * 30; // SPEC-003 §5 — 만료 30일
  const secure = window.location.protocol === "https:" ? "; Secure" : "";
  document.cookie = `${GATE_COOKIE}=1; Path=/; Max-Age=${maxAge}; SameSite=Lax${secure}`;
}

export function hasGateCookie(): boolean {
  return readCookie(GATE_COOKIE) !== null || readCookie(BACKEND_SESSION_COOKIE) !== null;
}

/* ─────────────────────────── 계층 쿼리 직렬화 ─────────────────────────── */

export interface LayerRowsQuery {
  limit?: number;
  offset?: number;
  filters?: { field: string; op: string; value: RowValue | RowValue[] }[];
}

/** `filters` 는 `/api/layers` 의 구조 그대로 URL 에 싣는다(SPEC-004 §4). */
export function serializeFilters(
  filters: { field: string; op: string; value: RowValue | RowValue[] }[] | undefined,
): string | null {
  if (!filters || filters.length === 0) return null;
  return JSON.stringify(filters);
}

export function parseFilters(
  raw: string | null,
): { field: string; op: string; value: RowValue | RowValue[] }[] | undefined {
  if (!raw) return undefined;
  try {
    const parsed = JSON.parse(raw) as unknown;
    if (!Array.isArray(parsed)) return undefined;
    return parsed as { field: string; op: string; value: RowValue | RowValue[] }[];
  } catch {
    return undefined;
  }
}

/* ─────────────────────────── 클라이언트 ─────────────────────────── */

export const ontologyApi = {
  /** 세션 유효 확인. mock 모드에서는 마커 쿠키만 본다. */
  async checkSession(): Promise<SessionResponse> {
    if (isMockMode) {
      if (!hasGateCookie()) throw new OntologyApiError("NO_SESSION", 401);
      return delay({ ok: true });
    }
    return request<SessionResponse>("/api/auth/session");
  },

  /**
   * 비밀번호 검증 → 세션 발급.
   *
   * mock 모드에서는 **아무 값이나 통과**시킨다(빈 입력은 no-op — 호출부가 선차단).
   * 검증 로직은 실 API 스위치에 물려 있어 env 만 채우면 그대로 진짜 검증이 된다.
   */
  async createSession(password: string): Promise<SessionResponse> {
    if (isMockMode) {
      if (password.trim().length === 0) throw new OntologyApiError("INVALID_PASSWORD", 401);
      writeGateCookie();
      return delay({ ok: true });
    }
    const result = await request<SessionResponse>("/api/auth/session", {
      method: "POST",
      body: JSON.stringify({ password }),
    });
    // 백 쿠키는 httpOnly·다른 오리진일 수 있어 미들웨어가 못 본다 — 화면 가드용 마커를 남긴다.
    writeGateCookie();
    return result;
  },

  async kpiCards(period?: string): Promise<KpiCardsResponse> {
    if (isMockMode) return delay(mockKpiCards(period));
    const query = period ? `?period=${encodeURIComponent(period)}` : "";
    return request<KpiCardsResponse>(`/api/kpi/cards${query}`);
  },

  /**
   * 그래프는 **최초 1회**만 받는다 — 판정 5종을 전부 요청하고 툴바 토글은
   * 클라이언트 필터다(SPEC-004 U-5 · AC-9).
   */
  async graph(): Promise<GraphResponse> {
    if (isMockMode) return delay(mockGraph());
    const verdicts = ["채택", "자동 확정", "선언", "보류", "기각"].join(",");
    return request<GraphResponse>(`/api/graph?verdicts=${encodeURIComponent(verdicts)}`);
  },

  async forecast(): Promise<ForecastResponse> {
    if (isMockMode) return delay(mockForecast());
    return request<ForecastResponse>("/api/forecast");
  },

  async layerTables(layer: ApiLayer): Promise<LayerTablesResponse> {
    if (isMockMode) return delay({ layer, tables: mockLayerTables(layer) });
    return request<LayerTablesResponse>(`/api/layers/${layer}/tables`);
  },

  async layerRows(layer: ApiLayer, table: string, query: LayerRowsQuery = {}): Promise<LayerRowsResponse> {
    const limit = query.limit ?? 50;
    const offset = query.offset ?? 0;
    if (isMockMode) {
      if (!mockTableExists(layer, table)) throw new OntologyApiError("UNKNOWN_TABLE", 404);
      const rows = mockLayerRows(layer, table, { limit, offset, filters: query.filters });
      if (!rows) throw new OntologyApiError("UNKNOWN_TABLE", 404);
      return delay(rows);
    }
    const params = new URLSearchParams({ limit: String(limit), offset: String(offset) });
    const filters = serializeFilters(query.filters);
    if (filters) params.set("filters", filters);
    return request<LayerRowsResponse>(`/api/layers/${layer}/${table}?${params.toString()}`);
  },

  async lineage(layer: ApiLayer, table: string): Promise<LineageResponse> {
    if (isMockMode) return delay(mockLineage(layer, table));
    return request<LineageResponse>(`/api/layers/${layer}/${table}/lineage`);
  },

  async createConversation(question: string): Promise<ConversationResponse> {
    if (isMockMode) return delay(mockCreateConversation(question));
    return request<ConversationResponse>("/api/chat/conversations", {
      method: "POST",
      body: JSON.stringify({ question }),
    });
  },

  /** 폴링 대상 — assistant 가 `pending` 인 동안 2초 간격(SPEC-003 §4). */
  async getConversation(id: string): Promise<ConversationResponse> {
    if (isMockMode) return delay(mockGetConversation(id));
    return request<ConversationResponse>(`/api/chat/conversations/${id}`);
  },

  async sendMessage(id: string, question: string): Promise<ConversationResponse> {
    if (isMockMode) return delay(mockPostMessage(id, question));
    return request<ConversationResponse>(`/api/chat/conversations/${id}/messages`, {
      method: "POST",
      body: JSON.stringify({ question }),
    });
  },

  async retryMessage(id: string, messageId: string): Promise<ConversationResponse> {
    if (isMockMode) return delay(mockRetry(id, messageId));
    return request<ConversationResponse>(
      `/api/chat/conversations/${id}/messages/${messageId}/retry`,
      { method: "POST" },
    );
  },
};

/** 채팅 폴링 간격 — 스트리밍이 아니다(SPEC-003 · 디자인 07). */
export const CHAT_POLL_INTERVAL_MS = 2000;

/** 질문 상한 — 초과는 컴포저가 선차단한다(SPEC-003 Validation). */
export const QUESTION_MAX_LENGTH = 1000;
