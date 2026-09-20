# W1 backend 결과 보고 — 2026-09-16

## 상태: done (코드·테스트 완료 / docs 2건은 allowed_paths 밖이라 코디 담당)

---

## 1. 수행 내용 — 제품 코드

### 새 파일

| 파일 | 역할 |
|---|---|
| `backend/src/ax_workspace/modules/work/creation.py` | **순수 결정 함수** — `decide_task_creation`(경로 셋·역량·수신자 검사 종류), `require_idempotency_key`, `creation_fingerprint`, `followup_idempotency_key`. 명령 종류 상수(`task.create`·`task.assign`·`work_request.create`) |
| `backend/src/ax_workspace/modules/work/creation_commands.py` | `TaskCreationApplication` — 세 생성 명령(`create_task`·`create_work_request`·`assign_task`)이 같은 결정·같은 멱등 원장을 지나고, 실제 생성은 소유 application 에 위임 |

### 스키마 (모델 metadata 만 — migration 도입 없음, `reset_demo` 가 여전히 유일한 소유자)

- `persistence.py` `TaskCreationAttemptRecord` (표 `task_creation_attempts`) — `UniqueConstraint(actor_id, command_kind, request_key)` + `payload_fingerprint` + `task_id`/`work_request_id`.
  `meeting_room_creation_attempts` 와 같은 모양. **기존 전역 `causation_key` 열은 뜻이 달라 그대로 두었고 동작을 바꾸지 않았다.**
- `persistence.py` `TaskAssignmentRecord` — 부분 unique 인덱스 `uq_task_assignments_active` (`task_id` WHERE `status='active'`). **활성 담당 유일성은 DB 제약**이고 application 검사로 낮추지 않았다.
- `persistence.py` `TaskRecord.approver_id` (nullable) — **열만** 만들었다. 입력 모델·응답·FE 어디에도 없다(W2 가 연다).

### 생성 계약

- `task_creation.py` `TaskCreateInput.assignee_id` (optional, ≤100자) 추가. `extra='forbid'` 유지 →
  본문 `idempotency_key`·`approver_id`·미지 필드는 계속 422.
- `TaskCreationApplication.create_task` — 키 검증 → 입력 정규화 → 결정 → **역량 검사** → **수신자 허용 판정**
  → 원장 claim → self 는 `TaskApplication.create_self`, horizontal 은 `WorkRequestApplication.create` 위임 → 업무 투영 반환.
  담당을 지정한 생성이 받지 않는 값(`start_date`·`parent_task_id`·`project_id`)은 **조용히 버리지 않고 422 로 거절**한다.
- 영수증은 **생성이 냈던 것과 같은 투영**이다 (`TaskApplication.creation_receipt` / `WorkRequestApplication.receipt`),
  돌려주기 전에 `get` 으로 열람 권한을 다시 검사하므로 잃었으면 `TaskNotFound`(404, 존재 은닉).
- 충돌: 같은 키 + 다른 지문 → `TaskIdempotencyConflict` → 409. 키 누락·빈 값 → `TaskIdempotencyKeyRequired` → 422.
  권한 밖 수신자 → `TaskRecipientNotAllowed` → 403. (`http.py` `_runtime_error` 에 `TaskError` 보다 **먼저** 매핑)

### 동시성 (원자성 포함)

- 업무 + 활성 담당 + 원장 한 줄이 **한 transaction**. 중간 실패 시 셋 다 남지 않는다.
- `claim()` 은 SAVEPOINT 를 쓰지 않는다 — pysqlite 에서 savepoint 가 바깥 transaction 과 함께 되돌아가지 않아
  실패한 생성의 원장 줄이 남았다(실측). 대신 보이는 행이 없으면 insert 하고, 동시 실행의 진 쪽은
  **commit 에서 unique 위반**으로 transaction 을 통째로 잃는다.
- `WorkflowApplication._created_once` 가 `IntegrityError` 를 받아 새 session 에서 영수증을 다시 읽는다.
  **원장에 그 키가 없으면 다른 제약이 깨진 것이므로 원래 오류를 그대로 올린다** — 영수증으로 위장하지 않는다.

### 권한 (Phase 3)

- `organization_access.py` `work_request_assignee_candidates` 에서 **`work_request.decide` 필터 한 줄만** 걷었다.
  남은 셋(로그인 가능 `_can_answer` · 본인 제외 · 조직 범위 교집합)은 그대로.
