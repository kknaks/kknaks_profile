# 리뷰 리포트 — day-app / code · iOS 앱(app/**) + D1↔앱 계약 (2026-11-09)

- 대상: `/Users/kknaks/orca/workspaces/CENTURION_DAY/day-app/app/**`(untracked, 브랜치 `kknaksss/day-app`). 백엔드 D1 은 6c6b9d13 으로 커밋된 상태라 그 실제 코드와 계약을 맞춰 봤다.
- SSOT: mediness `day-app-spec` 78f3ee59 의 DAY-SPEC-003 전문, DAY-SPEC-001 「앱 환경 연결」, DAY-SPEC-002, mobile-deployment. 그 밖에 Delivery #235, 사용자 지시(미머지 SPEC 기준 구현 — 결함으로 보지 않음), `mobile-code-report.md`, `review-backend-code2-report.md`, 프로토 `cc-prototype/procedure/app`(read-only), 실제 backend `routers/api` · `schemas` · `services` · 웹 템플릿 · `MESSAGES`.
- 검수 범위:
  - 직접 읽음: session · origin · build_config · day_api · board_stream · board_controller · app.dart · AppDelegate.swift · AcceptLogic.swift · Info.plist · entitlements.
  - 판 · 룸 · 원장 고르기 · 문구 · 배치, 통역 · 푸시: 읽기 전용 보조 검토 2건을 돌려 결과를 받고, 핵심 줄은 다시 열어 확인했다.
  - 코디 후속 질문 2건(푸시 401 · 이전 세션 응답)은 실제 코드로 probe 했다.

## 판정: FAIL — 차단 1건 (F-1). 나머지는 WARN · 참고

## 직접 실행

| 명령 | 결과 |
|---|---|
| `cd app && fvm flutter test` | **112 passed** (All tests passed — 워커 수치와 같음) |
| `app/tool/native_logic_test.sh` (TMPDIR = scratchpad, 실제 `ios/Runner/AcceptLogic.swift` 를 컴파일) | **40 PASS / ALL PASS** (워커 보고 39 — 하네스에 한 건이 더 있음) |
| probe: `app/` 을 scratchpad 로 복사하고 `test/probe/race_probe_test.dart` 1개를 더함. 실제 `SessionController` · `PushCoordinator` · `BoardController` · `DayApi` + `MockClient` 를 `app.dart` 와 같은 콜백 배선으로 묶음 | 2건 재현 — F-1 |
| 보조 검토: `fvm flutter test test/ui` · `test/interpret` · `test/state/push_coordinator_test.dart` | 21 · 19 통과 |

다시 돌리지 않은 것: analyze · unsigned build 는 워커 증거(`mobile-evidence/` — No issues, Built Runner.app unsigned)를 인용만 했다. 시뮬레이터 · 기기 · 서명 · 실 env 접근은 0. 원본 `app/` 은 바꾸지 않았다(`git status` 는 그대로 `?? app/`).

## FAIL

### F-1. 이전 세션의 늦은 401 이 새 세션을 지운다 (푸시 등록 · 판 조작 둘 다)

- 위치:
  - `app/lib/state/push_coordinator.dart:126-130` — `_register` 의 `on ApiError` 가 `identical(_session, session)` 을 확인하지 않고 `onSessionEnd(e.code)` 를 부른다. 성공 경로(:122)에만 그 확인이 있다.
  - `app/lib/state/board_controller.dart:135-138` — `run()` 이 dispose 된 뒤에 응답이 와도 `onSessionEnd` 를 부른다.
  - `app/lib/app.dart:60 · 96` — 두 콜백이 지금의 `SessionController.endSession(code)` 를 조건 없이 부른다.
  - `app/lib/state/session_controller.dart:311-316` — `endSession` 은 어느 세션의 끝인지 받지 않고, 지금 세션과 Keychain 묶음을 지운다.
