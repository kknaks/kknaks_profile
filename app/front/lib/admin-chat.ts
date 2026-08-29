"use client";

/**
 * 어드민 채팅 열람·인사이트 — API 클라이언트 (KDEV-SPEC-017 §4 · U-8).
 *
 * 계약 타입은 `admin-chat-types.ts` 가 갖고 여기서 그대로 재수출한다 — 화면은
 * `@/lib/admin-chat` 하나만 본다. 방문자 쪽(`lib/chat.ts`)과 같은 구조다.
 *
 * **관리자 세션 쿠키는 httpOnly 다** — `lib/api.ts` 의 `authFetch` 와 같은 이유로
 * `credentials: "include"` 가 필수다. 인증 게이트는 `(panel)/layout.tsx` 가
 * 이미 서고, 여기서는 401/403 을 `AuthError` 로 올려 화면이 문구를 만든다.
 *
 * **mock 스위치**: 기본은 실 API. `NEXT_PUBLIC_CHAT_MOCK=1` 이면 fixture mock
 * (`admin-chat-mock.ts`)을 쓴다 — BE 미완 상태의 화면 개발용. 방문자 채팅과 같은
 * 스위치 하나다. 통합은 env 를 내리는 것으로 끝나고 화면 코드는 바뀌지 않는다.
 */

import { AuthError } from "./api";
import { adminChatMock } from "./admin-chat-mock";
import {
  ADMIN_CHAT_PAGE_SIZE,
  type AdminChatClient,
  type AdminChatInsights,
  type AdminConversationDetail,
  type AdminConversationPage,
} from "./admin-chat-types";
import type { ChatId } from "./chat-types";

export * from "./admin-chat-types";

const API_BASE = process.env.NEXT_PUBLIC_API_BASE ?? "http://localhost:48000";
const USE_MOCK = process.env.NEXT_PUBLIC_CHAT_MOCK === "1";

async function adminChatFetch<T>(path: string): Promise<T> {
  const res = await fetch(API_BASE + path, {
    credentials: "include",
    cache: "no-store",
    headers: { "Content-Type": "application/json" },
  });
  if (!res.ok) {
    let detail = `admin chat ${res.status}`;
    try {
      detail = (await res.json())?.detail ?? detail;
    } catch {
      /* 본문 없음 */
    }
    throw new AuthError(res.status, detail);
  }
  return (await res.json()) as T;
}

/**
 * 상세의 `sessionId` 자리는 계약에 「공개 상세 shape + sessionId」로만 적혀 있다 —
 * 봉투 바깥에 오는지 `conversation` 안에 오는지는 정해지지 않았다. 둘 다 본다.
 */
function normalizeDetail(raw: unknown): AdminConversationDetail {
  const d = (raw ?? {}) as Record<string, unknown>;
  const conv = (d.conversation ?? {}) as Record<string, unknown>;
  const sid = d.sessionId ?? conv.sessionId ?? null;
  return {
    conversation: d.conversation as AdminConversationDetail["conversation"],
    messages: (Array.isArray(d.messages) ? d.messages : []) as AdminConversationDetail["messages"],
    sessionId: (sid ?? null) as ChatId | null,
  };
}

const realAdminChatApi: AdminChatClient = {
  conversations: (page, size = ADMIN_CHAT_PAGE_SIZE) =>
    adminChatFetch<AdminConversationPage>(
      `/api/admin/chat/conversations?page=${page}&size=${size}`,
    ),
  conversation: async (id) =>
    normalizeDetail(
      await adminChatFetch<unknown>(
        `/api/admin/chat/conversations/${encodeURIComponent(String(id))}`,
      ),
    ),
  insights: () => adminChatFetch<AdminChatInsights>("/api/admin/chat/insights"),
};

/** 화면이 쓰는 단일 진입점. mock 여부는 여기서 한 번만 갈린다. */
export const adminChatApi: AdminChatClient = USE_MOCK ? adminChatMock : realAdminChatApi;
