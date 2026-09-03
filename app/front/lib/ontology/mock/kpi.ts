/**
 * mock — `/api/kpi/cards`.
 *
 * **이 파일은 데모 전용 픽스처다.** WORK-002 API 가 붙으면 통째로 우회되고
 * (`NEXT_PUBLIC_ONTOLOGY_API_BASE` 스위치), 화면 코드는 한 줄도 바뀌지 않는다.
 *
 * shape 는 SPEC-003 §4 그대로다. 값은 다음 근거를 따른다:
 * - 8월 집계: SPEC-005 §6 R-2 실측 — 매출 3.69억 · 내원 4,196 · 예약 6,852 ·
 *   결제 내원 641(+23%) · 객단가 58만 · 취소율 35.5%
 * - 주별 노쇼율: R-1 실측 — 5.3 / 4.8 / 5.2 / 5.0 %
 * - 임계값: SPEC-001 §4 — 노쇼율 주의 7.14% · 경고 8.7%, 매출 주의 5,946,390 ·
 *   경고 2,819,740
 * - 상태 구성(알림·관찰·미관측): 디자인 `data/nodes.json`
 *
 * 정본이 값을 주지 않는 자리(임계값 없는 지표 등)는 **null 로 비워 둔다** —
 * 지어낸 숫자를 넣지 않는다(디자인 08 규칙 8).
 */

import type { KpiCard, KpiCardsResponse } from "../types";

/** 데이터 마지막 날 — 2026-01-07 ~ 08-30(SPEC-001 §4). */
export const MOCK_AS_OF = "2026-08-30";
export const MOCK_LATEST_PERIOD = "2026-08";
export const MOCK_FIRST_PERIOD = "2026-01";

type CardSeed = Omit<KpiCard, "node_id"> & { node_id: string };

