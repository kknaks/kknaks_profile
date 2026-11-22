# day-mobile-v2 F1 결과 보고 — Android 푸시 FCM 서버 + P2 검수 남은 것

## 상태: done

워크트리 `/Users/kknaks/orca/workspaces/CENTURION_DAY/day-mobile-v2` · P3 `9162ee18` 위. 커밋 · push · PR 없음. `app/` · Key Vault 손대지 않음.

---

## A. FCM (DAY-SPEC-003 §3 「Android 푸시 — FCM」 · OQ-A50 · A51 · A59 · DAY-SPEC-000 2026-11-20)

### 동작

| 항목 | 구현 |
|---|---|
| 기기 등록 | `PUT /api/devices/{install_id}` 에 `platform: "android"` · `push_env` **보내지 않음**(칸이 오면 null 이어도 400) · 토큰 = 빈 문자열 아님 · 4096자 이하 · 16진 검사는 `ios` 만 · `app_id` = `DAY_FCM_ALLOWED_APP_IDS` 안(밖 · iOS 목록의 id 면 400) · DB `push_env` = null. `ios` 는 그대로(`push_env` 필수 · 16진 · `DAY_APNS_ALLOWED_APP_IDS`) |
| 같은 토큰 = 연결 하나 | 이름공간 잠금 키의 `push_env` 자리 = `-`(android null) · 결속 끊기 조건은 `push_env IS NULL` 끼리(`services/devices.py` `_same_env`) — 2차 검수가 짚은 `push_env.value` 자리 |
| 보내기 대상 | `push.targets` — android 행은 `push_env` 없이 대상 · 허용 목록은 플랫폼별 · 세션 · 병원 · 직원 · 계정 규칙은 iOS 와 같다 |
| 발송 범위 | 원장 호출 · 호출 취소 · 채팅 — 셋 다 공유 `push.deliver` 를 지나며 기기 플랫폼으로 갈린다(android → FCM · ios → APNs) |
| FCM 클라이언트 | 새 `backend/day/adapters/fcm.py` — HTTP v1 `messages:send` · 서비스 계정 OAuth(RS256 assertion → `token_uri` · 접근 토큰 만료 1분 전까지 다시 씀) · 새 의존 없음(`httpx` · `PyJWT[crypto]`) |
| 메시지 모양 | **data 메시지** — `data` = APNs 본문의 커스텀 칸(`kind` · `environment` · `hospitalId` · `visitId` · `callId` · 채팅이면 `roomId` · `messageId`) + `title` · `body`(`aps.alert`) + `category`(`aps.category` 가 있을 때 = `CALL`) · 값 문자열 · `android.priority = HIGH` · `ttl` = APNs 만료에서(원장 호출 · 취소 `0s` · 채팅 1일). 알림 채널(「원장 호출」 · 「채팅」 · 취소 = 원장 호출 채널)은 앱이 `kind` 로 고른다 |
| 키 없음 | FCM 키(`DAY_FCM_SERVICE_ACCOUNT`)가 비면 **android 기기만** `skipped_no_key`(iOS 는 APNs 키대로 보냄) — 알림 행 · 실시간 그대로 |
| 죽은 토큰 | FCM `UNREGISTERED`(404) · `INVALID_ARGUMENT`(400) → `token_removed` + 결속 해제(보낸 시점 결속 · 토큰이 같을 때만 — APNs 와 같은 쿼리) |
| 재시도 | 네트워크 · 5xx · 429 → 1회 다시(APNs 와 같은 `send_with_retry`) |
| 로그 | `push_log` 의 `apns_status` · `apns_reason` · `apns_id` 칸에 FCM 상태 · 이유(`errorCode` 없으면 `status`) · 메시지 이름을 같이 쓴다(칸 이름은 그대로 · migration 없음). 키 · 접근 토큰 · 기기 토큰 전체는 로그 · 결과에 없음 |

### migration — `20261120_0013_device_platform_android.py`(0012 다음 · head 하나)

