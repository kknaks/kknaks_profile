/**
 * 백엔드 API fetcher — 단일 entry point. lang 상태를 받아 ?lang= 쿼리로 전달.
 * 페이지(서버 컴포넌트)에서 직접 호출. CSR 컴포넌트는 useEffect + lang prop으로 refetch.
 */

import type { Lang } from "./i18n";
import type {
  ActivityResponse,
  AlgorithmDetailResponse,
  AlgorithmsResponse,
  CareerResponse,
  ContentDetailResponse,
  ContentsResponse,
  GraphResponse,
  MeResponse,
  NoteDetail,
  NoteRecent,
  NotesGraphResponse,
  ProjectsResponse,
  SiteResponse,
} from "./types";

const API_BASE =
  process.env.NEXT_PUBLIC_API_BASE ?? "http://localhost:48000";

async function get<T>(path: string, lang?: Lang): Promise<T> {
  const url = new URL(API_BASE + path);
  if (lang) url.searchParams.set("lang", lang);
  const res = await fetch(url, { cache: "no-store" });
  if (!res.ok) {
    throw new Error(`API ${res.status}: ${path}`);
  }
  return (await res.json()) as T;
}

export const api = {
  site: (lang: Lang) => get<SiteResponse>("/api/site", lang),
  me: (lang: Lang) => get<MeResponse>("/api/me", lang),
  career: (lang: Lang) => get<CareerResponse>("/api/career", lang),
  projects: (lang: Lang) => get<ProjectsResponse>("/api/projects", lang),
  activity: (lang: Lang) => get<ActivityResponse>("/api/activity", lang),
  notesGraph: () => get<NotesGraphResponse>("/api/notes/graph"),
  graph: (lang?: Lang) => get<GraphResponse>("/api/graph", lang),
  notesRecent: (lang: Lang, limit = 5) =>
    get<{ "notes.recent[]": NoteRecent[] }>(
      `/api/notes/recent?limit=${limit}`,
      lang,
    ),
  noteDetail: (id: string, lang: Lang) =>
    get<{ "notes.detail": NoteDetail }>(`/api/notes/${id}`, lang),
  notesSearch: (q: string, lang: Lang) =>
    get<{ "notes.recent[]": NoteRecent[] }>(
      `/api/notes/search?q=${encodeURIComponent(q)}`,
      lang,
    ),
  contents: (lang: Lang, limit = 5) =>
    get<ContentsResponse>(`/api/contents?limit=${limit}`, lang),
  contentDetail: (id: string, lang: Lang) =>
    get<ContentDetailResponse>(`/api/contents/${id}`, lang),
  algorithms: (lang: Lang) => get<AlgorithmsResponse>("/api/algorithms", lang),
  algorithmDetail: (id: string, lang: Lang) =>
    get<AlgorithmDetailResponse>(`/api/algorithms/${id}`, lang),
};

// ── 관리자 인증 (KDEV-SPEC-006) ────────────────────────────────────────────
// 세션은 httpOnly 쿠키 → 브라우저가 쿠키를 붙이려면 credentials: "include" 필수.
export type AdminUser = { username: string; role: string };

export class AuthError extends Error {
  constructor(public status: number, message: string) {
    super(message);
  }
}

async function authFetch<T>(path: string, init?: RequestInit): Promise<T> {
  const res = await fetch(API_BASE + path, {
    ...init,
    credentials: "include",
    cache: "no-store",
    headers: { "Content-Type": "application/json", ...(init?.headers ?? {}) },
  });
  if (!res.ok) {
    let detail = `auth ${res.status}`;
    try {
      detail = (await res.json())?.detail ?? detail;
    } catch {
      /* 본문 없음 */
    }
    throw new AuthError(res.status, detail);
  }
  return (await res.json()) as T;
}

export const authApi = {
  login: (username: string, password: string) =>
    authFetch<{ user: AdminUser }>("/api/auth/login", {
      method: "POST",
      body: JSON.stringify({ username, password }),
    }),
  logout: () => authFetch<{ ok: boolean }>("/api/auth/logout", { method: "POST" }),
  me: () => authFetch<{ user: AdminUser }>("/api/auth/me"),
};

// ── 승인 큐 (KDEV-SPEC-007/008/009 · WORK-014 P4) ──────────────────────────
// 큐 표면 전체가 admin 뒤에 있다 — 승인 전 초안이 여기 있기 때문이다.
export type QueueItem = {
  id: number;
  source_kind: string;
  source_url: string | null;
  note: string | null;
  channel: string;
  status: string;
  submitted_by: string | null;
  submitted_at: string | null;
  published_at: string | null;
  commit_ref: string | null;
};

export type Preparation = {
  id: number;
  version: number;
  status: string;
  payload: Record<string, unknown> | null;
  created_at: string | null;
};

