/**
 * mock — `/api/graph`.
 *
 * 노드 25 · 엣지 27 은 디자인 `data/nodes.json` · `data/edges.json`(= `ontology_*` 정본
 * 재키잉본)에서 그대로 옮겼다. 라벨·좌표 키는 SPEC-001 §4 의 확정 `node_id` 다.
 *
 * 화면과 픽스처가 다른 상태를 보지 않도록 **노드 상태는 `mock/kpi.ts` 의 카드 표에서
 * 파생**시킨다 — SPEC-003 §4 「노드 상태색 기준은 `/api/kpi/cards` 와 같은 규칙」.
 *
 * `counts` 도 엣지 배열에서 파생시킨다. 숫자를 손으로 적으면 데이터와 어긋난다.
 */

import type { Confidence, EdgeKind, GraphEdge, GraphNode, GraphResponse, NodeType, Verdict } from "../types";
import { mockNodeStates } from "./kpi";

interface NodeSeed {
  node_id: string;
  name: string;
  node_type: NodeType;
  controllable: boolean;
  observed: boolean;
  /** 「원본 데이터 보기」 목적지의 출처. 테이블이 없는 노드는 null 이다. */
  source: string | null;
}

const NODES: NodeSeed[] = [
  { node_id: "weekday", name: "요일", node_type: "exogenous", controllable: false, observed: true, source: null },
  { node_id: "season", name: "계절(월)", node_type: "exogenous", controllable: false, observed: true, source: null },
  { node_id: "holiday", name: "연휴·공휴일", node_type: "exogenous", controllable: false, observed: true, source: null },
  { node_id: "promo_event", name: "프로모션 이벤트", node_type: "intervention", controllable: true, observed: true, source: "gold_promo_calendar" },
  { node_id: "discount_rate", name: "프로모션 평균 할인율", node_type: "attribute", controllable: true, observed: true, source: "silver_promotions.discount_rate" },
  { node_id: "naver_reviews", name: "네이버 리뷰 수", node_type: "intervention", controllable: true, observed: true, source: "gold_kpi_daily.naver_reviews" },
  { node_id: "gu_reviews", name: "강남언니 리뷰 수", node_type: "organic", controllable: false, observed: true, source: "gold_kpi_weekly.gu_reviews" },
  { node_id: "new_patients_domestic", name: "한국인 신환 수", node_type: "kpi", controllable: false, observed: true, source: "gold_kpi_daily.new_patients_domestic" },
  { node_id: "reservations", name: "예약 수", node_type: "kpi", controllable: false, observed: true, source: "gold_kpi_daily.reservations" },
  { node_id: "cancels", name: "취소 수", node_type: "kpi", controllable: false, observed: true, source: "gold_kpi_daily.cancels" },
  { node_id: "noshows", name: "부도 수", node_type: "kpi", controllable: false, observed: true, source: "gold_kpi_daily.noshows" },
  { node_id: "visits", name: "총 내원 수", node_type: "kpi", controllable: false, observed: true, source: "gold_kpi_daily.visits" },
  { node_id: "cancel_rate", name: "취소율", node_type: "kpi", controllable: false, observed: true, source: "gold_kpi_daily.cancel_rate" },
  { node_id: "noshow_rate", name: "노쇼율", node_type: "kpi", controllable: false, observed: true, source: "gold_kpi_daily.noshow_rate" },
  { node_id: "new_patients", name: "신환 수", node_type: "kpi", controllable: false, observed: true, source: "gold_kpi_daily.new_patients" },
  { node_id: "revisits", name: "재진 수", node_type: "kpi", controllable: false, observed: true, source: "gold_kpi_daily.revisits" },
  { node_id: "payment_visits", name: "결제 내원 수", node_type: "kpi", controllable: false, observed: true, source: "gold_kpi_daily.payment_visits" },
  { node_id: "new_patients_foreign_est", name: "외국인 추정 신환 수", node_type: "kpi", controllable: false, observed: true, source: "gold_kpi_daily.new_patients_foreign_est" },
  { node_id: "new_churns", name: "신규 이탈 수", node_type: "kpi", controllable: false, observed: true, source: "gold_kpi_daily.new_churns" },
  { node_id: "avg_ticket", name: "객단가", node_type: "kpi", controllable: false, observed: true, source: "gold_kpi_daily.avg_ticket" },
  { node_id: "sales_total", name: "매출", node_type: "kpi", controllable: false, observed: true, source: "gold_kpi_daily.sales_total" },
  { node_id: "retention_rate_60d", name: "재방문 전환율(60일)", node_type: "kpi", controllable: false, observed: true, source: "gold_retention_monthly.revisit_rate" },
  { node_id: "foreign_sales_share", name: "외국인 매출 비중", node_type: "kpi", controllable: false, observed: true, source: "gold_kpi_daily.foreign_sales_share" },
  { node_id: "sales_foreign_est", name: "외국인 추정 매출", node_type: "kpi", controllable: false, observed: true, source: "gold_kpi_daily.sales_foreign_est" },
  { node_id: "foreign_inflow_channel", name: "외국인 유입 채널", node_type: "unobserved", controllable: false, observed: false, source: null },
];

