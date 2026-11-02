# 고도화 2차 서버 전수조사

- 대상: `strong-hajin-polish2` 워크트리, base `origin/main`(`3d47a32`)
- 읽기 전용 조사다. 코드 수정, 테스트·빌드 실행, 서버·DB 기동, 운영 접속은 하지 않았다.
- 경로 약어: `B/` = `backend/src/ax_workspace/`, `F/` = `frontend/src/`, `SPEC/` = 문서 리포 `para/projects/summer-star/strong-hajin/20-spec/`
- 줄 번호는 모두 `3d47a32` 기준이다. 1차 리포트의 줄 번호는 옛 값이라 다시 셌다.

## 0. 한 줄 요약

- **E2E-1 체크리스트가 비어 온다**: 서버는 체크리스트를 **어느 단계에서도 버리지 않는다**. 도구 입력 → 정규화 → 스냅샷 → 편집 계약 → confirm → 업무 생성까지 `checklist` 가 전부 실린다. 비어 온 이유로 코드에서 보이는 것은 지시문이다. 생성 도구 설명이 「대화가 준 것·조회로 확인한 것만 채워라, 지어내느니 비워 둬라」(`B/modules/ax_execution/tool_catalog.py:546`, `:648`)라고 하고, 체크리스트·내용·기한을 **제안해서 채우라는 문장은 0건**이다. 사용자 발화에 단계·기한·내용이 없었으므로 AI 는 지시대로 비웠다. 다만 운영 trace 를 보지 않았으므로 이 원인은 **추정**이다.
- **E2E-2 「저장」(확정 없이 초안만 수정)**: 그런 서버 명령은 **없다**. AX 초안이 받는 명령은 `confirm`·`reject`(+ 호환 `approve`, 배정 취소) 뿐이고, 회차 증가·diff 기록은 `confirm` 안에서만, 확정·업무 생성과 **같은 transaction** 에서 일어난다. 그래서 지금 코드에는 「pending 이면서 2회차 이상인 초안」이 생기는 경로가 없다. 채팅 뷰와 판단 대기는 매번 **최신 Submission 스냅샷**을 읽는다(스냅샷을 메시지에 박아 두지 않는다). 초안 변경을 알리는 실시간 이벤트는 없다(WebSocket 은 회의 스트림 1개뿐).
- **E2E-5 업무 날짜**: `tasks` 에 날짜 열 2개(`start_date` 계획 시작일, `due_date` 기한)와 시각 열 5개(`started_at`·`completed_at`·`reopened_at`·`created_at`·`updated_at`)가 있다. 「실제 시작일 = `started_at`」, 「실제 종료일 ≈ `completed_at`」이다. 그런데 (1) 시작 전이가 비어 있던 `start_date` 를 **오늘로 채워** 계획 칸에 실제 값이 섞이고, (2) 요청 업무의 `completed_at` 은 승인 시각이 아니라 **완료 보고 제출 시각**이며, 보완 요청·재개 때 **지워진다**. SPEC-001·003 의 「계획 기한(박제)·실제 기한 두 값(`due_planned`/`due_actual`)」은 코드에 **없다**(기한은 `due_date` 한 값이고 사유 없이 바뀐다).
- **E2E-3·4 출처 정보**: 업무 응답마다 `lineage.source_action_item_id` 가 있다(`B/modules/work/application.py:2829`). 목록·상세의 `origin` 은 `kind:"self_created"` + `source:{type:"action_item", id, title}` 로 AX 출처를 준다(`:2467-2471`, `:2501-2509`). 단, 업무 요청에서 나온 업무는 `origin` 이 `work_request` 쪽을 먼저 택해 AX 출처가 `origin` 에는 나오지 않는다(`lineage` 에는 남는다).

---

## 1. E2E-1 AX 업무 초안에 체크리스트가 비어 온다

### 1-1. 초안 객체의 체크리스트 — 단계별로 실리나, 버려지나

결론: **모든 단계에서 실린다. 서버가 버리는 지점은 0곳이다.**

| 단계 | `task.create_self` (업무 생성) | `work_request.create` (업무 요청) |
|---|---|---|
| ① MCP 도구 입력 스키마 | `checklist: list[str] \| None = None` (`B/entrypoints/mcp.py:2016`) → facade 로 그대로 넘김(`:2031`) | `checklist: list[str] \| None = None` (`B/entrypoints/mcp.py:1679`) → 그대로 넘김(`:1687`) |
| ② facade 가 입력 모델로 검증 | `TaskCreateInput(..., checklist=checklist, ...)` (`B/entrypoints/mcp.py:748`) → `model_dump(mode='json')` 를 제안 payload 로(`:749-750`) | `WorkRequestCreateInput(..., checklist=checklist, ...)` (`B/entrypoints/mcp.py:384`) → payload(`:385-386`) |
| 입력 모델 정의 | `TaskCreationFields.checklist: list[str]`, 기본 `[]`, `title='체크리스트'`(설명문 없음) (`B/modules/work/task_creation.py:18`). `None`→`[]`(`:27-30`), `clean_checklist` 로 공백 정리·300자 자름·최대 50개(`:36`, `B/modules/work/task_values.py:11`, `:14-26`) | 같은 상속 사슬 `WorkPayloadFields`(`B/modules/work/task_creation.py:44`) → `WorkRequestCreateInput`(`B/modules/work/request_commands.py:98`) |
| ③ 제안 저장(정규화) | `_canonical_proposal` 은 회의·진행 묶음만 다시 얼리고 업무 생성 payload 는 **그대로 둔다** (`B/platform/actions.py:289-300`) | 같음 |
| ④ 스냅샷 | `SubjectVersionRecord.snapshot = dict(action.payload)` (`B/platform/actions.py:359`) — `checklist` 키 포함 | 같음 |
| ⑤ 화면 미리보기(preview) | 단계가 있을 때만 `{"id":"checklist", "value":"N단계 · a → b"}` 한 줄 (`B/platform/actions.py:1401-1406`). **비어 있으면 줄이 없다** | 같음(`_CREATION_KINDS` 에 둘 다 있다, `:1199-1204`) |
| ⑥ 편집 계약 | `values` = `normalize_task_draft(payload)`(`B/platform/actions.py:1697-1699`), 필드 목록에 `checklist`(`string_list`) (`:1795-1801`) | `values` = `normalize_work_request_draft`(`B/platform/actions.py:1943`), 필드 `checklist`(`:2022-2028`) |
| ⑦ confirm 정규화 | `normalize_ax_draft` → `normalize_task_draft` = `TaskCreateInput.model_validate(...).model_dump()` (`B/modules/actions/confirmation.py:161-166`, `B/modules/work/drafts.py:16-26`) | `normalize_work_request_draft` (`B/modules/actions/confirmation.py:156-158`, `B/modules/work/drafts.py:40-54`) |
| ⑧ 실행(업무 생성) | `TaskCreateInput.model_validate(payload)` → `task_creation().create_task(**command.model_dump(...))` (`B/platform/actions.py:826-836`) → `create_self(..., checklist=command.checklist)` (`B/modules/work/creation_commands.py:132-135`) → `seed_checklist` (`B/platform/work_tasks.py:427`, `:867-870`) | `WorkRequestCreateInput.model_validate(payload)` → `create_work_request(**command.model_dump())` (`B/platform/actions.py:708-718`) → `requests.create(..., checklist=checklist)` (`B/modules/work/creation_commands.py:329-333`) → `seed_checklist(task, request.initial_checklist)` (`B/platform/work_tasks.py:2074`) |

