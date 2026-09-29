# 업무 구조 백엔드 전수조사

조사 대상: `/Users/kknaks/orca/workspaces/Strong_hajin/strong-hajin-design` (브랜치 `kknaksss/strong-hajin-design`, base `origin/main`)
범위: `backend/src/ax_workspace/` 전부 (170 `.py`). **읽기 전용 — 코드·테스트를 한 줄도 바꾸지 않았고 테스트도 돌리지 않았다.**
경로는 모두 `backend/src/ax_workspace/` 기준 상대경로다.

## 0. 한 줄 요약

선행·후행 관계는 **저장·입력·검증·시작 게이트까지 전부 서 있다** (`task_predecessors` 표 · `preceding_task_ids` 입력 · 다섯 거절 코드 · `TaskPredecessorGate`), 그런데 **`successor` 라는 단어가 백엔드 전체에 0회 나오고 「나를 선행으로 삼는 업무」를 내주는 조회·필드·엣지가 어디에도 없다** — 후행은 프로젝트 상세 `tasks[]` 의 `preceding_task_ids` 를 화면이 뒤집어야만 얻어지며, 그 사실이 `modules/work/projects.py:431` 주석에 「후행 배열은 싣지 않는다 … 화면이 센다」로 명시돼 있다.

## 1. 심볼 개수표 (§5)

`grep -rho` 기준 **실제 출현 횟수**(줄 수가 아니라 토큰 수)다. `backend/src/ax_workspace/` 안 `*.py` 만 센다. `entrypoints` 는 http·mcp 로 쪼갰다 — 나머지 entrypoints(워커 5개·`reset_demo`·`dataset`·`protected`·`http_auth`·`material_backfill`·`mcp_server`)는 **여덟 심볼 모두 0회**다.

| 심볼 | 전체 | entrypoints/http.py | entrypoints/mcp.py | 그 외 entrypoints(워커 등) | modules/work | modules 그 외 | platform | bootstrap |
|---|---|---|---|---|---|---|---|---|
| `preceding` | 91 | 6 | 10 | 0 | 50 | 2 | 7 | 16 |
| `predecessor` | 97 | 0 | 0 | 0 | 69 | 0 | 28 | 0 |
| **`successor`** | **0** | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| `parent_task_id` | 115 | 6 | 10 | 0 | 60 | 1 | 24 | 14 |
| `reference_task_ids` | 74 | 6 | 15 | 0 | 34 | 1 | 7 | 11 |
| `project_id` | 327 | 21 | 36 | 0 | 156 | 4 | 70 | 40 |
| `source_work_request_id` | 47 | 0 | 0 | 0 | 20 | 0 | 27 | 0 |
| `supersedes` | 45 | 2 | 0 | 0 | 22 | 0 | 18 | 3 |
| `blocking` | 29 | 0 | 0 | 0 | 27 | 1 | 0 | 1 |


### 1.1 파일별 — `modules/work/`

| 파일 | preceding | predecessor | parent_task_id | reference_task_ids | project_id | source_work_request_id | supersedes | blocking |
|---|---|---|---|---|---|---|---|---|
| `application.py` | 13 | 55 | 20 | 6 | 34 | 16 | 0 | 17 |
| `creation_commands.py` | 12 | 0 | 13 | 12 | 13 | 1 | 6 | 0 |
| `requests.py` | 6 | 6 | 10 | 4 | 17 | 1 | 9 | 0 |
| `projects.py` | 6 | 2 | 3 | 0 | 37 | 0 | 0 | 0 |
| `task_commands.py` | 6 | 1 | 0 | 0 | 3 | 0 | 0 | 0 |
| `assignments.py` | 0 | 0 | 8 | 6 | 16 | 0 | 3 | 0 |
| `task_creation.py` | 3 | 0 | 3 | 5 | 6 | 0 | 0 | 0 |
| `task_results.py` | 2 | 1 | 0 | 0 | 1 | 1 | 0 | 4 |
| `lifecycle.py` | 0 | 4 | 0 | 0 | 0 | 0 | 0 | 0 |
| `errors.py` | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 6 |
| `graph.py` | 0 | 0 | 0 | 0 | 21 | 1 | 0 | 0 |
| `project_results.py` | 1 | 0 | 2 | 0 | 1 | 0 | 0 | 0 |
| `request_results.py` | 1 | 0 | 1 | 1 | 1 | 0 | 1 | 0 |
| `request_commands.py` | 0 | 0 | 0 | 0 | 0 | 0 | 3 | 0 |
| `project_commands.py` | 0 | 0 | 0 | 0 | 4 | 0 | 0 | 0 |
| `graph_results.py` · `drafts.py` | 0 | 0 | 0 | 0 | 1 각 | 0 | 0 | 0 |

### 1.2 파일별 — `platform/` · `bootstrap/` · `modules` 그 외

| 파일 | 해당 심볼 · 횟수 |
|---|---|
| `platform/work_tasks.py` | `predecessor` 21, `source_work_request_id` 20, `parent_task_id` 16, `project_id` 15, `supersedes` 11, `preceding` 3, `reference_task_ids` 2 |
| `platform/persistence.py` | `predecessor` 7, `source_work_request_id` 7, `parent_task_id` 6, `supersedes` 6, `project_id` 5, `preceding` 1 (표 정의 자리) |
| `platform/projects.py` | `project_id` 39 |
| `platform/actions.py` | `project_id` 11, `reference_task_ids` 5, `preceding` 2, `parent_task_id` 2 |
| `platform/action_center.py` | `supersedes` 1 |
| `platform/reports.py` | `preceding` 1 — **업무와 무관하다.** 보고서 워크플로 노드의 선행 노드 provenance 주석 (`platform/reports.py:745`) |
| `bootstrap/application.py` | `project_id` 23, `preceding` 11, `parent_task_id` 11, `reference_task_ids` 11, `supersedes` 3 — 전부 조립층 위임 인자 |
| `bootstrap/demo_work.py` | `project_id` 9, `preceding` 5 (`demo_work.py:207,228,243`), `parent_task_id` 2 — 데모 seed |
| `bootstrap/scenario.py` | `project_id` 5, `parent_task_id` 1 (`scenario.py:174`) |
| `bootstrap/dataset_import.py` | `project_id` 3 |
| `bootstrap/isolated_work.py` | `blocking` 1 — **업무와 무관하다.** 모듈 docstring 의 "blocking provider/parser work" (`isolated_work.py:1`) |
| `modules/meetings/commands.py` | `preceding` 1, `parent_task_id` 1, `reference_task_ids` 1, `project_id` 1 — `PromoteTodoInput` (`meetings/commands.py:272-275`) |
| `modules/meetings/batch_service.py` | `blocking` 1 — **업무와 무관하다.** `lock.acquire(blocking=False)` (`batch_service.py:242`) |
| `modules/reports/workflow_metadata.py` | `preceding` 1 — **업무와 무관하다.** 보고서 노드 그래프 오류 문구 (`workflow_metadata.py:76`) |
| `modules/ax_execution/command_contracts.py` | `project_id` 3 |

**업무 구조와 무관한 잡음 5건**을 위에 명시했다: `platform/reports.py:745` · `modules/reports/workflow_metadata.py:76` · `bootstrap/isolated_work.py:1` · `modules/meetings/batch_service.py:242` (그리고 `modules/work/application.py` 안의 `blocking` 은 전부 `blocking_children` 계열로 업무 것이다).

---

## 2. 관계 다섯 — 각각 §3 의 표

### 2.1 상위 ↔ 하위 (`parent_task_id`)

