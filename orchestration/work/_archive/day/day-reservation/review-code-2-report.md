# 코드 검수 2: 원내 현황 탭 (be-feat-1 · fix-1 · fe-feat-1)

- 대상: 워크트리 `CENTURION_DAY/day-reservation`의 미커밋 변경. HEAD `431c081b` 위 32개 파일이다.
- 기준:
  - SPEC-006 개정 ⑧(§3 「원내 현황 금액」 · U-8)
  - 결정 R46 ~ R55
  - `contract-v2-inhouse.md`
  - 시안 `20261113_예약현황_시연 (1).html`
- 이번 검수에서 파일은 고치지 않았고 커밋하지 않았다. stash도 쓰지 않았다.

## 판정: **FAIL (작은 1건)**

FAIL 1건은 SPEC에 적힌 것을 일부러 뺀 것이고, 고치는 데 CSS 한 줄이면 된다. 금액 규칙, R52, migration, 계층 규칙, 탭과 칩 유지는 모두 PASS다. WARN은 4건이다.

## 돌린 시험 (모두 직접 돌림 · 전체 check.sh는 돌리지 않음)

| 묶음 | 명령 | 결과 |
|---|---|---|
| 순수 | `scripts/test.sh --pure` + amounts · inhouse_rules · reservations_screen · reservation_page · test_screen_copy · kos_sale/keys_mapper · `tests/architecture` | **113 passed** |
| 인프라(격리 컨테이너, 임의 포트) | `scripts/test.sh` + inhouse_queries · reservation_queries · migration 0018 · test_alembic · 0017 migration · reservation_page · reservations_screen · amounts · inhouse_rules | **80 passed** (26.6 s) |
| 프론트 | `build.mjs --check` (CSS 재현) · `npm run lint` (ESLint + Stylelint) · `format:check` · `node --test tests/res-*.test.mjs` | 재현 일치 · lint 0 · Prettier 통과 · **22/22 pass** |

## ① 금액 함수: R49 ~ R55와 한 줄씩 비교 → **PASS**

대상은 `backend/day/policies/reservation_amounts.py`다.

| 규칙 | 코드 | 판정 |
|---|---|---|
| 수납 = 거래 합(부호 그대로)에서 선불카드 차감을 뺀 값 (R49) | `:87-92`: 상태가 `MONEY_STATUSES`인 거래만 `settled`에 더하고, `payment_type != PREPAID_CARD`인 거래만 `received`에 더한다. 금액은 부호 그대로다 | PASS |
| 세는 거래 = 승인 · 취소 · SPENT. REQUESTED · FAILED는 세지 않음 (R53 · R54) | `:26-32` `MONEY_STATUSES = {APPROVED, CANCELED, SPENT}`. 수납과 ⓐ 둘 다 이 집합 하나를 쓴다(`:88`) | PASS |
| ⓐ = 수납 건마다 (Σ coalesce(adjusted, price) − 그 건 거래 합(선불카드 포함)) 중 0 초과분 | `item_amount` `:37-39`. `:79-82`에서 `charged`, `:93`에서 `max(0, charged − settled)`. 건 하나가 더 냈어도 다른 건의 미수를 지우지 않는다 | PASS |
| 「살아 있는 수납 건」 | `queries/reservation_inhouse.py:119-131`: `purchase.visit_id ∈ 오늘 방문` ∧ `deleted_at IS NULL`. 항목과 거래도 각각 `deleted_at IS NULL`(`:145`, `:161`) | PASS |
| ⓑ 덮임 = 이번 방문의 살아 있는 수납 건에 같은 옵션이 있으면 뺌. 수납 건 상태는 따지지 않음 (R54) | `:78-84`: `covered` 집합에 살아 있는 건의 모든 항목 옵션을 넣는다. `purchase.status`는 읽기만 하고 판정에 쓰지 않는다 | PASS |
| ⓑ = 옵션 단위로 (옵션가 + VAT) × 횟수 | `_due_tasks_unpaid` `:49-66` | PASS |
| 횟수 = 그 옵션 안에서 같은 진료항목 줄 수의 최댓값 | `:62` `max(Counter(treatment_item_id).values())` | PASS |
| VAT = 옵션 VAT 칸이 우선. 없으면 진료항목 중 하나라도 과세면 10%, 원 단위 버림 (R50 · R55) | `option_vat` `:42-46`: `vat` 값이 있으면 그것, 아니면 `price * 10 // 100`(양수 정수라 버림). 과세 판정은 옵션 줄 전체에서 `any`(`:63`) | PASS |
| 결제총액 = 수납 + 미수 (R51) | `:95` | PASS |
| 「수납 완료」 = 시술 대기 이후 ∧ 결제총액 > 0 ∧ 미수 0 ∧ 수납 필요 아님 (R48 · R55) | `policies/reservation_inhouse.py:148-151` | PASS |
| 매핑 넓힘 (R53) | `mapper_sale_values.py`: 상태 5종(APPROVED · CANCELED · SPENT · REQUESTED · FAILED), 수단 7종. enum에 `SPENT` · `REQUESTED` · `FAILED`를 더했다 | PASS |

