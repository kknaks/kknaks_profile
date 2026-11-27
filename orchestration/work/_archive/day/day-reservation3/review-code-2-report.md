# 리뷰 리포트 — day-reservation3 / code 2차 (2026-11-26)

대상: 워크트리(origin/dev `3543d8b2` 위 · 미커밋) — 고침 1(`be-fix-1-report.md` · `fe-fix-1-instructions.md`) 뒤. 대조: `review-code-1-report.md` · 코디 기본값(다시 열지 않음). 리포 수정 · 커밋 · stash · 테스트 실행 0(코디 test.sh 3292 passed · check --pure 통과 인용). W3 · W4 · W10 은 코디 몫이라 제외했다.

## 판정: WARN — FAIL 0 · WARN 5 (1차 F1 ~ F3 닫힘)

### WARN (새로 생김 · 남음)

| # | 파일:줄 | 무엇이 | 근거 | 고칠 방향 | 몫 |
|---|---|---|---|---|---|
| N1 | `services/reservation_writes.py` `retry` — `thread_events = select(EventLog.id).where(EventLog.payload["request_id"].astext.is_not(None))` | 공용 다시 시도를 부를 때마다 **`event_log` 전체를 jsonb 로 훑는다**. 병원 조건 · `type` 조건 · 인덱스가 없다. 그리고 스레드 기록 행(`reservation_request_*` — `threads.record` 도 `request_id` 를 싣는다)까지 같이 걸린다. 동작은 맞지만, `event_log` 가 커질수록 토스트 「다시 시도」가 느려진다 | AGENTS.md 백엔드 안전 기준(조회 비용) · backend-reliability | `EventLog.hospital_id == current.hospital_id ∧ type IN (reservation.request_create · _update · _cancel)` 를 붙인다(`settle.ACTION_TYPES` 와 같은 목록) | BE |
| N2 | `services/reservation_request_actions.py:345`(`_look_first`) | W9 를 고치면서 초진 W1(KOS)을 **409 판정보다 먼저** 부르게 됐다. 그래서 ① 같이 누름 · 확인 대기 · 낡은 버전을 눌러도 KOS 를 한 번 부른 뒤에야 409 가 나온다 ② KOS 가 멈춰 있으면 409 가 아니라 503 `kos_unavailable` 이 나온다(검사 순서 400 → 404 → 409 가 503 에 밀림). 이중 예약은 생기지 않는다(잠금 안 판정 그대로) | SPEC-008 「웹 경로」 검사 순서 · W2(같이 누름 = 409 최신 창) | `_look_first` 안에서 잠그지 않은 값으로 `button_conflict` 를 먼저 보고, 걸리면 KOS 를 부르지 않는다(잠금 안에서 한 번 더 보는 것은 그대로) | BE |
| N3 | `templates/partials/reservations_request_thread.html:35` ← `services/reservation_request_settle.py` `_expire`(W11 — `author_staff_id` 없음) | W11 자동 취소 줄이 **「예약 취소됨 ·  · 12:00」** 으로 그려진다. 글쓴이가 빈칸이라 구분점이 두 번 붙는다 | SPEC-008 U-8 시스템 줄 `{동작} · {누른 직원} · {시각}` · 시안 | `it.author` 가 없으면 그 칸과 구분점을 빼고 그린다. 글자는 짓지 않는다 | FE |
| N4 | `policies/reservation_request.py:74-79` · `services/reservation_request_ext.py` `add_version` | W1 은 대부분 닫혔지만, **초진 [예약 생성]이 확인 대기일 때** 다른 사람이 아직 DAY 에 없는 고객으로 `change` 하면 통과한다. 이때 `thread.customer_id` 는 None, 판정된 고객도 None 이라 `None != None` 이 거짓이 된다. 기록은 `change`, 확인 뒤에는 [예약 수정]으로 가고 고객 바뀜은 빠진다. 드문 경우다(확인 대기 몇 초 사이 · 초진) | `_RESUME` §2 ③ OQ-Q15 | 확인 대기 중이고 스레드 고객이 비어 있으면, 그 확인 대기 버전의 판정 값(`Identity`)과 비교한다. 또는 이 틈을 알고 둔다고 리포트 · OQ 에 적는다 | BE · 코디 |
| N5 | `services/reservation_request_settle.py` `_expire`(W11 `cancel_done`) | W11 은 「예약 없음」을 `visit` 사본이 **취소됨 또는 지워짐(`deleted_at`)** 으로 본다. 그래서 동기화가 사본을 지운 경우(KOS 에서 지움 등)에도 시스템이 「예약 취소됨」 `reservation_applied` 를 남기고, 링키는 고객에게 취소를 알린다. 지금 정의(F1 · F2 「예약 있음」 하나)대로라 틀린 것은 아니다. 다만 **병원이 누르지 않은 취소 확정이 외부로 나가는** 새 길이다 | 코디 결정 W11 · RQ36(링키는 `reservation_applied` 로 고객 알림) | 동작은 그대로 둔다. e2e(A7) 때 「예약 현황에서 먼저 취소 → 10초 안에 취소됨」 한 번 확인. 사본 지움도 같게 볼지는 코디가 한 줄 정한다 | 코디 |

