# customer-erd backend 2단계 결과 보고 — KOS → DAY 동기화(메뉴 1시간 · 오늘 10초 · 5분 회차)

## 상태: done (커밋 · push · PR 없음 — 워크트리 변경만)

- 워크트리 `/Users/kknaks/orca/workspaces/CENTURION_DAY/customer-erd` · base `origin/dev` `bbd9220a`(시작 때 fetch — 나아가지 않음)
- Delivery #259 몫: D-2(매핑) · D-3 · D-4 · D-5 · D-6 · A3 · A4 · A5 · A6 · A7
- OQ-71: 코디 답대로 구현(아래 「계약 대조」)

## 수행 — 파일

새 파일(코드)
- `day/emr/normalized_sale.py` — 메뉴 · 구매 · 시술권 · 카드 · 병원 전체 변경의 우리 형식
- `day/emr/kos/mapper_sale_values.py` — **KOS 값 → DAY enum 매핑 표 한 곳**(㉔ 결정 5) · 금액 · 단위 · 열린 enum 읽기
- `day/emr/kos/mapper_menu.py` · `mapper_purchase.py` — 응답 → 우리 형식(필수 칸 없음 · 표 밖 값 → 그 행만 빼고 셈)
- `day/emr/kos/sale_reads.py` — ㉔ 원천 표의 경로 · 내부/공개 · 요청 키(`KosAdapter` 가 잇는 mixin)
- `day/emr/sync_sale_writes.py` — upsert(값 같으면 안 고침 · 같은 키 중복 막음) · 부모 아래 다시 만들기 · 소프트 딜리트
- `day/emr/sync_menu.py` · `sync_purchases.py` · `sync_tickets.py` · `sync_schedule_sales.py` — 반영
- `day/dtos/sale_sync_rows.py` — 새 28 테이블 쓰기 행(TypedDict · 모델 칸과 같은지 테스트)
- `day/services/emr_sale_sync.py` — 회차 셋(`run_menu` · `run_sales` · `run_sale_changes`)

고친 파일(더하기만 — 지금 함수의 동작 · 반환 · 호출 수 그대로)
- `day/emr/base.py` — 읽기 메서드 6개(기본 `None` = 지원 안 함 · `fetch_visit_tasks` 관례)
- `day/emr/normalized.py` — `NormalizedSchedulesData.sales`(기본 `()`) + 일정 참조 형식 2개
- `day/emr/kos/__init__.py` — mixin 잇기 · `fetch_schedules` 가 **같은 응답에서** 구매 · 처방 · 작업 참조를 따로 뽑는다(실패해도 판 그대로 — try 로 격리)
- `day/emr/factory.py` — 통계 장 크기 · 장 수 설정 주입
- `day/emr/sync_references.py` — `EntityModel` 유니온에 새 표 · `Refs.state()`(읽기 전용)
- `day/services/emr_sync.py` — `Job` 에 `menu` · `sales` · `sale_changes` · 잠금 TTL · `RunResult.sales` · `run_job`(=`_run` 공개 이름)
- `day/tasks/emr.py` — 기준 정보 태스크 뒤 `run_menu` · 일정 태스크 뒤 `run_sales`(오늘 일정이 있을 때만) · **새 5분 루프** `day.emr.sync_sale_changes` / `…_hospital` · `_isolated`(어떤 예외도 지금 태스크 반환값을 바꾸지 않음)
- `common/config.py` — 5분 주기 · 잠금 TTL 3개 · 통계 `limit`(50) · 장 수(20) · 첫 회차 되돌아볼 시간(300초)
- `day/identifiers.py` — 외부 id NewType 18개
- `day/models/{menu,purchase,prepaid_card,prescription}.py` · `migrations/versions/20261119_0010_sale_tables.py` — FK 인덱스 7개(아래)

테스트 · 고정본
- 새: `tests/day/emr/test_kos_sale_mapper.py`(22) · `test_sale_sync_rules.py`(11) · `test_sale_sync.py`(9 · infra) · `test_sale_sync_runs.py`(4 · infra)
- 고정본 15개 `tests/day/emr/fixtures/kos_{menu_*,medical_services,procedures,machines,medicines,etcetera_*,prepaid_card*,purchase_summaries,ticket_bundles,card_*,stat_*}.json`(HAR · openapi 키 모양 · **값은 전부 가짜**) + README 표

## 회차 구조 — 지금 동기화와 격리(브리프 「지킬 것」 1)

