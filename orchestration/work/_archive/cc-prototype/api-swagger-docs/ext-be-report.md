# WORK-012 BE1 ~ BE6 결과 보고 — 시술 · 상품 메뉴 저장 + 외부 연동 API(`/api/ext`) + Swagger

## 상태: done (커밋 · push · PR 안 함 — 워크트리 변경만)

- 워크트리 `/Users/kknaks/orca/workspaces/cc-prototype/api-swagger-docs` · 브랜치 `kknaksss/api-swagger-docs` · base `c9f30ac`
- 계약 = SPEC-008 0.2.0 + 코디 보정 1(`be-amend-1.md` N1 · N2 · N3 — §6 에 반영 여부)

## 1. 변경 파일 · WP 별 무엇

| WP | 파일 | 무엇 |
|---|---|---|
| BE1 | `app/repository/db.py` | `MENU_SCHEMA`(표 9 · 인덱스 2: `menu_option(product_kos_id)` · `menu_composition(option_kos_id)`) · `EXT_SCHEMA`(`ext_call` · 인덱스 `at`) · `Database.__init__` 에 `executescript` 한 줄 |
| BE1 | `app/repository/repo.py` | `upsert_composition` · `mark_absent_compositions`((`option_kos_id`, `seq`) 키) · `upsert_target_country` · `mark_absent_target_countries`(`raw` 키) · `set_option_medical_service` · `menu_rows` · `add_ext_call` · `ext_calls`. kos_id 표는 기존 `upsert` · `mark_absent_kos` 재사용 · 되살림 = upsert 칸 `present: True` |
| BE1 | `app/kos/menu_sync.py`(새) | 작업 ① ~ ⑧ · 작업마다 독립 · ② 성공 때만 ③ · ③ 은 `OPTION_BATCH`(=100)개씩 다 받은 뒤 한 번에 반영(실패면 안 바꿈 · 빠진 옵션 이전 값) · 상품 · 옵션 · 구성 한 트랜잭션 · `raw` = 원본 `json.dumps`(상품 `options` · 옵션 `compositions` 만 뺌) · `sync_state("menu")` · 잠금 |
| BE1 | `app/kos/runtime.py` | `KosRuntime.menu` · `master_once()` 에서 `resv.master()` 다음에 `menu.run()`(조회 시간 무관 · 서버 시작 1회 포함) |
| BE2 | `app/config.py` · `procedure/.env.example` | env 3(`PROC_EXT_KEY_LINKY` · `PROC_EXT_KEY_CHARTY` · `KOS_EXT_RESERVATION_GROUP_ID`) — 예시 파일엔 이름만 빈 값 |
| BE2 | `app/domain/errors.py` | `ServiceUnavailable`(503) |
| BE2 | `app/api/ext.py`(새) | `require_ext_key`(헤더 `X-Api-Key` · `hmac.compare_digest` · 빈 env 연동처 제외 · `request.state.ext_client` · 키당 60/60초) · `ext_middleware`(IP 차단 → 응답 → 연동처 없는 오류면 IP 카운트 → `ext_call` 1줄 → `Cache-Control: no-store`) · 라우터 셋 · 응답 표 · 설명 |
| BE2~5 | `app/service/ext.py`(새) | `ExtService` — 키 대조 · `RateLimiter` 재사용 · 기록(연동처 없는 오류 같은 IP · 같은 결과 1분 1줄 · 쓰기 실패는 응답 그대로) · 메뉴 트리 · `find()`(조회 · 예약 같이 씀) · `lookup()` · `reserve()` |
| BE2 | `app/main.py` · `app/container.py` | 미들웨어 · 라우터 등록 · `c.ext` |
| BE3 | `app/schemas/ext.py`(새) | 요청(모르는 키 400 · 빈 이름 · 이메일 400 · `start` ISO 검사) · 응답 모델 · 모든 칸 `description` |
| BE5 | `app/service/reservations.py` | 행위자 겹 — `create` · `_new_visitor` · `kos_write` · `_event` 의 `actor: Account \| str` · `_event` 한 곳에서 문자열은 그대로 · `Account` 는 `login_id`(부르는 곳 0 줄 변경) |
| BE6 | `app/api/docs.py` | `T_EXT = "외부 연동"` · `STATUS_TEXT` 503 「지금 쓸 수 없음」 · 405 「허용하지 않는 메서드」(보정 1 N1 의 405 줄 머리) |
| BE6 | `app/openapi_docs.py` | tag 설명 · `ExtApiKey` securityScheme · `require_ext_key` 의존 operation 에 `security [{ExtApiKey: []}]`(Bearer 안 닮) · `DESCRIPTION` `## 외부 연동 API` 절(첫 줄 = email 없는 고객 문장) |
| 시험 | `tests/fake_kos.py` | 메뉴 8 작업 · `get-ticket-bundles` 응답 · `get-visitors` 통째 응답(`visitors_page`) · `find-duplicated-visitor` 이메일 일치. **이름 검색 규칙(공백 그대로 · 부분 일치)은 안 고침**(보정 1 N2) |
| 시험 | `tests/ext_env.py`(새) · `tests/test_ext_{menu_sync,auth,menu,lookup,reserve,docs}.py`(새) | §3 표 |
| 시험 | `tests/test_kos_sync.py` · `tests/test_openapi_docs.py` · `tests/test_order.py` | 고친 단언 3곳 — §6 「기존 시험 고침」 |

