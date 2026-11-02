# [frontend] W1 frontend-test 정상 종료 검증

## 1. SSOT
기존 W1 FE 브리프·WORK-001과 w1-fe-api-clarification.md 그대로. 원래 역할 규칙 유지.

## 2. 목적
638 tests가 통과해도 make frontend-test exit 1이면 검증 완료가 아니다. MyWorkPage.test.tsx dragStart가 dataTransfer 없이 호출되는 최소 fixture 문제인지 확인하고 정상 드래그 이벤트로 고친다.

## 3. 계약
제품 동작/단언 유지. 테스트 오류 무시, unhandled error 필터, skip, 성공 exit 강제 금지. 실제 드래그 drop 전이 단언이 살아 있어야 한다.

## 4. 핵심 파일
frontend/src/features/work/MyWorkPage.test.tsx:461, WorkViews.tsx:542. HEAD에서도 같은 실패였다는 기존 실험의 명령/결과 증거를 보고한다. 공유 트리 파일을 HEAD로 덮는 기준선 실험은 하지 않는다.

## 5. allowed_paths
frontend/src/features/work/MyWorkPage.test.tsx만. 다른 수정이 필요하면 근거 보고. BE는 같은 트리에서 작업 중.

## 6. 구현
jsdom 드래그 fixture를 실제 이벤트에 필요한 dataTransfer와 함께 구성하고 기존 드래그 결과를 검증한다. 근본 원인이 다르면 덮지 말고 보고한다.

## 7. 제약
E2E 사용자 담당. 커밋/push/PR 금지. 테스트가 실제 제품 버그를 드러내면 숨기지 않는다.

## 8. 검증
make frontend-test exit 0 확인. 전건 통과 수·unhandled error 0·exit code와 최소 diff를 보고한다. 이 완료로 W1 전체가 끝났다고 주장하지 않는다.

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