- 근거:
  - DAY-SPEC-003 §3 「세션 보관」 — 세션 묶음 하나를 한 번에 쓰고 지우며, 토큰은 그 세션 것이다.
  - A-8 — 만료 · 401 이면 **그 세션**을 삭제한다.
  - DAY-SPEC-001 「앱 환경 연결」 규칙 5 — 토큰은 만든 세션 · 환경에서만 통한다.
  - 코디 지시 — 이전 세션의 늦은 응답은 새 세션에 영향을 주면 안 된다.
  - 같은 앱의 네이티브 쪽은 이미 이 규칙을 지킨다: `AcceptLogic.shouldClear` · `SessionKeychain.clearIfSame` — 보낸 세션과 저장된 세션이 같을 때만 지운다. Dart 쪽만 빠졌다.
- 재현(probe — 실제 클래스 · 배선):
  1. 푸시: 로그인(tok1) → 토큰 등록 PUT 이 늦게 돎 → 로그아웃 → 다시 로그인(tok2) 후 `phase=board`, 저장 `tok2` → tok1 의 PUT 이 401 `unauthorized` 로 돌아옴 → **`phase=signedOut`, 저장 null**. 방금 로그인한 새 세션이 지워졌다.
  2. 판 조작: tok1 로 [시작] POST 를 보냄 → 로그아웃 · board dispose(`_phaseChanged` 와 같음) → 다시 로그인(tok2) → 그 POST 가 401 로 돌아옴 → **`phase=signedOut`, 저장 null**. 그 future 는 `FlutterError` 로 끝난다 — dispose 된 ChangeNotifier 의 `notifyListeners`, `board_controller.dart:146` `finally`. debug 에서는 오류, release 에서는 조용히 넘어간다.
- 실제 영향:
  - 로그아웃 뒤 바로 다른 계정이나 같은 계정으로 다시 로그인하는 흔한 흐름에서, 앞 세션의 PUT/POST 가 시간 제한(20초) 안에 401 로 돌아오면 새 세션이 끊긴다. 직원은 「로그인했는데 바로 로그인 화면」을 겪는다.
  - 서버의 로그아웃 처리는 그 세션 토큰을 무효로 만들므로, 늦은 요청이 401 을 받는 것은 정상 동작이다. 그래서 재현 조건이 특수하지 않다.
  - 데이터 유출은 없다(토큰을 다른 곳으로 보내지 않음). 하지만 세션 무결성 회귀라서 차단으로 본다.
- 고칠 방향(원 워커):
  - 세션 끝 콜백에 「보낸 세션」을 넘긴다. `endSession` 은 그 세션이 지금 세션과 같을 때만 지운다(네이티브 `clearIfSame` 과 같은 규칙).
  - `PushCoordinator._register` 의 catch 앞에서도 `identical` 을 확인한다.
  - `BoardController` 는 dispose 뒤의 완료를 무시한다(`_disposed` 표시).
  - 회귀 테스트로 위 probe 두 건을 넣는다.

## WARN

### W-1. 기기 등록 401 의 처리 — SPEC 안의 문장 긴장 (문서 정합 · F-1 과 같이 해결)

- SPEC 의 두 문장:
  - DAY-SPEC-003 §3 「푸시」 오류 표 아래(spec 392행): 「앱은 400 · 401 을 화면에 띄우지 않는다(푸시만 없이 앱 사용 · **401 은 세션 처리 U-12 와 같음**)」.
  - A-24(560행) · WP A10: 「400 · 401 처리 — 화면 오류 없이 푸시만 없음」.
