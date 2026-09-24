# 리뷰 리포트 — strong-hajin-projects / WORK-005 빌드 계획 검수 (2026-09-21)

## 판정: **FAIL 4건 · WARN 6건**

계획의 **뼈대는 서 있다** — 인수조건 75줄을 내가 직접 세어 대조했고 수는 한 칸도 안 틀린다.
거는 자리 일곱은 전부 application 메서드이고 줄번호가 전부 실재한다. 검증 타겟도 전부 실재한다.
**깨지는 곳은 「코드가 실제로 그렇게 돌지 않는」 자리 둘과, 앞 판 지적의 재발 하나, 그리고 인수조건 한 줄의 오배정**이다.

## 검수 범위

- 대상: `para/projects/summer-star/strong-hajin/30-work/work-005-projects.md` (1222줄, 전문)
- 대조: `20-spec/spec-005-projects.md`(§6 인수조건 75줄 전수 재계수) · `10-decision/decision-004-projects.md`(D-01·D-08·D-13~D-15·D-19) ·
  `orchestration/work/strong-hajin-projects/review-spec-005-report.md`(앞 판 FAIL 4 · WARN 5)
- 코드(read-only, `/Users/kknaks/orca/workspaces/Strong_hajin/strong-hajin-projects`, `e46ce39`, 워크트리 clean):
  `modules/work/{assignments,requests,projects,application,project_results,task_creation}.py` ·
  `platform/{work_tasks,projects,persistence,action_center}.py` · `entrypoints/http.py` ·
  `Makefile` · `backend/pyproject.toml` · `docs/unified-operations-inventory.json` ·
  `tests/architecture/test_operation_inventory.py` · `frontend/src/{App.tsx,lib/api.ts,lib/viewModels.ts,ds,styles,features/project}`
- **테스트·빌드·서버 기동 0건** (검수 규약). 문서·코드 수정 0건 — 산출물은 이 파일 하나.

---

## 위반 (FAIL)

### [FAIL-1] 붙는 자리 #2(직접 배정)는 **코드상 자동 초대가 절대 안 돈다** — 그 업무에는 프로젝트가 없다

**무엇이.** WP `:267` 이 붙는 #2 를 `TaskAssignmentApplication.assign()`(`assignments.py:89`)에 걸고,
BE-2 완료 판정 `:607-608` 이 **「붙는 자리 셋 각각에 테스트가 있다 — 요청 발송·직접 배정·담당 교체 제안.
하나라도 빠지면 실패다」**를 완료 조건으로 세운다. **그 테스트는 통과할 수 없다.**

**근거.**

| 사실 | 파일:줄 |
|---|---|
| `assign()` 이 부르는 `create_assigned_task()` 가 만드는 `TaskRecord` 에 **`project_id` 가 없다** — 인자에도 본문에도 없다 | `platform/work_tasks.py:2413-2455` |
| 그게 실수가 아니라 **의도**다: `TaskAssignmentInput` 이 **non-null `project_id` 를 받기를 거부**한다 — 주석이 「A non-null project is not owned by assignment creation」이라고 적는다 | `modules/work/task_creation.py:115-126` |
| 부모의 프로젝트를 물려받는 자리는 `project_for()` 인데 **`assign()` 은 그것을 지나지 않는다** — `parent_for()` 만 부르고 `record_subtask()` 는 프로젝트를 안 건드린다 | `modules/work/application.py:360-367` · `:486-491` · `assignments.py:121-135` |
| `tasks.project_id` 는 nullable 이고 기본값이 없다 | `platform/persistence.py:939` |

그래서 `assign()` 이 세운 업무는 **언제나 `project_id = NULL`** 이고, WP 가 스스로 적은
「**업무에 프로젝트가 없으면 아무 일도 일어나지 않는다**」(`:577`)에 **항상** 걸린다.

**같은 뿌리의 둘째 증상 — 그 흔적 칸은 읽히는 자리가 없다.** `create_assigned_task` 는 배정 행을
`status="active"` 로 낳는다(`work_tasks.py:2460-2462`). `decline()` 은 `status=="pending"` 만 받고
(`assignments.py:348-349`), `cancel()` 은 `pending` 이 아니면 거절한다(`:309-310`).
**즉 #2 에는 떼는 자리가 하나도 없다** — `task_assignments.auto_project_join` 에 #2 몫으로 쓴 값은
영원히 안 읽힌다. SPEC `:1010-1011` 의 「붙는 자리 **#2**·#3 의 부정 종결이 둘씩 다 있다」도 그래서 안 선다.

