# 흔들림·기준선 판정 — strong-hajin-polish2 (WORK-009)

| 테스트 | 증상 | 판정 | 근거 |
|---|---|---|---|
| FE `CreateWork` 시작일 4 · `CreateWorkLayout` 1 | 직렬 전체 실행에서 실패 | **기준선**(날짜 의존 — 10월이라 9월 칸 없음) | 착수 전(`3d47a32`) 5 실패 동일 · 1차 `flaky-baseline-evidence.md` · 회고 §7 |
| FE `ActionCenter` 1 · `Checklist` 1 | 전체 실행에서 한 번씩 실패 | 흔들림 | 단독 3회 통과(워커 보고) · 이후 전체 실행 재현 안 됨 |
| BE `test-contract` 직렬 1 | reviewer 실행에서 1 failed | 흔들림(이름 미상) | `--lf` 재실행 통과 · 워커 두 번 128 passed |
| BE `test-postgres` `test_postgres_material_worker_recovery::test_heartbeat_keeps_one_postgres_owner_and_one_published_result` | 전체 실행 1 failed / 104 passed | 흔들림(하트비트 시간창) | 단독 2회 통과(코디 2026-10-02) · 이 판 변경에 material 워커 파일 0 |
