# [backend] WORK-005 Phase BE-1·BE-2 — 프로젝트 상세 확장 · 소속과 참여의 정합

너는 **strong-hajin `backend` 워커**다. **너는 이 작업의 맥락이 하나도 없다.** 먼저 읽어라:

- `/Users/kknaks/orca/workspaces/kknaks_profile/strong_hajin/orchestration/roles/strong-hajin/backend/role.md` (+ 같은 폴더 `.md` 전부)
- 코드 레포 `AGENTS.md` (워크트리 루트)
- `/Users/kknaks/orca/workspaces/kknaks_profile/strong_hajin/para/projects/summer-star/strong-hajin/30-work/work-005-projects.md` ← **실행 계획. Phase BE-1·BE-2 가 네 몫이다**
- `/Users/kknaks/orca/workspaces/kknaks_profile/strong_hajin/para/projects/summer-star/strong-hajin/20-spec/spec-005-projects.md` (1121줄) ← **계약의 SoT. 여기 없는 것을 발명하지 마라**
- `/Users/kknaks/orca/workspaces/kknaks_profile/strong_hajin/orchestration/work/strong-hajin-projects/research-be-domain.md` (726줄) ← 코드 지형(`파일:줄`). **네가 건드릴 자리가 거기 다 적혀 있다**
- `/Users/kknaks/orca/workspaces/kknaks_profile/strong_hajin/para/projects/summer-star/strong-hajin/10-decision/decision-004-projects.md` — 결정 D-01~D-27 (근거가 필요할 때)

작업 워크트리: **`/Users/kknaks/orca/workspaces/Strong_hajin/strong-hajin-projects`** (branch `kknaksss/strong-hajin-projects`, base `origin/main`)
문서는 **절대경로로 read-only** 로 읽는다. 문서 레포를 수정하지 마라.

## 1. 무엇을 만드나

### Phase BE-1 — 프로젝트 상세 `tasks[]` 확장 + 상태 투영

지금 `ProjectTaskView` 는 6필드뿐이라(`modules/work/project_results.py:28-37`) 화면을 못 그린다.
SPEC-005 §4 가 정한 대로 넓힌다. **그리고 `_external_state()` 를 지나게 한다** —
지금 `modules/work/projects.py:244` 가 원값을 그대로 내서 **`completion_submitted` 가 샌다.**
같은 업무가 `GET /api/tasks/{id}` 에서는 `done` 인데 프로젝트 상세에서는 다른 값이다.

**이것이 FE 전부의 선행이다.**

### Phase BE-2 — 소속과 참여의 정합

1. **손자까지 따라가는 프로젝트 이동** (D-19) — `modules/work/application.py:532-536` 이
   `children_of`(`platform/work_tasks.py:475-482`, 직속만)로 돌아서 **손자가 프로젝트 밖에 남는다.**
   자손 전체로 재귀시키고, **`_require_project_unlocked` 게이트도 자손 전체에** 건다
2. **자동 초대** (D-11·D-12) — 배정·발송 시 받는 사람이 그 프로젝트에 없으면 `참여`(member)로 붙인다.
   **열쇠는 `task.assign`** (`project.manage` 아님 — `may_assign_in`, `modules/work/projects.py:299-300`).
   **이미 붙어 있으면 아무 일도 안 일어난다**(`projects.py:163-165` 가 이미 멱등이다)
3. **자동 해제** (D-13~D-15) — 거절·철회 시 **조건 둘을 모두 만족할 때만** 뗀다.
   `end_reason` 으로 닫고 **행을 지우지 않는다.** 수락 뒤 취소·완료로는 떼지 않는다

## 2. ⚠ 반드시 지킬 것 — 검수가 이미 잡은 자리들

- **거는 자리는 `application` 메서드이지 entrypoint 가 아니다.**
  같은 명령이 **HTTP · MCP(`entrypoints/mcp.py`) · action-center** 세 입구로 들어온다.
  라우트에 걸면 **MCP 배정이 조용히 초대를 안 한다.** SPEC §5 가 이 규칙을 명시한다
- **떼는 자리는 넷이다** — 요청 거절 · 요청 철회 · `task-assignments/{id}/decline` ·
  **직접 배정/담당 교체 제안의 철회**(`modules/work/assignments.py:301` `cancel()`,
  표면은 `action_center.py:619-623` `cancel_assignment`). **네 번째를 빠뜨리지 마라**
