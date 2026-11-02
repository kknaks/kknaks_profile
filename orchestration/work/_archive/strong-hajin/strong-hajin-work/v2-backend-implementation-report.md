# WORK-002 v2 백엔드 구현 보고 (`@sc-ax-be`)

- 워크트리 `/Users/kknaks/orca/workspaces/Strong_hajin/strong-hajin-work` · 브랜치 `kknaksss/strong-hajin-work`
- 기준선: HEAD `8973791` + W1 미커밋 (`v2-code-baseline/manifest.json` 82파일)
- **커밋·push·PR 없음.** 워크트리에 변경만 남겼다.

## 상태: Phase 1~6 구현 완료 · 기존 계약 테스트 이행 완료 · **Phase 8 은 분담**

| 단계 | 소유 | 상태 |
|---|---|---|
| Phase 1 관계·저장 구조 · migration 기술안 | 원 BE | **done** |
| Phase 2 요청 발송·수락·거절·협의·철회·재요청 · `derived` | 원 BE | **done** |
| Phase 3 담당 변경(책임 공백 제거) | 원 BE | **done** |
| Phase 4 재귀 하위·중심 업무·순환 차단·요청 관계 읽기 | 원 BE | **done** |
| Phase 5 완료·승인·보완·합의 취소·조건 변경·재개 | 원 BE | **done** |
| Phase 6 REST·MCP·AX·회의 승격·seed·인벤토리 | 원 BE | **done** |
| Phase 8 신규 A1~C2·example 10단계 | **계약 테스트 워커** | 그쪽 보고 |
| Phase 8 PostgreSQL(C2 동시성·인덱스·FK) | **PG 워커** | 그쪽 보고 |
| Phase 7 FE | FE 워커 | 그쪽 보고 |

---

## 1. 변경 파일 — 내 소유분만

**제품 (15)**
`platform/persistence.py` · `platform/work_tasks.py` · `platform/action_center.py` ·
`modules/work/application.py` · `assignments.py` · `requests.py` · `request_lifecycle.py` ·
`request_commands.py` · `request_errors.py` · `request_results.py` · `errors.py` · `lifecycle.py` ·
`task_results.py` · `creation_commands.py` · `modules/organization_access/catalog.py` ·
`modules/ax_execution/tool_catalog.py` · `command_contracts.py` ·
`modules/meetings/followups.py` · `entrypoints/http.py` · `entrypoints/mcp.py` ·
`bootstrap/application.py` · `bootstrap/operation_inventory.py` · `bootstrap/scenario.py`

**신규 (2)** — `backend/migrations/manual/2026-09-17-w2-indexes.sql` ·
`2026-09-17-w2-indexes.concurrent.sql`

**기존 테스트 이행 (19)** — `tests/legacy_acceptance.py` + `tests/contract/` 18개
(action_center · decision_continuity · initial_checklist · mcp · meeting_finalize ·
product_operations · relation_graph · request_creation_input · request_evidence_and_cc ·
subtasks · task_actor · task_assignments · task_commands · task_creation_contract ·
task_delivery · task_history · task_origin · task_references · answer_resources)

**문서 (3)** — `README.md`(업무 절) · `docs/domain-model.md`(표 2행 신설 + 3행 갱신) ·
`docs/unified-operations-inventory.json`(**diff 난 항목만**)

> `frontend/` 와 `backend/tests/integration/postgres/` 는 **내가 만지지 않았다.**
> git status 에 보이는 그쪽 변경은 다른 워커 것이거나 W1 기준선이다
> (PG 디렉터리의 M 4개는 baseline manifest sha 대조로 **W1 기준선 그대로**임을 확인했다).
>
> **예외 한 자리**: `tests/contract/test_task_lifecycle_v2.py` 의 **`/cancel` 세 줄에만**
> 유효한 `reason` 을 더했다 — 취소 사유 필수가 켜지며 기존 분기 검증이 깨지는 자리이고,
> 코디네이터가 그 세 본문에 한해 소유를 넘겼다(msg_296877c9dcd9). 누락·공백 전용 검증은 그대로 두었고
> 그 파일의 나머지는 건드리지 않았다.

