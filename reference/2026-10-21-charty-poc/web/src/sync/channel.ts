// 두 탭 동기화 계약(SPEC §4-3). 태블릿이 상태의 주인, 큰 화면은 사본.
import type { FilterKey } from '@/domain/filters';
import type { SessionState } from '@/domain/session';

export const CHANNEL_NAME = 'charty-consult-mockup/v1';

export interface Payloads {
  'screen:hello': Record<string, never>;
  'state:snapshot': { seq: number; state: SessionState };
  'filter:set': { filter: FilterKey };
  'presence:ping': { seq: number };
  'presence:pong': Record<string, never>;
}
export type MsgType = keyof Payloads;

export type Envelope<T extends MsgType = MsgType> = {
  v: 1;
  type: T;
  from: 'tablet' | 'screen';
  senderId: string;
  at: number;
  payload: Payloads[T];
};

export interface SyncChannel {
  post<T extends MsgType>(type: T, payload: Payloads[T]): void;
  on<T extends MsgType>(type: T, fn: (msg: Envelope<T>) => void): () => void;
  close(): void;
}

export function openChannel(from: 'tablet' | 'screen'): SyncChannel {
  const senderId = crypto.randomUUID();
  const bc = new BroadcastChannel(CHANNEL_NAME);
  const handlers = new Map<MsgType, Set<(m: Envelope) => void>>();
  bc.onmessage = (e: MessageEvent<Envelope>) => {
    const m = e.data;
    if (!m || m.v !== 1 || m.senderId === senderId || m.from === from) return;
    handlers.get(m.type)?.forEach((fn) => fn(m));
  };
  return {
    post(type, payload) {
      bc.postMessage({ v: 1, type, from, senderId, at: Date.now(), payload } satisfies Envelope);
    },
    on(type, fn) {
      if (!handlers.has(type)) handlers.set(type, new Set());
      const set = handlers.get(type)!;
      const h = fn as (m: Envelope) => void;
      set.add(h);
      return () => set.delete(h);
    },
    close() {
      bc.close();
    },
  };
}

export const PING_MS = 2000;
/** 큰 화면: 마지막 ping 후 5초 지나면 「연결 대기」(SPEC §4-3) */
export const LINK_TIMEOUT_MS = 5000;
/** 태블릿: 마지막 pong 후 4초면 「큰 화면 없음」, 판정은 500ms 마다.
 *  최악 = 마지막 pong 이 닫기 직전(δ≈0) → 4초 + tick 0.5초 = 4.5초 < AC-11 의 5초. ping 2초보다 길어 정상 연결에선 깜빡이지 않는다 */
export const TABLET_LINK_TIMEOUT_MS = 4000;
export const TABLET_LINK_TICK_MS = 500;
