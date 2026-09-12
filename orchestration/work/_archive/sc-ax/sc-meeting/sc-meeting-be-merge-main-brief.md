# [backend] origin/main 병합 — PR #5 충돌 해소 (bootstrap/application.py)

너는 **sc-ax backend 워커**다. 세션 그대로. 워크트리 `/Users/kknaks/orca/workspaces/ax-workspace/sc-meeting`(HEAD ab8a8ef, 브랜치 kknaksss/sc-meeting). **이번만 예외로 `git merge` 를 실행하되 커밋은 하지 않는다** — 충돌을 풀고 stage 까지만(MERGE_HEAD 를 남겨라). 커밋은 코디가 검증 뒤 한다. push·PR 금지.

## 상황
- origin/main 에 `3bd2294 feat(delivery): SCAX 보호 이미지 빌드 추가 (#6)` 하나가 들어와 PR #5 가 CONFLICTING. `git merge-tree` 결과 충돌 파일은 `backend/src/ax_workspace/bootstrap/application.py` 하나(Makefile 은 자동 병합).
- 우리 브랜치는 그 파일에 회의 모듈 조립(회의 배치·합성·회의실 gateway·승격 등)을 많이 넣었고, main 은 배포 이미지 관련 조립을 넣었을 것이다.

## 할 것
1. `git fetch origin && git merge --no-commit --no-ff origin/main`. 충돌 hunk 를 **양쪽 다 살리는 방향**으로 푼다(main 의 배포/이미지 조립 + 우리 회의 조립). `git show 3bd2294 -- backend/src/ax_workspace/bootstrap/application.py` 로 main 의 의도를 먼저 읽어라. Makefile 자동 병합 결과도 눈으로 확인(우리 SONIOX/THECONNECT env source 줄과 main 의 타깃이 공존하는지).
2. 검증: `cd backend && uv run pytest -q tests/contract/test_meeting_core.py tests/contract/test_meeting_rooms.py tests/contract/test_meeting_finalize.py tests/architecture -m 'not integration'` + main 이 추가한 테스트가 있으면 그것도. `cd frontend && npx tsc --noEmit`.
3. `git add` 로 stage 만. **`git commit` 금지**. `git status` 에 「All conflicts fixed but you are still merging」 상태로 남겨라.

## 완료 보고 — **문구 변경 금지**
```bash
orca orchestration send \
  --to term_828dfb7e-5785-487c-b90c-863c6eaa8261 --from term_50bcf0cc-bae5-4c55-b23a-4143537dd1f3 \
  --type worker_done --task-id <taskId> --dispatch-id <dispatchId> \
  --subject "backend 완료: origin/main 병합 충돌 해소(미커밋)" \
  --body "충돌 hunk 요약 / 푼 방향 / 검증 수치 / git status"
orca terminal send --terminal term_828dfb7e-5785-487c-b90c-863c6eaa8261 \
  --text "[worker_done] backend 완료 — main 병합(미커밋). 상세는 인박스." --enter
```
