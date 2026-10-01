---
type: baseline
id: BASE-005
title: "업무 상세 — 관계 여섯이 지금 어디까지 서 있나, 그리고 확정 시안이 요구하는 것"
status: raw
product: strong-hajin
created_at: 2026-09-28
updated_at: 2026-09-28
tags:
  - product/strong-hajin
  - doc/baseline
  - status/raw
links:
  baselines:
    - "[[baseline-001-work-page|BASE-001]]"
    - "[[baseline-002-task-lifecycle-v2|BASE-002]]"
    - "[[baseline-004-projects|BASE-004]]"
  decisions:
    - "[[decision-006-task-detail|DEC-006]]"
  specs: []
  works: []
  releases: []
  related:
    - "[[spec-001-work-management|SPEC-001]]"
    - "[[spec-003-task-lifecycle-v2|SPEC-003]]"
    - "[[spec-005-projects|SPEC-005]]"
---

# 업무 상세 — 관계 여섯이 지금 어디까지 서 있나, 그리고 확정 시안이 요구하는 것

업무는 **하나씩** 산다. 그 하나를 여는 화면이 업무 상세다.
이 문서는 그 화면이 **관계 여섯**(상위·하위·선행·후행·참고·프로젝트)을 지금 어떻게 다루는지를
**스펙 / 서버 저장 / 서버 읽기 / 서버 수정 / 화면 표시 / 화면 수정** 여섯 칸으로 눕힌다.

**판단하지 않는다.** 무엇을 채택할지는 DEC-006 이 가른다.

---

## 읽는 규칙

| 표기 | 뜻 |
|---|---|
| **(스펙)** | `para/projects/summer-star/strong-hajin/20-spec/` 의 계약 문장 |
| **(서버)** | `backend/src/ax_workspace/` 의 코드 관측 — 조사 리포트 `be-survey-report.md` 가 원장 |
| **(화면)** | `frontend/src/` 의 코드 관측 — 조사 리포트 `fe-survey-report.md` 가 원장 |
| **(시안)** | 확정 시안 `reference/2026-09-10-sc-meeting/package 2/TaskDetail.html` 의 관측 |
| **(사용자)** | 2026-09-28 사용자가 말로 확정한 것 |

**경로 규약.** 코드 경로는 **저장소 루트 기준**으로 적는다 — `backend/src/ax_workspace/…` ·
`frontend/src/…`. 조사 리포트 둘의 경로 기준이 서로 달라(`be-survey-report.md:5` 는
`backend/src/ax_workspace/` 상대, `fe-survey-report.md:4` 는 루트 기준) 여기서 한 벌로 맞췄다.
문서 경로는 `para/projects/summer-star/strong-hajin/` 을 생략하고 파일명부터 적는다.

**조사 리포트 셋이 이 문서의 사실 원장이다.** 여기서는 그 결론을 접고 **원본 파일:줄**을 가리킨다.

| 리포트 | 범위 | 한계 |
|---|---|---|
| `orchestration/work/strong-hajin-design/spec-survey-report.md` | 문서 SSOT 전수 | 코드를 읽지 않았다 |
| `orchestration/work/strong-hajin-design/be-survey-report.md` | `backend/src/ax_workspace/` 170 `.py` 전수 | 테스트를 돌리지 않았고 런타임 응답을 확인하지 않았다 (`be-survey-report.md:707`) |
| `orchestration/work/strong-hajin-design/fe-survey-report.md` | `frontend/src/` 전수 | 브라우저로 확인하지 않았다 (`fe-survey-report.md:309`) |

---

## Raw

### 입력 1 — 확정 시안 (2026-09-28 사용자 지정)

`reference/2026-09-10-sc-meeting/package 2/TaskDetail.html` (409줄) 한 장에 **세 상태**가 들어 있다.

| 무대 | 무엇 | 줄 |
|---|---|---|
| **A** | 기본 — 선행이 끝나 시작할 수 있는 업무 | `TaskDetail.html:126-251` |
| **B** | 선행이 안 끝나 시작이 막힌 업무 | `TaskDetail.html:254-327` |
| **C** | 「연결 편집」 — 상위·프로젝트는 고르기, 나머지는 해제·추가 | `TaskDetail.html:330-405` |

시안이 스스로 적은 요약: 「업무 메타 · 업무 정보 · 연관 업무 · 자료 **네 덩어리**. 연관과 자료는
2열로 접는다. 목데이터이고 상호작용은 없다」 (`TaskDetail.html:117`).
그리고 범례 넷 — 「**NEW** 지금 화면에 없는 자리」 · 「선행 — 계약·서버 있음, **프론트 배선만**」 ·
「후행 — **같은 표를 반대로 읽기**」 · 「프로젝트 — **PATCH 이미 열림**」 (`TaskDetail.html:119-122`).

#### 1-1. 네 덩어리와 그 머리

- 덩어리 머리 `.block__row` 는 **한 벌**이다 — 「단추가 있든 없든 같은 높이·같은 활자로 서도록」
  주석이 명시한다 (`TaskDetail.html:35-41`). 셋(`업무 정보`·`연관 업무`·`자료`)이 **같은 레벨**이다.
- `업무 메타` 는 덩어리 머리를 쓰지 않는다 — `.meta` 가 제목 + 사실 줄 + 오른쪽 배지·단추다
  (`TaskDetail.html:81-87`, 마크업 `:131-146`).
- 2열은 `.cols` — `grid-template-columns: minmax(0,1fr) minmax(0,1fr)`, `gap:16px 22px`
  (`TaskDetail.html:44`). `업무 정보` 는 `.stack`(1열, `gap:14px`) (`:45`).

#### 1-2. 3행 스크롤

```
.scroll      max-height:105px  ← 기본 3행. 주석: "3행 = (34 + 경계선 1) × 3"
.scroll--tall max-height:280px ← 체크리스트만
```

근거 `TaskDetail.html:49-53`. 주석이 **왜**를 적는다 — 「목록은 «칸 안에서» 스크롤한다 —
하위 30개가 연관 업무를 화면 밖으로 밀지 않는다. 2열 격자에서 두 칸 높이가 어긋나는 것도
이 상한이 막는다」 (`TaskDetail.html:47-48`).
머리(`.cell__head` — 제목 `h5` · 셈 `.cell__n` · 단추)는 `.scroll` **밖**에 있다
(`TaskDetail.html:55-58`, 마크업 예 `:186-188`).

#### 1-3. 업무 메타가 내는 사실

| 무대 | 왼쪽 | 오른쪽 |
|---|---|---|
| A | 제목 「연동 규격 확인」 + 담당 · 기한 · 시작 · 결재 · 참조 | `진행중` 배지 + **「편집」 단추** |
| B | 제목 「연동 구현」 + 담당 · 기한 · 결재 (**시작·참조가 없다**) | `대기` 배지 (**편집 단추가 없다**) |

근거 `TaskDetail.html:131-146`(A) · `:258-266`(B).
**값이 없는 칸은 서지 않는다** — B 가 시작·참조를 빼고 그린 것이 그 관측이다.
**편집 단추가 A 에만 있는 이유는 시안이 적지 않았다** (§어긋남 ⑦).

