# WORK-002 v2 — frontend 구현 결과 보고

- 작성: `@sc-ax-fe` (task `task_fa58f0845362` · dispatch `ctx_55f3c91df10d`)
- 워크트리: `/Users/kknaks/orca/workspaces/Strong_hajin/strong-hajin-work` · 브랜치 `kknaksss/strong-hajin-work`
- 커밋·push·PR **하지 않았다.** 워크트리에 변경만 남겼다.

## 상태: done (자동 검증 범위) / 브라우저 E2E는 사용자 몫으로 남는다

> **이 문서는 fix1(검수 정정 1차)에서 §0·§5 가 정정됐다.** 정정 내용과 그 뒤의 변경은
> `v2-frontend-fix1-report.md` 가 이어서 적는다 — F-1(자리 판정) · W-1 · W-3 · Phase 7-A 첨부.

---

## 0. 착수 점검 — W1 경계

`v2-code-baseline/manifest.json` 의 **82 파일 sha256 을 전수 대조했고 불일치 0건**이었다
(HEAD `8973791` + W1 미커밋 상태 그대로). 다른 세션이 W1 을 건드린 흔적이 없었다(BASE U-4 해당 없음).
그 위에 FE 변경만 쌓았다.

> **이 수치는 «착수 시점» 값이다 (검수 W-6).** 지금 다시 재면 FE 변경분과 **동시에 수정 중인 BE
> 파일들** 때문에 달라진다 — 그것은 어긋남이 아니라 작업이 진행된 결과다. 현재 대조가 필요하면
> 그 시점에 다시 재야 하고, **이 줄을 현재 상태로 읽지 않는다.**

## 1. 변경 파일

**새로 만든 것 (4)**

| 파일 | 무엇 |
|---|---|
| `frontend/src/features/work/workRows.ts` | 표가 읽는 «행» 과 칩이 거는 «조건» 의 순수 판정 — 완결·막는 하위·하위 셈·기한 초과·칩 건수 |
| `frontend/src/features/work/workRows.test.ts` | 위 판정의 회귀 17건 |
| `frontend/src/features/work/WorkTables.tsx` | 시안의 표 세 벌(`TaskTable`·`SentTaskTable`·`DoneTaskTable`) + 4상태 + 배지 |
| `frontend/src/features/work/TaskLifecycleV2.test.tsx` | v2 상세 흐름의 회귀 15건 (담당 변경 대기·막는 하위·재개·제안 payload) |

**고친 것 (제품 코드 8)**

| 파일 | 무엇 |
|---|---|
| `lib/viewModels.ts` | `TaskState` 넷으로 축소(`completion_submitted` 제거) · `TaskDerived`/`BlockingChild`/`TaskCancelReason` · `DirectTask.derived`·`cancel_reason`·`started_at`·`completed_at`·`reopened_at`·`child_progress{blocking,cancelled}` · `TaskChild.derived`·`cancel_reason` · `TaskAssignmentsView{task_id,current,pending,history}` · `TaskProposal`/`TaskProposalsView`/`TaskProposalMutation` · `WorkRequest` 에 `cancelled_by_agreement`·`parent_task_id`·`supersedes_request_id`·`list_entry_hidden` |
| `lib/api.ts` | 신규 8종 + 기존 2종 확장 (아래 §3) |
| `lib/labels.ts` | `derivedAssignmentLabel`·`derivedApprovalLabel`·`derivedProposalLabel`·`cancelReasonLabel`·`blockingChildReasonLabel`·`proposalKindLabel`·`proposalStateLabel`·`proposalFieldLabel` · `WorkChip`/`workChipLabel`/탭별 칩 세트 · `workTabLabel` |
| `features/work/MyWorkPage.tsx` | 3탭·칩·표 세 벌·수락/거절/철회/재요청/숨기기 배선 (전면 개편) |
| `features/work/WorkModals.tsx` | `ReasonPrompt`·`TermsChangePrompt` 신설 · `TaskDetailDrawer` v2 확장 · `CreateWorkModal` 담당자/상위/재요청/시안 격자 · `allowedTaskTransitions` 재개 게이트 |
| `features/work/WorkViews.tsx` | 칸반에서 「완료 확인 대기」 칸 제거(상태가 아니다) |
| `ds/icons/glyphs.tsx` | 글리프 **10종** 추가 (시안이 부르는 9 + `chevron-left`) |
| `shell/CalendarRail.tsx` | 주·월 뷰를 시안 모양(`CalendarNav` + 요일 스트립 + 접이식 날짜 섹션 / 7×N 그리드)으로 |

