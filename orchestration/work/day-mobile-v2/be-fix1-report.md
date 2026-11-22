# day-mobile-v2 고침 1 결과 보고 — P3 검수 WARN · 푸시 묶음 ID · 배포 비밀 목록

## 상태: done (마지막 infra 재실행만 pending — 디스크 가득 · 아래)

워크트리 `/Users/kknaks/orca/workspaces/CENTURION_DAY/day-mobile-v2` · F1 `87cec04d` 위. 커밋 없음. `app/` 손대지 않음.

## 1. 취소 뒤 늦게 도는 원장 호출 푸시(P3 검수 WARN-1 · 실제 버그)

- `services/notifications.py`
  - `ensure_call_rows` — 호출 행을 잠근 뒤 `closed_at` 이 있으면(취소 · 재호출로 닫힘) **행을 쓰지 않고** None. → worker 가 닫힌 호출에 안 읽은 `doctor_call` 행을 새로 쓰지 않는다.
  - `call_deliveries` — 보내기 직전 호출을 다시 읽어 닫혔으면 0 · `read_at` 이 찬 행(취소가 닫은 원래 알림)도 보내지 않음.
  - 재호출은 새 call id 라 새 호출 쪽이 보낸다(재호출이 앞 호출을 닫는 경우도 앞 호출 푸시는 안 나감 — 같은 뜻).
- 남는 틈: 「다시 읽음 → APNs/FCM 요청」 사이 수 ms 의 경쟁은 남는다 → 아래 2(묶음 ID)가 OS 알림 센터에서 덮는다.
- 시험(`tests/day/notifications/test_notification_cancel.py` · infra):
  - `test_취소_뒤_늦게_도는_원장_호출_푸시는_보내지_않는다` — 호출 → 취소 → 늦은 `send_call_push` = 보낸 것 0 · 취소 푸시는 그대로 1
  - `test_원장_호출_훅이_실패한_채_취소되면_worker_가_닫힌_호출에_행을_쓰지_않는다` — 훅 실패 → 취소 → worker = 행 0 · 안 읽은 수 0

## 2. 푸시 묶음 = callId (코디 결정 a)

- `adapters/apns.py` — 본문에 `callId`(문자열)가 있으면 `apns-collapse-id` = 그 값(64바이트 상한 · uuid 36). 원장 호출 · 호출 취소 본문엔 같은 `callId` → 취소 푸시가 원래 호출 푸시를 덮는다. 채팅은 `callId` 가 없어 헤더 없음. 재호출 = 새 callId = 새 묶음.
- FCM — 새 칸 없음. data 에 `callId` 가 이미 실림 → 앱 F2 가 Android 알림 tag 로 쓴다(코디가 mobile 에 전달).
- 시험(새 `tests/day/notifications/test_push_collapse.py` · DB 없음): 원장 호출 · 취소 같은 헤더 · 채팅 헤더 없음 · FCM data 에 `callId`.
- ⚠ 주의: 처음엔 변수 이름을 `collapse` 로 썼다가 CSS 재현 검사가 깨졌다 — Tailwind 가 `backend/day/**` 를 훑어 `collapse` 를 유틸리티로 읽음. `group_key` 로 바꿔 해결(생성 CSS 무변경).

## 3. JS 시험(P3 검수 WARN-3) · 재호출 뒤 취소(WARN-4)

- `scripts/frontend/tests/controllers.test.mjs` — 픽스처 `NOTIFY_KIND` 를 실제와 같은 배열 `["doctor_call", "doctor_call_cancel"]` 로 · 새 시험 「a call cancel shows its own notification and closes the original call notification of this tab」: 원장 호출 둘(c1 · c2) 띄움 → c1 취소 행 → c1 원래 알림 `close()` 1번 · c2 그대로 · 취소 알림 띄움 · 읽힌 원래 행은 다시 안 띄움. `npm --prefix scripts/frontend run check` = CSS · ESLint · Stylelint · Prettier 통과 · **JS 시험 60/60**.
- `test_재호출_뒤_취소는_새_호출을_받은_계정만_앞_호출은_그대로`(infra) — 재호출로 생긴 새 호출을 취소 → 새 호출의 받은 계정에만 취소 알림 · 새 호출의 원래 알림만 닫힘 · 앞 호출은 취소 알림 0 · 원래 알림 상태 그대로 · 취소 훅은 새 호출 하나만.

## 4. 배포 비밀 목록

- `scripts/deploy/configuration.py` `OPTIONAL_SECRETS` 에 `"DAY_FCM_SERVICE_ACCOUNT": "fcm-service-account"` 한 줄 → Key Vault `day-<env>-fcm-service-account` 를 app.env 로 싣는다(없으면 빠짐 · 배포 성공 · Android 만 `skipped_no_key`).
- **Key Vault 값은 한 줄 JSON 이어야 한다**(예 `jq -c . 키파일`) — 내려받은 서비스 계정 파일은 여러 줄이고, 배포의 `render_env` 는 줄바꿈 값을 `value-unquotable` 로 거절한다(값 없이 멈춤 — 안전한 실패). 비밀 값 안의 `\n`(PEM 이스케이프)은 그대로 둔다.
- 배포 계약 시험(`tests/deploy/test_day_vm.py`) 고침: 선택 비밀 집합 · Key Vault 이름 · dry-run 출력 · materialize 가 묻는 이름 · 새 시험 「한 줄 JSON 은 그대로 실림 · 여러 줄은 멈춤」.

## 검증

- `ruff check backend scripts` · `ruff format --check` · strict mypy(445) — 통과
- `npm --prefix scripts/frontend run check` — 전부 통과(JS 60)
- `scripts/test.sh --pure`(deploy · notifications · chat · web · architecture) — **648 passed**
- infra: `scripts/test.sh -q backend/tests/day/notifications` — **47 passed**(새 경쟁 · 재호출 시험 포함 · 이 작업 중 실행). 그 뒤 바뀐 코드는 `apns.py` 변수 이름 하나(pure 시험이 덮음).
- **pending — infra 재실행**: 마지막에 다시 돌리려 했으나 **디스크가 가득 참(100% · 3.8 GiB 남음)** → Docker Desktop 이 뜨지 못하고 pytest 임시 폴더도 못 만듦. 내 것이 아닌 파일은 지우지 않았다. 공간을 비운 뒤 `scripts/test.sh -q backend/tests/day/notifications backend/tests/deploy` 한 번이면 된다.

## 바꾼 파일

- `backend/day/services/notifications.py` · `backend/day/adapters/apns.py`
- `scripts/deploy/configuration.py`(한 줄) · `scripts/frontend/tests/controllers.test.mjs`
- 시험: `backend/tests/day/notifications/test_notification_cancel.py` · 새 `test_push_collapse.py` · `backend/tests/deploy/test_day_vm.py`
- 워크트리의 `.gitignore`(`google-services.json`) 변경은 내 것이 아님(mobile 쪽으로 보임).
