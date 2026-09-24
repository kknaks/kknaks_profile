# [backend] 업무·프로젝트 도메인 read-only 조사 — D-1~D-9 대조

- **대상**: 워크트리 `/Users/kknaks/orca/workspaces/Strong_hajin/strong-hajin-projects`, 브랜치 `kknaksss/strong-hajin-projects` (HEAD `e46ce39`, 2026-09-21)
- **질문지**: `design-read-projects.md` §8 의 D-1~D-9
- **SoT**: **지금 돌아가는 코드.** 문서(SPEC/WP)는 배경으로만 읽었고, 코드와 어긋난 곳은 §5 에 모았다.
- **변경 없음.** 코드·설정·테스트 어느 것도 고치지 않았다. 서버·DB 도 띄우지 않았다 (정적 읽기만).
- 모든 경로는 워크트리 루트 기준 상대경로다.

## 0. 한 줄 결론

**9개 중 7개는 이미 있고, 1개(D-3 진행률)는 아예 없고, 1개(D-7 상태)는 개수가 다르다.**
그리고 **간트가 필요한 것의 절반은 `GET /api/projects/{project_id}` 한 방에 이미 나온다** —
`tasks[]` 가 `state`·`start_date`·`due_date`·`parent_task_id`·`preceding_task_ids` 를 함께 낸다
(`backend/src/ax_workspace/modules/work/projects.py:240-251`). 이 배열은 「간트 연결선의 유일한 원천」이라고
계약으로 못 박혀 있고 계약 테스트가 지킨다 (`backend/tests/contract/test_task_predecessors.py:448-461`).

판정 집계: **있다 6 · 다르다 2 · 없다 1**

| # | 판정 | 한 줄 |
|---|---|---|
| D-1 | 있다 | `tasks.project_id` (nullable, indexed) |
| D-2 | 있다(주의) | `tasks.start_date`·`due_date` — **둘 다 nullable, 역전도 실재**. 정규화 함수 `task_span()` 이 이미 있다 |
| D-3 | **없다** | 진행률 % 가 **저장에도 응답에도 없다.** 대체 재료는 `checklist_progress`·`child_progress` 둘 |
| D-4 | 있다 | `task_predecessors` 별도 표. **단방향 조회만** 있다(후행 조회 없음). 순환 방지는 application |
| D-5 | **다르다** | `tasks.parent_task_id` 자기참조 — **저장 깊이 제한 없음**. 시안은 1단계만 |
| D-6 | 있다 | `task_checklist_items` (text·done·position·state) |
| D-7 | **다르다** | 내부 **6종**, 외부 투영 **5종**. 이름이 시안과 다르다(`not-started`→`open`, `progress`→`in_progress`) |
| D-8 | 있다(부분) | 담당=`assignee`, 요청자=`origin.actor`(role `"요청자"`). **「분류」는 필드가 아니라 엔드포인트 축** |
| D-9 | 있다 | `projects` 는 **독립 엔티티**. `GET /api/projects` 목록 API 있음 |

---

## 1. D-1 ~ D-9 판정

### D-1 — 업무가 어느 프로젝트에 속하는가

```
D-1 | 판정: 있다
    | 우리 이름·모양: tasks.project_id  (UUID, nullable, FK → projects.id, index=True)
    |                 work_requests.project_id 도 따로 있다 (요청이 수락되며 업무로 물려준다)
    |                 응답 필드명: project_id (TaskMutationResult 이하 전부)
    | 근거:
    |   backend/src/ax_workspace/platform/persistence.py:939   tasks.project_id
    |   backend/src/ax_workspace/platform/persistence.py:1653  work_requests.project_id (인덱스 없음 — 주석 1651-1652 가 이유를 적는다)
    |   backend/src/ax_workspace/modules/work/task_results.py:79  응답 필드 project_id
    |   backend/src/ax_workspace/platform/work_tasks.py:1091-1098  tasks_in_projects()
    |   backend/src/ax_workspace/platform/projects.py:204-209      tasks_in()
    | 시안과의 차이: 없음 — 시안 가정 `tasks.project_id` 와 이름까지 같다.
    |   단 **비어 있는 것이 정상**이라고 주석이 명시한다(persistence.py:938 「프로젝트 없이 하는 일이
    |   조직에는 더 많다」). 프로젝트 없는 업무가 다수라는 전제로 화면이 서야 한다.
```

부가 사실 — `project_id` 는 **하위 업무에 전파된다**: 상위가 프로젝트에 붙으면 하위도 같은 프로젝트로
읽힌다 (`backend/tests/contract/test_projects.py:316` 이 이를 계약으로 잠근다).

---

### D-2 — 업무의 시작일·종료일

```
D-2 | 판정: 있다 (단, 시안이 가정한 「정수 일자」와 성질이 다르다)
    | 우리 이름·모양: tasks.start_date : Date | None   (계획 시작일)
    |                 tasks.due_date   : Date | None   (기한)
    |                 응답 필드명: start_date · due_date (ISO 날짜 문자열 또는 null)
    |                 별도로 tasks.started_at : datetime | None = **실제** 시작 시각 (계획일과 다른 사실)
    | 근거:
    |   backend/src/ax_workspace/platform/persistence.py:918-919   start_date · due_date
    |   backend/src/ax_workspace/platform/persistence.py:947-949   started_at (주석이 start_date 와 다름을 명시)
    |   backend/src/ax_workspace/modules/work/task_results.py:74-75  응답 필드
    |   backend/src/ax_workspace/modules/work/projects.py:245-246    프로젝트 상세 tasks[] 에도 실린다
    |   backend/src/ax_workspace/modules/work/schedule.py:40-62      task_span() — 기간 정규화
    | 시안과의 차이:
    |   (a) **둘 다 null 일 수 있고, 한쪽만 있을 수도 있다.** 시안은 from/to 가 항상 있다고 가정한다.
    |   (b) **start_date > due_date 인 역전 기간이 실재한다** — 시작 전이와 조건 변경 제안 동의가
    |       검증을 지나지 않고 날짜를 넣기 때문이다 (schedule.py:7-11 이 그렇게 적는다).
    |   (c) 그 네 경우를 한 함수가 이미 정규화한다 — task_span(start, due):
    |         둘 다 있고 순서 맞음 → [start, due]
    |         한쪽만 있음        → 그 날 **하루**
    |         둘 다 없음        → None (기간 없음)
    |         역전             → [min, max]
    |       (schedule.py:40-62). 캘린더 응답은 이 결과를 span_from·span_to 로 **서버가 이미 내보낸다**
    |       (task_results.py:371-373, application.py:794-795) — 다만 **`/api/calendar` 에만** 실리고
    |       프로젝트 상세 tasks[] 에는 실리지 않는다.
```

---

### D-3 — 업무의 진행률 %  ← **가장 큰 차이**

