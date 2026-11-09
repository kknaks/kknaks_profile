# [backend] KOS 주소를 레포 env 에서 빼고 Key Vault 로
같은 워크트리 `/Users/kknaks/orca/workspaces/CENTURION_DAY/day-data-architecture` · 937dbb68 이후 · 커밋 금지 · day-local 내리지 마라.
사용자 결정(2026-11-09): **KOS 주소 3개(`KOS_OPEN_API_BASE` · `KOS_INTERNAL_API_BASE` · `KOS_WEB_BASE`)는 레포에 두지 않는다.**
- **전수조사**: `git grep -n "kos-solution"` 과 세 이름을 쓰는 곳 전부(지금 확인: `deploy/config/dev.env` · `prod.env` · `deploy/local.env.example` — 그 밖 문서 · 테스트 · 리포트 예시 · 코드 기본값도 grep 으로 다시 세라). 레포 어디에도 실제 주소가 남지 않게.
- 서버: Key Vault 비밀 `day-<env>-kos-open-api-base` · `-kos-internal-api-base` · `-kos-web-base` → 같은 env 이름으로(기존 KV → env 경로 · dry-run 가림 · 없으면 배포 중지 규칙 그대로). 문서 `docs/development/deployment.md` KV 표 갱신(주소 값은 쓰지 마라).
- 로컬: `local.env.example` 은 이름만(값 빈칸 · 「사용자에게 받는다」). 사용자 `deploy/local.env`(gitignore)는 건드리지 마라.
- 설정 누락 시 동작은 기존 규칙대로(배포 환경 필수면 시작 거부).
검증: `uv run pytest -m "not infra" -q` · `scripts/test.sh -q` · ruff · shellcheck · actionlint · dry-run · 최종 `git grep -n "kos-solution"` 0건. 리포트 `/Users/kknaks/orca/workspaces/kknaks_profile/day/orchestration/work/day-data-architecture/backend-233-kos-kv-report.md`. 완료는 preamble 의 worker_done 절차대로(둘 다).
