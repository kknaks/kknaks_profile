# WORK-006 Phase 4 수정 재검수 (R2)

- **검수 대상**: `tauri-p4-web-wiring-fix-report.md` ↔ 실제 diff (선행 검수 `review-tauri-p4-web-wiring-report.md` 의 W-1·W-3·W-4·W-6)
- **코드**: `/Users/kknaks/orca/workspaces/Strong_hajin/strong-hajin-projects` · HEAD `a1f6791`(변동 없음)
- **방식**: 변경 5파일 전수 읽기 + 보고된 검증 **전부 재실행**
- **코드 수정·커밋·배포 없음**

---

## 0. 종합 판정 — **PASS · FAIL 0 · WARN 5**

**지적한 WARN 네 건이 모두 닫혔다.** W-1 은 「서버 `captureId` 계약을 건드리지 않고 점유 키만
분리」라는 **올바른 방향**으로 고쳤고, W-3 은 React state 밖(모듈 기록 + `console.warn`)에
사실을 남겨 언마운트 경로를 덮었으며, W-4 는 `mounted` + 회차 키 이중 가드로 회의 경로와
규칙을 맞췄다. W-6 은 `"opened" | "absent" | "failed"` 3분기로 실패를 성공으로 뭉개지 않는다.

보고된 증거(`tsc` · `shell.test` 13 · 전체 1053 3연속)를 **모두 재현**했다.

새로 든 WARN 다섯 중 하나(R-1, StrictMode)는 **이번 수정이 새로 들인 것**이라 다음 회차에서
한 줄로 닫는 편이 좋다. 나머지는 잔여·표현 문제다.

---

## 1. 판정표

| # | 항목 | 판정 |
|---|---|---|
| W-1 | 브라우저 점유 키가 회차마다 새로 생성 · 서버 `captureId` 계약 보존 | **PASS** |
| W-3 | 언마운트 release 실패가 state 밖에 기록 | **PASS** |
| W-4 | `mounted` / 회차 가드 | **PASS** (단 R-1) |
| W-6 | `open_external` 실패를 성공으로 뭉개지 않음 | **PASS** (단 R-3) |
| §6 | 동시 dynamic import 직렬화 결함 수정 | **PASS**(고침 타당·테스트로 고정) · 원인 서술은 **WARN**(R-2) |
| — | 허용 파일 범위 | **PASS** |
| — | `api.ts`·`microphone.ts`·`src-tauri/**` 무변경 | **PASS** (0줄) |
| — | `tsc` · `shell.test` 13 · 전체 1053 ×3 | **PASS** (전부 재현) |
| — | 화면 배선 회귀 테스트 | **WARN**(R-5, 기록만) |

---

## 2. FAIL

**없다.**

---

## 3. W-1 · W-3 · W-4 · W-6 — 닫힘 확인

### W-1 (PASS) — 키를 «분리»한 것이 옳다
- `wakeSession = useRef<string|null>(null)` 을 새로 두고 `holdWake()` 가 **마이크가 열릴 때마다**
  `newWakeSession()` 을 뽑는다 → 회의 경로(`stream.ts`)와 **같은 규칙**이 됐다.
- **`captureId` 는 그대로 두었다.** 이 값은 `startBrowserRecording`·`stopBrowserRecording` 의
  인자로 **서버가 녹음 회차를 짚는 값**이라, 회차마다 갈았으면 기존 브라우저 동작·API 계약이
  바뀌었을 것이다. **브리프가 준 두 선택지 중 안전한 쪽을 골랐고, 근거도 정확하다.**
- `start()` 실패 후 재시작 시 **다른 점유 키**가 쓰이므로 1회차의 늦은 해제가 2회차를 풀 수 없다.

### W-3 (PASS) — 사실이 화면 수명보다 오래 남는다
- `releaseWakeGuard` 의 `catch` 가 **호출 지점과 무관하게** `recordCleanupFailure()` 한다:
  모듈 `Set` + `console.warn`, **같은 세션은 한 번만**.
- `stream.ts` 의 `setState` 는 여전히 `!stopped` 가드 뒤에 있지만, **그것이 맞다** — 사실은
  이미 `shell.ts` 가 남겼고 화면은 살아 있을 때만 한 줄을 더한다. 녹음을 다시 켜지 않는다.