#### 1-4. 연관 업무 2열 — 여섯 칸과 그 짝

```
상위 업무 | 프로젝트      ← .one (값 한 줄)
하위 업무 | 선행 업무     ← .scroll > ul.material-list
참고 업무 | 후행 업무     ← 같음
```

근거 `TaskDetail.html:174-225`(A) · `:293-323`(B) · `:339-402`(C).
`NEW` 딱지가 붙은 자리 — **프로젝트 · 선행 업무 · 후행 업무 · 연관 업무 덩어리 전체**
(`.isnew` 클래스: `:169`·`:180`·`:196`·`:214`; 딱지 규칙 `:105-109`).

#### 1-5. 칸마다의 셈(`.cell__n`)

| 칸 | A | B | C |
|---|---|---|---|
| 체크리스트 | `1 / 3` (`:157`) | `0 / 0` (`:281`) | — |
| 하위 업무 | `2 / 5 · 완료 막음 3` (`:186`) | `0 / 0` (`:303`) | `3` (`:359`) |
| 선행 업무 | `2 · 모두 완료` (`:197`) | `1 · 미완 1` (`:308`) | `2` (`:371`) |
| 참고 업무 | `1` (`:207`) | `0` (`:316`) | `1` (`:382`) |
| 후행 업무 | `3` (`:215`) | `0` (`:320`) | `2` (`:392`) |
| 참고 자료 | `2` (`:233`) | — | — |
| 결과 자료 | `0` (`:243`) | — | — |

**⚠ A 의 후행 셈이 `3` 인데 목록 줄은 둘이다** (`:218-219`) — 그 아래 「🔒 비공개 업무 **1건**이
이 업무를 기다립니다」가 선다 (`:222`). **셈이 비공개 건수를 포함한다**는 관측이다.
**C 의 하위 셈은 `2/5` 가 아니라 `3`** — 편집 모드의 셈은 **건수만**이다 (`:359`).

#### 1-6. 빈 상태 문구 (시안 원문 그대로)

| 자리 | 문구 | 줄 |
|---|---|---|
| 상위 업무 없음 | `없음` (`.one--empty`) | `:296` |
| 체크리스트 0 | 「단계가 없습니다.」 | `:283` |
| 하위 0 | 「하위 업무가 없습니다.」 | `:305` |
| 참고 0 | 「연결된 참고 업무가 없습니다.」 | `:317` |
| 후행 0 | 「이 업무를 기다리는 업무가 없습니다.」 | `:321` |
| 결과 자료 0 | 「등록된 결과 자료가 없습니다.」 | `:245` |
| 비공개 후행(A) | 「🔒 비공개 업무 **1건**이 이 업무를 기다립니다.」 | `:222` |
| 비공개 후행(C) | 「🔒 비공개 **1건**은 여기서 해제할 수 없습니다.」 | `:399` |

#### 1-7. 시작 막힘 (B)

`업무 메타` **바로 아래**, `업무 정보` **위**에 `section.drawer-section.notice.danger.isnew` 가 선다.

```
h4  시작할 수 없습니다
p   <b>연동 규격 확인</b>이 끝나지 않았습니다.
```

근거 `TaskDetail.html:268-271`. 그리고 같은 화면의 선행 칸이 `1 · 미완 1` + `진행중` 배지로
같은 사실을 한 번 더 낸다 (`:308-313`).

#### 1-8. 연결 편집 (C)

- 머리가 `연관 업무 편집` 으로 바뀌고 오른쪽에 **「취소」·「저장」** 둘 (`TaskDetail.html:334-338`).
- 상위 업무 · 프로젝트 = `select.rel__select`, **「— 없음 —」 옵션 포함** (`:343-356`).
- 하위 · 선행 · 참고 = 줄마다 **「해제」** + 아래에 **「추가」 + 셀렉터** 한 줄 (`:358-389`).
  - 「추가」는 **글자**이고 `.rel__addlabel` 이 **`--scax-color-accent`(파란색) · 600** 이다 (`:96`).
  - 셀렉터 첫 옵션은 「업무 고르기」 (`:367`·`:378`·`:388`).
- 후행 = 줄마다 **「해제」만**. **추가 줄이 없다** (`:391-400`).
- 편집 목록의 줄은 **제목 + 해제 두 칸**이고 제목이 단추가 아니라 `<span>` 이다 (`:99-100`, 마크업 `:362`).
- 무대 라벨이 계약을 한 줄로 적는다 — 「상위·프로젝트는 고르기, 나머지는 해제·추가.
  **유효성은 서버가 판정한다**」 (`:331`).

### 입력 2 — 사용자 확정 (2026-09-28)

DEC-006 이 원장이다. 여기서는 **이 문서가 사실로 눕힐 때 근거가 되는 것**만 옮긴다.

- 업무 상세는 **네 덩어리**이고 세 덩어리 제목은 같은 레벨이다
- `업무 정보` 는 1열(내용 → 체크리스트), `연관 업무`·`자료` 는 2열
- 「산출물」 표기를 **「결과 자료」**로 바꾼다
- **후행은 저장하지 않는다** — `task_predecessors` 의 같은 줄을 반대쪽에서 읽는다
- **못 읽는 후행은 건수만** 낸다
- **선행은 시작을 막고 하위는 완료를 막는다** — 문구를 갈라 쓰고 두 오류 코드를 합치지 않는다
- **상위 업무를 나중에 바꿀 수 있게 한다** · **상위를 옮길 때 하위가 V-8 을 어기면 거절한다**
- **후행 해제는 즉시 반영한다** · **알림은 이번 범위 밖**

---

## 관계 여섯 — 여섯 칸 표

### 2-1. 상위 ↔ 하위 (`parent_task_id`)

