"use client";

import { useEffect, useMemo, useState } from "react";
import type { Lang } from "@/lib/i18n";
import type { ActivityEntry, ActivityResponse } from "@/lib/types";

interface Cell {
  date: Date;
  count: number;
  counts: ActivityEntry["counts"];
  summary: string | null;
  future: boolean;
}

const GAP = 3;

function levelColor(count: number): string {
  if (count <= 0) return "var(--bg-2)";
  if (count <= 2) return "oklch(0.42 0.14 152 / 0.45)";
  if (count <= 4) return "oklch(0.55 0.17 152 / 0.7)";
  if (count <= 7) return "oklch(0.68 0.19 152 / 0.85)";
  return "oklch(0.78 0.21 152)";
}

function fmtDateDot(d: Date): string {
  const y = d.getFullYear();
  const m = String(d.getMonth() + 1).padStart(2, "0");
  const dd = String(d.getDate()).padStart(2, "0");
  return `${y}.${m}.${dd}`;
}

function parseDateDot(s: string): Date {
  const [y, m, d] = s.split(".").map(Number);
  return new Date(y, m - 1, d);
}

export function ContribGrass({
  lang,
  activity,
}: {
  lang: Lang;
  activity: ActivityResponse;
}) {
  const t = (ko: string, en: string) => (lang === "en" ? en : ko);
  const items = activity["activity[]"];
  const total = activity.activity.totalCount;

  const { weeks, monthLabels } = useMemo(() => {
    const byKey: Record<string, ActivityEntry> = {};
    items.forEach((e) => {
      byKey[e.date] = e;
    });

    const todayStr = activity.activity.until ?? items.at(-1)?.date;
    const today = todayStr ? parseDateDot(todayStr) : new Date();
    today.setHours(0, 0, 0, 0);

    const totalDays = 53 * 7;
    const dayMs = 86_400_000;
    const todayDow = today.getDay();
    const startMs = today.getTime() - (totalDays - 1 - (6 - todayDow)) * dayMs;
    const start = new Date(startMs);
    start.setDate(start.getDate() - start.getDay());

    const cells: Cell[] = [];
    for (let i = 0; i < totalDays; i++) {
      const d = new Date(start.getTime() + i * dayMs);
      d.setHours(0, 0, 0, 0);
      const future = d > today;
      const entry = byKey[fmtDateDot(d)];
      cells.push({
        date: d,
        count: entry?.count ?? 0,
        counts: entry?.counts ?? {},
        summary: entry?.summary ?? null,
        future,
      });
    }

    const w: Cell[][] = [];
    for (let i = 0; i < 53; i++) w.push(cells.slice(i * 7, i * 7 + 7));

    const monthsKo = [
      "1월", "2월", "3월", "4월", "5월", "6월",
      "7월", "8월", "9월", "10월", "11월", "12월",
    ];
    const monthsEn = [
      "Jan", "Feb", "Mar", "Apr", "May", "Jun",
      "Jul", "Aug", "Sep", "Oct", "Nov", "Dec",
    ];
    const arr = lang === "en" ? monthsEn : monthsKo;
    const ml: { wi: number; label: string }[] = [];
    w.forEach((wk, wi) => {
      const first = wk[0];
      if (!first) return;
      if (first.date.getDate() <= 7) {
        ml.push({ wi, label: arr[first.date.getMonth()] });
      }
    });

    return { weeks: w, monthLabels: ml };
  }, [items, activity.activity.until, lang]);

  const [hover, setHover] = useState<{ wi: number; di: number } | null>(null);
  const [selected, setSelected] =
    useState<{ cell: Cell; wi: number; di: number } | null>(null);

  useEffect(() => {
    if (selected) return;
    for (let wi = weeks.length - 1; wi >= 0; wi--) {
      for (let di = 6; di >= 0; di--) {
        const c = weeks[wi]?.[di];
        if (c && !c.future && c.count > 0) {
          setSelected({ cell: c, wi, di });
          return;
        }
      }
    }
  }, [weeks, selected]);

  const dayLabels =
    lang === "en"
      ? ["", "Mon", "", "Wed", "", "Fri", ""]
      : ["", "월", "", "수", "", "금", ""];

  return (
    <div
      className="grass-wrap"
      style={{
        marginTop: 24,
        padding: 20,
        background: "var(--bg-1)",
        border: "1px solid var(--line-1)",
        borderRadius: 6,
        position: "relative",
        display: "grid",
        gridTemplateColumns: "minmax(0, 1fr) 260px",
        gap: 28,
        alignItems: "start",
      }}
    >
      <style>{`
        @media (max-width: 768px) {
          .grass-wrap { grid-template-columns: 1fr !important; }
          .grass-board-scroll { overflow-x: auto; overflow-y: hidden; }
          .grass-board-inner { min-width: max-content; }
        }
      `}</style>

      <div style={{ minWidth: 0 }}>
        <div
          style={{
            display: "flex",
            alignItems: "baseline",
            justifyContent: "space-between",
            marginBottom: 4,
          }}
        >
          <div className="mono" style={{ fontSize: 11, color: "var(--accent)" }}>
            // activity
          </div>
          <div className="mono" style={{ fontSize: 10, color: "var(--fg-3)" }}>
            {total} {t("회 · 지난 1년", "events · past year")}
          </div>
        </div>
        <div
          className="mono"
          style={{
            fontSize: 10,
            color: "var(--fg-3)",
            marginBottom: 12,
            lineHeight: 1.4,
          }}
        >
          {t(
            "AI가 분류한 커밋 · 노트 · 학습 활동",
            "AI-classified commits · notes · study",
          )}
        </div>

        <div className="grass-board-scroll" style={{ paddingBottom: 4 }}>
          <div className="grass-board-inner" style={{ width: "100%" }}>
            <div
              className="mono"
              style={{
                display: "grid",
                gridTemplateColumns: `18px repeat(${weeks.length}, 1fr)`,
                columnGap: GAP,
                fontSize: 9,
                color: "var(--fg-3)",
                marginBottom: 4,
                height: 12,
                lineHeight: "12px",
              }}
            >
              <span />
              {weeks.map((_, wi) => {
                const ml = monthLabels.find((m) => m.wi === wi);
                return (
                  <span key={wi} style={{ whiteSpace: "nowrap" }}>
                    {ml ? ml.label : ""}
                  </span>
                );
              })}
            </div>

            <div
              style={{
                display: "grid",
                gridTemplateColumns: `18px repeat(${weeks.length}, 1fr)`,
                columnGap: GAP,
                width: "100%",
              }}
            >
              <div style={{ display: "flex", flexDirection: "column", gap: GAP }}>
                {dayLabels.map((dl, i) => (
                  <span
                    key={i}
                    className="mono"
                    style={{
                      fontSize: 9,
                      color: "var(--fg-3)",
                      lineHeight: "11px",
                      display: "flex",
                      alignItems: "center",
                      minHeight: 11,
                    }}
                  >
                    {dl}
                  </span>
                ))}
              </div>
              {weeks.map((wk, wi) => (
                <div
                  key={wi}
                  style={{
                    display: "flex",
                    flexDirection: "column",
                    gap: GAP,
                    minWidth: 0,
                  }}
                >
                  {wk.map((cell, di) => {
                    const isSel =
                      selected && selected.wi === wi && selected.di === di;
                    const isHover =
                      hover && hover.wi === wi && hover.di === di;
                    return (
                      <div
                        key={di}
                        onMouseEnter={() => setHover({ wi, di })}
                        onMouseLeave={() => setHover(null)}
                        onClick={() =>
                          !cell.future &&
                          cell.count > 0 &&
                          setSelected({ cell, wi, di })
                        }
                        style={{
                          width: "100%",
                          aspectRatio: "1 / 1",
                          background: cell.future
                            ? "transparent"
                            : levelColor(cell.count),
                          border: cell.future
                            ? "none"
                            : "1px solid oklch(1 0 0 / 0.04)",
                          borderRadius: 1.5,
                          cursor:
                            cell.future || cell.count === 0
                              ? "default"
                              : "pointer",
                          outline: isSel
                            ? "1px solid var(--accent)"
                            : isHover
                              ? "1px solid var(--fg-2)"
                              : "none",
                          outlineOffset: 1,
                          transition: "outline 80ms",
                        }}
                      />
                    );
                  })}
                </div>
              ))}
            </div>
          </div>
        </div>

        <div
          style={{
            display: "flex",
            alignItems: "center",
            gap: 6,
            marginTop: 12,
            fontSize: 10,
          }}
        >
          <span className="mono" style={{ color: "var(--fg-3)" }}>
            {t("적음", "less")}
          </span>
          {[0, 1, 3, 5, 9].map((c) => (
            <span
              key={c}
              style={{
                width: 11,
                height: 11,
                background: levelColor(c),
                border: "1px solid oklch(1 0 0 / 0.04)",
                borderRadius: 1.5,
              }}
            />
          ))}
          <span className="mono" style={{ color: "var(--fg-3)" }}>
            {t("많음", "more")}
          </span>
        </div>
      </div>

      <div
        style={{
          minWidth: 0,
          borderLeft: "1px solid var(--line-1)",
          paddingLeft: 24,
          alignSelf: "stretch",
        }}
      >
        {selected && selected.cell && !selected.cell.future && selected.cell.count > 0 ? (
          <div>
            <div
              className="mono"
              style={{ fontSize: 11, color: "var(--accent)", marginBottom: 4 }}
            >
              // {Object.entries(selected.cell.counts)
                .filter(([, v]) => (v ?? 0) > 0)
                .map(([k, v]) => `${k}:${v}`)
                .join(" · ") || "—"}
            </div>
            <div
              className="mono"
              style={{ fontSize: 10, color: "var(--fg-3)", marginBottom: 14 }}
            >
              {fmtDateDot(selected.cell.date)} · {selected.cell.count}{" "}
              {t("회", "events")}
            </div>
            {selected.cell.summary && (
              <div
                style={{
                  fontSize: 14,
                  color: "var(--fg-0)",
                  lineHeight: 1.55,
                  fontWeight: 500,
                  marginBottom: 12,
                }}
              >
                {selected.cell.summary}
              </div>
            )}
            <p style={{ margin: 0, fontSize: 12, lineHeight: 1.65, color: "var(--fg-2)" }}>
              {t(
                "AI가 그날 작성한 노트·커밋·세션을 모아 한 줄로 요약하고, 관련 링크를 표시해요.",
                "AI summarises the day's notes/commits/sessions into one line and surfaces related links.",
              )}
            </p>
          </div>
        ) : (
          <div>
            <div
              className="mono"
              style={{ fontSize: 11, color: "var(--accent)", marginBottom: 4 }}
            >
              // summary
            </div>
            <div
              className="mono"
              style={{ fontSize: 10, color: "var(--fg-3)", marginBottom: 14 }}
            >
              {total} {t("회 · 지난 1년", "events · past year")}
            </div>
            <p style={{ margin: 0, fontSize: 12, lineHeight: 1.65, color: "var(--fg-2)" }}>
              {t(
                "잔디는 그날 AI가 가공한 활동 기록이에요. 셀을 클릭하면 그날 뭐를 했는지 볼 수 있어요.",
                "Each cell is an AI-curated record of that day's activity. Click a cell to see what happened.",
              )}
            </p>
          </div>
        )}
      </div>
    </div>
  );
}
