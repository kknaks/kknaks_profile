'use client';

import { Button, ComboBox, Textarea, notify } from '@medisolve-ai/medikit';
import { useState } from 'react';
import { buildChartText } from '@/content/chart-text';
import type { SkinReport } from '@/domain/skin-report';
import { useSessionStore } from '@/stores/session-store';

const ACTION_BTN = '!h-8 !px-2 !text-[10px]';

/** 차트 탭 — 미리보기 · [복사] · [편집]→[저장]/[취소](stg chart-toolbar.tsx:75-122) */
export function ChartPanel({ report }: { report: SkinReport | null }) {
  const session = useSessionStore((s) => s.session);
  const override = useSessionStore((s) => s.ui.chartOverride);
  const setUi = useSessionStore((s) => s.setUi);
  const [target, setTarget] = useState<'all' | 'no-memo'>('all');
  const [editing, setEditing] = useState<string | null>(null);

  const text = override ?? buildChartText(report, session, true);
  const copyText = target === 'all' || override ? text : buildChartText(report, session, false);

  return (
    <div className="flex h-full flex-col" data-testid="chart-panel">
      <div className="flex min-h-[44px] items-center justify-end gap-1 px-2 py-1.5">
        <ComboBox
          value={target}
          onValueChange={(v) => setTarget(v as 'all' | 'no-memo')}
          options={[
            { value: 'all', label: '전체 복사' },
            { value: 'no-memo', label: '내부 메모 제외' },
          ]}
          hasSearch={false}
          size="m"
          className="!h-8 w-[110px] shrink-0 !text-[10px]"
          classNames={{ item: '!h-8 !min-h-0 !py-0 !px-2 !text-[12px] !whitespace-nowrap', optionList: '!p-0' }}
        />
        {editing == null ? (
          <>
            <Button
              size="s"
              variant="outlined"
              color="gray"
              className={ACTION_BTN}
              data-testid="chart-copy"
              onClick={async () => {
                try {
                  await navigator.clipboard.writeText(copyText);
                } catch {
                  /* 권한이 없어도 토스트는 띄운다(목업) */
                }
                notify.success('복사되었습니다.');
              }}
            >
              복사
            </Button>
            <Button size="s" variant="outlined" color="gray" className={ACTION_BTN} onClick={() => setEditing(text)} data-testid="chart-edit">
              편집
            </Button>
          </>
        ) : (
          <>
            <Button
              size="s"
              variant="solid"
              color="blue"
              className={ACTION_BTN}
              onClick={() => {
                setUi({ chartOverride: editing });
                setEditing(null);
              }}
              data-testid="chart-save"
            >
              저장
            </Button>
            <Button size="s" variant="outlined" color="gray" className={ACTION_BTN} onClick={() => setEditing(null)}>
              취소
            </Button>
          </>
        )}
      </div>
      <div className="min-h-0 flex-1 px-3 pb-3">
        {editing != null ? (
          <Textarea value={editing} onChange={(e) => setEditing(e.target.value)} containerClassName="h-full" textareaClassName="chart-preview h-full" />
        ) : (
          <pre className="chart-preview custom-scrollbar h-full overflow-auto rounded-lg border border-ms-gray-300 bg-ms-gray-100 p-3" data-testid="chart-text">
            {text}
          </pre>
        )}
      </div>
    </div>
  );
}
