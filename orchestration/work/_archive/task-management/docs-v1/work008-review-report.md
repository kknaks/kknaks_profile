# WORK-008 검수 — 종료 · 통합 · 편집 · 업무 연동

- 검수 대상: `kknaksss/docs-v1` `ac9ee5b..580846a`(a48cbe2 BE Phase 1·2 · a5ae4c6 FE Phase 3·4·6 · 580846a Phase 5). 82 파일 · +10,210 / −205
- 기준 문서: DEC-003 §1 표·§4·§5·§6·§7 · DEC-002 §4 · BE §5-3·§6·§7·§8-2·§8-3·§12 · FE §2·§3-3~3-5·§6·§8·§11 · ERD `meeting.md` M-5~M-8-a·M-14·M-19·M-20 · SPEC-008 §2 U-1~U-11·§4·§5·§6 · SPEC-004 §4 L478 · SPEC-003 §4 · WORK-008 Phase 1~6 · WORK-005 L137·L147·L294
- 방식: read-only. 코드·테스트를 **읽었고 돌리지 않았다.** 워커 3명의 worker_done 본문(코디 인박스 2026-09-06 18:23 · 18:54 · 19:38 · 19:41 · 20:16)을 함께 대조했다.

## 0. 판정 요약

| 판정 | 수 | 항목 |
|---|---|---|
| **FAIL** | **1** | F-1 `features/meetings → features/tasks` 배럴 import 4건(드로어 아님 — 훅·API·전이표·타입). FE §2 규칙 4 위반 · WORK-006 W-1/G-5 재발 |
| **WARN** | **5** | W-1 목록 미리보기 `ended` 통합본 트리가 플레이스홀더로 남음(소유 공백 · 사용자 가시) · W-2 501 `SurfaceNotImplementedError` 죽은 클래스 · W-3 AI 탭 「종결 · HH:MM」 시각이 통합 시각(+`mergedSummary.integratedAt` 계약 밖 필드) · W-4 job 의 「①을 돌리는가」가 프로세스 메모리(`_plans`) · W-5 `MeetingStatusPlaceholder.tsx` 죽은 파일 |
| **문서 공백** | **13** | §5 — 가장 큰 것은 DG-1(ERD M-20 ↔ SPEC-008 「뒤 줄 당김」 모순) · DG-2(「종결 · HH:MM」의 원천 필드 없음) · DG-4(FE §2 규칙 4 — 제공 영역 배럴의 자리, G-5 세 번째) · DG-10(목록 미리보기 `ended` 트리 소유 공백) · DG-13(SPEC-008 U-9 유형 배지 ↔ SPEC-003 후보 응답에 `workType` 없음) |
| **완료 게이트 우회** | **0건** | §1-1 — 4항목 전부 내가 grep 으로 확인. `task_service.py` 변경 0 |
| **통과 판정의 정직성** | **위장 0건** | §1-7 — 워커 3명 모두 「실물 확인 필요」를 남겼고, 테스트로 옮겼다고 적은 항목은 전부 단언이 있다 |

**한 줄로:** 이 work 의 핵심(게이트 우회 0 · 모델 본문 안 읽음 · 삭제 경계 DB 전후 · 공용 부품 재사용)은 **전부 지켜졌다.** 뚫린 곳은 하나 — 직전 라운드에 닫은 「영역 사이 import 0」이 배럴 import 라는 옆문으로 다시 열렸다. 그 옆문은 워커가 판 것이 아니라 WORK-006 검수 때부터 정적 검사 ⑨ 가 못 보던 자리다(§1-4-b).

## 1. 코디 지정 축

### 1-1. 완료 게이트 우회 — 4항목 grep 판정 (WORK-005 L137 · L147 · L294)

내가 직접 돌린 grep(`app/back` 기준):

| # | 검사 | 결과 | 근거 |
|---|---|---|---|
| ① | `task.status` 에 값을 대입하는 코드가 `change_status()` 밖에 있나 | **0건.** `\.status\s*=[^=]` 는 `repository/task_repository.py:313 row.status = status`(`update_status`) 하나. `update_status(` 호출은 `service/task_service.py:748`(`change_status`) · `:825`(`undo_last_status`) 둘뿐 | `meeting_*` 에서 status 대입은 전부 `meeting.status`·`BatchRunStatus`·`JobStatus` — 업무가 아니다 |
| ② | `meeting_*` 서비스가 `TaskCompletionBlockedError` 를 잡아 다르게 처리하나 | **0건.** 식별자가 나오는 곳은 `meeting_task_link_service.py:8` **docstring 표의 「하지 않는 것」 칸**뿐. `edit`·`task_link` 두 서비스에 `try:`/`except` 자체가 없다 | `test_meeting_task_link.py:395-406` 이 같은 검사를 코드로 고정 |
| ③ | 전이 그래프 · 완료 조건 판정이 `meeting_*` 에 있나 | **0건.** `_TRANSITIONS`·`can_transition`·`completion`·`deliverable`·`TaskStatus.DONE` 전부 `service/meeting_*.py` 에 없다. `task_service` 를 부르는 회의 서비스는 `meeting_task_link_service.py` 하나이고 부르는 함수는 `create_task`·`change_status`·`update_task`·`add_memo` 넷 | `test_meeting_task_link.py:409-423` |
| ④ | `task_service.py` 가 변경됐나 | **변경 0.** `git diff ac9ee5b...HEAD --stat` 에 `service/task_service.py`·`repository/task_repository.py` 없음 | — |

**게이트가 거부했을 때 아무것도 안 바뀌는지** — `test_meeting_task_link.py:118-137` 가 `task.status · due_date · completed_at · 메모 수 · 로그 수 · 전이 수`(`_task_state` L66-77) 와 `pending_change`(L134) 를 **dict 통째로 전후 비교**한다. 뒤 단계(기한)가 거부됐을 때 앞 단계(전이)가 되돌아가는 것은 `:201-221` 이 savepoint 로 service 층에서 실측한다.
**같은 상태로 보낼 때 409** — 서버 `meeting_task_link_service.py:142` 가 `change["status"] != task.status` 일 때만 `change_status()` 를 부른다(`test_the_same_status_is_skipped_without_409` L158-182). 화면은 툴팁에서 같은 상태를 뺀다(`useMeetingTaskLink.tsx:56`) · U-9 드로어는 같은 상태를 요청에 싣지 않는다(`LinkTaskDrawer.tsx:145-147` · `MeetingTaskLink.test.tsx:364-365`). **SPEC-004 L478 의 409 가 사용자에게 보일 경로가 없다.**

**보태어** — `apply_pending_change` 의 순서 ① status → ② dueDate → ③ note → ④ NULL 이 SPEC-008 §4 L524-529 그대로다(`meeting_task_link_service.py:142-158`). 「업무 갱신」 한 번에 요청 하나는 `MeetingTaskLink.test.tsx:166·189·221` 이 MSW `request:start` 기록으로 단언한다(`/api/tasks` 로 새는 요청은 미등록이라 MSW 에러 — L107-112).

### 1-2. 통합 규칙 — 모델을 믿었나 (DEC-003 §4 L105 · OQ-7 L183 · SPEC-008 §4 「통합 규칙」)

| 검사 | 결과 | 근거 |
|---|---|---|
| 모델 출력에서 본문(`content`·`kind`·`detail`)을 읽는 코드 | **0건.** `meeting_merge_service.py:84-95` `_parse` 가 읽는 키는 `headline`·`agendas`·`agendaRef`·`humanAgendaId`·`aiAgendaId`·`lines`·`sourceHumanLineId`·`sourceAiLineId` 여덟뿐. 본문은 `_build_line` 이 `human_line.content`·`ai_line.content` 에서 복사(`:189-216`) | `test_meeting_finalize.py:361-372` 가 `\["(\w+)"\]` 키 집합을 그 여덟으로 고정 |
| 스키마에 본문 자리가 없나 | **없다.** `ai_schemas/meeting_integration.json` 줄 항목은 `sourceHumanLineId`·`sourceAiLineId` 둘 + `additionalProperties:false`. 모델이 `content` 를 실으면 **스키마 위반 → 시도 실패** | `test_meeting_merge.py:166-171` |
| 실패 5종이 테스트로 고정됐나 | **됐다 — 두 층에서.** 순수 함수(DB 없이): 사람 줄 누락 `:124` · 이중 계승 `:129` · AI 중복 참조 `:136` · 참조 없음 `:143` · `headline` 누락/201자/공백/줄바꿈 `:150-160`. 파이프라인(실행기째): `test_meeting_finalize.py:196-227` 파라미터 6종 × 3회 → `ended`+`failed` · `integration_failed` · `merged` 0건 · `ai_headline NULL` · 사람 줄 3 · AI 줄 3 · 트랜스크립트 잔존 | BE §12 필수 테스트 8 이 여기다 |
| 사람 문장 바이트 일치 | `test_meeting_merge.py:92` · `test_meeting_finalize.py:151` 이 `.encode()` 로 비교 | SPEC-008 §6 #4 |
| 그 밖의 구조 검증 | 안건 축(사람 안건 전수 · 중복 · 미러 안건 거부 · `agendaRef` 키 하나) `:174-200` · 사람 줄 상대 순서 `:203-213` · JSON 아님 `:216` | SPEC-008 §4 표 규칙 6·7 |

