# 리뷰 리포트 — strong-hajin-calendar / Phase FE-3 코드 검수 (2026-09-21)

## 판정: **PASS**

**여덟 항목이 전부 통과했다.** FAIL 도 WARN 도 없다.

셋 다 **사용자가 실물에서 찾은 것**이라 「고쳤다」가 아니라 **「그 자리가 실제로 닫혔나」**로 봤다.
셋 다 닫혔고, **과잉으로 번진 자리가 없다**:

- **K20** — 월 뷰에서 업무의 시간 배정이 사라졌고 **회의는 남았다.** 「배정을 안 그린다」가
  **회의까지 지우는 쪽으로 번지지 않았다.** 주 뷰는 종일 칸·시간 격자 둘 다 그대로다.
- **K21** — `packBlocks` 가 **거르는 것이 0건**이다(입력 수 = 출력 수). 나란히 앉히기가
  **막는 쪽으로 번지지 않았다.** 종일 띠의 `packLanes` 도 안 깨졌다 — 그쪽 조각은 전부
  `time === null` 이라 새 정렬 두 단계가 **아무것도 바꾸지 않는다.**
- **K19** — **새로 만든 말이 0개다.** `taskStateLabel`·`taskStateTone`·`derivedApprovalLabel` 을
  그대로 쓰고, **톤까지 `WorkTables.tsx` 와 같다.** `approved`·`null` 에 배지를 안 내는 것도 그쪽과 같다.

**1루프 규율도 회귀하지 않았다** — `start_date`/`due_date` 가 새로 닿은 자리 0건,
탭 전환 재조회 0건, K18 레일 범위 그대로, `api.ts` 밖 `fetch` 0건.

**공회전하는 테스트가 없다.** +15 건 표본을 전부 읽었고, 「나란히 그린다」를 단언하는 두 건 모두
**픽스처에 실제로 겹치는 블록이 있다**(09:30–12:30 배정 **안**에 10:00–11:00 회의).

---

## 검수 범위

BE-4 커밋 `434003c` **위의 uncommitted diff** — **수정 12 · 신규 0**, 전부 `frontend/`,
419 insertions / 103 deletions.
**테스트는 돌리지 않았다**(지시). **코드도 한 줄 고치지 않았다.**
코디가 확인한 것(`frontend/` 밖 0건 · **929 passed / 0 failed**(기준선 914 → **+15**) ·
`npx tsc --noEmit` exit 0)은 다시 세지 않았다.

실행한 검사: `git diff` 전문 정독 · `grep` 전수(아래 각 항목에 방법을 적었다) ·
SSOT 대조(SPEC-004 §2.1·§2.6·§4·완료판정 · DEC-003 증보 8 K19~K21 · WORK `Phase FE-3`) ·
BE-4 산출물 **읽기 확인**(`modules/work/application.py:756-800`).

### 변경 파일 12

```text
 M frontend/src/features/calendar/CalendarInteractions.test.tsx   (+2)
 M frontend/src/features/calendar/CalendarPage.test.tsx           (+97/-13)
 M frontend/src/features/calendar/CalendarPage.tsx                (+3/-2)
 M frontend/src/features/calendar/MonthGrid.tsx                   (+5)
 M frontend/src/features/calendar/ScheduleCard.tsx                (+16/-4)
 M frontend/src/features/calendar/WeekGrid.tsx                    (+62/-46)
 M frontend/src/features/calendar/calendarModel.test.ts           (+109/-15)
 M frontend/src/features/calendar/calendarModel.ts                (+107/-20)
 M frontend/src/features/calendar/calendarWrites.test.ts          (+1)
 M frontend/src/lib/labels.ts                                     (+15/-5)
 M frontend/src/lib/viewModels.ts                                 (+8/-3)
 M frontend/src/styles/calendar.css                               (+3/-1)
```

**allowed_paths** — 12개 전부 `frontend/` 아래다. `backend/`·`docs/`·`para/`·`orchestration/` **0건**.
`features/calendar/` 밖의 셋(`lib/labels.ts`·`lib/viewModels.ts`·`styles/calendar.css`)은
**계약이 요구한 자리**다 — `approval` 타입(§4) · 상태·승인 어휘 재사용(§2.6) · 시간 블록 폭(K21).

---

## ① K20 이 실제로 닫혔나 — **닫혔다. 회의도 지우지 않았다**

