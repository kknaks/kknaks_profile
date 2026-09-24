# SPEC-005 · WORK-005 동시 수정 — WP 검수 FAIL 4 · WARN 6

**고칠 파일 둘** (그 밖은 건드리지 마라):
- `para/projects/summer-star/strong-hajin/20-spec/spec-005-projects.md`
- `para/projects/summer-star/strong-hajin/30-work/work-005-projects.md`

**읽을 것**: `orchestration/work/strong-hajin-projects/review-wp-005-report.md` (검수 전문)

FAIL-1·FAIL-2 는 **계약까지 올라간다.** 코디가 코드로 확인하고 방향을 정했다 — **아래대로 고쳐라.**

---

## 결정 1 — 붙는 자리는 **둘**이다. 직접 배정은 빠진다 (FAIL-1)

`POST /api/tasks/assign`(직접 배정)은 **자동 초대가 성립하지 않는다.**

- `TaskAssignmentInput` 이 **non-null `project_id` 를 명시적으로 거부한다**
  (`modules/work/task_creation.py:118-126` — 「A non-null project is not owned by assignment
  creation and must not be silently ignored by the executor」)
- `create_assigned_task`(`platform/work_tasks.py:2413-2455`)도 `project_id` 를 싣지 않는다
- 즉 **그 경로로 태어난 업무는 프로젝트가 없다.** 붙을 프로젝트가 없으므로 초대할 일도 없다

**고칠 것**
- SPEC §4 의 붙는 자리 표에서 **#2(직접 배정)를 「세어서 뺀 자리」로 옮기고** 위 근거를 단다.
  붙는 자리는 **둘** — ① 요청 발송 ② 담당 교체 제안(`reassign`)
- WORK-005 BE-2 의 완료 판정에서 **「붙는 셋 각각에 테스트」를 「붙는 둘」로** 고친다
- 인수조건에서 직접 배정 초대를 겨누는 줄이 있으면 **같이 고친다**

## 결정 2 — 흔적은 **`task_assignments` 한 칸**이다 (FAIL-2 · D-14 재정정)

붙는 자리 **둘 다 `TaskAssignmentRecord` 를 만든다**:
- 요청 발송도 행을 세운다 — `assignment_kind="request_effect"` · `status="pending"` ·
  **`source_work_request_id=request.id`** (`platform/work_tasks.py:1938-1957`)
- 담당 교체 제안도 배정 행이다

**따라서 `work_requests.auto_project_join` 은 두지 않는다.** 흔적은
**`task_assignments.auto_project_join` 한 칸**이고, **요청 유래인지는 `source_work_request_id` 로 안다.**

이것이 FAIL-2 를 함께 닫는다 — 검수가 지적한 「요청 발송이 만든 pending 행을 수신자가
`decline` 으로 답하면 흔적이 `work_requests` 에 있어 자동 해제가 안 돈다」는,
**흔적이 그 배정 행에 있으면 그대로 돈다.** 떼는 자리 넷이 전부 그 행에 닿는다.

**고칠 것**
- WORK-005 `Domain / Schema` — 컬럼을 **하나로** 줄이고 위 근거를 적는다
- **D-14 의 「두 표에 한 칸씩」이 다시 정정됐음을 기록하라** — 지우지 말고
  「요청 발송도 배정 행을 만든다는 사실이 드러나 한 표로 좁혔다」로 남긴다
- SPEC 쪽은 저장 자리를 말하지 않으므로 **행동 서술만 확인**한다 —
  「흔적을 남긴다」가 특정 표를 가리키지 않는지 보고, 가리키면 지운다

## 결정 3 — FAIL-3 · FAIL-4 는 검수 지적대로

- **FAIL-3**: WP `:370` 의 `(확정 — D-19 "부분 이동은 없다")` 를 **`(도출)`** 로 강등한다.
  D-19 에 그 말이 없다. SPEC-005:706 이 같은 사실을 이미 `(도출)` 로 적는다 — **그쪽과 맞춘다**
- **FAIL-4**: 인수조건 「후행 목록이 우 레일에 나온다」(`spec:931`)는 **FE-3 몫**이다(우 레일은 FE-3).
  FE-2 에서 빼고 FE-3 으로 옮긴 뒤 **FE-3 완료 판정에 그 줄을 넣어라**

## WARN 여섯 — 전부 닫는다

1. **`-p no:randomly` 는 무동작이다** — `pytest-randomly` 가 설치돼 있지 않다.
   검증 계획에서 그 플래그를 **빼고 `-n0`(직렬)만** 남긴다. 「왜 뺐는지」 한 줄
2. 대장 drift 테스트 이름 오기 → 실제 이름 `test_inventory_schemas_match_the_actual_registered_tools`(`:104`)로
3. **FE 타입에 `preceding_task_ids` 가 없다**(`viewModels.ts:95-102`, `features/project` grep 0건) —
   I-6 의 「기존」이 **FE 쪽은 거짓**이다. 「FE 타입은 새로 더한다」로 고쳐라
4. FE-2 헤더의 「갈라지는 3줄」 → **5줄**
5. **「지연」의 「상태와 무관」이 코드와 갈린다** — `_overdue_days`(`application.py:2526`)는
   **끝난 일에 `null`** 이다. 그러니 지연 칸은 「**끝나지 않은 업무 중** 기한이 지난 것」이다.
   SPEC·WP 양쪽을 그 사실에 맞춰 고치고, SPEC-001 §U-3 의 문장을 그대로 베끼지 마라
6. `(확정 — D-01·D-08)` 과다 귀속 → **`(도출)`** 로 강등

## 하지 말 것

- **새 계약·새 결정을 만들지 마라.** 필요하면 SPEC §7 / WP Open Issues 로 올린다
- 색인·`log.md` 금지. **커밋·push 금지.** 지정한 두 파일 밖 변경 0건
- 첨부(material)·Phase 0 내용은 범위 밖

## 검증

- FAIL 4 · WARN 6 **각각이 어떻게 닫혔는지** 보고에 한 줄씩
- 붙는 자리 **둘**, 떼는 자리 **넷**, 흔적 컬럼 **하나** — 세 수가 SPEC·WP 양쪽에서 같다
- 인수조건 배정에 **빠진 줄 0 · 잘못 배정된 줄 0**
- `git status --porcelain` 이 **두 파일만** 바뀐 것을 보인다
