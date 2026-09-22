---
type: baseline
id: BASE-003
title: "캘린더 — 확정 시안과 「업무에 시간을 배분한다」, 그리고 조사가 뒤집은 전제 둘"
status: raw
product: strong-hajin
created_at: 2026-09-20
updated_at: 2026-09-20
tags:
  - product/strong-hajin
  - doc/baseline
  - status/raw
links:
  baselines:
    - "[[baseline-002-task-lifecycle-v2|BASE-002]]"
  decisions:
    - "[[decision-003-calendar|DEC-003]]"
  specs: []
  works: []
  releases: []
  related:
    - "[[spec-003-task-lifecycle-v2|SPEC-003]]"
up:
  - single-source-of-truth
---

# 캘린더 — 확정 시안과 「업무에 시간을 배분한다」, 그리고 조사가 뒤집은 전제 둘

업무는 **날짜 단위**로 산다. 시안은 그 위에 **시간 단위**를 하나 더 얹는다.
이 문서는 그 입력(시안·사용자 원문)과, 그것을 코드에 대 보고 나온 관측을 사실 그대로 둔다.

---

## Raw

### 입력 1 — 확정 시안 (2026-09-20 사용자 지정)

`reference/2026-09-10-sc-meeting/package 2/` 의 캘린더 화면.

| 파일 | 무엇 |
|---|---|
| `Calendar.html` | 화면 껍데기·로딩 순서 |
| `handoff/calendar/js/calendar.v1.jsx` (343줄) | 화면 본체 — 3분할·월 뷰·좌측 레일 |
| `handoff/calendar/js/week.jsx` (245줄) | 주 뷰 — 종일 + 0~24시 시간 격자 |
| `handoff/calendar/js/data.js` · `handoff/shared/js/work-data.js` | 목데이터 |
| `handoff/calendar/css/calendar.css` (103줄) | 스타일 |

> **사용자 원문**: "이거 시안인데 이거 레이아웃으로 적용하는게 이번 작업에 목표야"

### 입력 2 — 사용자가 말로 확정한 것 (2026-09-20)

원문 그대로 둔다. 해석은 아래 Context 에서 가른다.

> "업무를 보통 날짜 단위로 생성 하는데 / 이번주에 내가 맡은 업무 중에 시간을 배분하고 싶은거야 /
> 월~수 까지 해야하는 업무가 있으면 / 월요일은 오전 몇시에 / 화요일은 오후에 / 수요일은 오전에 /
> 이렇게 시간을 배정하는 거 거든"

> "그래서 지금 js 시안 구조상 / 목,금에는 배정 할 수 없게 되어 있을거야 /
> 또 업무 일정이 없는거는 드래그 앤 드랍으로 일정 부터 생성 하게 하고 거기에 시간을 둘거 같은데 /
> 또 업무 일정을 좌우 이동하면서 바꿀수도 잇고 아니야 ?"

> "기간이 바뀌면 스케쥴 검증ㅇ은 해야지 / 바뀐 기간밖에 스케쥴은 삭제(소프트딜리트) /
> 다시 해당 기간으로 돌려도 / 새 스케쥴을 넣어야 해 / 그리고 상태값 정본은 우리 백엔드가 가지고 잇는거야 /
> 디자이너가 상태값에 대한 이해가 없어서서"

> "스케쥴은 그렇게 중요한게 아니야 업무가 중요해서 종속된 개념으로 생각하면 돼 /
> 완료시점에도 일단은 그냥 스케쥴은 지워도 되는데"

### 입력 3 — 조사 리포트 2건 (2026-09-20, read-only 발주)

`orchestration/work/strong-hajin-calendar/` 에 있다. 둘 다 코드 변경 0건이고,
코디네이터가 `git status` 공백과 핵심 주장 표본을 직접 검증했다.

| 리포트 | 줄 | 무엇을 셌나 |
|---|---|---|
| `be-survey-report.md` | 764 | 새 표를 세울 때 닿는 자리 · 날짜가 바뀌는 경로 · 상태가 바뀌는 경로 · 소프트 딜리트 선례 · 회의 API · 가시성 |
| `fe-survey-report.md` | 727 | 시안 상호작용 명세 · 현 캘린더 표면 · DS 부품 12종 대조 · 데이터 · 상태값 · 스타일 |

