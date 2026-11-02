'use client';

import { useEffect, useRef, useState } from 'react';

/** 숫자 트윈(기본 300ms) — 금액이 바뀌면 부드럽게 넘어간다 */
export function useTween(target: number, ms = 300): number {
  const [value, setValue] = useState(target);
  const from = useRef(target);
  useEffect(() => {
    const start = performance.now();
    const v0 = from.current;
    let raf = 0;
    const step = (t: number) => {
      const k = Math.min(1, (t - start) / ms);
      const v = Math.round(v0 + (target - v0) * (1 - Math.pow(1 - k, 3)));
      setValue(v);
      from.current = v;
      if (k < 1) raf = requestAnimationFrame(step);
    };
    raf = requestAnimationFrame(step);
    return () => cancelAnimationFrame(raf);
  }, [target, ms]);
  return value;
}
