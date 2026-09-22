# 캘린더 시안 대비 현 구현 차이 — 프론트 전수조사

- 워커: `@sc-ax-fe` (term_49972e50)
- 작업 워크트리: `/Users/kknaks/orca/workspaces/Strong_hajin/strong-hajin-calendar` (branch `kknaksss/strong-hajin-calendar`)
- 조사 발주 — **코드는 한 줄도 고치지 않았다.** §9 에 `git status --short` 출력을 붙였다.
- 시안 루트(이하 `…`): `/Users/kknaks/orca/workspaces/kknaks_profile/strong_hajin/reference/2026-09-10-sc-meeting/package 2`
- 코드 경로는 모두 `frontend/` 기준 상대경로다.

각 절은 **사실(근거) / 해석 / 모르는 것** 을 나눠 적는다. 근거 없는 문장은 쓰지 않았다.

---

## 0. 한 장 요약

| 축 | 시안이 요구하는 것 | 지금 코드에 있는 것 | 판정 |
|---|---|---|---|
| 레이아웃 | `[SideNav][좌측 일정 레일][월·주 캘린더]` 3분할 | 본문 1칸. `CalendarPage` 는 레일을 셸에 등록하지 않는다 (`App.tsx:468` 이 `onRegisterRails` 를 안 넘긴다) | **없다** |
| 월 뷰 | 주 단위 lane 배치 + 띠 + 드롭 + 좌우 손잡이 | lane 배치·띠는 있다 (`WorkViews.tsx:198-243`). 드롭·손잡이는 없다 | **부분** |
| 주 뷰 | 종일 칸 + 0~24시 시간 격자(56px/시, 30분 스냅) 스크롤 | 날짜 격자 7칸 (`WorkViews.tsx:278-280`, `mode==="week"` 는 lane 을 8로 늘릴 뿐) | **없다** |
| 시간 배정 | 스케쥴 테이블(회의 + 업무의 그날 몇 시) | 개념 자체가 없다. `api.ts` 에 해당 호출 0건 | **없다** |
| 회의 | 탭(전체·회의·업무)으로 캘린더에 같이 낸다 (D9) | `CalendarPage.tsx:106` 주석이 "이 화면은 업무만 낸다" 고 못 박았다 | **뒤집힌다** |
| 날짜 표현 | `day: number` (달 안의 일 번호) | `start_date`/`due_date` = ISO `YYYY-MM-DD` | **불일치** |
| 상태값 | 시안 5종(`not-started`·`progress`·`blocked`·`done`·`cancelled`) — D4 가 폐기 | `TaskState` 5종(`open`·`in_progress`·`blocked`·`done`·`cancelled`), **`completion_submitted` 없음** | **D4 와 충돌** |
| DS 부품 12 | AppShell·SideNav·AppHeader·AppBody·Badge·Button·Icon·IconButton·SegmentedControl·GutterList·Empty·TaskCreateModal | 9 있음 · 1 이름충돌(GutterList) · 1 부분(Empty) · 1 없음(TaskCreateModal) | §4 참조 |
| 토큰 | `--scax-*` 51종 | 저장소에 **51종 전부 정의돼 있다** (`styles/scax.css`) | **그대로 쓸 수 있다** |
| CSS 클래스 | `.scax-*` 71종 | 저장소에 **0종** — 전부 새로 쓴다. 이름 충돌도 0 | **새로 쓴다(값은 복붙 가능)** |

**해석**: 시안 대비 이 화면은 «고쳐 쓰기» 가 아니라 «새로 세우기» 다. 다만 **스타일 층은 거의 무료다**(§8) — 비용은 상호작용·데이터·레이아웃에 몰려 있다.

---

## 1. 시안이 요구하는 상호작용 명세 (4-1)

시안 JSX 를 읽고 **동작 규칙**을 옮겼다. 각 항목에 **금지(가드)** 를 같이 적는다 — 시안은 금지를 `canDrop` 같은 조용한 가드로 표현한다.

### 1-1. 좌측 카드 → 날짜 칸 드롭 = 기간 이동

**사실**
- 드래그 시작: `ItemCard` 가 `draggable` 일 때 `window.__calDragId = card.id` 를 **전역에 적고** `dataTransfer.setData('text/plain', card.id)` 도 한다 (`…/handoff/calendar/js/calendar.v1.jsx:155`).
- 월 뷰 드롭: `.scax-month__cell` 이 `onDrop` 에서 `onDropDay(e.dataTransfer.getData('text/plain'), day)` (`calendar.v1.jsx:110`). 그 칸이 «이번 달 칸»(`live = !out`)일 때만 `onDragOver`/`onDrop` 이 달린다 (`calendar.v1.jsx:108-110`).
- 주 뷰 종일 칸 드롭: `.scax-week__day-allday` 가 `onMoveTask(...)` (`…/handoff/calendar/js/week.jsx:166-167`).
- 이동 규칙 — `moveTask` (`calendar.v1.jsx:205-210`):
  - `from && to` 있으면 → `{from: day, to: day + (to - from)}` **길이 유지**
  - `due` 만 있으면 → `{due: day}` **하루짜리 그대로**
  - 둘 다 없으면(기한 없음) → `{from: day, to: day}` **그날 하루가 된다**

**금지 / 가드**
- 달 밖 칸(`cell--out`)에는 드롭 핸들러 자체가 없다 (`calendar.v1.jsx:108-110`). → **전월·익월 칸으로 못 옮긴다.**
- 회의는 못 옮긴다 — 좌측 카드 중 회의 카드는 `draggable: false` (`calendar.v1.jsx:285`), `ItemCard` 는 `draggable` 이 거짓이면 `onDragStart` 를 아예 안 단다 (`calendar.v1.jsx:154-156`).
- **월 뷰·주 뷰 종일 칸의 드롭에는 `canDrop` 가드가 없다.** 시간 격자만 가드가 있다(1-3). → 날짜 이동은 언제나 허용된다.

**해석**: 「기간 길이 유지」는 `from`/`to` 쌍이 있을 때만이다. `due` 만 있는 업무를 날짜 칸에 떨어뜨리면 **기간이 생기지 않는다** — 기간이 생기는 유일한 길은 손잡이(1-2)다.

**모르는 것**: `day` 가 달을 넘는 이동(9/30 → 10/1)을 어떻게 다루는지 시안에 없다. 시안 데이터가 한 달짜리 `day:number` 라 표현할 수 없다(§5-1).

### 1-2. 띠 좌우 손잡이 = 시작·마감일 조정

**사실**
- 손잡이는 `resizable` 한 띠의 머리·꼬리에만 뜬다: `resizable = seg.kind === 'task' && seg.task` (`calendar.v1.jsx:124`), `head`/`tail` 일 때만 렌더 (`calendar.v1.jsx:135-136`).
- `onPointerDown` 이 `setGrab({id, edge})` 하고 `stopPropagation` + `preventDefault` 로 칸 클릭·드래그를 막는다 (`calendar.v1.jsx:67`).
- 끌기 중에는 `document.elementFromPoint(e.clientX, e.clientY).closest('.scax-month__cell[data-day]')` 로 «포인터 밑의 날짜 칸» 을 읽어 그 `data-day` 를 쓴다 (`calendar.v1.jsx:52-54`). 주 뷰는 같은 방식으로 `[data-day]` 를 읽는다 (`week.jsx:69-71`).
- 조정 규칙 — `resizeTask` (`calendar.v1.jsx:213-219`):
  - `edge==='start'` → `{from: min(day, to), to}` · `edge==='end'` → `{from, to: max(day, from)}`
  - 그리고 **언제나 `due: undefined`** — 마감만 있던 업무가 이때 `from`~`to` 기간을 갖는다.

**금지 / 가드**
- `min`/`max` 로 **시작이 마감을 넘지 못하고 마감이 시작보다 앞서지 못한다.** 넘기려 하면 조용히 같은 날로 접힌다(오류 문구 없음).
- 시간 배정 블록(스케쥴의 `kind:'task'`)은 `seg.task` 가 없어(`calEntries` 가 `slot` 키만 싣는다 — `calendar.v1.jsx:38`) **좌우 손잡이가 안 뜬다.**
- 회의(`kind:'meeting'`)도 손잡이가 없다 (같은 `resizable` 조건).
- 주 뷰 종일 띠는 **주 밖으로 나간 끝에는 손잡이를 안 단다**: `day === seg.f && taskFrom(seg.t) >= first` · `day === seg.to && taskTo(seg.t) <= last` (`week.jsx:177-178`). → 이 주 밖에서 시작/끝나는 업무는 **이 주에서 그 끝을 못 만진다.**
- 월 뷰는 `.scax-month__cell[data-day]` 를 요구하는데 `data-day` 는 `live`(이번 달) 칸에만 붙는다 (`calendar.v1.jsx:105`). → **달 밖 칸 위에서는 손잡이가 값을 안 읽는다.**

### 1-3. 좌측 카드 → 시간 격자 드롭 = 시간 배정 생성

**사실**
- 드롭 자리는 `.scax-week__hours` 열 (`week.jsx:199-214`).
- 분 계산 — `minAt` (`week.jsx:94-98`): 열 상자 기준 Y → `(Δy / 56px) * 60` → `round(raw / 30) * 30` → `clamp(0, 1440 - 60)`. **30분 스냅**, 그리고 **항상 60분이 들어갈 자리로 잘린다**.
- 드롭 시 `onSchedule(taskId, day, wkClock(min), wkClock(min + 60))` (`week.jsx:212`) → **기본 길이 1시간**.
- 드래그 중 고스트: `dropAt` 이 `.scax-week__ghost` 를 그 자리에 띄우고 `HH:MM – HH:MM` 을 쓴다 (`week.jsx:215-219`).
- 생성 규칙 — `addSlot` (`calendar.v1.jsx:222-226`): `{id:`sx${taskId}-${day}`, kind:'task', taskId, title, day, start, end, owner}` 한 줄을 만든다. **업무의 기간(`from`/`to`)은 건드리지 않는다.**

**금지 / 가드 — 여기가 시안의 핵심 가드다**
- `canDrop(day)` (`week.jsx:101-105`):
  ```js
  const t = tasks.find((x) => x.id === window.__calDragId);
  if (!t || !taskFrom(t)) return false;
  return day >= taskFrom(t) && day <= taskTo(t);
  ```
  1. **업무가 아닌 것은 못 넣는다** — `tasks` 에서 못 찾으면 거짓. 회의는 애초에 드래그가 안 된다.
  2. **기한 없는 업무는 못 넣는다** — `taskFrom(t)` 가 `undefined` 면 거짓. 시간 배정 전에 날짜부터 정해야 한다.
  3. **업무 기간 밖에는 못 넣는다** — `[from, to]` 바깥 날짜면 거짓.
