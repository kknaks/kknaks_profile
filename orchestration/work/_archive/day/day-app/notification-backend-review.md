# 리뷰 리포트 — 알림 v8 서버(DAY-SPEC-005) / code (2026-11-10)

- 대상: `CENTURION_DAY/day-app` base `3aaa9780` 위 미커밋 서버 변경 22개 파일. `app/` 은 다른 writer 라 제외했다.
  - 내가 계산한 sha256 22개는 작성자 `notification-backend-evidence/changed-files-sha256.txt` 와 **완전히 같다**(diff 0).
  - 해시 목록은 `notification-backend-review-logs/file-hashes.txt` 에 있다.
- 원천: SPEC `b0f71ec3` `spec-005-notifications.md`(+ 003 · 004 · 000 · 001) · cc-prototype `77173cf8` · 승인 v8.
- 방식: read-only. 코드 수정 · 커밋 · 하위 위임 · 실키 · Apple · 서버 11040 · 실 env · 포트 · 프로세스 조작 0.
  - DB 테스트는 내가 단독으로 돌렸다. 실행 전에 다른 pytest 가 없는 것을 확인했다.
  - `DAY_ENV_FILE=/Users/kknaks/git/CENTURION_DAY/deploy/local.env` 는 `scripts/test.sh` 가 source 만 했다. `day_test` 스키마 · Redis db15 만 썼고 값은 출력하지 않았다.

## 판정: **PASS (WARN 1 — 시험 격리)**

제품 코드에서 FAIL 은 없다. WARN 은 시험 순서에 따라 결과가 바뀌는 것 1건이다.

## 직접 실행

| 명령 | 결과 |
|---|---|
| sha256 22개 대조 | 작성자 기록과 일치 |
| `git diff HEAD -- backend/day/models backend/migrations` | 0(모델 · migration 무변경) |
| `uv run ruff check backend scripts` | 통과 |
| `uv run pytest -q backend/tests/architecture` | 27 passed |
| `scripts/test.sh -q backend/tests/day/notifications backend/tests/day/chat backend/tests/day/board`(실 PG · Redis) | **1 failed · 185 passed** → W1 |
| 같은 3묶음 · 순서만 `board chat notifications` | **186 passed** |

보고만 확인한 것: 전체 787 passed · not-infra 551 · alembic head `0007` 하나. 전체 테스트는 다시 돌리지 않았다.

## WARN

### W1. 채팅 푸시 시험이 「알림 행 전체 테이블이 비어 있음」을 단언한다 — v8 뒤로 시험 순서에 따라 깨진다

- 위치: `backend/tests/day/chat/test_devices_push.py:276-277`
  ```python
  async with get_async_session() as s:
      assert (await s.scalars(select(Notification))).all() == []
  ```
- 재현:
  - `notifications` 시험을 `chat` 보다 먼저 돌리면 `Left contains 88 more items`(Notification) 로 실패한다.
  - 기본 알파벳 순서(board → chat → notifications)에서는 통과한다.
  - 로그: `notification-backend-review-logs/focused-infra.txt` · `focused-infra-default-order.txt`.
- 원인: v8 알림 E2E 시험은 실제 API 호출 → 커밋 뒤 훅이 **별도 세션에서 commit** 하는 구조라, 시험 스키마에 알림 행이 남는다(판 E2E 와 같은 방식 · rollback 대상이 아님). 채팅 시험은 자기 병원 · 메시지가 아니라 **테이블 전체**를 본다.
- 영향:
  - 제품 영향은 0이다.
  - 다만 시험 일부만 다시 돌리거나 순서를 바꾸면(AGENTS.md 가 다음 단계로 적은 `pytest-xdist` 분할 포함) 빨간 줄이 생긴다. 「채팅 푸시는 알림함을 쓰지 않는다」는 원래 의도도 다른 시험의 데이터 때문에 흐려진다.
- 최소 정정(시험만): 단언을 그 world 범위로 좁힌다. 예: `select(Notification).where(Notification.hospital_id == world.a)` 또는 그 world 계정들.

## 확인한 경계 (PASS)

**API 4 + SSE**(`routers/api/notifications.py` · `services/notifications.py`)
- 목록: 세션 계정 **과** 세션 병원 · 지우지 않음 · 병원 현지 오늘 0시(`today_start`) 이후 · `created_at desc, id desc` · 50.
  - `unread` = 같은 조건의 안 읽은 수(50 밖 포함, 별도 count).
  - `target` 은 값이 있는 칸만 싣는다.
- 읽음은 원자적 `UPDATE … WHERE read_at IS NULL RETURNING` 이다. `ids: []` 는 0건이다.
  - `ids` · `callId` 가 둘 다 오면 AND 이고, 두 칸이 **아예 없을 때만**(`model_fields_set` 비어 있음) 내 병원 · 계정 전체 날짜를 읽는다.
  - 칸 값이 null 이면 400 이다. 남의 것 · 다른 병원 행은 조건으로 빠진다.
  - `read > 0` 일 때만 커밋 뒤에 `notification {unread}` 를 보낸다(다른 기기 종 맞춤).
- 설정: 세션 병원 원장 목록 판정(`_is_doctor` = 직무 태그 doctor · 활성 · 시스템 아님 · 지우지 않음 — 수신자 판정 `_recipients` 와 같은 함수)이면 `[doctor_call]`, 아니면 `[]`.
  - 저장이 없으면 true, 받지 않는 종류는 400 `setting_not_allowed`.
  - upsert 는 계정 × 종류다(병원 전역).
