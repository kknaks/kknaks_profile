// 가격 계산 — 차티 stg 와 같게(SPEC §1-4). 화면 ①·② 가 같은 함수를 쓴다.
// stg: features/pricing/utils/currency-format.ts:66-70 · cart-utils.ts:4-16 · utils/price-type.ts

export interface Procedure {
  id: string;
  category: string;
  sub_category: string | null;
  sub_sub_category: string | null;
  name: string;
  price: number;
  original_price: number | null;
  price_type: string | null;
  discount_rate: number | null;
  description: string | null;
  notes: string | null;
}

export interface PricedItem {
  price: number;
  discount: number;
  free: boolean;
  checked: boolean;
}

export const ITEM_DISCOUNT_RATES = [5, 10, 15, 20, 25, 30, 35, 40, 45, 50] as const;
/** 전체 할인율 버튼 — stg constants/currencies.ts:22. 협찬 100% 는 따로 */
export const DISCOUNT_RATES = ITEM_DISCOUNT_RATES;
export const SPONSOR_RATE = 100;

export function itemPrice(item: Pick<PricedItem, 'price' | 'discount' | 'free'>): number {
  if (item.free) return 0;
  const d = item.discount || 0;
  return d > 0 ? Math.round(item.price * (1 - d / 100)) : item.price;
}

export interface CartTotals {
  checkedCount: number;
  totalCount: number;
  total: number;
  totalVat: number;
  final: number;
}

export function calcTotals(cart: PricedItem[], discountRate: number): CartTotals {
  const checked = cart.filter((i) => i.checked !== false);
  const total = checked.reduce((s, i) => s + itemPrice(i), 0);
  const totalVat = Math.round(total * 1.1);
  const final = discountRate > 0 ? Math.round(totalVat * (1 - discountRate / 100)) : totalVat;
  return { checkedCount: checked.length, totalCount: cart.length, total, totalVat, final };
}

export const normalizePriceType = (s?: string | null) => (s ?? '').replace(/\s+/g, '');
export const isFirstVisitEvent = (priceType?: string | null) => normalizePriceType(priceType) === '첫방문이벤트';

/** 시술 목록 정렬 — 가격 내림차순 → 이름 가나다(stg pricing-panel.tsx:21-22) */
export const comparePriceThenName = (a: Procedure, b: Procedure) => b.price - a.price || a.name.localeCompare(b.name, 'ko');

export function buildCategoryPath(p: { category: string; sub_category: string | null; sub_sub_category?: string | null }, depth = 3): string {
  const parts = [p.category];
  if (depth >= 2 && p.sub_category) parts.push(p.sub_category);
  if (depth >= 3 && p.sub_sub_category) parts.push(p.sub_sub_category);
  return parts.join(' › ');
}

export function priceTypeStyle(type?: string | null): string {
  switch (normalizePriceType(type)) {
    case '첫방문이벤트':
      return 'bg-yellow-500 text-white';
    case '이벤트':
      return 'bg-orange-500 text-white';
    default:
      return 'bg-ms-gray-400 text-white';
  }
}

export const won = (n: number) => `${n.toLocaleString('ko-KR')}원`;

/** 재방문이면 첫방문이벤트를 목록·칩·카운트에서 뺀다(stg pricing-panel.tsx:58-66,84-88) */
export function visibleForConsult<T extends { price_type: string | null }>(list: T[], consultType: 'first' | 'revisit' | 'post'): T[] {
  return consultType === 'revisit' ? list.filter((p) => !isFirstVisitEvent(p.price_type)) : list;
}

/** 가격유형 칩 — 가격표에서 뽑아 정규가·이벤트·첫방문이벤트 순(stg pricing-panel.tsx:97-125) */
export function priceTypeChips(list: { price_type: string | null }[]): { key: string; label: string }[] {
  const order = ['정규가', '이벤트', '첫방문이벤트'];
  const seen = new Map<string, string>();
  for (const p of list) {
    const key = normalizePriceType(p.price_type);
    if (!key || seen.has(key)) continue;
    seen.set(key, order.find((o) => normalizePriceType(o) === key) ?? (p.price_type as string));
  }
  return [...seen].map(([key, label]) => ({ key, label })).sort((a, b) => {
    const ai = order.indexOf(a.label);
    const bi = order.indexOf(b.label);
    if (ai !== -1 && bi !== -1) return ai - bi;
    if (ai !== -1) return -1;
    if (bi !== -1) return 1;
    return a.label.localeCompare(b.label, 'ko');
  });
}
