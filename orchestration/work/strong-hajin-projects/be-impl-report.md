# WORK-005 Phase BE-1 · BE-2 결과 보고

## 상태: done

워크트리 `/Users/kknaks/orca/workspaces/Strong_hajin/strong-hajin-projects`, 브랜치
`kknaksss/strong-hajin-projects`, base `e46ce39`. **커밋하지 않았다 — 변경만 남아 있다.**

---

## 1. 기준선 — 회차 0 (내 변경이 한 줄도 없는 상태)

`make test-contract` 1회. **코드를 아직 고치기 전**이다.

| | 수 |
|---|---|
| passed | **1158** |
| failed | **2** |
| 소요 | 301.88s |

**실패 파일 집합 — 하나다.**

- `tests/contract/test_material_worker_recovery.py`
  - `test_long_parse_heartbeats_its_lease_so_a_second_worker_cannot_reclaim_it`
  - `test_stage_timeout_fences_the_late_parser_result`

브리프가 예고한 **`material_*` 병렬 흔들림 그대로**다. **고치지 않았다 — 범위 밖이다.**
원본 로그: `…/scratchpad/baseline-contract.txt` (세션 스크래치패드).

---

## 2. 회차별 실패 — 들고 난 파일 이름

| 회차 | 언제 | passed | failed | 실패한 **파일** | 판정 |
|---|---|---|---|---|---|
| **0 (기준선)** | 착수 전 | 1158 | **2** | `test_material_worker_recovery.py` **(2건)** | — |
| **1** | BE-1·BE-2 구현 뒤 | 1182 | **2** | `test_material_worker_recovery.py` **(1건)** · **`test_task_fields_and_materials.py` (1건)** | **뒤의 것이 내 탓** |
| **2 (최종)** | 그 한 건을 고친 뒤 | **1183** | **1** | `test_material_worker_recovery.py` **(1건)** | **기준선 밖 실패 0건** |

**들고 난 것 — 회차별로.**

- **새로 든 파일 (회차 1)**: `tests/contract/test_task_fields_and_materials.py`
  — `test_start_sets_a_missing_start_date_to_the_seoul_business_day`.
  **내 변경 탓이 맞다**: 그 테스트가 `work_application.datetime` 을 얼려 서울의 「오늘」을 고정하는데,
  내가 그 시계 읽기를 순수 모듈 `work/task_projection.py` 로 내리면서 얼린 시계가 안 닿게 됐다.
  **고쳤다** — 그 테스트가 `task_projection.datetime` 도 함께 얼리도록 한 줄 더했다(의도·단언은 그대로).
  회차 2에서 통과.
- **빠진 것 (회차 1·2)**: `test_material_worker_recovery.py::test_long_parse_heartbeats_its_lease…`
  가 회차 1·2 에서 **통과**했다. 같은 파일의 다른 한 건은 계속 실패한다 —
  **회차마다 둘 중 어느 것이 넘어질지가 바뀐다.** 흔들림이라는 진단과 일치한다.
- **회차 2 최종 실패 1건**: `test_material_worker_recovery.py::test_stage_timeout_fences_the_late_parser_result`
  — **기준선 파일 안이다.** 손대지 않았다.

> **내일 Phase 0 의 입력**: 흔들리는 파일은 `tests/contract/test_material_worker_recovery.py` **하나**이고,
> 그 안에서 **두 건이 번갈아** 넘어진다(3회차 중 2/1/1건). 파일 자체는 3회차 내내 실패 집합에 있었다.

---

## 3. 그 밖의 검증 — 전부 통과

| 무엇 | 명령 | 결과 |
|---|---|---|
| 도메인·구조·**운영 대장 drift** | `make test-unit` | **369 passed**, 1 deselected |
| **이번 판 계약만 직렬 (`-n0`)** | `make test-contract-serial FILES="…"` | **86 passed** (50.93s) |
| DB·제약·동시성 **회귀** | `make test-postgres POSTGRES_TEST_URL=…/ax_test_projects` | **103 passed**, 1567 deselected |
| 스키마 추가 | `schema_sync.plan()` | `ALTER TABLE task_assignments ADD COLUMN auto_project_join BOOLEAN;` · **`manual[]` 이 비어 있다** |