| 칸 | 지금 | 근거 |
|---|---|---|
| **스펙** | 관계 셋의 경계표가 상위를 「이 업무가 **어느 업무의 일부**인가 · 프로젝트와 무관 · 시작은 안 막고 **완료를 막는다** · 만들기 창 `업무 연결` 탭에서 단일 선택」으로 정한다 | `spec-001-work-management.md:1058` |
| | 저장 깊이 **제한 없음**(V-6), 상세는 **직속 하위만**(L-11), 중심 업무 판정과 V-8(직접 작업 중첩 금지) | `spec-003-task-lifecycle-v2.md:740` · `:237` · `:926-936` |
| | 판정은 **생성 시점**이고 담당이 나중에 바뀌어 어긋나도 **기존 구조를 깨지 않는다** — **(미정 EU-8)** 「소급 재배치를 이번에 만들지 않는다」 | `spec-003-task-lifecycle-v2.md:937-939` · 추적 `:1302` |
| **서버 저장** | `tasks.parent_task_id UUID NULL FK→tasks.id`, `index=True`. 별도 depth·path 열 없음 | `backend/src/ax_workspace/platform/persistence.py:937` |
| | 요청 쪽에도 같은 이름의 열 — `work_requests.parent_task_id`(+ index) | `backend/src/ax_workspace/platform/persistence.py:1682-1684`·`1633` |
| **서버 읽기** | 상세가 `parent:{task_id,title,state}` + `children:TaskSummaryView[]` + `child_progress:{done,blocking,cancelled,total}` 를 낸다 | `backend/src/ax_workspace/modules/work/application.py:1392-1398`; 타입 `modules/work/task_results.py:232-234`·`199`·`180` |
| | `GET /api/tasks/{id}/children` 가 **직속 하위만** | `backend/src/ax_workspace/entrypoints/http.py:1803`; 구현 `modules/work/application.py:1401-1410` |
| | 읽을 수 없는 하위는 **목록에도 건수에도 없다.** 다만 **완료를 막는 검사는 읽을 수 없는 하위까지 전부 센다** | `backend/src/ax_workspace/modules/work/application.py:1380-1391`·`1476-1490` |
| **서버 수정** | **없다 — 이것이 이번 판의 구멍이다.** `PATCH /api/tasks/{id}` 의 편집 계약 `TaskEditFields` 에 `parent_task_id` 가 **없고** `extra='forbid'` 라 보내면 **422** 다 | `backend/src/ax_workspace/modules/work/task_commands.py:45-58`; 라우트 `entrypoints/http.py:1524` |
| | 상위를 바꾸는 명령·엔드포인트를 **못 찾았다** | `be-survey-report.md:87` |
| | 만들 때는 넷이 받는다 — `POST /api/tasks` · `/api/tasks/assign` · `/api/work-requests` · 회의 승격 | `backend/src/ax_workspace/entrypoints/http.py:1355`·`1481`·`1997`·`824` |
| | ⚠ **`POST /api/tasks` + `assignee_id` 갈래는 `parent_task_id` 를 명시적으로 거절한다**(422) | `backend/src/ax_workspace/modules/work/creation_commands.py:168-198` |
| | 거절 계열: `TaskParentNotFound`(404) · `TaskParentClosed`(409) · `TaskParentUnassigned`(409) · `TaskParentCycle`(422) · `TaskDirectNesting`(409) | `backend/src/ax_workspace/modules/work/errors.py`; 매핑 `entrypoints/http.py:541-568` |
| **화면 표시** | 업무 상세 「상위 업무」 구획 — 「이 업무는 ○○의 하위 업무입니다」 + 상태. 조건 `parentTask` | `frontend/src/features/work/WorkModals.tsx:1779-1795` |
| | 업무 상세 「하위 업무」 구획 — `done/total` · 막는 수 · 취소 수 + 목록. 조건 `!readOnly` | `frontend/src/features/work/WorkModals.tsx:1804-1878` |
| | 프로젝트 사이드 패널 메타의 `상위 업무` 줄 · 간트 트리(깊이 무제한) · 그래프 `parent_of` 엣지 | `frontend/src/features/project/ProjectTaskPanel.tsx:159-168` · `features/project/projectModel.ts:94-108` · `features/graph/GraphCanvas.tsx:75` |
| **화면 수정** | 만들기 셋 — 「직접 작업 추가」(인라인) · 「하위 요청 보내기」(모달) · 생성 모달의 「상위 업무」 Select | `frontend/src/features/work/WorkModals.tsx:1069-1089`·`:2123-2140`·`:4496-4516` |
| | **떼기·옮기기 0건.** `TaskPatch` 에 `parent_task_id` 가 없고 api.ts 에 그 호출이 없다 | `frontend/src/lib/viewModels.ts:538-545` · `frontend/src/lib/api.ts:246-265` |
| **시안이 요구하는 것** | A·B 의 `상위 업무` 칸(`.one`, 없으면 「없음」) · C 의 **셀렉터(「— 없음 —」 포함)** · A 의 하위 칸 「추가」 단추 · C 의 하위 **해제 + 추가 셀렉터** | `TaskDetail.html:176-179`·`:296`·`:343-347`·`:186-188`·`:358-368` |

### 2-2. 선행 (`preceding_task_ids` · `task_predecessors`)

