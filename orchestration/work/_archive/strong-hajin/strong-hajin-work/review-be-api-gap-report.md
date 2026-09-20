# [reviewer] WORK-003 BE API gap — read-only 검수 보고

작성: 2026-09-20 · 리뷰 대상 워크트리 `/Users/kknaks/orca/workspaces/Strong_hajin/strong-hajin-work`
(브랜치 `kknaksss/strong-hajin-work`, 미커밋) · **소스와 diff만 읽었다. 코드·문서·테스트를 한 줄도 고치지 않았고
테스트·빌드·DB·E2E를 실행하지 않았다.**

---

## 0. 판정 요약

| # | 검수 항목 | 판정 |
|---|---|---|
| 1 | 자료 5 route 가 기존 attachments/bindings 재사용 · `work_request` context 일관 · 새 테이블/우회 없음 | **PASS** (F-1 이 AX 표면 한 곳에서 이 원칙을 깬다) |
| 2 | 요청자만 attach/detach · 참여자만 read/download · pending·negotiating 외 409 | **PASS** |
| 3 | 수락 시 원본 request binding 보존 + task binding 추가가 한 transaction · 멱등 | **PASS** |
| 4 | 요청 projection 의 preceding/reference/materials 가 생성·발송·상세·목록에서 shape 유지 | **PASS** (W-2 성능) |
| 5 | 회의 승격 직행/action 경로가 일곱을 빠뜨리지 않음 | **PASS** (W-5 테스트 공백) |
| 6 | CC 후보 완화가 `task.self_manage` 범위에 머무름 | **PASS** |
| 7 | FastAPI/SQLAlchemy 경계 · 예외 매핑 · operation inventory · allowed path · 테스트 존재 | **FAIL** (F-1 inventory drift) |
| 8 | 워커가 보고한 checkout 사고와 inventory 복구 | **WARN** (W-1 · 복구 자체는 현재 파일에서 확인됨) |

**전체 판정: FAIL 2건 · WARN 6건.** FAIL 둘 다 요청 자료 계약의 **가장자리**(AX 매핑 한 행, 레거시 첨부
다운로드 route)에 있다. 핵심 5 route 의 권한·상태·이중 바인딩·projection 계약 본체는 코드로 확인했고
계약대로다.

---

## 1. 검수 방법과 한계

- `git diff origin/main` 과 현재 워크트리 파일을 읽었다. 이번 dispatch 의 변경과 기존 WORK-003 미커밋
  변경은 **파일 단위가 아니라 hunk 단위로** 갈랐다 — `persistence.py`·`domain-model.md`·`frontend/` 의
  `M` 은 전부 기존 WORK-003/W2 작업의 것이고 요청 자료와 무관함을 diff 내용으로 확인했다(§7-4).
- inventory 정합성은 **테스트를 돌리지 않고** `tests/architecture/test_operation_inventory.py` 의
  HTTP 절반(AST 기반)을 그대로 재현해 정적으로 대조했다(§7-3). MCP 도구 스키마 절반은 런타임
  서버 기동이 필요해 **실행하지 않았다** — 그 부분은 미검증으로 남긴다.
- 워커가 보고한 4 failed(`test_material_worker_recovery` 2 · `test_material_search` 2)는 **재현하지
  않았다**. 대신 인과를 코드로 좁혔다(§8).

---

## 2. 항목 1 — 저장 구조 재사용과 context 일관성 · **PASS**

- 새 테이블 0. `git diff origin/main -- backend/src/ax_workspace/platform/persistence.py` 의 추가 클래스는
  `task_creation_attempts`·`task_predecessors`·`work_request_read_receipts`·`work_request_list_entries`·
  `task_proposals` 뿐으로, **전부 기존 WORK-003/W2 의 것**이고 요청 자료용 표는 없다.
- 기존 `attachments` + `attachment_bindings` 를 그대로 쓴다:
  `backend/src/ax_workspace/modules/work/requests.py:912` `_bind_material` 이
  `context_type=WORK_REQUEST_MATERIAL_CONTEXT`(= `"work_request"`, `requests.py:174`),
  `role=WORK_REQUEST_MATERIAL_ROLE`(= `"input"`, `requests.py:178`) 로 바인딩한다.
