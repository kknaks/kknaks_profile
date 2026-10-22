// 체크리스트 키워드 감지 — 차티는 녹취 텍스트에 돌리고, 목업은 목 상담 텍스트에 같은 규칙을 돌린다
// (stg consultation-checklist.tsx:654-747 의 감지 규칙을 같은 결과가 나오게 새로 짰다)
import { GUIDE_CHECKS, PROCEDURE_CHECKS, STATIC_CHECKS, TEMPLATE_CHECKS } from '@/data/mock/checklist';
import type { CartItem, ConsultType } from './session';

export function activeDisclosures(cart: Pick<CartItem, 'name' | 'category'>[]) {
  if (cart.length === 0) return [];
  const cartText = cart.map((c) => `${c.name} ${c.category}`).join(' ').toLowerCase();
  return Object.values(PROCEDURE_CHECKS).filter((d) => d.keywords.some((kw) => cartText.includes(kw.toLowerCase())));
}

export function detectChecks(text: string, template: ConsultType, cart: Pick<CartItem, 'name' | 'category'>[]): string[] {
  const t = text.toLowerCase();
  const out: string[] = [];
  for (const c of STATIC_CHECKS) if (c.keywords.some((kw) => t.includes(kw))) out.push(`s-${c.id}`);
  for (const c of TEMPLATE_CHECKS[template] ?? []) if (c.keywords.some((kw) => t.includes(kw))) out.push(`t-${c.id}`);
  for (const c of GUIDE_CHECKS) if (c.keywords.some((kw) => t.includes(kw))) out.push(`n-${c.id}`);
  for (const d of activeDisclosures(cart)) {
    for (const item of d.items) {
      const words = item.label.replace(/[()/]/g, ' ').split(/\s+/).filter((w) => w.length >= 1);
      if (words.some((w) => t.includes(w.toLowerCase())) || item.detectWords?.some((w) => t.includes(w))) out.push(`${d.label}-${item.id}`);
    }
  }
  return out;
}
