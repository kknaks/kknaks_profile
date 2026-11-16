# backend 2판 수정 1 — code r2 W-2 · W-3

리포트: `/Users/kknaks/orca/workspaces/kknaks_profile/kos-병원데이터/orchestration/work/agency-settlement/review-code-r2-report.md` W-2 · W-3 을 읽어라.
1. **W-2** — 증분 ② 범위를 SPEC §4.5 글자대로(옛 itemsMissing 수납도 증분에서 다시 찾음 · #26 과 충돌 없음 — 리포트 근거). 시험 1
2. **W-3** — uvicorn access log 에 쿼리(`agency=<에이전시 이름>` 등)가 찍히지 않게(경로만 · 또는 access log 끔 + 우리 로그 한 줄). README 실행 명령 맞춤. 시험 또는 확인 방법 1
- W-1(「바뀜」)은 코드 그대로 둔다(SPEC 을 고침)
- ⚠ 8800 서버(코디가 띄움 · 사용자가 보는 중)는 건드리지 마라. `back/data/` · `back/.env` 읽기 · 쓰기 금지. 시험은 임시 DB
- 검증 `uv run ruff check . && uv run pytest -q` · 끝나면 원 브리프 §9 두 채널(같은 task/dispatch · subject 「backend 2판 수정 1 완료」)