- 스키마 여유 확인: `attachment_bindings.context_type` 은 `String(20)` · CHECK 없음
  (`backend/src/ax_workspace/platform/persistence.py:1258`) → `"work_request"`(12자) 가 마이그레이션 없이
  들어간다. 인덱스 `ix_attachment_bindings_context` 가 그대로 쓰인다(`persistence.py:1254`).
- storage key 안전성: `backend/src/ax_workspace/platform/materials.py:9-11` 의 `_SAFE_KEY` 에
  `work_requests/<uuid>/materials/<uuid>` 가 **자기 접두로** 추가됐다. `comments|evidence` 자리를 빌려
  쓰지 않는다. `requests.py:835` 의 `key_prefix=f"work_requests/{request.id}/materials"` 와 일치한다.
- 생성 payload 불변: `WorkRequestCreateInput` 에 자료 칸이 없다. 자료는 `request_id` 를 받은 뒤 붙이는
  2단계다(`requests.py:815-819` 주석 · `entrypoints/http.py:2189-2193` 주석).
- 댓글/evidence 우회 없음: `attach_material` 은 `_comment_attachment_target`·`_evidence_target` 을
  거치지 않고 자기 경로만 쓴다(`requests.py:827-843`). 세 context 는 `material_bindings()` 에서만
  합쳐지고(`requests.py:1013`) 그것은 **읽기 집계**다.

> 단, AX 표면에서는 이 원칙이 깨져 있다 — **F-1** 을 보라.

---

## 3. 항목 2 — 권한·상태 경계 · **PASS**

판정이 `_material_writer` 한 곳에 모여 있고(`requests.py:891-906`) 순서가 계약대로다:

| 단계 | 코드 | 결과 |
|---|---|---|
| `work_request.read` 없음 | `requests.py:897` `self._require(...)` → `WorkRequestAccessDenied` | 403 (`entrypoints/http.py:522`) |
| 참여자 아님 | `requests.py:900` → `_participant_request` (`requests.py:1080-1086`) → `WorkRequestNotFound` | 404 (`ResourceNotFound` 분기, `http.py:468`) |
| 읽을 수는 있으나 요청자 아님 | `requests.py:901-902` `_is_requester` | 403 |
| `pending`·`negotiating` 아님 | `requests.py:903-904` · `_MATERIAL_WRITABLE_STATES` (`requests.py:181`) → `WorkRequestNotPending` | 409 (`http.py:561`) |

- 읽기·내려받기는 참여자 전부: `list_materials`(`requests.py:821-825`)·`open_material`
  (`requests.py:861-879`) 둘 다 `_participant_request` 하나만 지난다. `_is_participant` 는
  `parties.py::may_read` 로 요청자·담당·CC 셋을 연다(`requests.py:1120-1123`,
  `modules/work/parties.py:33-36`). 「보이는데 못 받는다」가 없다.
- 승격 요청에서 **누른 사람**이 요청자 자리에 선다(`requests.py:1089-1098`, D40) — 시스템 요청자 때문에
  아무도 못 고치는 요청이 생기지 않는다.
- 거절·철회 뒤: 목록·내려받기는 상태를 묻지 않고 그대로 열리고, 붙이기·떼기만 409 다. 계약 테스트가
  이것을 못 박는다(`backend/tests/contract/test_work_request_materials.py:94-99`).
- `kind` 경계: `_require_material_role`(`requests.py:908-910`)이 `input` 외를 `MaterialError` 로 거절하고,
  `MaterialError` 는 `TaskError` 하위(`modules/work/material_values.py:18`)라 422 로 나간다
  (`http.py:555`). 링크 입력은 pydantic `Literal['input']` 로 한 겹 더 막힌다
  (`modules/work/request_commands.py:29`).
- **결재자(`approver_id`)는 읽기에서 제외**됐다. 브리프의 「현재 권한 계약에 맞는 주체」를 좁게 읽은
  판단이고, 근거가 있다: `GET /api/work-requests/{id}` 자체가 결재자에게 열려 있지 않으므로
  (`parties.py` 의 세 자리에 결재자가 없다) 자료만 넓히면 「요청은 못 보는데 그 자료는 받는」 자리가
  생긴다. **의도된 미구현**으로 읽고 FAIL 로 세지 않는다 — 다만 W-6 으로 남긴다.

---

## 4. 항목 3 — 수락 시 이중 바인딩 · **PASS**