- `prepare_action` 은 회의 예약에만 손대고 나머지 payload 는 그대로 돌려준다(`B/bootstrap/application.py:3914-3924`).
- 업무 생성에서 담당을 남으로 지정한 갈래도 `checklist` 를 넘긴다(`B/modules/work/creation_commands.py:152-155`).
- **서버 정규화가 체크리스트를 비우는 경우**는 두 가지뿐이다. 공백뿐인 항목은 빠지고, 50개를 넘으면 거절된다(`B/modules/work/task_values.py:19-25`).

### 1-2. AI 에게 필드를 어디까지 채우라고 하나 — 해당 문장 전부

AI 가 받는 지시는 두 곳이다. (a) MCP 도구 설명: 카탈로그가 정본이고, 등록 시 `description=definition.description` 으로 들어간다(`B/entrypoints/mcp_server.py:38`, `:47-50`). (b) 턴 프롬프트의 정책 6절: `RELATIONSHIP` · `MEETING_CREATION` · `TASK_PROGRESS` · `WORK_AND_REPORT_ROUTING` · `ANSWER_PRESENTATION` · `FOLLOW_UP`(`B/platform/codex_cli.py:508-516`). Claude 어댑터도 같은 정책을 쓴다(`B/tests/unit/test_ax_work_lookup_policy.py:55-57`가 단언).

**「대화가 준 것만 / 지어내지 말라 / 비워 두라」에 해당하는 문장**

| # | 위치 | 원문 |
|---|---|---|
| 1 | `B/modules/ax_execution/tool_catalog.py:546` (`task_create_self`) | "Fill a link only when one candidate clearly matches; if none or several match, leave it empty and say so in the answer — never invent an ID." |
| 2 | 같은 줄 | "Fill every field the conversation gives you or that lookup confirmed: title (required, 1–300 characters), description, ISO start_date and due_date, project_id, cc_member_ids (참조자), approver_id (결재자), preceding_task_ids (선행업무, same project), parent_task_id (one-level 상위 업무), checklist (up to 50 first steps in order) and reference_task_ids …" |
| 3 | 같은 줄 | "Only the title is required; a due date is optional, so leave a value empty rather than inventing one." |
| 4 | `B/modules/ax_execution/tool_catalog.py:648` (`work_request_create`) | "fill a link only when one candidate clearly matches, otherwise leave it empty and say so in the answer — never invent an ID." |
| 5 | 같은 줄 | "Then fill every field the conversation gives you or that lookup confirmed: title (required, 1–300 characters), assignee_id (required), description, ISO start_date and due_date, … checklist and readable reference_task_ids." |
| 6 | 같은 줄 | "Only the title and the recipient are required; a due date is optional, so leave a value empty rather than inventing one." |
| 7 | `B/platform/codex_cli.py:464-466` (업무 생성 라우팅) | "대화에 나온 이름이나 업무 주제와 **한 후보로 확정될 때만** `project_id`·`parent_task_id`·`preceding_task_ids`(같은 프로젝트의 업무)·`reference_task_ids`를 채운다. 못 찾았거나 후보가 여럿이면 비워 두고, 답변에 「연결할 프로젝트를 찾지 못했습니다」처럼 무엇을 비웠는지(후보가 여럿이면 그 이름들)를 말한다. 조회 결과에 없는 ID를 지어내지 않는다." |
| 8 | `B/platform/codex_cli.py:402-404` (관계 지침) | "사용자가 본인 업무 생성이나 승인할 수 있는 생성안을 요청하면 필요한 자료 근거와 연결할 프로젝트·기존 업무를 먼저 조회한 뒤 … `task_create_self`로 Action 제안을 준비한다." (채울 범위에 대한 말은 없다) |

**참고 — 업무 생성이 아닌 갈래의 비슷한 문장**(이번 증상과 직접 관련은 없다)
- 회의 참석자: "찾지 못한 사람은 임의 ID나 다른 사람으로 채우지 않은 채 카드의 참석자 선택에서 보완하도록 짧게 알린다." (`B/platform/codex_cli.py:427-428`). AX 답변의 「승인 카드에서 보완할 수 있습니다」와 말투가 같다.
- 진행 묶음 "변경 값은 조회 결과만 사용하고 추측하지 않는다"(`:446`), 관계 "지어내지 말고"(`:393`), ID "추측하지 않는다"(`:384`, `:481`).
- `task_assign`(`tool_catalog.py:458`)에는 "optional ISO schedule, checklist" 만 있고 비우라는 문장은 없다.

**없는 것**
- 체크리스트·내용·기한을 업무 주제에서 **제안해 채우라**는 문장은 도구 설명·정책 어디에도 없다. `checklist` 를 언급하는 곳은 위 2·5번의 필드 나열과 진행 기록 지침(`codex_cli.py:443-445`)뿐이다.
- 도구 인자 스키마에도 체크리스트 설명이 없다. `title`·`assignee_id`·`approver_id` 는 `Annotated[..., model_fields[...]]` 로 필드 메타를 싣지만 `checklist` 는 맨 타입이다(`B/entrypoints/mcp.py:2014-2027`). 모델 필드도 `title='체크리스트'` 하나뿐이다(`task_creation.py:18`).
- 「지어내지 않는다」 계열을 단언하는 테스트: `B/tests/unit/test_ax_work_lookup_policy.py:17`("지어내지 않는다"), `:30`("never invent an ID"). 체크리스트를 채우라는 단언은 0건이다.

### 1-3. 생성 명령 필드 vs 초안 객체 필드 대조표

