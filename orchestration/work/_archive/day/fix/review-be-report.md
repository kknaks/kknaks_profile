# 리뷰 리포트 — fix 서버 WP-BE-1(채팅 · 알림) · WP-BE-2(통역) / code (2026-11-11)

검수 대상: `CENTURION_DAY/fix`(`kknaksss/fix`) 의 `app/` 밖 미커밋 변경 — 고친 25파일(+551 −24) + 새 파일 19(`day/services/interpret/*` · `routers/api/interpret.py` · `services/glossary.py` · `dtos/glossary.py` · `seed/glossary.json` · `tests/day/interpret/*` · `scripts/interpret_live_check.py`). 작성자 아님 · read-only · Soniox · KOS · 서버 호출 0.
원천 대조: interpret-pwa `origin/main` `17c26b5`(`git show` 로만).

## 판정: WARN

FAIL 0 · WARN 1 · 참고 7.
- 통역에서 원천과 로직이 달라진 곳은 `session.py` 한 파일뿐이고, 달라진 줄마다 스펙 근거가 있다.
- 동시 세션 자리는 모든 종료 경로에서 한 번만 반납된다.
- 인증은 accept 전 · DB 세션을 닫은 뒤 끝난다.
- 깨진 시드는 api 프로세스만 멈춘다(worker · scheduler 무관).
- 채팅 · 알림 계약 · 배포 설정(값 줄 diff 0) · 의존성 · 범위에 문제가 없다.

## FAIL

없음.

## WARN

### W1. 접근 로그에 쿼리 문자열이 그대로 남는다 — 원천의 `DropQueryString` 을 옮기지 않았다(작성자 보고 1)
- 근거: AGENTS.md 「백엔드 안전 기준」(로그에 비밀 금지) · 원천 `back/app/main.py:28-59`(`DropQueryString` 필터를 uvicorn 로거에 단다). DAY `backend/common/logs.py` 는 `uvicorn.access` 를 루트로 올리기만 하고(`_OWN_HANDLER_LOGGERS`) 쿼리를 지우지 않는다. `deploy/compose.yaml:42-52` 는 접근 로그를 켠 채(`--no-access-log` 없음)다.
- 판정: **넣는 것이 맞다.** 다만 통역만의 문제가 아니다.
  - DAY 의 어느 경로도 `?token=` 을 받지 않는다(`grep query_params` = `routers/api/chat.py` 의 `since` · 페이지 칸뿐).
  - 그래도 잘못 붙는 클라이언트가 쿼리에 Bearer 세션 토큰을 실으면, 그 토큰은 헤더로 쓰면 **살아 있는 자격**이고 JSON 로그(Docker `json-file`)에 평문으로 남는다.
  - 같은 위험은 `/api/board/stream` · `/api/chat/stream` · `/api/notifications/stream` 등 모든 경로에 똑같이 있다.
- 고칠 방향: `common/logs.py` `configure_logging` 에서 `uvicorn.access` 로거에 쿼리 지우기 필터 하나(원천 `DropQueryString` 모양 — `record.args` 의 경로에서 `?` 뒤를 뺌) + 시험 1건. 통역 라우터 쪽이 아니라 **공용 로그 한 곳**에 둔다. 스펙에 없는 동작 변경이 아니라 로그 모양만 바뀌므로 이번 PR 에 넣어도 되고, 따로 작은 PR 로 해도 된다(코디 판단).

## 원천 대비 달라진 줄 표

비교 방법: docstring 을 빼고 import 경로(`app.service.*` → `day.services.*`)를 맞춘 뒤 AST 를 다시 써서 diff 했다(줄 길이 · 포매팅 차이 제거). 시드는 sha256 으로 비교했다.