| 물음 | 답 | 근거 |
|---|---|---|
| 저장 모양 | **조인테이블 없음.** `tasks.parent_task_id UUID NULL FK → tasks.id`, `index=True`. 별도 depth·path 열 없다 | `platform/persistence.py:937` (`TaskRecord` 는 897) |
| | 요청 쪽에도 같은 이름의 열이 따로 있다: `work_requests.parent_task_id UUID NULL FK → tasks.id`, `use_alter=True`(두 표가 서로를 참조해 `create_all` 순서가 안 정해지는 것을 푸는 장치), index `ix_work_requests_parent_task_id` | `platform/persistence.py:1682-1684`, 인덱스 `1633` |
| 어느 엔드포인트가 **받나** — 생성 | `POST /api/tasks` (`CreateTaskRequest.parent_task_id`) | `entrypoints/http.py:1355`, 인자 전달 `1376` |
| | `POST /api/tasks/assign` (`TaskAssignmentInput.parent_task_id`) | `entrypoints/http.py:1481`; 입력 `modules/work/task_creation.py:20` |
| | `POST /api/work-requests` (`CreateWorkRequestRequest.parent_task_id`) | `entrypoints/http.py:1997`, 전달 `2012` |
| | `POST /api/meetings/{id}/todos/{id}/promote` | `entrypoints/http.py:824`, 전달 `850` |
| | MCP `task_create_self` · `task_assign` · `work_request_create` | `entrypoints/mcp.py:1970`(`parent_task_id` 1975) · `2005`(2010) · `1633` |
| 어느 엔드포인트가 **받나** — 수정 | **없다.** `PATCH /api/tasks/{id}` 의 편집 계약 `TaskEditFields` 에 `parent_task_id` 가 **없다** (`extra='forbid'` 이므로 보내면 422) | `modules/work/task_commands.py:45-58` (`TaskEditFields`), 라우트 `entrypoints/http.py:1524` |
| | 상위를 바꾸는 명령·엔드포인트를 **못 찾았다** |  |
| 어느 응답이 **내보내나** | 업무 상세 `parent: {task_id,title,state} \| null` + `children: TaskSummaryView[]` + `child_progress:{done,blocking,cancelled,total}` | 조립 `modules/work/application.py:1394-1398`; 타입 `modules/work/task_results.py:232-234`, `TaskParentView` 199, `TaskChildProgressView` 180 |
| | `GET /api/tasks/{id}/children` → `{task_id, children, child_progress}` (직속 하위만) | `entrypoints/http.py:1803`; 구현 `modules/work/application.py:1401-1410`; 타입 `task_results.py:302-306` |
| | 프로젝트 상세 업무 줄의 `parent_task_id: str \| null` | `modules/work/projects.py:444`; 타입 `modules/work/project_results.py:57` |
| | 요청 응답의 `parent_task_id: str \| null` | `modules/work/requests.py:1465`; 타입 `modules/work/request_results.py:52` |
| | **업무 목록(`GET /api/tasks`)·업무 변경 응답(`TaskMutationResult`)에는 `parent_task_id` 가 없다** — `_view()` 가 싣지 않는다 | `modules/work/application.py:2459-2509` (`_view` 전문), 타입 `task_results.py:66-98` |
| 검증 규칙 — 무엇을 거절하나 | 읽을 수 없는 상위 → `TaskNotFound`; 상위가 `done`·`cancelled` → `TaskParentClosed`; 자기 자신·자기 조상을 상위로 → `TaskParentCycle`; 상위에 활성 담당자가 없음 → `TaskParentUnassigned`; 같은 사람의 직접 작업 중첩(중심 업무 직속이 아님) → `TaskDirectNesting` | `modules/work/application.py:382-414` (`parent_for`), `478-490` (`_require_may_hold_children`) |
| | 하위는 상위의 프로젝트를 물려받고 **자기 프로젝트를 따로 못 갖는다** → 수정 시 `TaskError("하위 업무의 프로젝트는 상위 업무를 따릅니다")` | `modules/work/application.py:526-528` |
| 오류 코드·예외 클래스·메시지 | `TaskParentCycle` → **422** · 「자기 자신이나 상위 업무를 하위로 둘 수 없습니다」 | 클래스 `modules/work/errors.py:39`; 매핑 `entrypoints/http.py:566-568`; 메시지 `application.py:411` |
| | `TaskParentClosed` → **409** · 「이미 끝난 업무에는 하위 업무를 추가할 수 없습니다」 | `errors.py:51`; 매핑 `http.py:541-546`; 메시지 `application.py:413` |
| | `TaskParentUnassigned` → **409** · 「아직 수락되지 않은 업무에는 하위 업무를 만들 수 없습니다. 수락 후에 다시 시도하세요」 | `errors.py:47`; `http.py:545`; `application.py:486` |
| | `TaskDirectNesting` → **409** · 「직접 작업은 중심 업무의 바로 아래에만 둘 수 있습니다」 | `errors.py:43`; `http.py:543`; `application.py:490` |
| | **응답 본문은 `detail=str(error)` — 사람이 읽는 문장 하나뿐이고 기계용 `code` 필드가 없다** (SPEC 코드명은 docstring 에만 있다) | `entrypoints/http.py:541-568` |
| 방향이 양쪽인가 | **양쪽.** 상위→하위는 `children_of(parent_task_id == id)`, 하위→상위는 `parent_task_id` 열 자체. 자손 전체 조회도 둘 있다: `descendants_of` · `descendant_ids_of` | `platform/work_tasks.py:475-481`(children_of), `484-...`(descendants_of), `667-680`(descendant_ids_of) |
| 깊이·개수 제한 | **저장 깊이 제한 없다** (정책 V-6). `parent_for` docstring 이 명시. 화면이 두 단계만 보이는 것은 표시의 일 | `modules/work/application.py:390-397` |
| | 하위 개수 제한을 **못 찾았다.** 무한 순회 방지만 있다 — `_ancestor_ids` · `descendants_of` · `descendant_ids_of` 모두 「본 것을 다시 보지 않는다」 | `application.py:450-459`, `platform/work_tasks.py:492-...`, `672-680` |
| | 상세 `children` 은 **직속 하위만** (정책 L-11) | `modules/work/application.py:1372-1379` |
| 권한 — 누가 만들고 누가 읽나 | 만들기: `TASK_SELF_MANAGE`(내 업무) / `TASK_ASSIGN`(배정) / `WORK_REQUEST_CREATE`(요청) | `application.py:270`; `assignments.py` 참조; 이름 `modules/organization_access/domain.py:91-101` |
| | 읽기: `TASK_READ` + 그 업무 자체의 읽기 판정. **상위를 든 사람·상위에 사람을 붙인 사람은 하위를 읽는다** (`_manages(parent_task_id)`) | `application.py:963-967` |
| | **요청자는 자기 요청 업무의 하위 트리 전체를 깊이 제한 없이 읽는다** (정책 V-21) — 조상 중 하나라도 자기가 요청자면 열린다. 수신자·참조자(cc)는 여기 안 들어간다 | `application.py:971-973`, 구현 `417-446` (`_requested_ancestor`) |
| | 읽을 수 없는 하위는 **목록에도 건수에도 없다**; 다만 **완료를 막는 검사는 읽을 수 없는 하위까지 전부 센다** | `application.py:1380-1391`, `1476-1490`, `1497-1519` |

### 2.2 선행 ↔ 후행 (`preceding_task_ids` / `task_predecessors`)