**고친 것 (테스트 11)** — `App.test.tsx` · `MyWorkPage.test.tsx` · `Subtasks.test.tsx` ·
`TaskDelivery.test.tsx` · `CreateWork.test.tsx` · `Checklist.test.tsx` · `TaskHistory.test.tsx` ·
`TaskReferences.test.tsx` · `WorkModals.test.tsx` · `MeetingDetail.test.tsx` · `MeetingAfter.test.tsx`.
**삭제·skip·단언 약화는 하지 않았다** — 뒤집힌 계약 줄은 왜 뒤집혔는지 주석과 함께 다시 썼고,
나머지는 새 api 모킹만 더했다.

**`backend/` · `docs/` · 문서 리포는 한 줄도 건드리지 않았다.**

## 2. Phase 별 — 한 것 / 안 한 것

### Phase 7-A (BE 무관, 먼저 진행)

- [x] 글리프 9종: `mail` · `message` · `chat` · `image` · `external-link` · `circle-close` ·
      `circle-check` · `chevron-left-small` · `chevron-right-small`. 전부 Lucide(ISC) 24 그리드로,
      기존 세트와 같은 출처다. **기하를 새로 그리지 않았다.** `chevron-left` 도 함께 세웠다(짝이 비어 있었다).
- [x] `.scax-select__caret` 결정: **`<Icon name="chevron-down">` 으로 통일한다.** 앱의 `Select` 가
      이미 그렇게 그리고 있고, 179종 중 유일한 차집합 클래스를 되살리면 같은 꺾쇠가 두 벌이 된다.
      **CSS 클래스를 추가하지 않았다.**
- [x] 표 세 벌의 뼈대 + 4상태(default/empty/loading/error). `TaskTable` 은 `--nostar` 5열 유지 —
      **별표 열을 되살리지 않았다**(M-21).
- [x] 업무 만들기 모달을 시안 모양으로: **2열 격자 + 가운데 세로선**(`.scax-modal-grid`) ·
      **Composer**(테두리 + 글자 수). 좁은 골격(회의 승격)은 한 열 그대로.

### Phase 7-B (탭·칩)

- [x] 탭 셋 — **내 업무 / 보낸 업무 / 완료 업무**.
- [x] 「보낸 업무」가 요청과 배정을 함께 담고 **행에서 구분**한다(`origin.kind` 배지 「요청」/「배정」).
- [x] 「받은 요청」은 **「내 업무」의 필터 칩**이다 (`derived.assignment=awaiting_acceptance`).
- [x] 「참조된 업무」·「조직 업무」를 **지우지 않았다** — 「보낸 업무」 탭의 구획으로 남겼고,
      조직 업무는 `canReadOrganizationWork` 인 사람에게만 선다 (M-20 미정의 이번 판 기본값).
- [x] 칩 라벨의 건수 = **그 칩이 거는 필터의 건수** (`chipCounts`가 같은 `matchesChip` 을 쓴다).
- [x] **「막힘」 칩은 그리지 않았다** (M-6). 막힌 업무 자체·사유·전이는 그대로 산다.
- [x] 칩 바 오른쪽 끝: **보기 방식 유지 · 「WBS 보기」 없음** (M-24 이번 판 기본값).

### Phase 7-C (v2 흐름)

- [x] 상태 매핑 — 시안 `progress`→`in_progress`, `not-started`→`open`. 「시작」은 표의 상태 Select와
      상세 상단 [시작]으로 부른다.
