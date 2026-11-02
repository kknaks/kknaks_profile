# WORK-004 Phase FE-1 결과 보고 — 화면 골격: 3분할 · 좌측 레일 · 월/주 뷰

## 상태: done

- 워크트리 `/Users/kknaks/orca/workspaces/Strong_hajin/strong-hajin-calendar`, 브랜치 `kknaksss/strong-hajin-calendar`
- **커밋·push 하지 않았다.** 변경은 전부 uncommitted 로 남아 있다. base 는 `2a85176`(BE-2) 그대로다.
- `allowed_paths` 준수 — 고친 파일 전부가 `frontend/` 아래다. `backend/`·`docs/`·`para/` 0건.

---

## 0. 선행 확인 ① — **한 줄** (작업 0)

> **핸드오프 `_ds_bundle.css` 의 `--scax-*` 정의 143줄(고유 139종)이 저장소 `styles/scax.css` 의
> 정의와 값까지 완전히 같다 — 정규화 후 `diff` 출력 0. 시안 `calendar.css` 가 참조하는 51종은
> 전부 그 안에 있다. `_ds_bundle.js` 에는 토큰 «정의» 가 없다(`--scax-` 등장 1회, 참조).
> 고칠 것이 없었고, 값의 정본은 저장소 파일이다.**

실제로 돌린 명령(정규화 = 이름/값 쌍만 뽑아 공백 접기 후 정렬):

```bash
B=".../reference/2026-09-10-sc-meeting/package 2"
perl -ne 'while(/(--scax-[a-z0-9-]+)\s*:\s*([^;}]+)[;}]/g){...}' "$B/_ds_bundle.css" | sort -u   # 143줄
perl -ne '...' frontend/src/styles/scax.css                                                     | sort -u   # 143줄
diff <(bundle) <(repo)          # → 출력 없음
comm -23 cal_tokens.txt repo_names.txt   # 시안 51종 중 저장소에 없는 것 → 출력 없음
```

이 사실은 `frontend/src/styles/calendar.css` 머리 주석에도 박아 두었다.

---

## 1. 변경 파일 (수정 9 · 신규 9)

### 수정

| 파일 | 무엇 |
|---|---|
| `frontend/src/features/calendar/CalendarPage.tsx` | **재작성.** 「이 화면은 업무만 낸다」 주석이 뒤집혔다 — 합본 조회 한 번이 업무·회의를 함께 싣는다 |
| `frontend/src/App.tsx` | `:468` 이 `onRegisterRails` 를 넘긴다(선례 `MyWorkPage.tsx:899-921`) + 캘린더를 `.scax-page-scroll--fixed` 편으로 옮겼다 |
| `frontend/src/lib/api.ts` | `getCalendar` · `createTaskSchedule` · `updateTaskSchedule` · `listMeetingsInRange` (+62줄, 삭제 0) |
| `frontend/src/lib/viewModels.ts` | `CalendarEntry`(`CalendarTaskRow`\|`CalendarMeetingRow`) · `TaskScheduleRow` · `TaskScheduleMutation` · `ScheduleRelease` (+93줄, 삭제 0). **`TaskState` 5종 그대로** |
| `frontend/src/lib/labels.ts` | `calendarScreen` · `calendarTabLabel` · `calendarViewLabel` · `calendarHourLabel` · `calendarCursorText` · `calendarDow` (+61줄, 삭제 0) |
| `frontend/src/ds/Empty.tsx` | **`icon` prop — additive** (G-CAL-02) |
| `frontend/src/ds/Empty.test.tsx` | additive 임을 지키는 검사 2건 추가 |
| `frontend/src/styles/index.css` | `@import "./calendar.css"` 한 줄 |
| `frontend/src/shell/AppShell.test.tsx` | 가드 한 줄 — 「`--fixed` 는 회의뿐」 → 「회의·캘린더」 (§4 에 이유) |

### 신규

`frontend/src/features/calendar/` — `calendarModel.ts`(355) · `MonthGrid.tsx`(113) · `WeekGrid.tsx`(166) ·
`ScheduleRail.tsx`(102) · `ScheduleCard.tsx`(61) · `EventBar.tsx`(55) ·
`calendarModel.test.ts`(195) · `CalendarPage.test.tsx`(198) · `frontend/src/styles/calendar.css`(134)

