# 리뷰 리포트 — strong-hajin-calendar / Phase FE-1 코드 검수 (2026-09-21)

## 판정: **FAIL** — 한 건 (**K18 미반영**)

**나머지 여섯 항목은 전부 통과했다.** 특히 코디가 짚은 둘이 깨끗하다 —
**띠는 `span_from`·`span_to` 로만 그리고**(`taskSpan()` 호출 0건), **`ds/Empty.tsx` 는 진짜 additive**
(소비처 19곳 **0줄** 수정 + 양쪽을 박는 새 테스트 둘)이며, **AppShell.test.tsx 의 한 줄은
약화가 아니라 정당한 갱신**이다.

**걸리는 것은 K18 하나** — **격자는 달 밖 칸을 비워 두는데 레일은 달 밖 일정을 낸다.**
증보 7 K18 이 「레일과 격자는 **같은 범위**를 본다 … 격자가 달 밖 칸을 비워 두므로
**레일도 달 밖 일정을 내지 않는다**」로 닫은 바로 그 자리다.

**정상 참작이 있다** — K18 은 **이 워커가 물어서 생긴 결정**이고(증보 7 표제가 「FE-1 이 물어온 셋」),
코드는 그 답이 나오기 전에 쓰였다. **규율을 어긴 것이 아니라 아직 안 내려온 결정**이다.
고칠 양도 **레일 범위 한 줄**이다.

---

## 검수 범위

BE-2 커밋 `2a85176` **위의 uncommitted diff** — 수정 9 · 신규 9, **전부 `frontend/`**.
**테스트는 돌리지 않았다**(지시). **코드도 한 줄 고치지 않았다.**
코디가 확인한 것(`frontend/` 밖 0건 · `tsc --noEmit` exit 0 · 855통과)은 다시 세지 않았다.
사실 확인이 필요한 한 자리(`en-GB` 자정 렌더링)만 `node -e` 한 줄로 **읽기 확인**했다 —
프로젝트 테스트가 아니고 파일을 건드리지 않는다.

---

## ① allowed_paths · Phase 경계 — **둘 다 지켰다**

- 18개 전부 `frontend/` 아래다.
- **쓰기가 끼지 않았다.** FE-2 의 쓰기(`createTaskSchedule`·`updateTaskSchedule`)는
  `lib/api.ts` 에 **선언만** 되고 `features/calendar/` 에서 **호출 0건**이다.
  `draggable`·`onDrop`·`onDragStart`·resize 핸들러도 **0건** —
  `ScheduleCard.tsx:11` 이 「`--draggable` 한 종은 **FE-2**」라고 적어 두었다.
  (`api.ts` 에 셋을 미리 넣은 것은 WP FE-1 작업 4 가 요구한 것이다.)
- **CalendarPage 의 `transition`·`update` 는 새 쓰기가 아니다.**
  `git show HEAD:…/CalendarPage.tsx` 를 열어 확인했다 — `:68` `const transition` ·
  `:84` `const update` · `:113` `TaskDetailDrawer` 가 **이미 있었다**.
  FE-1 은 그 둘의 `reload()` 만 새 조회로 갈아 끼웠다. **기존 상세 서랍의 동작을 보존한 것**이다.
- 「업무 만들기」 단추 없음 — 코디가 정한 대로 **FE-2** 다(K17).

---

## ② 띠를 `span_from`·`span_to` 로만 그리는가 — **그렇다 (K14)**

`features/calendar/` 전체에서 `start_date`/`due_date` 가 코드로 닿는 자리는 **정확히 하나**다:

- `calendarModel.ts:294` `if (!row.start_date && row.due_date) return calendarScreen.dueOnly(row.due_date);`
  — **카드의 말**을 「…마감」으로 할지 「기간」으로 할지 고르는 자리다.
  **구간 자체는 그 아래 `:295` 가 `row.span_from`·`row.span_to` 로 낸다.**
  「마감만 있다」와 「하루짜리 기간」은 정규화 구간이 같아 **원본 필드로만 갈린다** — 주석이 그 이유를 적는다.

