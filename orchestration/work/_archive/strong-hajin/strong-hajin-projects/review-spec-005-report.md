# 리뷰 리포트 — strong-hajin-projects / SPEC-005 계약 검수 (2026-09-21)

## 판정: **FAIL 4건 · WARN 5건**

핵심 넷(손자 행 · 접어도 안 사라지는 의존선 · 프로젝트 밖 사람 초대와 거절 시 해제 · 이동 시 손자
추종)은 계약으로도 인수조건으로도 **전부 서 있다.** 저장 구조 누수도 **0건**이다. 깨진 것은 네
자리다 — **상태 어휘를 계약에 없는 다섯으로 올린 것** · **프로젝트 이동 게이트를 틀린 오류 갈래에
건 것** · **떼는 자리 하나가 통째로 빠진 것** · **DEC-004 가 정한 적 없는 것에 `(확정 — D-NN)`
을 단 것 셋.** 넷 다 코드나 상위 문서로 근거가 나온다.

## 검수 범위

- 문서: `spec-005-projects.md`(1000줄) 전문 · `decision-004-projects.md`(828줄) D-01~D-27 전수 ·
  `baseline-004-projects.md` · `spec-001` · `spec-003` · `spec-004` 대조 · `20-spec/README.md` § Data / Domain Boundary
- 코드(read-only): `/Users/kknaks/orca/workspaces/Strong_hajin/strong-hajin-projects`
- 실행한 검사: 라우트 전수 grep(159중 `/api/*` 리터럴 전부 추출) · `task.assign`/`TASK_ASSIGN`/`may_assign_in`
  전수 grep · `_external_state` · `_require_project_unlocked` · `children_of` · `tasks_in` ·
  `ProjectTaskView` · `taskStateTone` · `TaskState`(FE) · `modules/work/errors.py` 전수
- **테스트·빌드·서버는 돌리지 않았다** (역할 규칙 `roles/.../reviewer/tools.md`)
- 쓴 파일: 이 리포트 하나. 문서·코드 수정 0건, 커밋 0건

---

## 위반 (FAIL)

### [FAIL-1] 상태 어휘를 「외부 5종」으로 올렸다 — 계약은 넷이다

**무엇이.** `spec-005-projects.md:385-400`(§2.9 표) · `:656`(Validation 「밖으로 나가는 상태 =
**외부 5종뿐이다** … (확정 — D-06)」) · `:700`(Data Contract 「업무의 상태 어휘 | **외부 5종** —
`open`·`in_progress`·`blocked`·`done`·`cancelled` | (확정 — D-06)」) · `:860`(인수조건 「라벨이
**「시작 전」·「막힘」**이다」)이 `blocked` 를 **계약 어휘로 확정**한다.

**무엇과 어긋나나 — 셋 전부와 어긋난다.**

| 출처 | 무엇이라 적혀 있나 |
|---|---|
| `spec-003-task-lifecycle-v2.md:204` | **「수행 상태는 넷이다 (정책)」** — `open`·`in_progress`·`done`·`cancelled` |
| `spec-003-task-lifecycle-v2.md:888` | §4 Data Contract 표도 **넷** |
| `spec-003-task-lifecycle-v2.md:214` | 「`blocked` 「막힘」 \| **이 계약에 없다** \| SPEC-001 계승. 코드에 남아 있다 — **M-6 (미정)**」 |
| `spec-003-task-lifecycle-v2.md:839` | 「**`blocked` 와 `completion_submitted` 는 이 계약에 없다**」 |
| BE `backend/src/ax_workspace/modules/work/application.py:2496` | `_external_state` docstring: **「밖으로 나가는 수행 상태는 넷뿐이다」** |
| BE `application.py:2503-2504` | 「**`blocked` 도 계약에 없지만** 이 work 는 그 값을 발행하지도 없애지도 않는다(M-6) — 들어오는 그대로 낸다. **없는 계약을 여기서 지어내지 않는다**」 |
| FE `frontend/src/lib/viewModels.ts:110` | 「수행 상태 — **넷이 계약이다** (SPEC-003 §4 Data Contract)」 |
| FE `viewModels.ts:117-118` | 「`blocked` 는 **이 판이 없애지 않는다** — **계약에는 없고(M-6 미정)** 코드에는 남아 있어서…」 |

