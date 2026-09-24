# 리뷰 리포트 — strong-hajin-projects / WORK-006 Phase 1 탐침·fixture (2026-09-22)

## 판정: WARN — **Phase 1 은 진행 가능**

계약 위반(FAIL) **0건**. 아래 WARN 8건 중 **W-1 · W-2 는 Phase 2 가 «측정을 기록하기 전»에
고치는 것을 권한다** — 둘 다 코드 계약이 아니라 **계측 기록을 거짓으로 만드는** 자리다.
나머지 6건은 Phase 3(제품 셸)이 흡수할 때 반드시 같이 보는 항목이다.

**M-1 미측정은 FAIL 이 아니다.** 구현 보고서가 미실측을 통과로 쓰지 않았고(§4-1 「미측정이다.
통과로 쓰지 않는다」), TLS 우회를 만들지 않은 것을 코드에서 확인했다. 범위 문서의
「미실측 자체는 코드 FAIL 이 아니지만 미실측을 성공으로 보고하거나 계약과 반대 구현은 FAIL」
기준에 걸리는 것이 없다.

---

## 검수 범위

- **코드 워크트리**: `/Users/kknaks/orca/workspaces/Strong_hajin/strong-hajin-projects`
  · 브랜치 `kknaksss/strong-hajin-projects` · **HEAD `a1f67915aa8eeb551327b858428c5d4c1519e1b4`**
  (WORK §Code Surface 기준 HEAD 와 같다 — 발주 시 재확인 지시 이행)
- **diff**: 커밋 0건. 워킹트리 변경만 — **수정 2 · 신규 27 = 29개**
  (`git add -An --dry-run frontend/` 로 직접 셈. 보고서 §2 의 29 와 일치)
- **읽은 기준**: 코드 `AGENTS.md` · `roles/strong-hajin/reviewer/{role,rules,tools,workflow}.md` ·
  `tauri-p1-review-scope.md` · `tauri-code-review-focus.md` · `tauri-p1-url-note.md` ·
  `tauri-p1-implementation-brief.md` · `tauri-p1-implementation-report.md` ·
  `tauri-overnight-execution.md` · `tauri-implementation-status.md` ·
  SPEC-006 §4·§5 · WORK-006 §계약 불변식·§Code Surface·§Phase 1
- **참조(읽기전용)**: `/Users/kknaks/git/toy_pr2/task_management/app/front/src-tauri/src/lib.rs:49-88`
  (Windows 마이크 이식 원본 대조용). canonical `toy_pr2/{kknaks_profile,Strong_hajin}` 은 열지 않았다
- **산출물**: 이 파일 1개. **코드·설정을 한 글자도 고치지 않았다** (검수 종료 시점 `git status --porcelain`
  이 착수 시점과 동일: 수정 2 · untracked 6줄)

### 실행한 좁은 검증 — 보고서 수치를 **옮기지 않고 대조**했다

범위 문서의 「이미 실행된 전량 검사는 반복하지 않는다 · 필요한 좁은 검증만 허용」에 따라
전체 FE 스위트(1034건)·`npm run build` 는 **다시 돌리지 않았다.** 다음만 직접 실행했다.

| # | 명령 | 결과 | 보고서 주장과 대조 |
|---|---|---|---|
| R-1 | `npx tsc --noEmit` | **exit 0 · 출력 0줄** | V-1 일치 |
| R-2 | `cargo test` (`frontend/src-tauri`) | **`21 passed; 0 failed`** · 21건 이름 전수 확인 | V-4 일치 |
| R-3 | `npx vitest run src/dev` | **`Test Files 2 passed · Tests 17 passed`** | 「늘어난 17건이 이번 추가분 전부」 일치 |
| R-4 | `grep -rl "탐침\|probe-root\|__TAURI_INTERNALS__\|wake_guard\|@tauri-apps" dist/` | **0건** (`dist/` mtime 19:05 = 보고서 빌드본) | V-7 일치 (검색어에 `@tauri-apps` 를 더해도 0) |
| R-5 | `git check-ignore -v frontend/.dev-certs/{dev-ca.key,localhost.pem}` · `src-tauri/target` | 전부 `frontend/.gitignore` 로 제외 | 「키·인증서가 커밋 목록에 없다」 일치 |
| R-6 | `strings`·`otool -s __TEXT __info_plist target/debug/scax-probe-shell` | `NSMicrophoneUsageDescription` **박혀 있음** | `Info.plist` 주석의 「dev 에서도 프롬프트가 뜬다」 전제 **확인됨**(M-4 의 전제조건) |
| R-7 | `python3 socket.getaddrinfo("localhost",5180)` · `/etc/hosts` | **`::1` 이 먼저**, 그 다음 `127.0.0.1` | → **W-1** |
| R-8 | `cargo check --locked --target x86_64-pc-windows-msvc` | **실패 — 우리 소스가 아니라 빌드 스크립트**: `tauri-winres-0.3.6 … NotAttempted("llvm-rc")` | → **W-3** (Cargo.lock 무변경: `--locked`) |
| R-9 | 결과물 정합 확인 | `Cargo.lock` 의 `tauri = 2.11.6`(≥2.11.1) · `tauri-build 2.6.3` · `url 2.5.8` · `webview2-com 0.38.2` | 완료기준 「2.11.1 이상」 **충족** |
| R-10 | `gen/schemas/capabilities.json` 실물 해석 결과 확인 | 권한 4개 · `remote.urls` 1개 · `windows:["main"]` · **`"local": true`(기본값)** | → **W-6** |

