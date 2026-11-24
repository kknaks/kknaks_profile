# 코드 검수 3: E4 · E5 · 공지 수정 + KOS 공지 동기화

- 대상: 워크트리 `CENTURION_DAY/day-reservation`의 미커밋 변경 중 검수 2 이후분(be-feat-2 · be-feat-3 · fe-feat-2 · fe-feat-3).
- 기준:
  - SPEC-006 개정 ⑨(HEAD `039bbfd7`)
  - 결정 R56 ~ R62
  - `contract-v3-notice.md`(보충 1 · 2, KOS 장애 = 503)
- 이번 검수에서 파일은 고치지 않았고 커밋하지 않았다. stash도 쓰지 않았다.

## 판정: **PASS (WARN 4)**

FAIL은 없다. ① ~ ⑧ 모두 기준과 맞는다. WARN 4건은 실제 사용 중 짧게 어긋날 수 있는 자리와 시험이 비어 있는 곳이다.

## 돌린 시험 (직접 · 격리 컨테이너 · 전체 check.sh는 돌리지 않음)

| 묶음 | 결과 |
|---|---|
| `scripts/test.sh` 1차: 공지 저장 · KOS 공지 · 공지 동기화 · 공지 보기 · 담당자 규칙 · `tests/migrations/` 전체 · 예약 조회/규칙 · 원내 현황 · 화면/페이지 · 기본 권한 · 판 기본 보기 · KOS mapper · 날짜 최신화 2종 · `tests/architecture` | **573 passed** (87 s) |
| `scripts/test.sh` 2차: `backend/tests/day/board` 전체 (`load_world` 분리 회귀 확인) | **218 passed** |
| 프론트: `build.mjs --check` · ESLint/Stylelint · Prettier · `node --test tests/*.test.mjs` | 재현 일치 · lint 0 · 통과 · **116/116** |

## ① 공지 저장 분기 → **PASS**

대상은 `services/reservation_notice.py`와 `routers/reservations.py`다.

| 항목 | 근거 | 판정 |
|---|---|---|
| 검사 순서 401 → 403 → 400 → 409 | router에서 `writable_session`(세션 · CSRF) → `require_permission(NOTICE_KEY, EDIT)` → `_notice_form`(모르는 칸 400). service에서는 `parse_notice_day` → `parse_notice_id` → `check_content` → 지난 날짜 `NoticePastDate` 409(`:204-208`). 이 409는 KOS를 부르기 전에 난다 | PASS |
| 2,000 = 앞뒤 공백 자른 길이 | `check_content` `:82-84` `len(content.strip())`. 화면 글자 수도 `input.value.trim().length`(day.js `resNoticeCount`) | PASS |
| 보내는 글 = trim · 공백만 = 지우기 (R62 ③ · ④) | `:214` `text = content.strip()`. `plan`(`:140-145`)은 대상 있음 + 빈 값 → delete, 대상 없음 + 빈 값 → 호출 없음 | PASS |
| 대상 고르기 (R62 ② · 보충 1) | `notice_id`(DAY id) → `_kos_id`(같은 병원 · `entity_type='notice'` · 살아 있는 ref) → `pick_target`(`:87-95`). 다시 읽은 목록에 그 KOS id가 있으면 그것, 없으면 `found[0]`, 목록이 비면 None. `notice_id`가 uuid가 아니면 400 | PASS |
| create / change / delete | `_write` `:174-189`. create는 그 날 00:00(`start`)을 `releaseDateTimeUtc`로 보낸다. 같은 글도 다시 보낸다(비교하지 않음) | PASS |
| 오류 코드 | KOS 4xx → 409 `kos_rejected`. 5xx · 응답 없음 · 시간 초과(`post_kos`가 `httpx.HTTPError`를 `KosError`로 바꿈) · 연결 없음 → 503 `kos_unavailable`(보충 2). 화면은 `notice_error_handler`가 본문 없이 그 HTTP + `X-Day-Error` + `HX-Reswap: none`으로 받는다 | PASS |
| 403 | 권한이 없으면 403 조각을 돌려주고, 화면은 status ≥ 400이라 끼우지 않고 실패 줄을 그린다. 기본 행은 `policies/permissions.py`의 full · view 둘 다 `reservation.notice` edit | PASS |
| 기록 | 실패는 `kos_rejected {op, httpStatus, kosError}`, 성공은 `notice_save {date, op, length, noticeId}`. 본문 글은 남기지 않는다 | PASS |