정본: `TaskCreationApplication.create_task`(`B/modules/work/creation_commands.py:79-103`), `create_work_request`(`:270-301`).
초안: `TaskCreateInput`(`B/modules/work/task_creation.py:12-106`), `WorkRequestCreateInput`(`B/modules/work/request_commands.py:98-120`).
편집 계약: 업무 생성 `B/platform/actions.py:1730-1838`, 업무 요청 `:1936-2048`.

| 필드 | 생성 명령 `create_task` | 초안 `task.create_self` | 편집 계약 `task.create_self` | 생성 명령 `create_work_request` | 초안 `work_request.create` | 편집 계약 `work_request.create` | MCP 도구 인자 |
|---|---|---|---|---|---|---|---|
| title | ✔ | ✔ 필수 | ✔ 필수 | ✔ | ✔ 필수 | ✔ 필수 | ✔ 둘 다 |
| description | ✔ | ✔ | ✔ | ✔ | ✔ | ✔ | ✔ |
| start_date | ✔ | ✔ | ✔ | ✔ | ✔ | ✔ | ✔ |
| due_date | ✔ | ✔ 선택 | ✔ 선택(`:1754-1755`) | ✔ | ✔ 선택 | ✔ 선택 | ✔ |
| checklist | ✔ | ✔ | ✔ | ✔ | ✔ | ✔ | ✔ |
| reference_task_ids | ✔ | ✔ | ✔ | ✔ | ✔ | ✔ | ✔ |
| parent_task_id | ✔ | ✔ | ✔ | ✔ | ✔ | ✔ | ✔ |
| project_id | ✔ | ✔ | ✔ | ✔ | ✔ | ✔ | ✔ |
| cc_member_ids | ✔ | ✔ | ✔ | ✔ | ✔ | ✔ | ✔ |
| preceding_task_ids | ✔ | ✔ | ✔ | ✔ | ✔ | ✔ | ✔ |
| approver_id | ✔ | ✔ | ✔ | ✔ | ✔ | ✔ | ✔ |
| assignee_id | ✔ 선택 | ✔ 선택 | 읽기 전용, 본인 고정(`:1741-1752`, `editable: False` `:1748`) | ✔ 필수 | ✔ 필수 | ✔ | ✔ |
| supersedes_request_id | — | — | — | ✔ | ✔ (`request_commands.py:107`) | **없음** | **없음**(`mcp.py:1675-1686`) |
| idempotency_key | ✔ 필수 | — (실행기가 `str(action.id)` 를 넣음, `actions.py:829`) | — | ✔ 필수 | — (실행기가 `action.id`, `:713`) | — | ✔ 필수 |
| causation_key | ✔ | — (실행기가 `action.id`) | — | ✔ | — (실행기가 `action.id`) | — | — |
| source_action_item_id · source_decision_item_id · source_submission_id · source_review_decision_id | ✔ | — (실행기가 채움, `actions.py:830-833`) | — | ✔ | — (`actions.py:714-717`) | — | — |
| source_meeting_id · source_agenda_id · allow_self_assignment · promoted_by_member_id | — | — | — | ✔ (회의 승격 전용) | — | — | — |
| 자료(파일·링크) | (생성 뒤 별도 연결) | `attachment_draft_ids` 별도 칸 | 별도 | — | **불가** — `ATTACHABLE_ACTION_TYPES` 에 없다(`B/modules/actions/confirmation.py:38-40`) | — | — |

- 빠진 것: 업무 요청 초안의 `supersedes_request_id` 는 모델에 있지만 도구 인자와 편집 필드에는 없다. 업무 요청 초안은 자료를 붙일 수 없다.
- 이름이 다른 것: 없다. 도구·초안·생성 명령의 필드명이 같다(공통 모델 `WorkPayloadFields` 상속, `task_creation.py:44-55`).
- 업무 생성에서 담당을 남으로 지정하면 `start_date`·`parent_task_id`·`project_id`·`preceding_task_ids` 를 **거절**한다(`B/modules/work/creation_commands.py:170-200`). 초안 편집기는 담당을 바꾸지 못하지만(`actions.py:1741-1752`), AI 가 초안에 남의 `assignee_id` 를 넣었다면 confirm 할 때 이 거절을 만난다.

### 1-4. 체크리스트를 나중에 넣는 경로

| 시점 | 경로 | 근거 |
|---|---|---|
| 초안(확정 전) | **독립 명령 없음.** `confirm` 에 `draft.checklist` 를 실으면 수정과 확정이 한 번에 일어난다 | `B/entrypoints/http.py:2278-2284`, `B/platform/action_center.py:571-616` |
| 업무 생성 뒤 | `POST /api/tasks/{id}/checklist`(추가) · `PATCH …/checklist/{item_id}`(수정·완료) · `POST …/checklist/order`(순서) · `DELETE …/checklist/{item_id}`(보관) | `B/entrypoints/http.py:2173-2217` |
| 권한 | **활성 담당자만** — `_holding(principal, task_id, …)` | `B/modules/work/application.py:2518-2534` |
| 이력 | `record_activity("task.checklist.added", …)` → `activity_events` + `task_versions` | `:2533`, `B/platform/work_tasks.py:980-1010` |
| AX 경유 | MCP `task_checklist_add`/`update`/`archive`/`reorder` → 위임 턴에서는 `task.checklist.*` 제안 카드 | `B/entrypoints/mcp.py:1091-1096`, `:1991-2010`, 실행 `B/platform/actions.py:847-848` |
| `task.update`(PATCH) | 체크리스트 칸이 **없다** (`TaskEditFields` 에 없음) | `B/modules/work/task_commands.py:46-71` |

---

## 2. E2E-2 「수정」 모달의 등록 → 「저장」

### 2-1. 확정 없이 초안을 고쳐 저장하는 서버 명령 — 없다

- AX 초안에 걸리는 HTTP 라우트는 `/api/action-items*` 6개와 구 `/api/actions*` 2개다.
  - `GET /api/action-items` · `GET /{id}` · `POST /{id}/material-drafts/links` · `POST /{id}/material-drafts/files` · `POST /{id}/material-drafts/{draft}/discard` · `POST /{id}/commands/{command}` (`B/entrypoints/http.py:2221-2284`)
  - `GET /api/actions` · `POST /api/actions/{id}/decide` (`:1231-1250`)
