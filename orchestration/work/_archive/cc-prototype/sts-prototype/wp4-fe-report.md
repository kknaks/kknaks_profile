# WORK-001 WP4 결과 보고 (frontend) — 통역 모달

## 상태: done

환자 상세 [통역] → 통역 모달을 만들었다(SPEC §7 · `interpret-ws-contract.md` · 시안 `Ceramique 직원 - 의사`/`- 통역 모달 상태`). 실제 Soniox · 실제 마이크 통합은 WP5.
커밋 · push · PR 없음. `cc/front/` 만 고쳤다. 목업 서버 · 캡처 스크립트는 스크래치패드에만 두었고 지웠다(코드 레포에 남긴 것 없음).

## 수행 — 파일

| 파일 | 변경 |
|---|---|
| `lib/interpret.ts` (신규) | `InterpretSession` — `getUserMedia`(echoCancellation · noiseSuppression · autoGainControl) → AudioWorklet(Blob 모듈)이 컨텍스트 샘플레이트 → **16kHz mono s16le** 로 선형 보간 · 40ms(640샘플) 조각 → WS 바이너리. `ready` → 듣는 중, `caption` → 콜백, `audio_start`(sampleRate · format) → 바이너리 PCM 을 `AudioBuffer` 로 바꿔 **앞 조각 끝에 이어 예약 재생**(조각 경계의 홀수 바이트 이월), `audio_end`. `format` 이 pcm_s16le 가 아니면 조각을 모았다가 `audio_end` 에 `decodeAudioData`. `error` · WS 끊김 → 오류. [멈춤]/[다시] = `pause`/`resume` + 마이크 트랙 `enabled` 끄기/켜기(멈춤 동안 전송 0). [닫기] = `stop` → WS close · 트랙 stop · AudioContext close |
| `lib/api.ts` | `openInterpretSocket()` — `NEXT_PUBLIC_API_BASE_URL` 의 http→ws + `/api/interpret`, binaryType arraybuffer (back 연결은 계속 이 모듈만) |
| `components/staff/InterpretModal.tsx` (신규) | 시안 마크업 · 클래스 · 문구 그대로. 폰 = 아래 시트(`calc(100% - 24px)`, 위 모서리만 둥글게) · 폭 ≥760 = 가운데 창(560px · `min(720px, 100vh-80px)`). 언어 칩 8개(국적 기본값에 「· 자동」), 바꾸면 세션을 새로 연다. 자막은 `id` 로 갱신(언어 바꿔 다시 붙어도 안 겹치게 세션 번호를 붙임), `them` 왼쪽 · `me` 오른쪽, 원문 크게 + 번역 작게, 미확정은 흐리게 + 「…」 + 번역 비면 「번역 중…」. 새 말풍선·갱신마다 아래로 스크롤 |
| `components/staff/common.ts` | §7.2 국적 → 언어(TW·CN·HK zh · JP ja · US·PH·IN en · TH th · FR fr · 그 밖 en) · `traditional` = zh 이면서 TW·HK · 언어 8개 |
| `components/staff/PatientView.tsx` · `StaffShell.tsx` | [통역] → 모달 열기(KR 은 WP3 그대로 숨김). 폭 정보 전달 |
| `app/globals.css` | 시안의 `ip-pulse` · `ip-spin` 애니메이션 추가. `.cc-btn` 리셋을 `:where(.cc-btn)`(우선순위 0)으로 — 아래 이슈 2 |
| `README.md` | 통역 구조 · localhost 로 열어야 마이크가 열림 |

## 검증 — 명령과 결과

| 명령 | 결과 |
|---|---|
| `npx tsc --noEmit` | 통과 |
| `npm run lint` | 통과(오류 0 · 경고 0) |
| `npm run build` | 통과 |
| 기능 폴더 밖 import | 없음. `fetch` · `WebSocket` · `EventSource` 생성은 `lib/api.ts` 만 |
| 목업 WS(스크래치패드, 임시 포트 18611) + `next dev`(임시 13611) + headless 크롬(가짜 마이크) | 아래 표. 끝나고 두 프로세스만 종료(3600 · 8600 무관) |

