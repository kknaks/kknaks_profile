# [backend] W1 통합 리뷰 수정 1차

## 1. SSOT
기존 W1 브리프·WORK-001·SPEC 및 /Users/kknaks/orca/workspaces/kknaks_profile/strong_hajin/orchestration/work/strong-hajin-work/review-code-report.md 전체. w1-fe-api-clarification.md와 w1-acceptance-test-clarification.md 유지.

## 2. 목적
F-1 및 W-1~7 중 소유 항목을 수정하고 근거 있는 회귀 검증을 남긴다.

## 3. 계약
horizontal은 현재 start_date/parent/project를 지원하지 않는 계약을 유지한다. self/managed 기존 지원은 보존. 자료/출처/actor를 조용히 버리지 않는다. API 공개 shape/도구 schema를 임의 변경하지 않는다.

## 4. 담당 지적
F-1 BE: horizontal start_date/parent_task_id/project_id 각각 명시 422 + task/원장/출처 부수효과 없음 테스트 추가.
W-1: AX로 생성된 horizontal 업무에 source_action_item/decision_item/submission/review_decision 계보를 실제 요청→업무 생성까지 전달·보존한다. 사용자에게 열어 둔 AX 담당 지정 기능을 거절로 축소하지 않는다. 확인 전 effect0/확인 후 계보/replay 검증.
W-2: 신규 즉시 생성의 created_by_actor_id 및 최초 history actor를 실제 생성 명령 행위자로 기록한다. 단순히 전부 requester로 치환해 과거 수락/회의 승격 actor를 오염시키지 말고 실제 caller를 전달한다. 권한 회귀/열람 및 기존 legacy 수락 의미 보존 테스트.
W-3~6: README 권한을 명령별로 정확히 구분, domain-model AX 살아 있는 경로 분리, 없는 회의 route/table은 실제 todo 경로/잠금으로 정정. 신규 assigned에는 수락회차 evidence가 없고 업무 자료 기능은 남는다는 경계를 정확히 기술(참조 API/권한 실재 확인).
W-7: 수정 테스트의 잡음 공백 복원, SAVEPOINT 모순 주석/command_kind 오기 정정, no-op accept 응답 단언 또는 제거, 403/404/422 넓은 집합을 정확한 계약으로 고정, 4 REST/MCP 생성 도구별 누락/공백 키 거부 누락 커버. 유효한 기존 테스트 의미 보존.

## 5. allowed_paths
backend/ 및 README.md, docs/domain-model.md, docs/unified-operations.md만. frontend 사용자 파일 무수정. inventory 변경 필요하면 정확한 diff 보고.

## 6. 통합 테스트 실패 조사
코디 make verify 로그 verify-2026-09-16.log: 1289 passed, material_worker_recovery의 heartbeat/timeout 2건 실패. 기존 실패라고 묻지 말고 제품 race인지 fixture 시간 의존인지 원인을 좁혀 보고. 근거 있는 최소 수정은 가능하되 sleep 늘리기/단언 약화/skip으로 덮지 않는다. 큰 무관 구조 변경은 하지 않고 근거 보고. baseline 실험은 공유 트리 stash 없이 git show 등 읽기 전용 방법만.

## 7. 제약
legacy fixture는 리뷰에서 단언 보존을 확인했으므로 현재 것은 유지 승인. 신규 확대 불필요. 공유 트리 stash/checkout/reset 절대 금지. E2E 사용자 담당, 사용자 DB ax_demo 무접촉. 커밋/push/PR 없음.

## 8. 검증
Makefile 타겟 기반 변경 관련 unit/contract/격리 PG 검증. 전량 make verify는 수정 완료 후 코디가 실행. FE 테스트와 겹쳐 부하를 만들지 않게 테스트 시작 전 코디에 알린다. 지적별 수정/테스트/남은 항목을 보고하고 보고서는 scratchpad에 남겨 경로 전달.

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
