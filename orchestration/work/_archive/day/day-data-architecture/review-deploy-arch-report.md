# 리뷰 리포트 — 40-architecture/deployment.md (2026-11-08)

**대상**
- mediness 워크트리(미커밋): `products/day/40-architecture/deployment.md`(새 파일) · `system.md` · `README.md` · `log.md` diff

**기준**
- 원천 `system/README.md` 「배포 결정」(사용자 2026-11-08)
- 조사 `researcher-deploy-report.md` §1 ~ §4 · D1 ~ D15
- 작성 리포트 `planner-deploy-arch-report.md`
- DAY 코드 `CENTURION_DAY/day-data-architecture`(HEAD `8f26612f`)
  - `backend/common/config.py`
  - `deploy/local.env.example`
  - `runtime/health.py`
  - `emr/kos/writes.py`

lint `--strict` → 0 error · `products/day/` 경고 0.

## 판정: WARN

다음은 맞다.
- 사용자 결정 9줄이 빠짐 · 바뀜 없이 들어갔다.
- 지은 값이 없다(이름 · IP · 리소스 그룹 · Key Vault · identity 는 전부 「미정」).
- 수치 · 경로 · 별칭은 모두 조사 리포트에서 왔다.
- env 이름이 코드와 같다.
- 미결 8줄은 정직하다.

다만 **흐름에 빈칸이 셋 있다**.
- prod 「같은 SHA」를 만드는 브랜치 갱신 방식(W1)
- 롤백을 시작하는 길(W2)
- prod migration 과 배포의 순서(W3)

**사용자 준비 목록에는 GitHub 쪽이 빠졌다**(W4).

## 사용자 결정 ↔ 문서

| 원천 「배포 결정」 | deployment.md | 판정 |
|---|---|---|
| VM 한 대(2/4) · 관리형 PG 한 대 · 스키마 `day_dev` / `day_prod` | 결정 요약 · 그림 · env 표 | 같음 |
| 브랜치 `dev`(← `v2-dev`) · `prod` 새로 · 들어가면 그 환경 배포 · prod = dev 에서 확인한 같은 이미지 | 결정 요약 · 흐름 표 「시작」 · 「이미지」 | 같음 — 조사 D5(b) 「prod 수동」과 다른 점은 원천을 따랐다(작성 리포트 「주의」 · 맞다) |
| 도메인 `day-dev.medisolveai.com` · `day.medisolveai.com` · DNS 사용자 | 결정 요약 · 그림 · 준비 목록 | 같음 |
| Caddy · ACME · 80/443 · SSE | 결정 요약 · 그림 아래 · 준비 목록 NSG | 같음 |
| 백업 기본값만 | 결정 요약 · 미결 「PG 백업 설정」 | 같음 |
| 배포 시간 제한 없음 | 결정 요약 · 흐름 아래 | 같음 |
| Azure 권한 = 사용자 | 준비 목록 | 같음 |
| 그 밖 조사 추천 — project 셋 · redis 환경마다 · dev 상한 낮춤(실측 · 모자라면 2/8) · 공용 ACR · migration dev 자동 / prod 승인 · Key Vault · JSON 로그 · 롤백 = 이전 이미지 · prod 첫 배포 `KOS_TRIAL_WRITES_ON_LIVE=false` | 각 절 | 같음 |

## 발명 여부

- 메모리 상한(prod 1,792 · dev 960 · caddy 50 · ≈ 2,802 · 남는 ≈ 1.2GB)은 조사 L100-105 에서 왔다.
- `/etc/day/{dev,prod}` · `day-dev-api` · `day-prod-api` 별칭은 조사 L88-89 에서 왔다.
- `config/{dev,prod}.env` 는 조사 D7 · D13(centurion `deploy/config/prod.env` 모양) 에서 왔다.
- redis 설정은 조사 §2-1 에서 왔다.
- ACR 은 「회사 공용」으로만 적었다. 조사의 실제 이름 `<공용 ACR>` 를 옮기지 않았고, repo 는 「미정(예 `day-api`)」이다.
- 문서 스스로 「아직 아무것도 만들지 않았다 · `.github/` · 배포 compose 없음」이라 적었다. 코드도 그렇다(`.github` 없음 · `deploy/` = `compose.local.yaml` · `Dockerfile` · `local.env*`).

## env 이름 ↔ 코드

| 문서 | 코드 | 판정 |
|---|---|---|
| `APP_ENV` dev / prod | `config.py:23` `Literal["dev","prod"]` · L150-152 prod ↔ `day_prod` 검사 | 같음 |
| `DB_SCHEMA` · `DATABASE_URL` · `REDIS_URL` · `ENCRYPTION_KEY` · `DAY_ADMIN_EMAILS` · `KOS_TRIAL_WRITES_ON_LIVE` | `Settings` 칸 이름 | 같음 |
| `KOS_OPEN_API_BASE` · `KOS_INTERNAL_API_BASE` · `KOS_WEB_BASE` | `local.env.example` · `emr/kos/client.py` `KosEndpoints` | 같음 |
| `SYNC_*` · `OUTBOX_*` · `EMR_HTTP_TIMEOUT_SECONDS` · `HOSPITAL_TIMEZONE` | `Settings` 칸 | 같음 |
| `DAY_LOCAL_*` · `DAY_SEED_*` 는 배포 env 에 안 넣음 | `local.env.example` 에만 | 맞음 |
| 헬스 `/health/live` · `/health/ready`(DB · Redis) | `runtime/health.py:3-4 · 56` | 같음 |

