# 리뷰 리포트 — ext-api-charty1 / code r2 (2026-11-16)

**판정: WARN — FAIL 0 · WARN 3 · 질문 1** (r1 의 W1 ~ W5 · Q1 ~ Q3 · 참고는 코드에서 모두 반영됨 · 회귀 0 · 남은 것은 **시험 빈칸**: W5 를 고정하는 시험이 없고 board 고객 칸 값이 단언되지 않음)

- 대상: 같은 워크트리의 커밋 안 된 변경(지금 상태). 근거 = SPEC-008 **0.4.4** · DEC-012 **D-45** · `be-fix-r1-instructions.md` · 내 `review-code-r1.md`
- r1 뒤에 바뀐 앱 파일은 **둘뿐**이다(수정 시각이 r1 리포트보다 뒤): `app/service/ext.py`(525줄 diff · r1 때 524) · `app/repository/repo.py`(47줄 · r1 때 32). `api/ext.py` · `schemas/ext.py` · `service/reservations.py` · `domain/` · `db.py` · `openapi_docs.py` 는 r1 때 그대로다
- 돌린 시험(사용자 포트 · KOS 호출 없음): `test_ext_{board,lookup2,detail,write,clinic,auth,docs,history,lookup}.py` · `test_openapi_docs.py` · `test_order.py` · `test_resv_{detail,board,write}.py` → **289 passed**(r1 284 + 새 5)
- 변이 확인(파일은 고치지 않음 · 스크래치 스크립트가 시험 프로세스 안에서만 함수를 바꿔 끼움 — 아래 N1 · N2): 두 변이 모두 `test_ext_board.py` + `test_ext_auth.py` **41 passed**(못 잡음)

## r1 항목별 해결 표

| r1 | 지시(코디) | 판정 | 근거 파일:줄 |
|---|---|---|---|
| **W1 = Q1** ⓐ 가 귀가면 ⓒ 겸함 | 고침 | **해결** | `app/service/ext.py:758-760` — ⓐ 시도 예약에 `final_tried = int(main == "home")`(ⓑ 겸함과 같은 줄). SPEC §6.11 4 ⓐ(0.4.4) · D-45 ① 그대로. 시험 `tests/test_ext_board.py:380`(처음 봄 = 귀가 → board 4번 → 이력 1번 · `final_tried 1`) · `:390`(겹친 두 요청 → 이력 1번 · 그 뒤 board 도 0번) |
| W1 — 시도 예약 규칙 유지 | — | **PASS** | 고친 줄은 `with self.repo.immediate()` 블록 안 동기 코드(`:731-768`)이고 `await` · KOS 호출이 더해지지 않았다. KOS 부르기는 그대로 블록이 닫힌 뒤 `_history`(`:770-774`). ⓐ 가 상한 10에 밀린 귀가 줄은 행을 적지 않으므로 다음 요청에서 다시 ⓐ(1번)다 — 맞음. ⓐ 가 실패하면 `final_tried 1` · `last_failed 1` → ⓓ 가 받는다(D-41 그대로) |
| **W2 = Q2** HTTP 404 갈래 시험 | 코드 그대로 · 시험 더함 | **해결(+N3)** | 코드 `app/service/ext.py:352` 그대로. SPEC §6.4 · T48(0.4.4)이 404 · 400 + `id NotFound` 둘 다 계약으로 굳힘 · D-45 ②. 시험 `tests/test_ext_lookup2.py:91-93`(`resv_fail["get-visitor"] = (404, …)` → 이름 갈래 404 와 바이트 같음) · `:95-97`(400 + NotFound) |
| **W3** 섞인 사건 고르는 차례 | 시험 1개 | **해결** | `tests/test_ext_board.py:420` — ⓐ 4 · ⓑ 2 · ⓒ 2 · ⓓ 4 = 12줄. 첫 board 이력 호출을 **list** 로 단언(`a1 … a4, b1, b2, c1, c2, d2, d3` — ⓐ → ⓑ → ⓒ → ⓓ · ⓓ 는 `checked_at` 오래된 순 · 같은 사건 안은 줄 차례) · 남은 두 줄은 시도 행 안 씀(`retries 0`) · `partialErrors` · 두 번째 board = 남은 줄만 `["d4", "d1"]`(차례까지). 순위를 바꾸면 이제 실패한다 |
| **W4** 새 경로 caplog | 상세 · 오더 메모 각 1 | **해결** | `tests/test_ext_detail.py:211`(부분 실패 로그가 실제로 나는 상황 · 헤더 id · 예약 id · 고객 id · 이름 · KOS id 0) · `tests/test_ext_write.py:219`(성공 + KOS 거절 · 글 원문 포함 0). `_leaks`(`tests/test_ext_detail.py:204-208`)는 앞뒤가 단어 경계인 일치만 세어 숫자 id 가 시각 문자열에 섞여 오탐하지 않게 했다 · `caplog.records` 가 비지 않음도 단언 |
| **W5** board `event_log` · 고객 사본 거름 | 고침 · T55 그대로 통과 | **코드 해결 · 시험 빈칸(N1 · N2)** | 아래 「W5 새 쿼리」 절 |
| **Q3** 상세 `customerId` null | 코드 그대로 | **해결** | 코드 `app/service/ext.py:631` 그대로 · SPEC §6.12 표(0.4.4)에 `int \| null` · 직원 0 과 다름이 적힘 · D-45 ③ |
| **참고** 명시 `null` = 없음 | 그대로 · T49 단언 1 | **해결(+N3)** | 코드 `app/schemas/ext.py:58-63` 그대로 · SPEC T49(0.4.4) · D-45 ⑤. 시험 `tests/test_ext_lookup2.py:133`(`{name, email, customerId: null}` → 200) |

