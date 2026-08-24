/**
 * §01 Problem panel — proto-algorithms.jsx ProblemPanel 이식.
 * 지문 카드 (statement + constraints) + 입출력 예시.
 */

import type { AlgoProblem, AlgorithmSource } from "@/lib/types";

export function ProblemPanel({
  algoSlug,
  problem,
  source,
}: {
  algoSlug: string;
  problem: AlgoProblem;
  source: AlgorithmSource;
}) {

  return (
    <div
      className="m-stack"
      style={{ display: "grid", gridTemplateColumns: "1.4fr 1fr", gap: 24 }}
    >
      <div className="card" style={{ padding: 28 }}>
        <div
          style={{
            display: "flex",
            alignItems: "baseline",
            gap: 12,
            marginBottom: 14,
            flexWrap: "wrap",
          }}
        >
          <span className="mono" style={{ fontSize: 11, color: "var(--fg-3)" }}>
            P.{algoSlug}
          </span>
          {problem.title && (
            <h3 style={{ margin: 0, fontSize: 18, fontWeight: 600, letterSpacing: "-0.01em" }}>
              {problem.title}
            </h3>
          )}
          <a
            href={source.url ?? undefined}
            target="_blank"
            rel="noreferrer"
            className="mono"
            style={{
              marginLeft: "auto",
              fontSize: 10,
              color: "var(--accent)",
              textDecoration: "none",
              padding: "2px 6px",
              border: "1px solid var(--accent-line)",
              borderRadius: 3,
            }}
          >
            ↗ {source.platform} #{source.number}
          </a>
        </div>
        <p style={{ margin: 0, fontSize: 14, lineHeight: 1.7, color: "var(--fg-1)" }}>
          {problem.statement}
        </p>

        {problem.constraints?.length > 0 && (
          <>
            <div className="caps" style={{ marginTop: 22, marginBottom: 8 }}>
              {"제약"}
            </div>
            <ul style={{ margin: 0, padding: 0, listStyle: "none" }}>
              {problem.constraints.map((c, i) => (
                <li
                  key={i}
                  className="mono"
                  style={{
                    fontSize: 12,
                    color: "var(--fg-1)",
                    padding: "4px 0",
                    borderTop: i === 0 ? "none" : "1px dashed var(--line-1)",
                  }}
                >
                  · {c}
                </li>
              ))}
            </ul>
          </>
        )}

        <div className="mono" style={{ fontSize: 10, color: "var(--fg-3)", marginTop: 14, lineHeight: 1.6 }}>
          // {"지문은 본인 언어 요약 — 원문은 위 링크에서"}
        </div>
      </div>

      <div>
        <div className="caps" style={{ marginBottom: 8 }}>
          {"입출력 예시"}
        </div>
        <div style={{ display: "flex", flexDirection: "column", gap: 10 }}>
          {(problem.io ?? []).map((ex, i) => (
            <div key={i} className="card" style={{ padding: 0, overflow: "hidden" }}>
              <div
                className="mono"
                style={{
                  fontSize: 10,
                  color: "var(--fg-3)",
                  padding: "6px 12px",
                  borderBottom: "1px solid var(--line-1)",
                  display: "flex",
                  justifyContent: "space-between",
                }}
              >
                <span>example {i + 1}</span>
                <span>input → output</span>
              </div>
              <div
                className="m-stack"
                style={{ display: "grid", gridTemplateColumns: "1fr 1fr" }}
              >
                <pre
                  className="mono"
                  style={{
                    margin: 0,
                    padding: 12,
                    fontSize: 12,
                    color: "var(--fg-1)",
                    background: "var(--bg-0)",
                    borderRight: "1px solid var(--line-1)",
                    whiteSpace: "pre-wrap",
                    wordBreak: "break-word",
                    lineHeight: 1.5,
                    overflowX: "auto",
                  }}
                >
                  {ex.input}
                </pre>
                <pre
                  className="mono"
                  style={{
                    margin: 0,
                    padding: 12,
                    fontSize: 12,
                    color: "var(--accent)",
                    background: "var(--bg-0)",
                    whiteSpace: "pre-wrap",
                    wordBreak: "break-word",
                    lineHeight: 1.5,
                    overflowX: "auto",
                  }}
                >
                  {ex.output}
                </pre>
              </div>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}