**무엇과 어긋나나.** WP `:267`·`:571`·`:607-608` · SPEC-005 §4 `:629`(붙는 #2) · §6 `:991`·`:1010-1011`.
**계획이 코드 사실과 다르다.**

**한 줄 수정안.** 붙는 #2 를 **`reassign()` → `hand_to()`(프로젝트 업무에 첫 담당을 붙이는 자리,
`work_tasks.py:2316-2330`, `plan_project_work()` 가 만든 업무가 그 대상)**로 다시 지목하고,
`assign()` 은 「**프로젝트가 없어 무동작**」으로 명시한 뒤 완료 판정의 그 줄을 「무동작임을 보인다」로 바꾼다 —
계약이 갈리면 몰래 고치지 말고 **SPEC 환류**로 올린다.

---

### [FAIL-2] 떼는 자리는 **넷이 아니다** — 요청 발송이 만든 배정 행도 `decline` 으로 닫힌다

**무엇이.** WP `:269-272`·`:579` 가 떼는 자리를 넷으로 세고, 흔적을 **두 원장에 나눠** 둔다 —
#1(요청 발송)은 `work_requests.auto_project_join`, #3(담당 교체 제안)은 `task_assignments.auto_project_join`
(WP `:314-320`·`:327`). **그 가정은 「요청은 요청 경로로만 끝난다」인데, 코드는 그렇지 않다.**

**근거.**

| 사실 | 파일:줄 |
|---|---|
| 요청 발송이 업무와 **함께 `TaskAssignmentRecord`(`status="pending"`, `assignment_kind="request_effect"`)를 만든다** | `platform/work_tasks.py:1938-1957` |
| 배정 수신함 조회 `pending_for()` 가 **`assignment_kind` 를 안 가린다** — 그 행이 그대로 뜬다 | `platform/work_tasks.py:2490-2497` |
| `decline()` 의 관문 `_pending_target()` 도 **kind 를 안 본다** — 수신자 본인 + `pending` 이면 통과 | `modules/work/assignments.py:318-350` |
| 그 거절이 `supersedes_assignment_id` 가 없으므로 **업무를 `CANCELLED` 로 닫는다** — 요청 거절과 같은 결과 | `platform/work_tasks.py:2653-2663` |

→ **받는 사람이 `POST /api/task-assignments/{id}/decline` 로 답하면**, 붙인 흔적은 `work_requests` 에 있는데
떼는 코드는 `task_assignments` 쪽 칸만 본다. **거짓으로 읽혀 자동 해제가 안 돈다.**
WP `:327` 이 두 표로 나눈 이유로 든 「**한 표에 모으면 다른 원장의 종결이 그 칸을 못 찾는다**」도 코드와 다르다 —
그 배정 행이 **`source_work_request_id` 로 요청을 이미 가리킨다**(`work_tasks.py:1952`).

**무엇과 어긋나나.** WP `:269-272`(떼는 자리 표) · `:327`(두 표인 이유) · `:609`(완료 판정 「떼는 자리 넷 각각」) ·
SPEC-005 §4 `:670-686`. **전수라고 선언한 표에 다섯째 길이 있다**(`feedback_enumerate_all_surfaces` 의 결).

**한 줄 수정안.** 떼는 #3 에 「그 배정이 `source_work_request_id` 를 들면 **요청 쪽 흔적도 본다**」를 한 줄로 박거나,
흔적 칸을 **`task_assignments` 한 곳으로 모으고** reject/withdraw 는 그 컬럼으로 행을 찾는다 —
어느 쪽이든 **코디가 정하고 `Open Issues` 에 남긴다.**

---

### [FAIL-3] 앞 판 FAIL-4 의 재발 — `(확정 — D-19 「부분 이동은 없다」)` 는 **D-19 에 없는 말**이다

**무엇이.** WP `:370` 이 「게이트를 거는 순서」의 근거를 **`(확정 — D-19 「부분 이동은 없다」)`** 로 적는다.

**근거.**