- 거짓이면 `onDragOver` 가 `preventDefault` 를 **안 부른다** (`week.jsx:205`) → 브라우저가 드롭을 거절한다. **오류 문구도 고스트도 없다 — 조용한 금지다.**
- `addSlot` 의 `keep` 필터 (`calendar.v1.jsx:224`): `!(s.taskId === taskId && s.day === day)` → **한 업무는 하루에 시간 배정을 하나만 갖는다.** 같은 날에 두 번째로 떨어뜨리면 **첫 번째가 조용히 교체된다.**
- `canDrop` 이 `dataTransfer` 대신 **전역 `window.__calDragId`** 를 읽는 이유: `dragover` 중에는 `dataTransfer.getData` 가 빈 문자열이라 «끌고 있는 것이 무엇인지» 를 알 수 없다. 시안은 그래서 전역을 쓴다 (`calendar.v1.jsx:155` · `week.jsx:174` 가 쓰고, `week.jsx:102` 가 읽는다).

### 1-4. 시간 블록 세로 손잡이 = 시작·종료 시각 조정

**사실**
- 손잡이 둘이 모든 시간 블록에 붙는다 — `slotHandle(s,'start')` · `slotHandle(s,'end')` (`week.jsx:231-232`). **회의 블록에도 붙는다** (`shownSlots` 를 가리지 않는다).
- `onPointerDown` 이 `setGrabSlot({id, edge, el: e.currentTarget.closest('.scax-week__hours')})` — **기준 상자는 블록이 아니라 그 날짜 열 전체**다 (`week.jsx:125`).
- 끌기 — `week.jsx:82-87`: `((e.clientY - box.top) / 56) * 60` → `round(/30)*30` → `clamp(0, 1440)` → `onResizeSlot(id, edge, "HH:MM")`.
- 적용 — `resizeSlot` (`calendar.v1.jsx:229-233`): `edge==='start'` 면 `time < s.end` 일 때만 반영, `edge==='end'` 면 `time > s.start` 일 때만 반영.

**금지 / 가드**
- **역전 금지**: 시작이 종료 이상이 되면 값을 **그냥 버린다** (이전 값 유지). 오류 문구 없음.
- **자정 넘김 금지**: `clamp(0, 1440)` 이라 하루를 벗어나지 못한다.
- **최소 길이 없음**: `start < end` 만 지키면 30분 미만도 만들어진다. 다만 그리기는 `Math.max(px(30), px(b-a)) - 2` 로 **최소 30분 높이로 그린다** (`week.jsx:227`) — 값과 그림이 달라질 수 있다.
- **날짜 이동 불가**: `resizeSlot` 은 `day` 를 안 건드린다. 시간 블록을 다른 날로 옮기는 길은 시안에 **없다** (지우는 길도 없다).

### 1-5. 시안에 있는데 위 넷에 안 적힌 것

| # | 규칙 | 근거 |
|---|---|---|
| a | **탭 3종(전체·회의·업무)** 이 좌측 레일과 격자를 **동시에** 가른다 | `…/handoff/calendar/js/data.js:9-13` · `calendar.v1.jsx:179` |
| b | 격자와 레일의 **필터가 대칭이 아니다**. 격자(`calEntries`)는 `tab==='task'` 일 때 «업무 날짜 띠 + 업무 시간 배정» 둘을 낸다 (`calendar.v1.jsx:33-38`). 레일은 `tab==='all'` 이면 회의만 카드로 세우고, 업무의 시간 배정은 **업무 카드의 `meta` 줄로 접는다**(`13일 13:00` 꼴) | `calendar.v1.jsx:261` · `calendar.v1.jsx:274-275` |
| c | 날짜 한 칸을 **클릭하면 선택**, 다시 누르면 해제. 선택하면 좌측 레일이 그 날짜로 좁혀지고 「9월 N일 / 전체 보기」 줄이 뜬다 | `calendar.v1.jsx:107` · `181-185` · `inScope` `250-254` |
| d | 주·월 이동은 선택을 **항상 푼다** | `shift()` `calendar.v1.jsx:235-236` |
| e | 월 칸의 lane 상한 4, 넘치면 `+N건 더` — **그 날을 덮는 것만 센다** | `CAL_CELL_LIMIT = 4` (`calendar.v1.jsx:11`) · `101` · `140` |
| f | 주 뷰 종일 lane 상한 3, 넘치면 「N건 펴기 / 접기」 토글 | `WEEK_LANES = 3` (`week.jsx:8`) · `52-54` · `139-143` |
| g | 주 뷰는 **8시에 맞춰 열린다** (`scrollTop = 8 * 56`), rAF 로 한 번 더 맞춘다 | `WEEK_OPEN = 8` (`week.jsx:7`) · `58-63` |
| h | 같은 항목이 **그 주 내내 같은 줄**에 앉아야 띠가 이어진다 — 주 단위로 lane 을 새로 배정한다 | `calendar.v1.jsx:72-86` · `week.jsx:24-35` |
| i | 띠 라벨은 **머리 칸이나 그 주 첫 칸에만** 그리고, 폭을 `calc(reach * 100% - reach * 12px)` 로 늘려 칸을 넘어간다 | `calendar.v1.jsx:130-134` |
| j | 월 뷰는 **완전히 달 밖인 마지막 주를 지운다** (6주 → 5주) | `calendar.v1.jsx:26` |
| k | 날짜 열은 **위(종일)·아래(시간) 두 구역이 같은 `data-day`** 를 달고 같이 선택된다 | `week.jsx:4` · `155` · `201` |
| l | 주 뷰 종일 띠 자체도 **드래그 원본**이다 (띠를 잡아 다른 날로 옮긴다) | `week.jsx:173-174` |
| m | 「오늘」은 **하드코딩**: `new Date(2026, 8, 15)` | `calendar.v1.jsx:10` |
| n | 좌측 레일 맨 아래 「더보기」 단추가 있으나 **핸들러가 없다** (`onClick` 미지정) | `calendar.v1.jsx:187` |
| o | 완료 업무는 캘린더에 **애초에 안 들어온다**: `CAL_TASKS = WORK_TASKS.filter(t => t.group !== 'done')` | `…/handoff/calendar/js/data.js:6` |

**⚠ o 와 D5 의 관계**: 시안은 `status` 가 아니라 **`group`** 으로 거른다. `d4`(가격표 초안 회신)는 `status:'cancelled'` 인데 `group:'done'` 이다 (`…/handoff/shared/js/work-data.js:38`). 즉 시안의 「접는다」 기준은 상태값이 아니라 화면 탭 분류다. D5(「done·cancelled 로 가면 배정도 같이 접는다」)를 상태값으로 구현하면 시안과 **다른 규칙**이 된다 — §7 OQ-3.

---

## 2. 현 캘린더 표면 전수 (4-2) — 고칠 수 있나, 새로 세워야 하나

### 2-1. `TaskCalendar` 를 쓰는 곳 전부

**실제로 돌린 명령**
```bash
cd frontend && grep -rn "TaskCalendar" src
```

**출력 전문**
```
src/shell/CalendarRail.tsx:18: * 바퀴 5b 는 주·월을 본문용 `TaskCalendar`(폭 넓은 격자)로 때웠다. 7-D 가 시안 모양으로 옮긴다 —
src/features/calendar/CalendarPage.tsx:7:import { TaskCalendar } from "../work/WorkViews";
src/features/calendar/CalendarPage.tsx:111:      <TaskCalendar mode={mode} onModeChange={setMode} onOpen={setSelected} tasks={tasks} />
src/features/work/CalendarTasks.test.tsx:5:import { TaskCalendar, taskSpan, weekSegments } from "./WorkViews";
src/features/work/CalendarTasks.test.tsx:86:      <TaskCalendar
src/features/work/WorkViews.tsx:257:export function TaskCalendar({
src/styles/screens-b.css:708:   본문은 우리 `TaskCalendar`(`WorkViews.tsx`)다 — 공용 부품이라 마크업은 P-3 으로 못 건드린다.
src/styles/screens-b.css:715:   레일은 `TaskCalendar` 를 그대로 부른다(`CalendarRail.tsx:89`) — 같은 마크업이니 같은 규칙이 맞다.
```

**사실 — 실 호출부는 딱 둘이다**
1. `CalendarPage.tsx:111` — 이번 판이 다시 세우는 그 자리.
2. `CalendarTasks.test.tsx:86` — vitest.

나머지 셋(`CalendarRail.tsx:18` · `screens-b.css:708` · `screens-b.css:715`)은 **주석이고, 둘은 이미 낡았다.**
- `CalendarRail.tsx:18` 은 "바퀴 5b 는 `TaskCalendar` 로 때웠다 / 7-D 가 시안 모양으로 옮긴다" 는 **과거형 기록**이다. 지금 `CalendarRail` 은 자기 `WeekView`/`MonthView` 를 갖고 (`CalendarRail.tsx:160` · `219`) `TaskCalendar` 를 import 하지 않는다 (파일 상단 import 목록 `CalendarRail.tsx:1-11` 에 없다).
- `screens-b.css:715` 의 "레일은 `TaskCalendar` 를 그대로 부른다(`CalendarRail.tsx:89`)" 는 **사실이 아니다.** `CalendarRail.tsx:89` 는 지금 `<Empty title="오늘 기한인 업무가 없습니다" />` 다.

**해석 — 「고치면 남의 화면이 깨지나?」**
- **깨지지 않는다.** 실 소비처가 `CalendarPage` 하나뿐이므로 `TaskCalendar` 를 고쳐도 다른 화면이 움직이지 않는다.
- 다만 **그래도 새로 세우는 쪽이 맞다**고 본다. 근거 넷:
  1. `TaskCalendar` 는 `tasks: DirectTask[]` 와 `onOpen` 만 받는다 (`WorkViews.tsx:257-270`). 시안은 `tasks` + `schedule` + `tab` + 콜백 5개(`onSelect`·`onDropDay`/`onSchedule`·`onResizeTask`·`onMoveTask`·`onResizeSlot`)를 요구한다 (`calendar.v1.jsx:307-332`). 시그니처가 남는 것이 거의 없다.
  2. `TaskCalendar` 는 **앵커를 자기 안에 가둔다** (`useState(anchorDate ?? today)` — `WorkViews.tsx:272`). 시안은 툴바·좌측 레일·주 뷰가 같은 커서를 공유해야 한다 (`calendar.v1.jsx:199-200` 의 `weekAnchor`·`cursor` 가 페이지 상태다).
  3. `mode==="week"` 가 시안의 주 뷰와 **다른 것**이다 — 날짜 7칸에 lane 을 8로 늘릴 뿐이고 (`WorkViews.tsx:280`) 시간 축이 없다.
  4. `WorkViews.tsx` 는 585줄짜리 공용 파일로 `TaskTimeline`·`TaskKanban` 과 `MetricCard`·`TaskCard`·`PersonChip`·`CollapsibleGroup`·`TaskListRow` 를 같이 담고 있다. 캘린더 재작성을 이 파일 안에서 하면 관계없는 화면의 diff 가 커진다.
