'use client';

import { useEffect, useMemo } from 'react';
import { GUIDE_CHECKS, STATIC_CHECKS, TEMPLATE_CHECKS, type GroupedCheck } from '@/data/mock/checklist';
import { TRANSCRIPT_TEXT } from '@/data/mock/transcript';
import { activeDisclosures, detectChecks } from '@/domain/checklist';
import { CONSULT_TYPE_LABEL } from '@/domain/session';
import { useSessionStore } from '@/stores/session-store';

const TAG_ON = 'bg-primary-100 text-primary border-primary-300';
const TAG_OFF = 'bg-white text-ms-gray-600 border-ms-gray-300';

/** 체크리스트 탭 — stg consultation-checklist.tsx 렌더(:814-1016) 구조. 초기 체크는 목 상담 텍스트 키워드로 */
export function ChecklistPanel() {
  const cart = useSessionStore((s) => s.session.cart);
  const template = useSessionStore((s) => s.session.consultType);
  const checked = useSessionStore((s) => s.ui.checklist);
  const auto = useSessionStore((s) => s.ui.checklistAuto);
  const setUi = useSessionStore((s) => s.setUi);
  const checkedSet = useMemo(() => new Set(checked), [checked]);

  // 감지는 한 번 잡힌 것을 다시 켜지 않는다(사람이 끈 것은 존중) — 새로 감지된 것만 켠다
  useEffect(() => {
    const detected = detectChecks(TRANSCRIPT_TEXT, template, cart);
    const fresh = detected.filter((id) => !auto.includes(id));
    if (fresh.length) setUi({ checklistAuto: [...auto, ...fresh], checklist: [...new Set([...checked, ...fresh])] });
  }, [cart, template, auto, checked, setUi]);

  const toggle = (id: string) => setUi({ checklist: checkedSet.has(id) ? checked.filter((x) => x !== id) : [...checked, id] });

  const pill = (id: string, label: string) => {
    const done = checkedSet.has(id);
    return (
      <button key={id} onClick={() => toggle(id)} className={`h-8 rounded-full border px-2 text-[11px] ${done ? TAG_ON : TAG_OFF}`} data-testid={`check-${id}`} data-done={done}>
        {done && <span className="mr-0.5">✓</span>}
        {label}
      </button>
    );
  };

  const grouped = (items: GroupedCheck[], prefix: string) => {
    const groups: Record<string, GroupedCheck[]> = {};
    for (const it of items) (groups[it.group] ??= []).push(it);
    return Object.entries(groups).map(([g, its]) => (
      <div key={g} className="mb-1">
        <span className="text-[9px] text-slate-400">{g}</span>
        <div className="mt-0.5 flex flex-wrap gap-1">{its.map((it) => pill(`${prefix}-${it.id}`, it.label))}</div>
      </div>
    ));
  };

  const staticDone = STATIC_CHECKS.filter((c) => checkedSet.has(`s-${c.id}`)).length;
  const guideDone = GUIDE_CHECKS.filter((c) => checkedSet.has(`n-${c.id}`)).length;
  const tmpl = TEMPLATE_CHECKS[template] ?? [];
  const disclosures = activeDisclosures(cart);

  return (
    <div className="custom-scrollbar h-full divide-y divide-slate-200 overflow-y-auto px-3 pb-4 pt-2" data-testid="checklist-panel">
      <div className="pb-3">
        <div className="mb-1 flex items-center gap-2">
          <span className="text-[11px] font-bold text-slate-600">필수 확인</span>
          <span className="text-[10px] text-slate-400" data-testid="static-done">
            {staticDone}/{STATIC_CHECKS.length}
          </span>
          <button
            type="button"
            onClick={() => checked.length && setUi({ checklist: [] })}
            disabled={!checked.length}
            className={`ml-auto h-8 text-typo-caption-md-400 ${checked.length ? 'font-medium text-ms-gray-700 hover:text-red-500' : 'cursor-not-allowed text-ms-gray-400'}`}
          >
            초기화
          </button>
        </div>
        {grouped(STATIC_CHECKS, 's')}
      </div>
      {tmpl.length > 0 && (
        <div className="py-3">
          <div className="mb-1 flex items-center gap-2">
            <span className="text-[11px] font-bold text-slate-600">{CONSULT_TYPE_LABEL[template]}</span>
            <span className="text-[10px] text-slate-400">
              {tmpl.filter((c) => checkedSet.has(`t-${c.id}`)).length}/{tmpl.length}
            </span>
          </div>
          <div className="flex flex-wrap gap-1">{tmpl.map((c) => pill(`t-${c.id}`, c.label))}</div>
        </div>
      )}
      <div className="py-3">
        <div className="mb-1 flex items-center gap-2">
          <span className="text-[11px] font-bold text-slate-600">안내사항</span>
          <span className="text-[10px] text-slate-400">
            {guideDone}/{GUIDE_CHECKS.length}
          </span>
        </div>
        {grouped(GUIDE_CHECKS, 'n')}
      </div>
      {disclosures.length > 0 ? (
        <div className="pt-3">
          {disclosures.map((d) => (
            <div key={d.label} className="mb-3 rounded-lg border border-slate-200 bg-slate-50 p-2" data-testid={`disclosure-${d.label}`}>
              <span className="text-[12px] font-semibold text-primary">{d.label}</span>
              <div className="mt-1.5 flex items-stretch gap-2">
                {(
                  [
                    ['orange', '부작용'],
                    ['blue', '시술 전'],
                    ['emerald', '시술 후'],
                  ] as const
                ).map(([color, title]) => {
                  const items = d.items.filter((i) => i.color === color);
                  if (!items.length) return null;
                  return (
                    <div key={color} className="min-w-0 flex-1 border-r border-slate-200 pr-2 last:border-r-0 last:pr-0">
                      <p className="mb-1 text-typo-caption-md-400 font-semibold text-ms-gray-700">{title}</p>
                      <div className="flex flex-wrap gap-1">{items.map((i) => pill(`${d.label}-${i.id}`, i.label))}</div>
                    </div>
                  );
                })}
              </div>
            </div>
          ))}
        </div>
      ) : (
        <div className="flex min-h-[120px] items-center justify-center py-3">
          <p className="text-center text-typo-caption-md-400 text-ms-gray-500">시술을 선택하면 관련 체크항목이 추가됩니다</p>
        </div>
      )}
    </div>
  );
}
