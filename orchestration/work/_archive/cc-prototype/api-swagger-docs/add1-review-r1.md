# 리뷰 리포트 — WORK-013 add1 외부 API 3개(가능 시간대 · 과거 시술 · 예약 내역) / code 검수 r1 (2026-11-12)

- 대상: 워크트리 `/Users/kknaks/orca/workspaces/cc-prototype/api-swagger-docs` · 브랜치 `kknaksss/ext-api-add1` · base `e0e4a16` · 미커밋 diff(수정 10파일 +392 −26) + 새 시험 2파일
- 기준: SPEC-008 **0.3.1** §6.6 ~ §6.9 · §7 · §8 · T29 · T32 ~ T44 / DEC-011 D-01 ~ D-15 / WORK-013 WP-REVIEW / 문서 검수 `review-doc-add1.md` W1 ~ W6 · I2 / `add1-be-report.md`
- read-only다. 워크트리 파일 수정 0 · KOS 호출 0 · 서버 기동 0 · 사용자 포트 0.
- 확인 방법: scratchpad 의 재현 스크립트(가짜 KOS · TestClient)와 **scratchpad 사본에서만 한 변이 시험**. 스크립트는 `add1/prop.py` · `add1/http_check.py` · `add1/cmp.py` · `add1/mutants.txt`.

## 판정: **WARN** (FAIL 0 · WARN 1 · 경미 3)

검수 축 1 ~ 7은 모두 계약대로다.
- 핵심인 「목록에 있는 시각이면 정원으로 거절되지 않음」은 전수 대조 12만 2천 경우에서 어긋남이 0이다.
- 직원 쪽(`reservations.py` · `reservation_rules.py`)은 diff 0이고, 직원 OpenAPI 차이도 0이다.

WARN 1은 Swagger 문구 한 줄(가능 시간대 400 줄)이 SPEC §6.6 오류 표와 다른 것이다. 경미 3은 머지를 막지 않는다.

### 수치(직접 1회씩)

| | 결과 |
|---|---|
| `uv run pytest -q` | **639 passed**(599 → +40) · 1 warning(httpx 사용 중단 경고) · 70.7s. be 주장과 같다 |
| `uv run ruff check .` | All checks passed |
| 정원 규칙 전수 대조(`prop.py`) | 구역 1 ~ 3개 × 칸 값 {행 없음, capacity None·0~3 × count None·0~4} × 기본 구역 env 전부 = **122,109 경우**. 그중 목록에 나오는 78,021 경우에서 예약 생성 `_pick_zone` → `is_full` 이 참인 것 **0** |
| 직원 OpenAPI(`openapi-after.json` ↔ 지금) | 직원 경로 차이 **0** · 직원 스키마 차이 **0** |
| 외부 옛 셋(r2 덤프 ↔ 지금) | 바뀐 것은 세 operation 의 429 줄(「외부 경로 전부 합산」)과 500 줄(main 의 수정 2 몫)뿐이다. 옛 Ext 스키마 변화 0. 새 스키마 7개 |
| 변이 시험(사본에서 11개) | **8개 잡힘** · 3개 살아남음(경미 N2) |
| public grep(diff + 새 시험) | 이메일 = `a@example.com` · `b@example.com` 뿐 · id = `vis-1` · `grp-1` 같은 지어낸 값 · 실명 · 연락처 · 키 꼴 · hex · UUID 0 |
| 워크트리 | `git status` 가 검수 전과 같다(수정 10 · 새 파일 2) |

## 검수 축별