---

## Context

### 이 입력이 서는 자리

BASE-002 / DEC-002 / SPEC-003 이 업무의 **생명주기**를 세웠다. 이번 입력은 그 위에
**시간 축**을 얹는 것이고, 업무 자체의 규칙을 바꾸지 않는다.

### 관측 기준점

- 코드 레포 `Strong_hajin` `origin/main` = `1b40f83` (2026-09-20 fetch)
- 워크트리 `/Users/kknaks/orca/workspaces/Strong_hajin/strong-hajin-calendar`
- 테스트·빌드를 **돌리지 않았다** — 조사 발주라 실행이 없다. 통과 수치를 근거로 쓰지 않는다.

### 원문의 「스케쥴」을 두 겹으로 가른다

사용자 원문의 「스케쥴」은 시안 목데이터의 `CAL_SCHEDULE` 을 가리키는데, 그 배열은
**저장 단위가 아니라 읽기 합본**이다. 실제로는 성격이 다른 둘이 섞여 있다.

| 시안의 `CAL_SCHEDULE` 행 | 정체 | 코드에 있나 |
|---|---|---|
| `taskId` 가 **없는** 행 | 회의 | **있다** — `meetings.starts_at`/`ends_at` |
| `taskId` 가 **있는** 행 | 업무의 그날 몇 시 배정 | **없다** |

---

## 원문이 확정한 것 — 시간 배정

시안 코드가 규칙을 조용한 가드로 표현한다. 사용자가 말로 확인해 준 것과 일치한다.

| # | 규칙 | 시안 근거 | 사용자 원문 |
|---|---|---|---|
| R1 | 배정은 **업무 기간 안에서만** 만들어진다 | `week.jsx:139` `canDrop` — `day >= taskFrom(t) && day <= taskTo(t)` | "목,금에는 배정 할 수 없게 되어 있을거야" |
| R2 | 기한 없는 업무는 **날짜부터** 생긴다. 그 다음에 시간 | `calendar.v1.jsx:206` — 기한없음 드롭 시 `{from: day, to: day}` / `canDrop` 의 `!taskFrom(t)` 가 시간 격자를 막는다 | "업무 일정이 없는거는 드래그 앤 드랍으로 일정 부터 생성 하게 하고 거기에 시간을 둘거" |
| R3 | 기간은 **띠를 끌어** 옮기거나(길이 유지) **좌우 손잡이**로 늘린다 | `calendar.v1.jsx:206`(이동) · `:213`(리사이즈) | "업무 일정을 좌우 이동하면서 바꿀수도 잇고" |
| R4 | 마감만 있던 업무는 손잡이를 끄는 순간 **기간을 갖는다** | `calendar.v1.jsx:213-215` — `due: undefined` 로 지우고 `from`/`to` 를 세운다 | — |
| R5 | 같은 업무는 **하루에 배정 한 칸** | `calendar.v1.jsx:221` `addSlot` 이 같은 `(taskId, day)` 를 조용히 덮어쓴다 | "월요일은 오전 / 화요일은 오후 / 수요일은 오전" |
| R6 | 시간은 **30분 눈금**, 기본 1시간 | `week.jsx:9` `WEEK_SNAP = 30` · `:98` `wkClock(min + 60)` | — |
| R7 | 주 뷰는 **종일 칸 + 0~24시 격자**, 8시에 맞춰 열린다 | `week.jsx:7` `WEEK_OPEN = 8` · `:6` `WEEK_ROW = 56`(1시간 = 56px) | — |
| R8 | 화면은 **3분할** — 사이드바 · 좌측 일정 레일 · 캘린더 | `calendar.v1.jsx:293` `AppBody railLeft` | "이거 레이아웃으로 적용하는게 이번 작업에 목표" |
| R9 | 탭 셋 — 전체 · 회의 · 업무 | `data.js:10-14` `CAL_TABS` | — |

---

## 원문이 확정한 것 — 기간이 바뀔 때

> "기간이 바뀌면 스케쥴 검증은 해야지 / 바뀐 기간밖에 스케쥴은 삭제(소프트딜리트) /
> 다시 해당 기간으로 돌려도 새 스케쥴을 넣어야 해"

