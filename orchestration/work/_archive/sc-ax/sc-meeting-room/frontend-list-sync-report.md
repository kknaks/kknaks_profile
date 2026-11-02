# 프론트 — 왼쪽 회의 목록이 상태 변경을 따라오지 않는다

2026-09-15 · `sc-ax-fe` · 브랜치 `kknaksss/sc-meeting-room` · **미커밋**

## 한 줄

증상 셋 중 **둘은 같은 뿌리**(상세 → 목록 길이 없다)이고, **하나는 짚음이 틀렸다** —
구획이 낡은 것이 아니라 **구획의 «이름» 이 그 칸을 잘못 부르고 있었다.**

---

## 짚음이 맞았는지

| 코디의 짚음 | 판정 |
|---|---|
| `MeetingWorkspace.tsx:89` 배선이 한 방향뿐이다 — 상세에서 일어난 상태 변경이 목록으로 돌아오는 길이 없다 | **맞다.** 증상 1 의 원인이다 |
| [바로 시작]도 같은 구멍일 수 있다 | **반은 맞다.** 같은 「목록을 다시 안 읽는다」이지만 자리가 다르다 — `MeetingListPage` **안**이고, 워크스페이스 배선과 무관하다 |
| 구획 분류가 «낡은 상태로 남는다» / 배지와 구획이 «다른 데서 판단하고 있다» | **틀렸다.** 둘은 처음부터 **같은 응답**에서 나온다. 아래 §3 |

---

## 1. 증상 1 — 상세에서 바뀐 상태가 목록으로 안 돌아온다

### 진짜 원인

`MeetingWorkspace.tsx:89` — 길이 한 방향뿐이다.

```
목록 카드 [수정] → onMeetingUpdated → setDetailReloadToken → 상세만 다시 읽는다
상세에서 상태 변경 →  ✗ 아무 데도 안 간다
```

목록은 `MeetingListPage.tsx:55 reload` 를 **마운트 때와 `onRegisterRefresh`(셸의 새로고침)에서만**
돈다. 상세가 회의를 시작·종료해도 목록은 처음 읽은 `payload` 를 그대로 들고 있다.

### 고친 자리 — **반대 방향 길을 냈다**

이미 있던 `detailReloadToken` 과 **대칭**으로 `listReloadToken` 을 뒀다. 새 관용을 만들지 않았다.

| 파일 | 무엇 |
|---|---|
| `MeetingDetailPage.tsx` | `onMeetingChanged?: () => void` — **상태 값이 달라진 순간** 한 번 부른다 |
| `MeetingWorkspace.tsx` | `listReloadToken` + `reloadList` → 상세의 `onMeetingChanged` 에 물린다 |
| `MeetingListPage.tsx` | `reloadToken` prop — 값이 오르면 다시 읽는다 |

**상태를 바꾸는 자리를 하나씩 세어 부르지 않았다.** 그러면 다음에 생기는 경로가 반드시 빠진다.
대신 **서버가 낸 `meeting.status` 가 달라졌을 때** 한 번 알린다:

```ts
const seenStatus = useRef<string | null>(null);
useEffect(() => {
  const next = meeting?.status ?? null;
  if (next === null) return;
  const previous = seenStatus.current;
  seenStatus.current = next;
  if (previous !== null && previous !== next) onMeetingChanged?.();
}, [meeting?.status, onMeetingChanged]);
```

- **처음 읽었을 때는 안 알린다** — 목록이 방금 그 값을 실어 준 것이다 (헛 재요청 없음)
- **폴링이 아니다** — 상태가 실제로 달라졌을 때만 한 번 오른다
- **낙관 렌더가 아니다** — 「무엇이 어떻게 바뀌었는지」를 보내지 않는다. 보내는 것은
  **「다시 읽어라」** 하나이고, 그리는 값은 전부 서버가 낸 것이다

### 상태를 바꾸는 경로 전수 — 한 자리가 전부 덮는다

| # | 경로 | 어디 | 덮이나 |
|---|---|---|---|
| 1 | **[회의 시작]** | `MeetingDetailPage:831` `run(startMeeting)` → `reload()` | ✅ |
| 2 | **[회의 종료]** | `:840` `run(endMeeting)` → `reload()` | ✅ |
| 3 | **[다시 시도]** | `:875` `run(retryMeetingFinalize)` → `reload()` | ✅ |
| 4 | **합성 실패 / 완료** | 「정리 중」 폴링(`SETTLING_POLL_MS`)이 `reload()` | ✅ |
| 5 | **스트림이 끊길 때** | `onStreamClosed` 의 `ended`·`stale_status` → `reload()` | ✅ |
| 6 | **[바로 시작]** | `MeetingListPage` 안 — 상세를 안 거친다 | ❌ → §2 에서 따로 |
| 7 | 목록 카드 [수정]·[삭제] | 목록이 스스로 `reload()` | 이미 됨 |

**1~5 가 공통으로 하는 일이 「상세를 다시 읽는 것」**이라, 그 결과인 `status` 하나만 보면 전부 걸린다.
경로가 앞으로 늘어도 같다.

---

## 2. 증상 3 — [바로 시작]한 회의가 목록에 안 생긴다

### 진짜 원인

`MeetingListPage.tsx:141 quickStart` 가 **`reload()` 를 안 부른다.**

```ts
const next = await quickStartMeeting();
onOpenMeeting(next.meeting.meeting_id);   // 상세만 연다. 목록은 그대로
```

워크스페이스 배선과 **무관하다** — 목록 자기 안에서 나는 일이다. (코디의 「다른 원인일 수 있다」가 맞다.)

### 고친 자리

