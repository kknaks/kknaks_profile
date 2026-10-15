# WORK-013 P0 조사 (frontend · 셸) — 2026-10-08

- 워크트리 `strong-hajin-notify`. 코드는 바꾸지 않았다(`git status -- frontend` 0줄). 빌드·cargo 는 돌리지 않았다
- 실명·본문·키·uuid·userId·chatId 는 출력하지도 기록하지도 않았다. 방은 A/B/C 로 쓴다
- 임시 사본(카톡 DB·키 파일)과 받아 본 크레이트 소스는 모두 scratch 에 두었고 끝난 뒤 지웠다

## §0 한 줄 요약

| 항목 | 판정 |
|---|---|
| **P0-1** 카톡 「내가 보냄」(OQ-K01) | **맞음.** 운영 logId 범위 안에서 `NTChatMessage.authorId == NTChatContext.userId` 줄 수가 방 A 7 · B 7 · C 2 = **16**. 운영 「author=본인」 16(코디 2026-10-08 값)과 방마다 같다. 방별 메시지 수(54·63·2)도 같다. ⚠ 고른 방 3개가 **로컬에서도 셋 다 단체방**이라 1:1 은 운영과 대조할 표본이 없다. 대신 로컬 1:1 방 349개 전수로 보조 확인했다(§1-4) |
| **P0-2** 클릭 콜백(OQ-1108) | **공식 `tauri-plugin-notification` 2.5.1(최신 안정 · 2026-10-01) · 3.0.0-alpha.2 둘 다 데스크톱 클릭 콜백 없음.** 문서는 「Actions API 는 모바일 전용」, 소스는 클릭 응답을 버린다. 대안은 셋이다. ① OS 기본 동작(앱만 앞으로) + 웹이 마지막 알림/목록으로 감 ② 플러그인 대신 `notify-rust` 를 직접 써서 클릭을 기다림 ③ 서드파티 `tauri-plugin-notifications` 0.4.6(UNUserNotificationCenter · `notificationClicked` 있음). 비용은 §2-3 |
| **P0-3** 권한·서명 | 공식 플러그인 데스크톱의 권한 API 는 **항상 `Granted`** 를 돌려준다(묻지 않음 · 실제 OS 상태도 모름). macOS 백엔드는 **NSUserNotification**(폐기 API)이고, **`tauri dev` 에서는 알림이 「터미널」 앱 이름으로 뜬다.** 번들 실행에서는 번들 id(`app.stronghajin.desktop`/`app.ax.desktop`)로 뜬다. 지금 문서·소스로 보이는 범위에서 Info.plist **필수 키는 없다**(알림 모양 키는 선택). UN 계열 대안은 권한 프롬프트와 번들(서명)이 필요하다. 실기 결과는 WP4. Windows 는 pending |

---

## §1. P0-1 카톡 「내가 보냄」 재료 (OQ-K01)

### 1-1. 방법 — 수집기와 같은 길을 읽기 전용 사본으로

수집기 코드를 따라 아래 순서로 했다. 실행 중인 카톡·medi-ax·수집기 프로세스에는 손대지 않았다.

| 단계 | 따른 코드 | 한 일 |
|---|---|---|
| 기기 UUID | `T/kakao/crypto.rs:80-105` `platform_uuid`(ioreg) | 같은 명령으로 읽음. 수집기 캐시 `~/Library/Application Support/app.ax.desktop/kakao_resolve.json`(`crypto.rs:341-363`)의 uuid 와 **같음** |
| user_id | `crypto.rs:368-395` `resolve`(캐시 → 검증) | 캐시 user_id 의 `db_name`(`crypto.rs:157-169`)이 **가장 최근 78-hex DB 파일명과 같음**(수집기와 같은 검증) |
| 키 | `crypto.rs:136-155` `secure_key` | 같은 식(PBKDF2-SHA256 100k · dklen 128)을 python 으로 옮겨 scratch 파일(600)에만 둠 |
| DB 열기 | `T/kakao/db.rs:93-121` `open`/`try_open` | 최신 DB 와 `-wal`·`-shm` 을 scratch 에 **복사**한 뒤 그 사본을 열었다. `cipher_default_compatibility=3` 으로 **열림**(compat 4 는 실패 — 수집기도 3을 먼저 쓴다) |
| 내 userId | `db.rs:126-131` `self_user_id`(`NTChatContext.userId`) | 캐시 user_id 와 **같음** |
| 셈 기준 | `db.rs:236-286` `fetch_messages` | 수집기처럼 `type <> 0`(시스템 줄 제외) · 방별 `logId` 범위 = 코디가 준 운영 최소~최대 |

