# [frontend] fe-2 — 작은 픽스 2건

너는 앞 맥락이 없다. 원 브리프 `/Users/kknaks/orca/workspaces/kknaks_profile/day-fix-feedback/orchestration/work/kos-signin-limit/kos-signin-limit-fe-brief.md`(역할 · 검증 · 완료 보고)를 따르되, **이번 allowed_paths 는 아래로 넓힌다**: `backend/day/templates/ui.html` · `backend/day/templates/partials/board_parts.html` · `backend/day/static/day.js` · `backend/day/styles/app.css` · `backend/day/static/day.css`(빌드) · `backend/tests/day/web/`. 작업 워크트리 `/Users/kknaks/orca/workspaces/CENTURION_DAY/kos-signin-limit`(미커밋 위에 · 혼자). 커밋 금지.

## 1. 차트 여는 영역 = 시술명 영역 전체 (사용자 2026-11-17 로컬 확인)
지금(fix-feedback E6) 차트는 시술 이름 글자(`ui.chart_name` 버튼)만 연다 — 글자가 작아 잘 안 눌린다. 사용자: 「체크박스 — [시술명 영역] — (버튼) [더보기] 중 **시술명 영역에는 다 차트 작성**」.
- 시술 줄의 텍스트 블록 전체(`span.day-proc__text` — 1줄 시술 이름 + 2줄 상태 줄 「김태우 준비중」 등, 빈 자리 포함)를 누르면 차트(`data-day-row-get` 같은 url) · 호버하면 툴팁 「차트 작성」 + 옅은 배경(지금 이름 버튼과 같은 모양을 영역에).
- **예외**: 2줄의 원장 이름이 「원장 변경」 버튼(`p.doctor_pop` — 수락 · 진행중)이면 그 글자는 원장 변경 그대로(차트 안 열림 · 클릭 전파 막음). 체크박스 · 줄 버튼(시작 · 완료 등) · ⋮ 는 차트 안 열림.
- 판 카드 줄(`ui.proc_row` — 완료 줄 · 미완료 줄)과 「시술 완료」 탭 줄(`board_parts.html` `done_card` 의 `day-linkrow`) 모두.
- 키보드 접근(포커스 · Enter) 유지 · 인라인 스크립트 0 · 손 CSS 는 기존 토큰만.
- 화면 테스트: 영역 전체에 차트 url · 원장 변경 버튼은 그대로 · 체크박스 · ⋮ 는 영역 밖.

## 2. 검수 W-1
`backend/tests/day/web/test_login_device.py:81` monkeypatch `raising=False` → 지워서(기본 True) 이름이 바뀌면 실패하게.

## 검증
- 원 브리프 §8(화면 pytest · CSS 빌드 · node --check · 인라인/style= 0 grep).
- 리포트 `/Users/kknaks/orca/workspaces/kknaks_profile/day-fix-feedback/orchestration/work/kos-signin-limit/fe-2-report.md`. 완료 보고는 preamble 의 worker_done.
