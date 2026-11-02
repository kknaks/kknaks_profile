'use client';

import { Button, Card } from '@medisolve-ai/medikit';
import { ChevronDown, X } from 'lucide-react';
import { useCallback, useEffect, useRef, useState } from 'react';
import { hubPath, hubSourceLine, modalSections, type ModalSection, type SectionKey } from '@/data/hub/hub';

const LEFT: SectionKey[] = ['mechanism', 'indications', 'onset', 'procedure'];
const RIGHT: SectionKey[] = ['safety', 'contraindications', 'aftercare'];

function Body({ s }: { s: ModalSection }) {
  const b = s.body;
  if (b.kind === 'text') return <p className="text-typo-title-sm-400 text-ms-gray-800">{b.text}</p>;
  if (b.kind === 'list') {
    const Tag = b.ordered ? 'ol' : 'ul';
    return (
      <Tag className={`flex flex-col gap-1 pl-6 text-typo-title-sm-400 text-ms-gray-800 ${b.ordered ? 'list-decimal' : 'list-disc'}`}>
        {b.items.map((t, i) => (
          <li key={i}>{t}</li>
        ))}
      </Tag>
    );
  }
  if (b.kind === 'pairs') {
    return (
      <dl className="grid grid-cols-[auto_1fr] gap-x-4 gap-y-1 text-typo-title-sm-400">
        {b.pairs.map((p, i) => (
          <div key={i} className="contents">
            <dt className="whitespace-nowrap text-ms-gray-600">{p.label}</dt>
            <dd className="text-ms-gray-800">{p.text}</dd>
          </div>
        ))}
      </dl>
    );
  }
  return (
    <div className="flex flex-col gap-2">
      {b.groups.map((g, i) => (
        <div key={i}>
          <p className="text-typo-heading-md-600 text-ms-gray-600">{g.label}</p>
          <ul className="mt-0.5 flex list-disc flex-col gap-0.5 pl-6 text-typo-title-sm-400 text-ms-gray-800">
            {g.items.map((t, j) => (
              <li key={j}>{t}</li>
            ))}
          </ul>
        </div>
      ))}
    </div>
  );
}

function Section({ s }: { s: ModalSection }) {
  return (
    <section data-testid={`modal-sec-${s.key}`} data-source={s.sourceId} className="flex flex-col gap-2">
      <h3 className="flex items-baseline gap-2">
        <span className="text-typo-title-md-600 text-ms-black">{s.title}</span>
        {s.inheritedLabel && (
          <span className="rounded-md bg-ms-gray-200 px-2 py-0.5 text-typo-heading-md-500 text-ms-gray-800" data-testid="modal-inherited">
            {s.inheritedLabel}
          </span>
        )}
      </h3>
      <Body s={s} />
    </section>
  );
}

/** 시술명 모달(SPEC §4) — 화면 ① 안 오버레이. 메디킷 Dialog 는 포털이 Stage scale 밖으로 나가 쓰지 않는다 */
export function ProcedureModal({ hubId, label, onClose }: { hubId: string; label: string; onClose: () => void }) {
  useEffect(() => {
    const onKey = (e: KeyboardEvent) => e.key === 'Escape' && onClose();
    window.addEventListener('keydown', onKey);
    return () => window.removeEventListener('keydown', onKey);
  }, [onClose]);

  const scroller = useRef<HTMLDivElement>(null);
  const [more, setMore] = useState(false);
  const measure = useCallback(() => {
    const el = scroller.current;
    if (el) setMore(el.scrollHeight - el.scrollTop - el.clientHeight > 4);
  }, []);
  useEffect(() => {
    const el = scroller.current;
    if (!el) return;
    const ro = new ResizeObserver(measure);
    ro.observe(el);
    return () => ro.disconnect();
  }, [measure, hubId]);

  const sections = modalSections(hubId);
  const by = (keys: SectionKey[]) => keys.flatMap((k) => sections.filter((s) => s.key === k));
  const overview = sections.find((s) => s.key === 'overview');

  return (
    <div className="absolute inset-0 z-50 flex items-center justify-center bg-ms-black/50" onClick={onClose} data-testid="procedure-modal-backdrop">
      <Card
        padding="none"
        className="flex max-h-[880px] w-[1040px] flex-col overflow-hidden shadow-xl"
        onClick={(e) => e.stopPropagation()}
        role="dialog"
        aria-modal="true"
        aria-label={label}
        data-testid="procedure-modal"
        data-hub={hubId}
      >
        <header className="flex items-start gap-4 border-b border-ms-gray-200 px-8 pb-5 pt-6">
          <div className="min-w-0 flex-1">
            <p className="text-typo-heading-md-500 text-ms-gray-600" data-testid="modal-path">
              {hubPath(hubId)}
            </p>
            <h2 className="mt-1 text-typo-title-lg-600 text-ms-black">{label}</h2>
            {overview && overview.body.kind === 'text' && (
              <p className="mt-2 text-typo-title-sm-400 text-ms-gray-700" data-testid="modal-sec-overview" data-source={overview.sourceId}>
                {overview.body.text}
                {overview.inheritedLabel && (
                  <span className="ml-2 rounded-md bg-ms-gray-200 px-2 py-0.5 text-typo-heading-md-500 text-ms-gray-800" data-testid="modal-inherited">
                    {overview.inheritedLabel}
                  </span>
                )}
              </p>
            )}
          </div>
          <Button variant="outlined" color="gray" size="xl" onClick={onClose} aria-label="닫기" data-testid="procedure-modal-close" className="shrink-0 gap-2">
            <X className="h-6 w-6" />
            닫기
          </Button>
        </header>
        <div className="relative flex min-h-0 flex-1 flex-col">
          <div ref={scroller} onScroll={measure} className="grid min-h-0 flex-1 grid-cols-2 items-start gap-x-10 overflow-y-auto px-8 py-6" data-testid="modal-body">
            <div className="flex flex-col gap-6">{by(LEFT).map((s) => <Section key={s.key} s={s} />)}</div>
            <div className="flex flex-col gap-6">{by(RIGHT).map((s) => <Section key={s.key} s={s} />)}</div>
          </div>
          {/* 넘치면 아래 페이드 + 안내 — 대형 화면은 스크롤 막대를 잘 안 본다(2루프 W-6) */}
          {more && (
            <div className="pointer-events-none absolute inset-x-0 bottom-0 flex h-20 items-end justify-center bg-gradient-to-t from-ms-white via-ms-white/90 to-transparent pb-2" data-testid="modal-more">
              <span className="flex items-center gap-1 rounded-full bg-ms-black/70 px-3 py-1 text-typo-heading-md-500 text-ms-white">
                <ChevronDown className="h-4 w-4" />
                아래로 더 있어요
              </span>
            </div>
          )}
        </div>
        <footer className="border-t border-ms-gray-200 px-8 py-3 text-typo-heading-md-400 text-ms-gray-600" data-testid="modal-source">
          {hubSourceLine()}
        </footer>
      </Card>
    </div>
  );
}