- 역할 카탈로그를 **건드리지 않았다** — 일반 구성원에 `task.assign`·`work_request.decide` 를 주지 않았다.
- 명령과 목록이 같은 함수(`is_work_request_assignee`)를 지난다.
- 과거 pending 행의 수락·거절·조정은 여전히 `work_request.decide` 를 요구한다(테스트로 고정).

### 수락 gate 제거 (Phase 4)

- `work_tasks.py` `create_request` — 상태 `pending` → **`assigned`**, `DecisionItemRecord`·`SubmissionRecord`·
  `ReviewAssignmentRecord` 세 줄 생성 제거. Subject/SubjectVersion(내용의 판)은 그대로 남긴다.
  이어서 `create_task_for_request(request)` 로 업무 + 활성 담당을 같은 transaction 에 세운다.
- `create_accepted_task` 는 `create_task_for_request` 의 얇은 wrapper 로 남겼다(과거 pending 행의 수락 경로).
- `create_assigned_task` — `status="pending"` → **`"active"` + `accepted_at`**, `_open_assignment_acceptance` 호출 제거.
- **`_open_assignment_acceptance` 자체는 지우지 않았다** — 담당자 변경(`reassign`/`hand_to`)이 계속 쓴다.
  담당자 변경은 W1 범위 밖이라 현행(수락 대기) 그대로다.
- `assigned` 읽기 자리 전수 확인: 수신함(`work_tasks.py:inbox_for`)·`_decision_target`·`request_lifecycle`
  수정/재상신/철회 가드 모두 이미 `assigned` 를 거부한다 → **정의된 422**, side effect 없음(테스트로 고정).

### 회의 후속 승격 (Phase 5)

- `promote_meeting_todo`(실제 live 경로)가 `TaskCreationApplication.create_work_request` 를 지난다. HTTP·MCP 모두 키 필수.
- `modules/meetings/followups.py` 도 우회 호출을 걷고 `TaskCreationApplication` + 후보 identity 안정 키를 쓰게 고쳤다.
  ⚠ **이 모듈은 현재 레포에서 도달 불가능한 死코드다** — 아래 § 5 참고.

### 표면 (Phase 6)

- REST: `POST /api/tasks`(+`assignee_id`) · `POST /api/tasks/assign` · `POST /api/work-requests` ·
  `POST /api/meetings/{id}/todos/{id}/promote` 넷 다 `Idempotency-Key` **헤더 필수**.
- MCP: `task_create_self`(+`assignee_id`) · `task_assign` · `work_request_create` · `meeting_todo_promote` 넷에
  `idempotency_key` **필수 명시 인자**. 스키마 description 에 「한 생성 의도에 키 하나 · 재시도는 같은 키 · 새 의도는 새 키」를 적었다.
- **공용 `_mutation_key` 는 그대로다.** 일일보고 초안·회의 예약 fallback 의 기존 멱등 의미를 건드리지 않았고,
  W1 네 도구는 그 helper 를 더는 쓰지 않는다(그 helper 는 turn 을 가리켜서 한 turn 의 두 생성을 한 건으로 합쳐 버린다).
  이 사실을 테스트가 소스 수준에서 고정한다.
- AX 실행(`platform/actions.py`): `task.create_self`·`task.assign`·`work_request.create` 가
  `TaskCreationApplication` 을 지나고 `idempotency_key=str(action.id)` 를 싣는다. 기존 `causation_key=str(action.id)` 도 보존.
- AX 초안 정규화(`drafts.TASK_DRAFT_FIELDS`)는 `TaskCreateInput.model_fields` 에서 나오므로 `assignee_id` 가 자동 반영.
- seed/scenario: 요청·배정 뒤 수락 단계 제거, 생성마다 안정 키. CSV 의 `accept` 열은 과거 dataset 호환으로 **읽기만** 한다.

---

## 2. 검증 결과 (수치)

