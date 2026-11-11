# fix WP-BE-2 통역 서버 결과 보고

## 상태: done (A-44 서버 단위 · A-45 실물 Soniox · A-47 로컬 실물 통과) — I-1(동시 한도) · A-46(사용자)은 pending

## 수행 — 변경 · 새 파일

원천 = interpret-pwa `origin/main` `17c26b5`(`git show` 로만 읽음 · canonical 체크아웃 · 수정 없음). 각 파일 머리에 원천 경로 · ref.

**새 파일**

| 파일 | 무엇 |
|---|---|
| `backend/day/routers/api/interpret.py` | WS `/api/interpret` — 헤더 Bearer 만(`?token=` · Origin 안 봄) · `interpret.authorize()` 실패면 accept 전 close 1008 · 통과면 accept → 세션. router 에 DB 없음 |
| `backend/day/services/interpret/{__init__,langs,chinese,assembler,soniox}.py` | 원천 그대로(줄 길이 · 머리만 · 로직 같음) |
| `backend/day/services/interpret/session.py` | 원천 + 기록기 제거 · `Slots`/`Slot`(동시 세션 자리 — `try_acquire(limit)` · `release()` 여러 번 불려도 한 번) · `session_limit`(문구 = `MSG_NO_API_KEY` 재사용) · 자리는 키 확인 뒤 · Soniox 열기 전 · `_cleanup` 의 `finally` 에서 반납 · 키 없음 로그 문구에 env 이름 없음 |
| `backend/day/services/interpret/service.py` | 원천 `container.py` 통역 부분을 DAY 모양으로 — `load()`(시드 검사 · 7개 언어 context 를 기동 때 미리 만듦 · `glossary seed loaded: version=…` · 깨지면 `glossary seed invalid: … — 기동을 멈춘다` 뒤 예외) · `authorize()`(짧은 DB 세션 안에서 `sessions.current_session(bearer)` + `require_permission(board, VIEW)` — 전체 권한 계정 포함 · 닫은 뒤 결과만) · `Interpreter.session()`(키 · 상한은 지금 설정) |
| `backend/day/services/glossary.py` · `backend/day/dtos/glossary.py` | 원천 `glossary.py` — 검사 · context 조립은 service, 값 클래스(Entry · Term · Glossary · ContextParts)는 dtos |
| `backend/day/seed/glossary.json` | 원천 시드 **바이트 그대로** — sha256 `e273493603a52d3f07704a62ec83dcfe0c4871170ff975e4ede4880467cb4fe8`(원천 `git show` 값과 같음) · version `2026-10-27.6` · 170 term |
| `backend/tests/day/interpret/{__init__,conftest,seed_tables,test_seed,test_context,test_interpret,test_interpret_auth}.py` | 원천 시험 이식 + DAY 인증 · 상한 · 자리 반납. WS 는 같은 루프 ASGI 드라이버(`AsgiWs`) — 세션 단위 시험 루프와 DB 엔진을 섞지 않으려고 TestClient 를 쓰지 않음 |
| `scripts/interpret_live_check.py` | 원천 `live_check.py` 의 seed · zhhant(→ roundtrip) · idle 만 · 키는 프로세스 env `DAY_SONIOX_API_KEY` 만 · 출력 없음 · 키 없으면 `PENDING` · exit 2 |

**고친 파일**