**그리고 D-06 이 그것을 정하지 않았다.** `decision-004-projects.md:189-206` 의 D-06 이 말하는 것은
둘뿐이다 — ①「백엔드 `TaskState` 가 정본, 시안 5종은 폐기」 ②「**톤 5종**이 시안과 한 칸도 안
틀리므로 색은 시안 그대로 쓴다(`labels.ts:20-26`)」. **「외부 어휘가 다섯이다」는 D-06 에 없다.**
`labels.ts:20-26` 에 톤이 다섯 있는 것은 **렌더 상수표의 사실**이지 계약의 사실이 아니다 —
같은 저장소가 `viewModels.ts:117` 에서 바로 그 값을 「계약에 없다」고 적는다.

**어떻게 고치면 되나.** §2.9·§4 를 **「외부 계약은 넷. `blocked` 는 SPEC-003 M-6 미결을 그대로
승계한다 — 코드에 남아 있어 화면은 라벨·톤을 갖되 이 SPEC 이 계약 어휘로 올리지 않는다」** 로 고치고,
근거를 `(확정 — D-06)` 에서 **SPEC-003 M-6 승계**로 바꾼다. 화면 동작(배지·바 색)은 한 줄도 안 바뀐다.

---

### [FAIL-2] 프로젝트 이동 게이트를 **틀린 오류 갈래**에 걸었다 — 그리고 기존 어휘는 여섯이 아니라 일곱이다

**무엇이.** `spec-005-projects.md:666` 이 「기존 어휘가 **여섯 갈래**로 이미 있다」고 세고,
`:675` 가 그 여섯 중 **「끝나지 않은 선행」(HTTP 409)** 행에 D-19 를 걸어
「**적용 범위가 자손 전체로 넓어진다 (확정 — D-19)**」라고 적는다. `:678` 도
「그 게이트가 막는 사유가 **끝나지 않은 선행**이므로 어휘도 그 갈래다」로 못 박는다.

**무엇과 어긋나나 — 코드가 다른 예외를 던진다.**

- D-19 가 가리킨 게이트는 `_require_project_unlocked` 다
  (`decision-004-projects.md:457-478` · `spec-005:632`).
- 그 함수는 `backend/src/ax_workspace/modules/work/application.py:579-586` 이고,
  던지는 것은 **`TaskProjectLockedByPredecessors`** 다 —
  `errors.py:140-145`: 「남은 선행이 있는 업무의 프로젝트를 바꾸려 했다
  (SPEC-001 **`WORK_PROJECT_LOCKED_BY_PREDECESSORS`**, 409)」.
- 스펙이 건 「끝나지 않은 선행」은 **다른 클래스**다 — `errors.py:148`
  **`TaskPredecessorsUnfinished`** = `WORK_PREDECESSORS_UNFINISHED`, 그리고 그 docstring 이
  「**시작하거나 `시작 전 → 완료` 로 직행**」이라고 적는 **전이 게이트**다.
  조사 리포트도 같다 — `research-be-domain.md:175`: 「끝나지 않은 선행이 있으면
  `open → in_progress` 와 `open → done` **두 문만** 막는다」.
- 그래서 **「여섯 갈래」도 틀렸다.** `errors.py:110~155` 의 선행 계열은 **일곱**이다 —
  `ProjectRequired`·`ProjectMismatch`·`Self`·`Duplicate`·`Cycle`(이상 422) ·
  **`ProjectLockedByPredecessors`(409)** · `PredecessorsUnfinished`(409).
  스펙의 여섯에서 빠진 것이 정확히 **이번에 넓히려는 그 갈래**다.
  (조사도 `research-be-domain.md:168-173` 에서 **선행 편집 다섯**만 열거했다 — 스펙은 거기에
  전이 게이트 하나를 더해 여섯으로 만들었고, 이동 게이트는 양쪽 다 안 셌다.)

**왜 위험한가.** 표대로 구현하면 **전이 게이트(`WORK_PREDECESSORS_UNFINISHED`)를 이동 경로로
넓히게 되고**, 프로젝트 이동 거절의 **HTTP 응답 코드 이름이 바뀐다.** SPEC-005 자신의
「새 오류 코드 0건」(`:702`)이 그 자리에서 깨진다.

**어떻게 고치면 되나.** §4 에러 표를 **일곱 갈래**로 고치고
**`WORK_PROJECT_LOCKED_BY_PREDECESSORS`(409)** 행을 세워 D-19 의 「자손 전체로 넓어진다」를
**그 행으로** 옮긴다. 이것으로 **OQ-601 의 후반(게이트 예외 이름)은 닫힌다.**

