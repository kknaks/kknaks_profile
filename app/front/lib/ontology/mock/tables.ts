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

import type { Layer, LayerTable, LayerRowsResponse, RowValue, SourceGroup } from "../types";

/* ─────────────────────────── 컬럼 스펙 ─────────────────────────── */

type ColumnKind =
  | "date"
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
  layer: Layer;
  table: string;
  view: string;
  row_count: number;
  masked_fields: string[];
  columns: ColumnSpec[];
  note_ref: string;
  flows_to: { layer: Layer; table: string; note?: string }[];
  source_group?: SourceGroup;
  columns_note?: string;
}

const SURNAMES = ["김", "이", "박", "최", "정", "강", "조", "윤", "장", "임", "한", "오", "신", "권", "서"];
const CONCEPTS = ["제모", "리프팅", "스킨케어", "주사", "색소", "여드름", "체형"];
const PLATFORMS = ["네이버 플레이스", "강남언니"];

const UNKNOWN_COLUMNS_NOTE =
  "정본(빌드 실측)에 이 테이블의 컬럼 목록이 없어 비워 두었습니다 — 화면이 지어내지 않습니다. 행수는 응답값입니다.";

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

const BRONZE: TableSpec[] = [
  {
    layer: "bronze",
    table: "vegas_reservations",
    view: "v_bronze_vegas_reservations",
    row_count: 78216,
    masked_fields: ["patientName", "phone", "birthday"],
    source_group: "vegas",
    note_ref: "기록 02 브론즈 실사",
    columns: [
      { key: "resvDate", kind: "date" },
      { key: "chartNo", kind: "code" },
      { key: "patientName", kind: "masked_name" },
      { key: "phone", kind: "masked_phone" },
      { key: "birthday", kind: "masked_birth" },
      { key: "ageBand", kind: "enum", values: ["20대", "30대", "40대", "50대", "60대+"] },
      { key: "sales", kind: "money" },
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
    columns: [
      { key: "date", kind: "date" },
      { key: "platform", kind: "enum", values: PLATFORMS },
      { key: "authorName", kind: "masked_name" },
      { key: "rating", kind: "int", range: [1, 5] },
      {
        key: "body",
        kind: "text",
        values: [
          "상담이 꼼꼼했어요",
          "대기 시간이 길었습니다",
          "시술 후 관리 안내가 좋았어요",
          "가격 대비 만족합니다",
          "예약 변경이 번거로웠어요",
          "설명이 이해하기 쉬웠습니다",
          "○○ 실장님이 친절했어요",
        ],
      },
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
    view: `v_bronze_${child.table}`,
    row_count: child.rows,
    masked_fields: [],
    source_group: "nexus",
    note_ref: "기록 02 브론즈 실사",
    columns: [],
    columns_note: UNKNOWN_COLUMNS_NOTE,
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
    columns: [
      { key: "date", kind: "date" },
      { key: "chart_no", kind: "code" },
      { key: "age_band", kind: "enum", values: ["20대", "30대", "40대", "50대", "60대+", "미상"] },
      { key: "staff", kind: "enum", values: ["미지정"] },
      { key: "sales", kind: "money" },
      { key: "visit_status", kind: "enum", values: ["내원", "취소", "부도"] },
      { key: "is_new", kind: "enum", values: ["신환", "재진"] },
      { key: "concept", kind: "enum", values: CONCEPTS },
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
      { key: "date", kind: "date" },
      { key: "platform", kind: "enum", values: PLATFORMS },
      { key: "concept", kind: "enum", values: CONCEPTS },
      { key: "sentiment", kind: "enum", values: ["긍정", "중립", "부정", "판정불가"] },
      { key: "signal_type", kind: "enum", values: ["유기(강남언니)", "개입(네이버)"] },
      {
        key: "evidence",
        kind: "text",
        values: ["상담 품질 언급", "대기 시간 언급", "사후 관리 안내", "가격 만족", "예약 변경 절차"],
      },
    ],
    flows_to: [
      { layer: "gold", table: "gold_kpi_daily", note: "naver_reviews" },
      { layer: "gold", table: "gold_kpi_weekly", note: "gu_reviews · 긍/부정 분리" },
    ],
  },
  {
    layer: "silver",
    table: "catalog",
    view: "v_silver_catalog",
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
    view: "v_silver_promotions",
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
    view: "v_silver_mappings",
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
    view: "v_silver_branch_alias",
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
  { key: "new_patients_foreign_est", kind: "int", range: [2, 5] },
  { key: "visits_foreign_est", kind: "int", range: [18, 32] },
  { key: "sales_foreign_est", kind: "money" },
  { key: "foreign_sales_share", kind: "rate" },
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
    columns_note:
      "그레인이 일별 → 이벤트로 바뀌면서 이전 컬럼(date·promo_count·is_promo_day)이 성립하지 않습니다. 정본에 이벤트 그레인의 컬럼 목록이 없어 비워 두었습니다 — 빌드 실측 후 채웁니다.",
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

const ALL_TABLES: TableSpec[] = [...BRONZE, ...SILVER, ...GOLD];

const BY_KEY = new Map(ALL_TABLES.map((spec) => [`${spec.layer}:${spec.table}`, spec]));

export function mockLayerTables(layer: Layer): LayerTable[] {
  return ALL_TABLES.filter((spec) => spec.layer === layer).map<LayerTable>((spec) => ({
    table: spec.table,
    row_count: spec.row_count,
    masked: spec.masked_fields.length > 0,
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
  layer: Layer,
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
  };
}

export function mockTableExists(layer: Layer, table: string): boolean {
  return BY_KEY.has(`${layer}:${table}`);
}

export function mockTableSpecColumns(layer: Layer, table: string): string[] {
  return BY_KEY.get(`${layer}:${table}`)?.columns.map((c) => c.key) ?? [];
}
