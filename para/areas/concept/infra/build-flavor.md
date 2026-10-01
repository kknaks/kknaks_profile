---
type: concept
id: build-flavor
title: 빌드 판 (Build Flavor)
aliases:
  - 빌드 변형
  - build variant
  - flavor
  - 앱 두 판
  - bundle identifier
  - 앱 식별자
up:
  - 2026-10-01-strong-hajin-deploy
tags:
  - infra
  - 빌드
  - desktop
  - tauri
---

# 빌드 판 (Build Flavor)

**코드 한 벌에서 설정만 바꿔 서로 다른 앱 여러 개를 굽는 것.** 판마다 이름·식별자·접속 주소가 다르고, OS 는 그것들을 **완전히 다른 앱**으로 본다.

## 정의

판은 「코드」가 아니라 **빌드 시점에 끼워 넣는 설정 묶음**이다. Strong Hajin 데스크톱 셸은 `src-tauri/flavors/<판>/` 에 `tauri.conf` 오버레이·셸 설정(origin)·capabilities 를 두고 `SHELL_FLAVOR` 로 하나를 고른다.

| 판 | 이름 | identifier | origin |
|---|---|---|---|
| 개인 | Strong Hajin | `app.stronghajin.desktop` | 미정 |
| 회사 | medi-ax | `app.ax.desktop` | `https://ax.medisolveai.xyz` |

## 왜 중요한가

**identifier 는 이름표가 아니라 저장소 열쇠다.** macOS 는 쿠키·키체인·설정을 bundle identifier 별로 가른다. 그래서

- **판 안에서** identifier 를 바꾸면 → 새 앱이 되어 로그인이 날아간다(그래서 「판마다 고정」을 시험으로 박았다)
- **판 사이에서** identifier 를 안 가르면 → 개인판과 회사판이 같은 저장소를 공유해 섞인다

처음엔 「이름만 medi-ax 로」였는데, 사용자가 개인/회사 두 앱을 원한다는 게 드러나 판 분리로 갔다.

## 경계와 오해

- **판 ≠ 환경(dev/prod)** — 환경은 같은 앱이 붙는 서버가 다른 것이고, 판은 앱 자체가 다르다. 한 판 안에서도 dev/prod 가 있을 수 있다
- **런타임 분기가 아니다** — 셸 설정이 `include_str!` 로 박히므로 빌드 시점에 결정된다. 판이 섞인 빌드(오버레이는 A, 설정은 B)는 build.rs 가 막아야 한다
- **서명·공증은 판마다 따로** — 산출물이 다르니 [[code-signing]] 도 판마다 한다

## 함께 보는 개념

- [[code-signing]] — 판마다 서명·공증
- [[build]] — 빌드 시점에 설정을 굳히는 것

## 출처

- [[2026-10-01-strong-hajin-deploy]] — 개인 Strong Hajin / 회사 medi-ax 를 flavors 오버레이로 가르고 identifier 를 판마다 고정(코드 #8)
