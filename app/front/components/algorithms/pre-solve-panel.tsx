"use client";

/**
 * §02 Pre-solve panel — proto-algorithms.jsx PreSolvePanel + Quiz 이식.
 * Clarifying·Approach 탭, 각 탭은 3단계 quiz (리스트 → 선택 → 정답 공개).
 * 각 카드 우측 ▾ chevron 으로 이유 펼침 (정답 공개 후만).
 */

import { useState } from "react";

import type { AlgoQuizItem } from "@/lib/types";

type Kind = "clarifying" | "approach";

export function PreSolvePanel({
  clarifying,
  approach,
}: {
  clarifying: { items: AlgoQuizItem[] };
  approach: { items: AlgoQuizItem[] };
}) {
  const [tab, setTab] = useState<Kind>("clarifying");

  const tabs: { id: Kind; label: string }[] = [
    { id: "clarifying", label: "Clarifying — 어떤 질문을 던질까" },
    { id: "approach", label: "Approach — 어떤 접근이 맞을까" },
  ];

  return (
    <div>
      <div
        className="m-stack"
        style={{
          display: "flex",
          gap: 0,
          marginBottom: 18,
          borderBottom: "1px solid var(--line-1)",
        }}
      >
        {tabs.map((tt) => (
          <button
            key={tt.id}
            onClick={() => setTab(tt.id)}
            className="mono"
            style={{
              background: "transparent",
              border: "none",
              borderBottom: tab === tt.id ? "2px solid var(--accent)" : "2px solid transparent",
              color: tab === tt.id ? "var(--fg-0)" : "var(--fg-3)",
              fontSize: 13,
              padding: "10px 18px",
              cursor: "pointer",
              marginBottom: -1,
            }}
          >
            {tt.label}
          </button>
        ))}
      </div>

      {tab === "clarifying" ? (
        <Quiz key="clarifying" items={clarifying.items} kind="clarifying" />
      ) : (
        <Quiz key="approach" items={approach.items} kind="approach" />
      )}
    </div>
  );
}