- 지금 코드: `push_coordinator.dart:126-128` — 401 이면 바로 세션을 끝낸다. 392행 문장과 같고, 400 · 404 · 연결 실패는 `pendingCode` 만 남긴다(PASS).
- 판단: 새 정책 질문이 아니다. 같은 세션의 401 은 그 세션이 실제로 끝났다는 뜻이고(서버 세션 규칙은 하나), 그 다음 판 · `/me` 도 401 이라 결과는 같다. 위험은 F-1 의 「다른 세션」 경우뿐이다.
- 코디가 제안한 방식은 두 문장을 모두 만족하고 안전하다: 등록 401 이면 같은 세션의 `/me` 로 확인하고, `/me` 도 401 일 때만 U-12 종료, 아니면 푸시만 pending.
- 최소 조건은 F-1 의 세션 동일성 확인이다. A-24 문장을 「401 은 그 세션이 끝났을 때 U-12」로 맞추는 것은 SPEC 정리 몫(새 정책 아님)이다.

### W-2. Keychain 저장 실패 → 로그인 버튼이 영구 잠김

- 위치: `app/lib/state/session_controller.dart:266`(`await store.save`) · `:177-182` · `:213-216` — `login` · `chooseHospital` 은 `ApiError` · `_LoginFail` 만 잡는다.
- 네이티브는 저장이 실패하면 `FlutterError("keychain_save_failed")` 를 돌려준다(`AppDelegate.swift:147-149`). 그러면 `PlatformException` 이 밖으로 새어 `busy=true` 인 채 끝난다.
- 영향:
  - 로그인 버튼이 스피너인 채로 다시 누를 수 없어 앱을 다시 켜야 한다.
  - 저장은 안 되고 토큰은 메모리에만 남아 화면도 열리지 않는다. 데이터 문제는 없지만, 조용히 멈추는 실패 경로다.
  - Keychain 쓰기 실패는 드물지만 기기 상태에 따라 날 수 있다.
- 테스트가 없다.
- 고칠 방향: 저장 실패를 로그인 실패 코드로 바꾸고 busy 를 푼다.

### W-3. 로그인 대기 75초가 「전체」가 아니다

- 위치: `app/lib/data/day_api.dart:157-158` — `client.send(...).timeout(75s)` 다음에 `Response.fromStream(...).timeout(75s)` 가 따로 돈다. 머리가 74초에 오고 본문이 늦으면 최장 약 150초가 된다.
- 근거: DAY-SPEC-003 U-1 · A-23 「로그인 HTTP 대기 = 75초」. 서버 넘김(60초)보다 길게 잡은 설계라 75초가 전체여야 한다.
- 재전송 0(A-23)은 지켜진다.
- 테스트는 `loginTimeout` 값(:225)과 「시간 초과 → 요청 하나」만 본다.

### W-4. 서버 값 경계가 느슨함 (environment · staff_id)

- environment(`session_controller.dart:229-247` · `day_api.dart:82`): `"prod"` · `"dev"` 밖의 값(예 `"staging"`)도 연결 대상 환경으로 받는다. SPEC 은 `environment = "prod" | "dev"`(DAY-SPEC-001 「낱말」)다.
  - 허용 목록 origin 확인과 `/me` 일치가 따로 있어 위험은 낮다. 다만 「모르는 환경」은 거절하는 편이 계약대로다.
- staff_id(`day_api.dart:69-70`): UUID 형식을 보지 않고 그대로 묶음에 저장한다.
  - 네이티브 수락은 그 값을 그대로 `doctorStaffId` 로 보낸다(`AcceptLogic.swift:95` — callId 는 UUID 확인을 하는데 staffId 는 안 함).
  - 서버가 검증하므로 영향은 낮다. 브리프가 짚은 「staff UUID 경계」에서 빈 곳이다.

### W-5. 통역 — 오류 뒤에도 마이크가 계속 녹음

- 위치: `app/lib/interpret/interpret_client.dart:275-282`(`_fail` 은 WS 를 닫음) · `app/lib/state/interpret_controller.dart:163-167` — `error` 값만 바꾸고 마이크를 멈추지 않는다.
- 근거: U-15 · 오류 종료.
- 영향: 서버 `error` · 끊김 · 1008 뒤에도 드로어를 닫거나 [다시 연결]을 누를 때까지 iOS 마이크 표시가 켜진 채 녹음이 이어진다. 조각은 `sendPcm` 에서 버려져 밖으로 나가지 않는다.
  - 직원 · 고객 앞에서 「마이크 켜짐」이 계속 보이는 사생활 · 신뢰 문제다.