## 1차 지적 — 닫힘 확인

| # | 고친 자리 | 판정 |
|---|---|---|
| F1 | `reservation_request_reads.py:343`(실패면 `pending_write_id = None`) · `reservations_request_window.html:73`([다시 시도] = `data-day-rq-retry` · 잠금 표시 없음) · 화면 테스트 `test_U5_…:312-319`(실패 × `pending_write_id` None / `w-1` 둘 다) | 닫힘. 겹친 막음 — 서버가 id 를 비우고, 버튼에 잠금 표시도 없다. [다시 시도]를 두 번 누르면 두 번째는 409 `no_failed_write` → 창을 다시 받는다(안전) |
| F2 | `reservation_writes.py` `retry` — 공용 길 = 스레드 묶음 event 행을 찾지도 되살리지도 않음 · 그것뿐이면 409 `request_thread_write` / 스레드 길 = `event_id == event.id` 행만 | 닫힘. 되살리기 UPDATE 가 event(스레드) 또는 「스레드 아님」으로 좁혀졌다. 접힌 행은 스레드 길에서도 `write_event` 가 빼고 pending 이 없어 409. 성능은 N1 |
| F3 | 새 `tests/day/board/test_reservation_request_actions_flow.py`(infra 4) · `test_reservation_request_flow.py`(알림 · query-count) | 닫힘 — 아래 「새 테스트」 |
| W1 | `add_version` — `customer_changed(booked(state), …)` · 확인 대기 중 `customer_id` 안 덮음 | 대부분 닫힘 · 남은 틈 N4 |
| W2 | `ext_reservation_requests.py:88` E4 설명(5분 겹쳐 읽기 · `requestId` · `version` 으로 거름) | 닫힘(계약 안내) |
| W5 | `day.js:2667`(`rqSent` 면 글을 떠 두지 않음) | 닫힘. POST 가 먼저 와도(`rqSent` 꺼진 뒤 입력부가 이미 비어 있음) · SSE 가 먼저 와도 빈 글 |
| W6 | `ext.py` `grants()` — 같은 `hospital_id` 둘 = 503 + error 로그 · 계약 테스트 | 닫힘 |
| W7 | `notification_responses.py:23-31`(None 기본) · 알림 라우터는 원래 `response_model_exclude_unset=True`(`routers/api/notifications.py:51` · 이번 diff 없음) | 닫힘 — 앱 응답 모양 그대로 |
| W8 | `threads.states`(방문 한 번에) · query-count 테스트 `test_목록_조회는_…:323` | 닫힘. `settle._expire` 는 아직 스레드마다 `latest` 를 부른다(10초 회차 · 「요청됨」만 — 참고) |
| W9 | `_look_first`(잠금 전 W1 · 읽고 rollback · 버전 바뀌면 잠금 안에서 다시) | 닫힘 · 대신 N2 |
| W11 | `policies.cancel_done` · `settle._expire`(취소됨 + `reservation_applied` 취소) · `action` 의 「예약 없는 cancel = 버튼 없음」 · 테스트 | 닫힘 · 표시 N3 · 외부 영향 N5 |
| W12 | `reservations_request_parts.html:11 · 17` — 배지 · 버튼 줄 모두 「답변 대기중」 | 닫힘 |
| W13 | `add_version` 스레드 찾기를 `_check` 앞으로 · `Idempotency-Key` 설명 「표마다」 | 닫힘 |

## 지시 ② — 고치며 생긴 구멍: 서버 잠금 규칙

`pending_write_id` 를 화면에서 비워도 **서버 판정은 `pending_version_id` 를 본다**. 그래서 실패 묶음이 남은 동안 막는 것은 그대로다.