| 파일 | 결과 | 달라진 것 · 스펙 근거 |
|---|---|---|
| `services/interpret/assembler.py` | **AST 동일** | — |
| `services/interpret/chinese.py` | **AST 동일** | — |
| `services/interpret/langs.py` | **AST 동일** | — (env 덮기 `GLOSSARY_CONTEXT_MAX_CHARS` 는 원천에서도 `config` 쪽 — DAY 는 그 config 를 옮기지 않음 · 주석으로 적음) |
| `services/interpret/soniox.py` | **AST 동일** | — (`CONNECT_TIMEOUT` 10초 · `{"keep_alive": true}` 원천 그대로) |
| `services/glossary.py` + `dtos/glossary.py` | **AST 동일**(합치면) | 값 클래스 4개(Entry · Term · Glossary · ContextParts)를 `dtos/` 로 옮겼다 — 로직 같음(AGENTS 「dtos/」) |
| `seed/glossary.json` | **바이트 동일** | sha256 `e2734936…` 원천 `git show` 값과 같음 |
| `services/interpret/session.py` | 다름(아래 8곳) | |
| ↳ `Recorder` import · `recorder` 인자 · `record` · `_end_code` · `record.start/caption/end` 제거 | 기록기 제거 | SPEC-003 §3 「통역」 「기록 없음」(OQ-A41 · 비교 표 `:692` 근처) |
| ↳ `_error(…, final=…)` 인자 제거 · `final=False` 두 곳 | 기록기 종료 코드용 인자만 없어짐 · 보내는 프레임 같음 | 위와 같음 |
| ↳ `Slot` · `Slots` 클래스 | 동시 세션 자리 | SPEC-003 `:663` · `:692`(서버 전체 6) |
| ↳ `slots` · `max_sessions` 인자 · `self.slot` | 위와 같음 | 같음 |
| ↳ `run()` 키 확인 **뒤** `try_acquire` → 없으면 `session_limit` | 순서 = start → 키 → 자리 → STT | SPEC-003 `:648` |
| ↳ `MSG_SESSION_LIMIT = MSG_NO_API_KEY`(「통역 서버를 쓸 수 없어요」) | 새 문구 없음 | SPEC-003 `:636` · OQ-A43 |
| ↳ 키 없음 로그 `SONIOX_API_KEY 가 비어 있다` → `speech provider key is not configured` | env 이름을 로그에서 뺌 | 브리프 · AGENTS 로그 규칙 |
| ↳ `_cleanup` 을 `try/finally` 로 감싸고 `finally` 에서 `slot.release()` | 반납 한 곳 | SPEC-003 `:663` 「어떤 경로로 끝나도 한 번만」 |
| `routers/api/interpret.py` | 다시 씀 | 원천의 `?token=` · `Origin` · 로그인 계정 → DAY 헤더 Bearer + `board` view(SPEC-003 §3 「통역」 「인증」 · A-14b · OQ-A40) |
| `services/interpret/service.py` | 다시 씀(원천 `container.py` 통역 부분) | 기동 적재 · 7개 context 미리 만듦(I-4 허용) · `authorize` |

작성자의 「원천 그대로(줄 길이 · 머리만 · 로직 같음)」 보고는 **참이다**.

## 자리 반납 경로 표

자리는 `run()` 의 바깥 `try` 안에서만 잡고(`session.py:184-189`), 그 `try` 의 `finally` 가 늘 `_cleanup()` 을 부른다(`:213-214`). `_cleanup` 은 자기 `try/finally` 의 `finally` 에서 반납한다(`:430-433`). `Slot.release` 는 두 번째부터 아무것도 하지 않고(`:31-34`), `Slots._release` 는 `max(0, …)` 다.

| 경로 | 코드상 흐름 | 반납 | 시험(`tests/day/interpret/test_interpret.py`) |
|---|---|---|---|
| 정상 stop | `_client_reader` stop → `_pump` drain → `run` finally | 1 | `test_session_limit_default_six…`(정리 뒤 돌아옴) 외 |
| `start` 전 앱 닫음 · `start` 틀림 · 10초 | 자리 잡기 **전** return | 잡지 않음 | `test_bad_start` · `test_start_timeout_bad_request` |
| 키 없음 | 자리 잡기 **전** return | 잡지 않음 | `test_no_api_key_does_not_open_soniox_or_take_slot` |
| 7번째 | `try_acquire` = None → `session_limit` → return | 잡지 않음 | `test_session_limit_default_six_seventh…` · `…follows_setting` |
| STT 열기 실패 | `except Exception` → `soniox_unavailable` → return → finally | 1 | `test_error_codes_close_1000_and_no_leak` |
| TTS 열기 실패 | 같음 | 1 | `test_slot_returns_on_tts_open_failure` |
| 설정 재시도 중 예외 | `_open_stt_checked` 두 번째 열기 · 확인 예외 → 같음 | 1 | `test_slot_returns_on_exception_during_config_retry` |
| ready 뒤 Soniox 끊김 | `_stt_reader` 가 `SonioxError` → `_pump` except → `run` finally | 1 | `test_slot_returns_when_soniox_drops_after_ready` |
| 앱이 닫는 프레임 없이 사라짐 | `receive()` = disconnect(실서버는 uvicorn ws ping 20/20 이 감지) → `"close"` → `_pump` 끝 → finally | 1 | `test_slot_returns_when_app_vanishes_without_close_frame`(중간 `in_use == 1` 확인) |
| 서버 작업 취소 | `CancelledError` 가 `run` finally → `_cleanup` finally | 1 | `test_slot_returns_when_server_task_cancelled` |
| Soniox 연결 중 취소 | 같음(`open_stt` await 중) | 1 | `test_slot_returns_when_cancelled_during_soniox_connect`(중간 `in_use == 1`) |
| `_cleanup` 안에서 다시 취소 | 안쪽 `finally` 가 반납 | 1 | 직접 시험 없음(구조로 보장) — 참고 R1 |
| accept 뒤 · `run` 전 예외 | `current().session(…)` 은 설정만 읽음 · 자리 없음 | 잡지 않음 | — |
| 두 번 반납 · 음수 | `Slot` 이 자기 참조를 비움 · `max(0)` | — | `test_slot_release_is_once_and_never_negative` |

