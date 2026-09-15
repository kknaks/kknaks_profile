# 회의 빠른 시작 중복 생성 — frontend 결과 보고

워크트리 `ax-workspace/sc-meeting-room` · 브랜치 `kknaksss/sc-meeting-room` · HEAD `9fbf4f5` · 커밋/push/PR 없음.
`backend/` 무수정(읽기만). `.design-sync/` · `frontend/ds-entry.tsx` · 기존 프론트 변경 모두 보존.
이번 태스크가 만진 파일은 **둘뿐**이다.

---

## 1. 원인 — 사용자 분석이 정확했다

`MeetingListPage.tsx` 의 `quickStart` 가 **`setBusy` 의 함수형 업데이터 «안»** 에서 서버를 불렀다.

```ts
setBusy((current) => {
  if (current) return current;
  void (async () => { const next = await quickStartMeeting(); ... })();   // ← 부수효과가 업데이터 안에
  return true;
});
```

업데이터는 React 가 **순수하다고 전제하는 자리**다. 그래서 개발 모드(StrictMode)가 그 순수함을 드러내려고
**일부러 두 번 돌린다** — 두 번 다 `quickStartMeeting()` 이 나가 `POST /api/meetings/quick-start` 가
1ms 간격으로 두 번, 둘 다 201, 회의가 둘 생겼다.

`if (current) return current` 가드가 못 막은 이유도 분명하다: 두 번의 호출이 **같은 `current`(false)** 를 본다.
상태가 아직 커밋되지 않았으므로 첫 번째가 두 번째에게 보이지 않는다.

**왜 빠른 시작에서만 터졌나** — 예약(`bookMeeting`)은 `Idempotency-Key` 를 실어 보내
(`lib/api.ts:908~912`, `rules.md` 「재전송은 영수증이다」) 두 번 나가도 서버가 회의를 둘 만들지 않는다.
`quickStartMeeting` 에는 그 열쇠가 없어 두 요청이 그대로 회의 둘이 됐다.

## 2. 고친 것 — `frontend/src/features/meetings/MeetingListPage.tsx`

```ts
const startInFlight = useRef(false);
const quickStart = useCallback(async () => {
  if (startInFlight.current) return;      // 잠금은 «그 자리에서 바로» 걸린다
  startInFlight.current = true;
  setBusy(true);                          // state 는 단추를 흐리게 하는 표시일 뿐
  try {
    const next = await quickStartMeeting();   // 호출은 업데이터 «밖»
    onOpenMeeting(next.meeting.meeting_id);
  } catch (reason) {
    onError(reason instanceof Error ? reason.message : "회의를 시작하지 못했습니다.");
  } finally {
    startInFlight.current = false;        // 실패해도 풀린다 — 다시 누를 수 있다
    setBusy(false);
  }
}, [onError, onOpenMeeting]);
```

- **네트워크 호출을 업데이터 밖으로 뺐다.** 업데이터 자체를 없앴으므로 그 자리는 다시 순수해졌다.
- **잠금은 `useRef`.** ref 는 렌더를 기다리지 않고 즉시 바뀌어, 같은 tick 의 두 번째 진입이 이미 잠긴 것을 본다.
  `busy` state 하나로는 StrictMode 도 연타도 막지 못한다 — 그것은 **잠금이 아니라 표시**라 그대로 뒀다.
- 실패 후 재시도 가능 · 성공 시 `onOpenMeeting` 한 번 · `disabled={busy}` 그대로.
- **StrictMode 를 끄지 않았고 백엔드로 떠넘기지 않았다.** `api.ts` · idempotency 계층 · 권한 판단 무수정.

## 3. 같은 패턴 전수 조사 — 이 한 곳뿐이다

단순 텍스트 검색으로 단정하지 않고, `frontend/src` 의 `.ts`/`.tsx`(테스트 제외) 전부에서
`set<대문자>(` 호출을 찾아 **괄호 균형으로 인자 몸통을 잘라** 그 안을 검사했다.

| 단계 | 결과 |
|---|---|
| 함수형 업데이터 총수 | **123** |
| ① `await` · `void` · `.then(` · `fetch(` · `new Promise` · `window.` · `document.` · `localStorage` · 타이머 · `console.` | 7건 적발 |
| ② `api.ts` 가 내보내는 서버 호출 **119개 이름** + `on[A-Z]` 부모 콜백 + `fetch`/`Promise` | 2건 적발 |

**적발 9건을 한 줄씩 열어 본 결과, 진짜는 하나다:**

| 자리 | 판정 |
|---|---|
| `MeetingListPage.tsx:121` | ✅ **진짜 — 이번에 고친 것** |
| `BrowserRecordingPage.tsx:33` · `MeetingDetailPage.tsx:349` · `DailyReportPage.tsx:195` · `TodayPage.tsx:121` · `WorkModals.tsx:489` | ❌ 오탐 — `setInterval(() => …)` 타이머 콜백이다(`set` + 대문자라 정규식에 걸렸다). 업데이터가 아니다 |
| `WorkModals.tsx:780` `setRefChoices((await getTasks(true)).filter(…))` | ❌ 오탐 — `await` 가 **`setX` 를 부르기 전에** 끝난다. 인자는 평범한 값이고 업데이터가 아니다 |
| `ShareModal.tsx:61` `setViewers(await shareMeetingWith(…))` | ❌ 오탐 — 위와 같다. 몸통 뒤쪽의 `.map(one => …)` 때문에 걸렸다 |

