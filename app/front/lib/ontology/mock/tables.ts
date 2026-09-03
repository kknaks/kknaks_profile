/**
 * mock — 계층 테이블 목록·행·컬럼 상세(`/api/layers/*`).
 *
 * 행수·계층 구성·글로서리 규칙 ID 의 SoT 는 SPEC-001 §4 와 디자인 `data/tables.json`
 * 이다. 행 값 자체는 픽스처이고, **PII 는 마스킹 표기로만** 만든다 —
 * 이름 `김○○` · 전화 `010-****-1234` · 생년월일 `1990-**-**`(SPEC-001 §4).
 *
 * **정본에 컬럼 목록이 없는 테이블은 비워 두고 그 사실을 실어 보낸다**
 * (nexus 14테이블 · `gold_promo_calendar` — 디자인 08 규칙 8). 지어내지 않는다.
 */

import type { ApiLayer, Layer, LayerTable, LayerRowsResponse, RowValue, SourceGroup } from "../types";
import { mockOntologyEdgeRows, mockOntologyNodeRows } from "./graph";

/* ─────────────────────────── 컬럼 스펙 ─────────────────────────── */

type ColumnKind =
  | "date"
  /** 브론즈 원형의 `YYYYMMDD` 문자열 — 실버에서 표준화된다. */
  | "compact_date"
  | "timestamp"
  | "review_pk"
  | "score"
  /** 원천이 이미 마스킹한 닉네임(`tls****`) — 우리가 다시 가리지 않는다. */
  | "masked_handle"
  | "week"
  | "month"
  | "int"
  | "money"
  | "rate"
  | "enum"
  | "text"
  | "code"
  | "flag"
  | "masked_name"
  | "masked_phone"
  | "masked_birth";

interface ColumnSpec {
  key: string;
  kind: ColumnKind;
  values?: string[];
  /** 정수 범위 [min, max]. */
  range?: [number, number];
}

interface TableSpec {
  layer: ApiLayer;
  table: string;
  view: string;
  row_count: number;
  masked_fields: string[];
  columns: ColumnSpec[];
  note_ref: string;
  flows_to: { layer: Layer; table: string; note?: string }[];
  source_group?: SourceGroup;
  columns_note?: string;
  /** 컬럼 스펙으로 생성하지 않고 **정본 그대로** 싣는 행(온톨로지 계층). */
  fixedRows?: Record<string, RowValue>[];
}

const SURNAMES = ["김", "이", "박", "최", "정", "강", "조", "윤", "장", "임", "한", "오", "신", "권", "서"];
const CONCEPTS = ["제모", "리프팅", "스킨케어", "주사", "색소", "여드름", "체형"];
const PLATFORMS = ["네이버 플레이스", "강남언니"];

/** 「이 행들이 어디를 지나 나왔는가」 — 전 표면 공통(SPEC-001 뷰 경유 강제). */
const SOURCE_NOTE = "마스킹 뷰 경유 — 원 테이블 직접 조회 경로 없음";

const NEXUS_COLUMNS_NOTE =
  "nexus 원천 스키마를 원형 그대로 반입한 테이블이라 컬럼별 변환 규칙이 없다 — 글로서리(기록 03)가 판정한 용어가 아니라 외부 시스템의 컬럼이다";

const PROMO_COLUMNS_NOTE =
  "프로모션 이벤트 속성은 실버 스키마를 그대로 옮긴 것이라 KPI 계산식이 없다 — 구성 특성 4컬럼만 매핑 사슬에서 파생된다(기록 05 4장 개정 1)";

/* ─────────────────────────── 브론즈 16 ─────────────────────────── */

const NEXUS_CHILDREN: { table: string; rows: number }[] = [
  { table: "nexus_branches", rows: 3 },
  { table: "nexus_categories", rows: 157 },
  { table: "nexus_category_translations_ko", rows: 128 },
  { table: "nexus_procedure_groups", rows: 2154 },
  { table: "nexus_procedure_products_ko", rows: 2996 },
  { table: "nexus_procedure_group_product_mappings", rows: 5632 },
  { table: "nexus_event_procedure_groups", rows: 1769 },
  { table: "nexus_event_procedure_products_ko", rows: 2179 },
  { table: "nexus_event_procedure_group_product_mappings", rows: 3199 },
  { table: "nexus_procedure_packages_ko", rows: 323 },
  { table: "nexus_promotions_v1", rows: 24 },
  { table: "nexus_promotion_v2s", rows: 287 },
  { table: "nexus_promotion_v2_event_group_mappings", rows: 858 },
  { table: "nexus_promotion_v2_group_mappings", rows: 0 },
];