---

### [FAIL-3] 떼는 자리에 **「직접 배정·담당 교체 제안의 철회」**가 통째로 빠졌다

**무엇이.** `spec-005-projects.md:609-616` 의 「떼는 자리 — **셋**. 붙는 자리 셋의 **부정 종결**이다」
표는 ① 요청 거절 ② 요청 철회 ③ 배정 거절(`POST /api/task-assignments/{assignment_id}/decline`)
셋만 센다. **직접 배정·담당 교체 제안의 「철회」가 없다.**

**내가 직접 센 결과.** `grep -rn "task\.assign|TASK_ASSIGN|may_assign_in" backend/src/` →
`modules/work/assignments.py` 의 `self._require(principal, TASK_ASSIGN)` 은 **여섯 자리**다:

| 줄 | 메서드 | 무엇 | 스펙의 처분 |
|---|---|---|---|
| `assignments.py:72` | `candidates()` | 읽기 | 뺀 자리 ✓ |
| `assignments.py:108` | `assign()` | 직접 배정 | **붙는 자리 #2** ✓ |
| `assignments.py:153` | `plan_project_work()` | 「사람은 아직 정하지 않는다」 | 뺀 자리 ✓ |
| `assignments.py:177` | `reassign()` | 담당 교체 제안 | **붙는 자리 #3** ✓ |
| `assignments.py:225` | `sent()` | 읽기 | 뺀 자리(암묵) |
| **`assignments.py:301`** | **`cancel()`** | **「Withdraw a direct assignment before the assignee answers it」** | **어느 표에도 없다** ✗ |

- `cancel()` 은 `assignment_kind == "direct"` 인 pending 배정을 철회한다(`assignments.py:302-310`).
- 그 `"direct"` 를 만드는 자리가 **둘**이다 — `platform/work_tasks.py:2461`(직접 배정) ·
  **`work_tasks.py:2569`(담당 교체 제안)**. 즉 **붙는 자리 #2·#3 의 철회 종결이 바로 이것**이다.
- 표면도 실재한다 — `POST /api/action-items/{action_item_id}/commands/{command}` 의
  `cancel_assignment`(`platform/action_center.py:619-623` 이 `self._assignments.cancel(...)` 를 부른다 ·
  명령 정의 `modules/actions/policy.py:136` · `platform/actions.py:539`).

**무엇과 어긋나나.** **D-13**(`decision-004:343-357`)이 정한 것은 「**거절·철회**되면 뗀다」이고,
SPEC-005 자신의 인수조건 `:898` 이 「**요청 철회에서도 같은 규칙이 돈다 — 거절만 다루고 철회를
빠뜨리지 않는다**」를 요구한다. 그런데 표가 **배정 쪽 철회**를 빠뜨렸다.
표 자신이 「붙는 자리 셋의 **부정 종결**」이라고 선언했으므로, 붙는 자리 #2·#3 의 부정 종결이
**둘(거절·철회)인데 하나만 적힌 것**은 표 자신의 규칙 위반이기도 하다.

**어떻게 고치면 되나.** 떼는 자리를 **넷**으로 늘리고 4번 행에
「직접 배정·담당 교체 제안의 **철회**(`cancel_assignment` / `POST /api/action-items/{id}/commands/cancel_assignment`)
— 사유는 **「요청 철회」**를 그대로 쓴다」를 세운다. 새 사유가 안 생기므로 D-13 의 「사유는 둘」이 지켜진다.

---

### [FAIL-4] DEC-004 가 정한 적 없는 것에 `(확정 — D-NN)` 을 달았다 — 세 자리

스펙 머리의 표기 규약(`spec-005:62`)이 `(확정 — D-NN)` 을 「**DEC-004 의 결정 NN 번이 채택한 것.
뒤집으려면 새 사용자 결정이 필요하다**」로 정의한다. 아래 셋은 그 정의에 해당하지 않는데 그 표기를 달았다 —
**코디 제안이 사용자 확정으로 승격되어 있다.**

