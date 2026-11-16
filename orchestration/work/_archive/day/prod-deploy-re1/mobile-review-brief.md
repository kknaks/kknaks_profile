# [reviewer] 정식 DAY 앱 제출 준비 검수

코드 워크트리: /Users/kknaks/orca/workspaces/CENTURION_DAY/prod-deploy-re1. 프로필: /Users/kknaks/orca/workspaces/kknaks_profile/day-fix-web-app.
역할: /Users/kknaks/orca/workspaces/kknaks_profile/day-fix-web-app/orchestration/roles/day/reviewer/role.md 및 같은 폴더 rules/skills/tools/workflow.md.

## 1. SSOT
- 코드 AGENTS.md, app/README.md, app/lib/, app/ios/, app/pubspec.yaml 읽기만.
- /Users/kknaks/orca/workspaces/kknaks_profile/day-fix-web-app/orchestration/work/prod-deploy-re1/mobile-submission-draft.md
- /Users/kknaks/orca/workspaces/kknaks_profile/day-fix-web-app/orchestration/work/prod-deploy-re1/mobile-build-report.md (아직 없으면 제출 초안을 먼저 검수하고 리포트 생길 때 이어 확인)
- /Users/kknaks/orca/workspaces/kknaks_profile/day-fix-web-app/orchestration/work/prod-deploy-re1/mobile-build-brief.md (허용 범위와 빌드 계약)
- /Users/kknaks/orca/workspaces/mediness-mediness/prod-deploy-re1-spec/products/day/40-architecture/mobile-deployment.md
기대는 개념: 해당 없음.

## 2. 목표
앱스토어 준비 결과의 정확성과 빠뜨린 필수 항목을 독립 검수한다. 정식 prod 앱의 준비가 목표이며, 제출 자체는 사용자 판단이다. 개인정보·지원 URL은 사용자 확인으로 미정. Unlisted 최종 배포 확정.

## 3. 계약
ID day.medisolveai / 이름 DAY / 로그인 prod / 허용 origin prod+dev / APNs production / release 환경 칸 필수. 서버 prod 설정은 다른 코디가 소유한다. M-20은 서버 코디 몫.

## 4. 확인
빌드 리포트가 생성되면 bundle 검증과 테스트·build 결과를 산출물 및 소스에 대조. 정책 링크/음성 외부 공유 고지·허가 누락, privacy manifest, SDK, 권한, version, 심사 메타데이터를 확인한다. 준비 초안의 추론과 사실을 구분했는가. 앱 실물·실기기 미확인을 통과로 적었는가. Apple 공식 URL로 필요한 현재 규정만 확인한다.

## 5. allowed_paths
쓰기 가능한 유일 파일: /Users/kknaks/orca/workspaces/kknaks_profile/day-fix-web-app/orchestration/work/prod-deploy-re1/mobile-review-report.md. 그 밖의 파일은 전부 읽기 전용. app/build 검사 가능. backend/ 웹 변경분은 검사 범위 아님.

## 6. 단계
1. 제출 초안을 먼저 검수.
2. 빌드 리포트와 결과 생기면 검사(빌드/테스트 재실행 금지).
3. PASS/WARN/FAIL, 파일:줄 근거, 제출 차단과 준비 완료의 차이를 한국어 리포트로 보고.

## 7. 제약
소스·설정·기존 _RESUME 수정·커밋·push·PR·운영 접속·키/토큰/계정 출력·ASC 변경·업로드 금지. 다른 워커와 쓰기 경로 겹치지 않음. 제출 차단이 있다는 이유만으로 준비 리포트를 FAIL 처리하지 말고, 준비 리포트가 문제를 정확히 드러내는지 판단.

## 8. 수용
산출물 근거가 있는 검수 리포트. 필수 미결 누락은 FAIL, 정확히 기록된 미결은 WARN. 빌드 리포트 없으면 완료 보고 금지.

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
