# 조사 리포트 — cc-prototype ext API 현황 · DAY 이관 가능성

- 작성: day `researcher` · 2026-11-20 · 조사(판단 없음 — 판단은 C 「정할 것」)
- 읽은 ref(전부 read-only · `git show` / `git grep`):
  - cc-prototype `origin/main` = `0553173` — `procedure/back/`
  - CENTURION_DAY `origin/dev` = `844eace4` — `backend/` · `deploy/`
  - mediness-mediness `origin/main` = `ccede286` — `products/day/`
  - 프로필 문서: `para/projects/summer-star/cc-prototype/`(SPEC-008 0.4.7 · DEC-010 ~ 012 · WORK-012 ~ 015 · 회고 셋) · `orchestration/config/projects/day.json` `data_rules`
- 근거 표기: cc = `cc:<파일>:<줄>`(경로는 `procedure/back/app/` 아래), DAY = `day:<파일>:<줄>`(경로는 `backend/` 아래). 줄은 위 ref 기준.
- KOS · DAY 서버 · 연동처 실호출 0 · 키 · 토큰 · 개인정보 0(env 는 키 이름만).

## 0. 요약

| 항목 | 값 |
|---|---|
| ext 엔드포인트 수 | **13**(`git grep -c "@router\." origin/main -- procedure/back/app/api/ext.py` → `13` · 라우터 prefix `/api/ext` `cc:api/ext.py:41,101` · 붙는 곳 `cc:main.py:130-132`) · ext 밖에 연동처 키로 열리는 경로 0 |
| 스키마 필드(요청 · 응답 · 중첩) | **203** — 엔드포인트마다 표 행과 대조해 빠진 필드 0(§A2 표 머리) |
| **B1** DAY DB 대응(값 칸 151 — 묶음 · 계산 · 요청 칸 제외) | **있음 51 · 가공 65 · 없음 26 · 없음(시점 다름) 9** |
| **B3** 방향(KOS → DAY → 서비스) | DAY DB 만으로 응답 가능 **3**(메뉴 · 접수 목록 · 직원) · KOS 실시간 조회 필요 **5**(고객 조회 · 가능 시간대 · 예약 내역 · 예약 상세 · 병원) · 지금 그대로는 불가 **1**(과거 시술 — 고객 식별) · 쓰기 **4**(B4) |
| **B4** 방향(서비스 → DAY → KOS) | cc 쓰기 넷이 쓰는 KOS 경로 6개 중 DAY `writes.py` 에 있는 것 **0** · DAY 쓰기 큐는 「누른 직원의 KOS 토큰」만 씀 → 연동처 쓰기에 쓸 토큰이 없다 |
| 뜻 불일치 후보(A2-1) | **8** |
| **D2** Swagger 필드 설명 | 충분 **169** · 부족 **34** · 없음 **0**(203 필드 · 엔드포인트별 §D2) |
| 정할 것(C) | **21** |
| B6 도메인 | `day.medisolveai.com` 은 이미 DAY **prod** 앞단(Caddy)에 붙어 있다 · prod 는 Swagger 가 꺼져 있다 |

핵심 사실 다섯:

1. **cc ext 는 거의 KOS 실시간 중계였다.** 13개 중 KOS 를 안 부르는 것은 메뉴 하나(cc 사본)뿐이고, 고객 조회 · 예약 내역 · 과거 시술 · 상세 · 병원 · 직원은 요청마다 KOS 를 읽는다(§A2 「값의 출처」 · SPEC-008 §6.9).
2. **DAY 일정 동기화는 「오늘 하루」 창만 10초마다 받는다**(`day:day/services/emr_sync.py:111-115` · `day:day/tasks/emr.py:3-8`). 미래 일정은 DAY 에 없고, 과거는 수동 백필(어제까지 · `day:day/services/emr_backfill.py:1-5`)로만 들어온다.
3. **DAY 고객 동기화는 `email` · `language` · 고객 유입을 채우지 않는다**(칸은 있다 — `day:day/models/customer.py:54,65,77-78` · 매퍼에 없다 `day:day/emr/kos/mapper.py:300-329`). cc 의 「이름 + 이메일」 식별을 DAY DB 로는 못 한다.
4. **사람 칸 시점**: cc 의 `counselor`(접수 목록 · 예약 상세)는 **예약 때 지정한 희망 상담사**(`reservation.counselor`)다. 상담 차트의 상담사는 예약 상세의 `previousVisits[].counselors` 에만 있다. DAY 에는 두 칸이 따로 있다 — `visit.requested_counselor_id`(희망) · `consultation.counselor_id`(상담 기록).
5. **「상담 메모」 원천이 cc 와 DAY 가 다르다** — cc = 일정 `consultation.consultationMemo`(공개 쓰기 경로와 같은 칸) · DAY = 일정 `consultations[].content.text`(`day:day/emr/kos/mapper.py:507`). 같은 글인지 확인 안 됨.

---

## A. 현황 (cc-prototype)

### A1. API 목록

센 명령: `git -C cc-prototype grep -n "@router\." origin/main -- procedure/back/app/api/` 중 `api/ext.py` 행 13개(`:238,249,262,334,348,354,416,424,484,492,500,537,543`). 라우터 `APIRouter(prefix="/api/ext", tags=["외부 연동"])`(`cc:api/ext.py:101`) · `create_app` 이 마지막에 붙인다(`cc:main.py:130-132`) · 미들웨어 `ext_middleware` 가 `/api/ext` 접두로 거른다(`cc:main.py:114` · `cc:api/ext.py:110-142`). 연동처 키(`require_ext_key`)를 쓰는 경로는 이 13개뿐이다 — Swagger 시험이 「ext 밖 operation 에 ExtApiKey security 없음」을 단언한다(`tests/test_ext_docs.py:46-47`).

| # | 메서드 · 경로 | 요약 | 읽기/쓰기 | 추가된 판 · 결정 · 작업 | 시험(`tests/` · 함수 수) |
|---|---|---|---|---|---|
| E1 | `GET /api/ext/menu` | 메뉴 트리(카테고리 → 상품 → 옵션 → 구성) | 읽기(cc 사본) | SPEC 0.1.0 · DEC-010 D-11 ① · WORK-012 | `test_ext_menu.py`(4) · `test_ext_menu_sync.py`(8) |
| E2 | `POST /api/ext/customers/lookup` | 이름+이메일 또는 customerId → 고객 · 남은 시술권 · 선불카드 | 읽기(+ cc 고객 사본 덮어쓰기) | 0.1.0 · DEC-010 D-11 ② / 0.4.0 고침 DEC-012 D-08 · WORK-012 · 014 | `test_ext_lookup.py`(11) · `test_ext_lookup2.py`(16) |
| E3 | `POST /api/ext/reservations` | 이름+이메일+시작 → 예약(없으면 KOS 고객 생성) | **쓰기**(KOS) | 0.1.0 · DEC-010 D-11 ③ · WORK-012 | `test_ext_reserve.py`(7) |
| E4 | `GET /api/ext/availability?date=` | 기본 예약 그룹의 그날 칸 · 남은 자리 | 읽기(+ cc 칸 사본 갱신) | 0.3.0 · DEC-011 D-02 · WORK-013 | `test_ext_availability.py`(14) |
| E5 | `POST /api/ext/customers/visits` | 과거 일정 최신 50 | 읽기 | 0.3.0 · DEC-011 D-03 · WORK-013 | `test_ext_history.py`(17) |
| E6 | `POST /api/ext/customers/reservations` | 오늘 0시 이후 일정 | 읽기 | 0.3.0 · DEC-011 D-04 · WORK-013 | `test_ext_history.py`(위와 같은 파일) |
| E7 | `GET /api/ext/reservations/board` | 오늘 접수 목록(예약 단위) | 읽기(+ cc 이력 표 쓰기) | 0.4.0 · DEC-012 D-09 · D-16 · WORK-014 | `test_ext_board.py`(21) |
| E8 | `GET /api/ext/reservations/{reservationId}` | 예약 상세 | 읽기(+ cc 예약 사본 덮어쓰기) | 0.4.0 · DEC-012 D-10 · WORK-014 | `test_ext_detail.py`(10) |
| E9 | `PUT /api/ext/customers/{customerId}/language` | 고객 언어 | **쓰기**(KOS) | 0.4.0 · DEC-012 D-11 · WORK-014 | `test_ext_write.py`(14) |
| E10 | `PUT /api/ext/reservations/{reservationId}/order-memo` | 오더 메모 통째로 | **쓰기**(KOS) | 0.4.0 · DEC-012 D-12 · WORK-014 | `test_ext_write.py` |
| E11 | `PUT /api/ext/reservations/{reservationId}/consultation-memo` | 상담 메모(= 차트 메모) 통째로 | **쓰기**(KOS) | 0.4.0 · DEC-012 D-13 · 0.4.6 D-47 · WORK-014 | `test_ext_write.py` |
| E12 | `GET /api/ext/clinic` | 병원 정보 · 운영 시간 · 휴무 | 읽기(KOS) | 0.4.0 · DEC-012 D-14 · WORK-014 | `test_ext_clinic.py`(8) |
| E13 | `GET /api/ext/clinics/{clinicId}/staff` | 직원 목록 | 읽기(KOS) | 0.4.0 · DEC-012 D-15 / 0.4.7 D-48(email · realName · kosAccountId) · WORK-014 · 015 | `test_ext_clinic.py` |

공통 시험: `test_ext_auth.py`(18 — 키 · 제한 · 기록 · 열람 헤더) · `test_ext_docs.py`(3 — Swagger). 판 이력은 SPEC-008 「변경 이력」(`20-spec/spec-008-product-ext-api.md:89-105`).

### A2. 넘기는 값 — 통합표(A2 · A2-1 시점 · D2 Swagger 설명 · B1 DAY 대응)

읽는 법:

- **값의 출처**: KOS 경로는 `공개` / `내부` 와 경로 끝까지. cc 사본은 cc SQLite 표 이름(`cc:repository/db.py:1`). 출처 문자열 축약:
  - 「cc `reservation` 사본」 = 내부 `schedule/v2/queries/get-schedules-for-reservation`(그날 · 10초 캐시 · 화면 · 외부 요청이 올 때만 · `cc:kos/reservation_sync.py:263-304`) · 상세 때 내부 `schedule/v1/queries/get-schedule-detail` 다시 읽기(`cc:service/reservations.py:735-769`). 칸은 `reservation_fields`(`cc:kos/reservation_sync.py:117-140`).
  - 「cc `customer` 사본」 = 일정 · 조회 응답 안 `visitor` 를 그때 덮어쓴 값(`cc:kos/reservation_sync.py:143-151`).
- **출처 시점**: 그 값이 KOS 의 어느 업무 시점 기록인가(예약 지정 · 접수 · 상담 기록 · 작업 · 조회 시점의 지금 값 …).
- **D2**: Swagger 필드 설명의 판정 — `충분`(뜻 · 출처 시점 · 단위 · null 일 때) / `부족`(빠진 것) / `없음`. 경로 · 질의 · 헤더 행은 D2 집계에서 뺐다(라우터 `Header` · `Path` · `Query` 설명이 있다 — `cc:api/ext.py:44,68-73,343,433,487,495,504,549`).
- **B1**: `있음`(DAY 칼럼에 같은 시점 값) · `가공`(있는 칼럼에서 계산 · join · 타입 변환) · `없음` · `없음(시점 다름)`(같은 이름 칼럼이 있으나 다른 시점 · 다른 KOS 기록의 값) · `(묶음)` 객체 · 배열 칸 · `(계산)` 서버 계산 칸 · `-` 요청 칸 — 뒤 셋은 B1 집계에서 뺐다.
- **후보**: §A2-1 「뜻 불일치 후보」 번호.
- **쓰기 API 가 KOS 어디에 쓰나**: §B2 표.


#### E1. `GET /api/ext/menu`

스키마 필드 합 **34** · 표의 스키마 행 **34** · 빠진 필드 **0**(경로 · 질의 · 헤더 행은 따로).

| 필드 | 타입 | Swagger 설명 (그대로 · `schemas/ext.py:줄`) | 값의 출처 | 출처 시점 | D2 | D2 빠진 것 | DAY 대응(`origin/dev`) | B1 | 후보 |
|---|---|---|---|---|---|---|---|---|---|
| `header X-Api-Key` | `str` | (라우터 `api/ext.py` 의 Header · Path · Query 설명) | 연동처 키(env) | - | 충분 |  | DAY 에 연동처 키 없음(B5) | - |  |
| `syncedAt` | `str \| None` | 「메뉴 동기화가 마지막으로 **전부** 성공한 시각(ISO `+09:00`). 그 뒤 작업 하나가 실패해도 이 값은 그대로다. 한 번도 성공한 적 없으면 null」 (`:151`) | cc `sync_state('menu').last_ok_at`(`service/ext.py:201`) | 메뉴 동기화 전부 성공 시각 | 충분 |  | DAY 메뉴 회차의 「마지막 전부 성공」 칸 확인 안 됨(`external_ref.synced_at` 은 행마다) | 없음 |  |
| `categories` | `list[ExtCategory]` | 「지금 있는 카테고리(`order` 오름차순 → id). 메뉴가 비었으면(첫 동기화 전 · 실패) `[]`」 (`:154`) | cc `menu_*` 사본 ← 공개 `procedure-menu/open/...`(1시간 · 서버 시작 · `kos/menu_sync.py:24-31`) | - | 충분 |  | `product_category` | (묶음) |  |
| `categories[].id` | `str` | 「카테고리 KOS id(문자열)」 (`:142`) | KOS 카테고리 `id` | 메뉴 기준 정보 | 충분 |  | `external_ref`(entity=product_category).external_id | 가공 |  |
| `categories[].name` | `str` | 「카테고리 이름(KOS 기본 이름)」 (`:143`) | KOS 카테고리 `name` | 메뉴 기준 정보 | 충분 |  | `product_category.name`(내부 `procedure-menu/categories/...` · `sale_reads.py:50`) | 있음 |  |
| `categories[].order` | `int` | 「KOS 카테고리 순서(오름차순으로 준다)」 (`:144`) | KOS `order` | 메뉴 기준 정보 | 충분 |  | `product_category.sort_order` | 있음 |  |
| `categories[].translsMap` | `dict[str, Any]` | 「KOS 다국어 맵 그대로 · 없으면 `{}`」 (`:145`) | KOS `translsMap` 통째(cc `raw`) | 메뉴 기준 정보 | 부족 | 어떤 키·언어가 오는지(값 모양 예) 없음 | `product_category.name_translations` = `translsMap.name` 만(`mapper_menu.py:79`) | 가공 |  |
| `categories[].products` | `list[ExtProduct]` | 「이 카테고리에 속한 지금 있는 상품(KOS 상품 목록 순서). 한 상품이 카테고리 여럿에 걸리면 각 카테고리 아래에 다 나온다」 (`:146`) | cc `menu_*` 사본 ← 공개 `procedure-menu/open/...`(1시간 · 서버 시작 · `kos/menu_sync.py:24-31`) | - | 충분 |  | `product` + `product_category_link` | (묶음) |  |
| `products[].id` | `str` | 「상품 KOS id(문자열)」 (`:133`) | KOS 상품 `id` | 메뉴 기준 정보 | 충분 |  | `external_ref`(product) | 가공 |  |
| `products[].title` | `str` | 「상품 이름(KOS 기본 이름)」 (`:134`) | KOS 상품 `title` | 메뉴 기준 정보 | 충분 |  | `product.title` | 있음 |  |
| `products[].description` | `str` | 「상품 설명(KOS 값 · 없으면 빈 문자열)」 (`:135`) | KOS `description`(cc `raw`) | 메뉴 기준 정보 | 충분 |  | `product.description`(null 가능 — cc 는 빈 문자열) | 있음 |  |
| `products[].isEvent` | `bool` | 「이벤트 상품인가(KOS `isEvent`)」 (`:136`) | KOS `isEvent` | 메뉴 기준 정보 | 충분 |  | `product.is_event` | 있음 |  |
| `products[].translsMap` | `dict[str, Any]` | 「KOS 다국어 맵 그대로 · 없으면 `{}`」 (`:137`) | KOS `translsMap` | 메뉴 기준 정보 | 부족 | 모양 예 없음 | `product.translations`(`mapper_menu.py:172`) | 있음 |  |
| `products[].options` | `list[ExtOption]` | 「지금 있는 옵션(KOS 배열 순서 · 지운 옵션 제외)」 (`:138`) | cc `menu_*` 사본 ← 공개 `procedure-menu/open/...`(1시간 · 서버 시작 · `kos/menu_sync.py:24-31`) | - | 충분 |  | `product_option` | (묶음) |  |
| `options[].id` | `str` | 「옵션 KOS id(문자열) — 시술권 `optionId` 와 같은 체계」 (`:116`) | KOS 옵션 `id` | 메뉴 기준 정보 | 충분 |  | `external_ref`(product_option) | 가공 |  |
| `options[].type` | `Literal['SINGLE', 'GROUP', 'CONSULTATION']` | 「KOS 옵션 판별자 그대로 — `SINGLE`(시술 1개 · 옵션에 횟수 · 단위 · 시술) · `GROUP`(구성 여럿) · `CONSULTATION`(상담 · 가격 · 구성 없음)」 (`:117`) | KOS 옵션 판별자 | 메뉴 기준 정보 | 충분 |  | `product_option.type`(enum `OptionType` — 값 표기(대소문자) 일치 확인 안 됨) | 있음 |  |
| `options[].title` | `str` | 「옵션 이름(KOS 기본 이름)」 (`:120`) | KOS `title` | 메뉴 기준 정보 | 충분 |  | `product_option.title` | 있음 |  |
| `options[].description` | `str` | 「옵션 설명(KOS 값 · 없으면 빈 문자열)」 (`:121`) | KOS `description` | 메뉴 기준 정보 | 충분 |  | `product_option.description` | 있음 |  |
| `options[].translsMap` | `dict[str, Any]` | 「KOS 다국어 맵 그대로(`{칸: {translation: {언어: 값}}}`) · 없으면 `{}`」 (`:122`) | KOS `translsMap` | 메뉴 기준 정보 | 부족 | 모양 예 없음 | `product_option.translations` | 있음 |  |
| `options[].listPriceExVat` | `ExtMoney \| None` | 「옵션 정가 · **부가세 별도**(KOS `price.amount`). CONSULTATION 은 null」 (`:123`) | KOS 옵션 `price.amount`(+ currency) | 메뉴 기준 정보(정가) | 충분 |  | `product_option.price_amount` · `currency`(DAY 원천 = 내부 상품 응답 · cc = 공개) | 있음 |  |
| `options[].count` | `int \| None` | 「SINGLE 의 시술 횟수(KOS `count`). GROUP(구성마다 있음) · CONSULTATION 은 null」 (`:124`) | KOS `count` | 메뉴 기준 정보 | 충분 |  | `product_option.count` | 있음 |  |
| `options[].unit` | `ExtUnit \| None` | 「SINGLE 의 단위 = 이어진 진료항목의 `configuration.unit`. 진료항목이 이어지지 않았거나 단위가 없으면 null. GROUP · CONSULTATION 은 null」 (`:125`) | cc `menu_medical_service.unit_*` ← 진료항목 `configuration.unit` | 메뉴 기준 정보 | 충분 |  | `product_option.treatment_item_id` → `treatment_item.unit_type/unit_value` | 가공 |  |
| `options[].procedure` | `ExtProcedureRef \| None` | 「SINGLE 의 시술. GROUP · CONSULTATION 은 null」 (`:128`) | KOS 옵션 `procedure{id,name}`(cc `raw`) | 메뉴 기준 정보 | 충분 |  | `product_option.treatment_id` → `treatment` | 가공 |  |
| `options[].compositions` | `list[ExtComposition]` | 「GROUP 의 구성(KOS 배열 순서). SINGLE · CONSULTATION 은 `[]`」 (`:129`) | cc `menu_composition` | 메뉴 기준 정보 | 충분 |  | `product_option_composition` | (묶음) |  |
| `compositions[].title` | `str` | 「구성 이름(KOS 값)」 (`:106`) | KOS 구성 `title` | 메뉴 기준 정보 | 부족 | null 일 때 없음(타입은 str) | `product_option_composition.title`(null 허용) | 있음 |  |
| `compositions[].count` | `int \| None` | 「구성의 시술 횟수(KOS `count`)」 (`:107`) | KOS 구성 `count` | 메뉴 기준 정보 | 부족 | null 일 때 없음 | `product_option_composition.count` | 있음 |  |
| `compositions[].unit` | `ExtUnit \| None` | 「구성 단위 — KOS 구성 `unit` 그대로(`UnitType_UNKNOWN` 도 그대로). KOS 가 주지 않으면 null」 (`:108`) | KOS 구성 `unit` | 메뉴 기준 정보 | 충분 |  | `product_option_composition.unit_type/unit_value` | 있음 |  |
| `compositions[].listPriceExVat` | `ExtMoney \| None` | 「구성 정가 · **부가세 별도**(KOS `price.amount`). 한 GROUP 옵션의 구성 정가를 다 더하면 옵션 정가다」 (`:110`) | KOS 구성 `price.amount` | 메뉴 기준 정보 | 부족 | null 일 때 없음 | `product_option_composition.price_amount`(통화 칸 없음 — 옵션 `currency` 로) | 가공 |  |
| `compositions[].procedure` | `ExtProcedureRef \| None` | 「구성의 시술」 (`:112`) | KOS 구성 `procedure`(cc `raw`) | 메뉴 기준 정보 | 부족 | null 일 때 없음 | `product_option_composition.treatment_id` → `treatment` | 가공 |  |
| `*.value (ExtMoney)` | `int` | 「금액(원 단위 정수)」 (`:91`) | KOS `price.amount` 등 | - | 부족 | 부가세 포함 여부는 칸마다 다름(상위 칸 설명에 있음) | `*.price_amount`(정수) | 있음 |  |
| `*.currency (ExtMoney)` | `str` | 「통화 코드(ISO 4217 · 예 `KRW`) — KOS 값 그대로」 (`:92`) | KOS `currency` | - | 충분 |  | 옵션 `currency` 칸만(구성 · 시술권 · 카드에는 통화 칸 없음) | 가공 |  |
| `*.type (ExtUnit)` | `str` | 「단위 종류 — KOS 값 그대로(예 `SHOT` · `CC` · `UNIT` · `UnitType_UNKNOWN`)」 (`:96`) | KOS `unit.type` | - | 충분 |  | `unit_type`(DAY 작업 단위는 소문자 · `UnitType_UNKNOWN`→null `mapper.py:463` — 메뉴 단위 표기 확인 안 됨) | 가공 |  |
| `*.value (ExtUnit)` | `float \| None` | 「단위 값 — KOS 값 그대로. KOS 가 주지 않으면 null」 (`:97`) | KOS `unit.value` | - | 충분 |  | `unit_value`(Numeric) | 있음 |  |
| `*.id (ExtProcedureRef)` | `str` | 「시술 KOS id(문자열)」 (`:101`) | KOS 시술 `id` | 메뉴 기준 정보 | 충분 |  | `external_ref`(treatment) | 가공 |  |
| `*.name (ExtProcedureRef)` | `str` | 「시술 이름(KOS 값)」 (`:102`) | KOS 시술 `name` | 메뉴 기준 정보 | 충분 |  | `treatment.name` | 있음 |  |

