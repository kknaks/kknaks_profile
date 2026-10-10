# 알림 조사 (frontend)

- 대상: `/Users/kknaks/orca/workspaces/Strong_hajin/strong-hajin-notify` @ `d2a06fa` (origin/main) — 읽기 전용
- 줄 번호는 `frontend/` 기준 상대경로(`src/…`, `src-tauri/…`)다. 시안은 `handoff/…`(= `reference/2026-09-10-sc-meeting/package 2/handoff/`)로 줄인다
- 테스트·빌드·cargo 는 돌리지 않았다. 코드·워크트리는 바꾸지 않았다

## 0. 한 줄 요약

- **A. 화면의 알림** — 「알림」이라는 데이터를 그리는 화면이 **없다.** `getNotifications`·`markNotificationRead`(`src/lib/api.ts:726-732`)와 `Notification` 타입(`src/lib/viewModels.ts:1024-1037`)은 정의만 있고 **부르는 곳이 0** 이다. 사이드바 「알림」 줄은 `disabled: true` 고정(`src/App.tsx:457`)이고 점(dot)은 넘기지 않는다. 앱 안의 짧은 알림은 전역 토스트 한 통(`src/App.tsx:137-150`·`:655-670`)뿐이다.
- **B. 실시간 수신** — 사용자 사건 채널 `/api/inbox/stream` 은 **WebSocket** 이다(SSE 아님 · `src/lib/api.ts:1754-1757`). **전역 연결이 없다** — 메시지함 화면(`InboxPage.tsx:157`)과 설정 화면(`SettingsPage.tsx:182`)이 **화면마다 따로** 연다. 화면을 옮기면 그 화면이 언마운트되어 연결이 닫힌다. 다른 화면(홈·업무·캘린더…)에 있을 때는 열린 사용자 사건 연결이 **0개**다. 받는 사건 종류는 넷이다.
- **C. 설정** — 메뉴 「계정 > 알림 설정」은 자리만 있고 `disabled`(`SettingsPage.tsx:51`, D-37)다. 시안 알림 절의 **CSS(`.scax-switch*`)는 이미 `src/styles/settings.css:57-65` 에 옮겨져 있다.** 하지만 Switch **컴포넌트는 없다**(tsx 사용처 0). DS 의 FormControls 는 「Toggle 은 자리가 없어 만들지 않았다」고 적어 두었다(`src/ds/FormControls.tsx:9`). 시안에서 사이드바 `알림`을 누르면 무엇이 열리는지는 **시안에 없다.**
- **D. Tauri 셸** — OS 알림 수단이 **없다.** `tauri-plugin-notification` 의존이 없고, 알림 커맨드·capability 도 없다. Info.plist/Entitlements 에도 알림 관련 키가 없고, Windows AUMID 설정도 없다. 웹이 셸을 부르는 길은 strong-hajin 4개·medi-ax 7개 커맨드다(capability 의 `remote.urls` 한 origin). 셸이 웹에 보내는 길은 `window.eval` 로 DOM `CustomEvent` 를 쏘는 다운로드 사건 **1종**뿐이다. 창을 닫으면 웹뷰가 **실제로 파괴**된다. strong-hajin 은 프로세스도 끝나는 것으로 보이고(Tauri 기본 동작 — 실측 필요), medi-ax 는 트레이 프로세스만 남고 웹뷰는 없다.

---

## 1. A. 지금 화면의 알림

### A-1. 알림을 어디서 받고 어디에 그리나

| 자리 | 사실 | 근거 |
|---|---|---|
| API 함수 | `getNotifications()` → `GET /api/notifications`, `markNotificationRead(id)` → `POST /api/notifications/{id}/read` | `src/lib/api.ts:726-732` |
| 호출처 | **0** — 두 함수를 import 하는 파일이 없다(정의 줄 1건만 잡힘) | grep §N+1 |
| 타입 | `Notification { notification_id, kind: "meeting.shared" \| "work_request.received" \| "work_request.accepted" \| string, summary, actor_id, resource{type: "meeting"\|"work_request", id, version, title}, created_at, read_at }` | `src/lib/viewModels.ts:1024-1037` |
| labels | 사이드바 문구 `notifications: "알림"`, `notificationsDisabledHint: "알림은 아직 준비 중입니다."` | `src/lib/labels.ts:768-770` |
| labels(설정) | `menu.notify: "알림 설정"`, `notifyOutOfScope: "알림 설정은 아직 준비 중입니다."` | `src/lib/labels.ts:1607-1609` |
| labels(제품 원칙 흔적) | 회의 공유 문구에 「이 제품은 알림을 보내지 않는다」 주석 | `src/lib/labels.ts:1062` · `src/lib/api.ts:1458` · `src/features/meetings/ShareModal.tsx:22` |
| App.tsx | 「알림」은 **사이드바 자리**(`:457`)와 **토스트 통**(`:126-150` · `:650-670`) 두 곳에만 나온다. `ProductSurface` 에 알림 화면이 없다(`src/lib/viewModels.ts:1`) | `src/App.tsx:126-150,447-460,650-670` |
| AppShell.tsx | 알림 관련 코드 없음. 슬롯은 `nav`·`children`, `AppHeader(title, actions)`, `AppBody(railLeft, railRight)` | `src/shell/AppShell.tsx:37-82` |

### A-2. 사이드바 `SideNav`