| # | 스펙 자리 | 무엇에 달았나 | 그 D-NN 이 실제로 정한 것 |
|---|---|---|---|
| a | `spec-005:235`(요약 스트립 「지연」 칸) · `:520`(`tasks[]` 「기한 경과일」) | **(확정 — D-04)** | `decision-004:152-166` D-04 는 **「전체 진행률 = 완료 업무 수 / 전체 업무 수」 하나만** 정한다. 기한 경과·「지연」 칸은 **한 글자도 없다** — 실제 근거는 스펙이 같은 줄에 병기한 **SPEC-001 §U-3 승계**(`spec-001-work-management.md:200`)다 |
| b | `spec-005:337`(우 레일 체크리스트 「**읽기 전용이다**」) | **(확정 — D-20)** | `decision-004:480-492` D-20 은 **「좌 레일 카드 클릭의 뜻은 선택이다 / 여는 것은 한 줄로 따로 둔다」**뿐이다. **체크리스트를 읽기 전용으로 할지는 정한 적이 없다** — 새 제안이다(인수조건 `:874` 가 그것을 검증 대상으로 세운다) |
| c | `spec-005:206`(좌 레일 「**기존 업무 카드를 그대로 재사용한다**」) | **(확정 — D-10)** | `decision-004:277-294` D-10 은 **「DS 정본은 `src/ds`+`src/styles`, `.design-sync/` 는 거울」**이다. 부품 재사용의 근거는 같은 줄이 병기한 **BASE-004 § 부품 재고**이지 D-10 이 아니다 |

**왜 지적하나.** 「조용히 통과하는 자리」다 — 번호는 맞고 내용이 그 결정과 다르다. b 는 특히
**정정 가능한 코디 제안이 「새 사용자 결정 없이는 못 뒤집는 것」으로 굳는다.**

**어떻게 고치면 되나.** a·c 는 `(도출)` 로 내리고 근거를 각각 SPEC-001 §U-3 · BASE-004 § 부품 재고로
바꾼다. b 는 `(제안)` 으로 내린다. 셋 다 계약 내용은 그대로 두고 표기만 바꾸면 된다.

---

## 경미 (WARN)

### [WARN-1] OQ-601 의 전반은 **이미 닫혀 있다** — 라우트가 코드에 있다

`spec-005:572`(「발송·철회의 경로는 그 슬라이스 밖이라 조사에 없다 → OQ-601」) · `:613-614`(⚠ OQ-601) ·
`:967-974`. **한 번의 grep 으로 나온다:**

- `POST /api/work-requests` — `entrypoints/http.py:1992` (요청 발송)
- `POST /api/work-requests/{request_id}/withdraw` — 라우트 전수 목록에 실재 (요청 철회)
- `POST /api/work-requests/{request_id}/reject` — 실재 (요청 거절)

「조사 슬라이스 밖」은 **조사 리포트의 한계**이지 「코드에 이름이 없다」가 아니다. 스펙이 세운 원칙
(「없는 이름을 지어내지 않는다」)은 지켜졌지만, **미결로 남길 필요가 없던 것**이 미결로 남았다.
FAIL-2 와 합치면 **OQ-601 은 통째로 닫힌다.**

### [WARN-2] 붙는/떼는 자리를 **HTTP 라우트로만** 셌다 — MCP·action-center 경로가 조용히 빠질 수 있다

같은 명령이 **세 입구**로 들어온다:
- HTTP — `entrypoints/http.py`
- **MCP** — `entrypoints/mcp.py:215` `task.assign` · `:187` `task.reassign` · `:204` `project.plan_work`
  가 전부 `TASK_ASSIGN` 에 걸려 있고, `mcp.py:1140` 이 `task.assign` 액션을 낸다.
  도구 정의도 `modules/ax_execution/tool_catalog.py:73,84,257,461,470` 에 있다
- **action-center 명령** — `POST /api/action-items/{id}/commands/{command}`(FAIL-3 참조)

그런데 `spec-005:757-760`(§5)은 「**공통 지점으로 보이는 곳에 걸지 않는다** … 명령이 도는 그 자리에
건다」고 적는다. 표가 라우트 목록이라서, 구현자가 **HTTP 라우트 3곳에만** 걸면 MCP 배정이
**조용히 초대를 안 한다** — 스펙이 경계한 바로 그 실패 모양이다.

**권장 수정 한 줄:** 「명령이 도는 그 자리 = `TaskAssignmentApplication.assign()` ·
`reassign()` · 요청 발송의 application 메서드다. **entrypoint 가 아니다**」를 §5 에 박는다.
(`assignments.py:108,177` 이 그 자리이고 세 입구가 전부 그리로 모인다.)

