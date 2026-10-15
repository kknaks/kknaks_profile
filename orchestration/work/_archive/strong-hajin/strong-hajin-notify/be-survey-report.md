# 알림 조사 (backend)

- 대상: `Strong_hajin/strong-hajin-notify` 워크트리, base `origin/main` `d2a06fa` — **읽기 전용**(코드·테스트 무변경, 테스트·서버 미실행)
- 경로 약어: 아래 `src/` = `backend/src/ax_workspace/`. `tests/` = `backend/tests/`. `docs/` = 코드 레포 `docs/`
  - **WT** = `src/platform/work_tasks.py` · **APP** = `src/modules/work/application.py` · **REQ** = `src/modules/work/requests.py`
  - **ASG** = `src/modules/work/assignments.py` · **BA** = `src/bootstrap/application.py` · **AC** = `src/platform/action_center.py` · **ACT** = `src/platform/actions.py`
  - **HTTP** = `src/entrypoints/http.py` · **HIN** = `src/entrypoints/http_inbox.py` · **SYNC** = `src/modules/external_channels/sync.py` · **SS** = `src/platform/external_channels_sync_store.py` · **IS** = `src/platform/external_channels_inbox_store.py` · **INB** = `src/modules/external_channels/inbox.py`
- 사람은 「팀원 A」 식으로만 적는다(테스트 픽스처의 persona id 도 옮기지 않았다).

---

## 0. 한 줄 요약

- **A. 지금 있는 알림** — `notifications` 표 하나 + 생성 자리 **단 1곳**(WT:2116, 업무 요청 「발송→받는 사람」·「수락→요청자」 두 종류)이고, 읽기는 `GET /api/notifications`(페이지·안읽음 수·전체 읽음 없음) + 단건 읽음뿐이며, **프론트는 이 API를 어디서도 부르지 않는다**. 수신함(InboxRail)은 `work_requests` 원천이라 알림과 **다른 원천**이다.
- **B. 관련된 사람 재료** — 업무·요청 사건 40여 종 모두 요청자·담당자·CC·결재자·제안자 등 관련자 필드를 안다. 하지만 알림을 내는 것은 2종뿐이다. 메일·슬랙·카톡 메시지는 「연동 소유자(`external_integrations.member_id`)」 한 사람에게 쌓인다. 「나를 멘션」·「내가 보낸 것」·「나에게 온 To/CC」 **칸은 없고** raw 에만 있다. 시각 기반(기한 하루 전·일일 요약)을 돌릴 **스케줄러는 없다**.
- **C. 실시간 전달** — 서버→브라우저는 WebSocket 2개뿐이다. `/api/inbox/stream` 은 회원별·Postgres `LISTEN/NOTIFY ax_user_events`, `/api/meetings/{id}/stream` 은 회의별·API 프로세스 메모리. 사건 종류는 메시지함·연동 4종뿐이고 **알림·업무 사건은 스트림에 없다**. 재연결 커서·last-event-id 도 **없다**. 게시자는 API·external_worker 둘뿐이다.
- **D. 설정** — 사용자별 설정 표는 `assistant_character_preferences`(캐릭터 하나) 뿐이고 `members` 에 JSON·선호 칸이 없다. 「나에게 보내기」 수단으로는 메일 답장(`to` 임의 지정 가능, 단 기존 메일에 대한 답장으로만)과 슬랙 답장(이미 고른 방에만)이 있다.

---

## 1. A. 지금 있는 알림

### A-1. `modules/notifications.py` · `platform/notifications.py` 가 무엇인가

**표 — `notifications`**
- 마이그레이션 파일은 **없다.** `migrations/manual/` 의 7개 SQL(w2-indexes·w7-successor-index·external-channels·inbox-message-origin) 중 `notifications` 를 담은 것은 0개(`grep -rln notifications migrations` → 0)
- 스키마는 ORM `Base.metadata.create_all` 이 만든다(`src/bootstrap/reset.py:20`) · 안전 추가는 `src/bootstrap/schema_sync.py:27`
- 모델은 `NotificationRecord` — `src/platform/persistence.py:1299-1321`
- `make local-stack` preflight 가 이 표의 존재를 확인한다(`Makefile:332-333`, 그것을 지키는 시험 `tests/architecture/test_local_stack_targets.py:32-33`)

| 컬럼 | 형 | 줄 |
|---|---|---|
| `id` | UUID PK | persistence.py:1308 |
| `recipient_member_id` | FK members.id, not null | :1309 |
| `source_kind` | String(60) | :1310 |
| `source_id` | String(100) | :1311 |
| `kind` | String(80) | :1312 |
| `resource_type` | String(40) | :1313 |
| `resource_id` | String(100) | :1314 |
| `resource_version` | int null | :1315 |
| `resource_title` | String(300) | :1316 |
| `actor_member_id` | FK members.id | :1317 |
| `safe_summary` | String(300) | :1318 |
| `created_at` | tz datetime | :1319 |
| `read_at` | tz datetime null | :1320 |

- 제약: `UNIQUE(recipient_member_id, source_kind, source_id)` `uq_notification_recipient_source` (:1304), 인덱스 `(recipient_member_id, created_at)` (:1305)
- docstring: 「한 정본 도메인 사건의 수신자 투영. 내용은 읽을 때마다 다시 인가한다」(:1300)

**kind 값 전부 — 2개** (WT:2120)
- `work_request.received` — `work_request.created` 감사 사건에서 나온다
- `work_request.accepted`
- `source_kind` 값은 `work_request_audit_event` 하나(WT:2118)이고, `resource_type` 으로 쓰는 값도 `work_request` 하나(WT:2121)

**수신자 결정** — WT:2109 `recipient = request.assignee_id if created else request.requester_id`
- 발송 → 받는 사람(담당자), 수락 → 요청자
- CC·결재자·회의 승격자(`promoted_by_member_id`)는 받지 않는다(그 자리의 코드에 없다)

**생성 멱등** — `SqlAlchemyNotificationRepository.emit`(`src/platform/notifications.py:18-57`)은 같은 (수신자, source_kind, source_id) 가 있으면 기존 행을 돌려준다(:33-41). `safe_summary` 는 300자에서 자른다(:52).

**읽기 인가 — 알림이 권한을 넘겨주지 않는다**
- `NotificationApplication._authorized_view`(`src/modules/notifications.py:73-83`)가 행마다 원래 자원을 다시 읽는다
  - `meeting` 이면 `MeetingApplication.get`
  - `work_request` 이면 `WorkRequestApplication.get`
  - **그 밖의 resource_type 은 `None` 이 되어 목록에서 조용히 빠진다**(:79-80)
- 읽을 수 없게 된 자원(`ResourceNotFound`·`WorkRequestAccessDenied`)도 빠진다(:81-82)
- 제목·회차는 저장된 `resource_title` 이 아니라 **지금 자원의 값**으로 낸다(:83)

**관찰 1 — 회의 갈래의 모양 어긋남**
- `modules/notifications.py:76-83` 은 `self._meetings.get(...)` 결과에서 `resource['title']`·`resource['version']` 을 꺼낸다
- 그런데 `MeetingApplication.get`(`src/modules/meetings/application.py:296-298`)이 돌려주는 `_detail` 은 `{"meeting": {...}}` 모양이다(:1823-1824)
- 같은 일을 하는 `BA:2473-2492` `_authorized_notification_view` 는 `["meeting"]` 을 풀어 읽지만, 이 함수는 **정의만 있고 호출부가 0곳**이다(`grep -rn _authorized_notification_view` → 정의 1줄)
- 지금은 meeting 알림 행을 쓰는 자리가 없어 닿지 않는 갈래다(아래 A-2)

