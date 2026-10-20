# WP4-SHELL 결과 보고 — 셸 OS 알림 + 카톡 수집기 표지

## 상태: done — dmg · 서명 · 공증은 하지 않음(코디 몫) · 커밋 없음

- SSOT: WORK-013 「Phase WP4-SHELL」 · SPEC-006 v0.7.0 「시스템 알림 수용」 · SPEC-011 §2.5 · §4.6 · SPEC-009 v0.6.x · **사용자 처분(2026-10-08) ①~⑤가 SPEC 보다 앞선다**
- 경로: `T/` = `frontend/src-tauri/` · `F/` = `frontend/src/`. `backend/` 는 손대지 않았다

## 1. 계약 체크박스 — 6/7 (⑦ dmg 1회는 코디)

| # | 계약 | 구현 위치 |
|---|---|---|
| 1 | 알림 수단 · 커맨드 `notify_permission` · `notify_show` · **`build.rs` ACL 매니페스트** · capability 두 판 · `shell_info.features += "notification"` · 셸 시험(6 · 9) | **수단**(처분 ① · ②): macOS = objc2 로 UN 직접 · Windows = 공식 `tauri-plugin-notification` 2.5.1 — `T/Cargo.toml`<br>• `[target.'cfg(target_os = "macos")'.dependencies]`: objc2 0.6.4(+`exception`) · objc2-foundation 0.3.2 · objc2-user-notifications 0.3.2 · block2 0.6.2<br>• `[target.'cfg(windows)'.dependencies.tauri-plugin-notification]` 2.5.1<br>**모듈** 새 `T/src/notify.rs`<br>**커맨드** `T/src/lib.rs:253`(`notify_permission`) · `:263`(`notify_show` — `notify::validate` 뒤 별도 스레드). 둘 다 `rename_all = "snake_case"` 라 웹 인자 이름이 SPEC(`notification_id`) 그대로다<br>**등록**: `lib.rs:757`(medi-ax 9) · `:769`(strong-hajin 6) · Windows 플러그인 `:748`(`cfg(windows)`)<br>**ACL** `T/build.rs:144-145` · **capability** 두 판 `allow-notify-permission` · `allow-notify-show`(설명문 개수도 고침)<br>**features** `lib.rs:212`<br>**시험**: `lib.rs` 「웹에_여는_커맨드가_판에_맞다」 기대 6/9 · `scripts/verify-shell-build.mjs` 6/9 + 알림 둘 필수 + **§6 사건 이름 대조**(download · notification-click) |
| 2 | **클릭** — 창 보이기 · 포커스 → `strong-hajin:notification-click`(`{notification_id, target}`) · 이름 일치 시험 | macOS delegate `did_receive`(`notify.rs:212-236`): 기본 동작이면 userInfo 의 `notification_id` · `target`(JSON 문자열)을 꺼내 처리기에 넘긴다<br>처리기 = `lib.rs:281` `notify_click` — `main` 창 `show` · `unminimize` · `set_focus` 다음, **앱 origin 문서일 때만** `eval(notify::click_script(..))`(다운로드 사건과 같은 규칙). 새 창은 만들지 않는다(AC-T33) · 창이 없으면 아무것도 하지 않는다<br>설치 `lib.rs:700`(setup)<br>**이름 일치**: Rust `notify.rs` 시험 「사건_이름이_웹_수신부와_같다」 + `shell-verify` §6<br>Windows: 플러그인에 클릭 콜백이 없다 — OS 기본(앱만 앞으로 · 실기 pending) |
| 3 | **웹 다리**(`F/lib/shell.ts`) — `notifyPermission` · `notifyShow` · `onShellNotificationClick` · `features` 에 `notification` 있을 때만 | `shell.ts:337` `hasShellNotifications`(`shell_info.features` 판정 · 성공한 답만 기억) · `:359` `notifyPermission(request)` → `granted\|denied\|default\|absent` · `:378` `notifyShow(input)` → `boolean`(거부·실패·없음 = false, 던지지 않음) · `:392` `SHELL_NOTIFICATION_CLICK_EVENT` · `:405` `onShellNotificationClick`(셸 없으면 듣지 않음 · 모양이 다르면 버림) |
| 4 | **새 알림 → OS 알림**(D-39 · S11 §2.5) — `created: true` · `replayed: false` 만 · ① 앞에 있고 그 대상을 보면 생략 ② 합친 줄 갱신 없음 ③ 10초 창에 넷 이상이면 셋까지 + 「새 알림 N건」 · 글자 = WP3 문장 함수 · 클릭 → WP3 이동 함수 | 새 `F/lib/osNotifier.ts` — 상수 `OS_BURST_WINDOW_MS = 10_000` · `OS_BURST_LIMIT = 3`(실측 뒤 조정) · `createOsNotifier({show, isViewing, isForeground})`<br>• `offer`: `created`/`replayed` 거름 → 앞에 있음(`visibilityState === "visible" && document.hasFocus()`) + `isViewing` 이면 생략 → 창 셋까지 → 넷째부터 세어 창 끝에 `{notification_id: null, title: "알림", body: "새 알림 N건", target: {surface: "notifications"}}`<br>• 글자 = `describeNotification(n).title / text`(WP3)<br>**「지금 보는 화면」** 새 `F/lib/currentView.ts` — `useViewDetail(key, id)` 를 화면이 부른다: `MyWorkPage.tsx:246-247`(업무 · 요청 상세) · `InboxPage.tsx:105-106`(메일 · 방) · `MeetingWorkspace.tsx:55`(회의) · `SettingsPage.tsx:111`(설정 탭). `isViewingTarget(target, surface)` — 알림 목록은 대상이 아니다(OQ-1111)<br>**App** `App.tsx:107-131` `OsNotificationBridge`(사건 채널 Provider 안 · 셸 `notification` 기능이 있을 때만 · `:614`) · **클릭** `:493` `onShellNotificationClick` → `openNotification(id, target)`(WP3 — 묶음은 읽음 없이 목록) |
| 5 | **권한 묻기**(OQ-1102) — 로그인 뒤 첫 화면 한 번 · 거부면 다시 묻지 않는다 | `App.tsx:467-469` — 로그인(회원이 정해짐)마다 `notifyPermission(true)` 한 번. 셸은 **아직 묻지 않았을 때(`NotDetermined`)만** 프롬프트를 띄운다(`notify.rs:286-309`). 거부했으면 OS 가 다시 묻지 않고 「denied」 만 돌려준다 → OS 알림은 조용히 안 뜨고 목록·점은 그대로 |
| 6 | **카톡 수집기 `from_me`**(처분 ⑤ · OQ-K01 닫힘) | `T/src/kakao/db.rs` — `RawMessage.from_me: Option<bool>` · `fetch_messages` 가 `m.authorId` 를 함께 읽어 **`authorId == NTChatContext.userId`**(P0-1 의 그 이름 · 읽기 경로 그대로). 작성자 없는 줄(`authorId 0` · type 1999)은 `false` · type 0 은 지금처럼 건너뜀. 내 userId 를 못 읽으면(`0`) `None`<br>`T/src/kakao/client.rs:297-299` — `from_me` 가 있으면 업로드 줄에 `"from_me": bool`, `None` 이면 **키를 싣지 않는다**(서버 `null` · AC-12) · `:311` 변환 |
| 7 | dmg 빌드 · 서명 · 공증 1회 | **하지 않았다**(브리프 — 코디가 E2E 직전 · 사용자 키체인). `make shell-build`(서명 없는 `.app`)만 판마다 돌렸다 — §4 |

