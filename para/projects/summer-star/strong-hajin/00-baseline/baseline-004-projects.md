---
type: baseline
id: BASE-004
title: "「프로젝트」 화면 — 확정 시안과 조사 둘, 그리고 SPEC-001 이 이미 배제한 진행률"
status: raw
product: strong-hajin
created_at: 2026-09-21
updated_at: 2026-09-21
tags:
  - product/strong-hajin
  - doc/baseline
  - status/raw
links:
  baselines:
    - "[[baseline-003-calendar|BASE-003]]"
  decisions:
    - "[[decision-004-projects|DEC-004]]"
  specs: []
  works: []
  releases: []
  related:
    - "[[spec-004-calendar-scheduling|SPEC-004]]"
    - "[[spec-001-work-management|SPEC-001]]"
up:
  - single-source-of-truth
---

# 「프로젝트」 화면 — 확정 시안과 조사 둘, 그리고 SPEC-001 이 이미 배제한 진행률

업무는 **하나씩** 산다. 시안은 그 위에 **프로젝트 하나를 스코프로 잡는 한 화면**을 얹고,
그 안에서 업무들의 **기간과 순서**를 한눈에 보인다.
이 문서는 그 입력(시안·사용자 원문)과, 그것을 코드에 대 보고 나온 관측을 사실 그대로 둔다.

**판단하지 않는다.** 무엇을 채택할지는 DEC-004 가 가른다.

---

## Raw

### 입력 1 — 확정 시안 (2026-09-21 사용자 지정)

`reference/2026-09-10-sc-meeting/package 2/` 의 프로젝트 화면.

| 파일 | 무엇 |
|---|---|
| `Projects.html` | 화면 껍데기·로딩 순서 |
| `handoff/projects/js/projects.v1.jsx` | 화면 본체 — 3레일·요약 스트립·간트·의존선·우 레일 |
| `handoff/projects/js/data.js` | 목데이터 |
| `handoff/projects/css/projects.css` (13,510바이트) | `.scax-pj-*` 전용 스타일 |
| `handoff/shell/js/nav.js` · `handoff/shell/js/scax-ui.jsx` · `_ds_bundle.css` | 공용 셸·부품·토큰 |

**범위 밖**: `PROJECT_FILE_TREE`(자료 트리)는 `data.js` 에 있지만 **이 화면이 쓰지 않는다** —
시안 첫 줄 주석이 「자료함은 나중에 『자료』 탭으로 간다」고 명시한다.

#### 1-1. 틀 — 3레일

```
┌ SideNav ─┬ 좌 레일 380px ─┬ 본문 (flex) ──────┬ 우 레일 342px ─┐
│ 9항목    │ 「업무」 헤더    │ ① 요약 스트립      │ 선택 업무 상자  │
│ activeId │  + count 배지   │ ② 진행 라인(간트)  │  (없으면 Empty) │
│ ='project'│ + 프로젝트 셀렉터│   + ③ 의존선      │                │
│          │ 업무 카드 목록   │                   │                │
└──────────┴────────────────┴───────────────────┴────────────────┘
AppHeader: title 「프로젝트」 (breadcrumb·actions 없음)
```

- 레일 폭은 DS 토큰: `--scax-rail-left-width = --ax-inbox-w = 380px` ·
  `--scax-rail-right-width = --ax-calendar-w = 342px`. **업무·캘린더 화면과 같은 폭**이다
- 좌 레일 `border-right` + `shadow-card`, 우 레일 `border-left`. 둘 다 바닥까지
- 내비에서 「프로젝트」는 `folder` 아이콘, **업무 다음·캘린더 앞** 자리

#### 1-2. 좌 레일 — 프로젝트 셀렉터 + 업무 카드

- 헤더 한 줄: `square-check` 24px 아이콘 + **「업무」** + `Badge variant="count"` (건수).
  그 아래 `Select`(ariaLabel 「프로젝트 선택」) — **프로젝트 전환이 헤더에 있다.** 별도 목록 화면 없음
- 카드는 **업무 탭 `scax-inbox-card` 를 그대로 재사용**. 새 부품이 아니다
  - 구성: 상태 배지 → 제목 → meta 한 줄(`when` · 담당 · 분류)
  - 이 화면이 더하는 것은 **선택 상태뿐**: hover `accent-20`/`accent-05`,
    selected `border accent` + `bg accent-08`, focus `--scax-focus-ring`

#### 1-3. 본문 ① 요약 스트립

`grid-template-columns: repeat(4, minmax(96px,1fr)) minmax(180px,1.6fr)` — 5칸, 마지막이 넓다.

| 칸 | 라벨 | 값 색(tone) |
|---|---|---|
| 1 | 전체 업무 | `ink-strong` |
| 2 | 진행 중 | `accent` |
| 3 | 지연 | `danger` |
| 4 | 완료 | `positive` |
| 5 (wide) | 전체 진행률 | 6px 미터 바(`accent` fill) + % 텍스트 |

칸: `border line` · `radius-xl` · `surface`, 라벨 caption1 `ink-assistive`,
값 **24px/32px bold**, `tabular-nums`.

#### 1-4. 본문 ② 진행 라인(간트)

기하가 상수로 못 박혀 있다: `{ day: 34, row: 40, label: 200, days: 30, today: 17 }`

- 머리: 「진행 라인」(body1 semibold) + legend 「2026년 9월 · 화살표는 선행 → 후행」(caption1 assistive)
- 축: 1~30 일, 하루 34px, `today` 는 accent + semibold. 아래로 `line-weak` 경계
- 격자: 세로 34px · 가로 40px 의 `line-weak` 선. `now` 는 1px accent 세로선(opacity .5)
- 행(40px): `[twisty 16px][이름/담당 = label 200px][바]`
  - twisty 는 **하위 업무가 있을 때만**. `chevron-down/right`. 기본은 **모두 펼침**
  - 이름 2줄: 제목(label1 medium, ellipsis) / 담당·`하위 N`(caption2 assistive). 선택 시 accent semibold
  - 하위 행은 `padding-left: space-600` 들여쓰기, 이름 regular `ink-neutral`