> R-8 은 워커가 시도하지 않은 검사다. **결론: 이 기기에서 Windows 축은 «실행»뿐 아니라
> «컴파일»도 검증되지 않았다.** 원인은 소스가 아니라 호스트에 `llvm-rc` 가 없어서이고,
> `x86_64-pc-windows-msvc` 타깃 자체는 설치돼 있다.

---

## 위반 (FAIL 사유) — **없음**

allowed_paths 이탈 0건. 브리프 §4 가 연 자리(`frontend/src-tauri/**` · `frontend/src/dev/**` ·
`frontend/package.json`+lockfile · frontend 전용 fixture 설정·엔트리·실행 스크립트·관련 ignore)
**밖의 파일이 diff 에 하나도 없다.** `frontend/src/features/**` · `src/lib/api.ts` · `src/App.tsx` ·
`vite.config.ts` · `tsconfig.json` · `backend/**` · `docs/**` 전부 0줄 —
`git status --porcelain` 과 `grep -rn "src/dev\|probeShell\|probeRecording\|ProbePage\|@tauri-apps" src`
(dev 밖 **매치 0**)로 각각 확인했다.

---

## 경미 (WARN) — 8건

### W-1 · fixture 가 `127.0.0.1` 에만 붙는데 셸은 `localhost` 를 연다 — **M-1 재현의 취약점**

- `frontend/vite.probe.config.ts:34` — `host: "127.0.0.1"` (바인딩이 IPv4 하나)
- `frontend/src-tauri/src/lib.rs:37` — `DEFAULT_PROBE_URL = "https://localhost:5180/probe.html"`
- `frontend/src-tauri/capabilities/probe-fixture.json:7` — `"https://localhost:5180/*"`
- **근거(R-7)**: 이 기기에서 `localhost` 는 **`::1` 을 먼저** 돌려준다. `[::1]:5180` 에는
  아무도 듣지 않는다. 즉 웹뷰의 첫 연결 시도는 **거절**되고, IPv4 로 넘어가는 것은
  클라이언트의 fallback 에 기댄다.
- **왜 중요한가**: M-1 은 Phase 2 의 **중단 판정 근거**다(WORK §Phase 1 「실패 시 다음 조치」).
  「커맨드 왕복이 안 된다」와 「fixture 에 애초에 닿지 않았다」가 섞이면 그 판정이 틀린다.
  구현 보고서 §4-1 은 실패 원인을 **「추정이 아니라 구조상 확실한 것 — CA 미신뢰」** 로 단정했는데,
  남긴 로그는 `[probe][load] started` **부재**뿐이고 **TLS 에러 원문이 없다.** 부재는 TLS 거절과
  연결 실패 둘 다와 똑같이 들어맞는다. curl(V-8)이 200 을 받은 것은 curl 의 fallback 을
  증명할 뿐 WKWebView 를 증명하지 않는다.
- **권장 최소 수정**: `vite.probe.config.ts:34` 을 `host: "localhost"` 로 (vite 가 양쪽 스택에
  듣는다). leaf 인증서 SAN 에 이미 `DNS:localhost, IP:127.0.0.1, IP:::1` 이 들어 있어
  (`scripts/dev-https-cert.mjs:60`) 인증서 재발급이 필요 없다. **capability·URL 은 그대로 둔다.**
- **Phase 2 에 대한 요구**: M-1 을 「미측정」으로 닫을 때 **실패 원문(TLS 에러 코드 또는
  연결 거절)을 한 줄이라도 남긴다.** 지금 기록으로는 원인을 확정할 수 없다.

### W-2 · 계측 페이지가 **IPC 실패를 마이크 실패로 적는다** — 측정 기록이 거짓이 된다

- `frontend/src/dev/ProbePage.tsx:233` 에서 `running.current` 를 세우고 **녹음을 이미 시작한 뒤**,
  `:237` 에서 `guard?.acquire(...)` 를 같은 `try` 안에서 부른다.
