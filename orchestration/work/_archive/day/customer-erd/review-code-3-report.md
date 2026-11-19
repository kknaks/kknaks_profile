# 리뷰 리포트 — customer-erd / code 3 (2단계 동기화 전체 + 실물 발견 반영) (2026-11-19)

- 대상: `git diff origin/dev`(20 파일) + 미추적(코드 11 · 모델/enum/0010 · 테스트 4 · 고정본 17) · base `origin/dev` `bbd9220a`(fetch — 그대로)
- 계약: SPEC-002 개정 ㉔(실물 반영 포함) · SPEC-000 §4(2026-11-19 개정) · 발주 `customer-erd-be-2-brief.md` 지킬 것 1~4 · `sync-fix-1.md` F-1~F-5 · `_RESUME.md` OQ-71 코디 답
- 워커 리포트 `be-2-report.md` 는 diff · 실행으로 재확인.

## 판정: **FAIL 1 · WARN 5**

| 축 | 판정 |
|---|---|
| 1. 기존 동기화 격리 | **PASS**(WARN-1 · WARN-2) |
| 2. ㉔ 대조 | **PASS**(WARN-3) |
| 3. 소프트 딜리트 | **PASS** |
| 4. F-1~F-5 · OQ-71 | **PASS** |
| 5. 0010 변경 | **PASS** |
| 6. 보안 · 개인정보 | **PASS** |
| 7. 부하 | **FAIL-1**(시술권 고객 10초 무한 재조회) · WARN-4 |
| 8. 테스트 | **PASS**(WARN-5) |
| 9. 직원이 실물에서 만날 자리 | **없음** |

---

## FAIL

### FAIL-1 — 지난 구매 시술권을 쓰는 오늘 작업의 고객이 **10초마다 영원히** 「바뀐 고객」이 된다 (지킬 것 4 · ㉔ 「10초마다 오늘 고객 전부를 부르지 않는다」)

- `day/emr/sync_schedule_sales.py:155` — `ticket_changed_customers` 는 작업의 `ticketId` 가 DAY 에 **없으면**(`t.ticket_id is None`) 그 고객을 「바뀜」으로 본다(㉔ 「DAY 에 없는 티켓 포함」 문구 그대로).
- `day/emr/sync_tickets.py:85-88` — 그 고객의 시술권을 받아도 출처 구매 항목이 DAY 에 없는 번들은 `ticket_bundle.purchase_item_missing` 로 **건너뛰고**, 그 번들의 세트 · 티켓은 `external_ref` 에 연결되지 않는다(티켓 link 는 `kept` 번들 아래만).
- → 다음 10초 회차에도 그 티켓은 DAY 에 없다 → 같은 고객을 다시 큐(`_queue_customers`)에 넣는다 → `get-ticket-bundles` + `get-prepaid-card-summaries` **2호출 × 그 고객 × 10초마다 하루 종일**. 상한 `CUSTOMERS_PER_RUN = 20`(`services/emr_sale_sync.py:62`)이라 병원당 최대 **40호출 / 10초** 늘어난다.
- 드문 경우가 아니다: 다회권은 **지난 방문에 산 시술권을 오늘 쓰는 것**이 기본이다. 데모 실물에서도 오늘 고객의 지난 번들 21개가 이 이유로 건너뛰어졌다(be-2 「실물에서 찾은 것」 6). 백필(OQ-00-3 · 범위 밖)이 들어오기 전까지 prod 모든 병원에서 계속된다.
- 데모 2회차 「다시 받은 고객 0」 은 데모 오늘 방문에 작업이 0건이라 이 길을 지나지 않았다(be-2 표 「`visit_task` 새 칸 0」). 테스트 `test_오늘_회차는_바뀐_고객만…`(`test_sale_sync_runs.py:145`)도 풀리는 티켓(`tkt-1`)만 본다.
- **고칠 곳(제안 · 방식은 코디 판단)**: 「DAY 에 없는 티켓」을 한 번 받아 본 뒤에도 못 푼 경우 다시 큐에 넣지 않게 — 예) 고객의 시술권을 받은 뒤에도 없던 티켓 id 를 병원별 Redis 집합(TTL)에 두고 `ticket_changed_customers` 에서 제외, 또는 「KOS `ticketId` 가 지난 회차에 본 값과 다름」으로만 판단. + 그 길의 테스트(못 푸는 티켓 → 두 번째 회차 호출 `["purchases"]` 만). SPEC-002 ㉔ 「바뀐 것만」 표 문구(「DAY 에 없는 티켓 포함」)도 함께 고쳐야 한다 → planner.

## WARN

