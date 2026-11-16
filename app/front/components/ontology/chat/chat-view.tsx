"use client";

import { useCallback, useEffect, useMemo, useRef, useState } from "react";
import { useSearchParams } from "next/navigation";
import {
  CHAT_POLL_INTERVAL_MS,
  QUESTION_MAX_LENGTH,
  ontologyApi,
} from "@/lib/ontology/client";
import { isTimeout } from "@/lib/ontology/types";
import type { ChatMessage, KpiCard, ToolStep } from "@/lib/ontology/types";
import { OntologyShell } from "../shell";
import { StatusDot } from "../primitives";
import { AnswerBlocks } from "./answer-blocks";

/**
 * 채팅 — 단일 컬럼(우측 근거 그래프 패널을 두지 않는다, U-11).
 *
 * 상태 5종(U-9)이 전부 화면에 있다: `pending`(부분 텍스트 + 도구 단계 · **2초 폴링**) ·
 * `done`(답변 6블록) · `failed`+재시도 · 타임아웃 · 컴포저 잠금.
 * 스트리밍이 아니므로 커서 깜빡임·타이핑 애니메이션을 만들지 않는다.
 */

const THREAD_WIDTH = 820;

export function ChatView() {
  const searchParams = useSearchParams();
  const prefill = searchParams.get("q") ?? "";

  const [conversationId, setConversationId] = useState<string | null>(null);
  const [messages, setMessages] = useState<ChatMessage[]>([]);
  const [draft, setDraft] = useState(prefill);
  const [cards, setCards] = useState<KpiCard[] | null>(null);
  const [asOf, setAsOf] = useState<string | null>(null);
  const [nodeLabels, setNodeLabels] = useState<Record<string, string>>({});
  const [error, setError] = useState<string | null>(null);
  const threadRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    setDraft(prefill);
  }, [prefill]);

  // 빈 상태 카드의 dot·상태 라벨은 알림 KPI 파생이고, 칩 문구는 노드 라벨을 쓴다.
  useEffect(() => {
    let cancelled = false;
    ontologyApi
      .kpiCards()
      .then((res) => {
        if (cancelled) return;
        setCards(res.cards);
        setAsOf(res.as_of);
      })
      .catch(() => undefined);
    ontologyApi
      .graph()
      .then((res) => {
        if (cancelled) return;
        setNodeLabels(Object.fromEntries(res.nodes.map((node) => [node.node_id, node.name])));
      })
      .catch(() => undefined);
    return () => {
      cancelled = true;
    };
  }, []);

  const pending = messages.some((message) => message.status === "pending");

  // 2초 폴링 — `done`/`failed` 로 바뀌면 멈춘다.
  useEffect(() => {
    if (!conversationId || !pending) return;
    const timer = setInterval(() => {
      ontologyApi
        .getConversation(conversationId)
        .then((res) => setMessages(res.messages))
        .catch((err: Error) => setError(err.message));
    }, CHAT_POLL_INTERVAL_MS);
    return () => clearInterval(timer);
  }, [conversationId, pending]);

  useEffect(() => {
    threadRef.current?.scrollTo({ top: threadRef.current.scrollHeight, behavior: "smooth" });
  }, [messages]);

  const tooLong = draft.trim().length > QUESTION_MAX_LENGTH;

  const send = useCallback(
    async (question: string) => {
      const trimmed = question.trim();
      if (trimmed.length === 0) return; // 빈 입력은 no-op — 에러를 띄우지 않는다.
      if (trimmed.length > QUESTION_MAX_LENGTH) return;
      if (pending) return; // 409 를 사용자에게 노출하지 않는다 — 선차단.
      setError(null);
      setDraft("");
      try {
        const res = conversationId
          ? await ontologyApi.sendMessage(conversationId, trimmed)
          : await ontologyApi.createConversation(trimmed);
        setConversationId(res.conversation.id);
        setMessages(res.messages);
      } catch (err) {
        setError((err as Error).message);
      }
    },
    [conversationId, pending],
  );

  const retry = useCallback(
    async (messageId: string) => {
      if (!conversationId) return;
      try {
        const res = await ontologyApi.retryMessage(conversationId, messageId);
        setMessages(res.messages);
      } catch (err) {
        setError((err as Error).message);
      }
    },
    [conversationId],
  );

  const startNew = useCallback(() => {
    setConversationId(null);
    setMessages([]);
    setDraft("");
    setError(null);
  }, []);

  return (
    <OntologyShell cards={cards} asOf={asOf}>
      <div style={{ display: "flex", flexDirection: "column", flex: 1, minHeight: 0 }}>
        <div
          ref={threadRef}
          style={{ flex: 1, minHeight: 0, overflowY: "auto", padding: "32px 64px 8px" }}
        >
          <div style={{ maxWidth: THREAD_WIDTH, margin: "0 auto", display: "flex", flexDirection: "column", gap: 24 }}>
            {messages.length === 0 ? (
              <EmptyState cards={cards} onPick={send} />
            ) : (
              messages.map((message) =>
                message.role === "user" ? (
                  <UserBubble key={message.id} content={message.content} />
                ) : (
                  <AssistantBubble
                    key={message.id}
                    message={message}
                    nodeLabels={nodeLabels}
                    onRetry={() => retry(message.id)}
                    onFollowup={send}
                  />
                ),
              )
            )}
            {error && (
              <p style={{ margin: 0, fontSize: 12, color: "var(--ont-alert-text)" }}>
                요청을 처리하지 못했습니다 — {error}
              </p>
            )}
          </div>
        </div>

        <div style={{ flexShrink: 0, padding: "20px 64px 28px" }}>
          <div style={{ maxWidth: THREAD_WIDTH, margin: "0 auto", display: "flex", flexDirection: "column", gap: 8 }}>
            {messages.length > 0 && (
              <button
                type="button"
                onClick={startNew}
                style={{
                  alignSelf: "flex-end",
                  height: 26,
                  padding: "0 10px",
                  borderRadius: 6,
                  border: "1px solid var(--ont-border-card)",
                  background: "var(--ont-surface)",
                  fontSize: 12,
                  color: "var(--ont-body)",
                }}
              >
                새 대화
              </button>
            )}

            <Composer
              draft={draft}
              onChange={setDraft}
              onSubmit={() => send(draft)}
              locked={pending}
              tooLong={tooLong}
            />

            {tooLong && (
              <p style={{ margin: 0, fontSize: 12, color: "var(--ont-alert-text)" }}>
                질문은 1,000자까지 입력할 수 있습니다
              </p>
            )}

            <p style={{ margin: 0, fontSize: 12, color: "var(--ont-label)", display: "flex", alignItems: "center", gap: 6 }}>
              <svg width="12" height="12" viewBox="0 0 12 12" aria-hidden>
                <rect x="2.5" y="5" width="7" height="5.5" rx="1" stroke="var(--ont-label)" strokeWidth="1.4" fill="none" />
                <path d="M4 5V3.6a2 2 0 0 1 4 0V5" stroke="var(--ont-label)" strokeWidth="1.4" fill="none" />
              </svg>
              환자 실명·전화·생년월일은 답변에도 마스킹된 형태로만 나옵니다. 일 1회 배치
              데이터입니다.
            </p>
          </div>
        </div>
      </div>
    </OntologyShell>
  );
}

