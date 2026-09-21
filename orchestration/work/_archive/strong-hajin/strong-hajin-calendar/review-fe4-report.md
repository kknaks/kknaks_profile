# 리뷰 리포트 — strong-hajin-calendar / Phase FE-4 코드 검수 (2026-09-21)

## 판정: **PASS** (WARN 4건 — 전부 **사용자 E2E / 후속**으로 넘길 것이지 재발주 사유가 아니다)

**아홉 항목이 전부 통과했다.** FAIL 은 없다.

코디가 특별히 짚은 셋이 **셋 다 깨끗하다**:

- **문구의 주인이 옳게 갈렸다** — 회의 겹침은 `ApiError.message`(= 서버 문자열)를 **그대로** 내고,
  **`detail.code` 를 읽는 길로 새지 않는다.** 방예약 `409` 의 `{code,…}` 길은 `detail?.code` 가
  없으면 **`null` 을 돌려주고 일반 경로로 떨어지게** 이미 짜여 있다(`BookingModal.tsx:36-40`).
  **배정 겹침은 화면이 만든다.**
- **경계가 서버와 같다** — 반열림 `[시작, 끝)`. **11:00 끝 + 11:00 시작이 둘 다 선다.**
  모델 단위(`overlapsMinutes`)와 실제 드롭(`createTaskSchedule` 이 `11:00–12:00` 으로 나감)
  **양쪽에 테스트가 있다.**
- **「보낸 업무」 탭에서 보낸 업무가 안 사라진다** — 레일의 **업무 축을 한 줄도 안 건드렸다.**
  `MyWorkPage.test.tsx:269` 이 탭 전환 뒤 보낸 업무의 존재 **그리고** `getCalendar` **호출 1회**를
  같이 박는다.

**테스트 약화가 0건이다** — 이번 검수의 핵심이었다. 테스트 diff **+314 / −2** 이고
**`−2` 두 줄은 한 테스트의 제목과 단언 하나**인데, **K22 가 그 값을 바꿨기 때문**이다.
그 자리는 **오히려 조여졌다**(같은 테스트의 다른 두 단언 유지 + 「마침표 없음」 테스트 신설).
**나머지 11개 테스트 파일은 `−0`** 이다.

---

## 검수 범위

FE-3 커밋 `3c3dce2` **위의 uncommitted diff** — **수정 18 · 신규 0**, 전부 `frontend/`,
642 insertions / 52 deletions.
**테스트는 돌리지 않았다**(지시). **코드도 한 줄 고치지 않았다.**
코디가 확인한 것(`frontend/` 밖 0건 · **954 passed / 0 failed**(기준선 929 → **+25**) ·
`tsc` exit 0 · `make verify` 의 `material/job-queue` 는 기존 flaky)은 다시 세지 않았다.

실행한 검사: `git diff` 전문 정독 · `git diff --numstat` 로 테스트 파일별 `+/−` 대조 ·
`grep` 전수 · SSOT 대조(SPEC-004 §2.1·§2.6·§2.9·§2.10·§4 Case Matrix · DEC-003 증보 8~10 ·
WORK `Phase FE-4`) · **BE-3·BE-4 산출물 읽기 확인**
(`modules/time_blocks.py` · `platform/time_blocks.py` · `modules/meetings/policy.py:224` ·
`entrypoints/http.py:520-565`).

### 변경 18 — **비-테스트 6 · 테스트 12**

> ⚠ 브리프는 테스트 파일을 **여덟**으로 셌는데 **열둘**이다(`+2` 짜리가 다섯이 아니라 **여섯** —
> `work/` 다섯 + `MyWorkPage.test.tsx` 의 mock 한 줄이 그 파일의 `+41` 안에 들어 있다).
> **수치 `+314 / −2` 는 정확하다.**

| 비-테스트 (6) | +/− |
|---|---|
| `features/calendar/CalendarPage.tsx` | +31 −3 |
| `features/calendar/calendarModel.ts` | +27 −0 |
| `features/calendar/calendarWrites.ts` | +56 −7 |
| `features/work/MyWorkPage.tsx` | +52 −3 |
| `lib/labels.ts` | +12 −1 |
| `shell/CalendarRail.tsx` | +150 −36 |

| 테스트 (12) | +/− | 왜 바뀌었나 |
|---|---|---|
| `shell/CalendarRail.test.tsx` | **+95 −0** | K23·K24 신규 7건 |
| `features/calendar/calendarWrites.test.ts` | **+47 −2** | K22 가드 5건 + 409 값 교체(아래 ⑥) |
| `features/calendar/CalendarInteractions.test.tsx` | **+45 −0** | K22 드롭·손잡이 4건 |
| `features/work/MyWorkPage.test.tsx` | **+41 −0** | K23·K24 회귀 1건 + mock 한 줄 |
| `features/calendar/calendarModel.test.ts` | **+30 −0** | `blockingBlocks` 5건 |
| `features/meetings/MeetingEditModal.test.tsx` | **+25 −0** | K22 회의 문구 1건 |
| `features/meetings/MeetingList.test.tsx` | **+21 −0** | K22 회의 문구 1건 |
| `work/CreateWork` · `InboxRead` · `WorkRequestModalFlow` · `WorkRowCompletion` · `WorkTabsAndTables` | **각 +2 −0** | `vi.mock` 공장에 `getCalendar` 추가 |

**allowed_paths** — 18개 전부 `frontend/` 아래다. `backend/`·`docs/`·`para/`·`orchestration/` **0건**.

---

## ① 문구의 주인이 옳게 갈렸나 — **갈렸다. `detail.code` 를 읽는 자리 0건**