- `decision-004-projects.md:457-477`(D-19 전문)에 **「부분 이동」이라는 말이 한 번도 안 나온다.**
  그 문서 전체 grep 결과 **0건**.
- 같은 사실을 **SPEC-005 가 적었고, 거기서는 `(도출 — 게이트의 뜻)`** 이다 — `spec-005-projects.md:706`.
- 앞 판 검수 `review-spec-005-report.md:132-151`(FAIL-4)이 **정확히 이 패턴**을 지적해 셋을 `(도출)`·`(제안)` 으로 내리게 했다:
  「번호는 맞고 내용이 그 결정과 다르다 — 코디 제안이 사용자 확정으로 승격되어 있다.」

**무엇과 어긋나나.** 표기 규약(`spec-005:62`: `(확정 — D-NN)` = 「DEC-004 결정 NN 이 채택 · 뒤집으려면 새 사용자 결정」).
**SPEC 이 (도출)로 표시한 것을 WP 가 (확정)으로 올리고, 없는 문장에 인용부호까지 달았다.**

**한 줄 수정안.** `(도출 — 게이트의 뜻 · SPEC-005 §4)` 로 내리고 인용부호를 뗀다. 계약 내용은 그대로 둔다.

---

### [FAIL-4] 인수조건 한 줄이 **닫을 수 없는 Phase** 에 배정됐다 — 그리고 어느 완료 판정도 그 줄을 안 든다

**무엇이.** WP `:1039` 이 **의존선 묶음 C 5줄 전부를 FE-2** 에 준다.
그중 `spec-005:931` 은 **「후행 목록이 우 레일에 나온다 — 그것은 클라이언트가 뒤집어 만든 것이다」**이고,
**우 레일은 FE-3 이 만든다**(WP `:767` Phase 제목 · `:783-786` 작업 3 「관계(선행 건수+목록 · **후행 건수+목록**)」).

**근거.**

- FE-2 는 「간트와 의존선」이고 우 레일이 없다 — WP `:633`「아직 간트도 우 레일도 없다」·`:693` Phase 제목.
- **FE-2 완료 판정(`:745-763`)에 그 줄이 없다** — 있는 것은 「후행을 서버에 묻는 호출이 0건」(`:755`)뿐이고, 그건 `spec-005:930` 의 다른 줄이다.
- **FE-3 완료 판정(`:817-835`)에도 없다.** 우 레일 항목 다섯 중 후행 목록을 겨눈 줄이 0개다.

**무엇과 어긋나나.** WP `:1033`「**전수 매핑한다 — 닫는 Phase 가 없는 줄은 없다**」.
수로는 75 가 맞지만(내가 직접 세어 확인했다) **자리가 틀렸고, 실질적으로 아무 Phase 도 그 줄을 증명하지 않는다.**

**한 줄 수정안.** C 묶음을 **FE-2 4줄 / FE-3 1줄**로 가르고, FE-3 완료 판정에
「우 레일 후행 목록이 뜨고 그 원천이 클라이언트 역산이다」 한 줄을 더한다(Phase 부담 표 `:1056-1057` 의 19/11 도 18/12 로).

---

## 경미 (WARN)

### [WARN-1] `-p no:randomly` 는 이 저장소에서 **아무 일도 안 한다** — 「둘 다 끈다」가 거짓이다

- WP `:517`·`:967`「**`-p no:randomly -n0`** — 랜덤 순서와 병렬을 **둘 다 끈다**」.
- **`pytest-randomly` 가 설치돼 있지 않다** — `backend/pyproject.toml:32-37` 의 dev 그룹은 `httpx`·`pytest`·`pytest-xdist` 셋뿐이고, `uv.lock` 에 `pytest-randomly` **0건**. `addopts`(`:40`)에도 랜덤 플러그인이 없다.
- 실효 스위치는 **`-n0` 하나**다. (앞 판 재료 `material-parallel-isolation.md:28` 이 같은 플래그를 적었고 그것도 무해한 no-op 이었다.)
- **수정안**: 「`-n0` 가 병렬을 끈다. `-p no:randomly` 는 이 저장소에 랜덤 플러그인이 없어 무해한 무동작이다」로 한 줄 고친다.

### [WARN-2] 대장 drift 를 잡는 **테스트 이름이 틀렸다** — 두 자리

