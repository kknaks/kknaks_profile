# [planner] fix 스펙 5판 — 읽음 표시 계약 정정 1 반영

너는 day planner 워커(4판 작성자 · 같은 터미널)다. 스펙 워크트리 `/Users/kknaks/orca/workspaces/mediness-mediness/fix-spec`(4판 미커밋 위에 이어서).

**반영할 것**: `/Users/kknaks/orca/workspaces/kknaks_profile/day-r3/orchestration/work/fix/correction-read-1.md` 의 「결정」 1 · 2 · 3 을 SPEC-004(U-2 「메시지별 읽음 표시」 · 규칙 「읽음 표시 계약」 · 실시간 표 `chat_member_read` 줄 · 케이스 매트릭스 · C-A24 · C-A25) 와 `…/work/fix/wp-plan.md` §3 읽음 계약 표 · WP-BE-3 · WP-APP-3 시험 줄에 적는다. 출처 = 문서 리뷰 [긴급] 지적 · 코디 결정(2026-11-11). 사용자 확정을 바꾸는 것이 아니다 — 계약 구멍을 메우는 기술 규칙이라고 적는다.

문서 리뷰어가 4판 검수를 아직 하고 있다 — 리포트가 나오면 코디가 나머지 지적을 따로 보낸다. 이번엔 위 정정만.

Delivery #241 은 건드리지 않는다(결과 계약 범위 · 수용 항목 뜻이 그대로 — 바뀐다고 판단되면 고치지 말고 보고).

검증: `python3 scripts/lint-pipeline.py --strict`(products/day ERROR 0). 커밋 · push 금지.

리포트: `/Users/kknaks/orca/workspaces/kknaks_profile/day-r3/orchestration/work/fix/spec-5-report.md`(고친 자리 문서:줄).

끝나면 두 명령 모두(핸들은 dispatch preamble 값이 우선):

```bash
orca orchestration send --to term_284b2ffb-0602-4a35-b76f-0f005373d1e2 --from term_bf6ad1b2-354a-4423-8fd4-eb60fc4732c8 --type worker_done --task-id <taskId> --dispatch-id <dispatchId> --subject "planner 완료: <한 줄>" --body "고친 자리 / lint"
orca terminal send --terminal term_284b2ffb-0602-4a35-b76f-0f005373d1e2 --text "[worker_done] planner 완료 — <한 줄 요약>. 상세는 인박스." --enter
```