판별 컬럼은 `NTChatMessage.authorId` 다(컬럼 전수: `chatId, logId, prevId, msgId, authorId, type, status, subType, scope, threadId, contentFlag, attachment, supplement, extra, message, readAt, sentAt, referer, revision, localFilePath` — `isMine`·`fromMe` 류 전용 컬럼은 **없다**).

### 1-2. 결과 — 운영 logId 범위 안

| 방 | 로컬 종류(`directChatMemberUserId>0` 이면 1:1) | 운영 메시지 수 | 로컬 범위 내 `type<>0` | 운영 author=본인 | 로컬 `authorId==나` | 판정 |
|---|---|---|---|---|---|---|
| A | 단체 | 54 | **54** | 7 | **7** | 맞음 |
| B | 단체 | 63 | **63** | 7 | **7** | 맞음 |
| C | 단체 | 2 | **2** | 2 | **2** | 맞음 |
| 합 | — | 119 | 119 | **16** | **16** | **맞음** |

- 브리프의 「본인 14건」은 어제 값이다. 코디가 준 지금 값은 16(새 메시지 유입)이고 로컬도 16이다
- `type=0` 을 빼지 않은 범위 내 전체 줄은 A 61 · B 65 · C 2 다. 운영 수와 같은 것은 수집기 규칙대로 `type<>0` 일 때다
- 범위 밖까지 센 방 전체 `authorId==나` 는 A 7 · B 7 · C 3 이다. C 의 1건은 운영 최대 logId 뒤의 줄이다(아직 안 올라갔거나 범위 밖)
- A 의 운영 최소 logId 10(코디 주의)으로 잡아도 셈이 맞았다. 범위 하한이 셈을 바꾸지 않았다

### 1-3. 1:1 / 단체 구분

- 운영 `room_type` 은 셋 다 group 이다(코디). 로컬 값으로도 **셋 다 단체방**이다 → 고른 방에 1:1 이 없어 **1:1 은 운영 대조 표본 0**

### 1-4. 1:1 보조 확인 (운영 대조 아님 · 로컬 전수)

오픈채팅을 뺀 1:1 방(`directChatMemberUserId>0 · linkId=0`) 중 메시지가 있는 방 **349개**, `type<>0` 줄 **286,015** 를 셌다:

- `authorId == 나` **150,038** 줄 · 내 줄이 있는 방 148
- `authorId == 상대(directChatMemberUserId)` — 상대 줄이 있는 방 349
- 둘 다 아닌 줄 **759** — **전부 `type=1999` · `authorId=0`**(177개 방). 운영에서 「author 없음 3건 · `raw.type` 1999:3」 과 같은 갈래다

→ 1:1 에서도 사람이 쓴 줄은 「나」 아니면 「상대」로 갈린다. `authorId==나` 로 가르는 데 예외가 보이지 않는다.

### 1-5. 판정이 다음 판에 주는 것(사실만)

- WORK-013 WP4 「카톡 수집기 `from_me` — P0-1 이 맞음이면 `authorId == 내 userId`」 의 조건이 섰다
- 지금 `fetch_messages` 는 `authorId` 를 NTUser 이름 조인에만 쓰고 값은 내지 않는다(`db.rs:242-245`). `RawMessage`(`db.rs:52-60`)에도 그 칸이 없다
- `type=1999`·`authorId=0` 줄은 `authorId==나` 가 거짓이라 「내가 보냄=false」 로 갈린다(지금 수집기는 `type=0` 만 건너뛴다 — `db.rs:270-273`)

