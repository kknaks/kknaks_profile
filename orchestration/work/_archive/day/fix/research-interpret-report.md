# 통역 서버를 DAY 로 옮기려면 — 원천 두 곳 조사 (researcher · read-only)

> 2026-11-11 · task_8d6f416b5554 · 배경 = `e2e-feedback.md` 「버그 기록」 5번 · 그림 `e2e-shots/05-app-interpret-not-connected.png`(「통역 서버가 로그인을 받지 않았어요 — 다시 로그인해 주세요」 · 「연결 안 됨」 — 그림으로 확인)
> 읽은 ref: cc-prototype `origin/main` 77173cf(통역 파일은 로컬 main dbf0b53 과 같음 — `git diff --stat` 0) · interpret-pwa `origin/main` 17c26b5(로컬 main 은 뼈대 커밋 6a03d82 뿐이라 `git show origin/main:` 으로 읽음) · CENTURION_DAY 워크트리 `fix`(1975ee4f) · mediness `fix-spec` 워크트리(0d69a207 · planner 가 고치는 중 — 읽은 때 기준)
> 실제 Soniox · KOS · 서버 호출 없음. 키 · 토큰 · 기록 원문 없음(env 이름 · 칸 이름만).

## 세 줄 결론

1. **토큰만으로는 안 된다.** DAY 서버에는 `WS /api/interpret` 라우트 · Soniox 중계 · 사전 로딩 · 키 설정 칸 · Key Vault 이름이 **전부 없다** — 없는 경로라서 Starlette 가 accept 전에 닫고 uvicorn 이 403 을 낸다(§3-덧). 통역 로직을 옮겨 와야 한다.
2. **바탕은 interpret-pwa back** 이 맞다 — 앱(`interpret_client.dart` · `langs.dart`)과 DAY SPEC-003 §3 「통역」이 이미 interpret-pwa 계약(언어 7개 · `traditional` 없음 · 일반 오류 문구 · 사전 context)으로 짜여 있고, cc-prototype 원형에는 운영 장애를 낸 TTS keepalive `{}` 가 그대로 남아 있다. 인증만 DAY 세션(앱 Bearer + `board` view)으로 갈아 끼운다.
3. **앱은 안 고쳐도 된다** — 앱이 보내고 받는 메시지 · 필드 · 언어 코드 · 닫힘 처리가 interpret-pwa 서버와 필드 단위로 전부 맞는다(§3 표). 남는 건 하나: 앱은 핸드셰이크 403 을 모두 「로그인 거절」로 보이는데, 서버가 생겨도 「권한 없음」과 「세션 없음」을 앱이 구분하지 못한다(고칠지는 §8 Q-9).

---

## 1. 원형 서버 흐름 (cc-prototype `procedure/back`)

원형 = `procedure/back/app/api/interpret.py`(65줄) + `app/service/interpret/{session 221 · soniox 137 · assembler 134 · chinese 18}.py` · 시험 `tests/test_interpret.py` 316줄. cc 의 SPEC-004 §4 가 「이전 PoC `cc/back` 에서 복사 · 인증만 바꿈」으로 정했다(`para/projects/summer-star/cc-prototype/20-spec/spec-004-procedure-app.md:378-416`).

| 항목 | 원형 | 근거 |
|---|---|---|
| 경로 | `WS /api/interpret` | `api/interpret.py:15,50` |
| 인증 | 헤더 `Authorization: Bearer <토큰>` 또는 `?token=` · `accept()` **전에** 검증 · 실패면 `close(1008)`(클라이언트에는 핸드셰이크 403) · `Origin` 이 있으면 `PROC_INTERPRET_ORIGIN`(비면 `PROC_FRONT_ORIGIN`)과 같아야, 없으면(앱) 토큰만 · 토큰은 cc 자체 HMAC 토큰(`auth.verify`) · 세 역할 모두 | `api/interpret.py:43-63` · `service/auth.py:83-95` · spec-004 §4.2 |
| 앱 → 서버 | ① 첫 텍스트 `{type:"start", lang, traditional, scheduleId}` — `lang ∈ {zh,en,ja,th,fr,es,tl,hi}`(8개) · `traditional` bool(기본 false) · `scheduleId` 받아서 버림 · 10초 안에 안 오면 `bad_request` ② 바이너리 PCM ③ `{type:"pause"}` · `{type:"resume"}` · `{type:"stop"}` | `session.py:22-23,44-59,142-170` |
| 서버 → 앱 | `{type:"ready"}` · `{type:"caption", id, side:"me"\|"them", original, translation, final}` · `{type:"audio_start", id, sampleRate:24000}` · 바이너리 PCM · `{type:"audio_end", id}` · `{type:"error", code, message}` | `session.py:3-4,112,193-196` · `assembler.py:117-122` |
| 오디오 | 입력 PCM s16le 16 kHz mono(앞단 640샘플 = 40 ms 조각) · 출력 PCM s16le 24 kHz mono | `soniox.py:19-20,31-33` · spec-004 §4.3 |
| Soniox STT | `wss://stt-rt.soniox.com/transcribe-websocket` · 모델 `stt-rt-v5` · `language_hints: ["ko", lang]` · `enable_endpoint_detection: true` · `max_endpoint_delay_ms: 1000` · **번역 = `translation: {type:"two_way", language_a:"ko", language_b:lang}`**(Soniox 가 전사와 번역을 같이 냄 — 우리 쪽 번역 엔진 없음) · 키는 `Authorization: Bearer` 헤더로만 | `soniox.py:13-15,28-38,79-81` |
| 발화 묶기 | 토큰 `<end>`(끝 감지) · `<fin>`(수동 확정)까지가 한 발화 · final 토큰은 쌓고 non-final 은 갈아 끼움 · 같은 caption 재전송 안 함 · `side` = 원문 언어가 `ko` 면 `me` · zh · ja · th 문장 속 빈칸 정리 | `assembler.py:1-27,59-134` |
| TTS | **서버가 Soniox TTS 로** — `wss://tts-rt.soniox.com/tts-websocket` · 모델 `tts-rt-v2` · 음색 `Jiwoo` 고정 · 확정 발화의 번역문을 큐로 하나씩(`audio_start` → 조각 → `audio_end`). 「빠른 말하기」만 기기 TTS(서버 안 거침) | `soniox.py:14-18,41-49,117-128` · `session.py:188-199` · spec-004 §5 |
| 세션 수명 | 시간 상한 없음 · `start` 대기 10초 · `stop` 뒤 남은 토큰 3초 기다림(drain) · STT keepalive `{"type":"keepalive"}` 10초(오디오 없을 때 — Soniox STT 40초 idle 끊김 방지) · TTS keepalive **`"{}"`** 20초 | `session.py:23-26,124-127,201-210` · `soniox.py:87-88,133-134` |
| 끊김 · 정리 | 앱이 닫거나 · `stop` · 오류 → Soniox STT · TTS 두 연결을 반드시 닫음(주석: 「TTS 동시 한도 3」) · 서버는 재연결하지 않음 · 동시 세션 상한 없음 | `session.py:5,212-221` · spec-004 §4.2 「동시 연결」 · cc OQ-612 |
| 오류 코드 | `bad_request`(start 아님 · JSON 아님 · 언어 밖 · 10초 · 알 수 없는 type) · `no_api_key`(키 비었음 — 문구 「SONIOX_API_KEY 가 procedure/.env 에 없어요」) · `soniox_unavailable`(연결 · 인증 실패 / 중계 중 오류) — 문구에 env 이름 · 받은 값이 들어감 | `session.py:99-111,131-136,156,170` |
| `chinese.py` | OpenCC `s2tw`(간체 → 대만 번체) 한 줄 함수. Soniox 중국어 전사 · 번역은 **간체로만** 나오므로 `traditional=true` 면 **자막의 zh 쪽만** 번체로, TTS 에는 간체를 넣는다(번체를 넣으면 발음이 깨짐 — 2026-10-13 실물) | `chinese.py:1-18` · `assembler.py:113-115` |
| 설정 env | `SONIOX_API_KEY` · `PROC_INTERPRET_ORIGIN` (+ 토큰 검증용 `PROC_SESSION_SECRET` · `PROC_FRONT_ORIGIN`) | `config.py:55-59` |
| 주입 | `container.open_stt` · `open_tts` = Soniox 연결 팩토리(시험에서 가짜) | `container.py:53-55` |
| 의존성 | `websockets>=17.2` · `opencc-python-reimplemented>=0.1.7` | `pyproject.toml:12-13` |

