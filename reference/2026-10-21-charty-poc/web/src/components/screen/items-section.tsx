import { Card } from '@medisolve-ai/medikit';
import { ScoreBars } from '@/components/charts/score-bars';
import type { ItemKey, SkinReport } from '@/domain/skin-report';

export function ItemsSection({ report, highlight }: { report: SkinReport; highlight: ItemKey | null }) {
  return (
    <Card padding="md" className="h-full gap-2" data-testid="screen-items">
      <div className="flex items-center justify-between">
        <h2 className="text-typo-title-sm-600 text-ms-black">항목별 상태</h2>
        <span className="text-typo-heading-md-400 text-ms-gray-600">점수가 높을수록 좋아요 · 눈금 60 · 70 · 85</span>
      </div>
      <ScoreBars items={report.items} highlight={highlight} />
    </Card>
  );
}
