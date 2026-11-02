'use client';

import { useLayoutEffect, useRef, useState } from 'react';

interface StageProps {
  width: number;
  height: number;
  /** 레터박스 배경 */
  background?: string;
  children: React.ReactNode;
}

/**
 * 고정 설계 캔버스를 창 크기에 맞춰 transform: scale() 로 맞춘다(SPEC §1-1, §3-1).
 * 남는 곳은 레터박스.
 */
export function Stage({ width, height, background = 'var(--ms-gray-100)', children }: StageProps) {
  const hostRef = useRef<HTMLDivElement>(null);
  const [scale, setScale] = useState(1);

  useLayoutEffect(() => {
    const host = hostRef.current;
    if (!host) return;
    const update = () => {
      const s = Math.min(host.clientWidth / width, host.clientHeight / height);
      setScale(s > 0 ? s : 1);
    };
    update();
    const ro = new ResizeObserver(update);
    ro.observe(host);
    return () => ro.disconnect();
  }, [width, height]);

  return (
    <div
      ref={hostRef}
      className="fixed inset-0 flex items-center justify-center overflow-hidden"
      style={{ background }}
    >
      <div
        data-testid="stage-canvas"
        data-scale={scale}
        style={{
          width,
          height,
          flex: 'none',
          transform: `scale(${scale})`,
          transformOrigin: 'center center',
          position: 'relative',
        }}
      >
        {children}
      </div>
    </div>
  );
}
