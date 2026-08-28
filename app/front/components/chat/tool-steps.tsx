"use client";

import { useState } from "react";
import type { ChatStep } from "@/lib/chat";

/**
 * tool 호출 단계 박스 (§2 U-5a).
 *
 * - `pending` 중에도 폴링으로 단계가 하나씩 쌓인다 — 타이핑 인디케이터와 공존한다.
 * - **완료 후에는 접힌 상태가 기본**, 헤더를 누르면 펼친다. 진행 중에는 펼쳐 둔다.
 * - 호출이 0건이면 박스를 그리지 않는다.
 *
 * 여기 값(이름 · 소요 ms)은 소비자 폴딩 기록이다 — AI 자기 신고가 아니다(§5).
 */
export function ToolSteps({ steps, running }: { steps: ChatStep[]; running: boolean }) {
  // null = 아직 사람이 안 건드림 → 진행 중이면 펼침, 끝났으면 접힘.
  const [override, setOverride] = useState<boolean | null>(null);
  const open = override ?? running;

  if (steps.length === 0) return null;

  return (
    <div className="chat-steps">
      <button
        type="button"
        className="head"
        aria-expanded={open}
        onClick={() => setOverride(!open)}
      >
        <span>⚡ tool · {steps.length}단계</span>
        <span className={running ? "badge running" : "badge"}>
          {running ? "진행 중" : "완료"}
        </span>
      </button>
      {open && (
        <div className="body">
          {steps.map((s, i) => (
            <div className="step" key={`${s.tool}-${s.calledAt}-${i}`}>
              <span className="name">{s.tool}</span>
              <span className="args">({s.argsSummary})</span>
              <span className="ms">
                {typeof s.durationMs === "number" ? `${s.durationMs}ms` : "…"}
              </span>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}