| 물음 | 답 | 근거 |
|---|---|---|
| 저장 모양 | **전용 조인테이블 `task_predecessors`**: `id` · `task_id FK→tasks.id NOT NULL`(뒤에 오는 업무) · `predecessor_task_id FK→tasks.id NOT NULL`(먼저 끝나야 하는 업무) · `position INT NOT NULL default 0` · `created_by` · `created_at` · `released_at NULL` · `released_by NULL` | `platform/persistence.py:995-1045` (클래스 995, 열 1027-1045) |
| | 제약 셋: 부분 unique `uq_task_predecessors_active(task_id, predecessor_task_id) WHERE released_at IS NULL` · CHECK `ck_task_predecessors_not_self(task_id <> predecessor_task_id)` · index `ix_task_predecessors_task_id(task_id)` | `platform/persistence.py:1014-1025` |
| | **`predecessor_task_id` 단독 인덱스가 없다** — 역방향 조회를 위한 인덱스 자리가 비어 있다 | `platform/persistence.py:1014-1025` (index 는 `task_id` 만) |
| | **행을 지우지 않고 닫는다** (`released_at`). 닫힌 행은 부분 unique 에서 빠지므로 같은 관계를 다시 세울 수 있다 | `platform/persistence.py:1002-1004`, `1039-1041` |
| | `work_requests` 에는 **선행 열·표가 없다.** 요청의 선행은 발송이 세우는 Task 의 `task_predecessors` 행이 유일한 자리다 | `platform/persistence.py:1625-1692`(요청 표 전문에 선행 열 없음); 명시 주석 `platform/work_tasks.py:2163-2168` |
| 어느 엔드포인트가 **받나** — 생성 | `POST /api/tasks` (`preceding_task_ids`) | `entrypoints/http.py:1355`, 전달 `1379` |
| | `POST /api/work-requests` (`preceding_task_ids`) | `entrypoints/http.py:1997`, 전달 `2010` |
| | `POST /api/meetings/{id}/todos/{id}/promote` | `entrypoints/http.py:824`, 전달 `851` |
| | MCP `task_create_self` (`preceding_task_ids`) · MCP `work_request_create` (`preceding_task_ids`) | `entrypoints/mcp.py:1970`(1982) · `1633`(1640) |
| | **`POST /api/tasks/assign` · MCP `task_assign` 은 받지 않는다** — `TaskAssignmentInput` 은 `TaskCreationFields` 상속이라 `preceding_task_ids` 가 없다 | `modules/work/task_creation.py:12-41`(`TaskCreationFields`), `116`(`TaskAssignmentInput`); MCP `entrypoints/mcp.py:2005-2012` |
| | **`POST /api/tasks` + `assignee_id`(남에게 보내는 갈래)는 `preceding_task_ids` 를 명시적으로 거절한다** — 조용히 버리지 않고 422 | `modules/work/creation_commands.py:168-198` (`_refuse_unsupported_horizontal_fields`), 이름 목록 `186` |
| 어느 엔드포인트가 **받나** — 수정 | `PATCH /api/tasks/{id}` **하나뿐이다.** `preceding_task_ids` 는 **배열 전체 교체**다: 생략=건드리지 않음, `null`·`[]`=전부 뗀다 | 계약 `modules/work/task_commands.py:52-56`(필드) `61-67`(validator) `110-111`·`124-127`(`TaskUpdateInput`); 라우트 `entrypoints/http.py:1524-1527`; 구현 `modules/work/application.py:558-568` |
| | **MCP `task_update` 는 `preceding_task_ids` 를 받지 않는다** — 인자가 `title/description/start_date/due_date/clear_*/project_id/clear_project` 뿐이다 | `entrypoints/mcp.py:2015-2038` |
| | 한 건씩 붙였다 떼는 전용 명령은 **없다** (설계 의도로 명시) | `modules/work/task_commands.py:52-54` |
| | 요청 수정(`work_request_amend`)·재상신은 선행을 못 바꾼다 — `WorkRequestRevisionInput` 에 그 칸이 없다 | `modules/work/request_commands.py:48-56` |
| 어느 응답이 **내보내나** | **`preceding_task_ids: string[]`(활성만·고른 순서)** — `TaskMutationResult` 의 칸이라 생성·수정·전이·목록·상세 전부에 실린다 | 조립 `modules/work/application.py:2487-2495`; 타입 `modules/work/task_results.py:93`; 목록 `application.py:915,925` |
| | **`predecessors: [{task_id, title, state}]`** — **업무 상세에만** 실린다. `preceding_task_ids` 와 같은 순서·같은 길이. 못 읽는 선행은 `title`·`state` 가 `null` 이고 자리만 남는다 | 조립 `application.py:987`(read_only 갈래) · `2369`(owner 갈래); 구현 `1256-1289`; 타입 `task_results.py:111-121`, `238` |
| | 프로젝트 상세 `tasks[].preceding_task_ids` — 「간트 연결선의 유일한 원천」이라고 주석이 명시 | `modules/work/projects.py:445`; 타입 `modules/work/project_results.py:58-60` |
| | 요청 응답 `preceding_task_ids` — 요청이 세운 업무에서 읽어 온다 | `modules/work/requests.py:1477`; 타입 `modules/work/request_results.py:57-59`; 저장소 `platform/work_tasks.py:2163-2178` |
| | 확인 카드(AX 위임)의 편집 필드 `preceding_task_ids`(label 「선행업무」, `multi_select`, editable) | `platform/actions.py:1779-1788`, 두 번째 자리 `1996-2005` |
| 검증 규칙 — 무엇을 거절하나 | **다섯 거절이고 가르는 순서가 계약이다**: ① 자기 자신 ② 중복 ③ 읽기 권한(→`TaskNotFound`) ④ 프로젝트 불일치 ⑤ 순환. 그 앞에 ⓞ 프로젝트 없음 | `modules/work/application.py:1152-1195` (`_resolve_predecessors`) |
| | **선행은 같은 프로젝트 안에서만 선다** — `project_id` 가 `None` 이면 선행 지정 자체가 성립하지 않는다 | `application.py:1174-1176` |
| | **중복을 조용히 털지 않는다** — pydantic 단계에서 `reference_task_ids` 는 dedupe 하는데 `preceding_task_ids` 는 일부러 안 한다 | `modules/work/task_creation.py:81-91`(주석) vs `39`(참고는 dedupe) |
| | 순환: 활성 변을 BFS 로 걷고 본 것을 다시 보지 않는다. **검사와 저장이 한 transaction** | `application.py:1206-1225`; 저장 `1213`·`568`·`311-312` |
| | 생성 시엔 자기 자신·순환을 **묻지 않는다** (`task_id=None`) — 아직 없는 업무라 성립 불가 | `application.py:1167-1170`, `285-287`, `modules/work/requests.py:405-411` |
| | **남은 선행이 있으면 그 업무의 프로젝트를 바꿀 수 없다** → `TaskProjectLockedByPredecessors`. 자손 전체에 같은 게이트를 **먼저 다 걸고 나서** 옮긴다(부분 이동 금지) | `application.py:529-550`, 게이트 `592-601` |
| | **끝난·취소된 업무를 선행으로 지정하는 것을 막는 규칙을 못 찾았다** — 상태 검사가 `_resolve_predecessors` 에 없다 | `application.py:1178-1194` |
| | 선행 개수 상한·`max_length` 를 **못 찾았다** | `modules/work/task_creation.py:63`, `task_commands.py:56` (둘 다 상한 없음) |
| 오류 코드·예외 클래스·메시지 | `TaskPredecessorProjectRequired` → **422** · 「선행업무를 지정하려면 프로젝트를 먼저 선택해 주세요」 (SPEC 코드명 `WORK_PREDECESSOR_PROJECT_REQUIRED`) | `errors.py:110-115`; 메시지 `application.py:1176`; 매핑은 말미 `TaskError` → 422 `http.py:576` |
| | `TaskPredecessorProjectMismatch` → **422** · 「같은 프로젝트의 업무만 선행으로 지정할 수 있습니다」 | `errors.py:117`; `application.py:1191-1193` |
| | `TaskPredecessorSelf` → **422** · 「자기 자신을 선행으로 둘 수 없습니다」 | `errors.py:121`; `application.py:1180` |
| | `TaskPredecessorDuplicate` → **422** · 「이미 선행으로 지정된 업무입니다」 | `errors.py:128`; `application.py:1182` |
| | `TaskPredecessorCycle` → **422** · 「선행 관계가 서로를 기다리게 됩니다」 | `errors.py:132`; `application.py:1223` |
| | `TaskProjectLockedByPredecessors` → **409** · 「선행업무를 먼저 비워야 프로젝트를 바꿀 수 있습니다: {제목}」 | `errors.py:140`; 매핑 `http.py:552`; 메시지 `application.py:599-601` |
| | `TaskPredecessorsUnfinished`(`InvalidTaskTransition` 하위) → **409** · 「끝나지 않은 선행업무가 있습니다: {최대 3개 제목}」, 읽을 수 있는 게 없으면 이름 없이 「끝나지 않은 선행업무가 있습니다」. `.blocking` 에 `({"title": ...}, …)` 를 달고 있다 | `errors.py:148-161`; 매핑 `http.py:551`; 발생 `modules/work/lifecycle.py:130-140` |
| | 못 읽는 선행 → `TaskNotFound` → **404** 「task was not found」 | `application.py:1185-1189`; 매핑 `http.py:528-529` |
| | **`.blocking` 튜플은 HTTP 본문에 실리지 않는다** — `detail=str(error)` 만 나간다 | `entrypoints/http.py:551`, `564` |
| 방향이 양쪽인가 | **한쪽뿐이다.** 모든 조회가 `task_id.in_(...)` 로만 걸린다 — `predecessors_for` · `active_predecessor_ids` · `predecessor_edges` · `predecessor_task_ids`. `predecessor_task_id == X` 로 거는 문이 **저장소 전체에 하나도 없다** | `platform/work_tasks.py:1128-1153`, `2163-2178`; 전수 grep 결과 §3.1 |
| 깊이·개수 제한 | 개수 제한 없음(위). 순환 검사는 활성 변 BFS 라 사실상 그래프 깊이 전체를 본다 — 깊이 상한 없음 | `application.py:1206-1225` |
| 권한 — 누가 만들고 누가 읽나 | 만들기: `TASK_SELF_MANAGE`(생성·수정 둘 다 이 capability) / 요청 갈래는 `WORK_REQUEST_CREATE` | `application.py:270`, `519` |
| | 선행 후보는 **그 순간 읽을 수 있는 업무**여야 한다 — 못 읽으면 `TaskNotFound` | `application.py:1185-1189` |
| | 읽기: `preceding_task_ids`(id 배열)는 **권한 필터 없이** 실린다. `predecessors`(제목·상태)는 선행마다 `may_read_task` 를 다시 묻고 못 읽으면 `title`·`state` 를 비운다 — **제목은 감추고 건수는 낸다** | `application.py:2487-2495`(무필터) vs `1266-1289`(per-예측자 판정) |
| | **프로젝트 상세는 per-task 권한 필터가 없다** — `tasks_in(project_id)` 가 그 프로젝트의 업무를 전부 내고 각 줄이 `preceding_task_ids` 를 싣는다. 프로젝트 읽기 권한 하나로 그 프로젝트 안 선행 그래프 전체가 나간다 | `platform/projects.py:204-209`; 조립 `modules/work/projects.py:368-405`; 권한은 `PROJECT_READ` 하나 `modules/work/projects.py:359`, `514-516` |
| | 되돌이(선행 사슬) 방지 빗장: 읽기 판정이 부른 상세에서는 선행 요약을 접는다 (`_resolving_predecessor_access`) | `application.py:237-238`, `1256-1264`, `1291-1307` |

### 2.3 참고 (`reference_task_ids` / `task_references`)

| 물음 | 답 | 근거 |
|---|---|---|
| 저장 모양 | **조인테이블 `task_references`**: `id` · `task_id FK→tasks.id NOT NULL index` · `referenced_task_id FK→tasks.id NOT NULL index` · `created_by` · `created_at` · `released_by NULL` · `released_at NULL`. 부분 unique `uq_task_reference_active(task_id, referenced_task_id) WHERE released_at IS NULL` | `platform/persistence.py:1551-1578` (클래스 1551, 제약 1560-1569) |
| | **관계 종류가 없다** — 의미는 `참고` 하나뿐 | `platform/persistence.py:1552-1556`; `docs/domain-model.md:110` |
| | **자기 자신 금지 CHECK 이 없다** (`task_predecessors` 와 다르다) — application 이 답한다 | `platform/persistence.py:1560-1569` vs `1023`; 검사 `modules/work/application.py:2406-2407` |
| | 요청 쪽은 별표: `work_request_references(work_request_id, referenced_task_id)` + `UniqueConstraint uq_work_request_reference`. **`released_at` 이 없다** — 닫는 자리가 없다 | `platform/persistence.py:1581-1591` |
| 어느 엔드포인트가 **받나** — 생성 | `POST /api/tasks` · `POST /api/tasks/assign` · `POST /api/work-requests` · `POST /api/meetings/{id}/todos/{id}/promote` 전부 `reference_task_ids[]` | `entrypoints/http.py:1375`, `1481`, `2011`, `848` |
| | MCP `task_create_self`(1974) · `task_assign`(2010) · `work_request_create`(1638) | `entrypoints/mcp.py` 각 줄 |
| 어느 엔드포인트가 **받나** — 수정 | **전용 엔드포인트 두 개다.** `POST /api/tasks/{id}/references` (본문 `{referenced_task_id}`) · `DELETE /api/tasks/{id}/references/{reference_id}` | `entrypoints/http.py:1681-1697`; 구현 `modules/work/application.py:2403-2437`; 입력 `modules/work/task_commands.py:20-31` |
| | MCP `task_reference_add(task_id, referenced_task_id)` · `task_reference_release(task_id, reference_id)` | `entrypoints/mcp.py:1862`, `1866` |
| | `PATCH /api/tasks/{id}` 는 참고를 못 바꾼다 — `TaskEditFields` 에 칸이 없다 | `modules/work/task_commands.py:45-58` |
| 어느 응답이 **내보내나** | 업무 상세 `references: [{reference_id, created_by, created_at, task: TaskSummaryView \| null}]`. **`access: "owner"` 상세에만 실린다** — `read_only` 갈래(`_related_view`)에는 없다 | 조립 `application.py:2363`(owner 경유 `_with_checklist`); `read_only` 갈래 `application.py:946-1000`(references 없음); 타입 `task_results.py:212-217`, `241`(NotRequired) |
| | 요청 응답 `reference_task_ids: string[]` (무엇을 가리켰는지 자체) + 요청 상세 `references: WorkRequestReferenceView[]` | `modules/work/requests.py:1478-1480`; 타입 `request_results.py:60-62`, `88-90` |
| | 참고 추가 응답 `TaskReferenceResult = {reference_id, created_by, created_at, task, task_version}` | `application.py:2422-2428`; 타입 `task_results.py:315-317` |
| 검증 규칙 — 무엇을 거절하나 | 자기 자신 → `TaskError("a task cannot refer to itself")`; 못 읽는 업무 → `TaskNotFound`(읽는 것 자체가 권한 검사); 이미 있는 활성 연결 → `TaskError("this task already refers to that work")`; 없는 `reference_id` → `TaskNotFound("reference was not found")` | `application.py:2403-2415`, `2427-2433` |
| | 요청 쪽은 「지금 읽을 수 있는 것만」 통과시킨다(`_readable_references`) | `modules/work/requests.py:442` |
| 오류 코드·예외 클래스·메시지 | 전부 `TaskError` → **422** · 영어 메시지 그대로 (`a task cannot refer to itself` / `this task already refers to that work`) · `TaskNotFound` → **404** | 매핑 `entrypoints/http.py:576`, `528-529` |
| | **전용 오류 클래스·코드가 없다** — `TaskPredecessor*` 여섯과 대조적이다 | `modules/work/errors.py` 전체에 reference 전용 클래스 없음 |
| 방향이 양쪽인가 | **한쪽만 나간다.** `references_for(task_id)` 만 있고 「나를 참고로 가리키는 업무」 조회는 **못 찾았다**. 열 자체는 양쪽 index 가 걸려 있으므로 역방향 질의를 쓸 자리는 있다 | 저장소 `platform/work_tasks.py`(`references_for`); 인덱스 `platform/persistence.py:1571-1573` |
| 깊이·개수 제한 | **못 찾았다** (개수 상한 없음, 깊이 개념 없음). 생성 입력에서 **중복만 턴다** | `modules/work/task_creation.py:39` |
| 권한 — 누가 만들고 누가 읽나 | 만들기: `TASK_SELF_MANAGE` + **그 업무를 들고 있어야 한다**(`_holding`) | `application.py:2406`, `_holding` `2343-2349` |
| | **연결은 권한을 주지 않는다** — 매 조회마다 대상 업무를 읽을 수 있는지 다시 묻고, 못 읽으면 `task: null` 로 가린다 | `application.py:2374-2399`; 조립층 한 겹 더 `bootstrap/application.py:908-929` (`access != "owner"` 면 `None`) |

