# chat-backend 코드 결과 보고 — Delivery #235 v7 서버(직원 채팅 · 기기 등록 · 채팅 APNs)

## 상태: done (코드 · 로컬 스크래치 PG/Redis E2E 통과) — 커밋 · push · PR · 머지 · 하위 위임 없음

- 작업 tree `CENTURION_DAY/day-app` · branch `kknaksss/day-app` · 기준 HEAD `b6c034bf`(origin/dev `91728737` 와 차이 0 재확인).
- 계약 = SPEC `53adbd49` 의 004 · 000(device 개정) · 003(§3 푸시) · 001 · WP v7(plan `sha256:22f86376…`). SPEC-005 범위는 구현하지 않음.
- app/ 은 손대지 않음(앱 워커 변경은 그대로 둠). 사용자 day-local 컨테이너 · 11040 포트 · 업무 스키마 · 실 env/키 변경 0.

## 수행 — 파일

| 구분 | 파일 |
|---|---|
| 라우터 | `backend/day/routers/api/chat.py`(HTTP 20 + `GET /api/chat/stream`) · `routers/api/devices.py`(PUT/DELETE) · 조립 `day/public.py::api_routers` |
| 서비스 | `services/chat.py`(업무 · 잠금 · 멱등) · `chat_events.py`(Redis pub/sub) · `chat_storage.py`(디스크/Blob) · `chat_push.py`(받는 사람 · 기기 · push_log · 재시도) · `apns.py`(HTTP/2 · ES256) · `devices.py` |
| 조회 · 계약 | `queries/chat.py`(묶음 조회 · N+1 없음) · `schemas/{chat,devices}.py` · `errors.py`(ChatError + 원문 글자) · `enums/misc.py`(DevicePlatform · PushEnv) |
| 모델 · migration | `models/misc.py`(Device 5칸 · 비유일 인덱스) · `models/task.py`(EventLog Index — 옆 원천과 파일 동일) · `migrations/versions/20261110_0006_event_log_visit_type.py`(옆 원천 byte 그대로 · sha256 `fb035182…0739` 일치) · `20261110_0007_chat_device.py`(신규) |
| 태스크 | `day/tasks/chat.py`(`day.chat.send_push`) · `day/tasks/__init__.py` 등록 |
| 설정 · 배포 | `common/config.py`(채팅 · APNs 설정만) · `deploy/compose.local.yaml`(api/worker/scheduler 전달 8줄) · `deploy/local.env.example` · `deploy/config/{dev,prod}.env`(비밀 아닌 이름만 · 빈 값) |
| 의존성 | `pyproject.toml` · `uv.lock`: `python-multipart 0.0.33` · `h2 4.4.1` · `pyjwt[crypto] 2.15.1` · `azure-storage-blob[aio] 12.31.1`(azure-core 1.41.0 · aiohttp 3.14.5) |
| 테스트 | `tests/day/chat/`(conftest · units 37 · api 16 · concurrency 6 · attachments 8 · stream 6 · devices_push 10 · queries 2) · `tests/day/test_chat_device_schema.py` · `tests/migrations/test_chat_device_migration.py` · `tests/deploy/test_chat_env_contract.py` · 기존 갱신 `test_column_snapshot`(device 5칸) · `test_enum_labels`(28→30) · `test_alembic`(HEAD=0007) |

## API 별 구현 (원천 = cc-prototype `77173cf8` `procedure/back/app/{api,schemas,service}/chat.py` · `service/push.py` · `push/apns.py` — 동작·오류 차례·글자 이식, repo 층 복사 없음 · 서비스가 SQLAlchemy 직접)

