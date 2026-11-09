# planner-deploy-arch 결과 보고 — done (미커밋)

## 수행

| 파일 | 변경 |
|---|---|
| `products/day/40-architecture/deployment.md` | **새로**(id `DAY-DEPLOYMENT` · type architecture · draft) |
| `products/day/40-architecture/system.md` | 「배포는 DAY 전용 Azure 서버(나중)」 → deployment.md 연결 · 「서버 env → 나중에 Key Vault」 → Key Vault + Git config(deployment.md) · 토폴로지 VM 노드 「예정」 → 「dev · prod 같이」 |
| `products/day/40-architecture/README.md` | 진입 목록에 deployment.md |
| `products/day/log.md` | 2026-11-08 `arch-change` 한 줄 |

lint `--strict` → 0 error · products/day 경고 0.

## deployment.md 절

1. **결정 요약** — 원천 system 「배포 결정」 표 전부(한 VM · PG 한 대 스키마 둘 · 브랜치 dev / prod · 도메인 · Caddy · 백업 기본 · 시간 제한 없음 · Azure 권한 = 사용자 · 그 밖 조사 추천).
2. **한 장 그림**(mermaid) — Caddy(`day-edge`) · `day-dev` · `day-prod`(각 api · worker · scheduler · redis) · ACR · Key Vault · 관리형 PG(스키마 둘) · Blob · GitHub Actions.
3. **브랜치 → 배포 흐름**(sequence + 표) — dev push = 빌드 · ACR push(태그 SHA) · run-command · Key Vault env · migration 자동 · up · 헬스(`/health/live` · `/health/ready`) · 외부 TLS 확인 / prod push = **빌드 안 함 · 같은 SHA 이미지만(없으면 중지)** · head 확인만 · migration 따로 승인 · 한 concurrency group · 롤백 = 이력의 이전 이미지 · 「dev 배포 권한 = 사실상 prod VM root」 주의.
4. **compose project 셋 · 메모리 상한** — 네트워크 표 · 상한 표(prod 1,792 · dev 960 · caddy 50 · ≈ 2,802MB) · 실측 뒤 조정 · 모자라면 2/8 · redis 설정 · 빌드는 VM 밖.
5. **환경별 env(이름만)** — `APP_ENV` · `DB_SCHEMA` · `DATABASE_URL` · `REDIS_URL` · `ENCRYPTION_KEY`(Key Vault) · `KOS_OPEN_API_BASE` · `KOS_INTERNAL_API_BASE` · `KOS_WEB_BASE` · `DAY_ADMIN_EMAILS` · **`KOS_TRIAL_WRITES_ON_LIVE` prod 첫 배포 false** · 도메인 · 주기 값 · Blob/APNs(구현 뒤). 이름은 DAY 코드(`common/config.py` · `emr/kos/client.py` · `deploy/local.env.example`)에서 확인. `DAY_LOCAL_*` · `DAY_SEED_*` 는 배포에 안 넣음.
6. **사용자가 Azure 에서 준비할 것** — VM · VNet/NSG(80/443 만) · 공인 IP · DNS A 레코드 둘 · Key Vault(purge protection · VM identity) · ACR push/pull · OIDC 배포 계정 · PG 스키마 계정 · Blob — **이름 · 리소스 그룹 · IP 등 값은 전부 「미정」**(짓지 않음).
7. **미결** — 실측 메모리 · PG 백업 설정(보존 · PITR · 스키마 단위 복원 없음) · KOS IP 제한 · 스키마 생성 권한 · prod migration 승인 수단 · JSON 로그(구현 필요) · 신뢰 프록시 · infra 코드(Bicep 여부).

## 주의

- 원천 「브랜치 push → 배포」는 조사 D5 추천((b) main → dev 자동 · prod 수동)과 다르다 — 원천(사용자 결정)을 따랐다: **prod 도 push 로 시작**하되 같은 SHA 이미지만 쓰고 migration 은 따로 승인.
- prod migration 「따로 승인」의 실행 방법은 정해지지 않아 미결에 뒀다(centurion `migrate-runtime` 방식을 참고로만).