| 칸 | 지금 | 근거 |
|---|---|---|
| **스펙** | 관계 셋의 셋째 — 「이것이 **끝나야 시작**한다 · **같은 프로젝트 안** · **시작을 막는다** · 완료는 안 막는다 · 생성·수정 창에서 여러 개 한 번에」 | `spec-001-work-management.md:1060` |
| | 전이별 게이트표 — `open→in_progress` **건다** · `open→done`(직행) **건다** · `in_progress→done` **걸지 않는다** · 취소·보완 **걸지 않는다** | `spec-001-work-management.md:994-1006` |
| | 조회에 드러나는 자리 셋 — 업무 상세(`preceding_task_ids` + 요약, **볼 수 없는 선행은 제목 없이 건수만**) · 프로젝트 상세 업무 줄(**간트 연결선의 유일한 원천**) · 시작 거절 응답(**막는 선행의 이름**) | `spec-001-work-management.md:839-850` |
| | 수정은 **배열 전체 교체** · `expected_version` 필수 · 회차가 오르고 진행 기록에 남는다 · **전용 add/remove 를 두지 않는다** | `spec-001-work-management.md:831-836` · `decision-001-work-page.md:396-400` |
| | 권한은 「그 업무의 값을 고칠 수 있는 사람과 **같다**. 신규 권한을 만들지 않는다」 | `spec-001-work-management.md:1134` |
| | 화면 계약 셋 — U-13(선택·상세 줄) · U-14(막혔을 때) · U-15(간트 연결선) | `spec-001-work-management.md:460-504` |
| **서버 저장** | 전용 조인테이블 `task_predecessors` — `task_id`(뒤에 오는 업무) · `predecessor_task_id`(먼저 끝나야 하는 업무) · `position` · `created_by/at` · `released_at/by` | `backend/src/ax_workspace/platform/persistence.py:995-1045` |
| | 제약 셋 — 부분 unique `uq_task_predecessors_active(task_id, predecessor_task_id) WHERE released_at IS NULL` · CHECK `ck_task_predecessors_not_self` · index **`ix_task_predecessors_task_id`(task_id 하나)** | `backend/src/ax_workspace/platform/persistence.py:1014-1025` |
| | **`predecessor_task_id` 단독 인덱스가 없다** | `backend/src/ax_workspace/platform/persistence.py:1014-1025` |
| | 뗀 행은 지우지 않고 `released_at` 으로 닫는다 | `backend/src/ax_workspace/platform/persistence.py:1002-1004`·`1039-1041` |
| **서버 읽기** | `preceding_task_ids: list[str]` — **활성만·고른 순서**, `TaskMutationResult` 의 칸이라 생성·수정·전이·**목록**·상세 전부. **권한 필터 없음** | 조립 `backend/src/ax_workspace/modules/work/application.py:2485-2495`; 타입 `modules/work/task_results.py:90-93` |
| | `predecessors: [{task_id,title,state}]` — **업무 상세에만**. 같은 순서·같은 길이, 못 읽으면 `title`·`state` 가 `null` 이고 **자리만 남는다** | `backend/src/ax_workspace/modules/work/application.py:1266-1289`; 타입 `modules/work/task_results.py:111-121`·`237-238` |
| | `access:"read_only"` 상세에도 `predecessors` 가 실린다 | `backend/src/ax_workspace/modules/work/application.py:987` |
| | **목록은 `predecessors` 를 싣지 않는다** — id 배열만 | `backend/src/ax_workspace/modules/work/application.py:912-931` |
| **서버 수정** | `PATCH /api/tasks/{id}` **하나뿐.** 배열 전체 교체(생략=건드리지 않음, `null`·`[]`=전부 뗀다) | `backend/src/ax_workspace/modules/work/task_commands.py:52-67`·`110-127`; 구현 `modules/work/application.py:558-568` |
| | 거절 여섯 — `TaskPredecessorProjectRequired`(422) · `ProjectMismatch`(422) · `Self`(422) · `Duplicate`(422) · `Cycle`(422) · `TaskProjectLockedByPredecessors`(409) | `backend/src/ax_workspace/modules/work/errors.py:110-140`; 판정 `modules/work/application.py:1152-1195` |
| | 시작 게이트 — `TaskPredecessorsUnfinished`(409, `InvalidTaskTransition` 하위) 가 `open→in_progress`·`open→done` **두 문에만** 걸린다 | `backend/src/ax_workspace/modules/work/lifecycle.py:130-140`; 이유 `:111-128` |
| | ⚠ **MCP `task_update` 는 `preceding_task_ids` 를 받지 않는다** | `backend/src/ax_workspace/entrypoints/mcp.py:2015-2038` |
| | ⚠ **끝난·취소된 업무를 새로 선행으로 지정하는 것을 막는 규칙을 못 찾았다** | `be-survey-report.md:139`; 판정 `backend/src/ax_workspace/modules/work/application.py:1178-1194` |
| **화면 표시** | 업무 상세 「선행업무」 구획 — 목록 + 미완 `Badge tone="danger"` + 숨은 건수 + 막힘 문장. 조건 `(task.predecessors ?? []).length > 0` | `frontend/src/features/work/WorkModals.tsx:1749-1777` |
| | 단추 셋 비활성 — 상세 「시작」 · 상세 「완료 처리」 · 행 액션 | `frontend/src/features/work/WorkModals.tsx:1304`·`:1322`·`:2575` |
| | 프로젝트 사이드 「선행」 · 간트 의존선 | `frontend/src/features/project/ProjectTaskPanel.tsx:222` · `features/project/ProjectGantt.tsx:289-320` |
| **화면 수정** | **생성 모달의 「선행 업무」 표 하나뿐.** 프로젝트를 먼저 골라야 표가 뜬다 | `frontend/src/features/work/WorkModals.tsx:4587-4622`·`:4127-4137` |
| | **만든 뒤 더하거나 빼는 입구가 프론트 전체에 0건** — `TaskPatch` 에 없고 api.ts 에 mutation 이 없다 | `frontend/src/lib/viewModels.ts:538-545` · `fe-survey-report.md:172-173` |
| **시안이 요구하는 것** | A·B 의 `선행 업무` 칸(셈 「2 · 모두 완료」/「1 · 미완 1」) · B 의 상단 막힘 배너 · C 의 **해제 + 추가 셀렉터** | `TaskDetail.html:196-204`·`:307-314`·`:268-271`·`:370-379` |

### 2-3. 후행 — **저장도 조회도 없다**

| 칸 | 지금 | 근거 |
|---|---|---|
| **스펙** | **후행 조회 API 를 만들지 않는다**(D-07) — 「프로젝트 범위에서 **역산이 완전**하므로」 | `spec-005-projects.md:234` · `:1228` · `decision-004-projects.md:246-262` |
| | 그 근거 — 「선행은 같은 프로젝트 안에서만 성립한다 … **프로젝트 밖에 숨은 후행이 원리적으로 존재할 수 없다**」 | `spec-005-projects.md:608-610` |
| | **업무 상세에 후행을 그리라고 한 문서가 없다** — 후행이 그려지는 자리로 지정된 곳은 **프로젝트 화면 우 레일** 하나다 | `spec-survey-report.md` §3-3; 대상 계약 `spec-005-projects.md:536` |
| **서버 저장** | **전용 저장이 없다 — 있을 필요가 없다.** `task_predecessors` 한 줄이 이미 양쪽을 담고 있다(`task_id` ↔ `predecessor_task_id`) | `backend/src/ax_workspace/platform/persistence.py:1027-1045` |
| **서버 읽기** | **0건이다.** `successor` 라는 식별자·문자열이 `backend/src/ax_workspace/**/*.py` 전체에 **0회** | `be-survey-report.md:19`·`:252` |
| | 선행을 읽는 저장소 문 **넷이 전부 `task_id` 쪽으로만** 걸린다 — `predecessors_for` · `active_predecessor_ids` · `predecessor_edges` · `predecessor_task_ids` | `backend/src/ax_workspace/platform/work_tasks.py:1128-1153`·`2163-2178` |
| | `predecessor_task_id` 를 **필터 조건으로** 쓰는 문이 코드 전체에 없다 | `be-survey-report.md:258` |
| | 유일한 우회로는 프로젝트 상세다 — 주석이 설계 의도로 「**후행 배열**… 화면이 센다」를 적는다 | `backend/src/ax_workspace/modules/work/projects.py:429-431` |
| | 관계 그래프도 모른다 — 엣지 일곱에 선행·후행이 없다 | `backend/src/ax_workspace/modules/work/graph.py:145-208` |
| **서버 수정** | 후행을 직접 쓰는 명령이 **없다**(있을 자리가 아니다). 관계를 바꾸는 유일한 문은 **후행 쪽 업무의 `PATCH`** 다 | `backend/src/ax_workspace/modules/work/task_commands.py:52-56` |
| **화면 표시** | **업무 상세에 0건** — `TaskDetailDrawer` 안에 `successor`·「후행」 렌더가 없다 | `frontend/src/features/work/WorkModals.tsx:384-2175`; `fe-survey-report.md:177` |
| | 프로젝트 화면에만 둘 — 사이드 「후행」 `RelationBlock` · 간트 화살표 | `frontend/src/features/project/ProjectTaskPanel.tsx:223` · `features/project/ProjectGantt.tsx:289` |
| | 재료는 클라이언트 역산 — `successorIndex(tasks)` 가 그 프로젝트 업무 전부의 선행 배열을 뒤집는다 | `frontend/src/features/project/projectModel.ts:129-146` |
| **화면 수정** | **없다** — 역산값이라 고칠 대상 자체가 선행이다 | `fe-survey-report.md:281` |
| **시안이 요구하는 것** | A·B 의 `후행 업무` 칸 · **비공개 건수 한 줄** · C 의 **「해제」만(추가 줄 없음)** + 「🔒 비공개 1건은 여기서 해제할 수 없습니다」 | `TaskDetail.html:214-223`·`:319-322`·`:391-400` |

### 2-4. 참고 (`reference_task_ids` · `task_references`)

