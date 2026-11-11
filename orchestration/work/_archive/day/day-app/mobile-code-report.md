# day-app mobile — DAY iOS 직원 앱 신규 구현 결과 보고 (task_f8b9022d67c8)

## 상태: done (앱 구현 완료 = 더블 · 로컬 검증 통과) — 통합 검증(실서버 · 실기기 · APNs · Soniox)은 전부 pending

- 기준: SPEC commit `78f3ee59c8a10e0abb1bde8896302873a46d0732`(mediness kknaksss/day-app-spec — SPEC-003 · SPEC-001 · SPEC-002 · mobile-deployment 전문) · Delivery #235(`delivery-request.json`) · 사용자 지시 「머지는 마지막인데 코드 구현해」(`implementation-user-direction.md`). **spec-baseline 은 pending 그대로** — main 머지 · baseline ready 를 주장하지 않는다. 머지 · 배포 · 서명 · TestFlight 0.
- 코드 트리: `/Users/kknaks/orca/workspaces/CENTURION_DAY/day-app`(브랜치 `kknaksss/day-app`, origin/dev `91728737`). **커밋 · push · PR 안 함.**
- **앱 생성 전 baseline**: `app/` 없음 → 대상 Flutter baseline 없음(analyze · test · build 기준선 0). FVM 캐시 Flutter 3.44.8 / Dart 3.12.2 사용 · fvm 전역 설정 변경 없음 · `app/.fvmrc` 로 앱 안 pin.
- 변경 경로: **`app/**` 만**(새 디렉터리). backend · deploy · AGENTS.md · 웹 · SPEC · 옆 세션 · 프로토 원본 수정 0(`git status` = `?? app/` 하나). 사용자 포트 · 컨테이너 · 프로세스 · 시뮬레이터 · 기기 조작 0. 실제 env · 키 · 비밀번호 읽기 · 출력 0.

## 수행 — 파일

```text
app/.fvmrc · pubspec.yaml · pubspec.lock · analysis_options.yaml · README.md · .gitignore · .metadata
lib/main.dart · app.dart                       조립(실제 어댑터) · 단계(로그인 / 복원 / 판 / 권한 없음) · 앱 생명주기
lib/core/build_config.dart                     --dart-define 5개 · 설정 오류 코드 · release 는 환경 칸 필수 강제 · 로컬 http 무시
lib/core/origin.dart                           https origin 정규화 · 허용 목록 · debug 로컬 origin 예외(정확히 같을 때만)
lib/core/copy.dart                             원천 글자만(SPEC-001 문구 · SPEC-002/웹 MESSAGES · 프로토 앱 전용 글자) · 없는 자리 = 코드
lib/data/day_api.dart                          HTTP(snake auth · camel 업무 · {detail,code,field} · 리다이렉트 안 따름 · 로그인 75초)
lib/data/board_stream.dart                     SSE 파서 · version 순서 · 3→30초 백오프 · 45초 무바이트 · session_expired · pause/resume
lib/data/session_store.dart                    세션 묶음 모델 · Keychain 채널 day/session · 메모리 더블
lib/data/push_bridge.dart                      네이티브 채널 day/push · 더블
lib/model/board.dart                           스냅샷(dev board_rules.snapshot) 읽기만
lib/state/session_controller.dart              로그인 · 병원 · /me 뒤 원자 저장 · 복원 · 401 · 로그아웃 · D-1 전 dev 대체
lib/state/board_controller.dart                스냅샷 · 시각 보정 · 이중 탭 잠금 · 오류 코드 → 토스트 · kos_failed
lib/state/push_coordinator.dart                권한 · 등록/재등록/해제(세션 대상만) · 탭 환경 확인 · 콜드 스타트 탭 대기
lib/state/interpret_controller.dart            드로어 상태 · 마이크 권한 · 언어 기억 · 요약 한 줄
lib/interpret/{interpret_client,langs,audio_io}.dart  WS(Bearer · start{lang}) · 반이중 · 7개 언어 · 빠른 말하기 원천 5언어 · record/pcm/tts
lib/ui/{login_screen,board_screen,room_screen,doctor_picker,chart_sheet,interpret_widgets,widgets,format,theme}.dart
ios/Runner/AppDelegate.swift                   Keychain 세션 항목 하나 · 설치 id · 푸시 채널(준비 전 토큰 · 탭 보관) · 알림 [수락](백그라운드 · 콜드 스타트)
ios/Runner/AcceptLogic.swift                   수락 판단(Foundation 만) — 세션 · 환경 · 만료 · origin · uuid · 결과 글자 · 401 같은 세션만 삭제
ios/Runner/Runner.entitlements · Info.plist(마이크 문구 하나) · Flutter/Identity.xcconfig(임시 Bundle ID · 표시 이름)
ios/RunnerTests/RunnerTests.swift(XCTest — 시뮬레이터 필요해 미실행) · ios/NativeLogicTests/main.swift · tool/native_logic_test.sh
test/support/fixtures.dart · test/core · test/data · test/state · test/interpret · test/ui
```