### W-6. 통역 — 마이크 시작과 정리가 겹칠 때 녹음이 남음 · 녹음기 누수

- 위치: `interpret_controller.dart:176-178` · `audio_io.dart:61-90`.
- 세대 확인을 지난 뒤 `await mic.start` 가 도는 동안 닫기 · 언어 변경이 끼면, `stop()` 이 먼저 돌고 그 뒤 구독이 붙어 녹음이 남는다.
- `restart` · `setLang` 때마다 새 `AudioRecorder` 를 만들고 이전 것은 dispose 하지 않는다.

### W-7. 통역 — 핸드셰이크 거절(401 · 403)을 예외 문자열로 판별

- 위치: `interpret_client.dart:111-112`.
- `WebSocket.connect` 가 101 이 아닌 응답에 던지는 예외 글자에 상태 코드가 늘 들어 있다는 보장이 없다. 들어 있지 않으면 A-14b 권한 거절이 「연결할 수 없어요」로 보인다.
- 테스트는 가짜 opener 가 던지는 문자열에 기대고 있어 이 위험을 잡지 못한다.
- D-3 서버가 없어 실물로는 확인할 수 없다(pending).

### W-8. 기능이 깨져도 통과할 수 있는 테스트

- 칩 순서(`test/ui/app_flow_test.dart:296`): 서버 순서가 시간 · id 순서와 같아서, 앱이 다시 정렬해도 통과한다(규칙 1 「서버 순서」를 증명하지 못함).
- 수락 · 재호출 UI 테스트(:211 · :225 · :239 · :259): `requests.last.body` 만 본다. 경로가 틀려도 FakeServer 가 기록한 뒤 404 를 돌려주므로 본문 비교는 통과한다.
- 컨트롤러 경로 테스트(`test/data/board_stream_test.dart:198-243`): recall · accept · finish · undo-start · undo-finish · anesthesia/end 가 빠졌다. 코드 경로 자체는 실제 `routers/api/board.py` 와 같음을 확인했다.
- 화면에서 [시작] · [종료] · 더보기 · 마취 칩 · [귀가 대기]를 눌러 보는 테스트가 없다.
- 그 밖에 없는 것: 짧은 변 599/600 경계, 320 폭의 고르기 창 · 재호출+수락 동시 상자 overflow, 이전 세션 경합(F-1), Keychain 저장 실패(W-2).
- fixture id 가 uuid 가 아니다(`v1` 등). 앱이 id 를 문자열로만 다뤄 영향은 없다.

### W-9. 지정 호출의 지정 원장이 `doctors[]` 에 없을 때도 기본 선택됨

- 위치: `app/lib/ui/board_screen.dart:427-430`.
- 화면에 없는 원장이 골라진 채 [수락]이 켜지고, 누르면 서버가 `doctor_not_listed` 로 거절한다.
- 드물고 서버가 정본이라 낮음.

## 참고 (차단 아님)

