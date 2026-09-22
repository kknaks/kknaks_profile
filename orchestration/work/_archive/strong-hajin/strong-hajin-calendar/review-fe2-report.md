# 리뷰 리포트 — strong-hajin-calendar / Phase FE-2 코드 검수 (2026-09-21)

## 판정: **PASS**

**여덟 항목이 전부 통과했다.** 지적할 FAIL 도 WARN 도 없다.

계약이 가장 갈리기 쉬운 자리 셋이 **코드에서 정확히 닫혀 있다**:

- **정상 흐름에 `409` 가 없다** — 그 날에 배정이 있으면 `POST` 를 **아예 만들지 않고** 처음부터
  `PATCH` 로 간다(`CalendarPage.tsx:342-350`). 테스트가 `createTaskSchedule` **미호출**까지 박는다.
- **연타가 같은 멱등 키다** — 키 원장이 `useRef` 라 렌더를 타지 않고(`:135`),
  「업무·날·시각」이 같으면 같은 키가 나온다.
- **가드가 `span_from`·`span_to` 로만 판정한다** — 뒤집힌 업무를 `start_date` 로 막는 자리가 없다.

**워커가 신고한 「NaN:NaN」 가드는 진짜다.** 좌표를 읽는 자리 **셋 전부**가 한 함수를 지나고
그 함수가 `Number.isFinite` 로 막으며, 그 아래 `clock`·`snapClock`·`defaultSlot` 이 **각각 한 번 더**
막는다 — **세 겹**이다. 다른 자리에 같은 버그가 남아 있지 않다.

**기존 테스트를 약화시킨 자리도 없다.** 유일하게 손댄 기존 테스트의 변경은 **정당하고**,
그 테스트의 가장 센 단언(상태 클래스 다섯이 없다)은 **손대지 않았다.**

---

## 검수 범위

FE-1 커밋 `c5b109d` **위의 uncommitted diff** — 수정 10 · 신규 3, **전부 `frontend/`**, 717 insertions.
**테스트는 돌리지 않았다**(지시). **코드도 한 줄 고치지 않았다.**
코디가 확인한 것(`frontend/` 밖 0건 · 914통과 · `tsc` exit 0 · `make verify` exit 2 는 기존 flaky)은
다시 세지 않았다.

---

## ① 정상 흐름에 `409` 가 없는가 (K10) — **없다**

`CalendarPage.tsx:342-350` 이 전부다:

```ts
const standing = row.schedules.find((schedule) => schedule.on_date === date);
…
if (standing) {
  await updateTaskSchedule(standing.schedule_id, standing.version, slot);   // :347
} else {
  await createTaskSchedule(row.task_id, { on_date: date, ...slot }, scheduleKey(…));  // :349
}
```

- **`createTaskSchedule` 호출은 문서 전체에서 `:349` 하나**뿐이고 `else` 안에 있다(`grep` 확인).
  **그 날이 차 있을 때 `POST` 가 나갈 길이 없다.**
- 쓰는 값이 **합본 조회가 준 것**이다 — `standing.schedule_id` · `standing.version`(K8).
- 테스트가 양쪽을 박는다 — `CalendarInteractions.test.tsx:258`:
  기배정 `s1`/version 4 를 세워 두고 그 날에 떨어뜨리면
  `expect(updateTaskSchedule).toHaveBeenCalledWith("s1", 4, {…})` **그리고**
  `expect(createTaskSchedule).not.toHaveBeenCalled()`.

---

## ② 연타가 같은 멱등 키인가 (K12) — **그렇다**

- 원장이 **`useRef`** 다 — `CalendarPage.tsx:135` `const scheduleKeys = useRef(new Map<string,string>())`.
  렌더마다 새로 만들어지지 않는다. **여기가 틀리면 K12 가 통째로 무너지는 자리**인데 맞게 잡았다.
- `calendarWrites.ts:135-146` `scheduleKey` 가 `taskId|on_date|starts_at|ends_at` 로 캐시한다 —
  **같은 제출 의도면 같은 키, 내용이 다르면 다른 키**. 뒤엣것도 맞다: 다음 배정이 앞엣것의 영수증이
  되면 안 된다.
