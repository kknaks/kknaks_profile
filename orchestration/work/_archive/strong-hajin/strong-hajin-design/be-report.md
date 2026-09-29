# WORK-007 Phase B-1 · B-2 · B-3 결과 보고

워크트리: `/Users/kknaks/orca/workspaces/Strong_hajin/strong-hajin-design` (브랜치 `kknaksss/strong-hajin-design`, base `origin/main` = `b145745`)
SoT: SPEC-007 v0.2.0 · WORK-007 Phase B-1(`:236`) · B-2(`:273`) · B-3(`:312`)
**커밋·push·PR 하지 않았다.** 워크트리에 변경만 남겼다.

## 0. 한 줄 요약

후행은 **`task_predecessors` 를 반대로 읽는 문 하나 + 인덱스 하나 + 상세 응답 칸 둘**로 열었고(새 표 0·새 컬럼 0·새 쓰기 경로 0), 상위 변경은 `PATCH` 에 칸 둘을 열어 **검증 0~7** 을 걸었으며(1~5 는 기존 `parent_for()` 재사용, 6 은 새 오류 코드 `WORK_CHILDREN_DIRECT_NESTING` 409, 7 은 기존 선행 잠금 재사용), 후행 해제는 전용 라우트 하나로 **A 쪽에도 열었다** — `make test-unit` 381 passed · `make test-contract` 두 패스 green · 격리 PostgreSQL 에서 인덱스 valid 확인, **새로 쓴 테스트 54건 전부 통과**이고 기존 실패는 **1건뿐이며 그것은 SPEC-007 이 대체한 계약의 테스트**라서 함께 고쳤다.

---

## 1. 표면 전수조사 결과 (§4 심볼별 건수와 처분)

`grep -rho <심볼>` 의 **출현 횟수**다(줄 수가 아니다). 「전」은 `origin/main`, 「후」는 이번 판.

| 심볼 | src 전 | src 후 | tests 후 | 처분 |
|---|---|---|---|---|
| `predecessor_task_id` | 17 | **29** | 7 | **역방향 문 신설** — 이 열을 **필터로** 거는 문이 이번 판 전에 0건이었다(`be-survey-report.md` §3.1). `successors_for` · `active_successor_ids` · `predecessor_link` 셋이 그 방향을 쓴다. 인덱스 하나를 더했다 |
| `preceding_task_ids` | 79 | **80** | 95 | **손대지 않았다.** 값·검증 다섯·게이트 두 문 그대로. 늘어난 1건은 후행 문 docstring 의 참조 |
| `successors` | **0** | **10** | 25 | 신규 — `TaskSuccessorView` · `TaskDetailResult.successors` · `successor_views()` · `successors_for()` · 해제 응답 · 라우트 |
| `hidden_successor_count` | **0** | **6** | 9 | 신규 — 상세 두 갈래 + 해제 응답 |
| `parent_task_id` | 115 | **132** | 147 | **편집 칸으로 열었다.** 쓰는 자리는 여전히 둘(생성 · 이 이동)이고 **둘 다 「대상 업무 자신의」 상위**다 — 그 전수를 test 가 AST 로 센다 |
| `clear_parent` | **0** | **12** | 8 | 신규 — `TaskEditFields` · `TaskUpdateInput` 양쪽. **판정(둘 함께 금지)은 `TaskEditFields` 한 곳** |
| `project_id` | 327 | **333** | 622 | **자손 파급에 재사용.** 새 판정을 만들지 않고 `project_for(…, parent)`(생성이 부르는 그 문)과 `_require_project_unlocked()`(기존 잠금)를 그대로 쓴다 |
| `TaskEditFields` | 6 | **8** | 0 | 칸 둘을 더했다. `clear_parent` 를 여기 둔 이유: 확인 카드(AX)·MCP 는 `TaskUpdateCommand` 로 payload 를 **직접** 검증해 `TaskUpdateInput` 을 지나지 않는다 — HTTP 표면에만 두면 그 갈래에서 규칙이 빠진다 |
| `TaskUpdateInput` | 4 | **6** | 0 | 두 칸을 **접지 않고 그대로 넘긴다** — 「둘을 함께 보냈다」 거절이 `TaskEditFields` 의 몫이므로 |
| `TaskUpdateCommand` | 10 | **11** | 0 | **코드를 고치지 않았다.** `TaskEditFields` 상속이라 두 칸이 자동으로 따라오고, `platform/actions.py` 의 확인 카드 필드 빌더가 schema 를 **일반적으로** 읽으므로 그쪽도 자동이다 |
| `parent_for` | 5 | **9** | 1 | **재사용.** 검증 1~5 를 다시 짓지 않았다. `child_task_id` 인자가 순환 검사를 켠다(생성 경로는 업무가 없어 그 인자가 빈다) |
| `_require_may_hold_children` | 2 | **2** | 0 | **손대지 않았다** — 검증 5(`WORK_DIRECT_NESTING`)가 그 안에 그대로 있다 |
| `_is_central_task` | 2 | **2** | 0 | **손대지 않았다.** 게이트 6 은 같은 판정(SPEC-003 §5)을 **이동 후의 값으로** 다시 계산한다 — 그 함수는 현재 부모를 읽으므로 재사용할 수 없다 |
| `_predecessor_gate` | 2 | **2** | 0 | **손대지 않았다** — 시작 게이트는 이 판의 범위 밖이다 |

### 비대칭이 생기기 쉬운 셋 — 브리프 §4 가 지목한 자리