## 2. interpret-pwa 가 원형에서 바꾼 것

interpret-pwa back = 원형을 **복사(import 아님)** 해 고쳤다(`back/app/service/interpret/session.py:1-16` docstring · SPEC-001 §5.1 표 `para/projects/summer-star/interpret-pwa/20-spec/spec-001-interpret-pwa.md:616-633`).

| 항목 | 원형(cc) | interpret-pwa | 근거 |
|---|---|---|---|
| 중계 구조 · 메시지 모양 · 오디오 형식 · 모델 · 음색 · keepalive 주기 · drain | — | **그대로** | SPEC-001 §5.1 |
| `start.lang` | 8개 `{zh,en,ja,th,fr,es,tl,hi}` | **7개 `{en, ja, zh, zh-Hant, th, vi, yue}`** — 중국 · 대만 · 광둥어 별개(D-28). `zh-Hant` · `yue` 는 Soniox 엔 `zh` | `langs.py:13-16` · D-04 · D-28 |
| `traditional` · `scheduleId` | 받음 | **무시** — 번체 여부는 `lang` 이 정함 | `session.py:62-74` |
| 번체 변환 | `traditional` 이면 `s2tw` | lang 별: `zh-Hant` = `s2tw` + 낱말 표 「激光 → 雷射」 · `yue` = `s2tw` · `s2twp` 폐기(D-32 → D-35) | `langs.py:21-25,55-68` · `chinese.py` 27줄(`t2s` 추가) |
| **사전(용어집)** | 없음 | **STT 설정에 `context` 를 싣는다**(아래 「사전 구조」) | `glossary.py` 285줄 · D-05 · D-18 · D-33 |
| `ready` 시점 | STT · TTS 열자마자 | STT 열기 → 첫 메시지 최대 2초 기다려 설정 확인 → `invalid_request` 면 **정방향 기본만으로 STT 1회 재연결** → TTS 열기 → `ready` | `session.py:41,158-193` · SPEC-001 §4.6.1 |
| TTS keepalive | `"{}"` | **`{"keep_alive": true}`** · 남의 stream_id 오류는 발화를 끊지 않음 — **원형 `{}` 가 운영 장애(2026-10-27 02:07 · 50초 뒤 끊김)를 냈다** | ipwa `soniox.py`(diff) · SPEC-001 §5.8 · cc `soniox.py:133-134` 에 아직 `{}` |
| TTS 입력 | 번역문 그대로 | **괄호 부분 뺀 문자열**(자막은 그대로 · 다 빠지면 TTS 안 보냄 · D-19) | `assembler.py strip_parens` · `session.py:281-296` |
| 오류 문구 | env 이름 · 받은 값이 들어감 | **코드는 그대로 · 문구 일반 4종**(「요청을 처리할 수 없어요」 · 「통역 서버를 쓸 수 없어요」 · 「통역 서버에 연결하지 못했어요」 · 「통역 연결이 끊겼어요」) · 알 수 없는 프레임은 끊지 않음(D-37) | `session.py:36-40,245,261` · SPEC-001 §5.4 |
| 오류 로그 | 예외 종류 | `channel · error_type · request_id` + 그때 상태(종류 · 길이 · 시각만 — 발화 원문 0) | `session.py:311-321` |
| 인증 | 원형 그대로 — 헤더 또는 `?token=` · 허용 출처 `INTERPRET_FRONT_ORIGIN` · 토큰은 env 계정 하나(D-06) | `api/interpret.py:42-66` · `config.py:19-27` |
| 모드(자동 듣기 / 누르고 말하기) | — | **앞단(front)만** — 누름 = `resume` · 뗌 = `pause`(기존 메시지 그대로 · **back 무변경**, D-36) | decision-001 D-36 |
| 통역 기록 | 없음 | **서버 볼륨 JSONL**(`INTERPRET_RECORD_DIR` · 날짜별 파일 · session_start · utterance(원문 · 번역 · side · 걸린 term id) · session_end · 음성 없음 · 7일 뒤 삭제 · 화면 · API 없음 · 비면 끔) | `records.py` 238줄 · D-41 · SPEC-001 §5.9 |
| 언어별 줄이기 한도 | — | context 글자 수 한도 언어별(en 23424 · ja 20419 · zh 20933 · zh-Hant 21689 · th 21343 · vi 22891 · yue 21123 — 시드 .6 실측 통과 최대치 × 0.9) · env `GLOSSARY_CONTEXT_MAX_CHARS` 가 있으면 전부 덮음 | `langs.py:28-44` · `config.py:32-34` |
| 밖으로 내는 것 | — | 용어집 API · 메뉴 삭제 · `/docs` 끔 · 사전은 Soniox context 로만(D-37) | D-37 |

