# 재검수 리포트 — DAY 채팅 backend(WP v7) fix 뒤 / code (2026-11-10)

- 대상: `CENTURION_DAY/day-app` HEAD `b6c034bf` 위 미커밋 서버 변경 **45개 파일**. 첫 검수 42개 + fix 의 `scripts/deploy/day_vm.py` · `deploy/Dockerfile` · `backend/tests/deploy/test_day_vm.py` 등이 늘었다.
  - 파일별 sha256 은 `chat-backend-rereview-logs/file-hashes.txt` 에 남겼다.
  - `app/` 은 제외했다(mobile 검수와 병렬).
- 원천: `chat-backend-fix-report.md` · 첫 리뷰 `chat-backend-review.md` · `delivery-request-v7-execution.json` · SPEC `53adbd49` 의 004 · 000 · 003 · 001. 현재 spec `b0f71ec3` 의 /me 사실 정정은 참고만 했다. SPEC-005 는 범위 밖이다.
- 방식: read-only. 코드 수정 · 커밋 · 서비스 · 포트 · 운영 DB 조작 0, 하위 위임 0.
  - DB 테스트는 내가 유일한 실행자였다. 실행 전에 다른 pytest 가 없는 것을 확인했다.
  - `DAY_ENV_FILE=/Users/kknaks/git/CENTURION_DAY/deploy/local.env` 를 source 만 했다(`day_test` · Redis db15). 값은 출력하지 않았다.

## 판정: **PASS (WARN 1 — lint 한 줄)**

첫 검수 WARN 3건은 코드와 테스트로 모두 해소됐다. 이번에 새로 깊이 읽은 HTTP · 기기 · 첨부 · 멱등 권한 경계에서 FAIL 은 없다.

## 직접 실행

| 명령 | 결과 |
|---|---|
| `uv run ruff check backend` | 통과 |
| `uv run ruff check backend scripts` | **1 error** — `scripts/deploy/day_vm.py:183` E501(103 > 100) → W-R1 |
| `uv run pytest -q backend/tests/architecture backend/tests/deploy -m "not infra"` | **121 passed**(day_vm 선택 비밀 · 금지 키 · env 계약 · Dockerfile/볼륨 계약 포함) |
| `scripts/test.sh -q backend/tests/day/chat/test_chat_stream.py` × 3 | **7 passed × 3**(flaky 재발 없음) |
| `scripts/test.sh -q backend/tests/day/chat backend/tests/migrations/{test_chat_device_migration,test_alembic}.py backend/tests/day/test_chat_device_schema.py`(실 PG · Redis) | **96 passed** · 25.7s |

보고만 확인한 것: 전체 765 passed · not-infra 548 · 임시 이미지 · 볼륨 권한(`volume-permission.txt`). 전체 테스트와 docker 빌드는 다시 돌리지 않았다.

## 첫 WARN 해소 확인