| 칸 | 지금 | 근거 |
|---|---|---|
| **스펙** | 관계 셋의 둘째 — 「**맥락만** 준다 · 읽을 수 있는 업무 아무거나 · **시작도 완료도 막지 않는다** · **만들기 창에 없다**(D-21), 다는 자리는 **업무 상세**」 | `spec-001-work-management.md:1059` · `:326-328` |
| | 「참고를 선행의 대체물로 쓰지 않는다」 · E-6 「참고 연결을 하위 관계의 대체물로 확정하지 않는다」 | `spec-001-work-management.md:1062` · `baseline-002-task-lifecycle-v2.md:290` |
| | ⚠ **U-7 상세 구획표에 「참고 업무」 줄이 없다** — 「업무 상세에서 단다」만 있고 어느 구획인지가 비어 있다 | `spec-001-work-management.md:351-358` vs `:328` |
| **서버 저장** | 조인테이블 `task_references` — `task_id` · `referenced_task_id`(**양쪽 index**) · `released_at/by`. 부분 unique `uq_task_reference_active` | `backend/src/ax_workspace/platform/persistence.py:1551-1578` |
| | **자기 자신 금지 CHECK 이 없다**(선행과 다르다) — application 이 답한다 | `backend/src/ax_workspace/platform/persistence.py:1560-1569` vs `:1023` |
| **서버 읽기** | 상세 `references: [{reference_id, created_by, created_at, task \| null}]` — **`access:"owner"` 상세에만** 실린다 | 조립 `backend/src/ax_workspace/modules/work/application.py:2363`; `read_only` 갈래에 없음 `:946-1000`; 타입 `modules/work/task_results.py:212-217`·`241` |
| **서버 수정** | **전용 엔드포인트 둘** — `POST /api/tasks/{id}/references` · `DELETE /api/tasks/{id}/references/{reference_id}` | `backend/src/ax_workspace/entrypoints/http.py:1681-1697`; 구현 `modules/work/application.py:2403-2437` |
| | 거절은 전부 `TaskError`(422)·`TaskNotFound`(404) — **전용 오류 클래스가 없다**(선행 여섯과 대조적) | `be-survey-report.md:176-177` |
| | 만들기 권한: `TASK_SELF_MANAGE` + **그 업무를 들고 있어야 한다**(`_holding`) | `backend/src/ax_workspace/modules/work/application.py:2406`·`2343-2349` |
| **화면 표시** | 업무 상세 「참고 업무」 구획 — 목록(상태·기한·담당) + 「볼 수 없는 업무」. 조건 `!readOnly` | `frontend/src/features/work/WorkModals.tsx:1880-1944` |
| **화면 수정** | **온전하다** — 「업무 연결」(추가)·「연결 해제」 둘 다 있다 | `frontend/src/lib/api.ts:174`·`:182` · `WorkModals.tsx:1889-1919` |
| **시안이 요구하는 것** | A·B 의 `참고 업무` 칸(**A 에 추가 단추가 없다**) · C 의 **해제 + 추가 셀렉터** | `TaskDetail.html:206-213`·`:315-318`·`:381-389` |

### 2-5. 프로젝트 소속 (`project_id`)

| 칸 | 지금 | 근거 |
|---|---|---|
| **스펙** | 업무당 **단일**. 선행이 하나라도 있으면 **필수**가 된다. 남은 선행이 있으면 **바꿀 수 없다**(409) | `spec-001-work-management.md:738`·`:867`·`:913` |
| | 상위를 옮기면 **자손 전체**가 따라가고 이동 게이트도 자손 전체에 걸린다(D-19). **부분 이동은 없다** | `spec-005-projects.md:1063-1073` |
| | ⚠ 하위 업무는 프로젝트를 **따로 못 갖는다** — 상위를 따른다 | `backend/src/ax_workspace/modules/work/application.py:526-528` |
| **서버 저장** | `tasks.project_id UUID NULL FK→projects.id`, `index=True`. **비어 있는 것이 정상** | `backend/src/ax_workspace/platform/persistence.py:939` |
| **서버 읽기** | `TaskMutationResult.project_id: str \| null` — 생성·수정·전이·목록·상세 전부 | `backend/src/ax_workspace/modules/work/application.py:2470`; 타입 `modules/work/task_results.py:79` |
| | **프로젝트 «이름」을 업무 응답이 내지 않는다** — 이름은 `GET /api/projects` 가 갖는다 | 타입 `modules/work/task_results.py:79` vs `modules/work/projects.py:360-372` |
| | 프로젝트 읽기는 「**붙어 있는가**」 하나로만 열리고, 못 읽는 프로젝트는 **없는 것처럼 404** | `baseline-004-projects.md:510-511`; 코드 `backend/src/ax_workspace/modules/work/projects.py:304-319` |
| **서버 수정** | **이미 열려 있다** — `PATCH /api/tasks/{id}` 가 `project_id` + `clear_project` 를 받는다 | `backend/src/ax_workspace/modules/work/task_commands.py:53`·`111-112`·`120-122`; 구현 `modules/work/application.py:525-550` |
| | 거절 — `TaskProjectLockedByPredecessors`(409) · 하위가 스스로 바꾸려 하면 `TaskError`(422) · 못 읽는 프로젝트 `TaskNotFound`(404) | `backend/src/ax_workspace/modules/work/application.py:526-550`·`374-380` |
| **화면 표시** | **업무 상세가 프로젝트를 한 글자도 그리지 않는다** — `TaskDetailDrawer`(`:384-2175`) 안에 `project` 렌더 **0건** | `fe-survey-report.md:103`·`:268` |
| **화면 수정** | 생성 모달의 「프로젝트」 Select 하나. `TaskPatch.project_id`·`clear_project` 가 api.ts 에 **살아 있는데 호출자가 0건** | `frontend/src/lib/api.ts:258-261` · `WorkModals.tsx:778-783` |
| **시안이 요구하는 것** | A·B 의 `프로젝트` 칸(**이름을 단추로**) · C 의 **셀렉터(「— 없음 —」 포함)** | `TaskDetail.html:180-183`·`:298-301`·`:349-356` |

### 2-6. 요청 ↔ 수락으로 생긴 업무 — **이 판이 건드리지 않는 자리**

시안의 여섯 칸에 이 관계의 자리가 없다. 사실만 남긴다.

| 칸 | 지금 | 근거 |
|---|---|---|
| **스펙** | SPEC-003 이 정본. 요청 Task 의 완료는 **요청자 확인**을 지난다 | `spec-003-task-lifecycle-v2.md:546-547`·`:577-586` |
| **서버 저장** | `tasks.source_work_request_id` + **부분 unique** `uq_tasks_source_work_request` | `backend/src/ax_workspace/platform/persistence.py:901-907`·`925` |
| **서버 읽기** | `lineage.source_work_request_id` · 상세 `origin` · 상세 `delivery` | `backend/src/ax_workspace/modules/work/application.py:2500-2508`·`2123-2145`·`985` |
| **화면 표시** | 상세 상단 `.origin-chip` 「○○가 보낸 업무」 | `frontend/src/features/work/WorkModals.tsx:1531-1548` |
| **이 판의 자리** | **없다.** 시안의 `연관 업무` 여섯 칸에 요청 관계가 없다 | `TaskDetail.html:174-225` |

