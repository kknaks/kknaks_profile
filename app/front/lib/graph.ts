/**
 * 지식 그래프 공유 시각 규칙 (SPEC-005 §5) — 전역(WORK-008)·로컬(WORK-009) 뷰 공용.
 *
 * 주의: node `type`은 BE `/api/graph` 실응답 기준으로 다룬다. work-008/spec-005 문서가
 * 적은 `reference|permanent|post|product|idea`는 stale — 실데이터(2026-06-30 라이브 검증)는
 * `reference, baseline, decision, spec, work, release, runbook, bugfix` (notes=reference,
 * 나머지=products 문서). 타입 집합은 닫혀있지 않다고 가정하고 fallback·데이터 기반 범례로 처리.
 */

import type { GraphNode, GraphNodeType } from "./types";

// 알려진 타입 색 (oklch — 코드베이스 canvas fillStyle은 oklch 지원).
export const TYPE_COLOR: Record<string, string> = {
  reference: "oklch(0.72 0.13 240)", // notes — blue
  spec: "oklch(0.78 0.14 145)", // green
  work: "oklch(0.82 0.13 80)", // gold
  decision: "oklch(0.70 0.16 320)", // magenta
  baseline: "oklch(0.76 0.15 50)", // orange
  release: "oklch(0.78 0.12 195)", // cyan
  runbook: "oklch(0.68 0.15 285)", // purple
  bugfix: "oklch(0.66 0.18 25)", // red
};

export const FALLBACK_COLOR = "oklch(0.70 0.02 250)"; // 미지 타입 — 회색

// 범례 표시 순서(알려진 타입 우선). 데이터에 없는 타입은 범례에서 제외(presentTypes).
export const KNOWN_TYPE_ORDER = [
  "reference",
  "spec",
  "work",
  "decision",
  "baseline",
  "release",
  "runbook",
  "bugfix",
];

// `/api/notes/{id}` 상세를 가진 타입 = notes vault(reference)만. 나머지(products)는 404 → 정식 이동 후속.
export const NOTE_TYPES = new Set<string>(["reference"]);

// 링크 색 (hover 무관 base). lineage=진하게, assoc=연하게.
export const LINK_COLOR_LINEAGE = "rgba(255,255,255,0.22)";
export const LINK_COLOR_ASSOC = "rgba(255,255,255,0.1)";

// react-force-graph는 첫 렌더 후 link.source/target을 string id → node 객체로 변형한다.
export const endId = (v: unknown): string =>
  typeof v === "object" && v !== null && "id" in v
    ? String((v as { id: string | number }).id)
    : String(v);

// 노드 색 — type 매핑 + archived(투명도↓) + dimmed(포커스 시 비이웃) 합성.
export function nodeColorFor(
  type: string,
  opts?: { archived?: boolean; dimmed?: boolean },
): string {
  const base = TYPE_COLOR[type] ?? FALLBACK_COLOR;
  let alpha = opts?.archived ? 0.3 : 1;
  if (opts?.dimmed) alpha = Math.min(alpha, 0.12);
  if (alpha >= 1) return base;
  // "oklch(L C H)" → "oklch(L C H / a)"
  return `${base.slice(0, -1)} / ${alpha})`;
}

// lineage → 화살표 길이, assoc → 0 (무방향).
export const arrowLengthFor = (type?: string): number =>
  type === "lineage" ? 3 : 0;

// 데이터에 실제 등장하는 타입만 범례용으로 추출(알려진 순서 우선, 미지 타입은 뒤에).
export function presentTypes(
  nodes: GraphNode[],
): { type: GraphNodeType; count: number }[] {
  const counts = new Map<string, number>();
  for (const n of nodes) counts.set(n.type, (counts.get(n.type) ?? 0) + 1);
  const known = KNOWN_TYPE_ORDER.filter((t) => counts.has(t));
  const extra = [...counts.keys()]
    .filter((t) => !KNOWN_TYPE_ORDER.includes(t))
    .sort();
  return [...known, ...extra].map((type) => ({
    type,
    count: counts.get(type) ?? 0,
  }));
}
