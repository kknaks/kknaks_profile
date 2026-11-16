# [mobile] 5판 — F1(하단 시스템 바 가림) + AND-7(Play API 업로드 스크립트) · 빌드 2

같은 역할 · 같은 워크트리 `/Users/kknaks/orca/workspaces/CENTURION_DAY/android-app`(브랜치 `kknaksss/android-app` · HEAD `fa2f0d9f` · PR #253 OPEN). **커밋 · push · PR 금지**(코디가 한다 — 사용자: 「PR 은 다 하고 합치게」).
맥락: 이 폴더(`/Users/kknaks/orca/workspaces/kknaks_profile/안드로이드-배포/orchestration/work/android-app/`)의 `e2e-feedback.md`(F1) · `app-3-report.md` · `app-4-report.md` · `review-code-2-report.md`(W-1) · `_RESUME.md` §2 · Delivery `gh issue view 251 -R MediSolveAIDev/CENTURION_DAY`(AND-7).

## 0. 시작 전 — dev 최신 확인 (사용자 요청)

`git fetch origin` → `git log --oneline HEAD..origin/dev`. **0이 아니면** `git rebase origin/dev` 부터(충돌 나면 멈추고 코디에게). 끝나고 보고 직전에 한 번 더 같은 확인 · 결과를 리포트에.

## 사용자 결정 (2026-11-14)

- **F1 고친다** — 정석 = 하단 시스템 inset 만큼 비우기(몰입 모드로 숨기지 않음). **Dart 변경 OK**(사용자). **iOS 화면은 그대로**여야 한다(iOS 는 다시 제출 안 함).
- **채팅 「최근 사진 줄」은 그대로 둔다**(사진 권한 신고가 Play 심사 통과).
- 서비스 계정 키 발급 끝 → **빌드 2 부터 API 업로드**. 키 `~/.config/day/android/play-service-account.json`(600 · Play 업로드 전용 서비스 계정 · DAY · DAY Dev 권한). 코디가 읽기 시험 통과(DAY alpha vc1 · DAY Dev internal vc1).

## 할 것

### A. F1 — 하단 시스템 바(3버튼 내비 · 삼성 태스크바)가 앱 하단을 가림
1. **전수조사 먼저**: 화면 아래쪽에 붙는 요소를 `app/lib` 에서 grep 으로 **전부** 센다 — `bottomNavigationBar` · `bottomSheet` · `showModalBottomSheet` · `Positioned(... bottom:` · `Align(alignment: Alignment.bottom…` · 채팅 입력창 · 하단 고정 버튼 · `SafeArea` · `MediaQuery.*(padding|viewPadding|viewInsets)` 사용처. 표(파일:줄 · 요소 · 지금 inset 처리 · 고침 여부)를 리포트에.
2. 고침: 하단 요소가 `MediaQuery.viewPadding.bottom`(또는 SafeArea bottom)만큼 비우게. 키보드(viewInsets)와 겹쳐 두 번 비지 않게. **iOS 에서 이미 맞던 여백이 두 배가 되지 않게**(iOS 홈 인디케이터 영역은 지금 어떻게 처리되는지 먼저 읽고 같은 방식으로 맞춘다). Android 전용 분기(`Platform.isAndroid`)는 꼭 필요할 때만 · 쓰면 이유를 리포트에.
3. 확인(사용자 표면 = 화면):
   - **Android 에뮬레이터 3버튼 내비**로 바꿔서(예: `adb shell cmd overlay enable com.android.internal.systemui.navbar.threebutton`) 채팅 상세 입력창 · 하단 탭 · 시트 · 하단 버튼이 내비 바 위에 보이는지 스크린샷. 가능하면 태블릿/큰 화면 에뮬레이터(태스크바) 1장. 제스처 내비도 1장(퇴행 없음).
   - **iOS 시뮬레이터**(iPhone · iPad 각 1)에서 같은 화면 **고치기 전/후** 스크린샷 — 달라진 게 없어야 한다.
   - 스크린샷은 `app-5-shots/`(이 폴더). dev 로그인 = `~/.config/day/dev-login.local.json`(값 출력 금지).
   - 사용자 에뮬레이터 · 시뮬레이터 · 프로세스는 끄지 마라 — 네가 띄운 것만.
4. `fvm flutter analyze` · `fvm flutter test` 통과.

### B. AND-7 — Play Developer API 업로드 스크립트
1. 저장소 안 스크립트(위치는 `app/android/` 아래 또는 `app/scripts/` — 기존 관례 보고 정해 리포트에). 하는 일: 서비스 계정 키 경로(인자/환경변수 · 기본 `~/.config/day/android/play-service-account.json`)로 토큰 → `edits.insert` → `bundles.upload`(AAB) → `tracks.update`(트랙 · 출시명 · 출시 노트 ko-KR · status `completed`) → `edits.commit`. 실패하면 edit 삭제.
   - `--dry-run`(커밋 없이 검증만 · `edits.validate`) 지원.
   - 패키지 · 트랙 · AAB 경로 · 출시 노트는 인자. **키 · 토큰 값은 출력 · 로그 금지.** 저장소에 키 경로 외 값 없음.
   - 의존성 최소(파이썬이면 표준 + `requests` · `cryptography` — 코디 확인 시 이 둘은 있음). 추가 설치가 필요하면 README 에.
2. **W-1**(review-code-2): `app/.gitignore` 에 `*.jks` · `*.keystore` · `*.p12` · `*.aab` · `upload-key.properties` · `play-service-account*.json`.
3. `app/README.md` Android 절에 「Play 업로드(API)」 몇 줄 **추가만**(키 위치 = 개발자 로컬 · 명령 예 · dry-run).

### C. 빌드 2 + 업로드
1. AAB 두 개 · **versionCode 2** · versionName `0.1.0`(코드 변경만이라 그대로 — 바꿀 이유 있으면 코디에게):
   - 개발 앱: 3판과 같은 인자(`day.medisolveai.dev` · `DAY Dev` · dev dart-define) → `~/.config/day/android/out/DAY-Dev-0.1.0-2.aab`
   - 정식 앱: 4판과 같은 인자(`day.medisolveai` · `DAY` · prod dart-define) → `~/.config/day/android/out/DAY-0.1.0-2.aab`
   - 둘 다 600 · 지문 = 업로드 키(92:75:54:AE…69:AD) · versionCode 2 · targetSdk 36 확인.
2. **업로드는 개발 앱만**: `day.medisolveai.dev` → `internal` 트랙 · 출시명 `2 (0.1.0)` · 노트 「하단 내비게이션 바가 입력창을 가리던 문제 수정」. 먼저 `--dry-run` → 통과하면 실제. 결과(트랙 읽기)를 리포트에.
3. **정식 앱(`day.medisolveai` · alpha)은 dry-run 까지만.** 실제 업로드는 사용자가 실기기(Z Fold3)로 개발 앱 F1 확인한 뒤 코디가 지시한다.

## 하지 말 것

- 커밋 · push · PR · 정식 앱 실제 업로드 · 프로덕션 트랙 · 스토어 등록정보 변경.
- 채팅 최근 사진 줄 · 사진 권한 · iOS 네이티브(`app/ios`) 변경.
- F1 과 무관한 화면 수정. 화면 문구 새로 짓기.

## 산출물

- 리포트 `app-5-report.md`(같은 폴더) — dev 최신 확인(시작/끝) · F1 전수조사 표 · 변경 파일 · 스크린샷 목록(Android 3버튼/태스크바/제스처 · iOS 전/후) · analyze/test 수치 · 스크립트 경로 · 사용법 · dry-run/업로드 결과 · AAB 2개 확인값 · 비밀 grep 0 · 사용자에게 넘길 것.
- 완료 보고는 1판 브리프 §9 두 명령(새 preamble 의 taskId · dispatchId).
