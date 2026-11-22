# day-mobile-v2 P3 결과 보고 — 호출 취소 알림 + P1 남은 것 2개

## 상태: done

워크트리 `/Users/kknaks/orca/workspaces/CENTURION_DAY/day-mobile-v2` · P2 `e96b0718` 위. 커밋 · push · PR 없음. `app/` 손대지 않음.

---

## A. 호출 취소 알림(`doctor_call_cancel`)

### 동작(DAY-SPEC-005 2026-11-20 개정 · DAY-SPEC-002 규칙 38)

| 항목 | 구현 |
|---|---|
| 언제 | `cancel_call` 이 그 호출을 **완전히 닫을 때만**(`closed_at` 을 채운 경우) 커밋 뒤 `notification_cancel.after_cancel([call_id])`. 일부 줄 취소 = 아무것도 안 함(원래 알림 그대로) |
| 받는 사람 | 닫힌 그 호출의 원장 호출 행(`kind = doctor_call` · 같은 `doctor_call_id`)을 받은 계정 — 지금 계정 활성 · 그 병원 활성 직원인 계정만 · 「원장 호출」 설정을 끈 계정 제외(OQ-N18 기본값) · 원래 행이 없는 계정엔 안 만듦 |
| 알림 행 | 계정마다 1행 `kind = doctor_call_cancel` · `doctor_call_id` = 닫힌 호출 · `visit_id` · 제목 「호출 취소」 · 본문 「{방} · 호출 취소」(방 없으면 「방」) |
| 원래 알림 닫기 | 그 호출의 `doctor_call` 행 중 `read_at` 이 빈 것을 지금으로(목록엔 남음 · 안 읽은 수에서 빠짐) |
| 중복 · 원자성 | 호출 행 `FOR UPDATE` 안에서 있는 행 보고 없는 계정만(원장 호출과 같은 틀) · 취소 트랜잭션은 그대로 · 훅 실패해도 취소 200 · worker 태스크가 같은 함수로 메움 |
| 실시간 | 행을 쓴 계정 + 원래 알림을 닫은 계정에 `notification {unread}` |
| 앱 푸시(APNs) | 새 태스크 `day.notifications.call_cancel_push` → `send_cancel_push` — 같은 기기 고르기(`push.targets`) · 본문 `{aps: {alert: {title: "호출 취소", body}, sound: "default"}, kind: "doctor_call_cancel", environment, hospitalId, visitId, callId}` · 카테고리 없음 · 만료 0 · `push_log.kind = doctor_call_cancel` · 호출 단위 Redis 표지 `day:notify:call-cancel:{id}` + `push_log` 로 두 번 발송 0. FCM 은 이번 아님(F1) |
| 웹 OS 알림 | `static/day.js` `NOTIFY_KIND` = `["doctor_call", "doctor_call_cancel"]`(`.includes`) · 취소 행을 띄울 때 이 탭이 띄운 그 호출(`target.callId`)의 원장 호출 OS 알림을 `close()`(다른 탭 · 닫힌 탭 것은 못 닫음 — 스펙 그대로) |
| 앱 목록 | 서버 목록 · `unread` 는 종류를 거르지 않아 그대로 실림(`target = {visitId, callId}`) |

### migration — `20261120_0012_doctor_call_cancel_kind.py`(0011 다음 · head 하나)

- upgrade: `ALTER TYPE notification_kind ADD VALUE IF NOT EXISTS 'doctor_call_cancel'` · `push_kind` 같음
- downgrade: 새 값 쓰는 `push_log` · `notification` 행을 지우고 → 옛 값만 든 타입으로 다시 만들어 칸 옮김(PostgreSQL 은 enum 값을 지우지 못함)
- 실제 PG 테스트 스키마에서 upgrade → downgrade(-1) → upgrade 확인(`test_doctor_call_cancel_migration.py`) · `test_alembic` HEAD 를 0012 로 · `alembic check` 차이 없음 · 체인 head 하나

### 바꾼 파일(A)

- `backend/day/services/notification_cancel.py`(새 · **코디 허용**) · `backend/day/tasks/notifications.py`(태스크 1개 · **코디 허용**)
- `backend/day/services/board_calls.py` — `cancel_call` 커밋 뒤 훅(닫힌 경우만) · 문서
- `backend/day/services/notifications.py` — `_announce` → `announce_unread`(공개 이름 · 취소 쪽이 같이 씀 · 동작 같음)
- `backend/day/enums/notification.py` — `NotificationKind` · `PushKind` 에 `DOCTOR_CALL_CANCEL`
- `backend/migrations/versions/20261120_0012_doctor_call_cancel_kind.py`(새)
- `backend/day/static/day.js` — NOTIFY_KIND · 원래 OS 알림 닫기 부분만
- `adapters/apns.py` · `models/` · `schemas/` · `dtos/` — 바꿀 것 없음(알림 `kind` 칸은 문자열 · 모델은 enum 클래스에서 값을 읽음)
- 테스트: `tests/day/notifications/test_notification_cancel.py`(새 · 7) · `tests/migrations/test_doctor_call_cancel_migration.py`(새 · 3) · `tests/migrations/test_alembic.py`(HEAD) · `tests/day/conftest.py`(취소 푸시 발행을 실제 큐 대신 모으는 autouse 픽스처 — 원장 호출 것과 같은 까닭) · `tests/day/web/test_board_feedback.py`(JS 글자 단언 2줄)

### 검증(A)

