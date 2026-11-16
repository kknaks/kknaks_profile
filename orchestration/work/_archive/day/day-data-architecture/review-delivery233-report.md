# 리뷰 리포트 — Delivery #233 서버 배포 (2026-11-08)

**대상**
- Issue MediSolveAIDev/CENTURION_DAY#233(contract v1 · 코멘트 0)
- `delivery/v2-server-deploy.json` · plan · apply
- 지시 `planner-delivery-deploy-instructions.md` · 작성 리포트 `planner-delivery-deploy-report.md`

**기준**
- `products/day/40-architecture/deployment.md`(DAY-DEPLOYMENT)
- 원천 `system/README.md` 「배포 결정」
- 재확인 `review-deploy-arch-fix-report.md` 남은 것 3
- 레포 `CENTURION_DAY`: `origin/dev` = `8e4fb4b5` · 작업 브랜치 HEAD = `8f26612f`

## 판정: WARN

다음은 맞다.
- deployment.md 가 계약에 빠짐 없이 들어갔다.
- 남은 것 3 이 닫혔다.
- 「하지 않는 것」이 맞다.
- Acceptance 가 「Azure 없이(A1 ~ A6 · A8)」와 「사용자 준비 뒤 실물(A7)」로 나뉘었다.
- 위험 L3 · **승인 라벨 없음**(`delivery-plan:review` · `execution-plan:ready` · `spec-baseline:pending`)이다.

남은 것은 **배포할 앱이 아직 `dev` 브랜치에 없다**는 순서 빈칸 하나(W1)와 가벼운 둘이다.

## deployment.md ↔ 계약

| deployment.md | 계약 | 판정 |
|---|---|---|
| dev push → 빌드 · ACR(40자 SHA) · run-command · migration 자동 · up · 헬스 · TLS | TD2 ① | 같음 |
| prod fast-forward · 빌드 안 함 · 같은 SHA 없으면 중지 · head 확인만 | TD2 ② · A2 | 같음 |
| prod 순서 ① migration(승인 · dev 같은 revision) → ② 배포 | TD2 ③ · A7 「migration 승인 실행 뒤」 | 같음 |
| 롤백 수동(환경 · 이전 성공 SHA) · forward-only | TD2 ④ · rollback | 같음 |
| 한 concurrency group | TD2 끝 | 같음 |
| run-command · Key Vault + Git config → `/etc/day/{env}` · 이력 | TD3 · A3 | 같음 |
| compose 셋 · redis 환경마다(설정 4) · 메모리 상한 표 · 포트 80/443 뿐 · edge 별칭 | TD4 · A1 | 같음 |
| Caddy 두 도메인 · SSE · 인증서 volume | TD5 | 같음 |
| JSON 로그(미결 → 구현) | TD6 · A4 | 들어감 — `app_env` 필드 · 회전 10m × 5 는 조사 D10 · §1(centurion) 값이다 |
| env 이름 · 비밀값 Key Vault · `*.env.example` 만 · prod 첫 `KOS_TRIAL_WRITES_ON_LIVE=false` | TD10 · A6 · predeploy | 같음 |
| 값 짓지 않음(VM · RG · IP · Key Vault · identity) | TD1 · A6 | 같음 |

**deployment.md 에 없는데 더한 것**: TD7 `APP_ENV` 필수화 · TD8 #225 W5 offline SQL · W7 키 canary · W8 회귀 · TD9 AGENTS.md 「v2-dev」. 모두 코디 지시서에 명시된 앞 검수 이월분이다. 배포에 필요한 앱 쪽 손질이라 범위 이탈은 아니다.

## 재확인 남은 것 3

| 남은 것 | 계약 | 판정 |
|---|---|---|
| ① prod migration 이미지 = dev 확인 SHA | TD2 ③ 「입력 = dev 에서 확인한 SHA · 그 SHA 의 이미지로」 | 닫힘 |
| ② 롤백 뒤 브랜치 머리 ≠ 이미지 | TD2 ④ 굵은 문장 · Review Surface 마지막 줄 | 닫힘 |
| ③ 브랜치 만들기 · 구현 발주 줄 | 브랜치 = Non-Goal(2026-11-08 정리됨 — `origin/dev` 존재 확인) · 배포 workflow · compose · Caddyfile = 이 Delivery TD 자체 | 닫힘 |

