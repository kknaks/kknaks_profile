// M3D 응답 → SkinReport 어댑터(SPEC §5-3, §5-4). 화면 모델과 원본 사이의 유일한 경계.
import { ITEM_COPY, CATEGORY_COPY, REGION_LABEL, porphyrinScoreNote } from '@/content/copy';
import { gradeOf } from '@/domain/grade';
import type {
  CategoryKey,
  ItemKey,
  Metric,
  RegionKey,
  SkinItem,
  SkinReport,
  TextureKey,
  WrinkleRegion,
} from '@/domain/skin-report';
import type { M3dFeature, M3dMeasure, M3dRender, M3dResult } from './m3d-types';

const CATEGORY_MAP: { id: string; key: CategoryKey; items: ItemKey[] }[] = [
  { id: 'basic_247', key: 'inflammation', items: ['redness', 'porphyrin'] },
  { id: 'basic_246', key: 'tone', items: ['pigment', 'brightness'] },
  { id: 'basic_245', key: 'texture', items: ['pore', 'dermatoglyph'] },
  { id: 'basic_244', key: 'aging', items: ['fineWrinkle', 'deepWrinkle'] },
];

const FEATURE_MAP: { id: string; key: ItemKey }[] = [
  { id: 'Red', key: 'redness' },
  { id: 'Porphyrin', key: 'porphyrin' },
  { id: 'Pigment', key: 'pigment' },
  { id: 'Grayscale', key: 'brightness' },
  { id: 'Pore', key: 'pore' },
  { id: 'Dermatograin', key: 'dermatoglyph' },
  { id: 'basic_241', key: 'fineWrinkle' },
  { id: 'basic_242', key: 'deepWrinkle' },
];

const REGIONS: { key: RegionKey; group: 'fine' | 'deep'; feature: string }[] = [
  { key: 'TT', group: 'fine', feature: 'basic_241' },
  { key: 'MJ', group: 'fine', feature: 'basic_241' },
  { key: 'BG', group: 'fine', feature: 'basic_241' },
  { key: 'YD', group: 'fine', feature: 'basic_241' },
  { key: 'YW', group: 'fine', feature: 'basic_241' },
  { key: 'LG', group: 'deep', feature: 'basic_242' },
  { key: 'FL', group: 'deep', feature: 'basic_242' },
  { key: 'QJ', group: 'deep', feature: 'basic_242' },
];

// render mappings flag → 우리 텍스처 키
const TEXTURE_FLAG: Record<string, TextureKey> = {
  rgb: 'natural',
  rgb_cool: 'cool',
  red2_heat: 'red-heat',
  brown_heat: 'brown-heat',
  uv: 'uv',
};

type MetricSpec = { id: string; label: string; tabletOnly?: boolean };
// 화이트리스트 — label 은 여기서 새로 붙인다(원본 title 미사용). 사전에 없는 result 는 버린다.
const METRICS: Partial<Record<ItemKey, MetricSpec[]>> = {
  redness: [
    { id: 'red_max', label: '최댓값', tabletOnly: true },
    { id: 'red_peak', label: '대표값', tabletOnly: true },
  ],
  porphyrin: [
    { id: 'porphyrin_count', label: '개수' },
    { id: 'porphyrin_percentage', label: '얼굴 중 비율' },
  ],
  pigment: [
    { id: 'pigment_max', label: '최댓값', tabletOnly: true },
    { id: 'pigment_strength', label: '강도', tabletOnly: true },
  ],
  brightness: [
    { id: 'grayscale_peak', label: '대표값', tabletOnly: true },
    { id: 'grayscale_strength', label: '강도', tabletOnly: true },
  ],
  pore: [
    { id: 'pore_big_ratio', label: '넓어진 모공 비율' },
    { id: 'pore_area_peak', label: '가장 많은 모공 크기' },
    { id: 'pore_deep_ratio', label: '깊은 모공 비율' },
  ],
  dermatoglyph: [{ id: 'dermatograin_deep2_ratio', label: '깊은 골 비율' }],
};

const nullScore = (s: number | null | undefined) => (s == null || s < 0 ? null : s);
const fmt = (n: number, digits = 1) => (Number.isInteger(n) ? n.toLocaleString('ko-KR') : n.toFixed(digits));

function allResults(f: M3dFeature): M3dResult[] {
  return f.measures.flatMap((m) => m.results ?? []);
}

function toMetric(r: M3dResult, spec: MetricSpec): Metric | null {
  if (typeof r.value !== 'number') return null;
  if (r.type === 'ratio') {
    const pct = r.value * 100;
    return { key: r.id, label: spec.label, value: pct, unit: '%', display: `${pct.toFixed(1)}%`, tabletOnly: spec.tabletOnly };
  }
  if (r.type === 'count') {
    return { key: r.id, label: spec.label, value: r.value, unit: '개', display: `${r.value.toLocaleString('ko-KR')}개`, tabletOnly: spec.tabletOnly };
  }
  if (r.unit === 'μm') {
    return { key: r.id, label: spec.label, value: r.value, unit: 'μm', display: `${fmt(r.value)}μm`, tabletOnly: spec.tabletOnly };
  }
  // extremum·intensity — 단위 없는 지수
  return { key: r.id, label: spec.label, value: r.value, unit: '', display: fmt(r.value), tabletOnly: true };
}

