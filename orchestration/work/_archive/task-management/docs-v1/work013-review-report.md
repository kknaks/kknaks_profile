---
type: review
work: WORK-013
title: "WORK-013 검수 — payload 두 모양 · 「넣기」 두 표면 · payload 드로어 둘 · 편집 모드 칩 갈래 · 유형 설명"
reviewer: reviewer
date: 2026-09-08
scope: "미커밋 변경 48 파일(back 18 · front 30) + 리비전 0009 · 신규 3 · 폐기 1"
worktree: /Users/kknaks/orca/workspaces/task_management/docs-v1 (kknaksss/docs-v1 · HEAD 0415290)
verdict: "FAIL 0 · WARN 2 · 문서 공백 2"
---

# WORK-013 검수 리포트

**FAIL 0 · WARN 2 · 문서 공백 2.**
`tauri.conf.json` 은 범위 밖이라 보지 않았다. 테스트는 돌리지 않았다(코디 실측 — back 638 · front tsc 0 · vitest 340). 앱 창 실측은 아침 항목이라 요구하지 않았다.

## 0. 축별 판정 한 줄

| 축 | 판정 | 한 줄 |
|---|---|---|
| 2-1 게이트 · `done` 뒷문 | **PASS** | `PayloadStatus{todo,in_progress}` 를 새로 두고 세 표면이 **한 타입**을 본다 — 옛 `frozenset(TaskStatus) - {CANCELLED}` 가 `done` 을 통과시키던 구멍이 닫혔다. `task.status` 대입은 `task_repository.update_status` 한 줄뿐이고 정적 검사 넷이 잠근다 |
| 2-2 payload 저장 ≠ 업무 | **PASS** | `meeting_edit_service` 가 `task_service` 를 import 하지 않고, `task_service` 를 부르는 **함수**가 둘뿐임을 **AST 검사**가 고정한다. 논의·결정에 `payload`/`taskId` → 422 · `newTask` 0 · `kind` 0 · 보낸 키 `null` → 422 |
| 2-3 「넣기」 두 표면 · 원자성 | **PASS** | 두 함수 모두 한 `session` 안에서 업무와 줄을 함께 바꾼다 · 같은 상태면 전이를 건너뛴다 · 헤더 셀렉터의 `taskId` 가 이긴다 · 변경분 0 → ⑧만 · `delete_line` 은 `DELETE` 한 문장(8-b) |
| 2-4 리비전 0009 · 유형 설명 | **PASS** | `description text NULL` + 시드 2건(`is_default` · 이름 · `IS NULL` 삼중 조건) · 미팅·회의 NULL · 왕복 테스트 둘 · `update` 의 `UNSET` 전환은 호출자가 하나라 파급 0 · 응답·MCP 통과 |
| 2-5 payload 드로어 둘 | **PASS · WARN 1** | 업무 탭 드로어 diff **0줄** · `RelationPopover` 는 `mode` prop 하나 · 예외 총수 둘 · `isAiLine`·`line.track ===` **0건** · 필드 일곱/일곱 · `SUBMIT_LABEL` 한 자리. U-9 「현재 값」 두 행이 안 그려진다 |
| 2-6 편집 모드 · 모달 · 유형 설명 | **PASS** | `LineKindSelector` 파일·`onChangeKind` **0건** · 칩 둘 갈래가 드로어를 **바로** 열고 「저장」이 `POST …/lines` 한 요청 · `light` 420(슬롯 없음)/`heavy` 600 · `Dialog` 직접 import 하나 · 금지 목록 0 · 014 침범 0 |
| 2-7 테스트 | **PASS** | BE §12 8-b · 8-c 가 문장 그대로 · 정적 검사 4종(하나는 AST) · FE 가 두 칩 · 두 드로어 · 두 모드 · 모달 두 크기를 전부 단언 |

---

## 1. FAIL

**없다.** 브리프가 지목한 FAIL 조건 아홉을 전부 확인했다 — `task.status` 직접 대입 0 · `done` 뒷문 0 · payload 표면의 `task_service` 호출 0 · 업무 드로어 수정 0줄 · AI/사람 분기 prop 0 · 드로어 연달아 둘 0 · 한 푸터 셋 0 · 원자성 유지 · 014 범위 침범 0.