/* ─────────────────────────── 빈 상태 ─────────────────────────── */

interface StartCard {
  question: string;
  meta: string;
  /** 정적 카피 — 알림 KPI 가 있으면 라벨만 파생으로 덮는다. */
  fallbackLabel: string;
  derived: boolean;
  state: "알림" | "정상" | "미관측";
}

const START_CARDS: StartCard[] = [
  { question: "8월 매출이 왜 떨어졌어?", meta: "전제부터 확인합니다", fallbackLabel: "원인 질문", derived: true, state: "알림" },
  { question: "리뷰가 줄면 신환은 어떻게 돼?", meta: "채택 엣지 · lag 2w", fallbackLabel: "관계 질문", derived: true, state: "알림" },
  { question: "최근 4주 노쇼율 추이는?", meta: "골드 주별 View", fallbackLabel: "현황 질문", derived: false, state: "정상" },
  { question: "외국인 매출은 어디서 들어온 거야?", meta: "유입 채널은 관측되지 않습니다", fallbackLabel: "미관측", derived: false, state: "미관측" },
];

function EmptyState({ cards, onPick }: { cards: KpiCard[] | null; onPick: (q: string) => void }) {
  const alertCards = useMemo(
    () => (cards ?? []).filter((card) => card.node_state === "알림"),
    [cards],
  );

  return (
    <div style={{ display: "flex", flexDirection: "column", alignItems: "center", gap: 16, paddingTop: 48 }}>
      <span
        style={{
          width: 44,
          height: 44,
          borderRadius: 12,
          background: "var(--ont-grad-assistant)",
          display: "flex",
          alignItems: "center",
          justifyContent: "center",
          color: "#fff",
          fontSize: 20,
        }}
        aria-hidden
      >
        ✦
      </span>
      <h1 style={{ margin: 0, fontSize: 28, fontWeight: 700, letterSpacing: "-0.03em" }}>
        무엇이 궁금하세요?
      </h1>
      <p
        style={{
          margin: 0,
          maxWidth: 600,
          textAlign: "center",
          fontSize: 15,
          lineHeight: 1.7,
          color: "var(--ont-body)",
          textWrap: "pretty",
        }}
      >
        골드 KPI와 온톨로지 엣지를 근거로 답합니다. 모든 수치는 어느 테이블·기간에서 나왔는지 함께
        보여주고, 필요하면 브론즈 원본까지 내려갑니다.
      </p>

      <div style={{ width: "100%", marginTop: 16 }}>
        <div style={{ fontSize: 12, fontWeight: 700, letterSpacing: "0.04em", color: "var(--ont-muted)", marginBottom: 12 }}>
          지금 봐야 할 것에서 시작하기
        </div>
        <div style={{ display: "grid", gridTemplateColumns: "1fr 1fr", gap: 12 }}>
          {START_CARDS.map((card, index) => {
            const derivedCard = card.derived ? alertCards[index] : undefined;
            const label = derivedCard ? `알림 · ${derivedCard.label}` : card.fallbackLabel;
            const state = derivedCard ? "알림" : card.state;
            return (
              <button
                key={card.question}
                type="button"
                onClick={() => onPick(card.question)}
                style={{
                  textAlign: "left",
                  padding: "14px 16px",
                  borderRadius: 8,
                  border:
                    state === "미관측"
                      ? "1px dashed var(--ont-border-card)"
                      : "1px solid var(--ont-border)",
                  background: "var(--ont-surface)",
                  boxShadow: "var(--ont-shadow-card)",
                  display: "flex",
                  flexDirection: "column",
                  gap: 6,
                }}
              >
                <span style={{ display: "flex", alignItems: "center", gap: 6 }}>
                  <StatusDot state={state} size={7} />
                  <span style={{ fontSize: 12, color: "var(--ont-muted)" }}>{label}</span>
                </span>
                <span style={{ fontSize: 14, color: "var(--ont-ink)" }}>{card.question}</span>
                <span style={{ fontSize: 12, color: "var(--ont-muted)" }}>{card.meta}</span>
              </button>
            );
          })}
        </div>
      </div>
    </div>
  );
}