- 항목 타입 `NavItem { id, label, icon, href?, dot?, disabled?, onActivate? }` — **`dot` 속성은 이미 있다**(`src/shell/SideNav.tsx:25-43`). 그리기: `item.dot` 이면 글리프 옆에 `<span className="scax-nav-item__dot" />`(`:90-93`). CSS 는 5px 원, `--scax-color-accent`(`src/styles/shell.css:121-122`)
- **숫자 배지를 그리는 부품은 SideNav 에 없다.** `dot` 은 boolean 뿐이다. DS 에는 `Badge variant="count"`(빨간 원, `src/ds/Badge.tsx:15,38`)가 있다. 레일 머리 6곳에서 쓰지만 사이드바 줄에서는 쓰지 않는다(§N+1)
- 두 그룹: `utilityItems`(구분선 위, `:183-184`)와 `items`(`:185`)
- 「알림」 줄: `utilityItems` 의 `{ id: "notifications", label: shellNav.notifications, icon: "bell", disabled: true }`(`src/App.tsx:456-459`)
  - `disabled` 이면 `<button disabled>` 로 서서 클릭·키보드·탭 순서가 모두 막힌다(`src/shell/SideNav.tsx:103-109`). 색은 `--scax-color-ink-disabled`(`src/styles/shell.css:108-111`)
  - 주석이 「시안의 파란 점(안 읽은 것)은 셀 값이 없으므로 넣지 않는다」고 적어 두었다(`src/App.tsx:450-451`)
  - `bell` 글리프는 들여와 있다(`src/ds/icons/glyphs.tsx:139-140`)
- 주 메뉴 매핑 `visibleNavigation.map(item => ({id,label,icon,disabled}))`(`src/App.tsx:441`)은 **`dot` 을 넘기지 않는다**. 시안의 `메시지함` 점(`handoff/shell/js/nav.js:16` `dot: true`)도 지금 코드에 없다
- 시안 `alert` 항목(`handoff/shell/js/nav.js:5`)은 코드에서 `notifications` id 로 **있다.** 다만 비활성이고 점이 없다
- 테스트: `src/shell/AppShell.test.tsx:65-66`(「알림」 버튼이 disabled 인지 단언)

### A-3. 수신함 레일(`InboxRail`)과 「참고」

- `InboxRail` 은 업무 화면(`src/features/work/MyWorkPage.tsx:1030`)의 좌 레일이다. 원천은 **업무 요청**이다: `getWorkRequestInbox()`(`src/lib/api.ts:541`)와 권한 안의 요청 목록을 `requestInboxItems` 로 합친다(`src/features/work/requestInbox.ts:21-33` · `MyWorkPage.tsx:294-312,963-966`). 주석: 「업무 요청과 CC 요청만 담는다」(`src/shell/InboxRail.tsx:15`)
- **알림(`/api/notifications`)과 같은 데이터를 쓰지 않는다** — 레일은 notifications API 를 부르지 않는다
- 갈래 필터: `SegmentedControl` 전체/업무/참고(`InboxRail.tsx:37-38,110-112`). 머리 건수: `Badge variant="count"`(`:108`)
- 읽음 처리:
  - `[읽음]` 단추는 **참고 갈래이고 내가 참조자일 때만** 그린다(`requestInbox.ts:14-18` · `InboxRail.tsx:79-92`)
  - 카드를 **여는 것도 읽음**이다 — `open()` 이 `onOpen` 다음 `onRead` 를 부른다(`InboxRail.tsx:41-44`)
  - `readReference` → `markWorkRequestRead`(`POST /api/work-requests/{id}/read`, `src/lib/api.ts:671-672`). 성공하면 목록에서 빼고 `readLocally` 에 담는다. 실패하면 남겨 두고 토스트를 띄운다. 연타는 잠근다(`MyWorkPage.tsx:979-997`)
  - 성공 토스트는 없다(`InboxRail.tsx:74-78`)
- 별개로 **메시지함**(`src/features/inbox/`)에는 메일·방 안 읽음이 있다: `unread_counts`(`InboxPage.tsx:115`), 카드 `unread`/`unread_count`, `markInboxMailRead`/`markInboxRoomRead`(`InboxPage.tsx:180-208` · `src/lib/api.ts:1676,1681`). 레일 머리 `Badge variant="count"`(`src/features/inbox/MessageRail.tsx:80,170`)
- 테스트: `src/shell/InboxRail.test.tsx` · `src/features/work/InboxRead.test.tsx` · `src/features/work/requestInbox.test.ts`

### A-4. 앱 안에서 짧게 알리는 부품

- DS `Toast`(`src/ds/Modal.tsx:262-353`): `message`·`onClose`·`action?`·`tone?: success|error`·`icon?`·`closeLabel`·`persist?`. 4초 뒤 스스로 닫히고 `persist` 면 남는다(`:322-326`). `role=alert`(error)/`status`(그 밖) · `aria-live=polite`(`:328-333`)
- **전역 레이어 1곳**: App 의 `notices` 상태, 갈래(error/success/stale)마다 한 줄씩(`src/App.tsx:137-150`). `.scax-toast-stack`(`src/App.tsx:655-670` · `src/styles/components.css:338-341`)
  - 넣는 길: `setError`/`setToast`/`setStaleProjection` → `putNotice`. 화면에는 `onError`/`onNotice` prop 으로 내려간다(`src/App.tsx:393,403`)
- 화면이 따로 그리는 Toast 2곳: `src/features/org/OrgPage.tsx:458` · `src/features/meetings/AttachModal.tsx:171`
- 메시지함 연동 끊김(D-50)은 토스트가 아니라 **머리 `[!]` 배지 + `Popover`**다(`src/features/inbox/InboxPage.tsx:50-64,277-278`)
- 테스트: `src/ds/Modal.test.tsx` · `src/ds/Overlays.test.tsx` · `src/App.test.tsx`

---

## 2. B. 실시간 수신

### B-1. 연결을 어디서 열고 몇 개 여나

