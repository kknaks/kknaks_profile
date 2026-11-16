/**
 * mock — `/api/layers/{layer}/{table}/lineage`.
 *
 * 컬럼 상세가 요구하는 필드는 SPEC-003 §4 다: `rule_id` · `gate` · `downstream` ·
 * `source_columns` · `is_provisional` · `note_ref`.
 * 계산식·글로서리 규칙 ID·게이트 문구는 디자인 `data/tables.json` 과 SPEC-001 §4 에서
 * 왔다. **`source_columns` 가 골드 → 실버 → 브론즈 역추적의 사다리**다(SPEC-004 U-15).
 */

import type { ApiLayer, LineageColumn, LineageResponse } from "../types";

type LineageSeed = Omit<
  LineageColumn,
  "rule_id" | "is_provisional" | "note_ref" | "downstream" | "source_columns"
> &
  Partial<Pick<LineageColumn, "rule_id" | "is_provisional" | "downstream" | "source_columns">>;

function column(base: LineageSeed & { column: string; note_ref: string }): LineageColumn {
  return {
    rule_id: null,
    is_provisional: false,
    downstream: [],
    source_columns: [],
    ...base,
  };
}

const BRONZE_REF = "기록 02 브론즈 실사";
const SILVER_REF = "기록 04 실버 빌드";
const GOLD_REF = "기록 05 골드 KPI";