### 2.4 프로젝트 소속 (`project_id`)

| 물음 | 답 | 근거 |
|---|---|---|
| 저장 모양 | `tasks.project_id UUID NULL FK→projects.id`, `index=True`. **비어 있는 것이 정상**이라고 주석이 명시 | `platform/persistence.py:939` |
| | `work_requests.project_id UUID NULL FK→projects.id` — **인덱스를 일부러 두지 않는다**(요청을 프로젝트로 거르는 조회가 아직 없고 기존 표에 인덱스를 더하면 `schema_sync` 가 못 만든다) | `platform/persistence.py:1650-1653` |
| | `projects`: `id·name·description·state(default active)·starts_on·ends_on·external_key unique·created_by_actor_id·version·created_at·updated_at`. **소유 조직 단위 열이 없다** | `platform/persistence.py:838-861` |
| | `project_assignments(project_id, member_id, assignment_kind lead\|member, valid_from/until, ended_*)` + 부분 unique `uq_project_assignment_active WHERE ended_at IS NULL` | `platform/persistence.py:864-894` |
| 어느 엔드포인트가 **받나** — 생성 | `POST /api/tasks` · `POST /api/work-requests` · `POST /api/meetings/.../promote` · MCP `task_create_self`·`work_request_create` | `http.py:1377`, `2008`, `849`; `mcp.py:1979`, `1639` |
| | `POST /api/projects` 로 프로젝트 자체를 만든다; `project_plan_work(project_id, …)` 는 프로젝트를 경로에서 받는다 | `http.py:1394`; `modules/work/assignments.py:155-185`; MCP `mcp.py:1887` |
| | **`POST /api/tasks/assign` · MCP `task_assign` 은 `project_id` 를 받지 않는다** (`TaskAssignmentInput` 에 칸 없음, 과거 잔재는 `read_legacy_empty_project` 가 `null` 만 털어낸다) | `modules/work/task_creation.py:116-129` |
| | **`POST /api/tasks` + `assignee_id` 갈래는 `project_id` 를 명시적으로 거절한다**(422) | `modules/work/creation_commands.py:183` |
| 어느 엔드포인트가 **받나** — 수정 | `PATCH /api/tasks/{id}`: `project_id` + `clear_project` 플래그 | `modules/work/task_commands.py:53`·`111-112`·`120-122`; 구현 `application.py:525-550` |
| | MCP `task_update`: `project_id` · `clear_project` | `entrypoints/mcp.py:2023-2024`, `2032` |
| 어느 응답이 **내보내나** | `TaskMutationResult.project_id: str \| null` — 생성·수정·전이·목록·상세 전부 | `application.py:2470`; 타입 `task_results.py:79` |
| | 요청 응답 `project_id: str \| null` | `modules/work/requests.py:1443`; 타입 `request_results.py:37-38` |
| | `GET /api/projects` → `ProjectView[]`; `GET /api/projects/{id}` → `ProjectDetailResult = ProjectView + {may_manage, members[], tasks[]}` | `modules/work/projects.py:360-372`, `368-405`; 타입 `project_results.py:74-78` |
| | 그래프 엣지 `part_of` (업무→프로젝트) | `modules/work/graph.py:158-164` |
| 검증 규칙 — 무엇을 거절하나 | 읽을 수 없는 프로젝트 → `TaskNotFound("project was not found")` | `application.py:374-380` (`project_for`) |
| | **하위 업무는 프로젝트를 따로 못 갖는다** → `TaskError("하위 업무의 프로젝트는 상위 업무를 따릅니다")` | `application.py:526-528` |
| | **남은 선행이 있으면 프로젝트 변경 불가** → `TaskProjectLockedByPredecessors`(409). 자손 전체를 먼저 다 검사하고 나서 옮긴다 | `application.py:533-550`, `592-601` |
| | 프로젝트를 바꾸면 **자손 전체가 따라 옮겨진다**(직속만 옮기면 손자가 옛 프로젝트에 남아 「선행은 같은 프로젝트」 불변이 깨진다) | `application.py:536-550` |
| | `project_plan_work`: `may_assign_in(project_id)` 아니면 `TaskError("이 프로젝트에 업무를 올릴 수 있는 자격이 없습니다")` | `modules/work/assignments.py:170-172` |
| 오류 코드·예외 클래스·메시지 | `TaskProjectLockedByPredecessors` → **409**; 나머지는 `TaskError` → **422** / `TaskNotFound` → **404**. 프로젝트 모듈 자체 예외는 `ProjectAccessDenied` → **403**, `ProjectNotFound` → **404**, `ProjectError` → **422** | `http.py:552`, `576`, `528-529`, `501-506` |
| 방향이 양쪽인가 | **양쪽.** 업무→프로젝트는 `tasks.project_id`, 프로젝트→업무는 `tasks_in(project_id)` | `platform/projects.py:204-209` |
| 깊이·개수 제한 | 프로젝트당 업무 수 제한·페이징이 **없다** — `tasks_in()` 은 필터도 페이징도 없이 전부 낸다(주석이 D-16 전제로 명시) | `modules/work/projects.py:369-375`; `platform/projects.py:204-209` |
| 권한 — 누가 만들고 누가 읽나 | `PROJECT_MANAGE` — 만들기·사람 붙이기·업무 올리기 | `modules/work/projects.py:153`, `529`; 이름 `organization_access/domain.py:97` |
| | `PROJECT_READ` — 읽기. 읽을 수 있는 범위는 grant 의 project scope 가 정한다(`principal.projects_for(PROJECT_READ)`) | `modules/work/projects.py:359`, `514-516`; 이름 `organization_access/domain.py:99` |
| | **프로젝트 상세는 업무 줄을 per-task 로 걸르지 않는다** (§2.2 마지막 줄과 같은 사실) | `platform/projects.py:204-209` |
| | 업무 읽기 쪽: 「내가 함께 하는 프로젝트의 업무」는 조직 축과 나란히 목록에 들어온다 | `modules/work/application.py:902-908` |

### 2.5 요청 ↔ 수락으로 생긴 업무 (`source_work_request_id` · `supersedes_request_id`)

