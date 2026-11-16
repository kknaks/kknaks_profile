# 리뷰 리포트 — ext-api-charty1 / code r1 (2026-11-16)

**판정: WARN — FAIL 0 · WARN 5 · 질문 3** (SPEC-008 0.4.3 ↔ 코드 계약 위반 없음 · 기능 독립 지킴 · 고칠 것 권장 1(W1) · 나머지는 시험 보강 · SPEC 한 줄)

- 대상: 워크트리 `ext-api-charty1` 브랜치 `kknaksss/ext-api-charty1` 의 **커밋 안 된 변경**(base `origin/main` `0a58aba`). 변경 = `procedure/back/**` 만(app 8 · tests 기존 7 고침 + 새 5). 파일은 고치지 않았다
- 근거 문서: SPEC-008 0.4.3 · DEC-012 D-01 ~ D-44 · WORK-014 「계약 고정점」 · WP-REVIEW 행 · 「주의」 · `kos0-report.md`
- 돌린 시험(사용자 포트 · KOS 호출 없음): `uv run pytest -q` 로 `test_ext_{lookup,lookup2,auth,history,detail,write,board,clinic,docs}.py` · `test_openapi_docs.py` · `test_order.py` · `test_resv_{detail,board,write}.py` → **284 passed**. 전체 746 passed 는 코디 몫(이미 돌림)
- 줄 번호 = 워크트리 지금 파일 기준(`procedure/back/` 아래)

## WP-REVIEW 항목별 표