- WP `:398`·`:1176` 이 `test_inventory_lists_every_registered_tool` 이라고 적는다. **그런 함수가 없다.**
- 실제로 도구의 `output_schema` 를 통째로 비교하는 것은
  **`test_inventory_schemas_match_the_actual_registered_tools()`** — `backend/tests/architecture/test_operation_inventory.py:104`, 비교 자리는 `:122`.
- **주장 자체는 맞다**(내가 직접 확인: `get_project` 도구 스키마에 `ProjectTaskView`·`preceding_task_ids` 실재, `list_projects`·`project_list` 에는 없음. `http_count` 159 · `tool_count` 129 · `GET /api/projects/{project_id}` 의 `http_signature` = `(project_id: UUID, principal: Principal) -> ProjectDetailResult`). **이름만 고치면 된다.**

### [WARN-3] `preceding_task_ids` 는 FE 에서 **「기존」이 아니다** — 타입에도 없고 읽는 코드도 없다

- WP `:445`(I-6)이 「`preceding_task_ids`(**기존**) … 의존선의 **유일한 원천**」이라 적고 짝을 「**기존** ↔ FE-2·FE-3」으로 둔다.
- 그러나 `frontend/src/lib/viewModels.ts:95-102` 의 `ProjectDetail.tasks` 는 **여섯 필드**(`task_id`·`title`·`state`·`start_date`·`due_date`·`parent_task_id`)뿐이고 **`preceding_task_ids` 가 없다.**
  `frontend/src` 전체 grep 에서 `features/project` 쪽 사용 **0건**(있는 것은 `features/work` 의 `DirectTask` 뿐).
- FE-1 작업 8(`:658-659`)은 「타입을 넓히고 `state` 를 `TaskState` 로 조인다」까지만 적는다 — **BE-1 이 새로 더한 것만 넓히면 FE-2 가 재료 없이 시작한다.**
- **수정안**: FE-1 작업 8 에 「`preceding_task_ids: string[]` 도 같이 세운다 — 서버는 이미 내지만 FE 타입에 없다」 한 줄.

### [WARN-4] FE-2 헤더의 「갈라지는 3줄」은 **5줄**이다

- WP `:697-698`「= **19줄** (+ BE-1·FE-1 과 갈라지는 **3줄**)」.
- 같은 문서의 갈라지는 줄 표(`:1070-1076`)에서 **FE-2 가 절반을 드는 줄은 다섯**이다 — BE-1 과 둘(한쪽 날짜만·뒤집힌 기간), FE-1 과 셋(취소 2건·`blocked`·선택 축).
- 합계 75 는 안 깨진다(부담 표 `:1049-1060` 은 맞게 센다). **헤더 숫자만 3 → 5.**

### [WARN-5] 「지연」의 **「상태와 무관하게」**가 서버 함수와 갈린다 — 구현자가 둘로 읽는다

- WP `:654`·`:684` 「「지연」은 … **상태와 무관하게** 겹쳐 센다 — 진행 중인 업무도 기한을 넘겼으면 센다」.
- 서버의 `_overdue_days()` 는 **`done`·`cancelled`·`completion_submitted` 에 `None` 을 낸다** — `modules/work/application.py:2521-2529`(`:2526`). 「끝난 일에는 지연이 없다」가 그 함수의 주석이다.
- WP 는 같은 문서에서 「**화면이 「오늘」을 재판정하지 않는다**」(`:511`·`:443`)고 못 박으므로 **실제 동작은 서버 규칙**인데, 「상태와 무관」을 곧이 읽은 구현자는 「완료했지만 기한 넘긴 업무도 센다」는 테스트를 쓰고 막힌다.
- **수정안**: 「상태와 무관하게」를 「**서버가 낸 기한 경과일이 있는 업무의 수** — 완료·취소·승인 대기는 서버가 `null` 을 낸다」로 좁힌다.

### [WARN-6] `(확정 — D-01·D-08)` 과다 귀속 — 앞 판 FAIL-4 와 같은 결(경미판)