| 확인 항목 | 결과 |
|---|---|
| 시작 프레임 | `{"type":"start","lang":"zh","scheduleId":"s2","traditional":true}` (TW 환자) · 프랑스어로 바꾸면 `lang:"fr", traditional:false` 로 새 연결 |
| 상태 전환 | 열기 직후 「연결 중」(스피너) → `ready` 뒤 「듣는 중」(파란 원 · 펄스) → [멈춤] 「멈춤」 → [다시] 「듣는 중」 → 서버 `error` 「오류」(빨간 박스 + 다시 시도) · 마이크 거부(권한 거절) 「오류」 + WS 안 엶 |
| PCM 송신 | 듣는 동안 3.04초에 97,280 바이트 = **32,000 B/s = 16kHz × 2바이트** · 멈춤 동안 0 바이트 · 다시 듣기 0.8초 25,600 바이트 |
| 자막 | `u1` 미확정(흐림 · 「번역 중…」) → 같은 말풍선이 확정으로 바뀜 · `me` 는 오른쪽 파란 말풍선 |
| 음성 재생 | 0.9초 PCM 을 홀수 경계(7001 · 13000 바이트)로 3조각 → 예약 시각 2.434 → 2.580 → 2.851초, 길이 0.146 + 0.271 + 0.483 = 0.9초 — **빈틈 · 겹침 없이 이어짐**, 24kHz 그대로 |
| [닫기] | `stop` 받은 뒤 WS close · 모달 사라짐 |
| 폰 폭(390) | 아래 시트로 뜸 |
| 콘솔 오류 | 0 |
| 실제 Soniox · 실제 마이크 · 스피커 소리 | **pending** — WP5(노트북 크롬 localhost) |

## 계약 대조

| 계약 | 결과 |
|---|---|
| front → back: `start` 1회 · PCM s16le 16k mono 20~100ms(→ 40ms) · `pause`/`resume` · `stop` 후 close | 같음 |
| back → front: `ready` · `caption`(id 갱신 · final) · `audio_start`(sampleRate, format 없으면 pcm_s16le) · 바이너리 · `audio_end` · `error` | 같음 |
| 마이크 거부는 front 가 「오류」(서버 안 감) | 같음 |
| §7.1 모달 열기 = 연결 · 듣기 / [멈춤] = 마이크만 / [닫기] = WS 종료 · 상태 4종 | 같음 |
| §7.2 언어 · 번체(TW · HK) · KR 숨김 · 언어 바꾸면 WS 다시 | 같음 |

## 이슈 · 코디가 확인할 것

1. **오류 문구** — 시안의 오류 상태는 마이크 권한 거부 하나뿐이라, 서버 `error` · WS 끊김일 때는 제목을 「통역 서버에 연결하지 못했어요」, 본문은 back 의 `message`(끊김이면 「통역 서버와 연결이 끊겼어요.」), 아래 안내를 「다시 시도를 눌러 주세요」로 썼다(시안에 없는 문구). 마이크 거부는 시안 문구 그대로.
2. **WP3 버그 함께 고침** — `.cc-btn{background:none}` 이 Tailwind 배경 클래스보다 뒤에 와서 「듣는 중」 마이크 버튼의 파란 채움이 사라졌다(로그인 카드 테두리 색 문제도 같은 원인). 리셋을 `:where(.cc-btn)` 로 바꿔 유틸리티 클래스가 이기게 했다. 데스크 · 로그인 화면 모양은 그대로다(의도대로 색이 들어갈 뿐).
3. **[멈춤]** 은 트랙을 stop 하지 않고 `enabled=false` 로 끈다 — 다시 들을 때 권한을 다시 묻지 않게. 브라우저 주소창의 마이크 표시는 [닫기] 전까지 남는다.
4. 오류가 나면 그 세션은 정리하고, [다시 시도] 가 새 연결을 연다(자막은 남김). 이전 말풍선은 언어를 바꿔도 남는다.
5. 통역 중에 SSE 로 환자 상세가 다시 그려져도 모달은 유지된다. 다른 환자를 고르면(상세가 바뀌면) 모달이 닫히며 세션이 정리된다.
6. AudioContext 는 [통역] 클릭 뒤 비동기로 만들어서, 멈춰 있으면 `resume()` 한다 — 실제 크롬에서 첫 음성이 나오는지는 WP5 에서 귀로 확인.