| 자리 | 이번 판 | 근거 |
|---|---|---|
| `entrypoints/http.py` ↔ `entrypoints/mcp.py` | **`mcp.py` 를 한 줄도 고치지 않았다.** 상세 도구(`task_get`)는 `TaskDetailResult` 를 반환하므로 두 칸을 **자동으로** 실어 나른다(test 가 그것을 센다). MCP `task_update` 에 `parent_task_id` 를 **열지 않았다** — 아래 §5 ① | SPEC-007 §4 「MCP 에 새 도구를 내지 않는다」 · §5 표면 일치 ⚠ |
| `TaskVersion` snapshot | **고치지 않았다.** 상위·선행·프로젝트가 여전히 snapshot·diff 에 없다 | WORK-007 Out 「이력·diff 에 관계 변경 싣기 — 기록만」 · SPEC-007 §5 보존 ⚠ |
| **새 오류 «코드» 1건 · 새 예외 «클래스» 2건** | 계약상 새 코드는 `WORK_CHILDREN_DIRECT_NESTING` **하나**다(SPEC-007 § Case Matrix). 파이썬 클래스는 둘이다 — 둘째 `TaskSuccessorVersionConflict` 는 SPEC 이 **기존** 코드로 적은 `WORK_VERSION_STALE` 를 이 표면에서 409 로 내기 위한 것이고 **새 코드가 아니다**. 왜 새 클래스가 필요했는지는 §7 ③ | SPEC-007 § Case Matrix |
| 오류 본문의 기계용 `code` | **더하지 않았다.** 새 거절도 `detail=str(error)` 문장 하나로 나간다. **막는 하위 이름을 문장 안에 담았다** | WORK-007 Out 「오류 응답에 기계용 `code` 더하기」 · SPEC-007 § Case Matrix ⚠ 「문장 안에 담는 것으로 충분하다」 |

---

## 2. Phase 별 구현

경로는 모두 `backend/` 기준. 줄 번호는 이번 판 적용 후.

### Phase B-1 — 후행 역방향 조회와 응답 필드

| 작업 | 어디 | Acceptance 충족 근거 |
|---|---|---|
| 인덱스 설치 방법 답 | §3 | `test_work007_successor_index_postgres.py::test_postgres_w7_a_missing_index_on_this_existing_table_needs_the_manual_sql_not_schema_sync` 이 그 답을 **재현해 닫는다** |
| `predecessor_task_id` 인덱스를 모델 metadata 에 | `src/ax_workspace/platform/persistence.py:1027-1034` | `::test_the_model_declares_the_index_and_adds_no_table`(선언) · `::test_postgres_w7_the_successor_index_stands_and_is_valid`(실 PostgreSQL valid) |
| 역방향 조회 | `src/ax_workspace/platform/work_tasks.py:1155-1185` (`successors_for` · `active_successor_ids`) | 「`predecessor_task_id` 를 필터로 거는 문이 코드 전체에 0건」이었고 이제 하나다 |
| `TaskSuccessorView` — `TaskSummaryView` + `version` | `src/ax_workspace/modules/work/task_results.py:212-228` | `test_task_successors.py::…_a_successor_without_any_write` — 줄의 여섯 칸을 그대로 센다 |
| `TaskDetailResult` 에 칸 둘 | `src/ax_workspace/modules/work/task_results.py:255-264` | `test_task_successors.py::…_a_successor_without_any_write` |
| 후행마다 읽기 판정 · 못 읽으면 **배열에서 빼고 건수** | `src/ax_workspace/modules/work/application.py:1468-1506` (`successor_views`) | `test_task_successors.py::test_a_successor_the_reader_cannot_open_is_only_a_count` — `task_id` 도 제목도 응답 어디에도 없음을 `str(view)` 로 센다 |
| 되돌이 방지 빗장 — 선행과 **같은 모양** | `application.py:250`(빗장) · `:1455-1466`(`_successor_fields`) | 빗장 이름을 `_resolving_predecessor_access` → **`_resolving_relation_access`** 로 바꿔 **선행·후행이 하나를 공유**한다. 따로 두면 선행→후행→선행 사슬이 열린다. `test_task_successors.py::test_a_chain_of_successors_does_not_walk_the_read_probe_round_and_round` |
| `access: "read_only"` 갈래에도 싣는다 | `application.py:1131`(read_only) · `:2650`(owner) — **같은 함수** | `test_task_successors.py::test_the_read_only_branch_carries_the_successor_fields_too` — `access == "read_only"` 에 두 칸이 있고 `references` 는 여전히 없음도 함께 센다 |
| 정렬 = 관계가 선 순서 | `work_tasks.py:1178` (`order_by(created_at, id)`) | `test_task_successors.py::test_successors_are_ordered_by_when_the_relation_was_made` — 두 후행이 각자 `position=0` 이라 `position` 정렬로는 차례가 안 갈린다는 사실을 docstring 에 남겼다 |
| 목록·프로젝트 상세·요청 응답에 **안 싣는다** | 싣는 자리를 상세 두 갈래로 한정 | `test_task_successors.py::test_successors_are_not_in_the_list_or_the_project_detail` — `/api/tasks` · `/api/my-work` · 프로젝트 상세 `tasks[]` 세 곳을 전수로 센다 |
| MCP 상세 도구가 같은 확장 · **새 도구 없음** | `mcp.py` 무변경 | `test_task_successors.py::test_the_mcp_detail_tool_carries_the_same_two_fields` — 도구 이름에 `successor` 가 0건이고 `task_get` 이 두 칸을 낸다 |
| 운영 대장 서명 갱신 — **diff 난 항목만** | `docs/unified-operations-inventory.json` | 실제 drift 는 **정확히 둘**이었다: `task_get.output_schema` 하나와 새 HTTP 행 하나. 스크립트로 계산해 그 둘만 패치했고 `tool_count` 는 129 그대로, `http_count` 159→160 |

**검증 항목 대응**: 「쓰기 명령을 한 번도 안 불렀다」 → `test_task_successors.py::test_choosing_a_predecessor_makes_the_other_task_a_successor_without_any_write`(저장 행이 **하나**임을 DB 로 확인) · 「빠지면 사라진다」 → `::test_dropping_the_predecessor_drops_the_successor_too` · 「취소·완료된 후행도 남는다」 → `::test_a_cancelled_or_finished_successor_stays_in_the_list_with_its_state` · 「새 표가 0건」 → `test_work007_successor_index_postgres.py::test_the_model_declares_the_index_and_adds_no_table`(metadata 에 `successor` 이름 표 0건 + 열 목록 고정).

### Phase B-2 — 상위 변경 칸과 두 게이트

