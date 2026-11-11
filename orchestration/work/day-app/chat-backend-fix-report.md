# chat-backend fix 결과 보고 — 리뷰 WARN 3 마감 + 로컬 disk 영속

## 상태: done — 커밋 · push · PR · 서비스 기동 · migrate · 실 Vault/키 읽기 없음

근거: `chat-backend-review.md`(W1 · W2 · W3) · `chat-backend-fix-brief.md` · 코디 후속(Dockerfile 경로 = `deploy/Dockerfile`).

## 바꾼 파일 (이번 fix)

| 파일 | 내용 |
|---|---|
| `backend/day/services/chat_events.py` | `Subscription`(open = SUBSCRIBE + Redis 확인 메시지까지 받음 · `messages()` · 멱등 `close()`) — 옛 `subscribe()` 생성기 대체 |
| `backend/day/routers/api/chat.py` | `stream` 이 응답을 돌려주기 **전에** 구독을 연다 · `ChatStreamResponse`(응답 종료 · 끊김 · 취소 · 본문 시작 전 실패 모두 `finally` 에서 구독 닫기) · `chat_stream_events(subscription, …)` 도 finally 닫기 |
| `scripts/deploy/day_vm.py` | 선택 비밀 `OPTIONAL_SECRETS`(`DAY_CHAT_BLOB_CONNECTION_STRING` → `day-<env>-chat-blob-connection-string` · `DAY_APNS_AUTH_KEY` → `day-<env>-apns-auth-key`) · `read_optional_key_vault`(404 = 건너뜀 · 그 밖 실패 = 멈춤) · `optional_app_env`(빈 값 빼기 · PEM 줄바꿈 → `\n` 두 글자) · `FORBIDDEN_CONFIG_KEYS` 에 두 이름 · dry-run 은 `<key-vault-optional:…>` 이름만 |
| `deploy/Dockerfile` | `useradd` 뒤 · `USER day` 앞에 `/var/lib/day/chat` 생성 · `chown day:day` · `0700` |
| `deploy/compose.local.yaml` | api 에 named volume `day_chat_files:/var/lib/day/chat` · `DAY_CHAT_STORAGE_DIR` 기본값 `/var/lib/day/chat` · 최상위 volumes 에 `day_chat_files` 추가(기존 볼륨 무변경) · `DAY_CHAT_STORAGE` 기본 빈 값(꺼짐) 유지 |
| `deploy/local.env.example` | disk 켜는 법 설명(값 없음) |
| 테스트 | `tests/day/chat/test_chat_stream.py`(새 서명 · ASGI 순서 회귀 · 취소 정리) · `tests/deploy/test_day_vm.py`(선택 비밀 7건 · 기존 materialize 테스트에 선택 reader 더블) · `tests/deploy/test_chat_env_contract.py`(DIR 기본값 · Dockerfile/볼륨 계약) |

## WARN 별 before / after / 실제 결과

### W1 SSE 구독 순서
- before: 생성기 안에서 `retry` 를 yield 한 뒤에야 `pubsub.subscribe` — Starlette 는 생성기 시작 전에 `http.response.start` 를 보내므로 머리를 받은 앱의 메우기와 구독 사이에 틈(코드 구조로 확인 · 옛 코드로 새 테스트를 다시 돌려 보지는 않음).
- after: 라우트가 `Subscription.open`(SUBSCRIBE 확인 수신까지) → 그다음 응답 반환. 수명은 응답 객체 `__call__` 의 finally + 생성기 finally 둘 다에서 `close`(멱등 · shield).
- 실제: 새 회귀 테스트 = 앱을 ASGI 로 직접 돌려 `send(http.response.start)` 받는 그 순간 publish → 그 이벤트가 본문에 온다 · 머리 시점 NUMSUB = 1 · 끊김 뒤 0. 본문 시작 전 취소 테스트도 0. 기존 6종 · 1시간 · tick · 이벤트마다 세션 재검증 · 초기 재전송 0 · retry 3000 규칙 무변경(운영 기한 축소 · skip 없음).
- 첫 전체 실행에서 끊김 뒤 NUMSUB 를 바로 읽는 단언이 1회 실패(다른 연결이 UNSUBSCRIBE 처리 전에 읽음 — 테스트 타이밍). 3초까지 기다려 보는 단언으로 바꾼 뒤 스트림 파일 3회 연속 7 passed · 전체 765 passed. 실패 로그 보존 `full-test-sh-run1-flaky.txt`.