| 축 | 결과 | 근거(파일:줄) |
|---|---|---|
| 1 정원 규칙 하나 | **맞음** | `service/ext.py:328-340` `_seats`. 예약 생성과 같은 `reservation_slot` 사본 행(`tx.slots` · 그룹 · 구역 · 시각)과 같은 `is_full` 을 본다. 「참」 · 행 없음 · capacity null 은 0으로 센다. 합 ≥ 1 이면 `capacity − count ≥ 1` 인 구역이 있다 ⇒ `_pick_zone`(`service/reservations.py:857-873`)의 `has_room` 이 참인 구역이 적어도 하나 있다 ⇒ `slot_full`(`:818-819`) 없음. 전수 대조 0건. 키가 조금 다르다: 목록은 `kst_min` 분 단위, 생성은 `start_at == start` 정확 일치. 어긋나면 생성 쪽이 「행 없음 = 자리 있음」이 되므로 안전한 방향이다. 공유로 빼낸 것은 `_ext_group()`(`:254-266`)뿐이다. 이것은 예약(§6.5)에서 옮긴 같은 코드다(문구 상수만 바뀜). 직원 서비스 · 규칙 diff 0 · 기존 시험 단언 약화 0(아래 축 6) |
| 2 가능 시간대 | **맞음** | 기본 그룹만(`:302` `_ext_group`). 운영 구간 × 간격 = `open_spans` + 자정 경계 `m = a + (-a % iv)` · `m + iv ≤ b`(`:315-325`). 남은 0 · 행 없는 구역 제외는 `_seats`. 오늘 지난 시각은 `at > now`(KST 하루 `d0` 기준). 날짜 검사(`:289-297`): `str` 질의(`api/ext.py:270-273`) → `DAY_RE.fullmatch` 가 빈 문자열을 먼저 막음 → `parse_day` → 오늘~90일. 순서는 400 → 503 → runtime 없음 502 → KOS 다. 요청마다 `refresh_slots` 1번이고, 날짜 잠금 안에서 `replace_slots` 를 한다(`kos/reservation_sync.py:322-328` · I2). 실패는 예외 → 502이고 사본은 그대로다(`_slots` 가 `_data_list` 에서 먼저 터짐). 재현: 전각 숫자 · 앞뒤 공백 · 끝 `\n` · `T00` · `/` · `0000-01-01` 전부 400 `date: …` · KOS 0번. `date` 두 번이면 마지막 값을 쓴다 |
| 3 과거 시술 · 예약 내역 | **맞음** | `_schedules`(`:342-358`) = `find` 그대로(404 · 409 문구 상수 같음). `resp.get("data", [])` → 배열 아니면 502. `deleted` 는 한 곳에서 거른다. 과거 = `start < now` 내림차순 · 50(`:366` · `:374`). 내역 = `start ≥ 오늘 0시` 오름차순(`:383`). `state_of(...)[0]` = 7값. `reservation_id_of` 는 읽기만 한다(`:387` · SELECT). 시험 T39 로 404 가 세 경로 바이트까지 같은 것과 사본 행 수가 그대로인 것을 확인했다 |
| 4 개인정보 · 보안 | **맞음** | 응답 칸 = SPEC 칸만(스키마 `schemas/ext.py:156-203`). 재현(`http_check.py`): 이름 · 이메일을 실은 KOS 503 본문 · 이름 검색 401 · 슬롯 500 · 가능 시간대 `?name=&email=` 질의에서 로그 + `ext_call` 에 이름 · 이메일 · 키 **0**. 로그는 `describe(e)`(상태 · 이름)뿐이다. 새 셋 모두 `no-store`(오류 포함) · `ext_call.endpoint` = 경로 틀. 키 없음 + `date` 없음 = 401(키가 먼저). 이름 · 이메일은 본문 POST 로만 받는다 |
| 5 Swagger | **WARN 1** | 새 셋 `summary` · `description` · 칸 설명 · 표 = `errors(*COMMON, …)`. 429 줄 「외부 경로 전부 합산」(`api/ext.py:103-105`). 앱 설명 「경로 여섯」. `git grep 셋\|세 경로\|세 엔드포인트 app/` 에 남은 것은 알림 「셋 다」(외부와 무관) 1줄뿐이다. parameters 단언은 넓히기만 했다 — `{X-Api-Key header, date query}` 집합 같음 + query 는 availability 하나뿐. 직원 문서 차이 0. → 400 줄 문구만 SPEC 과 다르다(W1) |
| 6 시험 | **맞음 · 빈 곳 경미** | T32 ~ T44 대조표(be §3)의 시험이 실제로 있다. 기존 시험 변경은 셋이다: 개수 `n_ops - 5 - 6`, 경로 집합 여섯 · 77, parameters 단언 넓힘. 지우거나 약하게 한 단언 0. `fake_kos` 는 `slot_patch` · `slots_page` 가 비면 기본 동작 그대로다. 변이 11개 중 8개를 잡는다 → 살아남은 3개는 N2 |
| 7 public | **맞음** | 위 수치 표 |

## WARN

| # | 자리 | 무엇 | 근거 | 고칠 방향 |
|---|---|---|---|---|
| W1 | `app/api/ext.py:209-211` `AVAIL_INVALID` · `tests/test_ext_docs.py`(`test_t29_add1_docs` 의 `"\`date: …\`" in …400` 단언) | Swagger 400 줄이 「질의 `date` 없음 · … message = `<위치>: <이유>`(**`date: …`**)」다. 그런데 `date` 가 없을 때 실제 message 는 **`query.date: Field required`** 다(T34 · 재현). SPEC §6.6 오류 표는 두 경우를 나눠 적는다 — 없음 = `query.date: …`, 빈 문자열 · 꼴 · 범위 = `date: …`. 「빈 문자열」 갈래도 표에 없다. r1 W4(조회 400 줄의 `start`)와 같은 종류다 | SPEC §6.6 오류 표 · §9 T34 · 재현 `cl.get(URL)` → `query.date:` | 문구를 SPEC 표대로 바꾼다: 「`date` 없음(message `query.date: …`) · 빈 문자열 · `YYYY-MM-DD` 꼴 아님 · 오늘(KST) 앞 · 오늘 + 90일 뒤(message `date: <이유>`)」. T29 단언에 `query.date:` 를 하나 더한다 |