| 회차 | 언제 | 잠금 · 상한 | 지금 회차와의 관계 |
|---|---|---|---|
| 메뉴 ⑦ | `sync_master_hospital` 이 `run_master` **뒤에** | `menu` · 300초 | 따로 transaction · 예외는 `_isolated` 가 삼킴 → 태스크 반환은 master 상태 그대로 |
| 오늘 ① ~ ④ | `sync_schedules_hospital` 이 `run_schedules` 가 `done` 이고 그 응답에 일정이 있을 때 **뒤에** | `sales` · 60초 | 일정 목록을 **다시 받지 않는다**(`RunResult.sales` = 같은 응답) · 판 신호 · 「동기화 멈춤」(record_sync) 무관 |
| 병원 전체 변경 ⑤ ⑥ | 새 5분 루프 | `sale_changes` · 240초 | 새 태스크 |

- `visit_task` 새 칸 3개는 **판 반영(`sync_tasks`)이 아니라** `apply_task_refs` 가 따로 쓴다 — 판 반영의 칸 목록 · 생성 바인딩은 그대로. 같은 방문 advisory lock(`lock_visits`)을 같은 순서로 잡아 판 조작 · 일정 반영과 교착하지 않는다.
- 「바뀐 고객」은 알아챈 순간이 한 번뿐이라 병원별 Redis 집합 `day:emr:sale_customers:{병원}` 에 넣고 **시술권 · 카드를 commit 한 뒤에만 뺀다** — 회차가 끊겨도 다음 회차가 잇는다(테스트 있음). 한 회차 20명 상한.
- 「지난 회차 시각」(OQ-72)은 Redis `day:emr:sale_changes_at:{병원}` — 새 테이블 · 칸 없음. 성공한 회차의 끝 시각 · 통계 장 수 상한에 걸리면 옮기지 않는다. 처음 = 지금 - 300초(백필 아님).

## ㉔ 줄 → 코드

| ㉔ | 코드 |
|---|---|
| ① 일정 응답에서 추가 호출 없이 `purchaseIds` · `prescriptionIds` · `tasks[].procedureConfiguration` | `mapper_purchase.schedule_sale` ← `KosAdapter.fetch_schedules` · `sync_schedule_sales.purchase_visits` · `apply_prescriptions` · `apply_task_refs` |
| ② 내부 `get-purchase-summaries {purchaseIds, includeDeleted:true}` 묶음 | `sale_reads.fetch_purchases`(80개씩) · `sync_purchases.PurchaseApply` |
| ③ 바뀐 고객만 `get-ticket-bundles {visitorId}` · `get-prepaid-card-summaries {visitorId}`(available 없이) | `PurchasesResult.changed_customers`(구매 `lastUpdatedDateTimeUtc` ≠ `external_updated_at` · 새 구매) ∪ `ticket_changed_customers`(작업 `ticketId` ≠ `visit_task.ticket_id`) → Redis 집합 → `emr_sale_sync._customer_pass` |
| ④ 바뀐 카드만 이벤트 · 공유 고객 | `sync_tickets.changed_cards`(새 카드 · `updatedDateTimeUtc` 다름) → `fetch_prepaid_card_detail` → `apply_card_details` |
| ⑤ ⑥ 공개 통계 3개 · 지난 회차부터 · id 나열만 | `sale_reads.fetch_sale_changes`(`nextCursor` · 행의 id 칸만 읽음) → ② · ③ |
| ⑦ 메뉴 · 원천 표(내부 · 공개 3개) | `sale_reads.fetch_menu` · `sync_menu.MenuApply` |
| upsert = `external_ref` · `external_updated_at` | `Refs.link`(구매 · 카드 · 시술 항목에 KOS 바뀐 시각) |
| 삭제 = 소프트 딜리트만 | `sync_sale_writes.soft_delete` · `Refs.mark_absent` — DELETE 0(AST 테스트) |
| 사라짐: 메뉴 = 목록에서 빠짐 또는 `deleted:true` | `MenuApply._absent`(응답이 비거나 전부 매핑 실패면 표시 안 함 · `absence_keep`) |
| 사라짐: 구매 안 항목 · 거래 · 조정 · 담당은 그 구매 안에서 | `mark_absent(within=그 구매들)` · `replace_keyed`(부모 = 구매) · 하위 매핑 실패가 있는 구매는 그 종류 판단 안 함 |
| 시술권 응답에서 빠진 번들은 지우지 않음(OQ-73) · 번들 순서 「옛 번들 삭제 표시 → 새 번들 생성」 | `apply_tickets` · `_retire_other_bundles`(새 번들 upsert 전에) |
| 카드 행은 지우지 않음 · 공유 고객은 카드마다 비교 · 이력은 쌓기만 | `apply_cards`(`deleted_at` 있던 값 그대로) · `replace_keyed(prepaid_card_customer)` · 이력 upsert(지움 없음) |
| 처방: 그 일정 `prescriptionIds` 에서 빠짐 → `deleted_at`(범위 = 그 방문) | `apply_prescriptions` |
| 방문 없는 구매 건너뜀(OQ-69) | `purchase.visit_missing` 카운트 |
| 매핑 밖 값 건너뜀(OQ-70) | `mapper_sale_values` 표 + `MappingError` → `skipped` 카운트 |
| `external_ref.entity_type` 새 값 20 · KOS id 없는 하위 표는 부모 아래 다시 | `SaleEntityType` · `replace_links`(복합 PK) · `replace_keyed`(id 있는 하위 표) |
| 환경: DEMO 테넌트만 | 실물 확인 스크립트가 `hospitalName` 확인 + 구역 id 대조 뒤에만 진행(아래) |