**사전 구조**(`back/seed/glossary.json` · `version 2026-10-27.6` · 264 KB):

- 머리: `schema`(=1) · `version` · `langs`(7개 정확히) · `imported_from`(선택) · `terms` — 모르는 키는 기동 실패(`glossary.py:27-30,126-184`)
- term: `id` · `category` · `ko`(대표명) · `ko_aliases[]`(선택) · `entries{lang: entry}` · `note`(선택)
- entry: `name`(현지명 — 정방향 target · TTS 가 읽는 말 · 괄호 금지) · `aliases[]`(역방향 source 로만) · `source`(`procedure-hub` · `draft-s2twp` · `manual` · `web-research YYYY-MM-DD`) · `reviewed` bool · `raw` · `note`
- **건수**(파일을 직접 셈): term 170 · 카테고리 16(보톡스 27 · 기기 리프팅 18 · 메디컬스킨케어 17 · 레이저 15 …) · 7개 언어 각 170 entry(합 1,190) · `ko_aliases` 0 · source procedure-hub 901 / web-research 210 / draft-s2twp 51 / manual 28 · reviewed true 951 / false 239
- 싣는 방법: 기동 때 한 번 읽고 검사(깨지면 **기동 실패**) → 세션 `start` 마다 고른 lang 으로 `context = {general(피부과 고정 3쌍), terms(ko 대표명 · 별칭), translation_terms(정방향 기본 → 정방향 별칭 → 역방향 기본 → 역방향 별칭)}` 조립 · `zh-Hant` · `yue` 는 `t2s` · 한도를 넘으면 terms → 역방향 별칭 → 역방향 기본 → 정방향 별칭 순으로 뒤에서 뺀다(정방향 기본 · general 은 안 뺌)(`glossary.py:202-285` · `container.py:46-56`)
- 고치는 법: PR 로 시드를 고쳐 **재배포**. Procedure Hub 는 첫 가져오기 원천일 뿐 런타임에 안 부름(D-33 · `scripts/import_glossary.py` — 출력 파일이 있으면 안 씀)

**어느 쪽을 DAY 의 바탕으로 — 근거**(판단은 §8 Q-1)

| 근거 | 가리키는 쪽 |
|---|---|
| 앱이 이미 interpret-pwa 계약으로 짜여 있다 — 「`traditional` 칸은 뺌 — §5.1」 · 언어 7개 = interpret-pwa §5.5 그대로 · 「프로토 8개는 따르지 않는다」 | `app/lib/interpret/interpret_client.dart:1-7` · `langs.dart:1-3` |
| DAY SPEC-003 §3 「통역」 = 「interpret-pwa §5 의 WS 계약을 DAY 서버로 옮긴 모양」 · 사전 = interpret-pwa 시드 `2026-10-27.6` 읽기 전용 그대로 · 오류 = interpret-pwa §5.4 | `products/day/20-spec/spec-003-mobile-app.md:548-561` |
| 원형 서버를 그대로 쓰면 앱 7개 중 `zh-Hant` · `vi` · `yue` 3개가 `bad_request` 로 거절된다 | cc `session.py:22,53-55` |
| 원형엔 TTS keepalive `{}` 버그(운영 장애 원인)가 남아 있다 | cc `soniox.py:133-134` · ipwa SPEC-001 §5.8 |
| 원형 오류 문구는 env 이름(`procedure/.env`)을 앱 화면에 띄운다 — 앱은 `message` 를 그대로 보인다 | cc `session.py:103` · 앱 `interpret_client.dart:233` |
| 원형이 더 나은 점: 파일이 적고(사전 없음) 언어 8개(fr · es · tl · hi) — 앱은 그 넷을 안 쓴다 | — |

## 3. DAY 앱이 기대하는 계약 — 코드에서 전부 센 것

앱 코드: `app/lib/interpret/interpret_client.dart`(342줄) · `audio_io.dart`(175) · `langs.dart`(90) · `state/interpret_controller.dart` · `ui/interpret_widgets.dart` · `ui/room_screen.dart:62,74`.

**핸드셰이크 · 닫힘**