const LINEAGE: Record<string, LineageColumn[]> = {
  "bronze:vegas_reservations": [
    column({
      column: "visitStatus",
      note: "원천 6값(예약확정 · 내원 · 당일취소 · 사전취소 · 미방문 · 보류)을 원형 그대로 적재한다.",
      note_ref: BRONZE_REF,
      downstream: [{ layer: "silver", table: "reservations", column: "visit_status" }],
    }),
    column({
      column: "sales",
      note: "결제 금액 원 단위 정수. 음수는 빌드 중단 대상이다.",
      note_ref: BRONZE_REF,
      downstream: [{ layer: "silver", table: "reservations", column: "sales" }],
    }),
    column({
      column: "chartNo",
      note: "차트번호는 해시하지 않고 그대로 반입한다 — 계층 추적용(기록 03 확정). 빈 값은 「환자 미식별」 그룹이다.",
      note_ref: BRONZE_REF,
      downstream: [{ layer: "silver", table: "reservations", column: "chart_no" }],
    }),
    column({
      column: "patientName",
      note: "마스킹 뷰가 성 1자만 남긴다(`김○○`). 원값을 여는 경로가 없다.",
      gate: "게이트 3(마스킹) — 뷰 산출에 원값 검색 0건",
      note_ref: BRONZE_REF,
      downstream: [],
    }),
    column({
      column: "birthday",
      note: "마스킹 뷰가 연도만 남긴다(`1990-**-**`). 실버에는 `age_band` 로만 내려간다.",
      gate: "게이트 3(마스킹) — 뷰 산출에 원값 검색 0건",
      note_ref: BRONZE_REF,
      downstream: [{ layer: "silver", table: "reservations", column: "age_band" }],
    }),
  ],
  "bronze:reviews": [
    column({
      column: "body",
      note: "본문 내 직원 실명을 실명 토큰 사전으로 가린다. 원문은 마스킹본으로만 보관한다.",
      gate: "게이트 3(마스킹) — 실명 토큰 검색 0건",
      note_ref: BRONZE_REF,
      downstream: [{ layer: "silver", table: "reviews", column: "body_masked" }],
    }),
    column({
      column: "rating",
      note: "별점 원값. 감성은 별점만으로 판정하지 않는다(G-022).",
      note_ref: BRONZE_REF,
      downstream: [{ layer: "silver", table: "reviews", column: "sentiment" }],
    }),
  ],

  "silver:reservations": [
    column({
      column: "visit_status",
      note: "브론즈 6값을 내원 · 취소 · 부도 3값으로 축약한다. 「노쇼」가 아니라 「부도」다 — 지표명(노쇼율)과 원인값은 다른 층이다.",
      rule_id: "G-014",
      note_ref: SILVER_REF,
      source_columns: ["bronze_vegas_reservations.visitStatus"],
      downstream: [
        { layer: "gold", table: "gold_kpi_daily", column: "cancel_rate" },
        { layer: "gold", table: "gold_kpi_daily", column: "noshow_rate" },
        { layer: "gold", table: "gold_kpi_daily", column: "visits" },
      ],
    }),
    column({
      column: "age_band",
      note: "생년월일을 10세 단위 밴드로만 내린다. 결측은 「미상」이고 0 으로 채우지 않는다.",
      rule_id: "G-014",
      note_ref: SILVER_REF,
      source_columns: ["bronze_vegas_reservations.birthday"],
      downstream: [],
    }),
    column({
      column: "sales",
      note: "원 단위 정수 그대로. 음수 1건이라도 있으면 빌드 중단이다.",
      note_ref: SILVER_REF,
      source_columns: ["bronze_vegas_reservations.sales"],
      downstream: [{ layer: "gold", table: "gold_kpi_daily", column: "sales_total" }],
    }),
    column({
      column: "chart_no",
      note: "브론즈 차트번호를 그대로 유지한다 — 계층 역추적의 조인 키다.",
      note_ref: SILVER_REF,
      source_columns: ["bronze_vegas_reservations.chartNo"],
      downstream: [{ layer: "gold", table: "gold_retention_monthly", column: "cohort_size" }],
    }),
    column({
      column: "is_new",
      note: "신환 · 재진 판정. 총 내원 = 신환 + 재진 항등식의 입력이다.",
      note_ref: SILVER_REF,
      source_columns: ["bronze_vegas_reservations.chartNo"],
      downstream: [
        { layer: "gold", table: "gold_kpi_daily", column: "new_patients" },
        { layer: "gold", table: "gold_kpi_daily", column: "revisits" },
      ],
    }),
  ],
  "silver:reviews": [
    column({
      column: "sentiment",
      note: "긍정 · 중립 · 부정 · 판정불가 4값. 중립과 판정불가를 합치지 않는다.",
      rule_id: "G-022",
      note_ref: SILVER_REF,
      source_columns: ["bronze_reviews.body", "bronze_reviews.rating"],
      downstream: [{ layer: "gold", table: "gold_kpi_weekly", column: "gu_negative" }],
    }),
    column({
      column: "signal_type",
      note: "유기(강남언니) · 개입(네이버). 한 컬럼으로 합산하지 않는다 — 서로 다른 축이다.",
      rule_id: "G-021",
      note_ref: SILVER_REF,
      source_columns: ["bronze_reviews.platform"],
      downstream: [
        { layer: "gold", table: "gold_kpi_weekly", column: "gu_reviews" },
        { layer: "gold", table: "gold_kpi_daily", column: "naver_reviews" },
      ],
    }),
  ],
  "silver:catalog": [
    column({
      column: "unit_price",
      note: "패키지는 회당 단가로 환산해 객단가 계산에 투입한다.",
      rule_id: "G-008",
      note_ref: SILVER_REF,
      source_columns: ["bronze_nexus_procedure_products_ko.listPrice"],
      downstream: [{ layer: "gold", table: "gold_kpi_daily", column: "avg_ticket" }],
    }),
  ],
  "silver:promotions": [
    column({
      column: "discount_rate",
      note: "중첩 프로모션은 기간 가중 평균으로 접는다.",
      rule_id: "G-031",
      note_ref: SILVER_REF,
      source_columns: ["bronze_nexus_promotion_v2s.discountRate"],
      downstream: [{ layer: "gold", table: "gold_promo_calendar", column: "avg_discount" }],
    }),
  ],
  "silver:mappings": [
    column({
      column: "confidence",
      note: "낮음은 골드 집계에서 제외하고 「기타」로 남긴다 — 조용히 버리지 않는다.",
      rule_id: "G-040",
      note_ref: SILVER_REF,
      source_columns: ["bronze_nexus_procedure_group_product_mappings.groupId"],
      downstream: [{ layer: "gold", table: "gold_kpi_daily", column: "avg_ticket" }],
    }),
  ],
  "silver:branch_alias": [
    column({
      column: "canonical",
      note: "표기 변형을 대표 지점명(CERAMIQUE-GN-001)으로 통일한다. 인스턴스는 강남 단일이다.",
      rule_id: "G-050",
      note_ref: SILVER_REF,
      source_columns: ["bronze_nexus_branches.name"],
      downstream: [],
    }),
  ],

  "gold:gold_kpi_daily": [
    column({
      column: "noshow_rate",
      formula: "부도 ÷ (내원 + 부도)",
      note: "취소는 분모에서 제외한다 — 취소는 「안 온 것」이 아니라 「예약을 무른 것」이다.",
      gate: "기록 05 게이트 3(내원 대사) 통과 · 분모 0인 날은 null 처리 후 ma7 에서 제외",
      note_ref: `${GOLD_REF} 2.2 · 기록 03 1장 노쇼율`,
      source_columns: ["silver_reservations.visit_status"],
      downstream: [{ layer: "gold", table: "gold_kpi_weekly", column: "noshow_rate" }],
      status_thresholds: { direction: "높을수록 나쁨", 주의: 0.0714, 경고: 0.087 },
    }),
    column({
      column: "cancel_rate",
      formula: "취소 ÷ 예약",
      note: "재진 취소가 주 원천이다(33.5%).",
      gate: "게이트 G3 통과 · 분모 0일은 null 처리 후 ma7 에서 제외",
      note_ref: GOLD_REF,
      source_columns: ["silver_reservations.visit_status"],
      downstream: [{ layer: "gold", table: "gold_kpi_weekly", column: "cancel_rate" }],
    }),
    column({
      column: "sales_total",
      formula: "객단가 × 결제 내원",
      note: "항등식이라 자동 확정 엣지로 그래프에 실린다.",
      gate: "게이트 G2(빌드 재현) 통과 · 대조값 2,615,555,218원",
      note_ref: GOLD_REF,
      source_columns: ["silver_reservations.sales"],
      downstream: [
        { layer: "gold", table: "gold_kpi_weekly", column: "sales_total" },
        { layer: "gold", table: "gold_kpi_monthly", column: "sales_total" },
      ],
      status_thresholds: { direction: "낮을수록 나쁨", 주의: 5946390, 경고: 2819740 },
    }),
    column({
      column: "visits",
      formula: "신환 + 재진",
      note: "전 일자에서 신환 + 재진 = 총 내원이 성립해야 한다(게이트 AC-3).",
      gate: "게이트 3(내원 대사) 통과 · 235일 오차 0",
      note_ref: GOLD_REF,
      source_columns: ["silver_reservations.is_new"],
      downstream: [{ layer: "gold", table: "gold_kpi_weekly", column: "visits" }],
    }),
    column({
      column: "reservations",
      formula: "내원 + 취소 + 부도",
      note: "예약은 세 상태의 합이다.",
      gate: "게이트 G3 통과",
      note_ref: GOLD_REF,
      source_columns: ["silver_reservations.visit_status"],
      downstream: [],
    }),
    column({
      column: "avg_ticket",
      formula: "매출 ÷ 결제 내원",
      note: "시술 구성에 좌우된다 — 신환 수와는 직접 엮이지 않는다(기각 엣지).",
      gate: "게이트 G3 통과",
      note_ref: GOLD_REF,
      source_columns: ["silver_catalog.unit_price", "silver_reservations.sales"],
      downstream: [],
    }),
    column({
      column: "payment_visits",
      formula: "결제 금액 > 0 인 내원 건수",
      note: "매출로 가는 확정 경로의 시작점이다.",
      gate: "게이트 G2 통과 · 대조값 5,428건",
      note_ref: GOLD_REF,
      source_columns: ["silver_reservations.sales"],
      downstream: [],
    }),
    column({
      column: "foreign_sales_share",
      formula: "외국인 추정 매출 ÷ 매출",
      note: "비중은 답할 수 있지만 유입 채널은 관측되지 않는다 — 그래프의 물음표가 여기서 온다.",
      gate: "게이트 G3 통과",
      note_ref: GOLD_REF,
      source_columns: ["silver_reservations.sales"],
      downstream: [],
    }),
    column({
      column: "naver_reviews",
      note: "방향 없는 개입 변수라 상태 컬럼을 부여하지 않는다. 관측 개시(2026-03-21) 이전 구간은 0 이 아니라 빈 값이다.",
      gate: "상태 컬럼 미부여 · 관측 개시 이전은 null",
      note_ref: GOLD_REF,
      source_columns: ["silver_reviews.signal_type"],
      downstream: [{ layer: "gold", table: "gold_kpi_weekly", column: "naver_reviews" }],
    }),
  ],
  "gold:gold_kpi_weekly": [
    column({
      column: "noshow_rate",
      formula: "주 합계 부도 ÷ (주 합계 내원 + 주 합계 부도)",
      note: "비율형은 일별 평균이 아니라 주 합계에서 재계산한다.",
      gate: "게이트 G3 통과 · 부분 주는 플래그를 단다",
      note_ref: GOLD_REF,
      source_columns: ["gold_kpi_daily.noshow_rate"],
      downstream: [],
      status_thresholds: { direction: "높을수록 나쁨", 주의: 0.0714, 경고: 0.087 },
    }),
    column({
      column: "gu_negative",
      formula: "주 단위 부정 리뷰 수",
      note: "리뷰 0건 주는 null 이다 — 0 과 구분한다.",
      gate: "게이트 G3 통과 · 주 단위 카운트",
      note_ref: GOLD_REF,
      source_columns: ["silver_reviews.sentiment"],
      downstream: [],
    }),
  ],
  "gold:gold_kpi_monthly": [
    column({
      column: "sales_total",
      formula: "월 합계 매출 (일별에서 집계)",
      note: "월 집계는 골드 View 가 소유한다 — 도구·API 가 실행 시점에 합산하지 않는다.",
      gate: "게이트 G2 통과 · 비율형은 월 합계에서 재계산",
      note_ref: GOLD_REF,
      source_columns: ["gold_kpi_daily.sales_total"],
      downstream: [],
    }),
  ],
  "gold:gold_retention_monthly": [
    column({
      column: "revisit_rate",
      formula: "revisit_60d ÷ cohort_size",
      note: "60일이 지나지 않은 코호트는 미확정이다 — 0 으로 채우지 않고 집계에서 뺀다.",
      gate: "게이트 G4 통과 · 60일 미경과 코호트는 is_provisional",
      note_ref: GOLD_REF,
      source_columns: ["silver_reservations.chart_no"],
      downstream: [],
      is_provisional: true,
    }),
  ],
};

export function mockLineage(layer: ApiLayer, table: string): LineageResponse {
  return { table, columns: LINEAGE[`${layer}:${table}`] ?? [] };
}
