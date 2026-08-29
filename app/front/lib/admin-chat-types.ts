/**
 * 어드민 채팅 열람·인사이트 계약 타입 — KDEV-SPEC-017 §4 「어드민 chat API 응답
 * 계약(2026-08-29)」 그대로.
 *
 * 메시지·근거·tool 단계는 방문자 계약과 **같은 shape** 이라 `chat-types.ts` 의
 * 것을 그대로 쓴다(spec: 「상세 → 공개 상세와 같은 shape + sessionId」). 여기서
 * 필드를 발명하지 않는다 — spec 이 SoT.
 *
 * 파일이 따로 있는 이유는 방문자 쪽과 같다 — mock(`admin-chat-mock.ts`)과
 * 클라이언트(`admin-chat.ts`)가 서로를 물지 않게 하기 위해서다.
 */

import type {
  ChatId,
  ChatMessage,
  ChatSourceType,
  Conversation,
} from "./chat-types";

/** 목록 한 행 — `{id, sessionId, title, messageCount, createdAt, lastMessageAt}`. */
export interface AdminConversationRow {
  id: ChatId;
  /** 익명 세션 id. 개인정보가 아니다(DEC-026 D3) — 같은 손님 묶어 보기용. */
  sessionId: ChatId;
  title: string;
  messageCount: number;
  createdAt: string;
  lastMessageAt: string;
}

/** 목록 응답 — `{items, total, page, size}`. 최신순, `page`/`size` 쿼리(기본 1/20). */
export interface AdminConversationPage {
  items: AdminConversationRow[];
  total: number;
  page: number;
  size: number;
}

/** 상세 — 공개 상세와 같은 shape + `sessionId`. 소유 세션 무관, admin 인증만. */
export interface AdminConversationDetail {
  conversation: Conversation;
  messages: ChatMessage[];
  sessionId: ChatId | null;
}

/** 헤더 총계 줄 — 「대화 N · 질문 N · 최근 7일 +N」. */
export interface AdminChatTotals {
  conversations: number;
  questions: number;
  last7d: number;
}

/** ① 최근 질문 피드 — 최근 20건. 클릭하면 그 대화 상세로 간다. */
export interface AdminRecentQuestion {
  question: string;
  askedAt: string;
  conversationId: ChatId;
}

/** ② 일별 질문 수 — 최근 30일, **빈 날도 count 0 으로 온다**(계약). */
export interface AdminDailyCount {
  date: string;
  count: number;
}

/** ③ 근거로 많이 읽힌 문서 Top 5 — sources 집계. */
export interface AdminTopSource {
  type: ChatSourceType;
  slug: string;
  title: string;
  count: number;
}

export interface AdminChatInsights {
  totals: AdminChatTotals;
  recentQuestions: AdminRecentQuestion[];
  daily: AdminDailyCount[];
  topSources: AdminTopSource[];
}

/** 목록 기본 페이지 크기 — 계약의 `size` 기본값. */
export const ADMIN_CHAT_PAGE_SIZE = 20;

/** 화면이 쓰는 단일 API 표면. 실 API 와 mock 이 같은 모양을 만족한다. */
export interface AdminChatClient {
  conversations(page: number, size?: number): Promise<AdminConversationPage>;
  conversation(id: ChatId): Promise<AdminConversationDetail>;
  insights(): Promise<AdminChatInsights>;
}
