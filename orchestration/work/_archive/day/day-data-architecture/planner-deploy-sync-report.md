# planner-deploy-sync 결과 보고 — done (미커밋)

`products/day/40-architecture/deployment.md` · `README.md` 한 줄 · `log.md` 한 줄 · lint `--strict` 0 error. **비밀값 · IP · client id 없음**(grep 0).

| 항목 | 고친 곳 (구현 937dbb68 · 실제 Azure 기준) |
|---|---|
| ssl · CA | env 표 `DATABASE_URL` = `postgresql+asyncpg://…/day?ssl=verify-full`(asyncpg 이름 · `sslmode` · `sslrootcert` 거부) · 새 줄 `PGSSLROOTCERT=/etc/ssl/certs/ca-certificates.crt` · `DATABASE_TLS_REQUIRED=true` |
| KV 비밀 이름 | `day-<env>-database-url` · `day-<env>-redis-url`(호스트 `redis`) · `day-<env>-encryption-key` |
| OIDC subject | `repo:MediSolveAIDev/CENTURION_DAY:environment:dev` · `…:environment:prod` · 브랜치 제한은 Environment 배포 브랜치 규칙 |
| concurrency | 워크플로마다 group(`day-deploy-dev` · `day-deploy-prod` · `day-migrate-prod` · 롤백) + VM `flock -w` + run-command 충돌 재시도 |
| 승인 · dev 이력 | prod migration = `migrate-prod` · 확인 문자열 `migrate day_prod` · `prod` 브랜치 · Environment `prod` · dev 성공 이력(외부 HTTPS 까지)의 SHA · digest 일치 + dev DB revision = 이미지 head(→ 다음 dev migration 전에 prod 승격) · prod 배포도 dev 이력 SHA · digest 확인 · 롤백 입력 = `history.jsonl` 의 SHA · 미결 「승인 수단」 닫음 |
| 권한 | 배포 앱 `day-deployer` = AcrPush · ACR Reader · Virtual Machine Contributor · VM identity(system) = AcrPull · Key Vault Secrets User(실측 200) · 사용자 = KV Secrets Officer |
| KV · NSG | `kv-centurion-day-prod`(RBAC · **방화벽 = VM 서브넷만** · 로컬에서 넣을 땐 잠깐 IP 허용 또는 VM 에서) · NSG `nsg-vm-centurion-day-prod` 22 = 출처 한 곳만 · 80/443 = 인터넷 전체(사용자) |
| 준비 표 | 준비됨 = VM · 네트워크 · 공인 IP · 관리형 PG · Key Vault · ACR 권한 · 배포 계정 · OIDC credential / **남음 = GitHub Environments · Actions 변수 · Key Vault 비밀 6 · DNS A 레코드 둘** · (Docker · 로그 회전은 배포 스크립트 / VM 쪽) |
| 글귀 셋(review-deploy-db) | 머리말 「짓지 않는다 · 값 미정」 → 받은 이름은 적고 IP · 비밀 · 구독 · client id 는 안 적음 · env.py 문장 정밀화(없을 때만 만듦 · `IF NOT EXISTS` 는 offline) · README 줄 「서버 · DB · 권한 받음 · 배포 아직」 |
