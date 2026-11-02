# 리뷰 리포트 — strong-hajin-projects / backend **루프2 Phase BE-3** (2026-09-22)

## 판정: **PASS — FAIL 0건 · WARN 3건** (+ **BE-3 밖의 관측 1건**: 기준선 「실패 0」이 내 3회차에서 깨졌다 — **Phase 0 부류**이고 이 판과 무관하다. §10-B)

**계약과 다른 것이 도는 자리를 찾지 못했다.** 워커가 주장한 것 넷(게이트가 한 자리에서만 빠졌다 ·
`access` 를 안 늘렸다 · 다시 쓴 테스트가 새 계약을 잰다 · RED 가 3 failed / 4 passed 였다)을
**전부 뮤테이션으로 실측했고 네 주장이 모두 참이다.** 테스트 수치도 내가 다시 재서 **네 자리가 똑같다.**
WARN 셋은 **오늘 동작이 아니라 「내일 조용히 관측을 잃을 수 있는 자리」** 다.

---

## 검수 범위 — **이번 판이 만진 6파일만**

⚠ 워크트리에 커밋이 **0건**이라 `git diff` 는 1루프·Phase 0 변경과 섞인다(55 modified · 14 untracked).
**BE-3 의 6파일은 mtime 으로 갈랐다** — 13:24 이전, `12:54~13:03` 한 덩어리로 붙어 있고
**워커 리포트 §1 의 목록과 정확히 일치한다.**

| mtime | 파일 |
|---|---|
| 12:54 | `backend/tests/contract/test_task_checklist_read_scope.py` **(신규)** |
| 12:55 | `backend/tests/contract/test_project_membership_follows_work.py` |
| 12:56 | `backend/src/ax_workspace/modules/work/application.py` |
| 12:56 | `backend/src/ax_workspace/modules/work/projects.py` |
| 13:02 | `backend/tests/contract/test_projects.py` |
| 13:03 | `backend/tests/contract/test_task_checklist.py` |

**그 창(12:54~13:03) 안에 바뀐 다른 파일이 0개다** — `frontend/` 아래 최신 변경은 `dist/assets` **11:07**,
`bootstrap/demo_work.py` **11:20**, `assignments.py`·`requests.py` **00:49**,
`entrypoints/http.py`·`mcp.py`·`task_results.py`·`platform/projects.py` **09-21 19:33**.

**실행한 검사**: `make test-unit` · `make test-contract`(두 패스) **3회** · `make test-postgres` ·
**뮤테이션 6건**(아래 §뮤테이션) · grep 전수 · `psql -l`(DB 존재·시드 시각) · `git log`.

> ⚠ **내가 남긴 흔적 하나**: 뮤테이션을 위해 `projects.py`·`assignments.py`·`application.py` 를
> **임시로 고쳤다가 되돌렸다.** 셋 다 **원본과 sha1 이 동일**함을 확인했다
> (`05233e21…` · `1e358861…` · `20296fdb…`). **내용은 한 바이트도 안 바뀌었고 mtime 만 내 세션 시각**이다.

---

## 위반 (FAIL) — **없음**

---

## 경미 (WARN) — 셋

### [WARN-1] **L-08 의 「리드」가 단언되지 않는다** — 그 사실이 코드 기본값에만 기대 있다

**무엇이.** `tests/contract/test_task_checklist_read_scope.py:86`
`test_the_lead_reads_it_too` 는 지호가 **리드**라는 것을 **재지 않는다.** 장면(`scene` 픽스처 `:41`)은
지호가 프로젝트를 **만들기만** 하고, 리드라는 사실은 「만든 사람을 `kind="lead"` 로 붙인다」는
**코드 기본값**(`backend/src/ax_workspace/modules/work/projects.py:172-179`)에서만 나온다.