### [WARN-3] 인수조건 하나가 관측 불가하다

`spec-005:878` — 「관리 권한이 없는 사람에게 그 손잡이가 **서버 판정대로** 처리된다 — 화면이
추측하지 않는다」. **무엇을 보면 통과인지가 없다.** 서버는 `may_manage: bool` 을 이미 낸다
(`modules/work/project_results.py:40` · `modules/work/projects.py:234-235`).
**권장 수정:** 「`may_manage` 가 거짓인 사람의 헤더에 관리 모달 손잡이가 **렌더되지 않는다**」.

이 한 줄 말고는 관측 가능하다 — 핵심 넷을 포함해 「올바르게 동작한다」류 문장은 **0건**이다.

### [WARN-4] 깊이 정책을 SPEC-003 과 **화해시키는 한 줄이 없다**

`spec-005:108` 은 「SPEC-003 의 상태·전이표·**상위/하위**·중심 업무 판정을 **그대로 물려받는다**」고
적는데, SPEC-003 은 화면 깊이를 다르게 적는다:
- `spec-003:740` — 「저장 깊이 \| **제한 없음**(정책 V-6). **화면 두 단계와 무관하다**」
- `spec-003:720` — 「`children` — **직속 하위만**(정책 L-11)」

D-16 이 푸는 것은 **이 화면의 표시 깊이**이고 저장·`children` 계약이 아니므로 **실질 충돌은 없다.**
다만 문서만 읽는 사람에게는 모순으로 보인다.
**권장 수정:** §1 관계 절에 「SPEC-003 의 「화면 두 단계」는 **그 화면들의 표시 규칙**이고,
이 화면은 `children` 이 아니라 프로젝트 상세의 **평면 `tasks[]`** 에서 트리를 만든다」 한 줄.
(근거는 실재한다 — `platform/projects.py:204-209` `tasks_in` 은 `WHERE project_id = ?` 뿐이라
**깊이와 무관하게 전부** 낸다. D-16 의 전제는 코드에서 참이다.)

### [WARN-5] 표 이름 하나가 남아 있다

`spec-005:152` — 「시간 배정의 변경 — SPEC-004 그대로. **`task_schedules`** 를 건드리지 않는다」.
같은 문서가 §4 에서 다른 표 이름(`task_dependencies`·`task_checklists`)을 전부 「**우리 이름이
정본이다**」로 감춘 것과 결이 다르다. 실질 누수는 아니다(Out of scope 한 줄).
**권장 수정:** 「시간 배정의 저장을 건드리지 않는다」로 충분하다.

---

## 기존 부채 (이번 판정 제외)

- 어긋남 ① 은 **코드에서 확인된다** — `modules/work/projects.py:244` 가 `"state": task.state` 를
  원값 그대로 싣는다(`_external_state()` 를 안 지난다). SPEC-005 의 서술이 맞다.
- `research-be-domain.md:168-173` 이 선행 거절을 **다섯**으로만 열거했다 —
  `TaskProjectLockedByPredecessors` 가 조사에서도 빠져 있다(FAIL-2 의 뿌리).

---

## §2 확인 항목 — 7개 전부의 결과

### 1. 결정 27건 전수 대조 · **발주서 번호 vs DEC-004 본문**

- **작성자의 보고가 맞다.** `decision-004-projects.md` 본문 번호를 직접 확인했다:
  `:398` D-16 = 깊이 제한 없는 재귀 트리 · `:426` D-17 = 접힌 가지 의존선 · `:440` D-18 =
  들여쓰기 12px/최대 5단 · `:457` D-19 = 손자 프로젝트 종속 · `:480` D-20 = 카드 클릭 = 선택 ·
  `:496` D-21 = 헤더 `actions` · `:514` D-22 = 빈 상태 하나 · `:526` D-23 = `cancelled` 바 ·
  `:541` D-24 = `Empty` 글리프 유지 · `:553` D-25 = `titleEnd` 안 더함 · `:566` D-26 = 사이드바 ·
  `:578` D-27 = 필터·페이징 범위 밖.
  **SPEC-005 §6 추적표(`:918-947`)가 12건 전부 이 번호와 일치한다.** DEC-004 를 따른 것이 옳다.
