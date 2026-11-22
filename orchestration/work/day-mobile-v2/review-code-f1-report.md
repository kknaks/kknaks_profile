# 코드 검수 — backend F1 FCM (커밋 `87cec04d`)

판정: **조건부 PASS** — 코드 본체(등록 · 발송 · migration · auth)는 스펙과 맞고 시험도 통과. 다만 **FAIL 1건**(배포 · 로컬 설정에 FCM 키 연결이 빠짐 — allowed_paths 밖이라 워커가 손대지 않음)이 dev 배포 전에 닫혀야 하고, **WARN 3건**이 있다.

읽기만 했다(수정 · 커밋 없음). 근거: `git show 87cec04d` · 스펙 SPEC-003 §3 「Android 푸시 — FCM」(:695-707) · OQ-A50 · A51 · A59(:1165-1170) · SPEC-000 device(:37 · :1036-1052).

## 검증 실행

- `./scripts/test.sh -q backend/tests/day/notifications backend/tests/day/chat/test_devices_android.py backend/tests/day/chat/test_devices_push.py backend/tests/day/auth/test_device_choice_app_errors.py backend/tests/day/board/test_board_app_fields.py backend/tests/migrations` → **101 passed**(격리 PG · Redis)
- `uv run ruff check backend scripts` → All checks passed · `ruff format --check backend` → 432 files already formatted

## FAIL

### F-1 FCM 키가 배포 · 로컬 가드 어디에도 연결되지 않음
- `scripts/deploy/configuration.py:26-29` `OPTIONAL_SECRETS` 에 `DAY_FCM_SERVICE_ACCOUNT` 가 없다 → Key Vault 에 넣어도 app.env 로 실리지 않는다 → 서버는 계속 `skipped_no_key`(워커 리포트 ⚠ 와 같음).
- **워커 리포트에 없는 것** — 같은 파일 `:38-40` `FORBIDDEN_CONFIG_KEYS` 가 `OPTIONAL_SECRETS` 에서 만들어지므로, 지금은 누가 `deploy/config/<env>.env` 에 `DAY_FCM_SERVICE_ACCOUNT=` 를 적어도 배포 스크립트가 **거부하지 않는다**(AGENTS.md 「비밀 키를 넣으면 배포 스크립트가 거부한다」 보장이 FCM 키엔 없음). `OPTIONAL_SECRETS` 한 줄을 넣으면 함께 닫힌다.
- `scripts/devtools/environment.py:120-130` 로컬 「외부 연동 없음」 가드 목록에 `DAY_APNS_AUTH_KEY` · `DAY_SONIOX_API_KEY` 는 있고 `DAY_FCM_SERVICE_ACCOUNT` 는 없다 → 로컬 env 에 키를 넣으면 로컬 서버가 실제 FCM 으로 보낼 수 있다.
- 짝 문서 · 예시 미반영: `deploy/local.env.example:70`(APNs 만) · `deploy/compose.local.yaml:42`(APNs 만) · `docs/development/deployment.md:102`(선택 비밀 목록에 FCM 없음).
- 조치(코디): 위 4곳 + `deployment.md`. 키 이름 = `day-<env>-fcm-service-account`(JSON 한 줄 · `MULTILINE_SECRETS` 아님).

## WARN

### W-1 `INVALID_ARGUMENT` 를 모두 죽은 토큰으로 봄 — 본문 오류에도 결속이 풀림
- `backend/day/services/push.py:64`(`DEAD_FCM`) · `:282-284`(`is_dead` android 갈래) · `backend/day/adapters/fcm.py:82-91`(`reason_of`).
- FCM v1 은 토큰 오류와 **본문 오류(data 칸 · ttl 형식 · 크기 초과 등)** 를 똑같이 400 `INVALID_ARGUMENT` 로 준다. 토큰 오류는 `details` 의 `BadRequest.fieldViolations[].field == "message.token"` 로 갈린다.
- 스펙 :703 은 「`INVALID_ARGUMENT` **토큰 오류**」로 한정. 지금 구현이면 서버 쪽 본문 버그 하나가 나면 그 발송의 **모든 Android 기기 결속이 풀린다**(앱이 다시 로그인 · 등록할 때까지 푸시 0). 지금 본문은 평평하고 문자열이며 채팅 본문이 100자로 잘려(`services/chat_push.py:49-56`) 당장 터질 가능성은 낮지만, 되돌리기 힘든 쪽으로 실패한다.
- 제안: `reason_of` 가 `fieldViolations` 의 `message.token` 일 때만 `INVALID_ARGUMENT` 를 죽은 토큰으로 돌려주고, 그 밖은 `failed`. 시험 `test_fcm_client.py` · `test_devices_android.py:164` 에 본문 오류 갈래 1건.

