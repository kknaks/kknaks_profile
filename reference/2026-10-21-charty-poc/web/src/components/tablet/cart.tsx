'use client';

import { ITEM_DISCOUNT_RATES, buildCategoryPath, itemPrice, priceTypeStyle } from '@/domain/pricing';
import { useSessionStore } from '@/stores/session-store';

/** 선택 시술 — 행 탭 = 체크 토글 · 항목 할인 select · 무료 · 삭제(stg features/pricing/components/cart.tsx:33-198) */
export function Cart({ children }: { children?: React.ReactNode }) {
  const cart = useSessionStore((s) => s.session.cart);
  const removeFromCart = useSessionStore((s) => s.removeFromCart);
  const toggleFree = useSessionStore((s) => s.toggleFree);
  const toggleChecked = useSessionStore((s) => s.toggleChecked);
  const toggleAllChecked = useSessionStore((s) => s.toggleAllChecked);
  const setItemDiscount = useSessionStore((s) => s.setItemDiscount);
  const clearCart = useSessionStore((s) => s.clearCart);
  const checkedCount = cart.filter((c) => c.checked !== false).length;
  const allChecked = cart.length > 0 && checkedCount === cart.length;

  return (
    <div className="flex min-h-0 min-w-0 flex-1 flex-col border-l border-ms-gray-300 bg-white" data-testid="cart">
      <div className="flex h-9 shrink-0 items-center justify-between border-b border-ms-gray-300 px-3">
        <div className="flex items-center gap-1.5">
          <span className="text-typo-heading-sm-500 text-ms-black">선택 시술</span>
          {cart.length > 0 && <span className="rounded-full bg-primary-100 px-2 py-0.5 text-typo-caption-md-500 text-primary">{cart.length}</span>}
        </div>
        {cart.length > 0 && (
          <div className="flex items-center gap-2">
            <button onClick={toggleAllChecked} className={`h-8 text-[11px] font-medium ${allChecked ? 'text-primary' : 'text-ms-gray-500 hover:text-primary'}`}>
              {allChecked ? '전체해제' : '전체선택'}
            </button>
            <button onClick={clearCart} className="h-8 text-[11px] font-medium text-red hover:opacity-80" data-testid="cart-clear">
              전체삭제
            </button>
          </div>
        )}
      </div>

      <div className="custom-scrollbar flex-1 overflow-y-auto">
        {cart.length > 0 ? (
          <div className="divide-y divide-ms-gray-200">
            {cart.map((item) => {
              const isChecked = item.checked !== false;
              const path = buildCategoryPath({ category: item.category, sub_category: item.subCategory }, 2);
              return (
                <div
                  key={item.id}
                  onClick={() => toggleChecked(item.id)}
                  className={`cursor-pointer px-2 py-1.5 transition-colors ${item.free ? 'bg-green-50' : isChecked ? 'bg-primary-100' : ''}`}
                  data-testid="cart-row"
                  data-name={item.name}
                  data-checked={isChecked}
                >
                  <div className="flex items-start justify-between gap-1">
                    <div className="min-w-0 flex-1">
                      <div className="flex items-center gap-1">
                        <span className={`rounded px-1 py-px text-[9px] ${item.free ? 'bg-green-500 text-white' : priceTypeStyle(item.priceType)}`}>
                          {item.free ? '무료' : item.priceType || '정규가'}
                        </span>
                        {!item.free && item.discount > 0 && <span className="rounded bg-red-500 px-1 py-px text-[9px] text-white">{item.discount}%</span>}
                        <span className="max-w-[70px] truncate text-[8px] font-medium text-blue-500" title={path}>
                          {path}
                        </span>
                      </div>
                      <p className={`mt-0.5 line-clamp-2 text-[11px] leading-snug ${item.free ? 'text-green-700' : 'text-ms-gray-700'}`}>{item.name}</p>
                    </div>
                    <div className="flex max-w-[55%] shrink-0 flex-col items-end pl-1">
                      {!item.free && item.discount > 0 && (
                        <span className="whitespace-nowrap text-[9px] text-ms-gray-400 line-through">{item.price.toLocaleString()}원</span>
                      )}
                      <span
                        className={`whitespace-nowrap text-right text-[10px] font-bold ${item.free ? 'text-ms-gray-400 line-through' : 'text-ms-black'}`}
                        data-testid="cart-row-price"
                      >
                        {(item.free ? item.price : itemPrice(item)).toLocaleString()}원
                      </span>
                    </div>
                  </div>
                  <div className="mt-1 flex items-center gap-1" onClick={(e) => e.stopPropagation()}>
                    {!item.free && (
                      <select
                        value={item.discount || 0}
                        onChange={(e) => setItemDiscount(item.id, Number(e.target.value))}
                        className="h-8 rounded border border-ms-gray-300 bg-white px-1 text-[10px] text-ms-gray-600"
                        data-testid="item-discount"
                      >
                        <option value={0}>할인없음</option>
                        {ITEM_DISCOUNT_RATES.map((r) => (
                          <option key={r} value={r}>
                            {r}%
                          </option>
                        ))}
                      </select>
                    )}
                    <button
                      onClick={() => toggleFree(item.id)}
                      className={`h-8 rounded px-2 text-[10px] transition-colors ${
                        item.free ? 'bg-green-500 text-white hover:bg-green-600' : 'bg-ms-gray-100 text-ms-gray-500 hover:bg-green-100 hover:text-green-600'
                      }`}
                      data-testid="item-free"
                    >
                      {item.free ? '무료 해제' : '무료시술'}
                    </button>
                    <button
                      onClick={() => removeFromCart(item.id)}
                      className="h-8 rounded bg-ms-gray-100 px-2 text-[10px] text-ms-gray-500 transition-colors hover:bg-red-100 hover:text-red-600"
                      data-testid="item-remove"
                    >
                      삭제
                    </button>
                  </div>
                </div>
              );
            })}
          </div>
        ) : (
          <div className="flex h-full items-center justify-center">
            <p className="text-typo-caption-md-400 text-ms-gray-500">← 시술을 선택해 주세요</p>
          </div>
        )}
      </div>
      {cart.length > 0 && children}
    </div>
  );
}
