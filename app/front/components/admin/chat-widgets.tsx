"use client";

/**
 * 어드민 채팅 인사이트 위젯 3종 (KDEV-SPEC-017 §2 U-8).
 * 시각 정본: `21-html/admin-chat-mockup.html` — 마크업·값을 그대로 옮겼다.
 *
 *   ① 최근 질문 피드   — 시각 + 질문 원문. 행 클릭 = 그 대화 상세로.
 *   ② 일별 질문 수     — 최근 30일 단일 시리즈 CSS 바 + hover 툴팁 + 요약 3수치.
 *                        **차트 라이브러리를 쓰지 않는다**(시안·발주 §7).
 *   ③ 근거 문서 Top 5  — 유형 태그 + 제목 + 횟수 + 최다 대비 막대.
 *
 * 스타일은 `globals.css` 의 `.achat-*` 블록. 색은 토큰뿐이다.
 */

import { sourceTypeLabel } from "@/lib/chat-doc";
import type {
  AdminDailyCount,
  AdminRecentQuestion,
  AdminTopSource,
} from "@/lib/admin-chat";
import type { ChatId } from "@/lib/chat";

/* ── 시각 표기 ─────────────────────────────────────────────────────────
   ISO 문자열을 **파싱하지 않고 자른다** — 어드민 커밋 화면(`fmtWhen`)과 같은
   관례다. 서버가 KST 로 주는 값을 브라우저 타임존으로 다시 굴리지 않는다. */

/** `2026-08-29T10:12:00+09:00` → `10:12`. */
function hhmm(iso: string): string {
  return iso.slice(11, 16);
}

/** `2026-08-29T…` → `08-29`. */
function mmdd(iso: string): string {
  return `${iso.slice(5, 7)}-${iso.slice(8, 10)}`;
}

/** `2026-08-29` → `08-29`. daily 의 `date` 는 날짜만 온다. */
function mmddDate(date: string): string {
  return `${date.slice(5, 7)}-${date.slice(8, 10)}`;
}

/**
 * 피드의 시각 칸 — 오늘이면 `10:12`, 어제면 `어제`, 그 전은 `08-27`(시안 ①).
 * 기준 「오늘」은 브라우저 날짜다 — 표시용이라 정밀할 필요가 없다.
 */
function feedTime(iso: string, todayIso: string, yesterdayIso: string): string {
  const day = iso.slice(0, 10);
  if (day === todayIso) return hhmm(iso);
  if (day === yesterdayIso) return "어제";
  return mmdd(iso);
}

function localDate(offsetDays = 0): string {
  const d = new Date();
  d.setDate(d.getDate() + offsetDays);
  return `${d.getFullYear()}-${String(d.getMonth() + 1).padStart(2, "0")}-${String(
    d.getDate(),
  ).padStart(2, "0")}`;
}

/* ── ① 최근 질문 피드 ─────────────────────────────────────────────── */

export function RecentQuestionsCard({
  items,
  onOpen,
}: {
  items: AdminRecentQuestion[];
  onOpen: (conversationId: ChatId) => void;
}) {
  const today = localDate();
  const yesterday = localDate(-1);

  return (
    <div className="achat-card">
      <div className="caps">
        최근 질문 <span className="sub">→ 클릭 시 해당 대화</span>
      </div>
      {items.length === 0 ? (
        <p className="achat-empty">아직 질문이 없습니다</p>
      ) : (
        <ul className="achat-feed">
          {items.map((q, i) => (
            <li key={`${String(q.conversationId)}-${q.askedAt}-${i}`}>
              <button type="button" onClick={() => onOpen(q.conversationId)}>
                <span className="t">{feedTime(q.askedAt, today, yesterday)}</span>
                <span className="q" title={q.question}>
                  {q.question}
                </span>
              </button>
            </li>
          ))}
        </ul>
      )}
    </div>
  );
}

/* ── ② 일별 질문 수 ───────────────────────────────────────────────── */

/** 시안의 높이 식 그대로 — 0 은 2px 바닥선, 그 밖은 최다 대비 118px 안에서. */
function barHeight(count: number, max: number): number {
  if (count <= 0) return 2;
  return Math.max(6, (count / Math.max(1, max)) * 118);
}

export function DailyQuestionsCard({
  daily,
  totalQuestions,
}: {
  daily: AdminDailyCount[];
  /** 요약 첫 칸 「총 질문」 — 30일 합계가 아니라 전체 누계(totals.questions). */
  totalQuestions: number;
}) {
  const max = daily.reduce((m, d) => Math.max(m, d.count), 0);
  const sum = daily.reduce((s, d) => s + d.count, 0);
  const avg = daily.length ? sum / daily.length : 0;
  const peak = daily.reduce<AdminDailyCount | null>(
    (best, d) => (best == null || d.count > best.count ? d : best),
    null,
  );

  // 축은 처음·중간·끝 셋(시안 `.axis`). 데이터가 짧으면 있는 것만 그린다.
  const axis =
    daily.length >= 3
      ? [daily[0], daily[Math.floor((daily.length - 1) / 2)], daily[daily.length - 1]]
      : daily;

  return (
    <div className="achat-card">
      <div className="caps">
        일별 질문 수 <span className="sub">최근 {daily.length || 30}일</span>
      </div>

      {daily.length === 0 ? (
        <p className="achat-empty">집계할 질문이 없습니다</p>
      ) : (
        <>
          <div className="achat-chart">
            {daily.map((d) => (
              <button
                key={d.date}
                type="button"
                className={d.count === 0 ? "bar zero" : "bar"}
                style={{ height: `${barHeight(d.count, max)}px` }}
                aria-label={`${mmddDate(d.date)} ${d.count}건`}
              >
                <span className="tip">
                  {mmddDate(d.date)} · {d.count}건
                </span>
              </button>
            ))}
          </div>
          <div className="achat-axis">
            {axis.map((d) => (
              <span key={d.date}>{mmddDate(d.date)}</span>
            ))}
          </div>
          <div className="achat-stat">
            <div>
              <b>{totalQuestions}</b>
              <span>총 질문</span>
            </div>
            <div>
              <b>{avg.toFixed(1)}</b>
              <span>일평균</span>
            </div>
            <div>
              <b>{peak?.count ?? 0}</b>
              <span>최다{peak ? `(${mmddDate(peak.date)})` : ""}</span>
            </div>
          </div>
        </>
      )}
    </div>
  );
}

/* ── ③ 근거 문서 Top ──────────────────────────────────────────────── */

export function TopSourcesCard({ items }: { items: AdminTopSource[] }) {
  const max = items.reduce((m, s) => Math.max(m, s.count), 0);

  return (
    <div className="achat-card">
      <div className="caps">
        근거로 많이 읽힌 문서 <span className="sub">sources 집계</span>
      </div>
      {items.length === 0 ? (
        <p className="achat-empty">아직 근거로 읽힌 문서가 없습니다</p>
      ) : (
        <ul className="achat-top">
          {items.map((s) => (
            <li key={`${s.type}-${s.slug}`}>
              <div className="row1">
                {/* 태그 표기는 근거 카드와 같은 자리에서 온다 — `company_product` 는 `product`. */}
                <span className="tag">{sourceTypeLabel(s.type)}</span>
                <span className="name" title={s.title}>
                  {s.title}
                </span>
                <span className="n">{s.count}</span>
              </div>
              <div className="track">
                <div
                  className="fill"
                  style={{ width: `${max > 0 ? (s.count / max) * 100 : 0}%` }}
                />
              </div>
            </li>
          ))}
        </ul>
      )}
    </div>
  );
}
