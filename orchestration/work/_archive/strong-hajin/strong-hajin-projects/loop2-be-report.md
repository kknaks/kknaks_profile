# 루프2 Phase BE-3 결과 보고 — 자동 초대 게이트 제거(D-28) · 체크리스트 읽기 범위(D-29)

## 상태: done

- **task-id**: `task_acab59dd08e6`
- **워크트리**: `/Users/kknaks/orca/workspaces/Strong_hajin/strong-hajin-projects` (브랜치 `kknaksss/strong-hajin-projects`)
- **읽은 정본**: SPEC-005 **v0.2.0**(검수 반영본 — `새 오류 코드` 두 행이 한 행으로 합쳐진 판) ·
  WORK-005 Phase BE-3(`~~D-12~~ → D-28` 표기 반영본) · DEC-004 D-28·D-29 · `loop2-survey-report.md` Q5
- **커밋·push 0건.** **`frontend/` 0줄**(확인: 이 세션 중 `frontend/` 아래 수정 시각이 바뀐 파일 **0개**) ·
  **`bootstrap/demo_work.py` 미수정** · **`make reset-demo` 미실행**

---

## 1. 바꾼 파일 — **6개**(신규 1). 각각이 닫는 인수조건

| # | 파일 | 무엇을 | 닫는 인수조건 |
|---|---|---|---|
| 1 | `backend/src/ax_workspace/modules/work/projects.py` | `join_for_assignment()` 의 **게이트 한 줄 제거**(`if not self.may_assign_in(...): return False`) + docstring 을 새 계약으로 다시 씀 | **L-01 · L-02 · L-04** |
| 2 | `backend/src/ax_workspace/modules/work/application.py` | `_on_that_tasks_project()` **신설**(`_may_read_beyond_holding` 의 프로젝트 절반을 이름 있는 자리로 뽑음) · `_checklist_fields()` **신설**(항목+집계 한 벌) · `_related_view()` 반환에 **조건부로 그 한 벌을 싣는다** | **L-07 · L-08 · L-09 · L-12 · L-13** |
| 3 | `backend/tests/contract/test_project_membership_follows_work.py` | 뒤집힌 테스트 **다시 씀**(삭제·skip 아님) + **L-05 테스트 1건 신설** + 낡은 `D-12` 표기 3자리 정정 | **L-01 · L-02 · L-03 · L-05 · L-06** |
| 4 | `backend/tests/contract/test_task_checklist_read_scope.py` **(신규)** | D-29 계약 테스트 **7건** | **L-07 · L-08 · L-09 · L-11 · L-12 · L-13** |
| 5 | `backend/tests/contract/test_projects.py` | **조사가 못 찾은 둘째 뒤집힘**(`assert "checklist" not in body`)을 새 계약으로 다시 씀 — 아래 §5 | **L-07**(회귀) |
| 6 | `backend/tests/contract/test_task_checklist.py` | 모듈 docstring 의 **낡은 계약 문장** 정정(「holder 만 **볼 수** 있다」 → 쓰기만) · 주석 1줄. **단언은 한 줄도 안 바꿨다** | — (L-11 의 서술 정합) |

**건드리지 않은 것 — 확인한 자리**

- `may_assign_in` **정의**(`projects.py:503`) · **Protocol 선언**(`assignments.py:59`) ·
  **`plan_project_work()`**(`assignments.py:171`) — **조사가 센 나머지 3자리 그대로.**
  전수 grep 결과가 **4 → 3**(빠진 하나가 자동 초대 게이트다).
- **체크리스트 쓰기 가드 0줄** — `add_checklist_item` · `update_checklist_item` · `archive_checklist_item` ·
  `reorder_checklist` 전부 `_holding()`(활성 담당자 + `task.self_manage`) 그대로.
- `task_results.py` **미수정**(B4 확인만) — `checklist`·`checklist_progress` 는 **이미 `NotRequired`** 였다.
  **타입이 안 바뀌고 실리는 조건만 바뀌었다.**
