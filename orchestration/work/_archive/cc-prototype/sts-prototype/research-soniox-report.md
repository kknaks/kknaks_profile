# Soniox STS 조사 리포트 (2026-10-10)

- 조사자: cc-prototype `researcher` 워커 (task_3db1f4cad850)
- 정본: Soniox 공식 문서 `https://soniox.com/docs/*` (각 페이지 `.mdx` 원문, 2026-10-10 수집) · 공식 GitHub `soniox/*` · `soniox.com/pricing` 등 공식 제품 페이지
- 방법: 문서 읽기만. API 호출·코드 실행·설치 없음. 공식 문서에 없는 것은 「문서에 없음」으로 둠
- 표기: 〔공식 문서〕 = docs 페이지, 〔공식 예제〕 = soniox GitHub, 〔공식 마케팅〕 = soniox.com 제품·가격 페이지(문서보다 약한 출처), 〔비공식〕 = 제3자

---

## 결론 한 장 — 경로 후보

**요약: Soniox에는 단일 모델로 된 speech-to-speech가 없다.** Soniox가 말하는 STS는 공식적으로
**연결 두 개짜리 파이프라인**이다. ① STT WebSocket이 전사와 번역을 한 스트림으로 주고,
② TTS WebSocket이 번역 텍스트를 받아 오디오로 낸다. 둘을 앱 코드로 잇는다.
번역은 STT 안에 들어 있어서 따로 번역 단계를 두지 않아도 된다. 이 파이프라인은 Soniox 공식
문서에 「Real-time speech-to-speech translation」으로 올라 있고, **FastAPI + vanilla JS로 만든 공식 데모가 있다.**
(`/translation/sts-translation`, `/demo-apps/soniox-speech-to-speech-translation`)

| 경로 | 무엇이 되나 | 무엇이 안 되나 / 주의 |
|---|---|---|
| **P1. Soniox 단일 모델 STS(음성 입력 → 음성 출력 한 번에)** | — | **제공하지 않는다.** 공식 STS는 STT+TTS 두 연결을 앱 코드로 잇는 방식이다(`/translation/sts-translation` §How it works: "two Soniox WebSocket connections and a small piece of application logic between them") |
| **P2. Soniox STT(번역 내장) → Soniox TTS — 백엔드 중계(proxy)** | 한국어 STT·번역·TTS가 모두 지원 목록에 있다. 단방향과 양방향 번역, 발화 끝 `<end>` 감지, 번역 토큰을 문장 중간부터 스트리밍, 텍스트 조각을 넣으면 오디오 조각이 나오는 TTS. **공식 데모가 이 구조 그대로다(FastAPI 백엔드 + 브라우저).** 키가 서버에만 있다 | 사용자 한 명당 서버 WS 1개에 Soniox WS 2개가 붙는다(동시 연결 한도에 잡힘). 데모 README 기준 첫 음성까지 약 0.5–1.5초 |
| **P3. Soniox STT(번역 내장) → Soniox TTS — 브라우저 직결(direct)** | 공식 Web SDK `@soniox/client`와 React SDK `@soniox/react`가 마이크 캡처, STT·번역, 실시간 TTS를 모두 지원한다. back은 임시 키 발급 엔드포인트만 두면 된다. 공식 Next.js 예제가 있다(STT만) | STT 키와 TTS 키를 따로 발급해야 한다(`usage_type`이 다름). STT 결과를 TTS로 넘기는 로직이 브라우저에 들어간다. **STS 직결 공식 예제는 없다**(STS 데모는 proxy, Next.js 예제는 STT만) |
| P4. Soniox STT(번역 내장) → 타사 TTS | 기술적으로 가능 | Soniox TTS가 한국어, 대상 언어, 스트리밍을 모두 충족하므로 브리프 C 조건(빠지는 기능이 있을 때만)에 해당하지 않는다. §C 참고 |
| P5. Soniox STT → LLM 번역 → TTS | 가능 | 문서상 번역이 STT에 내장되어 있고 용어 고정(`translation_terms`)도 지원한다. LLM이 필요한 경우는 문서에 없다. §C-11 참고 |

---

## A. Soniox 기능 (질문 1~5)

### A-1. 제품·모델 목록

| 제품 | 현재 모델 | 상태·날짜 | 출처 |
|---|---|---|---|
| 실시간 STT(+번역) | **`stt-rt-v5`** | Active, 2026-06-16 출시. `stt-rt-v4`는 별칭으로 v5를 가리킴. v4는 2026-06-30에 제거 | 〔공식 문서〕 https://soniox.com/docs/stt/models |
| 파일(async) STT(+번역) | **`stt-async-v5`** | Active, 2026-06-11 출시 | 같은 곳 |
| 번역 | 별도 모델 없음. STT 요청의 `translation` 블록 | "Translation, already built into speech-to-text API" | 〔공식 문서〕 https://soniox.com/llms.txt · https://soniox.com/docs/translation/get-started |
| TTS(실시간 WS + REST) | **`tts-rt-v2`** | Active, 2026-08-11 GA. `tts-rt-v1`은 Deprecated(2026-08-31 제거 예정, 이후 v2로 자동 라우팅) | 〔공식 문서〕 https://soniox.com/docs/tts/models |
| Speech-to-speech | **단일 모델·엔드포인트 없음.** STT+번역과 TTS를 잇는 파이프라인 안내 페이지와 데모 앱만 있다 | — | 〔공식 문서〕 https://soniox.com/docs/translation/sts-translation |

