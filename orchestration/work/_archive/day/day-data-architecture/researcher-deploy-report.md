# DAY 서버 배포 방법 — centurion 배포 방식 조사 + DAY 대입

- 작성: day researcher · 2026-11-08 · 읽기 전용(클라우드 · 서버 접속 없음, 문서 · 코드만)
- 근거 ref
  - centurion: `/Users/kknaks/git/centurion` `origin/main` = `6fe5112` — 아래 `C:` 로 줄인다(`C:<경로>:<줄>`)
  - DAY 코드: `/Users/kknaks/orca/workspaces/CENTURION_DAY/day-data-architecture` HEAD `8f26612f` — `D:` 로 줄인다
  - DAY 원천: `reference/2026-11-03-cc-day/system/README.md` — `R:` · mediness `products/day/40-architecture/system.md` — `S:`
- **전제(사용자 2026-11-08 · 코디 전달)**: 앞단 = Caddy · **dev 와 prod 를 VM 한 대(2코어/4GB)에 같이** · 관리형 PostgreSQL 1대 · DB 1개 · 스키마 `day_dev` / `day_prod`.
  §2 · §3 은 이 전제로 썼다. centurion 은 stg/prod 를 VM 두 대로 나눴다(§1) — 그 차이가 이 리포트의 중심이다.

---

## 1. centurion 배포 흐름 한 장

```text
 개발자 ─ PR → main 병합
    │
    ▼  GitHub Actions 「Deploy Centurion STG / PROD」 — 수동 Run workflow(브랜치 선택 + 선택 commit_sha)
 ┌──────────────────────────── GitHub runner (ubuntu-24.04) ────────────────────────────┐
 │ ① 출처 고정: dispatch SHA · 실행자 권한 확인(prod 는 허용 actor 목록)                   │
 │ ② Azure 로그인 = OIDC(장기 키 없음) → ACR 로그인                                       │
 │ ③ 이미지: ACR `acrcspmedisolveaishared/centurion-api:<40자 SHA>` 있으면 재사용, 없으면 빌드·push │
 │    → 이후 전부 digest(`@sha256:…`)로 지칭                                              │
 └──────────────┬─────────────────────────────────────────────────────────────────────┘
                │  az vm run-command invoke (SSH 아님 · 스크립트를 base64 로 실어 VM root 로 실행)
                ▼
 ┌──────────────────────────── 앱 VM (환경마다 1대) ─────────────────────────────────────┐
 │ ④ env 만들기: VM managed identity 로 Key Vault 비밀값 내려받기 + Git 의 config/<env>.env  │
 │    → /etc/centurion/{medical.env,compose.env} (root 0600, 이전 것은 .previous)          │
 │    (STG 는 매 배포 · PROD 는 이미지 값 GIT_SHA · CENTURION_IMAGE 만 교체)                 │
 │ ⑤ preflight: compose.yaml · Caddyfile · config 를 /opt/centurion 에 놓고, VM 이 ACR 에서 │
 │    이미지 pull(VM identity) → `alembic current --check-heads` — **migration 은 안 돌린다** │
 │    head 가 아니면 중지                                                                 │
 │ ⑥ `docker compose up -d --remove-orphans <서비스>` → 180초 안에 health 확인             │
 │    실패 시 자동 복구 = bootstrap Caddy 만 남김(/health-check 200 · 나머지 503)          │
 │ ⑦ 관찰(이미지 identity · OOM · 재시작) → 외부 HTTPS 경로 curl                          │
 │ ⑧ 성공 이미지 이력 기록(/etc/centurion/deployment-history.env) · release receipt 업로드 │
 └──────────────────────────────────────────────────────────────────────────────────────┘
 migration · worker 전환 · DNS · 이전 이미지 복구 = 배포 버튼 밖, 운영자가 따로(승인 문자열 인자)
```