### 회의 겹침 = **서버 문자열 그대로**

이름(「민아 님의」)이 들어 있어 화면이 지을 수 없는 문장이다 — 남의 시간은 busy/free 만 읽으므로
화면에 그 이름이 올 자리가 없다. 코드가 그렇게 돼 있다:

| 자리 | 무엇 |
|---|---|
| 서버 | `meetings/application.py:387` `MeetingTimeOverlap(f"{이름} 님의 일정과 겹칩니다")` |
| 직렬화 | `entrypoints/http.py:532-533` — `MeetingTimeOverlap` 은 **`detail=str(error)`**, 즉 **문자열**이다 |
| 클라이언트 | `lib/api.ts:106`·`121` — `detail` 이 문자열이면 **그것이 `ApiError.message`** 다 |
| 화면 | `BookingModal.tsx:271` `onError(reason.message)` — **가공 없음** |

**미끄러운 자리를 지나갔다.** 같은 파일이 방예약 `409` 를 위해 `detail.code` 를 먼저 본다:

```ts
// BookingModal.tsx:33-40
function roomRejectionOf(reason: unknown): { message: string; rooms: MeetingRoom[] } | null {
  if (!(reason instanceof ApiError) || reason.status !== 409) return null;
  const detail = reason.detail as { code?: string; available_rooms?: MeetingRoom[] } | undefined;
  const message = detail?.code ? meetingScreen.roomRejected[detail.code] : undefined;
  if (!message) return null;          // ← 겹침(문자열 detail)은 여기서 빠진다
  return { message, rooms: detail?.available_rooms ?? [] };
}
```

겹침 `409` 는 `detail` 이 문자열이라 `detail?.code` 가 `undefined` → **`null` 반환 → `else` 로 떨어져
`reason.message` 가 그대로 나간다.** 객체 `detail` 을 내는 `409` 는 `http.py:520-527` 한 자리뿐이고
**겹침은 거기 없다**(`:532`·`:562` 둘 다 `str(error)`).

**`detail`(또는 `.code`)을 읽는 자리를 전수했다** — 셋뿐이고 **셋 다 겹침과 무관**하다:
`AttachModal.tsx:117`(자료 첨부) · `MeetingDetailPage.tsx:73`(안건 경합) · `BookingModal.tsx:36`(방예약).
**이번 diff 는 그 셋을 한 글자도 안 건드렸다.**

새 테스트 둘이 양쪽 모달에서 박는다 — `MeetingList.test.tsx:341`(예약) ·
`MeetingEditModal.test.tsx:170`(시각 변경). 둘 다 `onError` 가 **서버 문장 그대로**임을 단언하고,
`MeetingEditModal` 쪽은 **`toBe("민아 님의 일정과 겹칩니다")` 로 마침표까지** 박는다.

### 배정 겹침 = **화면이 만든다**

`calendarDeny.overlap`(`labels.ts:995`)을 **두 자리**가 쓴다 —
가드(`overlapGuard`)와 `409` 폴백(`denyMessage`). **마침표를 덧붙이지 않았다**(서버 문자열과 동일).
**다만 그 이유 설명이 코드와 어긋난다 — WARN-2.**

---

## ② 경계가 서버와 같은가 — **같다. 11:00 + 11:00 은 둘 다 선다**

```ts
// calendarWrites.ts:108
return left.startMin < right.endMin && right.startMin < left.endMin;
```

**서버와 같은 부등호다** — `modules/time_blocks.py:147` `one_from < other_to and other_from < one_to`.
SPEC §2.9 「경계가 닿는 것은 겹침이 아니다 — 10:00–11:00 과 11:00–12:00 은 둘 다 선다」 그대로다.

**증명이 두 층이다**:

- 값 단위 — `calendarWrites.test.ts:203` 이 **양방향**을 본다(앞에 붙는 것·뒤에 붙는 것)
  **그리고** `overlapsMinutes` 를 직접 `toBe(false)` 로 박는다.
- 실제 DOM — `CalendarInteractions.test.tsx:296` 이 회의(03-04 **10:00–11:00**) 바로 뒤
  `clientY 616`(= 660분 = **11:00**)에 떨어뜨려 **`createTaskSchedule` 이 실제로 나가고**
  인자가 `{on_date:"2027-03-04", starts_at:"11:00", ends_at:"12:00"}` 임을 단언한다.
  **「막지 않는다」를 「아무 일도 안 일어난다」로 때우지 않았다.**

**「화면이 서버보다 엄한가」를 전수로 봤다** — 블록 집합이 서버와 **같은 것**이다:

| 무엇 | 화면(`blockingBlocks`) | 서버(`platform/time_blocks.py`) | 일치 |
|---|---|---|---|
| 내 배정 | `schedules[]` 전부 | 활성 담당 + 업무가 `DONE`·`CANCELLED` 아님 | ✓ — 합본 조회가 `my_work(include_closed=False)` 라 **행 집합이 이미 같다** |
| 참석·주최 회의 | `viewer_relation === "attendee"` | `owner_id in ids OR 활성 참석자` | ✓ — `policy.py:224` `attendee = 주최 or 참석` → `relation="attendee"`. **주최자도 `attendee` 로 온다** |
| 공유받은 회의 | 뺀다 | 뺀다 (K25) | ✓ |
| 조직 범위 남의 회의 | 뺀다(`relation="shared"`) | 뺀다 | ✓ |
| 취소된 회의 | 뺀다 | `status != CANCELLED` (K26) | ✓ |
| 참석자 판정 | — | `removed_at IS NULL` | ✓ — 가시성 쪽 `attendee_ids` 도 **같은 술어**(`platform/meetings.py:196-199`) |