---

## §2. P0-2 알림 플러그인 클릭 콜백 (OQ-1108)

### 2-1. 대상 판

crates.io API(2026-10-08 조회) 기준이다:

- `tauri-plugin-notification`: max stable **2.5.1**(2026-10-01) · 알파 **3.0.0-alpha.2**(2026-09-30)
- 2.5.1 은 `tauri = "2.12"` 이상을 요구한다(그 크레이트 `Cargo.toml` `[dependencies.tauri] version = "2.12"`) · `rust-version = "1.90"`
- 우리 lock 은 `tauri 2.11.6`(`frontend/src-tauri/Cargo.lock:3725-3726`)이라 **넣으려면 tauri 판 올림이 함께 온다**

### 2-2. 근거 — 클릭 콜백 없음

| 근거 | 내용 |
|---|---|
| 공식 문서 https://v2.tauri.app/plugin/notification/ | 「**Mobile Only: The Actions API is only available on mobile platforms.**」 — `registerActionTypes()` · `onAction()` 이 해당 |
| 플러그인 소스 2.5.1 `src/desktop.rs:29-31` | 「Only the title, body, icon and sound of the notification are used on desktop; the scheduling, grouping and **action related options are ignored**.」 |
| 같은 파일 `:203-245` | 데스크톱 `show()` 가 `notify_rust::Notification` 을 만들고 `tauri::async_runtime::spawn(async move { let _ = notification.show(); })`(`:240-242`) — **반환 핸들을 바로 버린다.** 클릭을 기다리거나 앱에 전하는 코드가 없다 |
| 3.0.0-alpha.2 `src/desktop.rs` | 같은 줄(`:31` · `:234` · `:241`) — 알파도 같다 |
| notify-rust 4.18.2(플러그인 의존 `"4.11"` → 최신 4.18.2) `src/notification.rs:538-539` → `src/macos/nsusernotifications.rs:252-257` · `:142-161` | macOS 기본 백엔드는 NSUserNotification 이다. 핸들을 버리면 `Drop` 에서 `asynchronous: true` 로 보내고 응답을 받지 않는다 |

→ **공식 플러그인으로는 클릭을 셸이 받을 수 없다.** 사용자가 알림을 누르면 OS 기본 동작대로 「그 번들 앱을 앞으로」만 일어난다. 그 번들은 dev 에서 터미널이다(§3).

### 2-3. 대안과 비용