- 바: 높이 **22px**(기본) / **14px 상위** / **18px 하위**, `radius-sm`, 안에 진행률 fill + % 텍스트.
  **상위 바는 % 를 숨긴다**(`projects.css` `.scax-pj-gantt__bar--parent .scax-pj-gantt__bar-pct{display:none}`).
  선택 시 `box-shadow 0 0 0 2px accent`

| status | 바 배경 | fill | 근거 |
|---|---|---|---|
| progress | `accent-20` | `accent` | `projects.css` |
| blocked | `danger-soft` | `danger` | `projects.css:55-56` |
| done | `fill-weak` | `positive` | `projects.css:57-58` |
| not-started | `fill-weak` | `line-strong` | `projects.css:59-60` |
| **cancelled** | **정의 없음** | **정의 없음** | `projects.css` 에 `--cancelled` 규칙이 **없다** (`grep` 확인) |

#### 1-5. 본문 ③ 의존선

- 간트 위에 겹치는 **SVG 오버레이**(`position:absolute; inset:0; pointer-events:none`)
- 경로는 직각 3구간: `M 선행끝 H 중간 V 후행행 H 후행시작-5` + 화살표 marker
- 평소 `line-strong` 1.2px, **선택된 업무에 닿는 선만** `accent` 1.6px

#### 1-6. 우 레일 — 선택 업무 상자

선택 없으면 `Empty`(icon `square-check`, 「업무를 선택하세요」).

머리: 제목(body1 semibold) + 진행률 미터(6px) + %. 본문은 블록 4개:

1. **메타 정보** — `dl` 2열(키 64px): 상태(배지) · 기간 · 담당 · 요청 · 분류 · 상위 업무
2. **관계** — 선행(`arrow-up`) / 후행(`arrow-down`) 각각 건수 + 목록.
   줄마다 status dot(accent/danger/positive) + 제목 + `chevron-right`, **누르면 그 업무로 이동**
3. **체크리스트** — `done/total` 카운트. 완료 항목은 accent 체크박스 + 취소선
4. **하위 업무** — 카드 목록(제목 + 상태 배지 / `9월 N–M일 · 담당 · N%`), 누르면 이동

#### 1-7. 상호작용 축 — 하나뿐이다

- `project`(셀렉터) = 화면 전체의 데이터 스코프
- `taskId` 하나가 **좌 레일 카드 · 간트 행/바 · 의존선 · 우 레일**을 동시에 묶는다.
  어디서 골라도 나머지 셋이 같이 반응한다
- 그 외 상태는 간트의 `open`(펼침 목록)과 내비 `collapsed` 뿐. **모달·드로어 없음**

### 입력 2 — 사용자가 말로 확정한 것 (2026-09-21)

원문 그대로 둔다. 해석은 DEC-004 가 가른다.

> "시안은 레이아웃 색 위치 등을 보려고 만든거고 상태값 논리구조는 이미 우리 있는 구조를 정본으로 할거야"

> "그래서 일단 시안 구조를 탐색하고 → 우리 프론트/백 워커 보내서 조사를 할거야"

> "프론트는 거의 다시 그린다고 보면돼"

> "b가 메인인데 a도 해야 하잖아 … b를 하는데 어차피 검증에서 걸리니까 a까지 하고 갈거라고"

(a = `material_*` 계약 테스트의 병렬 경합. 재료는
`reference/2026-09-21-strong-hajin-calendar/material-parallel-isolation.md`. b = 이 프로젝트 화면.)

D-3 진행률에 대해:

> "체크리스트로 계산하자"

관리 기능에 대해:

> "별도 모달로 옮긴다"

### 입력 3 — 조사 리포트 2건 (2026-09-21, read-only 발주)

`orchestration/work/strong-hajin-projects/` 에 있다. 둘 다 코드 변경 0건이고,
두 워커 모두 워크트리 `git status --porcelain` 공백을 보고에 적었다.

| 리포트 | 줄 | 무엇을 셌나 |
|---|---|---|
| `research-be-domain.md` | 726 | D-1~D-9 판정 · HTTP 159 라우트 중 48 · MCP 125 도구 중 project 8 · 목록 필터/정렬/페이징 현황 · 권한 · 문서↔코드 어긋남 6 |
| `research-fe-structure.md` | 500 | 현 프로젝트 화면 전수 · 부품 재고 · DS 토큰 대조 · API 호출 전수 · 충돌 지점 · 눈에 띈 것 7 |

---

## Context

### 이 입력이 서는 자리

BASE-002 / DEC-002 / SPEC-003 이 업무의 **생명주기**를, BASE-003 / DEC-003 / SPEC-004 가 그 위의
**시간 축**을 세웠다. 이번 입력은 **프로젝트를 스코프로 한 읽기 화면** 하나이고,
업무 자체의 규칙도 시간 배정의 규칙도 바꾸지 않는다.

### 관측 기준점

- 코드 레포 `Strong_hajin` 워크트리 `/Users/kknaks/orca/workspaces/Strong_hajin/strong-hajin-projects`,
  브랜치 `kknaksss/strong-hajin-projects` HEAD `e46ce39` (2026-09-21)
- 테스트·빌드를 **돌리지 않았다** — 조사 발주라 실행이 없다. 통과 수치를 근거로 쓰지 않는다
- BE 워커는 `frontend/` 를 열지 않았고, FE 워커는 `backend/` 를 열지 않았다