| # | 항목 | 판정 | 근거 파일:줄 |
|---|---|---|---|
| 1 | 기능 독립(기능 폴더 밖 변경 · 레포 루트 공용 코드 0) | PASS | `git status` — 변경 15 + 새 5 모두 `procedure/back/` 안. `main.py` · `kos/` · 다른 기능 폴더 변경 0 |
| 2 | 경로 일곱 · 메서드 · 경로 칸 이름 · board 를 상세보다 먼저 등록(§6.11 ~ §6.17 머리) | PASS | `app/api/ext.py:415`(board) → `:423`(상세) · `:474` · `:482` · `:490` · `:524` · `:530` · 시험 `tests/test_order.py:272-280` · `tests/test_ext_board.py:371` |
| 3 | lookup — 두 갈래 · 갈래 오류 `body: …` · `ExtCustomerRequest` 상속 끊음(§6.4 · T49 · T71 ⓐ ⓑ ⓒ) | PASS | `app/schemas/ext.py:24`(`_NameEmail` = 옛 두 칸 · 검증 그대로) · `:42-63`(새 모델 · `StrictInt ge=1` · `_branch`) · `:212`(`ExtCustomerRequest(_NameEmail)`) · 시험 `tests/test_ext_lookup2.py:116` · `:126` · `tests/test_ext_history.py:295` |
| 4 | lookup — `customerId` 갈래(사본 → 내부 `get-visitor` 1 → `upsert_customer` · 없으면 같은 404 바이트 · KOS 0) | PASS(+W2) | `app/service/ext.py:343-363` · 시험 `tests/test_ext_lookup2.py:71` · `:97` |
| 5 | lookup — 내부 시술권 · 거르기 · `inUseCount` · 선불카드 동시 · 실패 = 200 + null + `partialErrors`(§4.3 · §4.4 · D-08 · D-36) | PASS | `app/service/ext.py:68-71`(경로 · `sort`) · `:312-338`(`gather` · 시술권 실패 502 · 선불카드만 부분 실패) · `:374-381`(`inUseCount` · `_live`) · 시험 `tests/test_ext_lookup2.py:135` · `:155` · `:180` · `:196` |
| 6 | 열람 헤더 — 다섯 경로에만 · 꼴 함수 하나 · lookup 너그러움 · 새 넷 400(`header.X-Ext-Staff-Id:`)(§6.10 · D-37) | PASS | `app/api/ext.py:76-96`(`staff_id_of` 하나 · `lenient_staff` · `strict_staff`) · `:256`(lookup = Lenient) · 상세 · 쓰기 셋 = Strict · board · clinic · staff · 기존 다섯은 의존성 없음 · 시험 `tests/test_ext_lookup2.py:233` · `:256`(T71 기존 다섯 같은 응답) · `tests/test_ext_detail.py:179` · `tests/test_ext_write.py:190` · `tests/test_ext_docs.py:71-77`(parameters 허용 목록) |
| 7 | `ext_view` — 200 일 때만 · `payload` · `actor = ext:<연동처>[:<직원 id>]`(§3.5) | PASS | `app/service/ext.py:293-299` · `app/api/ext.py:258` · `:434`(응답 검증 뒤에만 부름 → 오류 응답엔 없음) · 시험 `tests/test_ext_lookup2.py:206`(404 · 409 · 502 → 0줄) · `tests/test_ext_detail.py:159` |
| 8 | `ext_call` 에 직원 id · 고객 · 예약 id 0 · 앱 로그에 헤더 값 0(D-18 · D-24) | PASS(+W4) | `ext_call` 미들웨어(`app/main.py`) 변경 0 · 새 코드의 `log.*` 는 `kos_errors.describe(e)`(상태 · 이름만 · `app/service/kos_errors.py:40-42`)만 싣는다 · 시험 `tests/test_ext_auth.py:306`(경로 틀만) · `tests/test_ext_lookup2.py:242`(caplog) |
| 9 | 쓰기 = KOS 먼저 · 실패 때 성공 줄 0 · 사본 변경 0 · `kos_rejected` 1줄(D-04) | PASS | `app/service/ext.py:657-667`(`kos_write` → 성공 뒤 `_event` · visit 미러 · `after_write`) · 언어 = 직원 `personal()` 그대로 `:648-655` · 시험 `tests/test_ext_write.py:165`(셋 다) |
| 10 | 오더 메모 사본 = visit 행이 있을 때만 UPDATE · upsert 금지(§6.14 4 · W9) | PASS | `app/repository/repo.py:220-222` · 시험 `tests/test_ext_write.py:94`(visit 행 수 그대로 · 다른 칸 그대로) |
| 11 | 새 `event_log` type `order_memo` · `consultation_memo` = `{reservationId, length}` · 글 원문 0 | PASS | `app/service/ext.py:663` · 시험 `tests/test_ext_write.py:94` · `:136` |
| 12 | 경로별 KOS 호출 수(§6.9) | PASS | lookup 3 · 3 · 1 · 0 = `tests/test_ext_lookup2.py:206` · 상세 5(수납 0 · 날짜 조회 0) = `tests/test_ext_detail.py:72` · `:159` · 언어 2 · 1 · 0 = `tests/test_ext_write.py:52` · `:76` · 메모 1 · 0 = `:94` · `:150` · 병원 3 = `tests/test_ext_clinic.py:41` · 직원 1 · 0 = `:106` · `:128` · board 0(사건 없음) · ≤ 10 = `tests/test_ext_board.py:360` · `:283` |
| 13 | 상담 거침 판정 = 함수 하나 · `after` 문 먼저 · 직원 `_flow` 도 그 함수(§6.11 3) | PASS | `app/domain/reservation_rules.py:40-55` · `app/service/reservations.py:661`(옛 조건 그대로 옮김 · `_flow` 는 `after` 일 때만 불림 `:532`) · `app/service/ext.py:719` · 시험 `tests/test_ext_board.py:104`(직원 상세와 같은 판정 · 취소 · 부도 포함) |
| 14 | 이력 — 대상 = `after` 줄 · 찾은 값만 굳힘 · 사건 때만(ⓐ ~ ⓓ) · 실패 재시도 5분 · ≤ 3 · `eventType` 끝 조각 · 문자열 `flowStep` · 원소 시각 최솟값(§6.11 4 · D-38 · D-40 ~ D-42) | PASS(+W1 · W3) | `app/service/ext.py:697-700` · `:725-768` · `:785-807` · `app/repository/repo.py:210-218`(`first_at IS NULL` 인 행만 고침) · 시험 `tests/test_ext_board.py:146` ~ `:347` |
| 15 | 시도 예약 — `BEGIN IMMEDIATE` · 안에 `await` 0 · KOS 전 커밋 · 요청 트랜잭션과 따로 · 예외 때 잠금 안 남음 | PASS | 아래 「시도 예약」 절 · `app/repository/repo.py:877-886` · `app/service/ext.py:731-768` · 시험 `tests/test_ext_board.py:313` |
| 16 | 요청당 상한 10 · 자주 불러도 · 실패가 이어져도 호출이 늘지 않음 | PASS(+W3) | `app/service/ext.py:756` · 시험 `tests/test_ext_board.py:283` · `:296` · `:242` · `:347` |
| 17 | `partialErrors` `consultationHistory`(D-39 넓힘 포함) | PASS | `app/service/ext.py:703-704` · 시험 `tests/test_ext_board.py:242` · `:296` · `:313` |
| 18 | 예약 상세 — `_detail_reads(…, amount=False)` · 이전 방문 실패 알림 값 · 지금 메모 둘 · 부분 실패 · `reservation_gone`(§6.12) | PASS | `app/service/ext.py:581-646` · `app/service/reservations.py:582-623` · 시험 `tests/test_ext_detail.py:72` ~ `:196` |
| 19 | 병원 — 칸 = 이름 · 주소 · 전화 · 운영 시간 · 휴무 · `clinicId` 만 · 빈 문자열 null · 휴무 `{startDate, endDate}` · 하나라도 실패 502(§6.16 · D-25 ~ D-28 · D-43) | PASS | `app/service/ext.py:820-863` · 시험 `tests/test_ext_clinic.py:41` ~ `:93`(본문 기간 `…T15:00:00.000Z` 까지 단언) |
| 20 | 직원 — `clinicId` 상수 비교 404 · 시스템 · 제외 목록 뺌 · 사본과 KOS id 로 결합(§6.17 · D-29) | PASS | `app/service/ext.py:865-890` · 시험 `tests/test_ext_clinic.py:106` · `:128` |
| 21 | **직원 API 무변경**(`_flow` · `_detail_reads` · `personal` 셋만 · 응답 · `event_log` 그대로) | PASS | `app/service/reservations.py:582`(키워드 인자 기본 `True` · 직원 부르는 곳 고침 0) · `:623`(새 키 `previous_err` — 직원 응답 조립은 읽지 않음) · `:661` · `:1061`(타입만) · 시험 `tests/test_ext_detail.py:159`(직원 상세 수납 금액 그대로) · `:196` · `tests/test_resv_*` 통과 |
| 22 | **기존 여섯 계약 무변경**(lookup 은 칸 추가만) · 과거 시술 · 예약 내역 본문 모델 무변경 | PASS | `app/schemas/ext.py:24` · `:212` · `app/api/ext.py` 기존 다섯 라우트 서명 그대로 · 시험 `tests/test_ext_history.py:295` · `tests/test_ext_lookup2.py:256` |
| 23 | Swagger — 열셋 · 공통 응답 줄 · 헤더 설명 · 옛 문장 지움 · 개수 `n_ops - 5 - 13`(§8 · T70) | PASS | `app/openapi_docs.py:77-88` · `app/api/ext.py` 각 `*_DOC` · 시험 `tests/test_ext_docs.py:109` · `tests/test_openapi_docs.py:98` |
| 24 | 실명 · 키 · KOS id · 이메일 · 전화 grep | PASS | diff 전체 + 새 시험 다섯에 `@example.com` 밖 이메일 · 전화 꼴 · uuid · 키 꼴 0. 시험 이름 = `<상담사>` · `<병원>` 같은 자리표시 · 기존 가짜 이름(「가 원장」) |

