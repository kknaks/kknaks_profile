# BE 재수정 결과 보고 — 검수 WARN 다섯 (FAIL 0)

## 상태: done

워크트리 `/Users/kknaks/orca/workspaces/Strong_hajin/strong-hajin-projects`, 브랜치
`kknaksss/strong-hajin-projects`, base `e46ce39`. **커밋·push 0건** — 변경은 워크트리에만 있다.
**`frontend/` 는 한 줄도 열지 않았다** (FE 워커가 동시에 붙어 있다).
**서버·사용자 포트 0건** — postgres 54329 는 **이미 떠 있었고 내가 띄우지 않았다.**

---

## 1. WARN 다섯 — 각각 어떻게 닫혔나

### WARN-2 (지시문) — 빈 단언을 진짜 단언으로 · **닫음**

`test_after_the_move_no_descendant_keeps_a_predecessor_in_the_old_project`
(`backend/tests/contract/test_project_membership_follows_work.py`)를 **다시 썼다.**
옛 테스트의 `assert set(row["preceding_task_ids"]) <= known` 은 트리에 선행이 하나도 없어
**공집합 ⊆ known 으로 언제나 참**이었다.

새 테스트가 재는 것 셋 — 전부 **값이 있는 집합** 위에서:

1. **손자가 실제로 선행을 든다.** 프로젝트 P 안에 조부모→자식→**손자**→증손자를 세우고 P 안의
   다른 업무 `선행` 을 **손자에** 건 뒤, 프로젝트 화면의 선행 변 집합에 `(손자, 선행)` 이
   **실제로 서는 것**을 먼저 단언한다(`_edges()` 헬퍼 — 화면이 간트 연결선을 긋는 바로 그 배열).
2. **그 선행이 이동 전체를 막는다** — 409 `WORK_PROJECT_LOCKED_BY_PREDECESSORS`,
   거절 문구 「선행업무를 먼저 비워야」 고정, 그리고 **Q 에 아무것도 움직이지 않았다.**
3. **선행을 풀면 옮길 수 있고 손자까지 따라온다** — 네 업무 전부 Q, 옛 프로젝트 P 에는
   `선행` **하나만** 남는다. 그 뒤 **Q 안에서 선행을 다시 이어** 관측 집합을 비지 않게 만든 상태로
   「옛 프로젝트를 가리키는 변 0건」을 센다(`edges == {(손자, Q의 선행)}` · `preds ⊆ known` ·
   `preds & left_behind == ∅` · 뗀 선행 `earlier` 가 다시 서지 않음).

**「구조적으로 자명하다」가 깨지는 경로를 실제로 잡는지 뮤테이션으로 확인했다.**
`work/application.py` 의 `for descendant: self._require_project_unlocked(descendant)` 를 `pass` 로
바꾸면 **이 테스트가 FAIL 한다**(같이 `test_a_locked_grandchild_refuses_the_whole_move…` 도 FAIL).
소스는 즉시 원상복구했다 — `git diff` 에 뮤테이션 흔적 0건.

### WARN-6 (지시문) — `getattr(…, 'auto_project_join', False)` 제거 · **닫음**

**읽는 자리를 하나로 모으고 폴백을 지웠다.**

- 새 모듈 수준 헬퍼 `auto_joined_by(assignment)` — `modules/work/projects.py`
  (자동 해제 사유 상수 둘 바로 아래, 같은 계약이 사는 자리).
  **폴백 없는 직접 속성 접근**(`assignment.auto_project_join`)이고, `None`(배정 행이 아예 없는 것 —
  요청 쪽에서 실제로 일어난다)만 거짓으로 접는다.