```
D-3 | 판정: 없다
    | 우리 이름·모양: **없다.** 저장 컬럼도, 파생 계산도, 응답 필드도 없다.
    | 근거 (부재의 근거 — 이렇게 찾았다):
    |   grep -rn "percent|progress_rate|진행률|completion_rate|progress_pct" backend/src/  → 0건
    |   tasks 테이블 전 컬럼 열거: persistence.py:910-958 — progress 계열 컬럼 없음
    |   grep -rn "progress" backend/src/ax_workspace/modules/work/ (in_progress 제외) → 아래가 전부:
    |     task_results.py:194  TaskListEntry.checklist_progress
    |     task_results.py:234  TaskDetailResult.child_progress
    |     task_results.py:240  TaskDetailResult.checklist_progress
    |     task_results.py:306  TaskSubtasksResult.progress
    |     task_results.py:312  TaskChecklistResult.progress
    |     application.py:2234  add_progress_note()  ← 텍스트 메모다. 숫자가 아니다
    |   MCP 도구 `task_progress_batch` 가 있으나 **% 가 아니다** — 상태 전이·체크리스트 조작을
    |   한 번에 사람이 확인하는 배치다 (entrypoints/mcp.py:1074-1082, 1957-1959). 이름만 겹친다.
    | 시안과의 차이: 시안은 `tasks.progress` 를 5칸 요약 스트립의 「전체 진행률」, 간트 바 안의 fill·%,
    |   우 레일 머리의 미터, 하위 카드의 「N%」 **네 자리**에서 쓴다. 우리에겐 그 값이 하나도 없다.
```

**대체 계산에 쓸 수 있는 재료 (있는 것만 나열 — 설계하지 않는다)**

| 재료 | 모양 | 어디서 나오나 |
|---|---|---|
| `checklist_progress` | `{done: int, total: int}` | `TaskListEntry`(task_results.py:194) · `TaskDetailResult`(240) · `TaskChecklistResult.progress`(312). 계산은 `checklist_progress_for()` (application.py:125 포트, 895·904·913 사용) |
| `child_progress` | `{done, blocking, cancelled, total}` | `TaskDetailResult`(task_results.py:234) · `TaskSubtasksResult.progress`(306) · `GET /api/tasks/{id}/children`. 계산은 application.py:1361 |
| `state` 자체 | `done`/`cancelled` 이면 종결 | 어디서나 |
| `derived.overdue_days` | `int | None` — 기한 초과 일수, **끝난 일에는 null** | task_results.py:47, 계산 application.py:2521-2529 |
| `started_at` / `completed_at` / `reopened_at` | datetime | persistence.py:949·952·955 |
| `task_schedules` | 업무 하루치 시간 칸 (배정된 날·시각) | persistence.py:1068-1094 |

**주의**: 이 중 **`checklist_progress`·`child_progress` 는 프로젝트 상세(`GET /api/projects/{id}`)의
`tasks[]` 에 실리지 않는다** — `ProjectTaskView` 는 6개 필드뿐이다 (project_results.py:28-37).
그리고 문서 쪽 반대 신호가 하나 있다: SPEC-001 §「기한 경과일」이 **「진행률은 쓰지 않는다」**고
명시적으로 적는다 (`20-spec/spec-001-work-management.md:200`). §5-1 참조.

---

### D-4 — 업무 간 선행 → 후행

```
D-4 | 판정: 있다
    | 우리 이름·모양: **별도 표** task_predecessors (컬럼 아님)
    |   id · task_id(후행 — 이 업무의 **시작**이 막힌다) · predecessor_task_id(먼저 끝나야 하는 업무)
    |   · position(고른 순서) · created_by · created_at · released_at · released_by
    |   응답 필드명:
    |     preceding_task_ids : list[str]        (목록·상세·프로젝트 상세 전부)
    |     predecessors       : list[{task_id, title|null, state|null}]  (상세에만; 위 배열과 **같은 순서·같은 길이**)
    | 근거:
    |   persistence.py:995-1040  TaskPredecessorRecord
    |     :1015-1022  부분 unique 인덱스 uq_task_predecessors_active (released_at IS NULL 일 때만)
    |     :1023       CHECK ck_task_predecessors_not_self (자기참조 금지 — DB 가 답한다)
    |     :1024       ix_task_predecessors_task_id  ← **후행 방향만 인덱스가 있다**
    |     :1035       position — 화면이 고른 차례와 조회 차례를 같게 만드는 열
    |     :1039       released_at — **행을 지우지 않고 닫는다**
    |   task_results.py:93      preceding_task_ids
    |   task_results.py:111-121 TaskPredecessorView (읽을 수 없으면 title·state 가 null, 자리만 남는다)
    |   project_results.py:35-37  「간트 연결선의 유일한 원천」이라고 주석이 적는다
    |
    | ▶ 양방향 조회: **아니다 — 단방향만 있다.**
    |   platform/work_tasks.py:1102-1119  predecessors_for(task_ids) -> {task_id: [predecessor_ids]}
    |     → WHERE task_predecessors.task_id IN (...)  = **후행으로 묻고 선행을 받는다**
    |   platform/work_tasks.py:1122-1123  active_predecessor_ids(task_id)  — 위의 1건짜리
    |   platform/work_tasks.py:1125-1127  predecessor_edges(task_ids) — 순환 검사용. 같은 질의의 별명
    |   **「이 업무를 선행으로 갖는 업무들」(후행 조회)은 저장소에도 application 에도 없다.**
    |   grep -rn "successor|후행" backend/src/ → 도메인 주석 3곳뿐, 질의 0건.
    |   단 `predecessors_for(전체 task_ids)` 가 프로젝트 전체를 한 번에 내므로 **프로젝트 화면 범위
    |   안에서는 역방향을 클라이언트가 뒤집어 만들 수 있다** (projects.py:227-231 이 이미 그 형태다).
    |
    | ▶ 순환 방지: **있다 — application 이 답한다. DB 는 못 한다.**
    |   application.py:1169-1187  _require_no_predecessor_cycle() — 활성 변을 BFS 로 걷는다.
    |     「본 것을 다시 보지 않는다」 — 원장이 이미 어긋나 고리가 있어도 무한히 걷지 않는다.
    |   검사와 저장이 **같은 transaction** 안이다 (persistence.py:1009-1010 주석 · application.py:553)
    |
    | ▶ 거절 다섯 갈래가 서로 다른 오류다 (application.py:1116-1158, 순서가 계약):
    |     자기 자신 → TaskPredecessorSelf
    |     중복      → TaskPredecessorDuplicate
    |     프로젝트 없음     → TaskPredecessorProjectRequired
    |     프로젝트 불일치   → TaskPredecessorProjectMismatch
    |     순환      → TaskPredecessorCycle
    |   ★ **선행은 같은 프로젝트 안에서만 선다** (application.py:1139-1141, 1154-1157).
    |     프로젝트 없는 업무는 선행을 가질 수 없다 — 이 화면의 전제와 정확히 맞는다.
    |
    | ▶ 편집은 **전체 교체**다: replace_predecessors() (work_tasks.py:1129-). 빠진 것은 released_at
    |   으로 닫고 새 것만 더한다. 이미 활성인 것은 건드리지 않는다.
    |
    | ▶ 게이트: 끝나지 않은 선행이 있으면 `open → in_progress` 와 `open → done` **두 문만** 막는다
    |   (lifecycle.py:130-141). 취소된 선행은 막지 않는다. 오류는 TaskPredecessorsUnfinished → HTTP 409.
    |
    | 시안과의 차이: 시안 가정 `task_dependencies` → 우리 이름은 `task_predecessors`.
    |   **후행 조회 API 가 없다**는 것과 **선행은 같은 프로젝트 안에서만 성립한다**는 것 둘이 다르다.
    |   시안 우 레일 §6-2 「관계」 블록이 선행/후행을 **각각 건수 + 목록**으로 그리는데,
    |   후행 쪽은 서버가 직접 답하는 경로가 없다.
```