- 검증 시점은 **기간 변경 시**다.
- 밖으로 나간 배정은 **소프트 딜리트** — 하드 딜리트가 아니다.
- **복구 경로가 없다.** 기간을 되돌려도 살아나지 않는다. 사람이 새로 넣는다.

> "스케쥴은 그렇게 중요한게 아니야 업무가 중요해서 종속된 개념으로 생각하면 돼 /
> 완료시점에도 일단은 그냥 스케쥴은 지워도 되는데"

- 배정은 업무에 **완전히 종속**이다. 독립된 약속이 아니다.
- 완료·취소 시 배정을 남길 이유가 없다.

---

## 조사가 뒤집은 전제 둘

**여기가 이 baseline 의 값이다.** 코디네이터가 대화 중 깔고 간 전제 둘이 조사로 무너졌다.

### 뒤집힌 전제 1 — 「상태 변경은 `transition_task` 한 자리를 지난다」

**틀렸다.** Task 의 `state` 를 바꾸는 자리가 아홉인데 `lifecycle.transition_task()` 를
지나는 것은 **하나뿐**이다 (`be-survey-report.md` §4).

| # | 자리 | 목표 상태 | lifecycle |
|---|---|---|---|
| 1 | `modules/work/application.py:1277` `submit_completion` | `COMPLETION_SUBMITTED` | 아니오 |
| 2 | `modules/work/application.py:1296` `accept_delivery` | **`DONE`** | **아니오** |
| 3 | `modules/work/application.py:1311` `request_delivery_changes` | `IN_PROGRESS` | 아니오 |
| 4 | `modules/work/application.py:1442` `transition` | 6종 전부 | **예 — 유일** |
| 5 | `modules/work/application.py:1518` `reopen` | `IN_PROGRESS` | 아니오 |
| 6 | `modules/work/application.py:1662` `_apply_proposal` | **`CANCELLED`** | 아니오 |
| 7 | `platform/work_tasks.py:1855` `close_request_task` | **`CANCELLED`** | **아니오 — 영속 계층** |
| 8 | `platform/work_tasks.py:2658` `decide` | **`CANCELLED`** | **아니오 — 영속 계층** |
| 9 | `platform/work_tasks.py:2715` `cancel` | **`CANCELLED`** | **아니오 — 영속 계층** |

`CANCELLED` 로 가는 길이 **다섯**, `DONE` 으로 가는 길이 **둘**이다.

두 가지가 특히 아프다.

- **2 (`accept_delivery`) 는 요청 업무의 정상적인 완료 경로다.** 코디네이터가 표본 검증했다 —
  `task.state = TaskState.DONE` 을 직접 대입한다. 여기를 빠뜨리면
  「요청받아 한 일은 완료돼도 배정이 살아 있다」가 된다.
- **7·8·9 는 영속 계층 안이다.** 그 안에서 `TaskActivityRecord` 를 직접 add 하고
  `ActivityLedger(...).record(...)` 를 직접 부른다. 도메인 규칙을 application 층에 걸면
  이 셋이 그 밑으로 빠져나간다.

시드·배치·관리 스크립트는 **깨끗하다** — `bootstrap/scenario.py:278-294` 가
"상태는 옮겨 적는 것이 아니라 그 사람이 실제로 옮긴다" 는 규약을 지킨다.

### 뒤집힌 전제 2 — 「`TaskCalendar` 를 다른 화면도 쓰니 못 고친다」

**틀렸다.** 실 소비처는 `CalendarPage` 하나뿐이다 (`fe-survey-report.md` §2-1).
다만 결론은 같다 — 시그니처·앵커·주 뷰 성격이 전부 달라 **새로 세우는 쪽**이 맞고,
`taskSpan` 은 `TaskTimeline` 이 같이 쓰므로 **읽기만** 해야 한다.

`.calendar-*` 가 새는 곳은 정확히 둘 — `TaskTimeline`(`.calendar-toolbar`)과
DS `DatePicker`(`.calendar-weekdays`, `DateField` 12자리 경유).

---

## 관측 — 지금 코드에 있는 것과 없는 것

