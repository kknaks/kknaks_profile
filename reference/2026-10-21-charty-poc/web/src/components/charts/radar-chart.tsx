import { GRADE_META, GRADE_TICKS, formatScore } from '@/domain/grade';
import type { SkinCategory } from '@/domain/skin-report';

interface RadarChartProps {
  /** 위 → 오른쪽 → 아래 → 왼쪽 순 */
  categories: SkinCategory[];
  size?: number;
  highlight?: string | null;
}

/** G1 종합 레이더 — 0–100, 바깥일수록 좋음. 60·70·85 등급 띠를 옅은 점선으로 깐다 */
export function RadarChart({ categories, size = 320, highlight }: RadarChartProps) {
  const c = size / 2;
  const R = size / 2 - 48;
  const n = categories.length;
  const angle = (i: number) => -Math.PI / 2 + (i * 2 * Math.PI) / n;
  const pt = (i: number, v: number) => [c + Math.cos(angle(i)) * (R * v) / 100, c + Math.sin(angle(i)) * (R * v) / 100] as const;
  const poly = (v: (i: number) => number) => categories.map((_, i) => pt(i, v(i)).join(',')).join(' ');

  return (
    <svg width={size} height={size} viewBox={`0 0 ${size} ${size}`} role="img" aria-label="피부 종합 레이더" data-testid="radar">
      <polygon points={poly(() => 100)} fill="var(--ms-gray-100)" stroke="var(--ms-gray-300)" />
      {GRADE_TICKS.map((t) => (
        <polygon key={t} points={poly(() => t)} fill="none" stroke="var(--ms-gray-400)" strokeDasharray="4 4" />
      ))}
      {categories.map((_, i) => {
        const [x, y] = pt(i, 100);
        return <line key={i} x1={c} y1={c} x2={x} y2={y} stroke="var(--ms-gray-300)" />;
      })}
      <polygon points={poly((i) => categories[i].score ?? 0)} fill="var(--ms-primary)" fillOpacity={0.14} stroke="var(--ms-primary)" strokeWidth={2.5} />
      {categories.map((cat, i) => {
        const [x, y] = pt(i, cat.score ?? 0);
        const [lx, ly] = pt(i, 124);
        const hl = highlight === cat.key;
        return (
          <g key={cat.key} data-testid={`radar-${cat.key}`} data-score={cat.score ?? ''}>
            <circle cx={x} cy={y} r={hl ? 9 : 7} fill={GRADE_META[cat.grade].color} stroke="#fff" strokeWidth={2.5} />
            <text x={lx} y={ly - 10} textAnchor="middle" fontSize={16} fontWeight={600} fill="var(--ms-gray-800)">
              {cat.label}
            </text>
            <text x={lx} y={ly + 12} textAnchor="middle" fontSize={18} fontWeight={700} fill={GRADE_META[cat.grade].color}>
              {formatScore(cat.score)}
            </text>
          </g>
        );
      })}
    </svg>
  );
}
