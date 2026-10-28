# WORK-005 WP-BE1 · WP-BE2 결과 보고 (backend r1)

## 상태: done

워크트리 `cc-prototype/overall-board` (branch `kknaksss/overall-board`) · 커밋 · push 없음. `procedure/front/` 는 손대지 않음(frontend 워커 변경은 그대로).

## 수행 — 파일 · 모듈

### WP-BE1 「방 배정」 거르기
- `app/domain/rules.py` — 모듈 함수 `is_room_task(p)` = `kind == "etc"` 이고 `room_kos_id` 있음(`kos/sync.py` `_room_task` 와 같은 뜻 · ETCETERA + room). `Rules.items()` 가 이걸 뺀다(한 곳). `procedures()`(kind=procedure 만)·`canCall`·`all_done`·`payment_required` 는 원래 그대로라 결과 변화 없음
- `service/actions.py` `home()` — 바꾸지 않음(취소 대상은 계속 `visit.open_task_seqs` 에서 고름). 호출 전 방 넣기(`visit.room_id`)도 바꾸지 않음
- `service/fake_board.py` — etc 예시 「방 배정」 → 「시트팩」(지어낸 값)
- `repository/db.py` — `procedure.kind` 열 주석만 고침

### WP-BE2 드래그 순서 저장
- `repository/db.py` `SCHEMA` — `CREATE TABLE IF NOT EXISTS board_order (day PK, visit_ids json, updated_at, updated_by, event_id)`. ALTER · MIGRATIONS 추가 없음
- `domain/clock.py` — `kst_day(now)` (KST `YYYY-MM-DD`)
- `repository/repo.py` — `Tx.board_order(day)` · `Tx.put_board_order(...)`(INSERT OR REPLACE = 마지막 쓰기가 이긴다) · `Repository.world_and_order(day)`(스냅샷용 읽기 트랜잭션 하나)
- `service/actions.py` — `ActionService.board_order(actor, visit_ids)`: 같은 id 두 번이면 400 `invalid_request` → 한 트랜잭션에서 지금 카드 중 귀가 대기 아닌 것만 남기고(없는 id · 사라진 카드 · 방 없음 · 귀가 대기는 오류 없이 뺌) → `event_log(board_order, visit_id=NULL, payload {day, visitIds})` 1줄 + `board_order` 오늘 행 통째로 바꿈 · `kos_op` 0줄 → `on_change`(SSE 발행)
- `service/board_service.py` — `cards.sort` 를 §5.12 로 바꿈: ① 오늘 목록에 있는 귀가 대기 아닌 카드(목록 자리 순) → ② 목록 밖(입실 `room_assigned_at` 순 · 같으면 visit id) → ③ 귀가 대기(`flow_step_at` 순). 다음 날(KST)은 새 키라 순서 없음
- `schemas/actions.py` — `BoardOrderRequest{visitIds: list[StrictInt]}`(extra=forbid) · `BoardOrderResponse{ok, visitIds}`
- `api/board.py` — `PUT /api/board/order`(Bearer · `require_real_board` → 403 `fake_board` · 역할 검사 없음 = 세 역할 모두)
- `main.py` — **CORS `allow_methods` 에 `PUT` 추가**(없으면 브라우저 preflight 가 막힘 — 브리프 파일 목록에 없던 것이지만 `procedure/back/` 안)

### 시험
- 새 `tests/test_order.py`(26)
- `tests/test_rules.py` +3, `tests/test_e2e3_home.py` +1, `tests/test_stream.py` +1, `tests/test_auth_roles.py` 역할 행렬에 PUT 줄 추가
- 옛 계약을 단언하던 기존 시험 고침: `test_kos_sync.py`(「방 배정」이 procedures 에 보인다 → 안 보이고 DB 엔 etc · room 으로 저장됨) · `test_e2e1_room.py::test_etc_items_shown_but_not_actionable`(방 없는 「시트팩」 etc 로 바꿈)

## 검증 — 명령 · 수치

