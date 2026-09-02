"use client";

/**
 * 어드민 채팅 fixture mock — BE(WORK-025 Phase 1) 미완 상태에서 화면을 개발·확인
 * 하기 위한 것. 방문자 쪽 `chat-mock.ts` 와 같은 자리, 같은 스위치다.
 *
 * `lib/admin-chat.ts` 의 `NEXT_PUBLIC_CHAT_MOCK=1` 로만 붙는다. 계약(spec §4
 * 어드민 응답 계약)의 shape 을 그대로 흉내낸다 — 응답 형태를 바꾸려면 spec 을
 * 먼저 고친다.
 *
 * 값은 시안(`21-html/admin-chat-mockup.html`)의 숫자를 그대로 옮겼다 — 시안과
 * 화면을 나란히 놓고 비교할 수 있게.
 */

import type { ChatMessage } from "./chat-types";
import {
  ADMIN_CHAT_PAGE_SIZE,
  type AdminChatClient,
  type AdminChatInsights,
  type AdminConversationDetail,
  type AdminConversationPage,
  type AdminConversationRow,
} from "./admin-chat-types";

/** 시안 기준일 — 상대 시각을 만들 기준. 실 데이터에서는 서버 시각이 온다. */
const TODAY = "2026-08-29";

const ROWS: AdminConversationRow[] = [
  {
    id: 41,
    sessionId: 41,
    title: "FastAPI 실무 경험 있나요? 회사에서는 어떤 제품을 만들…",
    messageCount: 6,
    createdAt: `${TODAY}T10:03:00+09:00`,
    lastMessageAt: `${TODAY}T10:12:00+09:00`,
  },
  {
    id: 38,
    sessionId: 38,
    title: "퀀터스에서 뭘 했어?",
    messageCount: 4,
    createdAt: `${TODAY}T09:52:00+09:00`,
    lastMessageAt: `${TODAY}T09:58:00+09:00`,
  },
  {
    id: 37,
    sessionId: 38,
    title: "Mediness가 뭐야?",
    messageCount: 2,
    createdAt: "2026-08-28T22:41:00+09:00",
    lastMessageAt: "2026-08-28T22:42:00+09:00",
  },
  {
    id: 35,
    sessionId: 35,
    title: "비동기 처리 경험 있어?",
    messageCount: 8,
    createdAt: "2026-08-28T18:07:00+09:00",
    lastMessageAt: "2026-08-28T18:31:00+09:00",
  },
  {
    id: 34,
    sessionId: 35,
    title: "쿠버네티스 써봤나요?",
    messageCount: 2,
    createdAt: "2026-08-28T17:55:00+09:00",
    lastMessageAt: "2026-08-28T17:56:00+09:00",
  },
  {
    id: 31,
    sessionId: 31,
    title: "이력서 PDF 어디서 받아요?",
    messageCount: 2,
    createdAt: "2026-08-28T14:20:00+09:00",
    lastMessageAt: "2026-08-28T14:21:00+09:00",
  },
];

/** 시안의 30일 시리즈 — 07-30 부터. 빈 날(0)이 섞여 있어 zero 바를 확인할 수 있다. */
const DAILY_COUNTS = [
  2, 0, 1, 3, 2, 4, 1, 0, 2, 3, 5, 2, 1, 4, 3, 2, 6, 4, 3, 1, 0, 2, 5, 7, 4, 3,
  8, 19, 12, 9,
];

function dailySeries(): { date: string; count: number }[] {
  // 07-30 시작 — `Date` 로 하루씩 민다. 시안의 `new Date(2026,6,30)` 과 같다.
  const start = new Date(2026, 6, 30);
  return DAILY_COUNTS.map((count, i) => {
    const d = new Date(start);
    d.setDate(start.getDate() + i);
    const date = `${d.getFullYear()}-${String(d.getMonth() + 1).padStart(2, "0")}-${String(
      d.getDate(),
    ).padStart(2, "0")}`;
    return { date, count };
  });
}

const INSIGHTS: AdminChatInsights = {
  totals: { conversations: 47, questions: 128, last7d: 31 },
  recentQuestions: [
    {
      question: "FastAPI 실무 경험 있나요? 회사에서는 어떤 제품을 만들었나요?",
      askedAt: `${TODAY}T10:12:00+09:00`,
      conversationId: 41,
    },
    { question: "퀀터스에서 뭘 했어?", askedAt: `${TODAY}T09:58:00+09:00`, conversationId: 38 },
    {
      question: "가장 어려웠던 기술적 문제 하나만 얘기해줘",
      askedAt: `${TODAY}T09:31:00+09:00`,
      conversationId: 38,
    },
    {
      question: "Mediness가 뭐야? 네가 뭘 만들었는데?",
      askedAt: "2026-08-28T22:41:00+09:00",
      conversationId: 37,
    },
    { question: "비동기 처리 경험 있어?", askedAt: "2026-08-28T18:07:00+09:00", conversationId: 35 },
    { question: "쿠버네티스 써봤나요?", askedAt: "2026-08-28T17:55:00+09:00", conversationId: 34 },
  ],
  daily: dailySeries(),
  topSources: [
    { type: "company_product", slug: "mediness", title: "메디니스 · 의료 AI 서비스", count: 23 },
    { type: "career", slug: "medisolve-ai-1", title: "메디솔브 AI · 백엔드 개발자", count: 18 },
    { type: "company_product", slug: "quantus", title: "퀀터스 · 실시간 시세 파이프라인", count: 14 },
    { type: "problem", slug: "problem-4", title: "고부하에서 무너지던 뉴스·공시 조회", count: 9 },
    { type: "project", slug: "wine-log", title: "Wine Log", count: 6 },
  ],
};

