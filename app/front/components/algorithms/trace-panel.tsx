"use client";

/**
 * §04 Trace panel — proto-algorithms.jsx TracePanel 이식 (ADR-09 단순화 후 버전).
 * 코드 (read-only) + cases 리스트 + worked_example 펼침 + Solution 펼침.
 * step-by-step UI · 콜스택 viz · Predict 마커 폐기.
 */

import { useState } from "react";

import type { Lang } from "@/lib/i18n";
import type { AlgoSolution, AlgoTrace } from "@/lib/types";

import { SolutionReveal } from "./solution-reveal";

export function TracePanel({
  trace,
  solution,
  lang,
}: {
  trace: AlgoTrace;
  solution: AlgoSolution;
  lang: Lang;
}) {
  const t = (ko: string, en: string) => (lang === "en" ? en : ko);
  const [exampleOpen, setExampleOpen] = useState(false);
  const [solutionOpen, setSolutionOpen] = useState(false);

  if (!trace) {
    return (
      <div className="card" style={{ padding: 24 }}>
        <div className="mono" style={{ fontSize: 12, color: "var(--fg-3)" }}>
          {t("LLM 이 아직 trace 를 생성하지 않음.", "LLM has not generated trace yet.")}
        </div>
      </div>
    );
  }

  const code = trace.code ?? [];
  const cases = trace.cases ?? [];
  const worked = trace.worked_example;

  return (
    <div>
      {/* Code (read-only) — 긴 라인 시 카드 안에서만 가로 스크롤 (페이지 폭 유지) */}
      <div
        className="card"
        style={{
          padding: 0,
          overflow: "hidden",
          background: "var(--bg-0)",
          marginBottom: 18,
        }}
      >
        <div
          className="mono"
          style={{
            display: "flex",
            alignItems: "center",
            gap: 10,
            padding: "8px 14px",
            borderBottom: "1px solid var(--line-1)",
            background: "var(--bg-1)",
            fontSize: 11,
            color: "var(--fg-3)",
          }}
        >
          <span style={{ width: 10, height: 10, borderRadius: "50%", background: "#ff5f57" }} />
          <span style={{ width: 10, height: 10, borderRadius: "50%", background: "#febc2e" }} />
          <span style={{ width: 10, height: 10, borderRadius: "50%", background: "#28c840" }} />
          <span style={{ marginLeft: 12 }}>solution.py</span>
        </div>
        <div style={{ overflowX: "auto" }}>
          <div style={{ minWidth: "max-content" }}>
            {code.map((line, i) => (
              <div key={i} style={{ display: "grid", gridTemplateColumns: "40px 1fr" }}>
                <span
                  className="mono"
                  style={{
                    padding: "4px 8px",
                    textAlign: "right",
                    color: "var(--fg-3)",
                    fontSize: 12,
                    lineHeight: 1.65,
                    userSelect: "none",
                    borderRight: "1px solid var(--line-1)",
                  }}
                >
                  {i + 1}
                </span>
                <pre
                  className="mono"
                  style={{
                    margin: 0,
                    padding: "4px 16px",
                    color: "var(--fg-1)",
                    fontSize: 12,
                    lineHeight: 1.65,
                    whiteSpace: "pre",
                  }}
                >
                  {line}
                </pre>
              </div>
            ))}
          </div>
        </div>
      </div>

      {/* Cases list */}
      <div className="caps" style={{ marginBottom: 6 }}>
        {t("머릿속 dry-run 케이스", "mental dry-run cases")}
      </div>
      <div className="mono" style={{ fontSize: 11, color: "var(--fg-3)", marginBottom: 12, lineHeight: 1.6 }}>
        // {t(
          "각 케이스를 머릿속으로 따라가보세요. 막히면 아래 worked example 펼침.",
          "walk each case in your head; expand the worked example below if stuck."
        )}
      </div>
      <div style={{ display: "flex", flexDirection: "column", gap: 6, marginBottom: 18 }}>
        {cases.map((c, i) => (
          <div
            key={i}
            className="card"
            style={{
              padding: "10px 14px",
              display: "flex",
              alignItems: "center",
              gap: 10,
              flexWrap: "wrap",
              background: "var(--bg-1)",
            }}
          >
            <span className="mono" style={{ fontSize: 11, color: "var(--fg-3)", flex: "0 0 auto" }}>
              case {i + 1}
            </span>
            <pre
              className="mono"
              style={{
                margin: 0,
                fontSize: 12,
                color: "var(--fg-1)",
                whiteSpace: "pre-wrap",
                flex: "1 1 auto",
                minWidth: 0,
              }}
            >
              {c.input}
            </pre>
            <span className="mono" style={{ color: "var(--fg-3)", flex: "0 0 auto" }}>
              →
            </span>
            <pre
              className="mono"
              style={{
                margin: 0,
                fontSize: 12,
                color: "var(--accent)",
                whiteSpace: "pre-wrap",
                flex: "0 0 auto",
              }}
            >
              {c.expected}
            </pre>
          </div>
        ))}
      </div>

      {/* Worked example reveal */}
      {worked && (
        <div style={{ marginBottom: 18 }}>
          {!exampleOpen ? (
            <button
              onClick={() => setExampleOpen(true)}
              className="mono"
              style={{
                width: "100%",
                padding: "14px 18px",
                textAlign: "left",
                background: "var(--bg-1)",
                border: "1px solid var(--line-2)",
                color: "var(--fg-1)",
                fontSize: 12,
                cursor: "pointer",
                borderRadius: 4,
                display: "flex",
                alignItems: "center",
                gap: 12,
              }}
            >
              <span style={{ color: "var(--accent)", fontSize: 14 }}>▾</span>
              {t("예시 walked-through 보기 (답안지)", "show worked-through example (answer key)")}
              <span style={{ marginLeft: "auto", fontSize: 11, color: "var(--fg-3)" }}>{worked.input}</span>
            </button>
          ) : (
            <div
              className="card"
              style={{
                padding: "16px 20px",
                background: "var(--accent-soft)",
                borderColor: "var(--accent-line)",
              }}
            >
              <div
                style={{
                  display: "flex",
                  alignItems: "center",
                  gap: 12,
                  marginBottom: 12,
                  flexWrap: "wrap",
                }}
              >
                <span className="caps" style={{ marginBottom: 0, color: "var(--accent)" }}>
                  worked example
                </span>
                <pre className="mono" style={{ margin: 0, fontSize: 12, color: "var(--fg-1)" }}>
                  {worked.input}
                </pre>
                <button
                  onClick={() => setExampleOpen(false)}
                  className="mono"
                  style={{
                    marginLeft: "auto",
                    background: "transparent",
                    border: "1px solid var(--line-2)",
                    color: "var(--fg-2)",
                    fontSize: 10,
                    padding: "4px 8px",
                    cursor: "pointer",
                    borderRadius: 3,
                  }}
                >
                  ↑ {t("접기", "hide")}
                </button>
              </div>
              <ol style={{ margin: 0, paddingLeft: 20, listStyle: "decimal" }}>
                {worked.steps.map((s, i) => (
                  <li
                    key={i}
                    style={{ fontSize: 13, color: "var(--fg-0)", lineHeight: 1.7, padding: "4px 0" }}
                  >
                    {s}
                  </li>
                ))}
              </ol>
              <div
                style={{
                  marginTop: 12,
                  padding: "8px 14px",
                  background: "var(--bg-0)",
                  borderRadius: 4,
                  display: "flex",
                  gap: 12,
                  alignItems: "center",
                }}
              >
                <span className="mono" style={{ fontSize: 11, color: "var(--fg-3)" }}>
                  {t("정답", "answer")}
                </span>
                <span className="mono" style={{ fontSize: 13, color: "var(--accent)" }}>
                  {worked.answer}
                </span>
              </div>
            </div>
          )}
        </div>
      )}

      {/* Solution reveal */}
      <div>
        {!solutionOpen ? (
          <button
            onClick={() => setSolutionOpen(true)}
            className="mono"
            style={{
              width: "100%",
              padding: "14px 18px",
              textAlign: "left",
              background: "var(--bg-1)",
              border: "1px solid var(--line-2)",
              color: "var(--fg-1)",
              fontSize: 12,
              cursor: "pointer",
              borderRadius: 4,
              display: "flex",
              alignItems: "center",
              gap: 12,
            }}
          >
            <span style={{ color: "var(--accent)", fontSize: 14 }}>▾</span>
            {t("복잡도 · Follow-up 보기", "show complexity · follow-up")}
          </button>
        ) : (
          <SolutionReveal solution={solution} lang={lang} onHide={() => setSolutionOpen(false)} />
        )}
      </div>

      <div className="mono" style={{ fontSize: 10, color: "var(--fg-3)", marginTop: 14, lineHeight: 1.6 }}>
        // {t(
          "UI 가 walk-through 안 함 — 학습자가 머릿속으로. 막히면 worked example 펼침.",
          "UI does not walk-through — you do the dry-run mentally. Expand the worked example if stuck."
        )}
      </div>
    </div>
  );
}