- **WARN-1 (격리 — 시간)** `day/tasks/emr.py:79` — 오늘 구매 회차를 일정 태스크 **안에서 await** 한다. 예외 · 반환은 `_isolated` 로 완전히 떼었고 일정 잠금 · commit 은 이미 끝난 뒤라 판 반영 결과는 안 바뀐다. 다만 일정 태스크 한 건의 실행 시간이 sales 상한(60 − 5초)까지 늘고, worker 1 프로세스의 DB 풀(5 + 5 · `common/config.py:86-87`)을 같이 쓴다. 세션은 외부 호출 밖에서만 잡아(`emr_sale_sync._customer_pass`) 지금은 문제 없어 보이나, 병원 수가 늘면 판 반영의 풀 대기가 생길 수 있다. 별도 태스크 발행(`.kiq`)으로 떼는 방법이 있다 — 사용자 판단.
- **WARN-2 (격리 — 예외 범위)** `day/emr/kos/__init__.py:196` — 판 경로(`fetch_schedules`) 안에서 `schedule_sale` 를 `except MappingError` 로만 감쌌다. 지금 `schedule_sale` 이 쓰는 도우미(`text` · `obj` · `items` · `integer` · `names`)는 모두 타입 검사형이라 다른 예외가 날 길은 읽어서는 없다. 그래도 이 줄이 터지면 **판 동기화 전체가 멈추는** 자리라, `except Exception`(+ `noqa: BLE001`, `_isolated` 와 같은 이유)로 넓히는 것을 권고.
- **WARN-3 (㉔ ⑥)** `day/emr/kos/sale_reads.py` `fetch_sale_changes` · `services/emr_sale_sync.py:270-280` — 카드 이벤트 통계의 **카드 id 는 세기만** 하고 ④(이벤트 · 공유 고객)를 직접 부르지 않는다. 소유자를 ③ 으로 다시 받고 카드 `updatedDateTimeUtc` 가 바뀌어야 ④ 가 돈다. ㉔ ⑥ 「카드 id … → 카드 ④」와 한 단계 다르다 — 충전 이벤트가 카드 수정 시각을 안 바꾸면 이력을 놓친다(실측 없음). 사용자 판단 / OQ.
- **WARN-4 (부하 — 5분 회차 정체)** `services/emr_sale_sync.py:279` · `sale_reads.py:294` — 장 수 상한(20장 × 50)에 걸리면 표시를 옮기지 않아 다음 회차가 **같은 시각부터 같은 20장**을 다시 받는다. 한 5분 창에 1,000행을 넘는 병원은 영원히 앞으로 못 간다(+ 매 5분 60호출). 상한에 걸렸을 때 받은 마지막 행 시각까지는 옮기는 식이 필요할 수 있다 — 지금 규모(데모 5분 0행)에선 일어나지 않음.
- **WARN-5 (테스트)** 격리 테스트 `test_sale_sync_rules.py:113` 은 새 회차가 **예외를 낼 때 태스크 반환값**이 같은지만 본다(목). ① 느린 새 회차(시간) ② 판 경로 안 `schedule_sale` 실패(WARN-2) ③ 판 DB 결과 동일은 테스트가 아니라 워커 DEMO 「판 칸 해시 같음」으로만 확인됐다. FAIL-1 길의 테스트도 없다.

---

## 축별 근거

### 1. 기존 동기화 격리 — PASS

- 기존 함수 동작 · 반환 · 호출 수: `run_schedules` 는 응답을 `captured` 로 넘기기만(`services/emr_sync.py`) · `RunResult.sales` 기본 `()` · `Job` 에 값만 추가 · `run_job` = `_run` 공개 이름. `fetch_schedules` 는 **같은 응답**에서 `schedule_sale` 을 뽑아 KOS 호출 0 증가. 판 반영 `sync_tasks` 칸 목록 그대로 — `visit_task` 새 칸 3개는 `apply_task_refs` 가 따로(같은 `lock_visits` 순서 · DB 만 하는 짧은 transaction).
- 잠금 · 상한 · transaction: `menu`(300) · `sales`(60) · `sale_changes`(240) 가 별도 Redis 잠금 · `asyncio.timeout` · 별도 세션. `_run` 이 못 잡는 예외(IntegrityError 등)는 `_isolated`(`tasks/emr.py:52-58`)가 잡아 지금 태스크 반환을 지킨다. 메뉴는 `run_master` **뒤**, 오늘은 `run_schedules` 가 `done` 이고 일정이 있을 때만 **뒤**.
- 「동기화 멈춤」(`record_sync`) · 판 신호는 일정 회차에서만 — 새 회차 실패가 판 상태 표시에 안 닿음.

