# v2 BE·FE 통합 구현 검수

## 1. 역할
기존 리뷰어 재사용 허용. 제품 코드/문서 read-only, 리포트만 쓴다. 코드 워크트리와 SPEC/WORK 경로는 WORK002에 명시된 기존 것을 그대로 쓴다. WORK002·SPEC003·보존된 SPEC001/002가 계약. W1 미커밋 기준은 v2-code-baseline/manifest.json·working-files.zip·tracked.patch. HEAD 차이 전체를 v2 변경이라고 오인하지 말고 baseline↔현재를 비교한다.

## 2. 입력
v2-backend-implementation-report.md·v2-frontend-cancel-reason-report.md·v2-contract-tests-report.md·v2-postgres-report.md의 주장과 실제 diff/테스트를 대조. FE 앞선 정정은 review-v2-frontend-report.md에서 닫혔으므로 이후 취소사유 변경과 BE 연결만 검수. 증거는 v2-frontend-verification/cancel-reason/·v2-contract-verification/·v2-postgres-verification/에서 확인한다. review-v2-work-report.md 재검수1차 R1~3은 브리프·WORK 본문에 반영됨. v2-verification-and-e2e.md는 진행중 인계 틀이며 통과 증거 아님. Phase0 322/976/645/65는 현재 v2 결과 아님.

## 3. 전체 계약 검사
- A1~C2 21건·example10단계와 W1 K1~6/K11가 실제 코드/테스트로 닫혔는지. 명령/유입 REST·MCP·AX·회의·seed 모두. 변경된 테스트가 이전 보장을 삭제/skip/빈단언으로 숨기지 않는지.
- 같은Task 수락, 거절 취소·재요청 새Task/parent/log, 관리자 즉시배정 유지, 첫 지정 pending, 재배정 active1+pending1 원자전환/거절책임보존.
- 재귀중심/직접작업재중첩금지/순환/읽기 자료 모든 표면/건수 누출/읽기와수정권한 분리.
- 완료 원장은 현재유효회차만: report/revision/reopen후 과거승인 무효. open직접완료 자기/관리자 두 경로, request직접완료금지. 외부done+awaiting_review와 서버 명령봉투 일치, 제출상태에 재개 노출 안됨.
- 합의취소/조건변경/재개/목록숨김·복원, expected_version/멱등키/영수증앞권한검사, 잠금/DB유일성/경합/기존index결손재현·SQL두판 동등성.
- 승인 전동작은 OQ203 현행보존, 승격완료확인자 OQ206 미정 명시. 새로운 사용자답이 전달되면 그 확정만 적용. seed미답경로 삭제/승인자동생성 금지.

**키 입력 범위 정정:** SPEC003 §4:747-748 · §5:973-974에 따라 멱등키 필수는 생성/발송만. 새 명령 전부에는 expected_version과 상태가드·권한재검사·중복effect 없음이 요구된다. 새명령 전체에 키가 없다는 이유만으로 결함을 올리지 않는다.

**구현 중 발견한 필수 회귀:** FastAPI 응답모델이 derived/시간/child_progress/child.derived를 잘라내던 결함은 실제 HTTP로 검증한다. 재배정 대기에서 task.assignment가 pending을 현재담당처럼 내지 않는다. 일반 구성원 수신자도 수락/거절할 수 있으나 제3자는 못 답한다. 신규 요청자 조상 읽기권한은 requester_id/promoted_by 본인에 한정하고 CC 등 readable_request_ids 전체로 확장하지 않는다(기존 CC 직접 요청 읽기·다른 독립권한은 보존). 완료보고 하위 reason은 awaiting_approval. my_work에는 요청했다는 이유만으로 타인 업무가 섞이지 않는다.

추가: 요청자 관계 읽기 역량 회수 후 목록/상세/자료가 같은 경계를 쓰는지 확인한다. 승인 후 재개의 시간 비교는 SQLite naive/aware와 PostgreSQL을 모두 고려하고 과거 승인이 다시 유효해지지 않는 회귀가 있어야 한다.

재전송 검수: 새 상태 명령은 원래 expected_version과 같은 본문 그대로 재시도해야 한다. 최신version을 다시 읽어 보내거나 !=200으로 단언한 테스트는 영수증 증거가 아니다. 합의취소로 담당이 ended여도 현재읽기권한 있는 실제 응답자의 같은회차/같은답은 effect없이 영수증, 다른답은 충돌이어야 한다. 현재version/active검사가 영수증 앞을 막지 않는지 확인한다.

추가 확인: 신규 계약 보고서가 직접취소 reason 필수를 미검증으로 남겼다(SPEC003 API/Validation과 현행보존 문구가 함께 있음). 코디는 명시된 사유 필수 계약의 구현 누락으로 판정했고 WORK Execution에 BE·FE 통합 정정을 추가했다. 모든 취소입구 REST/MCP/AX·FE 상세/오늘/캘린더의 공백 거부와 사용자 사유 저장·이력을 검수한다. 취소 권한·미정 정책은 바꾸지 않는다. `GET /api/work-requests/inbox` 생략도 코디가 명시 계약 누락으로 지적해 원BE가 구현 중이다. 기존 동적 경로와 충돌 없이 실제 inbox 응답·권한·inventory가 닫혔는지 검수한다. `v2-contract-tests-report.md` 정정 부록의 숨은 직속 하위 권한 회귀와 정확한 거부 코드도 확인한다.