**직렬 실행에 넣은 파일**(`-n0`, `-p no:randomly` 는 **쓰지 않았다** — 이 레포에 `pytest-randomly` 가 없어 무동작):
`test_projects.py` · `test_project_membership_follows_work.py` · `test_project_commands.py` ·
`test_task_assignments.py` · `test_task_predecessors.py` · `test_task_fields_and_materials.py`.

**운영 대장**: `http_count` **159 불변** · `tool_count` **129 불변** · `acceptance_evidence` **141줄 보존**.
diff 는 **`get_project` 도구의 `output_schema` 한 칸**(90+/1−)뿐이다 — 테스트 실패 diff 의 그 항목만
프로그램으로 패치했고 **전체 재작성을 하지 않았다.**

**새 오류 코드 0건 · 새 라우트 0건**: `git diff -- backend/src` 에 새 `class *Error` 도 새 `raise` 도
**한 줄도 없고**, `entrypoints/http.py` 는 **diff 에 아예 없다.**

---

## 4. 바꾼 파일과 그것이 닫는 인수조건

### Phase BE-1 — 프로젝트 상세 `tasks[]` 확장 + 상태 투영

| 파일 | 무엇을 | 닫는 인수조건 (SPEC-005 §6) |
|---|---|---|
| **`modules/work/task_projection.py` (신규 · 순수)** | `external_state()` · `overdue_days()` · `today_for_tasks()` 를 **판정 한 자리**로 내렸다. `work/projects.py` 가 `work/application.py` 를 import 하지 않는다는 것이 어긋남 ① 의 뿌리라, **투영을 두 벌로 쓰지 않으려면 둘 다 지날 수 있는 자리**가 필요했다 | 상태 어휘 **2줄** — 「승인 대기가 `done` 으로 나온다」 · 「같은 업무가 두 표면에서 같은 값」 |
| `modules/work/application.py` | 위 셋을 import 해 이름만 잇는다(`_external_state = external_state`). 호출처는 한 곳도 안 바꿨다. `_TASK_TIMEZONE`·`ZoneInfo` 제거 | 같은 위 |
| `modules/work/project_results.py` | `ProjectTaskView` 에 **`assignee` · `checklist_progress` · `span_from`/`span_to` · `overdue_days`** 추가 (+ 두 개의 보조 TypedDict) | 간트·좌 레일·요약 스트립의 재료 (I-1~I-5) |
| `modules/work/projects.py` | `get()` 이 새 값을 싣는다. `TaskPredecessorSource` → **`ProjectTaskFactSource`** 로 넓혀 `checklist_progress_for`·`origin_facts` 를 함께 받는다 (옛 이름은 alias 로 남김) | 간트와 트리 BE 절반 **2줄** — 한쪽 날짜만 · 뒤집힌 기간 |
| `tests/architecture/test_test_pyramid.py` | `PURE_DOMAIN_MODULES` 에 `work/task_projection.py` **한 줄 등재** | (경계 규칙) |
| `docs/unified-operations-inventory.json` | `get_project` 의 `output_schema` **한 칸** | (대장 drift) |
| `Makefile` | **`test-contract-serial`** 타겟 (`-n0`) | (검증 편의) |
| `bootstrap/application.py` | `_projects()` 주석만 — 조립은 이미 `SqlAlchemyTaskRepository` 를 넘기고 있었다 | — |

**진행률 저장 컬럼이 늘지 않았다** (1줄): 응답 어디에도 저장된 % 가 없고, `tasks`·`projects` 표에
컬럼을 하나도 더하지 않았다. **하위 집계·후행 배열·「분류」·승인 값도 안 실었다** — 계약 테스트가
그 집합을 명시적으로 부정한다.