화면: 로그인(MediSolve AI · DAY · 이메일 · 비밀번호) · 병원 선택(처음으로) · 복원 중(끊김 줄) · 권한 없음 · 시술 현황(머리 · 끊김 줄 · 탭 현황/호출 n/시술 완료 n · 칩 · 카드) · 룸 상세 · 원장 고르기(폰 시트 88% / 아이패드 팝오버) · 차트(읽기) · 통역 바 · 통역 드로어(92%) · 언어 목록 · 계정 시트(로그아웃).
템플릿 잔재 정리: counter 화면 · `MyApp` 테스트 제거 · Flutter 로고 AppIcon png · 1x1 런치 이미지 제거 · 앱 이름 `DAY`(`$(DAY_DISPLAY_NAME)`) · **`flutter create` 가 키체인에서 자동으로 넣은 `DEVELOPMENT_TEAM` 3줄 삭제**(Team ID 저장소 0). DAY 로고 · 아이콘 자산이 저장소에 없어 새로 만들지 않음 → README 후속.

## 검증 — 명령과 결과 (증거 `mobile-evidence/`)

| 명령(cd app) | 결과 | 증거 |
|---|---|---|
| `fvm flutter analyze` | **No issues found** (exit 0) | `flutter-analyze.txt` |
| `fvm flutter test` | **112 passed / 0 failed** (exit 0) | `flutter-test.txt`(expanded) |
| `fvm flutter build ios --no-codesign` | **✓ Built build/ios/iphoneos/Runner.app (17.6MB)** · unsigned(`code object is not signed at all`) · 2회(코디 후속 네이티브 수정 뒤 재실행 요청) 모두 성공 | `build-and-static-checks.txt`(1차) · `flutter-build-ios.txt`(최종) |
| `tool/native_logic_test.sh`(macOS `xcrun swiftc` · 시뮬레이터 없음) | **39 PASS / 0 FAIL** | `native-logic-test.txt` |
| 산출물 · 소스 검사 | Info.plist 사용 권한 키 = `NSMicrophoneUsageDescription` 하나(+ 알림은 런타임 요청 · entitlement `aps-environment`) · `DEVELOPMENT_TEAM` 0 · lib/ios 소스 실주소 0 · 키 · 계정 0 · 변경 경로 app/ 밖 0 | `build-and-static-checks.txt` |

- 실패 · 고친 것: 처음 테스트에서 2건 실패 — fakeAsync 안에서 `StreamSubscription.cancel()` 의 root-zone future 를 기다려 WS 닫기가 멈춤 → `_release` 가 transport 를 먼저 닫고 cancel 을 기다리지 않게 고침(실제 동작에도 맞음). 위젯 테스트 1건은 가로 ListView 가 보이는 칩만 만드는 것을 셌던 테스트 가정 → 단언 수정. 그 뒤 analyze · test 재실행 통과.
- 빌드 경고: `flutter_pcm_sound` · `flutter_tts` 가 Swift Package Manager 미지원 → CocoaPods 사용(`ios/Podfile` · `Podfile.lock` 생성 · 커밋 대상). 향후 Flutter 에서 오류가 될 수 있음(플러그인 몫).
- **화면 크기 위젯 검증**: 폰 390×844 · 작은 폰 320×568(긴 방 · 고객 · 시술 이름 · 12줄 메모 · 마취 넘음) · 아이패드 1024×1366 — `tester.takeException()` = null(overflow 없음). 시뮬레이터 스크린샷은 금지 범위라 없음(통합 검증 pending).
- **네이티브 실물 유무**: Swift 코드는 실재하고 빌드에 링크됨(AppDelegate · AcceptLogic). 실행 검증은 판단 로직만(swiftc). Keychain 실제 읽기/쓰기 · `UNUserNotificationCenter` 액션 · APNs 토큰 · 백그라운드 실행 · 콜드 스타트는 **실기기에서 한 번도 돌지 않았다**(서명 · 기기 필요 — pending). RunnerTests(XCTest) 는 컴파일 · 실행 안 함.

