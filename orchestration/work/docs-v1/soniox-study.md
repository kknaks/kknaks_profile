# Soniox 실시간 STT 조사 — 회의록 화자 스크립트 적용

> 2026-09-03 조사. 출처: soniox.com/llms.txt · docs/llms.txt 및 하위 문서.
> 용도: 회의록(BASE/DEC-003) 실시간 받아쓰기·화자 분리 정책의 기술 근거.

## 핵심 사실

| 항목 | 내용 |
|---|---|
| 프로토콜 | WebSocket `wss://stt-rt.soniox.com/transcribe-websocket` — 최초 JSON config → 오디오 바이트 스트림 → 빈 문자열로 종료 |
| 모델 | `stt-rt-v5` (실시간). 한국어 지원(`language_hints: ["ko"]`) |
| 토큰 모델 | `is_final: false` = 잠정(계속 바뀜, 응답마다 리셋 렌더) / `is_final: true` = 확정(불변, append) |
| 화자 분리 | `enable_speaker_diarization: true` → 토큰마다 `speaker: "1"/"2"…`. **세션당 최대 15명** |
| 클라이언트 | Web SDK `@soniox/client` — mic 캡처+스트림+콜백(result/error, `stop()` 은 최종 결과 대기) |
| 인증(클라 직결) | **Direct stream**: 브라우저 → Soniox 직결. 백엔드는 **temporary API key 발급만** (`POST /v1/auth/temporary-api-key`, `usage_type: transcribe_websocket`, `expires_in_seconds` 짧게 60s, single-use 옵션, `client_reference_id`). long-lived key는 서버에만 |
| 한도 | 스트림 최대 **300분**(연장 불가 — 새 세션), 동시 접속 10, 요청 100/min. temp key 발급에도 rate limit |

## 유의사항 (사용자 요청 확인분)

1. **실시간 화자 분리는 async 대비 정확도가 낮다.** 저지연 제약 때문에 화자 오귀속·일시적 화자 전환이 생기고, 오디오가 쌓이면 안정화된다. 최고 정확도는 async(전체 오디오 컨텍스트).
2. **endpoint detection·manual finalization 이 화자 분리 정확도를 깎는다** — 조기 파이널라이즈 강제 때문. 회의록은 음성 명령형 앱이 아니라 응답 지연이 중요치 않으므로 **끄는 게 맞다**.
3. 화자 라벨은 익명(`1`, `2`…) — **라벨→이름 매핑은 우리 몫**. 목소리 등록 기반 화자 식별(speaker identification)은 우리 쪽 목소리 기능이 v1 목 UI 라 해당 없음.
4. 300분 초과 회의는 새 세션 — 세션 경계에서 화자 라벨 연속성 끊김.
5. 비슷한 목소리는 정확도 저하. 유사 음색 다수 회의에서 오귀속 증가.
6. **mic 캡처 경로 갈림** — WKWebView(Tauri macOS)에서 `getUserMedia` 동작은 Tauri 설정·OS 권한에 걸림. (a) 웹뷰 getUserMedia + Web SDK vs (b) Tauri(rust)가 캡처해 PCM 을 웹소켓으로 — DEC-002 Q-40 과 직결, spec 결정.

## 우리 적용 방향(제안 — 회의록 논의에서 확정)

- 아키텍처: FastAPI 는 temp key 발급 엔드포인트만, 프론트가 Soniox 직결(direct stream) — 지연 최소·백엔드 단순.
- 스크립트 렌더: 확정 토큰 append + 잠정 토큰 회색 갱신. 화자 전환마다 화자 블록 분리.
- 화자 라벨: 실시간엔 「화자 1/2」로 두고, 회의 중/후 사용자가 이름 지정(매핑 테이블). 
- 2-pass 여부(정책 결정 필요): 회의 종료 후 async 재전사로 화자·전사 정정할지, 실시간 결과를 정본으로 둘지.
- endpoint detection 미사용.
