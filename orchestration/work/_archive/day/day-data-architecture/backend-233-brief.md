# [backend] Delivery #233 — DAY 서버 배포(dev · prod 한 VM) 구현

너는 day backend 워커다. 워크트리 `/Users/kknaks/orca/workspaces/CENTURION_DAY/day-data-architecture` — PR #228 같은 브랜치에 이어서(마지막 커밋 `8f26612f` 이후 · 사용자 결정 PR 하나). 커밋 금지.
## SSOT
- 계약 = **Issue #233 contract v2** `gh issue view 233 -R MediSolveAIDev/CENTURION_DAY` · 검수 `/Users/kknaks/orca/workspaces/kknaks_profile/day/orchestration/work/day-data-architecture/review-delivery233-report.md` · `-v2-report.md`.
- 정본 = `/Users/kknaks/orca/workspaces/mediness-mediness/day-data-architecture-spec/products/day/40-architecture/deployment.md`(사용자 결정: 한 VM · DB 한 대 · Caddy · 브랜치 dev/prod · prod fast-forward · **ACR** · VM run-command · Key Vault env · migration dev 자동 / prod 승인 · 롤백 수동 실행 · 도메인 day-dev / day).
- 본(모양 · 고치지 마라): centurion `git -C /Users/kknaks/git/centurion show origin/main:<경로>` — `.github/workflows/deploy-stg.yaml` · `deploy-prod.yaml` · `scripts/infrastructure/manual-app-deploy.sh` · `check-prod-tls.sh` · `deploy/compose.yaml` · `compose.caddy.yaml` · `Caddyfile` · `environment-manifest.json` · 조사 `/Users/kknaks/orca/workspaces/kknaks_profile/day/orchestration/work/day-data-architecture/researcher-deploy-report.md`.
## 만들 것 (계약 「바뀌는 것」 그대로)
GitHub Actions(dev · prod · 롤백 · prod migration) · ACR 이미지(SHA 태그) · VM 배포 스크립트(run-command · Key Vault → env 파일 · compose up · 헬스 · TLS 확인 · 실패 시 복구) · compose project 셋(day-edge Caddy · day-dev · day-prod · redis 환경마다 · 메모리 상한) · Caddyfile 두 도메인 · JSON 로그(`app_env`) · 배포 env 에서 `APP_ENV` 필수 · 계약이 가져온 앞 검수 항목 · AGENTS.md 「v2-dev」 → dev · 배포 문서(사용자가 Azure · GitHub 에서 준비할 값 이름 목록 — 값은 짓지 마라: 리소스 그룹 · VM 이름 · ACR 이름 · Key Vault 이름은 변수로).
## 하지 말 것
Azure · GitHub 실제 리소스 만들기 · 비밀값 커밋 · 운영 KOS 쓰기 켜기 · 앱 기능 변경. **사용자 로컬 compose(11040 ~ 11043) 를 내리지 마라.**
## 검증
`uv run pytest -m "not infra"` · `scripts/test.sh -q` · ruff · actionlint(없으면 `uvx` · docker 로) · shellcheck · 스크립트 dry-run · **로컬에서 서버 모양 compose 로 dev · prod 두 벌 기동**(다른 포트 · project 이름 — 사용자 11040 대와 겹치지 않게 · 메모리 상한 걸린 채 health 200 · 끝나면 그 두 벌만 down) · JSON 로그 테스트. 실제 Azure 배포는 사용자 준비 · PR #228 머지 뒤.
리포트 `/Users/kknaks/orca/workspaces/kknaks_profile/day/orchestration/work/day-data-architecture/backend-233-report.md` — Acceptance 증거 · 사용자 준비 목록(Azure · GitHub · DNS · Key Vault 비밀 이름) · 첫 배포 절차. 완료는 preamble 의 worker_done 절차대로(둘 다).