- `accept()` 가 `accept_request_assignment` 직후 `_adopt_materials_into_task` 를 부른다
  (`requests.py:461`). 원본 요청 binding 은 **건드리지 않고**, 같은 `attachment_id` 에
  `context_type="task"` binding 을 더한다(`requests.py:1004-1010`). 복사본 없음 → 파일·무결성 해시 하나.
- **멱등**: 이미 그 업무에 붙은 attachment 는 건너뛴다(`requests.py:996-1003` 의 `already` 집합).
- **한 transaction**: `WorkflowApplication.accept_work_request` 가 `with self._session_factory()` 안에서
  상태 변경 + 입양을 끝내고 그 뒤에 한 번 `session.commit()` 한다
  (`backend/src/ax_workspace/bootstrap/application.py:3114-3122`).
- **모든 수락 경로가 같은 함수를 지난다**: REST(`http.py:2293`) · MCP(`entrypoints/mcp.py:383-388`) ·
  판단함 확인(`platform/action_center.py:252`) · action 실행(`platform/actions.py:877`) 넷 다
  `WorkRequestApplication.accept` 로 수렴한다 → 입양을 빠뜨리는 경로가 없다.
- DB 행으로 고정한 테스트가 있다: `tests/contract/test_work_request_materials.py:118-128`
  (`{("work_request", rid), ("task", task_id)}`, 둘 다 `unbound_at is None`, `role == "input"`).

관찰(차단 아님) — W-3: 입양은 `task.version` 을 올리지도 `task.material_attached` 활동을 남기지도
않는다(`requests.py:989-1011`). 업무 자료의 정상 경로(`modules/work/materials.py:277-281` `_moved`)와
다르다. 수락 화면을 이미 열어 둔 담당자는 자료가 는 것을 회차로 알 수 없고, 업무 이력에 그 자료가
어디서 왔는지 줄이 남지 않는다.

---

## 5. 항목 4 — projection shape · **PASS** (성능 WARN)

- 세 키가 `_view` 한 곳에 들어가므로(`requests.py:1404-1413`) **생성·발송·수락·거절·상세·목록·수신함·
  영수증이 전부 같은 모양**으로 나간다 — `_view` 를 지나지 않는 요청 응답이 없다.
- `preceding_task_ids` 는 파생 업무의 **활성** 선행에서 읽는다
  (`platform/work_tasks.py:2113-2131`, `released_at IS NULL`). 업무 쪽 투영
  (`platform/work_tasks.py:1102-1120` `predecessors_for`)과 **같은 기준**이라 두 화면이 어긋나지 않는다.
  `task_id` 가 `None` 이면 `[]` 를 돌려주므로 업무 없는 옛 요청 행에서도 안전하다.
- `reference_task_ids` 는 `request_references` 행 그대로이고, 기존 `references`(권한별 해소)와
  **별개 키**라 기존 계약을 덮지 않는다(`request_results.py:60-63`).
- `materials` 는 목록 경로에서 `extractions=False` 로 추출 표를 건너뛴다(`requests.py:1413`).
  `WorkRequestMaterialView` 는 `TaskMaterialView` 를 상속해 업무 자료와 **같은 키**로 나가고
  (`request_results.py:10-20`), 공용 `material_view` 가 채우는 `task_id`(= binding.context_id, 요청에서는
  요청 id)를 `_material_view` 가 **덮어쓴다**(`requests.py:969-977`) → 요청 id 가 `task_id` 로 새지 않는다.
- 상태·요청자 카드 계약(`state`·`requester_kind`·`assignment_state`·`promoted_by_member_id`)은 그대로다.

**W-2 (성능, 근거 있음)** — `_view` 가 요청 한 건마다 쿼리를 **4개** 더 쏜다:
`WorkRequestRepository.request_references`, `predecessor_task_ids`(`work_tasks.py:2113`),
`bindings_for`(`work_tasks.py:2813`), 그리고 `_material_views` 안의 `_derived_task_id`
(`requests.py:966` → `derived_task_ids([request])`, `work_tasks.py:2098`). 목록·수신함은 N 건이므로
**+4N 쿼리**다. 특히 `_derived_task_id` 는 **`_view` 가 이미 `derived` 를 손에 들고 있는데도**
(`requests.py:1356`) 다시 묻는 순수 중복이고, `list()` 는 그 값을 이미 bulk 로 구해 뒀다
(`list()` 안의 `derived = self._repository.derived_task_ids(requests)`, `requests.py:1193-1211`). 자료 검색도 이 길을 탄다 — `bootstrap/material_sources.py:76` 이 검색 한 번마다
`requests.list(principal)` 을 부른다.