## 2. 수치

| | 기준선(시작 전 · `c9f30ac`) | 이후(BE6 끝 한 번) |
|---|---|---|
| `uv run pytest -q` | **544 passed** | **588 passed**(+44 · 실패 0) |
| `uv run ruff check .` | All checks passed | All checks passed |

WP 별 부분 시험(WORK-012 명령): BE1 `test_ext_menu_sync + test_kos_sync` 22 · BE2 `test_ext_auth + test_auth_roles` 27 · BE3 `test_ext_menu + test_ext_auth` 16 · BE4 `test_ext_lookup + test_resv_detail` 29 · BE5 `test_ext_reserve + test_resv_write + test_resv_reception` 94 · BE6 `test_openapi_docs + test_ext_docs` 9 — 모두 통과.

public grep: 변경분(diff + 새 파일)에 데모 `.env` 값 **0** · 이메일은 모두 `example.com`(`a@example.com` 꼴) · 이름은 지어낸 값(「고객」 · 「가나다」 등) · 키는 시험 전용 문자열.

## 3. SPEC §9 시험 대조

| T | 시험 |
|---|---|
| T1 | `test_ext_menu_sync::test_t1_tables_and_raw_kept` |
| T2 | `test_ext_menu_sync::test_t2_product_options_batched_and_missing_keep` · `::test_t2_product_options_failure_keeps_values` · `::test_t2_no_products_no_options_call` |
| T3 | `test_ext_menu_sync::test_t3_absent_and_revive` · `::test_t3_kos_flags_kept_as_present` |
| T4 | `test_ext_menu_sync::test_t4_failure_keeps_tables_others_applied` |
| T5 | `test_ext_menu_sync::test_t5_master_once_and_startup_out_of_window` · `test_kos_sync::test_out_of_window_no_queries`(메뉴 호출 순서) |
| T6 | `test_ext_menu::test_t6_fields_and_hidden` · `::test_t6_empty_before_sync_and_synced_at_kept`(보정 1 N3 — 성공 → 작업 하나 실패 → `syncedAt` 그대로) |
| T7 | `test_ext_menu::test_t7_only_live` |
| T8 | `test_ext_menu::test_t8_list_price` |
| T9 | `test_ext_lookup::test_t9_one_page_dedupe_and_cap` |
| T10 | `test_ext_lookup::test_t10_name_strip_only` |
| T11 | `test_ext_lookup::test_t11_email_rules` |
| T12 | `test_ext_lookup::test_t12_exact_name_and_branches`(공백 경우 = 가짜 KOS 응답 직접 지정) · `::test_t12_kos_search_keeps_middle_space`(보정 1 N2 — 가운데 공백 다른 입력 → KOS 0건 → 404) |
| T13 | `test_ext_lookup::test_t13_not_found_bytes_identical`(여섯 경우 상태 · 본문 바이트 같음) |
| T14 | `test_ext_lookup::test_t14_no_tickets_vs_no_customer_vs_failure` |
| T15 | `test_ext_lookup::test_t15_ticket_line` |
| T16 | `test_ext_lookup::test_t16_customer_fields` |
| T17 | `test_ext_reserve::test_t17_existing_customer_and_actor` |
| T18 | `test_ext_reserve::test_t18_new_customer` |
| T19 | `test_ext_reserve::test_t19_ambiguous_and_duplicated` |
| T20 | `test_ext_reserve::test_t20_not_configured[empty · absent · no_zone · unknown]` |
| T21 | `test_ext_reserve::test_t21_slot_full_and_kos_failure` |
| T22 | `test_ext_reserve::test_t22_request_fields` |
| T23 | `test_ext_auth::test_t23_key_cases` · `::test_t23_disabled_client` |
| T24 | `test_ext_auth::test_t24_staff_and_ext_separate` |
| T25 | `test_ext_auth::test_t25_check_order`(다섯 경우 + 맞는 키 칸 틀림 400) |
| T26 | `test_ext_auth::test_t26_rate_per_key` · `::test_t26_401_not_counted_per_key` |
| T27 | `test_ext_auth::test_t27_ext_call_rows_and_privacy`(이메일 꼴 경로 · 표 전수 · caplog) · `::test_t27_clientless_collapsed_per_ip_minute`(보정 1 N1 — 401 · 깨진 JSON 400 · 405 각 같은 IP 5번 → 1줄 · 60초 뒤 다시 1줄) · `::test_t27_write_failure_keeps_response` |
| T28 | `test_ext_auth::test_t28_no_store` |
| T29 | `test_ext_docs::test_t29_ext_swagger` · `test_openapi_docs.py` 8개 전부(개수 단언 `n_ops - 5 - 3`) |
| T30 | 기존 시험 전부 통과(588). 직원 `event_log.actor` = `login_id` 는 `test_resv_write`(`ev["actor"] == "desk1"`) · `test_resv_reception` 그대로 통과 |
| T31 | `test_ext_auth::test_t31_ip_block`(401 · 404 · 깨진 본문 400 · 405 섞어 10번 → 맞는 키도 429 · 막힌 요청 안 셈 · 60초 뒤 열림 · 다른 IP 무관 · CF 우선) · `::test_t31_valid_key_errors_not_counted` |

