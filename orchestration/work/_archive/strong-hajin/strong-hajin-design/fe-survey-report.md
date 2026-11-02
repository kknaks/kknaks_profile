# 업무 구조 프론트 전수조사

조사 대상: `/Users/kknaks/orca/workspaces/Strong_hajin/strong-hajin-design` · 브랜치 `kknaksss/strong-hajin-design`
모든 경로는 저장소 루트 기준이다. 읽기 전용 — 코드는 한 줄도 바꾸지 않았다.

> ⚠ **`types.ts` 는 없다.** 브리프가 시작점으로 준 `types.ts`·`api.ts` 는 실제로
> `frontend/src/lib/viewModels.ts`(타입) · `frontend/src/lib/api.ts`(호출) 두 자리다.
> 아래 표의 「`types.ts`」 칸은 전부 `lib/viewModels.ts` 를 가리킨다.

---

## 0. 한 줄 요약

**프론트는 선행을 받고도 업무 상세에서 거의 못 그린다** — 그릴 코드(`frontend/src/features/work/WorkModals.tsx:1749-1777`)와
막는 게이트(`:1304`·`:1322`)는 있지만 **그 재료를 `task` prop 에서만 읽고**
(`WorkModals.tsx:991-995`) **상세 조회가 다시 채우지 않는다**(`WorkModals.tsx:574-584` 가
`checklist`·`references`·`delivery`·`children`·`parent` 다섯만 갱신한다). 반면
`predecessors` 는 계약상 **상세 조회에만 실리고**(`frontend/src/lib/viewModels.ts:256-257`),
업무 목록에서 여는 길은 목록 투영을 그대로 넘긴다(`frontend/src/features/work/MyWorkPage.tsx:577-580`·`:1230`).
**선행을 온전히 그리는 화면은 프로젝트 하나뿐이다**(`ProjectTaskPanel`·`ProjectGantt`) —
거기서는 서버가 `ProjectTaskRow.preceding_task_ids` 를 **목록마다** 싣기 때문이다
(`viewModels.ts:116-121`). **후행은 서버에 묻는 호출이 0건**이고 프로젝트 화면이 클라이언트에서
역산한다(`frontend/src/features/project/projectModel.ts:129-146`).

---

## 1. 심볼 개수표 (§6)

`frontend/src/` 전체. `prod` 는 `*.test.*` 를 뺀 수.

| 심볼 | 전체 | prod | test | 주요 자리 |
|---|---:|---:|---:|---|
| `preceding` | 52 | 30 | 22 | `WorkModals.tsx` 19 · `lib/viewModels.ts` 3 · `project/ProjectTaskPanel.tsx` 3 · `project/projectModel.ts` 3 · `lib/api.ts` 2 |
| `predecessor` | 21 | 20 | 1 | `project/projectModel.ts` 7 · `WorkModals.tsx` 5 · `work/workRows.ts` 3 · `lib/labels.ts` 2 · `ProjectTaskPanel.tsx` 2 · `lib/viewModels.ts` 1 |
| `successor` | 8 | 5 | 3 | `ProjectTaskPanel.tsx` 3 · `projectModel.ts` 1 · `lib/labels.ts` 1 |
| `parent_task_id` | 42 | 20 | 22 | `WorkModals.tsx` 8 · `lib/api.ts` 3 · `lib/viewModels.ts` 2 · `projectModel.ts` 2 · `ProjectTaskPanel.tsx` 2 · `action/ActionTaskCard.tsx` 2 · `MyWorkPage.tsx` 1 |
| `reference_task_ids` | 44 | 20 | 24 | `action/ActionTaskCard.tsx` 9 · `WorkModals.tsx` 8 · `lib/api.ts` 2 · `action/ActionMeetingCard.tsx` 1 |
| `blocking` | 64 | 41 | 23 | 아래 갈래표 참조 |
| `section-row` | 8 | 8 | 0 | tsx 6 (`WorkModals.tsx` 5 · `RelationGraphPage.tsx` 1) · css 2 (`styles/components.css`) |
| `drawer-section` | 46 | 46 | 0 | tsx 33 (`WorkModals.tsx` 26 · `action/ActionCenter.tsx` 5 · `graph/RelationGraphPage.tsx` 2) · css 13 (`screens-a.css` 11 · `screens-b.css` 1 · `components.css` 1) |
| `material-list` | 17 | 17 | 0 | tsx 10 (`WorkModals.tsx` 8 · `RelationGraphPage.tsx` 2) · css 7 (`styles/components.css`) |

### `blocking` 41건의 갈래 — **세 가지가 같은 낱말을 쓴다**

| 식별자 | 건수 | 뜻 |
|---|---:|---|
| `blocking` (맨몸) | 16 | 섞임 — `child_progress.blocking`(`viewModels.ts:280`) · `TaskDetailDrawer` 지역 state(`WorkModals.tsx` 안 「막힘」) · `ProjectTaskPanel.tsx:319` 의 `useState` |
| `blockingPredecessorsOf` / `blockingPredecessors` | 6 | **선행** — 시작을 막는 것 (`workRows.ts:113-119`) |
| `blockingChildrenOf` / `blockingChildren` / `blocking_children` / `blockingChildReasonLabel` | 15 | **하위** — 완료를 막는 것 (`workRows.ts:61-75`) |
| `blockingBlocks` | 4 | **캘린더 시간 블록** — 관계와 무관 (`features/calendar/calendarModel.ts:293`) |

---

## 2. 관계 다섯

### 2-1. 상위 ↔ 하위 (`parent_task_id`)

