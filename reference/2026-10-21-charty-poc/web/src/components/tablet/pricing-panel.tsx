'use client';

import { useMemo } from 'react';
import pricing from '@/data/mock/pricing.json';
import { comparePriceThenName, normalizePriceType, priceTypeChips, visibleForConsult, type Procedure } from '@/domain/pricing';
import { useSessionStore } from '@/stores/session-store';
import { Cart } from './cart';
import { CartSummary } from './cart-summary';
import { ProcedureList } from './procedure-list';

export const PROCEDURES = pricing.procedures as Procedure[];

/** 시술 가격 패널 440 — 목록 + 선택 시술(stg pricing-panel.tsx:199-259). 「감지됨」 대신 「추천」, 통화 선택 없음(KRW 고정) */
export function PricingPanel({ recommendedIds }: { recommendedIds: string[] }) {
  const consultType = useSessionStore((s) => s.session.consultType);
  const ui = useSessionStore((s) => s.ui);

  const all = useMemo(() => visibleForConsult(PROCEDURES, consultType), [consultType]);
  const recommended = useMemo(() => all.filter((p) => recommendedIds.includes(p.id)), [all, recommendedIds]);

  const matched = useMemo(() => [...(ui.showAll ? all : recommended)].sort(comparePriceThenName), [ui.showAll, all, recommended]);
  const categories = useMemo(() => [...new Set(matched.map((p) => p.category))].sort(), [matched]);
  const chips = useMemo(() => priceTypeChips(all), [all]);

  const display = useMemo(() => {
    if (ui.searchQuery.trim()) {
      const q = ui.searchQuery.toLowerCase();
      return all.filter((p) => `${p.name} ${p.category}`.toLowerCase().includes(q)).sort(comparePriceThenName);
    }
    let r = matched;
    if (ui.categoryFilter) r = r.filter((p) => p.category === ui.categoryFilter);
    if (ui.priceTypeFilter) r = r.filter((p) => normalizePriceType(p.price_type) === ui.priceTypeFilter);
    return r;
  }, [ui.searchQuery, ui.categoryFilter, ui.priceTypeFilter, all, matched]);

  return (
    <div className="flex h-full w-[440px] shrink-0 flex-col bg-white" data-testid="pricing-panel">
      <div className="flex h-10 shrink-0 items-center gap-2 border-b border-ms-gray-300 px-4">
        <span className="text-typo-heading-sm-500 text-ms-black">시술 가격</span>
        <span className="rounded-full bg-primary-100 px-2 py-0.5 text-typo-caption-md-500 text-primary" data-testid="matched-count">
          {matched.length}
        </span>
      </div>
      <div className="flex min-h-0 flex-1 overflow-hidden">
        <ProcedureList procedures={display} categories={categories} priceTypeChips={chips} recommendCount={recommended.length} totalCount={all.length} />
        <Cart>
          <CartSummary />
        </Cart>
      </div>
    </div>
  );
}
