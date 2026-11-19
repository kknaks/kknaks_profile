# 리뷰 리포트: customer-erd / code 1 (DB 1단계: 마이그레이션 0010 · 모델 · enum) (2026-11-19)

- 대상: 워크트리 `CENTURION_DAY/customer-erd` · 브랜치 `kknaksss/customer-erd` · base `origin/dev` `bbd9220a` (fetch 후 확인. dev 는 더 나아가지 않았음)
- 범위: `git diff origin/dev`(10파일) + 미추적 13파일
- SSOT: SPEC-000 §2 · §3 05 `visit_task` · §4(28 테이블) · SPEC-002 개정 ㉔(entity_type · 매핑 표) · mediness `customer-erd-spec` 워크트리(`kknaksss/customer-erd-sync`)
- 워커 리포트(`be-1-report.md`)는 그대로 믿지 않고 diff · 실행으로 다시 확인했다.

## 판정: **PASS (WARN 4 · FAIL 0)**

| 축 | 판정 |
|---|---|
| 1. SPEC 대조 (28 테이블 · 칸 · 타입 · 필수 · FK · enum) | **PASS** (WARN 1: 값이 열린 enum 은 문자열 칸) |
| 2. 상용 운영 (기존 변경 0 · nullable · 데이터 안 건드림 · 0009 다음 · downgrade · 잠금) | **PASS** (WARN 1: `visit_task` FK 추가 잠금. 0008 과 같은 수준) |
| 3. KOS 제거 · 소프트 딜리트 | **PASS** |
| 4. 범위 밖 변경 2곳 | **PASS** (둘 다 필요 · 안전) |
| 5. 1:0..1 유일 제약 | **WARN**: 권고만 냄. 「사용자 판단」 |
| 6. 테스트 | **PASS** (WARN 1: SPEC 타입 · 필수는 테스트가 지키지 않음) |
| 7. 직원이 실물에서 만날 자리 | **없음** |
| (추가) FK 인덱스 | **WARN**: 새 테이블 FK 인덱스 0. 2단계 전에 빈 테이블일 때 넣을지 결정 필요 |

---

## 1. SPEC 대조: PASS

마이그레이션 `backend/migrations/versions/20261119_0010_sale_tables.py` 본문과 SPEC-000 §4 표를 칸 하나씩 비교했다. `alembic check` 결과 모델과 migration 사이에 차이가 없다(아래 6). 그래서 아래 비교는 모델에도 그대로 해당한다.

| 테이블 | 줄 | 칸 · 타입 · 필수 · FK | 비고 |
|---|---|---|---|
| product_category | 181-206 | 같음 | |
| product | 207-240 | 같음 (`badges` varchar[] · `translations` jsonb) | |
| product_category_link | 241-267 | 같음 · 복합 PK | |
| treatment | 268-290 | 같음 | `category_ids` 는 만들지 않음. SPEC 타입 「—」 · 「확인 필요」라 맞음 |
| treatment_item | 291-351 | 같음 | `status` · `unit_type` · `healthcare_reimbursement` · `taxation` 은 String (WARN-1) |
| machine · medicine | 352-397 | 같음 | |
| treatment_item_machine · _medicine | 398-459 | 복합 PK 같음 | 공통 시각 칸 3개 추가. §4 「공통」 · §2 「삭제」라 맞음 |
| product_option | 460-513 | 같음. `type` 은 기존 `option_type`(single · group · consultation), `display_channels` 는 기존 `connected_channel[]`(값 3개 같음 · 0002:41,86) | `unit_type · unit_value` 없음. 11-19 개정대로 맞음 |
| product_option_price | 514-545 | 복합 PK · `amount` NOT NULL 같음 | |
| product_option_composition | 546-595 | 같음 | `ref_single_option_id` 없음. 11-19 개정대로 맞음 |
| etc_task_type | 596-618 | 같음 | |
| prepaid_card_product | 619-650 | 같음 (`expiration_days` 만 null 허용) | |
| etcetera_product_category · etcetera_product | 651-707 | 같음 | |
| purchase | 708-735 | 같음 · enum 5 / 5 값 | |
| purchase_item | 736-805 | 같음. 공급가 · 면세 · 부가세 NOT NULL(SPEC ✓), 조정 금액 null 허용 | |
| purchase_price_adjustment | 806-835 | SPEC 이 정한 칸만 | 나머지 칸 미정(OQ-08-4). 만들지 않은 것이 맞음 |
| prepaid_card | 836-867 | 같음 | |
| purchase_transaction | 868-911 | 같음 · 자기 참조 FK · `staff_id` NOT NULL | |
| purchase_assignee | 912-937 | SPEC 이 정한 칸만 (OQ-08-3) | |
| ticket_bundle · ticket_set · ticket | 938-1028 | 같음 · 가격은 번들에만 | |
| prepaid_card_customer · prepaid_card_ledger | 1029-1103 | 같음 · ledger kind 6 · pocket 2 | |
| prescription | 1104-1125 | 같음 | |
| `visit_task` 새 칸 | 150-162 · `models/task.py:96-99` | `machines` varchar[] · `treatment_item_id` FK · `ticket_id` FK. 모두 null 허용 | §3 05 와 같음 |

