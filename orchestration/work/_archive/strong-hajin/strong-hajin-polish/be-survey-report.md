# 고도화 1차 백엔드 전수조사

- 대상: `strong-hajin-polish` 워크트리, base `origin/main`(015bed2)
- 읽기 전용 조사다. 코드 수정, 테스트 실행, 서버·DB 기동은 하지 않았다.
- 경로 약어: `B/` = `backend/src/ax_workspace/`, `F/` = `frontend/src/` (둘 다 저장소 루트 기준)
- 쿼리 수는 모두 코드를 읽고 낸 **추정**이다. 실측하지 않았다.

## 0. 한 줄 요약

- **A-01**: AX 도구가 만든 초안은 `action_items` 1행(`state=pending`)과, 같은 id를 쓰는 `decision_items` 행(`kind=f"ax.{action_type}"`)으로 저장된다. 이 초안은 홈 판단 대기 API(`GET /api/action-items`)와 대화 조회에만 나오고, 수신함·업무 목록에는 나오지 않는다. 만료 전이는 없다. 「첫 회차」는 `submission_version`, 「○○ 차례」는 `waiting_on`(= 초안 소유자 본인)으로 프론트가 만든다.
- **B-01**: 서버에는 응답 캐시, ETag, Cache-Control이 없다(0건). 모든 요청이 인증마다 약 9~11+R 쿼리를 다시 계산한다. 홈, 내 업무, 조직, 회의 목록 API에는 행마다 쿼리가 나는 N+1 자리와 전 테이블 스캔이 있다. 프론트는 탭을 옮길 때마다 화면을 언마운트·재마운트하고, 진입 호출을 캐시 없이 다시 보낸다.
- **B-02**: 서버의 참조자 후보(`member_candidates`)는 역할·소속을 보지 않고, 재직 중인 사람 가운데 본인만 뺀다. 빠지는 한 명은 **프론트**에서 걸러진다. 「새 업무 추가」 창은 보이지 않는 `assigneeId`를 담당 후보 첫 사람으로 채우고, 참조자 칩에서 그 사람을 뺀다(`F/features/work/WorkModals.tsx:4387`, `:5228`).

---

## 1. A-01 AX 제안(초안 action)이 어디에 보이나

### 1-1. 모델·테이블·상태 전이

**저장 모델**

| 테이블 | 모델 | 상태 필드 | 근거 |
|---|---|---|---|
| `action_items` | `ActionItemRecord` | `state`, `version`, `result`, `decided_at`. `(execution_id, action_type)` 유니크 | `B/platform/persistence.py:771-796` (유니크 `:775-777`) |
| `decision_items` | `DecisionItemRecord` | `kind`, `status`(기본 `open`), `resolved_at` | `B/platform/persistence.py:1168-1183` |
| `subjects` / `subject_versions` | `SubjectRecord` / `SubjectVersionRecord` | `snapshot` | `B/platform/persistence.py:1143-1165` |
| `submissions` | `SubmissionRecord` | `submission_version`, `revises_id`, `diff` | `B/platform/persistence.py:1186-1201` |
| `review_assignments` | `ReviewAssignmentRecord` | `status`(기본 `pending`), `resolution_kind`, `expires_at` | `B/platform/persistence.py:1204-1218` |
| `review_decisions` | `ReviewDecisionRecord` | `decision`, `conditions` | `B/platform/persistence.py:1221-1232` |
| `action_item_audit_events` | `ActionItemAuditEventRecord` | `event_type` | `B/platform/persistence.py:827-835` |
| `action_material_drafts` | `ActionMaterialDraftRecord` | `state`(기본 `staged`), `expires_at` | `B/platform/persistence.py:799-824` |

**채팅 카드 id와 홈 카드 id가 같은 이유**
- `DecisionItemRecord`가 `id=action.id`, `kind=f"ax.{action.action_type}"`로 생성된다(`B/platform/actions.py:362-364`).
- 채팅 카드 id: `"action_id": str(action.id)` (`B/platform/actions.py:545`)
- 홈 카드 id: `action_item_id=str(record.id)`, `kind=f"ax.{record.action_type}"` (`B/platform/action_center.py:723-724`)

**생성 (도구 → `pending`)**
1. MCP 도구 `task_create_self`(`B/entrypoints/mcp.py:1977-1999`)가 `_propose_chat_action('task.create_self', '업무 생성 확인', payload)`를 부른다(`B/entrypoints/mcp.py:734`).
   - 제안이 `None`이면 업무를 바로 만든다(`:735-737`).
   - 제안은 `AX_MCP_CAUSATION_ID`가 있는 위임 턴에서만 생긴다(`B/entrypoints/mcp.py:752-754`).
2. `WorkflowApplication.propose_action`(`B/bootstrap/application.py:4219-4237`) → `ActionApplication.propose`로 이어진다. 여기서 `ACTION_DECIDE` 역량이 필요하다(`B/modules/ax_execution/actions.py:90-102`).
3. `SqlAlchemyActionRepository.propose`(`B/platform/actions.py:222-286`)가 저장한다.
   - 폐지된 타입이면 거부한다(`:237-239`).
   - 같은 턴·같은 타입 행이 이미 있으면, 해시가 같을 때 기존 행을 돌려주고 다를 때 `TurnProposalSlotTaken`을 낸다(`:250-263`).
   - 새 행은 `state="pending"`, `version=1`이다(`:264-280`).
   - 감사 이벤트 `action.proposed`를 남긴다(`:285`).
4. `_open_canonical_submission`(`B/platform/actions.py:334-414`)이 원장 행을 쓴다.
   - `SubjectRecord(subject_type="ax_proposal")`
   - `DecisionItemRecord(status="open")` (`:362-370`)
   - `SubmissionRecord(submission_version=1, submitted_by="ax")` (`:374`)
   - `ReviewAssignmentRecord(reviewer_member_id=owner_id, status="pending")` (`:390-397`)

**수정**
- 수정만 하는 독립 명령은 없다. `confirm` 명령에 `draft`를 실어 보내면 수정과 확정이 한 번에 처리된다.
- 정규화: `AxProposalActionHandler.normalize`(`B/platform/action_center.py:571-616`). `task.create_self`는 `due_date`가 없으면 거부한다(`:596-597`).
- 비교: `decide_ax_confirmation`이 초안을 기존 스냅샷과 비교한다. 다르면 `OpenAxSubmissionRound`(다음 회차와 diff)를 돌려준다(`B/modules/actions/confirmation.py:184-246`, 회차 증가 `:239`).
- 기록: `_confirm`(`B/platform/action_center.py:858-905`)
  - 기존 배정을 `superseded`, `resolution_kind="revised"`로 바꾼다(`:860-863`).
  - 새 SubjectVersion, Submission(`revises_id`), ReviewAssignment(`pending`)를 만든다.