- `TaskCalendar` 를 **지우는 것은 이번 판의 일이 아니다**: 지우면 `CalendarTasks.test.tsx` 의 케이스 5개가 같이 죽는다(§2-3).

### 2-2. `TaskCalendar` 가 딸고 있는 보조 함수

**실제로 돌린 명령**
```bash
cd frontend && grep -rn "weekSegments" src
cd frontend && grep -rn "taskSpan" src
```

**사실**

| 심볼 | 정의 | 쓰는 곳 |
|---|---|---|
| `weekSegments(tasks, days, maxLanes)` | `WorkViews.tsx:198-243` | `WorkViews.tsx:284`(TaskCalendar) · `CalendarTasks.test.tsx:47,48,65,74` — **본코드 소비처 1곳** |
| `taskSpan(task)` | `WorkViews.tsx:175-181` | `WorkViews.tsx:209`(weekSegments 내부) · `WorkViews.tsx:441`(**`TaskTimeline`**) · `CalendarTasks.test.tsx:5` |
| `CalendarSegment` (타입) | `WorkViews.tsx:183-192` | `WorkViews.tsx:246`(`segmentLabel`) · `202`(반환형) |
| `segmentLabel(segment)` | `WorkViews.tsx:246-255` (비공개) | `WorkViews.tsx:357,369` |

**해석**
- `weekSegments` 는 캘린더 전용이라 **가져가도 남는 자리가 없다.** 시안의 lane 배치(`calendar.v1.jsx:72-86` · `week.jsx:24-35`)와 알고리즘이 같은 계열이다 — 「긴 것 먼저, 겹치지 않는 lane 재사용」. 다만 다음 둘이 다르다:
  - 코드: 정렬을 **안 한다** — 들어온 순서대로 배치한다 (`WorkViews.tsx:208-211` 에 `.sort()` 가 없다). 시안은 `a.f - b.f || (b.t-b.f)-(a.t-a.f)` 로 정렬한다 (`calendar.v1.jsx:79`).
  - 코드: lane 초과분을 `hiddenByDay` 로 **날짜별로 센다** (`WorkViews.tsx:224-230`). 시안은 그리는 시점에 센다 (`calendar.v1.jsx:101`). 결과는 같은 뜻이다.
- **`taskSpan` 은 `TaskTimeline` 이 같이 쓴다** (`WorkViews.tsx:441`). → **이것만은 고치면 남의 화면(업무 타임라인)이 따라 움직인다.** 새 캘린더가 `taskSpan` 의 «양끝 포함 / 한쪽만 있으면 그 하루 / 둘 다 없으면 캘린더에 없음» 규칙(`WorkViews.tsx:169-181`)을 쓰고 싶다면 **읽기만 하고 시그니처를 바꾸지 마라.**

### 2-3. `TaskCalendar` 를 걸고 있는 테스트

**사실** — `src/features/work/CalendarTasks.test.tsx` 5케이스 (`grep -n "it(" src/features/work/CalendarTasks.test.tsx`):
```
17:  uses the planned dates and never invents one from when the row was written        (taskSpan)
45:  makes one bar per task per week, clipped to the week and marked where it continues (weekSegments)
59:  keeps overlapping work in stable lanes instead of moving it around                 (weekSegments)
70:  counts what a cell cannot show rather than dropping it                             (weekSegments)
83:  draws one bar for a range, one for a deadline, and nothing for a task without dates (TaskCalendar 렌더)
```
**해석**: `TaskCalendar` 를 남겨 두면 이 다섯은 그대로 통과한다. 새 부품을 세우면 **새 테스트 파일이 필요하고** 이 다섯은 손대지 않아도 된다.

### 2-4. `.calendar-*` 클래스가 지금 어디까지 새는가

`CalendarPage.tsx:99-100` 의 주석은 «8-B 가 `.calendar-*` 를 `.calendar-screen` 안에 가뒀고 8-C 가 그 울타리를 뗐다» 고 적는다. **지금 상태를 실제로 셌다.**

**실제로 돌린 명령**
```bash
cd frontend && grep -rn '\.calendar-' src/styles
cd frontend && grep -rn "calendar-" src --include="*.tsx" --include="*.ts"
```

**사실 ① — 규칙을 정의하는 자리 (4개 파일, 32줄)**

| 파일 | 줄 | 겨누는 것 |
|---|---|---|
| `styles/screens-b.css` | 718, 722, 730, 734, 741, 744, 747, 750, 756, 764, 774, 779, 784, 789, 793 | `.calendar-toolbar` · `-weekdays span` · `-grid` · `-cell`(+`.outside`/`.today`) · `-day` · `-chip`(+상태 4) · `-more` |
| `styles/screens-a.css` | 392, 394, 395, 396, 397, 398, 400, 401, 433, 434, 495 | `.calendar-weekdays` · `-week` · `-days` · `-bars` · `-cell:nth-child(7n)` · `-chip.continues-*` · `.work-timeline .calendar-toolbar` |
| `styles/components.css` | 559, 683 | `.calendar-grid.week .calendar-cell{min-height:280px}` · 미디어쿼리 안 `.calendar-grid:not(.week) .calendar-cell{min-height:96px}` |
| (주석만) `screens-b.css` | 7, 711, 712, 715 | — |

**사실 ② — 그 클래스를 실제로 다는 자리 (2개 파일)**

| 파일 | 줄 | 클래스 |
|---|---|---|
| `features/work/WorkViews.tsx` | 300, 327, 332, 334, 335, 341, 345, 346, 352, 359 | `calendar-toolbar` · `-weekdays` · `-grid`(+`week`) · `-week` · `-days` · `-cell`(+`outside`/`today`) · `-day` · `-more` · `-bars` · `-chip` |
| `features/work/WorkViews.tsx` | 405 | `calendar-toolbar` — **`TaskTimeline` 안이다** |
| `ds/DatePicker.tsx` | 113 | `calendar-weekdays` — **DS 날짜 선택기다** |

**해석 — 새는 범위는 정확히 둘이다**
1. **`TaskTimeline`(업무 타임라인)** 이 `.calendar-toolbar` 를 쓴다 (`WorkViews.tsx:405`). `screens-a.css:495` 가 `.work-timeline .calendar-toolbar` 로 한 번 더 겨눈다. → `.calendar-toolbar` 를 건드리면 **타임라인 머리가 따라 움직인다.**
2. **`DatePicker`** 가 `.calendar-weekdays` 를 쓴다 (`DatePicker.tsx:113`). `DatePicker` 는 `DateField` 가 감싸고 (`ds/DateField.tsx:1`), `DateField` 는 **7개 파일 12자리**가 쓴다:
   `features/action/ActionTaskCard.tsx:134` · `ActionMeetingCard.tsx:458` · `ActionCenter.tsx:279,542` · `features/work/WorkModals.tsx:1559,1569,2476,3061,4290,4305` · `features/report/DailyReportPage.tsx:183` · `features/meetings/BookingModal.tsx:363` · `MeetingEditModal.tsx:176`.
   → `.calendar-weekdays` 를 건드리면 **업무·액션·일일보고·회의 예약의 날짜 선택기가 전부 따라 움직인다.**

**판단 근거 (설계를 정하지 않고, 사실만)**
- `.calendar-*` 는 **이 화면의 이름이 아니다.** 두 부품이 이미 같이 쓰고 있고, 그중 하나(`DatePicker`)는 DS 층이다.
- 시안은 이 화면에 **완전히 다른 이름 체계(`.scax-month__*` · `.scax-week__*` · `.scax-event*` · `.scax-cal-*`)** 를 쓰며, 그 71종 중 저장소와 **이름이 겹치는 것이 하나도 없다**(§8-2). → 새 이름으로 세우면 위 두 소비처가 움직일 이유가 없다.
- 반대로 기존 `.calendar-*` 마크업을 시안 모양으로 고치면, `TaskTimeline` 과 12자리의 `DateField` 가 같은 규칙을 공유하므로 **회귀 표면이 최소 14곳**이다.

**모르는 것**: `screens-b.css:711-715` 가 근거로 든 「셋이 같은 모양」의 셋 중 하나(`CalendarRail`)는 이미 빠졌다. 그 블록을 정리할지는 이번 판의 결정 사항이 아니다 — 리포트에만 적는다.

---

## 3. 화면 골격 — 3분할을 받을 자리가 있는가 (4-2 보강)

**사실**
- 셸은 이미 3칸 규약을 갖는다: `AppBody({railLeft, railRight, children})` (`shell/AppShell.tsx:74-82`), `App.tsx:453` 이 `surfaceRails.left`/`.right` 를 꽂는다.
- 화면은 `onRegisterRails({left, right})` 로 자기 레일을 셸에 등록한다 (`App.tsx:130-131`). **안 넘기면 그 칸이 렌더되지 않는다** (`AppShell.tsx:77,79` 의 조건부).
- 지금 그것을 쓰는 화면은 둘뿐이다: `MeetingWorkspace` (`App.tsx:477`) · `MyWorkPage` (`App.tsx:494`).
- **`CalendarPage` 는 안 쓴다** — `App.tsx:468` 이 `{...pageProps} {...sharedWorkProps}` 만 넘기고, `pageProps` 에 `onRegisterRails` 가 없다 (`App.tsx:352`). `CalendarPage` 의 props 타입에도 없다 (`CalendarPage.tsx:9-19`).
- `MyWorkPage` 가 레일에 꽂는 것: 왼쪽 `InboxRail`, 오른쪽 `CalendarRail` (`MyWorkPage.tsx:899-921`).
- 본문 스크롤 기둥: `App.tsx:458` 이 surface 별로 `.scax-page-scroll` 변종을 고른다. 캘린더는 기본형 → `flex:1 1 auto; min-height:0; overflow-y:auto; padding:0 40px 152px` (`styles/shell.css:177`).

