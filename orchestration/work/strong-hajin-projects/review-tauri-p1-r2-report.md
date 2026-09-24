# 재리뷰 리포트 (R2) — strong-hajin-projects / WORK-006 Phase 1 · W-1·W-2 수정 확인 (2026-09-22)

## 판정: **W-1 · W-2 둘 다 닫혔다 — Phase 2 진행 가능**

- **W-1 닫힘 (실측 확인)** — 두 loopback 주소가 **동시에** 뜨고, 셋 다 TLS 검증을 켠 채 200 을 받는다.
  바인딩은 loopback 둘뿐이다(LAN 노출 0).
- **W-2 닫힘 (코드 + 회귀 시험 확인)** — `E-13`(마이크)과 `E-14a`(IPC)가 로그·화면 **양쪽에서** 갈렸고,
  갈린 자리를 지키는 시험 6건이 실제로 그 자리를 본다.
- **회귀 0건** — `tsc` 0 · `src/dev` 23건 전건 통과 · 제품 빌드 exit 0 · 제품 산출물 유출 0 ·
  allowed_paths 이탈 0 · capability·셸 URL 무변경.
- **남은 WARN 6건(W-3~W-8)은 그대로**이고, **새 WARN 2건(N-1·N-2)** 을 추가로 적는다.
  **둘 다 Phase 2 를 막지 않는다** — Phase 3 흡수 목록에 올린다.

> **이 검수도 코드를 한 글자도 고치지 않았다.** 종료 시점 `git status --porcelain` 이 착수 시점과
> 동일하다(수정 2 · untracked 6줄). `npm run build` 로 `dist/` 가 갱신됐지만 `dist/` 는 `.gitignore:7` 이다.

---

## 검수 범위

- **워크트리** `/Users/kknaks/orca/workspaces/Strong_hajin/strong-hajin-projects` ·
  브랜치 `kknaksss/strong-hajin-projects` · **HEAD `a1f67915aa8eeb551327b858428c5d4c1519e1b4`**(변동 없음)
- **읽은 기준**: `review-tauri-p1-report.md` · `tauri-p1-fix-report.md` · `tauri-p1-implementation-brief.md` §4·§5
- **초점(발주 지시대로 넷만)**: ① vite fixture 바인딩·설정(두 loopback 주소) ② `ProbePage` 오류 분리·시험
  ③ allowed paths ④ 제품 빌드 경계
- **의도적으로 돌리지 않은 것**: 전체 FE 스위트(`make frontend-test`) · `cargo test` · `cargo check`.
  **Rust 는 이번 수정에서 한 줄도 바뀌지 않았고**(아래 §4 로 확인), 전량 검사는 초점 밖이다.
- **산출물**: 이 파일 1개.

---

## 1. W-1 — fixture 가 두 loopback 에 «동시에» 뜬다 · **닫힘**

### 수정의 실체

수정자는 리뷰의 권장(`host: "localhost"` 한 줄)이 **이 기기에서 충분하지 않았다고 보고했고, 그 보고가 맞다.**
node 는 `host` 하나를 주소 하나로 잡는다. 대신 `vite.probe.config.ts:43-75` 에 **`loopbackMirror()` 플러그인**을
넣어, 런타임에 `httpServer.address()` 로 **잡힌 쪽을 보고 반대편 loopback 을 같은 포트로 마저 연다.**

### 직접 실측한 것 (보고서 수치를 옮기지 않았다)

fixture 를 직접 띄우고 쟀다.

```text
$ lsof -nP -iTCP:5180 -sTCP:LISTEN
node  21028  ...  IPv6  TCP [::1]:5180 (LISTEN)
node  21028  ...  IPv4  TCP 127.0.0.1:5180 (LISTEN)      ← 둘 다 산다

$ curl --cacert .dev-certs/dev-ca.pem   (검증 ON · -k 없음)
https://localhost:5180/probe.html    http=200  ssl_verify_result=0
https://[::1]:5180/probe.html        http=200  ssl_verify_result=0
https://127.0.0.1:5180/probe.html    http=200  ssl_verify_result=0

loopback 아닌 바인딩: 없음 (0.0.0.0 · :: 없음)
vite 출력: `➜  Loopback mirror: https://127.0.0.1:5180/`
```

**정적 파일만이 아니라 vite 변환 파이프라인 전체가 다리를 건넌다** — 확인용으로
`https://127.0.0.1:5180/src/dev/probeMain.tsx` 를 직접 받아 **`HTTP=200 · content-type: text/javascript` ·
sourcemap 포함 변환 결과**를 확인했다(`localhost` 경유와 동일). 즉 다리는 TCP 바이트만 넘기고
TLS·변환·모듈 그래프 어느 것도 우회하지 않는다.

