# 리뷰 리포트 — day-app / code · iOS 앱 재검수 F-1 · W-1~W-9 (2026-11-09)

- 대상: `/Users/kknaks/orca/workspaces/CENTURION_DAY/day-app/app/**` 수정본(아직 untracked). HEAD 는 `6c6b9d13`(backend D1)이고 `git status` 는 `?? app/` 하나뿐이라, backend 는 바뀌지 않아 다시 보지 않았다.
- 입력:
  - `review-mobile-code-report.md`(1차 — FAIL F-1 + W-1~W-9) · `mobile-fix1-report.md` · `mobile-fix1-brief.md`
  - SPEC 78f3ee59 · #235 · 사용자 미머지 구현 지시
- 변경 확인 방법: 1차 검수 때 떠 둔 scratchpad 사본(`appcopy`)과 지금 `app/` 을 `diff -u` 로 줄 단위 대조했다. 대조한 파일: lib 13 · ios 3 · test 9 + 새 파일 4.
- 이번에는 **하위 위임 · 보조 agent 0** — 모든 읽기 · 실행 · probe 를 본인이 했다. 원본 `app/` 수정 0(probe 는 scratchpad 사본 `appcopy2` 에서).

## 판정: PASS — 차단 없음

- F-1 은 고쳐졌고, 같은 불변식(이전 세션의 늦은 응답은 새 세션 · 저장소 · 토스트를 건드리지 않음)을 원 probe 와 확장 probe 로 다시 확인했다.
- W-1~W-9 는 모두 코드 · 테스트로 해소됐다.
- 새 회귀는 찾지 못했다. 아래 참고 4건은 비차단이다.

## 직접 실행 · 수치

| 관문 | 결과 |
|---|---|
| `cd app && fvm flutter test` | **155 passed**, 0 failed — 워커 수치와 같음 |
| `app/tool/native_logic_test.sh` | exit 0. **`^PASS ` 행 47건 · `^FAIL ` 0건**(마지막 줄 `ALL PASS` 는 집계에서 뺌) |
| 증거 확인(재실행 안 함) | `fix1-flutter-analyze.txt` No issues found · `fix1-flutter-build-ios.txt` ✓ Built Runner.app 17.6MB(unsigned) |
| scratch probe(`test/probe/race2_probe_test.dart` — 실제 `SessionController` · `PushCoordinator` · `BoardController` · `DayApi`+`MockClient`, `app.dart` 와 같은 결속) | 4/4 — 결과는 F-1 표 |

**수치 정정(1차 리포트):** 1차 리포트의 native 「40 PASS」는 `ALL PASS` 줄까지 센 값이다. 실제 테스트 건수는 **39건**이다(`mobile-evidence/native-logic-test.txt` 에서 `^PASS ` 39행 확인). 이번 수정본은 47건이다.

## 지적별 확인

### F-1 이전 세션의 늦은 응답 → PASS

- 코드:
  - `session_controller.dart`:
    - `endSession(code, of:)` · `showForbidden(of:)` 는 `sameSession`(token · 대상)일 때만 동작한다.
    - 로그인 · 병원 선택은 `_epoch` 로, await 뒤마다 `_check` 를 부르고 catch 쪽도 확인한다.
    - `_restore` 는 await 뒤 `_stillRestoring`(phase · `identical`)일 때만 반영한다.
    - `logout` 은 `loggingOut` 잠금, `_clearStoreIf(current)`, 끝난 뒤 `sameSession` 일 때만 로그인 화면으로 간다.
  - `session_store.dart`: `sameSession` · `clearIf` — Keychain 채널 `clearIf` 가 네이티브 `SessionKeychain.clearIf`(직렬 큐 안에서 읽기 · 비교 · 삭제)로 간다(`AppDelegate.swift` `case "clearIf"`). `AcceptLogic.storedMatches` 는 깨진 레코드라도 token · 대상이 같으면 지운다.
  - `push_coordinator.dart`: 모든 await 뒤 `_current(session)` 을 보고, `onSessionEnd(code, session)` 으로 세션에 묶는다.
  - `board_controller.dart`: `_disposed` 뒤에는 run 의 콜백 · 토스트 · `notifyListeners` 와 SSE 콜백을 무시한다.
  - `app.dart:60 · 96-98`: 판 콜백은 `of: s`(그 판을 연 세션), 푸시 콜백은 요청 세션으로 묶인다.
- 독립 probe(1차에서 실패했던 시나리오 그대로 + 확장):

| 시나리오 | 1차 | 지금 |
|---|---|---|
| tok1 등록 PUT 대기 → 로그아웃 → tok2 로그인 → PUT 401 | signedOut · 저장 null | **board · tok2 유지** · 확인용 /me 도 안 부름(호출 2회 = 로그인 2번) |
| tok1 PUT 401 → 같은 세션 /me 대기 → 로그아웃 → tok2 로그인 → /me 401 | — | **board · tok2 유지** |
| tok1 [시작] POST 대기 → 로그아웃 · board dispose → tok2 로그인 → 401 | signedOut · null · FlutterError | **board · tok2 · 토스트 없음 · 오류 없음** |
| 복원 /me 대기 → 그 세션 종료 → 새 로그인 → 복원 /me 401 | — | **board · 새 토큰 유지**(늦은 복원 결과 버림) |