---

## 지금 무엇이 깨져 있나 — 알려진 결함 다섯

### 결함 ① 상세 조회가 `predecessors` 를 버린다 → **선행 구획과 시작 게이트가 통째로 안 선다**

- 그릴 코드는 있다 — 「선행업무」 구획 (`frontend/src/features/work/WorkModals.tsx:1749-1777`)과
  단추 셋의 비활성 (`:1304`·`:1322`·`:2575`).
- 그 재료 넷(`blockingPredecessors`·`visiblePredecessors`·`hiddenPredecessors`·
  `startBlockedByPredecessors`)은 **한 자리에서 `task` prop 만 읽어 만들어진다**
  (`frontend/src/features/work/WorkModals.tsx:991-995`; 판정 `features/work/workRows.ts:113-147`).
- 그런데 **상세 조회 effect 가 다섯만 갱신한다** — `setChecklist`·`setReferences`·`setDelivery`·
  `setChildren`·`setParentTask`. `predecessors` 를 담는 state 자체가 없다
  (`frontend/src/features/work/WorkModals.tsx:574-584`).
- 그리고 **`predecessors` 는 업무 상세 응답에만 실린다** — 목록 투영은 id 배열만 낸다
  (`backend/src/ax_workspace/modules/work/application.py:912-931` vs `:987`·`2369`;
  프론트 타입 주석 `frontend/src/lib/viewModels.ts:256-257`).
- **목록에서 여는 길이 목록 투영을 그대로 넘긴다** — `openMyTask(task)` 가 `getMyWork()`/`getTasks()`
  결과 행을 그대로 `detailStack` 에 넣고 그것이 prop 으로 간다
  (`frontend/src/features/work/MyWorkPage.tsx:577-580`·`:284-285`·`:1230`).
- **같은 서랍인데 갈래마다 다르다** — 상세 안에서 다른 업무로 따라 들어가는 길(`pushDerivedTask`,
  `frontend/src/features/work/MyWorkPage.tsx:587-596`)은 `getTask(taskId)` 를 거치므로 선행이 보인다.
- 테스트는 이 갈래를 타지 않는다 — `task` prop 에 `predecessors` 를 직접 넣어 렌더한다
  (`frontend/src/features/work/Predecessors.test.tsx:64-86`).

> **서버 쪽은 서 있다.** 저장·입력·검증 다섯·시작 게이트가 전부 있다
> (`be-survey-report.md:9`). 깨진 곳은 **프론트의 배선 한 자리**다.

### 결함 ② 후행을 내주는 경로가 백엔드에 0건

`successor` 식별자 **0회**, `predecessor_task_id` 를 필터로 쓰는 문 **0건**,
`predecessor_task_id` 단독 인덱스 **없음**
(`be-survey-report.md:19`·`:258`·`:262`; 스키마 `backend/src/ax_workspace/platform/persistence.py:1014-1025`).

⚠ **인덱스를 더하는 길에 알려진 제약이 있다** — 같은 파일의 다른 자리에서
「기존 표에 인덱스를 더하면 `schema_sync` 가 못 만든다」는 이유로 인덱스를 **일부러 두지 않은**
선례가 있다 (`backend/src/ax_workspace/platform/persistence.py:1650-1653`;
`be-survey-report.md:188`). 그리고 **Alembic 도 migrations 체계도 없다** —
스키마는 `Base.metadata` 가 정본이고 `make sync-demo-schema` 가 **없는 표·컬럼만** 더한다
(`baseline-004-projects.md:525-526`).

### 결함 ③ 업무 상세가 `project_id` 를 한 글자도 그리지 않는다

`DirectTask.project_id` 가 오는데(`frontend/src/lib/viewModels.ts:242`)
`TaskDetailDrawer`(`frontend/src/features/work/WorkModals.tsx:384-2175`) 안에 `project` 렌더가
**0건**이다 — 구획도 `meta-grid` 칸도 없다 (`fe-survey-report.md:103`).
고칠 입구도 반만 있다: `TaskPatch.project_id`·`clear_project` 가 api.ts 에 살아 있는데
**그 patch 를 만드는 호출자가 0건**이다 (`frontend/src/lib/api.ts:258-261` ·
`WorkModals.tsx:778-783` 이 title·description·start_date·due_date 넷만 싣는다).

### 결함 ④ `RelationGraph` 엣지 일곱에 선행이 없다

그래프가 아는 `kind` 는 `parent_of`·`refers_to`·`produced`·`requested`·`asked_of`·`holds`·
`has_material` 일곱이다 (`frontend/src/features/graph/GraphCanvas.tsx:69-93`).
서버도 같다 — `_task_neighbors` 가 선행 엣지를 내지 않는다
(`backend/src/ax_workspace/modules/work/graph.py:145-208`).
그리고 **모르는 `kind` 는 자기 이름을 그대로 쓴다**
(`frontend/src/features/graph/RelationGraphPage.tsx:351`·`:423` 의 `?? edge.kind`) —
서버가 선행 엣지를 내기 시작하면 화면에 **`kind` 문자열이 날것으로** 뜬다.

### 결함 ⑤ 생성 모달에서 넷을 나란히 고르는데 만든 뒤 대접이 제각각이다

| 관계 | 생성 모달 | 만든 뒤 고치기 |
|---|---|---|
| 상위 업무 | Select (`WorkModals.tsx:4496-4516`) | **없다** — `TaskEditFields` 에 칸 없음 (`backend/.../task_commands.py:45-58`) |
| 프로젝트 | Select (`WorkModals.tsx:4526-4543`) | 서버는 **열려 있고** 화면 호출자가 **0건** (`frontend/src/lib/api.ts:258-261`) |
| 참고 업무 | 표 (`WorkModals.tsx:4558-4577`) | **온전하다** — 추가·해제 둘 다 (`api.ts:174`·`:182`) |
| 선행 업무 | 표 (`WorkModals.tsx:4587-4622`) | 서버는 **배열 교체가 열려 있고** 화면 입구가 **0건** (`fe-survey-report.md:172-173`) |

그리고 **생성 표면끼리도 받는 값이 갈린다** — 같은 「업무 하나 만들기」인데
`POST /api/tasks`(본인)는 넷을 다 받고, `+assignee_id` 갈래는 **선행·상위·프로젝트·시작일을 422 로 거절**하며,
`POST /api/tasks/assign` 은 선행·프로젝트 칸이 **아예 없다**
(`backend/src/ax_workspace/modules/work/creation_commands.py:168-198` ·
`modules/work/task_creation.py:112-129`).
⚠ 코드 주석은 「선행 배열은 생성 계약의 일부라 **모든 생성 표면에 함께 선다**」로 적혀 있다
(`backend/src/ax_workspace/platform/actions.py:1781`) — 실제와 어긋나 보인다
(`be-survey-report.md:688-693`).

---

## 겹쳐 읽어 드러난 것 — 시안 · 스펙 · 코드의 어긋남