- 스트림: 공유 `live.Subscription` 이 Redis SUBSCRIBE 확인을 받은 **뒤에** 응답 머리를 보낸다(v7 W1 규칙 재사용).
  - 채널은 `day:notify:<병원>:<계정>` 이고, 이벤트 이름 화이트리스트가 있다.
  - 이벤트 전 + 10초마다 세션 생존을 확인하고 → `session_expired`. 1시간과 만료 중 이른 때 닫고, 15초 ping, 초기 재전송 0.
  - 응답 · 생성기 finally 에서 멱등으로 닫는다. data 는 `{unread}` 숫자뿐이라 민감 데이터가 없다.

**호출 훅**(`services/board.py:537-539 · 590-592`)
- `_finish`(커밋 · 판 신호 · KOS 발행) **뒤에** `after_call(row.id)` 를 부른다. 업무 규칙 · 응답 · outbox 는 바뀌지 않았다.
- 훅은 3초 상한, 새 DB 세션이다. 모든 예외는 로그만 남기므로 호출 응답이 뒤집히지 않는다. 푸시 발행은 1초 상한이다.
- 수신자: 전체 = 그 병원의 원장 판정 + 활성 계정, 지정 = `target_staff_id` 그 원장. 관리자 추가 · 호출자 제외가 없다.
  - 설정 끔 = 행이 없다 → 푸시 · push_log 도 없다. 기기 · 키가 없어도 행은 쓴다.
- 중복 0: `doctor_call` 행 `FOR UPDATE` 안에서 (call, kind) 의 기존 계정을 보고 새 계정만 insert 한 뒤 같은 트랜잭션으로 commit 한다.
  - 훅과 worker 가 겹쳐도 직렬이다(실 PG 동시 6회 시험 통과).
  - 재호출은 새 call id 라 새 행이 생기고 앞 행은 그대로다.
- 본문은 「{방} · 시술 {N}건 · 전체/지정 호출」 이다(고객 정보 없음 · 프로토 `push.py:123-124`).

**공유 푸시**(`services/push.py` · `chat_push.py` 리팩터)
- 기기 = 결속 세션 생존 · 세션 병원 = 그 일의 병원 · 계정 · **세션 직원 활성(새 조건 · 채팅에도 적용)** · platform/app_id(허용 목록)/push_env.
- 재시도 1회(네트워크 · 5xx · 429), 죽은 토큰(410 · 400 3종)은 보낸 시점의 세션 · 토큰 해시가 지금도 같을 때만 결속을 해제한다. 상한 · timeout · 키 없음 = `skipped_no_key`. 이 동작은 v7 에서 그대로 옮겨졌다(코드 복제 0).
- 원장 호출 푸시: 만료 0 · `CALL` 카테고리 = 그 기기 **세션 직원**의 직무에 `board.accept` EDIT 가 있거나 관리자 이메일 계정.
  - payload = SPEC 칸(kind · environment · hospitalId · visitId · callId).
  - push_log 에는 `doctor_call` · `notification_id` · category · token_tail 이 들어간다.
- 중복 발송 0: 호출 단위 Redis claim(1일) + 알림 행별 push_log 존재 확인. 네트워크 발송은 DB 세션을 닫은 뒤에 한다.
- 채팅 회귀: 위 3묶음 186건(채팅 푸시 · 수신자 · 멱등 · 소프트 삭제 · 만료 1일 시험 포함)이 기본 순서에서 통과한다.

## 참고 (결함 아님 · SPEC 대로)

- 알림 행을 만든 뒤 푸시를 보내기 전에 원장이 설정을 끄면 그 한 건은 푸시가 간다. `call_deliveries` 는 설정을 다시 보지 않는다.
  - SPEC-005 :229 「받는 기기 = 알림 행을 쓴 계정(설정 켬)」 대로이고, 창은 커밋 직후 ms~초 단위다.
  - 직원 · 세션 · 토큰 변경은 `push.targets` 가 발송 시점에 다시 확인한다.
- `_announce` 의 unread 수는 각자 커밋 뒤에 따로 세서 보낸다. 동시 읽음 · 생성이 엇갈리면 늦게 도착한 이벤트가 이전 수일 수 있다. 앱은 다음 이벤트나 목록 조회로 맞춘다.
- 알림 스트림 guard 는 세션 생존만 본다(구현 선택 2 · SPEC-005 「세션이 살아 있으면」). 비활성 직원 세션도 unread 숫자는 받는다. 내용은 없다.

## 직원이 실물에서 만날 자리

- 원장 호출 → 원장 앱 종 숫자가 즉시 오르고, 알림 목록은 오늘 것만 보인다. 「모두 읽음」은 지난 날짜까지 읽음 처리한다.
- 설정을 끈 원장: 그 뒤 호출에는 알림 · 푸시가 없다. 판 표시는 그대로다.
- 실 APNs 키를 넣기 전에는 push_log `skipped_no_key` 만 쌓이고 잠금 화면 알림은 없다.

## 미검증 · pending (정직)

- 실 APNs 키 · Apple 설정 · 실기기 수신 · 잠금 화면 [수락] · 실 Key Vault · dev/prod 배포 · day-local 실물 = 미실행이다.
- 전체 787 · not-infra 551 은 작성자 보고만 확인했다. 내가 돌린 것은 위 3묶음(두 순서)과 lint · architecture 다.