## 경미 지적(머지 막지 않음)

| # | 자리 | 무엇 | 방향 |
|---|---|---|---|
| N1 | `service/ext.py:360-391`(→ `domain/reservation_rules.py` `schedule_start` · 응답 모델) | 일정 **원소** 모양이 깨지면 502가 아니라 `500 internal_error` 다. 재현: `reservation` 이 문자열(묶음 없음) · `reservationTime` 이 문자열 → 두 경로 다 500. 작업 `title` 이 숫자 → 과거 시술 500(응답 모델 검증). 본문 · 로그에 새는 것은 없다. SPEC 이 정한 502는 「`data` 가 배열 아님」뿐이라 계약 위반은 아니다. 직원 「이전 방문」도 같은 함수라 같은 성질이다. 다만 그 고객은 일정 하나 때문에 매번 500을 받는다(재시도 신호 아님) | 원소 처리에서 예외가 나면 그 원소만 건너뛰거나 502로 바꾼다. 아니면 SPEC §6.7 에 「원소 모양 오류 = 500」을 한 줄 적는다(planner 판단) |
| N2 | `tests/test_ext_history.py` · `tests/test_ext_availability.py` | 변이 중 살아남은 3개다. ① 과거 시술 `start >= now` → `> now`(시작 = 지금 정확히인 일정이 과거로 들어감) ② 예약 내역 `start < today0` → `<= today0`(오늘 00:00 정각 일정이 빠짐) ③ `refresh_slots` 날짜 잠금 제거(I2). ① · ②는 SPEC 경계(「지금보다 앞」 · 「0시와 같거나 뒤」)를 고정하는 시험이 없다는 뜻이다. 그 밖에 일정 읽기 4xx · 401 → 502(T39는 503만)와 가능 시간대 4xx · 401 때 「사본 그대로」 단언도 없다(코드는 `except Exception` 하나라 동작은 맞다) | T41 옆에 경계 두 줄을 넣는다(시계 = 일정 시작 정각 → 과거 시술에 없음 · 예약 내역에 있음 / 오늘 00:00 일정 → 내역에 있음). 잠금은 시험 없이 둬도 된다(be 도 적음) |
| N3 | SPEC §6.6 1단계 · be §6 차이 1 | 코드는 정규식 `\d{4}-\d{2}-\d{2}` 를 `parse_day` 앞에 둬서 `2026-W43-4` 를 막는다(10글자 · `fromisoformat` 은 받음). SPEC 글자(「10글자가 아니거나 `fromisoformat` 이 받지 않으면」)만 따르면 이 값은 통과해야 한다. 오류 표 「`YYYY-MM-DD` 꼴 아님」 뜻으로는 코드가 맞다 | SPEC §6.6 1단계에 「`YYYY-MM-DD` 숫자 꼴(ISO 주 날짜 등 다른 ISO 꼴은 400)」을 한 줄 적는다(planner) |

## 문서 검수(review-doc-add1) 지적 → 코드에서 닫혔나

| # | 결과 | 근거 |
|---|---|---|
| W1 `{}` = 빈 목록 | **닫힘** | `service/ext.py:354-357` · `test_w1_empty_object_is_empty_list` · 변이 「`resp.get("data")`」을 잡음 |
| W2 `deleted` 뺌 | **닫힘** | `:358` 한 곳 · `test_w2_deleted_schedules_dropped_from_both` · 변이 잡음 |
| W3 parameters 단언 | **닫힘** | `test_ext_docs.py` 끝 — 지우지 않고 `(이름, in)` 집합 + 「query 는 availability 하나」로 넓혔다. `name` · `email` 질의가 생기면 실패한다 |
| W4 「셋」 문구 | **닫힘** | `EXT_RATE` · 앱 설명 고침 · grep 잔여는 알림 「셋 다」뿐 · 여섯 operation 429 단언 |
| W5 날짜 칸 | **닫힘** | `date: str = Query(...)` · 빈 문자열 먼저 · 없음 = `query.date:`(T34). Swagger 문구만 → W1 |
| W6 오류 갈래 시험 | **닫힘** | runtime 없음 · KOS 4xx/401/5xx(가능 시간대) · 이름 검색 실패(두 경로) · 405(세 경로) · `COMMON` 표(T29 `OPS` 여섯 루프) |
| I2 잠금 | **닫힘(시험 없음)** | `kos/reservation_sync.py:324` 가 `ensure` 와 같은 `_locks[day]` 를 쓴다. `refresh_slots` 를 부르는 쪽이 잠금을 들고 있지 않아 교착이 없다 |