| 물음 | 답 | 근거 |
|---|---|---|
| 저장 모양 | `tasks.source_work_request_id UUID NULL FK→work_requests.id` + **부분 unique** `uq_tasks_source_work_request WHERE source_work_request_id IS NOT NULL` — 「수락된 요청 하나 = 업무 하나」를 DB 가 답한다 | `platform/persistence.py:901-907`, `925` |
| | `work_requests.supersedes_request_id UUID NULL FK→work_requests.id` + index `ix_work_requests_supersedes_request_id`. 재요청은 **새 요청·새 Task** 이고 이 열이 두 건을 잇는 유일한 연결 | `platform/persistence.py:1687-1689`, 인덱스 `1634` |
| | **연결은 업무 쪽 한 열에만 산다** — 요청 행에 `task_id` 열이 없다 | `platform/work_tasks.py:1793-1794` (주석·구현) |
| | 담당 행에도 같은 이름이 있다: `task_assignments.source_work_request_id UUID NULL FK` · `supersedes_assignment_id UUID NULL`(교체 제안 표식) | `platform/persistence.py:1773`, `1777`, `1202` |
| | 업무의 다른 lineage 열들: `request_thread_id` · `source_decision_item_id` · `source_submission_id` · `source_review_decision_id` · `source_action_item_id` · `source_task_id` · `source_meeting_id` · `source_agenda_id` | `platform/persistence.py:923-932` |
| 어느 엔드포인트가 **받나** — 생성 | **직접 못 받는다.** `source_work_request_id` 는 서버가 쓴다 — `create_task_for_request(request, …)` 가 `source_work_request_id=request.id` 를 박는다 | `platform/work_tasks.py:1965`, `1998` |
| | **업무는 「수락」이 아니라 「발송」이 세운다** — `WorkRequestApplication.create()` 가 같은 transaction 에서 요청 행과 업무를 함께 세우고, 수락은 담당 행 하나만 바꾼다 | `modules/work/requests.py:454-470`; 명시 주석 `platform/work_tasks.py:1820-1826` |
| | `supersedes_request_id` 는 `POST /api/work-requests` 본문이 받는다 (MCP `work_request_create` 는 **받지 않는다**) | `http.py:2012`; `WorkRequestCreateInput` `modules/work/creation_commands.py:107`; MCP 인자 목록 `mcp.py:1633-1646`(없음) |
| 어느 엔드포인트가 **받나** — 수정 | **없다.** 두 값을 바꾸는 명령을 못 찾았다. `WorkRequestRevisionInput` 에도 `TaskEditFields` 에도 칸이 없다 | `modules/work/request_commands.py:48-56`; `modules/work/task_commands.py:45-58` |
| 어느 응답이 **내보내나** | `TaskMutationResult.lineage.source_work_request_id` (그리고 `request_thread_id`·`source_decision_item_id`·`source_submission_id`·`source_review_decision_id`·`source_action_item_id`·`source_task_id`) | `application.py:2500-2508`; 타입 `task_results.py:15-22`, `97` |
| | 업무 상세 `origin: TaskOriginView \| null` — 「어디서 왔는가」 + 행위자 역할. **읽을 수 있을 때만 source 를 싣고 못 읽으면 행위자 라벨만 남긴다** | `application.py:2123-2145`; 타입 `task_results.py:162-173` |
| | 업무 상세 `delivery: TaskDeliveryView \| null` — 요청자가 「내 요청이 어디까지 갔나」를 본다 | `application.py:985`; 타입 `task_results.py:219-227` |
| | 요청 응답 `task_id: str \| null` + `assignment_state` + `supersedes_request_id` | `modules/work/requests.py:1459-1470`; 타입 `request_results.py:51`, `52-53` |
| | 그래프 엣지 `produced` (요청→업무) | `modules/work/graph.py:167-173` |
| | **`source_work_request_id` 는 `TaskVersionRecord.snapshot` 에도 들어간다** | `platform/work_tasks.py:1062` |
| 검증 규칙 — 무엇을 거절하나 | `supersedes_request_id`: 그 요청이 없거나 **내가 그 요청의 요청자(또는 승격 누른 사람)가 아니면** `WorkRequestNotFound` | `modules/work/requests.py:420-427` |
| | 「수락된 요청 하나 = 업무 하나」는 DB 부분 unique 가 답한다 | `platform/persistence.py:901-907` |
| | **수락된 요청 업무는 직접 취소할 수 없다** — 요청자·담당자·관리자 **모두** → `TaskCancelRequiresAgreement`. 출구는 합의 취소 하나 | `application.py:1698-1706`, `1772-1783`; 예외 `errors.py:66` |
| | **요청 업무는 담당자가 완료로 못 끝낸다** → `InvalidTaskTransition("이 업무는 요청자의 확인이 필요합니다. 완료 보고로 제출하세요")`. 판정 근거가 `source_work_request_id is not None` 하나다 | `modules/work/lifecycle.py:143-144`; 판정 `application.py:1521-1523` |
| | 상위 완료의 완결 판정: 요청 하위는 **요청자 승인까지**여야 끝난 것. 승인 행을 못 찾으면 완결로 치지 않는다 | `application.py:1440-1461` (`is_child_settled`) |
| 오류 코드·예외 클래스·메시지 | `TaskCancelRequiresAgreement` → **409**; `WorkRequestNotFound` → 요청 모듈 계열; `WorkRequestIdempotencyConflict`·`WorkRequestNotPending`·`WorkRequestLockedAfterAccept` → **409**; `WorkRejectReasonRequired` → **422**; `WorkRequestAccessDenied` → **403**; `WorkRequestError` → **422** | `http.py:541`, `582-587`, `534` |
| 방향이 양쪽인가 | **양쪽.** 업무→요청은 `lineage.source_work_request_id`, 요청→업무는 `task_for_request(source_work_request_id == request.id)` · `derived_task_ids([requests])` | `platform/work_tasks.py:1793-1794`, `2153-2161`, `976` |
| | 재요청 사슬은 **한쪽뿐이다** — `supersedes_request_id` 로 이전 요청은 찾지만 「나를 supersede 한 요청」 조회를 **못 찾았다**(index 는 있다) | `platform/persistence.py:1634`; 역방향 질의 없음 |
| 깊이·개수 제한 | 재요청 사슬 길이 제한을 **못 찾았다**. 순환 방지 가드도 **못 찾았다** — `supersedes_request_id` 검증은 존재·소유자만 본다 | `modules/work/requests.py:420-427` |
| 권한 — 누가 만들고 누가 읽나 | 만들기: `WORK_REQUEST_CREATE`; 판단: `WORK_REQUEST_DECIDE`; 읽기: `WORK_REQUEST_READ` | `modules/organization_access/domain.py:101-103` |
| | 업무 쪽 read_only 갈래가 여는 두 관계: **요청자**(그 요청을 읽을 수 있으면) · **배정한 사람**(`TASK_ASSIGN` + `assigned_by == me`) | `application.py:952-960` |
| | 요청자의 V-21 읽기 확장은 `WORK_REQUEST_READ` 를 함께 요구한다 | `application.py:436-438` |

---

## 3. 선행·후행 — §4 의 다섯 물음

### 3.1 후행(successor)을 조회하는 길이 있나 — **없다**

- `successor` 라는 식별자·문자열이 `backend/src/ax_workspace/**/*.py` 전체에 **0회**다 (§1 표).
- 선행을 읽는 저장소 문 네 개가 전부 `task_id` 쪽으로만 걸린다:
  - `predecessors_for(task_ids)` — `WHERE task_id IN (...) AND released_at IS NULL ORDER BY position, created_at` (`platform/work_tasks.py:1128-1146`)
  - `active_predecessor_ids(task_id)` — 위를 그대로 감싼다 (`platform/work_tasks.py:1148-1149`)
  - `predecessor_edges(task_ids)` — 「이름만 그래프 쪽」이고 같은 문이다 (`platform/work_tasks.py:1151-1153`)
  - `predecessor_task_ids(task_id)` (요청 저장소) — `WHERE task_id = ? AND released_at IS NULL` (`platform/work_tasks.py:2163-2178`)
- `predecessor_task_id` 를 **필터 조건으로** 쓰는 문이 코드 전체에 없다. `grep -rn "predecessor_task_id ==\|predecessor_task_id\.in_"` 의 결과는 세 줄인데 모두 SELECT 대상 컬럼·dict 키·enumerate 변수다 (`platform/work_tasks.py:1137`, `1145`, `1177`).
- 그래서 **「나를 선행으로 삼는 업무들」을 내주는 엔드포인트·필드가 없다.** 업무 상세(`predecessors`) · 업무 목록(`preceding_task_ids`) · 요청 응답(`preceding_task_ids`) 모두 「내 선행」만 낸다.
- 유일한 우회로는 **프로젝트 상세**다: `GET /api/projects/{id}` 의 `tasks[]` 가 그 프로젝트 업무 **전부**에 대해 `preceding_task_ids` 를 싣기 때문에, 화면이 그 배열을 뒤집으면 후행을 얻는다. 그것이 설계 의도로 적혀 있다 — 「**싣지 않는 것도 계약이다**: 하위 집계·**후행 배열**·「분류」·저장된 진행률·승인 값은 없다. 화면이 세거나(하위·후행) 만들지 않기로 한 것」 (`modules/work/projects.py:429-431`).
- 관계 그래프(`modules/work/graph.py:145-208`)도 후행을 모른다. `_task_neighbors` 가 내는 엣지는 `holds`·`part_of`(프로젝트)·`produced`(요청)·`parent_of`(양방향)·`refers_to`(참고)·자료·보고서 뿐이고 **선행/후행 엣지가 없다**.
- `predecessor_task_id` 단독 인덱스도 없으므로, 역방향 조회를 만들 때 인덱스가 하나 더 필요하다는 사실만 기록한다 (`platform/persistence.py:1014-1025`).

### 3.2 blocking 계산이 어디서 나나

프론트의 `blockingPredecessors`·`startBlockedByPredecessors` 는 **서버 필드가 아니다.** 둘 다 `predecessors[]` 를 프론트가 접어 만든다.

- `blockingPredecessorsOf(task)` = `task.predecessors` 중 `title !== null && state !== "done" && state !== "cancelled"` (`frontend/src/features/work/workRows.ts:113-117`)
- `startBlockedByPredecessors(task)` = `task.state === "open" && blockingPredecessorsOf(task).length > 0` (`frontend/src/features/work/workRows.ts:142-144`)
- 그러니까 **대응하는 서버 값은 업무 상세의 `predecessors: [{task_id, title, state}]` 하나**이고, 그것을 싣는 응답은 `GET /api/tasks/{id}`(그리고 MCP `task_get`) 뿐이다 (`modules/work/application.py:987`·`2369`; 타입 `modules/work/task_results.py:238`).
- 서버가 같은 판정을 **따로** 한다. 다만 그 결과는 응답에 실리지 않고 **전이 거절로만** 나간다:
  - `_blocking_predecessors(task)` — 활성 선행 중 `done`·`cancelled` 가 아닌 것 (`modules/work/application.py:1244-1254`)
  - `_predecessor_gate(task, principal)` → `TaskPredecessorGate(blocks: bool, unfinished_titles: tuple[str,...])`. **막을지는 선행 전부로 정하고, 이름은 읽을 수 있는 것만** 낸다 (`modules/work/application.py:1227-1242`; 값 객체 `modules/work/lifecycle.py:56-69`)
  - `transition()` 이 업무 행을 **잠근 뒤에** 그 게이트를 세워 `transition_task(...)` 에 넘긴다 — 판정과 전이가 한 transaction (`modules/work/application.py:1708`, `1740`)
  - `transition_task` 가 거는 자리는 **`open` 에서 나가는 두 문뿐이다**: `open → in_progress`, `open → done`. `in_progress → done`·`blocked → in_progress`·취소에는 걸지 않는다 (`modules/work/lifecycle.py:130-133`, 이유는 `111-128` docstring)
- 이름이 비슷한 **서버 필드**는 하나 있는데 **선행이 아니라 하위**다: `derived.blocking_children: [{task_id, title, why}]` (`why` = `unfinished` \| `awaiting_approval`), 그리고 `child_progress.blocking: int` (`modules/work/application.py:1044-1052`, `1398`; 타입 `modules/work/task_results.py:25-31`, `44`, `188`). 선행에 해당하는 필드는 **없다** — 코드가 「하위는 완료를, 선행은 시작을 막는다」로 두 축을 일부러 가른다 (`modules/work/errors.py:150-156`).

### 3.3 선행이 업무 상세 응답에 실리나 — **실린다, 두 필드로**

