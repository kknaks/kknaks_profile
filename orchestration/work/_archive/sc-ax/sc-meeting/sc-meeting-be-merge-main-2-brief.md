# [backend] origin/main 머지 충돌 해소 — backend/ 13개 + Makefile

너는 **sc-ax backend 워커**다. 세션 그대로. 워크트리 `/Users/kknaks/orca/workspaces/ax-workspace/sc-meeting`. **코디가 `git merge --no-ff --no-commit origin/main` 을 걸어 둔 상태다(MERGE_HEAD 있음).** 커밋·push·`git merge --abort`·`git reset` **절대 금지** — 충돌 파일을 풀고 `git add <파일>` 까지만. FE 워커가 같은 트리에서 `frontend/` 를 병렬로 푼다 — `frontend/` 건드리지 마라. pytest 스위트 금지(사용자 지시) — import 확인만.

## main 에 들어온 것(우리 브랜치에 없던 것)
- #3 「SCAX 채팅창 인터랙션 고도화」 · #8 「프로젝트 참여 이력 보존」. `git log --oneline HEAD..MERGE_HEAD` · `git diff HEAD...MERGE_HEAD -- <파일>` 로 그쪽 의도를 읽어라.

## 네 몫(`git status` 의 UU/AA/DU/UD 중)
Makefile · bootstrap/application.py · bootstrap/material_sources.py · entrypoints/http.py · entrypoints/mcp.py · modules/meetings/application.py · platform/codex_cli.py · platform/materials.py · platform/meetings.py · platform/native_materials.py · platform/persistence.py · tests/contract/test_mcp.py · tests/contract/test_meeting_core.py · tests/contract/test_meeting_material_search.py

## 원칙
- **둘 다 살린다.** 우리 쪽(HEAD)은 회의·미팅노트 1차 전체(WP-001~007, D25~D51)이고 main 쪽은 채팅·프로젝트다. 같은 자리(조립·라우터·persistence·MCP 도구 목록·Makefile 타깃)에 양쪽이 줄을 더한 것은 **둘 다 넣는다**. 우리가 지운 것(회의 native 자료 다리·구 MeetingDrawer 경로 등)을 main 이 아직 참조하면 main 쪽 참조를 우리 결정대로 걷는다(어디를 걷었는지 보고에).
- 충돌 마커 0 · 모듈 경계 규칙 그대로 · `python -c "import ax_workspace.entrypoints.http, ax_workspace.entrypoints.mcp, ax_workspace.bootstrap.meeting_worker"` 통과.
- 스키마: persistence 양쪽 열·테이블 모두 살림. 새 열이 생기면 보고에(코디가 sync-demo-schema).

## 완료 보고 — **문구 변경 금지**
```bash
orca orchestration send \
  --to term_828dfb7e-5785-487c-b90c-863c6eaa8261 --from term_50bcf0cc-bae5-4c55-b23a-4143537dd1f3 \
  --type worker_done --task-id <taskId> --dispatch-id <dispatchId> \
  --subject "backend 완료: main 머지 충돌 해소(backend)" \
  --body "푼 파일 / 양쪽 살린 자리·걷은 자리 / import 확인 / 새 열 / 미결"
orca terminal send --terminal term_828dfb7e-5785-487c-b90c-863c6eaa8261 \
  --text "[worker_done] backend 완료 — main 머지(backend). 상세는 인박스." --enter
```