- 수정 폼 계약: `ActionPresenter._edit_contract`(`B/platform/actions.py:1656`). 채팅 뷰에서는 계약이 있으면 명령이 `confirm`/`reject`로 바뀐다(`B/platform/actions.py:524-528`).

**등록(확정, confirm)**
- 경로: `POST /api/action-items/{id}/commands/confirm`(`B/entrypoints/http.py:2278-2284`) → `run_action_command`(`B/bootstrap/application.py:3383`) → `ActionCenterApplication.execute`(`B/modules/actions/domain.py:160-172`) → `AxProposalActionHandler.execute`/`_confirm`(`B/platform/action_center.py:618-638`, `:797-953`)
- 버튼 라벨은 「이 내용으로 업무 생성」이다(`B/modules/actions/policy.py:21`, `:121-130`).
- `_confirm` 처리 순서
  1. `ReviewDecisionRecord(decision="confirm")`을 쓴다(`B/platform/action_center.py:908-927`).
  2. 배정을 `decided`/`confirmed`로 바꾼다(`:930-932`).
  3. `decision_item.status="resolved"`로 닫는다(`:933-934`).
  4. `execute_confirmed`를 호출한다(`:935-948`).
- `ActionApplication.execute_confirmed`(`B/modules/ax_execution/actions.py:139-160`)가 executor를 실행한 뒤 `resolve(..., "approve")`를 부른다.
  - `state="approved"`, `version+=1`, 감사 `action.approved` (`B/platform/actions.py:452-465`)
- `task.create_self` executor는 `create_task(idempotency_key=str(action.id), source_action_item_id=action.id, ...)`를 부른다. **`TaskRecord`는 이때 처음 생긴다**(`B/platform/actions.py:824-834`).
- 호환 경로: `POST /api/actions/{id}/decide`(`B/entrypoints/http.py:1238-1250`) → `decide_action`(`B/bootstrap/application.py:4243-4271`)
  - `task.create_self`/`task.assign`/`meeting.reservation.create`에 DecisionItem이 있으면 `approve`를 `confirm`으로 바꿔 위 경로로 보낸다.

**거절 (reject)**
1. `AxProposalActionHandler.execute`가 `reject`를 받는다(`B/platform/action_center.py:624-634`).
2. `validate_action_rejection`을 거치고, staged 자료 초안을 discard한다.
3. `ActionApplication.decide`(`B/modules/ax_execution/actions.py:118-137`)가 버전과 `pending` 여부를 검사하고 `resolve`를 부른다.
4. 결과
   - `state="rejected"`, 감사 `action.rejected` (`B/platform/actions.py:459-465`)
   - 원장: `ReviewDecisionRecord(decision="reject")`, 배정 `resolution_kind="rejected"`, `status="resolved"` (`B/platform/actions.py:467-517`)

**만료 — 없다**
- `action_items.state`를 쓰는 곳은 `B/platform/actions.py:459` 한 곳뿐이다(`approved`/`rejected`만 쓴다).
- 백엔드에서 `"expired"` 리터럴은 0건이다.
- `ReviewAssignmentRecord.expires_at`(`B/platform/persistence.py:1216`)을 읽거나 쓰는 코드는 0건이다.
- 만료 처리가 있는 것은 `action_material_drafts`뿐이다(`B/platform/action_materials.py:66-76`).

**상태 요약**

| 단계 | `action_items.state` | `decision_items.status` | `review_assignments.status` |
|---|---|---|---|
| 생성 | `pending` | `open` | `pending` |
| 수정+확정 | → `approved` | → `resolved` | 기존 `superseded` + 새 행 → `decided`(`confirmed`) |
| 확정 | `approved` | `resolved` | `decided`(`confirmed`) |
| 거절 | `rejected` | `resolved` | `decided`(`rejected`) |
| 만료 | (없음) | (없음) | (없음) |

### 1-2. `ax.*` kind 전부

- kind는 하드코딩하지 않고 `f"ax.{action_type}"`로 만든다(`B/platform/actions.py:364`, `B/platform/action_center.py:724`). 백엔드에서 `"ax.` 리터럴은 5건이다(`B/platform/actions.py:364`, `:1001`, `B/platform/action_center.py:553`, `:724`, `B/entrypoints/mcp.py:459`).
- 아래 표는 `_propose_chat_action(` 호출(69건)과 MCP 도구 등록을 대조해 뽑았다.
- 활성 kind 60개, 도구 64개다. 도구 5개가 `ax.task.transition` 하나를 함께 쓴다.
- 모든 도구가 `requires_confirmation=True`로 등록돼 있다(64건, `B/modules/ax_execution/tool_catalog.py`).

| kind | MCP 도구 (`B/entrypoints/mcp.py`) | 제안 지점 (`B/entrypoints/mcp.py`) |
|---|---|---|
| ax.task.create_self | task_create_self :1977 | :734 |
| ax.task.assign | task_assign :2012 | :1147 |
| ax.task.update | task_update :2022 | :775 |
| ax.task.transition | task_start/block/resume/complete/cancel :2055-2059 | :1174 |
| ax.task.progress.batch | :1965 | :1083 |
| ax.task.checklist.add / update / archive / reorder | :1955 / :1959 / :1969 / :1973 | :1066 / :1076 / :1095 / :1105 |
| ax.task.material.attach_link / attach_reference / detach | :1825 / :1829 / :1833 | :609 / :616 / :623 |
| ax.task.reassign / reopen | :1837 / :1845 | :630 / :637 |
| ax.task.proposal.open / respond / withdraw | :1853 / :1857 / :1861 | :646 / :658 / :670 |
| ax.task.completion.submit | :1865 | :689 |
| ax.task.reference.add / release | :1869 / :1873 | :696 / :703 |
| ax.work_request.create / amend / withdraw / list_entry.remove | :1640 / :1621 / :1632 / :1636 | :385 / :343 / :362 / :369 |
| ax.work_request.comment.add | :1807 | :560 |
| ax.daily_report.edit / submit | :1571 / :1589 | :293 / :306 |
| ax.meeting.reservation.create | meeting_create :1698 | :810 |
| ax.meeting.quick_start / info.update / cancel / note.delete / start / end / finalize.retry | :1704 / :1708 / :1712 / :1716 / :1720 / :1724 / :1728 | :821 / :828 / :835 / :843 / :851 / :856 / :865 |
| ax.meeting.todo.promote / todo.remove | :1732 / :1739 | :873 / :882 |
| ax.meeting.agenda.add / update / remove | :1743 / :1747 / :1751 | :892 / :901 / :910 |
| ax.meeting.memo.write | :1755 | :920 |
| ax.meeting.material.remove | meeting_material_detach :1759 | :927 |
| ax.meeting.share_many / share.revoke | :1763 / :1767 | :937 / :946 |
| ax.action.material.link.stage / draft.discard | :1773 / :1777 | :506 / :513 |
| ax.conversation.create / message.send / turn.cancel / turn.retry | :1782 / :1786 / :1790 / :1794 | :519 / :526 / :533 / :540 |
| ax.notification.mark_read | :1799 | :547 |
| ax.assistant.character.set | :1803 | :553 |
| ax.material_folder.create / archive / detach | :1812 / :1816 / :1820 | :1217 / :1224 / :1231 |
| ax.project.create / assign_member / release_member / plan_work | :1878 / :1882 / :1886 / :1894 | :1246 / :1253 / :1260 / :1270 |
| ax.action_item.command | action_item_command :1543 | `_propose_action_item_command` :470 (`B/modules/ax_execution/actions.py:60`) |

