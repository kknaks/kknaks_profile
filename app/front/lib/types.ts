/**
 * Backend API 응답 타입 (spec-02 §3 기반).
 * 모든 string 필드는 백엔드가 lang 분기 후 단일 언어로 반환.
 */

export type HeadlineTone = "muted" | "default" | "accent";

export interface HeadlineLine {
  text: string;
  tone: HeadlineTone;
}

export interface HeroTerminalLine {
  prompt: string;
  output: string[];
}

export interface MeResponse {
  user: {
    handle: string;
    name: string;
    role: string;
    years?: string;
    location?: string;
    focus?: string;
    email: string;
    github?: string;
    linkedin?: string;
    avatarUrl?: string;
    tagline: string;
    intro: string;
    intro2?: string;
    stack: string[];
    stackShort?: string;
    cards?: { title: string; body: string }[];
  };
  hero?: { headline?: HeadlineLine[]; subline?: string };
  heroTerminal?: HeroTerminalLine[];
  about: { subtitle: string };
}

export interface CareerItem {
  period: string;
  title: string;
  org: string;
  location?: string;
  summary: string;
  stack: string[];
  is_current?: boolean;
  body?: string;
}

export interface CareerResponse {
  career: {
    subtitle: string;
    totalRoles: string;
    totalYears?: string;
    focus?: string;
  };
  "career[]": CareerItem[];
}

export interface ProjectItem {
  id: string;
  title: string;
  summary: string;
  category: string;
  status: "live" | "wip" | "archived";
  date?: string;
  stack: string[];
  thumbnail?: string | null;
  links?: { repo?: string; live?: string };
  body?: string;
}

export interface ProjectsResponse {
  projects: {
    subtitle: string;
    totalCount: number;
    categories: { id: string; label: string; count: number }[];
  };
  "projects[]": ProjectItem[];
}

export interface NoteRecent {
  id: string;
  title: string;
  date?: string;
  path: string;
}

export interface NotesGraphResponse {
  notes: {
    totalCount: number;
    edgeCount: number;
    graph: {
      clusters: { id: string; label: string; color?: string }[];
      nodes: { id: string; title: string; group?: string; stack?: string[] }[];
      edges: { source: string; target: string }[];
    };
    topics: { tag: string; count: number }[];
    stacks: { name: string; count: number }[];
  };
}

/* ---------- 전역 지식 그래프 (work-008 / spec-005) — NotesGraphResponse와 별개 ---------- */

export type GraphNodeType =
  | "reference"
  | "permanent"
  | "post"
  | "product"
  | "idea";

export interface GraphNode {
  id: string;
  type: GraphNodeType;
  title: string;
  archived: boolean;
}

export interface GraphEdge {
  source: string;
  target: string;
  type: "lineage" | "assoc";
  dir?: "up" | null;
}

export interface GraphResponse {
  nodes: GraphNode[];
  edges: GraphEdge[];
  backlinks: Record<string, string[]>;
}

export interface NoteDetail {
  id: string;
  title: string;
  date?: string;
  tags: string[];
  stack?: string[];
  body: string;
  backlinks: { id: string; title: string }[];
}

export interface ContentItem {
  id: string;
  date: string;
  day: string;
  title: string;
  youtubeId: string;
  duration?: string;
  summary: string;
  tags?: string[];
}

export interface ContentsResponse {
  contents: { subtitle: string; intro: string; totalCount: number };
  "contents[]": ContentItem[];
}

export interface ContentDetailNeighbor {
  id: string;
  title: string;
}

export interface ContentDetail extends ContentItem {
  speaker?: string;
  concept: string[];                       // 시안 02 영역 카드 (spec-06 §3.3)
  body: string;                            // 8섹션 강의 교안 markdown — 시안 03 영역
  newer: ContentDetailNeighbor | null;
  older: ContentDetailNeighbor | null;
}

export interface ContentDetailResponse {
  "contents.detail": ContentDetail;
}

export interface ActivityEntry {
  date: string;
  count: number;                                              // = sum(counts.values()) — 잔디 색 강도 호환
  counts: Partial<Record<"commit" | "note" | "study", number>>;
  // string = 레거시 entry, string[] = 새 spec (활동 단위별 1줄, spec-03 §3.2)
  summary: string | string[] | null;
}

export interface ActivityResponse {
  activity: { totalCount: number; since?: string; until?: string };
  "activity[]": ActivityEntry[];
}

export interface SiteResponse {
  site: {
    footerTagline: string;
    location: string;
    version: string;
    uptime: string;
    year: string;
  };
  files: {
    resumeLabel: string;
    portfolioLabel: string;
  };
}

/* ---------- Algorithms (spec-07) — i18n flatten 후 string ---------- */

export interface AlgorithmSource {
  platform: "leetcode";
  number: number;
  slug: string;
  url: string;
  curated_in?: string[];
}

export interface AlgorithmListItem {
  id: string;
  date: string;
  day?: string;
  title: string;
  summary: string;
  difficulty: "easy" | "medium" | "hard";
  source: AlgorithmSource;
  tags: string[];
}

export interface AlgorithmsResponse {
  algorithms: {
    subtitle: string;
    intro: string;
    totalCount: number;
    today: AlgorithmListItem | null;
  };
  "algorithms[]": AlgorithmListItem[];
}

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

export interface AlgorithmDetail {
  id: string;
  date: string;
  day?: string;
  title: string;
  difficulty: "easy" | "medium" | "hard";
  source: AlgorithmSource;
  tags: string[];
  problem: AlgoProblem;
  clarifying: { items: AlgoQuizItem[] };
  approach: { items: AlgoQuizItem[] };
  logic: AlgoLogic;
  trace: AlgoTrace;
  solution: AlgoSolution;
  newer: { id: string; title: string } | null;
  older: { id: string; title: string } | null;
}

export interface AlgorithmDetailResponse {
  "algorithms.detail": AlgorithmDetail;
}
