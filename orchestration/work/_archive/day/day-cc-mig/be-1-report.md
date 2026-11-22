# day-cc-mig backend 1단계 결과 보고 — #264 KOS 키 전부 담는 테이블 보충(0012 · 매퍼 · 기존 행 업데이트)

## 상태: done (코드 · 테스트 · A3 · A5 DEMO 실물 완료)

- 워크트리 `CENTURION_DAY/day-cc-mig` · 브랜치 `kknaksss/day-cc-mig` · base `origin/dev` `844eace4`(시작 때 fetch — 나아가지 않음). 커밋 · push · PR 없음.
- 계약: DAY-SPEC-000 §4A(mediness PR #954 · 1944f922) · Delivery #264 D-1 ~ D-5 · A1 ~ A7.

## 1. 수행 — 파일

새 파일(14)
- `backend/migrations/versions/20261120_0012_kos_keys.py` — 0011 을 잇는다(head 하나)
- `backend/day/models/_snapshot.py` — 시술 항목 스냅샷(TI 묶음 16칸) mixin
- `backend/day/emr/kos/mapper_kos_keys.py` · `mapper_kos_keys_hospital.py` · `mapper_kos_keys_sale.py` — KOS 응답 → 「더할 칸」
- `backend/day/emr/kos/hospital_reads.py` — 병원 설정 읽기(P22 · P25 · P26 · P27 · #30 · #32 · #33)
- `backend/day/emr/sync_kos_keys.py` · `sync_kos_keys_hospital.py` — 반영(바뀐 칸만 · 배열 행 · 약품 · 기기 참조 행 · 병원 설정)
- `backend/day/services/emr_kos_keys.py` — 회차 뒤 따로 반영(`apply_isolated`) · 새 단계 `run_hospital`(잠금 `kos_keys`)
- `backend/day/services/emr_kos_keys_backfill.py` — 기존 행 업데이트(`--stage kos_keys`)
- 테스트: `tests/migrations/test_kos_keys_migration.py` · `tests/day/column_snapshot_kos_keys_data.py` · `tests/day/emr/test_kos_keys_mapper.py` · `test_kos_keys_sync.py` · `test_kos_keys_isolation.py` · `test_kos_keys_backfill.py`

고친 파일(35 · 더하기만)
- 모델: `models/{__init__,hospital,room,customer,staff,visit,task,menu,purchase,ticket,prepaid_card}.py` — 새 칸 · 새 표(지금 칸 줄 삭제 · 변경 0 — 아래 §3 증거)
- enum: `enums/{task,visit,room,external_ref}.py` — 새 DAY enum 9 · `KosKeyEntityType`(external_ref 새 값 5)
- **`backend/day/identifiers.py`(allowed_paths 밖 · 코디 허용)** — 새 표 id NewType 10줄만 추가(구조 검사 `model_violations` 가 요구)
- emr: `base.py`(`fetch_hospital_settings` 기본 None) · `normalized.py`(§4A 우리 형식 + 묶음 칸 `kos_keys`) · `normalized_sale.py`(`kos_keys` · `oldest_last_visited_at`) · `kos/__init__.py`(같은 응답으로 `kos_keys` · 호출 수 그대로) · `kos/sale_reads.py`(같음) · `kos/client.py`(`outside_tenant` — 테넌트 밖 읽기 1개) · `kos/mapper_sale_values.py`(**`CARD → card`**)
- 서비스 · 태스크: `services/emr_sync.py`(RunResult 에 `kos_keys` · `vendor` 만 더함 · Job `kos_keys`) · `services/emr_sale_sync.py`(같음) · `services/emr_backfill.py`(`kos_keys` 단계 — `all` 에 안 듦) · `tasks/emr.py`(회차 **뒤** 따로 반영 + 새 단계) · `runtime/backfill.py`(`--stage kos_keys`)
- 기존 테스트(의도된 변경 반영): `test_alembic.py`(HEAD 0012) · `test_column_snapshot.py` · `test_models.py` · `test_constraints.py`(부분 유일 5 · DB 로 23505 확인) · `test_enum_labels.py`(49 · 빈 enum 2) · `test_kos_sale_mapper.py`(CARD) · `test_sale_sync_rules.py`(쓰기 행 = 지금 칸 · §4A 칸 제외)

## 2. 구조 — 지금 회차를 멈추지 않는 방법(상용 서비스 중)

| 장치 | 내용 |
|---|---|
| 같은 응답 · KOS 호출 0 추가 | 일정 · 기준 정보 · 메뉴 · 구매 · 시술권 · 카드 읽기가 **이미 받은 응답**에서 `kos_keys` 를 더 만든다. 지금 매퍼 · 지금 우리 형식 필드 · 반환값 그대로(새 필드는 기본값 있는 꼬리 칸) |
| 매핑 실패 격리 | `safe_kos_keys` — 어떤 예외든 빈 묶음 + 경고(오류 이름만). 테스트: 일정 묶음 만들기를 일부러 깨도 `visits` · `sales` 같음 |
| 반영 격리 | 지금 회차가 **반영 · commit · 신호 · 발행까지 끝난 뒤** 태스크가 `apply_isolated` — 다른 transaction · 다른 상한(30초) · 자기 잠금(`kos_keys_apply:<이름>`) · 모든 예외 · 시간 초과를 로그만. 회차 status · counts · 「동기화 멈춤」 표시 그대로 |
| 쓰는 칸 분리 | 지금 반영의 upsert 칸 목록(`dtos/*_rows`)에 §4A 칸이 없다 → 서로 덮지 않음(`test_sale_sync_rules` 가 고정) |
| 새 단계 | 병원 설정 = 기준 정보 태스크에서 메뉴 뒤 `_isolated("kos_keys", run_hospital)` — 잠금 `kos_keys` · 상한 = 메뉴와 같은 TTL · 부분마다 따로 실패 |
| 물리 DELETE 0 | 새 동기화 7파일 AST · 문자열 검사 테스트 · 빠진 배열 행 · 휴무 · 규칙은 `deleted_at` |

## 3. 계약 대조 — §4A 칸 → 코드(표별 칸 수 · 빠진 칸 0)

칸 이름은 `tests/day/column_snapshot_kos_keys_data.py`(새 12표 전체 칸 + 지금 23표에 더한 칸)에 고정 — 모델과 독립된 기대값 · `test_column_snapshot` 이 대조.

**지금 표에 더한 칸(23표 · 180칸 · 모두 NULL 허용 · 기본값 없음 — `test_KOS_키_보충은_지금_표에_칸을_더하기만_한다` · `test_0012_가_지금_테이블에_더하는_칸은_모두_null_허용이고_기본값이_없다`)**

| 표(prod/dev) | SPEC §4A 새 칸 | 모델 · 0012 | 채우는 곳 |
|---|---|---|---|
| hospital(prod) | 19 | 19 | P25 · 기준 정보 새 단계 |
| crm_connection(prod) | 1 `tenant_info` | 1 | P22(시스템 계정 · 그 테넌트 행 4키) |
| reservation_group(prod) | 3 | 3 | P03(기준 정보) |
| customer(prod) | 8 새 칸(+ 「동기화로 채움」 23키) | 8 | P20 목록(1시간 단계 · 업데이트) |
| visit(prod) | 6 | 6 | 일정(10초) |
| visit_requested_procedure(prod) | 2 + TI 17 = 19 | 19 | 일정 |
| staff(prod) | 2(+ 채움 `default_zone_id` · `account_id` · `created_at` · 외부 수정 시각) | 2 | P05 |
| job_role(prod) | 1 | 1 | P04 |
| visit_task(prod) | 15 | 15 | 일정 |
| product_option · composition · price · etc_task_type · prepaid_card_product · etcetera_product(dev) | 3 · 5 · 8 · 1 · 3 · 2 | 같음 | 메뉴 |
| purchase · purchase_item · purchase_transaction(dev) | 1 · 40(통화 8 · 옵션 4 · TI 17 · 선불 8 · 시술 외 2 · 번역 1) · 10 | 같음 | 구매 |
| ticket_bundle · ticket_set · ticket(dev) | 5 · 17(TI 16 + 번역) · 2 | 같음 | 시술권 |
| prepaid_card · prepaid_card_ledger(dev) | 8 · 1 | 같음 | 카드 · 이력 |

**새 표 12** — `hospital_operation_timetable`(10칸 · PK 병원+요일) · `hospital_day_off`(7) · `reservation_group_day_off`(7) · `reservation_rule`(13) · `reservation_rule_component`(9) · `reservation_rule_event`(9) · `customer_line_account`(9) · `visit_requested_procedure_composition`(23) · `visit_etc_work`(10) · `visit_etc_work_staff`(5 · PK) · `purchase_item_composition`(35) · `medicine_machine_ref`(12). 모두 `deleted_at` · 유일은 살아 있는 행만(부분 유일 5 · `uq_visit_requested_procedure_composition_parent_sort_order` 는 63자 제한으로 줄인 이름).

**새 enum 9**(관찰 값만 · OQ-4A-9): `task_urgency_level{unspecified}` · `etc_work_status{waiting, completed}` · `price_reason{general}` · `reservation_occupancy_policy{all_matched_sequential}` · `reservation_zone_occupancy_policy{single_zone_only}` · `requested_procedure_repetition{}` · `reservation_rule_event_type{}`(값 미관찰 → **빈 enum** · 늘 null + 경고) · `medicine_machine_owner_type{9 표}` · `medicine_machine_kind{medicine, machine}`. 기존 `weekday` · `option_type` 은 재사용(만들지 · 지우지 않음). TI 묶음의 상태 · 단위 · 급여 · 과세는 원본 `treatment_item` 과 같은 **열린 문자열 칸**(§4A.0 「같은 enum · 같은 매핑」).

**external_ref.entity_type 새 값**: `hospital`(entity_id = 그 병원 · KOS `hospitalId`) · `hospital_day_off` · `reservation_group_day_off` · `reservation_rule` · `visit_etc_work`(외부 id = 일정 id + `:` + sequence).

**지금 칸 변경 0 증거(A2)**: `git diff backend/day/models backend/migrations` 의 지운 줄은 import · 모듈 설명 · class 머리줄(mixin 추가) 뿐 — 칸 줄 삭제 · 타입 변경 0. 0012 upgrade 에 `drop_` · `alter_column` · `op.execute` · 데이터 이동 0(테스트). `alembic check` 차이 0.

**규칙별**
| 규칙 | 구현 |
|---|---|
| 목록 밖 KOS 값 = 행 유지 · 칸 null · 경고 1줄(A4) | `Extra.enum` → 값 None + `warnings`「칸=KOS 원래 문자열」 · 반영이 `emr kos value outside list hospital=<id> <표>.<칸>=<값>` 한 줄(같은 줄은 한 번). 실 DB 테스트: 표 밖 긴급도 → 작업 행 그대로 · `urgency_level` null · 경고 1줄 |
| CARD | `PAYMENT_TYPES` 에 `CARD → card` · `cardConfiguration` 은 지금처럼 `…Id` 키만 빼고 `payment_config` |
| `created_at` ← KOS 생성 시각 | 고객 · 직원(`createdAt`) · 상담 기록 · 구매 · 거래 · 티켓 · 카드 · 예약 규칙 |
| 금액마다 통화 · 번역 jsonb | §4A 그대로(빈 번역 객체는 null) |
| TI 묶음 · 약품 · 기기 id | TI 16칸(+`treatment_item_id`) · `medicine_machine_ref` 행(작업 · 희망 시술 · 구성 · 구매 항목 · 구매 구성 · 시술권 세트 · 상품 · 옵션 · 메뉴 구성) |
| 키 없음 = 건드리지 않음 | 같은 행이 키가 다른 응답(P07 목록 · P08 상세)에서 온다 — 키가 **있을 때만** 칸을 싣는다(빈 값 = 비움). 단건 전체 응답(P25 · 기타 업무 · 규칙 구성 · 이력)은 빠진 키 = 비움(OQ-4A-3 기본값) |
| 암호화(주민 · 외국인등록 · 여권) | 칸 타입 `EncryptedText` 가 저장 때 암호화(DEMO 실물에서 `enc:` 아닌 값 0 확인 항목) |
| 고객 칸 원천 회차(D-4 · OQ-4A-14) | **선택: 1시간 단계에서 `get-visitors`(P20 · 63키 = 단건과 같은 키) 를 최근 방문 순으로 오늘 0시 전 고객이 나올 때까지 · 상한 5장(100명)** — 고객마다 단건(P24)을 부르지 않는다. DAY 에 없는 고객은 만들지 않는다. 지난 고객은 업데이트 단계가 전 장을 돈다 |
| 병원 휴무(OQ-4A-2) | 빈 배열 → 아무것도 안 씀. 값이 오면 `{id, startDateTime, endDateTime}` 로 받고 모르는 키 · id 없음은 경고(키 이름만). 그룹 휴무는 그룹마다 따로 묻는다(응답 행에 그룹 id 가 없을 수 있어서) · 창(오늘-1일 ~ +90일) 안에서 빠진 휴무만 지움 표시 |

## 4. 검증 — 명령과 수치

| 명령 | 결과 |
|---|---|
| 버리는 PG16(로컬 컨테이너 · 사용자 포트 아님)에서 `alembic upgrade head → check → downgrade 0011 → upgrade head → heads` | 차이 0 · 왕복 성공 · `0012_kos_keys (head)` 하나(A1) |
| `./scripts/test.sh -q backend/tests/day/emr/test_kos_keys_sync.py` | **7 passed** |
| `./scripts/test.sh -q backend/tests/day/emr/test_kos_keys_backfill.py` | **4 passed** |
| `./scripts/test.sh --pure -q` 새 파일(mapper · isolation · migration) | **40 passed** |
| `./scripts/test.sh -q`(전체 · 격리 PG · Redis · 시술현황 판 포함) | **1931 passed**(A6) |
| `./scripts/test.sh --pure -q` | **1535 passed** · 396 deselected |
| `./scripts/check.sh --pure` | 구조 · Jinja · ruff · format · mypy(strict) · Taut audit/check **통과** · frontend 단계만 실패(`@tailwindcss/postcss` 미설치 — npm 의존성 · 무관 · 앞 작업과 같음) |

테스트가 덮는 것: 일정 한 건 → 방문 · 작업 · 상담 · 희망 시술(+구성) · 기타 업무 칸 · 목록 응답에 없는 키는 안 건드림 · 표 밖 긴급도 = null + 경고 1줄(실 DB · 로그) · 참조 못 찾으면 FK 비움 · **다시 돌리면 쓴 행 0** · 빠진 구성 · 기타 업무 = 소프트 딜리트(행 수 그대로) · DAY 에 없는 행은 만들지 않고 셈 · 메뉴 · 구매 · 시술권 · 카드 칸 + 다시 0 · CARD 매핑 · 모르는 결제 수단은 여전히 그 거래를 뺌(OQ-4A-1) · 병원 설정(요일 7 · 일요일 꺼짐 · `external_ref(hospital)` entity_id = 병원 · 휴무 · 다시 0 · 창 안 빠진 휴무 지움 · 받지 못한 부분은 안 건드림) · 칸 보충 실패 · DB 실패해도 예외 없음 · 묶음 만들기 실패해도 일정 매핑 같음 · 물리 DELETE 0 · **업데이트 드라이런 = DB 쓰기 0 · 진행 위치 안 씀 → 실행 = 칸 채워짐 → 다시 = 쓴 행 0 · 이어 받기 = KOS 0 호출** · 부분 유일 5 는 DB 23505.

## 5. DEMO 실물(A3 · A5) — 완료

방식: 로컬 · 버리는 PG16 · Redis7 컨테이너(임의 포트 · 끝나고 지움 · 남은 컨테이너 0) · 새 스키마에 0012 까지 migration · **사용자 테스트 계정**(`kos-test-account.env` · 값 출력 안 함)을 시스템 계정으로 · `get-user-tenants` 2개 중 `hospitalName` 에 DEMO 가 든 1개만 · `KOS_CLIENT_TAG=local` · 공개 API 0 · 실 명동점 0 · 사용자 포트 · 프로세스 안 건드림. 출력은 건수만.

**KOS 세션(코디 · 사용자 허락)**: 시작 때 테스트 계정 활성 로그인 5개(우리 표시 0) → 기기 제한. **가장 오래된 2개 해제 — 둘 다 UA 끝 `(dev)`**(dev 서버 worker 표시 · worker 는 다음 회차에 다시 sign-in). 끝에 우리 것 정리: `(local)` 2개 해제(실물 스크립트의 직원 로그인 · 시스템 클라이언트) · 백필은 실행마다 자기 `(backfill)` 1개씩 해제(4회) · 마지막 확인 활성 3 · `(local)` · `(backfill)` 남은 것 0.

**A3 — 동기화 한 회차(기준 정보 → 메뉴 → 병원 설정 · 오늘 고객 → 오늘 일정 → 오늘 구매 · 각각 회차 뒤 칸 보충)** · 새 칸 · 새 표 건수(0 에서):

| 묶음 | 건수 |
|---|---|
| 병원 | `registered_name` 등 채움 · `crm_connection.tenant_info` 1 · `external_ref(hospital)` 1 · 기본 운영 시간 7(꺼진 요일 0) · 특별 휴무 0 · 그룹 휴무 0(데모 빈 배열 — 아무것도 안 씀) · 예약 규칙 2 · 구성 4 · 이력 19 |
| 기준 정보 | 예약 그룹 `is_default` · `start_at` 13/13 · 직원 `mfa_methods` 83/83 · 직무 `feature_list` 14 |
| 고객(1시간 단계 · 1장) | DAY 고객 8명 중 `registered_at` · `is_new` · 동의 8/8 · `language` 7 |
| 일정 | 방문 12 · `reservation_group_id` 12/12 · 일정 상담 정보 상담사 3 · 작업 42 · `urgency_level` 42/42 · `product_option_id` 35 · 번역 42 · 희망 시술 2(TI 1) · 구성 스냅샷 2 · 약품 · 기기 참조 행 599(FK 찾음 599) |
| 구매 · 시술권 · 카드 | 구매 37 · 대표 담당 37 · 항목 39 · 통화 39 · TI 35 · 구매 구성 4 · 거래 35 · 통화 35 · 번들 32 · 세트 TI 32 · 티켓 가격 32 · 카드 총액 2 · 이력 통화 5 |
| 메뉴 | 옵션 분해 통화 8 · 기타 작업 번역 4 |

같은 회차를 **한 번 더**: 보충 쓴 행 = 일정 · 메뉴 · 구매 0 · 병원 0 — 단 `external_ref.external_updated_at` 이 매 회차 다시 쓰인다(직원 83 · 상담 3 · 고객 8 — §7-10).

**A4 실물** — 표 밖 값 경고(행은 받고 칸만 null)가 실제로 나왔다: `reservation_rule.requested_procedure_repetition=ONCE_PER_RESERVATION` · `reservation_rule_component.…=ONCE_PER_RESERVATION` · `reservation_rule_event.event_type=protos.schedule.{ReservationRuleCreatedEvent, ReservationRuleActivatedEvent, ReservationRuleDeactivatedEvent, ReservationRuleRuleSetChangedEvent, DefaultReservationRuleSetEvent}`(값 미관찰 enum 의 **첫 실값** — OQ-4A-9 값 추가 migration 재료).

**A5 — 기존 행 업데이트** · 먼저 지난 백필(`--from 2026-10` · 지금 칸만 · 582 호출 · 9분 47초)로 지난 행을 넣은 뒤:

| | 드라이런 | 실행 | 다시 실행 |
|---|---|---|---|
| KOS 호출 · 소요 | 652 · 650초 | 652 · 652초 | 652 · 654초 |
| 받은(더할 칸이 있는) 행 | 5,064 | 5,064 | 5,064 |
| **쓴 행** | **0** | **6,126** | **0** |
| DB 건수 스냅샷(56 항목) | 실행 전과 **같음** | 아래 | 실행 뒤와 **같음** |
| 진행 위치(Redis) | 안 씀 | 씀 | 씀 |

실행이 채운 것(지난 행 · 백필 뒤 → 업데이트 뒤): 방문 `reservation_group_id` 12 → 497/497 · 일정 상담 정보 상담사 3 → 53 · 작업 `urgency_level` 42 → 757/761 · `product_option_id` 35 → 592 · 기타 업무 0 → 18(담당 6) · 희망 시술 TI 1 → 10 · 구성 2 → 4 · 고객 `registered_at` · `is_new` · 동의 8 → 391/391 · `language` 7 → 131 · **여권번호 6(전부 `enc:` · 평문 0)** · 구매 대표 담당 37 → 448/448 · 항목 통화 39 → 490/490 · 항목 TI 35 → 452 · 구매 구성 4 → 56 · 거래 통화 35 → 428/428 · 번들 통화 32 → 423 · 세트 TI 32 → 438 · 티켓 가격 32 → 450 · 카드 총액 2 → 14 · 이력 통화 5 → 32 · 약품 · 기기 참조 행 599 → 2,022(FK 전부 찾음). 쓴 행 내역: visit 485 · visit_task 719 · consultation 55 · customer 383 · purchase 411 · purchase_item 451 · purchase_transaction 393 · ticket_bundle 391 · ticket_set 406 · ticket 418 · prepaid_card 12 · ledger 27 · 새 표(구성 54 · 기타 업무 24 · 참조 행 1,423) · external_ref 464.

- 셈만 한 것: DAY 에 없는 고객 179(고객 목록에만 있는 고객 — 만들지 않음) · 지금 매퍼가 뺀 번들 · 세트 · 티켓 10 · 11 · 15 · 직원 `account_id` 83 못 찾음(DAY 에 로그인한 적 없는 계정 — 지금처럼 로그인 때 잇는다) · 수가 유형 1 못 찾음.
- **CARD 실물**: 지난 백필에서 카드 거래 1건이 `card` 로 들어왔다(전에는 표 밖이라 빠지던 행).


## 6. dev 서버 실제 업데이트 방법(실행은 코디 · 서버)

dev 배포(0012 적용) 뒤, dev VM(`ssh day-vm`)의 dev api 컨테이너 안. 접속 값은 컨테이너 앱 설정 · KOS 접속값은 그 병원 `crm_connection`(명령줄로 받지 않음).

```sh
# 0) 병원 id · 연결 · 기준 정보가 한 번 돈 병원인지(아니면 종료 1). 0012 가 먼저 적용돼 있어야 한다
# 1) 드라이런 — KOS 만 읽고 DB 쓰기 0 · 받은 행 수 · 호출 수 · 시간
docker exec day-dev-api-1 python -m runtime.backfill --hospital <병원 uuid> --from 2026-08 --stage kos_keys --dry-run
# 2) 실제 — 길어서 tmux / nohup
nohup docker exec day-dev-api-1 python -m runtime.backfill --hospital <병원 uuid> --from 2026-08 --stage kos_keys \
  > ~/kos-keys-$(date +%Y%m%d-%H%M).log 2>&1 &
# 3) 끊기면 같은 인자 + --resume(끝난 부분 · 달 · 고객 장 · 순번부터)
# 4) 한 번 더 — 「kos_keys: 씀=0」 확인(멱등)
```

- 순서(한 실행 안): ① 병원 설정 · 기준 정보 · 메뉴 칸 → ② 고객 목록 전 장 → ③ 달마다 일정 → ④ 그 달 구매 → ⑤ 구매가 있는 고객의 시술권 → ⑥ DAY 고객의 카드 · 카드 이력. 지금 칸 · 지금 행은 쓰지 않는다(§4A 칸만) — 그래서 다시 돌리면 씀 0.
- **예상 호출 · 시간(1초 1회)**: ① 약 30 + 그룹 수 + 규칙 수 · ② 고객 수 ÷ 20 · ③ 달 수 · ④ 구매 수 ÷ 80 · ⑤ 구매 고객 수 · ⑥ 고객 수 ÷ 20 + DAY 고객 수 + 카드 수. 데모 크기(고객 ~560 · 구매 고객 ~140 · 카드 ~15 · 4달)면 약 **800 호출 ≈ 14분**. 고객 1만 병원이면 약 3시간(⑥ 고객마다 카드 요약 1회가 대부분).
- 표시 `backfill` 세션 — 끝나면 자기 로그인만 해제(운영 worker `dev` 세션 안 건드림). 시스템 계정 동시 로그인이 꽉 차 있으면 sign-in 실패(종료 2 · `SignInLimitExceeded`) — KOS 웹 「기기 제한」에서 사람이 정리.
- 운영 회차는 배포 직후부터 오늘 일정 · 기준 정보(1시간) · 메뉴 · 오늘 구매에서 §4A 칸을 채운다 — 업데이트는 지난 행 몫.

## 7. 남은 위험 · OQ 처리 · 코디가 확인할 것

1. **OQ-4A-1 vs 브리프 「CARD 처럼 행째 빼는 곳도 null 규칙으로」** — `payment_type` 은 지금 NOT NULL 칸이라 칸만 비울 수 없다(바꾸면 지금 칸 제약 변경 = 금지). SPEC OQ-4A-1 「그 전엔 표 밖 값 처리(그 행을 뺀다)가 그대로」 를 따랐다 — **CARD 만 더함** · 다른 모르는 수단은 지금처럼 그 거래를 뺀다(테스트로 고정). null 규칙은 §4A 새 enum 칸에 적용.
2. **OQ-4A-11(`created_at` 덮기)** — 브리프 D-2 「`created_at` ← KOS 생성 시각」대로 이미 있는 행도 다음 동기화 · 업데이트 때 KOS 시각으로 덮는다. OQ 가 열려 있으니 확인 바람(되돌리려면 mapper 의 `created_at` 줄들만 빼면 된다).
3. **진행 중 환불 `refundingItems[].adjustedPrice`** — 항목 자신의 `adjustPriceV2` 가 비었을 때만 채운다. 지금 구매 반영은 `adjusted_*` 를 `adjustPriceV2` 로 매번 덮으므로, 환불 진행 중인 항목은 회차마다 「지금 반영이 비움 → 보충이 채움」이 오간다(값은 회차 끝에 맞음 · 그 항목의 `updated_at` 만 움직임). 드문 상태라 그대로 둠.
4. **메뉴 `medicineAndMachines[]`(섞인 목록 · OQ-4A-12)** — 약품 → 기기 순으로 마스터에서 찾고, 둘 다 없으면 종류를 정할 근거가 없어 **그 참조 행은 뺀다**(센다 `unresolved` · 이름 배열 칸은 그대로). SPEC 「행은 이름만 · FK 비움」이지만 `kind` 가 필수 칸이라 종류 추정을 하지 않았다.
5. **예약 규칙 이력(쌓기만)** — KOS 이력에 id 가 없어 (일어난 시각 · 종류 · 직원 · 내용)이 같은 살아 있는 행이 있으면 다시 넣지 않는다.
6. 기준 정보 회차에 새 단계(병원 설정 · 오늘 고객 칸)가 붙어 KOS 호출이 1시간에 약 「10 + 그룹 수 + 규칙 수 + 고객 목록 1 ~ 5장」 늘어난다(10초 일정 회차 · 오늘 구매 회차의 호출 수는 그대로).
7. `uq_visit_requested_procedure_composition_parent_sort_order` — `live_unique` 이름 규칙(`uq_<표>_<칸…>`)이 63자를 넘어 줄였다.
8. 값 미관찰 enum 2개(`requested_procedure_repetition` · `reservation_rule_event_type`)는 빈 enum — 첫 실값이 오면 그 칸 null + 경고가 남고, 값 추가 migration 이 필요하다(OQ-4A-9).
10. **`external_ref.external_updated_at` 왕복(실물에서 찾음)** — 지금 반영의 연결(`Refs.link`)이 직원 · 상담 기록 · 고객 연결을 쓸 때 `external_updated_at` 을 매번 None 으로 덮고, 보충이 KOS 수정 시각으로 다시 쓴다. 값은 회차 끝에 맞지만 오늘 상담 기록 · 일정 고객은 10초마다, 직원은 1시간마다 그 연결 행이 한 번씩 더 UPDATE 된다(데모: 직원 83 · 상담 3 · 고객 8 행). 지금 반영(외부 계약 · 금지 범위)을 고치지 않았다 — 지금 연결이 이 칸을 쓰지 않게 하려면 `sync_references.Refs.link` 의 `set_` 한 줄이 필요하다(코디 판단). 업데이트 경로(백필)는 지금 반영이 끼지 않아 다시 실행 = 0.
11. **값 미관찰 enum 의 첫 실값** — 위 §5 A4 의 `ONCE_PER_RESERVATION` · `protos.schedule.*Event` 5개. 지금은 그 칸 null + 경고(매 1시간 22줄 정도). 값 추가 migration 을 할지 · 이력 종류 이름(긴 proto 이름)을 어떤 DAY 말로 둘지는 SPEC(OQ-4A-9).
9. OQ-4A-4 · 5 · 6 · 7 · 8 · 10 · 13 · 15 — 칸은 SPEC 대로 두고 KOS 값을 그대로 받는다(결정하지 않음). OQ-4A-15 의 「확인용 두 번째 경로」는 받지 않는다(원천 하나).

## 고침 1 (지시 `be-fix-1-instructions.md` · 2026-11-20)

| | 반영 | 파일 |
|---|---|---|
| 1 | 목록 밖 enum 9값을 **0012 안에서** 한 번에 더함(새 migration 없음): `task_urgency_level` + `urgent`(KOS `URGENT`) · `etc_work_status` + `canceled`(`CANCELED`) · `requested_procedure_repetition` + `once_per_reservation`(`ONCE_PER_RESERVATION` — 규칙 · 구성 두 칸) · `reservation_rule_event_type` + `created` · `activated` · `deactivated` · `rule_set_changed` · `default_rule_set`(KOS `protos.schedule.{ReservationRuleCreatedEvent, …Activated…, …Deactivated…, ReservationRuleRuleSetChangedEvent, DefaultReservationRuleSetEvent}` — KOS 문자열은 매핑 표에만). 빈 enum 없음 | `enums/task.py` · `enums/room.py` · `emr/kos/mapper_kos_keys.py`(매핑 표) · `migrations/versions/20261120_0012_kos_keys.py` · `models/room.py`(주석) |
| 2 | `external_ref.external_updated_at` 왕복 — `sync_references.Refs.link` 의 충돌 갱신을 `coalesce(excluded, 지금 값)` 으로: **값이 주어질 때만 쓴다**. 다른 동작 · 반환 · 호출 수 그대로(그 한 줄 · 코디 허용) | `emr/sync_references.py` |
| 테스트 | 새 값 8줄 매핑(`test_DEMO_실물에서_본_값은_DAY_enum_으로`) · `test_enum_labels`(49 · DB 라벨 = 모델 · 빈 enum 없음) · `test_같은_회차_두_번이면_external_ref_쓴_행_0`(기준 정보 · 일정 지금 반영 → 칸 보충을 두 번 — 두 번째 `external_ref` 쓴 행 0 · 직원 외부 수정 시각 남음) | `tests/day/emr/test_kos_keys_mapper.py` · `test_kos_keys_sync.py` · `tests/day/test_enum_labels.py` |

검증(각 1회 · 디스크 정리 뒤 테스트 이미지 다시 받음):
- `./scripts/test.sh -q` 바꾼 테스트 + `Refs.link` 을 지나는 것(`test_kos_keys_mapper` · `test_kos_keys_sync` · `test_enum_labels` · `tests/migrations`(0012 왕복 · `alembic check`) · `test_sync` · `test_sale_sync` · `test_backfill` · `test_kos_keys_backfill`) — **109 passed**
- `ruff check` · `ruff format` · `mypy`(day · tests/day/emr) — 통과

로컬 DEMO(버리는 PG16 · Redis7 · 새 스키마 0012 · 테스트 계정 · DEMO 테넌트만 · `KOS_CLIENT_TAG=local` · 끝나고 컨테이너 0):

| 회차 | 목록 밖 경고 | 칸 보충 쓴 행 |
|---|---|---|
| 1 | **0** | 채움(기준 정보 · 메뉴 · 병원 · 일정 · 구매 — 예약 규칙 4 · 구성 4 · 이력 19 행의 enum 칸이 이제 값으로 들어감) |
| 2 | **0** | **external_ref 0** · 기준 정보 · 메뉴 · 병원 · 일정 · 구매 **0** · 고객만 9(+ 그 연결 9) — 1회차에선 고객 단계(병원 단계 안)가 일정보다 먼저 돌아 그 고객 행이 아직 없었다(첫 채움) |
| 3 | **0** | **전부 0**(external_ref 포함) |

- KOS 세션: 회차마다 따로 프로세스라 시스템 클라이언트 로그인이 회차마다 하나(`(local)`). 셋업의 직원 로그인 1 · 회차 1 · 2 의 2 · 회차 3 의 1 을 그때마다 해제 — 끝에 `(local)` 남은 것 0. 다른 표시 로그인은 이번에 해제하지 않았다.
- 남은 것: 앞 §7 의 1 · 2 · 3 · 4 · 5 · 6 · 7 · 9 그대로. §7-10(왕복)은 고침 · §7-11(첫 실값)은 0012 에 반영(그 밖 새 값은 다시 null + 경고 · OQ-4A-9).

## 고침 2 (지시 `be-fix-2-instructions.md` · 검수 `review-code-1-report.md` W1 ~ W7 · W8 은 손대지 않음)

| | 반영 | 파일 |
|---|---|---|
| W1 | **N+1 제거** — 배열 행 · 약품 · 기기 참조 행을 단계(깊이)마다 **표 하나에 SELECT 한 번**(`parent_col.in_(…)` · `owner_type = … AND owner_id.in_(…)`)으로 읽고 부모마다 맞춘다 · 바뀐 칸 UPDATE 는 표마다 한 번 읽어 비교 · 기타 업무 `external_ref` 잇기는 한 문(`INSERT … ON CONFLICT DO NOTHING` 여러 행) · 외부 수정 시각은 **한 번 읽어 다른 것만** UPDATE(같으면 문 0). **잠금: 보충은 그 회차와 같은 잠금(`emr_sync.lock_key(job)` — `schedules` · `master` · `menu` · `sales`) 안에서** 반영 — 보충이 길어지면 다음 같은 회차가 「앞 회차가 안 끝남」으로 건너뛰어 같은 방문 · 작업 행을 두 쪽이 동시에 쓰지 않는다(행 잠금 대기 · deadlock 없음). 고른 이유: 상한만 줄이면 시간 초과 직전 commit 과 다음 회차가 여전히 겹칠 수 있고, 같은 잠금이면 겹침이 구조적으로 0. 거기에 일정 보충 상한도 **8초**(10초 주기보다 짧게 — 잠금을 오래 잡아 다음 회차를 여러 번 건너뛰게 하지 않게) · 나머지는 그 회차 상한(`run_budget`). DB 오류도 전부 잡아 로그만 | `emr/sync_kos_keys.py` · `services/emr_kos_keys.py` |
| W2 | 목록 밖 값 경고 · 반영 실패 · 묶음 만들기 실패 = **프로세스에서 같은 줄(병원 · 표 · 칸 · 값 / 이름 · 오류 이름)마다 한 번** WARNING · 그 뒤는 셈만(`warnings` · 실패 셈). 상한 1만 줄 | `emr/sync_kos_keys.py`(`warn_once`) · `services/emr_kos_keys.py` · `emr/kos/mapper_kos_keys.py` |
| W3 | 결과 줄에 **`missing` · `unresolved` 까지** — 쓴 행이 있거나 셈이 지난번과 다를 때만 한 줄(같은 반복은 조용 · 폭주 없음) · 잠금 못 얻음 = 셈 + 처음 · 360번마다 한 줄(10초 회차면 1시간에 한 줄) · `tasks/emr.py` `_kos_keys` 도 예외를 삼킨다. 배선 테스트: 보충이 늦거나 던져도 일정 · 기준 정보 · 구매 태스크 status `done` 그대로 · `run_hospital` 이 던져도 master status 그대로 · 보충 순서(schedules → master → menu → sales) | `services/emr_kos_keys.py` · `tasks/emr.py` · `tests/day/emr/test_kos_keys_isolation.py` |
| W4 | **`visit.reservation_status_at` 은 이번에 채우지 않는다 — 늘 null(2단계)**. 매퍼 줄을 빼고 이유 주석(P07 에 키가 없고, P08 · P33 은 2단계 ext 「예약 하나 · 날짜 하나 받기」에서 붙인다). 테스트 주석 「상세」 정정 · 키가 와도 칸을 싣지 않음을 고정 | `emr/kos/mapper_kos_keys.py` · `tests/day/emr/test_kos_keys_mapper.py` |
| W5 | `Refs.link` 를 **원래 뜻(None = 비움)** 으로 되돌리고 `keep_updated_at=False` 기본 인자만 더함. 직원(`sync_master`) · 상담 기록(`sync_tasks`) · 고객(`sync_schedules`) 연결 **세 자리에서만** `keep_updated_at=True`(수정 시각을 넘기지 않는 호출 — 보충이 채운 값 유지). 구매 · 카드 · 메뉴 · 방문 연결은 손대지 않아 「바뀜」 판정이 고침 1 전과 같다 | `emr/sync_references.py` · `emr/sync_master.py` · `emr/sync_tasks.py` · `emr/sync_schedules.py` |
| W6 | 예약 규칙 이력 열쇠 = **KOS 원래 값(일어난 시각 · 내용 문자열)** + 느슨한 칸(종류 · 직원 — 같거나 **비어 있는** 행에 맞춘다 · 빈 칸만 채움). enum 값 추가 · 직원 해석 뒤에도 같은 이력이 두 번 쌓이지 않는다. 원래 값 칸을 새로 두지 않았다(SPEC 밖 칸 0 — 시각 · 내용은 이미 KOS 그대로 저장되는 칸). 한계: 같은 시각 · 같은 내용에 종류가 다른 이력 둘 중 하나가 아직 목록 밖(null)이면 다른 하나와 짝이 바뀔 수 있다(관찰 없음) | `emr/sync_kos_keys.py`(`ChildRule.loose` · `nullable_key`) |
| W7 | 진행 위치 키 분리 — `--stage kos_keys` 만 `day:emr:backfill:kos_keys:<병원>`(지난 백필 `day:emr:backfill:<병원>` 을 덮지 않는다 · 반대도). 병원 설정 · 고객 부분은 운영 1시간 새 단계와 **같은 잠금 `day:lock:emr:kos_keys:<병원>`** 안에서(TTL 1시간 · 못 얻으면 10초마다 최대 60번 기다리고 그래도면 종료 2 `TimeoutError` → 잠시 뒤 `--resume`). 운영 쪽은 잡혀 있으면 그 회차만 건너뛴다(`skipped_locked`) | `services/emr_backfill.py` · `services/emr_kos_keys_backfill.py` · `tests/day/emr/test_kos_keys_backfill.py` |

새 테스트: `test_보충_반영_문_수는_방문_수와_무관하다`(query-count — 방문 1 vs 7 · 바뀐 것 없는 재회차의 SQL 문 수 같음) · `test_목록_밖_값_경고는_병원_줄마다_한_번` · `test_연결은_수정_시각을_주지_않으면_기본은_비우고_보충_호출만_유지한다`(구매 = 비움 · 직원 = 유지) · `test_규칙_이력은_종류가_나중에_잡혀도_두_번_쌓이지_않는다` · `test_보충이_실패하거나_늦어도_태스크_status_는_그대로` · `test_못_찾음만_있는_회차도_한_줄_같으면_다시_안_남긴다` · `test_다음_회차가_잠금을_잡고_있으면_보충은_건너뛰고_센다`(같은 `schedules` 잠금 키 · 한 줄).

검증(각 1회):
- `./scripts/test.sh -q backend/tests/day/emr backend/tests/migrations` + `test_enum_labels` · `test_column_snapshot` · `test_constraints` · `test_models` — **492 passed**(첫 실행에서 새 테스트 2개 고정본 실수 고친 뒤 `test_kos_keys_sync.py` **12 passed**)
- `./scripts/test.sh -q`(전체) — **1947 passed**
- `./scripts/check.sh --pure` — 구조 · ruff · format · mypy · Taut 통과 · frontend 단계만 npm `@tailwindcss/postcss` 미설치(무관 · 앞과 같음)

로컬 DEMO(버리는 PG16 · Redis7 · 0012 · 테스트 계정 · DEMO 테넌트만 · `KOS_CLIENT_TAG=local` · 컨테이너 0):

| 회차 | 걸린 시간(기준 정보 → 메뉴 → 병원 · 고객 → 일정 → 구매 + 각 보충) | 목록 밖 경고 · 실패 줄 | 보충 쓴 행 |
|---|---|---|---|
| 1 | 6초 | 0 · 0 | 처음 채움 |
| 2 | 4초 | 0 · 0 | 기준 정보 · 메뉴 · 병원 · 일정 · 구매 **0**(external_ref 0) · 고객 9 + 그 연결 9 = 첫 채움(1회차엔 고객 단계가 일정보다 먼저라 그 고객 행이 아직 없었다 — 고침 1 과 같은 순서 효과) |

- KOS 세션: 셋업 직원 로그인 1 · 회차마다 시스템 클라이언트 1 — 그때마다 `(local)` 하나씩 해제(동시에 산 `local` 은 늘 하나 이하) · 끝에 `(local)` 남은 것 0.
- W8(`created_at` 덮기 · OQ-4A-11)은 지시대로 지금 코드 그대로.
- PR 본문에 적을 것: `Refs.link` 는 원래 뜻 그대로 + 기본 꺼진 `keep_updated_at` 인자(세 호출만 켬) · 보충은 그 회차 잠금 안 · 업데이트 진행 키 분리 · `reservation_status_at` 은 2단계.