### 처분 ③ — tauri 2.12
- `T/Cargo.toml` `tauri = "2.12"` → lock `tauri 2.12.1` · wry 0.57 · **webview2-com 0.38 → 0.39**(wry 가 0.39 를 써서 우리 Windows 마이크 코드의 `with_webview` 타입이 같은 판이어야 한다 — 함께 올림)
- npm `@tauri-apps/api` · `@tauri-apps/cli` 2.11.1 → **2.12.1**(`package.json` · `package-lock.json`). `tauri build` 가 크레이트/npm 판 차이로 빌드를 막아서다
- 셸 시험 `셸_프레임워크_하한이_2_12_이상이다`(옛 2.11.1 단언을 고침 — GHSA 하한은 그대로 덮인다)

## 2. objc2 구현 요지 (`T/src/notify.rs` `mac` 모듈)

- **번들 판정**: `NSBundle.mainBundle` 의 식별자가 있고 경로가 `.app` 으로 끝날 때만 UN 을 연다(`bundled` `:175`). 그다음 `currentNotificationCenter` 도 `objc2::exception::catch` 로 감싼다(`center` `:180`). 번들이 아니면(`tauri dev` · `cargo test`) ObjC 예외가 나는 자리라 panic 없이 `default` / `{shown:false}` 로 떨어진다(처분 ④)
- **스레드**: UN 메서드는 어느 스레드에서 불러도 된다. 커맨드는 `spawn_blocking` 스레드에서 부르고, 완료 블록(`RcBlock`)이 `mpsc` 로 답을 넘긴다. 메인 run loop 는 막지 않는다. 상한은 프롬프트 120초(사람을 기다림) · 설정 읽기와 보내기 10초다. 넘으면 `default` / `false`
- **delegate 수명**: `define_class!` 로 `StrongHajinNotificationDelegate`(NSObject · ivar 없음)를 만들어 setup(메인 스레드)에서 한 번 건다. UN 의 `delegate` 는 약한 참조라 `std::mem::forget` 으로 앱 수명 동안 붙잡는다. 클릭 처리기는 전역 `OnceLock` 한 칸이다
- **willPresent**: `Banner | List | Sound` — 앱이 앞에 있어도 배너가 뜬다. 「보고 있으면 생략」은 웹이 이미 판단했다
- **didReceive**: `actionIdentifier == UNNotificationDefaultActionIdentifier` 일 때만 처리기를 부르고, 완료 블록은 늘 부른다
- **보내기**: `UNMutableNotificationContent` 에 제목 · 본문 · 기본 소리, `userInfo` 에 `notification_id`(있을 때) · `target`(JSON 문자열)을 싣는다. 요청 식별자는 알림 id 다(같은 알림을 다시 보내면 OS 가 갈아 끼운다). 묶음은 `bundle-<ms>`. 트리거는 없다(즉시)
- **권한**: `getNotificationSettings.authorizationStatus` → `NotDetermined = default` · `Denied = denied` · 그 밖(Authorized · Provisional · Ephemeral) = `granted`. 요청은 `Alert | Sound` 다
- **보내기 전 검증**(`validate` `:56`): id 128자 · 제어문자 없음 · 제목 200자 · 본문 1000자 · `target` 객체 4KB. 어긋나면 오류로 돌려 OS 에 흘리지 않는다
- Info.plist · Entitlements: **바꾸지 않았다**(P0-3 — 로컬 알림에 필수 키 없음). 서명 dmg 실측에서 필요하면 더한다