### 월 뷰에 업무의 시간 배정이 **안 그려진다**

`taskSlots()` 가 **함수째 삭제됐고**(`calendarModel.ts` −12줄), 호출부도 같이 빠졌다.
`grep -rn "taskSlots" src/` → **0건**. 남은 것은 `monthSegments`(`:148-160`) 하나이고
업무 쪽 분기가 `taskBar(entry)` **하나뿐**이다.

```ts
if (entry.kind === "task") {
  if (tab === "meeting") continue;
  const bar = taskBar(entry);
  if (bar) segments.push(bar);      // ← 배정을 더하던 줄이 사라졌다
} else if (tab !== "task") {
  segments.push(meetingChip(entry));
}
```

### **회의는 그려진다** — 과잉으로 번지지 않았다

`else if (tab !== "task")` 가지가 **그대로다.** 「배정을 안 그린다」가 회의까지 지우는 쪽으로
번졌는지가 이 항목의 핵심인데 **안 번졌다.**
검사도 둘이 박는다 — `calendarModel.test.ts:91`
「회의는 월 뷰에도 그려진다 — 회의는 그 자체가 일정이다」가 **`["task:t1", "meeting:m1"]` 순서까지**
단언하고, `CalendarPage.test.tsx:196-198` 이 **실제 DOM** 에서
`[data-date="2027-03-04"] .scax-event--meeting` **1개**를 센다.

### 셀 안이 **시간순**인가 — 그렇다

셀 안의 순서 = 줄 순서(`MonthGrid.tsx:64` `packLanes` → `:84` `laneSeats`)이고,
`packLanes` 의 정렬에 **두 단계가 새로 들어갔다**(`calendarModel.ts:188-190`):
`time === null` 이 먼저, 시간끼리는 이른 것부터.

**1차 키가 `from` 인 것은 바꿀 수 없다** — 「같은 항목은 그 주 내내 같은 줄」(SPEC §2.1 레이아웃 ·
`calendar.v1.jsx:72-86`)이 요구한다. 여러 날 띠가 칸마다 줄을 옮기면 띠가 끊긴다.
**워커가 그 제약을 docstring 에 그대로 적었다**(`:173-181`) — 조용히 넘기지 않았다.
따라서 한 칸의 순서는 **「먼저 시작한 것 → 그 날 시작하는 종일 띠 → 시간순」** 이고,
이것이 K20 의 「종일 띠가 먼저, 시간이 붙은 것은 이른 것부터」다.
검사가 `laneSeats` 로 **칸 단위 순서**를 박는다 — `calendarModel.test.ts:148`
`["task:bar", "meeting:early", "meeting:late"]`.

### 주 뷰는 **안 건드렸다**

- 종일 칸은 `spanSegments`(**무변경**) → `packLanes(spans, days)`(`WeekGrid.tsx:95`)다.
  `spanSegments` 가 내는 것은 `taskBar` 뿐이라 **전부 `time === null`** — 새 정렬 두 단계가
  **구조적으로 아무것도 바꿀 수 없다.** 회귀 테스트가 그것을 박는다(`calendarModel.test.ts:158`
  「시간이 없는 것끼리는 예전 규칙이다」 → `["long", "short"]`).
- 시간 격자는 `timedBlocks`(**무변경**)가 그대로 배정과 회의를 낸다.
- `CalendarPage.test.tsx:201` 이 **주 뷰에서 띠와 배정이 둘 다 뜨는 것**을 단언한다 —
  종일 칸의 `.scax-event__label` > 0 **그리고** `.scax-week__hours[data-date=…] .scax-week__slot` 에
  그 업무 제목.

---

## ② K21 이 **그리기만** 고쳤나 — **그렇다. 거르는 것이 0건이다**

### 막는 쪽으로 번지지 않았다

`packBlocks`(`calendarModel.ts:307-337`)에 **`filter`·`continue`·조기 반환이 없다.**
모든 입력이 `cluster.push` → `packed.push(...cluster)` 를 지난다 — **출력 수 = 입력 수**다.
검사가 그것을 정면으로 박는다 — `calendarModel.test.ts:232`
「이미 겹쳐 있는 것을 거르지 않는다 — 그리기이지 막는 것이 아니다」:
**똑같은 10:00–11:00 세 개**를 넣고 `toHaveLength(3)` · 줄 `[0,1,2]`.

