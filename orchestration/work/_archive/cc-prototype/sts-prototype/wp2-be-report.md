# WORK-001 WP2 결과 보고 — 통역 중계 WS · Soniox STT/TTS · 실물 호출 확인 4건

## 상태: done

## 수행 — 파일·모듈 목록

워크트리 `/Users/kknaks/orca/workspaces/cc-prototype/sts-prototype`. `cc/back/` 만 고쳤다. 커밋 없음.

- `app/api/interpret.py` — `WS /api/interpret`. Origin 이 있으면 `CC_FRONT_ORIGIN` 만 허용(아니면 1008 로 닫음)
- `app/service/interpret/session.py` — 세션 하나: start 검사 → 키 확인 → Soniox STT · TTS 연결 → `ready` → 중계(클라 PCM → STT · STT 토큰 → caption · 확정 발화 → TTS → audio_start/PCM/audio_end) · pause(=마이크만 멈춤 + Soniox `finalize`)/resume · stop(STT 정상 종료 후 최대 3초 기다림) · keepalive(STT 10초 · TTS 20초) · **끝날 때 Soniox 두 연결 모두 닫기**(닫기 · stop · 오류 어느 경우든)
- `app/service/interpret/assembler.py` — 토큰 → 발화 단위 caption(같은 id 갱신 → `final:true`), side, 번체 자막
- `app/service/interpret/soniox.py` — Soniox STT(`stt-rt-v5`, pcm_s16le 16kHz, two_way ko↔lang, endpoint 감지 1000ms) · TTS(`tts-rt-v2`, pcm_s16le 24kHz, 음색 `Jiwoo`) 연결. 키는 `Authorization` 헤더로만 보낸다
- `app/service/interpret/chinese.py` — 간체 → 번체(OpenCC `s2tw`)
- `app/container.py` · `app/main.py` — Soniox 연결 팩토리(시험에서 가짜로 바꿈) · 라우터 등록
- `pyproject.toml` · `uv.lock` — `websockets` · `opencc-python-reimplemented` 추가
- `tests/test_interpret.py` — 16개 시험
- `README.md` — 「통역 확인」 단락

## 실물 호출 확인 — SPEC §7.3 (2026-10-13, 키는 출력 · 기록하지 않음)

방법: 스크래치 스크립트(레포 밖)로 Soniox TTS 가 만든 음성 → Soniox STT(two_way)에 넣어 확인. 호출은 총 20회쯤, 각 10초 이내.

| # | 확인 | 결과 | 결정 |
|---|---|---|---|
| ① | `zh` STT · 번역이 간체/번체 | **간체.** zh 원문 전사(「你好，我想问一下…」)도, ko→zh 번역(「…我会先涂麻醉膏 然后请您等大约20分钟。」)도 간체. 문자 체계를 고르는 설정은 없다 | TW · HK(`traditional:true`)는 **back 이 자막만 번체로 바꾼다**(OpenCC `s2tw`) |
| ② | 광둥어 발화가 `zh` 로 잡혀 two_way 번역되나 | **된다.** 공개 광둥어 녹음(Wikimedia Commons, 1930년대 연설 mp3 25초)이 `language: zh` 로 태깅되고 한국어로 번역됐다(번역 품질 양호). 전사는 **표준 문어 간체**로 나왔다(광둥 구어 문자 嘅·係·唔 아님) | 국적 HK 도 `zh` 그대로. ⚠ 샘플이 격식체 연설이라 구어 광둥어 대화는 시연 전 사람 목소리로 한 번 더 보면 좋다 |
| ③ | 번체를 TTS 에 넣으면 | **오류 없이 오디오가 나오지만 발음이 깨진다.** 같은 문장을 STT 로 되돌려 보니 간체 입력은 원문 그대로, 번체 입력은 「請問→丧梦 · 時間→字卡 · 幫→报 · 藥膏→分高」처럼 틀렸다(문서의 「Simplified only」와 맞음) | TTS 에는 **간체만**(Soniox 번역 결과가 원래 간체라 변환 없음) |
| ④ | tts-rt-v2 음색 · 출력 형식 | `GET /v1/tts-models`: tts-rt-v2 음색 **200개**, 언어 63개. 한국어 음색(Mina · Jiwoo · Minjun · Seojun · Jihoon …) · 만다린 음색(Wei · Meilin · Haoran · Zihan)이 있다. `pcm_s16le` 16k · 24k 둘 다 정상 출력 | **음색 `Jiwoo` 하나 고정**(D-17). Jiwoo · Meilin 둘 다 ko · zh 를 STT 왕복으로 원문 그대로 읽었고, 한국어 직원 목소리 쪽인 Jiwoo 를 골랐다. **`audio_start.sampleRate` = 24000**, `format` 은 안 보냄(= pcm_s16le) |

덤으로 확인한 것: 번역 토큰은 원문 토큰 사이사이에 섞여 오고 `<end>` 전에 끝난다(→ `<end>` 단위로 발화를 묶음). 토큰의 `translation_status` 는 원문 `original`, 번역 `translation`, `<end>` 는 `none`.

## 검증 — 명령과 수치

