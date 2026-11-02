# 고도화 조사 (backend)

- 대상: Strong_hajin `origin/main` `f0ad522` (워크트리 `strong-hajin-enhance`) · 메디니스 `origin/dev` `b840254a`
- 성격: 읽기 전용. 코드·테스트를 바꾸지 않았고 테스트·빌드·서버도 돌리지 않았다
- 경로 약어: `B/` = `backend/src/ax_workspace/` · `T/` = `backend/tests/` · `F/` = `frontend/src/` · `M/` = 메디니스 `back/app/`
- ⚠ `application.py` 가 둘이다. **`B/bootstrap/application.py`(4772줄, 조립·회의실·Action 실행)** 과 **`B/modules/meetings/application.py`(2091줄, 회의 도메인)**. 아래에서는 앞의 것을 `boot/application.py`, 뒤의 것을 `mtg/application.py` 로 적는다

---

## 0. 한 줄 요약

| 항목 | 한 줄 (원인이 보이면 원인) |
|---|---|
| SH-IMP-001·017 업무 생성 | 서버에는 **의도 분류기도 단계 상태 기계도 없다**. 프롬프트 정책을 보고 모델이 탐색 도구를 부른 뒤 `task_create_self` 를 한 번 호출하면 Action 카드 1장(`ax.task.create_self`)이 생기고, 사람이 confirm 한다. 「스텝 바이 스텝」 의 실체는 프론트 `AxDraftCard` 의 4쪽 탭이다 |
| SH-IMP-017 맥락 탐색 | 프로젝트 후보는 `list_projects`(참여 프로젝트 **전부, 상한 없음**) 또는 `graph_search`(**제목 부분 일치**, 기본 20·최대 50)로 고른다. 연관 업무는 `graph_neighbors`(멤버 edge 를 먼저 채운 뒤 20개에서 자른다) 또는 `task_list`(상한 없음, 프로젝트 필터 없음)로 찾는다. 두 경우 모두 **턴당 1회 상한은 프롬프트 지시일 뿐**이다. 서버가 미리 싣는 프로젝트·업무 목록은 없다. 중복 후보 판정은 코드에 없다 |
| SH-IMP-001 회의 생성 | `meeting_create` → `meeting.reservation.create` 카드 1장(`ActionMeetingCard`, 쪽 나눔 없음). 프로젝트·연관 업무·자료 탐색 지시가 없고, `project_id`·`reference_task_ids` 필드도 없다. `save_draft` 도 없다 |
| SH-IMP-016 AX 회의 수정 | `meeting_update` → `meeting.info.update` 카드가 **있다**(시간·참석자·장소 텍스트). `room_id` 필드는 없어서 회의실은 바꿀 수 없다 |
| SH-IMP-003 Connect | 공용 계정 1개로 `rooms`·`reservations?date`·`members` 조회와 예약 POST/PUT/DELETE 를 부른다. 생성 때는 가용 조회와 예약을 실제로 한다. **수정 때는 시간만 PUT** 한다(같은 방, 가용 조회 없음, 참석자 미반영). 성공해도 location 텍스트를 다시 쓰지 않는다 |
| SH-IMP-005 버그1 시간 | **원인: 화면**. 「불러오기」 가 `GET /api/meetings/{id}` 를 읽은 뒤 `starts_at`·`ends_at` 을 폼의 날짜·시작·종료에 넣는다(`F/features/meetings/BookingModal.tsx:206-208`) |
| SH-IMP-005 버그2 출처 | **원인: 서버가 회의 단위로 출처를 정함 + 화면이 안건별 출처를 버림**. 요청에 `carried_from_meeting_id` 가 있으면 그 요청의 안건 전부를 `"carried"` 로 저장한다(`mtg/application.py:415`). 프론트는 안건별 `manual/carried` 를 지우고 `{title}` 만 보낸다(`BookingModal.tsx:251`) |
| SH-IMP-006 timeout | Codex `timeout_seconds=90`, Claude `180` 이 고정값이고 env 가 없다. 배치·웜스타트·최종·대화가 같은 값을 쓴다. 타임아웃은 세션 유실로 분류되지 않아서 3회 시도가 모두 같은 세션을 resume 하며 90초씩 기다린다 |
| SH-IMP-006 누락 | 세션을 이어 쓰는 최종 합성은 **재전사 원문을 프롬프트에 싣지 않는다**(콜드 스타트에서만 싣는다). 배치 실패 구간은 커서가 전진하지 않아 다음 배치에 다시 실린다. 다만 그 전 turn 이 세션에 남는지는 CLI 내부 동작이라 코드로 판단할 수 없다 |
| SH-IMP-006 교정 | 교정 단계·필드가 **없다**. `correction_kind` 는 쓰이지 않는 TypedDict 필드 하나뿐이다 |
| SH-IMP-006 기한 | `next_meeting_after` 가 「이어진 회의」 가 아니라 **이월 회의(날짜·상태 필터 없음) 또는 같은 owner 의 아무 다음 예약**을 고른다. 날짜는 KST 변환 없이 `.date()` 로 뽑는다. 세 경로 모두 회의일보다 이른 기한을 만들 수 있다 |
| SH-IMP-006 참석 N명 | 화자 수가 아니라 참석자 행(owner 포함) + 사외 참석자 수다. quick_start 는 참석자가 owner 1명이다 |
| SH-IMP-006 메디니스 | 카탈로그 서버 전량 주입 · 단계별 timeout(배치 240 / 최종 900) · 최종 전체 발화 재주입 · Pass1 정정 → Pass2 다시 쓰기 · 보정 표. strong-hajin 에는 다섯 가지 모두 없다(§5.7 대조표) |
| SH-IMP-012 슬랙 | 나간 뒤에도 분배가 남는 창이 **있다**. 재확인은 워커 프로세스 실행마다 방당 1회뿐이고(`_verified_this_run`), `member_left_channel` 등 이벤트는 처리하지 않는다. 창 길이는 시간 상수로 정해지지 않는다(워커 재시작 등 사건이 있어야 닫힌다) |
| SH-IMP-013① 카톡 | 이름은 방을 고를 때 한 번 서버로 오고, 비어 있으면 chatId 가 이름이 된다. 서버에는 숨김·필터 규칙이 없다. 데스크톱이 이름을 못 만들면 `"(이름 없음)"` 을 보낸다 |
| SH-IMP-008·015 | 참고 자료 `resource_type` 은 `task`·`work_request` 두 가지(나열 지점 5곳). 방 메시지는 과거 방향 커서만 있다. `(room_id, sent_at)` 인덱스로 양방향 범위 조회는 가능하다 |
| SH-IMP-010 | `/api/inbox/stream` 사건은 `ready` 와 3종(`inbox.message_arrived`·`inbox.reply_result`·`integration.changed`)이다. 건수가 바뀌면 사건이 나가지만, 진행 커서·방 이름·인원만 바뀌면 나가지 않는다 |

---

## 1. SH-IMP-001 · 017 — AX 업무 생성 vs AX 회의 생성

### 1.1 AX 업무 생성 경로

**의도 인식**
- 서버 분류기는 코드에 없다(`grep -rn "classify\|intent_" B/platform/conversations.py B/modules/ax_execution B/bootstrap/conversation_worker.py` → 0건)
- 대신 프롬프트 정책 6종이 모든 대화 프롬프트 앞에 붙는다: RELATIONSHIP·MEETING_CREATION·TASK_PROGRESS·WORK_AND_REPORT_ROUTING·ANSWER_PRESENTATION·FOLLOW_UP. 조립 위치는 `B/platform/codex_cli.py:529-536`, Claude 는 같은 문자열을 import 한다(`B/platform/claude_cli.py:302-317`)
- 생성 지시(`codex_cli.py:404-406`): 「…관련 회의·기존 업무·자료와 연결할 프로젝트를 먼저 찾아 읽은 뒤 … `task_create_self`로 Action 제안을 준비한다. … 사람의 승인 전까지 업무가 생성되지 않는다」
- 갈래 선택(`codex_cli.py:457-460`): 배정은 `task_assignment_candidates` → `task_assign`, 수평 요청은 `work_request_assignee_candidates` → `work_request_create`

**탐색 단계** — 모델이 스스로 하고, 서버는 강제하지 않는다
- `codex_cli.py:464-468`: 「초안을 만들기 전에 관련 회의·기존 업무·자료를 찾는다 — 짧은 핵심어(2~3 단어. 이름 검색은 제목 부분 일치…)로 `graph_search`·`my_meeting_list`·`material_search`… 가장 관련 높은 것만 상세를 최대 3건」
- 상한(`codex_cli.py:469`): 「도구마다 한 번 … 상세는 최대 3건, 연결 탐색(`list_projects`·`graph_neighbors` 또는 `task_list`)은 필요할 때 한 번만 … 턴에는 시간 제한이 있다」. 이 시간 제한이 §5.1 의 90초다

**채우는 값**
- 도구 설명(`B/modules/ax_execution/tool_catalog.py:546`)
  - title 은 필수(1–300자)
  - description·checklist(최대 50)는 모델이 직접 제안한다
  - 날짜·사람은 대화에 나온 것만 쓴다
  - 「Files and links are not form fields」
- 같은 규칙이 정책에도 있다(`codex_cli.py:478-484`)
- MCP 인자(`B/entrypoints/mcp.py:727-753`): `title, idempotency_key, checklist, reference_task_ids, parent_task_id, description, start_date, due_date, project_id, assignee_id, cc_member_ids, preceding_task_ids, approver_id`
- 검증 모델: `TaskCreateInput`(`B/modules/work/task_creation.py:43-90`)

**초안(Action 카드)**
- 위임 턴(`AX_MCP_CAUSATION_ID`)에서는 생성하지 않고 `_propose_chat_action('task.create_self','업무 생성 확인',payload)` 를 부른다(`mcp.py:750`, `:762-778`)
- 저장은 `propose()`(`B/platform/actions.py:228-292`)
  - 같은 턴·같은 action_type 에는 슬롯이 1개다. payload 가 다르면 `TurnProposalSlotTaken`(`:257-270`)
  - 원장(`:340-420`): `DecisionItemRecord(kind="ax.task.create_self")`(`:374`) · `SubmissionRecord(v1, submitted_by="ax")` · `ReviewAssignmentRecord(pending)`
- 카드 계약 `editor:"task"`(`actions.py:1852`), 필드는 `:1740-1850`, `save_command:"save_draft"`(`:1856`)