- `:239-243` 의 `catch` 는 이 실패를 **`M-4 마이크 열기 실패(E-13) — 점유를 걸지 않았다`** 로 찍고
  `setMicError` 까지 세운다. **실제로는 마이크가 열렸고 녹음이 돌고 있으며 실패한 것은
  `wake_guard_acquire`(= `E-14a`)다.**
- **근거**: SPEC-006 §4 Case Matrix — `E-13`(마이크가 안 열린다)과 `E-14a`(셸은 있는데 커맨드
  호출이 실패)는 **웹이 하는 일도 사용자에게 보이는 것도 다른 줄**이다.
  `tauri-code-review-focus.md` 「mic 오류·IPC 실패 표시」가 보라고 한 자리다.
- **왜 중요한가**: 이 페이지의 존재 이유가 M-2·M-4 를 «가르는» 것인데, 갈라야 할 두 사유를
  한 줄로 합쳐 찍는다. Phase 2 기록에 「마이크가 안 열렸다」가 남으면 **중단 판정이 잘못 열린다.**
- **권장 최소 수정**: `getUserMedia`+`MediaRecorder` 구간과 `guard.acquire` 구간의 `try` 를 가르고,
  후자의 실패는 `E-14a` 로 찍는다(녹음은 계속 — `E-14a` 가 「degraded 와 같게 녹음을 계속」이다).

### W-3 · Windows 축은 **실행이 아니라 컴파일도 미검증**이다 — 보고서의 표현이 한 단계 약하다

- 구현 보고서 §4-3 은 「Windows 축은 한 건도 **실행**하지 않았다」로 적었고, §3 V-3 은
  `cargo check --all-targets` **exit 0 · warning 0 · error 0** 을 나란히 놓았다.
- **사실**: `frontend/src-tauri/src/power.rs:278-326`(`mod windows`)와
  `src/lib.rs:251-287`(`allow_microphone_on_webview2`)는 전부 `#[cfg(windows)]` 라
  **macOS 의 `cargo check` 가 한 줄도 보지 않는다.** V-3 의 exit 0 은 Windows 코드에 대한
  증거가 아니다.
- R-8 로 교차검증을 시도했으나 `tauri-winres` 가 `llvm-rc` 를 찾지 못해 **빌드 스크립트 단계에서**
  멈췄다 — 우리 소스의 오류가 아니지만, **그래서 컴파일 증거도 없다.**
- 소스 자체는 참조 제품(`task_management/.../lib.rs:49-88`)과 **자구까지 동일**하고,
  `webview2-com-sys 0.38.2` 의 `add_PermissionRequested(…, token: *mut i64)` 와
  `let mut token: i64 = 0` 의 타입이 맞는 것까지는 바인딩 소스로 확인했다. 즉 **명백한 오류는
  보이지 않는다** — 다만 그것은 코드 읽기이지 컴파일이 아니다.
- **권장**: 상태표·보고서에 Windows 를 「**컴파일 미검증 · 실행 미검증**」으로 두 칸 분리해 적는다.
  `llvm-rc`(LLVM 설치본) 하나면 `cargo check --target x86_64-pc-windows-msvc` 가 열린다 —
  이것은 **전역 툴체인 설치**라 코디 판단 사항이고, 없으면 OQ-W01 「검증 불가」 그대로가 맞다.

### W-4 · macOS 재무장이 **캐시된 assertion id 앞에서 no-op** 이다

- `frontend/src-tauri/src/power.rs:243-245` — `if self.id.is_some() { return PowerOutcome::Engaged; }`
- SPEC-006 §4 `wake_guard_acquire`·`E-09`: 재요청은 「**그 시점에 OS 절전 방지가 걸려 있지 않으면
  다시 건다**」. 지금 구조는 id 를 들고 있는 한 **OS 에 되묻지 않고 `Engaged` 를 답한다** —
  L-14(수동 절전에서 깨어난 뒤)의 재확인이 macOS 에서 **형식만 남는다.**
- **FAIL 로 올리지 않는 이유**: 방향이 반대가 아니다(푸는 쪽으로 가지 않는다). 또 SPEC §5 가
  「OS 쪽 상태를 상시 감시한다고 보장하지 않는다」를 명시해 **상시 감시 부재 자체는 계약 안**이다.
  다만 「재요청 = 확인 + 필요하면 재무장」이라는 `E-09` 의 절반이 macOS 에서는 서 있지 않다.
- **Phase 3 이 정할 것**: `IOPMAssertionSetProperty`/재생성으로 실제 확인을 넣을지, 아니면
  「macOS 는 확인 수단이 없다」를 SPEC 쪽 한계로 올릴지. **Phase 2 의 M-9 가 이 칸을 재는 자리다.**

### W-5 · Windows `engage` 실패 뒤 `disengage` 가 **OS 요구를 지우지 않고 빠져나간다**

- `frontend/src-tauri/src/power.rs:302-308` — `SetThreadExecutionState` 가 0 을 돌려주면
  `self.engaged = false` 로 내린다.