**SPEC 보다 엄격한 곳 하나** — `meeting_merge_service.py:177-179` 는 계승 줄이 **자기 사람 안건 밖**에 놓이면 실패시킨다. SPEC-008 §4 표에는 이 문장이 없다(「안건 축」 행은 안건 단위, 「줄 순서」 행은 상대 순서만). M-6·M-8 의 결(사람 회의록 구조를 AI 가 옮기지 않는다)에 맞으므로 지적이 아니라 **문서 공백 DG-8** 이다.

### 1-3. 삭제 경계 — ERD M-20 · DEC-003 §1 표 L44

| 규칙 | 코드 | 테스트(DB 전후) |
|---|---|---|
| `merged` 만 지운다 · `failed` 면 `human` | `meeting_edit_service.py:56-66` `editable_track` 한 함수 · `require_editable_line` `:69-78` 이 트랙 밖 줄을 422 | `test_meeting_edit.py:48-74` (`succeeded` 에서 `human`·`ai` 줄 PATCH/DELETE 422 · `failed` 에서 `human` 만 200) |
| 원본 `human`·`ai`·트랜스크립트·녹음·`task` 는 남는다 | `meeting_line_repository.delete_line` `:550-566` — `delete(MeetingLine).where(id, meeting_id)` + 같은 안건 뒤 줄 `order_index − 1` 두 문장뿐. `edit_service` 는 `task_service`·`meeting_transcript_repository`·`storage`·`integrations` 를 import 하지 않는다(`:17`) | **`test_meeting_edit.py:154-220`** — 삭제 전후 `human 3 · ai 4 · transcript 1 · recording_path · task(status, deleted_at) · task_log 1 · task_memo 1 · 원본 사람 줄 content · 원본 AI 줄 evidence` 아홉 값을 dict 로 `after == before` 단언(`:209`) · 두 번째 DELETE 404(`:193-195`) · 뒤 줄 당김(`:216`) · `mergedSummary.actionCount − 1`(`:217`) · `agendas.ai`·`agendas.human` 응답 동일(`:219-220`) |
| 실패 상태에서 원본 줄을 지워도 AI 탭 그대로 | 같은 함수 | `:223-232` |
| 안건 삭제·추가·상태 변경은 종료 후 없다 · 줄 순서 변경 없다 | `update_agenda` `ended` 갈래 `:212-241` — `state` 동봉 422 · `assert_allowed("agenda_title")` · `meeting_service._ALLOWED` `agenda_create`·`agenda_delete` 에 `ended` 없음 → 409. `update_line` 은 `content`·`kind` 만 받는다(`schemas/meeting.py LineUpdate` — `orderIndex` 보내면 422 `test_meeting_edit.py:145`) | `:298-321` (`{title}` 200 · `{title,state}` 422 · `POST`/`DELETE …/agendas` 409) |
| 정적 검사 | `test_meeting_edit.py:353-368` — `editable_track` 정의 1 · 판정 패턴이 서비스·라우터에 그 파일뿐 · 삭제 경로 금지어 7종 0 | WP Phase 2 L231 |

**주의(문서 쪽)** — 코드는 뒤 줄 `order_index` 를 **당긴다**(SPEC-008 §4 L509 · U-7 L233 · WP L170 이 그렇게 정했다). 그런데 **ERD M-20 은 「지운 뒤 빈 자리는 그대로 두고 화면이 순서대로 그린다」**(`meeting.md:101`)고 적어 **서로 모순**이다. 코드 FAIL 이 아니라 **DG-1** 이다.

### 1-4. 공용 부품 — 세 work 가 공유하는 축

| 부품 | 판정 | 근거 |
|---|---|---|
| `AgendaLineTree` 안에 track 비교 0 | **PASS** | 파일에 `track`·`"human"`·`"ai"`·`"merged"` 리터럴 없음(직접 읽음 · `static.test.ts` ⑫ L189-198 · ⑮ L272-275 재실행). 008 은 `agendas={notesAgendas}`/`{editAgendas}`/`{meeting.agendas.ai}` 로 부를 뿐(`MeetingDetailBody.tsx:297·320` · `<AgendaLineTree … track=` 0건 ⑮ L267-270). 트랙 판정은 `closeState.ts` 의 `notesTrackOf`·`editTrackOf` 한 곳. 편집 prop 은 전부 선택이고 기본값 없음 → 회의 중 렌더 불변(`AgendaLineTree.tsx:63-81` · `LineRow.tsx:45-52`) |
| `MeetingStatusBar` 한 파일 | **PASS** | `generating`·`failed`·`headline(layout=stacked)` 변형이 **같은 파일**에 들어갔다(`MeetingStatusBar.tsx:34-69·204-250`). `HeadlineBar`·`GeneratingBar`·`IntegrationFailedBanner` 파일 없음(⑥ L88-95 · ⑯ L278-291). WP L125 가 그 세 파일을 「신규」로 적은 것은 WP 가 낡은 것 — DG-6 |
| `MeetingDetailBody` 하나 | **PASS** | 껍데기 둘(`MeetingClosedPage.tsx:62` · `MeetingDetailDrawer.tsx:205`)이 같은 export 를 `mode` 만 다르게 부른다 — ⑰ L293-303 · `MeetingDetailDrawer.test.tsx:91-105` 가 스파이로 단언. 드로어에서 빠진 것 넷(편집 · 줄 버튼 · 스크립트 · 첨부 쓰기)이 `isPage` 분기로만 갈린다(`MeetingDetailBody.tsx:107·255·429·459`) |
| `TranscriptPanel` · `PromptBar` · `DrawerFrame` · `ConfirmModal` · `Selector` · `TypeBadge` | **PASS** | `TranscriptPanel` 은 `footer` prop 확장(`:60`) · 삭제 모달은 `overlay.openConfirm`(`LineDeleteModal.tsx:32`) 하나 · 드로어 3종 전부 `DrawerFooter` + `openDrawer`(폭 리터럴 0 ⑦) · 유형/프로젝트는 공용 `Selector`(`CreateTaskFromLineDrawer.tsx:211·216` · `LinkTaskDrawer.tsx:195`) · 업무 줄 배지 `TypeBadge`(`LineRow.tsx:98`) · `lib/` 훅 `useRowFailures`·`useWorkSettings`·`useNow` 재사용 |
| features 사이 import 0 | **FAIL — F-1** | §1-4-b |
| `build_detail` 1개 · `_assert_allowed` 1곳 · `task_service` 미변경 | **PASS** | `test_meeting.py` 정적(빌더 1곳) · `meeting_service.py:130-137` `_assert_allowed` 하나 + `_REQUIRED_INTEGRATION_STATE` 축(`integrate` 는 `ended` AND `failed`) · `assert_allowed = _assert_allowed` 공개 이름을 `finalize`·`edit`·`task_link` 가 쓴다 · `task_service.py` diff 0 |

### 1-4-b. 정적 검사 완화 판정 — FE §2 규칙 4 L163

**사실 관계부터 바로잡는다.** 정적 검사 ⑨(`static.test.ts:134-152`)의 정규식 `/@\/features\/([a-z-]+)\//g` 는 **끝에 `/` 가 붙은 경로만** 잡는다. 이 정규식은 `ac9ee5b`(WORK-007 검수 뒤)에 **이미 그대로** 있었고 이번 diff 에서 ⑨ 블록은 **한 글자도 안 바뀌었다**(`git show ac9ee5b:…static.test.ts` 와 diff 동일). 즉 「배럴 import 허용」은 워커가 완화한 것이 아니라 **W-1 을 닫을 때부터 있던 구멍**이고, Phase 5 가 처음으로 그 구멍(`@/features/tasks` — 뒤에 `/` 없음)을 지났다. 워커는 ⑳(`:362-404`)에 **허용 5개 이름을 명시**하고 보고에 「명문화 여부」를 물었다 — 숨기지 않았다.

지금 실제 import 2건:

```
features/meetings/components/LinkTaskDrawer.tsx:32   canTransition · fetchRelationCandidates · type TaskRelation   ← @/features/tasks
features/meetings/hooks/useMeetingTaskLink.tsx:33   openTaskDetailDrawer · useTaskDoneToast                     ← @/features/tasks
```

| 질문 | 판정 | 근거 |
|---|---|---|
| ① `openTaskDetailDrawer` 는 예외에 해당하나 | **해당한다.** 회의록이 업무 상세 드로어를 여는 것(SPEC-004 U-6 「결과 입력」 → 업무 상세)이 규칙 4 의 「단 하나의 예외」 그 자체다 | FE §2 규칙 4 L163 · DEC-005 §2. 다만 예외 문면은 `features/<소유영역>/components/` 직접 import 를 말하는데 코드는 배럴 `@/features/tasks` 로 가져온다 — 문면 정정 대상(DG-4) |
| ② `canTransition` · `fetchRelationCandidates` · `useTaskDoneToast` (+`TaskRelation`) | **예외가 아니다 — 올려야 한다.** 전이 표 · 후보 검색 API · 완료 토스트 훅 · 타입은 드로어가 아니다. 규칙 4 문면은 「공유가 필요하면 `components/shared/` 나 `lib/` 로 올린다」이고, **WORK-006 W-1 → G-5 에서 코디가 같은 유형(설정의 유형·프로젝트 훅 · `useRowFailures`)을 `lib/api/workSettings.ts`·`lib/hooks/useWorkSettings.ts`·`lib/api/errors.ts` 로 올려 닫았다**(WORK-007 검수 §6 G-5). 같은 종류를 이번엔 그대로 두면 판정이 둘이 된다 | FE §2 규칙 4 · WORK-006 검수 §1-5 ④ · WORK-007 검수 §6 G-5 |
| ③ 정적 검사를 완화한 것 자체 | **완화한 것이 아니라 원래 구멍이었다**(위). 그러나 ⑳ 으로 「배럴 5개 허용」을 **테스트에 적어 넣은 것**은 코드를 고치는 대신 가드에 예외를 새긴 것이라 옳지 않다. 규칙 4 문면이 「제공 영역(DEC §8 Out)의 배럴」을 다루지 않는 것은 사실이고 그것은 G-5 가 이미 올렸던 공백이다 — **문서도 고쳐야 한다(DG-4)** | — |

**판정: FAIL F-1** (§2). 고치는 방향은 G-5 와 같다 — `fetchRelationCandidates`(+`RelationCandidate*` 타입) 를 `lib/api/tasks.ts` 로, `canTransition` 을 `lib/taskStatus.ts`(순수 표) 로, `useTaskDoneToast` 를 `lib/hooks/useTaskDoneToast.ts` 로(undo API 도 `lib/api/tasks.ts` 로 — `lib/api/workSettings.ts` 가 설정 자원 API 를 든 것과 같은 모양). 그 뒤 ⑨ 정규식을 `@\/features\/([a-z-]+)(\/|["'])` 로 고쳐 **배럴도 잡고**, 드로어 예외는 이름 목록(`openTaskDetailDrawer`·`openTaskCreateDrawer`·회의 드로어)으로 ⑨ 안에 둔다. ⑳ 의 `allowed` 5개 목록은 그때 지운다.

### 1-5. 편집 저장 경계 — DEC-003 §5 L117 · §7 L142 · SPEC-008 U-7

| 동작 | 코드 | 판정 |
|---|---|---|
| 본문 · 종류 · 안건 이름 = 포커스 해제 자동 저장 | `InlineFieldInput.tsx:97-103` blur → `commit` → `onSave` · 종류는 고르면 즉시(`LineKindSelector.tsx:69-74`) · 값이 그대로면 요청 0(`:68-71`) · 빈 값은 되돌리고 캡션(`:62-67`) · `Esc` 는 저장 안 함(`:110-116`) | **PASS** — `MeetingEditMode.test.tsx:133-161·187-202·244-268` |
| 줄 삭제 = **확인 모달 600**, 자동 저장 아님 | `renderLineAction` → `openLineDeleteModal` → `overlay.openConfirm`(`MeetingDetailBody.tsx:222-231` · `LineDeleteModal.tsx:27-40`) · 제목/요약/경고 슬롯 문구 SPEC L223-225 그대로 · `removeLine` 에 `onMutate` 없음(⑲ L333-342) · 실패면 모달 닫히고 줄 그대로 + 「삭제하지 못했습니다」(`useMeetingEdit.tsx:254-268`) | **PASS** — `MeetingEditMode.test.tsx:272-325` |
| 「되돌리기」 없음 | 헤더는 「변경은 자동 저장됩니다 · 편집 완료」뿐(`MeetingDetailBody.tsx:349-371`) · ⑱ 이 문구 0건 고정 | **PASS** — `MeetingEditMode.test.tsx:84-85` |
| 낙관적 갱신 표(SPEC-008 §5 · FE §3-4) | 본문·안건 이름·종류(`task` 이탈 제외) `onMutate` 있음(`useMeetingEdit.tsx:119·131·162`) · 삭제·추가·`task` 이탈·업무 생성/갱신·메타는 없음(`:143-157·173-191` · `useMeetingTaskLink.tsx:80-94` · `MeetingMetaInline.tsx:44-64`) | **PASS** — `task` 이탈이 응답 뒤 반영되는 것은 `MeetingEditMode.test.tsx:232-241` |
| 자동 저장 실패 = SPEC-002 U-7 규격 · 재시도 없음 | `useRowFailures` 소유 · `saveFailed` prop · `AutoSaveFailureNotice` 하나 · rethrow 없음(`useMeetingEdit.tsx:200-209`) | **PASS** — `:163-185`(재요청 0 · 「다시 저장」 1회) |

### 1-6. 그리지 않았나 · 있어야 하는 것 — SPEC-008 §7 제외 목록

| 항목 | 결과 | 근거 |
|---|---|---|
| 되돌리기 · 보기 모드 프롬프트 바 · 근거 구간/「구간 추가」 · 「비워두면 …」 · 「시작 상태」 · 「연관 업무로 바꾸기」 토글+캡션 · 「미팅·회의」 고정명 · 후보 「대기·진행 중」 · 「MM.DD HH:mm 생성」 · 「다음으로」 · 문단 요약 | **전부 0건** | `static.test.ts` ⑱ L312-330 · ⑳ L398-403 이 WORK-008 파일 19개(주석 제외)에서 문구 0을 고정. 화면 테스트도 단언(`MeetingClosedPage.test.tsx:84-94·228-245` · `MeetingEditMode.test.tsx:346-348` · `MeetingTaskLink.test.tsx:244-246`) |
| **있어야 하는 것** — 편집 중 안건 제목 입력 상자(결정 ②) | 있다 | `AgendaTitleInline.tsx` → `AgendaHeader.titleControl` 슬롯(`AgendaHeader.tsx` diff) · `MeetingEditMode.test.tsx:91` 4개 |
| 안건 배지 「다음 논의로」(종료 후) · 회의 중 「대기」 유지 | 있다 · 갈렸다 | `closeState.ts:44-48` vs `agendaBadges.ts:12-16` — 같은 `state` 값에 어휘 둘(DEC-003 §1 표 L45). ⑱ L326-329 |
| 한 줄 요약 바 — `headline` null 이면 안 그림 · 한 개 | 그렇다 | `MeetingDetailBody.tsx:189-191` · `MeetingClosedPage.test.tsx:225·271-276` |
| 「다시 생성」은 `ended`+`failed` 에서만 | 그렇다 | `MeetingDetailBody.tsx:187-188` · 서버 `_REQUIRED_INTEGRATION_STATE`(`meeting_service.py:126-128`) · `test_meeting_finalize.py:321-334` · `MeetingClosedPage.test.tsx:229` |

### 1-7. 통과 판정의 정직성 — 테스트를 돌리지 않고 읽었다

워커 보고 숫자(BE 507 → 508 → 519 passed · FE 283 → 297 passed · Errors 0)는 **내가 확인하지 않았다.** 대신 아래를 읽었다.

**백엔드 — 단독 실행에만 의존하는 픽스처가 있나**