---

### D-5 — 상위–하위 업무

```
D-5 | 판정: 다르다
    | 우리 이름·모양: tasks.parent_task_id (UUID | None, FK → tasks.id **자기참조**, index=True)
    |                 응답: TaskDetailResult.parent {task_id,title,state} · children[] (TaskSummaryView)
    |                       · child_progress {done, blocking, cancelled, total}
    |                       프로젝트 상세 tasks[] 에는 parent_task_id 만 실린다
    | 근거:
    |   persistence.py:937  parent_task_id
    |   task_results.py:199-210  TaskParentView · TaskSummaryView
    |   task_results.py:232-234  TaskDetailResult.parent · children · child_progress
    |   project_results.py:34    ProjectTaskView.parent_task_id
    |   entrypoints/http.py:1798-1810  GET /api/tasks/{task_id}/children
    |
    | ▶ 몇 단계까지 허용되나: **제한이 없다.**
    |   application.py:375-408 parent_for(), 특히 :385-387 —
    |     「**저장 깊이에 제한이 없다** (정책 V-6). 예전에는 「하위 아래에 하위를 둘 수 없다」로 한 단계에서
    |      끊었고 ... 화면이 두 단계만 보이는 것은 **표시**의 일이고 저장과 무관하다 (정책 L-11).」
    |   대신 걸리는 것 셋:
    |     (a) 자기 자신·자기 조상을 부모로 두면 TaskParentCycle (application.py:401-405)
    |     (b) 이미 끝난(done/cancelled) 업무에는 하위를 못 붙인다 → TaskParentClosed (:406-407)
    |     (c) **중심 업무 판정** — 같은 사람의 직접 작업을 무한히 겹치는 것만 막는다
    |         (_require_may_hold_children, application.py:408)
    |   그리고 조회 표면은 **직속 하위만** 낸다 — GET /api/tasks/{id}/children 주석(http.py:1803):
    |     「**직속 하위만** 낸다 (SPEC-003 §4 · 정책 L-11). 저장 깊이와 무관하다.」
    |
    | 시안과의 차이: **시안은 1단계(상위 + 하위)만 그린다. 우리 저장은 무제한이다.**
    |   화면이 1단계만 그리는 것 자체는 정책 L-11 이 이미 허용한다(「표시의 일」).
    |   다만 **3단계 깊이의 데이터가 실제로 들어올 수 있다** — 간트의 twisty 가 1단계만 펼치면
    |   손자 업무는 어느 행에도 안 보인다. 프로젝트 상세 tasks[] 는 **깊이와 무관하게 평평한 배열**로
    |   프로젝트의 업무 전부를 내므로(projects.py:224 tasks_in), 손자도 그 배열에는 들어 있다.
    |   ⚠ 저장소 안에 **서로 어긋나는 주석이 남아 있다** — persistence.py:935-936 은 여전히
    |     「One level only for now: a child never becomes a parent」라고 적는다. §5-2 참조.
```

---

### D-6 — 업무 체크리스트 (텍스트 + done)

```
D-6 | 판정: 있다
    | 우리 이름·모양: **별도 표** task_checklist_items
    |   id · task_id · text(String 300) · position(int) · done(bool) · state("active"|"archived")
    |   · version(자기 회차) · created_by · completed_by · completed_at · archived_by · archived_at
    |   응답 필드명: ChecklistItemView {item_id, text, position, done, state, version,
    |                                   created_by, completed_by, completed_at}
    |               집계: checklist_progress {done: int, total: int}
    | 근거:
    |   persistence.py:1097-1118  TaskChecklistItemRecord (:1101 index ix_task_checklist_items_task_position)
    |   task_results.py:123-133   ChecklistItemView
    |   task_results.py:175-178   TaskProgressView {done, total}
    |   task_results.py:239-240   TaskDetailResult.checklist · checklist_progress (둘 다 NotRequired)
    |   task_results.py:194       TaskListEntry.checklist_progress (목록은 **건수만**, 항목은 싣지 않는다)
    |   application.py:2319       checklist_progress 계산
    |   http.py:2133/2142/2153/2164  POST·PATCH·POST order·DELETE  /api/tasks/{id}/checklist
    | 시안과의 차이: 시안 가정 `task_checklists` → 우리 이름은 `task_checklist_items`. 내용은 같다.
    |   더 있는 것: position(순서 조작 API 있음) · state archived(지우지 않고 목록에서 뺀다) ·
    |   항목마다 자기 version(두 사람이 두 항목을 동시에 고쳐도 충돌하지 않는다).
    |   ⚠ `checklist` 는 **TaskDetailResult 에서 NotRequired** 다 — read_only 접근(access='read_only')
    |     에는 실리지 않는다 (application.py:920-930 get(): owner 경로만 _with_checklist(:2314) 를 지난다).
    |   ⚠ 프로젝트 상세 tasks[] 에는 체크리스트도 그 집계도 **없다**.
```

---

### D-7 — 상태 5종  ← **두 번째로 큰 차이**