| 앱이 하는 것 | 근거 | cc 원형 | interpret-pwa | 맞나 |
|---|---|---|---|---|
| 주소 = 세션 `api_base_url` 의 `http→ws` · `https→wss` + `/api/interpret` | `interpret_controller.dart:151` · `core/origin.dart:77-80` | 같은 경로 | 같은 경로 | ○ |
| 직접 업그레이드(리다이렉트 안 따라감) · 헤더 `Authorization: Bearer <세션 토큰>` · `Connection: Upgrade` · `Upgrade: websocket` · `Sec-WebSocket-Key/Version 13` · `Cache-Control: no-cache` · **`Origin` 안 보냄** · `?token=` 안 씀 · 10초 타임아웃 | `interpret_client.dart:67-95,48-65` | 헤더 Bearer 받음 · Origin 없으면 토큰만 | 같음 | ○ |
| 101 아닌 응답의 HTTP 상태가 401 · 403 → 「통역 서버가 로그인을 받지 않았어요 — 다시 로그인해 주세요」 · 그 밖 실패 → 「통역 서버에 연결할 수 없어요」 | `:112-113,122-124,169-173` | 인증 실패 = accept 전 1008 → 403 | 같음 | ○(뜻은 §3-덧) |
| 연결 뒤 서버가 close **1008** 로 닫으면 「로그인을 받지 않았어요」 · 그 밖 닫힘 → 「통역 서버와 연결이 끊겼어요」 · 오류 이벤트 → 끊김 | `:187-193` | 연결 뒤 1008 을 쓰는 곳 없음(오류 뒤엔 기본 1000) | 같음 | ○(앱 쪽 갈래가 하나 남는다 — 서버가 세션 만료로 끊을 때 1008 을 쓰면 그대로 맞물림 · §4) |
| WS ping 20초 | `:93` | uvicorn 이 자동 pong | 같음 | ○ |

**앱 → 서버 메시지**

| 프레임 | 앱 | cc 원형 | interpret-pwa | 맞나 |
|---|---|---|---|---|
| 첫 텍스트 | `{"type":"start","lang":<code>}` — 연결 직후 한 번 | `lang` 8개 · `traditional` 기본 false | `lang` 7개 · 나머지 무시 | **ipwa ○ · cc ✗**(`zh-Hant` · `vi` · `yue` 거절) |
| `lang` 값 | `en · ja · zh · zh-Hant · th · vi · yue`(대소문자 `zh-Hant`) | `{zh,en,ja,th,fr,es,tl,hi}` | `APP_LANGS` 같은 7개 | ipwa ○ |
| 바이너리 | PCM16 16 kHz mono · 1,280 바이트(640샘플 · 40 ms) · `listening` 이고 번역 음성 재생 중이 아닐 때만(재생 끝 + 400 ms 뒤 재개) | 16 kHz s16le mono | 같음 | ○ |
| `{"type":"pause"}` · `{"type":"resume"}` | 마이크 원 버튼 토글(멈춤 ↔ 듣기) | finalize · 재개 | 같음 | ○ |
| `{"type":"stop"}` | 닫기 · 언어 바꿈 · 다시 연결 · 앱이 뒤로 감(`AppLifecycleListener onHide`) 때 보내고 바로 소켓 닫음 | stop → STT end → 3초 drain | 같음 | ○ |
| `traditional` · `scheduleId` | 안 보냄 | 기본값 처리 | 무시 | ○ |

근거: `interpret_client.dart:195,199-203,289-309` · `audio_io.dart:14-15` · `interpret_controller.dart:98-107,216-235` · `room_screen.dart:74`.

**서버 → 앱 메시지**

| 프레임 | 앱이 읽는 칸 | 서버(둘 다) | 맞나 |
|---|---|---|---|
| `ready` | `type` — connecting → listening | `{type:"ready"}` | ○ |
| `caption` | `id`(세대 접두어 붙여 키) · `side`(`me` 아니면 `them`) · `original` · `translation` · `final == true` · 같은 키면 덮어씀 | 같은 칸 | ○ |
| `audio_start` | `sampleRate`(없으면 24000) — 마이크 막음 | `{id, sampleRate:24000}` | ○ |
| 바이너리 | PCM16 · 홀수 바이트 이월 · 직전 `sampleRate` 로 재생 | 24 kHz PCM | ○ |
| `audio_end` | — 재생 끝 + 400 ms 뒤 마이크 재개 | `{id}` | ○ |
| `error` | `message`(비면 `code`)를 그대로 화면에 · 상태 error · 소켓 닫음 | `{code, message}` | ○ — 문구는 ipwa 일반 문구가 SPEC-003 「오류」 줄과 맞음 · cc 문구는 env 이름이 화면에 나감 |
| 모르는 `type` | 무시 | — | ○ |

근거: `interpret_client.dart:205-253`.

**판정**: interpret-pwa 서버 계약 그대로 DAY 서버를 지으면 **앱은 고칠 곳이 없다**. 앱 쪽 차이로 남는 것은 화면 이름뿐(`zh-Hant` 한국어 이름 앱 「중국어(번체)」 · ipwa 「대만어」 — 서버와 무관 · 사용자 2026-11-10 확정 `langs.dart:18`). 「누르고 말하기」(D-36)는 앱에 없고(`interpret_widgets.dart:412` 토글만) 서버와 무관하다.

**덧 — 「없는 경로 403」이 「로그인 거절」로 보이는 까닭**

1. DAY 에 `/api/interpret` 라우트가 없다(`backend/` 에 `WebSocket` · `interpret` · `soniox` 0건 — `grep -rn` 확인).
2. Starlette 라우터는 맞는 라우트가 없는 **WebSocket** 요청을 `not_found` 에서 `WebSocketClose()` 로 accept 전에 닫는다(`.venv/.../starlette/routing.py:629-633` · starlette 1.10.0). uvicorn 은 accept 전 close 를 **HTTP 403** 으로 응답한다(dev 로그 `WebSocket /api/interpret 403` 과 일치).
3. 앱 `isAuthRejection()` 이 401 · 403 을 권한 거절로 보고(`interpret_client.dart:112-113`) `connect()` 의 catch 가 `interpAuthRejected` 문구를 고른다(`:171-172` · 문구 `:124`).

