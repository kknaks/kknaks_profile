# 재검수 — KOS 주소 3개 → Key Vault (2026-11-09)

읽기 전용(수정 · 커밋 없음) · `day-local` 5개 Up 그대로. 대상 = 워크트리 미커밋 diff · 작성 리포트 `backend-233-kos-kv-report.md`.

## 판정: **PASS** — 막는 것 없음

| 확인 | 결과 |
|---|---|
| `git grep -n "kos-solution"` | **0건**. 작업 트리 전체(`.git` · `.venv` 와 gitignore 된 사용자 `deploy/local.env` 제외)에서도 0 |
| 세 이름을 쓰는 곳 전수 | 앱: `day/emr/kos/client.py KosEndpoints`(pydantic env · 기본값 빈칸 · 쓸 때 `require()` → `KosError`, 이름만) · `rstrip("/")` 라 끝 `/` 도 괜찮다. 로컬 `compose.local.yaml:21-23` `${…:-}` · `local.env.example:28-30` 빈칸. 서버 `deploy/config/{dev,prod}.env` 는 주석만(값 없음). 배포 `day_vm.py SECRETS` 세 줄. 문서 `deployment.md:95-97` 이름 · 모양만. 테스트는 `.test` 자리 값뿐 |
| KV → env 경로 | Key Vault `day-<env>-kos-{open-api,internal-api,web}-base` → `SECRETS` → `/etc/day/<env>/app.env`(root 0600) → compose `env_file` 둘째 줄 → `KosEndpoints`. compose.env 에는 들어가지 않는다(테스트). migrate · migrate-prod 도 같은 materialize 를 탄다 |
| dry-run 가림 | `vm-deploy.sh deploy prod` · `migrate prod` dry-run 에 `KOS_*='<key-vault:day-prod-kos-…-base>'` 셋 · 자리 값 `dry-run.invalid` · `kos-solution` 안 나옴 · `/etc/day` 안 생김(직접 돌림) |
| 누락 시 중지 | Key Vault 에 없음 → `key-vault-read-failed secret=<이름>` · 비었음 / https 아님 / 사용자 정보 · 쿼리 있음 → `secret-kos-base-must-be-https-url key=<이름>`(값은 메시지에 없음) · Git config 에 넣으면 `FORBIDDEN_CONFIG_KEYS`(= `SECRETS` 를 따름)로 `config-key-forbidden`. 모두 materialize 단계라 컨테이너는 바뀌지 않고, 복구는 H2 사본(실패 직전) 기준 |
| 로컬 example | 세 칸 빈칸 · 「사용자에게 받는다」 — 계약 테스트가 지킨다 |
| 테스트 분리 | 새 · 바뀐 테스트(`tests/deploy/*`)는 DB 없음 → non-infra 409 에 포함 |
| `uv run pytest -m "not infra" -q` | **409 passed** |
| ruff · shellcheck · actionlint | 모두 통과 |

## 남은 것 (막지 않음)

1. **사용자 준비**: Key Vault 비밀이 여섯 개 늘었다(`day-{dev,prod}-kos-{open-api,internal-api,web}-base`). 다 넣기 전에는 dev 배포가 env 만들기에서 멈춘다(의도된 동작).
2. 정본 mediness `deployment.md` 「환경별 env」의 KOS 주소 「config」 → 「Key Vault」 — planner 몫.
3. 이미 커밋된 git 이력에는 옛 주소가 남아 있다 — 사용자 결정대로 둔다. 레포 밖(오케스트레이션 리포트 · 조사 문서)은 이번 범위가 아니다.
4. KOS 주소는 비밀이 아니라 「레포에 두지 않을 값」이다 — dry-run 가림 · 로그에 안 찍힘으로 충분. 앱 `KosError` 메시지도 이름만 낸다.