#### E2. `POST /api/ext/customers/lookup`

스키마 필드 합 **27** · 표의 스키마 행 **27** · 빠진 필드 **0**(경로 · 질의 · 헤더 행은 따로).

| 필드 | 타입 | Swagger 설명 (그대로 · `schemas/ext.py:줄`) | 값의 출처 | 출처 시점 | D2 | D2 빠진 것 | DAY 대응(`origin/dev`) | B1 | 후보 |
|---|---|---|---|---|---|---|---|---|---|
| `header X-Ext-Staff-Id` | `str\|None` | (라우터 `api/ext.py` 의 Header · Path · Query 설명) | 연동처 신고값 | - | 충분 |  | - | - |  |
| `body.name` | `str \| None` | 「고객 이름 — `email` 과 함께 보낸다(`customerId` 와 섞지 않는다). 앞뒤 공백만 지워 KOS 이름 검색에 그대로 보낸다 — **KOS 에 등록된 띄어쓰기 그대로** 보내야 한다. 앞뒤 공백을 지우면 비는 값은 400」 (`:50`) | 요청 → 내부 `visitor/v2/queries/get-visitors`(이름 검색 · 요청마다 · `service/ext.py:258-285`) `visitorName` | - | 충분 |  | `customer.name` | - |  |
| `body.email` | `str \| None` | 「고객 이메일 — `name` 과 함께 보낸다. 앞뒤 공백을 지우고 소문자로 바꿔 KOS 고객 email 과 정확히 같은지만 본다(형식 검사 없음). 앞뒤 공백을 지우면 비는 값은 400」 (`:51`) | 요청 → KOS 고객 `email` 과 대조 | - | 충분 |  | `customer.email` 칸은 있으나 **동기화가 채우지 않음**(`emr/kos/mapper.py:300-329` 고객 매핑에 email 없음) | - |  |
| `body.customerId` | `StrictInt \| None` | 「ccc 고객 id(1 이상 정수 · 문자열 불가) — 이 칸 **하나만** 보낸다(`name` · `email` 과 섞지 않는다). 다른 응답(접수 목록 · 예약 상세 · 조회)의 `customerId` 와 같은 체계」 (`:52`) | cc `customer.id` → `kos_id` → 내부 `visitor/v2/queries/get-visitor {id}`(요청마다 · `service/reservations.py:598`) | - | 충분 |  | `customer.id`(uuid) | - |  |
| `customer` | `ExtCustomer` | 「찾은 고객(상담에 필요한 칸만 — 전화 · 생년월일 · 국적 · 여권 · 차트번호 · 이메일 없음)」 (`:195`) | 이름 갈래 내부 `visitor/v2/queries/get-visitors`(이름 검색 · 요청마다 · `service/ext.py:258-285`) / id 갈래 내부 `visitor/v2/queries/get-visitor {id}`(요청마다 · `service/reservations.py:598`) | 조회 시점(KOS 지금 값) | 충분 |  | `customer` | (묶음) |  |
| `customer.customerId` | `int` | 「ccc 고객 id(직원 API 와 같은 체계 · 정수). KOS 고객 id 는 내지 않는다」 (`:159`) | cc `customer.id`(찾은 고객을 사본에 upsert) | - | 충분 |  | `customer.id` — DAY id 는 uuid(`models/*` `uuid_pk()`) — cc 정수 id 와 타입이 다르다(계약 변경) | 가공 |  |
| `customer.name` | `str` | 「KOS 고객 이름」 (`:160`) | KOS visitor `name` | 조회 시점 | 충분 |  | `customer.name`(일정 응답 visitor · 10초 · 오늘 방문 고객만 갱신) | 있음 |  |
| `customer.isNew` | `bool` | 「KOS 신규 고객 여부(`isNew`)」 (`:161`) | KOS visitor `isNew` | 조회 시점(고객 현재 상태) | 부족 | 「신규」 판정 기준(KOS 정의) 없음 | 고객 칸 없음 — `visit.is_new` 는 **방문마다** 값(SPEC-000:360 · `mapper.py:597`) | 없음(시점 다름) | M4 |
| `customer.lastVisitDate` | `str \| None` | 「최근 방문일 — KOS `lastVisitedDateTimeUtc` 의 KST 날짜 `YYYY-MM-DD`. KOS 가 주지 않으면 null」 (`:162`) | KOS visitor `lastVisitedDateTimeUtc` | KOS 「최근 방문」(정의 확인 안 됨) | 부족 | 무엇을 방문으로 세는지(예약·접수·완료) 없음 | 칸 없음 — `visit` 에서 계산 가능하나 KOS 정의와 같은지 확인 안 됨 · 과거 방문은 수동 백필(어제까지) 범위만 | 가공 | M9 |
| `tickets` | `list[ExtTicket]` | 「남은 시술권 — **사용 가능 또는 사용 중 장이 1장 이상인 묶음** 한 줄씩 · KOS 순서(다 쓴 · 다 취소된 묶음은 빠진다). 없으면 `[]`(고객은 있는데 남은 시술권 없음)」 (`:197`) | 내부 `ticket/v1/queries/get-ticket-bundles {visitorId}`(요청마다 · `service/ext.py:315`) | 조회 시점 | 충분 |  | `ticket_bundle` · `ticket_set` · `ticket` | (묶음) |  |
| `tickets[].optionId` | `str` | 「시술권의 옵션 KOS id(산 시점 값). 지금 메뉴에 없는 옵션이어도 그대로 준다」 (`:167`) | 번들 `optionConfiguration.optionId` | 구매 시점 값 | 충분 |  | `ticket_bundle.purchase_item_id` → `purchase_item.product_option_id` → `external_ref` | 가공 |  |
| `tickets[].optionTitle` | `str` | 「시술권의 옵션 이름(산 시점 값 · 메뉴 이름으로 덮지 않는다)」 (`:168`) | 번들 `optionConfiguration.optionTitle` | 구매 시점 값 | 충분 |  | `ticket_bundle.title` = 번들 `title`(`mapper_purchase.py:299`) — 다른 KOS 칸. 같은 값인지 확인 안 됨 | 가공 |  |
| `tickets[].remainingCount` | `int` | 「남은 장수 — 묶음 안 `AVAILABLE` 시술권 수. `IN_USE`(쓰는 중) · `USED` · `CANCELED` 는 넣지 않는다」 (`:169`) | 번들 `ticketSets[].tickets[].status == AVAILABLE` 개수 | 조회 시점 | 충분 |  | `count(ticket.status='available')` | 가공 |  |
| `tickets[].inUseCount` | `int` | 「사용 중 장수 — 묶음 안 `IN_USE`(시술 작업에 붙어 아직 안 끝남) 시술권 수. 남은 장수(`remainingCount`)와 따로 센다」 (`:171`) | `status == IN_USE` 개수 | 조회 시점 | 충분 |  | `count(ticket.status='in_use')` | 가공 |  |
| `tickets[].totalCount` | `int` | 「묶음 안 시술권 장수 합(상태 무관 · 사용 중 장도 센다). GROUP 에서 한 세트를 다 쓰면 그 세트가 빠져 줄 수 있다」 (`:173`) | 번들 안 장 수 | 조회 시점 | 충분 |  | `count(ticket)`(삭제 표시 제외) | 가공 |  |
| `tickets[].purchasedDate` | `str \| None` | 「가장 이른 시술권 발행 시각(수납 완료 때)의 KST 날짜 `YYYY-MM-DD`. 없으면 null」 (`:175`) | min(장 `createdDateTimeUtc`) KST 날짜 | 시술권 발행(문서: 수납 완료 때) | 충분 |  | 장 · 번들의 KOS 생성 시각 칸 없음(`models/ticket.py`) · `purchase` 에도 구매 일시 칸 없음 | 없음 | M10 |
| `tickets[].bundlePrice` | `ExtMoney` | 「**KOS 묶음 가격 그대로**(`price`). 고객이 낸 돈이 아니다. 산 시점 값에서 출발하지만 GROUP 에서 세트를 다 쓰면 줄 수 있다. 부가세 포함 여부는 표기하지 않는다」 (`:176`) | 번들 `price` | KOS 묶음 가격(세트 소진 시 줄 수 있음) | 충분 |  | `ticket_bundle.price_amount` ← 번들 `price`(`mapper_purchase.py:300`) · 통화 칸 없음 | 있음 |  |
| `prepaidCards` | `list[ExtPrepaidCard] \| None` | 「선불카드(만료되지 않았고 잔액이 남은 카드 · KOS 순서). 없으면 `[]`. **선불카드 조회가 실패하면 null**(「카드 없음」 `[]` 과 다르다 · `partialErrors` 에 `prepaidCards`)」 (`:200`) | 공개 `purchase/open/prepaid-card/v1/queries/get-prepaid-card-summaries {visitorId, available:true}`(요청마다 · `service/ext.py:316`) | 조회 시점 | 충분 |  | `prepaid_card`(+ 공유 고객 `prepaid_card_customer`) | (묶음) |  |
| `prepaidCards[].title` | `str` | 「선불카드 이름(KOS 값)」 (`:187`) | 카드 `title` | - | 충분 |  | `prepaid_card.title` | 있음 |  |
| `prepaidCards[].issuedDate` | `str \| None` | 「발급일 — KOS `createdDateTimeUtc` 의 KST 날짜 `YYYY-MM-DD`. 없으면 null」 (`:188`) | 카드 `createdDateTimeUtc` | 발급 | 충분 |  | 카드 KOS 생성 시각 칸 없음(`models/prepaid_card.py`) | 없음 |  |
| `prepaidCards[].expiresAt` | `str \| None` | 「만료 일시 — KOS `expirationDateTimeUtc` 의 ISO `+09:00`. 없으면 null」 (`:189`) | 카드 `expirationDateTimeUtc` | - | 충분 |  | `prepaid_card.expires_at` | 있음 |  |
| `prepaidCards[].balance` | `ExtBalance` | 「현금 잔액 `{remaining, total}`(KOS `remainingBalance`)」 (`:190`) | 카드 `remainingBalance{balance,total}` | 조회 시점 | 충분 |  | `prepaid_card.balance_amount` = `remainingBalance.balance` 만 | (묶음) |  |
| `prepaidCards[].point` | `ExtBalance` | 「포인트 잔액 `{remaining, total}`(KOS `remainingPoint`)」 (`:191`) | 카드 `remainingPoint{balance,total}` | 조회 시점 | 충분 |  | `prepaid_card.point_balance` = `remainingPoint.balance` 만 | (묶음) |  |
| `*.remaining (ExtBalance)` | `ExtMoney \| None` | 「남은 금액(KOS `balance` · 금액 꼴). KOS 가 주지 않으면 null」 (`:182`) | `remaining*.balance` | 조회 시점 | 충분 |  | `balance_amount` / `point_balance` | 있음 |  |
| `*.total (ExtBalance)` | `ExtMoney \| None` | 「충전 총액(KOS `total` · 금액 꼴). KOS 가 주지 않으면 null」 (`:183`) | `remaining*.total` | 충전 총액 | 부족 | 총액이 누적 충전인지 현재 유효 충전인지 없음 | 칸 없음(`prepaid_card_ledger` 합으로 가능할 수 있으나 KOS `total` 과 같은지 확인 안 됨) | 없음 |  |
| `partialErrors` | `list[str]` | 「실패한 KOS 읽기 칸 이름 — 지금은 `prepaidCards` 하나뿐. 없으면 `[]`」 (`:203`) | 계산(선불카드 조회 실패) | - | 충분 |  | DAY DB 만 읽으면 의미가 바뀜(KOS 읽기 실패가 없음) | (계산) |  |
| `*.value (ExtMoney)` | `int` | 「금액(원 단위 정수)」 (`:91`) | 번들 `price.value` / 카드 `remaining*.balance.value` | - | 부족 | 부가세 포함 여부 표기 없음(시술권 설명에 「표기하지 않는다」) | `ticket_bundle.price_amount` · `prepaid_card.balance_amount` · `point_balance` | 있음 |  |
| `*.currency (ExtMoney)` | `str` | 「통화 코드(ISO 4217 · 예 `KRW`) — KOS 값 그대로」 (`:92`) | KOS `currency` | - | 충분 |  | 통화 칸 없음(번들 · 카드) | 없음 |  |

#### E3. `POST /api/ext/reservations`

스키마 필드 합 **6** · 표의 스키마 행 **6** · 빠진 필드 **0**(경로 · 질의 · 헤더 행은 따로).

