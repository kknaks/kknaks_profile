# WP1-FE 결과 보고 — 사건 채널(화면)

## 상태: done (커밋 없음 · 워크트리에 변경만)

- SSOT: WORK-013 「Phase WP1-FE」 · SPEC-011 v0.2.2 §4.1(특히 §4.1-3 ⑤ · §4.1-6) · SPEC-008 §4.4 · 서버 실물 `be-wp1-report.md`
- 경로는 `frontend/` 기준. `backend/` · `src-tauri/` · 회의 WS(`features/meetings/stream.ts`)는 손대지 않았다
- 기준선: `fe-baseline.md` — 74 passed · 기존 실패 0 · tsc 0

## 1. 계약 체크박스 — 7/7

| # | 계약 | 구현 위치 |
|---|---|---|
| 1 | **App 이 로그인한 동안 EventSource 하나** — 화면이 바뀌어도 유지 · 로그아웃·세션 상실 때 닫음 | `src/App.tsx:442-451 · :783` — 로그인 분기(AppShell)를 `<EventStreamProvider>` 로 감쌌다<br>`src/lib/eventStreamContext.tsx` `EventStreamProvider` — mount 때 `createEventChannel(...).start()`, unmount 때 `stop()`<br>로그아웃·세션 상실이면 App 이 로그인 화면을 그려 Provider 가 내려가며 닫힌다. 화면 전환은 Provider 아래라 연결이 그대로다 |
| 2 | `useInboxStream` → 전역 연결 구독 · 메시지함·설정이 지금과 같이 반응 · 듣는 자식 넷 그대로 | `src/features/inbox/inboxStream.ts:16-22` — 시그니처 `(onEvent, {enabled, onReconnect})` 는 그대로다. 속은 `useEventStream` 구독(메시지함 사건 넷 → `onEvent` · `resync` → `onReconnect`)이다<br>부르는 곳 `InboxPage.tsx:157` · `SettingsPage.tsx:182` 는 **무변경**<br>InboxPage 의 자식 허브(`createInboxEventHub`)와 듣는 자식 넷(`MailView.tsx:294` · `RoomView.tsx:460,526,646`)도 **무변경** |
| 3 | **`resync` → 옛 `onReconnect` 와 같은 다시 읽기 · 한 연결에 한 번** — 순번을 실었으면 서버 `resync` 에서 · 순번 없이 다시 붙었으면 둘째 이후 `ready` 에서 · 첫 `ready` → 점(WP3 구독 자리) | `src/lib/eventStream.ts:175-192`<br>• `ready` 에서 `readyCount` 를 센다. `{kind:"ready", first}` 를 낸다 — WP3 가 점을 다시 읽을 자리(`useEventStream`)다<br>• 둘째 이후 `ready` 이고 이 연결이 순번을 안 실었으면 `resync` 를 낸다(`:184`)<br>• 순번을 실은 연결은 서버 `resync` 를 그대로 낸다(`:186-192`)<br>「순번을 실었나」 = 새 연결 주소에 `last_event_id` 가 있었거나(`urlCarriedSeq`), 이 인스턴스가 `id:` 를 받아 브라우저가 `Last-Event-ID` 머리를 싣는 경우(`instanceGotId`)다<br>같은 연결에 `replay_overflow` · `dropped` 가 또 오면 따른다 |
| 4 | **멈춤** — `/api/auth/me` 200 인데 스트림만 연속 10회 실패 → 빠른 재연결 멈춤 · 5분마다 · `visibilitychange`(visible) · 포커스 때 즉시 · `/api/auth/me` 실패(장애)는 세지 않음 | `eventStream.ts:138-158` — `verdict === "ok"` 일 때만 `streamFailures += 1`. 10이면 `paused` 로 두고 `SLOW_RETRY_MS`(5분) 뒤 한 번 시도한다<br>`:247-252` `wake` — 멈춘 동안만 `visibilitychange` · `focus` 에서 바로 연다<br>`ready` 면 세던 수와 멈춤을 0 으로 되돌린다(`:178-180`)<br>상수 `:66-71` |
| 5 | **닫힘 처리** — `CONNECTING` 은 브라우저 재연결에 맡김(30초 넘으면 버림) · `CLOSED` 면 `GET /api/auth/me` → `401` 세션 상실(회의 4401 과 같은 길) · 아니면 백오프(1→2→4…30초 · ±20%) 새 `EventSource(…?last_event_id=)` · 세션 확인도 같은 백오프 · WS 의 무한 재시도 없앰 | `eventStream.ts:226-244`(`onerror` — `readyState` 0 이면 30초 타이머, 2 이면 버리고 `handleClosed`)<br>`:138-158`(`handleClosed` — `getSession`: null(401) → `stop()` + `onSessionLost`. 그 밖은 `backoff()` 뒤 `open()`)<br>`:122-127` 백오프 계산(`BACKOFF_BASE_MS · 2^n`, 최대 30초, ±20%)<br>세션 확인이 5xx·네트워크로 실패해도 같은 백오프로 다시 연결하고, 다시 실패하면 다시 확인한다<br>세션 상실은 `App.tsx:443-446` — `resetWorkspace()` + `setSession(null)`. 회의 스트림의 `onSessionLost`(`App.tsx` MeetingWorkspace)와 같은 처리다 |
| 6 | **받은 (알림 id · 순번) 기억** — 겹침 창으로 다시 온 줄은 끼우지도 OS 알림도 하지 않음 | `eventStream.ts:194-208` — `seen` 집합(채널 수명 = 로그인 세션). 같은 쌍은 구독자에게 내지 않는다. 받은 가장 큰 순번은 `lastSeq` 로 두고 다음 새 연결의 `?last_event_id=` 로 싣는다 |
| 7 | WS 연결 코드(`new WebSocket` · 백오프 2→30s) 걷기 · 주소 함수 교체 | `inboxStream.ts` 의 WS 훅 전체를 걷었다(`git diff` 참고)<br>`src/lib/api.ts:1752-1759` `inboxStreamUrl`(ws(s)://…/api/inbox/stream) → `eventStreamUrl(lastEventId)`(같은 origin `/api/events/stream[?last_event_id=]`) |

더한 타입은 `src/lib/viewModels.ts:1705-1717` 이다: `StreamNotification` · `NotificationUpsertedEvent` · `NotificationReadEvent`. 서버 고정값(`id:` = `notification.seq` · 이어 받은 줄 `replayed: true`)을 따른다. `InboxStreamEvent` docstring 은 SSE 로 고쳤다(모양은 그대로).

## 2. Code Surface WP1 화면 줄 — 닿은 자리

| 패턴 | 표(시작 다시 셈) | 지금 prod / test | 처분 |
|---|---|---|---|
| `useInboxStream\(` | 3/3 | 3/3 · 0 | 정의를 전역 구독으로 바꿨다. 쓰는 두 곳은 그대로 |
| `new WebSocket` | 2/2 | **1/1** · 0 | 메시지함 WS 를 걷었다. 남은 1은 회의 `meetings/stream.ts:103`(손대지 않음) |
| `inboxStreamUrl` | 3/2 | **0** | → `eventStreamUrl` 3/2(정의 · 사용 · docstring) |
| `createInboxEventHub\|hub\.subscribe\|hub\.emit` | 8/4 · 2/1 | 9/5 · 2/1 | InboxPage 허브·자식 넷은 그대로. +1 은 새 `eventStreamContext.tsx` 의 `hub?.subscribe` |
| `InboxStreamEvent` | 9/3 | 12/4 | 타입은 그대로. 새 `eventStream.ts` 가 씀 |
| 메시지함 사건 이름 넷 | 14/6 · 13/2 | 16/8 · 16/3 | 이름은 그대로. +는 `INBOX_EVENT_NAMES` 정의 · `api.ts` 주석 · 새 시험 |
| `onReconnect`(사건 채널 쪽 6줄) | — | 그대로 | 이름을 유지하고 채널의 `resync` 에 묶었다. 나머지 14줄은 「다시 연결」 단추 prop 으로 무관 |
| 세션 상실 | — | — | `App.tsx` 회의 `onSessionLost` 와 같은 처리로 SSE 의 세션 확인 401 을 받는다 |
| `stubGlobal("WebSocket"` | 9/5 | **1/1** | 메시지함·설정·App·Landing 8곳을 `stubGlobal("EventSource"` 로 바꿨다. 남은 1은 `MeetingLive.test.tsx`(회의 — 그대로). `stubGlobal("EventSource"` 는 12/5 |

**표 밖에서 찾은 것** — 없다. `rg "inbox/stream|WebSocket"` 의 남은 줄은 회의 경로와 `viewModels.ts` 주석(옛 WS 이름을 밝힘)뿐이다.

## 3. 새 · 바뀐 시험

| 파일 | 내용 |
|---|---|
| **새** `src/lib/eventStream.test.ts`(16) | 연결 하나 · 같은 origin 주소 · 메시지함 넷 · 모르는 사건 버림<br>(id·순번) 거름<br>**① CLOSED + 200 → 1초 뒤 새 인스턴스 · `?last_event_id=` · 로그인 안 감 · 2초 · `ready` 뒤 0 으로**<br>백오프 30초 상한 · ±20%<br>**② 401 → 세션 상실 · 다시 안 붙음**<br>**③ CONNECTING 은 새 인스턴스 없음 · 30초 넘으면 버리고 확인** · ③′ 30초 안에 붙으면 유지<br>**④ 순번 없이 끊겼다 붙으면 쿼리 없이 · 둘째 `ready` 에서 `resync` 한 번** · ④′ 같은 인스턴스의 브라우저 재연결<br>**⑥ 순번 실은 재연결은 `ready` 말고 서버 `resync` 에서만 · `dropped` 도 따름 · 이어 받은 중복 거름** · ⑥′ `id:` 받은 인스턴스의 머리 재연결<br>**⑤ 200 + 10회 → 멈춤 → 5분 · `visibilitychange` · `focus` 로 다시 · 붙으면 0** · ⑤′ `/api/auth/me` 실패는 15회여도 안 멈춤<br>멈추지 않은 동안 포커스로 연결이 늘지 않음 · stop 뒤 오류 무시 · EventSource 없으면 아무것도 안 함 |
| **새** `src/lib/fakeEventSource.test-utils.ts` | EventSource 대역(`emit(name, data, id)` · `ready()` · `fail(0\|2)`) — 화면 시험이 같이 쓴다 |
| `src/features/inbox/InboxPage.test.tsx` | WS 대역 → EventSource 대역. Harness 둘을 Provider 로 감쌌다. 주소 단언은 `/api/events/stream` 으로 바꿨다<br>**+2**: 순번 없는 재연결은 둘째 `ready` 에서 목록 한 번(첫 `ready` 로는 안 읽음) · 서버 `resync` 에 목록 다시 읽기 |
| `src/features/settings/SettingsPage.test.tsx` | Harness 를 Provider 로 감쌌다. `integration.changed` 시험은 EventSource 대역으로 옮겼다<br>**+1**: `resync` · 순번 없는 둘째 `ready` 에서 연동을 한 번씩 다시 읽음(첫 `ready` 로는 안 읽음) |
| `src/App.test.tsx` | WS stub → EventSource stub 1곳<br>**+2**: 홈·업무·메시지함·설정을 오가도 EventSource 하나 · 로그아웃하면 닫힘 / 닫힌 뒤 `/api/auth/me` 401 → 로그인 화면 · 다시 안 붙음 |
| `src/SettingsLanding.test.tsx` | WS stub → EventSource stub 2곳 |

시험이 결함을 실제로 잡는지 변이 셋으로 확인했다(확인 뒤 원본으로 되돌렸다). 「순번 실음」 판정을 지우거나, 세션 200 만 세는 조건을 없애거나, 중복 거름을 빼면 각각 2건씩 실패한다.

## 4. 검증 (관련 시험만 — P-8 · 사용자 지시)

| 명령 | 결과 |
|---|---|
| `cd frontend && npx vitest run src/features/inbox/InboxPage.test.tsx src/features/settings/SettingsPage.test.tsx src/SettingsLanding.test.tsx src/App.test.tsx src/lib/eventStream.test.ts --no-file-parallelism` | **5 files · 95 passed · 0 failed**(기준선 74 + 새 21) · 12.6s |
| `cd frontend && npx tsc --noEmit` | **0 오류** |

- `node_modules` 가 워크트리에 없어 `npm ci` 를 했다(`.gitignore` 대상)
- 전체 `make frontend-test` · `make verify` · `make frontend-build` 는 돌리지 않았다. 브리프 §5 가 타입을 `tsc --noEmit` 으로 정했다(WORK 시험 줄의 `make frontend-build` 는 코디 몫으로 남김)
- 사용자 포트·로컬 스택은 띄우지 않았다

## 5. 미결 · 다음 판에 알릴 것

1. **실물 완료 조건(앱)은 코디 몫이다** — 앱에서 화면을 오가도 연결 하나 · 메시지함/설정 반응 · **노트북 덮었다 열기 · 최소화 10분 뒤** 재연결과 다시 읽기. 백엔드 WP1-BE 를 반영한 스택 재기동이 먼저다(P-4 — 옛 back 이면 `/api/events/stream` 404 → 닫힘 → 세션 200 → 백오프, 10회 뒤 멈춤으로 보인다)
2. **WP3 가 받는 자리**
   - `useEventStream(signal => …)`(`lib/eventStreamContext.tsx`) — `ready{first}`(점 다시 읽기) · `resync`(알림 목록 다시 읽기) · `notification.upserted{event, seq}`(이미 걸러짐) · `notification.read`
   - 이어 받은 줄은 `event.replayed` 로 가를 수 있다
3. **WP4 가 받는 자리** — OS 알림(`notify_show`)도 같은 `notification.upserted` 신호를 쓰면 겹침 창 중복이 이미 걸러져 있다
4. **기억의 수명** — (id · 순번) 기억과 마지막 순번은 Provider(로그인 세션) 수명이다. 앱 창을 새로 만들면 첫 연결이다(SPEC §4.1-3 ⑤ 그대로)
5. **세션 확인 결과 해석** — `getSession()` 이 `null` 이면(401) 세션 상실로 본다. 200 인데 본문이 비는 비정상 응답도 `null` 이라 상실로 간다. 실제 `/api/auth/me` 는 200 이면 프로필을 준다
6. 옛 WS `/api/inbox/stream` 서버 라우트는 남아 있다(Rollback — WP1-BE). 화면은 더 부르지 않는다
