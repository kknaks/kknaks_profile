/**
 * mock — 채팅(`/api/chat/*`).
 *
 * 서버가 진실을 갖는 구조(폴딩 + 2초 폴링)를 그대로 흉내 낸다. `pending` 동안
 * `content`(부분 텍스트)와 `steps`(도구 단계)가 **경과 시간에서 파생**되므로, 화면은
 * 실 API 와 똑같이 `GET /api/chat/conversations/{id}` 를 2초마다 부르기만 하면 된다.
 *
 * 답변 객체는 SPEC-005 §4 스키마이고, 예문 소재는 SPEC-004 §7.3 · 디자인 05 의 패턴
 * A~D 다 — **없는 엣지·지어낸 수치를 쓰지 않는다**(디자인 08 규칙 8). 수치는 SPEC-005
 * §6 회귀 3본(R-1·R-2·R-3)의 실측값이다.
 *
 * mock 한정 트리거(실 API 에는 없다): 질문에 「실패」가 있으면 `AI_FAILED`,
 * 「타임아웃」·「시간 초과」가 있으면 `AI_TIMEOUT` 으로 마감한다 — 화면의 상태 5종을
 * 실제로 밟아 보기 위한 픽스처 장치다.
 */

import type {
  AnswerResult,
  ChatMessage,
  Conversation,
  ConversationResponse,
  ToolStep,
} from "../types";
import { OntologyApiError } from "../types";
import { mockLayerRows } from "./tables";

const STEP_INTERVAL_MS = 1600;
const TAIL_MS = 1400;

type Outcome = "done" | "failed" | "timeout";

interface Plan {
  steps: ToolStep[];
  /** 단계 진행에 맞춰 자라는 부분 텍스트 — 스피너만 두지 않기 위한 재료다. */
  partials: string[];
  outcome: Outcome;
  result: AnswerResult | null;
}

interface StoredMessage {
  id: string;
  role: "user" | "assistant";
  createdAt: string;
  content: string;
  plan?: Plan;
  startedAt?: number;
}

interface StoredConversation {
  conversation: Conversation;
  messages: StoredMessage[];
}

const STORE = new Map<string, StoredConversation>();
let sequence = 0;

function nextId(prefix: string): string {
  sequence += 1;
  return `${prefix}-${sequence.toString(36)}-${Date.now().toString(36)}`;
}

function step(tool: string, args_summary: string, duration_ms: number): ToolStep {
  return { tool, args_summary, duration_ms, called_at: new Date().toISOString() };
}

/* ─────────────────────────── 답변 패턴 ─────────────────────────── */

