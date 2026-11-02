# WORK-002 v2 신규 계약·종단 회귀 — 테스트 리포트

- **작성**: 2026-09-17 · contract-tests 워커 (term_84ab1149)
- **대상**: `backend/tests/contract/test_task_lifecycle_v2.py` (33건) · `backend/tests/contract/test_task_lifecycle_v2_support.py` (도우미)
- **근거 계약**: SPEC-003 §4~6 · WORK-002 Phase 8 · Case Matrix · `example.md` §10
- **실행**: `PYTEST_XDIST_AUTO_NUM_WORKERS=4 PYTEST_ADDOPTS="-k lifecycle_v2 -p no:cacheprovider" make test-contract`
- **실행 결과 — 두 수치를 섞지 않는다** (자세히는 §8 부록 3):
  - **정정 전 전량**: 31 passed / 0 failed, `make` rc **0** (`/tmp/run22.out` · `/tmp/run22.exit`).
    그 전 실행의 30 passed / 1 failed 는 결함 H 잔여분이었고 원BE 수정 뒤 같은 명령으로 닫혔다.
  - **정정분(2026-09-17 재발주)**: 변경 테스트만 — 5 passed / 0 failed, `make` rc **0**
    (`/tmp/changed2.out` · `/tmp/changed2.exit`). **정정 후 33건 전량은 재실행하지 않았다.**

> **이 파일이 말하지 않는 것.** SQLite 계약 테스트다. PostgreSQL 의 FK · 유일성 · 잠금 · **진짜 경합**은
> `make test-postgres` 의 몫이고 여기서 통과했다고 주장하지 않는다 (P-7). **브라우저 E2E 는 실행하지
> 않았다** — 화면에서 눈으로 볼 것(UX-U1~U15 의 「표시」 칸)은 사용자 몫으로 남아 있다.

---

## 1. A1~C2 21건 전수 추적

| ID | 시나리오 | 테스트 | 결과 |
|---|---|---|---|
| A1 | 보고서와 내용 작성 하위 생성 | `test_lifecycle_v2_a1_own_work_stands_open_and_starting_is_a_separate_fact` | 통과 |
| A2 | 보고서에서 디자인 요청 발송 | `test_lifecycle_v2_a2_sending_stands_the_task_and_the_wait_not_the_holder` · `test_lifecycle_v2_a2_both_entrances_give_the_same_result_and_keep_their_own_input` | 통과 |
| A3 | 수락 후 시작 | `test_lifecycle_v2_a3_acceptance_confirms_the_same_task` | 통과 |
| A4 | 디자이너의 재분해 + 타인 요청 | `test_lifecycle_v2_a4_a_held_request_is_its_own_centre_of_work` · `test_lifecycle_v2_no_child_stands_under_a_request_nobody_has_taken` | 통과 |
| A5 | 요청자의 상세·연결 자료 조회 | `test_lifecycle_v2_a5_the_requester_reads_the_subtree_and_its_materials_only` · `test_lifecycle_v2_the_requesters_reading_closes_everywhere_at_once_when_it_is_revoked` | 통과 |
| A6 | 완료 보고 후 보완·재보고 | `test_lifecycle_v2_a6_report_revision_and_approval_stay_in_one_task` | 통과 |
| A7 | 미완료 하위가 있는데 최종 완료 시도 | `test_lifecycle_v2_a7_a8_a9_the_final_completion_is_what_the_children_block` · `test_lifecycle_v2_a7_the_blocking_error_names_only_what_the_caller_may_read` · `test_lifecycle_v2_a7_the_completion_gate_sees_every_direct_child_even_one_a_third_party_created`(정정분) · `test_lifecycle_v2_a7_a_new_holder_reads_the_children_they_inherit_the_gate_for`(정정분) | 통과 |
| A8 | 디자인 승인 전 보고서 완료 시도 | `test_lifecycle_v2_a7_a8_a9_the_final_completion_is_what_the_children_block` | 통과 |
| A9 | 하위 완결 후 보고서 완료 | 〃 | 통과 |
| B1 | 거절 후 재요청 | `test_lifecycle_v2_b1_rejection_cancels_and_a_re_request_is_new` | 통과 |
| B2 | 취소된 A 와 완료된 B 공존 | 〃 + `..._a7_a8_a9_...`(취소 하위 제외) | 통과 |
| B3 | 담당 변경 제안 후 거절 | `test_lifecycle_v2_b3_b4_a_handover_proposal_leaves_the_holder_in_place` | 통과 |
| B4 | 담당 변경 제안 후 수락 | 〃 | 통과 |
| B5 | 수락 전 철회 | `test_lifecycle_v2_b5_withdrawal_before_acceptance_cancels_and_keeps_the_log` | 통과 |
| B6 | 수락 후 취소 제안·동의 | `test_lifecycle_v2_b6_an_accepted_request_is_only_cancelled_by_agreement` | 통과 |
| B7 | 무응답·기한 초과 | `test_lifecycle_v2_b7_no_answer_and_an_overdue_date_change_nothing_but_the_marker` | 통과 |
| B8 | 완료된 상위 아래 하위 재개 | `test_lifecycle_v2_b8_reopening_and_the_finished_parent_that_blocks_it` · `test_lifecycle_v2_b8_reopening_does_not_reuse_the_approval_that_closed_it` | 통과 |
| B9 | 수락 후 조건 변경 | `test_lifecycle_v2_b9_terms_change_needs_agreement_before_it_applies` | 통과 |
| B10 | 취소 항목 목록 정리 | `test_lifecycle_v2_b10_tidying_the_list_is_the_requesters_own_and_only_when_it_is_over` | 통과 |
| C1 | 발송·수락·승인 재시도 | `test_lifecycle_v2_c1_the_key_is_required_where_something_is_created` · `test_lifecycle_v2_c1_answering_twice_is_one_answer` | 통과 |
| C2 | 수락↔철회 / 교체↔거절 / 상위완료↔하위재개 | `test_lifecycle_v2_c2_every_new_command_answers_a_version` · `test_lifecycle_v2_c2_two_commands_that_race_resolve_without_a_contradiction` | 통과(**순차 해소만** — 진짜 경합은 §4) |