**확정**
- 명령: `confirm`(「이 내용으로 업무 생성」, `B/modules/actions/policy.py:21`) · `reject` · `save_draft`(회차만 올린다, `policy.py:32-35`)
- 경로: `ActionCenter._confirm`(`B/platform/action_center.py:813-870`) → `decide_ax_confirmation`(`B/modules/actions/confirmation.py:178-`) → 실행 분기(`actions.py:838-848`, `idempotency_key=str(action.id)`) → `_claim_action_materials`(`actions.py:1028-1068`)

**프론트(참고)**
- `F/features/chat/MessageList.tsx:308-315` 에서 `AxDraftCard` 로 간다. 대상 kind 는 `AX_DRAFT_KINDS={"ax.task.create_self","ax.work_request.create"}`(`F/features/action/AxDraftCard.tsx:35`)
- 「스텝」 의 실체는 쪽 4개다: `["기본 정보","체크리스트","업무 연결","자료"]`(`F/lib/labels.ts:1360`), 쪽 이동은 `AxDraftCard.tsx:349-381`
- 버튼: 거절 · 수정(`CreateWorkModal`, `:422-450`) · 등록(confirm, `:413-417`)

### 1.2 프로젝트·연관 업무 탐색 (SH-IMP-017 핵심)

지시 문장(`codex_cli.py:472-477`): 「프로젝트는 `list_projects`(참여 프로젝트) 또는 이름으로 `graph_search`, 그 프로젝트의 업무는 `graph_neighbors(node='project:<id>')` 또는 `task_list`로 찾는다. … **한 후보로 확정될 때만** `project_id`·`parent_task_id`·`preceding_task_ids`·`reference_task_ids`를 채운다. 못 찾았거나 후보가 여럿이면 비워 두고…」. 도구 설명에도 같은 문장이 있다(`tool_catalog.py:546`).

| 도구 | 위치 | 인자 | 반환 범위 | 상한 |
|---|---|---|---|---|
| `list_projects` | catalog `:239-244`, `mcp.py:1531` | 없음 | 참여(배정) 프로젝트 전부(`B/modules/work/projects.py:357-366`, `:508-516`) | **없음** |
| `project_list` | catalog `:432-437`, `mcp.py:1726-1728` | 없음 | 같은 `list_projects` 를 `{"entries"}` 로 감싼 것 | 없음 |
| `task_list` | catalog `:569-575`, `mcp.py:1971-1972` | `include_closed` 만 | 읽을 수 있는 업무 전부(`B/modules/work/application.py:1007-1100`) | **없음**, 프로젝트 필터 없음 |
| `graph_search` | `mcp.py:1939`, `B/modules/work/graph.py:102-119` | `query`, `limit=20` | person·team·project·task·work_request·meeting | 기본 20 / 최대 **50**(`graph.py:34-35`) |
| `graph_neighbors` | `mcp.py:1942`, `graph.py:352-374` | `node`, `limit=20` | 프로젝트의 멤버 edge + `part_of` 업무 edge | 최대 50(`graph.py:612-629`) |
| `material_search` | `mcp.py:1948-1951` | query·resource_type(s)·resource_id·material_id·`limit=5`·기간 | 발췌·source_contexts | 최대 **8**(`B/modules/work/material_extraction.py:24`), 발췌 280자(`:23`) |

- **매칭은 제목 부분 일치뿐이다**: `matches()` = `folded(query) in folded(text)`(`B/modules/work/search.py:25-27`), 프로젝트 매칭은 `graph.py:114`
- 반환 필드
  - `list_projects`: `project_id, name, description, state, starts_on, ends_on, external_key, version`(`projects.py:534-544`)
  - `task_list`: `TaskMutationResult`(`B/modules/work/task_results.py:67-97`) + checklist_progress·origin·assignee(`:194-197`). `parent_task_id` 는 이 TypedDict 에 없다
  - graph task 노드: `kind,id,title,state,date,project_id`(`graph.py:676-686`)
- **서버가 미리 싣는 맥락**(`codex_cli.py:537-565`): `asked_at`, 최근 발화 최대 6개(`boot/application.py:2695`, `:2754-2766`), 이전 턴에서 조회한 ref 최대 12개(`:2694`, `:2737`, `:2753`), 사용자가 붙인 context_references(`B/platform/conversations.py:326-334`). **프로젝트·업무 목록을 미리 싣는 코드는 없다**
- 관찰한 사실
  1. 모델이 보는 후보와 카드 선택지가 다르다. 카드의 `project_options` 는 프로젝트 전부(`actions.py:1722-1726`), `reference_options` 는 `include_closed=True` 업무 전부(`:1717-1720`)다. 모델 쪽 `task_list` 기본값은 `include_closed=False` 다
  2. `graph_neighbors(project)` 는 멤버 edge 를 먼저 넣고 업무 edge 를 넣은 뒤 limit 20 에서 자른다(`graph.py:361-374`, `:627`). 멤버가 많은 프로젝트는 업무가 밀려나고 `truncated` 만 표시된다
  3. 중복 후보 탐지는 코드에 없다(grep `duplicate|중복` 결과는 선행 ID 중복 거절 `task_creation.py:83-86` 뿐)
  4. 선행은 `preceding_task_ids` 로 보인다. 후행은 저장하지 않고 역조회만 한다(`task_results.py:213-228`). 같은 프로젝트인지는 실행 때 서버가 검증한다(`actions.py:1782-1785`). 초안 단계에서 후행을 찾으라는 지시는 없다

### 1.3 참고자료

| 경로 | 누가 | 소스·계약 | 근거 |
|---|---|---|---|
| (a) 근거 자료 | 서버(자동) | 제안한 턴이 `material_search` 로 얻은 `ConversationContentEvidenceRecord` 를 `EvidenceRecord(evidence_role="supporting", adopted_by="ax")` 로 고정. 카드 필드 「근거 자료」. **업무 첨부(binding)가 아니다** | `boot/application.py:4474-4482`, `actions.py:404-420`, `:2188-2200`, `:1647` |
| (b) 첨부 초안 — 사람 | 사람 | `POST /api/action-items/{id}/material-drafts/{files\|links}`. `source_kind` 는 `external_link`·`file`, TTL 24h | `F/lib/api.ts:1149-1175`, `F/features/work/WorkModals.tsx:4712-4740`, `B/modules/work/action_materials.py:17,80,115` |
| (b) 첨부 초안 — AI | AI 제안 → 사람 승인 | `action_material_link_stage`(위임 턴에서는 그 자체가 별도 제안 `action.material.link.stage`), `file_attachment_request(intent='action_material')`(파일은 사람이 고른다) | `tool_catalog.py:51`, `mcp.py:1809`, `:520-525`, `B/modules/ax_execution/browser_interactions.py:42` |

- 첨부할 수 있는 kind 는 `task.create_self`·`task.assign`·`meeting.reservation.create` 뿐이다(`B/modules/actions/confirmation.py:38-40`). `work_request.create` 는 `[]` 다(`action_materials.py:66-67`)
- 확정 때 `attachment_draft_ids` → `validate_claim`(`action_center.py:849-856`) → `_claim_action_materials`(`actions.py:1028-1068`)
- **검색으로 찾은 기존 자료(material_id)를 초안에 붙이는 경로는 코드에 없다**(`source_kind` 2종뿐)

### 1.4 AX 회의 생성 경로

- 도구 `meeting_create`(`mcp.py:1734-1738`) → facade `create_current_meeting`(`mcp.py:822-834`) → `_propose_chat_action("meeting.reservation.create","회의 생성 확인",payload)`(`mcp.py:826`). 원장 kind 는 `ax.meeting.reservation.create`, 옛 `meeting.create` 는 폐기(`policy.py:39-41`)
- 프롬프트 `MEETING_CREATION_POLICY`(`codex_cli.py:425-441`)
  - 제목·날짜와 시각 하나를 알면 `meeting_create` 카드를 먼저 준비한다
  - 찾은 참석자만 넣는다
  - 관계·직책 표현은 그대로 `graph_search` 에 넘긴다
  - 기본 1시간
  - 날짜와 시각을 모두 추정해야 하면 묻는다
  - 「조직을 생략한다」(`:436-437`)고 하지만 입력 스키마에 조직 필드는 없다
- 입력 `MeetingReservationInput`(`B/modules/meetings/commands.py:132-160`, `extra=forbid`): `title, purpose, starts_at, ends_at, location, attendee_ids, external_attendees, agendas, carried_from_meeting_id, room_id`. `room_id` 가 있으면 `idempotency_key` 가 필수다(`mcp.py:124-150`). 제안 때 이 스키마로 고정된다(`actions.py:308-319`)
- 카드 `editor:"meeting"`(`actions.py:2064-2103`), confirm 라벨 「이 내용으로 회의 생성」(`policy.py:24`)
- 실행: `actions.py:714-718` → `_execute_meeting_action`(`boot/application.py:3700-3725`, 회의실 예약 포함) → `_claim_action_materials` → `_attach_meeting_references`(`actions.py:1070-1124`)
  - `_attach_meeting_references` 는 `reference_task_ids` 를 읽는다. 그런데 이 키는 `MeetingReservationInput` 에 없고 `extra=forbid` 라서 실제로 들어올 길이 없다(`F/features/action/ActionMeetingCard.tsx:30-31` 주석 「reservation contract does not carry it」)
- 프론트: `MessageList.tsx:324-331` → `ActionMeetingCard`(루트 `action-meeting-card`, `ActionMeetingCard.tsx:239`). 쪽 나눔 없이 한 장에서 요약과 편집을 전환한다(`:244-300`)
- 프로젝트·연관 업무: 필드도 지시도 없다(`commands.py:132-145`). 자료: 첨부 초안은 가능하지만 `material_search` 지시는 없다

**업무 생성과 갈라지는 곳**