**합본 조회에 `shared` 가 실제로 실려 온다** — 캘린더 갈래(`board` 의 span 분기,
`meetings/application.py:251-258`)는 `my_meetings` 와 달리 **`shared` 를 거르지 않는다.**
그러니 화면의 `viewer_relation` 필터는 **공회전이 아니라 K25 를 실제로 닫는 자리**다.
`calendarModel.test.ts:210`·`:216` 이 그 둘을 각각 박는다.

**탭으로 거르지 않는다** — 「업무」 탭을 봐도 회의가 내 시간을 막는다
(`CalendarPage.tsx:207-211` `busySpans` 는 `[entries]` 에만 매달리고 `tab` 이 없다).
`calendarModel.test.ts:220` 이 박는다.

**엄해지는 갈래가 하나 남아 있다 — WARN-1**(길이 0 인 회의 행). 덜 아는 갈래도 하나 — **WARN-3**.

---

## ③ 업무 축이 안 바뀌었나 (K24) — **안 바뀌었다. 회귀를 실제로 확인했다**

**레일은 여전히 자기 업무 질의가 없다.** `CalendarRail` 의 `tasks` prop 이 그대로이고
(`MyWorkPage.tsx:966` `tasks={tasks}`), `dueOn(tasks, date)` 도 그대로다.
**합본 조회는 회의 절반에만 쓴다** — `MyWorkPage.tsx:931`:

```ts
const entries = await getCalendar(from, to);
setRailMeetings(entries.filter((entry): entry is CalendarMeetingRow => entry.kind === "meeting"));
```

**업무 절반을 버린다.** 갈아탔다면 축이 `my_work` 라 「보낸 업무」가 사라졌을 자리다.

**회귀를 테스트가 직접 박는다** — `MyWorkPage.test.tsx:269`:

```ts
await openSentTab();
expect(within(screen.getByLabelText("보낸 업무")).getByText("내가 보낸 요청")).toBeTruthy();
expect(rail().getByText("주간 회의")).toBeTruthy();
expect(vi.mocked(api.getCalendar).mock.calls).toHaveLength(1);
```

세 단언이 각각 **「보낸 업무가 남는다」 · 「회의는 탭과 무관하다」 · 「탭 전환에 재조회 없다」**다.
WORK FE-4 완료판정의 회귀 줄이 그대로 닫혔다.

**탭이 재조회를 못 만든다 — 구조적으로 막혀 있다.** 조회는 `onRange(from, to)` 가 끌고,
`from`/`to` 는 `[anchor, range, today]` 에서만 나온다(`CalendarRail.tsx:157-167`) — **`tab` 이 없다.**
`loadRailMeetings` 는 `useCallback(…, [])` 로 **불변**이고 `railRange` ref 가 같은 범위를 한 번 더 막는다.

---

## ④ 회의가 탭과 무관한가 · 새 표면을 만들었나 — **무관하다. 안 만들었다**

- **새 API 가 없다** — `getCalendar` 는 캘린더 화면이 쓰던 **그 합본 조회**다.
  `lib/api.ts` 에 이번 diff 가 **한 줄도 닿지 않았다.**
- **「보낸 회의」 같은 축을 만들지 않았다** — 회의를 거르는 조건은 `kind === "meeting"` 하나이고,
  탭·관계·보낸 이로 다시 가르는 코드가 없다.
- **범위는 레일이 정하고 질의는 페이지가 한다**(`onRange`) — 「그리는 날」과 「받아 온 회의」가
  **어긋날 수 없다**(캘린더 화면 K18 과 같은 규율). `CalendarRail.test.tsx:127` 이 세 범위를 박는다:
  오늘 `2026-09-18~2026-09-18` · 주 `09-13~09-19` · 월 **`08-30~10-10`**(42칸 — 달 밖 칸도 점을 찍으므로).
  같은 주 안에서 날짜만 고르면 **호출 수가 안 는다**는 것까지 같은 테스트가 센다.
- **실패를 「없음」으로 위장하지 않는다** — `meetingsFailed` 가 한 줄을 세우고
  **업무 목록은 그대로 선다**(`CalendarRail.tsx:220`). 테스트 `:148`.
- **회의 줄은 누를 수 없다**(§2.4) — `MeetingItem` 에 `openable` 도 `onClick` 도 없다
  (`AgendaItem:256` 과 대조). 테스트 `:80`.

---

## ⑤ K17 단추 — **이미 서 있다. 이번 diff 에 없다**

`git log -S"onRegisterHeaderActions" -- CalendarPage.tsx` → **`aa8576b`(FE-2)**.
**FE-4 가 당겨 하지도, 다시 만들지도 않았다.**

읽기로 확인한 결과 **계약대로다** — `CalendarPage.tsx:486-495` 가 셸 머리에 등록하고 떠날 때 지우며,
`:482-483` 주석이 「단추는 레이아웃이라 시안 정본, **모달은 기능이라 우리 것**」을 적고
**기존 업무 생성 모달**을 연다. **시안 `TaskCreateModal` 의 필드 구성을 따라가지 않았다.**
테스트 `CalendarInteractions.test.tsx:427-439` 두 건이 박는다.

> 내 FE-3 리포트가 「FE-4 브리프에서 K17 줄을 빼라」로 올린 자리다. **브리프에 그대로 남아 있었지만
> 워커가 중복 구현하지 않았다** — 올바른 처리다.

---

## ⑥ 테스트 12개가 바뀐 이유 — **전부 정당하다. 약화 0건** (이번 검수의 핵심)

### `+2` 짜리 다섯 — **`vi.mock` 공장에 `getCalendar` 한 줄**. 단언 0줄

