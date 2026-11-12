# 리뷰 리포트 — WORK-012 외부 연동 API(`/api/ext`) · 메뉴 저장 / code (2026-11-11 · r1)

- 대상: 워크트리 `/Users/kknaks/orca/workspaces/cc-prototype/api-swagger-docs` · base `c9f30ac` · 미커밋 변경(수정 15 + 새 파일 11 — 모두 `procedure/` 안)
- 기준: SPEC-008 **0.2.1**(부록 A D-01 ~ D-36 · 부록 B) · WORK-012 WP-REVIEW 점검 목록 · `ext-be-report.md` · `be-amend-1.md`(N1 ~ N3)
- read-only. 서버를 띄우지 않았고, KOS 호출과 사용자 포트도 쓰지 않았다. 확인용 스크립트는 scratchpad 의 TestClient · 가짜 KOS 로만 돌렸다.

## 판정: **WARN** (FAIL 0 · WARN 7)

결과는 SPEC 0.2.1 과 대체로 맞는다. 보안 · 개인정보 축, 「없음」 바이트 일치, 행위자 겹, 메뉴 동기화(N3 포함), 직원 동작 불변은 모두 실물로 맞음을 확인했다. 머지 전에 고칠 것은 **W1**(KOS 이름 검색 응답 모양 오류를 「0명」으로 처리 — 실물 재현됨)이다. 나머지는 문서 문구 · 경계 사례 · SPEC 갱신 몫이다.

### 수치(직접 1회씩 실행)

| | 결과 |
|---|---|
| `uv run pytest -q`(`procedure/back`) | **588 passed** · 1 warning(httpx 사용 중단 경고) · 59.98s — be 리포트 588 과 같음 |
| `uv run ruff check .` | All checks passed |
| 직원 OpenAPI 차이(`openapi-after.json` ↔ 지금 `app.openapi()`) | 직원 경로 차이 **0** · 기존 스키마 차이 **0** · 새 경로 3 · 새 스키마 14 · tag 12 → 13 · `BearerAuth` 그대로 · 앱 설명은 더한 줄만 있고 지운 줄은 0 |
| public grep(diff + untracked 2406줄) | 이메일 = `example.com` 꼴만 · IP = RFC 5737 문서용만 · 긴 숫자 = 지어낸 전화 `1000000000` · URL 0 · 키 꼴 문자열 0 · 실명 0 |

---

## FAIL

없음.

## WARN

