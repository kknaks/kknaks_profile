# 리뷰 리포트 — strong-hajin-projects / backend (Phase BE-1 · BE-2) — 2026-09-22

## 판정: **FAIL 0건 · WARN 8건**

**계약과 같은 것이 돈다.** 붙는 자리는 **둘**이고 떼는 자리는 **넷**이며, 여섯 자리가 전부
application 메서드다 — 내가 HTTP · MCP · action-center 세 입구를 각각 따라가 **같은 메서드로 모이는 것을
코드로 확인했다**(아래 §2-2). 조건 ①·② 는 **둘 다** 걸려 있고, 자손 이동은 **게이트를 전부 먼저 건 뒤에**
옮긴다. `completion_submitted` 는 투영이 접고, 새 오류 이름·새 라우트·새 도구는 **0건**이다.
`tasks_in()` 에 필터·페이징이 안 들어왔고 `frontend/` 는 한 줄도 안 바뀌었다.

**WARN 여덟은 둘로 갈린다** — 계약 쪽 **셋**(SPEC 인수조건 한 줄이 오늘 역할 표로는 성립하지 않음 ·
조건 ② 의 「활성」 해석 · WP 가 이름 지은 기준선 파일 부재)과 코드·테스트 쪽 **다섯**(증명하지 않는
테스트 1건 · 실제 표면을 안 지나는 테스트 1건 · 방어적 `getattr` 둘 · 엉뚱한 필드에 붙은 계약 주석 ·
죽은 alias). **하나도 「다른 것이 돈다」가 아니다.**

---

## 검수 범위

- 워크트리: `/Users/kknaks/orca/workspaces/Strong_hajin/strong-hajin-projects`, branch `kknaksss/strong-hajin-projects`.
- **`git diff origin/main...` 은 비어 있다** — `HEAD == origin/main == e46ce39`. **커밋 0건**이고
  변경 전부가 **워크트리에만** 있다. 그래서 검수 범위는 `git diff`(수정 15) + untracked(신규 2) = **17 파일**,
  **+716 / −60** (인벤토리 제외) + `docs/unified-operations-inventory.json` **+90 / −1**.
- 대조 기준: `spec-005-projects.md` §4·§5·§6(인수조건 75줄) · `work-005-projects.md` Phase BE-1·BE-2 ·
  `be-impl-report.md` · `review-wp-005-report.md`(앞 판 FAIL 4 · WARN 6) · `AGENTS.md`.
- 실행한 것: `make test-unit` · `make test-contract` · `make test-contract-serial`(둘) ·
  `make test-postgres`. **서버·포트는 건드리지 않았다** — postgres 54329 는 **이미 떠 있었고**
  내가 띄우지 않았다. 코드·문서 수정 0건 — 산출물은 이 파일 하나.

---

## 경미 (WARN) — 여덟

### [WARN-1] SPEC §6 인수조건 한 줄이 **오늘의 역할 표로는 성립하지 않는다** — 그리고 새 테스트가 그 반대를 단언한다

**무엇이.** SPEC §6 자동 초대 묶음의 「**프로젝트 관리 권한이 없는 참여자**가 배정해도 붙는다 —
열쇠가 **배정 권한**이다」(`spec-005-projects.md:993`)를 **닫을 수 없다.**

**근거.**

| 사실 | 파일:줄 |
|---|---|
| `project-participant` = `project.read`·`work.read`·`task.read`·`work_request.read` — **`task.assign` 이 없다** | `modules/organization_access/catalog.py:139` |
| `project-lead` = 그것 + **`task.assign` + `project.manage`** — **둘이 한 상수에 묶여 있다** | `catalog.py:145` |
| 열쇠는 `may_assign_in()` = `principal.allows(TASK_ASSIGN, project=…)` | `modules/work/projects.py:480-481` |

→ **그 프로젝트에서 배정할 수 있는 사람은 그 프로젝트를 관리할 수도 있다.** 「관리 권한 없이 그
프로젝트에서 배정할 수 있는 사람」이 **존재하지 않는다.**
새 테스트 `test_the_key_is_assigning_in_that_project_not_managing_it`
(`tests/contract/test_project_membership_follows_work.py:120-158`)은 오히려 **반대 방향**을 단언한다 —
관리 권한 없는 참여자 지호가 조직 축 배정 권한으로 **배정은 성공하지만 초대는 안 일어난다**(`:152-156`).