| 명령 | 결과 |
|---|---|
| `CC_CAPTURE_DIR=<캡처> uv run pytest` (cc/back) | **36 passed**(WP1 20 + WP2 16) |
| `uv run ruff check .` | **All checks passed** |
| 임시 서버(포트 18612) + WS 클라이언트 스크립트, 실제 Soniox | **ko → zh**(TTS 로 만든 한국어 PCM 5.9초, `traditional:true`): `ready` → `caption` final(`side:me`, 원문 「안녕하세요, 오늘 시술 전에 마취 크림을 바르고 20분 정도 기다리실게요.」, 번역 번체 「你好，今天在治療前 我會先塗麻醉膏 …」) → `audio_start {sampleRate:24000}` → PCM 327,680 바이트 → `audio_end` → `stop` 후 1000 정상 종료. **zh → ko**: `side:them`, 원문 번체 「你好，我想問一下今天的治療需要多長時間？」, 번역 「안녕하세요, 오늘 치료가 얼마나 걸리는지 여쭤보고 싶어요.」, 음성 212,992 바이트. 끝나고 그 서버 프로세스만 종료(포트 비어 있음 확인) |
| 기능 폴더 밖 import · 사용자 포트(8600 · 3600) | 없음 · 안 건드림 |

단위 시험(`tests/test_interpret.py`): `<end>`/`<fin>` 까지 발화 묶기 · non-final 갈아 끼우기 · 바뀌지 않은 caption 다시 안 보냄 · 빈 발화 건너뜀 · side me/them · 번체는 중국어 자막만, TTS 는 간체 · flush · 잘못된 start 5종 · STT/TTS 설정값 · WS 전체 흐름(가짜 Soniox) · 클라가 그냥 닫아도 Soniox 두 연결 닫힘 · 오류 코드 3종(`no_api_key` · `soniox_unavailable` · `bad_request`) · 다른 Origin 거절.

## 계약 대조 — interpret-ws-contract · SPEC §7

| 항목 | 판정 | 비고 |
|---|---|---|
| start `{type,lang,scheduleId,traditional}` | 같음 | `lang` 은 §7.2 모달 언어 8개(zh · en · ja · th · fr · es · tl · hi). 그 밖 · `ko` · 첫 프레임이 start 가 아님 · 10초 안에 start 없음 → `bad_request` |
| 클라 PCM s16le 16kHz mono | 같음 | |
| pause/resume · stop | 같음 | pause 때 Soniox 에 `finalize` 를 보내 말하던 것을 바로 확정한다(자막 · 음성이 나옴) |
| ready · caption · audio_start · PCM · audio_end · error | 같음 | `audio_start.sampleRate` 24000 · `format` 없음 |
| side(원문 ko → me) | 같음 | 원문 토큰 언어의 최빈값 |
| 번체: 자막의 중국어만, TTS 는 간체 | 같음 | `s2tw` 하나로 TW · HK |
| 오류 코드 3종 | 같음 | 오류 뒤 서버가 닫는다. 중계 도중 Soniox 가 끊겨도 `soniox_unavailable` |
| WS Origin = `CC_FRONT_ORIGIN` | 같음 | Origin 헤더가 없는 클라(스크립트)는 허용 |
| 음색 하나 고정(D-17) | 같음 | `Jiwoo` |

## 이슈 · 코디가 확인할 것

1. **번역문 띄어쓰기가 어색할 때가 있다** — Soniox 번역 토큰을 그대로 이어서 「治療前 我會先塗」처럼 중국어 문장에 빈칸이 들어간다. 원문 그대로 두었다(고치려면 중국어 번역만 빈칸을 지우는 후처리).
2. **음성은 발화가 확정(`<end>`, 말 끝나고 최대 1초)된 뒤 번역문 전체를 TTS 로 보낸다.** 계약대로 「확정 발화의 번역문」. 실측: final caption 과 `audio_start` 가 같은 시각에 오고, 음성 조각이 이어서 스트리밍된다. 더 빠르게 하려면 번역 토큰을 오는 대로 TTS 에 흘리는 방식(공식 데모)이 있지만, 스트림 텍스트 공백 타임아웃 위험이 있어 이번엔 안 했다.
3. **한 세션에 TTS 스트림은 한 번에 하나**(발화 순서대로 줄 세움). 그래서 세션 3개까지는 TTS 동시 한도 3 안이다. 닫기 · stop · 오류 · 브라우저가 그냥 닫는 경우 모두 Soniox 두 연결을 닫는 걸 시험으로 확인했다.
4. 광둥어(②)는 격식체 녹음 하나로만 봤다. HK 고객 구어로는 시연 전 사람 목소리 1회 확인을 권한다.
5. 번체 변환은 대만 글꼴(`s2tw`) 하나다 — 홍콩 글꼴 차이(예: 綫/線)는 반영하지 않는다(계약에 지역 구분 필드가 없음).

## fix1 — 중국어 · 일본어 · 태국어 문장 속 빈칸 제거 (이슈 1)

- `app/service/interpret/assembler.py` 에 `squeeze_spaces(text, lang)` 를 추가했다. 언어가 `zh` · `ja` · `th` 일 때만, **양옆이 띄어쓰기 없는 문자인 빈칸만** 지운다. 대상 문자는 CJK 한자(확장 A · 호환 포함) · 히라가나/가타카나 · 태국 문자 · 전각 구두점(CJK 기호 U+3000–303F · 전각형 U+FF00–FFEF)이다. 영문 · 숫자 옆 빈칸은 그대로 둔다(「打 20 分钟」 유지)
- 적용 위치: 자막 `original` · `translation`(각각 그 텍스트의 언어로 판단), **TTS 로 보내는 번역문**
- 번체 변환 전에 지운다. OpenCC 는 빈칸 · 문자 종류를 바꾸지 않아서 전후 어느 쪽에서 해도 결과가 같다(시험으로 확인)
- 시험 9개 추가(언어별 8 + 자막 · TTS · 번체 순서 무관 1). `uv run pytest` **45 passed** · `uv run ruff check .` **All checks passed**
- 실물 재호출은 하지 않았다(토큰 이어 붙이기 후처리만 바뀜)