/** nexus 원천 스키마 표본 — 이름은 실 API 덤프 그대로다(값은 픽스처). */
const NEXUS_BRANCHES_COLUMNS: ColumnSpec[] = [
  { key: "id", kind: "code" },
  { key: "branch_id", kind: "enum", values: ["CERAMIQUE-GN-001"] },
  { key: "slug", kind: "enum", values: ["gangnam", "sinsa", "hongdae"] },
  { key: "subdomain", kind: "enum", values: ["gangnam", "sinsa", "hongdae"] },
  { key: "domain", kind: "text", values: ["gangnam.example-clinic.com"] },
  { key: "name", kind: "enum", values: ["강남점", "신사점", "홍대점"] },
  { key: "status", kind: "enum", values: ["ACTIVE", "INACTIVE"] },
  { key: "group_id", kind: "code" },
  { key: "created_at", kind: "timestamp" },
  { key: "updated_at", kind: "timestamp" },
];

const BRONZE: TableSpec[] = [
  {
    layer: "bronze",
    table: "vegas_reservations",
    view: "v_bronze_vegas_reservations",
    row_count: 78216,
    masked_fields: ["patientName", "phone", "birthday"],
    source_group: "vegas",
    note_ref: "기록 02 브론즈 실사",
    // 컬럼 이름·순서는 실 API(`v_bronze_vegas_reservations`) 그대로다. 브론즈는 원형이라
    // 날짜도 `YYYYMMDD` 문자열이고 실버에서 `resv_date` 로 표준화된다.
    columns: [
      { key: "branch", kind: "enum", values: ["세라미크의원 강남"] },
      { key: "resvDate", kind: "compact_date" },
      { key: "chartNo", kind: "code" },
      { key: "patientName", kind: "masked_name" },
      { key: "birthday", kind: "masked_birth" },
      { key: "phone", kind: "masked_phone" },
      { key: "staff", kind: "enum", values: ["미지정"] },
      { key: "sales", kind: "money" },
      { key: "receipt", kind: "money" },
      { key: "visitCount", kind: "int", range: [1, 12] },
      { key: "visitStatus", kind: "enum", values: ["내원", "취소", "부도"] },
    ],
    flows_to: [
      { layer: "silver", table: "reservations", note: "표준화 — 글로서리 G-014" },
      { layer: "gold", table: "gold_kpi_daily", note: "일별 KPI 의 주 원천" },
      { layer: "gold", table: "gold_retention_monthly", note: "코호트 60일" },
    ],
  },
  {
    layer: "bronze",
    table: "reviews",
    view: "v_bronze_reviews",
    row_count: 1962,
    masked_fields: ["authorName", "body"],
    source_group: "review",
    note_ref: "기록 02 브론즈 실사",
    // `authorName` 은 원천이 이미 마스킹 닉네임이라 그 표기를 유지한다(SPEC-001 §4).
    // 본문의 직원 실명은 `[직원]` 토큰으로 가려진 채로 온다.
    columns: [
      { key: "platform", kind: "enum", values: PLATFORMS },
      { key: "reviewDate", kind: "date" },
      { key: "authorName", kind: "masked_handle" },
      { key: "rating", kind: "int", range: [1, 5] },
      {
        key: "body",
        kind: "text",
        values: [
          "상담이 꼼꼼했어요",
          "대기 시간이 길었습니다",
          "시술 후 관리 안내가 좋았어요",
          "가격 대비 만족합니다",
          "[직원]실장님 통해 진행했어요. 잘 설명해주시니 감사합니다",
        ],
      },
      { key: "reviewPk", kind: "review_pk" },
      { key: "replyStatus", kind: "enum", values: ["replied", "none"] },
      { key: "collectedAt", kind: "timestamp" },
    ],
    flows_to: [
      { layer: "silver", table: "reviews", note: "감성·신호 유형 부여 — G-021·G-022" },
      { layer: "gold", table: "gold_kpi_daily", note: "naver_reviews" },
      { layer: "gold", table: "gold_kpi_weekly", note: "유기 신호 주별 집계" },
    ],
  },
  ...NEXUS_CHILDREN.map<TableSpec>((child) => ({
    layer: "bronze" as const,
    table: child.table,
    view: `bronze_${child.table}`,
    row_count: child.rows,
    masked_fields: [],
    source_group: "nexus",
    note_ref: "기록 02 브론즈 실사",
    // 표본이 있는 것은 `nexus_branches` 하나뿐이다(WORK-005 실 API 덤프). 나머지 13종은
    // 원천 스키마를 모르므로 **비워 두고** 그 사실을 `columns_note` 가 말한다 —
    // 지어내지 않는다(디자인 08 규칙 8).
    columns: child.table === "nexus_branches" ? NEXUS_BRANCHES_COLUMNS : [],
    columns_note: NEXUS_COLUMNS_NOTE,
    flows_to: [
      { layer: "silver" as const, table: "catalog", note: "시술 개념 매핑" },
      { layer: "silver" as const, table: "mappings", note: "코드 ↔ 개념" },
      { layer: "silver" as const, table: "promotions", note: "프로모션 정의" },
    ],
  })),
];