- `entrypoints/http.py`·`mcp.py` **미수정** — **새 라우트 0 · 새 도구 0 · 새 오류 코드 0.**
  `tests/architecture/test_operation_inventory.py` **초록**(대장 drift 0건 — 패치할 항목 없음).
- `docs/domain-model.md` **미수정** — **표도 컬럼도 안 늘었다.**

---

## 2. 무엇을 어떻게 갈랐나 (D-29 의 구현 판단)

SPEC §4 의 **ⓑ 를 그대로** 구현했다. **`access` 값은 `owner`/`read_only` 둘 그대로**이고,
넓어진 것은 **선택 필드가 실리는 조건 하나**다.

```python
# modules/work/application.py — _related_view() 끝
**(self._checklist_fields(task) if self._on_that_tasks_project(principal, task) else {}),
```

- **프로젝트 판정은 새로 만들지 않았다.** `_may_read_beyond_holding()` 안에 있던 **프로젝트 절반**을
  `_on_that_tasks_project()` 로 뽑아 **둘이 같은 함수를 부른다** — 새 질의 0건.
- **조직 축과 일부러 갈랐다.** 읽기를 여는 길은 둘(조직 범위 · 프로젝트 범위)인데 **항목을 여는 길은
  프로젝트 하나**다(D-29). 한 값으로 묶으면 **프로젝트 밖에서 조직 축으로 읽는 사람**(대표)에게도
  항목이 새어 나간다 — 그것이 **L-12 가 막는 자리**다.
- **항목과 집계를 한 벌로 묶었다**(`_checklist_fields`). 하나만 실으면 **같은 사실을 두 규칙으로 읽는
  것**이 된다(L-09). 담당이 보는 값과 **같은 함수가 만든 같은 값**이다.

---

## 3. ⚠ FE 가 받을 **실물 응답** — 서버를 띄우지 않고 계약 하네스(TestClient)에서 찍었다

**장면**: 지호(제품팀장)가 프로젝트 「한빛 통합 마케팅」을 만든다 → 지호는 **리드**.
민석(재무 구성원)을 **참여**로 붙인다. 프로젝트 업무 「플레이스 썸네일 제작」을 **민아**에게 넘기고
민아가 수락해 **쥔다**. 민아가 체크리스트 둘을 넣고 하나를 체크한다.
유나(대표)는 **이 프로젝트에 안 붙어 있고** 조직 축으로 그 업무를 읽는다.

### 3-1. `GET /api/tasks/{task_id}` — **내 업무일 때** (민아 · `access: "owner"`)

```json
{
  "task_id": "e6108be6-...", "title": "플레이스 썸네일 제작", "state": "open", "version": 5,
  "description": "시안 세 벌을 만들고 고른다",
  "project_id": "14610c3c-...",
  "assignment": { "assignment_id": "ba3de73d-...", "kind": "direct", "status": "active",
                  "assigned_by": "jiho", "accepted_at": "2026-09-22T03:57:24.161890" },
  "assignee": { "member_id": "mina", "display_name": "민아 (구성원)" },
  "access": "owner",
  "checklist": [
    { "item_id": "6d43766f-...", "text": "레퍼런스 모으기", "position": 1, "done": true,
      "state": "active", "version": 2, "created_by": "mina",
      "completed_by": "mina", "completed_at": "2026-09-22T03:57:24.183528" },
    { "item_id": "2924016b-...", "text": "시안 세 벌", "position": 2, "done": false,
      "state": "active", "version": 1, "created_by": "mina",
      "completed_by": null, "completed_at": null }
  ],
  "checklist_progress": { "done": 1, "total": 2 },
  "references": [],
  "children": [], "child_progress": { "done": 0, "blocking": 0, "cancelled": 0, "total": 0 },
  "delivery": null, "predecessors": []
}
```

### 3-2. `GET /api/tasks/{task_id}` — **같은 프로젝트의 「남의」 업무일 때**

**참여자(민석)와 리드(지호)의 응답이 바이트 단위로 같다** — `access` 값도 `checklist` 도 `checklist_progress` 도.
**리드·참여자를 가르지 않는다**(D-29)가 응답에서 그대로 관측된다.