| 물음 | 답 | 근거 |
|---|---|---|
| 타입이 있나 — 이름·모양 | 있다. **읽는 모양이 셋으로 갈린다.** ① `DirectTask.parent?: { task_id; title; state } \| null` ② `DirectTask.children?: TaskChild[]` + `child_progress?: {done,total,blocking?,cancelled?}` ③ `ProjectTaskRow.parent_task_id: string \| null`. 요청에도 `WorkRequest.parent_task_id?: string \| null` 가 있다 | `lib/viewModels.ts:273`·`:275`·`:277-280`·`:116`·`:683` |
| api.ts 의 어느 함수가 보내고 받나 | 보내기: `createDirectTask(..., { parent_task_id })` · `createWorkRequest(..., { parent_task_id })`. 받기: `getTask`(→`parent`·`children`) · `getTaskChildren` · `getProject`(→`tasks[].parent_task_id`) | `lib/api.ts:227`·`:515`·`:158`·`:337`·`:797` |
| **어느 화면이 그리나** | ① 업무 상세 「상위 업무」 구획 — 문장 한 줄 + 여는 단추 ② 업무 상세 「하위 업무」 구획 — 셈(`done/total` · 막는 수 · 취소 수) + 목록 ③ 프로젝트 사이드 패널 「메타 정보」의 `상위 업무` 줄 ④ 프로젝트 사이드 패널 「하위 업무」 블록 ⑤ 프로젝트 간트 트리(깊이 무제한) ⑥ 관계 그래프의 `parent_of` 엣지 ⑦ 생성 모달의 「상위 업무」 Select | `WorkModals.tsx:1779-1795`·`:1806-1878` · `ProjectTaskPanel.tsx:159-168`·`:218-260` · `projectModel.ts:94-108` · `graph/GraphCanvas.tsx:75`·`:90` · `WorkModals.tsx:4496-4516` |
| 만들 수 있나 (입구) | **셋이다.** ① 상세 「하위 업무」 → 「직접 작업 추가」 → `createDirectTask({parent_task_id})` ② 상세 「하위 업무」 → 「하위 요청 보내기」 → `CreateWorkModal({initial:{parentTaskId}})`(상위 고정·수정 불가) ③ 생성 모달의 「상위 업무」 Select | `WorkModals.tsx:1069-1089`·`:998-1006`·`:2123-2140` · `WorkModals.tsx:4496-4516` |
| 지울 수 있나 (입구) | **없다.** `TaskPatch` 에 `parent_task_id` 가 없고 api.ts 에 상위를 떼거나 옮기는 호출이 없다 | `lib/viewModels.ts:538-545` · `lib/api.ts:246-265` |
| 읽기만 되는 곳 | 프로젝트 사이드 패널(`ProjectTaskPanel`) 전부 · 프로젝트 간트 · 관계 그래프 · `readOnly` 인 업무 상세(「하위 업무」 구획이 `!readOnly` 로 가려진다) | `ProjectTaskPanel.tsx:114` · `WorkModals.tsx:1804-1806` |
| 받는데 안 그리는 자리 | **`WorkRequest.parent_task_id` 를 요청 상세가 그리지 않는다** — 타입에 있고 발송 시 실리지만(`V-9`) `WorkRequestDetailDrawer`(`WorkModals.tsx:2655-3305`)에 상위를 보여 주는 자리가 없다. 「이건 무엇의 하위 요청인가」를 요청 화면에서 읽을 수 없다 | `lib/viewModels.ts:683` · `WorkModals.tsx:2655-3305`(`parent` 렌더 0건) |

### 2-2. 선행 ↔ 후행 (`preceding_task_ids` · `predecessors`)

| 물음 | 답 | 근거 |
|---|---|---|
| 타입이 있나 — 이름·모양 | 있다. **두 모양이다.** ① `DirectTask.preceding_task_ids?: string[]` + `DirectTask.predecessors?: Array<{task_id; title: string\|null; state: TaskState\|null}>` — 같은 순서·같은 길이, **볼 수 없는 선행은 `title`·`state` 가 `null` 이고 자리만 남는다** ② `ProjectTaskRow.preceding_task_ids: string[]` — **필수 필드**이고 손자까지 평평하게 전부 실린다 | `lib/viewModels.ts:251-263`·`:116-121` |
| **후행 타입은 있나** | **없다.** 서버가 내는 후행 필드가 프론트 타입에 하나도 없다. 프로젝트 화면이 `successorIndex()` 로 **선행 배열을 뒤집어** 만든다 — 「후행을 서버에 묻는 호출은 0건이다(D-07)」 | `projectModel.ts:129-146` · `ProjectTaskPanel.tsx:40` |
| api.ts 의 어느 함수가 보내고 받나 | **보내기 둘뿐이다** — `createDirectTask(..., { preceding_task_ids })` · `createWorkRequest(..., { preceding_task_ids })`. 받기: `getTask`(→`predecessors`) · `getProject`(→`tasks[].preceding_task_ids`). **PATCH·DELETE 표면이 없다** | `lib/api.ts:234-235`·`:517-518`·`:158`·`:797` |
| **어느 화면이 그리나** | ① 업무 상세 「선행업무」 구획 — 목록 + 미완 배지 + 숨은 건수 + 막힘 문장 ② 업무 상세 상단 액션 줄의 「시작」·「완료 처리」 비활성 + 그 아래 `.scax-blocked-note` ③ 행 액션(`TaskQuickActions`)의 「시작」 비활성 ④ 프로젝트 사이드 패널 「관계」 블록 — `선행`/`후행` 두 `RelationBlock` ⑤ 프로젝트 간트 의존선 SVG(직각 3구간 + 후행 화살표) + 「접힌 선」 배지 + 「자리 못 찾은 선」 경고 ⑥ 생성 모달 「선행 업무」 `fieldset`(표 + 칩) ⑦ 생성 모달 「프로젝트」 Select 잠금 | `WorkModals.tsx:1749-1777` · `:1304`·`:1322`·`:1324` · `:2575-2576` · `ProjectTaskPanel.tsx:222-223`·`:405-447` · `ProjectGantt.tsx:62`·`:272-275`·`:289-320` · `WorkModals.tsx:4587-4622` · `:4536-4542` |
| 만들 수 있나 (입구) | **생성 모달의 「선행 업무」 표 하나뿐이다.** 두 갈래(`업무`·`요청`) 모두 그 값을 싣는다. **프로젝트를 먼저 골라야 표가 뜬다** — 안 고르면 「프로젝트를 먼저 선택하면…」 문장만 선다 | `WorkModals.tsx:4587-4622`·`:3896`·`:3967`·`:4127-4137` |
| 지울 수 있나 (입구) | **만든 뒤에는 없다.** 생성 모달 안에서만 칩의 「빼기」로 뺀다(`Chip onClick`). 저장된 업무의 선행을 떼는 UI·API 가 하나도 없다 | `WorkModals.tsx:4603-4615` · `lib/viewModels.ts:538-545`(`TaskPatch` 에 없음) · `lib/api.ts`(선행 mutation 0건) |
| 읽기만 되는 곳 | 업무 상세 「선행업무」 구획(단추는 「열기」뿐) · 프로젝트 사이드 패널 「관계」 · 프로젝트 간트 의존선 | `WorkModals.tsx:1750-1777` · `ProjectTaskPanel.tsx:405-447` |
| **받는데 안 그리는 자리** | **넷이다.** ① 업무 상세가 `predecessors` 를 **상세 조회로 다시 읽지 않는다** — §3-1 ② **후행이 업무 상세에 없다** — 프로젝트 화면만 그린다 ③ `WorkRequest` 타입에 `preceding_task_ids` 가 **없다** — 보낼 때는 싣는데 받을 때 읽을 자리가 없고 요청 상세도 안 그린다 ④ `ActionTaskCard` 의 `TaskDraft` 에 `preceding_task_ids` 가 없어 서버 `edit_contract` 가 그 필드를 내도 **sanitize 가 떨어뜨린다** | `WorkModals.tsx:574-584` · `WorkModals.tsx:384-2175`(후행 0건) · `lib/viewModels.ts:644-692` · `features/action/ActionTaskCard.tsx:19-29`·`:85-100` |