- `frontend/src-tauri/src/power.rs:312-315` — `disengage` 는 `if !self.engaged { return Released; }`
  로 **곧장 나간다.**
- **경로**: ① engage 성공(OS 에 `ES_CONTINUOUS|ES_SYSTEM_REQUIRED` 가 섰다) → ② 재무장 호출이
  실패(0 반환) → `engaged=false` → ③ release/창 닫기의 `disengage` 가 **아무 호출 없이** `Released`.
  OS 요구는 **스레드가 살아 있는 동안 계속 남는다.**
- **영향 방향은 안전한 쪽**(덜 푸는 것이 아니라 더 오래 깨어 있는 것)이고, 스레드 종료(L-13 앞자리)
  에서 OS 가 회수한다. 그래서 WARN 이다. **Windows 실기가 없어 관측되지 않았다**(W-3 과 같은 칸).
- **권장 최소 수정**: 실패해도 `engaged` 를 내리지 말거나, `disengage` 의 이른 반환을 없앤다.

### W-6 · capability 가 `local` 을 **명시하지 않아 기본값 `true`** 로 해석된다

- 원본 `frontend/src-tauri/capabilities/probe-fixture.json:1-15` 에 `local` 키가 없다.
- 해석 결과 `frontend/src-tauri/gen/schemas/capabilities.json` 에 **`"local": true`** 가 박힌다(R-10).
- **지금 실제 위험은 없다**: 이 셸은 `app.windows: []`(`tauri.conf.json:10`)이고 창을
  `WebviewUrl::External`(`src/lib.rs:308`)로만 띄운다 — 로컬 문서가 존재하지 않는다.
  **원격 허용은 `https://localhost:5180/*` 하나뿐**이고 와일드카드 서브도메인이 없다(계약 충족).
- **그래도 적는 이유**: `tauri-code-review-focus.md` 가 「로컬 다른 origin/프레임/외부 navigation 에서
  OS 기능을 넓혀주지 않는다」를 Phase 1 우선 검수로 세웠다. Phase 3 의 제품 셸은 로컬 자산을 가질
  수 있고, 그때 이 기본값이 **경계를 조용히 한 칸 넓힌다.**
- **권장**: `"local": false` 를 **명시**해 경계를 기본값이 아니라 글자로 세운다.

### W-7 · `Destroyed` 정리가 창 label 을 **`"main"` 으로 박았다**

- `frontend/src-tauri/src/lib.rs:380` — `event_shell.clear_window("main", "window-destroyed(L-06)")`
- 같은 파일 `:333` 의 `on_page_load` 는 `window.label()` 을 제대로 쓴다. 한 파일 안에서 기준이 둘이다.
- 창이 하나뿐이라 **지금은 동작이 같다.** 다만 `guard.rs:70-75` 의 `clear_window` 는 창별로 갈라
  두었고(`:207-216` 테스트가 「그 창의 세션만 비운다」를 지킨다), Phase 3 이 창을 늘리면
  **닫힌 창이 아니라 `main` 을 비우는** 버그가 된다.
- **권장 최소 수정**: `on_window_event` 의 클로저에서도 label 을 값으로 잡아 쓴다.

### W-8 · fixture 전용 의존성이 **제품 `dependencies`** 에 들어갔다 / 보고서 파일표 1칸 누락

- `frontend/package.json:57` — `@tauri-apps/api` 가 `dependencies`.
  (`@tauri-apps/cli` 는 `:70` devDependencies 로 옳게 들어갔다.)
- 이 패키지를 쓰는 곳은 `frontend/src/dev/probeShell.ts:44` 하나뿐이고 **제품 번들에는 들어가지
  않는다**(R-4 로 재확인). 그래서 유출은 아니지만, **fixture 전용 의존성이 제품 런타임 의존성으로
  선언**돼 있다 — 브리프 §3 「제품 빌드에 계측 화면/권한이 유출되지 않게」의 뜻과 결이 다르다.
- **권장**: `devDependencies` 로 옮긴다(Phase 4 가 제품 배선을 넣을 때 다시 올리면 된다).
- 함께: 구현 보고서 §2 의 파일표가 **`frontend/src-tauri/tauri.conf.json` 을 빠뜨렸다.**
  총계 29 는 맞고 실물도 29개지만 표에 열거된 것은 28개다. 검수자가 표만 읽으면
  **capability 다음으로 중요한 파일 하나를 못 본다.**

---

## 확인한 것 (PASS 근거) — 범위 문서 「핵심」 전 항목

