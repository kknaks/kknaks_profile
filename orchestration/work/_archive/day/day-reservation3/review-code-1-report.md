# 리뷰 리포트 — day-reservation3 / code 1차 (2026-11-26)

대상: `CENTURION_DAY/day-reservation3` 미커밋 변경(HEAD `a76496c4` 기준 `git diff HEAD` + 새 파일 25개). 대조: Delivery #297(A1 ~ A7 · Non-Goals) · SPEC-008(+ 006 ⑭ · 005 · 007 고침 6 · 000 ③) · `_RESUME.md` §2 11-26 뒷줄(①~⑥ — SPEC 보다 우선) · `be-1-report` · `be-probe-1-report` · `review-doc-1 ~ 4`.
리포 파일 수정 · 커밋 · stash 0 · 테스트 실행 0(결과는 코디 test.sh 3284 passed · be-1 2996 passed 인용).

> 범위 주의: `origin/dev` 가 HEAD 보다 한 커밋 앞섰다(`3543d8b2` #298 — 코드 안 스펙 인용 번호 바꾸기). `git diff origin/dev` 는 그 커밋을 거꾸로 보여 준다(예: `day.js` 「고침 6 → 고침 5」). 이 검수는 `git diff HEAD` 기준이다. → W10.

## 판정: FAIL — FAIL 3 · WARN 13

### FAIL

| # | 파일:줄 | 무엇이 | 근거 | 고칠 방향 | 몫 |
|---|---|---|---|---|---|
| F1 | `services/reservation_request_reads.py:362 · 370-383` → `templates/partials/reservations_request_window.html:17 · 72` → `static/day.js:2809-2810` | **실패 줄의 [다시 시도]가 실제 화면에서 늘 꺼진다.** `_failed()` 는 실패 여부와 상관없이 확인 대기 묶음의 `write_id` 를 돌려주고, `read_window` 가 그 값을 `pending_write_id` 로 싣는다. 창은 `data-day-rq-wait` 를 달고, `rqInit` 은 이 표시가 있으면 `[data-day-rq-lock]` 을 모두 끈다. [다시 시도] 버튼에 `data-day-rq-lock` 이 있어서 `action == "failed"` 일 때 늘 꺼진 채로 그려진다. `kos_failed` 뒤 `rqSettle → rqLoad` 로 다시 받아도 마찬가지다. 남는 길은 [KOS 등록 실패](접음)뿐이라, 실패하면 **이 스레드를 다시 보낼 방법이 없다.** 화면 테스트 `test_U5_기다림_실패_빈줄과_잠금`(`web/test_reservation_requests_screen.py:306-321`)은 `action="failed"` 를 `pending_write_id=None` 과 같이 넣는다. 서버는 이 조합을 만들지 않으니, 테스트가 초록이어도 실제 동작은 확인하지 않는다(조용히 통과하는 자리) | SPEC-008 U-5(실패 묶음 = [다시 시도] · [접음]) · N1 · 시안 `reqFail` | 실패 줄의 [다시 시도]에서 `data-day-rq-lock` 을 떼거나, `pending_write_id` 를 「보내는 중(실패 아님)」일 때만 싣는다. 테스트는 서버가 실제로 만드는 조합(`action="failed"` + `pending_write_id`)으로 고친다. JS 동작은 frontend 정형 검사 · e2e 로 한 번 본다 | FE(+BE 값 뜻) |
| F2 | `services/reservation_writes.py:345-366`(공용 `retry` 의 `reset` UPDATE) · `services/reservation_request_actions.py:427`(접음 = payload `folded` 만) | **접은 스레드 쓰기 행을 공용 다시 시도가 다시 보낸다**(M1 구멍이 다시 열림). 공용 `retry` 는 `failed[0]` 의 event 만 스레드 행인지 본다. 그런데 되살리는 UPDATE 는 `visit_id == target ∧ status = failed` 인 행을 **전부** pending 으로 돌린다. 예: [예약 수정](W4) · [예약 취소](W5)가 실패해 접혔다 → 같은 방문에서 직원이 예약 상세로 다른 쓰기를 했고 그것도 실패했다 → 공용 토스트 「다시 시도」(`/reservations/visits/{id}/retry`)를 누른다 → `failed[0]` 은 직원 쓰기라 409 를 피하고, **접힌 W4 · W5 까지 다시 나간다.** 접힌 W4 는 옛 시간 · 메모 · 유입을 덮어쓰고, 접힌 W5 는 KOS 예약을 취소해 버린다. 스레드 [다시 시도](`thread=True`)도 같은 UPDATE 를 써서, 같은 방문의 **앞서 접힌 스레드 묶음**과 관계없는 실패까지 같이 되살린다. 이 경로를 덮는 테스트가 없다(F3) | SPEC-008 §3 「웹 경로」 실패 접기(「어느 다시 시도 길로도 다시 보낼 수 없음」) · M1 · review-doc-4 「입구 전수」 #2 · #3 | `reset` 조건에 **그 event 의 행만**(`event_id = event.id`)을 넣는다. 공용 길이면 `payload.request_id` 가 있는 event 의 행은 빼고, 스레드 길이면 그 확인 대기 event 만 되살린다. 「접힌 행 + 다른 실패가 같은 방문」 infra 테스트를 단다 | BE |
| F3 | `tests/day/test_reservation_request_flow.py`(테스트 5개) · `tests/day/web/test_reservation_requests_screen.py`(전부 가짜 읽기 서비스) | **A3 · A6 완료 조건이 테스트로 덮이지 않았다.** `reservation_request_actions` 의 `press` · `retry` · `dismiss_failure` · `comment` · `withdraw_change`, 공용 retry 409 `request_thread_write`, `settle._expire`, 알림 `unread` 제외 · 목록 `transport` 거름을 부르는 테스트가 **0개**다(`git grep` — `request_thread_write` · `dismiss_failure` · `actions.press` · `RESERVATION_REQUEST` 를 쓰는 테스트 없음). Issue A3 가 콕 집은 이중 예약 길(F2 · N1 · M1 — 같이 누름 409 · 확인 대기 중 철회 / 자동 닫힘 / 새 버전 · [접음] 뒤 · 공용 다시 시도 409)은 순수 규칙 함수 테스트(`test_reservation_request_rules.py`)뿐이다. 행 잠금 · 접힘 표시 · 공용 retry 거름 같은 서비스 경로는 어디서도 돌지 않는다. 위 F2 가 그래서 드러나지 않았다. ext 도 HTTP 끝-끝이 없다(`X-Day-Client` 400 · 한도 키 `day:ext:key:{hospital}` · `Idempotency-Key` 헤더 빠짐 400) | Issue #297 A3 · A6 · AGENTS.md 「테스트」(DB 가 보장하는 것 · API 끝-끝 몇 개) · be-1 이슈 5(「웹 동작 테스트는 FE 몫이라 안 씀」 — 그 사이가 비었다) | 서비스 infra 테스트를 단다. ① 생성 · 같이 누름 409 ② W3 확인 · 뒤 실패 → `visit_id` 연결 · 확인 대기 유지 · 철회 409 · 자동 닫힘 건너뜀 · E2 `change` 종류 그대로 ③ 접음 → 공용 두 길 409 · 스레드 retry 409 · `folded` 닫힘 ④ 공용 retry 409 `request_thread_write` ⑤ 알림 앱 목록 · `unread` 빠짐 · 웹 목록 들어감. ext 는 `test_ext_contract` 처럼 TestClient 로 E1 · E2 를 한 줄씩 | BE |

### WARN

| # | 파일:줄 | 무엇이 | 근거 | 고칠 방향 | 몫 |
|---|---|---|---|---|---|
| W1 | `services/reservation_request_ext.py:386-401` · `policies/reservation_request.py:74-79` | **OQ-Q15 에 확인 대기 틈이 있다.** `customer_changed` 는 `thread.visit_id is not None` 일 때만 본다. [예약 생성]이 W3 확인을 기다리는 동안(`visit_id` 없음 · `pending`)에 **다른 고객의 `change`** 가 오면 400 이 아니다. 종류는 `change` 그대로 기록되고, `thread.customer_id` 는 다른 고객으로 바뀐다(:400-401). 그 뒤 W3 가 확인되면 `_link_visit` 이 고객을 원래대로 되돌리고, 답할 버전 = 다른 고객의 `change` → [예약 수정] = W4 는 고객을 바꾸지 않는다. 결국 고객 바뀜이 **조용히 빠진다** | `_RESUME` §2 ③(OQ-Q15 = 400 `customer_changed`) · SPEC-008 「확인 대기」 = 「예약 있음」으로 봄 | 판정을 `booked(state)`(= `visit_live ∨ pending`)로 넓힌다. 확인 대기 중에는 `thread.customer_id` 를 덮지 않는다 | BE |
| W2 | `services/reservation_request_ext.py:475-476` · `services/reservation_request_settle.py:125`(`touch(thread, now)`) · `services/emr_sync.py:307` | **E4 `updated_since` 가 바뀜을 놓칠 수 있다.** `updatedAt` 은 앱 시계 `now`(동기화 회차 시작 시각 · `onupdate` 면 트랜잭션 시작 시각)로 쓰인다. 그런데 커밋은 KOS 다시 읽기 뒤라 몇 초 늦다. 그 사이 링키가 다른 스레드의 더 늦은 `updatedAt` 을 받아 기준을 앞으로 옮기면, **`reservation_applied`(확정) 같은 바뀜은 앞 시각으로 커밋돼 영영 안 보인다** → 링키가 고객에게 확정 알림을 못 보낸다 | SPEC-008 E4(「그 뒤 바뀐 것만」 · Q13 「빠짐 · 겹침 없음」) · RQ36(링키는 E4 · E5 로 확정을 본다) | 링키 쪽 안내(겹쳐 읽기 — `updated_since` 를 몇 분 앞으로)를 계약에 적거나, 커밋 순서를 따르는 값(예: 전역 seq)으로 바꾼다. 적어도 OQ 로 남긴다 | BE · 기획 |
| W3 | `services/reservation_request_actions.py:256-265` → `services/reservation_book.py:117-126`(`_lookup_body`) | **이메일만 있는 초진의 W1 은 이름만 보낸다.** 사용자 결정 ①로 생년월일이 선택이 되면서, 이메일 하나로 들어오는 고객은 KOS `find-duplicated-visitor` 에 `{name}` 만 간다. KOS 가 이름만으로 무엇을 찾는지는 실물 확인이 없다(be-probe-1 은 연락처 · 생년월일 있는 본문만 봄). 같은 이름이 있으면 매번 409 `customer_ambiguous`(생성 막힘)일 수 있다 | `_RESUME` §2 ①(구분 값 = 연락처 · SNS · 이메일 · 생년월일 중 하나) · SPEC-008 Rule 2 · A4(실물 확인) | e2e(A7) 때 이메일만 · SNS 만 있는 초진을 한 번씩 본다. 이름만이면 `email` 을 W1 본문에 싣는 것이 KOS 에서 되는지 확인 | BE(실물) |
| W4 | `services/reservation_request_actions.py:348-351` | **[예약 수정]에서 상담사를 비우면 KOS 에 가지 않는다**(`counselor is not None` 일 때만 W18). 링키가 `counselorStaffId: null` 로 고쳐 보내면, 버전 카드는 「없음」인데 KOS 예약 「당일 지정 상담사」는 그대로 남는다. 오류도 없다. be-1 이슈 4 가 알렸지만 SPEC 에 없는 동작이다 | SPEC-008 KOS 쓰기 표(「상담사가 바뀌면 W18」) · 「외부 응답에 없는 값을 … 조용히 건너뛰지 않는다」(AGENTS 외부 CRM) | KOS 「없음」 쓰기가 되는지 실물 확인 뒤 보내거나, 안 되면 SPEC · 화면에 「상담사 비우기 = 반영 안 됨」을 OQ 로 올린다 | BE · 기획 |
| W5 | `services/reservation_request_actions.py:511-512`(커밋 뒤 SSE) · `routers/reservation_request_actions.py:188` · `static/day.js` `rqSseMessage` · `rqSnapshot` | **댓글을 보낸 뒤 입력 칸에 보낸 글이 다시 차오를 수 있다.** 서버는 커밋 직후 SSE `reservation_request` 를 쏘고, 그다음에 응답을 그린다. SSE 가 먼저 오면 `rqLoad` 가 그때 입력 칸 글을 떠 둔다(`rqSnapshot` 은 `rqSent` 를 보지 않음). POST 응답이 입력부를 비운 **뒤** 창 GET 응답이 와서, 떠 둔 글을 되살린다 → 직원이 같은 글을 두 번 보내기 쉽다(순서는 실물 확인 필요 · PLAUSIBLE) | SPEC-008 U-1(입력 중 글 유지) · U-9 | `rqSent` 가 켜져 있으면 떠 두지 않는다. 또는 그 브라우저가 쓴 글의 SSE 는 무시한다 | FE |
| W6 | `routers/api/ext.py:74-78 · 104-107` | **「병원당 키 하나」를 강제하지 않는다.** env 에 같은 병원 줄이 둘 남아 있어도(옛 링키 · 차티 키에서 `partner` 만 지운 경우) 503 없이 둘 다 열리고, 한도만 하나로 합쳐진다. 배포 때 env 를 덜 바꾼 것이 조용히 통과한다 | SPEC-008 「ext 키 = 병원당 하나」 · OQ-Q12(어느 키를 남길지) · taewoo 확인 ④ | `grants()` 에서 `hospital_id` 가 겹치면 503 `ext_unavailable`(설정 오류)로 막거나, 적어도 경고 로그를 남긴다 | BE |
| W7 | `schemas/notification_responses.py:23-31` | 앱 응답 모양이 바뀐다. `NotificationTarget` 에 기본값 `""` 칸 `requestId` · `date` 가 생겼고, 라우터에 `response_model_exclude_unset` 이 없다(`routers/api/notifications.py:58`). 그래서 **앱 알림 목록의 모든 `target` 에 `requestId:""` · `date:""` 가 붙는다.** docstring(「없는 칸은 응답에 없음」)과도 다르다 | AGENTS.md 「API 경로 · 오류 계약 = 외부 계약」 · RQ40(앱엔 이 종류 없음) | 웹 전용 칸이면 exclude_unset 을 달거나 `None` 기본 + 빼기. 앱 계약 테스트(OpenAPI)에 칸이 늘었음을 남긴다 | BE |
| W8 | `services/reservation_request_reads.py:165`(`read_list` 안 `threads.state` 스레드마다) · `routers/reservations.py` `reservations_page` 가 늘 부름 | 목록에서 스레드마다 `visit` 조회가 하나씩 더 나간다(N+1). 예약 현황 전체 · 조각을 다시 그릴 때마다 돈다. query-count 테스트가 없다 | AGENTS.md 「백엔드 안전 기준」(N+1 위험 경로 = query-count 테스트) | `visit_id` 들을 한 번에 읽어 「예약 있음」을 셈하고, query-count 테스트를 단다 | BE |
| W9 | `services/reservation_request_actions.py:113 · 258-261` | [예약 생성] 초진은 **스레드 행 잠금을 쥔 채 KOS W1 을 부른다**(최대 `KOS_READ_SECONDS` 8s). 그동안 같은 스레드의 ext E2 · E6(`load(lock=True)`)이 막히고, ext 는 `lock_hospital` 까지 쥐고 있어서 **그 병원 ext 쓰기 전체가 줄을 선다** | AGENTS.md 「async 경로 … timeout · 동시성 상한」 · backend-reliability | W1 을 잠금 전에 미리 부르고, 잠금 안에서는 판정만 다시 한다. 또는 이 대기를 알고 받아들인다고 적는다 | BE |
| W10 | 리포 전체 | `origin/dev` 에 #298(코드 안 SPEC-007 「고침 n」 번호 바꾸기)이 들어왔고, 이 변경과 **10개 파일이 겹친다**(`error_codes.py` · `errors.py` · `reservations*.py` · `board_events.py` · `day.css` · `day.js` · `app.css` · `test_screen_copy.py` · `test_reservation_detail_screen.py`). #298 은 옛 「고침 5」를 「고침 6」으로 옮겼다. 그래서 이 작업이 쓰는 「SPEC-007 고침 6」(예약 요청)과 이름이 겹친다 | Issue 「구현 · 검증 상세」 · AGENTS 작업 규칙(작업 전 branch 상태) | PR 전에 `origin/dev` 위로 rebase 하고 빌드 CSS 를 다시 만든다. 이 작업의 SPEC-007 인용 번호는 mediness #968 머지 뒤 번호로 맞춘다 | 코디 |
| W11 | `policies/reservation_request.py:143-168`(`action`) · `services/reservation_request_settle.py:145-146`(`_expire` 가 `last.start_at` 을 봄) | **취소 버전이 「요청됨」 목록에 영영 남을 수 있다.** `cancel` 버전이 기록된 뒤(예약 있음) 그 예약이 예약 현황에서 평소대로 취소되면(RQ2 — 스레드는 따라가지 않음), 버튼은 계속 [예약 취소]이고 누를 때마다 409 `visit_stage_changed` 다. 취소 버전은 `start_at` 이 없어 자동 닫힘도 안 된다. 링키가 철회해야만 빠진다 | SPEC-008 U-5 · 케이스(웹) 「visit_stage_changed — 글로 조율」 · Rule 5 | 「예약 없음 ∧ 답할 버전 `cancel`」이면 빈 줄(또는 `folded` 와 같게 닫기)로 할지 코디가 정한다. 적어도 케이스 표에 한 줄 | BE · 기획 |
| W12 | `templates/partials/reservations_request_parts.html:10 · 16` | 한 화면에 같은 상태가 두 글자로 나온다. 3열 변경 요청 배지는 「답변 대기」(SPEC 임시 목록)이고, 1열 버튼 줄은 「답변 대기중」(사용자 11-26)이다. 사용자 문구 「변경 요청 대기 = 답변 대기중」이 어느 자리를 말했는지 갈리지 않았다 | `_RESUME` §2 ④ · SPEC-008 「임시 글자 목록」 | 사용자에게 한 줄 확인 — 배지도 「답변 대기중」인지. 짓지 않고 묻는다 | 코디 |
| W13 | `services/reservation_request_ext.py:376-384` | E2 는 `_check`(400 · 404 `customer_not_found`)를 스레드를 찾기(404 `request_not_found`) **전에** 돈다. 없는 스레드에 틀린 `customerId` 를 보내면 `customer_not_found` 가 나간다. 또 `Idempotency-Key` 가 표마다 따로라(버전 표 · 댓글 표), 링키가 E1 과 E6 에 같은 키를 쓰면 충돌로 잡히지 않는다 | SPEC-008 E2 검사 순서 · 「같은 키 + 다른 본문 = 409」(범위 = 병원) | 스레드 찾기를 앞으로 올린다. 키 범위는 「표마다」라고 계약에 적거나 한 표로 모은다 | BE |

## 축별 대조

### 1. 이중 예약 · 상태 구멍 (코드 경로 하나씩)

| 길 | 코드 | 판정 |
|---|---|---|
| 확인 대기 유지(실패해도) | `pending_version_id` = `press` 때 채움(`actions.py:367`) · 비우는 곳 = `settle._settle_one`(모두 confirmed · :124) · `dismiss_failure`(:428)뿐 | ✓ |
| 확인 대기 중 E3 철회 | `withdraw_outcome` → `booked` = `visit_live ∨ pending` → 409 `request_already_applied` | ✓(규칙 테스트만) |
| 확인 대기 중 자동 닫힘 | `_expire` 가 `pending_version_id IS NULL` 만 봄 + `rules.expires` | ✓ |
| 확인 대기 중 E2 `change` · `cancel` | `recorded_kind` → `booked` 면 종류 그대로 | ✓ · 단 고객 바뀜 W1 |
| 생성 · 수정 · 취소 409 | `button_conflict`(본 버전 ≠ 답할 버전 · pending · waiting · 지금 버튼 아님 · 「예약 있음」 생성) | ✓ |
| 같이 누름 | `_thread(lock=True)` = `SELECT … FOR UPDATE` → 두 번째는 pending 을 보고 409 | ✓(코드) · 테스트 0(F3) |
| `visit_id` = W3 확인 때 | `settle._link_visit` — `creates == "visit"` 행이 CONFIRMED ∧ 사본 있음 → 연결(묶음 전체 확인 전이어도) | ✓ |
| `reservation_applied` = 묶음 마지막 확인 뒤 · Q19 | `_settle_one` 이 모두 CONFIRMED 일 때 댓글 + 최신 버전이 그 버전일 때만 상태 전이 | ✓ |
| 스레드 [다시 시도] | `pending` 아니면 409 · `write_event`(접힌 것 뺌) → `reservation_writes.retry(thread=True)` | 서버 ✓ · **화면에서 못 누름(F1)** · 되살리는 범위 넓음(F2) |
| [접음] | 실패 행 있음 ∧ 보내는 중 없음 → payload `folded` · pending 비움 · 예약 없음 ∧ `cancel` → `folded` 닫힘 | ✓ |
| 공용 retry 409 | `retry` 가 `failed[0]` event 의 `request_id` 만 봄 | **구멍(F2)** |
| 공용 토스트 「다시 시도」 → 창 | `kos_failed(…, request_id)` → `data-day-rq-open` | ✓(테스트 있음) |
| 생성 전 `change` → `new` · `cancel` 409 두 코드 | `recorded_kind` | ✓ |
| 접은 뒤 `change` → [예약 생성] · 예약 있음 ∧ `new` → 빈 줄(OQ-Q21) | `answer_kind` · `action` | ✓ |
| W2 · W3 시간 초과(V1 ⓐ — 사람이 고른다) | 막는 로직 없음 · 안내 글자 비움 | ✓(SPEC 대로) |
| be-probe ⑥ — 생성 묶음에 W18 없음 | 생성 = W3 에 `counselor` 바로 · W18 = 수정 때 상담사 바뀔 때만 | ✓ · 비우기는 W4 |

### 2. ext 키 병원당 하나

| 항목 | 코드 | 판정 |
|---|---|---|
| `PartnerGrant.partner` 제거 | `schemas/ext_common.py` | ✓ |
| `git grep partner` 전수 — 값을 쓰는 곳 | `ext_writes.Writer.partner`(= client 기록) · `ext_charty` 기록 · 로그 `ext_call partner=%s`(= client). `replay` · `submit_payment` 의 partner 거름 빠짐. 그 밖 `partner` 글자는 「연동처 쓰기」 이름(SPEC 표 마지막 줄 — 그대로) | ✓ |
| 한도 키 | `day:ext:key:{hospital}` 분당 60 | ✓ · 테스트 0(F3) |
| `_charty` 403 없어짐 | `Charty` 의존 삭제 · 계약 테스트 `403 not in` | ✓ |
| `X-Day-Client` 값 규칙 · 순서 | 401 → 429 → 400 | ✓ · HTTP 테스트 0 |
| outbox · payment 유일키 (`hospital_id`, `request_key`) | 모델 · migration · `test_constraints` | ✓ |
| migration 0031 중복 행 멈춤 | `_stop_on_duplicate_keys`(오프라인 SQL 모드만 건너뜀) · up/down 왕복 `test_alembic` | ✓ |
| 키 하나 강제 | 없음 | W6 |
| 테스트 11개 파일 | `test_ext_writes` · `test_room_move_chain` · `test_charty_*` 는 행의 `partner="charty"` 값만 남음(칸 null 가능이라 유효) | ✓ |

### 3. ext E1 ~ E8

| 항목 | 판정 |
|---|---|
| 본문 검증 — 이름 필수 · 구분 값 하나 이상(생년월일 선택 — ① 반영) · 길이 상한 · `phone` 정규식 · 통역 7개 · SNS 6개 · 모르는 키 400 · 버전 번호 보내면 400 | ✓(`schemas/ext_reservation_request.py`) |
| 목록 값(`groupId` · `funnelId` 닫힌 것 · 원장 = doctor 태그 · 상담사 = 목록) · 지난 시각 · 1000자 · `customerId` 404 | ✓(`_check`) · 순서 W13 |
| Idempotency 재생 / 충돌 | ✓(키 해시 · 경로 포함 digest · `lock_hospital`) · 표마다 따로 W13 |
| 버전 번호 = 서버 · 행 잠금 | ✓ |
| 판정 ② — 이름(대소문자 · 띄어쓰기) ∧ 온 구분 값 하나 ∧ 국적 양쪽 있을 때만 | ✓(`same_customers` · 테스트 있음) |
| `customer_changed`(③) | ✓ · 확인 대기 틈 W1 |
| E4 커서 · `updated_since` | ✓ · 놓침 W2 |
| E5 · E6 · E7 · E8 | ✓ |

### 4. KOS 쓰기

| 항목 | 판정 |
|---|---|
| `write_open` — reserve 최상위 `counselor{id,name}` 허용(나머지 BANNED 그대로) · W18 = 정확히 `{scheduleId, counselor}` | ✓(테스트 있음) |
| W4 한 본문 + `reservationMemo` · `funnel` 늘 · expect 메모 · 유입 | ✓ |
| W2 `email` | ✓ · 빈칸뿐인 이메일(`"  "`)도 그대로 실림(사소) |
| 메모 합치기 형식 · 순서 · 빈 줄 뺌 · 1000자 400(ext · 버튼 둘 다) | ✓ |
| 순서 묶음 · 담당자 = 누른 직원(`staff_ref(current.staff_id)`) | ✓ |
| 확인 = `reservation_met` `counselor` 키 | ✓ |
| 초진 W1 본문 | W3 |
| 상담사 비우기 | W4 |

### 5. 알림 · SSE

| 항목 | 판정 |
|---|---|
| 새 종류 · enum migration · `notification.reservation_request_id` | ✓ |
| 받는 사람 = 활성 · 비시스템 직원 ∧ 태그 admin · coordinator | ✓ |
| 만드는 때 = E1 · E2 · E6 · 재생은 안 만듦 · 병원 쪽 · 철회 · 자동 닫힘 · `reservation_applied` 는 안 만듦 | ✓ |
| `unread` 늘 뺌 · 목록 `transport != cookie` 면 뺌 · target `requestId` · `date` | ✓ · 테스트 0(F3) · 앱 응답 모양 W7 |
| `announce_unread` 커밋 뒤 · 웹은 `notification` 이벤트마다 목록을 다시 받음(수와 무관) → OS 알림 | ✓ |
| `day.js` 누르기 갈래 → `/reservations?request=&date=` · 열고 나면 주소에서 뺌 | ✓ |
| SSE `reservation_request` · `kos_failed` 뒤 신호 · 토스트 `request_id` | ✓ |

### 6. 화면

| 항목 | 판정 |
|---|---|
| 목록 · 창 1 · 2 · 3열 구조 = 시안 v15 · 배지 RQ43 · 빈 줄 높이 유지 | ✓(조각 테스트) |
| U-5 = 서버 `action` 그대로 | ✓ · 실패 줄 F1 |
| 문구 = SPEC 임시 목록 + 사용자 문구(「답변 대기중」 · [철회] · [KOS 등록 실패]) · 비움 = 판정 2명 이상 · 취소 `reason` 줄 이름 | ✓ · 「답변 대기」 / 「답변 대기중」 W12 · `aria-label` 「댓글」 · 「댓글 종류」 · 「닫기」는 보이지 않는 글자 |
| 인라인 스크립트 · `style=` · `on*=` | 0 |
| 손 CSS | `app.css` 원천 + `day.css` 빌드 — 재현 검사는 `check.sh` 전체에서(be-1 은 `--pure` 중간에서 멈춤) → 코디 `check.sh` 한 번 |

### 7. 권한 · 보안

| 항목 | 판정 |
|---|---|
| ext 병원 격리 — `threads.load(hospital)` · `customerId` 병원 확인 · 목록 값 병원 확인 | ✓ |
| 웹 병원 격리 — 창 · 2열 · 쓰기 · 댓글 철회(스레드 id 같이) | ✓ |
| 웹 권한 — 보기 `reservation` view · 쓰기 `reservation.detail` edit · CSRF(`writable_session`) | ✓ |
| 입력 이스케이프 — Jinja 자동 · JS `textContent` · `append(p.label)` | ✓ |
| `session.get(Customer, customer_ref_id)` 에 병원 조건 없음 | ext 받을 때 병원을 확인했으니 영향 없음(참고) |

### 8. 테스트

F3 · W8. 순수 규칙 · KOS 본문 · 조각은 잘 덮였다. 서비스 경로(잠금 · 접음 · 공용 retry · 자동 닫힘 · 알림 거름) · ext HTTP 는 비었다. 조용히 통과하는 자리 = F1 의 화면 테스트(서버가 만들지 않는 값 조합).

## 직원이 실물에서 만날 자리

1. 쓰기가 실패하면 「보내지 못했습니다」 옆 **[다시 시도]가 꺼져 있다** — [KOS 등록 실패]만 눌린다(F1).
2. 스레드 쓰기를 접은 뒤 그 예약을 예약 상세에서 손보다 실패해 「다시 시도」를 누르면, **접었던 수정 · 취소가 KOS 에 나간다**(F2).
3. 댓글을 보내고 나면 입력 칸에 **방금 보낸 글이 다시 들어와 있을 수 있다**(W5).
4. 링키가 상담사를 비워 고쳐 보내도 KOS 예약의 「당일 지정 상담사」는 남는다(W4).
5. 이메일만 있는 초진은 [예약 생성]이 「고객 확인 필요」로 막힐 수 있다(W3 — 실물 확인 전).
6. 링키 취소 요청을 처리하기 전에 데스크가 예약 현황에서 먼저 취소하면, 그 카드가 「요청됨」 목록에 남는다. [예약 취소]는 누를 때마다 거절되고, 링키가 철회해야 빠진다(W11).
7. 같은 상태가 1열 「답변 대기중」 · 3열 배지 「답변 대기」로 다르게 보인다(W12).
8. 링키가 E4 목록만 보고 확정을 놓치면 고객은 확정 알림을 못 받는다. 병원 화면은 「확정」이다(W2).
9. 초진 [예약 생성]을 누른 몇 초 동안(KOS 같은 고객 찾기) 그 병원으로 오는 링키 요청 · 댓글이 잠깐 기다린다(W9).

## 참고(기존 부채 · 무관)

- 공용 `retry` 가 「방문의 실패 행 전부」를 되살리는 것 자체는 SPEC-007 D22(멈춘 뒤 쓰기 포함)의 기존 동작이다. 문제는 스레드 행 · 접힌 행이 그 안에 섞인다는 점이다(F2).
- `reservation_book._lookup_body` 를 모듈 밖에서 부른다(`actions.py:260` — 밑줄 이름). 구조 규칙 위반은 아니다.
- 화면 조각 GET 은 `HX-Request` 분기 없이 늘 조각을 돌려준다. 예약 현황 기존 조각 경로와 같은 방식이다.