---

## 2. 구현 요약 — Phase 별

### Phase 1 · 저장 구조

- `tasks`: `cancel_reason` · `started_at` · `completed_at` · `reopened_at` (전부 nullable)
- `work_requests`: `parent_task_id` · `supersedes_request_id` (nullable FK)
- 신규 표 `task_proposals`(부분 유일 `uq_task_proposals_pending_kind`) · `work_request_list_entries`
- `active_assignment_for()` → **`current_assignment_for()` / `pending_assignment_for()`** 로 가르고
  호출부 전수 이동 (`active_assignment_for` grep 0건). `assignment_rows_for()` 추가.
- **FK 순환 해소**: `work_requests.parent_task_id` ↔ `tasks.source_work_request_id` 가 상호 참조라
  SQLAlchemy 가 「unresolvable cycles」로 **제약을 통째로 건너뛰고 있었다.**
  `use_alter=True, name="fk_work_requests_parent_task_id"` 로 풀었다. **PG 실재 확인은 PG 워커 몫.**
- 인덱스 DDL 두 파일. **「migration 체계를 세웠다」고 쓰지 않는다** — alembic 도 migrations 체계도
  이 저장소에 없고, 저 둘은 손으로 적용하는 `.sql` 이다.

### Phase 2 · 요청

- 발송이 업무 + **`status="pending"` 담당 행** + 상위 연결을 한 transaction 에 세운다.
  요청 상태는 `pending`(W1 의 `assigned` 는 더는 발행되지 않고 과거 행에서 뜻 보존).
- **발송이 수락 회차를 다시 연다** — `work_request.acceptance` DecisionItem + Submission +
  ReviewAssignment. 없으면 판단함에 아무것도 서지 않아 수락·거절·협의를 부를 자리가 사라진다.
  같은 이유로 `request_effect` 대기 담당은 `task.assignment` 판단 항목으로 **서지 않는다**
  (한 일을 두 항목으로 묻지 않는다).
- `accept()` 가 **새 Task 를 만들지 않는다** — 같은 업무의 대기 담당을 `active` 로 확정한다.
  `task_id`·`parent_task_id` 불변, `state=open` 유지, `started_at` 빈 채.
- `reject()`/`withdraw()` 가 그 업무를 `cancelled` + `cancel_reason` 으로 닫되 **상위 연결·로그 유지**.
- `POST /api/work-requests` 가 `parent_task_id`·`supersedes_request_id` 를 받고 **멱등 지문에 싣는다**.
- `amend` 가 수락 후 거부 (`WORK_REQUEST_LOCKED_AFTER_ACCEPT`).
- **`derived` 묶음 신설** — 서버가 만든다. `_view()` 를 인스턴스 메서드로 올리고 목록·상세·하위 줄에
  실었다. **FastAPI response_model 이 잘라내고 있어서** `task_results.py` 에 `TaskDerivedView` ·
  `TaskBlockingChildView` · `TaskChildProgressView` 를 신설하고 `TaskMutationResult` 를 넓혔다.

### Phase 3 · 담당 변경

- `reassign()` 이 기존 `active` 를 **닫지 않고** `pending` 을 덧붙인다(`supersedes_assignment_id`).
- `decide()` 의 거절 분기를 갈랐다 — **첫 지정 거절**은 현행대로 Task 취소, **교체 제안 거절**은
  제안만 닫는다. 표식은 `supersedes_assignment_id` 다.
- 수락은 `superseded` + `active` 를 한 transaction 에서. **닫는 UPDATE 를 먼저 flush** 한다 —
  안 하면 ORM 순서에 따라 새 행이 먼저 `active` 가 되어 부분 유일 인덱스가 간헐적으로 500 을 냈다.
