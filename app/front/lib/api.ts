/**
 * 백엔드 API fetcher — 단일 entry point.
 *
 * **`?lang` 은 없다.** 한국어 하나만 담는다(`database.md` 서두). 표면 이름은
 * `erd.md` 의 테이블 이름을 따른다 — `profile` · `career` · `projects` ·
 * `notes` · `contents` · `algorithms`.
 *
 * 상세는 `slug` 로 조회한다. `erd.md` 에서 각 표의 UK 가 `slug` 다.
 */

import type {
  ActivityResponse,
  AdminCareer,
  AdminCompany,
  AdminContent,
  ContentInput,
  AdminEducation,
  EducationInput,
  AdminProduct,
  AdminAlgorithm,
  AlgorithmInput,
  AlgorithmDetailResponse,
  AlgorithmsResponse,
  CareerInput,
  CareerResponse,
  Company,
  CompanyInput,
  ContentDetailResponse,
  ContentsResponse,
  NoteDetailResponse,
  NotesResponse,
  AdminNote,
  NoteInput,
  NoteFileCandidate,
  AdminProblem,
  AdminProject,
  ProblemInput,
  ProductInput,
  Profile,
  ProjectInput,
  ProfileResponse,
  ProjectsResponse,
  SiteConfigItem,
  SiteResponse,
} from "./types";

const API_BASE =
  process.env.NEXT_PUBLIC_API_BASE ?? "http://localhost:48000";

async function get<T>(path: string): Promise<T> {
  const res = await fetch(API_BASE + path, { cache: "no-store" });
  if (!res.ok) {
    throw new Error(`API ${res.status}: ${path}`);
  }
  return (await res.json()) as T;
}