| 항목 | 업무 생성 `task.create_self` | 회의 생성 `meeting.reservation.create` |
|---|---|---|
| MCP 도구 | `task_create_self`(`mcp.py:727`) | `meeting_create`(`mcp.py:1734`) |
| 프롬프트 | `WORK_AND_REPORT_ROUTING_POLICY`(`codex_cli.py:454-485`) + `:404-406` | `MEETING_CREATION_POLICY`(`:425-441`) |
| 사전 탐색 | graph_search·my_meeting_list·material_search 각 1회, 상세 3건 | 참석자 확인용 graph_search·graph_neighbors 만 |
| 프로젝트 | list_projects / graph_search, 단일 후보일 때만 | 없음(필드 없음) |
| 연관 업무 | parent/preceding/reference | 없음(스키마에 없음) |
| 내용 제안 | description·checklist 를 채운다(`codex_cli.py:478-479`) | 지시 없음(안건은 선택) |
| 날짜·사람 | 대화에 나온 것만 | 1시간 보정, 미확정 참석자는 비운다 |
| 제안 정규화 | payload 를 그대로 저장(`actions.py:301-306`), 표시 때 정규화 | `MeetingReservationInput` 으로 고정(`:302-303`) |
| 카드 | `AxDraftCard` 4쪽 | `ActionMeetingCard` 한 장 |
| 수정 | 「수정」 → `CreateWorkModal` → `save_draft`(회차+1) | 카드 안에서 편집. `save_draft` 없음(`DRAFT_SAVE_ACTION_TYPES`, `policy.py:35`) |
| 첨부 초안 | 가능 | 가능 |
| 확정 실행 | `create_task`(`actions.py:838-848`) | `_execute_meeting_action` + 회의실(`boot/application.py:3700`) |
| 멱등 | `idempotency_key` 필수 인자 | room_id 가 있을 때만 필수, 없으면 `_mutation_key`(`mcp.py:832`) |

### 1.5 만들어진 회의를 AX 채팅에서 바꾸는 도구 (SH-IMP-016)

- **있다**: `meeting_update`(catalog `:85`, `mcp.py:1744-1746`, facade `:840-847`) → 제안 kind `meeting.info.update`(사람 확인)
- `MeetingInfoPatch`(`commands.py:163-196`): `title, purpose, starts_at, ends_at, location(≤300 자유 텍스트), attendee_ids, external_attendees`
- 제약(`mtg/application.py:474-520`): 참석자만 바꿀 수 있고, 「예정」·「완료」 상태에서만 된다. 시각이 실제로 바뀌면 겹침을 검사한다
- 시각이 바뀌면 기존 회의실 예약을 같은 방으로 옮긴다(`boot/application.py:3734-3744` → `_sync_room_reservation`, §2.2)
- **`room_id` 를 바꾸는 필드는 없다**(grep `reschedul|room_change|change_room|meeting_room_(update|change|reserve)` in mcp.py·tool_catalog.py → 0건)
- 회의 관련 MCP 도구 전부(`mcp.py`)
  - 조회: meeting_list 1694 · my_meeting_list 1698 · meeting_get 1702 · meeting_room_list 1706 · meeting_transcript 1710 · meeting_materials_list 1714 · meeting_viewer_list 1718 · meeting_export 1722 · project_list 1726 · member_list 1730 · open_meeting_material 1459
  - 명령: meeting_create 1734 · meeting_quick_start 1740 · meeting_update 1744 · meeting_cancel 1748 · meeting_note_delete 1752 · meeting_start 1756 · meeting_end 1760 · meeting_finalize_retry 1764 · meeting_todo_promote 1768 · meeting_todo_remove 1775 · meeting_agenda_add 1779 · meeting_agenda_update 1783 · meeting_agenda_remove 1787 · meeting_memo_write 1791 · meeting_material_detach 1795 · meeting_share 1799 · meeting_revoke_share 1803 · recording_request 1438

---

## 2. SH-IMP-003 · 016 — The Connect 회의실

### 2.1 클라이언트와 부르는 API 전부

- 어댑터는 `B/platform/the_connect.py` `TheConnectGateway`(`:54`)다. 경계 Protocol 은 `B/modules/meetings/rooms.py:209-228`(rooms/available/members/create/update/cancel), 조립은 `boot/application.py:1030-1041`(계정이 설정됐을 때만)
- 인증
  - **회사 공용 계정 1개**(email/password/company_id, `the_connect.py:57-66`). 사용자별 인증은 하지 않는다
  - 쿠키는 프로세스 메모리에만 둔다(`:74-76`)
  - 401/403 이면 한 번 재로그인하고 재시도한다(`:175-179`)
- timeout: 요청마다 `timeout=self._timeout`(`:201`) = `TDL_HTTP_TIMEOUT_SECONDS`, 기본 20.0초(`B/bootstrap/settings.py:123`, `:224`)
- 오류 매핑
  - 2xx 가 아니면 `RoomGatewayUnavailable`(`:180-182`)
  - `/api/reservations` 쓰기 중 네트워크 예외면 `RoomOutcomeUnknown`(`:207-210`)
  - 그 밖은 `RoomGatewayUnavailable`(`:211`)

| 메서드·경로 | 위치 | 보내는 값 | 응답 처리 |
|---|---|---|---|
| `POST /api/auth/login` | `:190` | `{email,password,remember:true}` | 200 확인, 쿠키 |
| `GET /api/rooms` | `:88` | — | `id/name/capacity`. **id≤7 이고 「스튜디오」 가 아닌 방만** 남긴다(`:39-42`, `:89-93`), 300초 캐시(`:37`, `:85-87`) |
| `GET /api/reservations?date=` | `:101` | — | 그날 예약을 받아 **로컬에서 겹침을 판정**해 빈 방을 계산(`:97-104`, `_overlaps` `:50-51`). 전용 가용 API 를 쓰는 것이 아니다 |
| `GET /api/members` | `:109` | — | `{name,email}`. 사내 참석자를 계정에 매핑(`rooms.py:247-267`) |
| `POST /api/reservations` | `:122` | `room_id,date,start_time,end_time,company_id,title,password:"login",attendees(이름 콤마),booker_email,participants(이메일 콤마),notify`(`_body` `:144-164`) | `id` → external_id |
| `PUT /api/reservations/{id}` | `:137` | `{date,start_time,end_time[,room_id]}`. **참석자를 싣지 않는다**(`:128-133`: PUT 에 participants 를 넣으면 200 을 주면서 참석자를 지운다는 실측 기록) | 본문 무시 |
| `DELETE /api/reservations/{id}` | `:140` | — | 본문 무시 |

env(`settings.py:116-123`, `:219-224`): `TDL_BASE_URL`(기본 `https://connect.tdl-cloud.com`) · `TDL_EMAIL` · `TDL_PASSWORD` · `TDL_COMPANY_ID`(3) · `TDL_NOTIFY`(False) · `TDL_HTTP_TIMEOUT_SECONDS`(20.0). 「설정됨」 은 email 과 password 가 둘 다 있을 때다(`:160-162`).

### 2.2 생성·수정·취소 때 Connect 호출

- **생성: 실제로 예약한다.** 예약을 먼저 하고 회의를 만든다
  - `room_id` 가 없으면 Connect 를 부르지 않는다(`boot/application.py:1568-1572`)
  - 있으면: Idempotency-Key 필수(`:1574`) → 로컬 검증·겹침(`:1587`) → 시도 원장(`:1597`) → `_reserve_room`(`:1067-1130`) → 회의 생성 + `attach_reservation(location=room_name)`(`:1613-1615`)
  - **가용 조회도 한다.** 어댑터 `create` 가 POST 전에 `available()` 을 불러, 차 있으면 `RoomUnavailable(available=…)`(`the_connect.py:118-121`)
  - 차 있으면 `choose_replacement` 가 정원 ≥ 인원인 가장 작은 방으로 자동 대체한다(`rooms.py:318-332`, `boot/application.py:1098-1124`). 대체할 방도 없으면 409 `RoomBookingRefused` + `available_rooms`(`B/entrypoints/http.py:548-557`)
  - 인원 = 사내 + 사외(`rooms.py:309-315`)
- **수정**
  - `starts_at`/`ends_at` 키가 있을 때만 `_sync_room_reservation` → `gateway.update`(PUT)(`boot/application.py:1391-1397`, 호출 `:1737-1746`)
  - **가용 조회가 없다**(`the_connect.py:128-137`)
  - 기존 room_id 를 그대로 보낸다(`boot/application.py:1396`)
  - 참석자는 빈 값이다(`:1388-1389`)
  - PUT 이 성공하면 `return {}` 로 끝나 location 을 다시 쓰지 않는다(`:1398-1399`). 실패나 불명이면 location 을 room_name 으로 다시 쓴다(`:1421-1424`)
  - Action `meeting.info.update`(`:3734-3743`)·레거시 `meeting.update`(`:3744-3763`)도 같은 동기화를 탄다
  - 프론트 `MeetingEditModal.tsx:119-125` 는 저장할 때마다 `starts_at`/`ends_at` 을 함께 보낸다. 그래서 시간이 안 바뀌어도 예약 회의는 PUT 이 나간다
- **취소**
  - `cancel_meeting`(`:1748-1753`)·Action `meeting.cancel`(`:3782-3787`) → DELETE(`:1372-1378`). 성공하면 `location=None`(`:1423`)
  - DELETE 가 실패해도 회의 취소는 유지된다(`:1411-1420`)
  - `DELETE /api/meetings/{id}?scope=note` 는 예약을 건드리지 않는다(`http.py:977-990`)
- 미사용: `_release_orphan_reservation`(`boot/application.py:1622-1630`)은 호출처가 0이다
- **`meeting_room_creation_attempts`**(`B/platform/persistence.py:328-354`)
  - provider 에 조회·멱등 API 가 없어서 POST 가 두 번 나가는 것을 막는 영속 울타리다(docstring `:329-335`)
  - UNIQUE(owner_id, request_key)(`:338-340`), 상태는 `pending|booked|compensated|needs_verification|refused`(`:347`)
  - 처리(`boot/application.py:1191-1318`)
    - 없으면 pending 으로 insert
    - fingerprint 가 다르면 충돌
    - refused 는 저장된 거절을 다시 낸다
    - compensated 는 pending 으로 돌려 재시도
    - booked/needs_verification 은 저장값을 반환
    - 기존 pending 이면 다시 보내지 않고 needs_verification 으로 고정
  - Action 경로 키는 `action:{id}:{fingerprint}`(`:3984-4031`). 보상 DELETE 는 `:1632-1723`
- AX 가 「4인실 없음」 이라고 답한 근거: `meeting_room_list`(`mcp.py:1705-1707` → `boot/application.py:1043-1065`)가 시간을 주면 빈 방에 `available:true` 를 붙인다(`:1061-1062`). **정원 필터는 없다**(`grep -n capacity B/entrypoints/mcp.py` → 0). 4인 판단은 모델이 capacity 를 보고 한다. 그 대화에서 실제로 어떤 도구를 불렀는지는 코드로 알 수 없다(코디 확인 필요 §8)

### 2.3 코드에서 확인되는 Connect 기능