const CARDS: CardSeed[] = [
  // ── 알림 ───────────────────────────────────────────────────────────────
  {
    metric: "noshow_rate",
    node_id: "noshow_rate",
    label: "노쇼율",
    grain: "daily",
    latest: 0.053,
    unit: "%p",
    format: "percent",
    dod: 0.004,
    dod_pct: 0.082,
    spark: [0.041, 0.049, 0.075, 0.081, 0.052, 0.049, 0.053],
    status: "양호",
    alert_days: 3,
    node_state: "알림",
    thresholds: { 주의: 0.0714, 경고: 0.087 },
    direction: "높을수록 나쁨",
  },
  {
    metric: "gu_reviews",
    node_id: "gu_reviews",
    label: "강남언니 리뷰 수",
    grain: "weekly",
    latest: 1,
    unit: "건",
    format: "number",
    dod: -1,
    dod_pct: -0.5,
    spark: [11, 8, 6, 4, 3, 2, 1],
    status: "경고",
    alert_days: 5,
    node_state: "알림",
    thresholds: null,
    direction: "낮을수록 나쁨",
  },
  {
    metric: "new_churns",
    node_id: "new_churns",
    label: "신규 이탈 수",
    grain: "daily",
    latest: 7,
    unit: "명",
    format: "number",
    dod: 2,
    dod_pct: 0.4,
    spark: [4, 5, 8, 9, 6, 5, 7],
    status: "주의",
    alert_days: 4,
    node_state: "알림",
    thresholds: null,
    direction: "높을수록 나쁨",
  },

  // ── 관찰 ───────────────────────────────────────────────────────────────
  {
    metric: "cancel_rate",
    node_id: "cancel_rate",
    label: "취소율",
    grain: "daily",
    latest: 0.355,
    unit: "%p",
    format: "percent",
    dod: -0.008,
    dod_pct: -0.022,
    spark: [0.363, 0.371, 0.358, 0.349, 0.361, 0.363, 0.355],
    status: "주의",
    alert_days: 2,
    node_state: "관찰",
    thresholds: null,
    direction: "높을수록 나쁨",
  },
  {
    metric: "new_patients",
    node_id: "new_patients",
    label: "신환 수",
    grain: "daily",
    latest: 14,
    unit: "명",
    format: "number",
    dod: -3,
    dod_pct: -0.176,
    spark: [19, 17, 14, 16, 13, 17, 14],
    status: "주의",
    alert_days: 2,
    node_state: "관찰",
    thresholds: null,
    direction: "낮을수록 나쁨",
  },
  {
    metric: "retention_rate_60d",
    node_id: "retention_rate_60d",
    label: "재방문 전환율(60일)",
    grain: "retention_monthly",
    latest: 0.286,
    unit: "%p",
    format: "percent",
    dod: -0.021,
    dod_pct: -0.068,
    spark: [0.341, 0.336, 0.322, 0.318, 0.309, 0.307, 0.286],
    status: "주의",
    alert_days: 1,
    node_state: "관찰",
    thresholds: null,
    direction: "낮을수록 나쁨",
  },

  // ── 미관측 ─────────────────────────────────────────────────────────────
  {
    metric: "foreign_inflow_channel",
    node_id: "foreign_inflow_channel",
    label: "외국인 유입 채널",
    grain: "미관측",
    latest: null,
    unit: "",
    format: "number",
    dod: null,
    dod_pct: null,
    spark: null,
    status: null,
    alert_days: 0,
    node_state: "미관측",
    thresholds: null,
    direction: null,
  },

  // ── 정상 ───────────────────────────────────────────────────────────────
  {
    metric: "sales_total",
    node_id: "sales_total",
    label: "매출",
    grain: "daily",
    latest: 12_300_000,
    unit: "원",
    format: "currency",
    dod: 940_000,
    dod_pct: 0.083,
    spark: [10_900_000, 11_400_000, 12_800_000, 11_200_000, 13_100_000, 11_360_000, 12_300_000],
    status: "양호",
    alert_days: 0,
    node_state: "정상",
    thresholds: { 주의: 5_946_390, 경고: 2_819_740 },
    direction: "낮을수록 나쁨",
  },
  {
    metric: "payment_visits",
    node_id: "payment_visits",
    label: "결제 내원 수",
    grain: "daily",
    latest: 21,
    unit: "건",
    format: "number",
    dod: 2,
    dod_pct: 0.105,
    spark: [18, 20, 23, 19, 24, 19, 21],
    status: "양호",
    alert_days: 0,
    node_state: "정상",
    thresholds: null,
    direction: "낮을수록 나쁨",
  },
  {
    metric: "avg_ticket",
    node_id: "avg_ticket",
    label: "객단가",
    grain: "daily",
    latest: 580_000,
    unit: "원",
    format: "currency",
    dod: 12_000,
    dod_pct: 0.021,
    spark: [566_000, 571_000, 559_000, 588_000, 574_000, 568_000, 580_000],
    status: "양호",
    alert_days: 0,
    node_state: "정상",
    thresholds: null,
    direction: "낮을수록 나쁨",
  },
  {
    metric: "visits",
    node_id: "visits",
    label: "총 내원 수",
    grain: "daily",
    latest: 140,
    unit: "명",
    format: "number",
    dod: -6,
    dod_pct: -0.041,
    spark: [151, 148, 139, 144, 137, 146, 140],
    status: "양호",
    alert_days: 0,
    node_state: "정상",
    thresholds: null,
    direction: "낮을수록 나쁨",
  },
  {
    metric: "reservations",
    node_id: "reservations",
    label: "예약 수",
    grain: "daily",
    latest: 228,
    unit: "건",
    format: "number",
    dod: -9,
    dod_pct: -0.038,
    spark: [246, 241, 229, 235, 224, 237, 228],
    status: "양호",
    alert_days: 0,
    node_state: "정상",
    thresholds: null,
    direction: "낮을수록 나쁨",
  },
  {
    metric: "cancels",
    node_id: "cancels",
    label: "취소 수",
    grain: "daily",
    latest: 81,
    unit: "건",
    format: "number",
    dod: -4,
    dod_pct: -0.047,
    spark: [89, 89, 82, 82, 81, 86, 81],
    status: "양호",
    alert_days: 0,
    node_state: "정상",
    thresholds: null,
    direction: "높을수록 나쁨",
  },
  {
    metric: "noshows",
    node_id: "noshows",
    label: "부도 수",
    grain: "daily",
    latest: 8,
    unit: "건",
    format: "number",
    dod: 1,
    dod_pct: 0.143,
    spark: [6, 7, 11, 12, 7, 7, 8],
    status: "양호",
    alert_days: 0,
    node_state: "정상",
    thresholds: null,
    direction: "높을수록 나쁨",
  },
  {
    metric: "revisits",
    node_id: "revisits",
    label: "재진 수",
    grain: "daily",
    latest: 126,
    unit: "명",
    format: "number",
    dod: -3,
    dod_pct: -0.023,
    spark: [132, 131, 125, 128, 124, 129, 126],
    status: "양호",
    alert_days: 0,
    node_state: "정상",
    thresholds: null,
    direction: "낮을수록 나쁨",
  },
  {
    metric: "new_patients_domestic",
    node_id: "new_patients_domestic",
    label: "한국인 신환 수",
    grain: "daily",
    latest: 11,
    unit: "명",
    format: "number",
    dod: -2,
    dod_pct: -0.154,
    spark: [15, 13, 11, 12, 10, 13, 11],
    status: "양호",
    alert_days: 0,
    node_state: "정상",
    thresholds: null,
    direction: "낮을수록 나쁨",
  },
  {
    metric: "new_patients_foreign_est",
    node_id: "new_patients_foreign_est",
    label: "외국인 추정 신환 수",
    grain: "daily",
    latest: 3,
    unit: "명",
    format: "number",
    dod: -1,
    dod_pct: -0.25,
    spark: [4, 4, 3, 4, 3, 4, 3],
    status: "양호",
    alert_days: 0,
    node_state: "정상",
    thresholds: null,
    direction: "낮을수록 나쁨",
  },
  {
    metric: "sales_foreign_est",
    node_id: "sales_foreign_est",
    label: "외국인 추정 매출",
    grain: "daily",
    latest: 7_010_000,
    unit: "원",
    format: "currency",
    dod: 460_000,
    dod_pct: 0.07,
    spark: [6_210_000, 6_500_000, 7_290_000, 6_380_000, 7_460_000, 6_550_000, 7_010_000],
    status: "양호",
    alert_days: 0,
    node_state: "정상",
    thresholds: null,
    direction: "낮을수록 나쁨",
  },
  {
    metric: "foreign_sales_share",
    node_id: "foreign_sales_share",
    label: "외국인 매출 비중",
    grain: "daily",
    latest: 0.57,
    unit: "%p",
    format: "percent",
    dod: -0.004,
    dod_pct: -0.007,
    spark: [0.57, 0.57, 0.57, 0.569, 0.569, 0.577, 0.57],
    status: "양호",
    alert_days: 0,
    node_state: "정상",
    thresholds: null,
    direction: null,
  },

  // ── 상태 없음 — 개입 신호는 방향이 없어 status·node_state 를 갖지 않는다 ──
  {
    metric: "naver_reviews",
    node_id: "naver_reviews",
    label: "네이버 리뷰 수",
    grain: "daily",
    latest: 1,
    unit: "건",
    format: "number",
    dod: 0,
    dod_pct: 0,
    spark: [2, 1, 0, 1, 0, 1, 1],
    status: null,
    alert_days: 0,
    node_state: null,
    thresholds: null,
    direction: null,
  },
];

