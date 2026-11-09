# 재검수 — #233 H1 · H2 · M1 · M2 (2026-11-09)

읽기 전용(수정 · 커밋 없음) · `day-local` 5개 Up 그대로. 대상 = 같은 워크트리 미커밋 diff · 작성 리포트 `backend-233-fix-report.md`.

## 판정: **PASS** — 네 건 모두 닫힘. 머지를 막는 것 없음. 남은 것은 첫 실물에서 확인할 두 가지(권한 · run-command 충돌 문구).

| 명령 | 결과 |
|---|---|
| `uv run pytest -m "not infra" -q` | **388 passed** · 161 deselected |
| `ruff check backend scripts` | 통과 |
| `shellcheck scripts/deploy/*.sh scripts/*.sh` | 통과 |
| `actionlint` | 통과 |

`scripts/test.sh`(infra)는 돌리지 않았다(작성자 549 passed).

## 항목별

| | 판정 | 근거 |
|---|---|---|
| **H1** DB TLS | PASS | `session.py _check_tls`: `sslmode` · `sslrootcert` 거부 · `DATABASE_TLS_REQUIRED=true` 면 `ssl=verify-full` 만 · verify 모드면 `PGSSLROOTCERT` 파일이 있어야 한다. 앱(api factory · worker)은 기동 때, alembic 은 `validated_database_url` 에서 같은 검사를 탄다(`get_database_settings()` 도 같은 `Settings` 라 칸이 있다). `deploy/config/{dev,prod}.env` 에 두 줄. migrate 서비스도 `./config/<env>.env` 를 읽는다(migrate-prod 는 묶음의 config). `day_vm.py` 가 Key Vault URL · config 값을 검사한다. 앞 검수의 실험 결과(`ssl=verify-full` + `PGSSLROOTCERT` 만 됨)와 맞다. 작성자 실물(터널 · 이미지 둘 다 `pg_stat_ssl=true` · IP 이름 불일치 거부) 증거 인정 |
| **H2** 복구 다운그레이드 | PASS | `_write_private` 의 `.previous` 회전을 뺐다. `snapshot_environment` 가 materialize · 파일 설치 **전에** opt · app.env · compose.env 를 뜨고, 그 뒤에야 `RECOVER_ENV` 가 켜진다. 지금 것이 없으면 옛 사본을 지운다 → 두 판 전 것이 남지 않는다. `recover` 는 셋이 다 있을 때만 되돌린다. 비-dry 경로 테스트(가짜 docker · N/N-1)가 있다 |
| **M1** dev 이력 · digest | PASS | `require_dev_history`: dev 이력의 그 SHA 이미지 == `$image` 가 아니면 `image-differs-from-dev-history` · 없으면 `sha-not-deployed-to-dev`. prod deploy 는 맨 앞(edge · 파일보다 먼저), migrate 도 같은 함수를 쓴다 |
| **M2** 대기 취소 | PASS | group 이 워크플로마다 넷(`day-deploy-dev` · `-prod` · `day-migrate-prod` · `day-rollback-<env>`) · VM `flock -w 1800` · run-command `Conflict`/`in progress` 면 30초 × 60 재시도 · 문서에 Re-run 안내. 워크플로마다로 나눈 이유(prod group 하나면 migrate 대기가 deploy 대기에 밀린다)도 맞다 |
| 덤 L4 | PASS | `wait_healthy` 가 마감까지 기다린다 |
| 테스트 분리 | PASS | 새 `test_db_tls.py` · `test_day_vm.py` 는 DB 없음(non-infra 388 에 포함) · 실제 DB 확인은 테스트에 넣지 않았다 |

## 새 모순 · 작은 것 (막지 않음)

1. **group 을 나눈 결과**: deploy-dev 와 rollback-dev(또는 deploy-prod 와 rollback-prod)가 동시에 돌 수 있다. VM 단계는 flock 이 줄 세우고, 뒤에 오는 `record` 는 돌고 있는 이미지가 다르면 `running-image-differs` 로 멈춘다 → 이력이 틀리게 남지는 않는다. 다만 「나중에 끝난 쪽이 VM 을 차지」하므로 롤백과 배포를 같이 돌리지 않는다는 한 줄을 문서에 두면 좋다.
2. `DAY_VM_TEST_ROOT` 는 운영 스크립트 안의 테스트 구멍이다(root 확인 · flock 을 건너뛴다). run-command 에는 이 env 가 없어 실해는 없다. 원하면 `DAY_VM_TEST_ROOT` 가 있을 때 `/etc` · `/opt` 를 쓰지 못하게 막는 정도.
3. run-command 충돌 오류 문구(`conflict|in progress`)는 실물로 확인하지 못했다(작성자도 같은 말) — 그 밖의 오류는 바로 실패하니 안전한 쪽이다.

## Azure 권한 대조(`infra.azure`)

| 호출 | 필요한 권한 | 받은 권한 | 판정 |
|---|---|---|---|
| `Azure/login`(OIDC · `environment:<env>` subject) | federated credential 둘 | `repo:MediSolveAIDev/CENTURION_DAY:environment:{dev,prod}` | 맞음 — 워크플로 job 이 `environment:` 를 쓴다 |
| `az acr login` · `az acr repository show-tags` · `show` | 데이터 평면 pull/push(AcrPush 에 들어 있음). `--name` 으로 레지스트리를 찾을 때 ARM `registries/read` 도 쓴다 | AcrPush 만 | **대체로 OK · 첫 실물에서 확인** — ARM 조회가 안 되면 az 가 `<name>.azurecr.io` 로 짐작해 넘어간다(경고). centurion 도 같은 공용 ACR 에 같은 명령을 쓴다. 실패하면 ACR 에 Reader 를 주거나 `--name` 대신 login server 를 쓴다 |
| `docker build` · `docker push` | AcrPush | 있음 | OK |
| `az vm run-command invoke` | `virtualMachines/runCommand/action` | VM 에 Virtual Machine Contributor | OK. ACR 은 다른 RG(`rg-centurion-shared`)지만 run-command 는 `DAY_RESOURCE_GROUP` 의 VM 만 부른다 |
| `az account set`(login 의 subscription-id) | 그 구독 안 어딘가의 역할 | VM 범위 역할 | 대체로 OK — 리소스 범위 역할만 있어도 구독이 보인다. 첫 실물에서 확인 |
| VM: IMDS → `oauth2/exchange` → `docker pull` | AcrPull | 있음(실측 200) | OK |
| VM: Key Vault `GET secrets/day-<env>-*` | Key Vault Secrets User(RBAC) · 방화벽이 VM 서브넷 허용 | 있음(실측 200) | OK |
| 그 밖 az 호출 | — | — | 워크플로 · 스크립트에 위 말고 az 호출이 없다(grep). 모자란 권한 없음 |

준비 쪽 알림: Key Vault 비밀 여섯 개(`day-{dev,prod}-{database-url,redis-url,encryption-key}`)와 `DATABASE_URL` 의 `?ssl=verify-full` 은 사용자가 넣는다. NSG 80/443 출처 제한이 그대로면 Caddy ACME(HTTP-01 · TLS-ALPN-01)가 인증서를 못 받고, runner 의 외부 HTTPS 확인도 실패한다 → 사용자 결정 대기 항목과 같다.

## 남은 것

- 첫 실물에서: `az acr` 의 AcrPush 만으로 되는지 · run-command 충돌 문구 · 비-dry 경로 전체.
- NSG 80/443 공개 결정(인증서 · 외부 확인의 전제).
- 정본 deployment.md 차이 반영(작성 리포트 표 그대로) — planner 몫.