| # | 경로 | 핵심 |
|---|---|---|
| 1 | GET /people | 세션 병원 활성 직원(staff 활성 · 시스템 아님 · account 있음·활성) · 나 제외 · 이름 순 · 비밀번호/직무/board 권한 무관 |
| 2 | GET /rooms | 보이는 방(숨김 + 새 메시지면 다시) · 최근 순 · `unreadRooms` · Room에 `fromSeq` · `lastReadSeq` |
| 3 | POST /rooms/direct | `direct_key` 「작은:큰」 병원별 · 동시 생성 23505 → 트랜잭션 재시도 · 숨김 풂 |
| 4 | POST /rooms | 다른 사람 2~19 · 제목 trim 40 · 초대 시스템 줄 원문 · 푸시 없음 |
| 5 | POST /rooms/{id}/members | 그룹만 · ≤20(409 chat_room_full) · 재초대 = 경계(from_seq) 새로 |
| 6 · 7 · 8 | leave(그룹만) · hide(1:1만) · mute | 원문 code/글자 · 이벤트(chat_room_removed / chat_room 나만) |
| 9 · 10 | GET messages · attachments | `beforeSeq` · `since`(updated_at ≥, 지운 것 포함) · 둘 다 400 · limit 50/60 · 경계 밖만 |
| 11 | POST messages | 방 행 FOR UPDATE → seq+1 · last_message_at · 보낸 사람 읽음 한 tx · 시각 = 잠금 뒤 `clock_timestamp()` |
| 12 · 13 | PATCH · DELETE messages | 오류 차례 404→403→400 · 같은 글 200 무이벤트 · 소프트 삭제 · 파일은 마지막 참조일 때 커밋 뒤 삭제 |
| 14 | POST forward | 1~10 · 중복 400 · 대상별 결과(savepoint) · 같은 방 두 번 = 앞 결과 · 첨부 새 행 · 같은 파일 |
| 15 | POST read `{seq}` | `GREATEST(cur, LEAST(seq, last_seq))` 원자적 · seq 0 무변경 · chat_read 나만 |
| 16~20 | photos · videos 업/다운 · thumbnail | JPEG `FFD8FF` · MP4 `ftyp` · 5MB/90MB/1~180000ms · 본문 바이트 수로 끊는 bounded read(413) · Bearer · no-store · inline · Range 206/416 · HEAD · Content-Length |
| 21 | GET /stream | 채널 (병원, 계정) · 이벤트 6종 · **이벤트마다** + 10초마다 세션 생존·활성 직원 재확인 → `session_expired`(코드) 후 종료 · 1시간/만료 · 15초 ping · 연결 직후 재전송 없음 |
| — | PUT/DELETE /api/devices/{install_id} | 서버 세션 결속 · 늦은 이전 세션 PUT 무시(created_at, id 고정 순서) · 토큰 이름공간 advisory 잠금으로 연결 하나 · 다른 topic/env 불변 · DELETE 는 요청 세션 결속일 때만 · app_id 허용 목록(비면 전부 400) · 토큰 암호문 저장 |

## 동시성 · 멱등 (실제 PG 증명)

- seq: 15건 동시 보내기 → 2..16 빈틈·중복 0 · updated_at 순서 = seq 순서.
- clientId: 같은 계정·clientId 6건 동시 → 메시지 1 · 푸시 발행 1. **지운 행 포함** 조회 = (계정, clientId) `pg_advisory_xact_lock` 안(DB 유일 색인은 살아 있는 행만이라 그대로 둠 — §2 관례 · 기존 테스트 유지). 지운 뒤 재전송 = 처음(지운) 행 · 새 메시지/이벤트/푸시 0.
- 1:1 동시 6건 → 방 1 · 멤버 2. 동시 초대 → 정원 20 넘지 않음(200 + 409). 읽음 동시 → 단조.
- 첨부: 붙이기 = 첨부 행 FOR UPDATE(한 번만) · 삭제/전달 = 파일 키 advisory 잠금 안에서 살아 있는 참조 세기 → 경합 4회 모두 「파일 없는 전달본 0」 · 남은 파일 수 = 살아 있는 첨부 수.
- 잠금 순서 방 → 메시지 → clientId/파일 · 엇갈린 전달 교착(40P01)·23505 는 트랜잭션 통째 재시도 3회. 한 AsyncSession 동시 task 공유 0.
- N+1: 방 목록 · 메시지 목록 쿼리 수가 방/메시지 수와 무관(query-count 테스트).

## 채팅 푸시