| 단계 | 명령 | 결과 |
|---|---|---|
| WP-BE1 | `uv run ruff check . && uv run pytest -q tests/test_rules.py tests/test_e2e3_home.py tests/test_contract.py` | ruff 통과 · **25 passed** |
| WP-BE2 | `uv run ruff check . && uv run pytest -q tests/test_order.py tests/test_stream.py tests/test_auth_roles.py tests/test_contract.py` | ruff 통과 · **49 passed** |
| 전체 | `cd procedure/back && uv run ruff check . && uv run pytest -q` | ruff 통과 · **155 passed** |

기능 폴더 밖 import 0(서드파티 · `app` · `tests` 만). 사용자 포트 · 프로세스는 건드리지 않음(TestClient 만).

### WP-BE1 완료 조건
- ① 방 있는 etc 가 `procedures[]` 에 없음 — 통과 (`test_rules::test_room_task_not_in_snapshot` — 방 있는 etc 2개(OQ-511) 둘 다 빠짐 · `test_kos_sync::test_schedule_upsert_card_and_body`)
- ② 방 없는 etc 는 있음 · 읽기 전용(`pickable/canStart/canFinish` false) — 통과 (`test_rules::test_roomless_etc_stays_read_only` · `test_e2e1_room::test_etc_items_shown_but_not_actionable`)
- ③ [귀가 대기] `cancel-flow-tasks` `sequences` 에 「방 배정」 sequence 그대로 — 통과 (`test_e2e3_home::test_room_task_hidden_but_still_canceled` → `[3, 4]` · 기존 `test_home_cancels_open_tasks_then_flow_step` → `[3]`)
- ④ `canCall` · `all_done` · `paymentRequired` 변화 없음 — 통과 (`test_rules::test_room_task_filter_keeps_rules` — 「방 배정」 있는 카드와 없는 카드가 시작 전 · 전부 완료 뒤 같은 값)

### WP-BE2 완료 조건 (SPEC-003 §9 「0.4.0 더함」)
- 저장 — 통과 (`test_save_and_snapshot_follows`)
- 거르기(없는 id · 귀가 대기 · 사라진 카드 · 방 없는 visit) — 통과 (`test_filters_unknown_home_and_gone_cards`)
- 400 형식(객체 아님 · `visitIds` 없음 · 그 밖 필드 · 배열 아님 · null) — 통과 (`test_bad_format_400` 8 케이스, 저장 · 발행 0)
- StrictInt `"3"` · `3.0` · `true` → 400 — 통과 (같은 파라미터 시험)
- 같은 id 두 번 → 400 — 통과 (`test_duplicate_id_400` · 없는 id 의 중복도 400)
- 마지막 쓰기 — 통과 (`test_last_write_wins` — 행 1개 · 이벤트 2개 · 뒤 목록에 없는 카드는 맨 뒤)
- `event_log` 1줄 · `kos_op` 0줄 — 통과 (`test_event_log_one_row_and_no_kos_op` — actor · `visit_id` NULL · payload `{day, visitIds}` · `event_id` 연결)
- 저장 뒤 SSE 1개 — 통과 (`test_publishes_one_board_after_save` — 다음 프레임 1개 · 그 뒤 없음 · 새 순서 · `test_stream::test_board_order_publishes_board` · 400 은 발행 0)
- 401 — 통과 (`test_requires_login` · 잘못된 본문이어도 401 먼저)
- 403 `fake_board` — 통과 (`test_fake_board_403` · 401 이 403 보다 먼저)
- 역할 세 개 모두 200 — 통과 (`test_auth_roles::test_role_matrix[admin/doctor/nurse]` · actor = 로그인 아이디)
- 정렬(목록 → 목록 밖 입실순 → 귀가 대기 시각 순 · 다음 날 순서 없음) — 통과 (`test_sort_list_then_rest_by_in_at_then_home` · `test_in_at_tie_breaks_by_visit_id` · `test_next_day_has_no_order` · `test_kst_day_boundary`)
- 옛 스키마 DB — 통과 (`test_order.py::test_old_schema_db_keeps_rows` — 지금 `SCHEMA` 에서 `board_order` 문을 뺀 0.3.0 스키마로 만든 파일 + visit 행 1 → `Database()` 초기화 → `board_order` 5열 생김 · visit 행 남음)
- 경로 수 17(§7.4) — 통과 (`test_route_count_17` — openapi HTTP 16 + WS `/api/interpret` 1)
- CORS PUT preflight — 통과 (`test_cors_allows_put`)