**시험:** `test_reservation_notice.py`에 9건이 있다. 만들기 · 고치기 · 지우기 · 호출 없음, 앞날 허용과 지난 날짜 409, 409 · 503에서 글 유지, 401, 403과 400, CSRF, R62 대상 고르기, 공백만 = 지우기, 다시 읽기 실패.

## ② 누른 직원 토큰 · 시스템 토큰 누출 → **PASS**

- **토큰 출처:** `_staff_token` `:148-159`는 **이 세션**의 `ExternalSession`(만료 전 · 살아 있는 행)만 읽는다. 없으면 `SessionExpired`이고, 다른 직원 토큰이나 시스템 계정으로 넘어가지 않는다.
- **호출 경로:**
  - 저장 쪽 네 호출(다시 읽기 · create · change · delete)은 모두 `KosNotices._writer().call(token, …)`(`emr/kos/notices.py:73-96`)을 거친다. 이것은 `KosStaffWriter.call`이며, `Authorization: Bearer <그 직원 토큰>`과 브라우저 헤더를 붙이고 재시도하지 않는다.
  - 시스템 계정(`client.internal`)은 동기화용 `fetch_notices`에서만 쓴다.
- **401 처리:** 토큰이 거절되면(401) `StaffTokenRejected` → `end_session_on_kos_401` → commit → 401 `session_expired`.
- **시험이 확인하는 것:**
  - `kos.tokens == {"nurse-kos-token"}`(`test_reservation_notice.py:186`)
  - CSRF로 막히면 KOS 호출이 0이고 토큰도 0
  - `test_kos_notices.py`는 동기화가 시스템 계정이고 저장은 직원 토큰 · 헤더 · 경로 · 본문임을 본다

## ③ 저장 성공 뒤 DAY notice + external_ref 맞춤 · 다시 읽기 실패 → **PASS**

- **성공:** 쓰기 뒤 같은 직원 토큰으로 그 날짜를 다시 읽는다(`:246`). `apply_notices`(`emr/sync_notices.py`)가 그 날짜 창을 통째로 맞춘다.
  - `Refs.link`(`ON CONFLICT … DO UPDATE`)로 `external_ref(entity_type='notice')`를 맞춘다.
  - notice는 upsert하고, 창 안에서 이번 목록에 없는 연결 공지는 `mark_absent`(`deleted_at`)한다.
  - 그 다음 `notice_save`를 기록하고 commit한다. 응답은 다시 읽은 첫 공지와 그 DAY id(`_day_id`)다.
- **다시 읽기만 실패 (R62 ⑤):** `_saved_view`(`:282-295`)가 「저장 전 목록 + 방금 한 쓰기」로 사본과 응답을 만든다.
  - create의 새 id를 모르면 사본은 건드리지 않고, 방금 쓴 글만 응답한다(`notice_id=None`).
  - `StaffTokenRejected`는 `EmrError`의 하위 클래스(`emr/base.py:231`)라서, 다시 읽기 중 401이 나도 「다시 읽기 실패」로 처리된다. 500으로 새지 않는다.
- **시험:** `test_R62_다시_읽기만_실패하면_방금_저장한_글로_응답`

## ④ 공지 동기화가 일정 · 날짜 회차를 오류로 만들지 않는가 (R62 ①) · 통째 맞춤 → **PASS (+ WARN 2)**