- 27건 **전부에 자리가 있다** — 추적표의 「이 SPEC 의 어디」 칸을 §2~§6 에서 실제로 대조해
  빈 참조 0건을 확인했다.
- **번호가 아니라 내용이 다른 자리 셋** — **FAIL-4** (D-04 / D-20 / D-10).
- **D-06 은 내용이 결정을 넘어섰다** — **FAIL-1**.

### 2. 저장 구조 누수 — **0건 (PASS)**

`컬럼|column|인덱스|index|FK|foreign|migration|마이그레이션|ORM|repository|테이블|schema|CHECK|Alembic`
전수 grep → 걸린 9줄이 **전부 경계 선언이거나 부정문**이다(`:38` 경계 명시 · `:104`·`:154`·`:739`
「저장 컬럼을 만들지 않는다」 · `:149` 「`30-work/` 몫」 · `:691` 「DB 컬럼·인덱스·FK 는 코드와
migration 이 SoT」 · `:852` 응답 관측 · `:920` 추적표).
백틱 식별자도 전수로 뽑았다 — 남은 표 이름은 **시안 목데이터의 이름**(`task_dependencies`·
`task_checklists`·`tasks.progress`·`tasks.parent_id`)과 **응답 필드**(`span_from`·`span_to`)뿐이다.
유일한 우리 표 이름은 `:152` `task_schedules` 하나 → **WARN-5**.
`20-spec/README.md` § Data / Domain Boundary 기준으로 **FAIL 없음.**

### 3. 「새 라우트 0건 · 새 오류코드 0건」이 사실인가 — **라우트 PASS · 오류 FAIL**

- **라우트: 스펙이 쓰는 경로가 전부 실재한다.** `entrypoints/` 의 `/api/*` 리터럴을 전수 추출해
  대조했다 — `GET/POST /api/projects` · `/api/projects/{project_id}` · `/members` ·
  `/members/{member_id}` · `/participation-history` · `/api/projects/{project_id}/tasks` ·
  `GET /api/tasks/{task_id}` · `POST /api/tasks` · **`POST /api/tasks/assign`** ·
  **`POST /api/tasks/{task_id}/reassign`** · `/api/tasks/{task_id}/proposals` ·
  `/proposals/{proposal_id}/respond` · `/withdraw` · `/api/task-assignments/{assignment_id}/accept` ·
  **`/decline`** · `/api/task-assignment-candidates` · `/api/work-requests`.
  **없는 이름을 쓴 자리 0건.** 새 라우트 주장도 참이다.
- **오류: 갈래 수와 매핑이 틀렸다** → **FAIL-2**. 「새 코드 0건」이라는 결론 자체는 지킬 수 있지만,
  표대로 구현하면 **틀린 기존 코드**를 쓰게 된다.

### 4. 자동 초대 표면 「붙는 3 / 뺀 6 / 떼는 3」 — **붙는 3·뺀 6 은 맞고, 떼는 3 은 FAIL**

`task.assign`·`TASK_ASSIGN`·`may_assign_in` 전수 grep 으로 직접 셌다.
- **붙는 자리 3 — 맞다.** 사람이 지명되는 배정 진입점은 `assignments.py:108` `assign()` ·
  `:177` `reassign()` · 요청 발송(`POST /api/work-requests`, http.py:1992) 셋이다.
- **뺀 여섯 — 맞다.** `assignments.py:153` `plan_project_work()` 는 docstring 이 직접
  「**사람은 아직 정하지 않는다**」라고 적어 스펙의 사유와 한 글자도 안 틀린다.
  `:72` `candidates()`·`:225` `sent()` 는 읽기. `accept`·`proposals`·`members` 도 스펙 판단대로다.
  열쇠가 `may_assign_in` 인 것도 실재한다 — `modules/work/projects.py:299-300`.
- **떼는 자리 3 — 하나 빠졌다** → **FAIL-3** (`assignments.py:301` `cancel()`).
- 입구 다중성 → **WARN-2**.

### 5. 인수조건이 관측 가능한가 — **PASS (WARN 1건)**

- **핵심 넷이 전부 있다**: 손자 행 `:790-792` · 접어도 안 사라지는 의존선 `:796-797` ·
  프로젝트 밖 사람 초대와 거절 시 해제 `:798-802` · 이동 시 손자 추종 `:803-804`.