/** A. 전제 교정 — SPEC-005 R-2. */
function patternPremise(): Plan {
  const result: AnswerResult = {
    answer:
      "8월 매출은 떨어지지 않았습니다. **3.69억**으로 7월 **2.91억** 대비 **+27%**, 8개월 중 2위입니다.\n\n" +
      "실제로 떨어진 것은 **내원(5,428 → 4,196)** 과 **예약(9,057 → 6,852)** 이고 둘 다 기간 최저입니다. " +
      "매출이 버틴 이유는 **결제 내원이 +23%(641건)** 늘고 **객단가 58만 원**이 유지됐기 때문입니다.\n\n" +
      "예약 하락의 후보는 둘입니다. 취소율이 7월 **36.3%**(기간 피크)에서 8월 **35.5%** 로 높은 구간에 머물렀고, " +
      "주별 네이버 리뷰가 7월 말 **96 → 12 → 8 → 4건**으로 급감했습니다.",
    premise_correction: {
      corrected: true,
      claimed: "8월 매출이 떨어졌다",
      actual: "8월 매출 3.69억 (7월 2.91억 대비 +27%, 8개월 중 2위)",
      restated_question: "내원·예약은 왜 떨어졌고 매출은 왜 버텼나",
    },
    used_edges: [
      {
        edge_id: "payment_visits__sales_total",
        from: "payment_visits",
        to: "sales_total",
        verdict: "자동 확정",
        sign: "0",
        lag: "",
        lag_days: null,
        role: "매출이 버틴 경로",
      },
      {
        edge_id: "cancel_rate__reservations",
        from: "cancel_rate",
        to: "reservations",
        verdict: "채택",
        sign: "−",
        lag: "0d",
        lag_days: 0,
        confidence: "중간",
        role: "예약 하락 원인 후보 1",
      },
      {
        edge_id: "naver_reviews__reservations",
        from: "naver_reviews",
        to: "reservations",
        verdict: "채택",
        sign: "+",
        lag: "0d",
        lag_days: 0,
        confidence: "중간",
        role: "예약 하락 원인 후보 2",
      },
    ],
    citations: [
      {
        claim: "8월 매출 3.69억",
        value: 369_000_000,
        metric: "sales_total",
        grain: "monthly",
        period: { start: "2026-08-01", end: "2026-08-30" },
        row_count: 30,
        source: { tool: "query_kpi", table: "gold_kpi_monthly", column: "sales_total" },
      },
      {
        claim: "7월 매출 2.91억",
        value: 291_000_000,
        metric: "sales_total",
        grain: "monthly",
        period: { start: "2026-07-01", end: "2026-07-31" },
        row_count: 31,
        source: { tool: "query_kpi", table: "gold_kpi_monthly", column: "sales_total" },
      },
      {
        claim: "8월 내원 4,196",
        value: 4196,
        metric: "visits",
        grain: "monthly",
        period: { start: "2026-08-01", end: "2026-08-30" },
        row_count: 30,
        source: { tool: "query_kpi", table: "gold_kpi_monthly", column: "visits" },
      },
      {
        claim: "8월 예약 6,852",
        value: 6852,
        metric: "reservations",
        grain: "monthly",
        period: { start: "2026-08-01", end: "2026-08-30" },
        row_count: 30,
        source: { tool: "query_kpi", table: "gold_kpi_monthly", column: "reservations" },
      },
      {
        claim: "8월 결제 내원 641건 (+23%)",
        value: 641,
        metric: "payment_visits",
        grain: "monthly",
        period: { start: "2026-08-01", end: "2026-08-30" },
        row_count: 30,
        source: { tool: "query_kpi", table: "gold_kpi_monthly", column: "payment_visits" },
      },
      {
        claim: "8월 객단가 58만 원",
        value: 580_000,
        metric: "avg_ticket",
        grain: "monthly",
        period: { start: "2026-08-01", end: "2026-08-30" },
        row_count: 30,
        source: { tool: "query_kpi", table: "gold_kpi_monthly", column: "avg_ticket" },
      },
      {
        claim: "8월 취소율 35.5%",
        value: 0.355,
        metric: "cancel_rate",
        grain: "monthly",
        period: { start: "2026-08-01", end: "2026-08-30" },
        row_count: 30,
        source: { tool: "query_kpi", table: "gold_kpi_monthly", column: "cancel_rate" },
      },
    ],
    followups: ["취소율이 언제부터 올랐어?", "그 8월 취소 원본 20건 보여줘", "네이버 리뷰는 왜 줄었어?"],
    unknowns: [],
  };

  return {
    outcome: "done",
    result,
    steps: [
      step("query_kpi", "sales_total · monthly · 2026-07~08", 420),
      step("query_kpi", "visits · reservations · monthly", 380),
      step("trace_ontology", "target=sales_total · 확정 엣지만", 610),
      step("query_kpi", "payment_visits · avg_ticket · cancel_rate", 350),
    ],
    partials: [
      "8월 매출부터 확인하겠습니다.",
      "8월 매출은 떨어지지 않았습니다 — 3.69억으로 7월 대비 +27% 입니다.",
      "실제로 떨어진 것은 내원과 예약입니다. 매출로 가는 확정 경로를 되짚는 중입니다.",
      "결제 내원과 객단가로 매출이 버틴 구조를 확인했습니다.",
    ],
  };
}