| # | 자리 | 무엇이 문제인가 · 근거 | 고칠 방향 |
|---|---|---|---|
| **W1** | `app/service/ext.py:172-186` | **KOS 이름 검색(`get-visitors`) 2xx 응답 모양이 깨져도 「0명」으로 처리한다.** `resp.get("data") or []` 이라서 `data` 가 없거나 배열이 아니면 후보가 0명이 된다. 그러면 **조회는 `404 customer_not_found`** 가 되고, **예약은 「새 고객」 갈래로 들어가 KOS 에 고객을 새로 만들고 예약까지 한다**. 실물 재현(가짜 KOS · scratchpad `verify_w.py`): `{"count":0}` · `{"data":{"x":1}}` · `{"items":[]}` → 셋 다 404. `{"data":null}` 에서 예약 → **200 · `create-visitor` 1번**. SPEC §7.5 「KOS 내부 API 조건이 바뀌면 고객 조회 · 예약이 `502 kos_unavailable` 로 멈춘다」 · §4.3 「모양 오류 = 502」(시술권) · D-14(「없음」과 「실패」를 섞지 않음)의 취지와 어긋난다. 내부 API 는 D-15 가 「바뀔 수 있다」고 적은 자리다. 이름 검색의 모양 오류는 SPEC §4.2 에 따로 적혀 있지 않아 WARN 으로 둔다 | `data` 가 배열이 아니면(키가 없는 경우 포함) `BadGateway("kos_unavailable")` 로 낸다(`reservation_sync._data_list` 와 같은 규칙). `test_ext_lookup` · `test_ext_reserve` 에 「`data` 없음 · 배열 아님 → 502 · `create-visitor` 0번」 시험을 더한다. SPEC §4.2 「실패」 줄에 「2xx 인데 `data` 가 배열 아님 = 502」를 더한다(planner) |
| **W2** | `app/openapi_docs.py:73-74` | **앱 설명 외부 절에 이름 띄어쓰기 문장이 빠졌다.** SPEC 0.2.1 §8 「앱 설명」은 첫 줄(email 없는 고객) 바로 다음에 「이름은 KOS 에 저장된 띄어쓰기 그대로 보내야 한다(띄어쓰기가 다르면 찾지 못해 `404`).」를 둔다. 지금은 엔드포인트 설명(`api/ext.py:110`)과 칸 설명(`schemas/ext.py:8`)에만 있다. 보정 1 N2 는 「조회 · 예약 설명」만 말했고, 앱 설명 문장은 0.2.1 에서 더해졌다 | `DESCRIPTION` 의 email 문장 다음 줄에 SPEC 문장을 그대로 넣는다. T29 에 그 문장 단언 한 줄 |
| **W3** | `app/api/ext.py:174-176` | **예약 `502` · `409 kos_rejected` 오류 줄이 실제와 다르다.** ① 이름 검색(`find`)은 KOS **4xx 도 502** 다(`service/ext.py:167-171` 이 모든 예외를 502 로 바꾼다). 그런데 표는 502 = 「네트워크 · 5xx · 401 · 응답 형식」, 409 `kos_rejected` = 「KOS 가 4xx(401 제외)로 거절」이라고 적어서, 검색 단계 4xx 가 409 로 읽힌다. ② 「다시 읽기 어디서든 502」는 거짓이다. 다시 읽기(`refresh_schedule`)는 실패를 삼키고 None 을 돌려준다(`service/reservations.py:738-747`). 그러면 사본 행을 직접 만들어 200 이 나간다(`:847-852`). 502 는 응답에 `scheduleId` 가 없을 때만 난다. SPEC §6.5 오류 표 502 줄도 같은 문구다(SPEC 쪽 흠을 그대로 옮김) | 502 줄 = 「KOS 네트워크 · 5xx · 401 · 응답 형식(예약 쓰기 · 고객 만들기 · 중복 검사) · 이름 검색은 4xx 도 502 · 예약 응답에 일정 id 없음」. 409 `kos_rejected` 줄에 「중복 검사 · 고객 만들기 · 예약 쓰기 단계」를 붙인다. SPEC §6.5 502 줄도 같이 고친다(planner) |
| **W4** | `app/api/ext.py:89-91` · `:161` | 조회(`lookup`) 400 표가 예약과 같은 `EXT_INVALID` 를 써서 **「ISO 가 아닌 `start`」** 가 들어 있다. 조회 요청에는 `start` 가 없다(`schemas/ext.py:24-30`). 지어낸 설명 1줄 | 조회용 400 줄을 따로 두거나 `start` 부분만 예약 줄에 붙인다 |
| **W5** | `app/api/ext.py:31` · `app/service/questionnaire.py:73-95` | **키당 · IP 카운터가 원자적이지 않다(동시성).** `require_ext_key` 가 `def`(동기)라 FastAPI 가 스레드 풀에서 돌린다. `RateLimiter._recent` 는 읽고 → 걸러서 → 다시 쓰고 → 덧붙이는 사이에 잠금이 없다. 미들웨어(이벤트 루프 스레드)도 같은 `_hits` 를 만진다. 그래서 동시 요청 사이에 끼어들기가 일어나면 횟수를 잃어 60 을 넘겨 통과할 수 있다. 실측(ASGITransport 로 150 동시 요청): 보통 실행 3번은 **200 60 · 429 90 으로 정확**했다. `_recent` 안에 1ms 지연을 넣어 끼어들 틈을 넓히면 **150 모두 200** 이었다. 지금 부하에서는 드물다. 브리프 축 4 「다중 요청 동시성(락)」 | `require_ext_key` 를 `async def` 로 바꾼다(안에서 막히는 I/O 가 없다 — 키 비교 · 메모리 카운터뿐). 그러면 모든 카운터 접근이 이벤트 루프 한 스레드에서 일어난다. 또는 `ExtService` 에 `threading.Lock` 을 둔다. 문진 웹 `_gate` 도 같은 클래스를 쓰니 함께 보면 좋다(이번 범위 밖) |
| **W6** | `app/api/ext.py:64` | **처리하지 못한 예외(500)가 나면 `ext_call` 행도 `Cache-Control: no-store` 도 없다.** `call_next` 가 예외를 다시 던져서 기록 · 헤더 단계를 건너뛴다. 실물 재현: `c.ext.menu` 가 예외를 던지게 하면 → 500 · `cache-control` None · `ext_call` 0행. SPEC §7.4 「`/api/ext/…` 로 들어온 모든 요청마다 1줄」 · §6.1 「모든 응답(오류 포함) no-store」 | `call_next` 를 try 로 감싼다. 예외면 `record(ip, client, endpoint, 500, "internal_error")` 를 남기고 `500 {"error":{"code":"internal_error",…}}` + `no-store` 로 응답한다(본문에 예외 문구를 싣지 않는다). 로그에는 예외 종류만 남긴다 |
| **W7** | `app/schemas/ext.py:70-77` · `:62` · `:93` | **SPEC 갱신 몫(코드는 그대로 둬도 됨).** be 리포트 §6 「정한 것」 3번에 따라 구성 `count` · `unit` · `listPriceExVat` · `procedure`, 옵션 `procedure`, `ExtUnit.value` 를 null 이 될 수 있게 했다. SPEC §6.3 은 구성 칸 타입을 null 없이(`string · int` · `{type, value}` · `{value, currency}` · `{id, name}`) 적는다. KOS 가 칸을 주지 않을 때만 null 이 되고, 데모에서는 모두 값이 있었다. 지어 채우지 않는 쪽이 D-08 · D-29 「KOS 그대로」에 맞으므로 코드는 맞다. 계약 문서만 어긋난다 | SPEC §6.3 구성 · 옵션 칸 표에 「KOS 가 주지 않으면 null」을 더한다(planner). 코드 변경 없음 |

