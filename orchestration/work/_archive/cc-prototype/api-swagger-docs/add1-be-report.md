# add1 backend 리포트 — 외부 API 3개(가능 시간대 · 과거 시술 · 예약 내역)

- 워크트리 `api-swagger-docs` · 브랜치 `kknaksss/ext-api-add1`(base `e0e4a16`) · **커밋 안 함**
- 계약: SPEC-008 **0.3.1**(작업 중 0.3.0 → 0.3.1 · 「add1 고침 1」 = `add1-be-amend-1.md` 반영) · DEC-011 D-01 ~ D-15 · WORK-013 BE1 ~ BE3

## 1. 변경 파일 · WP 별 무엇

| 파일 | WP | 무엇 |
|---|---|---|
| `app/kos/reservation_sync.py` (+8) | BE1 | `refresh_slots(day)` 하나만 더함 — 사본 `present` 그룹 전부 · 그날 KST 하루로 지금 `_slots()` 를 부른다. 날짜 잠금(`_locks`) 안(고침 1 I2). 실패는 예외 그대로 → 사본 그대로 |
| `app/service/ext.py` (+148) | BE1 · BE2 | `_ext_group()` — 예약 · 가능 시간대가 같이 쓰는 기본 그룹 검사(503 · KOS 전, 예약 쪽은 이 함수로 옮김 · 동작 같음) / `availability()` · `_day()` · `_seats()` / `_schedules()` · `visits()` · `reservations()` |
| `app/schemas/ext.py` (+50) | BE1 · BE2 | `ExtCustomerRequest`(= `ExtLookupRequest` 상속 · 같은 칸 · 같은 검증) · `ExtSlot` · `ExtAvailability` · `ExtVisit` · `ExtVisits` · `ExtCustomerReservation` · `ExtCustomerReservations` — 모든 칸 `description` |
| `app/api/ext.py` (+91) | BE1 ~ BE3 | 새 세 경로 · `summary` · `description`(`AVAIL_DOC` · `VISITS_DOC` · `CUSTOMER_RESV_DOC`) · 응답 표(`errors(*COMMON, …)` 셋 다) · `EXT_RATE` 「외부 경로 전부 합산」 |
| `app/openapi_docs.py` | BE3 | 앱 설명 「경로 셋」 → **「경로 여섯」**(새 셋 줄 더함) · 호출 제한 「세 경로 합산」 → 「외부 경로 전부 합산」 |
| `tests/fake_kos.py` | BE1 | `slots_page`(슬롯 응답 통째로) · `slot_patch`((그룹, 구역, KST HH:MM) → 정원 · 예약 수 덮어쓰기 / None = 행 없음). 기본 동작 그대로 |
| `tests/test_ext_availability.py` (새) | BE1 | T32 ~ T37 · T42 · T43 몫 + 고침 1 W5 · W6 |
| `tests/test_ext_history.py` (새) | BE2 | T38 ~ T43 + 고침 1 W1 · W2 · W6 |
| `tests/test_ext_auth.py` | BE3 | T44 두 개 |
| `tests/test_ext_docs.py` | BE3 | `OPS` 여섯 · 429 줄 단언 · parameters 단언 넓힘(W3) · `test_t29_add1_docs` |
| `tests/test_openapi_docs.py` | BE3 | `secured == n_ops - 5 - 6` · 주석 |
| `tests/test_order.py` | BE3 | 외부 경로 집합 여섯 · 합계 77 |

- **diff 0**: `app/service/reservations.py` · `app/domain/reservation_rules.py`(가져다 쓰기만 — `is_full` · `open_spans` · `to_min` · `kst_min` · `day_range` · `parse_day` · `schedule_start` · `PREV_RESULT` · `ROOM_TASK_TITLE` · `state_of` · `ResvContext.enabled_zones` · `resources_of` · `tx.slots` · `tx.reservation_id_of`)
- **같은 함수 · 같은 사본**: 가능 시간대 `_seats()` 는 예약 생성 정원 검사와 같은 `reservation_slot` 행(그룹 · 구역 · 시작)과 같은 `is_full()` 을 본다. 「참」 구역 = 0 · 아니면 `max(0, capacity − (count or 0))`. 합 ≥ 1 이면 `_pick_zone` 이 자리 있는 구역을 반드시 찾는다. 새로 빼낸 공유 함수는 없다(직원 경로 결과 무변경)
- 내보내는 칸: SPEC 칸만. 메모 · 의사 · 담당자 · 그룹 · 구역 이름 · KOS id 없음(T38 · T40 이 응답 글자로 단언)

