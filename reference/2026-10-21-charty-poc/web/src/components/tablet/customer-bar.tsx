'use client';

import { Button, ComboBox, ConfirmModal, Toggle } from '@medisolve-ai/medikit';
import { ExternalLink } from 'lucide-react';
import { useState } from 'react';
import { ConnectionDot } from '@/components/common/connection-dot';
import { COPY } from '@/content/copy';
import { CONSULT_TYPE_LABEL, type ConsultType } from '@/domain/session';
import { useSessionStore } from '@/stores/session-store';

const TYPE_OPTIONS = (Object.keys(CONSULT_TYPE_LABEL) as ConsultType[]).map((k) => ({ value: k, label: CONSULT_TYPE_LABEL[k] }));

/** 고객 바 40 — 차티 세션 설정 바 자리(stg consultation-desktop.tsx:49-56) */
export function CustomerBar({ customerName, measuredAt, screenLinked }: { customerName: string | null; measuredAt: string | null; screenLinked: boolean }) {
  const consultType = useSessionStore((s) => s.session.consultType);
  const showPrice = useSessionStore((s) => s.session.screen.showPrice);
  const setConsultType = useSessionStore((s) => s.setConsultType);
  const setShowPrice = useSessionStore((s) => s.setShowPrice);
  const resetSession = useSessionStore((s) => s.resetSession);
  const [confirm, setConfirm] = useState(false);

  return (
    <div className="flex h-10 shrink-0 items-center justify-between gap-3 border-b border-ms-gray-300 bg-ms-gray-100 px-3 text-typo-caption-md-400">
      <div className="flex items-center gap-2">
        <span className="font-semibold text-ms-black">{customerName ? `${customerName} 님` : '고객'}</span>
        {measuredAt && <span className="text-ms-gray-600">· {measuredAt.replace(/-/g, '.')} 측정</span>}
        <ComboBox
          value={consultType}
          onValueChange={(v) => setConsultType(v as ConsultType)}
          options={TYPE_OPTIONS}
          hasSearch={false}
          size="m"
          testId="consult-type"
          className="!h-8 w-[104px] !px-2 !text-[11px]"
          classNames={{ item: '!h-8 !min-h-0 !py-0 !px-2 !text-[12px]', optionList: '!p-0' }}
        />
      </div>
      <div className="flex items-center gap-2">
        <span className="text-[11px]">
          <ConnectionDot on={screenLinked} size="sm" label={screenLinked ? COPY.screenOn : COPY.screenOff} testId="tablet-screen-link" />
        </span>
        <Button
          variant="outlined"
          color="gray"
          size="s"
          className="!h-8 gap-1 !px-2 !text-[11px]"
          onClick={() => window.open('/screen', 'charty-screen')}
          data-testid="open-screen-window"
        >
          큰 화면 열기 <ExternalLink className="h-3 w-3" />
        </Button>
        <span className="flex items-center gap-1 text-[11px] text-ms-gray-700">
          가격 표시
          <Toggle checked={showPrice} onChange={setShowPrice} data-testid="toggle-price" className="!h-8" />
        </span>
        <Button variant="text" color="gray" size="s" className="!h-8 !px-1 !text-[11px]" onClick={() => setConfirm(true)} data-testid="reset-session">
          상담 초기화
        </Button>
      </div>
      <ConfirmModal
        isOpen={confirm}
        title="상담을 초기화할까요?"
        description="선택한 시술·할인·필터가 처음 상태로 돌아가요."
        variant="caution"
        leftButton={{ label: '취소', onClick: () => setConfirm(false) }}
        rightButton={{
          label: '초기화',
          onClick: () => {
            resetSession();
            setConfirm(false);
          },
        }}
        onBackdropClick={() => setConfirm(false)}
        dataTestId="reset-confirm"
      />
    </div>
  );
}
