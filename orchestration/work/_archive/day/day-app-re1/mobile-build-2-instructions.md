# [mobile] DAY Dev 0.3.0 빌드 · 업로드 — iOS TestFlight 빌드 5 · Android internal vc5

너는 day `mobile` 워커다(역할 `/Users/kknaks/orca/workspaces/kknaks_profile/day-app/orchestration/roles/day/mobile/role.md`). 워크트리 `/Users/kknaks/orca/workspaces/CENTURION_DAY/day-app-re1`. 빌드는 **`git fetch origin && git checkout --detach origin/dev`** 위에서(= #295 `8fe0095a` + #296 카메라 문구 머지 커밋 — `app/ios/Runner/Info.plist` 에 「고객 여권의 정보면을 읽기 위해」가 있어야 한다 · 없으면 멈추고 보고). 코드 수정 금지. dev 서버 배포는 코디가 확인함(deploy-dev success · 새 `/api` 경로 응답).

## 절차 원천(지난 업로드 — 그대로 따른다)
- 지난 브리프 · 리포트: `/Users/kknaks/orca/workspaces/kknaks_profile/day-app/orchestration/work/_archive/day/day-mobile-v2/mobile-build-instructions.md` · `mobile-build-report.md`(같은 폴더) — 그 안에서 가리키는 iOS(config-only → archive → export · `altool --validate-app` → `--upload-app` · 키 `~/.config/day/apple/credentials.local.json` 칸) · Android(AAB `--release` · 업로드 키 · `google-services.json` 복사 후 지움 · `play_upload.py`) 절차 그대로
- dart-define · 식별자 = 지난 dev 빌드와 같은 값(`DAY_LOGIN_ENTRY` · `DAY_ALLOWED_ORIGINS` = `https://day-dev.medisolveai.com` · iOS `DAY_APNS_ENV=production` · `DAY_BUNDLE_ID=day.medisolveai.dev` · `DAY_DISPLAY_NAME=DAY Dev` / Android `DAY_APPLICATION_ID=day.medisolveai.dev` · `DAY_APP_NAME=DAY Dev`)
- 이번에 새로 들어간 네이티브(여권 스캔 iOS Vision · Android CameraX + ML Kit 번들)가 release 빌드 · 서명 · 업로드 검증을 통과하는지 확인(경고 · 오류 전문을 리포트에)

## 값
- `--build-name 0.3.0` · iOS `--build-number 5` · Android `--build-number 5`(versionCode 5)
- **정식 앱(day.medisolveai) 빌드 · 업로드 금지.** 테스터 그룹 · 심사 제출 금지(코디가 함)

## 확인 · 보고
- 산출물 안 서버 주소가 dev 도메인만인지 · Info.plist 카메라 문구 · AAB google_app_id(dev) · CAMERA 권한
- 업로드 결과(UPLOAD SUCCEEDED · play_upload commit) · TestFlight 처리 상태 · 사본 `~/.config/day/android/out/DAY-Dev-0.3.0-5.aab`
- 끝나면 `git checkout kknaksss/app-camera-copy-re1` 로 되돌리고 `app/android/app/google-services.json` 지움 · `git status` 깨끗
- 사용자 기기 · 시뮬레이터 · 로컬 스택(11040) · 실행 중 `flutter run` 건드리지 마라
- 리포트 `/Users/kknaks/orca/workspaces/kknaks_profile/day-app/orchestration/work/day-app-re1/mobile-build-2-report.md`(비밀값 · 키 id · issuer 출력 금지). 완료 = dispatch preamble 의 worker_done(`--report-path`) + 직접 주입 `[worker_done] mobile 완료: mobile-build-2 — <한 줄>. 상세는 인박스.`