| 단계 | 내용 | 근거 |
|---|---|---|
| 트리거 | `workflow_dispatch` 만(push · tag · PR 없음). 입력은 선택 `commit_sha` 하나. 동시 실행 금지(`cancel-in-progress: false`) | `C:.github/workflows/deploy-stg.yaml:4-18` · `deploy-prod.yaml:4-18` |
| 출처 · 실행자 확인 | 브랜치 ref · SHA 형식 · 그 SHA 가 원격 브랜치에 있는지. stg 는 write 권한자, prod 는 `PROD_ALLOWED_ACTORS` 목록 + `PROD_DEPLOYMENT_ENABLED` | `C:scripts/infrastructure/deployment_source.py:13-48` · `deploy-prod.yaml:34-35,54-62` |
| 승인 | GitHub Team private repo 라 Environment required reviewer 미지원 → 「허용 actor 목록」이 사실상 승인. 브랜치 writer 를 신뢰하는 모델이라고 문서가 명시 | `C:docs/migration/prod-cicd-runbook.md:48-51,79-84` · `stg-cicd-runbook.md:91-92` |
| Azure 인증 | `Azure/login` OIDC, `vars.AZURE_CLIENT_ID/TENANT/SUBSCRIPTION`. stg identity = AcrPush, prod identity = AcrPull + VM 한 대 Run Command 만 | `C:deploy-stg.yaml:64-77` · `prod-cicd-runbook.md:61-71,98-100` · `stg-cicd-runbook.md:44-68` |
| 레지스트리 | 회사 공용 ACR `acrcspmedisolveaishared`, repo `centurion-api`, 태그 = 40자 SHA, 있으면 재빌드 안 함 | `C:scripts/infrastructure/prepare-image.sh:14-44` |
| 빌드 비밀값 | `PRIVATE_PYPI_USERNAME/PASSWORD`(Environment secret) — 임시 파일로만 | `C:deploy-stg.yaml:79-89` · `prepare-image.sh:26-33` |
| VM 전달 | `az vm run-command invoke --command-id RunShellScript` · 스크립트 base64 · 성공 marker 문자열 검사. **SSH 아님**(prod 는 SSH ingress 없음) | `C:scripts/infrastructure/manual-app-deploy.sh:96-117` · `docs/migration/deployment-baseline.md:13` |
| VM 파일 자리 | `/etc/centurion`(root 0600 env · 이력) · `/opt/centurion`(compose.yaml · Caddyfile · config/<env>.env) | `C:manual-app-deploy.sh:640-701,886-930` |
| 설정 · 비밀값 | 일반 설정 = Git `deploy/config/<env>.env`(PR 로 변경, 비밀 키 넣으면 도구가 거부). 비밀값 = Key Vault(`kv-centurion-<env>`), VM identity 가 `Key Vault Secrets User` 로 읽음. 키 분류 정본 = `deploy/environment-manifest.json`(config 114 · secret 30 · 생성형 2) | `C:deploy/config/stg.env:1-3` · `docs/migration/application-deployment-runbook.md:28-65` · `deploy/environment-manifest.json` |
| env 순서 | compose `env_file` = config/<env>.env 다음 medical.env(뒤가 우선) | `C:deploy/compose.yaml:9-16` |
| migration 시점 | **배포는 안 돌린다** — preflight 가 head 확인만, 불일치면 중지. 별도 `migrate-runtime <env> migration-approved`(one-shot `migrate` 컨테이너 `alembic upgrade head`) | `C:manual-app-deploy.sh:871-985,1020-1061` · `compose.yaml:222-227` · `application-deployment-runbook.md:160-171` |
| HTTPS | Caddy 자동 HTTPS(80/443 만 publish, 관리 API 2019 미공개), 인증서 volume 영속 · `down -v` 금지. bootstrap Caddyfile(200/503) 로 먼저 인증서 받고 앱 붙임 | `C:deploy/Caddyfile:1-32` · `Caddyfile.bootstrap:1-4` · `docs/migration/caddy-https-runbook.md:7-22` |
| 네트워크 | NSG 외부 TCP 80/443 만, 22 · 8000 · Redis · RabbitMQ 차단. 나가는 IP = subnet NAT Gateway(Key Vault 방화벽이 그 /32 만 허용) | `C:docs/migration/infrastructure-deployment-runbook.md:30-47,87-88` |
| 로그 | cloud-init 이 Docker `json-file` 10m × 5 회전만. prod config 에 `LOG_FILE_PATH=/app/logs/*.json` | `C:infra/azure/cloud-init.yml:13-14` · `deploy/config/prod.env:35-36,72` |
| 롤백 | 자동 = bootstrap Caddy 만(이전 버전 복원 아님). 이전 정상 이미지는 이력에서 골라 운영자가 promote → preflight → deploy | `C:deploy-prod.yaml:236-243` · `prod-cicd-runbook.md:130-166` · `manual-app-deploy.sh:805-869` |
| 배포 시간대 | API 재시작이 진행 중 상담 상태를 지움 → 상담 시간 밖에 배포 | `C:docs/guides/01-code-deploy.md:18-20` |
| VM 크기 | stg `Standard_B2s`(2/4) · prod `Standard_B2ms`(2/8). 가용 메모리 1GiB 미만 · OOM 이면 재산정, 빌드는 VM 밖 | `C:infrastructure-deployment-runbook.md:35-36` · `deployment-baseline.md:9,16-18` |
| Redis 분리 이유 | Pub/Sub 은 logical DB 번호를 무시 → 환경 · 서비스 prefix 필수, 기존 Redis 재사용 안 함 | `C:deployment-baseline.md:48-69` |