- `wakeGuardCleanupFailures()` 로 진단·시험이 읽을 수 있다. 시험 3건이 이를 고정한다.

### W-4 (PASS) — 두 경로의 규칙이 같아졌다
- `mounted` ref 도입, `holdWake` 는 **`mounted` 와 «내 키가 아직 최신인가»를 함께** 본다.
- `dropWake` 는 **키를 먼저 비우고** 해제해 두 번 도는 정리에서도 멱등이다.
- `start()` 의 `catch` 경로 검증: `holdWake()` 가 `wakeSession.current` 를 **동기적으로** 세운 뒤
  `await` 하므로, 뒤따르는 `await dropWake()` 가 키를 확실히 본다 → 해제 누락 없음. ✅

### W-6 (PASS) — 실패가 더 이상 성공이 아니다
- 반환이 `boolean` → `"opened" | "absent" | "failed"` 로 바뀌고, `App.tsx` 는 **`absent` 일 때만**
  `window.open` 폴백을 한다.
- 실패에 웹 폴백을 붙이지 않은 판단도 **타당하다** — 셸 안의 `window.open` 은 앱 창에 두 번째
  웹뷰가 앉는 길이고 그것이 U-4 가 막으려는 사고다.

---

## 4. WARN (신규 5건)

| # | 내용 | 근거 |
|---|---|---|
| **R-1** | **StrictMode 에서 `mounted` 가 되살아나지 않는다 — 이번 수정이 새로 들인 결함.** `main.tsx` 가 `<StrictMode>` 를 쓰는데, React 18 dev 는 같은 인스턴스에서 effect 를 mount→unmount→mount 로 두 번 돌린다. `useEffect(() => () => { mounted.current = false; }, [])` 는 **본문에서 `true` 로 되돌리지 않아** 모의 언마운트 이후 `mounted.current` 가 **영구히 `false`** 가 된다 → **개발 빌드에서 U-3·정리 실패 한 줄이 아예 뜨지 않는다.** 운영 빌드는 정상이고 녹음도 깨지지 않지만, **개발 중 U-3 을 눈으로 확인할 수 없다.** 한 줄(`useEffect(() => { mounted.current = true; return () => { mounted.current = false; }; }, [])`)로 닫힌다. 회의 경로는 `stopped` 가 effect 지역 변수라 이 문제가 없다 | `BrowserRecordingPage.tsx` `mounted` 정의부 · `src/main.tsx:7` |
| **R-2** | **§6 의 「실제 결함」 서술이 증거를 넘어선다.** 관측은 `vi.mock` + `vi.resetModules()` 를 쓰는 **jsdom/vitest 모듈 러너**에서 나왔다. 실제 번들러·브라우저에서 같은 specifier 의 동시 `import()` 는 **같은 약속을 돌려주고 두 번째가 실패하지 않는다.** 따라서 「사용자에게 이유 없는 U-3 이 보인다」는 §6 의 단정은 **확인되지 않았다.** 보고서 §9-3 이 이 한계를 스스로 적었으나 §1·§6 은 여전히 「실제 결함」으로 쓴다 → **고침 자체는 유지 권고**(약속 공유는 어느 환경에서도 옳고, 실패 시 캐시를 비워 영구 사망도 막는다). 다만 **시험이 없었으면 못 찾을 «제품» 버그**로 기록하지는 말 것 | `shell.test.ts:11-12,25-28` · `shell.ts:82-92` |
| **R-3** | **`open_external` 실패는 여전히 «사용자에게» 무반응이다.** 늘어난 것은 반환값과 `console.warn` 뿐이고 화면에는 아무것도 뜨지 않는다. 브리프가 「반환/표시」라 했으므로 **위반은 아니지만**, 링크를 누른 사람 입장에서 조용한 실패는 그대로다 | `shell.ts` `openExternal` catch · `App.tsx` `outcome === "absent"` 분기 |
| **R-4** | `cleanupFailures` **Set 을 비우는 수단이 없다.** 운영에서는 실패한 세션 수만큼만 자라 실해는 없으나, 시험은 `vi.resetModules()` 에 의존해 격리한다. 진단용 `clear` 가 있으면 더 낫다 | `shell.ts:48-53` |
| **R-5** | **화면 배선 회귀 테스트는 여전히 0건**(과제 지시대로 WARN 기록). `shell.test.ts` 13건은 **`shell.ts` 모듈 계약**만 재고, 「마이크가 열린 뒤에만 acquire」·「구독/거부에서 미획득」·「W-1 회차 키 교체」·「W-4 가드」는 **코드 검토로만** 확인됐다. 보고서 §9-1 이 같은 사실을 올렸다 | `grep -rl "wakeGuard\|lib/shell" src --include=*.test.*` → `shell.test.ts` 만 |

