# 리뷰 리포트 — android-app AND-5 release 서명 / code (2026-11-13 · 2회차)

대상: 커밋 `e13ea876..fa2f0d9f`(1개). 바뀐 파일은 `app/android/app/build.gradle.kts` · `app/android/.gitignore` · `app/README.md` 3개다. 워크트리는 깨끗하다(`git status` 0).
근거: mobile-deployment §7-2(업로드 키는 저장소 밖 `~/.config/day/android/` · 600) · Delivery #251 A7 · 1회차 리포트 「6. 빌드 설정」.

## 판정: PASS (WARN 1 · 낮음)

## 볼 것별

| # | 항목 | 결과 | 근거 |
|---|---|---|---|
| ① | release 가 debug 키나 무서명으로 나가는 길 0 | PASS | `build.gradle.kts:80-83` release `signingConfig` 는 `upload` 아니면 `null` 이다. `getByName("debug")` 는 삭제됐다. `:88-98` `preReleaseBuild` doFirst 에서 `uploadKey == null` 이면 `GradleException` 을 던진다. **리뷰어가 직접 실행**: 키 경로 없이 `fvm flutter build apk --release` → `Execution failed for task ':app:preReleaseBuild'` · 안내 문구(값 없음) · BUILD FAILED. 키 파일 검증(`:27-41`)은 파일 존재 · 4칸이 비어 있지 않음 · keystore 파일 존재를 본다. 하나라도 빠지면 null 이 되고 빌드가 멈춘다(부분 서명 0) |
| ② | 주입 우선순위 · 저장소에 값 0 | PASS | `:28-29` `findProperty`(-P)가 먼저고 없으면 `identity` Properties 를 본다(= identity.local.properties, 1회차와 같은 로더). storeFile 이 상대 경로면 properties 파일 기준(`:36`)이다. `git grep` 결과 storePassword · keyPassword 는 `getProperty` 호출뿐이고 값 · 지문 · 비밀번호는 0이다. README 예시는 `$HOME/.config/...` 경로뿐이다 |
| ③ | `.gitignore` 가 키 · properties · aab 를 막는지 | PASS (`app/android/` 아래) · W-1 | `git check-ignore` 로 `app/android/` 와 `app/android/app/` 의 `upload-key.properties` · `key.properties` · `*.jks` · `*.keystore` · `*.p12` · `*.aab` · `identity.local.properties` 가 모두 ignored 인 것을 확인했다 |
| ④ | debug · flutter run 영향 없음 | PASS | `signingConfigs.debug` · debug buildType 은 건드리지 않았다. 검사는 `preReleaseBuild` 에만 걸린다. 워커가 키 없이 `build apk --debug` ✓ 를 확인했고, 1회차 debug 빌드 경로도 그대로다 |
| ⑤ | README 변경 = 추가 + 자기 줄 1개 수정 | PASS | `-1 +21` 이다. 지운 1줄은 1판에서 워커가 쓴 「release 빌드는 지금 SDK debug 키로 서명된다」로, 이제 사실이 아니라 바꾼 것이다. 나머지는 「release AAB(업로드 키)」 소절 추가다 |
| ⑥ | `~/.config/day/android/` 권한 | PASS | 폴더 · `out/` 은 `drwx------`(700)이고 `upload-key.properties` · `upload-keystore.jks` · `out/DAY-Dev-0.1.0-1.aab` 는 `-rw-------`(600)이다. 값은 열지 않았다(`stat` 만) |
| 관문 | `fvm flutter analyze` | PASS | No issues found (exit 0) |

## WARN

### W-1 (낮음) ignore 패턴이 `app/android/` 아래에서만 걸린다
- 위치: `app/android/.gitignore:22-25`
- 근거: `app/upload-keystore.jks` · `app/upload-key.properties` · `app/x.aab` · 레포 루트 `upload-keystore.jks` · `x.aab` 는 check-ignore 결과 **NOT ignored** 다. 키는 원래 `~/.config/day/android/` 에 두고 AAB 는 ignore 된 `app/build/` 에 생기므로 지금 새는 길은 없다. 다만 사람이 키나 AAB 를 `app/` 이나 루트에 복사하면 `git add -A` 로 들어갈 수 있다.
- 고칠 방향(선택): `app/.gitignore`(또는 루트)에 `*.jks` · `*.keystore` · `*.p12` · `*.aab` · `upload-key.properties` 를 더한다. 머지를 막을 사유는 아니다.

## 참고
- **profile 빌드는 debug 키로 서명된다**: Flutter 플러그인이 `profile` 을 `initWith(debug)` 로 만든다(`fvm/versions/3.44.8/.../FlutterPlugin.kt:207-209`). 그래서 `build appbundle --profile` 은 검사를 지나지 않는다. 하지만 profile 산출물은 debuggable 이고 debug 서명이라 Play 가 거절하므로 조용히 나가는 길은 아니다. README 의 업로드 명령은 `--release` 만 쓴다.
- **오래된 release APK 가 남아 있다**: `app/build/app/outputs/flutter-apk/app-release.apk`(12:19 · AND-5 커밋 13:14 이전 — 1판 debug 키로 서명된 것으로 보임). ignore 된 build/ 안이라 커밋 위험은 없다. 다만 이 파일을 기기 설치나 배포에 쓰면 안 된다(워커 리포트 5번과 같은 취지). 필요하면 `flutter clean` 하거나 다시 빌드한다.
- `-PDAY_UPLOAD_KEY_PROPERTIES=~/...` 처럼 `~` 를 따옴표 안이나 `=` 뒤에 쓰면 셸이 펼치지 않을 수 있다 → 파일을 못 찾아 null 이 되고 빌드가 멈춘다(조용하지 않음). README 는 `$HOME` 을 써서 문제없다.
- 업로드 키 인증서 SHA-256 은 공개 지문이다(비밀 아님). 저장소에는 없고 워커 리포트에만 있다.
