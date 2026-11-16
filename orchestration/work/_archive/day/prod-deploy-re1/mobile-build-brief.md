# [mobile] DAY 정식 앱 준비 및 prod release 빌드 검증

역할: orchestration/roles/day/mobile/{role,rules,skills,tools,workflow}.md를 절대경로로 읽는다. 프로필 루트 = /Users/kknaks/orca/workspaces/kknaks_profile/day-fix-web-app.
작업 코드 = /Users/kknaks/orca/workspaces/CENTURION_DAY/prod-deploy-re1 (kknaksss/prod-deploy-re1 → dev, PR #244).
이전 맥락은 없다. 같은 워크트리 backend/에는 다른 워커가 작업 중이다. app/ 밖 수정 금지.

## 1. SSOT
- 코드 AGENTS.md, app/README.md, app/pubspec.yaml, app/ios/Runner/Info.plist와 Runner.entitlements
- /Users/kknaks/orca/workspaces/mediness-mediness/prod-deploy-re1-spec/products/day/40-architecture/mobile-deployment.md 및 20-spec/spec-001-login-session.md, spec-003-mobile-app.md, spec-004-chat.md
- 프로필 orchestration/work/_archive/day/fix/app-testflight-upload-2-report.md (읽기만)
- 프로필 orchestration/config/projects/day.json apple (로컬 자격 위치만 확인, 값 출력 금지)
기대는 개념: 해당 없음.

## 2. 목표
사용자가 prod 기준 App Store 준비를 요청했다. 정식 앱 DAY / day.medisolveai. 기존 기능을 바꾸지 않고 현재 코드의 release 빌드와 제출 준비 상태를 사실로 확인한다. 최종 배포는 Unlisted. App Store Connect 정식 앱 record는 사용자가 만든다. 업로드·심사 제출·서명 방식 결정은 결과 보고 뒤 사용자 판단이다.

## 3. 계약
로그인 진입점 https://day.medisolveai.com, 허용 origin은 prod 및 https://day-dev.medisolveai.com 두 개, DAY_APNS_ENV=production, DAY_REQUIRE_ENVIRONMENT=true. prod에서 데모 로그인하면 dev 응답 origin으로 연결. 서버 설정 변경은 코디 몫(M-20 포함).

## 4. 확인
- 현재 git HEAD 및 app 상태, Flutter/Xcode 버전
- 정식 identity가 들어간 서명 없는 release 빌드 (임시 Identity.local.xcconfig는 기존 파일이 없을 때만 생성하고 반드시 원복; 기존 파일 있으면 덮어쓰지 않고 먼저 보고)
- 빌드 Info.plist ID/이름/버전/최소 OS/권한 설명/암호화, icon 알파 및 크기, privacy manifest와 required reason API/SDK 포함 여부 점검
- 바이너리 prod+dev 허용 origin 및 debug 로컬 설정 혼입 유무
- 코드에서 수집/전송/보관하는 데이터 목록(Apple App Privacy 작성 초안 근거), 계정 생성/삭제 기능과 직원 로그인 흐름, 통역 음성 외부 전달, 사진·영상·마이크 권한 사용
- 실제 prod 로그인·푸시 확인은 이번엔 하지 않는다(자격 입력/운영 변경 금지).

## 5. allowed_paths
소스 수정 없음. 빌드 생성물 app/build 및 무시 파일만 생성 가능. 영구 산출물은 프로필 orchestration/work/prod-deploy-re1/mobile-build-report.md 1개. backend/ · deploy/ · 환경 설정 · 기존 _RESUME.md 수정 금지.

## 6. 순서
1. 읽기 및 현재 상태 확인.
2. fvm flutter analyze, fvm flutter test, 정식 identity+prod define로 flutter build ios --release --no-codesign 각 1회. 기존 버전 그대로(첫 제출 버전은 사용자 판단, 임의 변경 금지).
3. 빌드 산출물 검사와 근거 리포트. 빌드 경고를 실제 메시지 그대로 짧게 정리. 소스 수정 필요하면 원인과 최소 변경안을 보고만 한다.

## 7. 제약
커밋·push·PR·서명·ASC mutation·업로드·심사 제출 금지. 키·토큰·Team ID·계정·개인정보 출력 금지. 다른 워커 파일을 되돌리지 않는다. 한국어 리포트. app/ 밖을 git add 하지 않는다.

## 8. 수용 기준
analyze/test/build 결과를 수치로, 산출물 절대경로와 bundle 검증 표, 소스 변화 유무, 제출을 막는 항목과 실물 미확인을 분리한다. 마지막 git diff는 app/만 확인. 위 각 검증 통과하면 반복 금지.

## 9. 완료 보고 — **문구 변경 금지**

> **⚠ 핸들은 dispatch preamble 의 값을 믿어라.** 아래 명령에 박힌 코디handle 은 **브리프 작성 시점** 값이라 오래됐을 수 있다 — 세션이 재연결되면 핸들이 바뀐다(2026-07-28·29 두 번 겪음). preamble 의 코디네이터 핸들과 아래 값이 다르면 **preamble 이 맞다.** 두 곳에 다 보내지 말고 preamble 쪽으로만 보내라.


- **커밋·push·PR 하지 마라.** 워크트리에 변경만 남긴다. 검증·PR 은 코디네이터가 한다.
- 끝나면 **아래 두 명령을 모두** 실행한다. 하나만 하면 안 된다.

```bash
# (1) 인박스 적재 — 태스크 완료 처리·영구 기록. 코디네이터를 깨우지 않는다.
orca orchestration send \
  --to term_2b709186-d9f1-4811-8538-95544d6d21b8 --from <네 워커handle> \
  --type worker_done \
  --task-id <이 태스크의 taskId — dispatch 로 받은 context 에 들어 있다> \
  --dispatch-id <이 태스크의 dispatchId — dispatch 로 받은 context 에 들어 있다> \
  --subject "mobile 완료: <한 줄>" \
  --body "변경 파일 목록 / 구현 요약 / 검증 결과(수치) / 계약 준수 / 미결·주의점"

# (2) 직접 주입 — 코디네이터 세션에 유저 메시지로 꽂혀 자동으로 깨운다.
orca terminal send --terminal term_2b709186-d9f1-4811-8538-95544d6d21b8 \
  --text "[worker_done] mobile 완료 — <한 줄 요약>. 상세는 인박스." --enter
```

- 막히면 30분 이상 혼자 헤매지 말고 같은 (2) 방식으로 물어라:
  `orca terminal send --terminal term_2b709186-d9f1-4811-8538-95544d6d21b8 --text "[질문] mobile: <질문>" --enter`
  (`orca orchestration ask` 는 채널이 닫혀 답이 안 닿는 경우가 많다.)