```json
{
  "task_id": "e6108be6-...", "title": "플레이스 썸네일 제작", "state": "open", "version": 5,
  "description": "시안 세 벌을 만들고 고른다",
  "project_id": "14610c3c-...",
  "assignment": { "assignment_id": "ba3de73d-...", "kind": "direct", "status": "active",
                  "assigned_by": "jiho", "accepted_at": "2026-09-22T03:57:24.161890" },
  "assignee": { "member_id": "mina", "display_name": "민아 (구성원)" },
  "access": "read_only",
  "checklist": [
    { "item_id": "6d43766f-...", "text": "레퍼런스 모으기", "position": 1, "done": true,
      "state": "active", "version": 2, "created_by": "mina",
      "completed_by": "mina", "completed_at": "2026-09-22T03:57:24.183528" },
    { "item_id": "2924016b-...", "text": "시안 세 벌", "position": 2, "done": false,
      "state": "active", "version": 1, "created_by": "mina",
      "completed_by": null, "completed_at": null }
  ],
  "checklist_progress": { "done": 1, "total": 2 },
  "children": [], "child_progress": { "done": 0, "blocking": 0, "cancelled": 0, "total": 0 },
  "delivery": null, "predecessors": []
}
```

> **`references` 키가 «없다».** `owner` 응답에는 `"references": []` 가 있고 **`read_only` 응답에는 그 키
> 자체가 없다.** 이 판이 만든 차이가 아니라 **원래 그랬다** — FE 가 `body.references.map(...)` 을 쓰면
> 남의 업무에서 터진다. **`checklist` 와 달리 `references` 는 이 판이 열지 않았다.**

### 3-3. `GET /api/tasks/{task_id}` — **프로젝트 «밖»에서 읽을 때** (유나 대표 · 조직 축)

```json
{
  "task_id": "e6108be6-...", "title": "플레이스 썸네일 제작", "state": "open", "version": 5,
  "description": "시안 세 벌을 만들고 고른다",
  "project_id": "14610c3c-...",
  "assignee": { "member_id": "mina", "display_name": "민아 (구성원)" },
  "access": "read_only",
  "children": [], "child_progress": { "done": 0, "blocking": 0, "cancelled": 0, "total": 0 },
  "delivery": null, "predecessors": []
}
```

**`checklist` · `checklist_progress` · `references` 세 키가 전부 «없다».** `description` 은 **온다**(L-13).

### 3-4. 같은 사람(민석)이 본 `GET /api/projects/{project_id}` 의 `tasks[]` — **안 넓어졌다**(D-38)

```json
{ "task_id": "e6108be6-...", "title": "플레이스 썸네일 제작", "state": "open",
  "start_date": null, "due_date": null, "parent_task_id": null, "preceding_task_ids": [],
  "assignee": { "member_id": "mina", "display_name": "민아 (구성원)" },
  "checklist_progress": { "done": 1, "total": 2 },
  "span_from": null, "span_to": null, "overdue_days": null }
```

**집계는 담당과 무관하게 언제나 실리고**(미터·막대의 재료) **항목은 상세에만** 있다.
프로젝트 상세 봉투 키는 `["description","ends_on","external_key","may_manage","members","name",
"project_id","starts_on","state","tasks","version"]` 이고 이 판이 **한 키도 더하지 않았다.**

### 3-5. 자동 초대가 돈 뒤 **초대된 사람 눈의 `GET /api/projects`**

지호는 「가을 캠페인」의 **참여자**(관리 권한 없음 · 그 프로젝트에서 배정 자격 없음)이고,
**조직 축 배정 권한**으로 민아에게 업무를 넘긴다 → `POST /api/tasks/{id}/reassign` **200**.

민아의 `GET /api/projects` — **초대 전후**:

```jsonc
// 전
[ { "project_id": "14610c3c-...", "name": "한빛 통합 마케팅", "description": null,
    "state": "active", "starts_on": null, "ends_on": null, "external_key": null, "version": 1 } ]

// 후 — 「가을 캠페인」이 한 줄 늘었다 (L-01)
[ { "project_id": "14610c3c-...", "name": "한빛 통합 마케팅", ... },
  { "project_id": "bc0246b8-...", "name": "가을 캠페인", "description": null,
    "state": "active", "starts_on": null, "ends_on": null, "external_key": null, "version": 1 } ]
```

`GET /api/projects/{id}/participation-history` 의 그 줄 — **`참여`(member)** 다(L-02):

```json
{ "assignment_id": "6ce1fc86-...", "member_id": "mina", "assignment_kind": "member",
  "valid_from": null, "valid_until": null, "assigned_by_member_id": "jiho",
  "created_at": "2026-09-22T03:57:24.240842+00:00",
  "ended_at": null, "ended_by_member_id": null, "end_reason": null,
  "display_name": "민아 (구성원)", "assigned_by_display_name": "지호 (팀장)", "ended_by_display_name": null }
```

민아가 그 배정을 **거절**하면 참여가 닫히고 목록에서 빠지며 **행은 남는다**(L-05):

```json
{ "assignment_id": "6ce1fc86-...", "member_id": "mina", "assignment_kind": "member",
  "ended_at": "2026-09-22T03:57:24.255280+00:00", "ended_by_member_id": "mina",
  "end_reason": "요청 거절", "ended_by_display_name": "민아 (구성원)" }
```

**배정 자체가 막히는 사람은 전과 같다**(L-04) — `POST /api/tasks/{id}/reassign` → **422**
`{"detail": "assignee is not within your assignment scope"}`. **새 오류 코드 0건.**

### 3-6. ⚠ **틀리기 쉬운 자리 — FE 는 이 목록을 보고 짠다**

| # | 틀리기 쉬운 자리 | 실물이 말하는 것 |
|---|---|---|
| ① | **`access` 로 체크리스트를 감추지 마라** | `access: "read_only"` **인데 `checklist` 가 실린다.** 그 조합이 **정상**이다. `access` 는 이제 **쓰기 범위**만 뜻한다 (L-10) |
| ② | **`checklist` 키의 «유무»로 그려라** | 안 실릴 때는 **`null`·`[]` 이 아니라 키 자체가 없다.** `body.checklist?.length` 로 갈라야 하고, `body.checklist.length` 는 프로젝트 밖 갈래에서 **터진다** |
| ③ | **`checklist_progress` 도 같이 없다** | 상세에서 항목이 안 오면 **집계도 안 온다.** 미터를 상세 응답으로 그리면 그 갈래에서 빈다 — **미터의 재료는 프로젝트 상세 `tasks[]` 의 `checklist_progress`** 이고 그쪽은 **언제나 실린다** |
| ④ | **`references` 는 안 열렸다** | `owner` 에만 있는 키다(§3-2 인용 참고). 이 판이 연 것은 **체크리스트 둘뿐**이다 |
| ⑤ | **리드라고 더 오지 않는다** | 리드 응답과 참여자 응답이 **완전히 같다.** 「리드면 쓰기도 되겠지」로 단추를 열면 **404 를 받는다** |
| ⑥ | **쓰기 네 표면은 전부 404 다** | `POST /api/tasks/{id}/checklist` · `PATCH .../checklist/{item_id}` · `DELETE .../checklist/{item_id}` · `POST .../checklist/order` — 담당이 아니면 **읽을 수 있어도 404**(403 이 아니다). 체크박스를 **읽기 전용으로 렌더**해야 한다 |
| ⑦ | **`tasks[]` 에는 `checklist` 가 없다** | 우 레일은 **선택된 하나에만** 상세를 불러야 한다. 목록으로 항목을 그릴 수 없다 (D-38 · L-33) |
| ⑧ | **`description` 은 네 갈래 전부에 온다** | 프로젝트 밖 읽기에도 온다. **「`read_only` 면 설명이 없겠지」는 틀리다** (L-13) |
| ⑨ | **초대는 `GET /api/projects` 에 한 줄이 «느는» 것으로 관측된다** | 새 필드·새 플래그가 아니다. 초대됐는지 알려 주는 값이 **응답에 없다** — 목록이 늘어난 것이 전부다 |
| ⑩ | **초대가 붙이는 관계는 `member` 다** | `participation-history` 의 `assignment_kind` 가 `"member"`. **`lead` 승격 없음** — 그러므로 `may_manage` 는 **여전히 `false`** 이고 **관리 모달 손잡이가 서면 안 된다** |
| ⑪ | **거절하면 «사라진다»** | 자동 해제가 돌면 그 프로젝트가 목록에서 빠진다. 화면이 프로젝트 목록을 캐시해 두면 **없는 프로젝트를 고른 상태**가 남는다 — 거절 뒤 목록을 **다시 읽어야** 한다 |
| ⑫ | **배정 거절 문구는 그대로다** | `422` + `{"detail": "assignee is not within your assignment scope"}`. **초대 전용 오류는 없다** — 새 갈래를 기다리지 마라 |