## 계약 대조 — 결정 · OQ 기본값

- **OQ-71(코디 답)**: 담당 직원을 `external_ref` 로 찾는다(직원 행이 소프트 딜리트돼도 ref 는 남아 찾음 — 테스트 `퇴사_직원도…`). 정말 없을 때만 **그 거래 행만** 건너뛴다 · 구매 · 항목은 쓴다. 카운트 `purchase_transaction.staff_missing`(건수) · `purchase.with_skipped_transaction`(구매 수) · 로그 `purchase=<DAY id> transactions skipped …: n`(값 · 이름 없음). `staff_id` NOT NULL 그대로. 건너뛴 거래가 응답에 있으면 그 거래의 옛 연결은 사라짐으로 보지 않는다.
- OQ-69 · 70 · 72 · 73: 위 표의 기본값.
- 「반영 대기 칸 · DAY 에만 있는 칸」: 시술 항목 `price_amount` · `duration_minutes` · `recommended_interval_days` 는 동기화가 덮지 않는다(`keep_existing`).
- KOS id 칸 0 · 결제 설정 jsonb 에서 `…Id` 키를 뺀다(선불카드 결제 = `{prepaidCardName}` 만).

## FK 인덱스 (0010 에 · 새 테이블에만)

동기화가 부모 아래 행을 고르는데 PK · 유일 인덱스가 앞 칸으로 덮지 않는 것만 7개:
`purchase_item(purchase_id)` · `purchase_transaction(purchase_id)` · `purchase_price_adjustment(purchase_id)` · `purchase_assignee(purchase_id)` — 구매 안 사라짐 · 다시 만들기 / `prepaid_card_customer(prepaid_card_id)` — 카드마다 비교 / `prescription(visit_id)` — 방문 안 사라짐 / `product_option_composition(option_id)` — 옵션 아래 다시 만들기.
덮여서 안 넣은 것: `product_category_link` · `product_option_price` · `treatment_item_machine/_medicine`(복합 PK 앞 칸) · `ticket_bundle.purchase_item_id`(부분 유일) · `external_ref`(기존 유일 · 인덱스). 0010 칸 변경 없음.

## 검증 — 명령과 수치

| 명령 | 결과 |
|---|---|
| `uv run pytest -q tests/day/emr/test_kos_sale_mapper.py tests/day/emr/test_sale_sync_rules.py` | **33 passed** |
| `./scripts/test.sh -q backend/tests/day/emr/test_sale_sync.py backend/tests/day/emr/test_sale_sync_runs.py`(격리 PG · Redis) | **13 passed** |
| `./scripts/test.sh -q backend/tests/migrations backend/tests/day/test_enum_labels.py backend/tests/day/test_constraints.py backend/tests/day/emr` | **271 passed**(0010 왕복 · head 하나 · `alembic check` 차이 없음 · FK 인덱스 포함) |
| `./scripts/test.sh -q`(전체) | **1814 passed** — 판(board) 테스트 전부 포함(A5) |
| `./scripts/test.sh --pure -q` | **1448 passed** · 366 deselected |
| `./scripts/check.sh --pure` | 구조 · ruff · format · mypy · Taut audit/check **통과**. frontend 단계만 실패 — **무관**(워크트리 npm 미설치 `@tailwindcss/postcss` · 프론트 변경 0 · 1단계와 같음) |
| 물리 DELETE grep(`day/emr/**` · `emr_sale_sync` · `emr_sync` · `tasks/emr`) | **0**(A6) |

A7 테스트 범위: 매핑(표 값마다 · 표 밖 값 건너뜀) · upsert(새로 · 바뀜 · 같으면 0) · 사라짐(메뉴 · 구매 안 항목 · 처방 · 공유 고객) · 되살림 · 응답 비면 사라짐 안 함 · OQ-69 · OQ-71(+ 퇴사 직원) · 번들 순서(부분 유일에 안 막힘) · 바뀐 고객만 · 끊겨도 다음 회차가 잇기 · 5분 회차 시각(첫 회차 · 상한이면 안 옮김) · 회차 격리(새 회차가 예외를 내도 일정 · 기준 정보 태스크 결과 그대로) · 쓰기 행 = 모델 칸.

## DEMO 실물 확인 (A3 · A4) — 로컬 · 버리는 PG16 · Redis7 컨테이너(임의 포트 · 끝나면 지움)

