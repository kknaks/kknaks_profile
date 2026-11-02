'use client';

import { useCallback, useEffect, useRef, useState } from 'react';
import type { FilterKey } from '@/domain/filters';
import { useScreenStore } from '@/stores/screen-store';
import { LINK_TIMEOUT_MS, openChannel, type SyncChannel } from './channel';

/** 큰 화면: 접속 인사 → 스냅샷 수신 · ping 에 pong · 필터 칩은 태블릿에 요청만. 반환 = 상담사 화면 연결 여부 + 필터 요청 함수 */
export function useScreenSync(): { linked: boolean; requestFilter: (f: FilterKey) => void } {
  const chRef = useRef<SyncChannel | null>(null);
  const [lastPing, setLastPing] = useState(0);
  const [now, setNow] = useState(0);

  useEffect(() => {
    const ch = openChannel('screen');
    chRef.current = ch;
    const offs = [
      ch.on('state:snapshot', (m) => {
        useScreenStore.getState().apply(m.payload.seq, m.payload.state);
        setLastPing(Date.now());
      }),
      ch.on('presence:ping', () => {
        setLastPing(Date.now());
        ch.post('presence:pong', {});
      }),
    ];
    ch.post('screen:hello', {});
    const tick = setInterval(() => setNow(Date.now()), 1000);
    return () => {
      offs.forEach((off) => off());
      clearInterval(tick);
      ch.close();
      chRef.current = null;
    };
  }, []);

  const requestFilter = useCallback((filter: FilterKey) => chRef.current?.post('filter:set', { filter }), []);
  return { linked: lastPing > 0 && (now === 0 || now - lastPing < LINK_TIMEOUT_MS), requestFilter };
}
