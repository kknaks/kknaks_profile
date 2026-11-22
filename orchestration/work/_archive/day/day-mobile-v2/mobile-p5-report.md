# day-mobile-v2 P5 결과 보고 — 앱 통역 클라이언트를 서버 P1(통키 `56e43a0`)에 맞춤

## 상태: done (커밋 · push · PR 없음 — 워크트리에 변경만 · 실기기 마이크 · 메아리 확인은 pending)

base = `a7868dc6`(서버 P1) 위. `backend/` 는 읽기만(같은 워크트리 backend 워커 P2 변경은 내 것 아님).

## 수행 — 파일

| 파일 | 변경 |
|---|---|
| `app/lib/interpret/interpret_client.dart` | 반이중 걷음 · `audio_stop` · PCM 버림 · `playback_stopped` · `audio_end` 버림 갈래 · `Caption.erases` |
| `app/lib/state/interpret_controller.dart` | 빈 final caption = 그 key 말풍선 지움(모르는 key 는 그리지 않음) — 스펙이 이 파일 `:162-169` 를 P5 범위로 짚음. **allowed_paths 의 `app/lib/interpret/` 밖(`app/lib/state/`)** — 통역 컨트롤러라 같은 범위로 보고 3줄만 고침 · 코디 확인 바람 |
| `app/test/interpret/interpret_playback_test.dart`(새) | 클라이언트 상태 · 프레임 처리 10건(fake_async) |
| `app/test/interpret/interpret_mock_ws_test.dart`(새) | 목 WS 실물 1건 — 실제 `IoTransport` 핸드셰이크로 127.0.0.1 임시 포트 가짜 서버 |
| `app/test/interpret/interpret_test.dart` | 기존 「재생 중엔 마이크 안 보냄」 기대를 「보냄」으로(반이중 걷음) |
| `app/test/support/fixtures.dart` | `FakeSink.flushed` 셈 칸 |

화면 · 글자 변경 없음(`app/lib/ui/` 무수정).

## 동작 — 통키 `front/lib/interpret.ts` · `output.ts` 와 대조

| 항목 | 앱 구현 | 통키 근거 · 스펙 |
|---|---|---|
| 반이중 걷음 | `sendPcm` 조건에서 `speaking` 제거 — ready 뒤 · 멈춤 아님 · 연결됨이면 재생 중에도 보냄 | `canSendPcm` · §3 「앱(반이중 걷음)」 |
| 출력 구간(audio_start ~ 재생 끝 + 400ms) | `speaking` 그대로 둠 — 표시(`onPlayback`) · `playback_stopped` 판정에만 | `OutputWindow` · `interpret.ts:252` |
| `audio_stop` | id 를 보지 않고 `_stopPlayback()` · 서버로 보내는 것 없음 · 듣기 계속 | `interpret.ts` `case 'audio_stop'` · W-12 |
| PCM 버림 | 멈춤 · 닫기 · 오류 · `audio_stop` 모두 `_stopPlayback()` → `_discarding = true` · 다음 `audio_start` 까지 PCM 조각 · `audio_end` 버림(출력 구간 타이머 안 건드림) | `OutputController.clear/accept/audioEnd` · W-13 |
| `playback_stopped {id}` | [멈춤](`toggle` → pause)일 때만 · 출력 구간 안 · 마지막 `audio_start` id · `pause` 보다 먼저. 다시 듣기 · 닫기 · 언어 바꿈 · 다시 연결 · 오류는 안 보냄. 앱엔 재생 지우기 조작이 없어 [멈춤] 하나 | `stopPlaybackByUser` · OQ-A61 |
| 서버 `audio_end` 응답 | `playback_stopped` 뒤 오는 `audio_end` 는 버림 갈래에서 무시(이미 멈춤) · 평소 `audio_end` 는 기존대로 출력 구간 닫기 | `session.py:527` · 스펙 「서버 응답」 |
| 빈 final caption | `original` · `translation` 둘 다 빈 `final` = 그 id 말풍선 지움 → 「마지막 통역 · N문장」 셈에서도 빠짐 · 보인 적 없는 id 는 추가 안 함 | F-4 · `session.py:373-376 · :414-421` |
| 멈춤 중 새 발화 TTS | `audio_start` 가 버림을 풀어 재생(통키 · 프로토와 같음) | `interpret.ts` pause 주석 |
| 모르는 프레임 | 무시(관대한 읽기) | tolerant-reader |