- KOS 연결: **사용자 테스트 계정**(`~/.config/day/kos-test-account.env` · 값 출력 안 함) + DEMO 지점 공개 키 · `KOS_CLIENT_TAG=local`. 데모 시스템 계정 · 명동점 키 사용 0.
- 테넌트: `get-user-tenants` 2개 중 `hospitalName` 에 DEMO 가 들어간 것 1개(정확히 「DEMO」인 것은 없음) → **내부 구역 id(그 테넌트) = 공개 구역 id(DEMO 키) 2/2 일치를 확인한 뒤에만** 진행. 다른 테넌트에는 테넌트 경로 호출 0.
- 순서: 기준 정보 → 일정 → 메뉴 → 오늘 → 5분 → 일정 → 오늘(두 번째).

| 메뉴(A3) | DAY | 조사 리포트 |
|---|---|---|
| 카테고리 | 15 | 15 |
| 상품 | 103 | 103(내부) |
| 옵션 | 326 | 326(내부) |
| 시술 | 804 | 804 |
| 시술 항목 | 226 | 226 |
| 기기 · 약물 | 302 · 349 | 302 · 349 |
| 선불카드 상품 | 8 | 8 |
| 시술 외 품목(분류) | 11(3) | 11(3) |
| 기타 작업 | 10 | 10 |
| 옵션 가격 · 카테고리 연결 · 항목↔기기 · 항목↔약물 | 1 · 103 · 63 · 159 | 가격 1 |
| 코스 구성 | **0**(34 건너뜀 — 아래 발견 2) | 34 |

| 오늘(A4) | 값 |
|---|---|
| 오늘 일정 · 고객 | 4 · 4 |
| 구매(살아 있음 / 받음) · 항목 · 거래 · 담당 · 가격 조정 | 2 / 3(1 = KOS 지움 → `deleted_at`) · 2 · 1 · 3 · **1** |
| 바뀐 고객 · 시술권 번들 · 세트 · 티켓 | 3 · 2 · 2 · 6 |
| 선불카드 · 이력 · 공유 고객 | 6 · 17 · 0(1 = 공유 고객이 DAY 에 없음) |
| 새 `external_ref` | 2,196 |
| 두 번째 오늘 회차 | 쓴 행 0 · 다시 받은 고객 0(**바뀐 고객만** 확인) |
| 5분 회차 | 지난 5분 통계 행 0 · `done` |
| 판 칸 해시(새 동기화 전 = 후) | **같음**(A5) |
| 처방 · `visit_task` 새 칸 | 0 · 0 — 데모 오늘 방문에 작업이 없음 · 처방 표본 없음(OQ-75). 경로는 infra 테스트가 덮음 |
| KOS 세션 | 이 작업이 만든 테스트 계정 로그인(앞서 중간에 끊긴 실행 2번 것 포함 · 같은 UA `local` · 최근 60분)을 모두 해제 · 마지막 확인 때 같은 UA 남은 것 0 |

## 실물에서 찾은 것 · 코디가 확인할 것 (SPEC 갱신 필요 표시 ★)

