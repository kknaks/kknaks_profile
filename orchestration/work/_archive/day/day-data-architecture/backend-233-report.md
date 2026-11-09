# backend 리포트 — Delivery #233 DAY 서버 배포(dev · prod 한 VM) 구현 (2026-11-09)

- 워크트리 `CENTURION_DAY/day-data-architecture` · 브랜치 `kknaksss/day-data-architecture`(PR #228) · 기준 `8f26612f` 위 **미커밋**(커밋 · push 안 함).
- 계약 = Issue #233 contract v2 · 정본 = mediness `products/day/40-architecture/deployment.md` · 본 = centurion `origin/main` 배포 파일(고치지 않음).
- Azure · GitHub 리소스는 만들지 않았다. 비밀값 커밋 없음. 운영 KOS 쓰기는 꺼 둔 채(`deploy/config/prod.env` `KOS_TRIAL_WRITES_ON_LIVE=false`). 사용자 로컬 compose(`day-local` 11040 ~ 11043)는 건드리지 않았다(시작 · 끝 모두 Up 확인).

## 바뀐 것

| 무엇 | 파일 |
|---|---|
| GitHub Actions 넷 — 한 concurrency group `day-vm` · OIDC · action SHA 고정(centurion 과 같은 pin) | `.github/workflows/deploy-dev.yaml` · `deploy-prod.yaml` · `migrate-prod.yaml` · `rollback.yaml` |
| runner 스크립트 — ACR 이미지(태그 = 40자 SHA · 있으면 재사용 · digest 로만) · run-command(레포 묶음 base64 · 한 줄) · 외부 HTTPS(TLS 1.2+) · prod fast-forward 검사 | `scripts/deploy/day-deploy.sh` |
| VM 스크립트(root · run-command) — Caddy(edge) · env 만들기 · ACR pull · migration(dev) / head 확인(prod) · up · 헬스 180초 · 실패 시 그 환경만 이전 env · compose 로 복구 · 이력 · `flock` · 출력은 표식 줄만(로그는 `/var/log/day-deploy/`) | `scripts/deploy/vm-deploy.sh` |
| VM 도우미(python3 3.10+ 표준 라이브러리) — IMDS → Key Vault · ACR refresh token · env 파일(root 0600 · `.previous`) · 이력 JSON 줄 · revision 비교 | `scripts/deploy/day_vm.py` |
| compose 셋 — 환경 하나(api · worker · scheduler · redis · migrate[profile]) · edge(Caddy) · 메모리 상한 · json-file 10m×5 · no-new-privileges | `deploy/compose.yaml` · `deploy/compose.edge.yaml` |
| Caddyfile 두 도메인(snippet · `flush_interval -1` · 본문 6MiB) | `deploy/caddy/Caddyfile` |
| Git 일반 설정 · 메모리 상한 · 도메인 | `deploy/config/{dev,prod}.env` · `{dev,prod}.compose.env` · `edge.env` · `.gitignore`(`!deploy/config/*.env`) |
| JSON 로그(`app_env` 칸 · uvicorn 로거도) | `backend/common/logs.py` · `backend/runtime/main.py` · `backend/runtime/worker.py`(taskiq `--no-configure-logging` 은 서버 compose 에) |
| APP_ENV 필수(앱 프로세스) | `backend/common/config.py`(`AppEnvMissingError` — env 에 없으면 `get_settings()` 실패 · alembic 은 그대로) · `backend/tests/conftest.py`(테스트는 `APP_ENV=dev`) |
| ENCRYPTION_KEY canary(#225 W7) — `/health/ready` 에 `encryption` 확인 | `backend/day/services/crm_connections.py:check_encryption_key` · `backend/day/public.py:encryption_key_canary` · `backend/runtime/health.py` |
| AGENTS.md — 「v2-dev」 → `dev` · `prod` 브랜치 체계 · 구조 · 작업 규칙(배포 = push · Azure 이름은 변수 · env 파일 규칙) | `AGENTS.md` |
| 배포 문서(사용자 준비 이름 목록 · 첫 배포 절차 · dry-run) | `docs/development/deployment.md`(새) |
| 테스트 | `backend/tests/deploy/test_day_vm.py` · `test_deploy_contract.py` · `tests/common/test_logs.py` · `tests/day/test_encryption_canary.py`(infra) · `tests/runtime/test_startup_key.py` · `test_health.py` |

#225 W5(offline SQL `CREATE SCHEMA IF NOT EXISTS` · `SET search_path`)는 이미 `backend/migrations/env.py:126-130` 에 있고 `tests/migrations/test_offline_sql.py` 가 지킨다 — 손대지 않음. #225 W8(공용 Redis timeout 분리) 회귀 = `tests/common/test_redis.py:21` 통과.

## Acceptance 증거

| AC | 증거 |
|---|---|
| **A1** 로컬 prod 모양 | 실제 `deploy/` 파일 그대로(스크래치에 `/opt` · `/etc` 모양 복사) · project `day-edge` · `day-dev` · `day-prod` · 버려도 되는 PG(127.0.0.1:11142) · Caddy 11180/11443 · 도메인 로컬 대체 `http://day-dev.localhost` · `http://day-prod.localhost`. ① **두 환경 health 200** — Caddy 경유 `/health/live` · `/health/ready` = `{"database":"ok","redis":"ok","encryption":"ok"}` 둘 다 ② **호스트 포트 = Caddy 뿐** — 다른 8컨테이너 `PortBindings={}` ③ **edge 별칭** — `day-edge` 망 = caddy · day-dev-api · day-prod-api, 별칭 `day-dev-api` · `day-prod-api` ④ **mem_limit = 표** — prod 768/384/384/256 · dev 384/256/192/128 · caddy 50 MiB(`HostConfig.Memory` 바이트 확인) ⑤ redis `maxmemory` 96mb/192mb · `noeviction` · `appendonly yes` ⑥ **project 독립** — `day-dev up -d --remove-orphans --force-recreate` 뒤 day-prod · day-edge 컨테이너 id · StartedAt 그대로, 반대로도 그대로 ⑦ `docker stats` 실측(빈 DB): api ≈ 89MiB · worker ≈ 106MiB · scheduler ≈ 83MiB · redis ≈ 4MiB · caddy ≈ 11MiB ⑧ 끝나고 그 셋 · PG · 망 · volume · 이미지만 지움 — `day-local` 5개 Up 그대로. 원본 출력 `scratchpad/shape/a1-evidence.txt`(아래 「증거 파일」) |
| **A2** 워크플로 | `actionlint` 0 오류(run 블록 shellcheck 포함). 계약 테스트 `test_deploy_contract.py`: 넷 모두 `day-vm` · `id-token: write` · action 40자 SHA 고정 · dev = push(dev) · `prepare-image` · TLS 뒤 이력 · prod = push(prod) · `check-promotion` → `require-image` → `remote deploy prod`(빌드 없음) · migrate-prod = 수동 · 입력 `commit_sha` · `confirm`(`migrate day_prod`) · `refs/heads/prod` 에서만 · 롤백 = 수동 · 환경 · SHA · `git push` 없음. **중지 분기**: 이미지 없음 → `require-image` `image-missing-for-sha` · prod head 다름 → `prod-revision-not-at-image-head` · **prod migration 은 dev 가 같은 revision 이 아니면** → `dev-revision-not-at-image-head`(그 전에 dev 이력에 SHA 없으면 `sha-not-deployed-to-dev`). revision 비교는 실물 alembic 출력으로도 확인: `heads`=`current`=`0005_outbox_sender (head)` → `DAY_REVISION_OK`, `0004_board` → `revision-mismatch` rc 2. fast-forward 검사는 임시 git 레포로(강제 · 뒤로 · dev 밖 commit 거부) |
| **A3** VM 스크립트 dry-run | `DAY_DRY_RUN=1` — deploy dev/prod · migrate prod · rollback · record · check-public · prepare/require-image. 만들 `app.env` · `compose.env` 내용(비밀값은 `<key-vault:day-prod-database-url>` 처럼 이름) · docker compose 명령 · 이력 줄을 출력만, `/etc/day` · `/opt/day` 없음 확인. 테스트: dry-run 출력에 `postgresql` · 자리 비밀번호 없음 · materialize dry-run 은 out-dir 를 만들지 않음 · 틀린 입력(stg · 짧은 SHA · 태그 이미지 · dev migrate) rc 2. 원본 `scratchpad/a3-evidence.txt` |
| **A4** JSON 로그 | 단위 `tests/common/test_logs.py`(줄마다 JSON · `app_env` · 한글 그대로 · 예외 `exc_info` 한 줄 · 재호출 안전 · factory 뒤 실제 프로세스 출력 전부 JSON). 실물: 6컨테이너 로그 모든 줄 JSON · `app_env` dev/prod 맞음(평문 0줄) · Docker 로그 `json-file` `max-size 10m` · `max-file 5` |
| **A5** | APP_ENV 없음 → `AppEnvMissingError`(api · worker · scheduler 테스트 + 실제 이미지 `docker run` 실패) · `--sql` 앞 `CREATE SCHEMA IF NOT EXISTS` · `SET search_path`(기존 테스트) · canary: infra 테스트(같은 키 통과 · 연결 없음 통과 · **다른 키 → `DecryptionError`**) + 실물: prod 스택에 암호화 연결 하나 넣고 dev 키로 api 재기동 → `/health/ready` **503** `encryption: failed` → 키 되돌리면 200 |
| **A6** grep | 추적 + 새 파일(`deploy/local.env` 제외)에 GUID 0 · `acrcsp` · `<이름>.azurecr.io` · `kv-` · `rg-` 실제 이름 0 · 워크플로 `secrets.` 0 · `vars.` 는 8개 이름만(테스트 `test_워크플로는_GitHub_변수만_참조한다`). 예시 값은 `exampleacr` 뿐(테스트 · 문서) |
| **A7** 실물 | **안 함** — 사용자 준비 + PR #228 `dev` 머지 뒤 |
| **A8** | `AGENTS.md` 의 `v2-dev` 0(grep · 테스트) |

검증 명령 결과: `uv run pytest -m "not infra"` 368 passed · `scripts/test.sh -q` **529 passed**(infra 포함) · `ruff check backend scripts` · `ruff format --check` 통과 · `shellcheck scripts/deploy/*.sh scripts/*.sh` 통과 · `actionlint` 통과.

## 사용자 준비 목록 (이름만 — 값은 짓지 않았다)

**GitHub**
- 브랜치 `dev` · `prod`(`prod` fast-forward 만 — 규칙 강제는 사용자 판단, 워크플로도 강제 push · 뒤로 · dev 밖 commit 을 막는다).
- Environments `dev`(배포 브랜치 = `dev`) · `prod`(배포 브랜치 = `prod` · 승인자 규칙은 plan 이 되면).
- Environment 변수(각 환경): `AZURE_CLIENT_ID` · `AZURE_TENANT_ID` · `AZURE_SUBSCRIPTION_ID` · `DAY_RESOURCE_GROUP` · `DAY_VM_NAME` · `DAY_ACR_NAME`(`<이름>.azurecr.io` 의 앞) · `DAY_IMAGE_REPOSITORY` · `DAY_KEY_VAULT`. Actions secrets 없음.

**Azure**
- VM 2코어/4GB · Docker compose v2 · python3 3.10+ · 시스템 managed identity. NSG 외부 80/443 만.
- DNS A `day-dev.medisolveai.com` · `day.medisolveai.com` → VM 공인 IP(먼저).
- ACR: 배포 identity AcrPush · VM identity AcrPull.
- 배포 identity(OIDC): federated credential subject **`repo:MediSolveAIDev/CENTURION_DAY:environment:dev`** · **`…:environment:prod`** — 워크플로가 GitHub Environment 를 쓰므로 subject 는 브랜치가 아니라 environment 다(브랜치 제한은 Environment 의 배포 브랜치 규칙이 한다). 권한 = ACR push · 그 VM 의 run-command.
- Key Vault: VM identity `Key Vault Secrets User` · purge protection.

**Key Vault 비밀 이름**(이 구현이 정한 이름 — Vault 하나 · 둘 어느 쪽이든 같은 이름)
- `day-dev-database-url` · `day-prod-database-url` → `DATABASE_URL`(`postgresql+asyncpg://…` · 환경별 계정)
- `day-dev-redis-url` · `day-prod-redis-url` → `REDIS_URL` — **호스트는 반드시 `redis`**(`redis://:<pw>@redis:6379/0`). 비밀번호를 redis 컨테이너에도 쓴다.
- `day-dev-encryption-key` · `day-prod-encryption-key` → `ENCRYPTION_KEY`(Fernet · 환경마다 다르게)

## 첫 배포 절차

1. 위 준비(DNS 먼저) · 로컬 `dev`(옛 rc.14 계열) 브랜치 정리.
2. PR #228 → `dev` 머지 = **deploy-dev** 시작 → `DAY_DEPLOY_OK` · `DAY_PUBLIC_TLS_OK` · 이력 기록 확인. 이때 Caddy 가 두 도메인 인증서를 받는다(prod 도메인은 prod 가 뜨기 전까지 502).
3. dev 화면 확인 → 그 SHA.
4. `prod` 브랜치가 없으면 `git push origin <sha>:refs/heads/prod` 로 만든다 — 이 push 의 deploy-prod 는 DB 가 head 가 아니라 **멈춘다(정상)**.
5. **migrate-prod** 를 `prod` 브랜치에서 실행(입력 SHA · `migrate day_prod`) → `DAY_MIGRATION_OK`.
6. deploy-prod 재실행(Re-run) 또는 다음 fast-forward push → prod 헬스 · `https://day.medisolveai.com` TLS.
7. VM `docker stats` 실측 → `deploy/config/<env>.compose.env` 다시 맞추기(PR).

## 코디가 볼 것 · 남은 것

- **실물로 돌려 보지 못한 길**: `vm-deploy.sh` 비-dry 경로(root · IMDS → Key Vault · ACR 토큰 교환 · `flock` · 실패 복구) · `az vm run-command` · 실제 ACR. dry-run · 단위 테스트 · 로컬 compose 로만 확인했다. 첫 dev 배포가 첫 실물 시험이다.
- run-command 에 싣는 스크립트 ≈ 37KB(묶음 base64 두 번). Run Command 크기 한도는 확인하지 않았다 — 넘치면 묶음을 Blob 등으로 바꿔야 한다. 출력 4KB 한도 때문에 VM 출력은 표식 줄 + 실패 시 로그 끝 15줄만.
- deployment.md 와 다른 점(코디 확인 필요): ① OIDC federated credential 을 「브랜치별」이 아니라 **environment 별** subject 로 안내 ② Key Vault 비밀 이름 `day-<env>-…` 은 이 구현이 정함 ③ prod migration 승인 = 확인 문자열 `migrate day_prod` + `prod` 브랜치 + Environment `prod`(승인자 규칙은 사용자) ④ 롤백은 실행한 브랜치 머리의 compose · 일반 설정을 쓴다(이미지만 이전 것).
- 외부 HTTPS 확인이 실패하면 워크플로 실패 · 이력 미기록이지만 VM 은 새 이미지로 떠 있다(자동 복구는 VM 안 헬스 실패 때만).
- Caddy 는 모르는 Host 에 빈 200 을 준다(Caddy 기본). edge 망에서 서비스 이름 `api` 별칭은 두 api 가 같이 갖는다 — Caddy 는 `day-<env>-api` 만 쓰므로 영향 없음.
- 신뢰 프록시: DAY 코드는 클라이언트 IP · scheme 을 읽지 않는다(세션 쿠키 늘 `Secure`) — uvicorn `--proxy-headers` 는 넣지 않음(문서 「아직 정하지 않은 것」).
- 로컬 `compose.local.yaml` 은 바꾸지 않았다 — 로컬 worker 는 taskiq 주 프로세스 몇 줄이 평문(자식은 JSON).
- 미결 그대로: 실측 메모리 · PG 백업 · KOS IP 제한 · 스키마 생성 권한 · prod 승인자.

## 증거 파일

- `/private/tmp/claude-501/-Users-kknaks-orca-workspaces-CENTURION-DAY-day-data-architecture/4fd42c8c-f3ab-42ea-92b0-f13eb573a6bb/scratchpad/shape/a1-evidence.txt`(A1 · A4 실물 · A5 canary 실물 · 정리) · `setup.sh` · `c.sh`(재현용 — 비밀 env 파일은 지움)
- 같은 scratchpad `a3-evidence.txt`(dry-run 출력) · `a6-evidence.txt`(grep)