| 안 | 무엇 | 클릭 | 비용 · 위험(사실) |
|---|---|---|---|
| **① OS 기본 + 웹이 감**(SPEC-011 OQ-1108 제안) | 공식 플러그인 그대로. 누르면 앱이 앞으로 온다. 이동은 하지 않고 웹이 알림 목록(또는 마지막 알림)을 연다 | 셸이 클릭을 **모른다** → 「누른 뒤 앞으로 왔다」 를 웹이 직접 알 길이 없다(포커스/visibility 사건뿐 — 일반 창 전환과 가를 수 없음) | 의존 1(+ tauri 2.12 올림). `notify_permission` 은 늘 `Granted`(§3). AC-T51 「클릭 사건 한 번」 은 못 짓는다 → SPEC 처분 필요 |
| **② notify-rust 직접**(플러그인 없이) | 셸이 알림마다 스레드에서 `NotificationHandle::wait_for_action`(`nsusernotifications.rs:32-62`)을 부르고, `"default"` 면 창 보이기 + `strong-hajin:notification-click` | **받는다** — mac-notification-sys 0.6.15 `NotificationResponse::Click`(`src/notification.rs:324-335`) · ObjC `didActivateNotification`(`objc/notify.m:252`) | 같은 의존을 **직접** 쓰므로 tauri 판 올림은 필요 없을 수 있다(확인 안 함). 다만: **알림 하나에 블로킹 대기 하나**다 — 소스 주석 「Requires the main run loop to be running … if nothing is pumping the main run loop this call will block indefinitely」(`:28-31`). 클릭이 없으면 사라질 때까지 폴링하며(`objc/notify.m:58-66,183-206`) 기다린다. **NSUserNotification 은 Apple 폐기 API**(macOS 11) — 언제 끊길지 모른다. `set_application` 으로 번들 id 를 직접 정해야 한다(dev 에서는 Terminal 이 기본 — `objc/notify.h:27-31`) |
| **②′ notify-rust `preview-macos-un`** | 같은 크레이트의 UNUserNotificationCenter 백엔드(옵트인 · 이름에 preview — `Cargo.toml [features] preview-macos-un`) · `wait_for_action`/`response().await`(`src/macos/unusernotifications.rs:112-136`) | 받는다(`is_default_action()` → `"default"`) | 「preview」 기능이다. **번들 id·권한이 없으면 보내기가 panic** 할 수 있다는 소스 주석(`unusernotifications.rs:31-34` 「Panics if UNUserNotificationCenter refuses … no bundle identifier, authorisation not granted」). `request_auth` 로 권한 프롬프트를 띄운다 |
| **③ 서드파티 `tauri-plugin-notifications`** 0.4.6(2026-09-16 · 내려받기 27k · MIT) | macOS 는 Swift(swift-bridge) + UNUserNotificationCenter. `didReceive(response:)` 에서 기본 동작이면 `trigger("notificationClicked")`(`macos/Sources/NotificationHandler.swift:91-142`). 리스너가 없을 때 누른 것은 보관했다가 붙으면 보낸다(`:14-21`) · `requestAuthorization`(`:26`) | 받는다 — 단 **플러그인 사건(JS 리스너)** 으로 온다 | 우리 계약은 원격 웹에 플러그인 권한을 열지 않는다(SPEC-006 I-2 · 커맨드 넷). 이 사건을 **셸 Rust 쪽에서 받아 우리 `eval` 사건으로 바꿀 수 있는지는 확인하지 못했다.** 기본 feature 가 `notify-rust` 로 켜져 있어 macOS 네이티브를 쓰려면 `default-features = false`(README `:70-88`). 의존 `tauri = "2.8.2"`. 공식이 아닌 1인 유지 크레이트 |
| ④ 직접 구현 | 셸에서 objc2 로 `UNUserNotificationCenterDelegate` 를 구현(lock 에 objc2 계열이 이미 전이로 있음) | 받는다 | 코드량이 가장 크다 · 서명 번들 필요(UN) |

---

## §3. P0-3 권한 · 서명 영향 (문서·소스 근거 · 실기는 WP4)

