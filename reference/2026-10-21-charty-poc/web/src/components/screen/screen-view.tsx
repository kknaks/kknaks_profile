'use client';

import { Card, Loading } from '@medisolve-ai/medikit';
import { COPY } from '@/content/copy';
import { FILTERS, type FilterKey } from '@/domain/filters';
import type { SessionState } from '@/domain/session';
import type { SkinReportState } from '@/data/sources/use-skin-report';
import { FocusCard } from './focus-card';
import { ItemsSection } from './items-section';
import { OverviewSection } from './overview-section';
import { PlanPanel } from './plan-panel';
import { ScreenHeader } from './screen-header';
import { ViewerArea } from './viewer-area';

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

  return (
    <div className="flex h-full w-full flex-col bg-ms-gray-100" data-testid="screen-root">
      <ScreenHeader customerName={r?.customer.name ?? null} measuredAt={r?.measuredAt ?? null} linked={linked} />
      <div className="flex min-h-0 flex-1 gap-6 px-6 py-4">
        <div className="h-full w-[1040px] shrink-0">
          <ViewerArea
            filter={session.filter}
            cameraResetAt={session.cameraResetAt}
            onFilter={onFilter}
            focusCard={<FocusCard filter={session.filter} report={r} />}
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
    </div>
  );
}
