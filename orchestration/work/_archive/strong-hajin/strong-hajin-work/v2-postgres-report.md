# WORK-002 v2 — PostgreSQL 동시성·스키마 검증 보고

- 작성: postgres 워커 (`term_2e64fd06-507c-460d-accd-2c91b8863dd8`) · 2026-09-17
- 코드 워크트리: `/Users/kknaks/orca/workspaces/Strong_hajin/strong-hajin-work`
- 계약: SPEC-003 §3 S-16 · §4/5/6 C1·C2 · WORK-002 Phase 1/3/5/8 및 §검증 계획
- **커밋·push·PR 없음.** 워크트리에 변경만 남겼다.

## 1. 실제 데이터베이스 — 무엇에 붙어 돌았나

| 값 | 실제 |
|---|---|
| `DATABASE_URL` (운영/사용자) | `postgresql+psycopg://ax:ax@localhost:54329/ax_demo` — **손대지 않았다** |
| `POSTGRES_TEST_URL` (격리) | `postgresql+psycopg://ax:ax@localhost:54329/ax_test_v2_pg` — **이번에 새로 만든 격리 DB** |
| Makefile 가드 | `test-postgres` 가 두 값이 **다를 때만** 돈다 (`Makefile:53`). 매 실행에서 통과했다 |
| 테스트가 실제로 연 URL | `AX_POSTGRES_TEST_URL` 하나 — 로그 첫 줄에 매번 찍힌다 (`/tmp/v2-pg-logs/*.log`) |

- 격리 DB 생성: `CREATE DATABASE ax_test_v2_pg OWNER ax` (54329). **다른 DB 는 생성·초기화·DDL 대상이 아니다.**
- `ax_test`, `ax_test_w1`, `ax_test_acceptance` 에는 **한 번도 연결하지 않았다.**
- PostgreSQL 서버·포트·프로세스는 시작도 종료도 하지 않았다. 5432 는 건드리지 않았다.
- **읽기 전용 확인 한 건**: `ax_demo` 는 사용자 스키마 표가 **0개**다(`information_schema.tables` 조회).
  이번 fixture 통과와는 다른 사안이며, **배포 직전 실데이터 재확인 조건은 그대로 남는다**(WORK-002 §Pre-deploy).

## 2. 실행 명령과 실제 rc — 숨긴 실행 없음

모든 진입은 `make test-postgres` 뿐이다. `uv run pytest` 를 직접 부른 적이 없다.
전체 stdout/stderr 와 rc 는 `/tmp/v2-pg-logs/` 에 그대로 있다.

| # | 명령(범위) | 로그 | rc | 결과 |
|---|---|---|---|---|
| 1 | `PYTEST_ADDOPTS="-k assistant_character"` (연결 확인) | `smoke-01.log` / `.exit` | 0 | 1 passed |
| 2 | **전체** (현상태 진단) | `baseline-full-01.log` / `.exit` | 2 | **65 collected · 63 passed · 2 failed** (142s) |
| 3 | `-k task_lifecycle_v2_postgres` | `v2-race-01.log` | 2 | 4 passed · 2 failed |
| 4 | `-k 'resending_one_handover or parent_completing_while_a_child'` | `v2-race-02.log` | 2 | 1 passed · 1 failed |
| 5 | `-k parent_completing_while_a_child` (증거 문구) | `v2-race-03.log` | 2 | 1 failed — 결함 확정 |
| 6 | `-k v2_schema_postgres` | `v2-schema-01.log` | 0 | **5 passed** |
| 7 | `-k 'parent_completion_waits or child_reopen_is_refused'` (BE 수정 후) | `v2-race-04.log` | 0 | 2 passed |
| 8 | 같은 범위 (잠금 관측 조회 교정) | `v2-race-05.log` → `v2-race-06.log` | 2 → 0 | 1 failed → **2 passed** |
| 9 | 신규·수정 묶음 전부 | `v2-group-01.log` | 0 | **14 passed** |
| 10 | **최종 전체 1회** | `final-full-01.log` / `.exit` | (§7) | (§7) |

## 3. 기존 8파일 — W1 보장을 새 계약으로 **교체**했다 (삭제·skip·약화 없음)

진단 실행에서 난 2건은 **둘 다 v2 계약 변경**이었다. 제품 결함이 아니라 W1 당시의 기대값이 낡은 것이다.