- 주소: `inboxStreamUrl()` = `ws(s)://{location.host}/api/inbox/stream` — **WebSocket, 같은 origin**(`src/lib/api.ts:1753-1757`). SSE(`EventSource`)는 코드 어디에도 없다(grep 0)
- 훅: `useInboxStream(onEvent, {enabled?, onReconnect?})`(`src/features/inbox/inboxStream.ts:16-69`). **훅을 부를 때마다 소켓이 1개씩** 열린다(`:32`)
- 부르는 곳 **2곳**:
  1. `InboxPage` — `useInboxStream(onEvent, { onReconnect: loadList("quiet") })`(`src/features/inbox/InboxPage.tsx:157`)
  2. `SettingsPage` — `integration.changed` 만 본다(`src/features/settings/SettingsPage.tsx:182-187`)
- 연결 소유자: **화면별**이다. App 은 화면을 `surface === "inbox" && <InboxPage…>` 식 **조건부 렌더**로 그린다(`src/App.tsx:570,585`). 그래서 화면을 옮기면 언마운트 → cleanup 이 소켓을 닫는다(`inboxStream.ts:60-67`)
  - 화면을 옮기면 연결이 **유지되지 않는다.** 두 화면은 동시에 뜨지 않으므로 사용자 사건 소켓은 **최대 1개**, 그 밖의 화면에서는 **0개**다
  - 전역(App·AppShell) 수준의 사용자 사건 구독은 없다
- 나눠 주기: `InboxPage` 가 `createInboxEventHub()`(`inboxStream.ts:72-88`)로 만든 통에 `hub.emit(event)` 한다(`InboxPage.tsx:153`). 듣는 자식은 4곳: `MailView.tsx:294` · `RoomView.tsx:460`(보내기 결과) · `:526`(스레드 패널) · `:646`(방 본문)
- 같은 파일 규약상 WebSocket 을 만드는 다른 곳은 회의 스트림 `src/features/meetings/stream.ts:103`(회의 오디오·스크립트 전용, 다른 길 — `api.ts:1753` 주석 「회의 WS 와 다른 길」)

### B-2. 받는 사건 종류와 화면이 하는 일

사건 모양: `InboxStreamEvent { v, type, member_id, integration_id?, room_id?, message_id?, source_kind?, data? }` — 본문은 싣지 않는다(`src/lib/viewModels.ts:1688-1699`). 파싱 실패나 `type` 이 문자열이 아니면 버린다(`inboxStream.ts:41-47`).

| type | 화면이 하는 일 | 근거 |
|---|---|---|
| `inbox.message_arrived` | 메시지함 목록을 400ms 모았다가 조용히 다시 읽는다. 열린 방·스레드가 그 `room_id` 면 다시 읽는다 | `InboxPage.tsx:148-151` · `RoomView.tsx:529,649` |
| `inbox.reply_result` | 보낸 답장의 `data.local_id`·`data.status`(sent/failed)로 로컬 줄 상태를 바꾼다. 메일 답장 창은 settle | `RoomView.tsx:461-466` · `MailView.tsx:295` |
| `integration.changed` | 메시지함: 연동 목록 다시 읽기(→ `[!]` 배지). 설정: 연동 다시 읽기 | `InboxPage.tsx:152` · `SettingsPage.tsx:184` |
| `inbox.message_updated` | 그 방(`room_id`) 또는 그 메일(`!room_id && message_id`)을 다시 읽어 「업무 만듦」 표지를 세운다 | `MailView.tsx:297` · `RoomView.tsx:529,649` |
| 그 밖의 문자열 | 타입상 `\| string` 이라 받지만 아무 일도 하지 않는다(분기 없음) | `viewModels.ts:1692` |

업무 상태 변경·업무 요청·회의 공유 같은 **업무 사건은 이 채널로 받는 코드가 없다**(위 넷이 전부). 업무 화면들은 사건을 받는 대신 명령 뒤 `refreshProjections` 로 다시 읽는다(`src/App.tsx:341-350`).

### B-3. 끊김·재연결·로그아웃

- 끊기면(`onclose`) 물러서며 다시 붙는다: 2s → 4s → 8s → 16s → 30s 상한(`inboxStream.ts:49-58`). 다시 붙은 `onopen` 에서 `attempt > 0` 이면 `onReconnect` 를 1회 부른다 — 메시지함은 목록 다시 읽기, 설정은 `load(true)`(`:37-40` · `InboxPage.tsx:157` · `SettingsPage.tsx:186`)
- **닫힘 코드를 구분하지 않는다** — 인증 실패로 닫혀도 같은 백오프로 계속 재시도한다(`inboxStream.ts:49-52`). 이와 달리 회의 스트림은 `4401` 을 `unauthorized` 로 가르고 App 의 `onSessionLost` 로 로그인 화면에 보낸다(`src/features/meetings/stream.ts:89-92` · `src/App.tsx:522-526`)
- 로그아웃: `endSession` → `resetWorkspace()` + `setSession(null)`(`src/App.tsx:259-279`) → `session === null` 이면 `LoginPage` 만 렌더(`:417-425`) → 화면이 언마운트되면서 소켓 cleanup(`closed = true` · 타이머 해제 · `onclose = null` 후 `close()`)
- `WebSocket` 이 없는 환경이면 아무것도 하지 않는다(`inboxStream.ts:24`) — 테스트 9곳이 `vi.stubGlobal("WebSocket", …)` 으로 이를 쓴다(§N+1)

---

## 3. C. 설정 화면

### C-1. 구조와 「알림 설정」 자리

