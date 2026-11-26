# WORK-002 app-2 결과 보고 — 앱 예약현황 · 문진 QR · 여권 스캔 · 태블릿에 보내기 · 받기 · 기기 이름 (Delivery CENTURION_DAY#288)

## 상태: done (코드 · 단위 / 위젯 시험 · iOS · Android 빌드 통과 — 실물 A4 는 코디 몫)

- 워크트리 `/Users/kknaks/orca/workspaces/CENTURION_DAY/day-app-re1` · HEAD `96036397` 위에 변경만(커밋 · push 없음) · `app/` 만 고침.
- iOS 카메라 문구(Info.plist) 손대지 않음(D15 그대로 · OQ-A79 열림).
- 새 Flutter 패키지 0. Android gradle 의존성만 추가(아래 「네이티브 채널」).

## 1. 검증 — 명령과 결과

| 명령 | 결과 |
|---|---|
| `fvm flutter analyze` | **No issues found** |
| `fvm flutter test` | **517 통과 · 81 건너뜀(기존 capture 시험의 skip) · 실패 0** (변경 전 기준 455 + 29 실패 → 29 실패는 이번 변경이 만든 것 = 메우기 요청 · 메뉴 수 — 아래 「기존 시험 고침」으로 해소) |
| `fvm flutter build ios --no-codesign` | **✓ Built build/ios/iphoneos/Runner.app (21.3MB)** — 첫 시도는 cc 코드의 `minimumFocusDistance`(iOS 15+) 때문에 실패 → `#available(iOS 15.0, *)` 로 가둠 → 통과 |
| `fvm flutter build apk --debug` | **✓ Built build/app/outputs/flutter-apk/app-debug.apk** (CameraX · ML Kit · ZXing 포함 · 1회 통과 — 그 뒤 Dart 파서 · 상세 동행 글자만 고침(backend 초안 꼴 맞춤) · analyze · test · build ios 는 그 뒤 다시 통과) |
| 덤: `app/tool/native_logic_test.sh`(iOS 네이티브 판단 · macOS swiftc) | ALL PASS(새 display 4건 포함) |
| 덤: `./gradlew :app:testDebugUnitTest`(Kotlin JVM · JAVA_HOME = Flutter jdk-dir) | PushLogicTest 9/9 통과(새 display 1건 포함) |

새 시험(테스트 더블 · 서버 · 시뮬레이터 없음):
- `test/scan/mrz_test.dart` — cc `test/mrz_test.dart` 그대로 옮김(패키지 이름만).
- `test/model/reservation_model_test.dart` 8 — W1 · W2(snake / camel / backend 초안 꼴) · 폰 목록 순서 · 진행 줄 글자 · 보낼 칸(N2) · W4 · W6 응답.
- `test/state/reservation_state_test.dart` 10 — 스트림 켜고 끄기 · 꺾쇠 연타 마지막만 · 신호 합침 · `display` 방문 신호 · 403 / 401 · watch · DisplayInbox(큐 · 이미 연 것 · qrUrl 없는 문진 건너뜀 · 화면 수) · 띄우기 푸시 갈래(환경 · 병원 · 세션 전 누름) · 기기 이름(등록 전 / 뒤 · 빈 값 · 실패) · ReservationApi 경로 · 본문 · multipart.
- `test/ui/reservation_ui_test.dart` 15 — A-62 폰 · 태블릿 · A-63 폰 · 태블릿 · A-64 · A-73 · A-68 · A-70 · 3번 실패 · A-71 · A-72/A-74 · 받은 스캔 원격 닫힘 · A-75 · A-76 ×2.
- 기존 시험 고침(SPEC 개정 ㉒ 때문): `app_flow_test` 메뉴 3 → 4(A-61) · `notification_ui_test` 「이 기기」 없음 → 있음(U-30). 시험 지원: `fixtures.dart`(예약 전송을 판 기록과 분리 · multipart 사진 바이트 받기) · `ui_harness.dart`(`resv` 가짜 서버 · 예약 SSE · 메우기 기본 빈 목록).

## 2. 수행 — 파일