| 작업 | 어디 | Acceptance 충족 근거 |
|---|---|---|
| `TaskEditFields` 에 `parent_task_id` · `clear_parent` · 함께 보내면 거절 | `src/ax_workspace/modules/work/task_commands.py:57-65`(칸) · `:85-101`(`validate_edits`) | `::test_the_patch_now_takes_the_parent_field_and_moves_the_task`(받아진다) · `::test_sending_both_the_parent_and_the_clear_flag_is_refused`(둘 함께 → 422) |
| 검증 0~7 을 **순서대로** | `application.py:622-689` (`_apply_parent_change`) | 0 → `::test_a_cancelled_task_still_cannot_be_moved` · 1 → `::test_an_unreadable_parent_is_a_404` · 2 → `::test_a_finished_parent_is_a_conflict` · 3 → `::test_a_parent_whose_assignment_is_not_settled_is_a_conflict` · 4 → `::test_a_cycle_is_refused_at_any_depth` · 5 → `::test_this_tasks_own_v8_violation_keeps_the_existing_code` |
| 1~5 는 **기존 `parent_for()` 그대로** | `application.py:661-665` | 그 함수를 고치지 않았다. ⚠ 실제 순서는 1→4→2→3→5 — **거절의 집합은 같고** 한 요청에 여럿 걸렸을 때 먼저 말하는 것만 다르다. 포크하면 V-8 판정이 두 벌이 되므로 그대로 썼다(§7 에 남긴다) |
| **6 — 직속 하위의 V-8 파급** | `application.py:691-747` (`_require_children_may_follow`) | `::test_moving_under_the_same_holder_breaks_the_direct_children_and_is_refused`(이름이 본문에) · `::test_a_child_held_by_someone_else_does_not_trip_the_gate` |
| 읽을 수 없는 하위까지 세고 이름은 읽을 수 있는 것만 | 같은 함수 `:734-747` | **HTTP 표면에서 도달 불가**한 갈래다(아래 §7 ②) → `tests/unit/test_task_children_nesting_gate.py::test_a_child_the_caller_cannot_read_still_blocks_but_is_only_a_count` · `::test_mixed_children_name_the_readable_and_count_the_rest` 이 그 층에서 센다 |
| **새 예외 1건** — `WORK_CHILDREN_DIRECT_NESTING`(409) | `src/ax_workspace/modules/work/errors.py:47-71`(클래스, `blocking` 포함) · `entrypoints/http.py:550`(409 매핑) | `test_task_parent_change.py::test_moving_under_the_same_holder_breaks_the_direct_children_and_is_refused` — 기존 `WORK_DIRECT_NESTING` 문장과 **다름**을 함께 센다 |
| **7 — 프로젝트 자손 파급** | `application.py:668-688` | `::test_moving_the_parent_carries_the_project_down_to_grandchildren` · `::test_a_new_parent_without_a_project_empties_the_whole_subtree` |
| 자손에 남은 선행 → 기존 코드 재사용 | `application.py:679-681` (`_require_project_unlocked`) | `test_task_parent_change.py::test_a_descendant_holding_a_predecessor_refuses_the_whole_move` — 상위도 프로젝트도 **아무것도 안 움직임**을 전수로 센다 |
| `clear_parent` 면 프로젝트는 그대로 | `application.py:670`(`if parent is not None:` 로 갈린다) | `test_task_parent_change.py::test_clear_parent_detaches_the_task_and_leaves_the_project_alone` |
| 검사와 저장이 한 transaction · 부분 이동 없음 | 게이트 전부가 값 변경 **앞**에 · 조립층이 한 session | `test_task_parent_change.py::test_a_descendant_holding_a_predecessor_refuses_the_whole_move` |
| 회차 상승 · 진행 기록 | 기존 `update()` 말미 그대로 (`task.version += 1` · `record_activity`) | `test_task_parent_change.py::test_the_patch_now_takes_the_parent_field_and_moves_the_task` — 활동 요약에 `parent_task_id` 가 들어감을 센다 |
| **소급 재배치 없음** | 서버가 하위를 옮기는 코드가 없다 | `test_task_parent_change.py::test_the_server_never_relocates_children_on_its_own` — `application.py` 를 **AST 로 파싱**해 `*.parent_task_id = ` 대입이 **한 곳**이고 그것이 `task.parent_task_id`(옮겨지는 업무 자신)임을 센다 |
| **검증 6 이 7 보다 먼저** | `application.py:667`(6) → `:668-688`(7) | `test_task_parent_change.py::test_the_children_gate_runs_before_the_project_cascade_gate` — 둘 다 걸리는 이동에서 6 의 문장이 나온다 |
| **자손 전체를 돌지 않는다**(V-8) | `children_of` 만 부른다 | `::test_the_gate_looks_at_direct_children_only_and_not_the_whole_subtree`(표면) + `tests/unit/…::test_the_gate_asks_for_direct_children_only`(질의 전수) — **왜** 직속만 보는지가 두 곳 docstring 에 있다 |

### Phase B-3 — 후행 해제 명령

