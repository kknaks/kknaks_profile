/**
 * 채팅 계약 타입 — KDEV-SPEC-017 §4 Data Contract 그대로.
 *
 * 화면은 `@/lib/chat` 에서 가져다 쓴다(거기서 재수출한다). 이 파일이 따로 있는 건
 * mock(`chat-mock.ts`)과 클라이언트(`chat.ts`)가 서로를 물지 않게 하기 위해서다.
 * **여기서 필드를 발명하지 않는다** — spec 이 SoT.
 */

/** BE 가 uuid 를 줄지 정수를 줄지는 계약에 없다 — 둘 다 받는다. 비교는 `sameId`. */
export type ChatId = string | number;

export type ChatRole = "user" | "assistant";
export type ChatMessageStatus = "pending" | "done" | "failed";
export type ChatSourceType =
  | "career"
  | "project"
  | "problem"
  | "note"
  | "company_product";

/**
 * 근거 카드 — AI 가 **실제로 읽은** 문서다(§3 S-9). `url` 은 공개 페이지 경로.
 *
 * 전용 상세 페이지가 없는 유형(career · problem)은 공개 표면 경로가 오고, 그마저
 * 없으면 `null` 이다 — 그때는 링크를 걸지 않고 카드만 그린다(BE `ChatSourceItem`).
 */
export interface ChatSource {
  type: ChatSourceType;
  slug: string;
  title: string;
  url?: string | null;
}

/** tool 호출 한 단계 — 기록 주체는 소비자(이벤트 폴딩). AI 자기 신고가 아니다. */
export interface ChatStep {
  tool: string;
  argsSummary: string;
  durationMs?: number | null;
  calledAt: string;
}

export interface ChatMessage {
  id: ChatId;
  role: ChatRole;
  status: ChatMessageStatus;
  /** `pending` 중에는 부분 텍스트, `done` 에서 최종 본문으로 교체된다. */
  content: string;
  sources: ChatSource[];
  steps: ChatStep[];
  createdAt: string;
}

export interface Conversation {
  id: ChatId;
  title: string;
  createdAt: string;
}

export interface ConversationDetail {
  conversation: Conversation;
  messages: ChatMessage[];
}

/** Case Matrix(§4)의 코드. 표시 문구는 화면이 정한다. */
export type ChatErrorCode =
  | "QUESTION_TOO_LONG"
  | "NOT_FOUND"
  | "CONVERSATION_BUSY"
  | "EMPTY_QUESTION";

export class ChatApiError extends Error {
  constructor(
    public status: number,
    public code: ChatErrorCode | null,
    message: string,
  ) {
    super(message);
  }
}

/** question 최대 길이 — §4 Validation(trim 후 1자 이상 1,000자 이하). */
export const QUESTION_MAX_LENGTH = 1000;

/** 폴링 간격 — §4 「2초」. */
export const POLL_INTERVAL_MS = 2000;

/** 화면이 쓰는 단일 API 표면. 실 API 와 mock 이 같은 모양을 만족한다. */
export interface ChatClient {
  /** 쿠키가 없으면 빈 목록 — 세션을 만들지 않는다(§3 S-2). */
  listConversations(): Promise<Conversation[]>;
  /** 대화 생성 + 첫 질문. 세션 없으면 BE 가 발급한다(§3 S-1). */
  createConversation(question: string): Promise<ConversationDetail>;
  /** 폴링 대상. 남의 세션·없는 대화면 404(§4 Case Matrix). */
  getConversation(id: ChatId): Promise<ConversationDetail>;
  /** 이어서 질문. pending 중이면 409 — FE 는 잠금으로 선차단한다(§2 U-6). */
  sendMessage(id: ChatId, question: string): Promise<{ messages: ChatMessage[] }>;
  /**
   * 실패한 답변 재시도(§3 S-8 3항) — **그 자리의 failed assistant 를 pending 으로
   * 되돌린다**(content·steps 초기화). 새 메시지 줄을 만들지 않는다.
   * 대상이 failed assistant 가 아니면 404, 대화에 pending 이 있으면 409.
   */
  retryMessage(id: ChatId, messageId: ChatId): Promise<{ message: ChatMessage }>;
}