1. ★ **카드 이력 `chargingId` 가 행마다 유일하지 않다** — 환불 한 이벤트가 `REFUND BALANCE` · `REFUND POINT` 두 행을 **같은 `chargingId`** 로 준다(데모 실물). SPEC-000 「KOS 이벤트 `chargingId` 는 `external_ref`」대로면 한 행만 남는다(첫 실물 실행에서 upsert 충돌로 확인). → 이력의 외부 id 를 **`chargingId:주머니`**(`chg:balance` · `chg:point` — 작업의 `일정 id:sequence` 꼴)로 두고, 거래 연결은 원래 `chargingId` 로. SPEC 표 · ㉔ 「`prepaid_card_ledger` = `chargingId`」 줄을 고쳐야 한다.
2. ★ **코스 구성 `compositions[].title` 이 실물에서 비어 온다**(34/34 · HAR 표본에는 있었다). `title` 은 필수(NOT NULL) · 다른 칸으로 추정 금지라 **구성만 건너뛰고 옵션은 쓴다**(옵션 326 ✓ · 구성 0 · 카운트 `product_option_composition` 34). 구성 이름을 비울 수 있게 할지(nullable) · 시술 항목 이름을 쓸지는 SPEC 결정.
3. ★ **티켓 상태 `CANCELED` 가 실물에 있다**(4장). SPEC enum(`available · in_use · used`)에 없어 OQ-70 대로 **그 티켓만** 건너뛴다(번들 · 세트는 쓴다 · `ticket.status_unknown`). enum 에 `canceled` 를 더할지 결정 필요(마이그레이션 필요 — 0010 이 아직 어디에도 적용 안 됐으면 0010 에).
4. **가격 조정 표본이 생겼다** — 데모 오늘 구매에 `priceAdjustments` 1건(OQ-08-4 「표본 0」이 바뀜). 지금은 관계 칸만 쓴다(칸 미정).
5. **열린 구매의 담은 항목은 `pendingItems[]`** 에 있고 `items[]` 는 비어 있다(HAR). SPEC 은 `items[]` 만 정해 그대로 따랐다 — 열린(`initialized`) 구매는 DAY 에서 항목 0 으로 보인다. `pendingItems` 를 받을지 SPEC 결정.
6. **번들 21개를 출처 구매 항목이 DAY 에 없어 건너뛰었다**(`ticket_bundle.purchase_item_missing`) — 오늘 고객의 지난 구매(오늘 일정의 `purchaseIds` 밖)라서다. `ticket_bundle.purchase_item_id` 가 필수라 지난 이력 백필(OQ-00-3 · 범위 밖)이 들어와야 채워진다. 그 전엔 오늘 고객의 옛 시술권이 DAY 에 없다.
7. 선불카드 상품은 SPEC 요청 키 `{closed:false}` 그대로라 **닫힌 상품은 응답에 없어 `deleted_at`** 이 된다(`is_closed` 는 늘 false). 닫힌 상품도 받으려면 요청 키 변경이 SPEC 에 필요.
8. 공개 openapi 의 시술 항목에는 `priceAmount` · `durationTime` · `recommendedInterval` 이 있다. SPEC(2026-11-19)이 「KOS 원천 없음 — 비워 둔다」라 받지 않았다(실물 응답에 키가 있는지는 확인 안 함).
9. 환불 완료 카드에 `deleted_at` 을 동기화가 채우지는 않는다(SPEC 「DAY 는 환불 완료 때」 — 동기화 규칙 아님으로 읽음 · 카드 행은 지우지도 되살리지도 않음).
10. 새 28 테이블 쓰기 행은 생성기(`scripts/devtools/sync_contracts`)가 jsonb(`Any`) 칸을 받지 않아 **손으로 둔 TypedDict**(`dtos/sale_sync_rows.py`) + 모델 칸 일치 테스트로 지킨다. `scripts/` 는 allowed_paths 밖이라 생성기를 넓히지 않았다 — 나중에 생성기에 jsonb 타입을 열면 옮길 수 있다.
11. 오늘 회차의 시술권 · 카드 고객은 한 회차 20명 상한(나머지는 Redis 집합에 남아 다음 회차). 5분 회차 통계는 장 50 · 회차 20장 상한(OQ-72 — 설정으로 바꿀 수 있음).
12. `day/emr/kos/demo/kos_board.py` 는 1단계의 이름 변경 그대로(이번에 더 건드리지 않음).

## 실물 발견 반영 (지시 `sync-fix-1.md` · 2026-11-19)

| # | 반영 | 파일 |
|---|---|---|
| F-1 | 확인만 — 이력 외부 id = `chargingId:주머니` · 거래 연결 = 원래 `chargingId`(앞 절 그대로). 실물: 이력 ref 17/17 이 주머니 붙은 꼴 | `mapper_purchase.ledger` · `sync_tickets.apply_card_details` |
| F-2 | `product_option_composition.title` **null 허용**(모델 · 0010 · 쓰기 행). 구성을 건너뛰지 않고 이름을 비운 채 쓴다 — 다른 칸으로 채우지 않는다. 앞 절의 「구성 건너뛰기」 코드는 지웠다 | `models/menu.py` · `0010` · `dtos/sale_sync_rows.py` · `mapper_menu.py` · `sync_menu.py` · `normalized_sale.py` |
| F-3 | `ticket_status` enum 에 **`canceled`**(0010 · `TicketStatus` · 매핑 `CANCELED → canceled`) | `enums/ticket.py` · `0010` · `mapper_sale_values.py` |
| F-4 | 구매 항목 = `items[]` + `pendingItems[]`(같은 `purchase_item` · 같은 id 가 둘에 있으면 `items`). 확정되면 같은 id → 같은 DAY 행 upsert · id 가 바뀌어 빠지면 구매 안 사라짐 → `deleted_at` | `mapper_purchase.purchase` |
| F-5 | `get-prepaid-card-product` 를 `{closed:false}` · `{closed:true}` 두 번 받아 합친다 · `is_closed` = 응답 값 · 닫힌 상품은 사라짐 아님 | `sale_reads.fetch_menu` |

- 0010 은 이름 · 칸 수 그대로(칸 스냅샷 변화 없음) — `title` nullable · enum 값 1개만 바뀜. 지금 테이블 변경 0 그대로.
- 테스트: F-2(이름 빈 구성 `opt-3` 도 씀 · 구성 3) · F-3(`CANCELED` 매핑 · 티켓 6 · 표 밖 값은 여전히 1 건너뜀) · F-4(`pendingItems` 수신 · **담은 항목 확정 = 같은 행 · id 바뀌면 사라짐** 새 infra 테스트) · F-5(두 번 부름 · 닫힌 상품 `is_closed=True` · 응답 id 에 포함). 고정본: `kos_prepaid_card_products_closed.json` 새로 · 구매 고정본에 `pendingItems` · 시술권 고정본에 `CANCELED`.