**종료 정리도 샌 곳이 없다** — 프로세스를 내린 뒤 `lsof -nP -iTCP:5180 -sTCP:LISTEN` 이 **비었다**
(`server.httpServer.on("close", () => mirror.close())`, `:71`). 고아 미러가 남지 않는다.

### 경계가 넓어지지 않았다 — 확인함

- `capabilities/probe-fixture.json:7` `remote.urls` = `https://localhost:5180/*` **무변경**
- `src-tauri/src/lib.rs:37` `DEFAULT_PROBE_URL` = `https://localhost:5180/probe.html` **무변경**
- 네비게이션 허용 목록(`lib.rs:41-52`)은 **`probe_url()` 의 origin 하나**를 파생한다 → `https://localhost:5180`
- ⇒ `https://127.0.0.1:5180` 로 뜬 문서는 **origin 이 달라 커맨드 ACL 도 네비 허용 목록도 통과하지 못한다.**
  다리가 연 것은 **도달 가능성**이지 **권한**이 아니다. 이 구분이 선 것을 코드로 확인했다.
- TLS 우회 grep(`rejectUnauthorized`·`NODE_TLS_REJECT_UNAUTHORIZED`·`insecure`·`accept_invalid`·
  `dangerous`·`ignore-certificate`) — **신규·수정 파일 전부 0건.** `.gitignore` 의 `.dev-certs/` 도 그대로다.
- `0.0.0.0`·`::` 로 넓히는 코드 **없음**(주석 문자열 1건이 전부). `strictPort: true` 유지.

### 남는 조건 — **리뷰 R1 의 요구는 그대로 살아 있다**

이 수정은 「**닿지 못해서 실패**」 가능성을 없앤 것이지 **M-1 을 측정하지 않았다.**
M-1 을 「미측정」으로 닫을 때 **실패 원문(TLS 에러 코드 또는 연결 거절)을 한 줄이라도 남긴다** —
R1 의 요구가 유효하다. 수정 보고서 §2 도 같은 말을 적었다(일치 확인).

---

## 2. W-2 — `E-13` 과 `E-14a` 가 갈렸다 · **닫힘**

### 코드로 확인한 분리 (`src/dev/ProbePage.tsx`)

| 구간 | 줄 | 실패하면 | 로그 | 화면 | 점유 | 녹음 |
|---|---|---|---|---|---|---|
| ① `getUserMedia` + `MediaRecorder` + `start()` | `:220-251` | `E-13` | `M-4 마이크 열기 실패(E-13) — 점유를 걸지 않았다`(`:249`) | 붉은 줄 「마이크 실패(E-13)」(`:326-330`) | **안 건다** → `:250` 에서 `return` | 시작 안 됨 |
| ② `guard.acquire` | `:256-270` | `E-14a` | `M-9 wake_guard_acquire 실패(E-14a) — 마이크는 열려 있고 녹음은 계속한다`(`:268`) | 주황 줄 「점유 문제 — 마이크는 열려 있고 녹음은 계속된다」(`:331-335`) | 실패 | **계속한다** |

- **`return` 이 실제로 있다** (`:250`) — ① 이 실패하면 `acquire` 를 **아예 부르지 않는다**(L-03).
- **`running.current` 가 ①과 ② 사이**(`:254`)에 선다 — ② 가 실패해도 `stop()` 이 정상으로 `release` 를 부른다.
- `MediaRecorder` 생성자가 던지는 경로에서 **트랙을 닫는다**(`:232`) — 마이크를 켜진 채 두지 않는다.
- **`degraded` 는 실패가 아니라 상태**로 따로 찍힌다(`:262-263`) — `E-14a` catch 와 다른 자리다.
- 두 오류 상태가 **별개 `useState`** 다(`micError` `:193` · `guardIssue` `:195`). 한 슬롯을 공유하지 않는다.

### 회귀 시험 6건이 «실제로» 그 자리를 보는가 — 확인함

`src/dev/ProbePage.test.tsx`(신규 166줄). `RecordingPanel` 을 `export` 해 props 로 직접 시험하고,
`getUserMedia`·`MediaRecorder` 는 jsdom 스텁을 꽂는다. 이 저장소의 기존 방식(`fireEvent`·수동 `cleanup`)을 따른다.

시험 1·2 의 단언이 **비어 있지 않다**는 것을 코드 대조로 확인했다 — 옛 구조(점유 실패를 `M-4`/`E-13` 으로
찍는 판)에서는