export type AiTask = {
  id: number;
  kind: string;
  status: string;
  retry_of_task_id: number | null;
  error_code: string | null;
  error_message: string | null;
  created_at: string | null;
};

export type QueueItemDetail = QueueItem & {
  preparations: Preparation[];
  ai_tasks: AiTask[];
};

export type RouteResult = {
  destinations: {
    reference: { enabled: boolean; group?: string };
    concept: { enabled: boolean };
    derived: { enabled: boolean };
  };
  exclusive: null | "inbox_hold" | "discard";
  rationale?: string;
};

export type Revision = {
  id: number;
  version: number;
  status: string;
  payload: RouteResult | null;
  parent_revision_id: number | null;
  feedback_id: number | null;
  created_at: string | null;
};

export type Gate = {
  id: number;
  stage_name: string;
  stage_no: number;
  status: string;
  active_revision_id: number | null;
  approved_revision_id: number | null;
  revisions: Revision[];
  feedbacks: { id: number; target_revision_id: number | null; body: string; status: string }[];
};

/** 백엔드가 `{code, message}` 로 주는 실패를 그대로 들고 온다 — 화면 문구가 코드별로 다르다. */
export class QueueError extends Error {
  constructor(
    public status: number,
    public code: string,
    message: string,
    public detail?: unknown,
  ) {
    super(message);
  }
}

async function queueFetch<T>(path: string, init?: RequestInit): Promise<T> {
  const res = await fetch(API_BASE + path, {
    ...init,
    credentials: "include",
    cache: "no-store",
    headers: { "Content-Type": "application/json", ...(init?.headers ?? {}) },
  });
  if (!res.ok) {
    let code = `HTTP_${res.status}`;
    let message = `요청에 실패했습니다 (${res.status})`;
    let detail: unknown;
    try {
      detail = (await res.json())?.detail;
      if (typeof detail === "string") message = detail;
      else if (detail && typeof detail === "object") {
        code = (detail as { code?: string }).code ?? code;
        message = (detail as { message?: string }).message ?? message;
      }
    } catch {
      /* 본문 없음 */
    }
    throw new QueueError(res.status, code, message, detail);
  }
  return (await res.json()) as T;
}

const QUEUE = "/api/admin/queue";

export const queueApi = {
  /** 선택지는 서버가 준다 — `persona/_meta.yaml` 이 SoT 라 프론트에 목록을 복사하지 않는다. */
  meta: () =>
    queueFetch<{
      reference_groups: string[];
      pipelines: Record<string, { name: string; kind: string; optional: boolean }[]>;
    }>(`${QUEUE}/meta`),
  list: (includeDone = false) =>
    queueFetch<{ items: QueueItem[]; counts: Record<string, number> }>(
      `${QUEUE}/items?include_done=${includeDone}`,
    ),
  detail: (id: number) => queueFetch<QueueItemDetail>(`${QUEUE}/items/${id}`),
  create: (body: { source_url?: string | null; note?: string | null; allow_republish?: boolean }) =>
    queueFetch<{ outcome: string; item_id: number }>(`${QUEUE}/items`, {
      method: "POST",
      body: JSON.stringify(body),
    }),
  updateNote: (id: number, note: string) =>
    queueFetch<QueueItem>(`${QUEUE}/items/${id}`, {
      method: "PATCH",
      body: JSON.stringify({ note }),
    }),
  retryPrepare: (id: number) =>
    queueFetch<{ status: string; version: number | null; error_code: string | null }>(
      `${QUEUE}/items/${id}/prepare`,
      { method: "POST" },
    ),
  remove: (id: number) =>
    queueFetch<{ id: number; status: string }>(`${QUEUE}/items/${id}`, { method: "DELETE" }),
  gates: (id: number) => queueFetch<{ gates: Gate[] }>(`${QUEUE}/items/${id}/gates`),
  feedback: (gateId: number, body: string) =>
    queueFetch<{ feedback_id: number; gate_status: string }>(`${QUEUE}/gates/${gateId}/feedback`, {
      method: "POST",
      body: JSON.stringify({ body }),
    }),
  regenerate: (gateId: number) =>
    queueFetch<{ gate_status: string; revision: Revision }>(
      `${QUEUE}/gates/${gateId}/regenerate`,
      { method: "POST" },
    ),
  retryGate: (gateId: number) =>
    queueFetch<{ gate_status: string; revision: Revision }>(`${QUEUE}/gates/${gateId}/retry`, {
      method: "POST",
    }),
  approve: (gateId: number, payload: RouteResult | null, expectedRevisionId: number | null) =>
    queueFetch<{
      gate_status: string;
      item_status: string;
      route_outcome: string | null;
      revision: Revision;
    }>(`${QUEUE}/gates/${gateId}/approve`, {
      method: "POST",
      body: JSON.stringify({ payload, expected_revision_id: expectedRevisionId }),
    }),
};