- `commands/{command}` 가 받는 명령은 envelope 가 허락한 것뿐이다(`B/modules/actions/domain.py:160-171`). AX 초안이 받는 것은 다음과 같다.
  - pending: `confirm`(라벨 「이 내용으로 업무 생성」/「이 내용으로 업무 요청」) + `reject` (`B/modules/actions/policy.py:114-128`, 라벨 `:19-26`)
  - 확정된 `task.assign`: `cancel_assignment` (`:129-136`)
  - 호환 `approve`: `COMMAND_CONTRACTS` 종류에만 붙는다(`B/platform/action_center.py:754-755`, 라벨 「승인」)
- `draft` 를 받는 명령은 `confirm` 하나다. 다른 명령에 `draft`·`base_submission_version` 을 실으면 거절된다(`B/platform/action_center.py:607-612`).
- 확정 전에 초안에 쓸 수 있는 것은 **자료 staging** 뿐이다. 이 경로는 `action_material_drafts` 행만 쓰고 Submission·SubjectVersion 을 만들지 않는다(`B/modules/work/action_materials.py:70`, `B/platform/action_materials.py:25`. 두 파일에 Submission 쓰기 0건).
- 회차·diff 는 confirm 안에서만 남는다(2-2). 그래서 「고친 초안 회차」가 확정 없이 남는 경로가 지금은 없다.

### 2-2. confirm + `draft` 경로가 하는 일 전부

진입: `POST /api/action-items/{id}/commands/confirm` → `run_action_command`. **한 세션·한 transaction** 이고 실패하면 전부 롤백된다(`B/bootstrap/application.py:3393-3402`).

| 순서 | 하는 일 | 근거 | 성격 |
|---|---|---|---|
| 1 | envelope 가 `confirm` 을 허락했는지 검사 | `B/modules/actions/domain.py:160-170` | 판단 |
| 2 | `normalize`: `expected_version`·`base_submission_version` 필수. `draft` 가 없으면 최신 스냅샷 사용. `normalize_ax_draft` 로 생성 입력 모델 검증 | `B/platform/action_center.py:571-616` | 내용 |
| 3 | `_confirm`: action 행 `FOR UPDATE`. pending 이 아니면 영수증 판정 | `:798-809` | 판단 |
| 4 | `decide_ax_confirmation`: state=pending · version 일치 · decision open · 기준 회차 일치를 검사한다. 기준 스냅샷과 최종 초안을 정규화해 비교하고, **다르면** `OpenAxSubmissionRound(submission_version+1, snapshot, diff=payload_diff(raw_base, final))` 를 만든다. 같은데 활성 배정이 없으면 거절 | `B/modules/actions/confirmation.py:178-246` (회차 `:237`, diff `:239`) | 내용 |
| 5 | 자료 초안 claim 가능 여부 검증 | `B/platform/action_center.py:834-840` | 실행 준비 |
| 6 | `prepare_action`(회의만 의미 있음) | `:842-853` | 실행 준비 |
| 7 | **(바뀌었을 때만)** 기존 ReviewAssignment → `superseded`/`revised` | `:858-863` | 내용 회차 |
| 8 | 새 `SubjectVersionRecord(version=n+1, snapshot=final)` | `:864-872` | 내용 회차 |
| 9 | 새 `SubmissionRecord(submission_version=n+1, revises_id=이전, submitted_by=사람, diff=…)` | `:873-885` | 내용 회차 |
| 10 | 이전 Submission 의 Evidence 행을 새 Submission 으로 복사 | `:888-901` | 내용 회차 |
| 11 | 새 `ReviewAssignmentRecord(status="pending", supersedes_assignment_id=…)` | `:902-911` | 내용 회차 |
| 12 | `ReviewDecisionRecord(decision="confirm", conditions={expected_version, base_submission_version, payload_hash, attachment_draft_ids, evidence…})` | `:914-934` | 판단 |
| 13 | 배정 → `decided`/`confirmed`, `decision_item.status="resolved"` | `:935-939` | 판단 |
| 14 | `execute_confirmed` → 실행기 → **업무(또는 요청+업무) 생성**. 멱등 키 = action id | `:940-951`, `B/modules/ax_execution/actions.py:139-160`, `B/platform/actions.py:708-718`, `:826-836` | 실행 |
| 15 | `resolve(..., "approve")`: `action_items.state="approved"`, `version+=1`, `decided_at`, 감사 `action.approved` | `B/platform/actions.py:459-465` | 판단 |

- 지금 코드에서 「내용 회차」(7~11)와 「판단·실행」(12~15)은 같은 함수 `_confirm` 의 같은 transaction 에 있다. 4번이 두 쪽 모두의 전제 검사다(state=pending, 기준 회차 일치).
- 「저장」과 「확정」을 가른다면, 지금 코드 기준으로 「저장」에 해당하는 몫은 2·4·7~11이고, 12~15와 5·6은 「확정」 몫이다. 단 다음 셋이 지금 코드의 제약이다.
  - 4번은 「바뀌지 않았는데 활성 배정이 없다」를 거절한다(`confirmation.py:228-230`).
  - 11번이 새 배정을 `pending` 으로 열지만, 지금은 곧바로 12~13번이 그 배정을 닫는다.
  - 회차 유일성은 `UniqueConstraint(decision_item_id, submission_version)` 이고(`B/platform/persistence.py:1190`), SubjectVersion 은 `(subject_id, version)` 이다(`:1158`).
- `action_items.payload`·`payload_hash` 는 **처음 AX 제안 값 그대로** 남는다. 회차가 올라도 갱신하지 않는다(`B/platform/actions.py:266-281`에서만 쓴다).

### 2-3. 초안이 바뀌면 채팅 뷰·판단 대기가 새 값을 주나

| 표면 | 읽는 값 | 근거 |
|---|---|---|
| 채팅 `GET /api/conversations/{id}` 의 `actions[]` | 대화의 `ActionItemRecord` 를 매번 조회해 `view()` 로 그린다. `view()` 는 `_canonical_payload` = **최신 Submission 의 SubjectVersion.snapshot** 으로 preview·edit_contract 를 만든다 | `B/platform/conversations.py:685-692`, `:854`, `B/platform/actions.py:519-521`, `:602-612` |
| 판단 대기 `GET /api/action-items` | `envelope()` 가 `_current_submission` 의 스냅샷으로 `present()` 를 부른다 | `B/platform/action_center.py:686-705` |
| 상세 `GET /api/action-items/{id}` | 위 envelope + `rounds[]`(Submission 마다 `snapshot`·`diff`·`decisions`) | `B/modules/actions/domain.py:145-152`, `B/platform/action_center.py:478-523` |
| 처음 값으로 고정되는 것 | `payload_summary` 는 `action.payload`(처음 값)로 만든다 — 업무 요청은 `업무 요청: {처음 제목}`, 업무 생성은 종류 문자열 | `B/platform/actions.py:625-643` |
| 처음 값으로 고정되는 것 | AX 답변 본문은 `conversation_messages.body` 에 저장된 텍스트다. 도구 호출 줄은 `tool_invocations.input_summary` 에 남는다 | `B/platform/persistence.py:712-725`, `:759` |

