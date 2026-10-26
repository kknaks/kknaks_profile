// 3D 앵커(SPEC §3) — React·three 없는 순수 함수. 단위 테스트 대상.
import type { AreaKey } from '@/domain/areas';

export type Vec3 = [number, number, number];
export interface AnchorPoint {
  key: AreaKey;
  p: Vec3;
  n: Vec3;
  /** 찍은 자리의 텍스처 UV(three 관례: flipY 기본 → 이미지 px = (u·W, (1−v)·H)) — 부위 확대 사진용 */
  uv?: [number, number];
}
export interface AnchorFile {
  meshBytes: number;
  points: readonly { key: string; p: readonly number[]; n: readonly number[]; uv?: readonly number[] }[];
}

/** §3-3 메시 가드 — 매니페스트 메시와 앵커를 찍은 메시가 같을 때만 */
export function anchorsUsable(manifest: { mesh: { bytes: number } } | null | undefined, anchors: AnchorFile): boolean {
  return !!manifest && manifest.mesh.bytes === anchors.meshBytes && anchors.points.length > 0;
}

/** 찍기 도구 — 개발 서버에서 `?anchors=edit` 일 때만(W-5) */
export function anchorEditEnabled(nodeEnv: string | undefined, search: string): boolean {
  if (nodeEnv === 'production') return false;
  return new URLSearchParams(search).get('anchors') === 'edit';
}

/** §3-5 뒷면 — facing ≤ 0.10 숨김, 0.10–0.30 선형, 이상 1 */
export function facingOpacity(facing: number): number {
  if (facing <= 0.1) return 0;
  if (facing >= 0.3) return 1;
  return (facing - 0.1) / 0.2;
}

/** §3-4 지시선 꺾은선 — 점 → 무릎(카드 끝점에서 얼굴 쪽으로 32px) → 카드 끝점(W-7) */
export const KNEE_PX = 32;
/**
 * route 'knee' = 무릎에서 점으로 비스듬히(기본).
 * route 'top' = 맨 위 카드(L1·R1)용(2루프 W-7) — 카드 높이에서 얼굴 위 빈 곳을 가로로 지나 점 바로 위에서 수직으로 내려간다.
 *   얼굴(이마·눈썹)을 대각선으로 가로지르지 않는다. 점이 무릎보다 카드 쪽에 있으면(크게 돌린 경우) 'knee' 로 돌아간다.
 */
export function leaderPoints(dot: [number, number], end: [number, number], side: 'left' | 'right', route: 'knee' | 'top' = 'knee'): [number, number][] {
  const dir = side === 'left' ? 1 : -1;
  const knee: [number, number] = [end[0] + dir * KNEE_PX, end[1]];
  if (route === 'top' && (dot[0] - knee[0]) * dir > 0) return [dot, [dot[0], end[1]], end];
  return [dot, knee, end];
}

type P = [number, number];
function orient(a: P, b: P, c: P) {
  return Math.sign((b[0] - a[0]) * (c[1] - a[1]) - (b[1] - a[1]) * (c[0] - a[0]));
}
/** 두 선분이 끝점 공유 없이 엇갈리는가 */
export function segmentsCross(a: P, b: P, c: P, d: P): boolean {
  const o1 = orient(a, b, c), o2 = orient(a, b, d), o3 = orient(c, d, a), o4 = orient(c, d, b);
  return o1 * o2 < 0 && o3 * o4 < 0;
}
/** 꺾은선 두 개가 엇갈리는가(R-12) */
export function polylinesCross(p: P[], q: P[]): boolean {
  for (let i = 0; i < p.length - 1; i++) for (let j = 0; j < q.length - 1; j++) if (segmentsCross(p[i], p[i + 1], q[j], q[j + 1])) return true;
  return false;
}

const f4 = (v: readonly number[]) => `[${v.map((x) => x.toFixed(4)).join(', ')}]`;
/** [복사] 본문 — src/data/face-anchors.ts 전체 */
export function anchorFileSource(meshBytes: number, points: AnchorPoint[]): string {
  const lines = points.map((a) => `    { key: '${a.key}', p: ${f4(a.p)}, n: ${f4(a.n)}${a.uv ? `, uv: ${f4(a.uv)}` : ''} },`);
  return [
    '// src/data/face-anchors.ts — 찍기 도구(/screen?anchors=edit) 산출물. 이 고객 메시 기준 고정값.',
    'export const FACE_ANCHORS = {',
    `  meshBytes: ${meshBytes}, // public/m3d/manifest.json mesh.bytes — 다른 메시면 점을 안 그린다`,
    '  points: [',
    ...lines,
    '  ] as { key: string; p: [number, number, number]; n: [number, number, number]; uv?: [number, number] }[],',
    '} as const;',
    '',
  ].join('\n');
}