## 2. `example.md` §10 — 10단계 연속 흐름

한 테스트가 1→10 을 끊지 않고 밟는다: `test_lifecycle_v2_example_ten_steps_from_the_report_to_its_completion` — **통과**.

| 단계 | 무엇을 단언했나 |
|---|---|
| 1 보고서 등록 | 담당=본인 · `open` · `started_at` 없음 |
| 2 디자인 발송 | Task 즉시 존재 · `parent`=R · 활성 담당 없음 · `derived.assignment=awaiting_acceptance` |
| 3-B 거절 | 요청 `rejected` · Task `cancelled` · `cancel_reason=request_rejected` · `parent` 유지 |
| 3-C 재요청 | 새 요청 Q2 + 새 Task D2 · 같은 `parent` · 거절된 D 재사용 없음 |
| 3-A 수락 | 같은 `task_id` · `open` 유지 · `parent` 유지 · `started_at` 빔 · `accepted_at` 채워짐 |
| 4 시작 | `open → in_progress` · `started_at` 이 그 시각 |
| 5 직접 작업 | L·S 가 D2 직속 · 그 아래 직접 작업 중첩 409 |
| 6 1차 보고 | `state=done` + `approval=awaiting_review` · **Task 표에 검토용 행 0건** |
| 7 보완 | `in_progress` + `awaiting_revision` · 사유 필수 · 자동 하위 없음 |
| 8 2차 보고 | 같은 판단 항목의 `submission_version=2` · 요청 행은 여전히 2건(Q·Q2) |
| 9 승인 | `approval=approved` · 담당자 쪽 판단 항목 없음(역승인 경로 없음) |
| 10 보고서 완료 | `child_progress={done:1, blocking:0, cancelled:1, total:2}` · 취소된 D 제외 · 사람이 부른 뒤에만 `done` |

## 3. 발견한 제품 결함 — 14건 · **전부 원BE 수정 후 해소 확인**

전부 실제 REST 응답으로 재현했고 원BE(term_c2b0c98)와 코디에 즉시 전달했다.