## 4. 데모 실물 확인(조회만 · 값 0 · 수만)

데모 `.env` 를 env 로만 읽어 스크립트(KosClient 실물 · 임시 DB = scratch)로 1회씩. KOS 쓰기 0 · 운영 키 0 · 사용자 포트 · 프로세스 0. 임시 DB 는 끝나고 지움.

**BE1 메뉴 동기화 한 바퀴** — `run()` = True · 0.79초 · `sync_state("menu")` last_ok 있음 · last_error 없음.

| 표 | 행 | 조사 1 §4 |
|---|---:|---:|
| menu_category | 15 | 15 |
| menu_product | 101 | 101 |
| menu_option | 323(SINGLE 307 · GROUP 16) | 323 |
| menu_composition | 32 | 32 |
| menu_procedure | 804 | 804 |
| menu_medical_service | 226 | 226 |
| menu_machine | 302 | 302 |
| menu_medicine | 349 | 349 |
| menu_target_country | 4 | 4 |

- SINGLE 옵션 진료항목 채움 **307/307**(그 진료항목이 `menu_medical_service` 에 있음 307/307 · 단위가 있는 것 188/307 → 나머지는 메뉴 응답 `unit` null)
- **공개 경로 8**(KOS `openapi.yaml` 1.0.1 operationId 에서 옮김 · SPEC §4.1 표 경로와 다름 → 스펙이 맞다):
  - `getCategories` `procedure-menu/open/categories/queries/get-categories`
  - `getProducts` `procedure-menu/open/products/queries/get-products`
  - `getProductOptions` `procedure-menu/open/v1/product-options/queries/get-product-options`
  - `getProcedures` `procedure-menu/open/v1/procedures/queries/get-procedures`
  - `getMedicalServices` `procedure-menu/open/v1/medical-services/queries/get-medical-services`
  - `getMachines` `procedure-menu/open/v1/machines/queries/get-machines`
  - `getMedicines` `procedure-menu/open/v1/medicines/queries/get-medicines`
  - `getTargetCountries` `procedure-menu/open/target-countries/queries/get-target-countries`
  - (시술권) `getTicketBundlesQuery` `ticket/open/v1/queries/get-ticket-bundles` — SPEC 과 같음