## 계약 대조 — WORK-005 계약 고정점 · SPEC-003 0.4.2

| 항목 | 결과 |
|---|---|
| `PUT /api/board/order` 본문 `{visitIds:[StrictInt]}` · 빈 배열 허용 · 응답 `{ok:true, visitIds}` · 400 `invalid_request` · 401 · 403 `fake_board` · 없는 id 거름 (§7.3) | 같음 |
| 스냅샷 `cards[]` 배열 순서 = 화면 순서 · 새 필드 없음 (§7.2 · §5.12) | 같음(`schemas/board.py` 안 바꿈) |
| `procedures[]` 에 방 있는 etc 없음 · 필드 모양 그대로 (§5.1 · §7.2) | 같음 |
| `cards[].kos` 그대로 (§7.2) | 같음(안 건드림) |
| SSE 순서 저장 직후 `board` 1개 (§7.5 ①) | 같음 |
| `board_order` 표 열 · `CREATE TABLE IF NOT EXISTS` · ALTER 없음 (§3.2) | 같음 |
| `event_log.type = board_order` · payload `{day, visitIds}` · `visit_id` 비움 (§3.2) | 같음 |
| 역할 admin · doctor · nurse 모두 (SPEC-004 §3.4) | 같음 |
| back `procedures[]` 순서(완료 → 진행 → 대기)는 그대로 (§5.9) | 같음(`ordered_procedures` 안 바꿈) |

## 이슈 · 코디가 확인할 것

1. **CORS** — `main.py` `allow_methods` 에 `PUT` 을 더했다. WORK 대상 파일 목록엔 없었지만 없으면 웹(3700 → 8700) PUT 이 preflight 에서 막힌다. 배포 ingress 가 따로 CORS 를 거르면 그쪽도 PUT 허용인지 WP-E2E 에서 확인 필요
2. **기존 시험 2개 수정** — `test_kos_sync.py` · `test_e2e1_room.py` 는 브리프의 대상 시험 목록 밖이지만 옛 계약(「방 배정」이 보인다)을 단언하고 있어 새 계약에 맞게 고쳤다(allowed_paths `procedure/back/` 안)
3. 「다른 날」 거르기 = 지금 카드(`present` · 오늘 조회분 · 날짜 바뀌면 `rollover` 가 내림) 기준. 따로 날짜 비교는 하지 않는다 — 카드 판정과 같은 규칙
4. 같은 id 두 번 검사는 service 에서(BadRequest `invalid_request`) — HTTP 밖에서 불러도 같은 규칙
5. 전날 `board_order` 행은 지우지 않는다(OQ-525 기본값). `.env.example` 안 바꿈(새 env 없음)

---

# WP-BE3(방 판정 · 2026-10-25) 결과 보고

## 상태: done

## 수행
- `app/kos/sync.py` — `_room_task` → **`_card_room_task`**: 카드 방 = **type 무관** `room` 있는 작업 중 `roomAssignedDateTimeUtc` 가 가장 늦은 것. 입실 시각(`room_assigned_at`) = 그 작업 값
  - **기본값(내가 정함)**: 배정 시각이 같거나 없으면 ① ETCETERA 먼저 ② 그다음 큰 `sequence`. 작업 상태는 보지 않는다(지금처럼 — 취소된 「방 배정」의 방도 카드 방이라 [귀가 대기] 뒤에도 방 그대로 · `test_e2e3_home` 그대로 통과)