| 테스트 | W1 이 지키던 것 | v2 에서 실제 | 어떻게 교체했나 |
|---|---|---|---|
| `test_postgres_integration.py::test_postgres_keeps_one_open_assignment_per_task_through_a_handover` | 열린 담당 행이 **1개** | `[mina active, jiho pending]` — 제안이 기존 담당을 닫지 않는다 (Phase 3 · 정책 V-18) | 「열린 행 1」을 **「활성 담당 정확히 1」**(K-3)로 옮겼다. 대기 제안은 **하나**이고 `supersedes_assignment_id` 가 그 활성 행을 가리키며, **아직 `superseded` 행이 없다**(교체는 수락 한 덩어리에서만)까지 함께 단언한다. 두 사람이 동시에 들 수 없다는 W1 문장은 그대로 산다 |
| `test_postgres_integration.py::test_postgres_promotes_one_meeting_candidate_into_one_task_under_concurrency` | 동시 발송 뒤 담당이 `active` | `pending` — **발송은 담당을 세우지 않는다** (Phase 2 · 정책 V-10) | 담당 행이 **정확히 하나**이고 그 하나가 `("jiho","pending")` 임을 단언. 같은 키의 동시 발송이 요청 1건·업무 1건이라는 W1 보장은 그대로 |

- 이름은 바꾸지 않았다(기준선 diff 를 흔들지 않으려고). 대신 docstring 에 「one open assignment」가 이제 **활성 담당 하나**를 뜻한다고 적었다.
- 나머지 6파일(`test_material_owners` · `test_material_upgrade` · `test_postgres_assignment_decision_replay` · `test_postgres_browser_interactions` · `test_postgres_extended_confirmation` · `test_postgres_material_worker_recovery` · `test_project_participation`)은 **손대지 않았다.** 자료 worker 관련 실패는 **한 건도 없었다** — timeout 을 올리거나 오류를 삼킨 자리가 없다.
- 기존 M 표시 4개는 W1 미커밋 기준선이다. **HEAD 로 되돌리지 않았고 v2 변경으로 오인하지도 않았다.**
- 직접 취소(`/api/tasks/{id}/cancel`)를 부르는 PG 테스트는 **없다.** `reason` 필수화의 영향 범위가 이 디렉터리에 닿지 않는다(확인: `grep`).

## 4. C1 · C2 — 실제 경합 (신규)

**파일**: `backend/tests/integration/postgres/test_task_lifecycle_v2_postgres.py`
(도우미: `backend/tests/integration/postgres/v2_pg_support.py` — 테스트를 담지 않는다)

전부 `Barrier`/`Event` 로 **두 transaction 이 실제로 겹친 뒤에야** 첫 잠금이 일어나게 만든다.
겹치지 못하면 barrier 가 시간 초과로 깨져 **시험이 실패한다** — 우연한 순차 실행이 통과로 새지 않는다.

| 경합 | 테스트 | 무엇을 못 박았나 |
|---|---|---|
| **수락 ↔ 철회** (S-16 3 · K-4) | `test_postgres_accepting_and_withdrawing_one_request_never_both_land` | 같은 원 회차로 동시에 와도 **정확히 하나만** 200, 다른 하나는 정의된 거절. 요청 회차가 **한 칸만** 오른다. 이긴 쪽이 수락이면 업무는 `open` + 활성 담당 1(jiho), 철회면 `cancelled`/`request_withdrawn` + **활성 담당 0**. `cancel_reason` 이 있는 것과 상태가 서로 어긋나지 않는다. **승자는 고정하지 않는다 (EU-17)** |
| **담당 교체 수락 ↔ 거절** (S-16 4 · K-3) | `test_postgres_handover_acceptance_and_decline_never_leave_the_task_unheld` | 하나만 서고, 경합이 도는 **내내** 별도 연결이 센 활성 담당이 **언제나 1**(책임 공백 없음). 수락이 이기면 `active(mina) + superseded(jiho)`, 거절이 이기면 `active(jiho) + declined(mina)`. **어느 쪽이든 업무는 취소되지 않는다**(O-13 — 교체 제안의 거절은 제안만 닫는다) |
| **같은 답 동시 재전송** (S-16 1 · K-1) | `test_postgres_resending_one_handover_answer_at_once_is_still_one_answer` | 담당 행이 **둘 그대로**(세 번째가 안 생긴다), 활성 1, **그 사람의 판단 행은 한 건**. 500 이 아니다. **영수증의 상태 코드는 확정하지 않는다** — 제품이 정하는 중인 자리다. 판단함 경유의 같은 자리는 기존 `test_postgres_assignment_decision_replay.py::test_assignment_simultaneous_same_decision_replays_after_the_owner_lock` 를 이름으로 연결하고 다시 짓지 않았다 |
| **상위 완료 ↔ 하위 재개 ①** (S-16 5 · L-13) | `test_postgres_a_parent_completion_waits_for_the_child_reopen_that_holds_it` | 재개가 상위 행을 먼저 잡으면 완료가 **실제로 줄을 선다** — `pg_stat_activity`(이 DB 로 한정, `pg_blocking_pids`)로 **대기를 눈으로 확인한 뒤에야** 재개를 놓아준다. 풀려난 완료는 `409 WORK_CHILDREN_UNFINISHED` 로 막히고 상위는 `in_progress` 로 남는다 |
| **상위 완료 ↔ 하위 재개 ②** | `test_postgres_a_child_reopen_is_refused_by_the_parent_that_completed_first` | 반대 순서 — 재개는 하위를 쥔 채 **상위를 잡으러 가기 직전**에 멈추고(인위 교착이 아니다: 완료는 자기 한 행만 잡으므로 막히지 않는다), 완료가 커밋한 뒤 풀려나 `409 상위 업무가 완료…` 로 막힌다. 하위는 `done` 그대로다 |
| **같은 키 동시 생성** (S-16 1) | `test_postgres_the_same_creation_key_sent_at_once_stands_one_task` | `POST /api/tasks` 동시 두 번 → 201·201, **같은 `task_id`**, 업무 1건·담당 행 1건(`mina/active`). 발송 쪽 같은 자리는 기존 `..._promotes_one_meeting_candidate_into_one_task_under_concurrency` 로 연결 |
| **영수증 전 권한 재검사** (S-16 2 · K-2) | `test_postgres_a_resent_creation_key_asks_for_the_right_to_read_again` | 같은 키 재전송은 영수증이지만, `work_request.read` 를 회수한 뒤의 재전송은 **403/404 로 존재를 숨긴다.** 거절이 새 요청을 만들지도, 있던 것을 지우지도 않는다 |