### 지금 「프로젝트 화면」은 시안과 같은 화면이 아니다

지금 것은 **본문 한 칸 안의 2컬럼 관리 화면**이다 — 프로젝트 목록 ↔ 담당자 붙이기/떼기 + 참여 이력
(`src/features/project/ProjectPage.tsx:146-330` · `src/styles/screens-a.css:232`).
겹치는 것은 「프로젝트를 고른다」 하나뿐이다.

| 축 | 시안 | 지금 코드 | 근거 |
|---|---|---|---|
| 레일 | 3레일 380/342 | **없다** — `App.tsx:352,515` 가 `onRegisterRails` 를 안 넘긴다 | FE §1-2 |
| 좌 칸 | 업무 카드 목록 + 프로젝트 `Select` | 프로젝트 `<ul>` 목록, 폭 `minmax(240px,320px)` | `ProjectPage.tsx:175-188` · `screens-a.css:232` |
| 선택 축 | `project` + **`taskId`** | `project` 하나뿐. 업무는 클릭도 안 되는 `<li>` | `ProjectPage.tsx:318-324` |
| 본문 | 요약 스트립 + 간트 + 의존선 | **담당자 관리 화면** (참여자 붙이기/떼기 · 참여 이력 · 새 프로젝트) | `ProjectPage.tsx:206-306` |
| 우 레일 | 선택 업무 상자 | 대응물 **0** | FE §1-2 |
| 라우팅 | `project`·`taskId` | **라우터가 없다** — `App.tsx:73` `useState<ProductSurface>`. URL·딥링크 없음 | FE §1-3 |

`ProjectPage` 를 겨누는 테스트는 `ProjectPage.test.tsx` **하나뿐**이고(`App.test.tsx` 에 「프로젝트」 0건),
그 안의 검사 **7개 중 6개가 다시 그리면 깨진다**(FE §1-4). 깨지는 것은 전부 **관리 UI 의 단언**이다.

---

## 화면이 요구하는 사실 D-1~D-9 와 우리 코드의 실제 모양

시안 목데이터의 구조가 아니라, **화면을 그리려면 반드시 있어야 하는 사실**만 뽑은 목록이다.
BE 리포트 §1 의 판정과 FE 리포트 §3-4 의 「프론트까지 내려오나」를 합쳤다.

| # | 화면이 요구하는 사실 | 시안의 가정 | BE 판정 | 우리 이름·모양 | 프론트까지 오나 |
|---|---|---|---|---|---|
| D-1 | 업무가 어느 프로젝트에 속하는가 | `tasks.project_id` | **있다** | `tasks.project_id` (UUID, nullable, FK, index) — `persistence.py` · `project_id` 는 **하위 업무에 전파**된다(`tests/contract/test_projects.py:316`) | **온다** (`viewModels.ts:209`) |
| D-2 | 업무의 시작일·종료일 | `from`/`to` (9월 정수일) | **있다(주의)** | `tasks.start_date`·`due_date` **둘 다 nullable**, `start_date > due_date` 역전도 실재(`schedule.py:7-11`). 정규화 함수 `task_span()` 이 이미 있다(`schedule.py:40-62`) | **온다** (`viewModels.ts:100-101,194-195`) |
| D-3 | 업무의 진행률 % | `tasks.progress` | **없다** | 저장 컬럼도 파생 계산도 응답 필드도 **없다**. 대체 재료는 `checklist_progress{done,total}`(`task_results.py:194,240,312`) · `child_progress{done,blocking,cancelled,total}`(`task_results.py:234,306`) 둘 | **안 온다** (`viewModels.ts` grep → 건수 둘뿐) |
| D-4 | 업무 간 선행 → 후행 | `task_dependencies` | **있다** | **별도 표** `task_predecessors`(`persistence.py:995-1040`). 응답은 `preceding_task_ids`(`task_results.py:93`) + 상세의 `predecessors[]`(`:111-121`). **후행(역방향) 조회가 저장소에도 application 에도 없다**(`work_tasks.py:1102-1127` 셋 다 `WHERE task_id IN (...)`) | **부분** — 선행만(`viewModels.ts:222,230`) |
| D-5 | 상위–하위 (시안은 **1단계만**) | `tasks.parent_id` | **다르다** | `tasks.parent_task_id` 자기참조(`persistence.py:937`). **저장 깊이에 제한이 없다**(`application.py:385-387`, 정책 V-6). 조회 표면은 **직속 하위만** 낸다(`http.py:1803`) | **온다** (`viewModels.ts:102,243-247`) |
| D-6 | 업무 체크리스트(텍스트 + done) | `task_checklists` | **있다** | **별도 표** `task_checklist_items`(`persistence.py:1097-1118`) — `text`·`position`·`done`·`state`·항목별 `version`. 집계 `checklist_progress{done,total}` | **온다** — 단 **업무 «상세» 응답에만** 실리고, `NotRequired` 라 `access=="read_only"` 면 안 실린다(`application.py:920-930`) |
| D-7 | 상태 5종 | `progress`·`not-started`·`blocked`·`done`·`cancelled` | **다르다** | 내부 **6종** `TaskState`(`lifecycle.py:20-26`): `open`·`in_progress`·`blocked`·`completion_submitted`·`done`·`cancelled`. 외부 투영 **5종** — `_external_state()` 가 `completion_submitted` 를 `done` 으로 접는다(`application.py:2495-2506`) | **온다** (`viewModels.ts:121` 5종 유니온) |
| D-8 | 담당자 · 요청자 · 분류 | `owner`·`requester`·`group` | **있다(부분)** | 담당 = **활성 `task_assignments` 행**(열이 아니다, `persistence.py:911-913`). 요청자 = `origin` 묶음(`task_results.py:168-172`). **「분류」는 필드가 아니라 어느 엔드포인트를 불렀나라는 축**이다(`grep "보낸 업무\|내 업무" backend/src/` → 응답 필드 0건) | **부분** — 프로젝트 조회에는 **하나도 없고**, 업무 상세에는 있다 |
| D-9 | 프로젝트 목록(선택지) | `PROJECT_OPTIONS` | **있다** | `projects` 는 **독립 엔티티**(`persistence.py:838-861`). `GET /api/projects` → `list[ProjectView]`(`http.py:1382`). **필터·정렬·페이징 없음**, `state` 로도 안 거른다, **집계 필드 0개** | **온다** — `Select` 옵션 선례 `WorkModals.tsx:4538` |