- 저장소 조건부 삭제: 원자성은 네이티브 직렬 큐라는 코드 구조가 근거다. 실제 Keychain 동시 경합은 실기기에서 pending.
- 원본 회귀 테스트(`test/ui/session_race_test.dart`)는 `Harness.start → DayApp(appDeps(...))` 로 실제 앱 배선을 쓰고 서버만 늦춘다(`ui_harness.dart:51-56`). 다루는 것:
  - 재현 1 · 2(401 · 늦은 200 · 409)
  - 늦은 로그아웃
  - 중복 종료
  - iPad 모달
  - 확인 단언: 저장 토큰 · 판 화면 · `takeException()==null` · 토스트 없음
- 워커는 변이 확인(가드를 지우면 6건 중 5건 실패)을 보고했다. 이 리뷰에서는 다시 하지 않았다 — 위 독립 probe 가 같은 가드를 직접 쳤다.

### iPad 모달 세션 결속(코디 점검) → PASS

- `chart_sheet.dart:19` `showDialog(useRootNavigator: false)` · `doctor_picker.dart:32` `showGeneralDialog(useRootNavigator: false)`.
- 나머지 오버레이도 모두 세션 Navigator(`_BoardShell`) 안이다:
  - `showModalBottomSheet`(board_screen:148 · interpret_widgets:80 · :109 · chart_sheet:26 · doctor_picker:43)는 기본 nested.
  - `PopupMenuButton`(room_screen:480)도 기본 nested.
  - `rootNavigator: true` 사용 0.
- 세션이 끝나면 `home` 이 LoginScreen 으로 바뀌어 `_BoardShell` Navigator 가 통째로 사라진다.
- 위젯 테스트(`session_race_test.dart:124-159`): iPad 에서 차트 · 원장 팝오버를 연 채 세션 끝 → 둘 다 없음 · 새 로그인 뒤 「이전고객」 · 「김원장」 글자 0 · 예외 0.

### W-1 기기 등록 401 → PASS

- `push_coordinator.dart` `_confirmSession`: 등록 401 이면 같은 세션 `/me` 로 확인한다.
  - 200 → 세션 유지 · 푸시 pending
  - 401 → `onSessionEnd(code, 그 세션)`
  - 연결 실패 · 5xx → 세션 유지
  - 매 await 뒤 `_current` 확인
- SPEC-003 392행 「401 은 세션 처리」와 A-24 「푸시만 없음」을 같이 만족하는 기술 처리다. 새 정책 아님.
- 테스트 4건(`push_coordinator_test.dart:93-125`).

### W-2 Keychain 저장 실패 → PASS

- `_finish` 가 `store.save` 예외를 잡는다:
  - epoch 를 확인하고, 남은 레코드를 정리 시도한다.
  - `_LoginFail('keychain_save_failed')` → `_fail` 로 busy 해제 · 코드만 보인다(새 문구 0).
  - 세션 · hook 은 열리지 않는다.
- 테스트(`session_controller_test.dart:385`): 로그인 · 병원 선택 · 비밀 노출 0 · 다시 누르면 성공.

### W-3 로그인 75초 전체 → PASS

- `day_api.dart` `_send`: 보내기 · 머리 · 본문을 감싼 async 블록 하나에 `.timeout` 하나. 일반 20초도 같은 방식이다. `followRedirects=false` · 재전송 0 은 그대로.
- 테스트(`session_controller_test.dart:428`): 머리 74초 + 느린 본문 → 75초에 timeout · 요청 1회.

### W-4 경계 → PASS

- Dart:
  - environment ∈ {prod, dev}: `_targetFrom` · `_environmentMatches` · `SessionBundle.fromJson`
  - release 는 저장 묶음 env 가 없거나 모르는 값이면 복원 없이 지운다(`start`).
  - staff_id 는 uuid: `Me.parse` · `fromJson`
- Swift:
  - `DaySession.parse` 가 env · staff uuid 를 검증한다.
  - `decide` 는 staff uuid 가 아니면 `.invalid`(보내지 않음).
- 개발 legacy null 예외는 release 에서는 막힌다. expires 누락 거절은 그대로.
- 테스트: session 466 · 476 + native.

### W-5 오류 뒤 마이크 → PASS

- `interpret_controller.dart` `onError` → `_stopMic()`. 서버 error · 1008 · 끊김 · 연결 실패가 모두 `_fail` 을 거친다.

### W-6 start/stop 경합 · 누수 → PASS

- 녹음기는 컨트롤러당 하나(`_micSource ??=`).
- start · stop · dispose 는 `_micQueue` 로 한 줄씩 차례로 돈다.
- start 뒤 세대가 바뀌었거나 오류면 즉시 stop, 지난 세대 PCM 은 전송 0.
- dispose 는 stop 뒤 `AudioRecorder.dispose`.
- `RecordMic.start` 는 앞 녹음이 있으면 먼저 stop.