| # | 자리 | 기대 (계약) | 실제 (발견 시점) | 지금 |
|---|---|---|---|---|
| 1 | `modules/work/task_results.py` `TaskMutationResult` | `derived` 7키 · `started_at` · `completed_at` · `reopened_at` · `cancel_reason` (SPEC-003 §4 상세) | 키 자체가 응답에 없음 (`_view()` 가 만든 값이 response_model 에서 잘림) | **해소 확인** |
| 2 | 같은 파일 `TaskProgressView` | `{done, blocking, cancelled, total}` (§4) | `{done, total}` | **해소 확인** |
| 3 | 같은 파일 `TaskSummaryView` | `children[]` 각 줄에 `derived` (UX-U5) | 없음 | **해소 확인** |
| 4 | `entrypoints/http.py` | `GET /api/tasks/{id}/children` 200 (§4 API 표) | 404 (라우트 없음) | **해소 확인** |
| 5 | `modules/work/lifecycle.py` | `complete` 의 미완결 하위 거부 = **409** `WORK_CHILDREN_UNFINISHED` (§4 Case Matrix) | 422 (평범한 `InvalidTaskTransition`) | **해소 확인** |
| 6 | `modules/work/application.py` `_assignment_view` | 담당 변경 대기 중 **활성 담당**을 낸다 (V-18 · K-3) | `assignments[-1]` 즉 `pending` 행을 냈다 | **해소 확인** |
| A | `modules/organization_access/catalog.py` `_MEMBER_CAPABILITIES` | 수신자면 누구나 자기 요청에 답한다 (§5 권한표) | 일반 구성원에게 `work_request.decide` 가 없어 `accept` 403 · 판단함에 항목 0건 → **구성원에게 보낸 요청은 수락할 사람이 0명** | **해소 확인** |
| B | `modules/work/application.py` `_related_view` | 요청자는 요청 Task 와 **그 하위 트리 전체**와 자료를 읽는다 (정책 V-21) | 요청 Task 한 겹만. 손자 GET 404 · `/children` 빈 목록 · 자료 404 | **해소 확인** |
| C | 같은 파일 `_settlement_gap_with` | 승인 전 요청 하위의 `why = awaiting_approval` (§4 · O-20) | 내부 enum(`COMPLETION_SUBMITTED`)을 읽어 `unfinished` | **해소 확인** |
| D | `platform/work_tasks.py` `decide()` | 담당 교체 수락은 **원자적** (V-18 · 인수조건 B4) | `superseded` 와 `active` 사이에 flush 가 없어 `UNIQUE uq_task_assignments_active` 위반 → 500 (행 UUID 순서에 따라 간헐) | **해소 확인** |
| E | `POST /api/tasks/{id}/cancel` | 수락된 요청 Task 직접 취소는 요청자·담당자·관리자 **모두** 409 `WORK_CANCEL_REQUIRES_AGREEMENT` | 요청자에게만 404 | **해소 확인** |
| F | `application.py` `_approval_from_rounds`·`_approval_state` | 승인받은 업무 재개 200 · 지난 승인은 무효 (V-19 · E-5) | `TypeError: can't compare offset-naive and offset-aware datetimes` → 500 | **해소 확인** |
| G | `application.py` `respond_to_proposal` | 같은 답의 재전송만 영수증 | 이미 처리된 제안에 **다른 답**을 보내도 200 영수증(본문은 `agreed`) | **해소 확인** |
| H | `respond_to_proposal` 회차 가드 | 원회차·같은 답 재전송 = 200 영수증 / **다른 답 = 409 `WORK_PROPOSAL_NOT_PENDING`** (§3 S-16 · §4 Case Matrix 비고) | 원회차·같은 답이 422 `version is stale` (수락·제안 응답 모두) · 고친 뒤에도 **다른 답이 409 가 아니라 422** 로 나갔다 — 회차 가드가 「이미 답했다」를 덮었다 | **해소 확인** |

> 부수 기록 — `accepted_at` 은 최상위가 아니라 `assignment.accepted_at` 에 있다. 「수락 시각과 시작
> 시각이 각각 읽힌다」(V-13 · UX-U3)는 만족하므로 결함으로 세지 않았고, 자리만 여기 적는다.