- **제안 코드는 있지만 연결된 MCP 도구가 없는 kind**: work_request.accept / negotiate / reject, meeting.material.attach_link / detach, meeting.summary.adopt, meeting.speaker.assign, meeting.followup.task / request, task.assignment.accept / decline
  - 제안 지점: `B/entrypoints/mcp.py:392`, `:401`, `:410`, `:567`, `:574`, `:581`, `:588`, `:595`, `:602`, `:1157`
  - 이 facade 메서드들을 부르는 곳은 0건이다.
- **폐지 타입**: `meeting.create`는 제안·실행 모두 거부된다(`B/modules/actions/policy.py:30-32`).

### 1-3. action item을 내려 주는 API 전부와 필터 조건

| 화면 | 라우트 | handler → service → query | 거르는 조건 |
|---|---|---|---|
| 홈 판단 대기 (`F/features/today/TodayPage.tsx:102`) | `GET /api/action-items` (`B/entrypoints/http.py:2221-2226`) | `pending_action_items` (`B/bootstrap/application.py:3370-3373`) → `ActionCenterApplication.pending` (`B/modules/actions/domain.py:139-143`) → 핸들러 4개 (`B/platform/action_center.py:1389-1421`) | 아래 핸들러 표 |
| 받은 요청 수신함 (`F/features/work/MyWorkPage.tsx:272`) | `GET /api/work-requests/inbox` (`B/entrypoints/http.py:2070-2078`) | `work_request_inbox` (`B/bootstrap/application.py:4149-4151`) → `WorkRequestApplication.inbox` (`B/modules/work/requests.py:1210-1236`) → `list_for` (`B/platform/work_tasks.py:2178-2200`) | `WorkRequestRecord`만 읽는다. 본인이 requester/assignee/cc인 행. `category=work`는 담당자=본인이고 state ∈ {pending, negotiating}. `reference`는 cc이면서 미읽음 |
| 업무 목록 (`F/features/work/MyWorkPage.tsx:284-285`) | `GET /api/my-work` (`B/entrypoints/http.py:693-698`), `GET /api/tasks` (`:2015-2023`) | `my_work`/`readable_tasks` (`B/modules/work/application.py:997-1015`) → `tasks_for` (`B/platform/work_tasks.py:1098-1102`, `_held_by` `:1322-1327`) | `TaskRecord` JOIN `TaskAssignmentRecord(status="active")`. 기본으로 DONE/CANCELLED 제외 |
| 채팅 | `GET /api/conversations/{id}` (`B/entrypoints/http.py:1186-1195`) | `_view` (`B/modules/ax_execution/conversations.py:219-226`) → `view()` (`B/platform/conversations.py:685-692`, `:854`) | `ActionItemRecord.conversation_id == 대화 id`. state 필터 없음. `ACTION_READ` 역량이 있을 때만 포함 |
| (구) 액션 목록 | `GET /api/actions` (`B/entrypoints/http.py:1231-1236`) | `ActionApplication.list` (`B/modules/ax_execution/actions.py:104-114`) → `list_for` (`B/platform/actions.py:434-441`) | `owner_id`=본인. state 필터 없음. 프론트 정의는 `F/lib/api.ts:522-523`에 있지만 호출처가 없다 |

**홈 판단 대기의 핸들러별 조건**

| 핸들러 | kind | 조건 | 근거 |
|---|---|---|---|
| WorkRequest | `work_request.acceptance` | `status ∈ {open, awaiting_revision}`. SQL에 수신자 조건이 없고, `_build`의 envelope 판정으로 거른다 | `B/platform/action_center.py:352-367` |
| TaskAssignment | `task.assignment` | `assignee_id`=본인, `status="pending"` | `B/platform/action_center.py:988-1004` |
| TaskDelivery | `task.delivery` | `reviewer_member_id`=본인, `status="pending"` | `B/platform/action_center.py:1207-1226` |
| AxProposal | `ax.*` | `ACTION_DECIDE` 필요, `owner_id`=본인, `state=="pending"` | `B/platform/action_center.py:686-694` |

- 「AX가 준비한 변경을 확정할지 결정하세요」 문구는 `B/platform/action_center.py:732`에서 나온다.

**AX 초안이 수신함·업무 목록에 들어가나 → 들어가지 않는다**
- 수신함: `inbox()`는 `WorkRequestRecord`만 순회한다(`B/modules/work/requests.py:1225-1235`).
- 업무 목록: `TaskRecord`와 활성 배정만 조회한다(`B/platform/work_tasks.py:1322-1327`). pending 초안에는 아직 `TaskRecord`가 없다. 확정 때 처음 생기고(`B/platform/actions.py:824-834`), 그 뒤에는 일반 업무로 목록에 들어간다. 원래 초안과의 연결은 `_action_item_source`가 한다(`B/modules/work/application.py:2501-2509`).
- 프론트: `getActionItems` 호출처는 `F/features/today/TodayPage.tsx:102`와 `F/features/work/WorkModals.tsx:1111` 두 곳이다. `WorkModals`는 `kind==="task.delivery"`만 고른다(`:1116`).
- 프론트 테스트 `F/features/work/MyWorkPage.test.tsx:349-370`이 「AX 제안은 수신함·업무 표에 섞이지 않는다」를 단언한다.

### 1-4. 「첫 회차」「○○ 차례」 계산

