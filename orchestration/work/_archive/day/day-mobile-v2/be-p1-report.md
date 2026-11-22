# day-mobile-v2 P1 결과 보고 — 통역 서버를 통키 `56e43a0` 최신으로

## 상태: done (프론트 정적 검사만 pending — npm 미설치 환경 · 내 변경과 무관)

워크트리 `/Users/kknaks/orca/workspaces/CENTURION_DAY/day-mobile-v2` · 브랜치 `kknaksss/day-mobile-v2`(base origin/dev `844eace4`). 커밋 · push · PR 없음 — 변경만 남김.

## §6-1 항목 표 — 통키 `17c26b5..56e43a0` · 스펙 §3 「통역 — 0.2.0」

| # | 항목 | 통키(`56e43a0`) | DAY 넣은 곳 | 스펙 근거 |
|---|---|---|---|---|
| 1 | STT `stt-rt-v6` | `soniox.py` `STT_MODEL` | `adapters/soniox.py` `STT_MODEL` | 0.2.0 표 「STT 모델」 · D-43 |
| 2 | `enable_agent_text_input: true` · `send_agent_text` | `soniox.py` `stt_config` · `SonioxStt.send_agent_text` | `adapters/soniox.py` | 「STT 모델」 · D-69 |
| 3 | 끊김 `max_endpoint_delay_ms` 2000 · `endpoint_sensitivity` -0.3 | `soniox.py` 상수 | `adapters/soniox.py` `MAX_ENDPOINT_DELAY_MS` · `ENDPOINT_SENSITIVITY` | 「끊김」 · D-67 |
| 4 | TTS `return_timestamps: true` · `TtsAudio`(오디오 + 글자 시각) | `soniox.py` `tts_config` · `speak` | `adapters/soniox.py` | 「`stop` · TTS 설정」 · D-70 |
| 5 | TTS cancel `{stream_id, cancel: true}` · 연결 세션 내내 하나 | `soniox.py:210` · `session.py:201` | `adapters/soniox.py` `cancel`(DAY 에 이미 있던 함수를 Protocol 에 올림) · `TtsConn.cancel` | 「`stop` · TTS 설정」 |
| 6 | 역할 context `text`(영문 4문장 424자) · 키 순서 general → text → terms → translation_terms | `glossary.py:43` `CONTEXT_TEXT` · `to_soniox` | `policies/glossary.py` `CONTEXT_TEXT` · `to_soniox` | 「역할 context」 · D-45 · D-49 |
| 7 | invalid_request 다시 연결 때 `text` 유지 · `TRIM_ORDER = ("terms", "reverse")` | `glossary.py:272` · `:331-334` | `policies/glossary.py` `forward_only` · `TRIM_ORDER` · `is_forward_only`(text 는 판정 밖) | 「역할 context」 · W-9 |
| 8 | 고유명사 context(proper 74개 · 정방향 + 역방향만 · 별칭 짝 0) | `glossary.py` `build_context` | `policies/glossary.py` `build_context` | 「사전 context」 · D-71 |
| 9 | 언어별 한도 = v6 실측 × 0.96 | `langs.py` `CONTEXT_MAX_CHARS` | `policies/interpret/languages.py` `CONTEXT_MAX_CHARS` | 「사전 context」 · D-56 |
| 10 | 시드 `.11` 바이트 그대로 | `back/seed/glossary.json`(sha1 `76d2e2bd…`) | `backend/day/seed/glossary.json`(같은 sha1) | 「시드」 |
| 11 | 로더 허용 칸 — term `proper`(bool 검사) · `ko_wrong` · entry `wrong`(괄호 허용) | `glossary.py` `TERM_KEYS` · `ENTRY_KEYS` · `validate_seed` | `policies/glossary.py` · 값 클래스 `dtos/glossary.py` | 「시드」 · W-14 |
| 12 | 검사 8 `wrong_form` · `wrong_key` | `glossary.py:153-180` | `policies/glossary.py` `_check_wrong_forms` · `wrong_key` | 「시드」 · W-14 |
| 13 | 빈 원문 막기 — caption · TTS 0 · 보인 말풍선은 같은 id 둘 다 빈 final caption 으로 지움 | `assembler.py` `is_blank` · `session.py:403-421` | `policies/interpret/assembler.py` `is_blank` · `services/interpret/session.py` `_blank_filter` | 「빈 원문」 · D-48 · F-4 |
| 14 | 세 참여자 — 차례 끝 서버 시계 1초 · `pause` = 바로 · 재생 중 듣기 | `turn.py` `Turn` · `session.py` `_tick` · `_player` | `policies/interpret/turn.py` · `services/interpret/speaker.py` | 「세 참여자」 · D-68 · D-69 |
| 15 | 차례 거르기 `TokenGate`(재생 언어 토큰 버림 · ECHO_TAIL 500 ms · `drop_open` → 빈 final caption) | `turn.py` `TokenGate` · `Echo` · `session.py:368-376` | `policies/interpret/turn.py` · `assembler.py` `drop_open` · `session.py` `_on_tokens` | 「세 참여자」 ① · F-3 |
| 16 | 끼어들기 — 반대 언어 토큰 2개 → `audio_stop` 먼저 → TTS cancel(대기 3초) | `session.py:513-545` | `services/interpret/speaker.py` `_stop_playback` | 「세 참여자」 · 「새 서버 → 앱 프레임」 · W-12 |
| 17 | `playback_stopped` 받으면 그 차례 발화일 때만 멈춤 · `audio_end` 응답 | `session.py:344-350` · `:526-527` | `session.py` `_client_reader` · `speaker.py` `_stop_playback` | 「새 앱 → 서버 프레임」 · 「서버 응답」 · D-70 |
| 18 | agent text(0.7초 앞서 · 차례 끝 end_of_segment) | `session.py:609-639` · `turn.py` `Playback.due_text` | `speaker.py` `_agent_*` | 「세 참여자」 ② · D-70 |
| 19 | `stop` 때 읽을 큐 비움 | `session.py:353` | `session.py` `_client_reader` | 「`stop` · TTS 설정」 · W-11 |
| 20 | 시술명 바로잡기 ① ~ ④ | `correct.py` 전부 | `policies/interpret/correct.py`(상수 · 순서 그대로) | 「바로잡기」 · D-58 · D-63 ~ D-66 |
| 21 | records 함수 4개(`_norm` · `_spans` · `hays_of` · `match_spans`) + `_squeeze` · `_is_word` · `_SIMPLIFY` | `records.py:41-118` | `policies/interpret/matching.py`(이름 `norm_text` · `find_spans` — 뜻 그대로 · 파일 · DB 없음) | 「바로잡기」 · M-8 |
| 22 | 세션에 메모리 사전 넘김(바로잡기 재료) | `api/interpret.py` 한 줄 | `bootstrap/interpret.py` `Interpreter.session(glossary=…)` | 「바로잡기」 |
| — | 통역 기록(records 저장 · 보관 기간 env · D-41 · D-42) | `records.py` `Recorder` · `config.py` | **안 가져옴** | 「통역 기록」 · OQ-A39 |
| — | 품질 시험 전용 인자(`block_blank` · `stt_model` · `endpoint_config` · `fix_terms` · `with_text` · `drop_reverse`) · `scripts/quality_check.py` · `seed_v*.py` | `session.py` · `soniox.py` · `glossary.py` · `scripts/` | **안 가져옴**(운영 기본값만 — 통키도 API 경로는 늘 기본값) | — |
| — | PWA 앞단(`front/lib/halfDuplex.ts` 삭제 · `outputWindow.ts` · `ptt.ts`) | `front/` | **안 가져옴**(앱은 mobile P5) | 「앱(반이중 걷음)」 |