### 2-3. 참고 (`reference_task_ids` · `references`)

| 물음 | 답 | 근거 |
|---|---|---|
| 타입이 있나 — 이름·모양 | 있다. `TaskReference = { reference_id; created_by; created_at?; task: {task_id; title; state; due_date?; assignee?} \| null; task_version? }` — **`task` 가 `null` 이면 「볼 수 없는 업무」**다. `DirectTask.references?: TaskReference[]` · `WorkRequest.references?: TaskReference[]` | `lib/viewModels.ts:353-361`·`:269`·`:657` |
| api.ts 의 어느 함수가 보내고 받나 | 보내기: `addTaskReference(taskId, referencedTaskId)` · `releaseTaskReference(taskId, referenceId)` · 생성 payload 의 `reference_task_ids`(두 갈래). 받기: `getTask` · `getWorkRequest` | `lib/api.ts:174`·`:182`·`:226`·`:514`·`:158`·`:483` |
| **어느 화면이 그리나** | ① 업무 상세 「참고 업무」 구획 — 목록 + 연결/해제 ② 요청 상세 「참고 업무」 구획(`aria-label="요청 참고 업무"`) — **읽기 전용** ③ 생성 모달 「참고 업무」 `fieldset` ④ AX 판단 카드의 `TaskAttachmentGroup` — 참고 업무 칩 + 검색 추가/제거 ⑤ 관계 그래프의 `refers_to` 엣지 | `WorkModals.tsx:1880-1944` · `:3013-3040` · `:4558-4577` · `action/ActionTaskCard.tsx:625-780` · `graph/GraphCanvas.tsx:76`·`:91` |
| 만들 수 있나 (입구) | **넷이다.** ① 업무 상세 「업무 연결」 → `addTaskReference` ② 생성 모달 「참고 업무」 표 ③ AX 판단 카드의 첨부 그룹(`searchReferences`) ④ 회의 승격 카드(`ActionMeetingCard`) | `WorkModals.tsx:1889-1893`·`:1113-1116` · `:4558-4577` · `ActionTaskCard.tsx:765-772` · `features/action/ActionMeetingCard.tsx`(`reference_task_ids` 1건) |
| 지울 수 있나 (입구) | **된다** — 업무 상세의 「연결 해제」가 `releaseTaskReference` 를 부른다. AX 카드에서도 칩 제거로 draft 에서 뺀다 | `WorkModals.tsx:1915-1919`·`:1125-1131` · `ActionTaskCard.tsx:714` |
| 읽기만 되는 곳 | 요청 상세의 「요청 참고 업무」 · `readOnly` 업무 상세(구획 자체가 `!readOnly` 로 가려진다) · 관계 그래프 | `WorkModals.tsx:3013-3040` · `:1880-1881` |
| 받는데 안 그리는 자리 | `TaskReference.created_by`·`created_at` 을 **어느 화면도 안 그린다** — 「누가 언제 이었나」가 타입에만 있다 | `lib/viewModels.ts:354-355` · `WorkModals.tsx:1884-1925`(그 둘 렌더 0건) |

### 2-4. 프로젝트 소속 (`project_id`)

