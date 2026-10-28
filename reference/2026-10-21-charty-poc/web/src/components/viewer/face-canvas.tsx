'use client';
/* eslint-disable react-hooks/immutability -- three.js 재질 uniform 은 useFrame·effect 안에서 직접 바꾸는 것이 r3f 관례다(재렌더 없이 GPU 값만 갱신) */

import { Bvh, OrbitControls } from '@react-three/drei';
import { Canvas, useFrame, useLoader, useThree } from '@react-three/fiber';
import { Suspense, useEffect, useMemo, useRef, useState } from 'react';
import * as THREE from 'three';
import { OBJLoader } from 'three/examples/jsm/loaders/OBJLoader.js';
import type { OrbitControls as OrbitControlsImpl } from 'three-stdlib';
import type { AreaKey } from '@/domain/areas';
import { FILTERS, type FilterKey } from '@/domain/filters';
import { AnchorProjector, meshRef, pickAt } from './anchor-projector';
import { anchorStore, editState } from './anchor-store';
import { createFaceMaterial, prepareTexture } from './face-material';
import { M3D_BASE, type M3dManifest } from './manifest';

const DEG = Math.PI / 180;
// 얼굴이 뷰어 안 두 카드 열 사이(256–784)에 들어오게 0.55 → 0.70(배치 정정)
const HOME = new THREE.Vector3(0, 0, 0.7);
const FADE_MS = 250;
const RESET_MS = 600;

export interface FaceCanvasProps {
  manifest: M3dManifest;
  filter: FilterKey;
  cameraResetAt: number;
  onReady?: () => void;
  onApplied?: (filter: FilterKey) => void;
  /** 점·지시선을 그린다(메시 가드 통과 · 또는 찍기 도구) */
  anchors?: boolean;
  /** 캔버스 원점의 뷰어 패널 좌표 — 지시선 SVG 가 패널 기준이다 */
  panelOffset?: [number, number];
}

declare global {
  interface Window {
    __faceViewer?: {
      azimuthDeg: () => number;
      polarDeg: () => number;
      distance: () => number;
      /** 월드 좌표 → 화면 NDC(−1 왼쪽 … +1 오른쪽). 좌우 반전 확인용 */
      project: (x: number, y: number, z: number) => [number, number];
      applied: FilterKey | null;
      /** 점 6개 — 뷰어 패널 기준 설계 px. opacity = SVG 에 실제 적용한 최종값, occlusion = 가림만(W-7) */
      anchors?: () => { key: AreaKey; x: number; y: number; visible: boolean; opacity: number; occlusion: number }[];
      anchor3d?: (key: AreaKey) => [number, number, number];
      /** 캔버스 설계 px → 메시 표면 { p, n } (찍기 도구 · W-4). key 를 주면 그 카드 앵커로 저장 */
      pickAt?: (cx: number, cy: number, key?: AreaKey) => { p: [number, number, number]; n: [number, number, number]; uv?: [number, number] } | null;
      /** 앵커 자리 UV(법선 raycast) — 부위 확대 사진 · 찍기 도구 */
      anchorUv?: (key: AreaKey) => [number, number] | null;
      /** 찍기 도구 [복사] 본문 */
      anchorFile?: () => string;
      /** AnchorProjector useFrame 1회 평균 ms(W-6) */
      anchorMs?: () => number;
      canvasSize?: () => [number, number];
    };
  }
}

const url = (file: string) => `${M3D_BASE}/${file}`;

