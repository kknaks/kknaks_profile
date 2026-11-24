# fe-loop3 결과 보고 — e2e 2회차 F1 · F2 · 검수 4 W2 · W4 · W7 · C33
## 상태: done (커밋 안 함 · backend 파일 손대지 않음) — C33 글자만 대기

## 수행
- F2 · W2 — 10초 확인(`?tick=1`)과 5초 다시 읽기(`poll=1`)는 **사진 목록만** 바꾼다.
  - `board_photos.html`: 묶음마다 사진들을 `<div class="day-photos__list" data-day-photo-list="{category}">`(display: contents — 배치 그대로)로 감싸고 올리기 form 은 그 밖에 둔다.
  - `day.js` `photosListOnly`(htmx:beforeSwap): 그 두 요청이면 통째 바꾸기를 막고(shouldSwap=false) 응답에서 같은 category 목록만 골라 `replaceWith` + `htmx.process`. 올리기 form · 파일 칸은 갈아 끼우지 않는다.
  - 건너뜀에 파일 고르기 추가: 파일 칸 click → `_dayPhotoPicking` · change / cancel / 창 focus 복귀 → 풀림. 요청 중 · 삭제 확인 창 열림은 앞 판 그대로.
- W4 — `photosShown` 에 `!document.hidden` · 숨으면 다음 회차에서 멈춤(타이머 0) · `visibilitychange` 로 보이면 사진 탭이 보이는 창마다 바로 1회 확인 + 10초 다시 걸기.
- W7 — 쓰기(올리기 · 삭제 · 다시 시도) 요청 시작 · 끝마다 `_dayPhotosSeq` +1 · 확인을 보낼 때 그 값을 `_dayPhotosTickSeq` 로 기억 · 응답 때 다르면 버린다(지운 사진이 되살아나지 않음).
- F1 — `#day-toasts` 를 `popover="manual"`(top layer)로 · `raiseToasts()` = 토스트가 들어올 때 열린 `<dialog>` 가 있으면 hide → show 로 모달보다 위로(나중에 연 top layer 가 위) · 없으면 한 번 연다. CSS 는 기본 popover 상자 모양을 지우고 같은 자리(top 16 · 가운데). popover 를 모르는 브라우저는 지금처럼. 차트 · 사진 모달의 모든 토스트(OOB · SSE · 403/413 template)가 같은 길.
- C33 — `board.html` 에 `<template data-day-toast-on="413">` 자리(기존 403 과 같은 방식 · X-Day-Error 없는 4xx 를 day.js 가 띄움) · **글자 `TOAST_413 = ""` — 비어 있으면 template 을 그리지 않는다**(코디: 사용자 확인 중 · 받으면 그 한 줄만 채우면 됨).
- 고정본: `scripts/frontend/tests/fixtures/reservations-page.html` — base.html 의 popover 한 줄만 바뀜(DAY_UPDATE_FIXTURES=1 로 다시 씀).
- 테스트: `scripts/frontend/tests/photos-tick.test.mjs`(photosCheck 분리 반영 + 확인이 쓰기 번호를 기억 1건) · `backend/tests/day/web/test_board_page_chart_photos.py`(목록 자리 · form 밖 · 숨김 · 고르기 · 엇갈림 · popover · 413 자리 1건).

## 검증
- `scripts/test.sh -q backend/tests/architecture backend/tests/day/web` → 513 passed · 0 failed
- `npm --prefix scripts/frontend run -s check` → 123 pass · 0 fail(CSS 재현 · ESLint · Stylelint · Prettier)
- ruff All checks passed · format 536 · mypy no issues(606) · day.js `innerHTML` 0
- 실행 못 함(실물만 보임): 파일 고르기 창 15초 열고 고르기(e2e 체크 7) · 숨긴 탭 1분(체크 8) · 모달 위 토스트 층(F1) · 413(dev 서버)

## 대기
- C33 413 토스트 글자(OQ-88 · 사용자 확인 중) — `templates/board.html` `TOAST_413` 한 줄