**어느 계약과 어긋나나.** L-08(`spec-005-projects.md:1490`)이 재라고 한 것은 **「리드도 같다」** 인데,
그 기본값이 바뀌는 날 이 테스트는 **「참여자가 둘」** 을 재게 되고 **L-08 은 조용히 관측 대상을 잃는다** —
그런데도 초록이다. **같은 판의 L-02 는 그 관계 종류를 `_history()` 로 실제로 잰다**
(`test_project_membership_follows_work.py:156` — `("mina", "member", None)`), 그 선례가 여기엔 없다.

**권장 수정 (한 줄).** `assert ("jiho", "lead", None) in _history(...)` 를 그 테스트에 더한다.

### [WARN-2] **L-03 의 대비군이 「422 가 났다」까지만 잰다** — 어느 문이 거절했는지는 안 잰다

**무엇이.** `tests/contract/test_project_membership_follows_work.py:141`
`assert planned.status_code == 422` 하나다. `POST /projects/{id}/tasks` 는 제목 검증·일정 검증 등
**다른 이유로도 422 를 낸다** — 그 줄만으로는 **「올리는 문의 게이트가 거절했다」가 아니라
「무언가가 거절했다」** 다.

**오늘은 실제로 그 게이트를 잰다 — 내가 확인했다.** 뮤테이션 M2(그 게이트 두 줄 제거,
`assignments.py:171-172`)로 이 테스트가 **빨강이 됐다.** 그래서 FAIL 이 아니다. 다만 **거절 사유가
붙어 있지 않아** 거절 이유가 갈리는 날 조용히 다른 것을 재게 된다.

**어느 계약과 어긋나나.** L-03(`spec-005-projects.md:1478`) — 「배정 자격이 없는 사람의 프로젝트 업무
등록이 **여전히 거절된다**」. 재는 것은 **그 거절**이지 아무 거절이 아니다.

**권장 수정 (한 줄).** `assert "올릴 수 있는 자격" in planned.text` 를 그 아래 한 줄 더한다
(문구 출처: `modules/work/assignments.py:172`).

### [WARN-3] **테스트 «이름» 하나가 낡은 계약을 그대로 주장한다**

**무엇이.** `tests/contract/test_task_checklist.py:88`
`test_only_the_person_holding_the_task_can_see_or_change_its_checklist` — 워커는 같은 파일의
**모듈 docstring 에서 「can see or change」를 「can change」로 고쳤는데**(그 줄이 거짓이 됐기 때문),
**테스트 이름의 같은 주장은 그대로 뒀다.**

**어느 계약과 어긋나나.** 단언은 **여전히 참**이다 — 그 장면에는 프로젝트가 없어서 지호는 읽지도 못한다
(`:101` `GET /api/tasks/{id}` → 404). 그래서 **FAIL 이 아니다.** 어긋난 것은 **L-06 이 세운 기준**
(`spec-005-projects.md:1483` — 「**이름**·설명·단언이 새 계약을 잰다」)을 **같은 판에서 계약 서술을
고친 다른 파일에는 적용하지 않은 것**이다. 이름만 보고 온 사람은 「담당만 볼 수 있다」로 읽는다.

**권장 수정 (한 줄).** `…_can_change_its_checklist_and_no_project_opens_this_one` 류로 개명한다.

---

## 「조용히 통과하는 자리」 — 다섯 모양을 각각 찾은 결과

