# [frontend] 기능 1 — 원내 현황 탭 화면

너는 이 작업의 frontend 다(앞 판 보고서 `fe-*-report.md` 가 이 폴더에 있다 — 먼저 읽어라). 결정 R46 ~ R48(`/Users/kknaks/orca/workspaces/kknaks_profile/day-ext/reference/2026-11-23-reservation/reservation-board-decisions.md` 끝 절) · 계약 `/Users/kknaks/orca/workspaces/kknaks_profile/day-ext/orchestration/work/day-reservation/contract-v2-inhouse.md` 이 정본. 생김새 · 문구 = 시안(`renderSide` L1804 · `stageCard` L1777 · CSS L440 ~ 475) — 시안에 없는 문구 짓지 마라.

할 일
1. 오른쪽 패널 탭 「공지 / 예약」 · 「원내 현황」(기본 = 공지 / 예약). 원내 현황 = 칩 줄(전체 · 접수 · 상담 · 시술 · 귀가 대기 · 가로 스크롤 시안대로) + 카드 목록 + 빈 상태.
2. 카드: 이름 · 수납 필요 / 수납 완료 배지 · 단계 배지(단계 색 토큰) · 접수 = 예약 일시 / 국적 · 그 뒤 = 상담 ○○ 실장 · 시술 대기부터 = 총 합계 · 수납 필요(빨강) · 수납 완료.
3. 칩 = 화면에서 `cat` 으로 거르고 `order_all` / `order_cat` 으로 정렬. 고른 탭 · 칩은 10초 폴링 · 날짜 이동 뒤에도 유지(기존 day.js 시계 한 개 · 인라인 스크립트 금지 · 손 CSS 금지 — 기존 규약).
4. backend 가 아직 `inhouse` 를 안 내도 계약 모양 픽스처로 node 시험(scripts/frontend/tests) · 화면 문구는 `tests/architecture/test_screen_copy.py` 에 시안 문구만 추가.
5. 관련 시험만.

backend 와 같은 워크트리 — **Python(routers / services / queries / policies / presentation / dtos) 은 backend 몫**. 계약 밖 필드가 필요하면 짓지 말고 ask.
금지: 스택 손대지 마라 · 커밋 · push 금지.
워크트리 `/Users/kknaks/orca/workspaces/CENTURION_DAY/day-reservation` · 리포트 `/Users/kknaks/orca/workspaces/kknaks_profile/day-ext/orchestration/work/day-reservation/fe-feat-1-report.md` · preamble 의 worker_done.
