---
type: concept
id: unlisted-app-distribution
title: Unlisted 앱 배포 — 검색에는 없고 링크로만 받는 App Store 앱
aliases:
  - Unlisted
  - 비공개 앱 배포
  - 링크 배포
  - unlisted app
up:
  - 2026-11-12-prod-deploy-re1
tags:
  - 모바일
  - 앱스토어
  - 배포
---

# Unlisted 앱 배포

App Store 심사를 통과한 앱이지만 검색 · 카테고리 · 「개발자의 다른 앱」에 보이지 않고, **직접 링크로만** 설치할 수 있게 하는 배포 방식.

## 정의

- 앱 설정이 아니라 **Apple 에 따로 내는 신청서**(웹 양식 · Account Holder · Admin · App Manager)로 요청한다. API 없음.
- 신청 조건: App Review 에 제출됐거나 이미 App Store 에 있음. 베타 · 출시 전은 거절.
- 승인되면 가격 및 사용 가능 여부의 배포 방식이 Unlisted 로 바뀌고 **이후 모든 버전에 적용**된다.
- **되돌릴 수 없다** — 공개나 맞춤형 앱(Apple Business 비공개)으로 다시 바꿀 수 없다.

## 왜 중요한가

특정 조직의 사람만 쓰는 앱은 셋 중 하나를 고른다.

| 방식 | 대가 |
|---|---|
| 공개 | 쓸 수 없는 일반 사용자에게 보인다 |
| 맞춤형 앱(Apple Business) | 고객 조직마다 Apple Business 등록이 필요 — 조직이 늘 때마다 절차 |
| Unlisted | 링크가 있으면 누구나 설치 — 보안은 로그인이 맡는다 |

DAY 는 병원이 계속 늘고 병원들이 Apple Business 를 쓰지 않아 Unlisted 를 골랐다. 출시를 수동으로 두면 심사 통과 뒤 Unlisted 승인 전에 공개될 걱정이 없다.

## 경계와 오해

- **비공개가 아니다** — 링크만 있으면 누구나 받는다. 데이터 보호는 계정 인증이 해야 한다.
- **TestFlight 대체가 아니다** — 출시 상태의 앱만 된다.
- **한 방향 결정이다** — 나중에 공개로 돌릴 계획이 있으면 신청하지 않는다.

## 함께 보는 개념

- [[app-privacy-disclosure]] — 같은 제출에서 함께 채우는 칸
- [[code-signing]]

## 출처

- [[2026-11-12-prod-deploy-re1]] §2 「Unlisted 배포」 — DAY 정식 앱 0.1.0 신청 · 신청서 동의 문구(https://developer.apple.com/support/unlisted-app-distribution/ · `40-architecture/mobile-deployment.md`)
