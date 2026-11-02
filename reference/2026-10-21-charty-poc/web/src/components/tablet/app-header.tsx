'use client';

import { useClock } from '@/components/common/use-clock';
import { COPY } from '@/content/copy';
import { MOCK_CLINIC, MOCK_COUNSELOR } from '@/data/mock/session';

/** 차티 header.tsx 문법의 축소판 — 50px 흰 헤더 · screenName · 시계 · 병원명 · 이름 pill(stg layouts/header.tsx:177-258) */
export function AppHeader() {
  const clock = useClock();
  return (
    <header className="flex h-[50px] shrink-0 items-center justify-between border-b border-ms-gray-300 bg-white px-5">
      <div className="flex items-center gap-3">
        {/* eslint-disable-next-line @next/next/no-img-element */}
        <img src="/charty-logo.svg" alt="Centurion Charty" className="h-5" />
        <span className="text-typo-caption-md-500 text-ms-gray-600">{COPY.tabletTitle}</span>
      </div>
      <div className="flex items-center gap-3 text-typo-caption-md-400">
        <span className="tabular-nums text-black">{clock}</span>
        <span className="text-ms-gray-600">{MOCK_CLINIC.name}</span>
        <span className="rounded-xl bg-primary-100 px-2.5 py-1 text-[11px] font-medium text-primary">{MOCK_COUNSELOR.name}</span>
      </div>
    </header>
  );
}