| 필드 | 타입 | Swagger 설명 (그대로 · `schemas/ext.py:줄`) | 값의 출처 | 출처 시점 | D2 | D2 빠진 것 | DAY 대응(`origin/dev`) | B1 | 후보 |
|---|---|---|---|---|---|---|---|---|---|
| `body.name` | `str` | 「고객 이름(필수). 앞뒤 공백만 지워 KOS 이름 검색에 그대로 보낸다 — **KOS 에 등록된 띄어쓰기 그대로** 보내야 한다(KOS 검색은 가운데 공백을 그대로 견준다). 앞뒤 공백을 지우면 비는 값은 400」 (`:71`) | 고객 정하기 내부 `visitor/v2/queries/get-visitors`(이름 검색 · 요청마다 · `service/ext.py:258-285`) | - | 충분 |  | `customer.name` | - |  |
| `body.email` | `str` | 「고객 이메일(필수). 앞뒤 공백을 지우고 소문자로 바꿔 KOS 고객 email 과 정확히 같은지만 본다(형식 검사 없음). 앞뒤 공백을 지우면 비는 값은 400. 새 고객이면 이 이메일로 KOS 고객을 만든다」 (`:72`) | 대조 · 새 고객이면 KOS `create-visitor` 의 email | - | 충분 |  | `customer.email`(미동기화) | - |  |
| `body.start` | `str` | 「시작 시각 ISO-8601(오프셋이 없으면 KST 로 본다). 끝 = 시작 + 서버 기본 예약 그룹의 간격. ISO 가 아니면 400」 (`:73`) | → KOS 내부 `reserve` `occupiedResources[].reservationTime` | - | 충분 |  | `visit.reserved_start_at` · `visit_occupied_resource.start_at` | - |  |
| `body.memo` | `str \| None` | 「예약 메모(선택). 비었거나 공백뿐이면 보내지 않는다」 (`:76`) | → KOS `reservationMemo` | - | 충분 |  | `visit.reservation_notes` | - |  |
| `reservationId` | `int` | 「만든 예약의 ccc id」 (`:208`) | cc `reservation.id`(쓰기 뒤 다시 읽어 upsert) | - | 부족 | id 체계(사본 id · 다른 경로와 같은 체계)만 있고 KOS 반영 지연 언급 없음 | `visit.id` — DAY id 는 uuid(`models/*` `uuid_pk()`) — cc 정수 id 와 타입이 다르다(계약 변경) | 가공 |  |
| `customerId` | `int` | 「예약 고객의 ccc id(새 고객이면 새로 만든 행)」 (`:209`) | cc `customer.id` | - | 충분 |  | `customer.id`(uuid) | 가공 |  |

#### E4. `GET /api/ext/availability`

스키마 필드 합 **5** · 표의 스키마 행 **5** · 빠진 필드 **0**(경로 · 질의 · 헤더 행은 따로).

| 필드 | 타입 | Swagger 설명 (그대로 · `schemas/ext.py:줄`) | 값의 출처 | 출처 시점 | D2 | D2 빠진 것 | DAY 대응(`origin/dev`) | B1 | 후보 |
|---|---|---|---|---|---|---|---|---|---|
| `query date` | `str` | (라우터 `api/ext.py` 의 Header · Path · Query 설명) | 요청 | - | 충분 |  | - | - |  |
| `date` | `str` | 「요청 날짜 `YYYY-MM-DD`(KST)」 (`:228`) | 요청 그대로 | - | 충분 |  | (계산) | (계산) |  |
| `intervalMinutes` | `int` | 「기본 예약 그룹의 시간 간격(분). 칸 끝 = `start` + 이 값(예약의 끝과 같다)」 (`:229`) | cc `reservation_group.interval_minutes` ← 내부 `get-reservation-groups`(1시간) | 기준 정보 | 충분 |  | `reservation_group.interval_minutes` | 있음 |  |
| `slots` | `list[ExtSlot]` | 「예약 가능한 칸 — 시각 오름차순. 없으면 `[]`(휴무 요일 · 다 참 · 다 지남)」 (`:230`) | cc 그룹 `timetable` + 칸 정원 사본 | - | 충분 |  | `reservation_group_timetable` | (묶음) |  |
| `slots[].start` | `str` | 「칸 시작 ISO `+09:00`(초 단위). 이 값을 그대로 예약(`POST /api/ext/reservations`) `start` 로 보내면 된다」 (`:221`) | 계산(운영 구간 × 간격) | - | 충분 |  | `reservation_group_timetable` + `interval_minutes` 로 계산 | 가공 |  |
| `slots[].remainingSeats` | `int` | 「남은 자리 수(1 이상) — 기본 그룹의 켜진 구역마다 `max(0, 정원 − 예약 수)` 를 더한 값. 0 인 칸은 나오지 않는다」 (`:223`) | 공개 `schedule/open/v2/queries/get-reservation-slots-by-groups` `capacity`·`reservationCount`(요청마다 새로 읽음 · `service/ext.py:447`) | 요청 시점 | 충분 |  | 칸별 예약 수 칸 없음 · `reservation_group_capacity` 는 구역 정원 설정만 · DAY 일정은 오늘 창만 동기화(`services/emr_sync.py:111`)라 미래 날짜 예약 수를 셀 수 없음 | 없음 |  |

#### E5. `POST /api/ext/customers/visits`

스키마 필드 합 **7** · 표의 스키마 행 **7** · 빠진 필드 **0**(경로 · 질의 · 헤더 행은 따로).

| 필드 | 타입 | Swagger 설명 (그대로 · `schemas/ext.py:줄`) | 값의 출처 | 출처 시점 | D2 | D2 빠진 것 | DAY 대응(`origin/dev`) | B1 | 후보 |
|---|---|---|---|---|---|---|---|---|---|
| `body.name` | `str` | 「고객 이름(필수). 앞뒤 공백만 지워 KOS 이름 검색에 그대로 보낸다 — **KOS 에 등록된 띄어쓰기 그대로** 보내야 한다(KOS 검색은 가운데 공백을 그대로 견준다). 앞뒤 공백을 지우면 비는 값은 400」 (`:28`) | 고객 정하기 내부 `visitor/v2/queries/get-visitors`(이름 검색 · 요청마다 · `service/ext.py:258-285`) | - | 충분 |  | `customer.name` | - |  |
| `body.email` | `str` | 「고객 이메일(필수). 앞뒤 공백을 지우고 소문자로 바꿔 KOS 고객 email 과 정확히 같은지만 본다(형식 검사 없음). 앞뒤 공백을 지우면 비는 값은 400」 (`:29`) | KOS 고객 email 대조 | - | 충분 |  | `customer.email`(미동기화) | - |  |
| `visits` | `list[ExtVisit]` | 「지금보다 앞선 일정 — 최신 순 · 최대 50건 · 취소 · 부도 포함. 없으면 `[]`(고객은 있는데 지난 일정 없음)」 (`:244`) | 공개 `schedule/open/v1/queries/get-schedules-by-visitor {visitorId}`(요청마다) | - | 충분 |  | `visit`(과거 = 수동 백필 어제까지 + 운영 동기화가 본 날) | (묶음) |  |
| `visits[].date` | `str` | 「일정 시작의 KST 날짜 `YYYY-MM-DD`」 (`:234`) | 일정 시작(`occupiedResources[].reservationTime.startDateTimeUtc` 최소 · 없으면 `reservation.startDateTime`) | 예약 시각 | 충분 |  | min(`visit_occupied_resource.start_at`) · 없으면 `visit.reserved_start_at` | 가공 |  |
| `visits[].start` | `str` | 「일정 시작 ISO `+09:00`(묶음 시작 중 가장 이른 값)」 (`:235`) | 위와 같음 | 예약 시각 | 충분 |  | 위와 같음 | 가공 |  |
| `visits[].result` | `Literal['completed', 'noshow', 'canceled', 'other']` | 「결과 — KOS 예약 상태가 `COMPLETED` → `completed` · `NO_SHOW` → `noshow` · `CANCELED` → `canceled` · 그 밖(값 없음 포함) → `other`(직원 「이전 방문」 분류 그대로)」 (`:236`) | `reservation.status` → 분류 | 예약 상태 | 충분 |  | `visit.reservation_status` → 분류 | 가공 |  |
| `visits[].procedures` | `list[str]` | 「그 일정 작업의 이름(KOS 배열 순서 · 빈 값이면 빈 문자열). 「방 배정」 기타 작업은 뺀다. 작업이 없으면 `[]`」 (`:239`) | `tasks[].title`(「방 배정」 기타 제외) | 작업(접수 뒤) | 충분 |  | `visit_task.title`(`is_room_assign` 제외) | 가공 |  |

#### E6. `POST /api/ext/customers/reservations`

스키마 필드 합 **8** · 표의 스키마 행 **8** · 빠진 필드 **0**(경로 · 질의 · 헤더 행은 따로).

| 필드 | 타입 | Swagger 설명 (그대로 · `schemas/ext.py:줄`) | 값의 출처 | 출처 시점 | D2 | D2 빠진 것 | DAY 대응(`origin/dev`) | B1 | 후보 |
|---|---|---|---|---|---|---|---|---|---|
| `body.name` | `str` | 「고객 이름(필수). 앞뒤 공백만 지워 KOS 이름 검색에 그대로 보낸다 — **KOS 에 등록된 띄어쓰기 그대로** 보내야 한다(KOS 검색은 가운데 공백을 그대로 견준다). 앞뒤 공백을 지우면 비는 값은 400」 (`:28`) | 고객 정하기 내부 `visitor/v2/queries/get-visitors`(이름 검색 · 요청마다 · `service/ext.py:258-285`) | - | 충분 |  | `customer.name` | - |  |
| `body.email` | `str` | 「고객 이메일(필수). 앞뒤 공백을 지우고 소문자로 바꿔 KOS 고객 email 과 정확히 같은지만 본다(형식 검사 없음). 앞뒤 공백을 지우면 비는 값은 400」 (`:29`) | KOS 고객 email 대조 | - | 충분 |  | `customer.email`(미동기화) | - |  |
| `reservations` | `list[ExtCustomerReservation]` | 「오늘(KST) 0시 이후 일정 — 시작 오름차순 · 취소 · 부도 포함 · 개수 상한 없음. 없으면 `[]`」 (`:261`) | 공개 `schedule/open/v1/queries/get-schedules-by-visitor {visitorId}`(요청마다) 중 오늘 0시 이후 | - | 충분 |  | **DAY 는 오늘 하루 창만 동기화** — 내일 이후 일정 행이 없다(`services/emr_sync.py:111-115`) | (묶음) |  |
| `reservations[].reservationId` | `int \| None` | 「ccc 예약 id(예약 응답 `reservationId` 와 같은 체계). ccc 사본에 그 일정이 없으면 null — 외부 예약 API 로 만든 예약은 늘 id 가 있다」 (`:249`) | cc 사본에서 일정 KOS id 로 찾은 `reservation.id`(없으면 null) | - | 충분 |  | `visit.id`(uuid) — 미래 일정 행 없음 | 없음 |  |
| `reservations[].date` | `str` | 「일정 시작의 KST 날짜 `YYYY-MM-DD`」 (`:252`) | 일정 시작 | 예약 시각 | 충분 |  | 미래 일정 행 없음 | 없음 |  |
| `reservations[].start` | `str` | 「일정 시작 ISO `+09:00`」 (`:253`) | 일정 시작 | 예약 시각 | 충분 |  | 미래 일정 행 없음 | 없음 |  |
| `reservations[].end` | `str \| None` | 「첫 예약 묶음(시작 순 첫 번째)의 끝 ISO `+09:00`. 묶음이 없으면 null」 (`:254`) | 첫 묶음 `endDateTimeUtc` | 예약 시각 | 충분 |  | 미래 일정 행 없음 | 없음 |  |
| `reservations[].state` | `Literal['reserved', 'reception', 'consultation', 'procedure', 'home', 'canceled', 'noshow']` | 「상태 — 취소 · 부도가 먼저(`canceled` · `noshow`), 아니면 KOS 진행 단계로 정한다: `reserved`(예약 · 모르는 단계) · `reception`(접수) · `consultation`(상담 대기 · 상담) · `procedure`(시술 대기 · 시술) · `home`(시술 끝 · 귀가)」 (`:255`) | `reservation.status` + `flowStep` | 조회 시점 단계 | 충분 |  | 미래 일정 행 없음(오늘 행은 `reservation_status`+`flow_step` 가공) | 없음 |  |

#### E7. `GET /api/ext/reservations/board`

스키마 필드 합 **27** · 표의 스키마 행 **27** · 빠진 필드 **0**(경로 · 질의 · 헤더 행은 따로).