**판정하지 않는다.** 양쪽을 인용만 한다. 처분은 DEC-006 과 SPEC-007 이 한다.

### ① 「후행을 만들지 않는다」 vs 시안이 후행 칸을 요구한다

- SPEC-005 — 「**후행(역방향) 조회 API** — 프로젝트 범위에서 **역산이 완전**하므로 만들지 않는다
  **(확정 — D-07)**」 (`spec-005-projects.md:234` · `decision-004-projects.md:246-262`)
- 시안 — A·B·C 세 무대 모두 `후행 업무` 칸을 그리고 범례가 「후행 — **같은 표를 반대로 읽기**」로
  적는다 (`TaskDetail.html:214-223`·`:121`)
- ⚠ **D-07 의 근거는 프로젝트 화면에 대해 세워졌다** — 「프로젝트 범위에서」가 그 전제다
  (`spec-005-projects.md:608-610`). 업무 상세는 프로젝트 범위가 아니다: 업무는
  **프로젝트 없이도 존재**하고(`backend/src/ax_workspace/platform/persistence.py:939`)
  그때 역산할 재료가 없다.

### ② 「선행은 상세에만 실린다」 vs 목록에서 여는 서랍

- 계약 — `predecessors` 는 업무 상세 응답의 칸이다
  (`backend/src/ax_workspace/modules/work/task_results.py:237-238`; 목록은 `application.py:912-931`)
- 화면 — 목록에서 여는 서랍은 **목록 투영을 그대로 prop 으로 받는다**
  (`frontend/src/features/work/MyWorkPage.tsx:577-580`·`:1230`)
- 두 사실이 겹쳐 결함 ① 이 된다. **어느 쪽을 고칠지는 정해지지 않았다** — 상세 조회를 태우느냐,
  목록에도 싣느냐.

### ③ 「참고 업무를 다는 자리는 업무 상세」인데 U-7 구획표에 그 줄이 없다

- SPEC-001 U-6-b — 「참고 업무를 다는 자리는 **업무 상세**다(U-7 **자료·연결 구획**)」
  (`spec-001-work-management.md:328`)
- SPEC-001 U-7 — 구획은 머리·내용·출처·값·자료·진행 기록 여섯이고 **「연결」 구획도
  「참고 업무」 줄도 표에 없다** (`spec-001-work-management.md:351-358`)
- 시안은 그 자리를 **`연관 업무` 덩어리의 한 칸**으로 준다 (`TaskDetail.html:206-213`)

### ④ U-7 의 구획 여섯 vs 시안의 덩어리 넷

- SPEC-001 U-7 — 「구획 순서는 **고정**이다」: 머리 → 내용 → 출처 → 값(담당자·요청자·기한·승인자·
  프로젝트·**선행업무**) → 자료 → 진행 기록 (`spec-001-work-management.md:349-358`)
- 시안 — 업무 메타 → (막힘 배너) → 업무 정보 → 연관 업무 → 자료
  (`TaskDetail.html:131-248`·`:268-271`). **「진행 기록」 구획이 시안에 없다.**
- 현행 화면에는 그 구획이 있다 — 「활동·이력」 `TaskHistorySection`
  (`frontend/src/features/work/WorkModals.tsx:182-305`, 호출 `:1953`)

### ⑤ U-14 의 「버튼 옆」 vs 시안의 상단 배너

- SPEC-001 U-14 — 「`[시작]` 은 **비활성**이고, 왜인지를 **그 옆에** 낸다 —
  "끝나지 않은 선행업무가 있습니다: {제목}"」 (`spec-001-work-management.md:489-490`);
  Case Matrix 의 표시 위치도 「**그 버튼 옆**」 (`:914`)
- 시안 B — `업무 메타` 바로 아래 **상단 배너**에 「시작할 수 없습니다 /
  **연동 규격 확인**이 끝나지 않았습니다.」 (`TaskDetail.html:268-271`)
- **문구도 다르다** — 서버가 내는 문장은 「끝나지 않은 선행업무가 있습니다: {최대 3개 제목}」
  (`backend/src/ax_workspace/modules/work/lifecycle.py:130-132`)

### ⑥ 「산출물」 vs 「결과 자료」

- 현행 화면 — 자료 두 벌이 `renderMaterials("input")`·`renderMaterials("output")` 이고
  **구획 라벨이 없다**(무라벨) (`frontend/src/features/work/WorkModals.tsx:1150-1175`·`:1951-1952`)
- 시안 — `참고 자료` | `결과 자료` (`TaskDetail.html:233`·`:243`)
- 그래프의 자료 엣지 문장은 「참고 자료·**산출물**」로 적혀 있다
  (`frontend/src/features/graph/GraphCanvas.tsx:69-78` 계열; `fe-survey-report.md:205`)

### ⑦ 시안 A 에만 「편집」 단추가 있다

`TaskDetail.html:144`(A) vs `:265`(B). **시안이 그 조건을 적지 않았다.**
현행 화면은 제목·내용·날짜를 **인라인 편집**하고 `readOnly` 면 구획이 사라진다
(`frontend/src/features/work/WorkModals.tsx:1549-1576`·`:1679-1690`·`:1804`).

### ⑧ 오류 응답에 기계용 코드가 없다

- SPEC 들은 코드명으로 계약을 적는다 — `WORK_PREDECESSORS_UNFINISHED` 등
  (`spec-001-work-management.md:908-914`)
- 실제 HTTP 본문은 **`detail=str(error)` 한 문장**이다. 코드명은 예외 클래스 docstring 에만 있다
  (`backend/src/ax_workspace/entrypoints/http.py:551`·`564`·`576`;
  `backend/src/ax_workspace/modules/work/errors.py:110-161`)
- 같은 파일 안에서 회의실 예약은 `detail={"code":…,"message":…}` 구조를 쓴다
  (`backend/src/ax_workspace/entrypoints/http.py:511-527`) — **두 모양이 섞여 있다**
  (`be-survey-report.md:676`)
- 그리고 `TaskPredecessorsUnfinished.blocking`(막는 선행 이름 튜플)이 **본문에 실리지 않는다**
  (`backend/src/ax_workspace/modules/work/errors.py:148-161` vs `entrypoints/http.py:551`)

### ⑨ 이력에 관계 변경이 안 남는다

`TaskVersionRecord.snapshot` 이 담는 것에 `preceding_task_ids`·`parent_task_id`·`project_id` 가
**없다** (`backend/src/ax_workspace/platform/work_tasks.py:1054-1077`).
diff 대상도 여섯 필드 + 컬렉션 둘뿐이다
(`backend/src/ax_workspace/modules/work/application.py:2580`·`2604-2606`).
프론트의 `HISTORY_FIELD_LABEL` 도 관계 필드를 모른다 — 뜨면 **필드 이름이 날것으로** 나온다
(`frontend/src/features/work/WorkModals.tsx:152-164`·`:277-290`).
다만 활동 로그에는 바뀐 키 이름이 남는다
(`backend/src/ax_workspace/modules/work/application.py:589-592`).

### ⑩ EU-8 이 가리키는 자리와 사용자가 닫으려는 자리가 다르다