- [x] **상세 상단에 [시작]과 [완료]를 함께** — `open` 에서도 [완료]가 선다. **행 액션에는 [시작]만.**
- [x] 수락 대기 행과 내가 맡은 행을 `derived.assignment` 로 갈라 그린다. 받은 요청 행에 **수락/거절**.
- [x] 「보낸 업무」 상태를 **요청 상태 여섯**으로 넓혔다(`cancelled_by_agreement` 포함).
- [x] 「다시 요청」 = **재요청** (`supersedes_request_id` + 같은 `parent_task_id` 를 실은 새 요청).
- [x] 업무 상세 v2: **중심 업무 + 직속 하위 두 단계**(상위 유무로 가리지 않는다 — 옛 「부분의 부분은
      없다」 제한을 걷었다) · 하위 생성 **직접 작업 / 하위 요청** 두 갈래 · **담당 변경 대기(기존+제안 각각)** ·
      **철회 · 취소 제안 · 조건 변경 제안 · 동의/동의하지 않음 · 제안 철회 · 재개** · 완료 보고/보완 회차.
- [x] **완료 거부 시 막는 하위를 이름으로** (`blocking_children`, `why` 를 문구로 가른다).
- [x] 거절한 행은 「완료 업무」 탭의 취소로 가고 **「취소됨 — 요청 거절」**로 읽힌다(`cancel_reason`).
- [x] 「완료 업무」에서 `done`/`cancelled` 를 다르게, **승인 전 `done` 은 「확인 대기」**로.
- [x] 업무 만들기 모달의 **담당자 지정 자리** — 비었거나 본인이면 본인 업무, 다른 사람이면 요청 발송.
- [x] 「확인받을 사람」=승인자 자리는 본인·배정 업무에만 남겼다.
- [x] **시작일·참조자·참고 업무·담당자 모드를 계약에서 지우지 않았다.**
- [x] 체크리스트는 하위 Task 로 바뀌지 않는다(각각 읽힌다).
- [x] 목록 정리 = **「숨기기」 + 「숨긴 항목 보기」 토글**.

### Phase 7-D (레일)

- [x] 수신함 좌 레일: **현재의 상태 축 유지**. 종류 축(전체/업무/참고)은 만들지 않았다 — 새 계약이다.
- [x] 카드 단추: 「답장」·「원문 확인하기」 **만들지 않았다**. 아바타·미읽음·수신 시각 **그리지 않았다**(M-22).
- [x] 캘린더 우 레일은 **업무 기한만** 싣는다. 회의 일정·근무 시간 없음(M-23).
- [x] 주/월 뷰를 시안 모양으로 옮겼다.

### Phase 7-E (내비)

- [x] **현재 8항목 유지.** 시안 10항목의 「수신함·진행 현황·자료」는 만들지 않았다 — 갈 화면도 승인도 없다.
      `SideNav.tsx` 를 **건드리지 않았다.**

## 3. api.ts — BE 실물과 대조한 결과

**추정으로 확정하지 않았다.** 코디네이터가 중계한 BE 중간 shape 를 받은 뒤
`backend/src/ax_workspace/entrypoints/http.py` 의 **실제 라우트와 입력 모델을 직접 읽어** 맞췄다.

| FE 함수 | 실제 라우트 | 대조에서 고친 것 |
|---|---|---|
| `withdrawWorkRequest` | `POST /api/work-requests/{id}/withdraw` | 입력 모델이 `WorkRequestVersionRequest`(회차만) — **`reason` 을 빼고 화면의 사유 칸도 확인 모달로 바꿨다** |
| `hideWorkRequestListEntry` | `DELETE /api/work-requests/{id}/list-entry` | 본문 없음 |
| `getTaskAssignments` | `GET /api/tasks/{id}/assignments` | 응답이 `{task_id,current,pending,history}` — 타입을 봉투형으로 |
| `reopenTask` | `POST /api/tasks/{id}/reopen` | `{expected_version, reason?}` |
| `getTaskProposals` | `GET /api/tasks/{id}/proposals` | 응답이 `{task_id,pending[],history[]}` — **평평한 배열이 아니다** |
| `createTaskProposal` | `POST /api/tasks/{id}/proposals` | 필드가 `payload`(내가 처음 쓴 `terms` 아님) · 반환이 `{task_id,proposal,task_version}` 봉투 |
| `respondTaskProposal` · `withdrawTaskProposal` | `.../respond` · `.../withdraw` | 같은 봉투형 |
| `getTaskChildren` | `GET /api/tasks/{id}/children` | — |
| `createWorkRequest` | `POST /api/work-requests` | `parent_task_id`·`supersedes_request_id` 추가 |
| `getWorkRequests(includeRemoved)` | `GET /api/work-requests?include_removed=` | 숨김 영속의 짝 |

