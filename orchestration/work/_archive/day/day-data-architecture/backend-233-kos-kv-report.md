# backend 리포트 — KOS 주소 3개를 레포에서 빼고 Key Vault 로 (2026-11-09)

- 워크트리 `CENTURION_DAY/day-data-architecture` · `937dbb68` 위 **미커밋**. 사용자 결정(2026-11-09): `KOS_OPEN_API_BASE` · `KOS_INTERNAL_API_BASE` · `KOS_WEB_BASE` 는 레포에 두지 않는다.
- `day-local` 5개 Up 그대로 · 사용자 `deploy/local.env`(gitignore)는 열지도 고치지도 않았다.

## 전수조사 (고치기 전)

| 무엇 | 나온 곳 | 처리 |
|---|---|---|
| `git grep -n "kos-solution"` | `deploy/config/dev.env:10-12` · `deploy/config/prod.env:10-12` · `deploy/local.env.example:28-30` — 9줄, 이것뿐 | 서버 config 에서 줄 삭제(Key Vault 로) · 예시는 값 빈칸 |
| 같은 주소 다른 표기(`open-api.kos` · `api.kos` · `app.kos` · 대소문자) | 테스트의 `https://api.kos.test` · `app.kos.test` 자리 값뿐(실제 주소 아님) | 그대로 |
| 세 env 이름 · 칸 이름을 쓰는 곳 | 코드 `backend/day/emr/kos/client.py:59-71`(`KosEndpoints` — 기본값 **빈 문자열** · 쓸 때 `require()` 가 없으면 `KosError`) · `staff_client.py` · `deploy/compose.local.yaml:21-23`(`${…:-}` — 값 없음) · 테스트(`.test` 자리 값) | 바꿀 것 없음 — 코드 기본값에 실제 주소 없음 |
| 문서 · AGENTS.md | 주소 없음 | `docs/development/deployment.md` KV 표에 이름만 추가 |

저장소 밖(오케스트레이션 리포트 · 조사 문서)은 이번 범위가 아니다. 이미 커밋된 git 이력(`937dbb68` 이전 커밋들)에는 옛 줄이 남아 있다 — 이력 다시 쓰기는 하지 않았다.

## 바꾼 것

| 파일 | 내용 |
|---|---|
| `scripts/deploy/day_vm.py` | `SECRETS` 에 `KOS_OPEN_API_BASE → kos-open-api-base` · `KOS_INTERNAL_API_BASE → kos-internal-api-base` · `KOS_WEB_BASE → kos-web-base` 추가 → Key Vault 비밀 `day-<env>-kos-*-base` 가 같은 env 이름으로 `/etc/day/<env>/app.env`(root 0600)에. 기존 경로 그대로: dry-run 은 `<key-vault:day-<env>-kos-…-base>` 로 가림 · Key Vault 읽기 실패면 `key-vault-read-failed` 로 배포 중지 · `FORBIDDEN_CONFIG_KEYS` 가 `SECRETS` 를 따르므로 Git config 에 넣으면 `config-key-forbidden`. 새 검사 `secret-kos-base-must-be-https-url key=<이름>` — 비었거나 https 아님 · 사용자 정보 · 쿼리가 있으면 중지(값은 메시지에 없음) |
| `deploy/config/dev.env` · `prod.env` | KOS 세 줄 삭제 → 「Key Vault 에서 들어간다 · 여기 넣으면 거부」 주석 |
| `deploy/local.env.example` | `KOS_OPEN_API_BASE=` · `KOS_INTERNAL_API_BASE=` · `KOS_WEB_BASE=`(빈칸) · 「사용자에게 받는다(서버는 Key Vault)」 |
| `docs/development/deployment.md` | Key Vault 비밀 표에 세 줄(이름 · env · `https://<호스트>` 모양 · 「사용자에게 받는다」) + 레포에 두지 않음 · 없으면 배포 중지 설명. 주소 값은 쓰지 않음 |
| 테스트 | `tests/deploy/test_day_vm.py`: config 에 KOS 키 3개 거부 · https 모양 15경우(빈 값 포함 — 메시지에 값 없음) · 비밀 이름 · app.env 로만(compose.env 에 없음) · Key Vault 에 없으면 materialize 실패 · out-dir 안 생김 · dry-run 가림. `tests/deploy/test_deploy_contract.py`: **레포 파일(추적 + 새 파일, local.env 제외)에 `kos-solution` 0** · 서버 config 에 KOS `_BASE` 키 없음 · 예시 값 빈칸 |

## 설정이 없을 때

- 서버: Key Vault 에 셋 중 하나라도 없거나 모양이 틀리면 **env 만들기에서 배포 중지**(기존 배포 시작 거부 규칙과 같은 자리 — 그 환경 컨테이너는 바뀌지 않고, H2 복구는 「실패 직전」으로).
- 앱 코드: 바꾸지 않았다 — 기존대로 `KosEndpoints.require()` 가 쓰는 순간 `KosError("KOS endpoints not configured: …")`(이름만).
- 로컬: `deploy/local.env` 에 사용자가 직접 넣는다. 비우면 로컬 worker 동기화 · 로그인이 위 `KosError` 로 실패한다(기존 동작).

## 사용자 준비 추가 (Key Vault)

`day-dev-kos-open-api-base` · `day-dev-kos-internal-api-base` · `day-dev-kos-web-base` · `day-prod-kos-open-api-base` · `day-prod-kos-internal-api-base` · `day-prod-kos-web-base` — 값은 `https://<호스트>`(사용자가 가진 KOS 주소). 정본 mediness `deployment.md` 「환경별 env」 표는 KOS 주소를 「config」로 적고 있다 → planner 가 「Key Vault」로 고칠 것(이번엔 고치지 않음).

## 검증

| 명령 | 결과 |
|---|---|
| `uv run pytest -m "not infra" -q` | **409 passed** |
| `scripts/test.sh -q` | **570 passed**(infra 포함) |
| `ruff check backend scripts` · `ruff format --check` | 통과 |
| `shellcheck scripts/deploy/*.sh scripts/*.sh` · `actionlint` | 통과 |
| dry-run `vm-deploy.sh deploy prod` | app.env 에 `KOS_*_BASE='<key-vault:day-prod-kos-…-base>'` 셋 · 자리 값(`dry-run.invalid`) 안 나옴 · `/etc/day` 안 생김. `day-deploy.sh remote deploy dev` 출력에 `kos-solution` 0 |
| 최종 `git grep -n "kos-solution"` | **0건**(rc 1) |

바뀐 파일: `scripts/deploy/day_vm.py` · `deploy/config/dev.env` · `deploy/config/prod.env` · `deploy/local.env.example` · `docs/development/deployment.md` · `backend/tests/deploy/test_day_vm.py` · `backend/tests/deploy/test_deploy_contract.py`.