### W-2 OAuth 접근 토큰 캐시가 사실상 발송 한 번짜리 · 첫 묶음은 동시 발급
- `services/push.py:319-334` — `deliver()` 가 호출될 때마다 `default_fcm_client(settings)` 를 새로 만들고 끝에 `aclose()` → `fcm.py:113`(`_access`)의 캐시는 그 한 번 안에서만 산다. 원장 호출 · 채팅 푸시마다 `oauth2.googleapis.com/token` 왕복이 한 번 더 붙는다(원장 호출 푸시 지연 · 토큰 엔드포인트 호출량).
- 같은 묶음 안에서도 `_bearer`(`fcm.py:123-147`)에 잠금이 없어, 첫 발송 때 `asyncio.gather` 동시 상한(`DAY_APNS_CONCURRENCY` 기본 8)만큼 토큰 요청이 동시에 나간다.
- 워커 리포트의 「접근 토큰 만료 1분 전까지 다시 씀」은 클라이언트 하나 기준으로만 맞다. APNs 도 같은 꼴(발송마다 클라이언트)이라 회귀는 아니고 동작은 정상이다.
- 제안: `_bearer` 에 `asyncio.Lock` · 접근 토큰(또는 클라이언트)을 워커 프로세스 단위로 캐시(`bootstrap/` 에 두기).

### W-3 FCM 기본 클라이언트 위치가 APNs 와 다름
- `services/push.py:44` 가 `day.adapters.fcm.default_fcm_client` 를 바로 import. APNs 는 `day.bootstrap.push.default_client`(`bootstrap/push.py`) 를 거친다. AGENTS.md 「bootstrap = 구현 선택 · 클라이언트 캐시 · 생성」. architecture 검사는 통과하지만 W-2 의 캐시를 넣을 자리도 bootstrap 이다. 낮은 우선순위.

## PASS (항목별)

### 1. 기기 등록 android · null push_env 잠금 키 · iOS 회귀
- `schemas/devices.py:47-54` — ios: `push_env` 필수 · 16진(`_HEX.fullmatch`) 그대로 / android: `push_env` 칸이 오면(null 이어도 `model_fields_set`) 400 · 토큰 1~4096자 · 16진 검사 없음 = OQ-A51 그대로.
- `services/devices.py:52-63` 허용 목록 플랫폼별(`DAY_FCM_ALLOWED_APP_IDS` · 비면 fail-closed) · `routers/api/devices.py:64` 변환.
- `services/devices.py:125-126` 이름공간 `push_env` 자리 = `-` · `:66-67` `_same_env` = `IS NULL` 비교 → SPEC-000 :1050 「android 는 push_env 없이」. 결속 해제 쿼리는 `platform` 도 걸어(`:150`) iOS 행을 건드리지 않음.
- 시험 `test_devices_android.py:82-112`(android 거절 5종 · 4096 OK · **iOS 그대로** — push_env 없음 400 · 16진 아닌 토큰 400 · Android app_id 400) · `:115-124`(같은 토큰 = 연결 하나).
- 참고(INFO): android 토큰 `" "`(공백) 도 통과 — 스펙 문구(「빈 문자열 아님」)엔 맞음.