**어느 계약과 어긋나나.** 구현은 **어긋나지 않는다** — D-12 와 WP BE-2 작업 4(「열쇠는 `may_assign_in`,
`project.manage` 를 요구하지도 넓히지도 않는다」)를 그대로 지켰다. **어긋난 것은 SPEC 의 그 인수조건 줄과
현재 역할 카탈로그**다. BE 리포트 §7(가)가 이미 올렸다.

**한 줄 수정안.** 그 인수조건을 「**관리 권한을 열쇠로 묻지 않는다**」로 좁히거나(증명 가능),
참여자에게 프로젝트 범위 `task.assign` 만 주는 **역할 표 후속**을 따로 연다 — **코디 결정**.

### [WARN-2] 통과하지만 **아무것도 증명하지 않는 테스트 1건** — 단언이 항상 참이다

**무엇이.** `test_after_the_move_no_descendant_keeps_a_predecessor_in_the_old_project`
(`tests/contract/test_project_membership_follows_work.py:503-521`)의 핵심 단언
`assert set(row["preceding_task_ids"]) <= known` 이 **공집합 ⊆ known** 으로 **항상 참**이다.

**근거.** `_three_generations()`(`:422-430`)이 만드는 네 업무(`상위`·`자식`·`손자`·`증손자`)는
**어느 것도 선행을 갖지 않는다** — `_own()`(`:396`)과 `_handed_down()`(`:400`) 어디에도
`preceding_task_ids` 가 없다. 그래서 루프가 네 번 돌며 **빈 집합만 비교한다.**

**어느 계약과 어긋나나.** SPEC §6 손자 종속 마지막 줄 「이동 뒤 **어느 자손의 선행도 다른 프로젝트에
남아 있지 않다**」(`spec-005-projects.md:1035`)를 겨눈 **유일한** 테스트인데 그 줄을 증명하지 않는다.
⚠ 다만 **그 줄은 게이트 때문에 구조적으로 자명하다** — `_require_project_unlocked()`
(`modules/work/application.py:593-601`)이 자손 중 하나라도 **활성 선행을 들면 이동 전체를 거절**하므로,
선행을 든 자손이 있는 트리는 애초에 안 움직인다. **증명할 상태를 만들 수 없다.**

**한 줄 수정안.** 그 테스트를 지우고 그 줄의 근거를 `test_a_locked_grandchild_refuses_the_whole_move_and_nothing_budges`
(`:461-500`, **이건 실제로 증명한다**)에 귀속시키거나, 「게이트가 그 불변식을 구조적으로 보장한다」를
docstring 에 적어 **공허한 단언이 아니라 회귀 방지선**임을 밝힌다.

### [WARN-3] 「조건 ② 의 **활성**」을 워커가 정했다 — `cancelled` 만 뺀다

**무엇이.** `_holds_other_active_work()`(`modules/work/projects.py:271-296`)가
`str(task.state) != TaskState.CANCELLED.value` 하나로 걸러, **`done` 과 `completion_submitted` 까지
「활성 업무」로 센다**(`:290-292`).

**근거.** D-14 는 「그 사람의 **다른 활성 업무**」라고만 적고(`spec-005-projects.md:657`), 무엇이 활성인지
정하지 않았다. 함수 docstring 이 그 해석과 이유를 적어 **감추지 않았다**(`:274-277`).

**어느 계약과 어긋나나.** 어긋난다고 단정할 근거가 없다 — **D-14 가 답을 안 줬다.** 방향은
「사람이 남는 쪽」이고 D-15(「수락 뒤 종료는 그 일이 있었다는 뜻」)와 같은 결이라 **안전한 쪽**이다.
BE 리포트 §7(마)가 결정을 요청했다. **코디 판단 · `Open Issues` 에 남길 자리.**

### [WARN-4] **WP 가 이름 지은 기준선 파일이 없다** — Phase 0 의 입력이 사라졌다