## 3. Code Surface WP4 표 대비

| 무엇 | 표 | 지금 | 처분 |
|---|---|---|---|
| `generate_handler` | 2 | 2 | 7→9 · 4→6 |
| ACL `AppManifest::new().commands` | `build.rs:138-160` | 같은 자리 | 알림 둘 더함 |
| 의존 | `Cargo.toml:35` opener | + mac objc2 넷 · win 플러그인 · tauri 2.12 · webview2-com 0.39 | `package.json` `@tauri-apps/*` 는 판만 올렸다 — 웹이 플러그인 JS 를 부르지 않는다는 원칙은 그대로다 |
| `.plugin(` | 1 | 1 + `cfg(windows)` 1 | macOS 는 플러그인이 아니라 objc2 |
| capability `permissions` | 7 · 4 | 9 · 6 | 두 판 |
| `features: [` | 1 | `"notification"` 더함 | — |
| 셸 → 웹 사건 `window.eval` | 1 | 2(`notify_click`) | 이름 일치: Rust 시험 + shell-verify §6 |
| 창 앞으로 `show()\|set_focus` | 트레이 | + `notify_click` | `unminimize` 도 |
| 웹 셸 다리 `invoke(` | 2/2 | 2/2 | `call()` 한 자리 그대로(새 커맨드도 그 길) |
| 셸 판별 `hasShell(` | 12/5 | + `hasShellNotifications` | — |
| 사건 수신 본보기 | `onShellDownload` | + `onShellNotificationClick` | 같은 결 |
| Info.plist · Entitlements | 키 1 · 1 | 그대로 | §2 끝 |
| 카톡 수집기 | `db.rs` · `client.rs` | `from_me` | §1-6 |
| 셸 Makefile | — | 그대로 | `shell-build` 는 서명 없이만 돌렸다 |

