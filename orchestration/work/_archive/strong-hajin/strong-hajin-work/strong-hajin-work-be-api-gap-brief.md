# [backend] 요청 자료 계약 및 FE API gap 구현

## 1. 작업 위치와 기준

- 코드 워크트리: `/Users/kknaks/orca/workspaces/Strong_hajin/strong-hajin-work`
- 기존 WORK-003 BE 변경 위에서 작업한다. reset/stash/checkout 금지.
- 문서 레포·`para/`·`frontend/`는 수정하지 않는다. 커밋·push·PR 금지.
- 문서 SSOT는 코디 워크트리의 다음 파일을 read-only로 참고한다.
  - `/Users/kknaks/orca/workspaces/kknaks_profile/strong_hajin/para/projects/summer-star/strong-hajin/20-spec/spec-001-work-management.md`
  - `/Users/kknaks/orca/workspaces/kknaks_profile/strong_hajin/para/projects/summer-star/strong-hajin/30-work/work-003-inbox-predecessor-and-create-frame.md`
- FE 감사 보고서: `/private/tmp/claude-501/-Users-kknaks-orca-workspaces-Strong-hajin-strong-hajin-work/3be67751-8772-4f7f-9a1a-43bbf5927497/scratchpad/create-modal-be-api-gaps.md`

## 2. 목표

FE가 이미 그려 둔 `자료` 탭과 공통 생성 프레임을 실제 BE 계약으로 연결한다. 이번 작업은 아래 5개 gap만 다룬다.

### A. 요청 자료 REST 계약(최우선)

요청 생성 payload에 임의 `material_ids`·`attachments`·`material_draft_ids`를 추가하지 않는다. 요청은 생성 후 반환된 request id를 사용해 자료를 붙이는 2단계 계약으로 만든다.

필수 엔드포인트:

- `POST /api/work-requests/{request_id}/materials` — multipart 파일 업로드
- `POST /api/work-requests/{request_id}/materials/links` — 링크 자료 등록
- `GET /api/work-requests/{request_id}/materials` — 목록
- `GET /api/work-requests/{request_id}/materials/{material_id}/content` — 파일 내용 다운로드/스트리밍
- `DELETE /api/work-requests/{request_id}/materials/{material_id}` — 요청 자료 해제

구현 원칙:

- 기존 `attachments`와 `attachment_bindings` 저장 구조를 재사용한다. 새 자료 테이블을 만들지 않는다.
- 요청 자료의 context는 명시적으로 `work_request`로 구분하고 기존 인덱스·바인딩 의미를 깨지 않는다. storage key 안전성 검사도 함께 갱신한다.
- 업로드 권한은 요청자 본인으로 고정한다. 읽기는 요청 참여자(요청자·담당 후보/활성 담당·CC·결재자 중 현재 권한 계약에 맞는 주체)만 허용한다. 실제 권한 판정은 기존 participant helper 한 곳에 모은다.
- 요청 생성 직후 자료가 요청에 남아야 한다. 거절·철회 후에도 요청 자료는 요청 기록에서 읽을 수 있어야 한다.
- 수락/발송 lifecycle에서 파생 Task가 자료를 읽을 수 있도록 기존 attachment에 Task binding을 추가한다. 원본 요청 binding은 보존한다(이중 바인딩). 복사본을 새로 만들지 않는다.
- 자료 version 증가 규칙은 기존 task 자료 계약과 일관되게 정하고 보고서에 명시한다.
- 댓글 첨부·evidence를 요청 자료 대용으로 사용하지 않는다. 댓글/evidence endpoint를 호출하는 우회 구현도 금지한다.

### B. 회의 승격 입력 확장

`MeetingTodoPromotionInput`이 실제 생성 프레임의 공통 값을 버리지 않도록 기존 요청/업무 계약과 같은 필드를 허용·전파한다.

- `start_date`
- `cc_member_ids`
- `approver_id`
- `reference_task_ids`
- `project_id`
- `parent_task_id`
- `preceding_task_ids`