- 프로세스 안 셈 = 서버 전체: `deploy/compose.yaml:50-51` api `--workers 1` · `common/config.py` 주석과 같다. worker · scheduler 는 통역 라우터를 돌리지 않는다.
- 작성자의 「반납 줄을 끄면 10개 실패」 변이 주장은 검증하지 못했다(파일 수정 금지). 다만 위 시험 중 2개는 반납 **전** `in_use == 1` 을 확인하므로, 반납을 끄면 실패하는 구조다.

## 인증 · 권한

- 순서(`routers/api/interpret.py:56-61`): 헤더 Bearer 만 → `interpret.authorize()`(`service.py:136-157`) — `get_async_session()` 안에서 `sessions.current_session(…, "bearer", now)`(로그아웃 · 만료 · 없는 토큰 = `ServiceError`) + `require_permission(board, VIEW)`(세션 병원 범위 · 전체 권한 계정 포함) → `async with` 가 끝나 **DB 세션을 닫은 뒤** True → 그 다음 `accept()`. 실패면 accept 없이 `close(1008)`(앱엔 핸드셰이크 403).
- 다른 병원: 권한은 세션의 병원 범위로만 본다. 다른 병원 세션 토큰은 그 세션 병원의 `board` 권한으로 판정된다(SPEC-003 §3 「통역」 「인증」과 같음).
- `day.public.run_interpret_session`(`public.py:99-107`): HTTP 라우터 · `day/routers` 어디서도 import 하지 않는다(`grep` — `scripts/interpret_live_check.py` 만). 「라우트가 핸드셰이크를 본 뒤와 같은 길」을 스크립트에 여는 것이라, `scripts` 는 `day.public` 만 쓰는 관례상 **경계를 넓힌 것이 맞다**. 참고 R4.
- (작음) `authorize` 에서 DB 연결 자체가 실패하면(`ServiceError` 가 아님) 예외가 그대로 올라가 1008 대신 핸드셰이크 500 이다. 앱은 같은 「연결 안 됨」 갈래로 보므로 계약 위반은 아니다 — 참고 R5.

## 비밀 · 로그 (`grep log\.|logger\.` 통역 · 사전 · 라우터 전부)

| 자리 | 싣는 것 | 판정 |
|---|---|---|
| `session.py:177` | 예외 **이름**만 | OK |
| `session.py:181` | 고정 문장(env 이름 없음) | OK |
| `session.py:187` | 상한 숫자 | OK |
| `session.py:199-204 · 226` | `channel` · `error_type` · `request_id` | OK |
| `session.py:208 · 298` | 예외 이름 | OK |
| `session.py:238` | 언어 · 칸 수 · 글자 수(용어 문자열 0) | OK |
| `session.py:295` `_error_state` | 채널 · Soniox `error_message`(`{e!s}`) · 상태 · 길이 · 몇 초 전 — 발화 원문 · 키 0 | OK(원천과 같음) |
| `soniox.py:182` | Soniox `error_message` | OK(원천과 같음) |
| `service.py:86 · 114` | 칸 수 · version · 시간 | OK |
| `service.py:110` | `SeedError` 문장(규칙 · 경로 · term id — 원천 lifespan 과 같은 줄) | OK |
| `service.py:143 · 154` | 거절 `code` 만 | OK |
| 오류 프레임 `message` | 고정 글자 4종(받은 값을 되돌려 보내지 않음 · `:335-337` 주석) | OK |
| `chat.py` rename 로그 | room id · account id 만(이름 없음) | OK |
| uvicorn 접근 로그 | 쿼리 그대로 | **W1** |

