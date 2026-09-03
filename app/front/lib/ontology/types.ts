/**
 * 온톨로지 데모 — API 응답 타입.
 *
 * **SoT 는 spec 이고 이 파일은 전사(轉寫)다.** 필드를 늘리거나 이름을 바꾸지 않는다 —
 * 화면이 필요로 하는 값이 없으면 여기서 지어내지 말고 spec 개정으로 올린다
 * (SPEC-004 §「Internal Interface Contract」).
 *
 * - 계층·enum·마스킹 표기 → SPEC-001 §4
 * - 엔드포인트·응답 shape  → SPEC-003 §4
 * - 답변 객체(`result`)    → SPEC-005 §4
 */

/** 데이터 화면이 다루는 계층. 온톨로지 계층은 제외한다(SPEC-004 U-13). */
export type Layer = "bronze" | "silver" | "gold";

/** 노드 상태 — 최근 window_days 의 빈도 판정(SPEC-003 OQ-5). */
export type NodeState = "정상" | "관찰" | "알림" | "미관측";

/** KPI 상태 — 그 시점의 값 판정(SPEC-001 §4 골드). */
export type KpiStatus = "양호" | "주의" | "경고";

/** 엣지 판정 — 한글 정본값이 그대로 계약 값이다. 번역이 없다(SPEC-001 §4). */
export type Verdict = "채택" | "자동 확정" | "선언" | "보류" | "기각";

/** 노드 유형 — 영문 enum 이 정본. 화면 카피 매핑은 SPEC-004 U-5 가 갖는다. */
export type NodeType =
  | "kpi"
  | "intervention"
  | "organic"
  | "exogenous"
  | "unobserved"
  | "attribute";

export type EdgeKind = "causal" | "derivation" | "exogenous" | "candidate" | "rejected";

export type Confidence = "높음" | "중간" | "낮음";

/* ─────────────────────────── 접속 게이트 ─────────────────────────── */

export interface SessionResponse {
  ok: boolean;
}

/* ─────────────────────────── KPI ─────────────────────────── */

export interface KpiCard {
  metric: string;
  label: string;
  /** 카드마다 다르다 — 캡션을 이 값으로 만든다. 「(주간)」을 하드코딩하지 않는다. */
  grain: string;
  latest: number | null;
  unit: string;
  format: "percent" | "number" | "currency";
  dod: number | null;
  dod_pct: number | null;
  /** 최근 7개 값. 미관측 카드는 null — 스파크라인을 그리지 않는다. */
  spark: number[] | null;
  /** 개입 신호(방향 없는 변수)는 status·node_state 를 갖지 않는다 → null. */
  status: KpiStatus | null;
  alert_days: number;
  node_state: NodeState | null;
  /** 그래프 노드와 잇는 키(SPEC-001 §4 25종). */
  node_id: string;
  thresholds: Record<string, number> | null;
  direction: string | null;
}

export interface KpiCardsResponse {
  as_of: string;
  period: string;
  window_days: number;
  has_next_period: boolean;
  cards: KpiCard[];
}

/* ─────────────────────────── 그래프 ─────────────────────────── */

export interface GraphNode {
  node_id: string;
  name: string;
  node_type: NodeType;
  controllable: boolean;
  observed: boolean;
  node_state: NodeState | null;
  alert_days: number | null;
  /** 「원본 데이터 보기」 목적지의 출처. `<table>.<column>` 또는 `<table>`. */
  source: string | null;
}

export interface GraphEdge {
  /** `<from>__<to>` — 응답이 문자열로 실어 준다. 화면이 조립하지 않는다. */
  edge_id: string;
  from: string;
  to: string;
  /** `+` · `−` 외에 `0`(항등식) · `exo` · `?` · 빈 값(기각)이 온다. */
  sign: string;
  /** 정본 문자열 원형 — `2w` 를 `14d` 로 고치지 않는다. */
  lag: string;
  lag_days: number | null;
  verdict: Verdict;
  kind: EdgeKind;
  /** `채택` 에만 있다. */
  confidence: Confidence | null;
  evidence: string;
  note: string | null;
  /** 기각·보류 사유. */
  reason: string | null;
  usable_for_causal_claim: boolean;
}

export interface GraphResponse {
  nodes: GraphNode[];
  edges: GraphEdge[];
  counts: Record<string, number>;
}

/* ─────────────────────────── 예보 ─────────────────────────── */

export interface ForecastEdge {
  edge_id: string;
  from: string;
  to: string;
  verdict: Verdict;
  sign: string;
  lag: string;
  lag_days: number | null;
  confidence: Confidence | null;
  evidence: string;
}

export interface ForecastEvidence {
  metric: string;
  value: number;
  period: { start: string; end: string };
}

export interface ForecastItem {
  rule: string;
  title: string;
  message: string;
  edge: ForecastEdge;
  trigger: string;
  target: string;
  horizon: string;
  risk: NodeState;
  evidence?: ForecastEvidence[];
  note?: string;
}

export interface ForecastResponse {
  as_of: string;
  forecasts: ForecastItem[];
}