**공통 불변식**: 두 재개 시험은 `_no_open_child_under_a_settled_parent()` 한 줄을 함께 지킨다 — **끝난 상위 아래 열린 하위가 없다**.

**미정은 미정으로 뒀다.** EU-17(수락↔철회 승자, 상위 취소 뒤 하위 수락)·OQ-203(제출의 하위 검사)·OQ-206(승격 요청 완료 승인)은 **어느 단언으로도 확정하지 않았다.** 선행·후행 강제와 부모 취소 후 수락 우선순위도 마찬가지다.

## 5. 제품 결함 1건 — 발견·보고·수정 후 재확인

| 항목 | 내용 |
|---|---|
| 증상 | 상위 완료와 하위 재개가 겹치면 **상위 `done` + 하위 `in_progress`** 가 함께 남았다(둘 다 200). 정책 L-13·L-14 위반 |
| 실제 증거 | `v2-race-03.log`: `상위=done(완료 200) · 하위=in_progress(재개 200)` |
| 원인 | `modules/work/application.py` 의 `reopen()` 이 상위를 `task_by_id(parent_id)` 로 **잠금 없이** 읽었고, `transition()` 은 완료 대상 행만 `FOR UPDATE` 로 잡은 뒤 하위를 잠금 없이 읽었다 — 서로 다른 행만 잠그므로 READ COMMITTED 의 write skew 가 그대로 났다 |
| 처리 | 제품은 **고치지 않았다.** 근거와 방향(상위 읽기를 `lock=True` 로; 완료가 이미 상위를 먼저 잡으므로 잠금 순서 역전 없음)을 원BE·코디에 단문으로 전달하고 **실패 테스트를 유지**했다 |
| 수정 후 | 원BE 가 `reopen` 의 상위 읽기를 `lock=True`(+`populate_existing`)로, 완료·승인은 자기 행만 잡도록 고쳤다. **두 순서 모두 실제 잠금 대기를 확인하며 통과**(`v2-race-06.log`, rc 0) |

## 6. Phase 1 — 스키마 · FK · 인덱스 (신규)

**파일**: `backend/tests/integration/postgres/test_task_lifecycle_v2_schema_postgres.py` — 5건, 전부 통과(`v2-schema-01.log`, rc 0).
근거는 **살아 있는 PostgreSQL 의 카탈로그**다. 모델 선언이나 `create_all` 성공은 근거로 쓰지 않았다.