- **키를 매번 새로 만드는 자리가 없다** — `createIdempotencyKey()` 를 부르는 곳은 `scheduleKey` 안뿐이다.
- 검사가 실제로 박는다 — `CalendarInteractions.test.tsx:249` 가 두 번 떨어뜨린 뒤
  `calls[1][2] === calls[0][2]` 를 단언하고, `calendarWrites.test.ts:133`·`:140` 이 같은·다른 내용을 가른다.

---

## ③ `expected_version` 이 배정 회차인가 (K8) — **그렇다**

- `:347` `updateTaskSchedule(standing.schedule_id, **standing.version**, …)` — `schedules[]` 원소의 회차.
- `:385` `updateTaskSchedule(block.scheduleId!, **block.version!**, …)` — `TimedBlock` 이 실어 온 배정 회차.
- **업무 회차를 배정 명령에 보내는 자리가 없다.** `row.version` 은 `updateTask`(업무 명령)에만 간다.
- 테스트가 숫자로 박는다 — `:258` 이 「업무 회차(7)가 아니다」라는 주석과 함께 `4` 를 단언하고,
  `:307` 이 `("s1", 4, …)` 를 단언한다.

---

## ④ 가드가 `span_from`·`span_to` 로만 판정하는가 (K14) — **그렇다**

- `calendarWrites.ts:32-34` `spanOf(row)` 가 **`span_from`/`span_to` 만** 읽는다.
- `:94-100` `slotGuard` 가 그 값으로 기간 밖을 판정한다. **`start_date`/`due_date` 로 막는 자리가 없다.**
- `:46-55` `moveTaskDates` 의 「길이」도 **span 길이**다(WARN-A 대로).
- `ghostAt`(`CalendarPage.tsx`)도 같은 `slotGuard` 를 쓴다 — **그림과 거절이 한 규칙**이다.
- 원본 두 날짜가 쓰이는 곳은 **손잡이 셋**뿐이고 그것이 맞다 —
  `:71-78` `resizeTaskDates` 는 **필드를 쓰는 명령**이라(WARN-A: 손잡이의 정체는 필드)
  역전 판정도 서버의 `validate_schedule` 과 같은 raw 비교여야 한다.
- 테스트 `calendarWrites.test.ts:92` 「기간 안이면 통과한다 — **뒤집힌 업무도 `start_date` 로 막지 않는다**」.

---

## ⑤ 세로 손잡이 · 회의 블록 — **놓을 때 한 번. 회의엔 없다**

**놓을 때 한 번만** — `WeekGrid.tsx:110-128`. `pointermove` 는 **로컬 state 만** 바꾸고(미리보기),
`:115` `up` 에서만 `onResizeSlot?.(…)` 을 부른다. `CalendarPage` 의 `resizeSlot` 은
「끌지 않은 쪽은 **서버가 준 문자열 그대로**」까지 지킨다 — 다시 눈금에 접으면 `23:59` 가 조용히 바뀐다.
테스트 `:307` 이 **pointermove 둘 뒤 `not.toHaveBeenCalled()`** → pointerup 뒤 **`toHaveBeenCalledTimes(1)`** 로 박는다.

**회의 블록에 손잡이가 없다 (§F)** — 세 겹으로 막혀 있다:

| 자리 | 조건 |
|---|---|
| `WeekGrid.tsx:254` | `Boolean(onResizeSlot) && block.scheduleId !== null` — 회의 블록은 `scheduleId: null` |
| `EventBar.tsx:35` | `Boolean(onGrab) && segment.kind === "task" && segment.time === null && segment.taskId !== null` |
| `ScheduleRail.tsx:75` | `onDragStart={card.kind === "task" ? onDragStart : undefined}` → `ScheduleCard.tsx:32` `draggable = Boolean(onDragStart)` = **false** |

테스트 `:329` 가 회의 블록 손잡이 **0개**, 업무 블록 **정확히 2개**를 단언하고,
`:340`·`:347` 이 회의 카드·회의 띠를 각각 박는다.