**무엇이.** WP Phase BE-1 작업 0 이 기준선 기록을
`orchestration/work/strong-hajin-projects/flaky-baseline-projects.md` 에 **회차 1 로 남기라**고 적고
「**이 기록이 내일 Phase 0 의 입력이다**」라고 못 박는다(`work-005-projects.md:494-497`).

**근거.** 그 디렉토리에 `flaky` 나 `baseline` 이 들어간 파일이 **0건**이다(내가 `ls` 로 확인).
수치는 `be-impl-report.md` §1·§2 에 **회차 0·1·2 로 온전히 남아 있다** — 내용은 안 잃었고 **자리만 다르다.**

**한 줄 수정안.** `be-impl-report.md` §1·§2 를 그 경로로 발췌해 옮기거나, Phase 0 브리프가
`be-impl-report.md` §1·§2 를 입력으로 가리킨다.

### [WARN-5] 떼는 자리 #4 테스트가 **실제 표면을 지나지 않는다**

**무엇이.** `test_withdrawing_a_handover_proposal_takes_the_person_off`
(`tests/contract/test_project_membership_follows_work.py:269-300`)가 HTTP 를 건너뛰고
`application._assignments(session).cancel(...)` 를 **직접** 부른다(`:294-297`).

**근거.** SPEC §4 떼는 자리 4번의 표면은 `POST /api/action-items/{action_item_id}/commands/cancel_assignment`
(`spec-005-projects.md:683`)다. **연결은 실재한다** — 내가 확인했다:
`platform/action_center.py:619-623` 이 그 명령에서 `self._assignments.cancel(principal, assignment.id)` 를
부르고, 그 handler 는 **같은 session** 으로 조립된다(`bootstrap/application.py:4095-4108` · `action_center.py:1407`).
**테스트는 그 연결을 증명하지 않는다** — 메서드만 증명한다.

**한 줄 수정안.** 그 판단함 명령으로 한 번 더 통과시키거나, docstring 에
「표면→메서드 연결은 `action_center.py:619-623` 이 갖는다」를 적어 **무엇을 증명하지 않는지**를 밝힌다.

### [WARN-6] 자기 컬럼을 **방어적 `getattr(..., False)`** 로 읽는 자리 둘 — 이름이 바뀌면 자동 해제가 **전부 무동작**이 된다

**무엇이.** 조건 ① 을 읽는 두 자리가 기본값 있는 `getattr` 를 쓴다 —
`modules/work/assignments.py:366` · `modules/work/requests.py:740`
(`bool(getattr(assignment, "auto_project_join", False))`).

**근거.** 그 컬럼은 `platform/persistence.py:1790` 에 **실재**하므로 지금은 옳다. 그러나 이름이 바뀌거나
포트가 다른 객체를 넘기면 **조용히 「안 붙였다」로 읽혀 떼는 자리 넷이 전부 무동작**이 된다 —
브리프가 경계한 **「예외를 삼키는 폴백 · 조건이 항상 거짓인 가드」** 의 모양이다. 포트 타입이 `Any` 라서
쓴 것으로 보인다(`ProjectAssigneePort`·`RequestProjectMembershipPort` 의 인자가 `Any`).

**한 줄 수정안.** 기본값 없는 직접 속성 접근(`assignment.auto_project_join`)으로 바꾸거나,
배정 포트가 그 사실을 내는 메서드를 갖게 한다.

### [WARN-7] `ProjectTaskView` 의 **상태 계약 주석이 한 칸 위 필드에 붙었다**

**무엇이.** 「밖으로 나가는 상태는 계약의 넷뿐이다 … `completion_submitted` 는 투영이 `done` 으로 접어
새지 않는다」 주석이 `state:` 가 아니라 **`title:` 위**에 있다 —
`modules/work/project_results.py:49-52`(주석 `:50-51`, 그 아래가 `title: str`, 그 다음이 `state: str`).

**근거.** 동작 영향 **0** — `#:` 주석은 JSON 스키마에 실리지 않는다(인벤토리 diff 에 description 변경 0건,
내가 구조 비교로 확인). **계약 문서가 엉뚱한 필드를 가리키는 것**이 문제다.

**한 줄 수정안.** 주석 두 줄을 `state: str` 바로 위로 옮긴다.

### [WARN-8] **죽은 alias 하나**