| 테스트 | 무엇을 확인했나 |
|---|---|
| `test_postgres_w2_additive_columns_and_tables_stand_and_need_no_human_decision` | `work_requests.parent_task_id`·`supersedes_request_id`, `tasks.cancel_reason`·`started_at`·`completed_at`·`reopened_at` 이 **실제로 있고 전부 `is_nullable=YES`**. `task_proposals`·`work_request_list_entries` 표 존재. `schema_sync.plan()` 의 `statements` 가 비었고, **이번에 더한 이름이 `manual` 에 없다**(O-25). `manual` 전체가 비기를 기대하지 않는다 |
| `test_postgres_w2_new_foreign_keys_are_valid_and_refuse_a_row_that_points_nowhere` | FK 4개(`work_requests.parent_task_id`→`tasks` / `.supersedes_request_id`→`work_requests` / `task_proposals.task_id`→`tasks` / `work_request_list_entries.work_request_id`→`work_requests`)가 `pg_constraint` 에 **있고 `convalidated`**. `use_alter` 이름 `fk_work_requests_parent_task_id` 가 그대로 선다. **의미 있는 거절 3건**: 없는 상위를 가리키는 하위 요청·없는 이전 요청을 가리키는 재요청·없는 업무에 붙는 제안이 모두 `ForeignKeyViolation`. 제대로 가리키는 행은 서는 것까지 함께 확인해 거절이 다른 이유가 아님을 못 박았다 |
| `test_postgres_w2_partial_unique_indexes_refuse_the_second_row_that_matters` | `uq_task_assignments_active`·`uq_task_proposals_pending_kind` 가 `indisvalid`·`indisready`·`UNIQUE … WHERE`. **두 번째 `active` 는 `UniqueViolation`**, 그러나 **`pending` 은 `active` 옆에 선다**(V-18). 같은 종류의 두 번째 `pending` 제안은 거절, **다른 종류는 함께 서고** 답이 끝난 제안은 다음 회차를 막지 않는다. `uq_work_request_list_entry` 의 두 번째 정리도 거절 |
| `test_postgres_w2_a_dropped_index_on_an_existing_table_needs_the_manual_sql_not_schema_sync` | **O-24 인위 재현**: `ix_work_requests_parent_task_id`·`ix_work_requests_supersedes_request_id` 를 `DROP INDEX` → `schema_sync.apply()` 를 돌려도 **돌아오지 않는다**(그 이름이 발행 statement 에도 없다) → `2026-09-17-w2-indexes.sql`(비-CONCURRENTLY)을 **트랜잭션 안에서** 적용하면 선다 → **한 번 더 적용해도 실패하지 않는다**(`IF NOT EXISTS`) → `pg_index` 가 `indisvalid`·`indisready` |
| `test_postgres_w2_the_concurrent_index_file_matches_and_cannot_run_inside_a_transaction` | 두 파일의 **인덱스 정의가 같다**(`CONCURRENTLY` 한 낱말을 뺀 글자까지 동일). 트랜잭션 **안에서는** PostgreSQL 이 `ActiveSqlTransaction` 으로 거절하고 인덱스는 생기지 않는다. **autocommit 에서는 서고**, 재적용해도 실패하지 않으며, `indisvalid` 다. 회복 절차가 쓰는 「INVALID 인덱스 찾기」 조회가 실제로 답을 내고 **빈 목록**이다 |

- **SQL 두 파일은 고치지 않았다.** 적용·검증만 했고 정의가 어긋나는 자리는 없었다.
- **격리 검증을 운영 적용으로 쓰지 않는다** — 운영 적용(Rollout ③-b)은 사람이 `.concurrent.sql` 로 트랜잭션 밖에서 한다.

## 7. 최종 `make test-postgres` — 전체 새 코드 결과

> 기준선 65 pass 를 재사용하지 않는다. 아래는 **이번 코드 상태에서 전체를 1회** 돌린 실제 결과다.

```
make test-postgres \
  DATABASE_URL=postgresql+psycopg://ax:ax@localhost:54329/ax_demo \
  POSTGRES_TEST_URL=postgresql+psycopg://ax:ax@localhost:54329/ax_test_v2_pg
→ cd backend && AX_POSTGRES_TEST_URL="postgresql+psycopg://ax:ax@localhost:54329/ax_test_v2_pg" uv run pytest -m integration
collected 1429 items / 1352 deselected / 77 selected
========= 77 passed, 1352 deselected, 11 warnings in 293.53s (0:04:53) =========
```

| 항목 | 값 |
|---|---|
| **실제 rc** | **0** |
| 선택된 시험 | **77** (진단 시점 65 + 신규 12) |
| 결과 | **77 passed · 0 failed · 0 skipped** |
| 소요 | 293.53s |
| 로그 | `/tmp/v2-pg-logs/final-full-01.log` · rc 는 `/tmp/v2-pg-logs/final-full-01.exit` |

- 이유 없는 반복 실행은 하지 않았다. 소유 범위 전체 실행은 **진단 1회 + 최종 1회**뿐이고, 그 사이는 전부 `PYTEST_ADDOPTS` 의 `-k` 로 좁힌 실행이다.
- 남은 경고 11건은 전부 `HTTP_422_UNPROCESSABLE_ENTITY` deprecation 과 `anyio.abc.BlockingPortal` alias 로, **이번 변경과 무관한 기존 경고**다.
- root `make verify` 는 코디 소유다. 브라우저 E2E 는 실행하지 않았다.

## 8. 변경한 파일

