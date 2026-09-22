# WORK-004 Phase FE-2 결과 보고 — 상호작용 넷 · 금지 문구 · K17

## 상태: done

- 워크트리 `/Users/kknaks/orca/workspaces/Strong_hajin/strong-hajin-calendar`, 브랜치 `kknaksss/strong-hajin-calendar`
- base 는 `c5b109d`(FE-1) 그대로다. **커밋·push 하지 않았다** — 변경은 전부 uncommitted 다.
- `allowed_paths` 준수 — 고친 파일 **13개 전부가 `frontend/`** 아래다. `backend/`·`docs/`·`para/` **0건**.

---

## 1. 변경 파일 (수정 10 · 신규 3)

### 신규

| 파일 | 줄 | 무엇 |
|---|---|---|
| `frontend/src/features/calendar/calendarWrites.ts` | 236 | **쓰기를 만드는 계산 전부** — 순수 함수. 가드·패치 모양·눈금·멱등 키·거절 문구 고르기·K3 알림 |
| `frontend/src/features/calendar/calendarWrites.test.ts` | 227 | 위의 값 단위 검사 **34건** |
| `frontend/src/features/calendar/CalendarInteractions.test.tsx` | 305 | 상호작용 넷이 **실제 API 를 부르는지** 화면 단위로 박는 검사 **23건** |

### 수정

| 파일 | diff | 무엇 |
|---|---|---|
| `features/calendar/CalendarPage.tsx` | +343/-25 | 쓰기 다섯 자리(`saveDates`·`dropTask`·`commitGrab`·`dropSlot`·`resizeSlot`) · 손잡이 포인터 추적 · K3 알림 · K17 머리 단추와 기존 생성 모달 |
| `features/calendar/WeekGrid.tsx` | +149/-29 | 종일 칸 드롭 · 종일 띠 손잡이 · 시간 격자 드롭과 **고스트** · 시간 블록 **세로 손잡이**(놓을 때 한 번) |
| `features/calendar/MonthGrid.tsx` | +45/-6 | 날짜 칸 드롭 · 띠 손잡이 · 받는 자리 표시 |
| `features/calendar/EventBar.tsx` | +37/-8 | `EventHandle` 신설 — 띠의 좌우 손잡이 |
| `features/calendar/ScheduleCard.tsx` | +30/-3 | 업무 카드가 **끌린다**(`--draggable`). 회의 카드는 안 끌린다 |
| `features/calendar/ScheduleRail.tsx` | +9/-1 | 끌기 시작을 위로 올린다 |
| `lib/labels.ts` | +50/-0 | `calendarDone`(성공·K3) · `calendarDeny`(거절 12종) · 손잡이 툴팁·「업무 만들기」 |
| `lib/viewModels.ts` | +8/-0 | `DirectTask.schedule_release` **additive** |
| `App.tsx` | +6/-1 | 캘린더에 `onRegisterHeaderActions` 를 넘긴다 (K17) |
| `features/calendar/CalendarPage.test.tsx` | +8/-5 | 새 prop 둘 + 유형 클래스 허용 목록에 `--resizable` 한 줄. **단언을 지우거나 약화하지 않았다** |

---

## 2. 구현 요약 — 작업 1~9

| # | 무엇 | 어디로 나가나 |
|---|---|---|
| 1 | **R1 · 날짜 칸 드롭** = 기간 이동 | `PATCH /api/tasks/{id}` |
| 2 | **R3 · 좌우 손잡이** = 시작·마감일 조정 | 같은 명령 |
| 3 | **R4 · 마감만 있던 업무**가 손잡이로 기간을 갖는다 | 같은 명령(`start_date` 가 채워진다) |
| 4 | **R5 · 시간 격자 드롭** = 배정 생성 | `POST …/schedules` **또는** `PATCH /api/task-schedules/{id}` (아래 K10) |
| 5 | **R6 · 세로 손잡이** = 시각 조정 | `PATCH /api/task-schedules/{id}` — **놓을 때 한 번만** |
| 6 | **금지는 말로** | 서버로 안 나간다. 문구는 우리 것 |
| 7 | **K3 알림** | `PATCH /api/tasks` 응답의 `schedule_release` |
| 8 | **K17 · 「업무 만들기」 단추** | 기존 `CreateWorkModal` 을 연다 |
| 9 | **WARN-A** | 아래 §4 — 정해진 한 줄을 그대로 구현했다 |

### 틀리기 쉬운 여섯 자리 — 하나씩

1. **같은 날 재배정은 `POST` 가 아니라 `PATCH`** (K10·K1).
   `dropSlot` 이 `row.schedules.find(s => s.on_date === date)` 로 먼저 본다. 있으면
   그 `schedule_id`·`version` 으로 **곧바로 `PATCH`** 다. 검사가 「`createTaskSchedule` 이 **안** 불린다」까지 박는다.
   **정상 흐름에서 `409` 를 보는 자리가 없다.**
