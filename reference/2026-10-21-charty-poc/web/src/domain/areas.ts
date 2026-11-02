// 화면 ① 부위 카드 규칙(SPEC §2). 목업용 매핑 · 의학적 근거 아님.
// 순수 함수만 — React 없음. 태블릿 추천(recommend-rules.ts)과 서로 import 하지 않는다(§5).
import hubRefs from '@/data/hub/hub-refs.json';
import { ITEM_COPY, REGION_LABEL } from '@/content/copy';
import { FILTERS, type FilterKey } from './filters';
import { gradeOf } from './grade';
import type { Grade, ItemKey, RegionKey, SkinReport } from './skin-report';

export type AreaKey = 'forehead' | 'eye' | 'nasolabial' | 'cheek' | 'poreTexture' | 'sebum';
export type AreaSlot = 'L1' | 'L2' | 'L3' | 'R1' | 'R2' | 'R3';

type AreaSource = { region: RegionKey } | { item: ItemKey };

export interface AreaDef {
  key: AreaKey;
  label: string;
  /** 근거 측정값 — 주름은 부위(wrinkleRegions), 나머지는 항목(items) */
  sources: AreaSource[];
}

export const AREAS: Record<AreaKey, AreaDef> = {
  forehead: { key: 'forehead', label: '이마/미간', sources: [{ region: 'TT' }, { region: 'MJ' }, { region: 'BG' }] },
  eye: { key: 'eye', label: '눈가/눈밑', sources: [{ region: 'YD' }, { region: 'YW' }, { region: 'LG' }] },
  nasolabial: { key: 'nasolabial', label: '팔자/광대', sources: [{ region: 'FL' }, { region: 'QJ' }] },
  cheek: { key: 'cheek', label: '볼/코 주변', sources: [{ item: 'redness' }, { item: 'pigment' }, { item: 'brightness' }] },
  poreTexture: { key: 'poreTexture', label: '모공/피부결', sources: [{ item: 'pore' }, { item: 'dermatoglyph' }] },
  sebum: { key: 'sebum', label: '피지/트러블', sources: [{ item: 'porphyrin' }] },
};

/** §1-2 칸 — 열 안 순서 = 점의 화면 높이 순서(지시선이 엇갈리지 않게) */
export const AREA_LAYOUT: Record<'left' | 'right', AreaKey[]> = {
  left: ['forehead', 'eye', 'nasolabial'],
  right: ['sebum', 'cheek', 'poreTexture'],
};
export const AREA_ORDER: AreaKey[] = [...AREA_LAYOUT.left, ...AREA_LAYOUT.right];

export function areaSlot(key: AreaKey): AreaSlot {
  const li = AREA_LAYOUT.left.indexOf(key);
  return (li >= 0 ? `L${li + 1}` : `R${AREA_LAYOUT.right.indexOf(key) + 1}`) as AreaSlot;
}

/** §2-3 항목 → 카드 */
export const ITEM_AREAS: Record<ItemKey, AreaKey[]> = {
  fineWrinkle: ['forehead', 'eye'],
  deepWrinkle: ['eye', 'nasolabial'],
  pore: ['poreTexture'],
  dermatoglyph: ['poreTexture'],
  redness: ['cheek'],
  pigment: ['cheek'],
  brightness: ['cheek'],
  porphyrin: ['sebum'],
};

export interface AreaChip {
  label: string;
  hubId: string;
  /** 시술 사진 경로(U-3) — 원본이 없어 지금은 비어 있고 자리표시를 그린다. hub-refs.json 칩에 "image" 를 넣으면 쓴다 */
  image?: string;
}

export interface AreaMeasure {
  label: string;
  /** 점수 없음(−1)이면 null */
  score: number | null;
}

export interface AreaCardModel {
  key: AreaKey;
  label: string;
  slot: AreaSlot;
  /** 대표 점수 = 점수 있는 측정값의 최솟값 */
  score: number | null;
  grade: Grade;
  /** 대표 먼저, 나머지 점수 오름차순. 점수 없는 것은 끝 */
  measures: AreaMeasure[];
  /** 점수가 없을 때 개수(피지 속 세균 흔적) */
  count: number | null;
  needed: boolean;
  state: 'strong' | 'dim';
  match: boolean;
  /** 큰 화면에서 카드를 눌러 고름(U-2) — 고르면 그 카드만 strong */
  selected: boolean;
  chips: AreaChip[];
}

const REFS = hubRefs.areas as Record<AreaKey, { problems: string[]; chips: (AreaChip & { problemItems: string[] })[] }>;

export function areaChips(key: AreaKey): AreaChip[] {
  return REFS[key].chips.map(({ label, hubId, image }) => (image ? { label, hubId, image } : { label, hubId }));
}

function measuresOf(def: AreaDef, report: SkinReport | null): { measures: AreaMeasure[]; count: number | null } {
  if (!report) return { measures: [], count: null };
  const measures: AreaMeasure[] = [];
  let count: number | null = null;
  for (const s of def.sources) {
    if ('region' in s) {
      const r = report.wrinkleRegions.find((x) => x.key === s.region);
      if (r) measures.push({ label: REGION_LABEL[s.region], score: r.score });
    } else {
      const it = report.items.find((x) => x.key === s.item);
      if (!it) continue;
      measures.push({ label: ITEM_COPY[s.item].label, score: it.score });
      if (it.score == null) count = it.metrics.find((m) => m.unit === '개')?.value ?? null;
    }
  }
  measures.sort((a, b) => (a.score ?? Infinity) - (b.score ?? Infinity));
  return { measures, count };
}

export interface AreaSessionView {
  filter: FilterKey;
  focusItem: ItemKey | null;
}

/** 지금 강조할 항목 — 화면 ① 기존 규칙 그대로(focusItem 우선) */
export function highlightItem(s: AreaSessionView): ItemKey | null {
  return s.focusItem ?? FILTERS[s.filter].relatedItem;
}

/** selected = 큰 화면에서 고른 카드(있으면 필터 강조보다 우선) */
export function areaCards(report: SkinReport | null, session: AreaSessionView, selected: AreaKey | null = null): AreaCardModel[] {
  const highlight = highlightItem(session);
  const hlAreas = highlight ? ITEM_AREAS[highlight] : null;
  return AREA_ORDER.map((key) => {
    const def = AREAS[key];
    const { measures, count } = measuresOf(def, report);
    const scored = measures.filter((m) => m.score != null && m.score >= 0);
    const score = scored.length ? Math.min(...scored.map((m) => m.score as number)) : null;
    const grade = gradeOf(score);
    const needed = grade === 'mild' || grade === 'moderate' || grade === 'severe';
    const inHighlight = !!hlAreas?.includes(key);
    const state = selected ? (selected === key ? 'strong' : 'dim') : needed && (hlAreas == null || inHighlight) ? 'strong' : 'dim';
    return {
      key,
      label: def.label,
      slot: areaSlot(key),
      score,
      grade,
      measures,
      count,
      needed,
      state,
      match: inHighlight,
      selected: selected === key,
      chips: areaChips(key),
    };
  });
}