- **N = 100**(`menu_sync.OPTION_BATCH`). 근거: KOS 스펙 `GetProductOptionsQuery.optionIds` 는 `minItems: 1` 만 있고 상한이 없다. 데모 실측 — 307개 한 번 = 200 · 307개 응답 / 100개씩 4번 = 모두 200 · 합 307. 상한이 문서에 없어 한 번 요청 크기를 줄이려고 100 을 골랐다(데모 SINGLE 307 → 4번)

**BE4 고객 조회** — 데모 고객 494명 중 email(`@` 포함) 보유 4명. 그중 1명:
- 맞는 이름 + 이메일 → **200** · 응답 키 `{customer, tickets}` · `customer` 키 `{customerId, isNew, lastVisitDate, name}` · 시술권 4줄 · 줄 키 `{bundlePrice, optionId, optionTitle, purchasedDate, remainingCount, totalCount}`
- 이메일 한 글자 틀림 → **404 `customer_not_found`**
- `ext_call` 2줄(`linky` · `POST /api/ext/customers/lookup` · 200 ok / 404 customer_not_found)
- **`lastVisitedDateTimeUtc`: 있음** — `get-visitors` 원소 494/494 에 키가 있고, 값이 비지 않은 것은 191/494(그 고객은 `lastVisitDate` 가 null 이 아님)
- 주의(하네스): 첫 실행은 502 가 섞였다. 원인은 시험 하네스 — 이름 검색 원소를 `asyncio.run` 으로 먼저 읽은 뒤 lifespan 없는 TestClient(요청마다 다른 이벤트 루프)로 부르면 같은 httpx 연결 풀을 다른 루프에서 다시 써서 실패한다. keep-alive 를 끈 클라이언트로 한 번 다시 돌려 위 결과를 얻었다(운영은 루프 하나라 해당 없음). 데모 호출은 모두 조회

## 5. Swagger

- tag **`외부 연동`**(설명 = SPEC §8 문구 그대로) — 세 operation 이 이 tag 하나만
- `components.securitySchemes.ExtApiKey = {type: apiKey, in: header, name: X-Api-Key, description: SPEC 문구}` · `BearerAuth` 그대로
- 세 operation `security = [{ExtApiKey: []}]` · Bearer 없음. 직원 operation 에 ExtApiKey 0
- 401 표 = `ext_unauthorized` 한 줄(「직원 로그인이 아니라 `X-Api-Key` …」로 시작) · 429 · 405 `http_error` · 조회 404(「모두 같은 응답」) · 409 · 502 · 예약 409 셋 · 502 · 503(머리 「지금 쓸 수 없음」 · `ext_not_configured`)
- 설명: 조회 = 이름 · 이메일 대조 규칙 · 「없음 = 같은 응답」 · `bundlePrice` 성질 셋 · `AVAILABLE` 0 묶음 없음 · `IN_USE` 안 셈 / 예약 = **D-35 문장** · 1 / 0 / 2+ · 503 / 메뉴 = `syncedAt` 뜻 · 지금 있는 것만
- 앱 설명 `## 외부 연동 API — /api/ext/*` 절 — 첫 줄 = email 없는 고객 문장 · 경로 셋 · `X-Api-Key` · 연동처별 키 · 직원 API 분리 · 검사 순서 · 제한(키당 · IP 당) · 기록 · 공통 오류 · 금액 · id
- 직원 API 문서 무변경 확인: 앞 판 `openapi-after.json` 과 견줘 직원 경로 차이 **0** · 기존 스키마 차이 **0** · 새 경로 3 · 새 스키마 14 · tag 12 → 13