**해석**
- 3분할 자체는 **셸이 이미 낸다.** 필요한 것은 `CalendarPage` 가 `onRegisterRails` 를 받아 좌측 일정 레일을 등록하는 배선이다 — `MyWorkPage.tsx:899-921` 이 그 선례다.
- 시안의 `AppBody railLeft={<ItemRail …/>}` (`calendar.v1.jsx:293`) 는 **왼쪽 한 칸만** 쓴다. `MyWorkPage` 가 오른쪽에 `CalendarRail` 을 세우는 것과 배치가 다르다 — 캘린더 화면에서 오른쪽 레일을 어떻게 할지는 시안에 없다(§7 OQ-5).
- 시안의 캘린더 본문은 `flex:1 1 auto; min-height:0` 으로 **칸을 꽉 채워 자기 안에서 스크롤한다** (`…/handoff/calendar/css/calendar.css:4` · `65` · `67`). 지금 기본 `.scax-page-scroll` 은 `overflow-y:auto` + `padding-bottom:152px` 라 **바깥이 스크롤한다.** 회의 화면은 이 충돌을 `--fixed` 변종으로 풀었다 (`shell.css:182` · `App.tsx:458`).

---

## 4. DS 부품 대조 (4-3)

시안 `…/handoff/calendar/js/calendar.v1.jsx:6` 이 `window` 에서 꺼내 쓰는 열둘을 하나씩 판정했다.

**실제로 돌린 명령**
```bash
cd frontend && grep -rn "^export function\|^export const\|^export type\|^export default" src/ds src/shell --include="*.tsx" --include="*.ts" | grep -v '\.test\.'
cd frontend && grep -n "^export function\|^export const\|^export type" src/features/work/WorkModals.tsx
cd frontend && grep -rn "scax-gutter-list" src
cd frontend && grep -rn "scax-inbox-card" src
```

### 4-1. 판정표

| # | 시안 부품 | 시안 시그니처 (`…/handoff/shell/js/scax-ui.jsx`) | 저장소 | 판정 |
|---|---|---|---|---|
| 1 | `AppShell` | `{nav, children}` (`:207`) | `shell/AppShell.tsx:37` — `{nav, children}` | **같다** |
| 2 | `SideNav` | `{user, activeId, onSelect, collapsed, onCollapse}`, 항목은 `NAV_PRIMARY`/`NAV_MAIN` 전역 (`:217`) | `shell/SideNav.tsx:70` — `{user, items, utilityItems, activeId, collapsed, onCollapse, onSelect, onUserClick, userActionLabel, footerActions, label, logo, version}` | **있다 · 시그니처 다름** (항목을 전역이 아니라 prop 으로 받는다) |
| 3 | `AppHeader` | `{breadcrumb, title, titleEnd, actions}` (`:264`) | `shell/AppShell.tsx:46` — `{breadcrumb, title, actions}` | **있다 · `titleEnd` 없음** (캘린더는 `title`+`actions` 만 쓴다 — `calendar.v1.jsx:292`) |
| 4 | `AppBody` | `{railLeft, railRight, children}` (`:288`) | `shell/AppShell.tsx:74` — 동일 | **같다** |
| 5 | `Badge` | `{tone, variant, children}` (`:52`) | `ds/Badge.tsx:26` — `{tone, variant, className, ...rest}`, tone 6종(accent·neutral·danger·positive·info·outline) | **같다** (캘린더가 쓰는 `accent`·`neutral` 둘 다 있다 — `calendar.v1.jsx:160`) |
| 6 | `Button` | `{variant, tone, size, label, iconBefore, block, disabled, onClick, type}` (`:25`) | `ds/Button.tsx:41` — 동일 + `ariaLabel`·`title`·`className`·`children`·`...rest`, variant 5종 | **같다 (상위집합)** |
| 7 | `Icon` | `{name, size, className}` — 글리프는 `window.SCAX_DS.Icon` (`:19`) | `ds/icons/Icon.tsx:14` — `{name: IconName, size, className}` | **있다** · 캘린더가 쓰는 글리프 `chevron-right`(`calendar.v1.jsx:298,300`) · `calendar`(`:186`) · `inbox`(`scax-ui.jsx:166`) **셋 다 `IconName` 에 있다** (`ds/icons/glyphs.tsx:39-84`) |
| 8 | `IconButton` | `{name, size, label, onClick, active, className}` (`:41`) | `ds/Button.tsx:107` — 동일 + `disabled`·`title`·`children`·`...rest`. `size` 는 `12\|14\|16\|20` 유니온 | **같다** (캘린더는 `size={20}` — `calendar.v1.jsx:298`) |
| 9 | `SegmentedControl` | `{value, options, onChange, ariaLabel}` (`:111`) | `ds/SegmentedControl.tsx:22` — 동일(제네릭 `T extends string`) + 항목 `disabled` | **같다 (상위집합)** |
| 10 | `GutterList` | `{title, count, headerEnd, children}` — 머리줄(아이콘+제목+count 배지+오른쪽 슬롯) + 스크롤 본문 (`:160`) | `ds/GutterList.tsx:20` — `{label, rows: GutterRow[], gutterWidth, asideWidth}` — **왼쪽 고정 칸 + 본문의 2단 목록.** 완전히 다른 부품 | **⚠ 이름 충돌. 시안 것은 없다** |
| 11 | `Empty` | `{icon, title, desc}` (`:176`) | `ds/Empty.tsx:34` — `{title, description, variant, actionLabel, onAction, className, children}` — **`icon` prop 이 없다.** 아이콘은 `variant` 가 고른다(`error`→`circle-exclamation`, `filter`→`tune`, 그 밖→`inbox`, `Empty.tsx:51`) | **있다 · `icon` 없음** (시안은 `icon="calendar"` — `calendar.v1.jsx:186`) |
| 12 | `TaskCreateModal` | `{open, onClose, onToast, draft}` (`…/handoff/shell/js/work-modal.jsx:194`) | 같은 이름 **없다**. 가장 가까운 것이 `features/work/WorkModals.tsx:3444` `CreateWorkModal({ownerName, canCreateTask, canCreateRequest, assigneeCandidates, assignCandidates, ccCandidates, initial, onSubmitRequest, projectCandidates, onCreated, onOpenTask, onError, onClose, size})` | **이름으로 없다 · 시그니처 전혀 다름** |

### 4-2. GutterList 이름 충돌의 실체

**사실**
- 시안 `GutterList` 의 마크업 — `.scax-gutter-list` > `__header` > `__title`(Icon+제목+count Badge) + `headerEnd`, 그리고 `__body` (`scax-ui.jsx:160-174`).
- **그 마크업은 저장소에 있다. 다만 부품이 아니라 `InboxRail` 안에 인라인으로 박혀 있다**: `shell/InboxRail.tsx:103`(`section.scax-gutter-list`) · `:104`(`header.__header`) · `:105`(`h2.__title`) · `:114`(`div.__body`).
- CSS 도 있다: `styles/components.css:105-108` (`.scax-gutter-list` · `__header` · `__title` · `__body`).
- 반면 `ds/GutterList.tsx` 가 그리는 클래스는 `.gutter-list` · `.gutter-row` · `.gutter-meta` · `.gutter-aside` · `.gutter-body` — **접두사 `scax-` 가 없는 다른 계열**이다 (`GutterList.tsx:41-55`).

**해석**: 「시안의 GutterList」를 부품으로 뽑으려면 `InboxRail.tsx:103-114` 에서 들어내야 하는데, 그 이름은 이미 `ds/GutterList.tsx` 가 쥐고 있다. → **이름 결정이 필요하다** (§7 OQ-6).

### 4-3. 좌측 카드(`ItemCard`) 대조 — 보너스

**사실**
- 시안 `ItemCard` 는 `.scax-inbox-card` 계열을 그대로 쓴다 (`calendar.v1.jsx:152-173`): `__content` · `__top` · `__title` · `__meta` · `__meta-who` · `__meta-sep`.
- 저장소에 **같은 클래스가 전부 있고** (`styles/components.css:111-121`), `InboxRail.tsx:59-71` 이 같은 구조로 쓴다.
- 시안이 더하는 것은 `.scax-inbox-card--draggable` 한 종뿐이고, 그 규칙은 `…/handoff/calendar/css/calendar.css:58-59` 에 있다 (저장소에 없음).

**해석**: 좌측 카드는 **거의 그대로 재사용된다.** 다만 저장소에는 `InboxCard` 라는 **부품이 없다** — `InboxRail` 안의 인라인 마크업이다.

### 4-4. 그 밖에 시안이 쓰는데 목록 열둘에 안 들어간 것

| 시안 | 근거 | 저장소 |
|---|---|---|
| `WeekGrid` (주 뷰 전체) | `week.jsx:37` · `window.WeekGrid` | **없다** |
| `MonthGrid` | `calendar.v1.jsx:42` | 비슷한 것이 `TaskCalendar` 안에 박혀 있다 (부품이 아니다) |
| `ItemRail` | `calendar.v1.jsx:177` | **없다** (`InboxRail`·`CalendarRail` 은 다른 목록이다) |
| `ItemCard` | `calendar.v1.jsx:150` | **없다** (§4-3) |
| 일정 조각 `.scax-event*` (띠·손잡이·고스트·+N건) | `calendar.css:34-57` · `95-103` | **없다** |

---

## 5. DS-gaps — 다음 판에 디자이너에게 넘어갈 목록

> 판단(「비슷한 걸로 대체 가능」)을 적지 않는다. **없다는 사실과 그 근거**만 적는다.

### G-CAL-01 · 레일형 `GutterList` 부품
- **없다**: `ds/` 에 `{title, count, headerEnd, children}` 부품이 없다.
- **이름이 이미 점유돼 있다**: `ds/GutterList.tsx:20` 이 다른 부품이다.
- **마크업·CSS 는 있다**: `shell/InboxRail.tsx:103-114` 인라인 · `styles/components.css:105-108`.
- 시안 근거: `…/handoff/shell/js/scax-ui.jsx:160-174` · 쓰는 곳 `calendar.v1.jsx:179`.

### G-CAL-02 · `Empty` 의 `icon` prop
- **없다**: `ds/Empty.tsx:34` 의 props 에 `icon` 이 없고, 아이콘은 `variant` 가 고정 매핑한다 (`Empty.tsx:51`).
- 시안 근거: `scax-ui.jsx:176` `Empty({icon='inbox', title, desc})` · 쓰는 곳 `calendar.v1.jsx:186` `icon="calendar"`.
- 부수 사실: prop 이름도 다르다 — 시안 `desc` ↔ 코드 `description`.

### G-CAL-03 · `TaskCreateModal`
- **이름으로 없다**. 가장 가까운 `CreateWorkModal` (`features/work/WorkModals.tsx:3444`) 은 `{ownerName, canCreateTask, canCreateRequest, assigneeCandidates, …}` 로 **권한·후보 목록을 부르는 쪽이 들고 있어야 한다.**
- 시안 근거: `…/handoff/shell/js/work-modal.jsx:193-194` `TaskCreateModal({open, onClose, onToast, draft})` · 쓰는 곳 `calendar.v1.jsx:337`.
- **캘린더 화면이 이것을 열려면 후보 목록 API 를 자기가 불러야 한다** — `MyWorkPage` 가 지금 그렇게 한다.

