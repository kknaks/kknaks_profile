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
  - Signing.xcconfig
  - release · debug 서버 주소
up:
  - 2026-10-01-strong-hajin-deploy
  - 2026-10-22-myeongdong-poc-v2
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

**identifier 는 푸시 토큰의 주소이기도 하다** — APNs 는 번들 id 를 `apns-topic` 으로 받고, 기기 토큰은 그 번들 id 에 묶인다. 명동 PoC v2 시술실 앱은 번들 id 를 바꾼 뒤 옛 토큰이 400 `DeviceTokenNotForTopic` 을 냈다 → [[apns-direct-push]]

### 공개 레포에서 식별자 · 팀을 빼기

번들 id · 팀 id 는 비밀은 아니어도 **공개 레포에 박을 값이 아니다**. Flutter iOS 는 `PRODUCT_BUNDLE_IDENTIFIER = $(APP_BUNDLE_ID)` 로 자리만 두고 값은 gitignore 된 `ios/Flutter/Signing.xcconfig`(`APP_BUNDLE_ID` · `DEVELOPMENT_TEAM`)에, Runner 설정이 그것을 include 한다. 파일이 없으면 서명 없이 시뮬레이터 빌드만 된다. back 은 같은 값을 env(`APNS_BUNDLE_ID`)로 받는다

### release 는 주소를 굽는다

처음엔 기기가 같은 Wi-Fi 의 맥 IP 로 붙게 했다(로그인 화면 서버 주소 칸 · ATS 로컬 허용). 「배포 먼저」 로 바뀌자 **release 빌드는 배포 주소를 빌드 인자(`--dart-define=API_BASE=…`)로 굽고 서버 주소 칸을 없앴다** — 칸은 debug 에만. 내부 테스터에게 가는 앱에 「주소를 바꾸는 칸」 이 있으면 잘못 바꾼 한 대가 조용히 다른 서버를 본다

## 경계와 오해

- **판 ≠ 환경(dev/prod)** — 환경은 같은 앱이 붙는 서버가 다른 것이고, 판은 앱 자체가 다르다. 한 판 안에서도 dev/prod 가 있을 수 있다
- **런타임 분기가 아니다** — 셸 설정이 `include_str!` 로 박히므로 빌드 시점에 결정된다. 판이 섞인 빌드(오버레이는 A, 설정은 B)는 build.rs 가 막아야 한다
- **release / debug 도 판이 아니다** — 같은 앱의 빌드 모드다. 다만 「어디에 붙나」 를 빌드 모드가 정하게 하면 판과 같은 성질(빌드 시점에 굳음)을 얻는다
- **서명·공증은 판마다 따로** — 산출물이 다르니 [[code-signing]] 도 판마다 한다

## 함께 보는 개념

- [[code-signing]] — 판마다 서명·공증
- [[build]] — 빌드 시점에 설정을 굳히는 것
- [[apns-direct-push]] — 식별자에 묶이는 푸시 토큰
- [[externalized-configuration]] — 레포 밖에 두는 설정 값

## 출처

- [[2026-10-22-myeongdong-poc-v2]] §2 — Flutter iOS 시술실 앱: 번들 id · 팀 id 를 gitignore `Signing.xcconfig` 로 · release = 배포 주소 고정, 서버 주소 칸은 debug 만(SPEC-004 §2.4 · `config/server.dart` · 실기기 T8)
- [[2026-10-01-strong-hajin-deploy]] — 개인 Strong Hajin / 회사 medi-ax 를 flavors 오버레이로 가르고 identifier 를 판마다 고정(코드 #8)