---

## 2. PASS — 무엇을 확인했나

### 2-1. 게이트 — `done` 뒷문이 **실제로 닫혔다** (BE §12 8-c · MF-59)

이 발주에서 가장 중요한 수정이다. **옛 코드는 `done` 을 통과시키고 있었다.**

```python
# 옛것 — dto/enums.py
PAYLOAD_STATUSES = frozenset(TaskStatus) - {TaskStatus.CANCELLED}   # done 이 남아 있다
```

`dto/enums.py:57-72` 가 **`PayloadStatus` StrEnum**(`TODO` · `IN_PROGRESS`)을 새로 두고 `PAYLOAD_STATUSES = frozenset(PayloadStatus)` 로 바꿨다. 값은 `TaskStatus` 에서 가져와 업무 상태의 정본이 갈리지 않는다.

**세 표면이 한 타입을 본다** — `schemas/meeting.py:186-190` 의 `_TaskChange.status: PayloadStatus | None` 이 `TaskLinePayload`(저장 · `POST`·`PATCH …/lines` 둘)와 `TaskUpdateBody`(`PATCH …/lines/{id}/task`)의 **공통 부모**다. 문자열 쌍을 세 곳에 적지 않았으므로 한 곳만 고쳐지는 사고가 구조로 막힌다. `done`·`cancelled` 는 스키마 층 **422** 다(테스트 `test_meeting_edit.py:192` = BE §12 8-c 문장 그대로).

**회의 중/최종 경로도 같은 집합을 쓴다** — `meeting_finalize_service.py:42` 가 `PAYLOAD_STATUSES` 를 import 하고 `:454` 에서 `status not in PAYLOAD_STATUSES` 면 그 키를 뗀다. WORK-012 의 지역 상수(`_PAYLOAD_ALLOWED_STATUSES`)가 **합쳐졌다** ✓.

**정적 검사 넷**(`test_meeting_task_link.py:415-489`)이 우회로를 잠근다 —
① `task.status` 대입은 `task_repository.py: row.status = status` **한 줄**이고 `update_status()` 호출자는 `task_service` 뿐이며 그 안에서도 `change_status` · `undo_last_status` 둘뿐이다
② `meeting_*` 서비스에 `TaskCompletionBlockedError` · `InvalidStatusTransitionError` 포착 **0건** — `edit` · `task_link` 에는 `try`/`except` 자체가 없다
③ 전이 그래프 · `count_deliverables` · `deliverable` · `TaskStatus.DONE` · `sync_actuals` **0건**
④ **AST 로** `task_service` 를 부르는 함수를 세어 `["apply_task_update", "create_task_from_line"]` 둘뿐임을 고정한다 — 브리프가 물은 「AST 단위 검사」가 실제로 AST 다(`ast.walk` · `ast.Attribute`).

### 2-2. `payload` 저장 ≠ 업무 (M-14-a · MF-60)

| 검사 | 결과 |
|---|---|
| `meeting_edit_service` 의 `task_service` import | **0** — 파일 머리(`:18`)가 정적 검사 대상임을 적어 두었고 ④ 검사가 파일 단위로 확인한다 |
| 논의·결정에 `payload`/`taskId` | **422** — `LineCreate._payload_shape_follows_kind`(`:327`)가 `kind` 로 모양을 고르고 액션·업무가 아니면 거부, `_task_id_only_on_task_lines`(`:321`)가 `taskId` 를 막는다 |
| `LineCreate` 의 `newTask` | **없다** · `extra="forbid"` 가 422 |
| `LineUpdate` 의 `kind` | **없다**(MF-60) · `extra="forbid"` 가 422. 셋(`content`·`payload`·`taskId`)뿐 |
| `content` 네 종류 필수 · 서버가 안 덮는다 | `LineCreate.content: LineContent` 필수 ✓ · `create_task_from_line` 이 줄 본문을 건드리지 않는다(`:74-84` — `values` 에 `content` 가 없다 · 테스트 `test_meeting_task_link.py:348`) |
| 보낸 키 `null` → 422 | `_TaskChange._sent_changes_are_not_null`(`:199-204`) — `model_fields_set` 에 있는데 값이 `None` 이면 거부. 「보내지 않음 = 변경 없음」이 값으로 표현될 자리가 없다 |
| 업무 `payload` `{}` 유효 | `TaskLinePayload` 가 필수 키 0 ✓(docstring 이 이유를 적었다 — 이제 저장값은 초안이고 요청은 `TaskUpdateBody` 다) |
| 액션 `payload.title` 필수 | `ActionLinePayload.title: TaskTitle` ✓ · `workTypeId` 는 `null` 허용(WP OQ-12) |

