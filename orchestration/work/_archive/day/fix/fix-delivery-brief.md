# [planner] CENTURION_DAY Delivery Issue 발행 + 승인 기록 — fix (실기기 피드백 · 통역 서버)

너는 day planner 워커다(스펙 1 ~ 3판 · `wp-plan.md` 를 쓴 같은 터미널). 스펙 워크트리 `/Users/kknaks/orca/workspaces/mediness-mediness/fix-spec`(브랜치 `kknaksss/fix-spec` · **스펙 PR 아직 없음 · 변경 미커밋**).

사용자 지시(2026-11-11): 「왜 이슈로 안 했어. 일단 이거 올리고 승인 처리 하자」 — 코디가 Delivery 등록을 미뤘던 것을 바로잡는다.

## 1. Delivery Issue 발행

레포 Skill **`start-delivery`**(`.claude/skills/start-delivery/SKILL.md` · `rules/delivery-workflow.md` · CLI 입력 `tools/harness/references/requests.md`)를 따라 **CENTURION_DAY(MediSolveAIDev/CENTURION_DAY)에 Delivery Issue 1건**을 연다.

- 결과 계약 원천: `/Users/kknaks/orca/workspaces/kknaks_profile/day-r3/orchestration/work/fix/wp-plan.md` 의 WP 4개(BE-1 · BE-2 · APP-1 · APP-2) — **하나의 Delivery 로 묶는다**(사용자 규칙: 코드 PR 하나 → dev · 앱도 같은 PR). WP 는 phase 로. 수용 항목 · 실물 확인(A-45 워커 · A-46 사용자 실기기 등)은 Acceptance 에 누구 몫인지와 함께.
- target SPEC: DAY-SPEC-003 · DAY-SPEC-004 · DAY-SPEC-005 · DAY-SPEC-000(+ 배포 문서). **스펙 변경이 아직 main 에 없으므로** Skill 규칙대로 `spec-baseline:pending` 으로 시작한다(스펙 PR 머지 뒤 같은 idempotency key 로 재결속 — 2차 #234 ~ #239 와 같은 방식). baseline 을 지어내지 마라. SPEC-000 이 draft 인 것 때문에 막히면 **우회하지 말고 그 상태를 보고**한다.
- 위험 수준: 레포 규칙의 분류를 그대로 적용한다(외부 서비스 Soniox 연동 추가 · 새 선택 비밀 · 새 의존성 · migration 없음).
- Execution: 코드 레포 `/Users/kknaks/orca/workspaces/CENTURION_DAY/fix`(`kknaksss/fix` · origin/dev `378e3ae3`)에서 code surface · phase · verification · rollback 을 `wp-plan.md` 에 근거가 있는 만큼 채운다.
- 이미 dev 에 들어간 것(#240 — 앱 아이콘 · 수출 규정 키 · dev.env 앱 연결 설정)은 이 Delivery 의 결과 계약 **밖**이다. 「같은 작업(fix)에서 먼저 머지된 설정 PR」로 한 줄만 적는다.
- idempotency key: `day/fix-device-feedback-interpret`. 제목 · 본문 한국어 · 화면 문구 지어내지 않음 · 값(키 · Vault 이름 · IP · Key ID · Team ID) 없음.
- 2차 Delivery(#234 · #235 · #236 · #239)는 **건드리지 않는다**(닫기 · 라벨 · 재결속 금지 — 따로 사용자와 닫는다). #235 에 「서버 변경 기록」을 덧붙이는 일도 이번에 하지 않는다.

## 2. 승인 기록

사용자(담당자 · GitHub `kknaksss`)는 위 지시에서 이 Delivery 의 **승인까지** 말했다. 그래서 발행 뒤 `delivery-plan:review` 에 서면:

1. plan_digest 를 확인한다.
2. 결과 계약이 `wp-plan.md` · 스펙과 **같은 범위**인지 스스로 대조한다. 범위가 넓어졌거나(계획에 없는 것이 들어감) 위험 수준이 예상과 다르게 높게 잡혀 추가 조건이 붙었다면 **승인하지 말고 멈춰서 보고**한다.
3. 같으면 `start-delivery` 규칙대로 receipt `{"decision":"approved","reviewer_type":"human","reviewer":"kknaksss","plan_digest":"<그 digest>"}` 로 같은 request 를 `--plan` 으로 digest 확인 뒤 `--apply` 한다. 계약 · digest 를 바꾸지 않는다.

MCP Task 승인 카드는 대신 처리하지 않는다.

## 하지 말 것

- 코드 · 스펙 파일 수정 · 커밋 · push · PR 금지(이번엔 Issue 발행 · 승인 기록만). 스펙을 고쳐야만 발행이 되면 고치지 말고 보고.
- request JSON 은 scratchpad 에 두고 경로를 보고에 적는다(레포에 넣지 않음).

## 완료 보고

리포트: `/Users/kknaks/orca/workspaces/kknaks_profile/day-r3/orchestration/work/fix/delivery-report.md` — Issue 번호 · URL · 라벨(상태) · risk_level · plan_digest · baseline 상태 · next_action · request 경로 · 승인 적용 여부(안 했다면 이유).

> **⚠ 핸들은 dispatch preamble 의 값을 믿어라.**

끝나면 **두 명령 모두**:

```bash
orca orchestration send \
  --to term_284b2ffb-0602-4a35-b76f-0f005373d1e2 --from term_bf6ad1b2-354a-4423-8fd4-eb60fc4732c8 \
  --type worker_done \
  --task-id <dispatch context 의 taskId> \
  --dispatch-id <dispatch context 의 dispatchId> \
  --subject "planner 완료: <한 줄>" \
  --body "Issue 번호 / 라벨 / risk / digest / 승인 적용 여부 / next_action"

orca terminal send --terminal term_284b2ffb-0602-4a35-b76f-0f005373d1e2 \
  --text "[worker_done] planner 완료 — <한 줄 요약>. 상세는 인박스." --enter
```

막히면: `orca terminal send --terminal term_284b2ffb-0602-4a35-b76f-0f005373d1e2 --text "[질문] planner: <질문>" --enter`