| 물음 | 답 | 근거 |
|---|---|---|
| 타입이 있나 — 이름·모양 | 있다. `DirectTask.project_id?: string \| null` · `ProjectTaskRow`(프로젝트 상세의 업무 행) · `GraphNode.project_id?` · `TaskPatch.project_id?: string \| null`(「`null` 이면 프로젝트에서 뗀다」) | `lib/viewModels.ts:242`·`:110-138`·`:14`·`:543-544` |
| api.ts 의 어느 함수가 보내고 받나 | 보내기: `createDirectTask({project_id})` · `createWorkRequest({project_id})` · `updateTask(patch.project_id)`(→ 값이 있으면 `project_id`, 없으면 `clear_project: true`). 받기: `listProjects` · `getProject` · `getTask` | `lib/api.ts:228`·`:516`·`:258-261`·`:793`·`:797` |
| **어느 화면이 그리나** | ① 프로젝트 화면 전부 — 레일·요약 스트립·간트·사이드 패널 ② 생성 모달 「프로젝트」 Select ③ 생성 모달의 업무 고르기 표 한 줄(`scax-pick-table__meta`)에 프로젝트 이름 ④ 관계 그래프의 `프로젝트로 묶기` 보기 · `project` 노드 | `features/project/ProjectPage.tsx` 전체 · `WorkModals.tsx:4526-4543` · `:3423` · `graph/RelationGraphPage.tsx:14` · `graph/GraphCanvas.tsx:61` |
| 만들 수 있나 (입구) | **생성 모달의 「프로젝트」 Select 하나뿐이다.** 선행을 고른 상태에서는 **잠긴다**(`disabled`) | `WorkModals.tsx:4526-4543` |
| 지울 수 있나 (입구) | **없다.** `TaskPatch.project_id` 와 `clear_project` 가 api.ts 에 살아 있지만 **그 patch 를 만드는 호출자가 0건**이다 — `updateTask` 를 부르는 네 자리(`CalendarPage:248`·`:559` · `TodayPage:214` · `MyWorkPage:481`)가 모두 제목·설명·날짜만 싣는다 | `lib/api.ts:258-261` · `WorkModals.tsx:778-783`(patch 조립: title·description·start_date·due_date 넷뿐) |
| 읽기만 되는 곳 | 프로젝트 화면 전부(업무의 소속을 그 화면에서 바꿀 수 없다) · 생성 모달의 고르기 표 | `ProjectPage.tsx` · `WorkModals.tsx:3423` |
| **받는데 안 그리는 자리** | **업무 상세 서랍이 프로젝트를 한 글자도 안 그린다.** `DirectTask.project_id` 가 오는데 `TaskDetailDrawer`(`WorkModals.tsx:384-2175`) 안에 `project` 렌더가 **0건**이다 — 구획도, `meta-grid` 칸도 없다. 「이 업무가 어느 프로젝트인가」를 업무 화면에서 읽을 수 없다 | `lib/viewModels.ts:242` · `WorkModals.tsx:384-2175`(`project` 는 `:424`·`:573` 주석의 “projection” 두 건뿐) |

### 2-5. 요청 ↔ 수락으로 생긴 업무

| 물음 | 답 | 근거 |
|---|---|---|
| 타입이 있나 — 이름·모양 | 있다. **네 모양이 같은 사실을 가리킨다.** ① `WorkRequest.task_id: string \| null` ② `TaskLineage.source_work_request_id`(+ `source_task_id`·`source_action_item_id` 등 7칸) ③ `TaskOrigin = { kind: "self_created"\|"work_request"\|"direct_assignment"; actor_role; actor; source }` ④ `ActionItemEnvelope.derived_task_id` | `lib/viewModels.ts:672`·`:455-463`·`:400-405`·`:738` |
| api.ts 의 어느 함수가 보내고 받나 | 만들기: `createWorkRequest` → `decideWorkRequest`(수락) → `getTask`. 잇기: `resubmitWorkRequest` · `createWorkRequest({supersedes_request_id})`. 받기: `getWorkRequest` · `getWorkRequestInbox` · `getTask` | `lib/api.ts:504`·`:613`·`:956`·`:519`·`:483`·`:479`·`:158` |
| **어느 화면이 그리나** | ① 요청 상세 `meta-grid` 의 「생성된 업무」 칸 — 「파생 업무 보기」/「생성됨 · 담당 수락 대기」/「아직 없음」 ② 업무 상세 상단 `.origin-chip` — 「○○가 보낸 업무」 배지 + 출처 열기 단추 ③ 내 업무 목록의 수신함/「보낸 업무」 탭 갈래 ④ 관계 그래프의 `produced`·`requested`·`asked_of` 엣지 ⑤ 하위 취소 사유 「취소됨 — 요청 거절」 | `WorkModals.tsx:2969-2983` · `:1531-1548`·`:376-382` · `work/workRows.ts:28-30`·`:168-172` · `graph/GraphCanvas.tsx:72-74`·`:86-88` · `WorkModals.tsx:1838-1841` |
| 만들 수 있나 (입구) | **요청 발송 → 수락**. 발송은 `CreateWorkModal` 의 「요청」 갈래(호출 자리 6곳: `MyWorkPage:1302` · `TodayPage:442` · `CalendarPage:645` · `MeetingDetailPage:1289` · `WorkModals:2125`(하위 요청)). 수락은 요청 상세의 `decideWorkRequest` | `WorkModals.tsx:3444`·`:3940-3970` · `lib/api.ts:613` |
| 지울 수 있나 (입구) | 연결 자체는 못 끊는다. **요청을 철회/거절**하면 파생 업무가 취소된다(원장이 남는다) — `withdrawWorkRequest` · `decideWorkRequest(reject)` | `lib/api.ts:641`·`:613` · `WorkModals.tsx:3111`(주석 「거절하면 그 Task 가 취소된다」) |
| 읽기만 되는 곳 | 업무 상세의 `.origin-chip` · 참고 수신함(`readOnly` 요청 상세) · 관계 그래프 | `WorkModals.tsx:1531-1548` · `:2991` |
| 받는데 안 그리는 자리 | `TaskLineage` 7칸 중 **화면이 읽는 것은 `source_work_request_id` 하나**다(`workRows.ts:29`·`:169`). `request_thread_id`·`source_decision_item_id`·`source_submission_id`·`source_review_decision_id`·`source_action_item_id`·`source_task_id` **여섯은 어디에도 안 그린다** | `lib/viewModels.ts:455-463` · `workRows.ts:29`·`:169` |