- 그 밖에 음성 복제(voice cloning), 화자 분리, 언어 판별, 컨텍스트(용어집)가 있다. 〔공식 문서〕 https://soniox.com/docs/llms.txt
- 참고: 공식 STS 데모 `main.py`는 아직 `"model": "tts-rt-v1"`을 쓴다(deprecated, v2로 자동 라우팅). 〔공식 예제〕 https://github.com/soniox/soniox_examples/blob/master/apps/soniox-speech-to-speech-translation-demo/main.py

### A-2. 실시간 번역 — 모드·설정·토큰

**모드** 〔공식 문서〕 https://soniox.com/docs/translation/stt-translation §Translation modes
- 단방향 `one_way`: 감지된 모든 언어를 대상 언어 하나로 번역한다. `{"translation": {"type": "one_way", "target_language": "fr"}}`
- 양방향 `two_way`: 두 언어 사이를 오가며 번역한다(두 사람 대화용). `{"translation": {"type": "two_way", "language_a": "ja", "language_b": "ko"}}`. 문서 예시에 **ja↔ko**가 그대로 나온다
- 양방향에서 두 언어 밖의 말(예: fr)은 `translation_status: "none"`으로 **전사만 하고 번역하지 않는다** (같은 페이지 Token format 예시)

**설정 방법**: 실시간 STT 시작 메시지에 `translation` 블록 하나를 추가한다. 나머지는 일반 전사와 같다.
〔공식 문서〕 https://soniox.com/docs/translation/stt-translation/rt-translation §Quickstart

**원문 토큰과 번역 토큰이 나오는 방식**
- **같은 WebSocket, 같은 토큰 스트림**으로 온다. 토큰마다 `translation_status`가 붙는다: `"none"`(번역 대상 아님) / `"original"`(발화 원문) / `"translation"`(번역)
- 번역 토큰에는 `language`와 `source_language`가 있다. 타임스탬프(`start_ms`/`end_ms`)는 **원문 토큰에만** 있다
- 원문이 먼저 오고, 번역이 덩어리 단위로 뒤따른다. **문장이 끝나기 전에** 번역이 시작된다(mid-sentence)
- ⚠ "tokens are not 1-to-1 mapped and may not align": 원문 토큰과 번역 토큰이 1:1로 대응하지 않는다
- 〔공식 문서〕 https://soniox.com/docs/translation/stt-translation §Token format · https://soniox.com/docs/translation/stt-translation/rt-translation §How real-time streaming works

**최종/중간 구분**
- 모든 토큰에 `is_final`이 있다. non-final 토큰은 잠정값이라 바뀌거나 사라질 수 있고, final 토큰은 한 번만 오고 바뀌지 않는다. 〔공식 문서〕 https://soniox.com/docs/stt/rt/real-time-transcription §How processing works
- **번역 토큰도 non-final로 먼저 오는지, final로만 오는지는 문서에 없다.** 참고로 공식 STS 데모 `handle_stt`는 `is_final`을 보지 않고 `translation_status == "translation"`인 토큰을 전부 TTS 큐에 넣는다. 〔공식 예제〕 main.py L174–205. 그래서 번역 토큰이 final로만 온다고 **추정할 수 있지만 확인되지 않았다.** 프로토타입 첫 실물 호출에서 확인해야 한다(§정할 것 Q-7)

### A-3. 한국어

- STT: 지원 언어 60여 개에 **Korean `ko`** 포함. 전사·번역 모두 실시간과 async에서 지원. 〔공식 문서〕 https://soniox.com/docs/stt/concepts/supported-languages
- 번역 언어 쌍: 지원 언어끼리는 **어떤 쌍이든** 된다("Translation → Works between any pair of supported languages", 3,600쌍 이상). ko↔en·ja·zh·vi·th 모두 지원 목록에 있다(en, ja, zh, vi, th, ko 각각 표에 있음).
  - 전체 목록: https://soniox.com/docs/translation/supported-languages