**읽음 처리**
- `mark_read` 는 `read_at` 이 비어 있을 때만 지금 시각을 찍는다(`platform/notifications.py:77-80`) — 멱등
- `for_recipient(lock=True)` 로 `FOR UPDATE` 잠금을 건다(:68-75)
- 수신자가 아니거나 원래 자원을 못 읽으면 `NotificationNotFound`(modules/notifications.py:64-69), HTTP 404 로 바뀐다(HTTP:528-529)

**조립** — `BA:2460-2471`(`_notifications` · `list_notifications` · `mark_notification_read`)

### A-2. 알림을 만드는 자리 전부

`grep -rnE '\.emit\(' src --include='*.py'` → **1곳**. `SqlAlchemyNotificationRepository` 참조는 5곳(import 2 · 생성 1 · BA 조립 2)이다.

| 파일:줄 | 사건 | 누구에게 | 실제로 부르는 곳 |
|---|---|---|---|
| WT:2116 (`append_audit` WT:2096-2128 안, 조건 WT:2106) | `work_request.created` → kind `work_request.received` | `request.assignee_id` | REQ:452 (`WorkRequestApplication.create` 끝) |
| WT:2116 (같은 자리) | `work_request.accepted` → kind 그대로 | `request.requester_id` | REQ:506 (`accept`) |

- `append_audit(` 호출은 37곳이다. 그중 업무 요청 쪽 11종(아래 B-1 「감사 표」)만 이 훅을 지나고, 그 11종 중 **2종만** 알림을 만든다(WT:2106)
- 회의 쪽 `append_audit`(`src/platform/meetings.py:356`)는 다른 저장소의 다른 메서드라 알림을 만들지 않는다
- 브리프가 출발점으로 준 파일들은 **알림을 만들지 않는다.** 읽기나 읽음 명령만 있다
  - `actions.py` — 읽음 확인 실행 ACT:832-834, 미리보기 ACT:1703-1707
  - `external_pubsub.py:35` — `GmailNotification` 은 Gmail Pub/Sub 메시지 타입이고 우리 알림과 무관하다
  - `mcp.py` — :622-627(읽음 제안·실행) · :1348-1349 · :1607-1608 · :1929-1930
  - `tool_catalog.py` — :57 `notification_mark_read`(확인 필요) · :231-234 `list_notifications`
  - `work/application.py` — 「알림의 자리」 표시 2곳만 있다(A-2 끝)
- 시드·데모·시나리오(`bootstrap/seed.py`·`demo_work.py`·`scenario.py`·`scenario_csv.py`·`reset.py`)에도 `NotificationRecord`·`emit` 쓰기가 없다
  - `resource_type="meeting"` 히트 11곳은 전부 `ResourceRelationshipRecord`·읽기 분기다(예: `src/platform/meetings.py:313`)
- 회의 공유는 알림을 내지 않는다고 MCP 도구 설명에 못박혀 있다(`src/modules/ax_execution/tool_catalog.py:446`)
- 예전 회의 공유 알림 시험은 걷어 냈다(`tests/contract/test_notifications.py:3-5`)
- 문서 쪽에도 경계가 있다
  - `docs/unified-operations.md:57` — 「D10의 새 작업 완료 알림은 만들지 않음」
  - `:85` — 「완료 알림함/푸시 … 추가하지 않는다」
  - `:113` — 「알림은 추가하지 않는다」

**「알림의 자리」 표시(의도적으로 부르지 않음) — 2곳**
- APP:741-744 — 상위·프로젝트 이동 때 자손 담당자가 모른다
- APP:1581-1585 — 선행 해제 때 후행 B 담당자의 시작 게이트가 열리는데 모른다
- 둘 다 SPEC-007 §5 · D-20 을 인용한다
- 「부르지 않는다」를 시험이 지킨다: `tests/contract/test_task_successors.py:495-515`(`emit` 를 세어 0 을 기대)

**관찰 2 — 수락 경로**
- v2 발송은 업무를 곧바로 세우지만(REQ:453-470) 요청 행은 `state="pending"` 으로 서고(WT:1422) 수락 판단 항목을 연다(WT:1465 `_open_request_acceptance`)
- 담당 행이 `pending` 이면 수락이 그것을 확정한다(WT:1885-1915). 그래서 수락 알림 경로는 v2 에서도 살아 있다
- 다만 계약 시험은 수락 알림을 **옛 행 모양**으로 되돌린 뒤 검증한다
  - `tests/contract/test_notifications.py:55` `make_request_look_pending` · `tests/legacy_acceptance.py:55-70`
  - 시험 docstring: 「수락 알림은 과거 행의 판단에만 붙는다」(:44)
- v2 발송 행에 수락했을 때 알림이 서는지를 직접 보는 시험은 찾지 못했다(조사 한계)

### A-3. 알림을 읽는 API 전부

**HTTP**
- `GET /api/notifications` — HTTP:1381-1383
  - 인증 `developer_principal`
  - 응답: `NotificationView` 의 **배열 전체**. 필드는 `notification_id` · `kind` · `summary` · `actor_id` · `resource{type,id,version,title}` · `created_at` · `read_at`(`modules/notifications.py:30-37`, 조립 :46-53)
  - **페이지·limit·커서 없음**. 저장소는 수신자의 행 전부를 `created_at desc, id desc` 로 읽는다(`platform/notifications.py:59-66`)
  - **안읽음 수·안읽음만 필터 없음**
- `POST /api/notifications/{notification_id}/read` — HTTP:1385-1392
  - 단건 읽음이고 응답은 그 `NotificationView`. 404 매핑은 HTTP:528
- **전체 읽음 엔드포인트는 없다**(HTTP·MCP 모두 `mark_all`·`read-all` 알림판 없음)
  - 메시지함의 `POST /api/inbox/read-all`(HIN:216-240 범위)은 외부 메시지 읽음이고 `notifications` 와 무관하다

**MCP · AX**
- `list_notifications` — mcp.py:1348-1349 · :1607-1608
- `notification_mark_read` — mcp.py:1929-1930
  - 채팅 위임 실행이면 ActionItem 제안 `notification.mark_read` 를 거쳐 사람 확인이 필요하다(mcp.py:162 `ACTION_DECIDE`, :622-627, `tool_catalog.py:57` `requires_confirmation=True`)
- 실행: ACT:832-834. 명령 계약: `src/modules/ax_execution/command_contracts.py:120`

**인벤토리** — `docs/unified-operations-inventory.json`
- :650-666 `GET /api/notifications`
- :1860-1879 `POST …/read`
- :8450-8572 MCP `list_notifications`

**BASE-001 PA-06 의 `http.py:1046,1050` 재확인 — 줄이 흘렀다.** 지금 HTTP:1046·1050 은 `POST /api/meetings/{meeting_id}/finalize`(회의 합성 다시 시도) 본문이다. 알림 라우트는 **HTTP:1381(목록)·1385(읽음)** 에 있다.

**프론트 소비** — `frontend/src/lib/api.ts:726-732` 에 `getNotifications` · `markNotificationRead` 가 정의돼 있다. 하지만 `frontend/src` 전체에서 이 둘을 부르는 곳은 **0곳**이다(정의 줄만 나온다). 지금 화면에 알림 목록이 없다(프론트 상세는 frontend 리포트 몫).

