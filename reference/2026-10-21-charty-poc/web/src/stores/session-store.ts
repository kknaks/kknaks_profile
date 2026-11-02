'use client';

import { create } from 'zustand';
import { filterForItem, type FilterKey } from '@/domain/filters';
import { isFirstVisitEvent, type Procedure } from '@/domain/pricing';
import { initialSessionState, type CartItem, type ConsultType, type SessionState } from '@/domain/session';
import type { ItemKey } from '@/domain/skin-report';

// 태블릿이 상태의 주인(SPEC §4-2). session 은 큰 화면으로 스냅샷째 보내고, ui 는 태블릿에만 남는다.

export type TabletTab = 'analysis' | 'checklist' | 'chart' | 'raw';

export interface TabletUi {
  tab: TabletTab;
  /** 가격 목록 보기 — false = 「추천」, true = 「전체」 */
  showAll: boolean;
  categoryFilter: string | null;
  priceTypeFilter: string | null;
  searchQuery: string;
  checklist: string[];
  checklistAuto: string[];
  chartOverride: string | null;
}

const initialUi = (): TabletUi => ({
  tab: 'analysis',
  showAll: false,
  categoryFilter: null,
  priceTypeFilter: null,
  searchQuery: '',
  checklist: [],
  checklistAuto: [],
  chartOverride: null,
});

const newId = () => (typeof crypto !== 'undefined' && 'randomUUID' in crypto ? crypto.randomUUID() : `${Date.now()}-${Math.random()}`);

interface Actions {
  addToCart: (p: Procedure) => void;
  removeFromCart: (id: string) => void;
  toggleFree: (id: string) => void;
  toggleChecked: (id: string) => void;
  toggleAllChecked: () => void;
  setItemDiscount: (id: string, discount: number) => void;
  setDiscountRate: (rate: number) => void;
  clearCart: () => void;
  setFilter: (f: FilterKey) => void;
  toggleFocusItem: (item: ItemKey) => void;
  resetCamera: () => void;
  setConsultType: (t: ConsultType) => void;
  setShowPrice: (on: boolean) => void;
  resetSession: () => void;
  setUi: (patch: Partial<TabletUi>) => void;
  hydrate: (session: SessionState, seq: number) => void;
}

export interface TabletStore extends Actions {
  session: SessionState;
  /** 스냅샷 번호 — session 이 바뀔 때마다 1 씩 */
  seq: number;
  ui: TabletUi;
}

export const useSessionStore = create<TabletStore>()((set) => {
  const patchSession = (fn: (s: SessionState) => Partial<SessionState>) =>
    set((st) => ({ session: { ...st.session, ...fn(st.session) }, seq: st.seq + 1 }));
  const mapCart = (id: string, fn: (c: CartItem) => CartItem) => patchSession((s) => ({ cart: s.cart.map((c) => (c.id === id ? fn(c) : c)) }));

  return {
    session: initialSessionState(newId()),
    seq: 1,
    ui: initialUi(),

    addToCart: (p) =>
      patchSession((s) => ({
        cart: [
          ...s.cart,
          {
            id: newId(),
            procedureId: p.id,
            name: p.name,
            category: p.category,
            subCategory: p.sub_category,
            priceType: p.price_type || '정규가',
            price: p.price,
            originalPrice: p.original_price,
            discount: 0,
            free: false,
            checked: true,
          },
        ],
      })),
    removeFromCart: (id) => patchSession((s) => ({ cart: s.cart.filter((c) => c.id !== id) })),
    toggleFree: (id) => mapCart(id, (c) => ({ ...c, free: !c.free })),
    toggleChecked: (id) => mapCart(id, (c) => ({ ...c, checked: c.checked === false })),
    toggleAllChecked: () =>
      patchSession((s) => {
        const all = s.cart.every((c) => c.checked !== false);
        return { cart: s.cart.map((c) => ({ ...c, checked: !all })) };
      }),
    setItemDiscount: (id, discount) => mapCart(id, (c) => ({ ...c, discount })),
    setDiscountRate: (rate) => patchSession(() => ({ discountRate: rate })),
    // 차티 [전체삭제] 는 할인율도 0 으로(stg cart.tsx:56-66)
    clearCart: () => patchSession(() => ({ cart: [], discountRate: 0 })),
    // 필터를 직접 바꾸면 피부 분석 강조(focusItem)는 비운다 — 필터·C 강조·B 테두리·A2 가 같은 대상을 가리키게(fix1 W-3)
    setFilter: (filter) => patchSession(() => ({ filter, focusItem: null })),
    toggleFocusItem: (item) =>
      patchSession((s) => {
        if (s.focusItem === item) return { focusItem: null };
        return { focusItem: item, filter: filterForItem(item) ?? s.filter };
      }),
    resetCamera: () => patchSession(() => ({ cameraResetAt: Date.now() })),
    // 재방문 전환 시 카트의 첫방문이벤트 항목 자동 제거(stg pricing-panel.tsx:58-66)
    setConsultType: (consultType) =>
      patchSession((s) => ({
        consultType,
        cart: consultType === 'revisit' ? s.cart.filter((c) => !isFirstVisitEvent(c.priceType)) : s.cart,
      })),
    setShowPrice: (on) => patchSession(() => ({ screen: { showPrice: on } })),
    resetSession: () => set((st) => ({ session: initialSessionState(newId()), seq: st.seq + 1, ui: initialUi() })),
    setUi: (patch) => set((st) => ({ ui: { ...st.ui, ...patch } })),
    hydrate: (session, seq) => set({ session, seq }),
  };
});
