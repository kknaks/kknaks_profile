# [frontend] WORK-013 Phase 3~5 — payload 드로어 둘 · 편집 모드 칩 둘 갈래 · 모달 420 · 유형 설명 UI

너는 **task-management `frontend` 워커**다.
역할 문서: `/Users/kknaks/orca/workspaces/kknaks_profile/task-management-app/orchestration/roles/task-management/frontend/role.md`

## 0. 어디서 무엇을 보나

**코드 워크트리** — `/Users/kknaks/orca/workspaces/task_management/docs-v1` (브랜치 `kknaksss/docs-v1`). **WORK-013 백엔드(Phase 1·2)가 방금 들어왔다** — 아직 커밋 전이다(`git diff HEAD -- app/back/schemas/meeting.py app/back/api/meeting_router.py`). be+fe 를 한 커밋으로 낸다. 서버 표면: `POST …/lines`(action/task 줄에 `payload` · `taskId`) · `PATCH …/lines/{id}`(`kind` 없음) · `POST …/lines/{id}/task` · `PATCH …/lines/{id}/task`(본문 `taskId` + 변경분) · `GET /api/work-types` 에 `description`.

문서는 전부 **코디 워크트리 절대경로 · 읽기 전용**이다.

```
/Users/kknaks/orca/workspaces/kknaks_profile/task-management-app/para/projects/summer-star/task-management/
  30-work/work-013-meeting-edit.md             ← 네 빌드 계획. **Phase 3 · 4 · 5.** Code Surface 프론트 행 · Internal Interface(드로어 prop 둘 · 푸터 · 칩 진입 · ConfirmModal size · RelationPopover 단일 · 낙관적 · 무효화) · Phase 검증
  20-spec/spec-008-meeting-close.md            ← **U-6**(줄 버튼 세 상태 · dot · 툴팁) · **U-7**(편집 모드 · 칩 둘 갈래 · 「제거」 420) · **U-8**(논의·결정 전용) · **U-9**(업무 payload 드로어 — 헤더 셀렉터 · 변경분 일곱 · 모드별 푸터) · **U-10**(액션 payload 드로어 — 안건 고정 · 일곱) · §4 · §5 구현 규칙 · Case Matrix · §6 AC
  20-spec/spec-003-tasks-crud.md               ← U-1(새 업무 드로어) · U-3(업무 상세 드로어) — **시각 부품 참조만** · U-8(RelationPopover 0건 폴백 · 단일 선택)
  20-spec/spec-002-work-settings.md            ← U-3 인라인 추가 행(설명 필드) · U-4 목록 행 설명 인라인 편집 · U-7 자동 저장 실패
  40-architecture/frontend/README.md           ← §2 규칙 8(payload 드로어는 회의록 것 · 업무 드로어 미수정 · 반려 조건) · §3-3 무효화 · §3-4 낙관적 · §6(모달 두 크기 · openConfirm size) · §6-1 · 금지 목록
/Users/kknaks/orca/workspaces/kknaks_profile/task-management-app/reference/2026-09-06-task-management-app/Meeting flow.md §3-4 · §3-5   ← MF-13 · 14 · 60 · 61 · 62 · 63 · 64(정정) · 65 · 66 · 67
```

**시각** — payload 드로어 둘은 **새 시안 없음.** 이미 만들어진 `features/tasks/components/TaskCreateDrawer.tsx` · `TaskDetailDrawer.tsx` 의 **부품**(입력 · 셀렉터 · 일정 · 할일 · 메모 · 완료 결과 블록 · 헤더 · 푸터 규격)을 보고 `features/meetings/components/` 안에서 조립한다. **그 두 파일은 수정하지 않는다**(diff 0 — 정적 검사). 옛 회의록 드로어 시안(L2306~2882)은 참고하지 않는다. 확인 모달 420 은 FE §6 규격.

## 1. 범위 — Phase 3 · 4 · 5