### A-4. 수신함(InboxRail · 「참고」)과 알림 — **다른 원천**

**수신함(InboxRail)** — 원천은 `GET /api/work-requests/inbox`(HTTP:2292-2298) → `BA:4769-4771` → `REQ:1210-1237 inbox()`
- 표는 `work_requests` + CC 관계(`resource_relationships`) + 읽음 `work_request_read_receipts`(`persistence.py:1747`, WT:2255 `mark_read`, WT:2282 `read_request_ids`)
- 카테고리는 둘이다
  - `work` — 내가 담당자이고 요청이 pending·negotiating
  - `reference` — 내가 CC 이고 아직 안 읽음(REQ:1233-1236)
- 「참고」 읽음은 `POST /api/work-requests/{id}/read`(HTTP:2330-2341) → `REQ:1239` `mark_reference_read`
- 프론트 주석도 「업무 요청과 CC 요청만 담는다. TaskReference와 AX 판단 항목은 이 목록의 원천이 아니다」라고 적는다(`frontend/src/shell/InboxRail.tsx:15`)

**알림** — 원천은 `notifications` 표다.

**같은 사건이 두 곳에 들어가나**
- **업무 요청 발송**은 두 곳에 다 들어간다
  - 받는 사람의 수신함 `work` 카드는 그 요청 행 자체다
  - 받는 사람의 `notifications` 행 `work_request.received` 도 생긴다(WT:2116)
  - 둘의 읽음은 따로 움직인다. 수신함 `work` 갈래에는 읽음이 없고 수락·거절로 접힌다(REQ:1213-1215). 알림은 `read_at` 으로 접힌다
- **CC 참고**는 수신함에만 있다. CC 는 알림 수신자가 아니다(WT:2109)
- **수락**은 알림에만 있다. 요청자의 수신함에는 서지 않는다(REQ:1233-1236 조건)
- 외부 메시지함(`/api/inbox/*`, `external_*` 표)은 이 둘과 또 다른 원천이다(HIN:180-338, HTTP:2798 등록)
- 판단함(ActionItem·DecisionItem, AC)도 별개의 「끌어오는」 표면이다
  - 수락 판단 WT:1501 · 담당 수락 WT:2459 · 완료 확인 WT:780 `open_delivery_round`
  - `docs/domain-model.md:194-200` 이 「알림은 판단이 아니다 … `activity_events` 위의 파생 projection, 대상자는 `resource_relationships` 에서 파생」을 **결정됨·아직 구현하지 않음**으로 적어 두었다. 지금 구현(감사 훅에서 직접 행 쓰기)은 그 모양이 아니다

---

## 2. B. 「나와 관련된」 을 정할 재료

### B-1. 업무

**저장된 사건 어휘**
- `activity_events`(`persistence.py:1276`, `ActivityLedger.record` WT:264-299)
- `work_request_audit_events`(`persistence.py:1789`, WT:2096)
- `task_versions`(`persistence.py:1644`, WT:995)
- 쓰기 호출을 손으로 짚어 센 결과
  - 업무 원장 `task.*` **33종**
  - 요청 원장 `work_request.*` **10종**
  - 요청 감사 `event_type` **11종**(REQ:452·506·531·559·604·680·691·723·862·954·989)
- `work_request.cancelled_by_agreement`·`work_request.list_entry_removed` 는 원장에만 있다. 감사 표에 없으므로 알림 훅에 닿지 않는다

**상태 기계(SPEC-003 §4 State) ↔ 코드**
- 수행 상태는 `open`·`in_progress`·`done`·`cancelled`
- 전이 실행은 APP:2037-2118(`task.state_changed` 기록 APP:2110). HTTP 는 :2763/2773/2777/2781/2786
- 재개는 APP:2140-2181
- 완료 승인·보완 요청은 APP:1933-1964(AC:1483-1494 경유)

**관련자 필드(공통)**
- 요청 행: `requester_id` · `assignee_id` · `promoted_by_member_id` · `approver_id` · CC(`cc_member_ids`)
  - 접근 투영: `ResourceRelationship` requester/assignee/cc(WT:1447-1456)
  - 재구성: WT:2140-2150 `rebuild_relationships`
- 업무 행: 활성 담당(`task_assignments`), `approver_id`(APP:589), `source_work_request_id` → 요청자(APP:2031-2035 `_requester_of`)
- 업무 CC: `ResourceRelationship kind=cc, resource_type=task`(WT:1262-1282)
- 댓글 독자: `party_of` — 요청자·승격자·담당자·CC(REQ:1183-1197). **결재자는 포함하지 않는다**

