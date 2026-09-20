# [backend] 요청 업무 참고자료 저장·전파

## 위치

코드 워크트리 `/Users/kknaks/orca/workspaces/Strong_hajin/strong-hajin-work`에서 기존 WORK-003 BE 변경을 이어서 수정한다. reset/stash/checkout 금지. frontend·문서 레포는 건드리지 않는다.

## 확정 수정

요청 생성에서도 참고 자료를 받을 수 있어야 한다. 내 업무 생성에서 사용하는 기존 자료/파일/링크 계약을 조사해 같은 식별자와 저장 관계를 요청에도 연결한다.

- 요청 생성 입력에 기존 자료 계약과 같은 파일/링크 참조 필드를 허용한다.
- WorkRequestRecord 또는 기존 정규화 자료 관계에 요청 자료를 저장한다.
- 요청 상세/projection에서 자료를 반환한다.
- 요청 수락 시 자료가 파생 Task의 자료로 이어진다.
- 요청 거절/철회 시 자료는 요청 기록에 남는다.
- 요청 payload에서 상태·요청자를 받지 않는다.
- 자료 필드 이름과 저장 방식은 기존 Task 자료 계약을 재사용하고 새 임의 모델을 만들지 않는다.

## 허용 경로

기존 자료/업무요청 계약에 직접 필요한 backend 파일과 관련 테스트만 수정한다. 최소 후보:

- `backend/src/ax_workspace/platform/persistence.py`
- `backend/src/ax_workspace/modules/work/request_commands.py`
- `backend/src/ax_workspace/modules/work/requests.py`
- `backend/src/ax_workspace/modules/work/request_results.py`
- `backend/src/ax_workspace/modules/work/application.py`
- `backend/src/ax_workspace/entrypoints/http.py`
- `backend/src/ax_workspace/entrypoints/mcp.py`
- 관련 `backend/tests/contract/`, `backend/tests/unit/`, `backend/tests/integration/postgres/`

frontend·docs·para 수정 금지. 커밋·push·PR 금지.

## 검증

- 요청 생성 파일/링크 자료 저장·반환
- 요청 수락 후 파생 Task 자료 일치
- 거절/철회 후 요청 자료 유지
- 상태·요청자 입력은 허용하지 않음
- 기존 Task 자료·요청 결재자·참조자·선행업무 회귀
- 관련 unit/contract/postgres 테스트

완료 시 현재 dispatch preamble의 taskId/dispatchId와 코디네이터 handle `term_30dfd82f-6173-466e-ae5c-d291b46c4a55`로 worker_done을 인박스와 코디 터미널 양쪽에 보낸다.