## 4. 검증하지 않은 것 — 통과로 읽지 말 것

| 항목 | 이유 |
|---|---|
| **PostgreSQL 경합·FK·유일성·잠금** | 이 파일은 SQLite 다. C2 의 「동시 실행」은 `test_lifecycle_v2_c2_two_commands_that_race_resolve_without_a_contradiction` 이 **순차 해소**만 본다. 진짜 경합은 **term_2e64fd06 소유**이고 `make test-postgres` 에서 판정된다 (P-7) |
| **브라우저 E2E** | 실행하지 않았다. UX-U1~U15 의 「표시」 칸(배치·문구·읽히는가)은 사용자 확인 전이다 |
| `WORK_PARENT_CYCLE` (422) | **제품 경로로 도달할 수 없다.** 부모는 생성 시점에 정해지고 이동 명령이 없다(EU-15). `test_lifecycle_v2_the_parent_link_is_fixed_at_creation_so_no_cycle_can_be_made` 가 「고리를 만들 입구가 없다」(PATCH 가 `parent_task_id` 를 입력으로 받지 않는다)까지만 못 박는다 |
| 읽을 수 없는 하위가 **이름 없이** 막는 갈래 | **좁은 전제 위에서** 도달 불가다 — 근거는 §8 부록 2. 「상위를 읽으면 하위도 읽는다」가 아니라 **완료 게이트를 부를 수 있는 사람이 둘뿐이고 그 둘이 각자 직속 하위를 읽는다**는 것이다. `test_lifecycle_v2_a7_the_completion_gate_sees_every_direct_child_even_one_a_third_party_created` 가 그 전제를 실제로 확인하고, `..._the_blocking_error_names_only_what_the_caller_may_read` 가 목록·건수·오류 본문의 일치를 본다 |
| **OQ-203** (제출 단계 하위 검사) | 미답. 현행대로 **제출은 통과**하고 최종 완료·승인이 막힌다는 것만 확인했다. 새 정책 확정으로 적지 않는다 |
| **OQ-206** (`system:meeting` 요청의 완료 확인자) | 미답. 확인자를 임의 지정하거나 자동 승인하는 경로를 만들지 않았고 그 좁은 경로는 **미결**로 둔다. 일반 요청자 축만 검증했다 |
| `derived.reply` · `derived.status_note` | 그 원장이 코드에 없다. `null` 이 정상이고 그렇게 단언했다 |
| `child_progress.blocking` = 0 의 뜻 | **보이는 하위만** 센다. 0 이 완료 허용을 보장하지 않는다 |
| 직접 취소의 `reason` 필수 (§4 Validation) | `POST /api/tasks/{id}/cancel` 은 `expected_version` 만 받는다(기존 동작 보존). 계약과 어긋나는 자리로 **기록만** 하고 단언하지 않았다 |
| 두 생성 입구의 **거절 봉투** | 허용 후보 밖 지정을 `POST /api/tasks` 는 403, `POST /api/work-requests` 는 422 로 낸다. §4 가 「응답 봉투는 입구마다 그대로」라 결과·권한 판정만 같음을 단언했다 |
| 선행·후행 강제, 상위 관계 이동 | 후속 범위 — 추가하지 않았다 (EU-2 · EU-15) |

## 5. W1 유지 회귀 (K-1~K-6 · K-11) — 신규 코드가 바꾸는 자리만 새로 덮었다

