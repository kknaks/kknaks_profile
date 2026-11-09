# [researcher · 읽기 전용] DAY 서버 배포 방법 논의 자료 — centurion 배포 방식 조사 + DAY 에 대입

너는 day researcher 다. 역할 문서 `/Users/kknaks/orca/workspaces/kknaks_profile/day/orchestration/roles/day/researcher/`. **읽기 전용** — 리포트 1개만. 클라우드 · 서버에 접속하지 마라(문서 · 코드만).

## 배경
사용자(2026-11-08): 새 기능 전에 **DAY 서버 배포 방법**을 논의하자. 이미 정한 것: `/Users/kknaks/orca/workspaces/kknaks_profile/day/reference/2026-11-03-cc-day/system/README.md` 「서버」 · 「기본값」(Azure VM 2코어/4GB · 관리형 PostgreSQL 1대 · DB 1개 · 스키마 `DB_SCHEMA`(day_dev/day_prod) · Blob · caddy · api/worker/scheduler/redis · env → 나중에 Key Vault · JSON 로그) · `/Users/kknaks/orca/workspaces/mediness-mediness/day-data-architecture-spec/products/day/40-architecture/system.md`.
DAY 코드: `/Users/kknaks/orca/workspaces/CENTURION_DAY/day-data-architecture`(`deploy/compose.local.yaml` · `Dockerfile` · env 이름들 · migrate).

## 조사할 것 (centurion — 같은 회사 · 같은 Azure · 모양을 맞출 본)
`git -C /Users/kknaks/git/centurion show origin/main:<경로>`:
- `.github/workflows/deploy-stg.yaml` · `deploy-prod.yaml` — 무엇이 트리거 · 이미지 빌드 · 레지스트리(ACR?) · VM 에 어떻게 올리나(ssh · compose pull?) · migration 시점 · 승인 · 비밀값 출처
- `deploy/compose.yaml` · `compose.caddy.yaml` · `Caddyfile` · `config/{stg,prod}.env` · `environment-manifest.json` · `compose.env.example`
- `docs/guides/01-code-deploy.md` · `docs/migration/*deployment*` · `caddy-https-runbook.md` · `prod-cicd-runbook.md` · `infrastructure-deployment-runbook.md`

## 리포트
`/Users/kknaks/orca/workspaces/kknaks_profile/day/orchestration/work/day-data-architecture/researcher-deploy-report.md`:
1. centurion 배포 흐름 한 장(그림 + 단계) — 근거 파일:줄.
2. DAY 에 그대로 쓸 수 있는 것 / 바꿔야 하는 것(DAY 는 VM 하나 · 스키마로 dev/prod · redis 같이 · worker/scheduler · KOS 연결) 표.
3. **사용자가 정해야 할 것** 목록 — 선택지 + 근거 + 추천(예: dev/prod 를 VM 하나에 같이 vs 따로 · 레지스트리 · 배포 트리거(브랜치 · 태그 · 수동) · migration 누가 언제 · 비밀값 자리 · 도메인 · HTTPS · 로그 · 백업 · 롤백 · 운영 KOS 쓰기 열기 `KOS_TRIAL_WRITES_ON_LIVE` 시점).
4. 확인 못 한 것.
완료는 preamble 의 worker_done 절차대로(둘 다).