→ **회의 생성 경로 둘 중 예약(`BookingModal.submit`)은 이 원인이 아니다.** 업데이터를 쓰지 않고
(`if (!ready || busy) return; setBusy(true);` 로 평범하게 간다) `Idempotency-Key` 까지 실어 보낸다.

### 범위 밖 관찰 (고치지 않았다 — 원인이 다르다)
`MeetingListPage.drop()`(DELETE)과 `ShareModal.share()`(POST)는 `busy` **state 하나로만** 연타를 막는다.
StrictMode 버그는 아니지만 «같은 tick 의 두 클릭» 에는 이론상 두 번 나갈 수 있다. 다만 둘 다
**효과가 멱등**하다 — 같은 회의를 두 번 지워도, 같은 사람을 두 번 공유해도 결과가 같아 중복 «생성» 이 아니다.
이번 브리프는 「같은 원인이 있으면 최소 수정」이라 손대지 않고 관찰로만 남긴다.

## 4. 검증

```
cd frontend && npx tsc --noEmit                      → 오류 0
cd frontend && npx vitest run --no-file-parallelism  → 50 files / 547 passed / 0 failed
```
직전 기준 543 → **547** (+4).

### ★ 검사가 진짜로 버그를 잡는지 먼저 확인했다 (RED 확인)
새 검사를 통과시키기만 하는 것이 아니라, **고친 코드를 잠시 되돌려 놓고** 돌려 봤다:

```
× StrictMode 에서도 클릭 한 번에 quick-start 는 한 번만 나간다   → expected 1 times, but got 2 times
× 응답을 기다리는 동안 연타해도 한 번만 나간다                    → expected 1 times, but got 2 times
× 실패하면 그 사실을 내고 잠금이 풀린다                            → expected 1 times, but got 2 times
```

**`got 2 times` — 사용자가 본 「클릭 한 번에 POST 두 번」이 검사 안에서 그대로 재현된다.**
고친 코드로 되돌리니 넷 다 초록이다. 확인 뒤 파일을 원래대로 복구했다(현재 워크트리에는 고친 판이 있다).

같은 실행에서 **기존 검사 「[회의 시작]은 값을 묻지 않고 바로 연다」는 버그 코드에서도 초록**이었다 —
StrictMode 로 렌더하지 않고 호출 «횟수» 를 세지 않기 때문이다. 버그가 여기로 빠져나간 자리가 그곳이다.

### 새로 건 회귀 (`MeetingList.test.tsx`, `<StrictMode>` 로 렌더)
1. **StrictMode 에서 클릭 한 번 → `quickStartMeeting` 정확히 1회**, `onOpenMeeting` 1회
2. **응답 대기 중 3연타 → 여전히 1회** (응답을 프라미스로 붙잡아 「busy 가 커밋되기 전」을 만든다)
3. **실패 → `onError` 로 사유를 내고 회의를 열지 않으며, 잠금이 풀려 다시 누르면 2회째가 나간다**
4. **예약은 재전송해도 같은 `Idempotency-Key`** 를 들고 간다 (그 열쇠가 사라지면 예약도 같은 증상이 나므로 잠근다)

### 병렬 실행 (숨기지 않고 보고)
`npx vitest run` 3회 → `546+1실패 / 547 / 547`. 낙오한 것은 **내가 만지지 않은**
`features/work/Checklist.test.tsx` 의 테스트 하나이고, 직전 두 태스크에서도 같은 파일이 매번 다른
테스트로 낙오했다(단독 실행은 항상 전량 통과). 기존 부하 민감성으로 본다. **직렬은 547 전량 통과.**

## 5. 실제 브라우저 Network 확인 — **하지 않았다**

DevTools Network 에서 클릭당 POST 1회를 **직접 확인하지 않았다.** 이유 둘:
- 사용자가 직전 태스크에서 「e2e 는 내가 직접 할거야」라고 명시했고 그 선호를 유지했다.
- 브리프가 실제 회의/데이터 생성을 피하라고 했다. 빠른 시작은 **누르는 순간 회의가 생기는** 동작이라
  화면에서 눌러 보는 것 자체가 데이터를 만든다.

**실제 생성 검증을 했다고 보고하지 않는다.** 지금 근거는 ①원인 코드 확인 ②StrictMode 재현 검사가
버그 코드에서 `got 2 times` 로 빨개지고 고친 코드에서 초록이 되는 것, 둘이다.
검사는 앱과 **같은 React 개발 빌드 · 같은 StrictMode** 에서 도므로 메커니즘은 동일하지만,
「실제 브라우저의 Network 탭」이라는 마지막 한 칸은 비어 있다.

### 사용자 확인 방법
1. `cd frontend && npm run dev` → 로그인 → [회의] 화면
2. DevTools Network 에서 `quick-start` 로 필터
3. **[회의 시작] 한 번 클릭 → `POST /api/meetings/quick-start` 가 1건**이면 고쳐진 것이다(예전에는 2건)
4. 응답이 오기 전 빠르게 여러 번 눌러도 1건이어야 한다
5. 목록에 회의가 **하나만** 늘었는지 함께 확인

## 6. 변경 파일

| 파일 | 무엇 |
|---|---|
| `frontend/src/features/meetings/MeetingListPage.tsx` | `quickStart` — 호출을 업데이터 밖으로, `useRef` 잠금 |
| `frontend/src/features/meetings/MeetingList.test.tsx` | StrictMode 회귀 4건 (+`StrictMode` import) |

`backend/` · `docs/` · `.design-sync/` · `frontend/ds-entry.tsx` **무수정**.
quick-start / 예약 외 무관한 변경 없음. 종료 후 UI 작업은 섞지 않았다.