---

## 2. DAY 에 대입 — 전제: VM 1대(2/4)에 dev + prod

### 2-1. 한 VM 에 두 환경 — compose 나누기 (추천안)

```text
 인터넷 ──80/443──▶ ┌─ compose project `day-edge` ─────────┐
                    │ caddy (한 개 · 80/443 · 인증서 volume)  │
                    │  {$DAY_DEV_DOMAIN}  → day-dev-api:8000  │
                    │  {$DAY_PROD_DOMAIN} → day-prod-api:8000 │
                    └──────────┬──────────────┬─────────────┘
              docker 네트워크 `day-edge`(external) — caddy 와 각 api 만 참여
                    ┌──────────▼───────┐  ┌───▼──────────────┐
 project `day-dev`  │ api · worker ·   │  │ api · worker ·   │ project `day-prod`
 (APP_ENV=dev,      │ scheduler · redis│  │ scheduler · redis│ (APP_ENV=prod,
  DB_SCHEMA=day_dev)│ 내부망 day-dev   │  │ 내부망 day-prod  │  DB_SCHEMA=day_prod)
                    └────────┬─────────┘  └────────┬─────────┘
                             └──── VM 밖 관리형 PostgreSQL(DB 1개) ────┘  · Azure Blob
```

| 항목 | 추천 | 이유 · 근거 |
|---|---|---|
| 프로젝트 이름 | `day-edge`(caddy) · `day-dev` · `day-prod` 셋 | centurion 은 `centurion-medical-<env>` 로 project 를 환경마다 나눈다(`C:compose.yaml:1`). project 가 나뉘면 `docker compose -p day-dev up -d --remove-orphans` 가 **prod 컨테이너를 건드리지 않는다**. caddy 를 어느 한 환경 project 에 넣으면 그 환경의 `--remove-orphans` · 복구 로직(centurion 은 실패 시 앱을 내리고 caddy 만 남김, `C:manual-app-deploy.sh:1089-1124`)이 다른 환경 트래픽까지 끊는다 → caddy 는 따로 |
| compose 파일 | `deploy/compose.yaml` 하나를 두 env 가 같이 쓰고 `DAY_DEPLOY_ENV`(dev/prod) 로 project 이름 · 네트워크 별칭 · volume 이름을 바꾼다 + `deploy/compose.edge.yaml`(caddy) | centurion 이 `name: centurion-medical-${CENTURION_DEPLOY_ENV}` 로 같은 방식(`C:compose.yaml:1,237-241`) |
| VM 파일 자리 | `/etc/day/{dev,prod}/`(root 0600 env) · `/opt/day/{dev,prod}/`(compose · config) · `/opt/day/edge/`(Caddyfile) | centurion `/etc/centurion` · `/opt/centurion` 을 환경별 하위로 |
| 포트 | **호스트에 여는 건 caddy 80/443 뿐**. api 는 호스트 포트 없이 edge 네트워크 별칭으로만(`day-dev-api` · `day-prod-api`). 디버그용으로 열려면 `127.0.0.1:11040`(dev) · `127.0.0.1:11050`(prod) 처럼 겹치지 않게 | centurion 은 api 를 `127.0.0.1:8000` 에만 publish(`C:compose.yaml:67-68`), NSG 가 8000 차단. 두 환경이면 같은 8000 을 둘 다 못 쓴다 |
| redis | **환경마다 한 개(공유 안 함)** | DAY 는 Redis 를 taskiq 브로커 · 결과 · SSE 알림 pub/sub · 병원별 잠금에 쓴다(`S:64`). 공유하면 ① pub/sub 은 DB 번호를 무시해 dev 알림이 prod 로 샌다(`C:deployment-baseline.md:67-69`) ② 잠금 · 큐 이름 충돌 ③ dev 정리(flush)가 prod 를 지운다. 공유안의 이득은 메모리 ~100–250MB 뿐 |
| redis 설정 | 비밀번호 + `appendonly` + `maxmemory` < `mem_limit` + `noeviction` | centurion `C:compose.yaml:174-199`. DAY 로컬은 maxmemory 없음(`D:deploy/compose.local.yaml:54-56`) |
| Caddy 한 개로 두 도메인 | Caddyfile 에 사이트 블록 둘(`{$DAY_DEV_DOMAIN}` · `{$DAY_PROD_DOMAIN}`), 각각 `reverse_proxy day-<env>-api:8000`. 인증서는 도메인별로 자동 발급 · 같은 `caddy-data` volume | centurion 은 블록 하나(`C:Caddyfile:1,31`) — 블록만 늘리면 된다. 두 도메인 DNS A 가 같은 VM IP 를 가리켜야 한다 |
| caddy 고정 IP | edge 네트워크 subnet · caddy IPv4 고정(신뢰 프록시 CIDR 용) | centurion `172.18.0.10` 고정 · `AUTH_TRUSTED_PROXY_CIDRS`(`C:compose.yaml:36-38` · `application-deployment-runbook.md:42-46`). DAY 코드에 신뢰 프록시 설정이 있는지는 확인 안 됨(§4) |
| 배포 동시 실행 | 두 환경 배포를 **한 concurrency group**(`day-vm`)으로 | VM 한 대는 Run Command 를 한 번에 하나만 받는다(`C:prod-cicd-runbook.md:123-125`) |

