// 화면 모델 — 화면 코드는 이 타입만 안다(SPEC §5-2). 원본(M3D) 타입은 src/data 밖으로 나가지 않는다.

export type Grade = 'good' | 'mild' | 'moderate' | 'severe' | 'none';
export type CategoryKey = 'inflammation' | 'tone' | 'texture' | 'aging';
export type ItemKey =
  | 'redness'
  | 'porphyrin'
  | 'pigment'
  | 'brightness'
  | 'pore'
  | 'dermatoglyph'
  | 'fineWrinkle'
  | 'deepWrinkle';
export type RegionKey = 'TT' | 'MJ' | 'BG' | 'YD' | 'YW' | 'LG' | 'FL' | 'QJ';
export type TextureKey = 'natural' | 'cool' | 'red-heat' | 'brown-heat' | 'uv';
export type OverlayKey = 'fine-wrinkle' | 'deep-wrinkle' | 'pore';

export interface Metric {
  key: string;
  label: string;
  value: number;
  unit: '' | '%' | 'μm' | 'mm' | '개';
  display: string;
  /** 단위 없는 지수(extremum·intensity) — 화면 ①에는 안 쓰고 태블릿만 */
  tabletOnly?: boolean;
  /** 좌/우 값 — 원본 좌우 표기가 id 와 반대라 태블릿에서 ⓘ 안내를 붙인다(SPEC §5-4) */
  sided?: boolean;
}

export interface SkinCategory {
  key: CategoryKey;
  label: string;
  score: number | null;
  grade: Grade;
  items: ItemKey[];
}

export interface SkinItem {
  key: ItemKey;
  label: string;
  score: number | null;
  grade: Grade;
  scoreNote?: string;
  metrics: Metric[];
}

export interface WrinkleRegion {
  key: RegionKey;
  label: string;
  group: 'fine' | 'deep';
  score: number;
  grade: Grade;
}

export interface SkinReport {
  customer: { name: string };
  measuredAt: string;
  categories: SkinCategory[];
  items: SkinItem[];
  wrinkleRegions: WrinkleRegion[];
  tone: { name: string; code: string; rgb: [number, number, number] } | null;
  textures: TextureKey[];
}

export interface SkinReportSource {
  load(): Promise<SkinReport>;
}
