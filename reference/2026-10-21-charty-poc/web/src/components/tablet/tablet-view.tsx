'use client';

import { NotifyContainer, TooltipProvider } from '@medisolve-ai/medikit';
import { useMemo } from 'react';
import { recommend } from '@/data/recommend-rules';
import type { SkinReportState } from '@/data/sources/use-skin-report';
import { AppHeader } from './app-header';
import { CustomerBar } from './customer-bar';
import { FilterStrip } from './filter-strip';
import { PricingPanel, PROCEDURES } from './pricing-panel';
import { RecommendationPanel } from './recommendation-panel';
import { RightTabs } from './right-tabs';

/** 화면 ② 1180×820 — 헤더 → 고객 바 → 좌우 분할(좌 700 | 핸들 8 | 우 472). 차티 데스크톱 배치(stg consultation-desktop.tsx:41-122) */
export function TabletView({ report, screenLinked }: { report: SkinReportState; screenLinked: boolean }) {
  const r = report.status === 'ready' ? report.report : null;
  const rec = useMemo(() => (r ? recommend(r, PROCEDURES) : { chips: [], procedureIds: [] }), [r]);

  return (
    <TooltipProvider>
      <div className="flex h-full w-full flex-col bg-white" data-testid="tablet-root">
        <AppHeader />
        <CustomerBar customerName={r?.customer.name ?? null} measuredAt={r?.measuredAt ?? null} screenLinked={screenLinked} />
        <main className="flex min-h-0 flex-1 overflow-hidden">
          <div className="flex w-[700px] shrink-0 flex-col">
            <FilterStrip />
            <div className="flex min-h-0 flex-1">
              <PricingPanel recommendedIds={rec.procedureIds} />
              <RecommendationPanel chips={rec.chips} />
            </div>
          </div>
          {/* 분할 핸들 — 차티와 같은 w-2. 목업은 드래그 없이 고정폭 */}
          <div className="w-2 shrink-0 bg-ms-gray-200" />
          <div className="min-w-0 flex-1">
            <RightTabs report={r} />
          </div>
        </main>
      </div>
      <NotifyContainer />
    </TooltipProvider>
  );
}