**집계: 있다 6 · 다르다 2 · 없다 1.**

### 간트가 필요한 것의 절반은 이미 한 방에 나온다

`GET /api/projects/{project_id}` 의 `tasks[]` 가 `state`·`start_date`·`due_date`·`parent_task_id`·
`preceding_task_ids` 를 함께 낸다(`modules/work/projects.py:240-251`).
이 배열은 「**간트 연결선의 유일한 원천**」이라고 주석이 계약으로 적고
(`project_results.py:35-37`), 계약 테스트가 그것을 지킨다
(`tests/contract/test_task_predecessors.py:448-461`).

### 그러나 그 배열은 6개 필드뿐이다

`ProjectTaskView` 에 **담당자도 origin 도 체크리스트도 그 집계도 없다**(`project_results.py:28-37`).
시안 좌 레일 카드의 meta(담당·분류)와 간트 이름줄의 담당, 우 레일 전체는
**업무 «상세» 조회**가 답한다 — 즉 지금 계약으로 한 프로젝트의 업무를 전부 깔면 **N번 호출**이 된다
(FE §3-4 요약).

---

## 부품 재고 — 새로 만들 것이 사실상 둘이다

FE §2 의 재고표. 판정: **있다** = 같은 이름·같은 역할로 쓸 수 있다 / **다르다** = 있지만 API·마크업·값이
어긋난다 / **없다** = 대응물 0.

| 시안 부품 | 판정 | 근거 |
|---|---|---|
| `AppShell` · `AppHeader` · `AppBody`(3레일) | **있다** | `src/shell/AppShell.tsx:37,46,74` — 시안 `scax-ui.jsx:207,264,288` 과 마크업 동일 |
| `SideNav` + `folder` + `activeId="project"` | **있다** | `src/shell/SideNav.tsx:70` · `App.tsx:39,398` — 아이콘까지 같다 |
| `scax-inbox-card` | **있다**(선택 상태만 없다) | CSS `components.css:111-121`, 조립 선례 `ScheduleCard.tsx:42-99` 가 시안 `ProjectTaskCard`(`projects.v1.jsx:8-28`)와 사실상 같은 코드. `.scax-inbox-card--selected` 는 저장소에 **0건** |
| `Badge`(tone 5종) · `Badge variant="count"` | **있다** | `ds/Badge.tsx:24,34,38` · `components.css:37-41`. 쓰임 선례 `InboxRail.tsx:108` · `ScheduleRail.tsx:86` |
| 글리프 7종 (`square-check` `chevron-down` `chevron-right` `arrow-up` `arrow-down` `check` `folder`) | **있다** | `glyphs.tsx:289,163,164,333,332,162,341` |
| `Icon` 크기 12/14/24 | **있다** | `ds/icons/Icon.tsx:21` — `12\|14\|16\|20\|24` 전부 받는다 |
| `Empty` | **있다**(크기만 다르다) | `ds/Empty.tsx:39,53`. ⚠ 글리프를 **20px 로 못박았다**(`Empty.tsx:70`), 시안은 24(`scax-ui.jsx:179`). props 이름도 다르다(우리 `description`, 시안 `desc`) |
| `.scax-gutter-list` 레일 껍데기 | **있다**(마크업으로) | `components.css:105-108` · 선례 `InboxRail.tsx:103-114` · `ScheduleRail.tsx:81-108` |
| `GutterList`(React 부품) | **다르다** | **이름이 같은 다른 부품**이다. 우리 `ds/GutterList.tsx:20-58` 은 「고정폭 메타 칸 + 본문」 표이고 **소비처 0건** |
| `Select` | **다르다** | `ds/Select.tsx:338-430` 있음. 시안 레일 헤더의 **알약꼴** `.scax-select__trigger` 는 **CSS 만** 있다(`components.css:44-49`). 다만 `trigger` prop 선례가 있다 — `MyWorkPage.tsx:1410`. 또 우리 것은 `label`·`labels`·`emptyActionLabel` 을 **필수**로 받는다(`Select.tsx:353,382,384`) |
| 진행률 미터(track+fill) | **다르다** | `ds/ProgressBar.tsx:5-41` 은 **`done`/`total` 을 받아 내부에서 % 를 계산**한다(`:18`). 시안은 `percent` 를 직접 받는다(`projects.v1.jsx:67,190`). 소비처 1곳(`WorkModals.tsx:1590`) |
| **간트**(축·격자·행·바·twisty) | **없다** | `grep -rin "gantt" src/` → **0건**. 날짜 축 위에 막대를 그리는 화면이 저장소에 없다 |
| **의존선 SVG 오버레이** | **없다** | `pointer-events` 를 쓰는 SVG 오버레이 **0건**. 노드-엣지를 그리는 유일한 자리는 sigma/graphology 캔버스이고 **SVG 가 아니다** |