---

## ⑥ 조용한 거절 0개 · 영문 누수 없음 — **그렇다**

네 거절이 전부 **우리 한국어 문구**를 낸다(`labels.ts` `calendarDeny`):

| 거절 | 문구 | 어디서 |
|---|---|---|
| 기간 밖 | 「이 업무의 기간(…) 안에만 …」 — **정규화 구간**을 적는다 | `slotGuard` → `outOfRange(span.from, span.to)` |
| 기한 없음 | 「먼저 업무 기간을 정해 주세요 …」 | `slotGuard` → `unscheduled` |
| 역전 | 「종료 시각은 시작 시각보다 뒤여야 합니다.」 / 「시작일은 마감일보다 뒤일 수 없습니다.」 | `resizeSlot` · `resizeTaskDates` |
| 담당 아님 | 「내가 맡은 업무에만 …」 | `dropGuard`·`slotGuard` → `notMine` |

- **서버 문구가 새지 않는다** — 쓰기 실패는 전부 `deny()` → `denyMessage(command, status, span)`
  (`calendarWrites.ts:158-168`)를 지나고, 그 함수는 **상태 코드 + 명령**으로만 고른다.
  `error.detail` 을 화면에 올리는 자리가 쓰기 경로에 **없다** — 영문인
  `WORK_SCHEDULE_START_AFTER_DUE` 가 그대로 뜰 길이 막혀 있다.
- **못 놓는 자리에서도 `preventDefault` 를 부른다**(`WeekGrid` `onDragOver` · `MonthGrid` 주석) —
  시안처럼 브라우저가 조용히 튕기게 두지 않는다. 거절은 **받고 나서 말로** 한다.
- 테스트 — `:271`(기간 밖, **아무것도 안 보냄**) · `:278`(기한 없음) · `:165`(담당 아님) ·
  `:201`·`:319`(역전) · `:285`(서버 거절 → 우리 문구) · `calendarWrites.test.ts:156`
  「**서버의 영문 문구를 그대로 내보내지 않는다**」.

---

## ⑦ K3 알림 — **첫 응답만 읽고, 0건이면 말하지 않으며, `undefined` 를 만지지 않는다**

- `releaseNotice`(`calendarWrites.ts:177-180`)가 `if (!release || release.released_count <= 0) return null`
  — **없어도 0이어도 침묵** ✓
- 타입이 그것을 보장한다 — `viewModels.ts:213-217` `schedule_release?: ScheduleRelease | null`
  **옵셔널**이고, docstring 이 싣는 표면 셋과 **안 싣는 넷(`/block`·`/resume`·`/complete`·`/cancel`)**
  을 이름으로 적는다. **`undefined` 를 만지는 자리가 없다.**
- **첫 응답만 읽는다** — `announce` 호출은 둘뿐이고(`:243` 격자 드롭·손잡이, `:532` 상세 서랍 저장)
  **둘 다 `updateTask` 의 반환값**이다. 영수증을 읽는 자리가 없다.
- **제안 재전송 영수증 문제는 이 화면에 없다** — 캘린더는 제안 응답을 부르지 않는다
  (`schedule_release` 참조가 `:228` 하나뿐).
- **상세 서랍의 날짜 수정도 알린다** — `:532` 가 `announce` 를 부르고 docstring 이 이유를 적는다
  (「여기서도 날짜가 바뀔 수 있으므로」). 격자만 챙기고 서랍을 빠뜨리지 않았다.
- 테스트 `:355`(건수 있으면 말함) · `:364`(0건이면 침묵) · `:371`(**칸이 아예 없는 응답**에서도 침묵).

> 상태 전이(`transition`)는 `announce` 를 안 부른다. **맞다** — 날짜를 바꾸는 전이는 `/start` 뿐이고
> BE-2 검수에서 확인했듯 그 자리의 `released_count` 는 **구조적으로 항상 0** 이라 할 말이 없다.

---

## ⑧ 조용히 통과하는 자리 — **없다.** NaN 가드는 진짜고, 남은 자리도 없다