- 진입: 사이드바 `utilityItems` 「설정」(`src/App.tsx:458`) → `surface="settings"` → `SettingsPage`(`src/App.tsx:585-600`). OAuth 콜백 `?surface=settings&tab=…&connect=…` 으로 첫 화면이 될 수 있다(`src/App.tsx:69-84`). `SettingsLanding` 은 이 경로의 **테스트 파일 이름**(`src/SettingsLanding.test.tsx`)이고 별도 컴포넌트는 없다
- 틀: 좌 레일(`SetNav`)을 `onRegisterRails` 로 셸 슬롯에 등록하고, 본문은 탭별 섹션이다(`SettingsPage.tsx:197-215`). 머리 제목은 메뉴 이름이다(`onRegisterTitle`)
- 메뉴(`SettingsPage.tsx:38-54`):
  - `연동`: 메일 연동 · 슬랙 연동 · 카카오톡 연동
  - `계정`: 프로필 설정 · **알림 설정 `{ id: "notify", disabled: true }`**
- 「알림 설정」: **보이지만 비활성**이다. `<button disabled>` + `title=notifyOutOfScope`(「알림 설정은 아직 준비 중입니다.」)를 달고, `onClick` 에서도 `notify` 를 거른다(`:62-76`). `SettingsTab` 타입에 `notify` 가 없다(`:36` — `"mail" | "slack" | "kakao" | "account"`). 콜백 쿼리 `tab=` 도 넷만 받는다(`src/App.tsx:73-74`)
- 근거 결정: 파일 머리 주석 「알림 설정은 이번 범위 밖이라(D-37) 자리만 선다」(`SettingsPage.tsx:31`) · DEC-008 D-37 · D-50
- 테스트: `src/features/settings/SettingsPage.test.tsx:355-358`(「알림 설정」 disabled 단언) · 같은 파일 `:162-180`(stream `integration.changed`)

### C-2. 시안 알림 설정 대조 → §N 표

### C-3. 사이드바 `알림`(bell · dot)을 누르면

- **시안 없음.** `handoff/shell/js/nav.js:5` 의 `alert` 항목에는 `href` 가 없다. 시안 SideNav 는 `href` 도 `onSelect` 도 없으면 `aria-disabled="true"` 로 선다(`handoff/shell/js/scax-ui.jsx:231-233`). 핸드오프 폴더(calendar·files·inbox·meetings·my-work·projects·settings·shared·shell)에 알림 화면·패널 파일이 없다
- 시안 문구 중 알림 표시처를 가리키는 것은 설정 `받는 경로 > 앱 알림`의 설명 「수신함과 좌측 알림에 표시」 하나다(`handoff/settings/js/data.js:86`)

---

## 4. D. Tauri 셸 — 시스템 알림을 띄울 길

### D-1. `src-tauri/` 현재 구조

- 파일: `src/{lib.rs 1077, download.rs 732, power.rs 543, guard.rs 364, connection.rs 203, config.rs 168, shell_ui.rs 160, main.rs 6}` + `src/kakao/{client, collector, commands, crypto, db, keychain, mod, tray}.rs`(medi-ax 전용)
- 플러그인 등록: **`tauri_plugin_opener` 하나**(`src-tauri/src/lib.rs:609`). URI 스킴 `stronghajin://`(셸 자기 화면, `:611-640`)
- 커맨드 등록(`lib.rs:683-699`):
  - medi-ax(`feature = "kakao-collector"`): `shell_info`·`wake_guard_acquire`·`wake_guard_release`·`open_external`·`kakao_list_rooms`·`kakao_collector_status`·`kakao_store_device_token` = **7**
  - strong-hajin: 위 앞 넷 = **4**
- `shell_info` 의 `features: ["wake_guard", "open_external"]`(`lib.rs:210`) — 웹은 이 목록으로 기능을 판단한다는 주석
- `Cargo.toml` 의존: `tauri 2.11.1`(features 없음)·`tauri-plugin-opener 2`·`serde`·`serde_json`·`native-tls 0.2`·`ureq 3.4.2`(native-tls)·win `webview2-com 0.38`. 선택 의존(kakao-collector): `rusqlite(sqlcipher)`·`keyring(apple-native)`·`sha1`·`sha2`·`pbkdf2`·`base64`·`plist`, feature 가 `tauri/tray-icon`·`tauri/image-png` 를 켠다(`src-tauri/Cargo.toml:14-116`)
- `capabilities/`: **루트에는 없다.** 판마다 `flavors/<판>/capabilities/product-shell.json` 하나씩이다. build.rs 가 `./flavors/{flavor}/capabilities/**/*` 를 쓰고 앱 커맨드 ACL 을 자동 생성한다(`src-tauri/build.rs:138-161`)
- `flavors/`:
  - `strong-hajin/tauri.conf.json`: productName `Strong Hajin` · identifier `app.stronghajin.desktop`
  - `medi-ax/tauri.conf.json`: productName/mainBinaryName `medi-ax` · identifier `app.ax.desktop`
  - `strong-hajin/shell.config.json`: `operationalOrigin: null`(OQ-T02 미정 → 「서버 주소가 설정되지 않았습니다」 화면)
  - `medi-ax/shell.config.json`: `operationalOrigin: "https://ax.medisolveai.xyz"`
  - 두 판 모두 `navigationAllowlist: []`
  - `product-shell.json`: `windows: ["main"]` · `local: false` · `remote.urls` 1개(strong-hajin 은 `https://operational-origin-not-yet-decided.invalid/*`, medi-ax 는 `https://ax.medisolveai.xyz/*`) · permissions 는 위 커맨드 수와 같다(4 / 7)
- 루트 `tauri.conf.json`: `app.windows: []`(창은 코드가 만든다) · `withGlobalTauri: false` · `bundle.macOS.infoPlist`/`entitlements` 지정 · `frontendDist: shell-noop`

### D-2. 웹 → 셸 커맨드 경로