| 필드 | 타입 | Swagger 설명 (그대로 · `schemas/ext.py:줄`) | 값의 출처 | 출처 시점 | D2 | D2 빠진 것 | DAY 대응(`origin/dev`) | B1 | 후보 |
|---|---|---|---|---|---|---|---|---|---|
| `date` | `str` | 「오늘 KST `YYYY-MM-DD`」 (`:449`) | 서버 시계 | - | 충분 |  | (계산) | (계산) |  |
| `now` | `str` | 「서버 지금 시각 ISO `+09:00`」 (`:450`) | 서버 시계 | - | 충분 |  | (계산) | (계산) |  |
| `sync` | `ExtSync` | 「사본 신선도」 (`:451`) | cc `sync_state('resv:<날짜>')` | - | 충분 |  | - | (묶음) |  |
| `sync.lastOkAt` | `str \| None` | 「그날 KOS 날짜 조회가 마지막으로 성공한 시각 ISO `+09:00`(직원 예약 현황 `sync` 와 같은 값)」 (`:443`) | cc `sync_state` last_ok | 그날 날짜 조회 성공 | 충분 |  | DAY 일정 회차 마지막 성공 시각 칸 확인 안 됨(Redis 잠금 · `RunResult` 만 확인) | 없음 |  |
| `sync.lastError` | `str \| None` | 「마지막 날짜 조회 실패 문구 — 있으면 이 목록은 낡은 사본일 수 있다. 없으면 null」 (`:445`) | cc `sync_state` error | - | 충분 |  | 확인 안 됨 | 없음 |  |
| `partialErrors` | `list[str]` | 「일부 KOS 읽기가 실패했거나 아직 못 한 칸 이름 — 지금은 `consultationHistory`(아직 확인하지 못한 처음 상담 대기 시각이 있다)만 있다. 없으면 `[]`」 (`:452`) | 계산(이력 미확인) | - | 충분 |  | (계산) | (계산) |  |
| `reservations` | `list[ExtBoardRow]` | 「오늘 예약 — 예약 1건 = 1줄(묶음이 여럿이어도) · 상태로 거르지 않는다(취소 · 부도 · 귀가 포함) · 시작 오름차순 → id」 (`:455`) | cc `reservation` 사본 ← 내부 `schedule/v2/queries/get-schedules-for-reservation`(그날 · 10초 캐시 · 요청이 올 때) · 상세 때 내부 `schedule/v1/queries/get-schedule-detail` 다시 읽기 | - | 충분 |  | `visit`(오늘 · 10초 동기화) | (묶음) |  |
| `reservations[].reservationId` | `int` | 「ccc 예약 id — 예약 상세 · 오더 메모 · 상담 메모 경로의 id」 (`:421`) | cc `reservation.id` | - | 충분 |  | `visit.id` — DAY id 는 uuid(`models/*` `uuid_pk()`) — cc 정수 id 와 타입이 다르다(계약 변경) | 가공 |  |
| `reservations[].start` | `str \| None` | 「첫 묶음 시작 ISO `+09:00`. 묶음이 없으면 null」 (`:422`) | 사본 `resources[0].startAt` ← `occupiedResources` | 예약 시각 | 충분 |  | min(`visit_occupied_resource.start_at`) | 가공 |  |
| `reservations[].end` | `str \| None` | 「묶음 끝 중 가장 늦은 값 ISO `+09:00`. 묶음이 없으면 null」 (`:423`) | 사본 `resources` 끝 최대 | 예약 시각 | 충분 |  | max(`visit_occupied_resource.end_at`) | 가공 |  |
| `reservations[].state` | `_State` | 「2계층 상태(직원 판 그대로)」 (`:424`) | 사본 `status` + `flow_step` | 날짜 조회 시점 단계 | 충분 |  | `visit.reservation_status` + `visit.flow_step` | (묶음) |  |
| `*.main (_State)` | `str` | 「주 상태 — 직원 예약 현황 2계층 상태 그대로(`reserved` · `reception` · `consultation` · `procedure` · `home` · `canceled` · `noshow`)」 (`:282`) | `state_of(status, flowStep)`(`domain/reservation_rules.py:60`) | 날짜 조회 시점 | 충분 |  | 같은 계산 | 가공 |  |
| `*.sub (_State)` | `str \| None` | 「부 상태(직원 판 그대로 · 예 `waiting` · `doing`). 없으면 null」 (`:284`) | `FLOW_STATE` 표(`reservation_rules.py:13-22`) | 날짜 조회 시점 | 부족 | 값 목록이 예 둘(`waiting` · `doing`)뿐 — `done` 등 전체 목록 없음 | 같은 계산 | 가공 |  |
| `reservations[].customer` | `ExtBoardCustomer` | 「고객(직원 예약 현황 카드 고객 칸과 같은 값)」 (`:425`) | cc `customer` 사본 ← 일정 응답 안 `visitor`(`reservation_sync.py:143-151` upsert) — 마지막으로 그 고객이 든 KOS 응답을 받은 때 값 | - | 충분 |  | `customer` + `visit` | (묶음) |  |
| `customer.customerId` | `int \| None` | 「ccc 고객 id. 사본에 고객이 없으면 null」 (`:412`) | cc `customer.id` | - | 충분 |  | `customer.id`(uuid) | 가공 |  |
| `customer.name` | `str` | 「고객 이름(고객 사본)」 (`:413`) | cc `customer` 사본 ← 일정 응답 안 `visitor`(`reservation_sync.py:143-151` upsert) — 마지막으로 그 고객이 든 KOS 응답을 받은 때 값 | 사본 갱신 시점 | 부족 | 어느 시점 사본인지 없음 | `customer.name` | 있음 | M12 |
| `customer.phoneticName` | `str \| None` | 「발음 이름」 (`:414`) | cc `customer` 사본 ← 일정 응답 안 `visitor`(`reservation_sync.py:143-151` upsert) — 마지막으로 그 고객이 든 KOS 응답을 받은 때 값 | 사본 갱신 시점 | 부족 | null 일 때 · 원천 칸 이름 없음 | `customer.name_pronunciation` | 있음 |  |
| `customer.gender` | `str \| None` | 「성별(KOS 값)」 (`:415`) | cc `customer` 사본 ← 일정 응답 안 `visitor`(`reservation_sync.py:143-151` upsert) — 마지막으로 그 고객이 든 KOS 응답을 받은 때 값 `gender` | 사본 갱신 시점 | 부족 | 값 목록 없음 | `customer.gender`(DAY 는 `GENDERS` 표로 바꿔 저장 `mapper.py:311` — 표기 다름) | 가공 |  |
| `customer.nationality` | `str \| None` | 「국적(KOS 값)」 (`:416`) | cc `customer` 사본 ← 일정 응답 안 `visitor`(`reservation_sync.py:143-151` upsert) — 마지막으로 그 고객이 든 KOS 응답을 받은 때 값 `nationality` | 사본 갱신 시점 | 부족 | 형식(코드/이름) 없음 | `customer.nationality` | 있음 |  |
| `customer.isNew` | `bool` | 「KOS 신규 고객 여부」 (`:417`) | cc `customer` 사본 ← 일정 응답 안 `visitor`(`reservation_sync.py:143-151` upsert) — 마지막으로 그 고객이 든 KOS 응답을 받은 때 값 `isNew`(그 예약 일정의 visitor 가 아니라 마지막 upsert 값) | 사본 갱신 시점(애매) | 부족 | 이 예약 기준인지 고객 현재 기준인지 없음 | `visit.is_new`(이 방문 기준) | 있음 | M4 |
| `reservations[].receptionAt` | `str \| None` | 「접수 시각 ISO `+09:00`(KOS 접수 시각) — **귀가한 예약도 준다**. 접수 전이면 null. 접수 뒤인데 KOS 가 비워 준 일정도 null」 (`:426`) | 일정 `receptionDateTimeUtc` | 접수 | 충분 |  | `visit.reception_at` | 있음 |  |
| `reservations[].counselor` | `ExtStaffRef \| None` | 「**KOS 희망 상담사**(예약에 지정한 상담사 — 실제로 상담한 사람이 아니다 · 예약 상세 `reservation.counselor` 와 같은 값). 없으면 null」 (`:429`) | 일정 `reservation.counselor`(`kos/reservation_sync.py:131`) | **예약 · 접수 때 지정(희망 상담사)** | 충분 |  | `visit.requested_counselor_id` ← `reservation.counselor`(`mapper.py:572`) | 있음 | M1 |
| `counselor.staffId (ExtStaffRef)` | `int \| None` | 「ccc 직원 사본 id(직원 목록 `GET /api/ext/clinics/{clinicId}/staff` 와 같은 체계). 사본에 없는 KOS 계정이면 null」 (`:267`) | cc `staff.id`(KOS id 로 찾음) | - | 충분 |  | `staff.id`(uuid) | 가공 |  |
| `counselor.name (ExtStaffRef)` | `str` | 「이름(KOS 값)」 (`:269`) | 일정 안 사람 `name`(없으면 cc staff 이름) | 그 기록의 이름 | 부족 | 이름 원천(일정 안 이름 / 직원 사본) 없음 | `staff.name` | 있음 |  |
| `reservations[].roomTitle` | `str \| None` | 「관리실 — 작업에 붙은 방 중 **가장 늦게 배정된 방** 이름. 방이 없으면 null」 (`:432`) | 일정 `tasks[].room` 중 `roomAssignedDateTimeUtc` 최대(`reservation_sync.py:123`) | 방 배정(시술) | 충분 |  | `visit.room_id` → `room.title`(같은 규칙 `mapper.py:388-408`) | 가공 |  |
| `reservations[].consultation` | `bool` | 「상담 거침(CC 판정) — 접수 뒤이고 ① 지금 상담 대기 · 상담 ② CC 접수가 상담 대기로 끝남 ③ CC 「상담 추가」 중 하나. 취소 · 부도 · 접수 전이면 false. KOS 「상담 필요」 체크는 보지 않는다」 (`:433`) | CC 판정 = `flowStep` + cc `event_log`(`reception` · `consultation_add`)(`service/ext.py:730` · `reservation_rules.py:45`) | CC 조작 + 단계 | 충분 |  | `visit_flow_log` 의 CONSULTATION_WAITING/CONSULTATION 행으로 계산 가능 · cc 조작 사건(CC 접수 · 상담 추가)에 대응하는 DAY 조작 없음 | 가공 | M6 |
| `reservations[].firstConsultationWaitingAt` | `str \| None` | 「처음 상담 대기가 된 시각 ISO `+09:00` — KOS 단계 변경 이력에서 찾은 값. **`consultation` 과 따로 정한다** (`consultation = false` 여도 값이 있을 수 있다 — KOS 웹에서만 상담 대기를 지나간 일정). null = 접수 전 · 취소 · 부도 · 아직 못 찾음(이력에 없음 · 조회 실패 · 다음 단계 변화 전 · 요청당 상한 · 다른 요청이 확인 중 · 그날 끝까지 못 찾음)」 (`:436`) | 내부 `schedule/v1/queries/get-schedule-event-logs` `FlowStepChanged`→`CONSULTATION_WAITING` 최소 `raisedDateTimeUtc` → cc `consult_wait_first` | 처음 상담 대기 | 충분 |  | min(`visit_flow_log.changed_at`) where flow_step=CONSULTATION_WAITING — 값 = 10초 조회가 본 `flowStepUpdatedDateTimeUtc`(`sync_schedules.py:351-362`) · 조회 사이에 지나간 단계는 빠짐 | 가공 |  |

#### E8. `GET /api/ext/reservations/{reservationId}`

스키마 필드 합 **57** · 표의 스키마 행 **57** · 빠진 필드 **0**(경로 · 질의 · 헤더 행은 따로).

| 필드 | 타입 | Swagger 설명 (그대로 · `schemas/ext.py:줄`) | 값의 출처 | 출처 시점 | D2 | D2 빠진 것 | DAY 대응(`origin/dev`) | B1 | 후보 |
|---|---|---|---|---|---|---|---|---|---|
| `path reservationId` | `int` | (라우터 `api/ext.py` 의 Header · Path · Query 설명) | cc `reservation.id` | - | 충분 |  | `visit.id`(uuid) | - |  |
| `header X-Ext-Staff-Id` | `str\|None` | (라우터 `api/ext.py` 의 Header · Path · Query 설명) | 연동처 신고값 | - | 충분 |  | - | - |  |
| `reservationId` | `int` | 「ccc 예약 id」 (`:358`) | cc `reservation.id` | - | 충분 |  | `visit.id`(uuid) | 가공 |  |
| `day` | `str` | 「예약 날짜 KST `YYYY-MM-DD`」 (`:359`) | 사본 `day` | 예약 날짜 | 충분 |  | `visit.reserved_start_at` KST 날짜 | 가공 |  |
| `start` | `str \| None` | 「첫 묶음 시작 ISO `+09:00`. 묶음이 없으면 null」 (`:360`) | 사본 `resources[0].startAt` | 예약 시각 | 충분 |  | min(`visit_occupied_resource.start_at`) | 가공 |  |
| `end` | `str \| None` | 「묶음 끝 중 가장 늦은 값 ISO `+09:00`. 묶음이 없으면 null」 (`:361`) | 사본 `resources` 끝 최대 | 예약 시각 | 충분 |  | max(`visit_occupied_resource.end_at`) | 가공 |  |
| `state` | `_State` | 「2계층 상태(직원 판 그대로)」 (`:362`) | `state_of` (위 `_State` 행) | 상세 다시 읽기 시점 | 충분 |  | `visit.reservation_status` + `flow_step` | (묶음) |  |
| `customer` | `ExtDetailCustomer` | 「고객 기본 정보 + 나이 · 언어 · 고객 유입(전화 · 이메일 · 여권 · 주소 없음)」 (`:363`) | cc `customer` 사본 ← 일정 응답 안 `visitor`(`reservation_sync.py:143-151` upsert) — 마지막으로 그 고객이 든 KOS 응답을 받은 때 값 + 내부 `visitor/v2/queries/get-visitor {id}`(요청마다 · `service/reservations.py:598`) | 섞임(아래) | 충분 |  | `customer` | (묶음) | M12 |
| `customer.customerId` | `int \| None` | 「ccc 고객 id. 예약에 고객 사본이 없으면 null」 (`:289`) | cc `customer.id` | - | 충분 |  | `customer.id`(uuid) | 가공 |  |
| `customer.name` | `str` | 「고객 이름(고객 사본 · 직원 상세와 같은 값)」 (`:290`) | cc `customer` 사본 ← 일정 응답 안 `visitor`(`reservation_sync.py:143-151` upsert) — 마지막으로 그 고객이 든 KOS 응답을 받은 때 값 | 사본 갱신 시점 | 충분 |  | `customer.name` | 있음 | M12 |
| `customer.phoneticName` | `str \| None` | 「발음 이름(고객 사본)」 (`:291`) | cc `customer` 사본 ← 일정 응답 안 `visitor`(`reservation_sync.py:143-151` upsert) — 마지막으로 그 고객이 든 KOS 응답을 받은 때 값 | 사본 갱신 시점 | 부족 | null 일 때 없음 | `customer.name_pronunciation` | 있음 |  |
| `customer.gender` | `str \| None` | 「성별(KOS 값 그대로)」 (`:292`) | cc `customer` 사본 ← 일정 응답 안 `visitor`(`reservation_sync.py:143-151` upsert) — 마지막으로 그 고객이 든 KOS 응답을 받은 때 값 | 사본 갱신 시점 | 부족 | 값 목록 · null 없음 | `customer.gender`(표기 다름) | 가공 |  |
| `customer.nationality` | `str \| None` | 「국적(KOS 값 그대로)」 (`:293`) | cc `customer` 사본 ← 일정 응답 안 `visitor`(`reservation_sync.py:143-151` upsert) — 마지막으로 그 고객이 든 KOS 응답을 받은 때 값 | 사본 갱신 시점 | 부족 | 형식 · null 없음 | `customer.nationality` | 있음 |  |
| `customer.isNew` | `bool` | 「KOS 신규 고객 여부」 (`:294`) | cc `customer` 사본 ← 일정 응답 안 `visitor`(`reservation_sync.py:143-151` upsert) — 마지막으로 그 고객이 든 KOS 응답을 받은 때 값 `isNew` | 사본 갱신 시점(애매) | 부족 | 이 예약 기준인지 없음 | `visit.is_new` | 있음 | M4 |
| `customer.chartNumber` | `str \| None` | 「차트 번호(KOS 값)」 (`:295`) | cc `customer` 사본 ← 일정 응답 안 `visitor`(`reservation_sync.py:143-151` upsert) — 마지막으로 그 고객이 든 KOS 응답을 받은 때 값 `chartNumber` | 사본 갱신 시점 | 부족 | null 일 때 없음 | `customer.chart_number` | 있음 |  |
| `customer.age` | `int \| None` | 「그 예약 날짜 기준 나이(KOS 고객 생년월일). 고객 읽기 실패 · 생년월일 없음이면 null」 (`:296`) | 내부 `visitor/v2/queries/get-visitor {id}`(요청마다 · `service/reservations.py:598`) `dateOfBirth` + 예약 날짜 | 상세 요청 시점 | 충분 |  | `customer.birth_date`(일정 visitor `dateOfBirth` · `mapper.py:312`) + 예약 날짜 | 가공 |  |
| `customer.language` | `str \| None` | 「고객 언어 — KOS 고객 `language` 값 그대로. 고객 읽기 실패 · 값 없음이면 null」 (`:297`) | 내부 `visitor/v2/queries/get-visitor {id}`(요청마다 · `service/reservations.py:598`) `language` | 상세 요청 시점 | 충분 |  | `customer.language` 칸은 있으나 동기화가 채우지 않음(`mapper.py:300-329`) | 없음 |  |
| `customer.funnel` | `ExtFunnel \| None` | 「고객 유입(KOS 고객 `visitorFunnel`). 없음 · 고객 읽기 실패면 null」 (`:298`) | 내부 `visitor/v2/queries/get-visitor {id}`(요청마다 · `service/reservations.py:598`) `visitorFunnel` + cc `funnel_code` | 고객 유입(고객 등록) | 충분 |  | `customer.funnel_id` · `funnel_detail` 칸은 있으나 동기화가 채우지 않음 | (묶음) |  |
| `*.name (ExtFunnel)` | `str \| None` | 「유입 이름(KOS 유입 코드 이름). 없으면 null」 (`:273`) | 고객: `visitorFunnel.funnelId`→cc `funnel_code.name` / 예약: `reservation.funnel.funnel.name` | 고객 유입 / 예약 유입 | 충분 |  | 고객: 없음(미동기화) / 예약: `visit.funnel_id`→`funnel.name` | 가공 |  |
| `*.detail (ExtFunnel)` | `str \| None` | 「유입 상세 글(KOS 값). 없으면 null」 (`:274`) | 고객: `visitorFunnel.funnelDetail` / 예약: `reservation.funnel.funnelDetail` | 고객 유입 / 예약 유입 | 충분 |  | 고객: 없음 / 예약: `visit.funnel_detail` | 가공 |  |
| `reservation` | `ExtDetailReservation` | 「예약 칸」 (`:364`) | cc `reservation` 사본 ← 내부 `schedule/v2/queries/get-schedules-for-reservation`(그날 · 10초 캐시 · 요청이 올 때) · 상세 때 내부 `schedule/v1/queries/get-schedule-detail` 다시 읽기 | - | 충분 |  | `visit` | (묶음) |  |
| `reservation.memo` | `str \| None` | 「예약 메모(KOS `reservationMemo`). **오더 메모 · 상담 메모와 다른 칸**이다」 (`:311`) | 일정 `reservation.reservationMemo` | 예약 | 충분 |  | `visit.reservation_notes` | 있음 |  |
| `reservation.desiredDischargeAt` | `str \| None` | 「귀가 희망 시각 ISO `+09:00`. 없으면 null」 (`:312`) | `reservation.desiredDischargeDateTimeUtc` | 예약 | 충분 |  | `visit.desired_discharge_at` | 있음 |  |
| `reservation.funnel` | `ExtFunnel \| None` | 「예약 유입. 없으면 null」 (`:313`) | `reservation.funnel` | 예약 | 충분 |  | `visit.funnel_id` · `funnel_detail` | (묶음) |  |
| `reservation.counselor` | `ExtStaffRef \| None` | 「**KOS 희망 상담사**(예약에 지정한 상담사 — 실제로 상담한 사람이 아니다). 없으면 null」 (`:314`) | 일정 `reservation.counselor` | **예약 · 접수 때 지정(희망 상담사)** | 충분 |  | `visit.requested_counselor_id` | 있음 | M1 |
| `reservation.orderMemo` | `str \| None` | 「지금 오더 메모(KOS 일정 `orderMemo` 그대로 · 빈 문자열 그대로) — 오더 메모 쓰기가 통째로 바꾸는 칸. null = KOS 일정 읽기 실패(`partialErrors` 에 `schedule`)」 (`:316`) | 내부 `get-schedule-detail` `orderMemo`(요청마다) | 오더(시술 지시) — 지금 값 | 충분 |  | `visit.procedure_order_note` ← 일정 `orderMemo`(`mapper.py:598`) · 오늘 일정만 10초 | 있음 |  |
| `reservation.consultationMemo` | `str \| None` | 「지금 상담 메모(= 차트 메모 · KOS 일정 `consultation.consultationMemo` 그대로) — 상담 메모 쓰기가 통째로 바꾸는 칸. null = KOS 일정 읽기 실패 · 상담 정보 없음」 (`:319`) | 내부 `get-schedule-detail` `consultation.consultationMemo`(`service/ext.py:634`) | 상담 정보(일정 단일 `consultation`) — 지금 값 | 충분 |  | `consultation.consultation_note` ← 일정 `consultations[].content.text`(`mapper.py:507` · SPEC-000:535) — **다른 KOS 칸** | 없음(시점 다름) | M3 |
| `reservation.requestedDoctor` | `ExtStaffRef \| None` | 「희망 의사(KOS 예약 `doctor`). 없음 · KOS 일정 읽기 실패면 null」 (`:322`) | 내부 `get-schedule-detail` `reservation.doctor` | 예약 때 지정(희망 의사) | 충분 |  | `visit.requested_doctor_id` ← `reservation.doctor`(`mapper.py:575`) | 있음 |  |
| `reservation.requestedProcedures` | `list[ExtRequestedProcedure] \| None` | 「희망 시술(KOS 예약 `requestedProcedures` 순서). `[]` = 희망 시술 없음 · null = KOS 일정 읽기 실패」 (`:323`) | `reservation.requestedProcedures[]` | 예약 때 지정 | 충분 |  | `visit_requested_procedure` | (묶음) |  |
| `requestedProcedures[].type` | `str` | 「`OPTION`(상품 옵션) · `TICKET`(시술권) — KOS 값 그대로」 (`:302`) | `type` | 예약 | 충분 |  | `visit_requested_procedure.kind`(enum) | 있음 |  |
| `requestedProcedures[].optionId` | `str \| None` | 「`OPTION` 의 옵션 KOS id(메뉴 `options[].id` 와 같은 체계). `TICKET` 이면 null」 (`:303`) | `optionConfiguration.optionId` | 예약 | 충분 |  | `product_option_id` 칸은 있으나 매퍼가 KOS 옵션 id 를 두지 않음(`mapper.py:335`) | 없음 |  |
| `requestedProcedures[].optionTitle` | `str \| None` | 「`OPTION` 의 옵션 이름. `TICKET` 이면 null」 (`:304`) | `optionConfiguration.optionTitle` | 예약 | 충분 |  | `visit_requested_procedure.option_title`(OPTION) | 있음 |  |
| `requestedProcedures[].productTitle` | `str \| None` | 「`OPTION` 의 상품 이름. `TICKET` 이면 null」 (`:305`) | `optionConfiguration.productTitle` | 예약 | 충분 |  | `visit_requested_procedure.product_title`(TICKET 이면 `ticketConfiguration.productTitle` 도 넣음 — cc 는 null) | 가공 |  |
| `requestedProcedures[].ticketId` | `str \| None` | 「`TICKET` 의 시술권 KOS id. `OPTION` 이면 null」 (`:306`) | `ticketConfiguration.ticketId` | 예약 | 충분 |  | 칸 없음 | 없음 |  |
| `requestedProcedures[].ticketTitle` | `str \| None` | 「`TICKET` 의 시술권 이름. `OPTION` 이면 null」 (`:307`) | `ticketConfiguration.ticketTitle` | 예약 | 충분 |  | `visit_requested_procedure.option_title`(TICKET 일 때 · `mapper.py:343-346`) | 가공 |  |
| `health` | `ExtHealth` | 「문진(직원 상세 `health` 와 같은 모양 · 같은 계산)」 (`:365`) | 공개 `visitor/open/v1/queries/get-visitor-questionnaire` + `get-questionnaire-submit` + cc 웹 문진 | 문진 제출 | 충분 |  | `questionnaire_history` 표는 있으나 KOS 동기화가 쓰지 않음(쓰는 코드 0 — `git grep` 결과 모델 · 식별자뿐) | (묶음) |  |
| `health.state` | `str` | 「`ok`(제출본 있음) · `none`(제출 안 함) · `error`(문진 읽기 실패 — `partialErrors` 에 `questionnaire`) — 직원 상세 `health` 와 같은 계산」 (`:329`) | 계산 | 문진 | 충분 |  | 원천 없음 | 없음 |  |
| `health.submittedAt` | `str \| None` | 「제출 시각 ISO `+09:00`. 없으면 null」 (`:331`) | 제출본 `createdDateTimeUtc` | 문진 제출 | 충분 |  | `questionnaire_history.submitted_at`(미동기화) | 없음 |  |
| `health.needCount` | `int` | 「확인이 필요한 답 수(직원 상세와 같은 규칙)」 (`:332`) | 계산(직원 규칙) | 문진 | 부족 | 「확인이 필요한 답」 규칙 내용 없음(직원 상세 참조만) | 원천 없음 | 없음 |  |
| `health.items` | `list[dict[str, Any]]` | 「「건강 정보」 질문 × 답 — 직원 상세 `health.items` 와 같은 모양」 (`:333`) | 질문 × 답(`health_items`) | 문진 | 부족 | 원소 모양이 `dict[str, Any]` — 칸 설명 없음(직원 상세 참조만) | 원천 없음 | 없음 |  |
| `previousVisits` | `list[ExtPrevVisit] \| None` | 「이전 방문(최신 순 · 그 예약 날짜와 같은 날 일정은 뺀다) — **예약 메모 · 상담 메모 · 의사 이름 · 상담자를 준다**(과거 시술 경로와 다르다). null = 이전 방문 조회 실패(`partialErrors` 에 `previousVisits`)」 (`:366`) | 공개 `schedule/open/v1/queries/get-schedules-by-visitor {visitorId}`(요청마다) 중 그 예약 날짜 제외 | 과거 방문 | 충분 |  | `visit`(과거 = 수동 백필 어제까지) | (묶음) |  |
| `previousVisits[].date` | `str` | 「일정 시작의 KST 날짜 `YYYY-MM-DD`」 (`:343`) | 일정 시작 | 예약 시각 | 충분 |  | min(`visit_occupied_resource.start_at`) | 가공 |  |
| `previousVisits[].start` | `str` | 「일정 시작 ISO `+09:00`」 (`:344`) | 일정 시작 | 예약 시각 | 충분 |  | 위와 같음 | 가공 |  |
| `previousVisits[].result` | `str` | 「결과 — `completed` · `noshow` · `canceled` · `other`(직원 「이전 방문」 분류)」 (`:345`) | `reservation.status` 분류 | 예약 상태 | 충분 |  | `visit.reservation_status` 분류 | 가공 |  |
| `previousVisits[].resultRaw` | `str \| None` | 「KOS 예약 상태 값 그대로」 (`:346`) | `reservation.status` | 예약 상태 | 충분 |  | `visit.reservation_status`(DAY enum 소문자 표기 가능성 — 값 표기 확인 안 됨) | 가공 |  |
| `previousVisits[].zoneTitle` | `str \| None` | 「구역 이름」 (`:347`) | 일정 `zone.title` | 접수 구역 | 부족 | 어느 구역(접수 / 지금 위치)인지 없음 | `visit.reception_zone_id` → `zone.title`(`zone` = 일정 `zone` · `mapper.py:593`) | 가공 |  |
| `previousVisits[].groupTitle` | `str \| None` | 「예약 그룹 이름(사본에 그 그룹이 있을 때)」 (`:348`) | 첫 묶음 그룹 → cc 그룹 사본 `title` | 예약 | 충분 |  | `visit_occupied_resource.reservation_group_id` → `reservation_group.title` | 가공 |  |
| `previousVisits[].reservationMemo` | `str \| None` | 「그 방문의 예약 메모(KOS 값). 없으면 null」 (`:349`) | `reservation.reservationMemo` | 예약 | 충분 |  | `visit.reservation_notes` | 있음 |  |
| `previousVisits[].consultationMemo` | `str \| None` | 「그 방문의 상담 메모(KOS 값). 없으면 null」 (`:350`) | 일정 `consultation.consultationMemo` | 상담 정보(단일) | 부족 | 「상담 메모 = 차트 메모」 등 뜻 설명 없음(KOS 값만) | `consultation.consultation_note` ← `consultations[].content.text` — 다른 KOS 칸 | 없음(시점 다름) | M3 |
| `previousVisits[].procedures` | `list[ExtPrevProcedure]` | 「그 방문의 작업(의사 이름 포함)」 (`:351`) | `tasks[]`(방 배정 제외) | 작업 | 충분 |  | `visit_task` | (묶음) |  |
| `procedures[].title` | `str` | 「작업 이름(KOS 값 · 「방 배정」 기타 작업은 뺀다)」 (`:337`) | `tasks[].title` | 작업 | 충분 |  | `visit_task.title` | 있음 |  |
| `procedures[].status` | `str \| None` | 「작업 상태(KOS 값 그대로)」 (`:338`) | `tasks[].status` | 작업 상태(조회 시점) | 부족 | 값 목록 없음 | `visit_task.status`(DAY enum — 표기 다름) | 가공 |  |
| `procedures[].doctors` | `list[str]` | 「그 작업의 의사 이름(KOS 순서)」 (`:339`) | `tasks[].doctors[].name` | **시술(작업) 의사** | 충분 |  | `visit_task_staff`(role=doctor) → `staff.name` | 가공 |  |
| `previousVisits[].counselors` | `list[ExtStaffRef]` | 「그 방문의 상담자 — KOS 일정 `consultations[].counselors[]`(나온 차례 · 같은 사람은 한 번). 그것이 비면 `consultation.counselor` 하나. 둘 다 없으면 `[]`」 (`:352`) | `consultations[].counselors[]` · 비면 `consultation.counselor`(`service/ext.py:576-589`) | **상담 기록(상담 차트) · 없으면 단일 상담 정보** | 충분 |  | `consultation.counselor_id` ← `consultations[].counselors` **1명일 때만**(`mapper.py:491-505`) | 가공 | M2 |
| `partialErrors` | `list[str]` | 「실패한 KOS 읽기 — `schedule`(희망 시술 · 희망 의사 · 지금 메모 둘이 null) · `visitor`(나이 · 언어 · 고객 유입 null) · `questionnaire`(`health.state = error`) · `previousVisits`(null). 없으면 `[]`」 (`:369`) | 계산 | - | 충분 |  | (계산) | (계산) |  |
| `*.main (_State)` | `str` | 「주 상태 — 직원 예약 현황 2계층 상태 그대로(`reserved` · `reception` · `consultation` · `procedure` · `home` · `canceled` · `noshow`)」 (`:282`) | `state_of`(상세 다시 읽기 뒤 사본) | 상세 요청 시점 | 충분 |  | `visit.reservation_status` + `flow_step` | 가공 |  |
| `*.sub (_State)` | `str \| None` | 「부 상태(직원 판 그대로 · 예 `waiting` · `doing`). 없으면 null」 (`:284`) | `FLOW_STATE` | 상세 요청 시점 | 부족 | 값 전체 목록 없음 | 같은 계산 | 가공 |  |
| `counselor/requestedDoctor/counselors[].staffId (ExtStaffRef)` | `int \| None` | 「ccc 직원 사본 id(직원 목록 `GET /api/ext/clinics/{clinicId}/staff` 와 같은 체계). 사본에 없는 KOS 계정이면 null」 (`:267`) | cc `staff.id` | - | 충분 |  | `staff.id`(uuid) | 가공 |  |
| `counselor/requestedDoctor/counselors[].name (ExtStaffRef)` | `str` | 「이름(KOS 값)」 (`:269`) | 그 기록 안 사람 `name`(희망 상담사 = `reservation.counselor` · 희망 의사 = `reservation.doctor` · 상담자 = `consultations[].counselors[]`) | **쓰인 자리마다 다름** | 부족 | 같은 클래스가 세 시점(예약 지정 상담사 · 예약 지정 의사 · 상담 기록 상담자)에 쓰인다 — 클래스 설명에는 시점이 없고 상위 칸 설명에만 있다 | `staff.name` | 있음 | M1 |