### 검증

| 명령 | 결과 |
|---|---|
| `uv run pytest -q tests/day/emr/test_kos_sale_mapper.py tests/day/emr/test_sale_sync_rules.py` | 33 passed |
| `./scripts/test.sh -q backend/tests/migrations backend/tests/day/test_enum_labels.py backend/tests/day/test_constraints.py backend/tests/day/emr` | 272 passed(0010 왕복 · `alembic check` 차이 없음 · enum 라벨 포함) |
| `./scripts/test.sh -q`(전체) · `--pure` | **1815 passed** · 1448 passed |
| `./scripts/check.sh --pure` | 구조 · ruff · format · mypy · Taut 통과 · frontend 만 npm 미설치(무관 · 앞과 같음) |

### DEMO 실물 다시 확인 (같은 방식 — 버리는 컨테이너 · 테스트 계정 · DEMO 테넌트 구역 대조 뒤 · 세션 해제)

| 볼 것 | 앞 | 지금 |
|---|---|---|
| 코스 구성(F-2) | 0(34 건너뜀) | **34**(이름 비움 34) |
| 선불카드 상품(F-5) | 8 | **20**(열림 8 + 닫힘 12) · `deleted_at` 0 |
| 열린 구매 · 그 항목(F-4) | 1 · 0 | 1 · **2** |
| 구매 항목 전체 | 2 | 5 |
| 티켓 상태 매핑 실패(F-3) | 4(`CANCELED`) | **0** — `CANCELED` 4장은 출처 구매 항목이 없는 지난 번들에 있어(백필 몫) 오늘은 0장 쓰임 |
| 이력 외부 id(F-1) | — | 17/17 `chargingId:주머니` · 오늘 선불카드 결제 거래 0이라 거래 연결 0 |
| 메뉴 건수 | 15 · 103 · 326 · 804 · 226 · 302 · 349 · 11 · 10 | 같음 |
| 매핑 실패 | 38 | **0** |
| 판 칸 해시 | 같음 | **같음** |
| 두 번째 오늘 회차 | 쓴 행 0 | 쓴 행 0 · 고객 0 |
| KOS 세션 | 해제 | 4 해제 · 같은 UA 남은 것 0 · 컨테이너 0 |

- 가격 조정 행이 1 → 3(열린 구매의 담은 항목에 붙은 조정까지 받음 · OQ-08-4 칸 미정 그대로 관계만).
- 남은 것: 지난 구매의 시술권 21 번들(백필 몫) · 오늘 처방 · 작업 0(데모 표본 없음).

## 검수 3 반영 + 내부 API 만 (지시 `sync-fix-2.md` · `sync-fix-3-internal-only.md` · 2026-11-19)

`sync-fix-3` 이 우선 — 5분 회차를 **회차째 뺐다**(WARN-3 · WARN-4 는 없던 것). 나머지 `sync-fix-2` 는 그대로 했다.

### sync-fix-2

| # | 반영 | 파일 |
|---|---|---|
| FAIL-1 | 고객의 시술권 · 카드를 commit 한 뒤에도 DAY 에 없는 그 고객의 오늘 작업 티켓 → 병원별 Redis 집합 `day:emr:sale_unresolved_tickets:{병원}`(만료 = 병원 현지 오늘 끝까지 · 회차 시계 기준 남은 초). `ticket_changed_customers` 는 이 집합의 티켓(그리고 DAY 에 없는 경우)으로는 고객을 다시 큐에 넣지 않는다. `ticketId` 가 바뀌면 다른 id 라 다시 부르고, 구매가 바뀌면 지금처럼 부른다. 원인 구분 없이 「받아도 안 풀림」이면 넣는다(출처 구매 항목 없음 · 응답에 없음 · 표 밖 상태) | `sync_schedule_sales.py`(`unresolved_tickets` · `ticket_changed_customers(…, unresolved)`) · `emr_sale_sync.py` |
| WARN-1 | 오늘 구매 회차 = **별도 태스크 `day.emr.sync_sales_hospital`**. 일정 태스크는 `run_schedules` 뒤 `.kiq(병원, 메시지)` 만 하고 기다리지 않는다 — 일정 태스크의 실행 시간 · DB 풀은 새 동기화 전과 같다. 메시지 = 그 일정 응답의 참조(`sales_payload` — 방문 · 고객 · 구매 · 처방 외부 id · 작업 sequence · 티켓 · 시술 항목 id · 기기 이름)라 KOS 를 다시 부르지 않는다. 발행이 실패해도 일정 태스크 결과는 그대로(로그만) | `tasks/emr.py` · `emr_sale_sync.sales_payload` · `sales_from_payload` |
| WARN-2 | `fetch_schedules` 안 `schedule_sale` 을 `except Exception`(+ `noqa: BLE001` · `_isolated` 와 같은 이유 주석)으로 — 판 반영은 계속, 그 일정의 참조만 건너뛰고 `NormalizedSchedulesData.sales_skipped` 로 센다 | `emr/kos/__init__.py` · `normalized.py` |
| WARN-5 | 아래 테스트로 덮음 — 격리 테스트가 「판 입력(`visits` · `skipped_external_ids`) 같음」을 직접 본다 | |