| 파일 | 성격 |
|---|---|
| `backend/tests/integration/postgres/test_postgres_integration.py` | **수정** — 위 §3 의 두 단언을 v2 계약으로 교체(+docstring 1) |
| `backend/tests/integration/postgres/test_task_lifecycle_v2_postgres.py` | **신규** — C1·C2 실제 경합 7건 |
| `backend/tests/integration/postgres/test_task_lifecycle_v2_schema_postgres.py` | **신규** — 스키마·FK·부분 유일·인덱스 결손 재현 5건 |
| `backend/tests/integration/postgres/v2_pg_support.py` | **신규** — 테스트를 담지 않는 도우미(격리 PG stack + 얇은 REST 감싸개) |

**손대지 않은 것**: 제품 코드 전부 · `backend/tests/conftest.py` · `legacy_acceptance.py` · `Makefile` ·
`backend/migrations/manual/*.sql` 두 파일 · 프런트엔드 · 제품 문서 · PG 디렉터리의 나머지 6파일.

## 9. 미완료·주의점

1. **미정은 미정으로 남았다.** EU-17(수락↔철회 승자 · 상위 취소 뒤 하위 수락), OQ-203(완료 보고 제출의 하위 검사 — **현행 보존**이지 새 정책 확정이 아니다), OQ-206(승격 요청의 완료 승인자)은 **어떤 테스트로도 확정하지 않았다.** 선행·후행 강제와 부모 취소 후 수락 우선순위도 같다.
2. **재전송 영수증의 상태 코드**는 담당 교체 입구(`/api/task-assignments/{id}/accept`)에서 확정하지 않았다 — 원BE 가 영수증 처리를 정정 중인 자리다. 지금 시험이 지키는 것은 **두 번째 effect 가 없다**는 것뿐이다. 정정이 끝나면 그 자리에 코드 단언을 더할 수 있다.
3. **`ax_demo` 는 사용자 스키마 표가 0개**다. 이번 PG fixture 통과와는 다른 사안이고, **배포 직전 실데이터 재확인**은 여전히 필요하다(WORK-002 §Pre-deploy · Rollout ①).
4. **운영 인덱스 적용(Rollout ③-b)은 남아 있다.** 여기서 검증한 것은 격리 판이고, `.concurrent.sql` 의 운영 적용은 **사람이 트랜잭션 밖에서** 한다. 실패 시 INVALID 인덱스를 `DROP INDEX CONCURRENTLY` 하고 다시 시작하는 절차는 파일 머리와 위 §6 마지막 시험이 함께 남긴다.
5. 브라우저 E2E 는 실행하지 않았다(범위 밖).

---

# 부록 A — 담당 교체 재전송 영수증 단언 정정 (2026-09-17, 후속 태스크)

## A.1 무엇이 구멍이었나

§7 의 **77 passed 는 그 시점의 실제 증거로 그대로 둔다.** 다만 그 안의 한 줄이
**계약을 검증하지 못하고 있었다.**

`test_postgres_resending_one_handover_answer_at_once_is_still_one_answer` 의 응답 단언이
`assert all(code in {200, 400, 404, 409, 422} ...)` 였다. 이 목록은 **제품이 내는 어떤 거절도
통과시킨다** — 「같은 답 재전송은 영수증」이라는 SPEC-003 §3 S-16 1 을 증명한 적이 없고,
판단함 경유에서 이미 `[200, 200]` 으로 서 있던 보장(`test_postgres_assignment_decision_replay.py:39`)을
이 입구에서만 **미정으로 되돌린 셈**이었다. 구현이 정하는 자리가 아니다.

**그래서 77 passed 중 이 한 건은 「통과」가 아니라 「묻지 않았다」로 읽어야 한다.** 나머지 76 건의
판정은 그대로다 — 다른 묶음은 재검수하지 않았다.

## A.2 정정한 단언

| 무엇 | 바뀐 뒤 |
|---|---|
| 응답 코드 | `codes == [200, 200]` — **거절 코드를 허용 목록에 넣지 않는다** |
| 같은 사건인가 | 두 영수증의 `assignment_id` 가 서로 같고 **제안 id 와도 같다**. `assignee_id="mina"` · `status="active"` · `task.task_id` 가 둘 다 같다 |
| 회차 | 두 응답의 `task.version` 이 같다 — 재전송이 회차를 한 번 더 올리지 않는다 |
| **권한 보존** | 같은 행에 `jiho` · `minseok` 가 같은 답을 보내면 **여전히 404** 다. 영수증이 열렸다고 남의 답까지 받지 않는다 |
| 원장 (그대로) | 담당 행 **2**(이전·새것) · `active` **1** · `mina` 의 판단 행 **1** |
| 경합 장치 (그대로) | `SqlAlchemyTaskAssignmentRepository.task_by_id(lock=True)` 앞의 barrier — 두 transaction 이 겹친 뒤 첫 잠금이 일어난다. **인위 교착 없음**(잠금을 쥔 채 이벤트를 기다리는 자리가 없다) |

