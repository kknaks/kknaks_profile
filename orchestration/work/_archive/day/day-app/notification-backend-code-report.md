# 알림 v8 서버 구현 보고 — DAY-SPEC-005 (backend)

## 상태: done — 코드 · 스크래치 PG/Redis E2E 통과

- 하지 않은 것: 커밋 · push · PR · 하위 위임 0. 실키 · 실 Vault · 실 APNs 0. 서버 재시작 · migrate · seed 0. 앱 · 웹 · 스펙 · EMR 변경 0.
- 기준: 시작 head `3aaa9780` · SPEC `b0f71ec3` `spec-005-notifications.md`(+ 003/004/000/001) · 승인 v8(plan-approved).
- 원천: cc-prototype `77173cf8` `service/notifications.py` · `service/push.py:97-136` · `api/notifications.py`(git show 만).
- 모델 · migration 변경 0: `git diff HEAD -- backend/day/models backend/migrations` 비어 있음. alembic head `0007_chat_device` 하나.
- app/ 의 dirty 는 다른 writer 것이다 — 손대지 않았다.

## 변경 파일 (22 · sha256 = `notification-backend-evidence/changed-files-sha256.txt`)

| 구분 | 파일 | 내용 |
|---|---|---|
| 알림 업무 | `day/services/notifications.py`(새) | 목록 · 읽음 · 설정 · `ensure_call_rows` · `after_call` 훅 · `call_deliveries` · `send_call_push` |
| 실시간 | `day/services/notification_events.py`(새) | 채널 `day:notify:<병원>:<계정>` · `notification {unread}` |
| API | `day/routers/api/notifications.py`(새) · `day/schemas/notifications.py`(새) · `day/public.py`(조립) | 4 + 스트림 |
| 오류 | `day/errors.py` | `SettingNotAllowed`(400 `setting_not_allowed`) |
| 태스크 | `day/tasks/notifications.py`(새 · `day.notifications.call_push`) · `day/tasks/__init__.py` 등록 | |
| 호출 훅 | `day/services/board.py` | `call` :538 · `recall` :591 — `_finish`(커밋 · 판 신호 · KOS 발행) **뒤** `await notifications.after_call(row.id)` 한 줄씩. 업무 규칙 · 응답 · outbox 무변경 |
| 공유 푸시 추출 | `day/services/push.py`(새) · `day/services/chat_push.py`(이것을 부르도록) | 기기 고르기 `targets` · `Delivery` · `send_with_retry` · `is_dead` · `deliver`(skipped_no_key · 동시 상한 · push_log · 죽은 토큰 해제) · `claim` · `kick_task`. 채팅 동작 무변경. 기기 조건에 「세션 직원 지금도 활성」을 더함 |
| 공유 SSE 추출 | `day/services/live.py`(새 · 머리 전 구독 `Subscription`) · `day/services/chat_events.py`(상속) · `day/routers/api/streams.py`(새 · 본문 생성기 · 응답) · `day/routers/api/chat.py`(별칭으로 바꿈) | v7 W1 규칙 그대로 재사용 · 채팅 동작 무변경 |
| 시험 | `tests/day/notifications/`(conftest · api 16 · push 3 · units 3) · `tests/day/conftest.py`(호출 푸시 발행을 실제 큐 대신 기록 · autouse) · `tests/day/chat/test_chat_units.py`(공유 `Delivery` 칸 이름) | |

## API · 규칙 (SPEC-005 §3)

| # | 경로 | 구현 |
|---|---|---|
| 1 | `GET /api/notifications` | 세션 계정 **이고** 세션 병원 · 오늘(`HOSPITAL_TIMEZONE` 자정) · `created_at` 내림차순 · 같으면 id · 50. `unread` = 오늘 안 읽은 수(50 밖 포함). 항목 = `{id, kind, title, body, createdAt, readAt, target{visitId, callId}}` |
| 2 | `POST /api/notifications/read` | 원자적 `UPDATE … WHERE read_at IS NULL RETURNING`. 규칙은 아래 |
| 3 · 4 | `GET` · `PUT /api/me/notification-settings` | 세션 병원 원장 목록에 본인이 있으면 `[doctor_call]`, 아니면 `[]` · 저장 없으면 true · 받지 않는 종류 = 400 `setting_not_allowed` · 저장 = 계정 × 종류 upsert(계정 단위 · 여러 병원 같이) |
| 5 | `GET /api/notifications/stream` | 아래 |

