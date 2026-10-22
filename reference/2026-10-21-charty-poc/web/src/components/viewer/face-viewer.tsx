'use client';

import { Loading } from '@medisolve-ai/medikit';
import dynamic from 'next/dynamic';
import { useCallback, useEffect, useState } from 'react';
import { COPY } from '@/content/copy';
import type { FilterKey } from '@/domain/filters';
import { loadManifest, type M3dManifest } from './manifest';

// WebGL 은 브라우저 전용
const FaceCanvas = dynamic(() => import('./face-canvas'), { ssr: false });

interface FaceViewerProps {
  filter: FilterKey;
  cameraResetAt: number;
}

export function FaceViewer({ filter, cameraResetAt }: FaceViewerProps) {
  const [manifest, setManifest] = useState<M3dManifest | null | undefined>(undefined);
  const [ready, setReady] = useState(false);
  const [applied, setApplied] = useState<FilterKey | null>(null);

  useEffect(() => {
    loadManifest().then(setManifest);
  }, []);

  const onReady = useCallback(() => setReady(true), []);

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
        <FaceCanvas manifest={manifest} filter={filter} cameraResetAt={cameraResetAt} onReady={onReady} onApplied={setApplied} />
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