| 작업 | 어디 | Acceptance 충족 근거 |
|---|---|---|
| 라우트 하나 — A · B 식별자 둘 + **B 의 `expected_version`** | `entrypoints/http.py:1709-1732` `DELETE /api/tasks/{task_id}/successors/{successor_task_id}?expected_version=` | 회차를 **질의 문자열**로 받는다 — `DELETE …/checklist/{item_id}` 가 이미 그 모양이다 |
| 활성 행 하나를 **닫는다**(지우지 않는다) | `work_tasks.py:1187-1214` (`predecessor_link` · `release_predecessor_link`) | `test_task_successors.py::test_the_owner_of_a_predecessor_may_release_their_own_successor` — 행이 **남아 있고** `released_at`·`released_by` 가 찬 것을 DB 로 확인 |
| **B 의 회차가 오르고 B 의 진행 기록에 남는다. A 는 안 움직인다** | `application.py:1555-1562` | 그 같은 테스트 (`…may_release_their_own_successor`) |
| 권한 — **A 또는 B 를 고칠 수 있으면** | `application.py:1572-1585` (`_may_edit_either`) | A 담당자 → `::…may_release_their_own_successor` · B 담당자 → `::test_the_owner_of_the_successor_may_close_the_same_relation` · 둘 다 아니면 403 → `::test_a_bystander_who_may_edit_neither_side_gets_403` |
| **멱등이 아니다** — 이미 닫혔으면 404 | `application.py:1547-1550` | `test_task_successors.py::test_releasing_twice_is_not_idempotent` — 「두 사람이 동시에 닫으면 먼저가 이기고 늦은 쪽이 404」가 같은 테스트다 |
| 성공 응답 = 갱신된 A 의 후행 묶음 | `application.py:1564-1570` · 타입 `task_results.py:350-365` | `test_task_successors.py::…may_release_their_own_successor` |
| **제안을 만들지 않는다** | 제안 경로를 부르지 않는다 | `test_task_successors.py::…may_release_their_own_successor` (`TaskProposalRecord` 조회) — `TaskProposalRecord` 가 **0건**임을 DB 로 확인 |
| **알림을 만들지 않는다** | `application.py:1524-1529` 에 ⚠ 주석 | `test_task_successors.py::test_the_release_command_never_calls_the_notification_module` — `SqlAlchemyNotificationRepository.emit` 을 monkeypatch 로 걸고 **호출 0건**임을 센다(「모듈이 없어서 안 불렀다」가 근거가 될 수 없게) |
| 해제 뒤 B 의 시작 게이트가 열린다 | (결과) | `test_task_successors.py::test_releasing_the_last_predecessor_opens_the_successors_start_gate` — 409 → 해제 → 200 |
| 비공개 후행에는 입구가 없다 | `application.py:1536-1539` | `test_task_successors.py::test_a_private_successor_cannot_be_released_through_this_command` — 식별자를 지어내 불러도 404 이고 **관계는 살아 있다** |

**알림의 자리 — 두 곳에 주석으로 남겼고 구현하지 않았다**: `application.py:1524-1529`(후행 해제 → B 의 게이트가 열림) · `application.py:685-688`(상위 이동 → 자손의 프로젝트가 옮겨짐). SPEC-007 §5 가 「같은 자리가 하나 더 있다」로 지목한 그 둘이다.

---

## 3. 인덱스 설치 방법과 근거 (§3)

**답: 모델 metadata + 손으로 적용하는 `.sql` 쌍. `schema_sync` 를 고치지 않았다.**

### 먼저 확인한 것

`bootstrap/schema_sync.py:30-33` 이 `CreateIndex` 를 내는 갈래는 **「표가 라이브에 없을 때」 하나**다. 기존 표에 대해서는 `:34-43` 이 **컬럼만** 순회한다. 그래서 `task_predecessors`(이미 사는 표)에 더하는 인덱스는 `make sync-demo-schema` 로 **절대 생기지 않는다** — BASE-002 O-24 그대로다.

### 왜 `schema_sync` 를 확장하지 않았나

확장은 기술적으로 쉽다(모델 인덱스 이름 ↔ `inspector.get_indexes()` 이름 비교 후 `CreateIndex`). **하지만 그 한계를 «계약으로» 고정한 PostgreSQL 테스트가 이미 있다** — `tests/integration/postgres/test_task_lifecycle_v2_schema_postgres.py:322` `test_postgres_w2_a_dropped_index_on_an_existing_table_needs_the_manual_sql_not_schema_sync`. 확장하면 그 테스트가 깨지고, 그것은 WORK-007 이 허가하지 않은 계약 변경이다(§Scope Out 에 없고 § Domain/Schema 는 「인덱스 하나」만 요구한다). **눈에 띄는 개선은 리포트에 적고 넘어간다**가 브리프 §6 이다 → §7 ③.

### 무엇을 했나

| 자리 | 무엇 | 누가 적용하나 |
|---|---|---|
| `platform/persistence.py:1027-1034` | `Index("ix_task_predecessors_predecessor_task_id", "predecessor_task_id")` — **정의의 SoT** | **새로 만드는 DB**: `create_all`(= `reset_demo` · `make reset-demo` · 모든 테스트) |
| `backend/migrations/manual/2026-09-28-w7-successor-index.sql` | `CREATE INDEX IF NOT EXISTS` — 트랜잭션 안에서 돈다 | **격리 PostgreSQL·demo DB**: `psql -1 -f` |
| `backend/migrations/manual/2026-09-28-w7-successor-index.concurrent.sql` | 같은 정의 + `CONCURRENTLY` | **운영**: 사람이 autocommit 으로. 쓰기를 막지 않는다 |

**W2 의 선례를 글자 그대로 따랐다** (`2026-09-17-w2-indexes.sql` 쌍). 파일 머리에 언제 쓰나·왜 파일인가·실패했을 때·되돌리기를 그 판과 같은 순서로 적었다.

**일반 API startup 은 DDL 을 돌리지 않는다** — 손댄 자리가 `persistence.py` 의 모델 선언과 `migrations/manual/` 뿐이고, `entrypoints/http.py` 의 startup 경로에 스키마 코드를 넣지 않았다.

### 검증

`tests/integration/postgres/test_work007_successor_index_postgres.py` — W2 테스트와 **같은 다섯 단계**로 재현해 닫는다: ① 인덱스를 내린다 → ② `schema_sync` 를 돌려도 돌아오지 않는다 → ③ `.sql` 을 적용하면 선다 → ④ 재적용해도 실패하지 않는다 → ⑤ `pg_index` 가 valid·ready 라고 말한다. 두 `.sql` 의 정의가 `CONCURRENTLY` 한 낱말만 다른 것도 텍스트로 센다.

---

## 4. 검증 결과 — 명령과 «수치»

