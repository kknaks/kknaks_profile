# [mobile] app-fix-2 리포트 — review-code-2 AW1 ~ AW7

대상 = 워크트리 `day-app-re1` HEAD `fb08fe4e` 위(커밋 안 함). 고친 곳 = `app/`만. 같은 워크트리의 `backend/` 변경(`questionnaire_reads.py` · `day.js` · `test_public_questionnaire_guard.py`)은 backend 워커 몫이라 건드리지 않았다.

## 1. 처분표

| # | 처분 | 무엇을 바꿨나 | 자리(파일:줄) |
|---|---|---|---|
| AW1 | **고침** | 스캔 Activity 창에 `FLAG_SECURE` 를 늘 켠다. Flutter 스캔 · 확인 화면이 떠 있는 동안 MainActivity 창에도 켜고, 닫을 때 끈다(새 채널 메서드 `secure(bool)`). 효과 없던 `excludeFromRecents` 는 지우고 이유를 주석으로 남겼다. app-2 리포트 §4 표 72줄의 「최근 앱 목록 제외」는 취소선으로 바로잡았다. | `PassportScanActivity.kt:98` · `ScanChannel.kt:63-72` · `AndroidManifest.xml:49-55` · `scan_channel.dart:22,58-66` · `scan_screen.dart` initState / dispose(`port.secure(true/false)`) · `TextScanner.swift` `case "secure"`(하는 일 없음) |
| AW2 | **고침** | 카메라 시작 실패(`ProcessCameraProvider.get` · `bindToLifecycle` 예외)는 이제 `finishWith(null)`([닫기])로 가지 않는다. `ScanHub.fail("no_camera")` 를 거쳐 Dart `NoCamera` 가 되고, 「이 기기는 카메라를 쓸 수 없어요」 + [손으로 입력]으로 간다. 받은 요청은 닫히지 않는다(`closeDisplay` 안 부름). | `PassportScanActivity.kt:213,232,381-389` · `ScanChannel.kt:156-160` |
| AW3 | **고침(앱 몫)** | 성별 = 「남성」 · 「여성」 고르기(U-27 글자 · 값 MALE/FEMALE · 고른 것을 다시 누르면 비움). 날짜는 YYYY-MM-DD 이면서 실제 있는 날, 국적은 `[A-Z]{2}`, 여권번호는 `[A-Z0-9]{1,9}` 로 검사한다. 국적 · 여권번호는 입력할 때 대문자로 바뀐다. 형식이 틀린 칸은 빨강 칸으로만 표시하고 새 글자는 넣지 않았다. 보낼 칸이 없거나 틀린 칸이 있으면 [저장]이 꺼진다. 서버 400 `field = fields.<key>` 는 그 칸을 빨강으로 표시하고, 그 칸을 고치면 표시가 지워진다. 날짜 자리 글 `yyyy-MM-dd` 는 cc `scan_screen.dart:331` 원천 그대로다. 이름 칸은 원천 규칙이 없어 자유 글자로 두었다. | `scan_screen.dart:64-100`(`scanValueOk` · `scanFieldOf` · `_upper`) · `:248-252`(`_canSave`) · `:278`(400 field) · `:427-480`(칸 표시 · 자리 글 · 키보드) · `:520-543`(`_genderPick`) · `reservation_copy.dart` `scanDateHint` |
| AW4 | **고침** | cc 원천을 확인했다(`git show origin/main:procedure/app/lib/scan/mrz.dart` · 0553173). DAY 파일과 다른 곳은 머리 주석 한 줄뿐이었다. 원천은 `_docNumber` 가 바꾸는 자리 수를 제한하지 않아 최대 63가지를 시도하고, 종합 검사 숫자를 보지 않는다. → 한 번에 바꾸는 자리를 2 이하(`maxSwaps`)로 줄였다. 바꾸기로 맞춘 번호는 종합 검사 숫자(ICAO 9303 TD3 · l2[0..10]+[13..20]+[21..43] → l2[43])도 맞아야 받는다. 틀리면 「읽지 못함」이 되고 다음 프레임에서 다시 읽는다. 바꾸지 않은 번호는 cc 규칙 그대로(종합 검사 숫자 안 봄). 바꾼 번호는 `Mrz.numberCorrected` 로 확인 화면 여권번호 칸에 노란 ⚠ 아이콘을 보인다(글자 없음). 고치면 아이콘이 사라진다. **근거**: 검사 숫자는 한 자리라 바꾼 조합 가운데 우연히 맞을 확률이 조합마다 약 1/10이다. 조합을 줄이고 두 번째 독립 검사 숫자를 걸면 잘못 받을 확률이 대략 1/100 아래로 내려간다. | `mrz.dart:1,16,25,85-106,150-157,176` |
| AW5 | **고침** | 받은 스캔의 상세 읽기 실패를 둘로 나눴다. 응답 없음(네트워크 · 시간 초과)이면 `inbox.release(id)` 로 「연 것」 표시를 푼다. 서버 메우기는 `opened` 도 돌려주므로(`displays.pending` · `rules.OPEN`) 다음 메우기(앱이 앞으로 옴 · 스트림이 다시 붙음 · `display` 신호) 때 다시 연다. 서버가 답한 실패(404 · 403 등 다시 열어도 같은 것)이면 `close canceled` 를 보낸다(cc [닫기]와 같은 값). 그 close 도 실패하면 release 한다. 토스트는 지금 그대로다. | `display_flows.dart:256,262-279` · `display_inbox.dart:79-84` |
| AW6 | **고침** | 간격 · 판독 중 검사(`FrameGate.shouldRead`)를 `toBitmap` 앞으로 옮겼다. 앞으로는 비트맵이 많아야 10장/초, 판독 중에는 0장이다. 마지막 프레임은 `LatestSlot` 하나에 두어, 새 것을 넣으면 앞 것을 바로 `recycle()` 한다. 자르기([촬영] · 자동 촬영 · MRZ 자리)는 잠금 안에서 해서, 쓰는 중인 그림을 놓지 않는다. 닫을 때 `close()` 로 남은 것도 놓는다. 회전 때 하나 더 만드는 것(원본은 바로 recycle)은 그대로 두었다. | `ScanFrames.kt`(새 파일) · `PassportScanActivity.kt:91,118,284-301,311-317,336,375` |
| AW7 | **기록만** | 아래 §3 목록. 코드는 바꾸지 않았다. | — |

