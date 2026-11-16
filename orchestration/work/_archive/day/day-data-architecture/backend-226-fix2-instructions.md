# [backend] #226 재검수 반영(fix2) — N1 · N2 · N3

너는 #226 backend 워커다. 같은 워크트리 · 미커밋 그대로. 앞 브리프 규칙 그대로(KOS 쓰기 금지 · 비밀값 금지 · 커밋 금지 · 포트 11040 · 11042 · 11043 · 모델 · migration 변경 금지).
읽을 것: 재검수 리포트 `/Users/kknaks/orca/workspaces/kknaks_profile/day/orchestration/work/day-data-architecture/review-226-fix1-report.md` N1 ~ N3.

1. **N1** — 일정 조회 `zoneIds` 를 **응답에 있던 구역 id**(매핑 성공 여부와 무관)로. `emr/kos/__init__.py:94 · 135-141`. 구역 하나가 매핑에 실패해도 그 구역 오늘 방문이 사라짐 처리되지 않게. DB 없는 테스트 1.
2. **N2** — `needs_master` 발행 억제: Redis `SET … NX EX 300`(키는 병원별 · 설정값) 성공 때만 `sync_master_hospital.kiq`. DB 없는 테스트 「연속 두 번 needs_master → 발행 1번」.
3. **N3** — 태스크 단계 `needs_master → kiq` 발행 테스트(가짜 broker · DB 없이).

검증: `uv run pytest -m "not infra"` · compose `up -d --wait postgres redis` → `scripts/test.sh -q` · ruff 각 1회 · 끝나면 `down`. KOS 실물 호출 없음.
리포트 `/Users/kknaks/orca/workspaces/kknaks_profile/day/orchestration/work/day-data-architecture/backend-226-fix2-report.md` — N 별 고친 곳 · 수치. 완료는 preamble 의 worker_done 절차대로(둘 다).
