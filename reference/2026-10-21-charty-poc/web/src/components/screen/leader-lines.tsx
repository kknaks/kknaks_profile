'use client';

import { useEffect, useLayoutEffect, useRef } from 'react';
import { leaderSlots } from '@/components/viewer/anchor-store';
import { AREA_LAYOUT, type AreaCardModel, type AreaKey } from '@/domain/areas';
import { CARD_TITLE_Y, FACE_X0, FACE_X1, FILTER_BAR_H, VIEWER_W } from './viewer-layout';

/** 지시선 SVG — 뷰어 패널 기준 좌표. 위치·opacity 는 AnchorProjector 가 매 프레임 setAttribute 로 고친다(SPEC §3-4) */
export function LeaderLines({ cards }: { cards: AreaCardModel[] }) {
  const svg = useRef<SVGSVGElement>(null);

  // 카드 쪽 끝점 — 카드 top 은 레이아웃 고정이라 마운트 때 한 번 읽는다
  useLayoutEffect(() => {
    const root = svg.current?.parentElement;
    if (!root) return;
    for (const side of ['left', 'right'] as const) {
      for (const key of AREA_LAYOUT[side]) {
        const el = root.querySelector<HTMLElement>(`[data-testid=area-card-${key}]`);
        const slot = leaderSlots.get(key);
        if (!el || !slot) continue;
        const col = el.offsetParent as HTMLElement | null;
        slot.end = [side === 'left' ? FACE_X0 : FACE_X1, (col?.offsetTop ?? 0) + el.offsetTop + CARD_TITLE_Y];
        slot.side = side;
        slot.endEl?.setAttribute('cx', String(slot.end[0]));
        slot.endEl?.setAttribute('cy', String(slot.end[1]));
      }
    }
  }, []);

  useEffect(() => () => leaderSlots.clear(), []);

  // ref 콜백은 렌더마다 다시 불린다 — 카드 강조(strong → 흐린 선 ×0.5 · 점선)를 여기서 넣고, 스무딩 값(cur)·끝점은 이어 받는다
  const reg = (key: AreaKey, strong: boolean) => (g: SVGGElement | null) => {
    if (!g) return;
    const prev = leaderSlots.get(key);
    leaderSlots.set(key, {
      g,
      line: g.querySelector('polyline'),
      dot: g.querySelector('[data-role=dot]'),
      endEl: g.querySelector('[data-role=end]'),
      end: prev?.end ?? [0, 0],
      side: AREA_LAYOUT.left.includes(key) ? 'left' : 'right',
      route: AREA_LAYOUT.left[0] === key || AREA_LAYOUT.right[0] === key ? 'top' : 'knee',
      strong,
      cur: prev?.cur ?? 0,
      target: prev?.target ?? 0,
      x: prev?.x ?? 0,
      y: prev?.y ?? 0,
      applied: prev?.applied ?? 0,
    });
  };

  return (
    <svg
      ref={svg}
      className="pointer-events-none absolute left-0 top-0 z-10"
      width={VIEWER_W}
      style={{ height: `calc(100% - ${FILTER_BAR_H}px)` }}
      data-testid="leader-lines"
    >
      {cards.map((c) => (
        <g key={c.key} ref={reg(c.key, c.state === 'strong')} data-testid={`leader-${c.key}`} data-visible="false" opacity={0} className="transition-none">
          <polyline fill="none" stroke="var(--ms-primary)" strokeWidth={2} strokeLinejoin="round" points="" />
          <circle data-role="end" r={4} fill="var(--ms-primary)" />
          <circle data-role="dot" data-testid={`leader-dot-${c.key}`} r={7} fill="#fff" stroke="var(--ms-primary)" strokeWidth={2} />
        </g>
      ))}
    </svg>
  );
}
