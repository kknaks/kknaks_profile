# fe-loop2 결과 보고 — e2e 1회차 피드백 C28 · C29 · C30
## 상태: done (커밋 안 함 · backend 파일 손대지 않음)

## 수행
- C28 여러 장 — `partials/board_photos.html` 파일 칸에 `multiple`. htmx 가 고른 파일 전부를 같은 이름 `file` 로 한 multipart 요청에 싣는다(htmx 2 는 `input.files` 를 배열로 넣음 — 확인).
- C29 토스트 — 화면 쪽 막힘 없음 확인: 409 `chart_conflict` = `board_chart_tab.html` 이 `message` 있으면 토스트 · 그 밖 거절(409 `chart_staff_required` · `staff_not_listed` · `doctor_not_listed` · 400) = `board_toast_error.html`(`message` 있으면 토스트 · X-Day-Error 응답을 day.js 가 끼움 · 차트 beforeSwap 은 conflict 가 아니면 손대지 않음). 빈 값일 때만 안 그리므로 서버가 C29 글자를 넣으면 뜬다. 코드 변경 없음 · 테스트로 고정.
- C30 사진 탭 — `static/day.js`
  - 탭을 고를 때마다 `day:photos-load`(이전: 비어 있을 때만) · 사진 자리 `hx-sync="this:replace"`(읽기끼리 겹치면 새 것만)
  - 보이는 동안 10초마다 `GET …/photos?tick=1`(SPEC 이름 `tick=1` · htmx.ajax · 같은 자리 innerHTML) — `runtime.defer` 한 타이머(자리마다 1개)
  - 멈춤: 다른 탭 고르면 `runtime.cancel` · 창 닫힘 / 패널 숨김 / 자리 사라짐이면 다음 회차에서 끝(타이머 0)
  - 겹침 없음: 자리 안에 `.htmx-request`(올리기 · 삭제 · 다시 시도 · 읽기) 있거나 삭제 확인 창이 열려 있으면 그 회차 건너뜀
  - 실패 자리: 목록이 없을 때만 보임 — 다시 읽기 · 10초 확인 실패면 있던 목록 그대로
- 테스트: `scripts/frontend/tests/photos-tick.test.mjs` 새로(10초마다 tick=1 · 진행 중이면 그 회차만 건너뜀 · 안 보이면 멈추고 타이머 0 · 자리 사라지면 해제) · `backend/tests/day/web/test_board_page_chart_photos.py`(multiple · 고를 때마다 읽기 · tick · 건너뜀 조건 · hx-sync) · `test_board_page_charts.py`(C29 세 글자 토스트 렌더)

## 검증
- 화면 pytest(chart_photos · chart_controller · charts · architecture/test_screen_copy) → 17 passed
- `npm --prefix scripts/frontend run -s check` → 122 pass · 0 fail(CSS 재현 · ESLint · Stylelint · Prettier)
- ruff check → All checks passed · format --check → 534 formatted
- 실행 못 함: 브라우저 실물(여러 장 · 10초 확인 · 토스트)

## 참고
- 10초 확인은 탭을 연 PC 마다 KOS 호출(planner-fix-10 메모 · 같은 방문 잠금은 서버)