**메모리 — 4GB 에 두 벌이 들어가나**

| | api | worker | scheduler | redis | 합 |
|---|---:|---:|---:|---:|---:|
| 원천 예상(한 벌, `R:37` · `S:114`) | 768 | 384 | 384 | 256 | 1,792MB |
| 두 벌 그대로 + caddy 50 | | | | | **≈ 3,634MB** |
| 추천: prod 그대로 + dev 낮춤(384 · 256 · 192 · 128) + caddy 50 | | | | | **≈ 2,802MB** |

- 원천 수치는 **상한(mem_limit) 성격**이고 실측이 아니다. 두 벌 그대로면 상한 합이 3.6GB 라 OS · Docker 데몬 · 이미지 pull(배포 중 일시적) 몫이 0.4GB 도 안 남는다 — centurion 의 재산정 기준(가용 1GiB 미만, `C:deployment-baseline.md:16-17`)에 걸린다.
- dev 상한을 낮추면 ≈ 2.8GB 로 1.2GB 가량 남는다. 참고 실측: centurion 은 taskiq 모듈을 읽은 프로세스 하나가 약 85MB(`C:compose.yaml:139`) — DAY 실측은 확인 안 됨.
- 빌드는 VM 밖(runner)에서 — centurion 원칙(`C:deployment-baseline.md:18`). VM 에서 `docker build` 하면 4GB 가 버티지 못할 수 있다.
- 결론: **두 벌은 상한을 조정하면 들어간다.** 다만 첫 배포 뒤 `docker stats` 실측으로 상한을 다시 맞추는 것을 조건으로 둔다.