→ 서버가 생기면 이 증상은 사라진다. 하지만 서버가 생긴 뒤에도 **원형 방식(accept 전 close 1008)은 모든 거절을 403 하나로** 보낸다 — 세션 없음 · 만료 · **`board` 권한 없음** · (만약 둔다면) Origin 거절이 앱에선 전부 「다시 로그인해 주세요」다. 권한 없는 사람은 앱이 시술현황 자체를 막아 드로어에 닿기 어렵지만(SPEC-003 U-2), 권한이 연결 중에 회수되면 「다시 로그인」이 틀린 안내가 된다(§8 Q-9).

## 4. DAY 서버에 놓을 자리

**AGENTS.md 계층에 맞춘 배치**(기능 하나 = 같은 파일 이름 · `AGENTS.md:62-81`)

| 무엇 | 자리(제안) | 비고 |
|---|---|---|
| WS 라우트 | `backend/day/routers/api/interpret.py` · `day/public.py api_routers()` 에 등록 | router 는 HTTP(WS)만 · DB 직접 금지(`AGENTS.md:73`) |
| 중계 세션 · Soniox · 자막 조립 · 번체 · 언어 표 | `backend/day/services/` — interpret-pwa `session · soniox · assembler · chinese · langs` | 지금 `services/` 는 평평한 파일들(`apns.py` · `chat_push.py` …) — 하위 폴더 `services/interpret/` 로 둘지 `interpret_*.py` 로 펼칠지는 구현 몫 |
| 사전 로더 · context 조립 | `backend/day/services/glossary.py`(또는 `interpret_glossary.py`) · 값 묶음(`ContextParts` · `Term` · `Entry`)은 `day/dtos/` 가 규칙상 자리 | |
| 시드 파일 | `backend/day/` 아래(예 `day/seed/glossary.json`) | `deploy/Dockerfile:16` 이 `backend` 를 통째로 복사 → 이미지에 자동 포함 |
| 시드 기동 때 읽기 | `runtime/main.py` lifespan → **`day.public` 경유**(runtime 은 `day.public` 만 import — `test_import_boundaries.py` · `AGENTS.md:76-77`) | 지금 lifespan 은 정리만 함(`runtime/main.py:22-28`) |
| 설정 칸 | `backend/common/config.py Settings` | §5 |
| 시험 | `backend/tests/day/` — ipwa `test_interpret` · `test_context` · `test_seed` 를 DAY fixture 로 + 인증 시험 | |

**인증(앱 Bearer 세션)을 WS 에 붙이는 법 — 기존 SSE 와 비교**

- SSE(`GET /api/board/stream`)는 HTTP 라 `Depends(current_session)` → `sessions.require_permission(board, VIEW)` → `await session.close()` 로 DB 세션을 돌려놓고, 연결 중에는 `stream_guard`(10초마다 `sessions.still_allowed` — 세션 생존 · 권한, 자기 짧은 DB 세션) · 수명 = 세션 만료와 1시간 중 이른 쪽(`routers/api/board.py:121-145` · `routers/board.py:349-356` · `routers/api/streams.py:22-24,43-85` · `services/sessions.py:187-205`).
- **WS 에서는 `day/session.py current_session` 의존성을 그대로 못 쓴다** — `Request` 타입 인자라 FastAPI 가 WebSocket 연결에는 값을 넣지 않는다(`fastapi/dependencies/utils.py:771-774` · fastapi 0.162.0). 그리고 `ServiceError` 예외 처리기(`runtime/main.py:31-33,49`)는 HTTP 응답용이라 WS 에선 안 탄다.
- 그래서 라우트에서 직접: 헤더 Bearer 를 읽고(`day/session.py:43-46 _bearer` 와 같은 규칙) → `async with get_async_session()` 짧게 열어 `sessions.current_session(token, "bearer")` + `sessions.require_permission(BOARD_KEY, VIEW)` → `ServiceError` 면 **accept 전 `close(1008)`**(앱 기대 · SPEC-003 「통역」 경로 · 권한 줄) → DB 세션을 닫은 뒤 `accept()`. 연결 내내 DB 세션을 쥐지 않는다(풀 `database_pool_size 5 + overflow 5` — `common/config.py:81-82`).
- 권한 = `board` view(`is_admin` 포함) — SPEC-003 U-15 · OQ-A15 「시술 현황에서 그 고객 정보를 볼 수 있는 사람 모두」(`spec-003-mobile-app.md:372,555,764`).
- 세션 생존 재확인은 cc · ipwa 에 **없다**(핸드셰이크 때 한 번). SSE 처럼 주기마다 볼지는 §8 Q-6. 재확인해서 끊을 때 close 1008 을 쓰면 앱의 「연결 뒤 1008 = 로그인 거절」 갈래(`interpret_client.dart:189`)와 그대로 맞물린다.
- `?token=` · Origin 허용 출처: DAY 의 통역 사용자는 앱뿐(웹 화면에 통역 없음 — SPEC-002 · SPEC-003 범위) → 쿼리 토큰을 받을 이유가 없고, cc · ipwa 의 「Origin 이 있으면 허용 출처만」 칸은 DAY 에 대응 env 가 없다. 두 칸을 빼는 것이 원천과 다른 점(기술 기본값 — 스펙이 적을 것).

**새 의존성**

- `opencc-python-reimplemented`(번체 · `t2s`) — DAY `pyproject.toml:6-24` 에 없음. 순수 Python. DAY 는 Python **3.13**(`.python-version`) · cc · ipwa 는 3.12 — 3.13 에서 동작은 **확인 안 됨**(시험으로 확인할 것).
- `websockets`(Soniox 로 나가는 연결) — DAY `uv.lock` 에 **이미 있음**(`uvicorn[standard]` 경유 17.4 · `uv.lock:1069,1112-1115`). 직접 의존으로 적을지는 구현 몫.
- `httpx` 는 ipwa 가져오기 스크립트만 씀(런타임 무관).

**프로세스 · 동시 세션 · 메모리(B2s)**