| 파일 | 무엇 |
|---|---|
| `backend/common/config.py` | `day_soniox_api_key: SecretStr = ""` · `day_interpret_max_sessions: int = Field(default=6, ge=1)` |
| `backend/day/public.py` | `api_routers()` 에 통역 라우터 · `load_interpret()`(기동 적재 → version) · `run_interpret_session(client)`(실물 스크립트용 — 아래 「다른 곳」 2) |
| `backend/runtime/main.py` | lifespan 첫 줄 `load_interpret()` — 깨진 시드면 api 기동 실패 |
| `scripts/deploy/day_vm.py` | `OPTIONAL_SECRETS["DAY_SONIOX_API_KEY"] = "soniox-api-key"`(한 줄 · 일반 설정 금지 키에 자동 포함) |
| `deploy/compose.local.yaml` | api 등 env 에 `DAY_SONIOX_API_KEY: ${…:-}` · `DAY_INTERPRET_MAX_SESSIONS: ${…:-6}`(빈 값이면 int 검사 실패라 기본 6 — `env_ignore_empty` 없음) |
| `deploy/local.env.example` | 키 빈 칸 · 상한은 주석(`# DAY_INTERPRET_MAX_SESSIONS=6`) |
| `deploy/config/dev.env` · `prod.env` | **주석 3줄만 덧붙임**(선택 비밀 이름 · 상한은 코드 기본값) — 값 줄 무변경 |
| `docs/development/deployment.md` | 선택 비밀 3개 이름 · 통역 상한 · 「깨진 시드 = api 기동 실패 · 로그 한 줄」 |
| `pyproject.toml` · `uv.lock` | `opencc-python-reimplemented>=0.1.7,<0.2`(0.1.7) · `websockets>=15,<18`(직접 의존으로 적음 — 잠금은 이미 17.4) |
| `backend/tests/common/test_config.py` · `tests/deploy/test_day_vm.py` · `tests/deploy/test_chat_env_contract.py` | 새 칸 기본 · 범위 · 선택 비밀 이름 · 금지 키 · dry-run 이름 · compose/예시/서버 설정 계약 |

migration 없음 · `app/` · `.github/` 무변경.

## 수용 항목 ↔ 시험

| 항목 | 시험 |
|---|---|
| A-14 시드 `2026-10-27.6` · 로그 | `test_interpret.py::test_real_seed_loads_and_logs_version`(로그 한 줄 · 7개 context = 원천 방식) · `test_seed.py::test_startup_log_one_line` · 원천 시드 검사 18개(`test_seed.py` — `.6` 표 대조 포함) |
| A-14b 보기 권한 · edit 불필요 · 쿼리 · Origin 안 봄 | `test_interpret_auth.py::test_authorize_갈래`(view · edit · 전체 권한 통과 / 권한 행 없음 거절) · `::test_끝에서_끝_실제_인증_가짜_Soniox` · `test_interpret.py::test_origin_is_not_checked` · `::test_only_bearer_header_counts` |
| A-44 핸드셰이크 거절(없음 · 틀림 · 만료 · 로그아웃 · 권한 없음 · `?token=` 만) = accept 전 1008 | `test_interpret.py::test_handshake_rejected_before_accept_with_1008` · `test_interpret_auth.py` 두 시험(실제 DB) |
| A-44 `start` 틀림 · 10초 = `bad_request` | `::test_bad_start`(8) · `::test_error_codes_close_1000_and_no_leak`(xx · pause) · `::test_start_timeout_bad_request` |
| A-44 키 없음 = `no_api_key` | `::test_error_codes_close_1000_and_no_leak` · `::test_no_api_key_does_not_open_soniox_or_take_slot` |
| A-44 7번째 = `session_limit` · 설정으로 바꿈 · 정리 뒤 자리 돌아옴 | `::test_session_limit_default_six_seventh_rejected_and_slot_returns` · `::test_session_limit_follows_setting` |
| A-44 자리 반납 갈래(각각 0 · 음수 없음) | STT 실패 = `::test_error_codes…`(soniox_unavailable) · TTS 실패 = `::test_slot_returns_on_tts_open_failure` · 설정 재시도 중 예외 = `::test_slot_returns_on_exception_during_config_retry` · ready 뒤 끊김 = `::test_slot_returns_when_soniox_drops_after_ready` · 앱 소켓 강제 끊김 = `::test_slot_returns_when_app_vanishes_without_close_frame` · 서버 작업 취소 = `::test_slot_returns_when_server_task_cancelled` · Soniox 연결 중 취소 = `::test_slot_returns_when_cancelled_during_soniox_connect` · 한 번만 · 음수 없음 = `::test_slot_release_is_once_and_never_negative`. 변이 확인: 반납 줄을 끄면 이 시험들 중 10개가 실패(되돌림 확인) |
| A-44 연결 수립 10초 넘김 | `::test_soniox_connect_timeout_is_soniox_unavailable`(핸드셰이크에 답하지 않는 로컬 TCP 서버 · 상한 0.2초로 낮춤 · 실제 `SonioxStt.open`) · `::test_configs`(상수 10) |
| A-44 Soniox 가짜 거절 · 끊김 = 두 문구 | `test_context.py` 1 ~ 6 · `::test_closed_without_error…`(「통역 서버에 연결하지 못했어요」) · `::test_5_invalid_request_after_ready_no_reconnect` · `test_interpret.py::test_slot_returns_when_soniox_drops_after_ready`(「통역 연결이 끊겼어요」) |
| A-44 `message` 에 env 이름 · 받은 값 없음 · accept 뒤 1008 없음 | `::test_error_codes_close_1000_and_no_leak`(close 1000 · 금지 낱말) · 로그 = `::test_relay_error_log_has_channel_and_state_only` · `test_context.py::test_rejection_log_has_type_and_request_id_only` |
| A-44 깨진 시드 = 기동 실패 | `test_interpret.py::test_broken_seed_fails_app_startup`(실제 `runtime.main.lifespan`) · `test_seed.py::test_broken_seed_fails_startup` |
| A-44 7개 언어 context = 원천 결과 | `test_context.py`(원천 24개) · `::test_service_uses_language_limit` · `test_interpret.py::test_lang_mapping_and_context_injected`(7) |
| A-44 Soniox 두 연결 닫힘 · 기록 0 | `::test_full_flow` 외 반납 시험들(`closed`) · `::test_no_record_files_and_no_recorder` |
| I-3 OpenCC × 3.13 | `::test_traditional_only_for_chinese…` · `::test_caption_conversion_per_lang_tts_simplified` · `uv run python -c` 확인(아래) |
| 연결 중 DB 안 쥠 | `test_interpret_auth.py::test_끝에서_끝…` — ready 상태에서 풀 `checkedout() == 0` |