`work/` 의 다섯 파일이 **똑같이** 이 두 줄만 더했다:

```ts
// 우 레일의 회의 절반 (증보 K23) — 업무 목록과 **다른 질의**다.
getCalendar: vi.fn().mockResolvedValue([]),
```

- `vi.mock(…, factory)` 는 모듈을 **통째로 대체**한다 — 없으면 `MyWorkPage` 의 `getCalendar` import 가
  `undefined` 라 렌더가 죽는다. **불가피한 추가**다.
- **`[]` 를 돌려주므로 그 테스트들의 기대값이 하나도 안 바뀐다** — 레일에 회의가 0건이면
  예전과 같은 화면이다. `−0` 이 그것을 증명한다.
- **단언·`expect`·`skip`·`todo` 가 한 줄도 안 늘거나 줄지 않았다**(diff 전문 확인).

### `−2` 두 줄 — **K22 가 그 값을 바꿨다. 그리고 조여졌다**

`calendarWrites.test.ts` 한 곳뿐이다:

```diff
-  it("409 도 명령마다 다르다 — 생성만 «그 날이 방금 찼다»이고 나머지는 회차 충돌이다", () => {
-    expect(denyMessage("schedule_create", 409, span)).toBe("이 날의 시간 배정이 방금 바뀌었습니다. …");
+  it("409 도 명령마다 다르다 — 생성은 «겹침»이고 나머지는 회차 충돌이다", () => {
+    expect(denyMessage("schedule_create", 409, span)).toBe("이미 다른 일정이 있는 시간입니다");
```

**약화가 아니다:**

- **같은 테스트의 다른 두 단언(`schedule_update`·`task_dates` → 회차 충돌)이 그대로다.**
  단언 수가 줄지 않았다.
- **값이 바뀐 근거가 실재한다** — K22 가 생성 경로에 **세 번째 409**(`TASK_SCHEDULE_OVERLAP`)를
  만들었고(SPEC §4 Case Matrix `:1052`), `DAY_TAKEN` 은 **K10 이후 정상 흐름에서 오지 않는다**
  (그 날에 배정이 있으면 화면이 처음부터 `PATCH` 를 부른다 — `CalendarPage.tsx:351`·`:366-368`).
  **워커가 그 추론을 `denyMessage` docstring 의 표로 적었다.**
- **한 건이 새로 붙었다** — 「겹침 문구에는 마침표가 없다」(`:180`).
  **서버 문자열과의 드리프트를 잡는 감시선**이다. 없앤 것보다 더 단단한 것을 놨다.
- **주석이 이력을 남긴다** — 「앞 판은 생성 409 를 «그 날이 방금 찼다»로 읽었는데…」.
  **조용히 바꾸지 않았다.**

### 나머지 여섯 — **전부 `−0`. 순수 추가**

`CalendarRail.test.tsx`(+95) · `CalendarInteractions.test.tsx`(+45) · `MyWorkPage.test.tsx`(+41) ·
`calendarModel.test.ts`(+30) · `MeetingEditModal.test.tsx`(+25) · `MeetingList.test.tsx`(+21).
**기존 `it` 블록을 건드린 자리가 하나도 없다**(diff 전문에서 `-` 줄 0개).

`calendarWrites.test.ts` 의 **`+2` 한 줄**(`MyWorkPage.test.tsx` 의 mock 줄과 같은 성격)도
import 추가일 뿐이다.

**새 테스트에 `expect(true)`·`skip(`·`todo(`·`as any`·`@ts-ignore`·빈 `catch {}` — 0건.**
(`MyWorkPage.test.tsx:290` 의 `as never` 는 **mock 반환 타입 캐스팅**이고 단언이 아니다.)

---

## ⑦ 1루프·FE-3 규율 회귀 — **0건**

| 규율 | 확인 | 결과 |
|---|---|---|
| `span_from`·`span_to` 로만 그린다 (K14) | `features/calendar/` 에서 `start_date`/`due_date` 전수 | **이번 diff 가 새로 만든 자리 0건.** 남은 자리는 FE-1·FE-2 검수가 통과시킨 그것들(카드의 말 1 · 손잡이 6)뿐 |
| 한 화면 = 한 요청 | `CalendarPage.tsx` 의 `range`→`reload`→effect 사슬 | **무변경.** 새로 든 `busySpans` 는 `useMemo([entries])` — **조회가 아니다** |
| 레일과 격자가 같은 범위 (K18) | `railScope`(`:190-195`) | **무변경** |
| 격자는 상태를 말하지 않는다 | `CalendarSegment`·`TimedBlock`·`EventBar`·`calendar.css` | **무변경.** 겹침이 배지·색을 만들지 않았다 |
| `api.ts` 밖 `fetch` | `grep -rn "fetch(" src/` | **0건** |
| **조용한 거절 0개** (§I) | 새 가드 둘 | **둘 다 `onError(taken)` 로 말한다**(`CalendarPage.tsx:358`·`:409`). 막고 침묵하는 자리가 없다 |

**거절의 순서도 맞다** — `dropSlot` 은 `meetingReadOnly` → `slotGuard`(기간 밖·기한 없음·담당 아님)
→ `overlapGuard` 순이다(`:341-361`). **더 근본적인 거절이 먼저 말한다.**

**`ignoreKey` 가 서버의 `ignore_schedule_id` 와 같은 자리다** —
드롭은 `standing ? schedule:${standing.schedule_id} : null`, 손잡이는 `block.key`.
둘 다 `timedBlocks` 의 키 형식(`schedule:<id>`)과 **정확히 같다.**
안 빼면 10:00–11:00 을 10:30 으로 옮기는 것이 자기와 겹쳐 거절된다 —
`calendarWrites.test.ts:213` 이 **뺐을 때와 안 뺐을 때를 나란히** 박는다.