---

## 6. 항목 5 — 회의 승격 · **PASS** (테스트 공백 WARN)

- 입력: `MeetingTodoPromotionInput` 에 일곱이 **같은 이름**으로 들어갔고 `extra="forbid"` 와 기존 다섯의
  뜻(`None` = 고치지 않음)은 그대로다(`backend/src/ax_workspace/modules/meetings/commands.py:235-263`).
- 직행 경로: `entrypoints/http.py:1003-1026`(route) → `bootstrap/application.py:1835-1894`
  (`promote_meeting_todo`) → `modules/work/creation_commands.py:201-270`(`create_work_request`,
  일곱이 전부 지문과 `requests.create` 로 흐른다). **일곱 다 실린다.**
- 확인(action) 경로: `bootstrap/application.py:3683-3711` 의 `meeting.todo.promote` 가 같은
  `MeetingTodoPromotionInput` 으로 재검증하고 **같은 일곱**을 `create` 에 싣는다
  (`application.py:3698-3705`).
- MCP: `entrypoints/mcp.py:1725-1729` → `mcp.py:861-871` 이 `**request.model_dump()` 로 넘기고, 확인
  경로로 갈 때도 `model_dump(mode="json")` payload 라 재검증이 통과한다. 빠지는 칸이 없다.
- inventory 의 도구 스키마에도 일곱이 그대로 잡혀 있다(`docs/unified-operations-inventory.json` 의
  `current_runtime.tools[meeting_todo_promote].input_schema.$defs.MeetingTodoPromotionInput`).

**W-5** — 계약 테스트(`tests/contract/test_meeting_promotion_payload.py:13-63`)는 **직행 REST 경로만**
고정한다. 확인 경로(`meeting.todo.promote` operation)는 코드로는 같은 일곱을 싣지만 테스트가 없다 —
두 경로가 갈라지는 회귀를 잡을 그물이 한쪽에만 있다.

참고(이번 dispatch 소관 아님): 직행 경로는 `create_work_request` 를 지나 멱등 키가 **필수**인데
(`modules/work/creation.py:90-102`), 확인 경로는 `_work_requests(session).create` 를 직접 불러 생성
멱등 원장을 지나지 않는다(`application.py:3690`). diff 상 기존 WORK-003 구조이므로 이번 변경의
책임으로 세지 않는다.

---

## 7. 항목 6 — CC 후보 완화 · **PASS**

- 완화는 한 줄이다: `cc_candidates` 가 `_require` → `_require_any(WORK_REQUEST_CREATE, TASK_SELF_MANAGE)`
  (`requests.py:1286-1298`, `_require_any` 는 `requests.py:1349-1353`).
- **담당 후보는 그대로다**: `assignee_candidates` 는 여전히 `WORK_REQUEST_CREATE` 하나다
  (`requests.py:1282-1284`). 단위 테스트가 이 경계를 양쪽에서 못 박는다
  (`tests/unit/test_work_request_cc_candidates.py:38-50` — `work_request.read` 만으로는 거절,
  `task.self_manage` 로 `assignee_candidates` 도 거절).
- 후보 projection 은 손대지 않았다: `member_candidates` 는 재직 중 구성원의 `id`·`display_name` 만 내고
  명부 행을 돌려쓰지 않는다(`platform/organization_access.py:876-891`).
- **조직 외 노출**: `member_candidates` 에는 `organization_scope` 필터가 **없다**(있는 것은
  `work_request_assignee_candidates`, `organization_access.py:863-869`). 그러나 같은 사실이 이미
  `GET /api/organization/members` 로 **아무 인증 principal 에게나** 열려 있으므로
  (`http.py:1210-1212` → `modules/organization_access/application.py:105-115`, 민감 두 칸만 마스킹)
  이번 완화가 **새로 여는 것은 없다**. 보고서의 「조직 외 노출도 없다」는 표현만 부정확하고 결론은 맞다
  → W-4(문구 정정)로만 남긴다.

---

## 8. 항목 7 — 경계·매핑·inventory·경로·테스트

### 7-1. FastAPI/SQLAlchemy 경계 · PASS

- `modules/work/{requests,request_results,request_commands,materials}.py` 와
  `modules/meetings/commands.py` 어디에도 `sqlalchemy`·`fastapi`·`mcp`·`ax_workspace.platform` import 가
  없다(전수 grep). `tests/architecture/test_architecture.py:111-120` 의 규칙을 지킨다.