- **새 명령에 멱등 키를 싣지 않았다** (SPEC §4 Validation — 키는 발송·본인 업무 생성에만). 코디의
  확대 해석 철회를 그대로 반영했다.
- **`api.ts` 밖에서 `fetch` 하는 자리 0건** (grep 확인).

## 4. 코디네이터가 중간에 지적한 것 — 반영 여부

| 지적 | 반영 |
|---|---|
| `isChildSettled` 가 `Boolean(child.derived)` 를 요청 업무 여부로 써서, v2 에서 모든 Task 에 `derived` 가 붙으면 **본인·배정 하위가 `approval=null` 인 채 미완결로 선다** | **고쳤다.** 이제 **승인 값 자체**를 읽는다 — `awaiting_review`·`awaiting_revision` 이면 미완결, `approved`·`null` 이면 완결. 요청 축은 **서버의 `origin`/`lineage`** 로만 읽고 `derived` 의 존재로 추론하지 않는다. 회귀 6건 추가(`workRows.test.ts` 「하위 완결 판정」) — 그중 한 줄이 정확히 이 사례(**본인 업무 하위는 derived 가 붙어 있어도 승인을 요구하지 않는다**)다. 취소는 `cancelled` 로 **따로** 센다 |
| `blocking=0` 을 완료 허가로 추론 금지 (서버 게이트는 비공개 하위 포함) | **화면이 완료 단추를 `blocking` 으로 지우지 않는다.** 막는 하위 구획은 **안내이지 관문이 아니다**. 서버 409 는 그대로 오류 문구로 뜬다. 회귀: 「막는 하위가 하나도 안 보여도 완료 명령을 화면이 막지 않는다」 |
| 재개/완료 노출은 봉투(`derived.approval`)로만, `state=done` 단독 금지 | `allowedTaskTransitions` 에 `reopenBlockedByApproval()` 게이트. 승인 대기/보완 대기면 전이 0건이라 표·칸반·상세 **세 자리가 동시에** 닫힌다. 회귀 2건 |
| 조건 변경 제안이 `payload` 없이 사유만 보낸다 | **고쳤다.** `TermsChangePrompt` 를 새로 두어 **기한·요청 내용을 실제로 입력**받아 `payload` 로 싣는다. 아무것도 안 바꾸면 보낼 수 없다. 받은 제안 쪽도 `payload` 를 표로 읽는다. 회귀 2건 |
| `terms_change` payload 최종 계약 `{title?,description?,due_date?}` · `due_date` 는 ISO 또는 `null` · 빈 payload 422 · `cancellation` 은 payload 없이 `reason` 필수 | **그대로 맞췄다.** `TermsChangePrompt` 가 세 칸만 묻고 **고친 칸만** 싣는다(안 고친 칸을 되쓰면 남의 편집을 덮는다). 기한을 「지우기」로 비우면 `due_date: null` 로 간다. 하나도 안 고치면 보내는 단추가 비활성이라 **빈 payload 가 서버에 닿지 않는다.** 취소 제안은 `payload` 키 자체가 없고 사유 없이는 보낼 수 없다. 회귀 2건이 `mock.calls` 의 실제 인자를 열어 이 계약을 그대로 단언한다 |
| 숨김이 메모리에서만 동작하면 완료 처리 금지 | BE 가 `?include_removed=true` + 행별 `list_entry_hidden` 을 같은 이름으로 확정했고 **그대로 소비한다**. 목록 읽기가 `getWorkRequests(true)` 로 간다. 회귀 2건(서버 숨김 행이 기본 목록에 없고 토글로 돌아온다 / 읽을 때 `true` 로 부른다). 서버가 명령을 거절하면 **「이 화면에서만 숨겼습니다 — 새로고침하면 다시 나타납니다」**라고 말한다 |
| `WorkRequest.assignment_state` 의 뜻이 정정됨 | 「보낸 업무」 행의 «담당이 실제로 섰나» 판정을 **`assignment_state` 로** 읽는다(값이 없는 응답에서만 요청 축으로 되돌아간다) |
| FE 테스트는 `make frontend-test` 로 | 최종 검증을 그렇게 돌렸고 **실제 exit code** 를 보존했다 |