### 2-3. 「넣기」 두 표면 · 원자성

**`POST …/lines/{id}/task`**(`meeting_task_link_service.py:47-86`) — `kind='action'` **and** `task_id is None` 조건(`:63`) · `task_service.create_task()` 하나로 업무를 만들고 **같은 세션**에서 줄을 `kind='task'` · `task_id` · `payload=None` 으로 바꾼다 · 줄 본문 유지 · `todos`·`start_date` 를 받는다(`LineNewTask`) · 유형이 삭제됐으면 `task_service` 가 거부하고 줄도 안 바뀐다.

**`PATCH …/lines/{id}/task`**(`:92-147`) — ①~⑧ 이 계약 순서 그대로다.
- ① `command.status is not UNSET **and** != task.status` 일 때만 `change_status()`(`:118-121`) — 같으면 건너뛰어 `task_log` 가 안 늘어난다(테스트 `:196`)
- ②③⑦ `update_task()` 한 번(`:122-131`) — 보낸 필드만
- ④ `add_memo`(새 항목) · ⑤ `add_todo`(추가) · ⑥ `link_relations`(추가 · 양방향)
- ⑧ `update_line(task_id=task.id, payload=None)`(`:143-145`) — **본문의 `taskId` 가 저장값을 이긴다**(테스트 `:177`)
- **원자성** — 전 단계가 한 `session` 이고 `try`/`except` 가 없어 어느 단계 거부든 요청째 롤백된다. `payload` 가 그대로 남는다(테스트 `:214` 409 · `:230` 후속 단계 실패가 앞 전이를 되돌린다)
- 변경분 0 → ⑧만(테스트 `:177`)

**`DELETE …/lines/{id}`** — `meeting_line_repository.delete_line`(`:135-146`)이 **`DELETE` 한 문장**이고 뒤 줄 `order_index` 당김이 사라졌다. `next_order_index` 는 `max+1` 그대로라 구멍이 있어도 겹치지 않는다(BE §12 8-b · 테스트 `test_meeting_edit.py:401` 이 그 문장 그대로). 편집 대상 트랙 판정은 `require_editable_line`(`meeting_edit_service.py:72-81`) 하나이고 `ai` 줄은 422 다.

### 2-4. 리비전 0009 · 유형 설명 (A-12 · SPEC-002)

- `0009_work_type_description`(`down_revision = "0008_meeting_payload_terms"` ✓) — `description text NULL` 추가 + **기본 2건** UPDATE. 조건이 **삼중**이다: `is_default = true AND name = :name AND description IS NULL` → 사람이 적어 둔 설명을 덮지 않고, **미팅·회의는 목록에 없어 NULL 로 남는다**(DEC-003 OQ-11 「문구를 정하지 않는다」).
- `downgrade` 는 컬럼을 지운다(값도 사라진다 — docstring 이 명시).
- **왕복 테스트 둘** — `test_migrations.py:271`(왕복 + 사람이 적은 설명 보존) · `:319`(기본 3종을 심어 두고 **2건만** 채워지고 미팅·회의는 NULL).
- 검증 — `Description` 0~200 · `_reject_description_newlines` 로 줄바꿈 **거부**(지우지 않는다) · `_NULLABLE` 에 `description` 만 넣어 **`null` 로 지우기**를 허용 · 기본 3종도 색·설명은 통과(`work_type_service.py:82-86` — 잠긴 것은 이름과 종류뿐).
- **`work_type_repository.update` 의 `None` → `UNSET` 규약 변경 파급 0** — 이 함수를 부르는 곳은 `work_type_service.py:108` **하나**뿐이고 같은 발주에서 함께 고쳐졌다. `repository/` 안에서 이런 부분 갱신 시그니처를 가진 함수도 이것 하나다.
- 응답 — `WorkTypeItem.description`(`schemas/setting.py:136`)이 목록에 실리고, 주석대로 MCP `list_work_types()` 가 그대로 통과시킨다(WORK-009 가 필드를 고르지 않는 구조로 만들어 두었다).

