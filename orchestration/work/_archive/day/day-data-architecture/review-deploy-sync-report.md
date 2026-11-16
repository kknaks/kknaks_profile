# review-deploy-sync — deployment.md ↔ #233(937dbb68) · 실제 Azure 검수 (읽기 전용)

**결론: PASS(조건부) — 아래 「남은 것」 ①② 두 줄은 사실과 어긋나므로 커밋 전에 고치는 게 맞다.** ③ 은 확인만.

대상: mediness 미커밋 diff(`deployment.md` · `40-architecture/README.md` 1줄 · `log.md` 1행) ↔ 지시 · planner 리포트 · 코드 937dbb68(`docs/development/deployment.md` · `.github/workflows/*` · `scripts/deploy/*` · `deploy/*`) · `day.json` `infra`(`vm` · `azure`).

## 확인한 것 (코드 · 실물과 일치)

| 항목 | 결과 |
|---|---|
| ssl · CA | ✓ `day_vm.py` — `ssl=verify-full` 만 허용(`sslmode` · `sslrootcert` 거부) · 기본 설정 `DATABASE_TLS_REQUIRED=true` · `PGSSLROOTCERT=/etc/ssl/certs/ca-certificates.crt` |
| Key Vault 비밀 이름 | ✓ `SECRETS` 맵 `day-<env>-database-url` / `-redis-url` / `-encryption-key` → 6개 |
| OIDC subject | ✓ 코드 docs 84행 · day.json `azure.deployer` = `repo:MediSolveAIDev/CENTURION_DAY:environment:{dev,prod}` · 워크플로 job 이 `environment:` 사용 |
| concurrency | ✓ `day-deploy-dev` · `day-deploy-prod` · `day-migrate-prod` · `day-rollback-<env>` + `vm-deploy.sh` `flock -w` + `day-deploy.sh` run-command 충돌 재시도(Conflict · in progress) |
| 승인 · dev 이력 · revision | ✓ `migrate-prod.yaml` 확인 문자열 `migrate day_prod` · Environment `prod` · `require_dev_history`(dev `history.jsonl` 의 SHA · 같은 digest) · `revision-gate`(DB current = 이미지 head) · prod 배포도 `require_dev_history` · 롤백 입력 = `/etc/day/<env>/history.jsonl` 의 SHA |
| Actions 변수 | ✓ 8개 이름 = 워크플로 `vars.*` 와 동일 · secrets 없음 |
| KV · NSG · 리소스 이름 | ✓ `<Key Vault>` · 방화벽 VM 서브넷만 · RBAC · VM identity Secrets User · 사용자 Secrets Officer · `<공용 ACR>`(`<공용 RG>`) · `<RG>` · `nsg-<VM>` 22 한 곳 · 80/443 공개 · `<배포 앱>` · VM identity AcrPull — day.json 과 전부 일치 |
| 비밀값 · IP · ID 없음 | ✓ grep — IP · GUID(client id) · ssh 키 이름 · 터널 포트 · 별칭 0건. day.json 의 `AZURE_CLIENT_ID` 값은 옮겨 적지 않음 |
| 준비됨 / 남음 | ✓ 남음 = GitHub Environments · Actions 변수 · KV 비밀 6 · DNS(`dig` 실측 둘 다 미등록) — 지시와 같음 |
| 머리말 · env.py 문장 · README 줄 | ✓ 앞 검수의 글귀 셋 반영(env.py 는 `pg_namespace` 확인 뒤 생성 · `IF NOT EXISTS` 는 offline) |
| 미결 「승인 수단」 닫힘 | ✓ 구현 사실과 같음 · 승인자(Environment reviewer)는 plan 조건으로 남겨 둠 — 발명 없음 |
| lint `--strict` | ✓ 0 error · log.md `arch-change` 1행 요약이 diff 와 맞음 |

## 남은 것

1. **VM 행 「Docker · 로그 회전은 아직 없음」 — 실물과 어긋남.** `day.json` `vm.installed` = "2026-11-09 Docker 29.9 · compose v5.7 · python3.12 · 로그 회전(json-file 10m×5) · <VM 사용자> docker 그룹". 즉 이미 설치됨. 「준비됨 — Docker · compose · 로그 회전 설치됨(2026-11-09)」 으로. (compose 의 `json-file 10m` 로그 드라이버와도 맞음.)
2. **머리말 마지막 줄 「DAY 레포에는 배포 workflow(`.github/`) · 배포용 compose 가 없다」 — 낡음 · 같은 머리말 윗줄과 모순.** 937dbb68 에 `.github/workflows/{deploy-dev,deploy-prod,migrate-prod,rollback}.yaml` · `deploy/compose.yaml` · `compose.edge.yaml` · `scripts/deploy/*` 가 있다. 그 문장을 지우거나 「#233 으로 들어옴」 으로.
3. **「ACR Reader」(ACR 권한 · 배포 계정 행) — 실물 근거 없음.** `day.json` `azure.deployer` 는 AcrPush · Virtual Machine Contributor 만. 출처는 지시문 · review-233 의 "ARM 조회 실패하면 Reader 를 주거나"(조건부). 실제 부여됐으면 day.json 에 추가, 아니면 「AcrPush(+ 필요 시 Reader)」 로.

## 기록만

- 코드 docs 81행은 「NSG 22 차단」 인데 실물은 22 를 한 출처에 열어 둠 — 정본(mediness)은 실물 쪽을 적었고 사용자 결정으로 명시돼 있어 모순 아님. 코드 docs 쪽 갱신은 DAY 레포 몫.