---

## 2. 구현 요약 — 작업 0~8

1. **작업 1 · 3분할** — `App.tsx` 가 `onRegisterRails={registerSurfaceRails}` 를 넘기고,
   `CalendarPage` 가 `{ left: <ScheduleRail …/> }` 만 등록한다.
2. **작업 2 · 오른쪽 레일은 비운다** — `right` 를 아예 안 넘긴다. 셸 규약상 그 칸이 렌더되지 않는다.
   떠날 때 `onRegisterRails({})` 로 되돌린다(MyWorkPage 와 같은 결).
3. **작업 3 · 본문 스크롤** — 캘린더가 회의와 같은 `.scax-page-scroll--fixed` 를 쓴다.
   `.scax-cal-main{flex:1 1 auto;min-height:0}` 과 바깥 스크롤이 주인을 다투던 자리다.
4. **작업 4 · `api.ts`·`viewModels.ts`** — 아래 §3.
5. **작업 5 · 부품 신설** — DS-gaps 처분표 그대로(§5).
6. **작업 6 · 월/주 렌더링, 읽기만** — 띠는 **`span_from`·`span_to`** 로만 그린다.
   `features/work` 의 `taskSpan()` 을 **한 번도 부르지 않는다**(`grep` 확인).
7. **작업 7 · 탭 셋 · 날짜 선택 · lane 상한 · 「오늘」** — 「오늘」의 출처는 `seoulToday()`.
   월 lane 상한 4 + `+N건 더`, 주 종일 lane 상한 3 + 「N건 펴기 / 접기」.
   주·월 이동은 **선택을 항상 푼다**.
8. **작업 8 · 격자는 상태를 말하지 않는다** — 조각의 유형 클래스가 `--task`·`--meeting` 둘뿐임을
   검사로 못 박았다. 좌측 카드도 **유형 배지 하나뿐**이다 (K15 — §4 의 판단 참조).

### 한 화면 = 한 요청

`getCalendar(from, to)` 를 **그려지는 칸 전부**로 한 번 부른다 — 월 뷰는 달 밖 칸까지(35~42일),
주 뷰는 이레. **탭 전환은 다시 묻지 않는다** — 받아 둔 한 배열을 `calendarModel` 이 걸러 낸다.
검사가 `toHaveBeenCalledTimes(1)` 로 지킨다.

### 함정 일곱 — 어떻게 닫았나

| # | 함정 | 이 판에서 |
|---|---|---|
| 1 | `start_date`·`due_date` 로 그리면 뒤집힌 업무가 어긋난다 | 띠·레일 범위 전부 `span_from`·`span_to`. 원본 둘은 **카드의 말**(「…마감」)에만 닿는다 — 「마감만 있다」와 「하루짜리 기간」은 정규화 구간이 같아서 그것으로만 갈린다 |
| 2 | 회의는 UTC ISO, 업무 배정은 `on_date`+`HH:MM` | `seoulDate()`·`seoulClock()` 이 회의 쪽을 Asia/Seoul 로 옮겨 **같은 꼴**로 만든다. 자정을 넘는 회의는 그 날 끝까지만 그린다 |
| 3 | `schedules[]` 에 `task_id` 가 없다 | 배열이 언제나 자기 업무 행 안에 실려 오므로 **행이 곧 소속**이다. 투영할 때 부모 행의 `task_id`·`title` 을 붙인다 |
| 4 | `completion_submitted` → `"done"` 투영 | **좌측 카드가 상태를 내지 않는다.** 검사가 상태 라벨 5종이 레일에 없음을 지킨다 |
| 5 | `is_active_assignee` 가 없다 | 행마다 묻지 않는다. 축이 `my_work` 라는 사실에 기대고, 쓰기는 FE-2 에서 서버 판정에 맡긴다 |
| 6 | 기간 없는 업무도 행으로 온다 | 격자에는 안 서고(`span` 이 `null`), **레일에는 선다**(R2 — 「날짜부터」). 날짜를 고른 동안에는 어느 날에도 안 걸치므로 빠진다 |
| 7 | `from`·`to` 둘 다 필수 · 역전이면 422 | 구간을 `monthGridDays`/`weekGridDays` 가 만들어 **언제나 `from <= to`** 다 |

---

## 3. 계약 준수 — `api.ts` 밖에서 `fetch` 하지 않았다