| 검수 항목 | 결과 | 근거 |
|---|---|---|
| **capability remote origin 정확성** | **PASS** | `capabilities/probe-fixture.json:6-8` — `remote.urls` 가 `https://localhost:5180/*` **하나**. 와일드카드 서브도메인 0. 경로 `*` 뿐이라 origin 은 정확히 하나다. 해석 결과도 동일(R-10). 운영 도메인은 코드 어디에도 없다 |
| **외부 URL 표준 파서** (코디 지시 `tauri-p1-url-note.md`) | **PASS — 지시 이행 확인** | `guard.rs:144-150` 이 `tauri::Url::parse`(= `url` crate, lock 2.5.8), `guard.rs:155-157` 이 `url.origin().ascii_serialization()`. **자체 `url_lite` 잔재 0**. `on_navigation`(`lib.rs:313-331`)이 받는 타입과 같아 **커맨드 허용 origin 과 네비 허용 목록이 한 기준**이다. 정규화 회귀시험 `guard.rs:265-276` 이 기본포트 생략·`userinfo`(`https://evil@localhost:5180/`)·대소문자·opaque(`"null"`)를 고정 |
| **TLS 우회 부재** | **PASS** | 신규 파일 전수 grep(`rejectUnauthorized`·`NODE_TLS_REJECT_UNAUTHORIZED`·`insecure`·`accept_invalid`·`danger*`·`ignore-certificate`) **0건**. `vite.probe.config.ts:21-27` 은 인증서가 없으면 **던지고 멈춘다**(우회 없음). `scripts/dev-https-cert.mjs:74-84` 는 신뢰 설치 명령을 **출력만** 한다 |
| **키체인/전역 신뢰 자동설치 부재** | **PASS** | `keyring`·`keychain` grep 0(`Cargo.toml` 에 `keyring` 없음 — D-02 이행). `security add-trusted-cert` 는 `dev-https-cert.mjs:76` 의 **console.log 인자**일 뿐 실행 경로가 아니다. 키 2개는 `chmod 0600`(`:69`) + `.gitignore`(R-5) |
| **명령 4 · 응답 형식** | **PASS** | `lib.rs:386-391` `generate_handler![shell_info, wake_guard_acquire, wake_guard_release, open_external]` · `build.rs:9-14` 의 `AppManifest::commands` 4개 · `permissions/autogenerated/` 에 정확히 4개 toml · capability 허용 4개. **다섯째(`wake_lease_renew`) 없음**. 응답은 `ShellInfo{shell_api, app_version, platform, features}`(`lib.rs:72-78`, SPEC §4 필드와 일치) · `WakeReply{state}` 가 `off/on/degraded`(`lib.rs:59-70`, `serde rename_all="lowercase"`) |
| **TTL·주기 갱신·참조계수 부재 (I-3)** | **PASS** | 셸·웹 양쪽 타이머 0. 점유는 `BTreeSet<String>`(`guard.rs:28`)로 **이름의 집합**이지 카운터가 아니다. `guard.rs:166-174` 가 「두 번 걸어도 한 번 풀면 풀린다」를 고정. 웹 쪽 `probeShell.ts` 에도 `setInterval`/재시도 루프 없음 |
| **OS 절전 assertion 수명 · Windows 호출 스레드 일관성** | **PASS** | `power.rs` 전체가 **전용 스레드 1개**(`scax-wake-guard`, `:66-84`) 소유. 커맨드는 `spawn_blocking`(`lib.rs:219·232`)으로 들어와도 OS 호출은 그 스레드로 모인다. 회귀시험 `power.rs:366-398` 이 **8개 호출 스레드**로 「전부 같은 스레드 · 호출 스레드가 아님」을 강제 — Windows `SetThreadExecutionState` thread-bound 문제의 **올바른 방향**이다. macOS 는 `PreventUserIdleSystemSleep` 하나만(`power.rs:180`) — `NoDisplaySleep`·`PreventSystemSleep`·`ES_DISPLAY_REQUIRED`·`ES_AWAYMODE_REQUIRED` **전부 없음**(화면 꺼짐·수동 절전 보존, DEC-005 D-03) |
| **종료 교착 수정과 회귀시험의 실효성** | **PASS — 실제로 그 경로를 검사한다** | `Op::Shutdown`(`power.rs:44·75`)이 **명시 사건**이고 `Drop`(`:118-131`)이 그것을 «보낸 뒤» join 한다. 회귀시험 `power.rs:414-437` 이 **`power.tx.clone()` 을 살려 둔 채** 다른 스레드에서 drop 하고 `recv_timeout(10s)` 로 받는다 — 구 구조(채널 닫힘 기대)에서는 이 시험이 **반드시 매달린다.** 짝 시험 `:439-447` 이 스레드 부재를 실패로 답하게 한다(`E-14a` 의 네이티브 쪽). 어느 길로 나가도 `backend.disengage()`(`:82`)로 푼다. **R-2 로 21건 전건 통과 재확인** |
| **acquire/release race · 최종 잔존 0 (I-7)** | **PASS(선택한 수단 기준)** | 네이티브: 장부 `Mutex` 를 **OS 호출 동안 들고 있어**(`lib.rs:100·130-132`) 교차가 없고, 16 스레드 동시 획득/해제 뒤 잔존 0 을 `lib.rs:471-489` 가 검사. 웹: `probeShell.ts:79-105` 가 **세션 키별 직렬화** — 「같은 세션의 해제는 진행 중인 획득 뒤」. 시험 `probeShell.test.ts:47-64` 가 **응답 전에 release 를 걸어** 순서를 관측하고, `:66-84` 가 「획득이 실패해도 뒤의 해제가 막히지 않는다」를 본다(실패 하나가 점유를 남기는 길 차단). SPEC 이 수단을 지정하지 않고 결과만 요구하므로 tombstone·타이머 부재가 맞다 |
| **CloseRequested vs Destroyed** | **PASS — 계약과 같은 방향** | `lib.rs:366-377` `CloseRequested` 는 **아무것도 풀지 않는다**(로그만). `lib.rs:378-381` `Destroyed` 에서만 `clear_window`. `SCAX_PROBE_CANCEL_FIRST_CLOSE`(`:296·369-373`)가 첫 닫기를 취소해도 정리 코드가 돌지 않는다 → I-4·I-5·`E-12`·AC-T36 의 «요청≠완료» 구분이 코드 구조로 서 있다. **커맨드를 늘리지 않고 환경변수로 연 것**도 I-2 를 지킨 선택이다 |
| **문서 교체 정리(L-09) vs 막힌 이동(L-11)** | **PASS** | `lib.rs:332-353` `PageLoadEvent::Started` 에서만 `clear_window("document-replaced(L-09)")`. 막힌 네비게이션(`:320-329`)은 **`allowed=false` 를 돌려주고 외부 브라우저로 넘길 뿐 아무것도 풀지 않는다**(`E-05`·L-11, `:328` 로그가 그 뜻을 적는다). `guard.rs:78-82` `bump_generation` 은 **점유를 건드리지 않고**, 그 사실을 `guard.rs:219-227` 이 고정한다 — 「카운터 올리는 것만으로 풀리면 같은 문서 안 주소 변경이 녹음을 깬다」 |
| **AC-T41(문서 교체 전 요청이 새 문서 점유를 만들지 않는다)** | **범위 밖 — Phase 3 몫으로 올바르게 남겼다** | 네이티브 보상 수단 미구현. `generation`(`guard.rs:30`)은 **로그 전용**이고 게이팅에 쓰이지 않는다(`lib.rs:338-347`). **구조가 계약과 반대가 아니고**(자리를 남겨 뒀다) 보고서 §6-7·B-4 가 한계를 그대로 적었다. WORK 는 AC-T41 측정을 **Phase 5(M-14)** 로 배치했다 — 범위 문서의 「미작성 단계를 Phase 1 전체 실패로 확대하지 않되 방향이 반대면 수정」 기준에 따라 **지적하지 않는다** |
| **Mic 권한 최소화** | **PASS** | `Info.plist` 는 `NSMicrophoneUsageDescription` **한 키**, `Entitlements.plist` 는 `com.apple.security.device.audio-input` **한 키**. 카메라·위치·네트워크 서버 등 **추가 키 0**. Windows 는 `COREWEBVIEW2_PERMISSION_KIND_MICROPHONE` 일 때만 `ALLOW`(`lib.rs:269-271`) — 다른 종류는 손대지 않고 기본 동작에 맡긴다. R-6 으로 dev 바이너리 임베드까지 확인 |
| **fixture 와 제품 빌드 격리 (probe/product 경계)** | **PASS — 4중으로 확인** | ① 설정 분리: `vite.probe.config.ts` 는 `--config` 로만 쓰이고(`package.json:9`), 제품 `vite.config.ts` 무변경 · `rollupOptions.input` 없음 → 기본 입력 `index.html` 하나 ② 엔트리 분리: `index.html:15` 는 `/src/main.tsx` 만, `probe.html:15` 는 `/src/dev/probeMain.tsx` ③ 참조 0: `src/` 에서 dev 밖이 `src/dev`·`probeShell`·`ProbePage`·`@tauri-apps` 를 **참조하지 않는다**(grep 매치 0) ④ 산출물 0: `dist/` 유출 grep 0건(R-4) |
| **MIME 2경로 drift 테스트가 «실제로» 제품을 본다** | **PASS** | `probeRecording.test.ts:4-5` 가 제품 소스를 `?raw` **문자열로** 읽는다(모듈 import 아님 — 번들 경계 유지). 대조 결과 실물과 일치: `microphone.ts:17 const MIME_TYPE = "audio/webm;codecs=opus"` · `:15 export const CHUNK_MS = 250` · `liveTranscription.ts:13 ['audio/webm;codecs=opus','audio/webm','audio/mp4']`. `:23-25` 가 **「회의 라이브에 후보 목록이 생기지 않았다」**(`isTypeSupported` 부재)까지 잡는다 — 중단 판정 전제가 바뀌는 것을 막는 줄이다. **두 경로를 뭉치지 않는다**(`probeRecording.ts:41-47` 이 `meetingLive` / `browserCandidates` / `browserChosen` 을 따로 낸다) |
| **명시적 녹음 종료 · 장치 해제** | **PASS** | `ProbePage.tsx:248-262` — `recorder.stop()` 을 try 로 감싸고(이미 끝난 장치에서 던져도 해제를 못 부르는 일이 없게), **`stream.getTracks()` 전부 `track.stop()`**, 그 뒤 `guard.release`. 시작 실패 경로도 `:222` 에서 트랙을 닫는다 |
| **테스트가 구현을 베끼는가, 실제 경합·실패를 보는가** | **PASS(대체로) — 베끼기 아님** | 실패를 «실제로» 만드는 시험들: 16 스레드 동시 획득/해제(`lib.rs:471-489`) · 8 스레드 OS 호출 스레드 동일성(`power.rs:366-398`) · sender 사본 생존 종료(`power.rs:414-437`) · 스레드 부재(`power.rs:439-447`) · 응답 전 release 삽입(`probeShell.test.ts:47-64`) · 획득 실패 뒤 해제 진행(`:66-84`) · 제품 소스 원문 대조(drift 4건). **가짜 백엔드(`FlakyBackend`·`Spy`)로 OS 실패를 주입**해 `degraded` 가 점유를 세우는 것까지 본다(`lib.rs:433-439`) |
| **allowed_paths · 잠금파일 · ignore 정합** | **PASS** | 이탈 0(위 「위반」절). `frontend/.gitignore` 4줄은 전부 **산출물·비밀**(`.dev-certs/` · `src-tauri/target/` · `gen/schemas/` · `permissions/autogenerated/`) — 소스를 가리지 않는다. `src-tauri/Cargo.lock` 은 **커밋 대상에 포함**(add 목록 확인). `package-lock.json` +229줄이 추가 2 패키지 + 플랫폼 optional 로 설명된다. R-8 을 `--locked` 로 돌려 **검수가 lock 을 건드리지 않았다** |
| **제품·백엔드 무영향** | **PASS** | `backend/**` · `docs/unified-operations-inventory.json` 0줄 → `tests/architecture/test_operation_inventory.py` 의 drift 대상이 아니다(AGENTS.md 규칙상 재실행 불필요). 기존 FE 테스트는 **전량 재실행하지 않았다**(범위 문서 지시) — 대신 tsc 0(R-1)과 신규 17건 단독 통과(R-3)로 「신규 실패 0」의 신규분을 확인했다 |
| **완료 기준: `tauri` ≥ 2.11.1** | **PASS** | `Cargo.toml:24` 하한 `2.11.1`, `Cargo.lock` 해석값 **2.11.6**(R-9). GHSA-7gmj-67g7-phm9 하한 충족 |
| **원격 문서 ACL 경계의 근거** | **확인함** | 보고서 §6-1 의 `!is_local` 주장은 **실물 산출물로 뒷받침된다** — `permissions/autogenerated/{shell_info,wake_guard_acquire,wake_guard_release,open_external}.toml` 이 생성됐고 capability 가 그 넷을 나열한다. `tauri-plugin-opener` 는 **Rust 쪽에서만** 쓰고 플러그인 권한을 webview 에 주지 않아 `open_path`·`reveal_item_in_dir` 이 웹에 열리지 않는다(AC-T23). **다만 이 경계가 «실제로» 막는지는 M-1 이 안 돌아 미관측이다** |

