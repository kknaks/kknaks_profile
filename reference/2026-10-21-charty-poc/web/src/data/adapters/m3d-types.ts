// M3D 원본 응답 형태 — src/data 밖으로 내보내지 않는다(SPEC §5-1).
// 필요한 필드만 적는다. 원본 title 은 중국어 미번역이 섞여 있어 화면에서 쓰지 않는다.

export interface M3dResult {
  id: string;
  title?: string;
  type: string;
  value: unknown;
  score?: number | null;
  unit?: string | null;
}

export interface M3dMeasureItem {
  id: string;
  title?: string;
  score: number;
  results: M3dResult[];
}

export interface M3dFeature {
  id: string;
  name?: string;
  score: number;
  level?: number;
  measures: M3dMeasureItem[];
}

export interface M3dCategory {
  id: string;
  name?: string;
  features: string[];
  score: number;
  level?: number;
}

export interface M3dMeasure {
  categories: M3dCategory[];
  features: M3dFeature[];
}

export interface M3dRender {
  date: string;
  atlas?: { flag: string; name?: string; type?: number }[];
  three_dimensional?: { mappings?: { flag: string; title?: string }[] };
}