- `GET /api/tasks/{id}/assignments` — `current` / `pending` / `history` 를 각각.
- 이력 세 줄: `task.assignment.change_proposed` · `task.assignment_accepted` · `task.assignment.changed`.
- **같은 답 재전송이 영수증이다** — `accept`/`decline` 맨 앞의 `_answer_receipt()` 가 회차 검사보다
  먼저 온다. 수락이 Task 회차를 올리므로 원회차 재전송이 stale 로 떨어지던 자리다. 돌려주기 전에
  읽기 권한을 다시 검사하고(K-2), **제3자는 여전히 404** 다(넓히지 않았다).
  **`source_review_decision_id` 가 있는 행만** 영수증이다 — 관리자 배정은 답 없이 바로 `active` 라
  상태만으로는 「수락된 것」과 구별되지 않는다. 답한 적 없는 배정에 수락을 부르는 것은 재전송이
  아니라 정의된 거절이고, 그 W1 계약이 그대로 산다. 판단함 경유(`action_center.py:1151`)도 같은 규칙이다.
  **재검사가 잠금 뒤에도 있다** — 잠금 앞에서만 보면 같은 순간의 두 요청이 **둘 다 아직 `pending` 인 행**을
  보고 함께 빠져나가고, 잠금에 걸렸다 풀려난 쪽이 그때 「이미 닫혔다」를 보고 422 를 낸다.
  그래서 `_pending_target()` 이 행을 잡고 다시 읽은 뒤 같은 답으로 닫혀 있으면 `None` 을 돌려주고,
  호출부가 영수증으로 답한다(effect 0). PG 동시성에서 확인된 자리다.

### Phase 4 · 하위와 읽기

- `parent_for()` 의 **한 단계 제한 제거**. 대신 **중심 업무 판정** — 같은 담당자의 직접 작업 아래
  직접 작업만 막는다(`WORK_DIRECT_NESTING`). `WORK_PARENT_UNASSIGNED`·`WORK_PARENT_CLOSED`·
  `WORK_PARENT_CYCLE`(조상 걷기, 고리가 있어도 멈춘다).
- `children` 을 **어느 Task 에서도** 낸다(직속만). `child_progress` = `{done, blocking, cancelled, total}`.
- **읽기 판정이 한 자리에서 나온다** — `TaskApplication.may_read_task()` / `readable_task_ids()`,
  `_SessionReadableWork` 는 위임만. `_list()` 에 **요청 관계 길**을 넣었고
  `_related_view()` 에 **조상이 내가 요청한 업무면 읽는다**(`_requested_ancestor`)를 더했다.
  이것이 「상세는 보이는데 파일은 못 연다」를 닫는다 — 자료 목록·본문·다운로드·검색·미리보기가
  같은 판정을 쓴다.
- **범위를 좁게 잡았다**: 하위 트리의 새 전이 권한은 **요청자 본인(+승격에서 누른 사람)**만이다.
  cc 는 부모 요청의 기존 한 겹 읽기를 그대로 갖되 하위로 자동 확장되지 않는다.
  목록 경로에도 `WORK_REQUEST_READ` 가드를 같이 걸어 **목록·상세·자료가 함께 닫힌다.**
- `my_work` 는 **활성 담당으로 든 것만** — 요청 관계는 `readable_tasks` 에만 들어간다.

### Phase 5 · 완료·제안·재개

- `_ALLOWED_TRANSITIONS[OPEN]` 에 `DONE` 추가. 요청 Task 는 여전히 거부, 하위 검사도 그대로.
- **`completion_submitted` 는 내부에 남기고 투영에서만** `state="done"` + `derived.approval="awaiting_review"`.
  `_external_state()` 한 함수가 그 매핑을 갖는다.
- **완결 판정 `is_child_settled()`** — 취소 제외 · `done` · **요청 Task 면 승인까지**.
  「지금 회차에 유효한 승인」만 센다(보완으로 회차가 오르거나 `reopened_at` 이후면 이전 승인 무효).
  세 판정(`is_child_settled` · `_settlement_gap` · `_settlement_gap_with`)이 **밖에서 보이는 값**으로 본다.
