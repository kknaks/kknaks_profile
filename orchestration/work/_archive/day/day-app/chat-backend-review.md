# 리뷰 리포트 — DAY 채팅 backend(WP v7) / code (2026-11-10)

- 대상: `CENTURION_DAY/day-app` HEAD `b6c034bf` 위의 미커밋 서버 변경 42개 파일. `app/` 은 mobile 이 동시에 고치는 중이라 제외했다.
  - 파일별 sha256 은 `chat-backend-review-logs/file-hashes.txt` 에 남겼다. 커밋 동일성 확인용이다.
- 계약: SPEC `53adbd49` 의 004 · 000(device) · 003 · 001.
  - 인용한 SPEC-004 줄(:249 · :388 · :400)은 pinned `53adbd49` 에도 같은 번호로 있다(`git show` 확인).
- 방식: read-only. 코드 수정 · 커밋 · 서버 · 운영 DB · 포트 조작 0, 하위 위임 0.
  - DB 하네스는 `DAY_ENV_FILE=/Users/kknaks/git/CENTURION_DAY/deploy/local.env` 를 source 만 해서 썼다(`day_test` · Redis db15). 값은 출력하지 않았다.
  - 실행 전에 다른 pytest 프로세스가 없는 것을 확인했다.
- 범위: 코디 지시대로 **SSE 경계와 설정 배선**을 깊게 봤다. 나머지 항목(HTTP 20 · 기기 · APNs · 첨부 · migration)은 집중 테스트 재실행과 보고 근거 확인 수준이다.

## 판정: **WARN (FAIL 0 · WARN 3)**

## 직접 실행 (내가 돌린 것)

| 명령 | 결과 |
|---|---|
| `uv run ruff check backend` | All checks passed |
| `uv run pytest -q backend/tests/architecture backend/tests/deploy -m "not infra"` | **112 passed** |
| `DAY_ENV_FILE=… scripts/test.sh -q backend/tests/day/chat backend/tests/migrations/test_chat_device_migration.py backend/tests/day/test_chat_device_schema.py`(실 PG · Redis) | **88 passed** · 13s |

보고만 확인한 것: 전체 755 passed · not-infra 539 · alembic head 1개 · 0006 sha 일치 · compose config 렌더. 전체 테스트는 다시 돌리지 않았다(브리프 지시).

## FAIL

없음.

## WARN

### W1. SSE 구독이 첫 바이트(`retry`)보다 늦게 걸린다 — 연결 직후 메시지를 놓칠 수 있음

- 위치: `backend/day/routers/api/chat.py:537-540` · `backend/day/services/chat_events.py:81-83`
- 내용: `chat_stream_events` 는 먼저 `yield "retry: 3000\n\n"` 을 내보낸다. 그다음 `async for … chat_events.subscribe(...)` 에 들어가서야 `pubsub.subscribe(name)` 이 실행된다.
  - async generator 는 첫 `__anext__` 때 몸통이 시작되므로, 클라이언트가 응답 머리와 `retry` 를 받은 시점에는 아직 Redis 채널을 듣고 있지 않다.
- 재현 시나리오:
  1. 앱이 스트림 연결을 확인한다(SPEC-004 :400 — 연결될 때마다 `GET /rooms` 와 `since` 로 메운다).
  2. 그 직후 다른 직원이 메시지를 보낸다.
  3. 이 메시지가 ① 앱의 `/rooms` · `since` 응답이 만들어진 **뒤**이고 ② `pubsub.subscribe` 완료 **전**에 publish 되면, 메우기에도 이벤트에도 잡히지 않는다.
  4. 다음 재연결이나 화면 재진입 전까지 새 메시지가 안 보인다. 실시간 채널 계약(:388 · :400)이 깨진다.
