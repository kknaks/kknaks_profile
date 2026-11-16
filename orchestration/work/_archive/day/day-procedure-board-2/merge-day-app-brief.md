# [backend] 앱 브랜치 합치기 — PR #237(kknaksss/day-app) → PR #238 브랜치

같은 워크트리 `/Users/kknaks/orca/workspaces/CENTURION_DAY/day-procedure-board-2`(브랜치 `kknaksss/day-procedure-board-2` · HEAD 9ba7b79e · 깨끗해야 함). 사용자 결정(2026-11-10): 앱도 같은 PR #238 로 — `origin/kknaksss/day-app`(HEAD f83d7fab · dev 91728737 에서 갈라짐 · 앱 5 + 백엔드 4 커밋)을 이 브랜치에 **합친다**.

## 할 것
1. `git fetch origin` · `git merge --no-commit --no-ff origin/kknaksss/day-app` — **커밋하지 마라**(코디가 확인 뒤 커밋)
2. 충돌 3개 풀기(시험 merge 결과): `backend/day/routers/api/auth.py` · `backend/day/services/board.py` · `backend/tests/migrations/test_alembic.py`
   - 원칙: **#234 · #236(이 브랜치)의 동작 · 계약은 그대로**, 앱 쪽이 더한 것(데모 계정 로그인 환경 · 채팅 · 기기 · 알림 · 푸시 · board 에서 알림 신호 등)은 살린다. 둘이 같은 자리를 바꿨으면 둘 다 살리는 쪽 — 판단이 필요하면 멈추고 질문
   - migration: `0006_event_log_visit_type` 은 두 쪽 같은 파일(내용 같음 확인) · 앱의 `0007_chat_device` 의 down_revision 이 0006 인지 · head 하나 · `test_alembic` HEAD 상수 = 0007
3. 자동 병합된 겹친 파일(`common/config.py` · `models/task.py` · `tests/deploy/test_day_vm.py` · `deploy/config/dev.env` · `prod.env` · `compose.local.yaml`)도 열어 서로 덮은 것 없는지 확인
4. 검증: `DAY_ENV_FILE=/Users/kknaks/git/CENTURION_DAY/deploy/local.env scripts/test.sh -q`(infra 포함 · 전부) · `uv run ruff check backend scripts` · format · `alembic heads` 하나 · build-css(템플릿 겹치면) · 앱은 `cd app && flutter analyze` 1회(되면 · 안 되면 사유)
5. 하지 말 것: 커밋 · push · PR 조작 · 앱/백엔드 기능 새로 짓기 · 사용자 포트/프로세스(로컬 day-local 재기동은 코디)

## 완료 보고
`orca orchestration send --to term_28f2b422-a0ae-490a-bbed-aeb19fbd7fdd --from <네 워커handle> --type worker_done --task-id <taskId> --dispatch-id <dispatchId> --subject "day-app 합치기: <한 줄>" --body "충돌 3개 각각 어떻게 풀었나 · 겹친 파일 확인 · 테스트 수 · alembic head · flutter analyze · 미결"` + `orca terminal send --terminal term_28f2b422-a0ae-490a-bbed-aeb19fbd7fdd --text "[worker_done] day-app 합치기 — <한 줄>" --enter`.
