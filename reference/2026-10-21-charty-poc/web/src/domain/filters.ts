import type { ItemKey, OverlayKey, TextureKey } from './skin-report';

export type FilterKey = 'natural' | 'fineWrinkle' | 'deepWrinkle' | 'pore' | 'redness' | 'pigment' | 'porphyrin';

export interface FilterDef {
  key: FilterKey;
  label: string;
  texture: TextureKey;
  overlay: OverlayKey | null;
  overlayColor: string | null;
  relatedItem: ItemKey | null;
  legend: string | null;
}

// SPEC §6-5. 오버레이 필터의 바탕은 원본 분석 atlas 가 쓰는 냉광(rgb_cool).
export const FILTERS: Record<FilterKey, FilterDef> = {
  natural: { key: 'natural', label: '자연광', texture: 'natural', overlay: null, overlayColor: null, relatedItem: null, legend: null },
  fineWrinkle: {
    key: 'fineWrinkle',
    label: '잔주름',
    texture: 'cool',
    overlay: 'fine-wrinkle',
    overlayColor: '#a290ff',
    relatedItem: 'fineWrinkle',
    legend: '보라 선 = 찾아낸 잔주름',
  },
  deepWrinkle: {
    key: 'deepWrinkle',
    label: '굵은 주름',
    texture: 'cool',
    overlay: 'deep-wrinkle',
    overlayColor: '#fd9400',
    relatedItem: 'deepWrinkle',
    legend: '주황 선 = 깊게 팬 주름',
  },
  pore: { key: 'pore', label: '모공', texture: 'cool', overlay: 'pore', overlayColor: '#ffffff', relatedItem: 'pore', legend: '흰 점 = 넓어진 모공' },
  redness: { key: 'redness', label: '붉은기', texture: 'red-heat', overlay: null, overlayColor: null, relatedItem: 'redness', legend: '붉을수록 붉은기가 강한 곳' },
  pigment: { key: 'pigment', label: '색소', texture: 'brown-heat', overlay: null, overlayColor: null, relatedItem: 'pigment', legend: '진할수록 색소가 많은 곳' },
  porphyrin: {
    key: 'porphyrin',
    label: '피지 세균',
    texture: 'uv',
    overlay: null,
    overlayColor: null,
    relatedItem: 'porphyrin',
    legend: '주황·붉게 빛나는 점 = 피지 속 세균 흔적',
  },
};

export const FILTER_ORDER: FilterKey[] = ['natural', 'fineWrinkle', 'deepWrinkle', 'pore', 'redness', 'pigment', 'porphyrin'];

/** 항목 → 그 항목을 보여 주는 필터(피부 분석 탭에서 항목을 고르면 이 필터로 바꾼다) */
export function filterForItem(item: ItemKey): FilterKey | null {
  return FILTER_ORDER.find((k) => FILTERS[k].relatedItem === item) ?? null;
}
