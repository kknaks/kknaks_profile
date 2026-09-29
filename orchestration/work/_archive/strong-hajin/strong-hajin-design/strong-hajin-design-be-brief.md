# [backend] WORK-007 Phase B-1 · B-2 · B-3 — 업무 상세 재설계 서버

너는 **strong-hajin `backend` 워커**다. 먼저 역할 문서를 읽어라 (이 워크트리엔 없다 — 절대경로):

- `/Users/kknaks/orca/workspaces/kknaks_profile/스트롱하진-디자인/orchestration/roles/strong-hajin/backend/role.md` (+ 같은 폴더 `rules.md` · `skills.md` · `tools.md` · `workflow.md`)

작업 워크트리: `/Users/kknaks/orca/workspaces/Strong_hajin/strong-hajin-design`
base 브랜치: `origin/main` → 최종 PR 대상 `main` (PR 은 코디네이터가 올린다)

⚠ **frontend 워커는 아직 안 탄다.** 이 판은 너 혼자다. `frontend/` 를 건드리지 마라 — 다음 판이 거기 탄다.

## 1. SSOT — 먼저 읽을 것. **여기 없는 건 발명하지 마라**

- `/Users/kknaks/orca/workspaces/kknaks_profile/스트롱하진-디자인/para/projects/summer-star/strong-hajin/20-spec/spec-007-task-detail.md` ← **계약의 SoT (v0.2.0)**
- `/Users/kknaks/orca/workspaces/kknaks_profile/스트롱하진-디자인/para/projects/summer-star/strong-hajin/30-work/work-007-task-detail.md` ← **네 단계가 여기 있다 (Phase B-1 · B-2 · B-3)**
- `/Users/kknaks/orca/workspaces/kknaks_profile/스트롱하진-디자인/para/projects/summer-star/strong-hajin/10-decision/decision-006-task-detail.md` — 왜 이렇게 정했나
- `/Users/kknaks/orca/workspaces/kknaks_profile/스트롱하진-디자인/orchestration/work/strong-hajin-design/be-survey-report.md` — 네가 지난 판에 쓴 조사. 지금 코드가 어떤지는 거기 있다

기존 계약: `20-spec/spec-001-work-management.md` · `spec-003-task-lifecycle-v2.md` · `spec-005-projects.md`
**SPEC-007 §7.2 가 이 셋의 여섯 줄을 대체한다.** 충돌하면 SPEC-007 이 이긴다. §7.2 를 먼저 읽어라.

## 2. 무엇을 만드나 — WORK-007 의 BE 셋

```
Phase B-1  후행 역방향 조회와 응답 필드        work-007:236
Phase B-2  상위 변경 칸과 두 게이트             work-007:273
Phase B-3  후행 해제 명령                       work-007:312
```

**WORK-007 이 단계마다 Acceptance 와 Covers(spec 절번호)를 달아 놨다. 그것이 완료 조건이다.**

핵심만 다시 적으면 이렇다 — **상세는 문서를 봐라.**

- **후행은 저장하지 않는다.** `task_predecessors` 를 반대로 읽는다. 새 표·새 쓰기 경로 없음
- 필요한 것 셋: 역방향 조회 · `predecessor_task_id` 인덱스 · 상세 응답 필드(`successors` + `hidden_successor_count`)
- **못 읽는 후행은 건수만.** 제목·담당자·기한을 내지 않는다
- **못 읽는 선행도 같은 규칙** — 건수만, 그리고 **미완으로 센다**
- **읽기 전용 갈래에도 후행이 실린다** — 읽기 전용은 보는 범위가 아니라 고치는 범위다
- 상위 변경: `PATCH /api/tasks/{id}` 에 `parent_task_id` + `clear_parent`. 검증은 **기존 `parent_for()` 를 재사용**
- **상위 이동으로 직속 하위가 V-8 을 어기게 되면 거절** — 새 오류 코드 `WORK_CHILDREN_DIRECT_NESTING`(409)
- **상위를 옮기면 자손 전체의 프로젝트가 따라간다**
- 후행 해제는 **전용 명령**(PATCH 배열 교체 아님). A 담당자가 자기 후행을 해제할 수 있다
- **알림은 범위 밖.** 「여기에 알림이 붙어야 한다」는 자리만 코드 주석으로 남기고 **구현하지 마라**

## 3. Phase B-1 의 첫 작업 — 인덱스를 어떻게 넣나

SPEC-007 은 「`predecessor_task_id` 인덱스가 필요하다」까지만 쓴다. **설치 방법은 네가 답한다.**

조사에서 네가 짚은 두 가지를 그대로 다뤄라 — Alembic 이 없고, `schema_sync` 가 기존 표에
인덱스를 더하지 못한 선례가 있다. **되는 길을 찾아 구현하고, 리포트에 그 방법과 근거를 적어라.**
`reset_demo` 전용 경로와 일반 API startup DDL 금지 규칙을 어기지 마라.