| 모양 | 결과 |
|---|---|
| **개명뿐인 변경** | **없다.** `_on_that_tasks_project()`(`application.py:1122`)는 `_may_read_beyond_holding()` 안의 두 줄을 이름 있는 자리로 뽑은 것인데, **뽑힌 쪽이 그 함수를 실제로 부른다**(`:1140`) — 호출자가 **둘**(그리고 `_related_view():998`)이라 판정이 한 벌이다. 뮤테이션 M4 가 이것을 확인했다(그 함수 하나를 무력화하니 **세 파일 4건**이 빨강) |
| **빈 단언** | **없다.** 의심한 둘을 각각 뮤테이션으로 깼다. ① `test_projects.py:352` `assert body["checklist"] == []` 는 항목이 0개라 비어 보이지만 **키가 없으면 `KeyError`** 라 M3 에서 빨강이 됐다. ② `test_the_project_detail_does_not_grow_the_items` 의 `"checklist" not in row` 는 **어느 뮤테이션에도 반응하지 않는다** — 다만 그것은 **이 판이 «안 한 것»(D-38)을 지키는 회귀 가드**이고, 같은 테스트의 양성 절반(`checklist_progress == {done:1,total:2}`)은 실재를 잰다. 의도된 모양으로 본다 |
| **항상 참인 가드** | **없다.** `_on_that_tasks_project` 를 `return True` 로 바꾸자(M4) `test_outside_the_project_the_items_do_not_come`·`test_only_the_person_holding_…`·`test_projects.py` 둘이 **빨강**이 됐다 — 경계가 실제로 관측된다 |
| **예외를 삼키는 폴백** | **없다.** 이번 판이 더한 코드에 `try`/`except` **0건**. `join_for_assignment` 의 `return False` 셋은 **무동작이 계약인 자리**다(SPEC §4 「거절이 아니라 무동작」) |
| **목만 검사하는 테스트** | **없다.** 신규 7건 + 재작성 3건이 **전부 `TestClient` 로 실제 HTTP 라우트**를 지난다. 목 0건 |

**기존 부채 하나를 그대로 옮겼다(이번 판정 제외).** `_on_that_tasks_project` 의
`str(getattr(task, "project_id", None) or "")`(`application.py:1131`)는 **자기 컬럼을 방어적 `getattr` 로
읽는 모양**이고, 1루프 검수 **WARN-6** 이 지적한 것과 같은 형태다. 다만 **이 판이 만든 줄이 아니라
`_may_read_beyond_holding` 에 있던 줄을 그대로 옮긴 것**이다(git diff 로 확인). 컬럼이 사라지면
**닫히는 쪽으로 틀린다**(항목이 조용히 안 실린다 — 새지는 않는다).

---

## 반드시 확인할 것 — **11항목 각각의 결과**

### 1. 게이트가 «자동 초대에서만» 빠졌나 — **참**

- **`may_assign_in` 전수 grep 이 4 → 3**: 정의(`modules/work/projects.py:503`) ·
  Protocol 선언(`modules/work/assignments.py:59`) · **`plan_project_work()`(`assignments.py:171`)**.
  `frontend/` 히트 **0건**. 빠진 하나가 **자동 초대**다(`projects.py:215` `join_for_assignment`).
- **「업무를 올리는 문」은 잠겨 있다**: `assignments.py:171-172` 의
  `if not self._projects.may_assign_in(...): raise TaskError("이 프로젝트에 업무를 올릴 수 있는 자격이 없습니다")`
  가 **그대로다**(그 파일 mtime **09-22 00:49** — BE-3 창 밖). 계약 테스트가 **422** 를 관측한다
  (`test_project_membership_follows_work.py:141`).
- **뮤테이션 M2 로 확인**: 그 두 줄을 빼자 `test_assigning_is_the_whole_condition_…` 과
  `test_projects.py::test_a_project_lead_may_put_work_on_someone_from_another_unit` 가 **빨강**.
  → **대비군이 「올리는 문」으로 옮겨진 것이 실제로 그 게이트를 잰다.**
- **붙는 자리 둘도 그대로**: `assignments.py:237`(담당 교체 제안) · `requests.py:476`(요청 발송).

### 2. 붙는 kind 가 `member` 인가 — **참**

`projects.py:243` `kind="member"`. **뮤테이션 M5**(`"lead"` 로 바꿈) → 같은 파일 **11건 빨강**
(L-02 단언 `("mina","member",None)` 포함). `lead` 승격 경로 **0건**.

### 3. 읽기 범위가 ⓑ 방식인가 (`access` 3분화 없음) — **참**