## 2. 검증(각 1회 · 마지막 통합)

| 명령 | 결과 |
|---|---|
| `fvm flutter analyze` | No issues found |
| `fvm flutter test` | **All tests passed — +527 ~81**(건너뜀 81 = 기존 capture 시험) |
| `fvm flutter build apk --debug` | ✓ Built `build/app/outputs/flutter-apk/app-debug.apk` |
| `fvm flutter build ios --no-codesign` | ✓ Built `build/ios/iphoneos/Runner.app`(21.3MB) |
| Kotlin `./gradlew :app:testDebugUnitTest`(JAVA_HOME = Flutter jdk-dir `openjdk@17`) | PushLogicTest 9/9 · **ScanFramesTest 3/3**(새) · 실패 0 |

새 시험:
- `test/scan/mrz_fix_test.dart` 4개 — 바꾸지 않은 번호는 종합 검사 숫자가 틀려도 받음(cc 그대로) · 한 자리 바꿈 + 종합 검사 숫자 맞음 = 받고 고친 표시 · 바꿈 + 종합 검사 숫자 틀림 = null · 세 자리 바꿔야 맞는 번호 = null
- `test/ui/scan_fix_test.dart` 6개 — 칸 형식 단위 · 400 field 대응 · 손 입력 흐름(빈 칸이면 [저장] 꺼짐 · 성별 고르기 · 틀린 날짜 칸 빨강 · 대문자 · 400 `fields.nationality` 칸 빨강 → 고치면 지움 · 보낸 값 · `secure` [true, false]) · MRZ 고친 번호 ⚠ · AW5 응답 없음 → 다시 엶(close 0건) · AW5 404 → close canceled 1건 · 다시 안 엶
- `android/app/src/test/kotlin/day/medisolveai/ScanFramesTest.kt` 3개 — 게이트 · 슬롯 놓기 · use 동안 다른 스레드 put 기다림
- 기존 `FakeScanPort` 에 `secure` 기록을 더했다(`test/support/resv_fixtures.dart`).

