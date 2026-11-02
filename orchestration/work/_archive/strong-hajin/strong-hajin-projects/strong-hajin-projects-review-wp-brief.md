# [reviewer] WORK-005 검수 — 계획이 계약을 전부 닫고, 코드 지형과 맞는가

너는 **strong-hajin `reviewer` 워커**다. **너는 이 작업의 맥락이 하나도 없다.** 먼저 읽어라:

- `/Users/kknaks/orca/workspaces/kknaks_profile/strong_hajin/orchestration/roles/strong-hajin/reviewer/role.md` (+ 같은 폴더 `.md` 전부)
- `/Users/kknaks/orca/workspaces/kknaks_profile/strong_hajin/para/projects/summer-star/strong-hajin/30-work/work-005-projects.md` (1222줄) ← **검수 대상**
- `/Users/kknaks/orca/workspaces/kknaks_profile/strong_hajin/para/projects/summer-star/strong-hajin/20-spec/spec-005-projects.md` (1121줄) ← **계약의 SoT.** 인수조건 75줄이 §6 에 있다
- `/Users/kknaks/orca/workspaces/kknaks_profile/strong_hajin/para/projects/summer-star/strong-hajin/10-decision/decision-004-projects.md` (결정 D-01~D-27) · `/Users/kknaks/orca/workspaces/kknaks_profile/strong_hajin/para/projects/summer-star/strong-hajin/00-baseline/baseline-004-projects.md`
- `/Users/kknaks/orca/workspaces/kknaks_profile/strong_hajin/orchestration/work/strong-hajin-projects/research-be-domain.md` · `/Users/kknaks/orca/workspaces/kknaks_profile/strong_hajin/orchestration/work/strong-hajin-projects/research-fe-structure.md` ← 코드 지형
- `/Users/kknaks/orca/workspaces/kknaks_profile/strong_hajin/orchestration/work/strong-hajin-projects/review-spec-005-report.md` ← **앞 판 검수.** 같은 실수가 WP 에 되살아났는지 본다

작업 워크트리: `/Users/kknaks/orca/workspaces/kknaks_profile/strong_hajin` (코디 워크트리). 코드는 read-only:
`/Users/kknaks/orca/workspaces/Strong_hajin/strong-hajin-projects`
⚠ 코디네이터가 같은 워크트리에 있다. **리포트 하나 밖은 건드리지 마라.**

## 1. 판정 규칙

**FAIL**(계획이 계약과 다르다·코드 사실과 다르다·내부 모순) / **WARN**(구현자가 둘로 읽는다) / **PASS**.
**각 지적에 `파일:줄` + 근거.** 근거 없는 지적은 쓰지 마라.

## 2. 반드시 확인할 것

1. **인수조건 전수 배정** — SPEC §6 의 **75줄이 하나도 빠짐없이** 어느 Phase 에 배정됐나.
   「10묶음·누락 0」이라는 주장을 **네가 직접 세어** 대조하라
2. **Phase 경계가 실제로 서는가** — BE-1 이 FE 전부의 선행이라는 전제가 맞나.
   FE Phase 가 BE-2 산출물에 의존하는데 순서가 뒤엉킨 자리는 없나
3. **Domain/Schema 가 코드와 맞나** — 컬럼 둘(`work_requests.auto_project_join` ·
   `task_assignments.auto_project_join`)이 실제로 **두 원장에 필요한지** 코드로 확인하라.
   `assign`(`platform/work_tasks.py:2461`)·`reassign`(`:2569`)·요청 발송 경로를 직접 보고 판단
4. **거는 자리가 application 메서드인가** — 계획이 entrypoint(라우트·MCP 도구)에 걸고 있지 않나.
   SPEC §5 가 이 규칙을 명시한다. **HTTP·MCP·action-center 셋이 같은 메서드로 모인다**
5. **떼는 자리 넷이 전부 계획에 있나** — 요청 거절 · 요청 철회 · `decline` ·
   **직접 배정/담당 교체 제안의 철회**(`assignments.py:301` · `action_center.py:619-623`)
6. **검증 계획이 실행 가능한가** — `make test-contract-serial` 같은 **타겟이 실재하는지**
   `Makefile` 에서 확인하라. 없는 타겟을 쓰면 FAIL
7. **범위 제약이 지켜졌나** — 첨부(material) 작업이 1루프 Phase 에 섞이지 않았나.
   Phase 0 가 **2루프·사용자 동반**으로 표시됐나. `tasks_in()` 필터·페이징이 몰래 들어오지 않았나
8. **앞 판 검수의 지적이 되살아났나** — 특히 상태 어휘(외부 넷 + `blocked` 통과값) ·
   오류 이름(`WORK_PROJECT_LOCKED_BY_PREDECESSORS`) · 근거 없는 `(확정 — D-NN)`

## 3. 범위 밖 — 지적하지 마라

- **Phase 0 의 내용**(내일 사용자 몫) · 첨부 관련 계약 · 문서 서식 취향
- SPEC 자체의 계약(이미 검수 통과) — 단 **WP 가 SPEC 을 잘못 옮겼으면 FAIL 이다**

## 4. allowed_paths

- **read-only.** 문서·코드 수정 금지. 커밋·push·테스트 실행·서버 기동 금지
- **쓰는 파일은 하나**: `/Users/kknaks/orca/workspaces/kknaks_profile/strong_hajin/orchestration/work/strong-hajin-projects/review-wp-005-report.md`

## 5. 리포트 형식

판정 한 줄(FAIL n · WARN n) → 지적마다
`[FAIL-n] 제목 / 무엇이 / 근거 파일:줄 / 무엇과 어긋나나 / 한 줄 수정안`
→ 마지막에 **§2 의 8개 항목 각각의 결과**.

## 6. 완료 보고 — **문구 변경 금지**

```bash
orca orchestration send \
  --to term_bdba055b-758b-4dc9-85c3-7836d56b615a --from term_8472422b-d250-45d5-b42a-03e21d2696ff \
  --type worker_done \
  --task-id <이 태스크의 taskId — dispatch context 에 있다> \
  --dispatch-id <이 태스크의 dispatchId — dispatch context 에 있다> \
  --subject "reviewer 완료: WORK-005 검수" \
  --body "판정(FAIL n·WARN n) / 큰 지적 3개 / §2 항목 8개 결과 / git status"

orca terminal send --terminal term_bdba055b-758b-4dc9-85c3-7836d56b615a \
  --text "[worker_done] reviewer 완료 — WORK-005 검수. 상세는 인박스." --enter
```
