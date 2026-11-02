'use client';

import { Card, Loading } from '@medisolve-ai/medikit';
import dynamic from 'next/dynamic';
import { useState } from 'react';
import { COPY } from '@/content/copy';
import { areaCards, type AreaKey } from '@/domain/areas';
import { FILTERS, type FilterKey } from '@/domain/filters';
import type { SessionState } from '@/domain/session';
import type { SkinReportState } from '@/data/sources/use-skin-report';
import { ItemsSection } from './items-section';
import { OverviewSection } from './overview-section';
import { PlanPanel } from './plan-panel';
import { ProcedureModal } from './procedure-modal';
import { ScreenHeader } from './screen-header';
import { ViewerArea } from './viewer-area';

// 찍기 도구는 개발 서버에서만 — 프로덕션 빌드에서는 import 자체가 빠진다(W-5)
const AnchorEditor = process.env.NODE_ENV === 'production' ? () => null : dynamic(() => import('@/components/viewer/anchor-editor'), { ssr: false });

interface ScreenViewProps {
  session: SessionState;
  report: SkinReportState;
  linked: boolean;
  onFilter: (f: FilterKey) => void;
}

function ReportPlaceholder({ state, title }: { state: SkinReportState; title: string }) {
  return (
    <Card padding="md" className="h-full">
      <h2 className="text-typo-title-sm-600 text-ms-black">{title}</h2>
      <div className="flex flex-1 items-center justify-center gap-3 text-typo-title-sm-500 text-ms-gray-600" data-testid="report-missing">
        {state.status === 'loading' ? <Loading className="h-8 w-8" /> : COPY.reportMissing}
      </div>
    </Card>
  );
}

/** 화면 ① 1920×1080 — 태블릿 상태의 사본을 그리기만 한다 */
export function ScreenView({ session, report, linked, onFilter }: ScreenViewProps) {
  const r = report.status === 'ready' ? report.report : null;
  const highlight = session.focusItem ?? FILTERS[session.filter].relatedItem;
  const focusCategory = r?.categories.find((c) => highlight && c.items.includes(highlight))?.key ?? null;
  // 카드 선택(U-2) — 큰 화면 로컬 상태. 고를 때의 필터·항목을 같이 적어 두고, 태블릿에서 필터가 바뀌어 오면 선택은 저절로 풀린다
  const [pick, setPick] = useState<{ key: AreaKey; filter: FilterKey; focusItem: SessionState['focusItem'] } | null>(null);
  const selected = pick && pick.filter === session.filter && pick.focusItem === session.focusItem ? pick.key : null;
  const cards = areaCards(r, session, selected);
  const [modal, setModal] = useState<{ hubId: string; label: string } | null>(null);
  const select = (key: AreaKey) => setPick({ key, filter: session.filter, focusItem: session.focusItem });
  const toggle = (key: AreaKey) => (selected === key ? setPick(null) : select(key));
  const filterAndClear = (f: FilterKey) => {
    setPick(null);
    onFilter(f);
  };

  return (
    <div className="relative flex h-full w-full flex-col bg-ms-gray-100" data-testid="screen-root">
      <AnchorEditor />
      <ScreenHeader customerName={r?.customer.name ?? null} measuredAt={r?.measuredAt ?? null} linked={linked} />
      <div className="flex min-h-0 flex-1 gap-6 px-6 py-4">
        <div className="h-full w-[1040px] shrink-0">
          <ViewerArea
            filter={session.filter}
            cameraResetAt={session.cameraResetAt}
            onFilter={filterAndClear}
            cards={cards}
            reportStatus={report.status}
            onDetail={setModal}
            onToggle={toggle}
            onSelect={select}
          />
        </div>
        <div className="flex min-w-0 flex-1 flex-col gap-4">
          <div className="h-[372px] shrink-0">
            {r ? <OverviewSection report={r} focusCategory={focusCategory} /> : <ReportPlaceholder state={report} title="한눈에 보기" />}
          </div>
          <div className="h-[300px] shrink-0">
            {r ? <ItemsSection report={r} highlight={highlight} /> : <ReportPlaceholder state={report} title="항목별 상태" />}
          </div>
          <div className="min-h-0 flex-1">
            <PlanPanel cart={session.cart} discountRate={session.discountRate} showPrice={session.screen.showPrice} />
          </div>
        </div>
      </div>
      {modal && <ProcedureModal hubId={modal.hubId} label={modal.label} onClose={() => setModal(null)} />}
    </div>
  );
}