받는 사람 = 경계 밖 지금 멤버 − 보낸 사람 − 알림 끔 − 방 병원 활성 직원 아님(커밋 뒤 worker 가 다시 읽음). 기기 = 결속 세션 살아 있음 · 세션 병원 = 방 병원 · 계정 일치 · platform/app_id(현재 허용 목록)/push_env 있음 → 옛 null 행 · 로그아웃 · 다른 병원 세션 0(테스트). 본문 SPEC 그대로(`thread-id` · environment · hospitalId · 1일 만료). notification 행 0 · push_log(kind chat · token_tail). 키 없음 = `skipped_no_key`. 재시도/죽은 토큰 = 프로토 push.py:28-31 · 286-306 그대로 · 결속 해제는 `login_session_id` 비움(보낸 시점 세션 + 토큰 해시가 같을 때만 — 그 사이 재등록 보존 테스트). 중복 발송 0 = Redis 표지 + push_log 존재 확인. 동시 상한 `DAY_APNS_CONCURRENCY` · 요청 timeout · `aclose` finally.

## 검증 — 실명령 · 수치 (증거 `chat-backend-evidence/`)

| 명령 | 결과 |
|---|---|
| `uv run pytest -q -m "not infra"` | **539 passed**, 216 deselected (기준선 496 → +43) |
| `DAY_ENV_FILE=…/CENTURION_DAY/deploy/local.env scripts/test.sh -q`(전체 · infra 필수) | **755 passed, 0 failed**, 1 warning(기존 TestClient deprecation) · 53.75s |
| 같은 하네스 · chat + migrations + env 계약만 | 100 passed |
| `uv run pytest -q backend/tests/architecture` | 27 passed |
| `uv run ruff check backend` · `ruff format --check` | All checks passed · 184 formatted |
| `alembic heads` | `0007_chat_device (head)` 하나 · test_alembic upgrade/downgrade base/다시 upgrade · `alembic check` 차이 0 · offline SQL 통과 |
| `docker compose -f deploy/compose.local.yaml --env-file <가짜 값> --profile app config` | api·worker·scheduler 모두 채팅 키 전달(컨테이너 기동 없음 · `compose-chat-env.txt`) |
| 0006 sha256 | `fb0351828664…0739` = 옆 원천(a1c90b9d · 옆 head caa72435 도 동일 · 0007 없음) |

테스트 하네스: `day_test` 스키마 + Redis db15 만(DAY_ENV_FILE source 만 · 값 출력 0). 실행 전 다른 pytest 프로세스 없음 확인. 중간에 내 SSE 테스트 한 건이 hang → **원인 = httpx ASGITransport 가 끝없는 StreamingResponse 본문을 다 모으려 함**(코디 지적과 동일). 내 프로세스만 종료 · 테스트를 라우트 함수 직접 호출 + 첫 청크만 읽도록 교체 · 운영 수명/deadline 변경 0 · 실제 Redis generator 테스트 유지(6 passed).

## 기존 회귀

board API/SSE · 원장 호출 · emr · 웹 화면 · login 코드 무변경. 기존 663→ 전체 755 중 기존 테스트 전부 통과(스냅샷 device 5칸 · enum 수 · alembic HEAD 만 기대값 갱신).

## 설정 키 (값은 사용자) · fail-closed

`DAY_CHAT_STORAGE`(disk|blob · 빈 값=꺼짐 → 첨부 409 photo_disabled) · `DAY_CHAT_STORAGE_DIR` · `DAY_CHAT_BLOB_CONTAINER` · `DAY_CHAT_BLOB_CONNECTION_STRING`(비밀) · `DAY_APNS_AUTH_KEY`(비밀 · .p8 PEM, 한 줄이면 `\n`) · `DAY_APNS_KEY_ID` · `DAY_APNS_TEAM_ID`(셋 중 하나라도 빔 → skipped_no_key) · `DAY_APNS_ALLOWED_APP_IDS`(빔 → 기기 등록 400) · 선택 `DAY_APNS_TIMEOUT_SECONDS` · `DAY_APNS_CONCURRENCY` · `DAY_CHAT_PUSH_KICK_TIMEOUT_SECONDS`. 단위 테스트로 fail-closed 확인.

## 미실행 · 사용자 후속 (정직 기록 — 코드 완료와 구분)

