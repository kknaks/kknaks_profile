# [planner] fix 스펙 10판 — 저장소 정정 4(컨테이너 이름 `dev` · `prod` · 이미 있음)

너는 day planner 워커(같은 터미널)다. 스펙 워크트리 `/Users/kknaks/orca/workspaces/mediness-mediness/fix-spec`(9판 미커밋 위에 이어서). 커밋 · push 금지.

반영할 것: `/Users/kknaks/orca/workspaces/kknaks_profile/day-r3/orchestration/work/fix/correction-storage-4.md` 전부. `daydev` · `dayprod` · 「아직 없음」 · 「인프라에 요청」을 **grep 으로 전부 찾아** 고친다(스펙 · `wp-plan.md`). 계정 이름 · 주소는 계속 적지 않는다.

Delivery #241: 결과 계약 · 수용 항목에 `daydev` 가 적혀 있다(v4) → version 을 올려 이름과 「있음」만 바로잡는다(더해진 범위 없음 · L3 그대로). 이것은 사실 정정이다 — 사용자가 컨테이너를 받아 알려 준 것(「컨테이너 안 받은 거 아니야?」)을 근거로 승인 receipt(`human` · `kknaksss`)를 적용한다. 범위 · 등급이 달라지면 멈추고 보고.

검증: `python3 scripts/lint-pipeline.py --strict`(products/day ERROR 0).
리포트: `/Users/kknaks/orca/workspaces/kknaks_profile/day-r3/orchestration/work/fix/spec-10-report.md`(고친 자리 · 옛 이름 grep 0 · Delivery 처리).

끝나면 두 명령 모두(핸들은 dispatch preamble 값이 우선):

```bash
orca orchestration send --to term_284b2ffb-0602-4a35-b76f-0f005373d1e2 --from term_bf6ad1b2-354a-4423-8fd4-eb60fc4732c8 --type worker_done --task-id <taskId> --dispatch-id <dispatchId> --subject "planner 완료: <한 줄>" --body "고친 자리 / Delivery 처리 / lint"
orca terminal send --terminal term_284b2ffb-0602-4a35-b76f-0f005373d1e2 --text "[worker_done] planner 완료 — <한 줄 요약>. 상세는 인박스." --enter
```
