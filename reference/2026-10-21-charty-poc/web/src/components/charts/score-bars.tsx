import { GradeBadge } from '@/components/common/grade-badge';
import { GRADE_META, GRADE_TICKS, formatScore } from '@/domain/grade';
import type { ItemKey, SkinItem } from '@/domain/skin-report';

interface ScoreBarsProps {
  items: SkinItem[];
  highlight: ItemKey | null;
}

/** G2 항목별 막대 — 길이 = 점수/100, 색 = 등급색, 60·70·85 세로 눈금 */
export function ScoreBars({ items, highlight }: ScoreBarsProps) {
  return (
    <ul className="flex flex-col" data-testid="score-bars">
      {items.map((it) => {
        const hl = highlight === it.key;
        return (
          <li
            key={it.key}
            data-testid={`bar-${it.key}`}
            data-highlight={hl}
            data-score={it.score ?? ''}
            data-grade={it.grade}
            className={`flex h-[28px] items-center gap-4 rounded-lg px-3 transition-colors ${hl ? 'bg-primary-100 ring-2 ring-primary' : ''}`}
          >
            <span className={`w-[150px] shrink-0 truncate text-typo-heading-md-600 ${hl ? 'text-primary' : 'text-ms-gray-800'}`}>{it.label}</span>
            {it.score == null ? (
              <span className="flex-1 truncate text-typo-heading-md-500 text-ms-gray-600">
                {/* 점수 없음 — 막대 대신 개수·비율(SPEC §2-2 G2) */}
                {it.metrics
                  .filter((m) => !m.tabletOnly)
                  .map((m) => (m.unit === '%' ? `얼굴의 ${m.display}` : m.display))
                  .join(' · ') || '점수 없음'}
              </span>
            ) : (
              <span className="relative h-3 flex-1 rounded-full bg-ms-gray-200">
                <span
                  className="absolute inset-y-0 left-0 rounded-full"
                  style={{ width: `${it.score}%`, background: GRADE_META[it.grade].color }}
                />
                {GRADE_TICKS.map((t) => (
                  <span key={t} className="absolute -inset-y-1 w-px bg-ms-gray-500" style={{ left: `${t}%` }} />
                ))}
              </span>
            )}
            <span className="w-[56px] shrink-0 text-right text-typo-title-sm-600 tabular-nums" style={{ color: GRADE_META[it.grade].color }}>
              {it.score == null ? '' : formatScore(it.score)}
            </span>
            <span className="flex w-[150px] shrink-0 justify-end">
              <GradeBadge grade={it.grade} size="screen" className="h-7" />
            </span>
          </li>
        );
      })}
    </ul>
  );
}