## WARN

### W1. prod 「같은 SHA」는 브랜치를 fast-forward 로만 올릴 때 성립한다 — 문서에 없다
흐름 표 「이미지」는 prod 를 이렇게 정한다. 「빌드하지 않는다 — dev 에서 배포한 같은 SHA 만 · ACR 에 없으면 중지」. 그리고 시작은 「`prod` 브랜치 push」다.

그런데 `prod` 를 merge commit(또는 squash)으로 올리면 prod 머리의 SHA 는 dev 에서 빌드한 SHA 와 다르다. 그러면 ACR 에 없어서 **매번 중지**한다.

고칠 방향: 「`prod` 는 `dev` 의 확인된 commit 으로 fast-forward 만(merge · squash 금지 · 브랜치 보호로 강제)」을 흐름 표나 준비 목록에 적는다. 또는 「prod 머리의 tree 가 dev 배포 SHA 와 같으면」처럼 이미지를 찾는 기준을 바꾼다. 어느 쪽이든 정하지 않으면 첫 prod 배포가 막힌다.

### W2. 롤백을 시작하는 길이 없다
표 「롤백 = 이력의 이전 이미지(SHA)로 다시 배포」. 그런데 배포는 push 로만 시작한다. 이전 SHA 로 다시 배포하는 방법이 없다.

조사 D12 의 추천은 「같은 workflow 에 `commit_sha` 입력」이다. centurion 은 `workflow_dispatch` + 선택 `commit_sha`(조사 L18 · L44)다.

고칠 방향: 「push 배포에 더해 수동 실행(`workflow_dispatch` · 환경 · `commit_sha`)으로 이전 이미지 재배포」를 흐름 표 롤백 줄에 적는다. 이것을 쓰면 브랜치를 되돌리지 않고 VM 만 이전 이미지가 되므로, 다음 push 와의 관계(브랜치 머리 ≠ 실행 중 이미지)도 한 줄 적는다.

### W3. prod migration 과 prod 배포의 순서가 그림 · 표에서 흐리다
그림은 「prod 배포 → head 확인 → (migration 은 따로) → up」이고, 표는 「배포는 head 확인만(아니면 중지)」이다. 그러면 새 revision 이 있는 prod push 는 항상 중지된다.

따라서 순서는 「① 승인된 prod migration 실행(같은 SHA 이미지로) → ② prod 배포(이제 head 맞음)」여야 한다. 그런데 그림의 Note 위치가 그 반대처럼 읽힌다.

실행 수단은 미결에 정직하게 있다. 고칠 방향: 순서 한 줄(① → ②)과 「① 이 쓸 이미지 = 같은 SHA」를 흐름 표 migration 줄에 적는다.

### W4. 사용자 준비 목록에 GitHub 쪽이 빠졌다
목록은 Azure 쪽 8줄이다. 다음 GitHub 쪽 준비가 없다.
- **브랜치**: `v2-dev` → `dev` 이름 바꾸기 · `prod` 새로 만들기 · `prod` 보호(누가 push 할 수 있나 — push = prod 배포 · W1 의 fast-forward 강제)
- **Actions 변수**: tenant · subscription · client id · VM 이름 · 리소스 그룹(값 미정)
- **배포 workflow · 배포 compose · Caddyfile 자체** — 지금 레포에 없다. 이 문서는 구조이고, 만드는 것은 구현 발주 몫이다.

조사 D5 의 「prod 실행자 허용 목록」도 이 브랜치 보호가 대신하게 된다.

고칠 방향: 준비 목록에 「GitHub(사용자)」 줄 둘을 더하고, 미결에 「배포 workflow · compose · Caddyfile 구현 발주」 한 줄을 더한다.

## 참고 (지적 아님)

- 조사 D13 에는 「스위치가 하나라 다섯 동작(다시 호출 · 시작 취소 · 완료 취소 · 귀가 대기 1 · 2)을 한꺼번에 연다」는 주석이 있다. env 표 비고에는 없다. 코드(`emr/kos/writes.py:17-18 · 56`)도 스위치 하나다. 켤 때 알아야 할 사실이라 비고에 반 줄 더하면 좋다.
- `system.md` · `README.md` · `log.md` 변경은 맞다. 「배포는 나중」 줄 → deployment.md 연결 · Key Vault + Git config · VM 노드 「dev · prod 같이」.
