import { FaceRegionMap } from '@/components/charts/face-region-map';
import { GradeBadge } from '@/components/common/grade-badge';
import { ITEM_COPY, gradeSentence } from '@/content/copy';
import { FILTERS, type FilterKey } from '@/domain/filters';
import { formatScore } from '@/domain/grade';
import type { SkinReport } from '@/domain/skin-report';

/** A2 지금 보는 것 — 자연광이면 숨김 */
export function FocusCard({ filter, report }: { filter: FilterKey; report: SkinReport | null }) {
  const def = FILTERS[filter];
  if (!def.relatedItem) return null;
  const item = report?.items.find((i) => i.key === def.relatedItem);
  const metrics = item?.metrics.filter((m) => !m.tabletOnly).slice(0, 3) ?? [];
  const isWrinkle = filter === 'fineWrinkle' || filter === 'deepWrinkle';

  return (
    <div className="rounded-xl border border-ms-gray-300 bg-white/95 p-5 shadow-lg" data-testid="focus-card" data-filter={filter}>
      <div className="flex items-center justify-between">
        <span className="text-typo-title-sm-600 text-ms-black">{def.label}</span>
        {item && (
          <span className="flex items-center gap-2">
            <span className="text-typo-title-lg-600 text-ms-black">{item.score == null ? '' : formatScore(item.score)}</span>
            <GradeBadge grade={item.grade} size="lg" />
          </span>
        )}
      </div>
      {def.legend && (
        <p className="mt-2 flex items-center gap-2 text-typo-heading-md-500 text-ms-gray-800">
          {def.overlayColor && <span className="h-3 w-6 rounded-full" style={{ background: def.overlayColor, boxShadow: '0 0 0 1px var(--ms-gray-400)' }} />}
          {def.legend}
        </p>
      )}
      {item && (
        <p className="mt-2 text-typo-heading-md-400 text-ms-gray-700">
          {item.score == null ? item.scoreNote : gradeSentence(item.label, item.grade)}. {ITEM_COPY[item.key].meaning}
        </p>
      )}
      {metrics.length > 0 && (
        <ul className="mt-3 flex flex-wrap gap-x-5 gap-y-1">
          {metrics.map((m) => (
            <li key={m.key} className="text-typo-heading-md-400 text-ms-gray-700">
              {m.label} <b className="text-ms-black">{m.display}</b>
            </li>
          ))}
        </ul>
      )}
      {isWrinkle && report && (
        <div className="mt-3">
          <FaceRegionMap regions={report.wrinkleRegions} emphasis={filter === 'fineWrinkle' ? 'fine' : 'deep'} />
        </div>
      )}
    </div>
  );
}
