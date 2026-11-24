# [backend] 고침 1 — 코드 검수 W-2 · W-3 · W-5
읽을 것: `/Users/kknaks/orca/workspaces/kknaks_profile/day-ext/orchestration/work/day-reservation/review-code-1-report.md` W-2 · W-3 · W-5 · 원 브리프 `/Users/kknaks/orca/workspaces/kknaks_profile/day-ext/orchestration/work/day-reservation/day-reservation-be-brief.md`(§5 · §8 · §9 그대로) · 작업 워크트리 `/Users/kknaks/orca/workspaces/CENTURION_DAY/day-reservation`(frontend 도 같은 트리에서 고침 중 — 서로 미커밋 변경 지우지 마라)
1. W-2 — request_refresh 를 메모리 broker 로 한 번 불러 task 이름 `day.sync_reservation_date_hospital` · args 가 들어갔는지 단언 + kiq 실패 로그 하나 시험
2. W-3 — [fetch] 실패 케이스를 transaction 안 실패로 바꾸거나 rollback 을 증명하는 다른 경우로 · timeout 되돌림 시험 · A1 에 카드 · 작업 저장 단언
3. W-5 — parse_day 가 다룰 수 없는 날짜(date.min · date.max 근처 넘침)를 400 invalid_request 로 · 시험 하나
4. W-4(오늘 회차와 같은 행 경합)는 **고치지 마라** — 사용자 판단으로 올린다. 다만 be 리포트에 「행 경합이 실제로 날 조건 · 대안 2개(예: 날짜 tx 를 짧게 / 같은 고객 행은 오늘 잠금 뒤로)」를 한 단락으로 적어라
5. §8 검증(네가 만든 · 고친 테스트 + tests/day/emr) · 리포트 `/Users/kknaks/orca/workspaces/kknaks_profile/day-ext/orchestration/work/day-reservation/be-fix-1-report.md` · 완료 보고는 preamble 의 worker_done