## W5 새 쿼리 — 브리프 §볼 것 2

| 볼 것 | 판정 | 근거 |
|---|---|---|
| `json_extract` 거르기가 지금 payload 모양과 맞나 | **PASS** | `app/repository/repo.py:202-208` — `json_extract(payload, '$.reservationId') IN (?…)`. 두 type 을 쓰는 곳은 `app/service/reception.py:205`(`reception`) · `:263`(`consultation_add`) 둘뿐이고 둘 다 `{"reservationId": r.id}` **정수**로 적는다 → `json_extract` 가 INTEGER 를 주고 정수 바인딩과 맞는다. 옛 코드(Python 쪽 `events.get(r.id)`)도 정수 키로만 맞췄으므로 뜻이 같다. 실제로 맞는다는 증거: T55(`tests/test_ext_board.py:104`)의 `s-recv`(접수 이벤트로만 `true`) · `s-add`(`consultation_add` 로만 `true`)가 통과 — 거르기가 아무것도 못 고르면 실패한다 |
| 예약 id 가 빈 집합일 때 | **PASS** | `:204-205` 빈 `types` · 빈 id → `[]`(`IN ()` SQL 오류 없음). `customers_in` 도 같음 `:633-634`. board 의 그날 예약 0건 = `tests/test_ext_board.py:371`(경로 차례 시험 · 빈 날) 통과 |
| 매개변수 바인딩(문자열 조립 아님) | **PASS** | f-string 으로 만드는 것은 `?` 자리표시 개수뿐이고 값은 모두 `execute(sql, [*types, *ids])` 로 묶는다(`:206-208` · `:635-636`). 바인딩 수 상한: 이 환경 SQLite 3.49(상한 32766) — 하루 예약 수로는 닿지 않는다 |
| 직원 쪽 `events()` · `customers()` 무변경 | **PASS** | `git diff app/repository/repo.py` 의 `-` 줄 0 — `events()`(`:192-196`) · `customers()`(`:627-629`)는 손대지 않았고 새 함수 둘만 더했다 |
| 결과가 옛 코드와 같나 | **PASS** | 고객: `customers_in(그날 줄의 customer_id)`(`app/service/ext.py:685`)는 옛 `customers()` 에서 그날 줄이 꺼내 쓰던 키와 같은 집합. 이벤트: 그날 예약 id 로만 꺼내 쓰던 것과 같은 집합 · 같은 `ORDER BY id` |

## 회귀 — r1 PASS 자리

r1 뒤 바뀐 줄은 `app/service/ext.py:685` · `:688`(board 읽기 두 줄) · `:759-760`(ⓐ 한 줄) · `app/repository/repo.py` 새 함수 둘뿐이다. r1 표 24항목 중 이 줄에 닿는 것은 #13(상담 판정) · #14 ~ #17(이력 · 시도 예약 · 상한 · `partialErrors`)이고 위에서 다시 확인했다(**PASS**). 나머지 항목(경로 · lookup · 헤더 · `ext_view` · `ext_call` · 쓰기 · 상세 · 병원 · 직원 · 직원 API · 기존 여섯 · Swagger)은 해당 파일이 r1 때 그대로이고 시험이 그대로 통과한다(**PASS · 변화 없음**). 실명 · 키 grep: 새 시험 줄은 `<이름77>` · `staff-w4-x` 같은 자리표시뿐(**PASS**).