**기하는 전부 span 이다** — `taskBar`(`:114-118`) · `overlaps`(`:285-289`) · `railCards`(`:303-315`) ·
`packLanes` · `dayReach`. **`taskSpan()` 호출 0건**(주석에서만 언급).

증명도 있다 — `CalendarPage.test.tsx:99` 「뒤집힌 업무의 띠가 서버가 준 구간대로 선다 —
**`start_date`(3/6)부터가 아니다**」 · `calendarModel.test.ts:71` 같은 취지.

---

## ③ `ds/Empty.tsx` 가 정말 additive 인가 — **그렇다. 잘 했다**

- `icon?: IconName` **선택**이고, 안 주면 `fallback` 이 **예전 `variant` 분기 그대로**다
  (`Empty.tsx:60-62`). 기존 호출부의 렌더 결과가 바뀔 수 없다.
- **`variant="error"` 는 `icon` 을 무시한다**(`:62`) — 「못 불러왔다」는 「비었다」가 아니라
  경고 글리프를 지킨다. **더하면서 좁히지도 않았다.**
- **소비처 19곳 중 0곳 수정** — `git status` 의 수정 9개에 `Empty` 소비처가 **하나도 없다**
  (`features/action`·`graph`·`meetings`×5·`org`×5·`today`·`work`×4·`shell`×2 전부 무변경).
  거기에 코디가 확인한 **`tsc --noEmit` exit 0** 이 얹히면 **타입·렌더 양쪽으로 additive 가 증명된다.**
- **테스트가 양쪽을 박는다**(`Empty.test.tsx` **+23 / -0**) —
  「아이콘을 안 주면 variant 가 고르던 글리프 그대로」와
  「아이콘을 주면 그것을 그리되 **error 자리는 경고 글리프를 지킨다**」.
  **기존 테스트는 한 줄도 안 지웠다.**

---

## ④ 한 화면 = 한 요청 — **그렇다**

- `CalendarPage.tsx:88-94` `range` = **그려지는 칸 전부**(월 35·42 / 주 7), deps 는 `[monthDays, view, weekDays]`.
- `:96-99` `reload` deps 는 `[range.from, range.to]`, 조회 effect(`:101-118`) deps 는 `[onError, reload]`.
- **`tab` 이 그 사슬에 없다.** 탭은 `cards`·`segments`·`spans`·`blocks` **네 `useMemo` 의 인자**일 뿐이라
  **화면에서 거른다** — 재조회가 없다.
- 호출도 **하나**다. `getCalendar` 한 번이고 `listMeetingsInRange` 는 부르지 않는다
  (회의 절반이 합본에 실려 오므로 맞다).
- `CalendarPage.test.tsx:83` 이 「한 화면 = 한 요청 — 그려지는 칸 전부를 한 번에 받고,
  **탭을 바꿔도 다시 묻지 않는다**」로 박는다.

---

## ⑤ 회의 UTC → Asia/Seoul — **옳다. 날이 밀리지 않는다**

- 날짜: `seoulDate` → `isoDateInSeoul`(`lib/labels.ts`, **기존 헬퍼 재사용**) →
  `toLocaleDateString("en-CA", {timeZone:"Asia/Seoul"})` = `YYYY-MM-DD` ✓
- 시각: `seoulClock` → `toLocaleTimeString("en-GB", {timeZone:"Asia/Seoul", hour:"2-digit", minute:"2-digit"})`
- **자정 경계를 실측했다**(Node v20.20.0, 이 저장소가 쓰는 버전):

  | UTC | → Seoul |
  |---|---|
  | `2027-03-02T15:00:00+00:00` | **`00:00`** (날짜는 3/3) |
  | `2027-03-02T15:30:00+00:00` | `00:30` |
  | `2027-03-03T14:59:00+00:00` | `23:59` |

  `en-GB` 가 자정을 **`24:00` 이 아니라 `00:00`** 으로 낸다 — `clockMinutes` 가 1440 을 받아
  격자 밖으로 떨어지는 사고가 없다.