/* ─────────────────────────── 실버 6 ─────────────────────────── */

const SILVER: TableSpec[] = [
  {
    layer: "silver",
    table: "reservations",
    view: "v_silver_reservations",
    row_count: 75479,
    masked_fields: [],
    note_ref: "기록 04 실버 빌드 — 브론즈 78,216 − 완전 동일 중복 2,737",
    // 실버는 snake_case 로 표준화된다 — `resv_date` · `visit_status` · 0/1 플래그.
    // 시술 개념은 이 표가 아니라 `reviews`·`catalog` 축에 있다.
    columns: [
      { key: "branch_code", kind: "enum", values: ["CERAMIQUE-GN-001"] },
      { key: "resv_date", kind: "date" },
      { key: "chart_no", kind: "code" },
      { key: "age_band", kind: "enum", values: ["20대", "30대", "40대", "50대", "60대+", "미상"] },
      { key: "staff", kind: "enum", values: ["미지정"] },
      { key: "sales", kind: "money" },
      { key: "receipt", kind: "money" },
      { key: "visit_count", kind: "int", range: [1, 12] },
      { key: "visit_status", kind: "enum", values: ["내원", "취소", "부도"] },
      { key: "is_new", kind: "int", range: [0, 1] },
      { key: "is_revisit", kind: "int", range: [0, 1] },
      { key: "is_payment_visit", kind: "int", range: [0, 1] },
      { key: "is_foreign_est", kind: "int", range: [0, 1] },
    ],
    flows_to: [
      { layer: "gold", table: "gold_kpi_daily", note: "일별 KPI 의 주 원천" },
      { layer: "gold", table: "gold_retention_monthly", note: "코호트 60일" },
    ],
  },
  {
    layer: "silver",
    table: "reviews",
    view: "v_silver_reviews",
    row_count: 1962,
    masked_fields: [],
    note_ref: "기록 04 실버 빌드 — 전건 채점, 판정불가 4건",
    columns: [
      { key: "review_pk", kind: "review_pk" },
      { key: "platform", kind: "enum", values: PLATFORMS },
      { key: "review_date", kind: "date" },
      { key: "rating", kind: "int", range: [1, 5] },
      { key: "body_masked", kind: "text", values: ["[직원]실장님 통해 진행했어요", "대기 시간이 길었습니다", "가격 대비 만족합니다"] },
      { key: "procedure_concept", kind: "enum", values: CONCEPTS },
      { key: "predicted_score", kind: "score" },
      { key: "score_evidence", kind: "text", values: ["잘 설명해주시니 감사합니다", "대기 시간 언급", "가격 만족"] },
      { key: "sentiment", kind: "enum", values: ["긍정", "중립", "부정", "판정불가"] },
      { key: "signal_type", kind: "enum", values: ["유기", "개입"] },
    ],
    flows_to: [
      { layer: "gold", table: "gold_kpi_daily", note: "naver_reviews" },
      { layer: "gold", table: "gold_kpi_weekly", note: "gu_reviews · 긍/부정 분리" },
    ],
  },
  {
    layer: "silver",
    table: "catalog",
    view: "silver_catalog",
    row_count: 6198,
    masked_fields: [],
    note_ref: "기록 04 실버 빌드 — 개념 13 + 그룹 ko 1,010 + 상품 5,175",
    columns: [
      { key: "code", kind: "code" },
      { key: "concept", kind: "enum", values: CONCEPTS },
      { key: "name", kind: "text", values: ["전신 1회", "겨드랑이 5회", "사각턱", "팔자 1cc", "기본 1회", "300샷"] },
      { key: "unit_price", kind: "money" },
      { key: "is_active", kind: "enum", values: ["사용", "중단"] },
    ],
    flows_to: [{ layer: "gold", table: "gold_kpi_daily", note: "avg_ticket" }],
  },
  {
    layer: "silver",
    table: "promotions",
    view: "silver_promotions",
    row_count: 73,
    masked_fields: [],
    note_ref: "기록 04 실버 빌드 — v1 24 + v2 ko 49",
    columns: [
      { key: "start_date", kind: "date" },
      { key: "end_date", kind: "date" },
      { key: "name", kind: "text", values: ["여름 프로모션", "가을 프리퀀시", "리프팅 패키지", "제모 시즌"] },
      { key: "discount_rate", kind: "rate" },
      { key: "target_concept", kind: "enum", values: CONCEPTS },
    ],
    flows_to: [{ layer: "gold", table: "gold_promo_calendar", note: "이벤트 그레인 달력" }],
  },
  {
    layer: "silver",
    table: "mappings",
    view: "silver_mappings",
    row_count: 9689,
    masked_fields: [],
    note_ref: "기록 04 실버 빌드 — 매핑 3종(5,632 + 3,199 + 858)",
    columns: [
      { key: "source", kind: "enum", values: ["nexus", "vegas", "review"] },
      { key: "source_value", kind: "code" },
      { key: "concept", kind: "enum", values: CONCEPTS },
      { key: "rule_id", kind: "enum", values: ["G-008", "G-021", "G-040"] },
      { key: "confidence", kind: "enum", values: ["높음", "중간", "낮음"] },
    ],
    flows_to: [{ layer: "gold", table: "gold_kpi_daily", note: "개념 축 집계" }],
  },
  {
    layer: "silver",
    table: "branch_alias",
    view: "silver_branch_alias",
    row_count: 11,
    masked_fields: [],
    note_ref: "기록 04 실버 빌드 — 표기 → CERAMIQUE-GN-001",
    columns: [
      { key: "alias", kind: "enum", values: ["GN", "강남", "강남점", "SS", "신사"] },
      { key: "canonical", kind: "enum", values: ["CERAMIQUE-GN-001"] },
      { key: "source", kind: "enum", values: ["nexus", "vegas", "review"] },
      { key: "rule_id", kind: "enum", values: ["G-050"] },
      { key: "is_active", kind: "enum", values: ["사용", "중단"] },
    ],
    flows_to: [{ layer: "gold", table: "gold_kpi_daily", note: "지점 단일화 후 집계" }],
  },
];

