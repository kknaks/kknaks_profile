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

  // career 와 education 을 **섹션으로 나눠** 각각 `startedOn DESC` 로 나열한다.
  const sortDesc = (arr: TimelineItem[]) =>
    [...arr].sort((a, b) => b.startedOn.localeCompare(a.startedOn));
  const roles = sortDesc(career["career[]"]);
  const education = sortDesc(career["education[]"]);
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

      {/* 커리어 | 교육 — 2열. 모바일(m-stack)에서는 세로로 쌓인다. */}
      <div
        className="pad-x m-stack"
        style={{
          padding: "48px 80px",
          display: "grid",
          gridTemplateColumns: "minmax(0, 1.6fr) minmax(0, 1fr)",
          gap: 64,
          alignItems: "start",
        }}
      >
        <section style={{ minWidth: 0 }}>
          <div
            className="mono"
            style={{
              fontSize: 11,
              textTransform: "uppercase",
              letterSpacing: "0.12em",
              marginBottom: 24,
              paddingBottom: 12,
              borderBottom: "1px solid var(--line-1)",
            }}
          >
            <span style={{ color: "var(--accent)" }}>{"// career"}</span>
            <span style={{ color: "var(--fg-3)", marginLeft: 12 }}>
              {meta?.totalYears ? `${meta.totalYears} · ` : ""}
              {totalRoles}
              {focusLines.length > 0 ? ` · ${focusLines.join(" ")}` : ""}
            </span>
          </div>
          <CareerTimeline items={roles} />
        </section>

        {education.length > 0 && (
          <section style={{ minWidth: 0 }}>
            <div
              className="mono"
              style={{
                fontSize: 11,
                textTransform: "uppercase",
                letterSpacing: "0.12em",
                marginBottom: 24,
                paddingBottom: 12,
                borderBottom: "1px solid var(--line-1)",
              }}
            >
              <span style={{ color: "var(--accent)" }}>{"// education"}</span>
              <span style={{ color: "var(--fg-3)", marginLeft: 12 }}>
                {education.length} course{education.length !== 1 ? "s" : ""}
              </span>
            </div>
            <CareerTimeline items={education} />
          </section>
        )}
      </div>
    </main>
  );
}