- WP `:332`「**`tasks` 변경 없음** … 담당도 체크리스트 집계도 **기간 정규화도 기한 경과도** 조인·계산이지 열이 아니다 | **(확정 — D-01·D-08)**」.
- D-01(`decision-004:97-112`)이 정한 것은 **진행률 저장 컬럼뿐**이고, D-08(`:231-250`)이 정한 것은 **「분류」를 뺀다**뿐이다.
  **기간 정규화·기한 경과가 열이 아니라는 것은 어느 결정도 정하지 않았다** — SPEC 자신도 기한 경과일을 **`(도출)`** 로 적고 「**D-04 는 이 값을 정한 적이 없다**」라고 명시한다(`spec-005:583`).
- **수정안**: `(확정 — D-01)` + `(도출 — SPEC-005 §4 Data Contract)` 로 가른다.

---

## 기존 부채 / 참고 (이번 판정 제외)

- **직접 배정으로 만든 하위 업무는 상위의 프로젝트를 안 물려받는다.** `create_assigned_task` 가 `project_for()` 를 지나지 않기 때문이다(`work_tasks.py:2436-2455` vs `application.py:366-367`). 그래서 **그 하위는 어느 프로젝트 화면에도 안 선다** — BASE-004 어긋남 목록에 없는 자리다. 이번 판의 3층 트리 인수조건은 **요청 경로**로만 만들면 성립한다(WP E-1 이 그렇게 적었다 — 문제 없음). **기록만.**
- `create_assigned_task` 에 **`causation_key` 멱등 조기 반환**이 있다(`work_tasks.py:2431-2434`). 자동 초대를 `assign()` 에 걸 때 그 분기도 지난다 — 멱등이라 해는 없지만 테스트를 쓸 때 알고 써야 한다.
- WP `:295-298`「이 판이 닿는 것은 **넷**」 뒤에 표를 **여섯** 적는다(읽는 넷 + 흔적 둘). 표 91개는 내가 세어 맞다(`persistence.py` `__tablename__` 91). **서식 수준.**
- 줄번호 미세 드리프트: `persistence.py` 표 선언이 WP 표기보다 8~10줄 앞선다(`projects` :848 / `project_assignments` :870 / `tasks` :898 / `task_checklist_items` :1100 / `work_requests` :1628). WP 가 「줄 번호는 조사 시점의 것이고 구현 전에 다시 연다」(`:174`)고 이미 적었다 — **지적 아님.**

---

## §2 확인 항목 — 8개 전부의 결과

### 1. 인수조건 전수 배정 — **수는 PASS · 자리 하나 FAIL**

**내가 직접 셌다.** `spec-005-projects.md:898-1024` 의 `- [ ]` = **75개**(파일 전체도 75). 묶음 10개.

| 묶음 | 내가 센 수 | WP 주장 | 배정 |
|---|---|---|---|
| A 핵심 넷 | 6 | 6 ✓ | BE-2 3 / FE-2 3 ✓ |
| B 간트와 트리 | 8 | 8 ✓ | FE-2 6 / 갈라짐 2 ✓ |
| C 의존선 | 5 | 5 ✓ | FE-2 5 — **→ FAIL-4** |
| D 진행률 | 13 | 13 ✓ | BE-1 1 / FE-1 5 / FE-2 5 / FE-3 1 / 갈라짐 1 ✓ |
| E 상태 어휘 | 7 | 7 ✓ | BE-1 2 / FE-1 3 / 갈라짐 1 / 문서 1 ✓ |
| F 좌·우 레일 | 8 | 8 ✓ | FE-1 3 / FE-3 4 / 갈라짐 1 ✓ |
| G 관리 모달·빈 상태 | 7 | 7 ✓ | FE-1 1 / FE-3 6 ✓ |
| H 자동 초대 | 7 | 7 ✓ | BE-2 ✓ |
| I 자동 해제 | 9 | 9 ✓ | BE-2 ✓ |
| J 손자 종속 | 5 | 5 ✓ | BE-2 ✓ |
| **합** | **75** | **75** ✓ | Phase 부담 표(`:1049-1060`) 3+24+12+19+11+1+5 = **75** ✓ |

**「10묶음·누락 0」은 참이다.** 다만 C 의 한 줄이 잘못된 Phase 에 가 있고 어느 완료 판정도 안 든다 → **FAIL-4**.
문서가 닫는 1줄(`spec-005:959`)을 「Phase 가 없다」로 숨기지 않고 `:1062-1064` 에 명시한 것은 **좋다.**