새 파일
| 파일 | 내용 |
|---|---|
| `lib/scan/mrz.dart` | cc `lib/scan/mrz.dart` 그대로(출처 줄 한 줄 더함) |
| `lib/scan/scan_channel.dart` | 채널 `day/scan`(cc `scan_channel.dart` — 이름만 바꿈) + 시험용 `ScanPort` |
| `lib/model/reservation.dart` | W1 ~ W6 · W8 값(snake / camel 둘 다 읽음 — 「계약에서 애매했던 곳」 1) |
| `lib/data/reservation_api.dart` | 계약 경로 11개(W1 · W2 · W3 · W4 ①~④ · W6 · kos-retry · W8) |
| `lib/state/reservation_controller.dart` | 예약현황 값 · `/api/reservations/stream`(`reservation` · `display`) · 방문 신호 · 필터 |
| `lib/state/display_inbox.dart` | 받기 큐(cc app_state 102-150) · 떠 있는 띄우기 화면 수 |
| `lib/core/reservation_copy.dart` | 화면 글자 — 줄마다 출처(웹 템플릿 · SPEC · cc) |
| `lib/ui/reservation_screen.dart` | 예약현황 탭(머리 · 달력 · 필터 · 폰 목록 / 태블릿 표) |
| `lib/ui/reservation_table.dart` | 카드 · 태블릿 시간 × 열 표(웹 day.js 자리 계산 그대로) |
| `lib/ui/reservation_detail.dart` | 상세(읽기 전용 · 폰 = 한 열 · 태블릿 = 가운데 창 · 웹 칸 배치) |
| `lib/ui/display_flows.dart` | 버튼 셋 · 진행 줄 · [문진 QR] · [태블릿에 보내기] 고르기 · 받은 것 열기 |
| `lib/ui/qr_screen.dart` | 문진 QR 전체 화면(cc `qr_show_screen.dart` 꼴) |
| `lib/ui/scan_screen.dart` | 여권 스캔 · 확인 · 저장 · 결과(cc `scan_screen.dart` 꼴) |
| `lib/ui/settings_device.dart` | 설정 「이 기기」 · 「이 기기 이름」 창 |
| `ios/Runner/TextScanner.swift` | cc `TextScanner.swift` — 채널 이름 · iOS 13 가드(UIButton.Configuration · 매크로 전환 · minimumFocusDistance = iOS 15+)만 바꿈 |
| `android/…/ScanChannel.kt` · `PassportScanActivity.kt` | Android 새로(CameraX + ML Kit 번들 Latin · ZXing QR · FLAG_KEEP_SCREEN_ON) |

고친 파일: `lib/app.dart`(세션마다 예약 상태 · 받기 · 전송 분리 · 앞으로 올 때 메우기) · `lib/ui/shell.dart`(메뉴 4 · 예약현황 본문 · 받기 펌프 · 채팅 배너 막음 · 설정 「이 기기」) · `lib/ui/theme.dart`(상담 색 2) · `lib/data/day_api.dart`(`putJson`) · `lib/data/event_stream.dart`(JSON 아닌 본문 `{value}`) · `lib/data/push_bridge.dart`(`deviceName` · `setDeviceName`) · `lib/state/push_coordinator.dart`(kind `display` · 등록 상태 · 기기 이름) · `lib/notify/notification_controller.dart`(알림 스트림 `display` → 메우기 신호) · iOS `AppDelegate.swift` · `AcceptLogic.swift` · `project.pbxproj`(TextScanner.swift 등록) · `NativeLogicTests/main.swift` · Android `PushLogic.kt` · `PushHub.kt` · `DayMessagingService.kt` · `PushChannel.kt` · `MainActivity.kt` · `AndroidManifest.xml` · `build.gradle.kts` · `PushLogicTest.kt`.

## 3. 화면 흐름

