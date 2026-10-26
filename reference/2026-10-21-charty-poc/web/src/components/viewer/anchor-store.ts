// 앵커 6점 · 지시선 SVG 요소 레지스트리 — 매 프레임 React state 를 바꾸지 않으려고 모듈 단위로 둔다(SPEC §3-4).
import { useSyncExternalStore } from 'react';
import { FACE_ANCHORS } from '@/data/face-anchors';
import type { AreaKey } from '@/domain/areas';
import type { AnchorPoint } from './anchors';

let points: AnchorPoint[] = FACE_ANCHORS.points.map((a) => ({
  key: a.key as AreaKey,
  p: [...a.p] as AnchorPoint['p'],
  n: [...a.n] as AnchorPoint['n'],
  uv: a.uv ? ([...a.uv] as [number, number]) : undefined,
}));
const listeners = new Set<() => void>();
const emit = () => listeners.forEach((l) => l());

export const anchorStore = {
  get: () => points,
  set(key: AreaKey, p: AnchorPoint['p'], n: AnchorPoint['n'], uv?: [number, number]) {
    points = [...points.filter((a) => a.key !== key), { key, p, n, uv }];
    emit();
  },
  reset() {
    points = [];
    emit();
  },
  subscribe(l: () => void) {
    listeners.add(l);
    return () => listeners.delete(l);
  },
};

export function useAnchorPoints(): AnchorPoint[] {
  return useSyncExternalStore(anchorStore.subscribe, anchorStore.get, anchorStore.get);
}

/** 지시선 한 줄의 SVG 요소 + 카드 쪽 끝점 + 카드 강조 — LeaderLines 가 채우고 AnchorProjector 가 매 프레임 고친다 */
export interface LeaderSlot {
  g: SVGGElement | null;
  line: SVGPolylineElement | null;
  dot: SVGCircleElement | null;
  endEl: SVGCircleElement | null;
  end: [number, number];
  side: 'left' | 'right';
  /** 맨 위 카드(L1·R1)는 'top'(W-7) */
  route: 'knee' | 'top';
  strong: boolean;
  /** 스무딩된 가림 opacity(0–1) */
  cur: number;
  /** 목표 가림 opacity — data-visible = target > 0(W-7) */
  target: number;
  x: number;
  y: number;
  applied: number;
}
export const leaderSlots = new Map<AreaKey, LeaderSlot>();

/** 찍기 도구에서 고른 카드 */
export const editState = { selected: null as AreaKey | null, enabled: false };
export function setEditSelected(k: AreaKey | null) {
  editState.selected = k;
}
export function setEditEnabled(v: boolean) {
  editState.enabled = v;
}