- `WORK_CHILDREN_UNFINISHED` **409**, 본문에 막는 하위 이름.
  **게이트와 공개를 갈랐다** — 막을지는 하위 **전부**로 정하고, 이름은 그 사람이 읽을 수 있는 것만.
  읽을 수 있는 것이 하나도 없으면 이름·건수 없이 일반 문구로 거절한다.
- `POST /api/tasks/{id}/reopen` · `proposals` 3종 + 조회 · `DELETE …/list-entry` ·
  `POST /api/work-requests/{id}/withdraw`.
- **상위 완료 ↔ 하위 재개의 write skew 를 닫았다** (PG 워커 보고). `reopen()` 이 상위를 잠금 없이
  읽어서, 두 transaction 이 서로 다른 행만 잡은 채 `done` 인 상위 아래에 `in_progress` 인 하위가
  남았다. 상위를 `lock=True` 로 잡고 **잡은 뒤 fresh 로 다시 읽는다.** 잠금 순서는 재개가 하위→상위
  둘, 완료가 자기 한 행 하나라 **서로를 기다리는 고리가 없다** — 모순을 deadlock 으로 바꾸지 않았고
  승자 우선순위도 새로 정하지 않았다(먼저 커밋한 쪽이 이기고 진 쪽은 기존 거절 코드로 막힌다).
- **수락된 요청 Task 의 직접 취소 거부** — 요청자·담당자·관리자 모두 409. 이 검사는 담당자 조회보다
  **앞에** 둔다(안 그러면 요청자에게 404 가 나가 왜 못 하는지도, 어디로 가야 하는지도 모른다).
- **합의 취소가 요청까지 끝낸다** — `accepted → cancelled_by_agreement` + 담당 관계 `ended` +
  열린 회차 `resolved`, 한 transaction. 안 하면 「보낸 업무」가 담당 확정으로 읽고, 목록 정리가
  그 항목을 「진행 중」이라며 거절한다.
- **목록 정리 가드** — **요청자만**(승격이면 누른 사람), **끝난 요청만**(rejected·withdrawn·
  cancelled_by_agreement). 수신자 호출 403, 진행 중 409.
- **재전송 영수증의 순서를 바로잡았다** — 요청 `accept`/`reject`, 제안 `respond`/`withdraw` 모두
  **회차 검사보다 먼저** 재전송을 가른다. 신원은 저장된 판단 행이 갖는다(누가·무엇을·어느 회차에).
  가름 셋: 같은답·원회차 = 200 영수증(effect 0) / 다른답 또는 지금회차 = 409 NOT_PENDING /
  아직 안 끝난 대상에 낡은 회차 = 422. 영수증 전에 **읽기 권한을 다시 검사한다**(K-2).
  **새 멱등 키 API 를 만들지 않았다** — 기존 회차 + 저장된 답으로만 처리했다.

### Phase 6 · 표면 일치

- MCP 도구 8 신설: `task_assignment_list` · `task_reopen` · `task_proposal_list|open|respond|withdraw` ·
  `work_request_withdraw` · `work_request_list_entry_remove`. 역량은 **REST 와 같은 것**을 건다.
  변경 명령은 전부 `requires_confirmation=True`(확인 전 effect 없음 · K-5).
- `DELEGATED_ACTION_CAPABILITIES` 6 + `COMMAND_CONTRACTS` 6(고정 필드 = 대상 + 기준 회차).
- `GET /api/tasks/{id}/children` 을 열고 인벤토리에서 **기존 `task_subtask_list`** 로 매핑했다
  (같은 판정을 지나므로 새 도구를 만들지 않는다).
- **`GET /api/work-requests/inbox`** 를 열었다 (SPEC §4 API 표의 명시 계약). 기존
  `WorkRequestApplication.inbox()` 에 얇게 연결했고 각 줄에 `task_id` 를 실었다 — 답하기 전에 무엇에
  대한 요청인지 열어 볼 수 있어야 한다. 라우트는 **`/{request_id}` 보다 먼저** 선언했다(뒤에 두면
  `inbox` 가 요청 id 로 읽혀 UUID 파싱에서 422). MCP/AX 에도 `work_request_inbox` 로 올렸다(K-10).
