# day-mobile-v2 고침 2 결과 보고 — F1 검수 FAIL 1 · WARN 3 + 고침 1 남은 infra 시험

## 상태: done

워크트리 `/Users/kknaks/orca/workspaces/CENTURION_DAY/day-mobile-v2` · 고침 1 `c22b56bc` 위. 커밋 없음. `app/` · 사용자 `day-local` 손대지 않음(시험은 `scripts/test.sh` 격리 인프라).

## FAIL-1 — FCM 키 배포 · 로컬 연결

| 곳 | 바꾼 것 |
|---|---|
| `scripts/deploy/configuration.py` | `OPTIONAL_SECRETS` 한 줄은 고침 1 에서 들어감 → `FORBIDDEN_CONFIG_KEYS` 가 `OPTIONAL_SECRETS` 에서 만들어지므로 **`deploy/config/<env>.env` 에 `DAY_FCM_SERVICE_ACCOUNT` 를 적으면 이제 거부**(코드 변경 없음 · 시험으로 고정) |
| `scripts/devtools/environment.py` | 로컬 「외부 연동 없음」 가드 목록에 `DAY_FCM_SERVICE_ACCOUNT` — 로컬 env 에 키가 있으면 로컬 설정 검사가 멈춘다(로컬 서버가 실제 FCM 으로 보내지 않게) |
| `deploy/local.env.example` | `DAY_FCM_SERVICE_ACCOUNT=` · `DAY_FCM_ALLOWED_APP_IDS=`(빈 값 · APNs 와 같은 꼴 · 설명 주석) |
| `deploy/compose.local.yaml` | api 환경에 두 칸(`${…:-}`) |
| `docs/development/deployment.md` | 선택 비밀 목록에 `day-<env>-fcm-service-account`(`DAY_FCM_SERVICE_ACCOUNT` · 한 줄 JSON `jq -c` · 여러 줄이면 `value-unquotable` 로 멈춤 · 없으면 Android 만 `skipped_no_key`) · Git 일반 설정에 적으면 거부 · `DAY_FCM_ALLOWED_APP_IDS` 는 일반 설정(dev · prod 값) |

시험: `tests/deploy/test_day_vm.py` 「선택 비밀을 Git 일반 설정에 넣으면 거부한다」에 FCM 키 · `tests/devtools/test_local_safety.py` 「외부 연동 켜는 로컬 값 거부」에 FCM 키.

## W-1 — `INVALID_ARGUMENT` 는 토큰 칸일 때만 죽은 토큰

- **실물 모양 확인**(코디 허용 · dev 서비스 계정 · validate_only 1회 · 가짜 토큰 · 키 · 토큰 출력 없음): HTTP 400 · `status = INVALID_ARGUMENT` · details = ① `google.firebase.fcm.v1.FcmError` `errorCode = INVALID_ARGUMENT` ② `google.rpc.BadRequest` `fieldViolations[].field = "message.token"`.
- `adapters/fcm.py` `reason_of` — `INVALID_ARGUMENT` 이고 `fieldViolations` 에 `message.token` 이 있으면 이유 = `INVALID_ARGUMENT:message.token` · 그 밖 `INVALID_ARGUMENT` 는 그대로.
- `services/push.py` `DEAD_FCM = ("UNREGISTERED", "INVALID_ARGUMENT:message.token")` — 본문 오류(data · ttl · 크기)는 `failed` · **결속 유지**.
- `push_log.apns_reason` 에 `INVALID_ARGUMENT:message.token` 이 그대로 남는다(이유 글자가 F1 때와 달라짐 — 알고 감).
- 시험: `test_fcm_client.py` 토큰 칸 · 본문 칸 두 모양(실물 모양 그대로) → `is_dead` 참 · 거짓 · `test_devices_android.py` 본문 오류 = `failed` · 결속 유지(infra) · 토큰 오류 = `token_removed` 갈래는 새 이유 글자로.

## W-2 · W-3 — 접근 토큰 프로세스 캐시 · bootstrap 주입

- `adapters/fcm.py` 새 `FcmTokens` — 접근 토큰 하나 · 만료 1분 전까지 재사용 · 만료 뒤 동시 발급은 `asyncio.Lock` 으로 한 번(잠금은 지금 이벤트 루프에 묶고 루프가 바뀌면 새로). `FcmClient(tokens=…)` 주입 · 없으면 클라이언트 자기 캐시(시험 · 실물 확인용).
- `bootstrap/push.py` — `default_fcm_client`(APNs `default_client` 옆)가 서비스 계정 값의 SHA-256 키로 **프로세스 공유 `FcmTokens`** 를 붙인다(키 값 자체는 들고 있지 않음). `services/push.py` 는 이제 bootstrap 에서 가져온다(apns 와 같은 꼴 · 어댑터에서 기본 클라이언트 함수를 뺌).
- 결과: 발송마다 새 클라이언트를 만들어도(`deliver` 끝에 닫음) 토큰 엔드포인트 왕복은 만료 때 한 번 · 첫 묶음 동시 8건도 발급 1번.
- 시험: 같은 캐시를 쓴 클라이언트 8개 동시 발송 → 발급 1 · 그 뒤 새 클라이언트도 캐시 · 기본 클라이언트 둘이 같은 캐시 · `services/push.py` 가 bootstrap 에서 가져옴.

## 고침 1 남은 infra 시험

- `scripts/test.sh -q backend/tests/day/notifications backend/tests/deploy backend/tests/devtools backend/tests/day/chat backend/tests/migrations` — **360 passed**(격리 PG · Redis · 디스크 26 GiB 회복 뒤)

## 전체 검증

- `./scripts/check.sh --static` — 전부 통과(구조 · ruff · format · strict mypy · Taut · frontend)
- `scripts/test.sh -q`(전체 · 격리 인프라) — **2076 passed**
- 시험용 임시 산출물(스크래치 `pt`)은 지웠다.

## 바꾼 파일

`backend/day/adapters/fcm.py` · `backend/day/bootstrap/push.py` · `backend/day/services/push.py` · `scripts/devtools/environment.py` · `deploy/local.env.example` · `deploy/compose.local.yaml` · `docs/development/deployment.md` · 시험 `backend/tests/day/notifications/test_fcm_client.py` · `backend/tests/day/chat/test_devices_android.py` · `backend/tests/deploy/test_day_vm.py` · `backend/tests/devtools/test_local_safety.py`. `services/notifications.py` · `scripts/deploy/configuration.py` 는 바꿀 것 없었음.