- upgrade: `ALTER TYPE device_platform ADD VALUE IF NOT EXISTS 'android'`
- downgrade: `android` 행은 `platform` · `login_session_id` 를 비워 보내기 대상에서 뺌(행 · `push_log` 는 남김) → 옛 값(`ios`)만 든 타입으로 칸 옮김
- 실제 PG 테스트 스키마 upgrade → downgrade(0012) → upgrade 확인 · `test_alembic` HEAD 0013 · P3 의 0012 시험은 downgrade 대상을 `0011` 로 고정(head 가 바뀌어 `-1` 이 0012 를 가리킴)

### 바꾼 파일(A)

- 새 `backend/day/adapters/fcm.py` · `taut.toml`(resource 역할에 `fcm.py` 한 줄 · **코디 허용**)
- `backend/common/config.py` — `day_fcm_service_account`(비밀) · `day_fcm_allowed_app_ids` · `fcm_allowed_app_ids` · `fcm_enabled`
- `backend/day/enums/device.py` — `DevicePlatform.ANDROID`
- `backend/day/schemas/devices.py` — 플랫폼별 검사(`model_validator`)
- `backend/day/routers/api/devices.py` — `push_env` 변환 한 줄(None 이면 None · **코디 허용**)
- `backend/day/services/devices.py` — 허용 목록 플랫폼별 · 이름공간 · `push_env` null 비교
- `backend/day/services/push.py` — 대상 · 플랫폼별 키 · 클라이언트(`fcm_factory`) · 죽은 토큰 규칙
- `backend/day/adapters/apns.py` — `push_env: str | None`(없으면 보내지 않고 `NoPushEnv` — ios 행은 등록 검사로 늘 있음)
- `backend/day/services/chat_push.py` · `notifications.py` · `notification_cancel.py` — `fcm_factory` 인자 통과만
- `backend/migrations/versions/20261120_0013_device_platform_android.py`(새)
- `deploy/config/dev.env` = `DAY_FCM_ALLOWED_APP_IDS=day.medisolveai.dev` · `prod.env` = `day.medisolveai`(비밀 아님)
- 테스트: 새 `tests/day/notifications/test_fcm_client.py`(9 · DB 없음 · MockTransport · 시험용 RSA 키) · 새 `tests/day/chat/test_devices_android.py`(6) · 새 `tests/day/notifications/test_notification_push_android.py`(1) · 새 `tests/migrations/test_device_platform_android_migration.py`(3) · `tests/migrations/test_alembic.py`(HEAD) · `test_doctor_call_cancel_migration.py`(downgrade 대상) · `tests/day/chat/test_devices_push.py` · `tests/day/notifications/test_notification_push.py`(가짜 APNs `push_env: str | None` 타입만)

### FCM validate_only 실물 1회

- 키 = `~/.config/day/android/fcm-service-account.dev.json` 를 env `DAY_FCM_SERVICE_ACCOUNT` 로만 넘김(파일 복사 · 내용 · 토큰 출력 0).
- `FcmClient(validate_only=True)` 로 가짜 기기 토큰 하나에 원장 호출 모양 본문.
- 결과: **접근 토큰 받음**(서비스 계정 키 · OAuth 정상) · `messages:send` = **400 `INVALID_ARGUMENT`**(가짜 토큰) → 우리 갈래 = 죽은 토큰(`token_removed`). 실제 기기 토큰으로 보내는 것은 앱(mobile)의 실기기 몫.
- 결과 파일(키 없음): `/private/tmp/claude-501/-Users-kknaks-orca-workspaces-CENTURION-DAY-day-mobile-v2/b4d91637-4b4e-4d53-b5c5-e7424833781d/scratchpad/fcm/result.txt`

### Key Vault 에 넣을 비밀 env(값 없이)