- **10초 회차:** `services/emr_sync.py` `run_schedules`가 `fetch_notices_isolated`(모든 예외 → None + 경고 로그 `emr notices skipped: <이름>`)를 **transaction 밖**에서 부른다. None이면 공지는 맞추지 않고 이전 사본을 그대로 둔다.
- **날짜 회차:** `services/emr_date_sync.py` `run_reservation_date`도 같은 방식이다. 읽기는 transaction 밖, None이면 `skipped.notice.unavailable`.
- **통째 맞춤:** `apply_notices`가 `[start, end)` 창 기준으로 넣기 · 고치기 · 없앰 표시를 한다. 연결 없는 옛 행은 건드리지 않는다.
- **시험:**
  - `test_그_날짜_창을_통째로_맞춘다`
  - `test_10초_일정_회차가_오늘_공지를_맞추고_실패해도_회차는_done`: 실패해도 `status == "done"`, 사본 유지, 경고 로그 확인

### W3-1 공지 「반영」은 일정 transaction 안에 있다: 읽기만 따로 떼어 냈다

- **현상:** `apply_notices`는 10초 회차의 일정 transaction 안(`emr_sync.py` `run_schedules` · `apply_schedules` 바로 뒤)에서 돈다. 날짜 회차에서는 C1 단일 transaction 안이다.
- **영향:** KOS 읽기 실패는 격리된다. 하지만 공지 반영 중 DB 오류(예: 저장 요청과 같은 notice · external_ref 행을 두고 잠금 시간 초과나 교착)가 나면 그 회차의 일정 반영까지 롤백되고 회차가 오류가 된다.
- **R62 ① 문장과 비교:** 「일정 회차를 오류로 만들지 않음 · 공지는 C1 묶음에서 뺌」을 글자 그대로 읽으면 반영도 따로(savepoint 또는 별도 transaction) 해야 한다.
- **판단:** 같은 순서(link → upsert → mark_absent)로 잠그기 때문에 교착 가능성은 낮다. 그래서 WARN이다.

### W3-2 날짜 회차의 공지 경로는 시험이 없다

`test_date_sync*.py`에는 notice가 한 번도 나오지 않는다. 다음 두 가지는 날짜 회차에서 시험되지 않는다.
- 날짜 회차가 그 날짜 공지를 맞추는 것
- 공지 읽기가 실패해도 C1 반영이 `done`인 것(`skipped.notice.unavailable`)

10초 회차 쪽만 시험이 있다.

## ⑤ migration 0020 · heads 하나 → **PASS**

- **0019** (`purchase(visit_id)` · `visit_task(visit_id)` 부분 인덱스 · 검수 2 W2-3 반영):
  - down_revision = 0018
  - 모델 `__table_args__`에도 같은 인덱스가 있다
  - up/down/up 시험 있음
- **0020** (`reservation.notice` edit 데이터 행):
  - down_revision = 0019
  - 0017과 같은 방식이다: 살아 있는 모든 직무에 넣고 `ON CONFLICT DO NOTHING`, downgrade는 그 키 행만 지운다
  - revision 이름은 alembic_version 칸 32자 안이다(시험)
- **heads:**
  - 체인은 0017 → 0018 → 0019 → 0020 한 줄이다. 각 revision을 down_revision으로 가진 파일이 하나씩뿐이다.
  - `test_alembic.HEAD = "0020_notice_permission"`이고 통과했다.

## ⑥ 화면: 편집 중 폴링 보호 · 실패 줄 · 문구 → **PASS (+ WARN 1)**

- **편집 중 폴링 보호:**
  - `resBeforeSwap`에서 폴링 요청이고 공지 폼이 열려 있으면 `resNoticeKeep`에 그 칸 노드와 커서를 잡아 둔다.
  - `resInit`이 새 칸을 옛 칸 노드로 `replaceWith` → `htmx.process` → 포커스 · 선택 범위를 되살린다.
  - 그래서 쓴 글, 커서, 떠 있는 저장 요청이 그대로 남는다.
  - 날짜를 옮기면 편집을 닫고 버린다(`:1800`).
- **실패 줄:**
  - 저장 응답이 status 0 또는 ≥ 400이면 `shouldSwap=false`이고, `afterRequest`에서 「저장하지 못했습니다」와 「다시 시도」를 보인다.
  - 「다시 시도」는 같은 폼을 `htmx.trigger(form,"submit")`로 다시 보낸다. 쓴 글은 그대로다.
  - 2,000자를 넘으면 [저장]이 비활성이 되고 요청도 막는다.