| 명령 | 결과 |
|---|---|
| `make test-unit` | **319 passed, 3 failed** — 실패 셋은 전부 `tests/architecture/test_operation_inventory.py` (docs 갱신 필요, § 4) |
| `make test-contract` | **969 passed / 0 failed** (contract 단독 run, `scratchpad/contract5.txt`). 전체 run 과 섞으면 자료 worker 타이밍 테스트 1건이 회차마다 다르게 흔들린다 — § 6 |
| `make test-scale` | **13 passed** |
| `make test-release` | **1 passed** |
| `make test-postgres` (격리 `ax_test_w1`) | **65 passed, 0 failed** |
| `make test` (전체, `-n auto`) | 1286 passed / 5 failed = inventory 3 + 자료 worker 타이밍 2 (§ 6) |

로그: `/private/tmp/claude-501/-Users-kknaks-orca-workspaces-Strong-hajin-strong-hajin-work/058c5706-74ff-427d-8d3f-0e62a49238d8/scratchpad/`
(`final-unit.txt` · `contract5.txt` · `final-contract2.txt` · `final-scale.txt` · `final-release.txt` · `postgres2.txt` · `full3.txt` · `baseline.txt` · `baseline2.txt`)

### 격리 DB

```
make postgres-up                       # compose project strong-hajin-work (신규 볼륨, 사용자 데이터 없음)
CREATE DATABASE ax_test_w1
make reset-demo   DATABASE_URL=postgresql+psycopg://ax:ax@localhost:54329/ax_test_w1
make test-postgres POSTGRES_TEST_URL=postgresql+psycopg://ax:ax@localhost:54329/ax_test_w1
```

`ax_demo` 는 **한 번도 건드리지 않았다**. 실제로 선 제약:

```
uq_task_assignments_active         UNIQUE (task_id) WHERE status = 'active'
uq_task_creation_actor_command_key UNIQUE (actor_id, command_kind, request_key)
tasks.approver_id                  존재
```

### Phase 별 증거

| Phase | 증거 |
|---|---|
| 1 결정 함수 | `test_task_creation_contract.py::test_the_one_decision_names_the_route_and_the_checks_each_path_still_has` · `..._a_creation_key_is_required_and_never_invented_by_the_server` · `..._the_creation_body_takes_the_recipient_and_still_refuses_what_it_never_took` |
| 2 멱등·원자성·유일성 | `..._every_creation_surface_refuses_a_missing_or_blank_key` · `..._the_same_key_is_a_receipt_a_different_payload_is_a_conflict_and_a_new_key_is_a_new_task` · `..._one_key_belongs_to_one_actor_and_one_command` · `..._a_receipt_is_withheld_from_a_caller_who_may_no_longer_read_it` · `..._the_task_and_its_active_assignment_stand_in_one_transaction` · `..._the_active_assignment_uniqueness_is_a_database_constraint` · PG: `test_postgres_makes_one_task_when_the_same_creation_key_arrives_twice_at_once` · `test_postgres_refuses_a_second_active_assignment_at_the_database` |
| 3 권한 | `..._a_member_with_neither_assign_nor_decide_may_send_work_to_a_peer` · `..._the_candidate_list_and_the_command_answer_the_same_question` · `..._sending_work_never_widens_what_a_person_may_change` · `..._manager_assignment_keeps_its_own_capability_and_organization_scope` · `..._past_pending_rows_still_need_the_judgement_capability` |
| 4 수락 gate | `..._no_creation_path_opens_an_acceptance_round` · `..._a_new_request_stands_as_assigned_and_takes_no_round_command` · `..._the_request_origin_and_its_completion_reviewer_survive` · `test_task_assignments.py::test_a_new_assignment_takes_no_acceptance_or_decline_command_and_nothing_changes` |
| 5 승격 | `test_meeting_finalize.py::test_the_promoted_request_carries_the_source_columns_onto_the_task` · `..._a_promoted_request_carries_the_meeting_onto_the_task_at_once` · PG: `test_postgres_promotes_one_meeting_candidate_into_one_task_under_concurrency` |
| 6 표면 | `..._rest_and_mcp_create_the_same_thing_under_the_same_key_rules` · `..._every_w1_tool_takes_the_key_as_an_explicit_argument` · `..._a_non_w1_mutation_keeps_its_own_idempotency_meaning` · `..._seed_data_carries_no_pending_assignment_or_acceptance_round` · `..._an_ax_proposal_creates_nothing_until_a_person_confirms_it` |

---

## 3. 테스트 이관 — 없앤/대체한 테스트별 근거

### 과거 모양 fixture

