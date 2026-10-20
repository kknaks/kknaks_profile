# WP4 검수 손질 결과 — W-1 · W-3 · W-4

## 상태: done (커밋 없음 · W-2 · W-5 · W-6 은 손대지 않음)

- 정본: `review-wp4-report.md` §WARN · 코디 택일
- 손댄 파일: `frontend/src-tauri/src/notify.rs` · `frontend/src-tauri/src/lib.rs` · `frontend/src/lib/osNotifier.ts` · `frontend/src/lib/shell.ts` · 시험 `frontend/src/lib/osNotifier.test.ts` · `frontend/src/lib/shell.test.ts` · `frontend/src/App.test.tsx`. 커맨드 수 · capability · `build.rs` 는 그대로다(6 · 9)

## W-1 창이 없을 때 배너 클릭 — 코디 택일 ①

**클릭 중계** `notify::ClickRelay`(`T/src/notify.rs:89-140`) — 웹이 들을 준비가 됐는지 보고, 아니면 클릭을 **하나만** 보관했다가 준비되면 **한 번** 보낸다.
- 보관 상한은 `PENDING_CLICK_TTL = 60초` — 넘으면 버린다. 새 클릭이 옛 것을 갈아 끼운다
- **「웹 준비됨」 신호 = 메인 창의 앱 문서가 `shell_info` 를 부름**(`lib.rs:208-221`). 새 커맨드를 열지 않으려고 고른 길이다. 웹은 로그인 뒤 알림 다리를 세우며 `hasShellNotifications` → `shell_info` 를 한 번 부른다
  - 그 호출은 클릭 구독(`App` 의 `onShellNotificationClick` effect)이 걸린 같은 커밋 뒤에 비동기로 나간다. 그래서 그 뒤에 쏜 사건은 들린다
  - `shell_info` 는 원격 앱 origin 문서만 부를 수 있다(capability)
- 「준비 안 됨」으로 돌아가는 때: 문서 교체(`PageLoadEvent::Started` · `lib.rs:649`) · 창 파괴(`Destroyed` · `:685`)

**`notify_click`**(`lib.rs:305-333`)
- **창이 있으면** 앞으로(show · unminimize · focus) 가져온다. 웹이 준비됐으면 바로 보내고, 아니면 보관한다. strong-hajin 이 알림 클릭으로 **새로 뜬 경우**도 이 길이다 — 웹이 `shell_info` 를 부를 때 나간다
- **창이 없으면**(medi-ax 트레이 상주) 트레이 「열기」 와 **같은 길**로 창을 새로 만들고 클릭을 보관한다. 창이 없을 때만 만들므로 **둘이 동시에 서지 않는다**(AC-T33)
  - 그 길은 `REOPEN_MAIN`(`lib.rs:203`) 하나다. 트레이 「열기」 와 알림 클릭이 **같은 클로저**를 쓴다(`lib.rs:785-801` — 옛 트레이 클로저를 옮긴 것이다)
  - 그 길이 없는 판(strong-hajin — 마지막 창이 닫히면 프로세스가 끝남)은 버린다
- 보내기는 `send_click`(`lib.rs:336`) — 앱 origin 문서일 때만이다(다운로드 사건과 같은 규칙)

**시험**(`notify.rs`): 준비된 문서에는 바로 · 준비 전엔 하나만 보관(새 것이 갈아 끼움) → 준비되면 한 번(두 번째는 없음) · 60초 상한 넘으면 버림 · 문서가 바뀌면 다시 준비될 때까지 보관

⚠ **실측 남김(dmg)**:
- medi-ax 창을 닫은 뒤 알림 센터 배너를 누르면 창이 새로 서고 그 대상으로 가는가
- strong-hajin 이 꺼진 상태에서 배너를 누르면 앱이 새로 뜨고 그 대상으로 가는가(macOS 가 그 클릭을 새 프로세스의 delegate 에 넘기는지)
- 로그인 화면에서 60초 넘게 머물면 보관한 클릭은 버려진다(로그인 전에는 `shell_info` 를 부르지 않는다)

## W-3 Windows 컴파일 — **안 됨 · 이유**

| 시도 | 결과 |
|---|---|
| `rustup target add x86_64-pc-windows-msvc` | 이미 있음(`rust-std` up to date) |
| `cargo check --target x86_64-pc-windows-msvc`(strong-hajin) | **실패** — `tauri-build` 의 Windows 리소스 단계가 `llvm-rc` 를 요구한다: `NotAttempted("llvm-rc")`. 이 Mac 에 `llvm-rc` · `lld-link` 가 없다(Homebrew llvm 미설치 — 시스템에 설치하지 않았다) |
| `SHELL_FLAVOR=medi-ax cargo check --target x86_64-pc-windows-msvc --features kakao-collector` | **실패** — 같은 `llvm-rc` + `openssl-sys`(카톡 수집기의 vendored OpenSSL 이 Windows C 교차 툴체인을 요구) |

→ `cfg(windows)` 코드(플러그인 등록 · `NotificationExt` · webview2-com 0.39 마이크)는 **여전히 컴파일 확인 없음**이다. Windows 빌드 기계(또는 CI)에서 첫 확인이 필요하고, 그 전까지 Windows 배포는 막는다(코디 기록). 참고로 medi-ax 판의 카톡 수집기는 Mac 전용이라, medi-ax Windows 빌드에서 `kakao-collector` 를 켤지부터 정해야 한다.

## W-4 `target: null` OS 클릭 — 목록 줄과 같은 일

- **셸**: `notify::validate` 가 `target: null` 을 받는다(`notify.rs:72` — 객체 또는 null). userInfo 에는 `"null"` 이 실리고, 클릭 때 `Value::Null` 로 돌아온다
- **웹**:
  - `osNotifier.ts` 가 열 수 없는 알림도 `target: item.target`(null) 그대로 싣는다(옛 `{surface:"notifications"}` 바꿔치기를 걷었다)
  - `NotifyShowInput.target: NotificationTarget | null`(`shell.ts`)
  - 클릭 사건의 `target: null` 은 그대로 `openNotification(id, null)` 로 간다 → **읽음 + 「열 수 없는 항목입니다」 · 화면 그대로**(목록 줄과 같다)
- 묶음(`notification_id: null` · `{surface:"notifications"}`)은 지금대로 읽음 없이 알림 목록이다
- **시험**:
  - `osNotifier.test.ts` +1(null 그대로 싣기)
  - `shell.test.ts`(클릭 사건 `target: null` 넘김)
  - `App.test.tsx` 「OS 알림 클릭 사건」 에 단언 추가(`n-gone` + null → 토스트 · 읽음 POST · 화면 그대로)
  - Rust 검증 시험(null 허용)

## 검증 (관련만)

| 명령 | 결과 |
|---|---|
| `cd frontend/src-tauri && cargo test` | **81 passed**(77 → +4 중계 시험) · 0 failed |
| `SHELL_FLAVOR=medi-ax cargo test --features kakao-collector` | **102 passed** · 0 failed · 6 ignored(기존 실기기 시험) |
| `cargo clippy --all-targets -- -D warnings`(두 판) | **경고 0** |
| `cd frontend && npx vitest run src/lib/osNotifier.test.ts src/lib/shell.test.ts src/App.test.tsx --no-file-parallelism` | **exit 0** · 71 passed · Errors 0 |
| `npx tsc --noEmit` | **0 오류** |
