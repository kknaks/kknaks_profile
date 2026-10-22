'use client';

import { Search, Sparkles, X } from 'lucide-react';
import { buildCategoryPath, priceTypeStyle, type Procedure } from '@/domain/pricing';
import { useSessionStore } from '@/stores/session-store';

const chip = (on: boolean, dark = true) =>
  `h-8 text-[10px] px-2.5 rounded-full transition-colors flex-shrink-0 ${
    on ? (dark ? 'bg-ms-gray-800 text-white' : 'bg-primary text-white') : 'bg-ms-gray-200 text-ms-gray-700 hover:bg-ms-gray-300'
  }`;

interface ProcedureListProps {
  procedures: Procedure[];
  categories: string[];
  priceTypeChips: { key: string; label: string }[];
  recommendCount: number;
  totalCount: number;
}

/** 시술 목록 — 행 탭 = 카트 추가 · 정가 취소선(stg features/pricing/components/procedure-list.tsx:56-227) */
export function ProcedureList({ procedures, categories, priceTypeChips, recommendCount, totalCount }: ProcedureListProps) {
  const ui = useSessionStore((s) => s.ui);
  const setUi = useSessionStore((s) => s.setUi);
  const addToCart = useSessionStore((s) => s.addToCart);
  const searching = ui.searchQuery.trim().length > 0;

  return (
    <div className="flex min-w-0 flex-1 flex-col" data-testid="procedure-list">
      <div className="flex h-9 shrink-0 items-center gap-1.5 border-b border-ms-gray-300 bg-white px-3">
        <Search className="h-3.5 w-3.5 shrink-0 text-ms-gray-400" />
        <input
          type="text"
          value={ui.searchQuery}
          onChange={(e) => setUi({ searchQuery: e.target.value })}
          placeholder="시술명 검색"
          className="flex-1 bg-transparent text-[12px] text-ms-black outline-none placeholder:text-ms-gray-400"
          data-testid="procedure-search"
        />
        {searching && (
          <button onClick={() => setUi({ searchQuery: '' })} className="flex h-8 w-8 items-center justify-center text-ms-gray-400 hover:text-ms-gray-600" aria-label="검색 지우기">
            <X className="h-3.5 w-3.5" />
          </button>
        )}
      </div>

      {!searching && (
        <div className="flex shrink-0 flex-col gap-1 border-b border-ms-gray-300 bg-ms-gray-100 px-3 py-2">
          <div className="flex items-center gap-1.5">
            <span className="shrink-0 text-[10px] font-medium text-ms-gray-600">보기</span>
            <button onClick={() => setUi({ showAll: false })} className={chip(!ui.showAll, false)} data-testid="view-recommend">
              추천{recommendCount > 0 ? ` ${recommendCount}` : ''}
            </button>
            <button onClick={() => setUi({ showAll: true })} className={chip(ui.showAll, false)} data-testid="view-all">
              전체 {totalCount}
            </button>
          </div>
          <div className="flex items-start gap-1.5">
            <span className="flex h-8 shrink-0 items-center text-[10px] font-medium text-ms-gray-600">시술</span>
            <div className="custom-scrollbar flex items-center gap-1.5 overflow-x-auto pb-0.5">
              <button onClick={() => setUi({ categoryFilter: null })} className={chip(ui.categoryFilter === null)}>
                전체
              </button>
              {categories.map((c) => (
                <button key={c} onClick={() => setUi({ categoryFilter: ui.categoryFilter === c ? null : c })} className={chip(ui.categoryFilter === c)} data-testid={`cat-chip-${c}`}>
                  {c}
                </button>
              ))}
            </div>
          </div>
          <div className="flex items-start gap-1.5">
            <span className="flex h-8 shrink-0 items-center text-[10px] font-medium text-ms-gray-600">유형</span>
            <div className="custom-scrollbar flex items-center gap-1.5 overflow-x-auto pb-0.5" data-testid="price-type-chips">
              <button onClick={() => setUi({ priceTypeFilter: null })} className={chip(ui.priceTypeFilter === null)}>
                전체
              </button>
              {priceTypeChips.map((c) => (
                <button
                  key={c.key}
                  onClick={() => setUi({ priceTypeFilter: ui.priceTypeFilter === c.key ? null : c.key })}
                  className={chip(ui.priceTypeFilter === c.key)}
                  data-testid={`ptype-chip-${c.label}`}
                >
                  {c.label === '첫방문이벤트' ? '첫방문' : c.label}
                </button>
              ))}
            </div>
          </div>
        </div>
      )}

      {searching && (
        <div className="shrink-0 border-b border-ms-gray-300 bg-ms-gray-100 px-3 py-1">
          <span className="text-[10px] text-ms-gray-500">
            &quot;{ui.searchQuery}&quot; 검색 결과 {procedures.length}/{totalCount}건
          </span>
        </div>
      )}

      <div className="custom-scrollbar flex-1 overflow-y-auto overflow-x-hidden">
        {procedures.length > 0 ? (
          <div className="divide-y divide-ms-gray-200">
            {procedures.map((p) => (
              <div
                key={p.id}
                onClick={() => addToCart(p)}
                className="min-h-[32px] cursor-pointer px-2 py-1.5 transition-colors hover:bg-primary-100 active:bg-primary-300"
                data-testid="procedure-row"
                data-name={p.name}
                data-price-type={p.price_type ?? ''}
              >
                <div className="flex items-start justify-between gap-1">
                  <div className="min-w-0 flex-1">
                    <div className="flex items-center gap-1">
                      <span className={`rounded px-1 py-px text-[9px] ${priceTypeStyle(p.price_type)}`}>{p.price_type || '정규가'}</span>
                      <span className="max-w-[110px] truncate text-[9px] font-medium text-blue-500" title={buildCategoryPath(p)}>
                        {buildCategoryPath(p)}
                      </span>
                    </div>
                    <p className="mt-0.5 line-clamp-2 text-[11px] leading-snug text-slate-700">{p.name}</p>
                  </div>
                  <div className="max-w-[55%] shrink-0 pl-1 text-right">
                    {p.original_price != null && p.original_price > p.price && (
                      <p className="whitespace-nowrap text-[9px] text-slate-400 line-through">{p.original_price.toLocaleString()}원</p>
                    )}
                    <p className="whitespace-nowrap text-right text-[10px] font-bold text-slate-900">{p.price.toLocaleString()}원</p>
                  </div>
                </div>
              </div>
            ))}
          </div>
        ) : (
          <div className="flex flex-col items-center justify-center gap-2 px-6 py-10 text-center">
            <Sparkles size={24} strokeWidth={1.5} className="text-ms-gray-300" />
            <p className="text-typo-caption-md-500 text-ms-gray-600">
              {searching ? '검색 결과가 없습니다' : !ui.showAll ? '추천 시술이 없습니다' : '등록된 시술이 없습니다'}
            </p>
          </div>
        )}
      </div>
    </div>
  );
}