`backend/tests/legacy_acceptance.py` (신규, **테스트 전용**) — `pending_request` · `make_request_look_pending` ·
`pending_assignment` · `make_assignment_look_pending`. 제품 코드에는 복원 경로·fallback 을 **두지 않았다**.
이 helper 는 「예전 배포가 남긴 행」을 세울 뿐이고, 신규 생성이 그 모양을 다시 만든다는 뜻이 아니다.
덕분에 판단 회차·근거·조정·재상신·영수증을 다루는 **살아 있는 코드의 검증을 하나도 잃지 않았다.**

### 이름이 바뀐(=계약이 바뀐) 테스트

| 기존 이름 | 기존 목적 | 지금 |
|---|---|---|
| `test_direct_task_and_accepted_request_carry_an_active_assignment` | 수락된 요청이 활성 담당을 만든다 | `..._and_sent_request_...` — 요청이 서면 바로 활성 담당. + 판단·판정 0건 단언 추가 |
| `test_manager_assignment_enters_my_work_only_after_the_assignee_accepts` | 배정은 수락 후 목록에 | `test_manager_assignment_enters_my_work_at_once` — 즉시 목록·즉시 시작, 수락 항목 0건, lineage 가 없는 판단을 가리키지 않음 |
| `test_declined_assignment_never_enters_my_work_and_records_the_reason` | 거절이 업무를 취소한다 | `test_a_new_assignment_takes_no_acceptance_or_decline_command_and_nothing_changes` — 신규 배정에 수락·거절을 걸면 **422 + side effect 0** (DEC-001 D-4). 과거 행의 거절 자체는 `test_legacy_assignment_confirmation.py`(무변경)와 `test_postgres_assignment_decision_replay.py`(과거 모양 fixture)가 계속 덮는다 |
| `test_accepting_the_same_request_twice_creates_exactly_one_task` | 수락 두 번 → 업무 1건 | `test_resending_the_same_request_creates_exactly_one_task` — 같은 멱등 키 재전송 → 요청·업무 1건 |
| `test_an_accepted_request_names_the_requester_...` | 수락된 업무의 출처 | `test_a_sent_request_names_the_requester_...` — 수락 단계만 빠지고 출처 단언 그대로 |
| `test_work_request_creates_a_task_only_after_the_assignee_accepts` | 수락 전 업무 없음 | `test_work_request_creates_a_task_without_waiting_for_the_assignee` — `assigned` + `task_id` + 판단함 0건 |
| `test_request_opens_thread_subject_submission_and_assignment` | 요청이 스레드·판·회차를 연다 | 둘로 갈랐다: `test_a_new_request_opens_a_thread_and_a_task_but_no_judgement_round`(신규) + `test_a_past_pending_request_keeps_its_round_and_its_reviewer`(과거 행, **원래 단언 전부 보존**) |
| `test_request_due_date_flows_into_the_accepted_task` | 요청 기한이 수락된 업무로 | `..._into_the_requested_task` — 수락 단계만 제거 |
| `test_accepting_the_request_carries_the_source_columns_onto_the_task` / `test_accepting_a_promoted_request_still_carries_...` | 수락이 회의 출처를 업무로 옮긴다 | `test_the_promoted_request_carries_the_source_columns_onto_the_task` / `test_a_promoted_request_carries_the_meeting_onto_the_task_at_once` — 출처 두 열 단언 그대로, 수락 단계만 제거 |
| `test_ax_task_assignment_uses_the_same_editor_but_keeps_assignee_acceptance_separate` | AX 확인 후 수락이 따로 남는다 | `..._and_stands_at_once` — 편집 계약·미리보기 단언 그대로, 뒤가 「즉시 활성 담당 + 수락 항목 0건」으로 |
| `test_ax_task_assignment_can_be_cancelled_by_the_requester_only_before_acceptance` | 수락 전 요청자의 취소 | `test_a_confirmed_ax_assignment_offers_no_withdrawal_because_it_already_stands` — 봉투가 `cancel_assignment` 를 **광고하지 않고**, id 를 알고 직접 불러도 4xx, 업무·담당 그대로 |

**삭제(대체 없이 사라진) 테스트: 0건.** 위 12건은 전부 같은 파일에서 새 계약 단언으로 다시 섰다.

### 그 밖 — 호출 계약만 업데이트한 것