| 기능 | 여부 | 근거 |
|---|---|---|
| 방 목록 | 있음 | `the_connect.py:82-95` |
| 가용 조회 | 있음(날짜별 예약 목록 + 로컬 겹침, 전용 API 아님) | `:97-104` |
| 예약 생성 | 있음 | `:113-126` |
| 예약 수정(시간·방) | 있음. 호출부는 시간만 바꾸고 방은 기존 그대로 | `:128-137`, `boot/application.py:1396` |
| 예약 취소 | 있음 | `:139-140` |
| 구성원 조회 | 있음 | `:106-111` |
| 예약 단건 조회·멱등 키 | 코드에 없음 | `persistence.py:331`, `boot/application.py:1401` 주석 |
| 외부인 등록 | 코드에 없음(「엔드포인트 없음」 주석) | `rooms.py:10-12`, `:292-294` |
| 수정 시 참석자 변경 | 의도적으로 금지 | `the_connect.py:128-133` |

### 2.4 회의 수정 API 전부

| 경로 | 위치 | 페이로드 |
|---|---|---|
| `PATCH /api/meetings/{id}` | `http.py:965-975` | `MeetingInfoPatch`(`commands.py:163-196`): title·purpose·starts_at·ends_at(tz 필수, UTC 정규화)·location(≤300)·attendee_ids·external_attendees, `exclude_unset` |
| `POST /api/meetings` | `http.py:907-929` | `MeetingReservationInput` + `Idempotency-Key` |
| `GET /api/meetings/rooms?starts_at&ends_at` | `http.py:931-948` | 회의실 목록 |
| `DELETE /api/meetings/{id}?scope=meeting\|note` | `http.py:977-990` | 취소 / 회의록만 삭제 |
| MCP `meeting_update` | `mcp.py:1743-1745` | 위 Patch → 제안 `meeting.info.update` |
| 레거시 Action `meeting.update` | `commands.py:18-40`, `actions.py:153` | title·description·starts_at·ends_at·visibility·expected_version. location·참석자는 없다 |

- **겹침 `MEETING_TIME_OVERLAP`**
  - 예외는 `MeetingTimeOverlap`(`B/modules/meetings/domain.py:30-55`). 문자열은 docstring 에만 나온다(`:31`)
  - 발생: `_require_free_time`(`mtg/application.py:358-387`), HTTP 409(`http.py:573-574`)
  - 비교 대상: **주최자 + 활성 참석자의 시간 블록**(회의 + 업무 시간 배정), 반열림 `[시작,끝)`, 자기 회의는 제외(`B/platform/time_blocks.py:69-92`). 사외 참석자는 대상이 아니다
  - 생성 때는 provider 호출 전에 검사한다(`mtg/application.py:418`). 수정 때는 시각이 실제로 바뀐 경우에만 바뀐 뒤의 명부로 검사한다(`:506-512`). 참석자만 바뀌면 검사하지 않는다
  - **Connect 회의실 점유와의 비교는 여기에 없다**
- **장소 저장**
  - `meetings.location String(300)` 자유 텍스트(`persistence.py:305`)
  - 방은 별도 `meetings.room_reservation` JSON `{status,room_id,room_name,external_id,reason,replaced,requested_room_name}`(`persistence.py:306-309`, `rooms.py:165-175`)
  - 예약에 성공하면 location 에 room_name 을 복사한다(`boot/application.py:1615`)
  - 수정에서 location 을 바꾸면 텍스트만 바뀐다(`mtg/application.py:519-520`)
  - 응답에서 external_id 는 숨긴다(`rooms.py:177-186`)

---

## 3. SH-IMP-005 — 「이전 회의 정보 불러오기」

### 3.1 부르는 API와 복사하는 필드
- 「이전 회의 정보 불러오기」 라는 문구는 코드에 없다(`grep -rnF` → 0). 실제 UI 는 예약 모달의 제안 카드 「지난 「{회의명}」」 + 버튼 「불러오기」 다(`F/lib/labels.ts:869-870`)
  - 회의명이 지난 회의와 **정확히 같을 때만** 나타난다(`BookingModal.tsx:174-179`)
  - 핸들러는 `applySuggestion`(`BookingModal.tsx:199-236`), 주석 「일시 · 장소 · 참석자 · 목적을 넣고 결론 안 난 안건만 넘겨 담는다 (X-121)」(`:199`)
- 전용 API 는 없다. `readMeeting` = `GET /api/meetings/{id}`(`F/lib/api.ts:1215-1217` → `http.py:960` 부근 → `mtg/application.py:291-293`)로 회의 상세를 통째로 읽는다

| 필드 | 코드 | 비고 |
|---|---|---|
| 날짜 | `BookingModal.tsx:206` | 지난 회의 날짜로 **덮어쓴다** |
| 시작 | `:207` | **버그1** |
| 종료 | `:208` | **버그1** |
| 목적 | `:209` | 이미 쓴 값이 있으면 유지 |
| 장소 | `:210` | location 이름으로 회의실을 매칭 |
| 참석자 | `:211-215` | 덮어쓴다. 사외 참석자는 복사하지 않는다 |
| 안건 | `:216-228` | final 벌에서 `!concluded` 이고 제목이 안 겹치는 것만 `{source:"carried"}` 로 추가. 수기 안건(`manual`)은 유지 |
| 이어온 회의 | `:229` | `setCarried(id)` → 제출 때 `carried_from_meeting_id` |

**시간이 들어가는 이유**: 서버는 상세 응답의 `starts_at`/`ends_at` 을 줄 뿐이다. 그 값을 폼에 넣는 것은 화면(`:206-208`)이고, 제출 때 그 폼 값으로 `starts_at`/`ends_at` 을 만든다(`:244-246`).

### 3.2 안건 `source` 값과 결정 주체
- 값: `AGENDA_SOURCES={"manual","set","carried","derived"}`(`B/modules/meetings/domain.py:140`, 뜻은 `:127-139`). `set`·`derived` 는 「만드는 경로가 아직 없다」(`:134`)
- 검사: `ensure_agenda_source`(`domain.py:190-201`). memo 벌만 출처를 가진다
- 컬럼: `meeting_agendas.source String(20) NULL`(`persistence.py:379`), `concluded Boolean`(`:380`), `meetings.carried_from_meeting_id` FK(`:319`)
- 프론트 라벨: `carried` = 「지난 회의에서 넘어옴」(`F/lib/labels.ts:749-754`, `:752`)

| 경로 | source | 근거 |
|---|---|---|
| 예약 생성(HTTP·MCP·승인 재실행) | `carried_from_meeting_id` 가 있으면 **안건 전부 `carried`**, 없으면 `manual` | `mtg/application.py:412-415`, `:328-331` |
| quick_start | manual | `:463-470` |
| legacy note | manual | `:560-566` |
| 회의 중·예정 상태의 안건 추가 | memo 벌이면 manual | `:1225` |

**수기 안건이 「넘어옴」 이 되는 경로**
1. 수기 입력 → 모달 상태 `{source:"manual"}`(`BookingModal.tsx:443`)
2. 「불러오기」 → `setCarried(id)`(`:229`)
3. 제출 → `agendas.map(a=>({title:a.title}))` 로 출처를 버리고 `carried_from_meeting_id` 만 싣는다(`:251-252`). API 타입부터 `{title}` 만 있다(`api.ts:1228`). 서버 입력 `MeetingAgendaDraftInput` 은 `title` 만 받고 `extra=forbid` 다(`commands.py:125-127`)
4. 서버가 `drafts` 를 제목 문자열 목록으로 만들고 `source="carried"` 를 전부에 넣는다(`mtg/application.py:413-415`, `:328-331`)
5. `_agenda_view` 가 `source` 를 그대로 내보낸다(`mtg/application.py:1967`)
6. 화면이 그린다: `MeetingDetailPage.tsx:1210` → `AgendaBlock.tsx:155`(`scax-agenda-block__source`)

**같은 결함이 나는 두 번째 입구**: 상세 화면 [다음 회의 예약] 은 `carriedFrom={meeting_id}` 를 넘긴다(`MeetingDetailPage.tsx:1393`, 모달 초기값 `BookingModal.tsx:121`). 이 모달에서 추가한 안건도 전부 carried 가 된다.

`carried_from_meeting_id` 가 출처 판정에 쓰이는 곳은 `mtg/application.py:415` 하나다(회의 단위로 값이 있는지만 본다). 그 밖의 용도
- 상세 응답(`:1805`)
- 합성 입력 `carried_from`(`:791-803`)
- 웜스타트(`:1408-1421`)
- 다음 회의 판정(`B/platform/meetings.py:786-794`, §5.5)
- 승인 편집기(`actions.py:2093`)

### 3.3 「지난 회의에서 결론이 안 난 항목」 을 가져오는 로직
- **프론트에만 있다**
  - 「불러오기」: final 벌 && `!concluded`(`BookingModal.tsx:222-226`, 사용자 결정 주석 `:218-221`)
  - [다음 회의 예약]: 같은 기준(`MeetingDetailPage.tsx:1397-1399`)
- 백엔드는 새 회의에 안건 행을 만들지 않는다. 이전 회의 final 벌 `{title,concluded}` 를 AI 맥락으로만 넘긴다(`mtg/application.py:796-802`, `:1415-1420`)
- `concluded` 를 쓰는 곳
  - 합성 반영(`mtg/application.py:912`, 스키마 `B/modules/meetings/finalize.py:86,129`, 지시 `:317`)
  - 사람 수정(`:1273-1277`)
  - 기본 False(`B/platform/meetings.py:435`)

---

## 4. (빈 번호 — §2 물음 순서상 SH-IMP-006 은 아래 §5)

## 5. SH-IMP-006 — 회의록 파이프라인

### 5.1 timeout

| provider | 단계 | 위치 | 제한 |
|---|---|---|---|
| Codex | 프로필 기본 | `B/platform/codex_cli.py:95` `timeout_seconds: int = 90` | 90s |
| Codex | `generate`(일보 등 단발) | `:136-142` | 90s |
| Codex | `converse` = 대화 · 회의 웜스타트 · 배치 · 최종 합성 | `:216-225` | 90s |
| Claude | 프로필 기본 | `B/platform/claude_cli.py:74` `= 180` | 180s |
| Claude | generate / converse | `:108` / `:179` | 180s |
| 재전사 | `TIMEOUT_SECONDS` | `B/modules/meetings/retranscribe.py:57` | 1200s |

