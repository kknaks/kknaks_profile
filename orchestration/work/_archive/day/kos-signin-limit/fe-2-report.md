# fe-2 리포트 — 차트 여는 영역 = 시술명 영역 전체 · 검수 W-1

워크트리 `/Users/kknaks/orca/workspaces/CENTURION_DAY/kos-signin-limit` (미커밋 · 커밋 안 함)

## 변경 파일
- `backend/day/templates/ui.html` — 새 매크로 `chart_hit(url, cls)`(영역 속성: `day-proc__hit` · `data-tip="차트 작성"` · `data-day-row-get`). `chart_name` 은 영역 안 키보드 포커스 자리로(같은 url · aria-label 「… 차트 작성」 · 자체 tip/`day-proc__doc` 제거). `proc_row` 미완료 줄 `span.day-proc__text`(1줄 이름 + 2줄 상태 줄) · 완료 줄 `span.day-proc__name`(이름 + 차트 아이콘)에 `chart_hit`. url 없으면(견본) 글자만 — 전처럼.
- `backend/day/templates/partials/board_parts.html` — `done_card` 의 `span.day-linkrow` 전체에 `chart_hit`. 주석 갱신.
- `backend/day/static/day.js` — data-day-row-get 처리: 영역 안의 다른 interactive(url 없는 버튼 등)를 누르면 열지 않음(`innerOwn`). 원장 변경 버튼은 팝오버 트리거라 원래 위에서 return(차트 안 열림). 헤더 주석 갱신.
- `backend/day/styles/app.css` + 빌드 `static/day.css` — `.day-proc__hit`(radius 4 · pointer · 호버/이름 버튼 focus-visible 때 `--ms-gray-200` · 원장 버튼 호버 중엔 영역 배경 끔), 판 줄은 margin -4/padding 4, `.day-proc__chart` 버튼 리셋. `span.day-linkrow:hover{background:none}` 삭제. 기존 토큰만.
- `backend/tests/day/web/test_board_page.py` — `test_차트는_시술_이름_글자만…` → `test_차트는_시술명_영역_전체가_열고_호버는_차트_작성`: 영역에 차트 url · 이름 버튼 같은 url · 상태 줄(meta) 영역 안 · 체크박스/⋮/hx-post 버튼 영역 밖 · 영역 밖엔 url 없음 · 원장 변경 버튼은 영역 안에서 팝오버 그대로(url 없음) · 완료 탭 linkrow 영역 · day.js innerOwn 가드.
- `backend/tests/day/web/test_login_device.py:81` — W-1 `raising=False` 제거.

## 검증
- `uv run pytest -q backend/tests/day/web -m "not infra"` → 122 passed
- `uv run pytest -q backend/tests/architecture` → 31 passed
- `scripts/build-css.sh` → day.css 56.7KB 빌드
- `node --check backend/day/static/day.js` OK
- 추가 줄 grep `<script|style=|onclick` → 0
- `uv run ruff check backend/tests/day/web` → 통과

## 주의 · E2E 에서 볼 자리
- 키보드: Tab 은 영역 안 이름 버튼에 멈춤 → Enter 로 차트, 포커스 시 영역 전체 배경 + 툴팁(focusin closest data-tip = 영역). 영역 자체는 tabindex 없음(버튼 안 버튼 중첩 회피).
- 원장 변경 버튼 호버 시 툴팁은 「원장 변경」(가장 가까운 data-tip), 영역 배경은 꺼짐(`:has(.day-proc__doc:hover)`).
- 판 다시 받은 직후(is-day-settling) 막음은 그대로.
- kit_page(견본)는 chart_url 없음 → 변화 없음.