- 빠진 것 0 · 다른 것 0 · SPEC 에 없는데 만든 것 0. 예외는 SPEC 이 허용한 공통 시각 칸뿐이다.
- enum 값 8개 타입은 SPEC §4 표 · SPEC-002 ㉔ 매핑 표의 DAY 값과 한 글자도 다르지 않다(`enums/purchase.py` · `ticket.py` · `prepaid_card.py`).
- `SaleEntityType` 20값(`enums/external_ref.py:16-36`)은 SPEC-002 ㉔ 목록 20개와 같다. KOS id 가 없는 8개 테이블을 뺀 목록도 ㉔ 와 같다.
- **WARN-1**: SPEC 은 `enum` 이라고 적었지만 값 목록이 없는 칸 9곳이 `String` + comment 「열린 enum」으로 들어갔다. 해당 칸은 `taxation` ×3 · `adjusted_taxation` · `unit_type` ×4 · `treatment_item.status` · `healthcare_reimbursement` 이다(예 migration 300-324, 475-480, 745-772, 974-979). 근거는 `enums/__init__.py:3-4`(「값이 열린 칸은 문자열」) · prod `visit_task.unit_type`(`models/task.py:82`) · `customer.gender` 선례라서 관례와 맞다. 값이 닫히면 문자열을 native enum 으로 바꾸는 migration(ALTER TYPE USING)이 필요하다. 이건 SPEC OQ-041-4 쪽 일이다.

## 2. 상용 운영: PASS

- 기존 migration 파일 변경 0(`git diff origin/dev --stat -- backend/migrations/versions/` 비어 있음). 0010 의 `down_revision = "0009_consultation_visit"`(33줄). 실제 PG 에서 head 하나 확인(6 참조).
- upgrade 본문에 `drop_` · `alter_column` · `op.execute` · `bulk_insert` · `rename` 없음. 직접 읽어 확인했고 `test_sale_tables_migration.py` 가 고정한다. 데이터 이동 · 백필도 없음.
- 기존 52 테이블에서 바뀐 것은 `visit_task` 3칸뿐이다. 칸 스냅샷 테스트(`column_snapshot_data.py` +3줄) · `test_models.py` 새 테스트로 확인했다. 3칸은 null 허용 · server_default 없음이라 PG11+ 에서 메타데이터만 바뀐다(행 재작성 없음).
- downgrade(165-177): FK → 칸 → 새 테이블 역순 → 새 enum 타입 역순으로 지운다. 기존 `option_type` · `connected_channel` 은 지우지 않는다(`create_type=False` · NEW_TYPES 밖). 실제 PG 에서 base ↔ head 왕복이 통과했다.
- **WARN-2 (잠금)**: `op.create_foreign_key(... "visit_task" ...)` 2회(153-162)는 `visit_task` 에 SHARE ROW EXCLUSIVE 잠금을 잡고 기존 행 전체를 검증 스캔한다. 새 칸이 전부 NULL 이라 검사는 가볍지만, 스캔하는 동안 `visit_task` 쓰기(현황판 동기화 10초 루프)가 막힌다. `lock_timeout` 도 없어서, 앞선 긴 트랜잭션이 있으면 줄을 서서 기다리게 된다. **0008(`started_room_id` FK · 0008:44-50)도 같은 방식으로 이미 prod 에 나갔다.** 그래서 새 위험은 아니다. 행 수가 많아졌다면 `postgresql_not_valid=True` + 별도 `VALIDATE CONSTRAINT` 또는 `SET lock_timeout` 을 쓰는 방법이 있다. 권고만 하고 결정은 하지 않는다.

