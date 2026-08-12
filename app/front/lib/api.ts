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
  MeResponse,
  NoteDetail,
  NoteRecent,
  NotesGraphResponse,
  PostDetailResponse,
  PostsResponse,
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
  posts: (lang: Lang, limit = 50) =>
    get<PostsResponse>(`/api/posts?limit=${limit}`, lang),
  postDetail: (id: string, lang: Lang) =>
    get<PostDetailResponse>(`/api/posts/${id}`, lang),
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

/** 발행 결과 — 성공만이 아니라 **거부와 실패도** 남는다 (KDEV-SPEC-010). */
export type ApplyResult = {
  id: number;
  status: string;
  commit_ref: string | null;
  violations: { rule: string; path?: string; detail?: string }[] | null;
  error_code: string | null;
  error_message: string | null;
  created_at: string | null;
};

export type QueueItemDetail = QueueItem & {
  preparations: Preparation[];
  ai_tasks: AiTask[];
  apply_results: ApplyResult[];
};

export type RouteResult = {
  destinations: {
    reference: { enabled: boolean };
    concept: { enabled: boolean };
    derived: { enabled: boolean };
  };
  exclusive: null | "inbox_hold" | "discard";
  rationale?: string;
};

/** 노트를 만드는 스테이지(source_note·concept·derived)의 산출물. AI 가 md 전문을 낸다. */
export type NotePayload = {
  filename_stem: string;
  content: string;
  /** 경로는 시스템이 조립한다 — AI 는 stem 만 낸다. */
  target_path?: string;
};

/** concept 게이트 산출물. `mode` 가 신규/보충을 가른다. */
export type ConceptResult = {
  mode: "create" | "supplement";
  stem: string;
  /** 무엇 때문에 기존 개념과 같다고 봤는지. create 면 null. */
  matched_by: string | null;
  content: string;
  excluded: boolean;
  target_path?: string;
  /** 보충일 때만. **사라지는 줄**이 승인 판단의 핵심이다. */
  diff?: string;
};

export type ConceptPayload = { concepts: ConceptResult[] };

/** 잔디 daily 초안. `counts` 는 **코드가 센 값**이라 화면이 고치지 않는다. */
export type DailyDraft = {
  date: string;
  counts: { commit?: number; note?: number; study?: number };
  /** 활동 단위마다 한 줄. 활동이 0인 카테고리는 줄이 없다. */
  summary: { ko: string[]; en: string[] };
  body: string;
  target_path?: string;
};

/**
 * career 갱신안. **본문 전문**이 온다 — 문장으로 나뉘어 있지 않다.
 *
 * 줄 단위 승인은 화면이 쪼개고 승인 시 남은 줄만 다시 합쳐 보낸다. 쪼개는 것은
 * 보여주기 위한 일이라 서버가 알 이유가 없고, 서버는 이미 "본문 전문 교체"로 서 있다.
 */
export type CareerDraft = {
  changed: boolean;
  stem?: string;
  content?: string;
  /** 기존 본문. **무엇이 바뀌었는지** 를 보여주려면 비교 대상이 있어야 한다. */
  previous_content?: string;
  target_path?: string;
};

/**
 * 조사가 얼마나 온전했는지. **`counts` 와 같이 코드가 센 값**이라 화면이 고치지 않는다.
 *
 * 이게 없으면 서술이 얕을 때 **자료가 부족했던 것인지 그날 일이 적었던 것인지**
 * 사람이 구분할 수 없다. `failed` 는 클론·fetch 에서 빠진 것이고 `missing` 은
 * 조사까지 갔다가 결과가 안 돌아온 것이라 — 다른 자리의 실패다.
 */
export type DailyCollection = {
  done: number;
  total: number;
  missing: string[];
  failed: { repo?: string; code?: string; message?: string }[];
  truncated: Record<string, { diff_bytes?: number; commits?: number }>;
  /** `detail` 오타로 갈 곳이 없어진 career stem — 그 레포의 작업이 어디에도 안 실린다. */
  career_missing?: string[];
};

/** 잔디 게이트 산출물 — 게이트 하나가 목적지 셋을 낸다. */
export type DailyPayload = {
  daily: DailyDraft;
  career: CareerDraft;
  concepts: ConceptResult[];
  /** 예전 리비전에는 없다 — 화면이 없으면 그리지 않는다. */
  collection?: DailyCollection;
};

export type GatePayload = RouteResult | NotePayload | ConceptPayload | DailyPayload;