- `scripts/test.sh -q backend/tests/migrations backend/tests/day/notifications backend/tests/day/board backend/tests/day/web` — **403 passed**
- 「로컬 실물(목 APNs)」 = `test_notification_cancel.py` 가 그것: 격리 PostgreSQL 테스트 스키마 + 실제 앱(`POST /api/visits/{id}/calls` → `POST /api/tasks/{id}/cancel-call` 두 번) → 첫 취소(줄 남음) 알림 0 · 원래 행 안 읽음 그대로 · 두 번째(호출 닫힘) 원장 둘에 취소 행 · 원래 행 `read_at` 채워짐 · 앱 목록 `unread = 1` · 푸시 태스크 발행 1번 · `send_cancel_push` 가 APNs 더블로 그 원장 기기 1대에만 본문 위 그대로 · `push_log` `doctor_call_cancel/sent` · 두 번째 · 표지 지운 세 번째 발송 0 · 설정 끈 원장 · 비활성 계정 행 0(원래 알림은 닫음) · 훅 실패해도 취소 200 · worker 가 메움
- JS: 이번에 워크트리에 잠근 npm 도구를 설치(`npm ci --ignore-scripts` · `scripts/frontend/node_modules` 는 gitignore)해서 **`check.sh --static` 이 frontend 단계까지 전부 통과**(CSS 재현 · ESLint · Stylelint · Prettier · JS 시험 59). JS 시험(`scripts/frontend/tests/controllers.test.mjs`)은 `NOTIFY_KIND` 를 문자열 전역으로 넣는데 `.includes` 라 그대로 통과 — 그 시험 파일은 손대지 않음

---

## B. P1 검수 남은 것

### B-1. W-1 · W-2 — 통키 경쟁 · 시간 초과 시험을 DAY 로(코드 수정 없음)

새 `tests/day/interpret/test_interpret_turn_races.py`(15건) — 통키 `back/tests/test_turn.py`:

| 통키 시험 | DAY 시험 |
|---|---|
| `test_3_other_side_restarts_clock…` | `test_3_반대쪽_새_말이면_시계를_다시_두_쪽_차례대로` |
| `test_9c_cancel_no_terminated_waits_3s_then_continues` | `test_9c_cancel_뒤_terminated_가_없으면_3초_기다리고_계속`(가짜 시계 2.9 s 아님 · 3.1 s 경고 · 연결 유지 · 다음 발화 계속) |
| `test_14_no_timestamps_even_split`(W-2) | `test_14_글자_시각이_없으면_고르게_나눈다` |
| `test_17_pause_whole_turn_no_end_of_segment` | `test_17_멈춤_중에_시작해_끝난_차례는_agent_text_0` |
| `test_19_logs_counts_only` | `test_19_로그는_수만_원문_없음` |
| `test_21` · `test_22` · `test_24` | 같은 번호 3건 |
| `test_next_turn_not_delayed_after_stop`(×2) | `test_멈춘_뒤_다음_차례가_밀리지_않는다[barge · playback_stopped]` |
| `test_stop_while_audio_start_in_flight`(×2) | `test_audio_start_를_보내는_중에_멈추면_그_뒤_PCM_audio_end_0[…]` |
| `test_barge_cancels_new_stream_in_progress` | `test_새_발화_스트림_진행_중_끼어들기는_그_발화를_cancel` |
| `test_echo_log_per_turn_and_rest_at_session_end` | `test_되울림_로그는_차례마다_그_몫_세션_끝에_나머지` |
| (덤) `Echo.on_pause` | `test_멈춤이_여유를_줄인다` |

- 하네스 손질만: `test_interpret_turn.py` 의 가짜에 손잡이 3개(`FakeTts.timestamps` · `term_on_cancel` · `FakeClient.block`) — 기존 시험 동작 그대로.
- **모두 처음부터 통과** — 코드 결함 없음(검수 판단과 같음). `test_15`(v6 아님) · `test_20`(records)은 DAY 해당 없음.
- 검증: `scripts/test.sh --pure backend/tests/day/interpret` — **318 passed**(303 + 15)

### B-2. 통역 동시 상한 3

- `deploy/config/dev.env` · `prod.env` — `# Soniox 조직 TTS 3 · 2026-11-20 사용자` + `DAY_INTERPRET_MAX_SESSIONS=3`(기존 「바꿀 때만 여기에 적는다」 주석 아래). 코드 기본값(6)은 그대로. 배포 계약 시험(`tests/deploy`) 통과.

---

## 전체 검증

- `./scripts/check.sh --static` — **전부 통과**(구조 · ruff · format · strict mypy · Taut audit/check · frontend)
- `scripts/test.sh -q`(전체 · 격리 인프라) — **2040 passed**(P2 뒤 2015 + 25)

## 이슈 · 코디가 확인할 것

1. allowed_paths 밖(코디 허용): `services/notification_cancel.py` 새 파일 · `tasks/notifications.py` 태스크 1개 · 그 밖으로 `tests/day/conftest.py`(관련 테스트 픽스처) · `tests/migrations/test_alembic.py`(HEAD 한 줄).
2. 새 태스크 이름 `day.notifications.call_cancel_push` 는 외부 계약(큐 이름) — worker 배포 때 같이 나가야 api 가 발행한 메시지를 받는다(api 만 먼저 나가면 큐에 남았다가 worker 가 뜨면 처리).
3. 받는 사람 「그 사이 병원 멤버십 잃음」 판정 = 그 병원 `staff` 활성 · 삭제 안 됨 + `account` 활성(원장 직무 태그까지는 보지 않음 — 원래 알림을 받은 사람이라).
4. 지금 `cancel_call` 은 유효 호출 하나만 닫으므로 사슬로 여러 호출이 함께 닫히는 경우는 생기지 않는다(스펙 N-3 사실 그대로) — `after_cancel` 은 호출 id 목록을 받아 그 경우도 처리한다.
5. 이번에 설치한 `scripts/frontend/node_modules`(gitignore)는 그대로 둠 — 지우려면 그 폴더만.