```
D-7 | 판정: 다르다 (내부 6종 / 외부 5종, 이름 전부 다름)
    | 우리 이름·모양: modules/work/lifecycle.py 의 `class TaskState(StrEnum)` — **코드에서 그대로 복사**:
    |
    |     OPEN                  = "open"
    |     IN_PROGRESS           = "in_progress"
    |     BLOCKED               = "blocked"
    |     COMPLETION_SUBMITTED  = "completion_submitted"
    |     DONE                  = "done"
    |     CANCELLED             = "cancelled"
    |
    |   저장은 tasks.state : String(40), NOT NULL (persistence.py:915)
    |   프로젝트 state 는 **다른 enum** 이다: PROJECT_STATES = ("active", "closed")
    |
    | 근거:
    |   backend/src/ax_workspace/modules/work/lifecycle.py:20-26   TaskState 6값
    |   backend/src/ax_workspace/platform/persistence.py:915       tasks.state
    |   backend/src/ax_workspace/modules/datasets/schema.py:54     PROJECT_STATES = ("active", "closed")
    |
    | ▶ **밖으로 나가는 값은 5종이다.** _external_state() 가 completion_submitted 를 done 으로 접는다:
    |   backend/src/ax_workspace/modules/work/application.py:2495-2506
    |     「밖으로 나가는 수행 상태는 **넷뿐이다** — open · in_progress · done · cancelled.
    |      ... `blocked` 도 계약에 없지만 이 work 는 그 값을 **발행하지도 없애지도 않는다**(M-6) —
    |      들어오는 그대로 낸다.」
    |   즉 **주석은 4종이라 말하지만 blocked 가 그대로 통과하므로 실제 외부 값은 5종**이다:
    |     open · in_progress · blocked · done · cancelled
    |   completion_submitted 은 **state="done" + derived.approval="awaiting_review"** 로 말한다
    |   (application.py:1432 · task_results.py:42 · 365-367).
    |
    | ▶ 전이 규칙: lifecycle.py:93-104 의 `_ALLOWED_TRANSITIONS` — **코드에서 그대로 복사**:
    |     OPEN                 → {IN_PROGRESS, DONE, CANCELLED}
    |     IN_PROGRESS          → {BLOCKED, DONE, CANCELLED}
    |     BLOCKED              → {IN_PROGRESS, CANCELLED}
    |     COMPLETION_SUBMITTED → {CANCELLED}
    |     DONE                 → {IN_PROGRESS}          ← 재개(reopen)
    |   판정 함수는 lifecycle.py:107-184 `transition_task()` 하나뿐이고, 여기 모든 게이트가 모인다:
    |     선행 미완(:130-141, 409) → 요청자 확인 필요(:142-143, 422) → 하위 미완(:144-149, 409)
    |     → 회차 불일치(:150-151) → 전이 불가(:152-153) → blocked 사유 필수(:154-155)
    |     → cancelled 사유 필수(:156-161)
    |   부수효과 두 개: open→in_progress 이고 start_date 가 비었으면 **오늘로 채운다**(:166-172),
    |   blocked 가 아니면 block_reason 을 **비운다**(:173).
    |
    | ▶ 명령 표면: POST /api/tasks/{id}/start · block · resume · complete · cancel
    |   (http.py:2501·2510·2514·2518·2522) + POST /api/tasks/{id}/reopen (http.py:1823)
    |
    | 시안과의 차이:
    |   | 시안 status  | 우리 값               | 비고 |
    |   |---|---|---|
    |   | not-started  | open                  | 이름만 다름 |
    |   | progress     | in_progress           | 이름만 다름 |
    |   | blocked      | blocked               | 같다. 단 **block_reason 이 필수**다 (lifecycle.py:154-155) |
    |   | done         | done                  | 같다. 단 **승인 대기인 done 이 섞여 있다** — derived.approval 로 갈라야 한다 |
    |   | cancelled    | cancelled             | 같다. 단 **cancel 에는 사유가 필수**고 cancel_reason 4종이 따로 있다 |
    |   | (없음)       | completion_submitted  | **시안에 자리가 없다.** 외부로는 done 으로 접혀 나간다 |
    |   추가: cancel_reason 4종 — `direct` · `request_rejected` · `request_withdrawn` ·
    |         `cancellation_agreed` (persistence.py:944-946).
    |   문서 쪽 확정: SPEC-004 가 「백엔드 TaskState 가 정본. 시안 5종은 폐기」를 사용자 지시 D4 로
    |   이미 못 박았다 (20-spec/spec-004-calendar-scheduling.md:1173).
```

---

### D-8 — 담당자 · 요청자 · 분류

```
D-8 | 판정: 있다 (담당·요청자는 있다. **「분류」는 필드가 아니다**)
    |
    | ▶ 담당자: **tasks 에 열로 없다.** 별도 표 task_assignments 의 **활성 행**이 답한다.
    |   persistence.py:911-913  「The one actor relationship a Task owns: who created it.
    |                            Who sent the work is on the WorkRequest, and who holds it now is on
    |                            the active TaskAssignment; neither is copied here.」
    |   persistence.py:1752     task_assignments 표
    |   응답: TaskMutationResult.assignment : {assignment_id, kind, status, assigned_by, accepted_at}
    |         (task_results.py:7-12, 88)
    |         TaskListEntry.assignee / TaskDetailResult.assignee : {member_id, display_name}
    |         (task_results.py:157-159, 196, 231)
    |   투영 규칙: application.py:2532-2551 _assignment_view() — status=="active" 를 **먼저** 찾고,
    |   없으면(수락 대기·첫 지정) 기다리는 행을 낸다. 담당 교체 제안 중에는 active·pending 이 공존한다.
    |   derived.assignment : null | "awaiting_acceptance" | "awaiting_handover" (application.py:2509-2519)
    |
    | ▶ 요청자: work_requests.requester_id (String(100), NOT NULL, **FK 없음** — 사람 아닌 행위자가 설 수 있어서)
    |   persistence.py:1641
    |   응답은 열 그대로가 아니라 **origin 묶음**이다 — TaskOriginView (task_results.py:168-172):
    |     { kind, actor_role, actor: {member_id, display_name} | null, source: {type,id,title} | null }
    |   계산: application.py:2086-2127 _origin_projection(). kind 4종(코드에서 복사):
    |     "work_request"      actor_role="요청자"  actor=requester        source=work_request
    |     "direct_assignment" actor_role="배정자"  actor=assigned_by      source=null
    |     "self_created"      actor_role=null      actor=null             source=action_item | null
    |     (actor 도 source 도 없으면 **origin 자체를 싣지 않는다** — 없는 역할을 지어내지 않는다)
    |   ⚠ source 는 **그 요청을 읽을 수 있는 사람에게만** 실린다 (application.py:2129-2141).
    |     actor 라벨은 남고 source 만 빠진다.
    |
    | ▶ 분류(내 업무 / 보낸 업무 / 완료): **그런 필드가 없다. 엔드포인트가 축이다.**
    |   grep -rn "보낸 업무|내 업무" backend/src/ → 응답 필드 0건, 주석·프롬프트만.
    |   실제로 세 개를 가르는 것:
    |     「내 업무」   GET /api/my-work            = 활성 담당으로 지금 들고 있는 것만
    |                   application.py:802-809 my_work() — 「요청 관계로 읽는 업무는 여기 서지 않는다」
    |     「보낸 업무」 GET /api/work-requests (http.py:2012) + GET /api/task-assignments/sent (http.py:1496)
    |                   ★ **두 표면으로 갈라져 있다** — 요청과 직접 배정이 다른 원장이다
    |     「완료」     같은 목록에 include_closed=true
    |                   (http.py:679-683 my_work · http.py:1975-1983 list_tasks)
    |   그리고 「읽을 수 있는 전부」는 또 다른 함수다: readable_tasks() (application.py:810-822,
    |   include_organization+include_requested+include_cc). **이 함수는 HTTP 로 열려 있지 않다** —
    |   자료 검색·그래프·권한 판정이 내부에서 쓴다.
    |
    | 시안과의 차이:
    |   (a) 담당자가 **업무의 열이 아니라 배정 원장의 활성 행**이다. 담당 없는 업무가 정상으로 존재한다
    |       (프로젝트 계획만 올린 업무 — POST /api/projects/{id}/tasks 는 「사람은 아직 정하지 않는다」,
    |        http.py:1420-1426).
    |   (b) 요청자는 **업무가 아니라 요청이 갖고**, 응답에는 origin 묶음으로 나온다.
    |   (c) 「분류」는 값이 아니라 **어느 엔드포인트를 불렀는가**다. 프로젝트 화면이 프로젝트 하나를
    |       스코프로 잡으면 그 축 자체가 성립하지 않는다 — 프로젝트 상세는 담당 무관하게 전부 낸다.
    |   (d) **프로젝트 상세 tasks[] 에는 담당자도 origin 도 없다** (project_results.py:28-37).
```

---

### D-9 — 프로젝트 목록(선택지)