## A.3 실행과 실제 rc — 변경한 한 테스트만

```
PYTEST_ADDOPTS="-q -p no:randomly -k resending_one_handover" make test-postgres \
  DATABASE_URL=postgresql+psycopg://ax:ax@localhost:54329/ax_demo \
  POSTGRES_TEST_URL=postgresql+psycopg://ax:ax@localhost:54329/ax_test_v2_pg
```

| 항목 | 값 |
|---|---|
| 로그 · rc 파일 | `/tmp/v2-pg-logs/receipt-fix-01.log` · `/tmp/v2-pg-logs/receipt-fix-01.exit` |
| **실제 rc** | **2** |
| 결과 | **1 failed** · 1428 deselected (2.89s) |
| 격리 DB | `ax_test_v2_pg`(54329) — `DATABASE_URL`(`ax_demo`)과 다름을 Makefile 가드가 통과. 사용자 DB·스택은 건드리지 않았다 |
| 범위 | **이 한 테스트만.** 전량 재실행 없음, 완료된 다른 14 묶음 재검수 없음 |

§7 의 전체 실행(`final-full-01.log`, rc 0, 77 passed)은 **정정 이전의 증거**다. 위 실행은 그와 별개의
파일에 남겼고 서로 섞지 않았다.

## A.4 제품 결함 — 정확한 응답

```
assert [422, 200] == [200, 200]
진 쪽 본문: {"detail":"task assignment is not awaiting acceptance"}
이긴 쪽 본문: {"assignment_id":"d94b3968-…","…","status":"active", "task":{…}}
```

- **증상**: 정당한 수신자가 같은 담당 행에 같은 답(accept)을 동시에 두 번 보내면 진 쪽이
  **422 거절**을 받는다. 기대는 **200 영수증**이다.
- **원장은 이미 옳다** — 담당 행 2 · `active` 1 · `mina` 의 판단 1건. **빠진 것은 영수증 분기 하나**다.
- **위치**: `modules/work/assignments.py` 의 `_pending_target()` 이 `assignment.status != "pending"` 을
  무조건 `TaskError` 로 올린다. 같은 파일 `cancel()` 은 `status == "cancelled"` 면 현재 투영을 그대로
  돌려주는 **영수증 모양을 이미 갖고 있고**, 요청 축은 `requests.py` 의 `_decision_receipt()` 가
  회차 검사보다 **먼저** 오며, 판단함 경유는 `test_postgres_assignment_decision_replay.py:39` 가
  `[200, 200]` 으로 못 박았다 — **세 자리가 같은데 이 입구만 다르다.**
- **처리**: 제품은 고치지 않았다. 근거·정확한 응답·방향(같은 actor·같은 결정으로 이미 닫힌 행이면
  **현재 읽기 권한을 다시 검사한 뒤** 200 영수증, effect 0)을 원BE 에 전달하고 **실패 테스트를 유지**했다.
  수정 통지가 오면 **이 한 테스트만** 다시 돌린다.

## A.5 이 부록에서 바뀐 파일

| 파일 | 성격 |
|---|---|
| `backend/tests/integration/postgres/test_task_lifecycle_v2_postgres.py` | 수정 — 위 한 테스트의 응답·식별자·권한 단언과 docstring |
| (이 보고서) | 부록 A 추가 |

제품·SQL·공통 fixture·다른 테스트는 **무수정**이다.

## A.6 BE 1차 수정 후 재확인 — **아직 실패** (`receipt-fix-02`)

```
PYTEST_ADDOPTS="-q -p no:randomly -k resending_one_handover" make test-postgres \
  DATABASE_URL=postgresql+psycopg://ax:ax@localhost:54329/ax_demo \
  POSTGRES_TEST_URL=postgresql+psycopg://ax:ax@localhost:54329/ax_test_v2_pg
```

| 항목 | 값 |
|---|---|
| 로그 · rc 파일 | `/tmp/v2-pg-logs/receipt-fix-02.log` · `.exit` |
| **실제 rc** | **2** |
| 결과 | **1 failed** · 1428 deselected (2.91s) |
| 응답 | `assert [422, 200] == [200, 200]` — 진 쪽 본문 `{"detail":"task assignment is not awaiting acceptance"}` (`receipt-fix-01` 과 글자까지 같다) |

**수정은 들어왔지만 동시 재전송을 잡지 못한다.** `modules/work/assignments.py` 의 `accept()`·`decline()` 이
`_pending_target` 보다 **먼저** `_answer_receipt()` 를 부르도록 바뀌었다. 그러나 `_answer_receipt()` 는
`self._repository.assignment(assignment_id)` 를 **잠금 없이** 읽는다 —