- `modules/work/task_results.py:236` **`access: Literal['owner', 'read_only']`** — **그대로**
  (그 파일 mtime **09-21 19:33**).
- `"access"` 를 **쓰는** 자리는 둘뿐이고(`application.py:942`·`:944`) 값도 둘뿐이다.
- **그 값을 읽는 자리 전수 grep**: `bootstrap/application.py:920` · `platform/actions.py:2101` —
  **둘 다 `!= "owner"`** 이고 **둘 다 미수정**(mtime 09-21 23:56 / 미변경). `owner` 의 뜻이 안 바뀌었으므로
  **함께 움직일 이유가 없었고, 실제로 안 움직였다.**
- 넓어진 것은 **선택 필드가 실리는 조건 한 줄**이다 — `application.py:998`
  `**(self._checklist_fields(task) if self._on_that_tasks_project(principal, task) else {})`.

### 4. 쓰기 가드가 한 줄도 안 움직였나 — **참**

네 표면 전부 `_holding()`(`application.py:2343`)을 지난다 —
`add_checklist_item:2201` · `update_checklist_item:2225` · `archive_checklist_item:2300` ·
`reorder_checklist:2326`. `_holding` 은 `repository.task(task_id, str(principal.id))` 로 **활성 담당자**를 묻는다.
**뮤테이션 M6**(그 한 줄을 `task_by_id` 로 바꿈) → `test_writing_is_still_refused_for_everyone_but_the_holder`
포함 **3건 빨강**. **L-11 을 재는 단언이 실재한다**(참여자·리드 각각 4표면 × 404 = 8회 관측).

### 5. 프로젝트 밖에서는 안 오는가 (L-12) — **참**

`_on_that_tasks_project` 가 **프로젝트 축 하나만** 본다(`_project_scope` = `principal.projects_for(PROJECT_READ)`,
즉 **실제 배정된 프로젝트**). 조직 축(`WORK_READ_ALL`)은 `_may_read_beyond_holding` 에만 남아 **읽기는 열고
항목은 안 연다.** **뮤테이션 M4**(항상 참) → `test_outside_the_project_the_items_do_not_come` 빨강.

### 6. `tasks[]` 가 안 넓어졌나 (D-38) — **참**

`modules/work/project_results.py:49-71` `ProjectTaskView` 의 필드는
`task_id · title · state · start_date · due_date · parent_task_id · preceding_task_ids · assignee ·
checklist_progress · span_from · span_to · overdue_days` **열둘 그대로**다 —
**`checklist` 도 `description` 도 없다**(그 파일 mtime **09-22 00:49**, BE-3 창 밖).
계약 테스트가 그것을 관측한다(`test_task_checklist_read_scope.py:154-160`).

### 7. 다시 쓴 테스트가 새 계약을 «재는가» — **세 자리 전부 잰다**

| 자리 | 확인 |
|---|---|
| ① `test_assigning_is_the_whole_condition_and_the_assigner_is_not_asked_for_permission`(`:121`) | **삭제·skip·약화 아님.** 이름·docstring·단언이 전부 바뀌었고, 뒤집힌 `assert _selector(MINA) == set()` 이 `== {"한빛 통합 마케팅"}` 으로 섰다(`:153`). **M1 로 확인** — 게이트를 되돌리니 **빨강** |
| ② 신설 `test_the_person_a_gateless_invite_brought_in_is_taken_back_off_when_they_decline`(`:159`) | 실제 `POST /api/task-assignments/{id}/decline` 를 지나고 **셀렉터에서 빠지는 것**과 **이력에 `("mina","member","요청 거절")` 닫힌 줄이 남는 것**을 둘 다 잰다. **M1 로 확인** — 빨강 |
| ③ `test_projects.py:326` 재작성 | `assert "checklist" not in body` → `assert body["checklist"] == []` + `checklist_progress == {done:0,total:0}`. **기존 단언(`access == "read_only"`·`children`·`child_progress`)을 살려 뒀다.** **M3 로 확인** — 빨강 |
| **대비군 이동** | ①의 대비군이 「올리는 문」(`POST /projects/{id}/tasks` → 422)으로 옮겨졌고 **M2 가 그것이 진짜 게이트를 잰다는 것을 증명했다.** ⚠ 다만 거절 사유는 안 잰다 → **WARN-2** |