- `backend/tests/conftest.py` autouse fixture: POST 에 `Idempotency-Key` 가 **없을 때만** 호출마다 **새 키**를 채운다.
  키는 인증 헤더와 같은 전송 계약이라 그것을 시험 대상으로 삼지 않는 테스트까지 줄마다 적게 하지 않는다.
  **새 키이므로 이 채움이 중복을 감춰 주지 않는다.** 키 자체를 시험하는 테스트는 `@pytest.mark.no_auto_idempotency_key`
  또는 헤더 직접 지정으로 이 채움을 밀어낸다(`test_task_creation_contract.py`, `test_meeting_rooms.py`).
- 과거 모양 fixture 로 바꾼 파일(주제 그대로, 상태만 과거로): `test_request_amendment` · `test_request_revision_input` ·
  `test_request_evidence_and_cc`(근거 부분만) · `test_decision_continuity` · `test_evidence_continuity` ·
  `test_action_center` · `test_mcp_action_items` · `test_mcp_request_query_results` · `test_mcp_confirmation_materials` ·
  `test_material_search_owners` · `test_material_search_public` · `test_unified_queries` · `test_browser_interactions` ·
  `test_notifications`(수락 알림 부분만) · `test_turn_proposal_slot` · `test_product_operations`(거절·조정) ·
  `test_meeting_finalize`(수정·거두기) · PG `test_material_owners`·`test_material_upgrade`·`test_postgres_integration`·
  `test_postgres_assignment_decision_replay`.
- 후보 목록 단언(`test_mcp.py`·`test_product_operations.py`): 판단 역량 필터를 걷은 결과로 갱신 — § 5 ②.

---

## 4. 코디 처리 필요 — allowed_paths 밖

### ① `docs/unified-operations-inventory.json` (operation inventory drift)

**갱신본을 만들어 세 테스트로 검증까지 마쳤다.** 그대로 복사하면 `make test-unit` 이 green 이 된다.

- 갱신본: `…/scratchpad/inventory/unified-operations-inventory.json`
- diff: `…/scratchpad/inventory/inventory.diff` (실질 변경 73줄)
- 검증: `…/scratchpad/inventory/fakeroot` 에 docs 만 갈아끼워 `test_inventory_schemas_match_the_actual_registered_tools`,
  `test_inventory_includes_each_declared_http_operation`, `test_final_inventory_has_no_implicit_or_unverified_product_surface` 3개 전부 PASS

diff 내용은 넷뿐이다.

1. `POST /api/tasks` — `http_handler` `create_self_task`→`create_task`, `http_application_calls` 동일 변경,
   `owning_calls` → `self._task_creation(session).create_or_receipt`, 시그니처에 `idempotency_key: str | None` 추가.
2. `POST /api/tasks/assign` · `POST /api/work-requests` · `POST /api/meetings/{id}/todos/{id}/promote` —
   시그니처에 `idempotency_key: str | None` 추가, `owning_calls` → `self._task_creation(session).create_or_receipt`.
3. 도구 4종(`task_create_self`·`task_assign`·`work_request_create`·`meeting_todo_promote`) —
   `input_schema` 에 필수 `idempotency_key`, `task_create_self` 에 `assignee_id`, description 갱신.
4. 코드 쪽 짝(이미 반영, backend 안): `bootstrap/operation_inventory.py` 에
   `'POST /api/tasks': ('task_create_self',)` override 추가. 라우트는 `create_task`, 도구 adapter_operation 은
   `create_self_task` 라 자동 매핑이 안 된다 — **MCP 도구 이름은 외부 계약이라 W1 이 바꾸지 않았다.**

### ② 제품 문서 (수락 전제 서술) — 수정 필요 목록

