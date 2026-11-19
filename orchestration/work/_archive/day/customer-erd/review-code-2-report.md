# 리뷰 리포트: customer-erd / code 2 (메뉴 키 보강 재검수) (2026-11-19)

- 대상: 지시 `menu-keys-addition.md` 대로 고친 0010 · 모델 · 테스트(`be-1-report.md` 「보강」 절)
- spec 워크트리 `customer-erd-spec`(`kknaksss/customer-erd-sync`)의 SPEC-000 「2026-11-19 추가」 11칸 · `ticket_bundle` 유일 표기
- 기준: `git diff origin/dev` + 미추적 파일. 워커 리포트는 diff · 실행으로 다시 확인했다.

## 판정: **PASS (FAIL 0 · 새 WARN 0)**

| 볼 것 | 판정 |
|---|---|
| 1. 11칸이 지시서 표와 같은가 | **PASS** |
| 2. SPEC-000 표 = 모델 = 마이그레이션 | **PASS** |
| 3. 유일 제약은 `ticket_bundle.purchase_item_id WHERE deleted_at IS NULL` 하나뿐 | **PASS** |
| 4. 기존 테이블 변경 0 | **PASS** |
| 5. 1차 리포트 PASS 항목 유지 | **PASS** |
| 6. 직접 실행 | **PASS** (수치 아래) |
| 직원이 실물에서 만날 자리 | **없음** |

## 1 · 2. 11칸: 지시서 = SPEC-000 = migration = 모델

| 테이블 | 칸 | 지시 타입 | SPEC-000 (줄) | migration `0010` (줄) | 모델 `models/menu.py` (줄) |
|---|---|---|---|---|---|
| treatment | `search_phonetic_name` | varchar | varchar · 1427 | String null · 283 | 216 |
| treatment | `registered_at` | timestamptz | timestamptz · 1428 (`createDate`) | DateTime(tz) null · 284 | 217 |
| machine | `search_phonetic_name` | varchar | 1439 | 370 | 227 |
| medicine | `search_phonetic_name` | varchar | 1440 | 394 | 237 |
| product | `cautions` | text[] | text[] · 1321 | ARRAY(Text) null · 230 | 78 |
| product | `target_country_codes` | varchar[] | 1328 | ARRAY(String) null · 231 | 79 |
| product | `medicine_and_machine_names` | varchar[] | 1329 | 232 | 80 |
| product_option | `medicine_and_machine_names` | varchar[] | 1363 | 501 | 126 |
| product_option_composition | `medicine_and_machine_names` | varchar[] | 1386 | 582 | 160 |
| treatment_item | `drafted_at` | timestamptz | 1409 | DateTime(tz) null · 341 | 186 |
| prepaid_card_product | `translations` | jsonb | 1468 | JSONB null · 648 | 266 |

- 11 / 11 이 이름 · 타입 · nullable · 테이블 모두 같다. 기본값은 없고, 관례 때문에 이름을 바꾼 칸도 없다(배열 = `ARRAY(String)` 은 `badges` · `visit_task.medicines` 관례와 같음).
- `treatment.category_ids` 는 넣지 않았다. 지시대로다(모델 머리말에 OQ 로 남김).
- 모델 = migration 은 실제 PG `alembic check` 차이 0 으로 확인했다(6). 칸 스냅샷 `column_snapshot_sale_data.py` 에도 11칸이 반영됐다(칸 스냅샷 테스트 통과).

## 3. 유일 제약: 하나뿐

- migration `0010:986-992`: `create_index("uq_ticket_bundle_purchase_item_id", "ticket_bundle", ["purchase_item_id"], unique=True, postgresql_where=deleted_at IS NULL)`. 파일 전체에서 `unique=True` 는 1회뿐이다.
- 모델 `models/ticket.py:33`: `live_unique("ticket_bundle", "purchase_item_id")`. 31-32 주석에 「옛 번들 삭제 표시 → 새 번들 생성」을 적었다.
- 걸지 않은 셋을 확인했다. `prepaid_card.py` · `task.py`(`ticket_id`) · `purchase.py` 에 새 `live_unique` 가 없다. `task.py:232` 는 기존 `external_outbox` 것이다.
- SPEC 쪽: SPEC-000 1640 에 유일 표기가 있다. 남은 셋은 OQ-09-3(1827)으로 열어 두었다. SPEC-002 918 에 upsert 순서 한 줄이 들어갔다.
- downgrade 는 `drop_table(ticket_bundle)` 이 인덱스를 함께 지운다. 왕복 테스트도 통과했다.
- `test_constraints.py` 에 실제 PG 사례를 더했다. 살아 있는 두 번째 행은 23505 로 막히고, 지운 행의 값은 다시 쓸 수 있다. 기존 테스트 파일에 사례를 추가한 것뿐이다.

## 4. 기존 테이블 변경 0

- `git diff origin/dev --stat` 에서 앞과 달라진 것은 `tests/day/test_constraints.py`(+40) 하나뿐이다. 기존 migration 파일 변경은 0이다.
- 0010 upgrade 에서 기존 테이블을 건드리는 것은 `visit_task` add_column 3개(157-159) · FK 2개뿐이다. 앞과 같다. 11칸은 모두 0010 이 새로 만드는 테이블 안에 있다.

## 5. 1차 리포트 PASS 항목

- SPEC 대조 · 상용 운영 · KOS 칸 0 · `deleted_at` 28 / 28 · 범위 밖 2곳 모두 그대로다. 1차 §5 권고(bundle 만 걸고 나머지 셋은 보류)가 반영됐다.
- 1차 WARN 가운데 남은 것은 셋이다. WARN-2 `visit_task` FK 잠금, WARN-3 스냅샷이 칸 이름만 봄, WARN-4 새 테이블 FK 인덱스 0. 이번 지시 범위 밖이라 그대로 열려 있다.

## 6. 직접 실행

| 명령 | 결과 |
|---|---|
| `cd backend && uv run pytest -q tests/day/test_models.py tests/day/test_column_snapshot.py tests/migrations/test_sale_tables_migration.py` (지시 지정) | **95 passed** |
| `./scripts/test.sh -q backend/tests/migrations backend/tests/day/test_enum_labels.py backend/tests/day/test_constraints.py` (자체 격리 compose · 무작위 포트 · 사용자 포트 안 씀) | **61 passed**: 왕복 · head 하나 · `alembic check` 0 · enum 라벨 · 부분 유일 사례 |
| `./scripts/test.sh --pure -q` | **1415 passed** · 353 deselected |
| `ruff check backend scripts` · `scripts.devtools.architecture` | All checks passed · exit 0 |

## FAIL 고칠 곳

**없음.**
