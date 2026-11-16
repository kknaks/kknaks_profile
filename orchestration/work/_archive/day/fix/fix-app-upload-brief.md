# [mobile] DAY Dev 첫 TestFlight 업로드 — 서명 아카이브 → IPA → 업로드

너는 **day `mobile` 워커**다. 앞 판(같은 터미널)의 맥락이 있더라도 아래 파일을 기준으로 한다.

- 역할: `/Users/kknaks/orca/workspaces/kknaks_profile/day-r3/orchestration/roles/day/mobile/role.md` (+ 같은 폴더 문서)
- 앞 판 리포트(명령 초안이 여기 있다): `/Users/kknaks/orca/workspaces/kknaks_profile/day-r3/orchestration/work/fix/app-testflight-prep-report.md`
- Apple 설정 위치: `/Users/kknaks/orca/workspaces/kknaks_profile/day-r3/orchestration/config/projects/day.json` 의 `apple`
- 빌드 설정: `/Users/kknaks/orca/workspaces/CENTURION_DAY/fix/app/README.md`

작업 워크트리: `/Users/kknaks/orca/workspaces/CENTURION_DAY/fix` (브랜치 `kknaksss/fix`). 앞 판 변경(아이콘 · README)이 미커밋으로 남아 있다 — 그대로 두고 그 위에서 빌드한다.

## 1. 배경

사용자가 App Store Connect 에 앱 record 「DAY Dev」(`day.medisolveai.dev`)를 만들었다(코디가 2026-11-11 API 로 확인). 사용자가 서명 · 업로드를 승인했다 — **이번 발주에 한해** 역할 문서의 「서명 · TestFlight 는 사용자 몫」을 연다. 목적은 사용자가 실기기에서 알림 · 채팅을 확인하는 것이다.

## 2. 할 것

1. **빌드 값**
   - Bundle ID `day.medisolveai.dev` · 이름 `DAY Dev` — Xcode 빌드 설정을 명령줄로(소스 기본값 안 바꿈).
   - 버전 `pubspec.yaml` 그대로(0.1.0) · 빌드 번호 `1`. ASC 에 이미 같은 번호가 있으면 다음 번호로 올리고 리포트에 적는다.
   - `--dart-define`: `DAY_LOGIN_ENTRY=https://day-dev.medisolveai.com` · `DAY_ALLOWED_ORIGINS=https://day-dev.medisolveai.com` · `DAY_APNS_ENV=production`. 그 밖의 define 을 넣지 않는다(`DAY_REQUIRE_ENVIRONMENT` · `DAY_DEV_LOCAL_ORIGIN` 금지).
2. **서명 아카이브 → IPA** — 앞 판 리포트 「업로드에 쓸 명령」 1)~3). 자동 서명(`-allowProvisioningUpdates` + ASC API 키)이 이 팀에 배포 인증서 · 프로비저닝 프로파일을 만드는 것은 허용한다. 그 밖의 것(기기 등록 · 다른 App ID · capability 변경)은 만들지 않는다.
3. **키 경로** — ⚠ `~/.appstoreconnect/private_keys/` 의 키는 **DAY 키가 아니다.** 쓰지 않는다. `-authenticationKeyPath` 는 `credentials.local.json` 의 `app_store_connect.private_key_path` 를 그대로 쓰고, `altool` 은 `API_PRIVATE_KEYS_DIR=~/.config/day/apple` 로 폴더를 지정한다. 키를 복사 · 이동하지 않는다.
4. **올리기 전 IPA 확인** — `CFBundleIdentifier` · `CFBundleDisplayName` · 버전 · 빌드 번호 · 아이콘 · entitlements 의 `aps-environment = production` · `application-identifier` 의 번들 ID.
5. **업로드** — `xcrun altool --validate-app` → 통과하면 `--upload-app`.
6. **처리 확인** — ASC API 로 그 빌드의 `processingState` 를 조회한다(최대 20분 · 1~2분 간격). `VALID` 가 되면 끝. 그 안에 안 끝나면 그때 상태를 적고 pending 으로 보고한다.

## 3. 하지 말 것

- 소스 수정 금지(`app/lib` · `app/test` · `Info.plist` · `pbxproj` · xcconfig · `backend/`). 업로드가 소스 수정 없이는 안 되면 **멈추고 물어라** — 무엇이 왜 필요한지 한 줄로.
- `ITSAppUsesNonExemptEncryption` 이 `Info.plist` 에 없다 — 지어 넣지 않는다. 그 때문에 빌드가 「수출 규정 준수 정보 누락」으로 서면 그 상태를 보고만 한다(사용자가 웹에서 답한다).
- TestFlight 테스터 · 그룹 추가, 베타 심사 제출, 앱 정보 · 스크린샷 입력 금지.
- 정식 앱 `day.medisolveai` 는 건드리지 않는다.
- Key ID · Issuer ID · Team ID · 키 내용 · 토큰 · 인증서 일련번호를 화면 · 리포트 · 로그에 내지 않는다(명령 출력에 섞이면 가린다). profile 레포는 PUBLIC 이다.
- 사용자 포트(로컬 11040) · 프로세스 · 시뮬레이터 · 실기기 금지. 커밋 · push · PR 금지.
- 임시 파일(`Identity.local.xcconfig` · `ExportOptions.plist` 등)은 끝나면 지우거나 `app/build/` 안에만 둔다. `git status` 가 앞 판과 같아야 한다.

## 4. 검증 · 보고

리포트: `/Users/kknaks/orca/workspaces/kknaks_profile/day-r3/orchestration/work/fix/app-testflight-upload-report.md`

- 실제로 돌린 명령(값은 가림) · 단계별 결과(archive · export · validate · upload)
- IPA 확인 표(§2-4)
- ASC 빌드 상태(버전 · 빌드 번호 · processingState · 수출 규정 누락 여부)
- 새로 생긴 서명 자산(종류 · 개수만)
- `git status --short` 가 앞 판과 같은지
- 실패하면 오류 원문(비밀값 가림)과 원인 · 필요한 것

## 5. 완료 보고 — **문구 변경 금지**

> **⚠ 핸들은 dispatch preamble 의 값을 믿어라.** 아래 값과 다르면 preamble 이 맞다.

끝나면 **두 명령 모두** 실행한다.

```bash
orca orchestration send \
  --to term_284b2ffb-0602-4a35-b76f-0f005373d1e2 --from term_8fae9ebc-816d-4674-970b-4107e45084ff \
  --type worker_done \
  --task-id <dispatch context 의 taskId> \
  --dispatch-id <dispatch context 의 dispatchId> \
  --subject "mobile 완료: <한 줄>" \
  --body "단계별 결과 / ASC 빌드 상태 / 새 서명 자산 / 미결·주의점"

orca terminal send --terminal term_284b2ffb-0602-4a35-b76f-0f005373d1e2 \
  --text "[worker_done] mobile 완료 — <한 줄 요약>. 상세는 인박스." --enter
```

막히면: `orca terminal send --terminal term_284b2ffb-0602-4a35-b76f-0f005373d1e2 --text "[질문] mobile: <질문>" --enter`
