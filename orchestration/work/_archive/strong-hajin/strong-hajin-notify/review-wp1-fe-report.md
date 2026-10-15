# 코드 검수 — WP1-FE (앱 전역 SSE 연결)

> reviewer(read-only) · 2026-10-08 · 대상 `strong-hajin-notify/frontend/` 변경(수정 8 · 새 4) · base `d2a06fa`
> 계약: WORK-013 「Phase WP1-FE」 · Code Surface WP1 화면 줄 · SPEC-011 §4.1(연결 수명 — v0.2.1 · r3 반영) · SPEC-008 §4.4
> 워커 리포트 `fe-wp1-report.md` · 서버 실물 WP1-BE(`backend/src/ax_workspace/entrypoints/http_events.py`) · 약어 `F/` = `frontend/src/`

## 0. 판정 — **PASS** (FAIL 0 · WARN 0 · 참고 4)

체크박스 7개는 **코드로** 지켜졌다(리포트가 아니라 줄로 확인). 아래가 모두 서 있다.
- 연결 하나 · 로그아웃 때 닫힘
- CLOSED → `/api/auth/me` 로 가름
- 백오프 새 연결 + `?last_event_id=`
- 한 연결에 다시 읽기 한 번
- 10회 멈춤은 auth 200 일 때만 셈 · 5분 느린 재시도 + 화면 활성/포커스
- (id · 순번) 거름

**서버(WP1-BE) 실제 구현과 사건 이름 · 필드 · `resync` 사유가 같다.** 「한 번만」 판단은 «서버가 `resync` 를 낼 연결인가»를 화면이 미리 가르는 방식이다. 그 기준이 서버의 `_last_event_id` 규칙과 정확히 맞물린다(§2).
관련 시험만 돌려 **6 files · 180 passed · `tsc --noEmit` 0**. 회의 WS · `src-tauri` 는 변경이 없다.

### 실행한 것
- `git diff` · 새 파일 4개 전문(`lib/eventStream.ts` · `lib/eventStreamContext.tsx` · `lib/fakeEventSource.test-utils.ts` · `lib/eventStream.test.ts`) · 서버 `http_events.py` 대조
- `cd frontend && npx vitest run src/lib/eventStream.test.ts src/features/inbox/InboxPage.test.tsx src/features/settings/SettingsPage.test.tsx src/SettingsLanding.test.tsx src/App.test.tsx src/features/meetings/MeetingLive.test.tsx --no-file-parallelism` → **180 passed**(회의 WS 시험을 일부러 넣어 무변경도 확인)
- `npx tsc --noEmit` → 0. 사용자 포트 · 프로세스는 건드리지 않았다(jsdom)

---

## 1. 체크박스 7 — 코드로

