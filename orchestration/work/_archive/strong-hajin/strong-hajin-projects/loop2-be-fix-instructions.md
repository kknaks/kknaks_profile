# BE-3 소수정 — 검수 WARN 셋 (판정은 PASS, 이건 「내일 관측을 잃는 자리」)

**읽을 것**: `orchestration/work/strong-hajin-projects/review-loop2-be-report.md`
**allowed_paths**: `backend/tests/` 만. **제품 코드 0줄.** 커밋·push 금지. 서버·개발서버 금지.

검수는 **PASS(FAIL 0)** 다. 계약은 맞게 돈다. 셋 다 **단언·이름이 무른 자리**이고
검수가 **수정안을 한 줄씩 줬다.** 그대로 고쳐라.

## WARN-1 — L-08 의 「리드」가 단언되지 않는다

`tests/contract/test_task_checklist_read_scope.py:86` 이 **지호가 lead 라는 사실을 재지 않고**
`projects.py:172-179`(만든 사람을 `kind=lead` 로 붙인다)라는 **코드 기본값에만 기댄다.**
그 기본이 바뀌면 **L-08 이 조용히 관측 대상을 잃는다**(테스트는 계속 초록인데 리드를 안 재게 된다).

→ 검수 수정안: `assert ("jiho","lead",None) in _history(...)` 한 줄.
**그 줄이 실제로 지키는 것**을 docstring 에 한 줄로 적어라.

## WARN-2 — L-03 대비군이 「422 가 났다」까지만 잰다

`tests/contract/test_project_membership_follows_work.py:141`.
그 라우트는 **다른 이유로도 422** 를 낸다. 오늘은 실제로 그 게이트를 재지만(검수 뮤테이션 M2 로 확인)
**이유가 바뀌면 그대로 초록이다.**

→ 검수 수정안: `assert "올릴 수 있는 자격" in planned.text` 한 줄.
**정확한 문구를 코드에서 확인해서** 넣어라(추측하지 마라).

## WARN-3 — 테스트 «이름»이 낡은 계약을 주장한다

`tests/contract/test_task_checklist.py:88` 의 이름에 `can_see_or_change` 가 남아 있다.
**같은 파일 docstring 은 앞 판에서 고쳤는데 이름은 안 고쳤다.** 단언은 여전히 참이라 FAIL 은 아니다.

→ **이름을 지금 계약에 맞게** 바꿔라(읽기는 프로젝트가 열고 쓰기는 담당이 쥔다).
이름만 바꾸고 **단언은 건드리지 마라.**

## 검증

- 셋을 고친 뒤 **그 세 테스트가 여전히 초록**인지 확인
- **뮤테이션으로 확인하라** — WARN-1·WARN-2 는 「더한 단언이 실제로 무언가를 잡는가」가 핵심이다.
  해당 구현·설정을 한 줄 무력화하면 **그 단언이 빨강이 되는가**. 안 되면 단언이 무의미한 것이다
- `make test-contract` 를 **한 번만** 돌려라 (⚠ 기계에 사용자 E2E 스택이 떠 있어 부하가 높다.
  직렬 패스가 400초를 넘을 수 있고, 그때 `material_*` 이 **부하 때문에** 깨질 수 있다 —
  **그것은 네 탓이 아니다.** 나오면 분리해서 보고만 해라)

## 역할·맥락

너는 **strong-hajin `backend` 워커**다. 먼저 읽어라:
- `.../roles/strong-hajin/backend/role.md` (+ 같은 폴더 `.md`) · 코드 레포 `AGENTS.md`
- `review-loop2-be-report.md`(검수) · `loop2-be-report.md`(앞 판이 한 일)

워크트리 `/Users/kknaks/orca/workspaces/Strong_hajin/strong-hajin-projects`.
⚠ `frontend/` 에 다른 워커가 붙어 있다 — **건드리지 마라.**

## 완료 보고 — **문구 변경 금지**

```bash
orca orchestration send \
  --to term_bdba055b-758b-4dc9-85c3-7836d56b615a --from term_3d3cc171-6937-4497-9eb7-022435e58993 \
  --type worker_done --task-id <taskId> --dispatch-id <dispatchId> \
  --subject "backend 완료: BE-3 소수정" \
  --body "WARN 셋 각각 어떻게 닫았나 / 뮤테이션 결과 / 테스트 수치(부하 실패는 분리) / git status"

orca terminal send --terminal term_bdba055b-758b-4dc9-85c3-7836d56b615a \
  --text "[worker_done] backend 완료 — BE-3 소수정. 상세는 인박스." --enter
```