/** B. 원인 추적 · 기각 배제 — 디자인 05 패턴 B. */
function patternRejected(): Plan {
  const result: AnswerResult = {
    answer:
      "그 경로는 **기각된 엣지**입니다 — `신환 수 → 매출` 은 시차 1~28일 전체에서 최대 **r=0.14** 로 효과가 잡히지 않았습니다. " +
      "매출 금액은 시술 구성에 좌우되기 때문입니다.\n\n" +
      "대신 실재하는 경로는 **신환 수 → 결제 내원 수**(채택 · `+` · lag `7d` · 신뢰도 높음)이고, " +
      "결제 내원이 항등식으로 매출에 이어집니다.",
    premise_correction: { corrected: false },
    used_edges: [
      {
        edge_id: "new_patients__payment_visits",
        from: "new_patients",
        to: "payment_visits",
        verdict: "채택",
        sign: "+",
        lag: "7d",
        lag_days: 7,
        confidence: "높음",
        role: "신환이 매출로 가는 실재 경로",
      },
      {
        edge_id: "payment_visits__sales_total",
        from: "payment_visits",
        to: "sales_total",
        verdict: "자동 확정",
        sign: "0",
        lag: "",
        lag_days: null,
        role: "항등식",
      },
    ],
    excluded_edges: [
      {
        edge_id: "new_patients__sales_total",
        from: "new_patients",
        to: "sales_total",
        verdict: "기각",
        reason: "최대 r=0.14 (시차 1~28일) — 매출 금액은 시술 구성에 좌우",
      },
    ],
    citations: [
      {
        claim: "신환 → 결제 내원 잔차 r=0.579 (n=227)",
        value: 0.579,
        metric: "new_patients",
        grain: "daily",
        period: { start: "2026-01-07", end: "2026-08-30" },
        row_count: 227,
        source: { tool: "trace_ontology", table: "ontology_edges", column: "evidence" },
      },
      {
        claim: "8월 결제 내원 641건",
        value: 641,
        metric: "payment_visits",
        grain: "monthly",
        period: { start: "2026-08-01", end: "2026-08-30" },
        row_count: 30,
        source: { tool: "query_kpi", table: "gold_kpi_monthly", column: "payment_visits" },
      },
    ],
    followups: ["결제 내원은 8월에 어떻게 움직였어?", "기각된 엣지가 또 있어?"],
    unknowns: [],
  };

  return {
    outcome: "done",
    result,
    steps: [
      step("trace_ontology", "from=new_patients · to=sales_total", 540),
      step("trace_ontology", "verdicts=기각", 300),
      step("query_kpi", "payment_visits · monthly", 360),
    ],
    partials: [
      "신환에서 매출로 가는 엣지를 확인하겠습니다.",
      "그 경로는 기각된 엣지입니다 — 최대 r=0.14 로 효과가 잡히지 않았습니다.",
      "대신 결제 내원을 경유하는 확정 경로를 제시합니다.",
    ],
  };
}

/** C. 관계 방향 — 정량 추정을 만들지 않는다(SPEC-005 §5). */
function patternDirection(): Plan {
  const result: AnswerResult = {
    answer:
      "강남언니 리뷰 수는 신환 수와 **같은 방향**으로 움직이는 채택 엣지입니다 — 리뷰가 늘면 약 **2주 뒤** 신환이 늘고, 줄면 그 반대입니다.\n\n" +
      "다만 **신뢰도는 낮습니다**(r=0.691, n=30주). 표본이 30주뿐이라 단독 근거로 쓰지 않습니다. " +
      "얼마나 줄지는 답하지 않습니다 — 계수를 주는 도구가 없어 곱셈으로 만든 수치는 역추적되지 않습니다.",
    premise_correction: { corrected: false },
    used_edges: [
      {
        edge_id: "gu_reviews__new_patients",
        from: "gu_reviews",
        to: "new_patients",
        verdict: "채택",
        sign: "+",
        lag: "2w",
        lag_days: 14,
        confidence: "낮음",
        role: "유기 신호 → 신환 유입",
      },
    ],
    citations: [
      {
        claim: "강남언니 리뷰 최근 주 1건",
        value: 1,
        metric: "gu_reviews",
        grain: "weekly",
        period: { start: "2026-08-24", end: "2026-08-30" },
        row_count: 1,
        source: { tool: "query_kpi", table: "gold_kpi_weekly", column: "gu_reviews" },
      },
      {
        claim: "엣지 근거 r=0.691 (n=30)",
        value: 0.691,
        metric: "gu_reviews",
        grain: "weekly",
        period: { start: "2026-01-07", end: "2026-08-30" },
        row_count: 30,
        source: { tool: "trace_ontology", table: "ontology_edges", column: "evidence" },
      },
    ],
    followups: ["강남언니 리뷰는 언제부터 줄었어?", "신환 수 추이를 보여줘"],
    unknowns: [],
  };

  return {
    outcome: "done",
    result,
    steps: [
      step("trace_ontology", "from=gu_reviews", 460),
      step("query_kpi", "gu_reviews · new_patients · weekly", 390),
    ],
    partials: [
      "강남언니 리뷰와 신환 사이의 엣지를 확인하겠습니다.",
      "같은 방향으로 움직이는 채택 엣지입니다 — 시차 2주, 신뢰도 낮음입니다.",
    ],
  };
}

