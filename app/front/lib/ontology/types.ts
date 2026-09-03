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

/** 데이터 화면이 다루는 계층. 온톨로지 계층은 제외한다(SPEC-004 U-13 · AC-18). */
export type Layer = "bronze" | "silver" | "gold";

/**
 * `/api/layers/{layer}` 가 받는 계층 — **온톨로지를 포함한다**(SPEC-003 §4).
 * 화면 탭이 3계층인 것과 API 표면이 4계층인 것은 다른 층이다.
 */
export type ApiLayer = Layer | "ontology";

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
  /** 노드 상태 판정 창(기본 7). 화면 카피가 이 값으로 만들어진다 — 숫자를 박지 않는다. */
  window_days: number;
  /**
   * 기간 스테퍼 양쪽 화살표의 비활성 근거를 **서버가 준다**(SPEC-003 v0.0.6 §4).
   * 이전 기간이 없으면 `has_prev_period: false`, 다음이 없으면 `has_next_period: false`.
   */
  has_prev_period: boolean;
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
  /**
   * 그 노드가 관측되는 그레인(`daily` · `weekly` · `monthly` · `monthly_cohort` ·
   * `event` · `promo` · `unknown`). 카드의 `grain` 과 같은 축이다.
   */
  grain: string;
  /**
   * 「원본 데이터 보기」 목적지의 출처. 테이블 이름이거나, 테이블이 아닌 출처면
   * 사람이 읽는 문자열이다(예: 「달력」·「데이터 부재 — 담당자 확인 항목」).
   */
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
  /** 기준일 — 그래프도 일 배치 산출물이다. */
  as_of: string;
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

/** 브론즈 원천 축 — 실버·골드는 `null` 이다(SPEC-003 §4 · AC-18). */
export type SourceGroup = "vegas" | "review" | "nexus";

export interface LayerTable {
  table: string;
  /** 소비자가 실제로 읽는 뷰·테이블 이름. 마스킹 대상은 `v_` 뷰다(SPEC-001 §4). */
  view: string;
  row_count: number;
  masked: boolean;
  /** 마스킹 컬럼 이름. 마스킹 바의 개수·이름이 여기서 파생된다. */
  masked_fields: string[];
  note_ref: string;
  flows_to: FlowTarget[];
  /**
   * 브론즈 1단 원천 축. 데이터 화면의 2단 칩(원천 3 → nexus 하위 14)이 이 값으로 묶인다
   * — **화면이 테이블 이름을 파싱해 그룹을 추측하지 않는다**(SPEC-004 U-13).
   */
  source_group: SourceGroup | null;
  /**
   * **컬럼 목록이 계약에 없는 테이블**의 사유 문자열(브론즈 `nexus_*` 14종 ·
   * `gold_promo_calendar`). 그 밖은 `null`. 화면은 빈 컬럼을 침묵으로 두지 않고 이 사유를
   * 표기한다 — 컬럼이 안 보이는 것과 「계약에 없어서 안 보이는 것」은 다른 사실이다.
   */
  columns_note: string | null;
}

export interface LayerTablesResponse {
  layer: ApiLayer;
  tables: LayerTable[];
}

export type RowValue = string | number | boolean | null;

export interface LayerRowsResponse {
  layer: ApiLayer;
  table: string;
  view: string;
  total: number;
  returned: number;
  offset: number;
  masked_fields: string[];
  columns: string[];
  rows: Record<string, RowValue>[];
  /** 이 행들이 어느 경로로 나왔는지 — 「마스킹 뷰 경유」임을 응답이 스스로 밝힌다. */
  source_note: string;
  // `columns_note` 는 **테이블 목록 응답**이 갖는다(`LayerTable`) — 행 조회 응답에는
  // 없다(SPEC-003 §4 · AC-18b). 같은 사실을 두 응답에 싣지 않는다.
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

/**
 * 실패 사유 코드 — `AI_TIMEOUT`(180초 초과) · `AI_FAILED`(그 밖의 실패).
 * 같은 버블·같은 배지 규격이고 **문장만** 갈린다(SPEC-004 U-9 #3·#4).
 */
export type FailureCode = "AI_FAILED" | "AI_TIMEOUT";

/**
 * **FE 는 문구가 아니라 이 코드로 분기한다**(SPEC-003 §4) — 문구 매칭으로 갈라내면
 * 카피가 바뀔 때 조용히 깨진다. 값이 없으면 일반 실패다(타임아웃을 추측하지 않는다).
 */
export function isTimeout(message: Pick<ChatMessage, "error_code">): boolean {
  return message.error_code === "AI_TIMEOUT";
}

export interface ToolStep {
  tool: string;
  args_summary: string;
  duration_ms: number | null;
  called_at: string;
  /**
   * 그 도구 호출이 실패했는지. 화면은 실패 단계를 **상태 dot 으로만** 구분하고
   * (기존 알림 토큰) 에러 원문을 노출하지 않는다 — `args_summary` 와 같은 규율이다.
   * 값이 없으면 성공으로 본다.
   */
  is_error?: boolean;
}

export interface ChatMessage {
  id: string;
  role: "user" | "assistant";
  status: MessageStatus;
  content: string;
  steps: ToolStep[];
  result?: AnswerResult | null;
  /** `status: failed` 일 때만 값을 갖는다. `pending`·`done` 이면 `null`(SPEC-003 AC-19). */
  error_code: FailureCode | null;
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
  /** 400 — `failed` 가 아닌 메시지에 재시도를 걸었을 때. FE 가 UI 로 선차단한다. */
  | "RETRY_NOT_ALLOWED"
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