interface EdgeSeed {
  from: string;
  to: string;
  verdict: Verdict;
  sign: string;
  lag: string;
  confidence: Confidence | null;
  kind: EdgeKind;
  evidence: string;
  note: string;
}

const EDGES: EdgeSeed[] = [
  { from: "naver_reviews", to: "reservations", verdict: "채택", sign: "+", lag: "0d", confidence: "중간", kind: "causal", evidence: "잔차 r=0.326 n=163 Granger p=0.036", note: "개입 변수(리뷰 확보 캠페인)와 예약의 동행 — 마케팅 활동 지표 엣지" },
  { from: "new_patients", to: "payment_visits", verdict: "채택", sign: "+", lag: "7d", confidence: "높음", kind: "causal", evidence: "잔차 r=0.579 n=227 Granger p=0.088", note: "신환이 약 1주 후 결제 방문(시술 계약)으로 전환 — 최강 후보" },
  { from: "cancel_rate", to: "reservations", verdict: "채택", sign: "−", lag: "0d", confidence: "중간", kind: "causal", evidence: "잔차 r=−0.583 n=235 Granger 방향분리 p<0.001(역방향 p=0.81)", note: "취소율 상승은 예약 경기 하강의 조기 경보 — 재진 취소(33.5%)가 주 원천" },
  { from: "gu_reviews", to: "new_patients", verdict: "채택", sign: "+", lag: "2w", confidence: "낮음", kind: "causal", evidence: "r=0.691 n=30 (유기 신호 — 보조 지위 + 도메인 지식 결합)", note: "리뷰를 보고 예약하는 유입 경로 — 표본 얇아 신뢰도 낮음 명시" },

  { from: "payment_visits", to: "sales_total", verdict: "자동 확정", sign: "0", lag: "", confidence: null, kind: "derivation", evidence: "매출 = 객단가 × 결제 내원", note: "항등식" },
  { from: "avg_ticket", to: "sales_total", verdict: "자동 확정", sign: "0", lag: "", confidence: null, kind: "derivation", evidence: "매출 = 객단가 × 결제 내원", note: "항등식" },
  { from: "new_patients", to: "visits", verdict: "자동 확정", sign: "0", lag: "", confidence: null, kind: "derivation", evidence: "총 내원 = 신환 + 재진", note: "항등식" },
  { from: "revisits", to: "visits", verdict: "자동 확정", sign: "0", lag: "", confidence: null, kind: "derivation", evidence: "총 내원 = 신환 + 재진", note: "항등식" },
  { from: "visits", to: "reservations", verdict: "자동 확정", sign: "0", lag: "", confidence: null, kind: "derivation", evidence: "예약 = 내원 + 취소 + 부도", note: "항등식" },
  { from: "cancels", to: "reservations", verdict: "자동 확정", sign: "0", lag: "", confidence: null, kind: "derivation", evidence: "예약 = 내원 + 취소 + 부도", note: "항등식" },
  { from: "noshows", to: "reservations", verdict: "자동 확정", sign: "0", lag: "", confidence: null, kind: "derivation", evidence: "예약 = 내원 + 취소 + 부도", note: "항등식" },
  { from: "cancels", to: "cancel_rate", verdict: "자동 확정", sign: "0", lag: "", confidence: null, kind: "derivation", evidence: "취소율 = 취소 ÷ 예약", note: "항등식" },
  { from: "noshows", to: "noshow_rate", verdict: "자동 확정", sign: "0", lag: "", confidence: null, kind: "derivation", evidence: "노쇼율 = 부도 ÷ (내원+부도)", note: "항등식" },
  { from: "new_patients_domestic", to: "new_patients", verdict: "자동 확정", sign: "0", lag: "", confidence: null, kind: "derivation", evidence: "신환 = 한국인 신환 + 외국인 추정 신환", note: "분해 항등식 (글로서리 개정 3)" },
  { from: "new_patients_foreign_est", to: "new_patients", verdict: "자동 확정", sign: "0", lag: "", confidence: null, kind: "derivation", evidence: "신환 = 한국인 신환 + 외국인 추정 신환", note: "분해 항등식 (글로서리 개정 3)" },
  { from: "sales_foreign_est", to: "sales_total", verdict: "자동 확정", sign: "0", lag: "", confidence: null, kind: "derivation", evidence: "매출 = 한국인 매출 + 외국인 추정 매출", note: "분해 항등식 (글로서리 개정 3)" },
  { from: "sales_foreign_est", to: "foreign_sales_share", verdict: "자동 확정", sign: "0", lag: "", confidence: null, kind: "derivation", evidence: "외국인 매출 비중 = 외국인 추정 매출 ÷ 매출", note: "정의 (05 개정 4)" },
  { from: "sales_total", to: "foreign_sales_share", verdict: "자동 확정", sign: "0", lag: "", confidence: null, kind: "derivation", evidence: "외국인 매출 비중 = 외국인 추정 매출 ÷ 매출", note: "정의 (05 개정 4)" },

  { from: "weekday", to: "reservations", verdict: "선언", sign: "exo", lag: "", confidence: null, kind: "exogenous", evidence: "요일 잔차 통제로 확인된 주간 리듬", note: "외생 — 나가는 엣지만" },
  { from: "season", to: "new_patients", verdict: "선언", sign: "exo", lag: "", confidence: null, kind: "exogenous", evidence: "1~8월 신환 하락 추세에 계절 혼입 가능", note: "외생 — 나가는 엣지만" },
  { from: "holiday", to: "visits", verdict: "선언", sign: "exo", lag: "", confidence: null, kind: "exogenous", evidence: "설 연휴 결측일 등", note: "외생 — 나가는 엣지만" },

  { from: "new_churns", to: "new_patients", verdict: "보류", sign: "?", lag: "0d", confidence: null, kind: "candidate", evidence: "r=0.323 n=235 — 공통 원인(유입 총량) 의심", note: "동반 관계 소지 — 유입 노드 해명 전까지 미확정" },
  { from: "new_patients_foreign_est", to: "new_patients_domestic", verdict: "보류", sign: "?", lag: "", confidence: null, kind: "candidate", evidence: "일 잔차 r=−0.25(임계 미달) · 월 r=−0.92는 추세 혼입으로 기각 (기록 06 부기)", note: "구축 효과 미확정 — 공통 원인(마케팅 재배분) 후보는 채널 데이터 부재로 검증 불가" },
  { from: "foreign_inflow_channel", to: "new_patients_foreign_est", verdict: "보류", sign: "?", lag: "", confidence: null, kind: "candidate", evidence: "미관측 — 유입 경로 데이터 없음", note: "매출 57%가 걸린 채널이나 데이터 밖 — 채널 기록 수집이 선결 과제" },

  { from: "promo_event", to: "sales_total", verdict: "기각", sign: "", lag: "", confidence: null, kind: "rejected", evidence: "전후 ±14일 변화율 ±6% 이내 (이벤트 23건)", note: "비교 구간 부재(월 단위 연쇄 진행)의 구조적 한계 병기" },
  { from: "discount_rate", to: "sales_total", verdict: "기각", sign: "", lag: "", confidence: null, kind: "rejected", evidence: "스피어만 −0.479 n=23", note: "역인과 의심 — 매출 부진기에 고할인 구성 투입(경영 대응) 독해가 우세" },
  { from: "new_patients", to: "sales_total", verdict: "기각", sign: "", lag: "", confidence: null, kind: "rejected", evidence: "최대 r=0.14 (시차 1~28일)", note: "매출 금액은 시술 구성에 좌우 — 결제 내원 경유 경로(채택 엣지)로 대체" },
];

