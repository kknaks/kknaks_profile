# [backend] 코드 재검수 잔여 R-1~4 최소 정정

## 1. SSOT
review-code-report.md 재검수(1차), 기존 W1 계약.
## 2. 목적
남은 문서 사실 오류와 변경 경계 회귀 가드를 닫는다. 제품 기능 확장 없음.
## 3. 계약
R-1: README116/domain-model53은 요청/배정 경로별 실제 422/403/404를 구분한다. 요청 코드가 404로 동작한다고 꾸미지 않는다. 코드의 기존 오류 계약 변경 금지.
## 4. 대상
R-2 회의 후속 승격 생성 actor/history=실제 누른 사람 테스트, R-3 활성 담당 부재 시 caller 기반 fallback 열람 경계(요청자/전담당자/무관한 사람) 테스트, R-4 test_task_actor.py 낡은 pending 주석 정정. 검증으로 실제 제품 회귀 발견시 보고.
## 5. allowed_paths
README.md, docs/domain-model.md, backend/tests/contract/test_task_actor.py, backend/tests/contract/test_meeting_finalize.py, backend/tests/contract/test_task_creation_contract.py만.
## 6. 범위
최소 diff. legacy fixture 확대 없음. 자료 worker의 기존 타이밍 테스트/Makefile/제품 코드는 이번 수정에서 건드리지 않는다. 병렬4 완화의 한계는 인수인계 기록으로 남기며 직렬화도 외부 CPU 부하에 대한 시간 보장 자체를 만들지는 않는다.
## 7. 제약
공유 트리 stash/checkout/reset 금지. E2E 사용자 담당. 커밋/push/PR 없음.
## 8. 검증
수정 테스트만 Makefile target+PYTEST_ADDOPTS 등 지원되는 필터로 실행. 전체 contract/verify 반복 불필요. 명령/exit/수치 보고. 문서 두 문장이 실코드 분기와 일치하는지 확인.

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
