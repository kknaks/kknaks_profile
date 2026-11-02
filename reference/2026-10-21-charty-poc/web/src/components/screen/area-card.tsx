'use client';

import { Card, Loading, cn } from '@medisolve-ai/medikit';
import { ImageIcon } from 'lucide-react';
import { useCallback, useEffect, useRef, useState } from 'react';
import { GradeBadge } from '@/components/common/grade-badge';
import { COPY } from '@/content/copy';
import { procedureSummary } from '@/data/hub/hub';
import type { AreaCardModel, AreaChip, AreaKey } from '@/domain/areas';
import { GRADE_META, formatScore } from '@/domain/grade';
import { AreaCrop, type CropSource } from './area-crop';

export type ReportStatus = 'loading' | 'ready' | 'missing';

interface AreaCardProps {
  card: AreaCardModel;
  status: ReportStatus;
  crop: CropSource | null;
  /** 카드 빈 곳 클릭 — 고르기/해제(U-2) */
  onToggle: (key: AreaKey) => void;
  /** 탭·[자세히] 클릭 — 그 카드를 고른다(해제하지 않음) */
  onSelect: (key: AreaKey) => void;
  onDetail: (chip: AreaChip) => void;
}

/** 대표 점수 1개 — 「눈물고랑 61.4」, 점수 없으면 「점수 없음 · 5,470개」 */
function ScoreLine({ card }: { card: AreaCardModel }) {
  const rep = card.measures[0];
  return (
    <span data-testid={`area-score-${card.key}`} data-value={card.score ?? ''} className="min-w-0">
      {rep && rep.score != null ? (
        <>
          {rep.label} <b className="font-semibold text-ms-black">{formatScore(rep.score)}</b>
        </>
      ) : rep ? (
        <>
          <span className="whitespace-nowrap">{GRADE_META.none.label}</span>
          {card.count != null && <span className="whitespace-nowrap">{` · ${card.count.toLocaleString('ko-KR')}개`}</span>}
        </>
      ) : null}
    </span>
  );
}

// 부위 확대 — 카드 머리에서 이름·등급·점수와 같이 들어가는 최대(3루프 V-3)
const CROP = 96;
const PHOTO = 56;

