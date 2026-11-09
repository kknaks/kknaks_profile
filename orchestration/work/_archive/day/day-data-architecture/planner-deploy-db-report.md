# planner-deploy-db 결과 보고 — done (미커밋)

`products/day/40-architecture/deployment.md` · `log.md` 한 줄 · lint `--strict` 0 error. **IP · 비밀번호 없음**(grep 으로 IP 0건 확인).

- 머리말: 2026-11-09 서버 · DB 받음 · IP · 비밀번호는 안 적음(비밀번호는 사용자 `~/.pgpass`).
- 준비 표 제목 「(값 미정)」 삭제 · **준비됨(2026-11-09)**: VM `vm-centurion-day-prod`(B2s · Ubuntu 24.04 · 64GB · `azureuser` · 삭제 방지) · 네트워크 22/80/443 열림(22 = 운영자 SSH · 배포는 run-command — 22 를 닫을지는 사용자) · 공인 IP(값 안 적음) · 관리형 PG `pg-centurion-day-prod.postgres.database.azure.com`(16 · DB `day` · `day_dev` 주인 `day_dev_app` · `day_prod` 주인 `day_prod_app` · search_path 자기 스키마 · 서로 · `public` 쓰기 막힘 · `dayadmin` 초기 설정용 · **공개 꺼짐 · VM 경유 · TLS verify-full**).
- **아직 없음**: Docker · 로그 회전 · DNS A 레코드 둘 · Key Vault · ACR 권한 · OIDC 배포 계정 · VM identity.
- env 표 `DATABASE_URL` = dev `day_dev_app` · prod `day_prod_app` · DB `day` · 호스트 · `sslmode=verify-full` · VM 안에서만 닿음 · 비밀번호는 Key Vault(지금은 `~/.pgpass` 에만).
- 미결 「스키마 생성 권한」 **닫음** — 앱 계정이 스키마 주인 · migration 도 앱 계정 · 별도 migration 계정 없음 · 스키마가 이미 있어 `CREATE SCHEMA IF NOT EXISTS` 는 아무 일도 안 함(사용자 승인).