**무엇이.** `TaskPredecessorSource = ProjectTaskFactSource`(`modules/work/projects.py:109`).

**근거.** `backend/src`·`backend/tests` 전체 grep 에서 **참조 0건**(그 선언 줄 자신뿐).
`ProjectApplication(...)` 호출처도 **하나**다(`bootstrap/application.py:4341`). 지킬 소비자가 없다.

**한 줄 수정안.** 지운다.

---

## 「조용히 통과하는 자리」 — 따로 본 결과

브리프가 지목한 다섯 모양을 각각 찾았다.

| 모양 | 결과 |
|---|---|
| **개명뿐인 변경** | **없다.** `_external_state`/`_overdue_days` 는 이름만 잇는 alias 로 남았지만(`application.py:2510`·`:2528`) 함수 본문이 **순수 모듈로 실제로 이동**했고, `work/projects.py` 가 **그 함수를 부른다**(`projects.py:418`·`:429`) — 두 표면이 같은 코드를 지난다. 「투영을 두 벌로 쓰지 않는다」가 실제로 성립한다 |
| **빈 단언** | **1건 → WARN-2** |
| **조건이 항상 참/거짓인 가드** | **없음(동작상).** 다만 `getattr(..., False)` 둘이 그 모양으로 **퇴화할 수 있다** → WARN-6. `_holds_other_active_work` 의 `if self._task_facts is None: return False`(`projects.py:288-289`)는 프로덕션 조립에서 **항상 None 이 아니다**(`bootstrap:4341`이 언제나 넘긴다) |
| **예외를 삼키는 폴백** | **없다.** diff 전체에 새 `try`/`except` 0건, 새 `raise` 0건 |
| **테스트가 실제 경로 대신 목을 검사** | **없다.** 새 계약 테스트 18건이 전부 `TestClient` 로 **실제 HTTP 라우트**를 지나고, 관측면도 실제 조회(`GET /api/projects` 셀렉터 · `/participation-history`)다. **목이 0건**이다. 예외는 #4 하나이고 그것도 목이 아니라 **application 메서드 직접 호출** → WARN-5 |

---

## §2 의 10개 항목 — 각각의 결과

### 1. 붙는 자리는 둘인가 — **PASS**

`grep -rn "join_for_assignment" backend/src` 의 **호출 2건**이 전부다:

| # | 자리 | 파일:줄 |
|---|---|---|
| 1 | 요청 발송 `WorkRequestApplication.create()` | `modules/work/requests.py:476` |
| 2 | 담당 교체 제안 `TaskAssignmentApplication.reassign()` | `modules/work/assignments.py:237`(호출), `:229`(흔적 기록) |

**직접 배정(`assign()`)에 초대가 없다** — `modules/work/assignments.py:106-140` 을 전문으로 읽었고
훅이 **한 줄도 없다.** 그리고 그 경로는 원리적으로 성립하지 않는 것이 맞다:
`create_assigned_task()` 의 `TaskRecord(...)`(`platform/work_tasks.py:2482~`)에 **`project_id` 가 없다.**
새 테스트가 그것을 「붙는 자리가 아니다」로 명시적으로 단언한다
(`test_direct_assignment_is_not_one_of_the_two_places`, `:169-186`).

### 2. 거는 자리가 application 메서드인가 — **PASS (세 입구를 내가 각각 따라갔다)**

**여섯 자리 전부 application 메서드**이고 `entrypoints/http.py`·`entrypoints/mcp.py` 는 **diff 에 없다**
(`git status` 로 확인). 입구별 수렴을 코드로 확인했다:

| 입구 | 요청 발송 | 담당 교체 | 요청 거절/철회 | 배정 거절 | 배정 철회 |
|---|---|---|---|---|---|
| HTTP | `http.py:1999` → facade `create_work_request` | facade `reassign_task`(`bootstrap:3030-3033`) | facade `reject/withdraw_work_request`(`:3222-3248`) | facade `decline_task_assignment`(`:3083-3085`) | — |
| MCP | `mcp.py:381`·`:1643` → 같은 facade | `mcp.py:626`·`:1831` → 같은 facade | 같은 facade | 같은 facade | — |
| action-center | `actions.py:710` → `task_creation` → **`creation_commands.py:152`·`:328` 가 `self._requests.create()` 를 부른다** | — | `action_center.py:254`·`:260` `self._work_requests.reject/withdraw` | `action_center.py:1153` `self._assignments.decline` | `action_center.py:623` `self._assignments.cancel` |

