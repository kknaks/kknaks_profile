# [reviewer] BE-1·BE-2 검수 — 코드가 계약과 같은 것을 하는가

너는 **strong-hajin `reviewer` 워커**다. **너는 이 작업의 맥락이 하나도 없다.** 먼저 읽어라:

- `/Users/kknaks/orca/workspaces/kknaks_profile/strong_hajin/orchestration/roles/strong-hajin/reviewer/role.md` (+ 같은 폴더 `.md` 전부)
- 코드 레포 `AGENTS.md`
- `/Users/kknaks/orca/workspaces/kknaks_profile/strong_hajin/para/projects/summer-star/strong-hajin/20-spec/spec-005-projects.md` ← **계약의 SoT** (인수조건 §6)
- `/Users/kknaks/orca/workspaces/kknaks_profile/strong_hajin/para/projects/summer-star/strong-hajin/30-work/work-005-projects.md` ← Phase BE-1·BE-2 의 작업과 완료 판정
- `/Users/kknaks/orca/workspaces/kknaks_profile/strong_hajin/orchestration/work/strong-hajin-projects/be-impl-report.md` ← **BE 워커의 리포트. 주장을 그대로 믿지 말고 실측하라**
- `/Users/kknaks/orca/workspaces/kknaks_profile/strong_hajin/orchestration/work/strong-hajin-projects/review-wp-005-report.md` ← 앞 판 검수. **같은 지적이 코드에서 재발했는지** 본다
- `/Users/kknaks/orca/workspaces/kknaks_profile/strong_hajin/orchestration/work/strong-hajin-projects/research-be-domain.md` ← 착수 전 코드 지형

검수 대상 워크트리: **`/Users/kknaks/orca/workspaces/Strong_hajin/strong-hajin-projects`** (branch `kknaksss/strong-hajin-projects`)
**`git diff origin/main...` 로 이번 판의 변경 전부를 본다.**

## 1. 판정 규칙

**FAIL**(계약과 다른 것이 돈다) / **WARN**(물어야 할 만큼 모호하다) / **PASS**.
**각 지적에 `파일:줄` + 근거.** 근거 없는 지적은 쓰지 마라.

**「조용히 통과하는 자리」를 따로 본다** — 테스트는 초록인데 계약이 깨진 곳:
개명뿐인 변경 · 빈 단언 · 조건이 항상 참인 가드 · 예외를 삼키는 폴백 ·
**테스트가 실제 경로 대신 목을 검사하는 것**.

## 2. 반드시 확인할 것

1. **붙는 자리는 둘인가** — 요청 발송 · 담당 교체 제안(`reassign`).
   **직접 배정(`POST /api/tasks/assign`)에 초대가 붙어 있으면 FAIL** — 그 경로는
   `project_id` 를 거부하므로(`modules/work/task_creation.py:118-126`) 원리적으로 성립하지 않는다
2. **거는 자리가 `application` 메서드인가** — 라우트·MCP 도구에 걸었으면 FAIL.
   **HTTP · MCP · action-center 셋이 같은 메서드로 모인다.** entrypoint 에 걸면 MCP 배정이 조용히 빠진다
3. **떼는 자리 넷이 전부 구현됐나** — 요청 거절 · 요청 철회 · `decline` ·
   **직접 배정/담당 교체 제안의 철회**(`modules/work/assignments.py:301` · `action_center.py:619-623`)
4. **자동 해제의 조건 둘이 모두 걸렸나** — ① 흔적(`task_assignments.auto_project_join`)이 있을 때만
   ② **그 프로젝트에 그 사람의 다른 활성 업무가 없을 때만.** 하나라도 빠지면 FAIL
   (②가 빠지면 **원래 멤버를 떼는 사고**가 난다)
5. **손자까지 따라가는가** — 자손 전체 재귀인지, `_require_project_unlocked` 게이트도
   **자손 전체에** 걸리는지. 직속만 돌면 FAIL
6. **`_external_state()` 를 지나는가** — 프로젝트 상세 `tasks[].state` 에
   `completion_submitted` 가 새면 FAIL
7. **새 오류 이름을 지어내지 않았나** — 프로젝트 이동 게이트는 기존
   `WORK_PROJECT_LOCKED_BY_PREDECESSORS`(409, `modules/work/errors.py:140`)
8. **멱등인가** — 이미 붙어 있는 사람에게 다시 붙이면 **아무 일도 안 일어나야** 한다
9. **테스트가 실제로 증명하나** — 새로 더한 계약 테스트가 **위 1~8 각각을 겨누는지.**
   통과하지만 아무것도 증명 안 하는 테스트가 있으면 WARN
10. **범위를 넘지 않았나** — `frontend/` 변경 0건 · 첨부(material) 손댄 것 0건 ·
    `tasks_in()` 필터·페이징 추가 0건 · 커밋·push 0건

## 3. 테스트 실행 — **네가 직접 재라**

- BE 리포트의 수치를 **믿지 말고 다시 돌려라.** 단, **첨부(`material_*`) 계열은 범위 밖**이다
- **`-p no:randomly` 를 쓰지 마라** — 이 저장소에 `pytest-randomly` 가 없어 무동작이다. 직렬은 `-n0`
- **기존 실패와 이번 판의 실패를 분리**해서 보고하라. 회차마다 실패 파일 집합이 바뀌면 그 사실을 적어라
- **서버를 띄우지 마라.** 사용자 포트·프로세스 금지

## 4. allowed_paths

- **read-only.** 코드·문서 수정 금지. 커밋·push 금지
- **쓰는 파일은 하나**: `/Users/kknaks/orca/workspaces/kknaks_profile/strong_hajin/orchestration/work/strong-hajin-projects/review-be-report.md`

## 5. 리포트

판정 한 줄(FAIL n · WARN n) → 지적마다
`[FAIL-n] 제목 / 무엇이 / 근거 파일:줄 / 어느 계약·인수조건과 어긋나나 / 한 줄 수정안`
→ **§2 의 10개 항목 각각의 결과** → **테스트 실측 수치**(기존 실패 분리).

## 6. 완료 보고 — **문구 변경 금지**

```bash
orca orchestration send \
  --to term_bdba055b-758b-4dc9-85c3-7836d56b615a --from term_5b46e9b2-9a00-492b-ba1b-1ff82a09a946 \
  --type worker_done \
  --task-id <이 태스크의 taskId — dispatch context 에 있다> \
  --dispatch-id <이 태스크의 dispatchId — dispatch context 에 있다> \
  --subject "reviewer 완료: BE-1·BE-2 검수" \
  --body "판정(FAIL n·WARN n) / 큰 지적 3개 / §2 10개 항목 결과 / 테스트 실측(기존 실패 분리) / git status"

orca terminal send --terminal term_bdba055b-758b-4dc9-85c3-7836d56b615a \
  --text "[worker_done] reviewer 완료 — BE 검수. 상세는 인박스." --enter
```