- `app/domain/rules.py` — `is_room_task`(방 있는 ETCETERA = 「방 배정」 줄 빼기)는 **그대로**, docstring 만 「카드 방 판정과 다른 판정」으로 고침
- `tests/test_kos_sync.py` +5

## 검증
`cd procedure/back && uv run ruff check . && uv run pytest -q` → ruff 통과 · **160 passed**(전 155 + 5)

| 조건 | 시험 | 결과 |
|---|---|---|
| ① PROCEDURE 에만 방 → 카드 방 있음 · 입실 = 그 작업 값 | `test_room_on_procedure_only_makes_card` | 통과 |
| ② ETCETERA 방 + PROCEDURE 방 → 가장 늦은 배정 | `test_room_latest_across_types`(양쪽 방향) · 기존 `test_room_latest_assigned` | 통과 |
| (기본값) 시각 없음/같음 → ETCETERA 먼저 | `test_room_tie_prefers_etcetera` | 통과 |
| ③ 방 없음 → 카드 없음 | `test_no_room_anywhere_no_card` | 통과 |
| ④ 「방 배정」 줄 빼기 그대로 · 시술 줄은 방이 붙어도 남음 | `test_room_task_row_still_hidden` · WP-BE1 시험 전부 | 통과 |

## 코디가 확인할 것
1. **입실 시각이 뒤로 밀릴 수 있음(실 KOS 확인 필요)** — ccc [의사 호출] 이 `change-tasks-room` 으로 카드 방을 시술 작업에 넣는다. 그때 KOS 가 그 시술 작업의 `roomAssignedDateTimeUtc` 를 **호출 시각으로 새로 찍으면**, 방은 같지만 「가장 늦은 배정」 = 그 작업이 되어 카드 `inAt` 이 호출 시각으로 바뀌고 목록 밖 카드 정렬(입실순)도 움직인다. 가짜 KOS 로는 확인 불가 — E2E §9 #3 뒤 카드 입실 시각이 그대로인지 봐 달라. 바뀌면 「입실 = 같은 방 작업 중 가장 이른 배정」 같은 규칙이 필요(계약 결정이라 내가 정하지 않음)
2. 문서(SPEC-003 0.4.3 · WORK-005 WP-BE3) 대조는 코디/planner 몫 — 위 기본값(동률 → ETCETERA → 큰 sequence)을 문서에 적어 달라

---

# 규칙 하나(one-rule · 2026-10-25) 결과 보고

no-kind 지시는 폐기됐고, 반쯤 고친 상태에서 one-rule 로 마무리했다(WP-BE1 「방 배정」 거르기는 되돌림).

## 상태: done

## 규칙 (코드 정본 = `app/domain/rules.py` `Rules.is_room_task` 한 곳)
- KOS 작업은 **type(PROCEDURE · ETCETERA) 무관 전부 같은 시술**. 스냅샷 `procedures[]` = 작업 전부(CANCELED 만 뺌)
- 예외 하나 = **「방 배정」 = 방 붙은 ETCETERA 이면서 ccc 가 한 번도 호출하지 않은 작업**(`doctor_call_item` 에 없음) — 코디 답 A
  - 근거: 「방 배정」은 호출 대상이 아니니, 호출된 적이 있으면 「방 배정」일 수 없다. 이게 없으면 시트팩에 [의사 호출]을 하는 순간 호출 전 방 넣기(`change-tasks-room` · 로컬 `room_kos_id`)로 방이 붙어 시트팩이 「방 배정」으로 바뀌어 버린다(시험으로 재현했음). KOS 쓰기는 그대로
