/**
 * /notes 머리 — career·projects 와 같은 구조(eyebrow + h1).
 * subtitle 은 백엔드가 내리지 않는다(erd 에 대응 컬럼 없음) — 기본 문구를 쓴다.
 */
export function NotesHeader({
  subtitle,
  totalCount,
}: {
  subtitle?: string;
  totalCount: number;
}) {
  return (
    <header
      className="pad-x m-pad-h"
      style={{
        padding: "56px 80px 32px",
        borderBottom: "1px solid var(--line-1)",
      }}
    >
      <div
        className="mono"
        style={{
          fontSize: 11,
          color: "var(--fg-3)",
          textTransform: "uppercase",
          letterSpacing: "0.14em",
          marginBottom: 12,
        }}
      >
        04 / Notes · {subtitle ?? "읽고 정리한 것"}
      </div>
      <div
        style={{ display: "flex", alignItems: "baseline", gap: 16, flexWrap: "wrap" }}
      >
        <h1
          className="m-h1"
          style={{
            fontSize: 56,
            lineHeight: 1.05,
            letterSpacing: "-0.025em",
            margin: 0,
            fontWeight: 600,
          }}
        >
          Notes
        </h1>
        <span className="mono" style={{ fontSize: 12, color: "var(--fg-3)" }}>
          {totalCount} 글
        </span>
      </div>
    </header>
  );
}
