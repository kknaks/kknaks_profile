/**
 * 백엔드 API 응답 타입. **근거는 `erd.md` 다.**
 *
 * 규칙 셋.
 *
 * 1. **한국어 하나만 담는다.** `{ko, en}` 축은 없다(`database.md` 서두).
 * 2. **상세 본문은 DB 에 없다.** DB 는 `detail_path` 만 갖고, 백엔드가 그 md 를 읽어
 *    `body` 로 내려준다(`erd.md` §상세 본문은 DB 에 없다). 프론트 입장에선 옛날과 같다.
 * 3. 컬럼이 아닌 필드에는 **무엇에서 파생됐는지** 를 주석으로 적는다. erd 에 대응이
 *    없으면 「대응 컬럼 없음」이라고 적고 추측으로 메우지 않는다.
 *
 * 날짜는 전부 `date` 컬럼의 문자열 표현이다(`YYYY-MM-DD` 를 가정).
 */

/* ══════════════════════════════════════════════════════════════════════════
 * profile — erd.md §profile. 루트 테이블.
 * ══════════════════════════════════════════════════════════════════════════ */

export type HeadlineTone = "muted" | "default" | "accent";

/** `profile.hero_headline` jsonb 의 한 항목 — `[{text, tone}]`. */
export interface HeadlineLine {
  text: string;
  tone: HeadlineTone;
}

/** `profile.hero_terminal` jsonb 의 한 항목 — `[{prompt, output[]}]`. */
export interface HeroTerminalLine {
  prompt: string;
  output: string[];
}

/** `profile.cards` jsonb 의 한 항목 — `[{title, body}]`, /about 카드 4개. */
export interface ProfileCard {
  title: string;
  body: string;
}

/**
 * 신원·연락·스택만 — **내 개인 정보**다. 표면에 뜨는 문구(히어로·소개·카드)는
 * 전부 `site_config`(`SiteResponse`)로 갔다. 1인 사이트라 사람/페이지 구분이
 * 무의미해서 그렇게 갈랐다(erd.md §profile · §site_config).
 */
export interface Profile {
  id: number;

  // 신원 — /about 상단.
  handle: string;
  name: string;
  /** 직함. 권한(`users.system_role`)과 다른 값이다. */
  role: string;
  years?: string | null;
  location?: string | null;
  focus?: string | null;
  avatarUrl?: string | null;

  // 연락 — /about + footer.
  email: string;
  github?: string | null;
  linkedin?: string | null;

  stack: string[];
}

export interface ProfileResponse {
  profile: Profile;
}

/* ══════════════════════════════════════════════════════════════════════════
 * career · education — erd.md §career, §education.
 * ══════════════════════════════════════════════════════════════════════════ */

/**
 * `career` 와 `education` 은 컬럼이 같다(erd.md). 다른 것은 `education` 에
 * `repo` 가 붙지 않는다는 점뿐이고, 그것은 이 표면에 드러나지 않는다.
 */
interface TimelineEntryBase {
  id: number;
  org: string;
  title: string;
  location?: string | null;

  startedOn: string;
  /** `NULL` 이면 현재 역할. */
  endedOn?: string | null;

  summary?: string | null;
  stack: string[];

  /** `detail_path` 가 가리키는 md 를 백엔드가 읽어 내려준 것. 없으면 상세 없음. */
  body?: string | null;

  /**
   * ── 아래 둘은 **DB 컬럼이 아니다**(erd.md §career, database.md §파생으로 뺀 것 셋).
   *
   * | 값          | 파생식                        |
   * |-------------|-------------------------------|
   * | `isCurrent` | `ended_on IS NULL`            |
   * | `period`    | `started_on`·`ended_on` 의 렌더 |
   * | (정렬)      | `started_on DESC`             |
   *
   * **백엔드가 계산해 내려준다고 가정한다.** 프론트에서 다시 계산하지 않는다 —
   * 두 곳에서 계산하면 형식이 갈린다.
   */
  isCurrent: boolean;
  /** 예: `2026.02 — present`. 표시 형식이라 정렬에 쓰지 않는다. */
  period: string;
}