| 명령 | 결과 | 비고 |
|---|---|---|
| `make test-unit` | **389 passed, 1 deselected** (12.60s) | `tests/unit` + `tests/architecture`. **실측이다** — 검수 반영 판에서 다시 재서 넣었다. ⚠ **앞판 리포트의 381 은 틀렸다**: `tests/unit/test_task_children_nesting_gate.py`(8건)를 **만들기 전**에 잰 수를 적고 괄호에 「8건이 더해진 수」라고 붙였다(검수 W-1). 381 + 8 = 389. **양쪽 다 0 failed 이므로 결론은 안 바뀐다** |
| `make test-contract` 병렬 패스 | **1123 passed, 0 failed** (5:14) | 검수 반영 판의 실측이다. **수가 맞는다**: 새 테스트 파일을 쓰기 전 이 패스는 `1074 passed / 1 failed`(= 1075 수집) → 계약 파일 둘(18 + 24) = **1117** → 검수 반영이 6건(후행 2 · 상위 4) = **1123**. 그 1 failed 가 §아래의 「대체된 계약」이고 고쳐서 passed 로 넘어왔다 |
| `make test-contract` 직렬 패스 (`test-contract-serial`) | **128 passed, 1136 deselected** (6:22) | `@pytest.mark.serial` 만. 내 새 테스트에 그 마커가 붙을 이유가 없다(자식 프로세스·스레드를 띄우지 않는다) — deselected 가 1130 → 1136 으로 **정확히 6** 늘어난 것이 그 사실이다. ⏱ 앞판보다 1분 반 느린 것은 **같은 워크트리에서 FE 워커가 함께 돌아** 기계가 실시간 창을 나눠 쓴 결과다(직렬 패스는 그 창에 민감하다) |
| `make test-contract` 전체 | **exit 0** — 두 패스 모두 green | 0 failed |
| 신규 `tests/contract/test_task_successors.py` | **20 passed** | B-1 · B-3 (검수 반영으로 2건 추가) |
| 신규 `tests/contract/test_task_parent_change.py` | **28 passed** | B-2 (검수 반영으로 4건 추가) |
| 신규 `tests/unit/test_task_children_nesting_gate.py` | **8 passed** | 게이트 6 의 도달 불가 갈래 |
| 신규 `tests/integration/postgres/test_work007_successor_index_postgres.py` | **2 passed** (선언·텍스트) + **2 passed** (`-m integration`, 격리 `ax_test`) | 아래 주의 |
| `tests/architecture/test_operation_inventory.py` | 4건 전부 통과 | drift 해소 확인 |

**새로 쓴 테스트 합계 60건 — 전부 통과.** (20 + 28 + 8 + 4. 그 4 중 2 는 `@pytest.mark.integration` 이라 격리 PostgreSQL 에서 따로 돌렸다.) 검수 반영 판이 6건을 더했다 — §8 참조.

**PostgreSQL 실행 범위 — 사용자 포트·프로세스를 건드리지 않았다.** `POSTGRES_TEST_URL` 기본값은 `…:54329/ax_test` 이고 사용자의 demo DB 는 `ax_demo` 다(`Makefile:1` vs `:10`). 내가 돌린 것은 **내 새 파일 하나**이고 쓴 대상은 `ax_test` 뿐이다 — 프로세스를 죽이거나 재시작하지 않았고 `ax_demo` 를 건드리지 않았다. **`make test-postgres` 전량과 `make verify` 는 브리프대로 돌리지 않았다** — 코디네이터 몫이다.

### 기존 실패 1건 — 「무관」이 아니라 **대체된 계약**이다

`tests/contract/test_task_lifecycle_v2.py::test_lifecycle_v2_the_parent_link_is_fixed_at_creation_so_no_cycle_can_be_made`

그 테스트는 「상위를 **옮기는 명령이 없다**(미정 EU-15)」를 근거로 `PATCH` 의 `parent_task_id` 가 **알 수 없는 필드로 422** 임을 셌다. SPEC-007 §4 가 그 자리를 명시적으로 열었다 — 「지금은 이 칸을 보내면 422 이고 **이 SPEC 이 그 자리를 연다**」, AC 도 「(지금은 보내면 422 다)」로 같은 말을 한다. **그래서 고쳤고, 고친 방식이 요점이다**: 상태 코드(422)와 결론(「고리를 만들 수 없다」)을 **그대로 두고** 근거만 `extra='forbid'` → 순환 검사(`WORK_PARENT_CYCLE`)로 바꿨다. 자기 자신 갈래도 함께 더했다. 파일 머리 docstring 의 「`WORK_PARENT_CYCLE` 은 도달 경로가 없다」 한 줄도 같이 갱신했다.

---

## 5. 손대지 않고 남긴 것

### ① MCP `task_update` 에 `parent_task_id` 를 **열지 않았다**

SPEC-007 §5 가 「`parent_task_id` 를 MCP 쪽에도 여는지는 `30-work/` 가 저장소 관례에 맞춰 정한다 **(제안)**」로 이 결정을 보냈다. **열지 않기로 정했다** — 근거 둘:

1. 그 도구는 이미 `preceding_task_ids`·`approver_id` 를 **받지 않고**, SPEC-007 §5 와 WORK-007 Out 이 그 어긋남을 **이 판이 고치지 않는다**로 못 박았다. 셋 중 하나만 열면 비대칭이 **더 불규칙**해진다.
2. **위임(AX) 갈래는 이미 두 칸을 갖는다.** 확인 카드는 `TaskUpdateCommand` 의 JSON schema 를 일반적으로 순회하므로(`platform/actions.py:1848-1862`) 새 칸 둘이 자동으로 편집 필드가 된다. 즉 「에이전트가 상위를 옮긴다」는 경로가 실제로는 **열려 있다** — 손으로 적은 좁은 도구 서명만 그대로다.

**따라온 결과**: `parent_task_id` 는 그 필드 빌더의 `select` 목록(`assignee_id`·`member_id`·`referenced_task_id`·`resource_id`·`output_material_ids`·`project_id`)에 없으므로 **후보 목록 없는 텍스트 칸**으로 선다. 상위 후보 목록을 내는 계약이 어디에도 없어 만들지 않았다.

### ② `TaskVersion` snapshot · diff — 그대로다

`task_snapshot()` 에 `parent_task_id`·`project_id`·`preceding_task_ids` 가 여전히 없고 `_DIFFABLE_FIELDS` 도 그대로다. 그래서 **이번 판이 연 두 쓰기(상위 이동 · 후행 해제)도 버전 이력에서 복원되지 않는다.** 활동 로그에는 남는다(상위 이동은 `task.updated` 요약에 `parent_task_id`, 후행 해제는 B 의 `task.predecessor_released`). WORK-007 Out 「이력·diff 에 관계 변경 싣기 — 기록만」 그대로다.