- 한국어 품질 수치(WER 등): **문서에 없음.** 모델 변경 기록에 "Significantly higher translation quality, especially for languages such as German and Korean"(v3, 2025-10-21) 한 줄이 있을 뿐이다. 〔공식 문서〕 https://soniox.com/docs/stt/models §October 21, 2025. `soniox.com/benchmarks` 본문에도 한국어 항목은 없었다(2026-10-10 확인)
- 리전: 현재 US·EU·JP·IN. **Korea는 "Coming soon"**으로 나온다. 〔공식 문서〕 https://soniox.com/docs/data-residency §Regional endpoints · 〔공식 마케팅〕 https://soniox.com/text-to-speech (리전 절)

### A-4. 언어 자동 판별 · 화자 분리 · 발화 끝 감지

| 기능 | 설정 | 동작·제약 | 출처 |
|---|---|---|---|
| 언어 자동 판별 | `"enable_language_identification": true` | 토큰마다 `language` 태그가 붙고, 문장 단위로 일관되게 맞춰진다. 실시간에서는 일시 오분류나 **나중에 고쳐지는 경우**가 있을 수 있다. `language_hints` 사용 권장 | https://soniox.com/docs/stt/concepts/language-identification |
| 언어 제한 | `language_hints`, `language_hints_strict` | 기대하는 언어로 결과를 제한한다 | https://soniox.com/docs/stt/concepts/language-restrictions |
| 화자 분리 | `"enable_speaker_diarization": true` | 토큰마다 `speaker` 라벨. 세션당 최대 15명. 실시간은 async보다 정확도가 낮다. ⚠ **발화 끝 감지나 수동 확정을 켜면 화자 분리 정확도가 떨어진다** | https://soniox.com/docs/stt/concepts/speaker-diarization |
| 발화 끝 감지 | `"enable_endpoint_detection": true` | 의미 기반(semantic) 판정. 발화가 끝나면 앞선 토큰을 모두 final로 바꾸고 **`<end>` 토큰**(항상 final, 한 번)을 보낸다. 튜닝값: `max_endpoint_delay_ms`(500–3000, 기본 2000), `endpoint_sensitivity`(-1.0–1.0, v5 전용), `endpoint_latency_adjustment_level`(0–3, v5 전용). 빨리 끊을수록 인식 정확도가 조금 떨어지고 발화가 더 잘게 쪼개진다 | https://soniox.com/docs/stt/rt/endpoint-detection · https://soniox.com/docs/api-reference/stt/websocket-api §Parameters |
| 수동 확정 | `{"type": "finalize"}` 제어 메시지 → `<fin>` 토큰 | 버튼으로 말을 끊는 방식(push-to-talk)에 쓸 수 있다 | https://soniox.com/docs/stt/rt/manual-finalization |

- 공식 STS 가이드는 `<end>`로 현재 TTS 스트림을 닫으라고 권장한다. 공식 데모 설정은 `max_endpoint_delay_ms: 500`. 〔공식 문서〕 https://soniox.com/docs/translation/sts-translation §Things to consider · 〔공식 예제〕 main.py L16–25

### A-5. Soniox TTS

| 항목 | 답 | 출처 |
|---|---|---|
| 지원 언어 | 60여 개, **Korean `ko` 포함**. STT·번역과 같은 언어 집합(en, ja, zh, vi, th 포함). 단, zh는 간체만, sr/bs는 라틴 문자만, kk는 키릴 문자만 | https://soniox.com/docs/tts/concepts/supported-languages · https://soniox.com/docs/translation/supported-languages |
| 음색 | 큐레이션된 공용(shared) 음색이 있고, **모든 음색이 모든 언어를 말한다**(같은 음색으로 언어만 바꿀 수 있음). 문서 예시에 나오는 이름: Daniel, Adrian, Claire, Emma, Grace, Jack, Arthur, Isla, Cooper, Elise, Arjun 등. 전체 목록은 Console이나 `Get shared voices` API로 본다(호출하지 않음). 음성 복제도 지원 | https://soniox.com/docs/tts/concepts/voices · https://soniox.com/docs/tts/concepts/voice-cloning |
| 감정·속도 | 오디오 태그로 감정·톤 조절, `speed` 0.7–1.3, `reduce_silence` | https://soniox.com/docs/tts/concepts/emotion-and-tone · https://soniox.com/docs/api-reference/tts/websocket-api |
| 스트리밍(텍스트 조각 → 오디오 조각) | **된다.** 한 스트림에 `{"stream_id", "text", "text_end": false}`를 여러 번 보내면 base64 `audio` 조각이 돌아온다. "can start generating speech from the first few words, before the full sentence is available" | https://soniox.com/docs/api-reference/tts/websocket-api §Text streaming · https://soniox.com/docs/tts/get-started |
| 출력 포맷 | pcm_s16le/f32le(8k–48k, 기본 24k), wav, flac, mp3, opus, aac, mulaw/alaw | https://soniox.com/docs/tts/concepts/audio-formats |
| 지연 | **TTS 첫 오디오까지의 시간(TTFA) 수치는 문서에 없다.** 문서는 "ultra-low latency"라는 표현만 쓴다. 공식 STS 데모 README: "첫 오디오 약 0.5–1.5초, 대부분이 TTS 첫 바이트 시간, 미리 연결(pre-warm)로 중앙값 약 400ms 단축, 백엔드 오버헤드 5ms 미만" | 〔공식 예제〕 https://github.com/soniox/soniox_examples/tree/master/apps/soniox-speech-to-speech-translation-demo (README §A note on latency) |
| 실시간 번역을 TTS로 바로 보내기 | **연결 두 개.** STT WS(`wss://stt-rt.soniox.com/transcribe-websocket`)와 TTS WS(`wss://tts-rt.soniox.com/tts-websocket`)를 따로 열고, 앱이 `translation_status=="translation"` 토큰을 TTS 스트림에 `text`로 보낸다. `<end>`가 오면 `text_end: true`로 스트림을 닫는다. TTS 스트림은 발화당 하나 | https://soniox.com/docs/translation/sts-translation |
| TTS 스트림 제약 | 연결 하나에 스트림 최대 5개(고정). **스트림당 생성 오디오 최대 2분(고정).** ⚠ **스트림 안에서 몇 초 넘게 `text`가 오지 않으면 `request_timeout`으로 종료**(keepalive로는 이 타이머가 리셋되지 않음). 스트림이 없을 때는 40초 idle 한도가 있어 20–30초마다 keepalive를 보내야 한다 | https://soniox.com/docs/tts/rt/limits-and-quotas · https://soniox.com/docs/api-reference/tts/websocket-api §Connection timeouts |
| 양방향일 때 | 방향별로 TTS 스트림을 따로 두고, 번역 토큰의 `language`를 보고 어느 쪽에 보낼지 고르라고 안내한다. TTS 스트림의 `language`는 스트림 설정값(필수)이다 | https://soniox.com/docs/translation/sts-translation §Things to consider |