| WORK WP1-FE | 코드 | 판정 |
|---|---|---|
| App 이 로그인한 동안 EventSource **하나** · 화면이 바뀌어도 유지 · 로그아웃/세션 상실 때 닫음 | `F/App.tsx:437-447,783` — 로그인 뒤 분기의 최상위를 `EventStreamProvider` 가 감싼다(로그인 화면 · 세션 확인 중 · 브라우저 상호작용 화면은 그 밖이라 연결이 없다). 연결 수명 = Provider 수명 = `useEffect(…, [hub])`(`F/lib/eventStreamContext.tsx:17-21` — hub 는 `useState` 로 고정 → 화면 전환에 다시 서지 않는다) · 로그아웃(`App.tsx:274-279`)과 세션 상실이 `setSession(null)` → Provider 내려감 → `channel.stop()`(`F/lib/eventStream.ts:261-271` — 타이머 둘 · 리스너 둘 · `close()`). 시험 `App.test.tsx` 「오가도 하나 · 로그아웃하면 닫힌다」 | PASS |
| `useInboxStream` → 전역 구독 · 메시지함 · 설정 그대로 · 듣는 자식 넷 그대로 | `F/features/inbox/inboxStream.ts:17-25` — 연결 코드를 걷고 `useEventStream` 으로 `inbox` → `onEvent` · `resync` → `onReconnect`. 훅 시그니처가 같아 `InboxPage.tsx:157` · `SettingsPage.tsx:182` 는 **무변경**이다. `createInboxEventHub` 와 자식 넷(`MailView:294` · `RoomView:460,526,646`)도 그대로 | PASS |
| `resync` → 지금 `onReconnect` 와 같은 다시 읽기 · `ready` → 점 다시 읽기 자리 | `eventStream.ts:187-193`(서버 `resync` → 신호) · `:176-186`(`ready{first}` 신호 · WP3 의 점 자리) | PASS |
| **401 → 세션 상실 · 다시 안 붙음**(닫힘 처리) | `eventStream.ts:226-243` — `CONNECTING` 이면 그대로 두되 30초 넘으면 버림(`:228-237`) · `CLOSED` 면 버리고 `handleClosed`(`:138-155`): `checkSession` = `getSession()`(`api.ts:826` — 401 만 `null`, 그 밖은 throw → `unknown`) · `lost` → `stop()` + `onSessionLost`(App 이 `resetWorkspace` + `setSession(null)` — 회의 4401 과 같은 길 `App.tsx:534-537`) · `ok`/`unknown` → `schedule(backoff())` 새 인스턴스. 백오프 1→2→4…30초 · ±20%(`:124-128`) · `ready` 에서 0 으로(`:179`) | PASS |
| WS 연결 코드 걷기 · 주소 함수 교체 | `inboxStreamUrl` 0건 · `eventStreamUrl(lastSeq)`(`F/lib/api.ts:1757-1759` — 같은 origin 상대 경로 · 순번이 있을 때만 쿼리) · `new WebSocket` 은 회의 하나만 남았다 | PASS |
| (r2 R-F1 · r3 R3-W2) **한 연결 다시 읽기 한 번** | `:184` — 둘째 이후 `ready` 에서 `resync` 를 내는 것은 **그 연결이 순번을 싣지 않았을 때만**(`!(urlCarriedSeq \|\| instanceGotId)`). 순번을 실었으면 서버 `resync` 하나에서만 읽는다(`:189-192`). 같은 연결에 서버 `resync(replay_overflow \| dropped)` 가 또 오면 따른다 | PASS |
| (r2 R-W6 · r3 R3-W1) 10회 멈춤은 **auth 200 + 스트림 실패만** · 5분 · 활성/포커스 | `:146-153` — `verdict === "ok"` 일 때만 `streamFailures` +1 · 10 이면 `paused` + `schedule(SLOW_RETRY_MS = 5분)` · `unknown`(서버 장애)은 세지 않고 백오프를 잇는다 · `wake`(`:247-251` — `paused` 이고 연결이 없고 화면이 숨지 않았으면 바로 `open`, `open` 이 느린 타이머를 지운다 `:162`) · `visibilitychange` · `focus` 리스너는 `start` 에서 붙이고 `stop` 에서 뗀다 | PASS |
| (id · 순번) 거름 | `:194-207` — 키 `${notification_id}:${seq}` · 같은 키는 다시 내지 않는다 · 같은 id 라도 새 순번(합쳐짐)이면 낸다 · `lastSeq` 는 최댓값(`:202`) | PASS |

## 2. 서버와 맞나 (WP1-BE `http_events.py` 대조)

