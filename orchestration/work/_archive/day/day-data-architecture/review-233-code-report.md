# 검수 리포트 — #233 DAY 서버 배포 코드 (2026-11-09)

- 대상: `CENTURION_DAY/day-data-architecture` · 브랜치 `kknaksss/day-data-architecture` · `8f26612f` 위 미커밋 diff 전부(수정 11 · 새 파일 전부). **읽기 전용** — 수정 · 커밋 없음. 사용자 로컬 compose `day-local` 5개 Up 그대로(시작 · 끝 확인).
- 기준: Issue #233 contract v2 · 정본 mediness `products/day/40-architecture/deployment.md` · 작성 리포트 `backend-233-report.md` · centurion `origin/main` `deploy-stg.yaml` · `manual-app-deploy.sh` · 받은 값 `config/projects/day.json` `infra`.

## 판정

**조건부 통과 — H1 은 머지(= 첫 dev 배포) 전에 고쳐야 한다.** H1 을 그대로 두면 첫 dev 배포가 migration 에서 멈춘다. H2 · M1 은 머지 전에 고치는 쪽을 권한다. 나머지는 문서화하거나 나중에 고쳐도 된다.

## 돌린 것

| 명령 | 결과 |
|---|---|
| `uv run pytest -m "not infra" -q` | **368 passed** · 161 deselected (6.5s) |
| `uv run ruff check backend scripts` · `ruff format --check` | 통과 · 155 files formatted |
| `shellcheck scripts/deploy/*.sh scripts/*.sh` | 통과 |
| `actionlint` | 통과(0 오류) |
| dry-run `DAY_DRY_RUN=1 day-deploy.sh remote deploy dev/prod · migrate prod` | 표식 · env(비밀값은 `<key-vault:day-<env>-…>`) · compose 명령 · gate 출력. `/etc/day` · `/opt/day` 안 생김. run-command 스크립트 **36,905 bytes** |
| asyncpg 0.32 / SQLAlchemy 2.1.8 TLS 실험(아래 H1) · 로컬 이미지 `day-backend:local` 안 CA · HOME 확인 | H1 근거 |
| A6 grep(추적 + 새 파일, `deploy/local.env` 제외 — ignore 확인) | 실제 VM · DB · IP · 계정 이름 0. 나온 것은 ACR 토큰 로그인용 0-GUID · 테스트의 `kv-` 검사 문자열 · `rg-` 단어 일부뿐 · 워크플로 `secrets.` 0 |

`scripts/test.sh`(infra)는 다시 돌리지 않았다. 작성자가 529 passed 로 보고했다.

## 발견

### H1 (High) — DB TLS verify-full 조건이 실제로 맞지 않는다. 문서대로 넣으면 접속이 실패한다

실제 DB 는 공개 꺼짐 · **TLS verify-full** 이고, 정본 표는 `DATABASE_URL` 에 `sslmode=verify-full` 을 쓴다. 그런데 앱 · alembic 은 `postgresql+asyncpg` 이고 TLS 를 따로 다루는 코드가 없다(`common/db/session.py` 는 URL 을 그대로 쓴다). 실험 결과:

| `DATABASE_URL` 쿼리 | 결과 |
|---|---|
| `?sslmode=verify-full`(정본 표 그대로) | `TypeError: connect() got an unexpected keyword argument 'sslmode'` |
| `?ssl=verify-full` | `root certificate file "~/.postgresql/root.crt" does not exist` — asyncpg 0.32 는 verify-full 에서 시스템 CA 로 넘어가지 않는다. 이미지 사용자 `day` 의 HOME `/home/day` 가 없다(`useradd --system`) |
| `?ssl=verify-full&sslrootcert=…` | `TypeError … 'sslrootcert'` — SQLAlchemy 가 쿼리를 kwargs 로 넘긴다 |
| `?ssl=verify-full` + env **`PGSSLROOTCERT=/etc/ssl/certs/ca-certificates.crt`** | 설정 단계를 지나 접속 시도까지 간다(정상) |