## 2. 기준선 → 이후

| | 시작 전(`e0e4a16`) | 끝 |
|---|---|---|
| `uv run pytest -q` | **599 passed** | **639 passed**(+40) |
| `uv run ruff check .` | All checks passed | All checks passed |

WP 부분 명령: BE1 `test_ext_availability · test_ext_reserve · test_resv_board` 57 passed / BE2 `test_ext_history · test_ext_lookup · test_resv_detail` 47 passed / BE3 `test_ext_docs · test_openapi_docs · test_order` 36 passed · `test_ext_auth` 16 passed → 전체 1회.

변이 확인 1개: `availability()` 의 `refresh_slots` 호출을 빼면 `test_ext_availability.py` 7개가 실패한다(T36 · T37 이 「새로 읽기」를 실제로 잡는다). 확인 뒤 되돌렸다.

## 3. T32 ~ T44 대조표

| T | 시험 |
|---|---|
| T32 | `test_ext_availability.py::test_t32_candidates_and_seats`(간격 30 · 쉬는 시간 · 구역 둘 · A 몫만 · 행 없음 · capacity null · 둘 다 참 · 휴무 요일 · 응답 키 · `+09:00`) · `test_t32_interval_15` |
| T33 | `test_t33_today_past_times`(14:10 → 14:30 부터 · 정확히 14:30 → 15:00 부터) |
| T34 | `test_t34_bad_date`(7개 · message `date: …` · KOS 0) · `test_t34_missing_date_and_range_edges`(없음 = `query.date: …` · 오늘 · +90 = 200 · +91 = 400) |
| T35 | `test_t35_not_configured`(env 빔 · present 0 · 켜진 구역 0 → 503 · KOS 0) |
| T36 | `test_t36_refresh_one_call_replaces_copy`(1번 · 본문 그룹 셋 · 하루 범위 · 사본 바뀜 · 5xx · 모양 오류 · runtime 없음 → 502 · 사본 그대로) · `test_w6_availability_kos_4xx_401_502` · `test_w6_availability_no_runtime_502_zero_calls` |
| T37 | `test_t37_stale_full_copy_then_listed_then_reserved`(①) · `test_t37_every_listed_time_reserves_and_unlisted_full_409`(② 목록 16칸 전부 200 · ③ 모두 참 시각 409) |
| T38 | `test_ext_history.py::test_t38_visits`(55건 → 50 · 내림차순 · 결과 다섯 갈래 · 「방 배정」 뺌 · 시트팩 남음 · 빠지는 키 · 빈 목록) |
| T39 | `test_t39_customer_branches_same_404_and_no_schedule_read`(네 경우 × 세 경로 404 바이트 같음 · 409 · 일정 읽기 0 · 5xx · 배열 아님 · `data: null` → 502 · 사본 행 수 같음) · `test_w1_empty_object_is_empty_list` · `test_w6_name_search_failure_502_no_schedule_read` · `test_w6_no_runtime_502` |
| T40 | `test_t40_reservations`(오늘 0시 이후 · 오름차순 · 취소 · 부도 · 상태 갈래 · 사본 id · null · `end` · 묶음 없음 null · 키 · 사본 행 같음 · 지난 것만 → `[]`) · `test_t40_external_reservation_shows_its_id` |
| T41 | `test_t41_today_overlap` |
| T42 | `test_t42_request_fields`(두 경로 × 모르는 키 · 빈 이름 · 빈 이메일 · 이메일 없음 → 400 · KOS 0) · `test_ext_availability.py::test_t42_name_query_ignored_and_endpoint` |
| T43 | `test_ext_history.py::test_t43_cost`(200 = 2 · 404 = 1 · 409 = 1) · `test_ext_availability.py::test_t43_availability_cost`(1) · T35 · T34 의 KOS 0 |
| T44 | `test_ext_auth.py::test_t44_shared_rules_new_three`(401 · no-store · `ext_call.endpoint` 셋 · `POST /api/ext/availability` 405 · 표 · 로그에 이름 · 이메일 · 키 0) · `test_t44_one_limit_across_six`(메뉴 30 + 가능 시간대 30 → 61번째 과거 시술 429) · 공통 표 줄은 `test_ext_docs.py::test_t29_ext_swagger` 의 `OPS` 여섯 루프(401 · 429 · 405 · 500) · `test_w6_availability_post_405` · `test_w6_wrong_method_405` |
| T29 | `test_ext_docs.py::test_t29_ext_swagger`(여섯) · `test_t29_add1_docs` · `test_openapi_docs.py` 전부 |

## 4. 데모 실물(KOS 조회만 · 값 0)