1. 같은 순간의 두 요청이 **둘 다 아직 `pending` 인 행**을 본다 → 둘 다 `None` → 영수증 분기를 빠져나간다.
2. 둘 다 `_pending_target` 으로 내려가 Task 행 잠금에 걸린다.
3. 진 쪽이 풀려나 `assignment(lock=True)` 로 다시 읽으면 그때는 이미 `active` →
   `status != "pending"` 분기에서 `TaskError` → **422**.

즉 **영수증 재검사가 잠금 앞에만 있고 잠금 뒤에 없다.** 순차 재전송은 200 이지만 **동시** 재전송은 아니다.
판단함 경유가 이 자리를 어떻게 넘겼는지는 그 테스트 이름에 그대로 있다 —
`test_assignment_simultaneous_same_decision_replays_after_the_owner_lock`(**after the owner lock**), 그쪽은 `[200, 200]` 이다.

**처리**: 제품은 고치지 않았다. 위 진단과 방향(잠금을 잡고 다시 읽은 뒤 「같은 사람의 같은 답」이면
`TaskError` 대신 영수증을 한 번 더 태운다 · effect 0 · 현재 읽기 권한 재검사 유지 · 다른 답·다른 사람은
지금처럼 거절)을 원BE·코디에 전달하고 **실패 테스트를 유지**했다. 전체 재실행은 하지 않았다.

## A.7 BE 2차 수정(잠금 뒤 재판정) 후 재확인 — **통과** (`receipt-fix-03`)

```
PYTEST_ADDOPTS="-q -p no:randomly -k test_postgres_resending_one_handover_answer_at_once_is_still_one_answer" \
make test-postgres \
  DATABASE_URL=postgresql+psycopg://ax:ax@localhost:54329/ax_demo \
  POSTGRES_TEST_URL=postgresql+psycopg://ax:ax@localhost:54329/ax_test_v2_pg
```

| 항목 | 값 |
|---|---|
| 로그 · rc 파일 | `/tmp/v2-pg-logs/receipt-fix-03.log` · `.exit` |
| **실제 rc** | **0** |
| 결과 | **1 passed** · 1428 deselected (2.96s) |

**무엇이 확인됐나** — 정당한 수신자가 같은 담당 교체 행에 같은 답을 **동시에** 두 번 보냈을 때:

| 계약 | 확인 |
|---|---|
| 같은 답 응답 코드 | **`[200, 200]`** — 거절 코드를 허용 목록에 넣지 않은 단언이다 |
| 같은 사건인가 | 두 영수증의 `assignment_id` 가 서로 같고 **제안 id 와도 같다** · `assignee_id="mina"` · `status="active"` · `task.task_id` 동일 |
| 회차 | 두 응답의 `task.version` 이 같다 — 재전송이 회차를 한 번 더 올리지 않는다 |
| **권한 보존** | 같은 행에 `jiho` · `minseok` 의 같은 호출은 **여전히 404** |
| 원장 불변 | 담당 행 **2**(이전·새것) · `active` **1** · `mina` 의 판단 행 **1** |
| 경합 장치 | `task_by_id(lock=True)` 앞의 barrier 유지 — 두 transaction 이 겹친 뒤 첫 잠금이 일어난다. **인위 교착 없음** |

**제품 쪽 변경(원BE 소유, 내가 고치지 않았다)**: `_pending_target` 이 `assignment(assignment_id, lock=True)`
로 다시 읽은 **뒤에** 「같은 사람의 같은 답으로 이미 닫힌 행」이면 `None` 을 돌려 영수증으로 되돌린다
(`assignments.py:339-345`). 잠금 **앞**의 `_answer_receipt` 만으로는 동시 재전송이 빠져나갔다.

## A.8 정정 태스크 종료 상태

| 실행 | rc | 결과 | 성격 |
|---|---|---|---|
| `final-full-01` (§7) | 0 | 77 passed | **정정 이전** 전체 증거. 그대로 남긴다 — 단, 그 안의 이 한 건은 §A.1 대로 「묻지 않았다」로 읽는다 |
| `receipt-fix-01` | 2 | 1 failed `[422, 200]` | 정정 직후 — 구멍 확인 |
| `receipt-fix-02` | 2 | 1 failed `[422, 200]` | BE 1차(잠금 앞 영수증) 후 — 동시 재전송은 여전히 빠져나감 |
| `receipt-fix-03` | **0** | **1 passed** | BE 2차(잠금 뒤 재판정) 후 — **계약 충족** |