- 즉 **스냅샷을 메시지에 박아 두지 않는다.** 카드 내용은 매번 최신 Submission 에서 읽는다. 다만 지금은 회차가 오르는 순간 같은 transaction 에서 resolved 되므로, 「pending 인데 2회차」를 보여 줄 일이 아직 없다.

### 2-4. 초안 변경 실시간 이벤트 — 없다

- 백엔드의 `@app.websocket` 은 회의 스트림 1개뿐이다(`B/entrypoints/http.py:1023`). SSE(`text/event-stream`)는 0건이다.
- `B/platform/actions.py`·`B/platform/action_center.py` 에는 알림·발행 호출이 없다. `notifications` 가 등장하는 곳은 `notification.mark_read` 액션뿐이다(`actions.py:737-739`, `:1600-1604`).
- 프론트의 `new WebSocket` 은 회의 스트림 1곳이다(`F/features/meetings/stream.ts:103`). 나머지 `setInterval` 은 화면별 폴링·시계다(`F/features/today/TodayPage.tsx:144` 등).

---

## 3. E2E-5 업무 날짜 — 시작 예정일 · 실제 시작일 · 실제 종료일 · 마감일

### 3-1. `tasks` 의 날짜·시각 열 전부

`TaskRecord`(`B/platform/persistence.py:897-962`)

| 열 | 타입 | 뜻(코드 주석) | 누가 언제 채우나 |
|---|---|---|---|
| `start_date` | Date | **계획** 시작일. `started_at` 과 다른 사실이다(`persistence.py:947-948`) | 생성 4경로가 입력값을 넣는다(`B/platform/work_tasks.py:400`, `:2012`, `:2404`, `:2549`). 수정 `PATCH` 가 바꾼다(`B/modules/work/application.py:602`). **시작 전이 `open→in_progress` 때 비어 있으면 오늘(Asia/Seoul)로 채운다**(`B/modules/work/lifecycle.py:165-171`, `application.py:2068`, 오늘 `B/modules/work/task_projection.py:30-32`) |
| `due_date` | Date | 기한 | 생성 4경로(`work_tasks.py:401`, `:2013`, `:2405`, `:2550`). 수정 `PATCH`(`application.py:603`). 조건 변경 제안 **동의**(`:2321-2324`) |
| `started_at` | timestamptz | **실제** 시작 시각 = `open→in_progress` 를 부른 순간. `open` 에서 바로 완료하면 비어 있다(`persistence.py:947-949`) | 전이로 `IN_PROGRESS` 가 되고 아직 비어 있을 때만(`application.py:2075-2076`). 재개·막힘 해제로는 다시 찍히지 않는다. 요청 수락도 채우지 않는다(`work_tasks.py:1886`) |
| `completed_at` | timestamptz | 완료 명령 성공 시각. 요청 업무에서는 **완료 보고 제출** 시각이고 승인 시각이 아니다(`persistence.py:950-952`) | 직접 완료(`application.py:2077-2078`), 완료 보고 제출(`:1899-1901`). **지운다**: 보완 요청(`:1935`), 재개(`:2146`) |
| `reopened_at` | timestamptz | 마지막으로 다시 연 시각. 이전 승인을 무효로 가르는 기준선(`persistence.py:953-955`) | 재개(`application.py:2145`) |
| `created_at` | timestamptz | 행 생성 | 생성 4경로(`work_tasks.py:407`, `:2036`, `:2409`, `:2554`) |
| `updated_at` | timestamptz | 마지막 변경 | `touch()` 가 매번(`work_tasks.py:1329-1331`) |

**업무 밖에 있는 관련 시각**
- `task_assignments.accepted_at` — 담당이 선 시각. 본인 생성·배정은 생성 순간, 요청은 수락 순간이다(`persistence.py:1802`, `work_tasks.py:419`, `:1920`, `:2062`, `:2568`). 응답은 `assignment.accepted_at` 이다(`application.py:2898`).
- `task_schedules(on_date, starts_at, ends_at, released_at)` — 캘린더의 **시간 배정**이다. 업무 날짜가 아니다(`persistence.py:1053-1104`).
- `task_proposals(created_at, responded_at)`(`persistence.py:1844-1845`), `work_requests(start_date, due_date)`(`persistence.py:1658-1659`).
- 완료 **승인** 시각은 `tasks` 에 없다. 승인은 `state` 를 바꾸지 않고, 판단 행(`record_delivery_decision`)이 그 시각을 갖는다(`application.py:1909-1920`, 주석 `persistence.py:950-951`).

**「시작」이 예정일인가 실제인가**
- `start_date` 는 계획이고 `started_at` 이 실제다. 응답 `_view` 주석도 같다(`application.py:2798`).
- 단, 계획 칸이 비어 있던 업무는 시작 순간 `start_date` 에 **실제 시작일이 들어간다**(`lifecycle.py:165-171`). 그 뒤로는 두 값이 구분되지 않는다.

**생성 경로 4개와 출처**(`TaskRecord(` 생성자 4곳)

| 경로 | 생성자 | `origin_kind` | 날짜 입력 |
|---|---|---|---|
| 본인 업무(`POST /api/tasks`, AX `task.create_self`) | `create_self_task` `work_tasks.py:365-433` | `direct` | start·due |
| 요청 발송(`POST /api/work-requests`, AX `work_request.create`, 회의 할 일 승격) | `create_task_for_request` `:1975-2075` | `request_effect`/`meeting` | 요청의 start·due 를 복사 |
| 프로젝트 계획(`POST /api/projects/{id}/tasks`) | `create_unheld_task` `:2381-2420` | `project_plan` | `ProjectWorkInput.start_date/due_date`(`B/modules/work/project_commands.py:51-56`) |
| 관리자 배정(`POST /api/tasks/assign`, AX `task.assign`) | `create_assigned_task` `:2519-2580` | `assignment` | start·due |

- 회의 할 일 승격 입력 `MeetingTodoPromotionInput` 이 `due_date`·`start_date` 를 받아 요청 생성으로 흘린다(`B/modules/meetings/commands.py:250-275`).

### 3-2. 상태 전이 때 시각이 이력에 남나 — 남는다(세 표에)