## 계약 표(SPEC-003 §3 「통역」) ↔ 구현 — 필드 단위

| 계약 | 구현 |
|---|---|
| 경로 `WS /api/interpret` | 같음(`APIRouter(prefix="/api")` · `@router.websocket("/interpret")`) |
| 헤더 Bearer 만 · `?token=` 안 받음 · Origin 안 봄 | 같음(`bearer()` 는 헤더만 · Origin 코드 없음) |
| accept 전 검사 · 세션 + `board` view(`is_admin` 포함) · DB 세션 accept 전에 닫음 | 같음(`authorize()` 의 `async with` 가 끝난 뒤 accept) |
| 거절 = accept 안 하고 1008 → 앱 403 | 같음(실제 uvicorn 에서 403 확인 — A-47) |
| 연결 중 재확인 없음 · accept 뒤 1008 없음 | 같음(세션 코드가 닫을 때 `client.close()` 기본 1000) |
| `start{type,lang}` · 그 밖 칸 무시 · 10초 · 7개 밖 = bad_request 닫음 | 같음 |
| 바이너리 PCM · pause 중 버림 · pause=finalize · resume · stop = end + drain 3초 | 같음(원천 그대로) |
| 그 밖 텍스트 = bad_request 안 닫음 · 받은 값 안 돌려보냄 | 같음 |
| `ready` · `caption{id,side,original,translation,final}` · `audio_start{id,sampleRate:24000}` → PCM → `audio_end{id}` · `error{code,message}` | 같음(시험에서 필드 단위 비교) |
| 오류 4코드 + `session_limit` · 문구 5개 | 같음 — `bad_request` 「요청을 처리할 수 없어요」 · `no_api_key` 「통역 서버를 쓸 수 없어요」 · `session_limit` 같은 글자 · `soniox_unavailable` 「통역 서버에 연결하지 못했어요」/「통역 연결이 끊겼어요」 |
| 닫음 close 1000 · 1008 은 거절에만 | 같음 |
| 순서: start → 키 → 자리 → STT(context) → 2초 확인 → invalid_request 면 정방향만 1회 → TTS → ready | 같음 |
| Soniox STT/TTS 모델 · URL · hints · endpoint · two_way · keepalive 10초 · TTS `{"keep_alive": true}` 20초 · 괄호 뺀 TTS 입력 | 같음(`test_configs` 로 상수 고정) |
| 정리 — 두 연결 닫기(3초) · 자리 한 번 반납 | 같음(`finally`) |
| 연결 시간 상한 ① 10초 ② websockets 기본 ping 20/20 ③ uvicorn 기본 ping | 같음 — ① `open_timeout=CONNECT_TIMEOUT` ② 값 안 줌(라이브러리 기본) ③ compose 명령 무변경 |
| 로그 = 종류 · 길이 · 시각 · id 만 | 같음 + 핸드셰이크 거절은 `code=` 만 |
| 기록 없음 | 같음 |
| 동시 세션 6 · `DAY_INTERPRET_MAX_SESSIONS` · 프로세스 안 셈 | 같음 |
| 사전 = 시드 사본 · 기동 때 한 번 · 깨지면 기동 실패 · 로그 한 줄 · 언어별 상수 · env 덮기 없음 | 같음(+ 7개 context 를 기동 때 미리 만듦 — 스펙 허용) |
| `DAY_SONIOX_API_KEY` 선택 비밀 `day-<env>-soniox-api-key` 한 줄 | 같음 |