/** 한 행 = 직장에서의 역할 하나. 같은 회사에서 직무가 바뀌면 행이 하나 더 생긴다. */
export type CareerItem = TimelineEntryBase;

/** 한 행 = 교육과정 하나. 부트캠프·학력. */
export type EducationItem = TimelineEntryBase;

/**
 * `/career` 타임라인은 `career` 와 `education` 을 **합쳐** `startedOn DESC` 로
 * 나열한다(database.md §화면에서는 합친다). 화면은 둘을 구분해 보여주지 않는다.
 */
export type TimelineItem = CareerItem | EducationItem;

export interface CareerResponse {
  "career[]": CareerItem[];
  "education[]": EducationItem[];
  /** **erd.md 에 대응 컬럼 없음.** 화면 상단 요약 문구·집계. */
  career?: {
    subtitle?: string;
    totalRoles?: string;
    totalYears?: string;
    focus?: string;
  };
}

/* ══════════════════════════════════════════════════════════════════════════
 * product · project — erd.md §product, §project.
 *
 * 옛 `projects` 가 둘로 갈렸다. `product` 는 회사 것이라 `career` 에 속하고,
 * `project` 는 혼자 만든 것이라 `profile` 에 바로 닿는다(database.md §project).
 * ══════════════════════════════════════════════════════════════════════════ */

export type WorkStatus = "live" | "wip" | "archived";

interface WorkBase {
  id: number;
  /** UK. 라우팅 키다 — 옛 `id` 자리. */
  slug: string;
  title: string;
  summary?: string | null;
  category?: string | null;
  status?: WorkStatus | null;
  startedOn?: string | null;
  stack: string[];
  thumbnail?: string | null;

  /** `detail_path` 가 가리키는 md 를 백엔드가 읽어 내려준 것. */
  body?: string | null;

  /**
   * `visible` 은 컬럼이지만 여기 담지 않는다 — 공개 API 가 걸러 낸 뒤 내려준다고 본다.
   * 어드민 표면이 서면 그쪽 타입이 따로 갖는다.
   */
}

/** 회사에서 만들어 파는 것. `career` 에 속한다. */
export interface ProductItem extends WorkBase {
  careerId: number;
  /** `product.links` jsonb — `{site, docs}`. */
  links?: { site?: string; docs?: string } | null;
}

/** 혼자 만든 것. `career_id` 가 없다 — 소속이 없어서지 비어 있는 게 아니다. */
export interface ProjectItem extends WorkBase {
  /** `project.links` jsonb — `{repo, site, store}`. */
  links?: { repo?: string; site?: string; store?: string } | null;
}

/**
 * **문서가 어긋난다.** `database.md` §진행 표는 `/projects` 가 `product` · `project`
 * 둘을 읽는다고 하고, 같은 문서 §project 는 「`/projects` 는 혼자 만든 것들이고
 * 회사 제품은 거기 안 뜬다」고 한다. 화면이 후자로 서 있으므로 `project` 만 담는다.
 * `product` 를 어디에 띄울지는 정해지지 않았다.
 */
export interface ProjectsResponse {
  "projects[]": ProjectItem[];
  projects?: {
    /** **erd.md 에 대응 컬럼 없음.** 화면 머리말 문구. */
    subtitle?: string;
    totalCount?: number;
    /** `GROUP BY category` 의 결과(database.md §product). */
    categories?: { id: string; label: string; count: number }[];
  };
}

/* ══════════════════════════════════════════════════════════════════════════
 * note — erd.md §note. 내가 쓴 글. 원장은 `para/resources/note/`.
 * ══════════════════════════════════════════════════════════════════════════ */

/** 이전/다음 글은 컬럼이 아니다 — `published_on` 정렬의 이웃이다(erd.md §content). */
export interface Neighbor {
  slug: string;
  title: string;
}

export interface NoteItem {
  id: number;
  slug: string;
  title: string;
  summary?: string | null;
  tags: string[];
  publishedOn?: string | null;
}

export interface NoteDetail extends NoteItem {
  /** `detail_path` md 전문. */
  body: string;
  newer: Neighbor | null;
  older: Neighbor | null;
}

