# [backend] #230 fix2 — #231 이 요청한 두 가지

너는 #230 backend 워커다. 같은 워크트리 · 미커밋 · 커밋 금지 · 템플릿 · day.js 는 건드리지 마라. 읽을 것: `/Users/kknaks/orca/workspaces/kknaks_profile/day/orchestration/work/day-data-architecture/frontend-231-fix1-report.md` 「요청」 · 「남은 것」.
1. `routers/board.py` `_render_board`(GET `/board` · 모든 조작 응답)가 `render(..., permissions=…, is_admin=…)` 를 넘긴다 — 조작 응답은 세션에서 권한을 읽는다(권한 검사 한 곳 · `DAY_ADMIN_EMAILS` 규칙 그대로). 테스트(DB 없이 가능하면 · 아니면 infra 1): 권한 없는 세션 → 조작 버튼 없음.
2. **`call.lateAt` = 원천 U12 규칙 그대로**(코디 결정 — 새 결정 아님): 호출은 `created_at` + 5분(재호출이면 열린 호출의 `created_at` — SPEC-002 OQ-04 시간 ⓐ) · 마취는 20분. 그 밖은 lateAt 없음. 테스트 DB 없이.
검증: `uv run pytest -m "not infra"` · `scripts/test.sh -q` · ruff · compose down 금지 · 끝나면 api 만 재빌드.
리포트 `/Users/kknaks/orca/workspaces/kknaks_profile/day/orchestration/work/day-data-architecture/backend-230-fix2-report.md`(짧게). 완료는 preamble 의 worker_done 절차대로(둘 다).