## 코디 후속 반영(네이티브 수락 · 세션)

| 요청 | 반영 | 검증 · 한계 |
|---|---|---|
| 백그라운드 · 콜드 스타트 실제 경로 · 엔진 준비 전 유실 금지 | 수락은 Flutter 없이 `didReceive`(대리자 = didFinishLaunching) → `AcceptAction`. 준비 전 APNs 토큰 · 알림 탭은 `pendingToken` · `pendingTap` 에 두고 Dart `ready` 때 넘김 | 로직 swiftc · Dart 콜드 스타트 탭 테스트. 실제 실행은 실기기 pending |
| 템플릿 잔재 | counter · Flutter 로고 아이콘 · 런치 이미지 · 기본 이름 · 자동 Team ID 제거 · RunnerTests 를 AcceptLogic XCTest 로 | 아이콘 자산은 README 후속 |
| D-1 부분 응답(dev) | 개발 빌드만 environment-only → 요청 주소 + env, 잘못된 주소는 debug 도 거절 | session「개발 빌드」3건 |
| 만료 · 필수 칸 누락 미전송 · 401 삭제 | `DaySession.parse` 가 expires_at 필수 · 만료면 `.expired`(미전송). Dart 묶음도 expires_at 필수 | native 39건 · session「expires_at」2건 |
| (msg_9c6b9ac898f0) expired 폐기 · 401 조건부 삭제 원자성 | `.expired` 도 `SessionKeychain.clearIfSame(stored)` 로 그 세션 폐기. 모든 세션 Keychain 접근(Dart 채널 load/save/clear · 네이티브 읽기 · 조건부 삭제)을 직렬 `DispatchQueue("day.session.keychain")` 하나로 — `clearIfSame` 은 읽기 · 비교(`shouldClear`) · 삭제를 한 `queue.sync` 임계 구간에서 | 비교 규칙(같은 token+대상만 삭제 · 재로그인 세션 보존)은 swiftc 로 검증. **동시 save 와의 실제 경합은 실행 검증하지 않았다**(Keychain · 기기 필요) — 직렬 큐 구조로 막았다는 코드 근거만. 프로세스 밖(다른 앱 확장) 접근은 없음 |
| 네이티브 URL 검증 | 저장 대상 https 정규화 origin 만(userinfo · port · path · `/` · 대문자 · query · fragment 거절) · http 는 DEBUG 빌드만 | native 10건 |

## 테스트 더블 경계

| 경계 | 실제 구현 | 더블 | 더블로 증명한 것 / 못 한 것 |
|---|---|---|---|
| DAY HTTP | `DayApi`(package:http · followRedirects=false) | `MockClient` 라우터(`FakeServer`) — 요청 origin · 헤더 · 본문 기록 | 대상 · 토큰 · 본문 · 오류 코드 처리 / 실제 dev · prod 서버 응답은 못 봄 |
| SSE | `openHttpSse`(연결마다 http.Client) | `FakeSse`(StreamController 바이트) | 파서 · 순서 · 백오프 · 무바이트 · 401 · session_expired / 실서버 1시간 닫힘 · 프록시 버퍼링은 못 봄 |
| Keychain 세션 | Swift `SessionKeychain`(항목 하나 · Update 아니면 Add · AfterFirstUnlockThisDeviceOnly) ↔ Dart `KeychainSessionStore` | `MemorySessionStore`(쓰기 횟수) | 저장 시점 · 원자 묶음 · 부분 레코드 거절(Dart · Swift parse 둘 다) / 실제 Keychain 동작은 실기기 pending |
| 푸시 | Swift: 권한 · `registerForRemoteNotifications` · 토큰 hex · 준비 전 토큰/탭 보관(`pendingToken`·`pendingTap` → `ready`) · 앞에서도 배너 · CALL/ACCEPT 카테고리 | `FakePushBridge` | 등록 본문 · 세션 대상 · 재등록 · 해제 · 400/401/404 · 탭 환경 · 콜드 스타트 탭(ready) / APNs 실제 도착 · 서버 D-2 없음 |
| 알림 [수락] | Swift `AcceptAction`(Flutter 엔진 없이 · didReceive 는 시작 때 대리자 설정 → 백그라운드 · 콜드 스타트에서도 옴 · beginBackgroundTask · 리다이렉트 거부 URLSession) + `AcceptLogic` | swiftc 하네스(판단 · 요청 · 결과 글자 · 401 삭제 판단) | 세션 대상만 · Bearer · `doctorStaffId = staff_id` · 다른/없는 환경 무시 · 만료 미전송 · 부분 레코드 미전송 · https 정규화(http 는 DEBUG 빌드만) · 정수/경로 주입 id 거절 · 401 같은 세션만 삭제(재로그인 세션 보존) / 실제 알림 액션 실행 · 백그라운드 시간 · 잠금 화면 Keychain 읽기는 실기기 pending |
| 통역 WS | `IoTransport`(dart:io WebSocket · Bearer 헤더 · ping 20s) | `FakeTransport` · `FakeMic` · `FakeSink` · `FakeSpeaker` | start{lang} · 반이중 · 자막 · error message · 1008 · 언어 기억 / Soniox · 실서버 D-3 · 실제 마이크/스피커 pending |