### 2-2. 그대로 쓸 것 / 바꿀 것

| 주제 | centurion | DAY | 판정 |
|---|---|---|---|
| 트리거 | 수동 `workflow_dispatch` + 선택 SHA, SHA 고정 | DAY 레포에 `.github/` 없음(D: 루트 목록) | **그대로** + 입력에 `environment: dev\|prod` 추가 |
| 이미지 | 공용 ACR · 태그=SHA · digest 로 배포 · 있으면 재사용 | `deploy/Dockerfile` 하나로 api/worker/scheduler 공용(`D:deploy/Dockerfile:1`) | **그대로**(repo 이름만 예: `day-api`). dev · prod 가 **같은 digest** 를 쓰게 — dev 에서 확인한 이미지를 prod 로 승격 |
| 빌드 비밀값 | private PyPI 계정 필요 | `pyproject.toml` 에 별도 index 없음 · uv 공개 이미지 | **바꿈** — 빌드 secret 불필요 |
| Azure 인증 · VM 전달 | OIDC + Run Command(SSH 없음) | — | **그대로**. 단 VM 한 대라 dev/prod identity 를 나눠도 둘 다 같은 VM root 를 얻는다(§3 D5) |
| 설정 · 비밀값 | Git config + Key Vault + manifest(분류 검사) | 원천은 「서버 env → 나중에 Key Vault」(`R:50` · `S:130`). env 이름: `APP_ENV` · `DB_SCHEMA` · `DATABASE_URL` · `REDIS_URL` · `ENCRYPTION_KEY` · `KOS_*_BASE` · `DAY_ADMIN_EMAILS` · `KOS_TRIAL_WRITES_ON_LIVE` 외 주기 값(`D:backend/common/config.py:37-105` · `D:deploy/compose.local.yaml:14-25`) | **모양 그대로, 크기 축소** — 비밀은 `DATABASE_URL` · `REDIS_URL`(비밀번호) · `ENCRYPTION_KEY` (+ 나중 APNs 키 · Blob 접속값) 정도라 manifest 가 작다 |
| 환경 이름 | `stg` / `prod` | `APP_ENV=dev` / `prod`(`D:config.py:23,40`) | **바꿈** — dev/prod |
| DB | 서비스마다 DB(`auth_stg` · `linky_stg`, `C:deployment-baseline.md:33-34`) | DB 1개 · 스키마 `DB_SCHEMA`, 계정도 스키마별(`R:22`) | **바꿈** — `DATABASE_URL` 의 계정이 환경마다 다르고 `DB_SCHEMA` 가 다르다 |
| migration | 배포 밖 · 승인 gate · preflight 는 head 확인만 | 로컬 compose 는 `migrate` 가 매번 먼저 돌고 api 가 그 뒤(`D:compose.local.yaml:70-96`). migrate 는 `ENCRYPTION_KEY` 없이 돈다(`:73-76`). 스키마가 없으면 `CREATE SCHEMA` 를 한다(`D:backend/migrations/env.py:80-88`) | **정할 것**(§3 D6). check-heads preflight 는 그대로 쓸 만하다 |
| 서비스 | caddy · redis · rabbitmq · api · worker · scheduler · common-worker · charty-* | api · worker · scheduler · redis(RabbitMQ 없음, `S:64`) | **바꿈** — rabbitmq · common-worker · charty 삭제 |
| 비동기 보류 모드 | `async-services-withheld`(legacy worker 가 큐 주인이라) | 넘길 legacy 주인 없음. worker 가 KOS 동기화의 본체(`S:61`) | **버림** — 항상 전체 기동 |
| api 프로세스 수 | `--workers 1`(상담 상태가 메모리) | SSE 알림은 Redis pub/sub(`R` 기본값 표) — 원리상 여럿 가능 | 1 로 시작(메모리 때문) |
| health | `/health-check`(caddy) · `/linky/api/v1/health/live` 등 | `/health/live`(생존) · `/health/ready`(DB · Redis, `D:backend/runtime/health.py:3-4`) | **바꿈** — 경로만 |
| Caddy body 상한 | 경로별 1–210MiB | DAY 업로드 경로(신분증 사진 · 채팅 첨부)는 Blob 구현 전이라 경로 미정 | **바꿈** — 기본 상한 하나로 시작, 업로드 경로 생기면 추가 |
| 로그 | Docker json-file 10m×5 + prod 파일 로그 | 원천 「구조화 JSON 로그(centurion 형식)」(`R:51`). **코드에는 아직 JSON 포매터 없음** — `logging.getLogger` 만(`D:backend/runtime/health.py:11,22`) | 회전은 **그대로**(cloud-init). JSON 포매터는 구현 필요 |
| 롤백 | 자동 = caddy 만 · 이전 이미지는 운영자 | — | **바꿈 권장** — 한 VM 두 환경에서 「앱 내리고 caddy 만」은 다른 환경까지 영향 없게 project 단위로만. 이전 이미지 재배포(이력) 쪽을 기본으로 |
| 배포 시간대 | 상담 시간 밖 | DAY api 재시작 = SSE 끊김 · 버튼 응답 일시 실패, worker 재시작 = 다음 10초 회차가 메움(outbox 는 DB 에 있음, `R:10`) | prod 는 **진료 시간 밖** 권장 |
| KOS 연결 | `KOS_OPENAPI_BASE_URL` 만(공개 API) | 내부 API 는 브라우저 헤더 필수(`S:202,212`) · 주소는 env 3개(`D:backend/day/emr/kos/client.py:51-72`) | env 3개를 `config/<env>.env` 에. 나가는 IP 는 NAT Gateway — KOS 쪽 허용 목록 필요 여부 확인 안 됨 |
| dev 데이터 보호 | — | `APP_ENV=dev` 는 `is_demo` 연결만 동기화(`D:backend/day/services/crm_connections.py:3` · `S:182`) · kit 화면은 dev 에서만(`D:backend/day/routers/kit.py:24`) | 그대로 — 같은 VM 이어도 dev 가 실제 병원을 안 건드리는 근거 |