/** 뷰어 안 부위 카드(2루프 U-1·U-3·U-4) — 머리(부위 확대 + 이름·등급·점수) · 시술 탭 한 줄 · 고른 시술(사진 자리 + 간단 설명 + [자세히]) */
export function AreaCard({ card, status, crop, onToggle, onSelect, onDetail }: AreaCardProps) {
  const dim = card.state === 'dim';
  const [tab, setTab] = useState(0);
  // 탭이 넘쳐 오른쪽에 더 있으면 끝을 흐린다(가로 스크롤 신호)
  const tabsRef = useRef<HTMLDivElement>(null);
  const [tabsMore, setTabsMore] = useState(false);
  const measureTabs = useCallback(() => {
    const el = tabsRef.current;
    if (el) setTabsMore(el.scrollWidth - el.scrollLeft - el.clientWidth > 2);
  }, []);
  useEffect(() => {
    const el = tabsRef.current;
    if (!el) return;
    const ro = new ResizeObserver(measureTabs);
    ro.observe(el);
    return () => ro.disconnect();
  }, [measureTabs]);
  const chip = card.chips[Math.min(tab, card.chips.length - 1)];
  const summary = chip ? procedureSummary(chip.hubId) : null;

  return (
    <Card
      padding="none"
      data-testid={`area-card-${card.key}`}
      data-state={card.state}
      data-match={card.match}
      data-selected={card.selected}
      data-grade={card.grade}
      data-slot={card.slot}
      onClick={() => onToggle(card.key)}
      // 흐림은 내용에만 — 테두리(필터 일치 · 고른 카드)는 100%(W-11)
      className={cn(
        'pointer-events-auto min-h-0 flex-1 cursor-pointer overflow-hidden p-4',
        card.selected ? 'border-primary shadow-[0_0_0_4px_var(--ms-primary)]' : card.match && 'border-primary ring-[3px] ring-primary',
      )}
    >
      {/* 흐림은 글자·탭·설명에만 .35, 부위 사진은 알아보게 .75(3루프 V-3) */}
      <div className="flex min-h-0 flex-1 flex-col gap-2.5">
        <div className="flex shrink-0 gap-2.5">
          <div className={cn('shrink-0 transition-opacity duration-200', dim && 'opacity-75')} data-testid={`area-crop-wrap-${card.key}`}>
            <AreaCrop testId={`area-crop-${card.key}`} src={status === 'ready' ? crop : null} size={CROP} />
          </div>
          <div className={cn('flex min-w-0 flex-1 flex-col justify-center gap-0.5 transition-opacity duration-200', dim && 'opacity-35')}>
            {/* 이름 · 등급 · 점수 세 줄 — 한 줄에 묶으면 긴 부위명(팔자/광대·모공/피부결)이 잘린다 */}
            <h3 className="whitespace-nowrap text-typo-title-sm-600 leading-[22px] text-ms-black">{card.label}</h3>
            {status === 'ready' && (
              <div className="flex">
                <GradeBadge grade={card.grade} size="sm" />
              </div>
            )}
            <div className="flex min-w-0 flex-wrap items-center gap-x-1.5 text-[14px] leading-5 text-ms-gray-700">
              {status === 'loading' ? (
                <Loading className="h-4 w-4" />
              ) : status === 'missing' ? (
                <>
                  <span data-testid={`area-score-${card.key}`} data-value="" />
                  {/* 긴 안내(prepare:assets)는 오른쪽 열 ReportPlaceholder 가 맡는다(W-4) */}
                  <span data-testid="area-report-missing">{COPY.reportMissingShort}</span>
                </>
              ) : (
                <ScoreLine card={card} />
              )}
            </div>
          </div>
        </div>

        {/* 시술 탭 한 줄 — 줄바꿈 없이 넘치면 가로 스크롤(U-1) */}
        <div
          ref={tabsRef}
          onScroll={measureTabs}
          className={cn('no-scrollbar -mx-1 flex shrink-0 gap-1 overflow-x-auto px-1 transition-opacity duration-200', tabsMore && 'tabs-fade', dim && 'opacity-35')}
          role="tablist"
          data-testid={`area-tabs-${card.key}`}
          data-overflow={tabsMore}
        >
          {card.chips.map((c, i) => {
            const on = c === chip;
            return (
              <button
                key={c.hubId + c.label}
                type="button"
                role="tab"
                aria-selected={on}
                data-testid="area-tab"
                data-hub={c.hubId}
                data-name={c.label}
                data-selected={on}
                onClick={(e) => {
                  e.stopPropagation();
                  setTab(i);
                  onSelect(card.key);
                }}
                className={cn(
                  'h-8 shrink-0 whitespace-nowrap rounded-full border px-2.5 text-[13px] font-medium transition-colors',
                  on ? 'border-primary bg-primary text-ms-white' : 'border-ms-gray-300 bg-ms-white text-ms-gray-700 hover:border-primary',
                )}
              >
                {c.label}
              </button>
            );
          })}
        </div>

        {chip && (
          <div className={cn('flex min-h-0 gap-2.5 transition-opacity duration-200', dim && 'opacity-35')} data-testid={`area-desc-${card.key}`} data-hub={chip.hubId}>
            {/* 시술 사진 자리(U-3) — 원본이 없어 자리표시. chip.image 가 생기면 그린다 */}
            <div
              className="flex shrink-0 flex-col items-center justify-center gap-0.5 rounded-lg bg-ms-gray-100 bg-cover bg-center text-ms-gray-500"
              style={{ width: PHOTO, height: PHOTO, backgroundImage: chip.image ? `url(${chip.image})` : undefined }}
              data-testid={`area-photo-${card.key}`}
              data-image={chip.image ?? ''}
            >
              {!chip.image && (
                <>
                  <ImageIcon className="h-5 w-5" />
                  <span className="text-[11px]">사진</span>
                </>
              )}
            </div>
            <div className="flex min-w-0 flex-1 flex-col gap-1">
              {/* 제목 줄 오른쪽에 [자세히](3루프 V-2). 출처는 모달 아래 출처 줄에만(V-1) */}
              <div className="flex items-center gap-1.5">
                <p className="min-w-0 flex-1 truncate text-[15px] font-semibold leading-5 text-ms-black">{chip.label}</p>
                <button
                  type="button"
                  data-testid="area-detail"
                  data-hub={chip.hubId}
                  onClick={(e) => {
                    e.stopPropagation();
                    onSelect(card.key);
                    onDetail(chip);
                  }}
                  className="h-7 shrink-0 rounded-md border border-primary px-2.5 text-[13px] font-semibold text-primary hover:bg-primary-100"
                >
                  자세히
                </button>
              </div>
              {summary?.inheritedLabel && (
                <span className="text-[11px] leading-4 text-ms-gray-600" data-testid="area-summary-inherited">
                  {summary.inheritedLabel}
                </span>
              )}
              {summary && (
                <p
                  // 카드 높이(약 267)에서 남는 자리는 3줄 — 4줄로 두면 말줄임 없이 잘린다
                  className={cn('text-[13px] leading-[18px] text-ms-gray-700', summary.inheritedLabel ? 'line-clamp-2' : 'line-clamp-3')}
                  data-testid="area-summary"
                  data-source={summary.sourceId}
                >
                  {summary.text}
                </p>
              )}
            </div>
          </div>
        )}
      </div>
    </Card>
  );
}
