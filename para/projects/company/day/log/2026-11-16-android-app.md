
# 작업 요약 — android-app (day)

기간: `2026-11-12` ~ `2026-11-16`
결과: 코드 머지(CENTURION_DAY#253 → dev `4f8316a7`) · Play 배포 — DAY Dev 내부 테스트 vc3 · 정식 DAY 비공개 테스트 vc3 출시 · **프로덕션 vc3 심사 중**(2026-11-15 제출)

## 1. 무엇을 했나

DAY 직원 앱은 iOS 로만 지어 와서 `app/android/` 가 없었다. 인수인계의 범위는 「개발 앱을 로컬 에뮬레이터에서 띄우기」였지만, 사용자가 회사 Play Console 권한을 받으면서 범위가 넓어졌다. 개발 앱(`day.medisolveai.dev`)을 Play 내부 테스트에 올렸고, 정식 앱(`day.medisolveai` · prod)은 비공개 테스트를 거쳐 프로덕션 심사까지 냈다.
코드로는 Android 네이티브 채널 세 개(session = Keystore 구현 · push/video = 스텁)를 만들고, 업로드 키 서명과 Play Developer API 업로드 스크립트를 붙였다. 실기기(Galaxy Z Fold3)에서 나온 하단 시스템 바 가림(F1)도 Dart 로 고쳤는데, iOS 화면은 픽셀 단위로 그대로 두었다.
스펙(mediness#940)은 코드보다 먼저 닫았고, 사실이 바뀐 부분은 마감 때 다시 맞췄다(마감 spec-sync PR).

## 2. 적용한 기술·개념

- **Android Keystore 로 세션 묶음 암호화(AES-256-GCM) + 단일 직렬 실행기** — iOS Keychain `ThisDeviceOnly` 자리를 Android 에 만든 것
  - 개념: [[para/areas/concept/infra/secret-store|secret-store]]
  - 왜 이걸 골랐나: Jetpack `EncryptedSharedPreferences`(security-crypto)는 deprecated 다. 플랫폼 API 로 쓰면 80줄 안팎이라 iOS 구현과 줄 단위로 대조할 수 있다. 백업 · 기기 이전도 제외해서 세션이 다른 폰으로 따라가지 않게 했다.
  - 무엇이 어려웠나: Dart 의 `clearIf`(토큰 · 주소가 같을 때만 지움)는 읽기 · 비교 · 삭제 사이에 `save` 가 끼면 새 로그인을 지운다. iOS 는 `DispatchQueue.sync` 로 막고 있었고, Android 는 단일 스레드 실행기로 같은 자리를 만들었다. 실행 중 예외가 나도 답을 꼭 돌려줘야 Dart 의 로그아웃 · 401 처리가 멈추지 않는다는 것도 리뷰(W-4)에서 잡았다.
  - 근거: `app/android/.../SessionChannel.kt` · `review-code-1-report.md` · `e13ea876`

- **빌드 값 3단 주입(id · 이름 · 서명) — 키가 없으면 release 빌드가 멈춘다**
  - 개념: [[para/areas/concept/infra/build-flavor|build-flavor]] · [[para/areas/concept/infra/code-signing|code-signing]]
  - 왜 이걸 골랐나: iOS `Identity.xcconfig` 처럼 저장소에 실제 id 를 두지 않으려고 `-P` > `identity.local.properties` > placeholder 순서로 읽게 했다. flavor 를 만들지 않은 건 정식 id 가 당시 미결이었기 때문이다. 템플릿 그대로면 release 가 **debug 키로 조용히 서명된다** — Play 가 거절하긴 하지만, 실수로 나간 빌드를 사람이 알아채기 어렵다. 그래서 키가 없으면 `preReleaseBuild` 에서 오류로 멈추게 했다.
  - 근거: `app/android/app/build.gradle.kts` · `app-3-report.md` · `fa2f0d9f`

- **Play 앱 서명 + 업로드 키 · 첫 AAB 는 손으로, 그 뒤 Developer API** — 배포 경로 설계
  - 개념: [[para/areas/concept/infra/code-signing|code-signing]] · [[para/areas/concept/infra/workload-identity|workload-identity]]
  - 왜 이걸 골랐나: 앱 서명 키는 Google 이 보관하고 우리는 업로드 키만 로컬에 둔다. 업로드 키를 잃어도 재발급할 수 있다. Play Developer API 는 앱을 만들지 못하고 첫 업로드도 하지 못해서, 앱 생성 · 첫 AAB · 콘텐츠 선언은 사용자 손 단계로 나눴다.
  - 무엇이 어려웠나: 서비스 계정 키 생성이 조직 정책 `iam.disableServiceAccountKeyCreation` 에 막혔다. 조직 관리자 계정에 「조직 정책 관리자」가 이미 있다는 걸 조직 단위 IAM 화면에서 확인하고, Play 업로드용 Cloud 프로젝트 하나만 「상위 정책 재정의 → 사용 안 함」으로 열었다. 반영까지 몇 분 걸려 첫 시도는 또 막혔다. 키를 받은 뒤에는 정책을 되돌렸다 — 이미 발급한 키는 계속 쓸 수 있다.
  - 근거: `_RESUME.md` §5 2026-11-14 · `~/.config/day/android/`(값은 저장소 밖)

- **edge-to-edge(targetSdk 36) 아래 하단 inset — Flutter 의 「padding 을 직접 주면 안전 영역을 안 더한다」** — F1
  - 개념: [[para/areas/concept/front/system-bar-inset|system-bar-inset]]
  - 무엇이 어려웠나: 에뮬레이터 제스처 내비에서는 보이지 않았다. Fold 펼침(태블릿 폭 → 레일 셸) · 3버튼 내비 · 삼성 태스크바에서만 나왔다. 원인은 두 갈래였다. ① 태블릿 채팅 칸이 iPad 에 맞춰 아래 여백을 0 으로 두었다(iPad 홈 인디케이터는 겹쳐 그려도 되는 자리다). ② `ListView(padding: …)` 처럼 padding 을 직접 준 목록은 `BoxScrollView` 가 MediaQuery 안전 영역을 자동으로 더하지 않는다. 처음 판은 ①만 고쳤는데, 리뷰가 워커 스크린샷 09 에서 마지막 카드가 잘린 걸 찾아냈다(워커는 ✓ 로 적었다). 두 번째 판에서 스크롤 목록 25자리를 전수 grep 했고, 리뷰 표 밖에서 차트 시트까지 찾았다.
  - 왜 이걸 골랐나: iOS 를 다시 제출하지 않으려고 `defaultTargetPlatform == android` 분기를 한 곳(`paneReservesBottomInset` · `listEndInset`)에만 두었다. 몰입 모드로 시스템 바를 숨기는 방법은 사용자가 원하지 않았다. iPhone · iPad 는 전후 스크린샷이 픽셀 단위로 같았다.
  - 시험: `debugDefaultTargetPlatformOverride` 를 `addTearDown` 으로 되돌리면 프레임워크의 debug 변수 검사가 tearDown 보다 먼저 돌아 실패한다. `TargetPlatformVariant` 로 바꿔 두 플랫폼을 한 테스트로 돌렸다. `listEndInset → 0` 변이로 테스트가 실제로 잡는지도 확인했다.
  - 근거: `app/lib/ui/theme.dart` · `test/ui/pane_bottom_inset_test.dart` · `review-code-3/4-report.md` · `099fe786`

- **Play Developer API edits 흐름 + 짝 고정(`play_upload.py`)** — AND-7
  - 개념: [[para/areas/concept/infra/artifact-promotion|artifact-promotion]]
  - 왜 이걸 골랐나: `edits.insert → bundles.upload → tracks.update → commit` 을 하나로 묶고, 실패하면 edit 을 지운다. dry-run 은 commit 대신 `edits.validate` 를 부른다. 정식 앱에 실수로 올리는 걸 막으려고 패키지와 트랙 짝을 표로 고정했다(`dev → internal` · `정식 → alpha`). **프로덕션은 스크립트로 못 올린다.** 의도한 것이고, 공개 출시는 Console 손 단계로 둔다(리뷰 W-2).
  - 무엇이 어려웠나: commit 은 됐는데 결과 다시 읽기만 실패하면 「실패」로 보여 사용자가 다시 올리게 되고, 같은 versionCode 라 Play 가 거절한다(리뷰 W-3). 그래서 그 경우는 exit 0 + 안내로 바꿨다. `google-api-python-client` 없이 `requests` + `cryptography` 로 서비스 계정 JWT 를 직접 서명했다.
  - 근거: `app/android/play_upload.py` · `0120b427`

- **Play 트랙 · 심사 · 노출 구조** — 내부 / 비공개 / 프로덕션
  - 개념: [[para/areas/concept/infra/unlisted-app-distribution|unlisted-app-distribution]] · [[para/areas/concept/infra/app-privacy-disclosure|app-privacy-disclosure]]
  - 무엇이 어려웠나: 비공개 · 내부 테스트 앱은 **검색에 아예 나오지 않는다.** 테스터는 참여 링크로만 들어온다. 게시 직후엔 「항목을 찾을 수 없음」이 몇 시간 간다. Console 테스터 탭의 링크가 「앱을 게시하면 표시됩니다」로 회색인 채 남아 있었지만, 참여 링크가 정해진 꼴(`play.google.com/apps/testing/<package>`)이라 직접 열어서 「You are a tester」를 받았다. 조직 계정이라 개인 계정의 「테스터 12명 × 14일」 조건이 없다. 비공개 테스트 첫 심사는 9분, 업데이트는 더 짧았다.
  - 콘텐츠 선언: 사진 · 동영상 권한(READ_MEDIA_*)은 「채팅 입력창 아래 최근 사진 줄 = 핵심 기능」으로 신고했고 통과했다. 그래서 「최근 사진 줄 제거」 대비책은 쓰지 않았다.

- **KOS 토큰 수명 = DAY 세션 수명(14시간 고정)** — 마감 중에 발견
  - 개념: [[para/areas/concept/back/refresh-token-rotation|refresh-token-rotation]]
  - prod `login_session` 최근 7일 세션이 모두 로그인 뒤 정확히 14시간에 만료됐다(읽기 전용 집계). 사용 중에도 연장되지 않는다. KOS sign-in 응답에는 refresh 토큰이 없다(HAR 50개 · 연동 코드). DAY 가 직원 본인 KOS 토큰으로 써서 KOS 기록에 실제 직원을 남기는 원칙(DAY-SPEC-001 규칙 8) 때문에 생긴 묶임이다. 별도 작업으로 넘겼다(§7).

## 3. 막혔던 것 / 사고

- **에뮬레이터 마이크** — macOS 가 에뮬레이터에 맥 마이크를 주지 않아 통역 녹음이 안 됐다 → 앱 문제가 아님을 확인하고 음성 입력은 실기기(Play 설치) 확인으로 옮겼다. 사용자가 Fold 에서 확인했다.
- **Play 설치 오류 · 「항목을 찾을 수 없음」** — 같은 패키지를 USB release apk(debug 키)로 깔아 둔 상태라 서명이 달랐다 → 지운 뒤에도 오류가 나서 폰을 재부팅해 풀었다. 「항목을 찾을 수 없음」은 게시 반영 지연이었다.
- **계정 이름을 내가 틀리게 의심했다** — 사용자가 맞게 쓴 계정을 오타로 의심했다가 정정받았다. 확인 없이 단정하지 않는다.
- **로그인 세부정보가 저장되지 않았다** — 앱 콘텐츠 「로그인 세부정보」가 [저장] 없이 빠져나가 비어 있었다 → 다시 넣었다. Console 의 각 선언은 [저장] 뒤 「완료됨」을 확인한다.
- **5판 스크린샷 오기** — 워커가 태블릿 판 끝 스크린샷 09 를 「바 위 ✓」라고 적었지만 실제로는 잘려 있었다 → 리뷰어가 화면을 직접 보고 잡았다. 워커 표를 그대로 믿지 않고 스크린샷을 연다.
- **「최근 사진 줄 제거」를 F1 과 묶자고 했다가 철회** — 심사 거절 대비책을 결정처럼 말했다. 심사 통과 뒤 사용자 질문으로 바로잡았다.
- **커밋 메시지 제목/본문 사이 빈 줄 누락** — heredoc 첫 줄 다음에 빈 줄이 없어 본문 전체가 제목이 됐다 → `commit-tree` 로 메시지만 다시 써서 force-with-lease. 코드 트리는 같았다(`git diff --quiet` 확인).
- **서비스 계정 키 생성이 조직 정책에 막힘** — §2 참고. 정책을 바꾼 직후에는 반영 지연으로 한 번 더 막힌다.

## 4. 결정

| 날짜 | 결정 | 왜 |
|---|---|---|
| 2026-11-12 | 범위 = 개발 앱 로컬 에뮬레이터 · session 구현 · push/video 스텁 · iOS 무변경 | 인수인계 §2(사용자) |
| 2026-11-13 | Android 통역도 범위 안 | 사용자 「안드로이드도 통역 넣어야지」 |
| 2026-11-13 | 범위 확장 — Play 에 올린다(개발 앱 내부 테스트) · Play 앱 서명 + 업로드 키 로컬 · 업로드 = Developer API | 사용자 · 회사 Play Console 권한 |
| 2026-11-13 | 업로드 키 = 워커가 keytool 로 · 백업은 사용자 · 실기기 = 실제 Android 폰 | 사용자 |
| 2026-11-13 | 정식 Android 앱 = `day.medisolveai` · `DAY` · prod · 비공개 테스트 · 업로드 키 공유 | 사용자 |
| 2026-11-13 | 사진 권한 그대로 · 막히면 「최근 사진 줄 = 핵심 기능」 신고 | 사용자(review-code-1 W-2) |
| 2026-11-14 | F1 고친다 — 하단 inset 만큼 비우기(몰입 모드 아님) · Dart 변경 OK · iOS 불변 · 사진 줄 유지 | 사용자 |
| 2026-11-14 | 서비스 계정 키 = 프로젝트 한정 조직 정책 재정의로 발급 후 되돌림 | 사용자(조직 관리자) |
| 2026-11-14 | PR 은 전부 끝난 뒤 한 번에 합친다 | 사용자 「PR 은 다하고 합치게」 |
| 2026-11-15 | 정식 DAY 프로덕션(공개) 출시 — vc3 승격 · Console 손 단계 | 사용자 「이제 출시 준비도 하면 되나?」 · 실기기 확인 「괜찮아서」 |
| 2026-11-16 | 마감 — #253 squash 머지 · spec-sync · 아카이브 | 사용자 「아카이브 회고 다 정리 · 문서 · 코드도」 |

## 5. 날짜별 로그

- `2026-11-12` 세팅(planner · mobile 워크트리) · planner 1회차 · reviewer_doc 발주
- `2026-11-13` 스펙 4회차 · 리뷰 4회 → mediness#940 머지 · Delivery #251 v2 승인 · mobile 1~4판(Android 개발 앱 · 업로드 키 · AAB) · 실기기 USB 확인 · Play Console 앱 생성 · DAY Dev 내부 테스트 vc1 · 정식 AAB
- `2026-11-14` 정식 DAY 콘텐츠 선언 11/11 · 비공개 테스트 vc1 심사 9분 출시 · 서비스 계정 키 · API 연결 · mobile 5 · 6판(F1 · play_upload.py) · 리뷰 3 WARN → 4 PASS · DAY Dev vc2 · vc3
- `2026-11-15` 코디 커밋 · PR #253 최신화 · 정식 alpha vc3 API 업로드 · 실기기 확인 · 프로덕션 vc3 심사 제출 · KOS 세션 14시간 확인
- `2026-11-16` #253 squash 머지 · 마감 spec-sync · 아카이브

## 6. 산출물

프로젝트와 당시 작업 문서는 `sync-work-links.py`가 만드는 작업 목차로 연결한다.
아래에는 판단의 근거가 된 리포트·PR·커밋을 구체적으로 남긴다.

- spec PR: https://github.com/MediSolveAIDev/mediness/pull/940 (머지 `855bab4f`) · 마감 spec-sync PR: https://github.com/MediSolveAIDev/mediness/pull/944 (머지 `13772db6`)
- code PR: https://github.com/MediSolveAIDev/CENTURION_DAY/pull/253 (squash `4f8316a7` → dev)
- Delivery: CENTURION_DAY#251 (v2 · L3 · conformant · 닫음 2026-11-16)

- `kknaksss/android-app` → `dev`
  - `0120b427` feat(app): Play Developer API 업로드 스크립트(play_upload.py) · 키 · AAB gitignore — AND-7
  - `099fe786` fix(app): Android 하단 시스템 바(3버튼 내비 · 태스크바)가 입력칸 · 목록 끝을 가림 — F1
  - `fa2f0d9f` feat(app): Android release 서명 = 업로드 키(저장소 밖) — 없으면 release 빌드가 멈춤
  - `e13ea876` feat(app): Android 개발 앱(DAY Dev) — app/android · day/session Keystore 구현 · push/video 스텁 · 통역 권한
- 리포트: `app-1~6-report.md` · `review-code-1~4-report.md` · `review-doc-1~4-report.md` · `spec-report.md` · `spec-2~4-report.md` · `delivery-v2-report.md` · `spec-close-report.md` · `app-5-shots/` · `app-6-shots/`
- 로컬(저장소 밖): 업로드 키 · 서비스 계정 키 · AAB · 스토어 에셋 `~/.config/day/android/`

## 7. 잔여

- **프로덕션 vc3 심사 결과** — 통과하면 자동 공개(관리형 게시 꺼짐). 거절되면 사유를 보고 다음 판.
- **KOS 세션 14시간 고정** — 모바일 로그인이 매일 끊긴다. 확인할 것: KOS 웹이 매일 로그아웃되는지 · KOS 측에 refresh API 나 토큰 수명 설정이 있는지. 그 답으로 ① KOS 갱신 ② DAY 세션 분리(시스템 계정으로 쓰기 — 기록 원칙 뒤집음) ③ 앱 비밀번호 저장 + 자동 재로그인 ④ 재로그인 편의 중에서 사용자가 고른다. **새 작업 단위.**
- Android **FCM 푸시**(지금 스텁 · 설정 탭 「알림 꺼짐」 안내가 늘 보임) · Android **동영상 보내기**(스텁).
- iPhone 차트 시트 끝이 홈 인디케이터에 조금 겹침(원래 그랬음 · iOS 불변 원칙으로 둠) — 다음 iOS 손볼 때.
- 업로드 키 **백업 위치** 미정(사용자) · 태블릿 스크린샷 · 그래픽 이미지(아이콘만 둔 단순형) 보강은 선택.
- 프로덕션 심사 결과가 나오면 mobile-deployment §1-1 · §9 「심사 중」 두 곳을 고친다.
- 통역 음성 입력(말하기 → 자막 → 번역 음성) 실기기 확인은 사용자 「확인했어」를 코디가 해석한 것 — 다음에 명시적으로 한 번 확인.

<!-- work-links:start -->
## 작업 기록

- [[orchestration/work/_archive/day/android-app/README|android-app]]
<!-- work-links:end -->
