import { api } from "@/lib/api";
import { CareerTimeline } from "@/components/career/career-timeline";
import type { TimelineItem } from "@/lib/types";

export const dynamic = "force-dynamic";

export default async function CareerPage() {
  let career;
  try {
    career = await api.career();
  } catch (err) {
    return (
      <main className="pad-x" style={{ padding: "56px 80px" }}>
        <h1>Career</h1>
        <p style={{ color: "var(--danger)" }}>
          백엔드 응답 실패: {(err as Error).message}
        </p>
      </main>
    );
  }

  // 타임라인은 `career` 와 `education` 을 합쳐 `startedOn DESC` 로 나열한다
  // (database.md §education). 화면은 둘을 구분해 보여주지 않는다.
  const roles = career["career[]"];
  const items: TimelineItem[] = [...roles, ...career["education[]"]].sort((a, b) =>
    b.startedOn.localeCompare(a.startedOn),
  );
  const meta = career.career;
  const totalRoles = meta?.totalRoles ?? `${roles.length} role`;
  const focusLines = meta?.focus ? meta.focus.split("\n") : [];

  return (
    <main>
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
          02 / Career · 언제 · 어디서
        </div>
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
          Career
        </h1>
      </header>

      <div className="pad-x" style={{ padding: "48px 80px" }}>
        <div
          className="m-stack"
          style={{
            display: "grid",
            gridTemplateColumns: "180px 1fr",
            gap: 48,
          }}
        >
          <div
            className="mono"
            style={{
              fontSize: 11,
              color: "var(--fg-3)",
              textTransform: "uppercase",
              letterSpacing: "0.12em",
            }}
          >
            {meta?.totalYears && <div>// {meta.totalYears}</div>}
            <div>// {totalRoles}</div>
            {focusLines.length > 0 && (
              <div style={{ marginTop: 16, color: "var(--fg-2)" }}>
                focus
                <br />
                {focusLines.map((line, i) => (
                  <span key={i}>
                    <span style={{ color: "var(--fg-0)" }}>{line}</span>
                    {i < focusLines.length - 1 && <br />}
                  </span>
                ))}
              </div>
            )}
          </div>

          <CareerTimeline items={items} />
        </div>
      </div>
    </main>
  );
}