## 돌린 명령 · 수치

격리 스택: `docker compose -p daybetest`(127.0.0.1:11142/11143 · 일회용 자격) — 끝나고 `down -v`(볼륨까지 지움). 사용자 `day-local-*` · 11040/11042/11043 미사용 · 무변경.

- `uv run python -c "import opencc"` 류(Python 3.13.11): `激光治疗 离子导入` → s2tw `激光治療 離子導入` · `美國熱瑪吉` → t2s `美国热玛吉` — **I-3 통과**
- 적재 실측(I-4): 시드 검사 + 7개 언어 context 조립 = **약 42 ms**(기동 때 한 번) — 세션마다 사전 줄이기 · OpenCC context 변환 없음. 자막 OpenCC 변환은 발화마다(원천 그대로)
- 7개 context(실제 시드): en 17,589자 · ja 19,408 · zh 18,565 · **zh-Hant 21,658(terms 170 · reverse_alias 33 줄임 — 원천 한도 그대로)** · th 20,804 · vi 17,596 · yue 17,636
- `uv run pytest -q tests/day/interpret`(DB 없음) → **174 passed** · `tests/deploy tests/common/test_config.py` → **112 passed** · `tests/architecture` → **28 passed**(`test_import_boundaries` 포함 · 고치지 않음)
- `scripts/test.sh -q tests/day/interpret/test_interpret_auth.py`(격리) → **2 passed**
- 마지막 전체: `uv run pytest -q -m "not infra"` → **842 passed**, 294 deselected · `scripts/test.sh -q`(격리 스택 · 전부) → **1136 passed**(경고 1 = 기존 `fastapi.testclient` deprecation)
- `uv run ruff check backend scripts` → All checks passed · `ruff format --check` → 227 files already formatted

## 실물 결과

**A-45 — 실제 Soniox(dev 와 같은 키 · 로컬 interpret-pwa `.env` 에서 프로세스 env 로만 · 값 출력 0)** `scripts/interpret_live_check.py all` 한 번:

| 언어 | start → ready |
|---|---|
| en | ready ✓ (사전 context 거절 0) |
| ja | ready ✓ |
| zh | ready ✓ |
| zh-Hant | ready ✓ (줄인 context 받아들임) |
| th | ready ✓ |
| vi | ready ✓ |
| yue | ready ✓ |

- 이 seed 갈래는 오디오 0 으로 바로 stop 해서, 7개 모두 ready **뒤** Soniox 가 `invalid_request: No audio received` 를 내 `soniox_unavailable`(「통역 연결이 끊겼어요」)로 끝났다 — ready 판정과 무관한 **스크립트 대본 탓**(원천도 같은 동작 · 앱은 stop 뒤 바로 소켓을 닫아 이 프레임을 보지 않음). 스크립트를 「무음 1초 뒤 stop」으로 고쳤지만 **다시 돌리지 않았다**(호출 되풀이 금지) → pending.
- **왕복(zh-Hant)**: ko 발화 → me 자막 「오늘은 울쎄라 시술을 먼저 하실게요.」 / 「今天先給您做一次Ulthera治療。」(번체) · zh 발화 → them 자막 「請問打完以後多久可以洗臉？」 / 「시술하고 나면 얼마나 시간이 지나서 세안하시면 되나요?」 · audio_start 2 · 번역 음성 356,352 바이트 · 오류 0 · 중국어 쪽 번체 ✓.
- **멈춤 35초 뒤 두 번째 발화(zh-Hant)**: 번역 있는 확정 자막 2 · audio_start 2 · 음성 360,448 바이트 · 오류 0 · 56.9초 — TTS keepalive 장애 갈래 통과.
- 관찰: zh-Hant 번역에 「울쎄라」가 사전 대만 이름(美國音波)이 아니라 「Ulthera」로 나왔다 — 사전은 Soniox 힌트일 뿐이라 보장 대상 아님(계약 위반 아님 · 참고).