### G-CAL-04 · `ItemCard` / `InboxCard` 부품
- **없다** — `.scax-inbox-card` 마크업이 `shell/InboxRail.tsx:59-71` 에 인라인이다.
- `--draggable` 모디파이어 규칙도 저장소에 없다 (`…/handoff/calendar/css/calendar.css:58-59` 에만 있다).

### G-CAL-05 · 일정 조각(`Event`) 부품 일체
- **없다**: 띠(`.scax-event--bar` + head/tail) · 좌우 손잡이(`.scax-event__handle--start/--end`) · 세로 손잡이(`.scax-week__slot-handle--start/--end`) · 드롭 고스트(`.scax-week__ghost`) · `+N건 더`(`.scax-event--more`).
- 근거: `…/handoff/calendar/css/calendar.css:34-57` · `93-103` ↔ 저장소 `.scax-*` 목록에 하나도 없다(§8-2 의 comm 결과).

### G-CAL-06 · 월 격자(`MonthGrid`) · 주 격자(`WeekGrid`) 부품
- **없다**: `ds/` 에 없고, 비슷한 것은 `TaskCalendar` 안에 박혀 있다 (`WorkViews.tsx:298-382`) — 재사용 가능한 부품이 아니다.
- 주 뷰의 시간 축(0~24시 / 56px 한 시간 / 30분 스냅 / 8시 초기 스크롤)은 **저장소 어디에도 없다.**

### G-CAL-07 · `AppHeader` 의 `titleEnd`
- **없다**: `shell/AppShell.tsx:22-29` `AppHeaderProps` 에 없다. 시안엔 있다 (`scax-ui.jsx:264`).
- **캘린더 화면은 안 쓴다** — 다른 화면을 위해 기록만 한다.

### G-CAL-08 · 상태 색 tint (기존 gap 의 재확인)
- `styles/screens-b.css:763-766` 주석이 이미 적어 둔 것: "새 DS 는 status 에 «진한 색 한 칸»만 준다(danger 만 soft 가 따로 있다) … 없는 tint 를 지어내지 않았다 (DS-gaps 후보)".
- 시안 캘린더는 이 문제를 **다르게 푼다**: 상태 색을 아예 안 쓰고 **유형 둘(업무=진한 면 / 회의=연한 면)로만** 말한다 (`…/handoff/calendar/css/calendar.css:45-47`).
- → 시안을 그대로 따르면 이 gap 은 캘린더에서 **사라진다.** 다만 §7 OQ-2 와 얽힌다.

---

## 6. 데이터 (4-4)

### 6-1. 캘린더가 부를 수 있는 호출

**실제로 돌린 명령**
```bash
cd frontend && grep -n "^export async function\|^export function\|^export const" src/lib/api.ts
cd frontend && grep -rn "schedule\|Schedule\|time_slot\|slot\|starts_at" src/lib/api.ts
```
(`api.ts` 전체 export 는 **132개**다. 아래는 캘린더가 쓸 수 있는 것만 추렸다.)

#### 업무 쪽

| 호출 | 줄 | 엔드포인트 | 캘린더에서 |
|---|---|---|---|
| `getMyWork()` | `api.ts:147` | `GET /api/my-work` | 지금 `CalendarPage.tsx:35` 가 쓴다 |
| `getTasks(includeClosed)` | `api.ts:151` | `GET /api/tasks[?include_closed=true]` | 지금 `CalendarPage.tsx:35` 가 `true` 로 쓴다 |
| `getTask(taskId)` | `api.ts:155` | `GET /api/tasks/{id}` | 상세 |
| **`updateTask(taskId, expectedVersion, patch)`** | `api.ts:243` | `PATCH /api/tasks/{id}` | **드래그·리사이즈가 쓸 유일한 쓰기 길** |
| `transitionDirectTask(...)` | `api.ts:397` | 상태 전이 | 지금 `CalendarPage.tsx:71` 이 쓴다 |
| `getTaskAssignments` · `getTaskChildren` · `getTaskHistory` … | `329` · `334` · `197` | 상세 부속 | 이번 범위 밖 |

`updateTask` 가 실제로 보내는 몸통 (`api.ts:243-261`):
```
expected_version  (필수)
title / description
start_date  또는  clear_start_date:true   (null 을 주면 지우기로 번역된다)
due_date    또는  clear_due_date:true
project_id  또는  clear_project:true
```
→ **날짜 드래그·좌우 손잡이는 `updateTask` 로 그대로 표현된다.** `TaskPatch` (`viewModels.ts:497-504`) 에 `start_date`·`due_date` 가 있고 `null` 이 「지우기」다.

#### 회의 쪽

| 호출 | 줄 | 엔드포인트 | 내는 것 |
|---|---|---|---|
| `listMeetings(cursor?)` | `api.ts:1145` | `GET /api/meetings[?cursor=]` | `{upcoming: MeetingRow[], past:{items, next_cursor}}` |
| `readMeeting(id)` | `api.ts:1149` | `GET /api/meetings/{id}` | `{meeting: MeetingInfo, agendas}` |
| `bookMeeting({title, purpose, starts_at, ends_at, room_id, attendee_ids, …})` | `api.ts:1153` | 예약 | 시간 있는 «만들기» |
| `updateMeetingInfo(...)` | `api.ts:1178` | 머리 수정 (`starts_at` 포함 — `api.ts:1182`) | 회의 시각 변경 |
| `readMeetingRooms(range?)` | `api.ts:1402` | `GET /api/meetings/rooms?starts_at=&ends_at=` | 회의실 |

`MeetingRow` (`viewModels.ts` — `export type MeetingRow`): `meeting_id` · `title: string|null` · **`starts_at`** · **`ends_at`** · `location` · `status` · `viewer_relation` · `created_by` · `attendee_count`.

**해석**: 회의는 **이미 시각을 가진 채 온다.** 시안의 `CAL_SCHEDULE` 중 `kind:'meeting'` 줄(`day`·`start`·`end`·`place`·`owner`)은 `MeetingRow` 의 `starts_at`/`ends_at`/`location`/`created_by` 로 **거의 1:1 로 채워진다.** 빠지는 것은 `repeat`(반복) 하나다 — `MeetingRow`·`MeetingInfo` 어디에도 반복 필드가 없다.

**모르는 것 / 제약**
- `listMeetings` 는 **기간 파라미터를 안 받는다** (`api.ts:1145-1147` — `cursor` 뿐). `upcoming` 전부 + `past` 를 커서로 거슬러 올라가는 꼴이다. → **「2026년 9월을 보여줘」를 한 번에 못 묻는다.** 보고 있는 달이 과거면 `past` 를 커서로 몇 번 긁어야 한다.
- 회의 «시간 이동» 은 `updateMeetingInfo` 로 되지만, 그것이 캘린더 드래그로 허용되는지는 시안이 말하지 않는다 — 시안에서 회의 카드는 `draggable:false` 다 (`calendar.v1.jsx:285`). 다만 **시간 블록의 세로 손잡이는 회의에도 붙는다** (§1-4). 시안 안에서도 이 둘이 어긋난다 → §7 OQ-4.

### 6-2. `DirectTask` ↔ 시안 `work-data.js` 1:1 대조표

**시안에만 있는 것 / 코드에만 있는 것을 양쪽 다 적는다.**

#### (a) 업무 — 시안 `WORK_TASKS` 항목 ↔ `DirectTask` (`viewModels.ts:186-270`)

| 시안 필드 | 예 (`…/handoff/shared/js/work-data.js`) | 코드 대응 | 비고 |
|---|---|---|---|
| `id` | `'w1'` (`:10`) | `task_id: string` (`viewModels.ts:187`) | 같다 |
| `title` | `'제품 소개서 스프린트'` (`:10`) | `title: string` (`:188`) | 같다 |
| `from` | `2` — **달 안의 일 번호** (`:10`) | `start_date?: string \| null` — **ISO `YYYY-MM-DD`** (`:193`) | **표현이 다르다** |
| `to` | `4` (`:10`) | `due_date?: string \| null` (`:194`) | **표현이 다르다** |
| `due` | `3` (`:15`) | `due_date` (같은 필드) | 시안은 `from/to` 와 `due` 를 **다른 필드로** 둔다. 코드는 `start_date` 유무로 구분한다 (`WorkViews.tsx:175-181`) |
| `owner` | `'유하람'` — **사람 이름 문자열** (`:10`) | `assignee?: {member_id, display_name} \| null` (`:210`) | 코드는 id+이름 객체 |
| `requester` | `'박혜진'` / `'-'` (`:10`) | **직접 대응 없다.** 가장 가까운 것은 `origin?: TaskOrigin \| null` (`:206`) · `assignment?: TaskAssignmentSummary` (`:200`) | **불일치** |
| `status` | `'progress'`·`'not-started'`·`'blocked'`·`'done'`·`'cancelled'` (`:10`,`:31`,`:13`,`:35`,`:38`) | `state: TaskState` = `open`·`in_progress`·`blocked`·`done`·`cancelled` (`viewModels.ts:121`) | **D4 가 시안 5종을 폐기.** 단 D4 의 6번째 값 `completion_submitted` 는 **코드에도 없다** → §7 OQ-1 |
| `group` | `'my'`·`'sent'`·`'done'` (`:10`,`:30`,`:35`) | **없다.** 화면이 `access`(`:204`)·`assignee`·`state` 로 갈라 만든다 | 시안의 캘린더 필터가 이것을 쓴다 (`…/handoff/calendar/js/data.js:6`) |
| `badge` / `badgeTone` | `'결정 요청'`/`'danger'` (`:13`) | **없다.** 대응은 `derived?: TaskDerived` (`:215`) 의 `assignment`·`approval`·`proposal` | 코드가 **더 구조적**이다 |
| `actions` | `'accept'`·`'confirm'` (`:13`,`:18`) | **없다.** 대응은 `allowedTaskTransitions(task)` (`WorkModals.tsx:133`) | |
| `starred` | `true` (`:16`) | **없다** | |
| `unread` | `true` (`:19`) | **없다** (업무에는. 요청에는 있다 — `WorkRequestReadReceipt`) | |
| `counterpart` | `'박민수'` (`:36`) | **없다** | |
| `closedAt` | `'09-02'` (`:35`) | `completed_at?: string \| null` (`:229`) | 코드가 ISO datetime |
| `sent` | `true` (`:38`) | **없다** | |
| — | | **코드에만 있는 것** (시안에 없다): `version`(`:189` — 낙관적 잠금, **쓰기에 필수**) · `block_reason`(`:190`) · `description`(`:192`) · `created_at`/`updated_at`(`:195-196`) · `organization_unit_id` · `origin_kind` · `visibility` · `lineage` · `access` · `project_id`(`:212`) · `preceding_task_ids`/`predecessors`(`:217,225`) · `approver_id`(`:227`) · `checklist`/`checklist_progress` · `references` · `delivery` · `parent`/`children`/`child_progress` · `derived` · `cancel_reason` · `started_at` · `reopened_at` | |

