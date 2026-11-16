# [mobile] 4판 — 정식 앱(DAY · day.medisolveai) release AAB 빌드

같은 역할 · 같은 워크트리 `/Users/kknaks/orca/workspaces/CENTURION_DAY/android-app`(HEAD `fa2f0d9f`). **코드 변경 없음** — 빌드만. 커밋 · push · 업로드 금지.

## 사용자 결정 (2026-11-13)
- 정식 Android 앱 = 패키지 **`day.medisolveai`** · 이름 **`DAY`** · **prod 서버** (iOS 정식과 같게 — `app/README.md` 「개발 / 정식 빌드」 표). 사용자가 Play Console 에 앱을 이미 만들었다. 배포 트랙 = 비공개 테스트(사용자가 손 업로드).
- 업로드 키는 dev 와 **같은 키**(`~/.config/day/android/upload-key.properties`).

## 할 것
1. `fvm flutter build appbundle --release --build-name 0.1.0 --build-number 1`
   - `--android-project-arg=DAY_APPLICATION_ID=day.medisolveai` · `--android-project-arg=DAY_APP_NAME=DAY`
   - `--android-project-arg=DAY_UPLOAD_KEY_PROPERTIES=$HOME/.config/day/android/upload-key.properties`
   - `--dart-define=DAY_LOGIN_ENTRY=https://day.medisolveai.com` · `--dart-define=DAY_ALLOWED_ORIGINS=https://day.medisolveai.com,https://day-dev.medisolveai.com`(README 「정식 빌드 = prod · dev 두 공개 주소」 — 데모 계정 → dev 연결 규칙) · `--dart-define=DAY_APNS_ENV=production`(iOS 정식과 같게 · Android 는 푸시 스텁이라 영향 없음)
2. 결과를 `~/.config/day/android/out/DAY-0.1.0-1.aab`(600)로 복사. dev AAB 는 그대로 둔다.
3. 확인: bundletool dump manifest → package `day.medisolveai` · label `DAY` · versionCode 1 · targetSdk 36 · debuggable 없음 / `keytool -printcert -jarfile` 지문 = 업로드 키(92:75:54:AE…69:AD) / AAB 안 dart-define 이 prod 인지(가능하면 문자열 확인 — 값은 공개 주소라 출력 OK).
4. `git status` 변경 0 확인.

리포트 `app-4-report.md`(같은 폴더 · 짧게). 완료 보고는 1판 브리프 §9 두 명령(새 preamble 의 taskId · dispatchId).