---

## B. 붙이는 법 (질문 6~9)

### B-6. 실시간 API

**STT(+번역)** 〔공식 문서〕 https://soniox.com/docs/api-reference/stt/websocket-api
- 엔드포인트: `wss://stt-rt.soniox.com/transcribe-websocket` (리전별 도메인: `stt-rt.eu.` / `.jp.` / `.in.`)
- 인증: 서버는 `Authorization: Bearer <key>` 헤더, 브라우저는 `new WebSocket(url, ["soniox-api-key", <임시키>])`. 시작 메시지의 `api_key` 필드는 **deprecated이고, 2027-01-15부터 거부된다.** 〔공식 문서〕 https://soniox.com/docs/guides/websocket-authentication
- 흐름: 연결 → JSON 설정 메시지 1회 → 오디오를 **바이너리 프레임**으로 계속 전송 → 종료할 때 **빈 텍스트 프레임 `""`**을 보냄 → `finished: true` 응답 뒤 서버가 연결을 닫음
- 오디오 포맷: `"audio_format": "auto"`이면 aac, aiff, amr, asf, flac, mp3, ogg, wav, **webm**을 헤더로 자동 판별한다(브라우저 MediaRecorder 출력을 그대로 넣을 수 있음). raw를 쓰면 `pcm_s16le` 등과 `sample_rate`, `num_channels`가 필수다. 〔공식 문서〕 https://soniox.com/docs/stt/rt/real-time-transcription §Audio formats
- 설정 메시지 최소 예시(공식 STS 가이드 원문):

```json
{
  "model": "stt-rt-v5",
  "audio_format": "auto",
  "enable_endpoint_detection": true,
  "max_endpoint_delay_ms": 500,
  "translation": {
    "type": "one_way",
    "target_language": "es"
  }
}
```

- 양방향: `{"type": "two_way", "language_a": "en", "language_b": "es"}` (같은 페이지)
- 응답 형식(원문):

```json
{
  "tokens": [
    { "text": "Hello", "start_ms": 600, "end_ms": 760, "confidence": 0.97, "is_final": true, "speaker": "1" }
  ],
  "final_audio_proc_ms": 760,
  "total_audio_proc_ms": 880
}
```

  번역 토큰 예: `{ "text": "Gu", "translation_status": "translation", "language": "de", "source_language": "en" }`. 오류는 `error_code` / `error_type` / `error_message`가 담긴 JSON이 온 뒤 연결이 닫힌다.
- 연결 시간 제한: 설정을 보내기 전이나 쉬는 동안 **40초 안에** keepalive를 보내야 한다. 그렇지 않으면 1001로 닫힌다.

**TTS** 〔공식 문서〕 https://soniox.com/docs/api-reference/tts/websocket-api
- 엔드포인트: `wss://tts-rt.soniox.com/tts-websocket`
- 스트림 시작(원문):

```json
{ "model": "tts-rt-v2", "language": "en", "voice": "Adrian", "audio_format": "wav", "sample_rate": 24000, "stream_id": "stream-001" }
```