## 3. KOS 제거 · 소프트 딜리트: PASS

- 새 28 테이블에 업체 칸(`vendor` · `external_id` · `kos_*` · `external_number`) 0. `test_업체_칸은_외부_테이블에만_있다` 가 통과했다. KOS id 는 `external_ref` 로만 둔다(`SaleEntityType`).
- `deleted_at` 은 28 / 28 테이블에 null 허용으로 있다(migration 전 테이블 · 모델 `Timestamps` → `_columns.py:66-71`).
- 새 유일 제약 0이라서 「유일은 살아 있는 행만」을 어기는 곳도 없다. 복합 PK 3개(link · price · item_machine/medicine)는 §2 「복합 PK 는 그대로」에 맞다.
- enum 값은 전부 DAY 말 소문자다. KOS 문자열(`ETCETRA_PRODUCT` 등)은 코드에 없고, 2단계 mapper 몫이다.

## 4. 범위 밖 변경 2곳: PASS

| 파일 | 내용 | 필요? | 안전? |
|---|---|---|---|
| `backend/day/emr/kos/demo/kos_board.py` (diff 32-37 · 267-345) | `purchase_id: str` → `purchase_external_id: ExternalPurchaseId`. 반환 타입 · 인자 타입만 바뀜 | **필요**: `PurchaseId` NewType 이 생기면서 식별자 규칙(`scripts/devtools/identifiers.py`)이 `purchase_id` 이름을 `PurchaseId` 로 요구한다. 바꾸지 않으면 check 가 깨진다 | **안전**: `NewType(str)` 은 실행할 때 그냥 `str` 이다. KOS 요청 키(`"id"` · `"purchaseId"`) · 값 · 호출 순서 · 비교식(`b.get("purchaseId") == …`)이 모두 그대로라 동작이 바뀌지 않는다. 같은 파일 관례(`staff_external_id: ExternalStaffId`)와도 맞다. 데모 테넌트 가드 안의 코드다 |
| `backend/day/identifiers.py:52-75 · 90` | 새 id NewType 23 + `ExternalPurchaseId` | 필요 (모델 타입) | 안전 (추가만) |
| `taut.toml:137` | `shared_modules` 에 `day.enums.external_ref` · `prepaid_card` · `purchase` · `ticket` 추가 | **필요**: 넣지 않으면 Taut ENUM001 이 난다 | **안전**: 기존 `day.enums.*` 과 같은 방식으로 등록만 했다. 규칙을 끄거나 baseline 에 넣은 것이 아니다 |

직접 실행: `scripts.devtools.architecture` exit 0 · `scripts.devtools.identifiers` exit 0 · `ruff check backend scripts` All checks passed.

## 5. 1:0..1 유일 제약: WARN (권고만 · **사용자 판단**)

워커는 SPEC 표에 UNIQUE 표기가 없어서 걸지 않았다. 브리프의 「SPEC 에 있는 것만」 기준으로는 맞다. 하지만 backend-reliability 의 「불변식은 DB 제약으로」와 부딪친다. 관계마다 위험이 다르다.