## 수행 — 바꾼 파일

allowed_paths 안:
- `backend/day/adapters/soniox.py` — v6 · 끊김 · agent text · TTS timestamps · `TtsAudio` · `TtsConn.cancel`
- `backend/day/policies/glossary.py` — 허용 칸 · proper bool · 검사 8 · `wrong_key` · `CONTEXT_TEXT` · D-71 context · `TRIM_ORDER` · `forward_only` text 유지 · `describe` text
- `backend/day/policies/interpret/assembler.py` — `is_blank` · `corrector` · `has_open` · `drop_open` · `Token` 칸 `start_ms` · `source_language`
- `backend/day/policies/interpret/languages.py` — 한도 표(D-56)
- `backend/day/policies/interpret/turn.py`(새) — 통키 `turn.py`(상수 · 판정 그대로 · 시계 주입)
- `backend/day/policies/interpret/correct.py`(새) — 통키 `correct.py`
- `backend/day/policies/interpret/matching.py`(새) — 통키 records 의 순수 함수
- `backend/day/services/interpret/session.py` — 중계 본체(빈 원문 · `playback_stopped` · `stop` 큐 비움 · 바로잡기 감싸기 · 자리 `Slots` 는 DAY 그대로)
- `backend/day/services/interpret/speaker.py`(새) — 통키 세션의 「통키 차례 · agent text」 부분(세션이 물려받는 믹스인 — 700줄 한도로 나눔)
- `backend/day/bootstrap/interpret.py` — 세션에 사전 넘김 · 로그 `text=`
- `backend/day/seed/glossary.json` — `.11` 바이트 그대로
- 테스트: `backend/tests/day/interpret/` — `conftest.py` · `interpret_fixtures.py` · `seed_tables.py`(통키 `56e43a0` 그대로) · `test_context.py` · `test_seed.py` · `test_interpret_sessions.py` 고침 · `test_interpret_turn.py` · `test_interpret_correct.py` · `test_interpret_correct_session.py` 새로