```
D-9 | 판정: 있다 — 프로젝트는 **독립 엔티티**다 (업무의 라벨/분류가 아니다)
    | 우리 이름·모양: 표 projects
    |   id(UUID) · name(String 300, NOT NULL) · description(Text|null) · state(String 20, default "active")
    |   · starts_on(Date|null) · ends_on(Date|null) · external_key(String 200, **unique**, null 가능)
    |   · created_by_actor_id · version · created_at · updated_at
    |   ★ **소유 조직 단위를 두지 않는다** — 부서를 가로지르려고 있는 것이라 의도적으로 뺐다
    |   짝이 되는 표: project_assignments (project_id · member_id · assignment_kind "lead"|"member"
    |   · valid_from · valid_until · ended_at · ended_by_member_id · end_reason)
    |     — 부분 unique index uq_project_assignment_active (ended_at IS NULL 일 때만)
    |   응답 타입: ProjectView {project_id, name, description, state, starts_on, ends_on,
    |                          external_key, version}
    |             ProjectDetailResult = ProjectView + {may_manage, members[], tasks[]}
    | 근거:
    |   persistence.py:838-861   ProjectRecord (:841-843 조직 소유를 두지 않는 이유)
    |   persistence.py:864-894   ProjectAssignmentRecord (:871-880 부분 unique)
    |   modules/work/project_results.py:5-13, 40-43  ProjectView · ProjectDetailResult
    |   modules/work/projects.py:89-374  ProjectApplication
    |   modules/datasets/schema.py:54  PROJECT_STATES = ("active", "closed")
    |
    | ▶ 목록 API: **있다** — GET /api/projects → list[ProjectView]  (http.py:1382-1387)
    |   MCP 로도 둘: list_projects (mcp.py:1488-1490) · project_list → {"entries": [...]} (mcp.py:1682-1684)
    |   구현: modules/work/projects.py:209-218 list()
    |     PROJECT_READ 역량 없으면 ProjectAccessDenied(403).
    |     ★ **붙어 있는 프로젝트만 보인다** — _readable() 이 principal.projects_for(PROJECT_READ) 하나로만
    |       연다 (projects.py:304-312: 「축이 하나면 뒷문이 없다. 부서로도, 만든 사람이라는 사실로도
    |       열리지 않고, 배정이라는 한 가지 사실로만 열린다」).
    |     ★ **필터·정렬·페이징이 하나도 없다.** 인자는 principal 뿐이다.
    |       저장소는 created_at 오름차순 전체를 읽는다 (platform/projects.py:71-72).
    |     ★ **state 로 거르지 않는다** — closed 프로젝트도 목록에 선다.
    |     ★ 업무 건수·진행률 같은 집계가 **ProjectView 에 없다.**
    |
    | 시안과의 차이: 시안 `PROJECT_OPTIONS` 는 (id, label) 짝 목록이다. 우리 ProjectView 는 그보다 넓고
    |   (기간·설명·회차·external_key), **집계는 없다.** 셀렉터 자체는 그대로 그릴 수 있다.
    |   ⚠ 「읽을 수 있는 프로젝트가 0개인 사용자」가 정상 상태다 — 배정이 유일한 열쇠이므로.
```

---

## 2. 표면 전수조사 — grep 으로 센 수

### 2-1. HTTP 라우터

`backend/src/ax_workspace/entrypoints/http.py` 전체 라우트 **159개** (`grep -c '@app\.(get|post|patch|put|delete)('`).
그중 이 화면의 사실이 나가는 입구는 아래 **48개**다 (projects 7 + tasks/task-/my-work 40 + calendar 1).

**응답 envelope**: **없다.** HTTP 는 TypedDict/리스트를 **그대로** 낸다 — 래퍼 키가 없다.
(MCP 쪽만 command 를 `CommandResult[...]` 로 감싸고, 일부 목록 도구가 `{"entries": [...]}` 로 낸다.)
오류는 도메인 예외 → `_runtime_error()` 가 HTTP 상태로 매핑한다.

#### projects (7개)
| 줄 | 메서드·경로 | 응답 타입 |
|---|---|---|
| 1382 | `GET /api/projects` | `list[ProjectView]` |
| 1389 | `POST /api/projects` | `ProjectView` (201) |
| 1403 | `GET /api/projects/{project_id}` | `ProjectDetailResult` |
| 1410 | `GET /api/projects/{project_id}/participation-history` | `list[ProjectParticipationView]` |
| 1420 | `POST /api/projects/{project_id}/tasks` | `TaskMutationResult` (201) |
| 1439 | `POST /api/projects/{project_id}/members` | `ProjectAssignmentView` (201) |
| 1457 | `DELETE /api/projects/{project_id}/members/{member_id}` | 204 |

#### tasks · task-* · my-work (40개)
| 줄 | 메서드·경로 | 응답 타입 |
|---|---|---|
| 679 | `GET /api/my-work` | `list[TaskListEntry]` |
| 1350 | `POST /api/tasks` | `TaskMutationResult` (201) |
| 1476 | `POST /api/tasks/assign` | (배정) 201 |
| 1489 | `GET /api/task-assignment-candidates` | `list[CandidateResponse]` |
| 1496 | `GET /api/task-assignments/sent` | `list[TaskAssignmentResult]` |
| 1503 | `POST /api/task-assignments/{assignment_id}/accept` | — |
| 1510 | `POST /api/task-assignments/{assignment_id}/decline` | — |
| 1519 | `PATCH /api/tasks/{task_id}` | `TaskDateMutationResult` |
| 1637 | `GET /api/tasks/{task_id}/materials` | — |
| 1644 | `POST /api/tasks/{task_id}/materials` | 201 |
| 1664 | `POST /api/tasks/{task_id}/completion-report` | `TaskCompletionResult` |
| 1676 | `POST /api/tasks/{task_id}/references` | 201 |
| 1685 | `DELETE /api/tasks/{task_id}/references/{reference_id}` | — |
| 1696 | `POST /api/tasks/{task_id}/schedules` | `TaskScheduleView` (201) |
| 1724 | `PATCH /api/task-schedules/{schedule_id}` | `TaskScheduleView` |
| 1779 | `GET /api/tasks/{task_id}/history` | `TaskHistoryResult` |
| 1786 | `GET /api/tasks/{task_id}/history/diff` | `TaskHistoryDiffResult` |
| 1798 | `GET /api/tasks/{task_id}/children` | `{task_id, parent, children, child_progress}` |
| 1812 | `GET /api/tasks/{task_id}/assignments` | dict |
| 1823 | `POST /api/tasks/{task_id}/reopen` | — |
| 1837 | `GET /api/tasks/{task_id}/proposals` | — |
| 1847 | `POST /api/tasks/{task_id}/proposals` | 201 |
| 1862 | `POST /api/tasks/{task_id}/proposals/{proposal_id}/respond` | — |
| 1878 | `POST /api/tasks/{task_id}/proposals/{proposal_id}/withdraw` | — |
| 1893 | `POST /api/tasks/{task_id}/reassign` | — |
| 1906 | `POST /api/tasks/{task_id}/materials/links` | 201 |
| 1919 | `POST /api/tasks/{task_id}/materials/references` | 201 |
| 1954 | `GET /api/tasks/{task_id}/materials/{material_id}/content` | — |
| 1968 | `POST /api/tasks/{task_id}/material-bindings/{binding_id}/detach` | — |
| 1975 | `GET /api/tasks` | `list[TaskListEntry]` |
| 1985 | `GET /api/tasks/{task_id}` | `TaskDetailResult` |
| 2133 | `POST /api/tasks/{task_id}/checklist` | `ChecklistMutationResult` (201) |
| 2142 | `PATCH /api/tasks/{task_id}/checklist/{item_id}` | `ChecklistMutationResult` |
| 2153 | `POST /api/tasks/{task_id}/checklist/order` | `ChecklistOrderResult` |
| 2164 | `DELETE /api/tasks/{task_id}/checklist/{item_id}` | — |
| 2501 | `POST /api/tasks/{task_id}/start` | `TaskDateMutationResult` |
| 2510 | `POST /api/tasks/{task_id}/block` | `TaskDateMutationResult` |
| 2514 | `POST /api/tasks/{task_id}/resume` | `TaskDateMutationResult` |
| 2518 | `POST /api/tasks/{task_id}/complete` | `TaskDateMutationResult` |
| 2522 | `POST /api/tasks/{task_id}/cancel` | `TaskDateMutationResult` |

