# 코드 검수 — WP4-SHELL (셸 OS 알림 · 카톡 수집기 표지)

> reviewer(read-only) · 2026-10-08 · 대상 `frontend/src-tauri/` 전부 · `frontend/src/lib/{shell.ts, osNotifier.ts, currentView.ts}` · WP4 가 손댄 화면 자리(`App.tsx` · `MyWorkPage` · `InboxPage` · `MeetingWorkspace` · `SettingsPage`) · `package.json`/lock · `Cargo.toml`/lock
> 계약: WORK-013 WP4-SHELL · SPEC-006 v0.7.1 · SPEC-011 v0.2.4 §2.5 · §4.6 · SPEC-009 v0.6.1 · `_RESUME.md` §2 「P0 처분」(④ macOS UN objc2 직접 · Windows 공식 플러그인 · tauri 2.12 · dev 는 `{shown:false}` · OQ-K01)
> 약어: `T/` = `frontend/src-tauri/` · `F/` = `frontend/src/`

## 0. 판정 — **WARN** (FAIL 0 · WARN 6)

계약 일곱 가운데 dmg 를 뺀 여섯이 코드로 서 있다. objc2 UN 구현은 안전 근거가 분명하다.
- delegate 를 영구 보유한다
- 번들이 아니면 panic 없이 떨어진다(시험으로 고정)
- 메인 run loop 를 막지 않는다
- 클릭 스크립트는 `serde_json` 으로만 만든다

경계(원격 웹에 여는 것 = 우리 커맨드 6 · 9 · 플러그인 권한 0)도 맞다. 웹 쪽 OS 발송기 규칙(새 줄만 · 보고 있으면 생략 · 10초에 셋 + 묶음 · 문장 공유 · 클릭 = 같은 이동)과 카톡 `from_me`(키 이름 · 모르면 싣지 않음)도 계약대로다.

WARN 은 셋이 크다.
- **창이 없을 때 알림 센터에 남은 배너를 누르면 아무 일도 없다**(medi-ax 트레이 상주 중)
- **tauri 2.12 올림이 tao · wry · tray-icon · muda · opener · Windows 크레이트까지 65 크레이트를 움직였다** — 트레이 · 내려받기 · 하위 프레임 · 마이크 회귀를 dmg 에서 봐야 한다
- `cfg(windows)` 코드는 컴파일조차 확인되지 않았다

나머지 셋은 작다.

### 실행한 것
- 코드 전문: `T/src/notify.rs` · `lib.rs`(커맨드 · `notify_click` · setup · 등록) · `build.rs` · capability 두 판 · `kakao/{db,client}.rs` diff · `Cargo.toml` · lock 변화(크레이트별 판 대조) · `F/lib/{osNotifier,currentView,shell}.ts` · `App.tsx` 브리지 · 권한 묻기 · `useViewDetail` 네 화면 · `scripts/verify-shell-build.mjs`
- 시험(관련만 · 앱 실행 없음 · 사용자 포트 없음)
  - `cd frontend/src-tauri && cargo test` → **77 passed**(strong-hajin)
  - medi-ax `--features kakao-collector` 98 · clippy 0 은 코디 관문 수치를 받아들였다(이번에 다시 굽지 않음)
  - `npx vitest run src/lib/shell.test.ts src/lib/osNotifier.test.ts src/App.test.tsx src/features/meetings/MeetingWorkspace.test.tsx src/features/work/MyWorkPage.test.tsx src/features/inbox/InboxPage.test.tsx src/features/settings/SettingsPage.test.tsx --no-file-parallelism` → **7 files · 160 passed · exit 0**(앞 검수 WP2·WP3 F-3 의 처리 안 된 예외는 이 실행에서 사라졌다)
  - `npx tsc --noEmit` → 0

---

## 1. objc2 UN 구현의 안전