- `close_scope`(`meeting_close_fixtures.py:64-78`)는 테스트마다 네 서비스의 `session_scope` 를 테스트 세션으로 바꾸고 `job_service.launch`·`meeting_batch_service.schedule` 을 기록기로 바꾸며 `reset_state()` 를 앞뒤로 부른다. `fake_agent`·`fake_stt`·`fake_store` 는 `conftest.py:56-81` autouse. **테스트 간 공유 상태는 `meeting_finalize_service._plans`(모듈 dict) 하나**가 남는데 — `/end` 만 부르고 `run_job` 을 안 부르는 테스트가 여럿(`test_any_line_write_during_generating_is_409` 등)이라 키가 쌓인다 — job id 가 `Identity` 시퀀스라 롤백돼도 되감기지 않아 **충돌하지 않는다.** 순서 의존 없음.
- 코디가 잡았던 1건(`test_job_over_the_limit…`)은 `handler.run` 을 「DB 를 안 건드리는 무한 대기」로 바꿔 고쳤고 docstring(`test_job.py:90-95`)이 이유를 적었다. **재는 것(실행기의 상한 마감 → `failed(job_timeout)` → `on_timeout` → 회의 `ended`+`failed`)은 그대로 검증된다** — 정직한 우회다.
- **HTTP 층 롤백은 테스트가 증명하지 못한다** — `conftest.py:128-131` 의 `get_db` 대역은 `flush` + 커밋 뒤 훅만 돌리고 예외 시 `rollback` 이 없다(WORK-001 부터의 인프라). 그래서 게이트 거부 뒤 「아무것도 안 바뀜」은 `change_status` 가 첫 단계라 통과하고, 뒤 단계 거부의 롤백은 `begin_nested()` 로 service 층에서만 실측했다(`test_meeting_task_link.py:201-221`). Phase 5 워커가 보고에 **스스로 적었다**(「테스트 get_db override 가 롤백 안 해」). 프로덕션 `get_db` 가 롤백하는 것은 BE §7 규약이고 코드 결함이 아니다 — 테스트 인프라 항목으로 §1-8 에 올린다.

**프론트 — 뮤테이션 거부를 받는 자리가 없는 경로가 있나**

전부 있다. `saveLineContent`·`changeLineKind`·`renameAgendaTitle`·`deleteLineConfirmed`(`useMeetingEdit.tsx:195-268` — catch 하고 다시 던지지 않는다) · `applyPendingChange`(`useMeetingTaskLink.tsx:106-152` — 던지지 않는다) · `createTaskFromLine`·`addLineFromDrawer`(던지되 드로어 3종이 catch — `AddLineDrawer.tsx:148-160` · `LinkTaskDrawer.tsx:169-184` · `CreateTaskFromLineDrawer.tsx:142-159`) · `regenerate`·`end`(`MeetingDetailBody.tsx:143-154` · `MeetingDetailPage.tsx:77-89`) · 메타 `save`(`MeetingMetaInline.tsx:44-64`) · undo `.catch`(`useTaskDoneToast.ts:44-55`) · `onLinked → void applyPendingChange`(던지지 않는 함수) · `failure.retry` 클로저(던지지 않는 함수). `useMeetingFinalizeJob` 의 폴링은 `refetchInterval` 하나이고 `retry:false` 전역(FE §3-2).

**WP 「앱 창」·「네트워크 탭」 항목이 테스트로 옮겨졌나**

| WP 항목 | 테스트 | 단언 |
|---|---|---|
| Phase 3 L256 폴링 2초 · 종결 뒤 상세 GET 한 번 · 재요청 없음 | `MeetingClosedPage.test.tsx:96-117` | `jobReads` 간격 ≥1900ms · `detailReads === 2` · 2.6초 뒤 폴링 수 불변 |
| Phase 3 L253 폴링 실패 → 「다시 확인」 | `:120-142` | `reads === 1` 유지 → 클릭 → 2 |
| Phase 3 L249 새로고침 뒤 스피너 | `:81`(`activeJobId` 로 첫 렌더부터 폴링) | 재진입 경로 |
| Phase 4 L279 서버 내린 채 수정 · 제거 | `MeetingEditMode.test.tsx:163-185·305-325` | 재요청 0 · 줄 그대로 |
| Phase 5 L307 「업무 갱신」 요청 하나 | `MeetingTaskLink.test.tsx:166·189·221·261·307·366·412` | `request:start` 기록 전량 비교 |
| Phase 6 L324 드로어 `recording` 에 WS 0 | `MeetingDetailDrawer.test.tsx:184-193` | `FakeWebSocket.instances.length === 0` |
| Phase 1 L209 EXPLAIN 인덱스 · L190 downgrade 왕복 | **테스트 없음** — 워커가 수동 확인했다고 보고 | §1-8 |
| Phase 3 L248 ①→② 단계 순서 실측 | `MeetingClosedPage.test.tsx:96-98` | 목으로만 |

**통과로 위장한 항목 — 0건.** 세 워커 보고 모두 「실물 확인 필요」 목록이 있고(§1-8), 테스트로 옮겼다고 적은 것은 위처럼 단언이 있다.

### 1-8. 실물 확인 필요 — WORK-006 · 007 · 008 통합표

**사용자가 앱 창에서 확인할 것.** 006·007 항목은 그 검수의 번호를 그대로 쓴다. 상태는 2026-09-07 코드 기준.

