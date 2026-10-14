# 통역 WS 계약 — WP2(back) ↔ WP4(front) (코디 결정 2026-10-13, SPEC-001 §7 구체화)

엔드포인트: `ws://<back>/api/interpret` (CORS 와 같은 origin 허용 — `CC_FRONT_ORIGIN`)

## front → back

| 프레임 | 모양 | 언제 |
|---|---|---|
| 텍스트 | `{"type":"start","lang":"zh","scheduleId":"…","traditional":true}` | 연결 직후 한 번. `lang` = SPEC §7.2 언어 코드, `traditional` = 자막 번체 변환(TW·HK) |
| 바이너리 | PCM signed 16-bit little-endian · 16000 Hz · mono, 조각 20~100ms | 듣는 중 |
| 텍스트 | `{"type":"pause"}` / `{"type":"resume"}` | [멈춤]/[다시 듣기] — 마이크만, 연결 유지 |
| 텍스트 | `{"type":"stop"}` 후 close | [닫기] |

## back → front

| 프레임 | 모양 | 뜻 |
|---|---|---|
| 텍스트 | `{"type":"ready"}` | Soniox 연결 완료 → 「듣는 중」 |
| 텍스트 | `{"type":"caption","id":"u3","side":"me"\|"them","original":"…","translation":"…","final":false}` | 발화 단위 자막. 같은 `id` 가 갱신되다가 `final:true` 로 확정. `side` = 원문 언어 ko → `me`(오른쪽) |
| 텍스트 | `{"type":"audio_start","id":"u3","sampleRate":24000}` | 그 발화의 번역 음성 시작 |
| 바이너리 | PCM s16le mono, `sampleRate` 는 직전 `audio_start` 값 | 음성 조각 — 받는 대로 이어서 재생 |
| 텍스트 | `{"type":"audio_end","id":"u3"}` | 그 발화 음성 끝 |
| 텍스트 | `{"type":"error","code":"soniox_unavailable"\|"no_api_key"\|"bad_request","message":"…"}` | 오류 → 모달 「오류」 상태 |

- 음성 출력 형식(PCM 24kHz)이 Soniox TTS 에서 안 되면 back 이 되는 형식으로 바꾸고 `audio_start.sampleRate`(+ 필요하면 `"format"`)로 알린다 — front 는 `format` 이 없으면 pcm_s16le 로 본다
- 마이크 권한 거부는 front 가 「오류」 상태로(서버 안 감)