function Quiz({
  items,
  kind,
}: {
  items: AlgoQuizItem[];
  kind: Kind;
}) {
  const [selected, setSelected] = useState<Set<number>>(new Set());
  const [revealed, setRevealed] = useState(false);
  const [expandedSet, setExpandedSet] = useState<Set<number>>(new Set());

  const toggle = (idx: number) => {
    if (revealed) return;
    const next = new Set(selected);
    if (next.has(idx)) next.delete(idx);
    else next.add(idx);
    setSelected(next);
  };
  const toggleExpand = (idx: number, e: React.MouseEvent) => {
    e.stopPropagation();
    const next = new Set(expandedSet);
    if (next.has(idx)) next.delete(idx);
    else next.add(idx);
    setExpandedSet(next);
  };
  const reveal = () => setRevealed(true);
  const reset = () => {
    setSelected(new Set());
    setRevealed(false);
    setExpandedSet(new Set());
  };

  const total = items.length;
  const correctCount = items.filter((it, i) => {
    const isGood = it.type === "good";
    return (isGood && selected.has(i)) || (!isGood && !selected.has(i));
  }).length;

  if (total === 0) {
    return (
      <div className="card" style={{ padding: 24 }}>
        <div className="mono" style={{ fontSize: 12, color: "var(--fg-3)" }}>
          {"LLM 이 아직 항목을 생성하지 않음."}
        </div>
      </div>
    );
  }

  return (
    <div>
      {/* Step indicator (3 stages) */}
      <div
        className="mono"
        style={{
          fontSize: 11,
          color: "var(--fg-3)",
          marginBottom: 12,
          display: "flex",
          alignItems: "center",
          gap: 8,
          flexWrap: "wrap",
        }}
      >
        <span style={{ color: "var(--accent)" }}>● 1</span>
        <span>{"리스트 출력"}</span>
        <span style={{ marginLeft: 4 }}>→</span>
        <span style={{ color: revealed || selected.size > 0 ? "var(--accent)" : "var(--fg-3)" }}>● 2</span>
        <span>{"선택"}</span>
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
            {correctCount} / {total} {"정답"}
          </span>
        )}
      </div>

      <ul style={{ margin: 0, padding: 0, listStyle: "none" }}>
        {items.map((it, i) => {
          const isChecked = selected.has(i);
          const isGood = it.type === "good";
          const isCorrect = (isGood && isChecked) || (!isGood && !isChecked);
          const isExpanded = expandedSet.has(i);

          let icon = "☐";
          let iconColor = "var(--fg-3)";
          if (revealed) {
            if (isCorrect) {
              icon = isChecked ? "✓" : "·";
              iconColor = "var(--accent)";
            } else {
              icon = isChecked ? "✗" : "!";
              iconColor = "#ff8b6e";
            }
          } else if (isChecked) {
            icon = "☑";
            iconColor = "var(--fg-0)";
          }

          const label = kind === "clarifying" ? it.q ?? "" : it.name ?? "";

          return (
            <li
              key={i}
              onClick={() => toggle(i)}
              className="card"
              style={{
                display: "grid",
                gridTemplateColumns: "32px 1fr 32px",
                gap: 14,
                padding: "14px 18px",
                marginTop: i === 0 ? 0 : 8,
                cursor: revealed ? "default" : "pointer",
                borderColor: revealed
                  ? isCorrect
                    ? "var(--accent-line)"
                    : "#ff8b6e44"
                  : isChecked
                  ? "var(--line-2)"
                  : "var(--line-1)",
                background: revealed && isCorrect ? "var(--accent-soft)" : "var(--bg-1)",
                transition: "all 120ms",
                alignItems: "start",
              }}
            >
              <div
                className="mono"
                style={{
                  fontSize: 16,
                  color: iconColor,
                  lineHeight: 1.2,
                  paddingTop: 2,
                  textAlign: "center",
                  userSelect: "none",
                }}
              >
                {icon}
              </div>
              <div>
                <div
                  style={{
                    fontSize: 14,
                    color: "var(--fg-0)",
                    lineHeight: 1.5,
                    display: "flex",
                    alignItems: "baseline",
                    gap: 10,
                    flexWrap: "wrap",
                  }}
                >
                  {label}
                  {kind === "approach" && it.complexity && (
                    <span className="mono" style={{ fontSize: 11, color: "var(--fg-3)" }}>
                      · {it.complexity}
                    </span>
                  )}
                </div>
                {isExpanded && (
                  <div
                    style={{
                      marginTop: 8,
                      paddingTop: 8,
                      borderTop: "1px dashed var(--line-1)",
                      fontSize: 12,
                      color: isGood ? "var(--fg-1)" : "#ff8b6e",
                      lineHeight: 1.6,
                    }}
                  >
                    <span className="mono" style={{ marginRight: 6, color: "var(--fg-3)" }}>
                      {isGood ? "// 좋은 이유" : "// 안 좋은 이유"}
                    </span>
                    {it.why}
                  </div>
                )}
              </div>
              {revealed ? (
                <button
                  onClick={(e) => toggleExpand(i, e)}
                  className="mono"
                  aria-label={isExpanded ? "collapse" : "expand"}
                  style={{
                    background: "transparent",
                    border: "none",
                    color: isExpanded ? "var(--accent)" : "var(--fg-3)",
                    fontSize: 14,
                    cursor: "pointer",
                    padding: "2px 4px",
                    lineHeight: 1,
                    alignSelf: "start",
                  }}
                >
                  {isExpanded ? "▴" : "▾"}
                </button>
              ) : (
                <div />
              )}
            </li>
          );
        })}
      </ul>

      <div style={{ display: "flex", gap: 10, alignItems: "center", marginTop: 18, padding: "12px 0" }}>
        {!revealed ? (
          <>
            <span className="mono" style={{ fontSize: 11, color: "var(--fg-3)" }}>
              {selected.size === 0
                ? "던질 질문에 체크하고 확인을 누르세요"
                : `${selected.size} ${"개 선택"}`}
            </span>
            <button
              onClick={reveal}
              disabled={selected.size === 0}
              className="mono"
              style={{
                marginLeft: "auto",
                background: selected.size === 0 ? "transparent" : "var(--accent)",
                color: selected.size === 0 ? "var(--fg-3)" : "var(--accent-ink, #0a0b0d)",
                border: "1px solid " + (selected.size === 0 ? "var(--line-2)" : "var(--accent)"),
                fontSize: 11,
                padding: "8px 16px",
                cursor: selected.size === 0 ? "not-allowed" : "pointer",
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
              {correctCount === total
                ? "완벽 — 모두 맞혔어요. ▾ 로 이유 확인"
                : "▾ 로 각 카드의 이유 펼쳐보기"}
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
        // {"결과는 세션 메모리만 — 새로고침하면 초기화됩니다 (반복 학습)"}
      </div>
    </div>
  );
}