## 5. 검증 결과 (수치 · 실제 exit code)

전부 `make` 타겟으로 돌렸고 **파이프를 거치지 않은 실제 exit code** 를 적는다. 로그는 세션
scratchpad 의 `tsc.log` · `frontend-test-*.log` · `frontend-build.log` 에 남겼다. Node **v20.20.0**.

| 명령 | exit | 결과 |
|---|---|---|
| `cd frontend && npx tsc --noEmit` | **0** | 오류 0 |
| `make frontend-test` (**통과한 5·7 회차** · 아래 표) | **0** | **52 파일 · 683 테스트 전부 통과** |
| `make frontend-build` | **0** | `tsc -b` + vite build 성공 (chunk 500kB 경고는 기존과 같다) |

기준선은 코디가 잰 **645 테스트**였고 지금 **683** 이다 — **+38 은 전부 이번에 더한 회귀**이고
**깨서 지우거나 skip 한 줄은 없다.**

### 도중에 나온 실패 — 부하 탓으로 넘기지 않고 원인을 갈랐다

전량 실행을 7회 돌렸다. 2·3·4회차에서 실패가 났고, **그것을 「부하 탓」으로 적고 넘기지 않았다.**
코디가 로그에서 짚어 준 대로 **테스트가 기다린 것이 틀렸다** —
`await findByLabelText("체크리스트")` 는 **구획이 서는 것**만 기다리는데, 그 구획은 상세 읽기 **전에**
이미 「불러오는 중」으로 렌더된다. 그 다음 줄의 `getByRole("checkbox")`·`getByRole("listitem")` 은
**값이 도착하기 전에** 실행될 수 있었다. 느린 기계에서만 깨지는 종류다.

**고친 방식**: 접근 경계와 단언은 **한 글자도 바꾸지 않고**, 기다리는 대상만 「자리」에서 「값」으로
옮겼다(`getByRole` → `findByRole`, `getByText` → `findByText`). 대상 8자리 —
`Checklist.test.tsx` 5 · `TaskReferences.test.tsx` 2 · `Subtasks.test.tsx` 2.
**타임아웃을 늘리거나 단언을 약화하지 않았다.**

> **정정 (검수 W-5 · fix1 에서 원본 로그로 다시 맞췄다).** 아래 표는 **살아남은 로그가 말하는 것만**
> 적는다. 1회차 자리에 적었던 「exit 0 · 681/681」은 **그 로그가 남아 있지 않다** — 같은 파일 이름
> (`frontend-test.log`)에 나중 회차가 덮어썼고, 그 파일이 지금 담고 있는 것은 `7 failed | 676 passed (683)`
> 다. **로그 없는 통과를 검증 근거로 쓰지 않는다**: 그 행을 지우고 실제 로그 수치로 바꾼다.

| 회차 | 로그 | load avg | exit | 실패 | 판정 |
|---|---|---|---|---|---|
| — | **없음(덮어씀)** | — | — | — | 처음 한 회는 통과했으나 **로그가 남지 않았다. 근거로 쓰지 않는다.** |
| 1 | `frontend-test.log` | 높음 | 2 | `7 failed \| 676 passed (683)` | **내 탓** — 구획 대기. 고쳤다 |
| 2 | `frontend-test-2.log` | 높음 | 2 | `1 failed \| 682 passed (683)` (`TaskReferences`) | **내 탓** — 같은 원인 |
| 3 | `frontend-test-3.log` | 18.9 | 2 | `2 failed \| 681 passed (683)` (`Checklist`) | **내 탓** — 같은 원인 |
| 4 | `frontend-test-4.log` | 18.4 | 2 | `2 failed \| 681 passed (683)` | 같은 원인 + 부하 |
| **5** | `frontend-test-5.log` | **18.4** | **0** | **0 (683/683)** | 수정 뒤. **2·3·4를 깨뜨린 것과 같은 부하에서 통과** |
| 6 | `frontend-test-6.log` | **24.25** | 2 | `3 failed \| 680 passed (683)` (`MeetingList`·`OrgPage`·`App`) | **무관** — 아래 |
| **7** | `frontend-test-7.log` | **20.67** | **0** | **0 (683/683)** | — |

