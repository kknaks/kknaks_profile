# 코드 검수 — mobile P5 앱 통역 클라이언트 0.2.0 (커밋 `bb8412de`)

## 판정: **PASS**(FAIL 0 · WARN 1 · INFO 4)

대상 = `bb8412de` 하나. 읽기만 했다(수정 · 커밋 없음). 워크트리 `app/` 는 `bb8412de` 와 차이 없음(`git diff --quiet bb8412de -- app`).
대조 원천 = 서버 `a7868dc6`(`backend/day/services/interpret/session.py` · `speaker.py`) · 통키 `56e43a0` `front/lib/interpret.ts` · `output.ts` · 스펙 SPEC-003 §3 「통역 — 0.2.0」(:828) · U-15(:460) · OQ-A61.

## 1. 서버 프로토콜 · 통키 front 대조 — PASS

| 경로 | 앱 (`app/lib/interpret/interpret_client.dart`) | 서버 `a7868dc6` | 통키 front | 결과 |
|---|---|---|---|---|
| `audio_stop` | `:248-250` id 안 봄 · `_stopPlayback()` · 보내는 것 없음 | `speaker.py:190-191` barge_in 때 `{audio_stop, id: _last_start}` 뒤 `_cut=True` → 그 차례 PCM · audio_end 안 보냄 | `case 'audio_stop'` → `stopPlayback()` | 같음 |
| `playback_stopped` | `:313-319` [멈춤] · `speaking`(출력 구간) · `_lastAudioId != null` 일 때만 · `pause` 앞 | `session.py:419-429` id 가 str · 이 차례 `_turn_ids` 안 · `!_cut` 일 때만 멈춤 절차 | `pause()` → `stopPlaybackByUser()`(outputting && lastAudioId) → `pause` | 같음 · 앱은 id null 이면 안 보냄(통키는 `String(null)`="null") — 서버가 str 만 받고 audio_start id 는 늘 str 이라 차이 없음, 앱 쪽이 더 엄격 |
| 응답 `audio_end` | `:243-247` `_discarding` 이면 무시(출력 구간 타이머 안 건드림) | `speaker.py:192-194` `_open_audio` 있을 때만 `audio_end` | `out.audioEnd()` 버리는 중 무시 | 같음 |
| PCM 버리기 | `_stopPlayback()`(`:297-309`)가 `_discarding=true` · `_carry=null` · 타이머 · `_playEnd` 초기화 · `sink.flush()`. 부르는 곳 = 멈춤 `:317` · 닫기 `:330` · 오류 `:363` · audio_stop `:250`. `_onAudio` `:257` 버림 · `audio_start` `:239` 해제 | `_cut` · `_gen` 으로 지난 차례 조각 막음(이중 방어) | `OutputController.clear/accept/audioStart` | 네 경로 전부 같음 |
| 빈 final caption | `Caption.erases` `:33`(final · 원문 · 번역 둘 다 빈 값) | `session.py:453-457`(drop_open) · `:479-501`(blank filter) — 보인 id 에만 `{original:"", translation:""}` final 1번 | — | 같음 |
| 반이중 걷음 | `sendPcm` `:212-216` — `speaking` 조건 제거 · ready 뒤(listening) · 멈춤 아님 · 연결됨 | `session.py:397-402` paused 아니면 STT 로 | `canSendPcm()` ready · !paused · !closed · OPEN | 같음 |
| 멈춤 중 새 `audio_start` | 버림 풀고 재생 | 서버 pause → finalize → 새 차례 TTS | 원형과 같음(재생) | 같음 |

## 2. 재생 중 마이크 · 상태 경합 — PASS

- 앱은 재생 중 마이크를 막지 않는다. `speaking` 은 표시(`onPlayback`) · `playback_stopped` 판정에만 쓰인다. 컨트롤러 마이크 콜백(`app/lib/state/interpret_controller.dart` `_mic.start` 안)은 세대만 보고 `sendPcm` 을 부른다. 다른 곳에서 `playing` 으로 마이크를 막는 곳도 없다(grep: `playing` 은 `interpret_widgets.dart:408` 표시뿐).
- 경합 확인:
  - **멈춤 직후 `audio_start`**: `_discarding=false` · `_lastAudioId` 갱신 · `_mute()` → 재생. 서버는 pause 를 받고 finalize 하므로 새 차례가 정상이다. 앞 차례 응답 `audio_end` 는 서버 reader 에서 pause 처리보다 먼저 나가므로(`playback_stopped` → `_stop_playback` 이 같은 reader 루프 안에서 끝남) 새 `audio_start` 를 앞지르지 않는다.
  - **`audio_stop` 과 [멈춤] 이 엇갈림**: `audio_stop` 을 먼저 받으면 `speaking=false` 라 `playback_stopped` 를 안 보낸다. 엇갈려 둘 다 날아가면 서버가 `_cut` 때문에 무시한다(`session.py:428`). 문제 없음.
  - **출력 구간 꼬리(재생 끝 ~ +400ms)에 [멈춤]**: 서버 `_open_audio` 가 이미 None 이면 응답이 없고 앱은 이미 버리는 중이다. 문제 없음.
  - **다시 연결 · 언어 바꿈**: `_teardown` 이 `_generation++` 하고 `close()`(stop · `playback_stopped` 없음)한 뒤 새 `InterpretClient` 를 만든다. 상태가 넘어오지 않는다. 지난 세대 caption · playback 콜백은 `gen` 검사로 막힌다.
  - `_stopPlayback` 이 `_resumeT` 를 취소하므로 버린 뒤 타이머가 `onPlayback(false)` 를 두 번 내지 않는다.