```bash
$ grep -rn "fetch(" frontend/src --include='*.tsx' --include='*.ts' | grep -v lib/api.ts | grep -v '\.test\.'
(출력 없음 — 새 파일 어디에도 fetch 가 없다)
```

- `getCalendar(from, to)` → `GET /api/calendar?from=&to=`
- `createTaskSchedule(taskId, {on_date, starts_at, ends_at}, idempotencyKey)` → `POST`, `Idempotency-Key` 필수,
  `expected_version` **안 보낸다**
- `updateTaskSchedule(scheduleId, expectedVersion, {starts_at, ends_at})` → `PATCH`, `on_date` **안 보낸다**
- `listMeetingsInRange(from, to)` → `GET /api/meetings?from=&to=` (배열)

> **⚠ `listMeetings(cursor)` 의 시그니처를 바꾸지 않고 옆에 함수를 하나 더 세웠다.** 발주서는
> 「`listMeetings` 에 기간 인자」라고 적었지만, 인자 없는 경로는 `{upcoming, past}` 라는 **다른 모양**이고
> 회의 화면이 그것을 쓴다 — 한 함수에 두 모양을 담으면 기존 소비처가 반환형을 좁혀야 한다.
> **계약이 아니라 FE 내부의 이름 문제**라 이쪽을 골랐다. 서버 표면은 그대로다.
> 캘린더 자신은 **이 함수를 쓰지 않는다** — 합본 조회가 회의까지 싣기 때문이다(한 화면 = 한 요청).
> FE-2 도 안 쓸 가능성이 높다. 발주서 §4 가 요구해서 표면만 열어 뒀다.

`createTaskSchedule`·`updateTaskSchedule` 도 **이번 판에서는 부르는 곳이 없다**(FE-2 가 쓴다).
발주서 작업 4 가 「배정 CRUD」를 FE-1 에 배치해서 계약이 신선할 때 박아 둔 것이다.

`ScheduleRelease` 타입도 세워 뒀지만 **`DirectTask` 에는 칸을 더하지 않았다** — 읽는 자리가 FE-2 라,
지금 더하면 쓰는 곳 없는 필드가 공용 타입에 남는다.

---

## 4. 판단한 것 — 셋. **조용히 정하지 않았다**

### (가) 좌측 카드가 상태를 내지 않는다 — **K15 를 따랐다**

SPEC §2.6 과 DS-gaps G-CAL-08 은 「좌측 카드는 **기존 상태 톤**을 쓴다」고 적는다.
DEC-003 **증보 K15** 와 이번 발주서 §2-4 는 「좌측 카드는 **유형만** 낸다」고 적는다. **둘이 어긋난다.**

**K15 를 따랐다** — 증보가 나중이고, 이유가 구체적이다: 합본 조회 행에 `derived` 가 없어
승인 대기인 업무가 카드에서 **「완료」로 읽힌다**. 톤만 빌려 와도 같은 거짓말이 된다.
`ScheduleCard` 의 docstring 이 그 이유를 들고 있고, 검사가 상태 라벨 5종의 부재를 지킨다.
**SPEC §2.6 · G-CAL-08 의 그 줄은 K15 로 덮인 것으로 읽었다 — 다르게 보면 말해 달라.**

### (나) `AppShell.test.tsx` 의 가드 한 줄을 고쳤다

`「--fixed 는 회의뿐」`을 `「회의·캘린더」`로 바꿨다. **작업 3 이 시킨 변경이라 가드가 낡은 것**이고,
이 파일은 발주서가 「고치지 않지만 걸리는 회귀 가드」로 못 박은 목록(전부 `backend/tests/architecture/`)에
없다. 고친 줄은 **한 줄**이고, 다른 아홉 화면이 문서형(`--fixed` 아님)임은 그대로 지켜진다.

### (다) 「업무 만들기」 머리 단추를 **세우지 않았다**

시안 머리에는 `업무 만들기` 단추가 있다(`calendar.v1.jsx:292`). 세우지 않은 이유:
**DS-gaps 처분표에서 G-CAL-03 의 Phase 칸이 `—`** 다 — FE-1 도 FE-2 도 아니다.
FE-1 완료 판정 아홉 줄에도 없다. 기존 `CreateWorkModal` 을 붙이려면 후보 목록 넷을 따로 읽어야 해서
(`MyWorkPage` 가 하는 일) 범위가 눈에 띄게 넘친다.
**세울지 말지는 코디네이터가 정해 달라** — 붙이는 일 자체는 작다(모달은 이미 있다).