#### E9. `PUT /api/ext/customers/{customerId}/language`

스키마 필드 합 **2** · 표의 스키마 행 **2** · 빠진 필드 **0**(경로 · 질의 · 헤더 행은 따로).

| 필드 | 타입 | Swagger 설명 (그대로 · `schemas/ext.py:줄`) | 값의 출처 | 출처 시점 | D2 | D2 빠진 것 | DAY 대응(`origin/dev`) | B1 | 후보 |
|---|---|---|---|---|---|---|---|---|---|
| `path customerId` | `int` | (라우터 `api/ext.py` 의 Header · Path · Query 설명) | cc 사본 id | - | 충분 |  | uuid | - |  |
| `header X-Ext-Staff-Id` | `str\|None` | (라우터 `api/ext.py` 의 Header · Path · Query 설명) | 연동처 신고값 | - | 충분 |  | - | - |  |
| `body.language` | `str` | 「고객 언어 — KOS 언어 값 그대로(꼴 검사 없이 KOS 에 보낸다 · 예 2자 · 5자 코드). 앞뒤 공백을 지운다. **빈 문자열 = 비움** · null 은 400」 (`:376`) | → 내부 `visitor/v2/commands/update-visitor-personal-information`(다시 읽은 개인정보 묶음 전체 + language) | - | 충분 |  | `customer.language`(미동기화) | - |  |
| `ok` | `bool` | 「늘 `true` — KOS 쓰기가 성공했다(또는 고객 언어가 이미 같은 값이라 쓰지 않았다)」 (`:278`) | 상수 true | - | 충분 |  | (계산) | (계산) |  |

#### E10. `PUT /api/ext/reservations/{reservationId}/order-memo`

스키마 필드 합 **2** · 표의 스키마 행 **2** · 빠진 필드 **0**(경로 · 질의 · 헤더 행은 따로).

| 필드 | 타입 | Swagger 설명 (그대로 · `schemas/ext.py:줄`) | 값의 출처 | 출처 시점 | D2 | D2 빠진 것 | DAY 대응(`origin/dev`) | B1 | 후보 |
|---|---|---|---|---|---|---|---|---|---|
| `path reservationId` | `int` | (라우터 `api/ext.py` 의 Header · Path · Query 설명) | cc 사본 id | - | 충분 |  | uuid | - |  |
| `header X-Ext-Staff-Id` | `str\|None` | (라우터 `api/ext.py` 의 Header · Path · Query 설명) | 연동처 신고값 | - | 충분 |  | - | - |  |
| `body.orderMemo` | `str` | 「오더 메모 글 전체 — **통째로 바꾼다**(일정 하나에 글 하나). 지금 값은 예약 상세 `reservation.orderMemo`. 빈 문자열은 그대로 보낸다(비움)」 (`:387`) | → 내부 `schedule/v1/commands/change-order-memo {scheduleId, orderMemo}` | - | 충분 |  | `visit.procedure_order_note` | - |  |
| `ok` | `bool` | 「늘 `true` — KOS 쓰기가 성공했다(또는 고객 언어가 이미 같은 값이라 쓰지 않았다)」 (`:278`) | 상수 true | - | 충분 |  | (계산) | (계산) |  |

#### E11. `PUT /api/ext/reservations/{reservationId}/consultation-memo`

스키마 필드 합 **2** · 표의 스키마 행 **2** · 빠진 필드 **0**(경로 · 질의 · 헤더 행은 따로).

| 필드 | 타입 | Swagger 설명 (그대로 · `schemas/ext.py:줄`) | 값의 출처 | 출처 시점 | D2 | D2 빠진 것 | DAY 대응(`origin/dev`) | B1 | 후보 |
|---|---|---|---|---|---|---|---|---|---|
| `path reservationId` | `int` | (라우터 `api/ext.py` 의 Header · Path · Query 설명) | cc 사본 id | - | 충분 |  | uuid | - |  |
| `header X-Ext-Staff-Id` | `str\|None` | (라우터 `api/ext.py` 의 Header · Path · Query 설명) | 연동처 신고값 | - | 충분 |  | - | - |  |
| `body.consultationMemo` | `str` | 「상담 메모(= 차트 메모) 글 전체 — **통째로 바꾼다**. 지금 값은 예약 상세 `reservation.consultationMemo`. **빈 값은 받지 않는다** — 앞뒤 공백을 지우면 비는 값은 `400`(KOS 가 상담 메모를 비우지 못한다 · 빈 값을 보내면 200 인데 그대로 남는다). 비우는 쓰기는 없다(오더 메모와 다르다)」 (`:396`) | → 공개 `schedule/open/v1/commands/update-schedule-consultation-info {scheduleId, consultationMemo}` | - | 충분 |  | `consultation.consultation_note` 는 다른 KOS 칸(M3) | - | M3 |
| `ok` | `bool` | 「늘 `true` — KOS 쓰기가 성공했다(또는 고객 언어가 이미 같은 값이라 쓰지 않았다)」 (`:278`) | 상수 true | - | 충분 |  | (계산) | (계산) |  |

#### E12. `GET /api/ext/clinic`

스키마 필드 합 **16** · 표의 스키마 행 **16** · 빠진 필드 **0**(경로 · 질의 · 헤더 행은 따로).

| 필드 | 타입 | Swagger 설명 (그대로 · `schemas/ext.py:줄`) | 값의 출처 | 출처 시점 | D2 | D2 빠진 것 | DAY 대응(`origin/dev`) | B1 | 후보 |
|---|---|---|---|---|---|---|---|---|---|
| `clinicId` | `int` | 「CC 고정 값 `1` — CC 서버 하나 = KOS 병원 하나. 직원 목록 경로(`/api/ext/clinics/{clinicId}/staff`)에 쓴다. **전역 유일하지 않다**(CC 서버 여럿을 모으면 겹친다)」 (`:480`) | 상수 1(`service/ext.py:80`) | - | 충분 |  | `hospital.id`(uuid · 병원 여럿) | 가공 |  |
| `name` | `str \| None` | 「병원 이름(KOS 값 · 비면 null)」 (`:483`) | 내부 `v1/hospital/queries/get-hospital` `hospitalName`(요청마다) | KOS 병원 설정 | 충분 |  | `hospital.name` 은 DAY 가 정한 이름 — KOS 에서 받지 않음 | 없음(시점 다름) |  |
| `phone` | `str \| None` | 「대표 전화(KOS 값 그대로 · 국가 번호를 붙이지 않는다 · 비면 null)」 (`:484`) | `hospitalPhoneNumber` | KOS 병원 설정 | 충분 |  | 칸 없음 | 없음 |  |
| `address` | `ExtAddress \| None` | 「주소. 세 칸이 모두 비면 null」 (`:485`) | `addressContract` | KOS 병원 설정 | 충분 |  | 칸 없음 | (묶음) |  |
| `address.address` | `str \| None` | 「주소(KOS 값 · 비면 null)」 (`:461`) | `addressContract.address` | KOS 병원 설정 | 충분 |  | 칸 없음 | 없음 |  |
| `address.detailed` | `str \| None` | 「상세 주소(KOS 값 · 비면 null)」 (`:462`) | `addressContract.detailedAddress` | KOS 병원 설정 | 충분 |  | 칸 없음 | 없음 |  |
| `address.zipCode` | `str \| None` | 「우편번호(KOS 값 · 비면 null)」 (`:463`) | `addressContract.zipCode` | KOS 병원 설정 | 충분 |  | 칸 없음 | 없음 |  |
| `operatingHours` | `dict[str, ExtDayHours]` | 「**병원 기본 운영 시간**(예약 그룹별 시간표가 아니다) — 요일 키 `monday` … `sunday`」 (`:486`) | 내부 `schedule/default-operation-time/v1/queries/get-default-operation-timetable` | 병원 기본 운영 시간 | 충분 |  | `reservation_group_timetable` 은 **예약 그룹별** 시간표 — 병원 기본 시간표 아님 | (묶음) |  |
| `*.enabled (ExtDayHours)` | `bool` | 「그 요일 운영하나(시작 · 끝이 다 있을 때만 true)」 (`:467`) | 운영 시간표 | 병원 기본 | 충분 |  | 병원 기본 칸 없음 | 없음(시점 다름) |  |
| `*.start (ExtDayHours)` | `str \| None` | 「운영 시작 KST `HH:MM`」 (`:468`) | 운영 시간표 | 병원 기본 | 부족 | null 일 때 없음 | 병원 기본 칸 없음 | 없음(시점 다름) |  |
| `*.end (ExtDayHours)` | `str \| None` | 「운영 끝 KST `HH:MM`」 (`:469`) | 운영 시간표 | 병원 기본 | 부족 | null 일 때 없음 | 병원 기본 칸 없음 | 없음(시점 다름) |  |
| `*.breakStart (ExtDayHours)` | `str \| None` | 「쉬는 시간 시작 KST `HH:MM`. 없으면 null」 (`:470`) | 운영 시간표 | 병원 기본 | 충분 |  | 병원 기본 칸 없음 | 없음(시점 다름) |  |
| `*.breakEnd (ExtDayHours)` | `str \| None` | 「쉬는 시간 끝 KST `HH:MM`. 없으면 null」 (`:471`) | 운영 시간표 | 병원 기본 | 충분 |  | 병원 기본 칸 없음 | 없음(시점 다름) |  |
| `daysOff` | `list[ExtDayOff]` | 「병원 기본 휴무 — 오늘(KST) ~ 오늘 + 90일 · KOS 차례. 없으면 `[]`」 (`:488`) | 내부 `.../get-default-days-off`(오늘~+90일) | 병원 기본 휴무 | 충분 |  | 칸 없음 | (묶음) |  |
| `daysOff[].startDate` | `str` | 「휴무 첫날 KST `YYYY-MM-DD`」 (`:475`) | `startDateTime` | 병원 기본 휴무 | 충분 |  | 칸 없음 | 없음 |  |
| `daysOff[].endDate` | `str` | 「휴무 마지막 날 KST `YYYY-MM-DD`(하루 휴무면 `startDate` 와 같다 · 여러 날 휴무는 한 원소)」 (`:476`) | `endDateTime`(배타 → 직전 날짜) | 병원 기본 휴무 | 충분 |  | 칸 없음 | 없음 |  |