1. **셸** — 하단 · 레일 4개 「예약현황 · 시술현황 · 채팅 · 설정」 · 첫 메뉴 = 시술현황(A-61). `reservation` view 없음 = 예약현황 본문 자리에 권한 없음 안내 + [로그아웃](시술현황과 같은 부품 · A-76) · 서버 403 도 같은 글자.
2. **예약현황**(U-24) — 머리 `YYYY-MM-DD (요)` · ‹ › · [오늘](오늘이면 꺼짐) · 날짜 누름 = 달력(웹 글자 「{y}년 {m}월」 · 일~토 · Material 영어 달력 안 씀) · [필터](「전체 n」 + 7줄 · 고르면 다른 카드 흐림). 폰 = `HH:MM` 행 머리 아래 카드(열 순서 → 줄 → 자리) + 카드에 열 이름 · 태블릿 = 열 머리 「{정원}명 / {간격}분」 · 시간 칸(회색 구간 글자 흐림) · 회색 면 · 동행 띠 · 현재 시각 선(오늘) · 처음 세로 = 오늘이면 현재 시각 1/3 · 아니면 운영 시작 줄. 스트림 `reservation` → 그 날짜 `poll=1`(받는 중이면 끝나고 한 번). 쓰기 입구 0.
3. **상세**(U-25) — 세션 Navigator · 머리(단계 이름 · 웹 색 · ✕) → 고객(이름 · 초진/재진 · 버튼 셋 · 진행 줄 · 성명(여권) · 연락처 · 생년월일/성별 · 국적/통역 · 신분확인 · 초진 문진 · 건강정보 · 특이사항) → 예약 정보 → 시술 목록(상품명 · 오늘 ✓ · 상태) → 오더 메모(값 있을 때) → 귀가 사유 → 수납 정보 · 재진 = 이전 방문. 열린 동안 그 방문 `display` · 모든 `reservation` 신호 → 값만 다시. 닫기 = ✕ · 뒤로 · 끌어 내림(폰) · 바깥 누름(태블릿).
4. **[문진 QR]**(U-26) → 요청 `{kind: questionnaire}` → QR 전체 화면(흰 바탕 · [닫기] · 안내 두 줄 · 네이티브 QR · 남은 시간 · keepAwake) → 신호로 상세 다시 읽어 pending 아니면 한 줄 뒤 1.5초 닫힘. 스트림이 끊긴 동안만 5초 폴링(OQ-A84).
5. **[여권 스캔]**(U-27) → 네이티브 스캔 → 확인(이 화면을 열 때만 `GET …/passport` · 다른 칸 노랑) → 저장(바뀐 칸만 · 못 읽었으면 비지 않은 7칸) → 「저장했어요」 · KOS 사진 실패면 [사진 다시 올리기]. 카메라 없음 / 거부 / 3번 실패 → [손으로 입력]. 원본 = 메모리만.
6. **[태블릿에 보내기]**(U-28) → 종류(보이는 버튼 둘이면 고름 · 하나면 그것) → 기기 목록(폰 시트 · 태블릿 창) → 요청 `{kind, deviceId}` → 토스트 「{기기}에 표시 중」 → 진행 줄은 신호로.
7. **받기**(U-29) — 알림 스트림 `display` · 다시 붙음 · 로그인 · 앞으로 옴 · 띄우기 푸시(누름 / 앞) → `GET …/pending` → 큐 → 하나씩 세션 Navigator 맨 위(문진 = 받은 qrUrl QR · 스캔 = 상세 읽고 스캔 화면 + `displayRequestId`) · 이미 연 id 다시 안 엶 · 띄우기 화면 동안 채팅 배너 없음 · 받은 스캔 [닫기] / 뒤로 = `close canceled` · 그 방문 신호로 요청이 닫힌 걸 보면 스캔 화면 닫음.
8. **설정 「이 기기」**(U-30) — 「기기 이름」 + 값 + › → 「이 기기 이름」 창(자리 글 · [취소] · [저장] · 40자) → 등록 뒤 = `PUT …/name` · 등록 전 = 이 기기에 두고 등록 직후 보냄 · 빈 값 = 안 함 · 등록 전이면 아래 줄 「알림을 켜면 웹 기기 목록에 보여요」. 자리 = 「알림」 칸 아래 · [로그아웃] 위(「정보」 위).

## 4. 네이티브 채널 표

| 항목 | iOS | Android |
|---|---|---|
| 채널 | `day/scan`(TextScanner.swift · AppDelegate 등록 `DayScan`) | `day/scan`(ScanChannel.kt · MainActivity 등록) |
| `scanPassport{windows, windowSec, debug}` | cc 그대로 — AVCaptureSession 1080p · 자동 매크로 가상 기기 · 틀 영역 잘라 Vision `.accurate` · Dart `checkMrz` · confirmed 자동 촬영 · [촬영] · [손으로 입력] · [닫기] = nil | PassportScanActivity — CameraX Preview + ImageAnalysis(최신 프레임만 · RGBA · 16:9 · 1080p 근처) · 틀 ↔ 영상 좌표 = PreviewView FILL_CENTER 계산 · ML Kit `text-recognition:16.0.1`(번들 Latin · 오프라인) · 같은 상태 글자 · 같은 반환 모양 · 뒤로 = [닫기] |
| 반환 | `{photo: JPEG(≤2000px · 0.8), lines}` · `+shutter` · `{failed: true}` · nil | 같음(ByteArray → Uint8List) |
| 오류 | `no_camera`(카메라 없음 · 권한 꺼짐) | `no_camera`(FEATURE_CAMERA_ANY 없음 · 권한 거부) · 처음이면 실행 중 권한 요청 |
| `qrImage{text, size}` | CoreImage `CIQRCodeGenerator` M | ZXing core 3.5.3 `QRCodeWriter` M · 칸 정수 배 · PNG |
| `keepAwake(bool)` | `isIdleTimerDisabled` | 창 `FLAG_KEEP_SCREEN_ON` |
| 원본 | 메모리만(디스크 · 사진첩 · 로그 0) | 메모리만(Bitmap · 바이트 · 파일 0 · ~~최근 앱 목록 제외~~ — 고침 app-fix-2: `excludeFromRecents` 는 task root 가 아니라 효과 없었음 · 이제 창 FLAG_SECURE 로 캡처 · 최근 앱 썸네일 막음) |
| 권한 선언 | Info.plist 지금 D15 문구 그대로 | `CAMERA` + `uses-feature camera.any required=false` |
| 푸시 `display` | `tapKeys` + `requestId` · 앞 + Dart 준비 = 배너 없이 `onForeground` · 뒤 = OS 알림(서버 `aps.alert`) | `known` · 채널 「고객 입력 요청」(id `display` · 소리 · 진동 없음 · DEFAULT) · tag `display:{requestId}` · 앞 = 알림 없이 Dart · 누름 칸 + `requestId` |
| `day/push` 추가 | `deviceName` · `setDeviceName`(UserDefaults `day.device.name`) | 같음(SharedPreferences `day.device`) |
| 의존성(Android) | — | `androidx.activity:activity:1.10.1` · `androidx.camera:camera-camera2/lifecycle/view:1.4.2` · `com.google.mlkit:text-recognition:16.0.1` · `com.google.zxing:core:3.5.3`(라이선스: Apache-2.0 · ML Kit = ML Kit 약관) |