- 이중 탭: 응답이 온 뒤 다음 스냅샷이 오기 전 다시 누를 수 있다. 그래도 DAY-SPEC-003 「요청이 끝날 때까지 잠근다 · 그래도 겹치면 서버 409」(429행)와 같아서 결함이 아니다. A-11 PASS.
- 원장 고르기 창 배치: 재호출 모드의 「추천」 머리 · 처음 대상 꼬리표가 웹 `ui.html` 과 다르다(`doctor_picker.dart:193-203`). 글자는 원천에 있고 배치만 다르다.
- 로그아웃에 진행 중 잠금이 없다(`board_screen.dart:161-163` · `login_screen.dart:179`). DELETE + logout(각 20초) 동안 판이 계속 조작되고, 두 번 누르면 요청이 두 번 나간다. 세션 결과는 같다.
- `showForbidden` 은 기기 DELETE 없이 푸시 세션만 비운다. 로그아웃 상태에서 누른 알림은 다음 로그인(같은 환경 · 다른 계정일 수 있음) 때 그 방으로 연다. 서버 권한이 정본이라 낮음.
- 빠른 말하기 TTS 에는 반이중이 없다(`interpret_widgets.dart:260-262`). 프로토와 같아 SPEC 위반은 아니다.
- 테스트 더블 `FakePushBridge`(`lib/data/push_bridge.dart:74`) · `MemorySessionStore`(`lib/data/session_store.dart:87`)가 `lib/` 에 있어 앱에 같이 실린다. 동작에는 영향이 없다.
- 네이티브 결과 알림: 모르는 오류 코드는 코드 그대로 보인다(`AcceptLogic.swift:128` — 문구를 만들지 않는 원칙대로).

## D1 ↔ 앱 계약 (실제 커밋 6c6b9d13 과 대조)

| 계약 | 서버(D1) | 앱 | 판정 |
|---|---|---|---|
| 로그인 · 병원 고르기 응답 `environment` · `api_base_url`(client=app) | 있음. `DAY_PUBLIC_API_BASE` 가 비면 `api_base_url` 생략 | release 는 두 칸 다 필수(`_targetFrom` :234-236). 개발 빌드만 「환경만」 → 요청 주소, 「주소만」 → 거절 | 같음 |
| 데모 넘김 응답(dev 대상) · `choose_hospital` 의 dev pending_token | prod 가 dev 대상으로 바꿔 실음 | 받은 대상으로 `/hospital` → 응답 대상 · 환경이 같아야 함(:196-199) | 같음 |
| `/me` `environment` | 늘 있음 | 저장 전 일치 확인(:256) · 복원 때도(:114) | 같음 |
| 오류 `{detail, code, field}` · `environment_unavailable` 503 | 공용 핸들러 | `code` 만 쓰고 문구 없는 자리는 코드(OQ-A16) | 같음 |
| 리다이렉트 | 서버 넘김 0 | HTTP `followRedirects=false` · SSE 같음 · 네이티브 `NoRedirect` | 같음 |
| 개발 빌드 + D1 이전 서버(두 칸 없음 · `/me` 환경 없음) | — | `held=null`, `answered=null` 일 때만 통과(:271-273) | 같음(개발 전용) |

## 인수 조건별 대응 (구현 · 테스트 · 실물)