| 파일 · 자리 | 지금 문장 | 대체 문장(제안) |
|---|---|---|
| `README.md` 「업무」절 | 배정/요청이 수락을 기다린다는 서술 | "생성 명령이 성공하면 담당자가 정해진 업무가 **수락 없이** 그 사람의 목록에 즉시 선다. 생성 명령은 `Idempotency-Key` 를 필수로 받는다." |
| `docs/domain-model.md` — `TASK_ASSIGNMENT` 행 | `direct` 는 수락 전까지 `pending` | "`direct` 도 생성 시점에 `active` 다. `pending` 은 **담당자 변경**과 과거 행에만 남는다. 한 업무의 활성 담당은 DB 부분 unique(`uq_task_assignments_active`)로 0 또는 1." |
| `docs/domain-model.md` — `WORK_REQUEST` 행 | 상태 다섯 | "`assigned` 추가 — 신규 경로가 내는 값이고 판단 없이 업무와 활성 담당이 섰다는 사실만 말한다. 기존 다섯의 뜻은 그대로." |
| `docs/domain-model.md` — 새 표 한 줄 | — | "`task_creation_attempts` — (행위자·명령 종류·키) 하나에 생성 결과 하나. payload 지문으로 같은 키의 다른 내용을 충돌로 가른다." |
| `docs/domain-model.md` — `TASK` 행 | — | "`approver_id` (nullable) — W1 은 열만 만든다. 입력·화면은 W2." |
| `docs/unified-operations.md` (생성 절이 있다면) | 수락 단계 서술 | 위와 같은 취지 |

> 실제 문구는 해당 파일을 열어 확인한 것이 아니라 **바뀐 동작에서 역산한 것**이다 — allowed_paths 밖이라 읽고 고치지 않았다.
> 코디가 문장 위치를 확정해 주기 바란다.

---

## 5. 발견 / 주의점

**① `modules/meetings/followups.py` 는 현재 도달 불가능한 死코드다.**
`platform/actions.py:750` 이 `self._services.meeting_followups().promote(...)` 를 부르지만
`WorkflowApplication._meeting_followups` 가 **존재하지 않고**, `MeetingApplication.followup_candidate` /
`record_followup_promotion` 도 **존재하지 않는다**(W1 이전부터). 즉 `meeting.followup.task`·`meeting.followup.request`
두 AX action type 은 실행하면 AttributeError 다. WORK-001 Phase 5 가 이 모듈을 승격 경로로 지목하지만,
**실제 live 승격 경로는 `promote_meeting_todo` 하나**이고 그쪽을 정렬했다.
`followups.py` 도 우회 생성을 걷고 `TaskCreationApplication` + 후보 identity 안정 키로 고쳐 두었으나
(되살아날 때 계약 위에 서게), **조립을 새로 붙이지는 않았다** — 죽은 하위 시스템을 되살리는 것은 W1 범위 밖이다.

**② 데모 조직에서는 「권한 밖 수신자」가 사실상 없다.**
`work_request.decide` 필터를 걷은 뒤 남는 조직 범위 교집합은, 데모 조직이 회사 하나(`scax`)뿐이라
**모든 구성원 사이에서 항상 겹친다**. 그래서 민아의 후보가 `{hyeon, jiho, minseok, sora, yuna}` 로 늘었다
(소라는 「외부 법무 자문」인데도 후보에 든다). WORK-001 Phase 3 이 "새 검사를 더하지 않는다"고 못 박아
그대로 두었고, SPEC 의 `WORK_RECIPIENT_NOT_ALLOWED` 는 이제 **원장에 없는 식별자·재직하지 않는 구성원**에만 걸린다.
`test_product_operations.py` 의 「권한 밖 배정 시도(mina→sora)」 단언을 그 사실대로 고쳤다.
**제품 판단이 필요하면 planner/코디가 SPEC 으로 닫아야 한다** — 코드로 발명하지 않았다.

**③ `created_by_actor_id` 는 요청 출신 업무에서 여전히 담당자다.**
수락이 업무를 세우던 시절의 의미가 남아 있다. 요청자는 `origin`(요청자) 과 `source_work_request_id` 로 정확히 읽히고
완료 승인 확인자도 거기서 나오므로 기능에 문제는 없으나, 뜻이 낡았다. 열람 판정에 닿아 있어 **W1 에서 바꾸지 않았다.**

**④ FE 표면 감사 (코디 요청 항목).** 신규 `assigned`/`active` 에 수락 회차 전용 명령을 **광고하지 않는다.**
- BE: 신규 경로는 `DecisionItem` 을 만들지 않아 `/api/action-items` 에 수락 종류가 서지 않고,
  확인된 AX 배정의 `allowed_commands` 가 빈 배열이다(테스트로 고정).
- FE(읽기만 함): `WorkModals.tsx:1724-1730` 이 `canAdoptEvidence`·`isOpen`·`canAmend`·`canResubmit` 를
  `pending`/`negotiating` 으로 막고 있어 `assigned` 에는 근거·조정·재상신이 뜨지 않는다. **문제 없음.**