**참고 (FAIL 아님).**
- 옵션은 있지만 옵션 가격이 null인 줄(`:60-61`)은 ⓑ에서 0으로 센다.
- 옵션이 없는 줄(`:54`)도 0으로 센다.
- 「지어내지 않는다」 원칙에 맞는다. 다만 그런 줄이 있으면 미수가 실제보다 적게 보인다.

## ② R52 세 사례 시험이 값을 실제로 단언하는가 → **PASS**

두 층에서 세 사례 모두 `(total, received, unpaid)`를 정확한 값으로 단언한다.
- **순수:** `test_reservation_amounts.py:85-118`. `assert got == expected`(`:213`)에 R51 항등식(`:214`)까지 본다.
- **DB 행:** `test_reservation_inhouse_queries.py:229-268`. `board_view`의 `inhouse.items[*].amounts` dict 전체를 비교한다.

| 사례 | fixture 구성 (review-doc-7이 실측 당시 스냅샷이라고 한 것) | 단언 |
|---|---|---|
| A 신도윤 | accepted 건: 440,000 + 11,000, cash 451,000. initialized 건: 33,000 × 2, 거래 없음. 수납 필요 2줄은 initialized 건의 옵션과 같음 | 517,000 / 451,000 / 66,000. 덮임이 깨지면 ⓑ가 33,000 × 2를 더 세므로 이 사례가 덮임 규칙을 잡는다 |
| B 홍길사 | 수납 건 없음. 코스 옵션(100,000 + VAT 10,000) 구성 2줄, 서로 다른 진료항목 | 110,000 / 0 / 110,000. 횟수 규칙이 깨지면 220,000이 되므로 이 사례가 그 규칙을 잡는다 |
| C 선불카드 정리 | DB 시험에서는 어제 방문에 충전 1,000,000을 따로 넣는다. 오늘 건 100,000은 PREPAID_CARD 거래로 정리 | 0 / 0 / 0. `payment_done is False`. 어제 방문이 결과에 없는지도 본다 |

R54 · R55 시험도 단언이 실제로 있다.
- `R54-수납완료-건-옵션-덮임-미수0`(amounts)
- `test_R54_…`(DB): `(payment_due, payment_done) == (True, False)`
- `test_R55_…`(rules)

## ③ migration 0018 → **PASS**

- **enum 값 추가:** `ALTER TYPE purchase_transaction_status ADD VALUE IF NOT EXISTS`로 `spent` · `requested` · `failed`를 더한다(`:28-30`).
  - 0013 · 0014와 같은 방식이다.
  - 시험이 upgrade 본문에 DDL과 DML이 없는지 확인한다(`test_transaction_status_migration.py:29-33`).