| 관계 | 걸 경우 모양 | 동기화 · KOS 재생성 때 막혀 깨질 위험 | 권고 |
|---|---|---|---|
| `purchase_item ‖--o| ticket_bundle` (`models/ticket.py:35`) | `uq_ticket_bundle_purchase_item_id WHERE deleted_at IS NULL` | **낮음**. KOS 번들의 외부 id 가 `purchaseItemId` 자체(㉔)라서 `external_ref` 유일(hospital · vendor · entity_type · external_id)이 이미 사실상 1:1 을 지킨다. 재확정이 없다(§4 08). 한 번 막히는 경우는 같은 회차에서 「새 번들 insert」가 「옛 번들 soft delete」보다 먼저 실행될 때뿐이다 | **걸어도 됨**. 거는 편을 권고(빈 테이블이라 지금이 가장 싸다). 2단계 upsert 순서를 「삭제 표시 → 생성」으로 고정해야 한다 |
| `purchase_item |o--o| prepaid_card` (`models/prepaid_card.py:37`) | `… WHERE purchase_item_id IS NOT NULL AND deleted_at IS NULL` | **중간**. KOS `process = prepaid_card_item_substituting`(표본 없음 · OQ-08-9)이 카드 교체일 수 있다. 그런데 ㉔ 에 따르면 「카드 행은 지우지 않는다」(환불 카드도 응답에 남음). 교체로 같은 항목을 가리키는 살아 있는 카드가 둘 생기면 동기화가 막히고, 그 고객의 카드 루프 전체가 실패할 수 있다 | **지금은 걸지 않기를 권고**. OQ-08-9 표본이 나온 뒤 정한다. 걸려면 위반 행을 「건너뛰어 센다」로 처리하는 2단계 계약이 먼저 있어야 한다 |
| `ticket |o--o| visit_task` (`models/task.py:99`) | `uq_visit_task_ticket_id WHERE ticket_id IS NOT NULL AND deleted_at IS NULL` | **높음**. ① KOS 에서 작업을 `canceled`(행은 남음) 처리한 뒤 같은 티켓을 새 작업에 다시 쓰면 살아 있는 행 2개가 같은 `ticket_id` 를 갖는다. ② 일정 동기화는 작업을 schedule+sequence 로 upsert 한다. 한 회차 안에서 티켓이 작업 A → B 로 옮겨 가면 행 순서에 따라 일시 위반이 생긴다(DEFERRABLE 이 아니면 막힌다). ③ 이 충돌은 **지금 prod 10초 현황판 동기화**를 막는다. 현황판이 멈춘다는 뜻이라 직원 영향이 바로 생긴다 | **걸지 않기를 강하게 권고**. 걸더라도 `status <> 'canceled'` 조건 + DEFERRABLE INITIALLY DEFERRED 를 검토해야 한다. 기본은 「서비스 검사 + 위반 집계」 |
| (워커가 덧붙인 것) `purchase_transaction ↔ prepaid_card_ledger` 0..1 (`models/prepaid_card.py:66-68`) | `… WHERE purchase_transaction_id IS NOT NULL AND deleted_at IS NULL` | 낮음 ~ 중간. 금액 · 포인트 두 주머니를 한 결제로 함께 빼면 거래 1개에 이력이 2행(주머니마다) 생길 수 있다(OQ-10-5 · 표본 없음). 그 경우 0..1 은 틀린 표기가 된다 | **걸지 않기를 권고**. OQ-10-5 를 먼저 닫는다 |

→ **사용자 판단**: (a) 위 넷 가운데 무엇을 SPEC §4 표에 「유일」로 올릴지 (b) 올린다면 0010 에 넣을지(빈 테이블 · 운영 영향 없음) 아니면 2단계 0011 로 미룰지.

## 6. 테스트: PASS

직접 실행한 결과:

| 명령 | 결과 |
|---|---|
| `cd backend && uv run pytest -q tests/day/test_models.py tests/day/test_column_snapshot.py tests/day/test_sale_entity_types.py tests/migrations/test_sale_tables_migration.py` (브리프 지정) | **97 passed** (0.61s). 워커가 적은 98 은 `test_offline_sql.py` 를 함께 돌린 수 |
| `./scripts/test.sh -q backend/tests/migrations backend/tests/day/test_enum_labels.py` (자체 격리 compose · 무작위 포트 · 끝나면 down. 사용자 포트와 공유 DB 는 쓰지 않음) | **23 passed** (12.67s). upgrade head · base ↔ head 왕복 · head 하나 · `alembic check` 차이 없음 · DB enum 라벨 == 모델(40) · offline SQL |
| `./scripts/test.sh --pure -q` | **1414 passed** · 351 deselected(infra) |

