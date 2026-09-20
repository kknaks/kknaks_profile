# [frontend] W1 통합 리뷰 수정 1차

## 1. SSOT
기존 W1 브리프·WORK-001·SPEC 및 /Users/kknaks/orca/workspaces/kknaks_profile/strong_hajin/orchestration/work/strong-hajin-work/review-code-report.md 전체. w1-fe-api-clarification.md와 w1-acceptance-test-clarification.md 유지.

## 2. 목적
F-1 및 W-1~7 중 소유 항목을 수정하고 근거 있는 회귀 검증을 남긴다.

## 3. 계약
horizontal은 현재 start_date/parent/project를 지원하지 않는 계약을 유지한다. self/managed 기존 지원은 보존. 자료/출처/actor를 조용히 버리지 않는다. API 공개 shape/도구 schema를 임의 변경하지 않는다.

## 4. 담당 지적
F-1: horizontal 대상에서는 시작일 입력을 노출하지 않고 payload에도 보내지 않는다. self에서 시작일을 입력한 뒤 horizontal로 담당을 바꾸는 전환도 처리한다. 입력 값이 해당 경로에 적용되지 않음을 사용자가 이해하게 하고, 숨긴 날짜가 새 의도 지문/전송에 섞이지 않게 한다. self/managed로 돌아갈 때 지원 날짜 동작은 보존. 재시도 키/경로 고정 계약 유지.

## 5. allowed_paths
frontend/만. backend와 docs는 다른 워커 소유.

## 6. 구현/회귀
시작일을 먼저 입력→수신 후보 선택→입력 미노출+payload start_date 없음+생성 성공을 테스트. self/managed start_date는 전달됨도 확인. 제출 중/실패 재시도/담당 전환 회귀.

## 7. 제약
공유 트리 stash/checkout/reset 금지. 사용자 파일 보존. E2E 사용자 담당. 커밋/push/PR 금지.

## 8. 검증
make frontend-test 및 tsc. BE 부하와 겹치면 좁은 테스트는 먼저 확인하고 전량은 코디 통합으로 넘겨도 됨. 검사 못한 것은 명시. 실행은 Makefile 준수, 전체 make verify 중복 금지.

## 9. 완료 보고 — **문구 변경 금지**

> **⚠ 핸들은 dispatch preamble 의 값을 믿어라.** 아래 명령에 박힌 코디handle 은 **브리프 작성 시점** 값이라 오래됐을 수 있다 — 세션이 재연결되면 핸들이 바뀐다(2026-07-28·29 두 번 겪음). preamble 의 코디네이터 핸들과 아래 값이 다르면 **preamble 이 맞다.** 두 곳에 다 보내지 말고 preamble 쪽으로만 보내라.


- **커밋·push·PR 하지 마라.** 워크트리에 변경만 남긴다. 검증·PR 은 코디네이터가 한다.
- 끝나면 **아래 두 명령을 모두** 실행한다. 하나만 하면 안 된다.

```bash
# (1) 인박스 적재 — 태스크 완료 처리·영구 기록. 코디네이터를 깨우지 않는다.
orca orchestration send \
  --to term_cc49c5dc-4e7a-4c27-b387-a37d1752fed4 --from term_dc53067e-a706-45f8-91b5-7314241fc3be \
  --type worker_done \
  --task-id <이 태스크의 taskId — dispatch 로 받은 context 에 들어 있다> \
  --dispatch-id <이 태스크의 dispatchId — dispatch 로 받은 context 에 들어 있다> \
  --subject "frontend 완료: <한 줄>" \
  --body "변경 파일 목록 / 구현 요약 / 검증 결과(수치) / 계약 준수 / 미결·주의점"

# (2) 직접 주입 — 코디네이터 세션에 유저 메시지로 꽂혀 자동으로 깨운다.
orca terminal send --terminal term_cc49c5dc-4e7a-4c27-b387-a37d1752fed4 \
  --text "[worker_done] frontend 완료 — <한 줄 요약>. 상세는 인박스." --enter
```

- 막히면 30분 이상 혼자 헤매지 말고 같은 (2) 방식으로 물어라:
  `orca terminal send --terminal term_cc49c5dc-4e7a-4c27-b387-a37d1752fed4 --text "[질문] frontend: <질문>" --enter`
  (`orca orchestration ask` 는 채널이 닫혀 답이 안 닿는 경우가 많다.)
