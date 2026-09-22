"use client";

import Link from "next/link";
import { usePathname } from "next/navigation";
import { useEffect, useState, type ReactNode } from "react";
import { ontologyApi } from "@/lib/ontology/client";
import type { KpiCard } from "@/lib/ontology/types";

/**
 * 데모 셸 — 자체 h64 헤더(디자인 02). 포트폴리오 `TopNav`·`PageFooter` 는 이 그룹에
 * 주입되지 않는다(토큰 레이어의 `body:has(...)` 규칙이 가린다 — SPEC-004 AC-2).
 *
 * **배지 카운트와 기준일은 전부 응답 파생이다**(§4 파생 카운트 표):
 * - 모니터링 탭 배지 = `/api/kpi/cards` 중 `node_state === "알림"` 인 카드 수
 * - 기준일 배지 = `/api/kpi/cards.as_of`
 *
 * 이미 카드를 가진 화면(모니터링·채팅)은 `cards` 를 내려 준다 — 같은 응답을 두 번
 * 부르지 않기 위해서다. 없으면 셸이 직접 한 번 받는다.
 */

const TABS = [
  { href: "/ontology/monitoring", label: "모니터링", badge: true },
  { href: "/ontology/chat", label: "채팅", badge: false },
  { href: "/ontology/data", label: "데이터", badge: false },
] as const;

export function OntologyShell({
  children,
  cards,
  asOf,
}: {
  children: ReactNode;
  cards?: KpiCard[] | null;
  asOf?: string | null;
}) {
  const pathname = usePathname();
  const [fallback, setFallback] = useState<{ cards: KpiCard[]; asOf: string } | null>(null);

  const needsFallback = cards === undefined || asOf === undefined;

  useEffect(() => {
    if (!needsFallback) return;
    let cancelled = false;
    ontologyApi
      .kpiCards()
      .then((res) => {
        if (!cancelled) setFallback({ cards: res.cards, asOf: res.as_of });
      })
      .catch(() => {
        // 셸은 화면을 막지 않는다 — 배지가 비고 본문은 자기 에러를 그린다.
      });
    return () => {
      cancelled = true;
    };
  }, [needsFallback]);

  const resolvedCards = cards ?? fallback?.cards ?? null;
  const resolvedAsOf = asOf ?? fallback?.asOf ?? null;
  const alertCount = resolvedCards
    ? resolvedCards.filter((card) => card.node_state === "알림").length
    : null;

  return (
    <div style={{ display: "flex", flexDirection: "column", minHeight: "100vh" }}>
      <header
        style={{
          height: 64,
          flexShrink: 0,
          display: "flex",
          alignItems: "center",
          padding: "0 64px",
          background: "var(--ont-surface)",
          borderBottom: "1px solid var(--ont-border-header)",
        }}
      >
        <Link href="/ontology/monitoring" style={{ display: "flex", alignItems: "center", gap: 8, marginRight: 40 }}>
          <span
            style={{
              width: 25,
              height: 25,
              borderRadius: 6,
              background: "var(--ont-grad-logo)",
              color: "#fff",
              fontSize: 13,
              fontWeight: 800,
              display: "flex",
              alignItems: "center",
              justifyContent: "center",
            }}
          >
            O
          </span>
          <span style={{ fontSize: 17, fontWeight: 800, letterSpacing: "-0.01em" }}>Ontology</span>
        </Link>

        <nav style={{ display: "flex", gap: 4 }}>
          {TABS.map((tab) => {
            const active = pathname?.startsWith(tab.href) ?? false;
            return (
              <Link
                key={tab.href}
                href={tab.href}
                style={{
                  height: 64,
                  padding: "0 16px",
                  display: "flex",
                  alignItems: "center",
                  gap: 7,
                  fontSize: 14,
                  fontWeight: active ? 700 : 400,
                  color: active ? "var(--ont-ink)" : "var(--ont-label)",
                  boxShadow: active ? "inset 0 -2px 0 var(--ont-ink)" : undefined,
                  transition: "color var(--ont-transition)",
                }}
              >
                {tab.label}
                {tab.badge && alertCount !== null && alertCount > 0 && (
                  <span
                    title="알림 상태 KPI 수"
                    style={{
                      width: 18,
                      height: 18,
                      borderRadius: "50%",
                      background: "var(--ont-alert)",
                      color: "#fff",
                      fontSize: 11,
                      fontWeight: 700,
                      display: "flex",
                      alignItems: "center",
                      justifyContent: "center",
                    }}
                  >
                    {alertCount}
                  </span>
                )}
              </Link>
            );
          })}
        </nav>

        <div style={{ marginLeft: "auto", display: "flex", alignItems: "center", gap: 12 }}>
          <AsOfBadge asOf={resolvedAsOf} />
          <span
            aria-hidden
            style={{
              width: 30,
              height: 30,
              borderRadius: "50%",
              background: "var(--ont-grad-avatar)",
            }}
          />
        </div>
      </header>

      <div style={{ flex: 1, minHeight: 0, display: "flex", flexDirection: "column" }}>{children}</div>
    </div>
  );
}

/**
 * 기준일 배지 — 「실시간 금지」의 UI 장치. 전 화면 우상단 고정, 생략하지 않는다.
 * 날짜는 `as_of` 파생이고 하드코딩하지 않는다(디자인 02 · 08 규칙 2·7).
 */
export function AsOfBadge({ asOf }: { asOf: string | null }) {
  return (
    <span
      style={{
        height: 26,
        display: "inline-flex",
        alignItems: "center",
        gap: 6,
        padding: "0 10px",
        borderRadius: 6,
        background: "var(--ont-hover)",
        border: "1px solid var(--ont-border-header)",
        fontSize: 12,
        color: "var(--ont-body)",
        whiteSpace: "nowrap",
      }}
    >
      <svg width="12" height="12" viewBox="0 0 16 16" fill="none" aria-hidden>
        <rect x="2" y="3" width="12" height="11" rx="2" stroke="var(--ont-muted)" strokeWidth="1.4" />
        <path d="M2 6.5h12M5.5 1.5v3M10.5 1.5v3" stroke="var(--ont-muted)" strokeWidth="1.4" />
      </svg>
      <span className="ont-mono">{asOf ?? "—"}</span>
      <span>기준</span>
    </span>
  );
}

/** 화면 본문 컨테이너 — 컨텐츠 패딩 `32px 64px 40px`, 최대 폭 1792(디자인 04·06). */
export function ScreenBody({ children, gap = 24 }: { children: ReactNode; gap?: number }) {
  return (
    <main
      style={{
        flex: 1,
        minHeight: 0,
        padding: "32px 64px 40px",
        maxWidth: 1792,
        width: "100%",
        margin: "0 auto",
        display: "flex",
        flexDirection: "column",
        gap,
      }}
    >
      {children}
    </main>
  );
}

export function ScreenTitle({
  title,
  meta,
  right,
}: {
  title: string;
  meta: string;
  right?: ReactNode;
}) {
  return (
    <div style={{ display: "flex", alignItems: "flex-end", gap: 16 }}>
      <div>
        <h1 style={{ margin: 0, fontSize: 28, fontWeight: 700, letterSpacing: "-0.03em" }}>{title}</h1>
        <p style={{ margin: "6px 0 0", fontSize: 13, color: "var(--ont-label)" }}>{meta}</p>
      </div>
      {right && <div style={{ marginLeft: "auto" }}>{right}</div>}
    </div>
  );
}
