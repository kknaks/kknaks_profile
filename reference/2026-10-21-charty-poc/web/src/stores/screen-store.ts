'use client';

import { create } from 'zustand';
import { initialSessionState, type SessionState } from '@/domain/session';

/** 큰 화면의 사본 — 태블릿 스냅샷으로만 바뀐다. 저장하지 않는다 */
interface ScreenStore {
  session: SessionState;
  seq: number;
  apply: (seq: number, state: SessionState) => void;
}

export const useScreenStore = create<ScreenStore>()((set, get) => ({
  session: initialSessionState('pending'),
  seq: 0,
  apply: (seq, state) => {
    const cur = get();
    // seq 가 가진 것보다 작거나 같으면 버린다. 단 태블릿이 상태를 잃고 새 세션으로 시작했으면(sessionId 다름) 받는다
    if (seq <= cur.seq && state.sessionId === cur.session.sessionId) return;
    set({ seq, session: state });
  },
}));
