# #225 검수 WARN 반영(fix1) 결과 보고

## 상태: done

같은 워크트리 · #225 미커밋 변경 위. 커밋 · push · PR 안 함. W7 · W8 · 「조용히 통과」 5 · 6 은 손대지 않음(사용자 결정 대기).

## W 별 고친 곳

| W | 고친 곳 | 내용 · 증거 |
|---|---|---|
| **W1** enum 라벨 | `backend/tests/day/test_enum_labels.py:28` (새, infra) | upgrade 한 `day_test` 의 `pg_enum` 라벨(타입별 · `enumsortorder` 순)을 모델 `Enum.enums`(ARRAY 안 enum 포함) 28 타입과 비교. 새 의존성 없음. **음성 확인**: `CrmVendor` 에 값 하나를 더하면(migration 그대로) 이 테스트 실패 · 같은 상황의 `alembic check` 테스트는 통과 — alembic 이 못 잡는 것을 이 테스트가 잡음. 되돌림 확인 |
| **W2** EncryptedJSONB | `backend/common/crypto.py:85-110` | 민감 키 값이 `str` 아니면 `TypeError("sensitive key 'x' must be a string")` · 민감 키 이름이 중첩 dict/list 안에 나오면 `ValueError(... must be at the top level)` — 메시지에 키 이름만. `decrypt_value` 는 비문자열도 `DecryptionError`(`:48`). 테스트 `tests/common/test_crypto.py:74`(비문자열 4종: int · dict · list · None) · `:83`(중첩 dict · list 안 dict), 둘 다 메시지에 값 없음 단언 |
| **W3** migration 상한 | `backend/common/config.py:55-56` · `backend/common/db/session.py:49` · `backend/migrations/env.py:102` | `MIGRATION_STATEMENT_TIMEOUT_MS`(기본 0 = 없음) · `MIGRATION_LOCK_TIMEOUT_MS`(기본 5000) → `migration_connect_args()`, env.py 가 이것만 쓴다(서비스 `DATABASE_STATEMENT_TIMEOUT_MS` 안 씀). 테스트(실 PG · alembic subprocess): `test_alembic.py:133` — 다른 접속이 `alembic_version` 을 ACCESS EXCLUSIVE 로 잡고 있으면 `MIGRATION_LOCK_TIMEOUT_MS=200` 인 upgrade 가 LockNotAvailable 로 끊긴다 · `:149` — 서비스 상한을 100ms 로 넣고 잠금을 1초 잡아도 migration 이 끊기지 않고 끝난다(서비스 상한이 걸렸다면 100ms 에 57014). 두 테스트 모두 고치기 전 설정(30s statement_timeout · lock_timeout 없음)이면 실패하는 모양 |
| **W4** 대조 | 스크립트 `work/day-data-architecture/backend-225-spec-compare.py:31,195` | 「모델에만 있는 칸」을 불일치로 센다. 예외는 `ALLOWED_EXTRA` 목록 3(event_log · push_log · external_outbox 의 `deleted_at` — §2) — 표에 「§2 로 더함」으로 따로 보인다. 재실행: SPEC 51 · 모델 51 · **불일치 0**. 음성 확인: 모델 `visit` 에 `kos_status` 칸을 넣으면 `**모델에만(불일치)** kos_status` · 불일치 1 |
| | `backend/tests/day/test_column_snapshot.py` (새) | 51 테이블 → 칸 이름 557개 스냅샷(모델에서 뽑아 고정). 칸이 늘거나 빠지면 테이블별로 실패(51 + 1 테스트) |
| **W5** offline | `backend/migrations/env.py:114-118` | offline 분기 트랜잭션 맨 앞에 `CREATE SCHEMA IF NOT EXISTS <DB_SCHEMA>` · `SET search_path TO <DB_SCHEMA>, public`. 테스트 `tests/migrations/test_offline_sql.py:11`(DB 접속 없음): 두 줄이 이 순서로 첫 `CREATE TYPE` 과 `alembic_version` 보다 앞 |
| **W6** 키 | `backend/common/config.py:51,75,99-116` | `ENCRYPTION_KEY` 는 설정 모델에서 선택(빈 값 = 없음, 형식은 여전히 검사). `get_settings()`(api · worker · scheduler · 암호화 칸이 쓰는 것)는 키가 없으면 `EncryptionKeyMissingError`. `get_database_settings()` 는 키 없이 읽는다 — `migrations/env.py:39` · `day/db.py:17` 만 쓴다. `common/crypto._fernet` 은 `get_settings()` 경유라 **키 없이 암호화 칸 읽기/쓰기 = 오류**(평문 폴백 없음 그대로) |
| | `deploy/compose.local.yaml:66-70` | migrate 서비스만 `environment: {<<: *backend-environment, ENCRYPTION_KEY: ""}`. YAML 병합 안에서는 `!reset` 이 듣지 않아(compose config 로 확인) 빈 값으로 뺐다 — 설정은 빈 값을 「없음」으로 읽는다. api · worker · scheduler 는 그대로 키를 받는다 |
| | 테스트 | `test_alembic.py:117` 키 없이 upgrade(파일의 모든 alembic subprocess 가 키를 빼고 돈다) · `test_offline_sql.py` 키 없음 · `tests/runtime/test_startup_key.py:12` api `create_application()` 키 없으면 실패 · `:20` worker · scheduler 진입점 import 키 없으면 실패 · `test_crypto.py:57` DB 설정은 키 없이 · `:67` 키 없이 암호화 칸 쓰기 = 오류 |