**`platform/projects.py` 를 건드리지 않았다 — 계획과 다른 한 곳.** WP §Code Surface #3 은 거기에 조회
둘을 더하라고 적었지만, **업무 저장소에 이미 같은 질의가 있었다**(`checklist_progress_for` ·
`origin_facts`). SPEC §4 가 「업무 상세의 `checklist_progress` 와 **같은 규칙**을 쓴다」·「투영 규칙은
`_assignment_view()` 와 **같은 말**이어야 한다」를 요구하는데, 프로젝트 저장소에 같은 SQL 을 한 벌 더
쓰면 **그 요구를 그 자리에서 깬다.** 그래서 저장소의 **자기 선례**(`TaskPredecessorSource` 의 docstring:
「프로젝트 저장소가 아니라 업무 저장소가 갖는다 … 두 벌이 되면 한쪽만 고쳤을 때 …」)를 그대로 따라
**그 포트를 넓혔다.** 질의 수는 계획과 같다(업무마다 묻지 않는다 — 통째로 한 번씩).

### Phase BE-2 — 소속과 참여의 정합

| 파일 | 무엇을 | 닫는 인수조건 |
|---|---|---|
| `platform/persistence.py` | `task_assignments.auto_project_join` **Boolean nullable** 한 칸. 인덱스·CHECK 없음 | 자동 해제 조건 ① 의 저장 |
| `platform/work_tasks.py` | **`descendants_of()`** (BFS 반복 · 본 것을 다시 보지 않는다) — `children_of()` 는 **안 고쳤다** · **`request_assignment()`** (요청이 세운 배정 행을 `source_work_request_id` 로) | 손자 종속 **5줄** · 떼는 자리 #1·#2 |
| `modules/work/application.py` | `update()` 의 `children_of` 루프 → **`descendants_of`**. **자손 전체를 먼저 다 모으고, 전부에 `_require_project_unlocked()` 를 건 뒤에 옮긴다** | 손자 종속 **5줄** · 핵심 넷 중 1줄 |
| `modules/work/projects.py` | **`join_for_assignment()`** (열쇠 = `may_assign_in`, 관계 = `member`, 멱등) · **`release_for_assignment()`** (**조건 ①·② 판정을 여기 한 곳에**) · `_holds_other_active_work()` (조건 ②) · 사유 상수 둘 | 자동 초대 **7줄** · 자동 해제 **9줄** |
| `modules/work/assignments.py` | **붙는 #2** `reassign()` · **떼는 #3** `decline()` · **떼는 #4** `cancel()`. `ProjectAssigneePort` 를 두 문으로 넓힘. **`assign()`(직접 배정)에는 안 걸었다** | 위와 같음 |
| `modules/work/requests.py` | **붙는 #1** `create()` · **떼는 #1** `reject()` · **떼는 #2** `withdraw()`. 새 포트 `RequestProjectMembershipPort` | 위와 같음 |
| `bootstrap/application.py` | `_work_requests()` 에 `self._projects(session)` 한 줄 — **같은 session 이라 붙이고 떼는 것과 그 명령이 한 트랜잭션** | (트랜잭션 경계) |
| `docs/domain-model.md` | `auto_project_join` 대조표 한 줄 | (대조표 규약) |

**거는 자리는 전부 application 메서드다 — entrypoint 가 아니다.** `entrypoints/http.py` 도
`entrypoints/mcp.py` 도 **diff 에 없다.**

---

## 5. 더한 테스트 — 직렬(`-n0`) 실행 결과

### 신규 `backend/tests/contract/test_project_membership_follows_work.py` — **18건 전부 통과**