---

## 5. 재현한 검증

| # | 명령 | 재현 결과 |
|---|---|---|
| V-1 | `npx tsc --noEmit` | **exit 0 · 출력 0줄** |
| V-2 | `npx vitest run src/lib/shell.test.ts` | **13 passed (13)** — 보고서와 일치 |
| V-3 | `make frontend-test` × 3 | **exit 0 · 1053 passed (1053)** × **3연속** |
| V-4 | `git status` · `find -newermt "21:00"` | 이번 회차 변경 **5파일**(`shell.ts`·`shell.test.ts`·`BrowserRecordingPage.tsx`·`stream.ts`·`App.tsx`) — **전부 허용 범위 안** |
| V-5 | `api.ts`·`microphone.ts`·`src-tauri/**` | **0줄** (git 무변경 · `find` 0건) |
| V-6 | 6파일 `http(s)://` 리터럴 | **0건** — 운영 URL 미추가 |

- **13건 구성 확인**: 셸 부재 1 · 획득 3 · 직렬화 3 · 해제 실패 3 · 세션 키 1 · 외부 링크 2 = **13**.
- **1040 → 1053** 증가분이 `shell.test.ts` 13건과 정확히 일치한다.
- 「다른 키는 서로를 기다리지 않는다」 시험은 §6 의 동시 import 결함을 **간접적으로 고정한다**
  (옛 구현이었다면 두 번째 invoke 가 나가지 않아 `vi.waitFor` 가 시간 초과로 붉어진다).
- `labels.ts`·`MeetingDetailPage.tsx` 무변경 — 보고서 §2 의 기술과 일치한다.
- 선행 회차가 보고한 스위트 flake 는 이번 **3회 실행에서도 재현되지 않았다**(선행 검수 2회 포함 5회 연속 통과). 사라졌다고 단정하지 않되, 현재로선 관측되지 않는다.

---

## 6. 보고서 자체의 정확성

- **닫힘 주장 네 건은 모두 코드로 확인된다.** 수치(5파일 · 13 · 1053 ×3)도 전부 재현됐다.
- **정확한 판단**: `captureId` 를 건드리지 않은 이유(서버 계약), 실패에 웹 폴백을 붙이지 않은
  이유(두 번째 웹뷰), 해제 실패를 화면이 아니라 모듈에 적은 이유(언마운트) — 셋 다 근거가 옳다.
- **과장 1건**: §1·§6 의 「실제 결함」(R-2). §9-3 의 유보와 §1 의 단정이 서로 어긋난다.
- **누락 1건**: R-1(StrictMode `mounted`). 이번 수정이 새로 들인 자리다.

---

## 7. 코디에게 올리는 결정거리

1. **R-1 한 줄 수정** — `mounted.current = true` 를 effect 본문에 넣는다. 가장 싸고 확실하다.
2. **R-2 문구 정정** — §6 을 「시험 환경에서 관측된 경합, 고침은 어느 쪽이든 옳음」으로 낮춘다.
3. **R-5** — 화면 배선 회귀 시험을 다음 Phase 에 열 것인지. 지금은 W-1·W-4 가 **코드 검토 증거뿐**이다.
4. **R-3** — 외부 링크 실패를 사용자에게 알릴지(토스트 한 줄 등) SPEC 판단.
5. **R-4** — `cleanupFailures` 진단 `clear` 추가 여부(작음).