---

## 자동검증으로 «닫힌» 자리 vs 사용자 실기 E2E 에서만 답이 나는 자리

범위 문서 요구대로 갈라 적는다. **이 구분을 흐리면 미실측이 통과로 둔갑한다.**

### A. 자동검증으로 닫혔다 (이 검수에서 재확인)

- 커맨드 **넷**과 그 ACL 권한 4개의 존재 · TTL/다섯째 커맨드 부재
- 점유 장부의 수명 규칙: 중복 획득·늦은 해제·모르는 세션·창 정리·다중 세션 (`cargo test` 21건)
- OS 호출의 **단일 스레드 고정**과 종료 시 해제 · 종료 교착 회귀 (`power.rs` 4건)
- 웹 쪽 **같은 세션 직렬화**와 실패 전파 (`probeShell.test.ts` 8건)
- **제품 포맷 drift** 4건 — 제품 소스 원문과 계측 상수의 일치
- 표준 URL 파서의 origin 정규화 · `open_external` 스킴 제한
- fixture ↔ 제품 빌드 격리(설정·엔트리·참조·산출물 4중)
- 비밀(키·인증서) 커밋 제외 · TLS 우회 부재 · keyring 부재

### B. 실기에서만 답이 난다 — **오늘 닫히지 않았다**

