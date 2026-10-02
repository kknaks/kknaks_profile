---
type: concept
id: shared-session-storage
title: 여러 파드가 이어 쓰는 세션은 공유 저장소에 둔다 (Shared Session Storage)
aliases:
  - 세션 공유
  - 파드 로컬 세션
  - AI 세션 resume
  - codex runtime home
  - 세션 홈 공유
up:
  - 2026-10-02-strong-hajin-polish
tags:
  - kubernetes
  - state
  - ai-cli
---

# 여러 파드가 이어 쓰는 세션은 공유 저장소에 둔다

한 프로세스가 연 세션(AI CLI 대화 기록·상태 파일)을 **다른 파드가 이어 써야 하면**, 그 세션 파일은 컨테이너 로컬이 아니라 **두 파드가 같이 보는 저장소**에 있어야 한다. 컨테이너 로컬 디렉터리는 파드마다 따로이고, 재시작·재배포 때 사라진다.

## 정의

- 증상: 이어 쓰기(resume)가 모델에 닿기도 전에 수백 ms 만에 「세션 없음」으로 실패하고, 재시도해도 같은 이유로 실패한다
- 해결의 핵심은 **공유**다 — 앱이 이미 쓰는 경로에 공유 볼륨(같은 노드면 hostPath)을 그대로 마운트하면 코드·env 변경 없이 닫힌다
- 공유는 원인을 닫고, **안전장치**는 공유 밖 원인(공유 도입 전에 열린 세션 · 볼륨 장애)을 막는다 — 세션을 잇지 못하면 저장된 원문 전량으로 새 세션을 연다(콜드스타트). 안전장치만으로는 매번 맥락을 잃는다
- 공유하면 상태 파일(sqlite 등)을 여러 파드가 동시에 쓴다 — 같은 커널이면 잠금이 원리상 맞지만 증명은 따로 본다(반영 뒤 오류 관찰, 문제면 세션 파일만 공유하고 나머지는 파드별)

## 경계와 오해

- 인증 볼륨을 공유했다고 세션도 공유된 게 아니다 — 같은 CLI 라도 **인증 홈과 런타임 홈이 다를 수 있다**(Strong Hajin: `/root/.codex` 는 PVC, 실제 `CODEX_HOME` 은 `/app/.scax/codex-runtime`)
- 「코드로만 닫자」는 판단이 틀리기 쉽다 — 재배포마다 세션이 사라지면 콜드스타트가 상시 경로가 된다
- hostPath type `Directory` 는 노드 디렉터리를 먼저 만들어야 한다 — 없으면 파드가 뜨지 않는다(마운트가 빠졌을 때 VM 디스크에 조용히 쓰지 않게 일부러)

## 함께 보는 개념

- [[cold-start]] · [[kubernetes-workload]] · [[no-silent-fallback]] · [[stateless-protocol]]

## 출처

- [[2026-10-02-strong-hajin-polish]] §2·§3 — Strong Hajin 운영 회의 요약 실패(`research-meeting-summary.md`), 인프라 MediSolveAIDev/k8s_infra_mac#7, 코드 `dd4bd7c`, 배포 직후 옛 대화 세션 소실
