# cc-prototype ext API — 보내는 값 · 받는 값

- 무엇: 지금 cc-prototype 에 있는 외부 연동 API(`/api/ext`) 13개의 요청 · 응답 필드 전부. DAY 로 옮기는 작업(day-ext)의 출발점
- 원천: `orchestration/work/_archive/day/day-cc-mig/research-cc-ext-report.md` §A1 · §A2 · §A3(cc `origin/main` 0553173 · 2026-11-20 조사) 에서 필드 행을 그대로 뽑았다. 새로 조사한 것은 없다
- 「뜻」 = cc Swagger 필드 설명 그대로
- 「DAY 대응 · 판정」 = **11-20 조사 때 DAY `origin/dev` 844eace4 기준**. 그 뒤 테이블 보충(#265 · 0012)으로 `없음` 이던 칸 중 상당수가 생겼다 — 이관 때 다시 본다
  - 판정: `있음`(같은 시점 값이 DAY 칸에) · `가공`(있는 칸에서 계산 · 변환) · `없음` · `없음(시점 다름)`(같은 이름 칸은 있으나 다른 시점 값) · 빈칸 = 묶음 · 계산 칸

## 공통

| 항목 | cc 지금 |
|---|---|
| 인증 헤더 | `X-Api-Key: <연동처 키>` — 13개 전부 |
| 연동처 | linky · charty (env `PROC_EXT_KEY_LINKY` · `PROC_EXT_KEY_CHARTY`) |
| 병원 범위 | 서버 하나 = KOS 병원 하나 · `clinicId = 1` 고정 |
| 열람 헤더 | `X-Ext-Staff-Id`(선택 · 연동처가 알려 주는 직원 id · 검증 안 함) — E2 · E8 · E9 ~ E11 |
| 호출 제한 | 키당 60초 60번 · 키 없는 오류는 IP 당 60초 10번이면 차단 |
| 호출 기록 | `ext_call`(시각 · 연동처 · 경로 틀 · 상태) |
| 에러 | `{"error": {"code", "message"}}` · 검증 오류 400 `invalid_request` · `Cache-Control: no-store` |
| id 체계 | cc 정수 id(`customerId` · `reservationId` · `staffId`). DAY 는 uuid — 정할 것 C10 |

## 목록

| # | 메서드 · 경로 | 무엇 | 읽기/쓰기 | 보내는 값 |
|---|---|---|---|---|
| E1 | `GET /api/ext/menu` | 메뉴 트리(카테고리 → 상품 → 옵션 → 구성) | 읽기 | 없음 |
| E2 | `POST /api/ext/customers/lookup` | 고객 · 남은 시술권 · 선불카드 | 읽기 | 이름+이메일 또는 customerId |
| E3 | `POST /api/ext/reservations` | 예약 만들기(고객 없으면 KOS 고객 생성) | **쓰기** | 이름 · 이메일 · 시작 · 메모 |
| E4 | `GET /api/ext/availability` | 그날 예약 가능한 칸 · 남은 자리 | 읽기 | `date` |
| E5 | `POST /api/ext/customers/visits` | 과거 일정 최신 50 | 읽기 | 이름 · 이메일 |
| E6 | `POST /api/ext/customers/reservations` | 오늘 0시 이후 일정 | 읽기 | 이름 · 이메일 |
| E7 | `GET /api/ext/reservations/board` | 오늘 접수 목록(예약 단위) | 읽기 | 없음 |
| E8 | `GET /api/ext/reservations/{reservationId}` | 예약 상세 | 읽기 | 경로 `reservationId` |
| E9 | `PUT /api/ext/customers/{customerId}/language` | 고객 언어 | **쓰기** | `customerId` · `language` |
| E10 | `PUT /api/ext/reservations/{reservationId}/order-memo` | 오더 메모 통째로 | **쓰기** | `reservationId` · `orderMemo` |
| E11 | `PUT /api/ext/reservations/{reservationId}/consultation-memo` | 상담 메모(= 차트 메모) 통째로 | **쓰기** | `reservationId` · `consultationMemo` |
| E12 | `GET /api/ext/clinic` | 병원 정보 · 운영 시간 · 휴무 | 읽기 | 없음 |
| E13 | `GET /api/ext/clinics/{clinicId}/staff` | 직원 목록 | 읽기 | 경로 `clinicId` |

## 엔드포인트별
### E1. `GET /api/ext/menu`

**보내는 값(요청)**

없음(키 헤더만)

**받는 값(응답)**

| 필드 | 타입 | 뜻 | DAY 대응(11-20 조사) | 판정 |
|---|---|---|---|---|
| `syncedAt` | `str \| None` | 메뉴 동기화가 마지막으로 **전부** 성공한 시각(ISO `+09:00`). 그 뒤 작업 하나가 실패해도 이 값은 그대로다. 한 번도 성공한 적 없으면 null | DAY 메뉴 회차의 「마지막 전부 성공」 칸 확인 안 됨(`external_ref.synced_at` 은 행마다) | 없음 |
| `categories` | `list[ExtCategory]` | 지금 있는 카테고리(`order` 오름차순 → id). 메뉴가 비었으면(첫 동기화 전 · 실패) `[]` | `product_category` |  |
| `categories[].id` | `str` | 카테고리 KOS id(문자열) | `external_ref`(entity=product_category).external_id | 가공 |
| `categories[].name` | `str` | 카테고리 이름(KOS 기본 이름) | `product_category.name`(내부 `procedure-menu/categories/...` · `sale_reads.py:50`) | 있음 |
| `categories[].order` | `int` | KOS 카테고리 순서(오름차순으로 준다) | `product_category.sort_order` | 있음 |
| `categories[].translsMap` | `dict[str, Any]` | KOS 다국어 맵 그대로 · 없으면 `{}` | `product_category.name_translations` = `translsMap.name` 만(`mapper_menu.py:79`) | 가공 |
| `categories[].products` | `list[ExtProduct]` | 이 카테고리에 속한 지금 있는 상품(KOS 상품 목록 순서). 한 상품이 카테고리 여럿에 걸리면 각 카테고리 아래에 다 나온다 | `product` + `product_category_link` |  |
| `products[].id` | `str` | 상품 KOS id(문자열) | `external_ref`(product) | 가공 |
| `products[].title` | `str` | 상품 이름(KOS 기본 이름) | `product.title` | 있음 |
| `products[].description` | `str` | 상품 설명(KOS 값 · 없으면 빈 문자열) | `product.description`(null 가능 — cc 는 빈 문자열) | 있음 |
| `products[].isEvent` | `bool` | 이벤트 상품인가(KOS `isEvent`) | `product.is_event` | 있음 |
| `products[].translsMap` | `dict[str, Any]` | KOS 다국어 맵 그대로 · 없으면 `{}` | `product.translations`(`mapper_menu.py:172`) | 있음 |
| `products[].options` | `list[ExtOption]` | 지금 있는 옵션(KOS 배열 순서 · 지운 옵션 제외) | `product_option` |  |
| `options[].id` | `str` | 옵션 KOS id(문자열) — 시술권 `optionId` 와 같은 체계 | `external_ref`(product_option) | 가공 |
| `options[].type` | `Literal['SINGLE', 'GROUP', 'CONSULTATION']` | KOS 옵션 판별자 그대로 — `SINGLE`(시술 1개 · 옵션에 횟수 · 단위 · 시술) · `GROUP`(구성 여럿) · `CONSULTATION`(상담 · 가격 · 구성 없음) | `product_option.type`(enum `OptionType` — 값 표기(대소문자) 일치 확인 안 됨) | 있음 |
| `options[].title` | `str` | 옵션 이름(KOS 기본 이름) | `product_option.title` | 있음 |
| `options[].description` | `str` | 옵션 설명(KOS 값 · 없으면 빈 문자열) | `product_option.description` | 있음 |
| `options[].translsMap` | `dict[str, Any]` | KOS 다국어 맵 그대로(`{칸: {translation: {언어: 값}}}`) · 없으면 `{}` | `product_option.translations` | 있음 |
| `options[].listPriceExVat` | `ExtMoney \| None` | 옵션 정가 · **부가세 별도**(KOS `price.amount`). CONSULTATION 은 null | `product_option.price_amount` · `currency`(DAY 원천 = 내부 상품 응답 · cc = 공개) | 있음 |
| `options[].count` | `int \| None` | SINGLE 의 시술 횟수(KOS `count`). GROUP(구성마다 있음) · CONSULTATION 은 null | `product_option.count` | 있음 |
| `options[].unit` | `ExtUnit \| None` | SINGLE 의 단위 = 이어진 진료항목의 `configuration.unit`. 진료항목이 이어지지 않았거나 단위가 없으면 null. GROUP · CONSULTATION 은 null | `product_option.treatment_item_id` → `treatment_item.unit_type/unit_value` | 가공 |
| `options[].procedure` | `ExtProcedureRef \| None` | SINGLE 의 시술. GROUP · CONSULTATION 은 null | `product_option.treatment_id` → `treatment` | 가공 |
| `options[].compositions` | `list[ExtComposition]` | GROUP 의 구성(KOS 배열 순서). SINGLE · CONSULTATION 은 `[]` | `product_option_composition` |  |
| `compositions[].title` | `str` | 구성 이름(KOS 값) | `product_option_composition.title`(null 허용) | 있음 |
| `compositions[].count` | `int \| None` | 구성의 시술 횟수(KOS `count`) | `product_option_composition.count` | 있음 |
| `compositions[].unit` | `ExtUnit \| None` | 구성 단위 — KOS 구성 `unit` 그대로(`UnitType_UNKNOWN` 도 그대로). KOS 가 주지 않으면 null | `product_option_composition.unit_type/unit_value` | 있음 |
| `compositions[].listPriceExVat` | `ExtMoney \| None` | 구성 정가 · **부가세 별도**(KOS `price.amount`). 한 GROUP 옵션의 구성 정가를 다 더하면 옵션 정가다 | `product_option_composition.price_amount`(통화 칸 없음 — 옵션 `currency` 로) | 가공 |
| `compositions[].procedure` | `ExtProcedureRef \| None` | 구성의 시술 | `product_option_composition.treatment_id` → `treatment` | 가공 |
| `*.value (ExtMoney)` | `int` | 금액(원 단위 정수) | `*.price_amount`(정수) | 있음 |
| `*.currency (ExtMoney)` | `str` | 통화 코드(ISO 4217 · 예 `KRW`) — KOS 값 그대로 | 옵션 `currency` 칸만(구성 · 시술권 · 카드에는 통화 칸 없음) | 가공 |
| `*.type (ExtUnit)` | `str` | 단위 종류 — KOS 값 그대로(예 `SHOT` · `CC` · `UNIT` · `UnitType_UNKNOWN`) | `unit_type`(DAY 작업 단위는 소문자 · `UnitType_UNKNOWN`→null `mapper.py:463` — 메뉴 단위 표기 확인 안 됨) | 가공 |
| `*.value (ExtUnit)` | `float \| None` | 단위 값 — KOS 값 그대로. KOS 가 주지 않으면 null | `unit_value`(Numeric) | 있음 |
| `*.id (ExtProcedureRef)` | `str` | 시술 KOS id(문자열) | `external_ref`(treatment) | 가공 |
| `*.name (ExtProcedureRef)` | `str` | 시술 이름(KOS 값) | `treatment.name` | 있음 |

### E2. `POST /api/ext/customers/lookup`

**보내는 값(요청)**

| 필드 | 타입 | 뜻 |
|---|---|---|
| `header X-Ext-Staff-Id` | `str\|None` | 선택 — 연동처 직원 id(열람 기록용 · 검증 안 함) |
| `body.name` | `str \| None` | 고객 이름 — `email` 과 함께 보낸다(`customerId` 와 섞지 않는다). 앞뒤 공백만 지워 KOS 이름 검색에 그대로 보낸다 — **KOS 에 등록된 띄어쓰기 그대로** 보내야 한다. 앞뒤 공백을 지우면 비는 값은 400 |
| `body.email` | `str \| None` | 고객 이메일 — `name` 과 함께 보낸다. 앞뒤 공백을 지우고 소문자로 바꿔 KOS 고객 email 과 정확히 같은지만 본다(형식 검사 없음). 앞뒤 공백을 지우면 비는 값은 400 |
| `body.customerId` | `StrictInt \| None` | ccc 고객 id(1 이상 정수 · 문자열 불가) — 이 칸 **하나만** 보낸다(`name` · `email` 과 섞지 않는다). 다른 응답(접수 목록 · 예약 상세 · 조회)의 `customerId` 와 같은 체계 |

**받는 값(응답)**

| 필드 | 타입 | 뜻 | DAY 대응(11-20 조사) | 판정 |
|---|---|---|---|---|
| `customer` | `ExtCustomer` | 찾은 고객(상담에 필요한 칸만 — 전화 · 생년월일 · 국적 · 여권 · 차트번호 · 이메일 없음) | `customer` |  |
| `customer.customerId` | `int` | ccc 고객 id(직원 API 와 같은 체계 · 정수). KOS 고객 id 는 내지 않는다 | `customer.id` — DAY id 는 uuid(`models/*` `uuid_pk()`) — cc 정수 id 와 타입이 다르다(계약 변경) | 가공 |
| `customer.name` | `str` | KOS 고객 이름 | `customer.name`(일정 응답 visitor · 10초 · 오늘 방문 고객만 갱신) | 있음 |
| `customer.isNew` | `bool` | KOS 신규 고객 여부(`isNew`) | 고객 칸 없음 — `visit.is_new` 는 **방문마다** 값(SPEC-000:360 · `mapper.py:597`) | 없음(시점 다름) |
| `customer.lastVisitDate` | `str \| None` | 최근 방문일 — KOS `lastVisitedDateTimeUtc` 의 KST 날짜 `YYYY-MM-DD`. KOS 가 주지 않으면 null | 칸 없음 — `visit` 에서 계산 가능하나 KOS 정의와 같은지 확인 안 됨 · 과거 방문은 수동 백필(어제까지) 범위만 | 가공 |
| `tickets` | `list[ExtTicket]` | 남은 시술권 — **사용 가능 또는 사용 중 장이 1장 이상인 묶음** 한 줄씩 · KOS 순서(다 쓴 · 다 취소된 묶음은 빠진다). 없으면 `[]`(고객은 있는데 남은 시술권 없음) | `ticket_bundle` · `ticket_set` · `ticket` |  |
| `tickets[].optionId` | `str` | 시술권의 옵션 KOS id(산 시점 값). 지금 메뉴에 없는 옵션이어도 그대로 준다 | `ticket_bundle.purchase_item_id` → `purchase_item.product_option_id` → `external_ref` | 가공 |
| `tickets[].optionTitle` | `str` | 시술권의 옵션 이름(산 시점 값 · 메뉴 이름으로 덮지 않는다) | `ticket_bundle.title` = 번들 `title`(`mapper_purchase.py:299`) — 다른 KOS 칸. 같은 값인지 확인 안 됨 | 가공 |
| `tickets[].remainingCount` | `int` | 남은 장수 — 묶음 안 `AVAILABLE` 시술권 수. `IN_USE`(쓰는 중) · `USED` · `CANCELED` 는 넣지 않는다 | `count(ticket.status='available')` | 가공 |
| `tickets[].inUseCount` | `int` | 사용 중 장수 — 묶음 안 `IN_USE`(시술 작업에 붙어 아직 안 끝남) 시술권 수. 남은 장수(`remainingCount`)와 따로 센다 | `count(ticket.status='in_use')` | 가공 |
| `tickets[].totalCount` | `int` | 묶음 안 시술권 장수 합(상태 무관 · 사용 중 장도 센다). GROUP 에서 한 세트를 다 쓰면 그 세트가 빠져 줄 수 있다 | `count(ticket)`(삭제 표시 제외) | 가공 |
| `tickets[].purchasedDate` | `str \| None` | 가장 이른 시술권 발행 시각(수납 완료 때)의 KST 날짜 `YYYY-MM-DD`. 없으면 null | 장 · 번들의 KOS 생성 시각 칸 없음(`models/ticket.py`) · `purchase` 에도 구매 일시 칸 없음 | 없음 |
| `tickets[].bundlePrice` | `ExtMoney` | **KOS 묶음 가격 그대로**(`price`). 고객이 낸 돈이 아니다. 산 시점 값에서 출발하지만 GROUP 에서 세트를 다 쓰면 줄 수 있다. 부가세 포함 여부는 표기하지 않는다 | `ticket_bundle.price_amount` ← 번들 `price`(`mapper_purchase.py:300`) · 통화 칸 없음 | 있음 |
| `prepaidCards` | `list[ExtPrepaidCard] \| None` | 선불카드(만료되지 않았고 잔액이 남은 카드 · KOS 순서). 없으면 `[]`. **선불카드 조회가 실패하면 null**(「카드 없음」 `[]` 과 다르다 · `partialErrors` 에 `prepaidCards`) | `prepaid_card`(+ 공유 고객 `prepaid_card_customer`) |  |
| `prepaidCards[].title` | `str` | 선불카드 이름(KOS 값) | `prepaid_card.title` | 있음 |
| `prepaidCards[].issuedDate` | `str \| None` | 발급일 — KOS `createdDateTimeUtc` 의 KST 날짜 `YYYY-MM-DD`. 없으면 null | 카드 KOS 생성 시각 칸 없음(`models/prepaid_card.py`) | 없음 |
| `prepaidCards[].expiresAt` | `str \| None` | 만료 일시 — KOS `expirationDateTimeUtc` 의 ISO `+09:00`. 없으면 null | `prepaid_card.expires_at` | 있음 |
| `prepaidCards[].balance` | `ExtBalance` | 현금 잔액 `{remaining, total}`(KOS `remainingBalance`) | `prepaid_card.balance_amount` = `remainingBalance.balance` 만 |  |
| `prepaidCards[].point` | `ExtBalance` | 포인트 잔액 `{remaining, total}`(KOS `remainingPoint`) | `prepaid_card.point_balance` = `remainingPoint.balance` 만 |  |
| `*.remaining (ExtBalance)` | `ExtMoney \| None` | 남은 금액(KOS `balance` · 금액 꼴). KOS 가 주지 않으면 null | `balance_amount` / `point_balance` | 있음 |
| `*.total (ExtBalance)` | `ExtMoney \| None` | 충전 총액(KOS `total` · 금액 꼴). KOS 가 주지 않으면 null | 칸 없음(`prepaid_card_ledger` 합으로 가능할 수 있으나 KOS `total` 과 같은지 확인 안 됨) | 없음 |
| `partialErrors` | `list[str]` | 실패한 KOS 읽기 칸 이름 — 지금은 `prepaidCards` 하나뿐. 없으면 `[]` | DAY DB 만 읽으면 의미가 바뀜(KOS 읽기 실패가 없음) |  |
| `*.value (ExtMoney)` | `int` | 금액(원 단위 정수) | `ticket_bundle.price_amount` · `prepaid_card.balance_amount` · `point_balance` | 있음 |
| `*.currency (ExtMoney)` | `str` | 통화 코드(ISO 4217 · 예 `KRW`) — KOS 값 그대로 | 통화 칸 없음(번들 · 카드) | 없음 |

### E3. `POST /api/ext/reservations`

**보내는 값(요청)**

| 필드 | 타입 | 뜻 |
|---|---|---|
| `body.name` | `str` | 고객 이름(필수). 앞뒤 공백만 지워 KOS 이름 검색에 그대로 보낸다 — **KOS 에 등록된 띄어쓰기 그대로** 보내야 한다(KOS 검색은 가운데 공백을 그대로 견준다). 앞뒤 공백을 지우면 비는 값은 400 |
| `body.email` | `str` | 고객 이메일(필수). 앞뒤 공백을 지우고 소문자로 바꿔 KOS 고객 email 과 정확히 같은지만 본다(형식 검사 없음). 앞뒤 공백을 지우면 비는 값은 400. 새 고객이면 이 이메일로 KOS 고객을 만든다 |
| `body.start` | `str` | 시작 시각 ISO-8601(오프셋이 없으면 KST 로 본다). 끝 = 시작 + 서버 기본 예약 그룹의 간격. ISO 가 아니면 400 |
| `body.memo` | `str \| None` | 예약 메모(선택). 비었거나 공백뿐이면 보내지 않는다 |

**받는 값(응답)**

| 필드 | 타입 | 뜻 | DAY 대응(11-20 조사) | 판정 |
|---|---|---|---|---|
| `reservationId` | `int` | 만든 예약의 ccc id | `visit.id` — DAY id 는 uuid(`models/*` `uuid_pk()`) — cc 정수 id 와 타입이 다르다(계약 변경) | 가공 |
| `customerId` | `int` | 예약 고객의 ccc id(새 고객이면 새로 만든 행) | `customer.id`(uuid) | 가공 |

### E4. `GET /api/ext/availability`

**보내는 값(요청)**

| 필드 | 타입 | 뜻 |
|---|---|---|
| `query date` | `str` |  |

**받는 값(응답)**

| 필드 | 타입 | 뜻 | DAY 대응(11-20 조사) | 판정 |
|---|---|---|---|---|
| `date` | `str` | 요청 날짜 `YYYY-MM-DD`(KST) | (계산) |  |
| `intervalMinutes` | `int` | 기본 예약 그룹의 시간 간격(분). 칸 끝 = `start` + 이 값(예약의 끝과 같다) | `reservation_group.interval_minutes` | 있음 |
| `slots` | `list[ExtSlot]` | 예약 가능한 칸 — 시각 오름차순. 없으면 `[]`(휴무 요일 · 다 참 · 다 지남) | `reservation_group_timetable` |  |
| `slots[].start` | `str` | 칸 시작 ISO `+09:00`(초 단위). 이 값을 그대로 예약(`POST /api/ext/reservations`) `start` 로 보내면 된다 | `reservation_group_timetable` + `interval_minutes` 로 계산 | 가공 |
| `slots[].remainingSeats` | `int` | 남은 자리 수(1 이상) — 기본 그룹의 켜진 구역마다 `max(0, 정원 − 예약 수)` 를 더한 값. 0 인 칸은 나오지 않는다 | 칸별 예약 수 칸 없음 · `reservation_group_capacity` 는 구역 정원 설정만 · DAY 일정은 오늘 창만 동기화(`services/emr_sync.py:111`)라 미래 날짜 예약 수를 셀 수 없음 | 없음 |

### E5. `POST /api/ext/customers/visits`

**보내는 값(요청)**

| 필드 | 타입 | 뜻 |
|---|---|---|
| `body.name` | `str` | 고객 이름(필수). 앞뒤 공백만 지워 KOS 이름 검색에 그대로 보낸다 — **KOS 에 등록된 띄어쓰기 그대로** 보내야 한다(KOS 검색은 가운데 공백을 그대로 견준다). 앞뒤 공백을 지우면 비는 값은 400 |
| `body.email` | `str` | 고객 이메일(필수). 앞뒤 공백을 지우고 소문자로 바꿔 KOS 고객 email 과 정확히 같은지만 본다(형식 검사 없음). 앞뒤 공백을 지우면 비는 값은 400 |

**받는 값(응답)**

| 필드 | 타입 | 뜻 | DAY 대응(11-20 조사) | 판정 |
|---|---|---|---|---|
| `visits` | `list[ExtVisit]` | 지금보다 앞선 일정 — 최신 순 · 최대 50건 · 취소 · 부도 포함. 없으면 `[]`(고객은 있는데 지난 일정 없음) | `visit`(과거 = 수동 백필 어제까지 + 운영 동기화가 본 날) |  |
| `visits[].date` | `str` | 일정 시작의 KST 날짜 `YYYY-MM-DD` | min(`visit_occupied_resource.start_at`) · 없으면 `visit.reserved_start_at` | 가공 |
| `visits[].start` | `str` | 일정 시작 ISO `+09:00`(묶음 시작 중 가장 이른 값) | 위와 같음 | 가공 |
| `visits[].result` | `Literal['completed', 'noshow', 'canceled', 'other']` | 결과 — KOS 예약 상태가 `COMPLETED` → `completed` · `NO_SHOW` → `noshow` · `CANCELED` → `canceled` · 그 밖(값 없음 포함) → `other`(직원 「이전 방문」 분류 그대로) | `visit.reservation_status` → 분류 | 가공 |
| `visits[].procedures` | `list[str]` | 그 일정 작업의 이름(KOS 배열 순서 · 빈 값이면 빈 문자열). 「방 배정」 기타 작업은 뺀다. 작업이 없으면 `[]` | `visit_task.title`(`is_room_assign` 제외) | 가공 |

### E6. `POST /api/ext/customers/reservations`

**보내는 값(요청)**

| 필드 | 타입 | 뜻 |
|---|---|---|
| `body.name` | `str` | 고객 이름(필수). 앞뒤 공백만 지워 KOS 이름 검색에 그대로 보낸다 — **KOS 에 등록된 띄어쓰기 그대로** 보내야 한다(KOS 검색은 가운데 공백을 그대로 견준다). 앞뒤 공백을 지우면 비는 값은 400 |
| `body.email` | `str` | 고객 이메일(필수). 앞뒤 공백을 지우고 소문자로 바꿔 KOS 고객 email 과 정확히 같은지만 본다(형식 검사 없음). 앞뒤 공백을 지우면 비는 값은 400 |

**받는 값(응답)**

| 필드 | 타입 | 뜻 | DAY 대응(11-20 조사) | 판정 |
|---|---|---|---|---|
| `reservations` | `list[ExtCustomerReservation]` | 오늘(KST) 0시 이후 일정 — 시작 오름차순 · 취소 · 부도 포함 · 개수 상한 없음. 없으면 `[]` | **DAY 는 오늘 하루 창만 동기화** — 내일 이후 일정 행이 없다(`services/emr_sync.py:111-115`) |  |
| `reservations[].reservationId` | `int \| None` | ccc 예약 id(예약 응답 `reservationId` 와 같은 체계). ccc 사본에 그 일정이 없으면 null — 외부 예약 API 로 만든 예약은 늘 id 가 있다 | `visit.id`(uuid) — 미래 일정 행 없음 | 없음 |
| `reservations[].date` | `str` | 일정 시작의 KST 날짜 `YYYY-MM-DD` | 미래 일정 행 없음 | 없음 |
| `reservations[].start` | `str` | 일정 시작 ISO `+09:00` | 미래 일정 행 없음 | 없음 |
| `reservations[].end` | `str \| None` | 첫 예약 묶음(시작 순 첫 번째)의 끝 ISO `+09:00`. 묶음이 없으면 null | 미래 일정 행 없음 | 없음 |
| `reservations[].state` | `Literal['reserved', 'reception', 'consultation', 'procedure', 'home', 'canceled', 'noshow']` | 상태 — 취소 · 부도가 먼저(`canceled` · `noshow`), 아니면 KOS 진행 단계로 정한다: `reserved`(예약 · 모르는 단계) · `reception`(접수) · `consultation`(상담 대기 · 상담) · `procedure`(시술 대기 · 시술) · `home`(시술 끝 · 귀가) | 미래 일정 행 없음(오늘 행은 `reservation_status`+`flow_step` 가공) | 없음 |

### E7. `GET /api/ext/reservations/board`

**보내는 값(요청)**

없음(키 헤더만)

**받는 값(응답)**

| 필드 | 타입 | 뜻 | DAY 대응(11-20 조사) | 판정 |
|---|---|---|---|---|
| `date` | `str` | 오늘 KST `YYYY-MM-DD` | (계산) |  |
| `now` | `str` | 서버 지금 시각 ISO `+09:00` | (계산) |  |
| `sync` | `ExtSync` | 사본 신선도 | - |  |
| `sync.lastOkAt` | `str \| None` | 그날 KOS 날짜 조회가 마지막으로 성공한 시각 ISO `+09:00`(직원 예약 현황 `sync` 와 같은 값) | DAY 일정 회차 마지막 성공 시각 칸 확인 안 됨(Redis 잠금 · `RunResult` 만 확인) | 없음 |
| `sync.lastError` | `str \| None` | 마지막 날짜 조회 실패 문구 — 있으면 이 목록은 낡은 사본일 수 있다. 없으면 null | 확인 안 됨 | 없음 |
| `partialErrors` | `list[str]` | 일부 KOS 읽기가 실패했거나 아직 못 한 칸 이름 — 지금은 `consultationHistory`(아직 확인하지 못한 처음 상담 대기 시각이 있다)만 있다. 없으면 `[]` | (계산) |  |
| `reservations` | `list[ExtBoardRow]` | 오늘 예약 — 예약 1건 = 1줄(묶음이 여럿이어도) · 상태로 거르지 않는다(취소 · 부도 · 귀가 포함) · 시작 오름차순 → id | `visit`(오늘 · 10초 동기화) |  |
| `reservations[].reservationId` | `int` | ccc 예약 id — 예약 상세 · 오더 메모 · 상담 메모 경로의 id | `visit.id` — DAY id 는 uuid(`models/*` `uuid_pk()`) — cc 정수 id 와 타입이 다르다(계약 변경) | 가공 |
| `reservations[].start` | `str \| None` | 첫 묶음 시작 ISO `+09:00`. 묶음이 없으면 null | min(`visit_occupied_resource.start_at`) | 가공 |
| `reservations[].end` | `str \| None` | 묶음 끝 중 가장 늦은 값 ISO `+09:00`. 묶음이 없으면 null | max(`visit_occupied_resource.end_at`) | 가공 |
| `reservations[].state` | `_State` | 2계층 상태(직원 판 그대로) | `visit.reservation_status` + `visit.flow_step` |  |
| `*.main (_State)` | `str` | 주 상태 — 직원 예약 현황 2계층 상태 그대로(`reserved` · `reception` · `consultation` · `procedure` · `home` · `canceled` · `noshow`) | 같은 계산 | 가공 |
| `*.sub (_State)` | `str \| None` | 부 상태(직원 판 그대로 · 예 `waiting` · `doing`). 없으면 null | 같은 계산 | 가공 |
| `reservations[].customer` | `ExtBoardCustomer` | 고객(직원 예약 현황 카드 고객 칸과 같은 값) | `customer` + `visit` |  |
| `customer.customerId` | `int \| None` | ccc 고객 id. 사본에 고객이 없으면 null | `customer.id`(uuid) | 가공 |
| `customer.name` | `str` | 고객 이름(고객 사본) | `customer.name` | 있음 |
| `customer.phoneticName` | `str \| None` | 발음 이름 | `customer.name_pronunciation` | 있음 |
| `customer.gender` | `str \| None` | 성별(KOS 값) | `customer.gender`(DAY 는 `GENDERS` 표로 바꿔 저장 `mapper.py:311` — 표기 다름) | 가공 |
| `customer.nationality` | `str \| None` | 국적(KOS 값) | `customer.nationality` | 있음 |
| `customer.isNew` | `bool` | KOS 신규 고객 여부 | `visit.is_new`(이 방문 기준) | 있음 |
| `reservations[].receptionAt` | `str \| None` | 접수 시각 ISO `+09:00`(KOS 접수 시각) — **귀가한 예약도 준다**. 접수 전이면 null. 접수 뒤인데 KOS 가 비워 준 일정도 null | `visit.reception_at` | 있음 |
| `reservations[].counselor` | `ExtStaffRef \| None` | **KOS 희망 상담사**(예약에 지정한 상담사 — 실제로 상담한 사람이 아니다 · 예약 상세 `reservation.counselor` 와 같은 값). 없으면 null | `visit.requested_counselor_id` ← `reservation.counselor`(`mapper.py:572`) | 있음 |
| `counselor.staffId (ExtStaffRef)` | `int \| None` | ccc 직원 사본 id(직원 목록 `GET /api/ext/clinics/{clinicId}/staff` 와 같은 체계). 사본에 없는 KOS 계정이면 null | `staff.id`(uuid) | 가공 |
| `counselor.name (ExtStaffRef)` | `str` | 이름(KOS 값) | `staff.name` | 있음 |
| `reservations[].roomTitle` | `str \| None` | 관리실 — 작업에 붙은 방 중 **가장 늦게 배정된 방** 이름. 방이 없으면 null | `visit.room_id` → `room.title`(같은 규칙 `mapper.py:388-408`) | 가공 |
| `reservations[].consultation` | `bool` | 상담 거침(CC 판정) — 접수 뒤이고 ① 지금 상담 대기 · 상담 ② CC 접수가 상담 대기로 끝남 ③ CC 「상담 추가」 중 하나. 취소 · 부도 · 접수 전이면 false. KOS 「상담 필요」 체크는 보지 않는다 | `visit_flow_log` 의 CONSULTATION_WAITING/CONSULTATION 행으로 계산 가능 · cc 조작 사건(CC 접수 · 상담 추가)에 대응하는 DAY 조작 없음 | 가공 |
| `reservations[].firstConsultationWaitingAt` | `str \| None` | 처음 상담 대기가 된 시각 ISO `+09:00` — KOS 단계 변경 이력에서 찾은 값. **`consultation` 과 따로 정한다** (`consultation = false` 여도 값이 있을 수 있다 — KOS 웹에서만 상담 대기를 지나간 일정). null = 접수 전 · 취소 · 부도 · 아직 못 찾음(이력에 없음 · 조회 실패 · 다음 단계 변화 전 · 요청당 상한 · 다른 요청이 확인 중 · 그날 끝까지 못 찾음) | min(`visit_flow_log.changed_at`) where flow_step=CONSULTATION_WAITING — 값 = 10초 조회가 본 `flowStepUpdatedDateTimeUtc`(`sync_schedules.py:351-362`) · 조회 사이에 지나간 단계는 빠짐 | 가공 |

### E8. `GET /api/ext/reservations/{reservationId}`

**보내는 값(요청)**

| 필드 | 타입 | 뜻 |
|---|---|---|
| `path reservationId` | `int` |  |
| `header X-Ext-Staff-Id` | `str\|None` | 선택 — 연동처 직원 id(열람 기록용 · 검증 안 함) |

**받는 값(응답)**

| 필드 | 타입 | 뜻 | DAY 대응(11-20 조사) | 판정 |
|---|---|---|---|---|
| `reservationId` | `int` | ccc 예약 id | `visit.id`(uuid) | 가공 |
| `day` | `str` | 예약 날짜 KST `YYYY-MM-DD` | `visit.reserved_start_at` KST 날짜 | 가공 |
| `start` | `str \| None` | 첫 묶음 시작 ISO `+09:00`. 묶음이 없으면 null | min(`visit_occupied_resource.start_at`) | 가공 |
| `end` | `str \| None` | 묶음 끝 중 가장 늦은 값 ISO `+09:00`. 묶음이 없으면 null | max(`visit_occupied_resource.end_at`) | 가공 |
| `state` | `_State` | 2계층 상태(직원 판 그대로) | `visit.reservation_status` + `flow_step` |  |
| `customer` | `ExtDetailCustomer` | 고객 기본 정보 + 나이 · 언어 · 고객 유입(전화 · 이메일 · 여권 · 주소 없음) | `customer` |  |
| `customer.customerId` | `int \| None` | ccc 고객 id. 예약에 고객 사본이 없으면 null | `customer.id`(uuid) | 가공 |
| `customer.name` | `str` | 고객 이름(고객 사본 · 직원 상세와 같은 값) | `customer.name` | 있음 |
| `customer.phoneticName` | `str \| None` | 발음 이름(고객 사본) | `customer.name_pronunciation` | 있음 |
| `customer.gender` | `str \| None` | 성별(KOS 값 그대로) | `customer.gender`(표기 다름) | 가공 |
| `customer.nationality` | `str \| None` | 국적(KOS 값 그대로) | `customer.nationality` | 있음 |
| `customer.isNew` | `bool` | KOS 신규 고객 여부 | `visit.is_new` | 있음 |
| `customer.chartNumber` | `str \| None` | 차트 번호(KOS 값) | `customer.chart_number` | 있음 |
| `customer.age` | `int \| None` | 그 예약 날짜 기준 나이(KOS 고객 생년월일). 고객 읽기 실패 · 생년월일 없음이면 null | `customer.birth_date`(일정 visitor `dateOfBirth` · `mapper.py:312`) + 예약 날짜 | 가공 |
| `customer.language` | `str \| None` | 고객 언어 — KOS 고객 `language` 값 그대로. 고객 읽기 실패 · 값 없음이면 null | `customer.language` 칸은 있으나 동기화가 채우지 않음(`mapper.py:300-329`) | 없음 |
| `customer.funnel` | `ExtFunnel \| None` | 고객 유입(KOS 고객 `visitorFunnel`). 없음 · 고객 읽기 실패면 null | `customer.funnel_id` · `funnel_detail` 칸은 있으나 동기화가 채우지 않음 |  |
| `*.name (ExtFunnel)` | `str \| None` | 유입 이름(KOS 유입 코드 이름). 없으면 null | 고객: 없음(미동기화) / 예약: `visit.funnel_id`→`funnel.name` | 가공 |
| `*.detail (ExtFunnel)` | `str \| None` | 유입 상세 글(KOS 값). 없으면 null | 고객: 없음 / 예약: `visit.funnel_detail` | 가공 |
| `reservation` | `ExtDetailReservation` | 예약 칸 | `visit` |  |
| `reservation.memo` | `str \| None` | 예약 메모(KOS `reservationMemo`). **오더 메모 · 상담 메모와 다른 칸**이다 | `visit.reservation_notes` | 있음 |
| `reservation.desiredDischargeAt` | `str \| None` | 귀가 희망 시각 ISO `+09:00`. 없으면 null | `visit.desired_discharge_at` | 있음 |
| `reservation.funnel` | `ExtFunnel \| None` | 예약 유입. 없으면 null | `visit.funnel_id` · `funnel_detail` |  |
| `reservation.counselor` | `ExtStaffRef \| None` | **KOS 희망 상담사**(예약에 지정한 상담사 — 실제로 상담한 사람이 아니다). 없으면 null | `visit.requested_counselor_id` | 있음 |
| `reservation.orderMemo` | `str \| None` | 지금 오더 메모(KOS 일정 `orderMemo` 그대로 · 빈 문자열 그대로) — 오더 메모 쓰기가 통째로 바꾸는 칸. null = KOS 일정 읽기 실패(`partialErrors` 에 `schedule`) | `visit.procedure_order_note` ← 일정 `orderMemo`(`mapper.py:598`) · 오늘 일정만 10초 | 있음 |
| `reservation.consultationMemo` | `str \| None` | 지금 상담 메모(= 차트 메모 · KOS 일정 `consultation.consultationMemo` 그대로) — 상담 메모 쓰기가 통째로 바꾸는 칸. null = KOS 일정 읽기 실패 · 상담 정보 없음 | `consultation.consultation_note` ← 일정 `consultations[].content.text`(`mapper.py:507` · SPEC-000:535) — **다른 KOS 칸** | 없음(시점 다름) |
| `reservation.requestedDoctor` | `ExtStaffRef \| None` | 희망 의사(KOS 예약 `doctor`). 없음 · KOS 일정 읽기 실패면 null | `visit.requested_doctor_id` ← `reservation.doctor`(`mapper.py:575`) | 있음 |
| `reservation.requestedProcedures` | `list[ExtRequestedProcedure] \| None` | 희망 시술(KOS 예약 `requestedProcedures` 순서). `[]` = 희망 시술 없음 · null = KOS 일정 읽기 실패 | `visit_requested_procedure` |  |
| `requestedProcedures[].type` | `str` | `OPTION`(상품 옵션) · `TICKET`(시술권) — KOS 값 그대로 | `visit_requested_procedure.kind`(enum) | 있음 |
| `requestedProcedures[].optionId` | `str \| None` | `OPTION` 의 옵션 KOS id(메뉴 `options[].id` 와 같은 체계). `TICKET` 이면 null | `product_option_id` 칸은 있으나 매퍼가 KOS 옵션 id 를 두지 않음(`mapper.py:335`) | 없음 |
| `requestedProcedures[].optionTitle` | `str \| None` | `OPTION` 의 옵션 이름. `TICKET` 이면 null | `visit_requested_procedure.option_title`(OPTION) | 있음 |
| `requestedProcedures[].productTitle` | `str \| None` | `OPTION` 의 상품 이름. `TICKET` 이면 null | `visit_requested_procedure.product_title`(TICKET 이면 `ticketConfiguration.productTitle` 도 넣음 — cc 는 null) | 가공 |
| `requestedProcedures[].ticketId` | `str \| None` | `TICKET` 의 시술권 KOS id. `OPTION` 이면 null | 칸 없음 | 없음 |
| `requestedProcedures[].ticketTitle` | `str \| None` | `TICKET` 의 시술권 이름. `OPTION` 이면 null | `visit_requested_procedure.option_title`(TICKET 일 때 · `mapper.py:343-346`) | 가공 |
| `health` | `ExtHealth` | 문진(직원 상세 `health` 와 같은 모양 · 같은 계산) | `questionnaire_history` 표는 있으나 KOS 동기화가 쓰지 않음(쓰는 코드 0 — `git grep` 결과 모델 · 식별자뿐) |  |
| `health.state` | `str` | `ok`(제출본 있음) · `none`(제출 안 함) · `error`(문진 읽기 실패 — `partialErrors` 에 `questionnaire`) — 직원 상세 `health` 와 같은 계산 | 원천 없음 | 없음 |
| `health.submittedAt` | `str \| None` | 제출 시각 ISO `+09:00`. 없으면 null | `questionnaire_history.submitted_at`(미동기화) | 없음 |
| `health.needCount` | `int` | 확인이 필요한 답 수(직원 상세와 같은 규칙) | 원천 없음 | 없음 |
| `health.items` | `list[dict[str, Any]]` | 「건강 정보」 질문 × 답 — 직원 상세 `health.items` 와 같은 모양 | 원천 없음 | 없음 |
| `previousVisits` | `list[ExtPrevVisit] \| None` | 이전 방문(최신 순 · 그 예약 날짜와 같은 날 일정은 뺀다) — **예약 메모 · 상담 메모 · 의사 이름 · 상담자를 준다**(과거 시술 경로와 다르다). null = 이전 방문 조회 실패(`partialErrors` 에 `previousVisits`) | `visit`(과거 = 수동 백필 어제까지) |  |
| `previousVisits[].date` | `str` | 일정 시작의 KST 날짜 `YYYY-MM-DD` | min(`visit_occupied_resource.start_at`) | 가공 |
| `previousVisits[].start` | `str` | 일정 시작 ISO `+09:00` | 위와 같음 | 가공 |
| `previousVisits[].result` | `str` | 결과 — `completed` · `noshow` · `canceled` · `other`(직원 「이전 방문」 분류) | `visit.reservation_status` 분류 | 가공 |
| `previousVisits[].resultRaw` | `str \| None` | KOS 예약 상태 값 그대로 | `visit.reservation_status`(DAY enum 소문자 표기 가능성 — 값 표기 확인 안 됨) | 가공 |
| `previousVisits[].zoneTitle` | `str \| None` | 구역 이름 | `visit.reception_zone_id` → `zone.title`(`zone` = 일정 `zone` · `mapper.py:593`) | 가공 |
| `previousVisits[].groupTitle` | `str \| None` | 예약 그룹 이름(사본에 그 그룹이 있을 때) | `visit_occupied_resource.reservation_group_id` → `reservation_group.title` | 가공 |
| `previousVisits[].reservationMemo` | `str \| None` | 그 방문의 예약 메모(KOS 값). 없으면 null | `visit.reservation_notes` | 있음 |
| `previousVisits[].consultationMemo` | `str \| None` | 그 방문의 상담 메모(KOS 값). 없으면 null | `consultation.consultation_note` ← `consultations[].content.text` — 다른 KOS 칸 | 없음(시점 다름) |
| `previousVisits[].procedures` | `list[ExtPrevProcedure]` | 그 방문의 작업(의사 이름 포함) | `visit_task` |  |
| `procedures[].title` | `str` | 작업 이름(KOS 값 · 「방 배정」 기타 작업은 뺀다) | `visit_task.title` | 있음 |
| `procedures[].status` | `str \| None` | 작업 상태(KOS 값 그대로) | `visit_task.status`(DAY enum — 표기 다름) | 가공 |
| `procedures[].doctors` | `list[str]` | 그 작업의 의사 이름(KOS 순서) | `visit_task_staff`(role=doctor) → `staff.name` | 가공 |
| `previousVisits[].counselors` | `list[ExtStaffRef]` | 그 방문의 상담자 — KOS 일정 `consultations[].counselors[]`(나온 차례 · 같은 사람은 한 번). 그것이 비면 `consultation.counselor` 하나. 둘 다 없으면 `[]` | `consultation.counselor_id` ← `consultations[].counselors` **1명일 때만**(`mapper.py:491-505`) | 가공 |
| `partialErrors` | `list[str]` | 실패한 KOS 읽기 — `schedule`(희망 시술 · 희망 의사 · 지금 메모 둘이 null) · `visitor`(나이 · 언어 · 고객 유입 null) · `questionnaire`(`health.state = error`) · `previousVisits`(null). 없으면 `[]` | (계산) |  |
| `*.main (_State)` | `str` | 주 상태 — 직원 예약 현황 2계층 상태 그대로(`reserved` · `reception` · `consultation` · `procedure` · `home` · `canceled` · `noshow`) | `visit.reservation_status` + `flow_step` | 가공 |
| `*.sub (_State)` | `str \| None` | 부 상태(직원 판 그대로 · 예 `waiting` · `doing`). 없으면 null | 같은 계산 | 가공 |
| `counselor/requestedDoctor/counselors[].staffId (ExtStaffRef)` | `int \| None` | ccc 직원 사본 id(직원 목록 `GET /api/ext/clinics/{clinicId}/staff` 와 같은 체계). 사본에 없는 KOS 계정이면 null | `staff.id`(uuid) | 가공 |
| `counselor/requestedDoctor/counselors[].name (ExtStaffRef)` | `str` | 이름(KOS 값) | `staff.name` | 있음 |

### E9. `PUT /api/ext/customers/{customerId}/language`

**보내는 값(요청)**

| 필드 | 타입 | 뜻 |
|---|---|---|
| `path customerId` | `int` |  |
| `header X-Ext-Staff-Id` | `str\|None` | 선택 — 연동처 직원 id(열람 기록용 · 검증 안 함) |
| `body.language` | `str` | 고객 언어 — KOS 언어 값 그대로(꼴 검사 없이 KOS 에 보낸다 · 예 2자 · 5자 코드). 앞뒤 공백을 지운다. **빈 문자열 = 비움** · null 은 400 |

**받는 값(응답)**

| 필드 | 타입 | 뜻 | DAY 대응(11-20 조사) | 판정 |
|---|---|---|---|---|
| `ok` | `bool` | 늘 `true` — KOS 쓰기가 성공했다(또는 고객 언어가 이미 같은 값이라 쓰지 않았다) | (계산) |  |

### E10. `PUT /api/ext/reservations/{reservationId}/order-memo`

**보내는 값(요청)**

| 필드 | 타입 | 뜻 |
|---|---|---|
| `path reservationId` | `int` |  |
| `header X-Ext-Staff-Id` | `str\|None` | 선택 — 연동처 직원 id(열람 기록용 · 검증 안 함) |
| `body.orderMemo` | `str` | 오더 메모 글 전체 — **통째로 바꾼다**(일정 하나에 글 하나). 지금 값은 예약 상세 `reservation.orderMemo`. 빈 문자열은 그대로 보낸다(비움) |

**받는 값(응답)**

| 필드 | 타입 | 뜻 | DAY 대응(11-20 조사) | 판정 |
|---|---|---|---|---|
| `ok` | `bool` | 늘 `true` — KOS 쓰기가 성공했다(또는 고객 언어가 이미 같은 값이라 쓰지 않았다) | (계산) |  |

### E11. `PUT /api/ext/reservations/{reservationId}/consultation-memo`

**보내는 값(요청)**

| 필드 | 타입 | 뜻 |
|---|---|---|
| `path reservationId` | `int` |  |
| `header X-Ext-Staff-Id` | `str\|None` | 선택 — 연동처 직원 id(열람 기록용 · 검증 안 함) |
| `body.consultationMemo` | `str` | 상담 메모(= 차트 메모) 글 전체 — **통째로 바꾼다**. 지금 값은 예약 상세 `reservation.consultationMemo`. **빈 값은 받지 않는다** — 앞뒤 공백을 지우면 비는 값은 `400`(KOS 가 상담 메모를 비우지 못한다 · 빈 값을 보내면 200 인데 그대로 남는다). 비우는 쓰기는 없다(오더 메모와 다르다) |

**받는 값(응답)**

| 필드 | 타입 | 뜻 | DAY 대응(11-20 조사) | 판정 |
|---|---|---|---|---|
| `ok` | `bool` | 늘 `true` — KOS 쓰기가 성공했다(또는 고객 언어가 이미 같은 값이라 쓰지 않았다) | (계산) |  |

### E12. `GET /api/ext/clinic`

**보내는 값(요청)**

없음(키 헤더만)

**받는 값(응답)**

| 필드 | 타입 | 뜻 | DAY 대응(11-20 조사) | 판정 |
|---|---|---|---|---|
| `clinicId` | `int` | CC 고정 값 `1` — CC 서버 하나 = KOS 병원 하나. 직원 목록 경로(`/api/ext/clinics/{clinicId}/staff`)에 쓴다. **전역 유일하지 않다**(CC 서버 여럿을 모으면 겹친다) | `hospital.id`(uuid · 병원 여럿) | 가공 |
| `name` | `str \| None` | 병원 이름(KOS 값 · 비면 null) | `hospital.name` 은 DAY 가 정한 이름 — KOS 에서 받지 않음 | 없음(시점 다름) |
| `phone` | `str \| None` | 대표 전화(KOS 값 그대로 · 국가 번호를 붙이지 않는다 · 비면 null) | 칸 없음 | 없음 |
| `address` | `ExtAddress \| None` | 주소. 세 칸이 모두 비면 null | 칸 없음 |  |
| `address.address` | `str \| None` | 주소(KOS 값 · 비면 null) | 칸 없음 | 없음 |
| `address.detailed` | `str \| None` | 상세 주소(KOS 값 · 비면 null) | 칸 없음 | 없음 |
| `address.zipCode` | `str \| None` | 우편번호(KOS 값 · 비면 null) | 칸 없음 | 없음 |
| `operatingHours` | `dict[str, ExtDayHours]` | **병원 기본 운영 시간**(예약 그룹별 시간표가 아니다) — 요일 키 `monday` … `sunday` | `reservation_group_timetable` 은 **예약 그룹별** 시간표 — 병원 기본 시간표 아님 |  |
| `*.enabled (ExtDayHours)` | `bool` | 그 요일 운영하나(시작 · 끝이 다 있을 때만 true) | 병원 기본 칸 없음 | 없음(시점 다름) |
| `*.start (ExtDayHours)` | `str \| None` | 운영 시작 KST `HH:MM` | 병원 기본 칸 없음 | 없음(시점 다름) |
| `*.end (ExtDayHours)` | `str \| None` | 운영 끝 KST `HH:MM` | 병원 기본 칸 없음 | 없음(시점 다름) |
| `*.breakStart (ExtDayHours)` | `str \| None` | 쉬는 시간 시작 KST `HH:MM`. 없으면 null | 병원 기본 칸 없음 | 없음(시점 다름) |
| `*.breakEnd (ExtDayHours)` | `str \| None` | 쉬는 시간 끝 KST `HH:MM`. 없으면 null | 병원 기본 칸 없음 | 없음(시점 다름) |
| `daysOff` | `list[ExtDayOff]` | 병원 기본 휴무 — 오늘(KST) ~ 오늘 + 90일 · KOS 차례. 없으면 `[]` | 칸 없음 |  |
| `daysOff[].startDate` | `str` | 휴무 첫날 KST `YYYY-MM-DD` | 칸 없음 | 없음 |
| `daysOff[].endDate` | `str` | 휴무 마지막 날 KST `YYYY-MM-DD`(하루 휴무면 `startDate` 와 같다 · 여러 날 휴무는 한 원소) | 칸 없음 | 없음 |

### E13. `GET /api/ext/clinics/{clinicId}/staff`

**보내는 값(요청)**

| 필드 | 타입 | 뜻 |
|---|---|---|
| `path clinicId` | `int` |  |

**받는 값(응답)**

| 필드 | 타입 | 뜻 | DAY 대응(11-20 조사) | 판정 |
|---|---|---|---|---|
| `clinicId` | `int` | 요청한 `clinicId` | `hospital.id` | 가공 |
| `staff` | `list[ExtStaff]` | 직원 — KOS 차례 · KOS 시스템 계정 · 제외 목록 계정은 뺀다 | `staff`(내부 같은 경로 · 1시간 동기화) |  |
| `staff[].staffId` | `int \| None` | ccc 직원 사본 id(접수 목록 · 예약 상세의 `counselor.staffId` 와 같은 체계). 사본에 아직 없는 계정이면 null | `staff.id`(uuid) | 가공 |
| `staff[].name` | `str` | 이름(KOS 지금 값) | `staff.name`(1시간) | 있음 |
| `staff[].roleName` | `str \| None` | KOS 역할 이름(지점마다 설정이 다름 · 예 「CS팀(콜센터)」 = 외주 직원). 외주 직원은 이 칸으로 가른다 | `staff.job_role_id` → `job_role.name`(내부 `role/v2/queries/get-roles`) | 가공 |
| `staff[].roleTags` | `list[str]` | 역할 태그(`ADMIN` · `DOCTOR` · `COUNSELOR` · `NURSE` · `SKINCARE` · `CALL_COUNSELOR` · `COORDINATOR`) — ccc 직원 사본 값. 사본에 없는 계정이면 `[]`. `CALL_COUNSELOR` 가 있다고 외주가 아니다(코디 · 관리자에게도 붙는다) | `job_role.tags`(직무 단위 · 출처 = 역할 조회) — 계정 `roleTags` 와 같은 값인지 확인 안 됨 | 가공 |
| `staff[].active` | `bool` | 활성 계정인가(KOS 값 · 비활성 직원도 싣는다) | `staff.is_active` | 있음 |
| `staff[].email` | `str \| None` | 이메일(KOS 지금 값). KOS 에 값이 없으면 null | `staff.email`(`mapper.py:241`) | 있음 |
| `staff[].realName` | `str \| None` | 실명(KOS `realName` 지금 값). KOS 에 값이 없으면 null. `name`(KOS 표시 이름)과 다른 칸이다 | `staff.real_name`(`mapper.py:240`) | 있음 |
| `staff[].kosAccountId` | `str` | KOS 계정 id(문자열 · null 없음 · 사본에 없는 계정도 값이 있다). `staffId`(ccc)와 다른 체계다 — 다른 ext 응답의 `staffId` 와 이 값을 잇는 곳은 이 목록뿐이다 | `external_ref`(entity=staff).external_id | 가공 |