| 물음 | 코드 | 판정 |
|---|---|---|
| delegate 수명 | `Delegate::new()` 를 `setDelegate` 뒤 `std::mem::forget`(`notify.rs:257-260`) — UN 의 `delegate` 는 약한 참조라 보유가 맞다. ivar · Drop 없음(`:188-192`). 한 번만 건다(setup). 누수는 객체 하나(의도) | PASS |
| 메인 스레드 · run loop | 커맨드는 `spawn_blocking`(`lib.rs:253-276`)에서 부르고, UN 완료 블록이 `mpsc` 로 답한다(`notify.rs:264-273,296-308,347-352`). 메인을 막지 않는다. 상한은 프롬프트 120초 · 그 밖 10초 | PASS |
| `requestAuthorization` 콜백 스레드 | 블록은 `tx.send` 만 한다(어느 스레드든 안전). 타임아웃이면 `default` | PASS |
| 번들 id 없을 때 | `bundled()`(식별자 + `.app`) → `currentNotificationCenter` 를 `objc2::exception::catch` 로 감쌈(`:175-186`). 시험 `번들이_아니면_panic_없이_못_함으로_떨어진다`(cfg macOS — 이 Mac 에서 돎) | PASS |
| `unsafe` 근거 | `UNNotificationDefaultActionIdentifier`(프레임워크 상수) · `settings.as_ref()`(UN 이 넘긴 살아 있는 객체) · `msg_send![super, init]` · `Retained::cast_unchecked`(키 · 값 모두 NSString — 속성 목록 형식) · `setUserInfo` — 각각 SAFETY 주석이 있고 근거가 맞다 | PASS |
| `didReceive` 처리 | 기본 동작일 때만 처리기를 부르고 **완료 블록은 늘 부른다**(`:212-231`). `target` 이 없거나 JSON 이 깨지면 `Null` → 웹 `readClickDetail` 이 `target: null` 로 받는다 | PASS |
| 창 숨김 · 최소화에서 앞으로 | `notify_click`(`lib.rs:281-300`) — `show` → `unminimize` → `set_focus`. tao 의 `set_focus` 는 최소화면 건너뛰므로 순서가 맞다. **창이 없으면**(파괴됨) 아무것도 하지 않는다 → **W-1** | PASS(W-1) |
| `willPresent` | `Banner \| List \| Sound` — 앱이 앞에 있어도 뜬다(생략 판단은 웹) | PASS |
| 클릭 스크립트 | `click_script` 가 이름 · 값을 `serde_json` 으로만 싣는다(`:81-85`) · 시험이 따옴표 · `</script>` 이스케이프 단언 · 「앱 origin 일 때만」 `eval`(다운로드 사건과 같은 규칙) | PASS |
| 보내기 전 검증 | `validate`(`:56-78` — id 128 · 제어문자 · 제목 200 · 본문 1000 · target 객체 4KB) · 시험 9경우 | PASS |

## 2. 경계

| 항목 | 확인 | 판정 |
|---|---|---|
| 원격 웹 커맨드 수 | `generate_handler!` strong-hajin 6 · medi-ax 9(`lib.rs:757-780`) · capability 두 판에 `allow-notify-permission` · `allow-notify-show` 만 더함(설명문 개수도 고침) · `build.rs:144-145` ACL 매니페스트 | PASS |
| 공식 플러그인 권한 | `tauri-plugin-notification` 은 `cfg(windows)` 의존 · `.plugin(…)` 도 `cfg(windows)`(`lib.rs:746-748`) · **capability 에 `notification:*` 권한 없음** → 원격 문서가 플러그인 커맨드를 부를 수 없다. macOS 에는 플러그인이 컴파일되지 않는다(lock 의 `notify-rust` · `mac-notification-sys` 는 Windows 대상 의존 그래프에만) | PASS |
| origin | capability `remote.urls` 한 origin 그대로 · 클릭 사건은 「창의 지금 URL 이 앱 origin 일 때만」 | PASS |
| 굽기 전 대조 | `verify-shell-build.mjs` — 개수 6/9 · 알림 둘 필수 · **§6 사건 이름 대조**(download · notification-click) · Rust 시험 `사건_이름이_웹_수신부와_같다` | PASS |

## 3. 웹 쪽