`WeekGrid` 쪽도 마찬가지다 — 기존 `blocks.filter((block) => block.date === date)` 를
`packBlocks(...)` 로 **감쌌을 뿐** 조건이 늘지 않았다(`:251`).

**겹침 금지(§2.9·K22)와 섞이지 않았다** — `grep -rn "OVERLAP|겹칩니다|이미 다른 일정" src/` → **0건**.
FE-4 의 몫이 들어와 있지 않다.

### 종일 띠의 `packLanes` 를 안 깼다

`packLanes` 는 **새 함수가 아니라 정렬 두 줄만 늘었다.** 줄 배정 알고리즘(`findIndex` → `lanes`)은
**한 글자도 안 바뀌었다.** 위 ①에서 적은 대로 종일 칸 입력은 전부 `time === null` 이라 무영향이고,
`packBlocks` 는 **별개 함수**다 — `packLanes` 를 고쳐 쓰지 않았다.

### 그리기 자체도 회귀가 없다

`styles/calendar.css:125` 에서 `.scax-week__slot` 의 `left:3px;right:3px` 가 빠지고
`WeekGrid` 가 인라인으로 준다. **혼자 선 블록은 예전 값과 같다** —
`lanes === 1` → `left:calc(0% + 3px)` · `width:calc(100% - 6px)`.
회귀 테스트가 그 **문자열 그대로**를 단언한다(`CalendarPage.test.tsx:231-233`).
**`.scax-week__ghost` 는 자기 `left:3px;right:3px` 를 그대로 갖는다**(`:133`) — 미리보기는 안 흔들린다.
높이 상수도 `px(30)` → `px(MIN_BLOCK_MINUTES)` 로 **같은 값**을 가리키게 바뀌었을 뿐이다.

**줄은 「저장된」 시각으로 잡는다** — `packBlocks` 에 들어가는 것은 `block.startMin`/`endMin` 이고,
끄는 중인 `held` 값은 **그 뒤 `top`/`height` 에만** 쓰인다(`WeekGrid.tsx:252-254`).
세로 손잡이를 끄는 동안 블록이 좌우로 튀지 않는다.

---

## ③ K19 가 기존 어휘를 재사용하나 — **그렇다. 새로 만든 것이 0개다**

`ScheduleCard.tsx:66-68` 세 줄이 전부다:

```tsx
{card.state ? <Badge tone={taskStateTone[card.state]}>{taskStateLabel[card.state]}</Badge> : null}
{card.approval === "awaiting_review" ? <Badge tone="accent">{derivedApprovalLabel.awaiting_review}</Badge> : null}
{card.approval === "awaiting_revision" ? <Badge tone="danger">{derivedApprovalLabel.awaiting_revision}</Badge> : null}
```

**업무 화면(`WorkTables.tsx:197-198` `WaitingBadge`)과 글자 단위로 같다** — 조건도 톤도 같고,
`approved`·`null` 에 배지를 안 내는 것도 같다(「기다리는 것이 없으면 말하지 않는다」).
**새 라벨 0개** — `grep` 으로 확인했다: `calendarScreen` 에 상태·승인 문자열이 **하나도 없다**.
`labels.ts:929-930` 주석이 「상태·승인의 말은 여기 없다」고 자리를 못 박는다.

### `taskStateTone` 을 고친 것 — **정당하고, 오히려 있던 버그를 닫았다**

`labels.ts:20-27` 에서 `done: "success"` → **`"positive"`**, `cancelled: "muted"` → **`"neutral"`**.

- **고치지 않으면 `tsc` 가 깨진다** — `BadgeTone` 은 `accent|neutral|danger|positive|info|outline`
  이고(`ds/Badge.tsx:25`), `components.css` 에 `.scax-badge--success` 도 `--muted` 도 **없다**.
  그 표는 **쓸 수 없는 값 둘을 들고 있던 죽은 표**였다.
- **소비처가 0곳이었다** — `git grep -n "taskStateTone" HEAD -- src/` → **`labels.ts` 선언 한 줄뿐**.
  기존 화면의 렌더가 바뀔 수 없다.
- **임의로 고른 값이 아니다** — 저장소가 상태를 실제로 배지로 내는 유일한 자리
  `WorkTables.tsx:205-213` `ClosedBadge` 가 `done` → `positive`, `cancelled` → `neutral` 이다.
  **거기에 맞췄다.**