allowed_paths 밖(코디 허용 — orchestration ask 「허용 · 이 칸 추가 범위 안에서만」):
- `backend/day/dtos/glossary.py` — `EntryData.wrong: tuple[str, ...] = ()` · `TermData.ko_wrong: tuple[str, ...] = ()` · `TermData.proper: bool = False`
- `backend/day/dtos/glossary_context.py` — `GlossaryContextState.text: str = ""`

`routers/api/interpret.py` 는 바꾸지 않았다(필요 없음). migration · 앱 · 웹 · 다른 서버 기능 0.

## 검증 — 명령과 수치

- `scripts/test.sh --pure -q backend/tests/day/interpret` — **303 passed**, 2 deselected(infra)
- `scripts/test.sh --pure -q`(전체 pure) — **1610 passed**, 375 deselected
- `scripts/test.sh -q`(전체 · 격리 인프라 — 일회용 compose · `day-local` 안 씀) — **1985 passed**(248초 · exit 0 · infra 포함)
- `uv run ruff check` · `ruff format --check` · `uv run mypy`(strict · 430 files) — 통과
- `./scripts/check.sh --static` — 구조 검사 · ruff · format · mypy · **Taut audit/check 통과** → 마지막 `frontend`(npm `scripts/frontend run check`) 단계에서 실패: `Cannot find module '@tailwindcss/postcss'` — 이 워크트리에 npm 모듈이 설치돼 있지 않음(setup 미실행). 프론트 파일은 건드리지 않았다 → **pending(환경)**
- 새로 덮은 것(브리프 §6-4 최소): 차례 거르기(`test_4_gate_*` · `test_10` · `test_11`) · `audio_stop`(`test_9a` · `9b`) · `playback_stopped` → `audio_end`(`test_16_*` · bad id) · 시드 로드(`test_repo_seed_*` `.11` · proper 74 · wrong 18 entry/47꼴 · 검사 8) · 바로잡기(통키 순수 시험 전부 + 세션 5개) · context 키 순서(`test_parts_and_order` · `test_forward_only_is_structural_and_keeps_text`) · 빈 final caption 지우기(`test_blank_original_shown_bubble_erased_with_empty_final` · `test_drop_open_*`) · stop 큐 비움(`test_18`)

## 실물 1회 — Soniox v6 `start` → `ready`

