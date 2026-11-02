'use client';

import { Tooltip, TooltipContent, TooltipTrigger } from '@medisolve-ai/medikit';
import { Info } from 'lucide-react';
import { GradeBadge } from '@/components/common/grade-badge';
import { COPY } from '@/content/copy';
import { formatScore, GRADE_META } from '@/domain/grade';
import type { SkinReport } from '@/domain/skin-report';
import { useSessionStore } from '@/stores/session-store';

/** 피부 분석 탭(새 탭) — 항목 탭 = 큰 화면에서 강조 + 이어진 필터, 다시 탭 = 해제 */
export function AnalysisPanel({ report }: { report: SkinReport | null }) {
  const focusItem = useSessionStore((s) => s.session.focusItem);
  const toggleFocusItem = useSessionStore((s) => s.toggleFocusItem);

  if (!report) {
    return <p className="p-4 text-center text-typo-caption-md-400 text-ms-gray-500">{COPY.reportMissing}</p>;
  }

  return (
    <div className="custom-scrollbar h-full overflow-y-auto px-3 py-2" data-testid="analysis-panel">
      <div className="grid grid-cols-4 gap-1.5">
        {report.categories.map((c) => (
          <div key={c.key} data-testid={`analysis-cat-${c.key}`} className="rounded-lg border border-ms-gray-300 px-2 py-1.5">
            <p className="truncate text-[10px] text-ms-gray-600">{c.label}</p>
            <div className="flex items-center justify-between gap-1">
              <span className="text-[15px] font-bold" style={{ color: GRADE_META[c.grade].color }}>
                {formatScore(c.score)}
              </span>
              <GradeBadge grade={c.grade} size="sm" className="!px-1.5 text-[10px]" />
            </div>
          </div>
        ))}
      </div>
      <p className="mb-1 mt-2.5 text-[10px] text-ms-gray-500">항목을 누르면 큰 화면에서 강조돼요. 다시 누르면 해제</p>
      <ul className="space-y-1">
        {report.items.map((it) => {
          const on = focusItem === it.key;
          return (
            <li key={it.key}>
              <button
                type="button"
                onClick={() => toggleFocusItem(it.key)}
                className={`w-full rounded-lg border px-2.5 py-1.5 text-left transition-colors ${on ? 'border-primary bg-primary-100' : 'border-ms-gray-300 hover:bg-ms-gray-100'}`}
                data-testid={`analysis-item-${it.key}`}
                data-focus={on}
              >
                <div className="flex items-center gap-2">
                  <span className={`flex-1 text-[12px] font-semibold ${on ? 'text-primary' : 'text-ms-black'}`}>{it.label}</span>
                  <span className="text-[13px] font-bold tabular-nums" style={{ color: GRADE_META[it.grade].color }}>
                    {it.score == null ? '' : formatScore(it.score)}
                  </span>
                  <GradeBadge grade={it.grade} size="sm" />
                </div>
                <div className="mt-0.5 flex flex-wrap gap-x-3 text-[10px] text-ms-gray-600">
                  {it.metrics.slice(0, 2).map((m) => (
                    <span key={m.key} className="inline-flex items-center gap-0.5">
                      {m.label} <b className="text-ms-gray-800">{m.display}</b>
                      {m.sided && (
                        <Tooltip>
                          <TooltipTrigger asChild>
                            <span role="img" aria-label={COPY.sideNote} data-testid="side-note" onClick={(e) => e.stopPropagation()}>
                              <Info className="h-3 w-3 text-ms-gray-500" />
                            </span>
                          </TooltipTrigger>
                          <TooltipContent>{COPY.sideNote}</TooltipContent>
                        </Tooltip>
                      )}
                    </span>
                  ))}
                </div>
              </button>
            </li>
          );
        })}
      </ul>
    </div>
  );
}