- 허용 방식: tauri 2.11 은 원격 문서(`is_local == false`)의 **앱 커맨드도 ACL 로 막는다.** capability 의 `remote.urls` origin 에서 온 문서만, permissions 에 적힌 커맨드만 부를 수 있다(`src-tauri/build.rs:1-6` · `Cargo.toml:16-19` 주석). `local: false` 라 셸 자기 화면(`stronghajin://`)은 커맨드를 못 부른다(`product-shell.json` description)
- 로컬 실행(`make tauri-local`)은 임시 판 폴더를 복사하고 `capability.remote.urls` 를 로컬 origin 으로 바꿔 쓴다(`scripts/run-tauri-local.mjs:93-96`)
- 셸 테스트가 판별 커맨드 수·허용 origin 하나·와일드카드 서브도메인 금지·판 정합을 지킨다(`src-tauri/src/lib.rs` tests `웹에_여는_커맨드가_판에_맞다` · `커맨드_허용_origin_은_하나이고…` · `판마다_운영_origin_은…` — 테스트 블록 `:721-` 중 `:844-930` 부근)
- 웹 쪽:
  - **`src/lib/shell.ts` 가 `invoke` 를 부르는 유일한 자리**다(파일 머리 `:1-15` · `call()` `:96-100`). `@tauri-apps/api/core` 를 늦게, 한 번만 import 한다(`:84-94`)
  - 예외로 개발 탐침 `src/dev/probeShell.ts:37-44` 도 invoke 한다(제품 경로 아님)
- 「Tauri 안인가」 판별: `hasShell()` = `typeof window.__TAURI_INTERNALS__ !== "undefined"`(`src/lib/shell.ts:64-72`). 셸이 없으면 호출을 만들지 않는다. 카톡 커맨드는 별도로 「커맨드가 있는지」(`kakao_collector_status` 를 불러 봄)로 판정하고 결과를 기억한다(`:256-268`)
- 셸 기능을 쓰는 웹 자리: `App.tsx:22,153`(다운로드 사건 · openExternal) · `features/meetings/stream.ts:5`(wake guard) · `features/settings/{SettingsPage.tsx:19, KakaoSection.tsx:7, consent.ts:2}` · `features/inbox/{inboxStream.ts:4, InboxAttachments.tsx:5,208}` · `lib/shellDownloads.ts:3,62`

### D-3. 셸 → 웹 사건 경로 (딥링크에 쓸 수 있는 기존 경로 사실)

- **1종**: 첨부 저장 결과. Rust `notify_download` → `window.eval(download::event_script(ok, filename))` → `window.dispatchEvent(new CustomEvent("strong-hajin:download", { detail: {ok, filename} }))`(`src-tauri/src/lib.rs:350-362` · `src-tauri/src/download.rs:26-27,474-478`)
  - 권한이 필요 없는 길이라 capability 를 바꾸지 않는다는 주석이 있다(`lib.rs:351`)
  - 창의 현재 URL origin 이 **앱 origin 일 때만** 보낸다(`lib.rs:352-358`)
- 웹 수신: `onShellDownload(handler)` — 셸이 있을 때만 `addEventListener(SHELL_DOWNLOAD_EVENT)`(`src/lib/shell.ts:216-243`). 받는 곳: App 토스트(`src/App.tsx:151-159`) · 「받는 중」 표시(`src/lib/shellDownloads.ts`)
- 이름 일치는 Rust 테스트가 지킨다 — `download.rs` `사건_이름이_웹_수신부와_같다`(`:725-731`). 이 테스트는 `shell.ts` 의 `SHELL_DOWNLOAD_EVENT = "…"` 문자열을 대조한다
- 웹 안 화면 이동 수단: 라우터·URL 경로가 없다. 화면은 App 상태 `surface` + 포커스 상태(`focusTaskId`·`focusWorkRequestId`·`focusMeetingId`·`focusProjectId`·`inboxFocus`)로 연다(`src/App.tsx:87-121`). 그 예로 AX 서랍의 `onOpenResource`(`src/App.tsx:694-754`)가 task/work_request/meeting/material/project/report 별로 화면과 포커스를 고른다. URL 쿼리로 첫 화면을 고르는 길은 `?surface=settings&tab=&connect=`(`src/App.tsx:69-84`)와 `?interaction=`(`:87`) 둘이다
- SPEC-006 §2.5 의 「딥링크 경로가 이미 있다」는 표현이 가리키는 구체 경로는 코드에서 위 쿼리 랜딩 외에 찾지 못했다(조사 한계)

### D-4. OS 알림 수단

- `tauri-plugin-notification`: **없음**(Cargo.toml · package.json `@tauri-apps/*` 는 `api`·`cli` 둘뿐 — `package.json:57,70`)
- Cargo.lock 의 `objc2-user-notifications` 는 `objc2-ui-kit`(iOS UIKit)의 전이 의존이다(`Cargo.lock:2479-2490` 부근). 우리 코드가 쓰지 않는다
- 셸에 알림 커맨드·`features` 항목·capability 권한이 없다(`lib.rs:210,683-699` · `product-shell.json`)
- `Info.plist`: `NSMicrophoneUsageDescription` 하나뿐 — 알림 관련 키 없음(`src-tauri/Info.plist`)
- `Entitlements.plist`: `com.apple.security.device.audio-input` 하나뿐(`src-tauri/Entitlements.plist`). 주석 「서명·공증 자체는 이번 Phase 가 만들지 않는다(OQ-T03)」
- 서명: Makefile 주석 「서명은 APPLE_SIGNING_IDENTITY 를 환경으로 주면 tauri 가 한다」(`Makefile:143`) — 저장소에 서명 identity·`signingIdentity`·`hardenedRuntime` 설정 키는 없다
- 번들 id: `app.stronghajin.desktop`(`src-tauri/tauri.conf.json` · `flavors/strong-hajin/tauri.conf.json`) / `app.ax.desktop`(`flavors/medi-ax/tauri.conf.json`)
- Windows: AppUserModelID·`windows` 번들 절 설정 **없음**(tauri.conf 에 `bundle.windows` 키 없음). Windows 전용 코드는 WebView2 마이크 권한(`lib.rs:248-283`)뿐이다