- 키: 브리프가 지정한 `CENTURION_DAY/deploy/local.env` 에 Soniox 줄이 없어, 코디 허용(ask)으로 통키 `.env` 의 회사 공용 키를 **환경변수로만** 넘김(파일 복사 · 출력 · 기록 0).
- 방법: DAY `bootstrap.interpret.load()`(레포 시드 `.11`) + 실제 `SonioxStt` · `SonioxTts` 로 `InterpretSession` 하나 → `start {lang: zh}` → 무음 0.2초 → `stop`.
- 결과: **`ready` 받음(1.32초)** · 받은 프레임 `['ready']` · close 1000 · `invalid_request` 다시 연결 없음(text 키 · 고유명사 context 7,277자 그대로 받아들여짐). 로그 `stt context: lang=zh terms=74 forward=74 forward_alias=0 reverse=73 reverse_alias=0 text=424 chars=7277`.
- 주의: 첫 시도는 내 출력 필터 실수로 결과 줄을 못 봐 코디 허용으로 1회 더 돌렸다(Soniox 세션 총 2회 · 둘 다 바로 stop).
- 결과 파일(키 없음): `/private/tmp/claude-501/-Users-kknaks-orca-workspaces-CENTURION-DAY-day-mobile-v2/b4d91637-4b4e-4d53-b5c5-e7424833781d/scratchpad/live/live_result.txt`

## 계약 대조 — 스펙 §3 「통역 — 0.2.0」

| 줄 | 결과 |
|---|---|
| STT 모델 · agent text | 같음 |
| 끊김 | 같음 |
| 역할 context(키 순서 · 다시 연결 text 유지 · TRIM_ORDER) | 같음 |
| 빈 원문 | 같음 — 둘 다 빈 `final: true` caption · 같은 id |
| 사전 context(proper 74 · 정방향 + 역방향 · ×0.96 한도) · 바로잡기는 170개 전부 | 같음(레포 시드로 7개 언어 줄이기 0 확인) |
| 시드 `.11`(term 170 · proper 74 · wrong 18 entry/47꼴 · ko_wrong 0) · 로그 `version=2026-11-16.11` · 검사 8 · `wrong_key` | 같음 |
| 바로잡기 + records 함수만 | 같음(기록 저장 · 보관 없음) |
| 세 참여자(1초 · TokenGate · ECHO_TAIL 500 · 반대 언어 2개 · cancel 대기 3초 · agent text) | 같음(상수 `turn.py` 한 곳 · 통키 값 그대로) |
| `audio_stop {id}` — id 는 마지막 시작 발화(`_last_start`)라 이전 차례 id · `null` 가능 | 같음(통키 그대로) |
| `playback_stopped {id}` → 그 차례 발화 · 통키 말하는 중일 때만 → `audio_end {id}` | 같음 |
| `stop` 읽을 큐 비움 · `return_timestamps` · cancel · TTS 연결 하나 · `tts-rt-v2` | 같음 |
| 바뀌지 않는 것(인증 · 상한 6 · 오류 코드 · 문구 · 언어 7 · 번체 · keepalive · 설정 이름) | 그대로(라우터 · 자리 · 문구 손대지 않음) |

스펙과 통키 코드가 어긋난 곳: **없음**(멈추고 물을 일 없었음).

## 이슈 · 코디가 확인할 것

1. **워크트리에 내 것이 아닌 변경이 있다** — `app/lib/**`(copy.dart · board.dart · board_controller.dart · board_screen.dart · doctor_picker.dart · format.dart · room_screen.dart · theme.dart · widgets.dart 수정 · `room_move.dart` 등 새 파일 3). 나는 `app/` 을 건드리지 않았다 — 같은 워크트리를 다른 워커가 쓰는 것으로 보임. 커밋 때 나눠야 한다.
2. **조직 TTS 동시 한도(I-1)** — 세션 하나 = TTS 연결 하나를 세션 내내 쥔다(통키 그대로). 상한 6 과 조직 TTS 3 의 차이는 스펙 그대로 열림.
3. `check.sh` frontend 단계는 이 워크트리에 npm 설치가 안 돼 실패 — `./scripts/setup-local.sh` 뒤 다시 돌려야 함(내 변경과 무관).
4. 통키 `session.py` 한 클래스를 DAY 에서는 `session.py`(중계) + `speaker.py`(통키 차례 믹스인)로 나눴다 — 700줄 한도. 동작 · 상태는 같음.
5. 바로잡기 실패 처리(예외 → 고치지 않은 글 · 경고 로그)는 통키는 조립기 안, DAY 는 세션의 corrector 감싸기 안 — `policies` 가 로그를 갖지 않게 옮긴 자리만 다름(동작 같음 · 시험 `test_session_correction_exception_passes_through`).
