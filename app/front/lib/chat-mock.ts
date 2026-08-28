"use client";

/**
 * 채팅 fixture mock — BE(WORK-023) 미완 상태에서 화면을 개발·확인하기 위한 것.
 *
 * `lib/chat.ts` 의 `NEXT_PUBLIC_CHAT_MOCK=1` 스위치로만 붙는다. 계약(spec §4)의
 * shape 을 그대로 흉내낸다 — **모의 지연 · 부분 텍스트 성장 · steps 누적 · 실패**.
 * 응답 형태를 바꾸려면 spec 을 먼저 고친다.
 *
 * 상태는 모듈 메모리다(새로고침하면 사라진다). 시간에 따른 진행은 저장하지 않고
 * 읽는 시점에 경과로 **계산한다** — 폴링이 몇 번 오든 같은 결과가 나온다.
 */

import {
  ChatApiError,
  QUESTION_MAX_LENGTH,
  type ChatClient,
  type ChatId,
  type ChatMessage,
  type ChatSource,
  type ChatStep,
  type Conversation,
  type ConversationDetail,
} from "./chat-types";

/** 질문에 이 말이 들어 있으면 실패 흐름(S-8)을 재현한다 — 「다시 시도」 확인용. */
const FAIL_TRIGGER = "실패";

const ANSWER = [
  "네, 실무 경험이 있습니다. 현재 메디솔브 AI 에서 백엔드 개발자로 일하며 FastAPI · Python · Postgres 스택으로 의료 AI 서비스의 백엔드를 개발하고 있습니다. AX팀 리더로 사내 AI 도입도 이끌었습니다.",
  "지금 보고 계신 이 사이트(kknaks.dev)도 FastAPI 백엔드로 직접 만들었습니다 — router → service → repository 계층 구조, Alembic 마이그레이션, Docker 배포까지 혼자 운영합니다.",
].join("\n\n");

// 근거 카드 네 장 — 유형마다 클릭 결과가 다르다(spec v0.0.12 U-5). career ·
// problem · company_product 는 우측 문서 패널, project 는 전용 페이지로 이동.
// **slug 는 BE 규약(core/chat_slugs.py) 그대로여야 한다** — 패널이 그 규약으로
// 공개 번들을 매칭하기 때문이다: career 는 `<company.slug>-<career.id>`,
// problem 은 `problem-<id>`, product 는 slug 컬럼.
const SOURCES: ChatSource[] = [
  { type: "career", slug: "medisolve-ai-1", title: "메디솔브 AI · 백엔드 개발자", url: "/career" },
  // **공개된 것만 건다** — 종전 `kknaks-dev` 는 visible=false 라 /projects/kknaks-dev
  // 가 404 였다. mock 이라도 죽은 링크를 두면 실서버로 오인한 사람이 밟는다.
  { type: "project", slug: "wine-log", title: "Wine Log", url: "/projects/wine-log" },
  // 제품 전용 페이지는 없지만 그 제품의 회사 이력이 그려지는 표면은 있다 —
  // BE `_URL_BUILDERS` 가 `/career` 를 준다(spec v0.0.9 에서 null 에서 뒤집혔다).
  { type: "company_product", slug: "mediness", title: "메디니스 · 의료 AI 서비스", url: "/career" },
  { type: "problem", slug: "problem-4", title: "고부하에서 무너지던 뉴스·공시 조회", url: "/career" },
];

/** {지연 ms, 단계} — 경과가 지연을 넘긴 단계만 보인다. */
const STEP_TIMELINE: { at: number; step: Omit<ChatStep, "calledAt">; doneAt: number }[] = [
  { at: 1200, doneAt: 2100, step: { tool: "list_career", argsSummary: "—", durationMs: 840 } },
  { at: 2600, doneAt: 3800, step: { tool: "get_career", argsSummary: "slug=medisolve-ai-1", durationMs: 1180 } },
  { at: 4200, doneAt: 5400, step: { tool: "get_project", argsSummary: "slug=wine-log", durationMs: 1120 } },
  { at: 5800, doneAt: 6900, step: { tool: "get_company_product", argsSummary: "slug=mediness", durationMs: 1060 } },
  { at: 6900, doneAt: 7800, step: { tool: "get_problem", argsSummary: "slug=problem-4", durationMs: 880 } },
];

const CONTENT_START_MS = 3200;
const CONTENT_FULL_MS = 7600;
const DONE_MS = 8200;

type MockMessage = {
  id: string;
  role: "user" | "assistant";
  question: string;
  createdAt: string;
  /** assistant 만 — 제출 시각. 여기서 경과를 잰다. */
  startedAt?: number;
  fail?: boolean;
};

type MockConversation = {
  id: string;
  title: string;
  createdAt: string;
  messages: MockMessage[];
};

const store = new Map<string, MockConversation>();
let seq = 0;
const nextId = () => `mock-${++seq}`;

function assertQuestion(question: string) {
  const q = question.trim();
  if (!q) throw new ChatApiError(422, "EMPTY_QUESTION", "빈 질문");
  if (q.length > QUESTION_MAX_LENGTH)
    throw new ChatApiError(422, "QUESTION_TOO_LONG", "질문이 너무 깁니다");
}

function find(id: ChatId): MockConversation {
  const conv = store.get(String(id));
  if (!conv) throw new ChatApiError(404, "NOT_FOUND", "없는 대화");
  return conv;
}