/** D. 답할 수 없음 — 미관측 노드. */
function patternUnknown(): Plan {
  const result: AnswerResult = {
    answer:
      "외국인 매출 **비중**은 답할 수 있습니다 — 최근 기준 **57.0%** 입니다(`foreign_sales_share`).\n\n" +
      "하지만 **유입 채널은 관측되지 않습니다.** 원천에 채널 필드가 없습니다. " +
      "대리 지표로 외국인 추정 신환 수를 볼 수는 있지만, 그것이 채널을 말해 주지는 않습니다. 추측으로 채우지 않겠습니다.",
    premise_correction: { corrected: false },
    used_edges: [],
    citations: [
      {
        claim: "외국인 매출 비중 57.0%",
        value: 0.57,
        metric: "foreign_sales_share",
        grain: "daily",
        period: { start: "2026-08-24", end: "2026-08-30" },
        row_count: 7,
        source: { tool: "query_kpi", table: "gold_kpi_daily", column: "foreign_sales_share" },
      },
    ],
    followups: ["외국인 추정 신환 수는 어떻게 움직였어?"],
    unknowns: [
      {
        topic: "외국인 유입 채널",
        reason: "미관측 노드 — 채널 기록이 데이터에 없다. 매출 57%가 걸린 경로가 그래프에서 물음표로 남아 있다.",
      },
    ],
  };

  return {
    outcome: "done",
    result,
    steps: [
      step("query_kpi", "foreign_sales_share · daily", 340),
      step("trace_ontology", "target=new_patients_foreign_est", 480),
    ],
    partials: [
      "외국인 매출 관련 지표를 확인하겠습니다.",
      "비중은 답할 수 있지만 유입 채널 노드는 미관측입니다.",
    ],
  };
}

/** 현황 질문 — 온톨로지를 타지 않는다. SPEC-005 R-1 실측값. */
function patternStatus(): Plan {
  const weeks = [
    { week: "2026-08-03", rate: 0.053, claim: "5.3% (54/958)" },
    { week: "2026-08-10", rate: 0.048, claim: "4.8% (46/921)" },
    { week: "2026-08-17", rate: 0.052, claim: "5.2% (53/961)" },
    { week: "2026-08-24", rate: 0.05, claim: "5.0% (56/1,066)" },
  ];

  const result: AnswerResult = {
    answer:
      "최근 4주 노쇼율은 **5.3% → 4.8% → 5.2% → 5.0%** 로 좁은 폭에서 움직였습니다. 네 주 모두 상태는 **양호**입니다 " +
      "(주의 7.14% · 경고 8.7% 경계).\n\n" +
      "계산식은 `노쇼율 = 부도 ÷ (내원 + 부도)` 이고 **취소는 분모에서 제외**합니다 — 취소는 「안 온 것」이 아니라 「예약을 무른 것」이기 때문입니다.",
    premise_correction: { corrected: false },
    used_edges: [],
    citations: weeks.map((w) => ({
      claim: `${w.week} 주 노쇼율 ${w.claim}`,
      value: w.rate,
      metric: "noshow_rate",
      grain: "weekly",
      period: { start: w.week, end: w.week },
      row_count: 1,
      source: { tool: "query_kpi", table: "gold_kpi_weekly", column: "noshow_rate" },
    })),
    followups: ["부도 수는 어떻게 움직였어?", "노쇼율 계산식의 게이트를 보여줘"],
    unknowns: [],
  };

  return {
    outcome: "done",
    result,
    steps: [
      step("query_kpi", "noshow_rate · noshows · visits · weekly", 410),
      step("get_definition", "noshow_rate", 180),
    ],
    partials: [
      "골드 주별 View 에서 노쇼율을 꺼내겠습니다.",
      "네 주 값을 모았습니다. 계산식과 상태 경계를 함께 확인합니다.",
    ],
  };
}

