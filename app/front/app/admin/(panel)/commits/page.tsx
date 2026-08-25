"use client";

import { useEffect, useMemo, useState } from "react";
import { adminApi, AuthError } from "@/lib/api";
import type {
  AdminCommitCalendar,
  AdminCommitCalendarDay,
  AdminCommitsPage,
} from "@/lib/types";

// 커밋 히스토리 — 조회 전용 + 하루 요약(daily) 재실행 버튼 하나.
// 위에서 아래로: 월 네비 → 한 줄 잔디 스트립(KST 날짜, 요약 실패 날은 빨간 점)
// → 레포 칩(그 달에 커밋이 있는 레포만) → 날짜 클릭 시 데일리 카드(AI 하루
// 요약·실패·미요약 상태 + 재요약) → 목록 표(50행 페이지네이션, 행 클릭 =
// message 원문 펼침). message 원문은 공개 표면에 절대 안 나가는 값 — 어드민
// 전용 확인 화면이다.

const PAGE_SIZE = 50;

/** /about 잔디(ContribGrass)와 같은 농도 계산 — 4단계 + 빈 칸. */
function levelColor(count: number): string {
  if (count <= 0) return "var(--bg-2)";
  if (count <= 2) return "oklch(0.42 0.14 152 / 0.45)";
  if (count <= 4) return "oklch(0.55 0.17 152 / 0.7)";
  if (count <= 7) return "oklch(0.68 0.19 152 / 0.85)";
  return "oklch(0.78 0.21 152)";
}

/** KST ISO(`2026-08-25T10:16:36+09:00`) → `08.25 10:16`. 파싱 없이 자른다. */
function fmtWhen(iso: string): string {
  return `${iso.slice(5, 7)}.${iso.slice(8, 10)} ${iso.slice(11, 16)}`;
}

/** `owner/name` → `name`. */
function repoName(slug: string): string {
  return slug.split("/").pop() ?? slug;
}