#### 곁에 있는 것 (1 + 1)
| 줄 | 경로 | 비고 |
|---|---|---|
| 1742 | `GET /api/calendar?from=&to=` | 업무+회의 **합본**. `kind:'task'` 행이 `span_from`·`span_to` 를 낸다 — **축이 `my_work`**(활성 담당인 업무만) |
| 1754 | `GET /api/graph/overview?view=member\|team\|project&limit=120` | 관계 그래프. `view="project"` 축이 있다 |

### 2-2. 목록 조회의 필터·정렬·페이징 현황

**프로젝트 단위로 업무를 긁는 경로는 이미 있다 — `GET /api/projects/{project_id}` 하나다.**
그러나 **필터도 정렬도 페이징도 없다.**

| 조회 | 필터 | 정렬 | 페이징 |
|---|---|---|---|
| `GET /api/projects` | 없음 (읽을 수 있는 것만) | `projects.created_at` 오름차순 (platform/projects.py:72) | 없음 |
| `GET /api/projects/{id}` → `tasks[]` | **없음 — done·cancelled 포함 전부** (platform/projects.py:204-209) | `tasks.created_at` 오름차순 | 없음 |
| `GET /api/tasks`, `GET /api/my-work` | `include_closed: bool` **하나뿐** (http.py:1976, 680) | 저장소 순서 | 없음 |
| `tasks_in_projects()` (내부) | `include_closed` 로 `state NOT IN (done, cancelled)` (work_tasks.py:1095-1096) | `created_at` | 없음 |
| `GET /api/calendar` | `from`·`to` **필수** | — | 없음 |
| `GET /api/meetings` | `cursor`·`from`·`to` | — | **20건 커서** ← 이 저장소에서 페이징이 있는 유일한 목록 |

`Query(...)` 사용은 http.py 전체에서 **13곳**뿐이다.

### 2-3. MCP 표면

`backend/src/ax_workspace/entrypoints/mcp.py` — `@server.tool` **125개**.
이름에 project/task/work 가 든 것 **52개**. 프로젝트 관련만 추리면:

| 줄 | 도구 | 종류 |
|---|---|---|
| 1489 | `list_projects` → `list[ProjectView]` | read |
| 1493 | `get_project(project_id)` → `ProjectDetailResult` | read |
| 1683 | `project_list()` → `{"entries": [...]}` | read (위와 같은 사실, 다른 포장) |
| 1871 | `project_create` | command (사람 확인 필요) |
| 1875 | `project_assign_member` | command |
| 1879 | `project_release_member` | command |
| 1883 | `project_participation_history` | read |
| 1887 | `project_plan_work` | command |

업무 쪽 read 도구: `my_task_list` · `task_list` · `task_get` · `task_subtask_list` ·
`task_checklist_list` · `task_assignment_list` · `task_history` · `task_history_diff` ·
`task_materials_list` · `task_proposal_list` · `sent_task_assignments` · `task_assignment_candidates`.

⚠ `task_progress_batch` (mcp.py:1957) 는 **진행률이 아니다** — 같은 종류의 명령을 한 번에 사람이
확인하는 배치다 (facade: mcp.py:1074-1082).

### 2-4. operation inventory / 스키마 정의 파일

- `docs/unified-operations-inventory.json` (관측 `2026-09-13`, baseline R2 / R3f) —
  `http` 112 entry 중 project|/tasks|task_ 매칭 **39**, `mcp` 42 entry 중 **20**.
  drift 검사는 `backend/tests/architecture/test_operation_inventory.py`.
- 표 정의의 SoT 는 **단일 파일**: `backend/src/ax_workspace/platform/persistence.py` (1985줄, `__tablename__` **91개**).
- 응답 타입 SoT: `modules/work/task_results.py`(375줄, 최상위 class 38개) ·
  `modules/work/project_results.py`(57줄, 최상위 class 7개).
- 역량 카탈로그: `modules/organization_access/catalog.py`, MCP 도구 카탈로그:
  `modules/ax_execution/tool_catalog.py`(도구 → 역량), `entrypoints/mcp.py:201-204`(`project.*` 명령 → `project.manage`).

### 2-5. 마이그레이션 — 해당 표가 언제 생겼나

**Alembic 도 migrations 체계도 없다.** 스키마는 SQLAlchemy `Base.metadata` 가 정본이고,
`bootstrap/reset.py:20` 의 `create_all()` 이 새로 만들고, `bootstrap/schema_sync.py`
(= `make sync-demo-schema`, 72줄)가 **없는 표를 만들고 없는 컬럼만 더한다** — 절대 지우거나
타입을 바꾸지 않고, 데이터가 사라질 변경은 「사람이 결정할 것」으로 출력만 한다.
손으로 적용하는 `.sql` 은 딱 2개다 (`backend/migrations/manual/2026-09-17-w2-indexes*.sql`,
`work_requests` 인덱스 2개. 그 파일 머리말이 「이 저장소에는 alembic 도 migrations 체계도 없다」고 적는다).

따라서 「언제 생겼나」는 **git 이력**이 답한다 (`git log -S '__tablename__ = "..."'`):