export interface NotesResponse {
  "notes[]": NoteItem[];
  notes?: {
    /** **erd.md 에 대응 컬럼 없음.** 화면 머리말 문구. */
    subtitle?: string;
    totalCount?: number;
  };
}

export interface NoteDetailResponse {
  "notes.detail": NoteDetail;
}

/* ══════════════════════════════════════════════════════════════════════════
 * content — erd.md §content. 영상 + 교안. 원장은 `para/resources/youtube/`.
 *
 * `note` 와 표면 모양이 같고 **영상 세 필드만 다르다.**
 * ══════════════════════════════════════════════════════════════════════════ */

export interface ContentItem {
  id: number;
  /** 예: `C-025`. */
  slug: string;
  title: string;
  summary?: string | null;

  youtubeId: string;
  /** 예: `3:58`. */
  duration?: string | null;
  /** 출처 채널. */
  speaker?: string | null;

  tags: string[];
  publishedOn?: string | null;
}

export interface ContentDetail extends ContentItem {
  /**
   * `detail_path` md 전문.
   *
   * 옛 frontmatter 의 `concept[]`(요지 6문장)은 **컬럼이 아니다** — 본문에 속하므로
   * 여기 안에 있다(erd.md §content). 화면이 따로 조립하지 않는다.
   */
  body: string;
  newer: Neighbor | null;
  older: Neighbor | null;
}

export interface ContentsResponse {
  "contents[]": ContentItem[];
  contents?: {
    /** **erd.md 에 대응 컬럼 없음.** 화면 머리말 문구. */
    subtitle?: string;
    intro?: string;
    totalCount?: number;
  };
}

export interface ContentDetailResponse {
  "contents.detail": ContentDetail;
}

/* ══════════════════════════════════════════════════════════════════════════
 * algorithm — erd.md §algorithm. 원장은 `para/resources/algorithms/`.
 * ══════════════════════════════════════════════════════════════════════════ */

export type AlgoDifficulty = "easy" | "medium" | "hard";

/**
 * 출처. jsonb 로 접지 않는다 — 플랫폼·번호로 거르고 싶어지기 때문이다(erd.md).
 * `source_platform` · `source_number` · `source_url` · `curated_in` 을 묶은 것이다.
 */
export interface AlgorithmSource {
  platform: string;
  number?: number | null;
  url?: string | null;
  /** `neetcode150` · `blind75`. */
  curatedIn?: string[];
}

export interface AlgorithmListItem {
  id: number;
  /** 예: `a-001-two-sum`. */
  slug: string;
  title: string;
  difficulty: AlgoDifficulty;
  source: AlgorithmSource;
  tags: string[];
  /** 「오늘의 문제」. DB 가 하나뿐임을 강제한다(`uq_algorithm_today`). */
  today: boolean;
  publishedOn?: string | null;

  /**
   * **erd.md 에 대응 컬럼 없음.** `algorithm` 에는 `summary` 가 없다 —
   * `note`·`content` 와 달리 카드 한 줄이 컬럼으로 잡혀 있지 않다.
   * 백엔드가 md 에서 뽑아 주는지, 컬럼을 더할지 정해지지 않았다.
   */
  summary?: string | null;
}

export interface AlgorithmsResponse {
  "algorithms[]": AlgorithmListItem[];
  algorithms?: {
    /** **erd.md 에 대응 컬럼 없음.** 화면 머리말 문구. */
    subtitle?: string;
    intro?: string;
    totalCount?: number;
    /** `today = true` 인 한 건. 목록 상단에 고정된다. */
    today?: AlgorithmListItem | null;
  };
}

/* ── 상세 단계 ─────────────────────────────────────────────────────────────
 *
 * **단계 구조는 컬럼이 아니다.** md 본문의 `## Data` fenced yaml 이 갖고 서버가
 * 그것을 읽어 렌더한다(erd.md §algorithm). 다른 표의 `body` 와 같은 자리이므로
 * 같은 규칙을 따른다 — 정보는 DB, 상세는 md.
 *
 * erd.md 는 단계를 넷(Clarifying → Approach → Trace → Solution)으로 적었는데
 * 화면은 다섯(Problem · Clarifying · Approach · Logic · Trace · Solution)을 그린다.
 * **어긋나는 지점이다.** 화면 쪽을 그대로 두고 여기 적어 둔다.
 */

