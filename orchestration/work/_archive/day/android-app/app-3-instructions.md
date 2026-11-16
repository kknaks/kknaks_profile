# [mobile] 3판 — AND-5: 업로드 키 · release AAB 서명 (Play 첫 업로드용)

같은 역할 · 같은 워크트리 `/Users/kknaks/orca/workspaces/CENTURION_DAY/android-app`(브랜치 `kknaksss/android-app` · 1판은 커밋 `e13ea876` 으로 PR #253 에 있음 — 그 위에 **미커밋**으로). 커밋 · push 금지 그대로.
맥락: 이 폴더(`/Users/kknaks/orca/workspaces/kknaks_profile/안드로이드-배포/orchestration/work/android-app/`)의 `app-1-report.md` · `app-2-report.md` · `review-code-1-report.md` · `_RESUME.md` §2 · Delivery `gh issue view 251 -R MediSolveAIDev/CENTURION_DAY`(AND-5).

## 사용자 결정 (2026-11-13)

- Play 앱 서명(앱 서명 키 = Google) · **업로드 키는 네가 keytool 로 만든다** → `~/.config/day/android/`(폴더 700 · 파일 600). 백업은 사용자.
- 사용자가 실기기(USB release apk)에서 1판 확인 끝 — 이제 Play 내부 테스트에 올린다. 첫 AAB 는 **사용자가 Play Console 에서 손으로** 올린다.

## 할 것

1. **업로드 키 생성**(이미 있으면 덮지 말고 멈춰 보고): `~/.config/day/android/` 만들고(700) `keytool -genkeypair` RSA 4096 · 유효 기간 충분히(25년+) · alias 정해서 keystore 파일 하나. 비밀번호는 무작위 생성해 `~/.config/day/android/upload-key.properties`(600 · `storeFile` · `storePassword` · `keyAlias` · `keyPassword`)에 쓴다. **비밀번호 · 키 내용은 터미널 · 리포트 · 로그에 출력하지 마라.** 인증서 지문(SHA-256)은 비밀이 아니니 리포트에 적어도 된다(사용자가 Play Console 대조용).
2. **release 서명 설정** — `app/android/app/build.gradle.kts` 의 release 서명을 debug 키 → 업로드 키로. 서명 파일 경로는 저장소에 값을 두지 말고 1판 id 주입과 같은 방식(`-P DAY_UPLOAD_KEY_PROPERTIES=<경로>` > `android/identity.local.properties` 같은 로컬 파일 > 없음)으로 읽는다. **없으면 release 빌드가 조용히 debug 키로 서명되지 않게** — 분명한 오류로 멈추거나, 서명 없는 AAB 임을 알리게(어느 쪽이든 리포트에 이유). `.gitignore` 에 keystore · properties 패턴.
3. **AAB 빌드**: `fvm flutter build appbundle --release`(1판과 같은 `-P` id · 이름 · dev `--dart-define`) · 버전 `0.1.0` · **build-number 1**(첫 업로드 · `--build-number 1`). 결과 AAB 를 `~/.config/day/android/out/DAY-Dev-0.1.0-1.aab` 로 복사(사용자가 올릴 파일).
4. **서명 확인**: `jarsigner -verify` 또는 `keytool -printcert -jarfile` 로 업로드 키 지문과 같은지. aapt/bundletool 로 package `day.medisolveai.dev` · versionCode 1 · targetSdk 36.
5. `app/README.md` Android 절에 「release AAB(업로드 키)」 몇 줄 **추가만**(키 위치 = 개발자 로컬 · 값은 저장소 밖 · 명령).
6. 검증: `fvm flutter analyze` · `git status`(키 · properties · aab 가 저장소에 0 — `git ls-files --others --exclude-standard` 확인) · 비밀 grep.

## 하지 말 것

- Play 업로드 · API 스크립트(AND-7) · 서비스 계정.
- `app/lib` · `app/ios` 변경. 사용자 기기 · 프로세스 건드림.

## 산출물

- 리포트 `app-3-report.md`(같은 폴더) — 변경 파일 · 키 파일 경로(값 X) · 인증서 SHA-256 지문 · AAB 경로 · versionCode · 서명 확인 결과 · 「debug 키로 조용히 서명되는 길 0」 증명 · 사용자에게 넘길 것.
- 완료 보고는 1판 브리프 §9 두 명령(새 preamble 의 taskId · dispatchId).
