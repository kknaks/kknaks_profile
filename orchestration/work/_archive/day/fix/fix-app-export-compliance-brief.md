# [mobile] 수출 규정(암호화) 답을 자동으로 — Info.plist 키 + 빌드 1 에 답 넣기

너는 **day `mobile` 워커**다. 앞 판 리포트: `/Users/kknaks/orca/workspaces/kknaks_profile/day-r3/orchestration/work/fix/app-testflight-upload-report.md` (미결 3).

작업 워크트리: `/Users/kknaks/orca/workspaces/CENTURION_DAY/fix`

## 배경

DAY Dev 0.1.0 (1) 이 ASC 에서 `MISSING_EXPORT_COMPLIANCE` 로 서 있다. 사용자 지시(2026-11-11): **자동으로 넣어 둔다** — 빌드마다 웹에서 답하지 않게.

## 할 것

1. **먼저 확인** — 앱이 Apple 이 면제하는 암호화(HTTPS/TLS · Keychain 같은 OS 제공 암호화)만 쓰는지 `app/pubspec.yaml` 의존 · `app/lib` · `app/ios/Runner` 에서 본다. 자체 구현 · 비표준 암호화 라이브러리가 **있으면 아무것도 넣지 말고 멈춰서 물어라**(무엇이 어디 있는지).
2. 면제 범위만이면 `app/ios/Runner/Info.plist` 에 `ITSAppUsesNonExemptEncryption` = `false` 를 넣는다. 그 한 키만.
3. 이미 올라간 **빌드 1** 에 같은 답을 ASC API 로 넣는다 — `PATCH /v1/builds/{id}` `usesNonExemptEncryption: false`. 대상은 앱 `day.medisolveai.dev` 의 빌드 1 하나뿐. 재조회로 `usesNonExemptEncryption` 과 `buildBetaDetail` 의 internal · external 상태를 확인한다.
4. `app/README.md` 에 이 키가 무엇이고 왜 `false` 인지 한두 줄(근거 = 1 의 확인 결과).

## 하지 말 것

- 그 밖의 소스 · 프로젝트 파일 수정, 다시 빌드 · 다시 업로드, 테스터 · 그룹 추가, 베타 심사 제출, 정식 앱 `day.medisolveai` 변경 금지.
- Key ID · Issuer ID · Team ID · 키 내용 · 토큰을 화면 · 리포트에 내지 않는다. `~/.appstoreconnect/private_keys/` 의 키는 DAY 키가 아니다 — `credentials.local.json` 의 경로를 쓴다.
- 커밋 · push · PR 금지. 사용자 포트 · 프로세스 · 기기 금지.

## 검증 · 보고

- `plutil -lint app/ios/Runner/Info.plist` · `git diff --stat`(Info.plist · README 뿐)
- 1 의 근거(의존 · 파일), 3 의 재조회 결과
- 리포트: `/Users/kknaks/orca/workspaces/kknaks_profile/day-r3/orchestration/work/fix/app-export-compliance-report.md`

## 완료 보고 — **문구 변경 금지**

> **⚠ 핸들은 dispatch preamble 의 값을 믿어라.** 아래 값과 다르면 preamble 이 맞다.

```bash
orca orchestration send \
  --to term_284b2ffb-0602-4a35-b76f-0f005373d1e2 --from term_8fae9ebc-816d-4674-970b-4107e45084ff \
  --type worker_done \
  --task-id <dispatch context 의 taskId> \
  --dispatch-id <dispatch context 의 dispatchId> \
  --subject "mobile 완료: <한 줄>" \
  --body "확인 근거 / 변경 파일 / ASC 재조회 결과 / 미결"

orca terminal send --terminal term_284b2ffb-0602-4a35-b76f-0f005373d1e2 \
  --text "[worker_done] mobile 완료 — <한 줄 요약>. 상세는 인박스." --enter
```

막히면: `orca terminal send --terminal term_284b2ffb-0602-4a35-b76f-0f005373d1e2 --text "[질문] mobile: <질문>" --enter`
