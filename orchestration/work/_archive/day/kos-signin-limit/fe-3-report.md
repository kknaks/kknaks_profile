# fe-3 리포트 — 정렬 탭 글자

사용자 2026-11-17: `/board` 정렬 탭 「시술순」→「시술대기 순」 · 「방별순」→「방별 순」. 쿼리 값(`sort=room`) · 내부 이름 그대로. 커밋 안 함.

## 변경 파일
- `backend/day/templates/partials/board_main.html` — 탭 글자 2개 + 템플릿 주석(이름 임시 → 사용자 2026-11-17)
- `backend/day/templates/partials/board_parts.html` — 템플릿 주석 1곳(방별 순)
- `backend/tests/architecture/test_screen_copy.py` — 근거 표 키 「시술대기 순」 · 「방별 순」(옛 키 제거)
- `backend/tests/day/web/test_board_page.py` — `test_정렬_탭은_머리_오른쪽_링크_GET_board_sort_room` 단언 · docstring

## 그대로 둔 것(코드 주석 · 선택)
- `routers/board.py` :13 · :164 · :298, `services/board.py` :403, `services/board_rules.py` :40 · :551, `styles/app.css` :449, `tests/day/board/test_board_feedback_rules.py`(테스트 이름 · 주석) — 사람에게 보이지 않는 주석 · 테스트 이름이라 손대지 않음(CSS 재빌드 불필요).
- aria-label 「정렬」 은 그대로.

## 검증
- `uv run pytest -q -m "not infra" backend/tests/day/web/test_board_page.py backend/tests/architecture/test_screen_copy.py` → 78 passed
- `uv run ruff check backend` → All checks passed