---

## 3. 사용자가 정해야 할 것

전제(VM 1대 · Caddy · PG 1대 · 스키마 둘)는 이미 정해졌으므로 다시 묻지 않는다. 각 항목 = 선택지 · 근거 · 추천.

| # | 정할 것 | 선택지 | 추천 · 근거 |
|---|---|---|---|
| D1 | compose 나누기 | (a) project 셋 `day-edge`·`day-dev`·`day-prod` (b) caddy 를 prod project 안에 (c) 한 project 에 서비스 이름 접미사로 두 벌 | **(a)** — 한쪽 배포 · 복구가 다른 쪽을 안 건드린다(§2-1). (c) 는 `--remove-orphans` 한 번에 둘 다 영향 |
| D2 | redis | (a) 환경마다 1개 (b) 1개 공유 + DB 번호 · key prefix | **(a)** — pub/sub 이 DB 번호를 무시(`C:deployment-baseline.md:67-69`), 이득은 ~100–250MB |
| D3 | 메모리 상한 | (a) 두 벌 원천 수치 그대로(3.6GB) (b) dev 낮춤(≈2.8GB) (c) VM 을 B2ms(2/8)로 | **(b)** + 첫 배포 뒤 실측으로 재조정. 실측이 모자라면 (c) — centurion prod 가 B2ms(`C:infrastructure-deployment-runbook.md:36`) |
| D4 | 레지스트리 | (a) 회사 공용 ACR `acrcspmedisolveaishared`(repo 예: `day-api`) (b) GHCR (c) VM 에서 직접 빌드 | **(a)** — VM managed identity 로 pull, centurion 도구 그대로. 권한 부여(AcrPush/AcrPull)는 Azure 관리자가 해야 함. (c) 는 4GB 에서 비권장 |
| D5 | 배포 트리거 · 실행 권한 | (a) 둘 다 수동 dispatch(환경 선택) (b) main 병합 → dev 자동, prod 수동 (c) 태그 → prod | **(b)** — dev 는 자주 올리고, prod 는 「dev 에서 확인한 같은 digest」만 수동 승격. prod 실행자는 허용 actor 목록(centurion 방식, Team plan 이라 reviewer 불가 `C:prod-cicd-runbook.md:79-84`). 주의: VM 이 하나라 dev 배포 권한 = 사실상 prod VM root(`C:prod-cicd-runbook.md:74-77` 같은 이유) — dev 배포 권한자도 prod 와 같은 사람으로 |
| D6 | migration 누가 · 언제 | (a) 배포 workflow 가 매번 `migrate` 먼저(로컬과 같음) (b) centurion 처럼 배포 밖 수동 gate, 배포는 head 확인만 (c) dev 는 (a) · prod 는 (b) | **(c)** — 원천 「dev 먼저 → prod 같은 것」(`R:22`)과 맞는다. prod 배포 전 「dev 에 같은 revision 적용됨」 확인. 함께 정할 것: `env.py` 가 `CREATE SCHEMA` 를 하므로(`D:backend/migrations/env.py:80-88`) migration 계정에 DB 의 CREATE 권한을 줄지, DBA 가 `day_dev`·`day_prod` 를 미리 만들어 둘지 · migration 계정을 앱 계정과 나눌지 |
| D7 | 비밀값 자리 | (a) 처음부터 Key Vault(centurion 모양) (b) 우선 VM root-only env 파일 → 나중에 Key Vault (c) GitHub Environment secret 을 배포 때 실어 보냄 | **(a)** — 이관을 두 번 하지 않는다. 특히 `ENCRYPTION_KEY` 를 잃으면 암호화 칸(KOS 접속값 등)을 못 읽는다(`D:config.py:8-11,50-52`) → purge protection 있는 Vault 가 보관처로 맞다. Vault 하나에 `dev-`/`prod-` 접두로 둘지, 둘로 나눌지도 함께 — VM identity 가 하나라 나눠도 VM 에서는 둘 다 읽힌다 |
| D8 | 도메인 | 이름 · DNS 관리 주체 | 사용자가 정한다(이 리포트는 이름을 짓지 않는다). centurion 은 `medisolveai.com` 하위(`C:caddy-https-runbook.md:11-12`). 두 도메인 A 레코드 → 같은 VM 공인 IP |
| D9 | HTTPS | (a) Caddy 자동 HTTPS(ACME) (b) 회사 인증서 수동 (c) 앞에 Application Gateway | **(a)** — 전제(Caddy)와 centurion 과 같음. 조건: NSG 80/443 열림 · DNS 먼저 · 인증서 volume `down -v` 금지(`C:caddy-https-runbook.md:16-22`) |
| D10 | 로그 | (a) JSON stdout + Docker 회전만 (b) + 파일 로그 volume (c) + Azure Monitor / Log Analytics 수집 | **(a)** 로 시작. JSON 포매터는 DAY 코드에 아직 없어 구현 발주가 필요(§2-2). 환경 구분 필드(`app_env`)를 로그에 싣기 |
| D11 | 백업 | PostgreSQL · Redis · Blob · `ENCRYPTION_KEY` | PG = 관리형 자동 백업(설정값은 확인 안 됨). **같은 서버 복원은 서버 단위**라 `day_prod` 만 되돌리려면 스키마 단위 `pg_dump -n day_prod` 를 따로 둘지 정할 것. Redis = 잃어도 되는 것만 둔다(쓰기 큐는 DB `external_outbox`, `R:10`) → 백업 불필요 추천. Blob = soft delete 여부. `ENCRYPTION_KEY` = Vault(D7) |
| D12 | 롤백 | (a) 이미지 이력 기반 이전 digest 재배포(같은 workflow 에 `commit_sha`) (b) centurion 식 caddy-only 비상 복구까지 | **(a)** 기본 + migration 은 되돌리지 않는 방향(forward-only)인지 정할 것. (b) 를 쓸 거면 project 단위(해당 환경 api 만 503)로 |
| D13 | 운영 KOS 쓰기 `KOS_TRIAL_WRITES_ON_LIVE` | (a) prod 첫 배포는 꺼둠, 데모 지점 실물 확인 후 켬 (b) 처음부터 켬 | **(a)** — 기본 꺼짐 · 「데모 지점 실물 확인 뒤에만 켠다」가 코드 계약(`D:config.py:90-94` · `D:backend/day/emr/kos/writes.py:18-28` · `D:backend/day/emr/factory.py:98`). dev 서버는 데모 연결만 동기화라 이 값이 의미 있는 곳은 prod 뿐. 켜는 방법 = `config/prod.env` PR → prod 배포. 스위치가 하나라 다섯 동작(다시 호출 · 시작 취소 · 완료 취소 · 귀가 대기 1·2)을 한꺼번에 연다 — 동작별로 열 필요가 있는지도 함께 |
| D14 | 배포 시간 | prod 배포 가능 시간대 | 진료 시간 밖 추천(§2-2) |
| D15 | Azure 쪽 준비 요청 | VM 이 놓일 VNet/subnet(관리형 PG private 접근) · NAT · NSG · Key Vault · ACR 권한 · OIDC identity | 누가 만들지(centurion 은 Bicep · `infra/azure/`) · DAY 도 Bicep 으로 둘지 정할 것 |