const PERIOD_INDEX: Record<string, number> = {
  "2026-01": 0,
  "2026-02": 1,
  "2026-03": 2,
  "2026-04": 3,
  "2026-05": 4,
  "2026-06": 5,
  "2026-07": 6,
  "2026-08": 7,
};

/** 기간 스테퍼가 실제로 움직이는 것을 보이기 위한 결정적 스케일(픽스처 한정). */
function periodFactor(period: string): number {
  const index = PERIOD_INDEX[period];
  if (index === undefined || index === 7) return 1;
  return 1 + (7 - index) * 0.035;
}

function scale(value: number | null, factor: number, format: KpiCard["format"]): number | null {
  if (value === null) return null;
  if (factor === 1) return value;
  const next = value * factor;
  if (format === "percent") return Number(next.toFixed(4));
  if (format === "currency") return Math.round(next / 1000) * 1000;
  return Math.round(next);
}

export function mockKpiCards(period?: string): KpiCardsResponse {
  const resolved = period && period in PERIOD_INDEX ? period : MOCK_LATEST_PERIOD;
  const factor = periodFactor(resolved);
  const asOf = resolved === MOCK_LATEST_PERIOD ? MOCK_AS_OF : `${resolved}-28`;

  return {
    as_of: asOf,
    period: resolved,
    window_days: 7,
    has_next_period: resolved !== MOCK_LATEST_PERIOD,
    cards: CARDS.map((card) => ({
      ...card,
      latest: scale(card.latest, factor, card.format),
      dod: scale(card.dod, factor, card.format),
      spark: card.spark ? card.spark.map((v) => scale(v, factor, card.format) as number) : null,
    })),
  };
}

/** `/api/graph` 픽스처가 노드 상태를 같은 표에서 파생시키기 위한 조회. */
export function mockNodeStates(): Map<string, { state: KpiCard["node_state"]; alertDays: number }> {
  return new Map(
    CARDS.map((card) => [card.node_id, { state: card.node_state, alertDays: card.alert_days }]),
  );
}
