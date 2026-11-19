# customer-erd backend 1단계(DB) 결과 보고 — 마이그레이션 0010 · 모델 · enum

## 상태: done (커밋 · push · PR 없음 — 워크트리 변경만)

- 워크트리 `/Users/kknaks/orca/workspaces/CENTURION_DAY/customer-erd` · 브랜치 `kknaksss/customer-erd`
- base = `origin/dev` `bbd9220a` (시작 시 fetch — dev 가 더 나아가지 않아 rebase 하지 않음)
- Delivery #259 몫: D-1 · D-2(모델 · enum · entity_type 값. **매핑 코드는 2단계**) · A1 · A2 · A6 · A7(1단계 테스트)

## 수행 — 파일 · 모듈

새 파일
- `backend/migrations/versions/20261119_0010_sale_tables.py` — revision `0010_sale_tables` · down `0009_consultation_visit`
- `backend/day/models/menu.py` (메뉴 16) · `purchase.py` (구매 5) · `ticket.py` (시술권 3) · `prepaid_card.py` (선불카드 3) · `prescription.py` (처방 1)
- `backend/day/enums/purchase.py` · `ticket.py` · `prepaid_card.py` · `external_ref.py`(`SaleEntityType` — entity_type 새 값 20)
- `backend/tests/migrations/test_sale_tables_migration.py` · `backend/tests/day/test_sale_entity_types.py` · `backend/tests/day/column_snapshot_sale_data.py`(SPEC 표를 손으로 옮긴 새 28 테이블 칸 기대값 — 모델에서 만들지 않음)

고친 파일
- `backend/day/models/task.py` — `VisitTask` 에 `machines`(varchar[]) · `treatment_item_id`(FK) · `ticket_id`(FK) 3칸, 모두 nullable
- `backend/day/models/__init__.py` — 새 모델 import (alembic 이 읽음)
- `backend/day/identifiers.py` — 새 테이블 id NewType 23개 + `ExternalPurchaseId`(str)
- 테스트: `test_alembic.py`(HEAD → 0010) · `test_models.py`(52 + 28 · 옛 메뉴 이름 금지 · visit_task 새 칸 nullable) · `test_column_snapshot.py`(두 스냅샷 합침) · `column_snapshot_data.py`(visit_task +3칸) · `test_enum_labels.py`(enum 수 32 → 40)
- **범위 밖 2곳(필수 검사 통과용 · 코디 확인 필요)** — 아래 「이슈」 1 · 2

## 만든 것 — 수치

| 항목 | 수 |
|---|---|
| 새 테이블 | **28** (메뉴 16 · 구매 5 · 시술권 3 · 선불카드 3 · 처방 1) |
| 새 테이블 칸 합계 | **269** (공통 `created_at · updated_at · deleted_at` 포함) |
| `visit_task` 새 칸 | **3** (`machines` · `treatment_item_id` → treatment_item · `ticket_id` → ticket · 전부 nullable · server_default 없음) |
| 새 PostgreSQL enum 타입 | **8** — `purchase_status` · `purchase_process` · `purchase_item_type` · `purchase_transaction_status` · `payment_type` · `ticket_status` · `prepaid_card_ledger_kind` · `prepaid_card_pocket` |
| 재사용한 기존 enum 타입 | 2 — `product_option.type` → `option_type`(single · group · consultation) · `product_option.display_channels` → `connected_channel[]`(homepage · gangnamunni · kos_connect). SPEC 값 목록이 똑같아 새 타입을 만들지 않음 · 0010 은 이 둘을 만들거나 지우지 않음 |
| `external_ref.entity_type` 새 값 | 20 (SPEC-002 ㉔ 목록 그대로 · 칸은 열린 문자열이라 DB 변경 없음) |
| 새 부분 유일 · 인덱스 | 0 (SPEC §4 표에 유일 · 인덱스 표기 없음) |

## 검증 — 명령과 수치

