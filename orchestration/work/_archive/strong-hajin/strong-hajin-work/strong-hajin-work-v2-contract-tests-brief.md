# WORK002 v2 신규 계약·종단 회귀 테스트 분담

## 1. 역할·위치
너는 신규 백엔드 계약 테스트 담당이다. 제품 코드는 원BE가 수정 중이다. 동일 코드 워크트리 /Users/kknaks/orca/workspaces/Strong_hajin/strong-hajin-work 에서 신규 테스트 2파일만 작성한다. 새 워크트리/브랜치/커밋/push 금지.
원BE term_c2b0c982-7078-4d5b-b14d-9342eef7f699 에 해당 두 파일 소유 이전을 통지했다. 소유 충돌 발견 시 쓰기 전에 코디에게 알린다.

## 2. 입력
코드 AGENTS.md와 /Users/kknaks/orca/workspaces/kknaks_profile/strong_hajin/para/projects/summer-star/strong-hajin/30-work/work-002-task-lifecycle-v2.md(Phase8·Case Matrix), 같은 제품 20-spec/spec-003-task-lifecycle-v2.md(§4~6), reference 원문은 docs /Users/kknaks/orca/workspaces/kknaks_profile/strong_hajin/reference/2026-09-10-sc-meeting/example.md §10.
기존 tests/conftest.py·계약 테스트 헬퍼·실제 HTTP/facade 입력을 읽고 사용한다. 코드와 테스트 일치만을 통과 근거로 삼지 말고 위 계약을 검증한다. 기존 원문 추적표를 다시 쓰지 않는다.

## 3. 맡은 것
WORK A1~C2 21건 및 example 10단계 연속 흐름을 신규 backend/tests/contract/test_task_lifecycle_v2.py 로 검증한다. 필요하면 같은 폴더 test_task_lifecycle_v2_support.py 에 도우미를 둔다. SQLite 기반 기존 계약 테스트 fixture 이용, 외부 DB/서비스/브라우저 실행 금지. PG 경합/인덱스는 원BE 소유이며 이 파일에서 통과로 주장하지 않는다.
명령 경로로 데이터를 만들고 effect·상태·권한·투영·이력을 함께 단언한다. 실제 계약 입구를 우회해 private helper만 부르는 테스트로 종단을 대체하지 않는다. W1 K1~6/K11 중 신규 코드가 바꾸는 보장도 함께 덮는다. 이미 기존 테스트가 정확히 덮는 단순 항목은 보고서에 파일/테스트 이름으로 연결하고 중복하지 않아도 된다.

## 4. 핵심 검증
- 발송시 Task 생성/pending, 수락해도 같은 task_id·parent 유지, 거절시 취소·이력 보존·재요청 새 id·supersedes.
- 본인 open→done 허용, 요청 직접완료 금지, 관리자 즉시배정 보존.
- 재배정 active+pending 책임 유지, 수락 원자교체, 거절 기존담당 유지.
- 재귀 하위/같은사람 직접작업 재중첩금지/순환, 요청자 하위자료 접근과 다른일 배제.
- 완료보고는 외부 done+approval.awaiting_review, 유효한 현재회차 승인만 완결, 보완/재개 이후 과거승인 재사용 금지. 숨은 하위가 있어도 완료게이트는 막지만 오류는 title/id/건수를 누출하지 않음.
- 제안 전 effect 없음, terms_change 필드 적용, 합의취소 request.cancelled_by_agreement/task.cancelled/assignment.ended → 요청자 목록정리 → include_removed 숨김표시 → 상세·이력 열림.
- 목록정리는 요청자만/종료된 요청만, 수신자403·진행중409.
- expected_version 필수·중복effect 없음, 키는 생성/발송만 필수(새 상태 명령에 없는 키를 요구하지 말 것), 영수증 반환 전 읽기권한 재검사.
- children GET API(원BE 연결 중)·상세 children은 직속이며 derived/approval 실림, accepted_at/started_at 분리, REST/MCP/AX 권한 일치 및 확인 전 effect 없음.