| 항목 | 상태 | 누가·언제 |
|---|---|---|
| **M-1** 원격 https 문서 ↔ 커맨드 왕복 | **미측정.** `[probe][load] started` 부재까지만 관측 | 사용자가 CA 신뢰 설치 후(§W-1 의 실패 원문 기록 조건 포함) |
| **M-7** 연결 실패를 셸이 감지 | **미측정 · 선행 관측은 부정적** — `on_page_load` 가 발화하지 않았다. SPEC U-2 가 「감지 수단이 없다고 판명되면 구현 차단 사유」로 표시한 지점 | Phase 2 정식 측정 → Phase 3 수단 결정 |
| **M-2 / M-2b** 두 경로 × 세 갈래 = 여섯 칸 | **조작 수단만 있다.** `isTypeSupported` 값도 아직 안 찍었다 | Phase 2 (사용자+코디) |
| **M-3** 네비게이션 훅 발화/미발화 | 조작 버튼 6개 준비됨. **훅이 pushState·해시에 «안» 터지는지는 미관측** | Phase 2 |
| **M-4** 마이크 프롬프트 | **미측정.** 전제조건(`Info.plist` 임베드)만 R-6 로 확인 | 사용자 |
| **M-5** 재시작 후 쿠키 지속 | 미측정 (`incognito(false)` 설정만 확인) | 사용자 |
| **M-6** 창 닫기 되묻기 층 | 미측정 | 사용자 |
| **M-8** 외부 링크 동작 | 미측정 | Phase 2 |
| **M-9** 자동 절전만 막는가 | **미측정.** `pmset -g assertions` 관찰 없음. macOS 재무장은 W-4 의 한계를 안고 잰다 | 사용자 · `max(3T,30분)` |
| **Windows 축 전부** | **컴파일·실행 둘 다 미검증**(W-3) | OQ-W01 |
| 제품 테스트 flake 1회(이름 미특정) | 재현 안 됨. 이번 diff 밖 | 반복되면 코디 추적 |