---

## 4. 테스트 — **실패 0**

| 명령 | 결과 |
|---|---|
| `make test-unit` (`tests/unit` + `tests/architecture`) | **380 passed, 1 deselected** — 실패 0 |
| `make test-contract` **(두 패스)** | 병렬 패스 **1068 passed** · 직렬 패스(`-n0`) **126 passed, 1081 deselected** — **실패 0** · `make` **exit 0** (고친 뒤 **전체 회차 두 번 연속 초록**) |
| `make test-postgres` (`POSTGRES_TEST_URL=postgresql+psycopg://ax:ax@127.0.0.1:54329/ax_test_projects`) | **103 passed, 1588 deselected** — 실패 0 |

- `tests/architecture` **전부 초록** — `test_operation_inventory.py`(대장 drift) · `test_architecture.py`(계층) ·
  `test_serial_test_targets.py`(직렬 가르기) · `test_test_pyramid.py` 포함. **패치할 drift 항목 0건.**
- **`@pytest.mark.serial` 을 새로 달 일이 없었다** — 이번에 더한 테스트 **8건 모두 자식 프로세스를 안 띄운다**
  (TestClient + sqlite). `conftest` 걸개가 병렬 패스에서 아무 말도 하지 않았다.
- **`-p no:randomly` 를 쓰지 않았다.** 전용 DB(`ax_test_projects`)는 **새로 만들었고** 데모 DB(`ax_demo`)는
  **건드리지 않았다.**

**⚠ 첫 `make test-contract` 회차에 실패 6건이 났다 — 그중 «내 탓은 1건»이다.**

| 실패 | 내 탓인가 | 처분 |
|---|---|---|
| `test_projects.py::test_a_project_member_sees_the_parts_they_could_already_open` | **그렇다** | **D-29 가 뒤집은 둘째 주장이다**(§5). 새 계약으로 다시 썼다 |
| `test_reference_read_receipt.py::test_my_read_never_moves_another_referrers_inbox` | **아니다** | 단건 재실행 **초록** · **둘째 전체 회차에서 재현 안 됨** |
| `test_task_schedule_overlap.py::test_a_slot_on_a_finished_task_holds_no_time` | **아니다** | 〃 |
| `test_meeting_core.py::test_the_places_a_meeting_actually_builds_agendas_from_are_still_three` | **아니다** | 〃 |
| `test_unified_commands.py::test_confirmed_report_revision_registers_material_and_job_before_any_read` | **아니다** | 〃 |
| `test_meeting_rooms.py::test_when_no_room_can_be_replaced_the_meeting_is_not_made_at_all` | **아니다** | 〃 |