```ts
const next = await quickStartMeeting();
await reload().catch(() => undefined);    // ← 목록이 서버에서 다시 받는다
onOpenMeeting(next.meeting.meeting_id);
```

돌아온 회의를 **낙관적으로 목록에 끼워 넣지 않았다** — 구획도 배지도 서버가 낸 값으로 서야 한다.
다시 읽기가 실패해도 여는 것은 막지 않는다(회의는 이미 섰다).

---

## 3. 증상 2 — 「진행 중」 회의가 「예정」 구획에 있다 ⚠ **짚음이 틀렸다**

### 낡은 것이 아니다 — 처음부터 그 자리였다

배지와 구획은 **같은 `listMeetings()` 응답**에서 나온다. 따로 판단하는 자리가 없다.
진짜 원인은 **서버가 내는 칸의 뜻과 화면이 붙인 이름이 다르다**는 것이다:

```python
# policy.py:277
return relation == "shared" or parse_status(status) in PAST_STATUSES or ends_at <= now
# PAST_STATUSES = {DONE, FAILED, CANCELLED}          ← in_progress 도 summarizing 도 없다
```

서버의 `upcoming` 은 「예정」이 아니라 **「아직 안 지난 회의」**다. 끝날 시각이 안 지난
**진행 중·정리 중이 그 칸에 함께 온다.** 그런데 화면은 그 칸 전체에 `meetingScreen.upcoming`
=「예정」이라는 제목 하나를 달았다 (`MeetingListPage.tsx:204`).

**즉 카드가 낡아서가 아니라 제목이 그 칸을 잘못 불렀다.** 배지(`진행 중`)는 처음부터 맞았다.

### 고친 자리 — **카드 배지가 읽는 그 값으로 한 번 더 가른다**

```ts
const notPast = payload?.upcoming ?? [];
const running  = notPast.filter((row) => row.status === "in_progress" || row.status === "summarizing");
const upcoming = notPast.filter((row) => row.status !== "in_progress" && row.status !== "summarizing");
```

- 구획 제목은 `meetingStatusLabel.in_progress` — **카드 배지와 같은 낱말**이다.
  둘이 다른 말을 할 방법 자체가 없어졌다
- 도는 회의가 **맨 위**다 (지금 가야 할 자리)
- 값을 새로 지어내지 않았다. `row.status` 를 한 번 더 읽을 뿐이다
- **서버 분류를 바꾸지 않았다** — `backend/` 무수정

> 대안으로 「예정」 제목만 다른 낱말로 갈 수도 있었지만, 그러면 **도는 회의가 목록 가운데
> 파묻히는** 문제가 그대로다. 구획을 가르는 쪽이 브리프의 「배지와 구획이 따로 놀면 안 된다」에 맞다.

---

## 4. 곁에서 확인한 것 — **고치지 않았다**

`MeetingWorkspace` 가 `onRegisterRefresh`(셸의 새로고침)를 **목록과 상세 «둘 다»** 에 넘긴다
(`:96` · `:123`). 둘이 같은 자리에 등록해서 **나중에 등록한 쪽이 이긴다** — 셸의 새로고침이
둘 중 하나만 돈다는 뜻이다. 이번 증상과는 무관하고 브리프 범위 밖이라 **손대지 않았다.**
고칠 값어치가 있으면 따로 발주해 달라.

---

## 5. 테스트가 거는 것 — 넷, 전부 적색 먼저 확인

`MeetingWorkspace.test.tsx` 에 「상세 ↔ 목록 동기화」 구획을 더했다.

| 테스트 | 적색 확인 |
|---|---|
| 회의를 시작하면 **카드 배지와 구획이 함께** 바뀐다 (목록을 실제로 다시 읽는 것까지) | `onMeetingChanged` 배선을 끊으니 적색 |
| 회의를 종료해도 그렇다 — 카드가 「지난」으로 넘어간다 | 〃 |
| **[바로 시작] 직후 목록에 선다** — 새로고침을 요구하지 않는다 | `await reload()` 를 빼니 적색 (이것만) |
| **배지와 구획이 같은 값에서 나온다** — 「진행 중」·「정리 중」이 「예정」 아래 서지 않는다 | 구획을 안 가르게 되돌리니 적색 |

셋을 각각 따로 되돌려 봤고, **끊은 자리에 대응하는 테스트만** 적색이 됐다 — 서로 기대어 있지 않다.

### 못 건 것

- **화면을 오래 열어 둘 때의 표류**는 안 걸었다. 다른 사람이 그 회의를 끝내면 내 목록은 여전히
  낡는다 — 그것은 폴링이나 푸시의 일이고 **폴링 금지**가 브리프에 있다. 이번 판은
  **내가 일으킨 변화**가 내 목록에 도는 것까지다.
- 육안 검증은 안 했다 (사용자가 직접 한다).

---

## 6. 검증

| 게이트 | 결과 |
|---|---|
| `npx tsc --noEmit` | **통과** |
| `npx vitest run` | **590 테스트 전부 통과** (직전 586 + 4) |
| `npx vite build` | **통과** (1.22s) |
| 기존 회의 테스트 | 손상 0 |

`vitest` 종료 코드 1 은 그대로다 (`WorkViews.tsx:542` — 지시대로 안 고쳤다).

## 하지 말라던 것

폴링 안 넣었다 · 낙관 렌더 안 했다(신호만 보내고 값은 서버가 낸다) · 충돌 판정 UI 없음 ·
원본 여는 자리 없음 · 계보 없음 · `backend/` 무수정 · 로컬 스택 무접촉 ·
`git add .` 안 했다 · 커밋·push·PR 안 했다.