| 물음 | 공식 플러그인(2.5.1) | UN 계열(②′·③·④) |
|---|---|---|
| 권한 묻기 · 읽기 | `request_permission`·`permission_state` 가 데스크톱에서 **항상 `Granted`**, 프롬프트 없음(`src/desktop.rs:85-99`). OS 설정에서 꺼도 셸은 모른다 → SPEC-006 「거부면 `{shown:false}`」 를 이 플러그인으로는 판정 못 함 | `requestAuthorization`/`request_auth` 가 **OS 프롬프트**를 띄우고 설정을 읽을 수 있다 |
| 미서명 `tauri dev` | **알림이 「터미널(com.apple.Terminal)」 이름·아이콘으로 뜬다** — `if tauri::is_dev() { "com.apple.Terminal" } else { identifier }`(`desktop.rs:232-237`). 터미널 쪽 알림 허용 상태를 따른다. 누르면 터미널이 앞으로 온다 | 번들이 없는 dev 바이너리는 번들 id 가 없어 거부·panic 위험(②′ 소스 주석). dev 실측 대상 |
| 번들 실행(서명 dmg) | 번들 id `app.stronghajin.desktop` / `app.ax.desktop` 로 알림 센터에 선다(`desktop.rs:236` · `tauri.conf.json` identifier). 처음 보낼 때 묻는 프롬프트는 이 API 에 없다(NSUserNotification) — 사용자는 시스템 설정 > 알림에서 끈다 | 첫 요청 때 프롬프트가 뜬다. 서명 dmg 1회 실측(WP4 · AC-T50) |
| 미서명 **번들**(로컬 `tauri build`) | 번들 id 로 뜨는 것으로 읽힌다(코드상 dev 만 Terminal). 실측 필요 | 실측 필요 |
| Info.plist 키 | **필수 키 없음**(문서·소스에 요구 없음 — 마이크처럼 usage description 이 있는 권한이 아니다). 선택으로 알림 모양(배너/알림) 키를 둘 수 있으나 이번에 확인하지 않았다 | 로컬 알림에 Info.plist 필수 키는 문서상 없음. 서명·번들 id 가 사실상 전제 |
| Entitlements | 알림 전용 entitlement 요구는 확인되지 않음(원격 푸시 `aps-environment` 는 해당 없음 — 서버 푸시 없음 D-07) | 같음 |
| Windows | **pending**(OQ-T01). 참고: 공식 문서 「Windows: Only works for installed apps. Shows powershell name & icon in development.」 · 소스는 `target/debug|release` 가 아니면 AUMID=identifier(`desktop.rs:219-229`) | — |

---

## §4. 사용자(코디)에게 물을 것

1. **OQ-1108 처분** — 공식 플러그인은 클릭을 못 준다. 다음 중 무엇으로 가나:
   - ① OS 기본(앱만 앞으로) + 웹이 알림 목록 열기 — AC-T51 을 바꿔야 함
   - ② `notify-rust` 직접 + 알림마다 대기 스레드 — 폐기 API(NSUserNotification) 위험
   - ③ 서드파티 플러그인 — 원격 웹에 플러그인 권한을 여는지 / Rust 에서 받을 수 있는지 추가 확인 필요
   - ④ objc2 직접 구현 — 가장 큼
2. **권한 표시** — 공식 플러그인(①·②)이면 `notify_permission` 이 늘 허용으로 답한다. 「거부면 `{shown:false}`」(SPEC-006 · SPEC-011 OQ-1102)를 지킬 수 없다 — 받아들이나, UN 계열로 가나
3. **tauri 판 올림** — 공식 플러그인 2.5.1 은 tauri ≥ 2.12 를 요구한다(우리 lock 2.11.6). WP4 범위에 판 올림을 넣나
4. **dev 실측** — 공식 플러그인은 dev 에서 「터미널」 로 뜬다. AC-T50 「미서명 dev 실행 결과도 기록」 은 이 사실로 갈음하나, 미서명 번들로 따로 재나
5. **P0-1 1:1** — 고른 방에 1:1 이 없어 운영 대조는 단체방만 했다. 로컬 1:1 전수 보조 확인(§1-4)으로 OQ-K01 을 닫아도 되나

## §5. 조사 한계

- P0-1 은 로컬 사본을 연 한 시점의 값이다. 운영 값은 코디가 2026-10-08 에 준 것이다. 비교 범위는 운영 최소~최대 logId 로 잡았다
- P0-2·P0-3 은 **문서와 크레이트 소스 읽기**다. 알림을 실제로 띄우거나 클릭해 보지 않았다(WP4 실기)
- ②의 「tauri 판 올림이 필요 없다」, ③의 「셸 Rust 에서 클릭 사건을 받을 수 있다」 는 확인하지 못했다
- Info.plist 의 알림 모양(배너/알림) 키 이름과 동작은 확인하지 않았다
- GitHub 이슈 트래커는 검색 결과가 빈약해 근거로 쓰지 않았다(문서 + 소스로 판정)
