# [frontend] WORK-003 정정 구현 — 기본정보·참고 업무·요청 자료 제한

## 역할과 위치

코드 워크트리 `/Users/kknaks/orca/workspaces/Strong_hajin/strong-hajin-work`에서 기존 FE 변경을 이어서 수정한다. reset/stash/checkout 금지. 백엔드·문서 레포는 건드리지 않는다.

현재 백엔드는 이전 발주(OQ-M: 요청 결재자 미개방) 기준으로 아직 작업 중이다. 이 작업은 목표 UI와 payload를 먼저 구현하되 backend 파일은 절대 수정하지 않는다. BE 통합 전에는 요청 `approver_id`가 서버에서 422일 수 있으므로, 이를 조용히 제거하거나 우회하지 말고 테스트 mock과 통합 메모에 명시한다.

## 확정 프레임

### 모달 갈래

- 상단 토글: `내 업무 | 요청 업무`
- 내 업무 제목: `새 업무 추가`
- 요청 업무 제목: `새 업무 요청`

### 기본 정보 — 두 갈래 모두

- 내 업무: 업무 제목, 시작일, 마감일, 업무 내용, 참조자(복수), 결재자(1명)
- 요청 업무: 요청할 업무, 시작일, 희망 기한, 담당 후보(1명), 요청 내용, 참조자(복수), 결재자(1명)
- 요청 업무의 결재자도 목표 payload에 `approver_id`로 포함한다. 현재 BE가 거부하는 것은 FE에서 삭제하거나 무시하지 않는다.
- 참조자 `cc_member_ids`는 두 갈래 모두 보낸다.

### 선택 탭

- `체크리스트`: 두 갈래 모두 유지
- `업무 연결`: 두 갈래 모두 유지
  - 상위 업무: 단일 선택
  - 프로젝트: 단일 선택
  - 참고 업무: 복수 체크박스. 기존 `reference_task_ids` 관계와 payload를 사용한다.
  - 선행 업무: 복수 체크박스. 프로젝트를 고른 뒤 해당 프로젝트 후보만 표시한다.
- `자료`: **내 업무에서만 표시**한다. 요청 업무에는 자료 탭·파일 업로드·자료 payload를 노출하지 않는다.

참고 업무는 DB의 `task_references` 관계와 `reference_task_ids`가 이미 존재하므로 UI에서 제거하지 않는다. 참고 업무와 선행 업무는 서로 다른 관계이며, 각각 업무명·프로젝트·담당자 열을 가진 동일한 체크박스 테이블 레이아웃을 사용한다. 프로젝트·상위 업무·선행 후보의 기존 필터와 값 보존 동작을 유지한다.

## 허용 경로

- `frontend/src/features/work/WorkModals.tsx`
- `frontend/src/features/work/*.test.tsx`
- `frontend/src/lib/api.ts`
- `frontend/src/lib/viewModels.ts`
- `frontend/src/lib/labels.ts`
- `frontend/src/features/work/MyWorkPage.tsx`
- `frontend/src/features/work/WorkTables.tsx`
- `frontend/src/styles/components.css`

backend/·docs/·migration 수정 금지.

## 검증

- 기본정보 갈래별 필드와 라벨 회귀
- 두 갈래 `cc_member_ids`, `approver_id`, 시작일 payload 회귀
- 참고 업무 `reference_task_ids` 체크박스와 프로젝트·담당자 표시
- 요청 업무 자료 탭이 없고 자료 payload가 나가지 않는 회귀
- 선행 업무 후보 필터·상위 업무·체크리스트 값 보존
- `make frontend-test`
- `cd frontend && npx tsc --noEmit -p tsconfig.json`

테스트 삭제·skip·완화 금지. 커밋·push·PR 금지. 완료 시 현재 dispatch의 taskId/dispatchId와 코디네이터 handle `term_30dfd82f-6173-466e-ae5c-d291b46c4a55`로 worker_done을 인박스와 코디 터미널 양쪽에 보낸다.