---

## 5. DS-gaps 8건 처분 — 전부 배치했다

| ID | 처분 | 어디에 |
|---|---|---|
| G-CAL-01 | **만들었다** — `ScheduleRail`. **저장소 DS 의 `GutterList` 와 다른 이름**이다(개명 안 했다) | `features/calendar/ScheduleRail.tsx` |
| G-CAL-02 | **만들었다** — `Empty` 의 `icon`, **additive** | `ds/Empty.tsx` |
| G-CAL-03 | **만들지 않았다** — §4(다) |
| G-CAL-04 | **만들었다** — `ScheduleCard`. `.scax-inbox-card` 계열 재사용, `--draggable` 은 FE-2 | `features/calendar/ScheduleCard.tsx` |
| G-CAL-05 | **만들었다(FE-1 몫)** — 띠·`+N건 더`. 손잡이·고스트 CSS 는 실려 있고 **쓰는 곳이 FE-2** | `features/calendar/EventBar.tsx` |
| G-CAL-06 | **만들었다** — `MonthGrid`·`WeekGrid`. **`TaskCalendar` 를 한 글자도 고치지 않았다** | `MonthGrid.tsx` · `WeekGrid.tsx` |
| G-CAL-07 | **만들지 않았다** — 머리는 `title`+`actions` 만 |
| G-CAL-08 | **격자에 만들지 않았다** — 유형 둘로만. 카드도 §4(가)에 따라 상태를 안 낸다 |

---

## 6. 검증 결과 (수치)

**기준선을 먼저 쟀다** (아무것도 고치기 전, `npm ci` 직후):

| | 기준선 | 지금 |
|---|---|---|
| `make frontend-test` (Node 20.20.0) | **65 파일 / 823 통과 / 0 실패** | **67 파일 / 855 통과 / 0 실패** |
| `cd frontend && npx tsc --noEmit` | **exit 0** | **exit 0** |

- **기존에 깨져 있던 실패: 0건.** 「무관」으로 분리할 것이 없다.
- 늘어난 것: 파일 2(`calendarModel.test.ts` 19건 · `CalendarPage.test.tsx` 11건) + `Empty.test.tsx` 2건 = **32건**.
- 도중에 한 번 깨진 것 하나 — `AppShell.test.tsx` 의 `--fixed` 가드. **우리가 만든 변경이고 §4(나)에서 고쳤다.**
- 같은 검증을 중복 실행하지 않았다: 전체 스위트 1회 + `tsc` 1회가 최종 수치다.

### `ds/Empty.tsx` 소비처를 **한 곳도 고치지 않았다** — 증거 둘

```bash
$ grep -rln --include='*.tsx' --include='*.ts' 'ds/Empty"|from "./Empty"' frontend/src | grep -v Empty.test
21개 파일  (그중 1개가 이번에 새로 만든 features/calendar/ScheduleRail.tsx → 기존 소비처 20곳)
$ git status --short          # 그 20곳 중 diff 에 오른 파일: 0개
$ cd frontend && npx tsc --noEmit ; echo $?
0                              # 20곳이 그대로 컴파일된다
```

`icon` 은 **선택 prop** 이고, 안 넘기면 `variant` 가 글리프를 고르던 경로가 **글자 그대로 그대로**다.
검사 두 건이 그 둘을 함께 지킨다(안 주면 예전 글리프 · `variant="error"` 는 주더라도 경고 글리프).

> 발주서는 소비처를 **19곳**으로 셌고 실제는 **20곳**이다(`ds/Empty.tsx` 자신과 테스트 제외).
> 그 파일 docstring 은 또 **29곳**이라고 적어 뒀다 — 바퀴 3a 시절 수치가 낡은 것으로 보인다.
> **셋 다 「한 곳도 안 고쳤다」에는 영향이 없다.** docstring 의 숫자는 이 판에서 건드리지 않았다.

### 완료 판정 아홉 줄

