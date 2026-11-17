# fe-4 리포트 — 차트 영역 호버 · 포커스 배경/테두리 없앰

## 변경
- `backend/day/styles/app.css`
  - `.day-linkrow:hover` → `.day-linkrow:hover:not(.day-proc__hit)` — 시술 완료 탭 줄(차트 영역)은 호버 회색 없음.
  - `.day-proc__hit` = `cursor: pointer` 만(배경 · 테두리 없음). 판 줄 영역 호버 · 누름 배경 없음.
  - 키보드 포커스 표시 없음(사용자 정정): `.day-proc__hit:has(:focus-visible)` 링 삭제 · `.day-proc__chart:focus-visible { outline: 0 }`(전역 `:focus-visible` 링 끔).
  - 「원장 변경」 `.day-proc__doc:hover` 회색(gray-200) 그대로 · 선택 줄 파란 배경 손대지 않음 · 툴팁 「차트 작성」(ui.chart_hit) 그대로.
- `backend/day/static/day.css` — 빌드 결과.
- `backend/day/templates/ui.html` — chart_hit 주석만(클래스 변경 없음).
- `backend/tests/day/web/test_board_page.py` — `test_차트_영역은_호버_포커스_배경_테두리_없음`(중복 워커가 만든 `…키보드_포커스만_링` 을 이 이름으로 바꾸고 지시서에 맞춤 · CSS 주석을 걷고 파싱하도록 고침).

## 검증
- `scripts/build-css.sh` 통과(day.css 56.5KB).
- `uv run pytest -q backend/tests/day/web` → 123 passed.
- ruff 통과 · ui.html `style=` 0 · 새 토큰 없음(기존 `--ms-gray-100` · `--ms-gray-200` 만).

## 주의
- 중복 발주된 워커가 같은 파일을 동시에 고쳤다. 코디네이터가 그 워커를 멈췄고, 최종 상태는 위와 같다.