/** 시안 상세의 두 턴. 읽기 전용이라 status 는 전부 `done` 이다. */
const DETAIL_MESSAGES: ChatMessage[] = [
  {
    id: "m1",
    role: "user",
    status: "done",
    content: "FastAPI 실무 경험 있나요? 회사에서는 어떤 제품을 만들었나요?",
    sources: [],
    steps: [],
    createdAt: `${TODAY}T10:03:00+09:00`,
  },
  {
    id: "m2",
    role: "assistant",
    status: "done",
    content: [
      "네, FastAPI 실무 경험이 있습니다. 메디솔브 AI와 퀀터스에서 Python·FastAPI 기반 백엔드를 개발했고, WebSocket·Redis·RabbitMQ·PostgreSQL/MySQL을 함께 활용했습니다.",
      "회사에서는 다음 제품을 만들었습니다 — Charty(실시간 전사·통역·AI 차트), Linky(6개 메신저 통합 다국어 상담), Mediness(사내 AX 워크스페이스)…",
    ].join("\n\n"),
    sources: [
      { type: "career", slug: "medisolve-ai-1", title: "메디솔브 AI · 백엔드 개발자", url: "/career" },
      { type: "company_product", slug: "mediness", title: "메디니스", url: "/career" },
      { type: "company_product", slug: "charty", title: "Charty", url: "/career" },
      { type: "career", slug: "quantus-2", title: "퀀터스 · 백엔드 개발자", url: "/career" },
    ],
    steps: [
      {
        tool: "list_company_products",
        argsSummary: "—",
        durationMs: 166,
        calledAt: `${TODAY}T10:03:02+09:00`,
      },
      { tool: "list_career", argsSummary: "—", durationMs: 32, calledAt: `${TODAY}T10:03:03+09:00` },
      {
        tool: "get_career",
        argsSummary: "slug=medisolve-ai-1",
        durationMs: 58,
        calledAt: `${TODAY}T10:03:04+09:00`,
      },
      {
        tool: "get_company_product",
        argsSummary: "slug=mediness",
        durationMs: 35,
        calledAt: `${TODAY}T10:03:05+09:00`,
      },
    ],
    createdAt: `${TODAY}T10:03:00+09:00`,
  },
  {
    id: "m3",
    role: "user",
    status: "done",
    content: "그 중에 제일 어려웠던 문제 하나만",
    sources: [],
    steps: [],
    createdAt: `${TODAY}T10:10:00+09:00`,
  },
  {
    id: "m4",
    role: "assistant",
    status: "done",
    content:
      "가장 어려웠던 문제는 퀀터스의 실시간 시세 파이프라인 안정화였습니다. ETF 60종의 웹소켓 시세를 자동트레이딩 서버로 전달해야 했고…",
    sources: [
      { type: "problem", slug: "problem-4", title: "고부하에서 무너지던 뉴스·공시 조회", url: "/career" },
    ],
    steps: [
      { tool: "list_problems", argsSummary: "—", durationMs: 41, calledAt: `${TODAY}T10:10:02+09:00` },
      {
        tool: "get_problem",
        argsSummary: "slug=problem-4",
        durationMs: 37,
        calledAt: `${TODAY}T10:10:03+09:00`,
      },
    ],
    createdAt: `${TODAY}T10:12:00+09:00`,
  },
];

/** 실제 왕복처럼 조금 늦게 답한다 — 로딩 상태가 눈에 보이게. */
const delay = (ms = 160) => new Promise((r) => setTimeout(r, ms));

export const adminChatMock: AdminChatClient = {
  async conversations(page, size = ADMIN_CHAT_PAGE_SIZE) {
    await delay();
    // 총계는 시안대로 47 건 — 페이지네이션이 여러 장으로 보이게. 실제 fixture 행은
    // 6개뿐이라 2쪽부터는 같은 행을 id 만 밀어 되쓴다.
    const total = 47;
    const offset = (page - 1) * size;
    const items = Array.from({ length: Math.min(size, Math.max(0, total - offset)) }, (_, i) => {
      const base = ROWS[(offset + i) % ROWS.length];
      return offset + i < ROWS.length ? base : { ...base, id: `p${page}-${i}` };
    });
    return { items, total, page, size };
  },

  async conversation(id) {
    await delay();
    const row = ROWS.find((r) => String(r.id) === String(id));
    if (!row) {
      // fixture 밖의 id 도 화면 확인은 되어야 한다 — 같은 스레드를 제목만 바꿔 준다.
      return {
        conversation: { id, title: "(mock) 대화", createdAt: `${TODAY}T10:03:00+09:00` },
        messages: DETAIL_MESSAGES,
        sessionId: null,
      };
    }
    return {
      conversation: { id: row.id, title: row.title, createdAt: row.createdAt },
      messages: DETAIL_MESSAGES,
      sessionId: row.sessionId,
    };
  },

  async insights() {
    await delay(120);
    return INSIGHTS;
  },
};

/** 타입만 쓰는 재수출 — mock 을 읽는 쪽이 shape 을 확인할 수 있게. */
export type { AdminConversationDetail, AdminConversationPage };
