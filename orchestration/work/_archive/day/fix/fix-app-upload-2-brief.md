# [mobile] DAY Dev TestFlight 빌드 2 업로드 — 서명 아카이브 → IPA → 업로드

너는 **day `mobile` 워커**(빌드 1 을 올린 같은 터미널)다. 아래 파일을 기준으로 한다.

- 빌드 1 때 네 리포트(성공한 절차 = 5차 · 실제로 돌린 명령): `/Users/kknaks/orca/workspaces/kknaks_profile/day-r3/orchestration/work/fix/app-testflight-upload-report.md`
- 빌드 1 브리프(규칙 그대로): `…/work/fix/fix-app-upload-brief.md`
- Apple 설정 위치: `/Users/kknaks/orca/workspaces/kknaks_profile/day-r3/orchestration/config/projects/day.json` 의 `apple`

작업 워크트리: `/Users/kknaks/orca/workspaces/CENTURION_DAY/fix`(브랜치 `kknaksss/fix-app-re1` · 커밋 `87cf2dec` — dev 에 스쿼시 머지된 `7b099e8f` 와 내용이 같다 · 워크트리는 깨끗하다). **이 커밋 그대로** 빌드한다. 소스 수정 금지.

## 배경

코드 PR #242 가 dev 에 머지 · 배포됐다(서버 먼저 — 완료). 앱 변경(시술현황 카드 · 채팅 · 읽음 표시 등)은 새 빌드라야 실기기에 보인다. 사용자가 TestFlight 업로드를 기대하고 있다(「테스트 플라이트도 올렸지?」) — 이번 발주에 한해 서명 · 업로드를 연다.

## 할 것

1. 빌드 값: Bundle ID `day.medisolveai.dev` · 이름 `DAY Dev` · 버전 `pubspec.yaml` 그대로 · **빌드 번호 2**(ASC 에 이미 있으면 다음 번호 · 리포트에 적는다). `--dart-define` 은 빌드 1 과 같은 셋만(`DAY_LOGIN_ENTRY` · `DAY_ALLOWED_ORIGINS` = `https://day-dev.medisolveai.com` · `DAY_APNS_ENV=production`).
2. 빌드 1 에서 성공한 절차 그대로: 서명 없이 archive → 앱만 저장소 entitlements 로 ad-hoc 서명 → export(자동 · app-store-connect) → IPA 확인 → `altool --validate-app` → `--upload-app`. 키는 `credentials.local.json` 의 경로(`~/.appstoreconnect/private_keys/` 의 키는 DAY 키가 아니다 — 쓰지 않는다).
3. 올리기 전 IPA 확인: `CFBundleIdentifier` · 버전 · 빌드 번호 · 아이콘 · `aps-environment = production` · **`ITSAppUsesNonExemptEncryption = false`** 가 들어 있는지.
4. ASC 처리 확인(최대 20분): `processingState = VALID` · **수출 규정이 이번에는 누락으로 서지 않는지**(`usesNonExemptEncryption = false` · beta 상태가 `MISSING_EXPORT_COMPLIANCE` 가 아님) — 빌드 1 때 남긴 확인 항목이다. 누락으로 서면 API 로 고치지 말고 보고한다.

## 하지 말 것

- 소스 · 프로젝트 파일 수정 · 커밋 · push 금지. 테스터 · 그룹 추가 · 베타 심사 제출 · 정식 앱 `day.medisolveai` 변경 금지.
- Key ID · Issuer ID · Team ID · 키 내용 · 토큰 · 인증서 일련번호를 화면 · 리포트에 내지 않는다.
- 사용자 포트 · 프로세스 · 시뮬레이터 · 실기기 금지. 임시 파일은 `app/build/` 안에만 — 끝나고 `git status` 가 깨끗해야 한다(이 워크트리는 곧 아카이브로 지워진다).

## 보고

리포트: `/Users/kknaks/orca/workspaces/kknaks_profile/day-r3/orchestration/work/fix/app-testflight-upload-2-report.md` — 단계별 결과 · IPA 확인 표 · ASC 빌드 상태(버전 · 빌드 번호 · processingState · 수출 규정) · 새 서명 자산(종류 · 개수) · `git status`.

끝나면 **두 명령 모두**(핸들은 dispatch preamble 값이 우선):

```bash
orca orchestration send --to term_284b2ffb-0602-4a35-b76f-0f005373d1e2 --from term_8fae9ebc-816d-4674-970b-4107e45084ff --type worker_done --task-id <taskId> --dispatch-id <dispatchId> --subject "mobile 완료: <한 줄>" --body "단계별 결과 / ASC 빌드 상태 / 수출 규정 / git status"
orca terminal send --terminal term_284b2ffb-0602-4a35-b76f-0f005373d1e2 --text "[worker_done] mobile 완료 — <한 줄 요약>. 상세는 인박스." --enter
```