### 2. FCM 발송
- data 메시지: `fcm.py:59-72` `data_of` — `aps` 제거 · `title` · `body` · `category`(있을 때만) · 값 `str`. 세 갈래 본문(`notifications.py:489-499` · `notification_cancel.py:253-261` · `chat_push.py:131-142`) 모두 평평한 문자열 칸이라 `str()` 로 안전. 호출 취소 `kind = doctor_call_cancel` · `callId` 있음 → 앱 F2 가 「원장 호출」 채널 고르기 · 원래 호출 알림 지우기에 쓸 값 있음. `category = CALL` 은 수락 가능 직원만(`notifications.py:490-491`). 채팅 `thread-id` 는 버리고 `roomId` · `messageId` 남김.
- `android.priority = HIGH` · `ttl` = 원장 호출 · 취소 `0s` / 채팅 1일(`fcm.py:75-79`). INFO: `0s` 는 기기가 Doze 등으로 바로 못 받으면 버려짐 — APNs `expiration=0` 과 같은 의미라 스펙과 일치.
- 키 없음: `push.py:305-316` 플랫폼별 `_has_key` — android 만 `skipped_no_key`, iOS 는 APNs 키대로. `config.py:295-299` `fcm_enabled`.
- 죽은 토큰: `UNREGISTERED`(404) → `token_removed` + 결속 해제(보낸 시점 세션 · 토큰 같을 때만 · `push.py:350-362`). `INVALID_ARGUMENT` 는 W-1.
- 재시도: 공유 `send_with_retry`(`push.py:262-279`) — `status None`(네트워크 · 키 · 토큰 엔드포인트 실패) · 5xx · 429 → 1회. APNs 와 같음.
- 키 노출 0: `fcm.py:41-56` 오류 문구는 칸 이름만 · `:159-160` · `:171-172` 예외는 클래스 이름만 · `push.py:338-344` 로그는 토큰 끝 6자리 · 상태 · 이유만 · `devices.py:171` 끝 6자리. 키 · 접근 토큰 · assertion 을 로그 · `push_log` 에 싣는 곳 없음.
- 시험 `test_fcm_client.py`(9 · DB 없음 · MockTransport) · `test_devices_android.py:128-195`(플랫폼별 클라이언트 · 죽은 토큰 2종 · 5xx 1회 다시).

### 3. 세 갈래 받는 사람 · push_log
- 세 갈래 모두 같은 `push.targets`(`push.py:195-240`) → 같은 받는 사람 · 같은 세션 · 병원 규칙, `deliver()` 안에서 기기 플랫폼으로만 갈림 → 같은 `push_log`(`_log`, `apns_*` 칸 재사용). `fcm_factory` 는 인자 통과만(`chat_push.py:160` · `notifications.py:517` · `notification_cancel.py:278`) — 받는 사람 코드 변경 없음.
- 시험 `test_notification_push_android.py:34-72`(원장 호출 · 호출 취소 → FCM · `push_log.kind` 두 종) · `test_devices_android.py:128`(채팅 iOS + Android 동시).
- INFO: `push_log.apns_*` 칸 이름에 FCM 값이 들어감 — 리포트 이슈 3 그대로, 운영 조회 때 혼동 주의.

### 4. migration 0013
- `20261120_0013_device_platform_android.py` — down_revision `0012_doctor_call_cancel_kind` · head 하나(`test_alembic` HEAD 0013 통과). upgrade `ADD VALUE IF NOT EXISTS`. downgrade: android 행 `platform` · `login_session_id` 비움 → 타입 다시 만들기. `device_platform` 을 쓰는 칸은 `device.platform` 하나(`0007_chat_device` 만 참조) → `ALTER COLUMN … TYPE` 안전.
- 시험 `test_device_platform_android_migration.py`(3 · 실제 PG up → down → up) · `test_doctor_call_cancel_migration.py` downgrade 대상 `0011` 고정은 head 이동에 맞는 수정.

### 5. `/api/auth/device` web 400 · P2 시험
- `routers/api/auth.py:159-162` — `client != "app"` 이면 `choose_device` **전에** 400 `invalid_request`(field `client`) → 임시 토큰을 쓰지 않아 앱이 다시 보낼 수 있음. 코디 결정 · SPEC-001 §3 근거.
- `test_device_choice_app_errors.py`(4: web 400 · 만료 401 KOS 안 부름 · KOS 장애 503 + 토큰 재사용 401 · caplog 에 이메일 · 비밀번호 · 임시 토큰 없음) · `test_board_app_fields.py`(+14줄 · 같은 호출의 다른 줄 수락 → `canCancelCall=false` · `call_already_accepted`).

### 6. 관련 테스트 · ruff
- 위 「검증 실행」 — 101 passed · ruff 통과.

## 시험 공백 (INFO)
- android 동시 `PUT`(같은 토큰 · null 잠금 키) 경합 시험 없음 — 키 문자열만 바뀌었고 iOS 동시 시험이 같은 코드 경로를 지나 위험 낮음.
- 원장 호출 android 끝까지 시험이 `category = CALL` 을 확인하지 않음(`data_of` 단위 시험이 따로 확인).
- W-1 본문 오류 갈래 시험 없음.