- **성공:** `#reservation-notice`를 outerHTML로 바꾸면서 편집이 닫힌다. 그리고 `HX-Trigger` `day:notice-saved`가 「공지를 저장했어요」 토스트를 띄운다.
- **문구 (R58 · R57 · R56만):**
  - 수정하기 · 취소 · 저장 · 저장하지 못했습니다 · 다시 시도 · 공지를 저장했어요
  - 상담사 · 담당의 · 미정
  - `test_screen_copy`에 근거 행이 있다. 「취소」 · 「다시 시도」 · 「공지」는 이전부터 있던 행이다.
  - 시안이나 결정 밖 글자는 없다.
- **E4 (R56):** 원내 현황 카드는 상담 대기부터 「상담」 줄을 늘 그리고, 이름이 없으면 「미정」이다(`reservations_parts.html` `inhouse_card`).
- **참고:** 검수 2의 W2-1 · W2-2(원내 목록 세로 스크롤, 칩 줄 가로 위치)는 `resInY` · `resCatsX`로 반영됐다.

### W3-3 저장 직후 한 폴링 동안 옛 공지가 다시 보일 수 있다

- **경합 순서:** 10초 회차가 저장 **전**에 KOS를 읽고(transaction 밖), 저장 요청이 commit한 **뒤**에 반영하는 경우다.
- **결과:**
  - 회차가 옛 목록으로 그 날짜를 통째로 맞춘다.
  - 방금 만든 공지는 `mark_absent`로 `deleted_at`이 찍히고, 고친 글은 옛 글로 되돌아간다.
  - 다음 회차(≤ 10초)가 다시 바로잡는다.
- **직원에게 보이는 것:** 「공지를 저장했어요」가 뜬 뒤 다음 폴링에서 옛 글이 잠깐 보인다.
- **판단:** 확률은 낮지만 막는 장치(회차 시작 시각과 저장 시각을 비교하는 것 등)도 없고 시험도 없다.

## ⑦ E5 담당의 판정이 시술 현황판과 같은가 · 쿼리 수 → **PASS (+ WARN 1)**

- **같은 재료:**
  - `queries/board.py`의 `load_world` 안 작업 · 집도의 / 호출 · 호출 작업 · 수락 / 직원 읽기를 `load_tasks` · `load_calls` · `load_staff`로 **그대로 떼어 냈다**(본문 동일).
  - 판(`load_world`)과 예약 표(`queries/reservation_staff.doctor_world`)가 같은 함수를 쓴다.
  - 판 시험 218건이 통과해서 회귀는 없다.
- **같은 판정:** `services/reservations.py`가 `BoardRules(data.staff_world).task_doctor`를 넘긴다. 판과 같은 메서드다.
  - 유효 호출이 있으면 그 수락 원장(수락 전이면 None)이다.
  - 없으면 KOS 집도의 중 원장 목록에 있는 직원이다.
  - `world.now`는 쓰지 않으므로 `now=start`로 넘겨도 결과가 같다.
- **고르는 줄:** `doctor_names`는 시술(`TaskKind.PROCEDURE`) 줄을 시작 순(시작 안 한 줄은 뒤 → sort_order → id)으로 놓고 **담당의가 정해진 첫 줄**을 고른다.
  - R57 「여러 줄이면 시작 순 첫 줄」을 「첫 줄에 담당의가 없으면 다음 줄」로 읽은 것이다.
  - 첫 줄이 미정이고 둘째 줄에 원장이 있으면, 「미정」이 아니라 둘째 줄 원장이 보인다.
  - 시험 `test_담당의는_시술_현황판_판정_그대로_시작_순_첫_줄`이 이 동작을 고정한다.
  - 해석 차이일 뿐이라 FAIL이 아니다. 사용자 확인이 필요하면 코디가 판단한다.
- **상담사:** 상담 기록 첫 상담사(시작 순) → 없으면 일정 상담 정보. 원내 현황과 같은 함수(`counselor_name`)다. 오늘을 볼 때는 표가 읽은 방문 행과 상담사를 원내 현황이 그대로 쓴다(검수 2 W2-4 반영).
- **쿼리 수:**
  - 방문 수와 상관없이 고정이다. `test_쿼리_수는_방문_수와_상관없다`가 `board_view` 전체를 13으로 단언한다: 표 6 + 상담사 1 + 판 세계 4 + 원내 1 + 공지 권한 1.
  - 호출이 있으면 +2다.