| 명령 | 결과 |
|---|---|
| `uv run pytest -q tests/day/test_models.py tests/day/test_column_snapshot.py tests/day/test_sale_entity_types.py tests/migrations/test_sale_tables_migration.py tests/migrations/test_offline_sql.py` | **98 passed** |
| `./scripts/test.sh -q backend/tests/migrations backend/tests/day/test_enum_labels.py` (격리 PG16) | **23 passed** — upgrade head · downgrade base → upgrade 왕복 · head 하나 · `alembic check` 차이 없음(모델 == migration) · DB enum 라벨 == 모델 · offline SQL |
| `./scripts/test.sh --pure -q` | **1414 passed** (351 deselected = infra) |
| `./scripts/test.sh -q` (전체 · 격리 인프라) | **1765 passed** |
| `./scripts/check.sh --pure` | 구조 · Jinja · ruff · format · **mypy(402 files, 0 issue)** · Taut audit · **Taut check 통과**. 마지막 `frontend` 단계만 실패 — **무관**: 이 워크트리에 npm 의존성이 설치되지 않음(`Cannot find module '@tailwindcss/postcss'`) · 프론트 파일 변경 0 |
| ruff check (만진 파일) | All checks passed |

## 기존 테이블 변경 0 증거 (A2)

`origin/dev` 를 scratch 에 풀어 같은 스크립트로 메타데이터 서명(칸별 타입 · nullable · server_default · FK · PK, 인덱스 이름 · 칸 · unique · where)을 떠서 비교:

```
base tables 52 now 80 new 28 removed set()
added cols visit_task ['machines', 'ticket_id', 'treatment_item_id']
  [VARCHAR[] nullable] [UUID nullable FK ticket.id] [UUID nullable FK treatment_item.id]
changed existing columns/indexes: []
```

- 0010 upgrade 본문에 `drop_` · `alter_column` · `op.execute` · `bulk_insert` · `rename` 없음(테스트로 고정) — 데이터 이동 · 백필 없음.
- 칸 스냅샷 테스트: 1차 52 테이블은 `visit_task` 3칸만 늘었다.
- A6(물리 DELETE 0): 이번 단계는 동기화 코드 없음 — 해당 없음(2단계).

## 계약 대조 — SPEC-000 §4 항목별

| 테이블 | 결과 |
|---|---|
| product_category · product · product_category_link · product_option_price · prepaid_card_product · etcetera_product_category · etcetera_product · etc_task_type · purchase · purchase_item · purchase_transaction · ticket_bundle · ticket_set · ticket · prepaid_card · prepaid_card_customer · prepaid_card_ledger · prescription | 같음 (칸 · 타입 · 필수 · FK) |
| product_option | 같음. `unit_type · unit_value` 없음(11-19 개정대로) |
| product_option_composition | 같음. `ref_single_option_id` 없음(11-19 개정). 「`price_amount (+ 공급가 · 부가세 · 면세)`」 → `price_amount` · `supplied_amount` · `vat_amount` · `tax_free_amount`(product_option 과 같은 이름) |
| treatment | `category_ids` 만들지 않음 — 타입 「—」 · 테이블 열 「확인 필요」 |
| treatment_item | 같음 |
| treatment_item_machine · treatment_item_medicine · machine · medicine | 표 칸 같음 + `created_at · updated_at · deleted_at`(표에 없지만 §4 「공통」 · §2 「삭제 — 모든 테이블」) |
| purchase_price_adjustment · purchase_assignee | SPEC 이 정한 칸만(`id` · 관계 FK · 공통 시각). 「나머지 칸 미정」(OQ-08-3 · 08-4)은 만들지 않음 |
| visit_task | `machines` · `treatment_item_id` · `ticket_id` — §3 05 「추가(2026-11-18)」 그대로 |

