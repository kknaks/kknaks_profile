# WORK-006 Phase 4 웹 배선 — 독립 검수

- **검수 대상**: `tauri-p4-web-wiring-report.md` ↔ 실제 diff
- **코드**: `/Users/kknaks/orca/workspaces/Strong_hajin/strong-hajin-projects` · HEAD `a1f6791`(변동 없음)
- **방식**: 6파일 전수 읽기 + 보고된 검증 **재실행**
- **코드 수정·커밋·배포 없음**

---

## 0. 종합 판정 — **PASS (조건부) · FAIL 0 · WARN 8**

발주 계약 1~5 의 **핵심은 모두 지켜졌다.** 허용 6파일 외 변경 0, `api.ts`·`microphone.ts`·
`src-tauri/**` 무변경, 운영 origin 하드코딩 0, 마이크가 «실제로» 열린 뒤 acquire·«실제로»
끝난 뒤 release, 셸 없는 브라우저 동작 보존. 보고된 증거(`tsc` · 1040)를 **재현**했다.

막는 결함(FAIL)은 없다. 다만 **배선을 검증하는 테스트가 0건**이고(1040건은 셸 없는 경로만 지난다)
브라우저 녹음 경로의 세션 키가 «회차»가 아니라 «마운트» 단위라, 두 가지는 다음 Phase 에서 닫아야 한다.

---

## 1. 판정표

| # | 검수 범위 | 판정 |
|---|---|---|
| 1 | 허용 6파일만 변경 | **PASS** |
| 2 | `shell.ts` 가 Tauri 없는 브라우저를 보존 | **PASS** |
| 3 | 마이크 실제 open 이후 acquire · 완료 후 release | **PASS** |
| 4 | 회차별 세션 키 / 중복 방지 | 회의 **PASS** · 브라우저 **WARN**(W-1) |
| 5 | `degraded`·`E-14a`/`E-14b` 가 녹음을 실패시키지 않음 | **PASS** (노출은 W-3) |
| 6 | 두 녹음 경로 · App 전환/닫기 취소 경계 | **PASS** |
| 7 | `api.ts`·`microphone.ts`·`src-tauri/**` 변경 | **PASS** (0줄) |
| 8 | 운영 origin 발명 | **PASS** (URL 리터럴 0) |
| 9 | `tsc` · 1040 증거 재현 | **PASS**(재현됨) · 증거 범위는 **WARN**(W-2) |

---

## 2. FAIL

**없다.**

---

## 3. WARN