**판정 근거**: 다섯 모두 **체크리스트·자동 초대·프로젝트 소속 어디에도 닿지 않는** 자리(회의실 배정 ·
자료/보고 잡 · 일정 겹침 · 참조 읽음 표시)이고, **다섯을 한 번에 직렬 재실행하면 5 passed**,
**그 뒤 전체 `make test-contract` 를 «두 번» 더 돌려 둘 다 실패 0**(병렬 1068 passed · 직렬 126 passed ·
`make` exit 0)이었다 — **다섯 중 하나도 재현되지 않았다.**
**병렬 패스의 흔들림으로 본다** — 다만 **Phase 0 가 닫힌 뒤의 기준선은 「실패 0」이므로 기록으로 남긴다.**
**이 다섯이 다시 보이면 `material_*` 계열과 같은 부류인지 따로 보아야 한다**(§7 판단이 필요한 것).

### 다시 쓴 테스트가 **무엇을 지키게 됐나**

**① `test_the_key_is_assigning_in_that_project_not_managing_it`
→ `test_assigning_is_the_whole_condition_and_the_assigner_is_not_asked_for_permission`** (L-06)

**삭제도 skip 도 단언 약화도 아니다.** 이름·docstring·단언이 **새 계약을 잰다.**

| 전에 지키던 것 | 이제 지키는 것 |
|---|---|
| 「열쇠는 그 프로젝트에서의 배정 권한이다」 | **「열쇠가 없다 — 배정이 성립하면 붙는다」** |
| `assert _selector(client, MINA) == set()` — 배정은 되는데 **초대는 안 된다** | `assert _selector(client, MINA) == {"한빛 통합 마케팅"}` — **붙는다** (L-01) |
| (없었다) | `assert ("mina", "member", None) in _history(...)` — **`참여` 그대로다** (L-02) |
| 대비군: 「배정 가능자가 하면 붙는다」 (게이트가 없어져 **무의미해졌다**) | **대비군을 「올리는 문」으로 옮겼다** — `POST /projects/{id}/tasks` 가 **여전히 422**. **게이트를 둘 다 뺀 것이 아니다** (L-03) |

**② 신설 `test_the_person_a_gateless_invite_brought_in_is_taken_back_off_when_they_decline`** (L-05)
게이트 없이 붙은 사람도 **예외가 아니다** — 거절하면 조건 ①·②를 똑같이 보고 참여가 닫히고,
이력에 **`end_reason: "요청 거절"` 닫힌 줄**이 남는다(행 삭제 아님).

**③ 신설 `test_task_checklist_read_scope.py` — 7건**
`참여자가 남의 항목을 읽는다`(L-07) · `리드도 같다`(L-08) · `집계가 항목과 함께 온다`(L-09) ·
`쓰기 네 표면이 전부 거절된다`(L-11 — 참여자·리드 둘 다) · `프로젝트 밖에서는 안 온다`(L-12) ·
`설명은 네 갈래 전부에 온다`(L-13) · `tasks[] 는 안 넓어졌다`(D-38).
**RED 를 먼저 확인했다** — 구현 전 **3 failed / 4 passed**(넷은 회귀 가드라 처음부터 초록이 정상).

**④ 낡은 표기 정정 3자리** — `# ---- 자동 초대 (D-11·D-12)` → `(D-11 · ~~D-12~~ → D-28)` ·
멱등 테스트의 `(D-12)` → `(D-11)`(그 주장의 실제 근거) ·
`test_no_new_rejection_branch_appears_on_the_invite_path` 의 `(D-12)` → `(D-28)` + **왜 더 참이 됐는지** 한 문단.
**단언은 셋 다 안 건드렸고 전부 초록이다**(이웃 회귀 — `:460-476` · `:170-188` 포함).

---

## 5. 조사가 못 찾은 것 — **뒤집힌 테스트가 «둘»이었다**

`loop2-survey-report.md` Q5 는 「깨지는 테스트 **정확히 1건**」이라 셌고 **그 셈은 D-28 쪽에서는 맞다.**
그 grep(`join_for_assignment|may_assign_in|자동 초대|auto_joined`)은 **D-29 쪽을 훑지 않았다.**

**둘째**: `tests/contract/test_projects.py:327` `test_a_project_member_sees_the_parts_they_could_already_open`
— 같은 프로젝트의 **현우**가 **민아**의 업무를 읽는 바로 그 장면이고, 마지막 줄이

