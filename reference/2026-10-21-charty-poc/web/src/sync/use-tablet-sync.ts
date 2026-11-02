'use client';

import { useEffect, useState } from 'react';
import { useSessionStore } from '@/stores/session-store';
import { PING_MS, TABLET_LINK_TICK_MS, TABLET_LINK_TIMEOUT_MS, openChannel } from './channel';
import { loadSession, saveSession } from './storage';

/** 태블릿: 저장된 상태 복원 → 바뀔 때마다 전체 스냅샷 송신 · hello/filter:set 처리 · 2초 ping. 반환 = 큰 화면 연결 여부 */
export function useTabletSync(): boolean {
  const [lastPong, setLastPong] = useState(0);
  const [now, setNow] = useState(0);

  useEffect(() => {
    const saved = loadSession();
    if (saved) useSessionStore.getState().hydrate(saved.session, saved.seq + 1);

    const ch = openChannel('tablet');
    const snapshot = () => {
      const { session, seq } = useSessionStore.getState();
      ch.post('state:snapshot', { seq, state: session });
    };

    const unsub = useSessionStore.subscribe((st, prev) => {
      if (st.session === prev.session && st.seq === prev.seq) return;
      saveSession(st.session, st.seq);
      snapshot();
    });

    const offs = [
      ch.on('screen:hello', snapshot),
      ch.on('filter:set', (m) => useSessionStore.getState().setFilter(m.payload.filter)),
      ch.on('presence:pong', () => setLastPong(Date.now())),
    ];

    snapshot();
    const ping = setInterval(() => ch.post('presence:ping', { seq: useSessionStore.getState().seq }), PING_MS);
    const tick = setInterval(() => setNow(Date.now()), TABLET_LINK_TICK_MS);

    return () => {
      unsub();
      offs.forEach((off) => off());
      clearInterval(ping);
      clearInterval(tick);
      ch.close();
    };
  }, []);

  return lastPong > 0 && now - lastPong < TABLET_LINK_TIMEOUT_MS;
}