이미지에는 `/etc/ssl/certs/ca-certificates.crt`(148개)가 있고 Azure PG 루트(DigiCert Global Root G2 · Microsoft RSA Root CA 2017 · DigiCert Global Root CA)가 들어 있다.
**영향**: 첫 dev 배포가 `dev-migration-failed` 로 멈춘다. `sslmode` 를 빼면 asyncpg 기본 `prefer` 라 검증 없는 TLS 로 접속된다 — 계약 조건(verify-full) 위반을 아무도 모른다.
**고칠 것**: ① `deploy/config/{dev,prod}.env`(또는 Dockerfile `ENV`)에 `PGSSLROOTCERT=/etc/ssl/certs/ca-certificates.crt` ② Key Vault `DATABASE_URL` 은 `…/day?ssl=verify-full` 로 안내(`docs/development/deployment.md:83` 예시 · 정본 표의 `sslmode` 표기) ③ `day_vm.py validate_secrets` 가 `ssl=verify-full` 이 없거나 `sslmode` 가 있으면 거부(지금은 scheme 만 본다) ④ 단위 테스트.

### H2 (High) — 실패 복구가 두 번 전 이미지로 되돌린다(조용한 다운그레이드)

`vm-deploy.sh deploy()` 에서 `RECOVER_ENV` 는 `materialize` **앞**에 켜진다(263행). `day_vm.py _write_private` 는 **쓰는 순간에** 지금 파일을 `.previous` 로 돌린다(214–217행). 그래서 `materialize` 가 쓰기 전에 실패하면(Key Vault 읽기 실패 · 비밀값 모양 오류 · 설정 키 거부 등) 이렇게 된다:
- `/etc/day/<env>/compose.env.previous` · `app.env.previous` 는 아직 **배포 N-1** 의 것이다(배포 N 이 성공할 때 돌린 것).
- `recover()`(232–236행)가 그것을 `compose.env` 로 깔고 `up -d` 한다 → 돌고 있던 N 이 **N-1 이미지로 다시 만들어진다**. 표식은 `DAY_DEPLOY_RECOVERED`.
- prod 면 N-1 이미지가 N 의 schema(head) 위에서 돈다. 이력 · 화면 어디에도 다운그레이드가 드러나지 않는다.
- `app.env` 는 썼는데 `compose.env` 를 쓰다 실패하면 반쪽 상태도 생긴다.

**고칠 것**: 복구용 사본을 `install_environment_files` 처럼 vm-deploy 가 materialize **전에** 스스로 떠 둔다(`/etc/day/<env>` 의 app.env · compose.env → 이번 배포 전용 사본). `recover` 는 그 사본만 되돌린다. 아니면 `_write_private` 의 `.previous` 회전을 빼고 셸 쪽 한 곳에서만 관리한다. 테스트: 「materialize 실패 → recover 뒤 compose.env 의 DAY_IMAGE = 실패 직전 값」.

### M1 (Medium) — prod 배포가 「dev 에서 배포 · 확인한 같은 digest」를 확인하지 않는다

- `deploy prod` 경로(`vm-deploy.sh` 266–274행)는 dev 이력을 보지 않는다. 막는 것은 `check-promotion`(origin/dev 위 commit) · `require-image`(ACR 에 SHA 태그) · head gate 뿐이다.
- 그래서 dev 배포가 헬스 · TLS 에서 **실패한** commit 도 이미지는 ACR 에 남아 있다. migration 이 없는 변경이면 prod 로 그대로 간다. 정본은 「dev 에서 배포 · 확인한 commit」이다.
- `migrate_prod`(288행)는 dev 이력에 SHA 가 있는지만 보고, 찾은 이미지를 버린다(`>/dev/null`). `$image`(ACR 태그에서 다시 푼 digest)와 비교하지 않는다. 태그가 바뀌어 있으면(수동 push 등) 다른 digest 로 migration 이 돈다.

**고칠 것**: `deploy prod` 와 `migrate` 둘 다 `find --history /etc/day/dev/history.jsonl` 결과가 `$image` 와 같아야 지나가게 한다(rollback 의 `rollback-image-differs-from-history` 와 같은 모양). 사유는 `sha-not-deployed-to-dev` · `image-differs-from-dev-history`.

### M2 (Medium) — 한 concurrency group 의 「대기 중」 실행은 새 실행에 밀려 취소된다

