"use client";

/**
 * §03 논리 구조 panel — proto-algorithms.jsx LogicPanel 이식.
 * slot 별 단일 선택 (radio) + 정답 공개 + 옵션별 ▾ 이유.
 * format=slot 만 분기 (MVP, ADR-08). 다른 format 은 Unsupported.
 */

import { useState } from "react";

import type { AlgoLogic } from "@/lib/types";

export function LogicPanel({ logic }: { logic: AlgoLogic }) {

  if (logic?.format !== "slot") {
    return (
      <div className="card" style={{ padding: 24 }}>
        <div className="mono" style={{ fontSize: 12, color: "var(--fg-3)" }}>
          {`format='${logic?.format ?? "?"}' 은 후속 버전 지원 (ADR-08).`}
        </div>
      </div>
    );
  }

  return <SlotQuiz slots={logic.slots} />;
}

function SlotQuiz({ slots }: { slots: AlgoLogic["slots"] }) {
  const [picks, setPicks] = useState<Record<number, number>>({});
  const [revealed, setRevealed] = useState(false);
  const [expandedSet, setExpandedSet] = useState<Set<string>>(new Set());

  const totalSlots = slots.length;
  const filledCount = Object.keys(picks).length;
  const allFilled = filledCount === totalSlots;
  const correctSlots = slots.filter((slot, i) => {
    const picked = picks[i];
    return picked != null && slot.options[picked]?.type === "good";
  }).length;

  const pick = (slotIdx: number, optIdx: number) => {
    if (revealed) return;
    setPicks({ ...picks, [slotIdx]: optIdx });
  };
  const reveal = () => setRevealed(true);
  const reset = () => {
    setPicks({});
    setRevealed(false);
    setExpandedSet(new Set());
  };
  const toggleExpand = (key: string, e: React.MouseEvent) => {
    e.stopPropagation();
    const next = new Set(expandedSet);
    if (next.has(key)) next.delete(key);
    else next.add(key);
    setExpandedSet(next);
  };

  if (totalSlots === 0) {
    return (
      <div className="card" style={{ padding: 24 }}>
        <div className="mono" style={{ fontSize: 12, color: "var(--fg-3)" }}>
          {"LLM 이 아직 논리 구조를 생성하지 않음."}
        </div>
      </div>
    );
  }

  return (
    <div>
      <div
        className="mono"
        style={{
          fontSize: 11,
          color: "var(--fg-3)",
          marginBottom: 16,
          display: "flex",
          alignItems: "center",
          gap: 8,
          flexWrap: "wrap",
        }}
      >
        <span style={{ color: "var(--accent)" }}>● 1</span>
        <span>{"슬롯 출력"}</span>
        <span style={{ marginLeft: 4 }}>→</span>
        <span style={{ color: filledCount > 0 || revealed ? "var(--accent)" : "var(--fg-3)" }}>● 2</span>
        <span>{"슬롯별 선택"}</span>
        <span style={{ marginLeft: 4 }}>→</span>
        <span style={{ color: revealed ? "var(--accent)" : "var(--fg-3)" }}>● 3</span>
        <span>{"정답 공개"}</span>
        {revealed && (
          <span
            className="mono"
            style={{
              marginLeft: "auto",
              fontSize: 10,
              color: "var(--accent)",
              padding: "2px 6px",
              border: "1px solid var(--accent-line)",
              borderRadius: 3,
            }}
          >
            {correctSlots} / {totalSlots} {"정답"}
          </span>
        )}
      </div>

      <div className="mono" style={{ fontSize: 11, color: "var(--fg-3)", marginBottom: 14, lineHeight: 1.6 }}>
        // {"각 슬롯에 들어갈 코드 한 줄을 골라 알고리즘 흐름을 합성해보세요. 코드는 안 짜지만 논리 뼈대는 직접."}
      </div>

      <div style={{ display: "flex", flexDirection: "column", gap: 14 }}>
        {slots.map((slot, sIdx) => {
          const slotIndent = (slot.indent ?? 0) * 16;
          const picked = picks[sIdx];
          const slotCorrect = revealed && picked != null && slot.options[picked]?.type === "good";

          return (
            <div key={sIdx}>
              <div
                className="mono"
                style={{
                  display: "flex",
                  alignItems: "baseline",
                  gap: 8,
                  fontSize: 11,
                  color: "var(--fg-3)",
                  marginBottom: 6,
                  paddingLeft: slotIndent,
                }}
              >
                <span style={{ color: "var(--accent)" }}>step {sIdx + 1}</span>
                <span>· {slot.label}</span>
                {revealed && (
                  <span style={{ marginLeft: 6, fontSize: 11, color: slotCorrect ? "var(--accent)" : "#ff8b6e" }}>
                    {slotCorrect ? "✓" : "✗"}
                  </span>
                )}
                {(slot.indent ?? 0) > 0 && (
                  <span style={{ marginLeft: 6, color: "var(--fg-3)" }}>
                    {"│ ".repeat(slot.indent ?? 0)}
                    {"중첩"}
                  </span>
                )}
              </div>

              <div
                style={{
                  display: "flex",
                  flexDirection: "column",
                  gap: 6,
                  paddingLeft: slotIndent,
                }}
              >
                {slot.options.map((opt, oIdx) => {
                  const isPicked = picks[sIdx] === oIdx;
                  const isGood = opt.type === "good";
                  const expandKey = `${sIdx}-${oIdx}`;
                  const isExpanded = expandedSet.has(expandKey);

                  let bg = "var(--bg-1)";
                  let borderColor = "var(--line-1)";
                  let radioColor = "var(--fg-3)";
                  let radio = "○";
                  if (revealed) {
                    if (isPicked && isGood) {
                      bg = "var(--accent-soft)";
                      borderColor = "var(--accent-line)";
                      radioColor = "var(--accent)";
                      radio = "✓";
                    } else if (isPicked && !isGood) {
                      borderColor = "#ff8b6e88";
                      radioColor = "#ff8b6e";
                      radio = "✗";
                    } else if (!isPicked && isGood) {
                      borderColor = "var(--accent-line)";
                      radioColor = "var(--accent)";
                      radio = "!";
                    } else {
                      radio = "·";
                    }
                  } else if (isPicked) {
                    borderColor = "var(--line-2)";
                    radioColor = "var(--fg-0)";
                    radio = "●";
                  }

                  return (
                    <div
                      key={oIdx}
                      onClick={() => pick(sIdx, oIdx)}
                      className="card"
                      style={{
                        display: "grid",
                        gridTemplateColumns: "24px 1fr 28px",
                        gap: 12,
                        padding: "10px 14px",
                        background: bg,
                        borderColor,
                        borderWidth: 1,
                        borderStyle: "solid",
                        borderRadius: 4,
                        cursor: revealed ? "default" : "pointer",
                        transition: "all 100ms",
                        alignItems: "start",
                      }}
                    >
                      <div
                        className="mono"
                        style={{
                          color: radioColor,
                          fontSize: 13,
                          paddingTop: 2,
                          textAlign: "center",
                          lineHeight: 1.2,
                          userSelect: "none",
                        }}
                      >
                        {radio}
                      </div>
                      <div>
                        <pre
                          className="mono"
                          style={{
                            margin: 0,
                            fontSize: 12.5,
                            color: "var(--fg-0)",
                            whiteSpace: "pre-wrap",
                            lineHeight: 1.5,
                          }}
                        >
                          {opt.code}
                        </pre>
                        {isExpanded && opt.why && (
                          <div
                            style={{
                              marginTop: 8,
                              paddingTop: 8,
                              borderTop: "1px dashed var(--line-1)",
                              fontSize: 11.5,
                              color: isGood ? "var(--fg-1)" : "#ff8b6e",
                              lineHeight: 1.55,
                            }}
                          >
                            <span className="mono" style={{ marginRight: 6, color: "var(--fg-3)" }}>
                              {isGood ? "// 정답 이유" : "// distractor"}
                            </span>
                            {opt.why}
                          </div>
                        )}
                      </div>
                      {revealed && opt.why ? (
                        <button
                          onClick={(e) => toggleExpand(expandKey, e)}
                          className="mono"
                          aria-label={isExpanded ? "collapse" : "expand"}
                          style={{
                            background: "transparent",
                            border: "none",
                            color: isExpanded ? "var(--accent)" : "var(--fg-3)",
                            fontSize: 13,
                            cursor: "pointer",
                            padding: 0,
                            lineHeight: 1,
                            alignSelf: "start",
                          }}
                        >
                          {isExpanded ? "▴" : "▾"}
                        </button>
                      ) : (
                        <div />
                      )}
                    </div>
                  );
                })}
              </div>
            </div>
          );
        })}
      </div>

      <div style={{ display: "flex", gap: 10, alignItems: "center", marginTop: 18, padding: "12px 0" }}>
        {!revealed ? (
          <>
            <span className="mono" style={{ fontSize: 11, color: "var(--fg-3)" }}>
              {filledCount === 0
                ? "각 슬롯에 한 줄씩 골라보세요"
                : `${filledCount} / ${totalSlots} ${"슬롯 채움"}`}
            </span>
            <button
              onClick={reveal}
              disabled={!allFilled}
              className="mono"
              style={{
                marginLeft: "auto",
                background: allFilled ? "var(--accent)" : "transparent",
                color: allFilled ? "var(--accent-ink, #0a0b0d)" : "var(--fg-3)",
                border: "1px solid " + (allFilled ? "var(--accent)" : "var(--line-2)"),
                fontSize: 11,
                padding: "8px 16px",
                cursor: allFilled ? "pointer" : "not-allowed",
                borderRadius: 3,
                fontWeight: 600,
              }}
            >
              {"확인"}
            </button>
          </>
        ) : (
          <>
            <span className="mono" style={{ fontSize: 11, color: "var(--fg-3)" }}>
              {correctSlots === totalSlots
                ? "완벽 — 논리 뼈대 잘 잡았음. ▾ 로 이유 확인"
                : "▾ 로 각 옵션의 이유 펼쳐보기"}
            </span>
            <button
              onClick={reset}
              className="mono"
              style={{
                marginLeft: "auto",
                background: "transparent",
                border: "1px solid var(--line-2)",
                color: "var(--fg-2)",
                fontSize: 11,
                padding: "8px 12px",
                cursor: "pointer",
                borderRadius: 3,
              }}
            >
              ↺ {"다시"}
            </button>
          </>
        )}
      </div>

      <div className="mono" style={{ fontSize: 10, color: "var(--fg-3)", marginTop: 8, lineHeight: 1.6 }}>
        // {"format: slot — 다른 패턴(재귀·DP 등) 은 ordering·state-first 등 별도 format. ADR-08 후속."}
      </div>
    </div>
  );
}