## 3. allowed_paths 밖 `app/lib/state/interpret_controller.dart:165-171` — PASS(필요 · 부작용 없음)

- **필요함**: 클라이언트는 `onCaption` 만 내고 말풍선 목록(`captions`)은 컨트롤러가 갖는다. 지우기는 여기서만 할 수 있다. 스펙 F-4(「N문장」 셈에서 빠짐)도 `closeDrawer` 의 `captions.where(isFinal)`(`:221`)이 이 목록을 세므로 여기서 지워야 맞는다. `app/lib/interpret/` 안에서는 풀 수 없다.
- **부작용**: 모르는 key 의 erase 는 무시한다(서버도 보인 id 에만 보냄 · `session.py:497`). `removeAt` 뒤 UI 는 매번 `captions.reversed` 로 새로 그리고(`interpret_widgets.dart:346`), 인덱스를 쥐는 곳이 없다. erase 는 final 프레임에만 걸려 진행 중(partial) 말풍선 갱신에는 영향이 없다. 세대 검사(`gen != _generation`)보다 뒤에 있다.
- 경로 이탈은 리포트에 밝혀 두었다. 코디 승인 기록만 남기면 된다.

## 4. 테스트 · 정적 검사 — PASS

| 명령 | 결과 |
|---|---|
| `fvm flutter analyze`(app) | No issues found |
| `fvm flutter test test/interpret`(1회) | **+34 All tests passed**(`interpret_playback_test.dart` · `interpret_mock_ws_test.dart` · `interpret_test.dart` · handshake 포함) |

덮는 범위: 반이중 걷음 · `audio_stop`(id null · 다른 id) · 버림 · 새 발화 재생 · `playback_stopped` 순서 · +400ms 경계 · 닫기 · 오류 무송신 · 멈춤 중 재생 · 모르는 프레임 · erase(컨트롤러 셈 포함) · 목 WS 실제 핸드셰이크 흐름.
빈 곳(경미 · 로직은 위 2절에서 확인): 「멈춤 상태에서 `audio_stop` 수신」 · 「`playback_stopped` 와 `audio_stop` 엇갈림」은 테스트가 없다.

## WARN

- **W-1 `app/lib/ui/interpret_widgets.dart:409`** — 재생 중 안내 「번역 음성이 나오는 동안은 듣지 않아요」가 반이중을 걷은 뒤로는 사실과 다르다(이제 재생 중에도 듣는다). 브리프 · U-15(「상태 글자 · 안내 글자는 프로토 그대로 — 새 글자를 짓지 않는다」)에 따라 워커가 그대로 두었다. 코드 결함이 아니라 제품 결정이다. 사용자에게 「안내 줄 비우기」와 「새 글자」 중 무엇으로 할지 물어야 한다. 0.2.0 실기기 전에 정할 것을 권한다(병원 직원이 보는 안내와 동작이 어긋난다).

## INFO(이번 커밋 결함 아님 · 실기기 A-50/I-6 에서 볼 것)

- **I-1 `interpret_client.dart:268-270`** — 출력 구간 끝(`_playEnd`)은 받은 바이트 길이와 벽시계로 셈한다. 실제 플레이어 출력 지연은 들어가지 않는다. 플레이어 버퍼 지연이 400ms 를 넘으면, 소리가 아직 나는데 `speaking=false` 라 [멈춤] 이 `playback_stopped` 를 안 보낼 수 있다. 기존 계산이고 통키(실제 `onended` 기준)와 다른 점이다. 서버 쪽 차례도 대개 끝난 상태라 영향은 작다.
- **I-2 `app/lib/interpret/audio_io.dart:107-130`** — `flush()` = `FlutterPcmSound.release()` 다(세션 비활성화는 없다 — 플러그인 `cleanup` 확인). 다음 `audio_start` 의 첫 `feed` 가 `setup`(setCategory · setActive)과 `_configureSession` 을 다시 한다. 0.2.0 에서는 끼어들기(`audio_stop`)로 녹음 중 재설정이 더 잦아진다. 실기기에서 마이크가 잠깐 끊기는지 볼 것.
- **I-3 `audio_io.dart:51 · :72`** — 메아리. 녹음은 `echoCancel: true`, 세션 모드는 `defaultMode` 다. 통키는 브라우저 AEC 와 서버 TokenGate 를 같이 쓴다. 앱은 서버 TokenGate · agent text 에 기댄다(스펙 「구현 확인」과 같음). 폰 스피커 되울림은 I-6 실기기에서 판단한다.
- **I-4** — 워크트리의 `backend/**` 미커밋 변경은 backend 워커 P2 몫이다. `bb8412de` 에는 `app/` 만 있다(stat 6 파일 확인).
