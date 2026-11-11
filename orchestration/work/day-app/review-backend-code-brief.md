# [reviewer] DAY 앱 코드 독립 검수 — backend D1

너는 day reviewer다. 맥락 없음. 역할 /Users/kknaks/orca/workspaces/kknaks_profile/cc-2ck/orchestration/roles/day/reviewer/{role,rules,skills,tools,workflow}.md 및 코드 AGENTS.md를 읽는다. 이번 검수는 backend D1만. mobile은 app/에서 구현중이므로 그쪽은 아직 검수대상아님.

## 1. SSOT
문서트리 /Users/kknaks/orca/workspaces/mediness-mediness/day-app-spec exact commit 78f3ee59c8a10e0abb1bde8896302873a46d0732의 SPEC001 로그인 환경연결전문·케이스매트릭스·규칙14, SPEC003 관련세션계약과 배포문서. profile 작업폴더 /Users/kknaks/orca/workspaces/kknaks_profile/cc-2ck/orchestration/work/day-app/의 delivery-request.json, implementation-user-direction.md, day-app-be-brief.md, backend-code-report.md. 승인된 GitHub Delivery https://github.com/MediSolveAIDev/CENTURION_DAY/issues/235.

## 2. 권한·현재상태
사용자가 “머지는 마지막인데 코드 구현해”라고 명시했다. SPEC PR #921 OPEN 및 baseline pending 그대로 미머지SPEC로 구현한다. 이를 구현결함이나 승인부재로 재질문하지 않는다. ready위조/merge/배포는금지. 결과계약승인됨, 변경금지. 이번은 단일코드PR→dev의 D1분담 검수.

## 3. 검수계약
prod+client app+demo email만 dev relay, trim/lowercase. DB쓰기/KOS호출전에 분기. 일반/prod·dev·웹·다중병원 계약, 설정origin정규화·userinfo/non443/path/query/fragment거부, 전체60초/redirect0/retry0,4xx보존/기타503,wrongenv/origin거부,prod행0. request 환경헤더/unknown필드로라우팅변경0. APP_ENV/DB_SCHEMA 요청변경0. 비밀번호/토큰로그0. rollback email목록유지+demo base비우면503. /me environment 및 앱모든성공응답필드. 공통설정값추가가 기존웹을깨지않는지, own_target오류전에외부KOS부작용발생여부, 실제httpx예외·malformedJSON·쿠키전달경계도 확인.

설정값 입력은 사용자 몫이지만 compose/배포 코드가 그 값을 실제 앱으로 전달하는 구조는 코드구현 몫이다. 현재 worker가 compose.local.yaml 신규env전달을 빠뜨렸다고 보고했으므로, 로컬/서버 manifest가 이미env_file로전부받는지 실제확인하고 명시목록이면 필요한이름의전달코드누락을 지적한다. 실제비밀파일읽기/수정은금지.

## 4. 읽을실물
코드트리 /Users/kknaks/orca/workspaces/CENTURION_DAY/day-app. git diff/신규파일로 backend D1, common/config, deploy예제, AGENTS 앱주소규칙을 확인. 테스트더블이 실제라우터와relay에결속됐는지/infra행0검증이단위spy로대체되지않았는지 확인. 테스트수치보고만믿지않는다.

## 5. allowed_paths
코드·스펙 read-only. profile 작업폴더 review-backend-code-report.md 보고서 하나만 생성. 수정/커밋/push/PR/네트워크외부write/서버기동·중지/기기조작금지. 앱빌드/실env읽기/DB테스트실행도 이번검수에서금지(코디가scratch day_test접속으로검증).

## 6. 검증
필요한 non-infra auth·architecture 테스트, ruff를 실행할 수 있다. 같은검증이미PASS면불필요한반복금지. FAIL/WARN/PASS를각파일:줄+SPEC/WP근거+재현/영향으로작성. 승인범위밖기능추가요구0.

## 7. 결과
backend D1 결함여부/스코프준수·의미있는테스트·실연동pending을구분. 조용히성공하는실패경로·보안경계·회귀를우선한다. code·integration전체완료를선언하지않는다. 지적만보고수정은원워커.

## 8. 통신
live preamble id/핸들/worker_done --outcome 우선, legacy§9보다live명령우선. 보고서는한국어.

## 9. 완료 보고 — **문구 변경 금지**

> **⚠ 핸들은 dispatch preamble 의 값을 믿어라.** 아래 명령에 박힌 코디handle 은 **브리프 작성 시점** 값이라 오래됐을 수 있다 — 세션이 재연결되면 핸들이 바뀐다(2026-07-28·29 두 번 겪음). preamble 의 코디네이터 핸들과 아래 값이 다르면 **preamble 이 맞다.** 두 곳에 다 보내지 말고 preamble 쪽으로만 보내라.


- **커밋·push·PR 하지 마라.** 워크트리에 변경만 남긴다. 검증·PR 은 코디네이터가 한다.
- 끝나면 **아래 두 명령을 모두** 실행한다. 하나만 하면 안 된다.

```bash
# (1) 인박스 적재 — 태스크 완료 처리·영구 기록. 코디네이터를 깨우지 않는다.
orca orchestration send \
  --to term_781a6b8f-68da-447e-acb9-c2261321c190 --from term_800d77f0-3654-4902-9baa-4f95bdb06d7b \
  --type worker_done \
  --task-id <이 태스크의 taskId — dispatch 로 받은 context 에 들어 있다> \
  --dispatch-id <이 태스크의 dispatchId — dispatch 로 받은 context 에 들어 있다> \
  --subject "reviewer 완료: <한 줄>" \
  --body "변경 파일 목록 / 구현 요약 / 검증 결과(수치) / 계약 준수 / 미결·주의점"

# (2) 직접 주입 — 코디네이터 세션에 유저 메시지로 꽂혀 자동으로 깨운다.
orca terminal send --terminal term_781a6b8f-68da-447e-acb9-c2261321c190 \
  --text "[worker_done] reviewer 완료 — <한 줄 요약>. 상세는 인박스." --enter
```

- 막히면 30분 이상 혼자 헤매지 말고 같은 (2) 방식으로 물어라:
  `orca terminal send --terminal term_781a6b8f-68da-447e-acb9-c2261321c190 --text "[질문] reviewer: <질문>" --enter`
  (`orca orchestration ask` 는 채널이 닫혀 답이 안 닿는 경우가 많다.)
