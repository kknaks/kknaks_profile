---
type: spec
id: SPEC-008
title: "시술 · 상품 메뉴 저장 + 외부 연동 API(`/api/ext` — 메뉴 · 이름+이메일 고객 조회 · 남은 시술권 · 예약 · 예약 가능 시간대 · 과거 시술 · 예약 내역) · 연동처별 키 계약"
version: 0.3.3
status: draft
product: cc-prototype
feature: procedure
created_at: 2026-11-11
updated_at: 2026-11-12
tags:
  - product/cc-prototype
  - feature/procedure
  - doc/spec
  - status/draft
links:
  baselines: []
  decisions:
    - "[[decision-010-product-ext-api|DEC-010]]"
    - "[[decision-011-ext-api-add1|DEC-011]]"
    - "[[decision-006-reservation-board|DEC-006]]"
    - "[[decision-005-procedure-board|DEC-005]]"
  specs:
    - "[[spec-005-reservation-board|SPEC-005]]"
    - "[[spec-003-procedure-board|SPEC-003]]"
    - "[[spec-006-customer-questionnaire-web|SPEC-006]]"
  works:
    - "[[work-012-product-ext-api|WORK-012]]"
    - "[[work-013-ext-api-add1|WORK-013]]"
  releases: []
  related: []
sources:
  - "para/projects/summer-star/cc-prototype/10-decision/decision-010-product-ext-api.md (DEC-010 · accepted · D-01 ~ D-36 · 2026-11-11 D-16 · D-19 · D-31 고침 · D-35 · D-36 추가)"
  - "orchestration/work/api-swagger-docs/review-doc-r1.md (doc 검수 r1 · WARN 13 · DEC 질문 Q-A ~ Q-C)"
  - "orchestration/work/api-swagger-docs/_RESUME.md §2 (2026-11-11 줄)"
  - "orchestration/work/api-swagger-docs/research-procedure-menu.md (조사 1 · 메뉴 키 트리 · §1 ~ §7)"
  - "orchestration/work/api-swagger-docs/research-purchase-snapshot.md (조사 2 · 고객 → 수납 → 시술권 · §1 ~ §4)"
  - "orchestration/work/api-swagger-docs/research-har-product-edit.md (조사 3 · 가격 수정 뒤 산 값 유지 · 옵션 id 유지)"
  - "orchestration/work/api-swagger-docs/research-name-email-lookup.md (조사 4 · 내부 get-visitors 이름 검색 · email 칸 · 페이징)"
  - "reference/2026-10-12-cc-prototype/kos-demo-api.md (공개 API 경로 · getTicketBundlesQuery 모양)"
  - "reference/2026-11-11-cc-product/har/ (내부 get-ticket-bundles 응답 키 모양만 · 값 안 옮김)"
  - "cc-prototype procedure/back origin/main c9f30ac (읽기만 — db.py · kos/ · service/reservations.py · schemas/reservations.py · domain/ · api/ · config.py · main.py · openapi_docs.py · tests/test_openapi_docs.py)"
  - "planner 질문 Q1 ~ Q5 코디 답(2026-11-11 · 부록 B)"
  - "para/projects/summer-star/cc-prototype/10-decision/decision-011-ext-api-add1.md (DEC-011 · accepted · D-01 ~ D-16(D-15 = 문서 검수 add1 Q-add1-A · D-16 = 코드 검수 add1 r1 N1 · 2026-11-12) · 2026-11-12 · add1 세 경로)"
  - "orchestration/work/api-swagger-docs/add1-spec-instructions.md (add1 지시 · 협업자 요청 요지)"
  - "cc-prototype procedure/back main e0e4a16 (읽기만 — §6.6 ~ §6.9 의 코드 규약 줄)"
  - "planner 질문 add1 Q1 ~ Q4 코디 답(2026-11-12 · 부록 E)"
  - "orchestration/work/api-swagger-docs/review-doc-add1.md (문서 검수 add1 · WARN 6 · Q-add1-A → 0.3.1)"
---

# 시술 · 상품 메뉴 저장 + 외부 연동 API 계약

> `procedure/back`(FastAPI) 이 지킬 계약이다. 정책의 원천은 **DEC-010(D-01 ~ D-36)** 이고, 결정 원천은 `orchestration/work/api-swagger-docs/_RESUME.md` §2 다. DEC-010 과 `_RESUME` 가 다르면 `_RESUME` 가 맞다.
> 화면(front · app)은 이번 범위가 아니다(D-01). 직원 API(SPEC-003 · SPEC-004 · SPEC-005 · SPEC-006 · SPEC-007)의 계약은 **바꾸지 않는다**. 이 문서가 더하는 것은 새 표 · 새 동기화 작업 · `/api/ext` 경로 여섯(0.3.0 에 셋 더함 — DEC-011) · 외부 키 인증뿐이다. 예외로 Swagger 문서 설정(`openapi_docs.py`)과 그 시험의 개수 단언 한 줄을 고친다(§8).
>
> 근거 표기: `D-nn` = DEC-010 · `R1 §` · `R2 §` · `R3 §` · `R4 §` = 조사 1 ~ 4 리포트의 절 · `KDA` = `kos-demo-api.md` · **`코드 규약: 파일:줄`** = DEC 에 없는 세부(이름 · 경로 · 표 · 코드 문자열)를 지금 코드에서 끌어온 곳(`procedure/back/` 아래 경로 · origin/main `c9f30ac` 줄) · **`코디 Q1 ~ Q5`** = DEC 와 코드 규약으로 정해지지 않아 planner 가 묻고 코디가 답한 것(부록 B · 2026-11-11).
> **0.3.0(add1)**: §6.6 ~ §6.9 · §9 T32 ~ T47 · 부록 D · E 는 **DEC-011(D-01 ~ D-16)** 을 근거로 한다 — 그 자리의 `DEC-011 D-nn` 은 DEC-011 번호이고, 꾸밈 없는 `D-nn` 은 지금처럼 DEC-010 이다. 그 절의 「코드 규약」 줄은 main `e0e4a16` 기준이다(앞 판 절은 `c9f30ac` 그대로).
> **이 레포는 public 이다** — 키 · 토큰 · 비밀번호 · 실명 · 이메일 · 연락처 · KOS id 값 · 실제 금액을 쓰지 않는다. env 는 이름만 적는다. 예시 값은 자리표시(`<이름>` · `a@example.com` · `<KOS id>`)다.

**변경 이력**

| 판 | 날짜 | 무엇 |
|---|---|---|
| 0.1.0 | 2026-11-11 | 첫 판(D-01 ~ D-34 · 코디 Q1 ~ Q5) |
| 0.2.0 | 2026-11-11 | doc 검수 r1 반영 — 이름 검색 한 페이지(1000) · 상한 · 중복 제거 · 이름 정확 일치(D-16 · D-19) · 시술권 가격 칸 `bundlePrice`(D-31) · 예약 이메일 드러남 수용 · Swagger 적기(D-35) · `syncedAt`(D-36) · 키 없는 거절 IP 제한 · 기록 미들웨어 · 검사 순서 · 켜진 구역 0 = 503 · 행위자 문자열 겹 · Swagger 503 · 근거 줄 고침 |
| 0.2.1 | 2026-11-11 | doc 검수 r2 N1 ~ N3 반영 — 「키 없는 거절」= `client` null 인 오류 응답 전부(깨진 본문 400 · 405 포함) · §6.2 `405 http_error` · 이름 띄어쓰기는 KOS 그대로(Swagger · 안내 줄 · T12 한정 · 404 시험 추가) · 메뉴 동기화가 실패해도 이전 `last_ok_at` 유지(`syncedAt` · T6) |
| 0.2.2 | 2026-11-11 | 코드 검수 r1 W1 · W3 · W7 반영 — 이름 검색 2xx 인데 `data` 가 배열 아님 = 502(예약은 새 고객 안 만듦) · 예약 502 · 409 `kos_rejected` 줄을 실제 단계대로 · 메뉴 구성 · 옵션 칸과 단위 `value` 에 「KOS 가 주지 않으면 null」 |
| 0.2.3 | 2026-11-11 | 코드 검수 r2 N1 반영 — 처리하지 못한 예외 = `500 internal_error` · `ext_call` 1줄 · IP 카운트 안 함(§6.2 · §7.4 · §3.4 정의에 예외 한 줄) |
| 0.3.0 | 2026-11-12 | add1(DEC-011) — 경로 셋 더함: `GET /api/ext/availability`(기본 그룹 예약 가능 시간대 · 남은 자리 · 슬롯 1번 새로 읽기) · `POST /api/ext/customers/visits`(과거 시술 · 최근 50) · `POST /api/ext/customers/reservations`(오늘 이후 예약 · 상태) · 경로별 KOS 호출 비용 표(§6.9) · 시험 T32 ~ T44 · Swagger 개수 단언 · 부록 D · E |
| 0.3.1 | 2026-11-12 | 문서 검수 add1 W1 ~ W6 반영 — 일정 응답 `{}` · `[]` = 빈 목록 · `data` 가 있으면서 배열 아님만 502(§6.7 · §6.8 2단계) · `deleted: true` 일정은 두 목록에서 뺌(DEC-011 D-15 · Q-add1-A 코디 기본값) · `date` 없음 message = `query.date: …` · 빈 문자열 400 · `str` 로 받음 · Swagger 시험 parameters 단언 넓힘 · 「세 경로 · 세 엔드포인트 합산」 → 「외부 경로 전부 합산」 · T29 · T34 · T36 · T39 · T44 줄 더함 |
| 0.3.2 | 2026-11-12 | 코드 검수 add1 r1 N1 ~ N3 반영 — 일정 원소 모양 오류 = `502 kos_unavailable`(원문 0 · DEC-011 D-16 · 코디 기본값) · 날짜는 `YYYY-MM-DD` 숫자 꼴만(ISO 주 날짜 등 400) · 경계 시험(시작 = 지금 정각 · 오늘 00:00) · 일정 읽기 4xx · 401 → 502 시험 · T45 ~ T47 |
| 0.3.3 | 2026-11-12 | 코드 검수 add1 r2 M1 반영 — T47: 작업 `title` 숫자 갈래는 과거 시술만 502(예약 내역은 작업을 보지 않음 · 200) · 로그 원문 0 은 리뷰 재현으로 확인(시험 단언 없음) |

## 0. 이 판에서 정한 것 한눈에

| 무엇 | 계약 | 근거 |
|---|---|---|
| 메뉴 저장 | KOS 메뉴 9종을 새 표 9개에 전부 넣는다. 각 행에는 조회 칸과 **KOS 원본 JSON(`raw`)** 이 함께 있다 | D-03 · D-04 |
| 메뉴 동기화 | 마스터 루프(1시간) + 서버 시작 1회. 작업 8개 | D-05 · D-06 · 코디 Q4 |
| 외부 API | `GET /api/ext/menu` · `POST /api/ext/customers/lookup` · `POST /api/ext/reservations` | D-10 · D-11 |
| 인증 | 헤더 `X-Api-Key`. 연동처 `linky` · `charty` 키는 각각 env 로 둔다. 직원 Bearer 와 섞이지 않는다 | D-10 · D-23 |
| 기록 · 제한 | 호출마다 미들웨어가 `ext_call` 1줄(이름 · 이메일 원문 없음 · 키 없는 거절은 같은 IP · 같은 결과 1분에 1줄). 키당 최근 60초 60회를 넘으면 `429`. 키 없는 거절(`client` null 인 오류 응답 전부)이 IP 당 최근 60초 10번이면 그 IP 를 `429` | D-24 · D-25 · D-34 · 코드 규약: 문진 웹 선례 |
| 고객 조회 | 내부 `get-visitors` 이름 검색 **한 페이지(1000)** → `count` > 1000 이면 「없음」 → KOS id 중복 제거 → 이름(또는 발음명) 정확 일치 → 이메일 정확 일치 → 0명 / 1명 / 2명 이상 | D-15 ~ D-22 |
| 시술권 가격 | `bundlePrice` = KOS 묶음 `price` 그대로 — 고객이 낸 돈이 아니고 부가세 포함 여부를 표기하지 않는다 | D-31 |
| 예약 | 1명이면 그 고객, 0명이면 새 고객(이름 + 이메일)으로 예약한다. 2명 이상이거나 KOS 중복 검사에 걸리면 `409 customer_ambiguous`. 이 409 가 이메일 존재를 드러내는 것은 받아들이고 Swagger 에 적는다 | D-32 · D-35 · 코디 Q1 |
| 2차(add1) | `GET /api/ext/availability?date=` · `POST /api/ext/customers/visits` · `POST /api/ext/customers/reservations`. 가능 시간대 = 기본 그룹 하나 · 예약 정원 검사와 같은 규칙 · 요청마다 KOS 슬롯 1번. 과거 시술 · 예약 내역 = 조회 규칙으로 고객을 정하고 KOS 고객 일정 1번 | DEC-011 D-01 ~ D-16 |

---

## 1. 범위

### 1.1 In (D-01 · D-02)

| # | 무엇 | 근거 |
|---|---|---|
| I1 | KOS 메뉴(카테고리 · 상품 · 옵션 · 구성 · 시술 · 진료항목 · 기기 · 약물 · 타겟 국가)를 ccc DB 에 **모든 칸** 그대로 저장한다(§3) | D-03 · D-04 |
| I2 | 메뉴 동기화를 마스터 루프에 얹는다(§4.1) | D-05 · D-06 · D-07 |
| I3 | 외부 연동 API 셋: 메뉴 조회 · 고객 조회(이름 + 이메일 → 고객 + 남은 시술권) · 예약(이름 + 이메일)(§6) | D-11 |
| I4 | 연동처별 API 키 인증 · 호출 기록 · 호출 제한(§7) | D-23 · D-24 · D-25 · D-34 |
| I5 | Swagger 에 외부 API 를 따로 tag 와 securityScheme 으로 싣는다(§8) | 코드 규약: `app/openapi_docs.py:98-159` |
| I6 | (0.3.0) 외부 연동 API 셋 더함: 예약 가능 시간대 · 고객 과거 시술 · 고객 예약 내역(§6.6 ~ §6.9) | DEC-011 D-01 · D-07 |

### 1.2 Out — 하지 않는 것

| # | 무엇 | 근거 |
|---|---|---|
| O1 | 화면(front · app) — 메뉴 · 외부 연동 화면 없음 | D-01 |
| O2 | 고객이 산 것(수납 · 시술권)의 ccc DB 저장. 남은 시술권은 조회 때마다 KOS 에서 읽는다 | D-12 |
| O3 | 다 쓴 시술권 · 취소된 시술권 · 시술권 그룹 통계 응답 | D-12 |
| O4 | 외부 메뉴 응답의 진료항목 · 기기 · 약물 객체, 공급가 · 부가세 · 면세 · 과세 유형 · 특별가 · 프로모션(이것들은 DB 에만 있다) | D-27 · D-30 |
| O5 | 고객 조회 응답의 전화 · 생년월일 · 국적 · 여권 · 차트번호 · 이메일 | D-13 · D-31 |
| O6 | email 이 빈 기존 고객을 보조 키(전화 · 생년월일)로 찾는 것 | D-22 |
| O7 | 이름 띄어쓰기 · 순서를 바꿔 다시 검색하는 것 | D-17 |
| O8 | 외부에서 예약 그룹 · 구역 · 담당자를 받는 것 | D-33 |
| O9 | KOS Webhook(`PRODUCT_*`) 받기 · 빈 검색어 `searchProductOptionSummaries` 호출 | D-05 · D-06 |
| O10 | 협업자 admin 계정 회수 — 언제 할지는 사용자가 정한다. 이 문서는 회수를 권한다고만 적는다(§7.6) | D-26 |
| O11 | 직원 API 의 동작 · 응답 변경(직원 고객 검색 `search()` 의 `countInPage:20` 도 그대로 둔다 — D-16 은 외부 조회에만 걸린다) | D-10 · D-16 |

---

## 2. 폴더 · env

### 2.1 폴더 — `procedure/back/` 안에 더한다(코드 레포 `kknaksss/cc-prototype`)

| 자리 | 무엇 | 근거 |
|---|---|---|
| `app/repository/db.py` | `MENU_SCHEMA`(§3.2 메뉴 표 9) · `EXT_SCHEMA`(§3.4 `ext_call`)를 지금 `SCHEMA` · `RESV_SCHEMA` 와 같은 방식(`CREATE TABLE IF NOT EXISTS` + `Database.__init__` 의 `executescript`)으로 더한다 | 코드 규약: `app/repository/db.py:96-149` · `:256-261` |
| `app/repository/repo.py` | 메뉴 upsert · 「없음」 표시 · 메뉴 트리 읽기 · `ext_call` 쓰기 함수 | 코드 규약: `app/repository/repo.py:272` · `:476-480` |
| `app/kos/menu_sync.py`(새) | 메뉴 동기화(§4.1) | 코드 규약: `app/kos/reservation_sync.py:177-190` |
| `app/kos/runtime.py` | `master_once()` 에서 메뉴 동기화 1번 호출 | 코드 규약: `app/kos/runtime.py:53-62` |
| `app/service/ext.py`(새) | 외부 API 서비스 — 메뉴 응답 조립 · 고객 조회(§5) · 예약(지금 `ReservationService.create()` 재사용) | D-11 · 코드 규약: `app/service/reservations.py:773` |
| `app/service/reservations.py` | 행위자 문자열 겹(§3.5) — `create()` · `_new_visitor()` · `kos_write()` · `_event()` 의 `actor` 가 `Account` 또는 행위자 문자열을 받고, `_event` 가 문자열은 그대로 · `Account` 는 `login_id` 로 적는다. 부르는 곳은 고치지 않는다. 그 밖 동작은 바꾸지 않는다 | D-11 · D-24 · 코드 규약: `app/service/reservations.py:478-479` · `:709-720` · `:773` · `:890` |
| `app/api/ext.py`(새) | 라우터 `prefix="/api/ext"` · 의존성 `require_ext_key` | D-10 · 코드 규약: `app/api/public_questionnaire.py:17-18` |
| `app/schemas/ext.py`(새) | 요청 · 응답 모델(모든 칸 `description` · 요청은 모르는 키 400) | 코드 규약: `app/schemas/reservations.py:696-722` · `tests/test_openapi_docs.py:63-68` |
| `app/domain/errors.py` | `ServiceUnavailable`(status 503) 1개 더함(§6.5 `ext_not_configured`) | 코디 Q3 · 코드 규약: `app/domain/errors.py:4-47` |
| `app/config.py` | env 3개(§2.2) | 코드 규약: `app/config.py:13-31` |
| `app/main.py` | 라우터 등록 · `/api/ext` 미들웨어(IP 차단 §7.3 · `ext_call` 쓰기 §7.4 · `Cache-Control: no-store`) | 코드 규약: `app/main.py:104-111` · `:128-129` |
| `app/openapi_docs.py` · `app/api/docs.py` | tag `외부 연동` · securityScheme `ExtApiKey` · 앱 설명 절 · `STATUS_TEXT` 503(§8) | 코드 규약: `app/openapi_docs.py:98-159` · `app/api/docs.py:42-47` |
| `tests/test_ext_*.py`(새) · `tests/test_openapi_docs.py`(개수 단언 고침) | §9 | 코드 규약: `tests/` 구성 |
| (0.3.0 · add1) `app/api/ext.py` · `app/service/ext.py` · `app/schemas/ext.py` · `app/kos/reservation_sync.py` · `app/openapi_docs.py` · `tests/test_ext_*.py` · `tests/test_openapi_docs.py` | 경로 셋 · 서비스(가능 시간대 · 과거 시술 · 예약 내역) · 응답 모델 · `ResvSync.refresh_slots(day)`(지금 `_slots` 를 부르는 공개 함수 하나 · 동작 무변경) · 앱 설명 · 시험. 직원 서비스(`reservations.py`) · `reservation_rules.py` 는 **고치지 않고** 함수만 가져다 쓴다(`open_spans` · `is_full` · `schedule_start` · `PREV_RESULT` · `state_of` · `resources_of` · `reservation_id_of`) | DEC-011 · §6.6 ~ §6.8 |

