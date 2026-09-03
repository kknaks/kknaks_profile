/**
 * 시각 인코딩과 표기 규칙.
 *
 * > **색 = 상태 · 모양 = 노드 타입 · 선 스타일 = 엣지 판정 · 굵기 = 채택 엣지의 신뢰도**
 * > (디자인 `03-graph-encoding.md` — 두 축을 색으로 겹치지 않는다)
 *
 * 판정(`verdict`)은 **번역이 없다** — API 값이 곧 화면 문구다(SPEC-004 U-5).
 * 노드 유형(`node_type`)은 영문 enum 이 정본이고 화면은 한글 카피를 쓴다 —
 * 영문 값을 화면에 그대로 노출하지 않는다(AC-11).
 */

import type { Confidence, KpiCard, Layer, NodeState, NodeType, Verdict } from "./types";

/* ─────────────────────────── 노드 유형 → 화면 카피 ─────────────────────────── */

export const NODE_TYPE_LABEL: Readonly<Record<NodeType, string>> = {
  kpi: "KPI",
  intervention: "개입",
  organic: "유기",
  exogenous: "외생",
  unobserved: "미관측",
  attribute: "속성",
};

export const NODE_TYPE_ORDER: NodeType[] = [
  "kpi",
  "intervention",
  "organic",
  "exogenous",
  "unobserved",
  "attribute",
];

/* ─────────────────────────── 엣지 판정 → 선 ─────────────────────────── */

export interface VerdictStroke {
  color: string;
  /** SVG `stroke-dasharray`. 실선이면 undefined. */
  dash?: string;
  opacity: number;
  /** 중앙에 × 표시(기각). */
  cross: boolean;
  arrow: boolean;
}

export const VERDICT_ORDER: Verdict[] = ["채택", "자동 확정", "선언", "보류", "기각"];

/** 인과 서술에 쓸 수 있는 판정 — `used_edges` 가 이 집합의 부분집합이다(SPEC-005). */
export const CONFIRMED_VERDICTS: Verdict[] = ["채택", "자동 확정", "선언"];

export function verdictStroke(verdict: Verdict): VerdictStroke {
  switch (verdict) {
    case "채택":
      return { color: "#1E1E1E", opacity: 1, cross: false, arrow: true };
    case "자동 확정":
      return { color: "#7181F8", opacity: 1, cross: false, arrow: true };
    case "선언":
      return { color: "#5F6470", dash: "7 3", opacity: 1, cross: false, arrow: true };
    case "보류":
      return { color: "#E3B93C", dash: "2.5 3", opacity: 1, cross: false, arrow: true };
    case "기각":
      return { color: "#E2685B", dash: "2.5 3", opacity: 0.5, cross: true, arrow: false };
  }
}

/**
 * 굵기 — **신뢰도가 있을 때만 신뢰도다.** `confidence` 는 `채택` 에만 존재한다.
 * 신뢰도가 없는 판정에서 굵기는 신뢰도를 말하지 않는다(디자인 03).
 */
export function verdictWidth(verdict: Verdict, confidence: Confidence | null): number {
  if (verdict === "채택") {
    if (confidence === "높음") return 2.6;
    if (confidence === "중간") return 1.6;
    return 1;
  }
  if (verdict === "자동 확정") return 1.6;
  if (verdict === "기각") return 1.2;
  return 1.4; // 선언 · 보류
}

/** 방향 배지는 `+`/`−` 일 때만. `0`·`exo`·`?`·빈 값은 방향이 없다(디자인 03). */
export function hasDirection(sign: string): boolean {
  return sign === "+" || sign === "−" || sign === "-";
}

export function directionGlyph(sign: string): string {
  return sign === "-" ? "−" : sign;
}

/* ─────────────────────────── 상태 → 색 ─────────────────────────── */

export interface StatusTone {
  dot: string;
  fill: string;
  text: string;
  border: string;
  softFill: string;
  spark: string;
  label: string;
}

const TONE_ALERT: StatusTone = {
  dot: "var(--ont-alert)",
  fill: "var(--ont-alert-fill)",
  text: "var(--ont-alert-text)",
  border: "var(--ont-alert-border)",
  softFill: "var(--ont-alert-soft)",
  spark: "var(--ont-spark-alert)",
  label: "알림",
};

