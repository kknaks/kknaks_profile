"use client";

import { useState } from "react";

/**
 * 터미널 스타일 입력창 — 히어로 · `/chat` 빈 상태 · 하단 컴포저가 같이 쓴다.
 * 시안(`21-html/chat-home-mockup.html` `.ask`)의 마크업 그대로.
 *
 * - 빈 입력은 **전송하지 않는다** — 버튼을 비활성하지 않고 no-op(§2 U-1).
 * - `onSubmit` 이 `false` 를 돌려주면(422 등) 입력값을 지우지 않는다 — 고쳐서
 *   다시 보낼 수 있어야 한다.
 */
export function AskBox({
  placeholder,
  showBar = false,
  disabled = false,
  autoFocus = false,
  onSubmit,
}: {
  placeholder: string;
  /** 터미널 타이틀바(`~/kknaks — ask`) — 히어로에만 있다. */
  showBar?: boolean;
  /** 답변 대기 중 잠금(§2 U-6). */
  disabled?: boolean;
  autoFocus?: boolean;
  onSubmit: (question: string) => void | boolean | Promise<void | boolean>;
}) {
  const [value, setValue] = useState("");
  const [busy, setBusy] = useState(false);

  async function submit() {
    const question = value.trim();
    if (!question || disabled || busy) return;
    setBusy(true);
    try {
      const kept = await onSubmit(question);
      if (kept !== false) setValue("");
    } finally {
      setBusy(false);
    }
  }

  return (
    <div className="chat-ask">
      {showBar && (
        <div className="bar">
          <span className="dots">
            <i />
            <i />
            <i />
          </span>
          ~/kknaks — ask
        </div>
      )}
      <div className="row">
        <span className="prompt">$</span>
        <input
          type="text"
          value={value}
          placeholder={placeholder}
          disabled={disabled}
          autoFocus={autoFocus}
          onChange={(e) => setValue(e.target.value)}
          onKeyDown={(e) => {
            if (e.key === "Enter") {
              e.preventDefault();
              void submit();
            }
          }}
          aria-label="질문"
        />
        <button type="button" onClick={() => void submit()} disabled={disabled || busy}>
          전송 ↵
        </button>
      </div>
    </div>
  );
}