- **자정을 넘는 회의**는 `timedBlocks:246-253` 이 `endsSameDay` 로 가려 `DAY_MINUTES` 로 자른다 —
  다음 날 칸으로 흘리지 않는다.
- 워커도 같은 자리를 테스트로 박았다 — `calendarModel.test.ts:191`
  「UTC 자정 근처의 회의가 서울 날짜로 **하루 넘어간다**」.

---

## ⑥ 격자 색 · 레일 부품 이름 — **둘 다 맞다**

- **격자에 상태 색이 없다.** `EventBar.tsx:28-30` 의 클래스는 `scax-event--${segment.kind}` 하나이고
  `kind` 는 `"task" | "meeting"` 둘뿐이다. `styles/calendar.css` 에 상태 이름 클래스가
  **0건**(`open`·`in_progress`·`blocked`·`done`·`cancelled` 전부 없음)이고 색 규칙은 **딱 둘**이다
  (`:74` task · `:75` meeting). `CalendarSegment`(`calendarModel.ts:103-112`)에 상태 필드가 없다.
  `CalendarPage.test.tsx:110`·`calendarModel.test.ts:97` 이 각각 박는다.
- **레일 부품이 다른 이름이다** — `features/calendar/ScheduleRail.tsx`.
  `ds/GutterList.tsx` 는 그대로 남았고, `ScheduleRail.tsx:16-17` 이
  「저장소 DS 에 같은 이름의 **다른 부품**이 있고 그 개명은 이번 범위 밖(§J)」이라고 적는다.
- **카드도 상태를 안 낸다**(K15) — `RailCard`(`:273-281`)에 상태 필드가 없고 유형 배지 하나다.
  코디가 정한 대로 **K15 를 따른 것이 옳다** — 지적하지 않았다.

---

## ⑦ 조용히 통과하는 자리 — **없다.** `AppShell.test.tsx` 한 줄은 **정당한 갱신이다**

### `AppShell.test.tsx` 판정 — **약화가 아니다**

바뀐 것은 한 줄이다: `const fixed = label === "회의"` → `label === "회의" || label === "캘린더"`.

**이 테스트는 「가드」가 아니라 화면별 기대값 표**다. 각 화면을 돌며
`expect(scroll.classList.contains("--fixed")).toBe(fixed)` 로 **양방향** 단언한다. 따라서:

- **단언을 지우거나 느슨하게 하지 않았다** — `toBeTruthy`·`skip`·조건 우회가 없다.
- **다른 화면은 전부 그대로 `false` 에 묶여 있다** — 캘린더 말고 어느 화면이 `--fixed` 가 되면 여전히 깨진다.
- 캘린더 쪽은 **오히려 조여졌다** — 전에는 「캘린더가 fixed 면 실패」였고 지금은
  **「캘린더가 fixed 가 아니면 실패」**다.

**그리고 그 값이 바뀐 이유가 실재한다** — 소스가 먼저 바뀌었다:
`App.tsx:460` 이 `surface === "meetings" || surface === "calendar"` 로 `--fixed` 를 준다.
근거도 코드에 있다 — `styles/calendar.css:32`
`.scax-cal-main{display:flex;flex-direction:column;flex:1 1 auto;min-height:0;…}` 는
**자기 안에서 스크롤하겠다는 선언**이라 바깥 문서 스크롤과 주인이 겹친다.
**회의 화면이 같은 충돌을 이미 `--fixed` 로 풀었다.**

→ **동작이 바뀌었으니 기대값 표의 그 칸이 바뀐 것**이고, 이것이 그런 표를 갱신하는 올바른 방법이다.
표를 지우거나 캘린더만 예외로 빼는 쪽이 약화였을 것이다.

### 그 밖

- **수정된 테스트 파일은 둘뿐이고 삭제는 1줄**이다 — `Empty.test.tsx` **+23/-0**,
  `AppShell.test.tsx` **+5/-1**(위 한 줄). **다른 기존 테스트는 손대지 않았다.**