- `expect(log.has("E-14a")).toBe(true)` 의 `waitFor` 가 **영영 서지 않고**,
- `expect(log.has("E-13")).toBe(false)` · `expect(...tag === "M-4").toBe(false)` 가 **뒤집히며**,
- `screen.getByText(/점유 문제/)` 가 **없고** `queryByText(/마이크 실패\(E-13\)/)` 가 **잡힌다.**

즉 **두 시험이 정확히 W-2 의 자리에서 붉어진다.** 수정 보고서 §3 의 mutation 결과
(`2 failed | 4 passed`)와 **논리적으로 일치한다.** 나머지 4건(degraded / `getUserMedia` 거부 /
`MediaRecorder` 던짐 / `guard` 없음)은 그 판에서도 통과한다 — 보고서의 숫자와 맞는다.

> **주의(방법론)**: 나는 「코드를 고치지 말라」는 지시에 따라 **mutation 을 직접 돌리지 않았다.**
> 위는 단언문과 구현의 대조에 근거한 판정이다. 수정자의 mutation 기록은 그 대조와 어긋나지 않는다.

### 직접 돌린 검증

| # | 명령 | 결과 |
|---|---|---|
| V-1 | `npx tsc --noEmit` | **exit 0 · 출력 0줄** |
| V-2 | `npx vitest run src/dev/` | **3 files · 23 tests 전건 통과** (17 + 신규 6) |
| V-3 | `npx vitest run src/dev/ProbePage.test.tsx src/features/meetings/MeetingLive.test.tsx src/features/browser/liveTranscription.test.ts` | **94 passed** — `navigator.mediaDevices` 스텁의 **파일 간 간섭 없음** |

V-3 을 따로 돌린 이유: 신규 시험이 `Object.defineProperty(navigator, "mediaDevices", …)`(`:47-50`)를
쓰는데 `afterEach` 가 그것을 **되돌리지 않는다**(`vi.unstubAllGlobals()` 는 `stubGlobal` 만 되돌린다).
vitest 기본 `isolate: true` + 파일별 jsdom 이라 새지 않는 것을 **같은 실행에 제품의 마이크 시험을
끼워 넣어 실측으로** 확인했다. (→ 부채로만 §5 N-2 에 적는다)

---

## 3. allowed_paths — **이탈 0**

브리프 §4 가 연 자리: `frontend/src-tauri/**` · `frontend/src/dev/**` · `frontend/package.json`+lockfile ·
frontend 전용 fixture 설정·엔트리·실행 스크립트·관련 ignore.

`git add -An --dry-run frontend/` 로 직접 센 **30개** 전부가 그 안이다.

- 이번에 바뀐 3개: `vite.probe.config.ts`(fixture 설정 ✓) · `src/dev/ProbePage.tsx`(✓) ·
  **`src/dev/ProbePage.test.tsx`(신규 · `src/dev/**` ✓)**
- R1 시점 29 → **30** (신규 시험 1개). 증가분이 그 하나뿐인 것을 목록 대조로 확인했다.
- `frontend/src/features/**` · `src/lib/api.ts` · `src/App.tsx` · `vite.config.ts` · `tsconfig*.json` ·
  `backend/**` · `docs/**` — **`git diff --stat` 0줄 · 목록에 없음.**
- 문서(SPEC/WP/index/log) 무변경 · 커밋·push·PR 없음(HEAD 그대로).

---

## 4. 제품 빌드 경계 — **유출 0 · 4중 확인 유지**

| 축 | 결과 | 근거 |
|---|---|---|
| **설정 분리** | 유지 | `vite.config.ts` **무변경**(`git diff --stat` 0줄) · `rollupOptions` 없음 → 기본 입력 `index.html`. `vite.probe.config.ts` 는 `--config`(`package.json:11`)로만 쓰인다 |
| **엔트리 분리** | 유지 | `index.html:15` → `/src/main.tsx` · `probe.html:15` → `/src/dev/probeMain.tsx` |
| **참조 0** | 유지 | `grep -rn --include='*.ts(x)' 'src/dev|probeShell|probeRecording|ProbePage|@tauri-apps|probeMain' src/` → `src/dev/` **밖 매치 0** |
| **산출물 0** | **재확인(직접 빌드)** | `npm run build` **exit 0** · `dist/` 에 `탐침\|probe-root\|probeMain\|ProbePage\|__TAURI_INTERNALS__\|wake_guard\|@tauri-apps\|loopbackMirror\|Loopback mirror\|scax-probe` **0건** · `dist/*.html` 은 **`index.html` 하나**(`dist/probe.html` 없음) |
| **새 의존의 유출** | 없음 | 미러가 쓰는 `node:net`(`vite.probe.config.ts:13`)은 **fixture 설정 파일에만** 있다. 제품 번들 grep 0건(위) |
| **vitest 영향** | 없음 | vitest 는 `vite.config.ts:17-19` 를 읽는다 — `vite.probe.config.ts` 를 보지 않는다. 미러가 시험 중에 뜨지 않는다 |