- `preceding_task_ids: string[]` — **활성만, 고른 순서**(`position, created_at`). `TaskMutationResult` 의 칸이라 생성·수정·전이·**목록**·상세 전부에 실린다. 권한 필터 없음 (`modules/work/application.py:2485-2495`; 타입 `modules/work/task_results.py:90-93`).
- `predecessors: [{task_id, title, state}]` — **업무 상세에만**. `preceding_task_ids` 와 **같은 순서·같은 길이**가 계약이고, 못 읽는 선행은 `title`·`state` 가 `null` 이 되어 **자리만 남는다**(「제목은 감추고 건수는 낸다 — 배열 길이가 그 건수다」) (`modules/work/application.py:1266-1289`; 타입 `modules/work/task_results.py:111-121`, `237-238`).
- **`access: "read_only"` 상세에도 `predecessors` 가 실린다** (`application.py:987`) — `references` 는 owner 갈래에만 실리는 것과 다르다 (`application.py:2363` vs `946-1000`).
- 목록(`GET /api/tasks`)은 `predecessors` 를 **싣지 않는다** — id 배열만이다 (`application.py:915-931`).
- 따로 받아야 하는 경우는 하나뿐이다: **후행**. §3.1 대로 프로젝트 상세(`GET /api/projects/{id}` → `tasks[].preceding_task_ids`)에서 뒤집어야 한다 (`modules/work/projects.py:445`).
- 참고로 요청 상세(`GET /api/work-requests/{id}`)도 `preceding_task_ids` 를 내는데, 값은 **그 요청이 세운 업무**에서 읽어 온다 (`modules/work/requests.py:1477`; 저장소 `platform/work_tasks.py:2163-2168`).

### 3.4 순환·자기참조를 막나 — **막는다. 상위보다 촘촘하다**

| | 상위(`parent_task_id`) | 선행(`task_predecessors`) |
|---|---|---|
| 자기참조 — DB | 없음 | **CHECK `ck_task_predecessors_not_self`** (`platform/persistence.py:1023`) |
| 자기참조 — application | `TaskParentCycle`(자기 자신 **또는 자기 조상**) (`application.py:408-411`) | `TaskPredecessorSelf` (`application.py:1179-1180`) |
| 중복 — DB | (관계가 한 열이라 성립 안 함) | **부분 unique `uq_task_predecessors_active`** (`platform/persistence.py:1015-1022`) |
| 중복 — application | — | `TaskPredecessorDuplicate` (`application.py:1181-1182`) |
| 순환 | `_ancestor_ids(parent)` 한 줄 조상 사슬 검사 (`application.py:448-459`) | `_require_no_predecessor_cycle` — 활성 변 BFS (`application.py:1206-1225`) |
| 순환 예외 | `TaskParentCycle` → **422** | `TaskPredecessorCycle` → **422** |
| 저장과 같은 transaction 인가 | 그렇다 (조립층이 한 session) | **그렇다 — 명시적 계약이다** (`application.py:1210-1213`, 저장 `1213`·`566-568`) |
| 무한 순회 방지 | 「본 것을 다시 보지 않는다」 (`application.py:450-459`) | 같다 (`application.py:1216-1225`) |

추가로 선행에만 있는 게이트: **프로젝트 잠금** — 남은 선행이 있으면 그 업무(및 상위를 따라 옮겨지는 자손)의 프로젝트를 바꿀 수 없다 (`TaskProjectLockedByPredecessors`, 409) (`application.py:529-550`, `592-601`).
생성 시엔 자기참조·순환을 **묻지 않는다** — 업무가 아직 없어서 성립하지 않는다(`task_id=None`) (`application.py:1167-1170`, `285-287`; 요청 갈래 `modules/work/requests.py:405-411`).

### 3.5 끝난 업무·취소된 업무가 선행으로 남아 있을 때

- **막지 않는다.** `_blocking_predecessors` 가 `done`·`cancelled` 를 건너뛴다 — 남은 선행이 전부 완료거나 취소면 게이트가 열린다 (`modules/work/application.py:1244-1254`, 특히 `1250-1252`). `TaskPredecessorGate` docstring 이 「취소된 선행은 막지 않는다 (SPEC-001 U-14)」로 명시 (`modules/work/lifecycle.py:63-64`).
- **행은 그대로 남고 `preceding_task_ids`·`predecessors` 에도 계속 실린다.** 활성 여부만 보고 상태는 안 본다 (`application.py:2487-2495`, `1266-1289`) — 그래서 상세에 `state: "cancelled"` 인 선행 줄이 남는다. 프론트가 그것을 걸러 내고 있다 (`frontend/src/features/work/workRows.ts:115`).
- **끝난·취소된 업무를 새로 선행으로 지정하는 것을 막는 규칙은 못 찾았다** — `_resolve_predecessors` 의 검사 다섯에 상태 항목이 없다 (`application.py:1178-1194`).
- **선행이 취소·완료되었을 때 관계 행을 자동으로 닫는 경로도 못 찾았다.** `released_at` 을 세우는 자리는 `replace_predecessors` 하나뿐이고, 그건 사람이 부른 `PATCH /api/tasks/{id}` 배열 교체다 (`platform/work_tasks.py:1155-1192`).
- 한 번 시작한 뒤 선행이 다시 열려도 **되돌리지 않는다** — `blocked → in_progress`(재개)에 게이트를 걸지 않는 이유가 그것이라고 명시돼 있다 (`modules/work/lifecycle.py:122-125`).
- 취소된 업무 자체는 수정 불가라 그 업무의 선행 배열을 비울 수 없다 — `TaskError("cancelled tasks cannot be edited")` (`application.py:522-523`).

---

## 4. 응답 shape 원문

요약하지 않고 그대로 붙인다.

### 4.1 `TaskMutationResult` 중 관계가 실리는 부분 — `modules/work/task_results.py:66-98`

```python
class TaskMutationResult(TypedDict):
    task_id: str
    title: str
    #: **넷뿐이다** — `open` · `in_progress` · `done` · `cancelled`.
    state: str
    version: int
    block_reason: str | None
    description: str | None
    start_date: str | None
    due_date: str | None
    created_at: str | None
    updated_at: str | None
    organization_unit_id: str | None
    project_id: str | None
    origin_kind: str
    visibility: str
    #: `direct` | `request_rejected` | `request_withdrawn` | `cancellation_agreed`
    cancel_reason: str | None
    #: **실제** 시작 시각. `start_date`(계획)와 다른 사실이다.
    started_at: str | None
    completed_at: str | None
    reopened_at: str | None
    assignment: TaskAssignmentView | None
    #: 참조자 — **읽기와 논의만** 열린다. 업무 요청의 같은 이름과 같은 뜻이다 (`modules/work/parties.py`).
    cc_member_ids: list[str]
    #: **선행업무 — 활성인 것만** (SPEC-001 §4 Data Contract). 상위·참고와 다른 세 번째 관계이고
    #: **간트 연결선의 유일한 원천**이다. 뗀 관계는 행으로 남지만 여기 서지 않는다.
    preceding_task_ids: list[str]
    #: 승인자 0..1 — 화면 라벨은 「결재자」고 같은 값이다 (SPEC-001 §7 OQ-N).
    approver_id: str | None
    derived: TaskDerivedView | None
    lineage: TaskLineageView
```

### 4.2 `TaskDetailResult` — `modules/work/task_results.py:229-242`

```python
class TaskDetailResult(TaskMutationResult):
    origin: TaskOriginView | None
    assignee: TaskMemberView | None
    parent: TaskParentView | None
    children: list[TaskSummaryView]
    child_progress: TaskChildProgressView
    delivery: TaskDeliveryView | None
    access: Literal['owner', 'read_only']
    #: 각 선행의 제목·상태. `preceding_task_ids` 와 **같은 순서·같은 길이**다.
    predecessors: list[TaskPredecessorView]
    checklist: NotRequired[list[ChecklistItemView]]
    checklist_progress: NotRequired[TaskProgressView]
    references: NotRequired[list[TaskReferenceView]]
```

### 4.3 관계 하위 타입들 — `modules/work/task_results.py:15-31`, `111-121`, `199-217`

```python
class TaskLineageView(TypedDict):
    request_thread_id: str | None
    source_work_request_id: str | None
    source_decision_item_id: str | None
    source_submission_id: str | None
    source_review_decision_id: str | None
    source_action_item_id: str | None
    source_task_id: str | None


class TaskBlockingChildView(TypedDict):
    """상위 완료를 막는 하위 하나 — 이름을 내야 사람이 다음 걸음을 고른다."""

    task_id: str
    title: str
    #: `unfinished`(아직 안 끝남) | `awaiting_approval`(끝났지만 요청자 승인 전)
    why: str
```

```python
class TaskPredecessorView(TypedDict):
    """선행 하나의 요약. **볼 수 없는 선행은 `title`·`state` 가 비고 자리만 남는다** (SPEC-001 §4).

    자료 구획과 다르다: 자료는 건수도 내지 않지만 선행은 **시작을 막는 이유**라, 이유를 숨기면
    사람이 다음 걸음을 고를 수 없다. **제목은 감추고 건수는 낸다** — 배열 길이가 그 건수다.
    """

    task_id: str
    title: str | None
    state: str | None
```

```python
class TaskParentView(TypedDict):
    task_id: str
    title: str
    state: str


class TaskSummaryView(TaskParentView):
    due_date: str | None
    assignee: TaskMemberView | None
    #: 하위 한 줄도 자기 파생 표시를 갖는다 — 승인 대기인지 아닌지가 그 줄에서 읽혀야 한다.
    derived: NotRequired[TaskDerivedView | None]


class TaskReferenceView(TypedDict):
    reference_id: str
    created_by: str
    created_at: str | None
    task: TaskSummaryView | None
```

### 4.4 `TaskDerivedView` / `TaskChildProgressView` — `modules/work/task_results.py:34-47`, `180-190`

```python
class TaskDerivedView(TypedDict):
    """**서버가 만드는 파생 표시** (SPEC-003 §4 Data). 화면이 `state` 로 되짚지 않는다.

    `reply`·`status_note` 는 **키만 있고 값은 `null`** 이다 — SPEC-001 에서 이어받은 이름이지만 그
    원장(문의·회신 대기·상태 메모)이 아직 구현되지 않았다. 없는 것을 있다고 내지 않는다.
    """

    assignment: str | None
    approval: str | None
    proposal: str | None
    blocking_children: list[TaskBlockingChildView]
    reply: str | None
    status_note: str | None
    overdue_days: int | None
```