### 2. Phase 경계가 실제로 서는가 — **PASS**

- **「BE-1 이 FE 전부의 선행」은 맞다.** 화면 다섯 칸(담당·체크리스트 집계·`span_from/to`·기한 경과일·상태 투영)이 전부 그 배열에서 나온다(I-1~I-5).
- **FE 가 BE-2 산출물에 코드로 의존하는 자리는 없다.** I-8(`:447`)이 자동 초대·해제의 FE 짝을 「**새 화면 조작이 없다** — 관리 모달의 참여 이력이 결과를 보여줄 뿐」으로 닫았고, 그 이력 API 는 기존(`api.ts:801`)이다. I-9 는 「이 화면에 이동 조작이 없다 — 화면이 내는 새 거절 0건」.
- 직렬 순서(BE-1 → BE-2 → FE-1 → FE-2 → FE-3)라 **순서가 뒤엉킨 자리 0건.** 같은 워크트리 공유를 이유로 든 것도 타당하다.
- 「BE-2 검수 통과 후 실제 응답 예시를 FE 브리프에 박는다」(`:478`)가 추정 배선을 막는다 — **잘 잡혔다.**

### 3. Domain / Schema 가 코드와 맞나 — **부분 PASS (FAIL-1·FAIL-2 가 여기서 났다)**

**맞는 것(코드로 확인).**
- `project_assignments` 에 떼는 재료가 이미 있다 — 부분 unique `uq_project_assignment_active` 실재(`persistence.py:870-880`).
- `tasks.parent_task_id` 자기참조 FK + `index=True`(`:939`) ✓. 마이그레이션 체계 없음 · `Base.metadata` 정본 ✓.
- `children_of()` 가 **직속만** 돈다(`work_tasks.py:475-482`) ✓. 이동 루프가 직속만 갱신한다(`application.py:532-536`) ✓ — 고칠 자리 지목이 정확하다.
- BFS 반복의 선례 `_require_no_predecessor_cycle()` 실재 ✓. 재귀 CTE 를 안 쓰는 판단도 저장소 사실과 맞다.
- 붙는 #1 은 `work_requests` 가 들고(`requests.create():306`, `create_request` 가 그 행을 만든다), 붙는 #3 은 `task_assignments` 가 든다(`reassign`/`hand_to` 가 `pending` 행을 만든다) — **「두 원장에 걸쳐 있다」는 사실 자체는 참이다.**

**틀린 것.**
- **붙는 #2 는 프로젝트가 없어 아예 안 돈다** → **FAIL-1**. 컬럼 둘 중 `task_assignments` 쪽은 **#3 만** 쓴다.
- **두 원장이 서로의 종결 경로를 갖는다** → **FAIL-2**. WP `:327` 이 든 이유(「다른 원장의 종결이 그 칸을 못 찾는다」)는 `task_assignments.source_work_request_id`(`work_tasks.py:1952`)가 반증한다.
- nullable 판단·인덱스 없음·CHECK 없음은 **타당**하다(`schema_sync` 가 NOT NULL+무기본값만 `manual[]` 로 올린다는 전제, `work_requests.project_id` 주석 `persistence.py:1651-1652` 이 그 결).

### 4. 거는 자리가 application 메서드인가 — **PASS**

일곱 자리 전부 application 메서드이고 **줄번호가 전부 실재한다**:
`requests.create():306` · `assignments.assign():89` · `reassign():171` · `requests.reject():466` · `withdraw():657` ·
`assignments.decline():276` · `cancel():295`.
세 입구가 같은 메서드로 모이는 것도 확인했다 — action-center 가 `self._assignments.cancel(principal, assignment.id)` 를 부른다(`platform/action_center.py:618-623`).
`entrypoints/http.py`·`mcp.py` 를 안 건드린다는 선언(`:197-200`)도 일관하고, `GET /api/projects/{project_id}` 핸들러 시그니처가 안 바뀐다는 근거도 실물과 일치(`http.py:1404`).
**세어서 뺀 여섯**(`:277-286`)도 코드와 맞다 — 특히 `plan_project_work()` 의 docstring 「사람은 아직 정하지 않는다」(`assignments.py:148-152`) 인용이 정확하다.

