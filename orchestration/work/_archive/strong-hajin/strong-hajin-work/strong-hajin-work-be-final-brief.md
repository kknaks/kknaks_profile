# [backend] WORK-003 Phase 1~3 구현 — 참조 읽음·프로젝트 선행업무·업무 결재자

## 1. 역할과 작업 위치
너는 strong-hajin-work 백엔드 구현 워커다. 코디네이터 handle은 현재 dispatch preamble의 값을 따른다. 코드 워크트리는 `/Users/kknaks/orca/workspaces/Strong_hajin/strong-hajin-work`이며 공유 트리다. 기존 변경을 reset/stash/checkout 하지 말고 이어서 구현한다. 문서 레포 `para/`와 frontend는 수정하지 않는다.

먼저 코드 레포 AGENTS.md와 관련 역할 문서를 읽고, 다음 SSOT를 읽는다.
- `/Users/kknaks/orca/workspaces/kknaks_profile/strong_hajin/para/projects/summer-star/strong-hajin/20-spec/spec-001-work-management.md`
- `/Users/kknaks/orca/workspaces/kknaks_profile/strong_hajin/para/projects/summer-star/strong-hajin/30-work/work-003-inbox-predecessor-and-create-frame.md`
- `/Users/kknaks/orca/workspaces/kknaks_profile/strong_hajin/para/projects/summer-star/strong-hajin/10-decision/decision-001-work-page.md`

## 2. 목표
WORK-003 Phase 1~3을 실제 코드로 구현한다.

### Phase 1 — 참조 CC 수신함 읽음
- `work_request_read_receipts` 모델 metadata와 `(work_request_id, member_id)` 유일성을 추가한다. 스키마 SoT는 모델 metadata이며 migration/backfill/startup DDL은 만들지 않는다.
- CC 참조자만 읽음 명령을 실행할 수 있다. 읽을 수 없으면 404, CC가 아니면 403. 명령은 멱등이고 request version/state/CC 관계를 변경하지 않는다.
- 수신함 `reference` 갈래에만 미읽음 필터를 적용한다. `work` 갈래, 참조 업무 탭/요청 목록, 일반 업무 조회에는 필터를 적용하지 않는다.
- REST 수신함/읽음 라우트, MCP 수신함 projection을 같은 projection으로 맞춘다. MCP/AX에 읽음 명령을 노출하지 않는다. MCP 설명의 처리 완료 항목 문구도 계약에 맞춘다.
- 동시 두 번 읽음은 한 행으로 수렴해야 한다.

### Phase 2 — 프로젝트 선행업무와 시작 게이트
- `task_predecessors` 모델 metadata, 활성 관계 부분 unique, 자기참조 CHECK를 추가한다.
- 생성 공통 payload와 수정 payload의 `preceding_task_ids`를 구현한다. 수정에서 필드 생략은 유지, 빈 배열은 전체 해제, 변경은 전체 교체다.
- 프로젝트 미선택/불일치, 자기 자신, 중복, 순환을 각각 기존 오류 체계에 맞는 별도 오류로 검증한다. 순환 검사와 저장은 한 transaction에서 한다.
- 같은 프로젝트 범위만 허용하고, 남은 선행이 있는 업무의 프로젝트 변경을 거부한다. 하위가 상위를 따라가는 프로젝트 변경 경로도 확인한다.
- 시작 게이트는 전이 판정 한 곳에 둔다. `in_progress` 시작과 `start_before -> done` 직행에만 `WORK_PREDECESSORS_UNFINISHED` 409를 적용하고, 취소된 선행은 제외한다. 막는 선행 이름을 본문에 포함한다. 시작 후 선행 재개로 후행을 되돌리지 않는다.
- 업무 projection과 프로젝트 상세 업무 줄에 선행 배열을 넣고 새 조회를 만들지 않는다. 볼 수 없는 선행은 제목 없이 건수만 낸다. REST/MCP/AX가 같은 배열 입력을 쓴다.
- 동시 동일 관계의 중복 생성이 한 행으로 수렴하는지 검증한다.

### Phase 3 — 업무 갈래 결재자
- `업무` 생성/수정 payload에서 `approver_id`를 받아 저장하고 projection에 낸다. 0..1, 재직 중, 담당자 본인 불가, 승인 대기 이후 변경 불가를 검증한다.
- `요청` 갈래는 `approver_id` 필드를 열지 않는다. 보내면 pydantic `extra='forbid'`로 422가 나야 하며 조용히 무시하거나 별도 거절 경로를 만들지 않는다. 이것은 OQ-M gate다.
- 업무 갈래 담당자 인자가 없으면 현재 사용자를 담당자로 기록하는 현행 동작을 회귀로 고정한다.
- 참조자 `cc_member_ids`는 업무/요청 양 갈래 모두 저장되는지 회귀로 고정한다. 요청 생성의 `start_date`도 회귀로 고정한다.

## 3. 허용 경로
아래 경로만 수정한다(후보를 먼저 grep으로 재확인하고 필요한 정확한 파일만 수정).
- `backend/src/ax_workspace/platform/persistence.py`
- `backend/src/ax_workspace/platform/work_tasks.py`
- `backend/src/ax_workspace/modules/work/requests.py`
- `backend/src/ax_workspace/modules/work/request_commands.py`
- `backend/src/ax_workspace/modules/work/request_results.py`
- `backend/src/ax_workspace/modules/work/request_errors.py`
- `backend/src/ax_workspace/modules/work/task_creation.py`
- `backend/src/ax_workspace/modules/work/task_commands.py`
- `backend/src/ax_workspace/modules/work/application.py`
- `backend/src/ax_workspace/modules/work/lifecycle.py`
- `backend/src/ax_workspace/modules/work/errors.py`
- `backend/src/ax_workspace/modules/work/projects.py`
- `backend/src/ax_workspace/modules/work/project_results.py`
- `backend/src/ax_workspace/modules/work/task_results.py`
- `backend/src/ax_workspace/bootstrap/application.py`
- `backend/src/ax_workspace/entrypoints/http.py`
- `backend/src/ax_workspace/entrypoints/mcp.py`
- `backend/src/ax_workspace/modules/ax_execution/tool_catalog.py`
- `backend/src/ax_workspace/platform/actions.py`
- `backend/tests/unit/**`
- `backend/tests/contract/**`
- `backend/tests/integration/postgres/**`

같은 파일을 Phase 2와 Phase 3에서 순서대로 다루되, FE 파일은 건드리지 않는다. 문서/코드 밖 경로, migration 도구, 사용자 DB reset은 금지한다.

## 4. 검증
Makefile과 AGENTS.md의 명령을 사용한다.
- 관련 unit/contract 회귀
- `make test-unit`
- `make test-contract`
- 격리 DB에서 `make test-postgres` (POSTGRES_TEST_URL과 DATABASE_URL을 반드시 구분)
- 수신함·상태 전이 입구를 grep으로 전수 확인
테스트를 삭제/skip/완화해 초록으로 만들지 않는다. flaky 부하는 원인과 별도 직렬 증거를 기록한다. 최종 `make verify`와 브라우저 E2E는 코디가 FE와 통합 후 수행한다.

## 5. 완료 보고
커밋·push·PR 금지. 변경 파일, Phase별 구현, 테스트 명령/수치, DB 격리, 미결/OQ-M gate를 보고한다. 완료 시 현재 dispatch preamble의 taskId/dispatchId와 코디 handle로 orchestration `worker_done`을 보내고, 같은 한 줄을 코디 터미널에 직접 주입한다. 두 채널을 모두 보내야 한다.