**우회 경로를 따로 찾았다.** `create_task_for_request`·`create_request` 를 application 밖에서 부르는
자리가 **0건**이고, `pending` `direct` 배정을 만드는 `hand_to()` 호출도 **`reassign()` 안의 1건뿐**
(`assignments.py:220`)이다 — **초대가 조용히 빠지는 입구가 없다.**

**트랜잭션 한 덩이도 확인했다.** `_work_requests(session)` 와 `_assignments(session)` 가 **같은 session** 으로
`self._projects(session)` 를 받는다(`bootstrap/application.py:4386` · `:3094`), action-center 도 같은
session 으로 조립된다(`:4095-4108`).

### 3. 떼는 자리 넷이 전부 구현됐나 — **PASS**

| # | 자리 | 구현 | 사유 |
|---|---|---|---|
| 1 | 요청 거절 | `requests.py:530`(→ `_release_project_for` `:724`) | `PROJECT_END_REQUEST_REJECTED` |
| 2 | 요청 철회 | `requests.py:722` | `PROJECT_END_REQUEST_WITHDRAWN` |
| 3 | 배정 거절 | `assignments.py:328` | 「요청 거절」 그대로 |
| 4 | **배정 철회** | `assignments.py:352` (`cancel()`) | 「요청 철회」 그대로 |

**사유는 둘뿐이다** — `modules/work/projects.py:86-87` 의 상수 둘이 유일한 원천이고, `grep` 으로
셋째 문자열이 없음을 확인했다. **#3 이 붙는 자리 둘의 종결을 함께 받는 것**도 테스트 둘로 각각 증명된다
(`:224-243` 요청 유래 행 · `:246-267` 담당 교체 제안 행).

### 4. 자동 해제의 조건 둘이 모두 걸렸나 — **PASS**

`release_for_assignment()`(`modules/work/projects.py:233-269`):

- **조건 ①** — `if not auto_joined or project_id is None or not member_id: return False`(`:261-262`).
  흔적은 `task_assignments.auto_project_join`(`platform/persistence.py:1790`) 한 칸이고,
  요청 쪽은 `request_assignment()`(`platform/work_tasks.py:1799`)가 `source_work_request_id` 로 찾는다.
- **조건 ②** — `if self._holds_other_active_work(...): return False`(`:263-264`).

**둘 다 없으면 나는 사고(원래 멤버를 뗀다)를 겨눈 테스트가 각각 있다** —
`test_an_original_member_is_not_taken_off_by_their_own_refusal`(`:305-321`, ① 거짓) ·
`test_someone_still_holding_other_work_here_stays_on`(`:324-336`, ② 거짓). 둘 다 통과.
「활성」의 범위만 워커가 정했다 → WARN-3.

### 5. 손자까지 따라가는가 — **PASS**

- `descendants_of()`(`platform/work_tasks.py:484-506`) — **BFS 반복 · `seen` 으로 본 것을 다시 보지 않는다.**
  `children_of()`(`:475-482`)는 **안 고쳤다**(diff 에 그 함수 변경 0줄).
- 게이트가 **자손 전체에** 걸린다 — `modules/work/application.py:540-546` 이
  `for descendant in descendants: self._require_project_unlocked(descendant)` 를 **먼저 다 돌고**,
  그 뒤 `:548-550` 에서 옮긴다. **부분 이동이 없다** — 거절이면 아무것도 mutate 되기 전에 던진다.
- 4층 트리(상위→자식→손자→증손자)가 전부 따라가는 것과, **손자에만** 선행을 걸었을 때 이동 전체가
  409 로 거절되고 **옛 프로젝트에 다섯 건이 그대로 남는 것**을 테스트가 증명한다(`:433-500`).

### 6. `_external_state()` 를 지나는가 — **PASS**

