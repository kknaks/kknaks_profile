'use client';

import type { SkinReport } from '@/domain/skin-report';
import { useSessionStore, type TabletTab } from '@/stores/session-store';
import { AnalysisPanel } from './analysis-panel';
import { ChartPanel } from './chart-panel';
import { ChecklistPanel } from './checklist-panel';
import { TranscriptPanel } from './transcript-panel';

// 「피부 분석」 탭을 맨 앞에 추가(SPEC §11-2). 나머지는 stg chart-toolbar.tsx:29-34
const TABS: { id: TabletTab; name: string }[] = [
  { id: 'analysis', name: '피부 분석' },
  { id: 'checklist', name: '체크리스트' },
  { id: 'chart', name: '차트' },
  { id: 'raw', name: '상담 텍스트' },
];

export function RightTabs({ report }: { report: SkinReport | null }) {
  const tab = useSessionStore((s) => s.ui.tab);
  const setUi = useSessionStore((s) => s.setUi);
  return (
    <div className="flex h-full flex-col bg-white">
      <div className="flex shrink-0 items-stretch" role="tablist">
        {TABS.map((t) => {
          const active = tab === t.id;
          return (
            <button
              key={t.id}
              type="button"
              role="tab"
              aria-selected={active}
              onClick={() => setUi({ tab: t.id })}
              data-testid={`tab-${t.id}`}
              className={`flex flex-1 items-center justify-center border-b-2 bg-transparent py-2.5 text-center text-typo-heading-sm-400 transition-colors ${
                active ? 'border-primary font-medium text-primary' : 'border-ms-gray-300 font-normal text-ms-gray-600 hover:text-ms-gray-800'
              }`}
            >
              {t.name}
            </button>
          );
        })}
      </div>
      <div className="min-h-0 flex-1">
        {tab === 'analysis' && <AnalysisPanel report={report} />}
        {tab === 'checklist' && <ChecklistPanel />}
        {tab === 'chart' && <ChartPanel report={report} />}
        {tab === 'raw' && <TranscriptPanel />}
      </div>
    </div>
  );
}
