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