`modules/work/projects.py:418` `"state": external_state(task.state)`. 투영은
`modules/work/task_projection.py:35-46` **한 자리**이고 `work/application.py:2510` 이 그것을 alias 로 잇는다 —
**두 벌이 아니다.** `overdue_days` 는 **투영 앞의 원값**으로 판정한다(`projects.py:429` 주석대로).
`test_a_task_awaiting_approval_reads_as_done_on_the_project_screen_too`
(`tests/contract/test_projects.py:641-679`)가 두 표면의 값이 같음까지 단언한다.

### 7. 새 오류 이름을 지어내지 않았나 — **PASS**

`git diff -- backend/src` 에 **새 `class *Error` 0건 · 새 `raise` 0건**(정규식 grep). 이동 게이트는
기존 `TaskProjectLockedByPredecessors`(`modules/work/errors.py:140`, `WORK_PROJECT_LOCKED_BY_PREDECESSORS`, 409)
그대로다 — `application.py:599`. **`WORK_PREDECESSORS_UNFINISHED` 를 끌어오지 않았다**:
테스트가 거절 문구까지 「선행업무를 먼저 비워야」로 고정한다(`test_project_membership_follows_work.py:493`).
새 라우트·새 도구도 0건 — 인벤토리 `http_count` **159 불변** · `tool_count` **129 불변**.

### 8. 멱등인가 — **PASS**

`join_for_assignment()`(`projects.py:201-231`)가
`if self._repository.assignment(project.id, member_id, lock=True) is not None: return False`(`:217-218`).
그 조회는 **활성 행만** 본다(`platform/projects.py:105-109`, `ended_at IS NULL`) — 그래서
**이미 붙어 있으면 무동작**이고 **떼어진 뒤 다시 보내면 새 회차가 선다.** 승격도 없다(`kind="member"` 고정).
`test_sending_to_someone_already_on_the_project_changes_nothing`(`:107-117`)이 `lead` 가
`member` 로 **안 내려감**까지 단언한다.

### 9. 테스트가 실제로 증명하나 — **WARN 2건(WARN-2 · WARN-5), 나머지 PASS**

1~8 각각을 겨눈 테스트가 있다: ①→`:71-104`·`:169-186` · ②→(코드로만; 입구별 테스트는 없다) ·
③→`:189-300` 넷 · ④→`:305-336` 둘 · ⑤→`:433-500` · ⑥→`test_projects.py:641-679` ·
⑦→`:493` 문구 고정 + 인벤토리 · ⑧→`:107-117`.
**증명 안 하는 것 하나**(WARN-2)와 **실제 표면을 안 지나는 것 하나**(WARN-5).
그 밖 사소한 것: `test_project_membership_follows_work.py:150` 의 `current = …` 가 **`:152` 에서 즉시
덮어써져 쓰이지 않는다**(죽은 줄); `test_projects.py:560` 의
`row["assignee"] == {"member_id": "mina", "display_name": row["assignee"]["display_name"]}` 는
display_name 쪽이 **자기참조**다 — 바로 다음 줄(`:561`)이 실제 검사를 하므로 공허하지는 않다.

### 10. 범위를 넘지 않았나 — **PASS**

| 제약 | 결과 |
|---|---|
| `frontend/` 변경 | **0건** (`git status` 에 `frontend` 0줄) |
| 첨부(material) | **동작 변경 0건.** 닿은 유일한 파일은 `tests/contract/test_task_fields_and_materials.py` **+5줄**이고, 바뀐 것은 `test_start_sets_a_missing_start_date_to_the_seoul_business_day` 의 **얼린 시계를 `task_projection` 에도 거는 한 줄**이다 — 첨부 기능이 아니다. `material_*` 소스·테스트는 **0줄** |
| `tasks_in()` 필터·페이징 | **0건** — `platform/projects.py:204-209` 가 여전히 `select(TaskRecord).where(project_id==…).order_by(created_at)` 뿐이다 |
| 커밋·push | **0건** — `HEAD == origin/main == e46ce39`, staged 0, 변경은 워크트리에만 |
| 그 밖 | 새 표 0개(컬럼 하나만) · `docs/domain-model.md` 대조표 한 줄 추가 · 인벤토리 diff 가 **`get_project` 도구 `output_schema` 한 칸**(구조 비교로 확인: `$defs` 둘 추가 + `ProjectTaskView` 속성 5개 추가 + `required` 7→12, **그 밖 변경 0**, `acceptance_evidence` 무변경) |