### D-5. 창을 닫거나 숨기면

- 창은 `spawn_main_window` 한 곳에서 만든다. 라벨 `main`, 1280×860, `incognito(false)`(`lib.rs:381-405`)
- `WindowEvent::CloseRequested` 는 **로그만** 남긴다 — `prevent_close`·`hide` 없음(`lib.rs:557-561`). 그러므로 닫기 = 창(웹뷰) 파괴 → `Destroyed` 에서 점유 정리(`:562-566`)
- 코드에 창 `hide()`/숨김 처리가 없다(grep). 트레이 「열기」의 `window.show()`(`src-tauri/src/kakao/tray.rs:52-54`)만 있다
- **strong-hajin**: `app.run` 콜백이 아무것도 하지 않는다(`lib.rs:707-714`) — 마지막 창이 파괴되면 Tauri 기본대로 프로세스가 끝나는 것으로 읽힌다(실측 필요). 트레이·백그라운드 없음
- **medi-ax**: `RunEvent::ExitRequested` 에서 `should_prevent_exit()` 이면 `prevent_exit()`(`lib.rs:707-713` · `tray.rs:22-25`). 프로세스와 수집기 스레드는 메뉴 막대에 남고 **웹뷰는 없다.** 「열기」가 창을 새로 만들고(`tray.rs:50-57` · `lib.rs:662-676`), 「종료」만 끝낸다(`tray.rs:59-62`)
- `shell_ui.rs` 는 셸 자기 화면 HTML(연결 실패·미설정)만 만든다 — 창 수명 처리 없음(`src-tauri/src/shell_ui.rs:1-60`)
- `guard.rs` 는 점유 장부(창 라벨별 세션) · 입력 검증 · 네비게이션 판정이다. 창 수명은 `clear_window`(장부 정리)뿐이다(`src-tauri/src/guard.rs:38-104,176-`)
- 문서 교체(`PageLoadEvent::Started`)도 점유를 푼다(`lib.rs:526-531`)
- 정리하면 코드 기준 「앱이 켜져 있고 웹이 돈다」 = **`main` 웹뷰 창이 존재하는 상태**(보임·최소화·가려짐 포함). 창을 닫으면 두 판 모두 웹뷰가 없어 웹 JS·WebSocket 도 없다. medi-ax 트레이 상주는 Rust 수집기만 돈다

### D-6. 포커스 없음·숨김에서 연결·타이머

- 셸 쪽: 웹뷰 백그라운드 스로틀 관련 설정이 없다(`backgroundThrottling` 등 grep 0 · tauri.conf · lib.rs builder)
- 웹 쪽 `useInboxStream` 은 `visibilitychange`·`focus` 를 보지 않는다 — 문서가 숨어도 스스로 소켓을 닫지 않는다(`inboxStream.ts:23-68`)
- `visibilitychange` 를 보는 곳은 3곳이다: 설정 연동 다시 읽기(`SettingsPage.tsx:170-179`), AX 캐릭터 표시(`AssistantCharacter.tsx:63-67`), 회의 녹음 점유 재요청(`meetings/stream.ts:289,402`)
- 타이머로 도는 곳(setInterval/setTimeout 폴링): `MailView.tsx:316` · `TodayPage.tsx:146` · `DailyReportPage.tsx:245` · `WorkModals.tsx:985` · `MeetingDetailPage.tsx:441,449` · `MessageList.tsx:516` · `BrowserRecordingPage.tsx:88` · `useConversations.ts:226-232`(800ms). 숨김에서 이들이 스로틀되는지는 코드로 가를 수 없다(§N+2)

### 공통 — 테스트 위치

| 자리 | vitest / cargo test |
|---|---|
| 사이드바 알림 줄 | `src/shell/AppShell.test.tsx:65-66` |
| 설정 알림 메뉴 · 설정 stream | `src/features/settings/SettingsPage.test.tsx:88,162-180,355-358` · `src/SettingsLanding.test.tsx:19,36` |
| 메시지함 stream(FakeSocket) | `src/features/inbox/InboxPage.test.tsx:153,492,506` |
| App 전역(토스트·셸 다운로드·WS stub) | `src/App.test.tsx`(`:2516` WS stub 외) |
| 토스트 부품 | `src/ds/Modal.test.tsx` · `src/ds/Overlays.test.tsx` |
| 업무 수신함 레일·읽음 | `src/shell/InboxRail.test.tsx` · `src/features/work/InboxRead.test.tsx` · `src/features/work/requestInbox.test.ts` |
| 셸 브리지 | `src/lib/shell.test.ts` · `src/lib/shellKakao.test.ts` · `src/features/inbox/InboxAttachments.test.tsx` |
| 회의 stream(4401 등) | `src/features/meetings/MeetingLive.test.tsx:261` |
| labels | `src/lib/labels.test.ts` |
| cargo test 모듈(`#[test]` 수) | `lib.rs` 15(커맨드·capability·판 정합·소스 문자열 검사 포함) · `download.rs` 19(사건 이름 대조 `:725`) · `guard.rs` 16 · `power.rs` 7 · `config.rs` 6 · `connection.rs` 5 · `shell_ui.rs` 5 · kakao: `crypto` 6 · `db` 6 · `collector` 4 · `client` 4 · `mod` 3(live `#[ignore]` 포함) · `keychain` 2 · `tray.rs`/`commands.rs` 0 |