### 「NaN:NaN」 가드 — 진짜다. 세 겹이다

**원인이 실재한다** — 좌표가 없는 이벤트(합성 이벤트·보조기술)에서 `event.clientY` 가 `undefined` 면
`(undefined - box.top) / WEEK_ROW * 60` 이 `NaN` 이고, 그대로 가면 `"NaN:NaN"` 이 서버에 닿아 **422** 다.

**막는 자리**:

| 겹 | 자리 |
|---|---|
| 1 — 좌표를 읽자마자 | `WeekGrid.tsx:27-33` `minutesAt` 의 `if (!Number.isFinite(raw)) return 0;` |
| 2 — 문자열로 바꾸기 직전 | `calendarWrites.ts:108-113` `clock()` 의 `Number.isFinite(minutes) ? minutes : 0` |
| 3 — 두 진입점 | `:103-106` `snapClock` · `:122-126` `defaultSlot` 이 각각 한 번 더 |

**다른 자리에 남아 있지 않다** — 좌표를 읽는 곳을 전수로 셌다(`grep clientY|clientX|getBoundingClientRect`):
`WeekGrid.tsx:114`·`:230`·`:234` 셋이 **전부 `minutesAt` 을 지나고**,
`CalendarPage.tsx:303` 의 `document.elementFromPoint(clientX, clientY)` 는 NaN 이면 `null` 을 내며
`?.closest?.()` 로 **옵셔널 체이닝**이 이어져 `date` 가 falsy → 아무 일도 안 일어난다.
검사도 있다 — `calendarWrites.test.ts:226` 「유한하지 않은 분은 0 시로 읽는다 — **그대로 보내면 422 다**」.

### 기존 테스트 약화 — **없다**

손댄 기존 테스트는 **`CalendarPage.test.tsx` 하나(+10/-3)** 뿐이고 셋 다 정당하다:

1. `vi.mock("../../lib/api", …)` 에 **`importOriginal()` 스프레드를 더했다** — 컴포넌트가 이제
   `ApiError`·후보 조회 셋을 import 하므로 **없으면 `undefined` 가 된다.**
   실제 모듈을 **더 많이** 드러내는 변경이라 약화의 반대다.
2. Harness 에 새 prop 둘 추가 — 타입이 요구한다.
3. 상태 색 단언의 제외 목록에 `"scax-event--resizable"` 추가.
   **이것이 유일하게 판단이 필요한 자리인데, 약화가 아니다:**
   - 그 단언은 여전히 **「유형 클래스 집합이 정확히 `[meeting, task]` 」** 를 박는다.
   - `resizable` 은 상태가 아니다 — `Boolean(onGrab) && …`(`EventBar.tsx:35`)로 **핸들러 유무**가 정하지
     업무 상태가 정하지 않는다. FE-2 가 정당하게 더한 **수식어**다.
   - **가장 센 단언은 손대지 않았다** — 바로 아래
     `for (const state of ["open","in_progress","blocked","done","cancelled"]) expect(…).toBeNull()`
     루프가 **그대로** 돈다.

### 그 밖

- 새 코드·새 테스트에 `expect(true)`·`skip(`·`todo(`·`as any`·`@ts-ignore`·빈 `catch {}` 가 **0건**이다.
- 새 검사가 실질적이다 — `calendarWrites.test.ts` **33건**(값 단위) ·
  `CalendarInteractions.test.tsx` **19건**(실제 DOM·실제 API 목). 표본으로 읽은 넷
  (K10·K12·R6 한 번만·회의 손잡이 없음)이 전부 **부정 단언까지** 갖는다 —
  「보냈다」만 보고 「안 보냈다」를 빠뜨린 자리가 없다.

---

## 사용자 E2E · 2루프에서 볼 것 (지적 아님 — 관찰)

계약에 어긋나는 것이 아니라 **브라우저에서 눈으로 볼 자리**다. 셋 다 이번 판에서 고칠 것이 아니다.