```python
class TaskChildProgressView(TypedDict):
    """하위 진행 — `blocking` 이 0이어야 상위를 끝낼 수 있다.

    **`blocking=0` 이 완료를 보장하지는 않는다**: 이 숫자는 읽을 수 있는 하위만 센 투영이고, 완료를
    막는 검사는 읽을 수 없는 하위까지 본다. 화면은 이 값으로 단추를 열되 409 를 정상 응답으로 받는다.
    """

    done: int
    blocking: int
    cancelled: int
    total: int
```

### 4.5 `_view()` 가 관계를 싣는 자리 (원문) — `modules/work/application.py:2469-2508`

```python
            "organization_unit_id": getattr(task, "organization_unit_id", None),
            # 어느 프로젝트의 일인가. 비어 있는 것이 정상이다.
            "project_id": _str(getattr(task, "project_id", None)),
```
```python
            # **선행업무 — 활성인 것만** (SPEC-001 §4). 뗀 것은 빠진다. 상위(`parent_task_id`)·
            # 참고(`references`)와 **다른 줄**이다: 한 배열에 섞으면 무엇이 시작을 막는지가 사라진다.
            "preceding_task_ids": [
                str(item)
                for item in (
                    preceding_task_ids
                    if preceding_task_ids is not None
                    else self.repository.active_predecessor_ids(task.id)
                )
            ],
```
```python
            "lineage": {
                "request_thread_id": _str(getattr(task, "request_thread_id", None)),
                "source_work_request_id": _str(getattr(task, "source_work_request_id", None)),
                "source_decision_item_id": _str(getattr(task, "source_decision_item_id", None)),
                "source_submission_id": _str(getattr(task, "source_submission_id", None)),
                "source_review_decision_id": _str(getattr(task, "source_review_decision_id", None)),
                "source_action_item_id": _str(getattr(task, "source_action_item_id", None)),
                "source_task_id": _str(getattr(task, "source_task_id", None)),
            },
```

### 4.6 `_hierarchy_view()` 원문 — `modules/work/application.py:1392-1398`

```python
        return {
            "parent": self._parent_summary(principal, task),
            "children": children,
            # `done` 은 **완결한 하위**다 — 취소는 따로 세고, `blocking` 이 0이어야 상위를 끝낼 수 있다.
            # 같은 `is_child_settled()` 판정을 쓰므로 이 숫자와 완료 거절이 어긋나지 않는다.
            "child_progress": {"done": settled, "blocking": blocking, "cancelled": cancelled, "total": len(children)},
        }
```

### 4.7 `predecessor_views()` 원문 — `modules/work/application.py:1266-1289`

```python
    def predecessor_views(self, principal: Principal, task_ids: list[UUID]) -> dict[UUID, list[dict[str, Any]]]:
        """선행 요약 — 제목과 상태. **볼 수 없는 선행은 제목 없이** 자리만 남는다 (SPEC-001 §4).

        자료 구획과 다르다: 자료는 건수도 내지 않지만, 선행은 **시작을 막는 이유**라 이유를 숨기면
        사람이 다음 걸음을 고를 수 없다. 그래서 **제목은 감추고 건수는 낸다** — 배열 길이가 그 건수다.
        """
        edges = self.repository.predecessors_for(task_ids)
        views: dict[UUID, list[dict[str, Any]]] = {}
        readable: dict[UUID, bool] = {}
        for task_id, predecessor_ids in edges.items():
            rows: list[dict[str, Any]] = []
            for predecessor_id in predecessor_ids:
                if predecessor_id not in readable:
                    readable[predecessor_id] = self._may_read_predecessor(principal, predecessor_id)
                node = self.repository.task_by_id(predecessor_id) if readable[predecessor_id] else None
                rows.append(
                    {
                        "task_id": str(predecessor_id),
                        "title": str(node.title) if node is not None else None,
                        "state": _external_state(node.state) if node is not None else None,
                    }
                )
            views[task_id] = rows
        return views
```

### 4.8 목록 응답이 관계를 싣는 자리 (원문) — `modules/work/application.py:912-931`

```python
        # 목록 한 줄마다 같은 질의를 반복하지 않는다 — 파생 표시를 한 번에 계산해 나눠 싣는다.
        derived = self._derived_for(tasks, readable_ids={task.id for task in tasks})
        cc = self.repository.cc_members_for([task.id for task in tasks])
        preceding = self.repository.predecessors_for([task.id for task in tasks])
        views = []
        for task in tasks:
            done, total = progress.get(task.id, (0, 0))
            views.append(
                {
                    **self._view(
                        task,
                        derived=derived.get(task.id),
                        cc_member_ids=cc.get(task.id, []),
                        preceding_task_ids=preceding.get(task.id, []),
                    ),
                    "checklist_progress": {"done": done, "total": total},
                    "origin": origins.get(task.id),
                    "assignee": assignees.get(task.id),
                }
            )
        return views
```

### 4.9 프로젝트 상세 업무 줄 — `modules/work/project_results.py:49-70` + 조립 `modules/work/projects.py:443-445`

```python
class ProjectTaskView(TypedDict):
    task_id: str
    title: str
    #: **밖으로 나가는 상태는 계약의 넷뿐**이다 (SPEC-005 §2.9 · 어긋남 ①). `completion_submitted` 는
    #: 투영이 `done` 으로 접어 새지 않는다 — 업무 상세가 내는 값과 같은 값이다.
    state: str
    start_date: str | None
    due_date: str | None
    parent_task_id: str | None
    #: **간트 연결선의 유일한 원천** (SPEC-001 U-15 · §4). 이 줄이 함께 내므로 선행을 묻는 조회를
    #: 따로 만들지 않는다. 상위–하위는 다른 그림이라 `parent_task_id` 와 섞지 않는다.
    preceding_task_ids: list[str]
```
```python
            "parent_task_id": str(task.parent_task_id) if task.parent_task_id else None,
            "preceding_task_ids": [str(item) for item in preceding],
```
그리고 「싣지 않는 것도 계약이다」 원문 — `modules/work/projects.py:427-431`:
```python
        """프로젝트 상세의 업무 한 줄. **화면의 모든 칸이 이 배열에서 나온다** (SPEC-005 §4).

        **싣지 않는 것도 계약이다**: 하위 집계·후행 배열·「분류」·저장된 진행률·승인 값은 없다.
        화면이 세거나(하위·후행) 만들지 않기로 한 것(진행률 저장)이라 서버가 또 내면 원천이 둘이 된다.
        """
```

### 4.10 요청 응답이 관계를 싣는 부분 — `modules/work/request_results.py:52-62` + 조립 `modules/work/requests.py:1465-1481`

```python
    parent_task_id: str | None
    supersedes_request_id: str | None
    #: 내가 이 항목을 목록에서 정리했는가. **서버가 답한다** — 화면의 기억은 새로 열면 사라진다.
    list_entry_hidden: bool
    conditions: dict[str, JsonValue] | None
    #: **이것이 끝나야 시작한다** — 요청이 세운 업무의 선행이다 (SPEC-001 §4). 생성 입력으로 받던
    #: 값이 조회로 돌아오지 않아 상세에서 「무엇 다음인가」를 그릴 수 없었다.
    preceding_task_ids: list[str]
    #: 함께 보낸 참고 업무. `references` 는 그 업무를 **지금 읽을 수 있을 때만** 내용까지 내지만,
    #: 이 목록은 무엇을 가리켰는지 자체다.
    reference_task_ids: list[str]
```
```python
            # 하위 요청이면 발송 때 정해진 상위. 재요청이면 이전 요청.
            "parent_task_id": str(request.parent_task_id) if getattr(request, "parent_task_id", None) else None,
            "supersedes_request_id": (
                str(request.supersedes_request_id) if getattr(request, "supersedes_request_id", None) else None
            ),
```
```python
            # 선행은 **요청이 세운 업무**에서 읽는다 — 요청 행은 순서를 따로 갖지 않는다.
            "preceding_task_ids": [str(item) for item in self._repository.predecessor_task_ids(derived)],
            "reference_task_ids": [
                str(row.referenced_task_id) for row in self._repository.request_references(request.id)
            ],
```

### 4.11 선행 게이트가 거는 자리 (원문) — `modules/work/lifecycle.py:130-140`

```python
    if predecessors.blocks and task.state is TaskState.OPEN and command.target in {
        TaskState.IN_PROGRESS,
        TaskState.DONE,
    }:
        names = ", ".join(predecessors.unfinished_titles[:3])
        # **409 다** — 명령 자체는 말이 되는데 지금 그 업무의 상태가 받지 않는다
        # (SPEC-001 Case Matrix `WORK_PREDECESSORS_UNFINISHED`). 미완 하위와 **다른 코드**다.
        raise TaskPredecessorsUnfinished(
            f"끝나지 않은 선행업무가 있습니다: {names}" if names else "끝나지 않은 선행업무가 있습니다",
            tuple({"title": title} for title in predecessors.unfinished_titles),
        )
```

### 4.12 `task_predecessors` 스키마 원문 — `platform/persistence.py:1013-1045`

```python
    __tablename__ = "task_predecessors"
    __table_args__ = (
        Index(
            "uq_task_predecessors_active",
            "task_id",
            "predecessor_task_id",
            unique=True,
            sqlite_where=text("released_at IS NULL"),
            postgresql_where=text("released_at IS NULL"),
        ),
        CheckConstraint("task_id <> predecessor_task_id", name="ck_task_predecessors_not_self"),
        Index("ix_task_predecessors_task_id", "task_id"),
    )

    id: Mapped[UUID] = mapped_column(Uuid(as_uuid=True), primary_key=True, default=uuid4)
    #: 뒤에 오는 업무 — 이 업무의 **시작**이 막힌다.
    task_id: Mapped[UUID] = mapped_column(ForeignKey("tasks.id"), nullable=False)
    #: 먼저 끝나야 하는 업무. **같은 프로젝트 안**이라는 것은 application 이 답한다.
    predecessor_task_id: Mapped[UUID] = mapped_column(ForeignKey("tasks.id"), nullable=False)
    #: **고른 순서.** 한 번의 교체가 여러 행을 같은 시각에 세우므로 `created_at` 으로는 순서가 갈리지
    #: 않는다 — 그러면 화면이 고른 차례와 조회가 내는 차례가 매번 달라진다. 상세의 요약 배열이
    #: `preceding_task_ids` 와 **같은 순서**여야 한다는 계약(§4)이 이 열 위에 선다.
    position: Mapped[int] = mapped_column(nullable=False, default=0)
    created_by: Mapped[str] = mapped_column(String(100), nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    #: 뗀 시각. 비어 있으면 **활성**이고, 활성 행만 투영과 시작 게이트가 본다.
    released_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
    released_by: Mapped[str | None] = mapped_column(String(100))
```