### sync-fix-3 — 공개 API 0

| 무엇 | 반영 |
|---|---|
| 메뉴 시술 항목 · 기기 · 약물 | 공개 `get-medical-services` · `get-machines` · `get-medicines` 뺌 → 내부 `get-products` 의 살아 있는 상품 · 옵션 · 구성 `medicalService`(+ `configuration.machines[]` · `medicines[]` · `procedure`)에서 모은다. id 로 중복을 빼고, 같은 시술 항목이 여러 번이면 `updatedDateTimeUtc` 가 가장 늦은 것 하나(`sale_reads.menu_services` · `service_parts`). 시술(`treatment`)은 내부 `get-procedures` 그대로 |
| 세 테이블의 사라짐 | **소프트 딜리트 안 함** — 옵션에서 빠졌다고 지우지 않는다(`sync_menu` 에서 세 종류 `_absent` 호출 뺌). **`external_ref.is_present_in_source` 도 갱신하지 않는다**(결정): 지금 관례에서 「있음 false」는 `deleted_at` 과 짝(`mark_absent`)인데, 옵션에서 빠진 것은 KOS 에서 지워진 게 아니라 반쪽만 쓰면 뜻이 섞인다. 받을 때마다 `link` 가 「있음」으로 둔다. 시술 항목 ↔ 기기 · 약물 연결은 **받은 시술 항목에 한해** 그 항목의 목록으로 다시 맞춘다(그 항목 설정의 목록이라 정확) |
| 5분 회차 | 뺐다 — 루프 · 스케줄(`day.emr.sync_sale_changes` · `…_hospital`) · Redis 표시(`sale_changes_at`) · `run_sale_changes` · 어댑터 `fetch_sale_changes` · 통계 읽기 · `NormalizedSaleChangesData` · 설정 5개(주기 · 잠금 TTL · 통계 limit · 장 수 · 첫 회차) · 잠금 `sale_changes` · 고정본 3개. 오늘 밖 고객의 변경은 OQ(후보 = 내부 `visitor/v2/queries/get-visitors` 하루 한 번) |
| 기존 운영 코드 — 구역 | `PATH_ZONES` = 내부 `schedule/zone/v1/queries/get-zones`(`fetch_master` · `fetch_schedules` 캐시 빔 두 곳 `_list("internal", …)`). 응답 칸 같음(HAR `수납필요 확인.har` 내부 응답 `id · isDefault · order · title` = 공개 고정본) — `mapper.zone` 그대로. **운영 루프에서 공개 토큰(`exchange-token`)을 받지 않는다**(테스트 · 실물 확인). `open_api_key` 필수 · `client.call("open", …)` 기능은 그대로(데모 시드 `emr/kos/demo/` 가 씀) |
| 새 코드가 공개를 못 부르게 | `sale_reads.ApiKind = Literal["internal"]`(타입으로 막음) |

### grep — `"open"` 호출 · 공개 경로(운영 경로 · demo 제외)

```
$ grep -rn '"open"' backend/day/emr backend/day/services/emr_sale_sync.py backend/day/services/emr_sync.py backend/day/tasks/emr.py | grep -v '/demo/'
backend/day/emr/kos/client.py:58:ApiKind = Literal["open", "internal"]
backend/day/emr/kos/client.py:411:        if api not in ("open", "internal"):
backend/day/emr/kos/client.py:413:        url = self._open_url(path) if api == "open" else self._internal_url(path)
backend/day/emr/kos/client.py:416:            if api == "open":
backend/day/emr/kos/client.py:430:        return await self.call("open", path, body)
$ grep -rn '/open/' backend/day/emr backend/day/services backend/day/tasks | grep -v '/demo/'
backend/day/emr/kos/writes.py:31:  (주석 — cc 의 옛 공개 경로 설명)
backend/day/emr/kos/__init__.py:22:  (주석 — 직원 목록을 공개 대신 내부로 받는 설명)
```