## 5. 계약 대조 · 애매했던 곳(코디 · backend 확인 필요)

1. **W1 · W2 칸 꼴** — 계약은 「웹과 같은 service 값」이라 처음엔 dict(snake)로 짓고 snake / camel 둘 다 읽게 했다. 작업 중 backend 초안(`backend/day/schemas/reservation_detail.py`)을 읽기만 해 보니 **camel** 이라 그 꼴(`sendStatus` · `time` · `health` 따로 · `doctor` 글자 · `previousVisits` …)도 시험에 넣었다. W1(목록)의 backend 칸은 아직 못 봄 — snake / camel 어느 쪽이든 읽는다.
2. **동행 누름(A-63 「동행 이름 누름 = 그 상세」)** — backend 초안은 `reservation.companions` 를 **이름 글자 목록**으로 줄여 방문 id 가 없다 → 앱은 그 이름을 **누를 수 없게** 그린다. `{visitId, name}` 으로 실어 주면 바로 그 상세로 바뀐다(앱 코드 준비됨 · 시험 있음). **backend 에 알려야 함.**
3. **초진 문진 KOS 상태 칸 이름** — 계약 글엔 이름이 없어 `kosStatus` 로 짓다가 backend 초안 `sendStatus` 를 보고 둘 다 읽게 함. `sending`(보내는 중) 글자는 OQ-D33 — 비움.
4. **예약 스트림 본문** — 계약 「`reservation` 본문 = version · `display` 본문 = 방문 id」 → JSON 아닌 글자 본문을 `{value}` 로 받음(`{visitId}` JSON 이어도 읽음).
5. **W8 등록 때 이름** — 계약은 「등록(`PUT /api/devices/{id}`) 때 이름 실음(칸 이름 BE)」. 지금 서버 등록은 모르는 칸을 400 으로 막아 푸시까지 끊길 수 있어, 앱은 **등록 본문을 그대로 두고 등록 성공 직후 `PUT …/name`** 으로 보낸다(같은 결과). backend 초안은 등록 본문 `name` 도 받게 했다 — 둘 다 맞는다.
6. **iOS 띄우기 푸시 본문** — W5 는 Android data 칸(`kind · requestId · environment · hospitalId`)만 적었다. iOS 도 APNs 본문에 같은 커스텀 칸이 있어야 누름 → 메우기가 된다(없으면 Dart 가 환경 · 병원 불일치로 무시). **backend 확인.**
7. **메우기의 문진 요청** — `pending` 은 상태를 안 싣는다. qrUrl 이 없는 문진은 열지 않는다(cc: 고객 폰이 이미 연 문진은 QR 이 필요 없음).
8. **「국적/통역」** — DAY-SPEC-007 U-3 은 「통역필요」 안 보임(OQ-D06 닫음)인데 **웹 템플릿은 `{국적} / 통역필요`** 를 그린다. 브리프 「글자 = 웹」대로 템플릿을 따랐다. 어느 쪽이 맞는지 코디 결정.
9. **진행 줄 — 이 기기 문진 QR(기기 없음) pending** = 줄 없음(웹 「고객 휴대폰 카메라로 찍어 주세요 · 남은 시간」은 웹 화면 안 QR 칸 글자라 앱 상세엔 안 둠).
10. **오류 코드 글자** — `visit_not_today` · `visit_stage_changed` · `reservation_past_date` · `kos_unavailable` · `photo_disabled` 등은 앱 글자 표(actionMessages)에 없어 **코드만** 보인다(기존 규칙 OQ-A7). 글자가 정해지면 넣을 자리 = `lib/core/copy.dart`.