## 하지 않는 것 · Acceptance 나눔

- Non-Goals 는 다음과 같다. 지시서 셋(Azure 리소스 · 운영 KOS 쓰기 · 앱 배포)을 담았다.
  - Azure · GitHub 준비(사용자) · 브랜치
  - `KOS_TRIAL_WRITES_ON_LIVE=true`
  - Flutter 앱 배포
  - 스키마 백업 · Monitor · Bicep
- **Azure 없이 확인하는 것**:
  - A1 로컬 prod 모양 compose · 상한 · project 독립
  - A2 actionlint + 중지 분기
  - A3 스크립트 dry-run · 비밀값 안 나옴
  - A4 JSON 로그
  - A5 APP_ENV · offline SQL · canary
  - A6 grep
  - A8 grep
- **사용자 준비 뒤 실물**: A7 dev 1회 → prod 1회(헬스 · 두 도메인 TLS). Review Surface 에 「그 전 완료 조건은 로컬 · 문법 · dry-run」이라고 적혀 있다.

## WARN

### W1. 배포할 앱이 `dev` 브랜치에 없다 — 의존 · 순서에 「PR #228 → `dev` 병합」이 빠졌다
- `origin/dev` = `8e4fb4b5` 이고, 최상위에 `AGENTS.md` · `CLAUDE.md` 뿐이다. #224 ~ #232 의 앱(backend · migrations · Dockerfile · health)은 작업 브랜치 `kknaksss/day-data-architecture`(PR #228 · HEAD `8f26612f`)에만 있다.
- 계약 dependencies 는 「#224 · #225 · #226 — 배포할 앱」뿐이다. 그런데 실제 화면 · 로그인 · 시술 현황(#227 · #229 ~ #232)도 같은 PR 에 있다.
- TD2 ① 「`dev` 브랜치 push → 배포」가 돌려면 앱이 먼저 `dev` 에 있어야 한다. A7 의 실물 dev 1회도 그 뒤에야 가능하다.
- 작성 리포트도 code repo 를 `origin/dev`(`8e4fb4b5`)로 잡았다. 그 상태로는 배포 파일이 기댈 Dockerfile · health · `config.py` 가 없다.
- 고칠 방향
  - dependencies 를 「#224 ~ #232(PR #228)」로 넓힌다.
  - 「A7 전에 PR #228 이 `dev` 에 병합돼 있어야 함(병합 = 첫 dev 배포)」을 phases · Review Surface 에 적는다.
  - 구현 워커의 작업 기준 브랜치(PR #228 위에서 할지 · 병합 뒤 `dev` 위에서 할지)를 코디가 정해 브리프에 적는다.

### W2(가벼움). prod migration 워크플로의 「dev 에 같은 revision 이 이미 적용됨」 확인이 Acceptance 에 없다
- A2 는 prod 배포의 중지 분기(SHA 없음 · head 다름)만 검사한다.
- TD2 ③ 의 「dev 에 같은 revision 이 없으면 migration 을 막는다」는 deployment.md 의 prod 안전장치인데 검사 항목이 없다.
- 고칠 방향: A2 에 「prod migration 워크플로는 dev 가 같은 revision 이 아니면 중지」를 한 마디 더한다.

### W3(가벼움). 로컬 `dev` 브랜치 이름 겹침
- 작성 리포트 「주의」에 따르면 `/Users/kknaks/git/CENTURION_DAY` 의 로컬 `dev` 는 옛 `release/v0.1.0-rc.14` 계열이고, 원격 `dev` 와 다르다.
- `dev` 가 이제 배포 트리거 브랜치다. 그래서 그 로컬 브랜치를 실수로 push 하면 옛 코드가 dev 서버로 간다.
- 계약 문제는 아니다. 코디가 실물 배포(A7) 전에 로컬 브랜치를 정리하라고 사용자에게 한 줄 알리면 된다.
