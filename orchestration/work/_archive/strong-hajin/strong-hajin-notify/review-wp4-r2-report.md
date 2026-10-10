# 재검수 r2(좁게) — WP4-SHELL (W-1 · W-3 · W-4)

> reviewer(read-only) · 2026-10-08 · 앞 판 `review-wp4-report.md` · 손질 보고 `fe-wp4fix-report.md`
> 약어: `T/` = `frontend/src-tauri/` · `F/` = `frontend/src/`

## 0. 판정 — **PASS** (FAIL 0 · WARN 0 · 참고 3)

W-1 클릭 중계 · W-4 `target:null` 이 코드로 닫혔다. W-3 은 「Windows 에서 컴파일 확인 불가 · 배포 막음」 이 기록됐다. 경합 · 스레드 안전 · 누수에서 문제를 찾지 못했다. 커맨드 수(6 · 9) · capability · `build.rs` 는 그대로다.

### 실행한 것(관련만)
- `cd frontend/src-tauri && cargo test` → **81 passed**(77 + 중계 시험 4) · medi-ax 102 · clippy 0 은 워커 · 코디 수치를 받아들였다
- `npx vitest run src/lib/osNotifier.test.ts src/lib/shell.test.ts src/App.test.tsx --no-file-parallelism` → **exit 0 · 71 passed · Errors 0**
- `npx tsc --noEmit` → 0

## 1. W-1 클릭 중계 — 코드로

| 물음 | 코드 | 판정 |
|---|---|---|
| 하나만 보관 · 60초 상한 | `ClickRelay`(`T/src/notify.rs:89-140`) — `pending: Option<(Click, Instant)>` 한 칸 · 새 클릭이 갈아 끼움 · `on_ready` 가 `take()` 로 꺼내 `PENDING_CLICK_TTL`(60초) 안일 때만 돌려줌 → **한 번만** | PASS |
| 「준비됨」 = 웹이 `shell_info` 를 부름 | `shell_info`(`T/src/lib.rs:208-221`) — **메인 창**에서 불렸을 때만 `on_ready`. `shell_info` 는 capability 상 원격 앱 origin 문서만 부를 수 있다(`local:false`)<br>웹에서 부르는 곳은 `hasShellNotifications` 하나다(기억함 · 문서마다 한 번 — `F/lib/shell.ts:337-345`). 그것을 부르는 것은 로그인 뒤 서는 `OsNotificationBridge` 의 effect(`F/App.tsx:119`) · `notifyPermission` · `notifyShow` 다<br>**사건이 들리는가**: 브리지(자식)의 effect 가 IPC 를 비동기로 내고, App 의 `onShellNotificationClick` 구독(`App.tsx:493`)은 같은 커밋에서 동기로 걸린다. 셸의 `eval` 은 IPC 응답보다 먼저 올 수 없으므로 구독 뒤에 도착한다 | PASS |
| 문서 교체 · 창 파괴 때 다시 대기 | `on_page_load` `Started`(`lib.rs:646-650` — 메인 프레임 문서가 실제로 바뀔 때 · 같은 문서 안 주소 변경은 오지 않음) · `WindowEvent::Destroyed`(`:683-686`) → `on_document_gone` | PASS |
| 창 없으면 `REOPEN_MAIN`(medi-ax) | `notify_click`(`lib.rs:305-333`): 창이 없으면 클릭을 보관(`on_document_gone` 뒤 `on_click`)하고 `REOPEN_MAIN` 으로 창을 만든다. `REOPEN_MAIN` 은 트레이 「열기」 와 **같은 클로저**다(`lib.rs:787-801` — 옛 트레이 클로저를 옮김). strong-hajin 판엔 그 길이 없어 버린다(그 판은 마지막 창이 닫히면 프로세스가 끝나므로 이 갈래에 올 일이 거의 없다) | PASS |
| **경합 — 두 클릭** | 첫 클릭이 창을 만들면(`spawn_main_window` 가 돌아온 뒤 창이 있다), 두 번째는 「창 있음」 갈래로 가서 보관을 갈아 끼운다 → 준비되면 **마지막 클릭 하나**만 간다 | PASS |
| **경합 — 준비 전 창 파괴** | `Destroyed` 가 준비를 끄고 보관은 남긴다 → 다음 창(트레이 「열기」 · 다음 클릭)의 문서가 `shell_info` 를 부르면 60초 안일 때만 보낸다 | PASS |
| **동시에 둘 생성 금지(AC-T33)** | 창은 「없을 때만」 만든다. 트레이 「열기」 와 알림 클릭이 거의 동시에 둘 다 「없음」 을 보더라도, 같은 라벨(`main`)의 두 번째 생성은 Tauri 가 거절해 로그만 남는다 — 창이 둘 서지 않는다 | PASS |
| 스레드 안전 · 데드락 | 중계는 `SharedShell.clicks: Mutex<ClickRelay>`(`lib.rs:94,108`). `shell_info` 는 `clicks` 잠금을 문장 끝에서 놓은 **뒤** `target` 을 잠근다(중첩 없음). `notify_click` 은 `clicks` 하나만 잡는다 — 잠금 순서 문제 없음 | PASS |
| 누수 | 보관 한 칸 · 만료되면 다음 `on_ready` 가 버린다. 클로저 · 정적은 앱 수명 하나씩(의도) | PASS |
| 보내기 규칙 | `send_click`(`lib.rs:336-`) — 앱 origin 문서일 때만 `eval`(다운로드 사건과 같은 규칙) | PASS |
| 시험 | `notify.rs` 중계 4 — 준비된 문서에는 바로 · 준비 전엔 하나(새 것이 갈아 끼움) → 준비되면 한 번(두 번째 없음) · 60초 넘으면 버림 · 문서가 바뀌면 다시 보관 | PASS |