## 6. 글자 원천이 없어 비운 자리(짓지 않음)

- 태블릿에 보내기 **종류 고르기** 시트 머리 · **스캔 부제**(OQ-A83) — 머리 없이 「문진 QR」 · 「여권 스캔」 두 줄만 · 기기 창 머리 = 「태블릿에 보내기」.
- 스캔 결과 **DAY 사진 줄 · KOS 사진 줄**(OQ-A85) — 안 그림(실패면 [사진 다시 올리기] 버튼만).
- 확인 칸 자리 글 — 「예: KR」(SPEC)만. cc 의 「MALE / FEMALE」 · 「yyyy-MM-dd」 자리 글은 SPEC U-27 목록에 없어 비움.
- 예약현황 **오른쪽 패널**(공지 · 원내 현황 보기만 — OQ-A80) — 이번 판에 안 둠.
- 상태 툴팁(웹 마우스 0.3초) — 터치에 없음(OQ-A81).

## 7. 코디가 시뮬레이터 · 에뮬레이터에서 볼 순서(A4)

1. iPad 시뮬레이터 · `reservation` view + `reservation.detail` edit 계정 → 하단 레일 4개 · 첫 화면 시술현황.
2. 예약현황 → 표(열 머리 · 회색 · 현재 시각 선 · 카드 띠 색이 웹과 같은지) → 날짜 ‹ › · [오늘] · 달력 · [필터].
3. 웹에서 접수 → 앱 표가 신호로 바뀜(A-62).
4. 카드 → 상세 → 웹 모달과 칸 · 글자 · 색 비교 · 쓰기 버튼 0(A-63) → 웹에서 바꾸면 열린 상세가 바뀜.
5. [문진 QR] → QR 화면 → 고객 폰으로 찍기 → 「고객 폰에서 열렸어요」 뒤 닫힘(A-64).
6. 시뮬레이터 [여권 스캔] = 카메라 없음 → 「이 기기는 카메라를 쓸 수 없어요」 → [손으로 입력] → 저장 → 웹 신분확인 「O」(A-70 · A-77).
7. 두 번째 기기(태블릿 · 코디 계정 · 알림 켬) 설정 「이 기기 이름」 저장 → 첫 기기 [태블릿에 보내기] 목록 이름(A-75 · A-71) → 보내면 태블릿에 바로 뜸 · 앱을 뒤로 보낸 뒤 보내면 알림 → 누르면 뜸(A-72) · 웹 [취소] → 태블릿 스캔 화면 닫힘(A-74).
8. Android 에뮬레이터 — 빌드 · 로그인 · 예약현황 · 상세 · [여권 스캔] 권한 창(거부 = 손 입력) · 에뮬레이터 카메라 화면이 뜨는지 · QR 이 그려지는지. **갤럭시 탭 실물 판독률 · 근접 초점 · CAMERA 선언 뒤 차트 「사진 찍기」 · 채팅 카메라(OQ-A91 · A-69)는 사용자 E2E.**

## 8. 사람 눈에 이상해 보일 자리

- 태블릿 표: 왼쪽 시간 칸이 가로로 밀면 같이 밀린다(고정 안 함) · 열 머리는 세로로 고정. 카드 글자는 웹 고정 크기(140 × 66)라 아이패드 글자 배율을 안 받는다 — 시술현황 글자보다 작아 보일 수 있다.
- 폰 상세 끌어 내림은 머리 띠를 잡고 내릴 때만(본문 스크롤과 겹치지 않게).
- 상세 태블릿 창 = 최대 1080 × 760(OQ-A82 기본값) · 이전 방문 칸 접기 버튼은 상세를 다시 열면 펼친 상태.
- 달력은 Material 달력이 아닌 웹 꼴 간단한 창 — 오늘 동그라미 테두리 · 고른 날 파란 원.
- 받은 띄우기 화면은 미저장 차트 위에도 뜬다(OQ-A87 기본값).
- Android 스캔 화면은 iOS 와 같은 글자 · 배치지만 시스템 버튼 모양이라 [닫기] · [손으로 입력] 모양이 조금 다르다.
- ML Kit 사용 지표 전송을 개인정보 안내에 넣을지(OQ-A89) — 안 다룸.