/* ─────────────────────────── 계층 조회 ─────────────────────────── */

export interface FlowTarget {
  layer: Layer;
  table: string;
  note?: string;
}

export interface LayerTable {
  table: string;
  row_count: number;
  masked: boolean;
  note_ref: string;
  flows_to: FlowTarget[];
  /**
   * 브론즈 1단 원천 축(vegas · reviewCsv · nexus). 계층 탭 카운트는 **테이블 수**이고
   * 이 값은 칩 그룹핑에만 쓴다(SPEC-004 U-13).
   */
  source_group?: string;
}

export interface LayerTablesResponse {
  layer: Layer;
  tables: LayerTable[];
}

export type RowValue = string | number | boolean | null;

export interface LayerRowsResponse {
  layer: Layer;
  table: string;
  view: string;
  total: number;
  returned: number;
  offset: number;
  masked_fields: string[];
  columns: string[];
  rows: Record<string, RowValue>[];
  /** 정본에 컬럼 목록이 없는 테이블은 그 사실을 실어 보낸다(디자인 08 규칙 8). */
  columns_note?: string | null;
}

export interface LineageColumn {
  column: string;
  formula?: string | null;
  note?: string | null;
  /** 실버 글로서리 규칙 ID(G-0xx). 골드는 null. */
  rule_id: string | null;
  /** 통과한 게이트와 예외 처리. */
  gate?: string | null;
  source_columns: string[];
  downstream: { layer: Layer; table: string; column: string }[];
  /** 아직 확정되지 않은 값 — `—` + 「미확정」. null(관측 없음)과 다른 층이다. */
  is_provisional: boolean;
  note_ref: string;
  status_thresholds?: Record<string, string | number> | null;
}

export interface LineageResponse {
  table: string;
  columns: LineageColumn[];
}

/* ─────────────────────────── 답변 객체 (SPEC-005 §4) ─────────────────────────── */

export interface PremiseCorrection {
  corrected: boolean;
  claimed?: string;
  actual?: string;
  restated_question?: string;
}

export interface UsedEdge {
  edge_id: string;
  from: string;
  to: string;
  verdict: Verdict;
  sign: string;
  lag: string;
  lag_days: number | null;
  confidence?: Confidence | null;
  role?: string;
}

export interface ExcludedEdge {
  edge_id: string;
  from: string;
  to: string;
  verdict: Verdict;
  reason: string;
}

export interface Citation {
  claim: string;
  value: number | null;
  metric: string;
  grain: string;
  period: { start: string; end: string };
  row_count: number;
  source: { tool: string; table: string; column: string };
}

export interface DrilldownFilter {
  field: string;
  op: string;
  value: RowValue | RowValue[];
}

export interface Drilldown {
  layer: Layer;
  table: string;
  view: string;
  filters: DrilldownFilter[];
  columns: string[];
  masked_fields: string[];
  rows: Record<string, RowValue>[];
  total: number;
}

export interface Unknown {
  topic: string;
  reason: string;
}

export interface AnswerResult {
  answer: string;
  premise_correction: PremiseCorrection;
  used_edges: UsedEdge[];
  excluded_edges?: ExcludedEdge[];
  citations: Citation[];
  drilldown?: Drilldown | null;
  followups?: string[];
  unknowns?: Unknown[];
}

/* ─────────────────────────── 채팅 ─────────────────────────── */

export type MessageStatus = "pending" | "done" | "failed";

/** 실패 사유 코드 — 화면은 문구로만 구분한다(SPEC-003 Case Matrix). */
export type FailureCode = "AI_FAILED" | "AI_TIMEOUT";

export interface ToolStep {
  tool: string;
  args_summary: string;
  duration_ms: number | null;
  called_at: string;
}

export interface ChatMessage {
  id: string;
  role: "user" | "assistant";
  status: MessageStatus;
  content: string;
  steps: ToolStep[];
  result?: AnswerResult | null;
  error_code?: FailureCode | null;
  created_at: string;
}

export interface Conversation {
  id: string;
  title: string;
  created_at: string;
  last_message_at: string;
}

export interface ConversationResponse {
  conversation: Conversation;
  messages: ChatMessage[];
}

/* ─────────────────────────── 에러 ─────────────────────────── */

export type OntologyErrorCode =
  | "NO_SESSION"
  | "INVALID_PASSWORD"
  | "UNKNOWN_TABLE"
  | "UNKNOWN_FIELD"
  | "UNKNOWN_METRIC"
  | "INVALID_RANGE"
  | "LIMIT_EXCEEDED"
  | "EMPTY_QUESTION"
  | "QUESTION_TOO_LONG"
  | "NOT_FOUND"
  | "CONVERSATION_BUSY"
  | "SOURCE_UNAVAILABLE";

export class OntologyApiError extends Error {
  readonly code: OntologyErrorCode | string;
  readonly httpStatus: number;

  constructor(code: OntologyErrorCode | string, httpStatus: number) {
    super(code);
    this.name = "OntologyApiError";
    this.code = code;
    this.httpStatus = httpStatus;
  }
}
