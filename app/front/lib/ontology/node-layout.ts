/**
 * 그래프 좌표 자산 — **확정 `node_id`(snake_case)로 키잉한다**.
 *
 * SoT: SPEC-001 §4 「`node_id` 25종」 표 + 디자인 `data/nodes.json`(좌표 배정본).
 * viewBox `0 0 1130 560`, 5열 레이어 배치(x = 95 · 355 · 625 · 895 · 1055).
 *
 * 화면이 자체 id 체계를 두고 매핑 표를 손으로 유지하지 않는다 — 매핑이 어긋나면 노드
 * 하나가 조용히 사라진다(SPEC-004 §4). 좌표가 없는 노드가 응답에 있으면
 * `missingCoords()` 로 **드러낸다**(AC-10).
 */

export interface NodeCoord {
  x: number;
  y: number;
  /** 매출은 그래프의 종착 노드라 시각 강조를 준다(디자인 03). */
  emphasis?: boolean;
}

export const NODE_COORDS: Readonly<Record<string, NodeCoord>> = {
  weekday: { x: 95, y: 60 },
  season: { x: 95, y: 145 },
  holiday: { x: 95, y: 230 },
  promo_event: { x: 95, y: 320 },
  discount_rate: { x: 95, y: 480 },
  naver_reviews: { x: 355, y: 90 },
  gu_reviews: { x: 355, y: 150 },
  new_patients_domestic: { x: 355, y: 210 },
  reservations: { x: 355, y: 270 },
  cancels: { x: 355, y: 330 },
  noshows: { x: 355, y: 390 },
  visits: { x: 355, y: 460 },
  cancel_rate: { x: 625, y: 130 },
  noshow_rate: { x: 625, y: 190 },
  new_patients: { x: 625, y: 250 },
  revisits: { x: 625, y: 310 },
  payment_visits: { x: 625, y: 370 },
  new_patients_foreign_est: { x: 625, y: 430 },
  new_churns: { x: 625, y: 490 },
  avg_ticket: { x: 895, y: 180 },
  sales_total: { x: 895, y: 250, emphasis: true },
  retention_rate_60d: { x: 895, y: 330 },
  foreign_sales_share: { x: 895, y: 410 },
  sales_foreign_est: { x: 895, y: 490 },
  foreign_inflow_channel: { x: 1055, y: 480 },
};

export const GRAPH_VIEWBOX = { width: 1130, height: 560 } as const;

/** 좌표 자산이 25행 전건인지 — 렌더 전 자체 점검용. */
export const COORD_COUNT = Object.keys(NODE_COORDS).length;

/**
 * 응답 노드 중 좌표가 없는 것을 돌려준다. 호출부는 **조용히 빼지 말고** 화면에
 * 드러내야 한다(SPEC-004 AC-10).
 */
export function missingCoords(nodeIds: string[]): string[] {
  return nodeIds.filter((id) => !(id in NODE_COORDS));
}