| 무엇 | 건수 |
|---|---|
| **붙는 자리 둘** — 요청 발송 · 담당 교체 제안 | 2 |
| 멱등(이미 붙어 있으면 무동작, `lead` 가 `member` 로 안 내려간다) | 1 |
| **열쇠가 `may_assign_in` 이지 `project.manage` 가 아니다** | 1 |
| 프로젝트 없는 업무 = 무동작 · **직접 배정은 붙는 자리가 아니다** | 2 |
| **떼는 자리 넷** — 요청 거절 · 요청 철회 · 배정 거절 · **배정 철회** | 4 |
| 배정 거절이 **요청 유래 행과 담당 교체 제안 행 둘 다**를 닫는다 | (위 4 중 2건이 각각) |
| **조건 ① 거짓**(원래 멤버) · **조건 ② 거짓**(다른 활성 업무) | 2 |
| **수락 뒤 취소로는 안 뗀다** (D-15) | 1 |
| **새 거절 갈래 0건** — 배정이 막히면 기존 배정 거절이 먼저 난다 | 1 |
| **손자 이동** — 4층 트리(상위→자식→손자→증손자) 전부 따라간다 · 옛 프로젝트에 0건 | 1 |
| **자손 잠김 거절** — 409 · 메시지가 「손자」를 짚는다 · **아무것도 안 움직였다** | 1 |
| 이동 뒤 **어느 자손의 선행도 다른 프로젝트에 없다** | 1 |
| 3레벨 트리 헬퍼 등 | 1 |

### 기존 `backend/tests/contract/test_projects.py` — **+6건** (파일 전체 25건 통과)

`tasks[]` 가 싣는 것/안 싣는 것 · 담당 없는 업무는 `assignee: null` · **한쪽만/뒤집힘/없음의 정규화** ·
체크리스트 집계가 업무 상세와 **같은 두 수** · **승인 대기가 두 표면에서 `done`** ·
기한 경과일이 `my-work` 의 `derived.overdue_days` 와 **같은 수**.

### 신규 `backend/tests/integration/postgres/test_project_participation.py` — **+1건**

**닫고 다시 붙이는 경로가 `uq_project_assignment_active` 와 부딪히지 않는다** —
떼어진 뒤 다시 보내면 **새 회차가 서고**, 닫힌 회차는 **지워지지 않고 남으며**, 활성 참여는 언제나 1이다.
**증명이 아니라 회귀다** — 이 판은 새 제약을 만들지 않았다.

### 고친 기존 테스트 1건

`tests/contract/test_task_fields_and_materials.py::test_start_sets_a_missing_start_date_to_the_seoul_business_day`
— 얼린 시계를 `task_projection` 에도 걸도록 **한 줄 추가**. 단언도 의도도 그대로다.

---

## 6. FE 브리프에 박을 **실물 응답** — `GET /api/projects/{project_id}` 의 `tasks[]`

실제 실행 결과다(추정이 아니다). 계약 테스트 하네스(TestClient) 안에서 찍었다 —
**사용자 포트·프로세스를 건드리지 않았다.**

```json
[
  {
    "task_id": "660ed336-2371-47e3-b1ae-3b4691d45fa0",
    "title": "홈페이지 디자인 기획",
    "state": "open",
    "start_date": "2026-09-10",
    "due_date": "2026-09-20",
    "parent_task_id": null,
    "preceding_task_ids": [],
    "assignee": { "member_id": "mina", "display_name": "민아 (구성원)" },
    "checklist_progress": { "done": 2, "total": 5 },
    "span_from": "2026-09-10",
    "span_to": "2026-09-20",
    "overdue_days": 2
  },
  {
    "task_id": "22251b6b-5226-44a0-8abe-63ca46f801a1",
    "title": "플레이스 썸네일 제작",
    "state": "open",
    "start_date": null,
    "due_date": "2020-01-01",
    "parent_task_id": null,
    "preceding_task_ids": ["660ed336-2371-47e3-b1ae-3b4691d45fa0"],
    "assignee": { "member_id": "mina", "display_name": "민아 (구성원)" },
    "checklist_progress": { "done": 0, "total": 0 },
    "span_from": "2020-01-01",
    "span_to": "2020-01-01",
    "overdue_days": 2456
  },
  {
    "task_id": "441314d2-869a-4b83-bac2-4c1b2da9f2bc",
    "title": "사람도 기간도 없는 일",
    "state": "open",
    "start_date": null,
    "due_date": null,
    "parent_task_id": null,
    "preceding_task_ids": [],
    "assignee": null,
    "checklist_progress": { "done": 0, "total": 0 },
    "span_from": null,
    "span_to": null,
    "overdue_days": null
  }
]
```

