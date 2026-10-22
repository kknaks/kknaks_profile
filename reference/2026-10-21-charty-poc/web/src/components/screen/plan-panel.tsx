'use client';

import { Badge, Card } from '@medisolve-ai/medikit';
import { useTween } from '@/components/common/use-tween';
import { COPY } from '@/content/copy';
import { calcTotals, itemPrice } from '@/domain/pricing';
import type { CartItem } from '@/domain/session';

const krw = (n: number) => n.toLocaleString('ko-KR');

function Money({ value, className, testId }: { value: number; className?: string; testId?: string }) {
  const v = useTween(value);
  return (
    <span className={`tabular-nums ${className ?? ''}`} data-testid={testId} data-value={value}>
      {krw(v)}
    </span>
  );
}

interface PlanPanelProps {
  cart: CartItem[];
  discountRate: number;
  showPrice: boolean;
}

/** D 오늘의 시술 플랜 — 체크된 항목만, 계산은 공통 함수(SPEC §1-4) */
export function PlanPanel({ cart, discountRate, showPrice }: PlanPanelProps) {
  const rows = cart.filter((c) => c.checked !== false);
  const totals = calcTotals(cart, discountRate);


  return (
    <Card padding="md" className="h-full min-h-0 gap-2" data-testid="screen-plan" data-show-price={showPrice}>
      <h2 className="text-typo-title-sm-600 text-ms-black">오늘의 시술 플랜</h2>
      {rows.length === 0 ? (
        <div className="flex flex-1 items-center justify-center">
          <p className="text-typo-title-sm-500 text-ms-gray-600" data-testid="plan-empty">
            {COPY.cartEmpty}
          </p>
        </div>
      ) : (
        <>
          <ul className="min-h-0 flex-1 overflow-y-auto">
            {rows.map((r) => {
              const applied = itemPrice(r);
              const hasCut = r.free || (r.discount || 0) > 0;
              return (
                <li
                  key={r.id}
                  data-testid="plan-row"
                  data-name={r.name}
                  // key=카트 행 id 라 새 행만 새로 붙는다 → 붙을 때 한 번 1.5초 하이라이트(CSS animation)
                  className="row-highlight flex items-center gap-3 border-b border-ms-gray-200 py-1.5"
                >
                  <span className="flex-1 truncate text-typo-heading-md-600 text-ms-black">{r.name}</span>
                  {r.free ? (
                    <Badge variant="primary" className="text-typo-heading-md-500">무료</Badge>
                  ) : (
                    <Badge variant="neutral" className="text-typo-heading-md-500">{r.priceType || '정규가'}</Badge>
                  )}
                  {!r.free && (r.discount || 0) > 0 && (
                    <Badge variant="danger" className="text-typo-heading-md-500">{r.discount}%</Badge>
                  )}
                  {showPrice && (
                    <span className="flex w-[260px] shrink-0 items-baseline justify-end gap-2">
                      {hasCut && <span className="text-typo-heading-md-400 text-ms-gray-600 line-through">{krw(r.price)}</span>}
                      <Money value={applied} className="text-typo-title-sm-600 text-ms-black" testId="plan-row-price" />
                      <span className="text-typo-heading-md-400 text-ms-gray-700">원</span>
                    </span>
                  )}
                </li>
              );
            })}
          </ul>
          {showPrice ? (
            <div className="flex items-end justify-between border-t border-ms-gray-300 pt-2" data-testid="plan-totals">
              <div className="text-typo-heading-md-400 text-ms-gray-700">
                <p>
                  합계 VAT 별도 <Money value={totals.total} className="text-ms-black" testId="plan-total" />원 · VAT 포함{' '}
                  <Money value={totals.totalVat} className="text-ms-black" testId="plan-total-vat" />원
                </p>
                {discountRate > 0 && (
                  <p className="text-primary" data-testid="plan-discount">
                    {discountRate === 100 ? '협찬 (100% 할인)' : `전체 ${discountRate}% 할인`}
                  </p>
                )}
              </div>
              <p className="flex items-baseline gap-2">
                <span className="text-typo-title-sm-600 text-ms-gray-800">최종</span>
                <Money value={totals.final} className="text-typo-headline-lg-600 text-primary" testId="plan-final" />
                <span className="text-typo-title-sm-600 text-ms-gray-800">원</span>
              </p>
            </div>
          ) : (
            <p className="border-t border-ms-gray-300 pt-2 text-right text-typo-title-sm-500 text-ms-gray-600" data-testid="plan-price-hidden">
              {COPY.priceHidden}
            </p>
          )}
        </>
      )}
    </Card>
  );
}