| 사건(원장/감사 이름) | 실행 자리 | 행위자 | 코드가 아는 영향 받는 사람 | 알림 | 스트림 |
|---|---|---|---|---|---|
| 내 업무 생성 `task.created` | WT:371-438 · APP:275 · HTTP:1586 | 본인 | 본인 · `approver_id`(WT:410) · 업무 CC(WT:434) | ✗ | ✗ |
| **요청 발송** `work_request.created` | REQ:334-484 · WT:1368 · HTTP:2254 | 요청자 / 회의 승격자(REQ:446) | 받는 사람 `assignee_id` · 요청자 · CC · 결재자(REQ:437) | **✅ 받는 사람** | ✗ |
| 요청 발송이 세운 업무 `task.created` | WT:1981-2085 | 같음 | 같음 | ✗ | ✗ |
| 발송 시 프로젝트 자동 합류 | REQ:475-483 | 같음 | 받는 사람 | ✗ | ✗ |
| **요청 수락** `work_request.accept`/`accepted` · `task.request_accepted` | REQ:486-507 · WT:1885 · HTTP:2645 · AC:260 | 받는 사람 | 요청자 | **✅ 요청자** | ✗ |
| 요청 거절 `work_request.rejected` + 업무 취소 | REQ:509-532 · WT:1946-1976 · HTTP:2658 | 받는 사람 | 요청자 · 사유 | ✗ | ✗ |
| 협의 `work_request.negotiated` | REQ:534-562 · HTTP:2671 | 받는 사람 | 요청자 · 조건 | ✗ | ✗ |
| 수락 전 수정 `work_request.amended` | REQ:564-616 · HTTP:2369 | 요청자 | 받는 사람 | ✗ | ✗ |
| 재상신 `work_request.resubmitted` | REQ:650-684 · HTTP:2355 | 요청자 | 받는 사람 | ✗ | ✗ |
| 철회 `work_request.withdrawn` + 업무 취소 | REQ:702-724 · HTTP:2312 | 요청자 | 받는 사람(REQ:739) | ✗ | ✗ |
| 요청 자료 첨부·해제·채택 | REQ:862·954·989 · HTTP:2529/2557/2606 | 당사자 | 요청 당사자 | ✗ | ✗ |
| 목록 정리 `list_entry_removed` | WT:1671-1692 · HTTP:2344 | 당사자 | — | ✗ | ✗ |
| 참고 읽음 | REQ:1239 · WT:2255 | CC | CC | ✗ | ✗ |
| 직접 배정 `task.assigned` | WT:2525-2590 · ASG:106-153 · HTTP:1712 | 배정자 | 배정자 `assigned_by` · 담당자 | ✗ | ✗ |
| 담당 넘김 `task.assignment.offered` | WT:2428-2456 · ASG:188-229 · HTTP:2155 | 배정자 | 새 담당자 | ✗ | ✗ |
| 담당 변경 제안 `task.assignment.change_proposed` | WT:2664-2702 · ASG:222 | 배정자 | 기존 담당(WT:2676) · 새 담당 | ✗ | ✗ |
| 담당 수락 `task.assignment_accepted`(+`assignment.changed`) | WT:2707-2793 · ASG:258-272 · HTTP:1739 | 새 담당 | 배정자 · 밀려난 담당(WT:2788) | ✗ | ✗ |
| 담당 거절 `task.assignment_rejected` | WT:2766-2781 · ASG:306-322 · HTTP:1746 | 새 담당 | 배정자 | ✗ | ✗ |
| 담당 제안 철회 `task.assignment_cancelled` | WT:2796-2841 · ASG:331-347 | 배정자 | 제안 받은 사람 | ✗ | ✗ |
| 업무 수정(제목·설명·**시작일·기한**·결재자·프로젝트·상위·선행) `task.updated` | APP:542-625 · HTTP:1755 | 담당 | 담당 · 결재자 · 자손(프로젝트 이동 APP:583-584) | ✗ | ✗ |
| 상위·프로젝트 이동 | APP:666-745 | 담당 | 자손 담당 — **「알림의 자리」 APP:741** | ✗ | ✗ |
| 시작·보류·재개(blocked)·완료·취소 `task.state_changed` | APP:2037-2118 · HTTP:2763-2786 | 담당(취소는 요청자 포함 APP:2120) | 담당 · 요청자 | ✗ | ✗ |
| 하위 추가 `task.subtask_added` | APP:524-528 | 만든 사람 | 상위 담당 | ✗ | ✗ |
| 선행 해제 `task.predecessor_released` | APP:1565-1619 · HTTP:1930 | 어느 쪽 편집자든 | 후행 담당 — **「알림의 자리」 APP:1581** | ✗ | ✗ |
| 완료 보고 `task.completion_submitted` | APP:1883-1926 · WT:780 · HTTP:1900 | 담당 | 확인자 = 요청자(APP:1906 · 2031-2035, `approver_id` 아님) | ✗ (판단함 항목은 열린다) | ✗ |
| 완료 승인 `task.completion_accepted` | APP:1933-1944 · AC:1483-1494 · HTTP:2500 | 확인자 | 보고자 `submitted_by` | ✗ | ✗ |
| **보완 요청** `task.completion_changes_requested` | APP:1946-1964 · AC:1494 | 확인자 | 담당/보고자 | ✗ | ✗ |
| **재개** `task.reopened` | APP:2140-2181 · HTTP:2085 | 요청자(요청 업무)·담당(APP:2183-2196) | 요청자 · 담당 | ✗ (SPEC-003:722 「요청 업무면 담당자에게 알림」은 미구현) | ✗ |
| 취소·조건변경 제안 `task.proposal_*_opened` | APP:2200-2228 · HTTP:2109 | 요청자·승격자 | 응답자 = 담당(APP:2273) | ✗ | ✗ |
| 제안 응답 `task.proposal_agreed/declined` | APP:2230-2283 · HTTP:2124 | 담당 | 제안자 `proposed_by` | ✗ | ✗ |
| 합의 취소 / 합의 조건 변경(기한 포함) | APP:2329-2341 / 2345-2366 | 담당 | 요청자 | ✗ | ✗ |
| 제안 철회 `task.proposal_withdrawn` | APP:2285-2309 · HTTP:2140 | 제안자 | 담당 | ✗ | ✗ |
| 체크리스트·진행 메모·참고·자료 `task.checklist.*`·`progress.noted`·`reference_*`·`material_*` | APP:2571-2697 · 2630-2650 · 2777/2799 · `modules/work/materials.py:169-272` | 담당 | 담당(관련자 별도 없음) | ✗ | ✗ |
| **댓글** (원장·감사 행 없음) | REQ:1122-1148 · WT:2986 · HTTP:2383 | 참여자 | 작성자 `author_member_id` · 독자(`party_of`) | ✗ | ✗ |
| AX 판단 승인·거절 `action.approved/rejected` | ACT:478-489 · HTTP:1460 | 소유자 | `action.owner_id` | ✗ (그 실행이 발송·수락이면 아래쪽 2종만) | ✗ |

**댓글 사실**
- 댓글은 **업무 요청 스레드에만** 있다(`CommentRecord` `persistence.py:1323-1333`, FK `request_threads` :1171). 업무 단독 댓글 엔드포인트는 없다
- 요청에서 나온 업무는 원장의 `request_thread_id` 로 같은 스레드를 공유한다(WT:990, WT:310)
- **@멘션 파싱은 없다**(`grep -rniE 'mention'` 관련 히트 0)

### B-2. 메일

**수신 — external_worker 프로세스에서만**
- Pub/Sub pull 스레드(`src/bootstrap/external_worker.py:181-208`)
- 주소 → 연동 매핑(SYNC:553-555 · SS:108-115)
- historyId·watch 갱신·INBOX 백필·`history.list` 폴링(SYNC:582-633, 60초 SYNC:40). INBOX 라벨만 받는다(SYNC:646)
- Gmail 호출: `src/platform/external_gmail.py:98-131`

**저장** — `save_messages`(SS:152-214) → `external_messages`(`persistence.py:2160-2192`, `migrations/manual/2026-10-06-external-channels.sql:83-103`)
- 칸: `integration_id` · `room_id`(메일은 NULL) · `source_kind` · `container_key` · `external_key`(Gmail id) · `thread_key` · `sent_at` · `subject` · `author`(From) · `preview` · `raw`(Gmail JSON 전체) · `safe_html`
- 중복 방지: UNIQUE(integration, container, external_key)(migration :99)

**누구의 메시지함인가** — 연동 소유자 `external_integrations.member_id`(`persistence.py:2076`) 한 사람. 같은 주소를 두 사람이 연결하면 각자 한 벌씩 받는다.

**읽음 상태** — 있다. 사용자별 `external_read_states`(`persistence.py:2232-2250`, migration :134-149). 메일은 단건 `message_id`, 방은 `read_up_to_*`.

**받는 칸(To/CC 중 나)** — 없다. To/CC 는 열 때 raw 헤더에서 푼다(INB:576-578). 「나」 표지는 없다.

**게시 사건** — `inbox.message_arrived`(SS:222, 실시간 저장 20건까지) · `integration.changed`(SS:229)

### B-3. 슬랙

**수신**
- external_worker 의 Socket Mode 하나(`src/platform/external_slack.py:356-407`, 시작 `external_worker.py:129-133`)
- → `ExternalSync.handle_slack_event`(SYNC:249-284)

**분배(fan-out) 판정** — `slack_fanout_targets(team_id, channel)`(SS:120-131)
- 같은 `account_key==team_id` 인 활성 슬랙 연동 중 그 채널을 **방으로 고른** 연동만 받는다
- 그중 `verified` 이고 `access_lost` 가 아닌 방만 남긴다
- 각 방에 (integration, channel, ts) 한 벌씩 저장한다(SYNC:267-283)
- 나감·보관·삭제는 방을 멈추고(SYNC:286-321), 토큰 회수는 SYNC:323-338

**저장 필드**
- 방 종류 `external_rooms.room_type` = `channel|private|dm|group_dm`(external_slack.py:251-258, SYNC:530-535). 이벤트 자체의 `channel_type` 은 저장 전에 버린다(SYNC:282)
- 스레드: `thread_key = thread_ts`(`src/modules/external_channels/sync_messages.py:87`)
- 본문: `raw`(이벤트 전체) · `preview`(앞 2000자)(sync_messages.py:83-92)

