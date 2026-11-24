# [frontend] 고침 2 — 사용자 결정 6(화면 쪽)
읽을 것: `/Users/kknaks/orca/workspaces/kknaks_profile/day-ext/orchestration/work/day-reservation/contract-v1-addendum.md` 6 · 원 브리프 `/Users/kknaks/orca/workspaces/kknaks_profile/day-ext/orchestration/work/day-reservation/day-reservation-fe-brief.md`(§5 · §8 · §9) · 워크트리 `/Users/kknaks/orca/workspaces/CENTURION_DAY/day-reservation`(backend 도 같은 트리 — 서로 미커밋 변경 지우지 마라)
1. 꺾쇠 · [오늘] · 달력 연타 = 날짜 바꾸기를 짧게 늦춰(debounce · 값 한 곳) 마지막으로 멈춘 날짜만 GET(중간 날짜 요청 0). 화면 머리 날짜 글자는 누를 때 바로 바뀌어도 된다(시안 동작 기준). 고침 1 의 순서 판정과 같이 동작
2. 시험(연타 N번 → 요청 1번 · 마지막 날짜) · §8 검증 · 리포트 `/Users/kknaks/orca/workspaces/kknaks_profile/day-ext/orchestration/work/day-reservation/fe-fix-2-report.md` · preamble 의 worker_done