### 8. RED 확인이 사실인가 (「구현 전 3 failed / 4 passed」) — **사실이다**

**뮤테이션 M3** — `application.py:998` 의 조건 한 줄을 무력화하고 신설 파일을 돌렸다:

```
FAILED test_task_checklist_read_scope.py::test_a_participant_reads_the_checklist_of_someone_elses_task
FAILED test_task_checklist_read_scope.py::test_the_lead_reads_it_too
FAILED test_task_checklist_read_scope.py::test_the_aggregate_comes_with_the_items
→ 신설 7건 중 3 failed / 4 passed  (+ test_projects.py 재작성 1건도 빨강)
```

**워커가 적은 수치와 정확히 같다.** 나머지 넷(L-11·L-12·L-13·D-38)이 처음부터 초록인 것도
**「회귀 가드라 정상」이라는 설명 그대로**다.

### 9. 테스트 수치 — **내가 다시 쟀다. 실패 0.**

| 명령 | 내 측정 | 워커 주장 |
|---|---|---|
| `make test-unit` | **380 passed, 1 deselected** · exit 0 | 380 passed, 1 deselected ✅ |
| `make test-contract` 1회차 (병렬 / 직렬) | **1068 passed** (241s) / **126 passed, 1081 deselected** (287s) · exit 0 | 1068 / 126 ✅ |
| `make test-contract` 2회차 | **1068 passed** (264s) / **126 passed, 1081 deselected** (288s) · exit 0 | — |
| `make test-contract` 3회차 | **1068 passed** (236s) / ⚠ **2 failed, 124 passed, 1081 deselected** (426s) · **exit 2** | — |
| `make test-postgres` (`ax_test_projects`) | **103 passed, 1588 deselected** (188s) · exit 0 | 103 passed, 1588 deselected ✅ |

- **`-p no:randomly` 미사용** — 플러그인 목록이 `xdist-3.8.0, anyio-4.15.0` 뿐이다(미설치 확인).
  직렬 패스는 Makefile 이 `-n0` 로 돈다.
- `tests/architecture` 전부 초록(`test_operation_inventory.py` 포함) — **대장 drift 0건.**
- **기준선 「실패 0」은 «두 회차» 충족하고 3회차에서 깨졌다** — 깨진 자리는 **직렬 패스의 `test_material_worker_recovery.py` 2건**이고 **Phase 0 가 이미 이름 붙인 부류**다. **BE-3 과 무관하다** — §10-B 에 따로 적는다.

### 10-A. 「첫 회차 병렬 실패 5건」의 정체 — **Phase 0 부류가 «아니다». 이번 변경 탓도 아니다. 원인은 미상.**

**세 가지를 확인했다.**

1. **Phase 0 부류(자식 프로세스 + 실시간 창)가 아니다 — 구조적으로 그렇다.** 그 다섯이 사는 파일
   (`test_reference_read_receipt.py` · `test_task_schedule_overlap.py` · `test_meeting_core.py` ·
   `test_unified_commands.py` · `test_meeting_rooms.py`) 에 **`IsolatedWork`·`stdio_client`·`subprocess`·
   `multiprocessing` 히트가 0건**이고 **`@pytest.mark.serial` 도 0건**이다. 즉 **걸개가 무장된 채로
   병렬 패스에서 돌았는데 아무 말도 안 했다** — `tests/conftest.py:60-90` 의 걸개는 그 부류가 xdist 워커 안에서
   자식을 띄우면 **자기 문구로 즉시 실패**시키므로, **걸개가 침묵했다는 사실 자체가 그 부류가 아니라는 증거다.**
   워커의 「걸개가 아무 말도 하지 않았다」는 진술은 **파일 내용으로 재확인된다.**