export default function AdminCommitsPage() {
  const today = useMemo(() => new Date(), []);
  const [cursor, setCursor] = useState({
    year: today.getFullYear(),
    month: today.getMonth() + 1,
  });
  const [repoId, setRepoId] = useState<number | null>(null);
  const [day, setDay] = useState<number | null>(null);
  const [page, setPage] = useState(1);
  const [expandedId, setExpandedId] = useState<number | null>(null);

  const [cal, setCal] = useState<AdminCommitCalendar | null>(null);
  const [list, setList] = useState<AdminCommitsPage | null>(null);
  const [loadError, setLoadError] = useState<string | null>(null);

  // 하루 요약 재실행 — 202 만 받고, 몇 초 간격으로 달력을 재조회해 결과를 줍는다.
  // baseline(dailyAt)이 바뀌면 요약이 착지한 것 — 폴링을 멈춘다.
  const [calTick, setCalTick] = useState(0);
  const [summarizing, setSummarizing] = useState<{
    day: number;
    baseline: string | null;
    startedAt: number;
  } | null>(null);

  // 모바일(≤720 — 어드민 기존 브레이크포인트)에서만 스트립을 7일씩 줄바꿈.
  const [isMobile, setIsMobile] = useState(false);
  useEffect(() => {
    const onResize = () => setIsMobile(window.innerWidth <= 720);
    onResize();
    window.addEventListener("resize", onResize);
    return () => window.removeEventListener("resize", onResize);
  }, []);

  // 달력 — 달·레포가 바뀌면 다시. 달을 바꾸면 칩 구성이 바뀐다.
  useEffect(() => {
    let alive = true;
    adminApi
      .commitCalendar(cursor.year, cursor.month, repoId)
      .then((c) => {
        if (!alive) return;
        setCal(c);
        setLoadError(null);
        // 달 이동으로 칩이 사라진 레포 필터는 해제한다.
        if (repoId != null && !c.repos.some((r) => r.id === repoId)) {
          setRepoId(null);
        }
      })
      .catch((e) => {
        if (!alive) return;
        setLoadError(e instanceof AuthError ? `${e.status} — ${e.message}` : String(e));
      });
    return () => {
      alive = false;
    };
  }, [cursor, repoId, calTick]);

  // 목록 — 달·레포·날짜·페이지가 바뀌면 다시.
  useEffect(() => {
    let alive = true;
    adminApi
      .commits({ year: cursor.year, month: cursor.month, repoId, day, page })
      .then((p) => {
        if (!alive) return;
        setList(p);
        setLoadError(null);
        setExpandedId(null);
      })
      .catch((e) => {
        if (!alive) return;
        setLoadError(e instanceof AuthError ? `${e.status} — ${e.message}` : String(e));
      });
    return () => {
      alive = false;
    };
  }, [cursor, repoId, day, page]);

  function moveMonth(delta: number) {
    setCursor((c) => {
      const d = new Date(c.year, c.month - 1 + delta, 1);
      return { year: d.getFullYear(), month: d.getMonth() + 1 };
    });
    setDay(null);
    setPage(1);
  }

  function pickRepo(id: number | null) {
    setRepoId(id);
    setPage(1);
  }

  function pickDay(d: number) {
    setDay((cur) => (cur === d ? null : d)); // 재클릭 = 해제
    setPage(1);
  }

  const daysInMonth = new Date(cursor.year, cursor.month, 0).getDate();
  const dayInfo = useMemo(() => {
    const m = new Map<number, AdminCommitCalendarDay>();
    cal?.days.forEach((d) => m.set(d.day, d));
    return m;
  }, [cal]);

  // 요약 결과 감시 — dailyAt 이 baseline 에서 움직이면 착지한 것.
  useEffect(() => {
    if (!summarizing) return;
    const entry = dayInfo.get(summarizing.day);
    if ((entry?.dailyAt ?? null) !== summarizing.baseline) setSummarizing(null);
  }, [dayInfo, summarizing]);

  // 폴링 — 5초 간격 재조회, 3분 지나면 포기(다음 방문 때 보인다).
  useEffect(() => {
    if (!summarizing) return;
    const id = setInterval(() => {
      if (Date.now() - summarizing.startedAt > 180_000) {
        setSummarizing(null);
        return;
      }
      setCalTick((t) => t + 1);
    }, 5000);
    return () => clearInterval(id);
  }, [summarizing]);

  async function requestSummarize(d: number) {
    const dateStr = `${cursor.year}-${String(cursor.month).padStart(2, "0")}-${String(d).padStart(2, "0")}`;
    setSummarizing({
      day: d,
      baseline: dayInfo.get(d)?.dailyAt ?? null,
      startedAt: Date.now(),
    });
    try {
      await adminApi.summarizeDaily(dateStr);
    } catch (e) {
      setSummarizing(null);
      setLoadError(e instanceof AuthError ? `${e.status} — ${e.message}` : String(e));
    }
  }

  const totalPages = list ? Math.max(1, Math.ceil(list.total / list.pageSize)) : 1;
  const mm = String(cursor.month).padStart(2, "0");

  return (
    <div className="admin-page" style={{ padding: "28px 32px", maxWidth: 960, margin: "0 auto" }}>
      <header style={{ marginBottom: 20 }}>
        <h1 style={{ fontSize: 22, color: "var(--fg-0)", margin: 0 }}>커밋 히스토리</h1>
        <p className="mono" style={{ fontSize: 12, color: "var(--fg-3)", marginTop: 6 }}>
          commit — 수집기가 채운 원본. 조회 전용 · 날짜는 KST 기준 · message 원문은 여기서만 본다
        </p>
      </header>

      {loadError && (
        <p className="mono" style={{ fontSize: 12, color: "var(--danger, #e5534b)", marginBottom: 12 }}>
          불러오지 못했습니다 — {loadError}
        </p>
      )}

      {/* ── 1. 월 네비 ──────────────────────────────────────────────── */}
      <div style={{ display: "flex", alignItems: "center", gap: 12, marginBottom: 14 }}>
        <button type="button" onClick={() => moveMonth(-1)} aria-label="이전 달" style={navBtn}>
          ◀
        </button>
        <span className="mono" style={{ fontSize: 14, color: "var(--fg-0)", minWidth: 110, textAlign: "center" }}>
          {cursor.year}년 {cursor.month}월
        </span>
        <button type="button" onClick={() => moveMonth(1)} aria-label="다음 달" style={navBtn}>
          ▶
        </button>
        <span className="mono" style={{ fontSize: 11, color: "var(--fg-3)", marginLeft: 4 }}>
          {cal ? `${cal.total}건` : "…"}
        </span>
        {day != null && (
          <span className="mono" style={{ fontSize: 11, color: "var(--accent)", marginLeft: "auto" }}>
            {cursor.month}월 {day}일 필터 — 재클릭으로 해제
          </span>
        )}
      </div>

      {/* ── 2. 한 줄 잔디 스트립 — 모바일만 7일씩 줄바꿈 ─────────────── */}
      <div
        style={{
          display: isMobile ? "grid" : "flex",
          ...(isMobile ? { gridTemplateColumns: "repeat(7, 1fr)" } : {}),
          gap: 3,
          marginBottom: 16,
        }}
      >
        {Array.from({ length: daysInMonth }, (_, i) => i + 1).map((d) => {
          const info = dayInfo.get(d);
          const count = info?.count ?? 0;
          const selected = day === d;
          return (
            <div
              key={d}
              onClick={() => pickDay(d)}
              title={`${cursor.year}.${mm}.${String(d).padStart(2, "0")} · ${count}건`}
              style={{ flex: isMobile ? undefined : 1, minWidth: 0, cursor: "pointer" }}
            >
              <div style={{ position: "relative" }}>
                <div
                  style={{
                    height: isMobile ? 34 : 22,
                    background: levelColor(count),
                    border: "1px solid oklch(1 0 0 / 0.04)",
                    borderRadius: 2,
                    outline: selected ? "1px solid var(--accent)" : "none",
                    outlineOffset: 1,
                    transition: "outline 80ms",
                  }}
                />
                {info?.dailyStatus === "error" && (
                  <span
                    title="하루 요약 실패 — 날짜를 눌러 재시도"
                    style={{
                      position: "absolute",
                      top: -2,
                      right: -2,
                      width: 6,
                      height: 6,
                      borderRadius: "50%",
                      background: "var(--danger, #e5534b)",
                      border: "1px solid var(--bg-0, transparent)",
                    }}
                  />
                )}
              </div>
              <div
                className="mono"
                style={{
                  marginTop: 2,
                  fontSize: 8,
                  textAlign: "center",
                  color: selected ? "var(--accent)" : "var(--fg-4)",
                }}
              >
                {d}
              </div>
            </div>
          );
        })}
      </div>

      {/* ── 3. 레포 칩 — 그 달에 커밋이 있는 레포만 ──────────────────── */}
      <div style={{ display: "flex", flexWrap: "wrap", gap: 6, marginBottom: 18 }}>
        <RepoChip
          label={`전체 ${cal?.total ?? "…"}`}
          active={repoId == null}
          onClick={() => pickRepo(null)}
        />
        {cal?.repos.map((r) => (
          <RepoChip
            key={r.id}
            label={`${repoName(r.slug)} ${r.count}`}
            title={r.slug}
            active={repoId === r.id}
            onClick={() => pickRepo(repoId === r.id ? null : r.id)}
          />
        ))}
      </div>

      {/* ── 3.5 데일리 카드 — 날짜 클릭 시, AI 하루 요약 상태 ─────────── */}
      {day != null && (
        <DailyCard
          entry={dayInfo.get(day) ?? null}
          busy={summarizing?.day === day}
          onSummarize={() => requestSummarize(day)}
        />
      )}

      {/* ── 4. 목록 표 — 행 클릭 = message 원문 + sha 펼침 ───────────── */}
      {!list ? (
        <p className="mono" style={{ fontSize: 12, color: "var(--fg-3)" }}>
          불러오는 중…
        </p>
      ) : list.items.length === 0 ? (
        <p className="mono" style={{ fontSize: 12, color: "var(--fg-3)" }}>
          커밋이 없습니다
        </p>
      ) : (
        <div style={{ border: "1px solid var(--line-1)", borderRadius: 8, background: "var(--bg-1)", overflow: "hidden" }}>
          <div style={{ ...rowGrid(isMobile), borderBottom: "1px solid var(--line-1)", padding: "8px 14px" }}>
            <span style={headCell}>날짜·시각</span>
            <span style={headCell}>레포</span>
            <span style={headCell}>summary</span>
          </div>
          {list.items.map((c) => {
            const open = expandedId === c.id;
            return (
              <div key={c.id} style={{ borderBottom: "1px solid var(--line-1)" }}>
                <div
                  onClick={() => setExpandedId(open ? null : c.id)}
                  style={{
                    ...rowGrid(isMobile),
                    padding: "9px 14px",
                    cursor: "pointer",
                    background: open ? "var(--bg-2)" : "transparent",
                  }}
                >
                  <span className="mono" style={{ fontSize: 11, color: "var(--fg-2)", whiteSpace: "nowrap" }}>
                    {fmtWhen(c.authoredAt)}
                  </span>
                  <span
                    className="mono"
                    title={c.repoSlug}
                    style={{
                      fontSize: 11,
                      color: "var(--fg-3)",
                      overflow: "hidden",
                      textOverflow: "ellipsis",
                      whiteSpace: "nowrap",
                    }}
                  >
                    {repoName(c.repoSlug)}
                  </span>
                  <span
                    style={{
                      fontSize: 12.5,
                      color: "var(--fg-1)",
                      overflow: "hidden",
                      textOverflow: "ellipsis",
                      whiteSpace: open ? "normal" : "nowrap",
                      lineHeight: 1.5,
                    }}
                  >
                    {c.summary ?? "—"}
                  </span>
                </div>
                {open && (
                  <div style={{ padding: "12px 14px 14px", background: "var(--bg-2)", borderTop: "1px solid var(--line-1)" }}>
                    <div className="mono" style={{ fontSize: 10, letterSpacing: "0.08em", color: "var(--fg-4)", marginBottom: 6 }}>
                      message 원문 — 어드민 전용 · 공개 표면에는 안 나간다
                    </div>
                    <pre
                      className="mono"
                      style={{
                        margin: 0,
                        fontSize: 11.5,
                        lineHeight: 1.6,
                        color: "var(--fg-1)",
                        whiteSpace: "pre-wrap",
                        wordBreak: "break-word",
                      }}
                    >
                      {c.message ?? "(원문 없음)"}
                    </pre>
                    <div className="mono" style={{ marginTop: 10, fontSize: 10, color: "var(--fg-4)", wordBreak: "break-all" }}>
                      sha {c.sha}
                      {c.author ? ` · ${c.author}` : ""}
                    </div>
                  </div>
                )}
              </div>
            );
          })}

          {/* 페이지네이션 — authored_at DESC 50행 */}
          <div style={{ display: "flex", alignItems: "center", gap: 10, padding: "10px 14px" }}>
            <span className="mono" style={{ fontSize: 11, color: "var(--fg-3)" }}>
              총 {list.total}건
            </span>
            <div style={{ marginLeft: "auto", display: "flex", alignItems: "center", gap: 8 }}>
              <button
                type="button"
                onClick={() => setPage((p) => Math.max(1, p - 1))}
                disabled={page <= 1}
                style={{ ...navBtn, opacity: page <= 1 ? 0.4 : 1 }}
              >
                ◀
              </button>
              <span className="mono" style={{ fontSize: 11, color: "var(--fg-2)" }}>
                {list.page} / {totalPages}
              </span>
              <button
                type="button"
                onClick={() => setPage((p) => Math.min(totalPages, p + 1))}
                disabled={page >= totalPages}
                style={{ ...navBtn, opacity: page >= totalPages ? 0.4 : 1 }}
              >
                ▶
              </button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}

/* ── 조각 ───────────────────────────────────────────────────────────── */

/** 데일리 카드 — 그날의 AI 하루 요약. 세 상태(요약됨·실패·미요약) + 버튼 하나.
 *  버튼은 셋 다 같은 API(POST /api/admin/daily/{date}/summarize) — 202 를 받고
 *  몇 초 간격 재조회로 결과를 줍는다. */
function DailyCard({
  entry,
  busy,
  onSummarize,
}: {
  entry: AdminCommitCalendarDay | null;
  busy: boolean;
  onSummarize: () => void;
}) {
  const status = entry?.dailyStatus ?? null;
  const btn = (label: string) => (
    <button
      type="button"
      onClick={onSummarize}
      disabled={busy}
      className="mono"
      style={{
        fontSize: 10,
        letterSpacing: "0.06em",
        padding: "4px 12px",
        borderRadius: 5,
        border: "1px solid var(--line-2)",
        background: "transparent",
        color: busy ? "var(--fg-4)" : "var(--accent)",
        cursor: busy ? "default" : "pointer",
        whiteSpace: "nowrap",
      }}
    >
      {busy ? "요약 중…" : label}
    </button>
  );

  return (
    <div
      style={{
        border: "1px solid var(--line-1)",
        borderRadius: 8,
        background: "var(--bg-1)",
        padding: "12px 14px",
        marginBottom: 18,
      }}
    >
      {status === "error" ? (
        <>
          <div style={{ display: "flex", alignItems: "baseline", gap: 10 }}>
            <span style={{ fontSize: 12.5, color: "var(--danger, #e5534b)" }}>
              ⚠ 요약 실패 — {entry?.dailyError ?? "사유 미상"}
            </span>
            <span style={{ marginLeft: "auto" }}>{btn("재시도")}</span>
          </div>
          <div className="mono" style={{ marginTop: 8, fontSize: 10, color: "var(--fg-4)" }}>
            실패 {entry?.dailyAt ? fmtWhen(entry.dailyAt) : "—"} · 다음 아침 판에 자동 재시도
          </div>
        </>
      ) : status === "ok" ? (
        <>
          <div style={{ display: "flex", gap: 10 }}>
            <ul style={{ margin: 0, paddingLeft: 18, flex: 1 }}>
              {(entry?.dailySummary ?? []).map((line, i) => (
                <li
                  key={i}
                  style={{ fontSize: 12.5, color: "var(--fg-1)", lineHeight: 1.7 }}
                >
                  {line}
                </li>
              ))}
            </ul>
            {btn("재요약")}
          </div>
          <div className="mono" style={{ marginTop: 8, fontSize: 10, color: "var(--fg-4)" }}>
            요약 {entry?.dailyAt ? fmtWhen(entry.dailyAt) : "—"} · 커밋 {entry?.count ?? 0}
          </div>
        </>
      ) : (
        <div style={{ display: "flex", alignItems: "baseline", gap: 10 }}>
          <span style={{ fontSize: 12.5, color: "var(--fg-2)" }}>
            아직 요약 전 — 내일 아침 판에 자동으로 돕니다
          </span>
          <span style={{ marginLeft: "auto" }}>{btn("지금 요약")}</span>
        </div>
      )}
    </div>
  );
}

function RepoChip({
  label,
  title,
  active,
  onClick,
}: {
  label: string;
  title?: string;
  active: boolean;
  onClick: () => void;
}) {
  return (
    <button
      type="button"
      onClick={onClick}
      title={title}
      className="mono"
      style={{
        fontSize: 10,
        letterSpacing: "0.06em",
        padding: "4px 10px",
        borderRadius: 999,
        cursor: "pointer",
        border: active ? "1px solid var(--accent)" : "1px solid var(--line-2)",
        background: active ? "var(--accent-soft)" : "transparent",
        color: active ? "var(--accent)" : "var(--fg-2)",
      }}
    >
      {label}
    </button>
  );
}

function rowGrid(isMobile: boolean): React.CSSProperties {
  return {
    display: "grid",
    gridTemplateColumns: isMobile ? "76px 84px 1fr" : "96px 150px 1fr",
    gap: 12,
    alignItems: "baseline",
  };
}

const headCell: React.CSSProperties = {
  fontFamily: "var(--font-mono)",
  fontSize: 9,
  letterSpacing: "0.12em",
  color: "var(--fg-4)",
};

const navBtn: React.CSSProperties = {
  fontSize: 10,
  fontFamily: "var(--font-mono)",
  padding: "4px 10px",
  borderRadius: 5,
  border: "1px solid var(--line-2)",
  background: "transparent",
  color: "var(--fg-2)",
  cursor: "pointer",
};