- 영향: 창은 ms 단위로 좁다. 다만 재연결이 잦은 모바일(앞/뒤 전환 · 3–30초 재연결)에서는 반복해서 생긴다. 서버 재전송이 없는 설계(:400)라 놓친 이벤트를 복구할 길이 없다.
- 최소 정정: 구독을 먼저 끝낸 다음 첫 바이트를 보낸다. 예를 들어 `subscribe()` 를 `pubsub.subscribe` 를 마친 뒤 반환하는 async context 로 만들고, 그 안에서 `retry` 를 yield 한다. 테스트: 「`retry` 를 받은 즉시 publish 한 이벤트가 스트림에 온다」 1건.
- 참고: 지금 테스트(`test_chat_stream.py:58-182`)는 라우트 함수를 직접 부르고 이벤트를 연결 뒤 충분히 늦게 보내서 이 순서를 보지 않는다.

### W2. 서버 배선 미완 — 채팅 비밀값이 dev · prod 서버에 갈 길이 없다(서버에서는 첨부 · 푸시를 켤 수 없음)

- 위치: `scripts/deploy/day_vm.py:34-42 · :228`(이번 diff 밖 · 무변경) · `deploy/config/{dev,prod}.env`(이번 diff)
- 내용: 서버 `app.env` 는 배포 때마다 `app_env = {key: secrets[key] for key in SECRETS}`(:228)로 **새로 만들어진다**. `SECRETS` 에는 DB · Redis · 암호화 키 · KOS 3개뿐이다.
  - 그래서 `DAY_CHAT_BLOB_CONNECTION_STRING` · `DAY_APNS_AUTH_KEY` 를 Key Vault 에 넣어도 컨테이너에 전달되지 않는다.
  - 손으로 `app.env` 에 넣어도 다음 배포가 덮어쓴다.
  - 서버 일반 설정의 `DAY_CHAT_STORAGE=` · `DAY_APNS_ALLOWED_APP_IDS=` 도 비어 있다.
- 결과(fail-closed 로 정상 동작):
  - 서버 앱에서 사진 · 동영상 올리기 · 열기 · 첨부 전달 = 409 `photo_disabled`.
  - 기기 등록 = 400(앱은 조용히 무시).
  - 채팅 푸시 = 전부 `skipped_no_key`.
  - 글 채팅 · SSE 는 동작한다.
- 판정 근거: mobile 보고서 「미실행 3」에 정직하게 적혀 있고, code_surface 밖이라 FAIL 은 아니다. 다만 「v7 = 채팅 첨부 · 채팅 APNs」를 서버에서 켜려면 **별도 승인 작업이 반드시 필요하다**는 것이 현재 상태다. `test_chat_env_contract.py` 도 로컬 compose · 일반 설정만 보고 서버 비밀 경로는 검사하지 않는다.
- 최소 정정(후속 · 별도 승인):
  - `day_vm.py` 에 **선택** 비밀 2개를 지원한다(값이 없으면 빈 값, 필수 아님). KOS 와 같은 Key Vault 이름 규칙을 따른다.
  - 서버 dev env 에 `DAY_CHAT_STORAGE=blob` · 컨테이너 · `DAY_APNS_*` 이름 값을 사용자가 채운다.
  - `day_vm` 테스트 1건을 더한다.

### W3. 새 비밀 이름이 배포 「Git 설정 금지 키」 검사에 없다

- 위치: `scripts/deploy/day_vm.py:45` `FORBIDDEN_CONFIG_KEYS = {*SECRETS, "REDIS_PASSWORD", "GIT_SHA", "DAY_IMAGE"}` · `validate_config` :110
- 내용: AGENTS.md 「비밀 키를 넣으면 배포 스크립트가 거부한다」는 지금 `SECRETS` 에 있는 키만 지킨다.
  - 누가 `deploy/config/dev.env` 에 `DAY_APNS_AUTH_KEY=…`(p8 본문)나 Blob 접속 문자열을 넣어도 배포가 통과한다. 그대로 Git 에 커밋된 비밀이 서버로 간다.
  - `test_chat_env_contract.py:66-73` 은 **현재 파일 내용**만 단언한다. 배포 경로의 거부는 막지 않는다.
- 영향: 지금 값은 비어 있어 실제 노출은 0이다. W2 를 고치러 손대는 사람이 Git 설정에 비밀을 넣는 실수를 배포가 못 잡는다.
- 최소 정정: W2 와 함께 두 이름을 `FORBIDDEN_CONFIG_KEYS` 에 넣는다(선택 SECRETS 에 넣으면 자동 포함). `validate_config` 거부 테스트 1건.

