import { Card } from '@medisolve-ai/medikit';
import { RadarChart } from '@/components/charts/radar-chart';
import { GradeBadge } from '@/components/common/grade-badge';
import { GRADE_PHRASE, summaryLine } from '@/content/copy';
import { formatScore } from '@/domain/grade';
import type { CategoryKey, SkinReport } from '@/domain/skin-report';

// 레이더 꼭짓점 순서: 위 염증·민감 → 오른쪽 피부톤 → 아래 피부결 → 왼쪽 노화
const RADAR_ORDER: CategoryKey[] = ['inflammation', 'tone', 'texture', 'aging'];

export function OverviewSection({ report, focusCategory }: { report: SkinReport; focusCategory: CategoryKey | null }) {
  const cats = RADAR_ORDER.map((k) => report.categories.find((c) => c.key === k)).filter((c) => !!c);
  return (
    <Card padding="md" className="h-full" data-testid="screen-overview">
      <h2 className="text-typo-title-sm-600 text-ms-black">한눈에 보기</h2>
      <div className="flex flex-1 items-center gap-3">
        <RadarChart categories={cats} size={280} highlight={focusCategory} />
        <div className="grid flex-1 grid-cols-2 gap-3">
          {report.categories.map((c) => (
            <div
              key={c.key}
              data-testid={`cat-${c.key}`}
              data-focus={focusCategory === c.key}
              className={`rounded-xl border px-3 py-2.5 ${focusCategory === c.key ? 'border-primary ring-2 ring-primary' : 'border-ms-gray-300'}`}
            >
              <div className="flex items-center justify-between">
                <span className="text-typo-heading-md-600 text-ms-gray-800">{c.label}</span>
                <GradeBadge grade={c.grade} size="screen" />
              </div>
              <p className="text-typo-title-lg-600 text-ms-black">{formatScore(c.score)}</p>
              <p className="text-typo-heading-md-400 leading-snug tracking-tight text-ms-gray-700">{GRADE_PHRASE[c.grade]}</p>
            </div>
          ))}
        </div>
      </div>
      <div className="flex items-center gap-3 border-t border-ms-gray-200 pt-3">
        <p className="flex-1 text-typo-title-sm-600 text-primary" data-testid="summary-line">
          {summaryLine(report.categories)}
        </p>
        {report.tone && (
          <span className="flex items-center gap-2 text-typo-heading-md-500 text-ms-gray-700" data-testid="tone-chip">
            <span className="h-6 w-6 rounded-full border border-ms-gray-300" style={{ background: `rgb(${report.tone.rgb.join(',')})` }} />
            피부톤 {report.tone.name}
          </span>
        )}
      </div>
    </Card>
  );
}
