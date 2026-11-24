# [backend] 고침 2 — 사용자 결정 4 · 5 · 6(서버 쪽)
읽을 것: `/Users/kknaks/orca/workspaces/kknaks_profile/day-ext/orchestration/work/day-reservation/contract-v1-addendum.md` 4 ~ 6 · 네 리포트 `/Users/kknaks/orca/workspaces/kknaks_profile/day-ext/orchestration/work/day-reservation/be-fix-1-report.md` W-4 · 원 브리프 `/Users/kknaks/orca/workspaces/kknaks_profile/day-ext/orchestration/work/day-reservation/day-reservation-be-brief.md`(§5 · §8 · §9) · 워크트리 `/Users/kknaks/orca/workspaces/CENTURION_DAY/day-reservation`(frontend 도 같은 트리 — 서로 미커밋 변경 지우지 마라)
1. 4 — 날짜 쪽 양보(lock_timeout · 정렬 순서) + 시험(행을 다른 transaction 이 쥐고 있으면 날짜 쪽 error · 0행 · 오늘 쪽은 기다리지 않음)
2. ~~5 — 서버 시작 때 시드~~ → addendum 9: 데이터 migration(모든 job_role 에 reservation view · ON CONFLICT DO NOTHING · downgrade) + 왕복 시험
3. ~~6 — 병원당 동시 1개~~ → addendum 8: 잠금 전에 Redis 10초 캐시(있으면 task · 잠금 안 함 · 시작 때 세움 · 실패면 지움) + 시험
4. §8 검증(네 테스트 + tests/day/emr) · 리포트 `/Users/kknaks/orca/workspaces/kknaks_profile/day-ext/orchestration/work/day-reservation/be-fix-2-report.md` · preamble 의 worker_done