**A-47 — 로컬 실제 uvicorn(격리 DB · 127.0.0.1:11150 · 키 비움 · 끝나고 내림)** websockets 클라이언트:

- `board` 권한 행 없는 계정 → 핸드셰이크 **HTTP 403**(→ 앱 「통역 서버가 로그인을 받지 않았어요 — 다시 로그인해 주세요」)
- 보기 권한 계정 · 키 비움 → 101 → `start` → `{"type":"error","code":"no_api_key","message":"통역 서버를 쓸 수 없어요"}` → close **1000**
- `?token=` 만 → **403**
- 서버 로그: `glossary seed loaded: version=2026-10-27.6` 한 줄 · `interpret handshake rejected: code=forbidden` / `code=unauthorized` · `interpret unavailable: speech provider key is not configured`(env 이름 없음)

## 스펙과 달라진 곳 · 물을 것

1. **uvicorn 접근 로그가 쿼리 문자열을 그대로 남긴다** — A-47 에서 `?token=…` 로 붙자 uvicorn 로그 한 줄에 `WebSocket /api/interpret?token=<값>" 403` 이 찍혔다. DAY 는 쿼리 토큰을 받지 않고 앱도 보내지 않지만, 잘못 붙는 클라이언트가 있으면 토큰이 로그에 남는다. 원천엔 쿼리 지우기 필터(`DropQueryString`)가 있었고 스펙은 이 점을 말하지 않는다 — **발명하지 않고 보고만** 한다. 넣을지 사용자 · planner 판단(넣으면 `common/logs` 에 필터 하나).
2. `day.public.run_interpret_session(client)` 를 더했다(계획 표에 없음) — 실물 스크립트가 `day` 안쪽을 import 하지 않게(scripts 는 `day.public` 만 쓰는 저장소 관례). 인증 없이 세션을 도는 길이라 HTTP 로는 노출되지 않는다.
3. `dtos/glossary.py` 가 `services/interpret/langs.APP_LANGS` 를 읽는다(`Glossary.entry_counts`) — 경계 시험은 통과. 거슬리면 `entry_counts(langs)` 로 바꾸면 된다.
4. compose 의 상한 기본을 `${DAY_INTERPRET_MAX_SESSIONS:-6}` 로 뒀다(계획 「APNs 줄과 같은 꼴」은 `:-` 빈 값) — 설정이 빈 문자열을 무시하지 않아 빈 값이면 기동 실패. 예시 env 도 같은 이유로 주석.
5. 계획 ↔ 스펙 충돌은 찾지 못했다.

## pending

- **I-1 Soniox TTS 동시 한도** — 실측하지 않았다(동시 4 세션 이상을 열어야 함 · 호출 최소 원칙). 6 보다 작으면 사용자에게 상한을 다시 물어야 한다(dev · prod 같은 공용 키).
- seed 갈래 재실행(「무음 1초 뒤 stop」으로 고친 대본) — 필요하면 코디 승인 뒤 한 번.
- A-46(사용자 실기기 · 긴 세션 3분 20초 · Caddy `request_body` 6MiB — I-2) · dev 배포 뒤 서버 로그 시드 버전(코디).
- 위험 알림(계획 §6): **깨진 시드 = api 기동 실패 → 로그인 · 시술현황 · 채팅 · 알림 전부 멈춤**(배포 헬스 실패로 롤백). 시드는 바이트 그대로이고 `test_seed` 가 CI 에서 같은 검사를 한다.
- 커밋 · push · PR 은 하지 않음.