## 계약 대조 — 인수 조건별 (구현 파일 · 더블 검증 · 실통합)

| # | 조건 | 구현 | 더블 검증(테스트) | 실통합 |
|---|---|---|---|---|
| A-1 | 보기만 직무 = 조작 · [수락] 없음, 판 · 호출 · 시술 완료 보임 · 권한 행 없음 = 권한 없음 안내 | `api.Me.allows` · room/board_screen · login_screen `ForbiddenScreen` | ui「보기만 직무(코디)」·「권한 행 없는 직무」· session「권한 없음」 | pending(dev · day-local) |
| A-2 | 간호사 대리 수락 = 고른 의사 · 원장 본인 기본 = 본인 | `acceptDefault` · doctor_picker | ui「간호사 대리 수락」·「원장 본인」·「지정 호출」 | pending |
| A-3 | 일반 계정 = prod 세션 · 이후 전부 prod | session_controller | session「일반 계정 — prod」 | pending(prod 배포 · D-1) |
| A-4 | 데모 = env dev · 이후 HTTP · SSE · 기기 등록 · 통역 전부 dev | session · board_stream · push · interpret(모두 bundle.apiBaseUrl) | session「데모 계정」· push「데모 = dev 에만」· interpret「세션 대상 wss」· ui 통역 드로어 | pending(D-1 배포 · prod 행 0 은 사용자 조회) |
| A-5 | dev 장애 = environment_unavailable · prod 우회 없음 | 오류 코드 그대로 · 재전송 없음 | session「dev 장애」 | pending |
| A-6 | 병원 여럿 → 같은 대상 · 5분 지나면 session_expired | `chooseHospital` | session「병원 고르기」4건 | pending |
| A-7 | 재실행 → 저장 대상 /me 복원 · 다른 환경 안 바뀜 · 부분 묶음 없음 | `start/_restore` · `SessionBundle.fromJson` · Swift parse | session「자동 로그인」5건 · 「Keychain 레코드 칸 빠짐」· native parse 3건 | pending(실기기 Keychain) |
| A-8 | 만료 · 401 · SSE session_expired → 삭제 · 로그인 · 진입점부터 | `endSession` · board_controller · native 401 삭제 | session「세션 중 401」· stream「session_expired」·「401 응답」· controller「401 → 세션 끝」· native「401 ends session」·「re-logged-in session kept」 | pending |
| A-9 | 첫 board · 낮은 version 버림 · 1시간 닫음 뒤 재연결 · 뒤/앞 끊고 붙음 | board_stream · app `didChangeAppLifecycleState` | stream「첫 board…」·「백오프」·「pause/resume」 | pending(dev) |
| A-10 | 오프라인 → 노란 줄 · 마지막 판 · 재연결 · 묶음 그대로 | ConnectionLine · RestoringScreen | ui「끊김 → 노란 줄」· session「연결 실패 → 묶음 그대로」· stream「45초」·「5xx」 | pending |
| A-11 | 이중 탭 요청 하나 · 409 토스트 + 다음 스냅샷 | `BoardController.run` 잠금 · 버튼 disable | controller「이중 탭」·「409」 | pending |
| A-12 | 반영 중 안 그림 · kos_failed 토스트 한 번(방 · 고객) | `_onKosFailed` · `reflecting` 미사용 | controller「kos_failed」 | pending(KOS 실패 재현 시) |
| A-13 | 폰 한 열 · 시트 · 룸 한 열 / 아이패드 격자 · 팝오버 · 두 열 · 짧은 변 600 | `isTablet` · board/room/doctor_picker | ui「폰」·「작은 폰(320)」·「아이패드」 | pending(시뮬레이터 · 실기기 — 사용자) |
| A-14 | start.lang 7개 · zh-Hant · yue 구분 · 사전 화면 없음 · 서버 시드 context | langs · interpret_client | interpret「언어 7개」·「start.lang 만」· ui「통역 바 … 사전 화면 없음」 | pending(D-3 · 시드 로그는 서버 몫) |
| A-14b | 보기 권한이면 통역(코디 포함) · 없으면 WS 거절 | 통역 바 = 판 화면 안(보기 권한) · 1008/403 안내 | ui「보기만 직무… 통역은 씀」· interpret「핸드셰이크 거절」·「close 1008」 | pending(D-3) |
| A-15 | 기기 등록 세션 대상만 · 데모 토큰 dev 만 · 로그아웃 해제 · 다른 env 알림 동작 안 함 | push_coordinator · AcceptLogic | push 9건 · ui「푸시 탭」·「로그아웃」· native「other environment」 | pending(D-2 · TestFlight) |
| A-16 | 알림 [수락] = 세션 대상 · doctorStaffId = 본인 · 로컬 알림 결과 | AppDelegate `AcceptAction` · AcceptLogic | native 39건(요청 · 결과 글자 · 만료 · origin) | **pending — 실기기 알림 액션 미실행**(서명 · APNs · D-2) |
| A-16b | 받는 사람 = 호출 대상 그대로(서버 몫) · 대리 수락은 푸시와 무관 | 앱은 받는 사람을 고르지 않음 · 대리 수락은 앱 화면 | ui 대리 수락(푸시 없이) — 서버 쪽 대상 계산은 D-2 서버 더블 없음(서버 미구현) | pending(D-2) |
| A-17 | 키 · 서명 · KOS · 환경 고르기 · 서버 주소 칸 없음 · 알림 · 마이크 외 권한 없음 | Info.plist · pbxproj · login_screen | ui「로그인 — 서버 주소 칸 없음」(TextField 2개) · 산출물 plist 검사 · grep | release 실물 pending |
| A-18 | 정식 빌드 환경 칸 없음 → 실패 · 저장 없음 · 개발 빌드만 대체 | `_targetFrom` · BuildConfig(release 강제) | session 「환경 칸…」3건 · 「개발 빌드」3건 · ui「정식 빌드 환경 칸 없는 응답」· origin「release 는 꺼짐 무시」 | pending |
| A-19 | 허용 목록 밖 · http · userinfo · 443 밖 · path · query · fragment → 실패 · 요청 0 · 끝 / 같은 대상 | origin.dart | origin 15건 · session 7건(요청 수 = 1 확인) | — |
| A-20 | hospital origin+env · /me env 불일치 → 실패 · 저장 없음 | `chooseHospital` · `_environmentMatches` | session「다른 origin」·「다른 environment」·「/me environment」 | — |
| A-21 | /me 전 Keychain 비어 있음 · 묶음엔 늘 staff_id | `_finish` | session「진입점 로그인…」(핸들러 안에서 saves==0 확인) · 「expires_at 없으면」 | pending(실기기) |
| A-22 | [재호출] = need.why call · called 줄 · board edit 만 | `recallCallId` | ui「[재호출] 노출」4건(+ 기본 선택 = 처음 대상 · 본문) | pending(dev) |
| A-23 | 로그인 75초 · 자동 재전송 없음 | `DayApi.loginTimeout` · busy 잠금 | session「기본 대기 75초」·「시간 초과 → 한 번만」·「다시 눌러도 하나」 | pending(지연 재현 시) |
| A-24 | 기기 등록 400 · 401 → 화면 오류 없이 푸시만 없음 | push_coordinator | push「400 … 401」·「404」·「APNs 설정 없음」 | pending(D-2) |