| 축 | 시안 | 코드 | 판정 |
|---|---|---|---|
| 레이아웃 3분할 | `[SideNav][레일][캘린더]` | 본문 1칸. `App.tsx:468` 이 `onRegisterRails` 를 안 넘긴다 | 없다 |
| 월 뷰 | lane 배치 + 띠 + 드롭 + 손잡이 | lane·띠 있음 (`WorkViews.tsx:198-243`). 드롭·손잡이 없음 | 부분 |
| 주 뷰 | 종일 + 0~24시 격자 | 날짜 격자 7칸. `mode==="week"` 는 lane 을 8로 늘릴 뿐 | 없다 |
| 시간 배정 | 스케쥴 | 개념 자체가 없다. `api.ts` 호출 0건 | 없다 |
| 회의 | 탭으로 같이 낸다 | `CalendarPage.tsx:106` 주석 "이 화면은 업무만 낸다" | **뒤집힌다** |
| 날짜 표현 | `day: number`(달 안의 일 번호) | ISO `YYYY-MM-DD` | 불일치 |
| 상태값 | 시안 5종 | 백엔드 6종 · **프론트 5종**(`completion_submitted` 없음) | 셋이 다 다르다 |
| DS 부품 12 | — | 9 있음 · 1 이름충돌(`GutterList`) · 1 부분(`Empty`) · 1 없음(`TaskCreateModal`) | DS-gaps 8건 |
| 토큰 `--scax-*` 51종 | — | `styles/scax.css` 에 **51종 전부** (`comm` 결과 0) | 그대로 쓴다 |
| 클래스 `.scax-*` 71종 | — | 저장소에 0종, 이름 충돌 0 | 새로 쓰되 값은 복붙 |

### 비용이 어디 있나 — 예상과 달랐다

- **스키마는 거의 공짜다.** `persistence.py` 에 클래스 하나를 더하면
  `make sync-demo-schema` 가 표와 인덱스를 함께 만든다. 손 `.sql` 은 **기존 표에 인덱스를
  더할 때만** 필요하다. 이 레포에 마이그레이션 체계는 없다.
- **스타일도 거의 공짜다.** `calendar.css` 103줄 중 규칙 89줄이 값 수정 없이 옮겨진다.
- **비용은 `docs/unified-operations-inventory.json`(2.1MB) 에 있다.** 세 architecture 테스트가
  **AST 수준으로** 이 캡처를 강제한다 — `http.py` 를 파싱해 라우트마다 `http_signature`·
  `http_application_calls` 를 뽑고, `bootstrap/application.py` 를 걸어 `owning_calls` 를 뽑아
  비교한다. `tool_count` 129 · `http_count` 156 도 센다. **새 엔드포인트 하나가 행 하나와
  count 두 개를 요구한다.** 자동 갱신 스크립트는 찾지 못했다.
- **나머지 비용은 상호작용·데이터 접합**(FE)에 몰려 있다.

### D2 가 따를 모양이 이미 레포에 있다

`task_predecessors`(`persistence.py:1015-1022`)·`task_references`(`:1506-1515`)가
`released_at` / `released_by` + 부분 unique `WHERE released_at IS NULL` 을
**같은 자리의 같은 뜻으로** 이미 쓴다. R5(하루 한 칸)가 요구하는 유일성 모양과 글자 그대로 같다.

---

## 아직 안 정한 것

조사가 낸 Open Questions 24건(BE 12 · FE 12)은 이 baseline 이 **답하지 않는다.**
DEC-003 이 가른다. 그중 셋은 사용자 결정으로 이미 닫혔다(DEC-003 Decision 참조).

리포트가 **안 본 것**도 사실로 남긴다.

- FE 워커는 `backend/` 를 열지 않았다 — D4 의 6종을 프론트 쪽 사실만으로 적었다
  (백엔드 6종은 코디네이터가 `lifecycle.py:20-26` 에서 확인했다).
- `_ds_bundle.css`(4069줄)·`_ds_bundle.js`(1862줄)를 전수로 읽지 않았다. 토큰 비교는
  저장소 정의와 `calendar.css` 의 **참조**를 맞춘 것이고, 번들과 저장소의 **값**이 같은지는 안 봤다.
- `ds/GutterList.tsx` 의 기존 소비처를 세지 않았다 — 개명을 검토하려면 그 수가 필요하다.
- `docs/unified-operations-inventory.json` 의 갱신 방법을 확인하지 못했다.