> **관측**: **새로 만들 것이 사실상 간트·의존선 둘**이다. 나머지는 있거나(재사용), 값 하나가 다르다.
> 코디네이터는 이 재고를 `_RESUME.md` 이력에 **19항목(있다 13 · 다르다 4 · 없다 2)** 으로 셌다.
> 위 표를 직접 다시 세면 행 묶는 방식(글리프 7종을 한 항목으로 접는가, `Empty` 를 「있다」로 세는가)에
> 따라 수가 달라진다 — **셈의 차이이고 판정의 차이가 아니다.** 판정은 위 표가 정본이다.

### DS 토큰은 이름까지 같다 — 없는 것 0개

시안 `projects.css` 가 참조하는 토큰을 전수 확인했고 **없는 것이 0개**다(FE §2-1 표) —
색(`accent`/`-05`/`-08`/`-20`, `danger`/`-soft`, `positive`, `ink` 5종, `line` 3종, `surface`, `fill-weak`) ·
간격 9종 · 반경 7종 · 타입 4종 · `--scax-focus-ring` · `--scax-shadow-card` ·
`--scax-control-height-sm`(32px) · `--scax-duration-fast`(120ms).

레일 폭도 값까지 같다: `--scax-rail-left-width`(`scax.css:119`) → `--ax-inbox-w`(`product.css:79`) = **380px**,
`--scax-rail-right-width`(`scax.css:120`) → `--ax-calendar-w`(`product.css:80`) = **342px**.

**상태 톤 5종은 한 칸도 안 틀린다**(FE §3-5). 라벨 둘만 말이 다르다:

| 시안 status | 시안 label / tone | 우리 `TaskState` | 우리 label / tone | 일치 |
|---|---|---|---|---|
| `progress` | 진행 중 / `accent` | `in_progress` | 진행 중 / `accent` | 라벨·톤 ✅ |
| `not-started` | 대기 / `neutral` | `open` | **시작 전** / `neutral` | 톤 ✅ · 라벨 다름 |
| `blocked` | 지연 / `danger` | `blocked` | **막힘** / `danger` | 톤 ✅ · 라벨 다름 |
| `done` | 완료 / `positive` | `done` | 완료 / `positive` | ✅ |
| `cancelled` | 취소 / `neutral` | `cancelled` | 취소 / `neutral` | ✅ |

(우리 라벨·톤 표는 `src/lib/labels.ts:3-9,20-26`. 서버는 라벨·색을 주지 않는다 — **상수표다**.)

**`.design-sync/` 는 거울이지 원본이 아니다.** `_ds_bundle.css:711-712,847-848,1025-1026` 이
`product.css:79-80`·`scax.css:119-120`·`shell.css:137-138` 과 **같은 줄**이고,
`.design-sync/NOTES.md:43-45` 에 사용자 결정이 박혀 있다 — 「지금은 정본이 우리 꺼야, 코드 기준」.

---

## 조사가 드러낸 어긋남 — 이 화면에 닿는 것

BE §5·§7 의 6건과 FE §6 의 7건 중 **이 화면에 닿는 것**만 골랐다.

**③④ 는 그 뒤에 더해진 것이다** — 검수를 지난 뒤 사용자와 손자 업무·자동 초대를 파는 과정에서
코드를 다시 읽다 드러났다. 둘 다 **화면을 안 만들어도 이미 일어나고 있는 일**이다.

### ① 프로젝트 상세의 `tasks[].state` 가 `_external_state()` 를 안 지난다 — `completion_submitted` 가 샌다

- 계약: 밖으로 나가는 상태는 `completion_submitted` 를 `done` 으로 접는다
  (`modules/work/application.py:2495-2506`)
- 그런데 `modules/work/projects.py:244` 는 `"state": task.state` 로 **원값을 그대로** 낸다.
  `ProjectApplication` 은 `work.application` 을 import 하지 않아 그 투영을 지나지 않는다
- 따라서 **같은 업무가 `GET /api/projects/{id}` 에서는 `completion_submitted`,
  `GET /api/tasks/{id}` 에서는 `"done"`** 이다
- 이 화면은 좌 레일 배지·간트 바 색·요약 스트립의 「완료」 칸을 **전부 이 배열로** 그린다.
  프론트 어휘에 `completion_submitted` 가 **없으므로**(`viewModels.ts:111-120` 이 일부러 뺐다)
  그 값이 닿으면 라벨·톤을 못 찾는다

### ② `tasks_in()` 이 done·cancelled 를 안 거르고 페이징도 없다

- `platform/projects.py:204-209` 가 `WHERE project_id = ?` 뿐이다.
  **정렬은 `tasks.created_at` 오름차순, 필터 없음, 페이징 없음**
- 형제 함수 `tasks_in_projects()` 는 `include_closed` 를 갖는다(`work_tasks.py:1095-1096`) — **이쪽만 없다**
- 업무가 수백 건인 프로젝트에서 상세 하나가 전부를 싣는다.
  이 저장소에서 페이징이 있는 목록은 `/api/meetings`(20건 커서) **하나뿐**이다(BE §2-2)

### ③ 손자의 `project_id` 가 「만든 순서」에 따라 갈린다 — 옮기면 손자가 프로젝트 밖에 남는다

**만들 때는 상속된다.** `project_for()` 는 parent 가 있으면 **부모의 프로젝트를 그대로 반환**한다
(`modules/work/application.py:365-367`) — 묻지도 않고, 깊이도 안 본다.
그래서 손자는 **태어날 때 조부의 프로젝트를 물려받는다.**

**옮길 때는 직속 하위만 갱신한다.** 업무의 프로젝트를 바꾸는 경로가
`children_of(task_id)` 로 자식을 훑는데(`modules/work/application.py:532-536`),
그 질의가 `WHERE parent_task_id == task_id` 한 줄이다
(`platform/work_tasks.py:475-482`) — **직속 자식뿐이고 재귀가 없다.**

**하위는 스스로 고칠 수도 없다.** 하위 업무가 자기 프로젝트를 직접 바꾸는 것은 막혀 있다
(`modules/work/application.py:522-524`).