2. **이번 변경이 만든 것으로 볼 근거가 없다.** BE-3 이 만진 두 자리는 **자동 초대 게이트**와
   **업무 상세의 체크리스트 투영**인데, 다섯은 **참조 읽음 표시 · 일정 겹침 · 회의 안건 원천 · 회의실 대체 ·
   보고 개정의 자료/잡 등록**이고 **프로젝트 소속·체크리스트 투영 어디에도 닿지 않는다**(각 파일에
   `project`/`checklist` 히트가 없거나 무관한 자리다). 그리고 **내가 전체 회차를 세 번 돌려 다섯 중
   하나도 재현되지 않았다.**
3. **그래서 셋째 부류다 — 원인은 «미상»이고, 그 사실을 숨기지 않는다.** 다섯 모두 `tmp_path` 로 자기
   sqlite 를 쓰고 목도 공유 상태도 안 쓴다. `test_meeting_rooms.py` 만 모듈 상위에서 `threading` 을
   import 하지만(`:12`) 문제의 `test_when_no_room_can_be_replaced_the_meeting_is_not_made_at_all`(`:818`)
   자체는 스레드를 안 띄운다. **원문 실패 메시지가 리포트에 없어서 더 좁힐 수 없다.**

**코디에게 — 한 줄.** 기준선이 「실패 0」인 이상 **다시 보이면 실패 «문구»를 그대로 남기게 해야 한다.**
걸개가 자식 프로세스 부류를 이미 걷어냈으므로, 그때는 **새 기준(무엇이 흔들리는가)이 필요한 자리**다.
지금 근거로는 **재발주 사유가 되지 않는다.**

### 10-B. ⚠ **내 3회차가 «다른» 흔들림을 실제로 잡았다 — Phase 0 부류가 직렬 패스에서도 흔들린다**

**무엇이 났나.** 3회차 `make test-contract` 의 **직렬 패스**(`-n0`)에서 **2건 실패 · exit 2**:

```
FAILED tests/contract/test_material_worker_recovery.py::test_long_parse_heartbeats_its_lease_so_a_second_worker_cannot_reclaim_it
FAILED tests/contract/test_material_worker_recovery.py::test_stage_timeout_fences_the_late_parser_result
2 failed, 124 passed, 1081 deselected in 425.93s
```

**정체 — Phase 0 가 이미 이름 붙인 «바로 그» 부류다.** 그 파일은 모듈 docstring 에
「한 건 안에서 `IsolatedWork` 로 **진짜 자식 인터프리터를 최대 둘** 띄우고 **초 단위 lease 창을 실시간
시계로 잰다**」라고 스스로 적고 있고(`tests/contract/test_material_worker_recovery.py:3-7`),
**`pytestmark = pytest.mark.serial` 이 이미 달려 있다**(`:24`). 즉 **가르기는 제대로 됐고 직렬 패스에서
돌았는데도** 흔들렸다.

**BE-3 과 무관하다.** 그 파일은 **이번 판이 만진 6파일에 없고**(mtime 10:52 — Phase 0 창),
자료 워커·lease·fencing 은 **자동 초대·체크리스트 어디에도 닿지 않는다.**
**단건 재실행은 초록이다** — `make test-contract-serial FILES=tests/contract/test_material_worker_recovery.py`
→ **5 passed in 18.31s** (exit 0).

**읽을 것 — 두 가지.**

1. **`@pytest.mark.serial` 이 그 부류를 «완화»하지 «제거»하지 않는다.** 그 직렬 패스는
   **425초**가 걸렸다(1·2회차는 **287·288초**). 같은 명령이 1.5배 느려진 회차에서만 깨졌다 —
   **초 단위 lease 창이 기계 부하에 먹힌 것**으로 보이고, 이 기계에는 지금 **사용자 E2E 스택
   (uvicorn + vite)이 떠 있다.** 그 부하는 `-n0` 가 못 막는다.