**연타(E-14)가 겹침 오류를 띄우지 않는다** — 재조회 전 연타는 `standing` 이 아직 없어
**같은 멱등 키의 `POST`** 로 나가고(FE-2 의 `scheduleKey` 원장 그대로), 재조회 뒤 같은 날 재배정은
`standing` 이 잡혀 **자기 자신이 가드에서 빠진다.** 두 경로 모두 겹침 문구가 나올 길이 없다.

---

## ⑧ +25 테스트에 공회전 — **없다. 「겹침」을 단언하는 넷 전부 픽스처가 실제로 겹친다**

**BE-4 검수가 변이 검사로 잡았던 눈으로 좌표까지 따라갔다:**

| 테스트 | 픽스처가 정말 겹치나 | 확인 |
|---|---|---|
| `CalendarInteractions:288` 「겹치면 보내기 전에 말한다」 | **겹친다** | 회의 `m1` = `2027-03-04T01:00Z–02:00Z` = **서울 10:00–11:00**, `viewer_relation:"attendee"`·`status:"scheduled"` → **블록이 된다.** 드롭 `clientY 560` ÷ 56px × 60 = **600분 = 10:00** → `defaultSlot` 10:00–11:00. **정면 충돌** |
| `CalendarInteractions:296` 「경계는 겹침이 아니다」 | **안 겹친다(의도대로)** | `clientY 616` = **660분 = 11:00**. 회의가 11:00 에 끝난다 → 반열림이라 통과. **`createTaskSchedule` 이 실제로 나가는 것**까지 단언 |
| `CalendarInteractions:355` 「늘리다 옆 배정과 겹치면」 | **겹친다** | `s1` 10:00–11:30 의 끝을 `clientY 812` = **870분 = 14:30** 까지 → `s2`(14:00–15:00)와 겹침. **자기(`s1`)는 빠진다** |
| `CalendarInteractions:304` 「서버가 409 로 말하면 같은 문장」 | **가드는 안 걸린다** | 03-0**3** 에 떨어뜨린다 — **회의가 없는 날**이라 가드를 통과하고 **서버 mock 이 409** 를 낸다. **가드 경로와 409 경로를 실제로 갈라 놨다** |

**CalendarRail 쪽도 공회전이 없다:**

- `:122` 「회의만 있는 날에도 점이 찍힌다」 → 점 **2개**를 센다. `DayCell:247` 이
  `(dot || isToday)` 라 오늘(09-18)이 하나, 회의(09-19)가 하나다. **회의가 없으면 1이 된다** —
  값이 실제로 갈린다. 섹션 머리의 **`(1)`** 까지 같이 박는다.
- `:86` 「업무가 먼저, 회의는 시간순」 → 회의 **둘**(오전/오후)을 순서까지 본다.
- `:104` 「취소된 회의는 일정이 아니다」 → 「오늘 일정이 없습니다」로 **부재**를 박는다.

**`blockingBlocks` 다섯 건도 값이 갈린다** — `shared`·`cancelled` 는 `toEqual([])`,
`attendee` 는 `["meeting"]`, 탭 무관은 `["meeting","task"]`. **전부 다른 답이 나오는 입력**이다.

---

## ⑨ K30 을 화면이 약속하지 않나 — **약속하지 않는다**

DEC-003 증보 10 K30: 「**참석자를 나중에 추가하는 것은 겹침 검사를 지나지 않는다**」
(SPEC §2.9 가 드는 것이 「생성」과 「시각 변경」 둘이라 BE-4 가 그대로 구현했다).

- **이번 diff 가 참석자 추가 UI 를 한 줄도 건드리지 않았다** — `BookingModal.tsx`·
  `MeetingEditModal.tsx`·`AttachModal.tsx` 모두 **코드 변경 0**(테스트만 늘었다).
- **「충돌 없음」·「비어 있음」·「가능」을 뜻하는 새 문구가 0개다** — `labels.ts` 의 이번 추가는
  `calendarDeny.overlap` **한 줄**뿐이다.
- 화면은 **거절을 전달할 뿐** 겹침 없음을 주장하지 않는다.

**즉 화면이 K30 을 숨기지도, 반대로 약속하지도 않는다.**
**다만 사람 눈에는 「막히지 않았으니 괜찮다」로 읽힌다** — 사용자 E2E 목록에 올렸다(U-8).

---

## 위반 (FAIL 사유)

**없음.**

---

## 경미 (WARN) — 넷. **전부 사용자 E2E / 후속이지 재발주 사유가 아니다**

### WARN-1 — `overlapsMinutes` 에 **서버가 가진 「빈 구간」 가드가 없다**

- `frontend/src/features/calendar/calendarWrites.ts:108`
- **근거**: `backend/src/ax_workspace/modules/time_blocks.py:144-147` 이 같은 판정 앞에
  **한 줄을 더 갖는다** — `if one_from >= one_to or other_from >= other_to: return False`.
  그 docstring 이 이유를 적는다: 「**이미 저장된 회의 행은 `starts < ends` 보장을 받지 않는다** —
  검증은 새 쓰기에만 걸렸고 기존 데이터는 그대로 두므로(K22), **그런 행 하나가 남을 막지 않게 한다**」.