세 줄을 합치면 결과가 하나다 — **상위 업무를 다른 프로젝트로 옮기면 자식은 따라가고
손자는 옛 프로젝트에 남는다. 그리고 영영 돌아올 길이 없다.**
같은 트리의 업무가 서로 다른 `project_id` 를 갖게 되고, 손자는 **어느 프로젝트 화면에도 안 보인다.**

⚠ 이것이 어긋남 ①②와 다른 점: ①②는 **화면이 잘못 그린다**이고,
이것은 **데이터가 조용히 갈라진다**이다. 화면을 안 만들어도 이미 일어나고 있다.

### ④ 배정·발송이 「받는 사람이 그 프로젝트를 읽을 수 있나」를 안 본다

- 업무의 프로젝트는 `project_for()` 가 정하는데, **parent 가 있으면 부모 것을 그대로 반환하고
  거기서 끝난다**(`modules/work/application.py:365-367`) — `readable_project_ids` 검사를
  **지나지 않는다.** 검사는 parent 가 없는 경로에만 걸린다
- 한편 배정 후보는 **두 축**에서 온다. 프로젝트 축의 후보는 그 프로젝트의 멤버뿐이지만,
  **조직 축에서 온 후보는 프로젝트 밖 사람일 수 있다** —
  `assignable_members`(`modules/work/projects.py:281-296`)의 주석이 프로젝트 축 후보는 멤버뿐이라고 적는다
- **프로젝트는 「붙어 있는가」 하나로만 열린다**(`modules/work/projects.py:304-312`, 위 「권한」 절).
  그래서 조직 축에서 온 사람에게 프로젝트 안 업무를 배정하면,
  **그 사람은 자기가 하는 일의 프로젝트를 못 읽는다** — 읽을 수 없는 프로젝트는 404 다(`:314-319`)

즉 업무는 프로젝트에 들어가는데 **사람은 안 들어간다.** 붙이는 쪽과 여는 쪽이 같은 조건을 안 본다.

### ⑤ 그 밖 — 이 화면에 닿지만 이번 결정의 중심이 아닌 것

| # | 무엇 | 근거 |
|---|---|---|
| ⑤-1 | `modules/work/projects.py:209-218` `list()` 가 전 프로젝트를 읽고 파이썬에서 거른다 | BE §7-3 |
| ⑤-2 | `persistence.py:935-936` 의 「One level only for now」 주석이 코드보다 낡았다 — `parent_for()` 에 깊이 검사가 없다 | BE §5-2 |
| ⑤-3 | `task_results.py:69` 의 「넷뿐이다」가 실제 외부 5종과 어긋난다 (`blocked` 가 그대로 통과한다) | BE §5-4 |
| ⑤-4 | **프로젝트를 닫는 명령이 없다** — `PROJECT_STATES = ("active","closed")` 인데 `"closed"` 를 세우는 API 가 없다 | BE §6 |
| ⑤-5 | `ProjectApplication.assign()` 이 `member` 를 `lead` 로 승격하는 길이 없다 | BE §7-8 |
| ⑤-6 | `ProjectDetail.tasks[].state` 가 `string` 으로 느슨하다 — `ProjectPage.tsx:321` 이 억지 캐스팅하고 `?? task.state` 로 원문을 흘린다 | FE §6-3 |
| ⑤-7 | `ProjectPage.tsx:325` — 업무 0건이고 내가 안 붙어 있으면 **빈 `<li>`** 가 DOM 에 남는다 | FE §6-4 |
| ⑤-8 | 내비 순서가 주석과 다르다 — `App.tsx:34` 는 「시안에 맞추고」라 적는데 실제는 업무 → 캘린더 → 프로젝트 | FE §6-1 |
| ⑤-9 | `.project-layout` 반응형이 `.dashboard-columns`·`.report-grid` 와 **같은 규칙에 묶여 있다**(`components.css:692-693`) — 그 줄을 손대면 홈·보고가 같이 움직인다 | FE §4-3 A |

---

## 조사가 뒤집은 전제 — 진행률은 빠뜨린 것이 아니라 **배제한 것**이다

**여기가 이 baseline 의 값이다.**

시안은 % 를 **네 자리**에서 그린다 — 요약 스트립의 「전체 진행률」, 간트 바 안의 fill·%,
우 레일 머리의 미터, 하위 업무 카드의 「N%」.

우리에겐 그 값이 하나도 없다. **그런데 그건 누락이 아니다.**

> `20-spec/spec-001-work-management.md:200` (§U-3 목록 행):
> 「**기한 경과일**: 실제 기한을 넘긴 행에만 날짜 뒤에 `+N` 을 붙인다. **진행률은 쓰지 않는다.**」

- 코드가 그 결정과 **정확히 일치한다** — `grep -rn "percent|progress_rate|진행률|completion_rate|progress_pct" backend/src/` → **0건**,
  `tasks` 전 컬럼 열거(`persistence.py:910-958`)에 progress 계열 없음(BE §6)
- SPEC-001 이 그 자리에 대신 둔 것은 `derived.overdue_days` 다(`application.py:2521-2529`) —
  정확히 그 `+N` 이고, **끝난 일에는 null** 이다
- MCP 도구 `task_progress_batch`(`mcp.py:1957`)는 **% 가 아니다** — 상태 전이·체크리스트 조작을
  한 번에 사람이 확인하는 배치다. 이름만 겹친다

**즉 시안은 SPEC-001 의 결정을 모른 채 그렸다.** 「진행률을 어디서 가져오나」가 아니라
**「배제한 결정을 뒤집을 것인가, 다른 값으로 그 자리를 채울 것인가」**가 물음이다.
DEC-004 가 가른다.