### 2-5. payload 드로어 둘 (FE §2 규칙 8 · MF-65 · 66 · 67)

| 검사 | 결과 |
|---|---|
| ① 업무 탭 드로어 | `TaskCreateDrawer.tsx` · `TaskDetailDrawer.tsx` **diff 0줄** ✓ |
| ① `RelationPopover` | `mode?: "single" \| "multi"` **하나**만 늘었고 기본값이 `"multi"` 라 **업무 화면 다중 선택이 그대로**다. `single` 은 행 클릭에서 확정·닫기 + 푸터 숨김 |
| ① 배럴 · 예외 총수 | `features/tasks/index.ts` 가 이유 주석과 함께 export. `CROSS_AREA_ALLOWED.tasks = {openTaskDetailDrawer, RelationPopover}` — **예외는 둘**이고 내부 경로 import 는 여전히 전부 위반이다 |
| ② prop | 두 드로어 모두 `prefill` + `submitMode`. **`isAiLine` · `line.track ===` 가 소스 전체에 0건**(정적 ㉓) |
| ③ 액션 드로어 일곱 | 안건 고정 · `title` · `workTypeId` · `projectId` · `startDate` · `dueDate` · `description` · `todos`. `workTypeId=null` 이면 `canSubmit` 이 `submitMode === "save"` 일 때만 참(`:138`) — **저장은 되고 넣기는 비활성** ✓ |
| ③ 업무 드로어 | 헤더 = `RelationPopover mode="single"`(`:164-165`) · 변경분 일곱(`dueDate`·`status`·`note`·`todos`·`relatedTaskIds`·`projectId`·`completionResult`) · 업무 미선택이면 `disabled` 가 본문 전체에 걸린다 · 제목·유형·설명·시작일 **없다** · 첨부·로그·참고자료 **없다**(파일 머리 `:18` 이 명시) |
| ④ 푸터 | `SUBMIT_LABEL: Record<SubmitMode, string> = { save: "저장", insert: "넣기" }`(`PayloadDrawerParts.tsx:23`) **한 자리** · 각 드로어가 `SUBMIT_LABEL[submitMode]` 하나만 그린다(정적 ㉓) → 취소 + 하나 |
| ⑤ 채워진 키만 | `compactChanges`(`linePayload.ts`) — `prefill` 을 되돌려 보내지 않고 **현재 상태와 같은 `status` 는 뺀다`. MSW 본문 단언(`MeetingTaskLink.test.tsx:316`)이 `{taskId, …채워진 키만}` 를 고정 |
| ⑤ 저장 경로 | 「저장」은 `PATCH …/lines/{id}` 또는 `POST …/lines` 뿐 — **업무 API 요청 0**(테스트 `:210`) |
| ⑥ 줄 버튼 세 상태 | 「업무 생성」/「업무 갱신」/「갱신 완료」 비활성 · dot · 툴팁 · `generating` 잠금 · AI 탭에는 없음(테스트 `:143` 한 건이 전부를 단언) |

**⑥ 삭제된 업무 — 워커의 판단이 맞다.** 디스패치 브리프는 「버튼 비활성」이라 적었지만 **SPEC-008 U-6 은 「배지 · 제목 그대로 + 「삭제된 업무」 12/`#9EA2AE`, 버튼은 「업무 갱신」 그대로(헤더 셀렉터에서 다른 업무로 바꿀 수 있다)」**다. 코드가 SPEC 을 따랐다 — 지적할 것이 없고, **브리프 쪽 문장이 틀렸다**.

### 2-6. 편집 모드 · 모달 · 유형 설명

