'use client';

import { Loading } from '@medisolve-ai/medikit';
import dynamic from 'next/dynamic';
import { useCallback, useEffect, useState } from 'react';
import { COPY } from '@/content/copy';
import { FACE_ANCHORS } from '@/data/face-anchors';
import type { FilterKey } from '@/domain/filters';
import { anchorsUsable } from './anchors';
import { loadManifest, type M3dManifest } from './manifest';
import { useAnchorEdit } from './use-anchor-edit';

// WebGL 은 브라우저 전용
const FaceCanvas = dynamic(() => import('./face-canvas'), { ssr: false });

interface FaceViewerProps {
  filter: FilterKey;
  cameraResetAt: number;
  /** 캔버스 원점의 뷰어 패널 좌표 */
  panelOffset?: [number, number];
  /** 점·지시선을 그려도 되는지(첫 프레임 뒤 · 메시 가드 통과) */
  onAnchorsActive?: (active: boolean) => void;
}

let warned = false;

export function FaceViewer({ filter, cameraResetAt, panelOffset, onAnchorsActive }: FaceViewerProps) {
  const [manifest, setManifest] = useState<M3dManifest | null | undefined>(undefined);
  const [ready, setReady] = useState(false);
  const [applied, setApplied] = useState<FilterKey | null>(null);

  useEffect(() => {
    loadManifest().then(setManifest);
  }, []);

  const onReady = useCallback(() => setReady(true), []);
  const editing = useAnchorEdit();
  const usable = anchorsUsable(manifest, FACE_ANCHORS);
  const anchors = !!manifest && (usable || editing);
  useEffect(() => {
    if (manifest && !usable && !warned) {
      warned = true;
      console.warn(`[anchors] mesh mismatch — manifest mesh.bytes ${manifest.mesh.bytes} ≠ FACE_ANCHORS.meshBytes ${FACE_ANCHORS.meshBytes} (or no points). 점·지시선을 그리지 않는다`);
    }
  }, [manifest, usable]);
  useEffect(() => {
    onAnchorsActive?.(anchors && ready);
  }, [anchors, ready, onAnchorsActive]);

  if (manifest === null) {
    return (
      <div className="flex h-full w-full items-center justify-center p-10 text-center" data-testid="viewer-missing">
        <p className="text-typo-title-sm-500 text-ms-gray-400">{COPY.assetsMissing}</p>
      </div>
    );
  }

  return (
    <div className="relative h-full w-full" data-testid="face-viewer" data-ready={ready} data-applied={applied ?? ''}>
      {manifest && (
        <FaceCanvas
          manifest={manifest}
          filter={filter}
          cameraResetAt={cameraResetAt}
          onReady={onReady}
          onApplied={setApplied}
          anchors={anchors}
          panelOffset={panelOffset}
        />
      )}
      {!ready && (
        <div className="pointer-events-none absolute inset-0 flex flex-col items-center justify-center gap-3">
          <Loading className="h-10 w-10" />
          <p className="text-typo-heading-md-500 text-ms-gray-400">{COPY.faceLoading}</p>
        </div>
      )}
    </div>
  );
}