## SSE 나머지 확인 (PASS)

| 항목 | 근거 |
|---|---|
| 병원 · 계정 격리 | 채널 = `day:chat:<hospital>:<account>`(`chat_events.py:51`) · 스트림은 세션의 (hospital, account) 만 구독 · 다른 병원 세션은 그 병원 채널만 |
| 받을 사람 = 이벤트를 만들 때(트랜잭션 안) 계산 · 커밋 뒤 발행 | `_finish`(`services/chat.py:172-178`) · 실패해도 업무는 성공(로그는 id 만) |
| 세션 · 권한이 도중에 바뀜 | 이벤트를 보낼 때마다 + 10초마다 `still_active`(로그인 세션 삭제 · 만료 · 활성 직원)를 다시 확인 → `session_expired` + 코드 후 종료. 확인할 때마다 짧은 DB 세션을 쓰고, 연결 내내 쥐지 않음(`:507-514` · 스트림 열기 전 `session.close()`) |
| 수명 | 1시간과 세션 만료 중 이른 때 · 15초 `: ping` · `retry: 3000` · 끊기면 `finally` 에서 unsubscribe · aclose |
| 초대 전 메시지 · 경계 | 실 Redis 테스트 `test_새로_초대된_사람은_초대_전_메시지_이벤트를_받지_않는다` 통과(내 재실행 포함) |

참고(결함 아님):
- Redis 클라이언트는 연결 수 상한이 없고(`common/redis.py:40-46`), SSE 하나가 pubsub 연결 하나를 쥔다. 직원 앱 규모에서는 문제가 아니다.
- 이벤트마다 DB 확인을 한 번씩 하므로, 메시지가 몰리면 확인 쿼리도 같이 는다.

## 설정 나머지 확인 (PASS)

- `common/config.py` 새 키는 SecretStr 2개와 상한(`Field gt/le`)을 쓴다.
- 미설정이면 꺼짐: 저장소 `storage_from` → None → 409. `blob` 인데 접속 문자열 · 컨테이너가 하나라도 비어도 None. APNs 는 셋 다 있어야 `apns_enabled`. 허용 app_id 가 비면 400.
- 로컬 `compose.local.yaml` 은 x-backend 앵커로 api · worker · scheduler 모두에 8키를 넘긴다. 서버 `compose.yaml` 은 `env_file` 로 일반 설정과 `app.env` 를 넘긴다.
- `dev/prod.env` 에는 비밀이 없고 값은 비어 있다.

## 직원이 실물에서 만날 자리

- **dev · prod 서버**(W2): 채팅 글은 되지만 사진 · 동영상은 「저장소 꺼짐」 409 이고, 채팅 푸시는 오지 않는다. 앱에서 「사진을 보낼 수 없음」으로 보인다.
- 로컬(사용자가 `local.env` 를 채우면): 첨부 · 푸시 가능. 실 APNs · 실 Blob 은 미실행이다.
- 드물게(W1): 앱을 앞으로 가져오거나 재연결한 직후 1–2초 안에 온 메시지가 다음 재연결 전까지 안 보일 수 있다.

## 미검증 · 정직 기록

- 실 APNs 키 · 실기기 발송 · Azure Blob 실물 · 로컬 day-local(11040) E2E 는 아무도 실행하지 않았다(보고서도 같음).
- HTTP 20 · 기기 · 첨부 · APNs 재시도 · 멱등 · 잠금은 이번에 깊이 재검수하지 않았다. 집중 테스트 88건 재실행으로 통과만 확인했다.
- 범위 밖 · 후속: `day_vm.py` 비밀 경로(W2 · W3)와 컨테이너 disk 마운트(보고서 미실행 4).

## 파일 경계

- 서버 변경 42개의 sha256 은 `chat-backend-review-logs/file-hashes.txt` 에 있다. 커밋 전에 이 목록으로 동일성을 대조하면 된다.
- `app/` 은 제외했다.
