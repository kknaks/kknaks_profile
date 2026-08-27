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
  AdminCommitCalendar,
  AdminCommitsPage,
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
  AdminGateItem,
  AdminGateResponse,
  GatePayload,
  AdminProblem,
  AdminProject,
  AdminQueueItem,
  AdminQueueResponse,
  AdminRepo,
  RepoInput,
  GitTokenMeta,
  GithubOwnerOption,
  GithubRepoOption,
  QueueCreateInput,
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

/**
 * para 자산 경로 → 백엔드 `/api/assets` URL.
 *
 * 원장(md)이 자기 옆 `assets/` 에 이미지를 갖는다 — DB thumbnail 도 showcase.md
 * 의 상대참조도 para 상대경로다. para 밖(프론트 public 의 `/assets/profile/...`)은
 * 그대로 둔다.
 */
export function assetUrl(path: string): string {
  return path.startsWith("para/") ? `${API_BASE}/api/assets/${path}` : path;
}

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
  /** 인박스(queue) — 최신순 목록 + 상태별 counts. 행은 done 이 돼도 남는다(erd §queue). */
  queue: () => authFetch<AdminQueueResponse>("/api/admin/queue"),
  /** 캡처 — queue 행 생성(queued). kind 는 사람이 고른다(케이스 1). 중복 검사 없음. */
  createQueueItem: (body: QueueCreateInput) =>
    authFetch<AdminQueueItem>("/api/admin/queue", {
      method: "POST",
      body: JSON.stringify(body),
    }),
  /** failed → queued 되돌림 + 처리를 처음부터 다시 건다. 삭제는 없다(v1). */
  retryQueueItem: (id: number) =>
    authFetch<AdminQueueItem>(`/api/admin/queue/${id}/retry`, { method: "POST" }),
  /** 게이트 목록 — 기본은 열린 것 + 「승인됨·푸시 실패」(commitRef null).
   *  scope="all" 은 닫힌 게이트(자동 착지 기록·거절)까지 전부 — done 행 펼침 이력용. */
  gates: (scope?: "all") =>
    authFetch<AdminGateResponse>(
      scope === "all" ? "/api/admin/gates?scope=all" : "/api/admin/gates",
    ),
  gateDetail: (id: number) => authFetch<AdminGateItem>(`/api/admin/gates/${id}`),
  /** 승인 — 다듬은 payload 그대로. 착지·commit·push 까지 이 요청이 한다.
   *  응답의 pushError 가 차 있으면 푸시 실패 — [재시도] 대기다. */
  approveGate: (id: number, payload: GatePayload) =>
    authFetch<AdminGateItem>(`/api/admin/gates/${id}/approve`, {
      method: "POST",
      body: JSON.stringify({ payload }),
    }),
  /** 거절 — rejected 기록, queue 는 done. 이유는 안 적는다(v1). */
  rejectGate: (id: number) =>
    authFetch<AdminGateItem>(`/api/admin/gates/${id}/reject`, { method: "POST" }),
  /** 푸시 실패분 재시도 — 저장된 payload 로 착지부터 다시. */
  retryGatePush: (id: number) =>
    authFetch<AdminGateItem>(`/api/admin/gates/${id}/retry-push`, { method: "POST" }),
  /** 레포 — productTitle·projectTitle 은 선택 조인 파생 표시값. 수집 상태 포함. */
  repos: () => authFetch<{ items: AdminRepo[] }>("/api/admin/repos"),
  /** 연결은 product/project 둘 중 정확히 하나 — 아니면 서버가 422 로 막는다. */
  createRepo: (body: RepoInput) =>
    authFetch<AdminRepo>("/api/admin/repos", {
      method: "POST",
      body: JSON.stringify(body),
    }),
  /** **바뀐 필드만 담는다** — 안 보낸 것과 `null` 을 보낸 것은 다르다. */
  patchRepo: (id: number, body: RepoInput) =>
    authFetch<AdminRepo>(`/api/admin/repos/${id}`, {
      method: "PATCH",
      body: JSON.stringify(body),
    }),
  /** 커밋이 CASCADE 로 쓸려간다 — 잔디를 남기려면 삭제 대신 enabled=false. */
  deleteRepo: (id: number) =>
    authFetch<{ ok: boolean }>(`/api/admin/repos/${id}`, { method: "DELETE" }),
  /** 「지금 수집」 — 백그라운드로 걸고 202. started=false 면 이미 돌고 있다. */
  collectRepos: () =>
    authFetch<{ ok: boolean; started: boolean }>("/api/admin/repos/collect", {
      method: "POST",
    }),
  /** 레포 연결 모달의 owner 후보 — 폼 스코프대로만 온다(회사 제품 폼은 그 회사 것만).
   *  빈 items = 그 스코프에 쓸 토큰이 없다 — 설정 › 깃 토큰 안내를 띄운다. */
  githubOwners: (scope: { productId?: number; projectId?: number }) =>
    authFetch<{ items: GithubOwnerOption[] }>(
      scope.productId != null
        ? `/api/admin/github/owners?product_id=${scope.productId}`
        : `/api/admin/github/owners?project_id=${scope.projectId}`,
    ),
  /** GitHub 의 owner 레포 목록 — 최근 갱신순. tokenId 는 owner 후보가 데려온 토큰. */
  githubRepos: (owner: string, tokenId?: number | null) =>
    authFetch<{ items: GithubRepoOption[] }>(
      `/api/admin/github/repos?owner=${encodeURIComponent(owner)}${
        tokenId != null ? `&token_id=${tokenId}` : ""
      }`,
    ),
  /** 깃 토큰 — 응답에 토큰 원문·암호문은 절대 없다. 원문은 등록·교체 요청에만. */
  gitTokens: () => authFetch<{ items: GitTokenMeta[] }>("/api/admin/git-tokens"),
  createGitToken: (body: {
    kind: string;
    account: string;
    email: string;
    token: string;
    /** kind=company 면 필수 — 서버가 422 로 막는다. personal 은 무시. */
    companyId?: number | null;
  }) =>
    authFetch<GitTokenMeta>("/api/admin/git-tokens", {
      method: "POST",
      body: JSON.stringify(body),
    }),
  /** 토큰 값 교체 — 이직·만료 갱신. 행(레포 연결)은 유지된다. */
  replaceGitToken: (id: number, token: string) =>
    authFetch<{ ok: boolean }>(`/api/admin/git-tokens/${id}`, {
      method: "PUT",
      body: JSON.stringify({ token }),
    }),
  /** 부분 수정 — 보낸 필드만. enabled 토글 · companyId 연결(null = 해제). */
  patchGitToken: (id: number, body: { enabled?: boolean; companyId?: number | null }) =>
    authFetch<GitTokenMeta>(`/api/admin/git-tokens/${id}`, {
      method: "PATCH",
      body: JSON.stringify(body),
    }),
  /** 삭제 — 붙어 있던 레포는 무토큰이 된다(FK SET NULL). */
  deleteGitToken: (id: number) =>
    authFetch<{ ok: boolean }>(`/api/admin/git-tokens/${id}`, { method: "DELETE" }),
  /** 커밋 월 달력 — total·repos 는 그 달 전체, days 만 repoId 필터를 탄다. */
  commitCalendar: (year: number, month: number, repoId?: number | null) =>
    authFetch<AdminCommitCalendar>(
      `/api/admin/commits/calendar?year=${year}&month=${month}${
        repoId != null ? `&repo_id=${repoId}` : ""
      }`,
    ),
  /** 커밋 목록 — authored_at DESC 50행. day 는 KST 날짜(1~31) 필터. */
  commits: (q: {
    year: number;
    month: number;
    repoId?: number | null;
    day?: number | null;
    page?: number;
  }) =>
    authFetch<AdminCommitsPage>(
      `/api/admin/commits?year=${q.year}&month=${q.month}${
        q.repoId != null ? `&repo_id=${q.repoId}` : ""
      }${q.day != null ? `&day=${q.day}` : ""}&page=${q.page ?? 1}`,
    ),
  /** 하루 요약 재실행 — 백그라운드 202. 몇 초 뒤 달력 재조회로 결과를 본다. */
  summarizeDaily: (date: string) =>
    authFetch<{ ok: boolean; started: boolean }>(
      `/api/admin/daily/${date}/summarize`,
      { method: "POST" },
    ),
};
