'use client';
/* eslint-disable react-hooks/immutability -- three.js 재질 uniform 은 useFrame·effect 안에서 직접 바꾸는 것이 r3f 관례다(재렌더 없이 GPU 값만 갱신) */

import { OrbitControls } from '@react-three/drei';
import { Canvas, useFrame, useLoader, useThree } from '@react-three/fiber';
import { Suspense, useEffect, useMemo, useRef, useState } from 'react';
import * as THREE from 'three';
import { OBJLoader } from 'three/examples/jsm/loaders/OBJLoader.js';
import type { OrbitControls as OrbitControlsImpl } from 'three-stdlib';
import { FILTERS, type FilterKey } from '@/domain/filters';
import { createFaceMaterial, prepareTexture } from './face-material';
import { M3D_BASE, type M3dManifest } from './manifest';

const DEG = Math.PI / 180;
const HOME = new THREE.Vector3(0, 0, 0.55);
const FADE_MS = 250;
const RESET_MS = 600;

export interface FaceCanvasProps {
  manifest: M3dManifest;
  filter: FilterKey;
  cameraResetAt: number;
  onReady?: () => void;
  onApplied?: (filter: FilterKey) => void;
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

  return <mesh geometry={geometry} material={material} />;
}

function Controls({ resetAt }: { resetAt: number }) {
  const ref = useRef<OrbitControlsImpl>(null);
  const camera = useThree((s) => s.camera);
  const reset = useRef<{ from: THREE.Vector3; t0: number } | null>(null);

  useEffect(() => {
    if (!resetAt) return;
    reset.current = { from: camera.position.clone(), t0: performance.now() };
  }, [resetAt, camera]);

  useEffect(() => {
    window.__faceViewer = {
      azimuthDeg: () => (ref.current?.getAzimuthalAngle() ?? 0) / DEG,
      polarDeg: () => (ref.current?.getPolarAngle() ?? 0) / DEG,
      distance: () => camera.position.length(),
      project: (x, y, z) => {
        const v = new THREE.Vector3(x, y, z).project(camera);
        return [v.x, v.y];
      },
      applied: window.__faceViewer?.applied ?? null,
    };
  }, [camera]);

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

export default function FaceCanvas({ manifest, filter, cameraResetAt, onReady, onApplied }: FaceCanvasProps) {
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
    </Canvas>
  );
}