### 대체에 쓸 수 있는 재료 — 있는 것만 나열한다

| 재료 | 모양 | 어디서 나오나 |
|---|---|---|
| `checklist_progress` | `{done: int, total: int}` | `TaskListEntry`(`task_results.py:194`) · `TaskDetailResult`(`:240`) · `TaskChecklistResult.progress`(`:312`). 계산 `checklist_progress_for()`(`application.py:125` 포트) |
| `child_progress` | `{done, blocking, cancelled, total}` | `TaskDetailResult`(`task_results.py:234`) · `GET /api/tasks/{id}/children`. 계산 `application.py:1361` |
| `state` 자체 | `done`/`cancelled` 이면 종결 | 어디서나 |
| `derived.overdue_days` | `int \| None` — 기한 초과 일수, **끝난 일에는 null** | `task_results.py:47` |
| `started_at` / `completed_at` / `reopened_at` | datetime | `persistence.py:949,952,955` |

⚠ **`checklist_progress` 도 `child_progress` 도 프로젝트 상세 `tasks[]` 에 실리지 않는다**
(`project_results.py:28-37`).

---

## 관측 — 화면 자리별로 지금 무엇이 나오고 무엇이 안 나오나

BE §3 의 대조표다. **판단이 아니라 대조다.**

### 업무 트리의 실제 모양 — 요청을 주고받으면 3층이 기본값이다

사용자가 요청 업무의 트리를 **원문 그대로** 그려 보였다 (2026-09-21):

> 「나 / 보고서작성 (상위) / |-보고서 디자인 업무요청 (하위 , 디자이너요청)
>  디자이너 / 보고서 디자인 업무요청(수락) / |- 디자인 시안 조사(하위)」

**이것이 설계대로 되는 모양이다.** `_is_central_task()`(`modules/work/application.py:457-469`)가
「**부모를 든 사람 ≠ 이 업무를 든 사람이면 중심 업무**」라고 판정하고, 그 자리 주석이 적는다 —
「다른 사람이 수락한 요청 업무는 **그 사람의 새 중심 업무**이고, 그래서 **자기 직속 하위와 하위 요청을 가질 수 있다**」
(정책 V-7 · P-3).

따라서 위 그림의 「디자인 시안 조사」는 **조부(「보고서작성」)에서 세면 손자**다.
**예외가 아니라 요청을 한 번 주고받으면 나오는 기본값**이다.

**요청을 보낼 때 프로젝트는 이미 상속된다.** 요청 생성 경로가 `project_for()` 를 그대로 지나고
(`modules/work/requests.py:371-375`), 그 자리 주석이 「**하위 요청은 묻지 않고 상위를 따른다**」고 적는다.
받는 사람이 그 프로젝트에 있는지는 **보지 않는다**(어긋남 ④).

**그리고 수락은 새 업무를 만들지 않는다** — `modules/work/requests.py:457-458` 주석:
「**같은 업무의 담당이 확정된다 — 새 업무가 생기지 않는다**」.
즉 위 그림의 두 줄(「보고서 디자인 업무요청」 / 「(수락)」)은 **한 업무의 앞뒤**이지 두 업무가 아니다.
트리의 깊이는 수락으로 늘지 않고, **그 업무 아래에 하위가 달릴 때** 늘어난다.


### 좌 레일

| 필요 | 있나 | 어디서 |
|---|---|---|
| 프로젝트 선택지 | ✅ | `GET /api/projects` → `ProjectView.name` |
| 업무 건수 배지 | ✅ | `tasks[].length` |
| 상태 배지 | ⚠ | `tasks[].state` — `completion_submitted` 가 그대로 나온다(어긋남 ①) |
| 제목 · meta `when` | ✅ | `tasks[].title` · `start_date`·`due_date` |
| meta 담당 | ❌ | `ProjectTaskView` 에 없다 |
| meta 분류 | ❌ | 그런 필드가 없다 (D-8) |

### 본문 ① 요약 스트립

| 칸 | 있나 | 어떻게 |
|---|---|---|
| 전체 업무 | ✅ | `tasks[].length` |
| 진행 중 | ✅ | `state=="in_progress"` 세기 |
| 지연 | ⚠ | `derived.overdue_days` 가 그 답인데 프로젝트 상세 `tasks[]` 에 **없다**. `due_date` 로 클라이언트 계산은 가능 |
| 완료 | ✅ | `state=="done"` 세기 — 승인 대기 done 이 섞인다 |
| 전체 진행률 | ❌ | **없다** (D-3) |

### 본문 ② 간트 + ③ 의존선

| 필요 | 있나 | 어디서 |
|---|---|---|
| 바의 시작·끝 | ✅ | `tasks[].start_date`·`due_date` — null·역전 처리 필요. `task_span()` 규칙이 이미 있다 |
| 바 색(status) | ✅ | `tasks[].state` |
| 바 안 fill·% | ❌ | **없다** (D-3) |
| 상위–하위 행 | ✅ | `tasks[].parent_task_id` — 깊이 무제한(D-5) |
| `하위 N` 카운트 | ⚠ | 평평한 `tasks[]` 에서 클라이언트가 셀 수 있다. 서버 집계 `child_progress` 는 상세에만 |
| 이름 줄의 담당 | ❌ | `ProjectTaskView` 에 없다 |
| 의존선 | ✅ | `tasks[].preceding_task_ids` — **계약으로 「간트 연결선의 유일한 원천」** |

**선행에는 깊이 제한이 없다.** `_resolve_predecessors()`(`modules/work/application.py:1116-1158`)가
보는 것은 넷뿐이다 — **같은 프로젝트인가 · 읽을 수 있는가 · 자기 자신이 아닌가 · 중복·순환이 아닌가.**
트리에서 몇 층인지도, 부모가 누구인지도 **안 본다.**
그래서 **손자 업무가 조부의 형제를 선행으로 가질 수 있고**, 실제로 막는 코드가 없다.