네 워크플로가 `group: day-vm` · `cancel-in-progress: false` 다. 이 설정은 돌고 있는 실행만 지킨다. GitHub 규칙상 그룹에는 대기 실행이 **하나만** 남는다. 예: migrate-prod 가 도는 중에 prod push(대기) → 곧이어 dev push → **대기 중이던 deploy-prod 가 취소된다**. 동시 실행은 막히지만(VM `flock -n` 도 있다) 배포가 빠질 수 있다.
**고칠 것**: `deployment.md` 에 「cancelled 면 Re-run」을 적는다. 아니면 dev · prod 를 group 둘로 나누고 VM `flock` 을 `-w <초>` 대기로 바꿔 겹침은 VM 이 막게 한다.

### L(Low) · 확인 필요

- **L1** migrate-prod gate 는 dev current == 이미지 head 를 **엄격히** 본다. 그 뒤 dev 에 새 migration 이 배포되면 앞 SHA 의 prod 승격이 막힌다. 의도에는 맞지만 「다음 dev migration 전에 prod 승격」이라는 운영 제약이 생긴다 → 문서에 한 줄.
- **L2** `migrate_prod` 가 `ensure_edge` 를 부른다(296행). migration 실행이 prod 브랜치 머리의 Caddyfile · edge compose 로 Caddy 를 바꾸거나 reload 할 수 있다 — migration 과 상관없는 부수효과다. 또 migration 은 대상 SHA 가 아니라 **prod 브랜치 머리의 `compose.yaml`** 로 돈다(migrate 서비스 정의가 바뀌는 commit 이면 어긋남).
- **L3** `existing_digest` 가 `az acr repository show-tags` 오류를 `2>/dev/null || true` 로 삼킨다. 권한 · 네트워크 오류가 prod 에서는 `image-missing-for-sha`(오해 소지), dev 에서는 불필요한 재빌드로 바뀐다. 「없음」과 「조회 실패」를 나누는 쪽을 권한다.
- **L4** `wait_healthy` 는 api 가 ready 된 첫 순간 worker · scheduler · redis 가 `Running` 이 아니면 180초를 기다리지 않고 곧바로 `return 1` 한다(207–209행) — 기동이 늦으면 거짓 실패 → 복구.
- **L5** `/health/ready` 응답에 `checks.encryption` 칸이 생겼다(외부 계약 변경 · 계약 W7 범위). probe 마다 DB 조회가 한 번 더 붙는다 — 문제는 없다.

## 계약 · 요구 항목별 확인