## 검증

| 명령 | 결과 |
|---|---|
| `fvm flutter analyze` | No issues found |
| `fvm flutter test` | **+382 ~75 All tests passed**(~75 = 캡처 · 평소 skip) — P5 새 11건 포함(M1 뒤 372 → 382 · 기존 1건 기대 수정) |
| `fvm flutter build ios --no-codesign` | ✓ Built `Runner.app` (20.7MB) |
| 목 WS 실물(`interpret_mock_ws_test.dart`) | 통과 — ready → caption → audio_start + PCM 1초 재생 → 재생 중 마이크 송신 확인 → `audio_stop{id:null}` 멈춤 · 남은 PCM · audio_end 버림 · 응답 0 → 새 발화 재생 → [멈춤] = `playback_stopped{id:u2}` → `pause` 순서 → 서버 `audio_end` 무시 → 빈 final caption 지우기 → 닫기 `stop`(playback_stopped 추가 없음) |

실물 범위: 로컬 DAY 서버 · Soniox 는 쓰지 않음(목 WS) · 사용자 포트 · 프로세스 · 시뮬레이터 · 기기 무접촉. **iOS 시뮬레이터 · 실기기 마이크 실호출 · 폰 스피커 메아리(I-6) = pending(A-50 사용자 실기기)**.

## 계약 대조 — 스펙 §3 「통역 — 0.2.0」 · U-15
| 줄 | 결과 |
|---|---|
| 새 서버 → 앱 `audio_stop` · id 무시 | 같음 |
| 빈 final caption 지움 · 셈 제외 | 같음 |
| 새 앱 → 서버 `playback_stopped` · [멈춤]만 · 출력 구간 안 · pause 앞 · 닫기 · 언어 바꿈 · 다시 연결 안 보냄 | 같음 |
| `playback_stopped` 서버 응답 `audio_end` | 같음(받아 처리 · 이미 멈춤) |
| 앱 반이중 걷음 · 출력 구간 판정용 · 모든 멈춤 경로 PCM 버림 · `audio_stop` 응답 없음 | 같음 |
| 드로어 모양 · 글자 | 그대로 |

## 이슈 · 코디가 확인할 것
1. **드로어 안내 글자가 이제 사실과 다르다** — 재생 중 상태 줄 「번역 읽는 중」 아래 안내 **「번역 음성이 나오는 동안은 듣지 않아요」**(`app/lib/ui/interpret_widgets.dart:409` · 프로토 원문)는 반이중 걷음 뒤 틀린 말(이제 재생 중에도 듣는다). 브리프가 글자 변경 · 새 글자를 막아 **그대로 두었다.** 통키에 대응 글자 없음(통키는 「〈언어〉로 출력 중」 원 표시 방식 · `phrases.ts:15`). 결정 필요: 그 안내를 비울지 · 사용자가 새 글자를 정할지(스펙 U-15 「상태 글자는 프로토 그대로」와 충돌).
2. `app/lib/state/interpret_controller.dart` 수정은 allowed_paths(`app/lib/interpret/` · ui · test) 밖 — 스펙이 이 파일을 P5 범위로 짚어 고쳤다(빈 final caption 처리 3줄).
3. 메아리(I-6) — 앱은 OS 음성 처리 모드를 바꾸지 않았다(서버 TokenGate + agent text 에 맡김 · 스펙 「구현 확인」). 실기기에서 재생 소리가 자막으로 되울리면 그때 판단.
4. 워크트리의 `backend/**` 수정(auth · board 등)은 backend 워커 P2 — 내 것 아님. 커밋 때 나눌 것.