| 계약 | 코드 | 판정 |
|---|---|---|
| `created:true` · `replayed:false` 만 | `osNotifier.ts:54` | PASS |
| 보고 있으면 생략 | `foreground()` = `visibilityState === "visible" && document.hasFocus()` · `isViewing(target)` = App `surface` + `currentView` 의 상세(업무 · 요청 · 메일 · 방 · 회의 · 설정 탭) · 알림 목록은 대상 아님(OQ-1111) · 생략은 묶음 셈에 들지 않는다(`:56`) | PASS |
| 10초 창 · 셋 · 묶음 | 첫 OS 알림에서 창을 열고(`:57-60`) 셋까지 낱낱이, 넷째부터 `held` → 창 끝에 `{notification_id:null, title:"알림", body:"새 알림 N건", target:{surface:"notifications"}}`(`:42-50`) | PASS |
| 문장 공유 · 클릭 = 같은 이동 | `describeNotification(item).title/text` · `onShellNotificationClick` → `openNotification(id, target)`(`App.tsx:493`) — 묶음(`id:null`)은 읽음 없이 목록 | PASS(W-4) |
| 권한은 로그인 뒤 한 번 · 거부면 다시 안 묻기 | `App.tsx:467-469` 회원이 정해질 때마다 `notifyPermission(true)` — 셸은 `NotDetermined` 일 때만 프롬프트(`notify.rs:293-295`) → OS 가 이미 답했으면 다시 묻지 않는다 | PASS |
| 셸 기능 판정 | `hasShellNotifications`(`shell.ts:337`) — 옛 dmg · 브라우저는 한 번도 부르지 않는다 · 실패한 판정은 기억하지 않는다 | PASS |
| 타이머 정리 | `dispose`(`osNotifier.ts:71-77`)를 브리지 언마운트 때 부른다(`App.tsx:121-124`) — 묶어 둔 수는 버린다(로그아웃 때라 맞다) | PASS |

## 4. 카톡 `from_me`

- `T/src/kakao/db.rs`: 조회에 `m.authorId` 를 더해 `from_me = (me != 0).then(|| author_id == Some(me))` 로 둔다
  - `me` = `self_user_id(conn)` = `NTChatContext.userId` — P0-1 의 그 출처다
  - 내 id 를 못 읽으면 `None`
  - 작성자 없는 줄(authorId 0 · type 1999)은 `false`
  - type 0 은 지금처럼 건너뛴다
- `client.rs`: `Some` 일 때만 업로드 줄에 `"from_me": bool` · `None` 이면 **키를 싣지 않는다**(AC-12)
- **서버 필드 이름과 같다**: `KakaoMessageInput.from_me: bool | None`(`backend/…/kakao_ingest.py`)
- 시험
  - 평문 인메모리 DB 로 `fetch_messages` 두 경우(나 · 상대 · 작성자 없음 · 시스템 줄 · 내 id 없음 — 이름 · id 는 가상)
  - `client.rs` true / false / 키 없음
- 판정 **PASS**

## 5. tauri 2.12 올림 — 회귀 위험

- lock 에서 **65 크레이트**의 판이 바뀌었다(직접 대조). 굵은 것만 적는다
  - `tauri` 2.11.6 → 2.12.1 · `tauri-runtime(-wry)` 2.12.1 · `tauri-build`/`codegen`/`macros`/`plugin` 2.7.1 · `tauri-utils` 2.10.1
  - **`tao` 0.35 → 0.37 · `wry` 0.55 → 0.57 · `tray-icon` 0.24 → 0.25 · `muda` 0.19 → 0.20 · `tauri-plugin-opener` 2.5.5 → 2.7.0**
  - `webview2-com` 0.38 → 0.39 · `windows` 0.61 → 0.62 · `window-vibrancy` 0.6 → 0.8
  - html/css 파서(`html5ever` · `cssparser` · `selectors`) · `urlpattern` 0.3 → 0.6
  - npm `@tauri-apps/api` · `cli` 2.12.1
- 기존 셸 시험(커맨드 · 사건 이름 · 판 오버레이 · GHSA 하한 → 2.12)은 77 / 98 로 통과한다
- 그러나 **시험이 덮지 못하는 실행 동작**이 많이 움직였다. 판 고정(`2.12` → lock 2.12.1)은 됐다
  - 트레이(medi-ax 메뉴 · 「열기」 · 「종료」)
  - 창 닫기 = 파괴 · 프로세스 상주
  - 내려받기(U-5 · 새 창 링크)
  - 하위 프레임 허용(WORK-012)
  - 외부 링크(opener 2.7)
  - 절전 방지
  - Windows 마이크(webview2-com 0.39)
- → **W-2**: dmg 실측 체크리스트(§8)에 회귀 줄을 보탰다

## 6. 조용히 통과하는 자리

- **cfg 로 갈린 코드**
  - `mac` 모듈은 이 Mac 의 `cargo test` 에서 컴파일되고, `번들이_아니면…` 시험이 실제로 돈다. 다만 **번들 경로**(UN 이 실제로 서는 갈래 — `status` · `requestAuthorization` · `addNotificationRequest` · `didReceive`)는 시험이 닿지 않는다. 서명 dmg 실측뿐이다(§8)
  - **`cfg(windows)`**(플러그인 등록 · `NotificationExt` 호출 · webview2-com 0.39 마이크 코드)는 **컴파일조차 확인되지 않았다**(워커 리포트 §4 끝 — `llvm-rc` 부재). Windows 빌드 기계에서 처음 서는 코드다 → **W-3**
