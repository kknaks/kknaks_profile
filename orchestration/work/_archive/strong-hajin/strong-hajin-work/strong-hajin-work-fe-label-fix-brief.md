# [frontend-fix] 업무 생성 갈래 라벨 정정

## 역할과 위치

코드 워크트리 `/Users/kknaks/orca/workspaces/Strong_hajin/strong-hajin-work`에서 기존 FE 구현을 좁게 수정한다. 기존 변경을 reset/stash/checkout하지 않는다. 백엔드·문서 레포는 건드리지 않는다.

## 정정 내용

최종 사용자 결정은 만들기 모달 상단 갈래를 다음처럼 표시하는 것이다.

- 첫 갈래: `내 업무`
- 둘째 갈래: `요청 업무`

갈래에 따른 모달 제목은 그대로 유지한다.

- `내 업무` → `새 업무 추가`
- `요청 업무` → `새 업무 요청`

현재 구현의 `업무 | 요청` 표기만 위 라벨로 바꾼다. payload, 서버 계약, 탭 구조(`기본 정보`, `체크리스트`, `업무 연결`, `자료`), 동작과 접근성 role/selected 의미는 보존한다. aria-label과 기존 FE 테스트가 표시 문자열을 검증한다면 함께 정정한다. 다른 디자인·로직 변경은 하지 않는다.

## 허용 경로

- `frontend/src/features/work/WorkModals.tsx`
- `frontend/src/features/work/*.test.tsx` (표시 라벨 회귀만)

## 검증

- 관련 create-work 테스트
- `make frontend-test`
- `cd frontend && npx tsc --noEmit -p tsconfig.json`

테스트 삭제·skip·완화 금지. 커밋·push·PR 금지. 완료 시 현재 dispatch의 taskId/dispatchId와 코디네이터 handle `term_30dfd82f-6173-466e-ae5c-d291b46c4a55`로 `worker_done`을 인박스와 코디 터미널 양쪽에 보낸다.