- [x] `make frontend-test` · `npx tsc --noEmit` 통과
- [x] `ds/Empty.tsx` 소비처가 전부 그대로 컴파일된다 — 한 곳도 안 고쳤다
- [x] 선행 확인 ①의 결과가 한 줄로 기록됐다 (§0 · `styles/calendar.css` 머리)
- [x] 3분할이고 오른쪽 레일이 비어 있다 · 탭 셋이 레일과 격자를 **동시에** 가른다 — 검사 2건
- [x] 주 뷰가 종일 칸 + 0~24시이고 **8시에 맞춰 열린다**(`scrollTop === 448`) · 월 뷰가 **완전히 달 밖인
      마지막 주를 지운다**(42 → 35) — 검사 2건
- [x] **한 화면 = 한 요청** — `toHaveBeenCalledTimes(1)`, 탭 전환에도 그대로
- [x] **뒤집힌 업무의 띠가 서버 구간대로** 그려진다(`start_date` 3/6 이 아니라 3/4~3/6) · `taskSpan()` 미사용
- [x] 회의 카드에 **주최자 이름**이 뜨고 member id 가 안 보인다
- [x] **공유받은 다음 주 회의가 그 주에 제자리로** 선다 — 검사 1건
- [x] 격자에 **상태 색이 없다** · 새 레일 부품이 `GutterList` 와 **다른 이름**(`ScheduleRail`)

---

## 7. 범위 — 당겨 하지 않은 것

FE-2 의 것은 **하나도 만들지 않았다**: 드래그·드롭·좌우/세로 손잡이·고스트·시간 배정 생성·
금지 문구·`schedule_release` 알림·WARN-A 판단. 시안 CSS 의 해당 규칙(`--resizable`·`--ghost`·
`--drop`·`--draggable`·`__slot-handle`·`__ghost`)은 **파일에 실려 있고 쓰는 곳이 없다** —
FE-2 가 클래스를 붙이면 그대로 산다.

백엔드 0건. 커밋·push·PR 0건.

---

## 8. 미결 · 코디네이터가 볼 것

1. **§4(가) — SPEC §2.6·G-CAL-08 과 K15 의 어긋남.** K15 를 따랐다. 계약을 고치지 않았고 보고만 한다.
2. **§4(다) — 「업무 만들기」 머리 단추.** 세울지 정해 달라. 세운다면 작업은 작다.
3. **달 밖 칸에 일정을 그리지 않는다 — 시안 그대로.** 그런데 조회는 달 밖 칸까지 받고 **레일에는
   그 날의 회의가 선다.** 시안도 같은 어긋남을 갖는다(월 뷰 레일에 범위 필터가 없다).
   「달 밖 칸에도 일정을 그린다」로 가면 어긋남이 사라지지만 **시안 화면과 달라진다** —
   레이아웃 정본을 건드리는 일이라 **정하지 않고 둔다.**
4. **주 뷰 머리의 「N주차」** — 시안은 목데이터 기준으로 셌다. 우리는 **그 주의 수요일이 속한 달**로
   센다(이레 중 나흘 이상이 있는 쪽). 달을 걸치는 주에서 어느 달로 읽을지의 문제다.
5. **`listMeetingsInRange` · 배정 CRUD 둘은 지금 부르는 곳이 없다**(§3). 죽은 코드가 아니라 FE-2 의 입구다.
6. **`ds/Empty.tsx` docstring 의 「소비처 29곳」이 낡았다**(실제 20곳). 건드리지 않았다.
7. **브라우저로 본 적이 없다.** 자동 검증까지가 에이전트 몫이라는 §검증 책임의 경계대로다 —
   3분할의 실제 폭·주 뷰 스크롤·띠 이음새는 사용자 E2E 가 처음 본다.

---

# 부록 — 검수 FAIL **F-1 (K18) 반영** (2026-09-21, 2차)

## 상태: done — **F-1 한 건만 고쳤다. 그 밖은 건드리지 않았다.**

### 무엇을 고쳤나 — 파일 둘

| 파일 | 무엇 |
|---|---|
| `frontend/src/features/calendar/CalendarPage.tsx` | `railScope` 를 `range` 와 **따로** 잡는다 (+22줄) |
| `frontend/src/features/calendar/CalendarPage.test.tsx` | K18 을 박는 검사 **2건** 추가 (+27줄, 삭제 0) |

**다른 16개 파일은 검수 시점과 바이트 단위로 같다.** 새 파일 0건, 삭제 0건.