/** 드릴다운 — SPEC-005 R-3. 행은 마스킹 뷰 산출 그대로다. */
function patternDrilldown(): Plan {
  const filters = [
    { field: "visitStatus", op: "eq", value: "취소" },
    { field: "resvDate", op: "between", value: ["2026-08-01", "2026-08-31"] },
  ];
  const rows = mockLayerRows("bronze", "vegas_reservations", { limit: 20, offset: 0, filters });

  const result: AnswerResult = {
    answer:
      "8월 취소 예약 원본입니다. **마스킹 뷰**(`v_bronze_vegas_reservations`)를 지나 나온 행이라 " +
      "이름은 `김○○`, 전화는 `010-****-1234`, 생년월일은 `1990-**-**` 형태로만 보입니다. 원값을 여는 경로는 없습니다.",
    premise_correction: { corrected: false },
    used_edges: [],
    citations: [
      {
        claim: `8월 취소 ${rows ? rows.total.toLocaleString("ko-KR") : 0}건`,
        value: rows?.total ?? 0,
        metric: "cancels",
        grain: "daily",
        period: { start: "2026-08-01", end: "2026-08-31" },
        row_count: rows?.total ?? 0,
        source: { tool: "query_layer", table: "v_bronze_vegas_reservations", column: "visitStatus" },
      },
    ],
    drilldown: rows
      ? {
          layer: "bronze",
          table: "vegas_reservations",
          view: rows.view,
          filters,
          columns: rows.columns,
          masked_fields: rows.masked_fields,
          rows: rows.rows,
          total: rows.total,
        }
      : null,
    followups: ["취소가 몰린 날짜가 있어?", "실버에서는 이 행들이 어떻게 보여?"],
    unknowns: [],
  };

  return {
    outcome: "done",
    result,
    steps: [
      step("query_layer", "bronze · vegas_reservations · 취소 · 2026-08", 720),
      step("query_kpi", "cancels · daily · 2026-08", 300),
    ],
    partials: [
      "브론즈 마스킹 뷰에서 8월 취소 행을 가져오겠습니다.",
      "20행을 받았습니다. 마스킹 표기를 확인합니다.",
    ],
  };
}

function planFailure(outcome: Outcome): Plan {
  return {
    outcome,
    result: null,
    steps: [
      step("query_kpi", "sales_total · monthly", 430),
      step("trace_ontology", "확정 엣지만", 900),
    ],
    partials: ["질문의 전제부터 확인하겠습니다.", "확정 엣지를 되짚는 중입니다."],
  };
}

function buildPlan(question: string): Plan {
  const q = question.replace(/\s/g, "");
  if (q.includes("타임아웃") || q.includes("시간초과")) return planFailure("timeout");
  if (q.includes("실패")) return planFailure("failed");
  if (q.includes("원본") || q.includes("드릴다운")) return patternDrilldown();
  if (q.includes("외국인")) return patternUnknown();
  if (q.includes("리뷰") && q.includes("신환")) return patternDirection();
  if (q.includes("신환") && q.includes("매출")) return patternRejected();
  if (q.includes("매출")) return patternPremise();
  if (q.includes("리뷰")) return patternDirection();
  return patternStatus();
}

/* ─────────────────────────── 상태 전이 ─────────────────────────── */

