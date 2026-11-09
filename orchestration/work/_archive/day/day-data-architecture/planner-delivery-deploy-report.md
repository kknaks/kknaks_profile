# planner-delivery-deploy 결과 보고 — done (human gate · 승인 안 함)

- **[CENTURION_DAY#233](https://github.com/MediSolveAIDev/CENTURION_DAY/issues/233)** 「DAY v2 서버 배포 — dev · prod 한 VM」 · key `day/v2-server-deploy` · **L3** · 라벨 `delivery-plan:review` · `execution-plan:ready` · `spec-baseline:pending`.
- **plan_digest = `sha256:d8cf855bcdf7914885a568cfc5d262c901225dbf43511854713331482ceb3cd7`**
- 파일 `delivery/v2-server-deploy.json` · `.plan.json` · `.apply.json`. code repo = CENTURION_DAY `dev`(`8e4fb4b5` — 원격 기본 브랜치 · scratchpad 에 그 ref 로 만든 clone). mediness origin/main `3a220ace`(PR #909 미머지).

## target

- `target_specs = ["DAY-DEPLOYMENT"]`(deployment.md frontmatter id). 스키마는 문자열 목록만 요구하고 CLI 가 받아들였다 — SPEC 이 아니라 아키텍처 정본이라는 점 · 머지 뒤 재결속을 Review Surface 첫 줄에 적었다.

## 계약 요약

- **TD 10**: 정본 = deployment.md(값은 짓지 않음) · Actions 넷(dev push 배포 · prod fast-forward 배포(같은 SHA 없으면 · head 다르면 중지) · **prod migration 수동 승인 — 입력 = dev 에서 확인한 SHA · 그 이미지로 실행 · dev 같은 revision 확인**(남은 것 ①) · **롤백 수동(환경 · 이전 성공 SHA) · forward-only · 브랜치 머리를 되돌리지 않고 다음 push 가 최신을 다시 올림**(남은 것 ②) · 한 concurrency group) · VM run-command 스크립트(Key Vault → /etc/day/{env} · 이력) · compose 셋 · redis 환경마다 · 메모리 상한 · 포트 80/443 뿐 · Caddyfile 두 도메인 · JSON 로그(app_env) · APP_ENV 필수 · #225 W5 offline SQL CREATE SCHEMA · search_path · W7 키 canary · W8 은 #226 반영(회귀만) · AGENTS.md 「v2-dev」 고침 · env 이름 · KOS_TRIAL_WRITES_ON_LIVE prod 첫 배포 false.
- **Acceptance A1 ~ A8**: 로컬 prod 모양 compose 두 환경(포트 · 상한 · project 독립) · actionlint + 중지 분기 · 스크립트 dry-run(비밀값 안 나옴) · JSON 로그 테스트 · APP_ENV · offline SQL · canary · 비밀값 · Azure 이름 없음(grep) · **실제 Azure 는 사용자 준비 뒤 dev 1회 → prod 1회** · AGENTS.md grep.
- **Non-Goals**: Azure · GitHub 준비(사용자) · **브랜치 만들기(2026-11-08 정리됨 — 이 Delivery 몫 아님 · 남은 것 ③)** · 운영 KOS 쓰기 켜기 · 앱 배포 · 스키마 단위 백업 · Monitor · Bicep.
- **Review Surface**: 아키텍처 target · pending · L3 근거(배포 · 도메인 · credential · prod migration · 같은 VM) · 실물은 사용자 준비 뒤 · deployment.md 미결(메모리 · 백업 · KOS IP · 스키마 생성 권한 · 승인 세부 · 신뢰 프록시) · 롤백 뒤 브랜치 머리 ≠ 이미지.
- **담당: backend(인프라 파일 포함)** — 스키마에 칸이 없어 리포트에만.

## 재확인 검수 남은 것 3 — 계약 문장으로 닫음

1. migration 이미지 SHA → TD2 ③ 「입력 = dev 에서 확인한 SHA · 그 SHA 의 이미지로」.
2. 롤백 뒤 브랜치 → TD2 ④ · Review Surface 「브랜치 머리를 되돌리지 않음 · 다음 push 가 최신을 올림」.
3. 브랜치 만들기 / 구현 줄 → 브랜치는 Non-Goal(이미 정리됨) · 배포 workflow · compose · Caddyfile 구현이 이 Delivery 의 TD 자체. deployment.md 준비 목록 문구는 그대로 둠(필요하면 다음 문서 판).

## 주의

- 로컬 `/Users/kknaks/git/CENTURION_DAY` 의 로컬 `dev` 브랜치는 원격 `dev` 와 다르다(옛 `release/v0.1.0-rc.14`) — clone 은 원격 추적 ref(`origin/dev`)로 만들었다. 코디가 로컬 브랜치를 정리하면 헷갈림이 줄어든다.
