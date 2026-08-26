import { api } from "@/lib/api";
import { CareerView } from "@/components/career/career-view";
import type { CareerItem, EducationItem } from "@/lib/types";

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

  // career 와 education 을 각각 `startedOn DESC` 로 나열한다(가장 최근이 위).
  const sortDesc = <T extends { startedOn: string }>(arr: T[]) =>
    [...arr].sort((a, b) => b.startedOn.localeCompare(a.startedOn));
  const roles: CareerItem[] = sortDesc(career["career[]"]);
  const education: EducationItem[] = sortDesc(career["education[]"]);
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

      {/* 3열 — 사이드 | 타임라인 | 상세. 선택 상태가 필요해 client 로 넘긴다. */}
      <div className="pad-x m-pad-h" style={{ padding: "48px 80px" }}>
        <CareerView
          roles={roles}
          education={education}
          meta={{
            totalYears: meta?.totalYears,
            totalRoles,
            focusLines,
            educationCount: education.length,
          }}
        />
      </div>
    </main>
  );
}