| 항목 | 서버 | 화면 | 일치 |
|---|---|---|---|
| 경로 · 쿼리 | `GET /api/events/stream` · `?last_event_id=` · 머리 우선(`_last_event_id :56-67`) | `eventStreamUrl` · 브라우저 머리는 자동 | ✓ |
| `retry` · `ready` | `retry: 3000` → `ready{v, server_time}` | `ready` 리스너 · `retry` 는 브라우저 몫 | ✓ |
| `resync` 사유 | `reconnected` · `replay_overflow` · `dropped` | 문자열 그대로 신호에(`:191`) | ✓ |
| 메시지함 넷 | `event:` = 이름 · `data` = NOTIFY 페이로드 그대로(`type` 포함) | `INBOX_EVENT_NAMES` 넷 · `type` 없으면 이름으로 메움(`:216-225`) | ✓ |
| `notification.upserted` | `id:` = 순번 · `{v, notification(+seq · updated_at), created, replayed}` | `lastEventId` → 순번(없으면 `notification.seq`) · `NotificationUpsertedEvent`(`viewModels.ts`) | ✓ |
| `notification.read` | `{v, notification_ids}` · 모두 읽음 `{v, all, theme}` | `NotificationReadEvent` | ✓ |
| **「서버가 `resync` 를 낼 연결인가」** | 머리나 쿼리에 값이 있으면 `reconnected=True` → 반드시 `resync` 하나(이어 받기 뒤 · 넘침 · 기준 없음 · 숫자 아님) | `urlCarriedSeq`(쿼리에 실음) 또는 `instanceGotId`(이 인스턴스가 `id:` 를 받음 → 브라우저가 다시 붙을 때 `Last-Event-ID` 머리를 싣는다) | ✓ — 두 조건이 서버가 `reconnected` 로 보는 조건과 1:1 이다. 그래서 다시 읽기가 0번이나 2번이 되는 경우가 없다 |

## 3. 조용히 통과하는 자리 — 시험 대역 · 누수 · 로그아웃

- **대역의 충실도**(`F/lib/fakeEventSource.test-utils.ts`)
  - `readyState` 0/1/2 · `onerror` 프로퍼티 · `open` → `ready` 순서 · `close()` → 2 를 실물처럼 굴린다
  - 실물과 다른 점: 실물 `MessageEvent.lastEventId` 는 `id:` 없는 사건에서도 **직전 id 를 들고 있다**. 대역은 `""` 를 준다. 코드는 `lastEventId` 를 `notification.upserted`(서버가 언제나 `id:` 를 싣는다)에서만 읽으므로 결과가 같다 → 참고 R-1
  - 대역은 브라우저 자체 재연결을 «같은 인스턴스에서 `fail(0)` → `ready()`» 로 흉내 낸다. 실물에서도 재연결은 같은 인스턴스라 맞다
  - 헤더(`Last-Event-ID`)는 대역이 보낼 수 없다. 머리를 «화면이 아는가» 로 바꿔 `instanceGotId` 로 고정했고, 그 기준은 §2 처럼 서버와 맞물린다
- **타이머 누수 없음**:
  - `stop()` 이 재시도 · CONNECTING 타이머를 지운다
  - 기다리던 `handleClosed` 는 `stopped \|\| source` 면 아무것도 하지 않는다(`:140`)
  - 버린 인스턴스의 늦은 사건은 `own()` 이 막는다(`:157-159`)
  - 시험 「stop 뒤에는 닫힌 연결의 오류로도 다시 붙지 않는다」
- **로그아웃 · 세션 상실 뒤 연결이 남지 않는다**: Provider 가 로그인 분기에만 있다. `App.test.tsx` 두 시험이 「로그아웃 → `closed` · 인스턴스 하나」 와 「CLOSED + 401 → 로그인 화면 · 다시 안 붙음」 을 단언한다. React 개발 모드의 효과 두 번 실행도 문제없다 — 채널을 효과 안에서 새로 만들고 정리에서 멈춘다
- 빈 단언은 없다. 새 시험 16(채널) + App 2 + 옮긴 대역 시험들이 순번 · URL · 횟수 · 지연(가짜 타이머)을 직접 단언한다

## 4. Code Surface 화면 줄 — 다시 grep