### 2.2 env 더함 — **이름만**(값은 레포 밖 `.env` · 클러스터 Secret)

| env | 뜻 | 비면 | 근거 |
|---|---|---|---|
| `PROC_EXT_KEY_LINKY` | 링키 연동처 API 키 | 그 연동처는 꺼진다. 어떤 키도 링키로 인정되지 않는다 | D-23 · 코드 규약: `app/config.py:59`(`PROC_SESSION_SECRET` 같은 서버 비밀 = `PROC_` 접두) · `:30-31`(비면 끈다) |
| `PROC_EXT_KEY_CHARTY` | 차티 연동처 API 키 | 위와 같음 | D-23 · 위와 같음 |
| `KOS_EXT_RESERVATION_GROUP_ID` | 외부 예약이 들어갈 KOS 예약 그룹 id(하나) | 외부 예약만 `503 ext_not_configured`. 조회 · 메뉴는 그대로 | D-33 · 코디 Q3 · 코드 규약: `app/config.py:24` · `:31`(KOS id 설정 = `KOS_` 접두) |

- 키를 바꾸거나 끄는 것은 이 env 를 바꿔 배포하는 것으로 한다(D-23). 키 값은 로그 · 응답 · `ext_call` 에 싣지 않는다(§7.1).
- **값을 두는 곳**: 세 env 모두 지금 `KOS_ZONE_ID` 와 같은 길을 탄다 — infra 레포(private) `provisioning/secrets/cc-prototype-prod.env.example` 에 **이름만 빈 값으로** 한 줄씩 더하고, 값은 클러스터 Secret `cc-prototype-secret` 에만 넣는다(로컬은 gitignore `.env`). infra · profile · 코드 레포 어디에도 키 · KOS id **값은 0** 이다(근거: infra `origin/main` 의 그 파일 25행 `KOS_ZONE_ID=` · `deploy.md` ② 「새 env 는 sync 전에 Secret — 값은 레포 밖」)

---

## 3. 데이터 모델 (D-03 · D-04 · D-07 · D-24)

### 3.1 원칙

- 메뉴 표는 모두 **조회 칸 + `raw`(KOS 원본 객체 JSON 문자열)** 로 이뤄진다. 표에 칸으로 뽑지 않은 값(다국어 · 가격 세부 · 상태 · deprecated 칸)도 `raw` 에 남는다(D-03 · D-04). `raw` 는 KOS 가 준 객체를 **고치지 않고** `json.dumps` 한 것이다(키 순서 · 빈 값 · deprecated 칸을 보존한다)
- 시각 = UTC ISO 문자열 · json 열 = 문자열(D-04 · 코드 규약: `app/repository/db.py:1`)
- KOS 에서 오는 행은 `kos_id`(UNIQUE)로 맞춰 **덮어쓴다**. KOS 에 id 가 없는 것(구성 · 타겟 국가)은 §3.2 에 적은 키로 맞춘다(코드 규약: `app/repository/db.py:100` · `:120-124` 복합 키 `reservation_slot`)
- **「없음」 표시(D-07)**: 이번 동기화 결과에 없는 행은 지우지 않고 `present = 0` 으로 둔다. 다시 나오면 `present = 1` 로 되살린다(코드 규약: `app/repository/repo.py:476-480` `mark_absent_kos` · 되살림 = upsert 칸에 `present: True` 를 넣는 `app/kos/reservation_sync.py:200-201` 선례). `mark_absent_kos` 는 `kos_id` 로 견주므로 `kos_id` 가 없는 `menu_composition`(복합 키 `option_kos_id` · `seq`) · `menu_target_country`(`raw` 키)에는 그대로 쓸 수 없다 — 그 두 표는 「이번 결과에 없는 행 = `present = 0`」을 자기 키로 하는 함수를 따로 둔다. KOS 가 행을 주면서 삭제 · 숨김 · 닫힘 표시를 단 경우(`deleted` · `opened:false` · `closed:true`)에는 행은 `present = 1` 로 두고 그 표시 칸만 저장한다. 외부 응답에서는 두 경우 모두 빠진다(§6.3)
- 동기화가 실패한 작업은 그 표를 건드리지 않는다. 이전 값과 `present` 가 그대로 남는다(§4.1)
- 고객이 산 것(수납 · 시술권)은 저장하지 않는다(D-12). 고객 조회가 찾은 고객은 지금 `customer` 사본에 덮어쓴다(이름 · 발음 · 국적 · 신규 여부 · 차트번호 · 성별). email 은 저장하지 않는다(코드 규약: `app/kos/reservation_sync.py:143-151` `upsert_customer` · SPEC-005 §3.1 「저장하는 개인정보」)

### 3.2 메뉴 표 (`MENU_SCHEMA`)

모든 표에 `id INTEGER PRIMARY KEY` · `raw TEXT NOT NULL` · `present INTEGER NOT NULL DEFAULT 1` · `synced_at TEXT` 가 있다. 아래 표에는 그 밖의 칸만 적는다.

| 표 | 맞추는 키 | 조회 칸 | 원천(§4.1) | 근거 |
|---|---|---|---|---|
| `menu_category` | `kos_id` UNIQUE | `name` · `"order"` · `opened`(0/1) · `deleted`(0/1) | `getCategories` `data[]` | R1 §1.6 |
| `menu_product` | `kos_id` UNIQUE | `title` · `is_event`(0/1) · `closed`(0/1) · `deleted`(0/1) · `seq`(`getProducts` 배열 순서 0..) · `category_kos_ids`(json `[..]` — `categories[].id`) | `getProducts` `data[]`(`raw` 에서 `options[]` 는 **빼고** 둔다 — 옵션은 `menu_option.raw` 에 있다) | R1 §1.2 · R1 §4 「정렬」 |
| `menu_option` | `kos_id` UNIQUE | `product_kos_id` · `seq`(그 상품 `options[]` 순서) · `type`(`SINGLE` · `GROUP` · `CONSULTATION` 그대로) · `title` · `deleted`(0/1) · `list_price`(`price.amount.value` 정수 · 없으면 null) · `currency`(`price.amount.currency` · 없으면 null) · `count`(SINGLE 만 · 그 밖 null) · `procedure_kos_id`(SINGLE `procedure.id` · 그 밖 null) · `medical_service_kos_id`(SINGLE 만 — §4.1 ③ `getProductOptions` 로 채움 · 그 밖 null) | `getProducts` `data[].options[]`(`raw` 에서 `compositions[]` 는 빼고 둔다) | R1 §1.1 `Option` · D-28 · D-09 · 코디 Q4 |
| `menu_composition` | (`option_kos_id`, `seq`) UNIQUE — KOS 구성에는 id 가 없다(R1 §2.1) | `title` · `count` · `unit_type` · `unit_value` · `list_price` · `currency` · `procedure_kos_id` · `medical_service_kos_id` | `getProducts` GROUP `options[].compositions[]` | R1 §1.1 `Composition` · R1 §2.1 「2 → 3」 |
| `menu_procedure` | `kos_id` UNIQUE | `name` | `getProcedures` `data[]` | R1 §1.7 |
| `menu_medical_service` | `kos_id` UNIQUE | `title` · `status` · `code`(`configuration.code`) · `procedure_kos_id`(`configuration.procedure.id`) · `unit_type` · `unit_value`(`configuration.unit` · 없으면 null) | `getMedicalServices` `data[]` | R1 §1.1 `MedicalService` · R1 §1.8 |
| `menu_machine` | `kos_id` UNIQUE | `name` | `getMachines` `data[]` | R1 §1.7 |
| `menu_medicine` | `kos_id` UNIQUE | `name` | `getMedicines` `data[]` | R1 §1.7 |
| `menu_target_country` | `raw` UNIQUE — id 가 없고 같은 `code` 가 두 번 온다(R1 §1.9 · §7-9). 객체 전체가 곧 행이다 | `code` · `"order"` | `getTargetCountries` `data[]` | R1 §1.9 |

- `getProducts` 의 상품 · 옵션 · 구성은 한 응답에서 함께 오므로 **한 트랜잭션**으로 반영한다. 상품이 빠지면 그 아래 옵션 · 구성도 이번 결과에 없으므로 같이 `present = 0` 이 된다
- 구성은 옵션마다 `seq` 0.. 로 맞춘다. 옵션의 구성이 줄면 남는 `seq` 행이 `present = 0` 이 된다
- 기기 · 약물 연결(`medicineAndMachines[]`)은 표 칸으로 뽑지 않고 옵션 · 구성의 `raw` 에 둔다. 이 배열은 기기와 약물을 섞어서 담고, 원소에 종류 칸이 없다(R1 §2.1). 외부 응답에도 나가지 않는다(D-27)
- 인덱스: `menu_option(product_kos_id)` · `menu_composition(option_kos_id)`(트리 읽기용 · 코드 규약: `app/repository/db.py:82` · `:119`)

### 3.3 KOS 필드 대응 (메뉴 응답에 쓰는 것)

| 외부 응답 칸(§6.3) | ccc | KOS | 근거 |
|---|---|---|---|
| 카테고리 `id` · `name` · `order` · `translsMap` | `menu_category.kos_id` · `name` · `order` · `raw.translsMap` | `getCategories` `data[].id` · `name` · `order` · `translsMap` | R1 §1.6 · D-29 · 코디 Q2 |
| 상품 `id` · `title` · `description` · `isEvent` · `translsMap` | `menu_product.kos_id` · `title` · `raw.description` · `is_event` · `raw.translsMap` | `getProducts` `data[]` 같은 이름 | R1 §1.2 · D-29 · 코디 Q5 |
| 옵션 `id` · `type` · `title` · `description` · `translsMap` | `menu_option.kos_id` · `type` · `title` · `raw.description` · `raw.translsMap` | `options[]` 같은 이름 | R1 §1.1 · D-28 · D-29 |
| 옵션 · 구성 `listPriceExVat` | `list_price` · `currency` | `price.amount{value, currency}`(정가 · 부가세 별도) | D-09 · D-30 · R1 §3 · R2 §1.2 |
| 옵션 · 구성 `count` | `menu_option.count` · `menu_composition.count` | SINGLE `count` · 구성 `count` | R1 §1.1 · 코디 Q5 |
| 옵션 `unit`(SINGLE) | `menu_medical_service.unit_type` · `unit_value`(`menu_option.medical_service_kos_id` 로 이음) | 진료항목 `configuration.unit{type, value}` | R1 §2.2(옵션 `unit` 은 0/307 · 단위는 진료항목에 있다) · 코디 Q4 · Q5 |
| 구성 `unit` | `menu_composition.unit_type` · `unit_value` | 구성 `unit{type, value}` | R1 §1.1 · 코디 Q5 |
| `procedure{id, name}` | 옵션 · 구성 `raw.procedure.id` · `.name` | SINGLE `procedure` · 구성 `procedure` | D-27 · R1 §1.1 |

### 3.4 외부 호출 기록 표 (`EXT_SCHEMA` · D-24)

| 표 | 칸 | 근거 |
|---|---|---|
| `ext_call`(쌓기만) | `id INTEGER PRIMARY KEY` · `at TEXT NOT NULL`(UTC ISO) · `client TEXT`(`linky` \| `charty` \| null) · `endpoint TEXT NOT NULL`(`<METHOD> <경로 틀>` — 예 `POST /api/ext/customers/lookup`) · `status INTEGER NOT NULL`(HTTP 상태) · `outcome TEXT NOT NULL`(성공 = `ok`, 오류 = §6 의 오류 `code` 그대로) | D-24 · 코드 규약: `app/repository/db.py:71-74`(`event_log` · 쌓기만) · `:152-163`(`push_log` 내역 표) |

- **누가 쓰나**: `/api/ext` 미들웨어가 응답을 낸 뒤 쓴다(401 · 없는 경로 404 · JSON 이 아닌 본문 400 은 라우터 의존성이 돌기 전에 끝나므로 의존성에서는 쓸 수 없다 — 코드 규약: `app/main.py:104-111` 미들웨어 선례 · `:117-125`)
- **`client`** = `require_ext_key` 가 키를 맞힌 뒤 `request.state` 에 남긴 연동처 이름. 남긴 값이 없으면(키 없음 · 틀림 · 의존성 전에 끝난 요청) **null**. 미들웨어는 키를 다시 견주지 않는다
- **`endpoint`** = 매칭된 라우트의 경로 틀(`path_format`). 매칭된 라우트가 없으면(없는 경로) **고정값 `"<METHOD> (unknown)"`**(예 `GET (unknown)`) — 실제 경로를 적지 않는다. 경로에 실린 이름 · 이메일 원문이 표에 남지 않게 하기 위해서다(D-24)
- **키 없는 거절**(정의 — §7.3 · §7.4 도 이 뜻): `client` 가 null 인 모든 `/api/ext` 오류 응답 — 401 · 없는 경로 404 · 깨진 본문 400 · 405 · IP 차단 429. 처리하지 못한 예외의 `500 internal_error` 는 서버 쪽 잘못이라 들어가지 않는다(§7.4). 라우터 밖 처리기에서 끝나는 400 · 405 도 들어간다(코드 규약: `app/main.py:117-125` — `RequestValidationError` · `StarletteHTTPException` 처리기). 401 · 404 만 고르지 않는다
- **줄이기**: 키 없는 거절은 **같은 IP · 같은 `outcome` 이면 1분에 1줄**만 쓴다. IP 는 이 판단의 메모리 키로만 쓰고 표 · 로그에 남기지 않는다(코드 규약: `app/service/questionnaire.py:108` · `:271-282` `_deny` — 「같은 IP 같은 이유는 1분에 1행 · IP 는 남기지 않음」)

- **싣지 않는 것**: 요청 이름 · 이메일 원문, 키 값, 고객 · 예약 id, KOS 응답 본문(D-24). 고객 · 예약 결과는 기존 `customer` · `reservation` · `event_log` 가 이미 갖는다
- 인덱스 `ext_call(at)`. 보존 기간은 정하지 않는다 — 지금 `event_log` · `push_log` 처럼 쌓기만 한다(코드 규약: `app/repository/db.py:153`)

### 3.5 `event_log` (지금 표 그대로)

- 외부 예약이 지금 `create()` 를 다시 쓰므로 지금 `resv_create` · `kos_rejected` 줄이 그대로 남는다(SPEC-005 §3.2). 그때 `event_log.actor` 는 직원 `login_id` 대신 **`ext:<연동처>`**(`ext:linky` · `ext:charty`)다(코드 규약: `app/service/reservations.py:709-720` · `app/repository/db.py:72` `actor TEXT`). 새 `type` 은 없다
- **넘기는 법 — 행위자 문자열 겹(하나로 정함)**: `create()` · `_new_visitor()` · `kos_write()` · `_event()` 는 지금 `Account` 를 받지만, 그 안에서 쓰는 것은 `actor.login_id` 하나뿐이다(`_event` → `tx.add_event(…, actor.login_id, …)` · 코드 규약: `app/service/reservations.py:478-479`. `create` · `_new_visitor` · `kos_write` 는 `actor` 를 아래로 넘기기만 한다 — `:709-720` · `:773-851` · `:890-924`). 그래서 이 네 함수의 `actor` 타입을 **`Account | str`** 로 넓히고, `_event` 한 곳에서만 「문자열이면 그대로 · `Account` 면 `login_id`」로 적는다. 외부 서비스는 `"ext:<연동처>"` 문자열을 넘긴다. 가짜 `Account` 를 만들지 않는다
- **이 방식을 고른 근거(더 작은 쪽)**: 네 함수를 「문자열만 받기」로 바꾸면 `kos_write` · `_event` 를 부르는 직원 쪽 30여 곳(`app/service/reservations.py` 안 · `app/service/reception.py:67` · `:183` · `:205` · `:222-225` · `:239-242` · `:260-263` · `app/api/reservations.py:224`)을 모두 `actor.login_id` 로 고쳐야 한다. 타입을 넓히면 부르는 곳은 한 줄도 바뀌지 않고, 직원 `event_log.actor` 값은 지금과 **같다**(`Account` → `login_id` 그대로). 문자열 actor 를 바로 적는 선례 = `app/service/questionnaire.py:38` · `:282`(`ACTOR = "customer"`). 시험 T17(외부 = `ext:linky`) · T30(직원 값 그대로)이 고정한다

---

## 4. KOS 연동

### 4.1 메뉴 동기화 (D-05 · D-06 · D-07 · 코디 Q4)

**언제**: `KosRuntime.master_once()` 안, 지금 예약 목록(`resv.master()`) 다음에 1번 부른다. 서버 시작 때 1회(`startup()` → `master_once(force=True)`), 그 뒤 `KOS_POLL_MASTER_SEC`(기본 3600초)마다 돈다. 예약 목록처럼 **조회 시간(09:00 ~ 21:00)과 상관없이** 돈다(D-06 · 코드 규약: `app/kos/runtime.py:45-62` · `:107-109`). Webhook 은 받지 않는다(D-06).

**작업 순서**(내부 = 없음 · 모두 **공개** API, `KosClient.open` · 코드 규약: `app/kos/client.py:179-180`):