PG에서 실제 상위 완료↔하위 재개 write skew가 재현됐다. BE 잠금 수정의 fresh 상태 재검사와 complete/approve/reopen 잠금 순서, 테스트가 두 TX를 실제 겹치게 하는지 확인한다. 부모 커밋을 기다린 채 자식 TX를 붙들어 인위 교착을 만들거나 400/404/5xx를 경합 승자로 받아 통과시키지 않는다.

## 4. FE와의 통합 검수
FE 자체 구현은 review-v2-frontend-report.md의 별도 검수와 후속 정정 결과를 입력으로 사용한다. 닫힌 FE 전체 검수를 반복하지 않고, 그 이후 변경과 BE 실물 연결을 확인한다. 특히 started_at·숨김 후 새로고침·비공개 하위 때문에 발생하는 409·외부 done의 승인 상태·제안 봉투와 회차·목록정리의 요청자/종료 상태 가드·합의취소 후 목록정리 종단을 대조한다. viewModels의 optional/string 확장이 BE 불일치를 감추는지 확인한다. 사용자 브라우저 E2E는 별도이며 직접 실행하지 않는다. 선행/후행 관계는 사용자가 현재 v2 완료 후 살피기로 했으므로 이번 범위에 추가하지 않는다.

## 5. allowed_paths
orchestration/work/strong-hajin-work/review-v2-code-report.md 하나만. 다른 코드/문서/DB/사용자프로세스 수정금지. 새 worker발주 금지.

## 6. 결과
PASS/WARN/FAIL, 각 지적 파일:줄·재현가능조건·계약근거·최소수정과 담당 BE/FE. 기존부채와 v2직접위반 분리. 테스트 로그의 수치는 실제 열어 확인하고 아직 코디 make verify가 안돌았으면 그대로 명시한다. 없는 증거는 통과 아님. 비차단 지적을 착수차단으로 부풀리지 않는다. 단 계약누락은 작아보여도 축소하지 않는다.

## 7. 실행
read-only 검수. 기존 테스트 로그/코드 확인, 직접 테스트·DB·빌드·브라우저 실행 없음(코디통합검증과 중복방지). 의심은 관련테스트 위치와 재현방법으로 보고.

## 8. 완료
2채널 완료 후 idle. 원문추적 전수조사 재시작 불필요, 검증대상은 현재 구현 diff다. 커밋 push PR 금지.

## 9. 완료 보고 — **문구 변경 금지**

> **⚠ 핸들은 dispatch preamble 의 값을 믿어라.** 아래 명령에 박힌 코디handle 은 **브리프 작성 시점** 값이라 오래됐을 수 있다 — 세션이 재연결되면 핸들이 바뀐다(2026-07-28·29 두 번 겪음). preamble 의 코디네이터 핸들과 아래 값이 다르면 **preamble 이 맞다.** 두 곳에 다 보내지 말고 preamble 쪽으로만 보내라.


- **커밋·push·PR 하지 마라.** 워크트리에 변경만 남긴다. 검증·PR 은 코디네이터가 한다.
- 끝나면 **아래 두 명령을 모두** 실행한다. 하나만 하면 안 된다.

```bash
# (1) 인박스 적재 — 태스크 완료 처리·영구 기록. 코디네이터를 깨우지 않는다.
orca orchestration send \
  --to term_9de388d5-58b1-4bbe-8864-5e930def648b --from term_6c69a3df-4dd6-4b56-ad9b-52133dd8efbc \
  --type worker_done \
  --task-id <이 태스크의 taskId — dispatch 로 받은 context 에 들어 있다> \
  --dispatch-id <이 태스크의 dispatchId — dispatch 로 받은 context 에 들어 있다> \
  --subject "reviewer 완료: <한 줄>" \
  --body "변경 파일 목록 / 구현 요약 / 검증 결과(수치) / 계약 준수 / 미결·주의점"

# (2) 직접 주입 — 코디네이터 세션에 유저 메시지로 꽂혀 자동으로 깨운다.
orca terminal send --terminal term_9de388d5-58b1-4bbe-8864-5e930def648b \
  --text "[worker_done] reviewer 완료 — <한 줄 요약>. 상세는 인박스." --enter
```

- 막히면 30분 이상 혼자 헤매지 말고 같은 (2) 방식으로 물어라:
  `orca terminal send --terminal term_9de388d5-58b1-4bbe-8864-5e930def648b --text "[질문] reviewer: <질문>" --enter`
  (`orca orchestration ask` 는 채널이 닫혀 답이 안 닿는 경우가 많다.)