| 표 | 무엇이 남나 | 쓰는 곳 |
|---|---|---|
| `activity_events` | `event_kind`(`task.state_changed`·`task.completion_submitted`·`task.completion_accepted`·`task.completion_changes_requested`·`task.reopened`·`task.updated` …), `before_ref`(`task:<id>@<ver>:<state>`), `after_ref`, `reason`, `causation_ref`, **`occurred_at`** | 모델 `persistence.py:1236-1256`. writer `ActivityLedger.record` `work_tasks.py:258-290`. 업무 쪽 진입 `record_activity` `work_tasks.py:980-987`(`application.py` 안 18곳). 전이 `application.py:2083-2090`(`task.state_changed` `:2086`), 완료 보고 `:1904-1906`, 인정 `:1920`, 보완 `:1938-1940`, 재개 `:2150-2153`, 합의 취소 `:2307-2309`, 제안 동의 `:2336-2339` |
| `task_versions` | 회차마다 스냅샷 1행(`change_kind`, `actor_id`, `reason`, `captured_at`, `snapshot`) | `persistence.py:1604-1622`, `work_tasks.py:989-1010`. **스냅샷에 `start_date`·`due_date`·`state` 는 있지만 `started_at`·`completed_at`·`reopened_at` 은 없다**(`work_tasks.py:1054-1078`). diff 비교 대상도 `title·description·state·block_reason·start_date·due_date` 뿐이다(`application.py:2903`) |
| `task_activities` | `(task_id, task_version, state, occurred_at)` — `touch()` 와 생성·수락·종료·배정 때마다 | `persistence.py:1625-1632`. 쓰기 11곳 `work_tasks.py:422`, `:1331`, `:1929`, `:1965`, `:2042`, `:2414`, `:2447`, `:2577`, `:2686`, `:2768`, `:2824`. 읽는 곳은 **일일보고 작업 기록**(그날 발생분, `work_tasks.py:1333-1355`) 하나다 |

- 이력 응답: `GET /api/tasks/{id}/history` = `versions[]`(+`captured_at`) + `activity[]`(+`occurred_at`) (`application.py:2384-2419`), `GET …/history/diff`(`:2421-2427`). MCP `task_history`(`B/entrypoints/mcp.py:1977`)도 같은 응답이다.

### 3-3. 날짜를 바꾸는 서버 명령 전부

| 명령 | 바뀌는 날짜 | 권한 조건 | 결재(승인) | 이력 | 근거 |
|---|---|---|---|---|---|
| `PATCH /api/tasks/{id}` (`update`) | `start_date`·`due_date`(+제목·내용·프로젝트·상위·선행·결재자) | `TASK_SELF_MANAGE` + **활성 담당자**(`repository.task` = `_held_by`). 취소된 업무 불가. `validate_schedule`(시작>마감 거절) | **없음**(주석 "no approval gate") | `task.updated` 「업무 내용 수정: … (바뀐 키)」 + 스냅샷. **사유 칸 없음** | `B/entrypoints/http.py:1533-1538`, `B/modules/work/application.py:528-610`, `B/platform/work_tasks.py:1090-1096`, 입력 `B/modules/work/task_commands.py:124-158` |
| AX `task_update` → `task.update` 제안 → 확정 시 위 `update` | 같음 | 위 + `ACTION_DECIDE` 로 확정 | 사람 확인 카드 | 위 + `causation_ref` | `B/entrypoints/mcp.py:789-795`, `B/platform/actions.py:837-844` |
| 시작 전이 `POST /api/tasks/{id}/start`(AX `task_start`) | 비어 있던 `start_date` ← 오늘, `started_at` ← 지금 | `TASK_SELF_MANAGE` + 활성 담당자. 선행 게이트 | 없음 | `task.state_changed` | `B/entrypoints/http.py:2541`, `application.py:2013-2089`, `lifecycle.py:107-171` |
| 완료 / 완료 보고 / 보완 요청 / 재개 | `completed_at` 찍기·지우기, `reopened_at` | 완료: 담당자. 보고: 담당자(요청 업무). 보완·인정: 요청자(판단함). 재개: 본인 업무는 담당자, 요청 업무는 요청자 | 요청 업무 완료는 요청자 확인을 거친다 | 각각의 `event_kind` | `application.py:1868-1940`, `:2077-2078`, `:2113-2169` |
| 조건 변경 제안 `POST /api/tasks/{id}/proposals`(`terms_change`) → 응답 `…/respond` | 동의하면 **`due_date` 만**(+제목·내용). `start_date` 는 받지 않는다 | 제안: **요청자만**(`:2190-2191`). 응답: **담당자만**(`:2245-2247`) | 상대 동의가 결재 역할 | 동의 시 `task.updated` 「조건 변경 동의」 + `reason` | `B/entrypoints/http.py:1887-1931`, `application.py:2173-2257`, 적용 `:2295-2340`. AX `task_proposal_open/respond` `mcp.py:1889-1895` |
| 요청 수정 `POST /api/work-requests/{id}/amend` | `work_requests.due_date`(+제목·내용) | 요청자, 요청 `state=pending` 일 때만(`B/modules/work/request_lifecycle.py:129-140`) | 없음 | 새 Submission 회차 + 감사 `work_request.amended` | `B/entrypoints/http.py:2147`, `B/modules/work/requests.py:564-616`, `:630-648`. **업무 행의 `due_date` 를 고치는 줄은 이 경로에서 찾지 못했다**(`requests.py:630-648`, `work_tasks.py:1710-1780`) |
| 요청 재상신 `…/resubmit` | 같음 | 요청자, `state=negotiating` 일 때만 | 없음 | 감사 `work_request.resubmitted` | `B/entrypoints/http.py:2133`, `requests.py:650-684` |
| 요청 협의 `…/negotiate` | 날짜를 바꾸지 않는다. `conditions` 에 저장만 | 수신자(`WORK_REQUEST_DECIDE`) | — | 감사 `work_request.negotiated` | `requests.py:534-562` |
| 시간 배정 `POST /api/tasks/{id}/schedules`, retime·release | `task_schedules` 만. 업무 날짜는 아니다. retime 은 `on_date` 를 받지 않는다 | 배정 가능한 사람 | 없음 | — | `B/entrypoints/http.py:1736`, `B/modules/work/task_commands.py:222-240` |