- 텍스트: `{ "text": "Hello there, this is chunk one.", "text_end": false, "stream_id": "stream-001" }` → 마지막에 `"text_end": true`
- 응답: `{ "audio": "<base64-audio-bytes>", "audio_end": true, "stream_id": "stream-001" }` → `{ "terminated": true, "stream_id": "stream-001" }`. 취소: `{ "stream_id": "...", "cancel": true }`

**두 연결을 잇는 핵심 로직** — 공식 데모 `main.py`에서 그대로 옮김(〔공식 예제〕 L195–200):

```python
for token in data.get("tokens", []):
    text = token.get("text")
    if text == "<end>":
        await tts_queue.put(("end", None))          # → TTS 스트림 text_end: true
    elif token.get("translation_status") == "translation":
        await tts_queue.put(("text", text))         # → 열린(없으면 새) TTS 스트림에 text
```

### B-7. 브라우저 마이크에서 바로 붙일 수 있나

- **된다(direct stream).** 공식 가이드에 브라우저가 Soniox WS에 직접 붙는 구조가 있고, 지연이 가장 낮다고 안내한다. 〔공식 문서〕 https://soniox.com/docs/guides/direct-stream
- **임시 키**: 서버가 `POST https://api.soniox.com/v1/auth/temporary-api-key`를 장기 키로 호출해서 발급하고 클라이언트에 넘긴다. 〔공식 문서〕 https://soniox.com/docs/guides/temporary-api-keys
  - `usage_type`(필수): `transcribe_websocket`(STT) 또는 `tts_rt`(TTS). **키 하나는 서비스 하나에만 쓸 수 있다.** STS면 키 두 개를 발급해야 한다
  - `expires_in_seconds`(필수, 1–3600. 새 스트림을 열 수 있는 시간이고, 이미 열린 스트림은 끊지 않는다) · `single_use` · `max_session_duration_seconds` · `client_reference_id`
  - 키는 `snx_temp_`로 시작한다. 발급하는 장기 키에는 "Temporary API keys" 권한이 있어야 한다
  - 발급 예시(Python, 원문):

```python
response = requests.post(
    "https://api.soniox.com/v1/auth/temporary-api-key",
    headers={"Authorization": f"Bearer {SONIOX_API_KEY}", "Content-Type": "application/json"},
    json={"usage_type": "transcribe_websocket", "expires_in_seconds": 60},
)
```

- **공식 Web/JS SDK**: `@soniox/client`(Web: 마이크 캡처, STT·번역, 실시간 TTS), `@soniox/react`(`useRecording`, `useTts` 훅). 〔공식 문서〕 https://soniox.com/docs/sdk/web-SDK · https://soniox.com/docs/sdk/react-SDK
  - React `useRecording`은 `translation`을 넘기면 토큰을 자동으로 묶는다: one_way는 `original`/`translation`, two_way는 언어 코드별. 〔공식 문서〕 https://soniox.com/docs/sdk/react-SDK/stt/realtime-transcription §Handling translation
  - Web TTS: `client.realtime.tts({voice, audio_format})` → `stream.sendText(chunk)`를 여러 번 → `for await (chunk of stream)` 또는 `MediaSource`로 받으면서 재생. 〔공식 문서〕 https://soniox.com/docs/sdk/web-SDK/tts/realtime-speech-generation
- **back이 중계하는 방식(proxy stream)**: 공식 가이드가 있다. 키가 브라우저로 가지 않지만, 사용자당 서버 WS 1개와 Soniox WS가 동시 연결 한도에 잡힌다. 〔공식 문서〕 https://soniox.com/docs/guides/proxy-stream
- 정리: 공식 문서로는 **둘 다 가능하다.** 백엔드가 반드시 중계해야 하는 것은 아니다. 어느 쪽으로 할지는 §정할 것 Q-1.

### B-8. 공식 SDK·예제

| 무엇 | 링크 | 비고 |
|---|---|---|
| Python SDK `pip install soniox` | https://github.com/soniox/soniox-python · https://soniox.com/docs/sdk/python-SDK | 실시간 STT, 실시간 TTS, async, 임시 키 `client.auth.create_temporary_api_key` |
| Node / Web / React SDK (모노레포) | https://github.com/soniox/soniox-js | `@soniox/node`, `@soniox/client`, `@soniox/react` |
| **STS 데모(FastAPI + vanilla JS, proxy, SDK 없이 프로토콜 직접)** | https://github.com/soniox/soniox_examples/tree/master/apps/soniox-speech-to-speech-translation-demo | 우리 스택(FastAPI·uv)과 같다. TTS pre-warm, 발화당 TTS 스트림, keepalive 20초, 텍스트만 모드 토글 |
| **Next.js 예제(`@soniox/react`, 임시 키 API 라우트)** | https://github.com/soniox/soniox-js/tree/master/examples/nextjs | **STT만 있다**("real-time speech-to-text in a Next.js application"). 번역·TTS는 없다 |
| Soniox Live 데모(React + Python 서버, direct, 번역 자막) | https://github.com/soniox/soniox_examples/tree/master/apps/soniox-live-demo | 임시 키 서버 + React 직결. TTS 없음 |
| 번역 CLI 예제(one_way/two_way) | https://github.com/soniox/soniox_examples (speech_to_text/) | `--translation two_way` |
| Voice Agent 데모(STT + LLM + TTS) | https://github.com/soniox/soniox_examples/tree/master/apps/soniox-voice-bot-demo | 참고용 |