/* ─────────────────────────── 버블 ─────────────────────────── */

function UserBubble({ content }: { content: string }) {
  return (
    <div style={{ display: "flex", justifyContent: "flex-end" }}>
      <div
        style={{
          maxWidth: "70%",
          background: "var(--ont-ink)",
          color: "#fff",
          fontSize: 14,
          lineHeight: 1.6,
          borderRadius: "10px 10px 2px 10px",
          padding: "12px 16px",
          whiteSpace: "pre-wrap",
        }}
      >
        {content}
      </div>
    </div>
  );
}

function AssistantBubble({
  message,
  nodeLabels,
  onRetry,
  onFollowup,
}: {
  message: ChatMessage;
  nodeLabels: Record<string, string>;
  onRetry: () => void;
  onFollowup: (question: string) => void;
}) {
  // 타임아웃은 같은 버블이고 **문구로만** 구분한다. `error_code` 가 없으면
  // 일반 실패로 둔다 — 추측으로 「시간 초과」라고 말하지 않는다.
  const timedOut = isTimeout(message);

  return (
    <div style={{ display: "flex", gap: 12, alignItems: "flex-start" }}>
      <span
        aria-hidden
        style={{
          width: 28,
          height: 28,
          flexShrink: 0,
          borderRadius: 8,
          background: "var(--ont-grad-assistant)",
          color: "#fff",
          fontSize: 13,
          display: "flex",
          alignItems: "center",
          justifyContent: "center",
        }}
      >
        ✦
      </span>

      <div style={{ flex: 1, minWidth: 0, display: "flex", flexDirection: "column", gap: 12 }}>
        {message.steps.length > 0 && (
          <StepList steps={message.steps} collapsed={message.status !== "pending"} />
        )}

        {message.status === "failed" && (
          <div style={{ display: "flex", flexDirection: "column", gap: 10 }}>
            <span
              style={{
                alignSelf: "flex-start",
                height: 24,
                display: "inline-flex",
                alignItems: "center",
                padding: "0 9px",
                borderRadius: 6,
                background: "var(--ont-alert-fill)",
                color: "var(--ont-alert-text)",
                fontSize: 12,
                fontWeight: 600,
              }}
            >
              {timedOut ? "시간 초과" : "답변 실패"}
            </span>
            {/* 부분 텍스트를 지우지 않고 그 위에 배지를 얹는다. */}
            {message.content && (
              <p style={{ margin: 0, fontSize: 14, lineHeight: 1.75, color: "var(--ont-ink)", whiteSpace: "pre-wrap" }}>
                {message.content}
              </p>
            )}
            <p style={{ margin: 0, fontSize: 13, lineHeight: 1.6, color: "var(--ont-body)" }}>
              {timedOut
                ? "180초 안에 답이 오지 않았습니다. 다시 시도해 주세요."
                : "답변을 만들지 못했습니다. 다시 시도해 주세요."}
            </p>
            <button
              type="button"
              onClick={onRetry}
              style={{
                alignSelf: "flex-start",
                height: 30,
                padding: "0 12px",
                borderRadius: 8,
                border: "1px solid var(--ont-border-card)",
                background: "var(--ont-surface)",
                fontSize: 13,
                color: "var(--ont-body)",
              }}
            >
              다시 시도
            </button>
          </div>
        )}

        {message.status === "pending" && (
          <>
            {message.content && (
              <p style={{ margin: 0, fontSize: 14, lineHeight: 1.75, color: "var(--ont-ink)", whiteSpace: "pre-wrap" }}>
                {message.content}
              </p>
            )}
            <span style={{ fontSize: 12, color: "var(--ont-muted)" }}>
              답변을 만드는 중입니다 · 2초마다 갱신
            </span>
          </>
        )}

        {message.status === "done" && message.result && (
          <AnswerBlocks result={message.result} nodeLabels={nodeLabels} onFollowup={onFollowup} />
        )}

        {message.status === "done" && !message.result && (
          <p style={{ margin: 0, fontSize: 14, lineHeight: 1.75, whiteSpace: "pre-wrap" }}>
            {message.content}
          </p>
        )}
      </div>
    </div>
  );
}