남은 것은 클라이언트의 「공개로 부르는 기능」 정의(`client.call` · `client.open` — 남기라는 지시) · 주석뿐 — **운영 경로의 공개 호출 0**. 새 코드는 AST 테스트(`test_새_동기화_코드는_공개_API_를_부르지_않는다`)로 `"open"` 인자 · `/open/` 경로 0 을 지킨다.

### 테스트

- 새 · 바뀐: FAIL-1 `test_풀리지_않는_티켓은_그날_다시_부르지_않는다`(첫 회차 시술권 받음 · 집합 + TTL ≤ 24h · **두 번째 회차 호출 = 구매만** · 티켓 id 가 바뀌면 다시 부름) · WARN-1 발행만(기다리지 않음) · 발행 실패해도 `done` · 메시지 왕복(JSON) · WARN-2 `schedule_sale` 이 아무 예외(KeyError)를 내도 `fetch_schedules` 의 `visits` · `skipped_external_ids` 같음 · 내부만: 메뉴 호출이 전부 `internal` · 시술 항목 · 기기 · 약물은 상품 응답에서 id 로 모음 · **세 테이블은 옵션에서 빠져도 `deleted_at` 없음 · `is_present_in_source` 그대로** · 운영 기준 정보 · 일정 회차에 `exchange-token` 0 · 공개 호출 0 · 5분 태스크 없음.
- `./scripts/test.sh -q backend/tests/day/emr backend/tests/migrations backend/tests/day/test_enum_labels.py backend/tests/day/test_constraints.py` **282 passed**
- `./scripts/test.sh -q`(전체) **1825 passed** · `--pure` **1457 passed**
- `./scripts/check.sh --pure` 구조 · ruff · format · mypy · Taut 통과 · frontend 만 npm 미설치(무관 · 같음)

### DEMO 실물 (같은 방식 · 테스트 계정 · DEMO 테넌트만 · 세션 해제 · 버리는 컨테이너)

- 테넌트: `hospitalName` 에 DEMO 가 들어간 것 1개 · 다른 하나는 아님. (앞 회차의 공개 키 구역 대조는 공개 API 라 이번엔 하지 않았다 — 같은 테넌트 id 가 앞 세 번의 대조에서 2/2 일치했다.)
- **공개 토큰을 받지 않음**(`exchange-token` 0 — 어댑터의 공개 토큰이 끝까지 비어 있음).

| 볼 것 | 앞(공개 포함) | 지금(내부만) |
|---|---|---|
| 구역 · 방 · 오늘 방문 | 구역 2(조사) · 방 — · 방문 4 | 구역 2 · 방 41 · 방문 4 |
| 시술 항목 | 226 | **226**(데모는 모든 시술 항목이 어떤 옵션 · 구성에 쓰인다) |
| 기기 · 약물 | 302 · 349 | **19 · 44**(쓰이는 것만 · HAR 「기기 19종 · 약품 41종」과 같은 규모) |
| 항목 ↔ 기기 · 약물 연결 | 63 · 159 | 63 · 159(같음) |
| 카테고리 · 상품 · 옵션 · 구성 · 시술 · 선불카드 상품 · 시술 외 · 기타 작업 | 15 · 103 · 326 · 34 · 804 · 20 · 11 · 10 | 같음 |
| 오늘 구매 · 항목 · 열린 구매의 항목 | — | 3(받음 5 · KOS 지움 2) · 11 · 열린 구매 2 / 항목 6(오늘 데모 데이터가 앞 실행보다 늘었다) |
| 판 칸 해시(새 동기화 전 = 후) | 같음 | **같음** |
| 두 번째 오늘 회차 | 0 | **쓴 행 0 · 다시 받은 고객 0** |
| KOS 세션 | 해제 | 해제(같은 UA 남은 것 0) · 컨테이너 0 |

- FAIL-1 길(못 푸는 티켓을 쓰는 오늘 작업)은 데모 오늘 방문에 작업이 0건이라 실물로는 지나지 않았다 — infra 테스트로 덮음.
- 일정 태스크 → 오늘 구매 태스크 발행은 실물 스크립트에서 같은 메시지 왕복(`sales_payload` → `sales_from_payload`)으로 돌렸다(taskiq 브로커 자체는 띄우지 않음).

### 남은 것 · 주의

- 오늘 밖 고객(오늘 일정 없는 고객)의 결제 · 환불 · 카드 사용은 이제 받지 않는다(OQ · 후보 = 내부 고객 목록 하루 훑기).
- 옵션에서 빠진 시술 항목 · 기기 · 약물은 DAY 에 남는다(지우지 않음 · `is_present_in_source` true 그대로) — 「지금 쓰이는가」는 옵션 쪽 참조로 판단해야 한다.
- 풀리지 않은 티켓 집합은 하루 단위라, 같은 날 백필이 들어오면 그 고객은 다음 날(또는 구매 변경 · 티켓 변경 때) 다시 받는다.
