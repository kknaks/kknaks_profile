# FE 재수정 — 검수 FAIL 1 · WARN 7

**읽을 것**: `orchestration/work/strong-hajin-projects/review-fe-report.md`
**allowed_paths**: `frontend/` 만. 커밋·push 금지. 개발 서버 금지.

검수는 **핵심 10개 항목 전부 PASS** 다 — 의존선·재귀·기하·진행률·BE 응답 읽기·공유 자산 전부.
아래는 **가장자리를 닫는** 일이다.

## FAIL-1 — 프로젝트 0개인 사람에게 3레일이 먼저 선다 (**반드시**)

`ProjectPage.tsx:219,226` — `projects` 가 `null` 인 첫 렌더에서 `noProjects` 가 거짓이라
**3레일이 먼저 서고 나서 빈 상태가 덮는다.** D-22 「네 칸이 각각 비지 않는다」 위반이고,
그 탓에 이번 판이 새로 쓴 「프로젝트 0개」 검사가 **격리 11회 중 2회 실패**한다.

**고칠 것**: 레일 등록 effect 에 **`projects === null` 조건**을 더해 **아직 모르는 동안은 레일을
등록하지 않는다.** 고친 뒤 **그 테스트를 격리로 10회 이상 돌려 전부 통과**하는 것을 보여라.

## WARN 일곱

1. **WARN-1** 빈 상태 섹션의 `aria-label` 이 「프로젝트 관리」다 → 그 자리에 맞는 이름으로
2. **WARN-2** — **고치지 마라. 코디가 정했다**: 접힌 가지 **안쪽** 선을 **셈으로 내는 것이 맞다**
   (자기 자신을 가리키는 화살표는 뜻이 없다). **계약 문구 쪽을 고친다** — 그건 문서 몫이라
   너는 건드리지 않는다. 지금 구현을 유지하라
3. **WARN-3** — **고치지 마라. 코디가 정했다**: 모수 0 일 때 **「—」가 맞다**(0% 아님).
   D-02 의 결(「셀 것이 없으면 말하지 않는다」)과 같다. 문서에 기록하는 것은 코디가 한다
4. **WARN-4** 담당 없음을 **좌 레일은 빈칸 · 우 레일은 「—」** 로 낸다 → **한쪽으로 통일**하라.
   BE 계약이 「`assignee: null` 이 정상이고 서버가 「미정」을 지어내지 않는다」이므로
   **화면도 지어내지 말되 두 자리가 같은 방식**이어야 한다
5. **WARN-5** 하위가 **전부 기간 없는** 업무면 twisty 가 서지만 **눌러도 아무 것도 안 움직인다**
   → 펼칠 것이 실제로 있을 때만 twisty 를 세워라
6. **WARN-6** 「상위이면서 하위」인 바의 높이가 **18px** 이다(14px 이 아니라) →
   시안 규칙은 **상위면 14px** 다(`--parent` 가 `--child` 를 이긴다). 맞춰라
7. **WARN-7** 강조된 의존선의 **화살촉 색이 안 바뀐다** → `marker` 가 `currentColor` 를 따르게 하거나
   강조용 marker 를 따로 둬라. 선만 accent 고 촉이 회색이면 눈에 어긋난다

## 검증

- `make frontend-test` · `npx tsc --noEmit` 을 **다시 돌려라**
- **FAIL-1 테스트는 격리 10회 이상** 돌려 흔들리지 않는 것을 보여라
- `ActionCenter.test.tsx` 실패는 **이 판 밖**이다(diff 0줄 · 단독 통과) — 분리해 보고
- WARN 각각이 **어떻게 닫혔는지**(또는 코디 지시로 유지했는지) 한 줄씩

---

## 역할·맥락 (터미널이 새로 떴다면 여기부터)

너는 **strong-hajin `frontend` 워커**다. 먼저 읽어라:
- `/Users/kknaks/orca/workspaces/kknaks_profile/strong_hajin/orchestration/roles/strong-hajin/frontend/role.md` (+ `rules.md`)
- 코드 레포 `AGENTS.md`
- `review-fe-report.md`(검수 전문) · `fe-impl-report.md`(앞 판) · `be-impl-report.md` §6(BE 실물 응답)
- `/Users/kknaks/orca/workspaces/kknaks_profile/strong_hajin/para/projects/summer-star/strong-hajin/20-spec/spec-005-projects.md`

워크트리 `/Users/kknaks/orca/workspaces/Strong_hajin/strong-hajin-projects` — **`frontend/` 만** 건드린다.
커밋·push·개발서버 금지.

## 완료 보고 — **문구 변경 금지**

```bash
orca orchestration send \
  --to term_bdba055b-758b-4dc9-85c3-7836d56b615a --from term_bd577955-7d7b-4e2d-ade1-deceda7d25c7 \
  --type worker_done --task-id task_d04b49559c96 --dispatch-id ctx_none \
  --subject "frontend 완료: FE 재수정" \
  --body "FAIL-1 닫힘 근거(격리 N회) / WARN 일곱 각각 처리 / 테스트·tsc 수치 / git status"

orca terminal send --terminal term_bdba055b-758b-4dc9-85c3-7836d56b615a \
  --text "[worker_done] frontend 완료 — FE 재수정. 상세는 인박스." --enter
```