## 3. AW7 — 출시 전 목록(사용자 · 코디 몫)

- 오픈소스 고지(Apache-2.0): CameraX 1.4.2 · androidx.activity 1.10.1 · ZXing core 3.5.3(`app/android/app/build.gradle.kts`)
- `com.google.mlkit:text-recognition:16.0.1` = ML Kit 약관(오픈소스 아님). 판독은 번들 모델이라 기기 안에서 한다. 사용 · 성능 지표 전송은 Google 공개 내용이며 Google 문서와 대조하지 않았다 → Play 데이터 보안 양식 · 개인정보 안내(OQ-A89)
- backend `segno` = PASS(리뷰 그대로)

## 4. 사실대로 — 실제 효과 · 남는 것

- **AW1 효과(Android)**: `FLAG_SECURE` 창은 스크린샷 · 화면 녹화 · 캐스트에서 검게 나오고, 최근 앱 썸네일도 비어 나온다. 스캔 Activity와 Flutter 스캔 · 확인 화면(여권 값 7칸 · 썸네일)이 모두 덮인다. 확인 화면이 닫히면 앱 창 secure 는 꺼진다(다른 화면 캡처는 그대로 됨). **기기 실행은 하지 않았다**(브리프 금지) — 썸네일이 실제로 비는지는 갤럭시 실물로 볼 것.
- **iOS 에는 같은 효과가 없다**: 앱이 스크린샷이나 앱 전환 썸네일을 막는 공개 API 가 없다. `secure` 채널은 iOS 에서 아무 일도 하지 않는다(`TextScanner.swift`). 앱 전환 썸네일을 가리려면(예: 비활성 때 덮개 뷰) 새 동작이라 이번 범위 밖에 두었다 → 필요하면 SPEC 결정.
- AW2: 권한 거부 · 카메라 없음과 같은 「이 기기는 카메라를 쓸 수 없어요」 화면으로 간다. 「다른 앱이 쓰는 중」 같은 따로 된 글자는 원천에 없어 짓지 않았다.
- AW3: **서버 쪽 국적 · 여권번호 형식 검사는 backend 몫**이다(이번 be-fix-2 범위인지 코디 확인 필요 — be-fix-2 지시서에는 AW3 서버 몫이 적혀 있지 않다). 앱은 400 `field` 가 `fields.<7칸 키>` 꼴이면 어느 칸이든 표시한다.
- AW4: 종합 검사 숫자는 옵션 칸 판독에 흔들린다. 그래서 **바꾸기가 필요한 여권(번호에 0/O · 1/I 등이 섞인)은 자동 확정이 전보다 늦거나 안 될 수 있다** → 그때는 [촬영] 또는 3번 실패 → [손으로 입력]으로 간다. 판독률 변화는 실물로 볼 것(A-69).
- AW6: 자동 촬영 · [촬영]에 쓰는 프레임은 이제 마지막으로 판독한 프레임(≤ 100 ms 간격 · 판독 중에는 그대로)이다. 전에는 「가장 최근 프레임」이었다. 손이 빨리 움직이면 [촬영] 사진이 판독 시간(수백 ms)만큼 앞의 것일 수 있다.
- 화면 글자는 새로 짓지 않았다. 새 상수는 `scanDateHint = 'yyyy-MM-dd'`(cc 원천) 하나다. 성별 버튼 글자는 기존 `resMale` · `resFemale`(「남성」 · 「여성」 · U-27)을 썼다.

## 5. 바꾼 파일

app/android/app/src/main/AndroidManifest.xml · app/android/app/src/main/kotlin/day/medisolveai/{PassportScanActivity.kt, ScanChannel.kt, ScanFrames.kt(새)} · app/android/app/src/test/kotlin/day/medisolveai/ScanFramesTest.kt(새) · app/ios/Runner/TextScanner.swift · app/lib/core/reservation_copy.dart · app/lib/scan/{mrz.dart, scan_channel.dart} · app/lib/state/display_inbox.dart · app/lib/ui/{display_flows.dart, scan_screen.dart} · app/test/support/resv_fixtures.dart · app/test/scan/mrz_fix_test.dart(새) · app/test/ui/scan_fix_test.dart(새) · (orchestration) app-2-report.md 72줄 정정