2. **그래서 「기준선 실패 0」은 오늘 이 기계에서 «결정적»이지 않다.** 이것은
   **워커가 든 5건의 원인을 설명하지는 않지만**(그 다섯은 자식을 안 띄운다 — §10-A),
   **「이 저장소가 부하 아래 흔들리는 자리를 아직 갖고 있다」는 사실은 내가 직접 관측했다.**

**코디에게 — 한 줄.** 이것은 **BE-3 재발주 사유가 아니다.** 다만 **기준선을 「실패 0」으로 못 박은 채
검증을 사용자 스택과 같은 기계에서 돌리면 이런 회차가 또 나온다** — Phase 0 후속으로
**그 두 테스트의 lease 창을 시계 대신 주입 가능한 시각으로 재게 하거나**, **검증 회차 동안 스택을 내리는
절차**를 두는 것이 이 부류를 실제로 닫는 길이다.

### 11. 범위 — **넷 다 지켜졌다**

| 무엇 | 결과 | 근거 |
|---|---|---|
| `frontend/` 0줄 | **참** | BE-3 창(12:54~13:03) 안에 `frontend/` 아래 변경 **0개**. 최신은 `dist/assets` **11:07** |
| `demo_work.py` 0줄 | **참** | mtime **11:20** — 창 밖 |
| 커밋 0건 | **참** | `git log -1` = `e46ce39`(대화 시작 시점과 동일) · 워크트리 상태 그대로 |
| `reset-demo` 0회 | **참** | `ax_demo.projects` 의 `min/max(created_at)` 가 **2026-09-22 02:20 UTC(=11:20 KST)** 한 덩어리다 — 데모 시드 시각이고 **BE-3 창 이후 재시드 흔적이 없다.** 워커가 만든 전용 DB `ax_test_projects` 는 별도로 존재한다(`psql -l`) |
| 저장소에 남은 부산물 | **없음** | `capture.py`·`capture.json` 이 리포 안에 **0건**. 신규 untracked 중 BE-3 것은 `test_task_checklist_read_scope.py` **하나뿐**(나머지 untracked 는 전부 창 밖 mtime) |

---

## 뮤테이션 — **6건 전부 예상대로 빨강. 끝나고 sha1 로 원복 확인.**

| # | 무엇을 되돌렸나 | 빨강이 된 것 | 무엇을 증명하나 |
|---|---|---|---|
| **M1** | `join_for_assignment` 에 `may_assign_in` 게이트 복원 | `test_assigning_is_the_whole_condition_…` · `test_the_person_a_gateless_invite_…` (2 failed / 18 passed) | 게이트 제거가 **실제로 관측된다** |
| **M2** | `plan_project_work` 의 게이트 제거(`assignments.py:171-172`) | `test_assigning_is_the_whole_condition_…` · `test_a_project_lead_may_put_work_on_someone_from_another_unit` (2 failed / 43 passed) | **대비군이 「올리는 문」을 진짜로 잰다** |
| **M3** | `application.py:998` 의 조건 한 줄 무력화 | read_scope **3건** + `test_projects.py` 재작성 **1건** (4 failed / 37 passed) | **RED 「3 failed / 4 passed」가 사실** · `== []` 단언이 **빈 단언이 아니다** |
| **M4** | `_on_that_tasks_project` → `return True` | `test_outside_the_project_…` · `test_only_the_person_holding_…` · `test_projects.py` 2건 (4 failed) | **L-12 의 경계가 실재** · 그 함수가 **항상 참인 가드가 아니다** |
| **M5** | 붙는 `kind` 를 `"lead"` 로 | `test_project_membership_follows_work.py` **11 failed / 9 passed** | **L-02 가 관계 종류를 실제로 잰다** |
| **M6** | `_holding` 에서 담당 판정 제거 | `test_writing_is_still_refused_…` 외 2건 (3 failed / 13 passed) | **L-11 의 404 여덟 번이 실재** |