---

## 3. 선행·후행 — §4 의 다섯 물음

### 3-1. 네 값은 어디서 오고 어디에 그려지나

넷 다 **한 자리에서 한 번에** 만들어진다 — `WorkModals.tsx:991-995`.

| 값 | 어디서 오나 | 어디에 그려지나 |
|---|---|---|
| `blockingPredecessors` | `blockingPredecessorsOf(task)` — **`task` prop** 의 `predecessors` 에서 `title !== null && state ∉ {done, cancelled}` 를 고른다 (`workRows.ts:113-119`) | **그 자체로는 안 그린다.** 제목만 뽑아 `blockedText` 로 바뀌고(`:993`) 그 문장이 두 자리에 선다 — 액션 줄의 `.scax-blocked-note`(`:1324`)와 「선행업무」 구획의 `.danger-text`(`:1776`) |
| `visiblePredecessors` | `visiblePredecessorsOf(task)` — `title !== null && state !== null` (`workRows.ts:130-136`) | **「선행업무」 구획의 `ul.material-list`** — 제목 단추 + 상태. 미완이면 `Badge tone="danger"`, 끝났으면 `span.t-meta` (`:1752-1773`) |
| `hiddenPredecessors` | `hiddenPrecedingCountOf(task)` — 배열 안 `title === null` 인 **빈 자리의 수** (`workRows.ts:125-127`) | 같은 구획 맨 아래 `p.t-meta` — 「볼 수 없는 선행업무 N건」(`:1775` · `labels.ts:318-320`) |
| `startBlockedByPredecessors` | `task.state === "open" && blockingPredecessorsOf(task).length > 0` (`workRows.ts:142-147`) | **단추 셋의 `disabled`** — 상세의 「시작」(`:1304`) · 상세의 「완료 처리」(`:1322`) · 행 액션 `TaskQuickActions`(`:2575`). 그 아래 `blockedText` 가 선다(`:1324`) |

**넷 모두 `task` prop 만 읽는다.** `current`(버전 반영본, `:537`)도 상세 조회 결과도 아니다.

### 3-2. 업무 상세 서랍에 선행을 보여 주는 자리가 있나

**있다 — `aria-label="선행업무"` 구획 하나.** `WorkModals.tsx:1749-1777`.
모양은 **목록 + 배지 + 문장** 셋이 겹쳐 있다:

- `ul.material-list` 의 줄마다 제목(여는 단추) + 상태 (`:1752-1773`)
- 미완 선행은 `Badge tone="danger"` (`:1766`)
- 볼 수 없는 선행은 제목 없이 건수 한 줄 (`:1775`)
- `startBlocked` 면 「끝나지 않은 선행업무가 있습니다: …」 (`:1776` · `labels.ts:310-312`)
- **`(task.predecessors ?? []).length > 0` 일 때만 구획 자체가 선다** (`:1749`) — 비면 줄이 없다

**그러나 값만 받고 버리는 갈래가 있다.** 상세 조회 effect(`:574-584`)가
`setChecklist`·`setReferences`·`setDelivery`·`setChildren`·`setParentTask` **다섯만** 부르고
`predecessors` 를 담는 state 자체가 없다. `predecessors` 는 계약상
**상세 조회에만 실리므로**(`viewModels.ts:256-257`), 목록에서 연 서랍에는 그 값이 없고
**구획도 게이트도 통째로 사라진다**. 목록에서 여는 길이 바로 그것이다 —
`MyWorkPage.tsx:577-580` 의 `openMyTask(task)` 가 `getMyWork()`/`getTasks()` 결과 행(`:284-285`)을
그대로 `detailStack` 에 넣고, `:1230` 이 그 `detail.task` 를 prop 으로 넘긴다.
반면 상세 안에서 다른 업무로 따라 들어가는 길(`pushDerivedTask`, `MyWorkPage.tsx:587-596` · 배선 `:1223`)은
`getTask(taskId)` 를 거치므로 **같은 서랍인데 선행이 보인다.**
`Predecessors.test.tsx` 는 `task` prop 에 `predecessors` 를 직접 넣어 렌더하므로
(`Predecessors.test.tsx:64-86`) 이 갈래를 타지 않는다.

> ⚠ 서버가 목록 투영에도 `predecessors` 를 싣는지는 **이 조사(프론트 전수)로 확인하지 않았다**
> — 프론트 타입의 문서화된 계약(`viewModels.ts:256-257`)만 근거로 적는다. §6 참조.

### 3-3. 선행을 만드는 입구 — 생성 모달 말고 또 있나

**없다.** 입구는 `CreateWorkModal` 의 「선행 업무」 `fieldset` **하나뿐**이다 (`WorkModals.tsx:4587-4622`).

- 후보는 **고른 프로젝트 안에서 내가 읽을 수 있는 업무**로 좁혀진다 — 새 조회를 열지 않고
  이미 읽어 둔 `referenceChoices` 를 `row.project_id === projectId` 로 거른다 (`:4127-4137`)
- 자기가 고른 상위(`parentTaskId`)와 이미 고른 선행은 후보에서 빠진다 (`:4133-4136`)
- 프로젝트를 안 골랐으면 표 대신 안내 문장 (`:4617-4619`)
- 고른 것은 `ChipRow` 로 서고 칩마다 「빼기」 (`:4603-4615`)
- 두 갈래 모두 실제로 보낸다 — `preceding_task_ids` (`:3896` 업무 · `:3967` 요청)
- 그 값이 있으면 「프로젝트」 Select 가 잠긴다 (`:4536-4542` · `labels.ts:315`)

