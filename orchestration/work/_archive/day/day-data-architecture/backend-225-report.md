# #225 DAY v2 데이터 모델 결과 보고

## 상태: done

워크트리 `/Users/kknaks/orca/workspaces/CENTURION_DAY/day-data-architecture`(브랜치 `kknaksss/day-data-architecture`, #224 커밋 `ec2a2681` 위). 커밋 · push · PR 안 함.

## 완료 조건

| | 결과 | 증거 |
|---|---|---|
| **A1** 모델 51 = SPEC §3 51 | 충족 | 대조 스크립트(아래) — SPEC 테이블 51 · 모델 51 · 불일치 테이블 0. SPEC 칸 560 − 보류(—) 6 = 554 + §2 `deleted_at` 3 = 모델 칸 557. `test_models.py::test_모델은_SPEC_1차_51_테이블과_같다` |
| **A2** 04-1 13 테이블 안 만듦 | 충족 | `test_04_1_메뉴_테이블은_만들지_않는다`(SPEC §4 이름 13개와 교집합 0) |
| **A3** 빈 DB_SCHEMA upgrade · downgrade + 제약 | 충족 | 새 스키마에 upgrade → downgrade base → upgrade(`test_alembic.py` 3개, 스키마 `day_test_<hex>`) · `alembic check` diff 0(새 테스트) · 유일 8 + 복합 PK 13 + enum + NOT NULL = `test_constraints.py` 23개, 전부 PostgreSQL sqlstate 로 확인(23505 · 22P02 · 23502) · compose migrate 로 `day_dev` 0001 → 0002 |
| **A4** 민감 칸 암호화 | 충족 | `test_encryption.py` — raw SELECT 값이 `enc:` 접두 Fernet 암호문, 평문 미포함, ORM 으로 읽으면 평문: 주민번호 · 외국인등록번호 · 여권번호 · `crm_connection.config`(open_api_key · system_email · system_password) · `external_session.access_token` · `device.push_token`. 다른 키로 읽으면 `DecryptionError`(평문 반환 없음) |
| **A5** ORM · Base 는 day 밖으로 안 나감 | 충족 | 경계 테스트 10개 통과 — `day.public` 은 여전히 빈 `__all__`, runtime/common 은 day 내부 import 0. migrations 예외는 `migrations/env.py` → `day.db` · `day.models` 만 |

## 수치

| 명령 | 결과 |
|---|---|
| `scripts/test.sh -q` (로컬 compose PG · Redis, `DAY_REQUIRE_INFRA=1`) | **80 passed** in 7.91s |
| `uv run pytest -q` (인프라 없이) | 45 passed, 35 skipped |
| `uv run ruff check backend` | All checks passed! |
| 실 PG 수동: 빈 스키마 `day_mig1` 에 upgrade → `alembic check` → downgrade base → upgrade | 테이블 52(51 + alembic_version) · enum 타입 28 · `public` 0 · check `No new upgrade operations detected.` |
| offline `alembic upgrade head --sql` | rc 0 · `CREATE TABLE` 52 · `CREATE TYPE` 28 (W8 — `CREATE SCHEMA` 없음 — 은 그대로) |
| compose `--profile app up --build --wait` | migrate `0001_baseline -> 0002_data_model` · api `/health/ready` 200 · `day_dev` 테이블 52 · enum 28 · scheduler `Sending task day.ping` → worker `Executing task day.ping` |
| compose `run -e ENCRYPTION_KEY= api …create_application()` | `ValidationError … ENCRYPTION_KEY must be a Fernet key` — 기동 실패 |
| 정리 | `compose down`(볼륨 남김) · 내가 만든 스키마 `day_gen` · `day_mig1` DROP · 테스트 스키마는 테스트가 DROP → DB 에 `day_dev` 만 |

## 테이블 목록 — 센 방법 · 51 과의 차이

- SPEC-000 §3(`## 3.` ~ `## 4.` 앞)의 테이블 머리(`#### \`이름\`` · `#### 이름 · …`) 정규식 = **46**, 02 「코드 테이블」 표의 한 줄 = **5**(`customer_type` · `customer_category` · `funnel_category` · `funnel` · `customer_category_link`) → **51**. Issue 의 51 과 **같다**.
- 04-1(§4): 머리 11 + 묶음 머리 2개 안의 두 번째 이름(`medical_service_medicine` · `medicine`) = **13** — Issue 의 「13」과 같고, 만들지 않음.

## SPEC ↔ 원천(erd 01 ~ 07) 차이

스크립트로 같은 파서를 원천 7개 파일에 돌려 비교 — 테이블 46 + 코드 5 의 필드 · 타입 · 필수 행이 **전부 같다**, 「제약:」 줄(customer · external_ref)도 같다. **차이 없음.**

## 코디 결정 1 ~ 6 처리

1. `product_option_id` — `visit_requested_procedure` · `consultation_procedure` 에 uuid 칸만, FK 없음, DB 칸 주석 「상품 옵션 참조 — FK 없음(1차 메뉴 테이블 없음). 04-1 생기면 FK」. 테스트 `test_product_option_id_는_FK_없는_uuid_칸이다`.
2. enum — **PostgreSQL native enum**. 근거: centurion `crm` 에는 DB enum 칸이 없어(`crm/enums.py` 는 코드 전용, `crm/models.py` 에 enum 칸 없음) 같은 레포 linky 선례를 따랐다 — `SQLEnum(native_enum=True, values_callable=…)` 34곳 · `native_enum=False` 0곳. 정해진 enum 28종 = DB 타입 28(`crm_vendor` 는 4테이블 · `flow_step` · `procedure_kind` · `option_type` 은 2테이블이 같은 타입을 씀)을 `backend/day/enums/<주제>.py` StrEnum 으로, DB 타입은 `DB_SCHEMA` 안. **열린 enum → varchar · 제약 없음 · DB 주석**: `customer.gender`(OQ-02-1) · `external_ref.entity_type`(목록이 「…」) · `visit_task.unit_type`(「cc · unit · shot …」) · `id_photo.doc_type`(「passport · id_card …」) · `display_request.kind` · `identity_check.status` · `identity_check.method` · `notification_setting.kind`(SPEC 에 값 없음 — OQ-07-3). `nationality` · `language` 도 OQ-02-1 주석.
3. 07 알림 · 접수 · 채팅 — SPEC 대로 13 테이블 만듦.
4. 보류 칸 — 안 만듦: `visit.purchase_ids` · `prescription_ids` · `reactions`(OQ-03-1). 같이 「—」인 `consultation.procedures`(→ `consultation_procedure`) · `visit_occupied_resource.doctor_ids`(→ `visit_occupied_resource_doctor`) · `id_photo` 「KOS 업로드 상태」(→ external_outbox)도 칸 없음 — 대조표 「보류」 6.
5. 암호화 — `backend/common/crypto.py`(Fernet · `EncryptedText` · `EncryptedJSONB(sensitive_keys)`, centurion 모양). **centurion 과 다른 점**: 평문 폴백 없음 — `ENCRYPTION_KEY` 는 `Settings` 필수 칸 + Fernet 형식 검사라 키가 없거나 틀리면 api · worker · scheduler · alembic 모두 기동 실패(dev 포함). 읽을 때 접두어 없음 · 다른 키면 원문 반환 대신 `DecryptionError`. `crm_connection.config` 는 최상위 `open_api_key` · `system_email` · `system_password` 만 암호화, `tenant_id` 는 평문(로그인 ② 에서 병원 고르는 데 읽는 값 — SPEC 04). 테스트 키는 `tests/conftest.py` 가 실행마다 `Fernet.generate_key()`. 코디 허용으로 `deploy/compose.local.yaml` x-backend 에 `ENCRYPTION_KEY: ${DAY_LOCAL_ENCRYPTION_KEY:?…}` 한 줄 · `deploy/local.env.example` 에 자리표시자 + 생성 명령.
6. #224 이월 — **W6**: `DATABASE_STATEMENT_TIMEOUT_MS`(기본 30000) → 접속 `server_settings.statement_timeout`(alembic 접속에도 걸림). 테스트: `SHOW statement_timeout = 30s` · 200ms 로 `pg_sleep(2)` → 57014 취소. **in-process 테스트 스키마**: `tests/day/conftest.py` 세션 fixture 가 `day_test` 를 DROP → `alembic upgrade head`(subprocess)로 만들고 세션 끝에 DROP. 테스트마다 세션 rollback. `test_테스트_프로세스는_day_dev_를_쓰지_않는다` 유지 · 통과.

## env.py autogenerate 수정 (코디 허용)

- 증상: `alembic check` 가 이미 있는 51 테이블을 전부 `add_table` 로 냈다. 원인 두 겹 — (1) alembic 은 기본 스키마(search_path 첫 칸 = `DB_SCHEMA`)를 `include_name` 에 `None` 으로 넘기는데 #224 필터가 `name == SCHEMA` 라 빠졌고 (2) `None` 을 받아도 모델 `MetaData(schema=X)` 와 반사(스키마 없음)가 어긋나 FK 119쌍 remove/add.
- 수정: 비교용 metadata = 모델 테이블을 `to_metadata(schema=None)` 로 복사하고 native enum(배열 포함)도 복사본에서만 스키마를 비움 · `include_schemas` 끔(기본 스키마만) · `alembic_version` 은 비교 제외. 업그레이드 경로 · offline 경로는 그대로. 모델 FK 문자열은 스키마 없이(`ForeignKey("hospital.id")` — MetaData 가 스키마를 붙인다)로 바꿈.
- 검증: 새 테스트 `test_upgrade_head_뒤_alembic_check_는_차이가_없다` — **수정 전 실패**(1 failed) → 수정 후 통과. upgrade/downgrade · offline `--sql` 그대로 동작.
- **#224 의 「가짜 차이 없음」 확인이 놓친 이유**: 그때는 모델 0개 · FK 0개라 비교할 것이 없었고, 스크래치 확인도 FK 없는 단일 테이블로만 봐서 (1) 기본 스키마 `None` 필터와 (2) FK 참조 스키마 불일치가 드러나지 않았다.

## migration 손 검토(autogenerate 뒤 고친 것)

`backend/migrations/versions/20261105_0002_data_model_first_data_model.py`
- 스키마 이름 제거(`schema='…'` · FK `'<schema>.x.id'`) — search_path 로 `DB_SCHEMA` 에 만들어져 같은 리비전이 dev · prod 에 그대로.
- enum 28 타입을 맨 위에 `postgresql.ENUM(..., create_type=False)` 로 한 번 정의, `upgrade` 처음에 만들고 `downgrade` 끝에 지움(공유 타입 중복 생성 방지).
- `chat_message.attachment_id` ↔ `chat_attachment.message_id` 순환 FK — 테이블 생성 뒤 `create_foreign_key`, downgrade 처음에 `drop_constraint`.
- 암호화 칸은 DB 타입 그대로(TEXT · JSONB) — 리비전이 앱 코드(`common.crypto`)를 import 하지 않게.

## 판단한 곳 · SPEC 이 말하지 않은 것 (코디 확인 권장)

- **§2 「삭제 — 모든 테이블에 deleted_at」 > 표**: `event_log` · `push_log` · `external_outbox` 표에 `deleted_at` 이 없지만 「표 읽는 법 — §2 와 어긋나면 §2 우선」에 따라 둠(대조표 「모델에만 deleted_at」 3). `updated_at` 은 추가하지 않음(§2 가 강제하지 않음). `visit_flow_log` 은 표대로 `deleted_at` 만(생성 · 수정 시각 없음).
- **FK 대상이 「uuid FK」로만 적힌 칸**: 이름 · 설명으로 대상 결정 — 직원류(`*_staff_id` · `assigned_*` · `requested_*` · `counselor_id` · `doctor_id` · `started_by` · `ended_by` · `reservation_assignee_id`) → `staff`, `*_zone_id` → `zone`, `room_id` → `room`, `funnel_id` → `funnel`, `referrer_customer_id` → `customer`. `event_log.hospital_id` · `external_outbox.hospital_id` · `board_card_order.hospital_id/visit_id` 도 FK(§2 · PK 구성).
- **FK 안 건 칸**: `external_ref.entity_id`(SPEC 명시) · `product_option_id`(결정 1) · `external_outbox.visit_id`(SPEC 타입 「uuid · int」— FK 표기 없음).
- **코드 테이블 5개**는 SPEC 에 타입 · 필수가 없다: `id` · `hospital_id` · `name` NOT NULL, `color`/`sort_order`/`is_closed`/`is_default`/`category_id` NULL 허용, 타입은 같은 이름의 다른 SPEC 칸(varchar · int · bool · uuid FK)을 따름.
- 기본값: `created_at` · `updated_at` 만 DB `now()`(+ ORM onupdate). bool 필수 칸 등 그 밖의 기본값은 두지 않음(SPEC 에 없음).
- 「최대 1,000자 / 2,000자 / 5,000자」(예약 · 오더 · 상담 메모)는 설명의 KOS 한도로 보고 DB CHECK 를 걸지 않음.
- §2 「업무 테이블에 hospital_id」 — SPEC 표에 없는 테이블(`visit_task` · `consultation` 등 하위 테이블)에는 덧붙이지 않음(표 그대로).

## 제안 (만들지 않음)

- `notification_setting.kind` 는 `notification.kind` 와 같은 enum 일 가능성이 크다 — SPEC 에 값이 없어 varchar 로 둠.
- 인덱스: SPEC 의 customer 이름 · 전화번호 · external_ref(entity_type, entity_id)만 만듦. 목록 화면이 정해지면 `visit(hospital_id, reserved_start_at)` · FK 칸 인덱스를 검토.
- 키 교체(MultiFernet) 없음 — 키가 바뀌면 기존 암호문을 못 푼다.

## 변경 파일

- 새: `backend/common/crypto.py` · `backend/day/enums/{__init__,hospital,customer,visit,staff,task,room,misc}.py` · `backend/day/models/{__init__,_columns,hospital,customer,visit,staff,task,room,misc}.py` · `backend/migrations/versions/20261105_0002_data_model_first_data_model.py` · `backend/tests/day/{__init__,conftest,factories,test_constraints,test_encryption,test_models}.py` · `backend/tests/common/test_crypto.py`
- 수정: `backend/common/config.py`(ENCRYPTION_KEY 필수 · statement timeout) · `backend/common/db/session.py`(statement_timeout) · `backend/migrations/env.py`(코디 허용 — `import day.models` · 비교용 metadata) · `deploy/compose.local.yaml`(코디 허용 1줄) · `deploy/local.env.example` · `pyproject.toml` · `uv.lock`(cryptography 46) · `backend/tests/{conftest,migrations/test_alembic,common/test_db_session,test_infra_guard}.py`
- 저장소 밖: 대조 스크립트 `work/day-data-architecture/backend-225-spec-compare.py`(SPEC 절대경로를 읽어서 레포에 두지 않음) · 출력 `backend-225-spec-compare.out.md`(아래와 같음)

## 남은 것

- W5 · W8 · W9(브리프 범위 밖) — 그대로. 특히 W8(offline `--sql` 에 `CREATE SCHEMA` 없음)은 이번 리비전으로 더 커짐(prod 첫 적용 전 필요).
- §6 OQ 는 결정하지 않음 — 열린 enum 8칸은 값이 정해지면 enum 으로 바꾸는 migration 필요.
- 07(OQ-07-3) 칸 단위 사용자 검토 · DAY-ESC-001 법적 검토 회신 전.

## 대조표 (스크립트 출력 — 손으로 쓰지 않음)

열: SPEC 칸(보류 포함) · 보류(—) · 모델 칸 · 칸 차이 · 타입 · 필수 · PK · 유일/FK/비고. 「모델에만 deleted_at」 = §2 규칙. 검사기는 결함을 넣어 보면 잡는다(필수 · 타입 · 길이 세 가지 주입 → 불일치 3).

SPEC 테이블 51 · 모델 테이블 51 · SPEC 만 [] · 모델만 []

| 테이블 | SPEC 칸 | 보류(—) | 모델 칸 | 칸 차이 | 타입 | 필수 | PK | 유일 · FK · 비고 |
|---|---|---|---|---|---|---|---|---|
| `account` | 9 | 0 | 9 | 없음 | 맞음 | 맞음 | (id) | FK 0 |
| `account_brand_access` | 5 | 0 | 5 | 없음 | 맞음 | 맞음 | (account_id,brand_id) | FK 2 |
| `board_card_order` | 8 | 0 | 8 | 없음 | 맞음 | 맞음 | (hospital_id,board_date,visit_id) | FK 3 |
| `brand` | 7 | 0 | 7 | 없음 | 맞음 | 맞음 | (id) | UNIQUE (code) · FK 0 |
| `chat_attachment` | 15 | 0 | 15 | 없음 | 맞음 | 맞음 | (id) | FK 3 |
| `chat_member` | 12 | 0 | 12 | 없음 | 맞음 | 맞음 | (room_id,account_id) | FK 2 |
| `chat_message` | 12 | 0 | 12 | 없음 | 맞음 | 맞음 | (id) | UNIQUE (account_id,client_id) / (room_id,seq) · FK 3 |
| `chat_room` | 11 | 0 | 11 | 없음 | 맞음 | 맞음 | (id) | UNIQUE (direct_key) · FK 2 |
| `consultation` | 10 | 1 | 9 | 없음 | 맞음 | 맞음 | (id) | FK 3 · 보류 procedures |
| `consultation_procedure` | 13 | 0 | 13 | 없음 | 맞음 | 맞음 | (id) | FK 1 |
| `crm_connection` | 7 | 0 | 7 | 없음 | 맞음 | 맞음 | (hospital_id) | FK 1 |
| `customer` | 41 | 0 | 41 | 없음 | 맞음 | 맞음 | (id) | UNIQUE (hospital_id,chart_number) · FK 7 · gender=열린 enum→varchar |
| `customer_category` | 9 | 0 | 9 | 없음 | 맞음 | 맞음 | (id) | FK 1 |
| `customer_category_link` | 5 | 0 | 5 | 없음 | 맞음 | 맞음 | (customer_id,category_id) | FK 2 |
| `customer_type` | 6 | 0 | 6 | 없음 | 맞음 | 맞음 | (id) | FK 1 |
| `device` | 10 | 0 | 10 | 없음 | 맞음 | 맞음 | (id) | UNIQUE (install_id) · FK 1 |
| `display_request` | 15 | 0 | 15 | 없음 | 맞음 | 맞음 | (id) | FK 4 · kind=열린 enum→varchar |
| `doctor_call` | 9 | 0 | 9 | 없음 | 맞음 | 맞음 | (id) | FK 4 |
| `doctor_call_accept` | 8 | 0 | 8 | 없음 | 맞음 | 맞음 | (id) | FK 3 |
| `doctor_call_task` | 5 | 0 | 5 | 없음 | 맞음 | 맞음 | (call_id,task_id) | FK 2 |
| `event_log` | 8 | 0 | 9 | 없음 | 맞음 | 맞음 | (id) | FK 3 · 모델에만 deleted_at |
| `external_outbox` | 16 | 0 | 17 | 없음 | 맞음 | 맞음 | (id) | FK 2 · 모델에만 deleted_at |
| `external_ref` | 15 | 0 | 15 | 없음 | 맞음 | 맞음 | (id) | UNIQUE (hospital_id,vendor,entity_type,external_id) · FK 1 · entity_type=열린 enum→varchar |
| `external_session` | 8 | 0 | 8 | 없음 | 맞음 | 맞음 | (session_id) | FK 1 |
| `funnel` | 10 | 0 | 10 | 없음 | 맞음 | 맞음 | (id) | FK 2 |
| `funnel_category` | 8 | 0 | 8 | 없음 | 맞음 | 맞음 | (id) | FK 1 |
| `hospital` | 7 | 0 | 7 | 없음 | 맞음 | 맞음 | (id) | FK 1 |
| `id_photo` | 12 | 1 | 11 | 없음 | 맞음 | 맞음 | (id) | FK 3 · 보류 KOS 업로드 상태 · doc_type=열린 enum→varchar |
| `identity_check` | 12 | 0 | 12 | 없음 | 맞음 | 맞음 | (id) | FK 5 · method=열린 enum→varchar · status=열린 enum→varchar |
| `job_role` | 8 | 0 | 8 | 없음 | 맞음 | 맞음 | (id) | FK 1 |
| `job_role_permission` | 6 | 0 | 6 | 없음 | 맞음 | 맞음 | (job_role_id,permission_key) | FK 1 |
| `login_session` | 11 | 0 | 11 | 없음 | 맞음 | 맞음 | (id) | UNIQUE (token_hash) · FK 3 |
| `notice` | 7 | 0 | 7 | 없음 | 맞음 | 맞음 | (id) | FK 1 |
| `notification` | 12 | 0 | 12 | 없음 | 맞음 | 맞음 | (id) | FK 4 |
| `notification_setting` | 6 | 0 | 6 | 없음 | 맞음 | 맞음 | (account_id,kind) | FK 1 · kind=열린 enum→varchar |
| `push_log` | 16 | 0 | 17 | 없음 | 맞음 | 맞음 | (id) | FK 5 · 모델에만 deleted_at |
| `questionnaire_history` | 13 | 0 | 13 | 없음 | 맞음 | 맞음 | (id) | FK 4 |
| `reservation_group` | 9 | 0 | 9 | 없음 | 맞음 | 맞음 | (id) | FK 1 |
| `reservation_group_capacity` | 6 | 0 | 6 | 없음 | 맞음 | 맞음 | (group_id,zone_id) | FK 2 |
| `reservation_group_timetable` | 10 | 0 | 10 | 없음 | 맞음 | 맞음 | (group_id,weekday) | FK 1 |
| `room` | 8 | 0 | 8 | 없음 | 맞음 | 맞음 | (id) | FK 2 |
| `staff` | 14 | 0 | 14 | 없음 | 맞음 | 맞음 | (id) | FK 4 |
| `visit` | 32 | 3 | 29 | 없음 | 맞음 | 맞음 | (id) | FK 9 · 보류 purchase_ids,prescription_ids,reactions |
| `visit_anesthesia` | 9 | 0 | 9 | 없음 | 맞음 | 맞음 | (id) | FK 3 |
| `visit_flow_log` | 7 | 0 | 7 | 없음 | 맞음 | 맞음 | (id) | FK 2 |
| `visit_occupied_resource` | 11 | 1 | 10 | 없음 | 맞음 | 맞음 | (id) | FK 3 · 보류 doctor_ids |
| `visit_occupied_resource_doctor` | 5 | 0 | 5 | 없음 | 맞음 | 맞음 | (occupied_resource_id,staff_id) | FK 2 |
| `visit_requested_procedure` | 13 | 0 | 13 | 없음 | 맞음 | 맞음 | (id) | FK 1 |
| `visit_task` | 30 | 0 | 30 | 없음 | 맞음 | 맞음 | (id) | FK 2 · unit_type=열린 enum→varchar |
| `visit_task_staff` | 6 | 0 | 6 | 없음 | 맞음 | 맞음 | (task_id,staff_id,role) | FK 2 |
| `zone` | 8 | 0 | 8 | 없음 | 맞음 | 맞음 | (id) | FK 1 |

불일치 테이블 0