## 계약 대조 — SPEC 과 같음/다름 · 판단 기록

- 같음: U-1 ~ U-16 동작 · 문구 원천(DAY-SPEC-001 문구 · 웹 `MESSAGES` · 웹 ui.html 창 글자 · 프로토 앱 전용 글자) · 서버 값만 사용 · uuid id · 프로토 경로/정수 id/`X-Accept-Source`/`?token=` 미사용 · 언어 7개 · vi/yue 칩 없음 · 사전 화면 없음 · 카드 끌어 놓기 없음(OQ-A1) · 국적 자동 언어 없음(OQ-A9).
- 문구 없는 자리(코드만 · 빈 칸): `environment_unavailable`(OQ-A16) · 설정 오류 `config_*` · 네트워크 `network_error`/`timeout`(OQ-A7) · 빈 판 빈 칸(OQ-A5) · 오더 메모 없으면 칸 없음(OQ-A6). 푸시 글자는 서버가 보내므로 앱엔 없음(OQ-A8). 마이크 안내 앱 이름 자리 = 번들 표시 이름 런타임 값(OQ-A10 · 기본 `DAY`).
- 판단(SPEC 에 명시 없음 · 리뷰 확인):
  1. 자동 로그인 때 `/me` environment 가 저장값과 다르면 묶음을 지우고 로그인 화면(코드 `environment_unavailable`).
  2. 빌드 허용 목록 밖으로 저장된 대상은 요청 없이 지운다(빌드 교체 대비).
  3. 개발 빌드에서 세션 environment 가 null(서버 D-1 전)이면 푸시 탭 · 네이티브 수락은 동작하지 않는다(환경 일치 확인 불가 — fail-closed).
  4. 코디 지시대로 D-1 부분 응답(environment 만 · `api_base_url` 없음)은 **개발 빌드에서만** 요청 주소 + 그 env 로 묶는다. 주소만 있고 env 가 없거나 주소가 틀리면 debug 에서도 거절. release 는 두 칸 필수 · https · 허용 목록 그대로.
  5. 알림 [수락] 결과 알림을 누르면 같은 환경일 때 그 룸 상세(payload 에 environment 를 다시 실음).
  6. 로컬 http 접속의 iOS ATS 예외는 저장소 Info.plist 에 넣지 않음(release 완화 금지) — README 에 개발자 로컬 몫으로 적음.
  7. 시각 표시는 KST 고정(프로토 · DAY 기본 병원 시간대). 다른 시간대 병원은 서버 `hospital_zone` 값이 앱 JSON 에 없어 반영 못 함.
