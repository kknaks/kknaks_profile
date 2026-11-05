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