---

## 기존 부채 (이번 판정 제외)

- `frontend/src/features/browser/liveTranscription.ts` 는 작은따옴표,
  `features/meetings/microphone.ts` 는 큰따옴표를 쓴다. drift 시험의 정규식
  (`probeRecording.test.ts:28`)이 **작은따옴표에 묶여** 있어, 저장소가 포매팅을 통일하면
  거짓 실패가 난다. **실패 방향이 안전한 쪽**(조용히 통과가 아니라 붉어진다)이라 부채로만 적는다.
- `SCAX_PROBE_URL`/`SCAX_PROBE_NAV_ALLOW`(`lib.rs:41-56`)는 **네비게이션 허용 목록을
  환경변수로 넓힐 수 있다.** 탐침 단계에서는 필요한 손잡이이고 **커맨드 허용 origin 은
  capability 에 박혀 있어 함께 넓어지지 않는다**(경계가 둘로 갈린 것이 오히려 SPEC §5 와 같다).
  **Phase 3 의 제품 셸은 이 손잡이를 계승하면 안 된다** — 흡수 시 명시적으로 제거할 것.

---

## 코디에게 — 최소 조치 제안

1. **Phase 2 착수 전 2건만 고친다**(fixture 품질, 계약 아님):
   **W-1** `vite.probe.config.ts:34` → `host: "localhost"` · **W-2** `ProbePage.tsx:237` 의 try 분리.
   둘 다 한 줄~다섯 줄이고, 고치지 않으면 **Phase 2 기록이 틀린 사유로 남는다.**
2. **상태표 정정 2건**: Windows 를 「컴파일 미검증 · 실행 미검증」 두 칸으로(W-3) ·
   M-1 실패 사유를 「원인 미확정(TLS 에러 원문 없음)」으로(W-1).
3. **Phase 3 흡수 시 인계 목록**: `Op::Shutdown`(보고서 §6-3 이 이미 적었다) · W-4 macOS 재무장 ·
   W-5 Windows 해제 · W-6 `local:false` 명시 · W-7 label 하드코딩 · `SCAX_PROBE_*` 손잡이 제거 ·
   AC-T41 보상 수단 결정.
4. **W-8** `@tauri-apps/api` 를 `devDependencies` 로 · 보고서 §2 표에 `tauri.conf.json` 추가.
5. **Phase 1 은 진행 가능하다.** 커맨드 왕복이 «안 된다»는 관측이 아니므로
   WORK §Phase 1 「실패 시 다음 조치」의 **즉시 판정 게이트를 열 사유가 아니다.**
