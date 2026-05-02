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
  count: number;
  kind: "commit" | "note" | "study" | null;
  summary: string | null;
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