- `as const satisfies Record<TaskState, string>` 이라 `Badge` 의 `tone` 에 형변환 없이 들어간다.
  **`as any`·`@ts-ignore` 가 아니다.**

### 격자와 카드가 같은 상태를 다르게 말하나 — **아니다**

캘린더 카드에 `state: "done"` 이 서는 경우는 **구조적으로 `COMPLETION_SUBMITTED` 뿐**이다 —
`calendar_tasks` 가 `my_work(include_closed=False)` 를 쓰므로 진짜 `DONE`·`CANCELLED` 는
행 자체가 안 온다(`application.py:770-772` docstring). 그래서 「완료」 배지 옆에는 **항상**
「확인 대기」가 선다. **상태 배지 하나만으로 「완료」라고 말하는 자리가 0개**다 —
WORK 완료판정 「`COMPLETION_SUBMITTED` 인 업무가 「완료」로만 읽히는 자리가 0개」 그대로다.

검사가 DOM 에서 **배지 배열 전체**를 박는다(`CalendarPage.test.tsx:167-175`):
`["업무","완료","확인 대기"]` · 다른 업무는 `["업무","진행 중"]` · 회의는 `["회의"]`.

---

## ④ `approval` 네 값을 다 다루나 — **그렇다. `undefined` 가 새는 자리가 없다**

| 값 | 카드가 내는 것 | 근거 |
|---|---|---|
| `null` | 승인 배지 **없음** | `=== "awaiting_review"` / `=== "awaiting_revision"` 둘 다 거짓 |
| `awaiting_review` | 「확인 대기」 accent | `ScheduleCard.tsx:67` |
| `awaiting_revision` | 「보완 요청」 danger | `:68` |
| `approved` | 승인 배지 **없음** | 업무 화면 `WaitingBadge` 와 같다 — SPEC §2.6 「업무 화면과 같은 방식」 |

- **조회(lookup)가 아니라 동치 비교 둘**이다 — `derivedApprovalLabel[card.approval]` 처럼
  **키로 읽는 자리가 없어서** 빠진 값에서 `undefined` 가 렌더될 길이 구조적으로 없다.
- **상태 쪽도 안전하다** — `taskStateLabel`/`taskStateTone` 은 `Record<TaskState, …>` 로 **5종 전수**다.
- **타입이 필수 필드다** — `viewModels.ts:1285` `approval: DerivedApproval | null`(옵셔널 아님).
  **서버가 언제나 싣는다** — `application.py:791` 이 무조건 키를 넣는다. `tsc` exit 0 이
  픽스처 넷이 전부 갱신됐음을 보증하고, diff 에도 넷이 다 보인다
  (`calendarModel.test.ts:28` · `calendarWrites.test.ts:28` · `CalendarInteractions.test.tsx:76`·`:90` ·
  `CalendarPage.test.tsx:62`·`:73`).
- **`derivedApprovalLabel.approved`(「확인 완료」)는 캘린더에서 쓰이지 않는다.** 업무 화면과 같다.

---

## ⑤ 격자는 여전히 상태를 안 말하나 — **그렇다. 배지는 좌측 카드뿐이다**

- **`ScheduleCard` 의 소비처가 하나다** — `grep -rn "ScheduleCard" src/` → `ScheduleRail.tsx:72` 뿐.
  **좌측 레일 밖으로 나갈 수 없다.**
- **격자 조각에 상태·승인 필드가 없다** — `CalendarSegment`(`calendarModel.ts:103-112`)·
  `TimedBlock`(`:217-231`) 둘 다 무변경이고, 새 테스트가 `approval` **키의 부재**까지 더해 박는다
  (`calendarModel.test.ts:107-108`).
- **가장 센 기존 단언이 그대로다** — `CalendarPage.test.tsx:145-149`:
  유형 클래스 집합이 정확히 `["scax-event--meeting","scax-event--task"]` **그리고**
  상태 다섯(`open`·`in_progress`·`blocked`·`done`·`cancelled`) 클래스 `toBeNull()` 루프.
  **한 글자도 안 바뀌었다.**
- 새 검사가 한 겹 더 얹혔다 — `:180-186` 「격자는 여전히 상태를 말하지 않는다」:
  `awaiting_review` 인 업무를 실은 채 `.scax-month__grid .scax-badge` **0개**,
  격자 텍스트에 **「확인 대기」 없음**. **픽스처에 그 값이 실제로 있으므로 공회전이 아니다.**
