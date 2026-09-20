# PostgreSQL 담당교체 재전송 영수증 단언 정정

## 1. 역할
기존 PG 워커 재사용. 기존 코드 워크트리 그대로. 제품은 원BE term_c2b0c982-7078-4d5b-b14d-9342eef7f699 소유.

## 2. 대상
본인 test_task_lifecycle_v2_postgres.py의 test_postgres_resending_one_handover_answer_at_once_is_still_one_answer. 현재 {200,400,404,409,422}는 같은답 영수증을 증명하지 못한다. SPEC003 S16 및 기존 assignment replay 보장을 구현자가 미정으로 돌릴 수 없다.

## 3. 수정
같은 정당한 수신자가 같은 담당교체 행에 같은 답을 동시에 보내면 둘 다 200 영수증, 같은 식별자·판단1건·active1·담당행2 유지가 기대다. 반환된 오류를 성공으로 허용하지 않는다. 현재 제품이 실패하면 실패 증거와 정확한 응답을 원BE/코디에게 전달하고 해당 제품은 원BE만 고친다. 응답 권한 검사 보존. 대기 잠금/barrier는 유지하되 인위교착 없음.

## 4. 범위
위 PG 테스트 파일과 v2-postgres-report.md 정정 부록만. 제품/SQL/공통fixture/다른 테스트 무수정. 기존 전체77pass는 당시 증거로 남기되 이 계약 미검증 구멍을 정확히 기록한다. 완료된 다른14묶음을 재검수하지 않는다.

## 5. 검증
동일 격리 ax_test_v2_pg(54329), ax_demo와 구별. make test-postgres PYTEST_ADDOPTS -k resending_one_handover로 변경 한 테스트만 수행. 전량 재실행 금지. stdout/stderr·실제make rc 파일 보존, 수정 후 증거를 이전전체와 구별. 사용자DB/스택 조작 금지.

## 6. 협업
BE에게 이 단언 누락 및 직접 assignment accept receipt 확인을 코디가 요청했다. BE 수정 완료 통지 전이라도 실패를 확인해 전달할 수 있다. 원BE 새 전량 검증과 겹치지 말고 한 테스트만. 새 워커 금지.

## 7. 보고
같은답 응답코드·원장 불변·권한·실행명령과 실제rc. 이유없는 재실행이나 skip/넓은 단언 금지.

## 8. 완료
두 채널 보고 후 idle. 커밋/push/PR 없음. 브라우저E2E 미실행, 전체verify는 코디가 한다.

## 9. 완료 보고 — **문구 변경 금지**

> **⚠ 핸들은 dispatch preamble 의 값을 믿어라.** 아래 명령에 박힌 코디handle 은 **브리프 작성 시점** 값이라 오래됐을 수 있다 — 세션이 재연결되면 핸들이 바뀐다(2026-07-28·29 두 번 겪음). preamble 의 코디네이터 핸들과 아래 값이 다르면 **preamble 이 맞다.** 두 곳에 다 보내지 말고 preamble 쪽으로만 보내라.


- **커밋·push·PR 하지 마라.** 워크트리에 변경만 남긴다. 검증·PR 은 코디네이터가 한다.
- 끝나면 **아래 두 명령을 모두** 실행한다. 하나만 하면 안 된다.

```bash
# (1) 인박스 적재 — 태스크 완료 처리·영구 기록. 코디네이터를 깨우지 않는다.
orca orchestration send \
  --to term_9de388d5-58b1-4bbe-8864-5e930def648b --from term_2e64fd06-507c-460d-accd-2c91b8863dd8 \
  --type worker_done \
  --task-id <이 태스크의 taskId — dispatch 로 받은 context 에 들어 있다> \
  --dispatch-id <이 태스크의 dispatchId — dispatch 로 받은 context 에 들어 있다> \
  --subject "postgres 완료: <한 줄>" \
  --body "변경 파일 목록 / 구현 요약 / 검증 결과(수치) / 계약 준수 / 미결·주의점"

# (2) 직접 주입 — 코디네이터 세션에 유저 메시지로 꽂혀 자동으로 깨운다.
orca terminal send --terminal term_9de388d5-58b1-4bbe-8864-5e930def648b \
  --text "[worker_done] postgres 완료 — <한 줄 요약>. 상세는 인박스." --enter
```

- 막히면 30분 이상 혼자 헤매지 말고 같은 (2) 방식으로 물어라:
  `orca terminal send --terminal term_9de388d5-58b1-4bbe-8864-5e930def648b --text "[질문] postgres: <질문>" --enter`
  (`orca orchestration ask` 는 채널이 닫혀 답이 안 닿는 경우가 많다.)