- 렌더링은 프론트 `F/features/action/ActionCenter.tsx`에서 한다.
  - `:93`: `submission_version > 1 ? "${n}회차" : "첫 회차"`
  - `:94`: `waiting_on ? "${personName(waiting_on.display_name)} 차례" : "—"`
  - 상세 서랍의 「현재 차례」(`:494-495`)와 「회차」(`:499`)도 같은 필드를 쓴다.
  - `personName`은 괄호 부분을 잘라낸다(`F/lib/labels.ts:154-156`).
- ax.* 카드에서 두 값의 출처(백엔드)
  - `submission_version`은 현재 Submission의 버전이고, 없으면 1이다(`B/platform/action_center.py:750`). 생성 때 1이므로(`B/platform/actions.py:374`) 「첫 회차」가 뜬다. 수정+확정 때 +1이 되지만(`B/modules/actions/confirmation.py:239`), 그 시점엔 이미 resolved라 홈 목록에서 빠진다.
  - `waiting_on`은 pending일 때 `MemberDirectory.waiting_on(record.owner_id)`다(`B/platform/action_center.py:752`, 함수 `:125-131`). 즉 **초안 소유자 본인의 표시 이름**이 들어가고, 화면에는 「본인 이름 차례」가 뜬다.
- 다른 kind의 `waiting_on` 계산 지점: WorkRequest `B/platform/action_center.py:395`, TaskAssignment `:1055`, TaskDelivery `:1276`

---

## 2. B-01 탭 이동 때 화면 깜박임 (서버 쪽 몫)

### 2-0. 모든 화면에 공통

**프론트 맥락(참고)**
- 탭은 `surface === "..." && <Page/>` 조건부 렌더라서, 옮길 때마다 언마운트·재마운트된다(`F/App.tsx:476-549`).
- `request()`는 캐시 없는 `fetch`다(`F/lib/api.ts:127-144`). react-query, SWR, `staleTime`은 0건이다.
- 진입할 때마다 화면 상태가 `"loading"`으로 돌아간다(`F/features/work/MyWorkPage.tsx:354`, `F/features/calendar/CalendarPage.tsx:158`).
- AX 드로어가 열려 있으면 탭을 옮길 때마다 `/api/my-work`와 `/api/work-requests`가 추가로 나간다(`F/App.tsx:245-252`, `:264-274`).

**요청마다 붙는 인증 비용**: 약 9~11+R 쿼리, DB 세션 2개 (R = 역할 grant 수)
- 모든 라우트가 `Depends(developer_principal)` → `current_principal`을 쓴다(`B/entrypoints/http_auth.py:73-83`, `:103`).
- 세션 쿠키 조회: 1쿼리, 세션 1개(`B/platform/auth_sessions.py:28-37`)
- `authenticated_principal` → `principal_for` → `profile_for`(`B/bootstrap/application.py:2119-2121`, `B/modules/organization_access/application.py:117-121`, `B/platform/organization_access.py:43-125`)
  - member, employment, organizations, appointments, grants: 각 1쿼리
  - rules: 0~1쿼리
  - 역할 grant마다 `RoleCapabilityRecord`: R쿼리(`:110-121`)
  - role labels: 0~1쿼리(`:123`)
  - `OrganizationUnitRecord` 전체 테이블 로드: 1쿼리(`:125`)
  - `_unit_descendants()`가 조직 단위 전체를 한 번 더 스캔해 트리를 계산한다(`:513`, `:553-573`).
- principal 캐시는 없다. 서비스는 그 뒤 세 번째 세션을 연다(예: `B/bootstrap/application.py:1396`).
- 엔진은 `create_engine(database_url, pool_pre_ping=True)` 기본 풀이다(`B/platform/persistence.py:2007`).

**표 기호**: T = 업무 수, Q = 요청 행 수, M = 회의 수, P = 전체 구성원 수, A = 서로 다른 행위자 수. 모든 행에 +auth가 붙는다.

### 2-1·2-2. 화면별 진입 API · 핸들러 · 쿼리 · 무거운 자리

**홈 (TodayPage)** — 진입 시 API 4~6개

| FE 호출 | route | service | query | 추정 쿼리 |
|---|---|---|---|---|
| `getMyWork` `F/features/today/TodayPage.tsx:101` | `B/entrypoints/http.py:693` | `B/bootstrap/application.py:1394` → `B/modules/work/application.py:997,1018` | `tasks_for` `B/platform/work_tasks.py:1098`, `origin_facts` `:918` | 약 15~20 + AX 출처 업무마다 3~4 + A |
| `getActionItems` `:102` | `B/entrypoints/http.py:2221` | `B/bootstrap/application.py:3370` → `B/modules/actions/domain.py:139-143` | `B/platform/action_center.py:352-366`, `:686-694`, `:988-1003`, `:1207-1224` | 4 + 행마다 2~6 + 대기자마다 (9~11+R) |
| `getWorkRequests` `:103` | `B/entrypoints/http.py:2052` | `B/bootstrap/application.py:3217` → `B/modules/work/requests.py:1268-1287` | `list_for` `B/platform/work_tasks.py:2178-2202` | 4 + Q×(5~7) |
| `getDailyReportStatus` `:110` | `B/entrypoints/http.py:2471` | `B/modules/reports/application.py:350` | `B/platform/reports.py:589-612` | 2. 위 세 호출 뒤에 순차로 나간다 |
| `getWorkRequestCcCandidates` `:158` | `B/entrypoints/http.py:2287` | `B/modules/work/requests.py:1361` | `B/platform/organization_access.py:876-893` | 1 |
| `getWorkRequestAssigneeCandidates` `:176` | `B/entrypoints/http.py:2413` | `B/modules/work/requests.py:1357` | `B/platform/organization_access.py:851-874` | **P×(10~12+R)** |

- **`/api/action-items`**
  - WorkRequest 핸들러는 수신자 조건 없이, 시스템 전체의 열린 `work_request.acceptance`를 읽는다(`B/platform/action_center.py:353-361`).
  - 모든 행에 `_build`가 submission과 active assignment 쿼리를 먼저 낸다(`:370`, `:376`, `:432-445`). 권한 envelope가 비면 버리는 판정은 그 뒤에 한다(`:381-382`).
  - 남은 행마다 `_preview`(`:417`)와 `_suggested_changes`(`:408-413`) 쿼리가 붙는다.
  - `waiting_on`은 이름 하나를 얻으려고 `principal_for` 전체를 실행한다(`:125-131`). 그 캐시 `_cache`는 핸들러 인스턴스마다 따로라 공유되지 않는다(`:144`).
