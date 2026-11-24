# day-reservation backend 기능 1 — 원내 현황 탭 데이터 · 금액 · 거래 매핑 (R46 ~ R54)

## 상태: done

- 커밋 · push 없음. 스택 · deploy/*.env는 건드리지 않았다.
- 템플릿 · day.js · CSS는 건드리지 않았다(frontend 몫).
- 데모 DB는 읽기 전용 SELECT만 썼고, 이름은 출력하지 않았다(WHERE 조건으로만 사용).
- 작업 중 보충 1(R54)을 반영했다.

## 1. 보기 모델 `inhouse` (계약 v2 그대로)

**위치**: `services/reservations.board_view`가 기존 V1 ~ V4에 최상위 `inhouse`를 더한다. 라우트는 그대로 `**values`로 넘긴다.
- 일반 · 조각 · `poll=1` 응답 모두 같은 `board_view`를 지나므로 셋 다 실린다.
- **보는 날짜와 무관하게 늘 오늘**이다(R47). 오늘 창은 `rules.day_window(today(now))`로 잡는다.

**계층** (새 파일):

| 계층 | 파일 | 내용 |
|---|---|---|
| dtos | `dtos/reservation_inhouse.py` | 행 DTO(방문 · 수납 건 · 항목 · 거래 · 수납 필요 줄), 출력 DTO(칩 · 카드 · 금액) |
| queries | `queries/reservation_inhouse.py` `inhouse_rows` | 아래 쿼리 표 참고 |
| policies | `policies/reservation_inhouse.py` `inhouse` | 대상 · cat · 단계 · 칩 · 순번 · 배지 · 접수 줄 · 상담 실장 |
| policies | `policies/reservation_amounts.py` `visit_amounts` | 금액(순수 함수) |
| presentation | `presentation/reservation_inhouse.py` `inhouse_view` | 계약 v2 dict |

`inhouse_rows`의 쿼리(방문이 있으면 6개 · 없으면 1개, 방문 수와 무관):
1. 방문 + 고객 + R42 EXISTS + 일정 상담 정보 상담사 이름
2. 상담 기록 첫 상담사
3. 수납 건
4. 항목
5. 거래
6. 수납 필요 줄 + 옵션 가격 · VAT + 진료항목 과세

지운 행은 모두 뺀다(방문 · 수납 건 · 항목 · 거래 · 작업 · 상담 · 직원).

**판정**:
- **대상**: 오늘 방문 중 `card_state`(표와 같은 키)가 다음 여섯 단계인 것.
  - `reception` · `consultation_waiting` · `consultation` · `procedure_waiting` · `procedure` · `procedure_done`
  - 예약 · 귀가 · 취소 · 노쇼는 빠진다.
  - 그룹이 없는 방문도 들어간다(표의 열과 무관).
- **cat**: 다음 넷이다.
  - `reception`
  - `consult`(대기 + 진행)
  - `procedure`(대기 + 진행)
  - `going_wait`
- **stage**: `{key, label}`. label은 시안 문구(접수 · 상담 대기 · 상담 진행 · 시술 대기 · 시술 진행 · 귀가 대기)다.
- **칩**: 시안 순서대로 전체 · 접수 · 상담 · 시술 · 귀가 대기, count를 붙인다.
- **순번**:
  - `order_all` = (수납 필요 먼저 → 단계 순 → 예약 시각 → 만든 시각 → id)
  - `order_cat` = (단계 → 시각 → 만든 시각 → id)
  - 카드는 `order_all` 순으로 싣는다.
  - 「수납 필요 먼저」의 「수납 필요」는 `payment_due`(R42 배지와 같은 값)다.
- **`payment_due`**: R42 그대로(표와 같은 EXISTS).
- **`payment_done`**: 금액 단계 ∧ 결제총액 > 0 ∧ 미수 0(R48).
- **접수만**:
  - `reserved_label` = 시안 `whenOf`(「2026.11.23 (월) 10:30」, 병원 현지)
  - `nationality` = 표와 같은 값(`nationality or ""`)
  - 그 밖 단계는 둘 다 null.
- **`counselor_name`**: 접수 아님일 때만. `consultation.counselor_id`(상담 시작 순 · 같으면 생성 · id, `queries.board.counselor_rows`와 같은 순서) → 없으면 `visit.consultation_info_counselor_id`. 지운 직원 · 지운 상담은 뺀다.
- **`amounts`**: 시술 대기 · 시술 진행 · 귀가 대기만. 그 밖은 null.
- **`name`**: 표와 같다(`name_pronunciation or name`).

## 2. 금액 R49 ~ R51 · R54 (`policies/reservation_amounts.py`)

- **수납(received)** = 살아 있는 수납 건의 거래 합. 부호 그대로 더하고(취소 · spent 음수 포함) **선불카드 제외**.
- **ⓐ** = 수납 건마다 max(0, Σ coalesce(adjusted, price) − 그 건 거래 합(선불카드 포함)).
- **세는 거래**: 수납 · ⓐ 둘 다 승인 · 취소 · spent만 센다. requested · failed는 안 센다(R53 · R54).
- **ⓑ**:
  - 대상: 수납 필요 줄(살아 있음) 중 **이번 방문의 살아 있는 수납 건(상태 무관 · R54)에 같은 상품 옵션이 없는 것**.
  - 계산: 옵션 단위로 (옵션 가격 + VAT) × 횟수.
  - 횟수 = 그 옵션 안에서 진료항목별 줄 수의 최댓값(구성 여러 줄 = 1회, 같은 진료항목 2줄 = 2회).
- **VAT** = `product_option.vat_amount`가 있으면 그것. 없으면 그 옵션 줄들의 진료항목 과세가 `taxable`일 때 가격 × 10 // 100(원 단위 버림). 아니면 0.
- **미수** = ⓐ + ⓑ. **결제총액** = 수납 + 미수(R51).

## 3. 상담 실장 R48
§1의 `counselor_name` 그대로다. 원천은 시술 현황판과 같은 `consultation.counselor_id`, 상담 시작 순이다.

## 4. 거래 매핑 R53 + migration 0018

**매핑 넓힘** (`emr/kos/mapper_sale_values.py`):
- `TRANSACTION_STATUSES`에 `SPENT` · `REQUESTED` · `FAILED`를 더했다.
- `PAYMENT_TYPES`에 `PLATFORM` · `EASY_PAY` · `MEDICAL_LOAN`을 더했다. 문자열은 openapi `TransactionStatus` · `TransactionPaymentType` 그대로다.

**enum**: `enums/purchase.PurchaseTransactionStatus`에 `spent` · `requested` · `failed`를 더했다. `payment_type` DB enum에는 일곱 값이 이미 있어 바꾸지 않았다.

**migration** `migrations/versions/20261123_0018_transaction_status_more.py`:
- revision = `0018_transaction_status_more`, down = `0017_reservation_permission`.
- upgrade: `ALTER TYPE … ADD VALUE IF NOT EXISTS` × 3.
- downgrade: 순서는 다음과 같다.
  1. 새 값 행을 가리키는 참조(취소 자기 참조 · `prepaid_card_ledger.purchase_transaction_id`)를 끊는다.
  2. 그 행을 지운다.
  3. 타입을 다시 만든다(0014와 같은 방식).
- `alembic heads`는 `0018_transaction_status_more (head)` 하나다.

**그에 따른 시험 수정**:
- `tests/migrations/test_alembic.py`: `HEAD` = 0018.
- `test_reservation_permission_migration.py`: 「upgrade head」를 「upgrade 0017」로 바꿨다(head가 뒤로 밀림).
- `tests/day/emr/test_kos_sale_mapper.py`: 매핑 표 · 「표본 없는 값」 시험을 R53에 맞췄다.
- `tests/day/emr/test_kos_keys_mapper.py`: 「모르는 결제 수단」 시험에서 `EASY_PAY`를 빼고 `TransactionPaymentType_UNSPECIFIED`로 바꿨다(`APP_PAY`는 그대로).

## 5. 시험

**새 시험**:
- `tests/day/test_reservation_amounts.py`(값 · 22개) — 금액 규칙 표 12행:
  - R52 세 사례: 신도윤 517,000 / 451,000 / 66,000 · 홍길사 110,000 / 0 / 110,000 · 선불카드 정리 0 / 0 / 0. 실측 당시 스냅샷을 fixture로 만들었다.
  - 같은 진료항목 2줄 = 2회 · 과세 10%
  - 결제 전 수납 건과 수납 필요 시술 겹침
  - **R54 수납 완료 건 옵션 덮임 → 미수 0**
  - 취소 음수
  - 부분 환불 adjusted + spent
  - REQUESTED · FAILED 미포함
  - 선불카드 섞인 결제
  - 수납 건별 0 초과분
  - 가격 원천 없는 줄 = 0
  - 그 밖에 VAT 표 6개, R53 매퍼 4개.
- `tests/day/test_reservation_inhouse_rules.py`(값 · 8개):
  - 대상 · cat · 단계 문구 · 칩 수
  - 정렬(전체 / 칩)
  - 접수 줄(예약 일시 · 국적)
  - 상담 실장 원천 순서
  - 금액 칸 단계 · 수납 완료 배지
  - 빈 목록
  - dict 이름 = 계약 v2
  - 현지 시각 형식
- `tests/day/test_reservation_inhouse_queries.py`(실 PostgreSQL · 5개):
  - R52 세 사례를 DB 행으로 재현(어제 충전 방문 제외 포함)
  - 지운 행 · 새 거래 상태 저장 · 집계(spent · requested · failed · easy_pay · medical_loan)
  - 상담 실장(시작 순 · 지운 상담 뺌 · 일정 상담 정보 대체) + 오늘만(보는 날짜 셋 모두 같은 오늘 · 내일 방문 제외)
  - 쿼리 수 6 = 6(방문 1 vs 15), 빈 병원 1
  - R54 DB판
- `tests/migrations/test_transaction_status_migration.py`: 0018 본문 검사 + up → down → up 왕복.

**바꾼 시험**:
- `tests/day/web/test_reservation_page.py`: 넘기는 값 이름에 `inhouse`를 더했다. 일반 · 조각 · 폴링 · 다른 날짜 폴링 네 응답 모두 `inhouse`가 실리는지 본다.
- `tests/day/test_reservation_queries.py`: `board_view` 쿼리 수 6 → 7. 원내 현황이 더하는 오늘 방문 쿼리 1개 때문이다(그 시험의 오늘 = 방문 없음).

**결과**:
- `./scripts/test.sh -q` 로 아래 묶음을 돌렸다: 새 시험 셋 · `test_reservation_queries` · `test_reservation_rules` · `test_reservation_refresh` · `web/test_reservation_page` · `web/test_reservations_screen` · `board/test_reservation_permissions` · `tests/day/emr` 전체 · `tests/migrations` 전체 → **485 passed**.
- `./scripts/test.sh --pure -q backend/tests/architecture` → **317 passed**.
- `./scripts/check.sh --static`(ruff · format · mypy · taut audit / check · frontend 정적, 시험 없음) → **All requested checks passed**. frontend 진행 중 파일까지 함께 통과했다.
- 전체 `check.sh`(infra 전체)는 돌리지 않았다.

## 6. 바꾼 파일 (내 것)
- 새 파일:
  - `day/dtos/reservation_inhouse.py`
  - `day/queries/reservation_inhouse.py`
  - `day/policies/reservation_inhouse.py`
  - `day/policies/reservation_amounts.py`
  - `day/presentation/reservation_inhouse.py`
  - `migrations/versions/20261123_0018_transaction_status_more.py`
- 수정:
  - `day/services/reservations.py`(`board_view` + 원내 현황)
  - `day/routers/reservations.py`(docstring만)
  - `day/enums/purchase.py`
  - `day/emr/kos/mapper_sale_values.py`
- 시험: §5에 적은 파일들(`backend/tests/...`).
- `git status`의 templates · static · styles · `test_reservations_screen.py` · `test_screen_copy.py` · `scripts/frontend/*` 변경은 frontend 것이다. 건드리지 않았다.

## 7. 코디가 확인할 것 · 열린 점
1. **배지 동시 표시**: R54 지연 중에는 `payment_due`(R42 · 수납필요 줄 켜짐) = true와 `payment_done`(미수 0) = true가 함께 나온다(시험에 그대로 고정). 화면에서 두 배지를 같이 그릴지는 결정이 필요하다.
2. **VAT 과세 판정**: 옵션 VAT 칸이 없고 옵션 줄들의 진료항목 과세가 섞이면(코스), 「하나라도 `taxable`이면 10%」로 계산한다. 결정 문구가 「진료항목 과세」라서 코스 혼합 경우는 정해지지 않았다. 반올림은 원 단위 버림이다(KOS 규칙은 확인 못 함).
3. **가격 원천 없는 줄**: 옵션이 없거나 옵션 가격이 없는 수납 필요 줄은 0원이다. 지어내지 않았다.
4. **downgrade 0018**: 새 상태 거래 행은 지운다. 앞 판은 받지 않던 행이다. 행이 있는 상태에서 downgrade하는 시험은 없고, enum 왕복만 시험했다.
5. **쿼리 추가**: `board_view`가 쿼리를 더 쓴다. 오늘 방문이 있으면 +6, 없으면 +1이다. 10초 폴링에도 같다.
6. **배포**: 스택 재기동(api · worker)과 migration 0018 적용은 코디 몫이다. 동기화가 새 거래 상태 · 수단 행을 받기 시작하는 것은 worker 재기동 뒤부터다.