**Rust 무변경 확인**: 이번 수정 파일 3개에 `src-tauri/**` 가 없다 → `cargo check`/`cargo test` 재실행 불필요.
(R1 의 `cargo test 21 passed` 가 그대로 유효하다.)

---

## 5. 남은 WARN

### R1 의 W-3 ~ W-8 — **6건 전부 그대로 열려 있다** (지시대로 손대지 않았다 · 확인함)

| # | 자리 | 상태 확인 |
|---|---|---|
| W-3 | Windows 컴파일·실행 둘 다 미검증 | Rust 무변경 · `llvm-rc` 여전히 없음 → **그대로** |
| W-4 | macOS 재무장이 캐시된 assertion 앞에서 no-op | `power.rs:243` `if self.id.is_some()` **존재** |
| W-5 | Windows engage 실패 뒤 `disengage` 가 OS 요구를 안 지움 | `power.rs:313` `if !self.engaged` **존재** |
| W-6 | capability 가 `local` 미명시 → 기본값 `true` | `probe-fixture.json` 에 `"local"` 키 **0개** |
| W-7 | `Destroyed` 정리가 label 을 `"main"` 하드코딩 | `lib.rs:380` **존재** |
| W-8 | `@tauri-apps/api` 가 제품 `dependencies` | `dependencies: true · devDependencies: false` |

**W-4 가 여섯 중 유일하게 점유 «계약» 에 닿는다** — Phase 3 이 반드시 본다. 나머지 다섯은 품질·경계 선긋기다.

### 새로 적는 것 — **N-1 · N-2** (둘 다 Phase 2 를 막지 않는다)

#### N-1 · `stop()` 의 **해제 실패(`E-14b`)가 아무 데도 남지 않는다** — W-2 와 같은 계열의 빈칸

- `ProbePage.tsx:286` — `const result = await guard?.release(active.session);` 가 **try 로 감싸여 있지 않다.**
  호출부는 `:323` 의 `onClick={() => void stop()}` 이라, `release` 가 던지면
  **① 로그 0줄 ② 화면 0줄 ③ unhandled rejection** 으로 끝난다.
- **같은 파일의 M-9 수동 패널은 이것을 제대로 한다** — `:150-151` 이 해제 실패를 **`E-14b`** 로 찍으며
  「해제 실패를 「녹음 계속」으로 뭉개지 않는다」고 주석까지 달았다. **한 파일 안에 기준이 둘이다.**
- 게다가 `:277` 에서 `running.current = null` 이 **먼저** 서므로, 「녹음 종료」를 다시 눌러도
  `:276` 에서 곧장 빠진다 — **재시도 수단도 없다.** 셸에는 점유가 남고 계측 기록에는 흔적이 없다.
- **이것은 이번 수정의 회귀가 아니다** — R1 이 본 판에도 같은 구조였다(R1 은 이 칸을 「장치 해제」
  관점에서만 PASS 로 봤고 해제 실패 경로를 따로 보지 않았다). **W-2 가 열어 준 눈으로 보면 같은 결함이다.**
- **왜 Phase 2 를 막지 않는가**: `release` 가 실패하려면 IPC 자체가 깨져야 하는데, 그 상태면
  `acquire` 도 같이 깨져 **N-1 보다 먼저 `E-14a` 가 찍힌다.** 「조용히 통과」가 아니라 「이미 붉은 상태의 뒷줄」이다.
- **권장 최소 수정**: `:286` 을 try 로 감싸고 실패를 `E-14b` 로 찍는다(`:151` 과 같은 문구 체계).
  **Phase 2 착수 전이면 5줄, 아니면 Phase 3 흡수 목록.**

#### N-2 · `loopbackMirror` 에 시험이 **하나도 없고**, 이 기기가 도는 분기는 **둘 중 하나뿐**이다

- W-1 의 병 자체가 **「어느 스택이 잡히는지는 기기마다 다르다」** 였는데, 고친 코드의
  **분기(`boundV6` · `vite.probe.config.ts:51`)를 검증한 것은 이 기기의 IPv6 경로 하나뿐**이다.
  IPv4 가 먼저 잡히는 기기에서 도는 `mirrorHost = "::1"` 경로는 **한 번도 실행되지 않았다.**
  (코드를 읽은 한 로그 문자열의 대괄호 처리까지 양쪽 다 맞다 — `:69`. 다만 그것은 읽기이지 실행이 아니다.)