```python
# 안을 열어 준 것은 아니다: 그 사람의 작업 공간인 체크리스트는 여전히 오지 않는다.
assert "checklist" not in body
```

**D-29 가 뒤집는 주장이 그 한 줄에 그대로 있었다.** **L-06 과 같은 방식으로 처리했다** —
삭제·skip 이 아니라 **새 계약을 재는 단언으로 다시 썼다**(항목이 빈 목록으로 오고 집계가 0/0으로 온다 ·
`access` 는 `read_only` 그대로라는 **기존 단언은 살려 두었다**).

**그리고 `tests/contract/test_task_checklist.py` 의 모듈 docstring** 이
「only the person who holds that Task **can see or change** it」이라 **계약을 문장으로 적고 있었다.**
**단언은 한 줄도 안 바꾸고**(그 파일의 장면에는 프로젝트가 없어서 전부 그대로 초록이다)
**문장만** 「읽기는 프로젝트가 열고 쓰기는 담당이 쥔다」로 고쳤다 — **거짓이 된 계약 서술을 남기지 않는다.**

---

## 6. 다른 팀 영향 (FE)

- **응답 «타입» 불변** — `TaskDetailResult` 의 `checklist`·`checklist_progress` 는 **이미 `NotRequired`** 였다.
  **새 필드 0 · 새 라우트 0 · 새 도구 0 · 새 오류 코드 0 · 시그니처 불변.**
- **바뀐 것은 「언제 실리나」 하나** — §3-6 의 열두 줄이 그 전부다.
- **L-10 의 FE 절반이 남는다** — 「`access` 로 항목을 감추는 자리가 0건」은 **FE-5 가 닫는다.**
  서버 절반(그 조합을 실제로 내는 것)은 이 판에서 닫혔고 **§3-2 가 그 실물이다.**
- **MCP 도 같은 `TaskApplication.get()` 을 지난다** — 별도 분기를 만들지 않았으므로 MCP 쪽도 같은 규칙이다.
  대장 테스트 초록이라 **도구 스키마는 안 흔들렸다.**

---

## 7. 막힌 것 · 판단이 필요한 것

**막힌 것: 없다.** BE-3 의 인수조건 12줄을 전부 닫았다.

**판단이 필요한 것 — 셋**

1. **첫 회차 병렬 실패 5건**(§4). 둘째 회차에서 재현되지 않았고 단건 재실행도 초록이라
   **내 변경 탓으로 볼 근거가 없다.** 다만 **기준선이 「실패 0」이 된 뒤에도 병렬 패스가 회차마다
   흔들리는 자리가 남아 있다**는 사실 자체는 코디가 알아야 한다 — **Phase 0 가 잡은 `material_*` 와
   같은 부류인지**(자식 프로세스 · 실시간 창) 아니면 다른 원인인지는 **이 Phase 의 범위 밖**이라 안 팠다.
2. **`access` 의 이름과 뜻이 어긋난다.** 이제 그 값은 **쓰기 범위**만 뜻하는데 이름은 「접근」이다 —
   SPEC §7 이 이미 기록으로 올린 자리이고, **개명은 이 판이 하지 않았다.** 다만 **FE 가 그 이름에 끌려
   읽기를 추론할 위험**이 실제로 있어 §3-6 ① 로 못 박아 두었다.
3. **`references` 가 `read_only` 응답에서 키째로 빠진다**(§3-2 인용). **이 판이 만든 것이 아니고
   SPEC 에도 없는 자리**라 **건드리지 않았다.** 「남의 업무에서 참조 목록을 보여 줄 것인가」는
   **계약이 없는 질문**이므로 planner 몫으로 남긴다.

---

## 부록 — 실물 응답 원본

전체 캡처(트림 전 JSON · 9개 장면)는 세션 스크래치패드의 `capture.json` 이고,
찍은 스크립트는 같은 폴더의 `capture.py` 다 — **서버를 띄우지 않고** `TestClient` 로 돌린다.
필요하면 그 스크립트를 `backend/` 에서 `uv run python <경로>` 로 재현할 수 있다(저장소에 넣지 않았다).
