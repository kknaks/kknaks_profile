# [frontend-fix] 요청 생성 모달의 상태·요청자 카드 제거

## 위치

코드 워크트리 `/Users/kknaks/orca/workspaces/Strong_hajin/strong-hajin-work`에서 기존 FE 변경을 이어서 수정한다. reset/stash/checkout 금지. backend·문서 레포는 건드리지 않는다.

## 확정 수정

새 업무 요청 **생성 모달**에서 `상태 | 요청자` 표시 카드를 완전히 제거한다.

생성 모달의 요청 기본정보는 다음만 유지한다.

- 요청할 업무
- 담당 후보
- 시작일
- 희망 기한
- 요청 내용
- 참조자
- 결재자

상태와 요청자는 생성 입력값이 아니다. 요청자는 서버가 현재 사용자로 기록하고, 상태는 서버가 판단 대기로 생성한다. 따라서 `status`, `requester_id` 입력이나 표시 카드를 생성 폼에 남기지 않는다.

요청 상세 모달·수신함 카드에서 상태와 요청자 정보를 보여주는 기존 표면은 보존한다. `내 업무` 생성 모달과 그 payload는 변경하지 않는다. 기존 탭·자료 제한·참고 업무·선행 업무·결재자/참조자 payload는 보존한다.

## 허용 경로

- `frontend/src/features/work/WorkModals.tsx`
- `frontend/src/features/work/*.test.tsx`
- `frontend/src/styles/components.css` (필요할 때만)

backend·migration·docs 수정 금지. 커밋·push·PR 금지.

## 검증

- 요청 생성 모달에 상태·요청자 카드가 렌더링되지 않는 회귀 테스트
- 요청 상세/수신함 표면의 상태·요청자 표시가 유지되는 회귀 확인
- 요청 payload에 status/requester_id 입력이 추가되지 않는지 확인
- `make frontend-test`
- `cd frontend && npx tsc --noEmit -p tsconfig.json`

완료 시 현재 dispatch preamble의 taskId/dispatchId와 코디네이터 handle `term_30dfd82f-6173-466e-ae5c-d291b46c4a55`로 worker_done을 인박스와 코디 터미널 양쪽에 보낸다.
