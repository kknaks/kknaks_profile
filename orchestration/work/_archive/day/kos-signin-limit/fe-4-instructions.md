# [frontend] fe-4 — 차트 영역 호버 회색 배경 없애기 (아주 작은 판)

너는 앞 맥락이 없다. 원 브리프 `/Users/kknaks/orca/workspaces/kknaks_profile/day-fix-feedback/orchestration/work/kos-signin-limit/kos-signin-limit-fe-brief.md`(역할 · 검증 · 완료 보고)를 따른다. 앞 판 `fe-2-report.md`(같은 폴더 — 차트 영역 `ui.chart_hit`). 워크트리 `/Users/kknaks/orca/workspaces/CENTURION_DAY/kos-signin-limit`(혼자 · 미커밋 위). 커밋 금지.

사용자 2026-11-17(스크린샷): 시술명 영역(fe-2 `chart_hit` — 이름 + 「김태우 준비중」 줄)에 호버하면 뒤에 **회색 상자**가 깔려 신경 쓰인다 → **투명하게**.
- 마우스 호버 · 누름: 회색 배경 없음. 툴팁 「차트 작성」 · `cursor: pointer` 는 유지.
- 줄 전체의 옅은 파란 배경(선택된 카드 줄 표시 — 원래 있던 것)은 건드리지 않는다.
- 키보드 포커스 표시도 없음(사용자 정정 — 호버 툴팁이면 충분 · 배경 · 테두리 모두 없음).
- 「원장 변경」 버튼의 회색 호버는 그대로.
- 판 줄 · 시술 완료 탭 줄 모두.
- allowed_paths: `backend/day/styles/app.css` · `backend/day/static/day.css`(빌드) · `backend/day/templates/ui.html`(클래스만 필요하면) · `backend/tests/day/web/`.
- 검증: CSS 빌드 1회 · 화면 pytest 1회 · 기존 토큰만 · style= 0. 리포트 `…/kos-signin-limit/fe-4-report.md`(짧게). 완료 보고는 preamble 의 worker_done.