`notifications` API(`getNotifications`·`markNotificationRead`)와 `Notification` 타입을 다루는 테스트는 **0** 이다.

---

## N. 시안 대조표

### N-1. 사이드바 알림

| 항목 | 시안 | 지금 코드 | 부품 |
|---|---|---|---|
| 자리 | `NAV_PRIMARY` 첫 줄, 설정 위(`handoff/shell/js/nav.js:4-7`) | `utilityItems` 첫 줄(`src/App.tsx:456-459`) | 있음(`SideNav` `utilityItems`) |
| id / 라벨 / 글리프 | `alert` / 알림 / `bell` | `notifications` / `shellNav.notifications`="알림" / `bell` | 있음(`glyphs.tsx:139`) |
| 점(dot) | `dot: true` | 넘기지 않음(주석 「셀 값이 없으므로」 `App.tsx:450-451`) | 있음(`NavItem.dot` · `.scax-nav-item__dot`) |
| 숫자 배지 | 시안에 없음 | 없음 | 사이드바용 없음(DS `Badge variant="count"` 는 있음) |
| 누름 동작 | `href` 없음 → `aria-disabled`(`scax-ui.jsx:231-233`) · **열리는 화면 시안 없음** | `<button disabled>`(진짜 비활성) | — |
| 메시지함 점 | `inbox` 에 `dot: true`(`nav.js:16`) | 주 메뉴 매핑이 `dot` 을 버림(`App.tsx:441`) | 있음 |

### N-2. 설정 알림 (`handoff/settings/js/settings.v1.jsx:681-710` · `data.js:66-89` · `settings.css:59-66`)

| 시안 요소 | 시안 내용 | 지금 코드 | 부품 유무 |
|---|---|---|---|
| 메뉴 항목 | `계정 > 알림 설정`(`settings.v1.jsx:16-19`) | 있음, `disabled`(`SettingsPage.tsx:51`) | 있음 |
| 머리 제목 | 「알림 설정」(`settings.v1.jsx:851`) | 탭 없음(`SettingsTab` 에 `notify` 없음) | `onRegisterTitle` 있음 |
| 소개 줄 | 「받을 알림과 받는 경로를 따로 정한다.」(`:684`) | 없음 | `.scax-set-view__intro` CSS 있음(`settings.css:18`) |
| 상자 | `Card title=…`(`:685,696`) | — | `settingsParts.tsx:12` `Card` 있음 |
| 행 | `.scax-switch-row` + `__who` + `.scax-set-row__name/__meta`(`:687-691`) | — | CSS 있음(`settings.css:58-60` · `.scax-set-row__*` 있음) |
| 스위치 | `Switch` = `<button role="switch" aria-checked>` + `__knob`(`settings.v1.jsx:70-75`) | **컴포넌트 없음**(`scax-switch`·`role="switch"` tsx 사용 0) | CSS 만 있음(`settings.css:61-65`). DS 「Toggle(36×20) 만들지 않았다」(`FormControls.tsx:9`) · DS 문서 `docs/design/design-system-v2.dc.html:914` 「Toggle · 36 × 20」 규격 존재 · 시안 CSS 는 40×22 → **DS-gaps 후보** |
| 받는 경로 | `앱 알림`「수신함과 좌측 알림에 표시」 on · `메일`「(주소)」 on · `슬랙 DM`「@(핸들)」 off(`data.js:85-89`) | 없음 | 문구 labels 없음 |
| 묶음 `업무` | 업무가 배정됐을 때「나에게 새 업무가 생기면 알립니다」 on · 기한 하루 전「마감 24시간 전에 한 번」 on · 내 업무에 댓글 off(`data.js:67-74`) | 없음 | — |
| 묶음 `회의 · 연동` | 회의록 정리 완료「에이전트가 정리를 마치면」 on · 연동 수집 실패「메일·슬랙·카카오 수집이 실패하면」 on · 일일 요약「매일 오전 9시」 off(`data.js:75-82`) | 없음(연동 실패는 D-50 대로 메시지함 `[!]` 배지 `InboxPage.tsx:277`) | — |
| 저장 방식 | 시안은 로컬 state 토글만(`settings.v1.jsx:845-848`) — 서버 저장 시안 없음 | — | — |

---

## N+1. grep 개수표

`src/**/*.{ts,tsx}` 기준, 「제품 / 테스트」. 정규식 그대로.