export interface AlgoQuizItem {
  q?: string;
  name?: string;
  complexity?: string;
  type: "good" | "distractor";
  why: string;
}

export interface AlgoLogicOption {
  code: string;
  type: "good" | "distractor";
  why: string;
}

export interface AlgoLogicSlot {
  label: string;
  indent?: number;
  options: AlgoLogicOption[];
}

export interface AlgoLogic {
  format: "slot";
  slots: AlgoLogicSlot[];
}

export interface AlgoTraceCase {
  input: string;
  expected: string;
}

export interface AlgoWorkedExample {
  input: string;
  steps: string[];
  answer: string;
}

export interface AlgoTrace {
  code: string[];
  cases: AlgoTraceCase[];
  worked_example: AlgoWorkedExample;
}

export interface AlgoSolution {
  code: string;
  complexity: { time: string; space: string };
  followup: string[];
}

export interface AlgoProblem {
  title?: string;
  statement: string;
  constraints: string[];
  io: { input: string; output: string }[];
}

export interface AlgorithmDetail extends AlgorithmListItem {
  problem: AlgoProblem;
  clarifying: { items: AlgoQuizItem[] };
  approach: { items: AlgoQuizItem[] };
  logic: AlgoLogic;
  trace: AlgoTrace;
  solution: AlgoSolution;
  newer: Neighbor | null;
  older: Neighbor | null;
}

export interface AlgorithmDetailResponse {
  "algorithms.detail": AlgorithmDetail;
}

/* ══════════════════════════════════════════════════════════════════════════
 * activity — 테이블이 없다. `commit` 을 날짜로 묶은 것이다(erd.md).
 * ══════════════════════════════════════════════════════════════════════════ */

export interface ActivityEntry {
  /** `authored_at::date`. */
  date: string;
  /** `COUNT(*) GROUP BY authored_at::date` — 칸 색 농도. */
  count: number;
  /**
   * **erd.md 에는 `commit` 만 있다.** `note`·`study` 를 셀 원천이 스키마에 없어서
   * 이 분류가 어디서 오는지 정해지지 않았다.
   */
  counts: Partial<Record<"commit" | "note" | "study", number>>;
  /** 그날 커밋들의 `commit.summary`. 커밋마다 한 줄이라 배열이다. */
  summary: string[] | null;
}

export interface ActivityResponse {
  "activity[]": ActivityEntry[];
  activity: { totalCount: number; since?: string; until?: string };
}

/* ══════════════════════════════════════════════════════════════════════════
 * site — **erd.md 에 대응 테이블이 없다.**
 *
 * footer 문구의 원천이 문서인지 DB 인지 정해지지 않았다. 옛 응답 모양을 그대로
 * 두되 전부 optional 로 둔다 — 없으면 화면이 그 줄을 그리지 않는다.
 * 옛 `files`(이력서·포트폴리오 PDF)는 `/print` 와 함께 빠졌다.
 * ══════════════════════════════════════════════════════════════════════════ */

/**
 * `site_config` — 사이트에 뜨는 문구 전부(erd.md §site_config).
 * DB key `<그룹>.<필드>` 를 백엔드가 `site.<그룹>.<camelField>` 로 접어 내려준다.
 * 키가 늘 수 있어 전부 optional — 없으면 화면이 대체 문구를 쓴다.
 */
export interface SiteResponse {
  site: {
    home?: {
      heroHeadline?: HeadlineLine[];
      heroSubline?: string;
      heroTerminal?: HeroTerminalLine[];
    };
    about?: {
      subtitle?: string;
      tagline?: string;
      intro?: string;
      intro2?: string;
      cards?: ProfileCard[];
    };
    footer?: {
      tagline?: string;
    };
  };
}

/** 어드민 site_config 목록의 행 — DB 행 그대로 (key · value · note). */
export interface SiteConfigItem {
  key: string;
  value: unknown;
  note?: string | null;
}