## 시도 예약(브리프 §6 3) — PASS

- **`await` 없음**: `_reserve_history`(`app/service/ext.py:725-768`)는 동기 함수이고 `with self.repo.immediate() as tx:` 블록 안에 KOS 호출 · `await` 가 없다. 블록은 `return` 전에 닫힌다 → `connect()` 가 `commit()`(`app/repository/db.py:350-361`)
- **KOS 전 커밋**: `_history`(`:770-783`)는 `_reserve_history` 가 돌아온 **뒤**에 `asyncio.gather(_first_wait…)` 를 부른다. 시험 `tests/test_ext_board.py:313` 이 KOS 호출 순간 행이 이미 `last_failed = 1` · `wait_called = 1` 로 적혀 있음을 단언한다
- **요청 트랜잭션과 따로**: `immediate()`(`app/repository/repo.py:877-886`)는 새 연결(`db.connect()`)을 연다. `board()` 의 앞 `with self.repo.tx()` 블록은 그 전에 닫혀 있고(`:684-692`), 요청 전체를 감싸는 연결은 없다
- **예외 때**: `connect()` 의 `except → rollback → close`. 결과 적기 전에 죽으면 `last_failed = 1` 이 남아 ⓓ 가 받는다(SPEC 그대로). `BEGIN IMMEDIATE` 는 Python sqlite3 legacy 모드에서 명시 BEGIN 뒤 DML 에 암묵 BEGIN 을 더하지 않는다 — 시험이 실제로 통과
- 한계(참고): 겹친 요청 시험은 한 이벤트 루프 안 두 코루틴이다. 두 프로세스 잠금 경합은 시험하지 않았다(코드상 같은 경로 · `timeout=10`)