스크립트 + TestClient + 실 KosClient(keep-alive 끔) · 임시 DB `/tmp/add1-demo-XXXX` → 지움(남은 것 0) · 외부 키는 로컬 임시값으로 덮어씀 · 운영 지점 키 안 씀.

- 예약 목록(master) 성공 · 예약 그룹 13 · 기본 그룹 env 있음
- 가능 시간대 **오늘 200**(276 ms · 칸 15 · 남은 자리 합 45 · 칸 최소 3) · **내일 200**(217 ms · 칸 20 · 합 60 · 최소 3) · 응답 키 `{date, intervalMinutes, slots}` · 모든 `start` `+09:00`
- 어제 날짜 400 · 키 없음 401
- email 있는 데모 고객 1명: **과거 시술 200**(153 ms · 8건 · 키 `{date, start, result, procedures}` · 결과 completed · other · 시술 이름 있는 것 5 · 메모 · 의사 칸 없음) · **예약 내역 200**(122 ms · 2건 · 상태 canceled · `reservationId` null 2 — 임시 DB 에 그날 사본이 없어서 · 예상대로 · `end` 다 있음)
- 틀린 이메일(끝 글자 1개 바꿈) → 조회 · 과거 시술 · 예약 내역 셋 다 404 · **본문 바이트 같음**
- `ext_call` 9줄 · 경로 틀만
- KOS 쓰기(예약 · 고객) **0**. `/commands/` 경로 2번은 토큰 받기(`exchange-token` · `sign-in`)뿐이다
- 정원 · 예약 수를 KOS 웹 예약 현황과 맞춰 보는 것(① · ②)은 WP-E2E-LOCAL(코디) 몫이라 하지 않았다

## 5. Swagger 확인

- `/api/openapi.json` 에 외부 여섯이 tag `외부 연동` 하나 · `security [{ExtApiKey: []}]` · Bearer 아님(`n_ops - 5 - 6` 통과)
- 새 셋: `summary` · `description` · 모든 응답 칸 `description`(「설명 빠진 곳 0」 시험 통과) · 응답 표 = 공통(401 · 429 · 405 · 500) + 400 · (가능 시간대) 502 · 503 / (두 고객 경로) 404 · 409 · 502
- 설명 문장: 가능 시간대 = 기본 그룹 하나 · 운영 구간 안 간격 칸 · 0 · 지난 칸 · 자리 수 모르는 칸 안 나옴 · 「목록에 없어도 예약이 될 수 있다」 · 「그 사이 다른 예약이 끼면 `409 slot_full`」 · 날짜 범위 · KOS 1번 / 과거 시술 = 최근 50 · 메모 · 의사 없음 / 예약 내역 = 오늘 0시 이후 · 취소 포함 · `reservationId` null 뜻 / 둘 다 = 같은 고객 찾기 · 띄어쓰기 · 404 바이트 같음 · 오늘 겹침 문장 · KOS 2번
- 질의 칸은 가능 시간대 `date`(required) 하나뿐 — 그 밖 query · path 칸 0 을 시험이 단언

## 6. SPEC ↔ 코드 차이 · 확인 못 한 것

1. **날짜 꼴 검사가 `parse_day` 보다 조금 엄격하다**: 정규식 `\d{4}-\d{2}-\d{2}` 를 먼저 보고 → `parse_day`(10글자 + `fromisoformat`). 파이썬 `fromisoformat` 은 10글자 ISO 주 날짜 `2026-W43-4` 도 받기 때문에 이것을 400 으로 막았다(시험 있음). `YYYY-MM-DD` 꼴만 받는다는 SPEC 뜻과 같다고 봤다 — 다르게 원하면 한 줄
2. 일정 응답 `{"data": null}` 은 「`data` 가 있으면서 배열 아님」으로 보아 502 다(W1 문구 그대로 · 시험 있음)
3. 예약 내역의 `end` 는 `resources_of` 첫 묶음 끝이다 — 시작 · 끝이 없는 묶음은 `resources_of` 가 버리므로 그런 묶음만 있으면 null
4. 지운 일정(`deleted: true`) 은 `_schedules()` 한 곳에서 거른다(D-15 · 두 목록 다)
5. KOS 공개 `get-schedules-by-visitor` 가 실제로 지운 일정을 돌려주는지 · `{}` 를 주는지는 데모에서 보지 못했다(이번 고객은 `data` 배열이었다)
6. 데모 예약 내역의 `reservationId` 가 null 인 것은 임시 DB 탓이다. 「외부 예약 → 그 id 로 보임」은 시험(T40)으로만 봤고, 실물은 WP-E2E-LOCAL ② · ③ 몫이다
7. 동시 요청 경합(목록과 예약 사이 다른 예약)은 시험하지 않았다(SPEC 이 받아들인 예외)

