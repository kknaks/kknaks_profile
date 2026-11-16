# WORK-001 WP2 결과 보고 — back 통역 WS

## 상태: done (코드 · 시험) / **실물 §9.3 ① ~ ⑦ pending — 레포 루트 `.env` 없음(SONIOX_API_KEY 없음)**

## 수행 — 파일·모듈 목록
워크트리 `/Users/kknaks/orca/workspaces/interpret-pwa/interpret-pwa-poc` (커밋 없음 · 변경만)

- 원형 `origin/main:procedure/back` 에서 **복사**(import 없음) 뒤 SPEC 자리만 고침:
  - `back/app/service/interpret/assembler.py` — 그대로(docstring 만)
  - `back/app/service/interpret/chinese.py` — 그대로 + `to_simplified`(t2s · 용어 target 용 · WP1)
  - `back/app/service/interpret/soniox.py` — `stt_config(lang, context)`(비면 `context` 키 없음) · `SonioxStt.open(api_key, lang, context)` · **`SonioxError.error_type` · `request_id`** (`_check` 가 문자열에 묻지 않음)
  - `back/app/service/interpret/session.py` — `LANGS` = 6개(`langs.py`) · `parse_start` 는 `{lang}` 만(`traditional` · `scheduleId` 무시) · `no_api_key` 문구 「SONIOX_API_KEY 가 .env 에 없어요」 · Soniox 에는 `soniox_lang(lang)`(yue→zh) · `CaptionAssembler(traditional=lang=="yue")` · **ready 앞 STT 설정 확인**(`_open_stt_checked` · `_check_config` · `_stt_messages`) · 오류 로그는 `error_type` · `request_id` 만 · context 칸 수 로그 1줄
  - `back/app/api/interpret.py` — Origin = `INTERPRET_FRONT_ORIGIN` · 토큰(§3.2) · 둘 다 accept 전 · 실패 1008 · 세션에 `context_for` · `config_check_sec`
  - `back/tests/test_interpret.py` — 원형 시험 복사 + 추가
- `back/app/service/interpret/langs.py` — §5.5 매핑 한 곳(WP1)
- `back/app/container.py` — `open_stt` · `open_tts`(가짜로 바꿈) · `stt_config_check_sec`(기본 2.0) · `context_for(lang)`
- `back/app/main.py` — interpret router 등록
- `back/tests/test_context.py` — §4.4.1 가짜 Soniox 시험 추가
- `back/scripts/live_check.py` — **실물 확인 스크립트(§9.3 ① ~ ⑦)**

### ready 앞 설정 확인 — 구현 모양(SPEC §4.4.1)
STT 열기(+context) → 첫 메시지를 최대 2초 기다림(태스크로 `anext` — 시간이 지나도 제너레이터를 취소하지 않고 그 태스크를 중계 첫 메시지로 넘김) →
① 오류 메시지: `error_type == "invalid_request"` 이고 context 에 `terms` 가 있으면 거절된 STT 를 닫고 `terms` 뺀 설정으로 STT 1회 다시(같은 2초 확인) · 그 밖 `error_type` 은 바로 `soniox_unavailable`
② 오류 없이 닫힘 → `soniox_unavailable` ③ 무응답 → 통과 ④ 토큰 메시지 → 통과 · 버리지 않고 중계
→ 그 뒤 TTS 열기 → `ready`. `ready` 뒤 거절은 재연결 없이 「통역 서버(Soniox) 오류로 끊겼어요」.

## 검증 — 명령과 수치
- `cd back && uv run ruff check .` → All checks passed
- `uv run pytest -q`(전체 1회 · WP1 + WP2) → **123 passed** (test_auth 26 · test_glossary 22 · test_context 20 · test_interpret 55)
  - WP2 범위 `tests/test_interpret.py tests/test_context.py` → 75 passed
- 시험 목록(§9.1):
  - 「통역」 원형 복사분 — 묶기 · 갱신 · 번체 자막 · TTS 간체 · flush · bad start · 전체 흐름 · 닫기 정리 · 오류 코드 3종 · Origin · 토큰(헤더 · 쿼리 · 틀림 · 없음) · 빈칸 정리 — 통과
  - 추가 — `lang` 6개 수락 · `traditional`/`scheduleId` 무시 · 오류 문구 「가능: en, ja, th, vi, yue, zh」 · 6개 언어 매핑(yue → Soniox zh · `language_b` · `language_hints`) · STT 에 `context_for(lang)` 그대로 들어감 · yue 자막 번체 `麻醉藥膏` / zh 간체 `麻醉药膏` / TTS 는 둘 다 `("zh","麻醉药膏")` · 빈 용어집 → context 없이 연결 · 알 수 없는 프레임은 끊지 않음 · 10초 start 시간 초과
  - 「context」 §4.4.1 — ① invalid_request → terms 없는 2번째 STT · 같은 브라우저 WS 에서 ready · 첫 STT 닫힘 ② 두 번 거절 → soniox_unavailable · TTS 안 열림 ③ unauthenticated · quota_exceeded · service_unavailable → 재연결 없음 ④ 무응답 → ready ⑤ ready 뒤 invalid_request → 재연결 없음 + 확인 중 닫힘 · 토큰 첫 메시지 중계 · `SonioxError.error_type`/`request_id` · terms 없는 context 는 재시도 안 함 — 통과
  - 「비밀값」 — 로그 캡처에 토큰 · 키 · 비밀번호 · 세션 비밀 · 용어 문자열 0 · 접근 로그 `?token=` 지움(HTTP · WebSocket 줄) — 통과