### 5. 떼는 자리 넷이 전부 계획에 있나 — **넷은 다 있다 · 다섯째가 있다(FAIL-2)**

요청 거절(`:269`) · 요청 철회(`:270`) · `decline`(`:271`) · **직접 배정/담당 교체 제안의 철회 `cancel()`**(`:272`, action-center 입구 `:249`) — **앞 판 FAIL-3 의 재발 없음.**
`cancel()` 이 `assignment_kind=="direct"` + `pending` 만 받는 것도 확인했고(`assignments.py:303-310`), `reassign`·`hand_to` 가 둘 다 `kind="direct"`·`pending` 행을 낳으므로(`work_tasks.py:2327-2328`·`2569-2570`) **#3 의 철회는 실제로 그 자리로 닫힌다** ✓.
빠진 것은 **요청 발송 산물의 배정-거절 경로** → FAIL-2.

### 6. 검증 계획이 실행 가능한가 — **PASS (WARN-1)**

`Makefile` 을 직접 열어 대조했다 — **쓰는 타겟이 전부 실재한다**:
`test-unit`(`:40`, `tests/unit tests/architecture` — `test_operation_inventory` 포함 ✓) · `test-contract`(`:43`) ·
`test-postgres`(`:52`, `-m integration`, `POSTGRES_TEST_URL != DATABASE_URL` 가드 있음 — WP 의 `ax_test_projects` 는 다르다 ✓) ·
`frontend-test`(`:59`) · `sync-demo-schema`(`:107`) · `verify`(`:65` = `test test-scale test-release frontend-test frontend-assets frontend-build`).
**`test-contract-serial` 은 없지만 「없는 타겟을 쓴」 것이 아니다** — BE-1 작업 8(`:516-519`)이 그것을 만들고 그 뒤부터 쓴다. 순서도 맞다(작업 8 → 9).
`make verify` 가 `test`(전체 pytest)를 통해 계약 테스트를 함께 돌므로 「exit 0 를 못 볼 수 있다」는 전제도 사실과 맞다.
플래그 한 줄만 부정확 → **WARN-1**.

### 7. 범위 제약이 지켜졌나 — **PASS**

- **Phase 0 가 2루프·사용자 동반으로 표시됐다** — `:123`(Role 표) · `:846`(Status) · `:86`·`:839-842`·`:898`「이 Phase 를 1루프로 끌어오지 마라 — 사용자 몫이다」. **선명하다.**
- **첨부(`material_*`) 작업이 1루프에 안 섞였다** — `:987-989`「그 계열을 겨눈 테스트를 더하지도 고치지도 않는다. 다만 스위트가 함께 도는 것은 막지 않는다」. 격리 수단 ①②③ 의 선택은 **Phase 0 몫으로 유보**(`:518-519`·`:883-889`).
  1루프가 더하는 것은 `Makefile` 한 줄뿐이고 「격리 수단이 아니라 재실행 편의」로 못 박았다 — **경계가 지켜졌다고 본다.**
- **`tasks_in()` 필터·페이징이 안 들어왔다** — BE-1 「하지 말 것」 `:527-528` 이 금지하고, D-16 이 거기 거는 전제까지 `Open Issues:1190-1193` 에 남겼다. `platform/projects.py:204-209` 는 실제로 필터도 페이징도 없다 ✓.
- 그 밖 Scope Out(진행률 컬럼 · 후행 API · 새 라우트/도구/오류 · `ds/` · `.design-sync/` · 사이드바 · `AppHeader` 슬롯)이 Phase 「하지 말 것」에 전부 되받아져 있다.

### 8. 앞 판 검수의 지적이 되살아났나 — **둘 살아났다(FAIL-3 · WARN-6), 나머지는 안 살아났다**