**FE 가 읽을 때 틀리기 쉬운 자리 넷.**

1. **`assignee` 는 `null` 이 정상이다.** 「미정」을 서버가 지어내지 않는다.
   그리고 **활성 배정이 없으면 답을 기다리는 사람**이 여기 선다(업무 상세 `_assignment_view()` 와 같은 말).
2. **`checklist_progress.total == 0` 은 0% 가 아니다.** fill 도 % 도 그리지 않는다 — **서버는 판정하지 않는다.**
3. **`span_*` 은 이미 접혀서 온다.** 「마감만 있는 일」은 그 날 하루, 뒤집힌 것은 `[min, max]`.
   **`start_date`·`due_date` 원값은 그대로 함께 온다** — 정규화가 덮어쓰지 않는다. 둘째 줄이 그 예다.
4. **`overdue_days` 는 끝난 업무에 안 온다**(완료·취소·**승인 대기**). 「지연」 칸은 **값이 온 업무만 센다** —
   화면이 「오늘」을 다시 판정하지 않는다.

**`state` 는 계약의 넷뿐이다.** `completion_submitted` 는 투영이 `done` 으로 접는다. `blocked` 는
**발행하지도 없애지도 않고** 들어오는 대로 낸다(M-6 승계) — 계약 어휘를 넓히지 않았다.

---

## 7. 막힌 것 · 판단이 필요한 것

### ⚠ (가) SPEC §6 인수조건 한 줄이 **오늘의 역할 표로는 성립하지 않는다**

> 「**프로젝트 관리 권한이 없는 참여자**가 배정해도 붙는다 — 열쇠가 **배정 권한**이다.」

**그런 사람이 지금 존재하지 않는다.** 근거는 역할 카탈로그다
(`modules/organization_access/catalog.py:139-153`):

- `project-participant` = `project.read`·`work.read`·`task.read`·`work_request.read` — **`task.assign` 이 없다**
- `project-lead` = 그것 + **`task.assign` + `project.manage`** — **둘이 붙어 있다**

`may_assign_in()` 은 `allows(TASK_ASSIGN, project=…)` 이므로, **그 프로젝트에서 배정할 수 있는
사람은 그 프로젝트를 관리할 수도 있다.** 조직 축의 배정 권한(예: 팀장)은 `project=` 질문에 답하지 않는다 —
실측으로 확인했다: 지호(프로젝트 참여자 + 조직 축 `task.assign`)가 프로젝트 업무를 **배정하는 데는
성공하지만**, `may_assign_in` 이 거짓이라 **초대는 일어나지 않는다.**

**내가 한 것.** 브리프·SPEC 이 못 박은 대로 **열쇠를 `may_assign_in` 으로** 두었다. **`project.manage`
를 요구하지도, `task.assign` 을 넓히지도 않았다.** 그 인수조건이 실제로 지키는 것 —
「**관리 권한을 묻지 않는다**」와 「**아무 배정에나 초대를 얹지 않는다**」 — 을 증명 가능한 형태로
테스트에 담았다(`test_the_key_is_assigning_in_that_project_not_managing_it`).

**판단이 필요한 것.** 이 줄을 **그대로 둘지**, 아니면 **역할 표를 나누는 후속**(참여자에게 프로젝트 범위
`task.assign` 만 주는 갈래)을 여는지. **역할 표를 건드리는 것은 이 판의 범위 밖**이라 하지 않았다.
그 갈래를 열면 **부수 효과**로 「배정은 되는데 받는 사람이 그 업무를 못 읽는」 자리(아래 (나))도 함께 닫힌다.

### ⚠ (나) 배정은 되는데 초대가 안 되는 틈 — **이 판이 만든 것이 아니라 드러낸 것**