- 「방 배정」은 스냅샷에 싣고 `isRoomTask: true`(front 가 숨김). 판정에서 뺀다: `pickable` · `canStart` · `canFinish` false · 호출 · 시작 · 종료 404 · `procedures()`(`all_done` · `payment_required` · `canCall` · `need` · 호출 받을 시술 · 원장 바쁨)에 안 듦 → 「전부 완료」가 「방 배정」을 기다리지 않음
- [귀가 대기] KOS 취소 대상 = **아직 안 끝난 「방 배정」만**(카드 작업 중 `is_room_task` · 완료 아님). 다른 작업은 전부 완료여야 귀가 대기라 취소할 것이 없다
  - **동작이 바뀐 곳**: 예전엔 `open_task_seqs`(KOS 미완료 작업 전부 · 저장 안 한 다른 type 포함) 중 시술 아닌 것을 취소했다. 이제는 카드에 있는 안 끝난 「방 배정」만 취소한다 → PROCEDURE · ETCETERA 가 아닌 type 의 열린 작업은 더는 취소하지 않는다(지금 데이터엔 없음). `open_task_seqs` 는 저장은 계속하지만 취소 계산엔 쓰지 않는다
- KOS 쓰기(방 넣기 · 담당자 · 호출 · 수락 · 완료)는 type 으로 거르는 곳이 없다(sequence 로만 보냄) — 시트팩 호출 · 완료가 같은 API 로 가는 것을 시험으로 확인. 단 실 KOS 가 ETCETERA 에 `call-tasks-doctors` · `change-tasks-complete` 를 받아 주는지는 가짜 KOS 로 확인 못 함 → E2E 에서 확인

## 수행 (`procedure/back/`)
- `app/domain/rules.py` — `Rules.is_room_task`(호출 이력 `_called` 포함) · `items` = CANCELED 만 뺌 · `procedures()` = 「방 배정」 뺀 전부 · `pickable` · `start_block` 이 type 대신 「방 배정」만 봄
- `app/service/actions.py` — `_procedure` 404 = 「방 배정」만 · `home` 취소 = 안 끝난 「방 배정」
- `app/service/board_service.py` — `isRoomTask` · `canFinish`
- `app/schemas/board.py` — `Procedure.isRoomTask: bool` 추가(그 밖 모양 그대로 · `kind` 유지)
- `app/service/fake_board.py` — 카드 101 에 시트팩(일반 시술 줄)과 「방 배정」(`isRoomTask: true`) 예시 하나씩
- 주석만: `domain/models.py` · `repository/db.py` · `domain/kos_ops.py`
- 시험: `tests/test_rules.py`(옛 WP-BE1 시험 4개를 새 규칙으로 바꾸고 +3) · `tests/test_e2e3_home.py`(새로 씀) · `tests/test_e2e1_room.py`(`test_etc_items_are_procedures`) · `tests/test_kos_sync.py`(2개 고침)

## 검증
`cd procedure/back && uv run ruff check . && uv run pytest -q` → ruff 통과 · **162 passed**

| 조건 | 시험 | 결과 |
|---|---|---|
| ① 시트팩이 일반 시술처럼 체크 · 호출 · 시작 · 종료 · 전부 완료 · 수납에 든다 | `test_rules::test_roomless_etc_is_procedure` · `test_sheet_pack_payment_counts` · `test_e2e1_room::test_etc_items_are_procedures`(KOS 쓰기 sequences [4]) | 통과 |
| ② 시트팩이 안 끝났으면 [귀가 대기] 409 | `test_e2e3_home::test_sheet_pack_blocks_home_and_cancel_is_room_task_only` | 통과 |
| ③ 「방 배정」이 실리고 `isRoomTask=true` · 판정 · 조작에서 빠짐 | `test_rules::test_room_task_in_snapshot_flagged` · `test_room_task_excluded_from_rules` · `test_can_call_needs_pickable_procedure` · `test_kos_sync` 2개 | 통과 |
| ④ [귀가 대기] 취소 sequences = 「방 배정」만 | `test_e2e3_home::test_home_cancels_room_task_then_flow_step`([3]) · 위 ② 시험([3]) · `test_home_without_open_room_task_skips_cancel` | 통과 |
| 시트팩을 호출해 방이 붙어도 `isRoomTask=false` · 판정 그대로 | `test_rules::test_called_sheet_pack_with_room_is_not_room_task`(취소 = [8] 「방 배정」만) | 통과 |
| ⑤ 드래그 순서 · 방 판정(type 무관) 시험 | `test_order.py` 26 · `test_kos_sync` 방 판정 5 | 통과(안 바꿈) |