- **셸 대역**(`__TAURI_INTERNALS__`): `shell.test.ts` 가 `invoke` 를 흉내 내 커맨드 이름 · 인자 · 응답을 단언한다. 실물과 다를 수 있는 곳은 인자 이름 변환인데, Rust 커맨드가 `rename_all = "snake_case"` 라 웹 인자(`notification_id`)와 같은 글자다 — 대역과 실물이 같은 모양이다
- `OsNotificationBridge` 의 `enabled` 는 `hasShellNotifications()` 가 답하기 전엔 거짓이다 — 앱이 막 섰을 때 도착한 첫 알림 몇은 OS 로 안 뜬다(목록 · 점에는 선다). 영향이 작아 참고만

## 7. WARN

| # | 무엇 | 파일:줄 | 고칠 것 |
|---|---|---|---|
| **W-1** | **창이 없을 때 알림 센터의 옛 배너를 누르면 아무 일도 없다.** medi-ax 는 창을 닫아도 프로세스가 트레이에 산다. 닫기 전에 뜬 배너는 알림 센터에 남는다. 그것을 누르면 delegate 는 받지만 `notify_click` 이 「창이 없어」 로 끝난다 — 앱도 앞으로 안 오고 창도 안 연다. strong-hajin 은 프로세스가 끝나 있으면 OS 가 앱을 새로 띄우는데, 웹이 다 뜨기 전이라 사건이 버려진다 | `T/src/lib.rs:281-286` | 택일(코디 · 사용자): ① 창이 없으면 **트레이 「열기」 와 같은 길로 창을 만든다**(AC-T33 「동시에 둘이 아님」 은 지켜진다) ② 창을 닫을 때 **알림 센터의 우리 배너를 지운다**(`removeAllDeliveredNotifications`) — D-08 「닫으면 끊긴다」 와 맞는 쪽. 어느 쪽이든 dmg 실측 항목으로 |
| **W-2** | tauri 2.12 올림이 65 크레이트(tao · wry · tray-icon · muda · opener · windows)를 움직였다 — 시험이 덮지 않는 실행 동작 회귀 위험 | `T/Cargo.toml` · `T/Cargo.lock` | §8 회귀 줄을 dmg 실측에 넣는다(트레이 · 닫기 · 내려받기 · 하위 프레임 · 외부 링크 · 절전 방지 · 마이크) |
| **W-3** | `cfg(windows)` 코드 컴파일 미확인 — 플러그인 등록 · `NotificationExt` · webview2-com 0.39 마이크 | `T/src/notify.rs:122-131` · `T/src/lib.rs:746-748` · 마이크 함수 | Windows 빌드 기계(또는 CI)에서 `cargo check --target x86_64-pc-windows-msvc` 한 번을 Windows dmg/설치본 전 관문으로. 그 전엔 Windows 배포를 막는다 |
| **W-4** | `target: null` 알림의 OS 클릭이 목록 클릭과 다르다 — 셸이 `target` 객체를 요구해 `{surface:"notifications"}` 로 바꿔 보낸다. 그래서 누르면 **읽음 + 알림 목록**이고, 목록에서 누르면 「열 수 없는 항목입니다」 다(SPEC-011 §2.5 「누르면 = §2.1 과 같은 일」 과 다름 · 워커 미결 3) | `F/lib/osNotifier.ts:65` | 클릭이 `notification_id` 가 있는데 `target.surface === "notifications"` 이면 `openNotification(id, null)` 로 보내 토스트를 띄우거나, 셸 검증에서 `target: null` 을 허용한다 |
| **W-5** | 권한을 **회원이 정해질 때마다** 셸에 묻는다(페르소나 전환 · 재로그인 포함) — OS 프롬프트는 한 번뿐이라 결과는 같지만, OQ-1102 「로그인 뒤 첫 화면 한 번」 보다 넓다 | `F/App.tsx:467-469` | 받아들일 수 있다(워커 미결 4) — 2루프에서 좁힐지 코디 판단 |
| **W-6** | 클릭 때 창이 앱 origin 이 아니면(OAuth · 셸 오류 화면 · 문서 로딩 중) 사건을 버린다 — 창은 앞으로 오지만 이동이 없다(SPEC-006 이 정한 규칙대로) | `T/src/lib.rs:290-297` | 계약대로다. 로딩 중이면 짧게 다시 시도할지는 2루프 후보 — 실측에서 체감 기록 |