function metricsFor(key: ItemKey, f: M3dFeature): Metric[] {
  const results = allResults(f);
  if (key === 'fineWrinkle') {
    // 부위별 wrinkles_*_length 합(선명·깊은 주름 길이는 중복이라 뺀다)
    const lens = results.filter((r) => /^wrinkles_[a-z]+_length$/.test(r.id) && typeof r.value === 'number');
    if (lens.length === 0) return [];
    const sum = lens.reduce((s, r) => s + (r.value as number), 0);
    return [{ key: 'wrinkles_length_sum', label: '주름 길이 합', value: sum, unit: 'mm', display: `${sum.toFixed(1)}mm` }];
  }
  if (key === 'deepWrinkle') {
    // 좌/우 평균 곡률 점수 — id(_left_/_right_) 기준. 원본 title 의 좌/우는 id 와 반대(R C-2) → 태블릿만, ⓘ 안내
    const out: Metric[] = [];
    for (const region of ['lg', 'fl', 'qj'] as const) {
      const left = results.find((r) => r.id === `wrinkles_${region}_left_avg_curvature`);
      const right = results.find((r) => r.id === `wrinkles_${region}_right_avg_curvature`);
      if (left?.score == null || right?.score == null) continue;
      const label = `${REGION_LABEL[region.toUpperCase() as RegionKey]} 깊이 점수(좌/우)`;
      out.push({
        key: `wrinkles_${region}_sides`,
        label,
        value: left.score,
        unit: '',
        display: `좌 ${fmt(left.score)} · 우 ${fmt(right.score)}`,
        tabletOnly: true,
        sided: true,
      });
    }
    return out;
  }
  const specs = METRICS[key] ?? [];
  const out: Metric[] = [];
  for (const spec of specs) {
    const r = results.find((x) => x.id === spec.id);
    const m = r && toMetric(r, spec);
    if (m) out.push(m);
  }
  return out;
}

export interface FromM3dOptions {
  customer: { name: string };
  /** 매니페스트에 실제로 있는 텍스처 */
  availableTextures?: TextureKey[];
}

export function fromM3d(measure: M3dMeasure, render: M3dRender, opts: FromM3dOptions): SkinReport {
  const featureById = new Map(measure.features.map((f) => [f.id, f]));

  const items: SkinItem[] = [];
  for (const { id, key } of FEATURE_MAP) {
    const f = featureById.get(id);
    if (!f) continue;
    const score = nullScore(f.score);
    const metrics = metricsFor(key, f);
    const item: SkinItem = { key, label: ITEM_COPY[key].label, score, grade: gradeOf(score), metrics };
    if (key === 'porphyrin' && score == null) {
      const count = metrics.find((m) => m.key === 'porphyrin_count')?.value ?? null;
      item.scoreNote = porphyrinScoreNote(count);
    }
    items.push(item);
  }

  const categories = CATEGORY_MAP.flatMap(({ id, key, items: its }) => {
    const c = measure.categories.find((x) => x.id === id);
    if (!c) return [];
    const score = nullScore(c.score);
    return [{ key, label: CATEGORY_COPY[key].label, score, grade: gradeOf(score), items: its }];
  });

  const wrinkleRegions: WrinkleRegion[] = [];
  for (const r of REGIONS) {
    const m = featureById.get(r.feature)?.measures.find((x) => x.id === `Wrinkles_${r.key}`);
    if (!m || m.score == null || m.score < 0) continue;
    wrinkleRegions.push({ key: r.key, label: REGION_LABEL[r.key], group: r.group, score: m.score, grade: gradeOf(m.score) });
  }

  let tone: SkinReport['tone'] = null;
  const pantone = featureById.get('Pantone')?.measures[0]?.results ?? [];
  const code = pantone.find((r) => r.id === 'Skin_ID')?.value;
  const name = pantone.find((r) => r.id === 'Skin_description')?.value;
  const rgb = pantone.find((r) => r.id === 'rgb_value')?.value;
  if (typeof code === 'string' && typeof name === 'string' && Array.isArray(rgb) && rgb.length === 3) {
    tone = { code, name, rgb: rgb.map(Number) as [number, number, number] };
  }

  const flags = render.three_dimensional?.mappings?.map((m) => m.flag) ?? [];
  const textures = [...new Set(flags.map((f) => TEXTURE_FLAG[f]).filter((t): t is TextureKey => !!t))].filter(
    (t) => !opts.availableTextures || opts.availableTextures.includes(t),
  );

  return {
    customer: { name: opts.customer.name },
    measuredAt: render.date.replace(/\//g, '-'),
    categories,
    items,
    wrinkleRegions,
    tone,
    textures,
  };
}