| # | 내용 | 근거 |
|---|---|---|
| **W-1** | **브라우저 경로의 세션 키가 «회차»가 아니라 «마운트» 단위다.** `captureId = useState(() => crypto.randomUUID())` 는 마운트당 하나인데, `start()` 가 `startBrowserRecording` 에서 던지면 `onChange` 가 불리지 않아 **`item.status` 가 `waiting` 으로 남고 시작 버튼이 다시 눌린다** → 2회차가 **같은 키**로 acquire 한다. 발주 계약 2 「세션 키는 회차마다 새로 생성」의 문자 그대로는 위배다. 네이티브 장부가 이름 집합이라 중복 점유는 생기지 않아 **실해는 작지만**, 1회차의 늦은 해제가 2회차를 풀 수 있는 `E-08` 보호가 그만큼 얇아진다 | `BrowserRecordingPage.tsx:15,33,42,91` · 렌더 `item.status === 'waiting'` 분기 |
| **W-2** | **배선 회귀 테스트 0건.** `wakeGuard`·`lib/shell`·`__TAURI_INTERNALS__` 를 참조하는 테스트는 저장소에 **하나도 없다**(유일 히트 `src/dev/probeShell.test.ts` 는 Phase 1 탐침 것으로 무관). jsdom 에는 셸 전역이 없어 **새 코드는 전부 `absent` 분기로만 지난다** → 1040 통과가 증명하는 것은 「셸 없는 브라우저 무회귀」**까지**이고, acquire/release 타이밍·`degraded`·`E-14b` 는 **한 줄도 검증되지 않았다.** 보고서 §9-1 이 이를 정직하게 올렸고 원인(발주가 6파일로 한정)도 타당하다 → **다음 Phase 에 테스트 파일 1개 허용 권고** | `grep -rl wakeGuard src --include=*.test.*` |
| **W-3** | **가장 흔한 해제 경로에서 `E-14b` 가 보이지 않는다.** `stream.ts` 의 `releaseWake()` 는 `if (!stopped && outcome.kind === "failed")` 로 `setState` 하는데, L-10(언마운트 정리)에서는 `stopped = true` 가 **먼저** 서므로 정리 실패가 **절대 화면에 뜨지 않는다.** 언마운트 후 setState 를 피하려는 올바른 가드이지만, 결과적으로 「사실을 드러낸다」는 계약 4 가 `onClosed` 경로에서만 선다 | `stream.ts` cleanup: `stopped = true` → `releaseWake()` |
| **W-4** | **두 경로의 가드 엄밀도가 다르다.** `stream.ts` 는 `stopped` · `wakeSession !== session` 을 둘 다 보는데, `BrowserRecordingPage` 의 `holdWake`/`dropWake` 는 **언마운트·회차 가드가 없다** — 언마운트 뒤 `setWakeGuard` 가 늦게 돌 수 있다(React 18 에서 무해하지만 규칙이 갈린다) | `BrowserRecordingPage.tsx:31-45` |
| **W-5** | **`openExternal`(U-4) 배선은 발주 계약 밖이다.** 계약 1 이 든 커맨드는 `shell_info`·`wake_guard_acquire`·`wake_guard_release` **셋**이고 `open_external` 은 없다. `App.tsx` 는 허용 파일이라 «금지» 위반은 아니나 **요구되지 않은 기능이 들어왔다** — 채택/되돌림은 코디 판단 | `App.tsx:685-690` · `shell.ts:134-143` |
| **W-6** | `openExternal` 이 **실패해도 `true`** 를 돌려준다 → App 이 웹 폴백(`window.open`)도 하지 않아 **링크가 조용히 아무 일도 안 한다.** 주석은 이를 `E-14c` 계약이라 적었으나, 발주에 근거가 없어 검수로는 확인 불가 | `shell.ts:139-142` |
| **W-7** | 발주의 허용 목록은 `features/**meetings**/BrowserRecordingPage.tsx` 라 적혀 있으나 실파일은 `features/**browser**/…` 다. 구현은 실경로를 고쳤고 이는 **발주서 오타**로 보인다(위반 아님). 또 브라우저 화면이 `meetingScreen` 라벨을 재사용해 네임스페이스 경계가 흐리다 | 발주 §허용 · `BrowserRecordingPage.tsx:5` |
| **W-8** | 보고서 §8 의 「스위트 전반 시간 의존 불안정」은 **이번 검수에서 재현되지 않았다**(2회 연속 1040/1040). 불안정 주장을 반증하진 못하나 **현재 기기 상태로는 관측되지 않는다** — 추적 여부는 코디 판단 | 아래 재현표 |

---

## 4. PASS — 직접 확인한 것