타입 해석(SPEC 이 값 목록을 닫지 않은 enum → 기존 관례대로 **문자열 칸**, `enums/__init__` 「값이 열린 칸은 문자열」 · `visit_task.unit_type` 과 같음):
`taxation`(product_option · purchase_item · treatment_item) · `adjusted_taxation` · `unit_type`(composition · treatment_item · purchase_item · ticket_set) · `treatment_item.status` · `treatment_item.healthcare_reimbursement`. 칸 comment = 「열린 enum — SPEC 값 목록이 닫히지 않았다」.

enum 값 = SPEC-000 §4 그대로(DAY 말 · 소문자): purchase.status 5(`paid` 포함) · process 5(`revoking` · `prepaid_card_item_substituting` 포함) · item_type 3 · 거래 status 2 · payment_type 7 · ticket status 3 · ledger kind 6 · pocket 2. KOS 문자열 → enum 매핑 코드는 2단계(emr).

`hospital_id`: 메뉴 머리 테이블(product_category · product · treatment_item · treatment · machine · medicine · etc_task_type · prepaid_card_product · etcetera_product_category · etcetera_product)만. 구매 · 시술권 · 카드 · 처방은 §2.1 대로 부모를 거쳐 안다(OQ-08-6 기본값).

KOS id 칸 0 — `test_업체_칸은_외부_테이블에만_있다` 통과.

## 이슈 · 코디가 확인할 것

1. **범위 밖 수정 — `backend/day/emr/kos/demo/kos_board.py`(이름 · 타입만)**. 새 `PurchaseId` 가 생기자 식별자 규칙(`scripts/devtools/identifiers.py` — `purchase_id` 라는 이름은 `PurchaseId` 여야 함)이 데모의 KOS 수납 id(`purchase_id: str`)를 잡아 `check.sh` 가 깨졌다. 같은 파일 관례(`staff_external_id: ExternalStaffId`)대로 `purchase_external_id: ExternalPurchaseId` 로 바꿨다(`identifiers.py` 에 `ExternalPurchaseId` 추가). 동작 변경 없음 · KOS 로 보내는 키 · 값 그대로. 2단계가 emr 에서 구매 외부 id 를 쓸 때 이 타입을 쓰면 된다.
2. **범위 밖 수정 — 루트 `taut.toml`** `[tool.taut.enum].shared_modules` 에 새 enum 모듈 4개(`day.enums.external_ref` · `prepaid_card` · `purchase` · `ticket`) 등록. 안 하면 Taut ENUM001(「Shared Enum is outside the central directory」)로 `taut-check` 실패. 한 줄 설정 추가뿐.
3. **유일 제약을 두지 않은 관계(SPEC 표기 없음 — 결정 필요하면 SPEC 으로)**: `ticket_bundle.purchase_item_id`(제목 「구매 항목 1 : 0..1」) · `prepaid_card_ledger.purchase_transaction_id`(「거래 1 : 이력 0..1」). 브리프 「SPEC 에 있는 것만」에 따라 부분 유일을 만들지 않았다. backend-reliability 「불변식은 DB 제약으로」 관점에서 2단계 upsert 전에 정할지 확인 바람. 또 2단계 upsert 가 ON CONFLICT 를 쓰려면 `external_ref` 의 기존 부분 유일만으로 충분한지도 함께.
4. **엔티티 id 이름**: 새 enum `SaleEntityType`(day/enums/external_ref.py)은 새 20 값만 담았다. 1차 값(`customer` · `visit` · `room` …)은 지금처럼 `emr/sync_references.py` 문자열 상수에 그대로 둠(emr 은 2단계 몫 — 합칠지는 2단계 판단).
5. 0010 은 forward-only 관례(머리말에 명시) — downgrade 는 테스트 왕복용으로 새 칸 · 새 테이블 · 새 enum 타입만 역순 삭제, 기존 `option_type` · `connected_channel` 은 건드리지 않는다.
6. `check.sh --pure` 의 frontend 단계 실패는 이 워크트리 npm 미설치(무관 · 프론트 변경 0). 코디 환경에서 `npm --prefix scripts/frontend ci` 뒤 재확인 권장.