## FAIL

없음.

## WARN

### W1. 처음 봄(ⓐ) 때 이미 귀가면 `final_tried` 를 세우지 않음 → 다음 board 에서 ⓒ 1번 더 · 겹친 요청이 같은 일정을 동시에 부름 (backend 미결 ②)

- 자리: `app/service/ext.py:739-740`(`row is None → rank 0`) · `:758-760`(ⓐ 는 `wait_called` 만 겸함) · `:747`(ⓒ = `main == "home" and not final_tried` — `last_failed` 를 보지 않음)
- SPEC: §6.11 4 ⓐ 는 「그때 대기면 ⓑ 몫도 겸한다」만 적고, ⓒ 를 겸하는지는 **적지 않았다**. 글자대로면 지금 코드가 맞다(하루 상한 「처음 봄 1 + 귀가 뒤 1」 안). 그래서 FAIL 아님
- 문제 둘:
  1. **비용**: ⓐ 의 1번은 이미 귀가를 본 **뒤**의 호출이라 ⓒ(「끝난 단계를 본 뒤 1번」 · D-40)를 이미 채운다. 그런데 다음 board 에서 같은 일정을 또 부른다. 연동처가 하루 끝에 board 를 처음 열면 귀가 일정 **전부**가 2번씩(요청당 10 상한 때문에 여러 요청에 걸쳐 null + `partialErrors`)
  2. **겹친 요청**: ⓐ 가 부르는 중(`last_failed = 1`)인 귀가 일정을 둘째 요청이 ⓒ(`final_tried = 0`)로 골라 **동시에 같은 일정을 한 번 더** 부른다. 「겹친 요청도 같은 일정 1번」(§6.11 4 시도 예약 · D-38 ④ · 검수 r2 N2)의 뜻과 어긋난다(사건 이름이 달라 글자로는 걸리지 않음)
- 시험: `tests/test_ext_board.py:229` 는 「ⓐ 뒤에 귀가」만 본다. 「처음 봄 때 이미 귀가」 줄이 없다
- 권장(코디 판단 · Q1): ⓐ 시도 예약에 `final_tried = int(main == "home")` 한 줄(ⓐ 가 ⓑ 를 겸하는 것과 같은 꼴) + SPEC §6.11 4 ⓐ 에 「귀가면 ⓒ 몫도 겸한다」 + 시험 1개(처음 봄 = 귀가 → board 여러 번 → 이력 1번)

### W2. `customerId` 갈래 — KOS 「없음」 판정이 SPEC 보다 넓고, SPEC 의 404 갈래는 시험이 없음 (backend 미결 ①)

- 자리: `app/service/ext.py:352` — `status == 404` **또는** `400 + errorProperties {key: id, reason: NotFound}` → `customer_not_found`
- SPEC §6.4 · T48: 「KOS 가 그 고객을 404 로 주면 404 · 그 밖 실패 = 502」. 400 + NotFound 갈래는 SPEC 에 없다(SPEC ↔ 코드 다름 · 작은 쪽)
- 판정 = **코드는 맞다**(KOS 가 「없는 고객」을 400 + NotFound 로 주는 선례가 레포에 있다 — `app/service/reservations.py:614` 문진 `visitorId NotFound` · 가짜 KOS `tests/fake_kos.py:284-287` 도 그 꼴). 502 로 두면 지워진 고객이 「KOS 장애」로 보인다
- 조용히 통과하는 자리: 가짜 KOS 의 `get-visitor` 없음 = 늘 400 + NotFound 라서, **SPEC 이 적은 404 갈래(`e.status == 404`)는 어떤 시험도 지나가지 않는다**(`tests/test_ext_lookup2.py:91-94`). 실물 KOS 가 어느 꼴을 주는지도 KOS0 에서 보지 않았다
- 권장: SPEC §6.4 · T48 에 「400 + `errorProperties` `id NotFound` 도 같은 404」 한 줄(Q2) + 시험에 `resv_fail["get-visitor"] = (404, …)` 갈래 1줄. 실물 꼴은 E2E-LOCAL ① 에서 지워진 · 없는 KOS id 로 1번 보면 닫힌다(쓰기 아님)