- 다름(원천 · 구현 사정): 마취 칩 툴팁(「마취 종료」 · 「마취 재시작」)은 길게 누르기 Tooltip · 탭 = 바로 그 동작(웹과 같은 흐름). 웹 인박스 칸별 정렬은 하지 않음(SPEC U-2 · OQ-A2 그대로).

## 이슈 · 코디가 확인할 것

1. **커밋 대상에 `app/ios/Podfile` · `Podfile.lock` 포함**(CocoaPods — 두 플러그인이 SPM 미지원). `app/build` · `Pods` · `.dart_tool` 는 .gitignore.
2. **Bundle ID = `com.example.day.placeholder`(임시 · 미등록)** · 표시 이름 `DAY` — `ios/Flutter/Identity.xcconfig` 기본값, 실제 값은 사용자가 `Identity.local.xcconfig`(커밋 안 함). Team · 서명 · Push capability · APNs 키 · TestFlight 는 사용자.
3. **앱 아이콘 비어 있음** — DAY 확정 자산 없음. App Store 제출 전 필수(README 후속).
4. backend 워커의 D-1 응답 모양(공개 주소 미설정 dev = environment 만)에 맞춘 개발 전용 대체를 넣었다. backend 가 최종적으로 `api_base_url` 을 dev 에서도 싣는지 PR 에서 맞춰 볼 것.
5. 통합 검증 전부 pending: dev 서버 · day-local 개발 빌드 연결 · 시뮬레이터/실기기 화면 · Keychain · APNs 도착 · 알림 [수락] 실행 · 통역 실서버(D-3) · prod 데모 넘김. 더블 PASS ≠ 실제 APNs · Soniox · prod 통합 완료.
6. RunnerTests(XCTest)는 시뮬레이터가 필요해 컴파일 · 실행하지 않았다(같은 로직은 swiftc 하네스로 39건 실행).