**만든 뒤에 선행을 더하거나 빼는 입구는 프론트 전체에 0건이다** —
`TaskPatch` 에 없고(`viewModels.ts:538-545`), api.ts 에 선행 mutation 함수가 없다.

### 3-4. 후행(나를 선행으로 삼는 업무)을 보여 주는 자리

**업무 상세에는 없다.** `TaskDetailDrawer`(`WorkModals.tsx:384-2175`) 안에 `successor`·「후행」 렌더 0건.

**프로젝트 화면에만 둘 있다.**

1. **프로젝트 사이드 패널 「관계」 블록** — `RelationBlock icon="arrow-down" label="후행"`
   (`ProjectTaskPanel.tsx:223` · 라벨 `labels.ts:1015`). 재료는
   `successorIndex(tasks).get(row.task_id)` (`ProjectTaskPanel.tsx:100`) —
   **그 프로젝트 업무 전부의 `preceding_task_ids` 를 클라이언트가 뒤집어 만든다**
   (`projectModel.ts:129-146`). 「후행을 서버에 묻는 호출은 0건이다(D-07)」(`projectModel.ts:130-132`)
2. **프로젝트 간트 의존선** — SVG 직각 3구간 + **화살표가 후행을 가리킨다**
   (`ProjectGantt.tsx:289`·`:302-320` · `projectModel.ts:379-382`)

**후행 전용 타입·API 는 프론트에 존재하지 않는다** (`successor` prod 5건이 전부
`projectModel.successorIndex` 와 그 소비처 · 라벨 하나).

### 3-5. `RelationGraphPage` 는 관계 다섯 중 무엇을 그리나 — 선행이 거기 있나

**선행은 없다.** 그래프가 아는 엣지 종류는 **일곱**이고(`graph/GraphCanvas.tsx:69-93`),
`precedes`·`preceding` 류가 그중에 없다.

| 엣지 `kind` | 짧은 이름 | 문장(들어옴 / 나감) | 관계 다섯 중 |
|---|---|---|---|
| `parent_of` | 하위 업무 | 상위 업무 / 하위 업무 | **① 상위↔하위** |
| `refers_to` | 참고 업무 | 이 업무를 참고한 업무 / 참고 업무 | **③ 참고** |
| `produced` | 만든 업무 | 이 업무를 만든 요청 / 이 요청이 만든 업무 | **⑤ 요청→업무** |
| `requested` | 보낸 요청 | 이 요청을 보낸 사람 / 보낸 요청 | ⑤ 주변 |
| `asked_of` | 요청받은 사람 | 요청받은 사람 / 요청받은 사람 | ⑤ 주변 |
| `holds` | 담당 | 담당 / 담당 중인 업무 | 담당(관계 다섯 밖) |
| `has_material` | 자료 | 붙어 있는 업무 / 참고 자료·산출물 | 자료(관계 다섯 밖) |

근거: `GraphCanvas.tsx:69-78`(`EDGE_LABEL`) · `:85-93`(`EDGE_SENTENCE`).

- **④ 프로젝트 소속**은 엣지가 아니라 **보기 모드**로만 있다 — `프로젝트로 묶기`
  (`RelationGraphPage.tsx:14` · `GraphView = "member"|"team"|"project"`, `viewModels.ts:54`).
  `project` 는 노드 종류로도 선다 (`GraphCanvas.tsx:61`)
- **② 선행↔후행은 노드로도 엣지로도 없다**
- 모르는 `kind` 는 **지어내지 않고 자기 이름을 그대로 쓴다**
  (`RelationGraphPage.tsx:351`·`:423` 의 `?? edge.kind`) — 서버가 선행 엣지를 내기 시작하면
  화면에는 **한국어 문장 대신 `kind` 문자열이 날것으로** 뜬다

---

## 4. 업무 상세 서랍 구획 목록 (§5)

`TaskDetailDrawer` (`frontend/src/features/work/WorkModals.tsx:384-2175`)가
`<Shell>` 자식으로 **위에서 아래로** 그리는 것 전부. 조건이 붙은 것은 조건도 적었다.