- 캘린더 띠 끌기·손잡이 전용 엔드포인트는 없다. SPEC-004 도 `PATCH /api/tasks/{id}` 를 쓴다고 적는다(`SPEC/spec-004-calendar-scheduling.md:1090`).
- `task.due_date =` 쓰기는 2곳(`application.py:603`, `:2323`), `task.start_date =` 는 2곳(`:602`, `:2068`), `task.started_at =` 1곳(`:2076`), `task.completed_at =` 4곳(`:1901`, `:1935`, `:2078`, `:2146`), `task.reopened_at =` 1곳(`:2145`)이다.
- 날짜가 바뀌면 기간 밖 시간 배정을 닫는다(`_schedule_release_for`). 거는 자리는 3곳이다: 수정 `:604`, 시작 전이 `:2081`, 제안 동의 `:2333`.

### 3-4. 날짜를 내보내는 API 응답 전부

업무 한 건의 기본 투영은 `TaskApplication._view` 다(`B/modules/work/application.py:2767-2832`, 타입 `B/modules/work/task_results.py:66-98`).
여기에 날짜·시각 7개가 실린다: `start_date`·`due_date`·`created_at`·`updated_at`·`started_at`·`completed_at`·`reopened_at`, 그리고 `assignment.accepted_at`.

| 엔드포인트 / 도구 | 주는 날짜 필드 | 근거 |
|---|---|---|
| `GET /api/tasks/{id}` (상세, 담당자) | `_view` 7개 + `assignment.accepted_at` + 체크리스트 항목 `completed_at` | `http.py:2025`, `application.py:1115-1125`, `:2680-2687`, `:3000` |
| `GET /api/tasks/{id}` (읽기 전용 갈래) | `_view` 7개 | `application.py:1127-1175` |
| `GET /api/tasks` · `GET /api/my-work` (목록·홈) | `_view` 7개 + `derived.overdue_days`(`due_date` 로 계산) | `http.py:2015`, `:693`, `application.py:1095-1115`, `:1240` |
| `GET /api/calendar` | 업무 행: `start_date`·`due_date`·`span_from`·`span_to`·`schedules[]`(on_date·시각). **`started_at`·`completed_at` 없음** | `http.py:1782`, `application.py:951-993` |
| `GET /api/projects/{id}` (프로젝트 업무 표·간트 원천) | `start_date`·`due_date`(+기간 정규화는 화면) | `http.py:1417`, `B/modules/work/projects.py:417-450` |
| `GET /api/tasks/{id}/children` · 상세의 하위·후행·참고 | `due_date` 만 | `application.py:1733-1747`, `:1510-1545`, `:2713-2723` |
| `GET /api/graph/*` | 업무 노드 `date = due_date or start_date`, 요청 노드 `date = due_date` | `http.py:1794-1817`, `B/modules/work/graph.py:683`, `:754` |
| `GET /api/tasks/{id}/history` | 스냅샷 `start_date`·`due_date`, `captured_at`, activity `occurred_at` | `application.py:2384-2419` |
| `GET /api/tasks/{id}/proposals` | `created_at`·`responded_at`, `payload.due_date` | `application.py:2284-2293`, `:2847-2858` |
| `GET /api/task-assignments/sent` · 배정 | 배정 `created_at`·`accepted_at`·`declined_at` + `task`(=`_view`) | `http.py:1510`, `B/modules/work/assignments.py:436-470` |
| `GET /api/work-requests*` | 요청 `start_date`·`due_date` | `B/modules/work/requests.py:1439-1442` |
| `GET /api/action-items` (AX 초안) | 초안 `start_date`·`due_date`(preview·edit_contract) + `created_at` | `B/platform/actions.py:1385-1386`, `B/platform/action_center.py:759` |
| 일일보고 작업 기록(내부 원천) | `task_activities.occurred_at`·`state` (그날 것) | `B/platform/work_tasks.py:1337-1355` |
| MCP `my_task_list`·`task_list`·`task_get`·`task_history` | 각각 `/api/my-work`·`/api/tasks`·`/api/tasks/{id}`·history 와 같은 응답 | `B/entrypoints/mcp.py:1968-1978` |
| 홈 | 전용 엔드포인트 없음. 화면이 `/api/my-work` 를 쓴다 | `F/features/today/TodayPage.tsx:101` |

- MCP 에 캘린더 도구는 없다(`B/entrypoints/mcp.py` 에서 `calendar` 0건).

### 3-5. SPEC 과의 차이

| 항목 | SPEC | 코드 |
|---|---|---|
| 기한 두 값 | 「계획/실제 기한 두 값」이 SPEC-001 계승 계약이다(`SPEC/spec-003-task-lifecycle-v2.md:105`, `:326`). 상세 응답 `due_planned · due_actual`(`:716`, `SPEC/spec-001-work-management.md:754`). `due_date` = **계획 기한, 생성 시점 박제**(`spec-001:736`, `spec-003:645`) | 기한은 `due_date` **한 값**(`persistence.py:919`). `due_planned`·`due_actual` 0건. `due_date` 는 `PATCH` 로 바뀐다(`application.py:603`) — 박제되지 않는다. SPEC-001 도 「실제 기한 필드와 계획 기한 박제 — 현행 기한은 한 값」을 신규 계약 표에 적어 두었다(`spec-001:714`) |
| 실제 기한 변경 권한·사유 | **담당자만, 사유 필수**(`spec-001:678`, `:862-864`, `:898`, `spec-003:746`) | `PATCH` 는 활성 담당자만 맞다. 그러나 **사유 칸이 없다**(`task_commands.py:46-71`, `:124-143`) |
| 시각 다섯 | `created_at`·`accepted_at`·`started_at`·`completed_at`·`reopened_at`. `started_at` = `open→in_progress` 시각(`spec-003:898-900`) | 넷은 `tasks` 에 있다. `accepted_at` 은 `task_assignments` 에 있고 `assignment.accepted_at` 으로 나간다(`application.py:2898`) |
| 수락 뒤 `started_at` | 수락은 `started_at` 을 채우지 않는다(`spec-003:658`, `:1110`) | 같다(`work_tasks.py:1886`) |
| 시작 전이가 시작일을 채운다 | SPEC-004 가 그 동작을 날짜 변경의 하나로 적는다(`spec-004:1206`, `:405-421`) | 같다(`lifecycle.py:165-171`) |
| 상세 메타 | 「담당 · 기한 · 시작 · 결재 · 참조」(`SPEC/spec-007-task-detail.md:232`). 「시작」이 계획인지 실제인지는 그 줄에 적혀 있지 않다 | 응답은 둘 다 준다(`start_date`·`started_at`) |
| 캘린더 | 업무는 날짜 단위 `start_date`·`due_date`, 시간 단위는 배정(`spec-004:29`). 행 필드 `start_date·due_date·span_from·span_to·…`(`spec-004:937`) | 같다(`application.py:983-991`) |
| 요청 수정 | `PATCH /api/work-requests/{id}`, 수락 전 요청자(`spec-003:534`) | 경로는 `POST /api/work-requests/{id}/amend` 이고 `state=pending` 일 때만이다(`http.py:2147`, `request_lifecycle.py:132-140`). 바꾸는 것은 요청 행의 `due_date` 다(3-3 참고) |

