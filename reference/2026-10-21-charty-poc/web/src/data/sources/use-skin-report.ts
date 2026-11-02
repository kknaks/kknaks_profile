'use client';

import { useEffect, useState } from 'react';
import type { SkinReport } from '@/domain/skin-report';
import { M3dMockSource } from './m3d-mock-source';

// 고객 이름은 원본 user 를 읽지 않고 여기서 넣는다(SPEC §5-1).
const source = new M3dMockSource({ baseUrl: '/m3d/report', manifestUrl: '/m3d/manifest.json', customer: { name: '이건학' } });

export type SkinReportState =
  | { status: 'loading'; report: null }
  | { status: 'ready'; report: SkinReport }
  | { status: 'missing'; report: null };

let cache: Promise<SkinReport> | null = null;

export function useSkinReport(): SkinReportState {
  const [state, setState] = useState<SkinReportState>({ status: 'loading', report: null });
  useEffect(() => {
    let alive = true;
    cache ??= source.load();
    cache.then(
      (report) => alive && setState({ status: 'ready', report }),
      () => {
        cache = null;
        if (alive) setState({ status: 'missing', report: null });
      },
    );
    return () => {
      alive = false;
    };
  }, []);
  return state;
}