- api = uvicorn **`--workers 1`**(`deploy/compose.yaml:41-51`) → 모든 통역 세션 · SSE · API 가 이벤트 루프 하나에 탄다. 세션 하나 = 앱 WS 1 + Soniox 나가는 WS 2 + asyncio 태스크 4(`session.py _pump`). 들어오는 오디오 32 KB/s · 나가는 TTS 48 KB/s(재생 구간).
- 루프를 막을 수 있는 동기 작업: OpenCC 변환(자막마다 · 작음) · 세션 시작 때 context 조립의 줄이기 루프(`glossary.py:261-264` — 뺄 때마다 전체를 `json.dumps` 해 잼). 실제 시간은 **확인 안 됨** — `AGENTS.md:127`(「async 경로에서 동기 I/O 로 루프를 막지 않는다 · 동시성 상한 명시」)에 걸리는지 측정 필요. 줄이기 결과는 언어별로 늘 같으므로 기동 때 7개를 미리 만들어 두면 세션마다 조립할 필요가 없다(구현 몫).
- **동시 세션 상한**: 원천 둘 다 「제한 없음」. 주석 · OQ 에 「Soniox TTS 동시 한도 3」(cc `session.py:5` · cc OQ-612) — 이 한도가 키 단위인지 계정 단위인지, 지금도 3 인지 **확인 안 됨**. DAY 는 병원 여러 곳 · dev · prod 가 같은 키를 쓰면 그 한도를 나눠 쓴다(§8 Q-4 · Q-5). AGENTS.md 「동시성 상한을 명시한다」(`:127`) 때문에 상한 값을 정해야 한다.
- 메모리: VM 한 대(B2s — 메모리 기록 `reference_day_vm`)에 dev · prod api 둘 + Caddy(`deploy/caddy/Caddyfile:1` 「두 도메인 … 같은 VM」). api 상한 dev 384m · prod 768m(`deploy/config/{dev,prod}.compose.env` — 「실측 아님」). 시드 파일 264 KB · OpenCC 사전 적재량 · 세션당 메모리 **확인 안 됨** → 배포 뒤 `docker stats` 로(`docs/development/deployment.md:115`).
- 배포(컨테이너 교체) · Caddy reload 때 열린 통역 세션은 끊긴다 → 앱은 「통역 서버와 연결이 끊겼어요」 + [다시 연결](`interpret_client.dart:189` · SPEC-003 U-15). 서버는 재연결하지 않는다(원천 그대로).

**Caddy · compose 가 WebSocket 을 통과시키나**

- Caddyfile = `reverse_proxy day-<env>-api:8000 { flush_interval -1 }` + `request_body { max_size 6MiB }`(`deploy/caddy/Caddyfile:6-14`). WS 전용 설정은 없다. Caddy v2 `reverse_proxy` 는 업그레이드 요청을 기본으로 통과시킨다(Caddy 문서 — 이 배포에서 101 까지는 **확인 안 됨**). 방증: dev 로그에 `WebSocket /api/interpret 403` 이 **uvicorn 에서** 찍혔다 = 업그레이드 요청이 Caddy 를 지나 api 까지 왔다.
- ⚠ `request_body max_size 6MiB` 가 업그레이드 뒤 스트림에도 걸리는지 **확인 안 됨**. 걸린다면 앱 오디오 32 KB/s 기준 **약 3분 15초**에 세션이 끊긴다 → 실물 시험에 「4분 넘는 세션 1회」를 넣어야 한다(§7).
- compose: api 는 `edge` 네트워크 별칭으로만 Caddy 에 닿음(`compose.yaml:52-56`) — 포트 · 프로토콜 추가 설정 없음. uvicorn `[standard]` 은 WS 를 받는다(지금 403 로그가 증거).

## 5. 비밀 · 설정

**Soniox 키 — 기존 선택 비밀 방식에 맞추면**

| 자리 | 추가할 것 | 근거 |
|---|---|---|
| `scripts/deploy/day_vm.py OPTIONAL_SECRETS` | `"<env 이름>": "soniox-api-key"` 한 줄 → Key Vault 이름 **`day-dev-soniox-api-key`** · **`day-prod-soniox-api-key`**(`secret_name()` 규칙 `day-<env>-<이름>`) · 한 줄 값이라 `MULTILINE_SECRETS` 아님 · `FORBIDDEN_CONFIG_KEYS` 에 자동 포함(일반 설정에 넣으면 배포 거부) | `day_vm.py:34-56,178-179,183-195` |
| 없을 때 | 선택 비밀은 「Key Vault 에 없으면 app.env 에 넣지 않는다(앱은 꺼짐 · 배포는 그대로 성공)」 → 통역 `start` 뒤 `error no_api_key`(「통역 서버를 쓸 수 없어요」) — ipwa 동작과 맞는다 | `day_vm.py:45-46` · ipwa `session.py:136-139` |
| `common/config.py` | `SecretStr` 칸 하나(APNs 키와 같은 모양 `day_apns_auth_key: SecretStr` `:157`) | |
| env 이름 | 후보: 원천 이름 `SONIOX_API_KEY`(cc · ipwa) / DAY 접두어 `DAY_SONIOX_API_KEY`(`DAY_APNS_*` · `DAY_CHAT_*` 와 같은 꼴) — 스펙이 고를 기술 기본값 | `common/config.py:137-164` |
| 값 넣기 | Key Vault 에 값을 넣는 것은 **사용자**(코디 · 워커는 이름만 — 메모리 「가짜 계정 금지」 · ipwa D-11) | |

**그 밖 설정 칸 후보**(원천에 있는 것)