### 2. ㉔ 대조 — PASS

- 경로 16개(`sale_reads.py:45-75`) · 내부/공개 구분 · 요청 키가 ㉔ 「테이블별 원천」 표와 한 줄씩 같다: 카테고리 `{sort}` · 상품 `{deleted:false, includePromotions:false}` · 시술 `{deleted:false}` · 공개 시술 항목/기기/약물 `{}` · 기타 작업 `{}` · 선불카드 상품 `{closed:false}`·`{closed:true}` 두 번 · 시술 외 `{deleted:false}` · 구매 `{purchaseIds, includeDeleted:true}`(80개씩 · 조사 87 됨) · 시술권 · 카드 요약 `{visitorId}`(`available` 없음) · 이벤트 · 공유 고객 `{id}` · 통계 3개 기간 키 이름 통계마다(㉔ 그대로) + `limit` · `cursor`. 지어낸 경로 · 필드 0.
- 공개 통계는 `stat_ids` 로 id 만 읽음(결정 9) ✓.
- 바뀐 것만: 구매 `lastUpdatedDateTimeUtc` ≠ `external_updated_at` · 새 구매(`sync_purchases.py:119-120`) · 카드 `updatedDateTimeUtc`(`sync_tickets.changed_cards`) ✓. 방문 없는 구매는 changed 에 넣지 않음 ✓. (티켓 쪽 FAIL-1.)
- 번들 순서: `_retire_other_bundles` 가 upsert 전(`sync_tickets.py:95-99`) ✓. 매핑 표(`mapper_sale_values.py`) = ㉔ 매핑 표(`CANCELED` 포함) ✓. entity_type 20 ✓.

### 3. 소프트 딜리트 — PASS

- 물리 DELETE: 새 · 바뀐 동기화 코드 grep 0 · AST 테스트(`test_새_동기화_코드에_물리_삭제가_없다`) 통과.
- 되살림: upsert 행 `deleted_at=None`(메뉴 · 구매 항목 · 시술권 · 링크) · 지운 구매만 `deleted_at=… if p.deleted`(`sync_purchases.py:139`) · 카드 행은 `deleted_at` 을 건드리지 않음(SPEC 「카드 행 지우지 않음」).
- `mark_absent(within=…)`: 구매 하위 = 그 구매들(`sync_purchases.py:248`) · 처방 = 그 방문들(`sync_schedule_sales.py`) · 메뉴 = 병원 전체(응답이 비거나 전부 매핑 실패면 표시 안 함) · 공유 고객 = 카드마다 ✓.

### 4. F-1~F-5 · OQ-71 — PASS

| # | 코드 | SPEC |
|---|---|---|
| F-1 | `mapper_purchase.ledger_external_id`(`:327-331` · `chargingId:pocket`) · 거래 연결 `charging_external_id` | SPEC-000 :1714 · ㉔ :920 · :942 ✓ |
| F-2 | 모델 `menu.py:153` `str | None` · 0010 :586 `nullable=True` · 추정 채움 없음 | SPEC-000 :1384 ✓ |
| F-3 | `enums/ticket.py:13` · 0010 :97 · 매핑 `:57` | SPEC-000 :1632 · :1664 · ㉔ :935 ✓ |
| F-4 | `mapper_purchase.purchase`(`items` + `pendingItems`, 같은 id 면 `items`) · infra 테스트 「확정 = 같은 행 · id 바뀌면 사라짐」 | SPEC-000 :1515 · :1556-1557 · ㉔ :884 ✓ |
| F-5 | `sale_reads` 선불카드 상품 두 번(`{"closed": closed}`) · `is_closed` 응답 값 | ㉔ :882 ✓ |
| OQ-71 | 담당 조회 = `external_ref`(직원 행 소프트 딜리트돼도 ref 는 `deleted_at` 이 안 채워져 찾음 — `sync_references.mark_absent` 는 ref 에 `is_present_in_source=false` 만) · 없는 거래만 건너뜀 · `purchase_transaction.staff_missing` + 구매 단위 카운트 · `staff_id` NOT NULL 유지 · 로그는 DAY id · 건수만(`sync_purchases.py:271`) | `_RESUME` §2 :47 ✓ |

### 5. 0010 변경 — PASS

- FK 인덱스 7개(`0010:158-164`) 전부 새 테이블(`purchase_item` · `purchase_price_adjustment` · `purchase_transaction` · `purchase_assignee` · `prepaid_card_customer` · `prescription` · `product_option_composition`). 기존 테이블에는 여전히 `visit_task` 3칸 + FK 2 뿐. 부분 유일은 `ticket_bundle` 1개 그대로.
- 실제 PG 왕복 · head 하나 · `alembic check` 0(아래 8).