---

## be 리포트 §6 「SPEC 과 다르거나 정한 것」 7개 판정

| # | be 주장 | 실물 확인 | 판정 |
|---|---|---|---|
| 1 | 메뉴 공개 경로 8개 = KOS `openapi.yaml` 경로(`procedure-menu/open/…`)로 SPEC §4.1 모양과 다름 | `app/kos/menu_sync.py:24-31` 상수 8개 · 시술권 `ticket/open/v1/queries/get-ticket-bundles`(`service/ext.py:31`) = SPEC 과 같음. SPEC §4.1 이 「스펙의 경로와 다르면 스펙이 맞다 · WP-BE1 리포트에 실제 경로를 적는다」로 열어 둔 자리다. 데모 1바퀴 행 수(조사 1 §4 와 9표 모두 같음)가 경로가 맞다는 근거다(이 리뷰는 KOS 를 부르지 않음) | **PASS** |
| 2 | IP 차단 429 의 `endpoint` = 늘 `"<METHOD> (unknown)"` | `api/ext.py:60-61` — 라우터 전에 막아 `scope["route"]` 가 없다. SPEC §3.4 「매칭된 라우트가 없으면 고정값」의 글자 그대로다. 경로 원문을 남기지 않는 쪽이라 D-24 에 맞는다 | **PASS**(참고: 차단 요청이 어느 경로를 노렸는지는 알 수 없다) |
| 3 | 구성 · 옵션 몇 칸 null 허용 | 위 W7 | **WARN → SPEC 갱신** |
| 4 | 묶음 `price.value` 없음 → `502 kos_unavailable` | `service/ext.py:221-224`. SPEC §4.3 이 `bundlePrice` 를 null 없는 칸으로 두고, 「고객 칸만 주고 시술권을 빈 배열로 주지 않는다」(D-14) 취지에 맞는다. 묶음 하나가 깨져도 조회 전체가 502 가 되는 점은 받아들일 만하다 | **PASS** |
| 5 | `currency` 가 없으면 빈 문자열(지어 `KRW` 를 넣지 않음) | `service/ext.py:134` · `:228`. SPEC §6.1 금액 칸 예시는 `"KRW"` 이지만 KOS 값 그대로(D-08 · D-31)에 맞다. 데모는 다 `KRW` | **PASS** |
| 6 | 새 고객 갈래에서 KOS 로 보내는 이름 · 이메일 = 앞뒤 공백만 지움(이메일 대소문자 그대로) | `service/ext.py:245` · T18(`New@Example.com` 그대로) — SPEC §5 0단계 · §6.5 「`{name, email}` 로」에 맞는다. 다음 조회는 양쪽을 소문자로 바꿔 견주므로 찾힌다 | **PASS** |
| 7 | 앱 로그 INFO 1줄 「외부 호출 <연동처> <경로 틀> <상태>」 | `service/ext.py:96` — 값이 연동처 · `_endpoint`(경로 틀 · unknown) · 상태뿐이다. SPEC §7.4 「앱 로그에는 연동처 · 엔드포인트 · 상태만」과 같다. 1분 1줄로 줄이는 갈래에서는 로그도 남기지 않는다(`:88-89` return) | **PASS** |