## 고침 1 (add1-be-amend-1.md · SPEC 0.3.1) 대조

| # | 한 것 | 시험 |
|---|---|---|
| W1 | `resp.get("data", [])` — 키 없음 · `[]` = 빈 목록 200 · 있으면서 배열 아님 = 502(`_data_list` 안 씀) | `test_w1_empty_object_is_empty_list` · T39 의 `{"data": {"x":1}}` · `{"data": null}` |
| W2 | `deleted: true` 일정은 `_schedules()` 한 곳에서 빼서 두 목록 다 빠짐(DEC-011 D-15) | `test_w2_deleted_schedules_dropped_from_both` |
| W3 | parameters 단언을 지우지 않고 넓힘 — `X-Api-Key`(header) + availability `date`(query)만 · 그 밖 query 가 생기면 실패 | `test_t29_ext_swagger` 끝 |
| W4 | `git grep -n "셋\|세 경로\|세 엔드포인트" app/` → 외부 쪽 두 곳을 「외부 경로 전부 합산」으로(남은 줄은 「오프셋」 · 알림 「셋 다」 — 외부와 무관) · 앱 설명 「경로 여섯」 | 여섯 operation 429 줄 단언 · 앱 설명 외부 절에 「셋」 없음 |
| W5 | `date: str = Query(...)`(pydantic date 아님) · 빈 문자열 먼저 400 · 꼴 → `parse_day` · 범위. 없음 = `query.date: …` | `test_t34_*` |
| W6 | runtime 없음 → 502 · KOS 0 / 이름 검색 5xx → 502 · 일정 읽기 0 / `POST /api/ext/availability` → 405 · 새 셋 모두 `errors(*COMMON, …)` · 경로마다 1줄 | `test_w6_*`(가능 시간대 3 · 고객 두 경로 3) · T44 |
| I2 | `refresh_slots` 를 날짜 잠금(`ensure` 의 `_locks`) 안에서 | (동작 시험은 T36 · 잠금 자체 시험 없음) |

## 고침 2 (add1-be-fix-1.md · 코드 검수 add1-review-r1 반영)

| # | 한 것 | 시험 |
|---|---|---|
| W1 | `api/ext.py` `AVAIL_INVALID` 400 줄 = SPEC §6.6 표대로 「`date` 없음(message `query.date: …`) · 빈 문자열 · `YYYY-MM-DD` 꼴 아님 · 오늘(KST) 앞 · 오늘 + 90일 뒤(message `date: <이유>`)」 | `test_t29_add1_docs` 400 줄 단언(`query.date: …` · 빈 문자열 · `date: <이유>`) |
| N1 | `service/ext.py` `visits()` · `reservations()` 의 원소 처리 + 응답 모델 검증(`ExtVisits` · `ExtCustomerReservations.model_validate`)을 한 `try` 로 감쌈 → `AttributeError` · `TypeError` · `ValueError`(pydantic 포함) · `KeyError` = `502 kos_unavailable` · 로그는 예외 종류만. 직원 「이전 방문」(`previous_visits`) · `reservation_rules.py` · `reservations.py` diff 0 | `test_n1_broken_schedule_item_502`(`reservation` 문자열 · `reservationTime` 문자열 → 두 경로 / 작업 `title` 숫자 → 과거 시술 · 본문에 원문 0) |
| N2 | 경계 시험 · 일정 읽기 4xx · 401 | `test_n2_start_equals_now_is_not_past`(시계 = 시작 정각 → 과거 시술 없음 · 내역 있음) · `test_n2_today_midnight_in_reservations`(오늘 00:00 있음 · 어제 23:30 없음) · `test_n2_schedule_read_4xx_401_502`(400 · 401 · 404 × 두 경로) |
| N3 | SPEC 몫 — 코드 그대로 | — |

- 변이 확인(되돌림): `start >= now` → `> now` · `start < today0` → `<= today0` · `except` 를 `KeyError` 만으로 → 셋 다 시험이 잡음(1 · 1 · 3 실패)
- 부분: `test_ext_history · test_ext_docs · test_resv_detail` 42 passed → 전체 `uv run pytest -q` **647 passed**(639 → +8) · `ruff` All checks passed
- 「`title` 숫자」 갈래는 예약 내역에 나가는 칸이 아니라서 과거 시술만 502 다(예약 내역은 작업을 보지 않음 · 200)