2. **연타는 같은 멱등 키** (K12). 키 원장은 `useRef(new Map())` 이고 키의 유효 범위는
   **「이 업무의 이 날 이 시각」이라는 한 제출 의도**다(`scheduleKey`). 같은 자리에 두 번 떨어뜨리면
   **같은 키**가 나가고(검사가 `calls[1][2] === calls[0][2]` 로 박는다), 내용이 달라지면 다른 키다 —
   다음 배정이 앞엣것의 영수증이 되면 안 되기 때문이다.
   `201` 과 영수증 `200` 은 본문이 같으므로 **화면은 둘을 구분하지 않는다** — 어느 쪽이든 다시 읽는다.
3. **`PATCH` 의 `expected_version` 은 그 배정 자신의 회차** (K8).
   `dropSlot` 은 `schedules[].version`, `resizeSlot` 은 `block.version` 을 쓴다.
   검사가 「업무 회차 7 이 아니라 배정 회차 4」를 명시적으로 박는다.
4. **가드는 `span_from`·`span_to`** (K14). `slotGuard`·`spanOf` 가 그것만 본다.
   원본 `start_date`/`due_date` 가 코드로 닿는 자리는 **손잡이의 역전 판정 두 줄과 카드의 말** 뿐이고,
   그 둘은 **필드가 대상이라서** 원본을 봐야 하는 자리다.
   검사: 뒤집힌 업무(시작 3/5 · 마감 3/3 · span 3/3~3/5)에서 **3/5 에 떨어뜨리는 것이 통과**한다.
5. **세로 손잡이는 놓을 때 한 번만.** 끄는 동안 `WeekGrid` 가 자기 상태로 **미리 그려 보여 줄 뿐**이고,
   `pointerup` 에서 한 번 위로 올린다. 검사가 「`pointermove` 두 번 뒤에도 **아직 0회**, `pointerup` 뒤 **1회**」를 박는다.
   **회의 블록에는 손잡이를 붙이지 않는다**(§F) — 검사가 회의 블록 0개 · 업무 블록 2개를 센다.
6. **에러 본문에 `code` 가 없다.** `denyMessage(command, status, span)` 이
   **상태 코드 + 어떤 명령을 불렀는지**로 고른다. 서버 문구를 그대로 뿌리는 자리가 **0개**다 —
   `WORK_SCHEDULE_START_AFTER_DUE` 의 영문도 우리 한국어로 덮인다.

### 좌우 손잡이를 놓을 때까지 보내지 않는 이유

`pointerdown` → `document.elementFromPoint` 로 포인터가 지나는 `[data-date]` 를 읽어 **그림만** 바꾸고
(`previewResize`), `pointerup` 에서 한 번 `PATCH` 한다. 모든 쓰기가 낙관적 잠금이라 끌 때마다 부르면
**회차가 매번 어긋난다** — 세로 손잡이에 SPEC 이 명시한 이유(§2.3 R6)가 가로에도 그대로 적용된다.

---

## 3. 조용한 거절 0개 (§I) — **넷 전부 문구가 난다**

| 거절 | 문구 | 어디서 |
|---|---|---|
| **기간 밖** | 「이 업무의 기간(2027/03/03~2027/03/05) 안에만 시간을 배정할 수 있습니다.」 | `slotGuard` — **정규화 구간**을 넣는다(K11·K14). 뒤집힌 업무면 원본 두 날짜가 아니다 |
| **기한 없음** | 「먼저 업무 기간을 정해 주세요. 기간이 있어야 시간을 배정할 수 있습니다.」 | `slotGuard` (R2) |
| **역전** | 「시작일은 마감일보다 뒤일 수 없습니다.」 · 「종료 시각은 시작 시각보다 뒤여야 합니다.」 | `resizeTaskDates` · `resizeSlot` |
| **담당 아님** | 「내가 맡은 업무에만 시간을 배정할 수 있습니다.」 | `dropGuard`·`slotGuard` + 서버 `403` |

**시안과 갈리는 자리 둘 — 둘 다 「말하려고」 그렇게 했다.**

- `onDragOver` 가 **언제나** `preventDefault` 를 부른다. 시안은 `canDrop` 이 거짓이면 안 불러
  **브라우저가 말없이 막는다**(`week.jsx:205`). 우리는 **받아 놓고 이유를 말한다.**
