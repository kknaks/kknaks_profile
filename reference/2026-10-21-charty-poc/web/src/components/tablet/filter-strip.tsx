'use client';

import { Button } from '@medisolve-ai/medikit';
import { RotateCcw } from 'lucide-react';
import { FilterBar } from '@/components/common/filter-bar';
import { useSessionStore } from '@/stores/session-store';

/** 필터 띠 72 — 차티 상태 패널 72px 슬롯 자리(stg consultation-desktop.tsx:100-106). 태블릿엔 3D 를 그리지 않는다 */
export function FilterStrip() {
  const filter = useSessionStore((s) => s.session.filter);
  const setFilter = useSessionStore((s) => s.setFilter);
  const resetCamera = useSessionStore((s) => s.resetCamera);
  return (
    <div className="box-border flex h-[72px] shrink-0 items-center gap-2 border-b border-ms-gray-300 px-4">
      <span className="shrink-0 text-[11px] font-bold text-ms-gray-700">3D 필터</span>
      <div className="min-w-0 flex-1">
        <FilterBar size="tablet" value={filter} onChange={setFilter} />
      </div>
      <Button variant="outlined" color="gray" size="s" className="!h-8 shrink-0 gap-1 !px-2 !text-[11px]" onClick={resetCamera} data-testid="camera-reset">
        <RotateCcw className="h-3.5 w-3.5" /> 정면으로
      </Button>
    </div>
  );
}