## 6. SPEC ↔ 코드 차이 · 확인 못 한 것 · 코디가 볼 것

**보정 1 반영**
- **N1 반영**: IP 카운트 · 「같은 IP · 같은 결과 1분 1줄」은 `request.state` 에 연동처가 없는 `/api/ext` 오류 응답 **전부**(401 · 404 · 깨진 JSON 400 · 405 · IP 차단 429)에 건다. 막힌 요청(IP 차단 429)은 카운트에 더하지 않는다. Swagger 세 operation 에 `405 http_error` 줄 · `STATUS_TEXT[405]` 「허용하지 않는 메서드」 추가(SPEC 에는 503 만 적혀 있었다 — 405 머리 문구는 내가 정함)
- **N2 반영**: `fake_kos` 검색 규칙 무수정 · T12 공백 경우 = 응답 직접 지정 · 가운데 공백 다른 입력 → 0건 → 404 시험 추가 · 조회 · 예약 설명과 `name` 칸 설명에 「KOS 에 등록된 띄어쓰기 그대로 보내야 한다」(「공백 무시」 약속 없음 — 우리 쪽 대조는 KOS 가 돌려준 고객 안에서만 공백 · 대소문자를 무시)
- **N3 반영**: `set_sync("menu", None, …)` 는 이전 `last_ok_at` 을 남긴다(기존 `set_sync` 동작) · 시험으로 고정

**SPEC 과 다르거나 SPEC 에 없어 정한 것**
1. 메뉴 공개 경로 8개 = KOS 스펙 경로(§4 목록) — SPEC §4.1 표의 경로 모양과 다르다(SPEC 이 「스펙이 맞다」로 열어 둔 자리)
2. IP 차단 429 의 `ext_call.endpoint` = 항상 `"<METHOD> (unknown)"` — 라우터에 닿기 전에 막아 매칭 라우트가 없다
3. 응답 null 허용 몇 칸: 구성 `unit` · `procedure` · `listPriceExVat`, 옵션 `procedure`(SINGLE 이라도 KOS 가 안 주면) — KOS 가 칸을 주지 않을 때만 null(데모는 다 있음). `ExtUnit.value` 도 KOS 가 안 주면 null
4. 시술권 묶음에 `price.value` 가 없으면(KOS 필수 칸) 응답 모양 오류로 보고 `502 kos_unavailable`
5. 통화가 비면(`currency` 없음) 빈 문자열 그대로 — 지어 `KRW` 를 넣지 않음
6. 새 고객 갈래에서 KOS 로 보내는 이름 · 이메일 = 앞뒤 공백만 지운 원문(이메일 대소문자 그대로)
7. 앱 로그에 호출마다 INFO 1줄 「외부 호출 <연동처> <경로 틀> <상태>」(이름 · 이메일 · 키 · IP 없음)

**기존 시험 고침(직원 동작 아님 · 목록 · 개수 단언)**
- `test_kos_sync::test_out_of_window_no_queries` — 서버 시작 KOS 호출 목록 단언에 메뉴 작업 7개(빈 메뉴라 ③ 없음)를 뒤에 더함
- `test_openapi_docs::test_bearer_security_matches_require_login` — `n_ops - 5` → `n_ops - 5 - 3`(SPEC §8)
- `test_order::test_route_count_71` — 새 `/api/ext/reservations` · `/api/ext/customers/lookup` 이 「`/reservations` · `/customers` 가 든 직원 경로 16」 필터에 걸려 18 이 됨 → 외부 셋을 따로 세고(정확히 셋) 직원 수 단언(16 · 51 · 71)은 그대로 · 총 74 단언 추가