```
Phase 3  CreateTaskFromLineDrawer.tsx → 액션 payload 드로어(U-10) 전면 수정 — 안건 고정 · 제목 · 유형 · 프로젝트 · 계획 시작~종료 · 설명 · 할일 (일곱뿐)
         LinkTaskDrawer.tsx → 업무 payload 드로어(U-9) 전면 수정 — 헤더 제목 자리 = 업무 셀렉터(RelationPopover mode="single") · 본문 변경분 일곱(상태 셀렉터에 완료·취소 없음) · 업무 미선택이면 본문 비활성
         두 드로어 prop 둘뿐 — prefill(= 줄의 payload | null) · submitMode:"save"|"insert". 푸터 "save" = 취소·저장 / "insert" = 취소·넣기. 인라인 자동 저장 0
         RelationPopover mode?: "single"|"multi" 하나(업무 화면 다중 선택 불변 · 기준 프로젝트 0건이면 「전체」)
         openMeetingDrawers.tsx · useMeetingTaskLink(applyTaskUpdate · savePayload) · LineTaskButton(업무 생성/업무 갱신/갱신 완료 · dot · 툴팁)
Phase 4  LineKindSelector.tsx 폐기 · LineRow/AgendaLineTree 에서 onChangeKind 제거 · AddLineDrawer 세그먼트 2값(논의|결정) · 캡션 정리
         MeetingDetailBody 칩 둘 갈래 — + 논의·+ 결정 → openAddLineDrawer / + 연관 업무·+ 액션 아이템 → payload 드로어 바로(submitMode:"save" · 「저장」= POST …/lines 한 요청 · 닫으면 줄 없음)
         ConfirmModal size?:"heavy"|"light"(420 · 제목 + 한 문장 + h32 · warning 없음) · OverlayProvider.openConfirm size · LineDeleteModal 한 문장
Phase 5  WorkTypePanel · InlineAddRow 설명 필드(추가 행 네 필드 · 목록 행 인라인 편집 · 비면 「설명 없음」 · 기본 3종도 편집) · settings types/api
```

## ⛔ 2. 하지 말 것

```
features/tasks/components/TaskCreateDrawer.tsx · TaskDetailDrawer.tsx   **수정 금지** (diff 0 · 반려)
AI 줄 / 사람 줄 분기   isAiLine · line.track === 로 드로어를 가르는 코드 0 (MF-65 · 반려). 드로어는 prefill 이 null 인지만 본다
한 푸터에 저장+넣기 셋   반려(MF-66)
드로어 연달아 둘         「+ 액션 아이템」이 줄 추가 드로어를 거치면 반려(MF-64 정정)
업무 payload 드로어에 제목·유형·설명·시작일 · 어느 드로어든 첨부·로그·참고자료 블록   반려(MF-14 · 67)
Dialog 직접 import      ConfirmModal 하나뿐 · Sheet 직접 import 0 · 폭 리터럴 840 은 DrawerFrame 안에만
줄 순서 변경 · 안건 추가·삭제 버튼 · 되돌리기 · 종류 셀렉터   없다
fetch 직접 · hex 리터럴 · localStorage · retry:true   금지
breadcrumb · 헤더 순서 · 미리보기 패널   WORK-014
```

## 3. 계약