- SPEC-003 §5 — 「판정은 **생성 시점**에 한다. **담당이 나중에 바뀌어** 규칙에 어긋나는 모양이
  되어도 기존 구조를 깨지 않는다. **담당 변경 후** 기존 하위 구조를 어떻게 처리할지는
  **(미정 EU-8)**」 (`spec-003-task-lifecycle-v2.md:937-939`)
- 사용자 확정 2026-09-28 — 「**상위를 옮길 때** 그 업무의 하위가 V-8 을 어기게 되면 거절한다」
- **두 갈래다.** ①**담당 변경**이 어긋남을 만드는 갈래 ②**상위 이동**이 어긋남을 만드는 갈래.
  EU-8 의 본문은 ①을 적고 있고 사용자 확정은 ②를 닫는다.
  **이 문서는 그 차이를 사실로만 둔다** — 처분은 DEC-006 이 한다.

### ⑪ 낱말이 갈린다

| 낱말 | 갈래 | 근거 |
|---|---|---|
| `blocking` | **셋** — 선행(시작 막음) · 하위(완료 막음) · 캘린더 시간 블록 | `fe-survey-report.md:43-50` |
| 선행의 한국어 | 「선행업무」(업무 화면·붙여 씀) vs 「선행」(프로젝트 화면) | `frontend/src/lib/labels.ts:310-320` vs `:1014` |
| 후행의 한국어 | 「후행」 — **프로젝트 화면에만** 있다 | `frontend/src/lib/labels.ts:1015` |
| 같은 사실의 두 이름 | `predecessors`(요약 배열) vs `preceding_task_ids`(id 배열) | `frontend/src/lib/viewModels.ts:255`·`:263`·`:121` |

⚠ **서버 필드 `derived.blocking_children` 과 `child_progress.blocking` 은 「하위」 축이다** —
선행에 해당하는 서버 파생 필드는 **없다**
(`backend/src/ax_workspace/modules/work/task_results.py:25-31`·`:44`·`:188`;
`be-survey-report.md:276`). 코드가 두 축을 **일부러** 가른다
(`backend/src/ax_workspace/modules/work/errors.py:150-156`).

---

## 이 문서가 답하지 않은 것

**추측으로 메우지 않는다.** DEC-006 과 SPEC-007 이 받는다.

1. **후행 응답 필드의 이름과 모양** — `successor` 라는 이름이 코드에 0회이므로 선례가 없다
   (`be-survey-report.md:19`)
2. **`predecessor_task_id` 인덱스가 실제로 어떻게 설치되나** — Alembic 이 없고
   `schema_sync` 가 기존 표에 인덱스를 못 더한다는 선례가 있다
   (`baseline-004-projects.md:525-526` · `backend/src/ax_workspace/platform/persistence.py:1650-1653`)
3. **후행 해제를 누가 부를 수 있나** — 그 행은 후행 쪽 업무의 것이고, 기존 선행 편집 권한은
   「그 업무의 값을 고칠 수 있는 사람」이다 (`spec-001-work-management.md:1134`).
   **A 의 화면에서 A 의 담당자가 B 의 행을 닫는 것**에 대한 계약이 없다
4. **프로젝트 «이름»을 업무 상세가 어디서 얻나** — 업무 응답은 `project_id` 만 낸다
   (`backend/src/ax_workspace/modules/work/task_results.py:79`)
5. **「연결 편집」의 저장이 여러 업무를 건드릴 때의 원자성** — 기존 계약에 다중 업무 원자 명령이 없다
6. **「편집」 단추가 서는 조건** — 시안이 A 에만 그렸고 이유를 적지 않았다 (§어긋남 ⑦)
7. **「진행 기록/활동·이력」 구획이 시안에 없는 것이 삭제인가 생략인가** (§어긋남 ④)

### 그 뒤 — 일곱이 어떻게 처분됐나 *(2026-09-28 증보)*

**이 절을 다시 쓰지 않는다** — 위 일곱은 **이 문서가 답하지 않았다는 사실 그대로**이고,
아래는 **DEC-006 과 SPEC-007 이 그것을 어떻게 받았는지**의 포인터다.

| # | 처분 | 어디 |
|---|---|---|
| 1 | `successors`(읽을 수 있는 것만) · `hidden_successor_count` 로 **정해졌다** | SPEC-007 §4 |
| 2 | **스펙은 「인덱스가 필요하다」까지만** 쓰고 설치 방법은 **backend 워커**가 답한다 | SPEC-007 §7.1 OQ-703 |
| 3 | **A 담당자에게도 «연다»** — A 쪽 또는 B 쪽 편집 권한 | SPEC-007 §7.1 OQ-708 · §4 |
| 4 | **새 필드를 만들지 않고** 프로젝트 목록에서 맞춘다. 못 읽으면 **「비공개 프로젝트」** | SPEC-007 §2.4.4 |
| 5 | **칸마다 따로 저장한다** — 거절된 칸만 되돌린다 | SPEC-007 §7.1 OQ-704 · §2.8.3 |
| 6 | **A(기본)에만** 선다 | SPEC-007 §7.1 OQ-702 · §2.2 |
| 7 | **생략이다 — 삭제가 아니다.** 덩어리 **`이력`** 이 그 자리를 받는다 | SPEC-007 §7.1 OQ-701 · §2.1 |

**그리고 §어긋남 ①·④ 가 대체로 처분됐다** — 어긋남 ①(후행 조회를 만들지 않는다)과
④(U-7 구획 순서 고정)는 **SPEC-007 이 대체한다.** 전수 목록은 **SPEC-007 §7.2** 가 갖는다
(여섯 줄). **이 문서는 관측만 남기고 처분을 갖지 않는다.**

---

## 조사 한계

- **이 문서는 코드를 직접 읽지 않았다.** 모든 코드 사실은 조사 리포트 둘의 관측을 **원본
  파일:줄로 되돌려** 적은 것이다. 리포트 둘은 테스트를 돌리지 않았고 브라우저로 확인하지 않았다
  (`be-survey-report.md:707` · `fe-survey-report.md:309`).
- **`backend/tests/`·`frontend/**/*.test.*` 를 전수조사하지 않았다** — 테스트가 계약을 더 좁게
  고정하고 있는지는 확인되지 않았다 (`be-survey-report.md:708`).
- **런타임 응답을 확인하지 않았다.** 응답 shape 은 TypedDict 정의와 조립 코드를 읽어 맞춘 것이다.
- **시안의 CSS 계산 결과를 브라우저로 보지 않았다.** `.scroll` 105px = 3행이라는 것은
  시안 주석의 산식(`TaskDetail.html:49`)을 그대로 인용한 것이다.
- **`_archive/` 를 보지 않았다.**
- 회사 원문(mediness `products/sc-ax/`)은 이 판에서 보지 않았다 — 앞 조사가
  「Subtask 는 한 단계까지만 허용한다」(`spec-001-work-management.md` 회사판 §3.4)와
  우리 V-6 의 어긋남을 이미 기록했고, **업무 상세 재설계가 그 자리를 건드리지 않는다.**
