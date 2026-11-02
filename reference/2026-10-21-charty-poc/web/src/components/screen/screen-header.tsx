'use client';

import { Button } from '@medisolve-ai/medikit';
import { Maximize, Minimize } from 'lucide-react';
import { useEffect, useState } from 'react';
import { ConnectionDot } from '@/components/common/connection-dot';
import { useClock } from '@/components/common/use-clock';
import { COPY } from '@/content/copy';

interface ScreenHeaderProps {
  customerName: string | null;
  measuredAt: string | null;
  linked: boolean;
}

export function ScreenHeader({ customerName, measuredAt, linked }: ScreenHeaderProps) {
  const clock = useClock();
  const [isFull, setIsFull] = useState(false);
  const [idle, setIdle] = useState(false);

  useEffect(() => {
    const onChange = () => setIsFull(!!document.fullscreenElement);
    document.addEventListener('fullscreenchange', onChange);
    return () => document.removeEventListener('fullscreenchange', onChange);
  }, []);

  // 전체화면이면 버튼과 커서를 3초 뒤 숨긴다
  useEffect(() => {
    if (!isFull) return;
    let t = setTimeout(() => setIdle(true), 3000);
    const wake = () => {
      setIdle(false);
      clearTimeout(t);
      t = setTimeout(() => setIdle(true), 3000);
    };
    window.addEventListener('mousemove', wake);
    return () => {
      clearTimeout(t);
      window.removeEventListener('mousemove', wake);
    };
  }, [isFull]);

  const hidden = isFull && idle;
  useEffect(() => {
    document.body.style.cursor = hidden ? 'none' : '';
  }, [hidden]);

  const toggleFull = () => {
    if (document.fullscreenElement) document.exitFullscreen();
    else document.documentElement.requestFullscreen?.();
  };

  return (
    <header className="flex h-16 shrink-0 items-center justify-between border-b border-ms-gray-300 bg-ms-white px-6" data-testid="screen-header">
      <div className="flex items-center gap-4">
        {/* eslint-disable-next-line @next/next/no-img-element */}
        <img src="/charty-logo.svg" alt="Charty" className="h-7" />
        <span className="text-typo-title-md-600 text-ms-black">{COPY.screenTitle}</span>
        {customerName && (
          <span className="ml-6 text-typo-title-sm-500 text-ms-gray-800" data-testid="screen-customer">
            {customerName} 님{measuredAt && ` · ${measuredAt.replace(/-/g, '.')} 측정`}
          </span>
        )}
      </div>
      <div className="flex items-center gap-6 text-typo-heading-md-500">
        <ConnectionDot on={linked} label={linked ? COPY.linkOn : COPY.linkWait} testId="screen-link" />
        <span className="tabular-nums text-ms-black">{clock}</span>
        <Button
          variant="outlined"
          color="gray"
          size="m"
          onClick={toggleFull}
          aria-label={isFull ? '전체화면 끝내기' : '전체화면'}
          className={`gap-1.5 ${hidden ? 'invisible' : ''}`}
        >
          {/* 메디킷 leftIcon 은 아이콘에 토큰 size 를 주입해 lucide 와 안 맞는다 → children 으로 */}
          {isFull ? <Minimize className="h-4 w-4" /> : <Maximize className="h-4 w-4" />}
          {isFull ? '창 모드' : '전체화면'}
        </Button>
      </div>
    </header>
  );
}