---

## 5. 계약과 문서가 어긋나 보이는 곳

판정하지 않고 「이렇게 보인다」로만 적는다.

1. **`docs/domain-model.md` 에 `task_predecessors` 행이 없어 보인다.** `grep -n "predecessor" docs/domain-model.md` 가 0건이고 「선행」도 안 나온다 (`task_references` 는 `docs/domain-model.md:110`, `task_schedules` 는 `:113` 에 각각 한 줄이 있다). `AGENTS.md`/role 규칙은 「새 모듈·새 표는 `docs/domain-model.md` 대조표에 한 줄 추가한다」인데 이 표는 그 한 줄이 없어 보인다.

2. **HTTP 오류 본문에 SPEC 코드명이 없어 보인다.** `WORK_PREDECESSOR_PROJECT_REQUIRED` 등 여섯 코드명은 `modules/work/errors.py:110-161` docstring 에만 있고, HTTP 로 나가는 것은 `detail=str(error)` 즉 한국어 문장 하나다 (`entrypoints/http.py:551`, `564`, `576`). 같은 파일 안에서 회의실 예약은 `detail={"code":…, "message":…}` 구조를 쓴다 (`entrypoints/http.py:511-517`, `520-527`) — 두 모양이 섞여 있어 보인다.

3. **`TaskPredecessorsUnfinished.blocking` 이 응답에 실리지 않아 보인다.** 예외는 `blocking: tuple[dict[str,str], ...]` 을 들고 있는데(`modules/work/errors.py:159-161`) 매핑이 `str(error)` 만 쓴다(`entrypoints/http.py:551`). 같은 모양의 `TaskChildrenUnfinished` 도 같다(`errors.py:61-63`).

4. **MCP 와 HTTP 의 편집 계약이 갈려 보인다.** `PATCH /api/tasks/{id}` 는 `preceding_task_ids`·`approver_id`·`clear_approver` 를 받는데(`modules/work/task_commands.py:110-113`), MCP `task_update` 는 그 셋을 인자로 갖지 않는다(`entrypoints/mcp.py:2015-2038`). AX 위임 turn 의 확인 카드는 `preceding_task_ids` 를 편집 필드로 내고 있다(`platform/actions.py:1783`) — 즉 MCP 표면에서 생성은 선행을 받고 수정은 못 받는 모양으로 보인다.

5. **`TaskVersionRecord.snapshot` 에 선행·상위·프로젝트가 없어 보인다.** `task_snapshot()` 이 담는 것은 `title·description·state·block_reason·start_date·due_date·created_by_actor_id·source_work_request_id·assignment·checklist·materials·references·children` 이다 (`platform/work_tasks.py:1054-1077`). `preceding_task_ids`·`parent_task_id`·`project_id` 가 없어서 「그 회차에 선행이 무엇이었나」를 이력에서 복원할 수 없어 보인다. 이어서 `_DIFFABLE_FIELDS = ("title","description","state","block_reason","start_date","due_date")` 이고 컬렉션 diff 는 `checklist`·`materials` 뿐이라(`modules/work/application.py:2580`, `2604-2606`), `TaskChangesView` 에도 선행·참고·상위 항목이 없다(`modules/work/task_results.py:286-295`). 다만 `record_activity` 는 `task.updated` 요약에 바뀐 키 이름을 넣으므로 활동 로그에는 `preceding_task_ids` 라는 글자가 남는다(`application.py:589-592`).

6. **프로젝트 상세의 선행 노출이 업무 상세보다 넓어 보인다.** 업무 상세는 선행마다 `may_read_task` 를 다시 묻고 못 읽으면 제목을 가린다(`application.py:1276-1288`). 프로젝트 상세는 `tasks_in(project_id)` 로 그 프로젝트 업무 전부를 내고(`platform/projects.py:204-209`) 줄마다 `preceding_task_ids` 를 싣는다(`modules/work/projects.py:445`) — per-task 권한 필터가 보이지 않아, `PROJECT_READ` 하나로 그 프로젝트의 업무 제목과 선행 그래프가 다 나가는 모양으로 보인다.

7. **관계 그래프가 선행을 모르는 것으로 보인다.** `_task_neighbors` 가 `holds`·`part_of`·`produced`·`parent_of`·`refers_to`·자료·보고서 엣지를 내는데(`modules/work/graph.py:145-208`) 선행 엣지가 없다. 「업무 구조」를 그래프로 본다는 화면과 어긋나 보인다.

8. **생성 표면들이 받는 값이 서로 다르다.** 같은 「업무 하나 만들기」인데 —
   - `POST /api/tasks`(본인): 선행 ○ 상위 ○ 프로젝트 ○ 참고 ○ cc ○ 결재자 ○ (`http.py:1370-1382`)
   - `POST /api/tasks` + `assignee_id`(남에게): 선행 ✕(422) 상위 ✕(422) 프로젝트 ✕(422) 시작일 ✕(422), 참고·cc·결재자는 ○ (`modules/work/creation_commands.py:168-198`)
   - `POST /api/tasks/assign`: 선행 ✕(칸 없음) 프로젝트 ✕ cc ✕ 결재자 ✕, 상위 ○ 참고 ○ (`modules/work/task_creation.py:112-129`)
   - `project_plan_work`: 넷만 받는다 — `title·description·start_date·due_date` (`modules/work/project_commands.py:51-56`)
   `platform/actions.py:1781` 주석은 「선행 배열은 생성 계약의 일부라 **모든 생성 표면에 함께 선다**(SPEC-001 §5 표면 일치)」인데, 실제로는 두 생성 표면이 안 받는 것으로 보인다.

9. **`work_request_references` 에 `released_at` 이 없어 보인다.** `task_references` 는 「행을 지우지 않고 닫는다」인데(`platform/persistence.py:1576-1578`) 요청 쪽 같은 표는 닫는 열이 없다(`platform/persistence.py:1581-1591`) — 두 표의 보존 규칙이 갈려 보인다.

10. **`supersedes_request_id` 에 순환·사슬 길이 가드가 없어 보인다.** 검증은 존재와 소유자만 본다(`modules/work/requests.py:420-427`). A 가 B 를, B 가 A 를 supersede 하는 배치를 막는 코드를 못 찾았다. `parent_task_id`·`preceding` 에는 순환 가드가 있어서 셋의 규율이 갈려 보인다.

11. **`derived.reply`·`derived.status_note` 는 키만 있고 값이 항상 `null` 이다** — 코드가 스스로 「그 원장이 이 코드에 아직 없다」고 적고 있다 (`modules/work/application.py:1053-1054`; 타입 주석 `modules/work/task_results.py:35-39`). 문서가 이름을 쓰고 있으면 값이 있는 것으로 읽힐 수 있어 보인다.

12. **`POST /api/tasks` + `assignee_id` 갈래의 거절 문구가 필드 이름을 그대로 낸다** — 「담당을 지정한 생성에는 쓸 수 없는 항목입니다: start_date, parent_task_id, project_id, preceding_task_ids」 (`modules/work/creation_commands.py:195-197`). 다른 거절은 한국어 라벨을 쓰는데 이 하나는 API 필드명이라 화면에 그대로 나가면 어긋나 보인다.

---

## 6. 조사 한계

- **읽기 전용이다.** 테스트를 돌리지 않았고 서버·DB 를 띄우지 않았다. 브리프 지시 그대로다. 그래서 **런타임 실제 응답을 확인하지 않았다** — 위 모든 shape 은 TypedDict 정의와 조립 코드를 읽어 맞춘 것이다.
- `backend/tests/` 는 **조사 범위 밖이라 전수조사하지 않았다.** 후행 조회 유무 확인을 위해서만 `grep` 을 한 번 돌렸고(`tests/contract/test_task_predecessors.py`·`tests/integration/postgres/test_work003_constraints_postgres.py` 에 「후행」이 테스트 **제목 문자열**로만 나온다), 테스트가 계약을 더 좁게 고정하고 있는지는 안 봤다.
- 프론트엔드는 §3.2 의 서버 대응값 확인을 위해 `frontend/src/features/work/workRows.ts` 두 함수만 읽었다. FE 전반은 frontend 워커 몫이다.
- **문서 SSOT(`para/projects/summer-star/strong-hajin/` 의 baseline·SPEC·ERD)를 읽지 않았다.** 브리프가 그 절대경로를 주지 않았다. 그래서 §5 는 **코드 안 docstring 이 자기 SPEC 절을 인용한 것**과 리포 안 `docs/` 만 대조한 결과다 — SPEC 원문과의 어긋남은 확인하지 못했다.
- `docs/unified-operations-inventory.json` 은 `preceding_task_ids` 를 49회 담고 있어 캡처가 돼 있음은 확인했지만(`docs/unified-operations-inventory.json:8801` 등), 각 operation 의 스키마가 현재 코드와 일치하는지는 대조하지 않았다 (`make test` 계열을 돌리지 않았으므로 drift 검사가 안 돌았다).
- 심볼 개수는 `grep -rho <심볼>` 의 **토큰 출현 횟수**다. 부분 문자열 포함이므로 `predecessor` 는 `predecessor_task_id`·`predecessors_for`·`TaskPredecessorRecord` 같은 이름 안의 출현을 모두 센다. 「같은 심볼이 한 줄에 두 번」도 두 번 센다. §1 표는 그 기준이고, `grep -c` 기준 줄 수는 값이 더 작다.
- `supersedes` 는 접두 검색이라 `supersedes_request_id`(요청 사슬)와 `supersedes_assignment_id`(담당 교체 제안) 둘을 함께 센다. §2.5 에서 갈라 적었다.
- `git status` 를 조사 시작 시점 그대로 두었다 — 커밋·push·PR 을 하지 않았고 워크트리에 코드 변경이 없다.
