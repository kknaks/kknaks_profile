# day-app mobile — 독립리뷰 F1 · W1~W9 수정 결과 (task_c6d0969b5e1b)

## 상태: done — 앱 구현 수정 · 재검증 통과. 통합 검증(실서버 · 실기기 · APNs · Soniox)은 그대로 pending

- 입력: `review-mobile-code-report.md`(FAIL — F-1 + W-1~W-9) · 원 브리프 · SPEC 78f3ee59 · 사용자 「머지는 마지막인데 코드 구현해」. 이전판 증거 `mobile-code-report.md` 는 그대로 보존.
- 코드 트리 `CENTURION_DAY/day-app`(HEAD `6c6b9d13` — backend D1 커밋, **수정 안 함**). 변경은 `app/**` 만(아직 untracked). 커밋 · push · PR · 머지 · 서명 · 시뮬레이터 · 기기 · 실 env 0. 하위 워커 · 위임 0.
- 코디 후속 반영: msg_1673f0e4e74a(iPad 모달을 세션 Navigator 에) · msg_ba47a004ec80(W7 loopback 실제 핸드셰이크 · 시간 제한 정리).

## 검증 — 수정본 기준 (증거 `mobile-evidence/fix1-*`)

| 명령(cd app) | 결과 | 증거 |
|---|---|---|
| `fvm flutter analyze` | No issues found | `fix1-flutter-analyze.txt` |
| `fvm flutter test` | **155 passed / 0 failed**(이전 112) | `fix1-flutter-test.txt` |
| `tool/native_logic_test.sh` | **47 PASS / ALL PASS**(이전 39 — 리뷰 집계 40) | `fix1-native-logic-test.txt` |
| `fvm flutter build ios --no-codesign` | ✓ Built Runner.app 17.6MB · unsigned | `fix1-flutter-build-ios.txt` |
| 정적 | app/ 밖 변경 0 · `DEVELOPMENT_TEAM` 0 · lib 실주소 0 · plist 권한 키 = 마이크 하나 | `fix1-static-checks.txt` |
| 변이 확인(F1) | push 동일성 · board dispose 가드 · app.dart 세션 결속을 일부러 지우면 `session_race_test` 6건 중 **5건 실패**, 되돌리면 6/6 통과(그 뒤 iPad 모달 1건 더해 7건) | 작업 로그(이 리포트) |

## 항목별

### F1 — 이전 세션의 늦은 응답이 새 세션을 지움
- 변경
  - `SessionController.endSession(code, of:)` · `showForbidden(of:)` — **넘긴 세션이 지금 세션일 때만**(`sameSession` = token · 대상) 묶음 · 화면을 지운다. 두 번째 종료 · 이전 세션 종료는 아무것도 하지 않음.
  - 저장소 삭제는 `SessionStore.clearIf(세션)` — 네이티브 `day/session` `clearIf` 가 직렬 큐 안에서 비교 · 삭제를 한 번에(`SessionKeychain.clearIf`). 그 사이 저장된 새 세션은 남김.
  - 로그인 · 병원 선택은 시도 번호(`_epoch`)로 await 뒤마다 확인 — 낡은 결과 · 오류는 버림(catch 쪽 포함).
  - 복원 `_restore` — await 뒤 성공 · 오류 모두 `phase == restoring && identical(session, saved)` 일 때만 반영.
  - 로그아웃 — 진행 중 잠금(`loggingOut`) · 끝난 뒤 지금 세션이 그 세션일 때만 로그인 화면으로(그 사이 만료 → 새 로그인이면 새 세션 그대로).
  - `PushCoordinator` — 성공 · 오류 · /me 확인 모든 await 뒤 `identical(_session, session)` · `onSessionEnd(code, session)` 로 세션 결속.
  - `BoardController` — `_disposed` 뒤 `run` 의 콜백 · 토스트 · `notifyListeners` 무시(disposed ChangeNotifier 오류 제거), SSE 콜백도 같음.
  - `app.dart` — 판 콜백은 그 판을 연 세션(`of: s`)에, 푸시 콜백은 요청 세션에 묶음.
- 테스트(실제 `DayApp` 배선 · 실제 클래스 · 서버만 지연): `test/ui/session_race_test.dart`
  - 재현 1(늦은 기기 등록 401) · 재현 2(닫힌 판의 늦은 [시작] 응답 — 401 · 늦은 성공 200 · 늦은 409) → 새 세션 · 판 · 저장 그대로 · 토스트 없음 · `takeException` null
  - 늦은 로그아웃(DELETE 지연 중 SSE 만료 → 새 로그인 → 앞 로그아웃 완료) → 새 세션 그대로 · 앞 logout 은 앞 토큰으로만
  - 중복 종료(SSE 만료 뒤 같은 세션의 늦은 401) · iPad 모달(아래)
  - 컨트롤러: 늦은 복원 결과 · 이전 세션 endSession/showForbidden · 중복 종료(`session_controller_test` 「fix1 — F1」)