- **허용 6파일뿐**: 수정 5(`App.tsx`·`BrowserRecordingPage.tsx`·`MeetingDetailPage.tsx`·`stream.ts`·`labels.ts`) + 신규 1(`lib/shell.ts`). `package.json`·`package-lock.json` 은 **Phase 1 잔여**(mtime 19:02, Phase 4 창은 20:45 이후) — 이번 Phase 변경 아님.
- **`api.ts`·`microphone.ts`·`src-tauri/**` 0줄**: `git status` 무변경 + `find -newermt "20:40"` 에 `src-tauri` 파일 0건.
- **브라우저 보존**: 모든 export 가 `hasShell()` 로 먼저 막히고, `@tauri-apps/api/core` 는 **동적 import** 라 셸 없으면 모듈조차 안 불린다. 1040건 통과가 이를 뒷받침.
- **acquire 시점**: 회의 = `startMicrophone(...).then(handle => …)` 에서 **핸들을 받은 그 줄**(연결·`onReady` 아님). 브라우저 = `startBufferedAudioCapture()` **성공 직후**. 둘 다 앞선 `await` 가 던지면 도달하지 않아 **권한 거부·미지원에서 걸지 않는다**(L-03).
- **미획득 자리**: 구독 역할은 `effectiveRole !== "upstream"` early return 으로 마이크 경로에 닿지 않음(L-04). `stopped` 인 늦은 핸들은 **닫기만 하고 걸지 않는다**.
- **release 시점**: `onClosed`(L-02, `taken` 포함 L-05) · effect cleanup(L-10) · 브라우저는 stop 성공·interrupt·폴링 종료·언마운트. **닫기 취소·화면 전환·막힌 이동에는 해제 경로가 없다**(계약 5).
- **업로드 실패 시 점유 유지**, 서버가 `completed` 면 해제 — 재시도 가능성과 일치.
- **회의 경로 세션 키**: `newWakeSession()` = `crypto.randomUUID()`, **회차마다** 생성, 회의 id 미사용.
- **실패가 녹음을 깨지 않음**: `acquireWakeGuard` 는 **던지지 않고** `E-14a` 를 `degraded` 로 변환. `E-14b` 는 별도 문구이고 **녹음을 다시 켜지 않는다**. `absent`·`on` 은 화면에 아무것도 내지 않는다.
- **타이머 없음**: L-14 재확인은 `visibilitychange` **사건**에서만, 정리 때 리스너 제거. TTL·주기 갱신·참조계수 0.
- **직렬화**: `shell.ts` 의 `chains` 가 세션별로 호출을 한 줄로 세워 해제가 획득 뒤에 간다. 앞 호출 실패에도 줄이 이어지고(`then(job, job)`) 정산 후 Map 에서 지워 누수도 없다.
- **운영 origin 미발명**: 6파일에 `http(s)://` 리터럴 **0건**.
- **App 계약 보존**: `if (browserInteractionId) return <BrowserInteractionPage …>` early return 그대로. diff 는 자료 링크 분기 한 곳만 건드렸다.

### 재현한 검증

| # | 명령 | 재현 결과 |
|---|---|---|
| V-1 | `npx tsc --noEmit` | **exit 0 · 출력 0줄** |
| V-2 | `make frontend-test` × 2 | **exit 0 · 1040 passed (1040)** × 2 |
| V-3 | `git status` · `find -newermt` | 허용 6파일 외 변경 **0** · `src-tauri` **0** |

---

## 5. 보고서 자체의 정확성

- **과장 없음.** 「배선 테스트를 못 만들었다」(§9-1), 「실제 셸에서 도는 것은 미확인」(§9-2),
  「U-3 문구 둘 해석을 재확인해 달라」(§6)를 **스스로 올렸다.** 수치(6파일 · 1040)도 재현됐다.
- **§6 문구 둘 해석에 대한 검수 의견**: SPEC 근거(정리 실패에는 다른 문구)가 타당하고,
  두 문구가 **동시에 렌더되지 않음**을 코드로 확인했다 → **수용 권고.**
- **정정할 것 1건**: §5 표가 「`start()` 의 `catch` → 해제」를 적으면서 세션 키를 「창이 뜰 때마다
  새 값」이라 했는데, 바로 그 `catch` 경로가 **같은 키로 2회차를 여는 통로**다(W-1).

---

## 6. 코디에게 올리는 결정거리

1. **다음 Phase 에 테스트 파일 1개 허용** — W-2 가 지금 가장 큰 구멍이다. 보고서가 제안한 5개 항목이 적절하다.
2. **W-1** — 브라우저 경로도 `newWakeSession()` 을 쓰거나, 최소한 `start()` 실패 뒤 키를 새로 뽑게 한다. (작은 수정)
3. **W-5 · W-6** — `open_external`/U-4 배선을 이번 범위로 인정할지, 되돌릴지.
4. **W-3** — 언마운트 해제 실패를 어디서 드러낼지(다음 화면? 로그?) SPEC 판단 필요.
5. **W-8** — 스위트 flake 추적 여부.