- **새 오류 이름을 지어내지 마라.** 프로젝트 이동 게이트는 **기존** `WORK_PROJECT_LOCKED_BY_PREDECESSORS`(409,
  `modules/work/errors.py:140`)다. `WORK_PREDECESSORS_UNFINISHED` 는 **전이 게이트라 다른 자리**다
- **스키마 변경은 `reset_demo` 전용 경로.** 일반 API startup DDL 금지 (AGENTS.md)

## 3. 검증 — **첨부(material) 계열은 이번 판에서 제외다**

`material_*` 계약 테스트는 **병렬에서 흔들리는 기존 문제**가 있고(`/Users/kknaks/orca/workspaces/kknaks_profile/strong_hajin/reference/2026-09-21-strong-hajin-calendar/material-parallel-isolation.md`),
그 격리는 **내일 사용자가 Phase 0 로 따로 한다.** 그러니:

1. **착수 전에 기준선을 먼저 재라** — 네 변경 없이 한 번 돌려서 **지금 실패하는 것의 목록**을 적어 둔다
2. **네가 더한 계약 테스트는 직렬로 따로 돌려 전부 통과를 보여라** (`-n0`).
   ⚠ **`-p no:randomly` 를 쓰지 마라 — `pytest-randomly` 가 이 레포에 설치돼 있지 않아 무동작이다**
   (WP 검수 WARN-1 이 실측으로 잡았다). 직렬화는 `-n0` 하나로 한다
3. **기준선 실패는 「무관」으로 분리 보고**한다. 회차마다 들고 나는 파일 이름을 적어라 —
   **그 기록이 내일 Phase 0 의 입력이다**
4. `material_*` 계열을 **고치려 들지 마라.** 범위 밖이다
5. `tests/architecture` 경계와 operation inventory drift 는 확인한다 (diff 항목만 패치)

## 4. allowed_paths

- `backend/` · `docker-compose.yml` · `Makefile`
- **커밋·push·PR 금지.** 워크트리에 변경만 남긴다
- **문서 레포를 건드리지 마라.** 리포트는 `/Users/kknaks/orca/workspaces/kknaks_profile/strong_hajin/orchestration/work/strong-hajin-projects/be-impl-report.md` 하나에 쓴다
- **사용자 포트·프로세스를 건드리지 마라.** 서버를 띄워야 하면 테스트 하네스 안에서만

## 5. 범위 제약

- **Phase 0(`material_*` 격리)는 네 몫이 아니다** — 내일 사용자가 한다
- **프론트를 건드리지 마라** — FE 워커가 따로 붙는다
- **SPEC 에 없는 계약을 만들지 마라.** 필요하면 리포트에 「막힌 것」으로 적고 멈추지 말고 나머지를 해라
- `tasks_in()` 의 필터·페이징은 **범위 밖**이다 (DEC-004 가 그렇게 정했다)

## 6. 리포트 (`/Users/kknaks/orca/workspaces/kknaks_profile/strong_hajin/orchestration/work/strong-hajin-projects/be-impl-report.md`)

- 바꾼 파일 목록과 **각각이 닫는 인수조건 번호**
- **기준선 실패 목록**(착수 전) vs **지금 실패 목록** — 회차별로
- 네가 더한 테스트의 **직렬 실행 결과**(수치)
- 막힌 것 · 판단이 필요한 것

## 7. 완료 보고 — **문구 변경 금지**

> **⚠ 핸들은 dispatch preamble 의 값을 믿어라.** preamble 과 아래가 다르면 **preamble 이 맞다.**

```bash
orca orchestration send \
  --to term_bdba055b-758b-4dc9-85c3-7836d56b615a --from term_bf9b108a-a407-4ef2-895b-f3c3a479767d \
  --type worker_done \
  --task-id <이 태스크의 taskId — dispatch context 에 있다> \
  --dispatch-id <이 태스크의 dispatchId — dispatch context 에 있다> \
  --subject "backend 완료: WORK-005 BE-1·BE-2" \
  --body "바꾼 파일 / 닫은 인수조건 / 기준선 대비 테스트 수치 / 직렬 실행 결과 / 막힌 것"

orca terminal send --terminal term_bdba055b-758b-4dc9-85c3-7836d56b615a \
  --text "[worker_done] backend 완료 — BE-1·BE-2. 상세는 인박스." --enter
```