| 길 | 보는 값 | 실패 묶음 남은 동안 |
|---|---|---|
| [예약 생성] · [예약 수정] · [예약 취소] | `button_conflict` → `state.pending` | 409 `request_version_changed` ✓ |
| E3 철회 | `withdraw_outcome` → `booked`(pending 포함) | 409 `request_already_applied` ✓(infra 테스트) |
| 자동 닫힘 · W11 취소됨 | `_expire` 가 `pending_version_id IS NULL` 만 + `booked` | 건너뜀 ✓(infra — 시작 지나도 그대로) |
| E2 `change` · `cancel` | `recorded_kind` → `booked` | 종류 그대로 ✓(infra) |
| 화면 버튼 | `action` → `pending` 이면 `failed` 또는 빈 줄 | [다시 시도] · [KOS 등록 실패]만 ✓ |
| W11 ↔ [접음] | 접음 = `pending` 비움과 같은 트랜잭션에서 「예약 없음 ∧ cancel」 → `folded` 닫힘. 그다음 회차의 W11 은 「요청됨」만 보니 겹치지 않음 | ✓ |
| W11 ↔ 확인 | 같은 `settle` 안에서 `_settle_one` 이 먼저 visit 연결 · pending 비움 → `_expire` 는 「예약 있음」을 봄 | ✓ |

## 지시 ③ — 새 테스트가 실제 경로를 도나

| 테스트 | 도는 경로 | 손으로 만든 것 | 판정 |
|---|---|---|---|
| `test_생성_같이_누름_409` | `actions.press` 두 번(실제 PG 행 잠금) · 쓰기 큐 본문(`reservationMemo` 합친 글) | 없음 | 실제 ✓ |
| `test_W3_확인_뒤_실패_…_retry_범위` | `settle.settle` · `ext.withdraw` · `ext.add_version` · `reservation_writes.cancel`(직원 쓰기) · `actions.dismiss_failure` · `actions.retry` · 공용 `retry` 두 길 | KOS 확인 결과(visit 사본 · CONFIRMED · 뒤 행 FAILED) — 외부 경계라 괜찮음 | 실제 ✓ — 1차 F2 장면(접힌 행 + 같은 방문 직원 실패) 그대로 |
| `test_예약_없는_취소_요청은_취소됨과_반영_줄` | `ext.add_version` · `settle.settle` | 스레드 `visit_id` 를 UPDATE 로 연결 | 실제 ✓ |
| `test_ext_HTTP_E1_E2_한_줄씩` | `create_ext_app` TestClient — `X-Day-Client` 400 · `Idempotency-Key` 빠짐 400 · 구분 값 없음 400 · 202 · 한도 키 `day:ext:key:{hospital}` · `customer_changed` 400 | `grants` monkeypatch | 실제 ✓ |
| 화면 `test_U5_기다림_실패_빈줄과_잠금` | 실패 = `action="failed"` × `pending_write_id` None / 있음 | 「`action="create"` + `pending_write_id`」 조합은 서버가 만들지 않는다(보내는 중이면 `action=None`). JS 잠금(`rqQueued`) 쪽 표시를 본 것이라 계약을 덮어 가리지는 않음 | ✓(참고) |
| 알림 `test_E1_새_요청_재생_충돌_알림` | `notifications.listing` cookie / bearer · `unread` | 없음 | 실제 ✓ |

## 직원이 실물에서 만날 자리

1. 링키 취소 요청을 처리하기 전에 예약 현황에서 먼저 취소하면, 10초쯤 뒤 스레드가 저절로 「취소됨」이 된다. 3열 줄은 「예약 취소됨 ·  · 시각」(N3)이고, 링키는 고객에게 취소를 알린다(N5).
2. KOS 가 멈춘 동안 초진 [예약 생성]을 다시 누르면, 「이미 처리 중」(409)이 아니라 KOS 오류(503)가 뜬다(N2).
3. [다시 시도]를 빠르게 두 번 누르면 두 번째는 오류 토스트(글자 비움)가 뜨고 창이 다시 그려진다 — 해는 없다.

## 참고

- `settle._expire` 의 스레드마다 `latest` 조회(W8 과 같은 꼴 · 「요청됨」 스레드 수만큼 · 10초 회차).
- W3 · W4 · W10 = 코디 e2e · rebase 몫(이번 판정에서 뺌).