### W3. 요청당 상한의 「고르는 차례」(ⓐ → ⓑ → ⓒ → ⓓ → 줄 차례)를 섞인 사건으로 시험하지 않음

- 자리: 코드 `app/service/ext.py:749-756`(정렬 키 `(rank, checked_at 또는 now, 줄 index)`) — 읽어 보면 SPEC §6.11 4 그대로다
- 시험: `tests/test_ext_board.py:283` · `:296` 은 15줄이 **모두 같은 사건**(ⓐ 만 · ⓑ 만)이다. 순위를 뒤집어도(예 ⓓ 를 먼저) 두 시험은 초록이다. 같은 사건 안의 줄 차례(시작 → id)도 `set` 으로만 견줘 차례가 틀려도 통과한다
- 권장: ⓐ · ⓑ · ⓒ · ⓓ 가 섞인 12줄 이상으로 첫 board 의 10개 집합 · 남은 줄을 단언하는 시험 1개

### W4. T69 「앱 로그에 직원 id · 고객 · 예약 id 0」을 새 경로에서는 시험하지 않음

- 시험: caplog 단언은 lookup 만(`tests/test_ext_lookup2.py:242`). 상세 · 쓰기 셋 · board 는 `ext_call` 표만 본다(`tests/test_ext_detail.py:176` · `tests/test_ext_auth.py:306`)
- 코드는 지금 안전하다 — 새 `log.warning` 은 모두 `kos_errors.describe(e)`(상태 · 이름만)를 싣는다(`app/service/ext.py:320` · `:337` · `:354-358` · `:778` · `:862` · `:876`). 나중에 누가 로그에 값을 더하면 막는 시험이 없다
- 권장: 상세 · 오더 메모(헤더 `st-…` 와 예약 id) 1번씩 caplog 단언 한 줄(T69 「새 경로 · lookup」 문구 그대로)

### W5. board 가 요청마다 `event_log` 의 `reception` · `consultation_add` 전체와 고객 사본 전체를 읽음(부하)

- 자리: `app/service/ext.py:684-690`(`tx.events("reception") + tx.events("consultation_add")` · `tx.customers()`) — 그날 예약으로 거르지 않는다
- 계약 위반은 아니다(직원 상세도 `tx.events()` 전체를 읽는 선례 — `app/service/reservations.py:509`). 다만 board 는 외부가 키당 60초 60번까지 부를 수 있는 목록이고, 두 type 은 접수마다 쌓여 줄지 않는다(§3.6 「지우지 않고 쌓는다」 · `event_log` 보존 기간 없음). 데모 · 첫 운영엔 문제 없고 몇 달 뒤 board 응답이 느려진다
- 권장(이번 범위 밖이면 기록만): 그날 예약 id 집합으로 거르는 쿼리. 지금 고칠지는 코디 몫

## 고객이 실물에서 만날 자리

1. **상담 메모 쓰기가 다른 상담 칸을 비우는지** — 공개 `update-schedule-consultation-info` 는 스펙으로만 봤다. 가짜 KOS(`tests/fake_kos.py:574-585`)는 `consultationMemo` 만 바꾸므로 시험은 이 위험을 못 본다. WORK-014 E2E-LOCAL ④(상담사 · 의사 · 결과 그대로인지 · 상담 전 일정에 쓰면 무엇이 오는지) 몫(backend 미결 ⑥ — **맞음**)
2. **하루 끝에 board 를 처음 열면** 귀가 일정마다 이력 2번 · 상한 10 때문에 몇 번의 요청 동안 `firstConsultationWaitingAt` null + `partialErrors: ["consultationHistory"]`(W1)
3. **지워진 · 없는 KOS 고객의 `customerId` 조회** — 실물 KOS 의 `get-visitor` 응답 꼴이 404 도 400 + NotFound 도 아니면 `502` 로 보인다(W2)
4. **고객 언어 덮어쓰기**(D-11 수용) — 다시 읽기와 쓰기 사이 KOS 웹 변경이 덮인다. Swagger 에 적혀 있다(`app/api/ext.py` `LANG_DOC`)
5. 예약 상세 `customer.customerId` 는 고객 사본이 없는 예약이면 **null** 이다(직원 상세는 `0`) — 연동처가 0 을 기대하지 않게 Swagger 칸 설명에 적혀 있다(`app/schemas/ext.py` `ExtDetailCustomer.customerId`)