## backend 리포트 §6 차이 1 ~ 7 판정

| # | 판정 | 까닭 |
|---|---|---|
| 1 날짜 정규식이 `parse_day` 보다 엄격 | **받음** | 오류 표 「`YYYY-MM-DD` 꼴 아님」과 같은 뜻이다. SPEC 글자 보강 → N3 |
| 2 `{"data": null}` = 502 | **받음** | SPEC §6.7 2 「`data` 가 있으면서 배열 아님」 그대로다. 시술권(§4.3 · `:229`)과 같은 처리 · T39 |
| 3 `end` = `resources_of` 첫 묶음 · 시각 없는 묶음은 버림 | **받음** | SPEC §6.8 「첫 묶음 끝 · 묶음 없으면 null」 · 사본 쓰기와 같은 함수다. 시작 · 끝이 없는 묶음은 묶음으로 보지 않는다(직원 판과 같음) |
| 4 `deleted` 한 곳 | **받음** | DEC-011 D-15 |
| 5 실물 KOS 의 `deleted` · `{}` 미확인 | **받음 → E2E** | 아래 「조용히 통과」 |
| 6 데모 `reservationId` null | **받음 → E2E** | 임시 DB 탓이다. T40 `test_t40_external_reservation_shows_its_id` 가 계약을 고정한다. 실물은 WP-E2E-LOCAL ② · ③ |
| 7 동시 경합 미시험 | **받음** | SPEC §6.6 · DEC-011 D-02 가 받아들인 예외다 |

## DEC-011 대조(코드 기준)

D-01 공유 규칙(T44 · 재현) · D-02 같은 규칙(전수 대조) · D-03 칸 · 메모 · 의사 없음(T38 키 부재) · D-04 오늘 이후 · 취소 포함 · D-05 같은 `find` · 404 바이트 · D-06 본문 POST(parameters 단언) · D-07 경로 셋(`test_order`) · D-08 오늘~90(T34) · D-09 503 KOS 전(T35) · D-10 50 · D-11 행 없음 · null 빼기(T32) · D-12 1번 · 공유 사본(T36) · D-13 칸 · id · 2계층 상태(T40) · D-14 겹침 · 문장(T41 · T29) · D-15 `deleted`(W2) — **모두 맞다.**

## 조용히 통과하는 자리

- **슬롯 경계 정렬**: 가짜 KOS 는 슬롯을 시간표 시작부터 간격으로 만든다. 그래서 늘 「자정 기준 간격 경계」와 맞는다. 실물 KOS 칸 시작이 그 경계와 어긋나는 그룹(예: 10:15 시작 · 간격 30)이면 모든 후보에 행이 없다 ⇒ **오류 없이 `slots: []`** 가 나간다. 안전한 방향이지만 「예약 가능 0」으로 읽힌다. 데모에서는 오늘 15칸 · 내일 20칸이 나와 맞았다(be §4). → WP-E2E-LOCAL ①에서 KOS 웹 칸 시각과 한 번 견주기를 권한다
- **`get-schedules-by-visitor` 의 `deleted` · `{}`**: 가짜는 늘 `{"data": [...]}` 를 준다. 실물이 지운 일정을 주는지, 일정 없는 고객에게 `{}` 를 주는지는 아직 보지 못했다(be §6-5). 코드는 두 경우를 모두 맞게 처리한다. → WP-E2E-LOCAL ③에서 일정 없는 데모 고객이 있으면 1번
- **일정 원소 모양 오류 = 500**(N1): 가짜는 늘 바른 모양이라 시험이 닿지 않는다
- **중복 검사 흉내**(r1 · r2 에서 이어짐): `find-duplicated-visitor` 의 이메일 대소문자 비교 방식은 실물 미확인이다 → WP-E2E-LOCAL 몫 그대로
- **가능 시간대가 직원 판 사본을 바꾼다**: 외부 호출이 그날 직원 예약 현황의 정원 표시를 새 값으로 바꾼다(SPEC §6.6 부작용 · 의도). `set_sync` · 날짜 캐시는 건드리지 않으므로 직원 화면의 「마지막 동기화」 표시는 그대로다. 같은 규칙이라 결과는 같다
- **경계 시각**(N2 ① · ②): 지금과 같은 시각 · 오늘 0시 정각 일정의 갈래가 시험에 없다. 지금 코드는 SPEC 대로다