- iPad 모달(코디 후속): `chart_sheet.dart` `showDialog` · `doctor_picker.dart` `showGeneralDialog` 에 `useRootNavigator: false` — 세션 Navigator(`_BoardShell`)와 같이 사라짐. 바텀 시트는 원래 nested. 테스트: iPad 에서 차트 · 원장 고르기 팝오버를 연 채 세션 끝 → 사라짐 · 새 로그인 뒤 이전 고객 · 의사 글자 0.

### W1 — 기기 등록 401
- 변경: 등록 401 → **같은 세션** `/me` 확인. `/me` 200 = 세션 유지 · 푸시만 pending · `/me` 401 = 그 세션만 U-12 종료 · `/me` 연결 실패/5xx = 세션 유지 · 푸시만 pending. 매 await 뒤 세션 동일성. SPEC · 정책 변경 없음(§3 「401 은 세션 처리」 + A-24 「푸시만 없음」을 함께 만족하는 기술 처리) — README 표로 구분.
- 테스트: `push_coordinator_test` 「등록 401 → 같은 세션 /me」 4건(200 · 401 · 503 · 이전 세션의 늦은 401 은 /me 도 안 부름).

### W2 — Keychain 저장 실패
- 변경: `_finish` 의 `store.save` 예외(PlatformException 등) → 남은 레코드 정리 시도 → 로그인 실패 코드 `keychain_save_failed`(원천 문구 없음 — 코드만) · busy 해제 · 세션 · /me · 푸시 hook 안 열림.
- 테스트: `FailingStore` — 로그인 · 병원 선택 둘 다 busy=false · session/me null · 저장 0 · hook 0 · 화면 글자에 토큰 0 · 다시 누르면 성공.

### W3 — 로그인 75초 전체
- 변경: `DayApi._send` 가 send + 머리 + 본문 전체를 하나의 `.timeout` 으로(일반 요청 20초도 같은 방식). 재전송 0 · 리다이렉트 0 유지.
- 테스트: fakeAsync + `MockClient.streaming`(머리 74초 + 본문 30초 지연) → 74.9초엔 진행 중, 75.1초에 `timeout` · 요청 1회 · 저장 0 · 3분 뒤에도 1회.

### W4 — environment · staff_id 경계
- 변경: `environment` ∈ {prod, dev} 만(로그인 · 병원 응답 · /me 비교 · Keychain 레코드). 개발 빌드 legacy 만 null. release 는 저장 묶음 environment 누락/모름이면 복원하지 않고 지움. `/me` `staff.id` · 레코드 `staff_id` = uuid(빈 값 · 형식 밖 → `unexpected_response` · 저장 0). Swift `DaySession.parse` 도 같은 검증 + `decide` 가 staff uuid 아니면 미전송. expires_at 누락/깨짐 거절은 기존대로.
- 테스트: 정식 · 개발 빌드 `staging` 거절 · `/me` staff `''`/`abc`/`42` 저장 0 · 레코드 검증 · release legacy null 복원 0 · native(빈/숫자 staff · staging · legacy null · 비-uuid staff 미전송).

### W5 — 통역 오류 뒤 마이크
- 변경: `onError`(서버 error · 끊김 · 1008 · 연결 실패 모두 `_fail` 경유) → 즉시 `_stopMic`. 문구 변경 없음.
- 테스트: 서버 error · close 1008 · 연결 끊김 각각 → `recording=false` · mic.stop 호출 · 드로어는 열린 채.

### W6 — 마이크 start/stop 겹침 · 녹음기 누수
- 변경: 녹음기 **컨트롤러당 하나**(`deps.mic()` 한 번) · start/stop/dispose 를 한 줄 큐로 차례 실행 · start 뒤 세대가 바뀌었으면 바로 stop · 지난 세대 PCM 은 보내지 않음 · start 실패면 stop 후 프로토 문구 · dispose 는 stop 뒤 `AudioRecorder.dispose`. `RecordMic.start` 는 앞 녹음이 있으면 먼저 stop. 반이중 · sink flush · 종료 정리는 그대로.
- 테스트: 느린 start 중 닫기 → start 뒤 stop · 늦은 조각 전송 0 / 느린 start 중 언어 바꿈 + restart → 녹음기 생성 1회 · 앞 세대 전송 0 · 새 세대만 전송 · dispose 1회 / start 오류 → 문구 · stop 1회.

