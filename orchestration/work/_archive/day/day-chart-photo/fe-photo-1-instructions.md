# [frontend] 사진 탭 — WP② 서버에 맞추기

## 먼저 읽을 것
- SPEC — `/Users/kknaks/orca/workspaces/mediness-mediness/day-chart-photo-spec/products/day/20-spec/spec-002-procedure-board.md`
  - U-16 · 규칙 39 · API · 매트릭스(최신 커밋)
- 결정 — `…/reference/2026-11-24-day-picture/chart-photo-decisions.md`
  - C22 · C23

**SPEC 이 바뀐 곳**
- 썸네일 · 원본은 DAY 경로에서 받는다(`data:` 아님).
- 「KOS 미반영」 표시와 [다시 시도]가 생겼다.
- 탭을 열면 가져오기 작업이 돌고, 화면은 다시 그린다(SPEC 이 정한 방식).

backend 가 같은 워크트리에서 WP② 를 병렬로 만든다.
- 조각 값 이름은 backend 와 맞춘다.
- 다르면 [질문].
- backend 파일은 건드리지 마라.

## 할 것
- `partials/board_photos.html` · `day.js` 를 위에 맞춘다.
- 글자는 SPEC · OQ 그대로 비운다.
- aria-label 은 OQ-88 — 비워 둔다.

## 검증
- 화면 pytest
- `npm run -s check`
- ruff

## 보고
- 커밋 금지
- 보고 파일 `fe-photo-1-report.md`
- preamble 의 worker_done 두 채널로 보고

## 추가 (코디 · 사용자 화면 확인 2026-11-24)
- 사진 조각을 못 받으면(서버 오류 · 404 · 네트워크) 탭이 빈 칸으로 남는다 → 실패 상태를 보이게(글자는 SPEC 에 있으면 그것 · 없으면 OQ 로 비우되 「실패 상태 영역」은 그린다) · 다시 열기로 재시도.
- 형식 = JPEG · PNG(C24-기본값) — 파일 고르기 `accept` 맞춤.
- SPEC 커밋 = mediness #960 `4d9214af`.