읽음(#2) 규칙:
- `ids` 만 있으면 그 행만 · `ids: []` = 0건 · `callId` 만 있으면 그 호출 행만 · 둘 다 있으면 AND.
- 두 칸이 **모두 없을 때만** 모두 읽음 = 내 병원 + 내 계정 · **전체 날짜**.
- 남의 것 · 다른 병원 · 없는 id 는 조용히 빼고 200. 칸에 `null` 이 오면 400(구현 선택 — 아래).
- 응답 `{ok, read=실제 바꾼 수}` · `read > 0` 일 때만 실시간.

스트림(#5):
- 채널 = 계정 + 세션 병원 · Bearer.
- Redis 구독은 응답 머리 **전에** 확인까지 받는다(v7 W1 공용 코드).
- 이벤트를 보내기 전 · 10초마다 세션을 다시 본다. 로그아웃 · 만료 → `session_expired` 한 번.
- 1시간 · 15초 ping · 연결 직후 재전송 0. 응답 종료 · 취소 · 본문 시작 전 실패 모두 구독을 닫는다.

## 호출 훅 · 알림 행 · 중복 근거

- 받는 계정 = 전체 → 그 병원 원장 목록(`queries.board` 와 같은 판정: 직무 태그 doctor · 활성 · 시스템 아님) 중 활성 계정이 있는 직원 · 지정 → 그 원장. 관리자 추가 · 호출자 제외 없음(시험: 원장이 호출해도 자기 행).
- 설정 끔 = 행 · push_log 없음. 기기 · 키 없어도 행은 쓴다.
- 제목 「원장 호출」 · 본문 「{방} · 시술 {N}건 · 전체/지정 호출」 · 고객 정보 없음.
- 훅(`after_call`)은 **업무 커밋 뒤** 따로 돈다. 다음 차례로 처리하고, 어떤 예외도 삼킨다(로그만 · 호출 응답 그대로):
  1. 짧은 새 DB 세션에서 `ensure_call_rows`(3초 상한).
  2. 새 계정에 `notification {unread}`.
  3. 푸시 태스크 발행(1초 상한).
  - 시험: 행 쓰기를 실패시켜도 호출 200, 이어서 worker 본문이 행을 메움.
- **중복 0 근거**:
  - `ensure_call_rows` 는 그 `doctor_call` 행을 `SELECT … FOR UPDATE` 로 잠근다. 그 안에서 (call, kind) 의 기존 계정을 보고 없는 계정만 넣은 뒤 같은 트랜잭션으로 커밋한다.
  - 훅과 worker 태스크가 겹쳐도, 훅이 재시도해도 직렬이 된다. 새 유일 색인 · migration 은 없다.
  - 실제 PG 시험 두 건: 이미 행이 있는 호출에 6번 동시 실행 → 새 행 0. 행 없는 호출에 6번 동시 실행 → 한 실행만 2행, 나머지 0.
  - 재호출 = 새 call id 라 새 행 · 앞 행 그대로(시험).
- 푸시 중복 0: 호출 단위 Redis 표지(1일) + 알림 행마다 `push_log` 가 있으면 건너뜀. 표지를 지워도 두 번째 발송 0(시험).

## 원장 호출 푸시 (공유 코드)

- 기기 = 공유 `push.targets`:
  - 결속 세션이 살아 있고 · 세션 병원 = 호출 병원 · 계정 = 받는 사람 · 세션 직원 · 계정 활성.
  - platform · app_id(허용 목록) · push_env 있음 · 옛 null 행 제외.
- 본문 = `{aps:{alert:{title, body}, sound:"default", category?:"CALL"}, kind:"doctor_call", environment, hospitalId, visitId, callId}` · 만료 0.
- `CALL` = 그 기기 세션 직원의 직무에 `board.accept` edit 가 있거나 전체 권한 계정(`DAY_ADMIN_EMAILS`)일 때(기존 권한 판정과 같은 근거).
- push_log = kind `doctor_call` · `notification_id` · category · token_tail.
- 키 없음 = `skipped_no_key`. 재시도 · 죽은 토큰 = 채팅과 같은 공유 `deliver`(보낸 시점 결속 · 토큰이 같을 때만 해제).
- 업무 트랜잭션 안에서 네트워크를 기다리지 않는다(HTTP 는 세션을 닫은 뒤).

## 검증 (각 최종 1회 · 증거 `notification-backend-evidence/`)

| 명령 | 결과 |
|---|---|
| `uv run pytest -q -m "not infra"` | **551 passed**(이전 548 + 3) |
| `DAY_ENV_FILE=…/deploy/local.env scripts/test.sh -q` | **787 passed · 0 failed**(이전 765 + 22) · 64s · warning 1(기존) |
| `pytest backend/tests/architecture` | 27 passed |
| `ruff check backend scripts` · `ruff format --check backend` | 통과 · 197 formatted |
| `alembic heads` | `0007_chat_device (head)` 하나 |
| 모델 · migration diff | 0 |

- 실행 전후: 다른 pytest 없음 확인 · `day_test` 스키마 + Redis db15 만 · env 값 출력 0 · 업무 DB · day-local 큐/포트/프로세스 조작 0.
- 중간 실행: 판 · 채팅 · 웹 회귀 221 passed · 알림 E2E 19 passed(개발 중 · 최종 수치는 위 1회).
- 합성 데이터: 두 병원 · 다중 병원 계정(A 원장 · B 코디) · 원장(계정 있음 2 · 계정 없음 1 · 비활성 1) · 간호(호출자) · 다기기(A 세션 · B 세션 · 간호).

## 앱 전달 계약

SPEC-005 §3 그대로이고 계약 차이는 0 이다. 앱이 알아 둘 것:

- `target` 칸은 값이 있을 때만 싣는다.
- 시각은 ISO 8601 · 밀리초 · UTC 오프셋이다(채팅과 같음).
- 읽음 본문의 `ids` · `callId` 칸에 `null` 을 보내면 400 `invalid_request` 다. 앱은 칸을 빼서 보낸다.
- 스트림 data 는 `{"unread": n}` 한 줄이다.

## 구현 선택 (SPEC 이 정하지 않은 곳 — 코디 확인)

1. 읽음의 `null` 칸 = 400(SPEC 은 「두 칸이 아예 없을 때만 모두 읽음」 — null 을 없음으로 보면 실수로 모두 읽음이 될 수 있어 거절).
2. 알림 스트림 인증 = 세션 생존만 본다(SPEC 「세션이 살아 있으면」). 채팅처럼 활성 직원까지 보지는 않는다.
3. 공유 기기 조건에 「세션 직원 활성」을 더해 채팅 푸시도 같이 엄격해졌다. 비활성 직원 세션 기기에는 보내지 않는다.
4. 훅 상한 3초 · 푸시 발행 상한 1초(`DAY_CHAT_PUSH_KICK_TIMEOUT_SECONDS` 재사용 — 새 설정 이름 0).

## 미실행 · pending (정직)

- 실 APNs 키 · Apple 설정 · 실기기 수신 · 잠금 화면 [수락] = 미실행(APNs 는 경계 더블).
- 실 Key Vault · dev/prod 배포 · 사용자 day-local 실물 = 미실행.
- 새 설정 이름 · 배포 배선 변경 0(기존 `DAY_APNS_*` 를 그대로 쓴다).