**확인 못 한 것 · 볼 것**
- KOS 쓰기(예약 · 새 고객)는 데모에서 부르지 않았다 — WP-E2E-LOCAL 몫. 가짜 KOS 의 `find-duplicated-visitor` 이메일 일치는 조사 4 §2(`findDuplicatedVisitorId` 「저장된 이메일 주소와 일치」)에 맞춘 흉내다
- `getProductOptions` 개수 상한은 문서에 없음 · 데모 307개 한 번까지만 봤다
- 운영 지점의 email 채움 비율 · `lastVisitedDateTimeUtc` 비율은 보지 않았다(데모만)
- 앞 판 문서의 사소한 흠: `openapi_docs.DESCRIPTION` 「역할」 절에 같은 문장 한 줄이 두 번 있다(이번 범위 밖이라 그대로 둠)

## 수정 1 (코드 검수 r1 WARN — `ext-be-fix-1.md`)

| # | 무엇 | 자리 · 시험 |
|---|---|---|
| W1 | 이름 검색 2xx 인데 `data` 가 없거나 배열이 아니면 `502 kos_unavailable`(「없음」 404 · 새 고객 갈래로 가지 않음). `count` 상한 판정보다 먼저 본다 | `service/ext.py` `find()` · `test_ext_lookup::test_lookup_search_bad_shape_502`(5경우 · 시술권 0번) · `test_ext_reserve::test_reserve_search_bad_shape_502_no_create`(4경우 · 중복 검사 · `create-visitor` · `reserve` 0번) |
| W2 | 앱 설명 외부 절 email 문장 다음 줄 「이름은 KOS 에 저장된 띄어쓰기 그대로 보내야 한다(띄어쓰기가 다르면 찾지 못해 `404`).」 | `openapi_docs.py` · T29 단언 |
| W3 | 예약 502 줄 = 「KOS 네트워크 · 5xx · 401 · 응답 형식(예약 쓰기 · 고객 만들기 · 중복 검사) · 이름 검색은 4xx 도 502 · 예약 응답에 일정 id 없음」(「다시 읽기」 뺌) · 409 `kos_rejected` 줄에 「중복 검사 · 고객 만들기 · 예약 쓰기 단계」 | `api/ext.py` · T29 단언 |
| W4 | 400 줄 분리 — 조회 = `start` 없음 · 예약 = `start` 있음 | `api/ext.py` `LOOKUP_INVALID` · `RESERVE_INVALID` · T29 단언 |
| W5 | `require_ext_key` → `async def`. 미들웨어(`ext_middleware`)도 `async` 로 이벤트 루프 스레드에서 돈다 → 키당 · IP 카운터는 한 스레드에서만 만진다(문진 웹 `_gate` 는 범위 밖 · 그대로) | `test_ext_auth::test_w5_concurrent_requests_never_exceed_limit` — ASGITransport 150 동시 요청 · `_recent` 에 1ms 지연 주입 → 200 정확히 60 · 429 90. **같은 시험을 `def` 로 되돌려 돌리면 150 모두 200 으로 실패함을 확인**(되돌린 뒤 원복) |
| W6 | 미들웨어 `call_next` 예외 → `ext_call` 1줄(그 연동처 · 경로 틀 · 500 · `internal_error`) + `500 {"error":{"code":"internal_error","message":"서버 오류가 났어요"}}` + `no-store`. 본문 · 로그에 예외 문구 없음 · 로그엔 예외 종류만 | `api/ext.py` · `test_ext_auth::test_w6_unhandled_error_logged_and_no_store` |
| W7 | SPEC 몫 — 코드 그대로 | — |

수치: 전체 `uv run pytest -q` **599 passed**(588 → +11) · `uv run ruff check .` All checks passed. KOS 호출 · 사용자 포트 0 · 커밋 0.

## 수정 2 (검수 r2 N1)

- 문서만: 앱 설명 외부 절 공통 오류 줄에 「처리하지 못한 예외 = `500 internal_error`(본문에 예외 문구 없음 · 호출 기록 1줄 · IP 카운트 안 함)」 · 세 operation 응답 표에 `500 internal_error` 줄(`STATUS_TEXT[500]` 「서버 오류」 추가 · 직원 경로에 500 줄 없음 → 직원 문서 무변경) · T29 단언 2개 — 코드 동작 변경 0 · 전체 pytest **599 passed** · ruff All checks passed.
