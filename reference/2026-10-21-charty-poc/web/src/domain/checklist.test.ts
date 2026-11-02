import { describe, expect, it } from 'vitest';
import { TRANSCRIPT_TEXT } from '@/data/mock/transcript';
import { activeDisclosures, detectChecks } from './checklist';

describe('체크리스트 초기 체크 — 목 상담 텍스트 키워드', () => {
  it('필수 확인 중 고민·희망시술·예산·알레르기·복용약물·통증·시술이력이 잡힌다', () => {
    const ids = detectChecks(TRANSCRIPT_TEXT, 'first', []);
    expect(ids).toEqual(expect.arrayContaining(['s-complaint', 's-desired', 's-budget', 's-allergy', 's-medication', 's-pain', 's-past_procedure']));
  });
  it('카트에 보톡스가 있으면 시술별 체크가 켜진다', () => {
    const cart = [{ name: '눈가 보톡스', category: '보톡스' }];
    expect(activeDisclosures(cart).map((d) => d.label)).toContain('보톡스');
    expect(activeDisclosures([])).toEqual([]);
  });
});
