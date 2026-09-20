# 리뷰 리포트 — strong-hajin-work / backend+frontend 통합 (2026-09-16)

## 판정: FAIL

FAIL 사유는 **1건**이다 — 생성 창이 내는 「시작일」과 horizontal 생성 경로의 422 거절이 어긋나
일반 구성원의 W1 핵심 동선(#7 W1.5)에서 사용자가 하드 에러를 만난다. 그 밖에는 계약이 대체로
서 있고, 테스트 이관은 단언을 줄이지 않았다. 나머지는 WARN 7건 · 기존 부채 4건이다.

**주의** — 이 판정은 **코드 검수**다. `make verify` 는 코디가 실행 중이고, 이 리포트의 어떤 항목도
실행 통과를 뜻하지 않는다. 브리프 §7 대로 테스트·빌드·DB·E2E 를 하나도 돌리지 않았다.

---

## 검수 범위

- base `origin/main`(= `8973791`). **커밋 diff 는 비어 있고 전부 워크트리 미커밋 변경**이다
  (`git diff --stat origin/main...HEAD` 0줄).
- 변경: tracked 79개 파일 (BE 62 · FE 13 · docs 4) + untracked 4개 소스
  (`modules/work/creation.py` · `creation_commands.py` · `tests/contract/test_task_creation_contract.py` ·
  `tests/legacy_acceptance.py`).
- 사용자 파일 **보존 확인** (읽기만): `definition.md`(16810B) · `lifecycle.md`(21963B) ·
  `정의_v2.md`(2382B) · `example.md`(0B, 원래 빈 파일) · `docs/work-code-db-audit-2026-09-16{,-manifest.json,
  -schema.json,-head-tests.txt,-working-tests.txt}` 5개 전부 존재. FE 13개 파일도 그대로 diff 에 살아 있다 —
  BE 의 `git stash push -u`/`apply` 로 유실된 것은 없다.
- 실행한 검사: `git diff`·`git show HEAD:<f>` 대조, 테스트 함수명 전수 diff(구/신), grep,
  `git blame`. **테스트·빌드·DB·E2E 는 돌리지 않았다.**

---

## 위반 (FAIL)

### F-1. 생성 창이 「시작일」을 내는데 horizontal 생성은 그 값을 422 로 거절한다 — P0

- `frontend/src/features/work/WorkModals.tsx:2509` — `start_date` 필드는 `directTaskContract.fields` 에
  **무조건** 들어간다. 담당을 남으로 골랐는지와 무관하다(`project_id`·`reference_task_ids` 는
  `...(!assignTarget ? [...])` 로 걷었는데 `start_date` 만 걷지 않았다).
- `frontend/src/features/work/WorkModals.tsx:2602-2610` — horizontal 갈래가 그 값을 그대로 싣는다
  (`start_date: startDate || undefined`, `assignee_id: assignTarget.id`).
- `backend/src/ax_workspace/modules/work/creation_commands.py:141,152-166` —
  `_refuse_unsupported_horizontal_fields` 가 `start_date`·`parent_task_id`·`project_id` 중 하나라도
  `None` 이 아니면 `TaskError` → `http.py:503` 매핑으로 **422**.
- **재현**: 배정 권한 없는 일반 구성원(민아) 계정 → `[업무 만들기]` → 담당에서 동료 선택
  (그 사람은 `assignCandidates` 가 비어 있어 **언제나 horizontal**) → 시작일 입력 → 생성
  → 「담당을 지정한 생성에는 쓸 수 없는 항목입니다: start_date」. W1 의 대표 동선이 막힌다.
- 근거: SPEC-001 §6 W1 인수조건 「화면·REST·MCP·AX 가 같은 계약을 쓴다」 ·
  WORK-001 Phase 7 「생성 창에 담당 필드를 연다 … 기존 부품만 쓴다」 ·
  `w1-fe-api-clarification.md` §3 「기존 일정 필드를 유지」.
- **양쪽 다 테스트가 없다.** BE: `grep -rn "쓸 수 없는 항목" backend/tests` → 0건
  (`_refuse_unsupported_horizontal_fields` 를 덮는 테스트가 하나도 없다).
  FE: `CreateWork.test.tsx` 의 horizontal 테스트(`:429`)가 시작일을 채우지 않는다.
- 권장 수정(택1, FE 쪽이 계약에 맞다):
  - **(권장)** `WorkModals.tsx:2509` 를 `...(routeFor(taskOwnerId) === "horizontal" ? [] : [start_date])`
    로 바꿔 horizontal 대상일 때 줄 자체를 세우지 않는다(`project_id` 와 같은 방식). 그리고
    `:2602` 갈래에서 `start_date` 를 싣지 않는다. 회귀 테스트 1건(시작일 입력 후 수신 후보 선택 →
    필드 사라짐 · 전송 payload 에 `start_date` 없음)을 더한다.
  - 대안: BE 가 `start_date` 를 받아 `create_task_for_request` 로 흘려보낸다 — 단 `work_requests` 에
    해당 열이 없어 SPEC 변경이 필요하므로 **W1 범위 밖**이다. 코드로 발명하지 말고 planner 에 올릴 것.
  - 어느 쪽이든 BE 에 `_refuse_unsupported_horizontal_fields` 계약 테스트(3필드 × 422 + 업무 0건)를 더한다.

---

## 경미 (WARN)

### W-1. AX 확인 실행이 horizontal 갈래에서 `source_*` 계보를 **조용히 버린다** — P1

- `backend/src/ax_workspace/modules/work/creation_commands.py:94-97,126-149` —
  `create_task` 는 `source_action_item_id`·`source_decision_item_id`·`source_submission_id`·
  `source_review_decision_id` 를 인자로 받지만 **`self` 갈래에서만** `create_self` 로 넘긴다.
  horizontal 갈래(`:141-149`)는 `self._requests.create(...)` 를 부르며 넷을 전혀 전달하지 않는다.
- 도달 경로: `platform/actions.py:820-829` 가 `task.create_self` 확정 실행에서 저 넷을 싣고
  `create_task` 를 부른다. 그리고 `modules/work/drafts.py:12` `TASK_DRAFT_FIELDS =
  frozenset(TaskCreateInput.model_fields)` 이라 **`assignee_id` 가 AX 초안의 편집 가능 필드로 자동 편입**됐다
  (`entrypoints/mcp.py:1843` 도구 인자로도 열려 있다). 사람이 초안에서 담당을 지정하고 확인하면
  horizontal 로 가고, 그 업무는 자기를 만든 AX action 을 가리키지 않는다.
- 같은 파일 `:153` 이 「받지 않는 값은 **조용히 버리지 않고** 거절한다」고 적어 두고 여기서는 버린다 —
  스스로 세운 원칙과 어긋난다. WORK-001 invariant 9 「행위자·출처 보존」 위반 소지.
- 권장: horizontal 갈래에서 넷 중 하나라도 들어오면 (a) 요청/업무에 실어 보내거나
  (b) `_refuse_unsupported_horizontal_fields` 처럼 명시 거절. 테스트 1건.

### W-2. 요청 출신 업무의 `created_by_actor_id`·최초 version actor 가 **담당자**다 — P1 (감사 사실 오류)

- `backend/src/ax_workspace/platform/work_tasks.py:1273` `created_by_actor_id=request.assignee_id`,
  `:1320` `tasks.capture_version(task, request.assignee_id, "task.created")`.
- W1 **이전에는 참이었다** — 담당자가 수락하는 행위로 업무가 섰다. W1 이후 그 업무를 만든 것은
  요청자의 명령이고 담당자는 아무 행위도 하지 않았다. 즉 **이 diff 가 그 칼럼을 거짓으로 만들었다.**
- 파급: `docs/domain-model.md:54` 가 「`tasks.created_by_actor_id`가 유일한 actor 칼럼이다」라고
  단정하는데 이 경로에서는 actor 가 아니다. `GET /api/tasks/{id}/history` 의 첫 version 이
  `actor_id=<담당자>` · `change_kind="task.created"` 로 나간다 — 하지 않은 일을 한 것으로 읽힌다.
- 권한 영향은 **없다**: `modules/work/application.py:433` 의 fallback 은 활성 담당이 없을 때만 쓰이는데
  이 경로는 언제나 활성 담당이 있다. 출처 행위자도 `origin.actor`(요청자)로 정확히 나온다
  (`test_task_creation_contract.py:379` 가 고정). 그래서 **기능 버그가 아니라 감사 사실 오류**다.
- 테스트가 낡은 뜻을 **못 박고 있다**: `backend/tests/contract/test_task_actor.py:66-73` 이
  주석 「The acceptance created the Task」를 그대로 둔 채 `row.created_by_actor_id == "jiho"` 를 단언한다.
  수락이 없어진 자리에 남은 문장이다.
- 권장: `created_by_actor_id=request.requester_id`(+`capture_version(..., request.requester_id, ...)`)로
  바꾸고 `test_task_actor.py` 단언·주석을 함께 고친다. 열람 판정에 닿아 있으니
  `_may_read_beyond_holding` 회귀 테스트를 같이 본다. BE 보고 §5-③ 이 「W1 에서 바꾸지 않았다」고
  적었으나, 바꾸지 않은 결과가 **새로 생긴 거짓**이므로 그대로 두려면 코디가 명시로 유예해야 한다.

### W-3. README 의 「과거 pending 명령은 `work_request.decide` 를 요구한다」가 실제 코드와 다르다 — P1

코디가 지적한 대로다. 소스 확인 결과:

| 명령 | 실제 역량 | README:116 주장 |
|---|---|---|
| `POST /api/work-requests/{id}/accept` | `work_request.decide` (`requests.py:296`) | ✅ |
| `…/reject` | `work_request.decide` (`requests.py:311`) | ✅ |
| `…/negotiate` | `work_request.decide` (`requests.py:333`) | ✅ |
| `…/resubmit` | **`work_request.create`** (`requests.py:454`) | ❌ |
| `…/withdraw` | **`work_request.create`** (`requests.py:496`) | ❌ |
| `POST /api/task-assignments/{id}/accept` | **`task.self_manage`** (`assignments.py:221`) | ❌ |
| `POST /api/task-assignments/{id}/decline` | **`task.self_manage`** (`assignments.py:232`) | ❌ |
| 배정 취소(`cancel`) | **`task.assign`** (`assignments.py:251`) | ❌ |

- `README.md:116` 「그 명령들은 여전히 `work_request.decide`를 요구하며」— **5/8 이 틀리다.**
  WORK-001 Phase 3 이 고정한 것은 「과거 pending **요청**의 수락·거절·조정이 `work_request.decide` 를
  계속 요구한다」이고(`requests.py:290·305·327` 인용), 배정·재상신·철회는 처음부터 다른 역량이었다.
- 권장: 「요청의 수락·거절·조정은 `work_request.decide`, 재상신·철회는 요청자의 `work_request.create`,
  배정 수락·거절은 담당자의 `task.self_manage`, 배정 취소는 `task.assign`」로 갈라 적는다.

### W-4. domain-model 의 「판단 API」 bullet 이 **살아 있는 AX 승인 경로**까지 과거 행 전용으로 묶는다 — P1

- `docs/domain-model.md:52` — 남은 kind별 endpoint 셋을 나열하고 「이 endpoint들은 **과거 행을 위해
  남아 있다**」로 묶었다. 그런데 그 목록의 `POST /api/actions/{id}/decide`(`entrypoints/http.py:1135`)는
  **신규 AX 제안의 사람 승인 경로**이고 W1 이 그대로 유지하기로 한 것이다
  (SPEC-001 §6 「AX 실행 확인이 남아 있고 확인 전에는 effect 가 없다」 ·
  `test_action_center.py:295`·`:998` 등이 지금도 이 라우트로 확정한다).
- `…/resubmit` 도 요청자의 재상신 경로라 「과거 행 전용」 묶음이 정확하지 않다(과거 회차에만 걸리는 것은
  맞지만 권한·행위자가 다르다 — W-3).
- 권장: 「과거 행을 위해 남아 있다」의 적용 범위를
  `POST /api/work-requests/{id}/accept|reject|negotiate` 와 `POST /api/task-assignments/{id}/accept|decline`
  로 한정하고, `POST /api/actions/{id}/decide` 는 **신규 AX 확인의 현행 경로**로 따로 적는다.

### W-5. 회의 승격 문서의 라우트·표 이름이 실재하지 않는다 — P2 (사전 drift, 수정한 줄에 실림)

코디가 「제품 문서에 없는 회의 승격 라우트」로 물은 항목이다. 검수 결과:

- `docs/domain-model.md:55` 가 API 로 `POST /api/meetings/{id}/summaries/{summary_id}/statements/{index}/promote`
  를, 중복 방지 근거로 `meeting_followup_promotions` 의 unique 를 든다.
  **둘 다 코드에 없다** — `grep -rn "statements/{" entrypoints/http.py` 0건,
  `grep -rn "meeting_followup_promotions" src/` 0건. 같은 문서 `:143` 이 그 표를
  **2026-09-10 에 제거했다**고 스스로 적는다.
- 실제 live 경로는 `POST /api/meetings/{id}/todos/{todoId}/promote` 하나이고(`http.py:738`),
  「같은 후보 한 건」은 `meetings/application.py:851-861` 의 `_readable(lock=True)` + `todo(lock=True)` +
  `ensure_todo_actionable(linked_work_request_id)` 가 세운다. **후보 잠금 층은 실재한다** —
  WORK-001 Phase 5 의 두 층 요구는 만족한다. 틀린 것은 문서가 지목한 **기전의 이름**뿐이다.
- 판정: **사전 drift**(BE docs 워커가 code-docs-report §6-① 로 정직하게 보고했다). 다만 이번 diff 가
  그 줄을 고치면서 새 W1 주장(「같은 멱등 계약」)을 존재하지 않는 표 위에 얹었으므로, 같은 줄에서
  라우트·표 이름을 `todos/{todoId}/promote` · `meeting_todos.linked_work_request_id` 로 바로잡는 것이 맞다.
  코드 변경은 필요 없다.

### W-6. 신규 `assigned` 요청은 **근거(evidence) 첨부를 아예 받지 못한다** — 제품 결정이 어디에도 기록되지 않았다 — P2

- `modules/work/requests.py:596-598` `_evidence_target` 이 `current_submission` 이 없으면
  `WorkRequestError("work request has no submission to attach evidence to")` → 422.
  신규 경로는 Submission 을 만들지 않으므로 **모든 신규 요청에서 `POST /api/work-requests/{id}/evidence`
  가 영구히 422** 다.
- 동작 자체는 clarification 요구를 지킨다: 정의된 4xx 이고 side effect 가 없다
  (`store_file` 앞에서 막힌다). `test_task_creation_contract.py:352-367` 이 422 + `AttachmentRecord` 0건 +
  감사 이벤트 `work_request.created` 하나만을 단언한다. FE 도 광고하지 않는다
  (`WorkModals.tsx:1724` `canAdoptEvidence = … && request.state === "pending"`).
- 그러나 **제품 기능 하나가 신규 경로에서 사라진 사실**이 BE 보고에도, `docs/domain-model.md:132`
  EVIDENCE 행에도 없다. 「생성 입력으로 수용한 자료·참조·설명·출처」(체크리스트·참고 업무·설명·출처
  두 열)는 `work_tasks.py:1314-1319` 로 보존되므로 clarification 이 지킨 것은 지켰지만,
  **요청에 파일을 붙이는 길**은 신규에서 없어졌다.
- 권장: 코드 변경 없음. `docs/domain-model.md` EVIDENCE 행에 「신규 `assigned` 요청에는 회차가 없어
  채택 대상이 없다 — 파일은 업무 쪽 자료로 붙인다」를 한 줄 적고, 제품 판단이 필요하면 planner 로 올린다.

### W-7. 기계적 일괄 치환 흔적 · 낡은 주석 · 무의미해진 테스트 호출 — P3

- **`== "` → `=="` 172줄.** HEAD 에는 0건이던 공백 없는 비교가 4개 파일에 새로 생겼다:
  `test_action_center.py`(91) · `test_mcp_action_items.py`(45) · `test_request_amendment.py`(21) ·
  `test_evidence_continuity.py`(15). 예: `test_evidence_continuity.py:159`
  `assert decision["reason"] =="근거를 더 주세요"`. 동작에는 영향이 없고 이 레포에 린터 설정이 없어
  규칙 근거는 없지만, **테스트 파일에 일괄 sed 가 돌았다는 신호**라 diff 를 읽는 사람에게 잡음이다.
- **자기모순 주석**: `platform/work_tasks.py:313` 「위반을 SAVEPOINT 안에서 받는다」 ↔
  `:336` 「**SAVEPOINT 로 받지 않는다**」. 실제 구현은 후자다(`:336` 이 맞다). `:313` 을 지운다.
- **낡은 주석**: `platform/persistence.py:974` 가 `command_kind` 값으로
  「`task.create` · `task.assign` · `meeting.followup.promote`」를 드는데, 실제 상수는
  `creation.py:33-35` 의 `task.create` · `task.assign` · **`work_request.create`** 다.
- **무의미해진 호출**: `test_task_origin.py:77`·`:246` 이 `POST /api/task-assignments/{id}/accept` 를
  응답 확인 없이 부른다 — 지금은 422 no-op 인데 테스트는 그대로 통과한다. 지우거나 422 를 단언한다.
- **얕은 단언**: `test_action_center.py:867` `assert refused.status_code in {403, 404, 422}` —
  clarification 이 요구한 「정의된 4xx」를 세 값의 집합으로 받는다. 어느 하나로 고정하는 쪽이 낫다.
- **키 누락 경계 미검**: `test_task_creation_contract.py:107-127` 이
  `POST /api/tasks`·`/api/work-requests`(헤더 없음·공백) · `/api/tasks/assign`(빈 문자열만) ·
  MCP `create_self_task`·`create_work_request` 를 덮는다. **미검**: `/api/tasks/assign` 헤더 누락,
  `POST /api/meetings/{id}/todos/{id}/promote` 누락·공백, MCP `assign_task`·`promote_current_meeting_todo`.

---

## 집중 확인 항목별 판정 (브리프 §4)

### ① `tests/conftest.py` 자동 키 삽입이 누락·공백 검증을 가리는가 → **가리지 않는다 (PASS)**

- `backend/tests/conftest.py:23-37` — `TestClient.request` 를 monkeypatch 해 **POST 이고 헤더가 없을 때만**
  `f"test-{uuid4()}"` 를 채운다. **호출마다 새 uuid** 이므로 두 POST 가 한 건으로 합쳐지는 일이 없다 —
  「중복을 감춰 주지 않는다」는 BE 주장은 코드상 맞다.
- 밀어내는 길이 둘 다 실재한다: `@pytest.mark.no_auto_idempotency_key`(`pyproject.toml:44` 에 등록,
  `test_task_creation_contract.py:106` · `test_meeting_rooms.py:291` 에서 사용)와 헤더 직접 지정.
- 실제 HTTP 실패 경계는 `test_task_creation_contract.py:107-127` 이 마커로 fixture 를 끄고 검증한다.
  MCP 는 TestClient 를 지나지 않으므로 fixture 와 무관하고 같은 테스트가 facade 를 직접 부른다.
- **남는 위험**: 라우트에서 `Idempotency-Key` 요구가 사라져도 위 한 테스트 말고는 아무도 깨지지 않는다.
  현재 그 한 테스트가 네 표면 중 셋을 덮는다(W-7 의 미검 목록 참조). 커버리지를 넓히면 좋으나
  **가림은 아니다.**

### ② `tests/legacy_acceptance.py` 가 회귀를 숨기는가 → **숨기지 않는다 (WARN 없음, 조건부 PASS)**

- 신규 파일 145줄, **테스트 전용**. `pending_request` · `make_request_look_pending` ·
  `pending_assignment` · `make_assignment_look_pending` 넷. 24개 테스트 파일이 쓴다.
- 제품 코드에 복원 경로·fallback 은 **없다**: `grep -rn "legacy_acceptance" backend/src` → 0건.
  `make_assignment_look_pending:133` 이 부르는 `_open_assignment_acceptance` 는 **담당자 변경**이 계속 쓰는
  살아 있는 코드이지 W1 이 되살린 것이 아니다.
- **단언이 줄지 않았음을 객관 확인**: 수정된 test 파일 전체에서 테스트 함수명을 구/신 전수 비교했다.
  - HEAD 453개 → 현재 457개.
  - **사라진 12개는 전부 같은 파일에 대체 이름으로 다시 섰다** (아래 표). **대체 없이 삭제된 테스트 0건.**
  - 신규 순증: `test_task_creation_contract.py` 22개 + PG 3개 + 분할 1개.
- clarification 이 금지한 「파일 전체 일괄 삭제」·「같은 '회차 0건' 단언으로 모두 대체」는 **없다**:
  `test_action_center.py` 는 38개 테스트를 유지한 채 legacy fixture 로 갈아탔고(`+152/-173`),
  `test_evidence_continuity.py` 는 근거 동결·상속·해시 단언을 **한 줄도 지우지 않고** 세팅만 바꿨다.
- 「테스트가 상태를 조작해 회귀를 숨기는가」 → 숨기는 구조가 아니다. 신규 경로의 동작은
  `test_task_creation_contract.py`(22건) + `test_task_assignments.py` + `test_decision_continuity.py:27`
  + `test_product_operations.py:475` 가 **신규 POST 로** 따로 검증하고, legacy fixture 는
  **과거 행의 판단 회차 코드**만 덮는다. 두 축이 분리돼 있다.
- 다만 `_erase_task`(`:34-48`)가 `Base.metadata` 를 훑어 tasks FK 를 가진 모든 행을 지운다 —
  `task_creation_attempts` 행도 함께 지워진다. 지금은 문제가 없으나, 이 helper 가 언제나
  「예전 배포가 남긴 모양」과 정확히 같지는 않다는 점은 기록해 둘 가치가 있다.

**폐기·대체 대응표 (전수, 기계 대조 결과 — BE 보고 §3 과 일치)**

| 사라진 이름 | 같은 파일의 대체 | 계약 변화 |
|---|---|---|
| `test_ax_task_assignment_uses_the_same_editor_but_keeps_assignee_acceptance_separate` | `…_and_stands_at_once` | 편집 계약·preview 단언 유지, 뒤가 즉시 활성 담당 + 수락 0건 |
| `test_ax_task_assignment_can_be_cancelled_by_the_requester_only_before_acceptance` | `test_a_confirmed_ax_assignment_offers_no_withdrawal_because_it_already_stands` | 봉투가 명령을 내지 않음 + 직접 호출 4xx + side effect 0 |
| `test_request_opens_thread_subject_submission_and_assignment` | `test_a_new_request_opens_a_thread_and_a_task_but_no_judgement_round` **+** `test_a_past_pending_request_keeps_its_round_and_its_reviewer` | 하나를 둘로 갈랐고 과거 행 단언은 원문 그대로 |
| `test_accepting_the_request_carries_the_source_columns_onto_the_task` | `test_the_promoted_request_carries_the_source_columns_onto_the_task` | 출처 두 열 단언 유지, 수락 단계만 제거 |
| `test_accepting_a_promoted_request_still_carries_the_meeting_onto_the_task` | `test_a_promoted_request_carries_the_meeting_onto_the_task_at_once` | 동상 |
| `test_work_request_creates_a_task_only_after_the_assignee_accepts` | `test_work_request_creates_a_task_without_waiting_for_the_assignee` | `assigned` + `task_id` + 판단함 0건 |
| `test_declined_assignment_never_enters_my_work_and_records_the_reason` | `test_a_new_assignment_takes_no_acceptance_or_decline_command_and_nothing_changes` | 422 + side effect 0 (DEC-001 D-4) |
| `test_direct_task_and_accepted_request_carry_an_active_assignment` | `…_and_sent_request_…` | 판단·판정 0건 단언 **추가** |
| `test_manager_assignment_enters_my_work_only_after_the_assignee_accepts` | `test_manager_assignment_enters_my_work_at_once` | 즉시 목록·즉시 시작 + lineage null |
| `test_request_due_date_flows_into_the_accepted_task` | `…_into_the_requested_task` | 수락 단계만 제거 |
| `test_accepting_the_same_request_twice_creates_exactly_one_task` | `test_resending_the_same_request_creates_exactly_one_task` | 같은 키 재전송 → 요청·업무 1건 |
| `test_an_accepted_request_names_the_requester_and_survives_a_new_session` | `test_a_sent_request_names_…` | 출처 단언 그대로 |

**잃은 단언 1건 (P3)**: 구 `test_manager_assignment_enters_my_work_only_after_the_assignee_accepts` 의
「보낸 사람이 남의 수락 명령을 부르면 404(존재 은닉)」가 대체 테스트에 없다.
`test_legacy_assignment_confirmation.py:38`(무수정)이 canonical command 경로에서 같은 취지를 422 로 덮으므로
공백이 완전하지는 않으나, `POST /api/task-assignments/{id}/accept` 의 404 은닉은 이제 무검증이다.
`legacy_acceptance.pending_assignment` 로 1건 복원 권장.

### ③ `actor=담당자` 잔존이 계약 위반인가 → **감사 사실 위반 (W-2). 권한 위반은 아니다.**

위 W-2 참조. 요약: 권한·기능에는 영향이 없고 출처 행위자는 `origin.actor` 로 정확히 나오지만,
`tasks.created_by_actor_id` 와 최초 version 의 `actor_id` 가 **아무 행위도 하지 않은 사람**을 가리키게 됐고
그 거짓은 **이번 diff 가 만들었다**. 문서(`domain-model.md:54`)의 단정과도 어긋난다.

### ④ `meeting.followup.*` AX action 의 AttributeError → **기존 부채가 맞다. 범위 제외 타당.**

실제 호출 연결을 끝까지 따라갔다.

- `platform/actions.py:757` → `self._services.meeting_followups().promote(...)`.
- `bootstrap/application.py:4054` → `meeting_followups=lambda: self._meeting_followups(session)`.
- **`WorkflowApplication._meeting_followups` 정의가 없다** (`grep -n "_meeting_followups"` → 4054 한 줄뿐).
- `MeetingFollowupApplication.promote` 가 부르는 `MeetingApplication.followup_candidate` ·
  `record_followup_promotion` 도 **정의가 없다** (`grep -rn "def followup_candidate\|def record_followup_promotion" src` → 0건).
- `git blame`: `application.py:4054` 도 `actions.py:757` 도 **`69dc2376` (2026-09-13)** — base `8973791` 이전이다.
  두 줄 모두 이번 diff 에 없다.

→ `meeting.followup.task` · `meeting.followup.request` 는 **W1 이전부터 실행 불가**다.
W1 이 만든 것도, W1 이 고쳐야 할 것도 아니다. BE 가 `followups.py` 를 새 계약 위로 올려 둔 것
(`followups.py:28,46-57`)은 조립을 붙이지 않았으므로 동작 변화가 없다 — 다만 생성자 인자가 5개로
늘었으니(`:22-32`) 훗날 되살릴 때 `creation` 을 넘겨야 한다는 사실만 인수인계에 남기면 된다.
**실제 live 승격 경로는 `promote_meeting_todo` 하나**이고 그쪽은 정렬돼 있다(아래 A-12).

### ⑤ horizontal 이 버리는 필드 · 응답 shape → **FAIL 1건(F-1) + WARN 1건(W-1). shape 불일치는 없다.**

- 「받았다 버리는 필드」: `start_date`·`parent_task_id`·`project_id` 는 **명시 거절**이라 계약상 옳다(F-1 은
  FE 가 그 사실을 모르는 것이 문제). `source_*` 넷은 **조용히 버린다**(W-1).
- **응답 shape 은 일치한다**: horizontal 첫 응답은 `self._tasks.get(...)` → `TaskDetailResult`,
  영수증은 `creation_receipt` → `TaskMutationResult`. `task_results.py:135` 가
  `class TaskDetailResult(TaskMutationResult)` 이고 REST 라우트 반환 타입이 `TaskMutationResult`(`http.py:1266`)라
  FastAPI 가 여분 키를 걸러 **두 응답이 같은 모양으로 나간다**. `_related_view`(`application.py:391`)도
  `**self._view(task)` 를 펼치므로 요청자(비담당자)가 받는 응답에 필수 키가 빠지지 않는다.
  MCP 에서는 첫 응답에 여분 키가 더 실리지만 `CommandResult` 가 그대로 통과시키는 자리라 파손은 없다 (P3).

### ⑥ 신규 assigned 에서 수락 회차 전용 명령 → **PASS. 자료·완료근거 보존도 PASS.**

- `test_task_creation_contract.py:330-371` 이 `accept`·`reject`·`negotiate`·`amend`·`resubmit` 다섯을
  전부 422 로 고정하고, evidence 422 + `AttachmentRecord` 0건 + 감사 이벤트가
  `work_request.created` **하나뿐**임을 단언한다. 「업로드만 남는」 모양이 아니다.
- 구현 근거: `requests.py:820` `_decision_target` 이 `state not in {"pending","negotiating"}` 를 거부하고,
  `_evidence_target`(`:596`)은 `store_file` **앞에서** 막는다. 수신함도
  `work_tasks.py:1414` `state.in_(("pending","negotiating"))` 라 신규가 서지 않는다(테스트 `:370` 이 고정).
- 보존: `work_tasks.py:1314-1319` 가 체크리스트·참고 업무를 요청에서 업무로 옮기고
  `source_work_request_id`·`source_meeting_id`·`source_agenda_id` 를 싣는다.
  완료 승인은 `test_task_creation_contract.py:396-404` 가 「완료 보고 → 요청자에게 `task.delivery`」로 고정.
- **단언을 줄여 만든 거짓 green 은 발견하지 못했다.** 오히려 판단 0건 단언이 여러 곳에 **추가**됐다.
- 다만 W-6 (신규 요청에 파일을 붙일 길이 없어진 사실)은 기록이 필요하다.

### ⑦ BE 의 공유 트리 stash 로 인한 FE·사용자 파일 유실 → **없음 (PASS)**

`git status --porcelain` 기준 FE 13개 파일 전부 `M` 로 살아 있고(리포트 §1 목록과 1:1 일치),
사용자 파일 9개도 전부 존재하며 mtime 이 11:55~12:10 로 BE 작업 시각 이후다. 내용도 비어 있지 않다
(`example.md` 만 0B 인데 HEAD 에도 untracked 빈 파일이라 이번 작업과 무관).

---

## SPEC-001 §6 W1 인수조건 대조 (18줄)

| # | 인수조건 | 판정 | 근거 |
|---|---|---|---|
| 1 | 본인 생성 한 건 · 수락 카드 없음 | PASS | `test_task_assignments.py:21-24` · `test_task_creation_contract.py:312` |
| 2 | 배정 권한 없는 구성원 → 상대 목록에 즉시 · 바로 시작 | **부분 FAIL** | 경로 자체는 `test_task_creation_contract.py:225-253` 로 PASS. 그러나 **시작일을 채우면 화면에서 막힌다** (F-1) |
| 3 | 선생성·재배정·상대 수락 불요 | PASS | `test_task_assignments.py:61-83` |
| 4 | 수락 판단·수락 대기 배정·재상신 회차 미생성 | PASS | `work_tasks.py:995-997`(삭제된 세 줄 자리) · `:1741-1745` `status="active"` · `test_…:312-328` |
| 5 | 신규 경로에 배정 거절 명령 없음 | PASS | `test_task_assignments.py:80-106` · `test_action_center.py:833-885` (DEC-001 D-4) |
| 6 | 신규 요청 권한으로 타인 기존 업무 수정·재배정 불가 | PASS | `test_task_creation_contract.py:263` |
| 7 | 관리자 배정의 조직 범위 검사 유지 | PASS | `assignments.py:105`·`:111` 무변경 · `test_…:275` · `test_task_assignments.py` 범위 테스트 무변경 |
| 8 | 권한 밖 담당 지정 거부 | **WARN** | 「원장에 없는 식별자·재직하지 않는 구성원」만 검증된다. 데모 조직이 회사 하나라 조직 범위 교집합이 늘 겹쳐 **실재 구성원은 아무도 후보 밖이 아니다** — 「외부 법무 자문」 소라까지 후보다(`test_product_operations.py:666-677`). `SPEC WORK_RECIPIENT_NOT_ALLOWED` 가 사실상 도달 불가. BE §5-② 가 정직하게 보고했고 코드로 발명하지 않은 것은 옳다. **planner/SPEC 결정 필요** |
| 9 | 멱등 키 필수 · 재전송 1건 · 동시 실행 중복 0 · 중복 활성 담당 0 | PASS | `creation.py:90-102` · `test_…:107·130` · PG `test_postgres_makes_one_task_when_the_same_creation_key_arrives_twice_at_once` · `test_postgres_refuses_a_second_active_assignment_at_the_database` · `persistence.py:1566-1576` 부분 unique |
| 10 | 같은 키 다른 내용 → 충돌 / 다른 키 같은 내용 → 둘 다 | PASS | `test_…:144-156` (409 + 업무 2건) |
| 11 | 권한 잃은 호출자에게 존재 은닉 | PASS | `creation_commands.py:274` → `application.py:186` `creation_receipt` 가 `get` 재검사 · `test_…:173-197` (404) |
| 12 | MCP 도구가 명시 키 없이 거부 · 같은 turn 다른 키 둘 다 | PASS | `mcp.py:1526·1614·1835·1864` 필수 인자 · `test_…:107·431` · `_mutation_key` 는 W1 도구에서 제거됐고 비 W1 은 그대로(`test_…:442`) |
| 13 | 다른 행위자·조직 범위의 같은 키가 안 섞임 | PASS | `UniqueConstraint(actor_id, command_kind, request_key)`(`persistence.py:969`) · `test_…:158-171` |
| 14 | 출처 상태 `assigned` · 그 상태에 판단 명령 안 걸림 · 수신함에 안 섬 · 과거 다섯 값 불변 | PASS | `work_tasks.py:957` · `requests.py:820` · `work_tasks.py:1414` · `labels.ts:26-46` 다섯 값 무변경 · `test_…:330-371` |
| 15 | 요청자·담당자·출처·행위자·시각 보존 · 진행 기록에서 읽힘 | **WARN** | 출처·요청자·시각은 PASS(`test_…:373-412`). **행위자 칼럼만 담당자로 잘못 남는다** (W-2) |
| 16 | 화면·REST·MCP·AX 같은 계약 · AX 확인 존치 · 확인 전 effect 없음 | **부분 FAIL** | REST↔MCP 는 `test_…:413-430` 로 PASS, AX 확인 전 effect 없음은 `:468` 로 PASS. **화면이 어긋난다** (F-1), AX 확정 실행의 계보 누락 (W-1) |
| 17 | 회의 승격이 같은 명령·권한·멱등성 · 재승격 1건 · 원본 회의 복귀 | PASS | `bootstrap/application.py:1847-1853` 가 `_task_creation(session).create_work_request` 를 지난다(우회 adapter 없음) · 후보 잠금 `meetings/application.py:851-861` · PG `test_postgres_promotes_one_meeting_candidate_into_one_task_under_concurrency` · 출처 두 열 `work_tasks.py:1282-1284` |
| 18 | seed 에 수락 대기 배정 0건 · 수락 판단 0건 | PASS | `scenario.py:198·224` 수락 단계 제거 · `test_…:456` |

---

## 역할 체크리스트 (rules.md)

### backend 리뷰

- **경계** — PASS. `modules/work/creation.py`·`creation_commands.py` 에 `fastapi`·`mcp`·`sqlalchemy`
  import 이 없다(`creation.py` 는 `hashlib`·`json`·`dataclasses` 만; `creation_commands.py` 는
  `Protocol` 로 원장·디렉터리를 추상화한다). `entrypoints/http.py` 는 `modules/work/errors` 만 새로 가져온다.
- **스키마** — PASS. 새 모델은 `persistence.py`(metadata)에만 더했고 `create_all`·DDL 호출을 더한 곳이 없다.
  `docs/domain-model.md` 대조표에 `task_creation_attempts` 행이 올랐다(코디 동기화분).
- **판단 계약** — PASS. envelope 은 서버가 만들고(`allowed_commands == []` 를 `test_action_center.py:860` 가 고정),
  command 는 소유 application 에 위임한다(`creation_commands.py:127·142·248` 셋 다 위임만 한다).
  재전송 = 영수증(`:122·125`).
- **재사용** — PASS. 멱등 원장은 레포에 이미 있는 `MeetingRoomCreationAttemptRecord` 모양을 따랐고
  (`persistence.py:952-980`), 후보 판정은 기존 `work_request_assignee_candidates` 에서 **한 줄만** 걷었다
  (`organization_access.py` 의 `work_request.decide` 필터 한 줄 삭제(diff)). 역할 카탈로그 무변경 — `catalog.py` 가 diff 에 없다.
- **테스트** — PASS. 신규 계약에 contract 22건 + PG 3건. `integration` 마커는 기존 PG 파일에만 있다.
- **예외** — PASS. 아래 층이 `HTTPException` 을 던지지 않는다(신규 3개 오류 전부 `TaskError` 파생,
  `errors.py:20-29`). `except Exception` 삼킴 없음 — `bootstrap/application.py:4094` 만
  `IntegrityError` 를 좁게 받고 원장에 없으면 **원래 오류를 다시 올린다**(`:4096-4099`, 위장하지 않는다).

### frontend 리뷰

- **envelope** — PASS. `WorkModals.tsx:2421-2432` 이 `canCreateRequest`·`assignCandidates` 로만 갈래를 정한다.
  kind·status 로 command 를 추론하는 새 코드가 없고, `MyWorkPage.tsx:722-726` 은 오히려
  **문구 문자열 매칭을 걷어내고** `outcome.assignedToOther` 로 바꿨다 — 개선이다.
- **호출 자리** — PASS. `grep -rn "fetch(" frontend/src` 기준 `api.ts` 밖 신규 호출 없음.
- **재사용** — PASS. 새 컴포넌트를 만들지 않았다(`TaskDraftFields`·`Select`·`Modal`·`Empty` 재사용).
- **카피·스타일** — PASS. `assigned` 라벨·톤은 `labels.ts:26-46` 안에 있고, 임의 hex 리터럴이 없다.
- **테스트** — PASS. `CreateWork.test.tsx` 11건 · `labels.test.ts` 3건 · `MyWorkPage.test.tsx` 2건 신규.
  다만 F-1 을 잡는 케이스가 없다.
- **allowed_paths** — PASS. FE diff 13개 전부 `frontend/` 안.

### allowed_paths (전체)

- BE: `backend/` 밖 수정 없음. `docs/unified-operations-inventory.json` 은 **docs 워커**가 반영했고
  code-docs-report 가 근거를 남겼다 — BE 브리프 이탈이 아니다.
- FE: `frontend/` 안.
- docs 워커: README · domain-model · unified-operations · inventory 넷. **이탈 없음.**
- 리뷰어: 이 파일 하나만 썼다. 코드·문서 무수정.

---

## 기존 부채 (이번 판정 제외)

1. **`meeting.followup.task` / `meeting.followup.request` AX action 은 실행하면 AttributeError.**
   `bootstrap/application.py:4054`(정의 없는 `_meeting_followups`) · `platform/actions.py:757` ·
   `MeetingApplication.followup_candidate`·`record_followup_promotion` 부재. blame `69dc2376` (2026-09-13).
   별도 work 로 「되살릴지 / action type 을 내릴지」를 정해야 한다.
2. **`docs/domain-model.md:55` 의 승격 라우트·표 이름이 실재하지 않는다** (W-5 — 사전 drift).
3. **`frontend/src/features/work/MyWorkPage.tsx:10-11` 의 `acceptTaskAssignment`·`declineTaskAssignment`
   는 쓰이지 않는 import.** `git show HEAD:…` 로 확인 — **W1 이전부터 죽어 있었다.** BE 보고 §5-④ 가
   「FE 워커가 정리하면 좋겠다」고 적었으나 이번 변경이 만든 것이 아니다. 정리는 선택.
4. **`docs/unified-operations.md` 의 `HTTP 137개` ↔ inventory `http_count 140`** 불일치 (docs 워커 §6-② 보고).

---

## 확인한 것 (PASS 근거) — 건너뛴 항목 명시

- **돌리지 않은 것**: 백엔드·프론트 테스트, 빌드, DB, E2E, 린트. 브리프 §7 금지 사항이고
  `make verify` 는 코디가 실행 중이다(`verify-2026-09-16.log`). **BE 보고의 수치
  (`make test` 1286 passed / 5 failed 등)를 나는 재현하지 않았고, 이 리포트의 어떤 PASS 도
  테스트 실행 결과가 아니라 소스 대조 결과다.**
- 「남은 실패 5건이 기존 flake」라는 BE §6 주장은 **검증하지 않았다** — 실행이 필요하고 코디 몫이다.
  다만 `test_relation_graph_scale.py:74` 의 module-scoped fixture 헤더 수정은 소스상 타당한 real fix 로 보인다
  (function-scoped autouse fixture 밖이라 키가 채워지지 않는다).
- 확인한 것: 신규 파일 4개 전문, BE 수정 17개 소스 파일 diff 전문, FE 8개 파일 diff 전문,
  테스트 파일 diff(주요 12개 전문 + 나머지 요약), inventory·README·domain-model diff,
  테스트 함수명 구/신 전수 대조, `git blame` 2건, 사용자 파일 9개 존재·크기.

---

## 재검수 (1차, 2026-09-16)

## 판정: WARN — **FAIL 해소**. 새 회귀 없음. 잔여는 문서 1건 + P3 3건.

F-1 과 W-1~W-7 **여덟 건 전부 해소**했다. 수정이 만든 회귀는 코드에서 발견하지 못했고, 새로 생긴
지적은 문서 한 줄의 과잉 일반화(R-1) 하나다. 브리프 §2 대로 **이미 PASS 였던 항목은 재개방하지 않았다.**

**범위**: 1차 리포트의 F-1·W-1~7 과 그 수정이 만든 회귀만. 실행 검증은 전혀 하지 않았다 —
`make verify` 로그(`verify-2026-09-16.log`, exit 2, `2 failed / 1289 passed`)와 BE 보고의 수치는
**PASS 근거로 쓰지 않았고** 전부 소스로 확인했다.

**확인 방법**: 현재 워크트리 `git diff`·`git show HEAD:<f>` 대조, `frontend-f1-fix.diff`,
`backend-review-fix1-report.md`, grep·호출 추적. 테스트·빌드·DB·E2E·stash 미실행.

---

### F-1 — 생성 창 「시작일」 ↔ horizontal 422 → **해소 (PASS)**

| 요구 | 확인한 자리 |
|---|---|
| horizontal 에서 **미노출** | `WorkModals.tsx:2444` `startDateSupported = ownerRoute !== "horizontal"` → `:2525` 필드가 조건부로만 선다. `project_id`·`reference_task_ids`(`assignTarget` 기준)와 달리 **경로 기준**이라 managed 를 걷지 않는다 |
| horizontal 에서 **미전송** | `:2622-2628` horizontal 갈래에 `start_date` **키 자체가 없다**(undefined 를 싣는 것이 아니다) |
| **지문 분리** | `:2594` `startDate: effectiveStartDate` — 숨긴 값이 지문에 들지 않아 재시도가 새 키를 만들지 않는다 |
| **validation 분리** | `:2574` `effectiveStartDate && dueDate && …` — 보내지도 않는 값으로 제출을 막지 않는다 |
| self·managed **유지** | `:2615`(managed `assignTask`) · `:2634`(self `createDirectTask`) 둘 다 `effectiveStartDate` 를 싣고, `ownerRoute` 가 horizontal 이 아니므로 값이 그대로 간다 |
| 값 **보존** | `directTaskDraft`(`:2492-2502`)가 필드 노출과 무관하게 언제나 `start_date` 를 싣고, `ActionTaskCard.tsx:107` `replace()` 가 draft 전체를 spread 하므로 **줄이 걷혀도 값이 지워지지 않는다**. `updateDirectTaskDraft` 가 되돌려 받는다 |
| 조용한 소실 **고지** | `:2447` `startDateDropped` → `:2762-2764` 「적어 둔 시작일은 보내지 않습니다 — 언제 시작할지는 담당자가 정합니다.」. 값이 있을 때만 뜬다 |

**BE 쪽 3필드 422 + no effect** — `test_task_creation_contract.py:555-594`
`test_a_recipient_creation_refuses_each_field_it_cannot_carry_and_leaves_nothing_behind`,
`start_date`·`parent_task_id`·`project_id` **parametrize 3건**. 각 건이 422 + detail 에 필드 이름 +
`TaskRecord`·`TaskCreationAttemptRecord`(그 키)·**`WorkRequestRecord` 0건** + 받는 사람 `my_work` 빈
목록 + **같은 값의 본인 생성은 201** 을 함께 단언한다. `project_id` 건이 민아를 프로젝트에 붙여
「읽을 수 없는 프로젝트(404)」와 「이 갈래가 안 받는 값(422)」을 분리한 것은 정확한 설계다.

**FE 테스트 7건** (`CreateWork.test.tsx:555-719` `describe("F-1 수평 생성과 시작일")`):
숨김·self 유지·managed 유지·**담당을 나로 되돌리면 값이 다시 선다**·숨긴 값이 validation 을 막지
않는다·재시도가 **같은 키**이고 `start_date` 키가 없다·수평에서도 연타 1회. 1차에서 「양쪽 다 테스트
0건」이라고 지적한 자리가 BE 3건 + FE 7건으로 덮였다.

**계약 유지 확인**: `creation_commands.py:157-171` `_refuse_unsupported_horizontal_fields` 는
**그대로**다 — BE 가 계약을 완화해 FE 를 맞추지 않았고, FE 가 계약에 맞췄다. 브리프가 요구한 방향이다.

---

### W-1 — AX 계보 소실 → **해소 (PASS)**

「거절」이 아니라 **전달**로 풀었다. 사용자에게 열어 둔 AX 담당 지정 기능을 축소하지 않은 판단이 옳다.

- `work_tasks.py:1260-1272` `create_task_for_request(request, *, actor_id, source_action_item_id,
  source_decision_item_id, source_submission_id, source_review_decision_id)`.
- `:1287-1289` — **요청 자신의 회차가 있으면 그것이 출처, 없으면 호출자의 계보**
  (`round_decision_item_id = item.id if item else source_decision_item_id`, submission·review_decision 동일).
  과거 행의 뜻을 덮지 않고 신규만 채운다.
- `:1303` `source_action_item_id=source_action_item_id` — 1차에 아예 비어 있던 열이 채워진다.
- 전달 경로가 **끊기지 않는다**(전수 추적):
  `actions.py:829` (`task.create_self` 확정) · `:712` (`work_request.create` 확정) →
  `creation_commands.py:148`(horizontal 갈래) · `:223`(`create_work_request`) →
  `requests.py:245-248`(인자)·`:305-312`(전달) → `work_tasks.py:1303`.
  `bootstrap/application.py` 의 `create_task`·`create_work_request` 도 넷을 그대로 흘린다.
- **「일부만 보존」 없음** (브리프 §4): Task 는 넷 전부를 받는다. 담당(assignment) 행은 회차에서만
  채우고(`:1326-1327` `item`/`decision` 만) 호출자 계보를 싣지 않는데, 이것이 **`create_assigned_task`
  (managed)와 같은 기준**임을 확인했다 — 그쪽도 task 에는 넷을 싣고 assignment 행에는 싣지 않는다.
  일관되고 문서화된 선택이다.
- 테스트 `test_task_creation_contract.py:596-651`
  `test_an_ax_confirmation_that_names_a_recipient_keeps_the_action_it_came_from`:
  확인 **전** Task·WorkRequest·원장 0건 → 확인 후 담당은 지호, `lineage.source_action_item_id ==
  action_id` + `source_work_request_id` + `source_decision_item_id` + `source_submission_id` →
  **replay** 로 두 번째 `decide` 를 보내면 Task 1건·WorkRequest 1건·원장 key = action id.
  **소실도 중복도 없음**이 한 테스트에서 함께 닫혔다.

---

### W-2 — 요청 출신 업무의 actor → **해소 (PASS) · 잔여 P3 2건**

「전부 requester 로 치환」하지 않고 **실제 caller 를 전달**했다. 브리프 §4 가 경계한 일괄 치환은 없다.

| 경로 | actor | 확인 |
|---|---|---|
| 신규 생성(본인이 보낸 요청) | **명령을 부른 사람** | `requests.py:307` `actor_id=str(principal.id)` → `work_tasks.py:1291` `created_by_actor_id=actor_id` · `:1339` `capture_version(task, actor_id, "task.created")` |
| **회의 승격** | **누른 사람** | `promote_meeting_todo(principal=클릭한 사람)` → `create_work_request` → `requests.create(principal)` → `actor_id=str(principal.id)`. 요청자 자리의 `system:meeting`(`request_lifecycle.py:13`)도, 받는 사람도 아니다 |
| **과거 pending 행의 수락** | **수락한 담당자** | `work_tasks.py:1252-1258` `create_accepted_task` 가 `actor_id=request.assignee_id` 를 그대로 넘긴다 — 그 시절엔 그 사람의 수락이 업무를 있게 한 것이 맞다 |

호출자는 이 셋뿐이다(`grep -rn "create_task_for_request\|create_accepted_task" backend/` 전수) —
actor 없이 부르는 자리가 남아 있지 않다.

**열람 권한 회귀 — 없다.** 읽기는 활성 담당으로 스코프되고(`_assignee_projection` 은
「열린 배정이 없으면 없다」로 fallback 을 두지 않는다), `created_by_actor_id` 는
`_may_read_beyond_holding`(`application.py:433`)에서 **활성 담당이 없을 때만** 쓰인다.
`test_task_creation_contract.py:654-684` 가 세 경계를 함께 고정한다 — 보낸 사람의 `my_work` 빈 목록 ·
관계 없는 구성원(minseok, `task.read` 보유)에게 **404 존재 은닉** · 보낸 사람은 출처로 **200**.
`test_task_actor.py:74`(신규 `mina`) · `:94`(과거 수락 `jiho`)도 두 뜻을 갈라 고정했고,
1차에 지적한 낡은 단언(`"jiho"` + 「The acceptance created the Task」)은 교정됐다.

**잔여 (둘 다 P3 — 동작은 옳고 «가드»가 없다)**

- **R-2. 회의 승격 actor 를 단언하는 테스트가 없다.** 구현은 위 추적대로 「누른 사람」이 맞는데,
  `created_by_actor_id` 를 보는 테스트는 `test_task_actor.py:51·74·94` 와
  `test_task_creation_contract.py:665·677` 뿐이고 **승격 경로는 그중 없다**
  (`test_meeting_finalize.py:737-760` 은 출처 세 열만 본다). 브리프 §3 이 「회의 승격자」를 명시로
  물었으므로 기록한다. 권장: `test_meeting_finalize.py` 의 승격 테스트에
  `created_by_actor_id == "mina"`(누른 사람) 한 줄 + history 첫 회차 actor 한 줄.
- **R-3. 활성 담당이 없는 순간의 열람 경계는 무검증이다.** 담당자 변경 중(직전 배정 `superseded`,
  새 배정 `pending`)에는 활성 담당이 없어 `_may_read_beyond_holding` 이
  `created_by_actor_id` fallback 을 쓴다. 그 값이 담당자→요청자로 바뀌었으므로 **조직 범위 독자의
  가시성이 그 순간에만 이동**한다(데모 조직은 회사 하나라 실제 차이가 없다). 방향은 중립이고
  「업무를 있게 한 사람」이 더 맞는 값이므로 **회귀로 보지 않는다.** 권장: 기록만, 또는 해당 순간의
  404/200 을 고정하는 테스트 1건.

---

### W-3 — README 권한 → **해소 (PASS)**

`README.md:116` 이 네 갈래로 갈라졌다. **소스와 1:1 대조 결과 전부 일치**:

| README 주장 | 실제 |
|---|---|
| 요청 수락·거절·조정 = `work_request.decide` | `requests.py:296`·`:311`·`:333` ✅ |
| 요청 재상신·거두기 = 요청자의 `work_request.create` | `requests.py:454`(resubmit)·`:496`(withdraw) ✅ |
| 배정 수락·거절 = 담당자의 `task.self_manage` | `assignments.py:221`·`:232` ✅ |
| 배정 취소 = 배정한 사람의 `task.assign` | `assignments.py:251` ✅ |

---

### W-4 — 「판단 API」 bullet → **해소 (PASS) · 새 WARN R-1**

`docs/domain-model.md:52` 이 **셋의 처지**로 갈라졌고, `POST /api/actions/{id}/decide` 가
**신규 AX 확인의 현행 경로**로 따로 섰다(`http.py:1135` 실재, `test_task_creation_contract.py:596`
신규 테스트가 지금도 이 라우트로 확정한다). `resubmit` 도 「판단이 아니라 요청자의 재상신」으로 분리됐다.
1차 지적은 닫혔다.

**새 WARN — R-1. 「관계 없는 사람에게는 존재 은닉(404)」이 요청 계열에는 성립하지 않는다 — P2 (문서만)**

- `README.md:116` 과 `docs/domain-model.md:53` 이 **요청과 배정을 한 문장으로 묶어**
  「받는 사람 422 / 관계 없는 사람 404(존재 은닉)」이라고 적는다.
- **배정은 맞다**: `assignments.py:264` `_pending_target` 이 `assignment.assignee_id != principal.id` 에
  `TaskNotFound` 를 던지고 `http.py:493` 이 404 로 매핑한다.
  `test_task_assignments.py:102-109` 가 ADMIN·JIHO 양쪽 × accept·decline 네 조합으로 404 를 고정했다
  (1차에 「잃은 단언 1건」이라 적은 자리가 원본보다 넓게 복원됐다).
- **요청은 아니다**: `requests.py:837` `_decision_target` 이
  `request.assignee_id != str(principal.id)` 에 평범한 `WorkRequestError("only the requested assignee
  may decide")` 를 던지고, `http.py:514` 가 **422** 로 매핑한다. 없는 id 는 `WorkRequestNotFound`
  (`request_errors.py:18`, `ResourceNotFound` 상속) → `http.py:442` 404.
  즉 **상태 코드가 존재를 가른다** — 판단 역량을 가진 제3자(팀장)가 남의 `assigned` 요청에 accept 를
  걸면 422 와 함께 그 요청이 있다는 사실을 얻는다. 역량이 없으면 403 이고 이 역시 404 가 아니다.
- **코드 동작은 기존 부채**다(W1 이 만들지 않았다). 새로 생긴 것은 **이번 수정이 넣은 문장**이
  배정의 실측을 요청 계열까지 일반화한 것이다 — W-3 이 지적한 것과 같은 종류의 과잉 일반화다.
  이 주장을 고정하는 테스트도 없다(요청 accept 에 대한 404 단언 0건).
- 권장(코드 변경 없음): 두 자리의 문장을 「**배정**은 관계 없는 사람에게 404 로 존재를 숨기고,
  **요청**은 판단 역량 검사(403)와 「담당자만 답한다」(422)로 막는다」로 갈라 적는다.
  요청 계열의 404 통일을 원하면 그것은 별도 결정이고 W1 범위 밖이다.

---

### W-5 — 회의 승격 route/잠금 → **해소 (PASS)**

`docs/domain-model.md:58` 이 실재하는 것으로 바뀌었다.

- API `POST /api/meetings/{id}/todos/{todoId}/promote` — `http.py:738` 실재 ✅
- 잠금 근거 `MeetingApplication.todo_for_promotion` 의 `lock=True` 두 번 +
  `ensure_todo_actionable(linked_work_request_id=…)` — `meetings/application.py:848-862` 실측과 일치 ✅
- 표시 `linked.work_request_id` ✅ · 두 층(후보 잠금 + 생성 멱등 키)을 「서로 다른 층」으로 적음 ✅
- 없는 `statements/{index}/promote` 와 `meeting_followup_promotions` unique 주장은 **사라졌다**.
  남은 `meeting_followup_promotions` 언급은 `:146` 의 「2026-09-10 에 제거했다」는 이력 한 줄뿐이고
  그것은 사실이다.

---

### W-6 — evidence vs 업무 자료 경계 → **해소 (PASS)**

`docs/domain-model.md:135` EVIDENCE 행에 경계가 정확히 적혔고, 주장마다 코드에 붙는다.

| 문서 주장 | 소스 |
|---|---|
| 신규 `assigned` 는 회차가 없어 채택 대상이 없고 `store_file` **앞에서** 422, 첨부·감사 0 | `requests.py:618` `_evidence_target` · `test_task_creation_contract.py:404-412`(422 + `AttachmentRecord` 0 + 감사 `work_request.created` 하나) |
| 업무 자료는 **담당자**의 길이다 | `materials.py:153·178·213·264` 전부 `_require(TASK_SELF_MANAGE)` + 활성 담당 |
| 논의 첨부는 신규에서도 산다 | `POST …/comments/{comment_id}/attachments` 실재 · `test_browser_interactions.py` 경로 유지 |

1차의 지적은 「기능이 사라진 사실이 어디에도 없다」였고, 지금은 **어디에 남고 누구의 길인지**까지
적혔다. 코드 변경 없이 닫힌 것이 맞다.

---

### W-7 — 잡음·주석·단언·키 커버리지 → **해소 (PASS) · 잔여 P3 1건**

| 항목 | 확인 |
|---|---|
| `== "` → `=="` 172줄 | **네 파일 전부 0건**이고 **diff 전체의 신규 `=="` 도 0건**이다(`git diff -U0 \| grep '^+' \| grep -F -c '=="'` → 0). 완전 복원 |
| SAVEPOINT 자기모순 | `work_tasks.py:311` 이 「SAVEPOINT 로 받지 **않는** 이유는 `claim` 의 주석에 있다」로 바뀌어 `:333` 과 같은 방향이다 ✅ |
| `command_kind` 오기 | `persistence.py:974` `task.create · task.assign · work_request.create`(+ 상수 위치) ✅ |
| no-op accept 호출 | `test_task_origin.py` 에 `task-assignments/…/accept` **0건** ✅ |
| `in {403, 404, 422}` 얕은 단언 | 내가 지적한 자리(구 `test_action_center.py:866`)가 `:872 == 404`(받는 쪽 존재 은닉) · `:877 == 422 and "cancel_assignment" in text`(보낸 쪽) **두 값으로 고정**됐다 ✅. 남은 13곳은 전부 **다른 파일의 사전 상태**이고(`git show HEAD:` 대조로 `test_action_center.py:756`·`test_task_actor.py:147·151` 등 확인) 이번 범위가 아니다 |
| 키 누락 미검 4자리 | `test_task_creation_contract.py:136-175` 신설 — `/api/tasks/assign`(누락·빈·공백) · `…/todos/{id}/promote`(누락·빈·공백) · MCP `promote_current_meeting_todo`. MCP `assign_task` 는 `:129` 에서 `(None, "", "   ")` 세 값으로 덮인다. **거절이 Task·원장·WorkRequest 0건이고 후보가 승격되지 않은 채 남는 것**까지 단언한다 ✅ |
| 잃은 단언 1건 | `test_task_assignments.py:102-109` 로 복원(원본보다 넓다) ✅ |

**잔여 R-4 (P3)** — `test_task_actor.py:140` 「The assignment is still pending, so nobody holds it
yet」. 바로 위 `:141` 이 이번 diff 에서 바뀐 줄이고(멱등 키 추가), **배정은 이제 `active`** 라
민아가 들고 있으므로 주석 두 절이 모두 거짓이다. W-2 가 고친 것과 같은 종류의 낡은 주석이 한 자리
남았다. 단언 자체는 여전히 옳다(`:147·151` 재배정 거절). 한 줄 교체 권장.

---

### 브리프 §4 — 자료 worker / lease 제품 코드

**보고대로 원복됐고 이번 변경에 없다 — diff 로 확인했다.**

- `git diff --stat -- backend/src/ax_workspace/bootstrap/material_worker.py` **빈 출력**(파일 실재 확인).
- `extend_lease`·`visibility_timeout` 을 쓰는 제품 파일 8개(`material_worker.py`·`report_worker.py`·
  `conversation_worker.py`·`settings.py`·`conversation_jobs.py`·`durable_jobs.py`·
  `ax_execution/conversations.py`·`jobs/domain.py`) **전부 무변경**.
- 실패한 두 테스트 파일 `test_material_worker_recovery.py`·`test_material_search.py` 도
  **diff 에 없다**(`git status --porcelain` 에 미등장). sleep 증가·단언 약화·skip 이 들어갈 자리가 없다.
- `verify-2026-09-16.log:336` `2 failed, 1289 passed` — 실패는 그 두 테스트뿐이고, 1차에 있던
  inventory 3건은 사라졌다.

**BE 의 원인 분석(박동 2.62s 블록·lease 만료 0.42s 초과)은 내가 재현·검증하지 않았다** — 계측이
필요하고 브리프 §7 이 실행을 금지한다. 다만 로그의 단언
(`['running','completed'] != ['failed','completed']`)은 「lease 를 잃은 worker 가 결과를 쓰지 않는다」는
fencing 이 동작한 모습과 일관된다.

**한 가지 의견** (코디 결정 사항이라 지적이 아니다): xdist worker 를 4개로 제한하면 이 기계에서는
통과하지만, 「3초 안에 반드시 한 번은 CPU 를 받는다」는 **테스트의 전제 자체는 여전히 무보장**이다 —
더 바쁜 기계나 CI 에서 같은 실패가 돌아온다. BE 권고 ①(두 테스트를 마커로 분리해 직렬 실행)이
단언을 하나도 잃지 않으면서 전제를 실제로 세우는 유일한 안으로 보인다. 병렬도 제한은 임시 완화로
기록해 두기를 권한다.

---

### 새로 생긴 회귀

**코드 회귀 없음.** 아래를 직접 확인했다.

- `create_task_for_request`/`create_accepted_task` 를 부르는 자리는 셋뿐이고 전부 `actor_id` 를 준다 —
  누락된 호출자가 없다(TypeError 경로 없음).
- `requests.py` 의 `create` 시그니처 확장은 **키워드 기본값 None** 이라 기존 호출부
  (`promote_meeting_todo` 등)가 그대로 통과한다.
- FE 의 `start_date` 숨김이 **하위 업무 생성**(`createDirectTask(title, {parent_task_id}, key)`)과
  **요청 갈래**(`createWorkRequest`)에 닿지 않는다 — 둘 다 `start_date` 를 싣지 않고 `directTaskContract`
  밖이다.
- `test_meeting_finalize`·PG 테스트가 보는 출처 열·`created_by_actor_id`(관리자 배정 `jiho`,
  `test_postgres_integration.py:2065`)는 managed 경로라 W-2 변경에 닿지 않는다.
- API 공개 shape·MCP 도구 스키마 무변경(`http.py` 는 1차 이후 무수정, inventory 도 재변경 없음).
- `frontend/` 는 F-1 두 파일(`WorkModals.tsx`·`CreateWork.test.tsx`)만 늘었고 나머지 11개 파일의
  변경량은 1차와 같다. 사용자 파일 9개·docs audit 5개 그대로.

### 잔여 목록 (우선순위순)

| # | 내용 | 등급 | 성격 |
|---|---|---|---|
| R-1 | README:116 · domain-model:53 의 「관계 없는 사람에게는 404 존재 은닉」이 **요청 계열에는 거짓**(422/403) | P2 | 이번 수정이 넣은 문장. 코드 동작은 기존 부채 |
| R-2 | **회의 승격 actor** 를 단언하는 테스트 없음(구현은 옳다) | P3 | 가드 누락 |
| R-3 | 활성 담당이 없는 순간의 `created_by_actor_id` fallback 열람 경계 무검증 | P3 | 중립적 변화, 기록만 |
| R-4 | `test_task_actor.py:140` 낡은 주석(「still pending, nobody holds it」) | P3 | 잡음 |

### 기존 부채 (1차와 동일 · 이번 범위 아님)

1. `meeting.followup.*` AX action 의 AttributeError (blame `69dc2376`, base 이전).
2. `docs/unified-operations.md` 의 `HTTP 137개` ↔ inventory `http_count 140`.
3. `frontend/src/features/work/MyWorkPage.tsx:10-11` 의 죽은 import (W1 이전부터).
4. 인수조건 #8 — 데모 조직이 회사 하나라 `WORK_RECIPIENT_NOT_ALLOWED` 가 실재 구성원에게 도달 불가.
   **SPEC 결정 사항**이고 코드로 발명하지 않은 것이 옳다.
5. 요청 계열 판단 명령의 422/404 불일치(R-1 의 코드 쪽) — 통일은 별도 결정.

### 이번 재검수에서 하지 않은 것

- 테스트·빌드·DB·E2E·린트 **전부 미실행**. BE 보고의 수치(`test-unit 322` · `test-contract 975` ·
  `test-postgres 65`)와 `verify` 로그는 **인용만 했고 PASS 근거로 쓰지 않았다.**
- 1차에서 PASS 였던 항목(멱등·동시성·권한 경계·seed·legacy fixture 대응표 등)은 **재개방하지 않았다.**
  다만 그 항목에 닿는 수정이 없었음을 diff 로 확인했다.
- 자료 worker 실패의 타이밍 계측은 재현하지 않았다(실행 금지).

---

## 재검수 (2차, 2026-09-16) — R-1~4 한정

## 판정: PASS — 네 건 전부 해소. 새 회귀 없음. 잔여 P3 1건(문서 대칭).

브리프 §2 대로 **R-1~4 만** 봤다. 기존 PASS 항목은 재개방하지 않았고 전체 재조사도 하지 않았다.
테스트·빌드·DB·E2E·stash 미실행 — BE 보고의 `scoped 84 passed / exit 0` 과 코디의
`BE 1297 + scale 13 + release 1(병렬4) · PG 65 · FE 645(Node 20.20)` 수치는 **인용만 했고 판정 근거로 쓰지 않았다.**

**이번 회차의 변경 범위 — 5개 파일, 제품 코드 0줄** (mtime + diff 양쪽으로 확인)

| 13:10~13:12 에 손댄 파일 | 성격 |
|---|---|
| `README.md` · `docs/domain-model.md` | R-1 |
| `backend/tests/contract/test_meeting_finalize.py` | R-2 |
| `backend/tests/contract/test_task_creation_contract.py` | R-3 |
| `backend/tests/contract/test_task_actor.py` | R-4 |

제품 코드(`backend/src`·`frontend/src`)의 최신 mtime 은 **12:31**(fix1 회차)이고 이번 회차에 바뀐 것이
없다. 자료 worker·lease 파일과 그 타이밍 테스트 두 개도 여전히 diff 밖이다.
테스트 함수명 전수 대조 결과 **삭제 0건** — `test_task_actor.py` 1건·`test_meeting_finalize.py` 2건은
모두 같은 파일 안의 1:1 개명이다.

---

### R-1 — 요청/배정 거절 코드 문장 정합 → **해소 (PASS) · 잔여 R-1a**

`README.md:116` 과 `docs/domain-model.md:53` 이 두 계열로 갈라졌다. 문장별로 소스와 대조했다.

| 문서 주장 | 실제 | 판정 |
|---|---|---|
| 배정: 담당자에게 422 `task assignment is not awaiting acceptance` | `assignments.py` `_pending_target` 의 `status != "pending"` → `TaskError` → `http.py:506` 422 | ✅ |
| 배정: 담당자가 아니면 404(존재 은닉, 보낸 사람 포함) | `_pending_target` 의 `assignment.assignee_id != principal.id` → `TaskNotFound` → `http.py:493` 404 | ✅ |
| 요청: 판단 역량 없으면 403 | `requests.py:296` `_require(WORK_REQUEST_DECIDE)` → `WorkRequestAccessDenied` → `http.py:497` 403 | ✅ |
| 요청: 역량이 있어도 담당자가 아니면 422 | `requests.py:837` 평범한 `WorkRequestError` → `http.py:514` 422 | ✅ |
| 요청: 404 는 없는 식별자뿐 | `WorkRequestNotFound`(`request_errors.py:18`, `ResourceNotFound` 상속) → `http.py:442` 404 | ✅ |
| domain-model: 제3자의 422 존재 누출은 **W1 이전부터의 계약**, 404 통일은 별도 결정 | 정확하다. `_decision_target` 의 그 줄은 이번 diff 밖이다 | ✅ |

**요청이 404 로 동작한다고 꾸미지 않았고 오류 계약을 코드로 손대지도 않았다** — 1차·재검수1차가
요구한 방향 그대로다. 1차 R-1 은 닫혔다.

**잔여 R-1a (P3, 문서만) — 배정 계열에도 403 분기가 있다.**

- 두 문서가 배정에 대해 「담당자에게 422, **그 밖의 모두에게 404**」라고 적는데,
  `assignments.py:221`(accept)·`:232`(decline)은 `_pending_target` **앞에서**
  `_require(principal, TASK_SELF_MANAGE)` 를 지난다(`:279-281` → `TaskAccessDenied` → 403).
- **데모에서 실제로 도달한다**: `catalog.py:142` `RoleTemplate("guest", …, ("meeting.read",))` 이고
  `seed.py:175` 의 소라가 그 역할이다 — 소라가 남의 배정에 accept 를 걸면 **404 가 아니라 403** 이다.
  `_PROJECT_PARTICIPANT_CAPABILITIES`·`_PROJECT_LEAD_CAPABILITIES`(`:133`·`:138`)에도
  `task.self_manage` 가 없다.
- R-1 을 고친 테스트(`test_task_assignments.py:102-109`)가 ADMIN·JIHO 만 써서 이 분기를 지나지 않았다.
- 성격상 **이번 수정이 요청 계열에만 403 을 적고 배정 계열에는 빼먹은 비대칭**이고, R-1 자체와 같은
  종류의 과잉 일반화다. 코드는 정상이고 문서 한 문장만 고치면 된다.
- 권장: 「배정은 `task.self_manage` 가 없으면 403, 있고 담당자가 아니면 404, 담당자면 422」로 세 갈래.
  원하면 guest 한 줄을 그 테스트에 더한다. **P3 — PR 을 막을 사유는 아니다.**

---

### R-2 — 승격 actor·history 단언 → **해소 (PASS)**

`test_meeting_finalize.py:763-768` 이 세 값을 **동시에** 고정한다 —
`task.created_by_actor_id == "mina"`(누른 사람) · `request["requester_kind"] == "system"` ·
`request["promoted_by_member_id"] == "mina"`. 요청자 자리의 `system:meeting`
(`request_lifecycle.py:13`)과 행위자가 **다른 값임을 한 테스트가 함께 증명**하므로,
재검수1차가 지적한 「구현은 옳은데 가드가 없다」가 정확히 닫혔다.
`:768` 이 history 첫 회차 `change_kind == "task.created"` · `actor_id == "mina"` 까지 본다.
기존 출처 세 열 단언(`:758-760`)은 그대로 남았다 — 교환이 아니라 추가다.

---

### R-3 — 활성 담당이 없는 순간의 열람 경계 + 한계 명시 → **해소 (PASS)**

`test_task_creation_contract.py:687-726` `test_the_read_boundary_holds_in_the_moment_no_one_holds_the_work`.

- 상태를 실제로 만든다: 신규 수평 생성 → `reassign` → `sorted(status) == ["pending","superseded"]` +
  **`active` 0건**(`:708-709`)을 단언한 뒤 그 순간을 잰다.
- fallback 이 읽는 값을 명시로 고정: `:711` `created_by_actor_id == "mina"`.
- 관측 경계: 요청자 200·전 담당자 200·`work.read.all` 독자(YUNA) 200 / minseok·hyeon **404** /
  세 사람 모두 `start` **404** — 「읽을 수 있다 ≠ 몰 수 있다」까지 함께 닫았다.
- **한계가 테스트 주석에 적혔다** (`:716-717`): 「이 데모 조직은 회사가 하나라 행위자 칼럼이 누구든
  같은 답이 나온다. 차이를 가르는 것은 `work.read.all` 의 범위이지 이 칼럼이 아니다.」
  브리프 §3 이 요구한 「fallback 분기 자체를 가르지 못하는 한계 명시」가 그대로 들어갔고,
  재검수1차의 「중립적 변화」 판정과 일치한다. **없는 보장을 주장하지 않았다.**

---

### R-4 — pending 주석·넓은 단언 → **해소 (PASS)**

- `test_task_actor.py:140` — 「The assignment is still pending, so nobody holds it yet」이
  「배정은 수락을 기다리지 않으므로 민아가 이미 들고 있다. 회차는 행에서 직접 읽는다」로 교정됐다.
  두 절 모두 지금 동작과 맞다.
- 같은 자리의 `in {403, 404, 422}` 두 줄이 `:150`
  `assert refused.status_code == 403 and "task.assign" in refused.text` **한 루프**로 좁혀졌다.
  실측과 맞다 — `reassign` 은 `task.assign` 을 요구하고, 담당자(민아)도 무관한 사람(소라)도
  그 역량이 없어 같은 403 에서 막힌다. 단언이 줄지 않고 **더 정확해졌다**.

---

### 새 회귀

**없다.** 이번 회차는 문서 2개 + 테스트 3개뿐이고 제품 코드가 0줄이다. 확인한 것:
테스트 삭제 0건(전수 대조) · 기존 단언 제거 없음(R-2 는 추가, R-4 는 좁힘) ·
`test_task_actor.py` 의 `[first] = … history …`(`test_meeting_finalize.py:767`)가 세션 밖에서
`task.id` 를 읽지만 `close()` 가 이미 적재된 속성을 지우지 않으므로 안전하다.

### 잔여 (2차 시점 전체)

| # | 내용 | 등급 |
|---|---|---|
| R-1a | README:116 · domain-model:53 의 배정 계열에 403(`task.self_manage` 부재) 분기 누락 — 데모의 `guest`(소라)가 실제 그 경우 | P3 · 문서만 |
| — | 재검수1차의 R-2·R-3·R-4 는 닫혔다 | — |

기존 부채 5건(`meeting.followup.*` AttributeError · `unified-operations.md` 137↔140 ·
FE 죽은 import · 인수조건 #8 SPEC 결정 · 요청 계열 422/404 불일치)은 이번 범위가 아니며 그대로다.

### 검증 상태에 대한 기록 (판정 근거 아님)

코디 보고: BE 1297 + scale 13 + release 1(xdist 병렬 4) · PG 65 통과, FE 는 Node 25 에서
localStorage 실패 후 Node 20.20 에서 645 + assets + build exit 0. **단계별 통과이고 단일
`make verify` green 은 아니다** — 이 리포트의 PASS 는 전부 소스 대조이고 실행 통과를 뜻하지 않는다.
병렬 4 완화의 한계(외부 부하가 worker 를 3초 이상 굶기면 동일 실패)는 BE 보고 §미결 2 와
재검수1차 의견이 같다 — 시간 보장 자체는 만들어지지 않으므로 임시 완화로 기록해 두기를 권한다.
E2E 는 사용자 담당.