1. **세로 손잡이의 끝은 `23:30` 까지만 간다.** `snapClock` 이 30분 눈금으로 접고 상한이
   `24:00 - 30분` 이다(`calendarWrites.ts:105`). 반면 `defaultSlot` 은 하루 끝에 떨어뜨리면
   **`23:59`** 로 붙는다(`:125` — 서버 `Time` 이 자정을 표현 못 하므로 옳다).
   그래서 **`23:59` 로 끝나는 배정의 끝을 손잡이로 다시 `23:59` 로 되돌릴 수 없다**(23:30 까지).
   눈금 규칙의 자연스러운 결과이고 계약 위반이 아니다 — **써 보고 불편한지만 본다.**
2. **입력 모델이 둘이다** — 카드→격자는 HTML5 드래그앤드롭(`dataTransfer`), 손잡이는 Pointer 이벤트다.
   **터치·보조기술 경로**는 자동 검증이 닿지 않는 자리라 E2E 가 본다.
3. **픽셀·간격·문구·시안 대조** — WP 가 이미 2루프로 보낸 항목 그대로다
   (「1루프는 계약을 세우는 판이다」).

> BE-2 검수가 넘긴 FE 쪽 WARN(「제안 재전송 영수증으로 알림을 만들지 마라」)은
> **이 화면에서 해당 사항이 없다** — 캘린더는 제안 응답을 부르지 않는다.

---

## 확인한 것 (근거)

- **①** `createTaskSchedule` 호출 자리를 `grep` 으로 전수(하나)하고 `if (standing)` 분기를 읽었다.
  테스트 `:258` 의 부정 단언까지 확인했다.
- **②** `useRef` 로 원장이 렌더를 안 타는 것과 `scheduleKey` 의 캐시 키를 읽었고,
  `createIdempotencyKey()` 호출이 그 안뿐임을 확인했다.
- **③** 두 `updateTaskSchedule` 호출의 두 번째 인자를 각각 확인하고, 테스트의 숫자 단언을 읽었다.
- **④** `spanOf`·`slotGuard`·`moveTaskDates` 를 읽고, 원본 두 날짜가 **손잡이에만** 쓰이는 것과
  그것이 WARN-A 대로인 것을 확인했다.
- **⑤** `pointermove` 가 로컬 state 만 바꾸고 `up` 에서만 콜백이 나가는 것을 읽었고,
  회의 배제 조건 **세 자리**를 각각 확인했다.
- **⑥** `calendarDeny` 전문을 읽고, `denyMessage` 가 상태+명령으로만 고르는 것과
  쓰기 경로에 `error.detail` 이 없는 것을 확인했다.
- **⑦** `releaseNotice` 의 가드, 타입의 옵셔널, `announce` 호출 **둘** 모두 첫 응답인 것,
  제안 경로가 없는 것을 확인했다.
- **⑧** 좌표를 읽는 자리를 `grep` 으로 전수(넷)하고 각각의 가드를 확인했다.
  기존 테스트 diff 세 덩어리를 각각 판정했고, 가장 센 단언이 그대로인 것을 확인했다.
- **테스트를 돌리지 않았다. 코드를 한 줄도 고치지 않았다.** 산출물은 이 리포트 하나.

---

## `git -C /Users/kknaks/orca/workspaces/Strong_hajin/strong-hajin-calendar status --short`

```text
 M frontend/src/App.tsx
 M frontend/src/features/calendar/CalendarPage.test.tsx
 M frontend/src/features/calendar/CalendarPage.tsx
 M frontend/src/features/calendar/EventBar.tsx
 M frontend/src/features/calendar/MonthGrid.tsx
 M frontend/src/features/calendar/ScheduleCard.tsx
 M frontend/src/features/calendar/ScheduleRail.tsx
 M frontend/src/features/calendar/WeekGrid.tsx
 M frontend/src/lib/labels.ts
 M frontend/src/lib/viewModels.ts
?? frontend/src/features/calendar/CalendarInteractions.test.tsx
?? frontend/src/features/calendar/calendarWrites.test.ts
?? frontend/src/features/calendar/calendarWrites.ts
```

(검수 시작 시점과 **같다** — 읽기만 했다.)