- **`/api/work-requests`**: 행마다 `_view`(`B/modules/work/requests.py:1429-1480`)가 다음 쿼리를 낸다 — N+1
  - `current_submission`: 2쿼리(`B/platform/work_tasks.py:1543-1558`)
  - `cc_member_ids`: 1쿼리(`:2286`)
  - `predecessor_task_ids`: 1쿼리(`:2219-2235`)
  - `request_references`: 1쿼리(`:2081`)
  - `_material_views`: 1~2쿼리(`B/modules/work/requests.py:1020-1036`)
- **`/api/work-request-assignee-candidates`**: 퇴직자를 포함한 `MemberRecord` 전체를 순회한다(`B/platform/organization_access.py:864`). 사람마다 `_can_answer`(`:841-849`)와 `principal_for` 전체(`:868`)를 실행한다.

**내 업무 (MyWorkPage)** — 진입 시 API 8~9개

| FE 호출 | route | service / query | 추정 쿼리 |
|---|---|---|---|
| `getMyWork` `F/features/work/MyWorkPage.tsx:284` | `B/entrypoints/http.py:693` | `B/modules/work/application.py:997` | 약 15~20 + AX 출처 업무마다 3~4 + A |
| `getTasks(true)` `:285` | `B/entrypoints/http.py:2015` | `readable_tasks` `B/modules/work/application.py:1004-1015`. 범위 확장 `:1045-1089` | my-work의 1.5~2배 + 범위 확장 쿼리 5~8 |
| `getWorkRequestInbox` `:272` | `B/entrypoints/http.py:2070` | `B/modules/work/requests.py:1210-1238` | 4 + Q×(5~7) |
| `getWorkRequests(true)` `:293` (실패 시 `:299`) | `B/entrypoints/http.py:2052` | `B/modules/work/requests.py:1268` | 4 + Q×(5~7) |
| `getSentTaskAssignments` `:306` | `B/entrypoints/http.py:2510` | `B/modules/work/assignments.py:254-256`, 행마다 `_view` `:466` | 1 + 행마다 약 8~9 |
| `getCalendar` 레일 `:943-955` | `B/entrypoints/http.py:1782` | 캘린더와 같음 | 캘린더와 같음 |
| `getWorkRequestCcCandidates` `:407` | `B/entrypoints/http.py:2287` | 홈과 같음 | 1 |
| `getWorkRequestAssigneeCandidates` `:425` | `B/entrypoints/http.py:2413` | 홈과 같음 | P×(10~12+R) |
| `getTaskAssignmentCandidates` `:443` | `B/entrypoints/http.py:1503` | `B/modules/work/assignments.py:88-101` → `B/platform/organization_access.py:931-949`, `unit_members` `:1005-1071` | 범위 인원마다 (12+R)+(10+R) |

- **`/api/my-work`**
  - 같은 업무 집합에 `origin_facts`를 3번 호출한다(`B/modules/work/application.py:1210`, `:2440`, `:2455`).
  - `_readable_request_ids`가 내 요청 전체를 다시 읽는다(`:2488-2498`).
  - AX 출처 업무마다 `_action_item_source`가 3~4쿼리를 낸다(`:2471`, `B/platform/actions.py:424-432`, `:600-610`). N+1이다.
  - `_actor`는 행위자마다 `session.get`을 한 번씩 낸다(`B/modules/work/application.py:2511-2514`).
  - 집계: `children_map`(`B/platform/work_tasks.py:633`), `approval_rounds_for` 3쿼리(`:510-558`), `pending_proposal_kinds`(`:560`)
- **`/api/tasks?include_closed=true`**: 완료·취소 업무까지 페이징 없이 싣고, 같은 파생 계산을 다시 돈다(`B/modules/work/application.py:1090-1112`).
- **inbox와 work-requests**: 같은 요청 행에 같은 행별 `_view`를 두 번 계산한다(`B/modules/work/requests.py:1232`).
- **`/api/task-assignments/sent`**: 행마다 `_view`(`B/modules/work/assignments.py:466`)를 부르고, 그 안에서 `cc_member_ids`, `active_predecessor_ids`, `_derived_for([task])`를 행마다 다시 계산한다(`B/modules/work/application.py:2805`, `:2813`, `:2821`).
- **`/api/task-assignment-candidates`**: 사람마다 `profile_for`를 두 번 계산한다(`B/platform/organization_access.py:1031-1059`, `:940-944`).

**캘린더 (CalendarPage)** — 진입 시 API 1개
- FE 호출: `getCalendar(from,to)` `F/features/calendar/CalendarPage.tsx:152`
- route `B/entrypoints/http.py:1782` → `B/bootstrap/application.py:1424-1438`
  - 업무: `calendar_tasks` `B/modules/work/application.py:951-993`
  - 회의: `calendar_rows` `B/modules/meetings/application.py:273-289` → `board` `:244-256`
- 추정 쿼리: 업무 약 6 + 회의 2 + M×(3~6) + 서로 다른 주최자 수
- 회의 행마다 `attendee_ids`를 3번 부른다(`B/modules/meetings/application.py:1648`, `:1750`, `:1752`). 공유 조회 0~2쿼리(`:1650-1654`), `line_count` 0~1쿼리(`:1680`)가 더해진다.
- 읽기 요청인데 `session.commit()`을 한다(`B/bootstrap/application.py:1437`). 자동 취소로 상태가 바뀌면 쓰기가 일어난다(`B/modules/meetings/application.py:1688-1690`).

**조직 (OrgPage)** — 진입 시 API 4~6개

| FE 호출 | route | service / query | 추정 쿼리 |
|---|---|---|---|
| `getMyOrganizationProfile` `F/features/org/OrgPage.tsx:90` | `B/entrypoints/http.py:1360` | `B/modules/organization_access/application.py:66-74` → `profile_for` | 9~10+R. 인증 때 계산한 것을 다시 계산한다 |
| `getOrganizationTree` `:90` | `B/entrypoints/http.py:1349` | `B/platform/organization_access.py:952-1003` | 5 |
| `getOrganizationUnitMembers(root)` `:127` | `B/entrypoints/http.py:1353` | `B/modules/organization_access/application.py:194-197` → `unit_members` `B/platform/organization_access.py:1005-1071` | 5 + 2 + **전체 인원×(12+R)** |
| `getOrganizationUnitMembers(selected)` `:146` | 같음 | 같음 | 5 + 2 + 하위 인원×(12+R) |
| `getInstalledAccessRoles` `:163` (관리자) | `B/entrypoints/http.py:1294` | `B/modules/organization_access/administration.py:92` | 소수 |
| `getOrganizationActivity` `:219,234` (관리자) | `B/entrypoints/http.py:1280` | `B/platform/organization_access.py:438-498` | 약 5~8 |