**나를 멘션** — 칸이 없다
- `<@U…>` id 는 이름표 조회에만 쓰인다(SYNC:203-211 · 465-480 `room_meta.users`)
- 내 슬랙 id 는 연동의 `account_meta.user_id`(SS:69)에 있다. raw.text 와 이 값으로 판정할 재료는 있다

**내가 보낸 것** — 칸이 없다
- 미읽음 수에서 `author != account_meta.user_id` 로 뺀다(IS:197-199)

**관찰 3 — 내가 보낸 줄 빼기가 이름 조회에 걸린다**
- `_save_slack` 이 이름 조회에 성공하면 `author` 를 **표시 이름으로 덮는다**(SYNC:484-485). 이후 IS:197-199 는 그 `author` 를 슬랙 id 와 비교한다
- 그래서 그 비교는 이름 조회가 실패한 줄에서만 「내 줄」을 가려낸다. 슬랙 id 는 `raw.user` 에 남아 있다
- 실제 미읽음 수 영향은 시험·운영으로 확인하지 않았다(조사 한계)

**읽음** — `external_read_states` 방 단위(B-2 와 같음)

### B-4. 카톡

**라우트**
- `POST /api/integrations/kakao/messages`(HIN:399)
- `…/attachments/{aid}`(HIN:407)
- `…/status`(HIN:432)
- 핸드셰이크 `GET /api/integrations/kakao/handshake`(HTTP:826)

**인증** — Bearer 기기 토큰. `device_principal` `src/entrypoints/http_auth.py:102-124`, SHA-256 해시로 `external_device_tokens` 에 저장(`persistence.py:2286`)

**저장** — `KakaoIngestApplication.ingest_messages`(`src/modules/external_channels/kakao_ingest.py:186-269`)
- 고른 방이 아니면 403(:194-196), 500건 초과면 413(:187-188)
- 같은 `external_messages` 에 `container_key=chatId`, `external_key=logId` 로 쓴다(:206-219)

**방** — `external_rooms.room_type` = `direct|group`(`src/modules/external_channels/domain.py:37`)

**보낸 사람** — 자유 글자 `author`(kakao_ingest.py:72)

**내가 보낸 것** — 칸이 없다. 입력 모델이 `extra="allow"`(:70)이고 `raw = model_dump`(:205)라서, 수집기가 보낸 여분 키는 `raw` 에 남는다.

**게시 사건** — `inbox.message_arrived`(kakao_ingest.py:258) · `integration.changed`(:324). **API 프로세스**에서 난다.

### B-5. 회의

| 사건 | 자리(`src/modules/meetings/application.py`) | 아는 관련자 | 알림 | 스트림 |
|---|---|---|---|---|
| 생성(=초대) `meeting.created` | :302-339(감사 :338) | `owner_id`(:430) · `attendee_ids`·외부 참석자(:437-438) | ✗ | ✗ |
| 정보 수정·참석자 교체 `meeting.updated` | :481-540(`replace_attendees` :531) | 참석자 · 소유자(:508) | ✗ | ✗ |
| 취소 `meeting.cancelled` | :591-603 | 참석자 | ✗ | ✗ |
| 시작·종료 `meeting.started/ended` | :630 · :644 | 참석자 | ✗ | 회의 WS 는 참석 중인 사람만 |
| **회의록 합성 완료** `meeting.finalized` | `commit_finalized` :886-970(감사 :969) | 소유자 · 참석자(:1029-1031) | ✗ | ✗ (meeting_worker 는 DB 만 쓴다, `src/bootstrap/meeting_worker.py:1-5`) |
| 합성 실패 `meeting.finalize_failed` | :972-980 | 소유자 | ✗ | ✗ |
| 공유·회수 `meeting.shared/share_revoked` | :1112-1133 · :1179-1223 | 공유 대상 · 소유자 · 참석자 | ✗ | ✗ |
| 안건 추가·수정·삭제 | :1250 · :1305 · :1344 | 참석자 | ✗ | 회의 WS `agenda.*`(진행 중 회의만) |

- 「회의 초대·변경」은 생성·수정 감사 사건으로만 존재한다. 사람에게 가는 전달은 없다

### B-6. 연동 수집 실패 (DEC-008 D-50 배너)

**상태 값** — `connected|backfilling|disconnected|removed`(domain.py:20-24, migration CHECK :46). 사유는 `disconnected_reason`·`disconnected_at`.

**`disconnected` 로 만드는 자리**
- 워커: `mark_disconnected`(SS:349-361) ← SYNC:338(`token_revoked`·`app_uninstalled`) · :363 · :389 · :568
  - 슬랙 인증류 오류는 external_slack.py:40-43
  - Gmail 은 401·`invalid_grant` 일 때(external_gmail.py:49-58). 403 은 아니다
- API·워커 공통: `InboxApplication._mark_disconnected`(INB:1054-1069), 사유 `revoked`·`token_expired`(:1026·1048·1051)

**카톡** — status 를 바꾸지 않는다. `collector_status`·`collector_reported_at` 을 쓰고, 보고 없이 90초가 지나면 꺼짐으로 본다(domain.py:47, 124-148). 그때 방은 `paused`.

**방** — `paused` + `room_meta.access_lost`(SS:295-317)

**기록되지 않는 실패**
- 슬랙 앱 토큰이 거절되면 Socket Mode 가 로그만 남기고 멈춘다(external_slack.py:401-403)
- Pub/Sub 거절도 로그만 남긴다(external_worker.py:188-190)

**노출**
- `GET /api/integrations`(HTTP:822-824) — `IntegrationView`(`src/modules/external_channels/application.py:185-195, 655-689`)에 `status`·`collector` 가 있다. **`disconnected_reason` 은 내지 않는다**
- 방 상태: `GET /api/integrations/{id}/rooms`(HTTP:852)
- WS `integration.changed`(`data.status`, SS:363-369)

### B-7. 시안의 설정 알림 항목 ↔ 코드 사건

| 시안 항목 | 대응 사건이 코드에 있나 | 근거 |
|---|---|---|
| 배정됐을 때 | **있음** — 요청 발송(REQ:452), 직접 배정 `task.assigned`(WT:2525-2590), 담당 넘김·변경 제안(WT:2428-2456·2664-2702). **알림은 요청 발송만** 만든다(WT:2116) | B-1 |
| 기한 하루 전 | **사건 없음** — 기한 값(`due_date`)과 기한 변경 사건(`task.updated` APP:621, 합의 조건 변경 APP:2345-2366)은 있지만, 「하루 전」에 일어나는 사건을 내는 자리가 없다 | 아래 스케줄러 |
| 내 업무에 댓글 | **부분** — 업무 **요청** 스레드 댓글만 있다(REQ:1122-1148). 원장·감사 행이 없고, 업무 단독 댓글은 없다 | B-1 댓글 |
| 회의록 정리 완료 | **있음** — `meeting.finalized` 감사(application.py:969). 알림·스트림 없음 | B-5 |
| 연동 수집 실패 | **있음(일부)** — `disconnected` 전이(SS:349-361, INB:1054-1069) + `integration.changed` 사건(SS:366, INB:1065). 슬랙 앱 토큰·Pub/Sub 거절은 기록되지 않는다 | B-6 |
| 일일 요약 | **사건 없음** — 일일 보고 생성은 사용자가 요청할 때만 잡을 넣는다(BA:2803-2814, `src/bootstrap/report_worker.py:46`) | 아래 |