---

## 기존 부채 (이번 판정 제외)

- **`references` 가 `read_only` 응답에서 키째로 빠진다.** 이 판이 만든 것이 아니다 —
  `_with_checklist`(`application.py:2360`)에만 `"references"` 가 있고 `_related_view`(`:946`)에는 **원래 없었다.**
  워커가 §7-3 으로 올린 그대로 **계약이 없는 자리**이고, planner 몫이다.
- **`getattr(task, "project_id", None)`** — 위 「조용히 통과하는 자리」 참조. 1루프 WARN-6 의 모양이지만
  **옮겨진 줄**이다.
- **WP 완료 판정 마지막 줄 「커밋 후 API 를 다시 띄웠다」는 구조적으로 미충족**이다 —
  이번 발주가 **커밋 0건·서버 기동 금지**였다. 워커는 **TestClient 캡처**로 대체했고(리포트 §3, 9개 장면)
  그 사실을 숨기지 않았다. **「실제 응답 예시를 FE 브리프에 박는 것」은 아직 남아 있다** — 값은 리포트 §3 에
  있으므로 **옮기는 것은 코디 몫**이다. 1루프 검수가 같은 줄을 같은 이유로 미충족 처리했다.

---

## 참고 — 코디가 알면 좋은 것 (지적 아님)

- **MCP 도 같이 넓어졌다.** `entrypoints/mcp.py:1053-1055` `task_checklist` 가 `task.get("checklist", [])`
  로 같은 `TaskApplication.get()` 을 지나므로 **프로젝트 구성원이면 MCP 로도 항목을 읽는다.**
  분기를 새로 만들지 않은 결과이고 **D-29 와 같은 방향**이다. 도구 스키마는 안 흔들렸다(대장 테스트 초록).
- **L-10 의 FE 절반은 이미 서 있는 것으로 보인다** — `frontend/src/features/project/ProjectTaskPanel.tsx:66`
  이 `detail?.checklist ?? null` 로 **키 유무**를 보고 그린다. `access` 로 항목을 감추는 자리가
  그 파일에 **0건**이다. **FE-5 의 몫이라 판정에는 안 넣는다.**
- **`test_the_project_detail_does_not_grow_the_items` 만 D-38 을 지킨다** — `ProjectTaskView` 에 필드를
  더하는 변경이 오면 그 한 줄이 유일한 걸개다.

---

## 확인한 것 / 확인 안 한 것

**확인했다**: 11항목 전부 · 「조용히 통과하는 자리」 다섯 모양 · 뮤테이션 6건 ·
테스트 4종 (contract 는 3회차 + 흔들린 파일 단건 재실행) · 범위 5종 · `access` 소비처 전수 grep ·
`may_assign_in` 전수 grep · 붙는 자리 둘의 호출부 · `ProjectTaskView` 필드 전수 · DB 시드 시각.

**확인 안 했다 (이유와 함께)**:

- **첫 회차 5건의 «원문 실패 메시지»** — 리포트에 없고 재현이 안 된다(3회차 전부 초록). §10 의 판정은
  **구조적 근거**(자식 프로세스 0건 · 걸개 침묵 · 변경과 무접점)까지이고 **근본 원인은 미상으로 남긴다.**
- **FE 몫**(L-49~L-52 · L-10 의 FE 절반 · 화면 9건) · **루프3 이월** · **1루프·Phase 0 변경** ·
  **SPEC §7 미결(OQ-604~607)** — **발주서가 범위 밖으로 지정한 것**이라 보지 않았다.
- **브라우저 동작** — 서버 기동이 금지됐고(사용자 E2E 스택 가동 중) 코드 리뷰의 몫이 아니다.