**「마지막 두 회차」가 아니라 「통과한 5·7 회차」다** — 그 둘 사이에 6회차가 있다(검수 W-5 ②).
1~4회차 로그는 **세션 scratchpad 에만** 있고 보존본(`v2-frontend-verification/`)에는 5·6·7 만 복사됐다.
그래서 위 표에 **수치를 본문으로 적어 두었다.**

**6회차 3건은 이 작업과 무관하다** — 근거를 적는다.

- 세 파일 모두 **내가 만들지도 고치지도 않은** 테스트다(`App.test.tsx` 의 내 diff 는 칩 라벨 3줄뿐이고
  실패한 줄은 그 함수가 아니다).
- 셋 다 **격리 실행에서 통과**한다(각각 단독 실행 exit 0).
- 실패 모양이 전부 **시간 초과**다(`Test timed out in 5000ms` · 스파이 호출 1/2).
- 그때 load average 가 **24.25** 로, 통과한 5·7회차(18.4·20.7)보다 높다. 이 기계에서 **BE 스위트가
  동시에 돌고 있었고** FE 테스트 구간이 110초 → 229초까지 벌어졌다.

**그래서 「전량 green」을 단정하지 않는다**: 통과한 5·7 회차가 같은 부하대에서 exit 0 이지만,
**더 높은 부하에서는 이 세 파일이 5초 한도에 걸린다.** 그 셋은 **이 작업 이전부터 있던 시간 민감성**이고
이번 범위에서 손대지 않았다 — 통합 검증에서 다시 뜨면 같은 성격으로 읽으면 된다.

## 6. UX-U1~U15 — 「데이터: 에이전트」 칸의 자동 검증 상태

| # | 자동으로 닫힌 것 | 어디서 |
|---|---|---|
| U-1 | `derived.assignment` 로 수락 대기 행이 갈린다 · 「시작 전」 칩에 섞이지 않는다 | `workRows.test.ts` · `MyWorkPage.test.tsx` |
| U-2 | 받은 요청 행에서 수락·거절을 부르고, 거절은 사유를 싣는다 | `MyWorkPage.test.tsx` |
| U-3 | **자리**는 섰다(표 상태 Select · 상세 [시작]). 두 시각을 각각 읽는 것은 **BE 응답 회귀** 몫 | `started_at` 은 최상위, **수락 시각은 `assignment.accepted_at`** — 최상위 `accepted_at` 은 서버가 내지 않아 타입에서 뺐다(fix1) |
| U-4 | 보낸 업무가 요청 상태 여섯을 각각 낸다(협의 중이 협의 중으로 읽힌다) | `MyWorkPage.test.tsx` |
| U-5 | 승인 전 `done` 이 「확인 대기」로, 취소가 「취소됨 — …」로 갈린다 | `MyWorkPage.test.tsx` |
| U-6 | 직속 하위 두 단계 · 상위가 있어도 자기 하위를 낸다 | `Subtasks.test.tsx` |
| U-7 | 막는 하위가 **이름과 사유**로 선다 | `TaskLifecycleV2.test.tsx` |
| U-8 | 기존 담당과 새 제안이 **각각** 읽힌다 | `TaskLifecycleV2.test.tsx` |
| U-9 | 철회·취소 제안·조건 변경·동의·제안 철회·재개·담당 변경 제안의 **자리가 전부 있다** | `TaskLifecycleV2.test.tsx` |
| U-10 | 담당자 지정이 요청 발송으로, 비우면 본인 업무로 간다 | `CreateWork.test.tsx` |
| U-11 | 「확인받을 사람」 자리 유지 (요청 Task 에서는 쓰지 않는다) | 화면 배치 |
| U-12 | 체크리스트가 하위로 바뀌지 않는다 | `Subtasks.test.tsx` |
| U-13 | 수신함이 명령을 스스로 부르지 않는다 (카드는 판단 드로어만 연다) | `InboxRail` |
| U-14 | 기한 초과가 **표시만** 바꾼다 · 끝난 업무는 지연으로 세지 않는다 | `workRows.test.ts` |
| U-15 | 목록·칩 건수가 같은 판정을 쓴다 | `workRows.test.ts` |

## 7. 미완료 · 사용자 E2E 대상 · 주의점