## 8. dmg 실측 체크리스트 — 워커 §5 열셋에 **보탠다**(서명 dmg · 두 판)

워커 §5 의 1~13 은 그대로 쓴다. 아래를 더한다.

| # | 볼 것 | 왜 |
|---|---|---|
| 14 | **창 닫은 뒤 알림 센터의 옛 배너 클릭**: medi-ax(트레이 상주) — 무엇이 일어나나 · strong-hajin(프로세스 끝남) — 앱이 새로 뜨는데 그 대상으로 가나 | W-1 |
| 15 | **앱이 아예 꺼져 있을 때 알림 센터 클릭으로 앱이 뜰 때** delegate 가 그 클릭을 받는가(setup 에서 delegate 를 거는 시점이 launch 응답보다 앞인가) | delegate 시점 |
| 16 | **OAuth 동의 창 · 셸 오류 화면이 떠 있을 때 클릭** — 창만 앞으로 · 이동 없음 · 셸 로그 한 줄 | W-6 |
| 17 | **방해 금지(집중 모드)** 켠 상태 — 배너 없이 알림 센터에만 · 앱 오류 없음 | OS 동작 확인 |
| 18 | **시스템 설정에서 나중에 알림을 끄면** — 다음 `notify_show` 가 `{shown:false}` · 다시 켜면 뜬다(앱 재시작 없이) | `status` 를 매번 읽는다 |
| 19 | **같은 알림 id 재전송**(이어 받기와 겹친 실시간이 새면) — OS 가 갈아 끼워 배너가 둘 서지 않는가 | 식별자 = 알림 id |
| 20 | **tauri 2.12 회귀** — 트레이 메뉴 셋(medi-ax) · 창 닫기 = 파괴 · 트레이 「열기」 로 다시 · 첨부 내려받기(대화상자 없이 · 번호 붙임 · 토스트) · `_blank` 링크 · 하위 프레임 허용(WORK-012) · 외부 링크 → 기본 브라우저 · 녹음 중 절전 방지 · 회의 마이크 · 앱 업데이트 받기 진행 표시(WORK-012 E-2) | W-2 |
| 21 | **Windows**(pending — 빌드 기계가 생기면): `cargo check` 통과 → 토스트 · 마이크 녹음 | W-3 |
| 22 | **카톡 `from_me` 셈** — 새 수집기로 올린 뒤 서버에서 그 연동의 `from_me = true` 줄 수가 사용자 본인 줄과 맞는가(백필 `apply=0` 출력과 함께 봄) | SPEC-009 AC-11 · 백필 순서 |

## 9. 사람 눈에 이상해 보일 자리

| # | 자리 | 왜 |
|---|---|---|
| ① | medi-ax 창을 닫은 뒤 알림 센터의 배너를 눌러도 **아무 반응이 없다** | W-1 |
| ② | 「열 수 없는 항목」 알림이 OS 에서는 **알림 목록**으로 가고, 목록에서는 토스트가 뜬다 | W-4 |
| ③ | 다른 회원 화면을 열어 둔 채 앱을 앞에 두면 **앱 안에서도 배너가 뜬다**(그 대상 상세를 보고 있을 때만 생략) — 시안 · 결정대로지만 처음엔 시끄럽게 느낄 수 있다 | D-39 ① 범위 |
| ④ | 10초에 4건 이상이면 셋 뒤 **「새 알림 N건」 이 10초 늦게** 뜬다 | 창이 끝날 때 묶음을 띄우는 설계 |
| ⑤ | 앱을 막 켠 직후 1~2초 안에 온 알림은 OS 로 안 뜬다(목록 · 점에는 선다) | §6 `enabled` |

---

## 10. 목록

### FAIL
없음.

### WARN
W-1 창 없을 때 배너 클릭 무반응(셸 · 코디 판단) · W-2 tauri 2.12 회귀 실측 · W-3 Windows 컴파일 미확인 · W-4 `target:null` OS 클릭 경로 · W-5 권한 묻기 범위 · W-6 앱 origin 아닐 때 클릭 — §7

### 사용자에게 물을 것
1. **창을 닫은 뒤 알림 센터에 남은 알림을 누르면** — ① 창을 다시 연다(트레이 「열기」 와 같음) ② 창을 닫을 때 그 알림들을 지운다 — 어느 쪽이 좋은가(W-1 · D-08 「닫으면 끊긴다」)