| 검사 | 결과 |
|---|---|
| ① `LineKindSelector` · `onChangeKind` | 소스 전체 **0건**(파일 삭제 · `lineKinds.ts` 머리 주석도 갱신). `AddLineDrawer.AddLineKind = "discussion" \| "decision"` 2값(`:32`) |
| ② 칩 둘 갈래 | `MeetingDetailBody` — 「+ 논의」·「+ 결정」은 U-8 드로어, 「+ 연관 업무」·「+ 액션 아이템」은 `openActionPayloadDrawer`/`openTaskPayloadDrawer` 를 **`line=null` 로 바로** 연다. 「저장」이 `edit.addLineFromDrawer({agendaId, kind, content, payload})` = **`POST …/lines` 한 요청** ✓ **드로어 연달아 둘 0**(테스트 `MeetingEditMode.test.tsx` 두 건) · 「취소」면 줄이 없다 |
| ③ 모달 | `ConfirmModal` `size = request.size ?? "heavy"` · `light` 는 420(`w-modal-light`)이고 **경고 슬롯을 받지 않는다** · `data-modal-size` 로 테스트가 잡는다. `size:"light"` 를 넘기는 곳은 `LineDeleteModal.tsx:29` **하나** — 회의 삭제는 인자를 안 넘겨 **600 그대로** ✓(테스트가 같은 파일에서 둘 다 단언). `Dialog` 직접 import = `ConfirmModal.tsx` 하나(정적 ㉓) |
| ④ 낙관적 | 인라인 본문 · 안건 이름 · `savePayload` 가 `onMutate` + `rollback` 을 갖고, **줄 삭제는 `onSuccess` 에서만** 캐시를 고친다(`useMeetingEdit.tsx:141-155` — 「낙관적이지 않다」를 주석이 명시). 「넣기」는 `useMeetingTaskLink` 가 응답으로 `setQueryData` 하고 `tasks`·`schedules` 를 무효화한다 |
| ⑤ 에러 분기 | `errors.ts` 가 **`code` 로만** 분기한다(`:57` switch · `isValidationError` · `validationFieldOf` · `isMeetingNotFound`). `useMeetingTaskLink` 머리표(`:22-23`)가 422 `task_completion_blocked` → 토스트 + 「결과 입력」 · 409 `invalid_status_transition` → 토스트 + 전부 롤백(`payload` 유지)을 적고 테스트가 확인한다 |
| ⑥ 유형 설명 UI | 추가 행 넷 · 인라인 편집 · 「설명 없음」 · 기본 3종 편집(`WorkTypePanel.test.tsx` +133줄) |
| ⑦ 금지 목록 | `fetch(` 직접 **0**(히트는 전부 `.refetch()`) · 인라인 hex **0**(히트는 전부 문서 주석 — 정적 ②가 주석을 벗기고 검사) · `sheet` 직접 import 0 · `localStorage` 0 · `retry: true` 0 |
| ⑦ 014 침범 | `MeetingPreviewPanel.tsx` · `MeetingStatusBar.tsx` **diff 없음** · breadcrumb · 헤더 파일 손대지 않음 |

---

## 3. WARN

### W-1. 업무 payload 드로어가 U-9 「현재 값」 두 행을 그리지 못한다

- **어긋난 문서**: SPEC-008 **U-9** 변경분 표 —
  | **프로젝트** | 고른 업무의 **현재 프로젝트** · `payload.projectId` 가 있으면 그 값 |
  | **완료 결과** | 고른 업무의 **현재 `completionResult`** · `payload` 값이 있으면 그 값 |
  그리고 같은 절의 「업무를 아직 안 골랐으면 본문이 비활성(캡션 「업무를 고르면 **현재 값이 보입니다**」)」.
- **무엇이 일어나나**: 회의록이 가진 두 응답 어디에도 그 값이 없다 —
  - `LineTaskSummary`(`schemas/meeting.py:479-490`) = `id` · `title` · `status` · `due_date` · `is_deleted` · `work_type` — **`projectId` 도 `completionResult` 도 없다**
  - `RelationCandidateItem`(`schemas/task.py:389-396`) = `id` · `title` · `status` · `project_name` · `due_date` — `project_name` 은 **표시용 이름**이라 `projectId` 를 채울 수 없고, `completionResult` 는 아예 없다
  그래서 기한·상태는 현재 값이 보이고 **프로젝트·완료 결과는 `payload` 값이 있을 때만** 채워지며 없으면 「변경 없음」으로 남는다.
- **워커의 선택은 옳다** — 회의록이 업무 상세를 읽는 경로를 새로 여는 것은 영역 경계를 넘는 결정이라 코드가 정할 일이 아니다. **뿌리는 D-1 이고**, 응답에 필드를 더할지는 문서가 정해야 한다.