- **down 가능:**
  - 순서는 이렇다. 새 값 행을 가리키는 FK 두 곳을 NULL로 바꾼다(`purchase_transaction.canceled_transaction_id`, `prepaid_card_ledger.purchase_transaction_id`). 그 행을 지우고, 타입을 rename한 뒤 새로 만들고, `USING status::text::…`로 옮기고, 옛 타입을 drop한다.
  - FK는 모델에서 확인한 두 곳(`models/purchase.py:187`, `models/prepaid_card.py:79`)뿐이다. `status` 칸에는 server_default도, 인덱스도, CHECK도 없어서 타입을 바꿔도 막히지 않는다.
  - up → down(0017) → up 시험이 실제 PG에서 통과했다(`:36-43`).
- **heads 하나:**
  - `down_revision = "0017_reservation_permission"`을 가진 파일은 0018 하나뿐이다.
  - `test_alembic.HEAD`를 0018로 올렸고 통과했다.
  - 0017 시험은 `upgrade head` 대신 `upgrade 0017`로 바꿔, head가 바뀐 뒤에도 깨지지 않게 했다.
- **참고:** downgrade하면 새 세 상태의 거래 행이 지워진다(docstring에 적혀 있다). 다음 구매 동기화 회차에서 다시 받으면 되지만, 그 사이 이력은 빈다. `rollback` workflow가 downgrade를 부른다면 알고 있어야 한다.

## ④ 계층 규칙 · 인라인 스크립트 · 손 CSS · 화면 문구 → **PASS (+ FAIL 1)**

- **계층:**
  - `queries/reservation_inhouse.py`: 모델을 묶어 조회하고 DTO만 돌려준다.
  - `policies/reservation_inhouse.py`, `policies/reservation_amounts.py`: dtos · enums · identifiers · policies만 import한다. I/O · 설정 · 화면은 모른다. `zone`은 인자로 받는다.
  - `presentation/reservation_inhouse.py`: DTO를 dict로 바꾼다.
  - `services/reservations.py:74-80`: 위 셋을 조립한다.
  - router에는 docstring만 바뀌었다. `tests/architecture`가 통과했다.
- **인라인 스크립트 · style 속성:** 템플릿 diff에 `<script>`와 `style=` 둘 다 없다. 꺾쇠 흐림은 day.js가 `style.setProperty`(CSSOM)로 바꾼다.
- **CSS:**
  - 원천 `styles/app.css`에만 썼다. 빌드된 `day.css`는 `build.mjs --check`에서 재현이 일치하고, Stylelint도 0이다.
  - 새 값 9개는 `:root`의 `--day-res-*` 토큰으로 두었고, 시안 줄 번호 근거가 있다.
  - `.day-res-chip.is-on`의 `#000`(`app.css`의 칩 블록)만 토큰 밖 리터럴이다. 시안 L406 값 그대로라서 WARN으로 올리지 않았다.
- **화면 문구:**
  - `test_screen_copy.py`에 VISIBLE 8개와 HIDDEN 3개가 늘었다.
  - 근거 줄을 시안과 대조했다. 「원내 현황」은 L1806, STAGE_CATS는 L1774, 「상담 ○○ 실장」 · 「총 합계」 · 「수납 완료」는 L1781 ~ 1785, n0w 「원」은 L1787, 「해당하는 고객이 없어요」는 L1824다. 「앞/뒤 칩 보기」는 L1790, 「보기」는 L1481(`role=group aria-label="보기"`)이다.
  - 이번 판에 시안 밖 글자는 없다.
  - 1차 검수 F-1(「예약 표」 aria-label)은 템플릿에서 지워졌다. grep 결과 0건이다.

### F2-1 (FAIL · 작음) 원내 현황 카드에 hover 테두리가 없다

- **SPEC U-8:** 「시안 카드의 `button` · 고른 카드 파란 테두리(`is-on`)는 쓰지 않는다 · **마우스를 올린 테두리(`--gray-500`)만**」. 시안은 L475 `.ibc:hover { border-color: var(--gray-500); }`.
- **구현:** `app.css`의 `.day-res-in-card`(약 L3368) 블록에 `:hover` 규칙이 없다. grep 결과 0건이다.
- **원인:** fe-feat-1 리포트 L44에 「누르기 동작이 없어(R47) 뺐다 — 필요하면 CSS 한 줄」이라고 적혀 있다. SPEC이 남기라고 한 것을 구현이 판단해서 뺐다.
- **고치는 방법:** `.day-res-in-card:hover { border-color: var(--ms-gray-500); }` 한 줄과, 시안 transition(150ms)이다.