/* ─────────────────────────── 골드 5 ─────────────────────────── */

const GOLD_DAILY_COLUMNS: ColumnSpec[] = [
  { key: "date", kind: "date" },
  { key: "sales_total", kind: "money" },
  { key: "payment_visits", kind: "int", range: [16, 26] },
  { key: "avg_ticket", kind: "money" },
  { key: "visits", kind: "int", range: [128, 158] },
  { key: "new_patients", kind: "int", range: [10, 20] },
  { key: "revisits", kind: "int", range: [115, 138] },
  { key: "reservations", kind: "int", range: [214, 252] },
  { key: "cancels", kind: "int", range: [72, 94] },
  { key: "cancel_rate", kind: "rate" },
  { key: "noshows", kind: "int", range: [5, 13] },
  { key: "noshow_rate", kind: "rate" },
  { key: "new_churns", kind: "int", range: [3, 10] },
  { key: "naver_reviews", kind: "int", range: [0, 3] },
  { key: "new_patients_domestic", kind: "int", range: [8, 16] },
  { key: "foreign_sales_share", kind: "rate" },
  { key: "sales_foreign_est", kind: "money" },
  { key: "visits_foreign_est", kind: "int", range: [18, 32] },
  { key: "new_patients_foreign_est", kind: "int", range: [2, 5] },
  // 지표마다 `_dod`·`_dod_pct`·`_ma7`·`_status` 파생이 붙는다(SPEC-001 §4). 실 API 는
  // 전 지표분 60여 컬럼을 주고, 픽스처는 **한 지표 몫만 표본**으로 든다 —
  // 「N개 컬럼 중 M개 표시」 규칙이 성립하는지 보기 위한 자리다.
  { key: "sales_total_dod", kind: "money" },
  { key: "sales_total_dod_pct", kind: "rate" },
  { key: "sales_total_ma7", kind: "money" },
  { key: "sales_total_status", kind: "enum", values: ["양호", "주의", "경고"] },
];

