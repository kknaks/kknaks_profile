---
type: concept
id: workload-identity
title: 워크로드 신원 — 장기 키 없이 클라우드에 붙기 (Workload Identity · OIDC · Managed Identity)
aliases:
  - managed identity
  - system identity
  - 관리 ID
  - GitHub OIDC
  - OIDC 배포
  - 장기 키 없이
  - federated credential
up:
  - 2026-11-09-day-data-architecture
tags:
  - 인프라
  - 인증
  - 배포
  - azure
---

# 워크로드 신원 — 장기 키 없이 클라우드에 붙기

사람이 아닌 실행체(배포 파이프라인 · VM 위의 앱)가 클라우드 자원에 접근할 때, **복사해 넣은 장기 키 대신 그 실행체 자신의 신원**으로 짧은 토큰을 받아 쓰는 것. 「누가 이 키를 갖고 있나」 를 관리할 필요가 없어진다.

## 정의

두 갈래가 있다.

1. **바깥 실행체 — OIDC 연합** — GitHub Actions 가 실행마다 「이 레포 · 이 브랜치 · 이 environment 의 실행」 이라는 OIDC 토큰을 받고, 클라우드는 미리 등록한 조건(연합 자격)과 맞을 때만 단기 토큰으로 바꿔 준다. 저장소 Secrets 에 클라우드 키를 넣지 않는다
2. **안쪽 실행체 — 관리 ID(managed identity)** — VM 자체에 신원이 붙는다. VM 위의 프로세스는 메타데이터 엔드포인트에서 토큰을 받아 레지스트리 pull · 비밀 보관소 읽기를 한다. 키 파일이 디스크에 없다
3. **권한은 신원마다 역할로 붙인다** — 배포 신원에는 「레지스트리 push · VM 명령 실행」, VM 신원에는 「레지스트리 pull · 비밀 읽기」 처럼 일마다 가른다

## 사용 예시

DAY 배포:

```text
GitHub Actions ─OIDC─▶ 클라우드 단기 토큰 ─▶ ACR push · VM run-command
VM(system identity) ─▶ ACR pull · Key Vault 비밀 읽기
SSH 키 · 클라우드 비밀 키: 저장소에 0
```

## 왜 중요한가

- **새는 키가 없다** — 장기 키는 저장소 · 로그 · 사람 노트북으로 퍼지고, 회수하려면 어디 있는지부터 찾아야 한다. 신원 기반은 토큰이 짧게 살고 조건(레포 · 브랜치)이 붙는다
- **배포가 SSH 를 안 쓴다** — 원격 명령도 신원으로 부르면 서버에 열린 SSH 포트와 그 키가 필요 없다 → [[ci-cd]]

## 경계와 오해

- **신원이 있어도 역할이 없으면 403** — 신원을 만드는 것과 권한(역할 배정)을 주는 것은 다른 단계다. 배포가 「인증은 됐는데 거절」 이면 역할 배정을 본다
- **연합 조건이 넓으면 키 없는 것이 의미 없다** — 「아무 브랜치」 를 허용하면 리뷰 안 된 브랜치가 운영 배포 권한을 갖는다. environment · 브랜치로 좁힌다. DAY 도 environment 배포 브랜치 제한은 남은 일로 적었다
- **관리 ID ≠ 비밀 보관소** — 신원은 「누구인가」, 보관소는 「무엇을 읽나」 다. 둘을 같이 써야 키 0 이 된다 → [[secret-store]]
- **[[delegated-authorization]] 과 닮았지만 주체가 다르다** — 그쪽은 사람이 앱에 권한을 위임하는 것, 여기는 실행체 자신의 신원이다

## 함께 보는 개념

- [[secret-store]] — 신원으로 읽는 비밀의 자리
- [[ci-cd]] — 배포 파이프라인이 이 신원으로 돈다
- [[delegated-authorization]] — 토큰을 받는 다른 갈래
- [[jwt]] — OIDC 토큰의 모양

## 출처

- [[2026-11-09-day-data-architecture]] §2 — DAY 배포: GitHub OIDC(장기 키 없이) · VM system identity 로 ACR pull · Key Vault 읽기 · SSH 없이 run-command(코드 `937dbb68` · 설정 `day.json` infra)
