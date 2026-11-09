# backend 리포트 — #233 코드 검수 반영 H1 · H2 · M1 · M2 (2026-11-09)

- 같은 워크트리 `CENTURION_DAY/day-data-architecture` · `8f26612f` 위 **미커밋**(커밋 · push 안 함). 기준 = `review-233-code-report.md`.
- 사용자 `day-local`(11040 ~ 11043) 5개 Up 그대로(시작 · 끝 확인). 터널은 코디가 연 것을 썼고 건드리지 않았다.
- 실제 DB 에는 **읽기만**(SELECT 1 · current_schema · pg_stat_ssl · current_user) — 쓰기 · migration 없음. 비밀번호는 `~/.pgpass` 에서 메모리로만 읽었다(출력 · 파일 · 이 리포트에 없음). 실제 서버 · 계정 이름도 저장소에 넣지 않았다(grep 0).

## H1 — DB TLS verify-full 이 asyncpg 0.32 에서 실제로 되게

| 고친 곳 | 내용 |
|---|---|
| `backend/common/db/session.py` `_check_tls` · `check_database_url_at_startup` | URL 에 `sslmode` · `sslrootcert`(libpq 이름)가 있으면 거부. `ssl=verify-full`/`verify-ca` 면 env **`PGSSLROOTCERT` 가 있고 파일이 있어야** 한다. `DATABASE_TLS_REQUIRED=true` 면 `ssl=verify-full` 이 아닌 URL(없음 · `require` · `prefer`)로 뜨지 않는다. 메시지에 URL · credential 없음 |
| `backend/common/config.py` | `database_tls_required: bool = False`(로컬 compose 는 TLS 없는 PG) |
| `backend/runtime/main.py` · `runtime/worker.py` | **기동 때 검사** — api factory · worker/scheduler 진입점이 `check_database_url_at_startup`(첫 쿼리까지 미루지 않음). alembic 은 시작하자마자 `validated_database_url` 을 부르므로 같은 검사를 탄다 |
| `deploy/config/{dev,prod}.env` | `DATABASE_TLS_REQUIRED=true` · `PGSSLROOTCERT=/etc/ssl/certs/ca-certificates.crt`(이미지 안 Debian 묶음 · Azure PG 루트 포함) |
| `scripts/deploy/day_vm.py` | `validate_secrets`: Key Vault `DATABASE_URL` 은 `ssl=verify-full` 필수 · `sslmode`/`sslrootcert` 거부. `validate_config`: 위 두 줄이 정확히 그 값이어야 함 |
| `docs/development/deployment.md` | Key Vault `DATABASE_URL` 모양 = `…/<DB>?ssl=verify-full` · CA 묶음 설명 |
| 테스트 | `tests/common/test_db_tls.py`(새 · DB 없음 — libpq 이름 거부 · 필수면 verify-full 아니면 실패 · CA 경로 없음/파일 없음 실패 · 정상 통과 · 로컬 TLS 없이 통과 · **api · worker 기동 실패**) · `tests/deploy/test_day_vm.py`(URL 4종 · config 2종) |

**실물 확인**(사용자 터널 127.0.0.1:15432 · `[day-dev]` 의 host · `.pgpass` 의 day_dev_app):
- 호스트에서 **앱 코드 경로**(`common.db` · `DATABASE_TLS_REQUIRED=true` · `?ssl=verify-full` · `PGSSLROOTCERT`=macOS 시스템 묶음)로: `SELECT 1 = 1` · `current_schema = day_dev` · `pg_stat_ssl.ssl = True` · `current_user = day_dev_app`. TCP 만 터널로 보내고(프로세스 안 이름 → 127.0.0.1) 인증서 이름 확인은 실제 서버 이름으로 했다(`hostaddr` 와 같은 뜻).
- **음성**: 같은 설정으로 이름을 `127.0.0.1` 로 주면 `SSLCertVerificationError … IP address mismatch` — verify-full 이 실제로 검증한다.
- **서버 이미지 경로**: `day-backend:local` 이미지에 고친 `backend/` 를 붙여(읽기 전용 마운트) `PGSSLROOTCERT=/etc/ssl/certs/ca-certificates.crt` 로 같은 확인 → `IMAGE OK 1 day_dev True`. 비밀번호는 `docker run -e DATABASE_URL`(값 없이 — 부모 env 상속, argv 에 안 나옴)으로만 넘겼다.
- 증거: scratchpad `h1-live-evidence.txt`(4줄 · 비밀 없음).

