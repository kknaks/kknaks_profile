/**
 * 백엔드 API fetcher — 단일 entry point. lang 상태를 받아 ?lang= 쿼리로 전달.
 * 페이지(서버 컴포넌트)에서 직접 호출. CSR 컴포넌트는 useEffect + lang prop으로 refetch.
 */

import type { Lang } from "./i18n";
import type {
  ActivityResponse,
  CareerResponse,
  ContentDetailResponse,
  ContentsResponse,
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
};