| 앞 판 | WP 에서 | 근거 |
|---|---|---|
| FAIL-1 상태 어휘를 다섯으로 올림 | **재발 없음** | WP 에 「계약 상태는 다섯」류 문장 0건. `blocked` 는 `:98`·`:686`·`:1075` 에서 **M-6 승계·통과값**으로만 다뤄지고, 계약 넷의 라벨도 「시작 전/진행 중/완료/취소」로 일관. 코드 주석(`application.py:2496-2505`)과도 같은 말 |
| FAIL-2 틀린 오류 갈래 | **재발 없음** | `:568-570`·`:615` 가 `WORK_PROJECT_LOCKED_BY_PREDECESSORS`(409)를 쓰고 **`WORK_PREDECESSORS_UNFINISHED` 를 끌어오지 말라고 명시**. 두 코드 모두 실재(`modules/work/errors.py:141`·`:150`) |
| FAIL-3 떼는 자리 `cancel()` 누락 | **재발 없음** | 넷 다 있다(§5) |
| FAIL-4 근거 없는 `(확정 — D-NN)` | **재발 1건 + 과다귀속 1건** | **FAIL-3**(D-19 「부분 이동은 없다」) · **WARN-6**(D-01·D-08) |
| WARN-2 입구 다중성 | **잘 반영됨** | `:254-262` 가 세 입구를 세고 「라우트가 아니라 application 메서드」를 제목으로 박았다 |
| WARN-3 `may_manage` 관측 | **반영됨** | `:446`(I-7) · FE-3 완료 판정 `:827-828` |
| WARN-5 표 이름 | **반영됨** | `task_schedules` 는 「읽지도 쓰지도 않는다」로만 등장(`:99`·`:152`) |

---

## 확인한 것 (PASS 근거 — 확인 안 한 것도 적는다)

- **운영 대장의 수를 내가 직접 읽었다**: `http_count` **159** · `tool_count` **129** · `get_project` 도구 스키마에 `ProjectTaskView`·`preceding_task_ids` **실재** · `list_projects`·`project_list` 에는 **없음** · `http_signature` = `(project_id: UUID, principal: Principal) -> ProjectDetailResult`. **WP 의 예측이 전부 맞다**(이름 하나만 WARN-2).
- **FE 줄번호 실측**: `ProjectPage.tsx` **333줄** ✓ · `ProjectPage.test.tsx` **179줄 · 검사 7개** ✓ · `App.tsx:352` `pageProps` ✓ `:515` `<ProjectPage>` ✓ · `onRegisterRails` 선례 실재(`App.tsx:477·488·505`, `CalendarPage.tsx:460-477`) ✓ · `api.ts` 여덟 호출 줄번호 **전부 일치**(146·158·793·797·801·805·814·818) ✓ · `ds/Select` 의 `trigger` prop 실재(`Select.tsx:380`) ✓ · `ds/ProgressBar` 가 내부에서 % 를 계산(`ProgressBar.tsx:18`) ✓ · `--scax-control-height-sm: 32px`(`scax.css:122`) — 「헤더 32px 고정」 ✓ · `components.css:692-693` 이 `.dashboard-columns, .report-grid, .project-layout` 를 한 규칙에 묶는다 ✓ · `index.css` `@import` 블록 `:16-40` ✓.
- **`_external_state`·`_overdue_days`·`_assignment_view`·`task_span` 지목이 정확하다** — `application.py:2495-2506`·`2521-2529`·`2532-2551`. 특히 `_assignment_view` 의 「`active` 먼저, 없으면 기다리는 행」을 WP `:376` 이 **같은 말로** 옮겼다.
- **확인 안 한 것**: 테스트·빌드·서버 기동(검수 규약상 금지) · 시안 CSS 13,510바이트의 토큰 대조(BASE-004 의 「누락 0」을 재검증하지 않았다 — WP 스스로 FE-1 작업 0 에서 확인 작업으로 남겼다) · Phase 0 내용과 첨부 계약(브리프 §3 범위 밖) · 문서 서식.

---

## 코디에게 — 무엇부터

1. **FAIL-1·FAIL-2 는 BE-2 발주 전에 닫아야 한다.** 둘 다 「붙는/떼는 자리의 지목」이라 발주서를 쓰는 순간 굳는다. 둘 다 **SPEC 과 뿌리를 공유**하므로 WP 만 고칠지 SPEC 환류로 올릴지는 코디 결정이고, 그 결정을 `Open Issues` 에 남겨야 한다.
2. **FAIL-3·FAIL-4 는 WP 안에서 한 줄씩**이면 닫힌다.
3. **WARN 여섯은 BE-1 발주 전에 같이 쓸어 담으면 된다** — 특히 WARN-3 은 FE-1 브리프에 들어가야 FE-2 가 안 막힌다.