새 테스트가 지키는 것:
- `test_sale_tables_migration.py`: 0009 다음인지 · upgrade 에 파괴 연산이 없는지 · 새 테이블이 정확히 28개 == 스냅샷인지 · 기존 테이블 추가는 `visit_task` null 허용 3칸뿐인지 · downgrade 가 새 것만 지우는지 · 기존 enum 타입을 만들거나 지우지 않는지. 텍스트 정규식 기반이라 DB 없이 돈다(테스트 전략에 맞음).
- `column_snapshot_sale_data.py`: SPEC 표를 손으로 옮긴 칸 이름 집합이다. 모델에서 만들지 않아서 순환 검증이 아니다.
- `test_sale_entity_types.py`: 20값 · 테이블 이름과 같은지 · 소문자인지.
- `test_models.py`: 80 테이블 · 옛 메뉴 이름(`procedure` · `medical_service*`) 금지 · `visit_task` 새 칸 nullable · FK 대상.
- **WARN-3**: 스냅샷은 **칸 이름만** 본다. SPEC 의 타입 · 필수(NOT NULL) · FK 대상을 기계적으로 지키는 테스트가 없다. 지금은 `alembic check`(모델 == migration) + 이 리뷰의 손 대조가 그 몫을 한다. 2단계에서 칸을 고치다 `purchase_item.supplied_amount` 를 nullable 로 바꾸는 식의 회귀가 생겨도 테스트는 초록이다. 기존 1차 52 테이블과 같은 수준의 부채라서 FAIL 은 아니다.

## (추가) FK 인덱스: WARN-4

- 새 28 테이블에 FK 칸 인덱스가 0개다(`create_index` 0회). SPEC 표기가 없으니 SPEC 위반은 아니다. 하지만 2단계 10초 루프가 `purchase.visit_id` · `purchase_item.purchase_id` · `ticket_bundle.customer_id` · `ticket_set.ticket_bundle_id` · `ticket.ticket_set_id` · `prepaid_card.customer_id` 로 묶음 조회를 하게 된다(㉔ ②③④).
- 테이블이 빈 지금(0010 · 또는 2단계 0011 에서 동기화가 켜지기 전)은 인덱스를 거의 공짜로 만들 수 있다. 데이터가 쌓인 뒤에는 `CONCURRENTLY` 가 필요하다.
- **사용자 판단 / 2단계 브리프**: 어느 FK 에 인덱스를 둘지는 2단계 queries 설계와 함께 정한다. 0010 을 고칠 필요는 없다.

## 7. 직원이 실물에서 만날 자리: 없음

화면 · API · 동기화 코드 변경이 없다. 새 테이블은 비어 있고 `visit_task` 새 칸은 NULL 이다. 데모 시더(`kos_board.py`)도 동작이 바뀌지 않는다. 배포할 때 생길 수 있는 유일한 접점은 WARN-2(마이그레이션 순간의 `visit_task` 쓰기 대기)다. 0008 과 같은 수준이다.

## 참고 (기존 부채 · 이번 범위 밖)

- `check.sh --pure` 의 frontend 단계는 워크트리에 npm 이 설치되지 않아 실패한다(워커 보고). 프론트 변경이 0이라 무관하다. 코디 환경에서 다시 확인하면 된다.
- 1차 `entity_type` 값은 `emr/sync_references.py` 문자열 상수에 그대로 있다. `SaleEntityType` 과 합칠지는 2단계에서 판단한다(워커 이슈 4).

---

## FAIL 고칠 곳

**없음.**

## 사용자 판단으로 모은 것

1. 1:0..1 부분 유일 4건을 SPEC 에 올릴지 · 언제 넣을지(§5 표. 권고: bundle 만 걸고 나머지 3건은 보류).
2. 새 테이블 FK 인덱스를 빈 테이블일 때 넣을지(§WARN-4).
3. `visit_task` FK 추가를 NOT VALID + VALIDATE / `lock_timeout` 으로 바꿀지(§WARN-2. 0008 선례는 그대로 나갔다).