## ⑤ 폴링 · 날짜 이동 뒤 탭 · 칩 유지 → **PASS (+ WARN 2)**

- **유지되는 원리:**
  - `resSide` · `resInCat`는 모듈 변수라 조각을 바꿔 끼워도 남는다(`day.js:1678-1679`).
  - 조각이 들어오면 `htmx:afterSwap` → `init` → `resInit`이 `resApplySide` · `resApplyInhouse`를 부른다(`:2003-2006`). afterSwap은 DOM을 넣은 같은 task에서 동기로 돌기 때문에, 기본 탭이 한 프레임 보였다가 바뀌는 깜빡임은 생기지 않는다.
  - 고른 칩이 새 조각에 없으면 「전체」로 되돌린다(`:1874-1875`).
  - 정렬과 거르기는 서버가 준 `order_all` · `order_cat` · `cat`만 쓴다.
- **시험:** `res-inhouse.test.mjs`의 「고른 탭 · 칩은 10초 폴링 · 날짜 이동 뒤에도 남는다(시계 하나)」 등 5건이 통과했다. 서버 쪽은 `test_원내_현황은_보는_날짜와_무관_폴링에도_같이`, `test_상담_실장_원천과_오늘만`(보는 날짜를 3개로 바꿔도 같은 결과)이 통과했다.

### W2-1 원내 현황 목록의 세로 스크롤이 10초마다 맨 위로 돌아간다

- **현상:** 폴링이 `#reservation-main` 전체를 바꿔 끼운다. `resBeforeSwap`(`day.js:~2164`)은 표의 `[data-day-res-scroll]` 위치만 저장한다. 그래서 새로 끼운 `.day-res-in` 목록(`overflow-y: auto`)은 `scrollTop`이 0에서 시작한다.
- **실제 사용에서:** 오늘 원내 고객이 패널 높이를 넘으면(대략 10명 이상, 금액 카드는 키가 크다) 직원이 아래 고객을 보려고 내리는 중에 10초마다 맨 위로 튄다.
- **시안과 비교:** 시안은 `side-body` 요소를 그대로 두고 `innerHTML`만 바꾸므로 스크롤이 남는다.
- **시험:** 이 경우를 보는 시험은 없다.

### W2-2 칩 줄의 가로 스크롤 위치가 폴링 뒤에 0으로 돌아간다

- **현상:** 시안 `syncCats`는 `catsX`를 기억해서 다시 그려도 「밀어 둔 자리 그대로」 둔다(L1793). 구현 `resSyncCats(row, false)`는 위치를 되살리지 않는다(`:2006`).
- **실제 사용에서:** 칩 다섯 개가 250px에 다 들어가면 드러나지 않는다. 글꼴이나 확대 배율 때문에 넘치면, 고른 칩(예: 「귀가 대기」)이 폴링 뒤 잘려 보일 수 있다.

## ⑥ 쿼리 수 증가(+6/폴링) 위험 → **PASS (+ WARN 2)**

- **고정 수:**
  - `inhouse_rows`는 방문이 있으면 쿼리 6번, 없으면 1번이다. 방문 1건과 15건에서 같다는 시험이 있다(`test_reservation_inhouse_queries.py:316-340`).
  - 항목과 거래는 `purchase_id IN (subquery)` 방식이라 N+1이 아니다.
  - `board_view`의 쿼리 수 시험은 7로 갱신됐다(표 6 + 방문 0건일 때의 원내 1).

### W2-3 새로 읽는 경로에 인덱스가 없다: `purchase.visit_id`, `visit_task.visit_id`