## 2. W-4 `target: null`

- 셸 `validate`(`T/src/notify.rs:71-74`): `target` 이 **객체 또는 null** — 나머지 검증(id 길이 · 제어문자 · 제목/본문 길이 · 4KB)은 그대로다. `validate` 는 `notify_show` 만 쓰므로 **다른 커맨드의 검증을 느슨하게 하지 않는다**
- userInfo 에 `"null"` 이 실리고 클릭 때 `Value::Null` 로 돌아온다
- 웹
  - `osNotifier.ts:65` 가 `item.target` 을 그대로 싣는다(옛 `{surface:"notifications"}` 바꿔치기를 걷음)
  - 「보고 있으면 생략」 은 `item.target &&` 로 null 을 건너뛴다(`:56`)
  - 클릭 → `readClickDetail` 이 `target: null` → `openNotification(id, null)` → 읽음 + 「열 수 없는 항목입니다」 · 화면 그대로(목록 줄과 같다)
- **묶음은 그대로** — `notification_id: null` · `target: {surface:"notifications"}`(`:46`) → 읽음 없이 목록
- 시험: osNotifier +1 · shell.test · App.test(`n-gone` + null → 토스트 · 읽음 POST · 화면 그대로) · Rust 검증
- 판정 **PASS**

## 3. W-3 Windows

시도 둘(strong-hajin · medi-ax `--features kakao-collector`)이 모두 이 Mac 에서 막혔다는 기록을 확인했다(`llvm-rc` 없음 · 카톡 수집기의 vendored OpenSSL 이 Windows C 교차 툴체인 요구). 「`cfg(windows)` 컴파일 확인 없음 · Windows 배포는 첫 확인 전까지 막음」 으로 기록됐다. 「medi-ax Windows 에서 `kakao-collector` 를 켤지부터 정해야 한다」 는 지적도 맞다(수집기는 Mac 전용). **기록 확인 — 판정 밖**.

## 4. 회귀

- 커맨드 등록 · capability · `build.rs` · 사건 이름 무변경 — 셸 시험(커맨드 6 · 사건 이름 대조) 통과
- `on_page_load` · `Destroyed` 에 한 줄씩 더했을 뿐 기존 L-09 · L-06(절전 방지 해제) 흐름은 그대로다(같은 자리 아래 기존 코드 무변경)
- 트레이 「열기」 는 같은 `spawn_main_window` 호출을 `REOPEN_MAIN` 클로저로 옮겼을 뿐이다(인자 같음)
- 웹 OS 발송기 · 셸 다리 · App 시험 71 통과 · exit 0

## 5. 참고 (판정 밖 — 실측 · 2루프)

- **R-1** 클릭으로 앱이 새로 뜬 뒤 **로그인까지 60초를 넘기면** 보관한 클릭은 버려진다(로그인 전엔 `shell_info` 를 부르지 않는다) — 워커가 dmg 실측 항목으로 남겼다. 의도와 맞다
- **R-2** 로그아웃 상태(같은 문서)에서도 App 의 클릭 구독은 살아 있다 — 이미 「준비됨」 인 문서에 클릭이 오면 `openNotification` 이 읽음 API(401)를 부르고 오류 띠가 설 수 있다. 드물다 — 실측에서 체감만
- **R-3** strong-hajin 이 꺼진 상태의 배너 클릭이 새 프로세스의 delegate 에 넘어오는지(setup 에서 delegate 를 거는 시점)는 서명 dmg 실측뿐이다(앞 검수 §8 #15 그대로)

## 6. 목록
- FAIL: 없음
- WARN: 없음
- 사용자에게 물을 것: 없음
