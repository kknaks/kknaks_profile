import { describe, expect, it } from 'vitest';
import pricing from '@/data/mock/pricing.json';
import { calcTotals, isFirstVisitEvent, itemPrice, normalizePriceType, type Procedure } from './pricing';

const P = pricing.procedures as Procedure[];
const byName = (n: string) => P.find((p) => p.name === n)!;
const line = (name: string, extra: Partial<{ discount: number; free: boolean; checked: boolean }> = {}) => ({
  price: byName(name).price,
  discount: 0,
  free: false,
  checked: true,
  ...extra,
});

describe('가격 계산(SPEC §1-4 · AC-14)', () => {
  const cart = [line('눈가 보톡스'), line('리쥬란 HB 1회', { free: true }), line('울쎄라 하안면', { discount: 10 })];

  it('항목가', () => {
    expect(cart.map(itemPrice)).toEqual([120000, 0, 1980000]);
  });
  it('합계 · VAT · 전체 할인 10%', () => {
    expect(calcTotals(cart, 0)).toMatchObject({ total: 2100000, totalVat: 2310000, final: 2310000, checkedCount: 3 });
    expect(calcTotals(cart, 10).final).toBe(2079000);
  });
  it('협찬 100% = 0원', () => {
    expect(calcTotals(cart, 100).final).toBe(0);
  });
  it('체크 해제는 합계에서 빠진다', () => {
    const c2 = [...cart.slice(0, 2), { ...cart[2], checked: false }];
    expect(calcTotals(c2, 0)).toMatchObject({ total: 120000, checkedCount: 2, totalCount: 3 });
  });
  it('항목 할인 반올림(stg 와 같게 Math.round)', () => {
    expect(itemPrice({ price: 99999, discount: 15, free: false })).toBe(Math.round(99999 * 0.85));
  });
});

describe('가격표 · 첫방문이벤트 규칙', () => {
  it('가격표 48건', () => {
    expect(P).toHaveLength(48);
  });
  it('공백 변형도 첫방문이벤트로 본다(가짜 값)', () => {
    expect(isFirstVisitEvent('첫방문이벤트')).toBe(true);
    expect(isFirstVisitEvent('첫방문 이벤트')).toBe(true);
    expect(isFirstVisitEvent('첫 방문 이벤트')).toBe(true);
    expect(isFirstVisitEvent('이벤트')).toBe(false);
    expect(normalizePriceType(' 정규 가 ')).toBe('정규가');
  });
  it('데모 가격표에는 첫방문이벤트 행이 0건이다(데이터상)', () => {
    expect(P.filter((p) => isFirstVisitEvent(p.price_type))).toHaveLength(0);
  });
});

describe('재방문 숨김(가짜 행 — 데모 가격표엔 0건)', () => {
  const fake = [
    { name: 'a', price_type: '정규가' },
    { name: 'b', price_type: '첫방문 이벤트' },
    { name: 'c', price_type: '이벤트' },
  ];
  it('재방문이면 행·칩에서 빠진다', async () => {
    const { visibleForConsult, priceTypeChips } = await import('./pricing');
    expect(visibleForConsult(fake, 'first').map((p) => p.name)).toEqual(['a', 'b', 'c']);
    expect(visibleForConsult(fake, 'revisit').map((p) => p.name)).toEqual(['a', 'c']);
    expect(priceTypeChips(fake).map((c) => c.label)).toEqual(['정규가', '이벤트', '첫방문이벤트']);
    expect(priceTypeChips(visibleForConsult(fake, 'revisit')).map((c) => c.label)).toEqual(['정규가', '이벤트']);
  });
});