1. 실 APNs 키 · Apple App ID/Push · 실기기 발송 = 미실행(APNs 는 HTTP 경계 더블 + MockTransport 로 헤더·ES256 서명만 검증).
2. Azure Blob 실물 = 미실행(SDK 경계 더블 · API 시그니처는 설치본 + 공식 문서 확인).
3. **서버 비밀 연결 범위 밖**: Key Vault → app.env 는 `scripts/deploy/day_vm.py::SECRETS`(필수 목록)가 정한다 — code_surface 밖이라 안 건드림. 지금 서버는 채팅 첨부/푸시가 꺼진 상태(fail-closed)로 뜬다. 켜려면 선택 비밀 2개(`blob-connection-string` · `apns-auth-key` 류) 지원을 별도 승인으로 추가 필요.
4. 로컬 컨테이너에서 `disk` 저장소는 쓸 수 있는 마운트 폴더가 필요(Dockerfile `USER day` · code_surface 밖이라 볼륨 추가 안 함). 호스트 `uv run` api 는 임의 폴더 가능.
5. 로컬 day-local 실물 E2E(사용자 서비스 · 11040)는 하지 않음 — 스크래치 하네스 E2E 로 대신.

## 구현 선택 (SPEC 이 정하지 않은 곳 — 코디 확인 요청)

- 같은 clientId 가 **다른 방**에서 다시 오면(실사용 거의 없음 · UUIDv4) 처음 행이 그 방이 아니므로 404 `chat_message_not_found`(새 메시지 0).
- `Person.role` = `{key: 첫 태그 | null, name: job_role.name}` · 직무 없으면 `role: null`(OQ-C3 기본값).
- 시각 = UTC 오프셋 `+00:00` · 밀리초(ISO 8601).
- 1:1 `name` = 상대 이름 + 비활성이면 `" (비활성)"`(프로토 서버 :58-66 그대로 — 앱이 또 붙이지 않게 앱 워커 확인 필요).
- 경로 id 가 uuid 아님 = 그 대상 404 code · 기기 install_id 형식 밖 = 400.
- `ForwardFail.roomId` = 사람 대상이 방을 못 열면 null(프로토 동일).
- 죽은 토큰 해제 = `login_session_id` 비움(deleted_at 아님).

## 앱 워커 전달 사항

- 스트림 = `GET /api/chat/stream`(Bearer) · `event:` 이름 6종 + `session_expired`(data = 코드) · data 는 JSON 한 줄 · `retry: 3000` · 15초 `: ping`.
- 읽음 응답/이벤트 칸 `lastReadSeq` · `lastViewedAt` · `unreadRooms` · 삭제 이벤트 `{roomId, messageId, seq, updatedAt}`.
- 업로드 multipart 칸 이름 = 프로토 그대로(roomId · photo · video · thumb · width · height · durationMs). 응답 id = uuid 문자열.
- 기기 PUT 본문 = SPEC-003 그대로(snake_case). 허용 app_id 가 서버 env 에 없으면 400 → 앱은 조용히 무시(SPEC).

## SPEC-005 후속이 재사용할 공통 경계 (지금 알림함/원장 호출 trigger 추가 0)

- 기기: `day/services/devices.py`(`register` · `unregister` · `token_hash` · `check_app_id`) — 결속 규칙 전부 여기.
- APNs: `day/services/apns.py::ApnsClient.send(token, topic, push_env, payload, expiration) → ApnsResult` — kind 무관.
- 대상 기기 판정 + 로그 + 재시도/죽은 토큰: 현재 `chat_push.py` 안(`deliveries` 의 기기 쿼리 · `_send_with_retry` · `_dead` · `_log` · 결속 해제). 005 에서 kind 를 넓힐 때 이 기기 쿼리/발송부를 공용 모듈로 빼는 것이 자연스러움(지금은 채팅 kind 만).
- 설정명: `DAY_APNS_*` 공용 · 태스크 이름 `day.chat.send_push`(외부 계약).

Sources(문서 확인): [Apple — Communicating with APNs](https://developer.apple.com/library/archive/documentation/NetworkingInternet/Conceptual/RemoteNotificationsPG/CommunicatingwithAPNs.html) · [azure.storage.blob.aio.BlobClient](https://learn.microsoft.com/en-us/python/api/azure-storage-blob/azure.storage.blob.aio.blobclient?view=azure-python)