export type Revision = {
  id: number;
  version: number;
  status: string;
  payload: GatePayload | null;
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
  /** 파이프라인 정의 — 정의가 코드에 있으므로 프론트에 복사해 두지 않는다. */
  meta: () =>
    queueFetch<{
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
  /** 발행 재시도 — **AI 를 다시 부르지 않는다.** 저장된 계획으로 다시 쓴다(DEC-012 D5). */
  retryPublish: (id: number) =>
    queueFetch<{ item_status: string; status: string; error_code: string | null }>(
      `${QUEUE}/items/${id}/publish`,
      { method: "POST" },
    ),
  remove: (id: number) =>
    queueFetch<{ id: number; status: string }>(`${QUEUE}/items/${id}`, { method: "DELETE" }),
  gates: (id: number) => queueFetch<{ gates: Gate[] }>(`${QUEUE}/items/${id}/gates`),
  /** 목적지 재검토 — 유일한 역방향 전이(DEC-011 D5). 뒤 게이트는 무효화되지만 기록은 남는다. */
  reopenRoute: (itemId: number) =>
    queueFetch<{ gate_id: number; gate_status: string; item_status: string }>(
      `${QUEUE}/items/${itemId}/reopen-route`,
      { method: "POST" },
    ),
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
  approve: (gateId: number, payload: GatePayload | null, expectedRevisionId: number | null) =>
    queueFetch<{
      gate_status: string;
      item_status: string;
      route_outcome: string | null;
      next_stage: string | null;
      revision: Revision;
    }>(`${QUEUE}/gates/${gateId}/approve`, {
      method: "POST",
      body: JSON.stringify({ payload, expected_revision_id: expectedRevisionId }),
    }),
};

/* ── 제품 레지스트리 (KDEV-WORK-018 P4 / KDEV-SPEC-014) ────────────────────
 *
 * 표면이 admin 뒤에 있는 이유는 큐와 같다 — 추적 대상과 토큰 종류가 드러난다.
 */

const PRODUCTS = "/api/admin/products";

export type RegistryRow = {
  id: number;
  slug: string;
  type: "company" | "studio";
  detail: string | null;
  product_slug: string | null;
  account: string;
  enabled: boolean;
  last_fetched_at: string | null;
  last_error: string | null;
  /** `product_slug` 가 가리키는 디렉토리가 실재하는가. **경고이지 차단이 아니다.** */
  product_exists: boolean;
  /** 공개 카드 노출 값. 파일이 SoT 라 읽기 전용이고, 카드가 없으면 `null`. */
  card_visible: boolean | null;
};

export type ProductOptions = {
  products: string[];
  categories: string[];
  statuses: string[];
  careers: string[];
};

export type DiscoveredRow = {
  slug: string;
  account: string;
  pushed_at: string | null;
  private: boolean;
};

export type CardInput = {
  title: { ko: string; en: string };
  summary: { ko: string; en: string };
  category: string;
  status: string;
  stack: string[];
  date?: string | null;
};

export type RegisterBody = {
  repo: string;
  type: "company" | "studio";
  detail?: string | null;
  product_slug?: string | null;
  card?: CardInput | null;
};

export const productsApi = {
  list: () => queueFetch<{ items: RegistryRow[] }>(PRODUCTS),
  options: () => queueFetch<ProductOptions>(`${PRODUCTS}/options`),
  /** 실패해도 200 이다 — 배너만 실패하고 표는 정상 표시된다. */
  undiscovered: () =>
    queueFetch<{
      items: DiscoveredRow[];
      hidden_old: number;
      window_days: number;
      error: string | null;
    }>(`${PRODUCTS}/undiscovered`),
  register: (body: RegisterBody) =>
    queueFetch<RegistryRow>(PRODUCTS, {
      method: "POST",
      body: JSON.stringify(body),
    }),
  /** **보낼 필드만 담는다** — 안 보낸 것과 `null` 을 보낸 것은 다르다. */
  patch: (id: number, body: Partial<Pick<RegistryRow, "detail" | "product_slug" | "enabled">>) =>
    queueFetch<RegistryRow>(`${PRODUCTS}/${id}`, {
      method: "PATCH",
      body: JSON.stringify(body),
    }),
  /** 이미 있는 제품에 공개 카드를 붙인다. 등록과 달리 **제품 디렉토리가 있어야** 한다. */
  addCard: (id: number, card: CardInput) =>
    queueFetch<RegistryRow>(`${PRODUCTS}/${id}/card`, {
      method: "POST",
      body: JSON.stringify(card),
    }),
  /** **DB 가 아니라 `showcase.md` 를 고친다** — 파일이 SoT 다(KDEV-DEC-017 D18). */
  setVisible: (id: number, value: boolean) =>
    queueFetch<RegistryRow>(`${PRODUCTS}/${id}/visible`, {
      method: "POST",
      body: JSON.stringify({ value }),
    }),
  sync: (id: number) =>
    queueFetch<{ row: RegistryRow; ok: boolean; code: string | null; message: string | null }>(
      `${PRODUCTS}/${id}/sync`,
      { method: "POST" },
    ),
};