| # | 출처 | 항목 | 층 | 왜 테스트로 못 닫나 | 상태 |
|---|---|---|---|---|---|
| 006-1 | 006 §1-6 | 1280~1439 반응형(사이드바 숨김 · 목록/시작 전 우 400 · 드로어 전체화면) | FE | 뷰포트 테스트 없음(FE §11) | 남음 |
| 006-2 | 〃 | 셀렉터에서 만든 프로젝트가 설정 목록에도 있다 | FE | 설정 화면 테스트 없음 | 남음 |
| 006-3 | 〃 | 업무 생성 드로어 캡처 | FE | — | 남음 |
| 006-4 | 〃 | `alembic downgrade -1 → upgrade head` 왕복(0005) | BE | 테스트 없음 | 남음 |
| 006-5 | 〃 | 삭제 후 캘린더에서 사라진다 | FE | 캘린더 미구현 | 남음 |
| 006-6 | 〃 | 칩 가로 스크롤 · 선택 행 색 · dot 광륜 등 시각 규격 | FE | 픽셀 테스트 없음 | 남음 |
| 006-7 | 〃 | 달 이동 후 새로고침에 그 달 유지 | FE | — | 남음 |
| 007-1 | 007 §1-7 | macOS Tauri `getUserMedia` 권한 → 캡처 · Windows | FE | jsdom 목 | 남음 |
| 007-2 | 〃 | `MediaRecorder` mime · 청크 ≤64KB · 250ms | FE | 목 recorder | 남음 |
| 007-3 | 〃 | 회의 중 반응형 · <1280 안내에서 스트림 유지 | FE | 뷰포트 | 남음 |
| 007-4 | 〃 | 근거 칩 → 실제 `scrollIntoView` 위치 | FE | jsdom | 남음 — 008 상세 페이지도 같은 패널 |
| 007-5 | 〃 | 재개 뒤 화자 번호 연속성 | FE+BE | 실 Soniox | 남음 |
| 007-6 | 〃 | Soniox 응답 필드 실측 | BE | 대역 | 남음 |
| 007-7 | 〃 | 오디오 포맷 `auto`/webm 수용 | FE+BE | 대역 | 남음 |
| 007-8 | 〃 | codex `--output-schema` 가 `meeting_batch.json` 을 강제하는가 | BE | 대역 gateway | 남음 — 008 이 `meeting_integration.json` 을 하나 더한다(008-1) |
| 007-9 | 〃 | 웜스타트 `result_session_id` 회수 | BE | 대역 | 남음 |
| 007-10 | 〃 | compose 에 Redis·worker 없음 | Ops | 인프라 | **닫힘** — `ac9ee5b` `docker-compose.local.yml:29-58` |
| 007-11 | 〃 | 일시정지 중 Soniox 유휴 연결 유지 시간 | BE | 실 Soniox | 남음 |
| 007-12 | 〃 | `at_ms` 기준(`_base_ms`)이 근거 칩 벽시계와 맞는가 | BE | 실 오디오 | 남음 |
| 007-13 | 〃 | NPM 리버스 프록시 WS upgrade · idle ≥300분 | Ops | 인프라 | 남음 |
| 007-14 | 〃 | 백엔드 다운 시 close 1006 → 「서버 연결이 끊겼습니다」 | FE | 대역 | 남음 |
| **008-1** | P1·2 ① · P3 | **실 codex 로 ① 마지막 배치 · ② 통합** — strict `meeting_integration.json` 수용 · 짝짓기 품질 · `headline` 언어/어조(WP Open Issues L363-364) | BE | 대역 `integration_from_prompt` 가 규칙대로만 짝짓는다 | 남음 — **가장 큰 미지수** |
| 008-2 | P1·2 ② | 실 서버 `curl /end` → 커밋 뒤 태스크 기동 → 폴링 → `ended` | BE | 테스트는 `launch` 기록기 + `run()` 직접 호출 | 남음 |
| 008-3 | P1·2 ③ · P3 ③ | 회의 중 화면에서 「회의 종료」 → 브라우저가 WS `1000 meeting_ended` 를 받고 생성중으로 | FE+BE | `FakeWebSocket` | 남음 |
| 008-4 | P1·2 ④ · P3 ④ | 300/180/900초 실시간 상한 · 프론트 480회(≈16분) | FE+BE | job 은 0.05초로 낮춰 실측 · ①② 는 대역 예외 · **480회 소진 경로는 FE 테스트 없음** | 남음 |
| 008-5 | P1·2 ⑤ | 앱 재시작 → lifespan 기동 스윕이 `running` 잔여를 마감 | BE | `ASGITransport` 는 lifespan 미실행 · 테스트는 `sweep_on_startup()` 직접 호출 | 남음 |
| 008-6 | P3 ① | AI 탭 「종결 · HH:MM」 시각이 **통합 시각**(`mergedSummary.integratedAt ?? updatedAt`) | FE | 계약에 마지막 배치 시각 필드가 없다 | **W-3 · DG-2** — 실물이 아니라 문서·코드 |
| 008-7 | P3 ② · P5 | 1280~1439: 좌 유동 + 우 400 · 한 줄 요약 말줄임 · 드로어 3종 전체화면 `←` · 시안 치수·색 | FE | 뷰포트·픽셀 테스트 없음 | 남음 — SPEC-008 §6 #25 |
| 008-8 | P3 ⑤⑧ · P5 | 일시 달력 팝오버 변경 · 드로어 헤더 유형/프로젝트 팝오버 저장 · U-9/U-10 달력·프로젝트 셀렉터 조작 | FE | 팝오버 상호작용은 일부만 테스트(제목 · 일시 겹침) | 남음 |
| 008-9 | P3 ⑥ | 「다시 생성」 → 통합본 실물 순서 | FE+BE | 목 | 남음 |
| 008-10 | P3 ⑦ · P5 | 네트워크 탭 캡처 | FE | MSW 기록으로 대체됨(§1-7) | 확인용 |
| 008-11 | P5 | 완료 토스트 → 실행취소 뒤 회의 상세 재조회(`onUndone`) | FE | 테스트는 undo 요청까지 | 남음 |
| 008-12 | P5 | 「결과 입력」 → 업무 상세 드로어 **카드 포커스**(`focusCompletion`) | FE | 테스트는 드로어 열림까지(업무 GET 500 목) | 남음 |
| 008-13 | P5 | `generating` 에서 줄 버튼(업무 생성·갱신) 비활성 렌더 | FE | `LineTaskButton locked` 경로에 화면 테스트 없음(`ClosedPage.test` 는 편집·삭제만) | 남음 — SPEC-008 §6 #2 일부 |
| 008-14 | P5 | U-9 후보 행에 **유형 배지 없음** — `GET /api/tasks/relations/candidates` 응답에 `workType` 이 없다 | FE+SPEC | SPEC-003 정합 | **DG-13** — 실물이 아니라 문서 |
| 008-15 | P1·2 | `EXPLAIN` — `merged` 조회가 `ix_meeting_line_meeting_id_track_agenda_id_order_index` 를 탄다(WP L209) · `0006_job` downgrade 왕복(WP L190) | BE | 테스트 없음 — 워커 수동 확인 보고 | 남음(재현용) |
| 008-16 | P3 범위 밖 | 공용 `InlineEditText` 의 `Esc → blur` 경합 의심(제목 인라인) | FE | 워커가 의심만 보고 | 남음 |
| 008-17 | 내 도출 | HTTP 층 롤백 — 게이트 거부 `422` 뒤 DB 가 실 `get_db` 경로로도 그대로인가(`conftest` 대역에 rollback 없음) | BE | 테스트 인프라(§1-7) | 남음 — 실 서버 curl 로 1회 |
| 008-18 | 내 도출 | 목록 미리보기 `ended` 통합본 트리 | FE | 플레이스홀더가 남아 있다 | **W-1** — 실물이 아니라 결함 |
| 008-19 | 내 도출 | 캘린더 블록 → 회의 상세 드로어(SPEC-008 §6 #22) | FE | 캘린더 미구현 · 목록 진입만 테스트 | 남음 |

### 1-9. 코디가 이미 판정한 것 — 확인만

- `POST …/lines` 응답 `LineItem`(201) — `meeting_router.py` `add_line` `response_model=LineItem` 그대로 · `ended` 갈래도 같다(`test_meeting_edit.py:257-261` 이 `item["track"]` 등 `LineItem` 필드로 단언). FAIL 아님. **SPEC-008 §4 L490·L507 은 여전히 `201 MeetingDetail`** 로 적혀 있다 — D-13 미정정, DG-5.
- `_default_session_scope` 안 `commit()` — `meeting_finalize_service.py:63-67` · `job_service.py:46-50`. 요청 경계 없는 자리의 `get_db` 대역. FAIL 아님.
- `meeting_service.start()` 의 `commit()` 1건 — `meeting_service.py:538` 그대로. BE §2 L37 ↔ §7 L175 충돌(D-3) 문서 대기.
- 웜스타트 실패 뒤 회의 상태(D-2) — `decisions-pending.md` ① 에 사용자 결정 대기. **008 이 영향을 키웠다**: `ai_session_id` 가 `NULL` 인 회의를 `/end` 하면 `_run_final_once`(`meeting_batch_service.py` diff L323-324) · `_attempt_integration`(`meeting_finalize_service.py:210-211`) 이 `RuntimeError` 를 던지고 → 설계 밖 예외라 job 은 `running` 잔류 · 회의는 `generating` 잔류 → 프론트는 480회(≈16분) 뒤 「다시 확인」만 남는다 → 앱 재시작 스윕까지 풀리지 않는다. Phase 1·2 워커가 (10)으로 보고했다. **정책 결정 뒤 SPEC-008 Case Matrix 행이 필요하다(DG-9).**

## 2. FAIL

**F-1. `features/meetings` 가 `features/tasks` 에서 드로어가 아닌 것 넷을 가져온다** — 프론트

- 자리: `features/meetings/components/LinkTaskDrawer.tsx:32`(`canTransition` · `fetchRelationCandidates` · `type TaskRelation`) · `features/meetings/hooks/useMeetingTaskLink.tsx:33`(`useTaskDoneToast`). 같은 줄의 `openTaskDetailDrawer` 는 예외 대상이라 제외.
- 어긋난 문서: **`frontend/README.md` §2 규칙 4 L163** 「영역 사이 import 금지 … 공유가 필요하면 `components/shared/` 나 `lib/` 로 올린다. 단 하나의 예외: 업무·회의 상세/생성 **드로어**」. WORK-006 검수 W-1 → WORK-007 검수 §6 G-5(코디가 같은 유형을 `lib/` 로 올려 닫음).
- 왜 FAIL 인가: 직전 라운드에 닫은 규칙이 같은 모양으로 다시 열렸다. 정적 검사 ⑨ 는 원래 배럴을 못 잡았고(§1-4-b), ⑳ 이 예외 5개를 테스트에 새겼다 — 코드 대신 가드를 연 것.
- 고치는 방향: §1-4-b 끝 문단. 코드 이동 3파일 + `features/tasks/index.ts` 재export 정리 + ⑨ 정규식/예외 목록 + ⑳ `allowed` 삭제. `useTaskStatus.ts` 는 이미 `useTaskDoneToast` 를 파일에서 import 하므로 경로만 바뀐다.
- 함께: FE §2 규칙 4 문면 정정은 **DG-4** — 코드 FAIL 과 별개로 문서에 「제공 영역의 배럴」과 「드로어 예외의 import 경로」를 적어야 다음 work 가 세 번째로 밟지 않는다.

## 3. WARN

**W-1. 목록 미리보기 `ended` 의 통합본 트리가 플레이스홀더다** — 프론트 · 소유 공백

- `features/meetings/components/MeetingPreviewPanel.tsx:152-153` — `<EmptyState message="통합본 트리는 WORK-008 에서 만든다" />`. 한 줄 요약 바(`:149-150`)와 목록 셋째 줄(`MeetingRow.tsx:24-30`)은 채워져 있어 **SPEC-008 §6 #5 는 통과**하지만, 종료된 회의를 목록에서 고르면 우측 미리보기에 저 문구가 보인다.
- 어긋난 문서: SPEC-006 §7 L728 「`ended` 통합본 … 렌더는 SPEC-008 규격을 읽기 전용으로 그대로 쓴다」 · WORK-008 L45 「WORK-006 목록 미리보기의 `ended` 렌더가 이 work 의 통합본 · 한 줄 요약을 읽는다」 · L155 Dependency 「미리보기가 `AgendaLineTree(track='merged', editable=false)` 를 읽기 전용 모드로 쓴다」.
- 왜 FAIL 이 아닌가: WORK-008 Scope L87 이 「목록 → WORK-006」으로 뺐고, WORK-006 은 SPEC-008 로 넘겼다 — **두 WP 가 서로에게 넘겨 아무도 안 만들었다.** Phase 3·4·6 워커가 「범위 밖 발견 · 5줄 교체 · 발주 필요」로 보고했다. 코디 발주 항목(DG-10). `notesAgendasOf(meeting)` + `<AgendaLineTree agendas=… expandable={notesExpandable} badgeFor={endedNotesBadge} …>` 로 `MeetingDetailBody` 와 같은 호출이면 된다.

**W-2. 501 `SurfaceNotImplementedError` 가 죽은 코드로 남았다** — 백엔드

- `core/exceptions.py:146-154`. 사용처 0(`grep -rn SurfaceNotImplementedError` — 정의뿐). Phase 5 워커가 「사용처 0(정의 유지)」로 보고.
- 어긋난 문서: WORK-008 Phase 2 L218 「Phase 5 가 채우는 순간 이 예외를 던지는 코드가 사라진다」 · BE §8-2 표에 `not_implemented` 없음(코드 자신의 docstring 도 「Case Matrix 에 없는 코드 · 임시 자리」). 지우면 된다.

**W-3. AI 탭 「종결 · HH:MM」 이 통합 시각이고, `mergedSummary` 에 계약 밖 필드가 있다** — 프론트+백엔드

- `MeetingDetailBody.tsx:83-87` — `finalBatchState === "succeeded"` 면 `mergedSummary?.integratedAt ?? meeting.updatedAt`. 코드 주석이 「마지막 배치 성공 시각은 `MeetingDetail` 에 없다 … 실물 확인 필요」라 적었다. 백엔드는 `mergedSummary` 에 `integratedAt`(통합 성공 행 `created_at`)을 더했다(`meeting_service.py` diff `_build_merged_summary` · `test_meeting_finalize.py:135-139`).
- 어긋난 문서: SPEC-008 U-3 L152 · U-2 L130 「종결 · HH:MM(**마지막 배치 성공 시각**)」 · §4 L470 「성공 시각은 그 행 `created_at`」 · §4 L432 · Data Contract L642 `mergedSummary = {agendaCount, decisionCount, actionCount}` 셋.
- 왜 WARN 인가: 문서가 화면에 요구한 값을 실을 필드를 계약에 두지 않았다 — 코드가 지어낸 것이 아니라 문서가 비었다(DG-2). 실패 상태(`mergedSummary` null)에서는 `updatedAt`(= `finish_integration` 시각)으로 떨어져 **① 성공 시각과 ② 실패 종결 시각이 같은 자리에 섞인다.** 필드를 정하면 코드 두 줄이다.

**W-4. job 의 「① 을 돌리는가」가 프로세스 메모리다** — 백엔드

- `meeting_finalize_service.py:96·114·119-120·144` — `/end` 는 `_plans[job.id]=True`, `/integrate` 는 `False`, handler 가 `pop`. `job` 행에는 없다.
- 어긋난 문서: BE §5-3 「`job` 행이 정본」. 재시작하면 스윕이 `failed(job_timeout)` 로 마감하므로(재개 없음) **관찰 가능한 오동작은 없다** — 그래서 WARN. `job.kind` 를 `meeting_finalize`/`meeting_integrate` 둘로 나누거나 컬럼 하나면 행이 정본이 된다. ERD `job.kind` CHECK 도 같이.

**W-5. `MeetingStatusPlaceholder.tsx` 가 사용처 없는 파일로 남았다** — 프론트

- WORK-006(`2d6319e`)이 만든 임시 화면. 008 이 `MeetingDetailPage` 스위치를 `MeetingClosedPage` 로 바꾸면서 import 가 사라졌다(`MeetingScheduledPage.test.tsx` diff 가 「이 화면은 WORK-008 에서 만든다」 문구 소멸을 단언). Phase 3·4·6 워커가 「죽은 파일」로 보고. 지우면 된다.

## 4. 층별 판정 요약 — PASS 근거

- **정책(DEC-003 · DEC-002)** — 종료 파이프라인 ①→② · 통합 실패 재시도 2회 · 무한 대기 금지 · 「다시 생성」 실패에서만 · 사람 줄 우선/AI 는 근거만 · `pendingChange` 3필드(`PENDING_CHANGE_STATUSES` 에 `cancelled` 없음 · `PendingChange` 스키마 `extra=forbid`) · 줄 삭제 경계 셋 · 안건은 이름만 · 줄 순서 없음 · 완료 게이트 우회 0 · 열거된 실패만(`except Exception` 0 — `test_meeting_finalize.py:391-399`) · 자동 재시도 없음(FE `retry:false` · 폴링 실패에 멈춤) ✔
- **아키텍처(BE)** — 계층(router 는 상태를 보지 않고 `meeting_edit_service`/`task_link` 가 앞문) · service 에 `fastapi`·`schemas` 없음 · repository 가 dto 만 · 요청 하나 = 트랜잭션 하나(`/lines/{id}/task` 둘이 `task_service` 를 같은 세션으로) · 백그라운드 단계마다 `session_scope` · 외부 호출 중 트랜잭션 없음(`_attempt_integration` 읽기 → 닫기 → codex → `_commit_success` 새 세션) · 원자성(`merged` INSERT + `ai_headline` + `ended/succeeded` + job 한 커밋 — `_commit_success`) · `ai_headline` 쓰는 곳 하나(`test_meeting_finalize.py:375-388`) · 상태 대입 격리(`meeting_repository` 전이 함수 셋 — `test_meeting.py` 정적) · `invalid_meeting_status` 409 하나 · 남의 것 404 · 기동 스윕 별도 태스크 · 설계 밖 예외 스택 로그 · `0006_job` 리비전 CHECK 4·인덱스 2·downgrade ✔ — W-2·W-4 참조
- **아키텍처(FE)** — `page.tsx` 무로직 · `Sheet`/`Dialog` 직접 0 · 폭 리터럴 0 · hex 0 · `new Date` 0 · `fetch` 직접 0 · 키는 `queryKeys` 하나(`job`·`meetingsListAll` 추가) · 무효화 표대로(줄/안건 → `detail`+`tasks`(+`meetings` 이름) · 업무 → `tasks`+`schedules` · job 종결 → `detail`+`list`) · 낙관적 표 · `code` 로 분기 · 드로어 동시 하나(드로어 안 모달 0 — ⑲) · 부모 모름 · WS 는 `useMeetingStream` 만(드로어 `recording` 스냅숏 WS 0) ✔ — F-1 참조
- **SPEC-008** — §4 표면 12개 전부 · Validation 표(줄 1~2000 · `detail` 4000 · `note` 1~2000 · `headline` 1~200 · `taskId`/`newTask` 정확히 하나 · `recording` 에 확장 필드 거부) · Case Matrix(`invalid_meeting_status`·`task_completion_blocked`·`invalid_status_transition`·`validation_error{field}`·`invalid_work_type`·`not_found`·`schedule_overlap`·자동 저장 실패·줄 삭제 실패·드로어 실패·조회 실패) 전부 코드+테스트 · 수치 4개 `config.py` 단일 출처 · State/Lifecycle(`ended_succeeded → generating` 전이 없음) · Acceptance 25 대조는 부록 ✔ — W-3 참조
- **WORK-008** — Phase 1~6 검증 항목 전부 테스트 또는 §1-8. 범위 밖 변경: `features/tasks`(`useTaskDoneToast` 추출 · 배럴 4개 — F-1) · `MeetingLiveView`(배지 상수 파일로 올림 — 순환 방지, 동작 동일) · `LineKindPopover`(`LINE_KINDS` 재export) · `MeetingScheduledPage.test`(플레이스홀더 단언 교체) — 전부 발주 범위 안 또는 순환 회피. `task_service.py` 0 · 문서 0 · 커밋 워커 없음(코디 커밋 3개) ✔

## 5. 문서 공백 — 이번 work 에서 드러난 것

| # | 어디 | 무엇 | 필요한 것 |
|---|---|---|---|
| **DG-1** | `database/domains/meeting.md` M-20 L101 ↔ SPEC-008 §4 L509 · U-7 L233 · S-5 L341 · WORK-008 L170 | ERD 는 「지운 뒤 빈 자리는 그대로」, SPEC·WP 는 「뒤 줄 `orderIndex` 가 당겨진다」. 코드는 당긴다(`meeting_line_repository.delete_line`) | ERD M-20 넷째 규칙을 「같은 안건의 뒤 줄 `order_index` 를 당긴다(순서 변경 표면이 없는 것과 별개)」로 |
| **DG-2** | SPEC-008 §4 L432 · L470 · Data Contract L642 · U-3 L152 · U-2 L130 | 「종결 · HH:MM」의 원천(마지막 배치 성공 시각)을 실을 필드가 없고, 코드는 `mergedSummary.integratedAt`(계약 밖)을 더해 대신 쓴다(W-3) | `MeetingDetail` 에 `finalBatchAt`(`meeting_batch_run(phase='final')` 최신 성공 행 `created_at`) 추가하거나, `integratedAt` 을 채택하고 U-3 문구를 「통합 시각」으로 |
| DG-3 | BE §6 L160 · SPEC-008 §4 L418 | `progress.phase` 를 「`meeting_batch_run` 최신 행」으로 파생하라 했으나 그 행은 시도가 **끝난 뒤** 쓰여 ② 진행 중에도 `final_batch` 로 보인다. 코드는 `job.attempt ≥ 1`(시도 시작 때 올림)로 파생 — 지연 없음(Phase 1·2 워커 (2)) | 두 문서의 파생 정의를 `job.attempt` 기준으로 |
| **DG-4** | `frontend/README.md` §2 규칙 4 L163 (G-5 세 번째) | ① 제공 영역(DEC §8 Out — 설정·업무)이 다른 영역에 내주는 훅·API·표가 어느 층에 사는지 없다 → 이번엔 `features/tasks/index.ts` 배럴(F-1) ② 드로어 예외의 import 경로가 `features/<소유>/components/` 로 적혀 있는데 실제는 배럴 ③ 정적 검사 ⑨ 가 배럴을 못 잡는 것을 문서가 모른다 | 규칙 4 에 「제공 영역의 공유 자원은 `lib/api/<자원>.ts`·`lib/hooks/`(G-5 선례) · 드로어 예외는 배럴 export 이름 목록으로 · 정적 검사는 배럴 포함」 |
| DG-5 | SPEC-008 §4 L490 · L507 (WORK-007 검수 D-13 그대로) | `POST …/lines` 응답이 `201 MeetingDetail` 로 적혀 있으나 코디 판정·코드는 `LineItem`. L507 「자식 쓰기 중 삭제만 204 이고 나머지는 MeetingDetail 전체」도 틀리다. `useMeetingEdit` 은 그래서 추가 뒤 상세를 다시 읽는다 | L490 을 `201 LineItem`(SPEC-007 정본) 으로, L507 에 「`POST lines` 는 `LineItem`」 예외 |
| DG-6 | WORK-008 L125 · Phase 3 L242-243 | `HeadlineBar.tsx`·`GeneratingBar.tsx`·`IntegrationFailedBanner.tsx` 「신규」 — SPEC-008 Placement L100 「상단 바는 한 자리」 · WORK-007 검수 ⑥ 「상단 바 파일 하나」와 충돌. 코드는 `MeetingStatusBar` 변형으로 맞게 갔다 | WP 표를 「`MeetingStatusBar` 에 `generating`·`failed`·`headline(stacked)` 변형 추가」로 |
| DG-7 | WORK-008 L103 · L191 (G-9 세 번째 재발) | `core/enums.py` — 코드는 `dto/enums.py`(`JobKind`·`JobStatus`·`JobErrorCode`·`JobPhase`·`PENDING_CHANGE_STATUSES` 전부 거기) | WP 경로 정정 · `backend/README.md` §4 트리에 `dto/enums.py` |
| DG-8 | SPEC-008 §4 통합 규칙 표 L605-615 | 「계승 줄은 자기 사람 안건 안에 있어야 한다」가 없다. 코드는 그렇게 검증한다(`meeting_merge_service.py:177-179` · `test_meeting_merge.py:203-208`) — M-6·M-8 의 결 | 표 「안건 축」 행에 한 문장 |
| **DG-9** | SPEC-008 §4 Case Matrix · DEC-003 §7 (D-2 파생) | `ai_session_id` 가 `NULL` 인 회의의 `/end`·`/integrate` — `RuntimeError` 전파 → job `running` 잔류 → 회의 `generating` 잔류 → 재시작 스윕까지 무한(프론트 16분 뒤 「다시 확인」만). 표에 행이 없다 | D-2 사용자 결정 뒤 행 하나 — 「AI 세션 없음 → ① 건너뛰고 ② 만」 또는 「`/end` 거부」 |
| **DG-10** | WORK-008 L45 · L87 · L155 ↔ WORK-006 · SPEC-006 §7 L728 | 목록 미리보기 `ended` 통합본 트리의 **소유자가 없다**(W-1). 두 WP 가 서로에게 넘겼다 | 어느 WP 의 Phase 에 넣을지 한 줄 + 발주 |
| DG-11 | `backend/README.md` §8-2 표 (G-2 잔여) | `validation_error{detail, code, field}` 행이 여전히 없다. 008 이 `field` 를 `pendingChange.status`·`pendingChange.priority`·`agendaId` 같은 중첩 키까지 넓혔다(`test_meeting_edit.py:277-292`) — 표기 규칙(점 표기)이 문서에 없다 | 행 추가 + 「중첩 키는 점 표기」 |
| DG-12 | WORK-008 Done Criteria L355 · `log.md` · `30-work/README.md` | 008 반영 0건(grep). Phase 상태 `TODO` 그대로 · §Domain/Schema 「조건부」의 확인 결과(WORK-006 리비전이 `source_*`·`ai_headline`·`source_agenda_id` 를 이미 담아 **`job` 테이블 하나만** `0006_job`) 가 WP 에 적히지 않았다 | 코디 갱신 |
| **DG-13** | SPEC-008 U-9 L261 ↔ SPEC-003 §4 `GET /api/tasks/relations/candidates` 응답 | U-9 는 후보 행에 **유형 배지**를 요구하는데 후보 응답에 `workType` 이 없다(Phase 5 워커 보고 · `MeetingTaskLink.test.tsx:57-63` 목에도 없음). 코드는 배지 없이 그린다 | SPEC-003 응답에 `workType{id,name,colorToken,isDeleted}` 추가 또는 U-9 에서 배지 삭제 — 어느 쪽이든 두 SPEC 정합 |

## 6. WORK-006 · 007 잔여 공백 — 현재 상태 (2026-09-07)

| # | 무엇 | 코드 | 문서 | 상태 |
|---|---|---|---|---|
| G-3 | 문서함 전 임시 계약(`doc` → `validation_error`) 각주 | 그대로 | SPEC-006 §4 에 각주 없음(`unsupported_file_type` 행 L539 만) | **남음** — 문서 |
| G-5 | 제공 영역 훅·API 가 사는 층 | 설정 것은 `lib/` 로 닫힘(`618d5bb`) · **업무 것은 이번에 배럴로 재발(F-1)** | FE §2 규칙 4 에 자리 명시 없음(grep 0) | **코드 재발 · 문서 남음** — DG-4 |
| G-6 | SPEC-006 U-7 목록 행 규격 ↔ `ItemRow` | 그대로 `ItemRow` | SPEC-006 L226 그대로(padding 11/12 · r10 · 타일 32) | **남음** — 문서 |
| G-9 | WP 의 `core/enums.py` 표기 | `dto/enums.py` 일관 | WORK-006 L109·L191 · WORK-007 L104·L186 · **WORK-008 L103·L191 세 번째** | **남음 · 재발** — DG-7 |
| W-1(007) | `meeting_service.start()` 안 `commit()` | `meeting_service.py:538` 그대로 | BE §2 L37 ↔ §7 L175 충돌(D-3) 그대로 | **문서 대기** — 코디 판정대로 FAIL 아님 |
| D-1 | SPEC-006 필드 소유 표 `task` 요약에 `workType` 없음 | 코드는 `workType` 을 싣는다(`test_meeting_task_link.py:322-325`) | SPEC-006 L453 여전히 `{ id, title, status, dueDate, isDeleted }` | **남음** — 문서 |
| D-2 | 웜스타트 실패 뒤 회의 상태 | `recording`+`ai_session_id NULL` 잔류 그대로 · **008 이 `/end` 경로까지 확장**(§1-9) | `decisions-pending.md` ① 사용자 결정 대기 | **대기 · 영향 확대** — DG-9 |
| D-5 | SPEC-007 검증 표에 `kind≠task` 의 `taskId` 처리 없음 | 무음 정정 그대로 | grep 0 | **남음** — 문서 |
| D-8 | compose 에 Redis·worker 없음 | `docker-compose.local.yml:29-58` 에 `redis` · worker 준비물 주석 | WORK-007 L43 전제 | **닫힘**(`ac9ee5b`) |

## 7. 가장 심각한 3건

1. **F-1 + DG-4 — 영역 사이 import 가 배럴로 다시 열렸다.** 게이트 우회는 0 이지만 「닫은 규칙이 다음 라운드에 다시 열린다」는 패턴이 두 번째다(설정 → 업무). 정적 검사 ⑨ 가 배럴을 못 본다는 것을 이번에 알았으니 코드 이동(G-5 방식)과 ⑨ 정정과 규칙 4 문면을 **한 번에** 닫아야 세 번째가 없다. 캘린더 그룹이 곧 `openMeetingDetailDrawer`·`openMeetingCreateDrawer` 를 같은 배럴 방식으로 가져간다.
2. **DG-9 (D-2 확대) — AI 세션 없는 회의는 끝낼 수 없다.** 웜스타트가 실패한 회의(D-2 · 사용자 결정 대기)를 `/end` 하면 job 이 `running` 으로 남고 회의는 `generating` 에 갇혀 재시작 스윕까지 풀리지 않는다. 코드는 「설계 밖 예외 전파」 규약대로 행동한 것이라 FAIL 이 아니지만, **사용자가 아침에 회의를 끝내다 이 자리를 만날 확률이 가장 높다**(D-8 이 닫혀 이제 회의를 시작할 수 있고, 워커가 잠깐이라도 죽어 있으면 D-2 상태가 생긴다). 정책 결정이 급하다.
3. **W-1 + DG-10 — 목록 미리보기에 「통합본 트리는 WORK-008 에서 만든다」가 보인다.** 5줄짜리 결함인데 두 WP 가 서로에게 넘겨 아무도 만들지 않았다. 사용자가 종료된 회의를 목록에서 고르는 순간 보인다 — 발주 한 줄이면 닫힌다.

## 부록 A. SPEC-008 §6 Acceptance 25 — 확인 경로

| # | 항목(요약) | 확인 경로 | 상태 |
|---|---|---|---|
| 1 | 종료 → 그 자리에서 생성중 · 문구 ①→② | `MeetingClosedPage.test.tsx:144-177 · 80-98` | 테스트 |
| 2 | 생성중 편집 없음 · 줄 버튼·삭제 비활성 · 원본 노출 | `:84-91`(편집·삭제·원본) · 줄 버튼 비활성은 `LineTaskButton locked` 경로 화면 테스트 없음 | 테스트 + **실물(008-13)** |
| 3 | 새로고침해도 스피너 이어짐 | `:81`(`activeJobId` 재진입) | 테스트 + 실물 |
| 4 | 문장 글자 그대로 · 근거 칩 · 「종결 · HH:MM」 | BE `test_meeting_finalize.py:151` · FE `:235·252-267` | 테스트 — 시각 출처 W-3 |
| 5 | 한 줄 요약 바 · 드로어 · 목록 셋째 줄 | `:224-227` · `MeetingDetailDrawer.test.tsx:110-114` · `MeetingRow.tsx:24-30` | 테스트 — 미리보기 트리는 W-1 |
| 6 | AI 에만 있던 내용 추가 · 「완료」 | BE `:157-161` · FE `:234-238` | 테스트 |
| 7 | 워커 다운 → ① 실패해도 AI 탭 유지 · 「종결 정리 실패」 | BE `:269-293` · FE `:197-200` | 테스트 + **실물(008-1)** |
| 8 | 3회 실패 → 배너 · 다시 생성 · 요약 없음 · 원본 · 편집 | BE `:196-227` · FE `:181-206` | 테스트 |
| 9 | 「다시 생성」은 실패 상태에서만 | BE `:321-334` · FE `:229` | 테스트 |
| 10 | 900초 → 실패 배너 · 무한 스피너 없음 | BE `test_job.py:87-121`(0.05초) · FE 480회 소진 경로 테스트 없음 | 테스트(축소) + **실물(008-4)** |
| 11 | 화살표 · 칩 · 「근거 구간」 · 근거 없는 줄 화살표 없음 | FE `:252-263` | 테스트 + 실물(007-4 스크롤 위치) |
| 12 | 편집 자동 저장 · 되돌리기 없음 | `MeetingEditMode.test.tsx:80-112 · 133-161` | 테스트 |
| 13 | 안건 제목 저장 · 보기 모드·드로어·미리보기 같은 이름 · 추가/삭제 없음 | `:244-268`(보기 모드) · `useMeetingEdit.tsx:166` `['meetings']` 무효화(드로어·미리보기는 단언 없음) | 테스트(일부) + 실물 |
| 14 | 제거 모달 → 삭제 → 카운트 · AI 탭 원본 그대로 | `:272-303` · BE `test_meeting_edit.py:154-232` | 테스트 |
| 15 | 업무 줄 제거 → 경고 · 업무 그대로 | `:305-325` · BE `:154-220` | 테스트 |
| 16 | 「업무」 활성 조건 · 업무 → 논의 연결 풀림 | `:204-242` · BE `:114-136` | 테스트 |
| 17 | 「+ 결정」 근거 입력 없음 · 맨 아래 | `:329-363` · BE `:257-261` | 테스트 |
| 18 | 액션 줄 업무 생성 → 프리필 · 시작 상태 없음 · 업무 줄 · 「시작전」 | `MeetingTaskLink.test.tsx:226-264` · BE `test_meeting_task_link.py:289-336` | 테스트 |
| 19 | 「+ 연관 업무」 기한만 → 갱신 완료 · 전이 없음 | FE `:313-368`(메모만) · BE `:158-182`(기한·메모 · 전이 로그 불변) | 테스트 |
| 20 | 게이트 거부 → 아무것도 안 바뀜 · 토스트 · 「결과 입력」 | BE `:118-137` · FE `:153-173` | 테스트 + 실물(008-12 포커스) |
| 21 | 이미 완료에 `done` → 409 없이 기한·메모만 | BE `:158-182` · FE `:195-222` | 테스트 |
| 22 | 캘린더 → 같은 드로어 · 버튼/편집/제거 없음 · 캡션 · ⤢ | `MeetingDetailDrawer.test.tsx:91-152`(목록 진입) | 테스트 + **실물(008-19 캘린더)** |
| 23 | 드로어 제목 저장 · 일시 겹침 원복 | `:154-171` · `MeetingClosedPage.test.tsx:278-311`(페이지 · 같은 컨트롤) | 테스트 |
| 24 | 서버 다운 시 수정 → 토스트·표시·재시도 없음 · 제거 → 그대로 | `MeetingEditMode.test.tsx:163-185 · 305-325` | 테스트 |
| 25 | 1280~1439 반응형 | 없음 | **실물(008-7)** |

## 부록 B. 이번 검수에서 확인만 하고 지적하지 않은 것

- `job_repository.find_active_job_id` docstring 「둘 이상이면 터진다」 — `session.scalar()` 는 첫 행을 돌려줄 뿐 터지지 않는다. `/end`·`/integrate` 가 상태 가드로 둘을 못 만들게 하므로 실효 없음.
- `AgendaSelect`(`AddLineDrawer.tsx:263-328`) · `StatusSelect`(`LinkTaskDrawer.tsx:340-398`)는 공용 `Selector` 대신 팝오버 목록을 새로 만들었다 — `Selector` 는 색 dot 옵션 전용이라 억지로 끼우면 더 나쁘다. 문서에 금지 근거가 없어 지적하지 않는다. 캘린더 그룹이 같은 모양을 또 만들면 그때 `components/shared/` 후보.
- `LineTaskButton` 은 `kind='task'` 인데 `taskId` 없는 줄(회의 중 사람 업무 줄)에 아무것도 그리지 않는다 — DEC-003 §1 표 「업무 줄」의 「업무 갱신」 버튼은 `pendingChange` 가 있는 줄의 것이라 맞다.
- 테스트 `test_meeting_task_link.py:216-221` 이 `ValidationError` 를 기대하는 것은 `update_task` 의 「기한이 시작일보다 앞」 규칙(SPEC-003) — 회의록 쪽 판정이 아니라 `task_service` 의 것이다. ③ 검사와 충돌하지 않는다.