function materialize(stored: StoredMessage, now: number): ChatMessage {
  if (stored.role === "user" || !stored.plan || stored.startedAt === undefined) {
    return {
      id: stored.id,
      role: stored.role,
      status: "done",
      content: stored.content,
      steps: [],
      created_at: stored.createdAt,
    };
  }

  const plan = stored.plan;
  const elapsed = now - stored.startedAt;
  const revealed = Math.min(Math.floor(elapsed / STEP_INTERVAL_MS), plan.steps.length);
  const finished = elapsed >= plan.steps.length * STEP_INTERVAL_MS + TAIL_MS;

  if (!finished) {
    return {
      id: stored.id,
      role: "assistant",
      status: "pending",
      content: plan.partials.slice(0, revealed).join("\n\n"),
      steps: plan.steps.slice(0, revealed).map((s, index) => ({
        ...s,
        // 마지막으로 드러난 단계는 아직 진행 중이라 소요를 싣지 않는다.
        duration_ms: index < revealed - 1 || revealed === plan.steps.length ? s.duration_ms : null,
      })),
      created_at: stored.createdAt,
    };
  }

  if (plan.outcome === "done") {
    return {
      id: stored.id,
      role: "assistant",
      status: "done",
      content: plan.result?.answer ?? "",
      steps: plan.steps,
      result: plan.result,
      created_at: stored.createdAt,
    };
  }

  return {
    id: stored.id,
    role: "assistant",
    status: "failed",
    content: plan.partials.join("\n\n"),
    steps: plan.steps,
    error_code: plan.outcome === "timeout" ? "AI_TIMEOUT" : "AI_FAILED",
    created_at: stored.createdAt,
  };
}

function snapshot(stored: StoredConversation): ConversationResponse {
  const now = Date.now();
  return {
    conversation: stored.conversation,
    messages: stored.messages.map((m) => materialize(m, now)),
  };
}

function validate(question: string): string {
  const trimmed = question.trim();
  if (trimmed.length === 0) throw new OntologyApiError("EMPTY_QUESTION", 422);
  if (trimmed.length > 1000) throw new OntologyApiError("QUESTION_TOO_LONG", 422);
  return trimmed;
}

function appendTurn(stored: StoredConversation, question: string): void {
  const now = new Date().toISOString();
  stored.messages.push({ id: nextId("m"), role: "user", content: question, createdAt: now });
  stored.messages.push({
    id: nextId("m"),
    role: "assistant",
    content: "",
    createdAt: now,
    plan: buildPlan(question),
    startedAt: Date.now(),
  });
  stored.conversation.last_message_at = now;
}

function hasPending(stored: StoredConversation): boolean {
  const now = Date.now();
  return stored.messages.some((m) => materialize(m, now).status === "pending");
}

export function mockCreateConversation(question: string): ConversationResponse {
  const trimmed = validate(question);
  const id = nextId("c");
  const now = new Date().toISOString();
  const stored: StoredConversation = {
    conversation: {
      id,
      title: trimmed.slice(0, 40),
      created_at: now,
      last_message_at: now,
    },
    messages: [],
  };
  appendTurn(stored, trimmed);
  STORE.set(id, stored);
  return snapshot(stored);
}

export function mockGetConversation(id: string): ConversationResponse {
  const stored = STORE.get(id);
  if (!stored) throw new OntologyApiError("NOT_FOUND", 404);
  return snapshot(stored);
}

export function mockPostMessage(id: string, question: string): ConversationResponse {
  const stored = STORE.get(id);
  if (!stored) throw new OntologyApiError("NOT_FOUND", 404);
  const trimmed = validate(question);
  if (hasPending(stored)) throw new OntologyApiError("CONVERSATION_BUSY", 409);
  appendTurn(stored, trimmed);
  return snapshot(stored);
}

/** 재시도는 **재제출**이다 — 새 줄을 만들지 않고 같은 메시지를 되살린다. */
export function mockRetry(id: string, messageId: string): ConversationResponse {
  const stored = STORE.get(id);
  if (!stored) throw new OntologyApiError("NOT_FOUND", 404);
  const target = stored.messages.find((m) => m.id === messageId);
  if (!target || !target.plan) throw new OntologyApiError("NOT_FOUND", 404);

  const askedIndex = stored.messages.indexOf(target) - 1;
  const question = stored.messages[askedIndex]?.content ?? "";
  // 재시도는 성공 경로로 돌린다 — 실패 재현이 필요하면 질문을 다시 보내면 된다.
  const retried = buildPlan(question.replace(/실패|타임아웃|시간\s*초과/g, ""));
  target.plan = retried;
  target.startedAt = Date.now();
  return snapshot(stored);
}
