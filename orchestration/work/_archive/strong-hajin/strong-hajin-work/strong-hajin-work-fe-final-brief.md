# [frontend] WORK-003 Phase 4~6 구현 — 만들기 프레임·읽음 수신함·선행 표시

## 1. 역할과 작업 위치
너는 strong-hajin-work 프론트엔드 구현 워커다. 코디네이터 handle은 현재 dispatch preamble의 값을 따른다. 코드 워크트리는 `/Users/kknaks/orca/workspaces/Strong_hajin/strong-hajin-work`이며 공유 트리다. 기존 변경을 reset/stash/checkout 하지 말고 이어서 구현한다. 문서 레포 `para/`와 backend는 수정하지 않는다.

먼저 코드 레포 AGENTS.md와 관련 역할 문서를 읽고, 다음 SSOT를 읽는다.
- `/Users/kknaks/orca/workspaces/kknaks_profile/strong_hajin/para/projects/summer-star/strong-hajin/20-spec/spec-001-work-management.md`
- `/Users/kknaks/orca/workspaces/kknaks_profile/strong_hajin/para/projects/summer-star/strong-hajin/30-work/work-003-inbox-predecessor-and-create-frame.md`
- `/Users/kknaks/orca/workspaces/kknaks_profile/strong_hajin/para/projects/summer-star/strong-hajin/10-decision/decision-001-work-page.md`

## 2. 목표
WORK-003 Phase 4~6을 실제 코드로 구현한다. 기존 로직·접근성·디자인 시스템을 유지하고, 보내지 않는 값은 UI에서 명확히 안내한다.

### Phase 4 — 만들기 창 최종 프레임
- 하나의 모달에서 `업무|요청` 토글을 유지한다. 제목은 업무=`새 업무 추가`, 요청=`새 업무 요청`으로 갈래에 따라 바뀐다.
- 왼쪽 탭은 필수 `기본 정보`, 선택 `체크리스트·업무 연결·자료`다. 선택 탭 이름은 `업무 연결`이다.
- 기본 정보: 제목, 시작일, 마감일, 내용, 참조자 다수, 결재자 1명. 업무 갈래는 담당자 필드를 세우지 않고 서버가 현재 사용자를 담당자로 기록한다. 요청 갈래는 담당자 1명을 세우고 요청 내용을 보낸다.
- 요청 갈래에도 시작일을 표시하고 전송한다. 업무/요청의 공통 payload는 title/description/start_date/due_date/project_id/parent_task_id/cc_member_ids/checklist/reference_task_ids 등 현행 계약을 따른다.
- 업무 갈래 결재자는 실제로 보낸다. 요청 갈래 결재자 칸은 세우되 OQ-M으로 아직 저장하지 않으며 보내지 않는다(보내면 backend 422). 참조자는 업무/요청 모두 저장됨을 안내한다.
- 업무 연결 탭은 상위 업무 단일 라디오/셀렉터, 프로젝트 단일 셀렉터, 선행 업무 복수 체크박스다. 프로젝트가 없으면 선행을 비활성화하고 안내하며, 선택하면 그 프로젝트의 업무만 후보로 보여 자기 자신·이미 선택된 업무를 제외한다. 참고 업무 fieldset은 만들기 창에서 내리되 계약/저장/상세 자리는 건드리지 않는다.
- 체크리스트/자료 탭의 현행 입력과 업로드 동작을 유지하고, 탭 이동에도 값이 보존되며 선택 탭을 비워도 생성된다.

### Phase 5 — 수신함 읽음과 참조 업무 탭
- 참조(CC) 카드에만 `[읽음]`을 표시하고 참조자에게만 보인다. 카드 열기에도 동일한 읽음 명령을 호출한다.
- 읽음 성공 시 수신함 reference 카드만 목록에서 제거하고 필터 뱃지를 줄인다. 연타는 멱등 처리한다.
- `참조 업무` 탭은 요청 목록을 계속 조회해 읽은 업무도 남긴다. 업무 요청 카드에는 `[읽음]`을 만들지 않는다.

### Phase 6 — 선행 표시와 시작 거절
- 업무 상세 값 구획에 선행업무 줄을 표시한다. 없으면 줄을 만들지 않는다. 볼 수 없는 선행은 제목 없이 건수만 표시한다.
- 미완 선행이 있으면 시작 전 업무의 `[시작]`과 `[완료]`를 클릭 전에 비활성화하고 옆에 막는 선행 이름을 표시한다. 서버가 거절한 경우에도 같은 문구를 표시한다.
- 프로젝트 변경 거절 문구를 프로젝트 필드 옆에 표시하고, 회차 충돌 시 최신 값을 다시 읽되 사용 중인 입력은 보존한다.

## 3. 허용 경로
아래 경로만 수정한다(후보를 먼저 grep으로 재확인하고 필요한 정확한 파일만 수정).
- `frontend/src/features/work/WorkModals.tsx`
- `frontend/src/shell/InboxRail.tsx`
- `frontend/src/features/work/requestInbox.ts`
- `frontend/src/features/work/MyWorkPage.tsx`
- `frontend/src/features/work/WorkTables.tsx`
- `frontend/src/lib/api.ts`
- `frontend/src/lib/viewModels.ts`
- `frontend/src/lib/labels.ts`
- `frontend/src/features/work/*.test.tsx`
- `frontend/e2e/**`

backend/·docs/와 문서 레포 수정 금지. 기존 변경을 덮어쓰거나 reset하지 않는다.

## 4. 검증
- `make frontend-test`
- frontend에서 `npx tsc --noEmit`
- 관련 테스트로 갈래 제목/탭, 요청 시작일, CC·approver·predecessor 전송, 프로젝트 후보 필터, 읽음 제거/뱃지, 선행 시작 비활성/거절 문구를 증명한다.
- 브라우저 E2E와 최종 `make verify`는 코디가 통합 후 수행한다. 테스트 삭제/skip/완화 금지.

## 5. 완료 보고
커밋·push·PR 금지. 변경 파일, Phase별 구현, 테스트/tsc 수치, 미결/OQ-M의 요청 결재자 미전송을 보고한다. 완료 시 현재 dispatch preamble의 taskId/dispatchId와 코디 handle로 orchestration `worker_done`을 보내고, 같은 한 줄을 코디 터미널에 직접 주입한다. 두 채널을 모두 보내야 한다.