## backend 미결 6개 판정

| # | 미결 | 판정 | 근거 |
|---|---|---|---|
| ① | `customerId` 갈래 KOS 고객 없음 = 404 또는 400 + NotFound 둘 다 `customer_not_found` | **맞음**(SPEC 한 줄 · 404 갈래 시험 더함 — W2 · Q2) | `app/service/ext.py:352` · 선례 `app/service/reservations.py:614` · SPEC §6.4 「404 → 같은 404」의 뜻(「KOS 에 그 고객 없음」)과 같다 |
| ② | 처음 봄(ⓐ) 때 이미 귀가면 `final_tried` 안 세움 → 다음 board 에서 ⓒ 1번 더 | **고칠 것(권장)** — 글자로는 SPEC 위반 아님 · 비용 두 배 · 겹친 요청 중복 호출(W1 · Q1) | §6.11 4 ⓐ · ⓒ · 시도 예약 · DEC-012 D-38 ④ · D-40 |
| ③ | `clinic_not_found` message 「없는 병원이에요」 | **맞음** | 같은 꼴의 선례: `RESV_NOT_FOUND` 「없는 예약이에요」(SPEC §6.12 1 이 정한 문구 · `app/service/ext.py:73`) · 직원 `NotFound("없는 고객이에요")`(`app/service/reservations.py:1065`). SPEC 은 문구를 구현에 맡기고 연동처는 `code` 로 가른다(§6.4 「문구 칸은 예」 · §6.1 오류) |
| ④ | 상세 `customer.customerId` 사본 없으면 null · 선불카드 객체 안쪽만 null | **맞음** | `customerId` null = board `customer.customerId(int \| null)`(§6.11 표)와 같은 꼴 · 직원 상세의 `0` 은 없는 id 라 외부에 내기 나쁘다(lookup 은 `customerId ≥ 1` 만 받음). SPEC §6.12 표 「직원 상세와 같은 값」과 글자로 다르므로 SPEC 한 줄(Q3). 선불카드 안쪽 null = §4.4 「값이 없으면 그 칸 null」 그대로(`app/service/ext.py:121-145`) |
| ⑤ | KOS0 인증 호출 | **무관(코드 밖) · 문제 없음** | `kos0-report.md` — 인증 명령(`exchange-token` · `sign-in`)만 · 데이터 쓰기(`/commands/`) 0. WORK-014 KOS0 「조회만 · 쓰기 0」 은 데이터 쓰기 뜻이고 지금 `KosClient` 토큰 받기와 같다 |
| ⑥ | 실물 쓰기는 E2E 몫 | **맞음** | WORK-014 「주의」 첫 줄 · WP-E2E-LOCAL ④ · SPEC §6.15 「실물 확인 ④」 |

## 시험이 계약을 고정하나 — 기존 시험에서 지우거나 약하게 바꾼 단언(`git diff tests/` 전수)

지운 `-` 줄 17개를 다 봤다. **계약을 약하게 한 것 0** — 모두 SPEC §8 「시험 고침(0.4.0)」 · T71 이 허락한 넓힘이다.