- 프로필은 `CodexCliProfile(runtime_home=…)` 한 곳에서만 만든다(`boot/application.py:4747`). timeout 을 넘기지 않으므로 항상 90이다. Claude 는 `ClaudeCliProviderAdapter(scax_mcp_server=…)`(`:4755-4757`)이고 프로필이 없다
- 회의 세 호출(웜스타트 `boot/application.py:614-617`, 배치 `:619-622`, 최종 `:516-532`)은 모두 `meeting_batch_provider()`(`:2093-2100`) → `create_conversation_provider`(`:4767-4772`)로 같은 provider 를 쓴다. 단계별로 다르게 둘 자리가 없다
- **env override 는 코드에 없다**(`grep -rnE "AI_TIMEOUT|CODEX_TIMEOUT|CLAUDE_TIMEOUT|CLI_TIMEOUT|PROVIDER_TIMEOUT|CodexCliProfile\(|ClaudeCliProfile\("` → 생성 지점만). settings 의 timeout env 는 material·report·room_booking 용뿐이다(`settings.py:200-224`). `AX_MEETING_BATCH_MAX_WAIT_SECONDS`(90, `:207`)는 배치 트리거 대기 시간이지 provider timeout 이 아니다
- 래퍼: deadline 을 넘기면 프로세스 그룹에 SIGINT→SIGTERM→SIGKILL(각 3초 유예), 그다음 `TimeoutExpired`(`B/platform/cli_process.py:143`, `:170-174`, `:184-201`) → `ProviderRequestFailed("Codex CLI conversation timed out")`(`codex_cli.py:226-227`, Claude `claude_cli.py:184`)
- 타임아웃은 returncode 검사 전에 raise 된다. 그래서 `_session_on_disk`(`codex_cli.py:242-245`)에 닿지 않고 **세션 유실로 분류되지 않는다** → 콜드 스타트 폴백도 없다
- Claude 에는 `ProviderSessionUnavailable` 을 던지는 곳이 없다. 그래서 resume 이 실패하면 콜드 스타트 대신 일반 실패가 된다

### 5.2 중간(배치)

- **웜스타트 맥락**(`mtg/application.py:1399-1438`, 프롬프트 `B/modules/meetings/batch.py:180-233`)
  - persona_id·meeting_id·title·purpose·location
  - `attendee_count`(행 수, `:1429`)
  - 사람 벌 안건 `{title,source}`(`:1433-1436`)
  - `carried_from` = 이전 회의 final 벌 `{title,concluded}`(`:1409-1422`)
  - 참석자 실명은 싣지 않는다(`:1402`)
  - 마지막 지시: 「「준비됨」이라고만 답하라」(`batch.py:233`)
  - 실패하면 로그만 남기고 재시도하지 않는다(`B/modules/meetings/batch_service.py:177-179`, `:326-331`)
- **모든 회의 호출에 채팅 정책 6종이 붙는다**: `_conversation_prompt` 가 정책을 붙이고 `"User message:\n{prompt}"` 로 감싼다(`codex_cli.py:529-564`, Claude `claude_cli.py:302,310-312`). 그래서 「턴에는 시간 제한이 있다 — 더 찾기보다…」(`codex_cli.py:469`) 같은 업무 생성 지시도 회의 프롬프트에 섞인다
- **배치 프롬프트**: `build_batch_prompt`(`batch.py:260-266`) = 지시 + 스키마 + 확정 발화 + 사람 벌 줄
  - 「이번 구간을 반영해 네 벌 전체를 다시 정리해라…처음부터 다시 낸다」(`:247`)
  - 「앞 구간은 다시 싣지 않는다 — 세션이 기억한다」(`:254`)
  - 숫자·날짜·고유명사는 그대로 옮긴다(`:212`)
  - 입력 `batch_input`(`mtg/application.py:1453-1499`): blocks 는 커서 이후(`:1465-1466`), memos 는 `at_ms >= blocks[0].at_ms`(`:1469-1473`). 회의가 진행 중이 아니면 None(`:1459-1464`)
- **도구**
  - 기본 `("task_list","project_list","meeting_get","member_list")`(`B/bootstrap/settings.py:13`, `batch.py:43`)
  - `AX_MEETING_AI_TOOLS` 는 쉼표로 이름을 더한다(`settings.py:33-37`, `:208`, 합집합 `:165-168`)
  - 전달: Codex `mcp_servers.scax.enabled_tools`(`codex_cli.py:343-346`), Claude `--allowedTools mcp__scax__*`(`claude_cli.py:274-277`)
  - 도구 사용 지시: 웜스타트 「없는 업무를 지어내지 마라 — 도구로 조회해 확인해라」(`batch.py:215`), 「필요할 때 조회해라. 미리 다 주지 않는다. 도구는 전부 조회다」(`:221-222`)
  - **배치 프롬프트 자체에는 도구 지시가 없다**(`batch.py:245-257`). **프로젝트를 조회하라는 지시는 어느 회의 프롬프트에도 없다**
- **배치 실패와 커서**
  - provider 예외(timeout 포함)는 `failed`, 스키마 위반은 `discarded` 로 기록한다(`batch_service.py:265-281`). docstring 「커서는 전진하지 않는다」(`:303-314`)
  - 커서 = `max(to_seq) where status='succeeded'`(`B/platform/meetings.py:940-950`) → `seq > cursor` 블록(`:873-880`)
  - 따라서 **실패 구간 발화는 다음 배치에 다시 실린다**(테스트 `T/contract/test_meeting_memo_batch.py:644`). seq 는 실패 회차도 소비한다(`meetings.py:952-956`)
  - 회의가 끝나면 새 배치가 없어서, 종료 직전 미처리 구간은 세션에 전달되지 않는다(`test_meeting_memo_batch.py:667-672`)
  - `meeting_batch_runs`(`persistence.py:526-547`): seq·status(succeeded|failed|discarded)·trigger_cause(transcript|agenda_switch|timer)·from_seq·to_seq·reason

### 5.3 최종(종료 합성)

- **재료**(`mtg/application.py:774-836`)
  - meeting(title·purpose·starts_on·next_meeting_on·carried_from)
  - memo/ai 안건과 id
  - memo_lines·ai_lines
  - transcript(재전사 블록 전량)
  - `covered_ms=(0,max end_ms)`
  - next_meeting_starts_on
  - session_ref
  - 합성 전에 재전사가 원문을 통째로 갈아 끼운다(`B/modules/meetings/finalize_service.py:141-148`, `:176-208`, `meetings.py:838-862`)
- **이어 쓰기 vs 콜드 스타트**
  - session_ref 가 있으면 resume(`finalize_service.py:210-227`)
  - `FinalizeSessionLost` 일 때만 같은 시도 안에서 콜드 스타트로 넘어간다(`:221-226`). 이 예외는 Codex 의 returncode≠0 && 세션 파일 없음에서만 나온다(`codex_cli.py:242-245` → `boot/application.py:533-535`)
  - `cold_start = not session_ref`(`finalize_service.py:230`)
- **전사 전량이 실리는 조건**: **콜드 스타트일 때만** — `transcript=source["transcript"] if cold_start else None`(`finalize_service.py:241`), docstring 「세션이 발화를 기억하므로 원문은 폴백에서만 싣는다」(`finalize.py:367-368`, `:384-386`). 이어 쓰기 합성은 재전사 원문을 보지 못한다
- **`_bind_evidence` 가 시도 전체를 실패시키는 경로**
  - `demote_line` 이 `covered_ms` 밖 구간을 떼어낸다(`batch.py:166-169`). 그 결과 근거가 0개인 줄이 하나라도 있으면 `SchemaViolation`(`finalize.py:177-186`)
  - 프롬프트: 「하나도 없으면 그 답 전체가 거절된다」(`finalize.py:311-312`)
  - `covered_ms` 는 재전사 원문 기준이다(`mtg/application.py:834`). AI 줄 evidence 는 실시간 원문 ms 이고, 프롬프트는 「그대로 이어 적어라」 라고 한다(`finalize.py:313-314`)
- **재시도**
  - 서비스는 `FINAL_ATTEMPTS=3`(`finalize.py:29`), 루프 `finalize_service.py:156-171`, **backoff 없음**
  - `SchemaViolation` → 「…출력 형식이 맞지 않았습니다」, 그 밖(timeout 포함) → 「회의록을 만들지 못했습니다 — 잠시 뒤 다시 시도해 주세요」(`:51-52`, `:69-75`). 운영 failure_reason 이 이 뒤쪽 문장이다
  - 3회 실패 → `fail_finalize`(`mtg/application.py:952-960`)
  - 워커: `MAX_DELIVERIES=FINAL_ATTEMPTS`(`B/bootstrap/meeting_worker.py:25`). 예외로 끝났을 때만 재배달하고 backoff 는 `min(30, 2*2^(n-1))`s(`:122-123`)
  - 따라서 timeout 이면 같은 세션 resume × 3 × 90s 가 된다

### 5.4 교정
- STT 오인식 교정 단계·필드는 **코드에 없다**(`grep -rni "correct\|오인식\|교정\|오타\|glossary\|용어집" modules/meetings platform/soniox.py platform/meetings.py` → 메모 오타 주석 3곳뿐)
- `correction_kind` 는 `B/modules/meetings/results.py:80` `MeetingRefinedSegmentView` TypedDict 필드다(`:71-90`). backend/src·frontend/src 어디서도 쓰이거나 채워지지 않는다(grep `MeetingRefinedSegmentView|MeetingRefinementView|refinement_revision` → results.py 밖 0건)

### 5.5 기한 버그
- `resolve_due`(`finalize.py:203-212`): ① AI `due_candidate` → ② `next_meeting_starts_on - 1일` → ③ None. **회의일 하한 검사가 없다**
- `next_meeting_after`(`B/platform/meetings.py:786-803`)
  1. `carried_from_meeting_id == 이 회의` 인 회의 중 starts_at 이 가장 이른 것. **날짜·상태 필터가 없다**
  2. 없으면 같은 조직·**같은 owner**·`starts_at > 이 회의`·`status=='scheduled'` 중 가장 이른 것. **연속 회의가 아니라 owner 의 아무 다음 예약**이다