- **구성원 역량에 `work_request.decide` 추가** — W1 에서는 답할 것이 없어 드러나지 않았고, v2 에서는
  없으면 **받은 요청을 수락할 수 없는 사람**이 생긴다. 수신자 검사는 그 위에 따로 선다.
- 회의 승격은 발송 계약을 그대로 쓰므로 **수락 대기로 선다**. 우회 어댑터 없음.
  **OQ-206 이 막는 자리를 주석으로 남겼다** — 승격 요청의 완료 승인을 부를 사람이 0명인 것은
  미답의 결과이지 제품 버그가 아니다. seed 에서 그 경로를 빼지 않았다.
- AX 확인 화면의 상태 변경 **사유 칸이 `blocked` 에서만** 뜨고 있었다(`platform/actions.py:1813`).
  취소 사유가 필수인데 확인 화면에 칸이 없으면 사람이 채울 자리가 없다 — `cancelled` 도 뜨게 했다.
- `scenario.py` seed 가 **`accept` 열을 다시 읽는다** — 켜진 줄만 **받는 사람으로** 수락을 부른다.
  하지 않은 수락을 만들지 않는다.
- `docs/unified-operations-inventory.json` — **diff 난 항목만.** HTTP **150** · 도구 **129**.

---

## 3. 검증 결과 (내가 실행한 것만)

**AGENTS.md 준수** — 전부 `make` 타겟으로 실행했다. 범위는 `PYTEST_ADDOPTS="-k ..."` 로 좁혔다.
`PYTEST_XDIST_AUTO_NUM_WORKERS=4`(부하 완화이지 검증 면제가 아니다).

| 명령 | 결과 |
|---|---|
| `make test-unit` (`tests/unit` + `tests/architecture`) | **328 passed, 1 deselected · exit 0** (inbox·children 반영 후 재실행) |
| `make test-contract` — **기존 계약 전량**(`-k 'not test_task_lifecycle_v2'`) | `narrow-15`: **975 passed / 2 failed** → 그 둘을 좁혀 고친 뒤 `narrow-17`·`narrow-19` **rc=0** |
| 좁힌 마지막 라운드 (담당·판단·생성 축) | `narrow-19` **rc=0 · 83 passed** · `narrow-20` **rc=0 · 54 passed**(동시 재전송 영수증 수정 후) |
| 좁힌 라운드 (상태 확인·프로젝트·확인 계약) | `narrow-17` **rc=0 · 61 passed** |

> 전량 1회를 반복하지 않았다 — `narrow-15` 이후로는 **고친 자리만** 좁혀 돌렸다.
> `make` 의 실제 rc 를 `.exit` 파일로 함께 보존했다.

전량 로그 보존: `/tmp/w2logs/contract-1..4.log` · `narrow-1..11.log` · `unit-final.log`(각 `.exit` 포함).
경과: **400 → 104 → 57 → 31 → 23 → 18 → 13 → 9 → 4 → 0**(좁힌 범위 기준).

> **전량 `make test-contract` 1회는 아직 돌리지 않았다** — 신규 21건(계약 워커)과 PG(PG 워커)가
> 준비된 뒤 코디네이터가 통합 1회로 모으기로 했다. **`make verify` 도 돌리지 않았다**(코디 몫).
> **과거 W1 수치(322/976/645/65)를 v2 통과 근거로 쓰지 않는다.**

### 기존 테스트를 바꾼 방식 — 삭제·skip·단언 약화 **0건**

전부 「이전 보장 → 대체 보장」 매핑이고 각 자리에 SPEC 절을 주석으로 달았다.

