# [frontend] 고침 1 — 코드 검수 F-1 · W-1
읽을 것: `/Users/kknaks/orca/workspaces/kknaks_profile/day-ext/orchestration/work/day-reservation/review-code-1-report.md` F-1 · W-1 · 원 브리프 `/Users/kknaks/orca/workspaces/kknaks_profile/day-ext/orchestration/work/day-reservation/day-reservation-fe-brief.md`(§5 · §8 · §9 그대로) · 작업 워크트리 `/Users/kknaks/orca/workspaces/CENTURION_DAY/day-reservation`(backend 도 같은 트리에서 고침 중 — 서로 미커밋 변경 지우지 마라)
1. F-1 — 시안에 없는 aria-label 「예약 표」 제거(reservations_parts.html:85) + test_screen_copy 의 그 행 제거. 시안에 있는 다른 이름이 맞으면 그것으로 · 없으면 비움
2. W-1 — 폴링 응답과 날짜 바꾸기 응답 경쟁: 두 요청이 같은 대상에서 마지막 것만 살게(hx-sync 등 · 방법은 네가 · 이유 한 줄). 순서를 시험하는 화면 테스트 또는 day.js 단위 시험을 더한다(속성 문자열만 보지 말 것)
3. §8 검증(네 화면 테스트 · npm run check) · 리포트 `/Users/kknaks/orca/workspaces/kknaks_profile/day-ext/orchestration/work/day-reservation/fe-fix-1-report.md` · 완료 보고는 preamble 의 worker_done