- **현상:**
  - `purchase.visit_id`는 FK만 있고 인덱스가 없다(`models/purchase.py:64` · migration 0010).
  - `visit_task.visit_id`도 마찬가지다(`models/task.py:92`).
  - PG는 FK에 인덱스를 자동으로 만들지 않는다.
- **영향:** 폴링 한 번마다 `purchase`를 2번(`:119-131`, 하위 조회 2개 포함) 훑고, `visit_task`를 1번(`:166-194`, 그리고 방문 쿼리의 EXISTS) 훑는다. 테이블이 커지면 순차 스캔이 된다.
  - `purchase`는 백필과 과거 이력이 쌓이는 테이블이다.
  - 데스크 PC 수 × 6회/분이므로, 데모에서는 보이지 않는 지연이 운영 데이터에서 쌓인다.
- **참고:** `visit_task` EXISTS는 기존 표와 시술 현황판도 같은 경로라 이번 판이 처음 만든 문제는 아니다. 그러나 `purchase.visit_id`는 이번 판이 처음 여는 경로다.
- **시험:** 쿼리 수 시험은 쿼리 「수」만 세고 실행 계획은 보지 않는다.

### W2-4 오늘을 볼 때 같은 방문을 두 번 읽고, 최악 쿼리 수는 시험이 없다

- **현상:**
  - 보는 날짜가 오늘이면 `day_rows`(표)와 `inhouse_rows`(원내)가 같은 창의 `visit`를 각각 읽는다(`services/reservations.py:72-76`).
  - 오늘 방문이 있는 날의 폴링은 표 6 + 원내 6 = **12회**다.
- **시험:** `board_view` 수준 시험은 원내 방문이 0건인 경우(7)만 본다. 「오늘 + 방문 있음 = 12」는 따로 단언하지 않는다. 깨질 위험은 작다.

## 그 밖 (참고 · FAIL 아님)

- **국적 빈 문자열:** 계약 v2의 `nationality: str|null`과 달리, 접수 단계에서 국적이 없으면 `""`를 준다(`policies/reservation_inhouse.py:153`). 템플릿이 `select`로 걸러서 화면은 SPEC대로 「{예약 일시}」만 보인다. 계약을 글자 그대로 읽으면 null이어야 한다.
- **aside 이름:** `<aside aria-label="공지 / 예약">`은 탭이 두 개가 된 지금도 그대로다. 이전 판부터 있던 글자이고 시안 근거 행이 있다.
- **고객 삭제:** 원내 조회는 `customer.deleted_at`을 거르지 않는다. 표 조회도 같은 방식이다.
- **단계 판정:** 대상은 `card_state`로 판정한다. 그래서 취소 · 노쇼 상태가 단계보다 먼저 빠진다. 시험은 `test_대상은_…`이다.

## 직원이 실제 사용에서 만날 자리

1. **원내 고객이 많은 날:** 목록을 내리는 중에 10초마다 맨 위로 튄다(W2-1). 가장 먼저 체감될 것이다.
2. **결제 직후 한 회차(R55 · 의도된 동작):** KOS가 `payment_required`를 늦게 끄는 동안 「수납 필요」 배지가 남는다. 그때 금액 줄의 「수납 필요」는 0원이다(R54). 배지와 금액이 한 폴링 동안 어긋나 보인다.
3. **구매 회차가 일정 회차보다 늦을 때:** 단계는 시술 대기인데 금액이 0 / 0 / 0으로 보일 수 있다(SPEC §3 사실 문장 그대로).
4. **옵션 가격이 비어 있는 수납 필요 시술:** 미수에 잡히지 않는다(지어내지 않음). 「수납 필요」 배지는 켜져 있는데 금액은 0원일 수 있다.
5. **카드에 마우스를 올려도 반응이 없다(F2-1):** 시안과 SPEC의 hover 테두리가 빠져 있다.
6. **운영 데이터가 쌓인 뒤:** 폴링 응답이 느려질 위험이 있다(W2-3, `purchase.visit_id` 순차 스캔).
