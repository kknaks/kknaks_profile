'use client';

import { FilterBar } from '@/components/common/filter-bar';
import { FaceViewer } from '@/components/viewer/face-viewer';
import type { FilterKey } from '@/domain/filters';

interface ViewerAreaProps {
  filter: FilterKey;
  cameraResetAt: number;
  onFilter: (f: FilterKey) => void;
  /** A2 지금 보는 것 카드(좌하 플로팅) */
  focusCard?: React.ReactNode;
}

/** 화면 ① A(3D 뷰) + A1(필터 바) — 1040×944 */
export function ViewerArea({ filter, cameraResetAt, onFilter, focusCard }: ViewerAreaProps) {
  return (
    <section className="relative h-full w-full overflow-hidden rounded-xl bg-ms-gray-800" data-testid="screen-viewer">
      <div className="absolute inset-0 bottom-[96px]">
        <FaceViewer filter={filter} cameraResetAt={cameraResetAt} />
      </div>
      {focusCard && <div className="absolute bottom-[112px] left-6 w-[400px]">{focusCard}</div>}
      <div className="absolute inset-x-0 bottom-0 flex h-[96px] items-center justify-center bg-ms-black/40 px-6">
        <FilterBar size="screen" value={filter} onChange={onFilter} />
      </div>
    </section>
  );
}
