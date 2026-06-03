/**
 * /api/print/* 응답 타입 — KO+EN 합본 PDF 용 raw 데이터 (planning-02).
 * 사이트 API 와 달리 i18n 미적용 — `{ko, en}` 객체 그대로 내려옴.
 */

export interface I18nPair<T = string> {
  ko: T;
  en: T;
}

export interface PrintProfile {
  handle: string;
  name: I18nPair;
  role: I18nPair;
  location?: I18nPair;
  email: string;
  github?: string;
  linkedin?: string;
  tagline: I18nPair;
}

export interface PrintAbout {
  intro: I18nPair;
  intro2?: I18nPair;
}

export interface PrintSkills {
  primary?: string[];
  secondary?: string[];
  learning?: string[];
}

export interface PrintCareerItem {
  period: string;
  title: I18nPair;
  org: I18nPair | string;
  location?: I18nPair | string;
  summary: I18nPair;
  stack: string[];
  bullets?: I18nPair<string[]>;
  is_current: boolean;
}

export interface PrintEducationItem {
  period: string;
  degree: I18nPair;
  org: I18nPair | string;
  loc?: I18nPair | string;
  note?: I18nPair;
}

export interface PrintAwardItem {
  period: string;
  title: I18nPair;
  note?: I18nPair;
}

export interface PrintResumeProjectMini {
  id: string;
  title: I18nPair;
  period?: string;
  summary: I18nPair;
}

export interface PrintResumeResponse {
  profile: PrintProfile;
  about: PrintAbout;
  skills?: PrintSkills;
  career: PrintCareerItem[];
  education: PrintEducationItem[];
  awards: PrintAwardItem[];
  projects: PrintResumeProjectMini[];
}

export interface PrintTrouble {
  when: string;
  title: I18nPair;
  cause: I18nPair;
  fix: I18nPair;
}

export interface PrintProjectItem {
  id: string;
  code?: string;
  title: I18nPair;
  summary: I18nPair;
  category: string;
  status: "wip" | "live" | "archived" | string;
  date?: string;
  stack: string[];
  links: { repo?: string; live?: string };
  thumbnail?: string;
  problem?: I18nPair;
  approach?: I18nPair<string[]>;
  impact?: I18nPair<string[]>;
  learnings?: I18nPair<string[]>;
  troubles: PrintTrouble[];
}

export interface PrintPortfolioResponse {
  profile: PrintProfile;
  projects: PrintProjectItem[];
}