const GOLD: TableSpec[] = [
  {
    layer: "gold",
    table: "gold_kpi_daily",
    view: "gold_kpi_daily",
    row_count: 235,
    masked_fields: [],
    note_ref: "기록 05 골드 KPI — 2026-02-17 행 없음(0 채움 없음)",
    columns: GOLD_DAILY_COLUMNS,
    flows_to: [
      { layer: "gold", table: "gold_kpi_weekly", note: "ISO 주 집계" },
      { layer: "gold", table: "gold_kpi_monthly", note: "달력 월 집계" },
    ],
  },
  {
    layer: "gold",
    table: "gold_kpi_weekly",
    view: "gold_kpi_weekly",
    row_count: 34,
    masked_fields: [],
    note_ref: "기록 05 골드 KPI — ISO 주 · 부분 주 플래그",
    columns: [
      { key: "iso_week", kind: "week" },
      { key: "is_partial", kind: "flag" },
      { key: "sales_total", kind: "money" },
      { key: "new_patients", kind: "int", range: [80, 130] },
      { key: "noshow_rate", kind: "rate" },
      { key: "gu_reviews", kind: "int", range: [0, 12] },
      { key: "gu_positive", kind: "int", range: [0, 9] },
      { key: "gu_negative", kind: "int", range: [0, 4] },
      { key: "naver_reviews", kind: "int", range: [0, 96] },
    ],
    flows_to: [{ layer: "gold", table: "gold_kpi_monthly", note: "월 집계와 같은 원천" }],
  },
  {
    layer: "gold",
    table: "gold_kpi_monthly",
    view: "gold_kpi_monthly",
    row_count: 8,
    masked_fields: [],
    note_ref: "기록 05 골드 KPI — 월 View 는 일별에서 집계한다(SPEC-001 §4)",
    // 지표 목록·계산식은 일별의 것을 그대로 쓴다 — 월 View 에 새 정의를 만들지 않는다.
    columns: [
      { key: "month", kind: "month" },
      { key: "is_partial", kind: "flag" },
      ...GOLD_DAILY_COLUMNS.slice(1),
    ],
    flows_to: [],
  },
  {
    layer: "gold",
    table: "gold_promo_calendar",
    view: "gold_promo_calendar",
    row_count: 57,
    masked_fields: [],
    note_ref: "기록 05 골드 — 프로모션 1건 = 이벤트 1행(생존만, v1 23 + v2 34)",
    columns: [],
    columns_note: PROMO_COLUMNS_NOTE,
    flows_to: [],
  },
  {
    layer: "gold",
    table: "gold_retention_monthly",
    view: "gold_retention_monthly",
    row_count: 8,
    masked_fields: [],
    note_ref: "기록 05 4b — 월 코호트 60일 재방문",
    columns: [
      { key: "cohort_month", kind: "month" },
      { key: "cohort_size", kind: "int", range: [380, 520] },
      { key: "revisit_60d", kind: "int", range: [100, 170] },
      { key: "revisit_rate", kind: "rate" },
    ],
    flows_to: [],
  },
];

/* ─────────────────────────── 온톨로지 2 ─────────────────────────── */

/**
 * **데이터 화면에는 나오지 않는 계층**이다(SPEC-004 U-13 · AC-18) — 모니터링 그래프가
 * 이미 그 표면이다. 그래도 `/api/layers/ontology/*` 는 실 API 가 서빙하므로 픽스처를
 * 둔다: 계약 대조와 드릴다운 URL 이 이 계층을 가리킬 수 있기 때문이다.
 *
 * 행은 그래프 픽스처와 **같은 시드**에서 만든다(`mock/graph.ts`) — 표와 그래프가 서로
 * 다른 노드를 보는 일이 없다.
 */
