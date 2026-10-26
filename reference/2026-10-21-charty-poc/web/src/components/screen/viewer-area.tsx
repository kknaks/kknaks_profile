'use client';

import { useEffect, useMemo, useState } from 'react';
import { FilterBar } from '@/components/common/filter-bar';
import { anchorsUsable } from '@/components/viewer/anchors';
import { FaceViewer } from '@/components/viewer/face-viewer';
import { M3D_BASE, loadManifest, type M3dManifest } from '@/components/viewer/manifest';
import { FACE_ANCHORS } from '@/data/face-anchors';
import { COPY } from '@/content/copy';
import { AREA_LAYOUT, type AreaCardModel, type AreaChip, type AreaKey } from '@/domain/areas';
import { FILTERS, type FilterKey } from '@/domain/filters';
import { AreaCard, type ReportStatus } from './area-card';
import { CROP_FRAMES, type CropSource } from './area-crop';
import { LeaderLines } from './leader-lines';
import { COL_GAP, COL_PAD, COL_W, FACE_X0, FACE_X1, FILTER_BAR_H, LEGEND_H, VIEWER_W } from './viewer-layout';

interface ViewerAreaProps {
  filter: FilterKey;
  cameraResetAt: number;
  onFilter: (f: FilterKey) => void;
  cards: AreaCardModel[];
  reportStatus: ReportStatus;
  onDetail: (chip: AreaChip) => void;
  onToggle: (key: AreaKey) => void;
  onSelect: (key: AreaKey) => void;
}

type ColumnProps = Pick<ViewerAreaProps, 'cards' | 'onDetail' | 'onToggle' | 'onSelect'> & {
  side: 'left' | 'right';
  status: ReportStatus;
  crops: Partial<Record<AreaKey, CropSource>>;
};

function Column({ side, cards, status, crops, onDetail, onToggle, onSelect }: ColumnProps) {
  return (
    <div
      className="pointer-events-none absolute flex flex-col"
      style={{ top: COL_PAD, bottom: FILTER_BAR_H + LEGEND_H, width: COL_W, gap: COL_GAP, [side]: COL_PAD }}
      data-testid={`area-col-${side}`}
    >
      {AREA_LAYOUT[side].map((k) => {
        const c = cards.find((x) => x.key === k)!;
        return <AreaCard key={k} card={c} status={status} crop={crops[k] ?? null} onDetail={onDetail} onToggle={onToggle} onSelect={onSelect} />;
      })}
    </div>
  );
}

/** 화면 ① A(3D 뷰 + 얼굴 좌우 부위 카드) + 범례 줄 + 필터 바 — 1040×984 */
/** 부위 확대 사진 원천 — 지금 필터 텍스처 + 오버레이 + 앵커 UV. 에셋 없음 · 메시 가드 불일치면 비운다(회색 자리표시) */
function useCrops(filter: FilterKey): Partial<Record<AreaKey, CropSource>> {
  const [manifest, setManifest] = useState<M3dManifest | null>(null);
  useEffect(() => {
    loadManifest().then(setManifest);
  }, []);
  return useMemo(() => {
    if (!manifest || !anchorsUsable(manifest, FACE_ANCHORS)) return {};
    const def = FILTERS[filter];
    const t = manifest.textures[def.texture];
    if (!t) return {};
    const ov = def.overlay ? manifest.overlays[def.overlay] : null;
    const out: Partial<Record<AreaKey, CropSource>> = {};
    for (const a of FACE_ANCHORS.points) {
      if (!a.uv) continue;
      out[a.key as AreaKey] = {
        tex: { url: `${M3D_BASE}/${t.file}`, w: t.w, h: t.h },
        overlay: ov && def.overlayColor ? { url: `${M3D_BASE}/${ov.file}`, color: def.overlayColor } : null,
        uv: a.uv,
        frame: CROP_FRAMES[a.key] ?? { r: 240, dx: 0, dy: 0 },
      };
    }
    return out;
  }, [manifest, filter]);
}

export function ViewerArea({ filter, cameraResetAt, onFilter, cards, reportStatus, onDetail, onToggle, onSelect }: ViewerAreaProps) {
  const def = FILTERS[filter];
  const [anchorsActive, setAnchorsActive] = useState(false);
  const crops = useCrops(filter);
  return (
    <section className="relative h-full w-full overflow-hidden rounded-xl bg-ms-gray-800" data-testid="screen-viewer">
      {/* 캔버스 = 두 카드 열 사이(얼굴 구역). 회전 시 넘치는 볼은 카드 가장자리에서 잘린다 */}
      <div className="absolute top-0" style={{ left: FACE_X0, right: VIEWER_W - FACE_X1, bottom: FILTER_BAR_H }}>
        <FaceViewer filter={filter} cameraResetAt={cameraResetAt} panelOffset={[FACE_X0, 0]} onAnchorsActive={setAnchorsActive} />
      </div>
      {anchorsActive && <LeaderLines cards={cards} />}
      <div data-testid="area-cards">
        <Column side="left" cards={cards} status={reportStatus} crops={crops} onDetail={onDetail} onToggle={onToggle} onSelect={onSelect} />
        <Column side="right" cards={cards} status={reportStatus} crops={crops} onDetail={onDetail} onToggle={onToggle} onSelect={onSelect} />
      </div>
      <div
        className="pointer-events-none absolute inset-x-0 flex items-center justify-between gap-4 px-6 text-typo-heading-md-500"
        style={{ bottom: FILTER_BAR_H, height: LEGEND_H }}
        data-testid="viewer-legend"
      >
        <span className="flex items-center gap-2 text-ms-gray-200">
          {def.legend && def.overlayColor && (
            <span className="h-3 w-6 rounded-full" style={{ background: def.overlayColor, boxShadow: '0 0 0 1px var(--ms-gray-400)' }} />
          )}
          {def.legend}
        </span>
        <span className="text-ms-gray-400">{COPY.mockNote}</span>
      </div>
      <div className="absolute inset-x-0 bottom-0 flex items-center justify-center bg-ms-black/40 px-6" style={{ height: FILTER_BAR_H }}>
        <FilterBar size="screen" value={filter} onChange={onFilter} />
      </div>
    </section>
  );
}