const TONE_WATCH: StatusTone = {
  dot: "var(--ont-watch)",
  fill: "var(--ont-watch-fill)",
  text: "var(--ont-watch-text)",
  border: "var(--ont-watch-border)",
  softFill: "var(--ont-watch-soft)",
  spark: "var(--ont-spark-watch)",
  label: "관찰",
};

const TONE_NORMAL: StatusTone = {
  dot: "var(--ont-normal)",
  fill: "var(--ont-normal-fill)",
  text: "var(--ont-normal-text)",
  border: "var(--ont-border)",
  softFill: "var(--ont-surface)",
  spark: "var(--ont-spark-normal)",
  label: "정상",
};

const TONE_UNOBSERVED: StatusTone = {
  dot: "var(--ont-unobserved)",
  fill: "var(--ont-unobserved-fill)",
  text: "var(--ont-unobserved-text)",
  border: "var(--ont-border-card)",
  softFill: "var(--ont-surface)",
  spark: "var(--ont-spark-normal)",
  label: "미관측",
};

export function stateTone(state: NodeState | null): StatusTone {
  switch (state) {
    case "알림":
      return TONE_ALERT;
    case "관찰":
      return TONE_WATCH;
    case "미관측":
      return TONE_UNOBSERVED;
    default:
      return TONE_NORMAL;
  }
}

/**
 * 카드 정렬 우선순위 — **알림 → 관찰 → 미관측 → 정상**(U-4).
 * 상태가 없는 카드(개입 신호처럼 방향 없는 변수)는 정상과 같은 자리에 둔다.
 */
export function stateRank(state: NodeState | null): number {
  switch (state) {
    case "알림":
      return 0;
    case "관찰":
      return 1;
    case "미관측":
      return 2;
    default:
      return 3;
  }
}

export function sortCardsBySeverity(cards: KpiCard[]): KpiCard[] {
  return [...cards].sort((a, b) => stateRank(a.node_state) - stateRank(b.node_state));
}

/* ─────────────────────────── 계층 배지 ─────────────────────────── */

export const LAYER_LABEL: Readonly<Record<Layer, string>> = {
  bronze: "브론즈",
  silver: "실버",
  gold: "골드",
};

/** 각 계층의 근거 기록 — 브론즈 02 · 실버 04 · 골드 05 · 그래프 07(SPEC-004 U-15). */
export const LAYER_NOTE_REF: Readonly<Record<Layer, string>> = {
  bronze: "기록 02",
  silver: "기록 04",
  gold: "기록 05",
};

export function layerTone(layer: Layer): { fill: string; border: string; text: string; dot: string } {
  return {
    fill: `var(--ont-${layer}-fill)`,
    border: `var(--ont-${layer}-border)`,
    text: `var(--ont-${layer}-text)`,
    dot: `var(--ont-${layer}-dot)`,
  };
}

/* ─────────────────────────── 테이블 참조 파싱 ─────────────────────────── */

export interface TableRef {
  layer: Layer;
  table: string;
  column: string | null;
}

/**
 * `gold_kpi_daily.sales_total` · `silver_reservations.visit_status` ·
 * `v_bronze_vegas_reservations` 같은 참조를 계층·테이블로 가른다.
 *
 * 인스펙터의 「원본 데이터 보기」와 컬럼 상세의 역추적이 이 함수 하나를 쓴다 —
 * **매핑 표를 화면에 손으로 두지 않는다**(SPEC-004 U-6·U-15).
 */
export function parseTableRef(ref: string | null | undefined): TableRef | null {
  if (!ref) return null;
  const dot = ref.indexOf(".");
  const name = dot === -1 ? ref : ref.slice(0, dot);
  const column = dot === -1 ? null : ref.slice(dot + 1);

  const strip = (prefix: string) => name.slice(prefix.length);

  if (name.startsWith("v_bronze_")) return { layer: "bronze", table: strip("v_bronze_"), column };
  if (name.startsWith("v_silver_")) return { layer: "silver", table: strip("v_silver_"), column };
  if (name.startsWith("bronze_")) return { layer: "bronze", table: strip("bronze_"), column };
  if (name.startsWith("silver_")) return { layer: "silver", table: strip("silver_"), column };
  // 골드 테이블은 이름에 접두를 포함한 것이 정본이다(`gold_kpi_daily`).
  if (name.startsWith("gold_")) return { layer: "gold", table: name, column };
  return null;
}