- `entrypoints/http.py` 의 새 5 route 는 `app.state.workflow_application.*` 만 부른다
  (`http.py:2196-2261`) — `ax_workspace.platform` import 0(`test_architecture.py:129-133`),
  `*Application(` 직접 조립 0(`test_architecture.py:145-168`).
- 저장소 접근은 전부 Protocol 뒤다(`requests.py:79-140` `WorkRequestRepository`,
  `modules/work/materials.py:39-47` `AttachmentRepository`).

### 7-2. 예외 매핑 · PASS

| 도메인 예외 | HTTP | 근거 |
|---|---|---|
| `WorkRequestAccessDenied` | 403 | `http.py:522` |
| `WorkRequestNotFound`(=`ResourceNotFound`) | 404 | `http.py:468` |
| `WorkRequestNotPending` | 409 | `http.py:561` |
| `MaterialNotFound` | 404 | `http.py:516` (`TaskError` 분기보다 **먼저** 선다) |
| `MaterialError`(`kind`·빈 파일·25MB 초과·링크 다운로드) | 422 | `http.py:555` via `TaskError` |
| pydantic `ValidationError`(링크 body) | 422 | `http.py:466` |

순서도 맞다 — `MaterialNotFound` 가 `MaterialError` 하위인데 404 분기가 422 분기보다 위에 있다.

### 7-3. operation inventory · **FAIL (F-1)** — 나머지는 정합

정적 대조 결과(`tests/architecture/test_operation_inventory.py::test_inventory_includes_each_declared_http_operation`
과 `::test_final_inventory_has_no_implicit_or_unverified_product_surface` 의 검사식을 그대로 재현,
테스트 실행 아님):

```
routes(런타임 AST) 156 · inventory rows 156 · 키 156
runtime-only: []      inventory-only: []      field mismatches: 0
current_runtime.http_count == 156  ✓
verified 행 필수필드 누락: []   excluded 행 exclusion 4필드 누락: []
tool_acceptance == registered tools (129 == 129) ✓   tool_count == 129 ✓
```

- 신규 5행은 `current_runtime.added_operations` 에 있고(`docs/unified-operations-inventory.json:71707`,
  `:71730`, `:71750`, `:71773`, `:71796`), `http_handler`·`http_application_calls`·`http_signature` 가
  AST 산출값과 **글자까지 일치**한다.
- `http_count` 156 은 `entrypoints/http.py` 의 `@app.{get,post,put,patch,delete}` 156개와 맞는다.
- `tool_count` 129 는 `modules/ax_execution/tool_catalog.py` 의 `_DEFINITIONS` 129개와 맞고 **도구는 한
  개도 늘지 않았다**. override 는 기존 파일 업로드 route 들과 같은 모양으로 한 줄 추가됐다
  (`bootstrap/operation_inventory.py:60-62`).
- 미검증으로 남긴 것: `test_inventory_schemas_match_the_actual_registered_tools` 는 MCP 서버를 실제로
  띄워 스키마를 비교하므로 **실행하지 않았다**.