**그리고 시안은 그 선을 조용히 버린다.** 시안 `DepLines` 가 양 끝 업무의 좌표를 찾고
`if (!a || !b) return`(`handoff/projects/js/projects.v1.jsx:85-106`) 으로 **말없이 빠져나간다** —
경고도, 빈 자리도 남기지 않는다.
간트가 깊이 2 에서 잘리면 손자 행의 좌표가 없으므로 **그 선이 사라지고,
화면은 「선행 없음」이라고 말한다.** 틀린 그림이 아니라 **없는 그림**이 된다.


### 우 레일 — `GET /api/tasks/{task_id}` 가 답한다

| 블록 | 필요 | 있나 |
|---|---|---|
| 머리 | 제목 | ✅ `title` |
| 머리 | 진행률 미터 + % | ❌ (D-3) |
| 메타 | 상태 · 기간 · 담당 · 요청 · 상위 업무 | ✅ `state`(+`derived.approval`) · `start_date`/`due_date` · `assignee` · `origin.actor` · `parent` |
| 메타 | 분류 | ❌ 그런 필드가 없다 |
| 관계 | **선행** 건수+목록 | ✅ `predecessors[]` — 읽을 수 없으면 `title`/`state` 가 null, **자리는 남는다**(`task_results.py:112-116`) |
| 관계 | **후행** 건수+목록 | ⚠ **서버 경로 없다.** 프로젝트 상세 `tasks[].preceding_task_ids` 를 뒤집으면 프로젝트 범위 안에서는 만들 수 있다 |
| 체크리스트 | done/total + 항목 | ✅ `checklist[]` + `checklist_progress` — 둘 다 `NotRequired`, `access=="read_only"` 면 안 실린다 |
| 하위 업무 | 카드 목록 | ✅ `children[]` (`TaskSummaryView`) |
| 하위 업무 | 카드의 「N%」 | ❌ (D-3) |

### 권한 — 화면이 부딪힐 자리

- **프로젝트는 「붙어 있는가」 하나로만 열린다.** 부서로도, 만든 사람이라는 사실로도 열리지 않는다
  (`modules/work/projects.py:304-312`). 읽을 수 없는 프로젝트는 **없는 것처럼 404** 다(`:314-319`)
- **읽을 수 있는 프로젝트가 0개인 사용자가 정상이다** — 배정이 유일한 열쇠이므로(BE §4)
- 프로젝트 상세의 `tasks[]` 는 **담당·조직과 무관하게 그 프로젝트의 업무 전부**를 낸다.
  같은 프로젝트에 있으면 남의 업무 상세도 열리고(`tests/contract/test_projects.py:86-93`),
  프로젝트에서 빠지면 그 순간 닫힌다(`:101`)
- **선행은 같은 프로젝트 안에서만 성립한다** — `TaskPredecessorProjectMismatch`(`application.py:1139-1141`).
  프로젝트 없는 업무는 선행을 가질 수 없다
- `may_manage: bool` 을 서버가 직접 낸다(`modules/work/projects.py:234-235`) —
  화면이 권한을 추측해 단추를 그리지 않는다

### 비용이 어디 있나

- **선행(D-4)과 시간 배정은 어제·그저께 들어왔다** — `task_predecessors` 는 `1b40f83`(2026-09-20),
  `task_schedules` 는 `e46ce39`(2026-09-21). **이 화면이 기대는 두 축이 가장 새것이다**(BE §2-5)
- **Alembic 도 migrations 체계도 없다.** 스키마는 `Base.metadata` 가 정본이고
  `make sync-demo-schema` 가 없는 표·컬럼만 더한다
- **화면 전용 CSS 파일을 새로 두는 선례가 이미 있다** — `calendar.css`·`meetings.css`·`workspace.css`.
  `index.css:16-40` 에 `@import` 한 줄을 더하는 것이 기존 방식이다
- **레일 등록 seam 도 이미 있다** — `App.tsx:130-131`, 선례 `MyWorkPage.tsx:941-972` ·
  `CalendarPage.tsx:460-477`. 새 배관이 필요 없다
- 비용은 **간트·의존선의 신설**과 **한 화면에 필요한 사실을 모으는 데이터 접합**에 몰려 있다

---

## 아직 안 정한 것

조사 둘이 드러낸 자리를 이 baseline 은 **답하지 않는다.** DEC-004 가 가른다.
DEC-004 에서도 닫지 못한 것은 그 문서의 「미결 사항」에 **질문 그대로** 남는다.

리포트가 **안 본 것**도 사실로 남긴다.

- BE 워커는 `frontend/` 를 열지 않았고, FE 워커는 `backend/` 를 열지 않았다.
  두 판정이 겹치는 자리(D-3·D-4·D-6·D-8)는 각자의 층에서만 본 것이다
- 두 워커 모두 **테스트를 돌리지 않았고 서버·DB 를 띄우지 않았다.** 정적 읽기만이다
- `_ds_bundle.css`·`_ds_bundle.js` 를 전수로 읽지 않았다. 토큰 대조는 **참조 이름**을 맞춘 것이고,
  번들과 저장소의 **값**이 같은지는 `product.css:79-80` 등 표본 세 줄만 확인했다
- `ProjectPage.tsx:54-73` `reload` 의 deps 문제(FE §6-5)는 **확인만 했고 재현하지 않았다**
- `material_*` 병렬 격리(Phase 0)는 **이번 조사와 섞지 않았다** — 원인 규명도 격리 수단도
  아직 조사되지 않았다. 재료는 `reference/2026-09-21-strong-hajin-calendar/material-parallel-isolation.md` 뿐이다
