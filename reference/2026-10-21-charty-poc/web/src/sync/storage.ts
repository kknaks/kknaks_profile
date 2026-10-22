import type { SessionState } from '@/domain/session';

const KEY = 'charty-consult-mockup/session';

/** 태블릿 상태 저장 — 읽기·쓰기 실패하면 조용히 초기 상태로(SPEC §4-2) */
export function loadSession(): { session: SessionState; seq: number } | null {
  try {
    const raw = localStorage.getItem(KEY);
    if (!raw) return null;
    const v = JSON.parse(raw);
    if (!v?.session?.sessionId || !Array.isArray(v.session.cart)) return null;
    return { session: v.session, seq: Number(v.seq) || 1 };
  } catch {
    return null;
  }
}

export function saveSession(session: SessionState, seq: number) {
  try {
    localStorage.setItem(KEY, JSON.stringify({ session, seq }));
  } catch {
    /* 저장 못 해도 화면은 돈다 */
  }
}