- 부차적으로, 신규 시험의 `navigator.mediaDevices` defineProperty 가 `afterEach` 에서 **되돌려지지 않는다**
  (`ProbePage.test.tsx:47-50` vs `:53-59`). vitest 기본 격리 덕에 새지 않는 것을 **V-3 으로 실측 확인**했지만,
  저장소가 `isolate: false` 나 공유 환경으로 바꾸면 **제품 마이크 시험에 스텁이 샌다.**
- **권장**: 미러는 Phase 3 이 제품 셸로 흡수할 때 **그대로 계승하지 말 것**(`SCAX_PROBE_*` 손잡이와 같은 칸).
  시험 쪽은 `afterEach` 에 원래 서술자 복원 한 줄이면 닫힌다. **둘 다 Phase 2 전 필수가 아니다.**

---

## 6. 기존 부채 — R1 것 유지 + 한 건 특정됨

- **`CreateWork.test.tsx` flake 특정됨.** R1 이 「이름 미특정」으로 남긴 flake 를 수정자가 잡았다
  (`생성 창의 갈래 — 업무는 내 업무다 › 실패한 제출을 …` · 「업무 추가」 버튼 못 찾음).
  **이번 변경과 무관하다는 근거가 성립한다** — 해당 파일 0줄 변경 · 제품 시험이 `src/dev` 를 import 하지 않음
  (§4 참조 grep 0) · vitest 가 `vite.probe.config.ts` 를 읽지 않음(§4). **전체 스위트 동시 실행 때만 나는
  제품 쪽 flake**로 코디 추적 대상이다. 나는 초점 밖이라 전체 스위트를 돌리지 않았다.
- R1 의 나머지 부채 유지: drift 시험 정규식의 따옴표 결합(`probeRecording.test.ts:28`) ·
  `SCAX_PROBE_URL`/`SCAX_PROBE_NAV_ALLOW` 손잡이의 Phase 3 제거.
- **부수 관찰(부채 축에도 못 미치는 것)**: `guardIssue` 는 `stop()` 에서 지워지지 않아
  녹음을 끝낸 뒤에도 주황 줄이 남는다(다음 `start()` 의 `:212` 가 지운다). 기록을 거짓으로 만들지 않고
  「직전 회차에 점유 문제가 있었다」는 사실 자체는 참이다 — **고칠 필요 없다. 읽을 때만 알아 두면 된다.**

---

## 7. Phase 2 진행 여부 — **진행 가능**

**게이트를 열 사유가 없다.** WORK §Phase 1 「실패 시 다음 조치」의 중단 판정은
「커맨드 왕복이 **안 된다**」는 **관측**을 전제하는데, 그 관측은 여전히 존재하지 않는다(M-1 미측정).
그리고 R1 이 「측정을 기록하기 전에 고치라」고 지목한 두 자리가 **둘 다 닫혔다** —
이제 Phase 2 의 기록이 ① fixture 에 닿지 못해 생긴 실패를 커맨드 실패로 적을 위험과
② IPC 실패를 마이크 실패로 적을 위험을 **구조적으로 지고 있지 않다.**

### Phase 2 착수 시 코디가 들고 가야 할 것

1. **M-1 을 「미측정」으로 닫을 때 실패 원문을 한 줄 남긴다** — R1 의 요구가 **그대로 유효하다.**
   이번 수정은 원인 후보 하나(도달 실패)를 지웠을 뿐, 원문을 대신 만들어 주지 않는다.
   CA 신뢰 설치는 여전히 **사용자 조작**이다.
2. **상태표 정정 2건**(R1 §코디 제안 2와 동일 — 아직 안 됨): Windows 를 「**컴파일 미검증 · 실행 미검증**」
   두 칸으로 · M-1 실패 사유를 「**원인 미확정**」으로.
3. **선택 · 5줄**: Phase 2 가 해제 경로까지 기록으로 쓸 생각이면 **N-1** 을 먼저 닫는다.
   쓰지 않을 거면 Phase 3 으로 넘긴다.
4. **Phase 3 흡수 목록(누적)**: `Op::Shutdown` · **W-4**(macOS 재무장 — 유일한 계약 항목) · W-5 · W-6 ·
   W-7 · W-8 · **N-1** · **N-2**(미러 비계승) · `SCAX_PROBE_*` 손잡이 제거 · AC-T41 보상 수단 결정.