**무엇이 갈리나.** `starts_at == ends_at` 인 회의 행이 있으면 `timedBlocks` 가
`startMin === endMin` 인 칸을 만든다. 서버는 **그 칸을 겹침에서 제외**하는데 화면의 부등호는
`600 < 610 && 590 < 600` → **`true`** 를 낸다. **화면이 서버보다 엄해진다** —
브리프 §2 가 FAIL 로 지목한 바로 그 방향이다.
`ends_at < starts_at` 이고 날짜가 다른 행은 더 나쁘다: `timedBlocks:257` 이 `endMin = DAY_MINUTES`
로 잘라 **시작 시각부터 자정까지 통째로** 막는다.

**FAIL 로 올리지 않은 이유(판단 근거를 남긴다).**
① 계약이 지목한 경계(11:00)는 **정확히 맞다** — 갈리는 것은 **퇴화 데이터 한 갈래**다.
② 거는 쪽(`at`)은 절대 퇴화하지 않는다 — `defaultSlot` 은 60분이고 손잡이는
`CalendarPage.tsx:397` `if (ends_at <= starts_at)` 가 먼저 막는다. **블록 쪽에서만 난다.**
③ 새 쓰기로는 만들 수 없는 행이라 **데모·신규 환경에서는 나타나지 않는다.**
④ `overlapGuard` docstring 이 「**화면은 서버보다 엄하지 않다**」고 **적어 놓았는데** 이 한 갈래에서
그 문장이 참이 아니다 — **문장과 코드를 맞추는 편이 낫다.**

- **권장 수정(한 줄)**: `if (left.startMin >= left.endMin || right.startMin >= right.endMin) return false;`
- **FE-4 후속에 실을지**: **실어라.** 한 줄이고, 서버 쪽에 **이미 같은 줄이 있어 근거가 명확하다.**

### WARN-2 — 겹침 문구만 **마침표가 없고**, 그 근거가 코드와 어긋난다

- `frontend/src/lib/labels.ts:995` `overlap: "이미 다른 일정이 있는 시간입니다"`
- **근거**: WORK `Phase FE-4` 작업 1 과 E-12 가 「**이미 다른 일정이 있는 시간입니다.**」(마침표) ·
  SPEC §4 Case Matrix `:1052` 도 같다. 같은 객체의 **다른 여섯 문구가 전부 마침표로 끝난다**
  (`outOfRange`·`unscheduled`·`invalidRange`·`startAfterDue`·`notMine`·`versionConflict`·`notFound`).

**계약 위반은 아니다** — 두 문구 다 **`(제안 — 문구)`** 로 표시돼 있어 확정이 아니다.
**다만 워커가 적은 근거가 사실과 다르다**: docstring 이 「같은 거절을 화면이 **두 자리**(가드 · `409`)에서
말하므로 두 자리가 한 글자도 달라선 안 된다」고 하는데, **그 두 자리는 둘 다 `calendarDeny.overlap`
같은 상수를 쓴다**(`denyMessage:213` 이 서버 문자열이 아니라 **우리 상수**를 돌려준다).
마침표를 붙여도 두 자리는 여전히 같다. **실제로 유효한 근거는 다른 것**이다 —
회의 쪽 문장(「민아 님의 일정과 겹칩니다」, 서버가 만들고 마침표가 없다)과 **나란히 보일 때
한쪽만 마침표가 붙는 것이 어색하다.**

- **권장**: 코드를 그대로 두되 **근거 문장을 고치거나**, WORK·SPEC 의 예시에 맞춰 마침표를 붙이고
  서버 문자열도 함께 맞춘다. **둘 중 무엇이든 「우연히 같다」는 상태는 남기지 않는다.**
- **FE-4 후속에 실을지**: **사용자 E2E 에서 눈으로 보고 정한다**(U-1). 코드 위험은 없다.

### WARN-3 — **자정을 넘는 회의의 둘째 날**을 가드가 못 본다. 그 자리의 `409` 문구가 오해를 만든다

- `frontend/src/features/calendar/calendarModel.ts:255-257`(`timedBlocks`) ·
  `frontend/src/features/calendar/calendarWrites.ts:213`(`denyMessage`)
- **근거**: 서버는 **날짜별로 쪼갠다**(SPEC §2.9 「자정 넘는 회의는 **날짜별로 쪼개** 비교한다」 ·
  `modules/time_blocks.py:152-172` `split_across_office_dates`). 화면은 **시작 날 한 칸만** 만들고
  자정에서 자른다 — **둘째 날에는 블록이 없다.**

**덜 아는 방향이라 안전하다** — 워커도 그렇게 적었고 맞는 판단이다. **문제는 그 다음이다**:
서버가 `schedule_update` 에 `409 OVERLAP` 을 내면 화면은 **「다른 곳에서 먼저 바뀌었습니다.
새로고침 후 다시 시도해 주세요.」** 를 낸다(`409` 를 회차 충돌과 못 가르므로 — 워커가 의도한 설계다).
**새로고침해도 달라지는 것이 없어 같은 실패가 반복된다.**

**FAIL 이 아닌 이유**: 「가를 수 없는 것을 가른 척하지 않는다」는 `denyMessage` 의 판단이
**그 자체로는 옳고**(update 의 `409` 는 실제로 둘 다 가능하다), 자정을 넘는 회의는 드물다.

- **권장**: `timedBlocks` 가 자정 넘김을 둘째 날 칸으로도 내거나, 그게 그리기와 얽히면
  **겹침 전용으로만** 둘째 조각을 만든다(`blockingBlocks` 안에서).
- **FE-4 후속에 실을지**: **실어라** — 다만 WARN-1 보다 낮은 우선순위다.

### WARN-4 — `CalendarRail` 의 「회의」 배지가 **`labels.ts` 를 놔두고 인라인**이다