## 루프 · 시간 상한 · 자원

- 시드 검사 + 7개 context 조립은 기동 때 한 번이다(작성자 실측 약 42ms). 세션 중 사전 줄이기 · OpenCC context 변환은 없다. 자막 OpenCC 변환은 발화마다 동기로 돌지만 원천 그대로이고 짧은 문자열이다(I-4 허용).
- 상한: `start` 10초(`wait_for` · `:172`) · Soniox 연결 10초(`open_timeout`) · 설정 확인 2초 · stop drain(`STOP_DRAIN` · `shield` + `wait_for`) · 연결 닫기 3초(`_close_conn`) · websockets ping 20/20 · uvicorn ws ping 기본값.
- 세션당 태스크 4개(`reader` · `stt` · `tts` · `keep`)는 `_pump` 의 `finally` 에서 전부 `cancel` + `gather`(`:300-303`). `_stt_first` 는 `_cleanup` 이 취소한다.
- 삼키는 `except`: `_error`(보내기 실패 — 끝나는 길) · `_keepalive`(keepalive 실패 — 다음 읽기가 오류를 냄) · `_close_conn` · `client.close` — 모두 원천 그대로이고 정리 · 끝 경로뿐이다. 업무 결과를 삼키는 자리는 없다.
- 참고 R1: `_cleanup` 이 STT 를 닫는 중에 취소되면 TTS `close` 는 불리지 않는다(자리는 반납됨). 원천과 같은 구조이고, 서버 종료 · 강제 취소 때만 생긴다.

## 기동

- `runtime/main.py` 는 `day.public.load_interpret` 만 import 한다(경계 유지 · `tests/architecture` 통과 — 작성자 28 passed, 내 실행 전체에 포함).
- lifespan 은 api(`runtime.main:create_application`)에만 있다. `runtime/worker.py` · `scheduler.py` 는 lifespan · `load_interpret` 를 부르지 않는다(`grep`) → **깨진 시드는 api 만 멈춘다. 동기화 · 푸시 worker 는 영향 없다.** 스펙(`:673` 「api 기동 때」)과 같다.
- 이미지: `deploy/Dockerfile:16` `COPY backend ./backend` · `.dockerignore` 에 `*.json` · `seed/` 제외 없음 · `git check-ignore` = 무시 아님 → 시드가 이미지에 들어간다. `SEED_PATH` = `services/interpret/service.py` 기준 `parents[2]/seed/glossary.json` = `backend/day/seed/glossary.json`.
- 위험(작성자도 적음): 깨진 시드 = api 전체(로그인 · 시술현황 · 채팅) 기동 실패. 시드가 바이트 그대로이고 `test_seed`(not infra)가 같은 검사를 하므로 CI 에서 먼저 걸린다.

## 채팅 · 알림 (BE-1)

- **#22** `services/chat.py:642-673` · `routers/api/chat.py:199-209` · `schemas/chat.py:36-42`.
  - 그룹만(`chat_group_only` 400).
  - `_room_for(lock=True)`(`:211-224` — 세션 병원 · 지금 멤버 · `left_at` 없음, 아니면 404 · `with_for_update` 방 행 잠금).
  - 앞뒤 공백 뺀 뒤 40자(`len` = 코드포인트) · 빈 값 = None · 같은 이름 = 이벤트 없이 200.
  - 바뀌면 `title` 만 고치고 `last_message_at` · `seq` · 안 읽음 · 시스템 줄은 건드리지 않는다.
  - 커밋 **뒤** `_Out(view, events)` 로 `chat_room` 을 지금 멤버 전부에게 보낸다.
  - 스펙 `:349` 와 같다. (작음) 41자 검사가 `actor()`(403) **앞**이라 비활성 직원의 41자 요청은 403 대신 400 이다 — 참고 R6.
