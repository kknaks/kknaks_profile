# [planner] fix 스펙 6판 — 문서 리뷰 4판 나머지 지적(정정 2) 반영

너는 day planner 워커(같은 터미널)다. 스펙 워크트리 `/Users/kknaks/orca/workspaces/mediness-mediness/fix-spec`(5판 미커밋 위에 이어서).

- 반영할 것: `/Users/kknaks/orca/workspaces/kknaks_profile/day-r3/orchestration/work/fix/correction-read-2.md` 「스펙(planner)이 반영할 것」 전부(W2 ~ W9) — 리포트 `…/work/fix/review-doc-2-report.md` 의 해당 지적과 「조용히 통과하는 자리」도 같이 본다.
- W2 의 앱 규칙은 **코디 기본값**(카톡과 같은 겉보기 · 사용자 통보 · 뒤집을 수 있음)으로 표시한다.
- `wp-plan.md`(같은 폴더)도 같이 맞춘다. Delivery #241 은 건드리지 않는다(범위가 바뀐다고 판단되면 고치지 말고 보고).

검증: `python3 scripts/lint-pipeline.py --strict`(products/day ERROR 0). 커밋 · push 금지.

리포트: `/Users/kknaks/orca/workspaces/kknaks_profile/day-r3/orchestration/work/fix/spec-6-report.md`(지적별 고친 자리 문서:줄 · 못 고친 것과 이유).

끝나면 두 명령 모두(핸들은 dispatch preamble 값이 우선):

```bash
orca orchestration send --to term_284b2ffb-0602-4a35-b76f-0f005373d1e2 --from term_bf6ad1b2-354a-4423-8fd4-eb60fc4732c8 --type worker_done --task-id <taskId> --dispatch-id <dispatchId> --subject "planner 완료: <한 줄>" --body "지적별 결과 / lint"
orca terminal send --terminal term_284b2ffb-0602-4a35-b76f-0f005373d1e2 --text "[worker_done] planner 완료 — <한 줄 요약>. 상세는 인박스." --enter
```