| # | 보장 | 어디서 |
|---|---|---|
| K-1 | 멱등 원장 — 키 필수 범위, 같은 키 충돌, 다른 키 둘 다 생성, 재전송 1건 | **신규** `test_lifecycle_v2_c1_the_key_is_required_where_something_is_created` (발송 축) · 기존 `test_task_creation_contract.py` (본인 업무 생성 축) |
| K-2 | 영수증 전 권한 재검사 | 기존 `test_task_creation_contract.py::test_a_receipt_is_withheld_from_a_caller_who_may_no_longer_read_it` — 중복하지 않음. 권한 회수의 v2 면(요청 관계 읽기)은 **신규** `test_lifecycle_v2_the_requesters_reading_closes_everywhere_at_once_when_it_is_revoked` |
| K-3 | 활성 담당 최대 1 · `pending` 은 세지 않는다 | **신규** `test_lifecycle_v2_b3_b4_...` (원장 행까지 확인) · `test_lifecycle_v2_a2_sending_...` |
| K-4 | 회차 필수 — 새 명령 전부 | **신규** `test_lifecycle_v2_c2_every_new_command_answers_a_version` (수락·거절·협의·철회·재개·제안·응답·제안철회·담당변경·완료보고 10입구) |
| K-5 | AX 사람 확인 — 확인 전 effect 없음 | **신규** `test_lifecycle_v2_the_same_contract_answers_on_rest_and_mcp_and_ax_waits_for_a_person` (`requires_confirmation` + 위임 호출이 action 으로만 서고 요청·업무가 그대로임) |
| K-6 | 출처와 actor | 기존 `test_meeting_finalize.py::test_the_promoted_request_carries_the_source_columns_onto_the_task` 가 정확히 덮는다(요청자=`system:meeting`, `promoted_by`·`created_by_actor_id`=누른 사람, 승격도 **수락 대기**로 섬 — L-15·L-16). **중복하지 않음** |
| K-10 | REST·MCP·AX 같은 계약·오류·권한 | **신규** `test_lifecycle_v2_the_same_contract_answers_on_rest_and_mcp_and_ax_waits_for_a_person` |
| K-11 | 관리자 직접 배정의 조직 범위 | **신규** `test_lifecycle_v2_k11_a_manager_assignment_still_stands_at_once` (즉시 `active`·수락 대기 아님·범위 밖 422·권한 없음 403) |

## 6. 추가로 못 박은 경계 (코디 요청분)

- **CC 는 요청자가 아니다** — 참조로 받은 사람은 요청 상세를 계속 읽되 하위·자료·검색으로 **자동 확장되지 않는다**. `test_lifecycle_v2_a5_...` 안의 양성/음성 단언.
- **요청 관계 읽기는 한 권한 위에 선다** — `work_request.read` 회수 시 목록(`GET /api/tasks`)·상세·자료·검색이 **함께** 닫히고, 자기가 든 업무 같은 독립 읽기는 보존된다. `test_lifecycle_v2_the_requesters_reading_closes_everywhere_at_once_when_it_is_revoked`.
- **제3자 거부 유지** — 구성원에게 판단 권한이 열린 뒤에도 그 요청의 수신자가 아니면 답하지 못한다(대표·요청자 모두 403). `test_lifecycle_v2_only_the_recipient_answers_and_a_second_answer_is_refused`.
- **재전송과 새 명령을 가른다** — 같은 사람·같은 답·**원회차** = 200 영수증 + effect 0 / 지금 회차로 다시 답하거나 다른 답 = 명시적 충돌. `test_lifecycle_v2_c1_answering_twice_is_one_answer` 와 `..._only_the_recipient_answers_...` 가 각각 맡는다.

## 7. 남은 일

1. 코디네이터의 통합 검증에서 **전체 스위트**(`make verify`)와 `make test-postgres` 를 별도로 확인해야 한다 — 이 워커는 신규 파일 범위만 돌렸다.
2. 사용자 브라우저 E2E 는 여전히 미실행이다.
3. §4 의 「검증하지 않은 것」은 그대로 남는다 — 특히 PostgreSQL 경합과 OQ-203 · OQ-206 은 이 파일이 답하지 않는다.

---

## 8. 부록 — 최종 증거 정정 (2026-09-17, 재발주 `task_58627c5f0d8b`)

두 자리를 고쳤다. **새 범위를 만들지 않았고** 본인 소유 두 테스트 파일과 이 리포트만 손댔다.

### 부록 1. A5 의 「조회가 명령을 넓히지 않는다」 — 넓은 단언을 정확한 거부 코드로

**무엇이 틀렸나.** `test_lifecycle_v2_a5_...` 의 두 자리가 `status_code != 200` 이었다. 그 단언은
**권한 거부를 증명하지 않는다** — 500 도, 다른 어떤 실패도 통과한다.

**고치고 나서 드러난 것.** 정확한 코드로 바꾸자 그 자리가 바로 깨졌다:

