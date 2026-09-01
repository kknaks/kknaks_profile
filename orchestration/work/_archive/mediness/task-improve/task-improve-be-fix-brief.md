
# [backend] WP-129 검수 WARN 정정 — W1 계층 역전 · W2 은퇴 어휘

너는 **mediness `backend` 워커**다. 검수 WARN 중 2건만 정정한다 — 좁은 라운드다.
역할 문서: `/Users/kknaks/orca/workspaces/kknaks_profile/task-improve/orchestration/roles/mediness/backend/role.md`

작업 워크트리: `/Users/kknaks/orca/workspaces/mediness-app/task-improve` (직전 산출물 미커밋 위에서 작업. **front/ 금지**)

## 1. SSOT

- `/Users/kknaks/orca/workspaces/kknaks_profile/task-improve/orchestration/work/task-improve/review-code-report.md` — W1·W2 절 (좌표·권장 수정)

## 2. 해야 할 일 — 이 2건만

**W1. 계층 역전 해소** — `back/app/repositories/action_runtime/runtime_task_repo.py:357` 이 `app/services/.../tasks/request_axis` 를 import 한다(repositories/ 전체에서 유일한 역방향 — 이 레포 계층 규약은 router→service→repository 단방향). **요청 판정 SQL 술어(request_predicate)를 repositories 층으로 옮기고 service 가 그것을 재사용**하는 방향으로 정리하라. «판정 술어 한 곳» 계약(중복 정의 금지 grep 테스트)은 그대로 성립해야 한다 — 한 곳의 «곳»이 repo 로 옮겨가는 것뿐이다.

**W2. 은퇴 어휘 정리** — `decision/const.py:135 RETIRED_FLOW_TYPES` · `decision_form.py:125 RETIRED_FLOW_VALUES` · `decision_gate.py:526 _FLOW_FORM_VALUES` 세 벌이 독립이라 「재활성 한 줄」이 등록 seam 한정이다. **한 정본(RETIRED_FLOW_TYPES)에서 파생**하도록 묶어 재활성이 실제로 한 줄이 되게 하라. + `const.py:139 REGISTRABLE_FLOW_TYPES` 주석이 코드 사실과 반대(프로덕션 소비처 0)인 것 정정 — 소비처가 정말 0 이면 주석을 사실대로 고치거나 상수를 정리하라(삭제가 아니라 사실 정합).

**하지 말 것**: 위 2건 밖 수정 금지. 계약(판정식·API shape·FE 계약 3종) 불변. 테스트 계약 강화는 기존 테스트가 깨지지 않는 선에서만.

## 3. 검증

```
cd /Users/kknaks/orca/workspaces/mediness-app/task-improve/back && uv run pytest -q tests/api/test_wp129_task_request_axis.py tests/api/test_wp129_instruction_entrance_closed.py tests/services/engine_v2/test_wp129_chat_assignee.py tests/migrations/test_0137_tasks_created_by_index.py
```

- 49 passed 유지(재활성 한 줄 증명 테스트 포함). 네가 고친 파일이 영향 주는 기존 테스트 파일이 있으면 그 파일만 추가 실행. 전체 스위트 금지. 검증 1회만.

## 4. 완료 보고 — **문구 변경 금지**

> **⚠ 핸들은 dispatch preamble 의 값을 믿어라.**

```bash
orca orchestration send \
  --to term_d5bec05e-881f-4a29-a144-fd73be7e23c4 --from <네 워커handle> \
  --type worker_done \
  --task-id <preamble 의 taskId> --dispatch-id <preamble 의 dispatchId> \
  --subject "backend W1·W2 정정 완료: <한 줄>" \
  --body "정정 내용 / 테스트 수치 / 계약 불변 확인"

orca terminal send --terminal term_d5bec05e-881f-4a29-a144-fd73be7e23c4 \
  --text "[worker_done] backend W1·W2 정정 완료 — <한 줄>. 상세는 인박스." --enter
```

- 막히면: `orca terminal send --terminal term_d5bec05e-881f-4a29-a144-fd73be7e23c4 --text "[질문] backend: <질문>" --enter`