## 코디가 확인할 것
1. front 는 `isRoomTask` 줄만 숨긴다(front 몫). 앱(`procedure/app/`)은 `isRoomTask` 를 모르니 「방 배정」을 `etc` 로 받는다 — 지금 앱은 `etc` 를 그리지 않아 화면은 그대로지만, 시트팩 등도 `etc` 라 앱에서 안 보인다(이번 판 범위 밖 · 사용자 확인 필요)
2. 판정에서 빠지는 「방 배정」 = 아직 호출 안 된 것뿐이라, 예전 DB 에 이미 호출된 ETCETERA 가 있으면 그건 일반 시술로 보인다(의도대로)
3. 문서(SPEC)는 코디가 맞출 몫 — 위 「규칙」 절 정의(호출 이력 포함)를 그대로 옮겨 달라

---

# 되돌리기(WORK-006 WP-BE · SPEC-003 0.5.1 §5.13) 결과 보고

## 상태: done (커밋 안 함)

## 수행 (`procedure/back/`)
- ⑤ 먼저 — `schemas/board.py` `Procedure.canUndoStart` · `canUndoFinish: bool`(기본 `false` — FE 가짜 보드 예시가 빠뜨려도 응답 모델 통과) · `service/board_service.py` `_proc` 가 아래 판정으로 채움
- ① `domain/kos_ops.py` `uncomplete_op` — `PATH_COMPLETE` · `{scheduleId, sequences:[seq], complete:false}` · expect `{tasks:[seq], statusNot:"DONE"}`
- ② `domain/rules.py` 한 곳 — `undo_start_block`(귀가 대기 → `visit_home` · `doing` 아님 · 「방 배정」 → `procedure_not_doing`) · `undo_finish_block`(`visit_home` → `done` 아님 · 「방 배정」 → `procedure_not_done` → ccc `started_at` 없음 → `procedure_not_started`) · `back_to_waiting`(고객 `PROCEDURE` 이고, 그 시술을 뺀 `procedures(v)`(「방 배정」 제외) 중 진행 · 완료 0). 스냅샷 `canUndo*` = 그 block 이 None
- ③ `service/actions.py` `undo_start` · `undo_finish` — 트랜잭션 하나 · `_procedure` 404 그대로(「방 배정」 · 없는 id · 카드 아님) · `event_log` 1줄 · `_done()`(SSE)
  - undo-start: `started_at` · `started_event_id` 비움(호출 · 수락 · 집도의 그대로) · `back_to_waiting` 이면 `update_visit(flow_step=PROCEDURE_WAITING, flow_step_at=now)` + `flow_step_op(PROCEDURE_WAITING)` **항상 1줄**(KOS 값 안 읽음) · payload `{procedureId, startedAt, startedEventId, flowStepChanged}`
  - undo-finish: `completed_at` 비움 · `kos_status = READY` + `uncomplete_op` · 고객 상태 그대로 · payload `{procedureId, completedAt}`
  - `MESSAGES` 두 코드 — `procedure_not_doing` 「진행 중인 시술이 아니에요」 · `procedure_not_done` 「완료된 시술이 아니에요」
- ④ `api/actions.py` — `POST /api/procedures/{id}/undo-start` → `{ok, flowStepChanged}`(`StartResponse` 재사용) · `/undo-finish` → `{ok}` · `require_real_board` 그대로 · 역할 검사 없음(세 역할) · `schemas/actions.py` `CONFLICT_CODES` 두 코드
- ⑥ `kos/ops.py` — `expect_met` 에 `statusNot` · `superseded` 가 `status` · `statusNot` 를 한 묶음(같은 작업 status 필드)으로 봄
- 브리프 파일 목록 밖(같은 `procedure/back/`): `repository/repo.py` `Tx.started_event_id(id)`(도메인 모델에 열이 없어 payload 용으로 읽기만) · `tests/fake_kos.py` `complete:false` → `READY` · 완료 시각 지움(WP-KOS K2 실값)
- `service/fake_board.py` 는 FE 몫(r6 W2)이라 손대지 않음