**WP 완료 판정 중 미충족 2건 — 숨기지 않고 적는다.** 「커밋 후 API 를 다시 띄웠다」(BE-1·BE-2 각 1줄)는
**안 됐다.** BE 브리프가 커밋과 사용자 포트·프로세스를 금지했으므로 **워커 잘못이 아니고 코디 몫**이다
(BE 리포트 §7(바)가 같은 말을 한다).

---

## 테스트 실측 — **내가 다시 돌렸다**

`-p no:randomly` 를 쓰지 않았다(이 저장소에 `pytest-randomly` 가 없어 무동작). 직렬은 `-n0`.

| 무엇 | 명령 | 내 실측 | BE 리포트 주장 | 일치 |
|---|---|---|---|---|
| 도메인·구조·**대장 drift** | `make test-unit` | **369 passed**, 1 deselected, 10.62s | 369 passed | ✓ |
| 계약 전체(병렬) | `make test-contract` | **1183 passed · 1 failed**, 283.32s, exit 2 | 회차 2: 1183 / 1 | ✓ |
| 이번 판 계약만 직렬 | `make test-contract-serial FILES="test_projects.py test_project_membership_follows_work.py test_project_commands.py test_task_assignments.py test_task_predecessors.py test_task_fields_and_materials.py"` | **86 passed**, 52.60s, exit 0 | 86 passed | ✓ |
| DB·제약·동시성 회귀 | `make test-postgres POSTGRES_TEST_URL=…/ax_test_projects` | **103 passed**, 1567 deselected, 153.56s, exit 0 | 103 passed, 1567 deselected | ✓ |

### 기존 실패와 이번 판의 실패 — 갈라서 적는다

**이번 판이 만든 실패: 0건.**

**기존(범위 밖) 실패: 1건** — `tests/contract/test_material_worker_recovery.py::test_stage_timeout_fences_the_late_parser_result`
(`assert ['failed','running'] == ['failed','completed']`).

**그것이 기존 흔들림임을 내가 따로 증명했다** — 그 파일만 **직렬(`-n0`)로 돌리면 5 passed · exit 0** 이다.
즉 **병렬에서만 넘어진다.** 그리고 그 파일은 이번 diff 에 **없고**(17 파일 목록 밖), 이번 변경 17 파일 중
material 워커 경로에 닿는 것이 **0건**이다.

### 회차마다 실패 파일 집합이 바뀐다 — 그 사실을 적는다

| 회차 | 누가 | 실패한 **파일** | 실패 건수 |
|---|---|---|---|
| 0 (BE 기준선, 착수 전) | BE | `test_material_worker_recovery.py` | **2** |
| 1 (BE 구현 뒤) | BE | 같은 파일 **1** + `test_task_fields_and_materials.py` **1**(BE 가 고침) | 2 |
| 2 (BE 최종) | BE | `test_material_worker_recovery.py` | **1** |
| **3 (내 재측정)** | **나** | `test_material_worker_recovery.py` | **1** |
| **직렬 단독** | **나** | **없음** | **0** |

**파일 집합은 3회차 내내 `test_material_worker_recovery.py` 하나**이고, **그 안에서 어느 건이 넘어지는지가
회차마다 바뀐다**(2 → 1 → 1 → 1). 내 회차 3 은 BE 회차 2 와 **같은 한 건**이었다.
→ **내일 Phase 0 의 입력**: 흔들리는 파일은 하나, 병렬에서만 넘어진다.

---

## 기존 부채 (이번 판정 제외)

- **직접 배정으로 만든 하위 업무는 상위의 프로젝트를 안 물려받는다** — `create_assigned_task` 의
  `TaskRecord(...)`(`platform/work_tasks.py:2482~`)에 `project_id` 가 없고 `project_for()` 도 지나지 않는다.
  그래서 그 하위는 **어느 프로젝트 화면에도 안 선다.** 앞 판 검수가 이미 「기록만」으로 남긴 자리이고
  이 판이 **건드리지 않았다**(건드리지 않는 것이 맞다 — SPEC 이 세어서 뺐다).