| 파일:줄 | 바뀐 것 | 판정 |
|---|---|---|
| `tests/test_ext_lookup.py:131-132` | 시술권 본문 `{visitorId}` → `+ sort` | 허락(T71 「공개 → 내부」) |
| `tests/test_ext_lookup.py:158-160` | 시술권 줄에 `inUseCount` 더함 | 허락 |
| `tests/test_ext_lookup.py:172-173` | 응답 키 집합에 `prepaidCards` · `partialErrors` 더함 · 고객 키 집합 단언은 줄을 나눠 **그대로** | 허락(T71 · N6) |
| `tests/test_openapi_docs.py:98` · `tests/test_order.py:272-291` | 개수 6 → 13 · 77 → 84 · 경로 집합 더함 | 허락(§8) |
| `tests/test_ext_docs.py:71-77` | parameters 단언 — `!= "header"` 를 `== "query"` 로 바꾸고 허용 집합 넓힘 · 헤더는 다섯 operation 정확히 · path 는 정수만 | 넓힘. `name` · `email` 이 질의 · 경로에 생기면 집합 등식에서 여전히 실패 — 약해지지 않음 |
| `tests/test_ext_docs.py:105-106` | 「경로 여섯」 → 「경로 열셋」 · `"셋" not in` 단언에서 「열셋」 · 「쓰기 셋」을 뺌 | 넓힘(§8 「셋」 문구 규칙은 「세 경로」 꼴을 막는 것). 참고: 「쓰기 셋」 예외는 「세 경로」류를 다시 막지 못하는 틈이 아니다 |

가짜 KOS ↔ KOS0 실물 모양:

| 가짜 응답 | KOS0 | 판정 |
|---|---|---|
| 이력 원소(`tests/test_ext_board.py:24-34`) | 6키 · 전체 이름 `eventType` · `payload` JSON 문자열(나노초) · `flowStep` 문자열 · 차례 섞임 · 소수 2 · 3자리 · 다른 이벤트 섞임 | 같음 |
| 휴무(`tests/test_ext_clinic.py:30-32`) | `{id, startDateTime, endDateTime}` · 초 `Z` · 끝 배타 | 같음 |
| 선불카드(`tests/test_ext_lookup2.py:58-66`) | 금액 객체 · 만료 `YYYY-MM-DDTHH:MMZ`(초 없음) · `ownerId` · `description` · `translsMap` | 같음 |
| 내부 시술권(`tests/test_ext_lookup2.py:52-55`) | `price.value` float · 다 쓴 · 취소 묶음 섞임 | 같음 |
| `get-visitor` 없음(`tests/fake_kos.py:284-287`) | KOS0 에서 보지 않음 | **모름**(W2) |
| 상담 메모 쓰기(`tests/fake_kos.py:574-585`) | 실물 없음(스펙만) | E2E 몫(실물 자리 1) |

## 질문 (코디 · 사용자 몫 — 결정하지 않음)

- **Q1**(W1 · 미결 ②): ⓐ(처음 봄)가 이미 귀가인 일정이면 ⓒ 몫도 겸하게(`final_tried = 1`) 고칠까? 고치면 SPEC §6.11 4 ⓐ 에 한 줄 · 시험 1개. 안 고치면 「귀가 일정은 처음 봄 + 귀가 뒤 = 2번」을 SPEC 에 적어 두는 것을 권한다
- **Q2**(W2 · 미결 ①): SPEC §6.4 · T48 의 「KOS 가 404」에 「400 + `errorProperties` `id NotFound`」를 더해 지금 코드를 계약으로 굳힐까? 실물 꼴은 E2E-LOCAL ① 에서 1번 확인
- **Q3**(미결 ④): SPEC §6.12 표에 「`customer.customerId` = 고객 사본이 없으면 null(직원 상세의 0 과 다름)」 한 줄을 넣을까?

## 참고 (판정 밖)

- `ExtLookupRequest` 는 명시 `null` 을 「없음」으로 본다 — `{"customerId": 1, "name": null}` 은 `customerId` 갈래로 `200`(`app/schemas/ext.py:58-63`). SPEC 「섞이면 400」의 「섞임」을 값이 있는 칸으로 읽으면 맞다. 바꿀 필요는 없어 보이나 T49 에 이 줄이 없다
- `app/repository/repo.py:133-138` 에 이미 `BEGIN IMMEDIATE` 를 쓰는 기존 함수가 있다(무관 · 이번 변경 아님). 새 `immediate()` 와 이름 · 쓰임이 겹치니 나중에 하나로 묶을 수 있다
- 기존 부채(무관): 직원 상세가 요청마다 `event_log` 전체를 읽는다(`app/service/reservations.py:509`) — W5 와 같은 뿌리