| # | 작업 | 공개 경로 | 본문 | 반영 표 | 근거 |
|---|---|---|---|---|---|
| ① | `getCategories` | `product/open/v1/queries/get-categories` | `{}` | `menu_category` | D-05 · R1 §1.6 |
| ② | `getProducts` | `product/open/v1/queries/get-products` | `{}`(필터 없음 · 페이징 없음) | `menu_product` · `menu_option` · `menu_composition`(한 트랜잭션) | D-05 · R1 §1.2 · §4 「페이징」 |
| ③ | `getProductOptions` | `product/open/v1/queries/get-product-options` | `{optionIds:[②의 SINGLE 옵션 kos_id], includePromotions:false}` — **N개씩 나눠 부른다**(N = 구현 때 데모에서 실측해 정하고 코드 상수 + WORK 리포트에 적는다. KOS 문서에 개수 상한이 있으면 그 값을 따른다 · R1 §1.4 「옵션 4개 = 8KB」) | `menu_option.medical_service_kos_id` 만(응답 `data[].medicalService.id`). 진료항목 본문은 ⑤ 행에 있다 | D-05 · 코디 Q4 · R1 §1.4 · §7-1 |
| ④ | `getProcedures` | `product/open/v1/queries/get-procedures` | `{}` | `menu_procedure` | D-05 · R1 §1.7 |
| ⑤ | `getMedicalServices` | `product/open/v1/queries/get-medical-services` | `{}` | `menu_medical_service` | D-05 · R1 §1.8 |
| ⑥ | `getMachines` | `product/open/v1/queries/get-machines` | `{}` | `menu_machine` | D-05 · R1 §1.7 |
| ⑦ | `getMedicines` | `product/open/v1/queries/get-medicines` | `{}` | `menu_medicine` | D-05 · R1 §1.7 |
| ⑧ | `getTargetCountries` | `target-country/open/v1/queries/get-target-countries` | `{}` | `menu_target_country` | D-05 · R1 §1.9 |

- **경로 문자열은 구현 때 KOS `openapi.yaml`(1.0.1)의 operationId 에서 옮긴다.** 위 경로 칸은 지금 공개 경로 모양(`<영역>/open/v1/queries/<동작>` — KDA 표 · 코드 규약: `app/kos/reservation_sync.py:24` · `:29-31`)으로 적은 것이다. 스펙의 경로와 다르면 **스펙이 맞다**. WP-BE1 리포트에 실제 경로를 적는다
- **부르지 않는 것**: 빈 검색어 `searchProductOptionSummaries`(D-05 · R1 §1.5 가이드 권고) · `getProduct` 단건(②가 같은 값 · R1 §1.3)
- ③ 은 ② 가 성공했을 때만 부른다. ③ 응답에서 빠진 옵션(KOS 가 「삭제 · 사용 중지 · 없는 id」를 뺀다 — R1 §1.4)은 `medical_service_kos_id` 를 **바꾸지 않는다**(이전 값 그대로). 나머지 작업은 서로 독립이다
- **실패**(네트워크 · 5xx · 401 재시도 뒤 · 2xx 인데 `data` 가 배열 아님): 그 작업이 반영하는 표는 **건드리지 않는다**(이전 값 · `present` 그대로). 다른 작업은 계속한다. 하나라도 실패하면 `sync_state("menu")` 의 `last_error` 에 `"<작업 이름>: <오류>"` 를 `; ` 로 이어 적고, 다 성공하면 `last_ok_at` 을 찍는다. **하나라도 실패한 바퀴는 `last_ok_at` 을 지우지 않는다 — 이전 값을 그대로 두고 `last_error` 만 바꾼다**(`set_sync("menu", None, <오류>)` 는 `ok_at or prev_ok` 로 이전 값을 남긴다 · 코드 규약: `app/repository/repo.py:452-455`. `syncedAt` 이 「언제 받은 메뉴인가」를 계속 알려 주게 하기 위해서다 — D-36). 로그에는 예외 종류 · HTTP 상태만 남긴다(본문 · 키 없음)(코드 규약: `app/kos/reservation_sync.py:35-43` `_err` · `_data_list` · `:177-190` `master()` · `app/kos/sync.py:158-169`)
- 작업마다 `present` 맞추기: 그 작업이 성공했을 때만, 이번 결과에 없는 행을 `present = 0` 으로 둔다(코드 규약: `app/kos/reservation_sync.py:192-202` `_zones` · `mark_absent_kos`)
- 동시에 두 번 돌지 않게 잠금 하나를 둔다(코드 규약: `app/kos/reservation_sync.py:173` `_master_lock`)
- 크기 · 시간: 한 바퀴에 약 0.9MB 와 ③ 정도이고, 각 작업은 0.03 ~ 0.8초다(R1 §6). 1시간 주기면 부담이 없다

### 4.2 고객 이름 검색 (D-15 · D-16 · D-17)

| 항목 | 계약 | 근거 |
|---|---|---|
| 작업 | **내부** `visitor/v2/queries/get-visitors`(지금 `PATH_VISITORS`) · `KosClient.internal`(시스템 계정 토큰 · 브라우저 UA) | D-15 · 코드 규약: `app/service/reservations.py:78` · `app/kos/client.py:10-11` · `:182-185` |
| 본문 | `{indexOfPage: 0, countInPage: 1000, visitorName: <다듬은 이름>, phoneNumber: "", chartNumber: "", sort: {by: "lastVisitedDateTimeUtc", order: "DESC"}}` | D-16 · 코드 규약: `app/service/reservations.py:448-450`(같은 본문 · 페이지 크기만 다름) · R4 §2.1(`countInPage` 100 · 500 · 1000 · 5000 모두 200) |
| 한 페이지만 | 조회 1건당 `get-visitors` **1번**. 다음 페이지를 부르지 않는다 | D-16 |
| 상한 | 응답 `count` 가 1000 을 넘으면 받은 결과를 **거르지 않고** §5 갈래 「없음」(`404 customer_not_found` — D-21 과 같은 바이트)으로 끝낸다. 시술권 조회도 하지 않는다 | D-16 · D-21 |
| 중복 제거 | 받은 `data[]` 를 KOS `id` 로 중복 제거한 뒤(처음 나온 것을 남김) §5 로 거른다 | D-16 |
| 이름 | 보낼 때는 앞뒤 공백만 지운다(`strip()`). 가운데 공백 · 순서는 그대로다. 다시 검색하지 않는다. 받은 뒤의 이름 정확 일치는 §5 3단계다 | D-17 · R4 §2.1 「이름 검색 시험」 |
| 응답에서 쓰는 칸 | `count`(상한) · `data[].id`(중복 제거) · `name` · `phoneticName`(이름 대조 · 사본) · `nationality` · `isNew` · `chartNumber` · `gender`(사본 덮어쓰기) · `email`(거르기에만 · 저장 안 함) · `lastVisitedDateTimeUtc`(최근 방문일) | D-16 · D-19 · R4 §0 #1 · 코드 규약: `app/kos/reservation_sync.py:143-151` |
| 실패 | KOS 호출 실패 = `502 kos_unavailable`. **2xx 인데 `data` 가 배열이 아님(키가 없는 경우 포함) = `502 kos_unavailable`** — 「0명」으로 보지 않는다. 그래서 조회는 404 가 아니라 502 이고, 예약은 새 고객을 만들지 않는다(`create-visitor` 0번) | D-14 · D-15 · 코드 규약: `app/service/reservations.py:454-458`(지금 검색 실패 = `502 kos_unavailable`) · `app/kos/reservation_sync.py:39-43` `_data_list`(같은 규칙) · 코드 검수 r1 W1 |

- `lastVisitedDateTimeUtc` 는 지금 코드가 정렬 키로 보내는 이름이다. 목록 원소에 이 칸이 실제로 오는지는 조사 4 가 키 목록을 적지 않아 **확인하지 않았다**. WP-BE4 의 데모 확인 1회로 확인한다(WORK-012). 키가 없거나 빈 값이면 응답 `lastVisitDate = null` 이다(지어 채우지 않는다)

### 4.3 남은 시술권 (D-12 · D-08 · D-31)

| 항목 | 계약 | 근거 |
|---|---|---|
| 작업 | **공개** `getTicketBundlesQuery` — `ticket/open/v1/queries/get-ticket-bundles` · 본문 `{visitorId: <KOS 고객 id>}` · 고객 1명당 1번 | D-12 · KDA 76행 · R4 §1 ③ |
| 언제 | 고객 조회(§6.4)에서 1명이 맞았을 때만, 매 조회마다 부른다. 캐시 · 저장은 없다 | D-12 |
| 결과 없음 | 응답이 `{}`(`data` 키 없음)이거나 `data: []` 이면 → 「남은 시술권 없음」(`tickets: []`) | KDA 182행 · R2 §3.2 · D-14 |
| 모양 오류 | 2xx 인데 `data` 가 있으면서 배열이 아니면 → `502 kos_unavailable` | 코드 규약: `app/kos/reservation_sync.py:39-43` |
| 실패 | 네트워크 · 5xx · 4xx · 401 재시도 뒤 = `502 kos_unavailable`(고객 칸만 주고 시술권을 빈 배열로 주지 않는다 — 「시술권 없음」과 섞이면 D-14 가 깨진다) | D-14 · 코드 규약: `app/service/kos_errors.py:6` |

묶음(`data[]` 원소) → 응답 한 줄(§6.4 `tickets[]`): 모양은 KDA 258행 · HAR(`reference/2026-11-11-cc-product/har/` 내부 `get-ticket-bundles`, 키만)을 따른다.

| 응답 칸 | KOS | 규칙 | 근거 |
|---|---|---|---|
| `optionId` | `optionConfiguration.optionId` | 그대로(KOS id 문자열). 메뉴에 없는 옵션이어도 그대로 준다 | D-08 · D-31 · 코디 Q2 |
| `optionTitle` | `optionConfiguration.optionTitle` | 그대로(산 시점 값). 메뉴 이름으로 덮지 않는다 | D-08 · R2 §1.3 · R3 §0 |
| `remainingCount` | `ticketSets[].tickets[].status` | 묶음 안 모든 세트의 `AVAILABLE` 장수 합. `IN_USE`(쓰는 중) · `USED` · `CANCELED` 는 넣지 않는다 | D-31 · R2 §3.2 |
| `totalCount` | `ticketSets[].tickets[]` | 묶음 안 모든 세트의 시술권 장수 합(상태 무관) | D-31 · R2 §3.3 |
| `purchasedDate` | `ticketSets[].tickets[].createdDateTimeUtc` | 그중 가장 이른 값의 KST 날짜 `YYYY-MM-DD`. 시술권은 수납이 끝날 때 만들어진다. 값이 없으면 null | D-31 · R2 §2(「발행 일시(수납 완료로 티켓그룹 생성)」) |
| `bundlePrice` | `price{value, currency}` | **KOS 묶음 가격 그대로**. `value` 는 정수로 바꿔 준다(원 단위). 칸 이름에 `purchase` · `VatIncluded` 를 넣지 않는다 | D-08 · D-31 · R2 §0(연결 그림) · §3.3 |

- KOS 그대로의 성질을 Swagger 설명에도 적는다(지어 바꾸지 않는다 · D-08 · D-31). ① `bundlePrice` 는 **고객이 낸 돈이 아니다**. 산 시점 값에서 출발하지만, GROUP 묶음에서 한 세트를 다 쓰면 그 세트가 응답에서 빠지므로 `totalCount` 와 함께 줄 수 있다(R2 §3.3 확인 1건). **부가세 포함 여부는 표기하지 않는다**. ② `AVAILABLE` 이 0장인 묶음은 KOS 가 주지 않는다(R2 §2). ③ `remainingCount` 는 `AVAILABLE` 만 센다 — `IN_USE`(쓰는 중)는 남은 장수에 넣지 않는다
- 순서 = KOS 배열 순서

---

## 5. 조회 규칙 — 이름 + 이메일 (D-15 ~ D-22)

고객 조회(§6.4)와 예약(§6.5)이 **같은 함수**로 고객을 정한다(D-32).

| 단계 | 규칙 | 근거 |
|---|---|---|
| 0. 입력 | 요청 `name` · `email` 은 둘 다 필수다. 앞뒤 공백을 지운 뒤 비면 `400 invalid_request` 이다 | D-11 · D-32 · 코드 규약: `app/main.py:117-121` |
| 1. 검색 | `name.strip()` 으로 §4.2 를 **한 번** 부른다. `count` > 1000 이면 여기서 「없음」 | D-16 · D-17 |
| 2. 중복 제거 | KOS `id` 로 중복 제거 | D-16 |
| 3. 이름 정확 일치 | 입력 이름과 KOS `name` · `phoneticName` 을 각각 **공백을 전부 지우고**(가운데 공백 포함) 대소문자를 무시해(`lower()` — 4단계 이메일과 같은 방식) 견준다. 둘 중 하나라도 **정확히 같은** 고객만 남긴다. 부분 일치로만 걸려 온 고객은 빠진다. KOS 쪽 값이 없거나 비면 그 칸은 맞지 않은 것으로 본다 | D-19 · R4 §2.1 |
| 4. 이메일 정규화 | 입력과 KOS `email` 양쪽 모두 `strip().lower()`. KOS 쪽에 키가 없거나 빈 문자열이면 그 고객은 후보에서 뺀다. 형식 검사(`@` 유무 등)는 하지 않는다 — 같으냐만 본다 | D-18 · R4 §2.2 |
| 5. 이메일 대조 | 정규화한 값이 **정확히 같은** 고객만 남긴다 | D-18 |
| 6. 갈래 | **0명** → 「없음」 · **1명** → 그 고객 · **2명 이상** → 「특정할 수 없음」(아무도 돌려주지 않음) | D-20 · D-21 |

- 「없음」은 이름이 틀린 경우(부분 일치만 맞는 경우 포함) · 이메일이 틀린 경우 · 고객이 없는 경우 · KOS 에 그 고객의 email 이 비어 있는 경우 · 이름 검색 `count` 가 1000 을 넘는 경우가 **모두 같은 응답**이다(코드 · 문구 · 칸이 같다). 어느 쪽이 틀렸는지 응답에서 알 수 없다(D-16 · D-21 · D-22)
- 보내는 이름(1단계)은 앞뒤 공백만 지우고, 견주는 이름(3단계)은 공백을 전부 지운다. 서로 다른 단계다 — KOS 에 다시 검색하지 않는다(D-17)
- 「특정할 수 없음」 응답에도 후보 수 · 이름 · id 를 싣지 않는다(D-20 · D-21)
- 1명이 맞으면 그 고객을 `customer` 사본에 덮어쓰고(§3.1) ccc `customerId` 를 얻는다(코드 규약: `app/service/reservations.py:461-466`)

---

## 6. 외부 API (D-10 · D-11 · D-27 ~ D-36 · DEC-011)

### 6.1 공통

| 항목 | 계약 | 근거 |
|---|---|---|
| 경로 | `/api/ext/…` — 직원 API 와 나눈다 | D-10 |
| 인증 | 헤더 `X-Api-Key: <연동처 키>`(§7.1). `Authorization` 은 보지 않는다 | D-10 · D-23 · 코드 규약: `app/api/public_questionnaire.py:1-8` · `app/openapi_docs.py:64-66`(`X-Questionnaire-Token` 선례) |
| 형식 | JSON · 칸 이름 camelCase · 요청에 모르는 키가 있으면 `400 invalid_request` | 코드 규약: `app/openapi_docs.py:54-62` · `app/schemas/reservations.py:696`(`_Req`) |
| 시각 | 요청 `start` = ISO-8601(오프셋이 없으면 KST). 응답 날짜 = KST `YYYY-MM-DD` · 응답 시각 = ISO `+09:00` 초 단위 | 코드 규약: `app/domain/reservation_rules.py:63-69` · `app/openapi_docs.py:60-62` |
| 금액 | `{value: int(원), currency: "KRW"}`. 메뉴 정가는 칸 이름으로 부가세 별도(`…ExVat`)를 밝힌다. 시술권 `bundlePrice` 는 KOS 묶음 가격 그대로이고 부가세 포함 여부를 표기하지 않는다(§4.3) | D-09 · D-30 · D-31 · R1 §1.1 `Money` |
| id | 메뉴 · 시술권의 카테고리 · 상품 · 옵션 · 시술 id = **KOS id 문자열**. 고객 id · 예약 id = **ccc 정수**(직원 API 와 같다). 고객의 KOS id 는 내지 않는다 | 코디 Q2 · D-08 · D-12 |
| 오류 | `{"error": {"code", "message"}}`. 분기는 `code` 로 한다. 외부 API 오류에는 `step` · `candidate` 를 싣지 않는다 | 코드 규약: `app/main.py:66-67` · `:113-125` · `app/api/docs.py:23-37` |
| 캐시 | 모든 `/api/ext` 응답(오류 포함)에 `Cache-Control: no-store` | 코드 규약: `app/main.py:104-111`(공개 경로 선례) |
| 검사 순서 | **키(`401 ext_unauthorized`) → 제한(`429 too_many_requests`) → 칸 검증(`400 invalid_request` — 필수 · 타입 · 모르는 키 · 빈 값) → 엔드포인트 규칙.** 단 ① IP 차단(§7.3 — `429`)은 미들웨어라서 무엇보다 먼저다. ② JSON 이 아닌 본문(형식이 깨진 JSON)은 FastAPI 가 본문을 읽는 단계에서 끝나므로 **키보다 먼저 `400`** 이다. ③ 없는 경로는 라우터 밖이라 **키 없이 `404 not_found`** 다 | 코드 규약: `app/openapi_docs.py:40`(검사 순서를 문서에 적는 선례) · `app/main.py:117-125` · FastAPI 요청 처리 순서(본문 JSON 읽기 → 의존성 → 칸 검증 오류) · review-doc r1 W6 |

### 6.2 공통 오류 표 (여섯 경로 모두 — 0.3.0 더한 셋 포함 · DEC-011 D-01)