const ONTOLOGY: TableSpec[] = [
  {
    layer: "ontology",
    table: "ontology_nodes",
    view: "ontology_nodes",
    row_count: 25,
    masked_fields: [],
    note_ref: "기록 07 온톨로지",
    columns: [
      { key: "node_id", kind: "code" },
      { key: "name_ko", kind: "text" },
      { key: "node_type", kind: "text" },
      { key: "controllable", kind: "text" },
      { key: "grain", kind: "text" },
      { key: "source", kind: "text" },
    ],
    fixedRows: mockOntologyNodeRows(),
    flows_to: [],
  },
  {
    layer: "ontology",
    table: "ontology_edges",
    view: "ontology_edges",
    row_count: 27,
    masked_fields: [],
    note_ref: "기록 07 온톨로지",
    columns: [
      { key: "cause", kind: "code" },
      { key: "effect", kind: "code" },
      { key: "sign", kind: "text" },
      { key: "lag", kind: "text" },
      { key: "lag_days", kind: "int" },
      { key: "edge_kind", kind: "text" },
      { key: "confidence", kind: "text" },
      { key: "evidence", kind: "text" },
      { key: "verdict", kind: "text" },
      { key: "rationale", kind: "text" },
    ],
    fixedRows: mockOntologyEdgeRows(),
    flows_to: [],
  },
];

const ALL_TABLES: TableSpec[] = [...BRONZE, ...SILVER, ...GOLD, ...ONTOLOGY];

const BY_KEY = new Map(ALL_TABLES.map((spec) => [`${spec.layer}:${spec.table}`, spec]));

export function mockLayerTables(layer: ApiLayer): LayerTable[] {
  return ALL_TABLES.filter((spec) => spec.layer === layer).map<LayerTable>((spec) => ({
    table: spec.table,
    view: spec.view,
    row_count: spec.row_count,
    masked: spec.masked_fields.length > 0,
    masked_fields: spec.masked_fields,
    note_ref: spec.note_ref,
    flows_to: spec.flows_to,
    // 계약은 두 필드를 **항상** 싣는다 — 해당 없으면 `null`(SPEC-003 AC-18·AC-18b).
    // undefined 로 흘려보내면 소비자가 「빠진 것」과 「없는 것」을 구별할 수 없다.
    source_group: spec.source_group ?? null,
    columns_note: spec.columns_note ?? null,
  }));
}

/* ─────────────────────────── 행 생성 ─────────────────────────── */

/** 결정적 난수 — 같은 테이블·오프셋이면 항상 같은 행이 나온다(픽스처의 조건). */
function seeded(seed: string): () => number {
  let h = 2166136261;
  for (let i = 0; i < seed.length; i += 1) {
    h ^= seed.charCodeAt(i);
    h = Math.imul(h, 16777619);
  }
  return () => {
    h = Math.imul(h ^ (h >>> 15), 2246822507);
    h = Math.imul(h ^ (h >>> 13), 3266489909);
    h ^= h >>> 16;
    return (h >>> 0) / 4294967296;
  };
}

const DAY_MS = 86_400_000;
const LAST_DAY = Date.parse("2026-08-30T00:00:00Z");

function dateAt(index: number): string {
  return new Date(LAST_DAY - index * DAY_MS).toISOString().slice(0, 10);
}

