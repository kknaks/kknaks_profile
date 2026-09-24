# WORK-006 Phase 4 수정2 보고 — R-1 · R-2

- **발주**: `tauri-p4-web-wiring-fix2-brief.md` (검수 `review-tauri-p4-web-wiring-fix-r2-report.md`)
- **코드 워크트리**: `/Users/kknaks/orca/workspaces/Strong_hajin/strong-hajin-projects` · 브랜치 `kknaksss/strong-hajin-projects` · HEAD `a1f6791`(변동 없음)
- **변경**: 허용된 **2개 파일뿐** — 코드 1 · 문서 1
- 커밋 · push · Release **없음**

---

## 1. 한 줄 결론

**R-1**(StrictMode 에서 `mounted` 가 되살아나지 않는 결함 — **내가 직전 회차에 들인 것**)을
effect 본문에서 `true` 로 되돌려 닫았다. **R-2**(동시 import 관측을 「실제 제품 결함」으로 단정한
서술)를 **시험 환경에서 관측한 경합 + 동시 호출 안전성 보강**으로 내렸다 — **코드 동작은 바꾸지
않았다.** `tsc` 통과 · `shell.test.ts` 13/13 · 관련 테스트 24/24 3연속 · 전체 3회 중 1회 완전 통과(§4).

---

## 2. R-1 — StrictMode 에서 `mounted` 복원

### 무엇이 잘못됐나 (내가 들인 결함)

```ts
const mounted = useRef(true);
useEffect(() => () => { mounted.current = false; }, []);   // ← 본문이 없다
```

`main.tsx` 가 `<StrictMode>` 를 쓰고, React 18 개발 빌드는 같은 인스턴스에서 effect 를
**mount → cleanup → mount** 로 두 번 돌린다. 위 코드는 정리에서 `false` 로 **내리기만** 하고
본문에서 되돌리지 않아, 모의 언마운트 이후 `mounted.current` 가 **영구히 `false`** 가 된다.

결과: **개발 빌드에서 U-3(절전 방지 실패)·정리 실패 한 줄이 아예 뜨지 않는다.**
운영 빌드는 정상이고 녹음도 깨지지 않지만, **U-3 을 눈으로 확인할 길이 개발 중에 막힌다** —
그 한 줄이 바로 「조용한 실패를 드러낸다」는 이 래퍼의 유일한 새 UI 라 가볍지 않다.

### 고친 것

```ts
const mounted = useRef(true);
useEffect(() => {
  mounted.current = true;      // ← StrictMode 의 두 번째 mount 에서 되살아난다
  return () => {
    mounted.current = false;   // ← 언마운트 뒤 늦은 호출은 계속 차단
  };
}, []);
```

- **언마운트 뒤 늦은 호출 차단은 그대로다** — 정리에서 내리는 동작을 없애지 않았다
- 회차 가드(`wakeSession.current !== session`)도 그대로다. 두 가드가 함께 선다
- 왜 회의 경로에는 이 문제가 없는지 주석에 남겼다 — `stream.ts` 의 `stopped` 는
  **effect 지역 변수**라 회차마다 새로 만들어지고, ref 처럼 인스턴스에 눌어붙지 않는다

---

## 3. R-2 — 증거를 넘어선 서술을 내렸다

### 무엇이 과했나

직전 fix 보고서는 §1·§6 에서 동시 `import()` 관측을 **「실제 결함」**·**「사용자에게 이유 없는
U-3 이 보인다」**로 적었다. 그러나 그 관측은 `vi.mock` + `vi.resetModules()` 를 쓰는
**jsdom/vitest 모듈 러너**에서 나왔고, **실제 번들러·브라우저에서 같은 specifier 의 동시
`import()` 는 같은 약속을 돌려주고 두 번째가 실패하지 않는다.** 확인되지 않은 것을 단정했다.

### 고친 것 (`tauri-p4-web-wiring-fix-report.md`)

| 자리 | 이전 | 지금 |
|---|---|---|
| §1 한 줄 결론 | 「**실제 결함**을 발견해 함께 고쳤다」 | 「**시험 환경에서** 경합을 관측해 **동시 호출 안전성을 보강**했다」 |
| §6 제목 | 「⚠ 시험이 잡아낸 **실제 결함**」 | 「**동시 호출 안전성 보강** — 시험 환경에서 관측한 경합」 |
| §6 본문 | 「**왜 실해인가** … 사용자에게 이유 없는 U-3」 | **관측 환경을 명시**하고, ⚠ 로 「제품 결함으로 단정하지 않는다 · 앞선 판의 그 서술을 내린다」를 적음 |
| §6 말미 | 「시험이 없었으면 못 찾았을 **제품 버그**」 | 「**제품 버그로 기록하지 않는다** — 제품 환경에서 같은 실패가 난다는 증거가 없다」 |
| §2 변경표 | 「동시 import **경합 수정**」 | 「동시 호출 **안전성 보강**」 |
| §9-3 잔여 | 「실제 웹뷰에서도 같은 형태인지 Phase 5 가 확인」 | 「제품 환경은 같은 약속을 돌려주므로 **같은 실패가 난다고 보지 않는다**」 |