- 새 코드·새 테스트에 `expect(true)` · `skip(` · `todo(` · `as any` · `@ts-ignore` ·
  빈 `catch {}` 가 **0건**이다.
- 새 테스트가 실질적이다 — `CalendarPage.test.tsx` 11건이 한 요청·3분할·뒤집힌 띠·유형 둘·
  주최자 이름·K15 카드·meta 접기·탭·8시 열림·공유 회의 제자리·날짜 선택을 각각 박고,
  `calendarModel.test.ts` 19건이 모델을 값 단위로 판다.

---

## FAIL — F-1. 격자는 달 밖 칸을 비우는데 **레일은 달 밖 일정을 낸다** (K18 미반영)

### 무엇이 다른가

**격자는 달 밖 칸을 비운다** — `MonthGrid.tsx:88-96`:

```tsx
if (day.out) {
  return (
    <div className="scax-month__cell scax-month__cell--out" key={day.date}>
      <div className="scax-month__daytop"><span className="scax-month__date">{number}</span></div>
    </div>
  );
}
```

`inside`(= `EventBar` 들을 담은 조각)를 **버리고 날짜 숫자만** 그린다. 시안 규칙대로다.

**그런데 레일은 그 칸의 일정을 낸다** — `CalendarPage.tsx:88-94` 가 `range` 를
**그려지는 칸 전부**(`monthDays[0].date` ~ `monthDays[last].date`)로 잡고,
`:126-129` 가 그 `range` 를 **그대로** 레일 범위로 넘긴다:

```tsx
const cards = useMemo(
  () => railCards(entries, tab, { from: range.from, to: range.to, selected }),
  [entries, range.from, range.to, selected, tab],
);
```

`railCards` 의 `overlaps`(`calendarModel.ts:285-289`)에 달 안/밖 구분이 없다.

**결과** — 2027년 3월을 볼 때 격자는 2/25~2/28 과 4/1~4/5 칸을 **비워 두는데**,
2/26 회의는 **좌측 레일에 선다.** 사람은 「레일에 있는데 격자에 없다 = 하나가 틀렸다」로 읽는다.

### 무엇을 어긴 것인가

DEC-003 **증보 7 K18**:

> 「**레일과 격자는 같은 범위를 본다.** 월 뷰면 **그 달**, 주 뷰면 **그 주**.
> 격자가 달 밖 칸을 비워 두므로 **레일도 달 밖 일정을 내지 않는다**」
> **K18 의 이유.** 「레일과 격자가 **같은 것을 다르게 보여주면** 사람이 「하나가 틀렸다」고 읽는다.」

**지금 코드가 정확히 그 상태다.** 주 뷰는 문제가 없다 — 이레를 다 그리므로 범위가 이미 같다.
**월 뷰에서만** 갈린다.

### 정상 참작

**K18 은 이 워커가 물어서 생긴 결정이다** — 증보 7 의 표제가 「**FE-1 이 물어온 셋**」이고,
K18 행의 물음이 「달 밖 칸에 일정을 안 그리는 시안 규칙과 좌측 레일의 범위가 어긋난다」다.
**워커가 이 어긋남을 스스로 발견해 올렸고**, 코디가 답을 내린 것은 그 뒤다.
**숨기거나 조용히 정하지 않았다** — 규율은 지켜졌다. 남은 것은 **반영**뿐이다.

### 권장 수정 — 레일 범위 한 줄

조회 범위(`range`)는 **그대로 두어도 된다** — 격자가 달 밖 칸을 안 그리므로 여분 데이터는 무해하고,
범위를 좁히면 재조회가 생긴다. **레일 범위만 따로 잡으면 된다.**

```tsx
/* K18 — 레일과 격자는 같은 범위를 본다. 월 뷰면 그 달, 주 뷰면 그 주.
   격자가 달 밖 칸을 비우므로(MonthGrid) 레일도 그 일정을 내지 않는다. */
const railScope = useMemo(
  () =>
    view === "month"
      ? { from: `${anchor.slice(0, 8)}01`, to: monthDays.filter((day) => !day.out).at(-1)!.date }
      : { from: weekDays[0], to: weekDays[6] },
  [anchor, monthDays, view, weekDays],
);
```
그리고 `cards` 의 `railCards(entries, tab, { ...railScope, selected })` 로 바꾼다.