- **`chat` 받는 종류** `notifications.py:216-242`: `_chat_active` = `chat.actor()` 를 그대로 부르고 `Forbidden` 이면 False → **채팅 403 판정과 한 곳**. 차례 `doctor_call` → `chat` · 저장 없으면 `True`(`:258`) · 받는 종류 아니면 PUT 400 `setting_not_allowed`(`:266`).
- **푸시 받는 사람** `chat_push.py:66-77 · 109-112`: 방별 `is_muted` 로 먼저 거르고, `notification_setting(kind='chat', is_enabled=false, deleted_at null)` 계정을 뺀다 → 4조합(켬/켬 = 받음 · 나머지 셋 = 안 받음). 원장 호출 푸시는 `kind == doctor_call` 만 본다(`notifications.py:336-337`) → 영향 없음.
- **migration 없음** 주장은 참이다: `notification_setting.kind` = `String` · `OPEN_ENUM`(`models/misc.py:115`) · PK `(account_id, kind)` · CHECK 없음 → `'chat'` 을 그대로 저장한다. `migrations/` 무변경.
- 시험: `test_채팅_전체_알림_끈_계정은_받는_사람에서_빠지고_방별_알림과_OR` · `test_이름_바꾼_뒤_푸시_제목은_발송_때_읽은_새_이름` · `test_설정은_원장이면_doctor_call_채팅_활성_직원이면_chat` · `test_설정_시스템_계정_비활성_직원은_빈_목록` + `test_chat_api.py` #22 — 전부 `infra`(내 실행에선 deselect).

## 배포 설정 · 의존성

- `deploy/config/dev.env` · `prod.env`: `git diff -U0` 에서 `#` 아닌 `+/-` 줄 **0** — 주석 3줄씩만 더했다.
- `scripts/deploy/day_vm.py:51` `DAY_SONIOX_API_KEY: soniox-api-key` 한 줄 → `FORBIDDEN_CONFIG_KEYS = {*SECRETS, *OPTIONAL_SECRETS, …}` 에 자동으로 들어간다 · `MULTILINE_SECRETS` 아님(한 줄 값) · 없으면 404 건너뜀(기존 `read_optional_key_vault`).
- `deploy/compose.local.yaml`: `DAY_SONIOX_API_KEY:-` · `DAY_INTERPRET_MAX_SESSIONS:-6`(빈 문자열이면 int 검사가 실패하므로 기본 6 — 작성자 4번). 서버 `compose.yaml` 무변경(env_file 로 실림 · 상한은 코드 기본값).
- `pyproject.toml`: `opencc-python-reimplemented>=0.1.7,<0.2` · `websockets>=15,<18` 두 줄. `uv.lock` 변경 = 그 둘의 의존 목록 · 명세 + `opencc-python-reimplemented 0.1.7` 패키지 블록 하나뿐이다(`websockets` 는 이미 잠겨 있던 17.4 그대로 · 다른 패키지 버전 변경 0).

## 작성자 5건 판정 (be-2 「스펙과 달라진 곳 · 물을 것」)

| # | 내용 | 판정 |
|---|---|---|
| 1 | uvicorn 접근 로그 `?token=` | **넣어야 한다** — W1. 공용 `common/logs.py` 에 · 모든 경로 대상 |
| 2 | `day.public.run_interpret_session` 추가(계획 표 밖) | **받아들임** — HTTP 경로 없음(`grep`) · scripts 는 `day.public` 만 쓰는 관례. 이름 · 문서로 「인증 없음 · 스크립트 전용」이 드러나 있다. 참고 R4 |
| 3 | `dtos/glossary.py` 가 `services/interpret/langs.APP_LANGS` 를 읽음 | **고치길 권함(작음)** — dtos 가 services 를 import 하는 역방향이다. 경계 시험은 `day` 안쪽이라 통과한다. `entry_counts(langs)` 로 인자를 받게 하면 끝. 참고 R3 |
| 4 | compose 상한 `:-6`(계획은 `:-`) | **맞다** — 빈 값이면 `Field(int)` 검사로 기동이 실패한다. 예시 env 를 주석으로 둔 것도 같은 이유 |
| 5 | 계획 ↔ 스펙 충돌 없음 | 확인 — 나도 찾지 못했다 |

## 조용히 통과하는 자리