#### E13. `GET /api/ext/clinics/{clinicId}/staff`

스키마 필드 합 **10** · 표의 스키마 행 **10** · 빠진 필드 **0**(경로 · 질의 · 헤더 행은 따로).

| 필드 | 타입 | Swagger 설명 (그대로 · `schemas/ext.py:줄`) | 값의 출처 | 출처 시점 | D2 | D2 빠진 것 | DAY 대응(`origin/dev`) | B1 | 후보 |
|---|---|---|---|---|---|---|---|---|---|
| `path clinicId` | `int` | (라우터 `api/ext.py` 의 Header · Path · Query 설명) | 상수 1 비교 | - | 충분 |  | `hospital.id`(uuid) | - |  |
| `clinicId` | `int` | 「요청한 `clinicId`」 (`:510`) | 요청 값 | - | 충분 |  | `hospital.id` | 가공 |  |
| `staff` | `list[ExtStaff]` | 「직원 — KOS 차례 · KOS 시스템 계정 · 제외 목록 계정은 뺀다」 (`:511`) | 내부 `account/v2/queries/get-accounts`(요청마다) | 조회 시점 | 충분 |  | `staff`(내부 같은 경로 · 1시간 동기화) | (묶음) |  |
| `staff[].staffId` | `int \| None` | 「ccc 직원 사본 id(접수 목록 · 예약 상세의 `counselor.staffId` 와 같은 체계). 사본에 아직 없는 계정이면 null」 (`:492`) | cc `staff.id`(KOS id 로 찾음) | - | 충분 |  | `staff.id`(uuid) | 가공 |  |
| `staff[].name` | `str` | 「이름(KOS 지금 값)」 (`:494`) | 내부 accounts `name` | 조회 시점 | 충분 |  | `staff.name`(1시간) | 있음 |  |
| `staff[].roleName` | `str \| None` | 「KOS 역할 이름(지점마다 설정이 다름 · 예 「CS팀(콜센터)」 = 외주 직원). 외주 직원은 이 칸으로 가른다」 (`:495`) | 내부 accounts `roleName` | 조회 시점 | 충분 |  | `staff.job_role_id` → `job_role.name`(내부 `role/v2/queries/get-roles`) | 가공 |  |
| `staff[].roleTags` | `list[str]` | 「역할 태그(`ADMIN` · `DOCTOR` · `COUNSELOR` · `NURSE` · `SKINCARE` · `CALL_COUNSELOR` · `COORDINATOR`) — ccc 직원 사본 값. 사본에 없는 계정이면 `[]`. `CALL_COUNSELOR` 가 있다고 외주가 아니다(코디 · 관리자에게도 붙는다)」 (`:497`) | cc `staff.role_tags` ← 공개 `account/open/v1/queries/get-accounts` `roleTags`(1시간 · `kos/sync.py:179`) | 직원 사본 갱신 | 충분 |  | `job_role.tags`(직무 단위 · 출처 = 역할 조회) — 계정 `roleTags` 와 같은 값인지 확인 안 됨 | 가공 |  |
| `staff[].active` | `bool` | 「활성 계정인가(KOS 값 · 비활성 직원도 싣는다)」 (`:500`) | 내부 accounts `activate` | 조회 시점 | 충분 |  | `staff.is_active` | 있음 |  |
| `staff[].email` | `str \| None` | 「이메일(KOS 지금 값). KOS 에 값이 없으면 null」 (`:501`) | 내부 accounts `email` | 조회 시점 | 충분 |  | `staff.email`(`mapper.py:241`) | 있음 |  |
| `staff[].realName` | `str \| None` | 「실명(KOS `realName` 지금 값). KOS 에 값이 없으면 null. `name`(KOS 표시 이름)과 다른 칸이다」 (`:502`) | 내부 accounts `realName` | 조회 시점 | 충분 |  | `staff.real_name`(`mapper.py:240`) | 있음 |  |
| `staff[].kosAccountId` | `str` | 「KOS 계정 id(문자열 · null 없음 · 사본에 없는 계정도 값이 있다). `staffId`(ccc)와 다른 체계다 — 다른 ext 응답의 `staffId` 와 이 값을 잇는 곳은 이 목록뿐이다」 (`:504`) | 내부 accounts `id` | - | 충분 |  | `external_ref`(entity=staff).external_id | 가공 |  |

### A2-1. 같은 이름 · 다른 출처

#### 사람 · 역할 필드 — 시점 한눈에

| 응답 칸 | 엔드포인트 | KOS 기록 · 칸 | 업무 시점 | 근거 |
|---|---|---|---|---|
| `reservations[].counselor` | E7 | 일정 `reservation.counselor` | **예약 · 접수 때 지정한 희망 상담사** | `cc:kos/reservation_sync.py:131` · `cc:service/ext.py:728` · Swagger `cc:schemas/ext.py:429-431` |
| `reservation.counselor` | E8 | 위와 같음(사본) | 예약 지정 희망 상담사 | `cc:service/ext.py:650` · `cc:schemas/ext.py:314-316` |
| `reservation.requestedDoctor` | E8 | `get-schedule-detail` `reservation.doctor` | 예약 지정 희망 의사 | `cc:service/ext.py:652` |
| `previousVisits[].counselors[]` | E8 | 지난 일정 `consultations[].counselors[]`, 비면 `consultation.counselor` | **상담 기록(상담 차트)의 상담자** — 비면 단일 상담 정보 | `cc:service/ext.py:576-589` · `cc:schemas/ext.py:352-354` |
| `previousVisits[].procedures[].doctors` | E8 | 지난 일정 `tasks[].doctors[].name` | 시술(작업) 의사 | `cc:service/reservations.py:213-216` |
| `staff[]` | E13 | 내부 `account/v2/queries/get-accounts` | 조회 시점 계정 | `cc:service/ext.py:876-902` |
| (응답 밖) 예약 담당자 | E3 쓰기 | `reservationAssignee` = KOS 시스템 계정 | 예약 생성 | `cc:service/reservations.py:803,880-887` |

**상담 차트 쪽 상담사 · 원장을 주는 칸은 「이전 방문」의 `counselors[]` 하나뿐**이다. 오늘(해당) 예약의 상담 차트 상담자 · 상담 원장 칸은 13개 응답 어디에도 없다(`ExtDetailReservation` 8칸 · `ExtBoardRow` 10칸 — `cc:schemas/ext.py:310-325,420-439`). 상담 원장(`consultations[].consultationDoctors`)은 cc 가 어느 응답에도 내지 않는다(`grep consultationDoctors` → cc 0 · DAY `day:day/emr/kos/mapper.py:506`).

#### 상태 · 시각 필드 — 시점 한눈에

| 응답 칸 | KOS 칸 | 업무 시점 |
|---|---|---|
| `state.main/sub`(E7 · E8) · `state`(E6) | `reservation.status` + 일정 `flowStep` | 사본을 읽은 때의 진행 단계 |
| `receptionAt`(E7) | `receptionDateTimeUtc` | 접수 |
| `firstConsultationWaitingAt`(E7) | 이력 `FlowStepChanged` → `CONSULTATION_WAITING` 최소 `raisedDateTimeUtc` | 처음 상담 대기 진입 |
| `consultation`(E7) | `flowStep` + **cc 자체 조작 기록**(`event_log` `reception` · `consultation_add`) | CC 조작 · 단계 |
| `start/end`(E5 ~ E8) | `occupiedResources[].reservationTime` | 예약 시각(내원 시각 아님) |
| `result` · `resultRaw`(E5 · E8) | `reservation.status` | 조회 시점 예약 상태 |
| `lastVisitDate`(E2) | visitor `lastVisitedDateTimeUtc` | KOS 「최근 방문」(정의 확인 안 됨) |
| `purchasedDate`(E2) | 시술권 장 `createdDateTimeUtc` 최소 | 시술권 발행 |
| `issuedDate` · `expiresAt`(E2) | 카드 `createdDateTimeUtc` · `expirationDateTimeUtc` | 카드 발급 · 만료 |
| `desiredDischargeAt`(E8) | `reservation.desiredDischargeDateTimeUtc` | 예약 때 적은 귀가 희망 |
| `health.submittedAt`(E8) | 문진 제출본 `createdDateTimeUtc`(cc 웹 제출이 더 새로우면 그것) | 문진 제출 |
| `syncedAt`(E1) · `sync.lastOkAt`(E7) | cc `sync_state` | cc 동기화 성공 |

#### 뜻 불일치 후보 (판정하지 않음)

| # | 필드 | 문서상 뜻(SPEC-008 · DEC · Swagger) | 코드상 출처 | 근거 파일:줄 |
|---|---|---|---|---|
| M1 | E7 `reservations[].counselor` · E8 `reservation.counselor` (+ `ExtStaffRef`) | 「**KOS 희망 상담사**(예약에 지정한 상담사 — 실제로 상담한 사람이 아니다)」(DEC-012 D-09) — 문서와 코드는 같다. 다만 칸 이름이 `counselor` 하나이고, 사용자가 기대하는 「상담 차트의 상담사」가 아니다 | 일정 `reservation.counselor` | `cc:kos/reservation_sync.py:131` · `cc:schemas/ext.py:314-316,429-431` · DEC-012 `:91` |
| M2 | E8 `previousVisits[].counselors` | 「그 방문의 상담자 — `consultations[].counselors[]` … 그것이 비면 `consultation.counselor` 하나」 | 두 KOS 기록(상담 기록 배열 / 일정 단일 상담 정보)을 한 칸에 섞는다. 단일 상담 정보의 `counselor` 가 무엇을 뜻하는 칸인지(지정 · 실제) 문서에 없다 | `cc:service/ext.py:576-589` · `cc:schemas/ext.py:352-354` |
| M3 | E8 `reservation.consultationMemo` · `previousVisits[].consultationMemo` · E11 쓰기 | 「상담 메모(= 차트 메모 · KOS 일정 `consultation.consultationMemo` 그대로)」 | 일정 **단일** `consultation.consultationMemo`. KOS 일정에는 상담 기록 배열 `consultations[]`(본문 `content.text`)이 따로 있고 DAY 는 그쪽을 「상담 메모」로 받는다 — 어느 쪽이 「차트 메모」인지 두 레포가 다르다 | `cc:service/ext.py:631-634` · `cc:service/reservations.py:211-212` · `day:day/emr/kos/mapper.py:497-508` · SPEC-000 `:535` |
| M4 | E2 `customer.isNew` · E7 `customer.isNew` · E8 `customer.isNew` | 「KOS 신규 고객 여부」 | E2 = 조회 때 KOS visitor 지금 값 · E7 · E8 = cc 고객 사본(마지막으로 그 고객이 든 아무 KOS 응답의 값) — 같은 이름 · 다른 시점. 「이 예약 기준」인지 문서에 없다 | `cc:service/ext.py:339,643,727` · `cc:kos/reservation_sync.py:147` |
| M5 | (없음 — 번호 비움) | | | |
| M6 | E7 `reservations[].consultation` | 「상담 거침(CC 판정) — 접수 뒤이고 ① 지금 상담 대기 · 상담 ② CC 접수가 상담 대기로 끝남 ③ CC 「상담 추가」 … KOS 「상담 필요」 체크는 보지 않는다」 | KOS 웹에서만 상담을 거쳐 이미 시술 단계로 간 일정은 `false` 가 될 수 있다(②③ 은 CC 조작 기록). 같은 줄의 `firstConsultationWaitingAt` 은 KOS 이력이라 값이 있을 수 있다 — 문서에 적혀 있으나 「상담 거침」이라는 이름과 범위가 다르다 | `cc:domain/reservation_rules.py:45` · `cc:service/ext.py:730` · `cc:schemas/ext.py:433-439` |
| M7 | (없음 — 번호 비움) | | | |
| M8 | (없음 — 번호 비움) | | | |
| M9 | E2 `customer.lastVisitDate` | 「최근 방문일 — KOS `lastVisitedDateTimeUtc` 의 KST 날짜」 | KOS 값 그대로 — 무엇을 방문으로 세는지(예약 생성 · 접수 · 완료) 문서 · 코드 어디에도 없다 | `cc:service/ext.py:340` · `cc:schemas/ext.py:162-163` |
| M10 | E2 `tickets[].purchasedDate` | 「가장 이른 시술권 발행 시각(**수납 완료 때**)의 KST 날짜」 | 장 `createdDateTimeUtc` 최소값 — 「수납 완료 때 발행」은 코드가 확인하지 않는 설명이다 | `cc:service/ext.py:379-380,390` · `cc:schemas/ext.py:175` |
| M11 | (없음 — 번호 비움) | | | |
| M12 | E8 `customer.*` · E7 `customer.*` | 「고객 기본 정보 + 나이 · 언어 · 고객 유입」 | 한 객체 안에서 이름 · 성별 · 국적 · 차트번호 · 신규는 cc 사본(마지막 갱신 시점), 나이 · 언어 · 고객 유입은 요청 때 `get-visitor`(지금 값) — 시점이 섞인다 | `cc:service/ext.py:640-647` |

후보 수 = **8**(M1 · M2 · M3 · M4 · M6 · M9 · M10 · M12 — 번호 M5 · M7 · M8 · M11 은 검토 뒤 뺐다: 문서와 코드가 같은 뜻으로 적혀 있음).

### A3. 인증 · 연동처

| 항목 | 사실 | 근거 |
|---|---|---|
| 헤더 | `X-Api-Key: <연동처 키>` — `Authorization` 은 보지 않는다 | `cc:api/ext.py:1-5,47-60` |
| 키 저장 | 서버 env `PROC_EXT_KEY_LINKY` · `PROC_EXT_KEY_CHARTY`(빈 값 = 그 연동처 꺼짐) | `cc:config.py:35-36` · `procedure/.env.example:16-17` |
| 연동처 | 코드 고정 `CLIENTS = ("linky", "charty")` — 등록된 연동처 이름 = **linky · charty** | `cc:service/ext.py:64,157-165` |
| 비교 | `hmac.compare_digest` · 모든 연동처와 다 견줌 | `cc:service/ext.py:157-165` |
| 발급 · 전달 | 키 원본 = 레포 밖 파일 → 클러스터 Secret(코디 기본값) · 연동처에 DM 전달은 사용자 몫 | 회고 `log/2026-11-12-api-swagger-docs.md` §4 · §7 |
| 지점 범위 | cc 서버 하나 = KOS 병원 하나(`KOS_TENANT_ID`) · `clinicId = 1` 고정 · 연동처별 권한 분기 없음 | `cc:service/ext.py:80` · DEC-012 D-01 · D-20 |
| 호출 제한 | 키당 최근 60초 60번(메모리) · 연동처 없는 오류 응답 IP 당 60초 10번이면 IP 차단 | `cc:service/ext.py:65-66,167-175` |
| 호출 기록 | 표 `ext_call`(시각 · 연동처 · `<METHOD> <경로 틀>` · 상태 · 결과 code) — 이름 · 이메일 · 키 · IP · 고객 id 없음 | `cc:service/ext.py:178-191` |
| 열람 기록 | 선택 헤더 `X-Ext-Staff-Id`(연동처 신고 · 검증 안 함) → `event_log` `ext_view` · 행위자 문자열 `ext:<연동처>[:<직원 id>]` | `cc:api/ext.py:65-100` · `cc:service/ext.py:116-118,293-299` |
| 에러 형식 | `{"error": {"code", "message"}}` · 검증 오류 = `400 invalid_request`(422 아님) · 응답마다 `Cache-Control: no-store` | `cc:main.py:67-68,120-124` · `cc:api/ext.py:139-142` |
| Swagger | §D1 | |

### A4. 실제 사용처 (문서 · 회고 근거만)

