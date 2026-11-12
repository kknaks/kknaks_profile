# fix-web fe-2 결과 보고 — 코드 리뷰(review-code-1) 반영 (frontend)

## 상태: done (infra 테스트는 fe-1 과 같은 사유로 pending)

## 수행
| 지적 | 파일 | 무엇 |
|---|---|---|
| F1 | `backend/day/templates/partials/board_parts.html` need_card | `why == "home"` 이면 머리 배지 = 「귀가대기」 글자만(경과 `n분째` 없음 · U-10). 나머지 3상황은 「상태 + n분째」 그대로. 매크로 주석에 반영 |
| F1 | `backend/tests/day/web/test_board_page.py` | 머리 정규식 끝을 `</span></span>`(배지 + 머리 닫힘)로 — home 은 `by_why["home"] == "귀가대기"`(정확 일치 = 경과 없음 확인) |
| W1 | `backend/day/static/day.js` 문서 click 맨 앞 | 고른 카드(`[data-day-card].is-selected`) · 인박스 카드 본문(`[data-day-goto]` — 아래 고르기가 맡음) · `.day-pop` · `dialog` · `#modal-root` 밖이면 `clearCards(document)`. **다른(흐린) 카드 위 클릭도 해제**. 이 해제는 return 하지 않으므로 다른 카드의 버튼 · 팝오버 트리거 동작은 그대로 이어진다. fe-1 의 뒤쪽 `else if` 분기는 삭제(중복). 인박스 탭 ←→ 키 해제 · OOB 복원 비충돌은 fe-1 그대로 |
| W2 | `backend/tests/architecture/test_screen_copy.py` | 근거 표에서 「현황」 · 「시작 가능」 · 「수락함」 · 「시술 대기」 삭제. 「시술 대기」 grep: 화면 글자 쓰임 없음(`routers/board.py:48` docstring · `kit_board.py:52` docstring · `board_regions.html:24` Jinja 주석 · `services/board_rules.py` 주석뿐 — 문구 검사는 주석 · docstring 제외). 「수락함」 · 「시작 가능」 · 「귀가 대기 전」은 지운 문구 목록에 남김 |
| W3 | `backend/tests/day/web/test_board_page.py` | `test_시술_줄_5상태와_버튼` 의 `[수락]` 단언을 `#inbox-call-list` ~ `#inbox-panel-done` 구간(수락 대기 탭)으로 좁힘 · `test_판_카드_호출_줄에는_재호출이_없다` 의 중복 `board = …` 줄 삭제 |

## 검증
- `uv run pytest -q backend/tests/day/web backend/tests/architecture` → **121 passed**
- `uv run pytest -q -m "not infra" backend/tests` → **930 passed, 318 deselected**
- `uv run ruff check backend` → All checks passed · `ruff format --check` OK · `node --check day.js` OK
- `scripts/build-css.sh` → `static/day.css` diff 는 fe-1 과 같음(메모 2값 + 해시)
- 추가 줄의 인라인 스크립트 · `style=` · `onclick` · `eval(` grep → 0
- pending: `scripts/test.sh`(infra) — 로컬 PostgreSQL 이 사용자 `day-local` 뿐이라 미실행

## 이슈
- 없음. W9 클릭 해제는 브라우저 수동 확인을 안 했다(사용자 포트 금지) — E2E 때 「흐린 카드의 [시작] · 더보기 누르면 동작 + 선택 해제」 확인 권장.
