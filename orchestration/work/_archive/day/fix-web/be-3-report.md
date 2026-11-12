# fix-web backend 3차 — review-code-3 W1 `consultation(visit_id)` 인덱스 결과 보고

## 상태: done (커밋 · push 안 함 — 1 · 2차 변경 위에 워크트리 변경만)

## 수행 — 파일

| 파일 | 변경 |
|---|---|
| `backend/migrations/versions/20261112_0009_consultation_visit.py` (새) | revision `0009_consultation_visit` · down `0008_chart_room`. upgrade = `op.create_index("ix_consultation_visit_id", "consultation", ["visit_id"], postgresql_where=deleted_at IS NULL)` 하나 · downgrade = 그 인덱스 drop. 이름 · 머리말 · 부분 인덱스 모양은 0006(`ix_event_log_visit_id_type`) 관례 그대로 |
| `backend/day/models/visit.py` | `Consultation.__table_args__` 에 같은 `Index`(부분 · `deleted_at IS NULL`) — 모델과 migration 이 같다(`alembic check` 통과) |
| `backend/day/queries/board.py` | 상담사 조회를 `counselor_rows(visit_ids) -> Select` 함수로 뺌(가드 테스트가 같은 문장을 EXPLAIN 하도록 — 예전 `doctor_changes()` 방식). 조건 · 순서는 2차와 같음 |
| `backend/day/models/task.py` | `EventLog` 인덱스 주석만 고침 — 1차에서 판 읽기의 원장 바꾼 시각 조회를 뺐는데 주석에 남아 있었음(동작 · 스키마 변경 없음) |
| `backend/tests/day/board/test_board_queries.py` | `test_상담사_조회는_consultation_인덱스를_탄다` — `enable_seqscan = off` 에서 `counselor_rows` 의 EXPLAIN 에 `ix_consultation_visit_id` 가 나오는지 |
| `backend/tests/migrations/test_consultation_visit_migration.py` (새) | 0009 가 0008 을 잇는다 · upgrade 는 부분 인덱스 하나만(drop · execute 없음) · downgrade 는 그 인덱스만 지운다 |
| `backend/tests/migrations/test_alembic.py` | `HEAD = "0009_consultation_visit"` |
| `backend/tests/day/test_chat_device_schema.py` | 테스트 스키마 인덱스 목록 단언에 `ix_consultation_visit_id` 추가 |

## 검증

- `uv run ruff check backend` → All checks passed · `ruff format` 통과.
- `DAY_ENV_FILE=/Users/kknaks/git/CENTURION_DAY/deploy/local.env scripts/test.sh -q backend/tests/migrations test_board_queries.py test_chat_device_schema.py test_board_rules.py test_board_api.py` → **131 passed**. 들어 있는 것: 체인 head 하나 · upgrade head · downgrade base → 다시 upgrade · `alembic check` 차이 없음 · 새 가드 테스트 · 2차 상담사 테스트.
- 따로 한 번 손으로 확인 — 로컬 compose postgres 의 **새 임시 스키마 `day_test_be3…`** 에서 `upgrade head`(→ `0009_consultation_visit`) → `downgrade -1`(→ `0008_chart_room`) → `upgrade head`(→ 0009). `pg_indexes` = `CREATE INDEX ix_consultation_visit_id ON …consultation USING btree (visit_id) WHERE (deleted_at IS NULL)`. 끝난 뒤 그 스키마는 `DROP SCHEMA … CASCADE` 로 지움.
- **사용자 `day_dev` 스키마 · day-local api/worker 에는 적용하지 않음.** 테스트는 `scripts/test.sh` 가 `DB_SCHEMA` 를 지우고 테스트 스키마만 씀.

## 주의 · 코디가 확인할 것

- 로컬 `day_dev` 와 dev · prod 서버는 이 migration 이 들어가기 전까지 `0008` 이다. 배포 때 migration 이 돌아야 인덱스가 생긴다(인덱스가 없어도 코드는 그대로 동작하고 느려지기만 한다).
- 큰 표에서 `CREATE INDEX` 는 쓰기를 잠근다. 0006 과 같은 방식(일반 `create_index`)을 따랐고 `CONCURRENTLY` 는 쓰지 않았다. 지금 상담 행 수면 문제없다고 봤다 — 운영 행 수가 많다면 알려 달라.