| 표 / 열 | 커밋 | 날짜 |
|---|---|---|
| `tasks` | `f275ea4` feat: add direct self task lifecycle | 2026-09-03 |
| `task_checklist_items` | `e09a60d` feat: add task checklist items | 2026-09-04 |
| `tasks.parent_task_id` | `029731b` feat: let work be broken into work, one level deep | 2026-09-06 |
| `projects` · `project_assignments` · `tasks.project_id` | `1fa6547` feat: 프로젝트 — 조직 단위와 나란한 두 번째 축 | 2026-09-07 |
| `task_predecessors` | `1b40f83` feat: 업무 요청 자료 및 업무 연결 계약 구현 | 2026-09-20 |
| `task_schedules` | `e46ce39` feat(calendar): 업무에 시간을 배분한다 (#2) | 2026-09-21 |

**선행(D-4)과 시간 배정은 어제·그저께 들어왔다.** 프로젝트 화면이 기대는 두 축이 가장 새것이다.

---

## 3. 화면 자리별 — 지금 무엇이 나오고 무엇이 안 나오나

시안 §3~§6 의 자리를 우리 응답에 대어 본 것이다. **판단이 아니라 대조표다.**

### 좌 레일 (업무 카드 목록 + 프로젝트 셀렉터)
| 필요 | 있나 | 어디서 |
|---|---|---|
| 프로젝트 선택지 | ✅ | `GET /api/projects` → `ProjectView.name` |
| 업무 건수 배지 | ✅ (배열 길이) | `GET /api/projects/{id}` → `tasks[].length` |
| 상태 배지 | ✅ (5종) | `tasks[].state` — ⚠ `completion_submitted` 가 **접히지 않고 그대로 나온다** (§5-3) |
| 제목 | ✅ | `tasks[].title` |
| meta: when | ✅ | `tasks[].start_date`·`due_date` |
| meta: 담당 | ❌ | `ProjectTaskView` 에 없다 |
| meta: 분류 | ❌ | 그런 필드가 없다 (D-8) |

### 본문 ① 요약 스트립 (5칸)
| 칸 | 있나 | 어떻게 |
|---|---|---|
| 전체 업무 | ✅ | `tasks[].length` |
| 진행 중 | ✅ | `state=="in_progress"` 세기 |
| 지연 | ⚠ | `derived.overdue_days` 가 그 답인데 **프로젝트 상세 tasks[] 에 없다.** `due_date` 로 클라이언트 계산은 가능 |
| 완료 | ✅ | `state=="done"` 세기 — ⚠ 승인 대기 done 이 섞인다 |
| 전체 진행률 | ❌ | **없다** (D-3) |

### 본문 ② 진행 라인(간트) + ③ 의존선
| 필요 | 있나 | 어디서 |
|---|---|---|
| 바의 시작·끝 | ✅ | `tasks[].start_date`·`due_date` — ⚠ null·역전 처리 필요. `task_span()` 규칙이 이미 있다 |
| 바 색(status) | ✅ | `tasks[].state` |
| 바 안 진행률 fill·% | ❌ | **없다** (D-3) |
| 상위–하위 행 | ✅ | `tasks[].parent_task_id` — ⚠ 깊이 무제한 (D-5) |
| `하위 N` 카운트 | ⚠ | 평평한 `tasks[]` 에서 클라이언트가 셀 수 있다. 서버 집계는 `child_progress` 인데 상세에만 있다 |
| 이름 줄의 담당 | ❌ | `ProjectTaskView` 에 없다 |
| 의존선 (선행→후행) | ✅ | `tasks[].preceding_task_ids` — **계약으로 「간트 연결선의 유일한 원천」** |

### 우 레일 (선택 업무 상자) — `GET /api/tasks/{task_id}` 가 답한다
| 블록 | 필요 | 있나 |
|---|---|---|
| 머리 | 제목 | ✅ `title` |
| 머리 | 진행률 미터 + % | ❌ (D-3) |
| 메타 | 상태 | ✅ `state` (+ `derived.approval` 로 승인 대기 구분) |
| 메타 | 기간 | ✅ `start_date`·`due_date` |
| 메타 | 담당 | ✅ `assignee {member_id, display_name}` |
| 메타 | 요청 | ✅ `origin.actor` + `origin.actor_role=="요청자"` |
| 메타 | 분류 | ❌ 그런 필드가 없다 |
| 메타 | 상위 업무 | ✅ `parent {task_id,title,state}` |
| 관계 | **선행** 건수+목록 | ✅ `predecessors[] {task_id,title,state}` — 읽을 수 없으면 title/state 가 null |
| 관계 | **후행** 건수+목록 | ⚠ **서버 경로 없다.** 프로젝트 상세 `tasks[].preceding_task_ids` 를 뒤집으면 **프로젝트 범위 안에서는** 만들 수 있다 |
| 체크리스트 | done/total + 항목 | ✅ `checklist[]` + `checklist_progress` — ⚠ 둘 다 `NotRequired`, `access=="read_only"` 면 안 실린다 |
| 하위 업무 | 카드 목록 | ✅ `children[]` (TaskSummaryView: task_id·title·state·due_date·assignee·derived) |
| 하위 업무 | 카드의 「N%」 | ❌ (D-3) |

---

## 4. 권한 — 화면이 부딪힐 자리

조사 중 반복해서 나온 사실이라 따로 적는다. 설계가 아니라 **지금 코드가 그렇다**는 기술이다.

- **프로젝트는 「붙어 있는가」 하나로만 열린다.** 부서로도, 만든 사람이라는 사실로도 열리지 않는다
  (`modules/work/projects.py:304-312`). 읽을 수 없는 프로젝트는 **없는 것처럼** 404 다 (:314-319).
- 역량 세 개: `project.read` · `project.manage` · `task.assign`
  (`modules/work/projects.py:23-28` import, `entrypoints/mcp.py:201-204` 의 `project.*` → `project.manage` 매핑).
- **읽을 수 있는 프로젝트가 0개인 사용자가 정상이다** — 셀렉터가 빈 경우를 정상 상태로 가져야 한다.
- 프로젝트 상세의 `tasks[]` 는 **담당·조직과 무관하게 그 프로젝트의 업무 전부**를 낸다
  (`platform/projects.py:204-209` — `WHERE project_id = ?` 뿐).
  같은 프로젝트에 있으면 남의 업무 상세도 열린다 (`tests/contract/test_projects.py:86-93`),
  프로젝트에서 빠지면 그 순간 닫힌다 (:101).
- 반대로 읽을 수 없는 **선행**은 목록에는 id 가 남고 `title`/`state` 만 null 이 된다 —
  「제목은 감추고 건수는 낸다」 (`task_results.py:112-116`,
  `tests/contract/test_task_predecessors.py:464-478`).
- `may_manage: bool` 을 서버가 직접 낸다 — 화면이 권한을 추측해 단추를 그리지 않는다
  (`modules/work/projects.py:234-235`).

---

## 5. 문서 ↔ 코드가 어긋나는 지점

브리프 §1 이 준 SPEC/WP 와 저장소 안 주석을 코드와 대조한 결과다. **코드를 사실로 적었다.**

### 5-1. 「진행률은 쓰지 않는다」 vs 시안이 네 자리에서 % 를 그린다
- 문서: `20-spec/spec-001-work-management.md:200` — 「**기한 경과일**: 실제 기한을 넘긴 행에만 날짜
  뒤에 `+N` 을 붙인다. **진행률은 쓰지 않는다.**」
- 코드: 진행률이 **정말 없다** (D-3). 대신 `derived.overdue_days` 가 정확히 그 `+N` 이다
  (`application.py:2521-2529`).
- 즉 D-3 은 「빠뜨린 것」이 아니라 **SPEC 이 의식적으로 배제한 것**이다. 시안은 그 결정을 모른 채 그렸다.
  → 코디네이터·planner 판단 필요.

### 5-2. 하위 깊이 — 같은 저장소 안 주석이 서로 어긋난다
- `platform/persistence.py:935-936`: 「One level only for now: a child never becomes a parent」
- `modules/work/application.py:385-387`: 「**저장 깊이에 제한이 없다** (정책 V-6). 예전에는 …
  한 단계에서 끊었고 … 화면이 두 단계만 보이는 것은 **표시**의 일이고 저장과 무관하다 (정책 L-11).」
- **코드가 이긴다** — `parent_for()` 에 깊이 검사가 없다. persistence 주석이 낡았다.
  (고치지 않았다 — 조사 범위 밖.)

### 5-3. 프로젝트 상세만 `_external_state()` 를 지나지 않는다
- 계약: 밖으로 나가는 상태는 `completion_submitted` 를 `done` 으로 접는다
  (`modules/work/application.py:2495-2506`).
- 그런데 `modules/work/projects.py:244` 는 `"state": task.state` 로 **원값을 그대로** 낸다.
  `ProjectApplication` 은 `work.application` 을 import 하지 않으므로 그 투영을 지나지 않는다.
- 따라서 **`GET /api/projects/{id}` 의 `tasks[].state` 에는 `completion_submitted` 가 그대로 실린다.**
  같은 업무가 `GET /api/tasks/{id}` 에서는 `"done"` 으로 보인다. → §7 「눈에 띈 것」에도 적었다.

### 5-4. `TaskMutationResult.state` 주석이 「넷뿐이다」라고 하지만 실제는 다섯이다
- `modules/work/task_results.py:69`: 「**넷뿐이다** — `open` · `in_progress` · `done` · `cancelled`」
- 그런데 같은 저장소의 `_external_state()` 가 **`blocked` 를 그대로 통과시킨다**
  (`application.py:2503-2505`: 「`blocked` 도 계약에 없지만 이 work 는 그 값을 발행하지도 없애지도
  않는다(M-6) — 들어오는 그대로 낸다」). `POST /api/tasks/{id}/block` 이 그 값을 실제로 세운다
  (http.py:2510). **실제 외부 값은 5종**이다.
- 시안의 5종과 **개수는 맞는다** — 이름만 다르다.

### 5-5. SPEC-004 가 시안 상태 5종을 이미 폐기했다
- `20-spec/spec-004-calendar-scheduling.md:1173`:
  「`status` 5종(`progress`·`not-started`·…) | **백엔드 `TaskState` 가 정본. 시안 5종은 폐기** |
   (확정 — 사용자 지시 D4) 「상태값 정본은 우리 백엔드가 가지고 있는 거야」」
- 코드와 일치한다. **이 화면도 같은 결정을 물려받는다.**

### 5-6. MCP 도구 설명이 없는 도구 이름을 가리킨다
- `modules/ax_execution/tool_catalog.py:80`·`:83` 의 설명문이 `project_get` 을 부르라고 적는다.
- 실제 등록된 도구 이름은 `get_project` 다 (`entrypoints/mcp.py:1493`). `project_get` 은 없다
  (`grep -n "project_get" entrypoints/mcp.py` → 0건). 조사 범위 밖이라 고치지 않았다.

---

## 6. 찾지 못한 것 — 이렇게 찾아봤다

| 찾던 것 | 찾은 방법 | 결과 |
|---|---|---|
| 진행률 % 컬럼·파생값 | `grep -rn "percent\|progress_rate\|진행률\|completion_rate\|progress_pct" backend/src/`; `tasks` 컬럼 49개 육안 열거 (persistence.py:910-958); `grep -rn "progress" modules/work/` | **없다.** §D-3 |
| 후행(successor) 조회 | `grep -rn "successor\|후행" backend/src/ax_workspace/modules/work/ platform/work_tasks.py`; `predecessors_for`·`predecessor_edges`·`active_predecessor_ids` 세 함수 전부 열람 | **없다** — 셋 다 `WHERE task_id IN (...)` 단방향 |
| 프로젝트 단위 집계(업무 수·진행률) API | `ProjectView`·`ProjectDetailResult` 전체 열람(project_results.py 57줄); `grep -n "@app.*api/projects" http.py` | **없다** — 집계 필드 0개 |
| 목록 필터·정렬·페이징 | `grep -c "Query(" http.py` (13곳) + 각 핸들러 시그니처 열람 | 업무 목록은 `include_closed` 하나뿐. 페이징은 `/api/meetings` 에만 |
| 「분류」(group) 필드 | `grep -rn "보낸 업무\|내 업무" backend/src/` | 응답 필드 0건 — 엔드포인트 축이다 |
| Alembic / 마이그레이션 | `find backend -iname "*alembic*" -o -iname "*migration*"`; `grep -rn "create_all" backend/src/` | 체계 없음. `create_all` + `schema_sync` + 손 `.sql` 2개 |
| 프로젝트 state 전이 규칙 | `grep -rn "ProjectRecord.state\|PROJECT_STATE" backend/` | 값은 `("active","closed")` (datasets/schema.py:54) 뿐. **전이 함수도 명령도 없다** — 프로젝트를 닫는 API 가 없다 |

---

## 7. 눈에 띈 것 (고치지 않았다 — 한 줄씩)

1. **`GET /api/projects/{id}` 의 `tasks[].state` 가 `_external_state()` 를 지나지 않아
   `completion_submitted` 가 그대로 샌다** — 같은 업무가 `GET /api/tasks/{id}` 에서는 `"done"` 이다.
   (`modules/work/projects.py:244` vs `modules/work/application.py:2495-2506`)
2. **`platform/projects.py:204-209` `tasks_in()` 이 done·cancelled 를 거르지 않고 페이징도 없다** —
   업무가 수백 건인 프로젝트에서 상세 하나가 전부를 싣는다. (`tasks_in_projects()` 쪽은
   `include_closed` 를 갖는데 이쪽만 없다.)
3. **`modules/work/projects.py:209-218` `list()` 가 `all_projects()` 전체를 읽고 파이썬에서 거른다** —
   읽을 수 있는 것이 1개여도 전 프로젝트를 읽는다.
4. `platform/persistence.py:935-936` 의 「One level only for now」 주석이 코드보다 낡았다 (§5-2).
5. `modules/work/task_results.py:69` 의 「넷뿐이다」가 실제 5종과 어긋난다 (§5-4).
6. `modules/ax_execution/tool_catalog.py:80,83` 의 설명이 없는 도구 `project_get` 을 가리킨다 (§5-6).
7. **프로젝트를 닫는 명령이 없다** — `projects.state` 에 `"closed"` 값이 정의돼 있는데
   (`modules/datasets/schema.py:54`) 그 값을 세우는 API·operation 이 없다. 데이터셋 import 로만 들어온다.
8. `ProjectApplication.assign()` 은 기존 활성 배정이 있으면 `kind` 가 달라도 그대로 영수증을 돌려준다
   (`modules/work/projects.py:163-165`) — `member` 를 `lead` 로 승격하는 길이 없다.

---

## 8. 검증 (이번 작업의 검증은 테스트가 아니라 근거다)

- [x] D-1 ~ D-9 **9개 전부**에 판정이 있다. 빠진 번호 없음.
- [x] 모든 판정에 `파일:줄` 근거가 붙어 있다. 부재 판정에는 **찾은 방법**을 §6 에 적었다.
- [x] 상태 enum 은 `modules/work/lifecycle.py:20-26` 과 `:93-104` 에서 **그대로 복사**했다.
- [x] 표면은 grep 으로 센 수다 — HTTP 159개 중 48개 전부 나열(§2-1), MCP 125개 중 project 8개 나열,
      inventory 112/42 entry 매칭 수 기재.
- [x] 코드·설정·테스트 **무변경**. 커밋·push 없음. 서버·DB 미기동. 테스트 미실행.
- [x] `frontend/` 를 읽지 않았다 (다른 워커 담당).
- [x] 쓴 파일은 이 리포트 하나다.

검증 시점 워킹트리 상태: `git status --porcelain` → clean (이 리포트는 다른 저장소에 있다).
