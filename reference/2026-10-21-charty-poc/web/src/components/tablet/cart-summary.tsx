'use client';

import { DISCOUNT_RATES, SPONSOR_RATE, calcTotals } from '@/domain/pricing';
import { useSessionStore } from '@/stores/session-store';

/** n/m건 · VAT 별도/포함 · 할인율 버튼 줄 + 협찬 100% · 최종(stg cart-summary.tsx:39-109). 환율 줄 없음 */
export function CartSummary() {
  const cart = useSessionStore((s) => s.session.cart);
  const discountRate = useSessionStore((s) => s.session.discountRate);
  const setDiscountRate = useSessionStore((s) => s.setDiscountRate);
  const t = calcTotals(cart, discountRate);
  const sponsor = discountRate === SPONSOR_RATE;

  return (
    <div className="shrink-0 border-t border-ms-gray-300 bg-ms-gray-100 px-3 py-2" data-testid="cart-summary">
      <div className="mb-1 flex items-baseline justify-between">
        <span className="text-[10px] font-medium text-primary">
          {t.checkedCount}/{t.totalCount}건 선택
        </span>
      </div>
      <div className="flex items-baseline justify-between gap-1">
        <span className="shrink-0 text-[11px] text-slate-500">VAT 별도</span>
        <span className="text-right text-[10px] font-bold text-slate-900" data-testid="tablet-total">
          {t.total.toLocaleString()}원
        </span>
      </div>
      <div className="mt-0.5 flex items-baseline justify-between gap-1">
        <span className="shrink-0 text-[11px] text-slate-500">VAT 포함</span>
        <span className="text-right text-typo-caption-md-600 text-slate-900" data-testid="tablet-total-vat">
          {t.totalVat.toLocaleString()}원
        </span>
      </div>
      <div className="mt-1.5 border-t border-slate-200 pt-1.5">
        <p className="mb-1 text-[10px] text-slate-500">할인율 적용</p>
        <div className="flex flex-wrap gap-1">
          {DISCOUNT_RATES.map((rate) => (
            <button
              key={rate}
              onClick={() => setDiscountRate(discountRate === rate ? 0 : rate)}
              className={`h-8 min-w-[36px] rounded px-1.5 text-[11px] transition-colors ${
                discountRate === rate ? 'bg-primary font-bold text-white' : 'bg-ms-gray-200 text-ms-gray-700 hover:bg-ms-gray-300'
              }`}
              data-testid={`rate-${rate}`}
            >
              {rate}%
            </button>
          ))}
          <button
            onClick={() => setDiscountRate(sponsor ? 0 : SPONSOR_RATE)}
            className={`h-8 min-w-[36px] rounded px-1.5 text-[11px] transition-colors ${
              sponsor ? 'bg-purple-600 font-bold text-white' : 'bg-purple-100 text-purple-600 hover:bg-purple-200'
            }`}
            data-testid="rate-100"
          >
            협찬 100%
          </button>
        </div>
      </div>
      {discountRate > 0 && (
        <div className={`-mx-2 mt-1.5 rounded-b border-t border-slate-200 px-2 pb-1 pt-1.5 ${sponsor ? 'bg-purple-50' : 'bg-blue-50'}`}>
          <div className="flex items-center justify-between">
            <span className={`text-[11px] font-medium ${sponsor ? 'text-purple-600' : 'text-blue-600'}`}>{sponsor ? '협찬 (100% 할인)' : `${discountRate}% 할인`}</span>
            <span className="text-[11px] text-red-500 line-through">{t.totalVat.toLocaleString()}원</span>
          </div>
          <div className="mt-0.5 flex items-baseline justify-between gap-1">
            <span className={`shrink-0 text-[10px] font-bold ${sponsor ? 'text-purple-700' : 'text-blue-700'}`}>최종 (VAT포함)</span>
            <span className={`text-right text-typo-caption-md-400 font-black ${sponsor ? 'text-purple-700' : 'text-blue-700'}`} data-testid="tablet-final">
              {t.final.toLocaleString()}원
            </span>
          </div>
        </div>
      )}
    </div>
  );
}