/* ══════════════════════════════════════════════════════════════════════════
 * company — erd.md §company. 어드민 회사 화면.
 * ══════════════════════════════════════════════════════════════════════════ */

export interface Company {
  id: number;
  slug: string;
  name: string;
  description?: string | null;
  location?: string | null;
  site?: string | null;
  logoUrl?: string | null;
}

/**
 * 회사 + career 파생값. `careerCount` 와 `period` 는 **컬럼이 아니다** —
 * 그 회사 career 행들의 개수·최소·최대다(erd.md §company). 읽기 전용 표시.
 */
export interface AdminCompany extends Company {
  careerCount: number;
  period?: string | null;
}

/** 등록·수정 폼이 보내는 필드 — 보낼 필드만 담는다. */
export type CompanyInput = Partial<Omit<Company, "id">>;

/* ══════════════════════════════════════════════════════════════════════════
 * career (admin) — erd.md §career. 어드민 역할 화면.
 * ══════════════════════════════════════════════════════════════════════════ */

/**
 * 역할 한 행 + 회사 이름. `isCurrent` · `period` 는 **컬럼이 아니다** —
 * `ended_on IS NULL` 과 두 날짜의 렌더다(erd.md §career). 백엔드가 계산해
 * 내려주고 프론트는 재계산하지 않는다(위 `TimelineEntryBase` 와 같은 규약).
 */
export interface AdminCareer {
  id: number;
  companyId: number;
  /** `company.name` 조인 — 읽기 전용 표시. 수정은 `companyId` 로 한다. */
  companyName: string;
  title: string;
  startedOn: string;
  endedOn?: string | null;
  isCurrent: boolean;
  /** 예: `2026.02 — 현재`. */
  period: string;
  summary?: string | null;
  description?: string | null;
  stack: string[];
}

/** 등록·수정 폼이 보내는 필드 — 보낼 필드만 담는다. 파생값·companyName 은 못 보낸다. */
export type CareerInput = Partial<
  Omit<AdminCareer, "id" | "companyName" | "isCurrent" | "period">
>;

/* ══════════════════════════════════════════════════════════════════════════
 * education (admin) — erd.md §education. 어드민 교육 화면.
 *
 * career 와 컬럼이 같지만 회사 조인이 없다 — org 가 컬럼이다. profile_id 는
 * 서버가 첫 profile 로 채우므로 계약에 없다.
 * ══════════════════════════════════════════════════════════════════════════ */

/**
 * 교육과정 한 행. `isCurrent` · `period` 는 **컬럼이 아니다** —
 * `ended_on IS NULL` 과 두 날짜의 렌더다(erd.md §education 은 컬럼만 갖는다).
 * 백엔드가 계산해 내려주고 프론트는 재계산하지 않는다(`AdminCareer` 와 같은 규약).
 */
export interface AdminEducation {
  id: number;
  org: string;
  title: string;
  location?: string | null;
  startedOn: string;
  endedOn?: string | null;
  isCurrent: boolean;
  /** 예: `2024.12 — 2025.03`. */
  period: string;
  summary?: string | null;
  /** 상세 md 경로. 본문은 DB 에 없다 — 정보는 DB, 상세는 md. */
  detailPath?: string | null;
  stack: string[];
}

/** 등록·수정 폼이 보내는 필드 — 보낼 필드만 담는다. 파생값은 못 보낸다. */
export type EducationInput = Partial<
  Omit<AdminEducation, "id" | "isCurrent" | "period">
>;

/* ══════════════════════════════════════════════════════════════════════════
 * product (admin) — erd.md §product. 어드민 회사 제품 화면.
 *
 * product 는 company 가 아니라 **career 에 속한다** — 「내가 그 역할에서 만든 것」의
 * 기록이다. 회사는 career.company_id 를 거쳐 닿는다.
 * ══════════════════════════════════════════════════════════════════════════ */

/**
 * 제품 한 행 + 역할·회사 이름. `careerTitle` · `companyName` 은 **컬럼이 아니다** —
 * product → career → company 2단 조인의 읽기 전용 표시. 수정은 `careerId` 로 한다.
 * `visible` 은 어드민이라 거르지 않고 그대로 온다.
 */