**스케줄러·시각 기반 워커 — 없다**
- `grep -rniE 'apscheduler|crontab|schedule\.every|celery' src` → 0
- 워커 5종은 모두 durable job 큐 소비자거나 외부 동기화 루프다. **업무 `due_date`·`start_date` 를 훑는 루프는 없다**
  - `src/bootstrap/conversation_worker.py:76`
  - `material_worker.py:72`
  - `meeting_worker.py:57`
  - `report_worker.py:46`
  - `external_worker.py:109/143/184/217`
- 잡 전송은 `src/platform/durable_jobs.py` 다(`FOR UPDATE SKIP LOCKED`). 지연 실행(`run_at`·예약 시각) 칸이 있는지는 이번에 보지 않았다(조사 한계)
- `docs/` SPEC-003 Scope 는 「무응답·기한 초과의 자동 전이 없음」(spec-003:145)이고, 「자동 전이는 어느 자리에도 없다」(spec-003:855)

---

## 3. C. 실시간 전달

### C-1. 서버 → 브라우저 경로 전부

- `grep -rnE '@app\.websocket' src` → **2**
- `StreamingResponse|EventSourceResponse|text/event-stream` → **0**(SSE 없음)

**① `/api/inbox/stream` (HIN:338-396)**
- 인증
  - 같은 출처 검사(:346-348, 아니면 `CLOSE_FORBIDDEN_ORIGIN`)
  - `connection_principal`(세션 쿠키 / 개발 `X-Demo-Persona`, `http_auth.py:82-101`). 없으면 `CLOSE_UNAUTHORIZED`(:350-353)
- 프레임: 먼저 `{"type":"ready"}`(:367). 이어 `UserEvent` 의 `type`·`integration_id`·`room_id`·`message_id`·`source_kind`·`data`(:376-383). **본문은 싣지 않는다**
- 사건 종류 **4개**(`src/modules/external_channels/events.py:30-39`)
  - `inbox.message_arrived`
  - `inbox.reply_result`
  - `integration.changed`
  - `inbox.message_updated`
- 사건을 내는 자리 — `UserEventType.` 생성 12히트(정의 제외 11)
  - 워커: SS:222 · 229 · 251 · 366 · INB:938
  - API: kakao_ingest.py:258 · 324 · external_channels/application.py:336 · 652 · BA:1790
  - 둘 다: INB:1065
- 사람별 거르기 — **한다**. `UserEventHub._deliver` 가 `event.member_id` 의 큐에만 넣는다(`src/platform/user_event_hub.py:118-125`)
- 묶기·밀림
  - `integration.changed` 는 같은 회원·같은 연동에 1초 1회로 묶는다(user_event_hub.py:29-30, 94-116)
  - 큐는 200칸이고, 넘치면 가장 오래된 것을 버린다(:28, 148-154)
- 하트비트 없음. 올라오는 프레임은 읽고 버린다(:358-362)
- **알림(`notifications`)·업무 사건은 이 채널에 실리지 않는다** — 업무 코드에 `user_events.publish` 호출 0
  - 채널 docstring 은 「2단계(AX 판단·알림)도 쓸 사용자 사건 채널」이라고 적는다(events.py:7-9)

**② `/api/meetings/{meeting_id}/stream` (HTTP:1245-1276)**
- 인증
  - 쿠키 principal(:1253-1255)
  - 그다음 5초 안에 `auth` 프레임 `role=upstream|subscribe`(:1257-1264, `StreamAuthFrame` :309-318)
  - 참석·상태·업스트림 하나 검사(`src/modules/meetings/stream_service.py:127-160`)
- 프레임: `ready` · `transcript.partial/final` · `ai.batch` · `memo.line(.updated/.removed)` · `agenda.added/updated/removed` · `error`(HTTP:321-366)
- 원천: API 프로세스 안의 회의별 메모리 `_Room`(stream_service.py:119, 301-321)
- 거르기: 회의 단위다(참석 검사 뒤). 회원 단위가 아니다

**그 밖** — 밀어 주는 경로가 없다. 모두 폴링이다
- AX 대화: `POST /api/conversations/{id}/messages` 가 202 를 주고 `GET` 으로 폴링한다(HTTP:1419 · 1408)
- 일일 보고: `GET /api/daily-reports/status` 폴링(HTTP:2693)
- 알림: REST 만 있다

### C-2. 여러 프로세스에서 난 사건이 스트림까지 오는 길

**보내는 쪽** — `platform/user_events.publish`(`src/platform/user_events.py:12-16`)
- `SELECT pg_notify('ax_user_events', payload)` 를 **같은 트랜잭션**에서 부른다 → 커밋될 때 전달된다
- PostgreSQL 이 아니면 아무것도 하지 않는다
- `user_events.publish` 9히트. 그중 `src/bootstrap/external_inbox.py:251` 은 워커 깨우기 채널 `ax_external_sync` 다

**듣는 쪽** — API 프로세스마다 데몬 스레드 하나가 `LISTEN ax_user_events`(user_event_hub.py:66-74, 130-145). 시험 DB 에서는 같은 프로세스 `dispatch`(:85-92, `src/bootstrap/external_inbox.py:144-147`).

**게시하는 프로세스** — **API · external_worker 둘뿐**
- conversation·material·meeting·report 워커는 `user_events`·`USER_EVENTS_CHANNEL` 을 import 하지 않는다
- 그래서 **회의록 합성 완료(meeting_worker)·자료 추출(material_worker)·보고(report_worker)·AX 턴(conversation_worker)** 은 지금 어떤 스트림에도 닿지 않는다(DB 에 쓰고 화면이 폴링한다)

**회의 WS** — 교차 프로세스 길이 없다. STT·AI 배치·안건/메모 변경이 모두 API 프로세스 안에서 메모리 방에 직접 민다(BA:696-706, 2312-2393, 2635-2637, 4452-4487). API 프로세스가 여럿이면 같은 회의라도 다른 프로세스의 방에는 닿지 않는 구조다(코드 구조상의 사실이고, 운영 프로세스 수는 확인하지 않았다).

### C-3. 끊겼다 다시 붙을 때

- 두 WS 모두 **커서·last-event-id·since 가 없다**
- 받은편지 채널은 「연결이 끊기면 … 그 사이 사건은 잃는다 — 화면은 WS 재연결 때 API 로 다시 읽는다」(user_event_hub.py:11). NOTIFY 는 저장되지 않는 신호다
- 회의 WS 는 `ready` 에 `latestBatchSeq` 를 실어 주는 스냅샷 힌트만 있다(stream_service.py:274-278, 606-614)
- 알림 목록 API 에도 `since`·커서가 없다(A-3)

---

## 4. D. 설정

### D-1. 사용자별 설정 저장 자리

**`members`**(`MemberRecord` `persistence.py:59-76`)
- 칸: `id` · `display_name` · `employment_state` · `employment_type` · `phone` · `birth_date` · `account_ref` · `record_status` · `created_at`
- **JSON·선호 칸이 없다**

**사용자별 선호 표는 하나** — `assistant_character_preferences`(`AssistantCharacterPreferenceRecord` `persistence.py:79-89`): `member_id` PK · `character_key` · `version` · `updated_at`

**그 밖의 사람별 표(설정이 아님)**
- `member_credentials`(:92-100)
- 프로필 이미지(:2326-2335)
- `auth_sessions`(:2037)
- `external_device_tokens`(:2286)
- `external_read_states`(:2232)

**알림 설정·알림 경로 설정 표는 없다**