## 검증 수치

| 명령 | 결과 |
|---|---|
| `scripts/test.sh -q` (로컬 compose PG · Redis, `DAY_REQUIRE_INFRA=1`) | **143 passed** in 12.30s (전 80 — +스냅샷 52 · 마이그레이션 4 · enum 1 · 암호화/키 6 · 기동 3 · offline 1 등) |
| `uv run pytest -q` (인프라 없이) | 104 passed, 39 skipped |
| `uv run ruff check backend` | All checks passed! |
| 대조 스크립트 1회 | SPEC 51 · 모델 51 · 불일치 0 (§2 로 더함 3) |
| compose: 로컬 `day_dev` 를 키 없이 `downgrade 0001_baseline` → `--profile app up --build --wait` | migrate 컨테이너 `ENCRYPTION_KEY=`(빈 값) · `Running upgrade 0001_baseline -> 0002_data_model` 성공 · api 키 있음 · `/health/ready` 200 · `day_dev` 0002 · 테이블 52 · scheduler `Sending task day.ping` → worker `Executing task day.ping` · `down`(볼륨 남김) · DB 스키마는 `day_dev` 하나 |

## 주의 · 코디 확인

- W6 의 「api 키 없으면 기동 실패」는 `create_application()` 안의 `get_settings()` 가 지킨다(runtime 파일은 고치지 않음). worker · scheduler 는 브로커를 만들 때 `get_settings()` 를 불러 같은 방식으로 실패.
- 키가 **빈 값**이어도 「없음」이다 — compose migrate 가 이 성질로 키를 뺀다. 키를 빈 값으로 둔 api 도 뜨지 않는다(`get_settings` 가 거절).
- `tests/day/conftest.py` 의 세션 migration subprocess 는 아직 테스트 키를 물려받는다(무해 — 키 없이 도는 것은 `test_alembic.py` 가 따로 증명).
- 남은 것: W7 · W8 · 조용히 통과 5 · 6(사용자 결정 대기) · 열린 enum 8칸 · OQ 들.

## 변경 파일(이번 fix1)

`backend/common/config.py` · `backend/common/crypto.py` · `backend/common/db/session.py` · `backend/day/db.py` · `backend/migrations/env.py` · `deploy/compose.local.yaml` · `backend/tests/conftest.py` · `backend/tests/common/test_crypto.py` · `backend/tests/migrations/test_alembic.py` · 새 `backend/tests/migrations/test_offline_sql.py` · 새 `backend/tests/day/test_enum_labels.py` · 새 `backend/tests/day/test_column_snapshot.py` · 새 `backend/tests/runtime/test_startup_key.py` · 저장소 밖 `work/day-data-architecture/backend-225-spec-compare.py`(+ 출력 `.out.md` 갱신)

---

## 추가(사용자 결정 2026-11-05) — 유일은 살아 있는 행만 · direct_key 병원별

### 바꾼 제약 전체 목록 (grep 전수 — 모델의 UNIQUE 8개 전부, 모두 `deleted_at` 있는 테이블)

| # | 전 (UNIQUE 제약 · 이름) | 후 (부분 유일 인덱스 `WHERE deleted_at IS NULL`) |
|---|---|---|
| 1 | `brand.code` · `uq_brand_code` | `uq_brand_code` (code) |
| 2 | `customer(hospital_id, chart_number)` · `uq_customer_hospital_id` | `uq_customer_hospital_id_chart_number` |
| 3 | `external_ref(hospital_id, vendor, entity_type, external_id)` · `uq_external_ref_hospital_id` | `uq_external_ref_hospital_id_vendor_entity_type_external_id` |
| 4 | `login_session.token_hash` · `uq_login_session_token_hash` | `uq_login_session_token_hash` |
| 5 | `device.install_id` · `uq_device_install_id` | `uq_device_install_id` |
| 6 | `chat_room.direct_key` · `uq_chat_room_direct_key` | **`uq_chat_room_hospital_id_direct_key` (hospital_id, direct_key)** — 병원별 유일 |
| 7 | `chat_message(room_id, seq)` · `uq_chat_message_room_id` | `uq_chat_message_room_id_seq` |
| 8 | `chat_message(account_id, client_id)` · `uq_chat_message_account_id` | `uq_chat_message_account_id_client_id` |