## 검증
- WP-BE 명령 `uv run ruff check . && uv run pytest -q tests/test_undo.py tests/test_kos_ops.py tests/test_auth_roles.py tests/test_order.py tests/test_contract.py` → ruff 통과 · **69 passed**
- 전체 `uv run ruff check . && uv run pytest -q` → ruff 통과 · **178 passed**(전 162 + 16)

| SPEC-003 §9 「0.5.0 더함」 | 시험 | 결과 |
|---|---|---|
| undo-start `doing` 만 · 호출 · 수락 · 집도의 남음 · [시작] 다시 켜짐 | `test_undo_start_back_to_waiting_with_flow_step` · `test_undo_start_keeps_call_and_accept` | 통과 |
| 진행 · 완료 0 이면 고객 `waiting` + flow-step op 항상 1줄 · 남으면 op 0 | 위 · `test_undo_start_other_doing_or_done_keeps_customer` | 통과 |
| 400 뒤 다음 조회에서 KOS `PROCEDURE_WAITING` 이면 `confirmed`(재전송 없음) | `test_kos_undo_start_same_step_400_then_confirmed` | 통과 |
| 첫 [시작] 직후 되돌리면 앞 `PROCEDURE` op `superseded` | `test_kos_first_start_then_undo_supersedes` | 통과 |
| undo-finish `done` + ccc [시작]만 · `completed_at` 비움 · `READY` · op 1줄 · 고객 그대로 · `canHome` 풀림 | `test_undo_finish` · `test_kos_undo_finish_confirmed_by_status_not` | 통과 |
| 409 네 코드 · 메시지 | `test_conflicts` · `test_messages` | 통과 |
| 404 「방 배정」 · 없는 id | `test_room_task_and_unknown_404` | 통과 |
| 403 `fake_board` · 401 | `test_requires_login_and_fake_board` | 통과 |
| 세 역할 | `test_auth_roles::test_role_matrix[admin/doctor/nurse]`(행렬에 두 조작 더함) | 통과 |
| `event_log` 1줄 · SSE 1개(거절은 0) | `test_one_event_one_publish` · 위 시험들 | 통과 |
| 스냅샷 두 필드(대기 줄 · 귀가 대기 · 「방 배정」 · KOS 만 완료 false) | `test_snapshot_flags` · `test_conflicts` · `test_room_task_and_unknown_404` · `test_contract` | 통과 |
| `statusNot` 확인 | `test_kos_ops::test_expect_met_status_not` | 통과 |
| [종료] → 되돌리기 → [종료] 앞 op 재전송 0 | `test_kos_finish_undo_finish_no_resend`(보낸 complete = [true, false, true]) · `test_kos_ops::test_superseded_status_and_status_not_same_field` | 통과 |
| 경로 19 | `test_order::test_route_count_19` | 통과 |

## 계약 대조 (WORK-006 계약 고정점)
API 두 경로 · 응답 · 409/404/403/401 코드 · 세 역할 · 스냅샷 두 필드만 더함 · 이벤트 두 type · payload · KOS op(undo-finish `complete:false` + `statusNot` / undo-start 고객이 대기로 갈 때만 flow-step) · SSE 1개 — 전부 같음.

## 코디가 확인할 것
1. `canUndo*` 스키마 기본값 `false` — 계약 모양은 같고(늘 실림), 가짜 보드가 키를 빠뜨려도 검증을 통과하게 한 것
2. 실 KOS 확인: [시작] 되돌리기의 flow-step 뒤로 가기 · [종료] 되돌리기의 `complete:false` 는 WP-KOS K2 · K4 로 확인됨. 「되돌리기 → 다시 [종료]」 연속 순서(실 KOS 에서 complete:false 직후 complete:true)는 E2E #26 에서
3. WP-KOS K5(ETCETERA)는 여전히 대기