#### (b) 스케쥴 — 시안 `WORK_SCHEDULE` 항목 (`work-data.js:41-52`)

| 시안 필드 | 예 | 코드 대응 | 비고 |
|---|---|---|---|
| `id` | `'s1'` | 회의: `MeetingRow.meeting_id`. 업무 배정: **없다** | |
| `kind` | `'meeting'` \| `'task'` | 회의: 암시적. 업무 배정: **없다** | |
| `taskId` | `'w2'` (`:51`) | **없다** — 배정과 업무를 잇는 것이 없다 | |
| `title` | `'주간 스크럼'` | `MeetingRow.title: string \| null` | 회의만 |
| `day` | `7` (일 번호) | `MeetingRow.starts_at` (ISO datetime) | 표현 다름 |
| `start` / `end` | `'11:00'` / `'12:00'` | `starts_at` / `ends_at` | 표현 다름 |
| `place` | `'회의실 B'` | `MeetingRow.location: string \| null` | 같다 |
| `owner` | `'유하람'` | `MeetingRow.created_by: string` (id) | 이름 아님 |
| `repeat` | `'매주 월'` (`:42`) | **없다** | `MeetingRow`·`MeetingInfo` 어디에도 없다 |

### 6-3. 시간 배정을 프론트가 부르려면 무엇이 필요한가

> 백엔드에 아직 없다(BE 워커 조사 중). **계약을 정하지 않고**, 프론트가 §1 의 넷을 그리려면 **무엇이 있어야 하는지**만 적는다. 다음 판 계약의 초안 재료다.

**사실 — 지금 없는 것**
```bash
cd frontend && grep -rn "schedule\|Schedule\|time_slot\|slot" src/lib/api.ts
# → starts_at 4건(회의)뿐. 시간 배정 호출 0건.
```
`viewModels.ts` 에도 업무의 시각을 담는 타입이 없다 — `DirectTask` 의 날짜는 `start_date`·`due_date` 둘뿐이고 형식이 `YYYY-MM-DD` 다 (`updateTask` 가 `clear_*` 로 지우는 것도 날짜 단위다 — `api.ts:247-255`).

**프론트가 §1-3·§1-4 를 그리려면 필요한 것 (관측된 요구사항)**

| # | 필요한 것 | 왜 (근거) |
|---|---|---|
| D-1 | **보고 있는 기간으로 묻는 읽기** — 업무 시간 배정을 `[from, to]` 로 한 번에 | 주 뷰는 7일, 월 뷰는 최대 42일을 한 화면에 그린다 (`calendar.v1.jsx:22` · `week.jsx:14`). 지금 `listMeetings` 처럼 커서만 있으면 달을 옮길 때마다 긁어야 한다 |
| D-2 | **하나의 배정에 `task_id` 가 실려야 한다** | 시안이 `s.taskId === t.id` 로 업무 카드의 `meta` 줄을 만든다 (`calendar.v1.jsx:261`), 그리고 `canDrop` 이 그 업무의 기간을 본다 (`week.jsx:101-105`) |
| D-3 | **시각은 날짜+시각 한 벌** (회의와 같은 `starts_at`/`ends_at` 꼴이면 같은 렌더러를 쓴다) | 주 뷰는 분 단위로 위치를 계산한다 (`week.jsx:17` `wkMin` · `55` `px`) |
| D-4 | **만들기 — 멱등키** | 저장소 규칙: 「재전송은 영수증이다」(`lib/idempotency.ts`). 드래그 중 연타가 두 번째 배정이 되면 안 된다 |
| D-5 | **고치기 — `expected_version`** | 저장소의 모든 쓰기가 낙관적 잠금이다 (`api.ts:243` · `397` · `1178`). 세로 손잡이는 끌 때마다 부를 수 없다 → **언제 저장하는가**(놓을 때 한 번?)가 계약과 함께 정해져야 한다 |
| D-6 | **지우기** | 시안에 지우는 길이 없다(§1-4). 그래도 만들 수 있으면 지울 수 있어야 한다 |
| D-7 | **서버 쪽 「기간 밖 금지」** | `canDrop` 은 화면의 가드다 (`week.jsx:101`). 저장소 규칙상 권한·가능은 서버가 정본이라, 같은 규칙이 서버에도 있어야 한다 |
| D-8 | **업무가 `done`/`cancelled` 로 갈 때 배정이 어떻게 되는가** (D5) | 프론트가 «접는» 것인지 서버가 «지우는» 것인지에 따라 읽기 응답이 달라진다 → §7 OQ-3 |
| D-9 | **한 업무 / 하루 = 배정 하나인가** | 시안의 `addSlot` 이 같은 날의 기존 배정을 조용히 교체한다 (`calendar.v1.jsx:224`). 이것이 UI 편의인지 계약인지 시안이 말하지 않는다 → §7 OQ-7 |

**이미 있어서 안 만들어도 되는 것**
- 30분 스냅 시각 목록: `ds/TimeField.tsx:62` `timeSlots(step=30, min?, max?)`, `DEFAULT_STEP = 30` (`TimeField.tsx:41`). `formatTime`/`parseTime` (`:46`,`:52`) 도 있다.
- 시간 범위 입력: `ds/TimeField.tsx:176` `TimeRangeField`.

### 6-4. `api.ts` 밖의 `fetch`

**실제로 돌린 명령**
```bash
cd frontend && grep -rn "fetch(" src --include="*.ts" --include="*.tsx" | grep -v "\.test\."
```

**출력 — 9건 전부 `src/lib/api.ts` 안이다**
```
src/lib/api.ts:100, 115, 124, 274, 565, 1019, 1096, 1343, 1368
```

**해석**: **규칙 위반 자리가 없다.** `api.ts` 밖에서 `fetch` 를 부르는 곳은 0건이다.
**모르는 것**: `fetch` 만 셌다. `EventSource`/`WebSocket` 은 이 검색에 안 잡힌다 — `features/meetings/stream.ts` · `features/browser/liveTranscription.ts` 가 있으나 캘린더와 무관해 열지 않았다.

---

## 7. 상태값 (4-5) — D4 를 걸 자리

### 7-1. 지금 프론트가 업무 상태를 표시하는 자리 전부

**실제로 돌린 명령**
```bash
cd frontend && grep -rn "taskStateLabel\|taskStateTone\|StatusText" src --include="*.tsx" --include="*.ts" | grep -v "\.test\."
```

**사실 — 말(라벨)의 정본은 한 곳이다**

| 자리 | 줄 | 내용 |
|---|---|---|
| `lib/labels.ts:3-9` | — | `taskStateLabel`: open=시작 전 · in_progress=진행 중 · blocked=막힘 · done=완료 · cancelled=취소 |
| `lib/labels.ts:11-17` | — | `taskStateTone`: open=neutral · in_progress=accent · blocked=danger · done=success · cancelled=muted |
| `lib/labels.ts:26-39` | — | **파생 표시의 말 — 상태와 다른 표다**: `derivedAssignmentLabel`(수락 대기·담당 변경 대기) · `derivedApprovalLabel`(**확인 대기**·보완 요청·확인 완료) · `derivedProposalLabel` |
| `lib/labels.ts:41-47` | — | `cancelReasonLabel` (취소됨 — 직접/요청 거절/요청 철회/합의 취소) |

**사실 — 그리는 자리 (부품 3종 + 직접 호출 다수)**

| 그리는 꼴 | 자리 |
|---|---|
| `StatusText` (`<span class="status {state}">`) — 정의 `WorkModals.tsx:313-315` | `WorkViews.tsx:160`(TaskListRow) · `WorkViews.tsx:545`(칸반 머리) · `WorkModals.tsx:1362`(상세) · `WorkModals.tsx:2946` · `MyWorkPage.tsx:1070,1328` · `DailyReportPage.tsx:327,341` · `ActionCenter.tsx:88,490` |
| `Badge` + `taskStateLabel` | `shell/CalendarRail.tsx:150` (`tone={state==='blocked'?'danger':'neutral'}`) · `WorkModals.tsx:1766` · `WorkTables.tsx:208,212` |
| `.calendar-chip.{state}` **CSS 클래스로** | `WorkViews.tsx:358-365` — 상태를 **클래스 이름으로** 붙인다. 규칙은 `screens-b.css:764-792` (in_progress·done·blocked·cancelled 넷만; `open` 은 기본형) |
| `.timeline-bar {state}` | `WorkViews.tsx:465` · 라벨도 상태 글자 (`:471`) |
| 글자만 | `MessageList.tsx:713` · `RelationGraphPage.tsx:390,432` · `ProjectPage.tsx:321` · `WorkTables.tsx:578` · `WorkModals.tsx:1768,1792,1838,1843,1910,3033` |
| 상태 필터 목록 | `labels.ts:249` `taskFilterOptions = ["active","all","open","in_progress","blocked","done","cancelled"]` |

**해석**: 「상태를 말로 바꾸는 자리」는 `lib/labels.ts` 하나로 모여 있다(저장소 규칙대로다). 반면 **「상태를 색으로 바꾸는 자리」는 셋으로 흩어져 있다**: `taskStateTone`(객체) · `.status {state}`(CSS 클래스) · `.calendar-chip.{state}`(CSS 클래스). 캘린더가 시안대로 «유형 둘(업무/회의)» 로만 칠하면 셋째는 안 쓰게 된다.

### 7-2. `completion_submitted` 를 지금 화면이 어떻게 내고 있는가

**실제로 돌린 명령**
```bash
cd frontend && grep -rn "completion_submitted" src
```

**출력 — 4건, 전부 «없다» 는 말이다**
```
src/features/work/WorkModals.tsx:804:  /* 「확인 대기」는 상태가 아니라 파생 표시다 — 외부 계약에 `completion_submitted` 가 없다
src/features/work/TaskDelivery.test.tsx:142:  `completion_submitted` 는 외부 계약에 없다 (SPEC-003 §4 · SPEC-001 §4 State).
src/features/work/TaskLifecycleV2.test.tsx:571: 제출이 성공하면 밖으로는 `done` + `awaiting_review` 다 — `completion_submitted` 는 계약에 없다.
src/lib/viewModels.ts:113: * `completion_submitted` 는 **외부 계약에 없다.** 요청 업무의 완료 보고가 들어가면 밖으로는
```

