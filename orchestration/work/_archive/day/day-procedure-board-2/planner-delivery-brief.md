# [planner] CENTURION_DAY Delivery Issue 발행 — 데모/운영 연결 구분 없앰 (DAY-SPEC-000 · 001 · 002)

너는 앞 작업(task_8dffb1d9d28e)을 한 day planner 워커다. 같은 스펙 워크트리 `/Users/kknaks/orca/workspaces/mediness-mediness/day-procedure-board-2-spec`(브랜치 `kknaksss/day-procedure-board-2-spec` · 스펙 PR **#920** · 아직 머지 안 됨).

## 할 일
레포 Skill **`start-delivery`**(`.claude/skills/start-delivery/SKILL.md` · `rules/delivery-workflow.md` · CLI 입력은 `tools/harness/references/requests.md`)를 따라 **CENTURION_DAY(MediSolveAIDev/CENTURION_DAY) 에 Delivery Issue 1건**을 연다.

- 결과 계약 원천: `/Users/kknaks/orca/workspaces/kknaks_profile/cc-2ck/orchestration/work/day-procedure-board-2/planner-demo-vs-live-report.md` 「Delivery Issue 초안」 D1~D5 — **하나의 Delivery** 로 묶는다(사용자: 코드 PR 하나 → dev). D5(데모 실물 확인)는 Acceptance 에.
- **리뷰 W3 반영**: D4 테스트에 `backend/tests/day/.../test_board_api.py:370-`(`test_재호출은_KOS_호출을_다시_보내고_앞_호출은_닫힘` — 데모 연결 전제) 「데모 전제 제거 · 확인」 한 줄 추가. 리뷰: `/Users/kknaks/orca/workspaces/kknaks_profile/cc-2ck/orchestration/work/day-procedure-board-2/review-doc-demo-vs-live-report.md`
- target SPEC: DAY-SPEC-000 · DAY-SPEC-001 · DAY-SPEC-002. **PR #920 이 아직 main 에 없으므로** Skill 규칙대로 `spec-baseline:pending` 으로 시작한다(머지 뒤 같은 idempotency key 로 재결속 — 1차 #224~#227 과 같은 방식). baseline 을 지어내지 마라.
- 위험 수준: 외부(KOS) 쓰기 범위가 바뀌고 migration(칸 삭제)이 있다 → 레포 규칙의 분류를 적용(L3 예상). L2/L3 면 `delivery-plan:review` 에서 **멈춘다** — 승인은 사용자 몫. 대신 승인하지 마라.
- Execution: 코드 레포 `/Users/kknaks/orca/workspaces/CENTURION_DAY/day-procedure-board-2`(origin/dev 91728737) 에서 code surface · phase · verification · rollback 을 근거가 있는 만큼 채운다. 리서치 `/Users/kknaks/orca/workspaces/kknaks_profile/cc-2ck/orchestration/work/day-procedure-board-2/research-demo-vs-live-report.md` §1 · §3 이 자리 목록.
- 같은 코드 PR 에 들어갈 **개발 도구** `scripts/seed_demo_board.py` · `backend/tests/scripts/`(KOS 데모 지점 테스트 데이터 · 스펙 무관 · 리뷰 PASS — `/Users/kknaks/orca/workspaces/kknaks_profile/cc-2ck/orchestration/work/day-procedure-board-2/review2-seed-demo-board-report.md`)를 Delivery 에 「같은 PR 에 포함되는 개발 도구」 한 줄로 적는다(결과 계약 범위 밖임을 분명히).
- idempotency key 예: `day/demo-live-unify`. 이슈 제목 · 본문은 한국어 · 화면 문구 지어내지 않음.

## 하지 말 것
- 코드 수정 · 커밋 금지(이번엔 Issue 발행만). 스펙 파일을 고쳐야 하면 고치지 말고 보고
- Delivery 승인 · 라벨 변경을 대신 하지 마라 · MCP Task 승인 카드 선택 금지

## 완료 보고
Issue 번호 · URL · 라벨(상태) · risk_level · plan_digest · next_action. 원 브리프 §9 와 같은 두 명령, 코디 핸들 `term_b915fb18-742f-4779-962c-79848020b8d5`.