## H2 — 실패 복구가 두 판 전 이미지로 내려가지 않게

- `day_vm.py _write_private` 에서 `.previous` 돌리기를 **뺐다**.
- `vm-deploy.sh snapshot_environment`(새): 이번 배포가 아무것도 바꾸기 **전에** `/opt/day/<env>` → `.previous`, `/etc/day/<env>/{app,compose}.env` → `.previous` 를 한 곳에서 뜬다(지금 것이 없으면 옛 사본을 지운다 — 첫 배포).
- 순서: `ensure_edge` → `snapshot_environment` → `RECOVER_ENV` 켬 → `install_environment_files` → `materialize` …. `recover` 는 그 사본(셋 다 있어야)만 되돌린다. app.env 만 쓰고 compose.env 에서 실패한 반쪽 상태도 사본으로 둘 다 되돌아간다.
- **테스트(실제 비-dry 경로)**: `DAY_VM_TEST_ROOT`(테스트 전용 — 파일 자리를 tmp 로 · root · 소유자 · flock 건너뜀) + 가짜 `docker`. 지금 = N, 옛 `.previous` = N-1 로 깔고 Key Vault 이름 오류로 materialize 를 쓰기 전에 실패시키면 → `DAY_DEPLOY_FAILED reason=env-materialize-failed` · `DAY_DEPLOY_RECOVERED` · **compose.env · app.env · compose 디렉터리 = N 그대로** · docker 호출은 `-p day-dev` 만(`test_env_만들기가_쓰기_전에_실패하면_실패_직전_이미지로_돌아간다`).
- 덤: macOS bash 3.2 에서 빈 배열(`"${dry[@]}"` · 소유자 인자)이 `set -u` 로 죽던 것을 `${a[@]+"${a[@]}"}` 로 고쳤다(VM bash 5 에서는 문제없던 것).

## M1 — prod 는 dev 성공 이력 · 같은 digest 만

- `vm-deploy.sh require_dev_history`(새): `/etc/day/dev/history.jsonl`(dev 배포가 외부 HTTPS 까지 성공해야 적힌다)에서 그 SHA 의 이미지를 찾아 `$image` 와 같아야 지나간다. 사유 `sha-not-deployed-to-dev` · `image-differs-from-dev-history`.
- `deploy prod` 는 **맨 앞**(edge · 파일 · env 를 건드리기 전)에서, `migrate prod` 도 같은 함수로(전에는 이미지를 버리고 SHA 만 봤다).
- 테스트: dev 이력 digest 가 다르면 prod 배포가 멈추고 docker 호출 0 · compose.env 그대로 · dev 이력에 SHA 가 없으면 deploy · migrate 둘 다 멈춤 · dry-run 에서 두 중지 줄이 `docker network` 보다 앞.

## M2 — 대기 실행이 다른 워크플로에 밀려 취소되지 않게

- concurrency group 을 **워크플로마다** 나눴다: `day-deploy-dev` · `day-deploy-prod` · `day-migrate-prod` · `day-rollback-${{ inputs.environment }}`(`cancel-in-progress: false`). 이제 migration 중 들어온 prod push 가 dev push 에 밀려 취소되지 않는다. 같은 워크플로 안에서는 새 push 가 대기 중인 옛 push 를 대신한다(최신이 이긴다 — 의도).
- VM 겹침: `flock -n`(바로 실패) → **`flock -w 1800`**(기다림). runner `invoke_run_command`: az 오류가 `Conflict`/`in progress` 면 30초 × 60 회 다시, 그 밖의 오류는 바로 실패.
- 리뷰어가 「dev · prod group 둘」을 말했지만, group 둘이면 같은 prod group 안의 deploy-prod 대기가 migrate-prod 대기를 취소할 수 있어 워크플로마다로 했다.
- 문서: `docs/development/deployment.md` 에 group · `cancelled` 면 Re-run · 재시도 · flock 기다림 · L1(다음 dev migration 전에 prod 승격) · 복구 범위를 적었다.