전체 재실행은 하지 않았다. 완료된 다른 14 묶음은 재검수하지 않았다. 제품·SQL·공통 fixture·다른
테스트는 무수정이고 커밋·push·PR 도 없다.

---

# 부록 B — 통합 리뷰 E-1: 최신 트리 전체 PG 재실행 (2026-09-17)

`final-full-01` 이후 `assignments.py` · `actions.py` · `command_contracts.py` 와 PG 테스트가 바뀌어,
같은 격리 DB 에서 **최신 트리 전체**를 다시 돌렸다.

## B.1 1차 — `final-full-02` (실패)

| 항목 | 값 |
|---|---|
| pid · 로그 · rc 파일 | `/tmp/v2-pg-logs/final-full-02.pid`(76225) · `.log` · `.exit` |
| **실제 rc** | **2** |
| 결과 | **1 failed · 76 passed** · 1352 deselected (143.35s) |
| 실패 | `test_postgres_integration.py::test_postgres_will_not_finish_work_while_a_part_of_it_is_still_open` — `assert 409 in {201, 422}` |

**판정: W1 기대값 마이그레이션 누락.** 409 를 낸 쪽은 `outcomes[0]`, 즉 **하위 붙이기**
(`POST /api/tasks` with `parent_task_id`)이고 그 코드는 **`WORK_PARENT_CLOSED`** 다 —
`TaskParentClosed` 가 일반 `TaskError`(422) 버킷을 떠나 SPEC-003 §4 Case Matrix 의 409 줄
(`spec-003 :765`)로 옮겨졌다(`http.py` 의 「요청 자체는 말이 되는데 **지금 그 자원의 상태가 그 명령을
받지 않는다**」 묶음). W1 테스트는 옛 422 를 기대하고 있었다.

## B.2 정정 — 넓히지 않고 **좁혔다**

`assert outcomes[0].status_code in {201, 422}` 한 줄을, 붙이기가 진 경우에 한해 다음으로 바꿨다:

| 무엇 | 단언 |
|---|---|
| 코드 | `== 409` (집합이 아니다) |
| **이유** | 본문에 `이미 끝난 업무에는 하위 업무를 추가할 수 없습니다` — 코드만 넓히면 회차 불일치·권한 거절도 이 자리를 지나간다 |
| 최종 상태 | 진 명령이 **아무것도 남기지 않는다**: `view["children"] == []` · `view["child_progress"]["total"] == 0` |

붙이기가 이긴 분기(201)와 상위 완료가 진 분기는 **손대지 않았다**. 제품은 고치지 않았다.

- 좁힌 실행: `PYTEST_ADDOPTS="-k test_postgres_will_not_finish_work_while_a_part_of_it_is_still_open"` →
  `/tmp/v2-pg-logs/parent-closed-01.log` · `.exit`, **rc 0 · 1 passed**.

## B.3 2차 — `final-full-03` (**green**)

```
make test-postgres \
  DATABASE_URL=postgresql+psycopg://ax:ax@localhost:54329/ax_demo \
  POSTGRES_TEST_URL=postgresql+psycopg://ax:ax@localhost:54329/ax_test_v2_pg
```

| 항목 | 값 |
|---|---|
| pid · 로그 · rc 파일 | `/tmp/v2-pg-logs/final-full-03.pid`(78290) · `.log` · `.exit` |
| **실제 rc** | **0** |
| 결과 | **77 passed · 0 failed · 0 skipped** · 1352 deselected (140.56s) |
| 격리 DB | `ax_test_v2_pg`(54329) — `DATABASE_URL`(`ax_demo`)과 다름을 Makefile 가드가 통과. 사용자 DB·스택 무조작 |

## B.4 실행 이력 — 무엇이 어느 시점의 증거인가

| 실행 | rc | 결과 | 시점 |
|---|---|---|---|
| `final-full-01` | 0 | 77 passed | 영수증 정정 **이전** (부록 A.1 의 단서 포함) |
| `receipt-fix-01/02` | 2 / 2 | 각 1 failed | 영수증 구멍 · BE 1차 후 |
| `receipt-fix-03` | 0 | 1 passed | BE 2차(잠금 뒤 재판정) 후 |
| `final-full-02` | **2** | 1 failed · 76 passed | **최신 트리 1차** — W1 기대값 누락 노출 |
| `parent-closed-01` | 0 | 1 passed | 기대값 정정 직후, 좁힌 실행 |
| **`final-full-03`** | **0** | **77 passed** | **최신 트리 최종** |

## B.5 이 부록에서 바뀐 파일

`backend/tests/integration/postgres/test_postgres_integration.py` 한 곳(위 한 줄 → 네 줄)과 이 보고서뿐이다.
제품·SQL·공통 fixture·다른 테스트는 무수정이고 커밋·push·PR 도 없다.