### W-2. 두 드로어의 **파일 이름**이 내용과 어긋난다

- **자리**: `components/CreateTaskFromLineDrawer.tsx` · `components/LinkTaskDrawer.tsx`
- 내보내는 이름은 `openActionPayloadDrawer` · `openTaskPayloadDrawer` 로 바뀌었는데 **파일 이름만 옛것**이다. 둘 다 이제 하는 일이 다르다 —
  - `CreateTaskFromLineDrawer` 는 「저장」에서 **업무를 만들지 않는다**(`payload` 만 붙인다). 「create task」는 `insert` 모드 하나뿐이다.
  - `LinkTaskDrawer` 의 「연결」은 **SPEC 이 없앤 개념**이다 — SPEC-008 U-9 가 「**「업무 연결」 같은 앞 단계가 없다**」고 못박았고 파일 머리 주석(`:12`)도 그렇게 적어 두었는데, 파일 이름이 계속 그 말을 한다.
- 동작에는 문제가 없다(WP §Code Surface 도 「두 파일을 전면 수정」으로 적었고 이름 변경을 지시하지 않았다). 다음에 이 화면을 여는 사람이 파일 이름으로 잘못 짚을 자리다.

---

## 4. 문서 공백

| # | 자리 | 무엇이 비었나 |
|---|---|---|
| **D-1** | SPEC-008 **U-9** 변경분 표(프로젝트 · 완료 결과 행) + §4 `MeetingDetail` `LineTaskSummary` · SPEC-003 §4 `RelationCandidateItem` | U-9 가 요구하는 「고른 업무의 **현재** 프로젝트 · 현재 `completionResult`」를 **회의록이 볼 수 있는 어떤 응답도 담고 있지 않다**. 기한·상태는 `LineTaskSummary` 에 있어 되지만 이 둘은 못 한다. 셋 중 하나가 필요하다 — ① `LineTaskSummary` 에 두 필드를 더하거나 ② 후보 항목에 더하거나 ③ U-9 에서 이 둘의 「현재 값」 규칙을 빼거나. **결정을 만들지 않았다**(W-1 의 뿌리) |
| **D-2** | SPEC-008 U-10 / §4 `POST …/lines/{id}/task` | **줄 본문과 업무 제목의 관계가 정해져 있지 않다.** 「넣기」가 줄 본문을 그대로 두고(사람이 적은 문장이라 옳다) 업무 제목은 드로어에서 따로 고칠 수 있어, 넣은 뒤 둘이 갈릴 수 있다. 코드가 그 자리에서 **「둘을 잇는 동기화 규칙은 SPEC 에 없다」**고 스스로 적어 두었다(`meeting_task_link_service.py:57`). 갈려도 되는지, 화면이 무엇을 보여 주는지가 없다 |

---

## 5. WP 검증 항목 ↔ 테스트 대응표

**Phase 1 — 스키마 층**

| 검증 항목 | 테스트 |
|---|---|
| `PATCH …/lines` 에 `kind` → 422 · `POST` 에 `newTask` → 422 · 논의·결정에 `payload`/`taskId` → 422 | `test_meeting_edit.py:224` · `:123` |
| 액션·업무 줄에 `payload` 를 실어도 내 업무에 아무것도 안 생긴다(행 수 대조) | `:123` |
| **BE §12 8-c** `done`·`cancelled` 스키마 층 422 · `task.status` 불변 | `:192` |
| 액션 `payload.workTypeId=null` 저장 | `:123` |
| `content` 네 종류 필수 · 서버가 안 덮는다 | `:340` · `test_meeting_task_link.py:348` |
| 두 표면이 한 상태 집합 | `test_meeting_edit.py:236` |
| 정적 — 옛 이름 0건 | `:507` |

**Phase 2 — 「넣기」 두 표면 · 자리 유지 · 유형 설명**

