# [reviewer] W1 BE+FE 통합 코드 검수

역할: /Users/kknaks/orca/workspaces/kknaks_profile/strong_hajin/orchestration/roles/strong-hajin/reviewer/role.md 및 rules/tools/workflow 읽기. 이번은 backend+frontend 코드 리뷰 모드.
코드 워크트리: /Users/kknaks/orca/workspaces/Strong_hajin/strong-hajin-work. base origin/main.

## 1. SSOT
/Users/kknaks/orca/workspaces/kknaks_profile/strong_hajin/para/projects/summer-star/strong-hajin/30-work/work-001-task-creation.md
같은 제품의 SPEC-001 v0.2.4, SPEC-002, DEC-001.
/Users/kknaks/orca/workspaces/kknaks_profile/strong_hajin/orchestration/work/strong-hajin-work/w1-fe-api-clarification.md 및 w1-acceptance-test-clarification.md.
/Users/kknaks/orca/workspaces/kknaks_profile/strong_hajin/orchestration/work/strong-hajin-work/backend-report.md, frontend-report.md.

## 2. 목적
W1 실제 코드가 승인 계약을 만족하는지 BE/FE 통합 검수. diff와 신규 파일을 직접 읽고 인수조건별 근거, FAIL/WARN/PASS.

## 3. 검수 계약
생성 3경로, 즉시 active/assigned, 권한과 후보 일치, source_work_request_id/완료 승인 보존, actor 기록, REST/MCP/AX/회의/seed 정렬, 영수증 권한·payload 지문·원자성·DB unique·동시 승격, FE retry key/route와 목록 갱신. API 명칭/필드는 clarification의 W1 slice 기준.

## 4. 집중 확인
- tests/conftest.py가 키를 자동 삽입하며 누락/공백 필수 검증을 가리는지, 실제 HTTP/MCP 실패 경계가 테스트되는지.
- 코디는 과거 모양 fixture 신규 도입 없이 수락 회차 전용 테스트 대체를 지시했는데 tests/legacy_acceptance.py가 추가됐다. 구현을 검증하는 대신 테스트가 상태/회차를 조작해 회귀를 숨기는지 구체적으로 판정. 폐기/대체 테스트 대응표가 충분한지.
- report의 actor=담당자 잔존이 실제 생성 행위자/권한/감사 계약 위반인지.
- report의 meeting.followup.task/request AX action AttributeError가 이번 W1 경로인지, 기존 부채라는 주장만으로 범위 제외가 가능한지 실제 호출 연결 확인.
- horizontal 경로가 start_date/parent/project를 거부한다는 구현과 FE 생성 필드가 맞는지. 받았다 버리는 필드·응답 shape 불일치 확인.
- 새 assigned에서 수락 회차 전용 명령은 side effect 없는 4xx, 자료/완료근거는 보존. 신규 테스트가 단언을 줄여 거짓 green을 만드는지.
- BE가 공유 트리 stash를 썼으므로 FE 13개 변경과 사용자 definition.md/lifecycle.md/docs/work-code-db-audit-* 보존 여부도 읽기로 확인.

## 5. allowed_paths
/Users/kknaks/orca/workspaces/kknaks_profile/strong_hajin/orchestration/work/strong-hajin-work/review-code-report.md 한 파일만 작성. 코드/문서 수정 금지. 제품 README/docs/inventory는 BE가 별도 동기화 중이니 코드부터 검수하고 이 파일들은 완료 시 최종본 확인. 사용자 audit 파일은 이번 산출물 아님.

## 6. 산출물
위반별 파일:줄+계약 근거, 우선순위, 수정 방향. 실제 버그와 기존 부채 구분. 보고 수치만 믿지 말고 소스 확인. 전체 재설계 제안 금지.

## 7. 제약
테스트/빌드/DB/E2E 실행 금지. stash/checkout/reset 금지. 커밋/push/PR 없음.

## 8. 검증 분담
실행 검증은 코디. E2E는 사용자. 아직 전체 make verify 미통과(워커 전체 test에 inventory3+타이밍2 실패 보고). 검수 통과를 실행 테스트 통과로 쓰지 않는다.

## 9. 완료 보고 — **문구 변경 금지**

> **⚠ 핸들은 dispatch preamble 의 값을 믿어라.** 아래 명령에 박힌 코디handle 은 **브리프 작성 시점** 값이라 오래됐을 수 있다 — 세션이 재연결되면 핸들이 바뀐다(2026-07-28·29 두 번 겪음). preamble 의 코디네이터 핸들과 아래 값이 다르면 **preamble 이 맞다.** 두 곳에 다 보내지 말고 preamble 쪽으로만 보내라.


- **커밋·push·PR 하지 마라.** 워크트리에 변경만 남긴다. 검증·PR 은 코디네이터가 한다.
- 끝나면 **아래 두 명령을 모두** 실행한다. 하나만 하면 안 된다.

```bash
# (1) 인박스 적재 — 태스크 완료 처리·영구 기록. 코디네이터를 깨우지 않는다.
orca orchestration send \
  --to term_cc49c5dc-4e7a-4c27-b387-a37d1752fed4 --from term_fd9e957e-c7d0-4e8e-a59c-c14c600da674 \
  --type worker_done \
  --task-id <이 태스크의 taskId — dispatch 로 받은 context 에 들어 있다> \
  --dispatch-id <이 태스크의 dispatchId — dispatch 로 받은 context 에 들어 있다> \
  --subject "reviewer 완료: <한 줄>" \
  --body "변경 파일 목록 / 구현 요약 / 검증 결과(수치) / 계약 준수 / 미결·주의점"

# (2) 직접 주입 — 코디네이터 세션에 유저 메시지로 꽂혀 자동으로 깨운다.
orca terminal send --terminal term_cc49c5dc-4e7a-4c27-b387-a37d1752fed4 \
  --text "[worker_done] reviewer 완료 — <한 줄 요약>. 상세는 인박스." --enter
```

- 막히면 30분 이상 혼자 헤매지 말고 같은 (2) 방식으로 물어라:
  `orca terminal send --terminal term_cc49c5dc-4e7a-4c27-b387-a37d1752fed4 --text "[질문] reviewer: <질문>" --enter`
  (`orca orchestration ask` 는 채널이 닫혀 답이 안 닿는 경우가 많다.)