- 날짜 변환: `_aware(next.starts_at).date()`(`mtg/application.py:835`). `_aware` 는 naive 일 때만 UTC 를 붙이고(`:1990-1991`) **KST 로 바꾸지 않는다**. `starts_on` 도 같다(`:814`)
- **회의보다 앞선 날짜가 되는 경로**
  - (a) 이월 회의가 원본과 같은 날이거나 이전이면 기한이 원본 전날 이하가 된다. 이월 회의를 만들 때 원본보다 뒤인지 검사하지 않는다(`domain.py:232-239`, `_carried_source` `mtg/application.py:1732-1738`)
  - (b) 같은 날 오후에 owner 의 다른 예약 회의가 있으면 next=같은 날 → 기한 = 회의 전날
  - (c) DB 가 UTC aware 로 돌려준다면, 다음 회의가 KST 09시 이전일 때 날짜가 하루 당겨진다(예: 다음 회의 10/8 08:00 KST = 10/7 23:00 UTC → 기한 10/6)
  - (d) 스키마 설명(`B/modules/meetings/schemas/ai_final_output.json:130`)에 ② 규칙이 있다. 모델이 `next_meeting_on` 으로 직접 전날을 계산해 ① 로 내면 서버는 형식만 보고 그대로 쓴다(`finalize.py:157-163`)
  - 운영 10-07 사례가 어느 경로인지는 DB 로만 가린다(§8)

### 5.6 「참석 N명」
- 상세 머리 = `meeting.attendees.length + meeting.external_attendees.length`(`F/features/meetings/MeetingDetailPage.tsx:872`, 라벨 `labels.ts:787`). 목록·모달은 `attendee_count = len(attendee_ids)`(`mtg/application.py:1752`)
- attendees 는 `removed_at IS NULL` 인 `MeetingAttendeeRecord`(`meetings.py:193-201`)다. **owner 가 항상 포함된다**(`B/modules/meetings/policy.py:124-126`)
- **quick_start 는 `attendee_ids=[principal]`**(`mtg/application.py:454`) → 「참석 1명」
- 화자 수 `transcript_speaker_count`(`meetings.py:882-890`)는 스트림 ready 프레임에만 쓰이고(`B/modules/meetings/stream_service.py:274-279`) 머리 계산에는 들어가지 않는다

### 5.7 메디니스 대조 (`M/` = mediness `back/app/`, origin/dev `b840254a`)

| 항목 | 메디니스 | strong-hajin |
|---|---|---|
| 세션 | 회의당 1세션. 지시문 전체는 warmup 1회, 배치·최종은 얇은 `turn`(phase 만 다름). 세션을 잃으면 `batch_form_b` 가 지시문 전체를 다시 보낸다(`M/seeds/prompt_seeds.py:620-637`, `:1471-1503`) | 회의당 세션, 웜스타트 1회 + 배치 resume(`batch.py:180-266`). 매 호출 채팅 정책 6종이 붙는다(`codex_cli.py:529-564`) |
| 배치 transcript | 새 문장 + 직전 꼬리 3문장 「(이어짐)」(`M/services/meeting_v2_extractor.py:725-747`) | 성공 커서 이후 블록만(`mtg/application.py:1465`) |
| 배치에 카탈로그 | 얇은 턴에는 없다(warmup 1회), form_b 에서만(`extractor.py:195`, `:199-205`) | 카탈로그 없음. 웜스타트에 회의 정보·안건·참석자 수·이전 회의 안건만(`mtg/application.py:1399-1438`) |
| 이전 회의록 | form_b 에서 최신 회의록 JSON 「갱신하라」(`extractor.py:554-586`) | 이전 회의 final 안건 `{title,concluded}` 만(`:1409-1422`) |
| 화자 정정 델타 | 바뀐 `라벨→이름(확정\|추정)` 만 + 이미 쓴 본문 소급 갱신 지시(`extractor.py:601-658`) | 코드에 없음(웜스타트에 실명을 싣지 않는다 `:1402`) |
| 화자 후보 표 | 미해결 화자 × 남은 참석자(부서·제품)(`extractor.py:750-798`) | 코드에 없음 |
| 도구 상한 | 턴당 6회(프롬프트 지시만, `M/config.py:242`, `prompt_seeds.py:776-777`). claude max_turns 5/15 | 상한 수치 없음(웜스타트 「필요할 때 조회」 `batch.py:221`) |
| 도구 | 읽기 10종, 쓰기 8종 차단(`M/services/meeting_v2_session_tools.py:42-72`) | 기본 4종 task_list·project_list·meeting_get·member_list + env(`settings.py:13`) |
| 배치 timeout | 제출 240 / 결과 280 / runtime wait_for 240(`M/services/meeting_extractor.py:364`, `config.py:224`) | 90(Codex)/180(Claude), 고정 |
| 배치 교정 | 하지 않는다. 보정 표가 오면 파서가 거부(`prompt_seeds.py:733`, `M/services/meeting_v2_minutes_form.py:1075-1078`) | 하지 않는다(단계 자체가 없음) |
| 배치 실패 | `MINUTES_UPDATE_FAILED`, 직전본 유지, 자동 재시도 없음(`extractor.py:240-262`) | `failed` 기록, 커서 유지 → 다음 배치에 재포함(`batch_service.py:265-314`) |
| 최종 사전 단계 | wav 전체 재STT + 화자 클러스터 + 음성 대조(0.45) + transcript 교체(`M/services/meeting_v2_finalize.py:145-273`) | 재전사로 원문 교체(`finalize_service.py:141-208`), 화자 실명 대조는 없음 |
| 최종 전체 발화 | **항상 교체된 전체를 다시 넣는다** `[HH:MM:SS]`(`extractor.py:322-333`) | **콜드 스타트에서만**(`finalize_service.py:241`) |
| 최종 절차 | Pass1 정정 → Pass2 처음부터 다시 쓰기(`prompt_seeds.py:736-754`) | 단일 합성, 정정 없음(`finalize.py:300-387`) |
| 보정 등급 | auto(기술 용어·고유명사 치환) / presumed(인명·숫자·금액·일정, 표에만) / 화자 라벨 불변(`prompt_seeds.py:738-746`) | 코드에 없음 |
| 보정 표 | `meeting_v2_minutes_term_correction(heard, corrected, grade)`(`M/models/meeting_v2.py:639-653`). 최종 후 auto 만 원문 치환(`extractor.py:684-707`) | 코드에 없음 |
| 2×2 분류 | 업데이트(decisions/tasks, 참조 필수) × 생성(issues/action_items)(`prompt_seeds.py:688-701`) | 해당 구조 없음. 할 일은 「`task_list` 로 이미 있는 업무를 조회해라」(`finalize.py:322`) |
| 화자 귀속 | 적극 배정 + 서버 가드 + 최종 1:1 confirm_gate(`prompt_seeds.py:855-879`, `extractor.py:1174-1180`) | 코드에 없음 |
| 최종 timeout | 900 제출 / 940 결과(`M/config.py:279`, `extractor.py:365`) | 90 × 최대 3시도 |
| 최종 재시도 | max_retries=0, 세션 오류일 때만 form_b 1회(`extractor.py:367-394`) | 3시도(backoff 없음), 세션 유실일 때만 콜드 스타트 |
| 최종 실패 | `FINAL_FAILED` + fallback, 진행 중 회의록 유지(`M/services/meeting_v2_finalize.py:309-315`) | 회의 `failed` + failure_reason(`mtg/application.py:952-960`) |
| 카탈로그 범위 | **서버 전량**: 회의·참석자·활성 제품(+대표 버전·리드)·열린 결정·미종결 Task·버전 담당·부서·구성원·전결표 발췌(`M/services/meeting_v2_catalog.py:288-321`, 각 조각 `:361-694`) | 코드에 없음(도구 조회 방식) |
| 카탈로그 상한 | decision/task limit 0 = 무제한(`M/config.py:253-254`). 실측 115KB 주석(`extractor.py:898`) | — |
| config | `meeting_v2_*` 18개(`M/config.py:224-331`): summary_timeout 240 · sentence_trigger 8 · batch_tool_call_limit 6 · catalog limit 0/0 · final_timeout 900 등 | timeout env 없음 |

---

## 6. SH-IMP-012 — 슬랙 방을 나간 뒤 분배

1. **멤버십과 재확인**
   - 방 `room_meta` 의 `verified_at` / `access_lost`(`B/platform/external_channels_sync_store.py:65`)로 안다. `set_room_access`(`:283-305`)가 쓴다: ok 면 verified_at, 아니면 access_lost + `paused`
   - verified_at 이 찍히는 곳은 (a) 방 추가 `add_rooms` → `describe()`(공개 채널 `is_member` 확인)(`B/modules/external_channels/application.py:389-424`, `B/platform/external_slack.py:321-322`)와 (b) 워커 `_verify_slack_room`(`B/modules/external_channels/sync.py:439-459`, `conversations.info` + `is_member`) 두 곳이다
   - **재확인은 워커 프로세스 실행마다 방당 1회**다: `_verified_this_run` 집합(`sync.py:220-221`, `:314-317`). 비우는 곳은 일시 장애 `discard`(`:450`) 하나이고, 주기·만료·이벤트 트리거는 없다. 인스턴스는 워커 시작 때 1개 만든다(`B/bootstrap/external_worker.py:65-72`)
   - 부수 경로: 백필·메우기 중 history/replies 가 `UpstreamRoomDenied` 면 paused(`sync.py:330-332`). 메우기는 시작 때와 재연결·이벤트 예외 뒤 `request_gap_fill()` 에서만 돈다(`sync.py:280-282`, `external_worker.py:172-174`, `external_slack.py:379-380`, `:397-400`). `request_gap_fill` 은 `_verified_this_run` 을 건드리지 않는다
   - **분배 판정**: `handle_slack_event` → `slack_fanout_targets(team, channel)`(`sync.py:227-259`, `:237`) → `room.verified and not room.access_lost`(`external_channels_sync_store.py:116-127`). 이벤트의 `authorizations`/`authed_users` 는 쓰지 않는다(grep 0)
2. **Socket Mode 이벤트**
   - 봉투: 전부 ack(`external_slack.py:388-389`) · `disconnect` → 재연결(`:391-393`) · `events_api` → on_event(`:394-396`), 나머지는 무시
   - 이벤트(`sync.py:229-258`): `tokens_revoked`·`app_uninstalled` → 연동 끊기(`:230-232`, `:261-276`) · `message`(channel 있음)만 처리. 하위 유형 `message_changed` 교체 / `message_deleted` 표지 / edit subtype 건너뜀 / 나머지 저장
   - **`member_left_channel`·`channel_left`·`member_joined_channel`·`group_left`·`channel_archive`·`channel_deleted`·`group_archive` 는 처리하지 않는다**(grep 0). 앱 매니페스트의 이벤트 구독 정의는 레포에 없다