| 이전 보장 | 대체 보장 | 근거 |
|---|---|---|
| 발송하면 즉시 수신자 `my-work` | 발송은 업무를, **수락이 담당을** | SPEC-003 §4 발송·수락 |
| 요청 상태 `assigned` | `pending` (`assigned` 는 미발행·과거 행 뜻 보존) | §4 State · P-8 |
| `state="completion_submitted"` | `state="done"` + `derived.approval="awaiting_review"` | §4 State · §3 S-7 |
| `child_progress {done,total}` | `{done,blocking,cancelled,total}` | §4 Data |
| 하위 미완결 완료 거부 **422** | **409** `WORK_CHILDREN_UNFINISHED` | §4 Case Matrix |
| 끝난 업무에 하위 붙이기 422 | **409** `WORK_PARENT_CLOSED` | §4 Case Matrix |
| 「한 단계만 저장」 422 | 깊이 제한 없음 + **409** `WORK_DIRECT_NESTING` | 정책 V-6·V-8 |
| 재배정 직후 `['superseded','pending']` | **`['active','pending']`** | 정책 V-18 (책임 공백 제거) |
| 그래프 「관계 없는 사람」을 MINA 로 | **SORA 로** (v2 에서 MINA 는 요청자다) | 정책 V-21 |
| 요청자의 `/materials` 403·404 | **200** (쓰기는 그대로 막힘) | 정책 V-21 |
| 구성원 역량 목록 | `work_request.decide` 추가 | §5 권한 |
| 발송이 회차를 만들지 않는다 | **회차는 열리고 답이 없다**(수락 회차) | SPEC-002 판단 계약 |

`tests/legacy_acceptance.py` 의 `make_request_look_pending()` 도 같은 결로 옮겼다 —
이제 **업무만 지우고**(W1 이전 모양) 회차는 제품이 연 것을 쓴다. 안 그러면 판단 항목이 둘이 된다.

---

## 4. 다른 워커가 보고한 결함 — 전부 수정

| # | 결함 | 수정 |
|---|---|---|
| 1 | FastAPI response_model 이 `derived` 등 신규 키를 **잘라냄** | `task_results.py` 응답 모델 확장 |
| 2 | `child_progress` 에 `blocking`/`cancelled` 없음 | `TaskChildProgressView` 신설 |
| 3 | `children[]` 줄에 `derived` 없음 | `TaskSummaryView.derived` |
| 4 | `GET /api/tasks/{id}/children` 없음 | 라우트 + 인벤토리 |
| 5 | 하위 미완결 거부가 422 | 409 |
| 6 | `_assignment_view` 가 `assignments[-1]`(= 대기 제안)을 담당자로 냄 | `active` 우선 |
| A | 구성원에게 `work_request.decide` 없어 **자기 요청을 수락 못 함** | 역량 추가 |
| B | 요청자가 하위 트리를 못 읽음(한 겹만) | `_requested_ancestor` (요청자 한정) |
| C | 완결 이유가 **내부 enum** 을 읽어 `awaiting_approval` 이 `unfinished` 로 | 세 자리 모두 외부 값으로 |
| D | 담당 교체 수락이 유일 인덱스로 **간헐 500** | 닫는 UPDATE 를 먼저 flush |
| E | 수락된 요청의 직접 취소가 요청자에게 404 | 취소 거절을 담당자 조회보다 앞으로 |
| F | 재개가 naive/aware 비교로 **500** | `_as_utc()` 한 헬퍼로 두 자리 normalize |
| G | 이미 답한 제안에 **다른 답**이 영수증(200) | 같은 답일 때만 영수증, 아니면 409 |
| H | 원회차 재전송이 영수증이 아니라 422 stale | 재전송 식별을 회차 검사보다 앞으로 |
| 코디 | 목록 경로에 `WORK_REQUEST_READ` 가드 없어 목록/상세 경계 불일치 | 가드 추가 |
| 코디 | 하위 트리 권한이 cc 까지 확장 | 요청자 본인으로 축소 |
| 코디 | 합의 취소가 원 요청 상태를 안 바꿈 | `settle_by_agreement` |
| 코디 | 목록 정리를 수신자도·진행 중에도 호출 가능 | 요청자 + 끝난 요청만 |
| 코디 | `withdraw_proposal` 에 회차 없음 | `expected_version` 필수 |
| 내 버그 | `my_work` 에 요청 관계 업무가 샘 | `include_requested` 분리 |
| 내 버그 | import 누락으로 336 실패 | 앵커 불일치로 조용히 no-op 된 편집 |