**표 밖에서 고친 것**: `webview2-com` 0.39 · npm `@tauri-apps/*` 2.12.1 · `verify-shell-build.mjs`(§5 개수 · §6 사건 이름) · `currentView.ts` 와 화면 넷의 `useViewDetail`(「보고 있으면 생략」의 재료 — WP3 화면은 상세가 열린 것을 App 에 알리지 않았다)

## 4. 시험 · 검증 (관련만)

| 명령 | 결과 |
|---|---|
| `make shell-verify SHELL_FLAVOR=strong-hajin` · `…=medi-ax` | 둘 다 **문제 0 · 구성 미비 0** · 호스트 한계 1(Windows 를 이 Mac 에서 못 구움) |
| `cd frontend/src-tauri && cargo test` (strong-hajin) | **77 passed** · 0 failed |
| `SHELL_FLAVOR=medi-ax cargo test --features kakao-collector` | **98 passed** · 0 failed · 6 ignored(실기기 live 시험 — 기존) |
| `cargo clippy --all-targets -- -D warnings` (두 판) | **경고 0** |
| `cd frontend && npx vitest run src/lib/shell.test.ts src/lib/osNotifier.test.ts src/App.test.tsx src/features/inbox/InboxPage.test.tsx src/features/settings/SettingsPage.test.tsx src/features/settings/NotifySection.test.tsx src/features/notifications/NotificationsPage.test.tsx src/features/meetings/MeetingWorkspace.test.tsx src/features/work/MyWorkPage.test.tsx src/lib/eventStream.test.ts src/lib/notificationLabels.test.ts src/shell/AppShell.test.tsx src/SettingsLanding.test.tsx --no-file-parallelism` | **13 files · 231 passed** · 0 failed |
| `npx tsc --noEmit` | **0 오류** |
| `make shell-build SHELL_FLAVOR=<판> SHELL_BUILD_ARGS="--bundles app"`(서명 없음) | 두 판 **성공**(exit 0) — `Strong Hajin.app`(13.16 MiB) · `medi-ax.app`(19.34 MiB). strict 검증 통과 뒤 구움 · 서명 없음 · dmg 는 굽지 않음(`/Volumes/medi-ax` 가 마운트돼 있어 dmg 스크립트와 겹치지 않게 `--bundles app`). 산출물은 `target/`(git 무시) |
| `cargo check --target x86_64-pc-windows-msvc` | **이 Mac 에서 못 잼** — `tauri-build` 가 Windows 리소스 컴파일러(`llvm-rc`)를 요구한다. `cfg(windows)` 코드(플러그인 호출 · webview2-com 0.39 마이크 코드)는 **컴파일 확인 없음** — Windows 실기에서 처음 서는 자리다 |

**새 시험**
- Rust `notify.rs` 5: 사건 이름 대조 · 클릭 스크립트 JSON 이스케이프 · 인자 검증 9경우 · 권한 직렬화 · **번들이 아니면 panic 없이 default/false**(macOS)
- Rust `kakao/db.rs` 2(평문 인메모리 DB 로 `fetch_messages`): 내가 보낸 줄 true / 받은 줄 · 작성자 없는 줄 false / type 0 건너뜀 · userId 없으면 None
- Rust `kakao/client.rs` +3단언: `from_me` true/false 싣기 · None 이면 키 없음
- 바뀐 Rust 시험 2: 커맨드 6/9 · tauri 하한 2.12
- vitest `shell.test.ts` +6(셸 없음 · 옛 dmg · 커맨드 둘 · 클릭 사건 · 이름) · 새 `osNotifier.test.ts` 9(새 줄 · 합친/이어 받은 줄 · 보고 있으면 생략/뒤에 있으면 띄움 · 셋+묶음 · 셋 이하 · 새 창 · 생략은 수에 안 듦 · currentView 대조) · `App.test.tsx` +1(셸 클릭 사건 → 읽음 + 업무 화면 / 묶음 → 읽음 없이 목록)

## 5. 실측 항목 — 코디 dmg 용 체크리스트 (macOS 서명 dmg · 두 판)