export const api = {
  site: () => get<SiteResponse>("/api/site"),
  profile: () => get<ProfileResponse>("/api/profile"),
  /** `career` 와 `education` 을 같이 내려준다 — 타임라인이 둘을 합쳐 그린다. */
  career: () => get<CareerResponse>("/api/career"),
  projects: () => get<ProjectsResponse>("/api/projects"),
  activity: () => get<ActivityResponse>("/api/activity"),
  contents: (limit = 5) => get<ContentsResponse>(`/api/contents?limit=${limit}`),
  contentDetail: (slug: string) =>
    get<ContentDetailResponse>(`/api/contents/${slug}`),
  notes: (limit = 50) => get<NotesResponse>(`/api/notes?limit=${limit}`),
  noteDetail: (slug: string) => get<NoteDetailResponse>(`/api/notes/${slug}`),
  algorithms: () => get<AlgorithmsResponse>("/api/algorithms"),
  algorithmDetail: (slug: string) =>
    get<AlgorithmDetailResponse>(`/api/algorithms/${slug}`),
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

// ── 어드민 CRUD ─────────────────────────────────────────────────────────────
export const adminApi = {
  /** site_config 행 그대로 — 공개 GET(/api/site)과 달리 key·note 가 보인다. */
  siteConfig: () => authFetch<{ items: SiteConfigItem[] }>("/api/admin/site-config"),
  /** **보낼 필드만 담는다** — 안 보낸 것과 `null` 을 보낸 것은 다르다. */
  patchProfile: (body: Partial<Omit<Profile, "id">>) =>
    authFetch<ProfileResponse>("/api/admin/profile", {
      method: "PATCH",
      body: JSON.stringify(body),
    }),
  /** key 는 경로로만 — 변경 불가. value 는 jsonb 그대로라 어떤 형이든 된다. */
  patchSiteConfig: (key: string, body: { value?: unknown; note?: string | null }) =>
    authFetch<SiteConfigItem>(
      `/api/admin/site-config/${encodeURIComponent(key)}`,
      { method: "PATCH", body: JSON.stringify(body) },
    ),
  /** 회사 — careerCount·period 는 career 에서 온 파생 표시값. */
  companies: () => authFetch<{ items: AdminCompany[] }>("/api/admin/companies"),
  createCompany: (body: CompanyInput) =>
    authFetch<Company>("/api/admin/companies", {
      method: "POST",
      body: JSON.stringify(body),
    }),
  patchCompany: (id: number, body: CompanyInput) =>
    authFetch<Company>(`/api/admin/companies/${id}`, {
      method: "PATCH",
      body: JSON.stringify(body),
    }),
  /** 역할이 붙어 있으면 서버가 409 로 막는다 — CASCADE 오발 방지. */
  deleteCompany: (id: number) =>
    authFetch<{ ok: boolean }>(`/api/admin/companies/${id}`, { method: "DELETE" }),
  /** 역할 — isCurrent·period 는 백엔드가 계산해 내려준 파생값. 재계산하지 않는다. */
  careers: () => authFetch<{ items: AdminCareer[] }>("/api/admin/careers"),
  createCareer: (body: CareerInput) =>
    authFetch<AdminCareer>("/api/admin/careers", {
      method: "POST",
      body: JSON.stringify(body),
    }),
  /** **바뀐 필드만 담는다** — 안 보낸 것과 `null`(endedOn 을 「현재」로) 은 다르다. */
  patchCareer: (id: number, body: CareerInput) =>
    authFetch<AdminCareer>(`/api/admin/careers/${id}`, {
      method: "PATCH",
      body: JSON.stringify(body),
    }),
  /** 제품이 붙어 있으면 서버가 409 로 막는다 — CASCADE 오발 방지. */
  deleteCareer: (id: number) =>
    authFetch<{ ok: boolean }>(`/api/admin/careers/${id}`, { method: "DELETE" }),
  /** 교육 — isCurrent·period 는 백엔드가 계산해 내려준 파생값. 재계산하지 않는다. */
  education: () => authFetch<{ items: AdminEducation[] }>("/api/admin/education"),
  createEducation: (body: EducationInput) =>
    authFetch<AdminEducation>("/api/admin/education", {
      method: "POST",
      body: JSON.stringify(body),
    }),
  /** **바뀐 필드만 담는다** — 안 보낸 것과 `null`(endedOn 을 「현재」로) 은 다르다. */
  patchEducation: (id: number, body: EducationInput) =>
    authFetch<AdminEducation>(`/api/admin/education/${id}`, {
      method: "PATCH",
      body: JSON.stringify(body),
    }),
  /** 가드 없음 — education 에는 아무것도 붙지 않는다. */
  deleteEducation: (id: number) =>
    authFetch<{ ok: boolean }>(`/api/admin/education/${id}`, { method: "DELETE" }),
  /** 회사 제품 — careerTitle·companyName 은 2단 조인 파생 표시값. 재계산하지 않는다. */
  products: () => authFetch<{ items: AdminProduct[] }>("/api/admin/products"),
  createProduct: (body: ProductInput) =>
    authFetch<AdminProduct>("/api/admin/products", {
      method: "POST",
      body: JSON.stringify(body),
    }),
  /** **바뀐 필드만 담는다** — 안 보낸 것과 `null` 을 보낸 것은 다르다. */
  patchProduct: (id: number, body: ProductInput) =>
    authFetch<AdminProduct>(`/api/admin/products/${id}`, {
      method: "PATCH",
      body: JSON.stringify(body),
    }),
  deleteProduct: (id: number) =>
    authFetch<{ ok: boolean }>(`/api/admin/products/${id}`, { method: "DELETE" }),
  /** 해결한 문제 — careerTitle·companyName·productTitle 은 조인 파생 표시값. */
  problems: () => authFetch<{ items: AdminProblem[] }>("/api/admin/problems"),
  createProblem: (body: ProblemInput) =>
    authFetch<AdminProblem>("/api/admin/problems", {
      method: "POST",
      body: JSON.stringify(body),
    }),
  /** **바뀐 필드만 담는다** — 안 보낸 것과 `null`(productId 연결 해제) 은 다르다. */
  patchProblem: (id: number, body: ProblemInput) =>
    authFetch<AdminProblem>(`/api/admin/problems/${id}`, {
      method: "PATCH",
      body: JSON.stringify(body),
    }),
  deleteProblem: (id: number) =>
    authFetch<{ ok: boolean }>(`/api/admin/problems/${id}`, { method: "DELETE" }),
  /** 개인 프로젝트 — slug 는 para/projects/summer-star/ 의 디렉토리명. */
  projects: () => authFetch<{ items: AdminProject[] }>("/api/admin/projects"),
  /** 디렉토리가 없으면 서버가 422 로 막는다 — md 가 먼저, DB 가 나중(케이스 2). */
  createProject: (body: ProjectInput) =>
    authFetch<AdminProject>("/api/admin/projects", {
      method: "POST",
      body: JSON.stringify(body),
    }),
  /** **바뀐 필드만 담는다** — 안 보낸 것과 `null` 을 보낸 것은 다르다. */
  patchProject: (id: number, body: ProjectInput) =>
    authFetch<AdminProject>(`/api/admin/projects/${id}`, {
      method: "PATCH",
      body: JSON.stringify(body),
    }),
  deleteProject: (id: number) =>
    authFetch<{ ok: boolean }>(`/api/admin/projects/${id}`, { method: "DELETE" }),
  /** 콘텐츠(영상 + 교안) — detailPath 는 para/resources/youtube/ 하위의 원장 md. */
  contents: () => authFetch<{ items: AdminContent[] }>("/api/admin/contents"),
  /** 원장 md 가 없으면 서버가 422 로 막는다 — 정보는 DB, 상세는 md. */
  createContent: (body: ContentInput) =>
    authFetch<AdminContent>("/api/admin/contents", {
      method: "POST",
      body: JSON.stringify(body),
    }),
  /** **바뀐 필드만 담는다** — 안 보낸 것과 `null` 을 보낸 것은 다르다. */
  patchContent: (id: number, body: ContentInput) =>
    authFetch<AdminContent>(`/api/admin/contents/${id}`, {
      method: "PATCH",
      body: JSON.stringify(body),
    }),
  deleteContent: (id: number) =>
    authFetch<{ ok: boolean }>(`/api/admin/contents/${id}`, { method: "DELETE" }),
  /** 노트 — 원장은 para/resources/note/ 의 md. 등록해야 사이트에 뜬다(케이스 4). */
  notes: () => authFetch<{ items: AdminNote[] }>("/api/admin/notes"),
  /** 등록 후보 파일 — 미등록 md + frontmatter 프리필 값. 서버는 읽기만 한다. */
  noteFiles: () =>
    authFetch<{ items: NoteFileCandidate[] }>("/api/admin/notes/files"),
  /** 실존 md 가 아니면 서버가 422 로 막는다 — 원장이 먼저, 등록이 나중(케이스 4). */
  createNote: (body: NoteInput) =>
    authFetch<AdminNote>("/api/admin/notes", {
      method: "POST",
      body: JSON.stringify(body),
    }),
  /** **바뀐 필드만 담는다** — 안 보낸 것과 `null` 을 보낸 것은 다르다. */
  patchNote: (id: number, body: NoteInput) =>
    authFetch<AdminNote>(`/api/admin/notes/${id}`, {
      method: "PATCH",
      body: JSON.stringify(body),
    }),
  /** 등록 해제일 뿐 — md 파일은 건드리지 않는다. 가드 없음. */
  deleteNote: (id: number) =>
    authFetch<{ ok: boolean }>(`/api/admin/notes/${id}`, { method: "DELETE" }),
  /** 알고리즘 — 메타만. 본문 단계는 detailPath 의 md 몫. today 행이 맨 앞에 온다. */
  algorithms: () => authFetch<{ items: AdminAlgorithm[] }>("/api/admin/algorithms"),
  /** detailPath 의 md 가 없으면 서버가 422 로 막는다 — md 가 먼저, DB 가 나중. */
  createAlgorithm: (body: AlgorithmInput) =>
    authFetch<AdminAlgorithm>("/api/admin/algorithms", {
      method: "POST",
      body: JSON.stringify(body),
    }),
  /** **바뀐 필드만 담는다.** today=true 는 서버가 이전 today 행을 내리고 올린다. */
  patchAlgorithm: (id: number, body: AlgorithmInput) =>
    authFetch<AdminAlgorithm>(`/api/admin/algorithms/${id}`, {
      method: "PATCH",
      body: JSON.stringify(body),
    }),
  deleteAlgorithm: (id: number) =>
    authFetch<{ ok: boolean }>(`/api/admin/algorithms/${id}`, { method: "DELETE" }),
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
  /** 활동 단위마다 한 줄. 활동이 0인 카테고리는 줄이 없다. 한국어 하나만 담는다. */
  summary: string[];
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