| 칸 | 원천 | DAY 에서 |
|---|---|---|
| 허용 출처 `PROC_INTERPRET_ORIGIN` / `INTERPRET_FRONT_ORIGIN` | cc · ipwa | 앱만 쓰면 불필요(§4) |
| `GLOSSARY_CONTEXT_MAX_CHARS`(언어별 표를 한 값으로 덮기) | ipwa `config.py:32-34` | 선택 — 없으면 언어별 표(코드 상수) |
| `INTERPRET_RECORD_DIR` | ipwa | 기록을 둘 때만(§8 Q-7) — 지금 api 컨테이너엔 볼륨이 없다(`compose.yaml:103-131` 볼륨은 redis 뿐) |
| 동시 세션 상한 | 없음 | 정하면 일반 설정(`deploy/config/<env>.env`) 칸 하나 |
| `STT_CONFIG_CHECK_SEC` · keepalive 주기 · drain | 코드 상수 | 상수 그대로 |

## 6. 사전 등록

| | interpret-pwa 방식(레포 시드 파일 → 재배포) | DB 에 두기 |
|---|---|---|
| 정본 | `backend/day/…/glossary.json`(git) | DB 테이블 |
| 고치기 | PR → dev 배포 → prod fast-forward(`AGENTS.md:10-12`) | 화면 또는 SQL — **편집 화면은 스펙이 「요청 없음」으로 뺐다**(`spec-003-mobile-app.md:89`) |
| 깨진 값 | 기동 때 검사 · 실패면 기동 실패(ipwa §4.4) | 쓰기 때 검사를 따로 만들어야 |
| 병원별 사전 | 한 벌(파일 하나) | `hospital_id` 칸으로 가능 |
| 새로 지을 것 | 로더 · 검사 · context 조립 복사뿐 | 모델 · migration · 시드 적재 · 검사 · 캐시 · (편집 화면) |
| DAY `data_rules` 와 | 파일이라 DB 규칙(소프트 딜리트 · `created_at/updated_at/deleted_at` · UTC)은 해당 없음 | 모든 규칙 적용 + 아래 충돌 |
| 두 원천 문제 | interpret-pwa 시드 사본 — SPEC-003 이 「값을 새로 번역 · 고치지 않는다 · 고칠 땐 interpret-pwa 시드를 고치고 다시 가져온다」로 정본을 interpret-pwa 에 둠(`spec-003-mobile-app.md:558`) | DB 가 정본이 되면 interpret-pwa 시드와 갈라진다 |

**`day.json data_rules` 와 부딪히는 곳**(DB 로 갈 때)

- 「1차는 상품 · 시술 메뉴 테이블을 만들지 않는다 … 메뉴 설계는 `reference/2026-11-03-cc-day/04-1-menu.md`(자체 운영 단계)」 — 사전은 시술 이름 표라 메뉴 테이블과 겹친다. 사전을 DB 로 먼저 지으면 나중 메뉴 설계와 같은 사실(시술 이름)이 두 곳에 생긴다.
- 「병원(지점) id 를 업무 테이블에 둔다」(`AGENTS.md:78`) · 「각 병원은 독립 운영 주체」 — DB 테이블이면 병원별인지 공통(브랜드/전체)인지 먼저 정해야 한다.
- 「최종 목표는 DAY 자체만 쓰는 것」 — 레포 파일 방식은 DAY 바깥(interpret-pwa)을 정본으로 둔다는 점에서 이 방향과 반대다. 다만 외부 CRM(KOS · Vegas) 규칙이라 사전에 직접 적용되는지는 문서에 없다.

**지금 스펙의 상태**: DAY SPEC-003 §3 「통역」 이 이미 「interpret-pwa 시드 `2026-10-27.6` 을 읽기 전용으로 그대로 가져와」로 적었고(출처 = 사용자 2026-11-09 「통역에 interpret-pwa 외국어 매핑 사전 적용」 `spec-003-mobile-app.md:29`), 완료 확인 A-14 가 서버 로그 `glossary seed loaded: version=2026-10-27.6` 을 본다(`:716`). 사용자 2026-11-11 「사전도 따로 등록해야 해 interpret-pwa 처럼」도 같은 방향이다.

**병원마다 다른 사전**: **정한 적 없음.** DAY 문서(`products/day/` 전체 · 기획안 `00-baseline/planning/` — 「통역」은 근무표의 통역 인원뿐) · SPEC-003 · interpret-pwa 결정(계정 하나 데모 · D-06) 어디에도 병원별 사전 근거가 없다(`grep` 0건).

## 7. 규모

**가져올 것**(interpret-pwa `origin/main` · 복사)

| 파일 | 줄 | 어떻게 |
|---|---|---|
| `app/api/interpret.py` | 66 | 인증 부분 다시 씀(§4) |
| `service/interpret/session.py` | 343 | 그대로 + 기록기 뺄지(§8 Q-7) |
| `service/interpret/soniox.py` | 170 | 그대로(keepalive 고친 판) |
| `service/interpret/assembler.py` | 164 | 그대로 |
| `service/interpret/chinese.py` · `langs.py` | 27 · 73 | 그대로 |
| `service/glossary.py` | 285 | 그대로(위치만) |
| `seed/glossary.json` | 264 KB | 그대로(`2026-10-27.6`) |
| `container.py` 중 통역 부분 | 약 25 | DAY 모양으로 다시(팩토리 주입 · 사전 적재 · context) |
| 시험 `test_interpret` · `test_context` · `test_seed` (+ `conftest` 97 · `seed_tables` 179) | 678 · 409 · 302 | DAY fixture · 인증으로 고쳐서 |
| 실물 스크립트 `scripts/live_check.py` | 718 | 필요한 갈래만(seed · idle · zhhant) |
| (기록을 둘 때만) `records.py` · `test_records.py` | 238 · 430 | §8 Q-7 |

→ 코드 약 1,130줄 + 시험 약 1,400줄 + 시드. `import_glossary.py`(197)는 시드가 이미 있으니 안 가져옴.

**새로 써야 하는 것**