**기존 시험 고침 3건**(축 6): 셋 다 단언을 약화하지 않았다.
- `test_kos_sync` — `paths()[5:]` 정확 비교를 `[5:10]` + `[10:]` 둘로 나눴다. 메뉴 7개를 순서까지 단언에 **더한** 것이다.
- `test_openapi_docs` — `n_ops - 5 - 3` 은 SPEC §8 이 정한 값이다. 연산마다 `(security == Bearer) is needs_login` 단언이 외부 셋에서도 그대로 돈다.
- `test_order` — 외부 셋을 정확히 셋으로 단언한 뒤 빼고, 직원 단언 16 · 51 · 71 은 그대로 뒀다. 총 74 단언은 더한 것이다.

---

## 축별 확인(PASS 근거)

**1. 보안 · 개인정보**
- 외부 라우터에 `require_login` · `Actor` 가 0이다(`api/ext.py` import = `Ctr` · `get_container` 뿐). 의존성은 `require_ext_key` 하나다.
- 직원 쪽에서 `X-Api-Key` 를 보는 곳은 0이다(grep — `openapi_docs.py` 문서 문자열 · `_needs_ext_key` 만).
- 키 비교는 `hmac.compare_digest` 이고, 두 연동처를 다 견준다(`service/ext.py:62-70`). 빈 env 연동처는 건너뛴다. 빈 키는 바로 None 이다(T23 `""` · `LINKY+" "` · 꺼진 연동처).
- `ext_call` 칸은 `{id, at, client, endpoint, status, outcome}` 뿐이다(`db.py` EXT_SCHEMA · T27 단언). 표 · caplog 에 이름 · 이메일 · 키 · IP 가 0이다(T27 · T31).
- 로그 · 예외 문자열: `kos_errors.describe` = 상태 · 이름만이고, `KosError` 메시지에 본문이 없다(`kos/client.py:62` 등). 검증 400 message = `<위치>: <pydantic msg>` 로 입력값이 없다.
- 외부 응답: `duplicated_visitor` → `customer_ambiguous` 로 바꾸고 `candidate` 를 버린다(`service/ext.py:250-252`). `step` 은 None 이면 `DomainError` 가 싣지 않는다(`domain/errors.py:11`). 고객 응답 키 = `{customerId, name, isNew, lastVisitDate}` 이고, 전화 · 생년월일 · 여권 · 차트 · 국적 · 성별 · KOS id 는 응답 문자열에 0이다(T16).
- 「없음」 404 는 이름 틀림 · 부분 일치 · 이메일 틀림 · email 빈 고객 · 고객 없음 · `count` 1001 의 **여섯 경우가 상태 + 본문 바이트까지 같다**(T13 `r.content` 집합 크기 1).

**2. 조회 규칙 §5**
- 본문 `countInPage: 1000` · `indexOfPage: 0` 이고 1번만 부른다(T9). `count > 1000` 이면 거르지 않고 「없음」 · 시술권 0번이다(`service/ext.py:173-174`).
- KOS id 로 중복을 없애고 처음 것을 남긴다(`:175-179`).
- 이름 대조는 공백을 전부 지우고 소문자로 바꾼 뒤 `name` · `phoneticName` 둘 중 하나와 맞추며, 빈 칸은 맞지 않은 것으로 본다(`:38-40` · `:181-183`).
- 이메일은 `strip().lower()` 로 정확히 견주고 KOS 쪽 빈 값은 뺀다(T11 `None` · `""` · `"   "`).
- `fake_kos` 이름 검색 규칙(소문자 · 부분 일치 · 공백 그대로)은 diff 에서 바뀌지 않았다. 바뀐 것은 `visitors_page` 통째 응답 갈래와 `find-duplicated-visitor` 의 이메일 일치를 더한 것뿐이다(N2 지킴).

