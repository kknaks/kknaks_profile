export interface M3dManifest {
  generatedAt: string;
  mesh: { file: string; bytes: number };
  textures: Record<string, { file: string; w: number; h: number }>;
  overlays: Record<string, { file: string; w: number; h: number; coverage: number }>;
}

export const M3D_BASE = '/m3d';

let cache: Promise<M3dManifest | null> | null = null;

/** 매니페스트가 없으면(준비 스크립트 미실행) null */
export function loadManifest(): Promise<M3dManifest | null> {
  cache ??= fetch(`${M3D_BASE}/manifest.json`, { cache: 'no-store' })
    .then((r) => (r.ok ? (r.json() as Promise<M3dManifest>) : null))
    .catch(() => null);
  return cache;
}