- 「올바르게 동작한다」류 **0건**. 대부분 수·유무·개수로 적혀 검산 가능하다
  (예: `:840` 「5개 중 2개 → **40%**」, `:847` 「전체 진행률 = 완료 칸 ÷ 전체 업무 칸」,
  `:836` 「후행을 서버에 묻는 호출이 **0건**」).
- 관측 불가 한 줄 → **WARN-3** (`:878`).

### 6. 기존 스펙과 충돌 — **상태 어휘 FAIL · 깊이 정책 WARN · 나머지 PASS**

- **상태 어휘** → **FAIL-1** (SPEC-003:204·214·839·888 과 정면 충돌).
- **깊이 정책** → **WARN-4** (SPEC-003:720·740 과 화해 문장 부재. 실질 충돌 아님).
- **SPEC-004 와의 기간 규칙 — 일치한다.** `spec-004:1010` 의 네 경우(① 구간 ② 한쪽만이면
  그 날 하루 ③ 둘 다 없으면 없음 ④ 뒤집히면 `[min,max]`)와 `spec-005:650` 이 **같은 문장**이고,
  이름도 `span_from`·`span_to` 로 같다(`spec-004:1150`). BE 에도 실재한다
  (`modules/work/schedule.py` `task_span`). **같은 사실을 두 규칙으로 읽지 않는다** — 지켜졌다.
- **SPEC-001 과 — 일치한다.** `spec-001:200` 의 「진행률은 쓰지 않는다 / 기한 경과일 `+N`」을
  `spec-005:104-105` 가 뒤집지 않고 승계한다. 「기한 경과일」은 SPEC-003:342 의 `overdue_days` 와
  같은 값이라 새 어휘가 아니다.
- **SPEC-003 상위/하위 · 중심 업무 · 전이표** — 이 SPEC 은 표시만 하고 바꾸지 않는다(`:110`). 충돌 없음.

### 7. 시안 기하 — **PASS (한 칸도 안 틀린다)**

`baseline-004-projects.md` · `design-read-projects.md` 와 값 단위로 대조했다.

| 값 | 스펙 | BASE-004 | 결과 |
|---|---|---|---|
| 좌 레일 380px | `:194` | `:67`·`:283` (`--scax-rail-left-width` → `--ax-inbox-w`) | ✓ |
| 우 레일 342px | `:195` | `:68`·`:284` (`--scax-rail-right-width` → `--ax-calendar-w`) | ✓ |
| 행 40px | `:254` | `:103` | ✓ |
| 하루 34px | `:255` | `:101-102` | ✓ |
| 라벨 200px | `:256` | `:103` | ✓ |
| 바 22/14/18px | `:257` | `:107` | ✓ |
| 요약 값 24/32px bold·`tabular-nums` | `:232` | `:94` | ✓ |

**변경된 값 둘 다 D-18 이 근거로 달려 있다** — `spec-005:253`
「들여쓰기 **깊이당 12px · 최대 5단** … **(확정 — D-18)**」이고, `decision-004:440-455` 의 D-18 이
그것을 정하며 근거(24px×3 = 제목 128px만 남음 → 12px 면 164px)까지 적는다. **D-18 본문도
「나머지 기하는 시안 그대로 — 행 40px·바 22/14/18px·하루 34px. 여기서 바꾸는 것은 들여쓰기 한 값뿐」**
이라 스펙과 일치한다. 「5단에서 멈추는 것은 들여쓰기이고 행이 아니다」(`spec-005:263`)도
D-18 `:449-453` 과 같다.

---

## 재발주 시 확인할 것 (요약)

1. §2.9 · §4 의 「외부 5종」 → **넷 + M-6 승계** (FAIL-1)
2. §4 에러 표 → **일곱 갈래**, 이동 게이트는 `WORK_PROJECT_LOCKED_BY_PREDECESSORS` (FAIL-2)
3. §4 떼는 자리 → **넷** (`cancel_assignment` 추가) (FAIL-3)
4. `(확정 — D-04/D-20/D-10)` 셋 → `(도출)`/`(제안)` 로 강등 (FAIL-4)
5. OQ-601 → **닫는다** (`POST /api/work-requests` · `/withdraw` · `WORK_PROJECT_LOCKED_BY_PREDECESSORS`)
6. §5 에 「거는 자리 = application 메서드, entrypoint 아님」 한 줄 (WARN-2)
7. `:878` 인수조건을 `may_manage` 로 관측 가능하게 (WARN-3)