- `styles/calendar.css` 에 상태 이름 클래스 **0건**(이번 diff 는 `.scax-week__slot` 한 줄만 건드렸다).

---

## ⑥ 1루프 규율 — **넷 다 회귀 없음**

### `span_from`·`span_to` 로만 그린다 (K14)

`features/calendar/` 에서 `start_date`/`due_date` 가 **코드로** 닿는 자리를 전수했다:

| 자리 | 무엇 | 판정 |
|---|---|---|
| `calendarModel.ts:377` | 카드의 **말** 고르기(「…마감」 vs 「기간」) | FE-1 검수가 통과시킨 그 자리. **무변경** |
| `calendarWrites.ts:47-54`·`:73-77` | 좌우 **손잡이** — 필드를 쓰는 명령이라 원본이 맞다 | FE-2 검수 WARN-A 대로. **무변경** |

**이번 diff 가 새로 만든 자리는 0건**이다. **그리는 기하는 전부 span** 이다 —
`taskBar`(`:114-118`) · `monthSegments` · `spanSegments` · `packLanes` · `railCards`.
`taskSpan()` 호출은 여전히 0건.

### 한 화면 = 한 요청

`CalendarPage.tsx` 의 diff 는 **3줄**(import 한 줄 · `useMemo` 한 줄 · 주석 한 줄)이고
**조회 사슬을 건드리지 않았다**: `range`(`:140-146`) → `reload`(`:148-151`, deps `[range.from, range.to]`)
→ effect(`:153-170`, deps `[onError, reload]`). **`tab` 이 그 사슬에 없다.**
`segments` 의 deps 도 `[entries, tab]` 그대로다 — 이름만 `gridSegments` → `monthSegments` 로 바뀌었다.
테스트 `:105` 「탭을 바꿔도 다시 묻지 않는다」가 **무변경**으로 남아 있다.

### 레일과 격자가 같은 범위 (K18)

`railScope`(`:190-195`)가 **무변경**이다 — 월 뷰면 `monthDays.filter(!day.out)` 의 양 끝.
FE-1 검수의 FAIL 이 닫힌 그 코드 그대로다. 조회 구간(`range`)은 여전히 안 좁힌다(재조회 방지).

### `api.ts` 밖 `fetch`

`grep -rn "fetch(" src/ | grep -v lib/api.ts` → 걸린 것은 `MeetingLive.test.tsx` 의
`didNotRefetch()` **헬퍼 이름 5건**뿐. 실제 호출 **0건**.

---

## ⑦ FE-4 를 당겨 하지 않았나 — **안 했다**

| FE-4 항목 | 확인 | 결과 |
|---|---|---|
| 겹침 **거절 문구**(K22) | `grep "OVERLAP\|겹칩니다\|이미 다른 일정" src/` | **0건** |
| **업무 탭 레일에 회의**(K23·K24) | diff 12개에 `features/work/` **0개** | **없음** |
| 「업무 만들기」 단추 | `CalendarPage.tsx:78`·`:450`·`labels.ts:949` | **FE-2 가 K17 로 이미 세운 것.** 이번 diff 에 **없다** |

> 지시서 §7 이 「업무 만들기 단추는 다음 Phase」라고 적었지만, 그 단추는 **FE-2 의 K17** 로
> 이미 서 있고 `CalendarInteractions.test.tsx:382` 가 1루프에 박아 둔 것이다.
> **FE-3 이 당겨 한 것이 아니다** — 지시서 쪽 표현이 앞 Phase 와 어긋난 것으로 읽힌다.
> **FE-4 브리프에서 이 줄은 빼는 게 맞다.**

쓰기도 안 늘었다 — `createTaskSchedule`·`updateTaskSchedule`·`updateTask` 호출 자리가
FE-2 와 **같은 수**이고 diff 가 그 근처를 건드리지 않았다. WORK 「쓰기는 안 는다」 그대로다.

---

## ⑧ 조용히 통과하는 자리 — **없다. +15 건이 전부 실질이다**

### 늘어난 15건의 출처가 맞는다

| 파일 | 내역 | 계 |
|---|---|---|
| `calendarModel.test.ts` | `monthSegments` +2 · `packLanes` +2 · `packBlocks` +5 · `railCards` −1 +2 | **+10** |
| `CalendarPage.test.tsx` | −1 +6 | **+5** |