**3. 예약 §6.5**
- 503 네 조건(env 빔 · 사본에 없음 · present 0 → `group_by_kos` 가 present 만 · 켜진 구역 0)을 `find()` 전에 판정하므로 KOS 호출이 0번이다(`service/ext.py:232-238` · T20 4갈래).
- 행위자 겹: `_event` 한 곳만 `isinstance(actor, str)` 로 가르고, 직원 경로는 `Account` → `login_id` 그대로다(`reservations.py:478-480`). 직원 `test_resv_write`(`actor == "desk1"`) · 접수 시험이 통과한다.
- 409 매핑: 2명 이상과 중복 검사 둘 다 `customer_ambiguous` 이고 `reserve` · `create-visitor` 는 0번이다(T19).
- 0명 갈래는 `NewCustomer(name, email)` → `identifiable` 통과 → 중복 검사 → 고객 생성 → 예약 순서다(T18).

**4. 제한 · 기록 §7**
- 키당 60/60s · 막힌 요청 안 셈 · 다른 연동처 따로 셈(T26).
- IP 카운트는 연동처 없는 오류 응답 **전부**에 건다(`api/ext.py:73-74` — 401 · 404 · 깨진 JSON 400 · 405, T31 섞어 10번). IP 차단 429 는 세지 않는다(`:60-63` 일찍 return).
- 연동처가 정해진 오류(필드 400 · 고객 404)는 세지 않는다(T31b).
- 1분 1줄은 `(IP, outcome)` 기준이다(T27b — 401 · 400 · 405 각 5번 → 3줄, 60초 뒤 다시 1줄).
- 기록 실패는 응답에 영향이 없다(`service/ext.py:91-95` · T27c).
- `no-store` 는 오류를 포함한 모든 응답에 붙고 `/api/health` 에는 없다(T28). 예외 = W6(500).

**5. 메뉴 동기화 §4.1**
- 8 작업은 `step()` 이 감싸 서로 독립이다. ③ 은 ② 가 성공할 때만 돈다(`menu_sync.py:90-98` · T2c).
- 실패한 작업은 tx 롤백(`db.py:345-350`)으로 표가 그대로 남는다(T4 — 5xx · `data` 가 배열 아님).
- 「없음」 표시는 각 작업 함수 안에서 성공한 뒤에만 한다. 복합 키 두 표는 별도 함수다(`repo.py` `mark_absent_compositions` · `mark_absent_target_countries`). 되살림 = upsert 의 `present: True` 다(T3).
- **N3**: `set_sync` 가 `INSERT OR REPLACE` 이지만 값으로 `ok_at or prev_ok` 를 넣는다(`repo.py:452-455`). 그래서 실패한 바퀴에 None 을 넘겨도 이전 `last_ok_at` 이 다시 쓰여 남는다. T6b(성공 → `get-machines` 503 → `syncedAt` 그대로 → 성공 → 새 시각) · T4(`ok == T0`)가 고정한다.
- 마스터 루프 순서: `resv.master()` 다음 `menu.run()` 이고, 예외는 따로 잡는다(`runtime.py:60-69`). 서버 시작과 조회 시간 밖에서도 돈다(T5). 기존 예약 동기화 호출 목록은 그대로다(`test_kos_sync`).
- ③ `OPTION_BATCH=100` 이고, 다 받은 뒤 한 번에 반영한다. 실패면 아무것도 바꾸지 않고, 응답에서 빠진 옵션은 이전 값을 둔다(T2).

**6. 직원 동작 불변**
- 직원 `search()` `countInPage: 20` 은 그대로다(`reservations.py:448`). `reservations.py` diff 는 `actor` 타입과 `_event` 한 줄뿐이다.
- 직원 OpenAPI 차이 0(위 수치).

**7. Swagger**
- tag 설명 = SPEC §8 문구. `ExtApiKey` = SPEC dict 그대로. 세 operation `security=[{ExtApiKey:[]}]` 이고 Bearer 는 0, 직원 operation 에 ExtApiKey 는 0이다(T29).
- 401 줄은 「직원 로그인이 아니라 `X-Api-Key`…」로 시작한다. 503 머리 = `STATUS_TEXT[503]` 「지금 쓸 수 없음」. D-35 문장 · `bundlePrice` 성질 셋 · `syncedAt` 뜻이 설명에 있다.
- 오류 표 ↔ 실제 raise 를 전수 대조했다. 메뉴 {401 · 405 · 429}, 조회 {400 · 401 · 404 · 405 · 409 · 429 · 502}, 예약 {400 · 401 · 405 · 409×3 · 429 · 502 · 503}. 빠진 code 와 나지 않는 code 는 0이다. 문구 흠은 W3 · W4, 앱 설명 누락은 W2.
- 「설명 빠진 곳 0」(`test_every_schema_property_has_description` · `test_every_operation_has_summary_description_and_tag`)이 새 스키마 14개와 `X-Api-Key` 헤더 파라미터까지 덮는다.