- 이미지: `docker build back` 성공 → 컨테이너 1회 기동(8800) — 기동 로그 `glossary loaded: version=2026-07-01-reviewed-v5 count=158` · `/api/health` 200 → 내리고 이미지 지움
- 실물 스크립트 — 가짜 Soniox 로 배관만 dry-run(③ · ④ 경로 끝까지 돎) · 실물은 키 없음 → `PENDING` · 종료 코드 2

## 실물 §9.3 — pending (키 없음)
레포 루트 `.env` 파일이 없다 — 우회하지 않았다. 사용자가 `SONIOX_API_KEY` 를 넣으면 코디가 아래를 돌린다(포트 안 씀 · 프로세스 안에서 InterpretSession 실물):

```bash
cd /Users/kknaks/orca/workspaces/interpret-pwa/interpret-pwa-poc/back
uv run python scripts/live_check.py all --out ../live-check.json    # ① ~ ⑦ 전부 · 수 분
# 항목별: context(①) · terms(②) · yue(③) · foreign(④) · paren(⑤) · noglossary(⑥) · overflow(⑦)
```

| # | 스크립트가 남기는 값 | 판정에 쓰는 키 |
|---|---|---|
| ① | 언어별 `terms` · `terms_dropped` · `translation_terms` · `chars` · `rejected` · `error_type` · `elapsed_sec` | 6개 모두 `rejected=false` → `GLOSSARY_CONTEXT_MAX_CHARS` 확정 |
| ② | en · zh · ja 각각 용어 3개(`필러` · `쥬비덤` · `신펄` 우선) — `with_context` / `no_context` 번역문 · `hits` · **`reverse_foreign_utterance`(외국어 발화 → 한국어 번역의 ko 표기 hit · OQ-003)** | hits 비교 |
| ③ | yue 자막 번역 · TTS 입력 · `caption_traditional` · `tts_simplified` | 둘 다 true |
| ④ | en 발화 → `sides` · 번역 · TTS (ko) · `audio_start.sampleRate` · `audio_bytes` · `ok` | `ok=true` |
| ⑤ | ja 괄호 병기 target 3개 · 번역문 · TTS 입력(OQ-009) | 기록만 |
| ⑥ | 틀린 주소 → `glossary_loaded=false` · `context_empty` · `ready` | ready |
| ⑦ | 약 2만 자 context(th × n) · `rejected` · `error_type` · `elapsed_sec` · `audio_sent` · `within_check_window` | 오디오 없이 2초 안 invalid_request → 2초 확정 |

입력 음성은 Soniox TTS(16 kHz)로 만든다. 출력에 키 · context 본문 없음(용어는 ②⑤ 판정용 target 몇 개만).

## 계약 대조 — SPEC 항목별
- §5.1 중계 구조 · 메시지 · 오디오 형식 · 모델(stt-rt-v5 · tts-rt-v2 · Jiwoo · 16k/24k) · keepalive · 3초 드레인 — 원형 그대로 · 같음
- §5.1 `lang` 6개 · `traditional` 없앰(와도 무시) · `scheduleId` 없앰 · STT `context` · ready 시점 · 인증 · 오류 문구 env 위치 — 같음
- §5.2 경로 · `?token=` + 헤더 Bearer · Origin → 토큰 순서 · accept 전 · 1008 · 동시 연결 제한 없음 · 세션 끝 두 연결 닫음 · back 재연결 없음 — 같음
- §5.3 메시지 모양 — 원형 그대로 · 같음
- §5.4 `bad_request` · `no_api_key` · `soniox_unavailable` 문구 3종 — 같음
- §5.5 매핑(yue → zh STT · TTS) · `langs.py` 한 곳 — 같음
- §5.6 yue 만 자막 중국어 쪽 s2tw · TTS 간체 · zh 는 간체 — 같음
- §4.4 4번 · 5번 · §4.4.1 표 전부 — 같음. **한 자리 해석**: context 에 `terms` 가 이미 없으면(빈 용어집 · 다 줄임) `invalid_request` 여도 같은 설정을 다시 보내지 않고 바로 `soniox_unavailable` (재시도해도 같은 설정이라)

## 이슈 · 코디가 확인할 것
1. **실물 ① ~ ⑦ pending** — 키를 넣고 위 명령 1회. ① 결과로 `GLOSSARY_CONTEXT_MAX_CHARS` · ⑦ 결과로 `STT_CONFIG_CHECK_SEC`(코드 상수 `session.py` · container 필드) 확정. 사용자 결정 2건(OQ-003 = ② `reverse_foreign_utterance` · OQ-009 = ⑤)은 그 출력으로.
2. 실물 matrix 글자 수(WP1 측정 · general 포함): th 9,900자가 한도에 가장 가깝다 — 토큰 기준 거절 여부는 ①.
3. **8800 포트에 내가 띄우지 않은 back 이 떠 있다** — PID 45321 `uv run uvicorn app.main:app --port 8800`(이 워크트리 `back/` · 16:00 경 시작 · frontend 워커의 WP3 실 back 확인으로 보임). 건드리지 않았다. 내가 띄운 것(WP1 uvicorn · WP2 docker 컨테이너)은 모두 내렸다.
4. `STT_CONFIG_CHECK_SEC` 는 env 가 아니라 코드 상수(SPEC §2.4 에 env 가 없어서). 시험은 container 필드로 0.05 ~ 0.1초.
5. `front/` 는 건드리지 않았다(`git status` 의 front 변경은 frontend 워커 것).
