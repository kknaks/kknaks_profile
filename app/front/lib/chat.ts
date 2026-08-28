"use client";

/**
 * 채용담당자 채팅 — API 클라이언트 · 2초 폴링 훅 (KDEV-SPEC-017 §4).
 *
 * 계약 타입은 `chat-types.ts` 가 갖고 여기서 그대로 재수출한다 — 화면은
 * `@/lib/chat` 하나만 본다.
 *
 * **세션 쿠키(`chat_sid`)는 httpOnly 다** — JS 가 만지지 않는다. 다른 오리진의
 * 백엔드라 브라우저가 쿠키를 붙이려면 `credentials: "include"` 가 필수다
 * (`lib/api.ts` 의 `authFetch` 와 같은 이유).
 *
 * **mock 스위치**: 기본은 실 API. `NEXT_PUBLIC_CHAT_MOCK=1` 이면 fixture mock
 * (`chat-mock.ts`)을 쓴다 — BE 미완 상태의 화면 개발용. 통합은 env 를 내리는
 * 것으로 끝나고 화면 코드는 바뀌지 않는다.
 */

import { useEffect, useRef } from "react";
import { chatMock } from "./chat-mock";
import {
  ChatApiError,
  POLL_INTERVAL_MS,
  type ChatClient,
  type ChatErrorCode,
  type ChatId,
  type ChatMessage,
  type Conversation,
  type ConversationDetail,
} from "./chat-types";

export * from "./chat-types";

const API_BASE = process.env.NEXT_PUBLIC_API_BASE ?? "http://localhost:48000";
const USE_MOCK = process.env.NEXT_PUBLIC_CHAT_MOCK === "1";

/* ── fetch ────────────────────────────────────────────────────────────── */

/** 에러 본문의 코드 자리는 계약에 없다 — `code` · `detail.code` · `detail` 문자열을 다 본다. */
function pickCode(body: unknown): ChatErrorCode | null {
  if (!body || typeof body !== "object") return null;
  const b = body as Record<string, unknown>;
  const raw =
    typeof b.code === "string"
      ? b.code
      : b.detail && typeof b.detail === "object"
        ? (b.detail as Record<string, unknown>).code
        : typeof b.detail === "string"
          ? b.detail
          : null;
  return typeof raw === "string" ? (raw as ChatErrorCode) : null;
}

async function chatFetch<T>(path: string, init?: RequestInit): Promise<T> {
  const res = await fetch(API_BASE + path, {
    ...init,
    // 익명 세션 쿠키(httpOnly)를 붙이려면 필수 — 크로스 오리진이다.
    credentials: "include",
    cache: "no-store",
    headers: { "Content-Type": "application/json", ...(init?.headers ?? {}) },
  });
  if (!res.ok) {
    let body: unknown = null;
    try {
      body = await res.json();
    } catch {
      /* 본문 없음 */
    }
    // 코드가 안 실려 와도 상태 코드로 갈린다 — Case Matrix 의 404·409 는 상태가 곧 뜻이다.
    const fallback: ChatErrorCode | null =
      res.status === 404 ? "NOT_FOUND" : res.status === 409 ? "CONVERSATION_BUSY" : null;
    throw new ChatApiError(res.status, pickCode(body) ?? fallback, `chat ${res.status}`);
  }
  return (await res.json()) as T;
}

/** 목록 응답의 봉투는 계약에 없다 — 배열이 있는 자리를 찾아 편다. */
function unwrapList(data: unknown): Conversation[] {
  if (Array.isArray(data)) return data as Conversation[];
  if (data && typeof data === "object") {
    const d = data as Record<string, unknown>;
    for (const key of ["conversations", "conversations[]", "items"]) {
      if (Array.isArray(d[key])) return d[key] as Conversation[];
    }
  }
  return [];
}

const realChatApi: ChatClient = {
  listConversations: async () =>
    unwrapList(await chatFetch<unknown>("/api/chat/conversations")),
  createConversation: (question) =>
    chatFetch<ConversationDetail>("/api/chat/conversations", {
      method: "POST",
      body: JSON.stringify({ question }),
    }),
  getConversation: (id) =>
    chatFetch<ConversationDetail>(
      `/api/chat/conversations/${encodeURIComponent(String(id))}`,
    ),
  sendMessage: (id, question) =>
    chatFetch<{ messages: ChatMessage[] }>(
      `/api/chat/conversations/${encodeURIComponent(String(id))}/messages`,
      { method: "POST", body: JSON.stringify({ question }) },
    ),
  // 본문 없음 — 질문은 서버가 그 메시지에서 되찾는다(§3 S-8 3항).
  retryMessage: (id, messageId) =>
    chatFetch<{ message: ChatMessage }>(
      `/api/chat/conversations/${encodeURIComponent(String(id))}/messages/${encodeURIComponent(
        String(messageId),
      )}/retry`,
      { method: "POST" },
    ),
};

/** 화면이 쓰는 단일 진입점. mock 여부는 여기서 한 번만 갈린다. */
export const chatApi: ChatClient = USE_MOCK ? chatMock : realChatApi;

/* ── 헬퍼 ─────────────────────────────────────────────────────────────── */

export function sameId(a: ChatId | null | undefined, b: ChatId | null | undefined): boolean {
  if (a == null || b == null) return false;
  return String(a) === String(b);
}

/** pending assistant 가 하나라도 있으면 폴링을 돌고 컴포저를 잠근다(§4 · U-6). */
export function hasPendingAssistant(messages: ChatMessage[]): boolean {
  return messages.some((m) => m.role === "assistant" && m.status === "pending");
}

/* ── 2초 폴링 훅 ──────────────────────────────────────────────────────── */

/**
 * `active` 동안만 2초 간격으로 대화를 다시 읽는다.
 *
 * - 호출부가 `done`/`failed` 에서 `active=false` 로 내리면 **폴링이 멈춘다**.
 * - 대화 전환·언마운트에서 인터벌을 걷고, 늦게 도착한 응답은 버린다
 *   (`cancelled` 가드 — 옛 대화의 응답이 새 스레드를 덮지 않게).
 */
export function useConversationPolling({
  conversationId,
  active,
  onTick,
  onError,
}: {
  conversationId: ChatId | null;
  active: boolean;
  onTick: (detail: ConversationDetail) => void;
  onError?: (err: unknown) => void;
}) {
  // 콜백은 ref 로 — 매 렌더마다 인터벌을 다시 걸지 않는다.
  const tickRef = useRef(onTick);
  const errRef = useRef(onError);
  tickRef.current = onTick;
  errRef.current = onError;

  useEffect(() => {
    if (!active || conversationId == null) return;
    let cancelled = false;

    const timer = setInterval(async () => {
      try {
        const detail = await chatApi.getConversation(conversationId);
        if (!cancelled) tickRef.current(detail);
      } catch (err) {
        if (!cancelled) errRef.current?.(err);
      }
    }, POLL_INTERVAL_MS);

    return () => {
      cancelled = true;
      clearInterval(timer);
    };
  }, [conversationId, active]);
}