| env | Key Vault 이름(규칙대로) | 꼴 |
|---|---|---|
| `DAY_FCM_SERVICE_ACCOUNT` | `day-dev-fcm-service-account` · `day-prod-fcm-service-account` | 서비스 계정 JSON **한 줄** · 선택 비밀(없으면 Android 만 `skipped_no_key` · 배포 성공) |

⚠ **배포 스크립트도 한 줄 필요** — `scripts/deploy/configuration.py` `OPTIONAL_SECRETS` 에 `"DAY_FCM_SERVICE_ACCOUNT": "fcm-service-account"` 가 있어야 Key Vault 값이 app.env 로 실린다(지금 `DAY_APNS_AUTH_KEY` · `DAY_SONIOX_API_KEY` 만). allowed_paths 밖이라 **손대지 않음** — 코디가 넣거나 지시 바람. 그 전까지 서버는 키 없음 = Android 푸시 `skipped_no_key`(나머지 정상).

---

## B. P2 검수 남은 것

| 검수 | 처리 |
|---|---|
| WARN-2 `/api/auth/device` 의 `client=web` 비대칭 | **`client=web` = 400 `invalid_request`(field `client`)** — 코디 결정(2026-11-20) · 근거 SPEC-001 §3 「JSON `/api/auth/*` 는 앱 전용」 · 웹 기기 선택은 `POST /login/device`. 토큰은 꺼내기 전에 거절해 앱이 다시 보낼 수 있음(`routers/api/auth.py` `device`) |
| WARN-1 앱 API 만료 · 로그 · 503 | 새 `tests/day/auth/test_device_choice_app_errors.py`(4): web 400 · 임시 토큰 5분 만료 401(KOS 안 부름) · 해제 중 KOS 장애 503 `kos_unavailable` + 그 토큰 재사용 401 · caplog 에 이메일 · 비밀번호 · 임시 토큰 없음 |
| WARN-4 `canCancelCall` 수락된 호출 | `tests/day/board/test_board_app_fields.py` 에 1건 — 같은 호출의 다른 줄이 수락됨 → 수락 전 줄도 `canCancelCall=false` · `cancel_call_block = call_already_accepted` |
| WARN-3 | 스펙 문서(SPEC-002 :672) 몫 — 코드 무변경 |

바꾼 파일(B): `backend/day/routers/api/auth.py` · 새 `tests/day/auth/test_device_choice_app_errors.py` · `tests/day/board/test_board_app_fields.py`. `services/auth.py` 는 바꿀 것 없었음.

---

## 전체 검증

- `./scripts/check.sh --static` — **전부 통과**(구조 · ruff · format · strict mypy · Taut audit/check · frontend)
- `scripts/test.sh -q`(전체 · 격리 인프라) — **2064 passed**(P3 뒤 2040 + 24). 그 뒤 `FcmKeyError` → `ValueError` 로만 바꾼 FCM 시험 9 다시 통과(Taut 가 새 업무 예외 클래스에 등록 코드를 요구 — 오류 코드 목록은 allowed_paths 밖이라 클래스를 두지 않음)
- 관련만: auth · board 새 칸 · migrations · chat · notifications · deploy = 495 + Android 알림 1 passed

## 이슈 · 코디가 확인할 것

1. **배포 스크립트 `OPTIONAL_SECRETS` 한 줄**(위 ⚠) — 이것 없이는 Key Vault 값이 서버에 닿지 않는다.
2. allowed_paths 밖(코디 허용): `taut.toml` 한 줄 · `routers/api/devices.py` 한 줄. 그 밖 `services/push.py`(공유 발송 — 채팅 · 호출 푸시 부분) · `adapters/apns.py`(`push_env` 타입) 는 FCM 갈래에 필요한 만큼.
3. `push_log` 칸 이름이 `apns_*` 인 채로 FCM 결과를 담는다 — 이름을 바꾸려면 migration(이번엔 안 함).
4. 앱 쪽: data 메시지라 앱이 로컬 알림을 띄워야 한다(채널 「원장 호출」 · 「채팅」 · `category = CALL` 이면 [수락]) — mobile 몫.