### ③ `schema_sync` 는 기존 표에 인덱스를 못 더한다 — 그대로다

§3 에 근거를 적었다. **고칠 가치가 있는 자리로 본다**: 지금 구조에서는 기존 표에 인덱스를 더할 때마다 `.sql` 쌍 + 그것을 적용·검증하는 PostgreSQL 테스트가 함께 생긴다(W2 가 하나, 이 판이 둘째). 다만 그 한계를 **계약으로 고정한 테스트**가 있어 이 판의 권한 밖이다.

### ④ 그 밖 — 전부 WORK-007 Out 그대로

`RelationGraph` 에 선행·후행 엣지 없음 · 생성 표면끼리 받는 값 맞추기 · 오류 본문의 기계용 `code` · 소급 재배치 · EU-8 담당 변경 갈래 · 프로젝트 화면의 후행 역산(SPEC-005 D-07) · `references` 가 `read_only` 갈래에 없는 것(SPEC-007 §2.7 이 그 사실을 적고 넘어간다 — test 가 그것을 **현행으로** 센다).

### ⑤ `frontend/` — 한 줄도 건드리지 않았다

`git status` 에 `frontend/` 가 없다.

---

## 6. 기준선 실패 (무관한 기존 실패)

**없다.** 시작 시점에 `make test-unit` 이 2건 실패했는데 둘 다 **내 변경이 만든 운영 대장 drift**였고(`test_operation_inventory.py`) 대장을 패치해 닫았다. `make test-contract` 의 1건은 §4 대로 **대체된 계약**이라 「무관」이 아니다.

무관한 소음 하나만 적는다: `StarletteDeprecationWarning: 'HTTP_422_UNPROCESSABLE_ENTITY' is deprecated` 가 여러 테스트에서 뜬다. **내 변경과 무관하고** 기존 코드 전체에 걸린 경고다 — 고치지 않았다.

---

## 7. 미결·주의점

1. **`parent_for()` 안의 검증 순서가 SPEC 표와 다르다.** SPEC-007 §4 표는 1→2→3→4→5 인데 실제는 **1→4→2→3→5**(순환이 끝난 업무·담당 미확정보다 먼저). **거절의 집합은 같고** 한 요청에 여럿 걸렸을 때 먼저 말하는 것만 다르다. WORK-007 이 「1~5 는 기존 `parent_for()` 를 **그대로** 쓴다」이므로 포크하지 않았다 — 포크하면 V-8 판정이 두 벌이 되고 그것이 바로 이 판이 피하려는 어긋남이다. **뒤집을 값어치가 있으면 SPEC 표를 실제 순서로 고치는 쪽을 권한다.**

2. **게이트 6 의 「못 읽는 하위」 갈래는 HTTP 표면에서 도달 불가다.** 게이트가 서는 조건이 「담당자가 이 업무의 담당자와 같은 직속 하위」이고 업무 편집은 **그 업무를 든 사람**만 부를 수 있으므로(소유 투영), 실제 요청에서 막는 하위는 **언제나 부르는 사람 자신이 든 것**이고 반드시 읽을 수 있다. SPEC-007 §4 의 「읽을 수 없는 하위까지 전부 센다」는 그래서 **방어**다 — 그 절반을 `tests/unit/test_task_children_nesting_gate.py` 가 그 층에서 센다. **계약을 약하게 구현하지 않았고, 표면 테스트로 있는 척하지도 않았다.**

3. **후행 해제의 회차 어긋남을 409 로 냈다 — 기존 업무 편집은 422 다.** SPEC-007 § Case Matrix 가 `WORK_VERSION_STALE` 을 **409**(「후행 해제의 B 의 회차 포함」)로 고정했는데, 레포의 업무 표면 현행은 `InvalidTaskTransition("task version is stale")` → **422** 다. **기존 422 를 바꾸지 않고** 새 예외(`TaskSuccessorVersionConflict`)를 409 에 두었다 — 선례가 `TaskScheduleVersionConflict`(「배정 회차는 업무 회차와 다른 예외」)다. **같은 제품에 회차 어긋남 상태가 둘이다.** 정리하려면 별도 판정이 필요하다.

4. **프로젝트 파급의 선행 잠금을 「프로젝트가 실제로 바뀔 때만」 걸었다.** SPEC-007 §4 7번이 「**프로젝트 파급**이 선행 잠금에 걸리지 않는가」를 묻기 때문이다 — 파급이 없으면 잠글 것이 없다. 무조건 걸면 **선행을 든 업무는 같은 프로젝트 안에서도 상위를 옮길 수 없게** 된다. 이 선택을 `test_task_parent_change.py::test_moving_inside_the_same_project_is_not_gated_by_predecessors` 이 명시적으로 못 박았다. **AC 가 그 갈래를 직접 말하지 않아 판단이 들어간 자리다** — 뒤집으려면 그 테스트 하나와 `application.py:675` 한 줄이다.

5. **한 `PATCH` 에 `parent_task_id` 와 `project_id` 를 함께 보내면 422 다.** 이동이 먼저 일어나 이 업무가 하위가 되고, 기존 거절 「하위 업무의 프로젝트는 상위 업무를 따릅니다」가 뒤의 `project_id` 를 막는다. 일관적이지만 **화면이 두 칸을 한 번에 저장하려 하면 부딪힌다** — SPEC-007 §2.8.3·OQ-704 가 「칸마다 따로 저장한다」이므로 FE 가 그 순서를 지키면 걸리지 않는다. `test_task_parent_change.py::test_the_project_field_and_the_parent_field_do_not_fight_in_one_patch` 가 현행을 고정했다. **FE Phase F-3 이 알아야 할 계약이다.**