/** 데이터 화면으로 가는 링크 — 테이블은 **이름**으로 싣는다(인덱스 아님). */
export function dataHref(ref: TableRef, filters?: string | null): string {
  const params = new URLSearchParams({ tier: ref.layer, table: ref.table });
  if (filters) params.set("filters", filters);
  return `/ontology/data?${params.toString()}`;
}

/* ─────────────────────────── 값 표기 ─────────────────────────── */

const NUMBER_FORMAT = new Intl.NumberFormat("ko-KR");

export function formatCount(value: number): string {
  return NUMBER_FORMAT.format(value);
}

/**
 * 카드 값 표기 — `format`·`unit` 은 응답값이다. 화면이 문자열을 만들지 않고
 * 이 값으로 조립한다(SPEC-003 §4 KPI).
 */
export function formatMetricValue(
  value: number | null,
  format: KpiCard["format"],
): string {
  if (value === null || value === undefined) return "—";
  switch (format) {
    case "percent":
      return `${(value * 100).toFixed(1)}%`;
    case "currency":
      return formatKrwCompact(value);
    default:
      return NUMBER_FORMAT.format(Number(value.toFixed(Math.abs(value) < 10 ? 1 : 0)));
  }
}

/** 금액은 28px 한 줄에 들어가야 해서 억·만 단위로 접는다. 원값은 툴팁·인용이 갖는다. */
export function formatKrwCompact(value: number): string {
  const abs = Math.abs(value);
  const sign = value < 0 ? "−" : "";
  if (abs >= 100_000_000) return `${sign}${(abs / 100_000_000).toFixed(2)}억`;
  if (abs >= 10_000) return `${sign}${NUMBER_FORMAT.format(Math.round(abs / 10_000))}만`;
  return `${sign}${NUMBER_FORMAT.format(Math.round(abs))}`;
}

export function formatDelta(
  dod: number | null,
  dodPct: number | null,
  format: KpiCard["format"],
): string | null {
  if (dod === null || dod === undefined) return null;
  const sign = dod > 0 ? "+" : dod < 0 ? "−" : "±";
  const magnitude =
    format === "percent"
      ? `${Math.abs(dod * 100).toFixed(1)}%p`
      : format === "currency"
        ? formatKrwCompact(Math.abs(dod))
        : NUMBER_FORMAT.format(Math.abs(Number(dod.toFixed(Math.abs(dod) < 10 ? 1 : 0))));
  if (dodPct === null || dodPct === undefined) return `${sign}${magnitude}`;
  return `${sign}${magnitude} (${sign}${Math.abs(dodPct * 100).toFixed(1)}%)`;
}

/**
 * 전 기간 대비 캡션 — **카드가 실은 `grain` 으로 만든다.** 「(주간)」을 하드코딩하지
 * 않는다(SPEC-004 U-4 · 디자인 02).
 */
export function grainCaption(grain: string): string {
  switch (grain) {
    case "daily":
      return "전일 대비";
    case "weekly":
      return "전주 대비 (주간)";
    case "monthly":
      return "전월 대비 (월간)";
    case "retention_monthly":
      return "전월 코호트 대비 (월간)";
    default:
      return `전 기간 대비 (${grain})`;
  }
}

/** 기간 스테퍼 — `YYYY-MM` 을 「2026년 8월」로. */
export function formatPeriod(period: string): string {
  const [year, month] = period.split("-");
  if (!year || !month) return period;
  return `${year}년 ${Number(month)}월`;
}

export function shiftPeriod(period: string, delta: number): string {
  const [yearStr, monthStr] = period.split("-");
  const year = Number(yearStr);
  const month = Number(monthStr);
  if (!year || !month) return period;
  const total = year * 12 + (month - 1) + delta;
  const nextYear = Math.floor(total / 12);
  const nextMonth = (total % 12) + 1;
  return `${nextYear}-${String(nextMonth).padStart(2, "0")}`;
}

/** 표 헤더 `1–N / total` — 응답의 `offset`·`returned`·`total` 파생. */
export function rangeLabel(offset: number, returned: number, total: number): string {
  if (total === 0 || returned === 0) return `0 / ${formatCount(total)}`;
  return `${formatCount(offset + 1)}–${formatCount(offset + returned)} / ${formatCount(total)}`;
}
