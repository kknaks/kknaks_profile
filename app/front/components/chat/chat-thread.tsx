"use client";

import type { ChatId, ChatMessage, ChatSource } from "@/lib/chat";
import { SourceCards } from "@/components/chat/source-cards";
import { ToolSteps } from "@/components/chat/tool-steps";

/**
 * 대화 스레드 (§2 U-5) — 질문은 `$ ask "…"` 커맨드 줄, 답변은 좌측 액센트 보더의
 * 출력 블록. `pending` 중에는 부분 텍스트가 폴링 주기마다 자라난다.
 */
export function ChatThread({
  messages,
  onRetry,
  onOpenSource,
}: {
  messages: ChatMessage[];
  /** 실패한 답변의 「다시 시도」 — 그 메시지를 그 자리에서 되살린다(§3 S-8 3항). */
  onRetry: (messageId: ChatId) => void;
  /** 근거 카드 클릭 — 패널로 여는 유형만 온다(§2 U-5). */
  onOpenSource: (source: ChatSource) => void;
}) {
  return (
    <>
      {messages.map((m) =>
        m.role === "user" ? (
          <QuestionLine key={String(m.id)} text={m.content} />
        ) : (
          <AnswerBlock
            key={String(m.id)}
            message={m}
            onRetry={() => onRetry(m.id)}
            onOpenSource={onOpenSource}
          />
        ),
      )}
    </>
  );
}

function QuestionLine({ text }: { text: string }) {
  return (
    <div className="chat-msg-q">
      <span className="prompt">$</span>
      <span>
        ask <span className="cmd">&quot;{text}&quot;</span>
      </span>
    </div>
  );
}

function AnswerBlock({
  message,
  onRetry,
  onOpenSource,
}: {
  message: ChatMessage;
  onRetry: () => void;
  onOpenSource: (source: ChatSource) => void;
}) {
  const pending = message.status === "pending";
  const failed = message.status === "failed";
  // 부분 텍스트는 문단 사이 빈 줄로만 나눈다 — 줄바꿈은 pre-wrap 이 살린다.
  const paragraphs = message.content ? message.content.split(/\n{2,}/) : [];

  return (
    <div>
      <ToolSteps steps={message.steps ?? []} running={pending} />
      <div className="chat-msg-a">
        {failed ? (
          <>
            <p className="failed">답변 생성에 실패했습니다. 다시 시도해 주세요.</p>
            <button type="button" className="chat-retry" onClick={onRetry}>
              다시 시도
            </button>
          </>
        ) : (
          <>
            {paragraphs.map((p, i) => (
              <p key={i}>{p}</p>
            ))}
            {/* 부분 텍스트가 아직 없으면 인디케이터만, 오기 시작하면 뒤에 붙여 둔다. */}
            {pending && (
              <span className="chat-typing" aria-label="답변 생성 중">
                <i />
                <i />
                <i />
              </span>
            )}
            <SourceCards sources={message.sources ?? []} onOpen={onOpenSource} />
          </>
        )}
      </div>
    </div>
  );
}
