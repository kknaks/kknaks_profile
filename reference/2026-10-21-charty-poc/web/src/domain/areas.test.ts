import { existsSync, readFileSync } from 'node:fs';
import path from 'node:path';
import { describe, expect, it } from 'vitest';
import { fromM3d } from '@/data/adapters/m3d';
import type { M3dMeasure, M3dRender } from '@/data/adapters/m3d-types';
import measureSample from '@/data/adapters/__fixtures__/measure.sample.json';
import renderSample from '@/data/adapters/__fixtures__/render.sample.json';
import { FILTER_ORDER, type FilterKey } from './filters';
import { AREA_ORDER, areaCards, type AreaKey } from './areas';

const REAL = path.resolve(__dirname, '../../public/m3d/report');
const scoreGrade = (cards: ReturnType<typeof areaCards>) => Object.fromEntries(cards.map((c) => [c.key, [c.score, c.grade]]));
const keysWhere = (cards: ReturnType<typeof areaCards>, f: (c: (typeof cards)[number]) => boolean) =>
  cards.filter(f).map((c) => c.key).sort();

describe('R-1 areaCards — 손으로 만든 픽스처(최솟값 · −1 제외)', () => {
  const report = fromM3d(measureSample as unknown as M3dMeasure, renderSample as M3dRender, { customer: { name: '테스트' } });
  const cards = areaCards(report, { filter: 'natural', focusItem: null });
  it('대표 점수 · 등급', () => {
    expect(scoreGrade(cards)).toEqual({
      forehead: [90, 'good'],
      eye: [50, 'severe'],
      nasolabial: [70, 'mild'],
      cheek: [60, 'moderate'],
      poreTexture: [59.9, 'severe'],
      sebum: [null, 'none'],
    });
  });
  it('칸 순서 L1–L3 · R1–R3', () => {
    expect(cards.map((c) => c.slot)).toEqual(['L1', 'L2', 'L3', 'R1', 'R2', 'R3']);
    expect(AREA_ORDER).toEqual(['forehead', 'eye', 'nasolabial', 'sebum', 'cheek', 'poreTexture']);
  });
  it('측정 줄 — 대표 먼저 · 나머지 오름차순', () => {
    expect(cards.find((c) => c.key === 'eye')!.measures.map((m) => m.label)).toEqual(['눈물고랑', '눈밑', '눈가']);
  });
  it('측정 JSON 없음 → 6장 모두 점수 없음 · 흐림', () => {
    const empty = areaCards(null, { filter: 'natural', focusItem: null });
    expect(empty.every((c) => c.score == null && c.grade === 'none' && c.state === 'dim' && c.chips.length > 0)).toBe(true);
  });
});

describe.skipIf(!existsSync(path.join(REAL, 'measure.json')))('실제 측정값(SPEC §2-2 · §2-3)', () => {
  const report = fromM3d(
    JSON.parse(readFileSync(path.join(REAL, 'measure.json'), 'utf8')),
    JSON.parse(readFileSync(path.join(REAL, 'render.json'), 'utf8')),
    { customer: { name: '이건학' } },
  );

  it('R-1 대표 점수 · 등급', () => {
    const cards = areaCards(report, { filter: 'natural', focusItem: null });
    expect(scoreGrade(cards)).toEqual({
      forehead: [88.3, 'good'],
      eye: [61.4, 'moderate'],
      nasolabial: [80.7, 'mild'],
      cheek: [67, 'moderate'],
      poreTexture: [68.8, 'moderate'],
      sebum: [null, 'none'],
    });
    const sebum = cards.find((c) => c.key === 'sebum')!;
    expect(sebum.count).toBe(5470);
  });

  // §2-3 마지막 표
  const TABLE: Record<FilterKey, { strong: AreaKey[]; match: AreaKey[] }> = {
    natural: { strong: ['eye', 'nasolabial', 'cheek', 'poreTexture'], match: [] },
    fineWrinkle: { strong: ['eye'], match: ['forehead', 'eye'] },
    deepWrinkle: { strong: ['eye', 'nasolabial'], match: ['eye', 'nasolabial'] },
    pore: { strong: ['poreTexture'], match: ['poreTexture'] },
    redness: { strong: ['cheek'], match: ['cheek'] },
    pigment: { strong: ['cheek'], match: ['cheek'] },
    porphyrin: { strong: [], match: ['sebum'] },
  };
  it.each(FILTER_ORDER)('R-2 필터 %s → strong · dim · match', (filter) => {
    const cards = areaCards(report, { filter, focusItem: null });
    const want = TABLE[filter];
    expect(keysWhere(cards, (c) => c.state === 'strong')).toEqual([...want.strong].sort());
    expect(keysWhere(cards, (c) => c.state === 'dim')).toEqual(AREA_ORDER.filter((k) => !want.strong.includes(k)).sort());
    expect(keysWhere(cards, (c) => c.match)).toEqual([...want.match].sort());
  });

  it.each(FILTER_ORDER)('U-2 카드를 고르면 그 카드만 strong(필터 %s · 추천 불필요 카드도)', (filter) => {
    for (const k of AREA_ORDER) {
      const cards = areaCards(report, { filter, focusItem: null }, k);
      expect(keysWhere(cards, (c) => c.state === 'strong')).toEqual([k]);
      expect(keysWhere(cards, (c) => c.selected)).toEqual([k]);
    }
  });

  it.each(FILTER_ORDER)('R-3 focusItem 이 필터보다 우선(필터 %s)', (filter) => {
    expect(keysWhere(areaCards(report, { filter, focusItem: 'dermatoglyph' }), (c) => c.state === 'strong')).toEqual(['poreTexture']);
    expect(keysWhere(areaCards(report, { filter, focusItem: 'brightness' }), (c) => c.state === 'strong')).toEqual(['cheek']);
  });
});
