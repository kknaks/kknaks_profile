# [frontend] fix-1 — ruff · mypy

코디 확인(2026-11-24): `cd backend && uv run ruff check day tests` → 21 errors, 전부 네 파일이다.
- tests/architecture/test_screen_copy.py 1
- tests/day/web/board_page_fixtures.py 1
- test_board_page_chart_controller.py 8
- test_board_page_chart_photos.py 6
- test_board_page_charts.py 5

E501 등이다. backend 보고에 따르면 mypy 오류 21건도 `tests/day/web/test_board_page_chart_controller.py` 에서만 난다.

할 것: 네 파일만 고친다. 아래 셋이 0 이 되면 된다.
- `uv run ruff check day tests`
- 레포 기준 mypy 명령(AGENTS.md)
- 네 화면 pytest 재실행 1회

backend 파일은 건드리지 마라. 커밋하지 마라. 보고는 preamble 의 worker_done 두 채널로 하고, 수치를 넣는다.