| 항목 | 판정 | 근거 |
|---|---|---|
| A1 로컬 prod 모양 | 리포트 증거 인정(재현 안 함) | compose 정의: 호스트 포트 = caddy 뿐 · `day-<env>-api` 별칭 · mem_limit = 표(768/384/384/256 · 384/256/192/128 · 50m) · project 이름 · 네트워크 · volume 환경별 · redis `appendonly` · `noeviction` · maxmemory < mem_limit(`validate_compose_config`) |
| A2 워크플로 | 통과(M1 · M2 남음) | actionlint 0. action pin = centurion 과 같은 SHA(checkout `3d3c42e…` v7.0.1 · Azure/login `a641126…` v3.1.0). 중지 분기 `image-missing-for-sha` · `prod-revision-not-at-image-head` · `dev-revision-not-at-image-head` · `sha-not-deployed-to-dev` 확인 |
| A3 dry-run | 통과 | 직접 돌림 — 비밀값 안 나옴 · 파일 안 생김 |
| A4 JSON 로그 | 통과 | `common/logs.py` · `app_env` 모든 줄 · 단위 테스트 non-infra |
| A5 | 통과 | `AppEnvMissingError`(`model_fields_set` 로 env 존재 판정) · offline SQL 맨 앞 두 줄(`env.py:116-117`) · canary(`EncryptedJSONB` 결과 처리에서 복호화 → 다른 키면 `DecryptionError`) |
| A6 grep | 통과 | 위 |
| A7 | 해당 없음(사용자 준비 + 머지 뒤) | — |
| A8 | 통과 | `AGENTS.md` 에 `v2-dev` 없음 |
| prod 같은 이미지 · 재빌드 없음 · fast-forward | 대체로 통과 · **M1** | prod · migrate · rollback 은 `require-image`(빌드 없음 · digest 로만). `check-promotion`: `forced` 거부 · before 의 자손 · origin/dev 의 조상(fetch-depth 0 이라 원격 브랜치 있음) |
| migration 순서 | 통과 | prod deploy 는 gate 만, migrate-prod 는 수동 · `refs/heads/prod` · Environment prod · 확인 문자열 · dev 이력 · dev revision gate · 운영 중인 prod env 를 건드리지 않음(staged 디렉터리) |
| 롤백 | 통과 | 이력에 있는 SHA · 같은 digest 만 · migration 없음 · 브랜치 머리 그대로 · 실행 브랜치 = 환경 |
| 비밀값 노출 | 통과 | 묶음 = 비밀 아닌 설정만 · runner 에 비밀 없음 · dry-run 은 이름으로 가림 · env 파일 root 0600 · `umask 077` · ACR 토큰은 stdin. 실패 때 로그 끝 15줄이 run-command 출력(→ Actions 로그)으로 나간다 — 지금 코드는 URL · 비밀번호를 찍는 곳이 없다 |
| 실패 복구가 다른 환경을 안 건드림 | 통과 · **H2**(같은 환경 안의 다운그레이드) | `recover` 는 그 project 만. 단 dev 배포의 `ensure_edge` 는 공용 Caddy 를 바꾼다(구조상 불가피 · 정본이 말한 「dev 배포 권한 = prod VM root」) |
| run-command 크기 | 위험 낮음 | 36,905 B. centurion 이 같은 이중 base64 방식으로 더 큰 payload(`app_environment.py` 35.7KB + manifest 5.5KB → ≈ 75KB)를 쓰고 있다. 공식 문서의 스크립트 크기 한도는 찾지 못했다(문서의 4KB 는 출력 한도이고, 출력은 표식 줄만 낸다). runner 의 argv 한 개 한도(128KiB)에도 여유가 있다. 첫 실물에서 확인 |
| Key Vault 비밀 이름 | 통과 | `day-<env>-database-url` · `-redis-url` · `-encryption-key` — Vault 이름 패턴 3–24자. 정본에 없는 이름이라 정본 반영 필요 |
| OIDC subject | 통과 · 정본 수정 필요 | job 이 `environment:` 를 쓰므로 토큰 subject 는 `repo:MediSolveAIDev/CENTURION_DAY:environment:<env>`(origin 확인)가 맞다. 정본의 「브랜치별」은 이 구현에서 로그인이 안 된다 → 정본을 environment 로 고치고, 브랜치 제한은 Environment 배포 브랜치 규칙으로 |
| DB 조건(앱 계정 = 스키마 주인 · migration 도 앱 계정) | 통과 | online migration 은 `pg_namespace` 를 먼저 보고 없을 때만 `CREATE SCHEMA` 를 한다(`env.py:82-88`) → DB `CREATE` 권한 없이도 지나간다. offline 의 `CREATE SCHEMA IF NOT EXISTS` 는 DBA 용이라 영향 없음 |
| DB TLS verify-full · CA | **H1** | 위 |
| 테스트 분리 | 통과 | `tests/deploy/*` · logs · startup · health 는 DB 없음. canary 실제 DB 테스트는 `pytestmark = infra` |
| 앱 기능 변경 없음 | 통과 | 바뀐 것은 기동 조건(APP_ENV) · 로그 모양 · readiness 칸뿐. 화면 · API 업무 경로는 그대로 |

## 남은 것

1. H1 수정(코드 + env + 문서 + 검사) — 머지 전 필수.
2. H2 · M1 수정 권장(머지 전).
3. M2 · L1 문서화. L2–L4 는 선택.
4. 정본 `deployment.md` 고칠 것: `sslmode` → `ssl=verify-full` + `PGSSLROOTCERT` · OIDC subject = environment · Key Vault 비밀 이름 `day-<env>-…` · prod 승인 = 확인 문자열 `migrate day_prod`.
5. 실물에서만 확인되는 것: run-command 비-dry 경로(IMDS · Key Vault · ACR 토큰 교환 · flock · recover) · 스크립트 크기.
