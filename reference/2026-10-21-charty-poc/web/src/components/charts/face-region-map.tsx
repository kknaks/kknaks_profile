import { GRADE_META, formatScore } from '@/domain/grade';
import type { RegionKey, WrinkleRegion } from '@/domain/skin-report';

// 정면 얼굴 선화(viewBox 360×230) 위 고정 좌표. 좌/우를 뜻하지 않는다 — 부위당 점 하나.
// 라벨은 겹치지 않게 양옆 열로 빼고 지시선으로 잇는다(잔주름 왼쪽 열 · 굵은 주름 오른쪽 열).
const DOT: Record<RegionKey, [number, number]> = {
  TT: [180, 40],
  MJ: [180, 82],
  BG: [180, 102],
  YD: [152, 116],
  YW: [124, 100],
  LG: [208, 122],
  FL: [204, 164],
  QJ: [234, 140],
};
const LABEL_Y: Record<RegionKey, number> = { TT: 34, MJ: 72, BG: 110, YD: 148, YW: 186, LG: 72, FL: 124, QJ: 176 };

interface FaceRegionMapProps {
  regions: WrinkleRegion[];
  /** 진하게 보일 무리 — 반대 무리는 흐리게 */
  emphasis: 'fine' | 'deep';
}

/** G3 주름 부위 맵 */
export function FaceRegionMap({ regions, emphasis }: FaceRegionMapProps) {
  return (
    <svg viewBox="0 0 360 220" className="h-[220px] w-full" role="img" aria-label="주름 부위 맵" data-testid="region-map" data-emphasis={emphasis}>
      <ellipse cx={180} cy={112} rx={78} ry={104} fill="var(--ms-gray-100)" stroke="var(--ms-gray-500)" strokeWidth={2} />
      <path d="M132 92 q14 -8 28 0 M200 92 q14 -8 28 0" stroke="var(--ms-gray-500)" strokeWidth={2} fill="none" />
      <path d="M180 100 l-9 38 q9 5 18 0" stroke="var(--ms-gray-500)" strokeWidth={2} fill="none" />
      <path d="M160 172 q20 12 40 0" stroke="var(--ms-gray-500)" strokeWidth={2} fill="none" />
      {regions.map((r) => {
        const [x, y] = DOT[r.key];
        const on = r.group === emphasis;
        const left = r.group === 'fine';
        const lx = left ? 92 : 268;
        const ly = LABEL_Y[r.key];
        return (
          <g key={r.key} opacity={on ? 1 : 0.28} data-testid={`region-${r.key}`} data-on={on}>
            <polyline points={`${x},${y} ${lx + (left ? 4 : -4)},${ly}`} stroke="var(--ms-gray-500)" strokeWidth={1} fill="none" />
            <circle cx={x} cy={y} r={6} fill={GRADE_META[r.grade].color} stroke="#fff" strokeWidth={2} />
            <text x={lx} y={ly + 5} textAnchor={left ? 'end' : 'start'} fontSize={15} fontWeight={600} fill="var(--ms-gray-800)">
              {r.label} <tspan fill={GRADE_META[r.grade].color}>{formatScore(r.score)}</tspan>
            </text>
          </g>
        );
      })}
    </svg>
  );
}