| 패턴(`F/`) | WORK 표(d2a06fa) | 지금 | 처분 |
|---|---|---|---|
| `useInboxStream\(` | 3 / 3 | 3 / 3 | 정의만 바뀌고 쓰는 두 곳은 무변경 |
| `new WebSocket` | 2 / 2 | **1 / 1** | 메시지함 것을 걷고 회의(`features/meetings/stream.ts:103`) 하나만 |
| `inboxStreamUrl` | 3 / 2 | **0** | `eventStreamUrl`(3 / 2)로 바뀜 |
| `new EventSource` | 0 | 1 / 1 | `lib/eventStream.ts` 만 — 연결은 한 곳에서만 만든다 |
| 허브 `createInboxEventHub\|hub.subscribe\|hub.emit` | 8 / 4 | 11 / 6 | 메시지함 허브 그대로 + 전역 `createEventHub` |
| `onReconnect` | — | 21 / 7 | 화면 쪽 의미(다시 읽기)는 그대로 · 입력이 `resync` 로 |
| `stubGlobal("WebSocket"` | 9 | **1**(`MeetingLive.test.tsx:261` — 회의) | 메시지함 · 설정 · App · SettingsLanding 시험이 `EventSource` 대역(13 / 6)으로 |
| 회의 WS · `src-tauri` | — | `git diff -- src/features/meetings src-tauri` = 0 | **무변경** |

## 5. 사람 눈에 이상해 보일 자리

| # | 자리 | 왜 | 처분 |
|---|---|---|---|
| ① | **옛 back 이 떠 있으면** 메시지함이 「실시간이 멈춘」 것처럼 보인다 | `/api/events/stream` 404 → CLOSED → `/api/auth/me` 200 → 백오프 → 10회(약 3분) 뒤 5분 간격. 화면에는 표시가 없다 | 워커 리포트 §5-1 대로 **백엔드 반영 뒤 스택 재시작**(P-4)이 먼저. 1루프 E2E 전 코디 확인 항목 |
| ② | 서버 재시작 직후 메시지함 · 설정 연동이 **한 번 깜빡이며 다시 읽힌다** | 다시 붙은 연결마다 다시 읽기 한 번(계약대로) | 정상 — 지금 WS 와 같다 |
| ③ | 연결이 끊긴 동안 **어디에도 표시가 없다** | 계약에 연결 상태 표시가 없다(지금 WS 도 없었다) | 참고 — 2루프 후보로만 |
| ④ | 세션이 서버에서 끝났는데 SSE 가 아직 붙어 있으면 로그인 화면으로 가지 않는다 | 서버는 시작할 때만 인가한다(WP1-BE 참고). 다음 REST 호출이 401 이 될 때 기존 길로 간다 | 참고 — 지금 WS 와 같다 |

## 6. 목록

### FAIL
없음.

### WARN
없음.

### 참고 (판정 밖 · 고치면 좋은 것)
- **R-1** 대역의 `lastEventId` 가 실물(직전 id 유지)과 다르다 — 지금 코드는 영향이 없지만, 나중에 다른 사건에서 `lastEventId` 를 읽게 되면 시험이 속는다. `FakeEventSource.emit` 이 `id` 가 없으면 직전 id 를 유지하게 하면 실물과 같아진다(`fakeEventSource.test-utils.ts:39-42`)
- **R-2** `seen` 집합(`eventStream.ts:98`)은 로그인 세션 내내 자란다(알림 수만큼 — 작다). 필요하면 최근 N 개만 들고 있어도 겹침 창(60초)에는 충분하다
- **R-3** `getSession()` 이 200 인데 본문이 비면 `null` → 세션 상실로 간다(워커 리포트 §5-5). 실제 `/api/auth/me` 는 200 이면 프로필을 주므로 생기지 않는다
- **R-4** `make frontend-build`(WORK 시험 줄)는 이번에 돌리지 않았다 — `tsc --noEmit` 0 이 같은 타입 근거다. 빌드는 코디의 마지막 확인으로

### 사용자에게 물을 것
없음.