6. **`docs/unified-operations-inventory.json` 이 브리프 §5 의 allowed_paths 문자열 밖이다.** 브리프는 `backend/` · `Makefile` · `docker-compose.yml` · 리포트를 적었는데, WORK-007 Phase B-1 의 작업 목록이 「운영 대장의 그 행 서명을 갱신한다 — 실패 diff 의 그 항목만 패치」를 명시하고 `AGENTS.md` 도 같은 말을 한다. **그래서 고쳤고 diff 는 정확히 그 둘이다**(`task_get.output_schema` · 새 HTTP 행). 코디가 allowed_paths 를 다시 볼 자리로 적어 둔다.

7. **OQ-709(못 읽는 선행만 남았을 때 `[시작]` 을 막나)는 손대지 않았다** — WORK-007 이 「Phase 6 의 한 조각만 gate 한다」로 FE 쪽에 걸어 두었고, 서버의 선행 게이트는 이 판에서 **한 줄도 바뀌지 않았다**.

8. **`clear_parent` 를 `TaskEditFields` 에 둔 결과 확인 카드에 boolean 칸이 하나 생긴다.** 일반 필드 빌더가 schema 를 순회하므로 자동이고 `empty_policy` 는 `forbid`(non-nullable bool)로 떨어진다. 화면 문구를 따로 정하지 않았다.

### 변경 파일 전수

수정 10 · 신규 6.

```
M backend/src/ax_workspace/bootstrap/application.py            (+14)
M backend/src/ax_workspace/entrypoints/http.py                 (+36)
M backend/src/ax_workspace/modules/work/application.py         (+287 -6)
M backend/src/ax_workspace/modules/work/errors.py              (+42)
M backend/src/ax_workspace/modules/work/task_commands.py       (+35 -1)
M backend/src/ax_workspace/modules/work/task_results.py        (+44)
M backend/src/ax_workspace/platform/persistence.py             (+10)
M backend/src/ax_workspace/platform/work_tasks.py              (+60)
M backend/tests/contract/test_task_lifecycle_v2.py             (+22 -5)   ← 대체된 계약
M docs/unified-operations-inventory.json                        (+100 -2)  ← drift 둘만

A backend/migrations/manual/2026-09-28-w7-successor-index.sql
A backend/migrations/manual/2026-09-28-w7-successor-index.concurrent.sql
A backend/tests/contract/test_task_successors.py                          (18건)
A backend/tests/contract/test_task_parent_change.py                       (24건)
A backend/tests/unit/test_task_children_nesting_gate.py                   (8건)
A backend/tests/integration/postgres/test_work007_successor_index_postgres.py (4건)
```

`entrypoints/mcp.py` 는 **무변경**이고, 그래도 상세 도구가 두 칸을 실어 나른다(test 가 센다).
`frontend/` · 문서 리포는 **무변경**이다.

---

## 8. 검수 반영

근거: `review-be-report.md` (**PASS · FAIL 0 · WARN 10**). 코디가 다섯을 고치라고 지정했고
나머지 다섯은 처분했다. **지정된 다섯만 고쳤다.**

### ① W-5 — 게이트 7 거절 문장의 «못 읽는 자손 제목» 누출을 닫았다

| 무엇 | 어디 |
|---|---|
| 게이트를 **목록 기반**으로 바꿨다 — `_require_project_unlocked(principal, tasks)` | `backend/src/ax_workspace/modules/work/application.py:613-648` |
| 잠긴 것만 모은다 | `:633` (`locked = …active_predecessor_ids`) |
| **잠긴 것에만** 읽기를 묻는다 — 정상 경로에서 판정 비용 0 | `:637` |
| 읽을 수 있는 것은 **이름**, 나머지는 꼬리에 건수 | `:639-644` |
| 하나도 읽을 수 없으면 **건수만** | `:646-648` |
| 호출 두 곳을 목록 한 번으로 | 프로젝트 직접 변경 `:566` · 상위 이동 `:723` |

**게이트 6 과 같은 규칙이다** (`_require_children_may_follow` — `application.py:770-781`): 막을지는 **전부**로 정하고
이름은 **읽을 수 있는 것만** 낸다.

**바꾸지 않은 것**: 오류 코드(`WORK_PROJECT_LOCKED_BY_PREDECESSORS` 409)와 문장 머리
(「선행업무를 먼저 비워야 프로젝트를 바꿀 수 있습니다: 」). 기존 테스트 넷이 그 머리를 단언하고
있고 전부 그대로 통과한다 (`test_task_predecessors.py:401`·`:441` ·
`test_project_membership_follows_work.py:612`·`:675`).

**두 경로에 함께 걸었다.** 같은 문장이 두 입구(프로젝트 직접 변경 · 상위 이동)에서 나오는데 한쪽만
가리면 같은 사실이 입구에 따라 새거나 안 새게 된다. 그 이유를 함수 docstring 에 적었다 (`:626-631`).

**테스트 2건 추가**:
- `tests/contract/test_task_parent_change.py:593` `…hides_the_title_of_a_descendant_the_caller_cannot_read`
  — 「볼 수 없는 업무 1건」이 있고 손자 제목이 **없음**을 센다. 무대가 맞는지(빼기 전엔 보인다 →
  뺀 뒤엔 404) 먼저 확인한다. **요청 경로를 쓰지 않는다** — 민아가 요청자가 되면 V-21 이 하위
  트리 전체를 열어 주므로 무대가 성립하지 않는다.
- `:638` `…still_names_a_descendant_the_caller_can_read` — 가리기가 이름을 통째로 없애지 않았음을
  센다. 이 줄이 없으면 「전부 감춘다」로 가도 통과한다.

### ② W-6 — 이동 경로에 프로젝트 «읽기 가드»를 걸었다

| 무엇 | 어디 |
|---|---|
| 상위를 따라 값을 얻는다 (**생성과 같은 답**) | `application.py:704` `inherited = self.project_for(principal, None, parent)` |
| **그 값에 가드만 한 번 더** 지난다 | `:718` `new_project = self.project_for(principal, inherited)` |
| 왜 이렇게 했나 · 두 경로가 갈리는 사실 | `:705-717` (주석) |
| `project_for` 자신에도 갈림을 적었다 | `:385-388` (docstring ⚠) |