| WARN | 이번 코드 | 판정 |
|---|---|---|
| W1 SSE 구독 순서 | `stream`(`routers/api/chat.py:586-609`)이 `Subscription.open`(`chat_events.py:95-112`)을 먼저 부른다. 여기서 `SUBSCRIBE` 를 보내고 `type == "subscribe"` 확인을 5초 안에 받은 **뒤에** 응답을 반환하므로, HTTP 머리가 나가기 전에 구독이 성립한다. 정리: `ChatStreamResponse.__call__` finally(`:578-582`, shield)와 본문 생성기 finally(`:569-570`)가 둘 다 `close()` 를 부르고, `_closed` 플래그로 한 번만 닫힌다. `open` 이 실패하면 `aclose` 후 다시 올린다. 세션 재검증 · 1시간 · ping · 재전송 0 규칙은 그대로다. | **해소**. 실 Redis 회귀(머리 받는 순간 publish → 본문 수신 · NUMSUB 1→0 · 본문 전 취소 0) 3회 연속 통과 |
| W2 서버 선택 비밀 | `day_vm.py`: `OPTIONAL_SECRETS` 2개(`day-<env>-chat-blob-connection-string` · `day-<env>-apns-auth-key`). `read_optional_key_vault` 는 404 면 건너뛰고 그 밖 실패면 `DeployError`(이름만) 로 멈춘다. `optional_app_env` 는 빈 값을 빼고 PEM 줄바꿈을 `\n` 으로 바꾼다. `ApnsClient` 가 `replace("\\n", "\n")`(`apns.py:52`)로 되돌린다. dry-run 은 이름만 보인다. | **해소**(실 Key Vault · 배포는 미실행) |
| W3 금지 키 | `FORBIDDEN_CONFIG_KEYS = {*SECRETS, *OPTIONAL_SECRETS, …}` → 두 이름이 Git 설정에 있으면 `config-key-forbidden` | **해소**(테스트 2건 통과) |
| 코디 필수: disk 영속 | `deploy/Dockerfile`: `/var/lib/day/chat` 를 `day:day 0700` 으로 만든다. `compose.local.yaml`: api 에만 named volume `day_chat_files`(기존 볼륨 무변경) · `DAY_CHAT_STORAGE_DIR` 기본값 경로 · `DAY_CHAT_STORAGE` 기본은 비어 있음(꺼짐). worker 는 첨부를 쓰지 않는다(`chat_push` 만). | **해소**(권한은 임시 컨테이너 증거로만 · 로컬 실물 업로드 미실행) |

## 새로 깊이 읽은 경계 (PASS)

**기기 `PUT/DELETE /api/devices/{install_id}`**(`services/devices.py` · `routers/api/devices.py` · `schemas/devices.py`)
- 본문은 `extra=forbid`, 토큰은 16진 · 1–4096자, `platform=ios`, `push_env`/`kind` 는 Literal, `app_id` ≤255 이고 허용 목록에 있어야 한다(비면 전부 400). install_id 는 uuid 로 정규화한다.
- 계정 · 세션은 서버가 채운다(본문에 칸 없음 → 메타 위조 불가).
- 잠금은 토큰 이름공간(platform, app_id, push_env, hash) advisory → 설치 advisory → 설치 행 FOR UPDATE 순서다. 모든 경로가 같은 순서라 교착 고리가 없고, 40P01 · 23505 는 3번 재시도한다.
- 늦게 온 이전 세션 PUT 은 서버 `login_session` (created_at, id) 순서로 무시한다. 같은 토큰을 가진 다른 설치의 결속은 같은 이름공간 안에서만 비운다(다른 topic · env 는 무변경).
- DELETE 는 요청 세션에 결속돼 있을 때만 비운다 → 새 로그인 결속을 지우지 않는다.
- 토큰은 `EncryptedText` 로 저장하고 로그에는 끝 6자리만 남긴다. 쓰기는 `writable_session`(쿠키면 CSRF).

**첨부**(`routers/api/chat.py:312-387` · `services/chat.py:1136-1329` · `chat_storage.py`)
- 업로드 순서: 인증 의존성 → `_form` bounded read(Content-Length 선검사 + 받은 바이트 누적이 한도를 넘으면 그 자리에서 413). Starlette 1.10 은 예외가 나면 임시 파일을 닫는다(`formparsers.py:281-284` 확인).
- 파일 수는 1/2개, 필드는 10개로 제한한다. JPEG `FFD8FF` · MP4 `ftyp` 를 바이트로 확인하고, 크기는 스트리밍 중에 세어 끊는다. 실패하면 쓰던 키를 지운다. 방 멤버 확인 후 DB 를 닫고 파일을 쓴다.
- 열기: 붙기 전에는 올린 사람 + 같은 병원 방만, 붙은 뒤에는 지금 멤버이고 메시지 `seq > from_seq` 이며 지우지 않은 것만. 아니면 404. 파일을 보내는 동안 DB 를 쥐지 않는다.
- Range 는 한 구간만 · 206/416 · HEAD 를 지원하고 응답은 `no-store` 다. Blob 은 서버가 대신 읽어 보내므로 공개 · 서명 URL 이 없다.
- 디스크 키는 서버가 만들고(`new_key`), 읽을 때 `check_key` + `resolve()` 루트 안인지 확인한다 → 경로 탈출이 없다.

