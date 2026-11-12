# 리뷰 리포트 — WORK-013 add1 / code 재검수 r2(고침 2) (2026-11-12)

- 대상: 워크트리 `/Users/kknaks/orca/workspaces/cc-prototype/api-swagger-docs` · 브랜치 `kknaksss/ext-api-add1`(미커밋)
- 기준: SPEC-008 **0.3.2**(DEC-011 D-16 · N3 · T45 ~ T47) · 고침 지시 `add1-be-fix-1.md` · `add1-be-report.md` 「고침 2」 · 지난 리포트 `add1-review-r1.md`
- read-only다. 워크트리 수정 0 · KOS 호출 0 · 서버 기동 0.
- 확인 방법: scratchpad 재현 스크립트(`add1/http_check.py` — 가짜 KOS · TestClient)와 **scratchpad 사본에서만** 한 변이 시험(`add1/mutants2.txt`)

## 판정: **PASS** (FAIL 0 · WARN 0 · 경미 1)

r1 의 W1 · N1 · N2 는 모두 닫혔다. N3 은 SPEC 0.3.2 §6.6 1단계에서 닫혔다. 직원 「이전 방문」 동작은 바뀌지 않았다. 경미 1은 SPEC T47 문구 하나다.

### 수치(직접 1회씩)

| | 결과 |
|---|---|
| `uv run pytest -q` | **647 passed**(639 → +8) · 1 warning(httpx 사용 중단 경고) · 67.5s. be 주장과 같다 |
| `uv run ruff check .` | All checks passed |
| 변이(사본 · 4개) | **4개 모두 잡힘**. ① 과거 `>=` → `>` 1 실패 ② 내역 `<` → `<=` 1 실패 ③ `except` 를 `KeyError` 만으로 3 실패 ④ 400 줄을 옛 문구로 1 실패. 고치지 않은 사본은 42 passed(`test_ext_history` · `test_ext_docs` · `test_resv_detail`) |
| 직원 쪽 diff | `service/reservations.py` · `domain/reservation_rules.py` **0**. `kos/reservation_sync.py` 는 r1 때와 같은 `refresh_slots` +8줄뿐이다 |

## r1 지적별

| # | r1 지적 | 확인 | 판정 |
|---|---|---|---|
| W1 | 가능 시간대 Swagger 400 줄 | `app/api/ext.py:209-211` = 「질의 `date` 없음(message `query.date: …`) · 빈 문자열 · `YYYY-MM-DD` 꼴 아님 · 오늘(KST) 앞 · 오늘 + 90일 뒤(message `date: <이유>`)」. SPEC §6.6 오류 표와 같다. T29 단언 `tests/test_ext_docs.py:80-81`(변이 ④ 잡음) | **닫힘** |
| N1 | 일정 원소 모양 오류 = 500 | `service/ext.py` `visits()` · `reservations()` 는 원소 처리 + 응답 모델 검증(`model_validate`)을 한 `try` 로 감싼다. `AttributeError` · `TypeError` · `ValueError`(pydantic 포함) · `KeyError` 가 나면 `_shape_error` → `502 kos_unavailable` 이고, 로그는 예외 종류만 남긴다. 고객 찾기 · KOS 호출(`_schedules`)은 `try` 밖이라 404 · 409 · 502 갈래가 섞이지 않는다. 재현 결과: `reservation` 문자열 · `reservationTime` 문자열 → 두 경로 **502**(r1 = 500). 작업 `title` 숫자 → 과거 시술 **502**. 로그는 `KOS 고객 일정 원소 형식: AttributeError` / `ValidationError` 뿐이고, 로그 + `ext_call` 에 이름 · 이메일 · 키 0, 본문은 공통 502 본문이다. 시작 시각 문자열 오류 · `id` 숫자는 지금처럼 200(그 원소만 건너뜀 · 정상 처리). **직원 「이전 방문」**: 감싸는 곳이 외부 서비스뿐이고 `previous_visits` · `schedule_start` 가 있는 두 파일 diff 0 · `test_resv_detail` 통과 → 동작 그대로다 | **닫힘** |
| N2 | 경계 · 일정 읽기 4xx/401 시험 | `test_n2_start_equals_now_is_not_past`(T45 ①) · `test_n2_today_midnight_in_reservations`(T45 ② · 어제 23:30 은 빠짐까지) · `test_n2_schedule_read_4xx_401_502`(400 · 401 · 404 × 두 경로 · T46). r1 에서 살아남은 변이 ① · ② 가 이제 잡힌다. 날짜 잠금(I2)은 r1 에 적은 대로 시험 없이 둔다 | **닫힘** |
| N3 | SPEC 날짜 꼴 문구 | SPEC 0.3.2 §6.6 1단계 「`YYYY-MM-DD` 숫자 꼴(숫자 4 · `-` · 숫자 2 · `-` · 숫자 2)」 = 코드 `DAY_RE`. 코드는 바뀌지 않았다 | **닫힘(SPEC)** |

## 새 지적(경미 · 머지 막지 않음)

| # | 자리 | 무엇 | 방향 |
|---|---|---|---|
| M1 | SPEC §9 T47(681 ~ 683행 부근) · `tests/test_ext_history.py:250-266` | T47 은 「`reservation` 문자열 · `reservationTime` 문자열 · 작업 `title` 숫자 → 과거 시술 · 예약 내역 **둘 다** 502」로 읽힌다. 그런데 예약 내역은 작업을 읽지 않으므로 `title` 숫자 갈래는 **200** 이다(be 리포트에 적혀 있다 · 재현 같음). 코드가 맞고 SPEC 글자가 넓다. 또 T47 의 「로그에 원문 0(caplog)」 단언은 시험에 없다. 이 리포트의 재현에서는 로그에 예외 종류만 있었다 | SPEC T47 에 「`title` 숫자는 과거 시술만(예약 내역은 작업을 보지 않음 · 200)」을 한 줄 적는다(planner). 시험에 `caplog` 로 `RAW-` 부재 한 줄을 넣으면 좋다(선택) |

## 조용히 통과하는 자리

- **넓은 `except`**: `TypeError` · `AttributeError` 까지 502 로 바꾼다. 그래서 앞으로 이 두 함수에 들어갈 **우리 코드 버그**도 「KOS 장애」(502)로 보인다. 지금 코드에는 그런 버그가 없다(재현 · 시험 통과). 로그의 예외 종류(`KOS 고객 일정 원소 형식: …`)로만 가려낼 수 있다는 점을 운영에서 알아 두면 된다
- r1 에 적은 나머지는 그대로다: 실물 KOS 의 `deleted` · `{}` 미확인, 슬롯 경계 정렬, 중복 검사의 이메일 대소문자 → WP-E2E-LOCAL 몫