## 덤 · 남긴 것

- L4 고침: `wait_healthy` 가 api ready 첫 순간 worker 등이 아직이면 바로 실패하던 것 → 마감까지 기다림(`others_running`).
- L2 · L3 · L5 는 손대지 않음(선택).
- run-command 충돌 오류 문구(`Conflict`/`in progress`)는 실물로 확인하지 못했다 — 첫 실물에서 확인.

## 정본 문서(mediness deployment.md) 차이 — planner 몫, 고치지 않음

| 정본 지금 | 구현 · 실물 |
|---|---|
| `DATABASE_URL` 예시 `sslmode=verify-full` | asyncpg 는 `?ssl=verify-full`. CA 묶음은 env `PGSSLROOTCERT=/etc/ssl/certs/ca-certificates.crt`(Git config) · `DATABASE_TLS_REQUIRED=true` 새 일반 설정 두 줄. `sslmode` · `sslrootcert` 는 거부 |
| OIDC federated credential 「브랜치별」 | 워크플로 job 이 GitHub Environment 를 쓰므로 subject = `repo:MediSolveAIDev/CENTURION_DAY:environment:dev` · `…:environment:prod`. 브랜치 제한은 Environment 배포 브랜치 규칙 |
| Key Vault 비밀 이름 없음 | `day-<env>-database-url` · `day-<env>-redis-url`(호스트는 `redis`) · `day-<env>-encryption-key` |
| 「두 환경 배포는 한 concurrency group」 | 워크플로마다 group + VM `flock -w` + run-command 충돌 재시도(M2) |
| prod 승인 세부 미결 | 확인 문자열 `migrate day_prod` · `prod` 브랜치 · Environment `prod` |
| prod = 「dev 에서 확인한 같은 이미지」(지키는 방법 미기재) | dev 성공 이력(외부 HTTPS 까지) 의 SHA · digest 일치 확인 — 배포 · migration 둘 다(M1) |
| (없음) | migrate-prod 는 dev DB revision = 이미지 head 일 때만 → 다음 dev migration 전에 prod 승격(L1) |

## 검증

| 명령 | 결과 |
|---|---|
| `uv run pytest -m "not infra" -q` | **388 passed** |
| `scripts/test.sh -q` | **549 passed**(infra 포함) |
| `uv run ruff check backend scripts` · `ruff format --check` | 통과 · 156 files |
| `shellcheck scripts/deploy/*.sh scripts/*.sh` | 통과 |
| `actionlint` | 통과 |
| dry-run deploy dev/prod · migrate prod | M1 중지 줄이 맨 앞 · 복구 사본은 materialize 전 · `/etc/day` · `/opt/day` 안 생김 — scratchpad `fix-dryrun-evidence.txt` |
| 실제 DB verify-full | 위 H1 — 호스트 · 서버 이미지 둘 다 OK · 이름 불일치는 거부 |
| grep(실제 서버 · 계정 이름) | 저장소 0 |

scratchpad = `/private/tmp/claude-501/-Users-kknaks-orca-workspaces-CENTURION-DAY-day-data-architecture/4fd42c8c-f3ab-42ea-92b0-f13eb573a6bb/scratchpad/`.

## 바뀐 파일(이번)

`backend/common/config.py` · `backend/common/db/session.py` · `backend/common/db/__init__.py` · `backend/runtime/main.py` · `backend/runtime/worker.py` · `deploy/config/dev.env` · `deploy/config/prod.env` · `scripts/deploy/day_vm.py` · `scripts/deploy/vm-deploy.sh` · `scripts/deploy/day-deploy.sh` · `.github/workflows/*.yaml`(group) · `docs/development/deployment.md` · 새 `backend/tests/common/test_db_tls.py` · `backend/tests/deploy/test_day_vm.py` · `backend/tests/deploy/test_deploy_contract.py`.