- **업무 카드는 「할 수 없을 때도」 끌린다.** 끌 수 없게 막으면 말할 자리가 사라진다.
  칸반 선례(`WorkViews.tsx:553` `draggable={canManage && !busy}`)와 다른 쪽을 골랐고, 이유는 §I 다.
  **회의 카드는 끌리지 않는다** — 그쪽은 「권한」이 아니라 **계약**이다(§F, 캘린더는 회의에 쓰기를 내지 않는다).

고스트는 **놓을 수 있는 자리에만** 뜬다(§2.3 R5 — `ghostAt`). 그래도 **받기는 어디서나 받는다.**

---

## 4. 작업 9 — WARN-A. **다시 정하지 않았다**

지시서에 이미 적힌 한 줄을 그대로 구현했다:

> **뒤집힌 업무에서도 `start` 손잡이는 `start_date` 를, `end` 손잡이는 `due_date` 를 쓴다.**
> **R1 의 「길이」는 span 길이**(`span_to - span_from`)다.

- 코드: `resizeTaskDates(row, edge, date)` 가 `edge` → 필드로 곧바로 간다.
  `moveTaskDates` 의 길이는 `dayDifference(span.from, span.to)` 다 — raw 차이가 아니다.
- 검사(값): 「뒤집힌 업무에서도 start 손잡이는 start_date 를 바꾼다」 · 「span 길이(2일)로 옮겨지고 **결과는 뒤집히지 않는다**」.
- 검사(화면): 뒤집힌 업무에서 `.scax-event__handle--start` 를 끌면 `updateTask("flip", 7, {start_date: …})` 가 나간다.

**한 가지 도출을 적어 둔다** — 옮긴 결과는 **언제나 뒤집히지 않은 같은 길이의 기간**이다.
뒤집힌 채로 옮기면 `validate_schedule` 이 거절하므로 선택지가 없다.

---

## 5. K3 알림 — 조건 둘 다 지켰다

- `releaseNotice(release)` 가 `released_count <= 0` 이면 **`null`** 이다. 칸 자체가 없는 응답(`undefined`)도 같다.
- **알림은 첫 응답으로만 만든다** — 화면이 읽는 자리는 `updateTask` 의 **반환값 한 번**뿐이고,
  영수증을 다시 읽어 알림을 만드는 경로가 없다.
- **`/block`·`/resume`·`/complete`·`/cancel` 에서 이 칸을 읽지 않는다.**
  `transitionDirectTask` 는 지금도 `Promise<void>` 이고 **시그니처를 바꾸지 않았다**(§7-2 참조).
- 검사 3건: 2건이면 성공 문장에 이어 말하고, 0건이면 「해제」라는 말 자체가 안 나오고, 칸이 없어도 안 나온다.

---

## 6. 검증 결과 (수치)

| 명령 | 결과 |
|---|---|
| `make frontend-test` (Node 20.20.0) | **69 파일 / 914 통과 / 0 실패** (FE-1 기준선 67/857 → **+2 파일 · +57 건**) |
| `cd frontend && npx tsc --noEmit` | **exit 0** |
| `make test-scale` | **13 passed** / 0 failed |
| `make test-release` | **1 passed** / 0 failed |
| `make frontend-assets` | **exit 0** (자산 9개 검증) |
| `make frontend-build` | **exit 0** (`✓ built`) |
| `make test-postgres POSTGRES_TEST_URL=…/ax_test_calendar` | **89 passed / 0 failed** (기준선 89p 재통과) |
| `make verify` (한 명령) | **exit 2** — 아래 |

### `make verify` 의 exit 2 는 **기존 flaky 둘**이다. 무관으로 분리한다

**두 번 돌렸다.**

| 회차 | 결과 |
|---|---|
| 1회차 | `3 failed, 1472 passed` — `material_worker_recovery` **2건** + `test_material_search.py::test_searching_without_naming_the_work_finds_what_this_person_may_read` 1건 |
| 2회차 | `2 failed, 1473 passed` — **`material_worker_recovery` 2건만** |

- `material_worker_recovery` 2건은 **브리프가 「기존 flaky」로 미리 지정한 그 둘**이다.
  실패 모양이 타이밍이다 — `assert ['failed','running'] == ['failed','completed']`.
- `test_material_search` 1건은 **1회차에만** 났고 `make test-contract` 재실행과 `make verify` 2회차에서
  **둘 다 통과**했다. 같은 성질(병렬 실행 간섭)로 읽는다.
- **셋 다 백엔드다.** 이번 diff 는 **`frontend/` 밖이 0건**이라 인과가 성립하지 않는다.
- `make verify` 는 `test` 에서 멈추므로 **나머지 다섯 타겟을 각각 돌려 전부 통과**를 확인했다(위 표).

> **정직하게 적는다 — 「최종 `make verify` 통과」를 한 명령의 exit 0 으로는 보이지 못했다.**
> 막는 것은 **미리 지정된 기존 flaky 둘**이고, 구성 타겟은 **전부 통과**한다.

