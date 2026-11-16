# [planner] fix 스펙 9판 — 저장소 정정 3(환경 = 컨테이너 · 환경 폴더 없음)

너는 day planner 워커(같은 터미널)다. 스펙 워크트리 `/Users/kknaks/orca/workspaces/mediness-mediness/fix-spec`(8판 미커밋 위에 이어서). 커밋 · push 금지.

반영할 것: `/Users/kknaks/orca/workspaces/kknaks_profile/day-r3/orchestration/work/fix/correction-storage-3.md` 「결정」 1 ~ 6 · 「planner」 줄 전부. 8판에서 「환경 폴더는 그대로」로 적은 자리를 **전부 찾아** 고친다(한 절만 고치고 다른 절이 옛 말을 하게 두지 않는다 — `{APP_ENV}/` · `dev/chat` · 「맨 위 = 환경」 · 「키의 환경」 grep).

- 컨테이너 이름 `daydev` · `dayprod` 는 사용자가 정한 이름이다 — 문서에 적어도 된다(계정 이름 · 주소는 계속 적지 않는다).
- 「지금은 컨테이너 `daydev` · `dayprod` 가 아직 없다 · 사용자가 인프라에 요청」을 사실로 적는다.
- `wp-plan.md` WP-BE-4 도 같이. Delivery #241 은 정정 문서의 규칙대로(계약 문장에 경로가 있으면 version 올리고 승인 적용 · 없으면 그대로).

검증: `python3 scripts/lint-pipeline.py --strict`(products/day ERROR 0).
리포트: `/Users/kknaks/orca/workspaces/kknaks_profile/day-r3/orchestration/work/fix/spec-9-report.md`(고친 자리 문서:줄 · 옛 문장 grep 0 확인 · Delivery 처리).

끝나면 두 명령 모두(핸들은 dispatch preamble 값이 우선):

```bash
orca orchestration send --to term_284b2ffb-0602-4a35-b76f-0f005373d1e2 --from term_bf6ad1b2-354a-4423-8fd4-eb60fc4732c8 --type worker_done --task-id <taskId> --dispatch-id <dispatchId> --subject "planner 완료: <한 줄>" --body "고친 자리 / Delivery 처리 / lint"
orca terminal send --terminal term_284b2ffb-0602-4a35-b76f-0f005373d1e2 --text "[worker_done] planner 완료 — <한 줄 요약>. 상세는 인박스." --enter
```