### W2 서버 선택 비밀 배선
- before: `app.env` = 필수 SECRETS 만 → 두 비밀이 서버에 갈 길 없음.
- after: Key Vault 에 있으면 app.env(Docker env_file)로, 없으면 빠짐 → 앱 fail-closed · 필수 비밀 계약 · 배포 준비 그대로.
- 실제(가짜 값 · 실제 az/IMDS 0): 없음/빈 값 = app.env == 필수만 · 있음 = 전달 · PEM 줄바꿈 보존(render 뒤 `ApnsClient` 가 원 PEM 으로 되돌림 확인) · 404 건너뜀 · 403 멈춤(이름만) · materialize stdout 에 값 0 · dry-run 은 이름만.

### W3 금지 키
- after: 두 이름을 Git 일반 설정에 넣으면 `config-key-forbidden key=…` 로 거부(테스트 2건).

### 코디 필수 — disk 영속
- 설계: 이미지가 `/var/lib/day/chat` 를 `day`(uid 10001) 소유 0700 으로 만들고, 빈 named volume 을 처음 붙이면 Docker 가 그 소유권을 복사 → `local.env` 에 `DAY_CHAT_STORAGE=disk` 만 넣으면 추가 코드 없이 사진 · 동영상 저장(재생성에도 남음). worker 는 파일을 안 써서 마운트하지 않음. 서버 compose 는 무변경(Blob 방향 · 사용자 설정).
- 실제 권한 근거: 임시 태그로 이미지 빌드 → 임시 볼륨으로 `docker run --rm` 2번: `id -un = day` · `stat = day 700` · 쓰기 ok · 새 컨테이너에서 읽기 ok(`volume-permission.txt`). 임시 이미지 · 볼륨은 바로 지움. day-local compose 서비스 재시작 · 기존 볼륨 변경 0(작업 시점 day-local api 가 29분 전 재시작돼 있었으나 내가 한 것 아님).

## 검증 (증거 `chat-backend-fix-evidence/`)

| 명령 | 결과 |
|---|---|
| `uv run pytest -q -m "not infra"` | 548 passed(이전 539 + 9) |
| `DAY_ENV_FILE=…/CENTURION_DAY/deploy/local.env scripts/test.sh -q`(최종 1회) | **765 passed, 0 failed**(이전 755 + 10) · 1 warning(기존) |
| 스트림 파일만 · 3회 | 7 passed × 3 |
| `pytest backend/tests/architecture` | 27 passed |
| `ruff check` · `ruff format --check` | 통과 · 184 formatted |
| `alembic heads` | `0007_chat_device (head)` 하나 |
| 실행 전 다른 pytest 프로세스 | 없음 확인 · 스크래치 `day_test` + Redis db15 만 · env 값 출력 0 |

## 미실행 · 남은 것 (정직)

- 실 Key Vault 읽기 · 실 서버 배포 · 실 APNs/Blob = 미실행(사용자 값 · 리소스). 서버에서 켜려면 사용자가 Key Vault 에 `day-<env>-apns-auth-key` · `day-<env>-chat-blob-connection-string` 을 넣고 `deploy/config/<env>.env` 에 `DAY_CHAT_STORAGE=blob` · `DAY_CHAT_BLOB_CONTAINER` · `DAY_APNS_KEY_ID` · `DAY_APNS_TEAM_ID` · `DAY_APNS_ALLOWED_APP_IDS` 값을 채워야 함(값 · 도메인 · 계정 하드코딩 0).
- Blob 접속 문자열에 홑따옴표가 있으면 기존 `render_env` 규칙대로 배포가 멈춘다(Azure 접속 문자열 형식상 보통 없음).
- 로컬 compose 실기동(사진 업로드 실물) = 미실행 — 권한은 임시 컨테이너로만 확인.
- 이번 수정 뒤 서버 HTTP · 기기 · 첨부 독립 리뷰는 코디가 예정(스스로 PASS 선언 안 함).