- 트리: 단위, 재직, 소속, 보직 테이블을 각각 통째로 읽는다(`B/platform/organization_access.py:954-985`). 단위마다 `subtree_members`를 메모 없이 재귀로 계산한다(`:975-979`, `:998`).
- 단위 구성원: 존재 확인을 위해 `organization_tree()` 전체를 먼저 실행한다(`B/modules/organization_access/application.py:195`). 그 뒤 사람마다 `profile_for`와 3쿼리를 낸다(`B/platform/organization_access.py:1031-1059`). N+1이다.
- 단위 구성원 호출은 프로필·트리 응답 뒤에 순차로 나간다(`F/features/org/OrgPage.tsx:124-158`).

**프로젝트 (ProjectPage)** — 진입 시 API 4개

| FE 호출 | route | service / query | 추정 쿼리 |
|---|---|---|---|
| `listProjects` `F/features/project/ProjectPage.tsx:107` | `B/entrypoints/http.py:1396` | `B/modules/work/projects.py:357-366` → `all_projects` `B/platform/projects.py:71-72` | 1. 전 테이블을 읽고 Python으로 거른다 |
| `getProject` `:97` | `B/entrypoints/http.py:1417` | `B/modules/work/projects.py:368-406`, `tasks_in` `B/platform/projects.py:204` | 약 9~10. 행별 N+1은 없다 |
| `getProjectParticipationHistory` `:98` | `B/entrypoints/http.py:1424` | `B/modules/work/projects.py:458-479` | 3 |
| `getMemberDirectory` `:128` | `B/entrypoints/http.py:1254` | `B/platform/organization_access.py:804-840` | 1 |

- 목록 응답 뒤에 상세와 이력이 순차로 나간다(`F/features/project/ProjectPage.tsx:107-110`).

**보고 (DailyReportPage)** — 진입 시 API 2~3개

| FE 호출 | route | service / query | 추정 쿼리 |
|---|---|---|---|
| `getTasks` `F/features/report/DailyReportPage.tsx:106` (실패 시 `getMyWork` `:107`) | `B/entrypoints/http.py:2015` | `readable_tasks` `B/modules/work/application.py:1004` | my-work 이상 + 범위 확장 |
| `getDailyReportStatus` `:139` | `B/entrypoints/http.py:2471` | `B/platform/reports.py:589-612` | 2 |
| `getDailyReportHistory` `:149` | `B/entrypoints/http.py:2523` | `B/platform/reports.py:501-530` | 약 3. status 뒤에 순차로 나간다 |

**회의 (MeetingListPage)** — 진입 시 API 1개
- FE 호출: `listMeetings` `F/features/meetings/MeetingListPage.tsx:64`
- route `B/entrypoints/http.py:700` → `B/bootstrap/application.py:1407-1422` → `board` `B/modules/meetings/application.py:225-271` → `meetings_visible_to` `B/platform/meetings.py:144-187`
- 추정 쿼리: 2 + 보이는 모든 회의×(3~6)
- 기간 제한 없이 보이는 회의를 전부 읽는다. 모든 행에 `_row`를 만든 뒤에야 Python에서 지난 회의를 20건으로 자른다(`B/modules/meetings/application.py:258-271`, `:2030-2041`, `PAST_PAGE_SIZE` `:64`).
- 읽기 요청인데 `commit`한다(`B/bootstrap/application.py:1421`).

**진입 비용 요약 (추정)**

| 화면 | 진입 API 수 | 무거운 자리 |
|---|---|---|
| 홈 | 4~6 | action-items 전역 스캔 + 행별 쿼리, assignee-candidates P×principal_for |
| 내 업무 | 8~9 | tasks 전량(닫힌 업무 포함), inbox·work-requests 행별 `_view` 이중 계산, sent 행별 `_view`, 후보 2종 N+1 |
| 캘린더 | 1 | 회의 행마다 attendee 3회 조회, 읽기 commit |
| 조직 | 4~6 | 단위 구성원 2회 × 인원별 profile_for, 트리 재귀 |
| 프로젝트 | 4 | 순차 워터폴 (행별 N+1은 없다) |
| 보고 | 2~3 | readable_tasks |
| 회의 | 1 | 기간 제한 없는 전체 회의 × 행별 3~6쿼리 |

### 2-3. 캐시 · ETag · Cache-Control

| 항목 | 결과 |
|---|---|
| `ETag` | 0건 (backend/src, frontend/src) |
| `Cache-Control` | 백엔드 0건. 정적 nginx에만 있다: `/assets/` immutable, `/` no-cache (`deploy/k8s/nginx.conf:10`, `:16`) |
| `Last-Modified` | 0건 |
| `lru_cache` | 2줄/1파일(`B/platform/korean.py:16`, `:80`). 한국어 처리용으로, API 응답과 무관하다 |
| `cache` (backend/src) | 29줄/8파일. 모두 요청 범위 dict이거나 무관한 것이다. 예: `MemberDirectory._cache`(`B/platform/action_center.py:123-131`), `_name_cache`(`B/platform/actions.py:1233`), 회의실 300초 캐시(`B/platform/the_connect.py:37`, `:85`) |
| 응답 캐시 / principal 캐시 / 조직 트리 캐시 | 없다 |
| 프론트 쿼리 캐시 | 없다. react-query, SWR, `staleTime` 0건(`F/lib/api.ts:127-144`) |

---

## 3. B-02 새 업무 추가 › 참조자 후보에 팀원 한 명이 빠짐

### 3-1. 후보 API와 거르는 조건 전부

**프론트 → API 연결**

| 칸 | 프론트 호출 | HTTP 라우트 |
|---|---|---|
| 참조자 | `getWorkRequestCcCandidates` → `/api/work-request-cc-candidates` (`F/lib/api.ts:1050-1051`) | `B/entrypoints/http.py:2287-2290` |
| 담당 후보(요청) | `getWorkRequestAssigneeCandidates` → `/api/work-request-assignee-candidates` (`F/lib/api.ts:526-527`) | `B/entrypoints/http.py:2413-2420` |
| 관리자 배정 후보 | `getTaskAssignmentCandidates` → `/api/task-assignment-candidates` (`F/lib/api.ts:1006-1007`) | `B/entrypoints/http.py:1503-1506` |
| 결재자 | 별도 API 없음. 참조자 후보와 담당 후보를 중복 없이 합친다 (`F/features/work/WorkModals.tsx:4966-4969`) | — |