function Face({ manifest, filter, onReady, onApplied }: Omit<FaceCanvasProps, 'cameraResetAt'>) {
  const obj = useLoader(OBJLoader, url(manifest.mesh.file));
  const baseTex = useLoader(THREE.TextureLoader, url(manifest.textures.natural.file));
  const gl = useThree((s) => s.gl);
  const maxAniso = gl.capabilities.getMaxAnisotropy();

  const geometry = useMemo(() => {
    let g: THREE.BufferGeometry | null = null;
    obj.traverse((o) => {
      if (!g && (o as THREE.Mesh).isMesh) g = (o as THREE.Mesh).geometry;
    });
    const out = (g as unknown as THREE.BufferGeometry).clone();
    out.computeBoundingBox();
    out.center();
    return out;
  }, [obj]);

  const material = useMemo(() => createFaceMaterial(prepareTexture(baseTex, maxAniso)), [baseTex, maxAniso]);

  // 나머지 텍스처·오버레이는 첫 화면 뒤 백그라운드로 선로딩
  const cache = useRef(new Map<string, THREE.Texture>([['tex:natural', baseTex]]));
  const [loaded, setLoaded] = useState(0);
  useEffect(() => {
    let alive = true;
    const loader = new THREE.TextureLoader();
    const jobs = [
      ...Object.entries(manifest.textures).filter(([k]) => k !== 'natural').map(([k, v]) => [`tex:${k}`, v.file] as const),
      ...Object.entries(manifest.overlays).map(([k, v]) => [`ov:${k}`, v.file] as const),
    ];
    for (const [key, file] of jobs) {
      loader.loadAsync(url(file)).then((t) => {
        if (!alive) return;
        cache.current.set(key, prepareTexture(t, maxAniso));
        setLoaded((n) => n + 1);
      });
    }
    return () => {
      alive = false;
    };
  }, [manifest, maxAniso]);

  const anim = useRef({ mixStart: 0, overlayTarget: 0 });
  useEffect(() => {
    const def = FILTERS[filter];
    const tex = cache.current.get(`tex:${def.texture}`);
    if (!tex) return; // 아직 로딩 중 — 다 오면 이 effect 가 다시 돈다
    const ov = def.overlay ? cache.current.get(`ov:${def.overlay}`) : null;
    if (def.overlay && !ov) return;
    const u = material.uniforms;
    if (u.uBase.value !== tex) {
      u.uBasePrev.value = u.uBase.value;
      u.uBase.value = tex;
      u.uMix.value = 0;
      anim.current.mixStart = performance.now();
    }
    if (ov) {
      u.uOverlay.value = ov;
      // <Canvas linear> 라 sRGB→linear 변환 없이 16진 값을 그대로 넣는다(사진 픽셀과 같은 공간)
      (u.uOverlayColor.value as THREE.Color).setStyle(def.overlayColor ?? '#ffffff', THREE.LinearSRGBColorSpace);
      anim.current.overlayTarget = 1;
    } else {
      anim.current.overlayTarget = 0;
    }
    if (window.__faceViewer) window.__faceViewer.applied = filter;
    onApplied?.(filter);
  }, [filter, loaded, material, onApplied]);

  useFrame((_, dt) => {
    const u = material.uniforms;
    if (u.uMix.value < 1) u.uMix.value = Math.min(1, (performance.now() - anim.current.mixStart) / FADE_MS);
    const target = anim.current.overlayTarget;
    const cur = u.uOverlayOn.value as number;
    if (cur !== target) {
      const step = (dt * 1000) / FADE_MS;
      u.uOverlayOn.value = target > cur ? Math.min(target, cur + step) : Math.max(target, cur - step);
    }
  });

  const readyFired = useRef(false);
  useFrame(() => {
    if (!readyFired.current) {
      readyFired.current = true;
      onReady?.();
    }
  });

  // 찍기 도구 — 드래그(회전)와 클릭을 가르려고 down→up 이동 4px 이하만 찍기로 본다(§3-2)
  const down = useRef<{ x: number; y: number } | null>(null);
  return (
    <Bvh firstHitOnly>
      <mesh
        ref={meshRef}
        geometry={geometry}
        material={material}
        onPointerDown={(e) => {
          if (editState.enabled) down.current = { x: e.nativeEvent.offsetX, y: e.nativeEvent.offsetY };
        }}
        onPointerUp={(e) => {
          const d = down.current;
          down.current = null;
          const key = editState.selected;
          if (!editState.enabled || !d || !key || !e.face) return;
          if (Math.hypot(e.nativeEvent.offsetX - d.x, e.nativeEvent.offsetY - d.y) > 4) return;
          const n = e.face.normal.clone().normalize();
          anchorStore.set(key, [e.point.x, e.point.y, e.point.z], [n.x, n.y, n.z]);
        }}
      />
    </Bvh>
  );
}

function Controls({ resetAt }: { resetAt: number }) {
  const ref = useRef<OrbitControlsImpl>(null);
  const camera = useThree((s) => s.camera);
  const gl = useThree((s) => s.gl);
  const reset = useRef<{ from: THREE.Vector3; t0: number } | null>(null);

  useEffect(() => {
    if (!resetAt) return;
    reset.current = { from: camera.position.clone(), t0: performance.now() };
  }, [resetAt, camera]);

  useEffect(() => {
    // 다른 컴포넌트(AnchorProjector)가 붙인 키를 지우지 않게 덧붙인다(W-10)
    window.__faceViewer = Object.assign(window.__faceViewer ?? ({ applied: null } as unknown as NonNullable<Window['__faceViewer']>), {
      azimuthDeg: () => (ref.current?.getAzimuthalAngle() ?? 0) / DEG,
      polarDeg: () => (ref.current?.getPolarAngle() ?? 0) / DEG,
      distance: () => camera.position.length(),
      project: (x: number, y: number, z: number): [number, number] => {
        const v = new THREE.Vector3(x, y, z).project(camera);
        return [v.x, v.y];
      },
      pickAt: (cx: number, cy: number, key?: AreaKey) => pickAt(camera, gl.domElement, cx, cy, key),
    });
  }, [camera, gl]);

  useFrame(() => {
    const r = reset.current;
    const c = ref.current;
    if (!r || !c) return;
    const k = Math.min(1, (performance.now() - r.t0) / RESET_MS);
    const e = 1 - Math.pow(1 - k, 3);
    c.enableDamping = false;
    camera.position.lerpVectors(r.from, HOME, e);
    c.target.set(0, 0, 0);
    c.update();
    if (k >= 1) {
      reset.current = null;
      c.enableDamping = true;
    }
  });

  return (
    <OrbitControls
      ref={ref}
      makeDefault
      enablePan={false}
      enableDamping
      minDistance={0.28}
      maxDistance={0.9}
      minAzimuthAngle={-75 * DEG}
      maxAzimuthAngle={75 * DEG}
      minPolarAngle={60 * DEG}
      maxPolarAngle={120 * DEG}
      target={[0, 0, 0]}
    />
  );
}

export default function FaceCanvas({ manifest, filter, cameraResetAt, onReady, onApplied, anchors, panelOffset = [0, 0] }: FaceCanvasProps) {
  const [localReset, setLocalReset] = useState(0);
  return (
    <Canvas
      flat
      linear
      resize={{ offsetSize: true }}
      dpr={[1, 2]}
      gl={{ preserveDrawingBuffer: true, antialias: true }}
      camera={{ fov: 28, position: [HOME.x, HOME.y, HOME.z], near: 0.01, far: 5 }}
      onDoubleClick={() => setLocalReset(Date.now())}
      data-testid="face-canvas"
    >
      <Suspense fallback={null}>
        <Face manifest={manifest} filter={filter} onReady={onReady} onApplied={onApplied} />
      </Suspense>
      <Controls resetAt={Math.max(cameraResetAt, localReset)} />
      {anchors && <AnchorProjector offset={panelOffset} />}
    </Canvas>
  );
}