`viewModels.ts:111-121` 전문(주석 + 타입):
> `completion_submitted` 는 **외부 계약에 없다.** … 내부 enum 은 백엔드에 남아 있지만 **그 값을 화면 타입으로 들이지 않는다** — 들이면 「승인 전 done」을 상태값으로 판단하는 코드가 다시 생긴다.
> `export type TaskState = "open" | "in_progress" | "blocked" | "done" | "cancelled";`

**대신 쓰는 것**
- `DerivedApproval = "awaiting_review" | "awaiting_revision" | "approved"` (`viewModels.ts:126`)
- 말: `derivedApprovalLabel.awaiting_review = "확인 대기"` (`labels.ts:31`)
- 그 값이 실제로 동작을 막는 자리: `reopenBlockedByApproval()` — `task.state==='done' && derived.approval ∈ {awaiting_review, awaiting_revision}` 이면 **전이 목록을 빈 배열로 만든다** (`WorkModals.tsx:125-138`).
- 칸반이 「완료 확인 대기」 칸을 두지 않는 이유도 같은 주석에 있다 (`WorkViews.tsx:490-491`).

**해석 / 충돌**
- D4 는 「`TaskState` 6종 … `completion_submitted`」 라고 한다. **프론트의 `TaskState` 는 5종이고, 6번째를 «일부러» 안 들인다.**
- D4 의 뜻(「완료 보고가 들어갔지만 아직 확인 안 된 업무를 캘린더에서 지우지 마라」)은 **지금 프론트 어휘로 이미 표현된다**: `state === 'done' && derived?.approval === 'awaiting_review'`.
- 이것을 「모순을 고쳐라」로 읽지 않는다 — **리포트에만 적는다** (§10 OQ-1).

### 7-3. 권한 envelope — 「할 수 있나」를 판단하는 자리

**실제로 돌린 명령**
```bash
cd frontend && grep -rn "canManageOwnTasks" src --include="*.tsx" --include="*.ts" | grep -v "\.test\."
cd frontend && grep -rn "allowed_commands\|requires_reason\|allowedTaskTransitions\|canTransition" src --include="*.tsx" --include="*.ts" | grep -v "\.test\."
```

**사실 — 판단이 걸리는 자리 셋**

| 층 | 자리 | 내용 |
|---|---|---|
| ① 세션 봉투 | `App.tsx:358` `canManageOwnTasks: has("task.self_manage")` | 「내 업무를 내가 다룰 수 있나」. `sharedWorkProps` 로 내려간다 (`App.tsx:353-365`) |
| ② 전이 표 | `WorkModals.tsx:133` `allowedTaskTransitions(task)` · `:141` `canTransition(task, action)` | **지금은 클라이언트 표다.** 주석 `WorkModals.tsx:100-102`: "**`allowed_commands` 가 생기면 갈아끼울 자리가 여기다.** 서버가 봉투에 … 실어 주면 `allowedTaskTransitions` 의 **몸통만** 그것을 읽게 바꾸면 된다" |
| ③ 진짜 `allowed_commands` | `viewModels.ts:691` `allowed_commands: ActionCommand[]` · `:768` `ActionCommand = {id, label, tone, requires_reason?}` | **액션 센터만** 쓴다 (`ActionCenter.tsx:415,464`) · 업무 요청 수락 (`WorkModals.tsx:826`) |

**캘린더에 걸리는 지점**
- `CalendarPage.tsx:13,23,115` 가 `canManageOwnTasks` 를 받아 **`TaskDetailDrawer` 에만** 넘긴다. **`TaskCalendar` 자체는 권한을 안 받는다** (`WorkViews.tsx:257-270` 의 props 에 없다) — 지금은 읽기 전용 격자라 받을 이유가 없었다.
- 시안의 드래그·리사이즈는 **전부 쓰기 동작**이다:
  - 날짜 드롭 / 좌우 손잡이 → `updateTask`(start_date·due_date) → **① `canManageOwnTasks`** 에 걸린다.
  - 시간 드롭 / 세로 손잡이 → 아직 없는 배정 API → **계약이 정해질 때 같은 봉투를 타야 한다** (D-7).
- 선례: `TaskKanban` 이 같은 문제를 이미 푼다 — `draggable={canManage && !busy}` (`WorkViews.tsx:553`), `onDragOver` 에서 `if (canManage) event.preventDefault()` (`WorkViews.tsx:540`), 허용 안 되는 이동은 `onInvalidMove` 로 **말해 준다** (`WorkViews.tsx:520-522`).
- **시안과 다른 점**: 시안은 금지를 **조용히** 한다(`canDrop` 이 거짓이면 아무 말 없다 — `week.jsx:205`). 칸반은 **문구로 말한다.** 어느 쪽을 따를지는 이번 조사가 정할 일이 아니다 → §10 OQ-8.

---

## 8. 스타일 (4-6) — 시안 CSS 를 얼마나 그대로 가져올 수 있나

### 8-1. 토큰 체계 — **같다**

**실제로 돌린 명령**
```bash
B="…/package 2"
grep -oE '\-\-scax-[a-z0-9-]+' "$B/handoff/calendar/css/calendar.css" | sort -u > /tmp/cal_tokens.txt   # 51종
cd frontend && grep -hoE '\-\-scax-[a-z0-9-]+[[:space:]]*:' src/styles/*.css | tr -d ' :' | sort -u > /tmp/repo_tokens.txt   # 143종
comm -23 /tmp/cal_tokens.txt /tmp/repo_tokens.txt   # → 출력 없음
```

**사실**
- 시안 `calendar.css` 가 쓰는 `--scax-*` 토큰: **51종.**
- 저장소 `styles/*.css` 가 정의하는 `--scax-*` 토큰: **143종.**
- **시안이 쓰는 51종 중 저장소에 없는 것: 0종.** `comm -23` 출력이 비었다.
- 정의 파일은 `styles/scax.css` 하나다 (`grep -ln 'scax-space-100[[:space:]]*:' src/styles/*.css` → `src/styles/scax.css`). `styles/index.css:33-35` 주석: "화면이 실제로 쓰는 이름 `--scax-*` 103종. 전부 `--ax-`·`--t-`·`--fw-` 의 별칭이다."
- 값이 정말 있는지 표본 확인: `--scax-color-accent-strong` (`scax.css:7`) · `--scax-control-height-md:39px` (`:123`) · `--scax-color-surface-selected:#f8faff` (`:177`) · `--scax-color-popover-current:#f4f5ff` (`:179`).
- 로드 순서는 `styles/index.css` 가 잡는다 — `fig-tokens → fig-typography → typography → product → scax → shell → components → workspace → meetings → screens-a → scrollbar → screens-b → ax`.

**해석**: **시안 `calendar.css` 의 토큰 참조는 한 글자도 안 고치고 그대로 옮겨진다.** `_ds_bundle.css` 의 토큰과 저장소 토큰은 **같은 이름 체계**다 (저장소가 그 번들에서 왔다고 `index.css` 주석이 말한다).

### 8-2. 클래스 이름 — **충돌 0, 재사용 0**

**실제로 돌린 명령**
```bash
grep -oE '\.scax-[a-zA-Z0-9_-]+' "$B/handoff/calendar/css/calendar.css" | sort -u > /tmp/cal_classes.txt        # 71종
cd frontend && grep -rhoE '\.scax-[a-zA-Z0-9_-]+' src/styles/*.css | sort -u > /tmp/repo_classes.txt            # 485종
comm -12 /tmp/cal_classes.txt /tmp/repo_classes.txt   # 겹치는 것 → 출력 없음
comm -23 /tmp/cal_classes.txt /tmp/repo_classes.txt   # 시안에만 → 71종 전부
```

**사실**
- 시안 `calendar.css` 의 `.scax-*` 클래스 **71종 전부가 저장소에 없다.**
- 저장소의 `.scax-*` 클래스 485종 중 겹치는 것 **0종.**
- 71종의 갈래: `.scax-cal-*` 9 · `.scax-month__*` 13 · `.scax-event*` 15 · `.scax-week*` 33 · `.scax-inbox-card--draggable` 1.
- **혼동 주의**: 저장소에 `.scax-month-grid`(`components.css:223,225` — `CalendarRail` 의 작은 달 격자)가 있고, 시안에는 `.scax-month__grid`(`calendar.css:19`)가 있다. **다른 이름이다 — 충돌하지 않지만 읽는 사람이 헷갈린다.**

### 8-3. `calendar.css` 103줄 — 그대로 쓸 것 / 다시 쓸 것

**사실 기반 분류.** 「그대로」는 *토큰이 다 있고 클래스가 안 겹치므로 값 수정 없이 옮겨진다* 는 뜻이다.

| 갈래 | 줄 | 판정 | 근거 |
|---|---|---|---|
| 툴바 `.scax-cal-main` · `.scax-cal-toolbar*` | 4-11 (8줄) | **그대로** | 토큰 전부 있음. 다만 `.scax-cal-main{flex:1 1 auto;min-height:0}` 은 **바깥 `.scax-page-scroll`(`shell.css:177`)과 스크롤 주인이 겹친다** — §3 |
| 월 격자 `.scax-month*` | 14-31 (17줄) | **그대로** | 토큰 전부 있음 |
| 일정 조각 `.scax-event*` | 34-53 (18줄) | **그대로** | 단, 46·85행에 **원색 `#fff` 리터럴**이 있다 |
| 드래그 상태 `--draggable` · `--drop` · `.scax-inbox-card--draggable` | 55-59 (5줄) | **그대로** | |
| 레일 `.scax-cal-rail__*` | 60-61 (2줄) | **그대로** | `.scax-inbox-card` 본체 규칙은 이미 저장소에 있다 (`components.css:111-121`) |
| 주 뷰 `.scax-week*` | 65-103 (39줄) | **그대로** | 토큰 전부 있음. 87행 `repeating-linear-gradient(… 0 1px, transparent 1px 56px)` 의 **56px 는 JS 상수 `WEEK_ROW`(`week.jsx:6`)와 짝**이다 — 한쪽만 고치면 격자가 어긋난다 |
| 주석 · 빈 줄 | 1,2,3,12,13,32,33,39,45,62,63,64,88,94 | — | |

**즉 103줄 중 규칙 89줄은 값 수정 없이 옮겨진다.** 「다시 써야 하는 것」은 규칙의 값이 아니라 **바깥과의 접합 셋**이다:

1. **스크롤 주인** — 시안은 화면이 칸을 꽉 채우고 안에서 스크롤한다(`calendar.css:4,65,67`). 저장소 기본 `.scax-page-scroll` 은 바깥이 스크롤한다(`shell.css:177`). 회의 화면은 `--fixed` 변종으로 풀었다(`shell.css:182` · `App.tsx:458`). → **접합 결정이 필요하다.**
2. **`#fff` 원색 2자리** (`calendar.css:29` `.scax-month__date--today`, `:46` `.scax-event--task`, `:85` `.scax-week__day-date--today` — 총 3자리). 저장소 규칙은 「컴포넌트에 임의 hex 리터럴을 두지 않는다」(`roles/.../rules.md`)지만, **CSS 파일에는 선례가 있다**: `components.css` 7건 · `scax.css` 33건 · `shell.css` 2건 · `screens-a.css` 3건 · `ax.css` 37건 (`grep -oiE '#[0-9a-f]{3,8}\b'` 로 셌다). 저장소에 `--scax-color-ink-inverse` 가 있다(`screens-b.css:757` 이 쓴다).
3. **파일 등록** — 새 CSS 는 `styles/index.css` 에 한 줄로 실려야 한다. 그 자리의 규약이 파일 안에 적혀 있다 (`index.css:74-78`: "싣는 차례가 곧 우선순위다 … 이 자리에서 git 충돌이 나면 답은 언제나 「세 줄 다 살린다」").

**모르는 것**: `…/handoff/my-work/css/components.css`(312줄) 는 `Calendar.html:10` 이 캘린더보다 **먼저** 싣는다. 저장소 `styles/components.css` 가 그 파일과 얼마나 같은지는 이번에 바이트 비교를 하지 않았다 — `index.css:48-52` 주석은 "원본 `handoff/my-work/css/components.css` 와 byte-identical 이다" 라고 적는다(주석의 주장이고, 확인하지 않았다).

---

## 9. 검증 — 아무것도 안 고쳤다는 증거

```bash
$ git -C /Users/kknaks/orca/workspaces/Strong_hajin/strong-hajin-calendar status --short
$ echo "exit=$?"
exit=0
```
**출력 없음** — 워크트리는 깨끗하다. 코드 파일을 하나도 만들거나 고치거나 지우지 않았다.
(이 리포트 파일은 워크트리 밖 `…/orchestration/work/strong-hajin-calendar/fe-survey-report.md` 에 있다 — allowed_paths 그대로다.)

테스트·빌드는 돌리지 않았다 (고친 것이 없으므로 발주 §7 에 따라 생략).

---

## 10. Open Questions — 정하지 못한 것

> 임의로 결정하지 않았다. 각각 **무엇이 걸려 있고 누가 답해야 하는지**만 적는다.

**OQ-1 · `completion_submitted` 를 프론트 타입에 들이는가 (D4)**
D4 는 `TaskState` 6종이라고 한다. 프론트의 `TaskState` 는 5종이고, `viewModels.ts:111-120` 이 **「들이면 「승인 전 done」을 상태값으로 판단하는 코드가 다시 생긴다」는 이유로 일부러 뺐다**고 적는다. D4 의 의도(「미완으로 취급해 캘린더에 계속 낸다」)는 지금 어휘로 `state==='done' && derived?.approval==='awaiting_review'` 다 (`WorkModals.tsx:125-138` 이 같은 조건을 이미 쓴다).
→ **6번째 상태값을 들일 것인가, 아니면 D4 의 뜻을 파생 표시로 구현할 것인가.** 답이 §6-3 D-8 과 §7-2 를 동시에 움직인다. **코디네이터·spec 결정.**

**OQ-2 · 캘린더가 상태를 색으로 말하는가**
시안은 **말하지 않는다** — 유형 둘(업무=진한 면 / 회의=연한 면)로만 칠한다 (`calendar.css:45-47`). 지금 코드는 상태 4종을 칩 색으로 말한다 (`screens-b.css:774-792`). 시안을 따르면 캘린더에서 상태가 **색으로 안 읽힌다.**
→ 시안을 깎지 않는다는 원칙대로면 시안이 이긴다. 그러면 **상태를 어디서 읽는가**(좌측 카드? 상세?)가 빈다. 시안 `ItemCard` 는 Badge 를 **유형(회의/업무)** 에만 쓰고 상태를 안 낸다 (`calendar.v1.jsx:160`). **디자이너 확인 필요.**

**OQ-3 · D5 의 「접는다」 기준이 상태인가 분류인가**
D5 는 「업무가 done·cancelled 로 가면 배정도 같이 접는다」 고 한다. 시안은 `group !== 'done'` 으로 거른다 (`…/handoff/calendar/js/data.js:6`) — **상태가 아니라 화면 탭 분류**이고, `status:'cancelled'` 인 `d4` 도 `group:'done'` 이라 같이 빠진다 (`work-data.js:38`).
한편 **지금 코드는 정반대로 동작한다**: `CalendarPage.tsx:35` 가 `getTasks(true)`(=`include_closed=true`)를 **일부러** 부르고, `.calendar-chip.done`/`.cancelled` CSS 까지 있다 (`screens-b.css:779,789`).
→ **완료·취소 업무를 캘린더에서 빼는 것이 이번 판의 결정인가.** 지금 화면의 동작이 바뀐다.

**OQ-4 · 회의를 캘린더에서 옮길 수 있는가 (시안 내부 모순)**
시안에서 회의 카드는 `draggable: false` 다 (`calendar.v1.jsx:285`). 그런데 **시간 블록의 세로 손잡이는 회의 블록에도 붙는다** (`week.jsx:231-232` — `shownSlots` 를 가리지 않는다). 즉 **좌측에서는 못 끌지만 격자 위에서는 시간을 늘릴 수 있다.**
→ 의도인지 시안의 빠뜨림인지 모른다. 회의 시각 변경 API 는 있다 (`updateMeetingInfo` — `api.ts:1178,1182`). **시안 작성자 확인 필요.**

**OQ-5 · 캘린더 화면의 오른쪽 레일**
시안은 `AppBody railLeft` 만 쓴다 (`calendar.v1.jsx:293`). `MyWorkPage` 는 좌우 둘 다 쓴다 (`MyWorkPage.tsx:901-921`). 셸 규약상 안 넘기면 그 칸이 안 그려진다 (`AppShell.tsx:79`).
→ **캘린더에서 오른쪽 칸을 비우는 것이 맞는가.** 지금 `CalendarRail`(업무 화면 우측)과 이 화면이 같은 일을 다른 크기로 하게 된다.

**OQ-6 · `GutterList` 이름을 누가 갖는가**
`ds/GutterList.tsx:20` 이 이미 다른 부품이다(§4-2). 시안의 레일형 목록은 `shell/InboxRail.tsx:103-114` 에 인라인으로만 있다.
→ **기존 것을 개명할지, 새것에 다른 이름을 줄지.** 기존 `GutterList` 소비처를 이번 조사에서 세지 않았다(캘린더와 무관해서다).

**OQ-7 · 한 업무 / 하루 = 시간 배정 하나인가**
시안 `addSlot` 이 같은 `(taskId, day)` 의 기존 배정을 **조용히 교체한다** (`calendar.v1.jsx:224`). 이것이 계약 제약인지 프로토타입 단순화인지 시안이 말하지 않는다. §6-3 D-9.

**OQ-8 · 금지를 조용히 할 것인가 말로 할 것인가**
시안은 조용하다 (`week.jsx:205` — `canDrop` 이 거짓이면 `preventDefault` 를 안 불러 브라우저가 거절, 문구 없음). 저장소의 같은 자리(칸반)는 **문구로 말한다** (`WorkViews.tsx:520-522` `onInvalidMove`).
→ 접근성·일관성 판단이 필요하다.

**OQ-9 · 날짜 표현 — 시안의 `day:number` 를 무엇으로 읽을 것인가**
시안 전체가 «달 안의 일 번호» 로 돌아간다 (`work-data.js:10` `from: 2` · `week.jsx:71` `Number(col.getAttribute('data-day'))`). 그래서 시안 안에서는 **달·주를 넘는 드래그·리사이즈가 표현되지 않는다** (§1-1, §1-2 의 가드가 그 결과다). 코드는 ISO 날짜라 **넘을 수 있다.**
→ 달 경계를 넘는 이동·조정을 허용하는가. 허용하면 시안에 없는 동작을 **더하는** 것이고, 막으면 ISO 로 표현 가능한 것을 **줄이는** 것이다.

**OQ-10 · 「더보기」 단추의 뜻**
시안 좌측 레일 바닥의 「더보기」에 핸들러가 없다 (`calendar.v1.jsx:187`). 무엇을 더 보여주는지 시안에 없다.

**OQ-11 · 회의 목록을 기간으로 못 묻는다**
`listMeetings` 는 커서만 받는다 (`api.ts:1145`). 월 뷰가 과거 달을 볼 때 `past` 를 커서로 몇 번 긁어야 한다 (§6-1).
→ BE 에 기간 파라미터를 요청할지, 프론트가 긁을지. **BE 워커 조사 결과와 합쳐 spec 이 정한다.**

**OQ-12 · 「오늘」의 출처**
시안은 `CAL_TODAY = new Date(2026, 8, 15)` 로 하드코딩한다 (`calendar.v1.jsx:10`). 코드에는 `seoulToday()` 가 있다 (`lib/labels.ts` — `WorkViews.tsx:271` 등이 쓴다). 시안의 하드코딩은 목데이터용으로 읽었지만, 그렇게 못 박지 않았다.

---

## 11. 못 찾은 것 / 안 본 것

- **`backend/` 를 열지 않았다** (발주 §7). D4 의 6종 `TaskState` 가 백엔드에 실제로 그렇게 있는지 **확인하지 않았다** — §10 OQ-1 은 프론트 쪽 사실만으로 적었다.
- `_ds_bundle.css`(4069줄) · `_ds_bundle.js`(1862줄) 는 **전수로 읽지 않았다.** 토큰 비교(§8-1)는 저장소 `styles/*.css` 의 정의와 시안 `calendar.css` 의 **참조**를 맞춘 것이고, 번들 자체와 저장소 토큰의 «값» 이 같은지는 안 봤다.
- `styles/components.css` 가 `…/handoff/my-work/css/components.css` 와 정말 byte-identical 인지 **비교하지 않았다** (`index.css:48` 주석의 주장을 그대로 옮겼다).
- `EventSource`/`WebSocket` 호출은 §6-4 의 `fetch` 검색에 안 잡힌다 — 캘린더와 무관해 열지 않았다.
- 시안의 다른 화면(`my-work.v2.jsx` · `workspace.v1.jsx` · `projects.v1.jsx` · `files.v1.jsx`)은 발주 §1 의 SSOT 목록에 없어 **읽지 않았다.** 단 `work-data.js`(캘린더와 공용) 와 `scax-ui.jsx`·`work-modal.jsx`(부품) 는 읽었다.
- `ds/GutterList.tsx` 의 **기존 소비처를 세지 않았다** (§10 OQ-6) — 캘린더와 무관해서다. 개명을 검토하려면 그 수가 필요하다.