| HTTP | code | 언제 | 근거 |
|---|---|---|---|
| 401 | `ext_unauthorized` | `X-Api-Key` 가 없거나 · 비었거나 · 어느 연동처 키와도 같지 않거나 · 그 연동처 env 가 비어 꺼졌을 때. 직원 Bearer 토큰만 실린 경우도 같다 | D-10 · D-23 · 코드 규약: `tests/test_openapi_docs.py:119-141`(`unauthorized` ↔ `require_login` 단언 — 외부 키는 다른 code 여야 그 시험이 그대로 맞다) |
| 429 | `too_many_requests` | 그 키로 최근 60초 안에 60번을 이미 불렀을 때 · 그 IP 의 키 없는 거절이 최근 60초 안에 10번 이상일 때(§7.3) | D-25 · D-34 · 코드 규약: `app/service/questionnaire.py:243`(같은 code) · `:254` |
| 400 | `invalid_request` | 본문이 JSON 이 아님 · 필수 칸 · 타입 · 모르는 키 · 앞뒤 공백을 지우면 빈 `name` · `email` · ISO 가 아닌 `start` · (가능 시간대) `date` 없음 · 꼴 틀림 · 범위 밖(§6.6) | 코드 규약: `app/main.py:117-121` · `app/domain/reservation_rules.py:63-69` |
| 404 | `not_found` | 없는 `/api/ext/…` 경로 | 코드 규약: `app/main.py:123-125` |
| 405 | `http_error` | 있는 `/api/ext/…` 경로에 틀린 메서드(예 `GET /api/ext/customers/lookup`). 키 검사 전에 끝난다(키 없는 거절 · §3.4) | 코드 규약: `app/main.py:123-125`(404 가 아닌 HTTP 오류 = `http_error`) |
| 500 | `internal_error` | 처리하지 못한 예외(서버 쪽 잘못). `ext_call` 1줄을 쓰고, `client` 가 null 이어도 IP 카운트(§7.3)에는 넣지 않는다 | 코드 검수 r2 N1(미들웨어 `except` 갈래) |

### 6.3 `GET /api/ext/menu` — 메뉴 조회 (D-11 ①)

우리 DB(§3.2)에서만 읽는다. KOS 를 부르지 않는다. 질의 칸은 없다.

**응답 200** `ExtMenu`:

| 칸 | 타입 | 뜻 · null | 근거 |
|---|---|---|---|
| `syncedAt` | string \| null | 메뉴 동기화가 마지막으로 다 성공한 시각(`sync_state("menu").last_ok_at` · ISO `+09:00`). 그 뒤 바퀴에서 작업이 실패해도 **이전 시각이 그대로 남는다**(§4.1). 한 번도 다 성공한 적 없으면 null. 메타 칸 — 언제 받은 메뉴인지 연동처가 알게 한다 | D-36 · 코드 규약: `app/repository/db.py:86-88` · SPEC-005 §4.2(`sync.lastError` 선례) |
| `categories[]` | array | 지금 있는 카테고리. `order` 오름차순 → `id` | D-07 · D-27 |
| `.id` · `.name` · `.order` | string · string · int | KOS 값 | D-29 · 코디 Q2 · Q5 |
| `.translsMap` | object | KOS `translsMap` 그대로. 없으면 `{}` | D-29 |
| `.products[]` | array | 그 카테고리에 속한(`category_kos_ids` 에 그 id 가 있는) 지금 있는 상품. `seq` 순서(KOS 배열 순서). 한 상품이 카테고리 여럿에 걸리면 각 카테고리 아래에 다 나온다 | D-07 · D-27 · R1 §1.2 · §4 |
| `..id` · `..title` · `..description` · `..isEvent` · `..translsMap` | string · string · string · bool · object | KOS 값. `description` 이 없으면 빈 문자열 | D-29 · 코디 Q5 |
| `..options[]` | array | 그 상품의 지금 있는 옵션. `seq` 순서 | D-07 · D-27 |
| `...id` · `...type` | string · `SINGLE` \| `GROUP` \| `CONSULTATION` | KOS 판별자 그대로 | D-28 |
| `...title` · `...description` · `...translsMap` | string · string · object | KOS 값 | D-29 · 코디 Q5 |
| `...listPriceExVat` | `{value, currency}` \| null | **정가 · 부가세 별도**(KOS `price.amount`). CONSULTATION 은 null | D-09 · D-28 · D-30 |
| `...count` | int \| null | SINGLE 의 시술 횟수(KOS `count`). GROUP · CONSULTATION 은 null(GROUP 은 구성마다 있다) | 코디 Q5 · R1 §1.1 |
| `...unit` | `{type, value}` \| null | SINGLE 의 단위 = 이어진 진료항목의 `configuration.unit`(§3.3). 진료항목이 이어지지 않았거나 단위가 없으면 null. GROUP · CONSULTATION 은 null | 코디 Q4 · Q5 · R1 §2.2 |
| `...procedure` | `{id, name}` \| null | SINGLE 의 시술. GROUP · CONSULTATION 은 null. SINGLE 이어도 KOS 가 주지 않으면 null | D-27 · R1 §2.2 |
| `...compositions[]` | array | GROUP 의 구성(지금 있는 것 · `seq` 순서). SINGLE · CONSULTATION 은 `[]` | D-27 · D-28 |
| `....title` · `....count` | string · int \| null | KOS 값. `count` 는 KOS 가 주지 않으면 null | 코디 Q5 |
| `....unit` | `{type, value}` \| null | KOS 구성 `unit` 그대로(`UnitType_UNKNOWN` 도 그대로 준다). KOS 가 주지 않으면 null | 코디 Q5 · R1 §1.1 |
| `....listPriceExVat` | `{value, currency}` \| null | 구성 정가 · 부가세 별도. KOS 가 주지 않으면 null. 구성 정가를 다 더하면 옵션 정가가 된다(R1 §3) | D-30 · 코디 Q5 |
| `....procedure` | `{id, name}` \| null | 구성의 시술. KOS 가 주지 않으면 null | D-27 |

- **단위 `{type, value}` 의 `value`**(옵션 `unit` · 구성 `unit`): KOS 가 주지 않으면 null 이다. 위 표의 「KOS 가 주지 않으면 null」 칸은 모두 지어 채우지 않는다(D-08 · D-29 「KOS 그대로」 · 데모에서는 모두 값이 있었다 · 코드 검수 r1 W7)
- **「지금 있는 것」**(D-07): `present = 1` 이면서 KOS 표시가 살아 있는 것이다. 카테고리는 `opened` 이고 `deleted` 가 아니어야 한다. 상품은 `closed` 도 `deleted` 도 아니어야 한다. 옵션은 `deleted` 가 아니어야 한다. 위 층이 빠지면 아래 층도 나오지 않는다. 지금 있는 카테고리에 하나도 걸리지 않은 상품은 응답에 나오지 않는다
- **내지 않는 칸**(D-27 · D-30 · 코디 Q5): 진료항목 · 기기 · 약물 객체, `medicineAndMachines`, 공급가 · 부가세 · 면세 · 과세 유형 · 특별가(`additional`) · 프로모션, `caution` · `cautions` · 이미지 URL · `displayChannels` · `badges` · `frequentlyUsedOption` · 노출 · 제공 기간 · deprecated 칸. 이 칸들은 DB `raw` 에만 있다
- 오류는 공통 표(§6.2)뿐이다. 메뉴가 비어 있으면(첫 동기화 전 · 실패) `200` 에 `categories: []` · `syncedAt: null` 이다

### 6.4 `POST /api/ext/customers/lookup` — 고객 조회 (D-11 ② · D-12 ~ D-14 · D-31)

이름 · 이메일을 경로나 질의에 싣지 않으려고 `POST` 본문으로 받는다. 접근 로그에 남지 않게 하기 위해서다(D-24 · 코드 규약: `app/api/public_questionnaire.py:6` 「토큰은 경로 · 쿼리에 싣지 않는다(접근 로그)」).

**요청** `ExtLookupRequest`: `{"name": "<이름>", "email": "a@example.com"}` — 둘 다 필수 string.

**처리**: §5 → 1명이면 §4.3 시술권 1번.

**응답 200** `ExtLookupResponse`:

| 칸 | 타입 | 뜻 · null | 근거 |
|---|---|---|---|
| `customer.customerId` | int | ccc 고객 id(직원 API 와 같은 체계) | D-31 · 코디 Q2 |
| `customer.name` | string | KOS 고객 이름 | D-31 |
| `customer.isNew` | bool | KOS `isNew`(신규 여부) | D-31 |
| `customer.lastVisitDate` | string \| null | 최근 방문일 — KOS `lastVisitedDateTimeUtc` 의 KST 날짜 `YYYY-MM-DD`. 없으면 null(§4.2) | D-31 |
| `tickets[]` | array | 남은 시술권(사용 가능한 묶음) 한 줄씩(§4.3 표). **없으면 `[]`** — 「고객은 있는데 남은 시술권 없음」 | D-12 · D-14 · D-31 |
| `tickets[].optionId` · `.optionTitle` | string · string | §4.3 | D-08 · D-31 |
| `tickets[].remainingCount` · `.totalCount` | int · int | §4.3 | D-31 |
| `tickets[].purchasedDate` | string \| null | §4.3 | D-31 |
| `tickets[].bundlePrice` | `{value, currency}` | §4.3 · **KOS 묶음 가격 그대로** — 고객이 낸 돈이 아님 · 산 시점 값에서 출발하지만 세트를 쓰면 줄 수 있음 · 부가세 포함 여부 표기 안 함 | D-31 |

- 응답에 **넣지 않는** 칸: 전화 · 생년월일 · 국적 · 여권 · 차트번호 · 이메일 · KOS 고객 id · 발음 이름 · 성별(D-13 · D-31 · 코디 Q2)

**오류**(§6.2 공통 + 아래):

| HTTP | code | 언제 | 문구(예) | 근거 |
|---|---|---|---|---|
| 404 | `customer_not_found` | §5 갈래 0명(이름 · 이메일이 틀림 · 고객 없음 · email 빈 고객 · 이름 검색 `count` > 1000 모두) | 「일치하는 고객이 없어요」 | D-14 · D-21 · D-22 · 코드 규약: `app/domain/errors.py:27-31`(404 · 코드를 따로 줄 수 있음 — 없는 경로의 `not_found` 와 갈라야 연동처가 「경로 틀림」과 「고객 없음」을 가른다) |
| 409 | `customer_ambiguous` | §5 갈래 2명 이상 | 「고객을 특정할 수 없어요」 | D-20 · 코드 규약: `app/domain/errors.py:34-35` |
| 502 | `kos_unavailable` | 이름 검색 · 시술권 조회 실패(§4.2 · §4.3) | 「KOS 에 연결하지 못했어요」 | 코드 규약: `app/service/kos_errors.py:6` · `:36-39` |

- 문구 칸은 Swagger 설명에 싣는 예다. 연동처는 `code` 로 분기한다(코드 규약: `app/api/docs.py:23-27`)

### 6.5 `POST /api/ext/reservations` — 예약 (D-11 ③ · D-32 · D-33)

**요청** `ExtReservationRequest`:

| 칸 | 타입 | 필수 | 뜻 | 근거 |
|---|---|---|---|---|
| `name` | string | ○ | 고객 이름(§5) | D-32 |
| `email` | string | ○ | 고객 이메일(§5) | D-32 |
| `start` | string | ○ | 시작 시각 ISO-8601(오프셋이 없으면 KST). 끝 = 시작 + 기본 그룹 간격 | D-32 · 코드 규약: `app/schemas/reservations.py:704-705` |
| `memo` | string | — | 예약 메모. 비면 보내지 않는다 | D-32 · 코드 규약: `app/schemas/reservations.py:713` |

그룹 · 구역 · 담당자 · 상담사 · 유입 칸은 **없다**. 보내면 모르는 키라서 `400 invalid_request` 이다(D-33).

**처리**:

1. **기본 그룹**: `KOS_EXT_RESERVATION_GROUP_ID` 가 비었거나, 그 kos_id 의 `reservation_group` 행이 없거나 `present = 0` 이거나, **그 그룹에 켜진 구역이 0 이면** → `503 ext_not_configured`. 모두 사본 기준이고 KOS 를 부르기 전에 막는다. 켜진 구역 0 은 지금 `create()` → `_pick_zone()` 이 `400 invalid_request`(「그 그룹에 켜진 구역이 없어요」)로 내는 경우다 — 연동처 요청과 상관없는 우리 설정 문제라 외부에는 503 으로 낸다(D-33 · 코디 Q3 · 코드 규약: `app/service/reservations.py:858-859`)
2. **고객 정하기**: §5 와 같은 함수로 정한다(D-32)
   - **2명 이상** → `409 customer_ambiguous`. 예약하지 않는다(D-20 · D-32)
   - **1명** → 그 고객(ccc `customerId`)으로 지금 `create()` 의 「기존 고객」 갈래를 탄다(D-32)
   - **0명** → 지금 `create()` 의 「새 고객」 갈래를 `{name, email}` 로 탄다. 이름 + 연락 수단 하나(이메일)라서 `identifiable()` 를 통과한다. KOS 고객에는 email 이 저장되고, 다음 조회부터는 찾힌다(D-22 · D-32 · 코드 규약: `app/domain/reservation_rules.py:249-255` · `app/service/reservations.py:913-917`)
   - **0명인데 KOS 중복 검사(`find-duplicated-visitor`)에 걸리면** — 지금 `create()` 는 `409 duplicated_visitor` + `candidate`(고객 이름 · 차트번호 · 생년월일)를 낸다. 외부 API 는 이를 **`409 customer_ambiguous` 로 바꾸고 `candidate` 를 싣지 않는다.** 예약하지 않는다. 무엇이 틀렸는지 밝히지 않는다(코디 Q1 · D-20 · D-21 · D-22 확장 · 코드 규약: `app/service/reservations.py:904-912`)
   - **드러남 수용(D-35)**: 이 갈래에서 중복 검사에 걸리면 409, 아니면 200(예약이 생김)이 나가므로 「그 이메일이 KOS 에 있는지」가 드러난다. 이 위험은 받아들인다(API 키를 가진 연동처만 부름 · 호출 제한 D-34 · 기록 D-24). 이 사실을 예약 엔드포인트 Swagger 설명에 적는다(§8)
3. **지금 예약 생성 로직을 다시 쓴다**(D-11 · D-33): `CreateReservationRequest` 를 서버 안에서 만들어(`groupId` = 기본 그룹 ccc id · `zoneId` 생략 · `customer` · `memo`) `ReservationService.create()` 를 부른다. 따라서 구역은 지금 기본 구역 규칙(SPEC-005 §5.5 — `KOS_ZONE_ID` 의 켜지고 자리 있는 구역 → order 순 첫 자리 있는 구역 → 첫 켜진 구역)을 따르고, 담당자는 KOS 시스템 계정이다. 칸 정원 검사(`slot_full`) · KOS 거절 처리도 지금과 같다(코드 규약: `app/service/reservations.py:773-854` · `:856-871` `_pick_zone` · `:873-881` `_assignee`)
4. 행위자 = `ext:<연동처>` 문자열을 `create()` 에 넘긴다(§3.5 행위자 문자열 겹). 지금 `create()` 가 남기는 `resv_create` · `kos_rejected` 줄과 날짜 캐시 비우기가 그대로 일어난다

**응답 200** `ExtReservationResponse`(지금 `CreateReservationResponse` 와 같은 모양):

| 칸 | 타입 | 뜻 | 근거 |
|---|---|---|---|
| `reservationId` | int | 만든 예약의 ccc id | 코드 규약: `app/schemas/reservations.py:718-722` · 코디 Q2 |
| `customerId` | int | 예약 고객 ccc id(0명 갈래면 새로 만든 고객) | 같음 |

**오류**(§6.2 공통 + 아래):

| HTTP | code | 언제 | 근거 |
|---|---|---|---|
| 409 | `customer_ambiguous` | §5 갈래 2명 이상 · 0명 갈래에서 KOS 중복 검사에 걸림 | D-20 · D-32 · 코디 Q1 |
| 409 | `slot_full` | 그 시간 칸의 정원이 찼다(사본 기준 · KOS 쓰기 직전) | D-33 · 코드 규약: `app/service/reservations.py:817-818` |
| 409 | `kos_rejected` | 중복 검사 · 고객 만들기 · 예약 쓰기 단계에서 KOS 가 4xx(401 제외)로 거절했다(같은 고객의 같은 시간 예약 · 정원 · 정책 등 — 문구는 지금 규칙) | 코드 규약: `app/service/kos_errors.py:9-39` |
| 502 | `kos_unavailable` | KOS 네트워크 · 5xx · 401 · 응답 형식(예약 쓰기 · 고객 만들기 · 중복 검사) · 이름 검색은 4xx 도 502(§4.2) · 예약 응답에 일정 id 없음. 예약 뒤 다시 읽기 실패는 502 가 아니다(사본 행을 직접 만들고 200) | 코드 규약: `app/service/kos_errors.py:36-39` · `app/service/reservations.py:738-747`(다시 읽기 실패 = None) · `:845-852` · 코드 검수 r1 W3 |
| 503 | `ext_not_configured` | 기본 그룹 env 가 비었거나 · 그 그룹이 KOS 에서 사라졌거나 · 그 그룹에 켜진 구역이 0 이다 | D-33 · 코디 Q3 · 코드 규약: `app/service/reservations.py:858-859` |

- 지금 `create()` 의 다른 오류 중 외부 요청으로는 일어날 수 없는 것: `groupId`(서버가 넣음) · `zoneId` · `assigneeStaffId` · `counselorStaffId` · `funnelId` · `desiredDischargeTime` 의 400, 「켜진 구역 없음」 400(1단계가 503 으로 먼저 막음), `404 없는 고객`, `409 not_identifiable`(이름 + 이메일이 늘 있다). 그래서 외부 오류 표에 싣지 않는다
- `duplicated_visitor` 는 외부 응답에 **절대 나가지 않는다**(코디 Q1 — `candidate` 누출 금지 · §9 시험)

### 6.6 `GET /api/ext/availability` — 예약 가능 시간대 (DEC-011 D-02 · D-07 ~ D-09 · D-11 · D-12)

> 0.3.0 더함. 이 절과 §6.7 · §6.8 의 「코드 규약」 줄은 main `e0e4a16` 기준이다.

**요청**: 질의 `date=YYYY-MM-DD`(필수). 이름 · 이메일이 없어서 GET 질의로 받는다(DEC-011 D-06 은 이름 · 이메일만 막는다). 본문은 없다.

**처리**(차례대로):