### W7 — 핸드셰이크 거절 판별
- 확인: 현재 SDK(3.44.8 / Dart 3.12.2) `_http/websocket.dart:435` `WebSocketException.httpStatusCode`(int?) 실재 · `WebSocket.connect` 는 101 아니면 그 칸을 채움. 단 `WebSocket.connect` 는 GET 리다이렉트를 따라가므로(HttpClientRequest 기본) 쓰지 않음.
- 변경: `IoTransport.open` = 최소 핸드셰이크 어댑터 — `HttpClient.openUrl` · `followRedirects=false` · Bearer · 키/`Sec-WebSocket-Accept` SHA-1 확인(`crypto` 의존 추가 — 캐시 패키지) · `detachSocket` → `WebSocket.fromUpgradedSocket`. 101 아니면 `WebSocketException(…, status)` · `isAuthRejection` = 401/403(문자열 판별 제거). 10초 시간 제한 때 자기 HttpClient 를 `close(force:true)` · 늦게 끝난 소켓/WS 즉시 닫음. 새 서버 API 없음.
- 테스트(`test/interpret/handshake_test.dart` — 테스트 프로세스 안 loopback `HttpServer`(포트 0 · 사용자 서버/포트 무관)): 101 Bearer · 문자+바이너리 왕복 / 403 · 401 → `httpStatusCode` · 권한 거절 / 302 → 미추종(대상 경로 요청 0) / InterpretClient 실제 403 → 로그인 거절 안내, 404 → 연결 실패 안내 / 시간 제한 100ms → TimeoutException · 서버가 늦게 업그레이드한 연결은 이미 끊김(readyState closed · 1006). 가짜 opener 더블도 실제 `WebSocketException('…', 403)` 타입으로 바꿈.

### W8 — 테스트 보강
- `FakeServer.unmatched` 추가 + `Harness.expectSent(method, url, body)` — 라우트 불일치(404)면 실패. 수락 · 재호출 · 호출 UI 테스트를 메서드 · 정확한 URL · 라우트 일치로 강화.
- 칩/카드 순서: 서버 순서(v4,v1,v5,v2,v3)를 id · 방 이름 · 입실 순서와 모두 다르게 — 아이패드 격자 · 「확인 필요」 칩 안에서도 서버 순서.
- 컨트롤러 경로: recall · accept · finish · undo-start · undo-finish · anesthesia/end(라우트 일치 · 본문).
- 화면 조작(`test/ui/actions_test.dart`): [시작] · [종료] · 더보기 「시작 취소」/「완료 취소」 · 마취 칩 시작→종료 · [귀가 대기] — 각각 정확한 경로.
- 짧은 변 599 = 폰(한 열 · 리스트) / 600 = 아이패드(두 열 · 격자). 320 폭 재호출+수락 동시 호출 상자 · 재호출/수락 고르기 창 overflow 0 + 수락 요청 경로.

### W9 — 목록 밖 지정 원장
- 변경: `acceptDefault` — 지정 호출 원장이 `doctors[]` 에 없으면 null(본인 · 다른 의사로 채우지 않음). `PickerPanel` 은 기본값이 창의 줄(「모든 의사」는 호출 · 재호출만)이 아니면 선택하지 않음 → [수락] 꺼짐.
- 테스트: 목록 밖 지정 원장 호출 → 「의사를 선택하세요」 · 버튼 비활성 · 수락 요청 0.

## 한계 · pending (숨기지 않음)
- Keychain 비교 · 삭제의 직렬 큐는 코드 구조 근거 — 실제 iOS Keychain 동시 경합은 실기기에서 실행 검증하지 않았다(판단 규칙 `storedMatches` · `shouldClear` 는 swiftc 로 검증).
- 실제 마이크(`record`) · PCM · TTS · APNs · 알림 액션 · 백그라운드 실행은 실기기 pending. W7 은 loopback 실제 소켓으로 검증했지만 TLS(wss)와 D-3 실서버는 pending.
- 비차단 참고(리뷰 「참고」) 중 범위 밖이라 그대로 둔 것: 빠른 말하기 TTS 반이중 없음(프로토와 같음) · 더블 클래스가 lib/ 에 있음 · 원장 창 「추천」 배치 차이. 로그아웃 이중 누름은 F1 수정에서 `loggingOut` 잠금으로 함께 막힘.
- 통합 검증(dev · day-local · 시뮬레이터/실기기 화면 · D-2 · D-3 · prod 데모 넘김)은 전부 pending. 더블 PASS ≠ 실통합 완료.

## 변경 파일(app/ 안)
lib: `app.dart` · `data/{day_api,session_store}.dart` · `state/{session_controller,push_coordinator,board_controller,interpret_controller}.dart` · `interpret/{interpret_client,audio_io}.dart` · `ui/{board_screen,doctor_picker,chart_sheet}.dart` · `pubspec.yaml/.lock`(crypto) · `README.md`
ios: `Runner/AppDelegate.swift`(clearIf 채널 · 큐) · `Runner/AcceptLogic.swift`(env · staff uuid · storedMatches) · `NativeLogicTests/main.swift`
test: `support/{fixtures,ui_harness}.dart` · `ui/{app_flow,session_race,actions}_test.dart` · `state/{session_controller,push_coordinator}_test.dart` · `data/board_stream_test.dart` · `interpret/{interpret,handshake}_test.dart`