- 다만 `frontend/src/features/work/MyWorkPage.tsx:10-11` 이 `acceptTaskAssignment`·`declineTaskAssignment` 를
  **import 만 하고 호출하지 않는다**(죽은 import). FE 워커가 정리하면 좋겠다 — 내 allowed_paths 밖이라 손대지 않았다.

**⑤ 공유 워크트리에서 `git stash push -u` / `apply` 를 2회 썼다.**
inventory·자료 worker 실패가 내 변경 탓인지 가르려고 baseline(`make test`)을 돌리기 위해서였다.
두 번 다 unique 태그 + SHA 로 `apply` 후 `drop` 했고 conflict·유실은 없다(`git status` 확인 완료, FE 워커 파일 13개 그대로).
다만 그 3분 동안 워크트리가 HEAD 상태로 보였을 수 있어 **FE 워커에게 알릴 가치가 있다.**

---

## 6. 남은 실패 — 내 변경과 무관(baseline 재현)

`tests/contract/test_material_worker_recovery.py` 와 `test_material_search.py` 의 타이밍 의존 테스트가
`-n auto` 전체 run 에서 회차마다 다르게 1~2건 흔들린다.

- **직렬 실행은 항상 green** (`uv run pytest tests/contract/test_material_worker_recovery.py tests/contract/test_material_search.py` → 20 passed).
- **변경 없는 baseline 에서도 재현했다**: stash 로 내 변경을 전부 걷고 `make test` 를 두 번 돌렸더니
  1회차 green(`baseline.txt`), **2회차에서 `test_long_parse_heartbeats_its_lease_so_a_second_worker_cannot_reclaim_it` 실패**(`baseline2.txt`).
- 원인: `material_queue_visibility_timeout=3` 대 `SlowExtractor` 의 `time.sleep(3.6)`, 그리고 자식 프로세스를
  spawn 하는 worker 가 xdist 병렬 부하에서 lease heartbeat 마감을 놓친다. **기존 flake 다.**

`test-scale` 에서 하나 고친 것은 real fix 다 — `test_relation_graph_scale.py` 의 **module-scoped fixture** 는
function-scoped autouse fixture 밖이라 키가 채워지지 않아, 그 fixture 의 헤더에 키를 직접 실었다.

---

## 7. 다른 팀 영향 (FE)

| 표면 | 변경 |
|---|---|
| `POST /api/tasks` | `Idempotency-Key` **헤더 필수**(누락·공백 → 422). 본문에 `assignee_id` 추가(없거나 본인 → 내 업무). 본문 `idempotency_key`·`approver_id` 는 계속 422. 담당 지정 시 `start_date`·`parent_task_id`·`project_id` 는 422. 응답은 **언제나 업무 투영** |
| `POST /api/tasks/assign` · `POST /api/work-requests` · `POST /api/meetings/{id}/todos/{id}/promote` | `Idempotency-Key` 헤더 필수 |
| 새 오류 | `403` 보낼 수 없는 사람 · `409` 같은 키 다른 내용 · `422` 키 누락 |
| `WorkRequest` 응답 | 신규는 `state: "assigned"`, `task_id` 가 **생성 즉시** 채워지고 `assignment_state: "active"`. `submission_version` 은 `null`(회차가 없다) |
| `TaskAssignment` 응답 | 신규 배정은 `status: "active"` + `accepted_at` |
| 판단함 | 신규 생성은 `work_request.acceptance`·`task.assignment.acceptance` 를 **만들지 않는다**. 완료 승인(`task.delivery`)·AX 확인은 그대로 |
| 후보 목록 | `GET /api/work-request-assignee-candidates` 유지(이름 전환 없음). 판단 역량 필터가 빠져 후보가 늘어난다 |
| MCP | 네 도구에 `idempotency_key` 필수 인자, `task_create_self` 에 `assignee_id` |

## 8. 하지 않은 것

- 커밋·push·PR·배포 없음. `frontend/`·`docs/` 무수정. `ax_demo` 무접촉.
- migration 도입 없음 · 일반 startup DDL 없음 · 문서 Phase Status 무수정.
- `make verify` 전량·`make acceptance-e2e`·브라우저 E2E 미실행(E2E 는 사용자 담당).
- W2/OQ-A/D2 정책 결정 없음. 승인자는 열만, 입력·응답 없음.