### 고친 내용

```tsx
/** **레일과 격자는 같은 범위를 본다** — 월 뷰면 그 달, 주 뷰면 그 주 (증보 K18). … */
const railScope = useMemo(() => {
  if (view !== "month") return { from: weekDays[0], to: weekDays[6] };
  const drawn = monthDays.filter((day) => !day.out);
  return { from: drawn[0].date, to: drawn[drawn.length - 1].date };
}, [monthDays, view, weekDays]);

const cards = useMemo(() => railCards(entries, tab, { ...railScope, selected }), [entries, railScope, selected, tab]);
```

- 검수 리포트의 권장안과 **한 곳이 다르다**: 월의 시작을 `` `${anchor.slice(0,8)}01` `` 로 **다시 만들지 않고**
  `monthDays.filter((day) => !day.out)` 의 **처음과 끝**을 쓴다. 그것이 곧 **`MonthGrid` 가 실제로 그리는 날들**이라
  두 값을 따로 계산하지 않으므로 **어긋날 수가 없다**. 앵커가 그 달 1일이 아닐 때도 같은 값이 나온다.
- **조회 구간(`range`)은 좁히지 않았다** — 권장안 그대로다. 달 밖 칸까지 한 번에 받아 두고 **내지 않을 뿐**이라
  **「한 화면 = 한 요청」이 그대로 산다**(재조회 0). 여분 데이터는 격자가 안 그리므로 무해하다.
- 주 뷰는 원래 이레를 다 그려 범위가 이미 같았다 — 그 갈래는 값이 바뀌지 않는다.

### 더한 검사 둘

1. **「레일과 격자가 같은 범위를 본다 — 달 밖 칸의 일정은 둘 다에 없다 (K18)」**
   3월 격자의 달 밖 칸(4/1)에 회의를 하나 두고 → 달 밖 칸이 실제로 서 있고(`--out` > 0),
   그 칸에 조각이 **0건**이며(`--out .scax-event`), 레일에도 **그 제목이 없다**.
   동시에 `getCalendar` 가 여전히 **`2027-02-28`~`2027-04-03`** 로 불린다 — **조회는 안 좁혔다**를 함께 박는다.
2. **「같은 일정이 그 날을 품는 주 뷰에서는 레일에 선다 — 범위는 뷰를 따라간다 (K18)」**
   주 뷰로 바꿔 3/28~4/3 주로 가면 **같은 회의가 레일에 돌아온다.**
   1번이 「그냥 어디서나 안 보인다」가 아니라 **범위 규칙**임을 증명하는 짝이다.

### 검증 (수치) — 전체 1회 + `tsc` 1회

| | 검수 시점 | 지금 |
|---|---|---|
| `make frontend-test` (Node 20.20.0) | 67 파일 / **855** 통과 / 0 실패 | 67 파일 / **857** 통과 / **0 실패** |
| `cd frontend && npx tsc --noEmit` | exit 0 | **exit 0** |

- 늘어난 2건이 위 검사 둘이다. **기존 검사는 한 줄도 고치거나 지우지 않았다.**
- 기존 11건 중 셋(`업무 카드 meta 접기`·`탭 가르기`·`격자 유형 둘`)이 **달 밖 회의가 한 건 늘어난 목데이터 위에서도 그대로 통과**한다 — 레일 카드 수 3, 격자 유형 클래스 둘.

### 완료 판정 — K18 줄

- [x] **레일에 뜬 일정과 격자에 그려진 일정이 같다** (증보 K18) — 월 뷰면 그 달, 주 뷰면 그 주.
      **레일에만 있고 격자에 없는 일정이 0건**이다.

### 범위

- **K17(「업무 만들기」 단추)은 손대지 않았다 — FE-2 다.** 드래그·드롭·손잡이·고스트·쓰기 호출도 여전히 0건이다.
- 백엔드 0건 · `frontend/` 밖 0건 · 커밋·push·PR 0건.
- §8 의 미결 중 **3번(달 밖 칸)은 K18 로 닫혔다.** 나머지(§8-4 「N주차」 셈법 · §8-5 아직 안 부르는 표면 셋 ·
  §8-6 `Empty` docstring 의 낡은 「29곳」 · §8-7 브라우저 미확인)는 그대로 남는다.
