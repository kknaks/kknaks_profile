# fe-photo-1 결과 보고 — 사진 탭을 WP② 서버(SPEC 4d9214af · C22 · C23 · C24)에 맞춤
## 상태: done (커밋 안 함 · backend 파일 손대지 않음)

## 조각 값(계약 보충 3 — 코디 확인 · backend 전달됨)
photos = {visit_id, edit, reread, groups: [{category: before|after, title, items: [{photo_id, shot_at, kos_synced}]}]} · 선택 message(200 인데 KOS 실패 토스트 — 빈 값이면 안 그림)

## 수행
- `partials/board_photos.html` 다시 씀 — 썸네일 · 원본 = `GET /board/visits/{v}/photos/{photo_id}/file`(data: · 서명 주소 없음 · C22-기본값 ②) · 삭제 `…/{photo_id}/delete` · `kos_synced` 아니면 `is-unsynced` + 「KOS 미반영」 아이콘(E65 · 글자 OQ-88 비움) + edit 면 [다시 시도] `…/{photo_id}/kos-retry` · 올리기 `accept="image/jpeg,image/png"`(C24-기본값) · 성공은 모두 같은 조각을 `#chart-photos-{v}` innerHTML · `reread` 면 `hx-get …?poll=1` `load delay:5s` 한 번(C23 · OQ-97 기본값 — 작업 안 넣음 · JS 없음) · message 토스트 자리 · aria-label 없음(OQ-88)
- `partials/board_chart_parts.html` — 사진 탭 패널에 실패 자리 `.day-photos__failed[data-day-photos-failed]`(경고 아이콘만 · role=alert · 처음 hidden) · 조각 요청 timeout 15초(서버 3초 기다림 포함)
- `static/day.js` — `photosLoaded`(htmx:afterRequest · 사진 자리 GET 만): 못 받으면(5xx · 404 · 연결 · 시간 초과 · 토스트만 온 4xx) 실패 자리 보임 · 받으면 감춤. 탭을 다시 고르면 자리가 비어 있으니 다시 읽는다(기존 day:tab 처리)
- `icons.html` — lucide `rotate-cw`(다시 시도 아이콘) · `styles/app.css` — 미반영 테두리(--ms-red) · 표시 · 다시 시도 버튼 · 실패 자리(토큰만) → `day.css` 빌드
- `backend/tests/day/web/test_board_page_chart_photos.py` — 새 모양 3개 테스트(DAY 파일 경로 · 미반영 + 다시 시도 · 보기 권한 · 다시 읽기 · message 토스트 · 실패 자리 · JPEG/PNG)

## 검증
- 화면 pytest(chart_photos · chart_controller · charts · architecture/test_screen_copy) → 13 passed
- `npm --prefix scripts/frontend run -s check` → 118 pass · 0 fail(CSS 재현 · ESLint · Stylelint · Prettier)
- `cd backend && uv run ruff check day tests` → All checks passed · `ruff format --check` → 515 already formatted · `uv run mypy` → no issues
- 인라인 script · style= 0
- 실행 못 함: 실물(사진 라우트 · 가져오기 작업은 backend 진행 중) · 브라우저 클릭

## 코디가 확인할 것
- 「KOS 미반영」 · [다시 시도] · 실패 자리는 아이콘만(글자 · aria OQ-88) — 사용자 확인
- 「KOS 삭제 안 됨」 표시(OQ-94)는 목록에서 빠지는 행이라 그리지 않음
- 원본 = 같은 파일 경로 새 창(OQ-87)