1. **날짜 검사** — 칸은 `date: str` 필수 질의로 받는다(pydantic `date` 타입으로 받지 않는다 — 숫자 문자열을 너그럽게 날짜로 읽을 수 있어 아래 꼴 검사와 어긋난다). `date` 가 **없으면** FastAPI 칸 검증으로 `400 invalid_request` 이고 message 는 지금 검증 규칙 그대로 **`query.date: …`** 다(본문 칸의 `body.name: …` 과 같은 규칙). 있으면 차례로 — **빈 문자열 → `400`**(먼저 막는다 · `parse_day` 의 「빈 값 = 오늘」 갈래를 타지 않는다) · **`YYYY-MM-DD` 숫자 꼴**(숫자 4 · `-` · 숫자 2 · `-` · 숫자 2)이 아니거나 `date.fromisoformat` 이 받지 않으면 `400` — ISO 주 날짜(`2026-W43-4`) 등 `fromisoformat` 이 받는 다른 ISO 꼴도 `400` 이다(코드 검수 add1 r1 N3) · **오늘(KST) 보다 앞이거나 오늘 + 90일보다 뒤이면 `400`**. 이 세 갈래의 message 는 **`date: <이유>`** 다(DEC-011 D-08 · 코드 규약: `app/main.py:120-124`(message = `loc` 를 `.` 로 이음) · `app/domain/reservation_rules.py:51-60` `parse_day` · 문서 검수 add1 W5)
2. **기본 그룹** — 예약(§6.5 1단계)과 같은 검사다. `KOS_EXT_RESERVATION_GROUP_ID` 가 비었거나 · 그 kos_id 의 `present` 그룹이 사본에 없거나 · 그 그룹에 켜진 구역(`ResvContext.enabled_zones`)이 0 이면 → `503 ext_not_configured`. KOS 를 부르기 전이다(DEC-011 D-09 · 코드 규약: `app/service/ext.py:235-242`)
3. **슬롯 새로 읽기** — KOS 공개 `schedule/open/v2/queries/get-reservation-slots-by-groups` 를 **1번** 부른다. 본문은 하루 조회와 같다 — `reservationGroupIds` = 사본의 `present` 예약 그룹 전부 · 기간 = 그 날짜 KST 하루(`day_range`). 성공하면 공유 슬롯 사본(`reservation_slot`)의 그날 행을 통째로 바꾼다(`replace_slots`). 그래서 이 응답 뒤 예약 생성(§6.5)이 같은 사본을 본다. 실패(네트워크 · 5xx · 4xx · 401 · `data` 가 배열 아님) · KOS 설정 없음이면 `502 kos_unavailable` 이고, 사본은 바꾸지 않는다. 지금 `ResvSync._slots()` 를 그대로 부르는 공개 함수 하나(`refresh_slots(day)`)를 `kos/reservation_sync.py` 에 더해 쓴다. 날짜 캐시(`ensure` · 10초)와 하루 예약 · 공지 · 금액 조회는 부르지 않는다(DEC-011 D-12 · 코드 규약: `app/kos/reservation_sync.py:283-284`(그룹 목록) · `:322-341` `_slots` · `app/repository/repo.py:547-554` `replace_slots`)
4. **후보 시각** — 기본 그룹 시간표의 그날 운영 구간(`open_spans` — 쉬는 시간을 뺀 조각들 · 그 요일이 꺼졌으면 없음) 안에서, 자정부터 그룹 간격(`interval_minutes`)으로 나눈 경계 `m`(`m % 간격 = 0` — `lines()` 와 같은 경계) 가운데 `구간 시작 ≤ m` 이고 `m + 간격 ≤ 구간 끝` 인 것. 오늘이면 **시작 시각이 지금보다 뒤인 것만** 남긴다(지금과 같거나 앞이면 뺀다)(DEC-011 D-02 · D-11 · 코드 규약: `app/domain/reservation_rules.py:103-117` `day_table` · `open_spans` · `:133-138` `lines`)
5. **남은 자리** — 후보 시각마다 기본 그룹의 켜진 구역 각각에 대해 사본 슬롯 (그룹 · 구역 · 그 시각) 행을 본다. 행이 있고 `capacity` 가 null 이 아니면 그 구역 몫 = `max(0, capacity − (reservation_count 또는 0))`. 행이 없거나 `capacity` 가 null 인 구역은 합에 넣지 않는다. **켜진 구역 모두 행이 없거나 `capacity` 가 null 이면 그 시각을 뺀다**(자리 수를 모름 — 목록에 없어도 예약은 될 수 있다). 몫을 더한 값이 `remainingSeats` 이고, **0 이면 그 시각을 뺀다**(DEC-011 D-02 · D-11)
6. 남은 것을 시각 오름차순으로 준다. 하나도 없으면(휴무 요일 · 다 참 · 다 지남) `200` 에 `slots: []` 다

**예약 생성과 같은 규칙인 까닭**(DEC-011 D-02): 예약 생성은 고른 구역의 슬롯 행 하나가 `count ≥ capacity` 일 때만 `409 slot_full` 이고, 구역은 `KOS_ZONE_ID` → order 순으로 **자리 있는 구역**을 고른다(행이 없는 구역도 자리 있음으로 본다). 5단계의 합이 1 이상이면 자리 있는 구역이 적어도 하나 있으므로, 같은 사본을 보는 바로 뒤 예약은 정원 때문에 거절되지 않는다. 틀릴 수 있는 것은 이 응답과 예약 사이에 다른 예약이 끼어드는 경합뿐이다(코드 규약: `app/service/reservations.py:818-819` · `:857-871` `_pick_zone` · `app/domain/reservation_rules.py:154-155` `is_full`). 운영 시간 · 휴무 · 지난 시각 검사는 예약 생성에 없다 — 이 목록이 그 시각을 내지 않을 뿐, 예약을 새로 막지 않는다(DEC-011 「걸리지 않는 것」 · SPEC-005 OQ-713).

**응답 200** `ExtAvailability`:

| 칸 | 타입 | 뜻 · null | 근거 |
|---|---|---|---|
| `date` | string | 요청 날짜 `YYYY-MM-DD`(KST) | DEC-011 D-02 |
| `intervalMinutes` | int | 기본 그룹 시간 간격(분). 칸 끝 = `start` + 이 값. 예약(§6.5)의 끝과 같다 | DEC-011 D-02 · 코드 규약: `app/service/reservations.py:827`(끝 = 시작 + 간격) |
| `slots[]` | array | 예약 가능한 칸. 시각 오름차순. 없으면 `[]` | DEC-011 D-02 |
| `slots[].start` | string | 칸 시작 ISO `+09:00`(초 단위). 이 값을 그대로 예약 `start` 로 보내면 된다 | DEC-011 D-02 · §6.1 「시각」 |
| `slots[].remainingSeats` | int | 남은 자리 수(1 이상) — 5단계 합. 0 인 칸은 나오지 않는다 | DEC-011 D-02 · D-11 |

- 응답에 **넣지 않는** 칸: 그룹 · 구역 id · 이름 · 구역별 정원 · 예약 수(DEC-011 D-02 — 그룹 하나 · 칸마다 시작과 남은 자리만)

**오류**(§6.2 공통 + 아래):

| HTTP | code | 언제 | 근거 |
|---|---|---|---|
| 400 | `invalid_request` | `date` 없음(message `query.date: …` — 지금 검증 규칙) · 빈 문자열 · `YYYY-MM-DD` 꼴 아님 · 오늘(KST) 앞 · 오늘 + 90일 뒤(message `date: <이유>`) | DEC-011 D-08 · 코드 규약: `app/main.py:117-121` · `app/domain/reservation_rules.py:51-60` |
| 502 | `kos_unavailable` | 3단계 슬롯 조회 실패 · KOS 설정 없음 | DEC-011 D-12 · 코드 규약: `app/service/kos_errors.py:36-39` |
| 503 | `ext_not_configured` | 2단계(기본 그룹 env 빔 · 그룹 없음 · 켜진 구역 0) — KOS 를 부르기 전 | DEC-011 D-09 · §6.5 |

- **부작용**: 공유 슬롯 사본의 그날 행을 바꾼다(직원 예약 현황의 정원 표시도 그 값을 본다 — 규칙은 같다). KOS 쓰기 · `event_log` 없음
- **KOS 비용**(요청 1번당): 공개 `get-reservation-slots-by-groups` **1번**. 400 · 503 이면 0번(DEC-011 D-12 · Consequences)

### 6.7 `POST /api/ext/customers/visits` — 고객 과거 시술 (DEC-011 D-03 · D-05 · D-06 · D-10 · D-14 · D-15)

**요청** `ExtCustomerRequest`: `{"name": "<이름>", "email": "a@example.com"}` — 조회(§6.4)의 `ExtLookupRequest` 와 같은 칸 · 같은 검증(모르는 키 · 빈 값 400). 경로 · 질의에 이름 · 이메일을 싣지 않는다(DEC-011 D-06).

**처리**:

1. **고객 정하기** — §5 와 같은 함수(`ExtService.find`)다. 0명 → `404 customer_not_found`(조회와 **바이트까지 같은** 본문) · 2명 이상 → `409 customer_ambiguous` · 이름 검색 실패 → `502`(DEC-011 D-05 · 코드 규약: `app/service/ext.py:163-190` · `:198-203`)
2. **일정 읽기** — 1명이면 KOS 공개 `schedule/open/v1/queries/get-schedules-by-visitor` 를 `{visitorId: <그 고객 KOS id>}` 로 **1번** 부른다(직원 상세 「이전 방문」과 같은 호출). **`data` 키가 없음(`{}`) · `data: []` = 일정 없음 → 빈 목록**(`200` · `visits: []` · `reservations: []`)이다. **`data` 가 있으면서 배열이 아님** · 호출 실패(네트워크 · 5xx · 4xx · 401) → `502 kos_unavailable`. **일정 원소의 모양이 깨져 처리할 수 없으면**(예: `reservation` · `reservationTime` 이 객체가 아님 · 작업 `title` 이 문자열이 아님) 그 고객 요청 전체를 **`502 kos_unavailable`** 로 낸다 — 원소를 건너뛰지 않고 `500` 으로 두지 않는다. 본문 · 로그에 KOS 원문은 0 이다(message 「KOS 에 연결하지 못했어요」 · 로그는 예외 종류만)(DEC-011 D-16 · 코드 검수 add1 r1 N1). 시술권(§4.3 「결과 없음」)과 같은 규칙이다 — `_data_list` 를 그대로 쓰지 않는다(그것은 키 없음도 실패로 본다). 고객 사본 · 예약 사본에 쓰지 않는다(코드 규약: `app/service/reservations.py:82` · `:593-594` · `:614-615`(직원 「이전 방문」 = `data` 없으면 빈 목록) · `app/service/ext.py:210-212`(`resp.get("data", [])` → 배열 아니면 502) · KDA 182행(`{}` 사례) · 문서 검수 add1 W1)
3. **고르기** — 일정 시작(`schedule_start` — 묶음 시작 중 가장 이른 값 · 없으면 `reservation.startDateTime`)이 **지금보다 앞인** 일정만 남긴다. 시작을 모르는 일정은 뺀다. **`deleted: true` 인 일정은 뺀다**(사본 쓰기 `apply_schedule` 과 같은 규칙 · DEC-011 D-15 · 코드 규약: `app/kos/reservation_sync.py:156`). 그 밖은 상태와 상관없이 남긴다(취소 · 부도도 결과 칸으로 보인다)(DEC-011 D-03 · 코드 규약: `app/domain/reservation_rules.py:336-340`)
4. **최신 순 · 50건** — 시작 내림차순으로 줄 세워 앞 50건만 준다(DEC-011 D-03 · D-10)

**응답 200** `ExtVisits`:

| 칸 | 타입 | 뜻 · null | 근거 |
|---|---|---|---|
| `visits[]` | array | 지금보다 앞선 일정, 최신 순, 최대 50. 없으면 `[]`(고객은 있는데 지난 일정 없음) | DEC-011 D-03 · D-10 |
| `visits[].date` | string | 시작의 KST 날짜 `YYYY-MM-DD` | DEC-011 D-03 · 코드 규약: `app/service/reservations.py:206` |
| `visits[].start` | string | 시작 ISO `+09:00` | DEC-011 D-03 |
| `visits[].result` | `completed` \| `noshow` \| `canceled` \| `other` | 직원 「이전 방문」 분류 그대로 — KOS `reservation.status` 가 `COMPLETED` · `NO_SHOW` · `CANCELED` 면 각각, 그 밖(값 없음 포함)은 `other` | DEC-011 D-03 · 코드 규약: `app/domain/reservation_rules.py:333` `PREV_RESULT` · `app/service/reservations.py:207` |
| `visits[].procedures` | string[] | 그 일정 작업의 `title`(KOS 배열 순서 · 빈 값이면 빈 문자열). 「방 배정」 기타 작업(`type = ETCETERA` 이고 제목이 「방 배정」)은 뺀다 — 직원 「이전 방문」과 같은 거르기. 작업이 없으면 `[]` | DEC-011 D-03 · 코드 규약: `app/service/reservations.py:212-215` |

- 응답에 **넣지 않는** 칸: 예약 메모 · 상담 메모 · 의사 이름 · 작업 상태 · 구역 · 그룹 · 결과 원래 값(`resultRaw`) · KOS 일정 id · 고객 칸(DEC-011 D-03 · DEC-010 D-13)
- **오늘 겹침**(DEC-011 D-14): 오늘 이미 시작 시각이 지난 일정은 여기에도, 예약 내역(§6.8)에도 나온다. Swagger 설명에 적는다

**오류**(§6.2 공통 + 아래): `400 invalid_request`(조회와 같은 칸 검증) · `404 customer_not_found` · `409 customer_ambiguous` · `502 kos_unavailable`(이름 검색 · 일정 읽기 실패 · 일정 원소 모양 오류 — 2단계 · DEC-011 D-16). 문구 · 조건은 §6.4 오류 표와 같다(DEC-011 D-05).

- **KOS 비용**(요청 1번당): 내부 `get-visitors` 1번 + 공개 `get-schedules-by-visitor` 1번 = **2번**. 404 · 409 이면 1번(일정 읽기 안 함)

### 6.8 `POST /api/ext/customers/reservations` — 고객 예약 내역 (DEC-011 D-04 · D-05 · D-06 · D-13 · D-14 · D-15)

**요청** `ExtCustomerRequest`(§6.7 과 같음).

**처리**:

1. **고객 정하기** — §6.7 1단계와 같다(DEC-011 D-05)
2. **일정 읽기** — §6.7 2단계와 같은 호출 1번 · 같은 규칙(`{}` · `[]` = 빈 목록 · `data` 가 배열 아님 · 원소 모양 오류 = 502)(DEC-011 D-13 · D-16)
3. **고르기** — 일정 시작(§6.7 3단계와 같은 값)이 **오늘(KST) 0시와 같거나 뒤인** 일정만 남긴다. 상태와 상관없이 남긴다(취소 · 부도 포함). 시작을 모르는 일정 · **`deleted: true` 인 일정은 뺀다**(§6.7 3단계와 같은 거르기 — DEC-011 D-04 · D-14 · D-15)
4. **차례** — 시작 오름차순. 개수 상한은 없다(DEC-011 D-04 — KOS 가 준 고객 일정 전부 중 오늘 이후)
5. **예약 id** — 일정 KOS id(`id`)로 ccc 예약 사본을 찾아(`reservation_id_of`) 있으면 그 ccc id, 없으면 null. 사본에 새로 쓰지 않는다. 외부 예약 API(§6.5)로 만든 예약은 예약 생성이 사본에 넣으므로 늘 id 가 있다(DEC-011 D-13 · 코드 규약: `app/repository/repo.py:538-540` · `app/service/reservations.py:847-851`)

**응답 200** `ExtCustomerReservations`:

| 칸 | 타입 | 뜻 · null | 근거 |
|---|---|---|---|
| `reservations[]` | array | 오늘(KST) 이후 일정, 시작 오름차순. 없으면 `[]` | DEC-011 D-04 |
| `reservations[].reservationId` | int \| null | ccc 예약 id(§6.5 응답 `reservationId` 와 같은 체계). ccc 사본에 그 일정이 없으면 null | DEC-011 D-13 · 코디 Q2(DEC-010 부록 B) |
| `reservations[].date` | string | 시작의 KST 날짜 `YYYY-MM-DD` | DEC-011 D-13 |
| `reservations[].start` | string | 시작 ISO `+09:00` | DEC-011 D-13 |
| `reservations[].end` | string \| null | 첫 묶음(`occupiedResources` 를 시작 순으로 놓은 첫 번째)의 끝 ISO `+09:00`. 묶음이 없으면 null | DEC-011 D-13 · 코드 규약: `app/kos/reservation_sync.py:80-99` `resources_of` |
| `reservations[].state` | `reserved` \| `reception` \| `consultation` \| `procedure` \| `home` \| `canceled` \| `noshow` | 직원 판 2계층 주 상태 그대로 — `reservation.status` 가 `CANCELED` · `NO_SHOW` 면 그것, 아니면 `flowStep` 으로 정한다(모르는 단계 = `reserved`) | DEC-011 D-04 · D-13 · 코드 규약: `app/domain/reservation_rules.py:13-22` `FLOW_STATE` · `:41-47` `state_of` |

- 응답에 **넣지 않는** 칸: 그룹 · 구역 이름 · 메모 · 담당자 · 상담사 · 부상태(`sub`) · KOS 일정 id · 고객 칸(DEC-011 D-13)
- **오늘 겹침**(DEC-011 D-14): 오늘 이미 시작 시각이 지난 일정도 여기 나온다(§6.7 에도 나온다)

**오류**: §6.7 과 같다.

- **KOS 비용**(요청 1번당): 내부 `get-visitors` 1번 + 공개 `get-schedules-by-visitor` 1번 = **2번**. 404 · 409 이면 1번

### 6.9 KOS 호출 비용 한눈에 (요청 1번당 · 성공 기준)

| 경로 | KOS 호출 | 근거 |
|---|---|---|
| `GET /api/ext/menu` | 0(DB 만) | §6.3 |
| `POST /api/ext/customers/lookup` | 내부 `get-visitors` 1 + 공개 `get-ticket-bundles` 1 = 2 | DEC-010 Consequences · §6.4 |
| `POST /api/ext/reservations` | 내부 `get-visitors` 1 + (0명이면 `find-duplicated-visitor` 1 + `create-visitor` 1) + `reserve` 1 + 다시 읽기 `get-schedule-detail` 1 = 3 ~ 5 | §6.5 · 코드 규약: `app/service/reservations.py:843-847`(`reserve` → `refresh_schedule` 1번) · `:905` · `:925`(0명 갈래 두 호출) |
| `GET /api/ext/availability` | 공개 `get-reservation-slots-by-groups` 1 | DEC-011 D-12 · §6.6 |
| `POST /api/ext/customers/visits` | 내부 `get-visitors` 1 + 공개 `get-schedules-by-visitor` 1 = 2 | §6.7 |
| `POST /api/ext/customers/reservations` | 내부 `get-visitors` 1 + 공개 `get-schedules-by-visitor` 1 = 2 | §6.8 |

키당 호출 제한(60초 60번)은 여섯 경로가 함께 쓴다(DEC-011 D-01 · DEC-010 D-34). 그래서 한 키가 KOS 에 거는 부담은 60초에 많아야 300번 남짓(예약 60번 × 5)이다.

---

## 7. 인증 · 보안 (D-10 · D-23 ~ D-26 · D-34)

### 7.1 키 (D-23)