export interface AdminProduct {
  id: number;
  careerId: number;
  /** `career.title` 조인 — 읽기 전용 표시. */
  careerTitle: string;
  /** `company.name` 2단 조인 — 읽기 전용 표시. */
  companyName: string;
  slug: string;
  title: string;
  summary?: string | null;
  /** 상세 md 경로. 본문은 DB 에 없다 — 정보는 DB, 상세는 md. */
  detailPath?: string | null;
  category?: string | null;
  status?: WorkStatus | null;
  startedOn?: string | null;
  stack: string[];
  thumbnail?: string | null;
  /** `product.links` jsonb — `{site, docs}`. */
  links?: { site?: string; docs?: string } | null;
  visible: boolean;
}

/** 등록·수정 폼이 보내는 필드 — 보낼 필드만 담는다. 파생 표시값은 못 보낸다. */
export type ProductInput = Partial<
  Omit<AdminProduct, "id" | "careerTitle" | "companyName">
>;

/* ══════════════════════════════════════════════════════════════════════════
 * problem (admin) — erd.md §problem. 어드민 해결한 문제 화면.
 *
 * 이력서의 알맹이다. career 에 속하고(NOT NULL) product 에는 매일 수도
 * 안 매일 수도 있다(NULL 허용 — 조직·프로세스 문제). body 는 Text 컬럼
 * 그대로다 — 이 표는 detail_path 없이 본문을 행에 담는다.
 * ══════════════════════════════════════════════════════════════════════════ */

/**
 * 문제 한 행 + 이름들. `careerTitle` · `companyName` 은 **컬럼이 아니다** —
 * problem → career → company 2단 조인의 읽기 전용 표시. `productTitle` 은
 * 선택 조인 — `productId` 가 null 이면 null. 수정은 `careerId` · `productId` 로 한다.
 */
export interface AdminProblem {
  id: number;
  careerId: number;
  /** `career.title` 조인 — 읽기 전용 표시. */
  careerTitle: string;
  /** `company.name` 2단 조인 — 읽기 전용 표시. */
  companyName: string;
  /** null = 제품에 매이지 않은 문제. */
  productId?: number | null;
  /** `product.title` 조인 — 읽기 전용 표시. */
  productTitle?: string | null;
  /** 무엇을 풀었나. */
  title: string;
  /** 어떻게 풀었나. */
  body?: string | null;
  displayOrder: number;
}

/** 등록·수정 폼이 보내는 필드 — 보낼 필드만 담는다. `productId: null` 은 연결 해제. */
export type ProblemInput = Partial<
  Omit<AdminProblem, "id" | "careerTitle" | "companyName" | "productTitle">
>;

/* ══════════════════════════════════════════════════════════════════════════
 * project (admin) — erd.md §project. 어드민 개인 프로젝트 화면.
 *
 * project 는 career 없이 **profile 에 바로 붙는다** — 혼자 만든 것이라 소속이
 * 없다. profile_id 는 서버가 채우므로 계약에 없다. slug 는 **디렉토리명**이다 —
 * para/projects/summer-star/<slug>/ 가 없으면 등록이 422 로 막힌다(케이스 2).
 * ══════════════════════════════════════════════════════════════════════════ */

export interface AdminProject {
  id: number;
  /** para/projects/summer-star/ 하위 디렉토리명 — wine-log. */
  slug: string;
  title: string;
  summary?: string | null;
  /** 상세 md 경로. 안 보내면 서버가 showcase.md 경로로 채운다. */
  detailPath?: string | null;
  category?: string | null;
  status?: WorkStatus | null;
  startedOn?: string | null;
  stack: string[];
  thumbnail?: string | null;
  /** `project.links` jsonb — `{repo, site, store}`. */
  links?: { repo?: string; site?: string; store?: string } | null;
  visible: boolean;
}

/** 등록·수정 폼이 보내는 필드 — 보낼 필드만 담는다. */
export type ProjectInput = Partial<Omit<AdminProject, "id">>;