### 6. 보안 · 개인정보 — PASS

- 고정본 17개: 이름은 「직원」 · 「가짜 지점」 · 「항목 가」 꼴 · id 는 `pur-1` · `chg-3` · `acc-1` 꼴 · 전화 · 토큰(`eyJ…` · `Bearer`) 패턴 0.
- 로그: 새 코드의 로그 2곳은 DAY id · 건수 · 오류 이름만(`_isolated` 는 `type(exc).__name__`).
- 테스트 계정 경로(`kos-test-account`) · DEMO 테넌트 선택 코드(`get-user-tenants`)가 `backend/` · `scripts/` 에 없다 — 실물 확인은 저장소 밖 로컬 전용. `scripts/` · `deploy/` 변경 0.

### 7. 부하 — FAIL-1 · WARN-4

- 10초: 구매 묶음 1회(오늘 일정 있을 때) + 대기 고객 ≤ 20 × 2 + 바뀐 카드 × 2 — ㉔ 「2 + 바뀐 고객 × 2 (+ 카드 × 2)」 모양. 두 번째 회차는 같은 응답이면 `["purchases"]` 만(테스트).
- Redis 키 `day:emr:sale_customers:{병원}` · `day:emr:sale_changes_at:{병원}` 만료 7일 ✓ · 고객은 commit 뒤에만 뺌 ✓.
- 5분: 통계 3 × ≤ 20장. 메뉴: 1시간 약 12호출(선불카드 상품 두 번 포함).

### 8. 테스트 — PASS (WARN-5)

| 명령(직접 1회) | 결과 |
|---|---|
| `cd backend && uv run pytest -q tests/day -k "sale or menu or prepaid or ticket or purchase"` | **48 passed · 16 skipped**(infra 표시 — 아래에서 실제 PG 로) |
| `./scripts/test.sh -q` 새 테스트 4 파일 + `tests/migrations` + `test_enum_labels` + `test_constraints`(자체 격리 compose · 무작위 포트 · 사용자 포트 안 씀) | **108 passed** |
| `./scripts/test.sh -q`(전체 · 격리 인프라) | **1815 passed** — 판 테스트 전부 포함 |

- 새 테스트가 지키는 것: 매핑 값마다 · 표 밖 값 건너뜀 · upsert(새 · 바뀜 · 같으면 0) · 사라짐 · 되살림 · 응답 빈 경우 · OQ-69 · OQ-71(+ 퇴사) · 번들 순서 · 바뀐 고객만(풀리는 티켓) · 끊긴 회차 잇기 · 5분 시각 · 회차 격리(예외 → 반환 그대로) · 쓰기 행 = 모델 칸 · DELETE 0.

### 9. 직원이 실물에서 만날 자리 — 없음

- 화면 · 라우터 · 템플릿 · 앱 변경 0. 판 반영 칸 · 신호 그대로(워커 DEMO 판 칸 해시 같음). `apply_task_refs` 의 `visit_task` 갱신은 `updated_at` 을 올리지만 판 표시에 쓰이는 곳은 「방 배정 이름」 고르기(`services/board_rooms.py:72`)뿐이라 영향 없음.
- 간접: FAIL-1 이 고쳐지지 않으면 KOS 호출이 늘어 KOS 쪽 지연 · 제한이 생길 때 **판 동기화도 같은 KOS 에 기대므로** 느려질 수 있다.

---

## FAIL 고칠 곳

1. **FAIL-1** — `day/emr/sync_schedule_sales.py:155`(`ticket_changed_customers`) + `day/emr/sync_tickets.py:85-88` 길: 못 푸는 티켓(출처 구매 항목 없는 번들)이 고객을 10초마다 다시 큐에 넣지 않게 + 테스트. SPEC-002 ㉔ 「바뀐 것만」 표의 「DAY 에 없는 티켓 포함」 문구도 함께(planner).

## 사용자 판단

1. FAIL-1 고치는 방식(못 푼 티켓 id 기억 vs 「지난 회차에 본 ticketId 와 다름」만 · SPEC 문구).
2. WARN-1 오늘 구매 회차를 일정 태스크 안 await → 별도 태스크 발행으로 뗄지.
3. WARN-2 `fetch_schedules` 안 `except MappingError` → `except Exception` 으로 넓힐지.
4. WARN-3 카드 이벤트 통계의 카드 id 로 ④ 를 직접 부를지(㉔ ⑥ 문구대로).
5. WARN-4 5분 회차 상한에 걸릴 때 시각을 부분 전진할지.