- 연동처 = `linky` · `charty` 둘(코드에 고정). 키는 env `PROC_EXT_KEY_LINKY` · `PROC_EXT_KEY_CHARTY` 에서만 읽는다(§2.2). 레포 · 이미지 · 로그 · 응답 · DB 에 키 값이 없다
- 전달 = 요청 헤더 **`X-Api-Key`**. 경로 · 질의 · 쿠키로는 받지 않는다(코드 규약: `app/api/public_questionnaire.py:6` · `app/openapi_docs.py:64-66`)
- 비교 = 들어온 값을 각 연동처 키와 **상수 시간 비교**(`hmac.compare_digest`)로 견준다. 같으면 그 연동처다. 빈 env 인 연동처와는 견주지 않는다
- 키를 바꾸거나 끄는 것은 배포 설정(env · Secret)으로 한다. 앱에 키 관리 API 는 없다(D-23)

### 7.2 직원 API 와의 분리 (D-10)

| 경우 | 결과 | 근거 |
|---|---|---|
| `/api/ext/*` 에 직원 `Authorization: Bearer <ccc 토큰>` 만 | `401 ext_unauthorized`(Bearer 는 보지 않는다) | D-10 · 코드 규약: `app/api/public_questionnaire.py:5` |
| `/api/ext/*` 에 Bearer + 맞는 `X-Api-Key` | 외부 키 권한으로만 동작한다(직원 권한이 더해지지 않음) | D-10 |
| 직원 API(`/api/*` 중 `/api/ext` 밖)에 `X-Api-Key` 만 | 지금처럼 `401 unauthorized`(직원 API 는 `X-Api-Key` 를 보지 않는다) | D-10 · 코드 규약: `app/api/deps.py:17-21` |
| 외부 라우터 | `require_login` · `Actor` 를 쓰지 않는다. 의존성은 `require_ext_key` 하나다 | D-10 · 코드 규약: `app/api/deps.py:17-24` |

`PROC_FAKE_BOARD`(가짜 스냅샷)는 외부 API 에 걸지 않는다. 외부 API 는 가짜 스냅샷을 읽지 않고(메뉴 = 메뉴 표 · 조회 = KOS), 예약은 지금 `create()` 를 그대로 탄다(코드 규약: `app/api/deps.py:27-31` — `require_real_board` 는 직원 조작 라우터에만 걸려 있다).

### 7.3 호출 제한 (D-25 · D-34)

- **키(연동처)당, 최근 60초 안에 60번**. 외부 경로 여섯을 합쳐서 센다(0.3.0 — DEC-011 D-01). 넘으면 `429 too_many_requests` 다(D-34)
- 창 = 고정 1분이 아니라 **미끄러지는 창**이다. 최근 60초 안의 횟수가 60 밑으로 내려가는 순간 다시 열린다. 막힌 요청은 횟수에 더하지 않는다(코드 규약: `app/api/public_questionnaire.py:45-49` · `app/service/questionnaire.py:73-95` `RateLimiter` 를 다시 쓴다)
- 서버 메모리 카운터다(재시작하면 지워진다). **지금 배포 가정 = 파드 1개**(SQLite 파일 하나 · 코드 규약: `app/repository/db.py:1`)라 파드 사이 공유가 필요 없다
- 키가 틀린 요청(401)은 연동처가 없으므로 이 키당 카운터에는 세지 않는다(아래 IP 카운터가 센다)
- 응답 헤더(`Retry-After` 등)는 싣지 않는다 — 지금 `429` 들과 같다(코드 규약: `app/service/questionnaire.py:243`)

**키 없는 거절 IP 제한**(키 추측 · `ext_call` 쌓기 막기 — 문진 웹 선례를 값까지 그대로 쓴다)

- 센다: `/api/ext` 에서 **키 없는 거절**(§3.4 정의 — 401 · 없는 경로 404 · 깨진 본문 400 · 405)이 나갈 때마다 그 IP 카운터에 1을 더한다. IP 차단 429 자신은 더하지 않는다(아래 「막힌 요청은 더하지 않는다」)(코드 규약: `app/service/questionnaire.py:264-265` — 틀린 · 지난 토큰 404 · 410 이면 `rate.add(("bad", ip))`)
- 막는다: 그 IP 의 이 카운터가 **최근 60초 안에 10번 이상**이면, 그 IP 의 `/api/ext` 요청을 키 검사 전에 `429 too_many_requests` 로 막는다. 미끄러지는 창이라 10 밑으로 내려가는 순간 다시 열린다. 막힌 요청은 더하지 않는다(코드 규약: `app/service/questionnaire.py:40` `WINDOW_SEC = 60.0` · `:42` `LIMIT_BAD_IP = 10` · `:253-256` `_gate` · `app/api/public_questionnaire.py:45-49`)
- 자리: 없는 경로 404 는 라우터 밖이므로 이 판단과 카운트는 `/api/ext` 미들웨어가 한다(§3.4 와 같은 미들웨어)
- IP = `CF-Connecting-IP` → `X-Forwarded-For` 첫 값 → 소켓 주소 순 — 지금 `client_ip()` 를 다시 쓴다. IP 는 메모리 카운터 키로만 쓰고 DB · 로그에 남기지 않는다(코드 규약: `app/api/public_questionnaire.py:21-33`)

### 7.4 기록 (D-24)

- `/api/ext/…` 로 들어온 **모든 요청**(성공 · 401 · 429 · 400 · 404 · 405 · 409 · 500 · 502 · 503)마다 미들웨어가 응답을 낸 뒤 `ext_call` 1줄을 쓴다(§3.4 — `client` · `endpoint` 를 정하는 법도 거기). 다만 키 없는 거절(`client` 가 null 인 모든 `/api/ext` 오류 응답 — 401 · 없는 경로 404 · 깨진 본문 400 · 405 · IP 차단 429 · §3.4)은 같은 IP · 같은 `outcome` 이면 1분에 1줄로 줄인다(§3.4). 쓰기 실패는 응답을 바꾸지 않는다(로그에 예외 종류만)
- **처리하지 못한 예외** = `500 internal_error`. `ext_call` 1줄을 쓴다(1분 1줄 줄이기 없음). 서버 쪽 잘못이므로 `client` 가 null 이어도 「키 없는 거절」(§3.4)로 보지 않고 IP 카운트(§7.3)에 넣지 않는다. 앱 설명의 공통 오류 줄(§8)에도 500 을 적는다
- 이름 · 이메일 원문 · 키 값 · 고객 정보는 `ext_call` · 앱 로그 어디에도 남기지 않는다. 앱 로그에는 연동처 · 엔드포인트 · 상태만 남긴다(D-24 · 코드 규약: `app/service/kos_errors.py:42-44` `describe` — 상태 · 이름만)

### 7.5 그 밖

- 고객 조회 · 예약 응답은 `Cache-Control: no-store`(§6.1)
- KOS 내부 API(시스템 계정 토큰 · 브라우저 UA) 조건이 바뀌면 고객 조회 · 예약이 `502 kos_unavailable` 로 멈춘다. 메뉴는 공개 API 와 DB 라서 영향을 받지 않는다(DEC-010 Consequences · D-15)

### 7.6 협업자 admin 계정 (D-26)

외부 API 를 배포하면 협업자에게 공유한 admin 계정 대신 연동처 키를 쓰도록 **권한다**. 계정 회수 시점은 사용자가 정한다. 이 문서 · WORK 는 회수 작업을 하지 않는다.

---

## 8. Swagger (코드 규약: `app/openapi_docs.py` · `tests/test_openapi_docs.py`)