**인수조건 한 줄을 같이 단다** — 「[ ] 월 뷰에서 **달 밖 칸의 일정이 레일에도 서지 않는다** —
격자가 비운 것을 레일이 내지 않는다(K18)」.
**기존 테스트를 고칠 필요는 없다** — 레일의 월 범위를 고정하는 테스트가 아직 없어
`calendarModel.test.ts` 에 **새로 한 건** 더하면 된다.

---

## 확인한 것 (근거)

- **①** `git status` 18건이 전부 `frontend/` 임을 확인하고, FE-2 쓰기 호출 0건 ·
  드래그 핸들러 0건을 `grep` 으로 셌다. `transition`·`update` 는
  **`git show HEAD:` 로 원본을 열어** 기존 코드임을 확인했다.
- **②** `features/calendar/` 에서 `start_date`/`due_date`/`taskSpan` 을 전수 `grep` 하여
  코드로 닿는 자리가 `calendarModel.ts:294` 하나(말 고르기)뿐임을 확인했다.
- **③** `Empty.tsx` 의 `fallback`/`glyph` 분기를 읽고, 수정 파일 목록에 소비처가 0건임을
  대조했으며, 새 테스트 둘이 양쪽을 박는 것을 확인했다.
- **④** `range`→`reload`→effect 의 의존 사슬에 `tab` 이 없음을 확인하고, 호출이 `getCalendar`
  하나뿐임을 확인했다.
- **⑤** `isoDateInSeoul`(기존 `en-CA`)를 읽고, `en-GB` 자정 렌더링을 **Node 20 에서 실측**했다
  (`00:00`). 자정 넘김 클램프(`:246-253`)도 확인했다.
- **⑥** `EventBar` 의 클래스 조립과 `calendar.css` 의 색 규칙 둘, 상태 클래스 0건,
  `ScheduleRail` 이름을 확인했다.
- **⑦** `AppShell.test.tsx` 의 단언 구조를 읽고 **양방향·전 화면 유지**를 확인했으며,
  소스(`App.tsx:460`)와 CSS(`calendar.css:32`) 근거를 대조했다.
  테스트 diff 전체가 **+27/-1** 임을 확인했다.
- **F-1** 은 `MonthGrid.tsx:88-96` 과 `CalendarPage.tsx:88-94`·`:126-129` 를 나란히 읽어 확인했고,
  증보 7 K18 원문과 대조했다.
- **테스트를 돌리지 않았다. 코드를 한 줄도 고치지 않았다.** 산출물은 이 리포트 하나.

---

## `git -C /Users/kknaks/orca/workspaces/Strong_hajin/strong-hajin-calendar status --short`

```text
 M frontend/src/App.tsx
 M frontend/src/ds/Empty.test.tsx
 M frontend/src/ds/Empty.tsx
 M frontend/src/features/calendar/CalendarPage.tsx
 M frontend/src/lib/api.ts
 M frontend/src/lib/labels.ts
 M frontend/src/lib/viewModels.ts
 M frontend/src/shell/AppShell.test.tsx
 M frontend/src/styles/index.css
?? frontend/src/features/calendar/CalendarPage.test.tsx
?? frontend/src/features/calendar/EventBar.tsx
?? frontend/src/features/calendar/MonthGrid.tsx
?? frontend/src/features/calendar/ScheduleCard.tsx
?? frontend/src/features/calendar/ScheduleRail.tsx
?? frontend/src/features/calendar/WeekGrid.tsx
?? frontend/src/features/calendar/calendarModel.test.ts
?? frontend/src/features/calendar/calendarModel.ts
?? frontend/src/styles/calendar.css
```

(검수 시작 시점과 **같다** — 읽기만 했다.)