| AC | 구현 확인 | 테스트 대응 | 메모 |
|---|---|---|---|
| A-1 보기만 · 권한 없음 | ✓ | ✓ | |
| A-2 대리 수락 · 본인 기본 | ✓ | ✓(본문만 — W-8) | W-9 |
| A-3 · A-4 일반 = prod / 데모 = dev 전부 | ✓ HTTP · SSE · 기기 · 통역 모두 `bundle.apiBaseUrl` | ✓ | |
| A-5 dev 장애 우회 없음 | ✓ | ✓ | |
| A-6 병원 여럿 · 5분 | ✓ | ✓ | |
| A-7 복원 · 부분 묶음 거절 | ✓ Dart · Swift parse 둘 다 | ✓ | |
| A-8 만료 · 401 · SSE 만료 삭제 | ✓ 같은 세션의 경우만 | ✓ | **F-1: 다른 세션의 401 도 지금 세션을 지움** |
| A-9 · A-10 SSE 순서 · 백오프 · 앞/뒤 · 오프라인 | ✓ generation 확인으로 오래된 구독이 새 세션을 건드리지 않음(SSE 경로 OK) · UTF-8 조각 · 멀티라인 data · CRLF | ✓ | |
| A-11 이중 탭 | ✓(SPEC 문장대로) | ✓(컨트롤러만) | 참고 |
| A-12 kos_failed 한 번 | ✓ | ✓(같은 이벤트 중복은 미검증) | |
| A-13 폰 / 아이패드 600 | ✓ | ✓ 390 · 320 · 1024(경계 599/600 없음) | 실물 pending |
| A-14 · A-14b 통역 언어 · 권한 | ✓ 7언어 · 빠른 말하기 원천 5언어(프로토와 글자 그대로) · 사전 없음 · Bearer 헤더 · wss | ✓(가짜 WS) | W-5 · W-6 · W-7, D-3 서버 없음 |
| A-15 기기 등록 세션 대상 · 다른 환경 알림 무시 | ✓ | ✓ | F-1(늦은 401) |
| A-16 알림 [수락] | ✓ 네이티브 실재 · 판단 로직 40건 | 판단만(swiftc) | `AcceptAction.run` · Keychain · 백그라운드 실행은 실기기 pending |
| A-16b 받는 사람 = 서버 몫 | 앱은 고르지 않음 | — | D-2 서버 없음 |
| A-17 키 · 서명 · 주소 칸 · 권한 | ✓ TextField 2 · plist 마이크 하나(프로토 문구 그대로) · Team ID 0 · 임시 Bundle ID | ✓ | 아이콘 자산 없음(후속) |
| A-18 · A-19 환경 칸 필수 · origin 엄격 | ✓ release 는 `requireEnvironment` 강제 · 로컬 http 무시 · 허용 목록 · 정규화 | ✓ | W-4(env 값 범위) |
| A-20 hospital · /me 일치 | ✓ | ✓ | |
| A-21 /me 전 저장 0 · staff_id | ✓ | ✓ | W-2(저장 실패 경로) |
| A-22 [재호출] 조건 | ✓ 웹 `inbox_card` 와 같음 | ✓(본문만) | |
| A-23 75초 · 재전송 0 | 재전송 0 ✓ | 값만 | W-3 |
| A-24 등록 400 · 401 | 400 ✓ · 401 = 세션 처리 | ✓ | W-1 문서 정합 · F-1 |

## 직원이 실물에서 만날 자리

- **로그아웃하고 곧바로 다시 로그인했는데 로그인 화면으로 튕긴다**(F-1) — 앞 세션의 기기 등록 · 조작 응답이 늦게 401 로 돌아온 경우.
- 통역에서 오류가 난 뒤에도 마이크 표시가 켜져 있다(W-5).
- 드물게 Keychain 저장이 실패하면 로그인 스피너가 멈춰 앱을 다시 켜야 한다(W-2).
- 지정 원장이 목록에 없는 호출에서 [수락]이 눌리지만 서버가 거절한다(W-9).
- `environment_unavailable` · 네트워크 오류 · 설정 오류는 문구 없이 코드로 보인다 — OQ-A16 · OQ-A7 의 열린 자리로, 결함 아님.

## 실서버 · 실물 통합 pending (구현 결함 아님 · 앱 완료로 주장하지 않음)

- dev 서버 · day-local 개발 빌드 연결
- 시뮬레이터 · 실기기 화면
- 실제 Keychain 읽기/쓰기 · 잠금 화면 읽기
- APNs 토큰 · 도착 · 알림 [수락] 실행(백그라운드 · 콜드 스타트) — 서명 · D-2 서버 필요
- 통역 실서버(D-3 · Soniox) · 실제 마이크/스피커
- prod 데모 넘김 실물 · prod 행 0 조회
- RunnerTests(XCTest)는 실행하지 않았다.
- 사용자 설정값(Bundle ID · Team · 진입점 · 허용 origin · APNs 환경 · 앱 아이콘)이 없는 것 자체는 결함이 아니다.

수정은 mobile 원 워커가 한다. F-1 이 고쳐지기 전에는 app 코드 완료로 보지 않는다.