| 순서 | 구획 (`aria-label`) | 무엇을 보여 주나 | 편집 입구 | 파일:줄 |
|---:|---|---|---|---|
| — | (머리) `headerExtra` | 상태 배지 · 「기한 초과」 · `v{version}` | 없음 | `WorkModals.tsx:1360-1366` |
| — | (아래) `Shell footer` | 취소/취소 제안/조건 변경 제안/변경 저장/막힘/**시작**/**완료 처리**/완료 보고/재개/닫기 + 선행 막힘 문장 | 명령 단추 | `:1261-1352` |
| 1 | `완료 확인 대기` (조건: `awaitingReview`) | 보고 대기 문장 · 보고한 결과 요약 | 「완료 인정」·「보완 요청」 | `:1378-1397` |
| 2 | `보완 필요` (조건: `delivery.status==="awaiting_revision"`) | 보완 사유 · 회차 | 없음(읽기) | `:1399-1405` |
| 3 | `담당 변경 대기` (조건: `assignments.pending`) | 현 담당 + 제안받은 담당 · 거절 사유 | 없음(읽기) | `:1411-1421` |
| 4 | `응답 대기 제안` (조건: `pendingProposal`) | 제안 종류·사유·바뀔 조건(`meta-grid`) | 「동의」·「동의하지 않음」·「제안 철회」 | `:1428-1464` |
| 5 | `완료를 막는 하위` (조건: 목록 비지 않음) | 막는 하위 이름 + 이유 라벨 | 이름 단추(열기)만 | `:1474-1488` |
| 6 | (무라벨 `div.form-stack`) | ↓ 6-a~6-f 를 감싼다 | — | `:1489-1691` |
| 6-a | `div.handover` (조건: `canAssign && !readOnly`) | 담당자 변경 폼(대상 Select + 사유) | 「담당자 변경」→「변경」 | `:1490-1527` |
| 6-b | `p[aria-label="업무 출처"]` (조건: `task.origin`) | 「○○가 보낸 업무」 배지 + 출처 열기 | 없음(읽기·이동) | `:1528-1548` |
| 6-c | (무라벨) 제목 | `input.title-input` | 인라인 편집 → 머리의 「변경 저장」 | `:1549-1552` |
| 6-d | (무라벨) `dl.meta-grid` | **담당자 · 시작일 · 기한** 셋 | 날짜 둘은 `DateField` 인라인 | `:1553-1576` |
| 6-e | `체크리스트` (조건: `!readOnly`) | `done/total` · `ProgressBar` · 항목 목록 | 추가·수정·삭제·순서(위/아래)·체크 | `:1578-1678` |
| 6-f | (무라벨) 업무 내용 | `textarea.task-description` | 인라인 편집 → 「변경 저장」 | `:1679-1690` |
| 7 | (무라벨) 막힘 사유 (조건: `task.block_reason`) | 저장된 막힘 사유 | 없음(읽기) | `:1692-1697` |
| 8 | `막힘 사유 입력` (조건: `isBlocking`) | 사유 입력칸 + 도움말 | 「막힘 처리」·「입력 취소」 | `:1708-1741` |
| 9 | **`선행업무`** (조건: `task.predecessors.length > 0`) | 선행 목록 + 미완 배지 · 숨은 건수 · 막힘 문장 | **없음 — 읽기 전용** | `:1749-1777` |
| 10 | `상위 업무` (조건: `parentTask`) | 「이 업무는 ○○의 하위 업무입니다」 + 상태 | **없음 — 읽기 전용** | `:1779-1795` |
| 11 | `하위 업무` (조건: `!readOnly`) | `done/total` · 막는 수 · 취소 수 · 하위 목록(상태·기한·담당·「미완결」 배지) | 「직접 작업 추가」·「하위 요청 보내기」 | `:1804-1878` |
| 12 | `참고 업무` (조건: `!readOnly`) | 참고 목록(상태·기한·담당) · 「볼 수 없는 업무」 | 「업무 연결」·「연결 해제」 | `:1880-1944` |
| 13 | (무라벨) 참고 자료 — `renderMaterials("input")` | 파일·링크·리소스 목록 + 추출 상태 | 「파일 추가」·「링크 추가」·떼기 | `:1150-1175`(구획) · `:1951` (호출) |
| 14 | (무라벨) 산출물 — `renderMaterials("output")` | 위와 같은 한 벌, `kind="output"` | 같음 | `:1150-1175` · `:1952` |
| 15 | `활동·이력` — `TaskHistorySection` | 필터 4개(전체/내용·상태/체크리스트/자료) · 버전 줄 · 펼치면 `dl[aria-label="변경 내용"]` diff | 「변경 내용」 펼치기만 | `:182-305`(구획 `:223`) · `:1953`(호출) |
| 16 | (무라벨) `AX` (조건: `onAskAx`) | 「AX에게 이 업무 묻기」 | 단추(패널로 넘김) | `:1954-1970` |

**서랍에 없는 것 — 다시 설계의 구멍 후보**

- **프로젝트 소속** 구획도 칸도 없다 (§2-4)
- **후행** 구획이 없다 (§3-4)
- 선행·상위 두 관계는 **읽기 전용**이다 — 고칠 입구가 서랍에 없다
- `readOnly` 일 때 9·10(선행·상위)은 남고 11·12·13·14(하위·참고·자료 두 벌)는 통째로 사라진다
  (`:1804`·`:1880`·`:1151`)

---

## 5. 받는데 안 그리는 것 / 그리는데 못 고치는 것

### 5-1. 받는데 안 그린다

| # | 값 | 받는 자리 | 안 그리는 자리 |
|---:|---|---|---|
| 1 | `DirectTask.predecessors` (상세 조회) | `lib/viewModels.ts:256-263` | **업무 상세가 상세 조회로 다시 안 읽는다** — `WorkModals.tsx:574-584` 가 다섯만 갱신하고 `predecessors` state 가 없다. 목록에서 연 서랍은 §3-2 처럼 구획도 게이트도 없다 |
| 2 | `DirectTask.project_id` | `lib/viewModels.ts:242` | **업무 상세 서랍 전체에 `project` 렌더 0건** — `WorkModals.tsx:384-2175` |
| 3 | `WorkRequest.parent_task_id` | `lib/viewModels.ts:683` | 요청 상세에 상위를 보여 주는 자리가 없다 — `WorkModals.tsx:2655-3305` |
| 4 | `TaskLineage` 6칸 (`request_thread_id`·`source_decision_item_id`·`source_submission_id`·`source_review_decision_id`·`source_action_item_id`·`source_task_id`) | `lib/viewModels.ts:455-462` | 화면이 읽는 것은 `source_work_request_id` 하나 — `workRows.ts:29`·`:169` |
| 5 | `TaskReference.created_by`·`created_at` | `lib/viewModels.ts:354-355` | 참고 목록이 제목·상태·기한·담당만 그린다 — `WorkModals.tsx:1896-1913` |
| 6 | `WorkRequest.superseded_by_request_id` | `lib/viewModels.ts:687` | 요청 상세에 「이 요청 뒤에 선 새 요청」을 보여 주는 자리가 없다 — `WorkModals.tsx:2655-3305`(렌더 0건) |
| 7 | `edit_contract` 의 선행 필드(만약 서버가 낸다면) | `ActionEditContract.fields` — `lib/viewModels.ts:825-831` | `TaskDraft` 에 `preceding_task_ids` 가 없어 `taskDraft()` sanitize 가 떨어뜨린다 — `ActionTaskCard.tsx:19-29`·`:85-100`. 서버 계약을 실제로 확인하지는 못했다(§6) |
| 8 | `TaskHistory` 의 선행·상위 변경 | `lib/viewModels.ts:363-387` | `HISTORY_FIELD_LABEL` 이 아는 필드는 9개(title·description·state·block_reason·start_date·due_date·assignee·checklist·materials) — 관계 필드가 하나도 없어 diff 에 뜨면 **필드 이름이 날것으로** 나온다. `WorkModals.tsx:152-164`·`:277-290` |