---

## 5. 미결·주의점

1. **OQ-203 은 답 대기다.** `completion-report` 에 하위 검사를 **더하지 않은 것은 현행 보존**이고
   새 정책의 확정이 아니다. 답이 「막는다」면 `submit_completion()` 에 검사 한 줄 + 회귀 한 줄이다.
2. **OQ-206 은 답 대기다.** 승격 요청(`requester_id = system:meeting`)의 완료 승인을 부를 수 있는
   사람이 **0명**이다. 구현하지 않았고 자동 승인도 만들지 않았다. seed 에서 그 경로를 **빼지 않고**
   `followups.py` 주석에 남겼다 — 상위 완료가 막히는 것은 **미답의 결과이지 제품 버그가 아니다.**
3. **`reply`·`status_note` 는 끝까지 `null`** 이다. 문의·회신 대기·상태 메모 원장이 코드에 없다.
   키만 두었고 값을 내는 것은 후속이다. **이번 회귀/배포 통과 대상으로 주장하지 않는다.**
4. **`blocked`·`completion_submitted` enum 을 없애지 않았다** — 투영만 바꿨다. 정리는 후속.
5. **직접 취소의 `reason` — 코디네이터 판정으로 구현했다(누락 수정).**
   - SPEC-003 §4 API(`:548`)·Validation(`:746`)과 SPEC-001 오류코드·인수조건이 **이미 확정**한 계약이었다.
     「현행 보존」은 **권한·허용 대상**에 붙는 말이고 사유 요구를 지우지 않는다.
   - 고친 자리 셋: `TaskTransitionInput.validate_reason()` 이 `target != "blocked"` 이면 `reason` 을
     지우던 분기를 **`cancelled` 보존**으로 넓혔다 · `POST /api/tasks/{id}/cancel` 이 `TaskCancelInput`
     (`reason` 필수)을 받아 넘긴다 · 순수 층이 취소에 사유를 요구하고 **이력 event 에 싣는다.**
   - **입력 통과로 끝나지 않는다** — `block_reason` 열은 「왜 막혔나」이므로 취소가 쓰지 않는다.
     그래서 `TaskStateChanged.reason` 에 정리된 사유를 실어 `ActivityEvent.reason` 으로 저장한다.
   - MCP `task_transition(target="cancelled")` 과 AX 확인 경로가 **같은 검증기**를 지난다(K-10).
   - 보존: `block` 현행 동작 · `start`/`complete`/`resume` 은 사유를 받지 않는다 ·
     수락된 요청 Task 의 `409 WORK_CANCEL_REQUIRES_AGREEMENT` 안내와 권한.
   - 회귀: `test_subtasks.py::test_a_direct_cancellation_needs_a_reason_and_keeps_it`
     (누락 422 · **공백뿐 422** · 성공 200 + `cancel_reason="direct"` + **실제 `ActivityEvent.reason` 저장**).
   - FE 계약(`{expected_version, reason}`)을 FE 워커에 직접 전달했다.

6. **배포 직전 재확인이 필요하다** — BASE U-1·U-2·U-6 과 인덱스 실재는 Phase 0 에서 **빈 DB** 라
   세지 못했다. 빈 DB 의 0건을 배포 통과로 쓰지 않는다. 특히
   `SELECT source_work_request_id, count(*) FROM tasks WHERE source_work_request_id IS NOT NULL GROUP BY 1 HAVING count(*) > 1`
   이 0이 아니면 부분 유일 인덱스를 만들 수 없다.
7. **`use_alter` FK 는 PG 에서 직접 확인해야 한다** — SQLite 에서는 무시될 수 있다. PG 워커에 넘겼다.
8. **브라우저 E2E 는 실행하지 않았다.** 화면 경로가 검증됐다고 쓰지 않는다.
9. **SQLite 계약 테스트로 PostgreSQL 을 대신하지 않았다.** PG 수치는 PG 워커 보고를 인용해야 한다.
