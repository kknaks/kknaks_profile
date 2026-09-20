# [backend-fix] 요청 갈래 결재자 저장·수락 전파

## 위치

코드 워크트리 `/Users/kknaks/orca/workspaces/Strong_hajin/strong-hajin-work`에서 기존 WORK-003 BE 변경을 이어서 수정한다. reset/stash/checkout 금지. frontend·문서 레포는 건드리지 않는다.

## 문제

현재 BE Phase 1~3은 업무 갈래 `approver_id`만 열고, 요청 갈래에서는 `extra='forbid'`로 `approver_id`를 422 처리한다. 최종 UI/payload 계약은 내 업무와 요청 업무 모두 결재자 1명을 받으며, 요청 수락 시 생성되는 업무에도 이 결재자가 이어져야 한다.

## 확정 수정

1. 요청 생성 입력에서 `approver_id`를 nullable 단일 값으로 허용한다.
2. WorkRequestRecord와 요청 저장소/애플리케이션/REST/MCP projection에 `approver_id`를 저장·반환한다.
3. 업무 갈래에서 이미 구현한 결재자 검증 규칙을 요청 갈래에도 적용한다: 재직 멤버, 담당 후보와 동일인 금지, 형식·권한 오류는 기존 결재자 오류 규약을 따른다.
4. 요청 수락으로 파생 Task를 만들 때 요청의 `approver_id`를 파생 업무에 전달한다. 요청 생성·수락·상세 projection의 값이 일관돼야 한다.
5. 기존 요청 결재자 422 회귀 테스트는 삭제하지 말고 새 계약에 맞는 저장·projection·수락 전파 테스트로 교체한다.
6. 요청 생성 payload에 자료/첨부 필드를 추가하지 않는다. 자료 키를 보내면 기존 `extra='forbid'`로 422가 나는 회귀 테스트를 유지 또는 추가한다.
7. 업무 갈래 결재자, 참조자, 선행업무, 읽음 영수증 동작은 회귀시키지 않는다.

## 허용 경로

기존 BE WORK-003 변경 파일 중 요청 계약·저장·수락·projection에 필요한 파일만 수정한다. 최소 후보:

- `backend/src/ax_workspace/platform/persistence.py`
- `backend/src/ax_workspace/modules/work/request_commands.py`
- `backend/src/ax_workspace/modules/work/requests.py`
- `backend/src/ax_workspace/modules/work/request_results.py`
- `backend/src/ax_workspace/modules/work/application.py`
- `backend/src/ax_workspace/entrypoints/http.py`
- `backend/src/ax_workspace/entrypoints/mcp.py`
- 관련 `backend/tests/contract/`, `backend/tests/unit/`, `backend/tests/integration/postgres/`

backend 내에서도 위 계약에 직접 필요한 파일만 건드린다. frontend·docs·para·migration 외 영역 수정 금지(저장소의 기존 스키마 적용 방식에 필요한 변경은 근거를 보고한다). 커밋·push·PR 금지.

## 검증

- 요청 생성 `approver_id` 저장·반환
- 요청 수락 후 파생 Task의 `approver_id` 일치
- 잘못된 결재자/담당 후보 동일인 거절
- 요청 payload의 자료/첨부 필드 422
- 기존 업무 갈래 결재자·참조자·선행업무 회귀
- 관련 unit/contract/postgres 테스트
- 최종 보고에 전체 실행이 병렬 부하로 미실행되면 그 사실과 통과한 수치를 정확히 적는다.

완료 시 현재 dispatch preamble의 taskId/dispatchId와 코디네이터 handle `term_30dfd82f-6173-466e-ae5c-d291b46c4a55`로 worker_done을 인박스와 코디 터미널 양쪽에 보낸다.