3. **창은 실제로 있다.** A 가 공개 채널 C 를 나가도 이번 실행 동안 verified_at 이 남는다(재확인하지 않음, `sync.py:314-319`). C 를 고른 다른 연결 회원 B 의 토큰으로 이벤트가 오면 `(team, channel)` 만으로 A 의 방도 대상이 된다(`external_channels_sync_store.py:122-127`). 연결 회원이 A 혼자면 이벤트 자체가 오지 않는다(`sync.py:454` 주석)
   - **최대 길이는 시간 상수로 정해지지 않는다.** 닫히는 사건: 워커 재시작 · 재연결/예외 뒤 메우기에서 A 토큰의 history 가 거절됨(나간 공개 채널을 Slack 이 거절하는지는 코드로 알 수 없음) · 방 재추가
   - 주기 상수(`IDLE 5s`·`REQUEUE 60s`·`PURGE 3600s` `external_worker.py:38,42-43`, 캐시 TTL 90/600 `external_slack.py:82-83`)는 이 재확인과 무관하다

## 7. SH-IMP-013 ① — 카톡 이름 없는 방

- 이름은 메시지 수집 API 로 들어오지 않는다(`KakaoMessagesCommand` = room_id·messages·backfill_done, `extra=forbid`, `B/modules/external_channels/kakao_ingest.py:94-99`). 방을 고를 때 `POST /api/integrations/{id}/rooms`(`http.py:833`)의 `rooms[].name` 으로 들어온다(`application.py:133-147`)
- 저장: 새 방이면 `name = detail.name or external_id`(**비면 chatId 가 이름**), 재추가 때는 이름이 있을 때만 덮어쓴다(`application.py:407`, `:418-419`). 그 뒤 카톡 이름을 갱신하는 경로는 없다(handshake `:554-562`, status `kakao_ingest.py:306-307`). 컬럼은 `external_rooms.name String(300) NOT NULL default ""`, `member_count Integer NULL`(`persistence.py:2098-2099`)
- 목록 API
  - `GET /api/integrations/{id}/rooms`(`http.py:826`)는 `removed_at IS NULL` 만 건다(`B/platform/external_channels.py:76-83`, `application.py:366-369`, `:687-702`)
  - 메시지함 카드는 메시지가 없는 방만 뺀다(`B/modules/external_channels/inbox.py:526`), 제목은 `room.name`(`:537`)
  - **이름·0명·시스템방 숨김 규칙은 코드에 없다**
- 데스크톱(참고): `frontend/src-tauri/src/kakao/db.rs:193-233`
  - `NTChatRoom WHERE lastUpdatedAt > 0`, 오픈채팅 제외
  - 이름은 chatName → 1:1 상대/단체 멤버 조합 → `"(이름 없음)"`(`:221-229`)
  - member_count 는 `activeMembersCount` 그대로이고 0명 방을 거르지 않는다(`:203`, `:230`)
  - 프론트는 그대로 서버로 보낸다(`F/lib/shell.ts:283-296`, `F/features/settings/KakaoSection.tsx:70`)

## 8-pre. SH-IMP-008 · 015 · 010 — 서버 쪽 시작점

1. **참고 자료 `resource_type`**
   - 받는 값은 `Literal['task','work_request']` 둘이다(`B/modules/ax_execution/conversation_commands.py:18-23`, HTTP `http.py:206`, 라우트 `:1384-1393`). 해석기는 그 밖이면 `unsupported context resource type`(`B/platform/conversations.py:1002-1006`). summary 는 「업무: {title} ({state})」/「업무 요청: …」(`:1026-1052`)
   - 흐름: 접수 때 resolve(`B/modules/ax_execution/conversations.py:180-181`) → `conversation_context_references` 행(`persistence.py:735-746`, CHECK 없음) → 실행 직전 재resolve·stale 확인 → included 만(`conversations.py:297-334`)
   - 프롬프트 모양(`codex_cli.py:558-563`, `claude_cli.py:339-344`, `User message:` 앞)
     ```
     Context references authorized for this turn:
     - {resource_type}:{resource_id}: {summary}
     ```
   - **종류를 나열하는 자리 5곳**: `conversation_commands.py:20` · `platform/conversations.py:1002-1006` · `http.py:433-434`(`ConversationContextReferenceRequest`, 정의만 있고 사용처 없음) · `F/lib/viewModels.ts:1030-1031` · `tool_catalog.py:54`(설명 문구)
2. **방 메시지 조회**
   - 최신 페이지부터 시작하고 `next_cursor` 는 **과거 방향만** 있다(`B/entrypoints/http_inbox.py:180-191`, `inbox.py:606-646`). 커서는 `(sent_at,id)` base64 JSON(`inbox.py:384-396`), 기본 50 / 최대 200(`:57`, `:611`)
   - 쿼리: `room_id=? AND [top-level|thread] AND (sent_at<at OR (sent_at=at AND id<marker)) ORDER BY sent_at DESC, id DESC`(`B/platform/external_channels_inbox_store.py:210-221`, `:36-48`)
   - 인덱스(`persistence.py:2123-2129`): `uq_external_messages_dedup(integration_id,container_key,external_key)` · `ix_external_messages_integration_sent_at` · `ix_external_messages_room_sent_at(room_id,sent_at)` · `ix_external_messages_room_thread(room_id,thread_key)`
   - 「기준 위아래」: `(room_id,sent_at)` 인덱스로 양방향 범위 탐색은 가능하다(동률을 가르는 id 는 인덱스 밖). API·저장소에는 before 방향만 있고 after/around 는 코드에 없다(`inbox.py:131`). 기준 메시지는 `message_by_id`(`external_channels_inbox_store.py:78-79`)나 `message_in_room(room_id, external_key)`(`:223-224`)로 찾는다
   - 메일 한 통: `GET /api/inbox/mail/{id}`(`http_inbox.py:170-178`) → `B/bootstrap/external_inbox.py:156` → `InboxApplication.mail`(`inbox.py:556-580`) → `mail_for`(`external_channels_inbox_store.py:81-93`)
3. **`/api/inbox/stream` 사건**: 접속 직후 `{"type":"ready"}`(`http_inbox.py:336`) + `UserEventType` 3종(`B/modules/external_channels/events.py:30-36`). 전달은 NOTIFY `ax_user_events` → `UserEventHub` → 회원별 큐(상한 200, 넘치면 오래된 것부터 버림)(`B/platform/user_events.py:12-16`, `B/platform/user_event_hub.py:21,59-98`)

| 사건 | 내는 자리 |
|---|---|
| `inbox.message_arrived` | `external_channels_sync_store.py:207-214`(live·20건 이하 건별), `:238-243`(수정·삭제), `kakao_ingest.py:254-265` |
| `inbox.reply_result` | `inbox.py:921-938` |
| `integration.changed` | `external_channels_sync_store.py:215-220`(백필·큰 메우기), `:351-357`(상태), `application.py:333-337`(OAuth), `:649-653`, `kakao_ingest.py:319-325`, `inbox.py:1046-1059` |

| 연동 숫자를 바꾸는 자리 | 바뀌는 값 | 사건 |
|---|---|---|
| `save_messages` `sync_store.py:188-200` | synced_count·last_synced_at·backfill_count | 있음(count>0) |
| `ingest_messages` `kakao_ingest.py:241-248` | synced_count·last_synced_at | 있음(accepted>0) |
| `kakao_ingest.py:250-253` | backfill_done_at·live | 있음(`:266-267`) |
| `update_integration` `sync_store.py:247-263` | backfill_cursor·sync_cursor·backfill_done_at 등 | **status 가 바뀔 때만**. 커서만 바뀌면 없음 |
| `update_room` `:265-281` | backfill_cursor·name·member_count·room_meta | status 가 바뀔 때만 |
| `set_room_access` `:283-305` | verified/access_lost/status | status 가 바뀔 때만 |
| `mark_disconnected` `:337-349` | disconnected | 있음 |
| add/remove room·disconnect·handshake·reset | 구성·상태 | 있음(`application.py:358,431,478,547,553,580`) |
| `report_status` `kakao_ingest.py:304-310` | collector_status·display_name | 바뀐 보고일 때만 |
| 읽음 `inbox.py:654`, `:662` | 읽음 | 없음 |

설정 화면은 `integration.changed` 를 받으면 다시 읽는다(`F/features/settings/SettingsPage.tsx:184`).

## 8-test. 공통 — 계약 테스트·journey 위치

- **acceptance journey 는 이 경로들 어디에도 없다**(`grep -rliE journey` → 무관한 docs·graph 테스트뿐. `T/legacy_acceptance.py` 에도 task_create_self·meeting_create 0건)

| 항목 | 테스트 |
|---|---|
| 업무 생성 프롬프트 | `T/unit/test_ax_work_lookup_policy.py`(:10 프로젝트·연관 업무 조회, :35, :93 최대 3건, :189 호출 상한, :56 Claude 동일), `T/contract/test_codex_cli.py:169`(:308 meeting_create 문구) |
| Action 카드·확정 | `T/contract/test_action_center.py`(:442, :860, :1091, :1713, :163), `T/contract/test_task_creation_contract.py`(:519, :558), `T/unit/test_action_policy.py`, `test_task_creation_input.py`·`test_task_predecessors.py`·`test_task_references.py`·`test_initial_checklist.py` |
| 첨부 초안 | `T/contract/test_action_material_drafts.py`(:59 외 3), `test_browser_interactions.py`(:193, :243) |
| 회의 생성·수정 | `T/contract/test_meeting_creation_input.py`(:63, :92), `test_unified_commands.py`(:36, :110), `test_mcp.py`, `test_mcp_command_result.py`, `test_meeting_core.py`(:281, :301) |
| Connect | `T/contract/test_meeting_rooms.py`(FakeRoomGateway :51-111 — 방 2번 4인·3번 6인·5번 12인, 실제 어댑터 전송 실패 :114 :134, 수정 동기화 :899 :919 :957-1112, 취소 :927 :944), `T/integration/postgres/test_postgres_integration.py:2356`. 녹화 fixture 없음 |
| 겹침 | `T/contract/test_meeting_time_overlap.py`(:221-338), `T/integration/postgres/test_meeting_time_overlap_postgres.py` |
| 안건 출처 | `T/contract/test_meeting_core.py:375-393`·`:630-647` — **현재 동작(전부 carried)을 고정**한다. `test_meeting_finalize.py:924-960`, `T/unit/test_meeting_domain.py:88`. 프론트 `MeetingList.test.tsx:254-277`(불러오기 안건만, 시간·payload 는 검사하지 않음), `MeetingAfter.test.tsx:222-243`·`:458-475`. `BookingModal.test` 는 없음 |
| 회의록 파이프라인 | `T/contract/test_meeting_memo_batch.py`(:374, :392, :421, :478, :523, :644), `T/unit/test_meeting_finalize_service.py`(:118, :128, :137-189, :199), `T/contract/test_meeting_finalize.py`(:279, :299, :972 근거 없는 줄, :1486, :1509, :1659), `T/unit/test_meeting_domain.py`(:162 기한, 정상 케이스만), `test_codex_cli.py`·`test_claude_cli.py`·`test_worker_resilience.py`. **provider timeout 이 배치·합성을 실패시키는 테스트는 없음** |
| 슬랙 | `T/contract/test_external_sync.py`(:170 분배, :372, :410 접근 상실→다음 실행 복구, :239, :484, :559). 나간 직후 같은 실행 안의 분배는 검증하지 않음 |
| 카톡 | `T/contract/test_kakao_ingest_and_profile.py`(:67, :91, :164, :184), `test_external_channels.py:251`·`:360`, 프론트 `F/lib/shellKakao.test.ts` |
| 메시지함·스트림·맥락 | `T/contract/test_external_inbox.py`(:241, :266, :317, :537, :557, :653), `T/integration/postgres/test_external_channels_postgres.py:44`, `T/contract/test_product_operations.py:580`(맥락 참조), 프론트 `InboxPage.test.tsx`·`SettingsPage.test.tsx`·`useConversations.test.tsx` |