- **불변식 3 의 동시성 틈** — 같은 사람에게 보낸 업무 둘이 **동시에** 거절되면 둘 다 상대의 활성 업무를
  보고 **아무도 안 뗀다.** `_holds_other_active_work` docstring(`projects.py:279-283`)이 감추지 않고 적었고,
  결과는 「사람이 프로젝트에 남는 것」으로 **안전한 쪽**이다. WP §불변식 3 이 미리 적은 그대로다.
- `assignee.display_name` 이 명부에서 안 나오면 **`member_id` 로 대체된다**
  (`projects.py:423` `names.get(member_id, member_id)`). 기존 `member_names` 의 결과가 비는 경우에만이고
  계약이 그 자리를 정하지 않았다 — **기록만.**

---

## 확인한 것 / 확인 안 한 것

**확인한 것** — §2 10개 항목 전부(위) · 「조용히 통과하는 자리」 다섯 모양 전부 · 앞 판 검수 재발 점검
(아래) · 인벤토리 구조 비교(프로그램으로) · 테스트 4회 실행.

**앞 판(WP 검수) 지적의 재발 — 없다.**

| 앞 판 | 이번 코드에서 | 근거 |
|---|---|---|
| FAIL-1 직접 배정에 초대를 걸었다 | **재발 없음** | `assign()` 에 훅 0줄 · 「붙는 자리가 아니다」 테스트 존재 |
| FAIL-2 흔적을 두 원장에 나눴다 | **재발 없음** | `task_assignments.auto_project_join` **한 칸**이고, 요청 쪽은 `source_work_request_id` 로 그 행을 찾는다(`work_tasks.py:1799-1818`) — 배정 거절로 닫아도 같은 칸을 읽는다(테스트 `:224-243`) |
| WARN-1 `-p no:randomly` | **재발 없음** | `Makefile:46-50` 의 새 타겟이 `-n0` 만 쓴다 |
| WARN-5 「지연」을 상태 무관으로 셈 | **재발 없음** | `overdue_days()` 가 `done`·`cancelled`·`completion_submitted` 에 `None`(`task_projection.py:24-27`·`:49-57`) |

**확인 안 한 것** — ① **실서버 `curl` 검증**(브리프가 포트·프로세스 금지). BE 가 TestClient 안에서 찍은
`be-impl-report.md` §6 응답 예시는 **내가 재현하지 않았다** — 다만 그 필드 집합이 `ProjectTaskView`
(`project_results.py:49-70`)와 계약 테스트 단언과 **한 칸도 안 틀린다**는 것은 확인했다.
② **`make sync-demo-schema` 재실행**(스키마를 건드리는 명령이라 read-only 검수에서 돌리지 않았다) —
`manual[]` 이 비었다는 주장은 **컬럼이 nullable 이고 `server_default` 가 없다**는 코드 사실
(`persistence.py:1790`)과 일관하다. ③ `frontend/` 전체와 Phase 0·첨부 계약(범위 밖).
④ SPEC §6 인수조건 75줄의 **FE 몫**(이 판의 대상이 아니다).

---

## 코디에게 — 무엇부터

1. **WARN-1 과 WARN-3 은 코디·SPEC 결정이다.** 둘 다 BE 가 리포트에서 이미 올렸고 **코드를 고칠 일이
   아니다.** WARN-1 은 인수조건 한 줄을 좁히거나 역할 표 후속을 여는 것, WARN-3 은 「활성」의 범위를
   못 박는 것 — 둘 다 `Open Issues` 에 남아야 FE 와 2루프가 흔들리지 않는다.
2. **WARN-2 · WARN-5 · WARN-6 은 BE 워커에게 한 번에 재발주할 만한 묶음**이다(각 한두 줄).
   WARN-7 · WARN-8 은 같은 통에 담으면 된다.
3. **WARN-4 는 코디가 지금 닫을 수 있다** — `be-impl-report.md` §1·§2 를
   `flaky-baseline-projects.md` 로 옮기거나 Phase 0 브리프가 그 절을 가리키게 한다.
4. **FE-1 발주를 막을 이유가 없다.** BE-1 의 산출물(I-1~I-6)이 전부 실물로 서 있고
   계약 테스트가 그것을 고정했다.
