# [planner] DAY-SPEC-002 를 stable 로 (문서 변경만)

너는 day planner 워커(같은 터미널)다.

사용자(2026-11-11): 「아 그럼 스테이블에 올리고 다 닫자」 → 「다음 작업이라고, 이제 다 한 거잖아. 검증은 다음에 하자니까. 닫는 데 문제가 있어?」 — Delivery 를 **전부 닫는다.** 2차 Delivery #234 · #236 · #239 가 DAY-SPEC-002 draft 때문에 baseline 에 묶이지 않으므로(네 `spec-stable-report.md`), SPEC-002 도 stable 로 올린다. 코디 판단: 사용자의 「스테이블에 올리고 다 닫자」가 닫는 데 필요한 stable 전환을 포함한다.

스펙 워크트리 `/Users/kknaks/orca/workspaces/mediness-mediness/fix-spec` — 코디가 새 브랜치 **`kknaksss/fix-app-re1-spec002-stable`**(= `origin/main` `caf7f3eb` · 깨끗함)으로 옮겨 놓았다. 커밋 · push · PR 은 코디가 한다.

## 할 것

SPEC-000 때와 **같은 방식**(네가 한 그대로): `products/day/20-spec/spec-002-procedure-board.md` `status: draft` → `stable` · 머리 한 줄 · `20-spec.md` SPEC List 상태 칸 · `10-decision.md` 등 「SPEC-002 는 draft」라고 적은 자리(grep) · `log.md`. 내용 · 열린 OQ · 버전은 그대로. 막는 규칙이 있으면 고치지 말고 보고.

검증: `python3 scripts/lint-pipeline.py --strict`(products/day ERROR 0).

리포트: `/Users/kknaks/orca/workspaces/kknaks_profile/day-r3/orchestration/work/fix/spec002-stable-report.md`(바꾼 자리 · lint).

끝나면 두 명령 모두(핸들은 dispatch preamble 값이 우선):

```bash
orca orchestration send --to term_284b2ffb-0602-4a35-b76f-0f005373d1e2 --from term_bf6ad1b2-354a-4423-8fd4-eb60fc4732c8 --type worker_done --task-id <taskId> --dispatch-id <dispatchId> --subject "planner 완료: <한 줄>" --body "바꾼 자리 / lint"
orca terminal send --terminal term_284b2ffb-0602-4a35-b76f-0f005373d1e2 --text "[worker_done] planner 완료 — <한 줄 요약>. 상세는 인박스." --enter
```
