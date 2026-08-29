"use client";

/**
 * 대화 상세 — **읽기 전용** (KDEV-SPEC-017 §2 U-8).
 * 시각 정본: `21-html/admin-chat-mockup.html` 의 `#detail`.
 *
 * 스레드는 방문자 렌더(`components/chat/chat-thread.tsx`)를 그대로 쓴다 — 질문
 * 줄 · tool 단계 · 답변 · 근거 카드가 방문자가 본 그대로여야 하기 때문이다.
 * 어드민이 대화에 개입하는 기능은 없다(spec U-8) — 그래서 `onRetry` 도
 * `onOpenSource` 도 넘기지 않는다. 「다시 시도」는 그려지지 않고, 근거 카드는
 * 문서 패널 없이 링크로만 남는다. **폴링도 컴포저도 없다** — 정적 렌더다.
 */

import { ChatThread } from "@/components/chat/chat-thread";
import type { AdminConversationDetail } from "@/lib/admin-chat";

/** `2026-08-29T10:03:00+09:00` → `2026-08-29 10:03`. 파싱 없이 자른다. */
function fmtFull(iso: string): string {
  return `${iso.slice(0, 10)} ${iso.slice(11, 16)}`;
}

export function ChatDetailView({
  detail,
  onBack,
}: {
  detail: AdminConversationDetail;
  onBack: () => void;
}) {
  const { conversation, messages, sessionId } = detail;

  // 메타 줄의 수치는 실린 메시지에서 센다 — 계약에 없는 값이라 화면이 만든다.
  const toolCalls = messages.reduce((n, m) => n + (m.steps?.length ?? 0), 0);
  const sourceCount = messages.reduce((n, m) => n + (m.sources?.length ?? 0), 0);

  return (
    <div>
      <button type="button" className="achat-back" onClick={onBack}>
        ← 목록으로
      </button>

      <div className="achat-head" style={{ marginTop: 10 }}>
        <span className="crumb">admin / 채팅 /</span>
        <h1 style={{ fontSize: 17 }}>{conversation?.title ?? "대화"}</h1>
      </div>

      <div className="achat-meta">
        {sessionId != null && <span>세션 s#{String(sessionId)}</span>}
        {conversation?.createdAt && <span>{fmtFull(conversation.createdAt)} 시작</span>}
        <span>
          메시지 {messages.length} · tool 호출 {toolCalls} · 근거 {sourceCount}
        </span>
        <span>읽기 전용</span>
      </div>

      <div className="achat-thread">
        <ChatThread messages={messages} />
      </div>
    </div>
  );
}