1. **BE-1 시험 전부 · 통역 인증 2건은 `infra`** — `-m "not infra"` 에서 294건 deselect. 내 실행 842 + 294 = 1136 으로 작성자의 「격리 스택 전부 1136 passed」 와 **수가 맞는다**(못 믿을 근거 없음). 다만 이번 검수에서 4조합 · #22 잠금 · 받는 종류는 **실행으로 확인하지 못했다** — 머지 전 코디가 `scripts/test.sh -q` 한 번(격리 스택).
2. `test_configs`(Soniox URL · 모델 · keepalive 상수 고정)는 기대값이 구현 상수를 베낀 시험이다. 원천과 AST 가 같다는 것이 이번 근거이고, 시험은 이후 바뀜을 막는 몫이다(괜찮음).
3. 가짜 Soniox 시험은 「Soniox 가 이렇게 굴면 앱에 무엇이 가나 · 자리가 몇 개인가」를 본다. 가짜가 구현을 흉내 내 늘 통과하는 구조는 아니다(반납 전 `in_use == 1` 중간 확인 2건).
4. **`scripts/interpret_live_check.py` 의 seed 갈래는 고친 뒤 한 번도 돌지 않았다**(작성자 pending — 「무음 1초 뒤 stop」으로 고친 대본). 커밋되는 스크립트의 그 갈래는 실행 확인이 없다. A-45 판정(7개 언어 ready)은 고치기 전 실행으로 이미 났다.
5. I-1(Soniox TTS 동시 한도)는 실측이 없다 — 상한 6 이 실제로 열리는지 모른다(작성자 pending · 스펙 I-1).
6. 수용 항목별 시험: A-14 · A-14b · A-44(갈래 전부) · A-47(로컬 실물 · 작성자) · C-A20 · C-A21 · N-A13(서버) — 있음. A-45 · A-46 · I-1 은 실물 몫.

## 범위

- 계획(`wp-plan.md` §2 WP-BE-1 · WP-BE-2 파일 표)에 없는 파일: `day/dtos/glossary.py`(값 클래스 분리 — 같은 기능 파일 이름 규칙 · 받아들임) · `day.public.run_interpret_session`(작성자 2번). 그 밖은 표 안이다.
- `app/` · `.github/` · `backend/migrations/` 변경 0(`git status`).

## 참고

- R1. `session.py:416-433` — `_cleanup` 이 STT 닫는 중에 취소되면 TTS 연결은 닫히지 않는다(자리는 반납). 고칠 방향: 두 연결 닫기를 `asyncio.gather(…, return_exceptions=True)` 로 묶거나 각 닫기를 `try/finally` 로.
- R2. `common/config.py` `day_interpret_max_sessions: Field(default=6, ge=1)` — 위 상한이 없다. 잘못 넣은 큰 값이 Soniox 공용 키 한도를 넘길 수 있다(`le=` 하나 · 예: 50).
- R3. `dtos/glossary.py:9` → `services.interpret.langs` 역방향 import(작성자 3번).
- R4. `day.public.run_interpret_session` — 「인증 없음 · 스크립트 전용」을 지키는 시험이 없다. `tests/architecture` 에 「`day/routers` 는 이 함수를 import 하지 않는다」 한 줄이면 굳는다.
- R5. `service.py:147-157` — DB 연결 실패는 `ServiceError` 가 아니라서 핸드셰이크 500 이 된다(1008 아님). 앱 결과는 같고 로그에 예외 추적이 남는다(토큰 없음).
- R6. `chat.py:651-654` — 길이 검사가 `actor()` 앞이다. 비활성 직원의 41자 요청 = 400(403 아님). 앱은 입력을 40자로 막으므로 실사용 영향은 없다.
- R7. 작성자 「번역에 사전 이름 대신 `Ulthera`」 관찰 — 사전은 Soniox 힌트이고 보장 대상이 아니다(스펙과 같음).

## 돌린 명령 · 수치(각 1회)

| 명령 | 결과 |
|---|---|
| `cd backend && uv run pytest -q -m "not infra"` | **842 passed, 294 deselected**, 1 warning(기존 `fastapi.testclient` deprecation) · 20.6s · exit 0 |
| `cd backend && uv run ruff check . ../scripts` | All checks passed! |
| 원천 AST 대조(assembler · chinese · langs · soniox · glossary) | 5/5 동일 · session.py 8곳 다름(위 표) |
| 시드 sha256 | 원천과 같음 |
| `git diff -U0 deploy/config` 값 줄 | 0 |
| infra(`scripts/test.sh`) | 돌리지 않음(지시) |