/* ══════════════════════════════════════════════════════════════════════════
 * algorithm (admin) — erd.md §algorithm. 어드민 알고리즘 화면.
 *
 * 메타만 다룬다 — 본문 단계(Problem→…→Solution)는 detailPath 의 md 몫이다.
 * profile_id 는 서버가 첫 profile 로 채우므로 계약에 없다. today 는 DB 의
 * partial unique index(uq_algorithm_today)가 하나만 허용한다 — today=true 를
 * 보내면 서버가 한 트랜잭션에서 이전 today 행을 먼저 내린다.
 * ══════════════════════════════════════════════════════════════════════════ */

export interface AdminAlgorithm {
  id: number;
  /** UK — frontmatter 의 `id` (A-001). */
  slug: string;
  title: string;
  difficulty: AlgoDifficulty;
  summary?: string | null;
  sourcePlatform: string;
  sourceNumber?: number | null;
  sourceUrl?: string | null;
  /** `neetcode150` · `blind75`. */
  curatedIn: string[];
  tags: string[];
  /** 「오늘의 문제」 — DB 가 하나뿐임을 강제한다. */
  today: boolean;
  /** 상세 md 경로 — para/resources/algorithms/*.md. 본문은 DB 에 없다. */
  detailPath: string;
  publishedOn?: string | null;
  visible: boolean;
}

/** 등록·수정 폼이 보내는 필드 — 보낼 필드만 담는다. */
export type AlgorithmInput = Partial<Omit<AdminAlgorithm, "id">>;

/* ══════════════════════════════════════════════════════════════════════════
 * note (admin) — erd.md §note. 어드민 노트 화면.
 *
 * 원장은 para/resources/note/ 의 md 다. **공개는 선택이다** — 글을 쓴다고
 * 사이트에 뜨지 않고, 어드민이 파일을 골라 등록해야 뜬다(케이스 4).
 * profile_id 는 서버가 첫 profile 로 채우므로 계약에 없다.
 * ══════════════════════════════════════════════════════════════════════════ */

export interface AdminNote {
  id: number;
  slug: string;
  title: string;
  summary?: string | null;
  /** 상세 md 경로 — para/resources/note/ 하위의 실존 파일만 등록된다. */
  detailPath: string;
  tags: string[];
  publishedOn?: string | null;
  visible: boolean;
}

/** 등록·수정 폼이 보내는 필드 — 보낼 필드만 담는다. */
export type NoteInput = Partial<Omit<AdminNote, "id">>;

/**
 * 등록 후보 파일 하나 — **DB 행이 아니다.** para/resources/note/ 의 미등록 md 를
 * 서버가 훑어 frontmatter(title·summary·date·tags)를 뽑아 준 것. 폼 프리필용.
 */
export interface NoteFileCandidate {
  /** repo 루트 기준 상대경로 — para/resources/note/... */
  path: string;
  /** 파일명 stem — slug 프리필 후보. */
  stem: string;
  title?: string | null;
  summary?: string | null;
  /** frontmatter date — publishedOn 프리필. `YYYY-MM-DD`. */
  date?: string | null;
  tags: string[];
}

/* ══════════════════════════════════════════════════════════════════════════
 * content (admin) — erd.md §content. 어드민 콘텐츠(영상 + 교안) 화면.
 *
 * 원장은 para/resources/youtube/ 의 md — detail_path 가 가리키는 파일이
 * 없으면 등록이 422 로 막힌다(정보는 DB, 상세는 md). profile_id 는 서버가
 * 첫 profile 로 채우므로 계약에 없다. visible 은 어드민이라 그대로 온다.
 * ══════════════════════════════════════════════════════════════════════════ */

export interface AdminContent {
  id: number;
  /** UK. 예: `C-025`. */
  slug: string;
  title: string;
  summary?: string | null;
  /** 상세 md 경로 — para/resources/youtube/ 하위. 본문은 DB 에 없다. */
  detailPath: string;
  youtubeId: string;
  /** 예: `3:58`. */
  duration?: string | null;
  /** 출처 채널. */
  speaker?: string | null;
  tags: string[];
  publishedOn?: string | null;
  visible: boolean;
}

/** 등록·수정 폼이 보내는 필드 — 보낼 필드만 담는다. */
export type ContentInput = Partial<Omit<AdminContent, "id">>;