```
AssertionError: ('start', '{"detail":[{"type":"extra_forbidden","loc":["body","summary"], ...}]}')
assert 422 == 404
```

`start` · `complete` 에 `summary` 를 함께 실어 보내고 있었고, 그 두 명령은 여분 필드를 거절한다.
**즉 옛 단언은 권한이 아니라 본문 스키마 때문에 통과하고 있었다.** 넓은 단언이 무엇을 가리고
있었는지가 그대로 나온 자리다.

**지금 단언하는 것.**

| 명령 | 본문 | 코드 | 계약 근거 |
|---|---|---|---|
| `start` · `complete` · `completion-report` | 각 명령이 실제로 받는 본문 | **404** | 수행 명령은 **활성 담당자**만 부른다 (§5 권한표 「시작 · 수행 기록 · 완료 보고 — 활성 담당자만」). 들고 있지 않으면 **없는 것과 못 읽는 것을 같은 말로** 답한다 (§4 Case Matrix `WORK_NOT_FOUND`) — 읽을 수 있다는 사실이 거절에서 새 나가지 않는다 |
| `reassign` | `assignee_id` · `reason` | **403** | 그 앞에 역량이 선다 — 민아에게 `task.assign` 이 없다 (§5 권한표 「담당 변경 제안 — 담당자 또는 배정 권한」). 본문에 `task.assign` 이 들어 있는 것까지 확인한다 |

거절 본문이 그 업무의 내용(`시안`)을 흘리지 않는 것과, **상태·회차·담당이 그대로**인 것을 함께
단언한다. 검증: `-k lifecycle_v2_a5` → **1 passed**, `make` 종료코드 **0** (`/tmp/fix2.out` · `/tmp/fix2.exit`).

### 부록 2. 「숨은 하위」 판독 정정 — 일반화를 걷고 좁은 전제로 바꾼다

**무엇이 틀렸나.** 이전 리포트와 테스트 docstring 이 「V-21 이 열린 뒤로는 **상위를 읽는 사람이 그
하위도 읽는다**」로 적었다. **그 문장은 거짓이다.** V-21 은 **요청자·승격자만** 넓히고, 참조(CC)와
조직·프로젝트 범위 독자는 상위를 읽어도 하위가 자동으로 열리지 않는다. 그 문장을 테스트와
리포트 양쪽에서 **제거했다.**

**실제로 확인한 것.** 「완료 가능한 상위 담당/승인 주체에게 숨은 직속 하위가 생길 수 있는가」를
API 로 재현해 보았다. 상위를 읽을 뿐인 **제3자(대표 · `work.read.all`)** 가 하위 요청을 걸어
게이트 호출자가 만들지 않은 직속 하위를 만드는 경로다.

| 만든 모양 | 게이트 호출자 | 그 하위를 읽나 | 완료 게이트 |
|---|---|---|---|
| 민아가 든 업무 아래 ← 대표가 건 하위(담당 민석) | 민아 (`complete`) | **읽는다** (200) | 409 이고 **이름이 나온다** |
| 민아→지호 요청 업무 아래 ← 대표가 건 하위(담당 민석) | 지호 (담당) · 민아 (승인) | **둘 다 읽는다** (200·200) | 승인 409 이고 **이름이 나온다** |

**왜 닫히나 — 좁은 전제.** 완료 게이트를 부를 수 있는 사람은 **둘뿐**이다: 그 업무의 **활성
담당자**(`complete`)와 **요청자**(요청 Task 의 최종 완료 = 요청자 승인). 그 둘은 **각자 다른 길로**
직속 하위를 읽는다 — 담당자는 「상위를 든 사람은 그 부분을 읽는다」(`_related_view` 의 부모 경로)로,
요청자는 V-21 의 **요청 조상 탐색**으로. 상위를 읽을 수 있다는 것만으로는 아니다.

따라서 「읽을 수 없는 하위가 이름 없이 막는다」는 갈래는 코드에 남아 있어도 **API 로는 그 상태를
만들 수 없고**, 그 결과 **혼합 경우(보이는 것 + 안 보이는 것)도 만들 수 없다** — 게이트 호출자에게는
직속 하위가 전부 보인다. 제품 결함이 아니므로 원BE·코디에 올릴 건은 없다.