function cellValue(spec: ColumnSpec, rnd: () => number, index: number): RowValue {
  switch (spec.kind) {
    case "date":
      return dateAt(Math.floor(index / 3));
    case "compact_date":
      return dateAt(Math.floor(index / 3)).replaceAll("-", "");
    case "timestamp":
      return `${dateAt(Math.floor(index / 3))} ${String(9 + (index % 9)).padStart(2, "0")}:${String((index * 7) % 60).padStart(2, "0")}:00`;
    case "review_pk":
      return `naver_dom_${2_000_000_000 + Math.floor(rnd() * 99_999_999)}_${Math.floor(rnd() * 0xffffff).toString(16).padStart(6, "0")}`;
    case "score":
      return Number(((Math.floor(rnd() * 9) + 1) * 0.5).toFixed(1));
    case "week": {
      const week = 34 - Math.floor(index);
      return `2026-W${String(Math.max(week, 1)).padStart(2, "0")}`;
    }
    case "month": {
      const month = 8 - index;
      return month >= 1 ? `2026-${String(month).padStart(2, "0")}` : "2025-12";
    }
    case "int": {
      const [min, max] = spec.range ?? [0, 100];
      return min + Math.floor(rnd() * (max - min + 1));
    }
    case "money":
      return Math.round((300_000 + rnd() * 13_000_000) / 1000) * 1000;
    case "rate":
      return Number((0.03 + rnd() * 0.55).toFixed(3));
    case "flag":
      return index === 0 ? "부분" : "완전";
    case "code":
      return String(37_000 + Math.floor(rnd() * 5_000));
    case "enum":
    case "text": {
      const values = spec.values ?? ["—"];
      return values[Math.floor(rnd() * values.length)];
    }
    // ── PII 는 마스킹 표기로만 만든다. 원값을 픽스처에도 두지 않는다. ──
    case "masked_name":
      return `${SURNAMES[Math.floor(rnd() * SURNAMES.length)]}○○`;
    case "masked_handle":
      // 원천 닉네임 자체가 마스킹본이다 — 앞 3자 + `****`.
      return `${"abcdefghijklmnopqrstuvwxyz"[Math.floor(rnd() * 26)]}${"abcdefghijklmnopqrstuvwxyz"[Math.floor(rnd() * 26)]}${"abcdefghijklmnopqrstuvwxyz"[Math.floor(rnd() * 26)]}****`;
    case "masked_phone":
      return `010-****-${String(1000 + Math.floor(rnd() * 9000))}`;
    case "masked_birth":
      return `${1960 + Math.floor(rnd() * 45)}-**-**`;
  }
}

export interface MockRowQuery {
  limit: number;
  offset: number;
  /** 드릴다운·「전체 보기」가 넘긴 필터. 값 일치(eq)와 between 만 다룬다. */
  filters?: { field: string; op: string; value: RowValue | RowValue[] }[];
}

export function mockLayerRows(
  layer: ApiLayer,
  table: string,
  query: MockRowQuery,
): LayerRowsResponse | null {
  const spec = BY_KEY.get(`${layer}:${table}`);
  if (!spec) return null;

  const columns = spec.columns.map((c) => c.key);
  if (columns.length === 0) {
    return {
      layer,
      table,
      view: spec.view,
      total: spec.row_count,
      returned: 0,
      offset: 0,
      masked_fields: spec.masked_fields,
      columns: [],
      rows: [],
      source_note: SOURCE_NOTE,
    };
  }

  // 정본 그대로 싣는 표(온톨로지) — 생성기를 태우지 않고 잘라서 준다.
  if (spec.fixedRows) {
    const page = spec.fixedRows.slice(query.offset, query.offset + query.limit);
    return {
      layer,
      table,
      view: spec.view,
      total: spec.fixedRows.length,
      returned: page.length,
      offset: query.offset,
      masked_fields: spec.masked_fields,
      columns,
      rows: page,
      source_note: SOURCE_NOTE,
    };
  }

  const filters = query.filters ?? [];
  // 필터가 걸리면 전체 건수도 줄어든다 — 결정적 비율로 접는다(픽스처 규약).
  const filterRatio = filters.length === 0 ? 1 : 1 / (filters.length + 2.4);
  const total = Math.max(Math.round(spec.row_count * filterRatio), Math.min(spec.row_count, 1));
  const returned = Math.max(Math.min(query.limit, total - query.offset), 0);

  const rows: Record<string, RowValue>[] = [];
  for (let i = 0; i < returned; i += 1) {
    const absolute = query.offset + i;
    const rnd = seeded(`${layer}:${table}:${absolute}`);
    const row: Record<string, RowValue> = {};
    for (const column of spec.columns) {
      row[column.key] = cellValue(column, rnd, absolute);
    }
    // eq 필터는 값을 고정한다 — 「8월 취소 원본」이 전 행 취소로 보여야 한다.
    for (const filter of filters) {
      if (filter.op === "eq" && filter.field in row) {
        row[filter.field] = filter.value as RowValue;
      }
    }
    rows.push(row);
  }

  return {
    layer,
    table,
    view: spec.view,
    total,
    returned,
    offset: query.offset,
    masked_fields: spec.masked_fields,
    columns,
    rows,
    source_note: SOURCE_NOTE,
  };
}

export function mockTableExists(layer: ApiLayer, table: string): boolean {
  return BY_KEY.has(`${layer}:${table}`);
}

export function mockTableSpecColumns(layer: ApiLayer, table: string): string[] {
  return BY_KEY.get(`${layer}:${table}`)?.columns.map((c) => c.key) ?? [];
}