## 보강 — 메뉴 키 11칸 · 유일 제약 1개 (지시 `menu-keys-addition.md` · 2026-11-19)

새 마이그레이션 파일 없이 **0010 을 고쳤다**(아직 어디에도 적용되지 않음). revision · down_revision 그대로.

### 더한 칸 (모두 nullable · 기본값 없음)

| 테이블 | 칸 | 타입(모델 · migration) |
|---|---|---|
| `treatment` | `search_phonetic_name` · `registered_at` | `String` · `DateTime(timezone=True)` |
| `machine` · `medicine` | `search_phonetic_name` | `String` |
| `product` | `cautions` | `ARRAY(Text)` (text[] — 지시 타입 그대로 · `caution` 한 칸은 그대로) |
| `product` | `target_country_codes` · `medicine_and_machine_names` | `ARRAY(String)` (varchar[] — `badges` · `visit_task.medicines` 관례) |
| `product_option` · `product_option_composition` | `medicine_and_machine_names` | `ARRAY(String)` |
| `treatment_item` | `drafted_at` | `DateTime(timezone=True)` |
| `prepaid_card_product` | `translations` | `JSONB` (다른 메뉴 `translations` 와 같음) |

- 칸 이름 · 타입은 지시 표 그대로 — 관례와 달라 바꾼 것 없음. 새 테이블 칸 합계 269 → **280**.
- `treatment.category_ids` 는 넣지 않았다(지시대로 · 모델 머리말에 「804건 모두 비어 있음 · OQ」).

### 유일 제약

- `uq_ticket_bundle_purchase_item_id` — `ticket_bundle(purchase_item_id) WHERE deleted_at IS NULL`(모델 `live_unique` · migration `create_index(unique=True, postgresql_where=…)`, `ticket_bundle` 생성 직후).
- 걸지 않음: `prepaid_card.purchase_item_id` · `visit_task.ticket_id` · `prepaid_card_ledger.purchase_transaction_id`(테스트 `CREATE_TABLES.count("unique=True") == 1` 로 고정).
- 모델 주석에 2단계 upsert 순서(「옛 번들 삭제 표시 → 새 번들 생성」)를 적었다.
- 앞 절 「이슈」 3 은 이걸로 닫힘(ticket_bundle) · 나머지 셋은 지시대로 열어 둠.

### 고친 파일

`backend/migrations/versions/20261119_0010_sale_tables.py`(머리말 · 8 테이블 칸 · 인덱스) · `backend/day/models/menu.py` · `backend/day/models/ticket.py` · `backend/tests/day/column_snapshot_sale_data.py`(11칸) · `backend/tests/migrations/test_sale_tables_migration.py`(부분 유일 1개 테스트) · `backend/tests/day/test_constraints.py`(`ticket_bundle.purchase_item_id` 실제 PG 사례 — 「모델의 부분 유일 = 사례 목록」 테스트가 요구).

### 검증

| 명령 | 결과 |
|---|---|
| `uv run pytest -q tests/day/test_models.py tests/day/test_column_snapshot.py tests/day/test_sale_entity_types.py tests/migrations/test_sale_tables_migration.py tests/migrations/test_offline_sql.py` | **99 passed** |
| `./scripts/test.sh -q backend/tests/migrations backend/tests/day/test_enum_labels.py backend/tests/day/test_constraints.py` (격리 PG) | **61 passed** — 왕복(upgrade → downgrade base → upgrade) · head 하나 · `alembic check` 차이 없음 · 새 부분 유일이 살아 있는 두 번째 행을 23505 로 막음 · 지운 행 값 재사용 됨 |
| `./scripts/check.sh --pure` | 구조 · ruff · format · mypy(402 files 0 issue) · Taut audit/check 통과 · frontend 단계만 npm 미설치로 실패(무관 · 앞과 같음) |
| ruff check (만진 파일) | All checks passed |