| 연동처 | 근거 있는 사용 | 근거 |
|---|---|---|
| charty(1차 상담 차팅 서비스) | 상담 대기 화면 · 예약 상세 · 메모 쓰기 · 병원/직원 정보를 요청 → E2(고침) · E7 ~ E13 을 만든 이유 | `log/2026-11-16-ext-api-charty1.md:9` · DEC-012 `:54` |
| linky | 「linky 도 같은 API 를 쓴다」(공통 키 체계) · 1차 · 2차(E1 ~ E6) 요청 주체 「협업자(링키 · 차티)」 | DEC-012 D-01 `:78` · `log/2026-11-12-api-swagger-docs.md` §1 |
| (연동처 미상) | 직원 목록 칸 셋(E13 0.4.7) — 「연동처가 계정을 이으려면」 | `log/2026-11-17-ext-api-staff-fields.md:7` |

- 엔드포인트별로 어느 연동처가 실제로 부르는지(운영 `ext_call` 집계)는 **확인 안 됨**(서버 DB 접속 금지).
- 협업자 쪽 연동 완료 여부 · 키 전달 여부는 **확인 안 됨**(회고 §7 잔여 「연동처 키 전달 — 사용자」).

---

## B. 이관 (DAY `origin/dev`)

### B1. 값이 DAY DB 에 있나

필드별 판정은 §A2 통합표의 `DAY 대응` · `B1` 칸이다. 엔드포인트별 집계(값 칸만):

| # | 있음 | 가공 | 없음 | 없음(시점 다름) |
|---|---|---|---|---|
| E1 메뉴 | 18 | 11 | 1 | 0 |
| E2 고객 조회 | 6 | 7 | 4 | 1 |
| E3 예약(응답) | 0 | 2 | 0 | 0 |
| E4 가능 시간대 | 1 | 1 | 1 | 0 |
| E5 과거 시술 | 0 | 4 | 0 | 0 |
| E6 예약 내역 | 0 | 0 | 5 | 0 |
| E7 접수 목록 | 7 | 11 | 2 | 0 |
| E8 예약 상세 | 15 | 23 | 7 | 2 |
| E9 ~ E11 쓰기 응답 | 0 | 0 | 0 | 0 |
| E12 병원 | 0 | 1 | 6 | 6 |
| E13 직원 | 4 | 5 | 0 | 0 |
| **합** | **51** | **65** | **26** | **9** |

`가공` 의 대부분은 **id 체계**다 — cc 정수 id(`customerId` · `reservationId` · `staffId` · `clinicId`)는 DAY 에서 uuid(`uuid_pk()` · `day:day/models/*.py`)이고, KOS id(메뉴 · 시술권 옵션 · 직원 `kosAccountId`)는 `external_ref` 에만 있다(data_rules 「외부 id 는 external_ref 한 테이블에만」 · `day:day/models/customer.py:88-112`).

#### `없음` · `없음(시점 다름)` — KOS 어디에 있나 · DAY 가 받고 있나 · 받으려면

| 칸 | KOS 어디 | DAY 가 지금 받나 | 받으려면 필요한 것(사실만) |
|---|---|---|---|
| 고객 `email`(E2 · E3 · E5 · E6 식별) | 내부 `visitor/v2/queries/get-visitors` · `get-visitor` 의 `email` | 아니오 — 칼럼 `customer.email` 은 있으나 일정 안 `visitor` 매퍼가 email 을 안 받는다 | 일정 응답 visitor 에 email 이 있는지 확인 안 됨. 백필은 `get-visitors` 를 「나열에만」 쓴다(`day:day/services/emr_backfill.py:12-13` · `day:day/emr/kos/sale_reads.py:65,323`) |
| E8 `customer.language` · `customer.funnel` | 내부 `get-visitor` `language` · `visitorFunnel` | 아니오(칼럼 `customer.language` · `funnel_id` · `funnel_detail` 있음) | 위와 같음 |
| E2 `customer.isNew`(고객 현재 값) | visitor `isNew` | `visit.is_new`(방문마다)만 — 고객 칼럼 없음(SPEC-000 `:360`) | 설계 결정(고객 칼럼을 안 두기로 함) |
| E2 `tickets[].purchasedDate` · `prepaidCards[].issuedDate` | 장 · 카드 `createdDateTimeUtc` | 아니오(DAY `created_at` 은 DAY 행 생성 시각) | 칼럼 없음 |
| E2 `prepaidCards[].balance.total` · `point.total` · 통화 | 카드 `remaining*.total` · `currency` | 아니오(`balance` 만) | 칼럼 없음(`day:day/emr/kos/mapper_purchase.py:315-320`) |
| E2 시술권 · 카드 전체(신선도) | 내부 `get-ticket-bundles` · `get-prepaid-card-summaries` | **오늘 일정이 있는 고객만**(일정 태스크가 발행 · `day:day/tasks/emr.py:74-85`) + 수동 백필 | 오늘 방문하지 않는 고객의 잔량은 백필 뒤 갱신 경로 없음 |
| E4 `slots[].remainingSeats` | 공개 `schedule/open/v2/queries/get-reservation-slots-by-groups` | 아니오(DAY 에 이 경로 0 — `git grep get-reservation-slots` → 0) | 칸별 예약 수 칼럼 없음 · 미래 일정 미동기화 |
| E6 전부(오늘 이후 일정) | 공개 `get-schedules-by-visitor` / 내부 날짜별 일정 | **오늘만**(`day:day/services/emr_sync.py:111-115`) | 창 확장 또는 다른 경로 |
| E8 `reservation.consultationMemo` · `previousVisits[].consultationMemo` | 일정 `consultation.consultationMemo` | 다른 칸(`consultations[].content.text`)을 받는다 | 같은 글인지 KOS 실물 확인 필요(확인 안 됨) |
| E8 `requestedProcedures[].optionId` · `ticketId` | `optionConfiguration.optionId` · `ticketConfiguration.ticketId` | 아니오(매퍼가 「KOS 옵션 id 를 두지 않는다」 `day:day/emr/kos/mapper.py:333-336`) | 칼럼(`product_option_id`)은 있음 · 시술권 id 칼럼 없음 |
| E8 `health.*` | 공개 `visitor/open/v1/queries/get-visitor-questionnaire` · `get-questionnaire-submit` | 아니오 — `questionnaire_history` 표는 있으나 쓰는 코드 0(`git grep QuestionnaireHistory` → 모델 · 식별자뿐) | 동기화 경로 없음 |
| E12 전부 | 내부 `v1/hospital/queries/get-hospital` · `schedule/default-operation-time/...` | 아니오 — `hospital` 은 이름(DAY 설정)만 · 시간표는 예약 그룹별만 | 칼럼 없음 |
| E1 `syncedAt` · E7 `sync.*` | (cc 자체 메타) | DAY 회차 성공 시각 칸 확인 안 됨 | — |

### B2. 쓰기 값 — DAY DB 어디 · DAY → KOS 경로가 있나

| cc 쓰기 | cc 가 KOS 에 쓰는 곳 | DAY DB 자리 | DAY 에 그 KOS 쓰기 경로가 있나 |
|---|---|---|---|
| E3 예약 | ① 내부 `visitor/v1/queries/find-duplicated-visitor` ② 내부 `v1/visitor/commands/create-visitor`(0명) ③ 내부 `schedule/reservation/v2/commands/reserve`(그룹 · 구역 · 담당자 = 시스템 계정 · 메모) → 다시 읽기(`cc:service/reservations.py:779-938`) | `customer`(새 고객) · `visit` · `visit_occupied_resource` · `external_ref` | **없음** — `day:day/emr/kos/writes.py:47-56` 표에 reserve · create-visitor 없음(`git grep` 0) |
| E9 언어 | 내부 `visitor/v2/queries/get-visitor` 다시 읽기 → 내부 `visitor/v2/commands/update-visitor-personal-information`(개인정보 묶음 전체) | `customer.language`(미동기화 칼럼) | **없음** |
| E10 오더 메모 | 내부 `schedule/v1/commands/change-order-memo {scheduleId, orderMemo}` | `visit.procedure_order_note` | **없음**(운영 `writes.py` 에 없음 · 같은 경로 상수가 데모 시드 `day:day/emr/kos/demo/kos_board.py:84` 에만 있음 — 데모 테넌트 가드 영역) |
| E11 상담 메모 | 공개 `schedule/open/v1/commands/update-schedule-consultation-info {scheduleId, consultationMemo}` | DAY `consultation.consultation_note` 는 다른 KOS 칸(M3) | **없음** |

DAY 에 있는 KOS 쓰기는 시술 현황 조작 18줄뿐이다(방 · 담당 · 의사 호출 · 단계 · 완료 · 작업 추가 · 간호/의사 차트 글 — `day:day/emr/kos/writes.py:9-29`).

### B3. KOS → DAY → 서비스 방향이 되나

DAY 의 읽기 동기화 주기 · 트리거(근거):

| 묶음 | 주기 · 트리거 | 범위 | 근거 |
|---|---|---|---|
| 일정 + 그 고객 | 10초(`SYNC_SCHEDULE_INTERVAL_SECONDS`) · scheduler | **병원 현지 오늘 00:00 ~ 다음 날 00:00** | `day:day/tasks/emr.py:3-4,113-118` · `day:common/config.py:119` · `day:day/services/emr_sync.py:111-115,206-207` |
| 오늘 구매 · 시술권 · 카드 | 일정 회차 뒤 별도 태스크 | 오늘 일정의 참조 · 그 고객 | `day:day/tasks/emr.py:74-85,98-105` |
| 기준 정보(구역 · 방 · 그룹 · 직무 · 직원 · 코드) | 3600초 · 시작 때 1회 | 병원 전체 | `day:day/tasks/emr.py:5-6,121-126` · `day:common/config.py:120` |
| 메뉴 | 기준 정보 회차 뒤 | 병원 전체 | `day:day/tasks/emr.py:89-95` · `day:day/emr/sync_menu.py:1-12` |
| 지난 이력 | **수동**(`python -m runtime.backfill`) · 어제까지 · KOS 1초 1회 | 일정 · 구매 · 시술권 · 카드 | `day:day/services/emr_backfill.py:1-20` |

| # | 판정 | 이유(사실) |
|---|---|---|
| E1 메뉴 | **DAY DB 만** | 메뉴 1시간 동기화(cc 와 같은 주기) · `syncedAt` 대응 칸만 없음 |
| E2 고객 조회 | **KOS 실시간 필요** | 이름+이메일 갈래 = DAY 에 email 없음 · 시술권 · 카드는 오늘 방문 고객만 갱신(그 밖은 백필 시점 값) · `lastVisitDate` · `isNew` 칸 없음 |
| E3 예약 | 쓰기(B4) | |
| E4 가능 시간대 | **KOS 실시간 필요** | 칸별 정원 · 예약 수 원천(`get-reservation-slots-by-groups`) 미동기화 · 미래 날짜 일정 없음 |
| E5 과거 시술 | **지금 그대로는 불가** | 데이터(과거 `visit` · `visit_task`)는 백필 범위에 있으나 요청이 이름+이메일뿐이고 DAY 에 email 이 없다(식별 불가) |
| E6 예약 내역 | **KOS 실시간 필요** | 오늘 이후 일정이 DAY 에 없다 · 식별도 email |
| E7 접수 목록 | **DAY DB 만** | 오늘 `visit` 10초 동기화(cc 10초 캐시와 같은 신선도) · 희망 상담사 · 접수 시각 · 방 칼럼 있음 · 처음 상담 대기는 `visit_flow_log` 로 가공(원천 다름) |
| E8 예약 상세 | **KOS 실시간 필요(일부 칸)** | DB 로 되는 칸: 예약 · 희망 상담사/의사 · 희망 시술 · 오더 메모 · 고객 기본. 안 되는 칸: 언어 · 고객 유입 · 문진 · 상담 메모(원천 다름) · 이전 방문(백필 범위 밖) |
| E9 ~ E11 | 쓰기(B4) | |
| E12 병원 | **KOS 실시간 필요** | DAY 에 병원 전화 · 주소 · 기본 운영 시간 · 휴무 칼럼 없음 |
| E13 직원 | **DAY DB 만** | `staff`(이름 · 실명 · 이메일 · 활성) · `job_role`(이름 · 태그) · `external_ref` — 1시간 신선도(cc 는 요청마다 KOS) |

집계: DAY DB 만 **3** · KOS 실시간 필요 **5** · 불가 **1** · 쓰기 **4**.

### B4. 서비스 → DAY → KOS 방향이 되나

**cc 는 어떻게 했나**: 쓰기 넷 모두 **KOS 먼저 · 동기**다. KOS 성공 뒤에만 cc 사본 · 기록을 바꾸고, 실패하면 `event_log kos_rejected` 1줄 + `409 kos_rejected` / `502 kos_unavailable` 를 그대로 돌려준다. **재시도 · 큐 없음**(`cc:service/reservations.py:715-726` · `cc:service/ext.py:667-686` · 계약 `cc:api/ext.py:440-447`). 예약은 쓴 직후 KOS 를 다시 읽어 사본을 만든다(`cc:service/reservations.py:848-860`).

**DAY 에 있는 것**(쓰기 큐 `external_outbox`):

| 있는 것 | 근거 |
|---|---|
| 큐 표 `external_outbox`(병원 · 업체 · **visit_id(NOT NULL)** · seq · api · path · body · expect · status · attempts · checks · last_error) | `day:day/models/task.py:227-250` |
| 보내기 10초 + 조작 직후 즉시 발행 · 재시도 상한 `MAX_ATTEMPTS = 3` · 확인 실패 상한 `MISS_LIMIT = 2` · 앞 쓰기 실패 시 같은 방문 뒤 쓰기 막음(`BLOCKED`) · 업체 미지원(`NOT_SUPPORTED`) · 보냈는데 확인 안 됨(`STALE` · 180초) | `day:day/tasks/emr.py:7-8,129-134` · `day:day/emr/outbox_persistence.py:24-42` · `day:common/config.py:121,137` |
| **확인 = 다음 조회에서 값 비교**(`expect`) · 반영 대기 칸은 조회 값으로 덮지 않음 | `day:day/emr/kos/writes.py:35-40` · `day:day/emr/sync_schedules.py:295-311` |
| 충돌 = 외부(KOS)가 이긴다 | data_rules |
| **토큰 = 누른 직원의 KOS 토큰만** — 없으면 보내지 않음(다른 직원 토큰 금지 · DAY-SPEC-001 규칙 4) · 기다림 상한 1800초(`NO_TOKEN`) | `day:day/emr/outbox_delivery.py:30-47` · `day:common/config.py:143` · `day:day/emr/kos/__init__.py:28` |
| 쓰기는 (경로 + 값) 단위로 연다 · 표 밖은 `WriteNotSupportedError` | `day:day/emr/kos/__init__.py:25-27` |

**DAY 에 없는 것**:

- cc 쓰기 넷의 KOS 경로(B2 표) — 0/6.
- 연동처(직원 세션 없음)가 쓸 KOS 토큰 — 지금 규칙상 시스템 계정 토큰으로 보내는 길이 없다.
- 고객 단위 쓰기 큐 — `external_outbox.visit_id` 가 NOT NULL 이라 고객 언어처럼 방문에 묶이지 않는 쓰기 자리가 없다.
- 「DAY 가 먼저 받고 나중에 KOS 에 반영」일 때 연동처에 돌려줄 상태(반영 중 · 실패) 계약 — cc 계약은 「200 = KOS 반영 끝」이다(`cc:schemas/ext.py:277-278`).
- 연동처 행위자 기록 자리 — DAY `event_log.actor_staff_id` 는 `staff` FK(`day:day/models/task.py:219`) · cc 는 문자열 `ext:<연동처>:<직원 id>`.

### B5. DAY 쪽 그릇

| 항목 | DAY `origin/dev` 사실 | 근거 |
|---|---|---|
| 자리 | `routers/api/` = 「JSON 라우터 (앱 · **외부**)」 · `schemas/` = 「JSON API 계약 (앱 · 외부)」 · 기능별 같은 파일 이름(`routers/api/<f>.py` · `services/<f>.py` · `schemas/<f>.py`) | AGENTS.md 「저장소 구조」 · 「계층 규칙」 |
| 붙는 곳 | `day.public.api_routers()` 목록(지금 6개: auth · board · chat · devices · notifications · interpret) → `runtime/main.py` 가 include | `day:day/public.py:220-231` · `day:runtime/main.py:66-67` |
| 계층 | router 는 HTTP 만(DB 금지) · service 가 세션 직접(**repository 없음**) · 묶음 조회는 `queries/` · ORM 은 `day` 밖으로 안 나감 | AGENTS.md 「계층 규칙」 · 경계 시험 `taut.toml:20` · `tests/architecture/` |
| 외부 쓰기 | DB transaction 안에서 외부를 기다리지 않는다 · outbox · 업체 미지원은 드러낸다 | AGENTS.md 「외부 CRM 연동」 |
| 인증 | 세션 하나(`login_session`) — 웹 쿠키 `day_session` · 앱 Bearer · CSRF. **API 키 인증 없음**(`git grep "X-Api-Key"` → 0) | `day:day/session.py:1-12,46-90` |
| 병원 | 여러 병원 · 업무 테이블에 `hospital_id` · 연결 업체는 병원별 `crm_connection` | `day:day/models/hospital.py:41-63` · AGENTS.md |
| 파일 크기 | 활성 Python 파일 700줄 이하 | AGENTS.md 「테스트」 끝 |
| 외부 계약 | API 경로 · 인증 · 오류 계약은 외부 계약 | AGENTS.md 「작업 규칙」 |

**그대로 옮길 수 없는 지점**:

1. cc `ExtService` 는 `ReservationService` 의 KOS 호출 · SQLite `Repository.tx()` 를 직접 부른다(`cc:service/ext.py:147-152,263,421,596-602`) — DAY 는 업무 코드가 업체를 모르고 `emr/base.py` 인터페이스만 부른다(AGENTS.md 「외부 CRM 연동」 · `day:day/emr/base.py:1-4`).
2. DAY 업무 코드에는 「요청 때 KOS 를 읽는」 인터페이스가 동기화 · 백필 · 로그인 외에 없다(`day:day/emr/kos/__init__.py:1-29` 의 읽기 목록).
3. id: cc 정수 → DAY uuid(응답 타입 · 경로 칸 타입 변경).
4. `clinicId = 1` 고정 — DAY 는 병원 여럿(키 ↔ 병원 연결이 필요).
5. 키: cc env 두 개 + 코드 고정 연동처 — DAY 는 비밀값을 Key Vault 로만 싣고 `deploy/config/<env>.env` 에 비밀 키를 넣으면 배포 스크립트가 거부한다(`deploy/config/dev.env:1-2` 주석 · AGENTS.md).
6. cc `ext_call` · `consult_wait_first` · 메모리 호출 제한 — DAY 에 같은 표 · 구조 없음(DAY 는 Redis 가 있다 `day:common/redis.py`).
7. 행위자: cc `event_log.actor` 문자열 — DAY `event_log.actor_staff_id` FK.
8. cc 의 「CC 판정」(`consultation`)은 cc 조작 기록(`reception` · `consultation_add`)을 읽는다 — DAY 조작 · 이벤트 이름과 대응 확인 안 됨.
9. 쓰기: B4.

### B6. 도메인

| 항목 | 사실 | 근거 |
|---|---|---|
| 있나 | **있다** — `DAY_PROD_DOMAIN=day.medisolveai.com` · `DAY_DEV_DOMAIN=day-dev.medisolveai.com` | `deploy/config/edge.env:2-3` |
| 어디로 | Caddy 사이트 블록 `{$DAY_PROD_DOMAIN}` → `day-prod-api:8000`(모든 경로 · 본문 상한 6MiB · SSE flush) | `deploy/caddy/Caddyfile:6-21` |
| 서버 설정 | prod `DAY_PUBLIC_API_BASE=https://day.medisolveai.com`(앱 로그인 응답의 연결 대상) | `deploy/config/prod.env` · mediness `products/day/40-architecture/deployment.md:31,164,167` |
| 상태 | 2026-11-12 prod 첫 배포 완료 · DNS A 레코드 등록(가비아) | `deployment.md:21,237` |
| 그 도메인의 Swagger | prod 는 `docs_url=None` · `openapi_url=None`(APP_ENV ≠ dev) | `day:runtime/main.py:53-61` |
| 경로 충돌 | `/api/ext` 는 DAY 에 없음(`git grep "/api/ext"` → 0) | |

즉 `day.medisolveai.com` 은 **DAY prod(운영 KOS 연결)** 다. 데모 테넌트 연결은 dev 서버(`day-dev`)만 동기화한다(data_rules 「APP_ENV=dev 서버는 데모 테넌트 연결만」).

---

## C. 정할 것 (결정하지 않음)

| # | 질문 | 선택지 | 각 선택의 근거(사실) |
|---|---|---|---|
| C1 | 연동처의 고객 식별 수단 | ① 이름+이메일 유지 → DAY 고객 동기화에 email 추가 ② DAY `customerId`(uuid)만 ③ 식별은 KOS 실시간 검색(cc 방식) 유지 | DAY `customer.email` 칼럼은 있으나 미동기화(B1) · cc 이름 검색은 내부 `get-visitors` 1000건 한 페이지에 기댄다(`cc:service/ext.py:258-285`) · 회고의 운영 위험 「이름 검색이 내부 get-visitors 에 기댄다」 |
| C2 | 미래 일정(E4 가능 시간대 · E6 예약 내역)의 원천 | ① DAY 동기화 창을 미래로 넓힘 ② 이 두 경로만 KOS 실시간(목표 구조의 예외) ③ 이관 범위에서 뺌 | DAY 는 오늘 창만(`emr_sync.py:111`) · 칸 정원 원천 미동기화 |
| C3 | 시술권 · 선불카드 신선도(E2) | ① DAY 사본 그대로(오늘 방문 고객 + 백필 시점) ② 조회 때 그 고객만 KOS 에서 받아 DB 갱신 뒤 응답 ③ KOS 실시간 중계 | 판매 동기화 범위 `tasks/emr.py:74-85` · 백필은 수동 |
| C4 | `counselor` 칸의 뜻(사용자 기대 = 상담 차트) | ① 희망 상담사 그대로(이름만 분명히) ② 상담 기록 상담사로 바꿈 ③ 두 칸 다 | DAY 에 `visit.requested_counselor_id` · `consultation.counselor_id` 둘 다 있음 · 상담 기록은 1명일 때만 저장(`mapper.py:491-494`) |
| C5 | 「상담 메모(차트 메모)」 원천 | ① 일정 `consultation.consultationMemo`(cc · 공개 쓰기와 같은 칸) ② `consultations[].content.text`(DAY) ③ KOS 실물로 두 칸 관계 확인 뒤 | M3 · 두 칸이 같은 글인지 확인 안 됨 |
| C6 | 연동처 쓰기가 KOS 로 갈 토큰 | ① 시스템 계정 토큰 허용(DAY-SPEC-001 규칙 4 의 예외) ② `X-Ext-Staff-Id` → DAY 직원 매핑해 그 직원 토큰 ③ 연동처 쓰기는 KOS 직접 동기(cc 방식) | outbox 는 누른 직원 토큰만(`outbox_delivery.py:30-47`) · cc `X-Ext-Staff-Id` 는 검증 안 하는 신고값 |
| C7 | 쓰기 응답 계약 | ① KOS 먼저 · 200 = 반영 끝(cc) ② DAY DB 먼저 · outbox · 200 = 접수(반영 중 상태 별도) | data_rules 「외부에 먼저 쓴다(outbox) … 확인 전까지 반영 중」 · cc `ExtOk` 뜻 |
| C8 | 고객 단위 쓰기(언어) 큐 | ① outbox 를 고객 단위로 넓힘 ② 고객 쓰기는 동기 ③ 범위에서 뺌 | `external_outbox.visit_id` NOT NULL |
| C9 | 예약 · 고객 생성 쓰기를 DAY 가 여는지 | ① `reserve` · `find-duplicated-visitor` · `create-visitor` 행을 `writes.py` 에 더함 ② 예약 생성은 이관하지 않음 | DAY `writes.py` 0 · cc 예약은 담당자 = 시스템 계정 · 이메일 존재 노출 수용(DEC-010) |
| C10 | id 체계 | ① DAY uuid 그대로(계약 변경 안내) ② 연동처용 별도 공개 id | cc 정수 · DAY uuid |
| C11 | 연동처 키 ↔ 병원 | ① 키 하나 = 병원 하나 ② 키 + 경로 `clinicId`(DAY hospital id) ③ 키 하나 = 브랜드 | cc 서버 하나 = 병원 하나 · DAY 다병원 |
| C12 | 연동처 키 저장 · 발급 | ① env(Key Vault) 연동처별 ② DB 표(해시) + 발급 화면/스크립트 | DAY 비밀값 = Key Vault · env 파일 비밀 금지 |
| C13 | 호출 기록 · 열람 기록 · 행위자 | ① `event_log` payload 에 연동처 행위자 ② 새 표 ③ 남기지 않음 | `event_log.actor_staff_id` FK · cc `ext_call` · `ext_view` |
| C14 | 병원 정보(E12) 원천 | ① 기준 정보 동기화에 병원 설정 추가 ② KOS 실시간 ③ 범위에서 뺌 | DAY 칼럼 없음 |
| C15 | 처음 상담 대기 시각 원천 | ① KOS 단계 이력(cc) ② DAY `visit_flow_log`(10초 관측) | 관측은 조회 사이 단계를 놓친다(`sync_schedules.py:351-362`) |
| C16 | 「상담 거침」 판정 규칙 | ① cc 규칙을 DAY 조작에 맞춰 다시 정의 ② `visit_flow_log` 의 상담 단계 행 유무 ③ 칸 제거 | M6 · cc 규칙은 cc 조작 기록에 기댄다 |
| C17 | 문진(E8 `health`) 원천 | ① 동기화 추가(`questionnaire_history`) ② KOS 실시간 ③ 범위에서 뺌 | DAY 표 있음 · 쓰는 코드 0 |
| C18 | Swagger 로그인 방식 | ① DAY 웹 세션(KOS 로그인) 재사용 — 직원만 문서 열람 ② 연동처 전용 계정 · 비밀번호 ③ 문서는 공개 · Try it out 은 연동처 키(cc 방식) ④ 관리자(`DAY_ADMIN_EMAILS`)만 | §D3 |
| C19 | Swagger 노출 범위 · 서버 | ① ext 라우터만 ② DAY 전체 API ③ prod(`day.medisolveai.com`)에도 열기 / dev 만 | DAY 는 dev 만 `/docs` (`runtime/main.py:58-60`) · cc 는 전체 공개 |
| C20 | 동기화 메타 칸(`syncedAt` · `sync.lastOkAt/lastError` · `partialErrors`)을 DAY 응답에 둘지 | ① DAY 회차 성공 시각을 기록해 냄 ② 칸 제거 ③ 의미를 바꿔 유지 | DAY 에 대응 칸 확인 안 됨 · KOS 실시간이 없으면 부분 실패 뜻이 바뀜 |
| C21 | 연동처 시험 환경 | ① `day-dev`(데모 테넌트)에서 시험 → prod ② prod 바로 | dev = 데모 연결만 · `day.medisolveai.com` = prod |

---

## D. Swagger (추가 지시 1)

### D1. cc Swagger 현황

| 항목 | 사실 | 근거 |
|---|---|---|
| URL | Swagger UI `/api/docs` · ReDoc `/api/redoc` · OpenAPI JSON `/api/openapi.json`(운영 호스트 `ccc.medisolveai.xyz`) | `cc:main.py:93-96` · `cc:openapi_docs.py:23-25` |
| 공개 여부 | **로그인 없이 열린다**(문서 · JSON 모두) — 「문서만 · 동작은 openapi_docs 참고」 | `cc:main.py:93` · `cc:openapi_docs.py:25` |
| 포함 범위 | **back 전체**(직원 API + 외부 연동 + 공개 문진 + 헬스) — ext 만이 아니다. ext 는 tag 「외부 연동」 | `cc:main.py:130-132` · `cc:api/docs.py:45` · `cc:openapi_docs.py:137-155` |
| 설정 코드 | `decorate(app)` 가 `app.openapi` 를 감싸 스키마 dict 만 고친다 — securitySchemes(`BearerAuth` · `ExtApiKey`) · operation 별 `security` · 422 제거 · 앱 설명(`DESCRIPTION` — 외부 연동 절 `:73-109`) | `cc:openapi_docs.py:158-231` |
| 오류 표 | `errors(...)` 도우미 — 상태별 `- code — 언제` 목록 · 모델 `ErrorResponse` | `cc:api/docs.py:65-71` |
| 필드 설명 | 스키마 모든 칸에 `Field(description=…)`(203/203 — §D2) | `cc:schemas/ext.py:1` |
| `test_ext_docs.py` 가 지키는 것 | ① ext operation 집합 = 13개(정확히) · tag · `security = ExtApiKey` · ext 밖에는 ExtApiKey 없음 ② 401 · 429 · 405 · 500 응답 설명 문구 ③ 이름 · 이메일이 경로 · 질의에 없음(질의는 `date` 하나 · 헤더 `X-Ext-Staff-Id` 는 다섯 operation) ④ 핵심 설명 문장(「고객이 낸 돈이 아니다」 · 「오늘 겹침」 · 「희망 상담사」 · 「덮어쓰기 위험」 · 「전역 유일하지 않다」 등) ⑤ 옛 문장이 없음 | `tests/test_ext_docs.py:6-16,24-77,80-106,109-140` |
| 회고의 결정 | 「API 문서는 코드 기준 Swagger(`/api/docs` · **공개**) · 동작 무변경」(2026-11-11 사용자 지시 · ingress 확인) · 70 operation · 683 필드 설명 · Swagger 설명을 시험으로 고정 · 잔여: 정적 `api-reference.html` 처리 · Swagger 기본 탭 Schema(사용자 답 없음) | `log/2026-11-12-api-swagger-docs.md` §1 · §2 · §4 · §7 |

### D2. 필드 설명 상태

판정은 §A2 통합표 `D2` 칸(설명 원문은 같은 표에 줄 번호와 함께 그대로 인용). 기준 = 뜻 · 출처 시점 · 단위 · null 일 때를 다 말하면 `충분`.

| # | 스키마 필드 | 충분 | 부족 | 없음 | 부족의 주된 이유 |
|---|---|---|---|---|---|
| E1 | 34 | 26 | 8 | 0 | `translsMap` 모양 예 없음 · 구성 칸 null 일 때 |
| E2 | 27 | 23 | 4 | 0 | `isNew` · `lastVisitDate` 정의 · 카드 `total` 뜻 · 금액 부가세 |
| E3 | 6 | 5 | 1 | 0 | `reservationId` KOS 반영 지연 |
| E4 | 5 | 5 | 0 | 0 | |
| E5 | 7 | 7 | 0 | 0 | |
| E6 | 8 | 8 | 0 | 0 | |
| E7 | 27 | 20 | 7 | 0 | 고객 칸 「사본」 시점 · 값 목록(성별 · 국적 · `sub`) · `ExtStaffRef.name` 원천 |
| E8 | 57 | 45 | 12 | 0 | 고객 칸 null · 값 목록 · `health.items` 모양 · `ExtStaffRef` 가 세 시점에 쓰임 · 이전 방문 `consultationMemo` 뜻 · `zoneTitle` 구역 종류 |
| E9 ~ E11 | 2 · 2 · 2 | 2 · 2 · 2 | 0 | 0 | |
| E12 | 16 | 14 | 2 | 0 | 운영 시작 · 끝 null 일 때 |
| E13 | 10 | 10 | 0 | 0 | |
| **합** | **203** | **169** | **34** | **0** | |

A2-1 후보와 겹치는 `부족`: M4(`isNew` — E2 · E7 · E8) · M9(`lastVisitDate`) · M12(E7 `customer.name` 등 사본 시점) · M1(E8 `ExtStaffRef.name`) · M3(E8 `previousVisits[].consultationMemo`). 후보 M1 의 `counselor` 칸 자체 · M2 · M6 · M10 은 설명이 「충분」인데 뜻이 사용자 기대 · 코드와 어긋나는 경우다(설명 충분 ≠ 뜻 일치).

### D3. 로그인 관련 사실

**cc**:

| 항목 | 사실 | 근거 |
|---|---|---|
| 문서 페이지 보호 | **없음** — `/api/docs` · `/api/redoc` · `/api/openapi.json` 로그인 없이 | `cc:main.py:93-96` |
| Try it out 인증 | **있음** — Authorize 에 `BearerAuth`(직원 토큰) · `ExtApiKey`(헤더 `X-Api-Key`) 두 scheme · ext 13 operation 은 `ExtApiKey` 만 | `cc:openapi_docs.py:193-207` · `tests/test_ext_docs.py:28-36` |

**DAY `origin/dev`**:

| 항목 | 사실 | 근거 |
|---|---|---|
| docs 설정 | `docs_url="/docs"` · `openapi_url="/openapi.json"` — **APP_ENV=dev 일 때만** · `redoc_url=None` · prod 는 둘 다 None | `day:runtime/main.py:53-61` · `deploy/config/prod.env` `APP_ENV=prod` |
| docs 보호 | 없음(FastAPI 기본 라우트 · 의존성 없음) · securitySchemes 손질 코드 없음 | `day:runtime/main.py:54-61` |
| 로그인 수단 ① 웹 | `GET/POST /login`(HTML · KOS 직원 이메일 · 비밀번호 → KOS sign-in) → 쿠키 `day_session`(httpOnly · SameSite=Lax · Secure) · CSRF | `day:day/routers/login.py:154-232` · `day:day/session.py:1-12,92-108` |
| 로그인 수단 ② 앱 | `POST /api/auth/login` → Bearer 토큰 · `POST /api/auth/hospital`(병원 고르기) · `GET /api/auth/me` · `POST /api/auth/logout` | `day:day/routers/api/auth.py:45,75-140` |
| 세션 | 둘 다 `login_session` 한 행(계정 · 병원 · 직원 · 만료) · 직원 KOS 토큰은 `external_session`(암호문) | `day:day/models/staff.py:83-110` · `day:day/session.py:6` |
| 세션 의존성 | `current_session` · `writable_session` · `require_permission(...)`(직무 권한) · 웹 화면용 `required_web_view` | `day:day/session.py:52-90,123-140` |
| 관리자 | env `DAY_ADMIN_EMAILS`(전체 권한 계정 목록 · 값은 이 리포트에 안 적음) · `account.is_system_admin` | `day:common/config.py:146,262` · `day:day/models/staff.py:29` |
| 시스템 계정 | KOS 동기화용 시스템 계정 = `staff.is_system_account`(직원 로그인 수단 아님) | `day:day/models/staff.py:58` · `day:day/emr/kos/mapper.py:249-250` |
| API 키 인증 | 없음 | `git grep "X-Api-Key"` → 0 |

**붙일 수 있는 자리(사실)**:

- 문서 라우트를 앱 생성 때 `docs_url=None` 으로 끄고 별도 라우트로 다시 열면, 그 라우트에 `current_session` / `required_web_view` / `require_permission` 의존성을 걸 수 있다 — 웹 로그인 세션(쿠키)을 그대로 쓰는 자리다(`day:day/session.py:52-90,123-140`).
- Try it out 의 연동처 키는 cc 처럼 OpenAPI `securitySchemes` 에 `apiKey`(header)를 싣는 자리다 — DAY 에는 아직 스키마 손질 코드가 없다(cc `decorate` 상당).
- 앱 생성은 `runtime/main.py` 한 곳이고, 라우터 목록은 `day.public.api_routers()` 다(`day:day/public.py:220-231`).
- 어느 방식을 쓸지는 C18 · C19.
