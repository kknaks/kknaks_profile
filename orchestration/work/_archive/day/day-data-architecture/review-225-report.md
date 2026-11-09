# 리뷰 리포트 — day-data-architecture / code · Delivery #225 데이터 모델 (2026-11-05)

대상: 워크트리 `/Users/kknaks/orca/workspaces/CENTURION_DAY/day-data-architecture` — HEAD `ec2a2681`(#224 커밋) 위의 미커밋 변경(수정 11 · 신규 28 파일). 읽기 전용, 레포 파일 수정 0.

근거 표기: **I#225** = Delivery Issue #225(「바뀌는 것」 · 「하지 않는 것」 · A1~A5) · **SPEC** = DAY-SPEC-000(`spec-000-data-model.md`) 절 · **AG** = 레포 `AGENTS.md` 절 · **브리프** = `backend-225-brief.md` §3 코디 결정 1~6 · **R224** = 내 #224 리뷰 W 번호.

## 판정: WARN

FAIL 은 없다. A1 ~ A5 는 직접 확인했다 — 51 테이블 전부를 모델 덤프와 SPEC 표로 한 칸씩 대조했고, FK 대상 · 필수 · enum 값 · UNIQUE 범위 · 복합 PK 가 모두 SPEC 과 같다. migration 은 dev/prod 에 같은 결과를 내고, downgrade 뒤 남는 것이 없으며, 앱 코드를 import 하지 않는다.
WARN 은 **「테스트 · 검사는 초록인데 놓치는 자리」 3개**(W1 enum 값 · W2 JSONB 비문자열 평문 · W3 migration 에 걸린 30초 statement_timeout)와, #224 에서 넘어온 W8(offline SQL)이 이번 리비전으로 커진 것이다.

## 계약 대조 (I#225)

| 항목 | 결과 | 근거 |
|---|---|---|
| A1 모델 51 = SPEC §3 51 | 같음 — 아래 「직접 대조」 | 모델 덤프(스크래치) ↔ SPEC 03 ~ 07 표 전수 |
| A2 04-1 13 테이블 안 만듦 | 같음 | `tests/day/test_models.py:59-61` · 덤프에 메뉴 테이블 0 |
| A3 빈 DB_SCHEMA upgrade/downgrade · 유일 · 복합 PK 실 DB | 같음 | 직접: 스크래치 스키마 `day_rv225` 에 upgrade → downgrade base → upgrade → downgrade 0001 모두 rc 0. `test_constraints.py:339-346` 은 두 번째 INSERT 를 실제 PG 의 sqlstate 23505 로 확인한다(ORM 이 먼저 막지 않도록 `expunge` — `:325-334`). 진짜 DB 위반을 본다 |
| A4 민감 칸 암호화 | 같음(주의 W2) | `customer.py:48-50` · `hospital.py:27,56-58` · `staff.py:105` · `misc.py:65`. raw SELECT 테스트 `test_encryption.py` |
| A5 ORM · Base 는 day 밖으로 안 나감 | 같음 | `day/db.py` 에 Base · `common/db/model_base.py` 는 `make_metadata` 만(R224 W2 해결). 경계 테스트 예외는 `migrations/env.py` → `day.db` · `day.models` 만(`test_import_boundaries.py:39-40`, R224 W7 해결) |
| 하지 않는 것 | 넘지 않음 | `backend/day/` = `db.py` · `public.py`(빈 `__all__`) · `tasks/__init__.py` · `models/` · `enums/` 뿐. 서비스 · 라우터 · 동기화 · 로그인 · 화면 · 04-1 없음. §6 OQ 는 결정하지 않고 varchar + 주석으로 둠 |
| SPEC 에 없는 칸 · 테이블 · 인덱스 발명 | 없음 — 단 §2 근거의 `deleted_at` 3칸(아래 판정 「받아들임」). 인덱스는 SPEC 의 `customer` 이름 · 전화 · `external_ref(entity_type, entity_id)` 3개뿐 |

## 대조 스크립트가 보지 않는 것 (브리프 「믿지 마라」)

`backend-225-spec-compare.py` 는 **칸 이름 · 타입 종류 · 필수 · PK · varchar 길이**만 비교한다. 비교하지 않는 것:

| 빈틈 | 스크립트 자리 | 내가 한 것 |
|---|---|---|
| FK **대상** · ON DELETE | `:176` FK **개수**만 출력 | 51 테이블 전 FK 대상 덤프 대조 — 전부 SPEC 과 같음(SPEC 이 대상을 적은 칸), 대상 미표기 칸은 아래 판정표. ON DELETE 는 전부 기본(NO ACTION) — SPEC 에 말이 없고 소프트 딜리트와 맞음 |
| UNIQUE **범위** | `:173-179` 모델 UNIQUE 를 출력만, SPEC 과 비교 안 함 | SPEC 의 UNIQUE 8개(brand.code · customer(hospital_id, chart_number) · external_ref 4칸 · login_session.token_hash · device.install_id · chat_room.direct_key · chat_message 2개)와 모델이 같음. 덧붙인 UNIQUE 없음 |
| enum **값 목록** | `:113` 타입이 Enum 인지만 | 28 타입 전부 SPEC 값과 같음(덤프) + 실제 `day_dev` 의 `pg_enum` 라벨과 모델 enum 이 28/28 같음 |
| 기본값 | 안 봄 | `created_at` · `updated_at` 의 `now()` 만. 그 밖 서버 기본값 0 |
| 인덱스 | 안 봄 | 위 3개만 |
| **모델에만 있는 칸** | `:181-182` 「모델에만」을 비고로만 쓰고 `bad`(`:187`)에 넣지 않음 → **SPEC 에 없는 칸이 생겨도 「불일치 0」** | 덤프로 모델에만 있는 칸 = `deleted_at` 3개뿐임을 확인 |
| 코드 테이블 5개 | `:78,165,168` 타입 · 필수 · PK 를 아예 건너뜀 | 덤프로 확인 — 판정표 참고 |
| 타입 칸 개수가 안 맞을 때 | `:48-49` 첫 타입을 모든 칸에 복사(조용히 넘어갈 수 있음) | 묶음 칸(`title · body` · `apns_status · apns_reason · apns_id` 등)을 손으로 봄 — 맞음 |

→ 리포트의 「불일치 테이블 0」은 위 빈틈 안에서만 참이다. 이번에는 직접 대조로 빈틈 쪽도 맞음을 확인했다. 스크립트는 레포 밖이라 회귀를 지키지 못한다 — W1 · W4 참고.

## 직접 대조 — 표본이 아니라 전수

모델을 덤프(칸 · 타입 · NULL · FK 대상 · ON DELETE · 기본값 · UNIQUE · 인덱스 · enum 값)해 SPEC 03 ~ 07 표와 51 테이블 전부를 맞췄다(05 · 06 은 브리프대로 전부, 나머지도 전부).
- 05: `visit_task` 30칸 · enum 3종(task_kind · task_status · anesthesia_type 7값) · `room_id → room` · `medicines varchar[]` 같음. `visit_task_staff` PK(task, staff, role) · role 3값 같음. `doctor_call.reassigned_from_call_id → doctor_call`(자기 참조) 같음. `external_outbox.visit_id` FK 없음 = SPEC 「uuid · int」 FK 표기 없음과 같음. `event_log` · `external_outbox` 의 `updated_at` 유무도 SPEC 표대로.
- 06: 8 테이블 전부 같음. `weekday` enum mon ~ sun · `time` 칸 4개(UTC 예외) · 복합 PK 2개.
- 01 · 02 · 03 · 04 · 07: 같음. `brand.code varchar(50)` · `hospital.name varchar(100)` · `push_log.token_tail varchar(6)` 길이까지 같음.

## 「판단한 곳」 판정

| 판단 | 판정 | 근거 |
|---|---|---|
| §2 우선 — `event_log` · `push_log` · `external_outbox` 에 `deleted_at` 추가 | **받아들임** | SPEC §1 「표 읽는 법 — §2 와 어긋나면 §2 가 우선」 · §2 「삭제 — 모든 테이블에 deleted_at」. `updated_at` 은 안 붙임 — §2 가 강제하지 않으므로 맞다. 다만 「쌓기만 — 고치거나 지우지 않는다」와 문장이 부딪히므로 SPEC 에 한 줄 정리 요청(코디 → 문서 몫) |
| 「uuid FK」(대상 미표기) 대상 추론 — 직원류 → staff · `*_zone_id` → zone · `room_id` → room · `funnel_id` → funnel · `referrer_customer_id` → customer · `event_log/external_outbox.hospital_id` → hospital · `board_card_order.hospital_id/visit_id` | **받아들임** | 칸 설명과 같은 이름의 대상 표기 칸(예: customer `assigned_*` 「→ 직원(4번)」 · visit_task `room_id` 「→ room(6번)」)이 같은 뜻이다. 다른 해석이 가능한 칸 없음. SPEC 에 대상을 써 달라는 정리는 문서 몫 |
| FK 안 건 칸 — `external_ref.entity_id` · `product_option_id` · `external_outbox.visit_id` | **받아들임** | 앞 둘은 SPEC 명시 · 브리프 결정 1. 셋째는 SPEC 이 FK 를 안 적었다(`visit_id · seq` = 「uuid · int」). FK 를 걸면 발명이 된다 |
| 코드 테이블 5개 타입 · 필수 — `id` · `hospital_id` · `name` NOT NULL, 나머지 NULL, 타입은 같은 이름 칸 따라 | **받아들임(SPEC 정리 필요)** | SPEC 02 코드 표에 타입 · 필수가 없다. `name` NOT NULL 은 KOS 코드가 늘 이름을 가지므로 무리 없음. `funnel.category_id` NULL(`customer.py:141`)도 「→ funnel_category」만 적혀 있어 NULL 이 덜 위험한 쪽. SPEC 에 타입 · 필수 기록 요청 |
| 기본값 없음(bool 필수 칸 등) | **받아들임** | SPEC 에 기본값이 없다 — 넣으면 발명. 동기화 코드(#226)가 모든 필수 bool 을 직접 채워야 한다는 점을 #226 브리프에 적을 것 |
| 하위 테이블에 `hospital_id` 안 붙임(`visit_task` · `consultation` · `device` · `id_photo` · `identity_check` · `questionnaire_history` · `push_log` 등) | **받아들임(SPEC 정리 필요)** | §2 「업무 테이블에 hospital_id」 와 각 표가 어긋나지만, 표가 칸을 명시하고 부모(`visit` · `customer`)를 거쳐 병원을 알 수 있다. 붙이면 발명. 다만 `id_photo` · `questionnaire_history` 처럼 법적 검토(DAY-ESC-001) 대상은 병원 단위 조회 · 보관 정책이 나오면 다시 볼 것 |
| 최대 1,000/2,000/5,000자 CHECK 안 검 | **받아들임** | SPEC 은 KOS 한도를 설명한 것. 길이 검증은 쓰기(외부 outbox) 쪽 몫 |
| enum = PG native(linky 선례) · 열린 enum 8칸 varchar + DB 주석 | **받아들임** | 브리프 결정 2. 덤프와 migration 주석(`0002…py:301,432,898,1215,1329,1495,1673,1679`) 확인 |

## FAIL

없음.

## WARN

### W1 (중간) enum **값**을 바꿔도 `alembic check` 도 테스트도 못 잡는다 — 조용히 통과
- 직접 실험(아래): 모델 `crm_vendor` 에 값을 하나 더하고 `alembic check` → **`No new upgrade operations detected`**. alembic autogenerate 는 PG enum 라벨을 비교하지 않는다(env.py 사본 탓이 아니라 alembic 의 한계).
- migration 의 enum 목록(`0002…py:22-134`)은 `day/enums/*.py` StrEnum 과 **따로 손으로 쓴 사본**이다. 지금은 28/28 같음을 확인했지만(실 `day_dev` `pg_enum` 대조), 다음 사람이 StrEnum 에 값을 더하고 migration 을 안 쓰면 `test_upgrade_head_뒤_alembic_check_는_차이가_없다`(`test_alembic.py`)도 초록이다. 운영에서 그 값을 INSERT 하는 순간 22P02.
- 근거: AG 테스트 「migration 은 실제 PostgreSQL 로 검증」 · SPEC §3 enum 값 목록 · 브리프 결정 2 「정해진 enum 은 SPEC 값 목록 그대로 DB 에서도 막는다」.
- 고칠 방향: infra 테스트 하나 — upgrade 한 `day_test` 의 `pg_enum` 라벨(타입별, 순서 포함)을 모델 `Enum.enums` 와 비교. (또는 `alembic-postgresql-enum` 도입 — 의존성 추가라 코디 결정.)

### W2 (중간) `EncryptedJSONB` 는 민감 키라도 값이 문자열이 아니면 **평문으로 저장**한다
- `backend/common/crypto.py:77-78` — `key in sensitive_keys and isinstance(item, str)` 일 때만 암호화. 직접 확인: `{'system_password': 123456, 'open_api_key': {'k': 'secret'}}` → bind 결과가 **그대로 평문**. 오류도 로그도 없다.
- 한 겹 감싼 경우(`{'auth': {'system_password': 'pw'}}`)도 평문 — 모듈 docstring 에 적혀 있으나 막지는 않는다.
- 근거: SPEC 01 `crm_connection.config` 「암호화 JSONB · 민감 키는 최상위」 · SPEC §2 「민감 정보 암호화」 · I#225 A4.
- 고칠 방향: 민감 키의 값이 `str` 이 아니면 `TypeError`(값을 메시지에 넣지 않음). 덧붙여 최상위가 아닌 곳에 민감 키 이름이 나타나면 거절. 테스트 2개(비문자열 · 중첩).
- 참고(받아들임): `tenant_id` 평문 — SPEC 01 표에서 「내부 API 경로 · 웹 링크」로 쓰는 식별자라 비밀이 아니다. `system_email` 은 암호화 — 지나치지 않음.

### W3 (중간) 30초 `statement_timeout` 이 **migration 접속에도** 걸린다
- `backend/common/db/session.py` `connect_args` 에 `statement_timeout` 을 넣었고(`git diff` +4줄), alembic 도 같은 함수를 쓴다(`backend/migrations/env.py:97`). 이번 리비전은 빈 테이블이라 무해하지만, 데이터가 쌓인 뒤 인덱스 생성 · 칸 타입 변경 · 백필 리비전이 30초에서 57014 로 끊긴다(prod 첫 적용 때 발견하게 된다).
- 근거: R224 W6 의 목적은 **서비스 쿼리** 상한. AG 백엔드 안전 「timeout 을 명시」 — 용도별로.
- 고칠 방향: env.py 는 `statement_timeout` 을 빼거나 따로(`MIGRATION_STATEMENT_TIMEOUT_MS`, 기본 0 = 없음) + `lock_timeout` 을 짧게(잠금 대기로 운영을 막지 않게).

### W4 (낮음) 대조 스크립트가 레포 밖이고, 「모델에만 있는 칸」을 실패로 세지 않는다
- 스크립트 `:181-187` — 위 표. SPEC 경로가 절대경로(`:20-21`)라 레포 테스트로 둘 수 없는 것은 이해하지만, 그러면 A1 을 지키는 회귀가 `test_모델은_SPEC_1차_51_테이블과_같다`(테이블 **이름**만, `test_models.py:54-56`)뿐이다.
- 고칠 방향: 스크립트에서 `extra`(§2 `deleted_at` 예외 목록 제외)를 `bad` 에 넣는다. 레포에는 칸 이름 스냅샷(테이블 → 칸 목록) 테스트를 둬서 칸이 조용히 늘거나 빠지는 것을 막는다.

### W5 (낮음 · R224 W8 이 커짐) offline `--sql` 출력은 스키마를 만들지도 고르지도 않는다
- 직접 확인: `upgrade head --sql` 에 `CREATE SCHEMA` · `SET search_path` 가 없다. 이제 `CREATE TYPE` 28 · `CREATE TABLE` 51 이 **스키마 없이** 나오는데 `alembic_version` 만 `day_dev.` 로 한정된다 → DBA 가 기본 search_path(`public`)로 돌리면 **테이블은 public, 버전 기록은 day_dev** 로 갈라진다.
- `backend/migrations/env.py:107-108`. 근거: SPEC §2 「스키마 이름은 env」 · 시스템 결정 7(관리형 DB · 스키마별 계정).
- 고칠 방향: offline 분기 맨 앞에 `CREATE SCHEMA IF NOT EXISTS <SCHEMA>` + `SET search_path TO <SCHEMA>, public` 출력. prod 배포 Delivery 전에 필수.

### W6 (낮음) alembic 이 `ENCRYPTION_KEY` 없이는 돌지 않는다
- `backend/common/config.py:48` 필수 칸이고 env.py 가 `get_settings()` 를 부르므로, 암호화와 무관한 migration 도 키가 있어야 한다(리포트 「compose migrate 포함 기동 실패」). prod 에서 migration 을 돌리는 사람 · 파이프라인에 데이터 키가 퍼진다.
- 고칠 방향: 키 검사를 「암호화 칸을 처음 쓸 때」(`common/crypto._fernet`) 또는 api · worker 기동 시점으로 옮기고, alembic 은 DB 설정만 읽게. 브리프 결정 5 「키가 없으면 기동 실패」는 api · worker 로 충분히 지켜진다 — 코디 판단.

### W7 (낮음) 키는 형식만 검사한다 — 틀린(다른) 키로는 뜨고, 첫 읽기에서 터진다
- `config.py:66` `_key_is_fernet` 은 형식만 본다. 다른 환경 키를 잘못 넣으면 api 는 정상 기동하고 민감 칸을 읽는 요청마다 `DecryptionError`(평문을 돌려주지 않는 것은 맞다 — `crypto.py` · `test_encryption.py:98-113`).
- 고칠 방향(제안 · 범위 밖 가능): 기동 때 알려진 행 하나를 풀어 보는 canary, 또는 `/health/ready` 항목. 다음 Delivery 몫.

### W8 (낮음 · R224 W5 그대로) 공용 Redis 클라이언트 timeout 이 헬스 timeout(2초)
- `backend/common/redis.py:24-26`. #226(잠금 · pub/sub) 착수 전에 분리. 이번 범위 밖 — 기록만.

## 「조용히 통과하는 자리」 (따로 모음)

1. **enum 값 추가** — W1. `alembic check` · 전 테스트 초록, 운영 INSERT 에서 실패.
2. **JSONB 민감 키의 비문자열 값** — W2. 암호화 테스트(`test_encryption.py:45-69`)는 문자열 값만 넣어 초록.
3. **대조 스크립트의 「모델에만」** — W4. 칸이 늘어도 「불일치 0」.
4. **offline SQL** — W5. rc 0 · `CREATE TABLE 52` 로 성공처럼 보인다.
5. **UNIQUE 와 소프트 딜리트**(코디 · SPEC 질문) — `customer(hospital_id, chart_number)`(`customer.py:25`) · `external_ref` 4칸(`:85`) · `brand.code` · `device.install_id` 는 `deleted_at` 이 찬 행도 막는다. 외부에서 지워진 고객의 차트번호를 KOS 가 다시 쓰면 동기화 INSERT 가 23505 로 실패한다. SPEC 은 「유일」만 적었으니 지금 코드는 SPEC 대로다 — 부분 유일(`WHERE deleted_at IS NULL`)로 할지 SPEC 결정이 필요(#226 동기화 전에).
6. **`chat_room.direct_key` 전역 UNIQUE**(`misc.py:196`) — SPEC 07 대로 전역이지만 키가 「account id 쌍」이고 계정은 여러 병원에 속한다(SPEC 04). 같은 두 계정이 다른 병원에서 1:1 방을 못 연다. SPEC 질문(07 은 OQ-07-3 칸 단위 검토 전).
7. 병원 경계 FK 없음 — `visit.room_id` 가 다른 병원의 방을 가리켜도 DB 는 막지 않는다(단일 칸 FK). SPEC 에 없는 제약이라 지금은 서비스 몫 — 참고.
8. `updated_at` 은 ORM `onupdate` 만(`_columns.py`) — raw SQL UPDATE 는 시각을 안 바꾼다. 서비스가 ORM 을 쓰는 한 무해 — 참고.

## migration 점검 (브리프 「볼 것」 3)

| 항목 | 결과 | 근거 |
|---|---|---|
| 스키마 이름 없는 리비전 → dev/prod 같은 결과 | PASS | `0002…py` 에 `schema=` · `day_dev` 0건(grep). 스크래치 `day_rv225` 에 upgrade → 테이블 52 · enum 28 모두 그 스키마, `public` 테이블 0 · FK 정의가 `day_rv225.x` 를 가리킴 |
| enum 공유 타입 생성 · 삭제 순서 | PASS | `create_type=False` 로 한 번 정의, upgrade 처음 `create`(`:168-170`) · downgrade 끝 `reversed` drop(`:1977-1979`). `crm_vendor` 4곳 · `flow_step` · `procedure_kind` · `option_type` 2곳이 타입 하나를 공유 |
| 순환 FK | PASS | `chat_message.attachment_id ↔ chat_attachment.message_id` — 테이블 뒤 `create_foreign_key`(`:1910`) · downgrade 처음 `drop_constraint`(`:1920`) |
| downgrade 깨끗함 | PASS | downgrade base 뒤 스키마에 `alembic_version` 과 그 PK 인덱스(2개)만, enum 타입 0 |
| 리비전이 앱 코드를 import 하지 않음 | PASS | import = `collections.abc` · `sqlalchemy` · `alembic` · `postgresql` 뿐(`:8-12`). 암호화 칸은 TEXT · JSONB |
| `alembic check` = 0 (모델 == migration) | PASS(enum 값 제외 — W1) | 아래 실험 `none` |

## 직접 실험 — env.py autogenerate 사본이 진짜 차이를 잡나

방법: 저장소 파일은 건드리지 않았다. 스크래치 스크립트가 같은 프로세스에서 `day.models` 를 import 한 뒤 **메모리의 `Base.metadata` 만 바꾸고** `alembic.config.main(["check"])` 를 불렀다(env.py 는 같은 모듈 객체를 읽는다). DB = 로컬 compose, 스크래치 스키마 `day_rv225`(upgrade head 뒤, 끝나고 DROP).

| 바꾼 것 | `alembic check` |
|---|---|
| 없음 | No new upgrade operations detected (정상) |
| 칸 추가 `brand.extra` | **잡음** — add_column |
| 타입 `hospital.name` varchar(100) → (200) | **잡음** — modify_type |
| 타입 `zone.sort_order` int → bigint | **잡음** |
| NULL 허용 `customer.name` | **잡음** — modify_nullable |
| FK 대상 `visit_task.room_id` room → zone | **잡음** — remove_fk + add_fk |
| FK 제거 | **잡음** — remove_fk |
| 새 enum 타입(varchar → enum) `customer.gender` | **잡음** — modify_type |
| **enum 값 추가** `crm_vendor` + `newvendor` | **못 잡음** — No new upgrade operations (W1) |
| UNIQUE 추가 · 인덱스 추가 · 서버 기본값 추가 | **잡음** |

덧: FK 를 `ForeignKey("<스키마>.zone.id")` 처럼 스키마를 붙여 쓰면 사본 만들기에서 `NoReferencedTableError` 로 check 가 깨진다(첫 시도에서 확인). 모델은 전부 스키마 없이 쓰므로(`_columns.py` `fk()` docstring) 지금은 무해 — #226 이후 모델 작성 규칙으로 `_columns.fk()` 만 쓰도록 하면 된다(참고).

결론: env.py 사본 수정은 **맞다** — 리포트의 원인 설명(기본 스키마가 `None` 으로 넘어옴 · FK 참조 스키마 불일치)과 수정이 실험과 맞고, enum 값만 alembic 자체 한계로 빠진다.

## 테스트 점검 (브리프 「볼 것」 6)

- `day_dev` 를 안 건드림: `tests/conftest.py` 가 어떤 import 보다 먼저 `DB_SCHEMA=day_test`(R224 W1 해결) · `tests/day/conftest.py` 가 `assert get_settings().db_schema == TEST_SCHEMA` 뒤 `day_test` 만 DROP/CREATE. 테스트 실행 전후 `day_dev` = 테이블 52 · enum 28 · `alembic_version 0002_data_model` 그대로, 남은 `day_test*` 스키마 0.
- 제약 테스트는 진짜 DB 위반을 본다(23505 · 22P02 · 23502 sqlstate). 다만 enum · NOT NULL 은 표본 1개씩(`crm_vendor` · `customer.name`) — `alembic check` 가 모델 == DB 를 보장하므로 표본으로 충분하되, enum **값**은 W1.
- skip: `uv run pytest -q` → 45 passed · 35 skipped(exit 0), `scripts/test.sh` 는 `DAY_REQUIRE_INFRA=1` 로 skip 대신 실패(`tests/test_infra_guard.py`) — R224 W4 해결. CI 가 생기면 `scripts/test.sh` 만 쓰라는 AG 실행 명령 주석도 있음.
- 고정 스키마 `day_test` — 같은 로컬 compose 를 두 워크트리가 동시에 쓰면 서로 DROP 한다. 참고(낮음).

## R224 W 처리 현황

| R224 | 처리 |
|---|---|
| W1 테스트 기본 스키마 · Base 동결 | 해결 — conftest `DB_SCHEMA=day_test` 선행 · `day_test` 세션 fixture |
| W2 Base 위치 | 해결 — `day/db.py` · `common/db/model_base.make_metadata` |
| W3 태스크 등록 | 해결 — taskiq CLI 모듈 인자 `day.tasks`(compose `:103,107` · AG 계층 규칙 마지막 줄) |
| W4 조용한 skip | 해결 — `DAY_REQUIRE_INFRA` |
| W5 Redis timeout | 남음 → 이 리포트 W8 |
| W6 DB 쿼리 timeout | 해결(statement_timeout) — 단 migration 에도 걸림 → W3 |
| W7 migrations 예외 범위 | 해결 — `migrations/env.py` → `day.db` · `day.models` 만 |
| W8 offline SQL | 남음 · 커짐 → W5 |
| W9 `.dockerignore` | 해결(`ec2a2681`). worker 의 migrate 의존은 #226 몫 |

## 코디가 확인할 것 (범위 · 권한)

- 브리프 §5 allowed_paths 에 없는 `backend/migrations/env.py` · `deploy/compose.local.yaml` 이 바뀌었다. 리포트는 「코디 허용」이라 적었다 — 허용 기록이 있으면 PASS, 없으면 rules.md 「allowed_paths 이탈 = FAIL」. 변경 내용 자체는 필요하고 맞다(env.py 는 위 실험으로 검증, compose 는 `ENCRYPTION_KEY` 한 줄).

## 직원이 실물에서 만날 자리

화면 없음. 운영에서 만날 자리는 「조용히 통과하는 자리」 5(지워진 고객의 차트번호 재사용 → 동기화 실패)뿐 — #226 전에 SPEC 결정.

## 직접 돌린 명령과 수치

| 명령 | 결과 |
|---|---|
| `lsof` 11040 · 11042 · 11043 | 비어 있음. 사용자 컨테이너 손대지 않음 |
| `uv run ruff check backend` | All checks passed! |
| `uv run pytest -q` (인프라 없이) | **45 passed, 35 skipped** in 1.06s |
| compose `up -d --wait postgres redis` → `scripts/test.sh -q` | **80 passed** in 7.41s |
| 모델 덤프(스크래치 `dump.py`) | 51 테이블 · 619 줄 — SPEC 03 ~ 07 전수 대조, 차이 0 |
| 스크래치 스키마 `day_rv225`: upgrade head → 실험 12건 → downgrade base → upgrade → downgrade 0001 | 전부 rc 0 · 실험 결과 위 표 · downgrade 뒤 relation 2(버전 테이블 · PK) · enum 0 |
| `pg_namespace` · `pg_class` · `pg_type` | `public` 테이블 0 · `day_rv225` 52/28 · `day_dev` 52/28(변화 없음) · ON DELETE 비기본 FK 0 |
| `day_dev` `pg_enum` ↔ 모델 Enum | 28 타입 · 불일치 0 |
| `upgrade head --sql` | `CREATE SCHEMA` · `search_path` 없음, `CREATE TYPE` 스키마 없음(W5) |
| `EncryptedJSONB.process_bind_param` 비문자열 · 중첩 | 평문 그대로(W2) |
| 정리 | `DROP SCHEMA day_rv225` · compose `down`(볼륨 남김) · DB 에 `day_dev` 만 |

## 권장 처리 순서

1. 이 PR 안: **W1**(pg_enum ↔ 모델 테스트) · **W2**(비문자열 민감 값 거절) · **W3**(migration 의 statement_timeout 분리).
2. 코디 결정: W6(alembic 의 키 요구) · allowed_paths 허용 확인 · SPEC 질문 3개(UNIQUE 와 소프트 딜리트 · `direct_key` 범위 · 코드 테이블 타입/필수 · `deleted_at` 3 문장).
3. prod 배포 Delivery 전: W5(offline SQL) · W7(키 canary).
4. #226 브리프: W8(Redis timeout) · 필수 bool 을 동기화가 전부 채울 것 · UNIQUE/소프트 딜리트 결정 반영.