- `frontend/src/shell/CalendarRail.tsx:128` `<Badge tone="neutral">회의</Badge>`
- **근거**: `lib/labels.ts:932` 에 **`calendarScreen.meetingBadge: "회의"` 가 이미 있고**,
  **같은 뜻의 같은 배지**를 `features/calendar/ScheduleCard.tsx:64` 가 그것으로 낸다.
  reviewer `rules.md` frontend 「카피 — 한국어 문자열이 `labels.ts` 밖에 흩어지지 않았나」 ·
  「재사용 — `labels.ts` 를 놔두고 중복 구현하지 않았나」.

**같은 파일의 다른 한국어 인라인(`캘린더`·`오늘 일정이 없습니다`·`막힘 사유:` 등)은 지적하지 않는다** —
**`labels.ts` 에 짝이 없고 FE-4 이전부터 그 파일의 방식**이다(기존 부채).
**짝이 있는데 안 쓴 것은 이 한 줄뿐**이고, 워커가 바로 옆에서 `meetingScreen.noTitle` 은
제대로 재사용했다(`:134`) — **일관성의 문제다.**

- **권장 수정**: `{calendarScreen.meetingBadge}`
- **FE-4 후속에 실을지**: **한 줄이므로 후속에 실을 가치가 낮다.** 다음에 그 파일을 열 때 같이 고친다.

---

## 기존 부채 (이번 판정 제외)

- **`shell/CalendarRail.tsx` 의 한국어 문자열이 `labels.ts` 밖에 산다** — FE-4 이전부터다
  (`git show HEAD:` 로 대조: `오늘`·`주`·`월`·`캘린더`·`일정을 불러오는 중`·`막힘 사유:` 등).
  FE-4 가 더한 넷(`오늘 일정이 없습니다`·`이번 주에 일정이 없습니다`·`…에 일정이 없습니다`·
  `회의를 불러오지 못했습니다.`)은 **그 방식을 따른 것**이라 위반으로 세지 않는다.
  **그 파일을 `labels.ts` 로 옮기는 것은 별건이다.**
- **회의 조회 실패에 자동 재시도가 없다** — `MyWorkPage.tsx:934` 가 `railRange.current = ""` 로
  되돌리지만 `onRange` 를 다시 부르는 것은 **범위가 바뀔 때**뿐이다(`CalendarRail.tsx:169-171` 의
  effect deps 가 그대로라 재발화하지 않는다). **무한 재시도 루프가 없다는 뜻이기도 하다** —
  의도적이라면 맞고, 사람이 탭/주/월을 움직이면 다시 시도된다. **한 줄 주석이 있으면 좋겠다.**

---

## 확인한 것 (체크리스트 — 건너뛴 항목 없음)

- **envelope** — 이번 diff 에 `kind`·`status` 로 command·권한을 추론하는 코드 **0건**.
  겹침 판정은 **시각**으로만 하고 상태를 읽지 않는다.
- **호출 자리** — `api.ts` 밖 `fetch` **0건**. 새 API 함수 **0개**(`lib/api.ts` 무변경).
- **재사용** — 합본 조회·`meetingClock`(`labels.ts:853`, 기존 Asia/Seoul 헬퍼)·`meetingScreen.noTitle` ·
  `isoDateInSeoul` · `Badge` · `Empty` 를 그대로 썼다. **새 부품·새 조회 0개.**
  `timedBlocks` 를 복제하지 않고 `blockingBlocks` 가 **걸러서 넘긴다** — 규칙이 한 자리에 남는다.
  ⚠ 예외 한 줄이 WARN-4 다.
- **카피·스타일** — 새 hex 리터럴 **0건**. 새 CSS **0줄**(`calendar.css` 무변경).
  회의 줄은 `.scax-agenda-item` **기존 마크업**을 쓴다.
- **테스트** — 모델(`calendarWrites`·`calendarModel`) · 컴포넌트(`CalendarRail`) ·
  화면 통합(`CalendarInteractions`·`MyWorkPage`) · 다른 도메인의 경계(`MeetingList`·`MeetingEditModal`)
  **네 층 전부**에 옆자리 검사가 있다.
- **allowed_paths** — 18개 전부 `frontend/`. 이탈 **0건**.
- **BE 대조** — `overlaps`·`overlapping_blocks`·`_meeting_blocks`·`project_meeting_view`·
  `_calendar_row`·`board` span 분기 · `http.py` 의 `409` 직렬화 **여섯 자리를 읽어** 화면과 맞췄다.
- **테스트를 돌리지 않았다. 코드를 한 줄도 고치지 않았다.** 산출물은 이 리포트 하나.

---

## 🔴 **사용자가 실물에서 만날 자리** — 구현이 끝났으므로 여기부터가 남은 일이다

> **2루프가 이렇게 시작됐다** — K19·K20·K21 셋 다 **사용자가 실물에서 찾은 것**이었고
> 테스트는 전부 초록이었다. **아래는 자동 검증이 닿지 않는 자리만** 모았다.

### A. WORK 가 이미 올린 2루프 인계 (E-12 ~ E-20) — **그대로 수행한다**

| | 조작 | 기대 |
|---|---|---|
| E-12 | 이미 일정이 있는 시간에 배정을 놓는다 | 「이미 다른 일정이 있는 시간입니다」 |
| E-13 | 11:00 에 끝나는 일정 바로 뒤 11:00 에 놓는다 | **선다** |
| E-14 | 드래그 **연타** | 겹침 오류가 **안 뜬다** · 배정 하나 |
| E-15 | 참석자가 바쁜 시간에 회의를 잡는다 | 「민아 님의 일정과 겹칩니다」 — **무슨 일정인지는 안 나온다** |
| E-16 | 「바로 시작」 회의 | **막히지 않는다** |
| E-17 | 월 뷰 | 두 번 안 뜬다 · 회의는 보인다 · 시간순 |
| E-18 | 09:30–12:30 안의 10:00–11:00 회의 | **나란히** |
| E-19 | 승인 대기 업무의 좌측 카드 | 「완료」로만 읽히지 않는다 |
| E-20 | 업무 탭 → 「보낸 업무」 탭 | 회의가 보인다 · **보낸 업무가 안 사라진다** |

