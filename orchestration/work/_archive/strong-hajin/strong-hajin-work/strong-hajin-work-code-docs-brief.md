# [backend] W1 operation inventory·제품 문서 동기화

## 1. SSOT
기존 BE 브리프, WORK-001 Phase8, backend-report.md §4. 제품 코드 변경 금지.

## 2. 목적
API inventory drift와 실제 제품 문서의 수락 전제를 정렬한다.

## 3. 계약
새 동작을 기술하고 과거 행·담당자 변경·완료 승인·AX 실행 확인을 수락 gate 제거와 혼동하지 않는다. 실행하지 않은 테스트 완료 주장은 하지 않는다.

## 4. 읽을 것
README.md, docs/domain-model.md, docs/unified-operations.md를 실제로 읽고 필요한 자리만 수정. 보고서 대체 문장은 추정이므로 무조건 적용하지 않는다.

## 5. allowed_paths
README.md, docs/domain-model.md, docs/unified-operations.md, docs/unified-operations-inventory.json만.

## 6. 작업
scratchpad/inventory 갱신본과 현재 inventory를 비교해 관련 diff만 반영한다. 제품 문서를 실제 코드 동작과 정렬한다. 기존 사용자 docs/work-code-db-audit-*는 읽기 전용.

## 7. 제약
공유 트리에서 stash/checkout/reset으로 기준선 비교 절대 금지. 다른 워커/사용자 파일 변경 금지. 커밋/push/PR 금지. E2E 사용자 담당. tests/legacy_acceptance.py 추가는 앞 지시와 다르므로 검토 중, 추가 확대하지 않는다.

## 8. 검증
JSON 파싱·git diff --check. 테스트는 코디가 통합 실행하므로 중복 실행하지 않는다. 실제 바꾼 문장·파일·범위 보고.

## 9. 완료 보고 — **문구 변경 금지**

> **⚠ 핸들은 dispatch preamble 의 값을 믿어라.** 아래 명령에 박힌 코디handle 은 **브리프 작성 시점** 값이라 오래됐을 수 있다 — 세션이 재연결되면 핸들이 바뀐다(2026-07-28·29 두 번 겪음). preamble 의 코디네이터 핸들과 아래 값이 다르면 **preamble 이 맞다.** 두 곳에 다 보내지 말고 preamble 쪽으로만 보내라.


- **커밋·push·PR 하지 마라.** 워크트리에 변경만 남긴다. 검증·PR 은 코디네이터가 한다.
- 끝나면 **아래 두 명령을 모두** 실행한다. 하나만 하면 안 된다.

```bash
# (1) 인박스 적재 — 태스크 완료 처리·영구 기록. 코디네이터를 깨우지 않는다.
orca orchestration send \
  --to term_cc49c5dc-4e7a-4c27-b387-a37d1752fed4 --from term_963b7fe7-7f52-49f4-af62-63c8100a091c \
  --type worker_done \
  --task-id <이 태스크의 taskId — dispatch 로 받은 context 에 들어 있다> \
  --dispatch-id <이 태스크의 dispatchId — dispatch 로 받은 context 에 들어 있다> \
  --subject "backend 완료: <한 줄>" \
  --body "변경 파일 목록 / 구현 요약 / 검증 결과(수치) / 계약 준수 / 미결·주의점"

# (2) 직접 주입 — 코디네이터 세션에 유저 메시지로 꽂혀 자동으로 깨운다.
orca terminal send --terminal term_cc49c5dc-4e7a-4c27-b387-a37d1752fed4 \
  --text "[worker_done] backend 완료 — <한 줄 요약>. 상세는 인박스." --enter
```

- 막히면 30분 이상 혼자 헤매지 말고 같은 (2) 방식으로 물어라:
  `orca terminal send --terminal term_cc49c5dc-4e7a-4c27-b387-a37d1752fed4 --text "[질문] backend: <질문>" --enter`
  (`orca orchestration ask` 는 채널이 닫혀 답이 안 닿는 경우가 많다.)