**멱등 · 메시지 권한**(`services/chat.py:700-830`)
- clientId 는 (계정, clientId) advisory 잠금 안에서 **지운 행 포함** 첫 행을 찾는다. 다시 보내면 처음 것을 돌려주고 새 이벤트 · 푸시는 없다.
- 다른 방이나 내 경계 안에 있는 처음 행이면 404 다. 다른 병원의 같은 clientId 는 그 방이 아니므로 404 이고, 데이터가 새지 않는다.
- 첨부 붙이기는 첨부 행 FOR UPDATE + 「내가 그 방에 올림 · 아직 안 붙음 · 안 지움 · 같은 종류」일 때만 한다.
- 수정 · 삭제 · 전달은 「방 잠금 → 메시지 잠금」 순서이고, 멤버 아님 · 나감 · 다른 병원 · 경계 안이면 404 다.
- `actor`: 세션 병원 = staff 병원, 계정 일치, staff · account 활성, 시스템 계정 아님, 지우지 않음 — 아니면 403.

## WARN

### W-R1. `scripts/deploy/day_vm.py:183` docstring 이 lint 줄 길이를 넘음(E501 103 > 100)

- 재현: `uv run ruff check backend scripts` → 1 error. HEAD 의 같은 파일은 통과했으므로(`git show HEAD:…` 로 검사) 이번 fix 가 만든 것이다.
- 영향: 기능 영향은 없다. 저장소 문서의 gate 는 `ruff check backend` 라 지금 CI 를 깨지는 않는다. 다만 `scripts` 까지 lint 하는 사람에게 빨간 줄이 하나 생긴다.
- 최소 정정: docstring 을 두 줄로 나눈다.

## 참고 (결함 아님)

- 기기 토큰 해시는 대소문자를 그대로 쓴다(`token_hash`). 같은 토큰이 대소문자만 달리 오면 다른 이름공간이 된다. 앱은 늘 같은 형식을 보내므로 실제 영향은 없다. 바꾸려면 소문자로 맞추면 된다.
- 업로드는 방 멤버 확인보다 본문 수신이 먼저다(인증은 먼저). 멤버가 아닌 같은 병원 직원도 최대 ~95MB 를 임시로 올린 뒤 404 를 받는다. 한도가 있어 무제한은 아니다.
- Blob 접속 문자열에 홑따옴표가 있으면 기존 `render_env` 규칙대로 배포가 멈춘다(보고서도 기록).

## 직원이 실물에서 만날 자리

- 로컬: `local.env` 에 `DAY_CHAT_STORAGE=disk` 만 넣으면 사진 · 동영상이 named volume 에 남는다. 실물 업로드는 아직 아무도 해 보지 않았다.
- dev · prod: Key Vault 에 두 비밀을, 일반 설정에 `DAY_CHAT_STORAGE=blob` · 컨테이너 · APNs id 들을 사용자가 채우기 전까지는 지금처럼 첨부 409 · 푸시 skipped · 기기 400 이다(이제 켤 길은 있음).
- 채팅 스트림: 앞/뒤 전환 직후 메시지를 놓치는 틈은 없어졌다.

## 미검증 · 정직 기록

- 실 Key Vault 읽기 · 실 서버 배포 · 실 APNs 키/기기 · Azure Blob 실물 · 로컬 day-local 끝까지 흐름은 미실행이다.
- docker 이미지 빌드 · 볼륨 권한은 fix 작성자 증거만 읽었다(내가 다시 돌리지 않음).
- APNs 재시도 · 죽은 토큰 처리 · push_log 는 집중 테스트 재실행으로 통과만 확인했다(이번 fix 범위 밖 · 코드 무변경 영역).