---

## 4. 확인 못 한 것

- **DAY 실제 메모리 사용량** — 원천 수치는 예상(상한)이고 실측 없음. 두 벌이 4GB 에 들어가는지는 첫 배포 후 실측이 필요.
- DAY VM 이 놓일 **subnet · NAT Gateway · 공인 IP** — 관리형 PostgreSQL 이 private 접근이면 VNet 연결이 필요(centurion 은 기존 `vnet-centurion-dev` 재사용, `C:deployment-baseline.md:11-12,33-35`). DAY 용 서버의 네트워크는 문서에 없음.
- 관리형 PostgreSQL 의 **백업 보존 기간 · PITR 설정**, DB 계정 권한(CREATE SCHEMA 가능 여부).
- **KOS 가 나가는 IP 를 제한하는지** — 내부 API 의 UA 차단(`S:212`)은 확인됨, IP 허용 목록은 확인 안 됨.
- DAY 레포(`MediSolveAIDev/CENTURION_DAY`)의 GitHub plan · Environment 설정 — centurion 과 같은 org 라 Team plan 제약이 같을 가능성이 높지만 DAY 레포에서 직접 확인하지 않음.
- DAY 코드의 **신뢰 프록시(X-Forwarded-For) 처리** — Caddy 뒤에서 클라이언트 IP · scheme 을 어떻게 읽는지 검색하지 않음.
- **Blob · APNs 구현** — 코드에 Blob 클라이언트 없음, APNs 는 모델 칼럼(`D:backend/day/models/misc.py:114-116`)만. 배포 env 에 들어갈 비밀값 목록은 이 둘이 구현돼야 확정.
- centurion prod 의 `LOG_FILE_PATH=/app/logs/*.json` 이 어느 volume 에 남는지 — compose 에 `/app/logs` mount 가 보이지 않음(`C:compose.yaml`).
- `Caddyfile` 에서 두 사이트 블록 · 공용 인증서 volume 구성은 centurion 에 선례가 없어 문서 근거가 아니라 Caddy 일반 동작에 기댄 설계다.