---

## 7. 계약 준수 · 범위

### 지킨 것

- **`api.ts` 밖 `fetch` 0건.** 쓰기 넷이 전부 `lib/api.ts` 의 함수를 부른다.
- **목데이터가 아니다** — 상호작용 넷이 각각 `updateTask` · `createTaskSchedule` · `updateTaskSchedule` 을
  부르는 것을 화면 단위 검사가 **인자까지** 박는다.
- **백엔드 0건 · 커밋·push·PR 0건.**
- **계약을 다시 정하지 않았다.** 모순을 발견한 자리도 없다.
- **기존 테스트를 지우거나 약화하지 않았다** — 손댄 기존 테스트는 `CalendarPage.test.tsx` 하나이고
  **새 prop 둘 + 유형 클래스 허용 목록에 `--resizable` 한 줄**이다. 상태 클래스 부재 단언은 그대로다.

### 찾은 것 하나 — **`"NaN:NaN"` 이 서버로 나갈 수 있었다**

좌표가 없는 포인터 이벤트(합성 이벤트 · 보조기술이 만든 것)에서 `clientY` 가 `undefined` 면
`minutesAt` 이 `NaN` 을 내고 그것이 `"NaN:NaN"` 으로 조립돼 **그대로 `PATCH` 로 나갔다**(422 가 된다).
검사를 쓰다가 실제로 재현됐다. `minutesAt`·`snapClock`·`defaultSlot` 셋에 **유한성 가드**를 넣고
「0 시로 읽는다」로 고정했으며, 그 자리를 검사 한 건으로 박았다.

### 시안과 다르게 둔 것 둘 — **보고만 한다**

1. **하루 끝의 기본 배정이 `24:00` 이 아니라 `23:59` 에 붙는다.**
   시안은 `wkClock(min + 60)` 으로 「24:00」을 만들지만(`week.jsx:212`), 서버가 받는 것은
   `datetime.time` 이라 **`24:00` 이 표현되지 않는다**(§A). 그대로 보내면 422 다.
2. **달 밖 칸은 여전히 아무것도 받지 않는다** — 일정을 그리지도, 고를 수도, 드롭을 받지도 않는다(시안 그대로).
   SPEC §2.2 는 시안의 그 제약을 「`day:number` 표현의 결과」로 부르고 §G 가 달 경계 넘기를 허용했지만,
   **다른 달로 옮기는 길은 막히지 않는다**(그 달로 넘겨서 떨어뜨리면 된다) — FE-1 의 K18 판정(격자가
   비운 것을 레일도 내지 않는다)과 결이 맞아 **건드리지 않았다.** 열어야 하면 말해 달라.

### 안 한 것

- **주 뷰 종일 띠 자체를 끌어 옮기는 길**(시안 `week.jsx:173-174`)은 만들지 않았다.
  작업 1 이 R1 을 「**좌측 카드** → 날짜 칸 드롭」으로 적었고, 띠에는 **손잡이**가 붙는다.
- **`/start`·제안 동의의 `schedule_release`** 는 읽지 않는다 — §7-2.

---

## 8. 미결 · 주의점

1. **`transitionDirectTask` 는 지금도 `Promise<void>` 다.** `POST …/start` 가 `schedule_release` 를
   싣지만 화면이 버린다. 바꾸려면 **여러 화면이 함께 쓰는 공용 함수의 시그니처**를 건드려야 하고,
   K11 정규화 이후 그 자리에서 닫히는 배정은 **구조적으로 0건**이다(WP 인수조건 F).
   **지금은 그대로 두었다** — 필요하면 별도 판으로.
2. **조건 변경 제안 동의(`respondTaskProposal`)의 `schedule_release` 도 읽지 않는다.**
   그 호출은 `WorkModals.tsx:1031` 안에 있고 **업무 화면과 공유**라, 캘린더가 가로챌 자리가 없다.
   브리프가 짚은 「제안 재전송 영수증은 `{0, null}`」 함정은 **우리가 그 자리를 아예 안 읽어서** 닿지 않는다.
3. **`make verify` 를 한 명령의 exit 0 으로 보이지 못했다** — §6. 기존 flaky 둘이 막는다.
4. **브라우저로 본 적이 없다.** 드래그의 손맛·고스트 위치·띠 이음새·`23:59` 가 읽히는지는
   사용자 E2E 가 처음 본다(검증 책임의 경계).
5. FE-1 §8 에서 남긴 것 중 **「N주차」 셈법**과 **`Empty` docstring 의 낡은 「29곳」**은 그대로 남는다.
   `listMeetingsInRange` 는 여전히 부르는 곳이 없다 — 합본 조회가 회의까지 싣기 때문이다.