### W-7 핸드셰이크 판별 → PASS (pending 표시)

- `IoTransport.open` 은 직접 핸드셰이크한다:
  - `HttpClient.openUrl` · `followRedirects=false` · Bearer 헤더
  - 무작위 키 + `Sec-WebSocket-Accept` SHA-1 검증
  - `detachSocket` → `WebSocket.fromUpgradedSocket`
- 101 이 아니면 `WebSocketException(…, status)` 를 던지고, `isAuthRejection` 이 `httpStatusCode` 401 · 403 을 본다. 문자열 판별은 없어졌다.
- 시간 제한은 `close(force:true)` 와 늦은 소켓 폐기로 처리한다.
- 테스트(`handshake_test.dart`, 테스트 프로세스 안 loopback 실제 소켓): 101 · 401 · 403 · 302 미추종 · 시간 제한 · InterpretClient 403 vs 404.
- 새 의존 `crypto`(pubspec · lock).
- 손수 짠 프로토콜 코드라 TLS(wss) 경로와 D-3 실서버는 검증하지 못했다 — pending.

### W-8 테스트 → PASS

- `FakeServer.unmatched` + `Harness.expectSent` — 라우트가 안 맞으면(404) 실패한다.
- 칩 순서: 서버 순서를 id · 방 · 시각과 모두 다르게 바꿨다(`app_flow_test.dart:238`).
- 컨트롤러 경로 6개(`board_stream_test.dart:214`).
- 화면 조작 tap 테스트(`actions_test.dart`).
- 경계: 599/600(`actions_test.dart:80`) · 320 폭 재호출+수락 상자 · 고르기 창(:95).

### W-9 목록 밖 지정 원장 → PASS

- `acceptDefault` 는 지정 원장이 목록에 없으면 null 을 돌려준다(`board_screen.dart:427-431`).
- `PickerPanel` 초기값은 창에 있는 줄만 받는다(`doctor_picker.dart:118-122`).
- 테스트 `actions_test.dart:126`: 기본 선택 없음 · [수락] 꺼짐 · 요청 0.
- 부수 확인: `kind=one` 은 항상 target 이 있으므로(서버 계약) 본인 기본값으로 넘어가지 않게 바뀐 것은 SPEC-002 OQ-19 와 같다.

## 신규 회귀 확인

- 문구: 새로 생긴 것은 코드 `keychain_save_failed` 뿐이다(문구 0). README 표는 화면 글자가 아니다. 빠른 말하기 TTS · 「추천」 배치 등 비차단 참고 항목은 손대지 않았다.
- 권한 · 경로 · 순서 · 수락/재호출 조건은 바뀌지 않았다(board_screen 변경은 `acceptDefault` 한 함수).
- 155 테스트 전부 통과 · analyze 0 · unsigned build 성공(증거).

## 참고 (차단 아님)

1. **깨진 Keychain 레코드가 남는다.** 시작 때 `fromJson` 이 null 이면(칸 누락 · 모르는 env · 비-uuid) `KeychainSessionStore.load` 가 null 을 돌려주고, `start` 는 지우지 않고 로그인 화면으로 간다(`session_controller.dart` `start`). 레코드는 다음 로그인 저장 때 덮어써지고 네이티브도 nil 로 무시하므로 영향은 없다. 이 경계는 「쓰지 않음」으로 지켜진다.
2. **로그아웃이 겹칠 때.** 앞 세션 로그아웃(DELETE · logout 각 최대 20초)이 진행 중일 때, SSE 만료 → 새 로그인이 일어나면 그 사이 새 세션의 [로그아웃]은 `loggingOut` 때문에 조용히 무시된다(최대 약 40초). 세션 안전에는 문제가 없고 드문 순서다.
3. **W-7 손수 만든 핸드셰이크.** 보안상 맞는 선택(리다이렉트 금지)이지만 유지보수할 코드가 늘었다. wss(TLS) 실경로는 실기기 · D-3 서버로 확인해야 한다.
4. 1차 리포트의 native 수치 정정(40 → 39)은 위에 적었다.

## 직원이 실물에서 만날 자리

- 1차 F-1(로그아웃 → 바로 재로그인 → 튕김)은 더블과 probe 기준으로 사라졌다. 실서버 · 실기기에서 같은 순서로 한 번 확인하면 좋다.
- Keychain 저장 실패 · 통역 오류는 이제 코드만 보이거나(문구 OQ) 마이크가 꺼진다.

## 실물 통합 pending (앱 완료로 주장하지 않음)

- 실제 Keychain 동시 경합 · 잠금 화면 읽기
- APNs 토큰 · 도착 · 알림 [수락] 백그라운드/콜드 스타트 실행(서명 · D-2)
- 실제 마이크 · PCM · TTS
- wss TLS 핸드셰이크 · 통역 실서버(D-3 · Soniox)
- dev · day-local 개발 빌드 연결 · 시뮬레이터/실기기 화면
- prod 데모 넘김
- XCTest(RunnerTests) 미실행
- 사용자 설정값(Bundle ID · Team · 진입점 · 허용 origin · APNs 환경 · 아이콘)이 없는 것은 결함 아님.
