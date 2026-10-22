'use client';

import { useState } from 'react';
import type { RecommendChip, TaxonomyExtracted } from '@/data/recommend-rules';
import { useSessionStore } from '@/stores/session-store';

type Tone = 'contra' | 'safety' | 'aftercare' | 'neutral';
const TONE: Record<Tone, { header: string; label: string }> = {
  contra: { header: 'bg-red-50', label: 'text-red-700' },
  safety: { header: 'bg-pink-50', label: 'text-pink-700' },
  aftercare: { header: 'bg-amber-50', label: 'text-amber-700' },
  neutral: { header: 'bg-gray-50', label: 'text-gray-700' },
};

function Chips({ items, cls }: { items: string[]; cls: string }) {
  return (
    <div className="flex flex-wrap gap-1">
      {items.map((s, i) => (
        <span key={i} className={`rounded px-1.5 py-0.5 text-[10px] ${cls}`}>
          {s}
        </span>
      ))}
    </div>
  );
}

function Section({ label, tone, children }: { label: string; tone: Tone; children: React.ReactNode }) {
  return (
    <div className="overflow-hidden rounded-xl border border-gray-200 bg-white">
      <div className={`px-2.5 py-1 ${TONE[tone].header}`}>
        <p className={`text-[10px] font-bold ${TONE[tone].label}`}>{label}</p>
      </div>
      <div className="px-2.5 py-1.5">{children}</div>
    </div>
  );
}

/** 상세 카드 — 기대 효과·금기·부작용·시술 후 주의(stg charty-recommendation.tsx DetailSection :106-230) */
function Detail({ data }: { data: TaxonomyExtracted }) {
  const primary = data.indications?.primary ?? [];
  const absolute = data.contraindications?.absolute ?? [];
  const relative = data.contraindications?.relative ?? [];
  const serious = data.safety?.serious ?? [];
  const common = data.safety?.common ?? [];
  return (
    <div className="space-y-2">
      {primary.length > 0 && (
        <Section label="기대 효과" tone="neutral">
          <Chips items={primary.slice(0, 4)} cls="border border-gray-200 bg-gray-50 text-gray-900" />
        </Section>
      )}
      {(absolute.length > 0 || relative.length > 0) && (
        <Section label="금기사항" tone="contra">
          <Chips items={[...absolute, ...relative].slice(0, 5)} cls="border border-red-200 bg-red-50 text-red-700" />
        </Section>
      )}
      {(serious.length > 0 || common.length > 0) && (
        <Section label="부작용" tone="safety">
          <Chips items={[...serious, ...common].slice(0, 5)} cls="border border-pink-200 bg-pink-50 text-pink-700" />
        </Section>
      )}
      {data.aftercare && data.aftercare.length > 0 && (
        <Section label="시술 후 주의" tone="aftercare">
          <ol className="space-y-1">
            {data.aftercare.slice(0, 3).map((s, i) => (
              <li key={i} className="flex gap-1.5 text-[10px] text-gray-700">
                <span className="flex h-4 w-4 shrink-0 items-center justify-center rounded-full bg-amber-50 text-[9px] text-amber-700">{i + 1}</span>
                {s}
              </li>
            ))}
          </ol>
        </Section>
      )}
    </div>
  );
}

/** 추천 260 — 「감지된 시술」 자리에 분석 규칙 추천(stg charty-recommendation.tsx:373-434) */
export function RecommendationPanel({ chips }: { chips: RecommendChip[] }) {
  const [active, setActive] = useState<string | null>(null);
  const setUi = useSessionStore((s) => s.setUi);
  const chip = chips.find((c) => c.modality === active) ?? null;

  return (
    <div className="flex h-full w-[260px] shrink-0 flex-col border-l border-ms-gray-300 bg-white" data-testid="recommend-panel">
      <div className="flex h-10 shrink-0 items-center gap-2 border-b border-ms-gray-300 px-4">
        <span className="text-typo-heading-sm-500 text-ms-black">추천 시술</span>
        {chips.length > 0 && (
          <span className="rounded-full bg-primary-100 px-2 py-0.5 text-typo-caption-md-500 text-primary" data-testid="recommend-count">
            {chips.length}
          </span>
        )}
      </div>
      <div className="custom-scrollbar min-h-0 flex-1 overflow-y-auto">
        {chips.length === 0 ? (
          <div className="flex h-full items-center justify-center px-4">
            <p className="text-center text-typo-caption-md-400 text-ms-gray-500">피부 분석 결과가 있으면 추천 시술이 여기에 보여요</p>
          </div>
        ) : (
          <>
            <div className="flex flex-wrap items-center gap-1 border-b border-slate-100 px-3 py-2">
              {chips.map((c) => (
                <button
                  key={c.modality}
                  type="button"
                  onClick={() => setActive(active === c.modality ? null : c.modality)}
                  className={`h-8 shrink-0 rounded-full px-2.5 text-[10px] transition-colors ${
                    active === c.modality ? 'bg-primary text-white' : 'bg-ms-gray-200 text-ms-gray-700 hover:bg-ms-gray-300'
                  }`}
                  data-testid={`recommend-chip-${c.modality}`}
                >
                  {c.label}
                </button>
              ))}
            </div>
            {chip ? (
              <div className="space-y-2 px-3 py-2.5">
                <p className="text-[13px] font-bold text-purple-700">{chip.label}</p>
                <p className="text-[11px] text-ms-gray-700">
                  <span className="font-semibold text-ms-black">이유</span> · {chip.reasons.join(' · ')}
                </p>
                {chip.extracted && <Detail data={chip.extracted} />}
                <button
                  type="button"
                  className="h-8 w-full rounded-md border border-primary text-[11px] font-medium text-primary hover:bg-primary-100"
                  onClick={() => setUi({ showAll: true, categoryFilter: chip.priceCategory, priceTypeFilter: null, searchQuery: '' })}
                  data-testid="recommend-goto-price"
                >
                  가격표에서 보기
                </button>
                <p className="text-[9px] text-ms-gray-500">목업용 추천 규칙 — 의학적 근거가 아니에요</p>
              </div>
            ) : (
              <p className="px-3 py-3 text-[11px] text-ms-gray-500">칩을 누르면 추천 이유와 설명이 보여요</p>
            )}
          </>
        )}
      </div>
    </div>
  );
}