- WS 인증(DAY 세션 · `board` view · accept 전 1008 · DB 세션 짧게) + 시험(토큰 없음 · 틀림 · 만료 · 로그아웃 · 권한 없음 → 403 / 헤더 토큰 통과 / Origin 처리)
- (Q-6 을 고르면) 연결 중 세션 재확인 · 수명 상한
- `common/config.py` 칸 · `day_vm.py OPTIONAL_SECRETS` 한 줄 + 그 시험 · `deploy/config/*.env` 주석
- lifespan 사전 적재(`day.public` 경유) · 깨진 시드 기동 실패 시험
- 동시 세션 상한(정하면)
- `pyproject.toml` · `uv.lock`(`opencc-python-reimplemented`)
- `test_import_boundaries` 를 지키는 배치

**시험 방법**

- 단위: Soniox 가짜(원천 두 곳 모두 가짜 주입 시험 있음) · 앱은 이미 가짜 WS 로 시험됨(SPEC-003 D-3 줄 `:688`).
- **실물 Soniox 1회가 완료 조건인 자리**(메모리 「실물 e2e 없이 done 금지」):
  1. 서버 단독: `live_check` 류로 시드 context 연결이 7개 언어에서 거절 없이 열리는지(특히 `zh-Hant` — ipwa ⑬ 에서 줄이기 이분 탐색이 필요했던 언어) · ko ↔ 한 언어 왕복 · **멈춤 35초 뒤 두 번째 발화**(TTS keepalive 장애 재현 갈래 `idle`)
  2. dev 배포 뒤 TestFlight 실기기: [통역하기] → `ready` → 한국어 · 고객 언어 한 마디씩 → 자막 양쪽 · 번역 음성이 기기 스피커로 · 언어 바꾸기 · [종료] · 서버 로그 `glossary seed loaded: version=2026-10-27.6`(A-14)
  3. **4분 넘는 세션 1회**(Caddy 6MiB 본문 상한이 WS 에 걸리는지 · §4)
  4. 키를 비운 환경에서 `no_api_key` 문구 · 권한 없는 계정 403
- 키는 사용자가 Key Vault 에 넣어야 1 · 2 를 돌릴 수 있다.

## 8. 정할 것 (사용자 몫만)

| # | 정할 것 | 후보 | 근거 · 메모 |
|---|---|---|---|
| Q-1 | 서버 바탕 | **A. interpret-pwa back(추천)** — 앱 · SPEC-003 이 이미 이 계약 · keepalive 장애 고친 판 / B. cc-prototype 원형 + 고쳐 쓰기 — 언어 7개 · 사전 · keepalive 를 다시 고쳐야 | §2 · §3. 스펙이 이미 A 로 적혀 있어 확인만 |
| Q-2 | Soniox 키를 dev · prod 에 **같은 키**로 쓸지 **따로**로 쓸지 | 같은 키 하나(두 Key Vault 이름에 같은 값) / 환경별 키 | 비용 · 동시 한도를 나눠 쓰는지가 갈린다. Key Vault 에 값 넣기는 사용자 |
| Q-3 | 사전을 어디에 | **A. interpret-pwa 시드 파일 사본(추천 · 스펙 그대로)** — 고칠 땐 interpret-pwa 시드를 고쳐 다시 가져옴 / B. DAY DB 테이블 — data_rules 「1차 시술 메뉴 테이블 안 만듦」과 겹침 · 편집 화면 없음 | §6 · `spec-003-mobile-app.md:558` |
| Q-4 | 병원마다 다른 사전이 필요한가 | 아니오(전 병원 한 벌) / 예(→ Q-3 B 가 사실상 필요) | 정한 적 없음(§6) |
| Q-5 | 동시 통역 세션 상한 | 상한 없음(원천 그대로 · 넘으면 Soniox 오류가 `soniox_unavailable` 로 보임) / 서버 전체 N 개 / 병원당 N 개 | Soniox TTS 동시 한도 「3」은 원천 주석뿐 · 확인 안 됨. AGENTS.md 는 상한 명시를 요구 |
| Q-6 | 통역 중 로그아웃 · 세션 만료 · 권한 회수 때 | 핸드셰이크 때만 확인(원천 그대로) / SSE 처럼 주기마다 다시 보고 끊음(close 1008 → 앱 「다시 로그인」) | `routers/board.py:349-356` |
| Q-7 | 통역 기록(interpret-pwa D-41) | 안 남김(SPEC-003 에 없음 · 지금 스펙 그대로) / 남김 — 어디에(DB · Blob · 볼륨) · 얼마나 · 누가 봄 | 대화 원문 = 고객 발화. api 컨테이너엔 볼륨 없음. data_rules 「민감정보 암호화」 검토 필요 |
| Q-8 | interpret-pwa 시드를 고치면 DAY 에 언제 다시 가져오나 | 고칠 때마다 사람이 PR / 가져오기 시점을 정해 둠 | 두 원천이 생기는 자리 |
| Q-9 | 앱의 403 문구 | 그대로(서버 생기면 대부분 해소) / 서버가 권한 없음 · 세션 없음을 구분해 보내고 앱 문구를 나눔(앱 수정 필요 — 「앱은 안 고친다」 결론이 바뀜) | §3-덧. 문구를 지어 넣지 않는다 — 나눈다면 글자도 사용자가 |

## 확인 안 됨

- Soniox TTS 동시 한도 「3」의 실제 값 · 단위(키 · 계정) — 원천 주석뿐(Soniox 호출 금지라 확인 안 함)
- Caddy 가 이 배포에서 101 까지 통과시키는지(방증만 — 업그레이드 요청이 api 까지 옴) · `request_body 6MiB` 가 업그레이드 뒤에도 걸리는지
- `opencc-python-reimplemented` 의 Python 3.13 동작
- 세션당 메모리 · OpenCC 적재량 · context 줄이기가 루프를 막는 시간(실측 없음)
- 앱 「누르고 말하기」 부재가 의도인지(SPEC-003 U-15 는 원형 드로어 모양 그대로라고만 적음 — 서버와 무관)
