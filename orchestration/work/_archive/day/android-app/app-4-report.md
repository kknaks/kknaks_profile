# android-app 4판 — 정식 앱 DAY(day.medisolveai · prod) release AAB 결과 보고

## 상태: done — 코드 변경 0(HEAD `fa2f0d9f` · `git status` 0 · untracked 0)

## 빌드
`fvm flutter build appbundle --release --build-name 0.1.0 --build-number 1`
`-P DAY_APPLICATION_ID=day.medisolveai` · `DAY_APP_NAME=DAY` · `DAY_UPLOAD_KEY_PROPERTIES=~/.config/day/android/upload-key.properties`
`--dart-define DAY_LOGIN_ENTRY=https://day.medisolveai.com` · `DAY_ALLOWED_ORIGINS=https://day.medisolveai.com,https://day-dev.medisolveai.com` · `DAY_APNS_ENV=production` → ✓ 54.8MB

- 올릴 파일: **`~/.config/day/android/out/DAY-0.1.0-1.aab`**(600) · sha256 `42bbf86ef71fa378eb60ba69325e48a17b92ad4afd4c050fa059b414f04ad2e1`
- dev AAB `DAY-Dev-0.1.0-1.aab` 그대로

## 확인
| 항목 | 결과 |
|---|---|
| bundletool dump manifest | package `day.medisolveai` · versionCode `1` · versionName `0.1.0` · targetSdk `36` · minSdk `24` · `debuggable` 0건 |
| label | `@string/app_name` = `"DAY"`(dump resources) |
| `jarsigner -verify` | jar verified |
| `keytool -printcert -jarfile` | `CN=DAY Upload…` · SHA-256 `92:75:54:AE:…:F9:A9:69:AD` = 업로드 키(dev 와 같은 키) |
| `base/lib/arm64-v8a/libapp.so` 문자열 | `https://day.medisolveai.com`(진입점) · `https://day.medisolveai.com,https://day-dev.medisolveai.com`(허용 목록) · `production`. (그 밖 `…/privacy` 는 앱 소스에 원래 있는 개인정보 처리방침 주소) |

## 사용자에게
- Play Console 정식 앱(`day.medisolveai`) → Play 앱 서명 → 비공개 테스트 트랙에 위 AAB 손 업로드. 업로드 키 지문 대조.
- 정식 · dev 는 Play 에서 앱이 달라 versionCode 가 따로 센다. 정식 다음 업로드는 `--build-number 2`.
