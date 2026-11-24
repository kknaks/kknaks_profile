# fe-loop4 결과 보고 — C36 413 토스트 글자
## 상태: done (커밋 안 함 · backend 파일 손대지 않음)

## 수행
- `templates/board.html` — `TOAST_413` = 「한 번에 올릴 수 있는 용량(100MB)을 넘었습니다」(결정 C36). 글자가 생겨 `<template data-day-toast-on="413">` 가 그려지고, 앞단 413(X-Day-Error 없음)이면 day.js `htmx:responseError` 가 그 토스트를 `#day-toasts`(popover · 모달 위 top layer — 3루프 F1)에 띄운다.
- 빠진 장 토스트 — 확인만(코드 변경 없음): backend 가 `message` 로 「올리지 못한 사진이 있습니다 (JPEG · PNG, 5MB 이하만)」를 주면 `board_photos.html` 끝 `toast_oob(message, "error")` 로 그려진다(빈 값이면 없음). 테스트로 고정.
- `backend/tests/architecture/test_screen_copy.py` — 413 글자 근거(C36) 추가.
- `backend/tests/day/web/test_board_page_chart_photos.py` — 413 글자 단정 · 빠진 장 message 토스트 렌더 1건.

## 검증
- `scripts/test.sh -q backend/tests/architecture backend/tests/day/web` → 514 passed · 0 failed
- `npm --prefix scripts/frontend run -s check` → 123 pass · 0 fail
- ruff All checks passed · format clean
- 실행 못 함: dev 서버 413 실물(5MB 가까운 사진 여러 장)