> **F-1 (FAIL) — `POST /api/work-requests/{request_id}/materials` 의 `verified` 근거가 실제와 다르다.**
>
> 이 행만 `status: "verified"`, `target_tools: ["file_attachment_request"]` 다
> (`docs/unified-operations-inventory.json:71730-71749`). 그런데 그 도구가 요청 자료에 닿는 길이
> **없다**:
> - `BrowserFileRequest.intent` 는 `Literal['task_material','meeting_material','meeting_material_replace',
>   'folder_material','request_evidence','request_comment_attachment','action_material']` 이고
>   `request_material` 이 **없다**(`modules/ax_execution/browser_interactions.py:42`).
> - 업무 요청을 대상으로 한 업로드는 마지막 분기에서 **무조건 evidence 로 떨어진다**:
>   `bootstrap/browser_interactions.py:144-146` — `request_comment_attachment` 가 아니면
>   `requests.add_evidence(...)` 다. `authorize` 도 `upload_target` → `_evidence_target` 을 지난다
>   (`browser_interactions.py:102-103`, `requests.py:771-776` → `requests.py:754`).
>
> 결과 둘:
> 1. **inventory drift.** 파일 머리의 정의(`note`: "verified means the mapped operation is connected and
>    covered by the named acceptance evidence")를 만족하지 않는다. `acceptance_evidence` 로 적힌
>    `tests/contract/test_work_request_materials.py` 는 `file_attachment_request` 를 한 번도 지나지 않는다.
>    architecture 테스트는 이것을 못 잡는다 — `target_tools` 를 `HTTP_TOOL_TARGET_OVERRIDES` 자신과
>    대조하므로 **자기 자신을 증명하는 검사**다(`test_operation_inventory.py:222-225`).
> 2. **브리프가 금지한 evidence 우회가 AX 표면에서 실제로 일어난다.** 에이전트가 「요청에 자료를
>    붙여라」로 `file_attachment_request` 를 부르면 파일은 요청 자료가 아니라 **현재 회차의 판단
>    근거(evidence)** 로 채택되고, 요청의 `materials` 목록에는 나타나지 않는다.
>
> 정직한 처리는 둘 중 하나다 — 나머지 넷처럼 `E2` 로 `excluded` 하거나(`reconsider_when` 에 intent 신설을
> 적는다), `request_material` intent 를 실제로 만들고 그때 `verified` 로 올린다.

### 7-4. allowed path · PASS

- 이번 변경이 닿은 파일은 전부 허용 경로 안이다: `backend/src/ax_workspace/**`,
  `backend/tests/{contract,unit}/**`, `docs/unified-operations-inventory.json`.
- `frontend/` 미개입을 **증거로** 확인했다: `frontend/src/features/work/WorkModals.tsx:3358` 이 아직
  `REQUEST_MATERIALS_SAVED = false` 이고, `frontend/src/lib/api.ts` 에 새 5 endpoint 호출이 하나도 없다
  (`work-requests/...` 호출 목록에 `materials` 없음). 즉 FE 는 이 계약을 아직 안 쓴다.
- `docs/domain-model.md` 는 diff 전량이 W2 판단 통합·`task_proposals`·`work_request_list_entries` 등
  **기존 WORK-003 문서 작업**이고, 요청 자료·`work_request` binding context 를 언급하는 줄이 **없다** →
  이번 dispatch 가 건드리지 않았다(브리프 지시대로). 후속으로 「`attachment_bindings.context_type` 에
  `work_request` 가 늘었다」를 문서에 반영할 필요는 남는다.
- 새 migration 파일 0, `persistence.py` 에 자료 관련 추가 0(§2).

### 7-5. 테스트 존재 · PASS (공백은 W-5)

브리프가 지정한 6 흐름이 6 함수로 있고 중복·전수 조합이 없다:
`tests/contract/test_work_request_materials.py`(4) · `tests/contract/test_meeting_promotion_payload.py`(1) ·
`tests/unit/test_work_request_cc_candidates.py`(1). 수락 이중 바인딩은 **DB 행으로** 못 박았다
(`test_work_request_materials.py:118-128`) — projection 만 보는 얕은 검증이 아니다.

---

## 9. 항목 8 — checkout 사고와 inventory 복구 · **WARN (W-1)**

**W-1 (사실 기록).** 워커는 금지된 `git checkout docs/unified-operations-inventory.json` 을 **한 번
실행했고**, 그 파일이 `M` 상태임을 알면서 되돌렸다고 스스로 보고했다(구현 보고서 §0). 이것은 PASS 근거가
아니라 절차 위반 사실이다.

**복구 여부는 현재 파일로 확인했다 — 복구된 것으로 보인다.** 근거(전부 정적):

1. §7-3 의 정적 대조가 전 항목 0 drift 다. 특히 `POST /api/work-requests/{request_id}/read` 행이
   사람이 쓴 산문 3필드(`reason`·`alternative`·`reconsider_when`)와 함께 살아 있다
   (`docs/unified-operations-inventory.json:71698-71703`) — 이 행이 유실 목록 중 유일한 **수작업** 항목이었다.
2. 기계 생성분도 **현재 런타임 모양**이다: `tools[work_request_create].input_schema` 에 WORK-003 이
   더한 `start_date`·`project_id`·`preceding_task_ids`·`approver_id` 가 있고,
   `tools[task_create_self]` 도 같다. `tools[meeting_todo_promote]` 의 `$defs` 에는 **이번에 더한 일곱과
   새 docstring** 이 그대로 잡혀 있다 → 캡처가 변경 이후에 다시 생성됐다.
3. `tool_count`·`tools`·`tool_acceptance` 가 129 로 삼자 일치하고 `_DEFINITIONS` 129 와도 맞는다.

**남는 한계**: 도구 스키마 본문의 전수 일치는 런타임 비교가 필요해 **확인하지 않았다**. 워커가 인용한
`test_operation_inventory.py` 4 passed 는 워커의 보고이고 이 리뷰가 재현한 것이 아니다.

**4 failed 의 인과**(워커가 「확정 못 함」으로 남긴 것) — 코드로 좁힌 결과 **이번 변경 때문일 가능성은
낮다**:
- 실패한 `test_material_search` 두 건은 업무와 파일만 만들고 **업무 요청을 한 건도 만들지 않는다**
  (`tests/contract/test_material_search.py:295-310`). 넓어진 `material_bindings()` 는 요청이 있을 때만
  행을 더하므로 그 시험의 자료 집합을 바꾸지 않는다.
- `resource_type='task'` 로 좁힌 검색은 `kinds` 가 `{'task'}` 로 줄어
  (`modules/work/material_search_policy.py:44-46`) 요청 갈래를 **아예 타지 않는다**
  (`bootstrap/material_sources.py:75`).
- 검색은 attachment id 로 중복을 접으므로(`modules/work/material_search.py:71-73`) 수락 뒤 두 자리에
  선 자료가 결과를 두 번 내지도 않는다. 링크 자료는 `projectable` 이 아니어서 backfill 도 안 걸린다
  (`material_search_policy.py:72-74`).
- 다만 **실행해 보지 않았으므로 배제했다고 말하지 않는다.** baseline 비교가 여전히 유일한 확정 방법이다.

---

## 10. FAIL · WARN 목록

### FAIL

- **F-1 — inventory 가 없는 AX 매핑을 `verified` 로 주장한다 (§7-3).**
  `docs/unified-operations-inventory.json:71730-71749` ↔
  `backend/src/ax_workspace/modules/ax_execution/browser_interactions.py:42` ·
  `backend/src/ax_workspace/bootstrap/browser_interactions.py:144-146`.
  부수 효과로 AX 표면에서 요청 자료 업로드가 **evidence 로 떨어진다**(브리프가 금지한 우회).

- **F-2 — 링크 자료를 레거시 첨부 다운로드로 열면 500 이다.**
  `material_bindings()` 가 이제 요청 자료를 함께 낸다(`backend/src/ax_workspace/modules/work/requests.py:1013-1021` (`bindings = list(self._material_bindings_for(request))`)).
  그 목록을 쓰는 `open_attachment` 는 `source_kind` 검사 없이 바로 저장소를 읽는다
  (`requests.py:1045` `self._storage.get(attachment.source_ref)`). 링크 attachment 의 `source_ref` 는
  URL 이라 `LocalDirectoryMaterialStorage._path` 의 `_SAFE_KEY` 가 걸러 `ValueError("invalid material
  storage key")` 를 던지고(`backend/src/ax_workspace/platform/materials.py:23-25`), `_runtime_error` 에
  그 분기가 없어 **그대로 재발생 → 500** 이다(`entrypoints/http.py:575`).
  변경 전에는 이 집합에 파일 첨부만 있었으므로(댓글 첨부·evidence 는 `store_file` 산출물) **이번
  변경이 새로 연 경로다.** 같은 일을 하는 새 route 는 제대로 422 를 낸다
  (`requests.py:866-867`) — 두 입구의 답이 다르다.
  하필 inventory 가 이 route 를 요청 자료 다운로드의 **대안**으로 적어 두었다
  (`unified-operations-inventory.json:71785-71787`).

### WARN

- **W-1 — 금지된 `git checkout` 실행(§9).** 복구는 현재 파일에서 확인됐으나 절차 위반 사실은 남는다.
  도구 스키마 전수 일치는 런타임 비교 미실시로 미검증.
- **W-2 — 요청 투영이 목록·수신함에서 요청당 쿼리 4개를 더 쏜다(§5).** `_material_views` 안의
  `_derived_task_id`(`requests.py:966`)는 `_view` 가 이미 가진 값을 다시 묻는 **순수 중복**이다.
- **W-3 — 자료를 붙이고 떼는 길만 요청 행을 잠그지 않는다.** `_material_writer`(`requests.py:891`)는
  `_participant_request` → `self._repository.request(request_id)` 로 **lock 없이** 읽고
  `_material_moved`(`requests.py:979-988`)에서 `request.version += 1` 한다. 같은 파일의 다른 변경 경로는
  전부 `lock=True` 다(`requests.py:536`·`618`·`660`·`758`·`1329`). 동시에 두 자료를 붙이면 회차 증가가
  하나 사라질 수 있고, 그러면 받는 사람이 **바뀐 요청을 stale 없이 수락한다**. 덤으로
  `add_evidence`(`requests.py:778-807`, `request.updated_at = datetime.now(UTC)`)와 달리 `updated_at` 을 갱신하지 않는다(`requests.py:979-988`).
- **W-4 — 입양이 업무 쪽에 흔적을 남기지 않는다(§4 관찰).** `task.version` 미증가 ·
  `task.material_attached` 활동 미기록(`requests.py:989-1011`).
- **W-5 — 승격 확인(action) 경로에 계약 테스트가 없다(§6).** 직행만 고정돼 있다.
- **W-6 — 보고서 문구 두 곳이 코드보다 강하다.**
  ① 「조직 외 노출도 없다」 — `member_candidates` 에는 org-scope 필터가 아예 없다
  (`platform/organization_access.py:876-891`). 결론(새 노출 없음)은 맞지만 이유가 다르다: 같은 명부가
  이미 `GET /api/organization/members` 로 열려 있어서다.
  ② `attach_material_link` 는 같은 URL 이면 **남이 만든 attachment 행을 그대로 재사용한다**
  (`platform/work_tasks.py` 의 `SqlAlchemyAttachmentRepository.add_link` — 같은 `source_ref` 행이 있으면 그것을 그대로 돌려준다) → 요청 자료의 `uploaded_by` 가 그 요청과
  무관한 제3자로 보일 수 있다. 업무 링크의 기존 설계지만 요청 표면에서는 처음 드러난다.
- **W-7 — 죽은 코드 1개.** `WorkRequestMaterialLinkCommand`
  (`backend/src/ax_workspace/modules/work/request_commands.py:44`)를 부르는 곳이 없다. 형제
  `WorkRequestCommentCommand` 는 실제로 쓰인다(`platform/actions.py:742`) — 이쪽만 미사용이고, 요청
  자료에 action/MCP 표면이 없다는 E2 결정과 일관되므로 지우는 편이 낫다.

---

## 11. 권고 (코디네이터 판단용)

1. **F-1**: inventory 한 행을 E2 `excluded` 로 내리거나 `request_material` intent 를 신설한다. 전자가
   이번 범위에 맞다 — `tool_count` 도 그대로다.
2. **F-2**: `open_attachment` 에 `open_material` 과 같은 `source_kind != "file"` 가드 한 줄
   (`requests.py:1044` 앞). 링크 자료 하나로 재현되는 계약 테스트 1개면 충분하다.
3. **W-3**: `_material_writer`(`requests.py:891-906`)가 `self._repository.request(request_id, lock=True)` 로
   잠근 뒤 참여자 판정을 하도록 바꾼다 — 나머지 변경 경로와 같은 모양이 된다.
4. **W-2**: `_material_views(request, *, task_id=None)` 로 호출자가 이미 가진 `derived` 를 넘긴다.
5. **W-1**: 확정하려면 도구 스키마 전수 일치 테스트(`make test-unit` 의 architecture 4건)를 **리뷰
   밖에서** 한 번 더 돌린 결과가 필요하다. 이 리뷰는 테스트를 실행하지 않았다.


---

## 12. 이 리뷰가 확인하지 못한 것 (WARN 으로 명시)

- **테스트를 한 건도 실행하지 않았다.** `make test`·`make test-unit`·`make test-contract`·
  `make test-postgres` 모두 미실행이다. 워커가 보고한 수치(6 passed · 349 passed · 1075 passed/4 failed,
  architecture 4 passed)는 **워커의 보고이지 이 리뷰의 재현이 아니다.**
- **MCP 도구 스키마 전수 일치**(`test_inventory_schemas_match_the_actual_registered_tools`)는 런타임
  서버 기동이 필요해 확인하지 않았다 → W-1 에 포함.
- **4 failed 의 인과**는 코드로 「이번 변경 때문일 가능성이 낮다」까지만 좁혔고 배제하지 못했다(§9).
- 일부 인용 줄번호는 함수 범위로 적었다 — 함수 이름과 파일은 전부 직접 읽어 확인한 것이다.