위 (가)의 실측 그대로다: 조직 축 배정 권한만 가진 사람이 프로젝트 업무를 남에게 넘기면
**그 사람은 그 업무를 들지만 프로젝트를 못 읽는다.** 자동 초대 이전에도 그랬고 이 판이 바꾸지 않았다.
**오류가 아니라 무동작**이므로 새 거절 갈래도 생기지 않았다. 계약을 새로 만들 자리라 **하지 않았다.**

### ⚠ (다) SPEC §5 「프로젝트 상세 **행의 서명**이 바뀐다」 — 실제로 바뀐 것은 다른 칸

WP 가 이미 `Open Issues` 로 든 그대로다. `http_signature` 는 **불변**이고
(`(project_id: UUID, principal: Principal) -> ProjectDetailResult`), 실제로 바뀐 것은
**MCP `get_project` 의 `output_schema`** 한 칸이다. **계약은 안 갈린다 — 가리키는 자리만 다르다.**

### (라) 동시성 틈 — 감추지 않았다

같은 사람에게 보낸 업무 **둘이 동시에** 거절되면 **둘 다 상대의 활성 업무를 보고 아무도 안 뗀다.**
결과는 「사람이 프로젝트에 남는 것」이고 **참여가 잘못 사라지는 것보다 안전한 쪽**이다.
「다른 활성 업무가 있나」는 두 표(`tasks`·`task_assignments`)에 걸친 세기라 **DB 제약으로 못 올린다** —
`_holds_other_active_work()` 의 docstring 에 그대로 적어 두었다.

### (마) 「조건 ②」의 「활성」을 내가 정한 자리 — **(제안)**

D-14 는 「그 사람의 **다른 활성 업무**」라고만 적는다. 나는 **취소된 업무만 빼고 나머지는 센다**로
읽었다(수락 뒤 완료된 일도 「그 일이 있었다」의 증거라서 — D-15 와 같은 결). **사람이 남는 쪽으로
치우친 해석**이고 위 (라)와 같은 안전 방향이다. 다르게 정하려면 알려 달라.

### (바) 하지 않은 것 — 범위대로

- **`material_*` 격리(Phase 0)**: 손대지 않았다. **사용자가 내일 한다.**
- **프론트**: 한 줄도 안 건드렸다.
- **`tasks_in()` 의 필터·페이징**: 안 넣었다 (D-27).
- **커밋·push·PR**: 하지 않았다. 워크트리에 변경만 있다.
- **「커밋 후 API 를 다시 띄웠다」**(WP 완료 판정의 마지막 줄): **띄우지 않았다.** 브리프 §4 가
  사용자 포트·프로세스를 건드리지 말라고 했고 커밋도 금지라, 실물 확인은 **테스트 하네스 안에서**
  했다(위 §6 이 그 결과다). 실서버 확인이 필요하면 코디네이터가 띄울 자리다.

---

## 8. 바뀐 파일 전수

**신규 2**
- `backend/src/ax_workspace/modules/work/task_projection.py`
- `backend/tests/contract/test_project_membership_follows_work.py`

**수정 15**
- `Makefile`
- `backend/src/ax_workspace/bootstrap/application.py`
- `backend/src/ax_workspace/modules/work/application.py`
- `backend/src/ax_workspace/modules/work/assignments.py`
- `backend/src/ax_workspace/modules/work/project_results.py`
- `backend/src/ax_workspace/modules/work/projects.py`
- `backend/src/ax_workspace/modules/work/requests.py`
- `backend/src/ax_workspace/platform/persistence.py`
- `backend/src/ax_workspace/platform/work_tasks.py`
- `backend/tests/architecture/test_test_pyramid.py`
- `backend/tests/contract/test_projects.py`
- `backend/tests/contract/test_task_fields_and_materials.py`
- `backend/tests/integration/postgres/test_project_participation.py`
- `docs/domain-model.md`
- `docs/unified-operations-inventory.json`

**건드리지 않은 것(확인)**: `entrypoints/http.py` · `entrypoints/mcp.py` ·
`modules/ax_execution/tool_catalog.py` · `platform/projects.py` · `bootstrap/schema_sync.py` ·
`frontend/` 전체 · 문서 레포.
