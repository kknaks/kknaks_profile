# android-app 3판 — AND-5 업로드 키 · release AAB 서명 결과 보고

## 상태: done

미커밋(브랜치 `kknaksss/android-app` · `e13ea876` 위). `app/lib` · `app/ios` 변경 0.

## 변경 파일
| 파일 | 무엇 |
|---|---|
| `app/android/app/build.gradle.kts` | release 서명 debug 키 → 업로드 키. 경로 주입 `-PDAY_UPLOAD_KEY_PROPERTIES=<경로>` > `android/identity.local.properties` 의 같은 키 > 없음. 파일 · 4칸(`storeFile` · `storePassword` · `keyAlias` · `keyPassword`) · keystore 존재를 모두 갖춰야 `signingConfigs.upload` 생성. 없으면 release `signingConfig = null` + `:app:preReleaseBuild` doFirst 에서 `GradleException`(값 없는 안내 문구) |
| `app/android/.gitignore` | `upload-key.properties` · `**/*.p12` · `**/*.aab` 추가(기존 `key.properties` · `*.jks` · `*.keystore` 와 함께) |
| `app/README.md` | Android 절에 「release AAB(업로드 키)」 소절 추가. 1판에서 내가 쓴 마지막 줄 「release 빌드는 지금 SDK debug 키로 서명된다」는 사실이 아니게 되어 「Play 업로드 · 업로드 API 는 이 절 밖 · release 서명은 아래」로 바꿈(이 한 줄만 고침) |

## 업로드 키(값은 여기 없음)
- 폴더 `~/.config/day/android/`(700) · `out/`(700)
- keystore `~/.config/day/android/upload-keystore.jks`(600 · PKCS12 · RSA 4096 · SHA384withRSA · alias `<alias>` · `CN=DAY Upload, O=MediSolveAI, C=KR`)
- 유효 기간 10,000일: 2026-11-13 ~ 2054-03-31(27년+)
- 비밀번호: `openssl rand` 무작위 40자(store = key 같은 값) → `~/.config/day/android/upload-key.properties`(600)에만. 터미널 · 로그 · 리포트 출력 없음
- **인증서 SHA-256**: `92:75:54:AE:6B:6B:E3:7D:2D:4D:3E:40:90:AD:32:06:C0:7C:D7:B0:08:81:5F:DA:40:22:6F:2D:F9:A9:69:AD`
- 참고: 시스템 `/usr/bin/keytool` 은 Java 런타임이 없어 못 씀 → Gradle 이 받은 JDK 17(`~/.gradle/jdks/eclipse_adoptium-17…/bin/keytool`) 사용

## AAB
- `fvm flutter build appbundle --release --build-name 0.1.0 --build-number 1` + 1판과 같은 `-P` id · 이름 · dev `--dart-define`(`https://day-dev.medisolveai.com`) + `-PDAY_UPLOAD_KEY_PROPERTIES=~/.config/day/android/upload-key.properties` → ✓ 54.8MB
- 사용자가 올릴 파일: **`~/.config/day/android/out/DAY-Dev-0.1.0-1.aab`**(600) · sha256 `f0b209fa8ce554c833fe00f7a1d1bdadb236e0fb9c9540f93a3dd8b5e57ff684`

## 서명 · 매니페스트 확인
| 명령 | 결과 |
|---|---|
| `jarsigner -verify` | `jar verified.` |
| `keytool -printcert -jarfile` | Owner `CN=DAY Upload…` · SHA-256 = 위 업로드 키 지문과 같음 |
| bundletool 1.18.3(Gradle 캐시) `dump manifest` | package `day.medisolveai.dev` · versionCode `1` · versionName `0.1.0` · targetSdk `36` · minSdk `24` · `debuggable` 없음 |

## 「debug 키로 조용히 서명되는 길 0」
- release buildType 의 `signingConfig` 는 `upload` 아니면 `null` — `debug` 를 가리키는 코드가 없다(1판의 `getByName("debug")` 삭제).
- `null` 인 채로 가면 무서명 AAB 가 나올 수 있으므로 `preReleaseBuild`(assembleRelease · bundleRelease 둘 다 지남)에서 멈춘다. 멈추는 쪽을 고른 이유: 무서명 AAB 는 Play 가 받지 않고, 「알리기만」은 놓치기 쉽다.
- 실제 확인(키 경로 없이 · `identity.local.properties` 없음):
  - `build appbundle --release` → `Execution failed for task ':app:preReleaseBuild'` · 「release 서명 업로드 키가 없습니다 …」 · BUILD FAILED
  - `build apk --release` → 같은 자리에서 실패
  - `build apk --debug` → ✓(debug 영향 없음)
- `identity.local.properties` 경로는 `-P` 와 같은 `identity` Properties 에서 읽는 코드라 따로 빌드해 보지 않음.

## 검증
| 명령 | 결과 |
|---|---|
| `fvm flutter analyze` | No issues found |
| `git status --short` | `M app/README.md` · `M app/android/.gitignore` · `M app/android/app/build.gradle.kts` 뿐 |
| `git ls-files --others --exclude-standard` | 0건(키 · properties · aab 없음. 빌드 aab 는 `app/build/` — 기존 ignore) |
| 비밀 grep(비밀번호 값으로 `git diff` · `app/android` · `app/README.md` · 이 폴더 리포트) | 0건(값은 출력 없이 변수로만 비교) |

## 사용자에게 넘길 것
1. **키 백업**: `~/.config/day/android/upload-keystore.jks` + `upload-key.properties` 를 안전한 곳(비밀번호 관리자 등)에. 잃으면 Play Console 에서 업로드 키 재설정 요청이 필요하다.
2. **Play Console 첫 업로드**: 앱 만들기(`day.medisolveai.dev`) → Play 앱 서명 사용(Google 관리 키) → 내부 테스트 트랙에 `~/.config/day/android/out/DAY-Dev-0.1.0-1.aab` 올림.
3. 올린 뒤 「앱 무결성 → 앱 서명」의 **업로드 키 인증서 SHA-256** 이 위 지문과 같은지 대조.
4. 다음 업로드부터 `--build-number` 를 2, 3… 로 올린다(versionCode 중복은 Play 가 거부).
5. release apk 를 USB 로 깔려면 이제도 같은 `-PDAY_UPLOAD_KEY_PROPERTIES` 가 필요(없으면 멈춤). 1판 debug 키로 서명된 release apk 가 기기에 있으면 서명이 달라 덮어 설치가 안 되니 먼저 지운다.
