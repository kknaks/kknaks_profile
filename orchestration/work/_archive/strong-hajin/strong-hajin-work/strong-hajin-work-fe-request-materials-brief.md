# [frontend] 요청 업무 참고자료 추가

## 위치

코드 워크트리 `/Users/kknaks/orca/workspaces/Strong_hajin/strong-hajin-work`에서 기존 FE 변경을 이어서 수정한다. reset/stash/checkout 금지. backend·문서 레포는 건드리지 않는다.

## 확정 수정

`새 업무 요청` 모달에도 선택 탭 `자료`를 표시한다. 사용자는 요청을 보낼 때 참고 파일/이미지와 링크를 추가할 수 있어야 한다.

- 탭 구조: 필수 `기본 정보`; 선택 `체크리스트`, `업무 연결`, `자료`
- 자료 탭에서 기존 내 업무 자료 UI/업로드·링크 입력 부품을 재사용한다.
- 요청 payload에 기존 자료 계약과 동일한 자료 식별자/링크 필드를 포함한다. 임의 필드명을 만들지 말고 현재 Task 자료 payload/어댑터와 맞춘다.
- 요청이 수락되면 자료가 파생 업무로 이어지는 것을 전제로 상태와 선택값을 보존한다.
- 요청 생성에서 상태·요청자 카드는 계속 제거 상태를 유지한다.
- 기존 내 업무 자료 탭, 참조업무/선행업무, 결재자/참조자 payload는 회귀시키지 않는다.

## 허용 경로

- `frontend/src/features/work/WorkModals.tsx`
- `frontend/src/features/work/*.test.tsx`
- `frontend/src/lib/api.ts`
- `frontend/src/lib/viewModels.ts`
- `frontend/src/styles/components.css` (필요할 때만)

backend·migration·docs 수정 금지. 커밋·push·PR 금지.

## 검증

- 요청 갈래에 자료 탭·파일/링크 입력이 보이는지
- 요청 payload에 자료 값이 포함되는지
- 내 업무 자료 탭이 유지되는지
- 상태·요청자 카드가 생성 모달에 다시 생기지 않는지
- `make frontend-test`
- `cd frontend && npx tsc --noEmit -p tsconfig.json`

완료 시 현재 dispatch preamble의 taskId/dispatchId와 코디네이터 handle `term_30dfd82f-6173-466e-ae5c-d291b46c4a55`로 worker_done을 인박스와 코디 터미널 양쪽에 보낸다.
