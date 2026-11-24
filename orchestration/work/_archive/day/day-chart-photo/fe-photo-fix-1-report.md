# fe-photo-fix-1 결과 보고 — 결정 C26 · C27 (review-code-3 P6 · P3)
## 상태: done (커밋 안 함 · backend 파일 손대지 않음)

## 수행
- C26 사진 삭제 확인 창
  - `partials/board_chart_parts.html` 새 매크로 `photo_confirm` — E59(`discard_confirm`)와 같은 모양 · 같은 방식: 차트 창 안 `<dialog class="ms-modal day-modal day-modal--confirm" role="alertdialog" data-day-photo-confirm>` · 경고 아이콘 · 「사진을 삭제할까요?」 · [취소](black) [삭제](solid-red). edit 일 때만 그린다.
  - `partials/board_photos.html` — 삭제 ✕ 의 요청 트리거를 click → `day:photo-delete` 로(누름만으로는 요청 없음).
  - `static/day.js` — ✕ 누름 = 확인 창 열고 그 ✕ 기억 · [삭제] = 창 닫고 그 ✕ 에 `day:photo-delete`(요청 1) · [취소] = 창만 닫음(요청 0) · Esc = 그 창만 닫힘(차트 Esc 가드가 안쪽 창이 열려 있으면 비켜 서도록 `dialog[open]` 으로 넓힘).
- C27 토스트 — 템플릿은 그대로(`message` 가 있으면 `toast_oob(message, "error")` · 빈 값이면 없음). 글자는 서버가 준다(「KOS 반영에 실패했습니다」 — backend 몫). 템플릿 주석만 C27 로.
- `backend/tests/architecture/test_screen_copy.py` — 「사진을 삭제할까요?」 · 「삭제」 근거(C26) 추가(「취소」는 이미 있음).
- `backend/tests/day/web/test_board_page_chart_photos.py` — 테스트 2개 추가: ✕ = `hx-trigger="day:photo-delete"` · 확인 창 모양 · 글자 · 버튼 · 보기 권한이면 창 없음 · [취소] 경로에 htmx 호출 없음 · [삭제] 경로가 기억한 ✕ 에 트리거 / C27 message 토스트 · 빈 값 없음.

## 검증
- 화면 pytest(chart_photos · chart_controller · charts · architecture/test_screen_copy) → 15 passed
- `npm --prefix scripts/frontend run -s check` → 118 pass · 0 fail(CSS 재현 · ESLint · Stylelint · Prettier)
- ruff check → All checks passed · ruff format --check → 534 already formatted
- mypy → 2 errors 는 `backend/tests/day/board/test_board_photos.py:444`(backend 파일 · 무관)
- 실행 못 함: 브라우저 실제 클릭(확인 창 · Esc)