---

## 조용히 통과하는 자리

1. **이름 검색 응답 모양 오류**(W1) — 시험은 `visitors_page` 를 늘 `{count, data:[…]}` 꼴로만 준다. 「`data` 없음 · 배열 아님」 시험이 없어서, 예약이 새 KOS 고객을 만드는 경로가 초록 그대로 지나간다.
2. **중복 검사(D-35 409) 흉내** — `fake_kos` 의 `find-duplicated-visitor` 에 「저장된 email 과 **대소문자까지 같으면** 후보」를 새로 넣었다(`tests/fake_kos.py:326-327`). T19 의 409 는 이 흉내에만 기대고 있다. 실물 KOS 의 이메일 비교 방식(대소문자 · 공백)은 확인하지 않았다(be 리포트도 「흉내」라고 적음). 실물에서 대소문자가 다른 같은 이메일이 중복으로 잡히지 않으면 0명 갈래가 KOS 고객을 하나 더 만든다(D-22 수용 범위). → WP-E2E-LOCAL ④ 에서 대소문자가 다른 이메일로 한 번 확인하기를 권한다.
3. **동시성**(W5) — 모든 시험이 순차 TestClient 라서 카운터 경쟁을 보지 않는다.
4. **500 경로**(W6) — 처리하지 못한 예외 시험이 없다. `test_t27_write_failure_keeps_response` 는 `repo.tx` 를 깨는데, 그 405 경로는 원래 DB 를 쓰지 않아서 「기록 실패 = 응답 그대로」만 보고 `no-store` · 본문은 단언하지 않는다.
5. **예약 「다시 읽기」 실패**(W3 ②) — 문서는 502 라고 하지만 코드는 200 이다. 이 갈래를 보는 외부 시험이 없어 문서 ↔ 코드 차이가 드러나지 않는다.
6. `test_error_tables_match_dependencies` 는 `unauthorized` · `fake_board` 만 본다. `ext_unauthorized` ↔ `require_ext_key` 대응은 T29 가 세 operation 을 직접 열거해서 본다. 외부 operation 이 하나 더 생기면 T29 의 `OPS` 와 `ext_ops == OPS` 비교가 깨져서 알려 주므로 빈 집합 문제는 없다.

## 고객이 실물에서 만날 자리

- **W1**: KOS 내부 `get-visitors` 응답 꼴이 바뀌면 연동처는 「고객 없음(404)」만 보게 된다. 예약은 성공(200)하면서 KOS 에 같은 사람이 새 고객으로 쌓인다. 데스크가 늦게 알아챈다.
- **W3**: 연동처 개발자가 예약 502 표를 믿고 「다시 읽기 실패 = 502 = 다시 시도」로 구현해도, 실제로는 200 이 나가므로 문제는 없다. 하지만 이름 검색 단계 4xx 를 409 `kos_rejected` 로 기대하면 502 를 받는다.
- **W2**: Swagger 앱 설명만 읽은 연동처는 띄어쓰기 규칙을 모르고 404 를 「고객 없음」으로 오해할 수 있다(엔드포인트 설명에는 있음).

## 참고(기존 부채 · 이번 범위 밖)

- `client_ip()` 는 `CF-Connecting-IP` 를 믿는다(문진 웹 선례 · SPEC §7.3 지정). 운영은 Cloudflare Tunnel 이라 엣지가 덮어쓰지만, 로컬 · LAN 에서는 헤더로 IP 제한을 피할 수 있다. `RateLimiter._hits` · `ExtService._logged` 는 IP 키를 지우지 않아서, 키 수만큼 메모리가 늘어난다.
- 미들웨어 접두 비교가 `startswith("/api/ext")` 라서 `/api/extfoo` 같은 경로도 외부로 취급한다(지금 직원 경로 중 걸리는 것 0).
- uvicorn 접근 로그는 없는 경로(`/api/ext/customers/a@example.com`)의 경로 원문을 남긴다. `DropQueryString` 은 쿼리만 지운다. SPEC 이 「POST 본문으로 받는다」로 받아들인 범위다.
- `openapi_docs.DESCRIPTION` 「역할」 절에 같은 문장이 두 번 있다(be 리포트가 이미 적음).
