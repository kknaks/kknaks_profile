# 로컬 day-local 채팅 · 알림 반영 재기동 보고

## 상태: done — API ready (127.0.0.1:11040)

## 소스 (로컬 전용 scratch · 원본 repo · 브랜치 · merge 변경 0)
- 기반: `git archive 9ba7b79e`(day-procedure-board-2 최신 board) → `/private/tmp/claude-501/-Users-kknaks-orca-workspaces-CENTURION-DAY-day-app/44c3b558-a0fe-40d0-95a6-6e1de4d785d2/scratchpad/day-app-local-runtime/src`(alternates 로 원 repo 객체만 읽기).
- 얹은 것: `git diff 91728737 f83d7fab -- . ':!app'`(채팅 · 알림 · 기기 · APNs · 0006/0007 · deploy) 를 `git apply --3way`. 패치 = `/private/tmp/claude-501/-Users-kknaks-orca-workspaces-CENTURION-DAY-day-app/44c3b558-a0fe-40d0-95a6-6e1de4d785d2/scratchpad/day-app-local-runtime/f83.patch`.
- 충돌 3 → 해결:
  1. `services/board.py` import = 9ba(`DOCTOR_CHANGE_EVENT`) + `notifications` 둘 다(호출 · 재호출 훅 2줄은 깨끗이 들어감).
  2. `routers/api/auth.py` 로그인 = 데모 넘김 유지 + 9ba 시그니처 `auth.login(...)`(app_env 없음) + 빠진 `get_settings` import.
  3. `tests/migrations/test_alembic.py` HEAD = 0007.
- 0006 은 byte 동일(sha256 fb035182…0739).
- 단위: 639 passed · 1 failed. 실패 1 = 9ba `tests/architecture/test_demo_flag.py` 가 day-app 의 데모 로그인 넘김(채팅 이전부터 있던 D1)을 잡는다 — 런타임 무관 · 실제 브랜치 통합 때 결정 필요.

## 기동
- 롤백 이미지: `day-backend:local-rollback-9ba-202611102023`(= 옛 `day-backend:local` 97a3b2469dc4).
- 새 `day-backend:local` = 11b7a5d9624d(scratch `deploy/Dockerfile` · `/var/lib/day/chat` day 소유).
- 명령: `docker compose -p day-local -f <scratch>/deploy/compose.local.yaml --env-file <기존 local.env> --env-file <보호 override> --profile app` 으로 다음을 차례로:
  1. `build migrate`
  2. `run --rm --no-deps migrate alembic upgrade head` → **0006 → 0007 만**
  3. `up -d --no-deps api worker scheduler`
- postgres · redis 컨테이너 · 볼륨 무변경(28시간 계속 가동). 포트 11040/11042/11043 그대로. 새 named volume `day_chat_files`(api).
- DB 백업(먼저): `~/.local/share/day-local-backups/day-local-before-0007-20261110202452.dump`(pg_dump -Fc · 0600 · 268KB).

## 설정 (이름만 · 값 출력 0)
- 기존 local.env 그대로.
- 보호 override(`/private/tmp/claude-501/-Users-kknaks-orca-workspaces-CENTURION-DAY-day-app/44c3b558-a0fe-40d0-95a6-6e1de4d785d2/scratchpad/day-app-local-runtime/protected/apns-chat.override.env` · 0600):
  - `DAY_APNS_AUTH_KEY` · `DAY_APNS_KEY_ID` · `DAY_APNS_TEAM_ID` · `DAY_APNS_ALLOWED_APP_IDS` — `~/.config/day/apple/credentials.local.json` 의 apns · bundle_id 에서 프로그램적으로.
  - `DAY_CHAT_STORAGE=disk`.
- 컨테이너 확인: 키 전부 set · `apns_enabled=True` · storage disk · 첨부 폴더 쓰기 가능.

## 관문
| 항목 | 결과 |
|---|---|
| health | live 200 · ready 200 |
| OpenAPI 경로 | `/api/chat/rooms` · `/api/chat/stream` · `/api/notifications` · `/api/notifications/stream` · `/api/devices/{install_id}` 있음 |
| 기존 board(9ba) | `/api/board` · `/api/board/stream` · `/api/board/search` 있음 |
| 웹 | `/login` 200 · `/api/board` 무인증 401 |
| DB | revision `0007_chat_device` · 살아 있는 로그인 세션 3 그대로 |

## 미결
- APNs 실수신 미검증: 키 환경이 Production 일 수 있고 시뮬레이터는 Sandbox → 수신 주장 0.
- 테스트 계정 · 채팅/알림 E2E 실조작은 아직 안 함(테스트 데이터 0).
- mobile 터미널(`term_e8a8842c…`)은 메일박스 · 쓰기 불가로 status 직접 전달 실패 → 코디에게만 전달.
- 실제 PR #237 ↔ #238 통합 시 위 충돌 3 + `test_demo_flag` 결정 필요.

## 롤백
`docker tag day-backend:local-rollback-9ba-202611102023 day-backend:local` 뒤 원 compose(day-procedure-board-2/deploy/compose.local.yaml)로 `up -d --no-deps api worker scheduler`. DB 는 0007 이 null 허용 칸 · 인덱스 추가뿐이라 옛 코드도 그대로 돈다(되돌릴 땐 백업 pg_restore).

## 후속(사용자 직접 지시) — #237 을 #238 에 합침 · push
- `kknaksss/day-procedure-board-2` 에 `origin/kknaksss/day-app`(f83d7fab) 를 merge → `7ae19cef` push · PR #238 head = 7ae19cef · MERGEABLE.
- 충돌 3 은 위와 같은 해결. 시험 정정 3:
  - `test_demo_flag` 를 `\bis_demo\b` 단어 매칭으로 바꿈(실제 칸 사용은 허용 3파일뿐 확인).
  - `test_environments_api` 는 설정을 읽는 라우터만 패치.
  - 알림 재호출 시험은 개정 ⑮ 빈 본문으로.
- 검증: ruff backend scripts 통과 · `scripts/test.sh -q` 전체 = 정정 전 6 failed / 895 passed → 정정 뒤 해당 두 파일 28 passed(전체 재실행은 안 함).
- 로컬 실행 중인 서버의 `backend/day` · migrations 는 push 한 브랜치와 byte 동일(diff 0).
- **남은 계약 불일치**: 앱 `app/lib/state/board_controller.dart:173-174` 재호출이 `{target, doctorStaffId}` 를 보내는데, #238 서버는 빈 본문만 받는다(400 `invalid_request`). 앱 재호출 대상 고르기를 없앨지 결정이 필요하다(제품 결정 · 앱 미수정).
