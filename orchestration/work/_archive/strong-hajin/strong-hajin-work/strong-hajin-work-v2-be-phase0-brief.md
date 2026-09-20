# [backend] WORK002 Phase0 읽기전용 관측
## 1. 역할/근거
/Users/kknaks/orca/workspaces/kknaks_profile/strong_hajin/orchestration/roles/strong-hajin/backend/role.md 및 rules/skills/tools/workflow, 코드 AGENTS.md 읽기.
/Users/kknaks/orca/workspaces/kknaks_profile/strong_hajin/para/projects/summer-star/strong-hajin/30-work/work-002-task-lifecycle-v2.md Phase0. WP검수 report /Users/kknaks/orca/workspaces/kknaks_profile/strong_hajin/orchestration/work/strong-hajin-work/review-v2-work-report.md에서 Phase0는 F5중복SELECT 추가로 독립착수 가능 판정. 현재 문서writer가 WP정정중이므로 Phase0 외 단계읽기/구현 금지. 스펙/코드 동시변경이 아니라 독립 readonly 관측만.

## 2. 작업
W1 baseline manifest82파일 sha 현재일치 코디확인했음. HEAD/status만 재확인, 새로운 diff있으면 보고. 코드변경 전 DB관측 U1/U2/U6 및 자료권한 U5 표면목록확인.
로컬 실행DB를 프로젝트설정으로 식별하고 READ ONLY transaction SELECT로 information_schema/pg_indexes/pg_constraint를 확인한다. 운영/공유DB쓰기는없음. 스키마/인덱스 실재와 ORM차이, assigned행 집계, 정상done요청 승인판단행 매핑 확인 및 예외행 개수, tasks.source_work_request_id 중복집계. 민감본문/자격증명 출력금지, 행 ID·건수·스키마만 필요최소.
F5 추가: SELECT source_work_request_id,count(*) FROM tasks WHERE source_work_request_id IS NOT NULL GROUP BY 1 HAVING count(*)>1. uq_tasks_source_work_request 및 active담당unique의 validity/predicate까지 읽는다.
접속불가면 로컬docker 상태/포트 read-only 조사 후 정확한 막힘만 보고, DB생성/리셋/DDL/스택재시작하지 말 것. 격리DB 준비는 다음 Phase1에서.
자료 read/list/search/preview/download 판정의 공통경로/누락을 코드로 확인. API/MCP/AX 생성입구도 현재코드 실물 목록화, 과거스펙 관측을 검증했다고 복제하지 말 것.

## 3. 검증
현재코드는 baseline과 동일하므로 과거W1 tests 재실행금지. 이번은 SELECT/읽기증거만. test/빌드0. 다음구현용 실행환경(Node20/PG포트/Make targets) 확인만. 비밀번호/토큰 출력 금지.

## 4. allowed_paths
쓰기 하나: /Users/kknaks/orca/workspaces/kknaks_profile/strong_hajin/orchestration/work/strong-hajin-work/v2-be-phase0-report.md
코드/문서/DB 전부읽기전용. temporary 분석스크립트가 필요하면 프로세스stdin 사용. 마이그레이션/코드/테스트작성은 후속발주에서.

## 5. 결과
관측 항목별 했다/못했다/건수/코드경로/스키마差. 다음Phase1의 적용전조건, 실제사용자결정 필요한 데이터예외만 보고. 예외0추정금지. 짧게 쓰고 완료.
## 6. 금지
코드/DB변경/테스트/빌드/commit/push/PR/stash/reset/checkout 없음. WP작성자와 공유쓰기없음.
## 7. 범위
독립 Phase0만, 후속구현 소유권은 다음발주로 넘김.
## 8. 완료
보고서 작성 후 2채널 완료, 후속발주대기.
## 9. 완료 보고 — **문구 변경 금지**

> **⚠ 핸들은 dispatch preamble 의 값을 믿어라.** 아래 명령에 박힌 코디handle 은 **브리프 작성 시점** 값이라 오래됐을 수 있다 — 세션이 재연결되면 핸들이 바뀐다(2026-07-28·29 두 번 겪음). preamble 의 코디네이터 핸들과 아래 값이 다르면 **preamble 이 맞다.** 두 곳에 다 보내지 말고 preamble 쪽으로만 보내라.


- **커밋·push·PR 하지 마라.** 워크트리에 변경만 남긴다. 검증·PR 은 코디네이터가 한다.
- 끝나면 **아래 두 명령을 모두** 실행한다. 하나만 하면 안 된다.

```bash
# (1) 인박스 적재 — 태스크 완료 처리·영구 기록. 코디네이터를 깨우지 않는다.
orca orchestration send \
  --to term_9de388d5-58b1-4bbe-8864-5e930def648b --from term_c2b0c982-7078-4d5b-b14d-9342eef7f699 \
  --type worker_done \
  --task-id <이 태스크의 taskId — dispatch 로 받은 context 에 들어 있다> \
  --dispatch-id <이 태스크의 dispatchId — dispatch 로 받은 context 에 들어 있다> \
  --subject "backend 완료: <한 줄>" \
  --body "변경 파일 목록 / 구현 요약 / 검증 결과(수치) / 계약 준수 / 미결·주의점"

# (2) 직접 주입 — 코디네이터 세션에 유저 메시지로 꽂혀 자동으로 깨운다.
orca terminal send --terminal term_9de388d5-58b1-4bbe-8864-5e930def648b \
  --text "[worker_done] backend 완료 — <한 줄 요약>. 상세는 인박스." --enter
```

- 막히면 30분 이상 혼자 헤매지 말고 같은 (2) 방식으로 물어라:
  `orca terminal send --terminal term_9de388d5-58b1-4bbe-8864-5e930def648b --text "[질문] backend: <질문>" --enter`
  (`orca orchestration ask` 는 채널이 닫혀 답이 안 닿는 경우가 많다.)