**합 +15** — 코디가 잰 914 → 929 와 **정확히 맞는다.** 숨은 skip 이 없다.

### 공회전하는 것이 있나 — **없다. 「겹침」 둘을 실제로 팠다**

- **`CalendarPage.test.tsx:211-229`(K21)** — 픽스처가 **진짜 겹친다**:
  `wide` 의 배정 **09:30–12:30**(2027-03-04)과 `thisWeek` 회의
  `2027-03-04T01:00Z–02:00Z` = **서울 10:00–11:00**. 「안에 든」 모양 그대로다.
  단언도 세다 — 폭이 `calc(50% - 6px)` **둘**, `left` 가 **서로 다른 값 2종**.
- **`calendarModel.test.ts:227`(최소 높이)** — `600–610` 과 `620–650` 은 **시간으로는 안 겹친다.**
  `drawnEnd(a) = max(610, 630) = 630 > 620` 이라 겹친다고 판정된다. **값을 실제로 가르는 검사다.**
- **`:220`(사슬)** — `600–700`·`660–760`·`720–820` 을 넣고 `lanes` 셋 다 **2**,
  `c.lane === 0`(첫 줄 재사용). 손으로 따라가 값이 맞는 것을 확인했다.
- **`:214`(반열림)** — `600–660` 과 `660–720` 이 **겹치지 않아** 둘 다 lane 0 · lanes 1.
  §2.9 의 반열림 정의와 같은 규칙을 박는다.
- **`:148`(시간순)** — `laneSeats` 로 **칸 단위 순서**를 읽는다. 줄 배열만 보고 넘기지 않았다.
- **`:180`(격자 배지 0)** — 픽스처 `submitted` 가 `awaiting_review` **를 실제로 들고 있다.**
  값이 없는데 부재를 단언하는 공회전이 아니다.

`expect(true)` · `skip(` · `todo(` · `as any` · `@ts-ignore` · 빈 `catch {}` — **새 코드·새 테스트에 0건.**

### 기존 테스트 약화 — **없다. 손댄 넷이 전부 정당하다**

1. **`calendarModel.test.ts` 「카드는 상태를 싣지 않는다 (K15)」 삭제** →
   K19 두 건으로 교체. **계약이 뒤집힌 자리**다(SPEC §2.6 ③ · DEC-003 증보 8).
   **주석이 「앞 판은 여기서 `state` 가 «없음»을 지켰다」로 이력을 남긴다** — 조용히 지우지 않았다.
2. **`CalendarPage.test.tsx` 「업무 카드는 상태를 내지 않고…」 교체** → 같은 이유.
   **새것이 더 세다** — 예전은 「라벨 5종이 없다」였고 지금은 **배지 배열 전체가 정확히 무엇인지**를
   업무 카드 둘 · 회의 카드 하나에 대해 각각 박는다.
3. **`monthSegments` 「탭이 격자를 가른다」의 수가 2→1 · 3→2** — K20 이 낸 수다. 제목에서
   「배정」을 뺀 것도 사실과 맞춘 것이다. **`every(kind === …)` 단언은 그대로.**
4. **「격자 조각은 상태를 싣지 않는다」** — `approval` 키 부재 단언이 **추가**됐다. 조여졌다.

**그 밖의 기존 테스트는 픽스처에 `approval: null` 한 줄만 늘었다**(필수 필드).
`CalendarInteractions.test.tsx` 는 **+2 줄이 전부**이고 단언은 한 글자도 안 바뀌었다 —
FE-2 가 박은 K10·K12·R6·회의 손잡이 없음이 **그대로 돈다.**

---

## 위반 (FAIL 사유)

**없음.**

## 경미 (WARN)

**없음.** — FE-4 브리프에 실을 것도 없다.

## 기존 부채 (이번 판정 제외)

- **지시서 §7 의 「업무 만들기 단추는 다음 Phase」** — 그 단추는 **FE-2 가 K17 로 이미 세웠다**
  (`CalendarPage.tsx:450` · `CalendarInteractions.test.tsx:382`). FE-3 의 위반이 아니다.
  **FE-4 브리프를 쓸 때 이 줄을 빼라** — 안 그러면 다음 워커가 「있는 것을 또 만든다」.

## 관찰 (지적 아님 — 2루프 사용자 E2E 에서 눈으로 볼 자리)

