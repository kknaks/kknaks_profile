# fe-fix-2 결과 보고 — review-code-1 W3 · W6
## 상태: done (커밋 안 함)

## 수행
- W3(C21-기본값) — `backend/day/static/day.js`: 새 `chartLock(form, on)` = 그 탭 글 칸 `readOnly` · 담당자 고르기 트리거 `disabled` · form `aria-busy`. `chartSave` 가 요청을 보내기 **전에** 잠그고(`chartLock(form, true)`), `htmx:afterRequest` 가 form 이 그대로 남았으면(실패 · 시간 초과 · HX-Reswap none 오류) 푼다(`if (form.isConnected) chartLock(form, false)`) — 기준값을 다시 잡지 않으므로 바뀐 줄 · [저장] 켜짐 그대로. 200 · 409 는 응답 form 이 통째로 바뀌어 새 칸(잠금 없음).
- W6 — `.agents/skills/verify-day-web/SKILL.md:130` 「입력·자동 저장·닫기」 → 「입력·[저장]·닫기」.
- 테스트: `scripts/frontend/tests/chart-save.test.mjs` — 기존 [저장] 테스트에 「요청 전에 잠금」 단정 · 새 테스트 「보내는 중 글 · 담당자 칸 잠김 → 응답 뒤(form 남음) 풀림 · 기준값 안 건드림」. `backend/tests/day/web/test_board_page_chart_controller.py` — day.js 에 잠금 → trigger 순서 · 응답 뒤 풀기 · readOnly/disabled 단정.

## 검증
- 화면 pytest(chart_controller · charts · chart_photos · architecture/test_screen_copy) → 11 passed
- `npm --prefix scripts/frontend run -s check`(CSS 재현 · ESLint · Stylelint · Prettier · node) → 118 pass · 0 fail
- `cd backend && uv run ruff check day tests` → All checks passed · `uv run mypy` → no issues(584 files)

## 손대지 않음
- backend 서비스 · policies · README(W6 의 README:197-198 문장은 backend 몫 — 이번 지정은 SKILL.md:130 만)