### B-9. 지연 수치

| 수치 | 무엇 | 출처 |
|---|---|---|
| "sub-200ms streaming latency" | STT 스트리밍(플랫폼 개요의 한 줄. 측정 조건 없음) | 〔공식〕 https://soniox.com/llms.txt |
| **0.5–1.5초** | STS 데모에서 말을 시작한 뒤 첫 번역 음성이 나오기까지. 대부분 TTS 첫 바이트 시간 | 〔공식 예제〕 STS 데모 README |
| 약 400ms | TTS pre-warm으로 줄어드는 중앙값 | 같은 곳 |
| 5ms 미만 | 데모 백엔드 파이프라인 자체 오버헤드 | 같은 곳 |
| 500–3000ms(기본 2000) | 발화 끝 → `<end>` 최대 지연(`max_endpoint_delay_ms`) | https://soniox.com/docs/api-reference/stt/websocket-api |
| 전체 지연 ≈ STT 번역 지연 + TTS 첫 오디오 시간 | 정성적인 공식 | https://soniox.com/docs/translation/sts-translation §Things to consider |
| 번역 토큰 지연, TTS TTFA 단독 수치 | **문서에 없음** | — |

- 연결 시간이 1초를 넘으면 네트워크나 리전 문제일 수 있으니, 연결 전에 오디오를 버퍼링하라고 권장한다. 〔공식 문서〕 https://soniox.com/docs/faq. 한국 리전은 아직 없다(가까운 곳은 JP).

---

## C. TTS 후보 비교표 (질문 10~11)

### C-10. 스트리밍 TTS 대안