### D-2. 메일·슬랙 DM 으로 「나에게 보내기」 수단 — 사실만

**슬랙 답장** — `POST /api/inbox/rooms/{room_id}/reply`(HIN:284)
- 로그인 세션만 부를 수 있다
- 방은 **내 연동이 고른 방**이어야 한다(INB:777). 카톡 방은 `read_only` 로 거부(:778-779)
- 내 사용자 토큰으로 `chat.postMessage`(또는 파일 업로드)를 `room.external_id` 에 보낸다. `thread_ts` 는 선택이라 최상위 글도 된다(INB:948-961, `src/platform/external_inbox_upstream.py:239-263`)
- `conversations.open`(새 DM 열기)이나 임의 채널 지정은 없다. 자기 DM 이 이미 고른 방이면 막는 코드는 없다

**메일 답장** — `POST /api/inbox/mail/{message_id}/reply`(HIN:309)
- 저장된 메일에 대한 답장이어야 하고, `threadId`·`In-Reply-To` 를 잇는다(INB:1004-1024)
- `to`·`cc` 는 임의 주소를 받는다(INB:814-816). 자기 주소는 전체답장 확장 때만 빠진다(:817-822)
- Gmail `messages/send`(external_inbox_upstream.py:179-190)

**공통** — API 는 202 를 주고 `external_sent_replies` 행과 durable job 을 쌓는다(`src/bootstrap/external_inbox.py:232-251`). external_worker 가 보내고(external_worker.py:146) 결과를 `inbox.reply_result` 로 알린다(INB:938).

**답장이 아닌 새 메일 작성·시스템 계정 발신**(SMTP·서비스 계정) 수단은 코드에서 찾지 못했다.

---

## 5. 공통 — 계약 테스트·journey 위치

| 범위 | 파일 |
|---|---|
| 알림 | `tests/contract/test_notifications.py`(시험 1개, :43) · `tests/contract/test_personal_command_tools.py` · `tests/contract/test_unified_queries.py`(:49) · `tests/contract/test_task_successors.py`(:495 「알림 모듈을 안 부른다」) · `tests/architecture/test_local_stack_targets.py:32-33` — **5파일** |
| 사용자 사건·메시지함 WS | `tests/unit/test_user_event_hub.py` · `tests/contract/test_external_inbox.py`(WS :541·543·559·602·658·661) · `tests/contract/test_kakao_ingest_and_profile.py`(WS :187·200) · `tests/contract/test_inbox_message_context.py` · `tests/integration/postgres/test_external_channels_postgres.py` · `tests/unit/test_external_channel_rules.py` (+ `tests/contract/conftest.py`) |
| 외부 채널 그 밖 | `tests/contract/test_external_channels.py` · `test_external_sync.py` · `tests/integration/postgres/test_inbox_message_origin_postgres.py` · `tests/unit/test_external_sync_messages.py` · `test_inbox_rules.py` · `test_slack_directory.py` · `tests/architecture/test_external_channel_schema.py` |
| 회의 WS | `tests/contract/test_meeting_stream.py` · `test_browser_recording.py` · `test_production_route_registration.py` · `tests/architecture/test_architecture.py` |
| 업무 수신함 | `tests/contract/test_work_request_inbox_categories.py` |
| 운영 인벤토리 drift | `tests/architecture/test_operation_inventory.py` ↔ `docs/unified-operations-inventory.json`(:650-666 · :1860-1879 · :8450-8572) |
| acceptance journey | **`tests/acceptance` 디렉터리 없음.** 옛 모양 재현 헬퍼 `tests/legacy_acceptance.py` 만 있다. 「journey」는 헬퍼 이름으로만 나온다(`tests/contract/test_relation_graph.py:42`, `test_mcp_graph_results.py:5`) |

---

## 6. 사건 × 관련된 사람 표

| 사건 | 발생 자리 | 알 수 있는 관련자 | 지금 알림 생성 | 지금 스트림 사건 |
|---|---|---|---|---|
| 업무 요청 발송 | REQ:452 → WT:2116 | 받는 사람 · 요청자 · CC · 결재자 · 승격자 | **✅ 받는 사람(`work_request.received`)** | ✗ |
| 업무 요청 수락 | REQ:506 → WT:2116 | 요청자 · 받는 사람 | **✅ 요청자(`work_request.accepted`)** | ✗ |
| 요청 거절·협의·수정·재상신·철회 | REQ:509-724 | 요청자 · 받는 사람 · CC | ✗ | ✗ |
| 직접 배정·담당 넘김·변경 제안·수락·거절·철회 | WT:2428-2841 · ASG:106-347 | 배정자 · 새 담당 · 기존 담당 | ✗ | ✗ |
| 업무 수정(기한·시작일 포함) | APP:542-625 | 담당 · 결재자 · 자손 담당 | ✗ | ✗ |
| 상위·프로젝트 이동 | APP:666-745 | 자손 담당(「알림의 자리」 :741) | ✗ | ✗ |
| 시작·완료·취소 | APP:2037-2118 | 담당 · 요청자 | ✗ | ✗ |
| 완료 보고 | APP:1883-1926 | 요청자(확인자) | ✗ (판단함 항목) | ✗ |
| 완료 승인·보완 요청 | APP:1933-1964 | 보고자·담당 | ✗ | ✗ |
| 재개 | APP:2140-2181 | 요청자 · 담당 | ✗ | ✗ |
| 취소·조건변경 제안 / 응답 / 철회 | APP:2200-2366 | 요청자·승격자 ↔ 담당 | ✗ | ✗ |
| 선행 해제 | APP:1565-1619 | 후행 담당(「알림의 자리」 :1581) | ✗ | ✗ |
| 요청 댓글 | REQ:1122-1148 | 작성자 · 요청자 · 승격자 · 담당 · CC | ✗ | ✗ |
| 메일 수신 | SS:152-214 (워커) | 연동 소유자 `external_integrations.member_id` | ✗ | ✅ `inbox.message_arrived`(SS:222) |
| 슬랙 수신 | SYNC:249-284 · SS:120-131 (워커) | 그 방을 고른 각 연동 소유자. 내 슬랙 id 는 `account_meta.user_id`. 멘션·발신자는 raw 에만 있다 | ✗ | ✅ `inbox.message_arrived` |
| 카톡 수신 | kakao_ingest.py:186-269 (API) | 연동 소유자. 보낸 사람은 `author` 글자 | ✗ | ✅ `inbox.message_arrived`(:258) |
| 메일·슬랙 답장 결과 | INB:938 (워커) | 보낸 사람 | ✗ | ✅ `inbox.reply_result` |
| 메시지로 만든 업무 확정 | BA:1773-1800 (API) | 연동 소유자 | ✗ | ✅ `inbox.message_updated` |
| 연동 끊김·되살림·백필 끝·카톡 수집기 상태 | SS:349-369 · INB:1054-1069 · kakao_ingest.py:311-324 · external_channels/application.py:336·652 | 연동 소유자 | ✗ | ✅ `integration.changed`(1초 묶음) |
| 회의 생성(초대)·수정·취소 | meetings/application.py:302-603 | 소유자 · 참석자 | ✗ | ✗ |
| 회의록 합성 완료·실패 | meetings/application.py:886-980 (meeting_worker) | 소유자 · 참석자 | ✗ | ✗ |
| 회의 공유·회수 | meetings/application.py:1112-1223 | 공유 대상 · 소유자 | ✗ (tool_catalog.py:446) | ✗ |
| 회의 진행(전사·메모·안건) | stream_service.py · HTTP:1245 | 참석 중인 접속자 | ✗ | ✅ 회의 WS(회의 단위) |
| 기한 하루 전 · 일일 요약 | **사건 없음** | — | ✗ | ✗ |

