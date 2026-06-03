/**
 * Solution reveal — Trace panel 끝 펼침. proto-algorithms.jsx SolutionReveal 이식.
 * 정답 코드 + 복잡도 + follow-up.
 */

import type { Lang } from "@/lib/i18n";
import type { AlgoSolution } from "@/lib/types";

export function SolutionReveal({
  solution,
  lang,
  onHide,
}: {
  solution: AlgoSolution;
  lang: Lang;
  onHide: () => void;
}) {
  const t = (ko: string, en: string) => (lang === "en" ? en : ko);

  if (!solution) {
    return (
      <div className="card" style={{ padding: 16 }}>
        <div className="mono" style={{ fontSize: 12, color: "var(--fg-3)" }}>
          {t("LLM 이 아직 solution 을 생성하지 않음.", "LLM has not generated solution yet.")}
        </div>
      </div>
    );
  }

  return (
    <div className="card" style={{ padding: 0, overflow: "hidden" }}>
      <div
        className="mono"
        style={{
          display: "flex",
          alignItems: "center",
          gap: 10,
          padding: "10px 14px",
          borderBottom: "1px solid var(--line-1)",
          background: "var(--bg-1)",
          fontSize: 11,
          color: "var(--fg-3)",
        }}
      >
        <span>solution.py</span>
        <span style={{ marginLeft: "auto", display: "flex", gap: 12 }}>
          <span>
            time <span style={{ color: "var(--accent)" }}>{solution.complexity.time}</span>
          </span>
          <span>
            space <span style={{ color: "var(--accent)" }}>{solution.complexity.space}</span>
          </span>
        </span>
        <button
          onClick={onHide}
          className="mono"
          style={{
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
      <pre
        className="mono"
        style={{
          margin: 0,
          padding: 16,
          background: "var(--bg-0)",
          fontSize: 12,
          color: "var(--fg-0)",
          lineHeight: 1.65,
          whiteSpace: "pre",
          overflowX: "auto",
        }}
      >
        {solution.code}
      </pre>
      {solution.followup && solution.followup.length > 0 && (
        <div style={{ padding: "14px 16px", borderTop: "1px solid var(--line-1)" }}>
          <div className="caps" style={{ marginBottom: 8 }}>
            {t("Follow-up", "follow-up")}
          </div>
          <ul style={{ margin: 0, padding: 0, listStyle: "none" }}>
            {solution.followup.map((f, i) => (
              <li
                key={i}
                style={{
                  fontSize: 13,
                  color: "var(--fg-1)",
                  padding: "5px 0",
                  borderTop: i === 0 ? "none" : "1px dashed var(--line-1)",
                  lineHeight: 1.5,
                }}
              >
                · {f}
              </li>
            ))}
          </ul>
        </div>
      )}
    </div>
  );
}