- 전 이름은 naming convention(`uq_%(table_name)s_%(column_0_name)s`)이 첫 칸만 써서 복합 제약 이름이 잘려 있었다 — 새 이름은 칸 전부(`live_unique` 가 정함).
- **복합 PK 13개는 그대로**(crm_connection · customer_category_link · account_brand_access · job_role_permission · external_session · visit_task_staff · doctor_call_task · board_card_order · reservation_group_capacity · reservation_group_timetable · visit_occupied_resource_doctor · notification_setting · chat_member) — 지운 행이어도 막는다.
- 인덱스(비유일) `ix_customer_name` · `ix_customer_phone_number` · `ix_external_ref_entity_type_entity_id` 는 그대로.
- 주의(다음 Delivery): 부분 유일 인덱스에 `INSERT … ON CONFLICT` 를 쓸 때는 같은 `WHERE deleted_at IS NULL` 을 줘야 한다(`index_where`) — `backend/day/models/_columns.py` `live_unique` docstring 에 적음.

### 고친 곳

| 파일 | 내용 |
|---|---|
| `backend/day/models/_columns.py` | `live_unique(table, *columns)` — `Index(uq_…, unique=True, postgresql_where=deleted_at IS NULL)` · 머리말에 규칙 |
| `backend/day/models/{hospital,customer,staff,misc}.py` | `unique=True` · `UniqueConstraint` 8곳 → `__table_args__` 의 `live_unique(...)`. `chat_room` 은 (hospital_id, direct_key). 모델에 `UniqueConstraint` · `unique=True` 칸 0 |
| `backend/migrations/versions/20261105_0002_data_model_first_data_model.py` | (아직 어디에도 적용 안 된 0002 를 고침) `create_table` 안의 `sa.UniqueConstraint` 8개 제거 → 맨 위 `LIVE_UNIQUE` 목록 + 테이블 생성 뒤 `op.create_index(..., unique=True, postgresql_where=deleted_at IS NULL)` · downgrade 맨 앞에서 `drop_index` |
| `backend/tests/day/test_constraints.py` | 살아 있는 행끼리 23505(기존 8 사례 · chat_room 은 같은 병원) + **새** `test_지운_행과_같은_값은_다시_넣을_수_있다` 8 사례 · `test_direct_key_는_병원이_다르면_같아도_된다` · `test_유일_사례는_모델의_부분_유일_인덱스_전부다`(모델에 UniqueConstraint 0 · 유일 인덱스는 전부 `deleted_at IS NULL` · 테스트 사례 집합 == 모델 유일 인덱스 집합 — 새 유일 칸이 생기면 사례를 강제) |
| 대조 스크립트 | 유일 인덱스를 「UNIQUE (… 살아 있는 행)」으로 표시. **SPEC 이 17:20 에 바뀌어(미커밋 — #225 결정 반영: §2 「유일 · 삭제」 · §2.1 FK 대상 · 「코드 테이블 타입 · 필수」 표 · `direct_key` 병원별) 파서가 깨져** 고침: 새 「코드 테이블 타입 · 필수」 표를 읽어 코드 테이블 5개도 타입 · 필수를 대조한다(전에는 「타입 미표기」로 건너뜀). 음성 확인: `funnel.name` NULL 허용 · `customer_category.color` int 로 바꾸면 불일치 2 |

### 수치

| 명령 | 결과 |
|---|---|
| `scripts/test.sh -q` | **153 passed** in 12.51s (+10: 지운 행 재사용 8 · direct_key 병원별 1 · 인덱스 전수 1) |
| `uv run pytest -q` (인프라 없이) | 104 passed, 49 skipped |
| `uv run ruff check backend` | All checks passed! |
| 대조 스크립트 | SPEC 51 · 모델 51 · 불일치 0 (코드 테이블 타입 · 필수 포함) |
| `alembic check` 테스트(diff 0) · 빈 스키마 upgrade/downgrade/upgrade 테스트 | 통과 |
| 로컬 `day_dev` | 옛 0002(UNIQUE 제약 8, 행 0)라 새 0002 의 downgrade(인덱스 drop)가 맞지 않아 **스키마를 DROP**(로컬 · 빈 스키마) → compose migrate(키 없음)가 `-> 0001 -> 0002` 로 다시 만듦 · `pg_constraint` UNIQUE **0** · `pg_indexes` 부분 유일 **8**(전부 `WHERE (deleted_at IS NULL)`) · api `/health/ready` 200 · worker `day.ping` 실행 · `down` |