## 4. 전수조사 — 목록으로 끝내지 마라

브리프가 준 것은 **시작점**이다. 손대는 표면을 **전부 grep 으로 세고 시작해라.**

```
predecessor_task_id   preceding_task_ids   successors   hidden_successor_count
parent_task_id        clear_parent         project_id
TaskEditFields        TaskUpdateInput      TaskUpdateCommand
parent_for            _require_may_hold_children   _is_central_task   _predecessor_gate
```

특히 이 셋은 **비대칭이 생기기 쉬운 자리**다 — 조사에서 네가 이미 짚었다.

- `entrypoints/http.py` ↔ `entrypoints/mcp.py` (MCP `task_update` 가 선행·승인자를 못 받는 비대칭)
- `TaskVersion` snapshot (선행·상위·프로젝트가 없어 이력 복원 불가)
- 오류 코드명이 docstring 에만 있고 HTTP 본문은 `detail=str(error)` 문장 하나

**이 셋을 이번 판에서 고칠지 말지는 WORK-007 이 정한다.** 문서에 없으면 고치지 말고 리포트에 적어라.

## 5. allowed_paths — 이 밖은 건드리지 마라

- `backend/`
- `Makefile` · `docker-compose.yml` (필요할 때만)
- 리포트: `/Users/kknaks/orca/workspaces/kknaks_profile/스트롱하진-디자인/orchestration/work/strong-hajin-design/be-report.md`

`frontend/` 금지. 문서 경로 금지(리포트 한 장 제외).

## 6. 범위 제약 — 하지 말 것

- **알림을 구현하지 마라.** 자리만 주석으로
- 소급 재배치를 만들지 마라 — 위반이 되는 이동을 **거절**할 뿐이다
- 후행을 저장하지 마라. 양방향 저장·새 표 금지
- 프론트를 고치지 마라
- WORK-007 에 없는 단계를 하지 마라. 눈에 띄는 다른 문제는 **리포트에 적고 넘어간다**
- 커밋·push·PR 금지

## 7. 검증

```
코드 레포 AGENTS.md 준수: backend 테스트는 Makefile 타겟으로만 실행. 변경 단계에 맞게 make test-unit 또는 make test-contract, 최종 코디 검증은 make verify 및 격리 PostgreSQL의 make test-postgres와 관련 acceptance journey. 단계별 전량 반복 금지. tests/architecture 경계 및 operation inventory drift 확인(diff 항목만 패치). 스키마 변경은 reset_demo 전용 경로, 일반 API startup DDL 금지. 기존 실패는 기준선과 분리 보고.
```

- **사용자 포트·프로세스를 건드리지 마라.** `127.0.0.1:8001`·`5176`·`54329` 가 떠 있고 사용자가 그 화면을 보고 있다. 죽이거나 재시작하지 마라. 스택 재시작은 코디가 한다
- 통과할 때까지 고친다. 못 고치면 이유와 함께 보고한다
- 기존에 이미 깨져 있던 무관한 실패는 「무관」으로 분리해 보고한다

## 8. 리포트

`.../orchestration/work/strong-hajin-design/be-report.md`

```
## 0. 한 줄 요약
## 1. 표면 전수조사 결과 (§4 심볼별 건수와 처분)
## 2. Phase 별 구현 — B-1 · B-2 · B-3. 각각 변경 파일:줄 · Acceptance 충족 근거
## 3. 인덱스 설치 방법과 근거 (§3)
## 4. 검증 결과 — 명령과 «수치»
## 5. 손대지 않고 남긴 것 (§4 의 비대칭 셋 포함)
## 6. 기준선 실패 (무관한 기존 실패)
## 7. 미결·주의점
```

## 9. 완료 보고 — **문구 변경 금지**

- **커밋·push·PR 하지 마라.** 워크트리에 변경만 남긴다.

```bash
orca orchestration send \
  --to term_e622370a-1f3b-4861-b759-daa3584eace0 --from <네 워커handle> \
  --type worker_done \
  --task-id <dispatch context 의 taskId> \
  --dispatch-id <dispatch context 의 dispatchId> \
  --subject "backend B-1·B-2·B-3 완료: <한 줄>" \
  --body "변경 파일 목록 / Phase별 요약 / 검증 결과(수치) / 계약 준수 / 미결·주의점"

orca terminal send --terminal term_e622370a-1f3b-4861-b759-daa3584eace0 \
  --text "[worker_done] backend B-1·B-2·B-3 완료 — <한 줄>" --enter
```

막히면: `orca terminal send --terminal term_e622370a-1f3b-4861-b759-daa3584eace0 --text "[질문] backend: <질문>" --enter`
