# [mobile] DAY Dev 0.2.0 빌드 · 업로드 — iOS TestFlight 빌드 4 · Android internal vc4

워크트리 `/Users/kknaks/orca/workspaces/CENTURION_DAY/day-mobile-v2`. **dev 에 스쿼시 머지됨(`5ece25ea` · PR #266)** — 빌드는 `git fetch origin && git checkout --detach origin/dev`(= 5ece25ea · 트리는 브랜치 HEAD 8a76c35b 와 같아야 함 · 다르면 멈추고 보고) 위에서. 코드 수정 금지. dev 서버 배포는 코디가 확인함.

## 절차 원천(지난 업로드 — 그대로 따른다)
- iOS: `/Users/kknaks/orca/workspaces/kknaks_profile/day-mobile-v2/orchestration/work/_archive/day/fix/app-testflight-upload-2-report.md` · `/Users/kknaks/orca/workspaces/kknaks_profile/day-mobile-v2/orchestration/work/_archive/day/fix/fix-app-upload-2-brief.md` · `/Users/kknaks/orca/workspaces/kknaks_profile/day-mobile-v2/orchestration/work/_archive/day/fix/app-testflight-prep-report.md` — config-only → 서명 없이 archive → export · 서명 우회 절차 · `altool --validate-app` → `--upload-app`. 키 = `~/.config/day/apple/credentials.local.json` 칸(값 출력 금지).
- Android: `/Users/kknaks/orca/workspaces/kknaks_profile/day-mobile-v2/orchestration/work/_archive/day/android-app/app-3-report.md` · `app-5/6` · `app/android/play_upload.py`(README `app/README.md` Android 절) — AAB `--release` · 업로드 키 `~/.config/day/android/upload-key.properties` · **`~/.config/day/android/google-services.json` 을 `app/android/app/google-services.json` 으로 복사(빌드 뒤 지움 · 커밋 금지)** · `play_upload.py upload --package day.medisolveai.dev --track internal --aab … --expect-version-code 4`
- 서버: dev 앱 dart-define = 지난 dev 빌드와 같은 값(`DAY_LOGIN_ENTRY` · `DAY_ALLOWED_ORIGINS` = dev 도메인 · `DAY_APNS_ENV=production` 등 — 지난 리포트 그대로)

## 값
- 버전 `--build-name 0.2.0` · iOS DAY Dev `--build-number 4` · Android DAY Dev `--build-number 4`(versionCode 4)
- 식별자 iOS `DAY_BUNDLE_ID=day.medisolveai.dev` · `DAY_DISPLAY_NAME=DAY Dev` / Android `-PDAY_APPLICATION_ID=day.medisolveai.dev` · `-PDAY_APP_NAME="DAY Dev"`
- **정식 앱(day.medisolveai) 빌드 · 업로드는 하지 마라.**

## 확인 · 보고
- 산출물 안 서버 주소가 dev 도메인만인지(지난 리포트 방식) · Android AAB 에 google_app_id(dev) 있는지
- 업로드 결과(altool UPLOAD SUCCEEDED · play_upload commit) · TestFlight 처리 상태 · 산출물 사본 `~/.config/day/android/out/DAY-Dev-0.2.0-4.aab`
- 끝나면 워크트리를 `git checkout kknaksss/day-mobile-v2` 로 되돌리고 `app/android/app/google-services.json` 지움 · `git status` 깨끗
- 리포트 `/Users/kknaks/orca/workspaces/kknaks_profile/day-mobile-v2/orchestration/work/day-mobile-v2/mobile-build-report.md`(비밀값 · 키 id · issuer 출력 금지). 사용자 기기 · 시뮬레이터 건드리지 마라.

완료 보고는 dispatch preamble 의 worker_done 그대로.