**브라우저 E2E 는 실행하지 않았다.** 사용자 확인 전에 「화면 경로가 검증됐다」로 쓰지 않는다. 아래는 **화면에서 눈으로 보아야** 닫히는 칸이고,
「자동 검증이 통과했으니 화면 경로가 검증됐다」로 읽지 않는다.

| 사용자 확인 | 무엇을 본다 |
|---|---|
| U-1·U-2·U-4·U-5·U-6·U-7·U-8 의 **표시** 칸 | 배지·행 액션·두 단계가 실제로 읽히는가 |
| U-3·U-9·U-10 의 **자리** 칸 | 그 단추를 사람이 찾을 수 있는가 |
| E-1~E-12 (WORK § 사용자 E2E 인계) | 흐름 전체 |
| 시안 대조 | 2열 격자·칩 바·표 세 벌·레일 두 벌의 **배치와 여백** |

**아직 열려 있는 것 — 숨기지 않고 적는다**

1. **OQ-203 (완료 보고 제출에 하위 검사)** — 답 대기. 화면은 **현행을 보존**했고 제출 단추를 하위로
   막지 않는다. **새 정책 확정으로 표시하지 않았다.**
2. **OQ-206 (`system:meeting` 승격 요청의 완료 확인자)** — 화면이 확인자를 **임의 지정하지도 자동
   승인하지도 않는다.** 그 Task 의 승인 자리는 서버 봉투가 열 때만 선다. 회의 승격 seed 를 지워
   미결을 숨기지 않았다.
3. **M-20·M-21·M-22·M-23·M-24** — WORK 가 적은 이번 판 기본값 그대로다. 새 범위를 만들지 않았다.
4. **문의·회신 대기·상태 메모 원장** — 미구현 후속이므로 이번 회귀·배포 통과 대상으로 **주장하지 않는다.**
5. **`derived` 가 없는 응답의 되돌아 읽기** — 담당 조회·제안 조회가 실패하면 그 구획을 **그리지 않고**,
   `derived` 가 통째로 없으면 재개 게이트를 걸지 않는다(회귀가 아니게). **BE 가 전 표면에서
   `derived` 를 내기 시작하면 이 되돌아 읽기는 죽은 길이 된다** — 지울지는 통합 뒤 판단할 일이다.

**DS 갭 (시안에 있으나 이번에 세우지 않은 것)**

| 갭 | 왜 |
|---|---|
| `.scax-select__caret` | `<Icon name="chevron-down">` 로 통일. 같은 꺾쇠를 두 벌로 두지 않는다 |
| 생성 모달의 **첨부 DropZone** | 업무가 생기기 전에 파일을 올리는 **계약이 없다**(자료는 상세에서 붙는다). 단추만 두면 누를 데가 없다 |
| Composer **200자 상한** | 시안의 숫자이고 **계약이 아니다.** 세고 표시하되 **막지 않는다** — 화면이 스스로 상한을 만들면 적던 글이 조용히 잘린다 |
| `star`·`star-fill`·`caret-up`/`caret-down` 글리프 | 부르는 자리가 없다(별표는 M-21, 접이식은 `chevron-*` 로 충분) |
| `mail`·`message`·`chat`·`image` 글리프 | **표에는 더했으나 이번 판에 호출부가 없다** — 수신함 카드의 출처 표시가 M-22 로 파킹돼 있다. WORK 7-A 가 9종을 명시해 그대로 더했고, 그 사실을 여기 적는다 |
| `StateSwitch` | 시안이 스스로 dev 전용이라 적었다. 제품에 넣지 않았다 |

**BE 와 함께 닫아야 남는 것**

- `?include_removed=true` + `list_entry_hidden` 은 **이름이 확정되어 FE 가 소비 중**이다.
  실제 응답으로 새로고침 뒤 복원이 서는지는 **통합 작업트리에서 함께** 봐야 한다(I-8).
- `started_at`(최상위)과 `assignment.accepted_at`(담당 관계)이 각각 오는지(U-3)는 BE 응답 회귀로 닫힌다. **최상위 `accepted_at` 을 받았다고 주장하지 않는다** — 서버가 내는 키가 아니다.
- 완료 거부 409 의 **비공개 하위 일반 문구**가 화면에 그대로 뜨는지는 통합에서 확인한다.