/** 경과로 assistant 한 건의 현재 모습을 만든다 — 폴링이 이걸 그대로 그린다. */
function renderAssistant(m: MockMessage): ChatMessage {
  const elapsed = Date.now() - (m.startedAt ?? 0);
  const steps: ChatStep[] = STEP_TIMELINE.filter((s) => elapsed >= s.at).map((s) => ({
    ...s.step,
    // 끝나기 전에는 소요 시간을 아직 모른다 — 짝이 맞아야 durationMs 가 생긴다.
    durationMs: elapsed >= s.doneAt ? s.step.durationMs : null,
    calledAt: new Date((m.startedAt ?? 0) + s.at).toISOString(),
  }));

  if (m.fail && elapsed >= DONE_MS) {
    return {
      id: m.id,
      role: "assistant",
      status: "failed",
      content: "",
      sources: [],
      steps,
      createdAt: m.createdAt,
    };
  }

  if (elapsed >= DONE_MS) {
    return {
      id: m.id,
      role: "assistant",
      status: "done",
      content: ANSWER,
      sources: SOURCES,
      steps,
      createdAt: m.createdAt,
    };
  }

  // 부분 텍스트 — 폴링 주기마다 자라난다(§2 U-5).
  const ratio = Math.min(
    1,
    Math.max(0, (elapsed - CONTENT_START_MS) / (CONTENT_FULL_MS - CONTENT_START_MS)),
  );
  return {
    id: m.id,
    role: "assistant",
    status: "pending",
    content: m.fail ? "" : ANSWER.slice(0, Math.floor(ANSWER.length * ratio)),
    sources: [],
    steps,
    createdAt: m.createdAt,
  };
}

function renderMessages(conv: MockConversation): ChatMessage[] {
  return conv.messages.map((m) =>
    m.role === "user"
      ? {
          id: m.id,
          role: "user" as const,
          status: "done" as const,
          content: m.question,
          sources: [],
          steps: [],
          createdAt: m.createdAt,
        }
      : renderAssistant(m),
  );
}

function hasPending(conv: MockConversation): boolean {
  return renderMessages(conv).some(
    (m) => m.role === "assistant" && m.status === "pending",
  );
}

function summary(conv: MockConversation): Conversation {
  return { id: conv.id, title: conv.title, createdAt: conv.createdAt };
}

/** 실제 왕복처럼 조금 늦게 답한다 — 로딩 상태가 눈에 보이게. */
const delay = (ms = 180) => new Promise((r) => setTimeout(r, ms));

function appendTurn(conv: MockConversation, question: string): ChatMessage[] {
  const now = new Date().toISOString();
  const user: MockMessage = { id: nextId(), role: "user", question, createdAt: now };
  const assistant: MockMessage = {
    id: nextId(),
    role: "assistant",
    question,
    createdAt: now,
    startedAt: Date.now(),
    fail: question.includes(FAIL_TRIGGER),
  };
  conv.messages.push(user, assistant);
  return renderMessages(conv).slice(-2);
}

export const chatMock: ChatClient = {
  async listConversations() {
    await delay(120);
    return [...store.values()].reverse().map(summary);
  },

  async createConversation(question) {
    assertQuestion(question);
    await delay();
    const q = question.trim();
    const conv: MockConversation = {
      id: nextId(),
      // 제목은 첫 질문에서 딴다 — 최대 50자(§2 U-4).
      title: q.length > 50 ? `${q.slice(0, 50)}…` : q,
      createdAt: new Date().toISOString(),
      messages: [],
    };
    store.set(conv.id, conv);
    const messages = appendTurn(conv, q);
    return { conversation: summary(conv), messages };
  },

  async getConversation(id) {
    const conv = find(id);
    return { conversation: summary(conv), messages: renderMessages(conv) };
  },

  async sendMessage(id, question) {
    assertQuestion(question);
    const conv = find(id);
    // 직렬화 — pending 이 있으면 409(§5). FE 는 잠금으로 선차단한다.
    if (hasPending(conv)) throw new ChatApiError(409, "CONVERSATION_BUSY", "답변 대기 중");
    await delay();
    return { messages: appendTurn(conv, question.trim()) };
  },

  async retryMessage(id, messageId) {
    const conv = find(id);
    if (hasPending(conv)) throw new ChatApiError(409, "CONVERSATION_BUSY", "답변 대기 중");

    const target = conv.messages.find((m) => String(m.id) === String(messageId));
    const live = renderMessages(conv).find((m) => String(m.id) === String(messageId));
    // 대상이 failed assistant 가 아니면 404(§3 S-8 3항).
    if (!target || target.role !== "assistant" || live?.status !== "failed")
      throw new ChatApiError(404, "NOT_FOUND", "재시도 대상이 아님");

    await delay();
    // **그 자리에서** pending 으로 되돌린다 — 새 줄을 만들지 않는다.
    target.startedAt = Date.now();
    // mock 편의: 재시도는 성공한다. 안 그러면 같은 질문이라 영원히 실패한다.
    target.fail = false;
    return { message: renderAssistant(target) };
  },
};

/** 타입만 쓰는 재수출 — mock 을 읽는 쪽이 shape 을 확인할 수 있게. */
export type { ConversationDetail };