기존 5개 필드의 의미와 extra-forbid 원칙은 유지한다. 회의 승격이 해당 값을 조용히 버리지 않는지 계약 테스트로 고정한다.

### C. 요청 상세 projection 확장

`WorkRequestService._view`와 결과 타입에 다음을 추가한다.

- `preceding_task_ids` 또는 현행 응답에서 사용하는 동일한 predecessor projection
- `reference_task_ids`
- `materials`(요청 자료 목록의 기존 material view 재사용)

생성·발송·조회에서 동일한 관계가 보이는지 확인한다. 기존 상태·요청자 카드 계약은 변경하지 않는다.

### D. CC 후보 조회 권한 gap

`GET /api/work-request-cc-candidates`가 요청 생성 권한이 없는 `task.self_manage` 사용자에게도 공통 생성 모달의 참조자·결재자 후보를 반환하도록 기존 capability를 재검토한다. 별도 엔드포인트를 만들기 전에 기존 후보 projection/권한을 최소 완화한다. 조직 외 사용자 노출이나 임의 권한 우회는 금지한다.

### E. inventory/문서 drift

신규 HTTP route가 생기면 `docs/unified-operations-inventory.json`과 runtime count를 갱신한다. 기존 route의 signature와 operation id를 유지한다. `docs/domain-model.md`는 새 테이블을 만들지 않으므로 변경하지 않는다.

## 3. 허용 경로

- `backend/src/ax_workspace/`
- `backend/tests/contract/`
- `backend/tests/unit/`
- `backend/tests/integration/postgres/` (격리 PostgreSQL 계약이 실제로 필요한 경우에만)
- `docs/unified-operations-inventory.json`

테스트를 위해 필요한 기존 backend 파일은 위 경로 안에서만 수정한다. `frontend/`, `para/`, `orchestration/`, 새 migration 파일은 수정하지 않는다.

## 4. 테스트 제한과 완료 조건

테스트를 무작정 늘리지 않는다. 기존 테스트를 재사용하고, 신규 테스트는 다음 핵심 회귀만 추가한다(중복 케이스·전체 조합 전수 테스트 금지).

1. 요청 파일 업로드와 링크 등록 후 목록/다운로드/해제 1개 흐름
2. 요청 자료 권한 거부 1개와 허용 주체 1개
3. 수락 시 요청 binding 보존 + Task binding 추가 1개
4. 회의 승격 7개 필드 전파 1개
5. 요청 projection에 predecessor/reference/materials가 돌아오는지 1개
6. CC 후보 capability 경계 1개

실행:

- 구현 중 해당 contract/unit 파일만 `make test-unit` 또는 `make test-contract`로 검증한다.
- 최종 보고에는 실행한 명령과 통과/실패 수를 정확히 적는다. 전체 suite를 반복 실행하지 않는다.
- 기존 실패와 이번 변경 실패를 분리한다. 실패가 남으면 임의 우회하지 말고 `blocked`로 보고한다.

## 5. FE에 전달할 완료 보고 필수 항목

- 실제 추가/변경한 endpoint 목록과 HTTP method, request/response 핵심 필드
- 자료 업로드 권한, 요청 거절/철회 보존, 수락 시 Task 이중 바인딩 lifecycle
- 회의 승격·요청 projection·CC 후보 변경의 파일/라인
- 변경 파일 전체 목록과 allowed path 준수 여부
- 테스트 명령·수치·실패 원인
- API가 아직 없는 항목과 후속 FE 연결 순서

## 6. 완료 보고 채널

완료 시 현재 dispatch preamble의 `taskId`/`dispatchId`를 사용해 `worker_done`을 인박스와 코디네이터 터미널 양쪽에 보낸다. 코디네이터 handle은 `term_30dfd82f-6173-466e-ae5c-d291b46c4a55`다. 보고서 경로를 payload에 포함한다.
