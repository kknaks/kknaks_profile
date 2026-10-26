'use client';
// 지시선 SVG 속성은 useFrame 안에서 직접 고친다(매 프레임 React state 를 바꾸지 않는다, SPEC §3-4)

import { useFrame, useThree } from '@react-three/fiber';
import { createRef, useEffect, useMemo } from 'react';
import * as THREE from 'three';
import type { AreaKey } from '@/domain/areas';
import { anchorStore, leaderSlots } from './anchor-store';
import { anchorFileSource, facingOpacity, leaderPoints } from './anchors';
import { FACE_ANCHORS } from '@/data/face-anchors';

/** 얼굴 메시 — 가림 raycast · 찍기 도구가 같이 쓴다 */
export const meshRef = createRef<THREE.Mesh>();

const OCCLUDE_EPS = 0.002; // 2mm
const SMOOTH = 0.25;
// 흐린 카드의 점·선 — 0.3 은 어두운 바탕에서 사라져 0.5 + 점선(2루프 W-5)
const DIM = 0.5;
const DIM_DASH = '6 4';

const raycaster = new THREE.Raycaster();
(raycaster as THREE.Raycaster & { firstHitOnly?: boolean }).firstHitOnly = true;

/** 캔버스 설계 px → 메시 표면 { p, n } — key 를 주면 그 카드 앵커로 저장(W-4) */
export function pickAt(camera: THREE.Camera, el: HTMLElement, cx: number, cy: number, key?: AreaKey) {
  const mesh = meshRef.current;
  if (!mesh) return null;
  const ndc = new THREE.Vector2((cx / el.offsetWidth) * 2 - 1, 1 - (cy / el.offsetHeight) * 2);
  raycaster.far = Infinity;
  raycaster.setFromCamera(ndc, camera);
  const hit = raycaster.intersectObject(mesh, false)[0];
  if (!hit?.face) return null;
  const n = hit.face.normal.clone().normalize();
  const out = {
    p: [hit.point.x, hit.point.y, hit.point.z] as [number, number, number],
    n: [n.x, n.y, n.z] as [number, number, number],
    uv: hit.uv ? ([hit.uv.x, hit.uv.y] as [number, number]) : undefined,
  };
  if (key) anchorStore.set(key, out.p, out.n, out.uv);
  return out;
}

/** 저장된 앵커 자리의 UV — 점 바깥 1cm 에서 법선 반대로 쏴 첫 교차의 uv(카메라와 무관) */
export function uvAtAnchor(key: AreaKey): [number, number] | null {
  const mesh = meshRef.current;
  const a = anchorStore.get().find((x) => x.key === key);
  if (!mesh || !a) return null;
  const n = new THREE.Vector3(...a.n).normalize();
  const origin = new THREE.Vector3(...a.p).addScaledVector(n, 0.01);
  raycaster.far = 0.02;
  raycaster.set(origin, n.negate());
  const hit = raycaster.intersectObject(mesh, false)[0];
  return hit?.uv ? [hit.uv.x, hit.uv.y] : null;
}

/** 앵커 6점을 매 프레임 화면에 투영하고 지시선 SVG 를 직접 고친다(SPEC §3-4 · §3-5) */
export function AnchorProjector({ offset }: { offset: [number, number] }) {
  const camera = useThree((s) => s.camera);
  const gl = useThree((s) => s.gl);
  const tmp = useMemo(() => ({ p: new THREE.Vector3(), n: new THREE.Vector3(), to: new THREE.Vector3(), ndc: new THREE.Vector3() }), []);
  const ms = useMemo(() => ({ list: [] as number[] }), []);

  useEffect(() => {
    window.__faceViewer = Object.assign(window.__faceViewer ?? ({ applied: null } as unknown as NonNullable<Window['__faceViewer']>), {
      anchors: () =>
        [...leaderSlots.entries()].map(([key, s]) => ({ key, x: s.x, y: s.y, visible: s.target > 0, opacity: s.applied, occlusion: s.cur })),
      anchor3d: (key: AreaKey) => {
        const a = anchorStore.get().find((x) => x.key === key);
        return (a ? [...a.p] : [NaN, NaN, NaN]) as [number, number, number];
      },
      anchorFile: () => anchorFileSource(FACE_ANCHORS.meshBytes, anchorStore.get()),
      anchorUv: (key: AreaKey) => uvAtAnchor(key),
      anchorMs: () => (ms.list.length ? ms.list.reduce((a, b) => a + b, 0) / ms.list.length : NaN),
      canvasSize: () => [gl.domElement.offsetWidth, gl.domElement.offsetHeight] as [number, number],
    });
  }, [gl, ms]);

  useFrame(() => {
    // OrbitControls(priority −1)가 이번 프레임에 옮긴 카메라 행렬로 투영한다 — 없으면 한 프레임 늦다(F-1)
    camera.updateMatrixWorld();
    const t0 = performance.now();
    const mesh = meshRef.current;
    const W = gl.domElement.offsetWidth;
    const H = gl.domElement.offsetHeight;
    const cam = camera.position;
    const points = anchorStore.get();
    for (const [key, s] of leaderSlots) {
      const a = points.find((x) => x.key === key);
      let target = 0;
      if (a) {
        tmp.p.set(a.p[0], a.p[1], a.p[2]);
        tmp.ndc.copy(tmp.p).project(camera);
        s.x = ((tmp.ndc.x + 1) / 2) * W + offset[0];
        s.y = ((1 - tmp.ndc.y) / 2) * H + offset[1];
        tmp.to.copy(cam).sub(tmp.p);
        const dist = tmp.to.length();
        tmp.to.divideScalar(dist);
        target = facingOpacity(tmp.n.set(a.n[0], a.n[1], a.n[2]).dot(tmp.to));
        if (Math.abs(tmp.ndc.x) > 1 || Math.abs(tmp.ndc.y) > 1) target = 0;
        if (target > 0 && mesh) {
          // 카메라 → 점 사이에 다른 면(코·볼)이 있으면 가림
          raycaster.set(cam, tmp.to.negate());
          raycaster.far = dist;
          const hit = raycaster.intersectObject(mesh, false)[0];
          if (hit && hit.distance < dist - OCCLUDE_EPS) target = 0;
        }
      }
      s.target = target;
      s.cur += (target - s.cur) * SMOOTH;
      if (Math.abs(target - s.cur) < 0.005) s.cur = target;
      s.applied = s.cur * (s.strong ? 1 : DIM);
      if (s.g) {
        s.g.setAttribute('opacity', s.applied.toFixed(3));
        s.g.setAttribute('data-visible', String(target > 0));
      }
      if (a && s.dot && s.line) {
        s.dot.setAttribute('cx', s.x.toFixed(1));
        s.dot.setAttribute('cy', s.y.toFixed(1));
        s.line.setAttribute('stroke-dasharray', s.strong ? 'none' : DIM_DASH);
        s.line.setAttribute('points', leaderPoints([s.x, s.y], s.end, s.side, s.route).map((q) => q.map((v) => v.toFixed(1)).join(',')).join(' '));
      }
    }
    ms.list.push(performance.now() - t0);
    if (ms.list.length > 120) ms.list.shift();
  });

  return null;
}