/**
 * 도구 단계 리스트 — 도구명·인자 요약은 응답의 `steps[]` 값 그대로다. 화면이 짓지 않는다.
 * 단계가 0건이면 블록 자체를 만들지 않는다(빈 상자 금지).
 */
function StepList({ steps, collapsed }: { steps: ToolStep[]; collapsed: boolean }) {
  const done = steps.filter((s) => s.duration_ms !== null).length;
  // 도구 실패는 **개수도 파생**이다 — 실패가 섞였다는 사실을 헤더에서 먼저 알린다.
  const failed = steps.filter((s) => s.is_error).length;
  return (
    <details
      open={!collapsed}
      style={{
        borderRadius: 8,
        background: "var(--ont-canvas)",
        border: "1px solid var(--ont-border)",
        padding: "10px 12px",
      }}
    >
      <summary style={{ display: "flex", alignItems: "center", gap: 8, cursor: "pointer", listStyle: "none" }}>
        <span style={{ fontSize: 12, fontWeight: 700, color: "var(--ont-muted)" }}>
          {collapsed ? "밟은 도구" : "근거를 모으는 중"}
        </span>
        {failed > 0 && (
          <span style={{ fontSize: 12, color: "var(--ont-alert-text)" }}>· 실패 {failed}</span>
        )}
        <span className="ont-mono" style={{ marginLeft: "auto", fontSize: 12, color: "var(--ont-muted)" }}>
          {done}/{steps.length}
        </span>
      </summary>
      <div style={{ display: "flex", flexDirection: "column", gap: 6, marginTop: 8 }}>
        {steps.map((step, index) => (
          <div key={`${step.tool}-${index}`} style={{ height: 20, display: "flex", alignItems: "center", gap: 8 }}>
            {/* 진행 중 = 관찰 · 실패 = 알림 · 완료 = 정상. 새 색을 만들지 않는다(디자인 02). */}
            <span
              style={{
                width: 6,
                height: 6,
                borderRadius: "50%",
                background: step.is_error
                  ? "var(--ont-alert)"
                  : step.duration_ms === null
                    ? "var(--ont-watch)"
                    : "var(--ont-normal)",
                flexShrink: 0,
              }}
            />
            <span
              className="ont-mono"
              style={{
                fontSize: 12,
                fontWeight: 600,
                color: step.is_error ? "var(--ont-alert-text)" : "var(--ont-ink)",
              }}
            >
              {step.tool}
            </span>
            <span
              style={{
                fontSize: 12,
                color: "var(--ont-label)",
                whiteSpace: "nowrap",
                overflow: "hidden",
                textOverflow: "ellipsis",
              }}
            >
              {step.args_summary}
            </span>
            {step.duration_ms !== null && (
              <span className="ont-mono" style={{ marginLeft: "auto", fontSize: 12, color: "var(--ont-muted)" }}>
                {step.duration_ms}ms
              </span>
            )}
          </div>
        ))}
      </div>
    </details>
  );
}