---

## 9. grep 개수표 (줄 수 / 파일 수)

범위: 따로 적지 않으면 `backend` + `frontend/src`(node_modules·.git·dist 제외)

| 항목 | 심볼 | 개수 |
|---|---|---|
| 001·017 | `project_list` | 12 / 8 (src 5/5) |
| | `list_projects` | 25 / 11 (src 16/6) |
| | `\btask_list\b` | 71 / 27 (src 21/8) |
| | `task\.create_self` | 119 / 35 (src 44/16) |
| | `ax\.task\.create_self` | 25 / 9 |
| | `task_create_self` | 40 / 18 |
| | `material_search` | 61 / 20 (src 26/9) |
| | `action_material_link_stage` | 4 / 3 |
| | `create_current_meeting` | 3 / 2 |
| | `\bmeeting_create\b` | 16 / 9 |
| | `meeting\.reservation\.create` | 42 / 18 |
| | `action-meeting-card` | 4 / 2 |
| 016 | `\bmeeting_update\b` | 8 / 4 |
| | `update_current_meeting` | 6 / 2 |
| | `meeting\.info\.update` | 14 / 5 |
| 003 | `the_connect\b` | 4 / 3 |
| | `TheConnectGateway` | 6 / 3 |
| | `TDL_` | 6 / 1 |
| | `room_booking` | 24 / 3 |
| | `room_gateway` | 23 / 3 |
| | `room_reservation` | 53 / 17 |
| | `/api/reservations` | 6 / 1 |
| | `meeting_room_creation_attempts` | 2 / 2 |
| | `MeetingRoomCreationAttemptRecord` | 52 / 5 |
| | `meeting_room_list` | 2 / 2 |
| | `MEETING_TIME_OVERLAP` / `MeetingTimeOverlap` | 1 / 1 · 5 / 3 |
| | `location`(modules/meetings 안) | 16 / 2 |
| 005 | `carried_from_meeting_id` | 46 / 20 |
| | `"carried"` | 12 / 9 |
| | 「지난 회의에서 넘어옴」 | 2 / 2 |
| | 「이전 회의 정보 불러오기」 | 0 / 0 |
| | `concluded` | 82 / 26 |
| 006 | `timeout_seconds` | 78 / 27 (레포 전체) |
| | `AX_MEETING_AI_TOOLS` | 3 / 2 |
| | `_bind_evidence` | 2 / 1 |
| | `resolve_due` | 6 / 2 |
| | `next_meeting_starts_on` | 15 / 5 |
| | `build_final_prompt` | 5 / 3 |
| | `correction_kind` | 1 / 1 |
| 012 | `member_left_channel`·`channel_left`·`member_joined_channel`·`group_left` | 0 / 0 |
| | `_verified_this_run` | 4 / 1 |
| | `_verify_slack_room` | 2 / 1 |
| | `slack_fanout_targets` | 3 / 2 |
| | `set_room_access` | 6 / 2 |
| | `access_lost` | 9 / 4 |
| | `request_gap_fill` | 2 / 2 |
| 013 | `(이름 없음)` | 3 / 1 (src-tauri 포함) |
| 008·015 | `resource_type` | 371 / 65 (다른 용도 포함) |
| | `ConversationContextReferenceInput` | 15 / 4 |
| | `conversation_context_references` | 1 / 1 |
| 010 | `inbox.message_arrived` / `inbox.reply_result` / `integration.changed` | 9/8 · 11/8 · 7/6 |
| | `INTEGRATION_CHANGED` | 7 / 5 |

---

## 10. 코디 확인 필요 (운영 DB·로그)

1. **SH-IMP-006 기한 10/06 의 출처** — 10-07 회의 「주간 제품·개발 진행 및 병원 AX 확장 회의」 의 다음 회의 후보
   ```sql
   -- 대상 회의
   SELECT id, owner_id, organization_id, starts_at, starts_at AT TIME ZONE 'Asia/Seoul' AS kst, status, carried_from_meeting_id
   FROM meetings WHERE title LIKE '주간 제품·개발 진행%' AND starts_at::date BETWEEN '2026-10-06' AND '2026-10-08';
   -- 경로 (a) 이월 회의
   SELECT id, title, starts_at AT TIME ZONE 'Asia/Seoul', status FROM meetings WHERE carried_from_meeting_id = :id ORDER BY starts_at;
   -- 경로 (b)(c) 같은 owner 의 다음 예약
   SELECT id, title, starts_at, starts_at AT TIME ZONE 'Asia/Seoul', status FROM meetings
   WHERE organization_id = :org AND owner_id = :owner AND starts_at > :starts_at AND status = 'scheduled' ORDER BY starts_at LIMIT 3;
   SHOW TimeZone;  -- DB 세션 타임존 (경로 (c))
   ```
   여기서 기한 10/06 을 설명하는 후보가 없다면 경로 (d), 즉 AI 의 `due_candidate` 다. 그 회의 할 일 행의 기한과 원래 발화를 대조해야 한다
2. **SH-IMP-006 참석 1명** — 그 회의가 quick_start 인지 확인한다
   ```sql
   SELECT count(*) FILTER (WHERE removed_at IS NULL) FROM meeting_attendees WHERE meeting_id = :id;
   SELECT count(DISTINCT speaker_label) FROM meeting_transcripts WHERE meeting_id = :id;  -- 표 `persistence.py:483-492`
   ```
3. **SH-IMP-006 누락** — 같은 회의의 `meeting_batch_runs`(status·from_seq·to_seq·reason)와 최종 합성이 resume 인지 콜드인지(worker-meeting 로그 / `session_ref` 존재 여부)를 본다. 회의 첫머리 00:05~01:07 구간이 실패 배치 구간이었는지도 확인한다
   ```sql
   SELECT seq, status, trigger_cause, from_seq, to_seq, reason, created_at FROM meeting_batch_runs WHERE meeting_id = :id ORDER BY seq;
   ```
4. **SH-IMP-006 timeout 회의**(`3abe9f9b-…`): 3번의 시도가 모두 timeout 이었는지, 각 시도가 90s 였는지, 워커 재배달 횟수(로그)
5. **SH-IMP-003** — 「4인실 없음」 답변 턴에서 `meeting_room_list` 를 불렀는지와 그 응답(conversation 이벤트·tool receipt 로그). 운영 `TDL_*` env 설정 여부, `TDL_NOTIFY` 값
6. **SH-IMP-012** — 운영 worker-external 의 마지막 재시작 시각(= 재확인 시점). 같은 워크스페이스·같은 채널을 고른 회원 수
   ```sql
   SELECT r.external_id, count(*) FROM external_rooms r JOIN external_integrations i ON i.id = r.integration_id
   WHERE i.kind = 'slack' AND r.removed_at IS NULL GROUP BY r.external_id HAVING count(*) > 1;
   ```
7. **SH-IMP-013** — 이름 없는 방 8개의 실제 저장값(`""` 인지, chatId 인지, `"(이름 없음)"` 인지)과 member_count
   ```sql
   SELECT r.id, r.name, r.external_id, r.member_count FROM external_rooms r JOIN external_integrations i ON i.id = r.integration_id
   WHERE i.kind = 'kakao' AND r.removed_at IS NULL AND (r.name = '' OR r.name = r.external_id OR r.name = '(이름 없음)' OR coalesce(r.member_count,0) = 0);
   ```

## 11. 조사 한계

- 테스트·서버를 돌리지 않았다. 동작은 코드를 읽어서만 판단했다
- 조사는 하위 탐색 에이전트 6개로 나눠 진행했다. 핵심 줄 일부(`mtg/application.py:410-415`, `boot/application.py:1385-1399`, `the_connect.py:118-137`, `meetings.py:786-803`, `finalize.py:203-212`, `finalize_service.py:241`, `codex_cli.py:95`·`:425-477`, `sync.py:310-320`, `external_channels_sync_store.py:116-127`, `mcp.py:822-828`, `graph.py:34-35`, `confirmation.py:38-40`)는 직접 다시 열어 확인했다. 나머지 줄 번호는 에이전트가 확인한 값이다
- Codex CLI 가 timeout 으로 죽은 turn 이 세션 rollout 에 남는지(실패 배치 구간이 세션 기억에 들어가는지)는 CLI 내부 동작이라 코드로 판단할 수 없다
- DB 가 `timestamptz` 를 UTC 로 돌려주는지(기한 경로 (c))는 운영 DB 세션 TimeZone 에 달려 있고, 코드에는 설정이 없다
- 나간 공개 채널의 `conversations.history` 를 Slack 이 거절하는지, The Connect 가 문서상 제공하는 다른 API(전용 가용 조회 등)가 있는지는 외부 시스템 동작이라 코드 밖이다. 코드에 없는 Connect 기능은 「코드에 없음」 으로만 적었다
- 운영 대화에서 모델이 실제로 어떤 도구를 몇 번 불렀는지(프롬프트 상한을 지키는지)는 로그로만 알 수 있다
- 프론트 쪽은 서버 계약을 설명하는 데 필요한 만큼만 읽었다. UI 전수는 frontend 리포트 몫이다
- §4 는 번호를 맞추려고 비워 둔 절이다. §8-pre(008·015·010)와 §8-test(공통)는 형식의 「N. grep 개수표」 앞에 오도록 붙인 번호다