/** `lag` 는 정본 문자열 원형이고 `lag_days` 를 병기한다 — `2w` → 14, 빈 값 → null. */
function toLagDays(lag: string): number | null {
  if (!lag) return null;
  const week = /^(\d+)w$/.exec(lag);
  if (week) return Number(week[1]) * 7;
  const day = /^(\d+)d$/.exec(lag);
  if (day) return Number(day[1]);
  return null;
}

function buildNodes(): GraphNode[] {
  const states = mockNodeStates();
  return NODES.map((node) => {
    const observedState = states.get(node.node_id);
    return {
      ...node,
      node_state: node.observed ? (observedState?.state ?? "정상") : "미관측",
      alert_days: node.observed ? (observedState?.alertDays ?? 0) : null,
    };
  });
}

function buildEdges(): GraphEdge[] {
  return EDGES.map((edge) => {
    const negative = edge.verdict === "기각" || edge.verdict === "보류";
    return {
      edge_id: `${edge.from}__${edge.to}`,
      from: edge.from,
      to: edge.to,
      sign: edge.sign,
      lag: edge.lag,
      lag_days: toLagDays(edge.lag),
      verdict: edge.verdict,
      kind: edge.kind,
      confidence: edge.confidence,
      evidence: edge.evidence,
      // 정본은 기각·보류 행에 **사유**를 싣는다(SPEC-001 §4). 픽스처에서는 그 행의
      // 설명이 곧 사유라 `reason` 으로 넘기고 `note` 는 비운다 — 같은 문장을 두 번
      // 그리지 않기 위함이고, 실 API 는 두 필드를 각각 채운다.
      note: negative ? null : edge.note,
      reason: negative ? edge.note : null,
      usable_for_causal_claim: !negative,
    };
  });
}

export function mockGraph(): GraphResponse {
  const edges = buildEdges();
  const counts = edges.reduce<Record<string, number>>((acc, edge) => {
    acc[edge.verdict] = (acc[edge.verdict] ?? 0) + 1;
    return acc;
  }, {});
  return { nodes: buildNodes(), edges, counts };
}

/** 노드 라벨 조회 — 칩·인스펙터가 id 대신 이름을 쓰기 위해(디자인 05). */
export function mockNodeLabels(): Record<string, string> {
  return Object.fromEntries(NODES.map((n) => [n.node_id, n.name]));
}