/* ─────────────────────────── 컴포저 ─────────────────────────── */

function Composer({
  draft,
  onChange,
  onSubmit,
  locked,
  tooLong,
}: {
  draft: string;
  onChange: (value: string) => void;
  onSubmit: () => void;
  locked: boolean;
  tooLong: boolean;
}) {
  const empty = draft.trim().length === 0;
  return (
    <form
      onSubmit={(event) => {
        event.preventDefault();
        onSubmit();
      }}
      style={{
        height: 56,
        display: "flex",
        alignItems: "center",
        gap: 10,
        padding: "0 10px 0 16px",
        borderRadius: 8,
        background: locked ? "var(--ont-hover)" : "var(--ont-surface)",
        border: `1px solid ${tooLong ? "var(--ont-alert-border)" : locked ? "var(--ont-border)" : "var(--ont-border-card)"}`,
      }}
    >
      <span aria-hidden style={{ opacity: 0.34, fontSize: 18 }}>
        ✦
      </span>
      <input
        value={draft}
        disabled={locked}
        onChange={(event) => onChange(event.target.value)}
        placeholder={locked ? "답변을 만드는 중입니다 — 끝나면 이어서 물어볼 수 있습니다" : "무엇이든 물어보세요"}
        style={{
          flex: 1,
          minWidth: 0,
          height: "100%",
          border: "none",
          outline: "none",
          background: "transparent",
          fontSize: 15,
          color: "var(--ont-ink)",
        }}
      />
      <button
        type="submit"
        disabled={locked || empty || tooLong}
        aria-label="보내기"
        style={{
          width: 40,
          height: 40,
          borderRadius: 8,
          border: "none",
          background: "var(--ont-grad-assistant)",
          color: "#fff",
          opacity: locked ? 0.35 : empty || tooLong ? 0.55 : 1,
          pointerEvents: locked ? "none" : "auto",
          cursor: locked || empty || tooLong ? "not-allowed" : "pointer",
        }}
      >
        ↑
      </button>
    </form>
  );
}
