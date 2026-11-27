# be-1 결과 보고 — SPEC-008 WP-0 ~ WP-2 (backend)

## 상태: done (커밋 · push 없음 — 워크트리에 변경만)

## 수행

- **WP-0 ① 실물 확인** — `be-probe-1-report.md`(같은 폴더). Q01 `reserve` 최상위 `counselor` **O**(KOS 화면 HAR `예약등록.har` 도 같은 칸) · Q02 W4 한 본문 + `reservationMemo` · `funnel` **O**(다른 칸 안 지워짐) · Q03 `create-visitor` `email` **O**. 시험 예약은 취소로 정리.
- **WP-0 ② migration** `20261126_0031_reservation_request.py` — 새 표 4 + enum 8 · `notification.reservation_request_id` · `notification_kind += reservation_request` · ext 3표 `partner` null · 유일키 (hospital_id, request_key) · **partner 만 다른 같은 키 행이 있으면 RuntimeError 로 멈춤**(offline SQL 모드는 건너뜀) · downgrade 왕복.
- **③ 모델** `models/reservation_request.py` · `enums/reservation_request.py` · identifiers 4.
- **④ ext 키 병원당 하나** — `PartnerGrant.partner` 제거 · 인증 의존 = `ExtCallerData(hospital_id, client)` · 한도 키 `day:ext:key:{hospital}` · `_charty` 403 없앰 · `X-Day-Client` 검증(400) · Writer/charty/audit = client(null 가능) · replay 에서 partner 거름 뺌.
- **WP-1 ext** `routers/api/ext_reservation_requests.py`(E1 ~ E8, `ext.create_ext_app` 이 붙임) · `services/reservation_request_ext.py` · `schemas/ext_reservation_request.py`.
- **WP-2 웹** `routers/reservation_request_actions.py`(create · update · cancel · retry · dismiss-failure · comments · withdraw — `routers/reservations.py` 에 include 한 줄) · `services/reservation_request_actions.py` · 확인 뒤 반영 + 자동 닫힘 `services/reservation_request_settle.py`(← `reservation_confirm.announce_confirmed` 맨 앞에서 같은 트랜잭션) · 공통 `services/reservation_request_threads.py` · 순수 규칙 `policies/reservation_request.py`.
- KOS 쓰기: `emr/kos/writes.py` W2 email · W3 counselor(write_open 허용) · W4 `with_memo_funnel` · 새 W18 `ReservationCounselorWriteData`(정확히 `{scheduleId, counselor}`) · `outbox_rules.reservation_met` `counselor`.
- 알림: `services/notifications.py` unread 늘 뺌 · 목록 transport(cookie 만) · target `requestId` · `date` · 받는 사람 = admin · coordinator 활성 직원 계정.
- SSE: `reservations_streams.py` `reservation_request`(본문 = 스레드 id) · `kos_failed` 에 `requestId` 있으면 뒤에 `reservation_request` 도 · 토스트 값 `request_id`.
- 공용 retry 두 길: `reservation_writes.retry` 가 스레드 행이면 409 `request_thread_write`(스레드 retry 만 `thread=True`).

## 사용자 결정 반영 (작업 중 받음)
- OQ-Q15: 예약 있는 스레드에 다른 고객 change → E2 400 `customer_changed`(「고객이 다르면 새 요청으로 보내 주세요」).
- RQ24 판정(마지막 결정 — 앞 「국적 더함」 대신): 요청 = 이름 + phone · sns · email · birthDate 중 하나 이상(birthDate 선택) · 판정 = 이름(대소문자 · 띄어쓰기 무시) ∧ 온 구분 값 하나라도 정확히 같음(이메일은 대소문자 · 앞뒤 공백 무시) ∧ 국적은 양쪽 다 있을 때만 같아야. OQ-Q20 닫음(새 조회 없음).