### B. 이번 검수가 **추가로** 올리는 것 — 코드가 통과시키는데 사람이 봐야 하는 자리

| | 무엇을 보나 | 왜 자동으로 못 잡나 | 나온 자리 |
|---|---|---|---|
| **U-1** | **거절 문구 셋을 나란히** 띄워 본다 — 기간 밖(마침표 있음) · 겹침(**마침표 없음**) · 담당 아님(마침표 있음) | 문장부호는 테스트가 「맞다」고 말해 줄 수 없다. **읽어 보고 어색한지**가 기준이다 | **WARN-2** |
| **U-2** | **시간 격자에서 같은 자리에 연타** — 재조회가 끝난 뒤 같은 날 같은 시각에 다시 놓는다 | 단위 테스트의 `getCalendar` mock 은 정적이라 **재조회 뒤 상태**를 재현하지 못한다. 실제로는 `PATCH` 로 간다 | ⑦ |
| **U-3** | **회의만 못 읽었을 때** — 네트워크를 끊고 업무 탭을 연다 | 「회의를 불러오지 못했습니다.」가 뜨고 **업무 목록은 그대로**여야 한다. **자동 재시도가 없으므로** 주/월을 눌러야 다시 시도된다 | 기존 부채 |
| **U-4** | **월 레일의 범위가 42칸**이라 달 밖 회의까지 받는다 — 9월을 보며 **8/30·10/10** 회의가 점으로 찍히는지 | 캘린더 **화면**은 K18 로 달 밖을 안 내는데 **레일은 낸다.** 둘이 다른 규칙인 것이 눈에 거슬리는지 | ④ |
| **U-5** | **우 레일의 줄 순서** — 기한 업무와 회의가 같은 날에 있을 때 **업무가 먼저** 서는 것이 읽히는지 | 「업무 먼저 · 회의 시간순」은 캘린더 화면 K20 과 맞춘 규칙이지만 **레일은 시각이 안 보이는 업무와 시각이 있는 회의가 섞인다** | ④ |
| **U-6** | **회의 줄을 눌러 본다** — 아무 일도 안 일어나는 것이 「고장」으로 읽히는지 | §2.4 대로 **읽기 전용**이 맞다. 다만 **누를 수 없다는 신호가 없어** 사람이 두 번 누를 수 있다 | ④ |
| **U-7** | **자정을 넘는 회의**가 있는 주에서, **그 다음 날 새벽**에 배정을 놓아 본다 | 화면 가드는 통과시키고 **서버가 거절**한다. 그때 문구가 「다른 곳에서 먼저 바뀌었습니다. 새로고침…」이라 **새로고침해도 안 풀린다** | **WARN-3** |
| **U-8** | **회의를 만든 뒤 바쁜 사람을 참석자로 추가**한다 | **막히지 않는다**(K30 — 의도된 현재 동작). 화면이 「충돌 없음」을 약속하진 않지만 **사람은 그렇게 읽는다.** 넓힐지는 계약 변경이다 | ⑨ |
| **U-9** | 「업무 만들기」를 캘린더 머리에서 눌러 본다 | FE-2 가 세운 것이라 **2루프 검수를 안 지났다.** 모달 필드 구성이 캘린더 맥락에서 말이 되는지 | ⑤ |

### C. 데이터가 있어야 보이는 자리 (데모 DB 에는 없을 수 있다)

- **길이 0 이거나 뒤집힌 회의 행**이 있으면 화면이 **서버보다 엄하게** 막는다(**WARN-1**).
  **새 쓰기로는 못 만드는 행**이라 기존 데이터가 있는 환경에서만 드러난다.
- **공유받기만 한 회의**가 캘린더에 서 있는데 **내 배정을 막지 않는 것**(K25)이 맞게 보이는지 —
  「보이는데 왜 안 막나」로 읽힐 수 있다. **계약대로다.**

---

## `git -C /Users/kknaks/orca/workspaces/Strong_hajin/strong-hajin-calendar status --short`

```text
 M frontend/src/features/calendar/CalendarInteractions.test.tsx
 M frontend/src/features/calendar/CalendarPage.tsx
 M frontend/src/features/calendar/calendarModel.test.ts
 M frontend/src/features/calendar/calendarModel.ts
 M frontend/src/features/calendar/calendarWrites.test.ts
 M frontend/src/features/calendar/calendarWrites.ts
 M frontend/src/features/meetings/MeetingEditModal.test.tsx
 M frontend/src/features/meetings/MeetingList.test.tsx
 M frontend/src/features/work/CreateWork.test.tsx
 M frontend/src/features/work/InboxRead.test.tsx
 M frontend/src/features/work/MyWorkPage.test.tsx
 M frontend/src/features/work/MyWorkPage.tsx
 M frontend/src/features/work/WorkRequestModalFlow.test.tsx
 M frontend/src/features/work/WorkRowCompletion.test.tsx
 M frontend/src/features/work/WorkTabsAndTables.test.tsx
 M frontend/src/lib/labels.ts
 M frontend/src/shell/CalendarRail.test.tsx
 M frontend/src/shell/CalendarRail.tsx
```

(검수 시작 시점과 **같다** — 읽기만 했다.)