**참조자 후보(서버)**: `B/entrypoints/http.py:2288` → `B/bootstrap/application.py:3308-3310` → `cc_candidates` `B/modules/work/requests.py:1361-1373` → `member_candidates` `B/platform/organization_access.py:876-893`
- 권한: `work_request.create` 또는 `task.self_manage` 중 하나(`B/modules/work/requests.py:1372`)
- `MemberRecord.employment_state == "active"` (`B/platform/organization_access.py:886`)
- `EmploymentPeriodRecord` inner join, `state == "active"`, `ended_at IS NULL` (`:884`, `:887-888`)
- 본인 제외 `MemberRecord.id != principal.id` (`:889`)
- 정렬 `MemberRecord.id` (`:891`)
- **역할, 팀, 보직, 조직 범위, 로그인 계정 조건은 없다**(`:883-892`).

**담당 후보(서버)**: `B/modules/work/requests.py:1357-1359` → `B/platform/organization_access.py:851-874`
- 권한 `work_request.create`(`B/modules/work/requests.py:1358`)
- 모든 `MemberRecord`를 id 순으로 순회한다(`B/platform/organization_access.py:864`). 그중 다음을 뺀다.
  - 본인(`:866`)
  - 로그인이 없는 사람: `_can_answer`가 `account_ref`가 비어 있는지 본다(`:866`, `:841-849`)
  - `principal_for`가 `None`인 사람(`:868-869`). 재직이 active가 아니거나 active 고용기간이 없으면 `None`이다(`:46-56`)
  - 조직 범위가 겹치지 않는 사람: `principal.organization_scope ∩ candidate.organization_scope`가 비면 제외(`:870-871`). 범위는 현재 유효한 소속 단위 id만 담고, 하위 단위로 펼치지 않는다(`:57-65`, `:548`).

**관리자 배정 후보(서버)**: `B/modules/work/assignments.py:88-101` → `B/platform/organization_access.py:931-947`
- 권한 `task.assign`(`B/modules/work/assignments.py:89`). 프로젝트 쪽 후보도 합친다(`:99-100`).
- grant가 닿는 단위와 하위 단위의 멤버가 대상이다(`B/platform/organization_access.py:937-938`, `unit_members` `:1005-1028`).
- 본인, 로그인 없는 사람, 이미 넣은 사람을 뺀다(`:940`).
- `principal_for`가 `None`이거나 `task.self_manage`가 없는 사람도 뺀다(`:943-944`).

**프론트 쪽 필터 (참고 — 빠지는 지점)**
- 「새 업무 추가」에서 한 명이 빠지는 흐름
  1. 담당자 상태값 `assigneeId`의 초기값: `initial`이 없으면 `assigneeCandidates[0]?.id`다(`F/features/work/WorkModals.tsx:4387`).
  2. 「새 업무 추가」는 `kind === "task"`다(`:4900`). 담당 후보 칸은 `kind === "request"`일 때만 그리므로(`:5174`), 이 갈래에서는 숨은 값을 바꿀 수 없다.
  3. 참조자 칩은 `.filter((candidate) => candidate.id !== assigneeId)`로, `kind`와 관계없이 담당자와 같은 사람을 뺀다(`:5228`).
  4. `task` 갈래 제출에는 `assigneeId`가 실리지 않는다(`:4730-4749`).
- 빠지는 사람은 `/api/work-request-assignee-candidates`의 첫 행이다. 정렬은 멤버 id 순이다(`B/platform/organization_access.py:864`).
- 두 목록은 페이지가 미리 읽어 두고(`F/features/work/MyWorkPage.tsx:407`, `:425`; `F/features/today/TodayPage.tsx:158`, `:176`), 창은 열 때 마운트된다(`F/features/work/MyWorkPage.tsx:1327`, `F/features/today/TodayPage.tsx:442`, `F/features/calendar/CalendarPage.tsx:645`). 그래서 창이 열릴 때 초기값이 이미 채워져 있다.
- 결과: 로그인한 사람이 `work_request.create`를 갖고 담당 후보가 1명 이상이면, 서버가 3명을 주더라도 참조자 칩은 2개만 그려진다.
- 그 밖의 프론트 필터
  - 참조자 후보가 0명이면 칸 자체를 그리지 않는다(`F/features/work/WorkModals.tsx:5223`).
  - 요청 권한이 없으면 수평 후보를 비운다(`:4463`).
  - 요청 갈래로 제출할 때 참조자에서 담당자를 한 번 더 뺀다(`:4813`).
  - 참조자 목록은 `canManageOwnTasks || canCreateWorkRequests`일 때만 읽는다(`F/features/work/MyWorkPage.tsx:400-413`, `F/features/today/TodayPage.tsx:152-164`). 실패하면 빈 목록이 된다(`F/features/work/MyWorkPage.tsx:411-412`).
  - 담당 후보 목록은 `canCreateWorkRequests`일 때만 읽는다(`F/features/work/MyWorkPage.tsx:420-431`, `F/features/today/TodayPage.tsx:170-181`).

### 3-2. 역할·소속에 따라 후보에서 빠질 수 있는 경로

| 경로 | 참조자 | 담당 후보 | 배정 후보 | 근거 |
|---|---|---|---|---|
| 프론트: 첫 담당 후보와 같은 사람 | **제외** | — | — | `F/features/work/WorkModals.tsx:4387`, `:5228` |
| 로그인 없음(`account_ref` 비어 있음) | 포함 | 제외 | 제외 | `B/platform/organization_access.py:841-849`, `:866`, `:940` |
| 직접 소속 단위가 겹치지 않음(예: 최상위 단위에만 소속 vs 팀에만 소속) | 포함 | 제외 | 해당 없음 | `B/platform/organization_access.py:57-65`, `:548`, `:870` |
| `task.assign` grant 범위 밖 | 포함 | — | 제외 | `B/platform/organization_access.py:937-944` |
| 재직 상태가 active가 아니거나 고용기간 행이 없음 | 제외 | 제외 | 제외 | `B/platform/organization_access.py:46-56`, `:884-888` |
| `task.self_manage` 없음 | 포함 | 포함 | 제외 | `B/platform/organization_access.py:943` |

- executive 역할도 `task.self_manage`와 `work_request.create`를 갖는다. `_PEOPLE_CAPABILITIES`를 포함하기 때문이다(`B/modules/organization_access/catalog.py:125`, `:156-162`).
- team-lead 역할도 두 권한을 가진다(`B/modules/organization_access/catalog.py:105-114`).
- 따라서 서버의 참조자 후보 경로에서 **역할·소속 때문에** 빠지는 조건은 없다. 재직·고용기간 조건만 있다.
- 담당 후보 경로에서는 소속 단위 교집합과 로그인 유무에 따라 빠질 수 있다. 그 결과로 「첫 담당 후보」가 누가 되는지가 달라진다.