계약에 어긋나는 것이 아니라 **브라우저에서 보고 판단할 것**이다.

1. **`packBlocks` 가 렌더마다 7열 각각에서 돈다**(`WeekGrid.tsx:251`, memo 없음).
   세로 손잡이를 끄는 동안 `pointermove` → 재렌더마다 7회다. 하루 블록 수가 작아 실측상 무해하고,
   **앞 판도 `blocks.filter(...)` 를 인라인으로 두었다** — 규칙 위반이 아니다.
2. **최소 높이(30분)로 겹침을 판정하므로**, 시간상 안 겹치는 짧은 블록들도 폭을 나눠 쓴다.
   **워커가 의도했고 docstring 에 이유를 적었다**(「나란히 앉히는 것은 그리기의 문제이므로
   그려지는 크기로 판정한다」). 짧은 배정이 많은 날에 얼마나 좁아 보이는지는 **써 보고 본다.**
3. **한 덩어리가 폭을 함께 나눈다** — 09:00–18:00 배정 하나가 있는 날은 그 날 블록 전부가
   최소 절반 폭이 된다. 일반적인 캘린더 동작이고 K21 이 요구한 「폭이 들쭉날쭉하지 않다」의 결과다.
4. **월 뷰에서 「그 업무가 몇 시로 잡혔는지」는 이제 좌측 카드의 meta 줄에서만 읽힌다.**
   SPEC §2.1 이 그렇게 정했다(「업무의 시간 배정 · 월 뷰 · **그리지 않는다**」). 의도대로다.

---

## 확인한 것 (체크리스트 — 건너뛴 항목 없음)

- **envelope** — 이번 diff 에 `kind`·`status` 로 command·권한을 추론하는 코드 **0건**.
  `approval` 은 **표시**에만 쓰이고 쓰기 가능 여부를 정하지 않는다(`ScheduleCard` 의 `draggable` 은
  여전히 `onDragStart` 유무로만 정해진다 — 무변경).
- **호출 자리** — `api.ts` 밖 `fetch` **0건**(grep 전수).
- **재사용** — `Badge`·`taskStateLabel`·`taskStateTone`·`derivedApprovalLabel` 을 **그대로** 썼다.
  새 배지 부품·새 라벨 표 **0개**. `packLanes` 를 복제하지 않고 `packBlocks` 를 **별개 물음**으로 두었다
  (한쪽은 날짜 줄, 한쪽은 분 단위 좌우 — 합치면 둘 다 나빠진다).
- **카피·스타일** — 한국어 문자열이 `labels.ts` 밖에 흩어지지 않았다(새 문자열 0개).
  컴포넌트에 임의 hex **0건**(`3px`·`6px` 은 `calendar.css` 가 쓰던 여백 그대로이고 주석이 그것을 적는다).
- **테스트** — 모델(`calendarModel.test.ts`)·컴포넌트(`CalendarPage.test.tsx`) 양쪽에 옆자리 검사가 있다.
- **allowed_paths** — 12개 전부 `frontend/`. 이탈 **0건**.
- **BE-4 대조** — `modules/work/application.py:791` 이 `approval` 을 **무조건** 싣고
  `_approval_from_rounds` 가 목록·상세와 **같은 함수**임을 읽기로 확인했다. 프론트 타입이 필수인 것과 맞는다.
- **테스트를 돌리지 않았다. 코드를 한 줄도 고치지 않았다.** 산출물은 이 리포트 하나.

---

## `git -C /Users/kknaks/orca/workspaces/Strong_hajin/strong-hajin-calendar status --short`

```text
 M frontend/src/features/calendar/CalendarInteractions.test.tsx
 M frontend/src/features/calendar/CalendarPage.test.tsx
 M frontend/src/features/calendar/CalendarPage.tsx
 M frontend/src/features/calendar/MonthGrid.tsx
 M frontend/src/features/calendar/ScheduleCard.tsx
 M frontend/src/features/calendar/WeekGrid.tsx
 M frontend/src/features/calendar/calendarModel.test.ts
 M frontend/src/features/calendar/calendarModel.ts
 M frontend/src/features/calendar/calendarWrites.test.ts
 M frontend/src/lib/labels.ts
 M frontend/src/lib/viewModels.ts
 M frontend/src/styles/calendar.css
```

(검수 시작 시점과 **같다** — 읽기만 했다.)