| 검증 항목 | 테스트 |
|---|---|
| **BE §12 8-b** 자리 유지 · 새 줄 마지막 + 1 | `test_meeting_edit.py:401` |
| 삭제가 업무·AI·트랜스크립트·녹음을 안 건드린다 | `:245` · `:315` |
| ①~⑧ 한 트랜잭션 | `test_meeting_task_link.py:129` |
| 같은 상태면 전이 0(`task_log` 0) | `:196` |
| 거부 시 전부 롤백 + `payload` 유지 | `:214` · `:230` |
| 변경분 0 → ⑧만 · 헤더 셀렉터가 이긴다 | `:177` |
| 완료 결과가 게이트를 연다(⑦) | `:259` |
| 리비전 0009 왕복 · 시드 2건 · 미팅·회의 NULL | `test_migrations.py:271` · `:319` |
| 설명 0~200 · 줄바꿈 · null · 기본 3종 | `test_work_type.py`(+59줄) |
| 정적 — `task_service` 를 부르는 함수 둘뿐 | `test_meeting_task_link.py:471`(**AST**) + `:415` `:434` `:448` |

**Phase 3~5 — 프론트**

| 검증 항목 | 테스트 |
|---|---|
| 줄 버튼 세 상태 · dot · 툴팁 · 삭제된 업무 · AI 탭 없음 | `MeetingTaskLink.test.tsx:143` |
| AI 액션 줄 → 일곱 · 「취소 · 넣기」 → `POST …/task` 하나 | `:170` |
| 사람 액션 줄 → 같은 드로어 · 「저장」 = `PATCH …/lines` 하나 · **업무 요청 0** · 보기 모드에서 값 그대로 | `:210` |
| 인라인 자동 저장 0 · 「취소」면 저장 0 | `:253` |
| AI 업무 줄 → 셀렉터가 물고 변경분 일곱 · **상태에 「완료」 없음** | `:272` |
| 사람 업무 줄 → 빈 셀렉터 · 본문 비활성 · 앞 단계 없음 | `:300` |
| 「넣기」 → 채워진 키만 · 「갱신 완료」 · 게이트 거부 처리 | `:316` |
| 편집 모드 종류 셀렉터 없음 · `PATCH` 에 `kind` 0 | `MeetingEditMode.test.tsx`(2건) |
| 칩 둘 갈래 · `POST …/lines` 하나 · 취소면 줄 없음 | 〃(2건) |
| 420 모달 한 문장 · 슬롯 없음 · 회의 삭제 600 | 〃(2건) |
| 정적 ㉓ 7건 | `static.test.ts` |
| 업무 탭 회귀 | `features/tasks` 기존 테스트 무수정 통과 + 드로어 diff 0줄 |

**빠진 것** — 앱 창 실측(아침 항목이라 세지 않았다)과 WP Phase 1~5 의 `완료 증거`(`미작성`).

---

## 6. 요약

**게이트가 실제로 막혔다.** 이 발주 전에는 `PAYLOAD_STATUSES = frozenset(TaskStatus) - {CANCELLED}` 라 `payload.status='done'` 이 스키마를 통과하고 있었다 — `PayloadStatus` 타입 하나로 세 표면이 같은 값 집합을 보게 되면서 BE §12 8-c 가 처음으로 참이 됐다. `task_service` 를 부르는 **함수**가 둘뿐임을 AST 로 세는 검사까지 붙어 우회로가 구조로 닫혔다.

**나머지도 계약대로다.** `payload` 두 모양이 `kind` 로 갈리고, 「넣기」 두 표면이 한 트랜잭션이며, `delete_line` 이 `DELETE` 한 문장이 됐다(8-b). 프론트는 **업무 탭 드로어를 한 줄도 안 고치고**(diff 0줄) `RelationPopover` 에 `mode` prop 하나만 더해 재사용했으며, 드로어가 AI/사람을 가르는 코드가 0건이고 푸터 문구가 한 자리에서만 난다. 칩 진입이 드로어를 바로 열어 「저장」이 요청 하나로 끝나고(MF-64 정정), 모달이 420/600 두 크기로 갈렸다. 014 범위 침범 0.

남은 둘은 성격이 다르다 — **W-1** 은 SPEC-008 U-9 가 요구하는 「현재 값」 두 개를 회의록이 가진 응답이 담고 있지 않아서 생긴 것이라 **문서가 먼저 정해야 하고**(D-1), **W-2** 는 파일 이름이 옛 개념을 계속 말하는 것이라 다음 발주에서 정리하면 된다. 커밋을 막을 무게는 없다.
