import { existsSync, readFileSync } from 'node:fs';
import path from 'node:path';
import { describe, expect, it } from 'vitest';
import { gradeOf } from '@/domain/grade';
import { fromM3d } from './m3d';
import type { M3dMeasure, M3dRender } from './m3d-types';
import measureSample from './__fixtures__/measure.sample.json';
import renderSample from './__fixtures__/render.sample.json';

const HAN = /[一-鿿]/;

describe('gradeOf — 등급 경계(SPEC §2-1)', () => {
  it.each([
    [84.9, 'mild'],
    [85, 'good'],
    [70, 'mild'],
    [69.9, 'moderate'],
    [60, 'moderate'],
    [59.9, 'severe'],
    [-1, 'none'],
    [null, 'none'],
  ] as const)('%s → %s', (score, grade) => {
    expect(gradeOf(score)).toBe(grade);
  });
});

describe('fromM3d — 가짜 픽스처', () => {
  const report = fromM3d(measureSample as unknown as M3dMeasure, renderSample as M3dRender, { customer: { name: '테스트' } });

  it('대분류 4 · 항목 8 · 부위 8', () => {
    expect(report.categories.map((c) => c.key)).toEqual(['inflammation', 'tone', 'texture', 'aging']);
    expect(report.items.map((i) => i.key)).toEqual([
      'redness',
      'porphyrin',
      'pigment',
      'brightness',
      'pore',
      'dermatoglyph',
      'fineWrinkle',
      'deepWrinkle',
    ]);
    expect(report.wrinkleRegions.map((w) => w.key)).toEqual(['TT', 'MJ', 'BG', 'YD', 'YW', 'LG', 'FL', 'QJ']);
  });

  it('ratio 는 ×100 해서 %', () => {
    const pore = report.items.find((i) => i.key === 'pore')!;
    const big = pore.metrics.find((m) => m.key === 'pore_big_ratio')!;
    expect(big.value).toBeCloseTo(20);
    expect(big.unit).toBe('%');
    expect(big.display).toBe('20.0%');
  });

  it('사전에 없는 result 는 버린다', () => {
    const pore = report.items.find((i) => i.key === 'pore')!;
    expect(pore.metrics.map((m) => m.key)).toEqual(['pore_big_ratio', 'pore_area_peak', 'pore_deep_ratio']);
  });

  it('점수 −1 → null · none, 포르피린 scoreNote', () => {
    const p = report.items.find((i) => i.key === 'porphyrin')!;
    expect(p.score).toBeNull();
    expect(p.grade).toBe('none');
    expect(p.scoreNote).toBe('점수는 나오지 않았어요 · 1,234개 발견');
  });

  it('중국어 title 이 결과 어디에도 없다', () => {
    expect(HAN.test(JSON.stringify(report))).toBe(false);
  });

  it('잔주름 길이 합 · 굵은주름 좌/우는 id 기준 + sided', () => {
    const fine = report.items.find((i) => i.key === 'fineWrinkle')!;
    expect(fine.metrics[0]).toMatchObject({ key: 'wrinkles_length_sum', value: 18.5, unit: 'mm' });
    const deep = report.items.find((i) => i.key === 'deepWrinkle')!;
    expect(deep.metrics[0]).toMatchObject({ key: 'wrinkles_lg_sides', display: '좌 55.5 · 우 60', sided: true, tabletOnly: true });
  });

  it('measuredAt · tone · textures', () => {
    expect(report.measuredAt).toBe('2026-01-02');
    expect(report.tone).toEqual({ code: '1A01', name: '샘플색', rgb: [10, 20, 30] });
    expect(report.textures).toEqual(['cool', 'natural', 'red-heat']);
    const limited = fromM3d(measureSample as unknown as M3dMeasure, renderSample as M3dRender, {
      customer: { name: 'x' },
      availableTextures: ['natural'],
    });
    expect(limited.textures).toEqual(['natural']);
  });

  it('고객 이름은 opts 에서', () => {
    expect(report.customer.name).toBe('테스트');
  });
});

// 준비 스크립트를 돌린 로컬에서만 — 실제 측정값이 §2-2 숫자와 같은지
const REAL = path.resolve(__dirname, '../../../public/m3d/report');
describe.skipIf(!existsSync(path.join(REAL, 'measure.json')))('fromM3d — 실제 public/m3d/report', () => {
  const measure = JSON.parse(readFileSync(path.join(REAL, 'measure.json'), 'utf8'));
  const render = JSON.parse(readFileSync(path.join(REAL, 'render.json'), 'utf8'));
  const report = fromM3d(measure, render, { customer: { name: '이건학' } });

  it('대분류 76 · 68 · 71.2 · 68.3', () => {
    expect(report.categories.map((c) => c.score)).toEqual([76, 68, 71.2, 68.3]);
  });
  it('항목 점수 · 포르피린 5,470개', () => {
    const s = Object.fromEntries(report.items.map((i) => [i.key, i.score]));
    expect(s).toEqual({
      redness: 76,
      porphyrin: null,
      pigment: 73,
      brightness: 67,
      pore: 68.8,
      dermatoglyph: 82.9,
      fineWrinkle: 83.8,
      deepWrinkle: 65.6,
    });
    const p = report.items.find((i) => i.key === 'porphyrin')!;
    expect(p.metrics.map((m) => m.display)).toEqual(['5,470개', '30.6%']);
  });
  it('부위 8', () => {
    expect(Object.fromEntries(report.wrinkleRegions.map((w) => [w.key, w.score]))).toEqual({
      TT: 92.8,
      MJ: 88.3,
      BG: 100,
      YD: 79.5,
      YW: 90.7,
      LG: 61.4,
      FL: 80.7,
      QJ: 83.8,
    });
  });
  it('피부톤 3R11 아몬드색 · 측정일 · 한자 없음', () => {
    expect(report.tone).toEqual({ code: '3R11', name: '아몬드색', rgb: [155, 108, 76] });
    expect(report.measuredAt).toBe('2026-10-16');
    expect(HAN.test(JSON.stringify(report))).toBe(false);
  });
  it('모공 측정치', () => {
    const pore = report.items.find((i) => i.key === 'pore')!;
    expect(pore.metrics.map((m) => m.display)).toEqual(['15.2%', '450μm', '10.6%']);
  });
});
