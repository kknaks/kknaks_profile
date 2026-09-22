/**
 * mock — `/api/forecast`.
 *
 * SPEC-003 §4 「예보」의 응답 예시를 그대로 옮겼다 — 수치·신뢰도·`lag` 는 기록 07
 * 정본값이다(취소율→예약 `0d`·중간·r=−0.583, 강남언니→신환 `2w`/14·낮음·r=0.691 n=30).
 * **`title`·`message` 는 서버가 만든다** — 화면이 카피를 짓지 않는다(SPEC-004 U-7).
 */

import type { ForecastResponse } from "../types";
import { MOCK_AS_OF } from "./kpi";

export function mockForecast(): ForecastResponse {
  return {
    as_of: MOCK_AS_OF,
    forecasts: [
      {
        rule: "취소율 → 예약",
        title: "예약 위험",
        message:
          "취소율이 경고 구간에 머물고 있습니다. 채택 엣지 「취소율 → 예약 수 (−)」 기준으로 예약 수 하락이 예상됩니다.",
        edge: {
          edge_id: "cancel_rate__reservations",
          from: "cancel_rate",
          to: "reservations",
          verdict: "채택",
          sign: "−",
          lag: "0d",
          lag_days: 0,
          confidence: "중간",
          evidence: "r=−0.583 · Granger 방향 분리(취소율→예약만 p<0.001)",
        },
        trigger: "취소율이 경고 구간에 머무름",
        target: "reservations",
        horizon: "0d",
        risk: "관찰",
        evidence: [
          {
            metric: "cancel_rate",
            value: 0.355,
            period: { start: "2026-08-01", end: "2026-08-30" },
          },
        ],
      },
      {
        rule: "강남언니 리뷰 → 신환",
        title: "신환 위험",
        message:
          "강남언니 유기 리뷰가 8월 거의 0입니다. 「리뷰 수 → 신환 수 (+)」 엣지 기준으로 2주 뒤 신환 유입 감소가 예상됩니다.",
        edge: {
          edge_id: "gu_reviews__new_patients",
          from: "gu_reviews",
          to: "new_patients",
          verdict: "채택",
          sign: "+",
          lag: "2w",
          lag_days: 14,
          confidence: "낮음",
          evidence: "r=0.691 · n=30",
        },
        trigger: "유기 리뷰가 8월 거의 0",
        target: "new_patients",
        horizon: "14d",
        risk: "알림",
        note: "신뢰도 낮음(표본 30주) — 단독 근거로 쓰지 않는다",
      },
    ],
  };
}