### W3-4 폴링 한 번의 쿼리가 늘었다: 최악 약 21회

- **최악 경우:** 다른 날짜를 보고, 오늘 원내 방문이 있고, 호출도 있을 때다. 표 6 + 담당자 5 ~ 7 + 원내 6 + 권한 1 ≈ 19 ~ 21회.
- **판 세계 직원 읽기:** `load_staff`는 병원 직원 전체를 매 폴링 읽는다.
- **시험:** 13은 단언되지만, 「원내 방문 있음 + 호출 있음」 조합의 상한은 시험이 없다.
- **판단:** 모두 인덱스 경로라(0019 포함) 당장 문제는 아니다. 데스크 PC 수 × 6회/분으로 쌓이는 비용이라 적어 둔다.

## ⑧ 업체 경계 · 계층 규칙 → **PASS**

- **업체 경계:**
  - KOS 경로 · 본문 · 헤더는 `emr/kos/notices.py` · `mapper_notice.py` 안에만 있다.
  - 업무 코드는 `EmrAdapter`의 `fetch_notices` · `staff_notices` · `create_notice` · `change_notice` · `delete_notice`와 `NormalizedNoticeData`만 안다.
  - 기본 구현은 「지원 안 함」이다: 읽기는 None, 쓰기는 `WriteNotSupportedError`. 조용히 건너뛰지 않는다.
  - `notices.py`는 `staff_client` · `client`를 import하지 않고 Protocol로 받는다.
- **계층:**
  - router는 HTTP만 다룬다(폼 파싱 · 응답 · 헤더).
  - service가 transaction과 KOS 호출 순서를 가진다. 외부 호출 중에는 DB 쓰기를 기다리지 않고, 쓰기 뒤에 반영 · commit한다.
  - policies(`reservation_staff`)는 값과 Callable만 받는다.
  - queries는 묶음 조회만 한다.
  - `tests/architecture`가 통과했다.
- **CSP:** 템플릿에 `<script>`와 `style=`이 없다. 토스트는 `<template>`으로 복제한다.
- **CSS:** 원천 app.css에만 썼고, 빌드 재현이 일치하고 Stylelint가 0이다.

## 그 밖 (참고 · FAIL 아님)

- **mapper 실패 행:** 공지 mapper가 실패한 행은 `map_all`이 빼고, 통째 맞춤에서 그 공지의 DAY 사본이 `deleted_at` 처리된다. 「외부 응답에 없는 값을 추정하지 않는다」에는 맞는다. 다만 id가 빠진 행 하나 때문에 공지가 사라져 보일 수 있다.
- **저장 응답의 `editable`:** 늘 `True`다. 날짜와 권한 검사를 통과한 뒤에만 오는 응답이라 맞다.

## 직원이 실제 사용에서 만날 자리

1. **저장 직후 옛 글이 잠깐 보임 (W3-3):** 「공지를 저장했어요」 뒤 다음 폴링에서 옛 공지가 잠깐 보였다가 10초 안에 돌아올 수 있다. 드물다.
2. **시술 줄이 여럿인 고객 (⑦):** 첫 시술 줄이 아직 미정이어도, 다른 줄에 원장이 있으면 카드에 그 원장이 「담당의 ○○○」로 보인다.
3. **편집 중 다른 직원이 같은 공지를 고침:** 편집 칸은 덮이지 않는다(R58). 저장하면 대상 공지를 KOS에서 다시 읽은 뒤 내 글로 덮는다(마지막 저장이 이김). 경고는 없다(결정 범위).
4. **편집 중 자정이 지남:** 그 날짜가 지난 날이 되어 저장이 409이고 「저장하지 못했습니다」가 뜬다. 「다시 시도」를 눌러도 계속 실패한다.
5. **KOS 토큰이 만료됨:** 저장을 누르면 로그인 화면으로 간다(401 · 세션 종료). 쓰던 글은 사라진다.