---

## 4. E2E-3 · E2E-4 출처 정보(한 줄)

`_view` 의 `lineage.source_action_item_id`(`B/modules/work/application.py:2829`; 생성 4경로 모두 채움 `B/platform/work_tasks.py:410`, `:2029`, `:2557`)가 AX 초안 출처다. 목록·상세의 `origin` 은 AX 출처를 `kind:"self_created"`, `source:{type:"action_item", id, title}` 로 낸다(`application.py:2467-2471`, `:2501-2509`; `ACTION_READ` 가 있고 그 제안의 주인일 때만). 업무 요청에서 나온 업무는 `origin` 이 `work_request` 를 먼저 택하므로(`:2459-2466`) AX 출처가 `origin` 에는 나오지 않는다. 요청 행(`work_requests`)에는 AX 출처 열이 없다.

---

## 5. grep 개수표

| 요청 | 심볼 / 패턴 | 범위 | 개수 |
|---|---|---|---|
| E2E-1 | `checklist` | `B/entrypoints/mcp.py` | 41 |
| E2E-1 | `checklist` | `B/platform/actions.py` | 36 |
| E2E-1 | `checklist` | `B/modules/ax_execution/tool_catalog.py` | 18 |
| E2E-1 | `checklist` | `B/modules/work/creation_commands.py` | 7 |
| E2E-1 | `checklist` | `B/modules/work/task_creation.py` | 5 |
| E2E-1 | `checklist` | `B/platform/action_center.py` | 2 |
| E2E-1 | `checklist` | `B/platform/codex_cli.py` | 1 (진행 기록 지침) |
| E2E-1 | `checklist` | `B/modules/actions/confirmation.py` · `B/modules/work/drafts.py` | 0 · 0 (모델 통째로 검증) |
| E2E-1 | `"id": "checklist"` (preview 1 + 편집 필드 3) | `B/platform/actions.py` | 4 (`:1404`, `:1797`, `:1824`, `:2023`) |
| E2E-1 | `def _*edit_contract` | `B/platform/actions.py` | 4 (`:1658`, `:1846`, `:1936`, `:2049`) |
| E2E-1 | `normalize_ax_draft(` 호출 | `B/` | 3 (`action_center.py:593`, `confirmation.py:198`, `:203`) |
| E2E-1 | `never invent` | `tool_catalog.py` | 2 |
| E2E-1 | `leave (it\|a value) empty` | `tool_catalog.py` | 4 |
| E2E-1 | `the conversation gives you` | `tool_catalog.py` | 2 |
| E2E-1 | `지어내\|추측하지\|채우지 않` | `codex_cli.py` | 6 |
| E2E-1 | 프롬프트 정책 절 | `codex_cli.py:508-516` | 6 |
| E2E-2 | `@app.* "/api/action-items` | `B/entrypoints/http.py` | 6 |
| E2E-2 | `@app.* "/api/actions` | `B/entrypoints/http.py` | 2 |
| E2E-2 | `@app.websocket` | `B/entrypoints/http.py` | 1 (회의 스트림) |
| E2E-2 | `SubmissionRecord(` 생성 | `action_center.py` · `actions.py` | 1 (회차) · 1 (첫 회차) |
| E2E-2 | `_canonical_payload` | `B/platform/actions.py` | 3 (정의 1, 사용 2) |
| E2E-5 | `TaskRecord(` 생성자 | `B/platform` | 4 |
| E2E-5 | `task.started_at =` | `B/` | 1 |
| E2E-5 | `task.completed_at =` | `B/` | 4 |
| E2E-5 | `task.reopened_at =` | `B/` | 1 |
| E2E-5 | `task.start_date =` | `B/` | 2 |
| E2E-5 | `task.due_date =` | `B/` | 2 |
| E2E-5 | `request.due_date =` | `B/` | 1 |
| E2E-5 | `TaskActivityRecord(` 쓰기 | `B/platform/work_tasks.py` | 11 |
| E2E-5 | `record_activity(` | `B/modules/work/application.py` | 18 |
| E2E-5 | `"due_date": ` 응답 키 | `B/modules/work` | 9 |
| E2E-5 | `due_planned\|due_actual` | `B/` | 0 |
| E2E-3·4 | `source_action_item_id` | `B/modules/work/application.py` | 6 |

---

## 6. 조사 한계

- **E2E-1 원인은 추정이다.** 운영 대화의 실제 도구 호출 인자(`tool_invocations.input_summary`), AX 제안 payload, codex 세션 로그를 보지 않았다(운영 접속 금지). 「AI 가 `checklist` 를 비워 보냈다」는 서버가 체크리스트를 버리지 않는다는 코드 사실과 지시문 문장에서 끌어낸 결론이다. 확정하려면 그 대화의 `action_items.payload`(또는 Submission 1회차 스냅샷)에 `checklist: []` 가 있는지 봐야 한다.
- 모델(Codex/Claude)이 도구 설명과 정책 중 어느 쪽을 더 따르는지는 코드로 답할 수 없다.
- 프론트가 초안 카드·수정 모달에서 체크리스트를 어떻게 보여 주고 보내는지(빈 배열 처리, 「저장」 버튼 연결)는 읽지 않았다. frontend 리포트 몫이다.
- `docs/unified-operations-inventory.json` 의 도구 설명 캡처가 카탈로그와 일치하는지는 대조하지 않았다(테스트를 돌리지 않았다).
- 3-3 「요청 수정이 업무 행의 `due_date` 를 고치지 않는다」는 `requests.py:564-684`와 `work_tasks.py:1710-1780`을 읽고 낸 결론이다. 다른 훅이 같은 transaction 에서 업무 행을 고치는지는 전수 추적하지 않았다.
- 완료 승인 시각을 담는 판단 행(`record_delivery_decision`)의 정확한 표·열은 열어 보지 않았다.
- 일일·주간 보고서 생성(AI)이 업무 날짜를 프롬프트에 싣는지는 보지 않았다. `B/platform/reports.py` 와 `B/modules/reports/*` 에 `due_date`·`start_date` 문자열은 0건이다.