### 3-3. 시드 적재 경로

- 진입: `B/entrypoints/dataset.py:115-123`(CSV 읽기) → `:126`, `:151`(`import_into`) → `B/bootstrap/dataset_import.py:93-110`
- 구성원 컬럼: `B/modules/datasets/schema.py:86-104`
  - `primary_unit_key`, `role_key`는 필수다(`:94-95`).
  - `employed_from`, `employed_until`은 선택이다(`:97-98`).
- 고용기간: 그 멤버에게 기존 행이 없을 때만 1행을 넣는다. CSV 재직 상태가 active가 아니면 `ended`로 들어간다(`B/bootstrap/dataset_import.py:233-241`). → 한 명만 active가 아닌 값으로 들어오면 그 사람은 참조자 후보에서도 빠진다(`B/platform/organization_access.py:884-888`).
- 소속
  - `memberships.csv`에 `primary_unit_key`와 같은 행이 없으면 그 단위를 주 소속으로 추가한다(`B/bootstrap/dataset_import.py:247-251`).
  - 종류 칸이 비면 `additional`이 된다(`:263`).
  - `valid_from`이 비면 기록 시점의 now가 들어간다(`:277`, `B/platform/persistence.py:121`).
- 보직: 역할은 보직의 `role_key`를 먼저 쓰고, 없으면 그 사람의 `role_key`를 쓴다(`B/bootstrap/dataset_import.py:313`). 모르는 역할이면 보직을 만들지 않고 건너뛴 목록에 남긴다(`:314-317`).
- grant
  - `primary_unit_key` 기준으로 그 사람의 역할 grant를 하나 준다(`B/bootstrap/dataset_import.py:345-351`).
  - 범위가 `organization`인 역할(executive)은 최상위 단위에 붙는다(`:377-378`, `:406-416`).
- 로그인
  - 비밀번호를 주지 않으면 로그인을 만들지 않아 `account_ref`가 비어 있다(`B/bootstrap/dataset_import.py:512-515`, `:517-519`). → 그 사람은 담당 후보에서 빠진다.
  - 이미 credential이 있는 멤버는 이메일만 갱신하고 `account_ref`는 건드리지 않는다(`:506-511`).
- 데모 시드 비교: `B/bootstrap/seed.py:189-288`는 모든 멤버에게 `account_ref`를 넣고(`:216`), 최상위 단위 `scax`에 소속을 하나씩 추가한다(`:229`). dataset 경로에는 이런 자동 최상위 소속이 없다.
- `B/bootstrap/scenario_csv.py:1-16`은 예제 업무만 읽고, 조직·소속은 넣지 않는다.

---

## 4. grep 개수표

범위: backend는 `backend/src`의 `*.py`, frontend는 `frontend/src`(테스트 포함, B-02 행은 테스트 제외).

| 기호 | backend | frontend |
|---|---|---|
| `"ax.` 리터럴 | 5 | – |
| `ax.task.create_self` | 0 (f-string으로만 생성) | 6 (모두 테스트) |
| `task.create_self` | 18 | – |
| `AX가 준비한` | 1 (`B/platform/action_center.py:732`) | 4 (테스트만) |
| `_propose_chat_action(` | 70줄 (정의 1 + 호출 69) | – |
| `requires_confirmation=True` (tool_catalog) | 64 | – |
| `ToolDefinition(` | 129 | – |
| `ActionItemRecord` | 70 | – |
| `waiting_on` | 12 | 10 |
| `submission_version` | 97 | 87 |
| `def pending(` | 6 | 0 |
| `pending_action_items` | 8 | 0 |
| `list_for(` | 31 | 0 |
| `"expired"` | 0 | – |
| `첫 회차` | 1 (주석) | 1 |
| `차례` | 3 (주석) | 27 |
| `ETag` | 0 | 0 |
| `Cache-Control` | 0 | 0 (nginx.conf에만 있음) |
| `Last-Modified` | 0 | 0 |
| `lru_cache` | 2 (1파일) | – |
| `cache` | 29줄 (8파일) | – |
| `staleTime` / react-query / SWR | – | 0 |
| `work-request-cc-candidates` | 1 | 2 |
| `work-request-assignee-candidates` | 1 | 1 |
| `task-assignment-candidates` | 2 | 1 |
| `member_candidates` | 12 | 0 |
| `work_request_assignee_candidates` | 21 | 0 |
| `task_assignment_candidates` | 20 | 0 |
| `cc_candidates` | 11 | 1 |
| `_can_answer` | 5 | 0 |
| `getWorkRequestCcCandidates` | 0 | 9 |
| `candidate.id !== assigneeId` | 0 | 1 |

## 5. 조사 한계

- **B-01 쿼리 수**: 모두 코드를 읽고 낸 추정이다. 서버를 띄우지 않았고, SQL 로그, 응답 시간, 행 수를 실측하지 않았다. selectin/lazy 로딩이 실제로 내는 쿼리 수는 확인하지 않았다.
- **B-01 깜박임의 원인 비중**: 서버 지연과 프론트 재마운트·로딩 상태 리셋 중 어느 쪽이 얼마나 기여하는지는 코드만으로 가를 수 없다.
- **`getInstalledAccessRoles`**: 세부 쿼리 수를 확인하지 않았다(`B/modules/organization_access/administration.py:92`).
- **B-02 운영 데이터**: 운영 시드(`~/strong-hajin-deploy-data/`)와 운영 DB는 열지 않았다. 그래서 다음은 확인하지 못했다.
  - 운영에서 빠진 사람이 실제로 「담당 후보 첫 행」인지
  - 로그인한 사람에게 `work_request.create`가 있는지
  - 네 사람의 소속 단위, `account_ref`, 고용기간 값
  - 프론트 경로(`F/features/work/WorkModals.tsx:4387`, `:5228`) 말고 재직·고용기간 경로(`B/platform/organization_access.py:884-888`)가 함께 작용했는지
- **A-01**: 프론트가 채팅 카드와 홈 카드를 어떻게 동기화·갱신하는지는 프론트 조사 범위로 두고 깊이 보지 않았다.
- **A-01 미연결 kind 12개**: 제안 코드는 있지만 도구가 없는 kind가 다른 진입점(HTTP 등)에서 쓰이는지는 `facade.X(` 호출 0건까지만 확인했다.
