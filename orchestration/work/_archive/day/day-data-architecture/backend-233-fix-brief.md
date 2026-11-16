# [backend] #233 코드 검수 반영 — H1 · H2 · M1 · M2
같은 워크트리 · 미커밋 이어서 · 커밋 금지 · **사용자 day-local(11040 ~ 11043) 내리지 마라.** 읽을 것: `/Users/kknaks/orca/workspaces/kknaks_profile/day/orchestration/work/day-data-architecture/review-233-code-report.md` 전부.
실제 DB 조건(day.json infra): 공개 꺼짐 · VM 경유 · **TLS verify-full** · 앱 계정 = 스키마 주인 · migration 도 앱 계정.
- **H1(필수)** asyncpg 0.32 에서 verify-full 이 실제로 되게 — 리뷰어 방향(`ssl=verify-full` + 시스템 CA 번들 경로 명시 · 시작 때 검사). **실물 확인**: 사용자 로컬 `ssh -N day-db` 터널(127.0.0.1:15432) + `~/.pg_service.conf [day-dev]` 의 host · `~/.pgpass` 의 day_dev_app 줄로 asyncpg verify-full 연결 1회(SELECT 1 · current_schema) — **비밀번호를 출력 · 파일 · 리포트에 쓰지 마라**(읽어서 메모리로만). 쓰기 금지 · migration 금지.
- **H2** env 만들기 실패 시 두 판 전 이미지로 내려가지 않게(리뷰어 방향).
- **M1** prod 배포가 dev 배포 성공 이력 · digest 같음을 확인(실패한 dev 이미지는 prod 불가).
- **M2** 같은 concurrency group 대기 실행이 취소되지 않게(리뷰어 방향).
- 리뷰어가 짚은 정본 문서 차이(ssl 파라미터 · OIDC subject · KV 비밀 이름)는 리포트에 목록으로 — 문서는 고치지 마라(planner 몫).
검증: `uv run pytest -m "not infra" -q` · `scripts/test.sh -q` · ruff · shellcheck · actionlint · dry-run. 리포트 `/Users/kknaks/orca/workspaces/kknaks_profile/day/orchestration/work/day-data-architecture/backend-233-fix-report.md`. 완료는 preamble 의 worker_done 절차대로(둘 다).