| 심볼 | 제품 | 테스트 |
|---|---|---|
| `getNotifications` | 1(정의만) | 0 |
| `markNotificationRead` | 1(정의만) | 0 |
| `/api/notifications` | 2(api.ts 정의 2줄) | 0 |
| `type Notification\b\|Notification[]\|<Notification>` | 5(viewModels 1 · api.ts 4) | 0 |
| `useInboxStream(` | 3(정의 1 · 호출 2) | 0 |
| `inboxStreamUrl` | 3 | 0 |
| `new WebSocket` | 2(inboxStream · meetings/stream) | 0 |
| `hub.subscribe` | 4 | 0 |
| `hub.emit` | 1 | 0 |
| `inbox.message_arrived` | 4 | 2 |
| `inbox.reply_result` | 4 | 3 |
| `integration.changed` | 3 | 3 |
| `inbox.message_updated` | 8 | 5 |
| `InboxStreamEvent` | 9 | 0 |
| `EventSource` | 0 | — |
| `stubGlobal("WebSocket"` | 0 | 9 |
| `<Toast` | 3(App · OrgPage · AttachModal) | 8 |
| `putNotice(` | 5 | 0 |
| `variant="count"` | 8(그리기 6 + 주석 2) | 0 |
| `dot?:` | 2(SideNav `NavItem` · CalendarRail `DayCell`) | 0 |
| `scax-nav-item__dot` | 1 | 0 |
| `shellNav.notifications` | 1 | 0 |
| `notifyOutOfScope` | 2 | 0 |
| `scax-switch`(tsx/ts) | 0 (CSS 9줄 `settings.css:57-65`) | 0 |
| `role="switch"` | 0 | 0 |
| `hasShell(` | 12 | 4 |
| `__TAURI_INTERNALS__` | 4 | 16 |
| `invoke(\|invoke<` | 2(shell.ts · dev/probeShell.ts) | 2 |
| `onShellDownload` | 6 | 3 |
| `SHELL_DOWNLOAD_EVENT\|strong-hajin:download` | 4 | 6 |
| Rust `generate_handler!` 커맨드 | 7(medi-ax) / 4(strong-hajin) | — |
| Rust `.plugin(` | 1(opener) | — |
| Rust `notification`(Cargo.toml·src) | 0 | — |
| Rust `window.eval` 셸→웹 사건 | 1(`notify_download`) | — |
| Rust `prevent_close`·`hide()` | 0 | — |
| Rust `prevent_exit` | 1(medi-ax) | — |
| vitest 파일 수(`src/**/*.test.*`) | — | 98 |

---

## N+2. 실측 필요 — 코드로 못 가르는 것

| 물음 | 판 · OS | 왜 코드로 못 가르나 |
|---|---|---|
| macOS 알림 권한 프롬프트·표시가 미서명/서명·번들 실행에서 각각 뜨는가, 알림 센터에 어떤 앱 이름·아이콘으로 서는가 | 두 판 · macOS (`app.stronghajin.desktop` / `app.ax.desktop`) | 알림 수단·Info.plist 키가 없다. 서명 identity 는 환경 변수로만 받는다(`Makefile:143`) |
| `tauri dev`(번들 아님) 실행에서 OS 알림이 번들 id 로 귀속되는가 | 두 판 · macOS | 실행 형태에 따라 다르다 — 코드에 근거 없음 |
| Windows 토스트가 AUMID 없이 설치본/개발 실행에서 뜨는가 | 두 판 · Windows | `bundle.windows`·AUMID 설정 없음 |
| strong-hajin 에서 마지막 창을 닫으면 프로세스가 끝나는가 | strong-hajin · macOS/Windows | `run` 콜백이 비어 Tauri 기본 동작에 맡긴다(`lib.rs:707-714`). 특히 macOS 는 Dock 에 남는지 확인 필요 |
| 창 최소화·다른 앱 뒤로 가려짐·데스크톱 전환에서 WKWebView / WebView2 가 WebSocket 을 유지하고 `setTimeout` 백오프·폴링을 제때 도는가(스로틀·정지) | 두 판 · macOS(WKWebView) · Windows(WebView2) | `backgroundThrottling` 설정·관련 코드 없음. 엔진 정책은 실측 사항 |
| 화면 잠금·잠자기 후 깨어났을 때 `/api/inbox/stream` 이 `onclose` 로 끊김을 알아채고 재연결·`onReconnect` 가 도는가 | 두 판 | 소켓 끊김 감지는 엔진·네트워크 동작 |
| 셸이 `window.eval` 사건을 보낼 때 웹뷰가 숨어 있거나 최소화된 상태에서도 전달되는가 | 두 판 | 기존 다운로드 사건은 사용자가 창 안에서 누른 직후라 숨은 상태의 근거가 없다 |
| medi-ax 트레이 상주(웹뷰 없음) 중에는 웹 실시간이 0 이 맞는가 | medi-ax · macOS | 코드상 웹뷰가 파괴되므로 0 으로 읽히지만, 실물로 확인되지 않았다 |
| 「켜져 있음」 = `main` 창 존재(최소화 포함)에서 실제 사용자 체감 | 두 판 | §D-5 의 코드 정의를 실물로 대조해야 한다 |

---

## N+3. 조사 한계

- 서버 쪽 `/api/notifications`·`/api/inbox/stream` 의 실제 응답·사건 종류·발행 조건은 보지 않았다(backend 워커 몫). 화면 쪽 타입(`viewModels.ts:1024,1689`)에 적힌 것만 옮겼다
- SPEC-006 §2.5 의 「딥링크 경로가 이미 있다」가 가리키는 구체 경로를 코드에서 특정하지 못했다. 쿼리 랜딩(`App.tsx:69-87`)과 상태 기반 포커스 seam 만 사실로 적었다
- Cargo.lock 의 전이 의존이 어떤 feature 로 실제 컴파일에 들어가는지는 `cargo tree` 를 돌리지 않아 확정하지 못했다(`objc2-user-notifications` 는 lock 상 `objc2-ui-kit` 의존으로만 확인)
- 테스트 단언의 세부(어떤 사건 시나리오를 덮는지)는 grep 개수와 대표 줄만 셌다. 파일 전체를 읽지 않았다
- 시안 `handoff/settings/css/settings.css` 와 우리 `src/styles/settings.css` 의 스위치 규칙은 줄 단위로 같은 값이다(시안 `:59-66` ↔ 우리 `:58-65`). 그 밖의 시안 CSS 와는 전수 diff 하지 않았다
- DS 문서 `docs/design/design-system-v2.dc.html` 의 Toggle 규격(36×20, `:914`)은 위치만 확인했고 시각 규격 전체를 읽지는 않았다
- WKWebView·WebView2 의 백그라운드 동작, OS 알림 권한, 서명 영향은 실행하지 않아 §N+2 로 넘겼다