---

## 7. grep 개수표

범위: `backend/src/ax_workspace` 에서 `grep -rnE '<패턴>' . --include='*.py' | wc -l`(별도 표기가 없으면).

| 패턴 | 개수 | 비고 |
|---|---|---|
| `\.emit\(` | **1** | WT:2116 — 알림 생성 자리 전부 |
| `SqlAlchemyNotificationRepository` | 5 | import 2 · 생성 1 · 조립 2 |
| `NotificationRecord` | 17 | |
| `NotificationApplication` | 6 | |
| `list_notifications` | 9 | HTTP·MCP·BA·tool_catalog |
| `mark_notification_read` | 7 | |
| `notification\.mark_read` | 6 | ActionItem 종류 |
| `_authorized_notification_view` | 1 | 정의만 있고 호출 0 |
| `append_audit\(` | 37 | 업무 요청 11 · 회의 다수 · 정의·프로토콜 |
| 그중 알림이 되는 `event_type` | 2 | `work_request.created`·`accepted` |
| 업무 원장 `task.*` 사건 종류 | 33 | 쓰기 호출을 손으로 짚어 셈 |
| 요청 원장 `work_request.*` 사건 종류 | 10 | 〃 |
| 요청 감사 `event_type` 종류 | 11 | REQ 의 11줄 |
| `"(task\|work_request)\.[a-z_.]+"` 서로 다른 글자 | 82 | 권한·ActionItem 이름과 섞인 수 |
| `알림의 자리` | 2 | APP:741 · APP:1581 |
| `user_events\.publish` | 9 | 그중 1 은 워커 깨우기 채널 |
| `pg_notify` | 1 | `platform/user_events.py:16` |
| `UserEventType\.` | 12 | 정의 제외 사건 생성 11 |
| `UserEventType` 값 | 4 | 메시지함·연동만 |
| `@app\.websocket` | 2 | 메시지함 · 회의 |
| `StreamingResponse\|EventSourceResponse\|text/event-stream` | 0 | SSE 없음 |
| `apscheduler\|crontab\|schedule\.every\|celery` | 0 | 스케줄러 없음 |
| `mark_disconnected` | 10 | 수집 실패 전이 |
| `disconnected_reason` | 5 | API 응답에는 나가지 않음 |
| `resource_type="meeting"\|resource_type == .meeting.` | 11 | 전부 관계·읽기 분기, 알림 쓰기 0 |
| `@멘션 파싱`(`mention`) | 0 | 관련 히트 없음 |
| 프론트 `getNotifications\|markNotificationRead` 호출부 | 0 | `frontend/src` 정의 2줄만 |
| `migrations/` 안 `notifications` | 0 | ORM create_all 로만 선다 |
| 알림 관련 시험 파일(`grep -rli notification tests`) | 5 | §5 |

---

## 8. 코디 확인 필요 (운영 DB·로그로만 갈리는 것)

운영 DB 에 접속하지 않았다. 아래 쿼리는 초안이다.

1. **운영 `notifications` 행이 실제로 쌓였나 · 종류별·읽음 비율** — 쌓였다면 이미 「안 보이는 알림」이 쌓여 있는 것이다(프론트 호출부 0)
   ```sql
   SELECT kind, count(*) AS n, count(read_at) AS read_n, min(created_at), max(created_at)
   FROM notifications GROUP BY kind;
   ```
2. **meeting·그 밖의 resource_type 행이 있나**(A-1 관찰 1의 갈래가 운영에서 닿는가)
   ```sql
   SELECT resource_type, source_kind, count(*) FROM notifications GROUP BY 1,2;
   ```
3. **v2 발송 요청에 수락이 실제로 일어나 수락 알림이 서는가**(A-2 관찰 2)
   ```sql
   SELECT r.state, count(DISTINCT r.id) AS requests, count(n.id) AS accepted_notifications
   FROM work_requests r
   LEFT JOIN notifications n ON n.resource_id = r.id::text AND n.kind = 'work_request.accepted'
   GROUP BY r.state;
   ```
4. **수집 실패가 실제로 얼마나 나는가 · 사유 분포**(D-50 배너·「연동 수집 실패」 알림 빈도)
   ```sql
   SELECT kind, status, disconnected_reason, count(*) FROM external_integrations GROUP BY 1,2,3;
   ```
5. **슬랙 `author` 가 표시 이름으로 덮인 비율**(B-3 관찰 3 — 「내 줄」 판정이 깨지는 범위)
   ```sql
   SELECT count(*) FILTER (WHERE m.author = m.raw->>'user') AS author_is_id,
          count(*) FILTER (WHERE m.author <> m.raw->>'user') AS author_is_name
   FROM external_messages m JOIN external_integrations i ON i.id = m.integration_id
   WHERE i.kind = 'slack';
   ```
6. **API 프로세스 수**(운영 compose·로그) — `/api/inbox/stream` 은 프로세스마다 LISTEN 하므로 여럿이어도 닿는다. 회의 WS 는 메모리 방이라 프로세스 수에 따라 갈린다(C-2)
7. 운영 로그의 `user event listener reconnecting`(user_event_hub.py:143) 빈도 — 놓친 사건 구간의 크기

---

## 9. 조사 한계

- 테스트·서버를 돌리지 않았다. 모든 결론은 코드를 읽어 얻었다. 특히 관찰 1(회의 갈래 KeyError 가능성)·관찰 3(슬랙 내 줄 판정)은 **실행으로 확인하지 않았다**
- 업무 사건 표(B-1)의 줄 번호 상당수는 범위 조사 하위 에이전트가 모은 것을 바탕으로 했다. 직접 다시 연 것은 다음뿐이다. 나머지는 ±수 줄 오차가 있을 수 있다
  - WT:2096-2128 · 1405-1425 · 1497-1503 · 1885-1915
  - REQ:400-532 · 1183-1197 · 1205-1290
  - APP:730-760 · 1570-1600 · 2029-2036
- `durable_jobs` 에 「예약 시각 실행」(run_at) 칸이 있는지, 즉 스케줄러 없이 지연 잡으로 시각 기반 사건을 만들 재료가 있는지는 보지 않았다
- v2 발송 요청에 수락했을 때 수락 알림이 서는지를 직접 검증하는 시험은 찾지 못했다. 기존 시험은 옛 행 모양만 본다(A-2 관찰 2)
- `BA:1790` `inbox.message_updated` 를 내는 실행 경로가 API 프로세스인지 conversation_worker(AX 실행)인지 끝까지 따라가지 않았다. external_worker 가 아닌 것만 확인했다
- 프론트가 `/api/inbox/stream` 사건을 어떻게 쓰는지, 사이드바·설정 시안의 정확한 항목 문구는 frontend 리포트 몫이라 보지 않았다(시안 6항목은 브리프 문구를 따랐다)
- 운영 DB·로그·프로세스 구성은 보지 않았다(§8)
- SPEC-003·008 은 「알림」 줄 주변만 읽었다. 그 SPEC 의 미정(EU-7 「다시 분해·재요청 사실을 요청자에게 어떻게 알릴지」 spec-003:1052, V-19 「재개 시 담당자 알림」 spec-003:722)이 코드와 어긋나는 것은 사실로만 적었다
