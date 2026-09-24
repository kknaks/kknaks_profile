---
title: Tauri local profile calendar width fix report
status: complete
updated: 2026-09-23
---

# 변경

`frontend/src/styles/calendar.css`의 `.scax-month__cell`에 `align-items:stretch`를 추가했다. 월간 날짜 칸은 `<button>`으로 렌더링되므로 Tauri WebView의 button UA 기본값 `align-items:flex-start`가 기존 flex column에 적용되어 자식 `.scax-event`/EventBar가 내용 폭으로 줄어들 수 있었다. 이제 날짜 셀의 이벤트 자식은 셀의 내부 가로폭을 채우며, 웹 브라우저와 같은 정렬 규칙을 갖는다.

변경은 CSS 한 줄이며 운영 셸 설정, capability, Tauri 로컬 실행 스크립트는 수정하지 않았다.

# 검증

- `npx vitest run src/features/calendar/CalendarPage.test.tsx --reporter=dot`: 18 passed
- `npx tsc --noEmit`: 통과
- CSS 정적 확인: `.scax-month__cell` 선언에 `align-items:stretch` 존재
- 로컬 서버 `http://127.0.0.1:5176`: HTTP 200
- `node scripts/run-tauri-local.mjs`: 실제 macOS Tauri 창 실행 성공
- Tauri 로그: `url=http://127.0.0.1:5176/`, 허용 navigation, `page load finished` 확인
- Tauri 종료 후 임시 복제 트리 잔존 없음
- `git diff --check`: 통과

# 확인 범위와 한계

Tauri WebView에서 실제 로컬 페이지 로드와 셸 부팅을 확인했다. 이번 회차는 화면 자동화 도구를 사용한 픽셀 측정이 아니라 CSS 원인 수정과 캘린더 회귀 테스트, 실제 Tauri 창 로드 로그를 검증 근거로 삼았다. 14일 이벤트의 픽셀 폭은 별도 수동 화면 확인에서 `align-items:stretch`가 적용된 셀 내부 폭을 기준으로 재확인해야 한다.
