# SPEC-005 · WORK-005 정정 3 — 구현이 드러낸 사실 셋을 계약에 반영한다

**고칠 파일 둘**:
- `para/projects/summer-star/strong-hajin/20-spec/spec-005-projects.md`
- `para/projects/summer-star/strong-hajin/30-work/work-005-projects.md`

**배경**: BE·FE 구현과 검수가 끝났다. 계약이 **코드 사실과 어긋난 자리 하나**와
**문구가 구현을 못 담는 자리 둘**이 나왔다. 코디가 방향을 정했다 — 그대로 반영하라.

---

## 정정 1 — 떼는 자리 #4 는 **표면이 오늘 없다** (가장 중요)

SPEC §4 의 떼는 자리 #4「직접 배정·담당 교체 제안의 철회 —
`POST /api/action-items/{action_item_id}/commands/cancel_assignment`」는 **부를 길이 없다.**

**근거(코디가 코드로 확인함)**
- `normalize_assigned_task_draft` 가 초안에 **`'project_id': None` 을 강제로 박는다**
  (`modules/work/drafts.py:33`)
- `cancel_assignment` 봉투는 **그 AX 제안 위에만 선다**
  (`platform/actions.py:539` · `modules/actions/policy.py:136`)
- 따라서 **프로젝트가 걸린 유일한 pending 배정**(담당 교체 제안이 세우는 행)에는
  **철회 표면이 HTTP·MCP·판단함 어디에도 없다**

**고칠 것**
- 떼는 자리 표에서 #4 를 **「표면이 오늘 없다 — 메서드는 준비돼 있고 표면이 생기면 그대로 돈다」**로
  바꾸고 위 근거를 단다. **실질 떼는 자리는 셋**(요청 거절 · 요청 철회 · `decline`)
- **붙는 자리 #2 를 뺐을 때와 같은 서식**으로 쓴다 — 그 선례가 이미 문서에 있다
- 관련 인수조건을 **관측 가능한 형태로** 고친다: 표면이 없는 것을 테스트가 증명할 수는 없으므로,
  **「메서드 수준에서 해제가 돈다」**와 **「표면이 없다는 사실」**을 갈라 적는다
- WORK-005 의 BE-2 완료 판정·Open Issues 도 같이 맞춘다

## 정정 2 — 「선의 개수가 줄지 않는다」 문구가 구현을 못 담는다

FE 는 접힌 가지의 선을 **세 갈래로** 처리한다(검수 PASS, 코디 승인):

| 경우 | 처리 |
|---|---|
| 한쪽이 접힌 가지 안 | **가장 가까운 서 있는 조상**(접힌 부모 바)에 닻을 박아 **선을 그린다** |
| **양 끝이 같은 접힌 가지 안** | 선이 아니라 **그 행이 건수로 든다**(`__folded` 배지 + title) — 자기를 가리키는 화살표는 뜻이 없다 |
| 한쪽이 기간 없거나 볼 수 없는 업무 | **머리줄이 건수로 말한다**(`__legend--warn`) |

지금 인수조건은 「접기 전후 **선의 개수**가 같다」라 **둘째 경우와 글자 그대로 어긋난다.**

**고칠 것**: 인수조건을 **「사라지지 않는다」**로 다시 쓴다 —
「접어도 **어떤 관계도 화면에서 사라지지 않는다**: 선으로 남거나, **건수로 남는다**.
**말없이 버려지는 경로가 없다**」. 세 갈래를 표로 적고, 각각이 **어떻게 관측되는지**를 단다.

## 정정 3 — 모수 0 일 때 전체 진행률은 **「—」** 다

DEC-004 D-04 는 「완료 ÷ (전체 − 취소)」만 정했고 **모수가 0 인 경우를 정하지 않았다.**
구현은 **「—」**(0% 아님)로 냈고 **코디가 승인**했다 — D-02(「셀 것이 없으면 말하지 않는다」)와 같은 결이다.

**고칠 것**: SPEC §2.3 과 Data Contract 에 그 경우를 **`(제안)`** 으로 적는다.
「업무가 0건이면 **「—」를 낸다. 0% 로 두지 않는다** — 0% 는 「아무것도 안 했다」는 거짓이 된다」.
D-04 가 정한 것처럼 쓰지 마라.

---

## 하지 말 것

- **새 계약·새 결정을 만들지 마라.** 위 셋 밖은 건드리지 마라
- 색인·`log.md` 금지. **커밋·push 금지.** 지정 두 파일 밖 변경 0건

## 검증

- 떼는 자리 **셋 + 표면 없는 하나**가 SPEC·WP **양쪽에서 같은 수**다
- 「사라지지 않는다」 인수조건이 **세 갈래를 전부** 담고 각각 **관측 방법**이 달려 있다
- 정정 셋 각각을 **어디에 어떻게 반영했는지** 보고에 한 줄씩
- `git status --porcelain` 이 **두 파일만** 바뀐 것을 보인다

## 역할·맥락 (터미널이 새로 떴다면)

너는 **strong-hajin `architect` 워커**다. 먼저 읽어라:
- `/Users/kknaks/orca/workspaces/kknaks_profile/strong_hajin/orchestration/roles/strong-hajin/planner/role.md`
  (+ 같은 폴더 `.md`. ⚠ `scripts/lint-pipeline.py` 는 이 레포에 없다 — 린트 건너뛰어라)
- `review-be-report.md` · `review-fe-report.md` · `be-fix-report.md` · `fe-impl-report.md`
작업 워크트리 `/Users/kknaks/orca/workspaces/kknaks_profile/strong_hajin`.
⚠ 코디네이터가 같은 워크트리에 있다 — 지정한 두 파일 밖은 건드리지 마라.

## 완료 보고 — **문구 변경 금지**

```bash
orca orchestration send \
  --to term_bdba055b-758b-4dc9-85c3-7836d56b615a --from term_08a9ebaa-6a84-4c30-a343-445d097496e3 \
  --type worker_done --task-id <taskId> --dispatch-id <dispatchId> \
  --subject "architect 완료: SPEC·WP 정정 3" \
  --body "정정 셋 각각 어디에 반영했나 / 떼는 자리 수가 양쪽에서 같은지 / git status"

orca terminal send --terminal term_bdba055b-758b-4dc9-85c3-7836d56b615a \
  --text "[worker_done] architect 완료 — SPEC·WP 정정 3. 상세는 인박스." --enter
```