## frontend 가 쓸 읽기 서비스 (`services/reservation_request_reads.py`)
FE 라우터 docstring 의 dict 모양 그대로(dataclass 아님 — FE 가 먼저 정한 계약):
- `read_list(session, current, now) -> {count, items[{request_id, name, unread, kind, when, nationality, interpreter, partner_at}]}`
- `read_window(session, current, request_id, now) -> rq{request_id, status, closed_reason, answer{kind, version}|None, customer{…}, reservation{when, procedures, doctor, counselor, interpreter}, memo, action(create|update|cancel|waiting|failed|None), pending_write_id, can_write, can_change_request, day{…}, thread[…]}` — 열면 `hospital_seen_at` = 지금(ext updatedAt 은 안 바뀜 · 안 읽음이었을 때만 SSE)
- `read_day(session, current, request_id, day, now) -> {date, label, prev, next, today, req_hour, groups[{id,title}], rows[{hour, label, counts[], at}]}` — 10 ~ 22시
- thread 항목: version `{type, kind, number, latest, at, values{when, group, doctor, counselor, procedures, reason}, previous}` · 댓글 `{type, side, author, at, body, comment_id, state, proposals[{at, label}]}` · `{type:"reservation_applied", action, author, at}`
- `action` 은 editable 을 모름 — 화면이 `editable` 과 같이 본다.

## 웹 동작 응답 · 오류
- create/update/cancel/retry: 200 본문 없음 · `HX-Reswap: none` · `HX-Trigger day:res-queued{writeId, visitId, requestId, action(request_create|request_update|request_cancel), message}` · 확인 뒤 SSE `write_confirmed`(action 같음) + `reservation_request`.
- dismiss-failure · withdraw → 창 조각(`reservations_request_window.html`, editable=True) · comments → `reservations_request_thread.html`.
- 오류 = 공용 oob 토스트 + `X-Day-Error` + `HX-Reswap: none`(글자 비움): 400 `memo_too_long` · `invalid_request` · 409 `customer_ambiguous`(「고객 확인 필요」 댓글 남김) · `request_version_changed`(→ 화면이 창 다시 GET) · `reservation_past_date` · `visit_stage_changed` · `request_closed` · `change_request_waiting` · `no_failed_write`(retry/접음 대상 없음) · `conflict`(철회: waiting 아님) · `request_thread_write`(공용 retry) · 503 `kos_unavailable`.
- ext 코드: `request_past_start` · `memo_too_long` · `customer_not_found` · `request_not_found` · `request_not_applied` · `request_finished` · `request_already_applied` · `request_closed` · `customer_changed` · `idempotency_conflict` · `invalid_request`.

## 검증
- `scripts/test.sh --ignore=backend/tests/day/web backend/tests` → **2996 passed · 2 failed** → 그중 `test_enum_labels`(내 것 · 고침 · 다시 1 passed). 남은 1 = `architecture/test_screen_copy.py`(**FE 템플릿 문구 근거표** — 무관 · FE 몫).
- 새 테스트: `test_reservation_request_rules.py` · `emr/test_reservation_request_writes_plan.py`(DB 없음) · `test_reservation_request_flow.py` · `test_alembic` 0031 · `test_constraints` 새 유일 3(infra) — 모두 통과.
- `scripts/check.sh --pure`: 구조 · mypy strict 통과 · Taut 남은 1 = `routers/reservations.py` `open_request` Query 설명 없음(**FE 몫**) — 그래서 그 뒤 단계(ESLint 등)는 이번에 안 돎.
- ruff: 만진 파일 전부 통과.

## 이슈 · 코디가 볼 것
1. **allowed_paths 밖 1줄**: 루트 `taut.toml` `[tool.taut.enum].shared_modules` 에 `day.enums.reservation_request` 추가(없으면 Taut ENUM001 · 새 enum 파일을 쓰려면 필요).
2. 「답변 대기 하나만」은 부분 유일 대신 **스레드 행 잠금 + 확인**(저장소 규칙: 유일 인덱스 WHERE 는 `deleted_at IS NULL` 만). 버전/댓글 키도 `live_unique`.
3. 자동 닫힘은 10초 회차(`announce_confirmed`)마다 「요청됨」 스레드를 훑는다 — 많아지면 SQL 거름 필요.
4. W18 = [예약 수정]에서 상담사가 바뀔 때만(지우기 = 보내지 않음 · KOS 에 「없음」 쓰기 없음). [예약 생성]은 W3 안에 counselor(Q01).
5. 웹 동작 HTTP 끝-끝 테스트는 `tests/day/web/`(FE 몫)라 안 씀 — 서비스 단위 infra 테스트로 대신. KOS 실제 e2e = 코디.
6. 배포 때 env `DAY_EXT_PARTNER_GRANTS` 를 병원당 한 줄(partner 없음)로 바꿔야 함(아니면 ext 503) — OQ-Q12 · taewoo 리뷰.
