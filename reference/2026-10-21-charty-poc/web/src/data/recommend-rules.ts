/**
 * 추천 규칙 — 목업용 · 의학적 근거 아님.
 *
 * 분석 결과 → 시술 매핑은 의료 판단이라 확정된 규칙이 아니다. SPEC §3-5 표를 그대로 옮긴
 * 시연용 규칙이며, 실제 상담·처방에 쓰면 안 된다(SPEC §11 정할 것 5 — 기본값 「표대로」).
 */
import type { Procedure } from '@/domain/pricing';
import type { ItemKey, SkinReport } from '@/domain/skin-report';
import taxonomy from '@/data/mock/taxonomy-subset.json';

export type ModalityId = 'M1' | 'M2' | 'M4' | 'M8' | 'M9' | 'M15';

interface Rule {
  id: string;
  /** 점수 정렬에 쓰는 항목 */
  item: ItemKey;
  when: (r: SkinReport) => boolean;
  modalities: ModalityId[];
  reason: string;
  rows: (p: Procedure) => boolean;
}

const item = (r: SkinReport, k: ItemKey) => r.items.find((i) => i.key === k);
const gradeIn = (r: SkinReport, k: ItemKey, gs: string[]) => gs.includes(item(r, k)?.grade ?? 'none');
const MILD_UP = ['mild', 'moderate', 'severe'];
const MOD_UP = ['moderate', 'severe'];
const nameHas = (p: Procedure, words: string[]) => words.some((w) => p.name.includes(w));

export const RULES: Rule[] = [
  {
    id: 'fine-wrinkle',
    item: 'fineWrinkle',
    when: (r) => r.wrinkleRegions.some((w) => w.group === 'fine' && w.score < 85) || gradeIn(r, 'fineWrinkle', MILD_UP),
    modalities: ['M1'],
    reason: '눈밑·눈가 잔주름',
    rows: (p) => p.category === '보톡스' && nameHas(p, ['눈가', '미간', '이마', '3부위 패키지', '풀페이스']),
  },
  {
    id: 'deep-wrinkle',
    item: 'deepWrinkle',
    when: (r) => gradeIn(r, 'deepWrinkle', MOD_UP),
    modalities: ['M9', 'M2'],
    reason: '눈물고랑·팔자 굵은 주름',
    rows: (p) =>
      (p.category === '리프팅' && ['울쎄라', '써마지', '신스킨', '고주파리프팅'].includes(p.sub_category ?? '')) || p.category === '필러',
  },
  {
    id: 'pore',
    item: 'pore',
    when: (r) => gradeIn(r, 'pore', MOD_UP),
    modalities: ['M4', 'M8'],
    reason: '넓어진 모공',
    rows: (p) => (p.category === '스킨케어' && nameHas(p, ['리쥬란 HB', '스킨보톡스'])) || (p.category === '레이저' && p.sub_category === '제네시스'),
  },
  {
    id: 'dull-pigment',
    item: 'brightness',
    when: (r) => gradeIn(r, 'brightness', MOD_UP) || gradeIn(r, 'pigment', MILD_UP),
    modalities: ['M8'],
    reason: '칙칙함·색소',
    rows: (p) => ['피코토닝', '르브란', '올레이저'].includes(p.sub_category ?? ''),
  },
  {
    id: 'redness',
    item: 'redness',
    when: (r) => gradeIn(r, 'redness', MILD_UP),
    modalities: ['M8'],
    reason: '붉은기',
    rows: (p) => p.sub_category === '엑셀V',
  },
  {
    id: 'porphyrin',
    item: 'porphyrin',
    when: (r) => (item(r, 'porphyrin')?.metrics.find((m) => m.key === 'porphyrin_count')?.value ?? 0) >= 3000,
    modalities: ['M15'],
    reason: '피지·트러블 관리',
    rows: (p) => p.sub_category === '수소피부관리',
  },
];

export interface TaxonomyExtracted {
  overview?: string;
  indications?: { primary?: string[]; extended?: string[] };
  contraindications?: { absolute?: string[]; relative?: string[] };
  safety?: { common?: string[]; uncommon?: string[]; serious?: string[] };
  onset_duration?: { onset?: string; duration?: string };
  aftercare?: string[];
  related_techniques?: string[];
}

export interface RecommendChip {
  modality: ModalityId;
  label: string;
  /** 대표 대분류(가격표) — [가격표에서 보기] 가 거르는 값 */
  priceCategory: string;
  reasons: string[];
  extracted: TaxonomyExtracted | null;
}

export interface Recommendation {
  chips: RecommendChip[];
  procedureIds: string[];
}

const PRICE_CATEGORY: Record<ModalityId, string> = {
  M1: '보톡스',
  M2: '필러',
  M4: '스킨케어',
  M8: '레이저',
  M9: '리프팅',
  M15: '스킨케어',
};

const TAX = new Map(
  (taxonomy.modality as { id: string; category: string; extracted: TaxonomyExtracted | null }[]).map((m) => [m.id, m]),
);

export function recommend(report: SkinReport, procedures: Procedure[]): Recommendation {
  const fired = RULES.filter((r) => r.when(report)).sort((a, b) => {
    const sa = item(report, a.item)?.score ?? Infinity;
    const sb = item(report, b.item)?.score ?? Infinity;
    return sa - sb;
  });
  const chips = new Map<ModalityId, RecommendChip>();
  const ids = new Set<string>();
  for (const rule of fired) {
    for (const m of rule.modalities) {
      const chip = chips.get(m);
      if (chip) {
        if (!chip.reasons.includes(rule.reason)) chip.reasons.push(rule.reason);
      } else {
        const t = TAX.get(m);
        chips.set(m, { modality: m, label: t?.category ?? m, priceCategory: PRICE_CATEGORY[m], reasons: [rule.reason], extracted: t?.extracted ?? null });
      }
    }
    for (const p of procedures) if (rule.rows(p)) ids.add(p.id);
  }
  return { chips: [...chips.values()], procedureIds: procedures.filter((p) => ids.has(p.id)).map((p) => p.id) };
}