**해당 없음.** 브리프 조건은 "A-5에서 한국어, 대상 언어, 스트리밍 중 빠지는 게 있을 때만"이다.
Soniox TTS는 셋 다 충족한다. 한국어와 en·ja·zh·vi·th가 지원 목록에 있고, 텍스트 조각을 넣으면 오디오 조각이 나오는 WS를 제공한다(§A-5).
- 남는 위험은 **한국어 음성 품질**이다. 문서에 품질 수치는 없다. Soniox의 TTS 비교 페이지(https://soniox.com/compare-tts, 〔공식 마케팅〕)는 공급사별로 같은 문장을 실시간 합성해서 들어 보는 도구이고, 지연은 비교하지 않는다고 명시한다. 귀로 확인하는 일은 §정할 것 Q-4로 넘긴다.

### C-11. LLM 번역이 필요한가

- 문서상 번역은 STT에 내장되어 있다("Speech translation is built into the Soniox real-time API"). 요금 FAQ도 번역이 같은 실시간 호출에 포함된다고 한다. 〔공식 문서〕 https://soniox.com/docs/translation/get-started · 〔공식 마케팅〕 https://soniox.com/pricing
- 용어나 고유명사를 정확히 옮기는 문제는 `context.translation_terms`(source→target 쌍)로 다룬다고 문서에 나온다. 도메인 설명은 `context.general`/`text`/`terms`로 준다(컨텍스트 최대 8000 토큰). 〔공식 문서〕 https://soniox.com/docs/translation/stt-translation §Context and translation terms · https://soniox.com/docs/stt/concepts/context
- **LLM 번역이 필요한 경우는 문서에 없다.** 문서로 확인되는 제약은 두 가지다.
  - (a) 지원 언어 60여 개 밖의 언어는 번역 대상이 아니다.
  - (b) 번역 결과에 존댓말, 문체, 요약 같은 지시를 줄 파라미터가 API 참조에 없다(`translation` 블록은 `type`/`target_language`/`language_a`/`language_b`만 있음).
  - 이런 요구가 고객 데모에 있을 때만 LLM 단계를 검토할 대상이 된다(§정할 것 Q-6).

---

## D. 비용·한도 (질문 12)

### 요금 〔공식 마케팅〕 https://soniox.com/pricing (페이지 표기 "Updated June 2026")

| 항목 | 단가(토큰) | 시간 환산(페이지 표기) |
|---|---|---|
| 실시간 STT 입력 오디오 | $2.00 / 1M 토큰 | **약 $0.12/시간** (1시간 ≈ 입력 오디오 30,000 토큰) |
| 실시간 STT 입력 텍스트(컨텍스트) | $4.00 / 1M | — |
| 실시간 STT 출력 텍스트(전사 **+ 번역**) | $4.00 / 1M | 1시간 발화 ≈ 출력 15,000 토큰 |
| Async STT | 오디오 $1.50 · 텍스트 $3.50 / 1M | 약 $0.10/시간 |
| **TTS** 입력 텍스트 | $4.00 / 1M | — |
| **TTS** 출력 오디오 | $21.50 / 1M | **약 $0.70/생성 시간** (1시간 ≈ 30,000 출력 오디오 토큰) |

- 번역 과금: 가격 FAQ는 "Is translation included, or billed separately? **Included** … at no extra cost"라고 한다. 반면 번역 제품 페이지(https://soniox.com/speech-translation)는 "**$0.18/hour real-time**"이라고 표기한다. 토큰 과금이라 번역 출력 텍스트 토큰만큼 출력 비용이 늘어나서 생긴 차이로 보이지만, **두 공식 페이지의 표기가 다르고 정확한 산식은 문서에 없다.** Console 사용량 로그(https://soniox.com/docs/guides/usage-logs)로 실측해야 한다.
- 화자 분리와 언어 판별은 추가 요금 없음(같은 FAQ).
- **구독 플랜별 차이: 문서에 없음.** 가격 페이지는 종량제(pay-as-you-go)와 "custom package" 문의만 안내한다. Business/Enterprise라는 이름은 법무 문서(MSA·DPA) 제공 대상으로만 나온다(https://soniox.com/docs/faq). 사용자의 "구독"이 어떤 계약인지는 Console에서 확인해야 한다(§정할 것 Q-8).

### 한도 (기본값)

| API | 한도 | 값 | 출처 |
|---|---|---|---|
| 실시간 STT | 분당 요청 | 100 | https://soniox.com/docs/stt/rt/limits-and-quotas |
| 실시간 STT | **동시 요청(활성 스트림)** | **10** | 같은 곳 |
| 실시간 STT | 세션 길이 | 300분(고정) | 같은 곳 |
| 실시간 TTS | 분당 요청 | 100 | https://soniox.com/docs/tts/rt/limits-and-quotas |
| 실시간 TTS | **동시 스트림(모든 연결 합계, REST 포함)** | **3** | 같은 곳 · https://soniox.com/docs/guides/concurrency-limits |
| 실시간 TTS | 연결당 스트림 | 5(고정) | 같은 곳 |
| 실시간 TTS | 스트림당 생성 오디오 | 2분(고정) | 같은 곳 |
| 공통 | 동시 연결(idle 포함) | 동시 요청·스트림 한도의 배수 | 같은 곳 |

- 한도는 Console(https://console.soniox.com/org/limits)에서 올려 달라고 요청할 수 있고, 1–3영업일 걸린다(고정 항목 제외). 〔공식 문서〕 https://soniox.com/docs/faq
- 프로토타입에 미치는 영향: TTS 동시 스트림 기본값이 **3**이다. 양방향에서 방향별 스트림 2개에 pre-warm까지 하면 데모 세션 하나가 한도를 거의 다 쓴다. 동시 시연 인원에 따라 한도 증설이 필요하다(§정할 것 Q-5).

---

## 프로토타입 구성 후보 — 경로별 한 줄 흐름

```text
P2 (proxy, 공식 STS 데모 구조)
  브라우저 mic(MediaRecorder webm) ─WS→ FastAPI ─WS→ Soniox STT(+translation) ─tokens→ FastAPI ─WS(text)→ Soniox TTS ─audio(base64)→ FastAPI ─PCM/JSON→ 브라우저(Web Audio 재생 + 원문/번역 표시)

P3 (direct, SDK)
  브라우저 ─POST→ FastAPI /temp-key (×2: transcribe_websocket, tts_rt) ─키→ 브라우저
  브라우저 mic ─@soniox/react useRecording(translation)→ Soniox STT ─번역 토큰→ (브라우저 로직) ─@soniox/client realtime.tts→ Soniox TTS ─audio→ 브라우저 재생

P2' (proxy + 텍스트만 — 데모 토글)
  브라우저 mic ─WS→ FastAPI ─WS→ Soniox STT(+translation) ─tokens→ 브라우저 (TTS 생략; 공식 데모의 "text-only translation mode")

P4 (Soniox STT+번역 → 타사 TTS) — §C-10 「해당 없음」이라 그리지 않음
```

번역 모드는 경로와 따로 고른다.
- one_way: 한국어 화자 한 명 → 대상 언어 하나
- two_way: `language_a=ko`, `language_b=<상대 언어>`. 두 사람이 마이크 하나를 쓰고, 번역 토큰의 `language`로 TTS 스트림의 언어를 고른다

---

## 정할 것 — 코디·사용자가 결정할 항목 (여기서 결정하지 않음)

| # | 항목 | 고를 수 있는 것 | 근거 위치 |
|---|---|---|---|
| Q-1 | 연결 구조 | P2 proxy(FastAPI 중계, 공식 STS 데모 구조) / P3 direct(브라우저 SDK + 임시 키 2종) | §결론 · §B-7 |
| Q-2 | 번역 모드 | one_way(ko→X) / two_way(ko↔X 대화) | §A-2 |
| Q-3 | 데모 언어 쌍 | ko↔en / ja / zh / vi / th … (모두 지원 목록에 있음) | §A-3 |
| Q-4 | TTS 음색과 한국어 품질 확인 방법 | Console에서 들어 보고 음색을 고를지 / 대안 TTS를 들어 볼지(현재 「해당 없음」) | §A-5 · §C-10 |
| Q-5 | 동시 시연 규모와 한도 증설 요청 여부 | TTS 동시 스트림 기본 3, STT 기본 10 | §D 한도 |
| Q-6 | LLM 번역 단계가 필요한 요구(존댓말, 문체, 지원 밖 언어)가 고객 데모에 있나 | 없음 → Soniox 내장 번역만 / 있음 → P5 검토 | §C-11 |
| Q-7 | 첫 실물 호출에서 확인할 것 | 번역 토큰이 non-final로도 오는지, 실제 첫 음성까지의 시간, 번역 과금 산식(사용량 로그) | §A-2 · §B-9 · §D |
| Q-8 | 사용자 Soniox 계약 형태(구독/종량제)와 한도 | Console에서 확인 | §D |
| Q-9 | 발화 끝 감지 튜닝값 | `max_endpoint_delay_ms`(데모 500) · `endpoint_sensitivity` · 화자 분리를 함께 쓸지(같이 쓰면 정확도가 떨어짐) | §A-4 |
| Q-10 | 리전 | 기본 US / JP(가장 가까운 리전, 리전 프로젝트는 support 문의 필요). Korea는 Coming soon | §A-3 · §B-9 |

---

## 출처 목록

**공식 문서** (모두 2026-10-10 수집, 본문은 각 URL에 `.mdx`를 붙여 읽음)
- https://soniox.com/llms.txt · https://soniox.com/docs/llms.txt · https://soniox.com/docs/llms-full.txt
- https://soniox.com/docs/index
- https://soniox.com/docs/stt/models · https://soniox.com/docs/tts/models
- https://soniox.com/docs/translation/get-started
- https://soniox.com/docs/translation/stt-translation
- https://soniox.com/docs/translation/stt-translation/rt-translation
- https://soniox.com/docs/translation/sts-translation
- https://soniox.com/docs/translation/supported-languages
- https://soniox.com/docs/stt/concepts/supported-languages
- https://soniox.com/docs/stt/concepts/language-identification
- https://soniox.com/docs/stt/concepts/speaker-diarization
- https://soniox.com/docs/stt/rt/real-time-transcription
- https://soniox.com/docs/stt/rt/endpoint-detection
- https://soniox.com/docs/stt/rt/limits-and-quotas
- https://soniox.com/docs/tts/get-started
- https://soniox.com/docs/tts/concepts/supported-languages · /voices · /audio-formats
- https://soniox.com/docs/tts/rt/limits-and-quotas
- https://soniox.com/docs/api-reference/stt/websocket-api
- https://soniox.com/docs/api-reference/tts/websocket-api
- https://soniox.com/docs/guides/websocket-authentication
- https://soniox.com/docs/guides/temporary-api-keys
- https://soniox.com/docs/guides/direct-stream · https://soniox.com/docs/guides/proxy-stream
- https://soniox.com/docs/guides/concurrency-limits
- https://soniox.com/docs/sdk · /sdk/python-SDK · /sdk/web-SDK · /sdk/web-SDK/tts/realtime-speech-generation · /sdk/react-SDK · /sdk/react-SDK/stt/realtime-transcription
- https://soniox.com/docs/demo-apps/soniox-speech-to-speech-translation · https://soniox.com/docs/demo-apps/soniox-live
- https://soniox.com/docs/data-residency · https://soniox.com/docs/faq

**공식 예제 (GitHub)**
- https://github.com/soniox/soniox_examples/tree/master/apps/soniox-speech-to-speech-translation-demo (README, main.py)
- https://github.com/soniox/soniox_examples/tree/master/apps/soniox-live-demo
- https://github.com/soniox/soniox-js/tree/master/examples/nextjs (README)
- https://github.com/soniox/soniox-js · https://github.com/soniox/soniox-python

**공식 마케팅 페이지** (문서보다 약한 출처)
- https://soniox.com/pricing ("Updated June 2026")
- https://soniox.com/speech-translation ("$0.18/hour real-time")
- https://soniox.com/text-to-speech (리전 Korea "Coming soon")
- https://soniox.com/compare-tts
- https://soniox.com/benchmarks (한국어 항목 없음 확인)

**비공식 출처**: 사용하지 않음.