**코디가 올린 담당 교체 가설 — 실측으로 기각.** 「A 가 상위를 들고 B 에게 하위 요청을 보낸 뒤 상위
담당을 C 로 교체하면, C 는 상위의 활성 담당이지만 그 하위의 requester 가 아니므로 열람이 안 열릴
수 있다」는 후보를 **가장 불리한 조건**으로 재현했다 — A·C 모두 `task.assign` 도 `work.read.all` 도
없는 구성원(민석 · 민아), 교체 제안자만 대표.

| 시점 | C 가 상위를 읽나 | C 가 그 하위를 읽나 | C 의 `complete` |
|---|---|---|---|
| 교체 전 | 404 | **404** (열람 없음 — 여기까지는 가설대로다) | 부를 수 없다 |
| 교체 수락 뒤 | 200 | **200** | **409 + 하위 이름** |

**열람과 게이트가 같은 사건에서 함께 열린다.** 여는 것은 「상위를 읽는다」가 아니라 **「상위를 든다」**
이고(`_related_view` 의 부모 경로가 활성 담당을 묻는다), 그래서 게이트를 새로 얻은 사람에게 그
하위가 숨는 구간이 없다. **가설은 성립하지 않으므로 제품 결함으로 올리지 않는다** — 다만 이 경로가
셋 중 가장 직접적이라 회귀로 남겼다. 넘겨준 A 쪽도 함께 확인했다: 상위는 404(책임이 옮겨 갔다),
자기가 부탁한 하위는 200(V-21) — 책임과 열람이 각자의 근거로 움직인다.

**남긴 회귀 둘.**
- `test_lifecycle_v2_a7_the_completion_gate_sees_every_direct_child_even_one_a_third_party_created`
  — 제3자(대표)가 건 하위를 담당 축·승인 축 양쪽 게이트가 이름으로 막는다. 반대쪽(참조는 요청을
  읽어도 그 하위가 404)도 같은 테스트에 있다.
- `test_lifecycle_v2_a7_a_new_holder_reads_the_children_they_inherit_the_gate_for`
  — 담당 교체 전후를 **한 사람의 404 → 200** 으로 못 박는다. 전제가 바뀌면 이 테스트가 먼저 깨진다.

순환 관계 방어는 억지 API 로 만들지 않았다 (§4 그대로).

검증: `-k lifecycle_v2_a7` → **4 passed**, `make` 종료코드 **0** (`/tmp/fix4.out` · `/tmp/fix4.exit`).

### 부록 3. 이번 검증 수치 — 이전 증거와 구별한다

| 무엇 | 명령 | 결과 | 로그 |
|---|---|---|---|
| **이번 정정분** (변경 테스트만) | `PYTEST_ADDOPTS="-k 'lifecycle_v2_a5 or lifecycle_v2_a7'" make test-contract` | **5 passed / 0 failed**, `make` rc **0** | `/tmp/changed2.out` · `/tmp/changed2.exit` |
| 직전 전량 (이 정정 **이전** 증거) | `PYTEST_ADDOPTS="-k lifecycle_v2" make test-contract` | 31 passed, rc 0 | `/tmp/run22.out` · `/tmp/run22.exit` |

**두 수치를 섞지 않는다.** 위의 31 pass 는 정정 **전** 파일에 대한 것이고, 이번 발주는 지시대로
**변경 테스트만** 돌렸다 — 정정 후 파일의 전량(33건) 재실행은 하지 않았으므로 「33 전부 통과」라고
적지 않는다. 전량 확인은 코디네이터의 통합 검증 몫이다.

### 부록 4. 이 발주에서 정하지 않은 것

- 직접 취소의 `reason` 필수(§4 Validation)와 현재 입구가 `expected_version` 만 받는 것 사이의 모순 —
  **원BE·코디 확인 중**이고 여기서 정하지 않았다. §4 표의 기록을 그대로 둔다.
- OQ-203 · OQ-206 — 현행 그대로. 새 정책으로 올리지 않았다.
- PostgreSQL 경합·FK·잠금 — **term_2e64fd06 소유**. 이 파일이 대신하지 않는다.