## 새 지적

### N1 (WARN). W5 를 고정하는 시험이 없음 — 옛 전체 읽기로 되돌려도 초록

- SPEC T55(0.4.4)에 더해진 줄: 「다른 날 예약의 `reception` · `consultation_add` 줄이 많아도 board 결과 같음 · board 가 읽는 `event_log` 는 그날 예약 id 것만(쿼리에 예약 id 조건)」. 이 줄을 단언하는 시험이 **없다**(`tests/test_ext_board.py` 에 다른 날 이벤트 · 쿼리 조건 단언 0 · `test_t55` 는 r1 그대로)
- 변이 확인: `Tx.events_for_reservations` 를 「그 type 전체 읽기」로 바꿔 끼우면 `test_ext_board.py` + `test_ext_auth.py` **41 passed** — W5 를 누가 되돌려도 아무 시험도 깨지지 않는다(조용히 통과하는 자리)
- 권장: T55 에 ① 다른 날 예약 id 의 `reception` · `consultation_add` 줄 여럿을 넣고 board 결과가 같음 ② `tx.events_for_reservations` 결과(또는 repo 함수 직접 호출)에 그날 예약 id 밖의 줄이 없음 — 단언 2줄

### N2 (WARN). board 고객 칸 **값**을 어떤 시험도 단언하지 않음 — `customers_in` 이 비어도 초록

- `tests/test_ext_board.py:100` 은 고객 칸 **키 집합**만 본다. `customerId` · `name` 값을 보는 board 시험이 없다
- 변이 확인: `Tx.customers_in` 을 늘 `{}` 로 바꿔 끼우면(모든 줄 `customerId: null` · `name: ""`) 같은 41 passed. r1 때부터 있던 빈칸인데(r1 리포트에서 놓침), 이번 W5 가 바로 그 읽기를 바꿨으므로 이제 위험이 실제다
- 권장: T54 에 한 줄 — 그 줄의 `customer.customerId` 가 사본 고객 id(int) · `name` 이 사본 이름

### N3 (WARN · 낮음). SPEC 0.4.4 가 T48 · T49 에 더한 줄 일부가 시험에 없음

- T48 「(0.4.4) 그 밖 400 → 502」 — `get-visitor` 가 NotFound 가 아닌 400 일 때 502 를 보는 시험이 없다(`tests/test_ext_lookup2.py:101-112` 는 5xx · 모양 오류만). 코드 `app/service/ext.py:352-358` 은 맞게 502 다. 404 갈래를 넓힌 판이라 「400 이면 모두 404」로 잘못 넓어지는 것을 막는 단언이 필요하다
- T49 「명시 null」 세 경우 중 하나만 있다(`:133` = `{name, email, customerId: null}` → 200). `{customerId: 1, name: null, email: null}` → 200 · `{customerId: null}` → 400 은 없다. backend 지시는 「1개」였고 SPEC 은 셋이라 지시 · SPEC 이 어긋난 자리다(Q-r2)
- 권장: 각 1줄(400 `{"className": "x.InvalidRequestException"}` → 502 · null 두 경우)

## 고객이 실물에서 만날 자리 (r1 에서 바뀐 것만)

- r1 의 2번(하루 끝 귀가 일정 2번 호출)은 W1 로 **닫힘**
- 나머지(상담 메모 쓰기가 다른 상담 칸을 비우는지 · 실물 `get-visitor` 「없음」 꼴 · 언어 덮어쓰기)는 그대로 WORK-014 E2E-LOCAL 몫

## 질문 (코디 몫 — 결정하지 않음)

- **Q-r2**: N1 ~ N3 은 모두 시험만 더하는 일이다(코드 변경 0). 이번에 backend 3차로 더할지, 아니면 기록만 하고 E2E 로 갈지?

## 참고 (판정 밖)

- SPEC §6.11 3(0.4.4)의 「`reservation_id IN (그날 사본 예약 id)`」는 `event_log` 에 그 이름의 열이 없어 글자로는 코드와 다르다(코드는 `payload.reservationId` 로 거름 · 뜻은 같음). SPEC 낱말을 `payload.reservationId` 로 고치면 읽는 사람이 헷갈리지 않는다
- 거른 쿼리도 `event_log` 에 `type` · payload 인덱스가 없어 표를 훑는다. Python 으로 전부 가져와 JSON 을 푸는 것보다는 훨씬 가볍다(SQL 안에서 거름). 인덱스는 이번 범위 밖