| 항목 | 계약 | 근거 |
|---|---|---|
| tag | 새 tag **`외부 연동`**(`app/api/docs.py` 에 `T_EXT`). 설명: 「링키 · 차티 같은 외부 연동처용 — `X-Api-Key` 헤더로 연다. 직원 로그인 토큰으로는 열리지 않는다.」 외부 경로 여섯 모두 이 tag 하나만 단다(0.3.0) | D-10 · 코드 규약: `app/api/docs.py:42-44` · `app/openapi_docs.py:98-115` |
| securityScheme | `components.securitySchemes.ExtApiKey = {type: "apiKey", in: "header", name: "X-Api-Key", description: "연동처별 API 키(링키 · 차티 각각). 직원 Bearer 와 다르다."}`. `BearerAuth` 는 그대로 둔다 | D-10 · D-23 · 코드 규약: `app/openapi_docs.py:118` · `:150-152` |
| 보안 표시 | `require_ext_key` 의존성이 있는 operation 에 `security: [{ExtApiKey: []}]` 를 단다. `BearerAuth` 는 달지 않는다. `_patch` 가 `_needs_login` 처럼 의존성을 보고 단다 | 코드 규약: `app/openapi_docs.py:121-159` |
| 앱 설명 | `DESCRIPTION` 에 `## 외부 연동 API` 절을 더한다. **첫 줄**: 「email 이 없는 기존 고객은 조회하면 `404` 다. 그 고객을 처음 예약하면 KOS 에 고객이 하나 더 생길 수 있다(데스크가 정리한다).」(D-22). 이어서 「이름은 KOS 에 저장된 띄어쓰기 그대로 보내야 한다(띄어쓰기가 다르면 찾지 못해 `404`).」(D-17 · R4 §0 #2 · §2.1). 그 뒤에 들어갈 것: 경로 여섯(0.3.0 — 「경로 셋」 줄을 여섯으로) · `X-Api-Key` · 연동처별 키 · 직원 API 와 분리 · 검사 순서(§6.1) · 호출 제한(키당 · IP 당 · §7.3) · 기록(무엇을 남기고 무엇을 안 남기나 · §7.4) · 오류 공통 표(§6.2) · 금액 칸 규칙(§6.1) | D-22 · 코드 규약: `app/openapi_docs.py:19-96` |
| 엔드포인트 | `summary` · `description` · 모든 응답 칸 `description` · 응답 표(`responses=` — `- \`code\` — 언제` 줄 꼴)를 지금 규약대로 단다. 설명에 적을 것: 조회 = §5 의 「없음 = 같은 응답」(이름 정확 일치 · `count` > 1000 포함) · **「이름은 KOS 에 저장된 띄어쓰기 그대로 보내야 한다」**(KOS 이름 검색이 공백을 그대로 비교한다 — 띄어쓰기가 다르면 KOS 가 0건을 돌려줘 404. 「공백은 무시한다」고 약속하지 않는다 · R4 §0 #2 · §2.1) · §4.3 의 KOS 그대로의 성질 셋(`bundlePrice` 는 고객이 낸 돈이 아님 · 세트를 쓰면 줄 수 있음 · 부가세 포함 여부 표기 안 함 / `AVAILABLE` 0 묶음 없음 / `IN_USE` 는 남은 장수에 안 넣음) · 예약 = **D-35 문장**(「0명 갈래에서 KOS 중복 검사에 걸리면 409, 아니면 200 이라 그 이메일이 KOS 에 있는지가 드러난다」) · 메뉴 = `syncedAt` 뜻(D-36) | D-31 · D-35 · D-36 · 코드 규약: `tests/test_openapi_docs.py:33-68` · `:104-107` `_codes` |
| 상태 문구 | `app/api/docs.py` `STATUS_TEXT` 에 **`503: "지금 쓸 수 없음"`** 을 더한다(지금 없어서 응답 표 머리가 「오류」로 나온다). 401 머리 「로그인 필요」는 그대로 두고, 외부 401 은 `errors()` 를 그대로 쓰되 `ext_unauthorized` 의 「언제」 줄을 「직원 로그인이 아니라 `X-Api-Key` 헤더의 연동처 키가 없거나 틀렸을 때 …」로 시작한다 | 코드 규약: `app/api/docs.py:46-47` · `:62-68` · review-doc r1 W12 |
| 문서 경로 | 지금 그대로(`/api/docs` · `/api/redoc` · `/api/openapi.json` · 로그인 없이 열림 — `_RESUME` §2 2026-11-11) | `_RESUME` §2 |
| 시험 고침 | `tests/test_openapi_docs.py` 의 `secured == n_ops - 5` 를 **`n_ops - 5 - 3`**(외부 세 operation 은 Bearer 가 아님)으로 고치고, 주석에 외부 셋을 적는다. **0.3.0: `n_ops - 5 - 6`**(외부 여섯) · `tests/test_ext_docs.py` 의 `OPS` 를 여섯으로. **0.3.1: 같은 파일 끝의 parameters 단언을 지우지 않고 넓힌다** — `/api/ext` 모든 operation 의 parameters = `X-Api-Key`(header) + `GET /api/ext/availability` 의 `date`(query) 하나뿐 · 그 밖 query · path 칸 0(`name` · `email` 이 질의에 생기면 실패해야 한다 — D-24 · DEC-011 D-06 · 문서 검수 add1 W3). 나머지 단언(설명 빠짐 0 · 422 없음 · `unauthorized` ↔ `require_login`)은 그대로 통과해야 한다 | 코드 규약: `tests/test_openapi_docs.py:78-101` |
| 「셋」 문구(0.3.1) | 코드에 남은 「세 경로 합산」(`app/openapi_docs.py:85` 앱 설명 호출 제한 줄) · 「세 엔드포인트 합산」(`app/api/ext.py:100` `EXT_RATE` — `COMMON` 으로 여섯 경로의 429 표에 다 붙는다) 문구를 **「외부 경로 전부 합산」** 으로 바꾼다. 「셋」 · 「세 경로」 · 「세 엔드포인트」를 `app/` 에서 전부 세어 고친다 | §7.3 · DEC-011 D-01 · 문서 검수 add1 W4 |
| 엔드포인트(0.3.0) | 새 셋도 `summary` · `description` · 모든 응답 칸 `description` · 응답 표를 단다. 설명에 적을 것: 가능 시간대 = 기본 그룹 하나 · 운영 구간 안 간격 칸 · 남은 자리 0 · 지난 시각 · 자리 수를 모르는 시각은 나오지 않음(「목록에 없어도 예약이 될 수 있다」) · 「이 목록의 `start` 로 예약하면 정원 때문에 거절되지 않는다 — 그 사이 다른 예약이 끼면 `409 slot_full`」 · 날짜 범위 오늘 ~ 90일 / 과거 시술 = 최근 50 · 메모 · 의사 없음 / 예약 내역 = 오늘 0시 이후 · 취소 포함 · `reservationId` null 뜻 / 둘 다 = 조회와 같은 고객 찾기(이름 띄어쓰기 · 「없음」 같은 응답) · **오늘 겹침 문장**(「오늘 이미 시작한 일정은 과거 시술과 예약 내역 둘 다에 나온다」) · KOS 호출 비용(§6.9) | DEC-011 D-02 ~ D-14 · 코드 규약: `app/api/ext.py:119-169`(`SHARED` · `NAME_RULE` · 설명 꼴) |

---

## 9. 시험 기준 (계약 → 고정하는 시험)

KOS 는 지금 시험 방식(`tests/fake_kos.py` 가짜 전송)으로 흉내 낸다. 시험 이름 · 데이터의 사람 이름 · 이메일은 지어낸 값(`<이름>` 꼴 · `a@example.com`)만 쓴다.

| # | 계약 | 시험(새 파일 `tests/test_ext_*.py`) | 근거 |
|---|---|---|---|
| T1 | 메뉴 표 9 · `raw` 원문 보존 | 가짜 KOS 응답(deprecated 칸 · 빈 배열 · 다국어 포함) → 각 표 행 수 · `raw` 를 `json.loads` 하면 원본과 같다(상품 `raw` 에 `options` 없음 · 옵션 `raw` 에 `compositions` 없음) | D-03 · D-04 |
| T2 | 동기화 순서 · ③ 나눠 부르기 | SINGLE N+1 개 → `getProductOptions` 2번 · `medical_service_kos_id` 채움. ③ 응답에서 빠진 옵션은 이전 값 그대로 | D-05 · 코디 Q4 |
| T3 | 「없음」 · 되살림 | 두 번째 동기화에서 상품 1 · 구성 1 · 타겟 국가 1 이 빠짐 → `present = 0`(행 남음) → 세 번째에 다시 나오면 `present = 1` | D-07 |
| T4 | 작업 실패 = 이전 값 | `getProducts` 5xx · `data` 가 배열 아님 → 메뉴 표 그대로 · 다른 작업은 반영 · `sync_state("menu").last_error` 에 이름 · 로그에 본문 · 키 없음 | §4.1 · 코드 규약 |
| T5 | 마스터 루프에 얹힘 | `master_once()` 1번 = 메뉴 작업 호출 · 서버 시작 1회 · 조회 시간 밖에서도 돈다 | D-06 |
| T6 | 메뉴 응답 깊이 · 칸 | SINGLE · GROUP · CONSULTATION 한 개씩 → 칸 목록이 §6.3 과 같다(내지 않는 칸 0 — 응답 JSON 에 `medicalService` · `medicineAndMachines` · `suppliedAmount` · `vatAmount` · `additional` · `displayChannels` · `badges` · `caution` 키가 없다). CONSULTATION 가격 · 횟수 · 단위 · 시술 null · `syncedAt` = 마지막 성공 시각(`+09:00`) · 성공 전 null · **성공 → 다음 바퀴에서 작업 하나 실패 → `syncedAt` 은 앞 성공 시각 그대로**(null 아님 · `last_error` 만 바뀜) | D-27 ~ D-30 · D-36 · 코디 Q5 |
| T7 | 메뉴 「지금 있는 것만」 | `present = 0` · `closed` · `deleted` · `opened:false` 행이 응답에 없음 · 위 층이 빠지면 아래 층도 없음 | D-07 |
| T8 | 정가 = 부가세 별도 · 칸 이름 | `listPriceExVat.value` = KOS `price.amount.value` · 구성 합 = 옵션 | D-09 · D-30 |
| T9 | 이름 검색 한 페이지 · 상한 · 중복 제거 | `get-visitors` 본문 `indexOfPage` 0 · `countInPage` 1000 · 조회 1건당 **1번**(두 번째 페이지 0번) · 같은 KOS id 가 두 번 오면 1명(→ `200`, `409` 아님) · `count` 1001 → `404 customer_not_found`(KOS 호출 1번 · 시술권 조회 0번 · 본문이 T13 「없음」과 바이트까지 같음) | D-16 · D-21 |
| T10 | 이름 다듬기 | 요청 `"  <이름>  "` → KOS 본문 `visitorName` 은 앞뒤 공백 없음 · 가운데 공백 그대로 · 검색 1번(다시 검색 0) | D-17 |
| T11 | 이메일 비교 | 대소문자 · 앞뒤 공백만 다른 이메일 = 맞음 · KOS 쪽 키 없음 · 빈 문자열 = 후보 아님 · `@` 없는 값도 같으면 맞음 | D-18 |
| T12 | 이름 정확 일치 · 갈래 0 · 1 · 2+ | 부분 일치만 맞는 이름(KOS `name` 이 입력을 포함만 함) + 맞는 이메일 → `404` · 발음명(`phoneticName`)만 같음 → `200` · 대소문자만 다름 → `200` · 공백(가운데 포함)만 다름 → **KOS 가 그 고객을 돌려준 경우(가짜 KOS 응답을 직접 지정)에만** `200` · 가운데 공백이 다른 입력 → KOS 0건(지금 `tests/fake_kos.py` 검색 규칙 그대로 — 공백 그대로 · 부분 일치. 이 규칙은 고치지 않는다) → `404` · 0명 → `404 customer_not_found` · 2명 → `409 customer_ambiguous`(본문에 이름 · id · 수 없음) | D-19 · D-20 |
| T13 | 「없음」 하나 | 이름 틀림 · 부분 일치만 맞는 이름 · 이메일 틀림 · email 빈 고객 · 고객 없음 · `count` > 1000 여섯 경우의 응답 본문 · 상태가 **바이트까지 같다** | D-16 · D-19 · D-21 · D-22 |
| T14 | 시술권 · 「없음」 구분 | 묶음 `{}` → `200 tickets: []` · 고객 없음 → `404` · 시술권 조회 실패 → `502`(빈 배열 아님) | D-12 · D-14 |
| T15 | 시술권 한 줄 | 묶음 2(SINGLE · GROUP 세트 둘 · USED · `IN_USE` 섞임) → `remainingCount`(`AVAILABLE` 만 · `IN_USE` 안 셈) · `totalCount` · `purchasedDate`(KST · 가장 이른 값) · `bundlePrice` = KOS `price` · 응답 JSON 에 `purchasePrice` · `VatIncluded` 가 들어간 키 없음 · 메뉴에 없는 `optionId` 도 그대로 · 옵션 이름은 메뉴 값이 아니라 묶음 값 | D-08 · D-31 |
| T16 | 고객 응답 칸 | 키 집합 = `{customerId, name, isNew, lastVisitDate}` · KOS id · 전화 · 생년월일 · 국적 · 여권 · 차트번호 · 이메일 없음 · `lastVisitedDateTimeUtc` 없으면 null | D-13 · D-31 · 코디 Q2 |
| T17 | 예약 1명 · 행위자 | 기존 고객 갈래 · KOS `reserve` 본문의 그룹 = env 그룹 · 구역 = 기본 구역 규칙 · 담당자 = 시스템 계정 · `event_log.resv_create` actor = `ext:linky` 문자열(가짜 `Account` 없음) · KOS 거절 때 `kos_rejected` actor 도 `ext:linky` | D-32 · D-33 · §3.5 |
| T18 | 예약 0명 | `find-duplicated-visitor` → `create-visitor`(본문에 `name` · `email`) → `reserve` · 응답 `customerId` = 새 행 | D-22 · D-32 |
| T19 | 예약 2명 · 중복 검사 걸림 | 둘 다 `409 customer_ambiguous` · `reserve` 0번 · 응답에 `candidate` 없음 · 외부 응답 어디에도 `duplicated_visitor` 없음 | D-20 · 코디 Q1 |
| T20 | 예약 그룹 설정 | env 빔 · 그룹 `present = 0` · 그룹에 켜진 구역 0 → 셋 다 `503 ext_not_configured`(`400 invalid_request` 아님) · KOS 호출 0번 | D-33 · 코디 Q3 |
| T21 | 예약 정원 · KOS 실패 | `slot_full` · `kos_rejected` · `kos_unavailable` 이 지금 규칙 그대로 | D-33 |
| T22 | 예약 요청 칸 | `groupId` · `zoneId` · `assigneeStaffId` 를 보내면 `400 invalid_request` · `start` 형식 오류 400 · 빈 이름 · 이메일 400 | D-32 · D-33 |
| T23 | 키 인증 | 키 없음 · 빈 값 · 틀림 · 꺼진 연동처 · Bearer 만 → `401 ext_unauthorized` · 맞는 키 = 그 연동처(`ext_call.client`) | D-10 · D-23 |
| T24 | 직원 API 분리 | 직원 경로에 `X-Api-Key` 만 → `401 unauthorized` · 외부 경로에 Bearer + 키 → 외부 권한(직원 경로를 대신 열지 못함) | D-10 |
| T25 | 검사 순서 | 키 틀림 + **칸** 틀림(필수 빠짐 · 모르는 키) → 401 · 한도 초과 + 칸 틀림 → 429 · 키 틀림 + JSON 이 아닌 본문 → 400 · 키 없음 + 없는 경로 → 404 · IP 차단 중 + 맞는 키 → 429 | §6.1 |
| T26 | 호출 제한 | 같은 키 60번 200 → 61번째 429(세지 않음) → 시계를 60초 넘기면 다시 200 · 다른 연동처 키는 따로 셈 · 401 은 키당 카운터에 안 셈 | D-25 · D-34 |
| T27 | 기록 | 성공 · 401 · 429 · 404 · 409 · 502 마다 `ext_call` 1줄(`client` · `endpoint` · `status` · `outcome`) · 맞는 키 + 없는 경로 → `client` null · `endpoint` = `"<METHOD> (unknown)"` · **경로에 이메일 꼴 문자열(`/api/ext/customers/a@example.com`) → 표 어디에도 그 문자열 없음** · 키 없는 401 을 같은 IP 에서 5번 → 1분 안 1줄 · 시계를 60초 넘기면 다시 1줄 · 키 없는 깨진 본문 400 · 405 도 같은 IP 에서 5번 → 1분 안 1줄(`client` null) · 테이블 전체 · 앱 로그(caplog)에 요청 이름 · 이메일 · 키 · IP 문자열 0 | D-24 · §3.4 |
| T28 | 캐시 헤더 | `/api/ext` 응답(오류 포함) `Cache-Control: no-store` | §6.1 |
| T29 | Swagger | `외부 연동` tag · `ExtApiKey` scheme · 외부 operation 3(0.3.0: **6** — 새 셋 설명에 오늘 겹침 문장 · 가능 시간대 규칙 문장) = `security [{ExtApiKey: []}]` · Bearer 아님 · 401 표에 `ext_unauthorized`(`unauthorized` 아님) · 그 줄이 `X-Api-Key` 를 말함 · 503 표 머리 = `STATUS_TEXT[503]` · 예약 설명에 D-35 문장 · 앱 설명 외부 절 첫 줄 = email 없는 고객 문장 · **(0.3.1) 여섯 operation 의 429 줄이 「외부 경로 전부 합산」을 말하고 「세 엔드포인트」 · 「세 경로」가 없음 · 앱 설명에도 「세 경로」 없음** · **(0.3.1) parameters = `X-Api-Key`(header) + availability `date`(query)만**(§8 시험 고침) · `test_openapi_docs.py` 전부 통과(개수 단언 고침 뒤) | §8 · D-35 · 문서 검수 add1 W3 · W4 |
| T30 | 직원 API 회귀 | 기존 시험 전부 통과 — 특히 `test_resv_write.py`(예약 생성) · `test_resv_*` · 접수 시험 · `test_openapi_docs.py`. 직원 예약 생성 · 접수의 `event_log.actor` = 그 직원 `login_id`(지금과 같음) | O11 · §3.5 |
| T31 | 키 없는 거절 IP 제한 | 같은 IP 에서 키 없는 401 · 없는 경로 404 · 깨진 본문 400 · 405(있는 경로에 틀린 메서드)를 섞어 합쳐 10번 → 11번째 요청은 맞는 키여도 `429 too_many_requests`(세지 않음) · 시계를 60초 넘기면 다시 열림 · 다른 IP 는 영향 없음 · `CF-Connecting-IP` 가 있으면 그 값으로 셈 · IP 문자열이 `ext_call` · 로그에 0 | §7.3 · D-24 |
| T32 | 가능 시간대 후보 · 남은 자리(0.3.0) | 기본 그룹(간격 30 · 운영 10:00 ~ 20:00 · 쉬는 시간 13:00 ~ 14:00 · 켜진 구역 둘) · 내일 날짜 → 후보 = 10:00 ~ 12:30 · 14:00 ~ 19:30(13:00 · 13:30 · 20:00 없음) · 한 시각에 구역 A 정원 3 · 예약 1, 구역 B 정원 3 · 예약 3 → `remainingSeats` 2 · 구역 B 행 없음 → A 몫만 · 두 구역 다 행 없음(또는 `capacity` null) → 그 시각 없음 · 두 구역 다 참 → 그 시각 없음 · 휴무 요일 → `slots: []` · 응답 키 = `{date, intervalMinutes, slots}` · `slots[]` 키 = `{start, remainingSeats}` · 15분 그룹이면 간격 15 · `start` 가 `+09:00` | DEC-011 D-02 · D-11 |
| T33 | 오늘 지난 시각 | 시계를 오늘 14:10 으로 둠 → 14:00 이하 시각 없음 · 14:30 부터 · 시계를 정확히 14:30 으로 두면 14:30 도 없음 | DEC-011 D-02 |
| T34 | 날짜 검사 | `date` 없음 → `400 invalid_request` · message 가 `query.date:` 로 시작 · `date=`(빈 문자열) · `2026-1-5` · `20261105` · 어제 · 오늘 + 91일 → `400 invalid_request` · message 가 `date:` 로 시작 · 모두 KOS 호출 0 · 오늘 · 오늘 + 90일 → 200 | DEC-011 D-08 |
| T35 | 가능 시간대 설정 | env 빔 · 그룹 `present = 0` · 켜진 구역 0 → `503 ext_not_configured` · KOS 호출 0 | DEC-011 D-09 |
| T36 | 슬롯 새로 읽기 | 요청 1번 = `get-reservation-slots-by-groups` 1번(본문 그룹 = 사본 `present` 그룹 전부 · 그날 KST 하루) · 하루 예약 · 공지 · 금액 조회 0번 · 사본 그날 행이 응답 값으로 바뀜 · KOS 5xx · 4xx · 401 · `data` 배열 아님 → `502 kos_unavailable` · 사본 그대로 · **(0.3.1) runtime 없음(KOS 설정 없음) → `502` · KOS 호출 0** | DEC-011 D-12 · 문서 검수 add1 W6 |
| T37 | 예약과 같은 규칙 | ① 사본에 「참」이 남은 시각을 KOS 가 「자리 있음」으로 바꾼 뒤 가능 시간대 → 그 시각이 나옴 → 곧바로 외부 예약(§6.5) → `slot_full` 아님 ② 목록의 모든 시각에 외부 예약 → `slot_full` 0 ③ 목록에 없는(모든 구역 참) 시각으로 예약 → `409 slot_full` | DEC-011 D-02 |
| T38 | 과거 시술 | 일정 55건(지난 53 · 앞으로 2 · 시작 없는 1 포함) → 지난 것 중 최신 50건 · 시작 내림차순 · `result` = `COMPLETED` → completed · `NO_SHOW` → noshow · `CANCELED` → canceled · `RESERVED` · 값 없음 → other · `procedures` = 작업 title(「방 배정」 ETCETERA 뺌 · 다른 ETCETERA 는 남음) · 응답 JSON 에 `reservationMemo` · `consultationMemo` · `doctors` · `resultRaw` · `zoneTitle` · `groupTitle` 키 없음 · 지난 일정 없음 → `visits: []` · **(0.3.1) `deleted: true` 지난 일정 → 나오지 않음** | DEC-011 D-03 · D-10 · D-15 |
| T39 | 과거 시술 · 예약 내역의 고객 갈래 | 0명 · 이름 틀림 · 이메일 틀림 · `count` > 1000 → `404` 본문 · 상태가 조회(§6.4) 404 와 **바이트까지 같음** · 2명 → `409 customer_ambiguous` · 404 · 409 이면 `get-schedules-by-visitor` 0번 · 일정 읽기 5xx · `data` 가 있으면서 배열 아님 → `502`(빈 목록 아님) · **(0.3.1) 일정 응답 `{}`(`data` 키 없음) · `{"data": []}` → `200` · `visits: []` · `reservations: []`** · **(0.3.1) 이름 검색 5xx → `502` · 일정 읽기 0번**(두 경로 각각 1줄) · 고객 · 예약 사본 행 수 그대로 | DEC-011 D-05 · D-12 · D-13 · 문서 검수 add1 W1 · W6 |
| T40 | 예약 내역 | 오늘 0시 이후 일정만 · 시작 오름차순 · 취소 · 부도 포함 · `state` = 2계층 주 상태(`RECEPTION` → reception · `PROCEDURE_DONE` → home · `CANCELED` → canceled · 모르는 단계 → reserved) · 사본에 있는 일정 = 그 ccc id · 없는 일정 = null(사본 행 늘지 않음) · 외부 예약(§6.5)으로 만든 예약 → 내역에 그 `reservationId` 그대로 · `end` = 첫 묶음 끝 · 묶음 없음 → null · 응답 키 = `{reservationId, date, start, end, state}` · 지난 일정만 있는 고객 → `reservations: []` · **(0.3.1) `deleted: true` 앞으로 일정 → 나오지 않음** | DEC-011 D-04 · D-13 · D-15 |
| T41 | 오늘 겹침 | 오늘 09:00 일정 · 시계 오늘 12:00 → 과거 시술과 예약 내역 둘 다에 나옴 | DEC-011 D-14 |
| T42 | 요청 칸 | 과거 시술 · 예약 내역 본문에 모르는 키 · 빈 `name` · `email` → `400` · 가능 시간대에 `name` 질의를 붙여도 쓰이지 않음(무시 · `ext_call.endpoint` 는 경로 틀만) | DEC-011 D-06 |
| T43 | KOS 비용 | §6.9 표 그대로 — 가능 시간대 1 · 과거 시술 2 · 예약 내역 2(404 · 409 이면 1) · 가짜 KOS 호출 수로 단언 | DEC-011 D-12 · §6.9 |
| T44 | 공유 규칙(새 세 경로) | 키 없음 → `401 ext_unauthorized` · 응답(오류 포함) `Cache-Control: no-store` · `ext_call.endpoint` = `GET /api/ext/availability` · `POST /api/ext/customers/visits` · `POST /api/ext/customers/reservations` · 키당 제한을 여섯 경로가 함께 셈(메뉴 30 + 가능 시간대 30 → 61번째 과거 시술 429) · 표 · 로그에 이름 · 이메일 0 · **(0.3.1) `POST /api/ext/availability` → `405 http_error` · 새 세 operation 의 Swagger 응답 표에 공통 줄(401 · 429 · 405 · 500)이 다 붙음**(`responses=errors(*COMMON, …)`) | DEC-011 D-01 · DEC-010 D-24 · D-34 · 문서 검수 add1 W6 |
| T45 | 경계 시각(0.3.2) | ① 시계 = 일정 시작 정각(오늘 12:00 일정 · 시계 12:00) → 과거 시술에 **없음**(「지금보다 앞」이 아님) · 예약 내역에 **있음** ② 오늘 00:00 정각 시작 일정 → 예약 내역에 **있음**(「0시와 같거나 뒤」) | DEC-011 D-03 · D-04 · 코드 검수 add1 r1 N2 |
| T46 | 일정 읽기 4xx · 401(0.3.2) | `get-schedules-by-visitor` 가 400 · 401 → 과거 시술 · 예약 내역 둘 다 `502 kos_unavailable`(빈 목록 아님 · 경로마다 1줄) | §6.7 2 · 코드 검수 add1 r1 N2 |
| T47 | 일정 원소 모양 오류(0.3.2 · 0.3.3 고침) | 일정 원소 하나의 `reservation` 이 문자열 · `occupiedResources[].reservationTime` 이 문자열 → 과거 시술 · 예약 내역 둘 다 `502 kos_unavailable`(500 아님) · **작업 `title` 이 숫자 → 과거 시술만 `502`**(예약 내역은 작업을 보지 않으므로 `200`) · 본문은 공통 502 본문과 같고 KOS 원문 문자열 0. 로그에 원문 0 은 **코드 검수 재현으로 확인**했다(로그에 예외 종류만 · 시험 단언은 없음 — `caplog` 단언을 넣는 것은 선택) | DEC-011 D-16 · 코드 검수 add1 r1 N1 · r2 M1 |

**실물 확인**(시험이 아니라 WORK-012 의 완료 조건): 데모 KOS 로 ① 메뉴 동기화 한 바퀴(표 행 수 = R1 §4 와 같은 규모) ② email 이 채워진 데모 고객 1명을 이름 + 이메일로 조회 ③ 이름 + 이메일로 예약(기존 고객 · 새 고객 각 1번)을 실제로 부른다. 값(이름 · 이메일 · id)은 문서에 적지 않는다.

**실물 확인(0.3.0 · WORK-013 의 완료 조건)**: 데모 KOS 로 ① 가능 시간대를 하루 부르고 KOS 웹 예약 현황(기본 그룹)의 정원 · 예약 수와 맞는지 본다 ② 목록의 한 시각으로 외부 예약 1번 → 200 · 그 칸의 `remainingSeats` 가 1 줄어듦(남은 자리 1 이었으면 칸이 빠짐) ③ email 이 채워진 데모 고객으로 과거 시술 · 예약 내역 → 200 · ② 의 예약이 예약 내역에 그 `reservationId` 로 나옴 · 과거 시술에 메모 · 의사 칸 없음 ④ 틀린 이메일 → 두 경로 모두 404 가 조회 404 와 같은 본문. 끝나면 ② 예약을 직원 화면으로 취소한다. 값은 적지 않는다.

---

## 10. 열린 것

**없음.** DEC-010 은 열린 것 0 으로 닫혔고(`_RESUME` §5 2026-11-11), 이 문서가 DEC 와 코드 규약으로 정하지 못한 다섯 가지는 코디 답(부록 B Q1 ~ Q5)으로, doc 검수 r1 의 DEC 질문 셋과 W11 은 DEC-010 고침(D-16 · D-19 · D-31 · D-35 · D-36 · 부록 B Q-A ~ Q-C · W11)으로 닫았다. 부록 B 의 질문은 모두 「답함」이다. 0.3.0(add1)은 DEC-011(열린 것 0)로 닫혔고, DEC-011 승인 결정만으로 정해지지 않은 넷은 코디 답(부록 E Q1 ~ Q4 → DEC-011 D-11 ~ D-14)으로, 0.3.1 의 문서 검수 DEC 질문 Q-add1-A 는 코디 기본값(DEC-011 D-15)으로, 0.3.2 의 코드 검수 N1 은 코디 기본값(DEC-011 D-16)으로 닫았다.

구현 때 실측으로 채우는 **값** 두 개는 정책이 아니라서 열린 것으로 두지 않는다(채우는 자리는 WORK-012 에 있다).
1. `getProductOptions` 한 번에 넣을 옵션 수 N(§4.1 ③ · 코디 Q4 「구현 시 실측」)
2. 공개 메뉴 작업 8개의 실제 경로 문자열(§4.1 — 스펙 operationId 에서 옮김)

---

## 부록 A. DEC-010 대응표 (D-01 ~ D-36 → 이 문서 · 빠짐 0)

| D | 결정(줄임) | 반영한 곳 |
|---|---|---|
| D-01 | 자리 = `procedure/back` · 화면 범위 아님 | 머리말 · §1.1 · §1.2 O1 · §2.1 |
| D-02 | 만드는 것 셋(메뉴 저장 · 외부 API · 인증) | §0 · §1.1 I1 ~ I4 |
| D-03 | KOS 메뉴 전부 · 모든 칸 저장 | §1.1 I1 · §3.1 · §3.2 · §9 T1 |
| D-04 | 단계별 표 + 원본 JSON · SQLite 규약 | §3.1 · §3.2 · §9 T1 |
| D-05 | 원천 작업 · SINGLE 진료항목 붙이기 · 빈 검색어 안 부름 | §4.1 ①~⑧ · §1.2 O9 · §3.2 `menu_option` · §9 T2 (코디 Q4 — `getProductOptions` 추가) |
| D-06 | 마스터 루프(1시간) · 서버 시작 1회 · Webhook 안 받음 | §4.1 「언제」 · §1.2 O9 · §9 T5 |
| D-07 | 사라진 행 = 「없음」 표시 · 되살림 · 응답엔 지금 있는 것만 | §3.1 「없음」 · §3.2 · §4.1 · §6.3 「지금 있는 것」 · §9 T3 · T7 |
| D-08 | 메뉴 = 지금 · 산 것 = KOS 값 그대로 · 메뉴에 없는 옵션도 그대로 | §4.3 표 · §6.4 · §9 T15 |
| D-09 | 정가 = 부가세 별도 · 응답 칸 이름으로 밝힘 · 시술권 가격 = KOS 값 그대로 | §3.3 · §6.1 「금액」 · §6.3 `listPriceExVat` · §6.4 `bundlePrice`(KOS 값 그대로 — 부가세 표기는 D-31 고친 문구대로 안 함) · §9 T8 · T15 |
| D-10 | 경로 분리 `/api/ext` · 토큰 · 키 섞이지 않음 | §6.1 · §7.2 · §8 · §9 T23 · T24 |
| D-11 | 엔드포인트 셋 · 예약은 지금 로직 재사용 | §6.3 · §6.4 · §6.5 · §2.1 |
| D-12 | 남은 시술권 = 조회 때마다 KOS · 복사 안 함 · 다 쓴 것 · 통계 안 줌 | §1.2 O2 · O3 · §4.3 · §9 T14 |
| D-13 | 고객 응답 = 상담 칸만 · 개인 칸 뺌 | §1.2 O5 · §6.4 · §9 T16 |
| D-14 | 「고객 없음」 ≠ 「시술권 없음」 | §4.3 「결과 없음」 · 「실패」 · §6.4 · §9 T14 |
| D-15 | 내부 `get-visitors` 이름 검색 → 우리 쪽 이메일 거르기 | §4.2 · §5 · §7.5 |
| D-16 | 한 페이지(1000)만 · `count` > 1000 = 「없음」 · KOS id 중복 제거 (2026-11-11 고침) | §4.2 「본문」 · 「한 페이지만」 · 「상한」 · 「중복 제거」 · §5 1 · 2 · §6.4 404 · §1.2 O11 · §9 T9 · T13 |
| D-17 | 이름 앞뒤 공백만 · 다시 검색 안 함 | §4.2 · §5 1 · §1.2 O7 · §9 T10 |
| D-18 | 이메일 = 공백 지움 + 소문자 · 정확 일치 · 빈 email 은 후보 아님 | §5 4 · 5 · §9 T11 |
| D-19 | 이름 정확 일치(공백 전부 지움 · 대소문자 무시 · 이름 또는 발음명) 뒤 이메일 (2026-11-11 고침) | §4.2 「응답에서 쓰는 칸」 · §5 3 · §9 T12 · T13 |
| D-20 | 2명 이상 = 「특정할 수 없음」 | §5 6 · §6.4 · §6.5 · §9 T12 · T19 |
| D-21 | 틀린 입력 = 없는 고객 = 같은 「없음」 | §5 「없음」 · §6.4 · §9 T13 |
| D-22 | email 빈 기존 고객 = 「없음」 · 보조 키 없음 · 예약으로 email 쌓임 · 중복 수용 | §1.2 O6 · §5 · §6.5 2 · §9 T13 · T18 |
| D-23 | 연동처별 API 키 · env/Secret · 배포 설정으로 교체 | §2.2 · §7.1 · §9 T23 |
| D-24 | 호출마다 기록 · 이름 · 이메일 원문 없음 | §3.4(미들웨어 · `client` · `endpoint` 고정값 · 줄이기) · §6.4(POST 본문) · §7.3(IP 저장 안 함) · §7.4 · §9 T27 · T31 |
| D-25 | 키별 호출 제한 | §7.3 · §9 T26 · T31(키 없는 거절 IP 제한) |
| D-26 | admin 공유 계정 → 외부 키 권함 · 회수는 사용자 | §1.2 O10 · §7.6 |
| D-27 | 메뉴 응답 깊이 · 진료항목 · 기기 · 약물은 DB 만 | §1.2 O4 · §6.3 · §9 T6 |
| D-28 | 옵션 `type` 그대로 · CONSULTATION 가격 · 구성 없이 | §3.2 `menu_option` · §6.3 `type` · §9 T6 |
| D-29 | `translsMap` 그대로 + 기본 이름 | §3.3 · §6.3 |
| D-30 | 가격 = 정가 `amount` 하나 · 나머지 DB 만 | §1.2 O4 · §6.3 · §9 T6 · T8 |
| D-31 | 고객 응답 칸 · 시술권 한 줄 칸 · 가격 = KOS 묶음 가격(`bundlePrice` · 낸 돈 아님 · 줄 수 있음 · 부가세 표기 안 함) (2026-11-11 고침) | §0 · §4.3 표 · §6.1 「금액」 · §6.4 · §8 · §9 T15 · T16 |
| D-32 | 예약 필수 · 선택 칸 · 1 / 0 / 2+ 갈래 · 신규 규칙을 이메일로 채움 | §5 · §6.5 · §9 T17 ~ T19 · T22 |
| D-33 | 그룹 = 설정값 하나 · 구역 = 기본 규칙 · 담당자 안 받음 · 정원 검사 같음 | §2.2 · §6.5 · §1.2 O8 · §9 T17 · T20 · T21 |
| D-34 | 키당 분당 60 · 넘으면 429 | §7.3 · §6.2 · §9 T26 |
| D-35 | 예약 0명 갈래 409/200 으로 이메일 존재가 드러나는 위험 수용 · Swagger 에 적음 (2026-11-11 추가) | §0 · §6.5 2 「드러남 수용」 · §8 엔드포인트 · §9 T29 |
| D-36 | 메뉴 응답 `syncedAt` 메타 칸 (2026-11-11 추가) | §6.3 `syncedAt` · §8 엔드포인트 · §9 T6 |

## 부록 B. planner 질문 → 코디 답 (2026-11-11)

DEC-010 과 코드 규약으로 정해지지 않아 물은 것(Q1 ~ Q5)과 doc 검수 r1 이 올린 DEC 질문(Q-A ~ Q-C · W11)이다. 모두 답을 받았다. 근거 칸의 「코디 Q1 ~ Q5」는 여기를 가리킨다(근거 표기: **코디 기본값(planner 질문 Q1 ~ Q5 · 2026-11-11)**).

| Q | 물은 것 | 상태 · 답 | 함께 가리키는 D | 반영 |
|---|---|---|---|---|
| Q1 | 0명 → 새 고객 갈래에서 KOS 중복 검사(`find-duplicated-visitor`)에 걸리면 | **답함** · **A** — 예약하지 않고 `409 customer_ambiguous`. `candidate` 를 싣지 않고, 무엇이 틀렸는지 밝히지 않는다 | D-20 · D-21 · D-22 확장 | §6.5 2 · §9 T19 |
| Q2 | 응답 id 체계 | **답함** · **A** — 메뉴 · 시술권의 id = KOS id 문자열 · 고객 id · 예약 id = ccc 정수. **KOS id 는 메뉴 · 시술권 id 에만** 내고, 고객 KOS id 는 내지 않는다 | D-08 · D-12 | §6.1 「id」 · §6.3 · §6.4 · §9 T16 |
| Q3 | 기본 그룹 설정이 비었거나 그룹이 사라졌을 때 | **답함** · **A** — 예약만 `503 ext_not_configured`(새 오류 클래스 1개). 조회 · 메뉴는 그대로 | D-33 | §2.2 · §6.5 1 · §9 T20 |
| Q4 | SINGLE 옵션의 진료항목 잇기(`getProducts` 에 id 가 없음) | **답함** · **A** — `getProductOptions` 를 원천 작업에 더해 SINGLE 진료항목 id 를 채운다. KOS 문서에 개수 상한이 있으면 따르고, 없으면 N개씩 나눠 부른다(N 은 구현 때 실측). 코디가 DEC-010 D-05 문구를 고친다 | D-03 · D-05 | §3.2 · §4.1 ③ · §9 T2 |
| Q5 | 메뉴 응답 칸 목록 | **답함** · **A + 두 칸** — 층마다 id · 기본 이름 · `translsMap` + 카테고리 `order` + 상품 · 옵션 `description` + 옵션 `type` · 정가 · 횟수 + 구성 title · count · 정가. 거기에 **단위 `unit`**(SINGLE = 진료항목 단위를 옵션 칸으로 · 구성 = 구성 단위 · 없으면 null)와 **상품 `isEvent`** 를 더한다. 그 밖(caution · 이미지 · displayChannels · badges 등)은 넣지 않는다 | D-27 · D-30 | §3.3 · §6.3 · §9 T6 |
| Q-A | (doc 검수 r1) 이름 검색의 범위 · 이름 대조 | **답함**(사용자) — 한 페이지(`countInPage` 1000)만 · `count` > 1000 = 「없음」 · KOS id 중복 제거 · 이름(또는 발음명) 정확 일치(공백 전부 지움 · 대소문자 무시) 뒤 이메일 | D-16 · D-19 | §4.2 · §5 · §9 T9 · T12 · T13 |
| Q-B | (doc 검수 r1) 예약 0명 갈래의 409/200 이 이메일 존재를 드러냄 | **답함**(사용자) — 받아들인다 · Swagger 예약 설명에 적는다 | D-35 | §6.5 2 · §8 · §9 T29 |
| Q-C | (doc 검수 r1) 시술권 가격 칸의 이름 · 뜻 | **답함**(사용자) — KOS 묶음 가격 그대로 `bundlePrice` · 낸 돈 아님 · 줄 수 있음 · 부가세 표기 안 함 | D-31 | §4.3 · §6.1 · §6.4 · §9 T15 |
| W11 | (doc 검수 r1) 메뉴 응답 `syncedAt` | **답함**(코디) — 둔다(메타 칸) | D-36 | §6.3 · §9 T6 |

## 부록 C. 조사 리포트의 「정할 것」 → 처분

| 리포트 | 정할 것 | 처분 |
|---|---|---|
| 조사 1 §8 | 1 노출 깊이 · 2 원천 작업 · 3 type 표현 · 4 가격 칸 · 5 다국어 | D-27 · D-05(+ 코디 Q4) · D-28 · D-30 · D-29 |
| 〃 | 6 채널 · 국가 필터 | 질의 칸을 열지 않는다(§6.3 「질의 칸 없음」 · D-27 이 깊이만 정함). 채널 필터는 KOS 가 키에 따라 이미 걸러 준 것을 그대로 저장한다(R1 §2.3) |
| 〃 | 7 캐시 | D-06(1시간 마스터 루프 · Webhook 안 받음) |
| 〃 | 8 id 노출 | 코디 Q2 |
| 〃 | 9 일정과 잇기 | 이번 범위 아님(D-02 · 화면 없음 D-01) |
| 〃 | 10 목록 순서 | KOS 배열 순서(`seq`)를 그대로 쓴다. 정렬해 바꾸지 않는다(§3.2 · §6.3) |
| 〃 | 11 기기/약물 구분 | 응답에 내지 않는다(D-27). DB `raw` 에 있다(§3.2) |
| 〃 | 12 스펙과 실제의 차이 | 실제 응답 기준으로 저장한다(`raw` 그대로). SINGLE 진료항목 누락은 코디 Q4 로 채운다 |
| 조사 2 §5 | 1 나눌 기준 · 3 가격 기준 · 4 삭제된 옵션 | D-08 · D-09 · D-08 |
| 〃 | 2 원천 · 6 남은 장수 · 7 저장 | D-12(묶음만 · 묶음 AVAILABLE 장수 · 매번 KOS) — §4.3 |
| 〃 | 5 같은 이름 · 다른 id | 이름으로 잇지 않는다 — 시술권 `optionId` 를 그대로 준다(D-08 · §4.3) |
| 조사 4 §3 | 1 ~ 8 | D-22 · D-16 · D-17 · D-18 · D-20 · D-19 · D-15 · D-14 |

## 부록 D. DEC-011 대응표 (D-01 ~ D-16 → 이 문서 · 빠짐 0 · 0.3.0 · D-15 는 0.3.1 · D-16 은 0.3.2)

| D | 결정(줄임) | 반영한 곳 |
|---|---|---|
| D-01 | 셋 다 `/api/ext` · 인증 · 제한 · 기록 · no-store · tag · 오류 모양 공유 | §1.1 I6 · §6.2 · §6.6 ~ §6.8 · §7.3 · §8 · §9 T29 · T44 |
| D-02 | 가능 시간대 = 기본 그룹 하나 · 간격 칸 · 시작 · 남은 자리 · 0 뺌 · 지난 시각 뺌 · 예약 정원 검사와 같은 규칙 | §6.6 4 · 5 · 「같은 규칙인 까닭」 · 응답 표 · §9 T32 · T33 · T37 |
| D-03 | 과거 시술 = 지금 앞 · 최신 순 · 날짜 · 시작 · 결과 · 시술 이름 · 메모 · 의사 안 냄 | §6.7 · §9 T38 |
| D-04 | 예약 내역 = 오늘(KST) 이후 · 오름차순 · 상태(취소 포함) | §6.8 3 · 4 · §9 T40 |
| D-05 | 고객 찾기 = DEC-010 조회 규칙 · 404 바이트 같음 | §6.7 1 · §6.8 1 · §9 T39 |
| D-06 | 이름 · 이메일은 본문 POST | §6.6 요청(GET 은 날짜만) · §6.7 요청 · §9 T42 |
| D-07 | 경로 셋(코디 기본값) | §0 · §1.1 I6 · §6.6 ~ §6.8 머리 · §8 |
| D-08 | 날짜 범위 오늘 ~ 90일 · 그 밖 400(코디 기본값) | §6.6 1 · 오류 표 · §9 T34 |
| D-09 | 설정 빔 · 그룹 없음 · 켜진 구역 0 = 503(코디 기본값) | §6.6 2 · 오류 표 · §9 T35 |
| D-10 | 과거 시술 최근 50건(코디 기본값) | §6.7 4 · §9 T38 |
| D-11 | 후보 시각 = 운영 구간 안 간격 줄 · 남은 자리 = 켜진 구역 합 · 행 없는 구역 뺌 · 모두 없으면 시각 뺌(Q1) | §6.6 4 · 5 · §9 T32 |
| D-12 | 요청마다 슬롯 1번 · 공유 사본 바꿈 · 실패 502 · KOS 1번(Q2) | §6.6 3 · 오류 표 · §6.9 · §9 T36 · T43 |
| D-13 | 예약 내역 칸 · 일정 읽기 1번 · 예약 id = 사본 있으면 · 상태 = 2계층 주 상태(Q3) | §6.8 2 · 5 · 응답 표 · §9 T40 |
| D-14 | 오늘 겹침 그대로 · SPEC · Swagger 에 적음(Q4) | §6.7 · §6.8 「오늘 겹침」 · §8 · §9 T41 · T29 |
| D-15 | `deleted: true` 일정은 과거 시술 · 예약 내역에서 뺌(사본 쓰기와 같은 규칙 · Q-add1-A) | §6.7 3 · §6.8 3 · §9 T38 · T40 |
| D-16 | 일정 원소 모양이 깨지면 두 경로 `502 kos_unavailable`(원문 0) | §6.7 2 · §6.7 오류 · §6.8 2(같은 규칙) · §9 T47 |

## 부록 E. planner 질문 → 코디 답 (add1 · 2026-11-12)

코드 사실(main `e0e4a16`)을 보고 DEC-011 승인 결정만으로 정해지지 않아 물은 넷이다. 코디가 「4개 모두 추천대로」로 답했고(msg_ad6deebe3459), DEC-011 에 **코디 기본값(planner 질문 Qn)** 으로 D-11 ~ D-14 가 됐다.

| Q | 물은 것 | 답 | DEC-011 | 반영 |
|---|---|---|---|---|
| Q1 | 가능 시간대 후보 시각 · 슬롯 행이 없을 때 | 운영 구간 안 간격 줄 · 켜진 구역 남은 자리 합 · 행 없는 구역 뺌 · 모두 없으면 시각 뺌 | D-11 | §6.6 4 · 5 |
| Q2 | 신선도 · KOS 비용(사본만 · 날짜 캐시 · 슬롯 직접) | 요청마다 슬롯 1번 → 공유 사본 바꿈 · 실패 502 | D-12 | §6.6 3 · §6.9 |
| Q3 | 예약 내역 칸 · 우리 사본에 없는 KOS 예약 | 일정 읽기 1번 · `reservationId` 사본 있으면 · 없으면 null · 상태 = 2계층 주 상태 | D-13 | §6.8 |
| Q4 | 오늘 지난 일정이 두 목록에 겹침 | 글자 그대로 두고 적는다 | D-14 | §6.7 · §6.8 · §8 |
| Q-add1-A | (문서 검수 add1 W2) KOS 일정 `deleted: true` 를 두 목록에서 뺄지 | 뺀다(사본 쓰기 `apply_schedule` 과 같은 규칙) — 코디 기본값 | D-15 | §6.7 3 · §6.8 3 |
| N1(코드 검수 add1 r1) | 일정 원소 모양이 깨지면 500 그대로 · 원소 건너뜀 · 502 중 무엇 | 502 `kos_unavailable`(원문 0) — 코디 기본값 | D-16 | §6.7 2 · §9 T47 |
