# [planner] 40-architecture 배포 문서 — DAY 서버 배포 구조 (dev · prod 한 VM)

너는 day planner 다. 워크트리 `/Users/kknaks/orca/workspaces/mediness-mediness/day-data-architecture-spec` · 미커밋 · 커밋 금지.
정본(사용자 결정): 원천 `/Users/kknaks/orca/workspaces/kknaks_profile/day/reference/2026-11-03-cc-day/system/README.md` 「배포 결정」 표 전부(2026-11-08) — 한 VM · DB 한 대 · Caddy · 브랜치 `dev`/`prod`(push → 그 환경 배포 · prod 는 dev 에서 확인한 같은 이미지) · 도메인 `day-dev.medisolveai.com` / `day.medisolveai.com` · DNS · Azure 권한 = 사용자 · 백업 기본 · 배포 시간 제한 없음 · 그 밖 조사 추천대로.
근거: 조사 `/Users/kknaks/orca/workspaces/kknaks_profile/day/orchestration/work/day-data-architecture/researcher-deploy-report.md`(centurion 흐름 · §2 대입 · §3 D1 ~ D15 · §4 확인 못 한 것) · 기존 `/Users/kknaks/orca/workspaces/mediness-mediness/day-data-architecture-spec/products/day/40-architecture/system.md` · `mobile-deployment.md`.

## 할 일
1. `products/day/40-architecture/deployment.md` 새로: 한 장 그림(Caddy · day-dev · day-prod · ACR · Key Vault · 관리형 PG 스키마 둘 · Blob) · 브랜치 → 배포 흐름(GitHub Actions · OIDC · ACR · VM run-command · Key Vault env · migration: dev 자동 / prod 승인 · 헬스 · TLS 확인 · 롤백 = 이전 이미지) · compose project 셋과 메모리 상한 · 환경별 env 표(이름만 — 값 없음) · `KOS_TRIAL_WRITES_ON_LIVE` prod 첫 배포 false · 사용자가 Azure 에서 준비할 것 목록(VM · VNet/NSG · Key Vault · ACR 권한 · OIDC · DNS A 레코드) · 미결(실측 메모리 · PG 백업 설정 · KOS IP 제한 · 스키마 생성 권한).
2. `system.md` 의 「배포는 나중」 줄들을 이 문서로 연결 · README 링크 · log.
3. 결정에 없는 값(VM 이름 · 리소스 그룹 · IP 등)은 짓지 말고 「사용자 준비 · 값 미정」.
lint `--strict`. 리포트 `/Users/kknaks/orca/workspaces/kknaks_profile/day/orchestration/work/day-data-architecture/planner-deploy-arch-report.md`. 완료는 preamble 의 worker_done 절차대로(둘 다).