### 코드는 그대로 두었다

브리프대로 **`shell.ts` 를 한 줄도 바꾸지 않았다.** 약속 공유(`corePromise`)는 유지한다 —

- 호출마다 동적 import 를 되풀이할 이유가 없다
- 약속을 하나로 모으는 편이 **어느 환경에서도 옳다**
- 실패 시 캐시를 비우므로 한 번의 실패로 기능이 영구히 죽지 않는다

즉 **결함 수정이 아니라 보강**이고, 이제 보고서도 그렇게 읽힌다.

---

## 4. 검증

| # | 명령 | 결과 |
|---|---|---|
| V-1 | `npx tsc --noEmit` | **통과**(출력 0줄) |
| V-2 | `npx vitest run src/lib/shell.test.ts` | **13 passed** |
| V-3 | `npx vitest run src/features/browser/ src/lib/shell.test.ts` × 3 | **24 passed × 3연속** |
| V-4 | `make frontend-test` × 3 | run1 `1 failed / 1052` · run2 `1 failed / 1052` · **run3 `1053 passed` (EXIT=0)** |
| V-5 | `find -newermt` · `git status` | 이번 회차 변경 **코드 1 · 문서 1** (§5) |

### V-4 의 실패 둘은 내 변경과 무관하다 — 근거

- 실패한 파일이 **매번 다르다**: run1 `ProjectPage.test.tsx` · run2 `ActionCenter.test.tsx`
- **둘 다 이번 변경과 접점이 없다.** 내가 건드린 것은 `BrowserRecordingPage.tsx` 의
  `mounted` effect 한 곳뿐이고, 그 컴포넌트를 렌더하는 테스트는 실패 목록에 없다
- **내 변경이 닿는 테스트는 3연속 전건 통과**했다(V-3 — `src/features/browser/` 24건 포함)
- run3 은 **1053 전건 통과**
- 이 현상은 앞선 회차에서 **기준선(내 변경을 되돌린 트리)도 4회 중 2회 실패**하는 것으로
  이미 측정해 둔 **스위트 전반의 시간 의존 불안정**과 같은 형태다(파일이 매번 다르고,
  「불러오는 중」에서 요소를 못 찾는 모양)

> **「불안정이 사라졌다」고 쓰지 않는다.** 직전 보고서가 3연속 통과를 근거로 「재현되지
> 않았다」고 적었는데, 이번에 다시 나왔다. **여전히 있는 것으로 보는 편이 맞다.**

---

## 5. 변경 파일 — 허용 2개

| 파일 | 변경 |
|---|---|
| `frontend/src/features/browser/BrowserRecordingPage.tsx` | R-1 — `mounted` effect 본문에서 `true` 복원 |
| `orchestration/work/.../tauri-p4-web-wiring-fix-report.md` | R-2 — §1 · §2 · §6 · §9-3 표현 정정 |

`find -newermt` 로 확인: 이번 회차에 손댄 코드 파일은 **`BrowserRecordingPage.tsx` 하나**다.

---

## 6. 금지 사항 준수

| 금지 | 확인 |
|---|---|
| `src-tauri/**` | **0줄**(이번 회차 변경 파일 0건) |
| `api.ts` · `microphone.ts` | **0줄** |
| 운영 · 배포 | 손대지 않았다 |
| 허용 파일 외 | 없다 — 코드 1 · 문서 1 |
| 코드 동작 변경(R-2) | **없다** — `shell.ts` 무변경, 문구만 고쳤다 |
| 커밋 · push · Release | 하지 않았다. HEAD `a1f6791` 그대로 |

---

## 7. 남은 것 (이번 범위 밖)

| # | 내용 |
|---|---|
| **1** | **R-3** — `open_external` 실패가 사용자에게는 여전히 무반응이다(반환값·`console.warn` 뿐). 토스트 등으로 알릴지는 SPEC 판단 |
| **2** | **R-5** — 화면 배선 회귀 시험이 아직 없다. W-1·W-4·R-1 은 **코드 검토 + `tsc`** 증거뿐이고, 특히 **R-1 의 StrictMode 동작을 고정하는 시험이 없다** — 같은 실수가 다시 들어올 수 있다 |
| **3** | 스위트 전반의 시간 의존 불안정(§4) — 이번에도 관측됐다 |
| **4** | 실제 셸에서의 동작은 여전히 미확인(M-1 미측정) — Phase 5 |