- **드로어 둘 · prop 둘** — `prefill` · `submitMode`. 저장 = `PATCH …/lines/{id} {payload(, taskId)}`(있는 줄) 또는 `POST …/lines {agendaId, kind, content, payload(, taskId)}`(칩 진입) — 업무 없음. 넣기 = `POST …/lines/{id}/task`(액션) / `PATCH …/lines/{id}/task {taskId, …변경분}`(업무). 넣기 조건 — 액션: 제목 + 유형 / 업무: 업무 골라짐
- **줄 버튼** — 액션 「업무 생성」 · 업무 「업무 갱신」 · 넣기 뒤 「갱신 완료」 비활성 · `payload` 있으면 6px dot · 툴팁(변경분 — `status` 가 현재와 같으면 뺀다) · `generating` 잠금
- **모드** — 보기 모드 줄 버튼 → `"insert"` · 편집 모드 줄 버튼·칩 → `"save"`
- **낙관적** — 인라인 본문 · 안건 이름 · U-8 추가 · `payload` 저장 O / 줄 삭제 · 넣기 X
- **무효화** — 줄·안건·payload → `['meetings','detail',id]` / 넣기 → + `['tasks',…]` 전부(+ 기한·시작일 바뀌면 `['schedules']`)
- **변경분 키는 값이 있을 때만 보낸다** — 백엔드가 `null` 키를 422 로 막는다(「보내지 않음」= 변경 없음 · 비우는 뜻의 값은 계약에 없다). 드로어가 `prefill` 을 그대로 되돌려 보내지 말고 **채워진 키만** 본문에 싣는다. AI 가 저장한 `payload` 에는 `completionResult: null` 같은 키가 들어 있을 수 있다(SPEC-008 §4 예시) — 읽을 때는 무시하고 보낼 때는 뺀다
- **`status` 셀렉터 값은 `todo` · `in_progress` 둘뿐** — 스키마 `PayloadStatus` 와 같다. 액션 payload 는 `title` 필수 · 업무 payload 는 `{}` 도 유효(저장된 초안)
- **PATCH …/lines/{id} 본문에 `kind` 가 없다** — payload 모양은 서버가 줄 종류로 판단한다. 프론트는 줄 종류에 맞는 드로어만 연다
- **에러 code 분기** — `invalid_status_transition` 409(드로어 유지 + 토스트) · `validation_error` 422(그 필드 인라인) · `not_found` 404(줄에 「삭제된 업무」 + 버튼 비활성)

## 4. allowed_paths

```
app/front/
```
(`features/tasks/components/TaskCreateDrawer.tsx` · `TaskDetailDrawer.tsx` 는 allowed 안이지만 **수정 금지**. `RelationPopover.tsx` 는 `mode` prop 하나만)

## 5. 검증

WP §Execution Phase 3 · 4 · 5 검증 체크리스트 전부(MSW 요청 단언 포함). 정적 — `git diff --stat features/tasks/components/TaskCreateDrawer.tsx TaskDetailDrawer.tsx` 0 · `isAiLine|line.track ===` 0 · `LineKindSelector|onChangeKind` 0 · `Dialog` 직접 import 1(ConfirmModal) · `pendingChange|applyPendingChange` 0

```bash
cd /Users/kknaks/orca/workspaces/task_management/docs-v1/app/front && npx tsc --noEmit && npx vitest run 2>&1 | tail -8   # Errors 줄 0
```

**앱 창 실측** — 가능하면 `tauri dev` 로 편집 모드 → 「+ 액션 아이템」 → 저장 → 보기 모드 「업무 생성」 → 넣기 → 내 업무에 생김 · 「+ 연관 업무」 → 헤더 셀렉터 → 저장 → 넣기 흐름을 눈으로 보고 캡처 경로를 보고에. 못 띄우면 그 사실만.

막히면 30분 넘기지 말고 §9 (2) 로 물어라.

---

## 9. 완료 보고 — **문구 변경 금지**

> **⚠ 핸들은 dispatch preamble 의 값을 믿어라.** preamble 의 코디네이터 핸들과 아래 값이 다르면 **preamble 이 맞다.**

- **커밋·push·PR 하지 마라.**
- 끝나면 **아래 두 명령을 모두** 실행한다.

```bash
# (1) 인박스 적재
orca orchestration send \
  --to term_98a33032-2134-4bf9-ac48-e9df737f9b8f --from term_1c173ed7-8c1c-4b28-9b4c-f7817cc54ec8 \
  --type worker_done \
  --task-id <이 태스크의 taskId — dispatch 로 받은 context 에 들어 있다> \
  --dispatch-id <이 태스크의 dispatchId — dispatch 로 받은 context 에 들어 있다> \
  --subject "frontend 완료: WORK-013 Phase 3~5" \
  --body "변경 파일 목록 / Phase 별 구현 요약 / 검증 결과(tsc · vitest · 정적 · 앱 창) / 계약 준수 / 미결·주의점"

# (2) 직접 주입
orca terminal send --terminal term_98a33032-2134-4bf9-ac48-e9df737f9b8f \
  --text "[worker_done] frontend 완료 — WORK-013 편집 프론트. 상세는 인박스." --enter
```

- 막히면 `orca terminal send --terminal term_98a33032-2134-4bf9-ac48-e9df737f9b8f --text "[질문] frontend: <질문>" --enter`
