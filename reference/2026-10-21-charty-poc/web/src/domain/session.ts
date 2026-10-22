import type { FilterKey } from './filters';
import type { ItemKey } from './skin-report';

export type ConsultType = 'first' | 'revisit' | 'post';

export interface CartItem {
  id: string;
  procedureId: string;
  name: string;
  category: string;
  subCategory: string | null;
  priceType: string;
  price: number;
  originalPrice: number | null;
  discount: number;
  free: boolean;
  checked: boolean;
}

export interface SessionState {
  sessionId: string;
  consultType: ConsultType;
  filter: FilterKey;
  focusItem: ItemKey | null;
  cameraResetAt: number;
  cart: CartItem[];
  discountRate: number;
  screen: { showPrice: boolean };
}

export function initialSessionState(sessionId: string): SessionState {
  return {
    sessionId,
    consultType: 'first',
    filter: 'natural',
    focusItem: null,
    cameraResetAt: 0,
    cart: [],
    discountRate: 0,
    screen: { showPrice: true },
  };
}

export const CONSULT_TYPE_LABEL: Record<ConsultType, string> = { first: '첫방문', revisit: '재방문', post: '시술후' };
