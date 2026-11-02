# 기준선 실패 · 플레이크 판정 — strong-hajin-polish

| 언제 | 기준 | 판정 | 근거 |
|---|---|---|---|
| 2026-10-01 | 코드 `015bed2`(origin/main), FE vitest 1092 | **기존 실패 5 — 이번 작업과 무관(날짜 의존)** | CreateWork 「업무/요청 갈래의 시작일…」 4 + CreateWorkLayout 「요청 갈래에도 시작일이 서고…」 1. 오늘이 10월이라 테스트가 고르는 09-xx 달력 칸이 없다. Phase 1 FE 워커가 깨끗한 별도 worktree 에서 측정 |
| 2026-10-01 | Phase 1 변경 후 전체 직렬 실행 | **플레이크 1** | Checklist 「moves a step with the keyboard」 — 전체 1회차 1번 실패, 단독·전체 재실행 통과 |

- FE 테스트는 `npx vitest run --no-file-parallelism`(직렬)로 돈다 — 병렬 실행이 사용자 로컬 스택을 죽인 이력
| 2026-10-01 | Phase 3b 후 BE test-contract 직렬 | **플레이크 1** | `test_material_worker_recovery::test_long_parse_heartbeats_its_lease_so_a_second_worker_cannot_reclaim_it` — 3초 리스 창을 3.15초 sleep 으로 재는 실시간 테스트. 코디 실행에선 통과(128 passed), 워커 실행에선 1 실패. 이번 변경과 무관 |
| 2026-10-01 | Phase 3b 후 FE 전체 직렬 | **부하 플레이크** | 한 번 8 실패 → 바로 재실행 5(기준선)만. BE 테스트와 동시에 돈 부하로 판단 |