## 5. 미정·경계
OQ203 미답: 미완결 하위가 있어도 완료보고는 현행 허용, 최종승인은 차단. 새 정책 확정이라고 적지 않는다. OQ206 system:meeting 완료확인자 미답: 임의지정/자동승인 금지, 그 좁은 경로는 미결로 명시하고 예시의 일반 요청자 흐름을 검증한다. 사용자 E2E 미실행. 선행/후행 강제는 후속범위, 추가하지 않는다. reply/status_note는 없는 원장이므로 null 정상. child_progress.blocking은 보이는 하위만 세므로 0이 완료 허용을 보장하지 않는다.

## 6. 허용 파일
backend/tests/contract/test_task_lifecycle_v2.py
backend/tests/contract/test_task_lifecycle_v2_support.py
/Users/kknaks/orca/workspaces/kknaks_profile/strong_hajin/orchestration/work/strong-hajin-work/v2-contract-tests-report.md
이 셋뿐. 기존 테스트/conftest/제품코드/Makefile/FE/스펙 수정 금지. 코드를 고쳐야 하는 실패는 코디와 원BE에게 재현명령·실제오류·계약근거를 즉시 메시지로 보내고 독립 테스트를 계속 작성한다. 다른 워커가 쓰는 실패를 기대값 약화/skip/xfail로 덮지 않는다.

## 7. 실행
Makefile만 사용. PYTEST_ADDOPTS='-k lifecycle_v2 ...' 처럼 신규 파일/테스트 이름에 한정하여 make test-contract. test_* 이름에 lifecycle_v2 를 넣거나 -k 파일명을 정확히 사용. PYTEST_XDIST_AUTO_NUM_WORKERS=4. 직접 uv run pytest 금지, 전체 스위트/verify/PG/빌드 실행금지. 전체 stdout/stderr와 실제exit 보존, 제품 수정 중 실패와 완료테스트 구분. 새 테스트가 제품버그를 잡으면 짧게 보고하고 원BE 수정 후 해당 묶음만 재확인한다.

## 8. 완료
A1~C2/예시10단계/관련K 회귀별 테스트 이름·결과·미검증 항목 표를 리포트에 남긴다. 신규 회귀가 모두 의미있게 통과하고 제품 결함은 원BE 수정 확인 후 완료 보고한다. 사용자 미결은 그대로 표시. 새 워커 발주 금지.

## 9. 완료 보고 — **문구 변경 금지**

> **⚠ 핸들은 dispatch preamble 의 값을 믿어라.** 아래 명령에 박힌 코디handle 은 **브리프 작성 시점** 값이라 오래됐을 수 있다 — 세션이 재연결되면 핸들이 바뀐다(2026-07-28·29 두 번 겪음). preamble 의 코디네이터 핸들과 아래 값이 다르면 **preamble 이 맞다.** 두 곳에 다 보내지 말고 preamble 쪽으로만 보내라.


- **커밋·push·PR 하지 마라.** 워크트리에 변경만 남긴다. 검증·PR 은 코디네이터가 한다.
- 끝나면 **아래 두 명령을 모두** 실행한다. 하나만 하면 안 된다.

```bash
# (1) 인박스 적재 — 태스크 완료 처리·영구 기록. 코디네이터를 깨우지 않는다.
orca orchestration send \
  --to term_9de388d5-58b1-4bbe-8864-5e930def648b --from term_84ab1149-5aef-4981-aa60-2c48e3be004c \
  --type worker_done \
  --task-id <이 태스크의 taskId — dispatch 로 받은 context 에 들어 있다> \
  --dispatch-id <이 태스크의 dispatchId — dispatch 로 받은 context 에 들어 있다> \
  --subject "contract-tests 완료: <한 줄>" \
  --body "변경 파일 목록 / 구현 요약 / 검증 결과(수치) / 계약 준수 / 미결·주의점"

# (2) 직접 주입 — 코디네이터 세션에 유저 메시지로 꽂혀 자동으로 깨운다.
orca terminal send --terminal term_9de388d5-58b1-4bbe-8864-5e930def648b \
  --text "[worker_done] contract-tests 완료 — <한 줄 요약>. 상세는 인박스." --enter
```

- 막히면 30분 이상 혼자 헤매지 말고 같은 (2) 방식으로 물어라:
  `orca terminal send --terminal term_9de388d5-58b1-4bbe-8864-5e930def648b --text "[질문] contract-tests: <질문>" --enter`
  (`orca orchestration ask` 는 채널이 닫혀 답이 안 닿는 경우가 많다.)
