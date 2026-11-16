# [planner] fix 스펙 8판 — 저장소 7판 리뷰 지적(W1 ~ W7) + 사용자 결정 반영

너는 day planner 워커(같은 터미널)다. 스펙 워크트리 `/Users/kknaks/orca/workspaces/mediness-mediness/fix-spec`(7판 미커밋 위에 이어서). 커밋 · push 금지.

반영할 것: `/Users/kknaks/orca/workspaces/kknaks_profile/day-r3/orchestration/work/fix/correction-storage-2.md` 의 「사용자 결정」 1 · 2 와 「스펙(planner)이 반영할 것」 W1 ~ W7 전부 — 리포트 `…/work/fix/review-doc-3-report.md`.

- 폴더 이름 셋은 이제 **사용자 확정**이다(OQ · 미결 줄 정리).
- 컨테이너 이름 = 환경별 설정값(지금은 하나라 같은 값) · 컨테이너 분리 = 사용자가 인프라에 요청 — 미결 줄을 그렇게 고친다. 판단 · 권고 문장을 붙이지 않는다(사실만).
- 값(계정 이름 · 주소 · 컨테이너 이름 등)은 적지 않는다.
- `wp-plan.md` WP-BE-4 도 같이. Delivery #241 은 범위가 그대로면 건드리지 않는다(바뀐다고 판단되면 고치지 말고 보고).

검증: `python3 scripts/lint-pipeline.py --strict`(products/day ERROR 0).
리포트: `/Users/kknaks/orca/workspaces/kknaks_profile/day-r3/orchestration/work/fix/spec-8-report.md`(항목별 고친 자리 문서:줄).

끝나면 두 명령 모두(핸들은 dispatch preamble 값이 우선):

```bash
orca orchestration send --to term_284b2ffb-0602-4a35-b76f-0f005373d1e2 --from term_bf6ad1b2-354a-4423-8fd4-eb60fc4732c8 --type worker_done --task-id <taskId> --dispatch-id <dispatchId> --subject "planner 완료: <한 줄>" --body "항목별 결과 / lint"
orca terminal send --terminal term_284b2ffb-0602-4a35-b76f-0f005373d1e2 --text "[worker_done] planner 완료 — <한 줄 요약>. 상세는 인박스." --enter
```