### 5-2. 그리는데 못 고친다 (읽기 전용)

| # | 관계 | 그리는 자리 | 고칠 입구 |
|---:|---|---|---|
| 1 | **선행** | 업무 상세 「선행업무」(`WorkModals.tsx:1750-1777`) · 프로젝트 사이드 「선행」(`ProjectTaskPanel.tsx:222`) · 간트 의존선(`ProjectGantt.tsx:289-320`) | **생성 모달 하나뿐**(`WorkModals.tsx:4587`). 만든 뒤 더하기·빼기 **0건** — `TaskPatch` 에 없고 api.ts 에 mutation 없음 |
| 2 | **후행** | 프로젝트 사이드 「후행」(`ProjectTaskPanel.tsx:223`) · 간트 화살표(`ProjectGantt.tsx:289`) | 없다 — 역산값이라 고칠 대상 자체가 선행이다(`projectModel.ts:129-146`) |
| 3 | **상위** | 업무 상세 「상위 업무」(`WorkModals.tsx:1779-1795`) · 프로젝트 사이드 메타(`ProjectTaskPanel.tsx:159-168`) | 만들기만 셋(§2-1). **떼기·옮기기 0건** |
| 4 | **프로젝트 소속** | 프로젝트 화면(`ProjectPage.tsx` 전체) | 생성 모달 Select 하나. `TaskPatch.project_id`·`clear_project` 가 api.ts 에 살아 있으나 **호출자 0건**(`lib/api.ts:258-261`) |
| 5 | **참고** | 업무 상세·요청 상세·AX 카드 | **온전하다** — 더하기(`addTaskReference`)·빼기(`releaseTaskReference`) 둘 다 있다(`lib/api.ts:174`·`:182`) |

### 5-3. 낱말이 갈린다

- **`blocking` 이 세 가지를 가리킨다** — 선행(`blockingPredecessorsOf`) · 하위(`blockingChildrenOf`) ·
  캘린더 시간 블록(`blockingBlocks`). §1 갈래표
- **선행의 한국어가 두 가지다** — 업무 화면은 「선행업무」(붙여 씀, `WorkModals.tsx:1751` ·
  `labels.ts:310-320`), 프로젝트 화면은 「선행」(`labels.ts:1014`). 후행은 프로젝트 화면에만
  「후행」(`labels.ts:1015`)으로 있다
- **`predecessors` / `preceding_task_ids` 두 이름이 같은 사실을 가리킨다** — 업무 상세는
  요약 배열(`predecessors`)을, 프로젝트는 id 배열(`preceding_task_ids`)을 읽는다
  (`viewModels.ts:255`·`:263`·`:121`)

---

## 6. 조사 한계

1. **백엔드를 읽지 않았다.** 「서버가 목록 투영에 `predecessors` 를 싣는가」는
   프론트 타입의 문서화된 계약(`viewModels.ts:256-257` 「상세 조회에만 실린다」)만 근거로 적었다.
   실제 응답은 backend 워커의 리포트와 맞춰야 확정된다. §3-2 의 「목록에서 연 서랍에는 선행이 없다」는
   **그 계약이 참일 때** 성립한다 — 코드 구조상 「상세 조회가 `predecessors` 를 다시 읽지 않는다」는
   부분(`WorkModals.tsx:574-584`)은 서버와 무관하게 참이다.
2. **서버의 `edit_contract.fields` 실목록을 확인하지 못했다.** §5-1 #7 은
   「서버가 선행 필드를 내면 프론트가 떨어뜨린다」는 조건부 진술이다 — 프론트 쪽 sanitize 는
   확정(`ActionTaskCard.tsx:85-100`), 서버가 그 필드를 내는지는 미확인.
3. **브라우저로 확인하지 않았다.** 지시대로 서버·프론트를 띄우지 않았고 테스트·빌드도 돌리지 않았다.
   렌더 조건은 JSX 를 읽어 판정했다.
4. **CSS 계산 결과는 보지 않았다.** `drawer-section` 13건·`material-list` 7건·`section-row` 2건이
   CSS 에 있지만 그 규칙이 실제로 무엇을 숨기는지(예: `display:none`)는 확인하지 않았다.
5. **`chat/`·`meetings/`·`report/`·`org/` 는 관계 다섯의 렌더가 0건임만 확인**하고
   (`grep "선행\|후행\|상위 업무\|하위 업무\|참고 업무"` 결과 해당 파일 없음) 내부를 읽지는 않았다.
   `MeetingDetailPage.tsx:1289` 는 `CreateWorkModal` 호출 자리로만 셌다.
6. **생성 모달의 「선행 업무」 후보가 실제로 채워지는 조건**(`referenceChoices` 가 어떤 조회로 오는지)은
   `getTasks(include_closed)` 를 거른다는 주석(`WorkModals.tsx:4124-4126`)까지만 확인했고
   그 조회의 실응답은 보지 않았다.