**판정을 복제하지 않았다.** 같은 함수에 `parent=None` 으로 값을 다시 넣어 아래쪽 가드
(`:394-396`)를 그대로 지난다. **거절도 기존 것 그대로** — `TaskNotFound("project was not found")`
→ **404**. 새 코드를 만들지 않았다.

**생성 경로는 건드리지 않았다** (브리프 §1②·§3). 두 경로가 갈리는 이유를 코드에 적었다: 생성은
**새 업무 하나**를 세우는데 이동은 **이미 있는 서브트리 전체**를 옮긴다 — 상위 P 는 읽으면서 P 의
프로젝트는 못 읽는 사람이 자기 트리를 그 프로젝트로 밀어 넣으면, 그 프로젝트를 아는 사람들의
화면에 그가 읽을 수도 없는 자리로 업무가 나타난다.

**테스트 2건 추가**:
- `test_task_parent_change.py:662` `…a_parent_whose_project_the_caller_cannot_read_is_refused`
  — 참조자(cc)로 상위 **하나만** 읽는 사람이 그 상위의 비공개 프로젝트로 못 밀어 넣는다.
  404 이고 본문이 `project was not found` 이며 상위도 프로젝트도 안 움직인다.
- `:692` `…the_creation_path_still_inherits_without_the_guard` — **갈림을 못질한다.** 같은 상위
  아래에 **새 업무를 만드는** 것은 통과하고 프로젝트를 물려받으며, 그 프로젝트는 여전히 못 읽는다.
  나중에 누가 「일관성」을 이유로 한쪽을 맞추려 할 때 이 테스트가 그 결정이 있었음을 말한다.

### ③ W-8 — 테스트 구멍 셋을 닫았다

| 구멍 | 어디 |
|---|---|
| ① 후행의 **섞인 갈래** | `tests/contract/test_task_successors.py:184` `…a_mix_of_readable_and_hidden_successors_splits_into_the_array_and_the_count` — 배열에 하나 + `hidden_successor_count == 1`. 앞판은 「전부 보인다(0)」와 「전부 가려진다(1)」 두 끝뿐이었다 |
| ② **응답 전용 입력 거절** | `:214` `…the_two_successor_fields_are_response_only_and_refused_as_input` — `PATCH` 와 `POST` **두 입구**에 두 필드를 넣어 각각 422 이고 본문에 그 필드명이 있음을 센다. 그리고 **아무것도 바뀌지 않았음**(회차·후행 배열)을 확인한다 |
| ③ **약한 단언** `:177` | `:179-181` 로 교체 — `json.dumps(view)` 로 응답 **전체**를 직렬화해 식별자와 제목 두 문자열을 찾는다. 앞줄의 `== []` 때문에 항상 참이던 줄(그리고 문자열 vs dict 비교라 애초에 원하던 비교도 아니던 줄)을 **어느 칸에 새더라도 걸리는** 검사로 바꿨다. 같은 교체를 새 섞인-갈래 테스트에도 썼다(`:209-211`) |

### ④ W-1 — §4 수치를 실측으로 교체했다

`make test-unit` → **389 passed, 1 deselected, exit 0** (12.60s). 검수 실측과 **같다**.
앞판의 381 은 `tests/unit/test_task_children_nesting_gate.py`(8건)를 **만들기 전** 수였고
괄호 설명이 사실과 어긋났다 — §4 첫 줄에 그 경위를 그대로 적었다. 두 수 모두 0 failed 라
결론은 뒤집히지 않는다.

### ⑤ W-9 — 인덱스는 **코디가 데모 DB 에 적용 완료**

`ix_task_predecessors_predecessor_task_id` 가 `ax_demo` 에 붙었다 — **코디가 적용했다.**
워커가 한 일은 없다. 정의의 SoT 는 모델 metadata(`platform/persistence.py:1027-1034`)이고
적용 단위 `.sql` 쌍은 `backend/migrations/manual/2026-09-28-w7-successor-index*.sql` 이다.

### 손대지 않은 것 — 코디가 처분한 다섯

| WARN | 처분 | 이 판에서 |
|---|---|---|
| W-2 `inventory.json` allowed_paths 밖 | 인정 | 그대로 |
| W-3 `parent_for` 순서 ≠ SPEC 표 | **SPEC 표를 고친다**(writer 몫) | 코드 그대로. §7 ① 이 그 사실을 이미 적고 있다 |
| W-4 회차 409/422 공존 | 그대로 둔다 | 코드 그대로. §7 ③ 이 기록 |
| W-7 AX 확인 카드 두 칸 자동 개방 | 승인 | 그대로. §5 ① · §7 ⑧ 이 기록 |
| W-10 `parent_task_id`+`project_id` 동시 PATCH 422 | FE 계약으로 넘긴다 | 그대로. §7 ⑤ 가 기록 |

그리고 이 판도 **알림을 구현하지 않았다** — 여전히 범위 밖이고 자리 표시 둘은 그대로다
(`application.py` 의 후행 해제 · 프로젝트 자손 파급).

### 검수 반영 판의 변경 파일

```
M backend/src/ax_workspace/modules/work/application.py   ① 게이트 7 가리기 · ② 이동 경로 읽기 가드
M backend/tests/contract/test_task_successors.py         ③①② 신규 2건 · ③③ 약한 단언 교체
M backend/tests/contract/test_task_parent_change.py      ①② 신규 4건
M (문서) be-report.md                                     ④ §4 수치 · 이 §8
```

`entrypoints/mcp.py` · 생성 경로(`parent_for` 의 create 갈래) · `docs/unified-operations-inventory.json` 은
**이 판에서 무변경**이다. 커밋·push·PR 하지 않았다.

⚠ **워크트리의 `frontend/` 에 변경이 있는데 내 것이 아니다.** 이 판이 도는 동안 같은 워크트리에서
**FE 워커가 함께 돌았다**(`WorkModals.tsx` · `workRows.ts` · `api.ts` · `labels.ts` ·
`viewModels.ts` · `styles/` · 신규 `styles/task-detail.css`). 나는 `frontend/` 를 한 줄도
건드리지 않았다 — 코디가 두 워커의 diff 를 가를 때 이 줄을 근거로 쓰면 된다.
