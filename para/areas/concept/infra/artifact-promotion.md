---
type: concept
id: artifact-promotion
title: 산출물 승격 — 한 번 빌드해 dev 에서 확인한 것을 prod 로 (Artifact promotion · Build once, deploy many)
aliases:
  - 빌드 한 번 배포 여러 번
  - build once deploy many
  - prod fast-forward 배포
  - 같은 SHA 이미지
up:
  - 2026-11-12-prod-deploy-re1
tags:
  - 인프라
  - 배포
  - ci-cd
---

# 산출물 승격

**prod 에서 새로 빌드하지 않는다.** dev 에서 빌드 · 배포 · 확인한 커밋의 이미지를 그대로 prod 로 올린다. prod 에 가는 것은 「무엇을 올렸나」 라는 커밋 하나다.

## 정의

- dev 브랜치 머지 → 이미지를 커밋 SHA 로 한 번 빌드 → dev 배포 · 확인.
- prod 브랜치를 **그 커밋으로 fast-forward** 만 한다(merge · squash 금지 — 새 커밋이 생기면 새 SHA 라 확인한 이미지와 다르다).
- prod 배포는 그 SHA 의 이미지를 받아 띄운다. DB migration 은 확인 문자열이 있는 수동 단계로 따로 돌린다.

## 왜 중요한가

prod 에서 다시 빌드하면 「dev 에서 본 것」과 「prod 에 올라간 것」이 같다는 보장이 사라진다(의존성 · 빌드 시점 차이). SHA 하나로 묶으면 롤백도 「이전 SHA 로 다시 올리기」가 된다 → [[ci-cd]]

DAY 첫 prod 배포에서 `prod` 브랜치는 있었지만 워크플로 파일이 없어, 첫 fast-forward push 의 배포가 `revision-mismatch current=none`(DB 가 비어 있음)으로 멈추는 것이 **정상 경로**였다 → migration 수동 실행 → 같은 배포 실행을 다시 돌림.

## 경계와 오해

- **환경 설정은 이미지 밖이다** — 같은 이미지가 env · 비밀로 dev / prod 가 된다 → [[externalized-configuration]] · [[secret-store]]
- **migration 은 승격 대상이 아니다** — 이미지와 달리 되돌리기 어려워 사람이 확인하고 돌린다.
- **멈춤이 실패가 아닐 수 있다** — 순서가 정해진 첫 배포는 일부러 멈추는 단계를 끼고 있다. 사유 코드로 정상 멈춤인지 가른다.

## 함께 보는 개념

- [[zero-downtime-deployment]] — 올리는 방식
- [[web-application-deployment]]

## 출처

- [[2026-11-12-prod-deploy-re1]] §2 「같은 서버 · 다른 스키마 prod 첫 배포」 — CENTURION_DAY `382827d5` · `0b2f8cff` prod fast-forward · deploy-prod run 43153893222 · migrate-prod 43154046130 · `40-architecture/deployment.md`