1. **권한 프롬프트** — 처음 로그인하면 「"Strong Hajin"(또는 "medi-ax")에서 알림을 보내려고 합니다」 가 한 번 뜬다. 허용/거부 각각, 다시 로그인해도 다시 안 뜬다
2. **알림 센터의 이름 · 아이콘** — 번들 이름 · 아이콘(`app.stronghajin.desktop` / `app.ax.desktop`). 시스템 설정 > 알림에 앱이 선다
3. **새 알림 표시** — 다른 계정으로 업무 요청 → 배너. 제목 「업무 · 담당」 · 본문은 목록 문장과 같다
4. **앱이 앞에 있어도 배너**(willPresent) — 단 **그 대상 화면을 보고 있으면 안 뜬다**(그 업무 상세 · 그 방 · 그 메일 · 그 회의 · 그 연동 탭). 알림 목록을 보고 있으면 뜬다(OQ-1111)
5. **합친 슬랙 채널 줄은 처음만** — 같은 채널에 두 번째 메시지 → OS 알림 없음 · 목록 줄 숫자만 는다
6. **몰림** — 10초 안에 5건 → 낱낱이 3 + 10초 뒤 「새 알림 2건」. 그 묶음을 누르면 알림 목록(읽음 없음). **재연결 직후 · 최소화 풀림** 때도(이어 받은 줄은 OS 알림 없음 — 목록·점만). 창·문턱 체감을 기록
7. **클릭** — 앱이 앞으로(최소화였으면 풀림) + 그 대상을 고른 상태 + 그 줄 읽음 + 점 갱신. 가려짐 · 다른 Space 에서도
8. **권한 거부** — OS 알림 안 뜸 · 목록 · 점은 그대로 · 오류 토스트 없음
9. **창 닫으면 OS 알림 없음** — strong-hajin: 마지막 창을 닫으면 프로세스가 끝나는가(기록) / medi-ax: 트레이만 남고 OS 알림 없음 · 「열기」 뒤 목록 · 점 맞음. 닫기 전에 온 알림을 알림 센터에서 누르면? — 창이 없으면 셸은 아무것도 하지 않는다(새 창을 만들지 않음 · 기록)
10. **최소화 · 가려짐 30분** — 그동안 온 알림이 제때 뜨는가(웹뷰 스로틀 — 기록)
11. **tauri dev**(번들 아님) — 권한 `default` · OS 알림 안 뜸 · 오류 없음(셸 로그 「번들이 아니라 UN delegate 를 걸지 않는다」)
12. **카톡 `from_me`** — medi-ax: 내가 보낸 1:1 · 단체방 줄은 서버에 `true`, 받은 줄은 `false`, 그 줄로는 나에게 알림 없음(SPEC-011 AC-08)
13. **Windows**(pending) — 토스트가 뜨는가 · 클릭은 앱만 앞으로(이동 없음) · AUMID(설치본만 — 플러그인 소스 `desktop.rs:219-229`) · 마이크(webview2-com 0.39 로 올림 — 녹음 회귀 확인)

## 6. 미결

1. **dmg · 서명 · 공증** — 코디(브리프). 서명 없이는 UN 이 서는지 이 기기에서 확인하지 못했다(§5-1·2)
2. **Windows 컴파일 미확인** — `cfg(windows)` 코드 · webview2-com 0.39 마이크 코드(§4 끝). Windows 빌드 기계에서 첫 확인 필요
3. **목록 화면 「열 수 없음」과 OS 클릭의 차이** — 대상이 `null` 인 알림을 OS 로 띄울 때는 셸이 `target` 객체를 요구해 `{surface: "notifications"}` 로 보낸다 → 누르면 읽음 + 알림 목록으로 간다(목록에서 누르면 「열 수 없는 항목입니다」 토스트). 사용자 E2E 에서 보고 2루프
4. 권한 묻기는 로그인마다 한 번 셸에 묻는다 — OS 가 이미 답을 가졌으면 프롬프트는 없다(같은 결과). 「로그인 뒤 첫 화면 한 번」 을 더 좁힐지는 2루프
5. SPEC 문서(OQ-1108 ④ · tauri 2.12 · OQ-K01 닫힘)는 writer 가 병렬로 고친다 — 이 리포트는 사용자 처분을 따랐다