- 부르는 자리 둘이 그것을 쓴다: `modules/work/assignments.py`(떼는 자리 #3·#4) ·
  `modules/work/requests.py`(떼는 자리 #1·#2). **`src` 전체에 `getattr(..., "auto_project_join", ...)`
  0건**(grep 확인).

**그 칸이 없으면 실패하는 것을 테스트로 보였다** — 신규 `backend/tests/unit/test_project_auto_join_flag.py` 3건:
- 행에서 곧바로 읽는다(True/False/`None`)
- **배정 행이 없는 것**(`None`)은 「칸이 사라진 것」과 다른 사실이다
- **칸 이름이 바뀐 행을 넘기면 `AttributeError`** — 여기서 `False` 가 나오는 날이
  **떼는 자리 넷이 전부 조용히 멈춘 날**이고, 그때 깨지는 테스트가 이것 하나다.

### WARN-5 (지시문) — 기준선 기록 파일 · **만들었다**

`orchestration/work/strong-hajin-projects/flaky-baseline-projects.md` (신규).
회차 0~4 의 passed/failed·소요·exit · **회차마다 어느 파일의 어느 건**이 넘어졌는지 ·
`test_material_worker_recovery.py` 만 `-n0` 로 돌리면 **5 passed · exit 0** 이라는 증명 ·
**이번 판이 만든 실패 0건**의 근거 넷 · Phase 0 가 받아야 할 것.

⚠ **`-p no:randomly` 정정을 §0 에 못 박았다** — 이 저장소에 `pytest-randomly` 가 없어 그 플래그는
**무동작**이고, 어느 회차도 그것으로 직렬화하지 않았다. **직렬화는 전부 `-n0`** 였다
(`Makefile:46-50` 의 `test-contract-serial` 도 `-n0` 하나뿐). reference 문서가 그 플래그로 직렬 증명을
했다고 적는다면 **그 전제는 다시 재야 한다.**

### WARN-7 (지시문) — 떼는 자리 #4 테스트가 표면을 지나게 · **표면 테스트를 새로 넣었고, 한 가지를 보고한다**

**새 계약 테스트** `test_the_cancel_assignment_surface_lands_in_the_one_method` 가
**판단함 라우트를 실제로 지난다**: AX `task.assign` 제안 → `confirm` →
`POST /api/action-items/{id}/commands/cancel_assignment` → 배정 `cancelled` · 업무 `cancelled`.
봉투가 그 명령 하나만 내는 것(`allowed_commands == ["cancel_assignment"]`)까지 단언한다.
**뮤테이션 확인**: `platform/action_center.py:619-623` 의 `self._assignments.cancel(...)` 를 지우면
**이 테스트가 FAIL** 한다(소스 즉시 복구, diff 0건).

⚠ **그런데 그 표면으로는 「같은 결과」가 나올 수 없다 — 감추지 않고 적는다.**
`cancel_assignment` 봉투는 **`task.assign` AX 제안에만** 서고(`modules/actions/policy.py:129-136`),
그 제안의 초안은 `project_id` 를 **언제나 `None` 으로 못 박는다**
(`modules/work/drafts.py:35` · `TaskAssignmentInput.read_legacy_empty_project`,
`modules/work/task_creation.py:118-126`). 게다가 신규 경로는 배정을 바로 `active` 로 세우므로
그 명령이 서려면 과거 모양(`pending`)이어야 한다.
→ **프로젝트가 걸린 유일한 `pending` 배정**(담당 교체 제안이 `hand_to()` 로 세우는 행)에는
**오늘 철회 표면이 HTTP·MCP·판단함 어디에도 없다.** `TaskAssignmentApplication.cancel()` 을 부르는
자리는 `action_center.py:619-623` 하나뿐이고 그 자리는 위 이유로 프로젝트를 가질 수 없다.

그래서 이렇게 갈랐다:
- **표면→메서드 수렴**은 위 새 테스트가 **실제 라우트로** 증명한다.
- **프로젝트가 걸린 철회의 자동 해제**는 `test_withdrawing_a_handover_proposal_takes_the_person_off`
  가 계속 메서드로 잰다. docstring 에 **왜 메서드로 재는지와 표면이 없다는 사실**을 적었고,
  「표면이 생기면 이 테스트가 그 표면으로 올라와야 한다」를 남겼다.

**코디 결정이 필요한 자리다**: SPEC §4 가 떼는 자리 #4 의 표면으로 적은
`POST /api/action-items/{id}/commands/cancel_assignment` 는 **담당 교체 제안이 세운 배정에는
오늘 서지 않는다.** SPEC 의 그 줄을 좁히거나, 그 배정에도 철회 명령이 서게 하는 후속을 따로 연다.

### WARN-8 (지시문) — 두 가지 정리 · **닫음**

- `modules/work/project_results.py` — 「밖으로 나가는 상태는 계약의 넷뿐」 주석 두 줄을
  `title:` 위에서 **`state: str` 바로 위로** 옮겼다.
- `modules/work/projects.py` — 죽은 alias `TaskPredecessorSource = ProjectTaskFactSource` **삭제**.
  `backend/src` · `backend/tests` · `docs/` grep 참조 **0건** 확인.

### 덤 — 검수 §9 가 적은 죽은 줄 하나

`test_project_membership_follows_work.py` 의 `current = …` 가 두 줄 뒤에서 즉시 덮어써지던 자리
하나를 지웠다(동작 무관, 1줄).

---

## 2. 바꾼 파일 — 여섯 (전부 `backend/`)

| 파일 | 무엇을 |
|---|---|
| `backend/src/ax_workspace/modules/work/projects.py` | `auto_joined_by()` 추가 · 죽은 alias 삭제 |
| `backend/src/ax_workspace/modules/work/assignments.py` | `getattr` 폴백 → `auto_joined_by()` |
| `backend/src/ax_workspace/modules/work/requests.py` | `getattr` 폴백 → `auto_joined_by()` |
| `backend/src/ax_workspace/modules/work/project_results.py` | 상태 계약 주석을 `state:` 위로 |
| `backend/tests/contract/test_project_membership_follows_work.py` | WARN-2 재작성 · 표면 테스트 1건 추가 · 죽은 줄 1 삭제 |
| `backend/tests/unit/test_project_auto_join_flag.py` (신규) | 칸이 없으면 실패하는 것을 보이는 단위 테스트 3건 |

**새 오류 이름 0건 · 새 라우트 0건 · 새 도구 0건 · 스키마 변경 0건 · `docs/` 변경 0건.**
운영 대장(`docs/unified-operations-inventory.json`) 은 **이번 판이 건드리지 않았다** —
`tests/architecture` 의 drift 테스트가 통과한다.

---

## 3. 테스트 재측정 — **기존 실패와 갈라서**

| 무엇 | 명령 | 결과 |
|---|---|---|
| 도메인·구조·**대장 drift** | `make test-unit` | **372 passed**, 1 deselected, 10.65s, **exit 0** (앞 판 369 + 이번 판 3) |
| 계약 전체(병렬) | `make test-contract` | **1181 passed · 4 failed**, 1185 collected, 384.32s, exit 2 — **실패 4건 전부 `material_*` 계열**, 아래 참조 |
| 이번 판이 닿은 계약만 직렬 | `make test-contract-serial FILES="test_projects.py test_project_membership_follows_work.py test_project_commands.py test_task_assignments.py test_task_predecessors.py test_task_fields_and_materials.py test_action_center.py"` | **125 passed**, 77.21s, **exit 0** |
| 흔들리는 파일만 직렬 | `make test-contract-serial FILES="tests/contract/test_material_worker_recovery.py"` | `test_material_search.py` + `test_material_worker_recovery.py` **20 passed**, 46.00s, **exit 0** |
| DB·제약·동시성 회귀 | `make test-postgres POSTGRES_TEST_URL=…/ax_test_projects` | **103 passed**, 1571 deselected, 159.54s, **exit 0** |

**`-p no:randomly` 는 쓰지 않았다** — 미설치라 무동작이다. 직렬화는 전부 **`-n0`**.

### 새 실패 — **0건**. 다만 **흔들림이 두 파일로 넓어진 것은 감추지 않는다**

병렬 회차 4 의 실패 **4건**은 회차 3 의 **1건**보다 늘었다. 내역:

| 파일 | 건 | 단언 |
|---|---|---|
| `test_material_worker_recovery.py` | `test_long_parse_heartbeats_its_lease…` | `assert ('queued' == 'running')` |
| `test_material_worker_recovery.py` | `test_stage_timeout_fences_the_late_parser_result` | `assert ['running','running'] == ['failed','completed']` |
| **`test_material_search.py`** ← 회차 4 에 처음 | `test_searching_without_naming_the_work_finds_what_this_person_may_read` | `assert set() == {'남견적.md'}` |
| **`test_material_search.py`** | `test_when_a_material_was_registered_is_a_different_question_from_what_it_says` | `assert set() == {'8월정리.md'}` |

**넷 다 「자료 파싱 워커가 아직 안 갔다」는 단언**이다 — 값이 *다른* 상태가 아니라 **이전** 상태로 온다
(`queued`·`running`·색인 전 빈 집합). 그리고 **그 두 파일만 `-n0` 로 돌리면 20 passed · exit 0** 이다.

**이번 판 탓이 아닌 근거 넷** (자세히는 `flaky-baseline-projects.md` §4):
1. 실패가 전부 `material_*` 계열이고, 이번 판이 바꾼 여섯 파일에 material 경로가 **0줄**이다.
2. 직렬 격리가 통과한다(20 passed · exit 0).
3. 실패 단언이 전부 「아직 진행 안 함」이다 — 계약이 다른 값을 내는 것이 아니다.
4. 이번 판이 닿은 계약 7파일 직렬 **125 passed · exit 0** · `make test-unit` **372 passed · exit 0** ·
   `make test-postgres` **103 passed · exit 0**.

⚠ **관측 하나를 같이 적는다**: 같은 스위트의 소요가 **283.32s(회차 3) → 384.32s(회차 4)** 로 36% 늘었고,
회차 4 동안 **같은 기기에서 FE 워커가 동시에 돌고 있었다.** 부하가 커질수록 이 계열이 더 넘어지는
모양과 일치한다 — **단정이 아니라 관측**이다.

---

## 4. 다른 팀 영향 (FE)

**없다.** envelope·응답·라우트·오류 코드·스키마가 **한 칸도 바뀌지 않았다.**
`ProjectTaskView` 는 필드 집합·순서 그대로이고 옮긴 것은 `#:` 주석 두 줄뿐이다
(JSON 스키마에 실리지 않는다 — 대장 drift 테스트가 통과한다).

---

## 5. 이슈 / 코디 결정이 필요한 것

1. **떼는 자리 #4 의 표면이 실제로는 닫히지 않는다** (위 WARN-7 ⚠). SPEC §4 의 그 줄을 좁히거나
   담당 교체 제안이 세운 `pending` 배정에도 철회 명령이 서게 하는 후속을 연다.
2. 앞 판 검수의 **WARN-1(역할 표 ↔ SPEC §6 인수조건)** · **WARN-3(조건 ② 의 「활성」 범위)** 는
   **코드가 아니라 SPEC·역할 표 결정**이다 — 이번 판이 건드리지 않았다. `Open Issues` 에 남아야 한다.
