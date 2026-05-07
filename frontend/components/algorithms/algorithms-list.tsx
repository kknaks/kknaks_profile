/**
 * Algorithms 목록 — proto-algorithms.jsx AlgorithmsList 이식.
 * 오늘 카드 (큰 카드) + 회차 로그 (테이블).
 */

import Link from "next/link";

import type { Lang } from "@/lib/i18n";
import type { AlgorithmListItem } from "@/lib/types";

import { CurationChip, DiffBadge, PlatformChip } from "./algo-chips";

export function AlgorithmsList({
  meta,
  items,
  lang,
}: {
  meta: { subtitle: string; intro: string; totalCount: number; today: AlgorithmListItem | null };
  items: AlgorithmListItem[];
  lang: Lang;
}) {
  const t = (ko: string, en: string) => (lang === "en" ? en : ko);
  const today = meta.today;
  const rest = today ? items.filter((a) => a.id !== today.id) : items;

  return (
    <div>
      {/* Today — large card */}
      {today && (
        <section className="pad-x" style={{ padding: "48px 80px 24px" }}>
          <div
            className="caps"
            style={{ marginBottom: 16, display: "flex", alignItems: "center", gap: 10 }}
          >
            <span
              style={{
                width: 6,
                height: 6,
                borderRadius: "50%",
                background: "var(--accent)",
                boxShadow: "0 0 0 3px var(--accent-soft)",
              }}
            />
            {t("오늘의 항목", "today's entry")}
          </div>
          <Link
            href={`/algorithms/${today.id}${lang === "en" ? "?lang=en" : ""}`}
            style={{ textDecoration: "none", color: "inherit" }}
          >
            <article
              className="card m-stack"
              style={{
                overflow: "hidden",
                cursor: "pointer",
                display: "grid",
                gridTemplateColumns: "1.05fr 1fr",
              }}
            >
              {/* Left — problem statement preview */}
              <div
                style={{
                  position: "relative",
                  minHeight: 280,
                  background: "var(--bg-1)",
                  borderRight: "1px solid var(--line-1)",
                  padding: "28px 32px",
                  display: "flex",
                  flexDirection: "column",
                }}
              >
                <div
                  className="mono"
                  style={{
                    fontSize: 11,
                    color: "var(--fg-3)",
                    display: "flex",
                    gap: 10,
                    marginBottom: 14,
                  }}
                >
                  <span>{today.id}</span>
                  {today.day && <span style={{ color: "var(--accent)" }}>● {today.day}</span>}
                  <span style={{ marginLeft: "auto" }}>{today.date}</span>
                </div>
                <div
                  className="mono"
                  style={{ fontSize: 11, color: "var(--fg-3)", marginBottom: 8 }}
                >
                  // problem.statement
                </div>
                <div
                  style={{
                    padding: 16,
                    background: "var(--bg-0)",
                    border: "1px solid var(--line-1)",
                    fontSize: 13,
                    color: "var(--fg-1)",
                    lineHeight: 1.7,
                    borderRadius: 4,
                    flex: 1,
                    overflow: "hidden",
                  }}
                >
                  {today.summary}
                </div>
                <div style={{ display: "flex", gap: 6, marginTop: 14, flexWrap: "wrap" }}>
                  <DiffBadge level={today.difficulty} />
                  <PlatformChip source={today.source} />
                  <CurationChip source={today.source} />
                  {today.tags.map((tag) => (
                    <span key={tag} className="tag" style={{ fontSize: 10 }}>
                      #{tag}
                    </span>
                  ))}
                </div>
              </div>

              {/* Right — summary + 4 stages preview */}
              <div style={{ padding: "28px 32px", display: "flex", flexDirection: "column" }}>
                <div className="mono" style={{ fontSize: 11, color: "var(--fg-3)", marginBottom: 10 }}>
                  {t("주제", "topic")}
                </div>
                <h2
                  style={{
                    margin: "0 0 14px",
                    fontSize: 26,
                    lineHeight: 1.25,
                    letterSpacing: "-0.015em",
                    fontWeight: 600,
                  }}
                >
                  {today.title}
                </h2>
                <p style={{ margin: "0 0 18px", color: "var(--fg-1)", fontSize: 14, lineHeight: 1.65 }}>
                  {today.summary}
                </p>

                <div
                  className="mono"
                  style={{ fontSize: 11, color: "var(--fg-3)", marginTop: 6, marginBottom: 8 }}
                >
                  {t("4단계 도장", "four stages")}
                </div>
                <div
                  className="mono"
                  style={{
                    fontSize: 12,
                    color: "var(--fg-1)",
                    marginBottom: 18,
                    display: "flex",
                    flexDirection: "column",
                    gap: 4,
                  }}
                >
                  <span>· clarifying — {t("좋은 질문 골라내기", "pick the right questions")}</span>
                  <span>· approach — {t("맞는 후보·복잡도 고르기", "pick the right approach·complexity")}</span>
                  <span>
                    · logic —{" "}
                    <span style={{ color: "var(--accent)" }}>
                      {t("코드 합성 (slot quiz)", "code synthesis (slot quiz)")}
                    </span>
                  </span>
                  <span>· trace — {t("머릿속 dry-run", "mental dry-run")}</span>
                </div>

                <div style={{ marginTop: "auto", display: "flex", alignItems: "center", gap: 12 }}>
                  <span className="mono" style={{ fontSize: 11, color: "var(--fg-3)" }}>
                    {t("지하철에서 한 손으로", "one-thumb subway dojo")}
                  </span>
                  <span className="mono" style={{ fontSize: 11, color: "var(--accent)", marginLeft: "auto" }}>
                    {t("풀러가기", "enter")} →
                  </span>
                </div>
              </div>
            </article>
          </Link>
        </section>
      )}

      {/* List — log */}
      <section className="pad-x" style={{ padding: "24px 80px 64px" }}>
        <div
          className="caps"
          style={{ marginBottom: 16, display: "flex", alignItems: "center", gap: 12 }}
        >
          <span>{t("회차 로그", "log")}</span>
          <span className="mono" style={{ fontSize: 10, color: "var(--fg-3)", marginLeft: "auto" }}>
            {rest.length} {t("회차", "entries")}
          </span>
        </div>
        <ul style={{ margin: 0, padding: 0, listStyle: "none" }}>
          <li
            className="mono m-hide"
            style={{
              display: "grid",
              gridTemplateColumns: "76px 80px 1fr 80px 110px 160px 80px",
              gap: 20,
              padding: "8px 12px",
              fontSize: 10,
              color: "var(--fg-3)",
              textTransform: "uppercase",
              letterSpacing: "0.1em",
              borderBottom: "1px solid var(--line-1)",
            }}
          >
            <span>id</span>
            <span>day</span>
            <span>{t("주제", "topic")}</span>
            <span>diff</span>
            <span>source</span>
            <span>tags</span>
            <span style={{ textAlign: "right" }}>date</span>
          </li>
          {rest.map((a) => (
            <li
              key={a.id}
              style={{
                display: "grid",
                gridTemplateColumns: "76px 80px 1fr 80px 110px 160px 80px",
                gap: 20,
                padding: 0,
                borderTop: "1px solid var(--line-1)",
                alignItems: "center",
              }}
            >
              <Link
                href={`/algorithms/${a.id}${lang === "en" ? "?lang=en" : ""}`}
                style={{
                  display: "contents",
                  textDecoration: "none",
                  color: "inherit",
                }}
              >
                <span className="mono" style={{ fontSize: 11, color: "var(--fg-3)", padding: "18px 12px" }}>
                  {a.id}
                </span>
                <span className="mono" style={{ fontSize: 11, color: "var(--fg-2)", padding: "18px 0" }}>
                  {a.day ?? ""}
                </span>
                <div style={{ padding: "18px 0" }}>
                  <div style={{ fontSize: 15, color: "var(--fg-0)", marginBottom: 4 }}>{a.title}</div>
                  <div style={{ fontSize: 13, color: "var(--fg-2)", lineHeight: 1.5 }}>{a.summary}</div>
                </div>
                <div style={{ padding: "18px 0" }}>
                  <DiffBadge level={a.difficulty} />
                </div>
                <div style={{ padding: "18px 0" }}>
                  <PlatformChip source={a.source} />
                </div>
                <div style={{ padding: "18px 0", display: "flex", gap: 6, flexWrap: "wrap" }}>
                  {a.tags.slice(0, 2).map((tag) => (
                    <span key={tag} className="tag" style={{ fontSize: 10 }}>
                      #{tag}
                    </span>
                  ))}
                </div>
                <span
                  className="mono"
                  style={{ fontSize: 11, color: "var(--fg-3)", textAlign: "right", padding: "18px 12px" }}
                >
                  {a.date}
                </span>
              </Link>
            </li>
          ))}
        </ul>
      </section>
    </div>
  );
}
