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
  name: string;
  role: string;
  location?: string;
  email: string;
  github?: string;
  linkedin?: string;
  tagline: I18nPair;
}

export interface PrintAbout {
  intro: I18nPair;
  intro2?: I18nPair;
}

export interface PrintCareerItem {
  period: string;
  title: I18nPair;
  org: I18nPair | string;
  location?: I18nPair | string;
  summary: I18nPair;
  stack: string[];
  is_current: boolean;
}

export interface PrintResumeResponse {
  profile: PrintProfile;
  about: PrintAbout;
  career: PrintCareerItem[];
}
